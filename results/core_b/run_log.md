# Core-B run log

- Date 2026-11-01; runtime 31.8 min; quick=False; seed 20261101; bootstrap B=2000.
- Python 3.10.9, numpy 1.26.4, pandas 2.2.3, scipy 1.15.3, scikit-learn 1.7.2, joblib 1.5.3; OMP_NUM_THREADS=1.
- Input data/processed/features.csv sha256[:16] e7a51a2a27d91043 (unchanged by this run; lag 0/10 features rebuilt in memory with build_features.build(lag) and its self_check).
- Runs: 250; total fit time 6.27 CPU-h.

## Ambiguity choices
- Predictors (protocol 4): log1p_smax_cur; change from previous dekad = log1p_delta_smax (log scale, matches the log1p target); km_from_mouth; inland_canal; river_group one-hot (8 groups, the 'estuary/branch group'); dekad_of_season; q_mean10, q_mean30, q_min30, q_anom30 (GloFAS, lag L); tide_abscos_mean (spring-neap index) and tide_perigee_cos (perigee proximity) for the target dekad; oni. tide_spring_days and tide_perigee_min are not used (protocol names one spring-neap index and one perigee index).
- Both models are fitted on log1p(Smax) (protocol states it for the linear model; the same for HGB so that the back-transform and conformal scores are on one scale). Quantiles are sorted per row (non-crossing) and back-transformed with expm1.
- Linear model missing values: a missing-indicator column for log1p_delta_smax, then every NaN replaced by the training-set median; features standardized with training mean/sd; columns constant in training dropped. All fitted on the (inner) training set only. HGB uses NaN natively.
- Hyperparameter grids. HGB: max_depth {2,3,4} x learning_rate {0.03,0.1} x min_samples_leaf {10,30} x max_iter {100,500} (24 combinations, endpoints/midpoint of the protocol ranges), other parameters library defaults, early_stopping off. QuantileRegressor: alpha {0, 0.001, 0.01, 0.1} on standardized features, solver highs. One hyperparameter set per model per run (shared by all 19 quantile levels).
- Tuning criterion: mean pinball loss on the log1p scale over levels 0.05, 0.5, 0.95 (not all 19, to keep the ~250 runs affordable), pooled over the leave-one-season-out folds of the training seasons. Ties: first in grid order. Tuning is redone inside every run (also inside every leave-station-out/leave-province-out run, with the held-out group removed).
- The cross-conformal (CV+) folds are the same leave-one-season-out folds, refitted with the chosen hyperparameters on all 19 levels. The hyperparameters were chosen on the same folds, so the calibration scores are not nested (small optimism possible).
- CQR scores and intervals on the log1p scale: E_i = max(q05_k(i)(x_i) - y_i, y_i - q95_k(i)(x_i)); CV+ interval lower = floor(0.1(n+1))-th smallest of q05_k(i)(x) - E_i, upper = ceil(0.9(n+1))-th smallest of q95_k(i)(x) + E_i (Barber et al. 2021 CV+ applied to CQR); back-transformed with expm1.
- Conformalized quantile grid (used for probabilities and CRPS): each level tau separately, one-sided CV+: score s_i = y_i - q_tau,k(i)(x_i); q'_tau(x) = ceil(tau(n+1))-th smallest of q_tau,k(i)(x) + s_i. Then sorted across tau. The CQR 90% interval is computed separately (two-sided score), so cq05/cq95 need not equal lo_cqr/hi_cqr.
- Exceedance probabilities: CDF linear in log1p(Smax) between the 19 conformalized quantiles; beyond 0.05/0.95 extended linearly with the slope of the end segment; CDF clipped to [0.01, 0.99]; P(Smax > c) = 1 - CDF. Probabilities come from the plain (non-Mondrian) grid.
- Mondrian groups: km <= 15 '0-15', 15 < km <= 40 '15-40', km > 40 '>40'. Inland canals (inland_canal = 1) form their own group when the run's calibration set holds >= 30 inland rows, else they stay in their km group.
- Point forecast = median of the full model (raw, sorted), as protocol 5 states. MAE of the conformalized median (cq50) is reported as mae_cmed.
- Climatology benchmark: observations = every station-dekad Smax in features.csv (smax_cur, incl. ODV rows and rows without a target) of seasons before the test season (incl. the single 2020 bulletin); dekad-of-year of the TARGET dekad. Fallback station mean. The benchmark is the same in all designs (it uses the station's own training-season history also under leave-station/province-out, where only the models lose the station).
- Brier for benchmarks (a) and (b): their deterministic forecast as a 0/1 probability (value > c). A probabilistic climatology (share of training-season observations > c at the station-dekad, same fallback) is reported as climfreq, outside the verdicts.
- Yes/no conversion of model probabilities: threshold p* on 0.01..0.99 maximising the Peirce score on the training rows' out-of-fold calibrated probabilities (fold model quantiles + one-sided conformal shift from the other folds' scores); median of tied maximisers; 0.5 if the training rows have no events or no non-events. Forecast 'yes' when p > p*. Benchmarks: 'yes' when value > c. False-alarm rate = false alarms / non-events (probability of false detection), so PSS = hit rate - false-alarm rate.
- CRPS = 2 x mean pinball loss over the 19 levels (g/L scale, conformalized grid; raw grid as crps_raw).
- Relative economic value at 4 g/L (Richardson 2000), cost/loss a on 0.01 steps, base rate = observed frequency in the (resampled) sample; rows with an official forecast only (paired). The model's user acts when P(>4) > a (main, rev_area_*). The envelope over all probability thresholds (Richardson's potential value) is reported as rev_area_model_env. Areas: trapezoid over a in [0.1, 0.9], value not clipped at 0.
- Bootstrap: issue dates resampled with replacement within each test season (pooled = per-season resamples concatenated), 2,000 resamples, same seed for every forecaster of a design/model (paired). Percentile 95% CIs. Metrics are ratio-of-sums over the resampled dates.
- Verdicts use the pooled forward design (main variant). H2 coverage criteria are applied to the point estimate. H1/H3 are judged per model; the protocol pre-registers two models and no primary one, so both are reported.
- H2 'plain split/cross-conformal' = the plain CV+ CQR interval of this script (lo_cqr/hi_cqr).
- Test stations: the 28 canonical stations in every design; extra stations (Cầu Nổi, Xẻo Rô, Mỹ Tho, Đồng Tâm, Cà Mau) are training-only. Leave-province-out removes extra stations of the held-out province too.
- Sensitivity runs (forward design only): lag0, lag10, noODV (ODV rows removed from training and from the climatology pool), noSD42, stationid (station one-hot added; H1 only).

