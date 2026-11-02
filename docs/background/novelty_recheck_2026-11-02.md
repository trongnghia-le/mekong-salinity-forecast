# Novelty re-check before submission (Climate Services), 02/11/2026

All searches below ran on 2026-11-02. They repeat and extend the search of 2026-11-01 (docs/background/salinity_novelty.md).
Every novelty statement here describes the scope of these searches. None is a statement of fact about the literature.

**How works were verified.** A work counts as verified if its record was opened on 02/11/2026 through one of these:
- the OpenAlex single-work endpoint, the Crossref `/works/<doi>` endpoint, the Zenodo records API or the arXiv API;
- for the one item without a DOI, the web page itself (marked "page opened").

Only abstracts and record metadata were read. The exception is the README of Zenodo record 10.5281/zenodo.23497554, a small text file that was downloaded and read.

**What could not be searched, or not fully:**
- **OpenAlex.** After about 80 list requests (log rows 1-48 plus the author and citation calls), list and search queries returned HTTP 429. The message said the free daily budget for this IP address was used up and would reset at midnight UTC. A free API key needs an email address, which the project rules forbid, so no key was requested. As a result:
  - forward-citation checks ran only for Apel et al. 2020;
  - the citation checks for Tran 2025, An-Vo 2021, Cong 2026 (both papers), Nguyen 2026, Le 2025, Mills 2025 and Rummel 2025 failed;
  - the author watch stopped after Apel.

  Single-record lookups continued to work. **Rerun these citation checks before submission.**
- **Semantic Scholar.** HTTP 429 on all 8 queries, including at 15 s spacing.
- **Blocked pages.** The IGES publication page (iges.or.jp) returned HTTP 403, and the Chesapeake STAC PDF exceeded the fetch size limit. No workaround was tried.
- **Not used.** Google Scholar was reached only through web-search results. Europe PMC worked this time (it returned HTTP 503 on 01/11).

**Request settings.** User-Agent `mekong-salinity-research/0.1`, TLS verification on, no email address in any request. The scripts are in the session scratchpad and are not part of the repository.

## 0. Novelty sentences in the manuscript (as of 02/11/2026; files are being edited)

| Id | File:line | Exact text |
|---|---|---|
| S1 | abstract.tex:2-4 | "We built a pre-registered benchmark from 50 public bulletins of the National Center for Hydro-Meteorological Forecasting (NCHMF) at 28 stations, scored against the official forecast." |
| S2 | highlights.tex:2 | "Pre-registered benchmark of dekadal salinity forecasts at 28 Mekong Delta stations" |
| S3 | 01_introduction.tex:21-27 | "Machine-learning forecasts of salinity in the delta have multiplied, but they are point forecasts at one or a few stations, without a test at stations or seasons outside the training data [...] None of these studies uses the official forecast as a benchmark." |
| S4 | 01_introduction.tex:32-36 | "In our searches (OpenAlex, Crossref, arXiv and web search, 1 November 2026) we did not find a multi-station salinity forecast benchmarked against the official forecast, conformal prediction applied to estuarine salinity forecasting, or a cost--loss evaluation of probabilistic salinity forecasts for a farm decision. These are statements about the scope of our searches, not claims that no such work exists." |
| S5 | 01_introduction.tex:41-48 | Contributions 1-4: "A public, pre-registered benchmark [...]"; "Conformalized quantile forecasts [...] tested under forward-in-time, leave-station-out and leave-province-out designs"; "The relative economic value [...] of calibrated exceedance probabilities against the official deterministic forecast"; "A light seasonal layer [...] with break-even probabilities for crop options." |
| S6 | 07_conclusions.tex:3 | "We built a pre-registered benchmark of dekadal maximum salinity forecasts at 28 stations [...]" |

Claims tested, mapped to these sentences:
- **C1** multi-station forecast benchmarked against the official forecast (S1, S4, S5.1);
- **C2** conformal intervals for salinity, tested at held-out stations and provinces (S4, S5.2);
- **C3** cost/loss value (relative economic value, REV) of probabilistic forecasts against the deterministic official forecast (S4, S5.3);
- **C4** seasonal severe-season forecast linked to the value of the sowing decision and break-even probabilities (S4, S5.4);
- **C5** pre-registered protocol (S1, S2, S5.1, S6).

## 1. Search log

**How to read the columns.**
- **Hits screened:** "total" is the count the API reported. Titles of the top N records, by relevance, were screened by hand.
- **Relevant hits:** screened records that appear in Section 2 or 3, or in the closest-work list of salinity_novelty.md. They were counted against a fixed list of DOIs (the logtable script), not by eye.
- **Rows by source:** OpenAlex 1-48; Crossref from 2024-01-01, 49-65; arXiv 66-73 (no date filter); Semantic Scholar 74-81; Crossref from 2023-01-01, 82-109 and 113-136 (82-94 restricted to preprint and repository DOI prefixes: EarthArXiv 10.31223, ESS Open Archive/Authorea 10.22541, Copernicus/EGU 10.5194, SSRN 10.2139, Research Square 10.21203, Preprints.org 10.20944, Zenodo 10.5281); Europe PMC 110-112; rows 137 onward are author watch, citation, repository and web searches. The 2023 window catches older works that might pre-empt a claim.
- **Reruns of 01/11 queries:** rows 1-14 rerun 14 of the 01/11 OpenAlex queries. The other 01/11 OpenAlex queries could not be rerun because of the HTTP 429 limit.

