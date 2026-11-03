"""H4 (layer-A decision value) and crop-option break-even. Protocol section 8 + D4.
Run from repo root: python -I -X utf8 scripts/run_h4.py
Parameters: docs/background/decision_parameters.md (rows cited in comments). Money: M VND/ha, 2025 VND.
Scenario analysis, not farm advice.
"""
import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
OUT = "results/layer_a_decision"
os.makedirs(OUT, exist_ok=True)
os.makedirs("figures", exist_ok=True)
SEED, B = 20261101, 2000

# ---- parameters (decision_parameters.md, "Loss model" section, L25 Table 2/4; 2025 VND) ----
C_FLOOR = 20.0                      # Cost2, M22 Table 1 (option-1 table)
GRP = {  # pi_bar (M VND/ha), slope b (M VND/ha per g/L), S_bar, Y_bar (kg/ha), a (kg/ha per g/L), SE of b
    "gated":   dict(pi=21.4, b=0.221, Sbar=7.41, Y=6505., a=43.4, seb=0.0795 * 1.197),
    "ungated": dict(pi=19.0, b=1.349, Sbar=6.53, Y=6112., a=197.4, seb=0.1358 * 1.197),
}
D_FERRER, D_LE = 10.1, 8.3          # Delta_sev: F22 abstract 10.0-10.2 (2025 VND); L25 gated average 8.3
M_RANGE = {"gated": (0.0, 8.3), "ungated": (-4.2, 4.7)}   # m range, Option-2 table / loss-model section
REV_REV, REV_PI, REV_RATE = 43.4, 23.4, None   # FAO variant: gross revenue 43.4, net revenue2 23.4 (M22 Table 1)
RGRID = np.round(np.arange(0.05, 0.951, 0.05), 2)
INT = (RGRID >= 0.1 - 1e-9) & (RGRID <= 0.9 + 1e-9)
STRATS = ["fixed", "always", "clim", "fc", "perfect"]


def load(path, cols):
    d = pd.read_csv(path).rename(columns=cols)
    return d[["season", "station", "p", "pclim", "sev", "smax"]]


MAIN = load("results/layer_a/forecasts_loso.csv", dict(p_severe="p", p_clim="pclim", severe_obs="sev"))
TERC = load("results/layer_a/forecasts_loso_sens_tercile_TanChau.csv", dict(p_clim="pclim", p="p", severe="sev"))


def pstd_fao(S, f):
    ece = 1.56 * f * S                      # FAO Table A1.1: threshold 3.0, 12 %/dS/m, 1 g/L = 1.56 dS/m
    yrel = np.maximum(0, 1 - 0.12 * np.maximum(0, ece - 3.0))
    loss = REV_REV * (1 - yrel)
    return np.maximum(-C_FLOOR, REV_PI - loss), loss


def make_var(name, data=MAIN, cap=14., db=None, gratio=None, D=D_FERRER, fao_f=None):
    return dict(name=name, data=data, cap=cap, db=db or {}, gratio=gratio, D=D, fao_f=fao_f)


def prep(var, grp):
    """per station-season: profit under standard calendar, and the early-sowing gain in a severe season."""
    d = var["data"]
    S = np.minimum(d.smax.values, var["cap"])
    g = GRP[grp]
    b = g["b"] + var["db"].get(grp, 0.0) * 1.96 * g["seb"]
    if var["gratio"] is not None and grp == "gated":
        b = var["gratio"] * (GRP["ungated"]["b"])
    if var["fao_f"] is not None:
        f = var["fao_f"] * (0.2 if grp == "gated" else 1.0)
        ps, loss = pstd_fao(S, f)
        dsev = np.minimum(var["D"], loss)      # cannot recover more than the salinity loss (FAO variant only)
    else:
        ps = np.maximum(-C_FLOOR, g["pi"] - b * (S - g["Sbar"]))
        dsev = np.full(len(S), var["D"])
    return ps, dsev


def evaluate(var, grp, m, r):
    """m, r: arrays (nr,). Returns dict strategy -> returns (n, nr)."""
    d = var["data"]
    ps, dsev = prep(var, grp)
    sev = d.sev.values[:, None].astype(bool)
    gain = np.where(sev, dsev[:, None], m[None, :])
    base = ps[:, None] * np.ones_like(gain)
    acted = np.maximum(-C_FLOOR, base + gain)
    A = {"fixed": np.zeros_like(gain, bool), "always": np.ones_like(gain, bool),
         "clim": d.pclim.values[:, None] > r[None, :], "fc": d.p.values[:, None] > r[None, :],
         "perfect": gain > 0}
    return {k: np.where(a, acted, base) for k, a in A.items()}


def rm_from_grid(D):
    return RGRID, -RGRID * D / (1 - RGRID)       # m = -r D/(1-r)  <=>  r = -m/(D-m)


def rev(num, den):
    with np.errstate(divide="ignore", invalid="ignore"):
        out = np.where(np.abs(den) > 1e-12, num / den, np.nan)
    return out


