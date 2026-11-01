# station_meta_B sources (pass B, 2026-11-01)

## 1. Province merger (legal source)
- Nghị quyết 202/2025/QH15 of the National Assembly on arrangement of provincial administrative units, adopted 12 Jun 2025, effective on adoption (Điều 2.1); new provincial governments operate from 1 Jul 2025 (Điều 2.2). Text read via https://luatvietnam.vn/hanh-chinh/nghi-quyet-202-2025-qh15-cua-quoc-hoi-ve-viec-sap-xep-don-vi-hanh-chinh-cap-tinh-402728-d1.html (secondary host, not the Công báo; verify against the official gazette before citing).
- Mapping used (Điều 1): Long An + Tây Ninh -> Tây Ninh (1.18); Cần Thơ + Sóc Trăng + Hậu Giang -> Cần Thơ (1.19); Bến Tre + Trà Vinh + Vĩnh Long -> Vĩnh Long (1.20); Tiền Giang + Đồng Tháp -> Đồng Tháp (1.21); Bạc Liêu + Cà Mau -> Cà Mau (1.22); Kiên Giang + An Giang -> An Giang (1.23); TP HCM + Bình Dương + Bà Rịa-Vũng Tàu -> TP HCM (1.16).
- Other pointer: https://pbgdpl.cantho.gov.vn/nghi-quyet-so-2022025qh15-cua-quoc-hoi-ve-viec-sap-xep-don-vi-hanh-chinh-cap-tinh (not opened).
- Data observation: in nchmf_obs.csv the bulletins switch to the new names at issue 2026-04-20, not 1 Jul 2025 (last old name 2026-04-10). Cà Mau/Sông Đốc is "Cà Mau" in both systems. Commune-level (3,321 xã) mapping not done.

## 2. Coordinates
- 19 stations: Zenodo record 20003854, file Mekong_Station_Metadata.csv (Nguyen D.Q.H., Nguyen T.A., Tran T.K., CC BY 4.0), https://zenodo.org/records/20003854. Same group as the RSASE 2026 LOSO paper. Not stated whether points are surveyed gauges; confidence "medium". It has 21 stations; An Lạc Tây and Khánh Thạnh Tân are not in our list.
- 13 stations: OSM Nominatim locality centroids (queried 1.5 s apart, UA mekong-salinity-research/0.1). These are NOT gauges; error of several km. Confidence "low". OSM labels already show post-merger provinces.
- 5 with no coordinates: Tuyên Nhơn, Cầu Nổi, Xuân Hòa, Giao Hòa, Láng Thé (no OSM hit for these names in the right place). Not invented.
- Better sources not reached: GFZ doi:10.5880/GFZ.4.4.2024.004 (Sơn Đốc, CC BY 4.0) and the Mendeley Cầu Quan/Trà Vinh set likely carry station coordinates; NCHMF/SRHMC station lists (kttv-nb.org.vn has an expired certificate, skipped).

## 3. Sluice evidence
- Cái Lớn-Cái Bé: Cái Bé sluice operating from 2/2021, phase 1 inaugurated 5/3/2022; Cái Lớn sluice 2.1 km from Cái Lớn bridge toward the Hậu; Xẻo Rô sluice on Xẻo Rô canal ~550 m from mouth, An Biên; all gates closed 26-29/12/2023 for a drill. From web-search snippets of https://www.sggp.org.vn/cong-thuy-loi-cai-lon-cai-be-bat-dau-van-hanh-cap-thoat-nuoc-post621328.html, https://nongnghiepmoitruong.vn/cong-cai-lon--cai-be-tag108388/, https://nongnghiepmoitruong.vn/cong-xeo-ro-tag145554/ (pages not opened).
- Ninh Quới sluice (Bạc Liêu, Quản Lộ-Phụng Hiệp): https://vietnamagriculture.nongnghiep.vn/ninh-quoi-sluice-gate-citadel-wall-safeguarding-freshwater-in-four-mekong-delta-provinces-d384033.html (snippet).
- All "outside" calls on main river channels, and all system assignments marked "reasoning", are my inference from river and position, not a source. No station-to-polygon test was possible without boundary geometry.

## 4. Boundary maps for later digitising (none downloaded)
- Quản Lộ-Phụng Hiệp (279,000 ha): ISPRS paper figure with sluices, districts, 4 g/L isohalines: https://www.isprs.org/proceedings/XXXIII/congress/part7/79_XXXIII-part7s.pdf; JICA report with sluice inventory and the salt/fresh demarcation line: https://openjicareport.jica.go.jp/pdf/12114633_02.pdf.
- Cái Lớn-Cái Bé: Vietnam Academy for Water Resources papers https://vawr.org.vn/Upload/BaibaoKH/gsts-tran-dinh-hoa-tcnnptnt2023-6-11.pdf and https://vawr.org.vn/Upload/BaibaoKH/tran-dinh-hoa-63-2020.pdf (not opened; may have layout maps).
- Gate-vs-no-gate effect context: Le, Alpizar, Mills 2025, doi:10.1111/agec.70045.
- For Ba Lai, Nam Măng Thít, Gò Công, Bảo Định, Bắc Bến Tre, Tiếp Nhật, Ô Môn-Xà No, U Minh: no map found; candidates are SIWRP (Phân viện Quy hoạch thủy lợi Nam Bộ) master-plan atlases, provincial Sở NN&PTNT irrigation plans, and the Tà Vinh plan PDF https://travinh.gov.vn/SiteFolders/ubnd1/QUY%20HO%E1%BA%A0CH%20T%E1%BB%88NH%20TV%202021%20-%202030/2.11.HT_CCN_19_09_23.pdf (irrelevant hit, not checked).

## 5. Long-record stations
- Cầu Quan: Hậu River, Tiểu Cần, Trà Vinh (literature via web search). Trà Vinh and Sơn Đốc: no information found. No relocation documented for any of the three in sources reached; absence is a search-scope statement only. NCHMF km differs by bulletin era for some stations (Đại Ngãi 30/35, An Định 45/48, Cát Lái 20/58, Gành Hào/Sông Đốc 0-2), which could indicate re-chainage or relocation; check bulletins.
