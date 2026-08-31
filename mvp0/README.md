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
| [`panel-script-ch1.yaml`](./panel-script-ch1.yaml) | **22 panel / trang 1–6** — nghĩa địa → tỉnh dậy → bia đá → flashback → ký hiệu con mắt | `Roadmap §2` · [DB-Entity-Comic-IR](../docs/030-Specs/Schema/DB-Entity-Comic-IR.md) |
| [`panel-script-ch2.yaml`](./panel-script-ch2.yaml) | **20 panel / trang 7–12** — cánh cửa TÀ → giao kèo → hắc khí → Vọng Tử → khuôn mặt sau mây | như trên |
| [`typeset-corpus.json`](./typeset-corpus.json) | **5 mục** ở **cả NFC và NFD**, sinh bằng [`scripts/gen-typeset-corpus.py`](../scripts/gen-typeset-corpus.py) | `ADR-001` `## Consequences` **#5** |
| [`threshold-signoff.md`](./threshold-signoff.md) | Phiếu ký nhận ngưỡng `[EM]` — **ký TRƯỚC khi đo** | `MVP-Scope §7` · `Q-2` |

**Nguồn**: *Tà Nguyệt Vô Tận* — Chương chữ 1 *(Người chết trở về)*, tách thành **hai chương comic**.

**Ràng buộc đã kiểm cơ học** (cả hai file): tổng **42 panel / 12 trang** · `character_count` max = **3** (trần `INV-2`) · emphasis quota **mỗi chương comic** = 1 full_page + 3 large (đúng `ADR-012 D-23`) · mọi toạ độ **0–1** (`INV-5`) · `panel_index` liên tục 1–42.

> [!WARNING]
> ⚠️ **Ngân sách vượt trần `~$12`.** Phủ trọn chương chữ = **42 panel × N=3 = 126 ảnh** × `$0.134` ≈ **$16,88** — vượt `~$12` (`CF-3.11`) khoảng **41%**, nhưng vẫn **dưới trần thực tế `~$50`** (`Analysis §10`).
>
> **Đường lui nếu cần ép về ngân sách**: chạy **chỉ chương comic #1** (22 panel ≈ **$8,84**). Đổi lại thì mất phần đo `G1-e` giàu nhất — 7 trong 9 panel có thoại nằm ở chương comic #2.

> [!NOTE]
> ⭐ **Điểm dữ liệu đầu tiên cho `G-07`**: chương chữ này ra **42 panel**, so với giả định **60 ảnh/chapter** `[EM]` `CF-3.3` — **thấp hơn 30%**.
>
> ⛔ **Chưa kết luận được gì**: `n = 1`, và đây là số panel do **người phân cảnh**, ⛔ không phải số đo từ hệ thống. Nhưng nó là điểm dữ liệu thật đầu tiên chạm vào thứ mà `Charter §8 A1` gọi là *"thừa số gốc của toàn bộ mô hình chi phí"*. Ghi lại để đối chiếu khi có chương thứ hai.

## ⚠️ Giới hạn đo lường đã biết — đọc trước khi chấm `G1`

Chương này chấm theo phiếu [`C-1…C-8`](../docs/050-Research/Analysis-MVP0-Requirements.md):

| # | Kết quả | Ghi chú |
|:-:|:-:|---|
| `C-1` ≥2 nhân vật cùng cảnh | ⛔ **TRƯỢT** | Xem cảnh báo dưới |
| `C-2` ≥1 cảnh 3 nhân vật | 🟡 Mỏng | Đúng **một** panel (16) |
| `C-3` 8 panel liền cùng nhân vật | ✅ | `lam_uyen` có mặt ở **24/42** panel |
| `C-4` có thoại | ✅ | **9 panel** có thoại, gồm **2 ca typeset khó** — xem dưới |
| `C-5` dấu chồng hai tầng | ✅ | `ế`×25 · `ữ`×8 · `ợ`×8 · 30 loại / 283 lần |
| `C-6` trọn trong ≤30 panel | ✅ | **22 và 20 panel** — mỗi chương comic đều dưới trần |
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

## Provider dùng cho MVP0

> [!IMPORTANT]
> ⚠️ **Đây là LỰA CHỌN VẬN HÀNH để chạy MVP0, ⛔ KHÔNG phải chốt vendor.**
>
> [ADR-007](../docs/030-Specs/Architecture/ADR-007-VLM-Provider-For-QA-Select.md) `Q4` đã định sẵn: *"**Ai đóng**: PM + Architect. **Khi nào**: tại gate cuối **MVP0**, khi ba phép đo bắt buộc của MVP0 có kết quả."* Lý do là biến quyết định — chi phí per-call, `N` tối thiểu, human-reject rate — **chính là output của MVP0**. ⇒ Chốt trước là *"chọn mù"* (chữ của ADR).