| # | Date | Engine / API | Exact query | Hits screened | Relevant hits |
|---|---|---|---|---|---|
| 1 | 2026-11-02 | OpenAlex /works (from 2024-01-01) | salinity forecast decision support farmers Mekong Delta | 348 total; top 25 screened | 5 |
| 2 | 2026-11-02 | OpenAlex /works (from 2024-01-01) | value of salinity forecast information agriculture Mekong | 741 total; top 25 screened | 6 |
| 3 | 2026-11-02 | OpenAlex /works (from 2024-01-01) | salinity early warning planting calendar rice Mekong Delta | 35 total; top 25 screened | 1 |
| 4 | 2026-11-02 | OpenAlex /works (from 2024-01-01) | economic value probabilistic forecast salinity intrusion | 414 total; top 25 screened | 1 |
| 5 | 2026-11-02 | OpenAlex /works (from 2024-01-01) | cost-loss salinity forecast | 11623 total; top 25 screened | 0 |
| 6 | 2026-11-02 | OpenAlex /works (from 2024-01-01) | conformal prediction salinity | 5970 total; top 25 screened | 2 |
| 7 | 2026-11-02 | OpenAlex /works (from 2024-01-01) | probabilistic salinity forecast uncertainty estuary machine learning | 273 total; top 25 screened | 0 |
| 8 | 2026-11-02 | OpenAlex /works (from 2024-01-01) | salinity prediction unseen stations spatial generalization estuary | 63 total; top 25 screened | 1 |
| 9 | 2026-11-02 | OpenAlex /works (from 2024-01-01) | seasonal salinity intrusion forecast Mekong | 361 total; top 25 screened | 5 |
| 10 | 2026-11-02 | OpenAlex /works (from 2024-01-01) | salinity intrusion prediction Mekong uncertainty quantification quantile | 17 total; top 17 screened | 1 |
| 11 | 2026-11-02 | OpenAlex /works (from 2024-01-01) | spatiotemporal deep learning salinity intrusion Mekong multi-station | 65 total; top 25 screened | 3 |
| 12 | 2026-11-02 | OpenAlex /works (from 2024-01-01) | salinity prediction intervals estuary calibrated coverage | 390 total; top 25 screened | 0 |
| 13 | 2026-11-02 | OpenAlex /works (from 2024-01-01) | saltwater intrusion early warning decision rice Mekong probabilistic threshold exceedance | 9 total; top 9 screened | 0 |
| 14 | 2026-11-02 | OpenAlex /works (from 2024-01-01) | optimal sowing date salinity risk rice Mekong Delta | 31 total; top 25 screened | 0 |
| 15 | 2026-11-02 | OpenAlex /works (from 2024-01-01) | dự báo xâm nhập mặn học máy | 1431 total; top 25 screened | 0 |
| 16 | 2026-11-02 | OpenAlex /works (from 2024-01-01) | dự báo xâm nhập mặn xác suất | 982 total; top 25 screened | 0 |
| 17 | 2026-11-02 | OpenAlex /works (from 2024-01-01) | dự báo mặn học máy đồng bằng sông Cửu Long | 3043 total; top 25 screened | 0 |
| 18 | 2026-11-02 | OpenAlex /works (from 2024-01-01) | khoảng tin cậy dự báo độ mặn | 5226 total; top 25 screened | 0 |
| 19 | 2026-11-02 | OpenAlex /works (from 2024-01-01) | dự báo độ mặn lớn nhất tuần | 6915 total; top 25 screened | 0 |
| 20 | 2026-11-02 | OpenAlex /works (from 2024-01-01) | đánh giá chất lượng dự báo mặn Trung tâm Dự báo khí tượng thủy văn quốc gia | 2716 total; top 25 screened | 0 |
| 21 | 2026-11-02 | OpenAlex /works (from 2024-01-01) | salinity forecast Mekong Delta national hydro-meteorological forecasting center verification | 39 total; top 25 screened | 1 |
| 22 | 2026-11-02 | OpenAlex /works (from 2024-01-01) | dekadal salinity forecast | 7 total; top 7 screened | 0 |
| 23 | 2026-11-02 | OpenAlex /works (from 2024-01-01) | 10-day maximum salinity forecast Mekong | 352 total; top 25 screened | 2 |
| 24 | 2026-11-02 | OpenAlex /works (from 2024-01-01) | operational salinity forecast verification benchmark persistence | 392 total; top 25 screened | 0 |
| 25 | 2026-11-02 | OpenAlex /works (from 2024-01-01) | conformal prediction hydrology | 2167 total; top 25 screened | 1 |
| 26 | 2026-11-02 | OpenAlex /works (from 2024-01-01) | conformal prediction water quality | 27326 total; top 25 screened | 3 |
| 27 | 2026-11-02 | OpenAlex /works (from 2024-01-01) | conformal prediction streamflow forecasting | 462 total; top 25 screened | 2 |
| 28 | 2026-11-02 | OpenAlex /works (from 2024-01-01) | conformalized quantile regression environmental forecasting | 176 total; top 25 screened | 0 |
| 29 | 2026-11-02 | OpenAlex /works (from 2024-01-01) | relative economic value salinity | 63745 total; top 25 screened | 0 |
| 30 | 2026-11-02 | OpenAlex /works (from 2024-01-01) | relative economic value water quality forecast | 67167 total; top 25 screened | 0 |
| 31 | 2026-11-02 | OpenAlex /works (from 2024-01-01) | salinity forecast value sowing date | 1071 total; top 25 screened | 0 |
| 32 | 2026-11-02 | OpenAlex /works (from 2024-01-01) | planting calendar salinity forecast value | 1032 total; top 25 screened | 1 |
| 33 | 2026-11-02 | OpenAlex /works (from 2024-01-01) | seasonal forecast salinity intrusion ENSO Mekong logistic | 4 total; top 4 screened | 0 |
| 34 | 2026-11-02 | OpenAlex /works (from 2024-01-01) | pre-registered forecast evaluation hydrology | 1464 total; top 25 screened | 0 |
| 35 | 2026-11-02 | OpenAlex /works (from 2024-01-01) | preregistration hydrology forecasting study | 5 total; top 5 screened | 0 |
| 36 | 2026-11-02 | OpenAlex /works (from 2024-01-01) | salinity intrusion forecasting Red River delta machine learning | 317 total; top 25 screened | 4 |
| 37 | 2026-11-02 | OpenAlex /works (from 2024-01-01) | salinity forecast Ganges Brahmaputra probabilistic | 61 total; top 25 screened | 0 |
| 38 | 2026-11-02 | OpenAlex /works (from 2024-01-01) | salinity intrusion Pearl River estuary probabilistic forecast | 28 total; top 25 screened | 0 |
| 39 | 2026-11-02 | OpenAlex /works (from 2024-01-01) | saltwater intrusion Yangtze estuary forecast machine learning uncertainty | 25 total; top 25 screened | 1 |
| 40 | 2026-11-02 | OpenAlex /works (from 2024-01-01) | salinity intrusion Chao Phraya forecast | 54 total; top 25 screened | 2 |
| 41 | 2026-11-02 | OpenAlex /works (from 2024-01-01) | salinity Irrawaddy Ayeyarwady delta forecast | 5 total; top 5 screened | 0 |
| 42 | 2026-11-02 | OpenAlex /works (from 2024-01-01) | salt intrusion Rhine-Meuse forecast probabilistic | 25 total; top 25 screened | 1 |
| 43 | 2026-11-02 | OpenAlex /works (from 2024-01-01) | Sacramento San Joaquin delta salinity machine learning emulator uncertainty | 3 total; top 3 screened | 0 |
| 44 | 2026-11-02 | OpenAlex /works (from 2024-01-01) | salinity intrusion Cambodia Mekong forecast | 115 total; top 25 screened | 4 |
| 45 | 2026-11-02 | OpenAlex /works (from 2024-01-01) | salinity forecast leave-one-station-out | 1671 total; top 25 screened | 1 |
| 46 | 2026-11-02 | OpenAlex /works (from 2024-01-01) | estuarine salinity machine learning prediction uncertainty quantification | 990 total; top 25 screened | 2 |
| 47 | 2026-11-02 | OpenAlex /works (from 2024-01-01) | salinity Mekong Delta deep learning forecasting 2026 | 122 total; top 25 screened | 2 |
| 48 | 2026-11-02 | OpenAlex /works (from 2024-01-01) | saltwater intrusion forecast economic value | 1317 total; top 25 screened | 1 |
| 49 | 2026-11-02 | Crossref /works (from 2024-01-01) | conformal prediction salinity forecasting | 327187 total; top 20 screened | 0 |
| 50 | 2026-11-02 | Crossref /works (from 2024-01-01) | conformal prediction intervals salinity estuary | 272383 total; top 20 screened | 1 |
| 51 | 2026-11-02 | Crossref /works (from 2024-01-01) | salinity forecast Mekong Delta official forecast benchmark | 67897 total; top 20 screened | 2 |
| 52 | 2026-11-02 | Crossref /works (from 2024-01-01) | salinity forecast relative economic value cost-loss | 653321 total; top 20 screened | 1 |
| 53 | 2026-11-02 | Crossref /works (from 2024-01-01) | probabilistic salinity intrusion forecast exceedance probability | 80144 total; top 20 screened | 1 |
| 54 | 2026-11-02 | Crossref /works (from 2024-01-01) | seasonal salinity forecast Mekong sowing | 51123 total; top 20 screened | 1 |
| 55 | 2026-11-02 | Crossref /works (from 2024-01-01) | salinity intrusion forecast Mekong machine learning 2026 | 9282302 total; top 20 screened | 5 |
| 56 | 2026-11-02 | Crossref /works (from 2024-01-01) | dự báo xâm nhập mặn | 4644 total; top 20 screened | 0 |
| 57 | 2026-11-02 | Crossref /works (from 2024-01-01) | xâm nhập mặn học máy dự báo đồng bằng sông Cửu Long | 13631 total; top 20 screened | 0 |
| 58 | 2026-11-02 | Crossref /works (from 2024-01-01) | salinity prediction leave-one-station-out cross-validation | 841915 total; top 20 screened | 0 |
| 59 | 2026-11-02 | Crossref /works (from 2024-01-01) | salinity forecasting quantile regression prediction intervals | 368355 total; top 20 screened | 0 |
| 60 | 2026-11-02 | Crossref /works (from 2024-01-01) | saltwater intrusion forecast value decision farmers | 471876 total; top 20 screened | 0 |
| 61 | 2026-11-02 | Crossref /works (from 2024-01-01) | pre-registered protocol forecast verification environmental | 675329 total; top 20 screened | 0 |
| 62 | 2026-11-02 | Crossref /works (from 2024-01-01) | salinity Mekong conformal | 19932 total; top 20 screened | 8 |
| 63 | 2026-11-02 | Crossref /works (from 2024-01-01) | salinity reconstruction Mekong prediction intervals imputation | 349432 total; top 20 screened | 7 |
| 64 | 2026-11-02 | Crossref /works (from 2024-01-01) | forecast value planting date decision seasonal forecast rice cost-loss | 20931 total; top 20 screened | 1 |
| 65 | 2026-11-02 | Crossref /works (from 2024-01-01) | value of seasonal forecasts sowing date rice Vietnam | 282816 total; top 20 screened | 0 |
| 66 | 2026-11-02 | arXiv API | all:salinity AND all:forecast | 28 total; top 28 screened | 0 |
| 67 | 2026-11-02 | arXiv API | all:salinity AND all:Mekong | 0 total; top 0 screened | 0 |
| 68 | 2026-11-02 | arXiv API | all:conformal AND all:salinity | 9 total; top 9 screened | 0 |
| 69 | 2026-11-02 | arXiv API | all:conformal AND all:hydrolog* | 2 total; top 2 screened | 0 |
| 70 | 2026-11-02 | arXiv API | all:"saltwater intrusion" | 9 total; top 9 screened | 0 |
| 71 | 2026-11-02 | arXiv API | all:"salt intrusion" | 4 total; top 4 screened | 0 |
| 72 | 2026-11-02 | arXiv API | all:conformal AND all:"water quality" | 1 total; top 1 screened | 0 |
| 73 | 2026-11-02 | arXiv API | all:"relative economic value" AND all:forecast | 0 total; top 0 screened | 0 |
| 74 | 2026-11-02 | Semantic Scholar API | conformal prediction salinity forecasting | HTTP Error 429:  (0 screened) | 0 |
| 75 | 2026-11-02 | Semantic Scholar API | salinity forecast Mekong Delta probabilistic | HTTP Error 429:  (0 screened) | 0 |
| 76 | 2026-11-02 | Semantic Scholar API | economic value of salinity intrusion forecasts | HTTP Error 429:  (0 screened) | 0 |
| 77 | 2026-11-02 | Semantic Scholar API | leave-one-station-out salinity Mekong | HTTP Error 429:  (0 screened) | 0 |
| 78 | 2026-11-02 | Semantic Scholar API | salinity forecast sowing decision value | HTTP Error 429:  (0 screened) | 0 |
| 79 | 2026-11-02 | Semantic Scholar API | conformal prediction salinity | HTTP Error 429:  (0 screened) | 0 |
| 80 | 2026-11-02 | Semantic Scholar API | salinity forecast official forecast benchmark Mekong | HTTP Error 429:  (0 screened) | 0 |
| 81 | 2026-11-02 | Semantic Scholar API | relative economic value salinity forecast | HTTP Error 429:  (0 screened) | 0 |
| 82 | 2026-11-02 | Crossref /works (from 2023-01-01), DOI prefix 10.31223 | salinity forecast | 28 total; top 20 screened | 0 |
| 83 | 2026-11-02 | Crossref /works (from 2023-01-01), DOI prefix 10.31223 | salt intrusion estuary | 39 total; top 20 screened | 0 |
| 84 | 2026-11-02 | Crossref /works (from 2023-01-01), DOI prefix 10.31223 | conformal prediction hydrology | 139 total; top 20 screened | 0 |
| 85 | 2026-11-02 | Crossref /works (from 2023-01-01), DOI prefix 10.22541 | salinity forecast estuary | 213 total; top 20 screened | 0 |
| 86 | 2026-11-02 | Crossref /works (from 2023-01-01), DOI prefix 10.22541 | salt intrusion machine learning | 1881 total; top 20 screened | 0 |
| 87 | 2026-11-02 | Crossref /works (from 2023-01-01), DOI prefix 10.22541 | conformal prediction | 624 total; top 20 screened | 0 |
| 88 | 2026-11-02 | Crossref /works (from 2023-01-01), DOI prefix 10.5194 | salinity intrusion forecast | 1156 total; top 20 screened | 0 |
| 89 | 2026-11-02 | Crossref /works (from 2023-01-01), DOI prefix 10.5194 | salt intrusion probabilistic forecast | 1862 total; top 20 screened | 0 |
| 90 | 2026-11-02 | Crossref /works (from 2023-01-01), DOI prefix 10.5194 | economic value forecast cost-loss hydrological | 5136 total; top 20 screened | 0 |
| 91 | 2026-11-02 | Crossref /works (from 2023-01-01), DOI prefix 10.2139 | salinity forecast Mekong | 1690 total; top 20 screened | 2 |
| 92 | 2026-11-02 | Crossref /works (from 2023-01-01), DOI prefix 10.21203 | salinity forecast Mekong | 480 total; top 20 screened | 1 |
| 93 | 2026-11-02 | Crossref /works (from 2023-01-01), DOI prefix 10.20944 | salinity forecast Mekong | 153 total; top 20 screened | 0 |
| 94 | 2026-11-02 | Crossref /works (from 2023-01-01), DOI prefix 10.5281 | salinity Mekong forecast | 0 total; top 0 screened | 0 |
| 95 | 2026-11-02 | Crossref /works (from 2023-01-01) | saltwater intrusion forecast Red River Delta Vietnam | 305284 total; top 20 screened | 0 |
| 96 | 2026-11-02 | Crossref /works (from 2023-01-01) | salinity intrusion forecasting Ganges Brahmaputra Meghna delta machine learning | 1469103 total; top 20 screened | 0 |
| 97 | 2026-11-02 | Crossref /works (from 2023-01-01) | salt intrusion forecast Pearl River estuary machine learning probabilistic | 1538191 total; top 20 screened | 1 |
| 98 | 2026-11-02 | Crossref /works (from 2023-01-01) | saltwater intrusion Yangtze estuary forecast uncertainty | 122433 total; top 20 screened | 0 |
| 99 | 2026-11-02 | Crossref /works (from 2023-01-01) | salinity forecast Chao Phraya | 196763 total; top 20 screened | 1 |
| 100 | 2026-11-02 | Crossref /works (from 2023-01-01) | salinity intrusion Ayeyarwady delta | 65990 total; top 20 screened | 4 |
| 101 | 2026-11-02 | Crossref /works (from 2023-01-01) | salt intrusion forecast Rhine-Meuse delta machine learning | 1444807 total; top 20 screened | 2 |
| 102 | 2026-11-02 | Crossref /works (from 2023-01-01) | Sacramento-San Joaquin Delta salinity machine learning | 1445953 total; top 20 screened | 0 |
| 103 | 2026-11-02 | Crossref /works (from 2023-01-01) | salinity intrusion forecast Cambodia Mekong Bassac | 56078 total; top 20 screened | 4 |
| 104 | 2026-11-02 | Crossref /works (from 2023-01-01) | forecast value sowing decision seasonal forecast cost-loss regret rice | 27112 total; top 20 screened | 1 |
| 105 | 2026-11-02 | Crossref /works (from 2023-01-01) | economic value probabilistic hydrological forecast cost-loss relative economic value 2025 | 665499 total; top 20 screened | 0 |
| 106 | 2026-11-02 | Crossref /works (from 2023-01-01) | conformal prediction streamflow | 317996 total; top 20 screened | 1 |
| 107 | 2026-11-02 | Crossref /works (from 2023-01-01) | conformal prediction water quality forecasting river | 1332516 total; top 20 screened | 1 |
| 108 | 2026-11-02 | Crossref /works (from 2023-01-01) | operational salinity forecast skill persistence benchmark | 127947 total; top 20 screened | 0 |
| 109 | 2026-11-02 | Crossref /works (from 2023-01-01) | Mekong salinity probabilistic forecast | 55210 total; top 20 screened | 3 |
| 110 | 2026-11-02 | Europe PMC REST (2023-2026) | salinity AND forecast AND Mekong | 16 total; top 16 screened | 1 |
| 111 | 2026-11-02 | Europe PMC REST (2023-2026) | conformal AND salinity | 141 total; top 25 screened | 0 |
| 112 | 2026-11-02 | Europe PMC REST (2023-2026) | saltwater intrusion AND forecast AND economic value | 43 total; top 25 screened | 2 |
| 113 | 2026-11-02 | Crossref /works (from 2023-01-01) | Machine learning prediction of saltwater intrusion to support coastal water resource management | 580233 total; top 20 screened | 1 |
| 114 | 2026-11-02 | Crossref /works (from 2023-01-01) | An-Vo seasonal climate forecast value rice Vietnam sowing | 609920 total; top 20 screened | 2 |
| 115 | 2026-11-02 | Crossref /works (from 2023-01-01) | value of seasonal forecasts rice Mekong Delta farmers decision bio-economic | 29719 total; top 20 screened | 0 |
| 116 | 2026-11-02 | Crossref /works (from 2023-01-01) | break-even probability forecast decision crop sowing salinity | 480391 total; top 20 screened | 0 |
| 117 | 2026-11-02 | Crossref /works (from 2023-01-01) | Mekong salinity seasonal forecast ENSO logistic regression extension stations | 177665 total; top 20 screened | 1 |
| 118 | 2026-11-02 | Crossref /works (from 2023-01-01) | saltwater intrusion forecast exceedance probability water supply intake Macau Pearl River decision | 43303 total; top 20 screened | 2 |
| 119 | 2026-11-02 | Crossref /works (from 2023-01-01) | prediction intervals salinity Mekong | 332806 total; top 20 screened | 8 |
| 120 | 2026-11-02 | Crossref /works (from 2023-01-01) | uncertainty quantification salinity forecasting estuary quantile regression deep learning | 1636061 total; top 20 screened | 0 |
| 121 | 2026-11-02 | Crossref /works (from 2023-01-01) | spatial transferability salinity forecasting unseen station | 296939 total; top 20 screened | 3 |
| 122 | 2026-11-02 | Crossref /works (from 2023-01-01) | conformal prediction groundwater salinity | 360799 total; top 20 screened | 0 |
| 123 | 2026-11-02 | Crossref /works (from 2023-01-01) | reconstructing incomplete daily river salinity records calibrated uncertainty Mekong Delta | 10146 total; top 20 screened | 1 |
| 124 | 2026-11-02 | Crossref /works (from 2023-01-01) | river flow mediates drought propagation salinity intrusion Vietnamese Mekong Delta | 14655 total; top 20 screened | 0 |
| 125 | 2026-11-02 | Crossref /works (from 2023-01-01) | salinity intrusion delays transplanting reduces yield paddy rice Mekong | 228371 total; top 20 screened | 2 |
| 126 | 2026-11-02 | Crossref /works (from 2023-01-01) | Wullems salt intrusion Rhine-Meuse probabilistic forecast LSTM multiple locations | 2209 total; top 20 screened | 2 |
| 127 | 2026-11-02 | Crossref /works (from 2023-01-01) | ensemble forecast salt intrusion chloride Rhine-Meuse uncertainty operational | 262139 total; top 20 screened | 2 |
| 128 | 2026-11-02 | Crossref /works (from 2023-01-01) | Sacramento San Joaquin Delta salinity forecast neural network emulator uncertainty | 116488 total; top 20 screened | 0 |
| 129 | 2026-11-02 | Crossref /works (from 2023-01-01) | Ganges delta salinity forecast farmers advisory value | 280073 total; top 20 screened | 1 |
| 130 | 2026-11-02 | Crossref /works (from 2023-01-01) | Bangladesh coastal river salinity forecast machine learning | 1557987 total; top 20 screened | 0 |
| 131 | 2026-11-02 | Crossref /works (from 2023-01-01) | Red River Delta salinity intrusion forecasting machine learning Thai Binh | 391815 total; top 20 screened | 2 |
| 132 | 2026-11-02 | Crossref /works (from 2023-01-01) | salinity intrusion forecast Mekong Cambodia Bassac Prek | 56390 total; top 20 screened | 3 |
| 133 | 2026-11-02 | Crossref /works (from 2023-01-01) | Irrawaddy Ayeyarwady salinity intrusion | 37505 total; top 20 screened | 0 |
| 134 | 2026-11-02 | Crossref /works (from 2023-01-01) | Chao Phraya salinity forecast probabilistic | 221414 total; top 20 screened | 1 |
| 135 | 2026-11-02 | Crossref /works (from 2023-01-01) | Yangtze estuary saltwater intrusion forecast probabilistic interval | 96593 total; top 20 screened | 0 |
| 136 | 2026-11-02 | Crossref /works (from 2023-01-01) | Pearl River estuary chlorinity forecast interval uncertainty deep learning | 1599226 total; top 20 screened | 1 |
| 137 | 2026-11-02 | OpenAlex /authors + /works (from 2025-01-01) | author watch: Nguyen Phuoc Cong; Nigel K. Downes; Huynh Vuong Thu Minh; Pankaj Kumar (IGES); Tran Van Ty (Can Tho); Dat Q. Tran (Arkansas); Heiko Apel; Kieu N. Le | all works since 2025-01-01 of the matched author records, about 160 titles; Dat Q. Tran matched only a UC Riverside record; Kieu N. Le failed (HTTP 429) | 4 (cong2026multi, cong2026deep, tran2025it, Minh et al. 2026 EGH) |
| 138 | 2026-11-02 | OpenAlex /works filter cites: (from 2024-01-01) | works citing Apel et al. 2020 (10.5194/nhess-20-1609-2020) | 18 total; all 18 screened | 6 (Cong 2026 Water; Rapid Prediction Hau 2026; Tian 2025 ASOC; Bauer 2025 J. Hydrol.; Duc/Phong 2025; Nguyen V.H. 2024 JHE) |
| 139 | 2026-11-02 | OpenAlex /works filter cites: | works citing Tran 2025 STOTEN, An-Vo 2021, Cong 2026 (x2), Nguyen 2026 RSASE, Le 2025 Agric. Econ., Mills 2025 JAAEA, Rummel 2025 | HTTP 429 (daily budget used up); 0 screened | n/a, RERUN |
| 140 | 2026-11-02 | Crossref /works query.author + query.bibliographic (from 2025-06-01) | "Nguyen Phuoc Cong / salinity"; "Downes / salinity Mekong"; "Huynh Vuong Thu Minh / salinity"; "Nguyen Dam Quoc Huy / salinity"; "Dat Q. Tran / saltwater intrusion"; "Heiko Apel / salinity"; "Hoa Thanh Thi Nguyen / salinity"; "Duc-Anh An-Vo / forecast"; "Le Phuong Dung / Mekong"; "Bradford Mills / salinity" | 10 queries x top 15 = 150 screened | 5 (Nguyen H.T.X., Mills et al. 2026 JAE; Tran D.D. et al. 2026 JHRS; Ababneh, An-Vo et al. 2026 SSRN; Sang et al. 2026 ISE; Cong 2026) |
| 141 | 2026-11-02 | Zenodo records API (sort=bestmatch) | title:(salinity AND Mekong) | 11 total; 11 screened | 4 (zenodo.23497554 reconstruction with conformal PIs; zenodo.20003854 RSASE maps; zenodo.18622634 transplanting delay; zenodo.23252592 drought propagation) |
| 142 | 2026-11-02 | Zenodo records API (sort=bestmatch) | title:(salinity AND forecast*) | 6 total; 6 screened | 0 (coastal aquifer, Hungary soil and Argo records; none estuarine forecast with value) |
| 143 | 2026-11-02 | Zenodo records API | title:(salinity AND conformal); title:(salt AND intrusion AND forecast*); title:(xâm AND nhập AND mặn) | 0; 0; 0 | 0 |
| 144 | 2026-11-02 | Zenodo records API (sort=mostrecent) | salinity Mekong; salinity forecast conformal; salinity intrusion forecast; dekadal salinity; salinity Vietnam prediction intervals | first query failed (IncompleteRead); others: top 25 newest screened, off-topic because the sort ignores relevance | 0 |
| 145 | 2026-11-02 | WebSearch (standard) | conformal prediction salinity forecast estuary | 10 links | 0 (quantile regression Suwannee Sound 2023; Haringvliet NCK abstract, see row 157) |
| 146 | 2026-11-02 | WebSearch (standard) | NCHMF salinity forecast verification Mekong Delta bulletin accuracy evaluation | 10 links | 2 (Apel 2020; Cong 2026) - no published verification of NCHMF salinity bulletins found |
| 147 | 2026-11-02 | WebSearch (standard) | "relative economic value" salinity forecast | 10 links | 0 (REV/PEV only for streamflow, egusphere-2024-4046) |
| 148 | 2026-11-02 | WebSearch (standard) | đánh giá chất lượng dự báo xâm nhập mặn Trung tâm Dự báo KTTV quốc gia sai số dự báo độ mặn | 10 links | 0 (KNN Hàm Luông; regression Cổ Chiên/Hậu; Nam Định MIKE 11 - point forecasts, no NCHMF verification) |
| 149 | 2026-11-02 | WebSearch (standard) | Tạp chí Khí tượng Thủy văn đánh giá kết quả dự báo xâm nhập mặn mùa khô 2024 2025 đồng bằng sông Cửu Long độ mặn lớn nhất | 10 links | 0 |
| 150 | 2026-11-02 | WebSearch (extended) | probabilistic salinity intrusion forecast Mekong Delta exceedance probability 2025 2026 | 9 links | 1 (Apel 2020); operational 2025-26 outlooks deterministic |
| 151 | 2026-11-02 | WebSearch (extended) | seasonal salinity forecast sowing date winter-spring rice Mekong value early warning cost-loss | 9 links | 3 (Tran 2025; Apel 2020; Ferrer 2022, already cited) |
| 152 | 2026-11-02 | WebSearch (standard) | pre-registration hydrology forecasting study preregistered protocol hydrological model evaluation | 10 links | 0 |
| 153 | 2026-11-02 | WebSearch (standard) | "preregistered" OR "pre-registered" forecast verification climate services water | 10 links | 0 (WMO-No. 1364 verification guidelines; CLARA BAMS 2024 - not pre-registration) |
| 154 | 2026-11-02 | WebSearch (standard) | conformal prediction hydrology water level streamflow 2025 "conformal" river forecasting intervals coverage held-out stations | 10 links | 1 (Zhang et al. 2025 arXiv:2503.04981 STACI) |
| 155 | 2026-11-02 | WebSearch (standard) | IGES 2026 salinity forecasting Mekong Delta report Cong Downes Kumar | 10 links | 0 (IGES page found earlier returned HTTP 403) |
| 156 | 2026-11-02 | WebSearch (standard) | verification of operational salt intrusion chloride forecasts against observations skill persistence benchmark estuary | 10 links | 2 (Wullems 2023 HESS; Steenman & Stolp NCK 2026) |
| 157 | 2026-11-02 | WebFetch | nck-web.org/boa-2026/operational-forecast-of-salinity-levels-in-the-haringvliet-outer-delta-using-machine-learning | page opened | 1 |
| 158 | 2026-11-02 | WebFetch | iges.or.jp/jp/pub/sustainable-water-management-vietnam/en | HTTP 403 | n/a |
| 159 | 2026-11-02 | WebSearch (extended) | seasonal forecast salinity intrusion Mekong Delta months ahead ENSO machine learning severe dry season prediction 2025 2026 | 10 links | 1 (Apel 2020); no 2024-26 seasonal salinity forecast found |
| 160 | 2026-11-02 | WebSearch (extended) | "cost-loss" OR "economic value" saltwater intrusion forecast water intake decision probabilistic | 9 links | 2 (Tran 2025 STOTEN; Tran & Le 2025 Water) |
| 161 | 2026-11-02 | WebSearch (standard) | dự báo xâm nhập mặn xác suất vượt ngưỡng 4 g/l học máy khoảng dự báo | 10 links | 1 (Cong 2026 Water 18(10)) |
| 162 | 2026-11-02 | WebSearch (standard) | Shen Cai Qin 2026 "Machine learning prediction of saltwater intrusion to support coastal water resource management" abstract | 10 links | 1 |
| 163 | 2026-11-02 | WebFetch | chesapeake.org/stac/.../Zhang_Machine-learning-prediction-of-saltwater-intrusion-...pdf | failed: content > 10 MB | n/a |
| 164 | 2026-11-02 | WebSearch (extended) | "conformal" salinity Mekong Delta prediction intervals | 9 links | 0 (the Zenodo reconstruction record of row 141 was NOT surfaced by web search) |
| 165 | 2026-11-02 | WebSearch (standard) | Climate Services journal salinity intrusion forecast Mekong climate service 2025 2026 | 10 links | 1 (Apel 2020); no Climate Services paper on Mekong salinity forecasts found |
| 166 | 2026-11-02 | WebSearch (standard) | lịch thời vụ Đông Xuân né mặn dự báo mặn mùa khô giá trị kinh tế xuống giống sớm nghiên cứu 2025 | 12 links | 0 (provincial sowing calendars only; no study of the value of early sowing) |
| 167 | 2026-11-02 | Zenodo file download (README.md, cv_threshold_skill.csv) | zenodo.org/records/23497554 | read | 1 |
| 168 | 2026-11-02 | arXiv API id_list | 2503.04981 | record opened | 1 |

