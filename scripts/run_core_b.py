"""Core-B experiments, run as pre-registered in docs/protocol.md (FROZEN v1, git tag protocol-v1).

Run:  python -I -X utf8 scripts/run_core_b.py            full run (~30-60 min on 12 cores), writes results/core_b/
      python -I -X utf8 scripts/run_core_b.py --quick    forward design only, B=200 (debugging; does not run the check)
      python -I -X utf8 scripts/run_core_b.py --check    self-check only (toy CQR + checks on the written outputs)

Every choice the protocol leaves open is listed in CHOICES and copied to results/core_b/run_log.md.
Input: data/processed/features.csv (lag 5). Lag 0/10 features are rebuilt in memory with build_features.build(lag);
features.csv is never written by this script.
"""
import os
os.environ.setdefault("OMP_NUM_THREADS", "1")  # one thread per HGB fit; parallelism is across runs
import argparse, hashlib, io, math, platform, sys, time
from datetime import date

import numpy as np
import pandas as pd
import joblib, scipy, sklearn
from joblib import Parallel, delayed
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.linear_model import QuantileRegressor

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import build_features as bf  # noqa: E402
from parse_nchmf import STATIONS as CANON28  # noqa: E402

P = lambda *a: os.path.join(ROOT, *a)
OUT = P("results", "core_b")
SEED = 20261101
TAUS = np.round(np.arange(0.05, 0.951, 0.05), 2)            # protocol 5: 0.05, 0.10, ..., 0.95
TUNE_TAUS = np.array([0.05, 0.5, 0.95])
THR = (1, 2, 4)
ALPHA = 0.10                                                 # 90% intervals
TEST_SEASONS = (2024, 2025, 2026)
B = 2000
PGRID = np.round(np.arange(0.01, 0.995, 0.01), 2)            # probability thresholds and C/L grid
INLAND_MIN_N = 30
PCTT4 = ["Tân An", "Bến Lức", "Cầu Quan", "Gò Quao"]
NUM = ["log1p_smax_cur", "log1p_delta_smax", "km_from_mouth", "inland_canal", "dekad_of_season", "q_mean10",
       "q_mean30", "q_min30", "q_anom30", "tide_abscos_mean", "tide_perigee_cos", "oni"]
RG = ["SaiGon", "VamCo", "Tien", "HamLuong", "CoChien", "Hau", "GanhHao", "WestSea"]
HGB_GRID = [dict(max_depth=d, learning_rate=lr, min_samples_leaf=l) for d in (2, 3, 4) for lr in (0.03, 0.1)
            for l in (10, 30)]
HGB_ITERS = (100, 500)
QR_GRID = [dict(alpha=a) for a in (0.0, 1e-3, 1e-2, 1e-1)]
QCOL = [f"q{int(round(t * 100)):02d}" for t in TAUS]
CQCOL = ["c" + c for c in QCOL]

CHOICES = [
    "Predictors (protocol 4): log1p_smax_cur; change from previous dekad = log1p_delta_smax (log scale, matches the "
    "log1p target); km_from_mouth; inland_canal; river_group one-hot (8 groups, the 'estuary/branch group'); "
    "dekad_of_season; q_mean10, q_mean30, q_min30, q_anom30 (GloFAS, lag L); tide_abscos_mean (spring-neap index) and "
    "tide_perigee_cos (perigee proximity) for the target dekad; oni. tide_spring_days and tide_perigee_min are not "
    "used (protocol names one spring-neap index and one perigee index).",
    "Both models are fitted on log1p(Smax) (protocol states it for the linear model; the same for HGB so that the "
    "back-transform and conformal scores are on one scale). Quantiles are sorted per row (non-crossing) and "
    "back-transformed with expm1.",
    "Linear model missing values: a missing-indicator column for log1p_delta_smax, then every NaN replaced by the "
    "training-set median; features standardized with training mean/sd; columns constant in training dropped. All "
    "fitted on the (inner) training set only. HGB uses NaN natively.",
    "Hyperparameter grids. HGB: max_depth {2,3,4} x learning_rate {0.03,0.1} x min_samples_leaf {10,30} x max_iter "
    "{100,500} (24 combinations, endpoints/midpoint of the protocol ranges), other parameters library defaults, "
    "early_stopping off. QuantileRegressor: alpha {0, 0.001, 0.01, 0.1} on standardized features, solver highs. "
    "One hyperparameter set per model per run (shared by all 19 quantile levels).",
    "Tuning criterion: mean pinball loss on the log1p scale over levels 0.05, 0.5, 0.95 (not all 19, to keep the "
    "~250 runs affordable), pooled over the leave-one-season-out folds of the training seasons. Ties: first in grid "
    "order. Tuning is redone inside every run (also inside every leave-station-out/leave-province-out run, with the "
    "held-out group removed).",
    "The cross-conformal (CV+) folds are the same leave-one-season-out folds, refitted with the chosen "
    "hyperparameters on all 19 levels. The hyperparameters were chosen on the same folds, so the calibration scores "
    "are not nested (small optimism possible).",
    "CQR scores and intervals on the log1p scale: E_i = max(q05_k(i)(x_i) - y_i, y_i - q95_k(i)(x_i)); CV+ interval "
    "lower = floor(0.1(n+1))-th smallest of q05_k(i)(x) - E_i, upper = ceil(0.9(n+1))-th smallest of q95_k(i)(x) + "
    "E_i (Barber et al. 2021 CV+ applied to CQR); back-transformed with expm1.",
    "Conformalized quantile grid (used for probabilities and CRPS): each level tau separately, one-sided CV+: score "
    "s_i = y_i - q_tau,k(i)(x_i); q'_tau(x) = ceil(tau(n+1))-th smallest of q_tau,k(i)(x) + s_i. Then sorted across "
    "tau. The CQR 90% interval is computed separately (two-sided score), so cq05/cq95 need not equal lo_cqr/hi_cqr.",
    "Exceedance probabilities: CDF linear in log1p(Smax) between the 19 conformalized quantiles; beyond 0.05/0.95 "
    "extended linearly with the slope of the end segment; CDF clipped to [0.01, 0.99]; P(Smax > c) = 1 - CDF. "
    "Probabilities come from the plain (non-Mondrian) grid.",
    "Mondrian groups: km <= 15 '0-15', 15 < km <= 40 '15-40', km > 40 '>40'. Inland canals (inland_canal = 1) form "
    "their own group when the run's calibration set holds >= 30 inland rows, else they stay in their km group.",
    "Point forecast = median of the full model (raw, sorted), as protocol 5 states. MAE of the conformalized median "
    "(cq50) is reported as mae_cmed.",
    "Climatology benchmark: observations = every station-dekad Smax in features.csv (smax_cur, incl. ODV rows and "
    "rows without a target) of seasons before the test season (incl. the single 2020 bulletin); dekad-of-year of the "
    "TARGET dekad. Fallback station mean. The benchmark is the same in all designs (it uses the station's own "
    "training-season history also under leave-station/province-out, where only the models lose the station).",
    "Brier for benchmarks (a) and (b): their deterministic forecast as a 0/1 probability (value > c). A probabilistic "
    "climatology (share of training-season observations > c at the station-dekad, same fallback) is reported as "
    "climfreq, outside the verdicts.",
    "Yes/no conversion of model probabilities: threshold p* on 0.01..0.99 maximising the Peirce score on the "
    "training rows' out-of-fold calibrated probabilities (fold model quantiles + one-sided conformal shift from the "
    "other folds' scores); median of tied maximisers; 0.5 if the training rows have no events or no non-events. "
    "Forecast 'yes' when p > p*. Benchmarks: 'yes' when value > c. False-alarm rate = false alarms / non-events "
    "(probability of false detection), so PSS = hit rate - false-alarm rate.",
    "CRPS = 2 x mean pinball loss over the 19 levels (g/L scale, conformalized grid; raw grid as crps_raw).",
    "Relative economic value at 4 g/L (Richardson 2000), cost/loss a on 0.01 steps, base rate = observed frequency in "
    "the (resampled) sample; rows with an official forecast only (paired). The model's user acts when P(>4) > a "
    "(main, rev_area_*). The envelope over all probability thresholds (Richardson's potential value) is reported as "
    "rev_area_model_env. Areas: trapezoid over a in [0.1, 0.9], value not clipped at 0.",
    "Bootstrap: issue dates resampled with replacement within each test season (pooled = per-season resamples "
    "concatenated), 2,000 resamples, same seed for every forecaster of a design/model (paired). Percentile 95% CIs. "
    "Metrics are ratio-of-sums over the resampled dates.",
    "Verdicts use the pooled forward design (main variant). H2 coverage criteria are applied to the point estimate. "
    "H1/H3 are judged per model; the protocol pre-registers two models and no primary one, so both are reported.",
    "H2 'plain split/cross-conformal' = the plain CV+ CQR interval of this script (lo_cqr/hi_cqr).",
    "Test stations: the 28 canonical stations in every design; extra stations (Cầu Nổi, Xẻo Rô, Mỹ Tho, Đồng Tâm, "
    "Cà Mau) are training-only. Leave-province-out removes extra stations of the held-out province too.",
    "Sensitivity runs (forward design only): lag0, lag10, noODV (ODV rows removed from training and from the "
    "climatology pool), noSD42, stationid (station one-hot added; H1 only).",
]


