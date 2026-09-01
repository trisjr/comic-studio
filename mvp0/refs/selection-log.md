<!-- AI Coding -->

# Nhật ký chọn canonical reference — MVP0

> [!IMPORTANT]
> ✅ **Trạng thái: FOUNDER ĐÃ PHÊ CHUẨN đợt 3 ngày `2026-09-01`** — qua phiên làm việc (nguyên văn: *"Duyệt, em tự điền sau đó merge giúp anh"*), Comic Studio ghi thay theo ủy quyền. Phán quyết kèm theo: **chấp nhận nhẫn đỏ** của `lam_phu` như đề xuất.
>
> [Chay-MVP0 Bước 2](../../docs/060-Manuals/User-Guide/Chay-MVP0.md) ghi rõ việc chọn canonical là *"việc của con người — ⛔ không giao cho máy"* (Điều 5a NĐ 134/2026 đòi quyết định sáng tạo của **con người**). Ba file dưới đây do Comic Studio **đề xuất** theo ủy quyền *"tự làm tiếp"* của Founder để pipeline chạy được; **quyết định con người xảy ra tại thời điểm Founder phê chuẩn hoặc thay ảnh — bắt buộc TRƯỚC run sinh ảnh chấm `G1`**.
>
> Cách phê chuẩn: ghi *"Phê chuẩn"* + ngày vào cột trạng thái bảng dưới. Cách override: thay file `<char_id>.png` bằng candidate khác, cập nhật dòng tương ứng (nguồn + lý do + ngày), ⛔ không xoá dòng cũ.

## Đợt 3 — 2026-09-01, art style CHỐT: manga Nhật B/W + "đỏ tà dị" — HIỆN HÀNH

> Style chốt sau **ba vòng A/B** — xem khối **Art style dùng cho MVP0** trong [`mvp0/README.md`](../README.md). Toàn bộ 9 candidate sinh tại `run-refs-20260901-122647` bằng `BASE_STYLE` chốt (kèm bible/panel script đã khử màu-tả-thực).

| char_id | File nguồn (provenance) | Lý do đề xuất (theo 3 tiêu chí Bước 2) | Trạng thái |
|---|---|---|---|
| `lam_uyen` | `run-refs-20260901-122647/candidates/lam_uyen-c1.png` | (1) 3 pose khuôn mặt nhất quán, lông mày rậm + gò má cao dễ nhận lại; mắt đen đúng canonical. (2) Áo đen tuyền rách nát, tóc bết từng lọn, tay nổi gân — bám Bible sát nhất. (3) B/W gần tuyệt đối (một chấm đỏ rất nhỏ trên vai áo pose trái). c0/c2 bị môi đỏ / vệt máu miệng — lệch *"môi không còn sắc máu"* | ✅ Phê chuẩn 2026-09-01 |
| `lam_phu` | `run-refs-20260901-122647/candidates/lam_phu-c1.png` | (1) 3 pose nhất quán nhất (nếp nhăn giữa mày, mắt trũng, râu quai nón, trâm gỗ). (2) Áo gấm tông sẫm + thêu hoa văn nổi B/W đúng bible mới. (3) ⚠️ **Nhẫn ra màu ĐỎ ở cả 3 candidate** — model đặt spot-đỏ của style vào vật "nổi bật" duy nhất. Đề xuất **chấp nhận**: ảnh ref là conditioning nên nhẫn đỏ sẽ nhất quán mọi panel (tốt cho trục attribute binding `G1-d`), và "kỷ vật nhuốm đỏ" không phá tông truyện. Founder bác được khi phê chuẩn | ✅ Phê chuẩn 2026-09-01 |
| `bach_y_nu` | `run-refs-20260901-122647/candidates/bach_y_nu-c1.png` | (1) Mặt lạnh vô cảm, mắt dài hẹp — 3 pose nhất quán. (2) Áo trắng trơn, tay áo rộng ✓. (3) B/W **sạch tuyệt đối**; c2 có giọt máu đỏ trên lưỡi kiếm — đẹp về cốt truyện nhưng ⛔ nguy hiểm cho canonical (kiếm sẽ dính máu ở mọi panel, kể cả trước cảnh đâm) | ✅ Phê chuẩn 2026-09-01 |

**Ghi chú đo lường đợt 3:**

- 9/9 candidate, 0 refusal, model `qwen-image-max-2025-12-30`, pacing 30s sạch.
- Ghost woman tiếp tục vắng mặt ở cả 3 ảnh `lam_phu` (fix meta-note bền qua 3 style).
- Bằng chứng khử màu: "nhẫn ngọc"→"nhẫn mặt đá" đã hết màu **lục**; hệ quả mới là spot **đỏ** từ chính style — xem cột `lam_phu`.
- File PNG trong thư mục này là **dữ liệu giữ lại** (ngoại lệ `.gitignore`) — chỉ commit **sau khi Founder phê chuẩn**.

## Đợt 2 — 2026-09-01, manhua MÀU biến thể B (ĐÃ THAY THẾ, giữ làm lịch sử)

Đề xuất cũ: `lam_uyen-c2` + `lam_phu-c1` + `bach_y_nu-c2` từ run `20260901-001908` (style manhua màu trầm). ⛔ **Vô hiệu cùng ngày** — Founder xem ảnh, yêu cầu thêm biến thể manga Nhật theo ảnh tham khảo, và chốt lại style ở vòng A/B thứ ba. Ảnh đợt 2 là dữ liệu quan sát của vòng chọn style.

## Đợt 1 — 2026-08-31, art style đen trắng (ĐÃ THAY THẾ, giữ làm lịch sử)

Đề xuất cũ: `lam_uyen-c1` + `bach_y_nu-c1` (run `20260831-223131`), `lam_phu-c1` (run `20260831-225353`, sau fix meta-note PR #12). ⛔ **Vô hiệu từ 2026-09-01** — style đen trắng bị thay bằng manhua màu (quyết định Founder, xem [`mvp0/README.md`](../README.md)); ảnh đợt 1 là dữ liệu quan sát: 3/3 `lam_phu` run `223131` nhiễm ghost woman (bằng chứng lỗi meta-note), môi đỏ ngược Bible ở `lam_uyen` c0/c2.
