---
id: STORY-H-01
type: story
status: draft
created: 2026-08-24
---

# Story-Golden-Dataset-For-Regression

## 1. Story

Là Founder (operator), tôi muốn **một golden dataset 15–20 panel có spec + ref + ảnh + bảng chấm**, để **mọi thay đổi prompt/model về sau đo được thay vì đoán**.

## 2. Part of

- Epic cha: [Epic-Quality-And-Operations](../Epics/Epic-Quality-And-Operations.md)
- BRD cha: [BRD-008-Quality-And-Operations](../../020-Requirements/BRD/BRD-008-Quality-And-Operations.md)
- UC liên quan: [UC-06-Generate-Panel-And-Pick-Variant](../../020-Requirements/Use-Cases/UC-06-Generate-Panel-And-Pick-Variant.md) — không có UC riêng cho dataset; đây là UC nơi panel/candidate được sinh ra và trở thành nguyên liệu của dataset, không phải một luồng người dùng riêng.

## 3. Bối cảnh & nguồn

- `MVP-Scope.md` §3 hạng mục **H6** — *"Golden dataset regression (15–20 panel có spec + ref + ảnh + đánh giá)"*: `✅` ở **mọi** mốc MVP0–MVP4. Căn cứ: `findings/architect.md` §7.3 điểm 4 — *"tài sản dùng suốt vòng đời"*, không phải artifact của riêng MVP0.
- `Roadmap.md` mốc **Pre-cycle 09/2026**, exit criterion **P-6**: *"golden dataset tồn tại dưới dạng file (spec + ref + ảnh + bảng chấm)"*.
- `Roadmap.md` §6.2 bảng phụ thuộc: *"Golden dataset của MVP0 → Eval kit ở MVP1 (M1-6) — Mềm, có thể dựng lại, nhưng dựng lại tốn tiền API lần hai"*. Đây là lý do dataset phải được lưu bền, không phải chỉ tồn tại trong bộ nhớ tạm của script MVP0.
- CF-8.4/CF-8.5/CF-8.6: MVP0 kéo dài **1–2 tuần**, phạm vi **1 chapter duy nhất**, code đúng **một việc**, đo 3 chỉ số chính + 2 chỉ số bổ sung.
- `MVP-Scope.md` §3.1: *"code của MVP0 KHÔNG phải nền của sản phẩm — viết để trả lời câu hỏi rồi bỏ, giữ lại kết luận và dữ liệu"*. Golden dataset chính là phần **dữ liệu giữ lại** sau khi code MVP0 bị vứt.

## 4. Acceptance Criteria

### Xác minh được

- [ ] Dataset chứa tối thiểu **15** và tối đa **20** panel — đo bằng: đếm số bản ghi panel trong dataset.
- [ ] Mỗi panel trong dataset có đủ 4 trường bắt buộc: Panel Specification, ảnh reference, ảnh output đã sinh, bảng chấm — đo bằng: script kiểm tra completeness trả về **0** panel thiếu trường trên tổng số panel.
- [ ] Bảng chấm của mỗi panel ghi giá trị cho các tiêu chí gate G1 áp dụng ở mức panel (`G1-a` consistency, `G1-d` attribute binding) — đo bằng: đối chiếu số cột đã điền trong bảng chấm với danh sách tiêu chí, không panel nào thiếu cột.
- [ ] Dataset được lưu tại một vị trí lưu trữ cố định, độc lập với thư mục chạy script MVP0 — đo bằng: dataset load thành công từ vị trí lưu trữ lâu dài **sau khi** code/thư mục tạm của MVP0 đã bị xoá theo kỷ luật code dùng một lần của MVP0.
- [ ] Load lại dataset hai lần liên tiếp (không sinh ảnh mới) cho ra cùng nội dung — đo bằng: so sánh hash nội dung dataset giữa hai lần load, diff = 0.

### Đường không hạnh phúc (unhappy path)

- [ ] Nếu MVP0 dừng giữa chừng vì vượt trần ngân sách thực tế **~$50** (rủi ro đã ghi ở `Roadmap.md` §3.1) mà chưa đủ 15 panel, dataset chính thức phải ghi rõ số panel thực tế và lý do dừng, **không** được làm tròn lên 15 để "cho đủ" — đo bằng: tồn tại trường `actual_panel_count` và `stopped_reason` khi số panel < 15.
- [ ] Nếu một panel bị lỗi kỹ thuật ở bước sinh ảnh (ví dụ VLM trả về lựa chọn không nằm trong 3 candidate, theo unhappy path của `Story-Generate-Panel-With-Reference-And-VLM-Select`), panel đó bị loại khỏi tập đếm 15–20, không được tính là panel hợp lệ — đo bằng: đối chiếu danh sách panel lỗi kỹ thuật với danh sách panel trong dataset chính thức, không có phần giao nhau.
- [ ] Vì golden dataset **không backfill được rẻ** (dựng lại tốn tiền API lần hai, `Roadmap.md` §6.2), phải tồn tại ≥1 bản backup ở vị trí lưu trữ khác với nơi chạy script MVP0 — đo bằng: kiểm tra tồn tại bản copy độc lập.

