# Data feasibility: VMD salinity forecast -> calibrated risk -> farm decision (checked 2026-11-01)

Scope: student team, laptop + GEE (noncommercial), no field budget, no agency contacts.
"Checked" = opened/downloaded this session. "Snippet" = search-engine text only (site blocked or not opened).
"Not verified" = not confirmed. Not legal advice on licences.

## 0. Bottom line

- **No open, continuous (hourly/daily) station salinity series for the VMD after 2016 was found.** Every recent ML paper
  checked uses SRHMC/SIWRR/NCHMF data that it does not release.
- **What can be assembled without agencies** is a *coarse* target: the 10-day maximum salinity (Smax, g/L) at 28 named
  stations from NCHMF bulletin PDFs (2024-2026 confirmed, plus 2021-22 as an ODV CSV), plus near-daily or weekly
  "max salinity" maps from the Southern Regional center (2020-2024, ~40 stations, JPG maps, hand transcription), plus
  older open records (Son Doc 1996-2016; annual/monthly maxima at Tra Vinh and Cau Quan 1990-2016).
- That supports **dekadal exceedance forecasts (P[Smax > 1, 2, 4 g/L] next dekad) at ~28 stations over ~5-6 seasons**,
  not daily or hourly forecasts. The decision layer can be built from open data at **province/season level**. Validating
  decisions against real farm losses is only possible at **province level, district level for a few events**.

## 1. Salinity observations (the crux)

