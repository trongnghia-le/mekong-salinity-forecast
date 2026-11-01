"""Paper figures for core B. Run: python -I -X utf8 scripts/make_figures.py  (from repo root).

Only aggregated scores, data-availability counts and the ONI predictor are plotted;
no per-row NCHMF observation or forecast value is drawn.
"""
import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
os.makedirs("figures", exist_ok=True)
MM = 1 / 25.4
W1, W2 = 90 * MM, 190 * MM

plt.rcParams.update({
    "font.family": "sans-serif", "font.sans-serif": ["Arial", "DejaVu Sans"],
    "font.size": 7.5, "axes.labelsize": 7.5, "axes.titlesize": 8, "legend.fontsize": 7,
    "xtick.labelsize": 7, "ytick.labelsize": 7, "axes.linewidth": 0.6,
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.grid": True, "grid.color": "#e3e2de", "grid.linewidth": 0.5, "axes.axisbelow": True,
    "svg.fonttype": "none", "figure.facecolor": "white",
})
INK, MUTED = "#0b0b0b", "#52514e"
# fixed per-method colour + marker (validated categorical order; climatology = neutral reference)
METH = {  # key: (label, colour, marker)
    "hgb": ("HGB", "#2a78d6", "o"), "qr": ("QR", "#eb6834", "s"),
    "official": ("Official NCHMF", "#6250d6", "^"), "persist": ("Persistence", "#008300", "D"),
    "clim": ("Climatology", "#6b6a66", "v"),
}


def save(fig, name):
    for ext in ("png", "svg"):
        fig.savefig(f"figures/{name}.{ext}", dpi=300, bbox_inches="tight")
    plt.close(fig)


def panel(ax, s):
    ax.text(-0.02, 1.04, s, transform=ax.transAxes, fontweight="bold", fontsize=9, ha="right", va="bottom")


ci = pd.read_csv("results/core_b/bootstrap_ci.csv")
ci = ci[ci.variant == "main"]
feat = pd.read_csv("data/processed/features.csv", usecols=["issue_date", "season_label", "obs_source", "source_file", "oni"])
inv = pd.read_csv("data/raw/nchmf/inventory.csv")
SEAS = {"2024": "2023-24", "2025": "2024-25", "2026": "2025-26"}


def get(design, model, scope, metric):
    r = ci[(ci.design == design) & (ci.model == model) & (ci.scope == scope) & (ci.metric == metric)].iloc[0]
    return r.estimate, r.ci_lo, r.ci_hi


# ---------------- fig01 data coverage ----------------
def fig01():
    fo = inv[inv.status == "found"][["issue_date", "season", "source"]].rename(columns={"source": "src"})
    d = {}  # issue_date -> (season, category)
    for r in fo.itertuples():
        d[r.issue_date] = (r.season, "Live NCHMF" if r.src == "live" else "Wayback NCHMF")
    for r in feat.drop_duplicates("issue_date").itertuples():
        if r.issue_date in d:
            continue
        cat = "Wayback NCHMF" if "wayback" in str(r.source_file) else "ODV only"
        d[r.issue_date] = (r.season_label, cat)
    df = pd.DataFrame([(k, *v) for k, v in d.items()], columns=["date", "season", "cat"])
    seasons = ["2019-20", "2020-21", "2021-22", "2022-23", "2023-24", "2024-25", "2025-26"]
    cats = [("Live NCHMF", "#2a78d6", None), ("Wayback NCHMF", "#eb6834", None), ("ODV only", "#6250d6", "//")]
    cnt = df.groupby(["season", "cat"]).size().unstack(fill_value=0).reindex(seasons).fillna(0)
    fig, ax = plt.subplots(figsize=(W1 * 1.45, 62 * MM * 1.2))
    left = np.zeros(len(seasons))
    y = np.arange(len(seasons))[::-1]
    for c, col, hatch in cats:
        v = cnt[c].reindex(seasons).fillna(0).values if c in cnt else np.zeros(len(seasons))
        ax.barh(y, v, left=left, color=col, hatch=hatch, edgecolor="white", linewidth=0.8, height=0.62, label=c)
        left += v
    ax.axvline(21, color=INK, ls="--", lw=0.8)
    ax.text(21.3, y[0] + 0.55, "21 canonical\nissue dates", fontsize=6.5, va="center", color=INK)
    ax.axhspan(y[4] + 0.5, y[-1] - 0.5, color="#e8e7e2", zorder=0)
    for yi, tot in zip(y, left):
        ax.text(tot + 0.4, yi, f"{int(tot)}", va="center", fontsize=7, color=INK)
    ax.text(26.8, y[5], "test", va="center", ha="right", fontweight="bold", fontsize=7.5)
    ax.text(26.8, y[2], "training only", va="center", ha="right", fontweight="bold", fontsize=7.5, color=MUTED)
    ax.set_yticks(y); ax.set_yticklabels(seasons)
    ax.set_xlim(0, 27); ax.set_xlabel("Issue dates available per dry season (n)")
    ax.grid(axis="y", visible=False)
    ax.legend(ncol=3, frameon=False, loc="lower center", bbox_to_anchor=(0.45, 1.0), columnspacing=1, handletextpad=0.4)
    save(fig, "fig01_data_coverage")
    return df.groupby("season").size().reindex(seasons).to_dict(), cnt


