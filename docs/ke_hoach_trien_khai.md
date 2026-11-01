# Kế hoạch triển khai Paper 4: dự báo xâm nhập mặn có khoảng tin cậy kiểm chứng và giá trị cho quyết định gieo sạ

Lập ngày 01/11/2026. Cơ sở: `docs/background/salinity_novelty.md` (kiểm tra tính mới) và `docs/background/salinity_data.md`
(khả năng dữ liệu), cả hai tìm ngày 01/11/2026. Mọi nhận định "chưa ai làm" chỉ đúng trong phạm vi các truy vấn đã ghi ở đó.

## 0. Một câu tóm tắt

Dự báo xác suất độ mặn lớn nhất 10 ngày tới vượt ngưỡng tại khoảng 28 trạm ĐBSCL, kèm khoảng dự báo conformal. Kiểm tra
bằng cách giữ lại hẳn mùa, trạm, tỉnh và mùa cực đoan. So với dự báo chính thức của Trung tâm Dự báo KTTV quốc gia
(NCHMF). Sau đó đo xem xác suất đã hiệu chỉnh có giá trị gì cho quyết định chọn ngày gieo vụ Đông Xuân, tách vùng trong
và ngoài hệ thống cống.

Tên tạm: "Calibrated salinity-intrusion forecasts for unmonitored stations and their value for rice sowing decisions:
Vietnamese Mekong Delta" (có "Vietnam", được thêm 5% theo HD 491).

## 1. Đóng góp (cái phản biện sẽ chấm)

1. **Benchmark công khai đầu tiên** (trong phạm vi đã tìm) về dự báo mặn nhiều trạm ở ĐBSCL, dùng dự báo chính thức
   làm mốc so sánh. Bảng 2 của bản tin NCHMF có sẵn dự báo độ mặn lớn nhất cho từng trạm, đã kiểm trên bản tin 20/3/2024.
2. **Khoảng dự báo conformal** được kiểm tra khi chuyển giao sang trạm, tỉnh và mùa cực đoan chưa thấy trong lúc
   huấn luyện. Các bài trước chỉ có 1 trạm và 1 mùa kiểm tra, khoảng phủ 97-100% so với mức danh định 90%.
3. **Giá trị kinh tế** của xác suất đã hiệu chỉnh so với dự báo tất định chính thức (đường cost-loss), và một
   ứng dụng: chọn ngày gieo Đông Xuân, tách trong và ngoài cống.
4. **Dữ liệu, mã nguồn và atlas tương tác** công khai. Bảng số liệu chỉ công bố nếu NCHMF đồng ý (xem mục 3).

## 2. Giả thuyết (đóng băng trong protocol trước khi chấm điểm, như Paper 3)

- **H1 (độ chính xác):** mô hình học máy gộp các trạm tốt hơn ba mốc: giữ nguyên, khí hậu theo trạm và tuần, và dự báo
  chính thức. Đo bằng MAE của Smax và điểm Brier của biến cố vượt ngưỡng, ở tầm 1 đợt (10 ngày), kiểm tra tiến theo mùa.
  Bài học Paper 3: "giữ nguyên" rất mạnh. Kết quả không ủng hộ vẫn được viết như thật.
- **H2 (độ phủ):** khoảng conformal 90% phủ 90 ± 3 điểm % khi kiểm tra tiến theo mùa. Khi giữ lại trạm hoặc tỉnh thì độ
  phủ giảm. Conformal Mondrian theo nhóm khoảng cách tới cửa sông đưa độ phủ về ít nhất 87%.
- **H3 (giá trị):** xác suất đã hiệu chỉnh có giá trị kinh tế tương đối (Richardson 2000) cao hơn dự báo tất định
  chính thức trên một dải tỉ lệ C/L, ở ngưỡng 4 g/L.
- **H4 (quyết định gieo sạ):** gieo theo dự báo mùa làm giảm mức hối tiếc kỳ vọng so với lịch thời vụ cố định. Mức giảm
  ngoài vùng cống lớn hơn trong vùng cống.

## 3. Dữ liệu

### 3.1 Biến mục tiêu (lõi B)