# ---------------------------------------------------------------- data
def doy(d):
    d = pd.to_datetime(pd.Series(d))
    return ((d.dt.month - 1) * 3 + (d.dt.day > 10) + (d.dt.day > 20)).to_numpy()


def load_features(lag=5):
    if lag == 5:
        df = pd.read_csv(P("data/processed/features.csv"))
    else:
        b, _ = bf.build(lag)
        bf.self_check(b, lag)
        df = pd.read_csv(io.StringIO(b.to_csv(index=False)))
    df["issue_date"] = pd.to_datetime(df.issue_date)
    # protocol 2 exclusions: 2021-01-05 bulletin and An Định "202" are already absent; any value > 45 g/L
    assert (df.issue_date != "2021-01-05").all()
    assert not (df.y_smax_next > 45).any() and not (df.smax_cur > 45).any()
    df.loc[df.bench_official > 45, "bench_official"] = np.nan
    assert not ((df.issue_date == "2026-04-20") & (df.station == "An Định") & df.bench_official.notna()).any()
    assert set(df.river_group) <= set(RG), set(df.river_group)
    df["toy"] = doy(df.target_end)   # dekad-of-year of the target dekad
    df["oy"] = doy(df.issue_date)    # dekad-of-year of the observed (current) dekad
    return df


def climatology(test, pool, test_season):
    """Station mean at the target dekad-of-year over seasons < test_season; fallback station mean (protocol 5b).
    Also the share of those observations above 1, 2, 4 g/L (climfreq, secondary)."""
    p = pool[pool.season < test_season]
    out = pd.DataFrame(index=test.index)
    key = pd.MultiIndex.from_arrays([test.station, test.toy])
    for name, v in [("bench_clim", p.smax_cur)] + [(f"clim_freq_gt{c}", (p.smax_cur > c).astype(float)) for c in THR]:
        g1 = v.groupby([p.station, p.oy]).mean()
        g0 = v.groupby(p.station).mean()
        a = g1.reindex(key).to_numpy()
        fb = g0.reindex(test.station).to_numpy()
        if name == "bench_clim":
            out["clim_src"] = np.where(np.isnan(a), np.where(np.isnan(fb), "none", "station_mean"), "station_dekad")
        out[name] = np.where(np.isnan(a), fb, a)
    return out


def feats(d, station_id=False, stations=()):
    X = d[NUM].astype(float).copy()
    for g in RG:
        X["rg_" + g] = (d.river_group == g).astype(float)
    if station_id:
        for s in stations:
            X["st_" + s] = (d.station == s).astype(float)
    return X


def lin_prep(Xtr, Xouts):
    def ind(X):
        X = X.copy()
        X["miss_delta"] = X.log1p_delta_smax.isna().astype(float)
        return X
    A = ind(Xtr)
    med = A.median()
    A = A.fillna(med)
    mu, sd = A.mean(), A.std(ddof=0)
    keep = (sd > 1e-12).to_numpy()
    f = lambda X: ((ind(X).fillna(med) - mu) / sd.where(sd > 1e-12, 1.0)).to_numpy(float)[:, keep]
    return f(Xtr), [f(x) for x in Xouts]


# ---------------------------------------------------------------- models
def fit_predict(kind, hp, Xtr, ytr, Xouts, taus):
    """One model per quantile level; returns {hp_key: [array (n_out, len(taus)) per X in Xouts]} on the log1p scale.
    HGB without max_iter in hp: one fit with max(HGB_ITERS) trees gives predictions after each count (staged)."""
    hp = dict(hp)
    if kind == "qr":
        A, Xo = lin_prep(Xtr, Xouts)
        outs = [np.empty((len(x), len(taus))) for x in Xo]
        for j, t in enumerate(taus):
            m = QuantileRegressor(quantile=float(t), alpha=hp["alpha"], solver="highs").fit(A, ytr)
            for o, x in zip(outs, Xo):
                o[:, j] = m.predict(x)
        return {tuple(hp.items()): outs}
    iters = (hp.pop("max_iter"),) if "max_iter" in hp else HGB_ITERS
    res = {it: [np.empty((len(x), len(taus))) for x in Xouts] for it in iters}
    for j, t in enumerate(taus):
        m = HistGradientBoostingRegressor(loss="quantile", quantile=float(t), max_iter=max(iters), early_stopping=False,
                                          random_state=SEED, **hp).fit(Xtr.to_numpy(float), ytr)
        for i, x in enumerate(Xouts):
            for k, s in enumerate(m.staged_predict(x.to_numpy(float)), 1):
                if k in res:
                    res[k][i][:, j] = s
    return {tuple(hp.items()) + (("max_iter", it),): v for it, v in res.items()}


def pinball(y, q, taus):
    d = y[:, None] - q
    return np.maximum(taus * d, (taus - 1) * d)


def run(kind, train, test, Xf):
    """Tune by leave-one-season-out inside the training seasons, refit the CV+ fold models and the full model."""
    Xtr, Xte = Xf(train), Xf(test)
    y = np.log1p(train.y_smax_next.to_numpy(float))
    seas = train.season.to_numpy()
    folds = sorted(set(seas))
    loss = {}
    for hp in (QR_GRID if kind == "qr" else HGB_GRID):
        for k in folds:
            tr = seas != k
            for key, (pr,) in fit_predict(kind, hp, Xtr[tr], y[tr], [Xtr[~tr]], TUNE_TAUS).items():
                loss[key] = loss.get(key, 0.0) + pinball(y[~tr], pr, TUNE_TAUS).sum() / (len(y) * len(TUNE_TAUS))
    best = min(loss, key=loss.get)
    oof = np.empty((len(y), len(TAUS)))
    fte = np.empty((len(folds), len(test), len(TAUS)))
    fid = np.empty(len(y), int)
    for i, k in enumerate(folds):
        tr = seas != k
        a, b = next(iter(fit_predict(kind, best, Xtr[tr], y[tr], [Xtr[~tr], Xte], TAUS).values()))
        oof[~tr], fte[i], fid[~tr] = np.sort(a, 1), np.sort(b, 1), i
    full = np.sort(next(iter(fit_predict(kind, best, Xtr, y, [Xte], TAUS).values()))[0], 1)
    return dict(hp=dict(best), loss=loss, y=y, oof=oof, fid=fid, fte=fte, full=full, folds=folds)


