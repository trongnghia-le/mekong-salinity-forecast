# Layer-A decision parameters (compiled 2026-11-01)

Scenario inputs for the regret and break-even analysis (protocol section 8). Not farm advice.
Labels: **checked** = value read in full text (page/table given); **abstract** = abstract or search snippet only;
**nf** = not found; **assumed** = to be swept. Full texts read (local, gitignored, `data/raw/decision_papers/`): Mills et al. 2022,
Ferrer et al. 2022. Mills et al. 2025 (J. Agric. Appl. Econ. Assoc., Wiley) and Le et al. 2025 (Agric. Econ., Wiley) returned
403 / Cloudflare to automated fetch; not worked around, so abstract only (Mills 2025 is CC BY per Crossref; the owner can
download the PDF in a browser and place it in `data/raw/decision_papers/`).
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
| Exit vs profit and salinity | high salinity cuts profit by >75%; exit rises when expected profit < 20 M VND/ha | | | 2025 | M25 abstract; coefficients not read | abstract |
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
| Effect in a mild season (loss when unnecessary) | nf | | | | F22 covers one severe year only | nf, assumed |
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

## Loss model (proposed, exact form)
Yield relative to potential for option k in a season with gauge seasonal severity S (g/L, from the forecast target scale):
- Field water salinity: `C_field = f * S` (g/L), `f` = field-exposure factor (swept, below).
- Field soil-water EC: project conversion 1 g/L = 1.56 dS/m; treat `C_field` as soil-water EC (FAO paddy
  footnote: values refer to soil water while submerged), so `ECe = 1.56 * C_field`. Under this main reading the 1.5 ECe/ECw factor is NOT applied; the alternative
  reading (irrigation water, ECe = 1.5 ECw, leaching fraction 15-20%) is run as sensitivity: `ECe = 1.5 * 1.56 * C_field`.
- Relative yield: `Y_rel = max(0, 1 - k_v * 0.12 * max(0, ECe - 3.0))`, `k_v` = 1 (standard), `k_STV` in [0.2, 0.6] (option 3).
  [FAO Table A1.1: threshold 3.0 dS/m, slope 12 per cent per dS/m, rating S, grain yield. checked]
  Main reading: threshold 3.0 dS/m = 1.92 g/L, zero yield at 11.3 dS/m = 7.2 g/L field. Alternative: threshold 1.28 g/L, zero yield at 4.8 g/L.
- Option 2 (early sowing): the salinity front arrives after the sensitive reproductive stage; model as `C_field_early = f * S * (1 - e)`, `e` in [0.3, 0.7] (assumed;
  calibrated so that the severe-year gain matches F22 +2.5 t/ha, i.e. about +0.4 of mean yield). Not identified by any source beyond F22's average effect.
- Net return: `pi_k = P * Y0 * Y_rel * (1 - d_k) - C_k` where `Y0` = 6.5 t/ha potential (M22), `P` price, `d_2` mild-year early-sowing penalty, `d_3` = STV price discount 7%,
  `C_k` as tables above (2025 VND), option 3 yield bonus +0.364 t/ha is NOT added on top (the k_STV scaling already carries the benefit; avoid double counting).
- Seasonal outcome: severe season = S_sev (upper-half draw), non-severe = S_mild, from the station reference distributions in protocol section 8; expected
  return `E[pi_k] = p * pi_k(S_sev) + (1-p) * pi_k(S_mild)`; break-even `p*` between options i and j solves `E[pi_i] = E[pi_j]` (linear in p, closed form).
- Regret of acting on the forecast: realised return of the best option given the realised season minus the option chosen from the issued P; sweep C/L over [0.1, 0.9].

## Gauge-to-field exposure factor `f` (swept)
No source links gauge salinity to field salinity. Evidence for the range: (i) station median annual max is 8.55 and 9.0 g/L (protocol section 8), and
the FAO curve reaches zero yield at 7.2 g/L field salinity, so f = 1 would give near-total loss every year, contradicting M22 (6.5 t/ha with 73% gated)
and F22 (about 52% loss in the worst year); (ii) M22 found gate-inlet salinity a weak proxy for field exposure; (iii) ungated fields exit 8 pp more (M22 Table 5).
Proposed sweep: inside sluice systems `f` in {0, 0.1, 0.25, 0.5}; outside `f` in {0.25, 0.5, 0.75, 1.0}. Main run: inside 0.1, outside 0.5.
Calibration check (assumed, to run): choose outside `f` so the model reproduces about 50% loss in 2019-20 (F22 anchor) with the 2020 gauge maxima.
L25 (inside vs outside gate planting-date payoffs) not read; use it to narrow the range once its full text is available.

## Parameters still assumptions (to be swept)
1. `f` inside/outside gates, and the ECe reading (soil water vs irrigation water, factor 1.5).
2. Mild-year cost and yield penalty of early sowing (`d_2`, extra cost 0 to 4.6 M VND/ha) and early-sowing shift `e`.
3. `k_STV` (0.2 to 0.6) and the STV price discount (7% from M22; varieties such as ST24/ST25 sell at higher price, snippets only).
4. Price scenario `P` (M22: 5.45 and falling 14% between years; F22: 5.34 in 2019/20): use 4.7 to 7.0 thousand VND/kg (assumed bound).
5. Fixed cost F for option 6 (0 to 3.15 M VND/ha) and the mapping of profit measure (net2 vs net3).
6. Severe-season severity values `S_sev`, `S_mild` per station (from reference medians; upper tercile as sensitivity).
7. Exit/abandonment (M22: 15%; M25 threshold 20 M VND/ha) is reported as context, not entered in returns.

## Biggest uncertainties
- M25 and L25 full texts unread (403): profit-vs-salinity coefficients, salinity definition, and inside/outside gate planting-date effect are unchecked.
- F22 gives one severe year, no mild-year contrast, and its cost gap includes harvest of extra yield.
- Every number comes from a different year, province mix and measure; CPI deflation covers costs only.
- Unit chain gauge g/L -> field dS/m is unsupported by any source; the main conclusions must be read as sensitivity over `f`.
- Observation for the log: Cloudflare and 403 on Wiley blocked two key papers; a browser download by the owner would close the gap.