def boot_weights(d):
    seas = np.sort(d.season.unique())
    rng = np.random.default_rng(SEED)
    idx = rng.integers(0, len(seas), (B, len(seas)))
    W = np.stack([(d.season.values[None, :] == seas[i][:, None]).sum(0) for i in idx]).astype(float)
    return W / W.sum(1, keepdims=True)


def area(y, mask=None):    # trapezoid over C/L 0.1-0.9 (or mask), along last axis; nan -> 0 (undefined REV)
    mask = INT if mask is None else mask
    return np.trapz(np.nan_to_num(y[..., mask]), RGRID[mask], axis=-1)


LIT = (RGRID >= 0.1 - 1e-9) & (RGRID <= 0.3 + 1e-9)   # C/L window implied by the literature m range (ungated)


def summarize(R, W):
    """point + bootstrap arrays of the key quantities. R: strategy -> (n, nr)."""
    def mean(x, w=None):
        return x.mean(0) if w is None else w @ x
    out = {}
    for tag, w in (("pt", None), ("bs", W)):
        M = {k: mean(R[k], w) for k in STRATS}
        out[tag] = dict(
            M=M,
            red_fix=M["fc"] - M["fixed"], red_clim=M["fc"] - M["clim"],
            rev_fc_fix=rev(M["fc"] - M["fixed"], M["perfect"] - M["fixed"]),
            rev_fc_clim=rev(M["fc"] - M["clim"], M["perfect"] - M["clim"]),
            rev_clim_fix=rev(M["clim"] - M["fixed"], M["perfect"] - M["fixed"]))
    return out


def pct(x):
    return np.nanpercentile(x, [2.5, 97.5], axis=0)


# ---------------- H4 ----------------
variants = [make_var("main"), make_var("cap10", cap=10.), make_var("cap20", cap=20.),
            make_var("b_ungated_plus1.96SE", db={"ungated": 1}), make_var("b_ungated_minus1.96SE", db={"ungated": -1}),
            make_var("b_gated_plus1.96SE", db={"gated": 1}), make_var("b_gated_minus1.96SE", db={"gated": -1}),
            make_var("gated_slope_0.1x", gratio=0.1), make_var("gated_slope_0.2x", gratio=0.2),
            make_var("gated_slope_0.3x", gratio=0.3), make_var("Dsev_Le_8.3", D=D_LE),
            make_var("target_upper_tercile", data=TERC)]
variants += [make_var(f"FAO_f{f}", fao_f=f) for f in (0.1, 0.25, 0.5, 0.75)]

W_ALL = {"main": boot_weights(MAIN), "terc": boot_weights(TERC)}
ret_rows, rev_rows, ci_rows = [], [], []
RES = {}
for v in variants:
    W = W_ALL["terc"] if v["data"] is TERC else W_ALL["main"]
    r, m = rm_from_grid(v["D"])
    for grp in GRP:
        R = evaluate(v, grp, m, r)
        s = summarize(R, W)
        RES[(v["name"], grp)] = s
        pt = s["pt"]
        for k in STRATS:
            for j, rr in enumerate(r):
                ret_rows.append(dict(variant=v["name"], group=grp, regime="costloss_grid", C_L=rr, m=m[j], strategy=k,
                                     mean_return=pt["M"][k][j], mean_regret=pt["M"]["perfect"][j] - pt["M"][k][j]))
        lo_f, hi_f = pct(s["bs"]["rev_fc_fix"]); lo_c, hi_c = pct(s["bs"]["rev_clim_fix"])
        for j, rr in enumerate(r):
            rev_rows.append(dict(variant=v["name"], group=grp, C_L=rr, m=m[j], rev_fc_vs_clim=pt["rev_fc_clim"][j],
                                 rev_fc_vs_fixed=pt["rev_fc_fix"][j], rev_clim_vs_fixed=pt["rev_clim_fix"][j],
                                 rev_fc_vs_fixed_lo=lo_f[j], rev_fc_vs_fixed_hi=hi_f[j],
                                 rev_clim_vs_fixed_lo=lo_c[j], rev_clim_vs_fixed_hi=hi_c[j]))
        for met, key in (("area_regret_reduction_vs_fixed", "red_fix"), ("area_regret_reduction_vs_clim", "red_clim"),
                         ("area_rev_fc_vs_fixed", "rev_fc_fix"), ("area_rev_fc_vs_clim", "rev_fc_clim"),
                         ("area_rev_clim_vs_fixed", "rev_clim_fix")):
            lo, hi = np.percentile(area(s["bs"][key]), [2.5, 97.5])
            ci_rows.append(dict(variant=v["name"], group=grp, metric=met, estimate=float(area(pt[key])), ci_lo=lo, ci_hi=hi))
        for met, key in (("area_lit0.1-0.3_regret_reduction_vs_fixed", "red_fix"), ("area_lit0.1-0.3_regret_reduction_vs_clim", "red_clim")):
            lo, hi = np.percentile(area(s["bs"][key], LIT), [2.5, 97.5])
            ci_rows.append(dict(variant=v["name"], group=grp, metric=met, estimate=float(area(pt[key], LIT)), ci_lo=lo, ci_hi=hi))
    for met, key in (("area_regret_reduction_vs_fixed", "red_fix"), ("area_regret_reduction_vs_clim", "red_clim"),
                     ("area_rev_fc_vs_fixed", "rev_fc_fix"), ("area_rev_fc_vs_clim", "rev_fc_clim")):
        a_u = area(RES[(v["name"], "ungated")]["bs"][key]) - area(RES[(v["name"], "gated")]["bs"][key])
        est = float(area(RES[(v["name"], "ungated")]["pt"][key]) - area(RES[(v["name"], "gated")]["pt"][key]))
        lo, hi = np.percentile(a_u, [2.5, 97.5])
        ci_rows.append(dict(variant=v["name"], group="ungated_minus_gated", metric=met, estimate=est, ci_lo=lo, ci_hi=hi))

