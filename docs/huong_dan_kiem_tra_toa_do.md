# Hướng dẫn tìm tọa độ trạm đo mặn (cho Hiếu và Nam)

**Mục tiêu:** tìm vị trí chính xác của 37 trạm đo mặn trên Google Maps. Tọa độ dùng để vẽ bản đồ trong bài báo và atlas.

**File cần điền:** `data/meta/station_coords_check.csv` (mở bằng Excel). Mỗi dòng là một trạm.

**Chia việc:** Hiếu làm dòng 1-19, Nam làm dòng 20-37. Xong thì mỗi người kiểm lại 3 trạm bất kỳ của người kia.

## Cách làm cho mỗi trạm (3-5 phút)

1. Mở Google Maps, gõ **"Trạm thủy văn" + tên trạm**, ví dụ: `Trạm thủy văn Bến Lức`.
2. Nếu không thấy: bật **ảnh vệ tinh**, tìm con sông ở cột `river`, gần thị trấn cùng tên. Trạm thường là nhà nhỏ sát
   bờ sông, có cột đo nước. Cột `km_from_mouth` là khoảng cách tới cửa sông (dùng "Đo khoảng cách" để ước).
3. **Chuột phải đúng điểm trạm**, bấm vào dãy số đầu tiên (ví dụ `10.6412, 106.4823`) để copy.
4. Điền vào file:
   - `lat`: số thứ nhất, `lon`: số thứ hai;
   - `how_found`: ghi `nhan Google Maps`, `anh ve tinh` hoặc `uoc theo km`;
   - `screenshot`: chụp màn hình, lưu vào thư mục `data/meta/screenshots/`, ghi tên file (ví dụ `ben_luc.png`);
   - `checked_by`: tên của bạn.

## Quy tắc

- **Không chắc thì để trống `lat` và `lon`**, ghi lý do vào `notes`. Tọa độ sai còn tệ hơn để trống.
- Không lấy tọa độ từ ChatGPT, AI hay trí nhớ. Chỉ lấy từ điểm mình nhìn thấy trên bản đồ.
- Không sửa các cột `station`, `river`, `km_from_mouth`, `province_old`.
- Lưu file dạng **CSV UTF-8** (Excel: File > Save As > "CSV UTF-8") để không mất dấu tiếng Việt.

Xong thì báo Nghĩa. Claude sẽ kiểm tra tọa độ có nằm trên đúng sông và khớp khoảng cách tới cửa sông không.
