# Dry-season land-use options: data feasibility for a break-even chart (checked 2026-11-01)

Scope: can free, citable numbers support a chart "above which P(severe season) does option X beat option Y"?
Decision support only, not farm advice. Labels: **checked** = I opened the source (or its PDF text); **snippet** = search
snippet only; **nv** = not verified. Conversion: project value 1 g/L ~ 1.56 dS/m; FAO tables are in ECe (saturated soil
extract), not irrigation-water EC (ECw); the two differ (ECe ~ 1.5 x ECw), so g/L at the gauge is NOT ECe. Sources that give
salinity in per mille (‰) are treated as ~ g/L (my assumption, flag in paper). No source below states its own conversion.

## Cross-cutting evidence (rice, delta)

| Item | Value | Source | Label |
|---|---|---|---|
| Rice ECe threshold / slope | 3.0 dS/m, -12 %/dS/m, rating S; "less tolerant during seedling stage"; paddy values refer to soil water while submerged | FAO Irrig. & Drain. Paper 29 rev.1 (Ayers & Westcot 1985), Table, fao.org/4/Y4263E/y4263e0e.htm | checked (via fetch tool) |
| Rice irrigation water / soil limits | yield loss if water EC > 2 dS/m or soil EC > 3 dS/m | MRC BDP Tech Note 4, Environment Assessment (2010) | snippet |
| Sensitive stages | seedling and reproductive; tolerant at germination, active tillering, maturity; the two stages weakly correlated | Review in PMC8519845 (Rice salt tolerance QTL) | snippet |
| Mekong breeding target | EC 4-6 dS/m tolerance needed for salt intrusion before the wet season | Mekong Delta breeding summary, agris.fao.org record 647239e6e17b74d2224eec3a | snippet |
| Panel of 788 households, 7 provinces (Kien Giang, Ca Mau, Bac Lieu, Soc Trang, Tra Vinh, Ben Tre, Tien Giang), Dong Xuan 2017/18 and 2018/19 | mean yield 6.5 t/ha; 73% of fields behind salinity barriers; net revenue excl. family labour ~VND 21 M/ha (~USD 900) per season; 15% of fields not planted to rice next season (abandonment, coastal Ben Tre highest); rice price fell ~14% between years | Mills et al. 2022, Climate and Development, doi:10.1080/17565529.2022.2072800 (open PDF, WUR edepot.wur.nl/571344) | checked (PDF text) |

NOTE: the "Mills et al. 2025" in the brief was not found; the matching paper is Mills et al. 2022 (above). It has no explicit
abandonment threshold, only that falling rice profitability drives exit (probit/IV-probit). Cost totals are in its Table 1
(cost1-cost3 definitions seen; the numeric table was not extracted).

## Option 1: Dong Xuan rice, standard calendar

| Field | Value | Source / label |
|---|---|---|
| Tolerance | 3.0 dS/m ECe, -12 %/dS/m (FAO) | checked |
| Season / window | sowing ~Nov-Dec, harvest ~Feb-Mar (duration in days: nv). Salinity front Jan-Apr hits late vegetative/reproductive stage (Mills describes DX as "immediately prior to the Jan-Apr salinity surge") | checked (Mills) |
| Yield | 6.5 t/ha (7 provinces, 2017/19); Kien Giang Chau Thanh 6.7 t/ha, Can Tho Vinh Thanh ~7.3, An Giang 7.01 (DX 2021-22) | checked (Mills; Nongnghiep news 10/03/2022 via van.nongnghiepmoitruong.vn) |
| Price (farm gate) | VND 5,400-5,850/kg common varieties; RVT 7,000 (DX 2021-22) | checked (news, 2022) |
| Cost | ~VND 27-30 M/ha (Kien Giang, Chau Thanh, DX 2021-22, converted from 2.7-3 M per 1,000 m2); ~VND 40 M/ha (Kien Giang farmer, 2021, snippet) | checked / snippet; news, not survey |
| Profit | ~VND 21 M/ha net excl. family labour (Mills, 2017-19); news says profit "eroded" 2021-22 with no figure | checked |
| Constraints | needs sluice-protected freshwater; low capital; market price risk | Mills |

## Option 2: early-sown DX rice (xuong giong som)