# ---------------------------------------------------------------- conformal
def kth(M, k):
    """k-th smallest (1-based) along axis 0; -inf if k < 1, +inf if k > n (finite-sample conformal convention)."""
    n = M.shape[0]
    if k < 1:
        return np.full(M.shape[1:], -np.inf)
    if k > n:
        return np.full(M.shape[1:], np.inf)
    return np.partition(M, k - 1, axis=0)[k - 1]


def lo_rank(n): return math.floor(round(ALPHA * (n + 1), 9))
def hi_rank(n): return math.ceil(round((1 - ALPHA) * (n + 1), 9))


def cqr(res, gcal=None, gte=None):
    """CV+ CQR on the 0.05/0.95 levels (log1p scale); Mondrian if groups are given."""
    y, oof, fid, fte = res["y"], res["oof"], res["fid"], res["fte"]
    E = np.maximum(oof[:, 0] - y, y - oof[:, -1])
    gcal = np.zeros(len(y)) if gcal is None else gcal
    gte = np.zeros(fte.shape[1]) if gte is None else gte
    lo, hi = np.empty(fte.shape[1]), np.empty(fte.shape[1])
    for g in np.unique(gte):
        i, j = gcal == g, gte == g
        n = int(i.sum())
        lo[j] = kth(fte[:, :, 0][fid[i]][:, j] - E[i, None], lo_rank(n))
        hi[j] = kth(fte[:, :, -1][fid[i]][:, j] + E[i, None], hi_rank(n))
    return lo, hi


def conformal_grid(res):
    """One-sided CV+ per level: q'_tau(x) = ceil(tau(n+1))-th smallest of q_tau,k(i)(x) + (y_i - q_tau,k(i)(x_i))."""
    y, oof, fid, fte = res["y"], res["oof"], res["fid"], res["fte"]
    n = len(y)
    out = np.column_stack([kth(fte[:, :, j][fid] + (y - oof[:, j])[:, None], math.ceil(round(t * (n + 1), 9)))
                           for j, t in enumerate(TAUS)])
    return np.sort(out, 1)


def oof_conformal_grid(res):
    """Out-of-fold calibrated grid for the training rows: fold model quantiles + one-sided shift from other folds."""
    y, oof, fid = res["y"], res["oof"], res["fid"]
    out = np.empty_like(oof)
    for i in np.unique(fid):
        m = fid == i
        n = int((~m).sum())
        for j, t in enumerate(TAUS):
            out[m, j] = oof[m, j] + kth((y - oof[:, j])[~m], math.ceil(round(t * (n + 1), 9)))
    return np.sort(out, 1)


def exceed_prob(q, c):
    """P(Smax > c) from a sorted log1p quantile grid: CDF linear between levels, end-segment slope beyond 0.05/0.95,
    CDF clipped to [0.01, 0.99]."""
    x = math.log1p(c)
    F = np.empty(len(q))
    for r, row in enumerate(q):
        if x < row[0]:
            w = row[1] - row[0]
            F[r] = TAUS[0] - 0.05 / w * (row[0] - x) if w > 0 else 0.0
        elif x > row[-1]:
            w = row[-1] - row[-2]
            F[r] = TAUS[-1] + 0.05 / w * (x - row[-1]) if w > 0 else 1.0
        else:
            F[r] = np.interp(x, row, TAUS)
    return 1 - np.clip(F, 0.01, 0.99)


def choose_pstar(p, e):
    if e.all() or (~e).all():
        return 0.5
    yes = p[:, None] > PGRID[None, :]
    pss = (yes & e[:, None]).sum(0) / e.sum() - (yes & ~e[:, None]).sum(0) / (~e).sum()
    return float(np.median(PGRID[pss >= pss.max() - 1e-12]))


def dist_group(d, inland_sep):
    km = d.km_from_mouth.to_numpy(float)
    assert not np.isnan(km).any()
    g = np.where(km <= 15, "0-15", np.where(km <= 40, "15-40", ">40")).astype(object)
    if inland_sep:
        g = np.where(d.inland_canal.to_numpy() == 1, "inland", g)
    return g


# ---------------------------------------------------------------- one run
KEEP = ["issue_date", "season", "station", "province_canon", "km_from_mouth", "inland_canal", "obs_source",
        "y_smax_next", "bench_persist", "bench_official", "smax_cur", "toy"]


def task(sp):
    t0 = time.time()
    tr, te = sp["train"], sp["test"]
    Xf = lambda d: feats(d, sp["station_id"], sp["stations"])
    res = run(sp["model"], tr, te, Xf)
    inland_sep = int((tr.inland_canal == 1).sum()) >= INLAND_MIN_N
    gtr, gte = dist_group(tr, inland_sep), dist_group(te, inland_sep)
    lo, hi = cqr(res)
    lom, him = cqr(res, gtr, gte)
    cq = conformal_grid(res)
    oofc = oof_conformal_grid(res)
    out = te[[c for c in KEEP if c in te.columns] + [c for c in ("check", "n_days_cur") if c in te.columns]].copy()
    out = out.rename(columns={"y_smax_next": "y_obs", "season": "test_season"})
    for k in ("held_out", "model", "variant", "design"):
        out.insert(0, k, sp[k])
    out["dist_group"] = gte
    out["med_raw"] = np.expm1(res["full"][:, list(TAUS).index(0.5)])
    out[QCOL] = np.expm1(res["full"])
    out[CQCOL] = np.expm1(cq)
    out["lo_raw"], out["hi_raw"] = np.expm1(res["full"][:, 0]), np.expm1(res["full"][:, -1])
    out["lo_cqr"], out["hi_cqr"] = np.expm1(lo), np.expm1(hi)
    out["lo_mond"], out["hi_mond"] = np.expm1(lom), np.expm1(him)
    ytr = tr.y_smax_next.to_numpy(float)
    for c in THR:
        out[f"p_gt{c}"] = exceed_prob(cq, c)
        out[f"pstar_{c}"] = choose_pstar(exceed_prob(oofc, c), ytr > c)
    out["hp"] = str(res["hp"])
    info = dict(design=sp["design"], variant=sp["variant"], model=sp["model"], held_out=sp["held_out"],
                test_season=sp["T"], n_train=len(tr), train_seasons=",".join(map(str, res["folds"])),
                n_test=len(te), hp=str(res["hp"]), tune_loss=round(min(res["loss"].values()), 5),
                inland_sep=inland_sep, n_cal_inland=int((tr.inland_canal == 1).sum()),
                cal_groups=str(dict(zip(*np.unique(gtr, return_counts=True)))), secs=round(time.time() - t0, 1))
    return out, info