# ---------------- fig02 MAE by season ----------------
def fig02():
    scopes = [("pooled", "Pooled\n2024-26"), ("2024", "2023-24"), ("2025", "2024-25"), ("2026", "2025-26")]
    order = [("hgb", "mae_model"), ("qr", "mae_model"), ("official", "mae_official"),
             ("persist", "mae_persist"), ("clim", "mae_clim")]
    fig, ax = plt.subplots(figsize=(W2, 70 * MM))
    off = np.linspace(-0.32, 0.32, 5)
    for k, (m, metric) in enumerate(order):
        lab, col, mk = METH[m]
        xs, es, lo, hi = [], [], [], []
        for i, (sc, _) in enumerate(scopes):
            e, l, h = get("forward", "qr" if m == "qr" else "hgb", sc, metric)
            xs.append(i + off[k]); es.append(e); lo.append(e - l); hi.append(h - e)
        ax.errorbar(xs, es, yerr=[lo, hi], fmt=mk, color=col, ms=4.5, mec="white", mew=0.5, elinewidth=1.1,
                    capsize=2, label=lab, zorder=3)
    ax.axvline(0.5, color="#bdbcb6", lw=0.8)
    ax.set_xticks(range(4)); ax.set_xticklabels([s[1] for s in scopes])
    ax.set_ylabel("MAE of dekadal maximum salinity (g/L)"); ax.set_ylim(0, None)
    ax.grid(axis="x", visible=False)
    ax.legend(ncol=5, frameon=False, loc="upper center", bbox_to_anchor=(0.5, 1.12), columnspacing=1.2, handletextpad=0.3)
    save(fig, "fig02_mae_by_season")


# ---------------- fig03 coverage by design ----------------
def fig03():
    designs = [("forward", "Forward"), ("loso", "Leave-station-out"), ("lopo", "Leave-province-out")]
    kinds = [("cov_raw", "Raw quantiles", "#c9c8c2", None), ("cov_cqr", "CQR", None, None), ("cov_mond", "Mondrian CQR", None, "//")]
    fig, axs = plt.subplots(1, 2, figsize=(W2, 66 * MM), sharey=True)
    for ax, mod, t in zip(axs, ["hgb", "qr"], ["HGB", "QR"]):
        ax.axhspan(0.87, 0.93, color="#dfe9f7", zorder=0)
        ax.axhline(0.90, color=INK, lw=0.8, ls="--", zorder=1)
        for j, (k, lab, col, hatch) in enumerate(kinds):
            c = col or METH[mod][1]
            for i, (d, _) in enumerate(designs):
                e, l, h = get(d, mod, "pooled", k)
                x = i + (j - 1) * 0.27
                ax.bar(x, e, 0.24, color=c, hatch=hatch, edgecolor="white" if hatch is None else METH[mod][1],
                       linewidth=0.6, zorder=2, label=lab if i == 0 else None, alpha=1 if k != "cov_cqr" else 0.8)
                ax.errorbar(x, e, yerr=[[e - l], [h - e]], color=INK, lw=0.9, capsize=1.8, zorder=3)
                ax.text(x, h + 0.008, f"{e:.2f}", ha="center", fontsize=6.3)
        ax.set_xticks(range(3)); ax.set_xticklabels([d[1] for d in designs])
        ax.set_title(t, loc="left"); ax.set_ylim(0.6, 1.02); ax.grid(axis="x", visible=False)
    axs[0].set_ylabel("Empirical coverage of the 90% interval")
    h, l = axs[0].get_legend_handles_labels()
    from matplotlib.patches import Patch
    from matplotlib.lines import Line2D
    h += [Patch(color="#dfe9f7"), Line2D([], [], color=INK, ls="--", lw=0.8)]
    l += ["H2 band 0.87-0.93", "Nominal 0.90"]
    fig.legend(h, l, ncol=5, frameon=False, loc="upper center", bbox_to_anchor=(0.5, 1.05), columnspacing=1.2)
    save(fig, "fig03_coverage_by_design")


