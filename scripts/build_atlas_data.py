"""Build atlas/data/*.json from results/core_b (aggregated scores only; no per-row NCHMF values)."""
import json, math
from pathlib import Path
import pandas as pd

R = Path(__file__).resolve().parent.parent
OUT = R / "atlas" / "data"
OUT.mkdir(parents=True, exist_ok=True)
SEL = dict(variant="main", model="hgb")


def clean(x):
    if isinstance(x, float) and not math.isfinite(x):
        return None
    return round(float(x), 4) if isinstance(x, (float,)) else x


def km(v):
    try:
        return float(v)
    except ValueError:
        return str(v)  # e.g. "Nội đồng" (inland canal)


def pick(df, **kw):
    for k, v in {**SEL, **kw}.items():
        df = df[df[k] == v]
    return df

# ---- stations --------------------------------------------------------------
pred = pd.read_csv(R / "results/core_b/predictions.csv", low_memory=False)
meta = pd.read_csv(R / "data/meta/station_meta.csv").set_index("station")
fwd = pick(pred, design="forward").dropna(subset=["y_obs", "bench_persist", "bench_official"])
loso = pick(pred, design="loso")


def cov(d):
    return ((d.y_obs >= d.lo_cqr) & (d.y_obs <= d.hi_cqr)).mean()


stations = []
for st, d in fwd.groupby("station"):
    m = meta.loc[st] if st in meta.index else None
    ok = lambda c: m is not None and pd.notna(m[c])
    ls = loso[loso.station == st].dropna(subset=["y_obs"])
    mm, mp = (d.y_obs - d.med_raw).abs().mean(), (d.y_obs - d.bench_persist).abs().mean()
    stations.append({
        "station": st,
        "river": m.river if ok("river") else None,
        "km_from_mouth": km(m.km_from_mouth) if ok("km_from_mouth") else None,
        "province_old": m.province_old if ok("province_old") else None,
        "province_new": m.province_new if ok("province_new") else None,
        "lat": float(m.lat) if ok("lat") and ok("lon") else None,
        "lon": float(m.lon) if ok("lat") and ok("lon") else None,
        "n": int(len(d)),
        "mae_model": clean(mm), "mae_persist": clean(mp),
        "mae_official": clean((d.y_obs - d.bench_official).abs().mean()),
        "skill_vs_persist": clean(1 - mm / mp) if mp > 0 else None,
        "cov_cqr": clean(cov(d)), "width_cqr": clean((d.hi_cqr - d.lo_cqr).mean()),
        "cov_cqr_loso": clean(cov(ls)) if len(ls) else None,
        "n_loso": int(len(ls)),
    })
stations.sort(key=lambda s: s["station"])

# ---- summary ---------------------------------------------------------------
boot = pick(pd.read_csv(R / "results/core_b/bootstrap_ci.csv"), design="forward")
met = pick(pd.read_csv(R / "results/core_b/metrics.csv"), design="forward")
bp = boot[boot.scope == "pooled"].set_index("metric")
ci = lambda k: {"est": clean(bp.loc[k, "estimate"]), "lo": clean(bp.loc[k, "ci_lo"]), "hi": clean(bp.loc[k, "ci_hi"])}
h1k = ["mae_diff_persist", "mae_diff_clim", "mae_diff_official", "brier_diff_persist_4", "brier_diff_clim_4"]
h1 = {k: ci(k) for k in h1k}
for v in h1.values():
    v["met"] = v["hi"] < 0
cc = ci("cov_cqr")
rev = ci("rev_area_diff_official")
loso_b = pick(pd.read_csv(R / "results/core_b/bootstrap_ci.csv"), design="loso", scope="pooled").set_index("metric")
lopo_b = pick(pd.read_csv(R / "results/core_b/bootstrap_ci.csv"), design="lopo", scope="pooled").set_index("metric")
seasons = []
for s in ["2024", "2025", "2026", "pooled"]:
    g = met[met.scope == s].set_index("metric").value
    seasons.append({"season": s, **{k: clean(g[k]) for k in
        ["n", "mae_model", "mae_persist", "mae_official", "cov_cqr", "width_cqr", "brier_model_4", "pss_model_4", "pss_official_4"]}})
summary = {
    "model": "HGB (histogram gradient boosting, quantile + CQR)", "design": "forward-by-season, test seasons 2024-2026",
    "H1": {"supported": all(v["met"] for v in h1.values()), "criteria": h1,
           "pss4": {"model": clean(bp.loc["pss_model_4", "estimate"]), "official": clean(bp.loc["pss_official_4", "estimate"]), "diff": ci("pss_diff_official_4")}},
    "H2": {"H2a_supported": 0.87 <= cc["est"] <= 0.93, "cov_cqr_forward": cc,
           "cov_cqr_loso": {"est": clean(loso_b.loc["cov_cqr", "estimate"]), "lo": clean(loso_b.loc["cov_cqr", "ci_lo"]), "hi": clean(loso_b.loc["cov_cqr", "ci_hi"])},
           "cov_cqr_lopo": {"est": clean(lopo_b.loc["cov_cqr", "estimate"]), "lo": clean(lopo_b.loc["cov_cqr", "ci_lo"]), "hi": clean(lopo_b.loc["cov_cqr", "ci_hi"])}},
    "H3": {"supported": rev["lo"] > 0, "rev_area_diff_official": rev,
           "rev_area": {k: clean(bp.loc["rev_area_" + k, "estimate"]) for k in ["model", "official", "persist"]}},
    "seasons": seasons,
}

# ---- value curve & reliability ---------------------------------------------
rc = pick(pd.read_csv(R / "results/core_b/rev_curve.csv"), design="forward")
vc = {"cost_loss": rc.cost_loss.round(4).tolist(),
      **{k: [clean(x) for x in rc[c]] for k, c in [("model", "V_model"), ("official", "V_official"), ("persistence", "V_persist")]}}
rl = pick(pd.read_csv(R / "results/core_b/reliability.csv"), design="forward", scope="pooled", threshold=4)
rel = {"threshold": 4, "bins": [{"bin": r.bin, "n": int(r.n), "mean_prob": clean(r.mean_prob), "obs_freq": clean(r.obs_freq)} for r in rl.itertuples()]}

for name, obj in [("stations", stations), ("summary", summary), ("value_curve", vc), ("reliability", rel)]:
    (OUT / f"{name}.json").write_text(json.dumps(obj, ensure_ascii=False, indent=1, allow_nan=False), encoding="utf-8")

# ---- self-check: nothing per-row / transcribed ------------------------------
FORBID = {"y_obs", "smax_cur", "bench_persist", "bench_official", "obs", "official_fc", "issue_date", "bench_clim"}


def walk(o, depth=0):
    if isinstance(o, dict):
        assert not FORBID & set(o), FORBID & set(o)
        for v in o.values():
            walk(v)
    elif isinstance(o, list):
        for v in o:
            walk(v)

for name in ["stations", "summary", "value_curve", "reliability"]:
    walk(json.loads((OUT / f"{name}.json").read_text(encoding="utf-8")))
st = json.loads((OUT / "stations.json").read_text(encoding="utf-8"))
assert all(not isinstance(v, (list, dict)) for s in st for v in s.values()), "per-station arrays"
assert len(st) <= 30 and all(s["n"] > 0 for s in st)
assert len(json.dumps(st)) < len(st) * 700
print(f"self-check OK: {len(st)} stations, {sum(s['lat'] is not None for s in st)} with coordinates")