def splits(df):
    """(design, T, held_out, train, test) per protocol 6; train = rows with a target from seasons < T."""
    lab = df[df.y_smax_next.notna()]
    for T in TEST_SEASONS:
        tr = lab[lab.season < T]
        te = lab[(lab.season == T) & lab.station.isin(CANON28)]
        yield "forward", T, "", tr, te
        for s in CANON28:
            if (te.station == s).any():
                yield "loso", T, s, tr[tr.station != s], te[te.station == s]
        for p in sorted(te.province_canon.unique()):
            yield "lopo", T, p, tr[tr.province_canon != p], te[te.province_canon == p]


def pctt_rows(df):
    """Extreme-season check rows from PCTT 2020 dekads at the 4 in-list stations (lower-bound values).
    check i : current and next dekad complete (>= 7 report days); target = next dekad.
    check ii: issue 2020-02-20 (current dekad 6 report days, incomplete), median vs Feb 2020 monthly maximum."""
    p = pd.read_csv(P("data/processed/pctt_dekadal.csv"), parse_dates=["dekad_end"])
    p = p[(p.year == 2020) & p.station.isin(PCTT4)]
    val = {(r.station, r.dekad_end.date()): (r.smax_gL, r.complete, r.n_days) for r in p.itertuples()}
    q = pd.read_csv(P("data/raw/glofas/kratie_glofas_daily.csv"), parse_dates=["date"]).set_index("date").q_m3s
    clim, oni = bf.make_clim(q), bf.load_oni()
    stat = df.drop_duplicates("station").set_index("station")
    rows = []
    for (st, t), (v, comp, nd) in sorted(val.items()):
        ts, te = bf.next_dekad(t)
        nxt = val.get((st, te))
        if nxt is None:
            continue
        check = "i" if comp and nxt[1] else ("ii" if t == date(2020, 2, 20) else None)
        if check is None:
            continue
        pv = val.get((st, bf.prev_dekad_end(t)))
        prev = pv[0] if pv and pv[1] else np.nan
        s = stat.loc[st]
        d = dict(issue_date=pd.Timestamp(t), season=2020, station=st, check=check, n_days_cur=nd,
                 province_canon=s.province_canon, km_from_mouth=s.km_from_mouth, inland_canal=s.inland_canal,
                 river_group=s.river_group, obs_source="pctt", y_smax_next=nxt[0] if nxt[1] else np.nan,
                 bench_persist=v, bench_official=np.nan, smax_cur=v, log1p_smax_cur=np.log1p(v),
                 log1p_delta_smax=np.log1p(v) - np.log1p(prev), dekad_of_season=bf.dekad_idx(t),
                 oni=bf.oni_for(oni, t)[0])
        d.update(bf.glofas_features(q, t, 5, clim))
        d.update(bf.tide_features(ts, te))
        rows.append(d)
    return pd.DataFrame(rows)


# ---------------------------------------------------------------- scoring
POINT = {"model": "med_raw", "cmed": "cq50", "persist": "bench_persist", "clim": "bench_clim",
         "official": "bench_official"}


def rowstats(d):
    y = d.y_obs.to_numpy(float)
    n = len(d)
    cols = {"n": np.ones(n)}

    def add(name, v, m=None):
        v = np.asarray(v, float)
        bad = np.isnan(v) if m is None else (np.isnan(v) | ~np.asarray(m, bool))
        cols[name] = np.where(bad, 0.0, v)
    pt = {f: d[c].to_numpy(float) for f, c in POINT.items()}
    ae = {f: np.abs(v - y) for f, v in pt.items()}
    for f, v in pt.items():
        m = ~np.isnan(v)
        add(f"ae_{f}", ae[f], m)
        add(f"n_{f}", m)
        if f in ("persist", "clim", "official"):
            add(f"dae_{f}", ae["model"] - ae[f], m)
            add(f"nd_{f}", m)
    om = ~np.isnan(pt["official"])
    for c in THR:
        e = y > c
        add(f"ev{c}", e)
        pm = d[f"p_gt{c}"].to_numpy(float)
        bs, masks, yes = {"model": (pm - e) ** 2}, {"model": np.ones(n, bool)}, {"model": pm > d[f"pstar_{c}"].to_numpy()}
        for f in ("persist", "clim", "official"):
            masks[f], yes[f] = ~np.isnan(pt[f]), pt[f] > c
            bs[f] = (yes[f].astype(float) - e) ** 2
        cf = d[f"clim_freq_gt{c}"].to_numpy(float)
        bs["climfreq"], masks["climfreq"] = (cf - e) ** 2, ~np.isnan(cf)
        for f in bs:
            add(f"bs_{f}{c}", bs[f], masks[f])
            add(f"nbs_{f}{c}", masks[f])
            if f != "model":
                add(f"dbs_{f}{c}", bs["model"] - bs[f], masks[f])
        for f in yes:
            m = masks[f]
            add(f"hit_{f}{c}", yes[f] & e, m)
            add(f"fa_{f}{c}", yes[f] & ~e, m)
            add(f"evm_{f}{c}", e, m)
            add(f"nev_{f}{c}", ~e, m)
        add(f"hitO{c}", yes["model"] & e, om)
        add(f"faO{c}", yes["model"] & ~e, om)
    add("crps_model", 2 * pinball(y, d[CQCOL].to_numpy(float), TAUS).mean(1))
    add("crps_raw", 2 * pinball(y, d[QCOL].to_numpy(float), TAUS).mean(1))
    for v in ("raw", "cqr", "mond"):
        lo, hi = d[f"lo_{v}"].to_numpy(float), d[f"hi_{v}"].to_numpy(float)
        add(f"cov_{v}", (lo <= y) & (y <= hi))
        cols[f"wid_{v}"] = hi - lo
    e4 = y > 4
    act = d.p_gt4.to_numpy(float)[:, None] > PGRID[None, :]
    for k in range(len(PGRID)):
        add(f"rh_{k}", act[:, k] & e4, om)
        add(f"rf_{k}", act[:, k] & ~e4, om)
    for f in ("official", "persist", "clim"):
        assert not np.isnan(pt[f][om]).any() or f == "official"
        add(f"rvh_{f}", (pt[f] > 4) & e4, om)
        add(f"rvf_{f}", (pt[f] > 4) & ~e4, om)
    return pd.DataFrame(cols, index=d.index)


def value(h, f, a, E, N):
    s = E / N
    ec = np.minimum(a, s)
    return (ec - (a * (h + f) + E - h) / N) / (ec - a * s)


AMASK = (PGRID >= 0.1 - 1e-9) & (PGRID <= 0.9 + 1e-9)