### Ràng buộc cứng không được vi phạm

- — Không có `KC-x`/`C-x`/`AG-x` áp trực tiếp lên dataset này. Ghi chú: dataset không chạm 7 mục `KC-1…KC-7` vì nó không phải dữ liệu người dùng thật — chỉ là 1 chapter của Founder, chạy trong MVP0 (không DB, không tenant).

### Story này KHÔNG làm

- [ ] KHÔNG tự động chạy eval kit trên dataset — đó là phạm vi của `Story-HITL-Gate-And-Eval-Kit` (exit criterion **M1-6**).
- [ ] KHÔNG mở rộng dataset sang nhiều chapter — giữ đúng phạm vi **1 chapter duy nhất** của MVP0 (CF-8.4).
- [ ] KHÔNG dùng VLM để tự chấm bảng chấm thay người — bảng chấm của dataset là chấm bằng mắt của Founder, theo đúng cách đo của `G1-a`…`G1-d` (`MVP-Scope.md` §7.2).
- [ ] KHÔNG dùng dataset này làm hồ sơ pháp lý provenance (`KC-1…KC-4`) — đây là tài sản kỹ thuật đo chất lượng, không phải bằng chứng compliance.

## 5. Ước lượng

| Đại lượng | Giá trị | Ghi chú |
|---|---|---|
| `E_build` | **~6 giờ-người** `[EM]` | Thời gian tổ chức file dataset + chấm bằng mắt 15–20 panel, tách biệt khỏi effort sinh ảnh (đã tính ở `Story-Generate-Panel-With-Reference-And-VLM-Select`, ~24h). Trong trần 16h. |
| `E_hitl` | **0 giờ-người/chapter** | Việc tạo dataset là **một lần** (one-time, gắn với 1 chapter MVP0), không phải nghĩa vụ lặp lại theo chapter — khác với `Story-Record-Readability-Human-Judgement`, vốn là nghĩa vụ **liên tục**. |

## 6. INVEST

`INVEST không áp — Story thuộc [MVP0]`. Lý do (`findings/business-analyst.md` §4.9, `MVP-Scope.md` §3.1, `Roadmap.md` §3.1): code của MVP0 không phải nền của sản phẩm — viết để trả lời câu hỏi rồi bỏ, giữ lại kết luận và dữ liệu. Story này là một lát cắt xuyên tầng để mua dữ liệu đo lường cho gate G1 và cho eval kit MVP1, không phải một tính năng giao cho khách; tiêu chí `Valuable` của nó là **thông tin đo được** (chính dataset), không phải tính năng.

**Definition of Done — 5 tiêu chí gate G1** (`MVP-Scope.md` §7.2), thay cho Acceptance Criteria kiểu Gherkin thông thường — dataset này là **nguyên liệu đo** của cả 5 tiêu chí:

- [ ] `G1-a` Consistency nhân vật ≥70% panel — dataset cung cấp panel để chấm tiêu chí này (`⚠️ [EM]` ngưỡng do run trước định nghĩa).
- [ ] `G1-b` N tối thiểu ≤3 để VLM-select ra panel đạt.
- [ ] `G1-c` `reject_rate` sau VLM-select có số và verdict phân loại đúng dải (`≤30%` PASS · `30–50%` PASS có điều kiện · `>50%` FAIL) `⚠️ [EM]`.
- [ ] `G1-d` Panel 2 nhân vật ≥60% đúng identity + attribute binding; panel 3 nhân vật đo và báo cáo, không đặt ngưỡng chặn `⚠️ [EM]`.
- [ ] `G1-e` 100% panel có thoại dùng overlay, 0 panel nhờ model render chữ — dataset phải chứa cả panel có thoại để tiêu chí này đo được.

⛔ Dùng đúng tên **MVP0** — `Glossary.md` cấm *"phase 0"*, *"spike"*, *"PoC"* (`CẤM-11`).

---

_Created by quality-assurance_
_Author: trisjr_