Record lookups that verified existence (OpenAlex single work and Crossref /works/<doi>, both 02/11/2026):
- 10.68277/kjwe.2026.11, 10.12911/22998993/207704, 10.2166/wpt.2026.273, 10.21203/rs.3.rs-8822636/v1
- 10.1016/j.ejrh.2026.103838, 10.21203/rs.3.rs-9178680/v1, 10.48084/etasr.19195, 10.55659/2525-2496/36.121708
- 10.1061/jhyeff.heeng-6223, 10.1007/s13201-025-02419-z, 10.1007/978-981-95-6770-6_225, 10.64697/iahr.proc.ise2026.abs.184
- 10.2139/ssrn.4965853, 10.2139/ssrn.7505678, 10.2139/ssrn.7203434, 10.2139/ssrn.6991006
- 10.1016/j.jhydrol.2024.131894, 10.3990/1.9789036568647, 10.1038/s41598-026-48012-5, 10.2139/ssrn.7589481
- 10.1016/j.asoc.2025.113897, 10.5194/hess-27-3823-2023, 10.5194/egusphere-egu24-12982, 10.1016/j.jhydrol.2025.133745
- 10.1007/s10653-026-03022-0, 10.3389/fmars.2024.1407690, 10.36335/vnjhm.2025(770).97-107, 10.1016/j.jenvman.2026.128811
- 10.1016/j.jenvman.2023.119443, 10.1016/j.crm.2023.100541, 10.1590/1807-1929/agriambi.v30n10e304109, 10.15625/1859-3097/18174
- 10.1111/1477-9552.70042, 10.1016/j.ejrh.2026.104029, 10.2166/wcc.2026.035, 10.1088/1755-1315/1674/1/012005
- 10.1029/2024wr039807, 10.3390/s26185800