def metrics(T):
    M = {"n": T["n"]}
    with np.errstate(all="ignore"):
        for f in POINT:
            M[f"mae_{f}"] = T[f"ae_{f}"] / T[f"n_{f}"]
        M["skill_vs_persist"] = 1 - T["ae_model"] / T["ae_persist"]
        for f in ("persist", "clim", "official"):
            M[f"mae_diff_{f}"] = T[f"dae_{f}"] / T[f"nd_{f}"]
        for c in THR:
            M[f"base_rate_{c}"] = T[f"ev{c}"] / T["n"]
            for f in ("model", "persist", "clim", "official", "climfreq"):
                M[f"brier_{f}_{c}"] = T[f"bs_{f}{c}"] / T[f"nbs_{f}{c}"]
                if f != "model":
                    M[f"brier_diff_{f}_{c}"] = T[f"dbs_{f}{c}"] / T[f"nbs_{f}{c}"]
            for f in ("model", "persist", "clim", "official"):
                H, F = T[f"hit_{f}{c}"] / T[f"evm_{f}{c}"], T[f"fa_{f}{c}"] / T[f"nev_{f}{c}"]
                M[f"hit_rate_{f}_{c}"], M[f"far_{f}_{c}"], M[f"pss_{f}_{c}"] = H, F, H - F
            pss_m_on_off = T[f"hitO{c}"] / T[f"evm_official{c}"] - T[f"faO{c}"] / T[f"nev_official{c}"]
            M[f"pss_diff_official_{c}"] = pss_m_on_off - M[f"pss_official_{c}"]
        for k in ("crps_model", "crps_raw"):
            M[k] = T[k] / T["n"]
        for v in ("raw", "cqr", "mond"):
            M[f"cov_{v}"], M[f"width_{v}"] = T[f"cov_{v}"] / T["n"], T[f"wid_{v}"] / T["n"]
        N, E = T["nd_official"], T["evm_official4"]
        A = PGRID[AMASK]
        idx = np.flatnonzero(AMASK)
        Hm = np.stack([T[f"rh_{k}"] for k in range(len(PGRID))], -1)
        Fm = np.stack([T[f"rf_{k}"] for k in range(len(PGRID))], -1)
        Vm = np.stack([value(Hm[:, k], Fm[:, k], PGRID[k], E, N) for k in idx], -1)
        Venv = np.stack([np.nanmax(value(Hm, Fm, a, E[:, None], N[:, None]), 1) for a in A], -1)
        area = lambda V: np.trapz(V, A, axis=-1)
        M["rev_area_model"], M["rev_area_model_env"] = area(Vm), area(Venv)
        for f in ("official", "persist", "clim"):
            M[f"rev_area_{f}"] = area(np.stack([value(T[f"rvh_{f}"], T[f"rvf_{f}"], a, E, N) for a in A], -1))
        M["rev_area_diff_official"] = M["rev_area_model"] - M["rev_area_official"]
        M["rev_area_diff_official_env"] = M["rev_area_model_env"] - M["rev_area_official"]
    return M


def rev_curve(T):
    N, E = T["nd_official"][0], T["evm_official4"][0]
    rows = []
    with np.errstate(all="ignore"):
        for k, a in enumerate(PGRID):
            if not (0.05 - 1e-9 <= a <= 0.95 + 1e-9):
                continue
            r = dict(cost_loss=a, V_model=value(T[f"rh_{k}"][0], T[f"rf_{k}"][0], a, E, N),
                     V_model_env=np.nanmax([value(T[f"rh_{j}"][0], T[f"rf_{j}"][0], a, E, N) for j in range(len(PGRID))]))
            for f in ("official", "persist", "clim"):
                r[f"V_{f}"] = value(T[f"rvh_{f}"][0], T[f"rvf_{f}"][0], a, E, N)
            rows.append(r)
    return rows


def score(pred, seed):
    """Point metrics, bootstrap CIs, reliability and value curve for one (design, variant, model) prediction set."""
    rs = rowstats(pred)
    C = list(rs.columns)
    rs["season"], rs["date"] = pred.test_season.to_numpy(), pred.issue_date.to_numpy()
    S = rs.groupby(["season", "date"])[C].sum()
    lev = S.index.get_level_values(0)
    seasons = sorted(set(lev))
    rng = np.random.default_rng(seed)
    Ws = {}
    for s in seasons:
        D = int((lev == s).sum())
        W = np.zeros((B, D))
        np.add.at(W, (np.arange(B)[:, None], rng.integers(0, D, (B, D))), 1)
        Ws[s] = W
    out, rel, curve = [], [], []
    for scope in seasons + ["pooled"]:
        m = np.ones(len(S), bool) if scope == "pooled" else (lev == scope)
        Sm = S.to_numpy()[m]
        W = np.hstack([Ws[s] for s in seasons]) if scope == "pooled" else Ws[scope]
        tot = lambda X: {c: X[:, i] for i, c in enumerate(C)}
        T1 = tot(Sm.sum(0)[None, :])
        pt, bs = metrics(T1), metrics(tot(W @ Sm))
        for k in pt:
            v = bs[k][np.isfinite(bs[k])]
            lo, hi = np.percentile(v, [2.5, 97.5]) if len(v) else (np.nan, np.nan)
            out.append(dict(scope=str(scope), metric=k, estimate=float(pt[k][0]), ci_lo=lo, ci_hi=hi,
                            n_boot_finite=len(v)))
        sub = pred if scope == "pooled" else pred[pred.test_season == scope]
        for c in THR:
            b = np.minimum((sub[f"p_gt{c}"].to_numpy() * 10).astype(int), 9)
            e = (sub.y_obs > c).to_numpy()
            for k in range(10):
                mk = b == k
                rel.append(dict(scope=str(scope), threshold=c, bin=f"{k/10:.1f}-{(k+1)/10:.1f}", n=int(mk.sum()),
                                mean_prob=sub[f"p_gt{c}"].to_numpy()[mk].mean() if mk.any() else np.nan,
                                obs_freq=e[mk].mean() if mk.any() else np.nan))
        if scope == "pooled":
            curve = rev_curve(T1)
    return out, rel, curve


# ---------------------------------------------------------------- main
def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()[:16]