## Proposed deviations after freeze (not applied to docs/protocol.md; owner to decide)
- (D1) Extreme-season check (ii) (protocol 6.4): the Jan-Feb 2020 monthly maxima cannot be checked as written. A dekadal forecast needs the current-dekad Smax at the issue date, and no bulletin exists between 25/12/2019 and 20/05/2020 in our data. Only the 4 PCTT stations have a current-dekad value in Jan-Feb 2020: the dekad 11-20/02/2020 (6 report days, below the >= 7-day completeness rule, lower bound). Run here: issue 20/02/2020 at those 4 stations, median for 21-29/02 vs the Feb 2020 monthly maximum (flag ok). Jan 2020 and the other ~24 stations: not possible (missing log1p_smax_cur, log1p_delta_smax).
- (D2) Extreme-season check (i) uses models trained on all seasons with a target (2021-2026), i.e. later seasons than 2020; it is an extreme-season-out check, not a forecast in time.
- (D3) noSD42 sensitivity: the Sông Đốc 42 g/L value (20/05/2020) has no target and is not a predictor of any row with a target, so the models are unchanged; only the climatology benchmark is recomputed.

## Data and run facts
- Rows with a target: 1223; per season {2021: 201, 2022: 237, 2023: 53, 2024: 168, 2025: 348, 2026: 216}; ODV rows with a target 127.
- Forward test rows: 732 ({2024: 168, 2025: 348, 2026: 216}); issue dates {2024: 6, 2025: 13, 2026: 8}; official forecast missing in 1 test rows; climatology source {'station_dekad': 686, 'station_mean': 46}.
- Leave-province-out groups (province_canon, pre-merger) and test stations:
  - Bạc Liêu: Gành Hào
  - Bến Tre: An Thuận, Bình Đại, Bến Trại, Hương Mỹ, Lộc Thuận, Sơn Đốc
  - Cà Mau: Sông Đốc
  - Hồ Chí Minh: Cát Lái
  - Kiên Giang: An Ninh, Gò Quao, Rạch Giá
  - Long An: Bến Lức, Tuyên Nhơn, Tân An, Xuân Khánh
  - Sóc Trăng: Long Phú, Sóc Trăng, Thạnh Phú, Trần Đề, Đại Ngãi
  - Tiền Giang: An Định, Hòa Bình, Vàm Kênh
  - Trà Vinh: Cầu Quan, Hưng Mỹ, Trà Kha, Trà Vinh

