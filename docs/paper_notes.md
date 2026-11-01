# Paper notes (results, numbers, decisions)

## 01/11/2026 — G0 inventory, step 1 (NCHMF bulletins, live site)
- Script `scripts/probe_nchmf.py`; inventory `data/raw/nchmf/inventory.csv` (gitignored); PDFs `data/raw/nchmf/pdf/`.
- Live kttv.gov.vn path `upload/{thuyvan1|thuyvan2}/YYYY/M/D/dbqg_xman_YYYYMMDD_1500.pdf`; both folders in use, no rule.
- Found live: 30 bulletins, 20/03/2024 to 31/05/2026. Per season (of 21 canonical dates Dec-Jun): 2023-24 = 7,
  2024-25 = 14, 2025-26 = 9. Nothing live for 2016-17 to 2022-23 (every canonical date 404 in both folders).
- Listing page only shows 6 posts (31/03-20/05/2026); useless for history.
- Text layer present in all checked years (2024, 2025, 2026): "Bảng 1", "Bảng 2" and station names extractable.
  Station count and layout consistency not yet checked (parser step).
- Wayback Machine holds bulletins that are now 404 live (e.g. 31/01, 10/02, 29/02, 10/03/2024); directory date can
  differ from file date (2024/3/1/dbqg_xman_20240229). Full Wayback enumeration in progress.
- Correction to docs/background/salinity_data.md row 1a: "Jan 2024-May 2026 confirmed" was not reproduced live.
- G0 status: NOT met from the live site alone (<=3 partial seasons). Pending: Wayback, ODV CSV 2021-22,
  Southern centre JPG maps 2020-24.

## 01/11/2026 — G0 inventory, step 2 (parser, G0 table, ODV)
- `scripts/parse_nchmf.py` -> `data/processed/nchmf_obs.csv`, `nchmf_fc.csv` (840 rows each from 30 PDFs);
  self-check on 20/03/2024 passes (e.g. Cát Lái obs 10.4, fc 9.3 g/L). `scripts/g0_stats.py` prints the G0 table.
  Run both with `python -I -X utf8`.
- Layout stable 2024-2026: Bảng 1 p.3, Bảng 2 p.4 (spills to p.5 in 2025-26); 28 stations in every bulletin, same order.
  Text-line parsing, because PyMuPDF find_tables() drops rows that cross the page break.
- Bảng 2 = one number per station (no ranges); 2026 adds "Thời gian xuất hiện" (kept as fc_time_of_max).
- Periods derived from the issue date: three bulletins carry stale headers (20250210 B1, 20250228 B2, 20260410 B1).
- Missing values: "-" only (Rạch Giá mostly missing; fails 80% in 2024-25 and 2025-26). One forecast typo kept raw,
  not corrected: An Định "202" on 20/04/2026.
- Provinces: 2025-26 bulletins use post-merger provinces; a crosswalk is needed before province-level work
  (leave-province-out test, layer A).
- G0 table (30 live files): 2023-24 = 7 bulletins, 2024-25 = 14, 2025-26 = 9; >=27 stations at >=80% of the
  bulletins present, but 0 stations reach 17 of the 21 canonical dates in any season. Bảng 2 parsed in all 30.
- ODV CSV (data/raw/odv/, licence field "cc-by-sa", version not stated in the API; downloaded 01/11/2026): same
  dekads as Bảng 1 but Jan-Mar only; 2021 = 9 dekads, 24 stations >=80%; 2022 = 7 of 9 dekads filled, 25 stations.
  26 of 30 names map to the 28 (Cát Lái, Rạch Giá absent). 2022 river/province columns are shifted: match by name.
- G0 still NOT met: waiting for the Wayback enumeration (targets: Dec-Feb gaps and pre-2024 seasons).

## 01/11/2026 — G0 inventory, step 3 (Wayback Machine)
- Scripts `scripts/wayback_nchmf.py` (modes cdx, cdx2, download; rerunnable) and `scripts/season_table.py`;
  CDX outputs in `data/raw/wayback/`; inventory.csv now has `source` (live|wayback) and `wayback_ts`.
