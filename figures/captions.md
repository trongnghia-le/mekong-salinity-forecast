# Figure captions (core B, protocol-v1)

All figures: `scripts/make_figures.py` (run `python -I -X utf8 scripts/make_figures.py` from the repo root). PNG 300 dpi and SVG. Test seasons are 2023-24, 2024-25, 2025-26 (scope labels 2024, 2025, 2026). Bootstrap CIs: paired bootstrap over issue dates within test seasons, 2,000 resamples, percentile 95% (`results/core_b/bootstrap_ci.csv`). Main variant only.

## Fig. 1 (fig01_data_coverage, 90 mm x 1.45)
Number of bulletin issue dates available per dry season, by source: live NCHMF archive, Wayback Machine copies of NCHMF bulletins, and dekads covered only by the ODV CSV. The dashed line marks the 21 canonical issue dates per season. Seasons 2019-20 to 2022-23 (1, 10, 12, 3 dates) are training only; 2023-24 to 2025-26 (7, 14, 9 dates, all live) form the test set. The 2020-21 bar includes one Wayback bulletin (5 Jan 2021) that yields no scored row.
Inputs: `data/raw/nchmf/inventory.csv` (status = found, source), `data/processed/features.csv` (issue_date, season_label, source_file only).

## Fig. 2 (fig02_mae_by_season, 190 mm)
Mean absolute error of the dekadal maximum salinity forecast (g/L) for HGB, QR, the official NCHMF forecast, persistence and station climatology under the forward-by-season design, pooled over the test seasons (n = 732 station-dekads) and per season (n = 168, 348, 216). Points are estimates; whiskers are 95% bootstrap CIs. Pooled MAE: HGB 1.88, QR 2.44, official 1.85, persistence 1.91, climatology 2.83 g/L.
Inputs: `results/core_b/bootstrap_ci.csv` (metrics mae_model, mae_official, mae_persist, mae_clim).

## Fig. 3 (fig03_coverage_by_design, 190 mm)
Empirical coverage of the nominal 90% prediction interval for raw quantile forecasts, conformalized quantile regression (CQR) and Mondrian CQR, under forward, leave-station-out and leave-province-out designs, for HGB (left) and QR (right), pooled over the test seasons (n = 732). Whiskers are 95% bootstrap CIs; the shaded band is the H2 criterion range 0.87-0.93. Forward CQR coverage: HGB 0.923, QR 0.955; leave-station-out CQR: HGB 0.911, QR 0.944; leave-province-out CQR: HGB 0.892, QR 0.933.
Inputs: `results/core_b/bootstrap_ci.csv` (cov_raw, cov_cqr, cov_mond; designs forward, loso, lopo).

## Fig. 4 (fig04_reliability_4gL, 190 mm)
Reliability diagram for the probability that the dekadal maximum salinity is at least 4 g/L, forward design, pooled test seasons (n = 732), for HGB (left) and QR (right), in ten equal-width probability bins. Upper panels: mean forecast probability against observed frequency per bin (open markers: bins with n < 20), the diagonal, and the base rate (0.70). Lower panels: number of forecasts per bin (log-type scale). The two extreme bins hold 556 (HGB) and 491 (QR) of the 732 forecasts.
Input: `results/core_b/reliability.csv` (threshold 4, forward, main, pooled); base rate from `results/core_b/bootstrap_ci.csv` (base_rate_4).

## Fig. 5 (fig05_economic_value, 90 mm x 1.6)
Relative economic value of 4 g/L exceedance forecasts as a function of the cost/loss ratio C/L (0.05-0.95), forward design, pooled test seasons, for HGB, QR, the official forecast, persistence and climatology. The shaded interval C/L 0.1-0.9 is the window used for the H3 area criterion; values below -0.6 are clipped. Area under the curve over 0.1-0.9: HGB 0.557, QR 0.516, official 0.428, persistence 0.479, climatology 0.150. Differences from the official area: HGB 0.129 [0.052, 0.211], QR 0.088 [0.009, 0.173] (95% bootstrap CIs; see Fig. 2 for the sample). No CI is drawn on the curves.
Inputs: `results/core_b/rev_curve.csv` (forward, main); areas from `results/core_b/bootstrap_ci.csv` (rev_area_*).

## Fig. 6 (fig06_extrapolation_2024, 190 mm)
(a) Oceanic Nino Index (ONI) at each issue date, by season; the shaded band is the range over the training seasons 2019-20 to 2022-23 (-1.11 to 0.66 deg C), and the 2023-24 issue dates lie at 1.53-1.99 deg C. (b) Forward-design MAE (g/L) of HGB and QR per test season with 95% bootstrap CIs: 2023-24 HGB 2.11 [1.82, 2.48], QR 4.58 [4.05, 5.13]; 2024-25 HGB 1.64 [1.37, 1.95], QR 1.60 [1.35, 1.86]; 2025-26 HGB 2.10 [1.70, 2.56], QR 2.14 [1.72, 2.69]. Horizontal jitter in (a) is for visibility only.
Inputs: `data/processed/features.csv` (issue_date, season_label, oni only; ONI is not NCHMF data), `results/core_b/bootstrap_ci.csv` (mae_model).

## Fig. 7 (fig07_h4_value, 90 mm)
Relative economic value (REV) of the severe-season forecast for the early-sowing decision, relative to the fixed standard calendar (never act), as a function of the cost/loss ratio C/L (0.05-0.95), leave-one-season-out forecasts pooled over Cầu Quan, Trà Vinh and Sơn Đốc (70 station-seasons, S capped at 14 g/L, severe-season effect Delta_sev = 10.1 M VND/ha). Solid blue: forecast; dashed orange: climatology; bands: pointwise 95% bootstrap intervals over seasons (2,000 resamples). Main setting: D4 loss model (Le et al. 2025 gauge-to-profit slope). The FAO yield-curve sensitivity run (exposure factor 0.5) gives the same curve up to C/L ~0.7, because with a constant early-sowing effect relative economic value does not depend on the loss model unless the profit floor binds. Scenario analysis, not farm advice.
Inputs: `results/layer_a_decision/rev_curve_h4.csv` (variants main, FAO_f0.5), `results/layer_a_decision/bootstrap_ci.csv`.

## Fig. 8 (fig08_breakeven, 190 mm)
Break-even thresholds for the layer-A crop options (scenario analysis; the mild-season net effect of early sowing, m, has no direct estimate, so the figure shows thresholds as a function of it rather than fixing it). (a) Break-even probability p* of a severe season above which early sowing (option 2) has a higher expected net return than the standard calendar (option 1), p* = -m/(Delta_sev - m) for m < 0, against m (M VND/ha, 2025 VND), for a severe-season effect Delta_sev of 10.1 (Ferrer et al.; solid) and 8.3 (Le et al.; dashed) M VND/ha. For m >= 0 (grey) early sowing is never worse at any probability. Right of the curves: distribution of the out-of-sample P(severe) (n = 70, leave-one-season-out, same y axis), showing how often a forecast would exceed a given p*. (b) Break-even probability between standard rice (option 1) and the salt-tolerant variety (option 3) against the variety's loss scaling k (0.2-0.6), with and without the +364 kg/ha yield gain (price discount 458 VND/kg; fixed cost 3.15 M VND/ha). Values below 0 or above 1 (grey) mean one option is better at any probability. Skipping the season (option 6) is dominated by another option in every setting of m, k, fixed cost and yield gain tested. No range of m is shown as an estimate. Not farm advice.
Inputs: `results/layer_a_decision/breakeven.csv`, `results/layer_a_decision/run_log.md` (threshold table), `results/layer_a/forecasts_loso.csv`.
