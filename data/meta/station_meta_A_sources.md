# station_meta_A sources (pass A, 2026-11-01)

Status: web searches returned little station-level material. Coordinates and sluice status are NOT verified.

## 1. Province merger (verified from secondary text of the law)
- Nghị quyết 202/2025/QH15 của Quốc hội về sắp xếp đơn vị hành chính cấp tỉnh, adopted 12/06/2025 (in force on adoption, Điều 2 khoản 1); new local governments operate from 01/07/2025 (Điều 2 khoản 2).
- Text read at https://luatvietnam.vn/hanh-chinh/nghi-quyet-202-2025-qh15-cua-quoc-hoi-ve-viec-sap-xep-don-vi-hanh-chinh-cap-tinh-402728-d1.html (secondary site; the official copy is on vanban.chinhphu.vn / quochoi.vn, not opened). Other mirrors found: https://nhandan.vn/quoc-hoi-thong-qua-nghi-quyet-ve-sap-xep-don-vi-hanh-chinh-cap-tinh-ca-nuoc-con-34-tinh-thanh-post886206.html
- Mapping used (Điều 1): Bến Tre + Trà Vinh + Vĩnh Long -> Vĩnh Long; Tiền Giang + Đồng Tháp -> Đồng Tháp; Long An + Tây Ninh -> Tây Ninh; Cần Thơ + Sóc Trăng + Hậu Giang -> Cần Thơ (city); Kiên Giang + An Giang -> An Giang; Bạc Liêu + Cà Mau -> Cà Mau; TP HCM + Bà Rịa-Vũng Tàu + Bình Dương -> TP HCM.
- Commune/ward level (the 3321 xã after 1/7/2025) not mapped; the district column is only a rough old-district guess for 17 rows, unverified.

## 2. Coordinates
- Not found in any open source I could reach (searches for NCHMF/SRHMC station lists, GFZ Son Doc and Mendeley Cau Quan/Tra Vinh records: these give place names only, e.g. GFZ "Son Doc, Ben Tre province").
- 23 of 37 rows carry coordinates rounded to 0.01 deg, written from general knowledge of the locality (town centre), confidence low. 14 rows are blank on purpose.
- Candidate real sources to fill them: MRC hydrological station list (archive.iwlearn.org/mrcmekong.org/spatial/meta_html/HydrologicalData.pdf, not opened); Apel et al. GFZ dataset metadata; SRHMC station catalogue; OSM/Google Maps check of each locality by the owner.

## 3. Sluice systems: boundary map sources for later digitising (none opened; leads only)
- Quy hoạch thuỷ lợi vùng ĐBSCL giai đoạn 2021-2030 (MARD / Viện Quy hoạch Thủy lợi miền Nam, SIWRP): the plan maps show the sluice-closed zones. Leads, not verified.
- SIWRP project documents for: Cái Lớn-Cái Bé (World Bank/ADB; Phase 1 2017+), Nam Măng Thít (WB), Quản Lộ-Phụng Hiệp, Gò Công, Ba Lai, Bắc Bến Tre, Bảo Định, Ô Môn-Xà No, Tiếp Nhật/Long Phú, U Minh Thượng/Hạ.
- MRC / Delta-wide: Tran et al. 2025 STOTEN (doi:10.1016/j.scitotenv.2025.178711) and Apel et al. 2020 NHESS may include zone maps; check figures.
- Wikimapia/OSM: sluice structures (waterway=sluice_gate / lock_gate) can be pulled from OSM via Overpass to place gates; polygons must then be drawn by hand.

## 4. Per-station sluice evidence
All rows in the CSV are reasoning from channel type (main channel / open estuary = outside; inland canal = unknown), not from a map. Only Gò Quao (inside Cái Lớn-Cái Bé) and Xẻo Rô (boundary) rest on recalled project geography and need checking.

## 5. Relocations of Cầu Quan, Sơn Đốc, Trà Vinh
No relocation found in my searches; absence of evidence only. Ask SRHMC / check Apel et al. data descriptor.