| # | Source | URL | Coverage | Format | Licence / terms | Effort | Verdict |
|---|---|---|---|---|---|---|---|
| 1a | NCHMF (national forecast centre, KTTV) "Tin dự báo xâm nhập mặn trên khu vực Nam Bộ" | listing https://kttv.gov.vn/kttv/vi-VN/1/xam-nhap-man-20-18.html ; PDFs `https://kttv.gov.vn/upload/thuyvan{1,2}/YYYY/M/D/dbqg_xman_YYYYMMDD_1500.pdf` | **Checked** (20/03/2024 PDF, text layer): Table 1 = **observed Smax (g/L) for the past 10 days at 28 stations** (name, river, province, km from mouth, comparison to the same month last year): Cát Lái, Bến Lức, Xuân Khánh, Tân An, Tuyên Nhơn, Vàm Kênh, Hòa Bình, An Định, Bình Đại, Lộc Thuận, An Thuận, Sơn Đốc, Bến Trại, Hương Mỹ, Hưng Mỹ, Cầu Quan, Trà Vinh, Trà Kha, Long Phú, Đại Ngãi, Trần Đề, Thạnh Phú, Sóc Trăng, Gành Hào, Sông Đốc, Rạch Giá, Gò Quao, An Ninh. Table 2 = **the official Smax forecast for the next dekad** (a ready-made operational benchmark). Also gives the 4‰ intrusion length per estuary and weekly max water levels at Tân Châu, Châu Đốc, Vũng Tàu. Issued on the 10th, 20th and last day of each month, Dec/Jan-May/June. Dates confirmed by curl/search: Jan 2024-May 2026. Early-2024 files and 2020-2023 PDFs were not found at this path (different file names?); **archive before 2024 not verified**. | PDF with a text layer (tables can be parsed with PyMuPDF) | Footer "© Trung tâm Dự báo KTTV quốc gia"; no reuse terms page found. Publicly issued forecasts; republishing transcribed numbers with attribution is probably tolerated but **not verified**. Safe option: release code + derived scores, and ask NCHMF for written permission before releasing the table. | Low-medium: scraper + table parser; ~15 bulletins x 28 stations per season | **Usable with effort**. The best public target series, but dekadal maxima only. |
| 1b | Open Development Vietnam: "Saline intrusion in the Southern region Vietnam" (NCHMF bulletin tables as CSV) | https://data.opendevelopmentmekong.net/dataset/saline-intrusion-in-the-southern-region-vietnam | **Checked page**: 1 Jan 2021-13 Apr 2022; station, river, province, km to mouth, Smax per period (g/L); EN + VN CSV | CSV | Listed CC BY-SA 4.0 (ODV's own licence over NCHMF numbers; the underlying rights are NCHMF's) | Low | **Ready** (fills the 2021-22 gap of 1a) |
| 1c | Southern Regional Hydro-Met Center (Đài KTTV khu vực Nam Bộ), section "Hạn mặn" | https://www.kttv-nb.org.vn/index.php/thong-tin-kttv/han-man (TLS certificate expired on 01/11/2026) | **Checked**: 326 posts listed, 31/03/2020 to 31/05/2024 ("Bản tin mặn", "Bản đồ mặn lớn nhất ..."). Posts are **JPG maps of observed max salinity at measuring points**: e.g. 6/12-7h 7/12/2021 (daily) and 27-31/05/2024 (5-day); about 36-40 stations with values, ~46-49 "no data". Bulletins in 2020-21 were roughly weekly, from Dec 2021 on also daily (not verified for every season). Also XMAN PDFs (e.g. NABO_XMAN_20250120_1530.pdf). | JPG map images (labels overlap; some values hidden) and PDFs | "Nguồn: Đài KTTV khu vực Nam Bộ"; no reuse terms found (**not verified**) | **High**: hand transcription or OCR of hundreds of maps, with QC for hidden labels | **Usable with effort**. The only near-daily public series 2020-2024. |
| 1d | SIWRR (Viện KH Thủy lợi miền Nam) "Dự báo mặn ĐBSCL" | https://siwrr.org.vn/?gid=93 (63 items, 2016-2026); weekly/monthly bulletins for Cái Lớn-Cái Bé-Xẻo Rô operation under ?gid=540 | **Checked** one bulletin (12/3/2020, scanned PDF): narrative forecast + 4 g/L intrusion length per estuary (e.g. Hàm Luông 70-75 km). **No station tables** in that one; others not opened. | Scanned PDF | "© SIWRR"; reuse with credit "Viện Khoa học Thủy lợi miền Nam / SIWRR.ORG.VN" (site footer) | Medium | **Not usable as observations**; usable as a benchmark for forecast intrusion length and for gate-operation context |
| 1e | VNDMS (disaster portal, now https://vndms.gov.vn) | https://vndms.gov.vn | **Checked**: salinity warning layers (>1‰, >4‰) and intrusion boundaries for 2016, 2020, 2021, 2022, multi-year mean; Excel export only for rainfall/flood panels; account features need login. "Bản quyền Cục QLĐĐ & PCTT"; the /dieukhoan page is only a privacy policy. | Web map | All rights reserved | - | **Not usable** for station series; boundary layers maybe as a qualitative check |
| 1f | MRC Data Portal | https://portal.mrcmekong.org | Hydrology, water quality (conductivity monthly), sediment; **salinity at Vietnamese delta stations not verified**. Portal is a JS app (not readable by fetch). Third-party catalogues list the licence as "Other (Not Open)"; free account needed to download. Older MRC licences (2005) forbid passing data to third parties without permission. | Web/CSV | Non-commercial; redistribution needs MRC permission (old licence; **current terms not verified**) | Low to download | **Not usable** for salinity (not shown); see 2a for discharge |
| 1g | GFZ: Apel et al., "Surface water salinity measurements at Son Doc, Ben Tre ... and monthly discharge of Tan Chau" | https://doi.org/10.5880/GFZ.4.4.2024.004 | **Checked metadata**: Son Doc (Hàm Luông) 1996-2016, dry season only, usually 2-hourly over several consecutive days with gaps; Tan Chau monthly Q 1995-2016 (pre-1995 reconstructed). Source SRHMC. | Data files (GFZ) | **CC BY 4.0** | Low | **Ready** (one station, historic) |
| 1h | Mendeley: Binh et al. 2019 "Long-term discharges, water levels, salinity ... Mekong" | https://data.mendeley.com/datasets/fm996rrfyz/2 | **Checked file**: one xlsx; sheets "Max. salinity" = **annual max** at Tra Vinh and Cau Quan, plus **monthly max (Jan-Jun)** at Cau Quan, 1990-2016; Q sheets are period-mean climatologies; WL Tan Chau/My Thuan annual stats | XLSX | **CC BY 4.0** | Low | **Ready** but coarse (monthly/annual maxima) |
| 1i | Zenodo: Eslami & Nguyen Trung Nam, SIWRP gauge data 2015 | https://zenodo.org/records/4771261 | **Checked**: WL, Q, salinity, 1 Feb-15 Apr 2015, stations not listed | Files on request | **Restricted**: SIWRP approval, non-commercial | Needs request (a formal request, not a contact) | **Not usable** without approval |
| 1j | Zenodo: Nguyen Dam Quoc Huy et al., monthly 30 m surface salinity maps 2015-2025 (data of the RSASE 2026 transferability paper) | https://zenodo.org/records/20003854 | **Checked**: monthly PSU GeoTIFFs 2015-2025 (Tien, Hau, Co Chien, Ham Luong, Cua Dai), RF model (joblib), GEE scripts, **station list (21 stations) but no in-situ values** ("without requiring access to the raw in-situ observation data"). Wet season months are extrapolations. | GeoTIFF + code | **CC BY 4.0** | Low | **Usable** as a gridded covariate/prior; **not** as ground truth (model output) |
| 1k | Zenodo: Wang et al. 2025, soil salinity + NDWI dry-season maps 2000-2023 (Commun. Earth Environ. 6, 503) | https://zenodo.org/records/15653696 | Checked page: annual dry-season Landsat-derived soil salinity; validation not shown on the page | GeoTIFF (7.4 GB) | CC BY 4.0 | Low | Usable as context only (model product, soil not river salinity) |
| 1l | Real-time networks: RYNAN Mekong app/IoT buoys; Reecotech/Bewaco online stations (Bến Tre); Mekong Salt Lab (Trà Vinh); MRSS (waterdata.vn/mekong/mrss); UNEP-DHI/VNMC sharing platform | rynan.vn (up); waterdata.vn and mekong.rynan.vn did not answer | Snippets: RYNAN buoys installed 2018-2021, used in a 2026 Kyoto paper; MRSS draws on ~20 stations 2016-2020; UNEP-DHI platform "in development" | Apps/dashboards | Proprietary/private; no API terms found | Scraping: unreliable (apps) and probably against terms | **Not usable** without agreement (**not verified**) |
| 1m | Provincial DARD/thủy lợi reports, VDDMA | - | Snippets only: provinces issue sowing calendars and closure notices, no station series found | PDF/news | - | High | Not usable as series |
| 1n | Official purchase: Trung tâm Thông tin và Dữ liệu KTTV (and regional centres) sell station data under the fee schedule of Thông tư 197/2016/TT-BTC (consolidated 16/VBHN-BTC 2019). | https://caselaw.vn/van-ban-phap-luat/339893-... (snippet) | Any station, hourly if measured | Paid data supply | Purchased data usually may not be redistributed (**not verified**) | A formal application + fee; **needs no personal contact** | **Usable with money**. The route to a daily or hourly target. |

### Data availability of the named VMD salinity ML papers

| Paper | Data used | Data statement |
|---|---|---|
| Bui, Luu, Ha, Do, Tran 2025, *Adv. Space Res.* 76(3):1417-1437, doi:10.1016/j.asr.2025.05.055 (pii S0273117725005368), "Surface water salinity modeling ... using hourly salinity observed data, remote sensing, and ML" | Hourly observed salinity (68 stations per the brief; **not verified**) | **Not verified** (ScienceDirect 403) |
| Cong, Downes, Minh, Kumar 2026, *Water* 18(19):2379, doi:10.3390/w18192379 (XGBoost/LSTM/hybrid) | **Checked**: one station (Vàm Kênh), 721 daily means, Feb-May 2020-2025; predictors My Thuan Q/WL and Ba Tri air temperature; agency not named | "The original contributions presented in this study are included in the article. Further inquiries can be directed to the corresponding author." = **no data released** |
| Same group, *Water* 18(10):1240 (2026), Cung Hau | **Checked**: daily mean at Hưng Mỹ and Trà Vinh, 2000-2024 | Same wording = **not released** |
| Phong Nguyen Duc et al. 2025, *Discover AI* 5:79, doi:10.1007/s44163-025-00336-3 (CC BY-NC-ND) | **Checked**: hourly, 1 Jan 2015-29 Feb 2020, Trà Vinh, Bến Trại, Cầu Quan, Trần Đề (44,592 obs); SIWRR + SRHMC network | "Raw data ... are not publicly available to preserve individuals' privacy" (GDPR boilerplate) = **not released** |
| Nguyen Dam Quoc Huy, Nguyen Truong An, Tran Thi Kim 2026, *Remote Sens. Appl. Soc. Environ.* 44:102297, doi:10.1016/j.rsase.2026.102297 (pii S2352938526004301) | 21 stations (from its Zenodo CSV), HLS + S1 + forcing | Maps/model/code on Zenodo (CC BY 4.0); **in-situ values withheld** |

Pattern: no paper released station values; at most "on request". Reviewers will accept a public-bulletin target only if it is
described honestly as the 10-day max.

## 2. Forcings

| Item | Source / URL | Coverage | Format | Licence | Effort | Verdict |
|---|---|---|---|---|---|---|
| Upstream discharge, observed | MRC portal (Kratie daily Q, Tân Châu/Châu Đốc WL) | Owner's earlier note (this repo's CLAUDE.md): on MRC, Tân Châu (019803) = water level only (manual 1979-, telemetry 2010-), **no discharge**; Kratie Q present (**not re-verified**) | CSV after free login | "Not open"; redistribution needs permission (not verified) | Low | **Usable with effort** (use; do not redistribute raw) |
| Hourly Q 2005-2015 | NERC EIDC, Darby et al. 2020, doi:10.5285/ac5b28ca-e087-4aec-974a-5a9f84b06595 | Châu Đốc, Tân Châu, Cần Thơ, Mỹ Thuận, hourly, 2005-2015 (ADCP-based) | CSV | Open Government Licence (snippet) | Low | **Ready** (historic only) |
| Weekly WL in bulletins | NCHMF PDFs (1a) | Tân Châu, Châu Đốc, Vũng Tàu weekly max, forecast tide peaks | PDF | as 1a | Low | Usable (coarse) |
| Modelled discharge | GloFAS v4 reanalysis + forecasts (Copernicus EWDS) at Kratie | 1979-present daily | NetCDF/API | CEMS data believed CC BY 4.0 (**not verified** this session) | Low-medium | **Ready** as a fallback for operational lead time |
| Tides | FES2022 (AVISO, free registration; used by the 1j dataset), TPXO9/10 (OSU, free academic licence), `pyTMD` | Global, any time | NetCDF + code | Free for research; redistribution of model files not allowed, derived series fine (**not verified**) | Low | **Ready** |
| Tide gauge | UHSLC station 383 / PSMSL 2268 "Vung Tau II" | 2007-2018, 93% complete (snippet) | Hourly/daily | UHSLC/PSMSL open | Low | Usable (ends 2018; Vietnamese gauges not public) |
| Rainfall / ET | GEE: CHIRPS daily (UCSB-CHG/CHIRPS/DAILY), GPM IMERG V07, ERA5-Land daily | 1981-/2000-/1950-present | GEE | Open (Copernicus licence for ERA5: free reuse with attribution) | Low | **Ready** |
| ENSO | NOAA CPC ONI / Niño3.4 | 1950-present monthly | Text | Public domain | Trivial | **Ready** |
| Sea level | Copernicus Marine / C3S altimetry SLA | 1993-present daily | NetCDF | Free registration, attribution | Low | **Ready** |

