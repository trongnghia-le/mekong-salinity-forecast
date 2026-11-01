"""Build data/processed/features.csv: one row per (issue_date, station) with an observed Smax at issue.
Run: python -I -X utf8 scripts/build_features.py [--lag 5]

NO-LEAKAGE RULES
 - Everything except `tide_*` uses only information available on issue_date t.
 - GloFAS features use days <= t - LAG (LAG = --lag, default 5; the protocol sets it).
 - GloFAS anomaly climatology = same calendar window in 1997-2015 only. It uses no target-period data as long as
   the evaluation seasons are >= 2020 (they are: all bulletins are 2020+). If a protocol evaluates earlier years,
   shrink the climatology window.
 - Tide features describe the TARGET dekad (astronomical, predictable, so allowed).
 - ONI: for issue month M, the 3-month season whose last month is M-2 (e.g. issue in March -> NDJ, ends January).
   NOAA publishes a season about 1 month after it ends, so this is conservative (one month spare).
 - Benchmarks (bench_*) and targets (y_*) are NOT features.
 - Climatology benchmark is computed later in modelling from training seasons only.
EXCLUDED: the 5-day bulletin of 2021-01-05 (obs 01-05, fc 06-10): not a dekad, so not a row and not a target.
ODV (CC BY-SA) 2021/2022 dekad tables fill observation dekads missing from the PDFs (obs_source='odv', no official
forecast); derived rows therefore inherit CC BY-SA.
"""
import argparse, calendar, csv, math, os, sys, urllib.request
from collections import Counter
from datetime import date, timedelta

import numpy as np
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from parse_nchmf import norm, CANON  # noqa: E402

P = lambda *a: os.path.join(ROOT, *a)
ONI_URL = "https://www.cpc.ncep.noaa.gov/data/indices/oni.ascii.txt"
CLIM_YEARS = range(1997, 2016)
SYNODIC, ANOMALISTIC = 29.530588861, 27.55454989

# ---------- river -> group (document: substring on the canonical river name) ----------
def river_group(r):
    r = norm(r).casefold()
    for key, g in (("sài gòn", "SaiGon"), ("vàm cỏ", "VamCo"), ("tiểu", "Tien"), ("đại", "Tien"), ("tiền", "Tien"),
                   ("hàm luông", "HamLuong"), ("cổ chiên", "CoChien"), ("hậu", "Hau"), ("như gia", "Hau"),
                   ("maspero", "Hau"), ("gành hào", "GanhHao"), ("sông đốc", "WestSea"), ("kiên", "WestSea"),
                   ("cái lớn", "WestSea"), ("cái bé", "WestSea")):
        if key in r:
            return g
    return "other"

# ---------- dekad helpers ----------
def is_dekad_end(d):
    return d.day in (10, 20) or d.day == calendar.monthrange(d.year, d.month)[1]

def dekad_of(d):  # end of the dekad containing d
    if d.day <= 10: return d.replace(day=10)
    if d.day <= 20: return d.replace(day=20)
    return d.replace(day=calendar.monthrange(d.year, d.month)[1])

def next_dekad(end):  # (start, end) of the dekad after the one ending `end`
    s = end + timedelta(days=1)
    return s, dekad_of(s)

def prev_dekad_end(end):
    return dekad_of(end.replace(day=1) - timedelta(days=1)) if end.day == 10 else (
        end.replace(day=10) if end.day == 20 else end.replace(day=20))

def season_of(d):
    y = d.year + (d.month == 12)
    return y, f"{y-1}-{str(y)[2:]}"

def dekad_idx(end):  # 0 = Dec 1-10 ... 20 = Jun 21-30 (idx of the dekad that ENDS on `end`)
    return ((end.month - 12) % 12) * 3 + (end.day > 10) + (end.day > 20)

# ---------- astronomy (Meeus ch.49 + mean perigee ch.50) ----------
def jd_of(d, hour_utc=0.0):
    return 2451544.5 + (d - date(2000, 1, 1)).days + hour_utc / 24

