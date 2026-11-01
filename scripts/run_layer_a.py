"""Layer A: seasonal severe-season forecast, protocol section 8 (protocol-v1). Run: python -I -X utf8 scripts/run_layer_a.py"""
import os
import numpy as np, pandas as pd
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.metrics import roc_auc_score

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = lambda *a: os.path.join(ROOT, *a)
OUT = P("results", "layer_a"); os.makedirs(OUT, exist_ok=True)
SEED, NB = 20261101, 2000
ST = ["Cầu Quan", "Sơn Đốc", "Trà Vinh"]

# ---------- data ----------
m = pd.read_csv(P("data/processed/long_mendeley_max.csv"))
m = m[m.month.isna()]
sd = pd.read_csv(P("data/processed/long_sondoc_monthly_max.csv"))
sd = sd[sd.month.isin([2, 3])].groupby("year").smax_gL.max().reset_index().assign(station="Sơn Đốc")
tgt = pd.concat([m[["station", "year", "smax_gL"]], sd]).rename(columns={"year": "season", "smax_gL": "smax"})
tgt = tgt[tgt.station.isin(ST)].reset_index(drop=True)
assert tgt.groupby("station").size().to_dict() == {"Cầu Quan": 26, "Sơn Đốc": 21, "Trà Vinh": 26}
med = tgt.groupby("station").smax.median()
assert abs(med["Cầu Quan"] - 8.55) < 1e-9 and abs(med["Trà Vinh"] - 9.0) < 1e-9  # protocol medians
q67 = tgt.groupby("station").smax.quantile(2 / 3)
tgt["prev"] = tgt.sort_values("season").groupby("station").smax.shift(1)
tgt.loc[tgt.groupby("station").season.diff() != 1, "prev"] = np.nan  # (no gaps expected)

oni = pd.read_csv(P("data/raw/oni/oni.ascii.txt"), sep=r"\s+")
oni = oni[oni.SEAS == "JAS"].set_index("YR").ANOM
tc = pd.read_csv(P("data/processed/long_tanchau_monthly_q.csv"))
tcq = tc[tc.month.isin([9, 10])].groupby("year").q_m3s.mean()
gf = pd.read_csv(P("data/raw/glofas/kratie_glofas_daily.csv"), parse_dates=["date"])
gf = gf[gf.date.dt.month.isin([9, 10])]
gfq = gf.groupby(gf.date.dt.year).q_m3s.mean()
# GloFAS rescaled to Tan Chau scale (linear fit on overlap 1997-2016): used for the 2022/2025 extension
ov = sorted(set(tcq.index) & set(gfq.index))
lin = LinearRegression().fit(gfq[ov].values.reshape(-1, 1), tcq[ov].values)
r_ov = np.corrcoef(gfq[ov], tcq[ov])[0, 1]

tgt["oni"] = (tgt.season - 1).map(oni)
tgt["q_tc"] = (tgt.season - 1).map(tcq)
tgt["q_gf"] = (tgt.season - 1).map(gfq)

# ---------- model ----------
def design(df, mu_prev, mu, sd_, feats):
    """station dummies + standardised slopes. prev = station-demeaned (training means), then pooled scaling."""
    X = df.copy()
    X["prev_a"] = X.prev - X.station.map(mu_prev)
    D = np.column_stack([(X.station == s).astype(float) for s in ST])
    Z = (X[feats].values - mu) / sd_
    return np.hstack([D, Z])

def fit_predict(train, test, feats):
    mu_prev = train.groupby("station").prev.mean()
    tr = train.assign(prev_a=train.prev - train.station.map(mu_prev))
    mu, sd_ = tr[feats].mean().values, tr[feats].std(ddof=0).values
    # penalty=None: 3 slopes + 3 intercepts on >=70 rows; weak L2 only if coefficients blow up (checked below)
    clf = LogisticRegression(penalty=None, fit_intercept=False, max_iter=5000)
    clf.fit(design(train, mu_prev, mu, sd_, feats), train.severe)
    assert np.abs(clf.coef_).max() < 10, "quasi-separation: switch to weak L2 and log"
    return clf.predict_proba(design(test, mu_prev, mu, sd_, feats))[:, 1], clf

def prep(thr_kind, qcol):
    d = tgt.dropna(subset=["prev", "oni", qcol]).copy()
    thr = med if thr_kind == "median" else q67
    d["severe"] = (d.smax > d.station.map(thr)).astype(int)
    return d.rename(columns={qcol: "q"}).reset_index(drop=True)

def loso(d):
    feats = ["oni", "q", "prev_a"]
    d = d.copy(); d["p"] = np.nan; d["p_clim"] = np.nan
    for s in sorted(d.season.unique()):
        te = d.season == s
        tr = d[~te]
        assert s not in set(tr.season)  # no held-out season in training
        d.loc[te, "p"] = fit_predict(tr, d[te], feats)[0]
        br = tr.groupby("station").severe.mean()
        d.loc[te, "p_clim"] = d[te].station.map(br).values
    return d