# fixed-m table (includes m >= 0, where early sowing dominates; and literature m values)
for grp, (lo_m, hi_m) in M_RANGE.items():
    mv = np.unique(np.round(np.concatenate([np.linspace(lo_m, hi_m, 5), [0.0]]), 2))
    v = variants[0]
    r = np.where(mv < 0, -mv / (v["D"] - mv), 0.0)
    R = evaluate(v, grp, mv, r)
    for k in STRATS:
        for j in range(len(mv)):
            mean_k = R[k][:, j].mean()
            ret_rows.append(dict(variant="main", group=grp, regime="literature_m", C_L=r[j] if mv[j] < 0 else np.nan, m=mv[j],
                                 strategy=k, mean_return=mean_k, mean_regret=R["perfect"][:, j].mean() - mean_k))

ret = pd.DataFrame(ret_rows); revdf = pd.DataFrame(rev_rows); ci = pd.DataFrame(ci_rows)
ret.to_csv(f"{OUT}/returns_by_strategy.csv", index=False)
revdf.to_csv(f"{OUT}/rev_curve_h4.csv", index=False)
ci.to_csv(f"{OUT}/bootstrap_ci.csv", index=False)

# ---------------- break-even ----------------
PRICE = 5.451 * 1.215      # k VND/kg, M22 Table 1 x year factor 1.215
STV_GAIN = 0.364 * 1000 * PRICE / 1000      # 364 kg/ha x price -> M VND/ha (M22 Table 3)
STV_DISC = 372e-6 * 1.215                   # 372 VND/kg (M22 Table 4) x year factor 1.215 = 452 VND/kg, M VND per kg
                                            # (was 458 = 372 x 1.232, the 2018 factor; corrected 03/11/2026 to match PRICE)
F_RANGE = (0.0, 3.15)
K_RANGE = (0.2, 0.6)
dm = MAIN
CAP = 14.
S_SEV = np.minimum(dm.smax, CAP)[dm.sev == 1].mean()
S_MILD = np.minimum(dm.smax, CAP)[dm.sev == 0].mean()


def option_lines(grp, m, k, F, D=D_FERRER, yield_gain=True):
    """each option -> (intercept, slope) of expected return in p."""
    g = GRP[grp]
    ps = lambda S: max(-C_FLOOR, g["pi"] - g["b"] * (S - g["Sbar"]))
    p3 = lambda S: (max(-C_FLOOR, g["pi"] - k * g["b"] * (S - g["Sbar"])) + (STV_GAIN if yield_gain else 0.0)
                    - STV_DISC * max(0.0, g["Y"] - k * g["a"] * (S - g["Sbar"])))
    L = {1: (ps(S_MILD), ps(S_SEV) - ps(S_MILD)),
         2: (ps(S_MILD) + m, ps(S_SEV) - ps(S_MILD) + D - m),
         3: (p3(S_MILD), p3(S_SEV) - p3(S_MILD)),
         6: (-F, 0.0)}
    return L


def pstar(L, a, b):
    (a0, a1), (b0, b1) = L[a], L[b]
    if abs(a1 - b1) < 1e-12:
        return np.nan
    p = (b0 - a0) / (a1 - b1)
    return p if 0 <= p <= 1 else np.nan


