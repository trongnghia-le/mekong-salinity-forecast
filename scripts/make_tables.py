"""Write the manuscript tables (LaTeX, booktabs) from results/ CSVs into manuscript/tables/.

Aggregated scores only: no per-row NCHMF value (observation or official forecast) enters any table.
Run from the repo root: python -I -X utf8 scripts/make_tables.py
"""
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / "results"
OUT = ROOT / "manuscript" / "tables"


def ci(est, lo, hi, nd=3):
    return f"{est:.{nd}f} [{lo:.{nd}f}, {hi:.{nd}f}]".replace("-", "$-$")


def write(name, caption, label, colspec, header, rows, note=""):
    body = "\n".join(" & ".join(r) + r" \\" for r in rows)
    note_tex = f"\n\\par\\smallskip\\footnotesize {note}" if note else ""
    tex = (
        "\\begin{table}[htbp]\n\\centering\\small\n"
        f"\\caption{{{caption}}}\\label{{{label}}}\n"
        "\\begin{adjustbox}{max width=\\textwidth}\n"
        f"\\begin{{tabular}}{{{colspec}}}\n\\toprule\n{header} \\\\\n\\midrule\n{body}\n\\bottomrule\n"
        f"\\end{{tabular}}\n\\end{{adjustbox}}{note_tex}\n\\end{{table}}\n"
    )
    (OUT / name).write_text(tex, encoding="utf-8")


# ---------- core B ----------
cb = pd.read_csv(RES / "core_b" / "bootstrap_ci.csv")


def g(design, model, scope, metric, variant="main"):
    r = cb[(cb.design == design) & (cb.variant == variant) & (cb.model == model)
           & (cb.scope == scope) & (cb.metric == metric)]
    assert len(r) == 1, (design, model, scope, metric)
    return r.iloc[0]


def gci(design, model, scope, metric, nd=3):
    r = g(design, model, scope, metric)
    return ci(r.estimate, r.ci_lo, r.ci_hi, nd)


def core_verdicts():
    crit = [
        ("H1", "MAE, model $-$ persistence", "forward", "mae_diff_persist", "CI $<0$"),
        ("H1", "MAE, model $-$ climatology", "forward", "mae_diff_clim", "CI $<0$"),
        ("H1", "MAE, model $-$ official", "forward", "mae_diff_official", "CI $<0$"),
        ("H1", "Brier(4), model $-$ persistence", "forward", "brier_diff_persist_4", "CI $<0$"),
        ("H1", "Brier(4), model $-$ climatology", "forward", "brier_diff_clim_4", "CI $<0$"),
        ("H2a", "CQR 90\\% coverage, forward", "forward", "cov_cqr", "in [0.87, 0.93]"),
        ("H2b", "Plain CQR coverage, leave-station-out", "loso", "cov_cqr", "$<0.87$"),
        ("H2b", "Mondrian CQR coverage, leave-station-out", "loso", "cov_mond", "$\\ge 0.87$"),
        ("H2b", "Plain CQR coverage, leave-province-out", "lopo", "cov_cqr", "$<0.87$"),
        ("H2b", "Mondrian CQR coverage, leave-province-out", "lopo", "cov_mond", "$\\ge 0.87$"),
        ("H3", "REV area (C/L 0.1--0.9), model $-$ official", "forward", "rev_area_diff_official", "CI $>0$"),
    ]
    rows = [[h, c, req, gci(d, "hgb", "pooled", m), gci(d, "qr", "pooled", m)] for h, c, d, m, req in crit]
    rows.append(["", "\\textit{Verdicts}", "", "H1 no; H2a yes; H2b no; H3 yes", "H1 no; H2a no; H2b no; H3 yes"])
    write(
        "tab_core_verdicts.tex",
        "Core-B criteria of the frozen protocol (protocol-v1), test seasons 2024--2026 pooled (27 issue dates, "
        "732 station-dekads). Estimates with paired-bootstrap 95\\% CIs (issue dates resampled within seasons, "
        "2,000 resamples). MAE in g/L; Brier and coverage unitless. HGB: gradient-boosted quantile regression; "
        "QR: linear quantile regression.",
        "tab:verdicts", "@{}lp{4.6cm}lll@{}",
        "Hyp. & Criterion & Required & HGB & QR", rows,
        "H2a and H2b coverage criteria are applied to the point estimate. H2b requires plain coverage below 0.87 "
        "and Mondrian coverage at or above 0.87 in both transfer designs.")