def main(quick):
    t0 = time.time()
    os.makedirs(OUT, exist_ok=True)
    fpath = P("data/processed/features.csv")
    h0 = sha(fpath)
    dfs = {"main": load_features(5)}
    if not quick:
        dfs["lag0"], dfs["lag10"] = load_features(0), load_features(10)
    assert sha(fpath) == h0, "features.csv changed"
    df = dfs["main"]
    stations = sorted(df.station.unique())
    # Sông Đốc 42 g/L (20/05/2020) has no target and is no predictor of any row with a target; it only enters the
    # climatology pool. So noSD42 = main models with the climatology recomputed.
    sd42 = (df.station == "Sông Đốc") & (df.issue_date == "2020-05-20")
    assert df.loc[sd42, "smax_cur"].item() == 42.0 and df.loc[sd42, "y_smax_next"].isna().all()
    assert not ((df.station == "Sông Đốc") & (df.smax_prev == 42.0) & df.y_smax_next.notna()).any()
    pools = {"main": df, "lag0": df, "lag10": df, "stationid": df, "noODV": df[df.obs_source != "odv"],
             "noSD42": df[~sd42]}

    specs = []
    base = dict(variant="main", station_id=False, stations=stations)
    for design, T, held, tr, te in splits(df):
        if quick and design != "forward":
            continue
        for model in ("hgb", "qr"):
            specs.append(dict(base, design=design, T=T, held_out=held, model=model, train=tr, test=te))
            if design == "forward" and not quick:
                for v in ("lag0", "lag10"):
                    d2 = dfs[v]
                    lab = d2[d2.y_smax_next.notna()]
                    specs.append(dict(base, variant=v, design=design, T=T, held_out="", model=model,
                                      train=lab[lab.season < T],
                                      test=lab[(lab.season == T) & lab.station.isin(CANON28)]))
                specs.append(dict(base, variant="noODV", design=design, T=T, held_out="", model=model,
                                  train=tr[tr.obs_source != "odv"], test=te))
                specs.append(dict(base, variant="stationid", station_id=True, design=design, T=T, held_out="",
                                  model=model, train=tr, test=te))
    if not quick:
        lab = df[df.y_smax_next.notna()]
        pr = pctt_rows(df)
        for model in ("hgb", "qr"):
            specs.append(dict(base, design="extreme", T=2020, held_out="", model=model, train=lab, test=pr))
    for sp in specs:  # no test-season row in training or calibration (calibration = training rows, out of fold)
        assert sp["design"] == "extreme" or sp["train"].season.max() < sp["T"]
        assert not set(sp["train"].index) & set(sp["test"].index) or sp["design"] == "extreme"
    specs.sort(key=lambda s: (s["model"] != "hgb", -s["train"].season.nunique()))
    print(f"{len(specs)} runs", flush=True)
    results = Parallel(n_jobs=min(12, os.cpu_count()), verbose=5)(delayed(task)(s) for s in specs)
    preds = pd.concat([r[0] for r in results], ignore_index=True)
    info = pd.DataFrame([r[1] for r in results]).sort_values(["design", "variant", "model", "test_season", "held_out"])

    # benchmarks that depend on the training seasons (climatology), per variant pool
    nosd = preds[(preds.design == "forward") & (preds.variant == "main")].assign(variant="noSD42")
    preds = pd.concat([preds, nosd], ignore_index=True)
    parts = []
    for (v, T), g in preds.groupby(["variant", "test_season"]):
        if T == 2020:
            parts.append(g)
            continue
        parts.append(pd.concat([g, climatology(g, pools[v], T)], axis=1))
    preds = pd.concat(parts, ignore_index=True)
    assert preds.loc[preds.design != "extreme", "bench_clim"].notna().all()

    # scoring
    allm, rel, curves = [], [], []
    for (design, v, model), g in preds[preds.design != "extreme"].groupby(["design", "variant", "model"]):
        o, r, cv = score(g, SEED)
        for x in o:
            allm.append(dict(design=design, variant=v, model=model, **x))
        for x in r:
            rel.append(dict(design=design, variant=v, model=model, **x))
        for x in cv:
            curves.append(dict(design=design, variant=v, model=model, **x))
    M = pd.DataFrame(allm)
    M.to_csv(os.path.join(OUT, "bootstrap_ci.csv"), index=False, float_format="%.6g")
    M[["design", "variant", "model", "scope", "metric", "estimate"]].rename(columns={"estimate": "value"}).to_csv(
        os.path.join(OUT, "metrics.csv"), index=False, float_format="%.6g")
    pd.DataFrame(rel).to_csv(os.path.join(OUT, "reliability.csv"), index=False, float_format="%.6g")
    pd.DataFrame(curves).to_csv(os.path.join(OUT, "rev_curve.csv"), index=False, float_format="%.6g")
    preds.to_csv(os.path.join(OUT, "predictions.csv"), index=False, float_format="%.6g")
    info.to_csv(os.path.join(OUT, "runs.csv"), index=False)
    write_reports(M, preds, info, dfs, time.time() - t0, quick)
    print(f"done in {(time.time() - t0) / 60:.1f} min", flush=True)


# ---------------------------------------------------------------- reports
def get(M, design, model, metric, scope="pooled", variant="main"):
    r = M[(M.design == design) & (M.variant == variant) & (M.model == model) & (M.scope == scope) & (M.metric == metric)]
    return (np.nan, np.nan, np.nan) if r.empty else tuple(r[["estimate", "ci_lo", "ci_hi"]].iloc[0])


def fmt(t, d=3):
    return f"{t[0]:.{d}f} [{t[1]:.{d}f}, {t[2]:.{d}f}]"


def h1(M, model, variant="main"):
    crit = [(f"MAE diff vs {b}", get(M, "forward", model, f"mae_diff_{b}", variant=variant))
            for b in ("persist", "clim", "official")]
    crit += [(f"Brier(4) diff vs {b}", get(M, "forward", model, f"brier_diff_{b}_4", variant=variant))
             for b in ("persist", "clim")]
    ok = [c[1][2] < 0 for c in crit]
    return crit, ok, all(ok)


