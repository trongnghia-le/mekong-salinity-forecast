# Salinity directions (A/B/C): claim check and prior-art scan

Date of all searches: 2026-11-01. Every DOI below was resolved on the Crossref API (title, venue, year, authors match).
Abstracts come from Crossref, OpenAlex or Semantic Scholar metadata. Publisher pages (ScienceDirect, MDPI) returned
HTTP 403, so no full text was read. Novelty statements are search-scope statements, not facts.

## 1. Claim verification

| # | Claim in report | Source found (DOI) | Verdict |
|---|---|---|---|
| 1 | 2026 LOSO study, 21 stations 2016-2023, R2 0.26 -> 0.60 | Nguyen D.Q.H., Nguyen T.A., Tran T.K. "Physics-aware feature engineering improves spatial transferability of satellite estuarine salinity models: a Mekong Delta evaluation", Remote Sens. Appl. Soc. Environ. 44:102297 (2026), doi:10.1016/j.rsase.2026.102297 (PII S2352938526004301 per Crossref alternative-id). Preprint doi:10.2139/ssrn.6772608 (abstract from Crossref) | CORRECT. Random Forest; HLS + Sentinel-1 + discharge/tide/position interaction features; square-root target. LOSO R2 0.26 (RMSE 5.33 PSU) -> 0.60 (3.93 PSU); leave-one-year-out 0.67; forward-in-time 0.78. "Physics" = engineered features + hydrodynamic pseudo-observations (boundary regularisation). It is NOT a forecast and has no calibrated intervals: it maps dry-season salinity at unmonitored river locations. |
| 2 | 2025 ASR, hourly data at 68 stations + Landsat-8 + ML | Bui Q.D., Luu C., Ha H., Do V.C., Tran T.X. "Surface water salinity modeling for the Mekong Delta of Vietnam using hourly salinity observed data, remote sensing, and machine learning models", Adv. Space Res. 76(3):1417-1437 (2025), doi:10.1016/j.asr.2025.05.055 (PII S0273117725005368) | PARTLY VERIFIED. Paper exists; title confirms hourly data + remote sensing + ML. "68 stations" and "Landsat-8" could NOT be checked (no abstract in Crossref/OpenAlex/S2; publisher 403; web search found nothing). |
| 3 | Water 2026 18(19):2379, XGBoost/LSTM/hybrid, empirical 90% PIs | Cong N.P., Downes N.K., Minh H.V.T., Kumar P., doi:10.3390/w18192379 | CORRECT but narrow: ONE station (Vam Kenh), daily mean, 1-5 days ahead, six dry seasons 2020-2025 (721 obs), test = the 2025 season only. Empirical 90% PIs gave 0.97-1.00 coverage (too wide). The authors say explicitly: not spatial transferability, not operational readiness. |
| 4 | Discover AI 2025, 4 stations, XGBoost/LSTM | Phong N.D., Thang T.D., Giap P.V., Hoat N.V., Tuan T.M., Discov. Artif. Intell. 5:79, doi:10.1007/s44163-025-00336-3 | CORRECT. Hourly, Cau Quan / Tra Vinh / Ben Trai / Tran De, 2015-2020; six models (XGB, GB, SVR, LSTM, RNN, ANN); LSTM and XGB best. Point forecasts only. |
| 5 | 44 stations 1996-2023, RF/SVR, 1-7 days | Le V.Q., Nguyen T.C., Kantoush S.A., Phan C.D., Nguyen T.P.M., Doan V.B., Hue Univ. J. Sci. Nat. Sci. 134(1S-1) (2025), doi:10.26459/hueunijns.v134i1s-1.7876 | FOUND; matches. SVR best at 1-3 d, RF at 4-7 d; lag features 1-60 d; time-series CV. Point forecasts, no transfer test. |
| 6 | Phuong-Dung et al. 2025: refine planting-date advice + integrate with salinity early warning; effects differ inside vs outside gates | Le Phuong-Dung, Alpizar F., Mills B., Agric. Econ. 56(6):976-988, doi:10.1111/agec.70045 | GATE PART CORRECT, EARLY-WARNING PART OVERSTATED. Panel of 775 households 2018-2020: following government planting dates is associated with higher yield/profit ONLY in fields protected by salinity barrier gates; no significant association outside gates. Abstract conclusion: current advice "seem[s] to be tailored to intensive rice production areas protected by salinity barriers"; adaptation information must account for heterogeneity. Early warning appears only as background; "integrate with salinity early warning" is the report's gloss (full text not read). It is an association study (random-effects panel), not causal. |
| 7 | Commun. Earth Environ. 2025, ~25% of paddy loss from salinity and drought | Wang Q. et al., Commun. Earth Environ. 6:503, doi:10.1038/s43247-025-02490-z | CORRECT with a caveat: 25.14% of paddy-field loss EXCLUDING urban conversion comes directly from salinity + drought stress; 74.86% has indirect links mixed with economic drivers. |
| 8 | SIWRR 2024 maps (CGSpace), CS-MAP (CCAFS), ACIAR SLAM/2018/144 | (a) Bui V.C., Tran M.T., Le T.T., Nguyen V.T., Nguyen H.D.H., Nguyen V.H. "Digital salinity maps for crop and forecasted vulnerable areas in the Mekong River Delta", SIWRR, Dec 2024, CC-BY-4.0, https://hdl.handle.net/10568/172467 (district level; ArcGIS web map). (b) "Regional Climate-Smart Maps and Adaptation Plans (CS MAP) for Mekong River Delta", CGSpace 10568/111168 (CCAFS SEA + Dept. of Crop Production; 2020 drought/salinity risk maps for rice). (c) ACIAR SLAM/2018/144, Jul 2019-Jun 2024, lead J. Condon (Charles Sturt Univ.), partner Can Tho Univ.; alternative dry-season crops, mulch, soil sensors: https://www.aciar.gov.au/sites/default/files/2021-09/SLAM-2018-144.pdf | ALL EXIST (from web search snippets; PDFs not read). These are maps and agronomy, not forecast-to-decision models. |

