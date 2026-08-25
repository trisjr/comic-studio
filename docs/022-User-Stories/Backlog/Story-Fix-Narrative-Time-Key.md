---
id: STORY-B-01
type: story
status: draft
created: 2026-08-24
---

# Story-Fix-Narrative-Time-Key

## 1. Story

Là **Founder (architect)**, tôi muốn **khoá thời gian dùng `timeline_id` + `story_order` thay cho `(chapter, scene)`**, để **flashback không làm sai state một cách âm thầm**

## 2. Part of

- Epic cha: [Epic-Story-Intelligence](../Epics/Epic-Story-Intelligence.md)
- BRD: [BRD-002-Story-Intelligence](../../020-Requirements/BRD/BRD-002-Story-Intelligence.md)
- Use Case liên quan: không có UC nào chạy trực tiếp Story này — nó là **khoá thời gian nền** mà [UC-02-Review-And-Edit-Story-Bible](../../020-Requirements/Use-Cases/UC-02-Review-And-Edit-Story-Bible.md) và [UC-03-Review-Panel-Script](../../020-Requirements/Use-Cases/UC-03-Review-Panel-Script.md) đọc/ghi thông qua nó, chứ không phải một tương tác goal-level của actor

## 3. Bối cảnh & nguồn

Đây là hàng **`B4`** của [MVP-Scope §3](../../010-Planning/MVP-Scope.md#3-bảng-mvp-vs-full-scope): *"Khoá thời gian đúng (thay `(chapter, scene)`)"* — không có ô mốc `✅/🟡/⛔/❌` vì nó phải xong **trước** MVP0 chấm điểm được, dùng nguyên chú thích nguồn *"Analysis §5.1 — sai âm thầm ở flashback; phải sửa trước dòng code đầu tiên"*.

Exit criterion tương ứng là **`P-4`** của [Roadmap §2](../../010-Planning/Roadmap.md#2-bảng-lộ-trình-tổng), mốc **Pre-cycle 09/2026**: *"khoá thời gian thay `(chapter, scene)` được viết ra dưới dạng schema draft"* — trước dòng code đầu tiên, không phải sau. [Roadmap §6.2](../../010-Planning/Roadmap.md#62-bảng-phụ-thuộc) xếp đây là **phụ thuộc CỨNG** của mọi bảng timeline dùng ở MVP1.

Nền lý thuyết: [Glossary.md](../../999-Resources/Glossary.md) mục *syuzhet vs fabula* — **syuzhet** (`reading_order`, thứ tự người đọc gặp sự kiện) khác **fabula** (`story_order`, thứ tự sự kiện thực sự xảy ra); dùng `(chapter, scene)` làm khoá thời gian sai âm thầm ở **mọi** flashback. Mục *`timeline_id`* — định danh nhánh thời gian, cho phép nhiều dòng thời gian song song (hồi tưởng, giấc mơ, tuyến phụ) mà không làm hỏng phép reduce trạng thái.

## 4. Acceptance Criteria

### Xác minh được

- [ ] Schema draft dùng `timeline_id` + `story_order` làm khoá thời gian chính thức cho mọi bảng cần thứ tự sự kiện của module Story Intelligence — đo bằng: tồn tại artifact schema draft (`P-4`) có ngày tạo **trước** ngày commit code sản phẩm đầu tiên của MVP1
- [ ] Một sự kiện flashback (đọc ở chapter N nhưng `story_order` thuộc thời điểm trước chapter N) có `story_order` khác với thứ tự đọc (`chapter`, `scene`) của nó — đo bằng: query event đó trả về `story_order` < `story_order` của các event ở chapter trước N
- [ ] Không còn bảng nào trong schema `story` dùng cặp `(chapter, scene)` làm khoá thời gian duy nhất — đo bằng: rà soát schema, 0 kết quả dùng cặp đó làm primary/foreign key thời gian
- [ ] Hai event có cùng `story_order` nhưng khác `timeline_id` (ví dụ giấc mơ chạy song song với mạch chính) được lưu là hai chuỗi độc lập — đo bằng: query theo `timeline_id` trả về đúng tập event của nhánh đó, không lẫn nhánh kia

### Đường không hạnh phúc (unhappy path)

- [ ] Insert một event thiếu `story_order` — hệ thống **từ chối** insert, không tự suy ra giá trị mặc định từ `(chapter, scene)` (đo bằng: request thiếu `story_order` trả lỗi ràng buộc, không có row mới được tạo)
- [ ] Sửa `story_order` của một event đã tồn tại (biên tập lại thứ tự) — mọi giá trị `state_at` phụ thuộc event đó phải phản ánh thay đổi ở lần gọi tiếp theo, không giữ giá trị đã cache từ khoá cũ (đo bằng: gọi lại truy vấn state sau khi sửa, kết quả khác với trước khi sửa và khớp `story_order` mới)
- [ ] Dữ liệu Story Bible viết tay của MVP0 (đang dùng `(chapter, scene)`) được migrate sang khoá mới — bản ghi nào không gán được `story_order` hợp lệ thì bị đánh dấu `cần xác nhận thủ công`, không bị âm thầm bỏ qua hay gán sai (đo bằng: sau migrate, 0 record ở trạng thái vừa "đã migrate" vừa thiếu `story_order`)

### Ràng buộc cứng không được vi phạm

- —

### Story này KHÔNG làm

- Không migrate dữ liệu sản xuất thật — tại thời điểm Story này chạy (pre-cycle 09/2026), chưa có tenant nào và chưa có dữ liệu thật; phạm vi chỉ là schema draft + dữ liệu viết tay của MVP0
- Không implement Timeline State Resolver (`state_at(N) = reduce(events)`) — đó là `Story-Timeline-State-Resolver`, Story tiêu thụ khoá thời gian này
- Không implement Story Bible extraction — đó là `Story-Story-Bible-Extraction`
- Không có UI cho tác giả xem/sửa timeline — thuộc `Story-Story-Bible-Editor-Form` (Epic-D)

## 5. Ước lượng

| Đại lượng | Giá trị | Ghi chú |
|---|---|---|
| `E_build` | **8h** `[EM]` | Thiết kế schema draft (`timeline_id` + `story_order`), viết script migrate dữ liệu viết tay MVP0, và cập nhật mọi bảng liên quan trong schema `story`. Trong trần 16h — đây là một quyết định kiến trúc hẹp, không phải một tính năng nhiều tầng |
| `E_hitl` | **0** | Không tạo ra HITL gate lặp lại; đây là một thay đổi schema một lần, không phải một quy trình vận hành theo chapter |

## 6. INVEST

- **I (Independent)**: ⚠️ — theo nguyên văn lý do tại [`findings/business-analyst.md` §4.10](../../010-Planning/pm-runs/2026-08-24-khoi-tao-requirements-stories-comic-studio/findings/business-analyst.md#410-bảy-story-sẽ-vỡ-khi-cắt-lô--pm-cần-biết-trước): *"Nó nằm trong khoá của mọi bảng timeline (`Roadmap` §6.2: phụ thuộc cứng). Làm sau MVP1 = migration toàn bộ. Nó là điều kiện tiên quyết, không phải một lô song song."* Ba Story còn lại của Epic-B đọc/ghi đúng cái khoá mà Story này định nghĩa — không có cách xếp nó song song với chúng.
- **S (Small)**: ✅ — phạm vi hẹp (một quyết định khoá thời gian + migrate dữ liệu viết tay), nằm gọn trong trần `E_build ≤ 16h`.

---

_Created by product-owner_
_Author: trisjr_
