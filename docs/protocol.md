# Protocol — Paper 4: calibrated dekadal salinity forecasts, Vietnamese Mekong Delta

Status: **FROZEN v1 (01/11/2026), approved by the owner; git tag `protocol-v1`.** Frozen before any model was
scored on a test season. After the freeze, changes go only into "Deviations after freeze" (end of file), dated, with
the reason. Plan of record: docs/ke_hoach_trien_khai.md; data state: docs/paper_notes.md.

## 1. Questions and hypotheses

Core B forecasts the next dekad's maximum salinity Smax (g/L) at each station, issued on NCHMF bulletin dates
(10th, 20th, last day of month), horizon h = 1 dekad (the official forecast's horizon).

- **H1 (accuracy).** A pooled multi-station model beats (a) persistence, (b) station-by-dekad climatology and
  (c) the official NCHMF forecast (Bảng 2) on MAE of Smax and on the Brier score at 4 g/L, in forward-by-season
  testing. Supported if the paired-bootstrap 95% CI of the MAE difference (model minus benchmark) lies below 0 for
  each benchmark, and likewise for Brier against (a) and (b). Against (c), Brier is not defined (single value); the
  official forecast is compared on MAE and on hit rate / false-alarm rate / Peirce skill score at 4 g/L, with the
  model's probability turned into a yes/no forecast at the threshold chosen on calibration data only.
- **H2 (coverage).** Conformalized 90% intervals cover 90 ± 3 percentage points in forward-by-season testing.
  Under leave-station-out and leave-province-out, coverage of plain split/cross-conformal falls below 87%, and
  Mondrian conformal by distance-to-mouth group (0-15, 15-40, >40 km; inland canals as their own group if n allows)
  restores >= 87%. Each part is reported separately (support for one part does not imply the other).
- **H3 (value).** The calibrated exceedance probability at 4 g/L has higher relative economic value (Richardson 2000)
  than the official deterministic forecast over C/L in [0.1, 0.9]. Supported if the bootstrap 95% CI of the
  difference in area under the value curve over that range is above 0.
- **H4 (sowing, layer A).** Sowing by the 1 November seasonal forecast reduces expected regret against a fixed
  calendar; the reduction is larger outside than inside sluice systems. Details in section 8; to be completed
  before the freeze.

Unsupported hypotheses are reported as such, with the same prominence.

## 2. Data (as of 01/11/2026; see paper_notes.md for provenance)

- **Target and official forecast:** NCHMF bulletins, 50 PDFs (Jan 2021 - May 2026 plus 20/05/2020), parsed by
  scripts/parse_nchmf.py into data/processed/nchmf_obs.csv (Bảng 1) and nchmf_fc.csv (Bảng 2). Values as printed.
- **Usable forecast cases:** an issue date is a case when the bulletin for the next dekad also exists (its Bảng 1 is
  the verifying observation). From bulletins alone, 40 issue dates: season (January year) 2021: 2, 2022: 9,
  2023: 2, 2024: 6, 2025: 13, 2026: 8; about 27 stations each. ODV dekads add 6 training-only dates in 2021.
- **Extra observations (no forecast cases):** ODV CSV dekads Jan-Mar 2021 (copy of the bulletins; 261/262 equal);
  Bảng 1 comparison-column monthly maxima (nchmf_ref_monthly.csv; flag `ok` only); PCTT daily reports 2020 and the
  2016 same-date column (pctt_dekadal.csv; unknown daily statistic, lower bounds).
- **Predictors:** scripts/build_features.py (section 4) -> data/processed/features.csv (1,478 station-dekad rows,
  1,223 with a target; self-check passes). Issue dates with a target per season: 2021: 8 (incl. ODV dekads),
  2022: 9, 2023: 2, 2024: 6, 2025: 13, 2026: 8.
- **ODV rows** (153 rows, 127 with a target, `obs_source = odv`, no official forecast) are training-only. Some 2021
  ODV dekads repeat the previous dekad exactly (possible copy-down); a sensitivity run drops all ODV rows.
- **Station statics** (km from mouth, river, inland flag) are the per-station mode over bulletins, because printed
  columns vary between issues (2022 columns shifted; Cát Lái printed km 20 in 2023 and km 58 from 2024 — open
  question whether the site or the reference point changed).
- **Excluded:** the 5-day bulletin of 05/01/2021 (not a dekad); An Định forecast "202" (20/04/2026, printing error);
  any value > 45 g/L. Sông Đốc 42 g/L (20/05/2020) is kept but checked in a sensitivity run without it.
- **Stations:** the 28 canonical NCHMF stations. Cầu Nổi, Xẻo Rô, Mỹ Tho, Đồng Tâm, Cà Mau (2020-2022 lists only)
  enter training as extra stations but are not test stations. "Ngã 3 Cát Lái" (2022) = Cầu Nổi, not Cát Lái.
- **Provinces:** grouping uses pre-merger provinces (finer; 2021-2025 bulletins print them); crosswalk to the 2025
  provinces in data/meta/ (pending, two independent passes compared).
- **Season label:** the January year (season 2024 = Dec 2023 - Jun 2024).

## 3. Forecast-time information rule

Only information available on the issue date t may enter a predictor:
- Smax of the dekad ending at t (Bảng 1 of the same bulletin) and earlier dekads;
- GloFAS v4 Kratie discharge up to t - L, latency L = 5 days (main run); L = 0 and 10 days as sensitivity runs;
- ONI: the value for the 3-month season ending two months before the issue month;
- astronomical tide (spring-neap and perigee indices) for the target dekad, which is predictable;
- static station attributes (km from mouth, inland canal, river/branch).
The official forecast is a benchmark, never a predictor in the main models. A self-check in build_features.py
asserts the rule.

## 4. Predictors (main model)

log1p(Smax) of the current dekad; change from the previous dekad (when that bulletin exists, else missing);
km from mouth; inland-canal flag; estuary/branch group; dekad of season; GloFAS mean Q over 10 and 30 days and min Q
over 30 days ending t - L, and the Q anomaly against 1997-2015 for the same calendar window; tide spring-neap index
and perigee proximity for the target dekad; ONI. No station identifier in the main model (so it can predict unseen
stations); a station-identifier variant is a secondary run for H1 only.

## 5. Models and benchmarks

- **Benchmarks:** (a) persistence: current-dekad Smax; (b) climatology: mean Smax of the station at the same
  dekad-of-year over the training seasons only (fallback: station mean over training seasons if the dekad is
  unseen); (c) official: Bảng 2 value for the target dekad.
- **Models (two only):** (1) linear quantile regression on log1p(Smax) (scikit-learn QuantileRegressor);
  (2) gradient-boosted quantile regression (scikit-learn 1.7.2 HistGradientBoostingRegressor, loss="quantile";
  LightGBM is not installed and is not needed). Quantile grid
  0.05, 0.10, ..., 0.95. Point forecast = median.
- **Hyperparameters:** library defaults plus a small grid (boosting: depth 2-4, learning rate 0.03-0.1, 100-500
  trees, min leaf 10-30) tuned only by leave-one-season-out inside the training seasons. No test data used.
- **Conformal:** conformalized quantile regression (Romano et al. 2019) on the 0.05/0.95 quantiles for the 90%
  interval, calibrated by cross-conformal over training seasons (season groups, CV+ style). Mondrian variant groups
  the calibration scores by distance-to-mouth group. Exceedance probabilities P(Smax > c), c = 1, 2, 4 g/L, from
  the conformalized quantile grid (monotone interpolation; tails clipped at 0.01/0.99).

## 6. Evaluation designs

1. **Forward by season (main):** test seasons 2024, 2025, 2026; each trained on all earlier seasons (2021-2023 for
   2024, and so on). 2021-2023 are training-only (too few cases: 2, 9, 2 issue dates).
2. **Leave one station out:** within each forward split, the held-out station is removed from training (all
   seasons) and scored in the test season. 28 canonical stations.
3. **Leave one province out:** as 2, with pre-merger province groups.
4. **Extreme-season check (exploratory, not a hypothesis test):** the 2019-20 record season has no forecast cases.
   Checks: (i) PCTT 2020 dekads at Tân An, Bến Lức, Cầu Quan, Gò Quao: are the models' 90% intervals consistent with
   these lower-bound values when driven by PCTT current-dekad values? (ii) monthly maxima Jan-Feb 2020 from the
   comparison column: share of station-months where the model's dekadal median exceeds the monthly maximum
   (should be ~0). Season 2024 (severe) is also reported separately within design 1.

## 7. Metrics and inference

- MAE and skill vs persistence (1 - MAE/MAE_persistence); Brier, reliability diagram, CRPS (from the quantile
  grid); 90% interval coverage and mean width; hit rate, false-alarm rate, Peirce skill score at 1, 2, 4 g/L;
  relative economic value at 4 g/L over C/L 0.05-0.95.
- **Primary threshold 4 g/L** (rice; the bulletins' 4 ‰ line). 1 and 2 g/L are secondary. Note: 68% of observed
  station-dekads exceed 4 g/L, so base rates are high; report base rates with every Brier score.
- **Uncertainty:** paired bootstrap over issue dates (all stations of an issue date resampled together), 2,000
  resamples, within test seasons; percentile 95% CIs. With 27 test issue dates the CIs will be wide; this is stated
  in the paper, not hidden.
- Results per test season and pooled; no cherry-picking of seasons, stations or thresholds.

## 8. Layer A (to be completed before the freeze)

**Data check 01/11/2026 (scripts/tidy_long_records.py) breaks the planned target:**
- Sơn Đốc (GFZ, 2-hourly, ~12 days/month): max(Feb, Mar) > 4 g/L in 21 of 21 seasons 1996-2016 (min 6.3);
  > 8 g/L in 17, > 12 g/L in 9. A 4 g/L event has no variance at this gauge.
- Mendeley (Binh et al. 2019): annual max only at Cầu Quan and Trà Vinh (1991-2016, 26 years); monthly Jan-Jun
  max at Cầu Quan only for 1998, 2010, 2016. No Feb/Mar series at these two stations.
- Bulletins give full Feb/Mar monthly maxima only for Feb 2025, Mar 2025, Mar 2026.
**Redesign (owner, 01/11/2026: option 1, "severe-season" forecast).**
- **Target:** a season is *severe* at a station when its seasonal maximum exceeds the station's median over the
  reference period: Cầu Quan and Trà Vinh annual max 1991-2016 (26 seasons each; medians 8.55 and 9.0 g/L),
  Sơn Đốc max(Feb, Mar) 1996-2016 (21 seasons). Base rate ~50% by construction; upper tercile as a sensitivity run.
  Rationale stated in the paper: at these gauges 4 g/L is exceeded every season, so the decision-relevant signal is
  severity (how far and how early the 4 g/L front reaches inland fields), not exceedance at the gauge.
- **Issue date and predictors (known on 1 November):** ONI of JAS (the latest season published by early November);
  Tân Châu observed monthly Q, Sep-Oct mean (GFZ file, 1980-2016); previous season's maximum at the station.
  GloFAS Kratie Sep-Oct as an alternative discharge predictor (1997+) in a sensitivity run.
- **Model:** logistic regression pooled over the three stations with station intercepts (at most 3 slopes;
  26 seasons do not support more). Climatology (50%) is the reference forecast.
- **Evaluation:** leave-one-season-out (all stations of the held-out season removed together); Brier skill score
  vs climatology with bootstrap over seasons; reliability; ROC AUC. Comparison with Apel et al. 2020 (NHESS) at
  Sơn Đốc where comparable. Out-of-sample extension: seasons 2022 and 2025 where bulletins cover Jan-May (seasonal
  max from bulletins is a lower bound; reported separately).
- **H4 (revised):** acting on the forecast (protective action when P(severe) > C/L, e.g. early sowing) reduces expected
  regret against a fixed calendar and against climatology over C/L in [0.1, 0.9]; relative economic value with
  bootstrap CIs. Regret uses the FAO yield-loss curve and a field-exposure factor swept 0-1 for fields inside
  sluice systems (no operating logs exist). The inside/outside split is a scenario sweep, not station-based (station
  sluice status is unverified for 13 of 37 stations).
- **Crop-option break-even (owner, 01/11/2026; shallow, decision support, not advice).** Options: (1) standard
  Đông Xuân rice; (2) early sowing; (3) salt-tolerant variety; (6) skip the season (zero revenue). For each, expected
  net return as a function of P(severe) using cited yields, costs and prices (Mills et al. 2022 and 2025, Ferrer et
  al. 2022, FAO Paper 29 tolerance curves; docs/background/crop_options_data.md), costs deflated to one base year.
  Output: break-even probabilities between options and the share of seasons in which the forecast crosses them.
  Gauge-to-field salinity factor and sluice exposure factor are swept (no source links them). Rice-shrimp and
  upland crops are out of scope (data news-only) and left to a later crop paper.
- **Not in scope:** farm advice; every crop-option result is reported as a scenario under stated assumptions.

## 9. Deviations from the plan (before freeze)

1. Data: 7 seasons but thin; G0 decided on bulletins present, not on the 21 canonical dates (owner, 01/11/2026).
   Southern-centre JPG maps dropped (no posts for the gap months).
2. Upstream discharge: GloFAS v4 (Open-Meteo) instead of MRC Kratie (portal showed no series for our account).
3. Tide: astronomical spring-neap/perigee indices instead of FES2022/TPXO via pyTMD (no registration needed;
   adequate for a dekadal maximum).
4. Extreme-season test (plan 4.4) downgraded to an exploratory check: no forecast cases in 2019-20.
5. Weekly water levels (Tân Châu, Châu Đốc, Vũng Tàu) and CHIRPS/ERA5-Land rainfall not in the main model (not yet
   parsed; dry-season rain is small). Possible secondary run.
6. Provinces: pre-merger grouping for leave-province-out.
7. Boosting library: scikit-learn HistGradientBoosting instead of LightGBM (already installed; same model class).
8. Main test seasons are 2024-2026 only; 2021-2023 are training-only.
9. Layer A target changed from P(Feb/Mar max > 4 g/L) to a severe-season (above-median seasonal max) forecast,
   because the long records saturate 4 g/L and hold annual maxima only (section 8); crop-option break-even added
   (options 1, 2, 3, 6). Target venue: Climate Services.

## 10. Reproducibility

All scripts in scripts/, run with `python -I -X utf8`. Raw third-party files are not committed (data/raw/ is
gitignored); transcribed NCHMF tables are not published until NCHMF permits; code and scores are published.
Random seeds fixed and recorded per run.

## Deviations after freeze

Approved by the owner on 01/11/2026, after the core-B run (none changes a model, metric or verdict rule):
- **D1.** Check 6.4(ii) (Jan-Feb 2020 monthly maxima) cannot be run as written: no bulletin exists between
  25/12/2019 and 20/05/2020 in our data, so there is no current-dekad Smax at Jan-Feb 2020 issue dates. Only a
  partial run is possible: the 4 PCTT stations on 20/02/2020 (a 6-day dekad, below the completeness rule).
- **D2.** The 2020 extreme-season check trains on the 2021-2026 seasons (later in time). It is a season-held-out
  check, not a forecast in time; reported as such.
- **D3.** The Sông Đốc 42 g/L value (20/05/2020) has no target and predicts no row with a target, so its
  sensitivity run changes only the climatology benchmark.
- **D4** (owner, 02/11/2026; before any H4 computation). H4 main loss model = the direct gauge-to-profit relation of
  Le Phuong-Dung, Alpizar & Mills 2025 (Agric. Econ. 56:976-988, Table 4): profit linear in February maximum gauge
  salinity, separate gated / ungated slopes (-184.4 / -1,127 thousand VND/ha per ‰, deflated to 2025 VND), anchored at
  their group means, floored at -Cost2, salinity capped at 14 g/L (10 and 20 as sensitivity). Reason: same gauge
  variable as our forecast target, with an estimated inside/outside contrast, instead of an unsourced gauge-to-field
  factor. The FAO yield curve with a swept exposure factor becomes a sensitivity run. Parameters and sources:
  docs/background/decision_parameters.md.
- **D5** (owner, 02/11/2026; after the H4 run). H4 part (c) (larger value outside than inside sluice systems) is not
  identifiable under D4: the early-sowing effect is constant across field types, so the forecast's value is
  identical inside and outside wherever the profit floor does not bind; the computed difference (0.037 M VND/ha x
  C/L, from the floor at C/L >= 0.75) is an artefact. Part (c) is therefore not reported in the manuscript; the
  computed value stays in results/layer_a_decision/verdict_h4.md. H4 is reported on parts (a) and (b).
- **D6** (03/11/2026; after scoring, during manuscript revision). Two descriptive calibration measures for the
  4 g/L probabilities were added to the reporting: the reliability term of the Brier score and the count-weighted
  mean |forecast probability - observed frequency| over the reliability-diagram bins (scripts/calibration_summary.py,
  results/core_b/calibration_summary.csv). They are computed from the released reliability bins and do not enter any
  hypothesis criterion; no verdict changes. The pre-specified metrics (CRPS, hit and false-alarm rates, PSS at 1, 2
  and 4 g/L), computed at the time of scoring, are now reported in an appendix table.