## 2. Prior art closest to directions A and B (all DOIs Crossref-verified)

Direction A (forecast -> farm decision -> value):
1. Tran D.Q., Le K.N., Durand-Morat A., Nguyen N.N.T., Bairagi S.K., Huynh M.V.T., Tran T.V. (2025) "Is it worth it? Land-fallowing and saltwater intrusion control under uncertainty", Sci. Total Environ. 966:178711, doi:10.1016/j.scitotenv.2025.178711. Probabilistic hydro-economic model (hydro-statistical model + inventory theory) for the VMD to 2050. It states that better saltwater-intrusion forecasts are worth USD 47.18-51.37 million per year. **This is the closest work: it already puts a dollar value on salinity forecast accuracy in the VMD.** But it works at delta/policy scale (area to fallow), not farm level; it uses no ML forecasts and no regret or false-safe metrics.
2. Tran D.Q., Le K.N. (2025) "Sea-Level Rise and Saltwater Intrusion: Economic Estimates of Impacts of Nature-Based Mitigation Policies Under Uncertainty", Water 17(9):1355, doi:10.3390/w17091355. Chain of hydrodynamic, statistical, crop and economic models; costs of mitigation under uncertainty.
3. An-Vo D.-A., Radanielson A.M., Mushtaq S., Reardon-Smith K., Hewitt C. (2021) "A framework for assessing the value of seasonal climate forecasting in key agricultural decisions", Clim. Serv. 22:100234, doi:10.1016/j.cliser.2021.100234. Bio-economic value of seasonal PRECIPITATION forecasts for rice sowing windows in the Greater Mekong Region (USD 135-220/ha depending on skill). Same decision (sowing date), different hazard.
4. Le Phuong-Dung, Alpizar, Mills (2025), doi:10.1111/agec.70045. Also Mills B., Ta C., Ta D.P., Nguyen H. (2025) "Salinity inundation, profitability, and rice farming exits in the Mekong Delta of Vietnam", J. Agric. Appl. Econ. Assoc. 4(2):170-186, doi:10.1002/jaa2.70004 (758 households; high salinity cuts profit by > 75%; farmers exit rice when expected profit falls below 20 M VND/ha). Empirical evidence on planting calendars, salinity losses and gate heterogeneity: the inputs a decision model would need.
5. Apel H., Khiem M., Quan N.H., Toan T.Q. (2020) "Brief communication: Seasonal prediction of salinity intrusion in the Mekong Delta", NHESS 20:1609-1616, doi:10.5194/nhess-20-1609-2020. Logistic-regression seasonal forecast (ENSO3.4 or streamflow), ROC > 0.8 up to 9 months ahead. A probabilistic exceedance forecast at the lead time sowing decisions need already exists.