- 19 more bulletins recovered (total 49 PDFs, 32 MB). Nothing found before Jan 2021.
- Pre-2024 files sit on the old domain thoitietvietnam.gov.vn/upload/thuyvan2/ with other names:
  dbqg_xmnb_YYYYMMDD_1530 (2021, 2022), dbqg_xmnb_..._1500 (Feb 2023), dbqg_xmtb_..._1500 (Mar 2023; "tb" to be
  checked). Directory date may differ from file date; some under thuyvan1; one "-1" suffix.
- Canonical dates found per season (of 21): 2020-21 = 3 (+ 05/01/2021 off-canonical), 2021-22 = 12 (Jan-May 2022),
  2022-23 = 3, 2023-24 = 7, 2024-25 = 14, 2025-26 = 9. Dec-Feb gaps of 2021-22, 2022-23, 2023-24 are 404-only captures.
- Archived listing pages (Jul 2022-Sep 2026 snapshots) could locate more posts if fetched near each issue date; not done.
- Parser extended to xmnb/xmtb (glob dbqg_xm*_*.pdf): 49 PDFs -> 1,359 obs rows, 1,355 fc rows; stations per
  bulletin 24-30 (2021 lists vary: Cầu Nổi, Xẻo Rô, Mỹ Tho, Đồng Tâm, Cà Mau appear; Cát Lái/Rạch Giá/Gành Hào
  mostly absent); 27 in 2022-23, 28 from 2024. xmtb files are Nam Bộ bulletins (title checked), kept.
  "Ngã 3 Cát Lái" (2022, Vàm Cỏ, km 20) = Cầu Nổi, not the 2024+ Cát Lái (Sài Gòn, km 58). Second self-check
  on 20/03/2022 passes. `scripts/odv_crosscheck.py`: Bảng 1 vs ODV 261 of 262 equal (one diff: 28/02/2022 Bình Đại
  23.9 vs 23.7) -> ODV is a copy of the bulletins; it adds Jan-Mar 2021 dekads not in the PDFs.
- G0 table (49 files): bulletins per season 4 / 12 / 3 / 7 / 14 / 9 (2020-21 ... 2025-26); stations >=80% of
  bulletins present 23 / 27 / 26 / 28 / 27 / 27; >=17 of 21 canonical dates: 0 in every season; Bảng 2 parsed in
  all 6 seasons. Verdict on the plan's wording: Bảng 2 criterion met; the 5-season criterion met only on the
  "present" denominator, NOT on the canonical-date denominator. Decision on G0 pending (owner).

## 01/11/2026 — Southern centre JPG maps (fallback for G0): not usable for the gaps
- Owner checked the live "Hạn - Mặn" section in a browser: no posts for Dec 2022 and none in all of 2023.
  Early 2024 posts are irregular-window maps (01-12/03/2024) and a monthly map (Feb 2024), not dekads.
- Wayback (data/raw/kttvnb/cdx/): ~325 archived post slugs; 13 in Dec 2021-Feb 2022, none for Dec 2022-Feb 2023
  or Dec 2023-Feb 2024; map images not archived under /images/.
- Demo reading of the 01-12/03/2024 map: ~55 stations, 26 of the 28 NCHMF stations legible, values close to
  NCHMF 11-20/03/2024 (e.g. Bến Trại 29.0 vs 29.0, Cầu Quan 10.2 vs 10.2, Sông Đốc 31.3 vs 31.6).
- Live download with TLS verification off was denied by the Claude Code classifier ([TLS/Auth Weaken]).
- Conclusion: JPG transcription cannot fill the Dec-Feb gaps; option 2 dropped.

## 01/11/2026 — DECISIONS (owner)
- Climate Services is SCIE and JCR Q1 (owner checked, 01/11/2026). First-choice venue: Climate Services.
  APC 2,680 USD; Vietnam-based authors get a 50% waiver (owner) -> ~1,340 USD. Whether the 200 M VND funding pays
  the APC: ask the advisor.
