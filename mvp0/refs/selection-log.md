<!-- AI Coding -->

# Nhật ký chọn canonical reference — MVP0

> [!IMPORTANT]
> ✅ **Trạng thái: FOUNDER ĐÃ PHÊ CHUẨN đợt 4 ngày `2026-09-02`** — qua phiên làm việc, chốt phong cách **Pure 2D Anime / Manhwa Webtoon** (Clip Studio Paint 2D Drawing, nét mảnh, mảng màu phẳng cel-shading, triệt tiêu hoàn toàn 3D CGI).
>
> [Chay-MVP0 Bước 2](../../docs/060-Manuals/User-Guide/Chay-MVP0.md) ghi rõ việc chọn canonical là *"việc của con người — ⛔ không giao cho máy"*. Ba file canonical dưới đây được chọn từ run `20260902-155323` cho vòng đo `G1`.

## Đợt 4 — 2026-09-02, art style CHỐT: Pure 2D Anime / Manhwa Webtoon — HIỆN HÀNH

> Style chốt theo mẫu Webtoon 2D phẳng của Founder: nét mảnh sắc sảo, cel-shading 2D thuần túy, ngũ quan cách điệu anime, cấm triệt để 3D CGI. Toàn bộ 9 candidate sinh tại `run-refs-20260902-155323`.

| char_id | File nguồn (provenance) | Lý do đề xuất / phê chuẩn | Trạng thái |
|---|---|---|---|
| `lam_uyen` | `run-refs-20260902-155323/candidates/lam_uyen-c0.png` | 4 góc nhìn chuẩn 2D Anime (chính diện, toàn thân, nghiêng, 3/4). Mắt đen sắc bén, tóc đen tỉa mảng 2D, áo rách đen, chân trần đúng Story Bible. 100% 2D lineart phẳng | ✅ Phê chuẩn 2026-09-02 |
| `lam_phu` | `run-refs-20260902-155323/candidates/lam_phu-c0.png` | 3 góc nhìn 2D, trung niên uy nghiêm, tóc búi trâm gỗ, râu quai nón, nhẫn đá lớn ở tay phải, áo gấm sẫm đúng gia chủ | ✅ Phê chuẩn 2026-09-02 |
| `bach_y_nu` | `run-refs-20260902-155323/candidates/bach_y_nu-c0.png` | 3 góc nhìn 2D thanh thoát, váy trắng kiếm tu, nét vẽ thanh mảnh, mắt lạnh 2D sắc lẹm, kiếm có chuôi quấn dải lụa trắng | ✅ Phê chuẩn 2026-09-02 |

## Đợt 3 — 2026-09-01, art style manga Nhật B/W (ĐÃ THAY THẾ, giữ làm lịch sử)
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
