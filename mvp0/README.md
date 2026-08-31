# MVP0 — dữ liệu viết tay

> Thư mục này chứa **dữ liệu đầu vào viết tay** của MVP0, ⛔ không phải tài liệu dự án.
>
> **Vì sao nằm ngoài `docs/`**: [`RULE-001`](../knowledge-base/99-Templates/Documents-Template.md) quản lý **tài liệu**; đây là **nguyên liệu chạy**. Tách riêng còn làm rõ một ranh giới mà kỷ luật MVP0 bắt buộc phải rõ — xem ngay dưới.

## Kỷ luật MVP0 — cái gì vứt, cái gì giữ

> *"Code của MVP0 KHÔNG phải nền của sản phẩm — viết để trả lời câu hỏi rồi **bỏ**; giữ lại **kết luận và dữ liệu**."* — [MVP-Scope §3.1](../docs/010-Planning/MVP-Scope.md) · [Roadmap §3.1](../docs/010-Planning/Roadmap.md)

| Thành phần | Số phận |
|---|---|
| Script sinh ảnh, adapter, compiler | ⛔ **Vứt** sau khi có số |
| `story-bible.yaml` · `panel-script.yaml` | ✅ **Giữ** — là nguyên liệu tái dựng golden dataset |
| Golden dataset (ảnh + bảng chấm) | ✅ **Giữ vĩnh viễn** — `H6` là `✅` ở **mọi** mốc MVP0–MVP4, và là đầu vào eval kit `M1-6` |

⛔ **Không** tạo migration, config loader, hay abstraction provider trong thư mục này — đó là **dấu hiệu sớm** của rủi ro *"spike biến thành nền móng"* ([Roadmap §3.1](../docs/010-Planning/Roadmap.md)).

## Nội dung

| File | Nội dung | Neo |
|---|---|---|
| [`story-bible.yaml`](./story-bible.yaml) | **3 nhân vật** viết tay + canonical reference + trạng thái theo thời điểm | `Roadmap §3.1` việc 2 |
| [`panel-script.yaml`](./panel-script.yaml) | **22 panel / 6 trang**, tên trường khớp đúng cột `comic.panel` | `Roadmap §2` (~8–30 panel) · [DB-Entity-Comic-IR](../docs/030-Specs/Schema/DB-Entity-Comic-IR.md) |

**Nguồn**: *Tà Nguyệt Vô Tận* — Chương 1 *(Người chết trở về)*, **chương comic #1**.

⚠️ Chương chữ 1 được tách thành **hai chương comic**; file hiện tại phủ chương comic #1 (nghĩa địa → tỉnh dậy → bia đá → flashback → ký hiệu con mắt). Xem [`F-8`](../docs/050-Research/Analysis-MVP0-Requirements.md) — đơn vị `chapter` hiện nhập nhằng giữa chương chữ và chương comic.

**Ràng buộc đã kiểm cơ học**: 22 panel · `character_count` max = **3** (trần `INV-2`) · emphasis quota = **1 full_page + 3 large** (đúng `ADR-012 D-23`) · mọi toạ độ **0–1** (`INV-5`) · `panel_index` liên tục 1–22.

**Ngân sách ước tính**: 22 panel × N=3 = **66 ảnh** × `$0.134` ≈ **$8,84** — dưới trần `~$12` (`CF-3.11`).

## ⚠️ Giới hạn đo lường đã biết — đọc trước khi chấm `G1`

Chương này chấm theo phiếu [`C-1…C-8`](../docs/050-Research/Analysis-MVP0-Requirements.md):

| # | Kết quả | Ghi chú |
|:-:|:-:|---|
| `C-1` ≥2 nhân vật cùng cảnh | ⛔ **TRƯỢT** | Xem cảnh báo dưới |
| `C-2` ≥1 cảnh 3 nhân vật | 🟡 Mỏng | Đúng **một** panel (16) |
| `C-3` 8 panel liền cùng nhân vật | ✅ | `lam_uyen` có mặt ở 9 panel, liền mạch |
| `C-4` có thoại | ✅ | Panel 10, 17 |
| `C-5` dấu chồng hai tầng | ✅ | `ế`×25 · `ữ`×8 · `ợ`×8 · 30 loại / 283 lần |
| `C-6` trọn trong ≤30 panel | ✅ | 22 panel, sau khi tách chương comic |
| `C-7` content policy | ⚠️ Rủi ro | Panel **18** (kiếm xuyên ngực + máu) là chỗ rủi ro cao nhất |
| `C-8` bằng chứng đồng ý | — | Founder xác nhận đã có |

> [!WARNING]
> ⭐ **`G1-d` sẽ ra một con số, nhưng con số đó có mẫu quá nhỏ để mang nghĩa.**
>
> - Panel **2 nhân vật**: `n = 3` (panel 14, 15, 18)
> - Panel **3 nhân vật**: `n = 1` (panel 16)
>
> `G1-d` đòi *"panel 2 nhân vật **≥60%** đạt"*, với dải `50–60%` là PASS CÓ ĐIỀU KIỆN. Với `n=3`, các giá trị quan sát được **chỉ có thể là** `0% · 33% · 67% · 100%` — ⛔ **dải `50–60%` không tồn tại trên thang đo này**, và một panel hỏng làm verdict tụt **33 điểm phần trăm**.
>
> ⇒ Khi ghi verdict `G1-d`, **bắt buộc ghi kèm cỡ mẫu**. Báo cáo `67%` mà không nói `n=3` là biến một phép đo trên ba tấm ảnh thành một tuyên bố về năng lực model — đúng thứ [MVP-Scope §7](../docs/010-Planning/MVP-Scope.md) gọi là *"gate biến thành nghi lễ"*.
>
> **Đường xử lý**: bổ sung một chương có hội thoại nhiều người để nâng cỡ mẫu, hoặc chấp nhận và ghi `G1-d` là **đo-và-báo-cáo**, ⛔ không dùng làm điều kiện chặn.

## Việc còn thiếu

- [ ] ⭐ **Corpus NFD**: văn bản gốc là **NFC thuần** (kiểm cơ học: `t == NFC` → `True`). Nghiệm thu [ADR-001](../docs/030-Specs/Architecture/ADR-001-Backend-And-Frontend-Tech-Stack.md) `#5` đòi corpus **cả NFC và NFD** để test tiêu chí (c). ⇒ Phải **chủ động sinh** biến thể NFD từ thoại panel 10 và 17
- [ ] Chương comic **#2** (cánh cửa TÀ → giao kèo → hắc khí → Vọng Tử → khuôn mặt sau mây)
- [ ] Chốt **vendor** image + VLM — `Q-3`, số đo trên provider A ⛔ không chuyển giao sang provider B
- [ ] Ký nhận ngưỡng `[EM]` `G1-c` / `G1-d` **trước** khi đo — `Q-2`
- [ ] Bảng chấm golden dataset (`P-6`)