Zenodo API records: 23497553 (redirects to version 23497554), 22791748, 23252592, 20003854, 18622634.

The prior-art DOIs already in references.bib were Crossref-verified on 02/11/2026 (header of references.bib) and were not re-opened.

## 2. Verdict per claim

### C1. Multi-station dekadal salinity forecast benchmarked against the official national (NCHMF) forecast

**Closest works:**
- **Nguyen, Duc Phong et al. (2025)**, Discov. Artif. Intell. 5:79, doi:10.1007/s44163-025-00336-3 (cited as duc2025predicting).
  - They: hourly forecasts at 4 stations, point forecasts, no operational benchmark.
- **Le V.Q. et al. (2025)**, Hue Univ. J. Sci. 134(1S-1), doi:10.26459/hueunijns.v134i1s-1.7876 (le2025salinity).
  - They: 44 stations, 1-7 days ahead, point forecasts, time-series CV, no operational benchmark.
  - **The manuscript's phrase "one or a few stations" (S3) does not fit this paper.**
- **Do Dang L.-P. (Crossref: Le Thi Thanh Dang), Ishidaira H., Nguyen K.P., Souma K., Magome J. (2025)** "Short-term salinity prediction for coastal areas of the Vietnamese Mekong Delta using various machine learning algorithms: a case study in Soc Trang Province", Appl. Water Sci., doi:10.1007/s13201-025-02419-z.
  - They: 4 stations, hourly, up to 16 h ahead, random 75/25 split, point forecasts.
