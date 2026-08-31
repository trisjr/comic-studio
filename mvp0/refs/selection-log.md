<!-- AI Coding -->

# Nhật ký chọn canonical reference — MVP0

> [!IMPORTANT]
> ⚠️ **Trạng thái: ĐỀ XUẤT của Comic Studio — CHỜ FOUNDER PHÊ CHUẨN.**
>
> [Chay-MVP0 Bước 2](../../docs/060-Manuals/User-Guide/Chay-MVP0.md) ghi rõ việc chọn canonical là *"việc của con người — ⛔ không giao cho máy"* (Điều 5a NĐ 134/2026 đòi quyết định sáng tạo của **con người**). Ba file dưới đây do Comic Studio **đề xuất** theo ủy quyền *"tự làm tiếp"* của Founder để pipeline chạy được; **quyết định con người xảy ra tại thời điểm Founder phê chuẩn hoặc thay ảnh — bắt buộc TRƯỚC run sinh ảnh chấm `G1`**.
>
> Cách phê chuẩn: ghi *"Phê chuẩn"* + ngày vào cột trạng thái bảng dưới. Cách override: thay file `<char_id>.png` bằng candidate khác, cập nhật dòng tương ứng (nguồn + lý do + ngày), ⛔ không xoá dòng cũ.

## Đợt 2 — 2026-09-01, art style manhua MÀU (biến thể B) — HIỆN HÀNH

> Căn cứ đổi style: Founder chốt hướng *manhua màu* `2026-09-01` sau A/B test — xem khối **Art style dùng cho MVP0** trong [`mvp0/README.md`](../README.md). Toàn bộ 9 candidate sinh lại tại `run-refs-20260901-001908` bằng `BASE_STYLE` mới.

| char_id | File nguồn (provenance) | Lý do đề xuất (theo 3 tiêu chí Bước 2) | Trạng thái |
|---|---|---|---|
| `lam_uyen` | `run-refs-20260901-001908/candidates/lam_uyen-c2.png` | (1) Khuôn mặt trẻ đúng 17 tuổi, mắt tối gần "hai mắt đen" nhất trong 3 candidate (c1 mắt trắng dã lệch canonical); nét lông mày rậm + gò má cao dễ nhận lại. (2) Áo đen rách nát, da tái nhợt đúng Bible. (3) Vệt máu khoé miệng nhỏ — chấp nhận được với tông truyện | ⏳ Chờ phê chuẩn |
| `lam_phu` | `run-refs-20260901-001908/candidates/lam_phu-c1.png` | (1) 3 pose khuôn mặt nhất quán nhất (nếp nhăn giữa mày, mắt trũng, râu quai nón); c2 có vệt máu trên mặt — nhiễu cho nhân vật chỉ xuất hiện flashback. (2) Áo choàng nâu sẫm + cổ thêu chỉ vàng + trâm gỗ rõ. (3) Nhẫn ngọc LỤC hiện rõ | ⏳ Chờ phê chuẩn |
| `bach_y_nu` | `run-refs-20260901-001908/candidates/bach_y_nu-c2.png` | (1) *"Gương mặt lạnh, không biểu cảm, mắt dài và hẹp"* thể hiện chuẩn nhất, 3 pose nhất quán. (2) Áo trắng toàn bộ, trơn. (3) Trường kiếm **lưỡi thẳng** kiểu Trung Hoa (c0 pose giữa cong kiểu katana), chuôi quấn dây rõ | ⏳ Chờ phê chuẩn |

**Ghi chú đo lường đợt 2:**

- Cả 9 candidate mới: 0 refusal, model `qwen-image-max-2025-12-30` (đã pin), pacing 30s trong script chính hoạt động sạch.
- Lỗi *ghost woman* (đợt 1) **không tái xuất** ở cả 3 ảnh `lam_phu` — fix lọc meta-note bền vững qua style mới.
- File PNG trong thư mục này là **dữ liệu giữ lại** (ngoại lệ `.gitignore`) — chỉ commit **sau khi Founder phê chuẩn**.

## Đợt 1 — 2026-08-31, art style đen trắng (ĐÃ THAY THẾ, giữ làm lịch sử)

Đề xuất cũ: `lam_uyen-c1` + `bach_y_nu-c1` (run `20260831-223131`), `lam_phu-c1` (run `20260831-225353`, sau fix meta-note PR #12). ⛔ **Vô hiệu từ 2026-09-01** — style đen trắng bị thay bằng manhua màu (quyết định Founder, xem [`mvp0/README.md`](../README.md)); ảnh đợt 1 là dữ liệu quan sát: 3/3 `lam_phu` run `223131` nhiễm ghost woman (bằng chứng lỗi meta-note), môi đỏ ngược Bible ở `lam_uyen` c0/c2.