def moon_phase_jde(k):  # k integer = new moon, k+.5 = full moon (Meeus 49.1, main periodic terms)
    T = k / 1236.85
    jde = 2451550.09766 + SYNODIC * k + 0.00015437 * T**2
    E = 1 - 0.002516 * T - 0.0000074 * T**2
    r = math.radians
    M = r(2.5534 + 29.10535670 * k - 0.0000014 * T**2)
    Mp = r(201.5643 + 385.81693528 * k + 0.0107582 * T**2)
    F = r(160.7108 + 390.67050284 * k - 0.0016118 * T**2)
    new = k == round(k)
    c = ((-0.40720, 0.17241, 0.01608, 0.01039, 0.00739, -0.00514, 0.00208) if new else
         (-0.40614, 0.17302, 0.01614, 0.01043, 0.00734, -0.00515, 0.00209))
    return jde + (c[0] * math.sin(Mp) + c[1] * E * math.sin(M) + c[2] * math.sin(2 * Mp) + c[3] * math.sin(2 * F)
                  + c[4] * E * math.sin(Mp - M) + c[5] * E * math.sin(Mp + M) + c[6] * E**2 * math.sin(2 * M))

# syzygies (new and full moons) 2019-2027 as sorted JDs; flag new=True
SYZ = sorted((moon_phase_jde(k / 2), k % 2 == 0) for k in range(int((2019 - 2000) * 12.3685) * 2, int((2028 - 2000) * 12.3685) * 2))
SYZ_JD = np.array([s[0] for s in SYZ])

def tide_features(start, end):
    """Over the target dekad, evaluated at local noon (UTC+7 = 05:00 UT) of each day.
    tide_spring_days  : days within +-2 d of a new or full moon
    tide_abscos_mean  : mean |cos(2*pi*f)|, f = fraction of the synodic month elapsed since the previous new moon
                        (1 at new/full, 0 at quarters)  -> spring-neap index
    tide_perigee_cos  : mean cos(2*pi*(t - t_perigee)/27.5545) with t_perigee the mean perigee (1 = at perigee)
    tide_perigee_min  : min over the dekad of |days to the nearest mean perigee| (mean perigee is accurate to ~2 d)"""
    days = [start + timedelta(days=i) for i in range((end - start).days + 1)]
    t = np.array([jd_of(d, 5.0) for d in days])
    near = np.min(np.abs(t[:, None] - SYZ_JD[None, :]), axis=1)
    news = np.array([s[0] for s in SYZ if s[1]])
    i = np.searchsorted(news, t) - 1
    f = (t - news[i]) / (news[i + 1] - news[i])
    # Meeus 50.1: mean perigee JDE = 2451534.6698 + 27.55454989 k
    ph = 2 * math.pi * ((t - 2451534.6698) / ANOMALISTIC)
    pd_ = ((t - 2451534.6698) / ANOMALISTIC + 0.5) % 1 - 0.5
    return dict(tide_spring_days=int((near <= 2).sum()), tide_abscos_mean=float(np.abs(np.cos(2 * math.pi * f)).mean()),
                tide_perigee_cos=float(np.cos(ph).mean()), tide_perigee_min=float(np.abs(pd_).min() * ANOMALISTIC))

