# Layer-A decision parameters (compiled 2026-11-01)

Scenario inputs for the regret and break-even analysis (protocol section 8). Not farm advice.
Labels: **checked** = value read in full text (page/table given); **abstract** = abstract or search snippet only;
**nf** = not found; **assumed** = to be swept. Full texts read (local, gitignored, `data/raw/decision_papers/`): Mills et al. 2022,
Ferrer et al. 2022, Mills et al. 2025 and Le et al. 2025 (the last two downloaded by the owner in a browser, 2026-11-01; both CC BY).
Page numbers are journal pages (M25 170-186, L25 976-988). Updated 2026-11-02 with M25 and L25.
Sources: [M22] Mills et al. 2022 Clim. Dev., doi:10.1080/17565529.2022.2072800 (788 hh, 7 provinces, Dong Xuan 2017/18 and 2018/19).
[F22] Ferrer et al. 2022 Econ. Anal. Policy 73:639-652, doi:10.1016/j.eap.2021.12.018 (1,176 farmers, Long An / Kien Giang / Soc Trang, W-S 2019/20, CC BY-NC-ND).
[M25] Mills, Ta, Ta, Nguyen 2025, doi:10.1002/jaa2.70004. [L25] Le, Alpizar, Mills 2025, doi:10.1111/agec.70045.
[FAO] Ayers & Westcot 1985, FAO I&D Paper 29 rev.1, Table A1.1, fao.org/4/Y4263E/y4263e0e.htm.

## Deflator (World Bank FP.CPI.TOTL, Viet Nam, 2010=100; IMF IFS source; API fetch 2026-11-01, one decimal)
| Year | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 |
|---|---|---|---|---|---|---|---|---|---|
| CPI | 153.6 | 159.1 | 163.5 | 168.8 | 171.9 | 177.3 | 183.1 | 189.7 | 196.0 |
| Factor to 2025 VND | 1.276 | 1.232 | 1.199 | 1.161 | 1.140 | 1.105 | 1.070 | 1.033 | 1.000 |

Base year 2025. Year mapping (assumption): M22 mean of DX 2017/18 and 2018/19 -> factor 1.215 (average of 2018 and 2019 harvest-year factors);
F22 W-S 2019/20 -> 2020, factor 1.161. 2025 value is as reported on the fetch date and may be revised.
Rice farm-gate price is not deflated by CPI in the model: use observed nominal price per year as a price scenario (assumed, see below).