def core_seasons():
    rows = []
    for s in ["2024", "2025", "2026", "pooled"]:
        n = int(g("forward", "hgb", s, "n").estimate)
        br = g("forward", "hgb", s, "base_rate_4").estimate
        rows.append([
            s, str(n), f"{br:.2f}",
            gci("forward", "hgb", s, "mae_model", 2),
            f"{g('forward', 'qr', s, 'mae_model').estimate:.2f}",
            gci("forward", "hgb", s, "mae_official", 2),
            f"{g('forward', 'hgb', s, 'mae_persist').estimate:.2f}",
            f"{g('forward', 'hgb', s, 'mae_clim').estimate:.2f}",
            f"{g('forward', 'hgb', s, 'cov_cqr').estimate:.3f}",
            f"{g('forward', 'hgb', s, 'rev_area_model').estimate:.3f}",
            f"{g('forward', 'hgb', s, 'rev_area_official').estimate:.3f}",
        ])
    write(
        "tab_core_seasons.tex",
        "Forward-by-season scores per test season (season = January year). MAE in g/L with 95\\% bootstrap CIs "
        "for HGB and the official forecast; CQR = coverage of the HGB conformalized 90\\% interval; REV = area "
        "under the relative-economic-value curve at 4 g/L over C/L 0.1--0.9.",
        "tab:seasons", "@{}lrrllllllll@{}",
        "Season & $n$ & $\\bar o_4$ & MAE HGB & QR & MAE official & Pers. & Clim. & CQR & REV HGB & REV off.",
        rows,
        "$n$: station-dekads; $\\bar o_4$: base rate of $S_{\\max}>4$ g/L. Rounded to 2 (MAE) or 3 decimals.")


# ---------- layer A ----------
def layer_a():
    met = pd.read_csv(RES / "layer_a" / "metrics.csv")
    bs = pd.read_csv(RES / "layer_a" / "bootstrap_ci.csv")
    names = {"main_median_TanChau": "Main (median; Tân Châu Q)",
             "sens_tercile_TanChau": "Upper tercile; Tân Châu Q",
             "sens_median_GloFAS": "Median; GloFAS Q",
             "sens_tercile_GloFAS": "Upper tercile; GloFAS Q"}
    rows = []
    for v, label in names.items():
        for sc in ["pooled", "Cầu Quan", "Sơn Đốc", "Trà Vinh"]:
            if v != "main_median_TanChau" and sc != "pooled":
                continue
            m = met[(met.variant == v) & (met.scope == sc)].iloc[0]
            b = bs[(bs.variant == v) & (bs.scope == sc) & (bs.metric == "bss")].iloc[0]
            a = bs[(bs.variant == v) & (bs.scope == sc) & (bs.metric == "auc")].iloc[0]
            rows.append([label if sc == "pooled" else "", sc, str(int(m.n)), f"{m.base_rate:.2f}",
                         ci(b.est, b.lo, b.hi), f"{b.share_bss_pos:.3f}", ci(a.est, a.lo, a.hi)])
    write(
        "tab_layer_a.tex",
        "Layer A: 1 November forecast of a severe season (seasonal maximum above the station median), "
        "leave-one-season-out. Brier skill score (BSS) against station climatology and ROC AUC with 95\\% "
        "bootstrap CIs over seasons (2,000 resamples).",
        "tab:layera", "@{}llrrlrl@{}",
        "Variant & Scope & $n$ & Base rate & BSS & $P(\\mathrm{BSS}>0)$ & AUC", rows,
        "$n$: station-seasons. $P(\\mathrm{BSS}>0)$: share of bootstrap resamples with positive BSS.")