## Chosen hyperparameters and inland-group decisions (forward and extreme runs)

| design | variant | model | test season | n train | train seasons | hp | tune loss | inland separate (n cal) | groups |
|---|---|---|---|---|---|---|---|---|---|
| extreme | main | hgb | 2020 | 1223 | 2021,2022,2023,2024,2025,2026 | {'max_depth': 3, 'learning_rate': 0.1, 'min_samples_leaf': 10, 'max_iter': 100} | 0.05581 | True (92) | {'0-15': 477, '15-40': 422, '>40': 232, 'inland': 92} |
| extreme | main | qr | 2020 | 1223 | 2021,2022,2023,2024,2025,2026 | {'alpha': 0.01} | 0.0568 | True (92) | {'0-15': 477, '15-40': 422, '>40': 232, 'inland': 92} |
| forward | lag0 | hgb | 2024 | 491 | 2021,2022,2023 | {'max_depth': 2, 'learning_rate': 0.03, 'min_samples_leaf': 10, 'max_iter': 500} | 0.06295 | True (38) | {'0-15': 201, '15-40': 179, '>40': 73, 'inland': 38} |
| forward | lag0 | hgb | 2025 | 659 | 2021,2022,2023,2024 | {'max_depth': 2, 'learning_rate': 0.1, 'min_samples_leaf': 30, 'max_iter': 100} | 0.05822 | True (50) | {'0-15': 267, '15-40': 233, '>40': 109, 'inland': 50} |
| forward | lag0 | hgb | 2026 | 1007 | 2021,2022,2023,2024,2025 | {'max_depth': 2, 'learning_rate': 0.1, 'min_samples_leaf': 10, 'max_iter': 100} | 0.05305 | True (76) | {'0-15': 397, '15-40': 350, '>40': 184, 'inland': 76} |
| forward | lag0 | qr | 2024 | 491 | 2021,2022,2023 | {'alpha': 0.01} | 0.06116 | True (38) | {'0-15': 201, '15-40': 179, '>40': 73, 'inland': 38} |
| forward | lag0 | qr | 2025 | 659 | 2021,2022,2023,2024 | {'alpha': 0.01} | 0.07615 | True (50) | {'0-15': 267, '15-40': 233, '>40': 109, 'inland': 50} |
| forward | lag0 | qr | 2026 | 1007 | 2021,2022,2023,2024,2025 | {'alpha': 0.01} | 0.05182 | True (76) | {'0-15': 397, '15-40': 350, '>40': 184, 'inland': 76} |
| forward | lag10 | hgb | 2024 | 491 | 2021,2022,2023 | {'max_depth': 2, 'learning_rate': 0.03, 'min_samples_leaf': 10, 'max_iter': 500} | 0.06378 | True (38) | {'0-15': 201, '15-40': 179, '>40': 73, 'inland': 38} |
| forward | lag10 | hgb | 2025 | 659 | 2021,2022,2023,2024 | {'max_depth': 2, 'learning_rate': 0.03, 'min_samples_leaf': 10, 'max_iter': 500} | 0.0583 | True (50) | {'0-15': 267, '15-40': 233, '>40': 109, 'inland': 50} |
| forward | lag10 | hgb | 2026 | 1007 | 2021,2022,2023,2024,2025 | {'max_depth': 2, 'learning_rate': 0.1, 'min_samples_leaf': 10, 'max_iter': 100} | 0.05304 | True (76) | {'0-15': 397, '15-40': 350, '>40': 184, 'inland': 76} |
| forward | lag10 | qr | 2024 | 491 | 2021,2022,2023 | {'alpha': 0.01} | 0.06439 | True (38) | {'0-15': 201, '15-40': 179, '>40': 73, 'inland': 38} |
| forward | lag10 | qr | 2025 | 659 | 2021,2022,2023,2024 | {'alpha': 0.01} | 0.07761 | True (50) | {'0-15': 267, '15-40': 233, '>40': 109, 'inland': 50} |
| forward | lag10 | qr | 2026 | 1007 | 2021,2022,2023,2024,2025 | {'alpha': 0.01} | 0.05174 | True (76) | {'0-15': 397, '15-40': 350, '>40': 184, 'inland': 76} |
| forward | main | hgb | 2024 | 491 | 2021,2022,2023 | {'max_depth': 2, 'learning_rate': 0.03, 'min_samples_leaf': 10, 'max_iter': 500} | 0.06184 | True (38) | {'0-15': 201, '15-40': 179, '>40': 73, 'inland': 38} |
| forward | main | hgb | 2025 | 659 | 2021,2022,2023,2024 | {'max_depth': 3, 'learning_rate': 0.1, 'min_samples_leaf': 30, 'max_iter': 100} | 0.05718 | True (50) | {'0-15': 267, '15-40': 233, '>40': 109, 'inland': 50} |
| forward | main | hgb | 2026 | 1007 | 2021,2022,2023,2024,2025 | {'max_depth': 2, 'learning_rate': 0.1, 'min_samples_leaf': 10, 'max_iter': 100} | 0.05346 | True (76) | {'0-15': 397, '15-40': 350, '>40': 184, 'inland': 76} |
| forward | main | qr | 2024 | 491 | 2021,2022,2023 | {'alpha': 0.01} | 0.06399 | True (38) | {'0-15': 201, '15-40': 179, '>40': 73, 'inland': 38} |
| forward | main | qr | 2025 | 659 | 2021,2022,2023,2024 | {'alpha': 0.01} | 0.07373 | True (50) | {'0-15': 267, '15-40': 233, '>40': 109, 'inland': 50} |
| forward | main | qr | 2026 | 1007 | 2021,2022,2023,2024,2025 | {'alpha': 0.01} | 0.05258 | True (76) | {'0-15': 397, '15-40': 350, '>40': 184, 'inland': 76} |
| forward | noODV | hgb | 2024 | 364 | 2021,2022,2023 | {'max_depth': 2, 'learning_rate': 0.1, 'min_samples_leaf': 30, 'max_iter': 100} | 0.06805 | False (28) | {'0-15': 150, '15-40': 134, '>40': 80} |
| forward | noODV | hgb | 2025 | 532 | 2021,2022,2023,2024 | {'max_depth': 4, 'learning_rate': 0.1, 'min_samples_leaf': 10, 'max_iter': 100} | 0.05918 | True (40) | {'0-15': 216, '15-40': 188, '>40': 88, 'inland': 40} |
| forward | noODV | hgb | 2026 | 880 | 2021,2022,2023,2024,2025 | {'max_depth': 2, 'learning_rate': 0.1, 'min_samples_leaf': 30, 'max_iter': 100} | 0.05367 | True (66) | {'0-15': 346, '15-40': 305, '>40': 163, 'inland': 66} |
| forward | noODV | qr | 2024 | 364 | 2021,2022,2023 | {'alpha': 0.01} | 0.06422 | False (28) | {'0-15': 150, '15-40': 134, '>40': 80} |
| forward | noODV | qr | 2025 | 532 | 2021,2022,2023,2024 | {'alpha': 0.01} | 0.07001 | True (40) | {'0-15': 216, '15-40': 188, '>40': 88, 'inland': 40} |
| forward | noODV | qr | 2026 | 880 | 2021,2022,2023,2024,2025 | {'alpha': 0.01} | 0.05427 | True (66) | {'0-15': 346, '15-40': 305, '>40': 163, 'inland': 66} |
| forward | stationid | hgb | 2024 | 491 | 2021,2022,2023 | {'max_depth': 2, 'learning_rate': 0.1, 'min_samples_leaf': 10, 'max_iter': 500} | 0.06251 | True (38) | {'0-15': 201, '15-40': 179, '>40': 73, 'inland': 38} |
| forward | stationid | hgb | 2025 | 659 | 2021,2022,2023,2024 | {'max_depth': 3, 'learning_rate': 0.1, 'min_samples_leaf': 10, 'max_iter': 100} | 0.05594 | True (50) | {'0-15': 267, '15-40': 233, '>40': 109, 'inland': 50} |
| forward | stationid | hgb | 2026 | 1007 | 2021,2022,2023,2024,2025 | {'max_depth': 2, 'learning_rate': 0.03, 'min_samples_leaf': 30, 'max_iter': 500} | 0.05346 | True (76) | {'0-15': 397, '15-40': 350, '>40': 184, 'inland': 76} |
| forward | stationid | qr | 2024 | 491 | 2021,2022,2023 | {'alpha': 0.01} | 0.05903 | True (38) | {'0-15': 201, '15-40': 179, '>40': 73, 'inland': 38} |
| forward | stationid | qr | 2025 | 659 | 2021,2022,2023,2024 | {'alpha': 0.01} | 0.07511 | True (50) | {'0-15': 267, '15-40': 233, '>40': 109, 'inland': 50} |
| forward | stationid | qr | 2026 | 1007 | 2021,2022,2023,2024,2025 | {'alpha': 0.01} | 0.05264 | True (76) | {'0-15': 397, '15-40': 350, '>40': 184, 'inland': 76} |
- loso: 164 runs; inland group separate in 156; hp counts {('hgb', "{'max_depth': 2, 'learning_rate': 0.03, 'min_samples_leaf': 10, 'max_iter': 500}"): 27, ('hgb', "{'max_depth': 2, 'learning_rate': 0.1, 'min_samples_leaf': 10, 'max_iter': 100}"): 15, ('hgb', "{'max_depth': 2, 'learning_rate': 0.1, 'min_samples_leaf': 30, 'max_iter': 100}"): 13, ('hgb', "{'max_depth': 3, 'learning_rate': 0.1, 'min_samples_leaf': 30, 'max_iter': 100}"): 11, ('hgb', "{'max_depth': 3, 'learning_rate': 0.1, 'min_samples_leaf': 10, 'max_iter': 100}"): 6, ('hgb', "{'max_depth': 4, 'learning_rate': 0.1, 'min_samples_leaf': 30, 'max_iter': 100}"): 4, ('hgb', "{'max_depth': 2, 'learning_rate': 0.1, 'min_samples_leaf': 10, 'max_iter': 500}"): 2, ('hgb', "{'max_depth': 3, 'learning_rate': 0.03, 'min_samples_leaf': 30, 'max_iter': 500}"): 2, ('hgb', "{'max_depth': 2, 'learning_rate': 0.03, 'min_samples_leaf': 30, 'max_iter': 500}"): 1, ('hgb', "{'max_depth': 3, 'learning_rate': 0.03, 'min_samples_leaf': 10, 'max_iter': 500}"): 1, ('qr', "{'alpha': 0.01}"): 82}
- lopo: 54 runs; inland group separate in 48; hp counts {('hgb', "{'max_depth': 2, 'learning_rate': 0.03, 'min_samples_leaf': 10, 'max_iter': 500}"): 7, ('hgb', "{'max_depth': 2, 'learning_rate': 0.1, 'min_samples_leaf': 30, 'max_iter': 100}"): 6, ('hgb', "{'max_depth': 2, 'learning_rate': 0.1, 'min_samples_leaf': 10, 'max_iter': 100}"): 3, ('hgb', "{'max_depth': 3, 'learning_rate': 0.1, 'min_samples_leaf': 30, 'max_iter': 100}"): 3, ('hgb', "{'max_depth': 2, 'learning_rate': 0.03, 'min_samples_leaf': 30, 'max_iter': 500}"): 2, ('hgb', "{'max_depth': 3, 'learning_rate': 0.03, 'min_samples_leaf': 10, 'max_iter': 500}"): 2, ('hgb', "{'max_depth': 2, 'learning_rate': 0.1, 'min_samples_leaf': 30, 'max_iter': 500}"): 1, ('hgb', "{'max_depth': 3, 'learning_rate': 0.1, 'min_samples_leaf': 10, 'max_iter': 100}"): 1, ('hgb', "{'max_depth': 4, 'learning_rate': 0.1, 'min_samples_leaf': 10, 'max_iter': 100}"): 1, ('hgb', "{'max_depth': 4, 'learning_rate': 0.1, 'min_samples_leaf': 30, 'max_iter': 100}"): 1, ('qr', "{'alpha': 0.01}"): 26, ('qr', "{'alpha': 0.1}"): 1}