## Option 1: standard Dong Xuan rice (mild-year anchor from M22; severe-year anchor from F22 non-early group)
| Parameter | Value (nominal) | 2025 VND | Unit | Year | Source, page/table | Label |
|---|---|---|---|---|---|---|
| Yield, mean of 2 seasons | 6.5 | | t/ha | 2017-19 | M22 Table 1 (6,500 kg, SD 2,153) | checked |
| Farm-gate price | 5.451 (SD 1.131) | | 000 VND/kg | 2017-19 | M22 Table 1; price fell ~14% 2017/18 to 2018/19 (Table 4, DX1819 -0.769) | checked |
| Gross revenue | 35.69 | 43.4 | M VND/ha | 2017-19 | M22 Table 1 | checked |
| Cost1 (inputs, water, land rent) | 11.21 | 13.6 | M VND/ha | 2017-19 | M22 Table 1 | checked |
| Cost2 (+ machine, hired labour) | 16.47 | 20.0 | M VND/ha | 2017-19 | M22 Table 1 | checked |
| Cost3 (+ family labour) | 19.24 | 23.4 | M VND/ha | 2017-19 | M22 Table 1 | checked |
| Net revenue2 (proposed profit measure) | 19.23 (text: 20.8 in exit sample) | 23.4 | M VND/ha | 2017-19 | M22 Table 1, p.7 text | checked |
| Share of fields behind salinity gates | 0.73 (panel A), 0.69 (panel B) | | share | 2017-19 | M22 Table 1 | checked |
| Severe-year yield (sold) | 3.09 early-not / 5.51 early | | t/ha | 2019/20 | F22 Table 3 (PDF p.7) | checked |
| Severe-year revenue, cost, profit (non-early) | 16.91, 13.66, 3.26 | 19.6, 15.9, 3.8 | M VND/ha | 2019/20 | F22 Table 3 | checked |
| Annual land rent | 2.71 (all) | 3.15 | M VND/ha/yr | 2019/20 | F22 Table 4 (Rental) | checked |
| Growth period | emergence 18 d, flowering ~60 d, harvest ~97 d | | days | 2019/20 | F22 sec. 4.1 | checked |
| Exit: share of fields not in rice next season | 0.15; ungated +0.08; profit 20.8 -> 0 raises exit by 0.031 | | prob. | 2017-19 | M22 Table 1B, Table 5 text | checked |
| M25 salinity measure `sal3` | indicator, field-interpolated station salinity > 3 g/L in February (mean 0.69); stations sit at irrigation-gate inlets of major tributaries (higher than interior fields); nearest of 25 stations; statistic (max or mean) for `sal3` not stated, `sal3_5yrs` is defined on monthly average | | g/L | 2017-20 | M25 p.175, Table 1 p.176 | checked |
| M25 profit definition, mean (SD) | profit1 19.7 (13.7), min -23.6, max 197.9 (rice, paid labour in, family labour out); profit2 (+shrimp) 21.7 | 23.2 | M VND/ha | DX 2018/19-2019/20 (wave 1 not used) | M25 Table 1 p.176, p.177; factor 1.18 (avg 2019, 2020) | checked |
| M25 effect of `sal3` on IHS(profit) | -2.417 (SE 0.937) rice; -2.217 (0.870) rice+shrimp; two-stage panel selection (Semykina-Wooldridge), N=1,275 / 1,344; FE estimate "much smaller, n.s." | | log-like | | M25 Table 2 p.179, text p.178 | checked |
| M25 simulated profit, high vs low salinity | 4.5 vs 51.6 (76% below sample mean 19.7) | 5.3 vs 60.9 | M VND/ha | | M25 p.178 and Fig. 1 | checked; the low-salinity level is an out-of-range simulation (2.6x the sample mean), use only as an upper bound |
| M25 field exits | 22.3% of fields leave rice in 2 transitions (130 of 865; 172 of 735); 70% still rice after 3 seasons; of non-rice fields 62.5% fallow, 20% other crops, 7.8% shrimp | | % | 2018-20 | M25 p.175-178 | checked |
| M25 exit vs expected profit | probit coefficient 0.171 (0.059) per unit expected IHS-profit via `sal3` (lag 1); 0.0105 (0.0039) continuous; slope steepest below 20 M VND/ha (~sample mean) | | | | M25 Table 3 p.181, Fig. 2 p.182-183 | checked |
| Share of DX fields with salinity problems (self-report) | 9.4% (2017/18), 22.2% (2019/20) | | % | | M25 p.175 | checked |
Caution: F22 non-early profit (3.3 M) vs M22 mild profit (19 M) mixes samples, provinces and years; use only as a severe-to-mild contrast
(severe sold-yield 3.09 vs 6.5 t/ha = about 52% loss, a calibration anchor, not an identified effect).

