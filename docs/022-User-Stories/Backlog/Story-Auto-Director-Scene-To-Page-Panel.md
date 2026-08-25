---
id: STORY-C-02
type: story
status: draft
created: 2026-08-24
---

# Story-Auto-Director-Scene-To-Page-Panel

## 1. Story

Là tác giả truyện chữ, tôi muốn **hệ thống tự chia scene thành page và panel**, để **không phải viết tay panel script cho từng chương**.

## 2. Part of

- Epic cha: [Epic-Comic-Director-And-Layout](../Epics/Epic-Comic-Director-And-Layout.md)
- BRD cha: [BRD-003-Comic-Director-And-Layout](../../020-Requirements/BRD/BRD-003-Comic-Director-And-Layout.md)
- UC liên quan: [UC-03-Review-Panel-Script](../../020-Requirements/Use-Cases/UC-03-Review-Panel-Script.md)

## 3. Bối cảnh & nguồn

- `MVP-Scope.md` §3 hạng mục **C2** — *"Director tự động scene → page → panel"*: `❌ viết tay` ở MVP0, `⛔` ở MVP1, `✅` từ MVP2. Căn cứ: CF-8.8.
- `Roadmap.md` mốc **MVP2 — Comic Director**, exit criterion **M2-1**: *"Director sinh page/panel tự động cho ≥1 chapter mà không cần panel script viết tay"*.
- `Roadmap.md` §3.3 mục *"Nội dung theo CF-8.8"* liệt kê Director là nền cho ba điều chỉnh khác của MVP2 (rubric, ≤3 nhân vật, `text_safe_zone`) — Director sinh ra Panel Specification (`Story-Comic-IR-Panel-Specification`) làm output.
- Rủi ro chính đã ghi ở `Roadmap §3.3`: *"Directing nhồi hết nhân vật vào một panel"* — Director phải **thiên vị panel một nhân vật vì lý do kỹ thuật**, và LLM không biết điều đó nếu không được nói tường minh (Analysis §5.6).

## 4. Acceptance Criteria

### Xác minh được

- [ ] Đưa vào Director ≥1 chapter đã có Story Bible + timeline state (từ MVP1), Director sinh ra tập page/panel spec hợp lệ theo schema Comic IR **mà không cần bất kỳ dòng panel script viết tay nào** — đo bằng: chạy trên 1 chapter, đếm số panel spec sinh ra > 0 và 100% pass schema validation.
- [ ] Mỗi scene trong chapter đầu vào được ánh xạ tới ≥1 panel trong output — đo bằng: đối chiếu danh sách scene input với danh sách `scene_id` xuất hiện trong panel spec output, không có scene nào bị bỏ sót.
- [ ] Panel spec do Director sinh ra tuân thủ ràng buộc ≤3 nhân vật/panel ngay tại thời điểm sinh (không đợi DB reject ở bước sau) — đo bằng: đếm nhân vật mỗi panel trong output, 100% panel ≤3.

### Đường không hạnh phúc (unhappy path)

- [ ] Scene có >3 nhân vật cùng lúc active theo timeline state: Director phải tách thành nhiều panel qua shot xa/silhouette/crop thay vì tạo panel vi phạm ràng buộc — đo bằng: test 1 scene có 5 nhân vật active, kiểm tra output không có panel nào vượt 3 nhân vật.
- [ ] Chapter đầu vào có scene rỗng hoặc scene không xác định được nhân vật nào (extraction lỗi từ MVP1): Director phải trả về lỗi tường minh cho scene đó, không tạo panel với dữ liệu nhân vật rỗng/giả — đo bằng: test input scene rỗng, kiểm tra output ghi nhận lỗi thay vì panel spec sai.

### Ràng buộc cứng không được vi phạm

- `C5` (≤3 nhân vật/panel, xem `Story-Enforce-Max-Three-Characters-Per-Panel`) — Director là nơi ràng buộc này được **thi hành sớm nhất** trong pipeline, dù DB vẫn là tuyến phòng thủ cuối.

### Story này KHÔNG làm

- [ ] KHÔNG tự quyết định `beat_type` hay emphasis quota cho từng panel — đó là `Story-Layout-Rubric-Beat-Type-And-Emphasis-Quota`.
- [ ] KHÔNG chừa `text_safe_zone` trong spec sinh ra — đó là `Story-Text-Safe-Zone-In-Panel-Spec` (Director gọi tới sau khi field này tồn tại trong schema, không tự cài đặt nó).
- [ ] KHÔNG cho phép người dùng chỉnh sửa page/panel do Director sinh ra qua UI kéo-thả — đó là `UC-08-Arrange-Page-And-Preview` / Epic-Minimum-Editor.
- [ ] KHÔNG thực hiện human gate xác nhận speaker/dialogue — đó là hai Story human gate riêng.

## 5. Ước lượng

| Đại lượng | Giá trị | Ghi chú |
|---|---|---|
| `E_build` | **~16 giờ-người** `[EM]` | Ở trần. Nếu logic tách panel theo timeline state phức tạp hơn dự kiến (nhiều scene đồng thời-nhân-vật), có nguy cơ vượt trần — theo dõi tại thời điểm implement, không tự vượt trần trước. |
| `E_hitl` | **0 giờ-người/chapter** | Director tự động không tự nó tạo gate; output của nó được duyệt tại `UC-03-Review-Panel-Script`, đo ở phạm vi Story khác (đã tồn tại từ MVP0 dưới dạng review thủ công). |

## 6. INVEST

- **I (Independent)**: ✅ Phụ thuộc **đầu vào** (Story Bible + timeline state từ MVP1) nhưng không phụ thuộc lẫn nhau với các Story còn lại của Epic-C theo chiều ngược — có thể ship trước rubric/`text_safe_zone`/human gate và vẫn tạo giá trị đo được (M2-1 tự đứng độc lập với M2-2/M2-3/M2-4).
- **S (Small)**: ⚠️ Theo `findings/business-analyst.md` §4.3 — cờ gốc là `⚠️`. Lý do: logic Director phải "biết" ràng buộc ≤3 nhân vật và phải xử lý shot xa/silhouette/crop cho cảnh đông người (Analysis §5.6) — đây là logic nghiệp vụ không tầm thường, khác với việc chỉ ghi một trường dữ liệu. Chưa đủ dữ kiện để khẳng định vượt trần `E_build`, nhưng rủi ro vượt là thật và đã ghi ở mục 5.

---

_Created by product-owner_
_Author: trisjr_