def write_reports(M, preds, info, dfs, secs, quick):
    L = []
    w = L.append
    models = sorted(M.model.unique())
    # ---- verdicts
    V = ["# Core-B verdicts (protocol-v1, pre-registered criteria applied literally)", "",
         f"Generated by scripts/run_core_b.py on {date.today().isoformat()}. Forward-by-season design, test seasons "
         "2024-2026 pooled (27 issue dates), main variant. CIs: paired bootstrap over issue dates within test seasons, "
         "2,000 resamples, percentile 95%. Differences are model minus benchmark (negative = model better for MAE "
         "and Brier).", "", "| Hypothesis | Criterion | Model | Estimate [95% CI] | Met? |", "|---|---|---|---|---|"]
    verdict = {}
    for m in models:
        crit, ok, allok = h1(M, m)
        for (name, t), o in zip(crit, ok):
            V.append(f"| H1 | {name}: CI upper < 0 | {m} | {fmt(t)} | {'yes' if o else 'no'} |")
        V.append(f"| **H1** | all five | {m} | | **{'SUPPORTED' if allok else 'NOT SUPPORTED'}** |")
        verdict[("H1", m)] = allok
    for m in models:
        c = get(M, "forward", m, "cov_cqr")
        ok = 0.87 <= c[0] <= 0.93
        V.append(f"| **H2a** | forward coverage of CQR 90% in [0.87, 0.93] | {m} | {fmt(c)} | "
                 f"**{'SUPPORTED' if ok else 'NOT SUPPORTED'}** |")
        verdict[("H2a", m)] = ok
    for m in models:
        oks = []
        for d in ("loso", "lopo"):
            p, q = get(M, d, m, "cov_cqr"), get(M, d, m, "cov_mond")
            ok = p[0] < 0.87 and q[0] >= 0.87
            oks.append(ok)
            V.append(f"| H2b | {d}: plain < 0.87 and Mondrian >= 0.87 | {m} | plain {fmt(p)}; Mondrian {fmt(q)} | "
                     f"{'yes' if ok else 'no'} |")
        V.append(f"| **H2b** | both designs | {m} | | **{'SUPPORTED' if all(oks) else 'NOT SUPPORTED'}** |")
        verdict[("H2b", m)] = all(oks)
    for m in models:
        t = get(M, "forward", m, "rev_area_diff_official")
        ok = t[1] > 0
        V.append(f"| **H3** | REV area (C/L 0.1-0.9) model minus official, CI lower > 0 | {m} | {fmt(t)} | "
                 f"**{'SUPPORTED' if ok else 'NOT SUPPORTED'}** |")
        verdict[("H3", m)] = ok
    V += ["", "## H1 (accuracy)", ""]
    for m in models:
        crit, ok, allok = h1(M, m)
        mae = {f: get(M, "forward", m, f"mae_{f}") for f in ("model", "persist", "clim", "official")}
        V.append(f"**{m}.** Pooled MAE {mae['model'][0]:.2f} g/L (persistence {mae['persist'][0]:.2f}, climatology "
                 f"{mae['clim'][0]:.2f}, official {mae['official'][0]:.2f}). " + " ".join(f"{n}: {fmt(t)}." for n, t in crit)
                 + f" Base rate at 4 g/L {get(M, 'forward', m, 'base_rate_4')[0]:.2f}; Brier(4) model "
                 f"{get(M, 'forward', m, 'brier_model_4')[0]:.3f}. H1 is {'supported' if allok else 'not supported'} "
                 f"for {m}" + ("." if allok else f" (criteria not met: {', '.join(n for (n, _), o in zip(crit, ok) if not o)}).")
                 + " Against the official forecast at 4 g/L: PSS model "
                 f"{get(M, 'forward', m, 'pss_model_4')[0]:.3f} vs official {get(M, 'forward', m, 'pss_official_4')[0]:.3f}, "
                 f"difference {fmt(get(M, 'forward', m, 'pss_diff_official_4'))}.")
        V.append("")
    V += ["## H2 (coverage)", ""]
    for m in models:
        per = ", ".join(f"{s}: {get(M, 'forward', m, 'cov_cqr', scope=str(s))[0]:.3f}" for s in TEST_SEASONS)
        V.append(f"**{m}.** Forward CQR 90% coverage {fmt(get(M, 'forward', m, 'cov_cqr'))} (per season {per}); "
                 f"Mondrian {get(M, 'forward', m, 'cov_mond')[0]:.3f}; raw quantiles {get(M, 'forward', m, 'cov_raw')[0]:.3f}. "
                 f"Leave-station-out: plain {get(M, 'loso', m, 'cov_cqr')[0]:.3f}, Mondrian {get(M, 'loso', m, 'cov_mond')[0]:.3f}; "
                 f"leave-province-out: plain {get(M, 'lopo', m, 'cov_cqr')[0]:.3f}, Mondrian {get(M, 'lopo', m, 'cov_mond')[0]:.3f}. "
                 f"H2a {'supported' if verdict[('H2a', m)] else 'not supported'}; H2b "
                 f"{'supported' if verdict[('H2b', m)] else 'not supported'}.")
        V.append("")
    V += ["## H3 (value)", ""]
    for m in models:
        V.append(f"**{m}.** Area under the REV curve over C/L 0.1-0.9 at 4 g/L: model "
                 f"{fmt(get(M, 'forward', m, 'rev_area_model'))}, official {fmt(get(M, 'forward', m, 'rev_area_official'))}, "
                 f"difference {fmt(get(M, 'forward', m, 'rev_area_diff_official'))} (users act when P > C/L). With the "
                 f"envelope over probability thresholds the difference is "
                 f"{fmt(get(M, 'forward', m, 'rev_area_diff_official_env'))} (secondary, threshold chosen on test data). "
                 f"H3 is {'supported' if verdict[('H3', m)] else 'not supported'} for {m}.")
        V.append("")
    open(os.path.join(OUT, "verdicts.md"), "w", encoding="utf-8").write("\n".join(V) + "\n")

    # ---- run log
    w("# Core-B run log")
    w("")
    w(f"- Date {date.today().isoformat()}; runtime {secs / 60:.1f} min; quick={quick}; seed {SEED}; bootstrap B={B}.")
    w(f"- Python {platform.python_version()}, numpy {np.__version__}, pandas {pd.__version__}, scipy {scipy.__version__}, "
      f"scikit-learn {sklearn.__version__}, joblib {joblib.__version__}; OMP_NUM_THREADS={os.environ.get('OMP_NUM_THREADS')}.")
    w(f"- Input data/processed/features.csv sha256[:16] {sha(P('data/processed/features.csv'))} (unchanged by this run; "
      "lag 0/10 features rebuilt in memory with build_features.build(lag) and its self_check).")
    w(f"- Runs: {len(info)}; total fit time {info.secs.sum() / 3600:.2f} CPU-h.")
    w("")
    w("## Ambiguity choices")
    for c in CHOICES:
        w(f"- {c}")
    w("")
    w("## Proposed deviations after freeze (not applied to docs/protocol.md; owner to decide)")
    w("- (D1) Extreme-season check (ii) (protocol 6.4): the Jan-Feb 2020 monthly maxima cannot be checked as written. "
      "A dekadal forecast needs the current-dekad Smax at the issue date, and no bulletin exists between 25/12/2019 "
      "and 20/05/2020 in our data. Only the 4 PCTT stations have a current-dekad value in Jan-Feb 2020: the dekad "
      "11-20/02/2020 (6 report days, below the >= 7-day completeness rule, lower bound). Run here: issue 20/02/2020 "
      "at those 4 stations, median for 21-29/02 vs the Feb 2020 monthly maximum (flag ok). Jan 2020 and the other "
      "~24 stations: not possible (missing log1p_smax_cur, log1p_delta_smax).")
    w("- (D2) Extreme-season check (i) uses models trained on all seasons with a target (2021-2026), i.e. later "
      "seasons than 2020; it is an extreme-season-out check, not a forecast in time.")
    w("- (D3) noSD42 sensitivity: the Sông Đốc 42 g/L value (20/05/2020) has no target and is not a predictor of any "
      "row with a target, so the models are unchanged; only the climatology benchmark is recomputed.")
    w("")
    w("## Data and run facts")
    lab = dfs["main"][dfs["main"].y_smax_next.notna()]
    w(f"- Rows with a target: {len(lab)}; per season {lab.groupby('season').size().to_dict()}; ODV rows with a target "
      f"{int((lab.obs_source == 'odv').sum())}.")
    fw = preds[(preds.design == "forward") & (preds.variant == "main") & (preds.model == models[0])]
    w(f"- Forward test rows: {len(fw)} ({fw.groupby('test_season').size().to_dict()}); issue dates "
      f"{fw.groupby('test_season').issue_date.nunique().to_dict()}; official forecast missing in "
      f"{int(fw.bench_official.isna().sum())} test rows; climatology source {fw.clim_src.value_counts().to_dict()}.")
    lp = preds[(preds.design == "lopo") & (preds.model == models[0]) & (preds.variant == "main")]
    if len(lp):
        w("- Leave-province-out groups (province_canon, pre-merger) and test stations:")
        for p, g in lp.groupby("held_out"):
            w(f"  - {p}: {', '.join(sorted(g.station.unique()))}")
    w("")
    w("## Chosen hyperparameters and inland-group decisions (forward and extreme runs)")
    w("")
    w("| design | variant | model | test season | n train | train seasons | hp | tune loss | inland separate (n cal) | groups |")
    w("|---|---|---|---|---|---|---|---|---|---|")
    for r in info[info.design.isin(["forward", "extreme"])].itertuples():
        w(f"| {r.design} | {r.variant} | {r.model} | {r.test_season} | {r.n_train} | {r.train_seasons} | {r.hp} | "
          f"{r.tune_loss} | {r.inland_sep} ({r.n_cal_inland}) | {r.cal_groups} |")
    for d in ("loso", "lopo"):
        sub = info[info.design == d]
        if len(sub):
            w(f"- {d}: {len(sub)} runs; inland group separate in {int(sub.inland_sep.sum())}; hp counts "
              f"{sub.groupby('model').hp.value_counts().to_dict()}")
    w("")
    w("## Headline numbers (pooled; per season in bootstrap_ci.csv)")
    w("")
    w("| design | model | MAE model | MAE diff vs persist | vs clim | vs official | Brier4 diff vs persist | vs clim | cov CQR | cov Mondrian | width CQR | REV area diff |")
    w("|---|---|---|---|---|---|---|---|---|---|---|---|")
    for d in ("forward", "loso", "lopo"):
        for m in models:
            w(f"| {d} | {m} | {get(M, d, m, 'mae_model')[0]:.2f} | {fmt(get(M, d, m, 'mae_diff_persist'), 2)} | "
              f"{fmt(get(M, d, m, 'mae_diff_clim'), 2)} | {fmt(get(M, d, m, 'mae_diff_official'), 2)} | "
              f"{fmt(get(M, d, m, 'brier_diff_persist_4'))} | {fmt(get(M, d, m, 'brier_diff_clim_4'))} | "
              f"{get(M, d, m, 'cov_cqr')[0]:.3f} | {get(M, d, m, 'cov_mond')[0]:.3f} | {get(M, d, m, 'width_cqr')[0]:.2f} | "
              f"{fmt(get(M, d, m, 'rev_area_diff_official'))} |")
    w("")
    w("## Sensitivity runs (forward design, pooled)")
    w("")
    w("| variant | model | MAE model | MAE diff vs persist | vs clim | vs official | Brier4 diff vs persist | vs clim | cov CQR | REV area diff | H1 |")
    w("|---|---|---|---|---|---|---|---|---|---|---|")
    for v in ("main", "lag0", "lag10", "noODV", "noSD42", "stationid"):
        for m in models:
            if get(M, "forward", m, "mae_model", variant=v)[0] != get(M, "forward", m, "mae_model", variant=v)[0]:
                continue
            g = lambda k: get(M, "forward", m, k, variant=v)
            w(f"| {v} | {m} | {g('mae_model')[0]:.2f} | {fmt(g('mae_diff_persist'), 2)} | {fmt(g('mae_diff_clim'), 2)} | "
              f"{fmt(g('mae_diff_official'), 2)} | {fmt(g('brier_diff_persist_4'))} | {fmt(g('brier_diff_clim_4'))} | "
              f"{g('cov_cqr')[0]:.3f} | {fmt(g('rev_area_diff_official'))} | "
              f"{'supported' if h1(M, m, v)[2] else 'not supported'} |")
    w("- stationid is an H1-only run; its coverage/REV columns are shown for completeness.")
    w("")
    ex = preds[preds.design == "extreme"]
    if len(ex):
        w("## Extreme-season check 2020 (exploratory)")
        ref = pd.read_csv(P("data/processed/nchmf_ref_monthly.csv"))
        ref = ref[(ref["flags"] == "ok") & (ref.ref_month == "2020-02")].set_index("station").ref_smax_gL
        for m in models:
            e1 = ex[(ex.model == m) & (ex.check == "i")].dropna(subset=["y_obs"])
            if len(e1):
                below_up = (e1.y_obs <= e1.hi_cqr).mean()
                inside = ((e1.y_obs >= e1.lo_cqr) & (e1.y_obs <= e1.hi_cqr)).mean()
                w(f"- (i) {m}: {len(e1)} station-dekads (4 stations, issues 29/02-30/04/2020, PCTT complete dekads). "
                  f"PCTT next-dekad value <= CQR upper bound in {below_up:.0%} (consistent with a lower bound); inside "
                  f"the interval {inside:.0%}; above the upper bound {(e1.y_obs > e1.hi_cqr).mean():.0%}; Mondrian upper "
                  f"bound exceeded in {(e1.y_obs > e1.hi_mond).mean():.0%}. Median abs. diff median vs PCTT "
                  f"{(e1.med_raw - e1.y_obs).abs().median():.2f} g/L.")
            e2 = ex[(ex.model == m) & (ex.check == "ii")]
            if len(e2):
                mm = ref.reindex(e2.station).to_numpy()
                s = ", ".join(f"{r.station} {r.med_raw:.1f} vs {x:.1f}" for r, x in zip(e2.itertuples(), mm))
                w(f"- (ii) {m}: issue 20/02/2020, dekadal median for 21-29/02 vs Feb 2020 monthly max (ok): {s}; "
                  f"median exceeds the monthly max in {int((e2.med_raw.to_numpy() > mm).sum())} of {len(e2)}.")
        w("")
    open(os.path.join(OUT, "run_log.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")


# ---------------------------------------------------------------- self-check
def check():
    rng = np.random.default_rng(0)
    # 1. toy CQR (CV+, 3 folds) with a too-narrow model: coverage must come back to ~90%
    n, nte = 600, 20000
    x, xt = rng.normal(size=n), rng.normal(size=nte)
    y, yt = x + rng.normal(size=n), xt + rng.normal(size=nte)
    grid = lambda v: v[:, None] + 0.5 * (TAUS[None, :] - 0.5)          # quantiles far too narrow
    res = dict(y=y, oof=grid(x), fid=np.arange(n) % 3, fte=np.stack([grid(xt) + 0.01 * k for k in range(3)]))
    lo, hi = cqr(res)
    cov = ((yt >= lo) & (yt <= hi)).mean()
    assert 0.88 <= cov <= 0.92, cov
    cg = conformal_grid(res)
    assert abs((yt <= cg[:, list(TAUS).index(0.5)]).mean() - 0.5) < 0.02
    lo2, hi2 = cqr(res, np.where(np.arange(n) % 2, "a", "b"), np.where(np.arange(nte) % 2, "a", "b"))
    assert 0.88 <= ((yt >= lo2) & (yt <= hi2)).mean() <= 0.92
    p = exceed_prob(np.log1p(np.sort(np.abs(rng.normal(5, 3, (50, 19))), 1)), 4)
    assert (p >= 0.01).all() and (p <= 0.99).all()
    # 2. split hygiene: no test-season row in any training/calibration set; held-out group absent from training
    df = load_features(5)
    for design, T, held, tr, te in splits(df):
        assert tr.season.max() < T and (te.season == T).all() and te.station.isin(CANON28).all()
        assert not set(tr.index) & set(te.index)
        if design == "loso":
            assert held not in set(tr.station)
        if design == "lopo":
            assert held not in set(tr.province_canon)
    # 3. climatology uses training seasons only: changing every test-season value does not change it
    te = df[(df.season == 2025) & df.y_smax_next.notna()]
    a = climatology(te, df, 2025)
    df2 = df.copy()
    df2.loc[df2.season >= 2025, "smax_cur"] = 999.0
    assert np.allclose(a.bench_clim, climatology(te, df2, 2025).bench_clim)
    r = te.iloc[0]
    pool = df[(df.season < 2025) & (df.station == r.station) & (df.oy == r.toy)].smax_cur
    assert np.isclose(a.bench_clim.iloc[0], pool.mean() if len(pool) else df[(df.season < 2025) & (df.station == r.station)].smax_cur.mean())
    # 4. checks on written outputs
    if os.path.exists(os.path.join(OUT, "metrics.csv")):
        M = pd.read_csv(os.path.join(OUT, "metrics.csv"))
        pr = pd.read_csv(os.path.join(OUT, "predictions.csv"), parse_dates=["issue_date"])
        t = df[(df.season == 2025) & df.y_smax_next.notna() & df.station.isin(CANON28)]
        mae = (t.smax_cur - t.y_smax_next).abs().mean()
        v = M[(M.design == "forward") & (M.variant == "main") & (M.model == "qr") & (M.scope == "2025")
              & (M.metric == "mae_persist")].value.item()
        assert abs(v - mae) < 1e-4, (v, mae)
        f = pr[(pr.design == "forward") & (pr.variant == "main")]
        for T, g in f.groupby("test_season"):
            assert np.allclose(g.bench_clim, climatology(g, df, T).bench_clim, rtol=0, atol=1e-3)  # csv rounding
        assert (pr.p_gt1 >= pr.p_gt2 - 1e-12).all() and (pr.p_gt2 >= pr.p_gt4 - 1e-12).all()
        assert (np.diff(pr[CQCOL].to_numpy(), axis=1) >= -1e-9).all()
        assert (pr[pr.design != "extreme"].issue_date.dt.year.isin([2023, 2024, 2025, 2026])).all()
    print("self-check OK")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--quick", action="store_true")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    if a.check:
        check()
    else:
        if a.quick:
            B = 200
        main(a.quick)
        if not a.quick:
            check()