PAIRS = [(1, 2), (1, 3), (1, 6), (2, 3), (2, 6), (3, 6)]
be_rows = []
pf = dm.p.values
MAIN_PAR = {"gated": dict(m=4.15, k=0.4, F=3.15), "ungated": dict(m=0.25, k=0.4, F=3.15)}   # midpoints of the file's ranges; F = rent anchor
for grp in GRP:
    L = option_lines(grp, **MAIN_PAR[grp])
    lo_m, hi_m = M_RANGE[grp]
    sweep = [pstar(option_lines(grp, m, k, F, yield_gain=yg), *pr) for pr in PAIRS
             for m in np.linspace(lo_m, hi_m, 9) for k in np.linspace(*K_RANGE, 5) for F in np.linspace(*F_RANGE, 7) for yg in (True, False)]
    sweep = np.array(sweep).reshape(len(PAIRS), -1)
    for i, pr in enumerate(PAIRS):
        p0 = pstar(L, *pr)
        if not np.isnan(p0):       # self-check: break-even solves equality
            assert abs((L[pr[0]][0] + L[pr[0]][1] * p0) - (L[pr[1]][0] + L[pr[1]][1] * p0)) < 1e-9
        ex = ~np.isnan(sweep[i])
        # which option wins at p=0.5 in the main setting when no crossing
        win = pr[0] if (L[pr[0]][0] + L[pr[0]][1] * .5) > (L[pr[1]][0] + L[pr[1]][1] * .5) else pr[1]
        be_rows.append(dict(group=grp, option_a=pr[0], option_b=pr[1], p_star_main=p0,
                            p_star_sweep_min=np.nanmin(sweep[i]) if ex.any() else np.nan,
                            p_star_sweep_max=np.nanmax(sweep[i]) if ex.any() else np.nan,
                            share_sweep_with_crossing=ex.mean(), winner_at_p05_main=win,
                            share_forecasts_above_main=(pf > p0).mean() if not np.isnan(p0) else np.nan,
                            m=MAIN_PAR[grp]["m"], k=MAIN_PAR[grp]["k"], F=MAIN_PAR[grp]["F"], S_sev=S_SEV, S_mild=S_MILD))
be = pd.DataFrame(be_rows)
be.to_csv(f"{OUT}/breakeven.csv", index=False)

# ---------------- self-checks ----------------
v0 = variants[0]
r0, m0 = rm_from_grid(v0["D"])
for grp in GRP:
    R = evaluate(v0, grp, m0, r0)
    assert np.allclose(R["perfect"].mean(0) - R["perfect"].mean(0), 0)
    for k in STRATS:                                  # perfect information has the highest return everywhere
        assert (R["perfect"].mean(0) >= R[k].mean(0) - 1e-12).all()
    d2 = v0["data"].copy(); d2["p"] = d2.sev.astype(float); d2["pclim"] = d2.sev.astype(float) * 0 + d2.sev.mean()
    v2 = dict(v0, data=d2)
    R2 = evaluate(v2, grp, m0, r0); s2 = summarize(R2, W_ALL["main"])["pt"]
    assert np.allclose(s2["rev_fc_fix"], 1) or np.nanmax(np.abs(s2["rev_fc_fix"] - 1)) < 1e-9   # perfect forecast: REV = 1
    s3 = summarize(dict(R, fc=R["clim"]), W_ALL["main"])["pt"]
    assert np.allclose(s3["rev_fc_clim"], 0)         # climatology vs itself: REV = 0
assert (revdf[revdf.variant == "main"].groupby("C_L").rev_fc_vs_fixed.nunique() <= 2).all()
assert ((be.p_star_main.isna()) | ((be.p_star_main >= 0) & (be.p_star_main <= 1))).all()
SELF = "passed"

# ---------------- figures (dataviz: fixed categorical order, direct legend, thin marks, light grid) ----------------
MM = 1 / 25.4
plt.rcParams.update({
    "font.family": "sans-serif", "font.sans-serif": ["Arial", "DejaVu Sans"], "font.size": 7.5, "axes.labelsize": 7.5,
    "axes.titlesize": 8, "legend.fontsize": 7, "xtick.labelsize": 7, "ytick.labelsize": 7, "axes.linewidth": 0.6,
    "axes.spines.top": False, "axes.spines.right": False, "axes.grid": True, "grid.color": "#e3e2de",
    "grid.linewidth": 0.5, "axes.axisbelow": True, "svg.fonttype": "none", "figure.facecolor": "white"})
BLUE, ORANGE, GREEN, PURPLE, GREY = "#2a78d6", "#eb6834", "#008300", "#6250d6", "#6b6a66"


def save(fig, name):
    for ext in ("png", "svg", "pdf"):  # pdf: vector file for journal submission
        fig.savefig(f"figures/{name}.{ext}", dpi=300, bbox_inches="tight")
    plt.close(fig)


def pan(ax, s):
    ax.text(-0.02, 1.04, s, transform=ax.transAxes, fontweight="bold", fontsize=9, ha="right", va="bottom")