Direction B (unseen-station / calibrated forecasting):
6. Nguyen D.Q.H. et al. (2026), doi:10.1016/j.rsase.2026.102297 (claim 1): LOSO on 21 stations, but for satellite nowcast mapping, not forecasting; no intervals.
7. Cong N.P. et al. (2026), doi:10.3390/w18192379 (claim 3), and Cong N.P., Ty T.V., Duy D.V., Ngoc D.T.H., Downes N.K., Minh H.V.T., Chatterjee A., Chakraborty S., Kumar P. (2026) "Deep Learning-Based Salinity Forecasting in the Vietnamese Mekong Delta: A Cung Hau Estuary Case Study", Water 18(10):1240, doi:10.3390/w18101240 (LSTM at Hung My and Tra Vinh, 1-3 d, under-predicts peaks). Single stations; empirical intervals only.
8. Point-forecast ML papers (no transfer test, no calibrated intervals): doi:10.1007/s44163-025-00336-3; doi:10.26459/hueunijns.v134i1s-1.7876; Nguyen H.D., Dang D.K., Bui Q.-T. (2025) Water Supply 25(2):327-342, doi:10.2166/ws.2025.007 (GRU + metaheuristics, Hau estuary, 1-30 d); Nguyen H.D. (2025) Iran. J. Sci. Technol. Trans. Civ. Eng. 50(4):4305-4323, doi:10.1007/s40996-025-02034-7; Lam V.H. (2023) Res. Crops 24(4), doi:10.31830/2348-7542.2023.roc-1001 (22 stations, remote-sensing regression). A global analogue for estuaries with few stations: Rummel K., Strauss T., Lauer F., Graewe U. (2025) JGR Mach. Learn. Comput. 2(4):e2025JH000768, doi:10.1029/2025jh000768 (LSTM predicts salt-intrusion length in the Weser/Elbe; still works with missing input stations).

Other items seen (not close): Kaveney B. et al. (2023) Agric. Syst. 207:103632, doi:10.1016/j.agsy.2023.103632 (ACIAR review of alternative crops); NuocGPT chatbot blog, doi:10.21955/gatesopenres.1117194.1; SaltGuard, LNCS pp. 160-172 (2026), doi:10.1007/978-981-92-2888-1_13 (no abstract available).

Not found in my searches (OpenAlex, Crossref, arXiv, WebSearch; 2026-11-01):
- a farm-level (field or crop-stage) decision-theoretic evaluation (regret, cost-loss, false-safe rate, value of information) of ML or probabilistic salinity forecasts, in the VMD or in other deltas (Ganges-Brahmaputra, Pearl River);
- conformal prediction applied to estuarine salinity forecasting (WebSearch also found none; nearest are quantile regression and MC dropout for conductivity);
- graph neural networks applied to salinity forecasting (GNNs appear for multi-station water level, e.g. Mach. Learn. Appl. 2026, doi:10.1016/j.mlwa.2026.100971; title only, not read);
- leave-one-province-out or extreme-season-out evaluation of salinity FORECASTS (only the LOSO satellite mapping study of claim 1).

Search caveats: Semantic Scholar returned HTTP 429 to almost every query, even at 8 s spacing (one query succeeded). Europe PMC returned HTTP 503. Vietnamese-language OpenAlex queries return mostly off-topic hits (tourism, medicine). Vietnamese journals (J. Hydro-meteorology, CTU J. Sci., Tap chi KH Bien doi khi hau) contain ML salinity forecasts at single stations (e.g. LSTM at Dai Ngai, 10.36335/vnjhm.2022(740(1)).98-104; not Crossref-checked) and warning-system papers. No forecast-value or decision-optimisation paper was found there. Google Scholar was not queried directly (WebSearch only).