## 3. Remote-sensing salinity proxies

- Salinity is not optically active; band relations work through co-varying turbidity/sediment/CDOM, so they are site- and
  season-specific. Reported fits: Landsat 8 vs 11 stations (2014), R > 0.8 (exponential on PCA bands); Sentinel-2 + RF vs
  40 stations (2015-2023), R² 0.84, RMSE 3.65 g/L (IAHR 2026 abstract, snippet); Bayesian merging of Landsat + model, NSE
  0.73 vs 0.67 Landsat alone (ESS Open Archive, snippet). The RSASE 2026 paper (1j) is explicitly about poor **spatial
  transferability** of such models, which "physics-aware" features (discharge, tide, distance) only partly fix.
- Image dates are sparse (16-day Landsat, 5-day S2, clouds) and capture one tidal phase; an RMSE of ~3-4 g/L is as large as
  the 1-4 g/L decision thresholds for rice.
- **Verdict: not usable as a target or as validation.** Usable at most as a covariate or as the 1j gridded prior, with the
  caveat that it is model output trained on undisclosed station data.

## 4. Decision-layer inputs

| Item | Source / URL | Coverage | Format | Licence | Effort | Verdict |
|---|---|---|---|---|---|---|
| Crop calendar (province) | RiceAtlas (Laborte et al. 2017, Sci. Data, doi:10.1038/sdata.2017.74; CGSpace) | Province-level seasons (WS, SA, AW), planting/harvest windows, ~2010s | Shapefile/CSV | CC BY 4.0 (CGSpace record) | Low | **Ready** (static, old) |
| Crop calendar (official, per season) | Cục Trồng trọt và BVTV advisories; provincial DARD "lịch xuống giống" (e.g. Trà Vinh notice 655/TB-SNN 2023 gives calendars by commune/hamlet: https://snnptnt.travinh.gov.vn/SiteFolders/snn/Nam_2023/TT_can_biet/655_TB_SNN.pdf) | Per season, per province, sometimes per commune | PDF/news | Official documents (public) | Medium-high (collect per province and year) | **Usable with effort** |
| Sowing date / phenology maps | No ready open S1 rice-calendar dataset for the VMD found (studies: An Giang 2017-18, coastal 2015/16/19/20, OA 85%) ; RICA (MODIS, Asia) on 4TU: CC BY-NC-SA, partly "on request" | - | - | - | Build yourself in GEE from S1 GRD (well-established method) | **Usable with effort** (own product; validate with calendars) |
| Sluice/gate locations | OSM (Overpass, this session): only **39** waterway=sluice_gate/weir/lock_gate features and ~116 features named "Cống/Đập" in the whole delta (many not sluices) vs thousands of real sluices; MRC irrigation headworks (2001, archive) | - | - | ODbL / MRC | - | **Not usable** as an inventory; hand-digitise the few major ones (Cái Lớn-Cái Bé, Ba Lai, Bến Tre system) |
| Gate operation records | None public. Closure notices in news (e.g. Kiên Giang closes Cái Lớn gates 14-17/3/2024; 3‰ rule at Cái Bé); SIWRR weekly operation bulletins (1d); a 2026 VAWR paper (No. 94) used 2021-2023 gate logs + 25 stations (not public) | - | News/PDF | - | High | **Not usable** beyond event dates from news |
| Rice salt tolerance | FAO/USDA (Maas-Hoffman; Ayers & Westcot 1985): paddy rice ECe threshold **3.0 dS/m, slope 12%/dS/m**, "sensitive"; Grattan et al. 2002 (Calif. Agric.): yield loss above **1.9 dS/m** seasonal field-water EC; seedling and 3-leaf-to-panicle-initiation most sensitive. Vietnamese: TCVN 11199:2016 (irrigating rice on saline soil) sets stage limits (values **not verified**); CLRRI: >80% plant death at 4-6‰ for a month at seedling stage. | Literature | - | Citable | Low | **Ready** (convert g/L to dS/m ~ x1.5-1.7; state the assumption) |
| Yield | GSO/NSO PX-Web (province x season: area, yield, production; **not re-verified this session**); provincial statistical yearbooks (district level, PDF) | Province annual/season 1995-2024 | PX-Web/PDF | Public statistics | Low (province), medium (district) | **Ready** at province level. **Break**: 63 -> 34 provinces from 1/7/2025 and districts abolished (two-tier local government), so the series from 2025 onward needs crosswalks and district series end in 2024 |
| Prices | World Bank Pink Sheet (Viet Nam 5% broken, monthly; CC BY 4.0); provincial/news farm-gate paddy prices; AGROINFO (paid) | Monthly | XLSX/news | Open / mixed | Low | **Ready** (export) / usable with effort (farm-gate) |
| Farm costs | No open per-season cost dataset found; costs appear in DARD news and academic surveys (CTU/IRRI) | - | - | - | Medium | **Usable with effort** (literature ranges + sensitivity analysis) |
| Household surveys | VHLSS microdata from GSO: licensed request with fees, redistribution forbidden (typical NSO terms; **VHLSS-specific terms not verified**); VARHS (UNU-WIDER, 12 provinces incl. Long An; **not verified**) | Biennial | Microdata | Restricted | Medium-high (formal request) | Not needed for a first paper |

## 5. Validation of decisions (actual losses)

- **2015-16**: UN/OCHA situation updates (ReliefWeb; e.g. update no. 4, 11 Jul 2016) and dmc.gov.vn disaster record "dis165"
  (rice area by severity band, households, VND damage, by province, dated March 2016; site returned 503 to fetch, snippet only).
  Kiên Giang 34,000 ha rice loss etc. **Province level.**
- **2019-20**: MARD/press totals: ~41,900 ha winter-spring rice affected, ~26,000 ha total loss in 6 provinces; Trà Vinh 28,500 ha;
  Cà Mau 16,500 ha; **district only sporadically** (Bến Tre: Ba Tri 4,428 ha, Giồng Trôm 631 ha, SGGP).
- **Commune-level loss records: none public found.** DesInventar Viet Nam not confirmed (not verified).
- Satellite alternative: paddy loss maps (Wang et al. 2025; 1k), or own S1/S2 crop-failure mapping in 2016, 2020, 2024 as
  a proxy "loss" label (must be validated against the province totals above).
- **Verdict:** decision regret can be evaluated against **province-season loss totals for 2016, 2020 (and 2024)** and against
  satellite crop-failure maps; **not** against farm or commune outcomes.

## 6. Minimum assemblable dataset (no agency collaboration)

1. Target: NCHMF dekadal observed Smax, 28 stations, Jan 2024-May 2026 (scraped PDFs) + ODV CSV 2021-22 + Southern-center
   maps 2020-2024 transcribed for ~15-20 estuary stations -> ~6 dry seasons x ~15 dekads x ~20-28 stations
   (about 2,000-2,500 station-dekads; strongly autocorrelated, only 6 independent seasons including 2020 and 2024 extremes).
   Historic context: Son Doc 1996-2016 (GFZ), Cau Quan/Tra Vinh monthly/annual max 1990-2016 (Mendeley).
2. Benchmark: NCHMF's own Smax forecasts (Table 2) and SIWRR intrusion-length forecasts = the operational baseline to beat.
3. Forcings: MRC Kratie Q (use only), GloFAS Kratie, EIDC hourly Q 2005-2015, FES2022/TPXO tide at estuary mouths,
   CHIRPS/ERA5-Land/IMERG in GEE, ONI, altimetry SLA.
4. Decision: RiceAtlas + DARD calendars + own S1 sowing-date maps; FAO/Grattan thresholds; GSO province yields; Pink Sheet
   prices; cost ranges from literature.
5. Validation: province-season damage totals 2016/2020/2024; S1/S2 crop-failure maps.

## 7. Biggest gaps

1. No daily/hourly station series after 2016 in the open: the target is a 10-day maximum, and 2020-2024 needs transcription.
2. Only ~6 seasons: calibration/coverage claims will rest on few independent years (block/season-wise conformal needed).
3. Licence of transcribed bulletin numbers not confirmed; redistribution of MRC/purchased data not allowed.
4. Gate operations unknown (Cái Lớn-Cái Bé since 2021-22 changes the system behind the stations).
5. No commune/farm loss records: "regret" can only be evaluated as a modelled quantity or against province totals.
6. Province merger (2025) breaks yield/admin series.

## 8. Collaboration that would change the verdict

- Not strictly required for a dekadal, station-level exceedance-forecast paper.
- For daily/hourly forecasting: a **paid formal data request** to the KTTV data centre (Thông tư 197/2016/TT-BTC fee
  schedule; no personal contact needed, but redistribution likely barred), or a co-author from SIWRR/CTU/SRHMC.
- For gate operations and commune losses: provincial DARD/Irrigation Management companies (would need a partner).
- Low-cost step: email NCHMF asking permission to republish the transcribed bulletin tables (a permission request, not a
  collaboration).

## Sources opened or used (this session)
- NCHMF bulletin 20/03/2024: https://kttv.gov.vn/upload/thuyvan2/2024/3/20/dbqg_xman_20240320_1500.pdf ; listing https://kttv.gov.vn/kttv/vi-VN/1/xam-nhap-man-20-18.html
- Southern center: https://www.kttv-nb.org.vn/index.php/thong-tin-kttv/han-man (map JPGs 07/12/2021, 31/05/2024)
- SIWRR: https://siwrr.org.vn/?gid=93 ; bulletin https://www.siwrr.org.vn/docs/2018/files/Bantin_VKHTLMN.pdf
- VNDMS: https://vndms.gov.vn
- ODV CSV: https://data.opendevelopmentmekong.net/dataset/saline-intrusion-in-the-southern-region-vietnam
- GFZ: https://doi.org/10.5880/GFZ.4.4.2024.004 (via b2find)
- Mendeley: https://data.mendeley.com/datasets/fm996rrfyz/2
- Zenodo: https://zenodo.org/records/4771261 ; https://zenodo.org/records/20003854 ; https://zenodo.org/records/15653696
- Papers: Crossref records for 10.1016/j.asr.2025.05.055, 10.1016/j.rsase.2026.102297, 10.1007/s44163-025-00336-3; MDPI PDFs w18192379, w18101240; Springer page of s44163-025-00336-3
- EIDC Mekong discharge: https://www.data.gov.uk/dataset/f786782a-073a-438e-ab6a-1c4afa39fb79
- PSMSL Vung Tau II: https://psmsl.org/data/obtaining/stations/2268.php
- Overpass API (OSM sluice count), this session
- Snippets only: ScienceDirect (403), dmc.gov.vn (503), RiceAtlas/CGSpace, USDA salt tolerance, Grattan 2002, ReliefWeb/press damage figures, Thông tư 197/2016 fee schedule, Trà Vinh DARD calendar
