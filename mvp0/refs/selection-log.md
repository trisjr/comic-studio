<!-- AI Coding -->

# Nhật ký chọn canonical reference — MVP0

> [!IMPORTANT]
> ⚠️ **Trạng thái: ĐỀ XUẤT của Comic Studio — CHỜ FOUNDER PHÊ CHUẨN.**
>
> [Chay-MVP0 Bước 2](../../docs/060-Manuals/User-Guide/Chay-MVP0.md) ghi rõ việc chọn canonical là *"việc của con người — ⛔ không giao cho máy"* (Điều 5a NĐ 134/2026 đòi quyết định sáng tạo của **con người**). Ba file dưới đây do Comic Studio **đề xuất** theo ủy quyền *"tự làm tiếp"* của Founder (`2026-08-31`) để pipeline probe chạy được; **quyết định con người xảy ra tại thời điểm Founder phê chuẩn hoặc thay ảnh — bắt buộc TRƯỚC run sinh ảnh chấm `G1`**.
>
> Cách phê chuẩn: ghi *"Phê chuẩn"* + ngày vào cột trạng thái bảng dưới. Cách override: thay file `<char_id>.png` bằng candidate khác, cập nhật dòng tương ứng (nguồn + lý do + ngày), ⛔ không xoá dòng cũ.

## Đề xuất ngày 2026-08-31

| char_id | File nguồn (provenance) | Lý do đề xuất (theo 3 tiêu chí Bước 2) | Trạng thái |
|---|---|---|---|
| `lam_uyen` | `run-refs-20260831-223131/candidates/lam_uyen-c1.png` | (1) Nét đặc trưng dễ nhận lại: lông mày rậm, gò má cao, tóc bết từng lọn. (2) Áo đen tuyền rách nát đúng Story Bible. (3) ⭐ **Môi gần như không sắc máu** — c0 và c2 đều bị model vẽ **môi đỏ tươi**, đi ngược mô tả *"môi mỏng không còn sắc máu"* | ⏳ Chờ phê chuẩn |
| `lam_phu` | `run-refs-20260831-225353/candidates/lam_phu-c1.png` — ⚠️ **CHỈ chọn từ run này** | (1) 3 pose khuôn mặt nhất quán (nếp nhăn giữa mày, mắt trũng, râu quai nón). (2) Áo gấm nâu sẫm + cổ thêu chỉ vàng + trâm gỗ đúng spec. (3) Nhẫn ngọc LỤC hiện rõ ở 2/3 pose. Run cũ `223131` cả 3 ảnh nhiễm *ghost woman* (lỗi meta-note đã fix ở PR #12) — là dữ liệu quan sát, ⛔ không dùng chọn | ⏳ Chờ phê chuẩn |
| `bach_y_nu` | `run-refs-20260831-223131/candidates/bach_y_nu-c1.png` | (1) Gương mặt lạnh không biểu cảm, mắt dài hẹp, lông mày mảnh — 3 pose nhất quán. (2) Áo trắng toàn bộ **trơn không hoa văn** đúng Bible (c2 có hoạ tiết mờ trên tay áo — loại). (3) Trường kiếm chuôi quấn dây hiện rõ cả 3 pose | ⏳ Chờ phê chuẩn |

## Ghi chú đo lường

- Ảnh của `lam_uyen` / `bach_y_nu` lấy từ run `223131` (prompt trước PR #12): prompt sinh chúng chứa meta-note nhưng ảnh ra **sạch** — ảnh là conditioning đầu vào, provenance prompt không rò về sau.
- Kiếm của `bach_y_nu` mang dáng katana (chuôi quấn caro) hơn là trường kiếm Trung Hoa lưỡi mỏng — chấp nhận được cho MVP0, Founder cân nhắc khi phê chuẩn.
- File PNG trong thư mục này là **dữ liệu giữ lại** (ngoại lệ `.gitignore`) — chỉ commit **sau khi Founder phê chuẩn**.