# ---------------- fig04 reliability ----------------
def fig04():
    r = pd.read_csv("results/core_b/reliability.csv")
    r = r[(r.variant == "main") & (r.design == "forward") & (r.scope == "pooled") & (r.threshold == 4)]
    base = get("forward", "hgb", "pooled", "base_rate_4")[0]
    fig, axs = plt.subplots(2, 2, figsize=(W2, 96 * MM), gridspec_kw={"height_ratios": [3, 1], "hspace": 0.12}, sharex="col")
    for j, (mod, t) in enumerate([("hgb", "HGB"), ("qr", "QR")]):
        d = r[r.model == mod].reset_index(drop=True)
        ax, hb = axs[0, j], axs[1, j]
        col = METH[mod][1]
        ax.plot([0, 1], [0, 1], color=MUTED, lw=0.8, label="Perfect reliability")
        ax.axhline(base, color=INK, lw=0.8, ls=":", label=f"Base rate {base:.2f}")
        ok = d.n > 0
        ax.plot(d.mean_prob[ok], d.obs_freq[ok], "-", color=col, lw=1.2, zorder=2)
        small = ok & (d.n < 20)
        ax.plot(d.mean_prob[ok & ~small], d.obs_freq[ok & ~small], METH[mod][2], color=col, ms=5, mec="white", mew=0.5, zorder=3, label="Bin (n >= 20)")
        ax.plot(d.mean_prob[small], d.obs_freq[small], METH[mod][2], mfc="white", mec=col, ms=5, mew=1, zorder=3, label="Bin (n < 20)")
        ax.set_xlim(0, 1); ax.set_ylim(0, 1.02); ax.set_title(t, loc="left")
        ax.set_ylabel("Observed frequency" if j == 0 else "")
        if j == 0:
            ax.legend(frameon=False, loc="upper left")
        centers = np.arange(10) * 0.1 + 0.05
        hb.bar(centers, d.n, 0.085, color=col)
        for c, n in zip(centers, d.n):
            hb.text(c, n + 8, str(n), ha="center", fontsize=6)
        hb.set_yscale("symlog", linthresh=10); hb.set_ylim(0, 2000)
        hb.set_yticks([0, 10, 100, 1000]); hb.set_yticklabels(["0", "10", "100", "1000"])
        hb.set_xlabel("Forecast probability of Smax >= 4 g/L"); hb.set_ylabel("Count" if j == 0 else "")
        hb.grid(axis="x", visible=False)
    save(fig, "fig04_reliability_4gL")