## 3. Groups already working in this space (competitor risk)
- Can Tho University / IGES / UNU (Nguyen Phuoc Cong, Huynh Vuong Thu Minh, Nigel K. Downes, Pankaj Kumar, Tran Van Ty): two 2026 Water salinity-forecast papers within 5 months. Closest to B; they list intervals and transfer as future work.
- Univ. of Arkansas (Dat Q. Tran, Kieu N. Le, A. Durand-Morat, with Tran Van Ty and Huynh Vuong Thu Minh of CTU): probabilistic hydro-economics and forecast value. Closest to A.
- Virginia Tech / Duke (Bradford Mills, Le Phuong-Dung, Francisco Alpizar): 2018-2020 household panel on salinity, planting calendars and gates.
- SIWRR (Tran Minh Tuan, Bui Van Cuong): operational salinity forecasts, 2024 crop salinity maps, the Discover AI paper; holds the station data.
- Huu Duy Nguyen (VNU Hanoi): a series of ML salinity forecast papers. Kantoush / Doan Van Binh (Kyoto / VGU): the 44-station paper.

## 4. Verdict per direction
- A (forecast -> farm decision): PARTLY DONE. Forecast value is already priced at delta scale (Tran et al. 2025), and the value of forecasts for rice sowing is already priced for precipitation (An-Vo et al. 2021). A farm/crop-stage, regret-based evaluation of probabilistic salinity forecasts with gate heterogeneity was not found in my searches. Main risk: no public field-level yield/loss data. The loss function L would come from published relations (Mills 2025, Phuong-Dung 2025) and would be partly assumed.
- B (unseen-station calibrated forecasting): PARTLY DONE. LOSO exists for satellite mapping (R2 0.60), and empirical intervals exist at single stations. A leave-province- or extreme-season-out FORECAST evaluation with conformal coverage across many stations was not found. Main risks: station data (SIWRR / provincial bulletins, 44-68 stations) is not openly downloadable, and the CTU group is moving in this direction.
- C (yield + methane + AWD): not searched in depth (outside this brief). The report's data-risk judgement is plausible: methane ground truth is the bottleneck.

## 5. What a new paper must do to differ
- vs Tran et al. 2025 (STOTEN): farm or crop-stage decisions, not delta-wide fallowing area; use the actual out-of-sample skill of the forecasts at each lead time, not a hypothetical accuracy gain; report regret and false-safe rate.
- vs An-Vo et al. 2021: use salinity exceedance P(S > S_crit) as the hazard, not rainfall terciles; analyse gate-protected and unprotected fields separately.
- vs Apel et al. 2020: probabilities at station or field level, short and seasonal leads, with calibration checked.
- vs Nguyen et al. 2026 (RSASE): forecast t+h, not nowcast maps; calibrated intervals evaluated on held-out stations.
- vs Cong et al. 2026 (both papers): many stations; leave-station/province/extreme-year-out; distribution-free coverage (split or Mondrian conformal); coverage reported for the extreme 2016/2020/2024 seasons.

## 6. Report claims that were wrong or overstated
- Claim 6: "integrate with salinity early warning" is not in the abstract (the gate heterogeneity is correct); the study shows association, not causation.
- Claim 2: "68 stations" and "Landsat-8" are unverified.
- Claim 1: correctly described as transferability, but it is a satellite nowcast; it says nothing about whether forecasts transfer.
- Claim 3: the intervals over-cover (0.97-1.00 at nominal 0.90), at one station and one test season; this is not evidence that calibrated forecasting is solved.
- Claim 7: "~25%" holds only when urban conversion is excluded.
- The report missed the closest prior art for A: Tran et al. 2025 (forecast value USD 47-51 M/yr) and An-Vo et al. 2021.

## 7. Recommendation
Make B the core and add a light A layer. First, a leave-station/province/extreme-season-out benchmark with conformal coverage. Then a simple cost-loss/regret evaluation of the calibrated exceedance probabilities for ONE decision (sowing date of the winter-spring crop), split inside/outside gates. This reuses the conformal experience from Paper 3 and keeps the economics of A modest and honest. Before committing, confirm that station data can be obtained: daily data for 2016-2024 at 20 or more stations, from SIWRR or provincial bulletins. If it cannot, fall back to the data route of claim 1 (satellite + discharge).

