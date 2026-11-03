# Novelty re-check before submission (Climate Services), 03/11/2026

All searches below ran on 2026-11-03. This file continues docs/background/novelty_recheck_2026-11-02.md (rows 1-168; here rows 169 onward) and closes the gaps listed there.
Every novelty statement describes the scope of these searches. None is a statement of fact about the literature. No manuscript file was edited.

**How works were verified.** A work counts as verified if its record was opened on 03/11/2026 through the OpenAlex single-work endpoint, the Crossref `/works/<doi>` endpoint, the DataCite DOI endpoint or the Zenodo records API. Only titles, authors, dates and abstracts were read. Items marked "not opened" came from a web-search summary only.

**Request settings.** User-Agent `mekong-salinity-novelty-check/1.0`, TLS verification on, no email address in any request, at least 1.2 s between requests. Raw responses are saved in `scratchpad/novelty1103/raw/` (session scratchpad, not in the repository); scripts sit one level up.

**What could not be checked (details in Section 5):**
- Semantic Scholar: HTTP 429 on all 6 queries, each retried 3 times with 30 s waits. Second day running; treat as unavailable.
- OpenAlex worked today (the daily budget had reset), so the citation checks of 02/11 row 139 are now done.
- The abstract of the 2026 TU Delft dissertation "Forecasting Salt Intrusion in Estuaries" (Gerritsma) could not be read.
- The Earth Science Informatics article of the HCMUNRE group is still not indexed anywhere I could query.

## 1. Search log (continuing from row 169)

