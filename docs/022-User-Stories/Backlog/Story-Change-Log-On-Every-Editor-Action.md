---
id: STORY-D-02
type: story
status: draft
created: 2026-08-24
---

# Story-Change-Log-On-Every-Editor-Action

## 1. Story

Là Founder (operator), tôi muốn **MỌI hành động trong editor sinh một `change_log` row — kể cả "chọn ảnh này thay ảnh kia"**, để **việc cắt canvas không đồng thời cắt luôn lá chắn pháp lý**

## 2. Part of

- Epic cha: [Epic-Minimum-Editor](../Epics/Epic-Minimum-Editor.md)
- BRD: [BRD-004-Minimum-Editor](../../020-Requirements/BRD/BRD-004-Minimum-Editor.md)
- Use Case liên quan: cơ chế **xuyên suốt**, áp dụng cho mọi hành động ghi của [UC-02-Review-And-Edit-Story-Bible](../../020-Requirements/Use-Cases/UC-02-Review-And-Edit-Story-Bible.md), [UC-07-Edit-Bubble-And-Dialogue-In-Panel](../../020-Requirements/Use-Cases/UC-07-Edit-Bubble-And-Dialogue-In-Panel.md), [UC-08-Arrange-Page-And-Preview](../../020-Requirements/Use-Cases/UC-08-Arrange-Page-And-Preview.md) — không phải một luồng riêng của một UC

## 3. Bối cảnh & nguồn