| Vai trò | Dùng cho MVP0 | Căn cứ |
|---|---|---|
| **Sinh ảnh** | **Gemini 3 Pro Image** (Nano Banana Pro) — `$0.134` standard / `$0.067` batch | ⛔ **Không phải lựa chọn mới.** [Spec-Integration-Image-Provider §6.2](../docs/030-Specs/API/Spec-Integration-Image-Provider.md) và **mọi** con số chi phí trong repo (`~$12`, `$12,06`, `CF-3.11`, `CF-3.5`) đều **đã tính từ provider này** |
| *Đường lui sinh ảnh* | FLUX.2 pro — `$0.03` | Đã ghi sẵn là *"đường lui"* ở cùng bảng giá |
| **VLM-select** | ⭐ **Cùng Gemini**, nhưng qua **adapter RIÊNG** | Xem hai lý do dưới |

**Vì sao dùng chung vendor cho VLM-select:**

1. [ADR-007](../docs/030-Specs/Architecture/ADR-007-VLM-Provider-For-QA-Select.md) dòng 185 nêu chính xác cái giá của việc thêm provider: *"**Thêm một provider = thêm một điểm phụ thuộc ngoài**: một bộ credential, một hạn mức, một chính sách nội dung có thể từ chối (`D-67`), một bề mặt drift."* Với MVP0 — một lát cắt 1–2 tuần để **mua thông tin** — trả cái giá đó cho một vendor thứ hai ⛔ không mua thêm được thông tin nào.
2. Chọn khác Gemini cho phần sinh ảnh sẽ làm **lệch toàn bộ mô hình chi phí** đã dựng trên `$0.134` — và `G2` (gate kinh tế) lấy đầu vào từ chính những con số đó.

⚠️ **Adapter phải TÁCH, dù cùng vendor.** [ADR-007](../docs/030-Specs/Architecture/ADR-007-VLM-Provider-For-QA-Select.md) `Q1`: *"VLM QA-select là **integration thứ hai, riêng biệt**, ⛔ không phải một hàm của adapter ảnh"* — ba lý do: hai vòng đời model version khác nhau (pin riêng), hai đường lỗi khác nhau (*"ảnh sinh xong nhưng chấm hỏng là một trạng thái hợp lệ"*). ⇒ **Cùng vendor, hai adapter.** ⛔ Đừng gộp cho tiện.

**Việc chốt vendor thật** vẫn dùng **5 tiêu chí `Q5`** của `ADR-007`, theo thứ tự — tiêu chí #1 (*nhận nhiều ảnh trong MỘT call*) là tiêu chí **loại**, ⛔ không phải cộng điểm.

## ⭐ Hai ca typeset khó — nơi `G1-e` thật sự bị thử

`G1-e` đòi **100%** panel có thoại dùng overlay và **0** panel nhờ model render chữ. Chín panel có thoại chứa **hai loại bubble mà một chương đối thoại thường ⛔ không có**:

| Loại | Panel | Vì sao khó |
|---|---|---|
| `voice_no_speaker` | 27, 42 | Tà Thần và thiên đạo ⛔ **không có thân thể** — bubble ⛔ không có đuôi trỏ về người nói. Chạm thẳng vào **human gate speaker attribution** (MVP2) ngay từ MVP0 |
| `system_panel` | 37, 39, 40 | Bảng trạng thái là **giao diện**, ⛔ không phải lời thoại. ⭐ Đây là chỗ dễ hỏng nhất: model rất hay **tự vẽ "bảng chữ" thành một phần của tranh** — mà đó chính là định nghĩa của việc **trượt `G1-e`** |

## Việc còn thiếu

- [ ] Chốt **vendor VLM** — `Q-3`. ⚠️ ⛔ **KHÔNG chặn MVP0**: `ADR-007` `Q4` đặt việc này ở **gate cuối MVP0**, vì đầu vào của nó là chính số đo MVP0
- [ ] Ký nhận [`threshold-signoff.md`](./threshold-signoff.md) — `Q-2`, phải xong **trước** khi sinh ảnh đầu tiên
- [ ] Bảng chấm golden dataset (`P-6`) — 15–20 panel có spec + ref + ảnh + đánh giá
- [ ] Nâng cỡ mẫu `G1-d`, hoặc chấp nhận ghi nó là **đo-và-báo-cáo** thay vì điều kiện chặn

**Đã xong**: ✅ Story Bible · ✅ panel script cả hai chương comic · ✅ corpus NFC/NFD · ✅ provider vận hành cho MVP0