## Headline numbers (pooled; per season in bootstrap_ci.csv)

| design | model | MAE model | MAE diff vs persist | vs clim | vs official | Brier4 diff vs persist | vs clim | cov CQR | cov Mondrian | width CQR | REV area diff |
|---|---|---|---|---|---|---|---|---|---|---|---|
| forward | hgb | 1.88 | -0.02 [-0.13, 0.08] | -0.95 [-1.36, -0.53] | 0.03 [-0.15, 0.23] | -0.025 [-0.039, -0.011] | -0.106 [-0.138, -0.072] | 0.923 | 0.928 | 9.72 | 0.129 [0.052, 0.211] |
| forward | qr | 2.44 | 0.54 [0.34, 0.73] | -0.39 [-0.75, -0.04] | 0.59 [0.37, 0.81] | -0.013 [-0.030, 0.003] | -0.094 [-0.126, -0.061] | 0.955 | 0.951 | 35.36 | 0.088 [0.009, 0.173] |
| loso | hgb | 2.15 | 0.25 [0.14, 0.36] | -0.68 [-1.09, -0.25] | 0.30 [0.11, 0.50] | -0.024 [-0.038, -0.010] | -0.105 [-0.139, -0.070] | 0.911 | 0.900 | 9.75 | 0.124 [0.046, 0.211] |
| loso | qr | 2.53 | 0.62 [0.43, 0.81] | -0.31 [-0.67, 0.04] | 0.68 [0.45, 0.90] | -0.012 [-0.030, 0.004] | -0.093 [-0.125, -0.060] | 0.944 | 0.941 | 33.98 | 0.083 [0.003, 0.169] |
| lopo | hgb | 2.15 | 0.24 [0.13, 0.36] | -0.69 [-1.09, -0.27] | 0.30 [0.09, 0.50] | -0.024 [-0.038, -0.011] | -0.105 [-0.137, -0.071] | 0.892 | 0.902 | 10.06 | 0.122 [0.048, 0.203] |
| lopo | qr | 2.59 | 0.69 [0.50, 0.87] | -0.24 [-0.61, 0.12] | 0.74 [0.51, 0.97] | -0.009 [-0.026, 0.008] | -0.089 [-0.121, -0.057] | 0.933 | 0.932 | 32.33 | 0.078 [-0.000, 0.164] |