| Field | Value | Source / label |
|---|---|---|
| Definition | sown on or before 15 Nov 2019, last crop of farmer | Ferrer et al. 2022, Economic Analysis and Policy 73:639-652, doi:10.1016/j.eap.2021.12.018 (abstract page checked; full text not) |
| Effect (PSM, 1,176 farmers: 412 early / 764 not; Long An, Kien Giang, Soc Trang; 2019/20, severe salinity year) | season income +VND 8.62-8.77 M/ha; yield +2.51-2.59 t/ha; annual income +VND 3.2-4.3 M/ha | checked (abstract) |
| Costs / risks | abstract reports no costs. Known risks (shorter-duration variety, lower potential yield, floodwater not receded) are NOT quantified in anything I opened | nv |
| Caveat for break-even | the estimate is conditional on a single severe season; there is no estimate for a mild season (the loss when early sowing was unnecessary), which is the term a break-even needs | gap |

## Option 3: salt-tolerant varieties (STV)

| Field | Value | Source / label |
|---|---|---|
| Trial loss under saline conditions | STV -10%, moderately tolerant -30%, sensitive -50% (multi-location Mekong trials; salinity level not given in the Mills text) | Nhan et al. 2012 as cited in Mills 2022 | checked (secondary) |
| Field effect | STV +364 kg/ha yield, but gross/net revenue not significantly different; STV price VND 372/kg (~7%) lower | Mills 2022, Table 3-4 | checked |
| Adoption | 12 of 42 varieties are STV, ~40% of fields (2018 survey, Paik et al. 2020) | Mills | checked (secondary) |
| Named varieties | CLRRI reports OM6976, OM18 tolerant to 2-4 ‰; ST24 ~3%, ST25 ~2% of area; OM6976 "highly tolerant" at 8 dS/m in seedling screen; ST24 yield falls from 2 to 6 ‰ (Summer-Autumn 2023). Tolerance is a seedling-stage test or a breeder claim, not a field-yield curve | Saigon Times (?p=526355, now redirects), sj.agu.edu.vn art. 7983, jad.hcmuaf.edu.vn art. 1119 | snippet |
| ST25 DX price | ~VND 8,000/kg, ~700 kg/cong (7 t/ha) (2025 news) | snippet |
| Gap | no controlled yield-vs-salinity curve per variety at field scale with a stated g/L | gap |

## Option 4: rice-shrimp (tom-lua)

| Field | Value | Source / label |
|---|---|---|
| Profit | Phuoc Long, Bac Lieu: revenue ~VND 340 M/ha/yr, profit ~220 M (40 M rice + 180 M shrimp) (article dated 25/06/2021; a search snippet dated it 2025, check) | van.nongnghiepmoitruong.vn d294916, news | checked |
| Other profit claims | ~VND 90 M/ha/yr Bac Lieu, 130 M An Bien (Kien Giang); farmer "double rice monoculture" vs official "15-30% higher" (contradictory) | VASEP / VietnamNews, snippets | snippet |
| Yield | prawn 250-300 kg/ha/crop; rice 4-4.5 t/ha (Bac Lieu) | VASEP snippet | snippet |
| Relative income | household income 50% higher than 2 rice crops (Smajgl et al. 2015, cited in Mills); shrimp disease can give near-complete loss | checked (secondary) |
| Rice-stage tolerance | rice grown in the wet season in rotation; shrimp uses the saline dry season (salinity range not stated in sources) | nv |
| Constraints | pond conversion capital, brackish water supply, and shrimp leakage harms neighbouring rice; efficiency scores only (technical 0.665, 84 farms, Ca Mau/Kien Giang, doi:10.21608/ejabf.2022.265413) | snippet |
| Gap | no peer-reviewed per-ha cost table opened; conversion cost and conversion time nv | gap |

## Option 5: upland/secondary crops