Đây là **ràng buộc thiết kế xuyên suốt cả 5 thành phần** editor tối thiểu của hàng **`D1`** ([MVP-Scope §3](../../010-Planning/MVP-Scope.md)), không phải một tính năng của riêng một màn hình — [MVP-Scope §5.2](../../010-Planning/MVP-Scope.md#52-năm-thành-phần-bắt-buộc-2025-em-mẫu-số-saas) khối ghi chú cuối bảng: *"mọi hành động của người dùng trong editor phải sinh một `change_log` row — kể cả hành động chỉ là 'chọn ảnh này thay vì ảnh kia'"*. Đây chính là `KC-2` trong [MVP-Scope §6 — danh sách không được cắt](../../010-Planning/MVP-Scope.md#6-không-được-cắt--danh-sách-cứng).

Anchor exit criterion: **M1-5** ([Roadmap §2](../../010-Planning/Roadmap.md#2-bảng-lộ-trình-tổng), mốc MVP1): *"5 hạng mục provenance (`parent_generation_id`, `relation_kind`, `change_log`, `field_provenance`, `generation.origin`) tồn tại, và có test chứng minh chúng commit CÙNG MỘT transaction với artifact"*.

> [!CAUTION]
> **Story này tồn tại ĐỒNG THỜI ở hai nơi, có chủ ý — không phải trùng lặp cần dọn.** [Epic-Minimum-Editor mục 5](../Epics/Epic-Minimum-Editor.md#5-definition-of-done-cấp-epic) cũng liệt `KC-2` như một mục Definition of Done cấp Epic. Lens phân tích (`findings/business-analyst.md` §4.10) từng đề xuất **chuyển hẳn** ràng buộc này thành DoD và xoá Story riêng — PM đã **bác** đề xuất đó: `KC-2` nằm trong danh sách *"không được cắt"* của `MVP-Scope §6`, và *"một ràng buộc chỉ tồn tại trong DoD thì không có ai tick nó"* (không owner, không estimate, không nằm trong backlog). Giữ ở cả hai chỗ: Story để có người làm và có người tick; DoD để không Story editor nào `Done` mà bỏ sót nó.

## 4. Acceptance Criteria

### Xác minh được

- [ ] Thực hiện một hành động sửa trong **Story Bible editor** (component `#5`) — đo bằng: query `change_log` ngay sau hành động trả về đúng 1 row mới, với `actor`, `action_type`, `entity_id`, `timestamp` đầy đủ
- [ ] Mọi endpoint ghi của editor (Story Bible editor, page layout, bubble/dialogue) đi qua **cùng một middleware `change_log`** — đo bằng: test unit liệt kê toàn bộ endpoint ghi hiện có và xác nhận từng endpoint gọi middleware đó; endpoint nào ghi dữ liệu mà bỏ qua middleware làm test FAIL (cơ chế "selection" như "chọn ảnh này thay ảnh kia" của component `#1` panel card sẽ được test bằng chính middleware này khi component đó build ở MVP3, ngoài phạm vi ước lượng của Story)
- [ ] Thực hiện một hành động sửa **bubble/dialogue** trong panel (khi `Story-Bubble-Text-Overlay-Editor` build xong) — đo bằng: query `change_log` trả về đúng 1 row mới
- [ ] Thực hiện một hành động **swap panel / đổi template** trong page layout (khi `Story-Page-Template-Layout-And-Swap-Panel` build xong) — đo bằng: query `change_log` trả về đúng 1 row mới
- [ ] Mỗi `change_log` row commit **cùng transaction** với thay đổi dữ liệu nó mô tả — đo bằng: test kill process/rollback giữa chừng cho thấy **hoặc cả hai đều tồn tại, hoặc cả hai đều không tồn tại**, không có trạng thái lệch pha (khớp M1-5 + KC-4)

### Đường không hạnh phúc (unhappy path)

- [ ] Một hành động editor gọi API ghi dữ liệu nhưng **worker/network fail giữa chừng trước khi `change_log` được ghi** — transaction phải rollback toàn bộ, không được để dữ liệu đổi mà `change_log` thiếu (đo bằng: test giả lập lỗi network giữa hai câu lệnh ghi, sau đó `GET` dữ liệu chính phải khớp trạng thái TRƯỚC hành động)
- [ ] Một component editor mới được thêm vào (ví dụ tương lai mở lại `D6` UI cây generation) **quên** gọi cơ chế ghi `change_log` — phải có test tự động chặn được lớp này ở tầng service/middleware, không phụ thuộc từng developer nhớ gọi thủ công (đo bằng: một action giả lập bỏ qua middleware bị test unit bắt lỗi, không phải bị bỏ sót âm thầm)
- [ ] Hai hành động editor xảy ra gần như đồng thời trên cùng một entity (race condition) — cả hai đều phải sinh `change_log` row riêng biệt, không được để hành động sau ghi đè mà mất dấu hành động trước (đo bằng: 2 request ghi đồng thời cách nhau <100ms, `change_log` có đủ 2 row)

### Ràng buộc cứng không được vi phạm

- `KC-2` — chính là nội dung của Story này
- `KC-3` — mọi `change_log` row phải phân biệt được `origin` (`ai`/`ai_edited`/`human`) của hành động
- `KC-4` — commit cùng transaction với artifact được chứng minh
- `KC-5` — `change_log` cũng phải có `tenant_id` và tuân RLS như mọi bảng khác

### Story này KHÔNG làm

- Không tự **hiển thị** UI xem lịch sử change log cho người dùng cuối — đó là `D6` UI duyệt cây generation, đã **cắt hẳn** ở horizon này. Story này chỉ đảm bảo dữ liệu **được ghi**, không đảm bảo có màn hình đọc lại
- Không thiết kế cơ chế **rollback/undo** dựa trên `change_log` — undo xuyên state (`D3`) đã hoãn, không mở trong Story này
- Không tự phát minh thêm `action_type` ngoài các hành động mà 4 Story editor còn lại của Epic-D thực sự có
- Không áp dụng cho hành động **ngoài phạm vi editor** (ví dụ: hành động của Director tự động ở Epic-C) — phạm vi Story này là hành động của **con người** trong editor

## 5. Ước lượng

| Đại lượng | Giá trị | Ghi chú |
|---|---|---|
| `E_build` | **20h** `[EM]` ⚠️ vượt trần 16h | **Lý do vượt trần, ghi thành văn (theo §4.3 của `findings/product-owner.md`)**: đây là middleware/service-layer cross-cutting phải tích hợp đúng vào **cả 4 Story editor còn lại** + đảm bảo cùng-transaction (KC-4) qua monolith 1 DB — chi phí không nằm ở một màn hình mà ở việc thiết kế **một cơ chế dùng chung** (ví dụ: decorator/hook ở tầng service) rồi wiring vào từng điểm ghi. Không split được vì split sẽ để lại các component chưa được bảo vệ giữa chừng — đúng lý do "không cắt được theo đường nào" đã ghi ở `findings/business-analyst.md` §4.10 |
| `E_hitl` | **0h/chapter** | Đây là cơ chế **tự động, minh bạch với người dùng** — không tạo thêm thao tác tay nào cho tác giả mỗi chapter. Không phải một HITL gate |

## 6. INVEST

⚠️ **Story này vỡ chuẩn `Independent` và `Small` — nguyên lý do trích từ `findings/business-analyst.md` §4.10**: *"Cross-cutting qua **cả 5 thành phần editor** (`MVP-Scope` §5.2 ràng buộc xuyên suốt) ⇒ mỗi Story editor mới đều mở lại Story này. Đề xuất: đưa nó thành Definition of Done của Epic-D, không phải một Story"*.

PM đã cân nhắc đề xuất đó và **quyết định giữ nguyên là một Story riêng, đồng thời cũng là một mục DoD cấp Epic** (xem callout ở mục 3 và [Epic-Minimum-Editor mục 5](../Epics/Epic-Minimum-Editor.md#5-definition-of-done-cấp-epic)) — vì `KC-2` là ràng buộc **không được cắt**, và một ràng buộc chỉ nằm trong DoD thì không có ai sở hữu việc triển khai nó.

---

_Created by product-owner_
_Author: trisjr_