"Total" is the count the API reported. "Screened" = titles read by hand (OpenAlex/Crossref/Zenodo: top 200 or top 25 by the API's order, as stated). Relevant hits are works that matter for a claim or that are already in the 02/11 file.

| # | Date | Engine / API | Exact query | Hits screened | Relevant hits |
|---|---|---|---|---|---|
| 169 | 2026-11-03 | OpenAlex /works filter cites: (from 2024-01-01) | citing Tran/Le/Durand-Morat 2025 STOTEN (W4407121263, 10.1016/j.scitotenv.2025.178711) | 3 total; 3 screened | 1 (Tran & Le 2025 Water 17(9):1355, known); the other two (Yellow River soil carbon, managed aquifer recharge value) are off-topic |
| 170 | 2026-11-03 | OpenAlex filter cites: | citing An-Vo et al. 2021 (W3160523267, 10.1016/j.cliser.2021.100234) | 19 total; 19 screened | 0 on salinity. Context only: 10.1088/1748-9326/ad8bde (seasonal forecast skill and agricultural decisions), 10.1016/j.crm.2024.100686 (Tanzania), 10.1111/1477-9552.70054 (Ethiopia, precipitation forecast benefit), 10.3389/fclim.2026.1741828 (review, economic value of agro-meteorological services) |
| 171 | 2026-11-03 | OpenAlex filter cites: | citing Cong et al. 2026 Water 18(19) (W7214191557, 10.3390/w18192379) | 0 total | 0 |
| 172 | 2026-11-03 | OpenAlex filter cites: | citing Cong et al. 2026 Water 18(10) (W7161829978, 10.3390/w18101240) | 1 total; 1 screened | 1 (it is cited only by Cong 18(19), the same group) |
| 173 | 2026-11-03 | OpenAlex filter cites: | citing Nguyen D.Q.H. et al. 2026 RSASE (W7214602809, 10.1016/j.rsase.2026.102297) | 0 total | 0 |
| 174 | 2026-11-03 | OpenAlex filter cites: | citing Le et al. 2025 Agric. Econ. (W4410617054, 10.1111/agec.70045) | 2 total; 2 screened | 0 (social capital SSRN; Annu. Rev. Resour. Econ. soil degradation) |
| 175 | 2026-11-03 | OpenAlex filter cites: | citing Mills et al. 2025 (W4408467207, 10.1002/jaa2.70004) | 6 total; 6 screened | 2 (Minh et al. 2026 EGH, known; Nguyen H.T.X. et al. 2026 J. Agric. Econ., known) |
| 176 | 2026-11-03 | OpenAlex filter cites: (from 2026-11-02) | citing Apel et al. 2020 (W2982230088) | 0 total | 0 (18 earlier citers screened on 02/11, row 138) |
| 177 | 2026-11-03 | Semantic Scholar Graph API | salinity intrusion forecast Mekong | HTTP 429 after 4 attempts | n/a |
| 178 | 2026-11-03 | Semantic Scholar Graph API | salinity forecast conformal prediction | HTTP 429 after 4 attempts | n/a |
| 179 | 2026-11-03 | Semantic Scholar Graph API | salinity forecast relative economic value | HTTP 429 after 4 attempts | n/a |
| 180 | 2026-11-03 | Semantic Scholar Graph API | seasonal salinity forecast sowing decision | HTTP 429 after 4 attempts | n/a |
| 181 | 2026-11-03 | Semantic Scholar Graph API | probabilistic salinity forecast estuary | HTTP 429 after 4 attempts | n/a |
| 182 | 2026-11-03 | Semantic Scholar Graph API | salinity prediction leave-one-station-out | HTTP 429 after 4 attempts | n/a |
| 183 | 2026-11-03 | OpenAlex /works (from 2026-10-25) | salinity forecast | 215 total; top 200 screened | 0 new (Pal 2026 known; Gerritsma dissertation, see row 217) |
| 184 | 2026-11-03 | OpenAlex (from 2026-10-25) | salinity prediction | 905 total; top 200 screened | 0 (soil-salinity and aquifer papers) |
| 185 | 2026-11-03 | OpenAlex (from 2026-10-25) | saltwater intrusion | 64 total; 64 screened | 1 (Tra Vinh coastal groundwater model 10.3390/w18212714, off-topic: groundwater) |
| 186 | 2026-11-03 | OpenAlex (from 2026-10-25) | salt intrusion | 125 total; top 125 screened | 1 (Gerritsma dissertation) |
| 187 | 2026-11-03 | OpenAlex (from 2026-10-25) | salinity Mekong | 29 total; 29 screened | 1 (Wang & Yang figshare copy of the transplanting-delay data, known from Zenodo) |
| 188 | 2026-11-03 | OpenAlex (from 2026-10-25) | salinity estuary forecasting | 25 total; 25 screened | 1 (Gerritsma) |
| 189 | 2026-11-03 | OpenAlex (from 2026-10-25) | xâm nhập mặn | 19 total; 19 screened | 0 |
| 190 | 2026-11-03 | OpenAlex (from 2026-10-25) | conformal prediction salinity | 42 total; 42 screened | 1 (Pal 2026, known) |
| 191 | 2026-11-03 | OpenAlex (from 2026-10-25) | salinity delta machine learning | 56 total; 56 screened | 0 |
| 192 | 2026-11-03 | OpenAlex (from 2026-10-25) | salinity probabilistic | 86 total; 86 screened | 0 |
| 193 | 2026-11-03 | OpenAlex (from 2026-10-25) | Mekong Delta forecasting | 20 total; 20 screened | 0 (dengue early-warning economic-evaluation protocol, other domain) |
| 194 | 2026-11-03 | Crossref /works (from-created-date 2026-10-25) | salinity forecast Mekong | 287 total; top 100 screened | 0 |
| 195 | 2026-11-03 | Crossref (from-created-date 2026-10-25) | salinity prediction estuary forecast | 3829 total; top 100 screened | 0 |
| 196 | 2026-11-03 | Crossref (from-created-date 2026-10-25) | salinity intrusion forecast delta | 917 total; top 100 screened | 0 |
| 197 | 2026-11-03 | Crossref (from-created-date 2026-10-25) | conformal prediction salinity | 3738 total; top 100 screened | 0 |
| 198 | 2026-11-03 | Crossref (from-created-date 2026-10-25) | saltwater intrusion forecasting machine learning | 17066 total; top 100 screened | 0 |
| 199 | 2026-11-03 | Crossref (from-created-date 2026-10-25) | salinity Mekong Delta | 516 total; top 100 screened | 0 (groundwater governance preprint 10.21203/rs.3.rs-11584104/v1, off-topic) |
| 200 | 2026-11-03 | Crossref (from-created-date 2026-10-25) | xâm nhập mặn dự báo | 124 total; top 100 screened | 0 |
| 201 | 2026-11-03 | Crossref (from-created-date 2026-10-25) | probabilistic salinity forecast | 554 total; top 100 screened | 0 |
| 202 | 2026-11-03 | Crossref (from-created-date 2026-10-25) | seasonal salinity forecast | 684 total; top 100 screened | 0 |
| 203 | 2026-11-03 | Crossref (from-created-date 2026-10-25) | relative economic value forecast salinity | 7111 total; top 100 screened | 0 |
| 204 | 2026-11-03 | Zenodo records API (sort=mostrecent, size 25) | salinity Mekong | 13332 total; newest 25 screened (created 30/10-03/11) | 0 (23888498 Mekong water-quality package: organic pollution, off-topic; 23918729 irrigation governance replication data, off-topic) |
| 205 | 2026-11-03 | Zenodo (mostrecent) | salinity forecast | 26954 total; newest 25 screened | 0 |
| 206 | 2026-11-03 | Zenodo (mostrecent) | salinity intrusion forecast | 33561 total; newest 25 screened | 0 |
| 207 | 2026-11-03 | Zenodo (mostrecent) | conformal salinity | 16036 total; newest 25 screened | 0 (conformal records are lithium, wind power, tabular classifiers) |
| 208 | 2026-11-03 | Zenodo (mostrecent) | xâm nhập mặn | 24065 total; newest 25 screened | 0 |
| 209 | 2026-11-03 | OpenAlex works, filter authorships.author.id (from 2026-09-01) | CTU/IGES group: Nguyen Phuoc Cong, Downes, Huỳnh Vương Thu Minh, Sudhir Kumar Singh, Tran Van Ty (two IDs), Pankaj Kumar, Đinh Văn Duy | 17 total; 17 screened | 1 (Cong 18(19), known); no new salinity output |
| 210 | 2026-11-03 | OpenAlex (author ids, from 2026-09-01) | Arkansas group: Kieu Ngoc Le, Alvaro Durand-Morat | 3 total; 3 screened | 0 (rangeland carbon, rice breeding, cover crops) |
| 211 | 2026-11-03 | OpenAlex (author ids, from 2026-09-01) | RSASE/Grenoble group: Nguyen Dam Quoc Huy, Truong An Nguyen, Tran Thi Kim | 6 total; 6 screened | 1 (RSASE 10.1016/j.rsase.2026.102297, known) |
| 212 | 2026-11-03 | OpenAlex (author ids, from 2026-09-01) | HCMUNRE: Hoa Thanh Thi Nguyen, Tran Thi My Hong, Giang Song Lê | 9 total; 9 screened | 1 (Zenodo reconstruction 23497553, known). The rest are geotechnics, seepage and microplastics code records |
| 213 | 2026-11-03 | OpenAlex (author ids, from 2026-09-01) | Apel, Mai Van Khiem, Nguyễn Hồng Quân, Tô Quang Toản, Doan Van Binh, Kantoush, Ngô Trần Sang | 9 total; 9 screened | 0 (floods, drought, SMAP; no salinity) |
| 214 | 2026-11-03 | Crossref /works query.author + query.bibliographic (from-created-date 2025-06-01) | "Dat Q. Tran" and "Kieu N. Le" with "salinity saltwater intrusion Mekong" | 2 x 8 screened | 0 new (known: Tran D.D. 2026 EJRH, etasr review, SSRN copy of RSASE) |
| 215 | 2026-11-03 | Crossref /works query.bibliographic | hybrid deep learning and machine learning framework for reconstructing incomplete daily river salinity records with calibrated uncertainty Mekong Delta | top 5 screened | 0: the HCMUNRE article is not indexed |
| 216 | 2026-11-03 | OpenAlex /works search | reconstructing incomplete daily river salinity records calibrated uncertainty Mekong Delta | top 5 screened | 0: not indexed |
| 217 | 2026-11-03 | DataCite DOI + OpenAlex single work | 10.4233/uuid:f059bc44-6aa7-4df8-b9e7-af52817b562e | record opened: A. Gerritsma, "Forecasting Salt Intrusion in Estuaries", dissertation, 2026-10-26 (TU Delft DOI prefix) | 1; no abstract in OpenAlex or DataCite |
| 218 | 2026-11-03 | Zenodo API single record | 23497554 | record opened, updated 2026-10-20, version 1.0, unchanged since 02/11 | 1 |
| 219 | 2026-11-03 | Zenodo API single record | 23888498; 23918729 | records opened | 0 |
| 220 | 2026-11-03 | Crossref single works | 10.1016/j.scitotenv.2025.178711; 10.3390/w17091355; 10.1007/s41748-026-01090-x | records opened | 3 (the first two confirm authors and titles of the C3 works; the third is an unrelated imputation paper, see Section 3) |
| 221 | 2026-11-03 | Crossref query.bibliographic | Hung My Tra Vinh salinity forecasting LSTM lookback window horizon Duy Ty Ngoc Minh Downes | top 6 screened | 1 (resolves to Cong 18(10) and 18(19), known) |
| 222 | 2026-11-03 | WebSearch (standard) | Mekong salinity forecast 2026 probabilistic | 9 links | 1 (Cong 18(10)); operational 2026 outlooks are deterministic |
| 223 | 2026-11-03 | WebSearch (standard) | dự báo xâm nhập mặn xác suất 2026 | 10 links | 0 (news on El Nino probability, see Section 4) |
| 224 | 2026-11-03 | WebSearch (standard) | conformal prediction salinity | 20+ links | 0 (USGS quantile and Bayesian salinity uncertainty items, not conformal; not opened) |
| 225 | 2026-11-03 | WebSearch (extended) | salinity forecast "relative economic value" OR "cost-loss" estuary Mekong 2026 decision sowing | 9 links | 2 (Tran 2025 STOTEN; Cong 18(10)) |
| 226 | 2026-11-03 | WebSearch (standard) | Gerritsma "Forecasting Salt Intrusion in Estuaries" TU Delft thesis | 10 links | 0 (search could not find the thesis; Wullems 2023, Wegman 2026 dissertation, Gerritsma et al. JGR Oceans 2025 on storm surge and salt intrusion appeared; not opened) |
| 227 | 2026-11-03 | WebFetch | doi.org/10.4233/uuid:f059bc44-... then resolver.tudelft.nl | redirect, then connection refused (ECONNREFUSED) | n/a |
| 228 | 2026-11-03 | WebSearch (standard) | "reconstructing incomplete daily river salinity records" Mekong Delta Earth Science Informatics | 10 links | 0 (surfaced only 10.1007/s41748-026-01090-x, a different paper, see Section 3) |
| 229 | 2026-11-03 | WebSearch (standard) | Nguyen Phuoc Cong Downes salinity forecasting Mekong Delta uncertainty OR probabilistic OR conformal 2026 | 10 links | 2 (Cong 18(10), 18(19)); no uncertainty method in the snippets (full text not read) |

## 2. Verdict per claim

### (i) Multi-station salinity forecast verified against an operational national forecast

**Verdict: HOLDS** as a search-scope statement (with the wording fixes E3-E4 of 02/11).
- New searches (rows 183-196, 209-213, 222-229) found no multi-station salinity forecast scored against NCHMF or any other operational forecast.
- The closest work remains Steenman and Stolp 2026 (NCK abstract, one Dutch station, benchmark against the operational OSR model, 02/11 row 157).
- New and unread: A. Gerritsma (2026), "Forecasting Salt Intrusion in Estuaries", TU Delft dissertation (10.4233/uuid:f059bc44-6aa7-4df8-b9e7-af52817b562e, record verified, abstract unavailable). By title and DOI it is estuarine salt-intrusion forecasting in the Delft group that produced Wullems 2023. It is Dutch, not Mekong, and I cannot say whether it benchmarks against an operational forecast. If the owner wants the strictest statement, someone must read it (TU Delft repository, unreachable from this machine today).
- No competitor output changes this (Section 4).

### (ii) Conformal prediction intervals for salinity forecasts at stations or provinces left out of training

**Verdict: MUST BE NARROWED** (unchanged from 02/11; nothing new makes it worse or better).
- Closest remains Nguyen H.T.T., Tran H.M.T., Le G.S. (2026), Zenodo doi:10.5281/zenodo.23497554: 90% cross-conformal intervals for reconstructed daily peak salinity at 34 stations. It is reconstruction, not forecasting, and has no leave-station-out or leave-province-out test.
- Their journal article is still not indexed in Crossref or OpenAlex (rows 215-216, 228), and the Zenodo record is unchanged since 20/10/2026 (row 218). I cannot say whether it is published or what it now says. If it appears before submission, re-read it: a revised version could add a forecasting or spatial-holdout design.
- Pal et al. (2026), doi:10.68277/kjwe.2026.11 (TDS, random split, no lead time) remains the other nearest work. Nothing new in conformal salinity: rows 190, 197, 207, 224 returned no conformal salinity forecast.
- Use E1 of 02/11 (narrowed wording citing both).

### (iii) Relative-economic-value comparison of probabilistic and official deterministic salinity forecasts

**Verdict: HOLDS** as a search-scope statement.
- Rows 179, 203, 206, 225 found no REV or cost-loss application to salinity forecasts. The 19 works citing An-Vo 2021 (row 170) are about seasonal rainfall or climate forecasts; none is about salinity.
- The three works that cite Tran et al. 2025 are Tran and Le 2025 Water (known), and two off-topic papers (row 169).
- Closest stay: Tran et al. 2025 STOTEN (OpenAlex/Crossref title: "Is it worth it? Land-fallowing and saltwater intrusion control under uncertainty"; authors Tran, Le, Durand-Morat, Nguyen, Bairagi, Huynh, Tran; Crossref confirms 966:178711, Feb 2025). It values better intrusion forecasts at delta scale from assumed accuracy gains. It is not a REV comparison of probabilistic versus deterministic forecasts.

### (iv) Cost/loss evaluation of a seasonal salinity forecast for a sowing decision

**Verdict: HOLDS** as a search-scope statement.
- No seasonal salinity forecast newer than Apel et al. 2020 turned up. Apel has no citing work after 2026-11-01 (row 176), and none of the 18 earlier citers was a seasonal forecast (02/11 row 138).
- The citing-work checks that failed on 02/11 are now done (rows 169-175). Nothing among the citing works of Tran 2025, An-Vo 2021, Cong 2026 (both), Nguyen 2026 RSASE, Le 2025 or Mills 2025 combines a salinity forecast with a sowing or planting decision.
- Of the Mills 2025 citers, the two relevant ones were already known (Nguyen H.T.X. et al. 2026 J. Agric. Econ., 10.1111/1477-9552.70042; Minh et al. 2026, 10.1007/s10653-026-03022-0).
- Context only: the Frontiers in Climate 2026 review "Economic value of agro-meteorological services" (10.3389/fclim.2026.1741828) cites An-Vo 2021; it is a general review, not opened beyond the title.

### Introduction's prior-art description (ML salinity forecasts are point forecasts, mostly one or a few stations, one pooled 44, none tested at stations left out)

**Verdict: HOLDS** with edit E3 of 02/11 (already says "mostly one or a few stations (one study pooled 44)").
- Cong et al. 2026, Water 18(19) is the only new-ish item: multi-day forecasts at Hưng Mỹ and Trà Vinh (from the web summary and the Crossref record, both cited by the manuscript). It is multi-day, point, two stations, no station holdout as far as the abstract shows. The full text was not read for intervals or holdout.
- No 2024-2026 Mekong ML salinity forecast with a leave-station-out test was found in rows 183-229. The only leave-station-out salinity work remains Nguyen D.Q.H. et al. 2026 RSASE, a satellite nowcast (not a forecast).
- Cong 18(10) cites no one outside the group and is cited only by Cong 18(19) (rows 171-172): the CTU line of work has not been picked up by other authors yet.

## 3. Works the manuscript should cite or know about (verified in this session)

Nothing new that must be cited. Everything the manuscript needs is in Section 3 of the 02/11 file.

Optional or "know about":
1. **Gerritsma A. (2026)**, "Forecasting Salt Intrusion in Estuaries", dissertation, TU Delft, 2026-10-26, doi:10.4233/uuid:f059bc44-6aa7-4df8-b9e7-af52817b562e. Record verified (OpenAlex, DataCite); abstract not read. Know about; cite only if its abstract shows an operational benchmark or intervals, and then reconsider the "closest international work" sentence (E3 option).
2. **Thuy, Ishidaira, Souma, Magome (2026)**, "Machine Learning-Based Multivariate Time Series Imputation for Long Continuous Gaps in Surface Water Salinity Monitoring Data", Earth Systems and Environment, doi:10.1007/s41748-026-01090-x (Crossref record opened, created 2026-02-27). Gap filling, not forecasting; the web summary attributes it to the Sài Gòn-Đồng Nai system. It shares authors with Do Dang et al. 2025 (already in the 02/11 list). Optional beside the HCMUNRE reconstruction when citing imputation.
3. **Nguyen, Doan, Tran et al. (2026)**, "Operational Effectiveness of The Cai Lon - Cai Be Irrigation System in Salinity Intrusion Control and Sustainability...", doi:10.64599/gbrs8458 (Crossref, created 2026-09-28, title read only). Possibly useful for the inside/outside sluice split of Layer A; title only, not opened.
4. **Mekong 2026-27 outlook (news only, not citable as science):** several Vietnamese news items (27/10/2026) report a very high probability of a strong El Nino from late 2026 and early, severe salinity from November. This bears on the planned live 2026-27 forecasts and on the out-of-sample severe-season story (the 1 November 2026 severe-season probability is the thing to check against it). News items; do not cite as evidence.

## 4. Competitor watch update (03/11/2026)

- **CTU / IGES / UNU** (Cong, Downes, Minh, Kumar, Ty): last salinity-forecast output is still Water 18(19):2379 (24/09/2026). Works since 2026-09-01 (row 209): ctujos water-loss (29/10), microplastics (13/10), Tien Giang water quality preprint (05/10), wave height, droughts, urban heat, riverbank erosion. No uncertainty, conformal or value paper. Water 18(19) has no citing work (row 171), and Water 18(10) is cited only by Water 18(19). The group's publishing cadence is about one salinity-forecast paper every 4 months; a probabilistic follow-up is plausible but not visible.
- **HCMUNRE (Nguyen H.T.T., Tran H.M.T., Le G.S.):** the Earth Science Informatics article "A hybrid deep learning and machine learning framework for reconstructing incomplete daily river salinity records with calibrated uncertainty in the Mekong Delta" is **not published or indexed** as of today (Crossref, OpenAlex, web: rows 215, 216, 228). The Zenodo record is unchanged since 20/10/2026. No salinity *forecasting* output from the group (row 212). Their other outputs are geotechnical and seepage code records, several per month: this group posts to Zenodo often, so recheck Zenodo on the day before submission.
- **RSASE group (Nguyen D.Q.H., Nguyen T.A., Tran T.K.):** RSASE paper (28/09/2026) has no citing works; nothing new (row 211). The group's August-September output is water-quality and biogeochemistry in Sài Gòn-Đồng Nai.
- **Arkansas group (Tran D.Q., Le K.N., Durand-Morat):** the author match now works through OpenAlex authorship IDs from Tran et al. 2025 and Tran and Le 2025 (Kieu Ngoc Le, Alvaro Durand-Morat). Dat Q. Tran has no author ID in those records, so his works are searchable only by name (row 214: nothing new). Nothing on salinity since September (row 210).
- **Kantoush / Doan Van Binh / Ngô Trần Sang:** ISE 2026 abstract only; no new salinity work since 2026-09-01 (row 213). A "Proposal Construction Measures for Adapting to Salinity Intrusion in Mekong Estuaries" (10.64697/iahr-apd2024_p075, 21/08/2026, authors Mai, Binh, Kantoush) is adaptation planning, not forecasting (title only).
- **Apel:** no new salinity output; no citing work after 2026-11-01.
- **New names:** none relevant. Gerritsma (TU Delft) is a new international entry in estuarine salt-intrusion forecasting (Section 3, item 1).

## 5. Remaining gaps

1. **Semantic Scholar:** 6 of 6 queries failed with HTTP 429 after 3 retries at 30 s (rows 177-182). Second consecutive day; no further retry is worthwhile today. Google Scholar remains unusable from here. Mitigation: OpenAlex, Crossref, Zenodo and web search covered the same queries.
2. **OpenAlex coverage is limited to the top 200 of each result set** where the total was above 200 (rows 183, 184), and to titles/authors (no abstracts screened). A recent paper whose title does not mention salinity, forecasts or the Mekong would be missed. OpenAlex indexing lags by days to weeks, so works from the last week may not be in it yet; the same holds for Crossref (created date) and Zenodo (newest 25 only, row 204-208 sort by date, not relevance).
3. **HCMUNRE Earth Science Informatics article:** unavailable. Its text could include a forecasting or spatial-holdout design; the claim (ii) wording depends on that. Check Springer (Earth Science Informatics) and Zenodo again just before submission.
4. **Gerritsma dissertation:** abstract unread (TU Delft host refused the connection).
5. **Cong et al. 2026 Water 18(19) full text:** not read for any uncertainty or holdout design; relied on the Crossref record and web snippets.
6. **Dat Q. Tran:** no OpenAlex author ID in the sampled records; name-based Crossref search only.
7. **Not searched today:** arXiv, Europe PMC and the Vietnamese-language Crossref/OpenAlex queries of 02/11 were not rerun (they returned nothing on 02/11 and the window since is two days). Rerun them with the date filter on the day before submission, together with items 3-4.
8. **Wording items from 02/11 still open for the owner:** "pre-registered" (C5), "public benchmark", and the 1/2/4 g/L threshold citation. Not part of this check; unchanged.