| Crop | Tolerance (FAO, ECe) | Delta economics | Label |
|---|---|---|---|
| Maize | 1.7 dS/m, -12 %/dS/m (MS) | Soc Trang Long Phu/Tran De trials 2021-23 and 204 households: favourable economics; beetroot best; no VND figures on the page (full text at AgEcon) - Kha et al., Int. J. Agric. Environ. Res. 11(4), ideas.repec.org/a/ags/ijaeri/371459 | tolerance checked; economics abstract only |
| Watermelon | no threshold/slope, rating MS (estimate) | Ben Tre: profit VND 70-150 M/ha/crop (provincial official, news snippet); Soc Trang farmer 6 t from 2,000 m2, profit 6-7 M (no cost basis) | snippet |
| Chili (Capsicum annuum) | 1.5 dS/m, -14 %/dS/m (MS) | Tra Vinh Chau Thanh: 1.5-3x rice profit (DARD claim, snippet) | snippet |
| Mung bean | 1.8 dS/m, -20.7 %/dS/m (S) | no delta numbers found | tolerance checked; economics nv |
| Sesame | rating S, no coefficients | none found | checked / nv |
| Freshwater need / constraints | stored freshwater, drip or hand irrigation, labour, market and price volatility, poor suitability on heavy clay | no number opened | nv |

## Option 6: skip the season

Zero revenue; costs avoided are nearly all variable costs. Fixed costs (land rent/tax, family labour opportunity cost)
are not documented; Mills defines cost1-cost3 so that a rent-inclusive baseline is computable from its data. Label: derived, nv.

## Verdict

- **Ready for a scenario break-even (with stated assumptions):** Options 1 and 2 against each other. Mills 2022 gives
  cost/yield/profit for standard DX, FAO gives the damage curve, Ferrer 2022 gives the effect of early sowing in one severe
  year. Option 6 is a trivial baseline.
- **Partly ready:** Option 3 (STV): yield advantage and price penalty are quantified (+364 kg/ha, -7% price), and an
  approximate trial loss ratio (10/30/50%) exists. Missing: a field yield-salinity curve with units. Option 4: profit headline
  exists but from news; usable only as an upper-end scenario with explicit uncertainty.
- **Not ready:** Option 5 (no peer-reviewed per-ha cost/profit with units; FAO gives tolerance only; watermelon and
  sesame have no coefficients; mung bean has no delta data).
- **Biggest gaps:**
  1. No source links gauge salinity (g/L, 4 and 8 g/L at the river) to field ECe at the intake; the sluice
     split and ECe/ECw conversion must be a swept parameter.
  2. No estimate of the cost of early sowing in a mild year (needed for the "wrong action" side of the break-even).
  3. The costs are from different years and units (2017/19 survey, 2021-22 news). A deflator is needed.
  4. Shrimp/upland crop costs and conversion capital are from news or snippets only.
- **Suggested next steps if the owner wants Option 5 and 4:** read the full texts of Kha et al. (AgEcon Search), Mills Table 1, Ferrer
  et al. full text (the CGIAR/IRRI repository holds it: repository.upv.edu.ph), and the Bac Lieu rice-shrimp papers in Can Tho Univ. J. Sci.

## Top sources

1. Mills et al. 2022, doi:10.1080/17565529.2022.2072800 (open PDF at edepot.wur.nl/571344).
2. Ferrer et al. 2022, doi:10.1016/j.eap.2021.12.018.
3. FAO Irrigation & Drainage Paper 29 rev.1 (Ayers & Westcot 1985), fao.org/4/Y4263E/y4263e0e.htm.
4. Kha et al., Int. J. Agric. Environ. Res. 11(4), ideas.repec.org/a/ags/ijaeri/371459.
5. Nongnghiep news 10/03/2022 (DX 2021-22 costs, prices) and 25/06/2021 (Bac Lieu rice-shrimp).

## Controller correction (01/11/2026)
- "Mills et al. 2025" DOES exist and was missed by this search: Mills B., Ta C., Ta D.P., Nguyen H. (2025) "Salinity
  inundation, profitability, and rice farming exits in the Mekong Delta of Vietnam", J. Agric. Appl. Econ. Assoc.
  4(2):170-186, doi:10.1002/jaa2.70004 (758 households; high salinity cuts profit by > 75%; source:
  docs/background/salinity_novelty.md row 26). It is the planned source for the profit-loss relation and rice exits;
  Mills et al. 2022 (above) is an additional source, not a replacement. Read its full text before use.
- Closest prior art for the sowing layer: Le Phuong-Dung, Alpizar, Mills (2025) Agric. Econ. 56(6):976-988,
  doi:10.1111/agec.70045 (following government planting dates pays off only inside salinity gates).
