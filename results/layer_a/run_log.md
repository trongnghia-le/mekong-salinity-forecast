# Layer A run log (scripts/run_layer_a.py, seed 20261101, 2000 bootstrap resamples)

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
  (slope 0.216, intercept 13483, r = 0.429); chosen over the GloFAS-model variant so the pre-registered main model is unchanged.
- Observed seasonal max = max over bulletin issue dates Dec(Y-1)-Jun(Y) (Sơn Đốc: Feb-Mar issues only), a LOWER bound; coverage per station is in extension.csv (n_bulletins).
  Previous-season max for the lag predictor is likewise a bulletin lower bound (2021 covers Jan-Feb only; 2024 covers Mar-May only) and is therefore biased low; this is a known weakness of the extension.
- Bulletin dekad Smax vs 2-hourly/daily gauge max: different support, so comparison to the medians is approximate.

## Variants run
- main_median_TanChau: n=70, seasons 1992-2016, base rate 0.500
- sens_tercile_TanChau: n=70, seasons 1992-2016, base rate 0.343
- sens_median_GloFAS: n=57, seasons 1998-2016, base rate 0.596
- sens_tercile_GloFAS: n=57, seasons 1998-2016, base rate 0.421

## Proposed deviations
None required. (Only notes: seasons lost to the lag predictor; unpenalised fit; GloFAS rescaling for the extension.)