## Sensitivity runs (forward design, pooled)

| variant | model | MAE model | MAE diff vs persist | vs clim | vs official | Brier4 diff vs persist | vs clim | cov CQR | REV area diff | H1 |
|---|---|---|---|---|---|---|---|---|---|---|
| main | hgb | 1.88 | -0.02 [-0.13, 0.08] | -0.95 [-1.36, -0.53] | 0.03 [-0.15, 0.23] | -0.025 [-0.039, -0.011] | -0.106 [-0.138, -0.072] | 0.923 | 0.129 [0.052, 0.211] | not supported |
| main | qr | 2.44 | 0.54 [0.34, 0.73] | -0.39 [-0.75, -0.04] | 0.59 [0.37, 0.81] | -0.013 [-0.030, 0.003] | -0.094 [-0.126, -0.061] | 0.955 | 0.088 [0.009, 0.173] | not supported |
| lag0 | hgb | 1.88 | -0.02 [-0.12, 0.08] | -0.95 [-1.36, -0.54] | 0.03 [-0.17, 0.25] | -0.023 [-0.038, -0.009] | -0.104 [-0.137, -0.070] | 0.933 | 0.119 [0.044, 0.202] | not supported |
| lag0 | qr | 2.51 | 0.61 [0.40, 0.81] | -0.32 [-0.68, 0.02] | 0.66 [0.43, 0.89] | -0.012 [-0.029, 0.004] | -0.093 [-0.125, -0.061] | 0.955 | 0.090 [0.012, 0.173] | not supported |
| lag10 | hgb | 1.84 | -0.06 [-0.17, 0.05] | -0.99 [-1.39, -0.58] | -0.01 [-0.18, 0.18] | -0.023 [-0.037, -0.009] | -0.104 [-0.136, -0.070] | 0.926 | 0.115 [0.041, 0.198] | not supported |
| lag10 | qr | 2.35 | 0.45 [0.25, 0.65] | -0.48 [-0.85, -0.12] | 0.50 [0.29, 0.72] | -0.014 [-0.032, 0.002] | -0.095 [-0.127, -0.063] | 0.944 | 0.092 [0.011, 0.179] | not supported |
| noODV | hgb | 1.89 | -0.01 [-0.15, 0.12] | -0.95 [-1.29, -0.60] | 0.04 [-0.14, 0.22] | -0.024 [-0.041, -0.009] | -0.103 [-0.133, -0.074] | 0.922 | 0.120 [0.042, 0.201] | not supported |
| noODV | qr | 2.08 | 0.17 [0.02, 0.32] | -0.76 [-1.18, -0.34] | 0.22 [0.04, 0.41] | -0.027 [-0.040, -0.014] | -0.106 [-0.138, -0.074] | 0.917 | 0.132 [0.066, 0.201] | not supported |
| noSD42 | hgb | 1.88 | -0.02 [-0.13, 0.08] | -0.95 [-1.36, -0.53] | 0.03 [-0.15, 0.23] | -0.025 [-0.039, -0.011] | -0.106 [-0.138, -0.072] | 0.923 | 0.129 [0.052, 0.211] | not supported |
| noSD42 | qr | 2.44 | 0.54 [0.34, 0.73] | -0.39 [-0.76, -0.05] | 0.59 [0.37, 0.81] | -0.013 [-0.030, 0.003] | -0.094 [-0.126, -0.061] | 0.955 | 0.088 [0.009, 0.173] | not supported |
| stationid | hgb | 1.87 | -0.04 [-0.14, 0.07] | -0.97 [-1.38, -0.55] | 0.02 [-0.17, 0.22] | -0.024 [-0.039, -0.010] | -0.105 [-0.137, -0.072] | 0.930 | 0.122 [0.047, 0.205] | not supported |
| stationid | qr | 2.43 | 0.53 [0.33, 0.72] | -0.40 [-0.77, -0.05] | 0.58 [0.36, 0.80] | -0.016 [-0.033, 0.000] | -0.097 [-0.128, -0.066] | 0.958 | 0.101 [0.023, 0.185] | not supported |
- stationid is an H1-only run; its coverage/REV columns are shown for completeness.