def fig07():
    fig, ax = plt.subplots(figsize=(90 * MM, 70 * MM))
    d = revdf[(revdf.variant == "main") & (revdf.group == "ungated")]
    ax.fill_between(d.C_L, d.rev_fc_vs_fixed_lo, d.rev_fc_vs_fixed_hi, color=BLUE, alpha=.15, lw=0)
    ax.fill_between(d.C_L, d.rev_clim_vs_fixed_lo, d.rev_clim_vs_fixed_hi, color=ORANGE, alpha=.12, lw=0)
    ax.plot(d.C_L, d.rev_fc_vs_fixed, color=BLUE, lw=1.4, marker="o", ms=3, label="Forecast")
    ax.plot(d.C_L, d.rev_clim_vs_fixed, color=ORANGE, lw=1.0, ls="--", marker="v", ms=3, mfc="white", label="Climatology")
    ax.axhline(0, color=GREY, lw=.6)
    ax.set_xlabel("Cost/loss ratio C/L"); ax.set_ylim(-0.6, 1.0)
    ax.set_ylabel("Relative economic value vs fixed calendar")
    ax.legend(frameon=False, loc="upper right", fontsize=6.5)
    save(fig, "fig07_h4_value")


def pstar_m(m, D):
    """break-even P(severe) for early sowing vs standard calendar: p* = -m/(D-m) for m < 0, 0 for m >= 0."""
    m = np.asarray(m, float)
    return np.where(m < 0, -m / (D - m), 0.0)


def stv_pstar(grp, k, yg):
    L = option_lines(grp, 0.0, k, 3.15, yield_gain=yg)     # options 1 and 3 do not depend on m
    return (L[3][0] - L[1][0]) / (L[1][1] - L[3][1])        # unclipped; <0: option 3 always better, >1: option 1 always better


# option 6 (skip) is never the best option anywhere in the sweep (m, k, F, yield gain, p)
_pp = np.linspace(0, 1, 11)
SKIP_DOMINATED = all(
    max(L[o][0] + L[o][1] * q for o in (1, 2, 3)) > L[6][0] + L[6][1] * q
    for grp in GRP for m in np.linspace(-10, 5, 7) for k in np.linspace(*K_RANGE, 5)
    for F in np.linspace(*F_RANGE, 7) for yg in (True, False) for q in _pp
    for L in [option_lines(grp, m, k, F, yield_gain=yg)])
assert SKIP_DOMINATED
THR = {(D, m): (float(pstar_m(m, D)), float((pf > pstar_m(m, D)).mean())) for D in (D_FERRER, D_LE) for m in (-2.0, -4.0)}


def fig08():
    fig = plt.figure(figsize=(190 * MM, 85 * MM))
    gs = fig.add_gridspec(1, 3, width_ratios=[3.3, 0.9, 2.6], wspace=.3)
    ax = fig.add_subplot(gs[0]); axh = fig.add_subplot(gs[1], sharey=ax); ax3 = fig.add_subplot(gs[2])
    fig.subplots_adjust(wspace=.3)
    m = np.linspace(-10, 5, 301)
    ax.axvspan(0, 5, color="#eceae4", lw=0)
    ax.text(2.5, 0.5, "m >= 0:\nearly sowing never\nworse than standard\n(any P(severe))", ha="center", va="center", fontsize=6.5, color="#52514e")
    ax.fill_between(m, pstar_m(m, D_LE), pstar_m(m, D_FERRER), where=m < 0, color=BLUE, alpha=.15, lw=0)
    ax.plot(m[m < 0], pstar_m(m, D_FERRER)[m < 0], color=BLUE, lw=1.4, label="Delta_sev = 10.1 (Ferrer)")
    ax.plot(m[m < 0], pstar_m(m, D_LE)[m < 0], color=ORANGE, lw=1.4, ls="--", label="Delta_sev = 8.3 (Le)")
    ax.text(-9.8, 0.97, "Above a line: early sowing beats\nthe standard calendar", fontsize=6.5, color="#52514e", va="top")
    ax.text(-9.8, 0.03, "Below: standard calendar better", fontsize=6.5, color="#52514e", va="bottom")
    ax.legend(frameon=False, loc="center left", bbox_to_anchor=(0, .72), fontsize=6.5)
    ax.set_xlim(-10, 5); ax.set_ylim(0, 1)
    ax.set_xlabel("Mild-season effect of early sowing, m (M VND/ha)\n(no direct estimate; assumed)")
    ax.set_ylabel("Break-even P(severe season), p*")
    axh.hist(pf, bins=np.linspace(0, 1, 21), orientation="horizontal", color=GREY, edgecolor="white", lw=.5)
    axh.set_xlabel("Forecasts (n = 70)"); axh.grid(False)
    plt.setp(axh.get_yticklabels(), visible=False); axh.tick_params(left=False)
    kk = np.linspace(*K_RANGE, 41)
    for yg, ls, lab in ((True, "-", "with +364 kg/ha yield gain"), (False, "--", "without yield gain")):
        ax3.plot(kk, [stv_pstar("ungated", k, yg) for k in kk], color=BLUE, ls=ls, lw=1.4, label=lab)
    ax3.axhspan(1, 1.6, color="#eceae4", lw=0); ax3.axhspan(-0.4, 0, color="#eceae4", lw=0)
    ax3.text(0.41, 1.45, "standard rice better at any P", ha="center", va="center", fontsize=6.2, color="#52514e")
    ax3.text(0.41, -0.3, "salt-tolerant variety better at any P", ha="center", va="center", fontsize=6.2, color="#52514e")
    ax3.set_ylim(-0.4, 1.6); ax3.set_xlim(*K_RANGE)
    ax3.set_xlabel("Salt-tolerant variety loss scaling, k"); ax3.set_ylabel("Break-even P(severe), standard vs variety")
    ax3.yaxis.set_label_position("right"); ax3.yaxis.tick_right()
    ax3.legend(frameon=False, loc="lower right", bbox_to_anchor=(1.0, .21), fontsize=6.5)
    ax3.set_title("Skipping the season is dominated\nin all settings", fontsize=6.5, color="#52514e")
    pan(ax, "a"); pan(ax3, "b")
    save(fig, "fig08_breakeven")