- Crop-option layer uses options 1, 2, 3, 6 (protocol section 8).

## 01/11/2026 — Venue shortlist (docs/background/venues.md; quartiles NOT verified)
- Order proposed: Climate Services (Elsevier, gold OA ~USD 1,500 unconfirmed; An-Vo 2021 published there) ->
  Journal of Hydrology (Elsevier, hybrid, high desk-reject) -> Environmental Modelling & Software (Elsevier);
  alternates Agricultural Water Management, Climate Risk Management. Excluded: HESS/NHESS (public Discussions =
  preprint conflict; 80%), Hydrological Sciences Journal (Q2).
- All JCR quartiles from aggregators or recall; Clarivate/ScienceDirect/Scimago blocked automated fetches. Owner to
  verify in UEH library JCR: quartile per category, SCIE (not ESCI) status of Climate Services / Climate Risk
  Management, APC and whether the 200 M VND funding covers it.

## 01/11/2026 — Crop-option data check (docs/background/crop_options_data.md)
- Data-ready for a break-even: option 1 (standard Đông Xuân rice: Mills et al. 2022 yield 6.5 t/ha, net ~21 M VND/ha
  2017-19; FAO rice 3.0 dS/m, -12%/dS/m), option 2 (early sowing: Ferrer et al. 2022, +8.6-8.8 M VND/ha and +2.5 t/ha in
  the severe 2019-20 season; no cost and no mild-season estimate = the main gap), option 6 (skip, zero revenue).
  Option 3 (salt-tolerant varieties) partly: trial losses 10/30/50%; Mills 2022 field gain +364 kg/ha, no revenue gain.
- Not ready (news/snippets only): option 4 rice-shrimp, option 5 upland crops (FAO tolerances exist for maize, chili,
  mung bean; delta economics news-only). -> move to the later crop paper.
- Gauge g/L -> field ECe link has no source: sweep it (with the sluice exposure factor). Costs need a deflator.
- Agent said "Mills et al. 2025" does not exist: wrong; it is doi:10.1002/jaa2.70004 (profit loss > 75% under high
  salinity) - the intended source for the loss relation. Prior art for H4: Le Phuong-Dung et al. 2025 (agec.70045).

## 01/11/2026 — DECISIONS (owner): layer A option 1 + shallow crop-option layer
- Layer A = severe-season forecast (protocol section 8, redesigned).
- This paper adds a SHALLOW crop-option scenario analysis (break-even probabilities for 3-6 options with cited
  costs/tolerances; decision support, not advice). A deep crop-advisory study is a separate later paper.
- Before committing: an agent checks whether free, citable cost/profit/tolerance data exist for the options.

## 01/11/2026 — Features, protocol draft, long records
- scripts/build_features.py -> data/processed/features.csv (1,478 rows, 1,223 with target; GloFAS lag 5 d; tide from
  Meeus lunar phase/perigee, new moons Jan-Mar 2024 within 0.1 d; ONI season ending month M-2). Self-check passes.
- docs/protocol.md DRAFT v0 written (not frozen). Test seasons 2024-2026; scikit-learn models (LightGBM absent).
- Long records (scripts/tidy_long_records.py; GFZ Sơn Đốc 1996-2016 + Tân Châu monthly Q; Mendeley xlsx, both
  CC BY 4.0 (Mendeley licence to re-check on its page)): Sơn Đốc max(Feb,Mar) > 4 g/L in 21/21 seasons; Mendeley has
  annual maxima only (Cầu Quan, Trà Vinh 1991-2016), monthly at Cầu Quan only 1998/2010/2016. Layer A as planned
  (P(Feb/Mar max > 4 g/L) at 3 stations) is not feasible -> redesign needed (owner).