# ---------- metrics ----------
def bs(y, p): return (y - p) ** 2
def stats(d, idx_seasons=None):
    """BSS (sum Brier ratio) and AUC, pooled + per station; d rows already selected (may repeat for bootstrap)."""
    out = {}
    for name, g in [("pooled", d)] + [(s, d[d.station == s]) for s in ST]:
        bm, bc = bs(g.severe, g.p).sum(), bs(g.severe, g.p_clim).sum()
        auc = roc_auc_score(g.severe, g.p) if g.severe.nunique() == 2 else np.nan
        out[name] = (1 - bm / bc, auc, bs(g.severe, g.p).mean(), bs(g.severe, g.p_clim).mean(), g.severe.mean(), len(g))
    return out

def boot(d, rng):
    by = {s: g for s, g in d.groupby("season")}; ss = np.array(list(by))
    res = []
    for _ in range(NB):
        pick = rng.choice(ss, len(ss))
        res.append(stats(pd.concat([by[s] for s in pick])))
    return res

def run(label, d, rng, rows_m, rows_ci, rows_rel, logf):
    d = loso(d)
    st = stats(d)
    bt = boot(d, rng)
    for name, v in st.items():
        rows_m.append(dict(variant=label, scope=name, n=v[5], base_rate=v[4], brier_model=v[2], brier_clim=v[3], bss=v[0], auc=v[1]))
        for k, i in (("bss", 0), ("auc", 1)):
            x = np.array([b[name][i] for b in bt], float)
            rows_ci.append(dict(variant=label, scope=name, metric=k, est=v[i], lo=np.nanpercentile(x, 2.5), hi=np.nanpercentile(x, 97.5),
                                n_valid=int(np.isfinite(x).sum()), share_bss_pos=float((x > 0).mean()) if k == "bss" else np.nan))
    d["bin"] = pd.cut(d.p, [0, 1 / 3, 2 / 3, 1.0], include_lowest=True, labels=["<=0.33", "0.33-0.67", ">0.67"])
    for b, g in d.groupby("bin", observed=True):
        rows_rel.append(dict(variant=label, bin=b, n=len(g), mean_p=g.p.mean(), obs_freq=g.severe.mean()))
    logf.append(f"- {label}: n={len(d)}, seasons {d.season.min()}-{d.season.max()}, base rate {d.severe.mean():.3f}")
    return d

rng = np.random.default_rng(SEED)
M, C, R, L = [], [], [], []
variants = {
    "main_median_TanChau": ("median", "q_tc"),
    "sens_tercile_TanChau": ("tercile", "q_tc"),
    "sens_median_GloFAS": ("median", "q_gf"),
    "sens_tercile_GloFAS": ("tercile", "q_gf"),
}
res = {}
for k, (t, q) in variants.items():
    res[k] = run(k, prep(t, q), rng, M, C, R, L)
main = res["main_median_TanChau"]
res["main_median_TanChau"][["season", "station", "p", "p_clim", "severe", "smax", "oni", "q", "prev"]].rename(
    columns={"p": "p_severe", "severe": "severe_obs", "q": "q_tanchau_sepoct", "prev": "prev_season_max"}).to_csv(P("results/layer_a/forecasts_loso.csv"), index=False)
for k in list(variants)[1:]:
    res[k][["season", "station", "p", "p_clim", "severe", "smax", "oni", "q", "prev"]].to_csv(P(f"results/layer_a/forecasts_loso_{k}.csv"), index=False)
pd.DataFrame(M).to_csv(P("results/layer_a/metrics.csv"), index=False)
pd.DataFrame(C).to_csv(P("results/layer_a/bootstrap_ci.csv"), index=False)
pd.DataFrame(R).to_csv(P("results/layer_a/reliability.csv"), index=False)

# ---------- self-check ----------
assert len(main) == 25 + 20 + 25 and main.p.between(0, 1).all() and main.p.notna().all()
assert set(main.groupby("station").season.min()) == {1992, 1997}
assert (main.severe == (main.smax > main.station.map(med))).all()
assert abs(main.groupby("station").severe.mean() - 0.5).max() < 0.2

# ---------- extension 2022, 2025 (train on all seasons of main spec) ----------
ob = pd.read_csv(P("data/processed/nchmf_obs.csv"), parse_dates=["issue_date"])
ob = ob[ob.station.isin(ST)]
def bull_max(st, season):
    g = ob[(ob.station == st) & (ob.issue_date >= f"{season-1}-12-01") & (ob.issue_date <= f"{season}-06-30")]
    if st == "Sơn Đốc":
        g = g[g.issue_date.dt.month.isin([2, 3])]
    return (g.smax_obs_gL.max() if len(g) else np.nan), len(g)