Smax = độ mặn lớn nhất (g/L) trong 10 ngày tại trạm s, đợt d. Mùa khô gán theo năm của tháng 1 (mùa 2024 là tháng
12/2023 đến tháng 6/2024).

| Nguồn | Mùa | Trạm | Việc phải làm |
|---|---|---|---|
| Bản tin NCHMF (PDF có lớp chữ), `kttv.gov.vn/upload/thuyvan2/YYYY/M/D/dbqg_xman_YYYYMMDD_1500.pdf` | 2024, 2025, 2026 (đã thấy); trước 2024 chưa thấy ở đường dẫn này | 28 | Viết script quét theo ngày (thử cả thuyvan1/thuyvan2), đọc Bảng 1 (quan trắc) và Bảng 2 (dự báo chính thức) bằng PyMuPDF |
| Open Development Vietnam, CSV CC BY-SA | 01/2021 đến 04/2022 | 28 | Tải về. Mùa này không có dự báo chính thức trong CSV, phải kiểm lại |
| Đài KTTV Nam Bộ, bản đồ JPG "độ mặn lớn nhất" | 03/2020 đến 05/2024 | khoảng 40 | Chép tay mùa 2020 (cực đoan) và 2023, hai người nhập độc lập rồi so (như rater 2 ở Paper 3). Trang có chứng chỉ TLS hết hạn: tải bằng trình duyệt, không vượt chặn bằng curl |

Kỳ vọng: 5-7 mùa × 28 trạm × khoảng 15 đợt ≈ 2.000-3.000 cặp trạm-đợt. Cỡ mẫu hiệu dụng là số mùa (5-7), nên mọi khoảng
tin cậy phải bootstrap theo khối mùa.

### 3.2 Biến đầu vào (chỉ dùng thông tin có được tại thời điểm phát bản tin)

- Smax đợt trước tại trạm (có sẵn trong cùng bản tin), khoảng cách tới cửa sông, nhánh sông, tỉnh.
- Lưu lượng thượng nguồn: Kratie trên MRC (chủ dự án đăng nhập; chỉ dùng, không phát hành lại), GloFAS dự phòng.
  Chỉ dùng giá trị trễ, đã biết lúc phát bản tin.
- Triều thiên văn cho 10 ngày tới (FES2022 hoặc TPXO qua pyTMD). Dùng được vì triều tính trước được, không rò rỉ.
- Mực nước tuần Tân Châu, Châu Đốc, Vũng Tàu (trong bản tin); ONI (ENSO); mưa CHIRPS/ERA5-Land trên GEE.

### 3.3 Lớp quyết định (lớp A)

- **Chuỗi dài cho dự báo mùa:** Cầu Quan (độ mặn lớn nhất tháng 1990-2016, Mendeley, CC BY 4.0), Sơn Đốc (1996-2016,
  GFZ, CC BY 4.0), Trà Vinh (độ mặn lớn nhất năm 1990-2016). Ba trạm này đều có trong 28 trạm của bản tin, nên nối được
  2021-2026. Thiếu 2017-2019; 2020 chỉ có từ 31/03 (cần kiểm).
- **Lịch thời vụ:** RiceAtlas cùng các thông báo lịch thời vụ của tỉnh.
- **Ngưỡng chịu mặn của lúa:** FAO (Ayers & Westcot): ngưỡng 3,0 dS/m, giảm 12% năng suất cho mỗi dS/m. Quy đổi gần đúng
  1 g/L ≈ 1,56 dS/m. Ngưỡng 1,9 dS/m của Grattan 2002 cần kiểm lại trước khi dùng.
- **Năng suất và giá:** năng suất tỉnh của GSO (dùng tên tỉnh trước sáp nhập 2025), giá xuất khẩu của World Bank, lợi
  nhuận và ngưỡng bỏ lúa từ Mills et al. 2025.
- **Vùng cống:** số hóa gần đúng ranh các hệ thống Nam Măng Thít, Ba Lai, Quản Lộ-Phụng Hiệp, Gò Công từ bản đồ đã công
  bố. Ghi rõ là gần đúng; OpenStreetMap chỉ có 39 đối tượng cống.