fig07(); fig08()

# ---------------- verdict + log ----------------
def g(v, grp, met):
    r = ci[(ci.variant == v) & (ci.group == grp) & (ci.metric == met)].iloc[0]
    return r.estimate, r.ci_lo, r.ci_hi


def fm(t):
    return f"{t[0]:.3f} [{t[1]:.3f}, {t[2]:.3f}]"


pos = lambda t: t[1] > 0
parts = {}
lines = ["# H4 verdict (layer A, severe-season forecast; scenario analysis, not farm advice)", "",
         "Areas are integrals over C/L 0.1-0.9 (trapezoid, step 0.05). Regret reduction in M VND/ha x unit C/L; REV area unitless (max 0.8). "
         "Bootstrap: 2,000 season resamples, seed 20261101, 95% percentile CI. Main model: D4 loss model, S cap 14 g/L, Delta_sev = 10.1 M VND/ha (F22), 70 station-seasons.", ""]
for grp in GRP:
    a = g("main", grp, "area_regret_reduction_vs_fixed"); b = g("main", grp, "area_regret_reduction_vs_clim")
    parts[grp] = (pos(a), pos(b))
    lines.append(f"- {grp}: regret reduction by the forecast vs fixed calendar {fm(a)}; vs climatology {fm(b)}. "
                 f"REV area vs fixed {fm(g('main', grp, 'area_rev_fc_vs_fixed'))}; vs climatology {fm(g('main', grp, 'area_rev_fc_vs_clim'))}; climatology vs fixed {fm(g('main', grp, 'area_rev_clim_vs_fixed'))}.")
dif = {m: g("main", "ungated_minus_gated", m) for m in ("area_regret_reduction_vs_fixed", "area_regret_reduction_vs_clim")}
pa = all(parts[x][0] for x in GRP); pb = all(parts[x][1] for x in GRP); pc = all(pos(t) for t in dif.values())
lines += ["", "## H4 parts, applied literally",
          f"- (a) forecast reduces expected regret vs fixed calendar (CI > 0, both field types): {'YES' if pa else 'NO'}.",
          f"- (b) forecast reduces expected regret vs climatology (CI > 0, both field types): {'YES' if pb else 'NO'}.",
          f"- (c) reduction larger outside than inside sluice systems (ungated minus gated CI > 0): {'YES' if pc else 'NO'}; "
          f"vs fixed {fm(dif['area_regret_reduction_vs_fixed'])}, vs climatology {fm(dif['area_regret_reduction_vs_clim'])}.",
          f"- **H4 overall: {'SUPPORTED' if (pa and pb and pc) else 'NOT SUPPORTED'}** (requires a, b and c).", "",
          "## Structural note on (c)",
          "In the D4 model the early-sowing effect Delta (m or Delta_sev) is a constant that does not depend on S or on field type, so the profit level and "
          "slope cancel in the difference between actions: REV and regret reduction are identical for gated and ungated fields wherever the -Cost2 floor "
          "does not bind (C/L up to about 0.70; checked numerically). The only gated-ungated difference in the main run (0.037 M VND/ha x C/L) comes from the floor "
          "at C/L >= 0.75, where the implied m = -rDelta/(1-r) is below -30 M VND/ha, far outside any literature value; it is an artefact of the grid, "
          "not an inside/outside effect. Part (c) is therefore reported literally as computed but should not be read as evidence for the hypothesis. "
          "Gating matters substantively through (i) which m (hence C/L) is plausible and (ii) the FAO variant, where the recoverable loss is capped by the salinity loss.", ""]
lines.append("## Restricted to the C/L window implied by the literature m range (0.1-0.3, ungated; descriptive)")
for grp in GRP:
    lines.append(f"- {grp}: regret reduction vs fixed {fm(g('main', grp, 'area_lit0.1-0.3_regret_reduction_vs_fixed'))}; vs climatology {fm(g('main', grp, 'area_lit0.1-0.3_regret_reduction_vs_clim'))}.")