# ---------------- fig05 economic value ----------------
def fig05():
    v = pd.read_csv("results/core_b/rev_curve.csv")
    v = v[(v.variant == "main") & (v.design == "forward")]
    g = v[v.model == "hgb"].sort_values("cost_loss")
    q = v[v.model == "qr"].sort_values("cost_loss")
    fig, ax = plt.subplots(figsize=(W1 * 1.6, 72 * MM))
    ax.axvspan(0.1, 0.9, color="#eeede9", zorder=0)
    ax.text(0.5, 1.0, "C/L 0.1-0.9 (H3 window)", ha="center", va="top", fontsize=6.5, color=MUTED,
            transform=ax.get_xaxis_transform())
    ax.axhline(0, color=INK, lw=0.7)
    series = [("hgb", g.cost_loss, g.V_model, "-"), ("qr", q.cost_loss, q.V_model, "-"),
              ("official", g.cost_loss, g.V_official, "-"), ("persist", g.cost_loss, g.V_persist, "-"),
              ("clim", g.cost_loss, g.V_clim, "--")]
    for m, x, y, ls in series:
        lab, col, mk = METH[m]
        ax.plot(x, y, ls, color=col, lw=1.4, marker=mk, markevery=6, ms=4, mec="white", mew=0.4, label=lab)
    ax.set_ylim(-0.6, 1.0); ax.set_xlim(0.05, 0.95)
    ax.set_xlabel("Cost/loss ratio C/L"); ax.set_ylabel("Relative economic value, 4 g/L")
    ax.legend(frameon=False, ncol=2, loc="lower center")
    ax.text(0.95, -0.57, "Values below -0.6 clipped", fontsize=6, ha="right", color=MUTED)
    save(fig, "fig05_economic_value")


# ---------------- fig06 extrapolation ----------------
def fig06():
    f = feat.drop_duplicates("issue_date")[["issue_date", "season_label", "oni"]].sort_values("issue_date")
    seasons = ["2019-20", "2020-21", "2021-22", "2022-23", "2023-24", "2024-25", "2025-26"]
    test = {"2023-24", "2024-25", "2025-26"}
    fig, axs = plt.subplots(1, 2, figsize=(W2, 70 * MM), gridspec_kw={"width_ratios": [1.25, 1], "wspace": 0.3})
    ax = axs[0]
    tr = f[~f.season_label.isin(test)].oni
    ax.axhspan(tr.min(), tr.max(), color="#dfe9f7", zorder=0)
    ax.text(len(seasons) - 0.5, tr.max() + 0.05, "range in training seasons", ha="right", va="bottom", fontsize=6.3, color=MUTED)
    rng = np.random.default_rng(0)
    for i, s in enumerate(seasons):
        o = f[f.season_label == s].oni.values
        x = i + rng.uniform(-0.12, 0.12, len(o))
        col = "#eb6834" if s in test else "#2a78d6"
        ax.plot(x, o, "o" if s not in test else "s", color=col, ms=4.2, mec="white", mew=0.4, zorder=3,
                label=("Test season (issue date)" if s == "2023-24" else "Training season (issue date)" if s == "2019-20" else None))
    ax.axvline(3.5, color="#bdbcb6", lw=0.8)
    ax.set_xticks(range(len(seasons))); ax.set_xticklabels(seasons, rotation=40, ha="right")
    ax.set_ylabel("ONI at issue date (deg C)"); ax.grid(axis="x", visible=False)
    ax.legend(frameon=False, loc="upper left")
    panel(ax, "a")
    ax = axs[1]
    sc = [("2024", "2023-24"), ("2025", "2024-25"), ("2026", "2025-26")]
    for k, m in enumerate(["hgb", "qr"]):
        lab, col, mk = METH[m]
        es, lo, hi = zip(*[get("forward", m, s, "mae_model") for s, _ in sc])
        es, lo, hi = map(np.array, (es, lo, hi))
        x = np.arange(3) + (k - 0.5) * 0.25
        ax.errorbar(x, es, yerr=[es - lo, hi - es], fmt=mk, color=col, ms=5, mec="white", mew=0.5, capsize=2, label=lab)
    ax.set_xticks(range(3)); ax.set_xticklabels([s[1] for s in sc])
    ax.set_ylabel("MAE (g/L)"); ax.set_ylim(0, None); ax.grid(axis="x", visible=False)
    ax.legend(frameon=False, loc="upper right")
    panel(ax, "b")
    save(fig, "fig06_extrapolation_2024")
    return tr.min(), tr.max(), f[f.season_label == "2023-24"].oni.agg(["min", "max"]).tolist()


if __name__ == "__main__":
    print(fig01()); fig02(); fig03(); fig04(); fig05(); print(fig06())