- **Đối chiếu thiệt hại:** diện tích lúa thiệt hại theo tỉnh mùa 2016 và 2020 (báo cáo của Bộ NN&PTNT và Cục Quản lý đê
  điều và PCTT; nguồn cụ thể cần tìm). Chỉ so thứ hạng, vì cỡ mẫu nhỏ.

### 3.4 Quyền dữ liệu

- Bản tin ghi "© Trung tâm Dự báo KTTV quốc gia" nhưng không có điều khoản tái sử dụng. **Nhờ thầy gửi email xin phép
  công bố lại bảng đã chép** trước khi phát hành. Chưa có phép thì chỉ công bố mã nguồn, điểm số và hình.
- Số liệu thô của MRC không phát hành lại. CSV của Open Development Vietnam theo CC BY-SA: phần dẫn xuất phải ghi nguồn
  và dùng cùng giấy phép.

## 4. Thiết kế lõi B

**Thời điểm dự báo:** ngày phát bản tin (ngày 10, 20 và cuối tháng). Tầm h = 1 đợt (bằng tầm của dự báo chính thức);
h = 2-3 đợt là phân tích phụ.

**Mốc so sánh:**
1. giữ nguyên (Smax đợt trước);
2. khí hậu theo trạm và đợt trong năm;
3. dự báo chính thức của NCHMF (Bảng 2).

**Mô hình:** chỉ hai loại để bài gọn:
1. hồi quy phân vị tuyến tính trên log(Smax);
2. gradient boosting phân vị (LightGBM).

Dùng một mô hình gộp mọi trạm, có đặc trưng của trạm, để dự báo được cho trạm chưa thấy. Không dùng GNN hay LSTM: dữ
liệu quá ít, và phản biện sẽ hỏi vì sao cần.

**Xác suất vượt ngưỡng:** từ phân phối dự báo đã conformal hóa (conformalized quantile regression trên một lưới phân
vị), lấy P(Smax > c) với c = 1, 2 và 4 g/L. Ba ngưỡng này lần lượt dùng cho nước sinh hoạt, mạ và lúa (ranh 4‰ của bản
tin).

**Các kiểu kiểm tra:**
1. tiến theo mùa (huấn luyện các mùa trước, kiểm tra mùa sau): kiểu chính;
2. giữ lại từng trạm;
3. giữ lại từng tỉnh;
4. giữ lại mùa cực đoan (2020, nếu chép được).

Conformal: split, và Mondrian theo nhóm khoảng cách tới cửa sông (0-15, 15-40, trên 40 km).

**Chỉ số:**
- MAE và hệ số kỹ năng so với giữ nguyên;
- Brier, biểu đồ tin cậy, CRPS;
- độ phủ và độ rộng khoảng 90%;
- hit rate, false-alarm rate, Peirce skill score cho dự báo chính thức và cho dự báo của mình;
- giá trị kinh tế tương đối theo C/L.

**So sánh công bằng với dự báo chính thức:** dự báo chính thức là một con số. So MAE trên cùng các cặp trạm-đợt. So
phân loại vượt ngưỡng bằng cách quy xác suất của mình về nhị phân ở ngưỡng tối ưu trên tập hiệu chỉnh. Lợi thế "có xác
suất" chỉ được tính trong H3, không tính lẫn vào H1.

## 5. Thiết kế lớp A (giữ nhẹ)

**Chỗ phải nói thẳng:** quyết định gieo Đông Xuân được đưa ra vào tháng 11-12, còn đỉnh mặn rơi vào tháng 2-4. Dự báo 10
ngày của lõi B **không đủ tầm** cho quyết định này. Vì vậy lớp A dùng một dự báo mùa riêng tại 3 trạm có chuỗi dài:
- phát ngày 1/11;
- dự báo P(độ mặn lớn nhất tháng 2 và tháng 3 > 4 g/L);
- biến đầu vào: ONI, lưu lượng Kratie tháng 9-10, độ mặn mùa trước;
- mô hình: hồi quy logistic, giống Apel et al. 2020, nhưng thêm kiểm tra độ tin cậy và conformal;
- cỡ mẫu khoảng 30 mùa.