- **Nguyen V.-H., Duong V.-T., Le A., Mai H.T.H., Dang H.T., Phan D., Adhikari J. (2024)** "Machine Learning-Based Early-Warning Systems for Salinity Intrusion in the Mekong River Delta, Vietnam", J. Hydrol. Eng. (Oct 2024), doi:10.1061/jhyeff.heeng-6223.
  - They: 13 classifiers of intrusion severity (accuracy 86-100%), no probabilities scored, no operational benchmark.
- **Le Van Chin, Pham Van Chien (2025)** "Estimating salinity using long short-term memory in the Vietnamese Mekong Delta and analyzing its dynamics", J. Ecol. Eng., doi:10.12911/22998993/207704.
  - They: LSTM at 6 locations, 2014-2017, estimation from tide and discharge, point values.
- **Wullems B.J.M., Brauer C.C., Baart F., Weerts A.H. (2023)** "Forecasting estuarine salt intrusion in the Rhine-Meuse delta using an LSTM model", HESS 27:3823-3850, doi:10.5194/hess-27-3823-2023.
  - They: 1-7 day chloride forecasts at one location (Krimpen aan den IJssel), threshold precision and recall, no comparison with an operational forecast reported in the abstract.
- **Steenman Y.B., Stolp T. (2026)** "Operational forecast of salinity levels in the Haringvliet outer delta using machine learning", NCK Days 2026 Book of Abstracts, https://www.nck-web.org/boa-2026/operational-forecast-of-salinity-levels-in-the-haringvliet-outer-delta-using-machine-learning (page opened).
  - They: one station (Stellendam-buiten), 48 h ahead.
  - "Model performance was benchmarked against the OSR numerical model", the operational Rotterdam flow model.
  - Uncertainty band from perturbed inputs, with no calibration or coverage reported.
  - **This is the only work found that benchmarks a statistical salinity forecast against an operational forecast.**