def h4():
    d = pd.read_csv(RES / "layer_a_decision" / "bootstrap_ci.csv")

    def c(v, grp, met):
        r = d[(d.variant == v) & (d.group == grp) & (d.metric == met)].iloc[0]
        return ci(r.estimate, r.ci_lo, r.ci_hi)

    # Main setting only (D4 loss model, ungated slope); one row per comparison. No field-type rows (owner, 02/11/2026).
    rows = [
        ["Forecast vs fixed calendar", c("main", "ungated", "area_regret_reduction_vs_fixed"),
         c("main", "ungated", "area_rev_fc_vs_fixed")],
        ["Forecast vs climatology", c("main", "ungated", "area_regret_reduction_vs_clim"),
         c("main", "ungated", "area_rev_fc_vs_clim")],
        ["Climatology vs fixed calendar", "--", c("main", "ungated", "area_rev_clim_vs_fixed")],
    ]
    write(
        "tab_h4.tex",
        "H4: value of the severe-season forecast for the early-sowing decision (scenario analysis, not farm "
        "advice), main setting. Areas over C/L 0.1--0.9 of the regret reduction (M VND ha$^{-1}$ $\\times$ C/L, "
        "2025 VND) and of the relative economic value (REV). 95\\% CIs from 2,000 season resamples; "
        "70 station-seasons.",
        "tab:h4", "@{}lll@{}",
        "Comparison & Regret reduction & REV area", rows,
        "Main setting: loss model D4 with the profit slope of \\citet{le2025size} for fields outside sluice "
        "systems, salinity capped at 14 g/L, $\\Delta_{\\mathrm{sev}}=10.1$ M VND ha$^{-1}$. H4 (a) and (b) "
        "require the regret-reduction CI above 0.")


def data_sources():
    rows = [
        ["NCHMF dekadal salinity bulletins (Tables 1--2)", "50 PDFs: 20 May 2020; Jan 2021--May 2026",
         "Target $S_{\\max}$; official forecast", "No reuse terms; values not redistributed"],
        ["Open Development Vietnam CSV", "Jan--Mar 2021 dekads", "Training only", "CC BY-SA 4.0"],
        ["GloFAS v4 via Open-Meteo Flood API (Kratie)", "1997--2026, daily", "Discharge predictors",
         "CC BY 4.0"],
        ["NOAA CPC Oceanic Ni\\~no Index", "1950--2026, monthly", "ENSO predictor", "Public domain"],
        ["Astronomical tide (lunar phase, perigee)", "computed", "Tide predictors", "--"],
        ["GFZ: Sơn Đốc salinity, Tân Châu discharge", "1996--2016", "Layer A target and predictor", "CC BY 4.0"],
        ["Mendeley: Cầu Quan, Trà Vinh annual maxima", "1990--2016", "Layer A target", "CC BY 4.0"],
        ["PCTT daily reports (4 stations)", "Feb--May 2020", "Exploratory extreme-season check",
         "No terms found; scores only"],
        ["Published farm economics (Le et al.\\ 2025; Ferrer et al.\\ 2022; Mills et al.\\ 2022)",
         "2017--2020 seasons", "Layer A loss model", "Cited parameters"],
    ]
    write(
        "tab_data.tex", "Data sources, periods, use and licences.", "tab:data", "@{}p{4.6cm}p{2.9cm}p{3.2cm}p{3.2cm}@{}",
        "Source & Period & Use & Licence / terms", rows)


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    core_verdicts(); core_seasons(); layer_a(); h4(); data_sources()
    # self-check: tables hold no per-row NCHMF fields and carry the frozen headline numbers
    txt = "".join(p.read_text(encoding="utf-8") for p in OUT.glob("tab_*.tex"))
    for must in ["0.923 [0.898, 0.949]", "0.129 [0.052, 0.211]", "-0.022 [-0.129, 0.084]",
                 "0.253 [-0.023, 0.490]", "1.564 [0.068, 3.064]"]:
        assert must.replace("-", "$-$") in txt, must
    assert "ungated_minus_gated" not in txt and "minus" not in txt.lower().replace("$-$", "")
    print("wrote", sorted(p.name for p in OUT.glob("tab_*.tex")))