**Quyết định:**
- Lựa chọn: gieo sớm (đầu tháng 11), gieo chuẩn (giữa tháng 12) hoặc gieo muộn.
- Giai đoạn nhạy cảm (làm đòng đến trổ) rơi vào khoảng 50-80 ngày sau gieo.
- Thiệt hại: năng suất giảm theo độ mặn tại giai đoạn nhạy cảm, theo đường FAO.
- Chi phí gieo sớm (năng suất tiềm năng thấp hơn, nước lũ chưa rút) là tham số, được quét qua một dải giá trị.
- Ruộng trong cống: phơi nhiễm nhân với hệ số bảo vệ, quét từ 0 đến 0,5, vì không có nhật ký vận hành cống.

**So sánh các chiến lược:**
1. lịch cố định;
2. khí hậu;
3. dự báo mùa đã hiệu chỉnh;
4. thông tin hoàn hảo.

**Chỉ số:** mức hối tiếc (thiệt hại trừ thiệt hại khi biết trước), đường giá trị theo C/L, tách trong và ngoài cống.
Đối chiếu thứ hạng thiệt hại theo tỉnh năm 2016 và 2020.

**Giới hạn ghi trong bài:** hàm thiệt hại một phần là giả định. Kết quả là phân tích độ nhạy, không phải khuyến nghị
cho nông dân.

## 6. Phần trực quan (tăng sức thuyết phục và tác động)

Phản biện chấm chủ yếu ở phương pháp. Atlas giúp phần tác động, khả năng tái lập và tóm tắt bằng hình, nên làm gọn,
không ôm đồm.

**Hình trong bài:** 300 dpi, bảng màu an toàn cho người mù màu, có cả SVG.
1. Bản đồ vùng nghiên cứu: 28 trạm tô theo khoảng cách tới cửa sông, ranh vùng cống.
2. Chuỗi thời gian kèm quạt khoảng dự báo tại 3-4 trạm đại diện mùa 2024 (hoặc 2020), chồng dự báo chính thức và quan
   trắc.
3. Kỹ năng so với các mốc theo từng kiểu kiểm tra: dạng dot plot có khoảng bootstrap.
4. Độ phủ theo kiểu kiểm tra và theo nhóm khoảng cách (cùng kiểu với Paper 3, để phản biện thấy nhất quán).
5. Biểu đồ tin cậy cho 3 ngưỡng.
6. Đường giá trị kinh tế tương đối theo C/L: mình, chính thức, khí hậu.
7. Bản đồ mức hối tiếc theo tỉnh, trong và ngoài cống (lớp A).

**Atlas tương tác** (trang tĩnh trên GitHub Pages khi công bố, như atlas Paper 3; Leaflet + JSON, không cần server):
- bản đồ trạm tô theo P(Smax > 4 g/L) đợt tới;
- bấm vào trạm để xem quạt khoảng dự báo, quan trắc và dự báo chính thức;
- thanh trượt "phát lại" cả mùa 2024 theo từng đợt;
- nút chuyển kiểu kiểm tra để thấy độ phủ từng trạm;
- bảng quyết định: kéo tỉ lệ C/L, xem chiến lược gieo khuyến nghị và mức hối tiếc theo tỉnh.

**Tóm tắt bằng hình** 13 × 5 cm (nếu tạp chí yêu cầu).

**Tùy chọn mạnh: dự báo trực tiếp mùa khô 2026-2027.**
- Mỗi lần NCHMF phát bản tin (từ tháng 12/2026), mình công bố dự báo trên atlas, gắn mốc thời gian bằng git tag, trước
  khi có quan trắc.
- Chấm điểm khi mùa kết thúc. Đây là kiểm tra ngoài mẫu thật, phản biện rất khó bác.
- Đổi lại: nếu muốn trọn mùa thì phải nộp bài sau tháng 6/2027. Quyết định ở cổng G2.

## 7. Lịch và cổng quyết định

Ước tính làm bán thời gian (khoảng 15-20 giờ/tuần).