- Station metadata, two independent agent passes (data/meta/station_meta_A.csv, _B.csv) merged by
  scripts/merge_station_meta.py -> data/meta/station_meta.csv (37 stations):
  - provinces old/new: A and B agree 37/37 (NQ 202/2025/QH15, secondary copy on luatvietnam.vn; check Công báo).
    Bulletins switch to new province names at issue 20/04/2026.
  - coordinates: 19 from Zenodo 20003854 station metadata (Nguyen et al. 2026, CC BY 4.0; gauge vs approximate not
    stated); 18 to verify. Pass A's recalled coordinates differed by up to 10 km (Sơn Đốc, Cầu Quan): discarded.
  - sluice status: 24 kept where both passes agree (reasoning, no boundary map), 13 to verify. No sluice-zone
    boundary map found online for most systems.

## 01/11/2026 — DECISION (owner): no data purchase now
- Wait for NCHMF's reply; write the paper with the data in hand; add data (NCHMF files or paid Thông tư 197 data)
  only if reviewers ask at revision. Pipeline must accept new bulletins/daily series without code changes.

## 01/11/2026 — PCTT daily reports 2020 (+ same date 2016)
- scripts/fetch_pctt_2020.py, parse_pctt_2020.py (self-check passes) -> data/processed/pctt_daily_2020.csv
  (648 rows = 8 stations x 81 report days, 10/02-25/05/2020) and pctt_dekadal.csv (192 rows; 128 complete
  station-dekads = 64 for 2020 + 64 for the 2016 same-date column; complete = >=7 report days).
- Stations: Tân An, Bến Lức, Cầu Quan, Gò Quao (in the 28) + Xuân Hòa, Giao Hòa, Mỹ Hóa, Láng Thé.
- Caveat: the daily statistic is not stated (max? morning reading?), and only 6-9 days per dekad exist, so the
  dekadal values are lower bounds, not NCHMF-style Smax. 2016 dekadal max reproduces the printed 2015-16 season
  max (Tân An 11.8, Bến Lức 12.9, Gò Quao 22.7). Use for the extreme-season check, flagged as a different source.
- Table date can differ from the page slug date by one day (17/02, 05/03, 29/04): join on table date.
- No terms of use found: score-only.

## 01/11/2026 — Paid data (Thông tư 197/2016, VBHN 16/VBHN-BTC; caselaw.vn, read 01/11/2026)
- Fees are per "lần khai thác", in thousand VND. Salinity rows: 4.5 "Đo mặn" items (incl. "Độ mặn chi tiết",
  "Đường quá trình mặn") 150 per season each; 4.4 coastal "Độ mặn" 110 per year; 7.1 "Độ mặn nước biển" 220 per year.
  Tidal-river water level rows 300 per year. Not stated whether the fee multiplies per station (likely per element).
- No exemption for research/students. Later amendments (TT 43/2024, 64/2025) not verified. Get an official quote.

## 01/11/2026 — Comparison column mined; 2019-20 bulletin added
- parse_nchmf.py keeps Bảng 1 "So sánh" (cmp_* columns, ref_smax_gL, cmp_ref_flag) -> data/processed/
  nchmf_ref_monthly.csv: 490 station-months (455 backed by a bulletin whose reference is exactly 12 months back).
  New months not covered by our bulletins: Jan-Feb 2020 (record season, 27-29 stations), Mar-May 2021, Apr 2023,
  Feb 2024; 2016-01 (13) and 2016-05 (22) from one 2020 bulletin each. Monthly maxima, not dekads.
- Stale reference labels (copied from earlier issues) in 20220210, 20240510/20, 20250410/20, 2026 Mar-May;
  20250120/31 unlabelled. Back-test: 2026 "T3/2024" values match our Mar-2025 observations in 20-26 of 27 stations.
  Only rows with flag ok are trusted. With ok rows only, 2 conflicts: Gò Quao 2024-03 (12.7 vs 2.7, likely a
  print error) and Trần Đề 2020-01 (5-day bulletin vs dekadal base).
- dbqg_xmtb_20200520 (Wayback) parsed: 30 stations, adds season 2019-20 (1 bulletin). Sông Đốc prints 42 g/L in
  both tables (kept; plausibility cut raised 40 -> 45; check before modelling). 50 PDFs -> 1,389 obs / 1,385 fc rows.