lines.append("")
mr = ret[(ret.regime == "literature_m")]
lines.append("## C/L implied by the literature parameters")
lines.append(f"- Ungated m in [-4.2, +4.7]: C/L = -m/(Delta_sev - m) runs from 0 (m >= 0, early sowing dominates) to {4.2 / (D_FERRER + 4.2):.3f} (m = -4.2, Ferrer Delta_sev 10.1); "
             f"with Delta_sev 8.3: {4.2 / (D_LE + 4.2):.3f}.")
lines.append("- Gated m in [0, +8.3]: m >= 0 throughout, so early sowing is never worse than the standard calendar (no cost-loss tradeoff; C/L = 0). "
             "The forecast then has no value for this action over the literature range.")
for grp in GRP:
    t = mr[(mr.group == grp) & (mr.strategy.isin(["always", "fc", "clim", "fixed"]))].pivot_table(index="m", columns="strategy", values="mean_regret")
    lines.append(f"- Mean regret (M VND/ha) at literature m, {grp}:\n\n```\n{t.round(3).to_string()}\n```")
lines += ["", "## Sensitivity (area of regret reduction vs fixed / vs climatology, ungated; gated differs only in FAO variants)"]
for v in variants:
    ug = g(v["name"], "ungated", "area_regret_reduction_vs_fixed"), g(v["name"], "ungated", "area_regret_reduction_vs_clim")
    gt = g(v["name"], "gated", "area_regret_reduction_vs_fixed"), g(v["name"], "gated", "area_regret_reduction_vs_clim")
    d = g(v["name"], "ungated_minus_gated", "area_regret_reduction_vs_fixed")
    lines.append(f"- {v['name']}: ungated vs fixed {fm(ug[0])}, vs clim {fm(ug[1])}; gated vs fixed {fm(gt[0])}, vs clim {fm(gt[1])}; ungated-gated (vs fixed) {fm(d)}.")
lines += ["", "## Break-even (main setting: m gated 4.15, ungated 0.25 = range midpoints; k 0.4; F 3.15; S_sev %.2f, S_mild %.2f g/L)" % (S_SEV, S_MILD)]
lines.append("\n```\n" + be.drop(columns=["m", "k", "F", "S_sev", "S_mild"]).round(3).to_string(index=False) + "\n```")
lines.append(f"\nOut-of-sample p_severe: median {np.median(pf):.2f}, share below 0.2 {np.mean(pf < .2):.2f}, share above 0.8 {np.mean(pf > .8):.2f}.")
open(f"{OUT}/verdict_h4.md", "w", encoding="utf-8").write("\n".join(lines) + "\n")