feats = ["oni", "q", "prev_a"]
ext = []
for Y in (2022, 2025):
    q_gf = gfq[Y - 1]; q_eq = float(lin.predict([[q_gf]])[0])
    rows = []
    for s in ST:
        sm, n = bull_max(s, Y); pv, npv = bull_max(s, Y - 1)
        rows.append(dict(season=Y, station=s, smax_bulletin_lb=sm, n_bulletins=n, prev=pv, n_prev_bulletins=npv,
                         oni=oni[Y - 1], q=q_eq, q_glofas=q_gf))
    te = pd.DataFrame(rows)
    te["p_severe"] = fit_predict(main, te, feats)[0]
    te["median_ref"] = te.station.map(med)
    te["severe_obs_lb"] = (te.smax_bulletin_lb > te.median_ref).astype(float)  # a lower bound can only understate severity
    ext.append(te)
ext = pd.concat(ext)
ext.to_csv(P("results/layer_a/extension.csv"), index=False)
print(pd.DataFrame(M).round(3).to_string()); print(pd.DataFrame(C).round(3).to_string())
print(pd.DataFrame(R).round(3).to_string()); print(ext.round(3).to_string())

# ---------- log ----------
w = f"""# Layer A run log (scripts/run_layer_a.py, seed {SEED}, {NB} bootstrap resamples)

Self-check: passed (medians 8.55/9.0, 26/21/26 target seasons, severe == smax > median, no held-out season in training, p in [0,1]).

## Choices where protocol section 8 was not explicit
- Seasons used: 1992-2016 for Cầu Quan and Trà Vinh (25), 1997-2016 for Sơn Đốc (20): the previous-season-max predictor
  needs season Y-1 in the record, so 1991 / 1996 drop out. 70 station-seasons. Medians (target) still use the full reference period (frozen definition),
  so the held-out season contributes to its own target threshold (small leak into the label, not into the features).
- Severe = strictly above the station median; upper-tercile = above the station's 2/3 quantile (numpy linear interpolation). Base rates are reported in metrics.csv (ties/sample size make them not exactly 0.5).
- ONI = NOAA CPC ANOM column for JAS of Y-1. Tân Châu predictor = mean of Sep and Oct monthly Q of Y-1. GloFAS predictor = mean of daily Sep-Oct Q of Y-1 (seasons 1998-2016).
- Previous-season max enters station-demeaned (training-fold station mean), then all three slopes are standardised on training data (pooled mean/sd) because gauges differ in scale.
- Model: LogisticRegression(penalty=None), station dummies without a separate intercept, 3 slopes. Unpenalised because 70 rows / 6 parameters is well-posed;
  an assertion stops the run if any |coef| >= 10 (quasi-separation) -> would switch to weak L2 and be logged. It never triggered.
- Climatology reference in each fold = training-fold base rate of the SAME station (matches station intercepts). BSS = 1 - sum Brier(model) / sum Brier(clim).
- Bootstrap: seasons resampled with replacement (all stations of a season together), percentile 95% CI; AUC is pooled across stations (station base rates are near 0.5, so mixing is mild); per-station AUC also given.
- Reliability: 3 fixed bins on pooled LOSO p (0-1/3, 1/3-2/3, 2/3-1); more bins would be empty at n=70.
- Apel et al. 2020 comparison: not compared (no comparable number available without fetching the paper).

## Extension 2022 / 2025
- Model trained on all 1992-2016 station-seasons of the main spec. Discharge: GloFAS Kratie Sep-Oct of Y-1 mapped to the Tân Châu scale with a linear fit over overlap 1997-2016
  (slope {lin.coef_[0]:.3f}, intercept {lin.intercept_:.0f}, r = {r_ov:.3f}); chosen over the GloFAS-model variant so the pre-registered main model is unchanged.
- Observed seasonal max = max over bulletin issue dates Dec(Y-1)-Jun(Y) (Sơn Đốc: Feb-Mar issues only), a LOWER bound; coverage per station is in extension.csv (n_bulletins).
  Previous-season max for the lag predictor is likewise a bulletin lower bound (2021 covers Jan-Feb only; 2024 covers Mar-May only) and is therefore biased low; this is a known weakness of the extension.
- Bulletin dekad Smax vs 2-hourly/daily gauge max: different support, so comparison to the medians is approximate.

## Variants run
""" + "\n".join(L) + "\n\n## Proposed deviations\nNone required. (Only notes: seasons lost to the lag predictor; unpenalised fit; GloFAS rescaling for the extension.)\n"
open(P("results/layer_a/run_log.md"), "w", encoding="utf-8").write(w)