## Extreme-season check 2020 (exploratory)
- (i) hgb: 28 station-dekads (4 stations, issues 29/02-30/04/2020, PCTT complete dekads). PCTT next-dekad value <= CQR upper bound in 93% (consistent with a lower bound); inside the interval 93%; above the upper bound 7%; Mondrian upper bound exceeded in 7%. Median abs. diff median vs PCTT 0.95 g/L.
- (ii) hgb: issue 20/02/2020, dekadal median for 21-29/02 vs Feb 2020 monthly max (ok): Bến Lức 9.2 vs 11.1, Cầu Quan 12.2 vs 14.6, Gò Quao 8.4 vs 10.4, Tân An 7.3 vs 8.6; median exceeds the monthly max in 0 of 4.
- (i) qr: 28 station-dekads (4 stations, issues 29/02-30/04/2020, PCTT complete dekads). PCTT next-dekad value <= CQR upper bound in 89% (consistent with a lower bound); inside the interval 86%; above the upper bound 11%; Mondrian upper bound exceeded in 11%. Median abs. diff median vs PCTT 1.32 g/L.
- (ii) qr: issue 20/02/2020, dekadal median for 21-29/02 vs Feb 2020 monthly max (ok): Bến Lức 10.6 vs 11.1, Cầu Quan 14.2 vs 14.6, Gò Quao 10.8 vs 10.4, Tân An 7.7 vs 8.6; median exceeds the monthly max in 1 of 4.


Note: verdicts.md and run_log.md were regenerated from the written CSVs after fixing a report-only bug (Feb 2020 monthly-max lookup in check ii used the DataFrame .flags attribute). Metrics, predictions and bootstrap CIs are those of the full run (31.8 min); the self-check tolerance was set to the CSV rounding (predictions.csv written with 5 significant digits in this run; 6 from now on).