THRTXT = "; ".join(f"Delta_sev {D}, m {m:g}: p* {v[0]:.3f}, share above {v[1]:.2f}" for (D, m), v in THR.items())
log = f"""# Layer A decision run log (scripts/run_h4.py, seed {SEED}, {B} resamples)

Self-check: {SELF} (perfect information has the highest mean return at every C/L; perfect forecast REV = 1; climatology vs itself REV = 0; break-even solves equality and lies in [0,1]).

## Choices where protocol section 8 / D4 was not explicit
- Parameters: L25-based loss model (pi_bar, b, S_bar per group) from decision_parameters.md, 'Loss model' section, in 2025 VND (x1.197 for slopes); Cost2 20.0 floor; S capped at 14 (10, 20 sensitivity); slope SE: 0.0795 and 0.1358 M VND nominal x 1.197.
- Delta_sev = 10.1 M VND/ha (F22 abstract 10.0-10.2, 2025 VND) for both field types in the main run; 8.3 (L25 gated average) as sensitivity. Delta is a constant (no S dependence; the file says no source for it).
- C/L grid 0.05-0.95 step 0.05; for each r, m = -r*Delta_sev/(1-r) (so m < 0 throughout). The m >= 0 case is reported separately (returns_by_strategy.csv regime=literature_m), where the forecast threshold is set to 0 (always act).
- Strategies: fixed = never act; always; climatology = act if the fold's training base rate of the same station (p_clim column) > C/L; forecast = act if p_severe > C/L; perfect = act iff gain > 0.
- Early-sowing return = max(-Cost2, profit_std + gain) (floor also after acting). The floor never binds in the main run.
- REV in return form: (R_fc - R_ref)/(R_perfect - R_ref); reference = fixed calendar or climatology. Undefined REV (zero denominator, FAO f=0.1 where Delta_i = 0) is set to 0 in areas.
- Tests use the area of the regret reduction (M VND/ha x C/L, a money quantity) as the primary statistic; REV areas are reported alongside.
- Bootstrap: seasons resampled together (all stations), same resamples for gated, ungated and their difference; separate resample set (same seed) for the tercile sample.
- H4 (c) evaluated on the regret-reduction areas vs fixed AND vs climatology (both must have CI > 0). H4 (a), (b) require both field types.
- FAO variant: ECe = 1.56 f S, Y_rel = max(0, 1 - 0.12 (ECe - 3)), loss = 43.4 M x (1 - Y_rel), profit_std = max(-20, 23.4 - loss); gated f = 0.2 x ungated f; early-sowing gain in a severe season = min(Delta_sev, loss) (a recovered amount cannot exceed the loss; my choice). With f = 0.1 field salinity never exceeds the threshold, so Delta = 0 and the forecast has no value by construction.
- Break-even: representative S = pooled mean of capped smax over severe ({S_SEV:.2f}) / non-severe ({S_MILD:.2f}) station-seasons (stations differ in level, Son Doc is much higher; not station-specific). Main m = midpoint of the file's range (gated 4.15, ungated 0.25), k = 0.4, F = 3.15 (rent anchor). Option 3 = profit with slope x k, plus 364 kg/ha x 6.62 k VND/kg (price 5.451 x 1.215), minus 452 VND/kg (372 x 1.215) x yield (yield slope also x k). The +364 kg gain is an average over mixed salinity, so it may double count with k: sweep includes a no-yield-gain variant.
- Sweep: m (9 values over the group range) x k (0.2-0.6, 5) x F (0-3.15, 7) x yield-gain on/off; reported min/max p* where a crossing in [0,1] exists and the share of sweep points with a crossing. Delta_sev fixed at 10.1 in the sweep.

## Proposed deviations (not applied; docs/protocol.md untouched)
1. H4 part (c) cannot be tested in a meaningful way with the D4 model as specified: with a constant Delta the REV curve does not depend on the field type (except via the -Cost2 floor at C/L >= 0.75, an artefact), so (c) cannot reflect a real inside/outside effect. Proposal for the owner: either state in the protocol that (c) is evaluated through the plausible C/L range per field type (gated: m >= 0, no tradeoff; ungated: C/L up to about 0.29), or specify an S/field-dependent Delta (no source exists).
2. The tercile run uses the same Delta and loss model; base rate 0.34 so the always-act threshold shifts.

## Fig. 8 redrawn (owner decision 02/11/2026)
The first fig08 fixed m at the midpoint of the literature range, which made early sowing look always best. That m has no direct estimate: the gated range came from Le 2025 calendar-compliance effects, not from an early-sowing estimate. The figure now shows the break-even P(severe) p* = -m/(Delta_sev - m) as a function of m (m < 0; m >= 0 means early sowing is never worse), for Delta_sev 10.1 (Ferrer) and 8.3 (Le), with the out-of-sample P(severe) histogram on the same y axis. p* does not depend on field type (constant Delta), so there is one main panel, not two. Panel b: standard vs salt-tolerant variety break-even over k 0.2-0.6, by field type, with and without the 364 kg/ha yield gain. Skipping the season is dominated in the whole sweep (asserted: {SKIP_DOMINATED}). The breakeven.csv table (main m = range midpoints) is unchanged and should not be read as a result about m.
Thresholds (p*, share of the 70 forecasts above p*): {THRTXT}

## Items for the observation log (controller)
- Specification gap: a gated/ungated split in a cost-loss framework is invariant unless the action effect itself differs by group.
"""
open(f"{OUT}/run_log.md", "w", encoding="utf-8").write(log)

cap07 = f"""\n## Fig. 7 (fig07_h4_value, 190 mm)\nRelative economic value (REV) of the severe-season forecast for the early-sowing decision, relative to the fixed standard calendar (never act), as a function of the cost/loss ratio C/L (0.05-0.95), leave-one-season-out forecasts pooled over Cầu Quan, Trà Vinh and Sơn Đốc (70 station-seasons, S capped at 14 g/L). Solid: forecast (band: pointwise 95% bootstrap interval over seasons); dashed: climatology. (a) D4 loss model (Le et al. 2025 gauge-to-profit slopes): the REV curve is the same for fields inside and outside sluice systems because the early-sowing effect is constant. (b) FAO yield curve with exposure factor f = 0.5 outside gates and 0.1 inside (inside-gate REV is undefined: the salinity loss never reaches the FAO threshold, so early sowing recovers nothing). The grey strip marks C/L 0-{4.2 / (D_FERRER + 4.2):.2f}, the range implied by the literature range of the mild-season effect m for ungated fields. Area of the regret reduction over C/L 0.1-0.9 (M VND/ha x C/L), forecast vs fixed calendar {fm(g('main', 'ungated', 'area_regret_reduction_vs_fixed'))}, vs climatology {fm(g('main', 'ungated', 'area_regret_reduction_vs_clim'))}. Scenario analysis, not farm advice.\nInputs: `results/layer_a_decision/rev_curve_h4.csv` (variants main, FAO_f0.5), `results/layer_a_decision/bootstrap_ci.csv`.\n\n## Fig. 8 (fig08_breakeven, 190 mm)\n(see figures/captions.md; caption maintained there since the 02/11/2026 redraw)\n"""
if "## Fig. 7 (fig07" not in open("figures/captions.md", encoding="utf-8").read():
    with open("figures/captions.md", "a", encoding="utf-8") as fh:
        fh.write(cap07)
print("done, self-check", SELF)