# ---------- ONI ----------
def load_oni():
    path = P("data/raw/oni/oni.ascii.txt")
    if not os.path.exists(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        req = urllib.request.Request(ONI_URL, headers={"User-Agent": "mekong-salinity-research/0.1"})
        open(path, "wb").write(urllib.request.urlopen(req, timeout=60).read())
    seas = ["DJF", "JFM", "FMA", "MAM", "AMJ", "MJJ", "JJA", "JAS", "ASO", "SON", "OND", "NDJ"]
    out = {}  # (year of centre month, centre month) -> anom
    for ln in open(path).read().split("\n")[1:]:
        p = ln.split()
        if len(p) == 4:
            out[(int(p[1]), seas.index(p[0]) + 1)] = float(p[3])  # DJF centre = Jan (1) ... NDJ centre = Dec (12)
    return out

def oni_for(oni, d):
    end_m = d.month - 2          # season ends at month M-2, so its centre month is M-3
    c = end_m - 1
    y = d.year
    while c < 1: c += 12; y -= 1
    return oni.get((y, c), np.nan), f"centre {y}-{c:02d}"

# ---------- GloFAS ----------
def glofas_features(q, t, lag, clim):
    e = pd.Timestamp(t - timedelta(days=lag))
    w10, w30 = q.loc[e - pd.Timedelta(days=9):e], q.loc[e - pd.Timedelta(days=29):e]
    ok30 = len(w30) == 30
    out = dict(q_mean10=w10.mean() if len(w10) == 10 else np.nan, q_mean30=w30.mean() if ok30 else np.nan,
               q_min30=w30.min() if ok30 else np.nan, glofas_last_day=e.date().isoformat())
    c = clim(e)
    out["q_mean30_clim"] = c
    out["q_anom30"] = out["q_mean30"] / c if ok30 and c == c else np.nan  # ratio to 1997-2015 same-window mean
    return out

def make_clim(q):
    cache = {}
    def clim(e):
        key = (e.month, e.day)
        if key not in cache:
            v = []
            for y in CLIM_YEARS:
                try: ee = pd.Timestamp(y, e.month, e.day)
                except ValueError: ee = pd.Timestamp(y, e.month, 28)
                w = q.loc[ee - pd.Timedelta(days=29):ee]
                if len(w) == 30: v.append(w.mean())
            cache[key] = float(np.mean(v)) if v else np.nan
        return cache[key]
    return clim

# ---------- observations ----------
def load_obs():
    o = pd.read_csv(P("data/processed/nchmf_obs.csv"), parse_dates=["issue_date", "obs_start", "obs_end"])
    o = o[o.obs_end.map(lambda x: is_dekad_end(x.date()))]  # drops the 5-day 2021-01-05 bulletin
    assert (o.issue_date == o.obs_end).all()
    o = o.assign(obs_source="bulletin")
    # ODV fill
    with open(P("data/raw/odv/salinization_2021_2022_vi.csv"), encoding="utf-8-sig") as fh:
        rows = list(csv.reader(fh))
    hdr, rows = rows[0], rows[1:]
    have = set(zip(o.obs_end.dt.date, o.station))
    add = []
    for y, blk in ((2021, rows[:30]), (2022, rows[30:])):
        for r in blk:
            st = CANON.get(norm(r[0]).casefold())
            if st is None: continue
            for c in range(4, 13):
                dd, mm = hdr[c].replace(" ", "").split("-")[1].split("/")
                end = date(y, int(mm), int(dd))
                v = r[c].strip()
                if v in ("", "-") or (end, st) in have: continue
                add.append(dict(issue_date=pd.Timestamp(end), station=st, smax_obs_gL=float(v.replace(",", ".")),
                                source_file="odv:salinization_2021_2022_vi.csv", obs_source="odv"))
    return pd.concat([o, pd.DataFrame(add)], ignore_index=True), len(add)

def station_statics(o):
    """Per station: modal km / river / inland_canal over all rows (a few early rows have shifted columns);
    province_canon = modal province over pre-2026 rows excluding 2022 (shifted columns, 2026 = post-merger names)."""
    b = o[o.obs_source == "bulletin"]
    mode = lambda s: Counter(s.dropna()).most_common(1)[0][0] if s.notna().any() else np.nan
    st = b.groupby("station").agg(km_from_mouth=("km_from_mouth", mode), river=("river", mode), inland_canal=("inland_canal", mode))
    ok = b[(b.issue_date.dt.year < 2026) & (b.issue_date.dt.year != 2022)]
    st["province_canon"] = ok.groupby("station").province.agg(mode)
    st["province_canon"] = st.province_canon.fillna(b.groupby("station").province.agg(mode))
    st["river_group"] = st.river.map(river_group)
    return st

def build(lag):
    o, n_odv = load_obs()
    st = station_statics(o)
    fc = pd.read_csv(P("data/processed/nchmf_fc.csv"), parse_dates=["issue_date", "fc_start", "fc_end"])
    fc = fc.set_index(["issue_date", "station"])
    q = pd.read_csv(P("data/raw/glofas/kratie_glofas_daily.csv"), parse_dates=["date"]).set_index("date").q_m3s
    clim, oni = make_clim(q), load_oni()
    val = o.dropna(subset=["smax_obs_gL"]).set_index([o.dropna(subset=["smax_obs_gL"]).issue_date.dt.date, "station"]).smax_obs_gL
    val = val[~val.index.duplicated()]
    cur = o.dropna(subset=["smax_obs_gL"]).drop_duplicates(["issue_date", "station"])
    rows, tide_cache = [], {}
    for r in cur.itertuples():
        t = r.issue_date.date()
        ts, te = next_dekad(t)
        y = val.get((te, r.station), np.nan)
        pe = prev_dekad_end(t)
        prev = val.get((pe, r.station), np.nan)
        fk = (r.issue_date, r.station)
        bo = np.nan
        if fk in fc.index:
            f = fc.loc[fk]
            if f.fc_start.date() == ts and f.fc_end.date() == te: bo = f.fc_low_gL
        s = st.loc[r.station]
        sy, sl = season_of(t)
        oni_v, oni_lab = oni_for(oni, t)
        if (ts, te) not in tide_cache: tide_cache[(ts, te)] = tide_features(ts, te)
        d = dict(issue_date=t, season=sy, season_label=sl, station=r.station, dekad_of_season=dekad_idx(t),
                 target_start=ts, target_end=te, y_smax_next=y)
        for c in (1, 2, 4): d[f"y_exceed_{c}"] = np.nan if y != y else int(y > c)
        d.update(bench_persist=r.smax_obs_gL, bench_official=bo, smax_cur=r.smax_obs_gL, smax_prev=prev,
                 delta_smax=r.smax_obs_gL - prev, log1p_smax_cur=np.log1p(r.smax_obs_gL), log1p_smax_prev=np.log1p(prev),
                 km_from_mouth=s.km_from_mouth, inland_canal=s.inland_canal, river=s.river, river_group=s.river_group,
                 province_canon=s.province_canon, province_as_printed=getattr(r, "province", np.nan))
        d.update(glofas_features(q, t, lag, clim))
        d.update(tide_cache[(ts, te)])
        d.update(oni=oni_v, oni_season=oni_lab, source_file=r.source_file, obs_source=r.obs_source)
        rows.append(d)
    df = pd.DataFrame(rows).sort_values(["issue_date", "station"]).reset_index(drop=True)
    df["log1p_delta_smax"] = df.log1p_smax_cur - df.log1p_smax_prev
    df["glofas_lag_days"] = lag
    return df, n_odv

def self_check(df, lag):
    assert (df.bench_persist == df.smax_cur).all()
    assert (pd.to_datetime(df.target_start) - pd.to_datetime(df.issue_date) == pd.Timedelta(days=1)).all()
    assert (pd.to_datetime(df.glofas_last_day) <= pd.to_datetime(df.issue_date) - pd.Timedelta(days=lag)).all()
    assert (pd.to_datetime(df.issue_date) != pd.Timestamp("2021-01-05")).all()
    # new moons 2024 (local UTC+7): Jan 11 11:57 UT, Feb 9 22:59 UT, Mar 10 09:00 UT; full Jan 25 17:54 UT
    for k, (y, m, d, h) in {1: (2024, 1, 11, 11.95), 2: (2024, 2, 9, 22.98), 3: (2024, 3, 10, 9.0)}.items():
        kk = round((jd_of(date(y, m, d), h) - 2451550.09766) / SYNODIC)
        assert abs(moon_phase_jde(kk) - jd_of(date(y, m, d), h)) < 0.1, (y, m, d, moon_phase_jde(kk))
    assert abs(moon_phase_jde(round((jd_of(date(2024, 1, 25), 17.9) - 2451550.09766) / SYNODIC - .5) + .5) - jd_of(date(2024, 1, 25), 17.9)) < 0.1
    # ONI rule: issue 2024-03-20 -> season ending Jan 2024 = NDJ 2023/24, centre Dec 2023
    assert oni_for({(2023, 12): 1.9}, date(2024, 3, 20))[0] == 1.9
    # row identity: target of 2024-03-20/Cát Lái equals Bảng 1 of the 2024-03-31 bulletin
    o = pd.read_csv(P("data/processed/nchmf_obs.csv"))
    a = df[(df.issue_date == date(2024, 3, 20)) & (df.station == "Cát Lái")].iloc[0]
    assert a.y_smax_next == o[(o.issue_date == "2024-03-31") & (o.station == "Cát Lái")].smax_obs_gL.iloc[0]
    print("self-check OK")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--lag", type=int, default=5, help="GloFAS latency in days")
    lag = ap.parse_args().lag
    df, n_odv = build(lag)
    df.to_csv(P("data/processed/features.csv"), index=False, encoding="utf-8")
    self_check(df, lag)
    print("rows", len(df), "with target", df.y_smax_next.notna().sum(), "ODV rows added to obs pool", n_odv)
    print(df.groupby("season").agg(rows=("station", "size"), with_target=("y_smax_next", "count"), with_official=("bench_official", "count")))
    print((df.isna().mean() * 100).round(1).to_string())
