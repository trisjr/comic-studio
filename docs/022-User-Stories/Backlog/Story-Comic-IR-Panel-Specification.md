---
id: STORY-C-01
type: story
status: draft
created: 2026-08-24
---

# Story-Comic-IR-Panel-Specification

## 1. Story

Là tác giả truyện chữ, tôi muốn **panel được lưu dưới dạng spec có schema, không phải dưới dạng ảnh**, để **sửa một field thay vì re-roll cả ảnh**.

## 2. Part of

- Epic cha: [Epic-Comic-Director-And-Layout](../Epics/Epic-Comic-Director-And-Layout.md)
- BRD cha: [BRD-003-Comic-Director-And-Layout](../../020-Requirements/BRD/BRD-003-Comic-Director-And-Layout.md)
- UC liên quan: [UC-03-Review-Panel-Script](../../020-Requirements/Use-Cases/UC-03-Review-Panel-Script.md)

## 3. Bối cảnh & nguồn

- `MVP-Scope.md` §3 hạng mục **C1** — *"Comic IR / Panel Specification (spec là dữ liệu chính)"*: `🟡 YAML tay` ở MVP0, `✅` từ MVP1. Căn cứ: `Analysis §4.2` — Comic IR đã được xếp là hàng **rủi ro thấp nhất** của bảng khả thi.
- `Roadmap.md` mốc **Pre-cycle 09/2026**, exit criterion **P-2**: *"G1 có SỐ cho cả 5 tiêu chí và verdict được ghi"* — đây là exit criterion mà bản MVP0 (YAML viết tay) của Story này phải phục vụ. Không có `M1-x` riêng cho C1 vì C1 chuyển sang `✅` ngay từ MVP1 với vai trò nền tảng cho toàn bộ dữ liệu, không phải một cột deliverable độc lập của bảng lộ trình mục 2.
- **Comic IR** (`Glossary.md`): tầng biểu diễn trung gian giữa văn bản gốc và ảnh — mô tả cấu trúc truyện tranh dưới dạng dữ liệu có schema, **trước khi** bất kỳ ảnh nào được sinh.
- **Panel Specification** (`Glossary.md`): đơn vị dữ liệu mô tả đầy đủ một panel (bố cục, nhân vật, camera, ràng buộc thị giác, vùng an toàn cho chữ) — là *"dữ liệu chính"*, ảnh là output phái sinh.
- Panel Specification là input trực tiếp của **Visual Prompt Compiler** (`Glossary.md`, thuộc Epic-A) — compiler tra bảng `field value → cụm từ`, xử lý xung đột theo **precedence ladder** (identity refs không bao giờ bị drop) và **constraint budget**. Story này chỉ chịu trách nhiệm cho schema đủ trường để compiler đọc được; không viết lại compiler.

## 4. Acceptance Criteria

> Ghi chú áp dụng cho toàn bộ khối dưới: Story này mang **hai dấu** kế thừa từ Epic cha — bản **MVP0 (YAML viết tay)** và phần **vượt khỏi MVP0**. Bốn khối AC bên dưới mô tả phần vượt khỏi MVP0 (schema chính thức từ MVP1); Definition of Done riêng cho lát cắt MVP0 nằm ở mục 6.

### Xác minh được

- [ ] Một `Panel Specification` hợp lệ chứa tối thiểu các trường: nhân vật có mặt, hành động, camera, ràng buộc thị giác, vùng an toàn cho chữ (`text_safe_zone`) — đo bằng: schema validation PASS trên ≥1 spec mẫu có đủ 5 trường.
- [ ] Sửa một trường của spec (ví dụ đổi camera) không làm thay đổi bất kỳ trường nào khác của cùng spec — đo bằng: diff trước/sau chỉ có đúng 1 trường đổi.
- [ ] Panel Specification được lưu như **dữ liệu chính** (bản ghi trong DB/schema `comic`), ảnh sinh ra được liên kết tới spec qua khoá ngoại — đo bằng: query 1 spec trả về 0 hoặc nhiều ảnh liên kết, không có ảnh nào tồn tại mà không trỏ về một spec.

### Đường không hạnh phúc (unhappy path)

- [ ] Insert một Panel Specification thiếu trường bắt buộc (ví dụ thiếu danh sách nhân vật) bị **DB từ chối**, không phải chỉ log cảnh báo — đo bằng: test insert thiếu trường trả về lỗi constraint.
- [ ] Spec có nhân vật được tham chiếu nhưng nhân vật đó không tồn tại trong Story Bible bị từ chối tại thời điểm ghi, không phải phát hiện muộn ở thời điểm sinh ảnh — đo bằng: test insert với `character_id` không tồn tại trả về lỗi.

### Ràng buộc cứng không được vi phạm

