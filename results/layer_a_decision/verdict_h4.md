# H4 verdict (layer A, severe-season forecast; scenario analysis, not farm advice)

Areas are integrals over C/L 0.1-0.9 (trapezoid, step 0.05). Regret reduction in M VND/ha x unit C/L; REV area unitless (max 0.8). Bootstrap: 2,000 season resamples, seed 20261101, 95% percentile CI. Main model: D4 loss model, S cap 14 g/L, Delta_sev = 10.1 M VND/ha (F22), 70 station-seasons.

- gated: regret reduction by the forecast vs fixed calendar 1.527 [0.012, 3.045]; vs climatology 0.617 [-0.336, 1.489]. REV area vs fixed 0.302 [0.003, 0.487]; vs climatology 0.109 [-0.159, 0.309]; climatology vs fixed 0.180 [0.006, 0.272].
- ungated: regret reduction by the forecast vs fixed calendar 1.564 [0.068, 3.064]; vs climatology 0.654 [-0.270, 1.505]. REV area vs fixed 0.310 [0.018, 0.490]; vs climatology 0.117 [-0.148, 0.313]; climatology vs fixed 0.180 [0.006, 0.272].

## H4 parts, applied literally
- (a) forecast reduces expected regret vs fixed calendar (CI > 0, both field types): YES.
- (b) forecast reduces expected regret vs climatology (CI > 0, both field types): NO.
- (c) reduction larger outside than inside sluice systems (ungated minus gated CI > 0): YES; vs fixed 0.037 [0.006, 0.074], vs climatology 0.037 [0.006, 0.074].
- **H4 overall: NOT SUPPORTED** (requires a, b and c).

## Structural note on (c)
In the D4 model the early-sowing effect Delta (m or Delta_sev) is a constant that does not depend on S or on field type, so the profit level and slope cancel in the difference between actions: REV and regret reduction are identical for gated and ungated fields wherever the -Cost2 floor does not bind (C/L up to about 0.70; checked numerically). The only gated-ungated difference in the main run (0.037 M VND/ha x C/L) comes from the floor at C/L >= 0.75, where the implied m = -rDelta/(1-r) is below -30 M VND/ha, far outside any literature value; it is an artefact of the grid, not an inside/outside effect. Part (c) is therefore reported literally as computed but should not be read as evidence for the hypothesis. Gating matters substantively through (i) which m (hence C/L) is plausible and (ii) the FAO variant, where the recoverable loss is capped by the salinity loss.

## Restricted to the C/L window implied by the literature m range (0.1-0.3, ungated; descriptive)
- gated: regret reduction vs fixed 0.750 [0.392, 1.115]; vs climatology -0.000 [-0.135, 0.113].
- ungated: regret reduction vs fixed 0.750 [0.392, 1.115]; vs climatology -0.000 [-0.135, 0.113].

## C/L implied by the literature parameters
- Ungated m in [-4.2, +4.7]: C/L = -m/(Delta_sev - m) runs from 0 (m >= 0, early sowing dominates) to 0.294 (m = -4.2, Ferrer Delta_sev 10.1); with Delta_sev 8.3: 0.336.
- Gated m in [0, +8.3]: m >= 0 throughout, so early sowing is never worse than the standard calendar (no cost-loss tradeoff; C/L = 0). The forecast then has no value for this action over the literature range.
- Mean regret (M VND/ha) at literature m, gated:

```
strategy  always  clim   fc  fixed
m                                 
0.00         0.0   0.0  0.0  5.050
2.08         0.0   0.0  0.0  6.090
4.15         0.0   0.0  0.0  7.125
6.22         0.0   0.0  0.0  8.160
8.30         0.0   0.0  0.0  9.200
```
- Mean regret (M VND/ha) at literature m, ungated:

```
strategy  always  clim     fc  fixed
m                                   
-4.20       2.10  2.10  1.597  5.050
-1.98       0.99  0.99  1.228  5.050
 0.00       0.00  0.00  0.000  5.050
 0.25       0.00  0.00  0.000  5.175
 2.48       0.00  0.00  0.000  6.290
 4.70       0.00  0.00  0.000  7.400
```