## Appendix: query log (engine, date, query, total hits returned by the API; errors recorded as returned)
| Date | Engine | Query | Hits |
|---|---|---|---|
| 2026-11-01 | Crossref | spatial transferability satellite salinity Mekong Delta leave-one-station-out | 27685 |
| 2026-11-01 | Crossref | salinity intrusion Mekong hourly 68 stations Landsat-8 machine learning | 4179545 |
| 2026-11-01 | Crossref | multi-day salinity forecasting XGBoost LSTM hybrid prediction intervals Mekong | 117814 |
| 2026-11-01 | Crossref | salinity forecasting Mekong 44 stations random forest support vector regression 1-7 days | 100813 |
| 2026-11-01 | SemanticScholar | Surface water salinity modeling for the Mekong Delta of Vietnam using hourly salinity observed data, remote sensing, and machine learning models | HTTP Error 429:  |
| 2026-11-01 | OpenAlex | salinity forecasting Mekong Delta 44 stations random forest SVR | 32 |
| 2026-11-01 | OpenAlex | salinity forecast decision support farmers Mekong Delta | 1106 |
| 2026-11-01 | OpenAlex | value of salinity forecast information agriculture Mekong | 2413 |
| 2026-11-01 | OpenAlex | salinity early warning planting calendar rice Mekong Delta | 132 |
| 2026-11-01 | OpenAlex | economic value probabilistic forecast salinity intrusion | 1216 |
| 2026-11-01 | OpenAlex | salinity intrusion decision support system agriculture delta | 7066 |
| 2026-11-01 | OpenAlex | cost-loss model forecast value irrigation sowing decision | 7657 |
| 2026-11-01 | OpenAlex | Bayesian decision analysis saltwater intrusion | 905 |
| 2026-11-01 | OpenAlex | salinity intrusion forecast Ganges Brahmaputra delta decision agriculture | 372 |
| 2026-11-01 | OpenAlex | salinity intrusion Pearl River Estuary forecast machine learning | 142 |
| 2026-11-01 | OpenAlex | graph neural network salinity forecasting estuary | 590 |
| 2026-11-01 | OpenAlex | conformal prediction salinity | 25367 |
| 2026-11-01 | OpenAlex | probabilistic salinity forecast uncertainty estuary machine learning | 537 |
| 2026-11-01 | OpenAlex | salinity prediction unseen stations spatial generalization estuary | 100 |
| 2026-11-01 | OpenAlex | seasonal salinity intrusion forecast Mekong | 1080 |
| 2026-11-01 | OpenAlex | dự báo xâm nhập mặn học máy | 2964 |
| 2026-11-01 | OpenAlex | khuyến nghị lịch thời vụ xâm nhập mặn | 621 |
| 2026-11-01 | OpenAlex | hỗ trợ ra quyết định xâm nhập mặn nông nghiệp | 1352 |
| 2026-11-01 | OpenAlex | giá trị kinh tế của dự báo mặn | 19181 |
| 2026-11-01 | OpenAlex | optimal sowing date salinity risk rice Mekong Delta | 155 |
| 2026-11-01 | OpenAlex | crop calendar salinity intrusion risk model rice growth stage threshold Mekong | 80 |
| 2026-11-01 | OpenAlex | salinity forecast rice farmers decision Vietnam economic benefit | 1257 |
| 2026-11-01 | OpenAlex | transfer learning salinity prediction Mekong stations | 473 |
| 2026-11-01 | OpenAlex | spatiotemporal deep learning salinity intrusion Mekong multi-station | 114 |
| 2026-11-01 | OpenAlex | salinity intrusion prediction Mekong uncertainty quantification quantile | 36 |
| 2026-11-01 | OpenAlex | value of forecast information decision regret agriculture | 6623 |
| 2026-11-01 | OpenAlex | economic value seasonal climate forecast rice planting decision | 17367 |
| 2026-11-01 | OpenAlex | salinity barrier sluice gate operation forecast Mekong optimization | 21 |
| 2026-11-01 | Crossref | value of salinity forecasts for farm decisions | 1039733 |
| 2026-11-01 | Crossref | salinity intrusion forecast decision support rice Mekong Delta | 2002536 |
| 2026-11-01 | Crossref | graph neural network salinity intrusion | 2165036 |
| 2026-11-01 | Crossref | conformal prediction water quality forecasting | 4200576 |
| 2026-11-01 | EuropePMC | salinity intrusion Mekong forecast | HTTP Error 503:  |
| 2026-11-01 | EuropePMC | "saltwater intrusion" forecast agriculture decision | HTTP Error 503:  |
| 2026-11-01 | arXiv | all:salinity AND all:forecast | 28 |
| 2026-11-01 | arXiv | all:salinity AND all:Mekong | 0 |
| 2026-11-01 | arXiv | all:conformal AND all:salinity | 9 |
| 2026-11-01 | OpenAlex | cost-loss salinity forecast | 37068 |
| 2026-11-01 | OpenAlex | forecast-based decision rice planting salinity intrusion optimization Vietnam | 278 |
| 2026-11-01 | OpenAlex | salinity intrusion forecast Bangladesh farmers decision | 1042 |
| 2026-11-01 | OpenAlex | saltwater intrusion forecast water intake decision value | 553 |
| 2026-11-01 | OpenAlex | graph neural network water quality monitoring stations forecasting river network | 6222 |
| 2026-11-01 | OpenAlex | graph neural network Mekong | 1092 |
| 2026-11-01 | OpenAlex | lịch thời vụ né mặn dự báo | 1228 |
| 2026-11-01 | OpenAlex | dự báo độ mặn mô hình LSTM đồng bằng sông Cửu Long | 28 |
| 2026-11-01 | OpenAlex | cảnh báo xâm nhập mặn nông nghiệp đồng bằng sông Cửu Long thời vụ | 1372 |
| 2026-11-01 | OpenAlex | salinity intrusion rice yield loss forecast growth stage damage function Mekong | 238 |
| 2026-11-01 | SemanticScholar | salinity forecast decision support agriculture Mekong Delta | HTTP Error 429:  |
| 2026-11-01 | SemanticScholar | economic value of salinity intrusion forecasts | 258 |
| 2026-11-01 | SemanticScholar | graph neural network salinity prediction | HTTP Error 429:  |
| 2026-11-01 | SemanticScholar | conformal prediction salinity forecasting | HTTP Error 429:  |
| 2026-11-01 | SemanticScholar | leave-one-station-out salinity Mekong | HTTP Error 429:  |
| 2026-11-01 | Crossref | Tran saltwater intrusion Mekong fallowing inventory theory hydro-statistical | 2752341 |
| 2026-11-01 | OpenAlex | saltwater intrusion Mekong hydro-economic probabilistic land fallowing | 5 |
| 2026-11-01 | SemanticScholar | graph neural network salinity prediction | HTTP Error 429:  |
| 2026-11-01 | SemanticScholar | conformal prediction salinity forecasting | HTTP Error 429:  |
| 2026-11-01 | SemanticScholar | salinity forecast decision support agriculture Mekong Delta | HTTP Error 429:  |
| 2026-11-01 | SemanticScholar | leave-one-station-out salinity Mekong | HTTP Error 429:  |
| 2026-11-01 | OpenAlex | graph neural network salinity | 42532 |
| 2026-11-01 | OpenAlex | spatio-temporal graph salinity intrusion estuary forecasting | 144 |
| 2026-11-01 | OpenAlex | salinity prediction intervals estuary calibrated coverage | 1903 |
| 2026-11-01 | OpenAlex | saltwater intrusion early warning decision rice Mekong probabilistic threshold exceedance | 16 |
| 2026-11-01 | WebSearch | 8 queries: ASR 68-station paper (x2), CGSpace SIWRR maps, ACIAR SLAM/2018/144, economic value salinity forecast Mekong (extended), hydro-economic fallowing forecast value, GNN salinity estuary, conformal salinity estuary | n/a (10 links each) |
| 2026-11-01 | WebFetch | sciencedirect.com PII S0273117725005368; mdpi.com 2073-4441/17/9/1355 | HTTP 403 |