- **Shen J., Cai X., Qin Q. (2026)** "Machine learning prediction of saltwater intrusion to support coastal water resource management", J. Environ. Manage., doi:10.1016/j.jenvman.2026.128811.
  - They: ML intrusion-length forecasts for the Chesapeake main stem and 8 tributaries, daily to 14-day lead (from a web-search summary of the authors' PDF; the record was opened, no abstract in the API).
  - Deterministic, with no operational benchmark found.

**What the manuscript does:** a pooled model over 28 NCHMF stations at a 10-day lead. It is scored under one protocol against the official NCHMF forecast, persistence and climatology, with forward, leave-station-out and leave-province-out tests.

**Other searches:**
- English and Vietnamese searches found no published verification of the NCHMF salinity bulletins (rows 146, 148, 149).
- They found no dekadal salinity forecast study (row 22, "dekadal salinity forecast": 7 hits, none relevant).

**Verdict: holds as a search-scope statement**, with two wording fixes.
- (a) S3 says "one or a few stations", but le2025salinity used 44 stations (and bui2025surface reportedly 68, unverified).
- (b) S1 and S5.1 call the benchmark "public". The bulletins are public, but the transcribed values cannot be redistributed (declarations.tex:19). A reader may take "public benchmark" to mean released data. Say "built from public bulletins".

Optional narrower international wording: "...a multi-station salinity forecast verified against an operational national forecast; the closest, at a single Dutch station, compared a machine-learning forecast with an operational numerical model (Steenman and Stolp, 2026)."

### C2. Conformal (or other calibrated) prediction intervals for salinity, tested at held-out stations and provinces

**Closest works:**
- **Nguyen H.T.T., Tran H.M.T., Le G.S. (2026)** "Reconstructed daily peak river salinity in the coastal Mekong Delta, 2016-17 to 2024-25, with prediction intervals, and analysis code" [data set], Zenodo, published 2026-10-20, doi:10.5281/zenodo.23497554 (concept doi:10.5281/zenodo.23497553), CC BY 4.0 / MIT.
  - Associated article (README): "A hybrid deep learning and machine learning framework for reconstructing incomplete daily river salinity records with calibrated uncertainty in the Mekong Delta", Earth Science Informatics (submitted; no DOI yet).
  - They: 34 stations in former Bến Tre, Trà Vinh and Vĩnh Long provinces; daily peaks.
  - Gaps were filled by SAITS stacked into LightGBM, XGBoost and random forest.
  - Each filled value has a **90% cross-conformal prediction interval** (strata: gap class x stations available x predicted level). README: "the 90% intervals achieved 89-90% coverage".
  - Includes whole-season reconstruction (a season-held-out design). POD, FAR and CSI are reported at 4, 10 and 20 per mille.
  - **This is conformal prediction applied to estuarine salinity in the Mekong Delta**, but for imputation and reconstruction (same-day values at other stations are predictors), not forecasting. There is no leave-station-out or leave-province-out test.
- **Pal M., Abdi E., Torabi Haghighi A. (2026)** "Conformal Prediction for River Total Dissolved Solids (TDS) Prediction and Risk Quantification", Khazar J. Water Environ., published 2026-10-31, doi:10.68277/kjwe.2026.11.
  - They: monthly TDS in a Hong Kong river.
  - Split CP, CV+ and CQR intervals, plus exceedance probabilities.
  - Predictors are concurrent pH, salinity, turbidity and temperature: estimation, not forecasting with lead time.
  - The test is a random 80/20 split, with no spatial transfer.
- **Cong N.P. et al. (2026)**, Water 18(19):2379 and 18(10):1240 (already cited). Single stations, with empirical intervals that over-cover.
- **Nguyen D.Q.H. et al. (2026)**, RSASE, doi:10.1016/j.rsase.2026.102297 (already cited), with its 2026 Zenodo map set doi:10.5281/zenodo.20003854. Leave-one-station-out mapping, no intervals.
- **Conformal analogues in hydrology (not salinity):**
  - Jia Y., Su X., Singh V.P. et al. (2026) WRR, doi:10.1029/2024wr039807: weighted conformal runoff intervals across Australia.
  - Abdi E., Sattari M.T., Pal M. et al. (2026) Sensors 26:5800, doi:10.3390/s26185800: river discharge.
  - Zhang J., Wang F., Song Z., Yu P.S., Ding K. (2025) "Topology-Aware Conformal Prediction for Stream Networks", arXiv:2503.04981.
  - Mends L.G. et al. (2026) "Event-Grouped Calibration for Conformal Streamflow Reconstruction", SSRN, doi:10.2139/ssrn.7589481. Grouped calibration folds restore coverage, close in spirit to the manuscript's season folds.
  - Goenka S.K., R M. (2026) Zenodo doi:10.5281/zenodo.22791748: group-aware conformal for water-quality retrieval. "Marginal coverage survives water-body shift; conditional coverage does not."

**What the manuscript does:** conformalized quantile forecasts at a 10-day lead. Their coverage is tested forward in time and with whole stations and whole provinces left out of training.

**Verdict: must be narrowed.** The present S4 wording, "conformal prediction applied to estuarine salinity forecasting", is still literally true: the Zenodo record is reconstruction, not forecasting. But it is now one step from pre-emption, and a reviewer who knows the record will read the claim as incomplete. Cite the record and narrow the claim to forecasting plus spatial transfer.

Narrower wording: "conformal prediction intervals for salinity forecasts evaluated at stations or provinces withheld from training (conformal intervals have been used to reconstruct gaps in daily salinity records at 34 stations of the coastal delta; Nguyen et al., 2026)".

### C3. Economic value (cost/loss, REV) of probabilistic salinity forecasts compared with a deterministic official forecast

**Closest works:**
- **Tran D.Q. et al. (2025)** STOTEN 966:178711, doi:10.1016/j.scitotenv.2025.178711 (cited). Value of better intrusion forecasts (USD 47-51 M/yr) at delta scale, from assumed accuracy gains; not cost/loss and not probabilistic-versus-deterministic.
- **Tran D.Q., Le K.N. (2025)** Water 17(9):1355, doi:10.3390/w17091355. Costs of mitigation under uncertainty.
- **Pal et al. (2026)**, above. Exceedance probabilities for TDS, but no value analysis.
- **Wullems et al. (2023)**, above. Threshold precision and recall only.
- **Pham Ngoc, Bui Thi Diep Oanh, Pham Thi Hoa (2026)** IOP Conf. Ser. Earth Environ. Sci. 1674:012005, doi:10.1088/1755-1315/1674/1/012005. Economic loss of intrusion to the water supply of Ho Chi Minh City under scenarios (replacement cost); no forecast value.

REV and cost/loss are standard for weather and streamflow forecasts (Richardson 2000; Zhu et al. 2002; EGU preprint egusphere-2024-4046, streamflow, from a search result, not opened). Rows 147 and 160 and the Crossref and OpenAlex value queries found no application to salinity forecasts.

**What the manuscript does:** the REV of the calibrated P(Smax > 4 g/L) against the official deterministic forecast and persistence, for C/L 0.1-0.9.

**Verdict: holds as a search-scope statement.** S4 currently words this claim as "a cost--loss evaluation of probabilistic salinity forecasts for a farm decision". That describes the Layer A scenario, not the core-B REV result, which is the stronger finding. Split it into two items (Section 4, edit E2).

### C4. Seasonal severe-season salinity forecast linked to the value of the sowing decision and break-even probabilities

**Closest works:**
- **Apel H. et al. (2020)** NHESS 20:1609, doi:10.5194/nhess-20-1609-2020 (cited). Logistic seasonal forecast at Sơn Đốc, ROC > 0.8 up to 9 months ahead, no decision value.
  - Searches found no follow-up seasonal salinity forecast: of 18 works citing it since 2024, none is a seasonal forecast (row 138), and Apel's 2025-26 outputs contain none (rows 137, 140).
- **An-Vo D.-A. et al. (2021)** Clim. Serv. 22:100234 (cited). Value of seasonal rainfall forecasts for sowing.
  - Follow-up: Ababneh S., An-Vo D.-A., Mushtaq S., Gillies M.H., Kouadio L. (2026) "Enhancing the economic value of irrigation water through seasonal climate forecast integration", SSRN, doi:10.2139/ssrn.6991006. Irrigation in Australia, not salinity.
- **Kayamo S.E., Troost C., Yismaw H., Berger T. (2023)** "The financial value of seasonal forecast-based cultivar choice: Assessing the evidence in the Central Rift Valley of Ethiopia", Clim. Risk Manag., doi:10.1016/j.crm.2023.100541.
  - A climate-service analogue. It finds that evidence on yield differences between options, not forecast skill, limits value. **This is the same conclusion as the manuscript's statement on the parameter m.**
- **Nguyen H.T.X., Mills B.F., Ta C.L., Stewart S.L. (2026)** "Rising Tides, Falling Harvests: Examining the Effects of Salinity Intrusion on Paddy Production in Vietnam's Mekong Delta", J. Agric. Econ., doi:10.1111/1477-9552.70042.
  - District panel 2000-2020. A Nerlovian adaptive-expectations model shows that Winter-Spring acreage responds to past extreme salinity.
- **Wang Q., Yang K. (2026)** "Salinity Intrusion Delays Transplanting and Reduces Yield of Paddy Rice in the Vietnam Mekong Delta", Zenodo doi:10.5281/zenodo.18622634.
  - Peer-review data attachment; the article is not yet published.
  - Pixel-level transplanting dates, EC before transplanting, and relative-yield scenarios.
- **Le Phuong-Dung et al. (2025)**, **Mills et al. (2025)** and **Ferrer et al. (2022)**, all already cited.

**What the manuscript does:** a 1 November severe-season probability at 3 gauges, evaluated out of sample. Its regret and REV for early sowing are compared with a fixed calendar and with climatology, and crop-option break-even probabilities are given.

**Verdict: holds as a search-scope statement.** No study found links a seasonal salinity forecast to the value of a sowing decision or to break-even probabilities.

**Must-cite:** Nguyen, Mills et al. (2026). Its adaptive-expectations result (farmers already respond to past salinity) is direct context for the finding that the forecast adds nothing beyond climatology.

### C5. Pre-registered protocol in this field

**Searches:**
- Web rows 152-153 found no pre-registered (or registered-report) salinity, hydrological or climate-service forecast evaluation.
- OpenAlex rows 34-35 ("pre-registered forecast evaluation hydrology", "preregistration hydrology forecasting study") returned only 1,464 and 5 off-topic hits.
- Nearest standards: WMO-No. 1364 guidelines on hydrological forecast verification (2025; from search result, not opened), and the CLARA joint verification framework (BAMS 2024, doi:10.1175/BAMS-D-23-0026.1; from search result, not opened).

The manuscript does not claim to be the first. If such a claim is added, phrase it as a search-scope statement.

**Verdict: holds as a search-scope statement (no priority claimed). Wording risk:**
- (i) "Pre-registered" usually implies an externally time-stamped registration (OSF, AsPredicted, a registry). Here the protocol is a git tag in a repository that, according to the project notes, has no remote yet. Readers cannot verify the freeze date independently.
- (ii) The test-season data (2024-2026) existed before the freeze. Methods 3.1 says this correctly ("frozen ... before any model was scored on a test season"); it amounts to pre-registration of an analysis of existing data.

Options, for the owner to decide:
- (a) Replace "pre-registered" with "protocol frozen before scoring" in the abstract, highlights and conclusions.
- (b) Keep "pre-registered" and add one sentence in 3.1 on how the freeze can be verified, for example the tag's commit date once the repository is public.

## 3. Papers and records the manuscript should cite or know about

None of the works found is dated after 01/11/2026; the newest are Pal et al. (31/10/2026) and the Zenodo reconstruction (20/10/2026). Everything below was missed by the 01/11 search or is new to the manuscript.

1. **Nguyen H.T.T., Tran H.M.T., Le G.S. (2026)**, Zenodo doi:10.5281/zenodo.23497554 (article submitted to Earth Sci. Inform.).
   - Cite in the introduction (C2) and Discussion 6.2. Their reconstruction coverage of 89-90% agrees with ours.
   - **New competitor (HCMUNRE, per the README contact).** They hold daily records at 34 stations for 2016-2025 and already run conformal intervals, so a forecasting paper from them is the obvious next step. Re-check before submission.
2. **Pal, Abdi, Torabi Haghighi (2026)**, doi:10.68277/kjwe.2026.11. Cite in the introduction as the nearest conformal plus exceedance-probability work on river salt content (estimation, not forecast).
3. **Steenman and Stolp (2026)**, NCK abstract (URL above), and **Wullems et al. (2023)**, doi:10.5194/hess-27-3823-2023.
   - International context for C1: the only benchmark against an operational model found (one station), and threshold-based salt-intrusion forecasting in the Rhine-Meuse delta.
4. **Nguyen H.T.X., Mills, Ta, Stewart (2026)**, doi:10.1111/1477-9552.70042. Cite in Discussion 6.3: farmers' acreage already responds to salinity history. This is consistent with the forecast adding nothing beyond climatology.
5. **Do Dang et al. (2025)**, doi:10.1007/s13201-025-02419-z, and **Nguyen V.-H. et al. (2024)**, doi:10.1061/jhyeff.heeng-6223. Add to the list of Mekong ML forecasts in S3; the second is a threshold classifier, closest in spirit to exceedance forecasts.
6. **Kayamo et al. (2023)**, doi:10.1016/j.crm.2023.100541 (Climate Risk Management). Cite in 6.3 next to the m argument: forecast value is limited by evidence on how the options differ, not by skill.
7. **Nguyen Trinh Chung, Vo Van Tien, Nguyen Dang Tinh (2026)**, Water Pract. Technol., doi:10.2166/wpt.2026.273. It analyses MIKE 11 output "using operational thresholds of 1.0, 2.0, and 4.0 g L-1". This is a secondary, peer-reviewed use of the same thresholds and could replace `\citetodo{source for the 1/2/4 g/L use thresholds}` until the primary standard is found.
8. Optional:
   - **Shen, Cai, Qin (2026)** JEM doi:10.1016/j.jenvman.2026.128811 and **Kang et al. (2026)** Sci. Rep. doi:10.1038/s41598-026-48012-5: international ML salinity forecasts, deterministic.
   - **Tran D.D., Park E. et al. (2026)** JHRS doi:10.1016/j.ejrh.2026.104029: MIKE 11 scenarios; sluice gates shift intrusion to adjacent branches. Relevant to the gated/ungated discussion.
   - **Wang & Yang (2026)**, Zenodo doi:10.5281/zenodo.18622634: salinity delays transplanting. Cite only once the article is out.
   - **Conformal hydrology analogues:** Jia et al. 2026 WRR; Mends et al. 2026 SSRN.

**Competitor watch, 2025-2026:**
- **CTU / IGES / UNU** (Cong, Downes, Minh, Kumar, Ty): no salinity-forecast output after Cong et al. Water 18(19):2379 (24/09/2026). Their other 2026 outputs cover regime-shift trends (Minh et al. 2026 Environ. Geochem. Health, doi:10.1007/s10653-026-03022-0), drought, sediment forecasting (Water 18(8):923), microplastics and riverbank erosion. The IGES page could not be read (HTTP 403).
- **RSASE group** (Nguyen D.Q.H.): only the map data set (Zenodo, May 2026).
- **Arkansas group** (Tran D.Q., Le K.N.): nothing new found. The OpenAlex author match failed, so **rerun**.
- **Apel:** no new salinity forecast. A 2026 German chapter on Mekong agricultural risks (doi:10.25592/uhhfdm.18920) was not read.
- **New groups:**
  - HCMUNRE (item 1);
  - Kantoush / Doan Van Binh: Sentinel-2 random forest at 40 stations, ISE 2026, doi:10.64697/iahr.proc.ise2026.abs.184 (nowcast);
  - Nguyen T.K.D. and Nguyen D.P.: drought propagation to salinity, HSJ manuscript HSJ-2026-0487, data doi:10.5281/zenodo.23252592.

## 4. Suggested sentence edits (do not apply without the owner)

- **E1 (S4, 01_introduction.tex:32-36), replace the search sentence with:** "In our searches of OpenAlex, Crossref, Europe PMC, arXiv, Zenodo and the web (1-2 November 2026) we did not find a multi-station salinity forecast verified against an operational national forecast, conformal prediction intervals for salinity forecasts evaluated at stations or provinces withheld from training, a relative-economic-value comparison of probabilistic and official deterministic salinity forecasts, or a cost--loss evaluation of a seasonal salinity forecast for a sowing decision. Conformal intervals have been used to reconstruct gaps in daily salinity records at 34 stations of the coastal delta \citep{nguyen2026reconstructed} and to estimate river total dissolved solids \citep{pal2026conformal}. These are statements about the scope of our searches, not claims that no such work exists."
  - New bib keys: nguyen2026reconstructed = doi:10.5281/zenodo.23497554 (@misc, data set); pal2026conformal = doi:10.68277/kjwe.2026.11.
- **E2:** E1 splits C3 into its two parts: REV against the official forecast (core B), and cost/loss for sowing (layer A).
- **E3 (S3, 01_introduction.tex:21-23):**
  - Replace "they are point forecasts at one or a few stations, without a test at stations or seasons outside the training data" with "they are point forecasts, mostly at one or a few stations (one study pooled 44), without a test at stations or seasons outside the training data".
  - Extend the citation list to `\citep{duc2025predicting,le2025salinity,nguyen2025estuary,bui2025surface,dodang2025short,nguyen2024machine}` (dodang2025short = doi:10.1007/s13201-025-02419-z; nguyen2024machine = doi:10.1061/jhyeff.heeng-6223).
  - Optionally add: "In other deltas, a machine-learning forecast has been compared with an operational numerical model at a single station \citep{steenman2026operational}, and salt-intrusion forecasts are usually verified with threshold hit rates \citep{wullems2023forecasting}."
- **E4 (S5.1, 01_introduction.tex:41):** replace "A public, pre-registered benchmark of dekadal maximum salinity forecasts" with "A benchmark of dekadal maximum salinity forecasts built from public NCHMF bulletins under a protocol frozen before scoring". Keep "pre-registered" only if option C5(b) is chosen.
- **E5 (S1, abstract.tex:2-4):** replace "We built a pre-registered benchmark from 50 public bulletins" with "We built a benchmark from 50 public bulletins [...], with a protocol frozen before any test season was scored". This adds about 9 words; check the abstract limit.
- **E6 (S2, highlights.tex:2):** if C5(a) is chosen, use "Protocol-first benchmark of dekadal salinity forecasts at 28 Mekong Delta stations" (82 characters, counted).
- **E7 (S6, 07_conclusions.tex:3):** same change as E5 ("pre-registered" to "protocol-frozen"), if C5(a) is chosen.
- **E8 (06_discussion.tex, 6.2 "Calibration transfers", after the first paragraph):** add "Cross-conformal intervals for reconstructed daily salinity peaks at 34 coastal stations reached a similar 89--90\% coverage \citep{nguyen2026reconstructed}; our result extends this from gap filling to forecasts and to stations and provinces left out of training."
- **E9 (06_discussion.tex, 6.3, after "...cannot be separated from zero."):** add "Farmers' Winter--Spring acreage already responds to past salinity extremes \citep{nguyen2026rising}, so part of the climatological signal may already be in use; a seasonal forecast has to beat that, not a fixed calendar."
  - Also, after the m sentence, add: "Forecast-based cultivar choice in Ethiopia met the same limit: evidence on how options differ, not forecast skill, bounded the value \citep{kayamo2023financial}."
- **E10 (01_introduction.tex:17), the 1/2/4 g/L thresholds `\citetodo`:** interim citation \citep{chung2026operational} (doi:10.2166/wpt.2026.273), which uses 1, 2 and 4 g/L as operational thresholds. Replace it with the primary national standard if one is found.
- **E11 (S4 date):** change "1 November 2026" to "1--2 November 2026", and rerun the searches (especially the OpenAlex citation checks and Semantic Scholar) on the day before submission.