- 2019-20 names: 27 distinct files, 2 archived (data/raw/alt_samples/nchmf_2019_20_names.csv); follow-up e-mail
  drafted for the owner.

## 01/11/2026 — G0 DECISION (owner): proceed with option 1
- Proceed with the data in hand: 49 NCHMF bulletins (2020-21 to 2025-26) + ODV Jan-Mar 2021 dekads, plus the free
  add-ons (comparison-column monthly maxima; PCTT 2020 daily at 4 stations). G0's 80% rule is computed on the
  bulletins present, not the 21 canonical dates; record this in protocol.md Deviations. Thin seasons (2020-21,
  2022-23) used for training only. JPG transcription dropped. Ask NCHMF for the 30 named 2019-20 bulletins;
  paid data (Thông tư 197) remains an option to discuss with the advisor.

## 01/11/2026 — Free alternative sources (docs/background/salinity_alt_sources.md)
- Bảng 1 "So sánh" column (e.g. 20/03/2024 Cát Lái "10.4 | Lớn hơn 4.4 | T3/2023" -> Mar 2023 max = 6.0; checked)
  gives the reference month's max per station: ~230-250 station-months from the PDFs we hold, incl. Jan-Feb 2020,
  Mar-Apr 2023, Feb 2024, Jan/May 2016. Monthly maxima, not dekads; reference labels sometimes stale -> hand check.
- PCTT daily reports (phongchongthientai.mard.gov.vn), ~10/02-25/05/2020: daily g/L at 8 stations (4 in our 28:
  Tân An, Bến Lức, Cầu Quan, Gò Quao) + same date 2016 -> ~40 station-dekads each for 2019-20 and 2015-16.
- NCHMF public bulletins start 25/12/2019 (5-day until 25/04/2020, then dekadal dbqg_xmtb_NN); 30 file names known
  from archived nchmf.gov.vn/Kttvsite posts, only 2 PDFs archived (05/02/2020, 20/05/2020; in data/raw/alt_samples/).
  Ask NCHMF for the other 28 by name.
- SIWRR seasonal reports: season-to-date max at ~15-20 stations, 2015-16 (~8), 2016-17 (3), 2017-18 (1); censored.
- Dead ends: old NCHMF site 2016-19 ("Không có dữ liệu"), Common Crawl, archive.today, data repositories.
- Still unfillable for free: dekads of 2016-17 to 2018-19, most Dec-Feb. Remaining routes: NCHMF reply, paid data.

## 01/11/2026 — NCHMF permission request sent
- Owner sent the e-mail to NCHMF on 01/11/2026: use of Bảng 1/2 for research, republication of transcribed tables
  with attribution, access to 2016-2023 bulletins. Until a written reply: publish code and scores only.
  Follow up if no reply by ~15/11/2026.

## 01/11/2026 — Upstream discharge: GloFAS instead of MRC
- MRC Data Portal: account created (research type), but the time-series request page returned 0 series for any
  parameter/country combination. Decision (owner, 01/11/2026): use GloFAS; MRC only as an optional check later.
- GloFAS v4 daily discharge via Open-Meteo Flood API (no account). Script `scripts/fetch_glofas_kratie.py`.
  The gauge coordinate (12.481, 106.018) is a tributary cell (0.06 m3/s); main-stem cell chosen by max mean flow:
  12.425 N, 105.975 E (~6 km downstream of the gauge, no tributary between). 2023 mean 11,208 m3/s.
- File `data/raw/glofas/kratie_glofas_daily.csv`: 1997-01-01 to 2026-11-01, 10,897 days (API starts 1997 here,
  not 1984). Dry-season minima 465-1,041 m3/s look low against typical observed Kratie low flows; treat as a
  biased index, not absolute Q. Recent days in the "seamless" series are forecast-based.
- Licence: GloFAS (Copernicus EMS) + Open-Meteo, CC BY 4.0; cite both.
- Real-time caveat for the protocol: at bulletin issue time only GloFAS forecasts/near-real-time values exist;
  hindcasts must lag the reanalysis by the product latency (decide the lag in protocol.md).