- — (không có `KC-x`/`Charter §7 C-x`/`AG-x` trực tiếp áp cho schema nền này). Ghi chú: schema Comic IR là nơi hạng mục `MVP-Scope §3` **C5** (≤3 nhân vật/panel — xem `Story-Enforce-Max-Three-Characters-Per-Panel`) và **C6** (`text_safe_zone` — xem `Story-Text-Safe-Zone-In-Panel-Spec`) cắm vào. Hai Story đó **mở rộng** schema này, không thay thế.

### Story này KHÔNG làm

- [ ] KHÔNG tự sinh ảnh từ spec — đó là Visual Prompt Compiler + pipeline sinh ảnh của Epic-A.
- [ ] KHÔNG cài đặt cơ chế Layout Score 5 số thực — hạng mục `C4` đã **cắt hẳn** (`CF-9.3`).
- [ ] KHÔNG viết Director tự động scene → page → panel — đó là `Story-Auto-Director-Scene-To-Page-Panel`.
- [ ] Ở bản MVP0: KHÔNG dựng database — `MVP-Scope §3` hạng mục A5 = `❌` ở MVP0, *"MVP0 không có database"*; spec MVP0 tồn tại dưới dạng file YAML viết tay.

## 5. Ước lượng

| Đại lượng | Giá trị | Ghi chú |
|---|---|---|
| `E_build` | **~20 giờ-người** `[EM]` — **vượt trần 16h** | Lý do vượt trần: schema này là nền cho cả C5 và C6 cắm vào (xem mục 6) — tách nhỏ hơn sẽ để lại một schema không đủ ràng buộc để hai Story kia dùng ngay. Ghi lý do thành văn theo đúng quy tắc "vượt `E_build` ⇒ ghi lý do", không tự split. |
| `E_hitl` | **0 giờ-người/chapter** | Story này không tạo human gate; con người tương tác với spec qua `UC-03-Review-Panel-Script`, được đo ở Story khác. |

## 6. INVEST

- **I (Independent)**: ⚠️ **Vỡ.** Schema Comic IR là nơi hạng mục `MVP-Scope §3` **C5** (≤3 nhân vật/panel) và **C6** (`text_safe_zone`) cắm vào — thiếu các ràng buộc/trường đó thì hai Story kia không có chỗ để mở rộng. Lý do "không cắt được theo đường nào" (nguyên văn từ khối `[!WARNING]` của **Epic cha**, dấu (2)): *"vượt khỏi bản YAML viết tay, nó thuộc bảy Story vỡ khi cắt lô: schema Comic IR là nơi C5 (≤3 nhân vật) và C6 (text_safe_zone) cắm vào ⇒ nó không độc lập với hai Story đó, và nó không nhỏ"*. ⚠️ **Mâu thuẫn nguồn đã phát hiện**: khối `[!WARNING]` của Epic cha dẫn lý do này về `findings/business-analyst.md` §4.10, nhưng bảng §4.10 gốc **không có dòng riêng cho `Story-Comic-IR-Panel-Specification`** — đã báo cáo ở SUMMARY, không tự suy diễn thêm để lấp khoảng trống này.
- **S (Small)**: ⚠️ **Vỡ**, cùng lý do I — `E_build` vượt trần 16h (xem mục 5).
- **Ghi chú riêng cho lát YAML viết tay ở MVP0**: `INVEST không áp — Story thuộc [MVP0]`. Lý do: `MVP-Scope §3.1` và `Roadmap §3.1` ghi kỷ luật *"code của MVP0 KHÔNG phải nền của sản phẩm — viết để trả lời câu hỏi rồi bỏ, giữ lại kết luận và dữ liệu"*. Bản YAML viết tay không cần Independent (nó là một lát cắt xuyên tầng) và `Valuable` của nó là **thông tin đo được**, không phải tính năng giao cho khách. **Definition of Done của lát MVP0 = 5 tiêu chí gate G1** (`MVP-Scope §7.2`), không phải AC ở mục 4:
  - `G1-a` consistency nhân vật ≥70% panel, không cần retry `⚠️ [EM]` ngưỡng do run trước tự định nghĩa.
  - `G1-b` N ≤ 3 để VLM-select ra panel đạt.
  - `G1-c` human-reject rate sau VLM-select: ≤30% PASS / 30–50% PASS có điều kiện / >50% FAIL `⚠️ [EM]`.
  - `G1-d` panel 2 nhân vật ≥60% đạt (đúng identity và đúng attribute binding); panel 3 nhân vật đo và báo cáo, không đặt ngưỡng chặn `⚠️ [EM]`.
  - `G1-e` 100% panel có thoại dùng overlay layer, 0 panel nhờ model render chữ.
  - Dùng đúng tên **MVP0** — `Glossary.md` cấm *"phase 0"*, *"spike"*, *"PoC"*.

---

_Created by product-owner_
_Author: trisjr_