## Sensitivity (area of regret reduction vs fixed / vs climatology, ungated; gated differs only in FAO variants)
- main: ungated vs fixed 1.564 [0.068, 3.064], vs clim 0.654 [-0.270, 1.505]; gated vs fixed 1.527 [0.012, 3.045], vs clim 0.617 [-0.336, 1.489]; ungated-gated (vs fixed) 0.037 [0.006, 0.074].
- cap10: ungated vs fixed 1.563 [0.068, 3.064], vs clim 0.653 [-0.271, 1.505]; gated vs fixed 1.527 [0.012, 3.045], vs clim 0.617 [-0.336, 1.489]; ungated-gated (vs fixed) 0.036 [0.006, 0.073].
- cap20: ungated vs fixed 1.564 [0.068, 3.064], vs clim 0.654 [-0.270, 1.505]; gated vs fixed 1.527 [0.012, 3.045], vs clim 0.617 [-0.336, 1.489]; ungated-gated (vs fixed) 0.037 [0.006, 0.074].
- b_ungated_plus1.96SE: ungated vs fixed 1.569 [0.076, 3.067], vs clim 0.659 [-0.260, 1.510]; gated vs fixed 1.527 [0.012, 3.045], vs clim 0.617 [-0.336, 1.489]; ungated-gated (vs fixed) 0.043 [0.007, 0.085].
- b_ungated_minus1.96SE: ungated vs fixed 1.558 [0.060, 3.062], vs clim 0.648 [-0.280, 1.501]; gated vs fixed 1.527 [0.012, 3.045], vs clim 0.617 [-0.336, 1.489]; ungated-gated (vs fixed) 0.031 [0.005, 0.063].
- b_gated_plus1.96SE: ungated vs fixed 1.564 [0.068, 3.064], vs clim 0.654 [-0.270, 1.505]; gated vs fixed 1.528 [0.013, 3.046], vs clim 0.618 [-0.334, 1.489]; ungated-gated (vs fixed) 0.036 [0.006, 0.072].
- b_gated_minus1.96SE: ungated vs fixed 1.564 [0.068, 3.064], vs clim 0.654 [-0.270, 1.505]; gated vs fixed 1.526 [0.011, 3.045], vs clim 0.616 [-0.337, 1.489]; ungated-gated (vs fixed) 0.038 [0.006, 0.076].
- gated_slope_0.1x: ungated vs fixed 1.564 [0.068, 3.064], vs clim 0.654 [-0.270, 1.505]; gated vs fixed 1.526 [0.012, 3.045], vs clim 0.616 [-0.337, 1.489]; ungated-gated (vs fixed) 0.037 [0.006, 0.075].
- gated_slope_0.2x: ungated vs fixed 1.564 [0.068, 3.064], vs clim 0.654 [-0.270, 1.505]; gated vs fixed 1.527 [0.013, 3.045], vs clim 0.617 [-0.336, 1.489]; ungated-gated (vs fixed) 0.037 [0.006, 0.073].
- gated_slope_0.3x: ungated vs fixed 1.564 [0.068, 3.064], vs clim 0.654 [-0.270, 1.505]; gated vs fixed 1.528 [0.013, 3.046], vs clim 0.618 [-0.334, 1.489]; ungated-gated (vs fixed) 0.036 [0.006, 0.072].
- Dsev_Le_8.3: ungated vs fixed 1.246 [-0.006, 2.496], vs clim 0.498 [-0.291, 1.222]; gated vs fixed 1.226 [-0.034, 2.485], vs clim 0.478 [-0.323, 1.216]; ungated-gated (vs fixed) 0.020 [0.003, 0.039].
- target_upper_tercile: ungated vs fixed 0.399 [-1.068, 1.722], vs clim 0.203 [-0.979, 1.190]; gated vs fixed 0.371 [-1.133, 1.715], vs clim 0.175 [-1.055, 1.190]; ungated-gated (vs fixed) 0.028 [-0.000, 0.086].
- FAO_f0.1: ungated vs fixed -1.209 [-2.071, -0.464], vs clim -0.225 [-1.061, 0.537]; gated vs fixed -1.209 [-2.071, -0.464], vs clim -0.225 [-1.061, 0.537]; ungated-gated (vs fixed) 0.000 [0.000, 0.000].
- FAO_f0.25: ungated vs fixed 0.770 [-0.642, 2.137], vs clim 0.451 [-0.497, 1.268]; gated vs fixed -1.209 [-2.071, -0.464], vs clim -0.225 [-1.061, 0.537]; ungated-gated (vs fixed) 1.979 [1.066, 2.957].
- FAO_f0.5: ungated vs fixed 1.697 [0.311, 3.117], vs clim 0.787 [-0.039, 1.563]; gated vs fixed -1.209 [-2.071, -0.464], vs clim -0.225 [-1.061, 0.537]; ungated-gated (vs fixed) 2.907 [1.824, 4.029].
- FAO_f0.75: ungated vs fixed 2.161 [0.963, 3.399], vs clim 1.098 [0.449, 1.716]; gated vs fixed -1.090 [-1.969, -0.338], vs clim -0.181 [-1.037, 0.562]; ungated-gated (vs fixed) 3.251 [2.078, 4.423].

## Break-even (main setting: m gated 4.15, ungated 0.25 = range midpoints; k 0.4; F 3.15; S_sev 11.49, S_mild 7.54 g/L)

```
  group  option_a  option_b  p_star_main  p_star_sweep_min  p_star_sweep_max  share_sweep_with_crossing  winner_at_p05_main  share_forecasts_above_main
  gated         1         2          NaN            -0.000            -0.000                      0.111                   2                         NaN
  gated         1         3        0.922             0.709             0.922                      0.300                   1                       0.086
  gated         1         6          NaN               NaN               NaN                      0.000                   1                         NaN
  gated         2         3          NaN               NaN               NaN                      0.000                   2                         NaN
  gated         2         6          NaN               NaN               NaN                      0.000                   2                         NaN
  gated         3         6          NaN               NaN               NaN                      0.000                   3                         NaN
ungated         1         2          NaN             0.079             0.294                      0.444                   2                         NaN
ungated         1         3          NaN             0.382             0.924                      0.500                   3                         NaN
ungated         1         6          NaN               NaN               NaN                      0.000                   1                         NaN
ungated         2         3        0.039             0.008             0.497                      0.411                   2                       0.957
ungated         2         6          NaN               NaN               NaN                      0.000                   2                         NaN
ungated         3         6          NaN               NaN               NaN                      0.000                   3                         NaN
```

Out-of-sample p_severe: median 0.57, share below 0.2 0.24, share above 0.8 0.24.