| Tuần | Việc | Cổng |
|---|---|---|
| 1 | Script quét và đọc bản tin NCHMF; tải CSV Open Development Vietnam; kiểm kê bài đăng của Đài Nam Bộ; email xin phép NCHMF (thầy); hỏi thầy có quen SIWRR, ĐH Cần Thơ không | **G0:** ít nhất 5 mùa, mỗi mùa ít nhất 20 trạm có ít nhất 80% số đợt, và Bảng 2 đọc được ít nhất 3 mùa. Không đạt thì chuyển phương án dự phòng (mục 8) |
| 2-4 | Chép tay mùa 2020 và 2023 (Hiếu và Nam, nhập độc lập); biến đầu vào; chuỗi dài cho lớp A; số hóa vùng cống; kiểm tra chất lượng | G1: sai khác giữa hai người nhập dưới 2% số ô |
| 5 | Viết và đóng băng `docs/protocol.md` (giả thuyết, cách chia tập, chỉ số, ngưỡng), git tag `protocol-v1` | Chủ dự án duyệt |
| 6-8 | Thí nghiệm lõi B (H1-H3) | G2: chốt có làm dự báo trực tiếp 2026-2027 không |
| 9-10 | Lớp A (H4) | |
| 10-12 | Hình, atlas, tóm tắt bằng hình | |
| 12-16 | Viết bài, phản biện nội bộ, kiểm số tự động, nộp | |

Tổng cộng khoảng 4 tháng. Chi phí khoảng 0 đồng, trừ khi chọn mua số liệu theo ngày (Thông tư 197/2016).

## 8. Rủi ro và phương án dự phòng

| Rủi ro | Dấu hiệu | Phương án |
|---|---|---|
| Không có bản tin trước 2024 | G0 chỉ đạt 3-4 mùa | Chép thêm JPG của Đài Nam Bộ cho 2021-2023; hoặc mua số liệu ngày (Thông tư 197) cho 10 trạm |
| Không được phép công bố lại bảng | NCHMF từ chối hoặc im lặng | Chỉ công bố mã nguồn và điểm số; người đọc tự chạy script trên bản tin công khai |
| Học máy không thắng giữ nguyên hoặc dự báo chính thức | H1 không được ủng hộ | Bài vẫn đứng nhờ H2 và H3 (độ phủ, giá trị xác suất), giống Paper 3 |
| Độ phủ sụp khi giữ lại trạm hoặc tỉnh | H2 thất bại | Báo cáo trung thực; Mondrian hoặc weighted conformal; đây cũng là phát hiện đáng viết |
| Nhóm ĐH Cần Thơ, IGES, UNU ra bài trước | Bài mới về chuyển giao hoặc khoảng dự báo | Điểm khác của mình: nhiều trạm, so với dự báo chính thức, lớp quyết định, atlas. Kiểm tra lại tài liệu trước khi nộp |
| Dữ liệu thiệt hại tỉnh không tìm được | Không có số 2016 hoặc 2020 | Lớp A chỉ còn phân tích độ nhạy, bỏ phần đối chiếu |

## 9. Tạp chí và thưởng UEH

- **Ứng viên (Elsevier):** Journal of Hydrology, Agricultural Water Management, Environmental Modelling & Software,
  Climate Services. Hạng JCR phải kiểm trên JCR mới nhất trước khi chọn; tôi chưa kiểm được.
- **HESS** (Copernicus) được UEH tính 80%. **Water** (MDPI) tính 80% và có lẽ không phải Q1.
- **Theo HD 491:** WoS SCIE Q1 được thưởng 100 triệu, hoặc tài trợ 200 triệu nếu đăng ký trước khi xuất bản; có
  "Vietnam" được thêm 5%; số tiền nhân theo tỉ lệ tác giả UEH. Câu tài trợ và nơi công tác ghi giống Paper 3.
- **Không preprint** (theo thầy).

## 10. Việc cần chủ dự án quyết hoặc làm

1. Xác nhận tên folder và tên tạm của bài.
2. Nhờ thầy gửi email xin phép NCHMF; hỏi thầy về liên hệ SIWRR hoặc ĐH Cần Thơ.
3. Đăng nhập MRC để tải lưu lượng Kratie.
4. Phân công chép tay JPG (Hiếu, Nam).
5. Ở G2: có làm dự báo trực tiếp mùa 2026-2027 hay không.