## Option 2: early sowing (on or before 15 Nov; DCP calendar recommends October sowing, F22 sec. 2)
| Parameter | Value | 2025 VND | Unit | Year | Source | Label |
|---|---|---|---|---|---|---|
| Yield gain in severe year | +2.51 to +2.59 | | t/ha | 2019/20 | F22 abstract, PSM (4 matchers) | checked |
| Season income gain (severe year) | +8.62 to +8.77 | 10.0 to 10.2 | M VND/ha | 2019/20 | F22 abstract | checked |
| Operating cost, early vs non-early | 17.65 vs 13.66 (+4.0) | +4.6 | M VND/ha | 2019/20 | F22 Table 3 | checked (descriptive, includes harvest and drying of extra yield) |
| Early-group revenue, profit | 29.65, 11.99 | 34.4, 13.9 | M VND/ha | 2019/20 | F22 Table 3 | checked |
| Annual income gain | +3.2 to +4.3 (annual profit 27.0 vs 23.4; early planters also forgo some Autumn-Winter crops, F22 sec. 4.4) | | M VND/ha/yr | 2019/20 | F22 Table 4 | checked |
| L25 compliance with official planting window (IV random effects, 775 hh, 874 fields, 2,169 field-seasons, DX 2017/18-2019/20, 7 provinces; instrument = neighbours' compliance, F>290) | all: yield +686.6 kg/ha (SE 177.3), profit +4,402 (1,119) k VND/ha; gated: +913.5 (213.9), +6,883 (1,369); ungated: +194.8 (281.8) n.s., +200.5 (1,891) n.s. | gated 8,253; ungated 240 | kg/ha, k VND/ha | 2017-20 | L25 Table 4 p.985 (text p.984) | checked; association, not causal |
| L25 compliance rate; window | 36.3% of fields (gated 32.3%, ungated 40.7%); window about 2 weeks, set by provincial DARD in April, revised Sep-Oct; ungated fields tend to plant earlier than the window | | | | L25 Table 1-2 p.981-982, p.977, p.979 | checked |
| L25 internal inconsistency | conclusion text says gated gain 771 kg/ha and 6,314 k VND/ha; Table 4 and p.984 text say 913.5 and 6,883 | | | | L25 p.986 vs Table 4 | checked; use Table 4 |
| Effect in a mild season (loss when unnecessary) | no season-specific estimate; ungated 95% CI of the profit effect = 200 +/- 1.96*1,891 = about -3.5 to +3.9 M VND/ha | | | | derived from L25 Table 4 | derived |
| Mild-season bound for gated fields | if the 3-season average gain is 6.9 M and the severe-year gain is 8.7 M (F22, other sample), the other two seasons average at least 6.0 M; no penalty is visible | | M VND/ha | | derived, L25 + F22 | derived, weak |
| Yield penalty of early sowing in mild year | 0 to 10% (shorter-duration variety, floodwater) | | % | | | assumed |
| Extra cost of early sowing in mild year | 0 to +4.6 | | M VND/ha | | upper bound = F22 cost gap | assumed |
| Weakness | F22 early planters self-selected; PSM controls observables only; sample sits in unfavorable (coastal) provinces; no salinity level measured at farm | | | | F22 sec. 3.3 | checked |

## Option 3: salt-tolerant variety (STV)
| Parameter | Value | 2025 VND | Unit | Year | Source | Label |
|---|---|---|---|---|---|---|
| Yield effect, all fields | +364 kg/ha (SE 165) | | kg/ha | 2017-19 | M22 Table 3 panel A (fixed effects) | checked |
| Gross / net revenue effect | +966.8 / +236.0 (net2); not significant | | 000 VND/ha | 2017-19 | M22 Table 3 panel A | checked |
| Price discount | -372 VND/kg (~7%) | -458 | VND/kg | 2017-19 | M22 Table 4 (constant 5.971) | checked |
| Input cost difference | none found | | | | M22 text and Table A.3 | checked |
| Gated vs ungated | STV yield and net2 gain weak (p=.10) on ungated fields only | | | | M22 text, Table 3 panels B-C | checked |
| Trial yield loss under salinity, STV / moderate / sensitive | 10 / 30 / 50% (salinity level not stated) | | % | 2012 | Nhan et al. 2012 cited in M22 | checked (secondary) |
| Loss scaling vs FAO curve (k_STV) | 0.2 (=10/50) to 0.6 | | ratio | | derived from trial ratios | assumed |
| STV adoption | 47% of fields (Table 1 STV mean 0.469); 40% in panel B | | share | 2017-19 | M22 Table 1 | checked |
| January salinity effect in M22 | n.s. (gate inlet gauge is a weak field proxy; measure = share of January days > 3 per mille) | | | | M22 Table 1, Table 3 | checked |

## Option 6: skip the season
| Parameter | Value | Label |
|---|---|---|
| Revenue | 0 | by definition |
| Avoided cost | Cost2 minus fixed part | derived |
| Net return | -F, with F = land rent or fixed cost not avoided; anchor 2.7 M VND/ha/yr (F22 Table 4, 3.15 in 2025 VND) to 0 | anchor checked, F assumed |
| Alternative-use income / exit | not modelled (rice-shrimp and upland crops out of scope) | |

## Loss model (revised 2026-11-02): recommended = direct empirical gauge-to-outcome relation from L25
**Why the change.** L25 regresses field yield and profit on the *February maximum salinity (per mille) at the nearest of 27 Southern
Centre stations* (mean 6.99, SD 5.71; L25 Table 1 p.981, data p.980), the same kind of quantity as our target (gauge seasonal maximum),
separately for gated and ungated fields (Table 4 p.985, N=2,169). This removes the assumed gauge-to-field factor and the g/L-to-ECe chain.
Per-mille is treated as g/L (project assumption, as elsewhere). M25 supports the sign and size order but uses a 3 g/L indicator and a
simulated high-salinity level, so it is a bound, not the main relation.

**Recommended (main) form, per hectare, season with gauge severity S (g/L):**
- `profit_std(S; z) = pi_bar_z - b_z * (S - S_bar_z)`, floored at `-C` (crop failure loses variable cost C, Cost2 = 20.0 M VND/ha in 2025 VND, M22 Table 1);
  `z` in {gated, ungated}. Yield: `Y(S; z) = Y_bar_z - a_z * (S - S_bar_z)`, floored at 0.
- L25 values (SE; k VND = thousand, nominal): profit slope b = -541.7 (71.2) all, -184.4 (79.5) gated, -1,127 (135.8) ungated per g/L;
  yield slope a = -97.3 (11.3), -43.4 (12.7), -197.4 (20.5) kg/ha per g/L. In 2025 VND (x1.197, mean of 2018-20 factors): b = 648, 221, 1,349 k VND/ha per g/L.
  Anchors: pi_bar = 17.86 (gated), 15.87 (ungated) M VND/ha, i.e. 21.4 and 19.0 in 2025 VND; Y_bar = 6,505 and 6,112 kg/ha; S_bar = 7.41 and 6.53 (L25 Table 2 p.982).
- Gated/ungated slope ratio (the data-based sluice factor): 0.22 on yield (delta-method SE 0.07, 95% CI 0.09-0.35), 0.16 on profit (SE 0.07, CI 0.02-0.31).
  Gauge-to-field exposure is then the slope itself; no separate `f`. Sensitivity: gated slope multiplier in {0.1, 0.2, 0.3} x the ungated slope, and each slope +/- 1.96 SE.
- Linearity is assumed over L25's range (mean 7, SD 5.7 per mille); beyond about 14 g/L it is extrapolation. Our stations reach 12-20 g/L, so cap S at 14 (assumed) and run the cap at 10 and 20.
- Check against M25: moving ungated S from 3 to 10 g/L cuts profit by about 9.4 M (L25 slope), about half of mean profit; M25's "76% below mean" at `sal3`=1 is the stronger bound (run as scenario: profit 5.3 M VND/ha whenever S > 3 g/L, ungated).
- Option 2 (early sowing): `profit_early(S) = profit_std(S) + Delta(S)`, `Delta(S) = m` in mild seasons, `Delta_sev` in severe seasons. `Delta_sev` = 10.1 M (F22, 2019/20, 2025 VND) or 8.3 M gated (L25 average); `m` swept:
  gated 0 to +8.3 M, ungated -4.2 to +4.7 M (L25 CI). Break-even P(severe) `p* = -m/(Delta_sev - m)` if `m < 0`, else early sowing is never worse (p* = 0). L25 has no S x compliance interaction, so S-dependence of Delta is an assumption.
- Option 3 (STV): profit_std plus 0.364 t/ha x price, minus 458 VND/kg x yield (M22 Tables 3-4); alternative `k_STV` (0.2-0.6) multiplying the slope; ungated-only benefit is a sensitivity (M22: p=.10).
- Option 6: -F (land rent, 0 to 3.15 M VND/ha). Regret and C/L sweep unchanged (protocol section 8).

**Alternative (kept as sensitivity): FAO yield curve + assumed factor `f`.** `C_field = f*S`, `ECe = 1.56*C_field` (soil water; optional x1.5 for irrigation water, ECe = 1.5 ECw at leaching fraction 15-20%, secondary sources only),
`Y_rel = max(0, 1 - 0.12*max(0, ECe - 3.0))` (FAO Table A1.1: threshold 3.0 dS/m, 12 %/dS/m, rating S, paddy = soil water while submerged; checked). Zero yield at 7.2 g/L field salinity.
Implied f: matching L25's ungated mean loss (about 22% of yield at S = 6.5) gives f of about 0.5; gated about 0.1-0.2. Use f in {0.1, 0.25, 0.5, 0.75} outside, and gated = 0.2 x outside.
**Recommendation:** use the L25 direct relation as the main analysis because it is estimated on the same gauge variable, with real gated/ungated contrast and standard errors, and needs no unsupported unit chain;
use FAO as a stated alternative, mainly for the STV scaling and as a check on shape. Caveats: L25 is an association (IV with a neighbour-compliance instrument),
the salinity coefficient is a between-field random-effects estimate, and 2019/20 is the only extreme year.

## Positioning vs Le Phuong-Dung, Alpizar, Mills 2025 (for the discussion)
- They: ex-post, 3 Dong Xuan seasons (2017/18-2019/20), 775 households, 7 coastal provinces; compare planting inside vs outside the official 2-week window; find +914 kg/ha and +6.9 M VND/ha
  inside gates, nothing significant outside (Table 4). They treat the recommendation as given and call for early-warning systems that use river flow and September-October forecasts (p.986-987).
- We: produce the missing forecast. A probabilistic, pre-season (1 Nov) forecast of severe-season risk at three long-record gauges, evaluated out-of-sample with leave-one-season-out over 21-26 seasons,
  then a decision layer: break-even probabilities, regret and cost-loss over C/L. Added: forecast skill vs climatology, a threshold at which acting pays off, and the share of seasons in which the forecast crosses it.
- Not claimed: causal effects of planting dates (we take their estimates and Ferrer's as scenario inputs), farm-level advice, or season-specific early-sowing payoffs (not identified in any source).
- Link: their gate heterogeneity supplies our inside/outside split and its range from data rather than assumption.

## Parameters still assumptions (to be swept)
1. Severity values `S_sev`, `S_mild` per station (from reference distributions), cap on S (10/14/20), and that per-mille equals g/L.
2. Mild-season early-sowing effect `m` (gated 0 to +8.3, ungated -4.2 to +4.7 M VND/ha) and whether Delta depends on S (no source).
3. Gated slope multiplier (0.1-0.3 of ungated; data CI 0.05-0.35) and each slope within +/- 1.96 SE; the share of fields gated (M22 0.73, L25 0.52; not by station).
4. STV: `k_STV` 0.2-0.6, ungated-only benefit, price discount 7%; no source gives a salinity interaction.
5. Price scenario 4.7-7.0 thousand VND/kg and fixed cost F (0 to 3.15 M VND/ha); year mapping of the deflator.
6. FAO alternative: `f`, soil-water vs irrigation-water reading (factor 1.5).
7. Exit/abandonment (M22 15%, M25 22%, steepest below 20 M VND/ha) is context only, not in returns.

## Biggest uncertainties
- Early-sowing payoff in a mild season: no estimate; the break-even for options 1 vs 2 is driven by it.
- L25 coefficients are associations from 3 seasons with one extreme year; linearity beyond about 14 g/L is an extrapolation; their salinity is the nearest gauge, not station-specific to ours.
- L25 text and Table 4 disagree on the gated compliance effect (771 vs 914 kg/ha); Table 4 used.
- M25 does not state whether `sal3` uses the February maximum or mean; its level effect (-76%) rests on a simulated low-salinity profit of 51.6 M VND/ha.
- Cross-paper heterogeneity in years, provinces and profit definitions (M22 cost-based, L25/M25 net revenue); CPI deflation covers money values only.
