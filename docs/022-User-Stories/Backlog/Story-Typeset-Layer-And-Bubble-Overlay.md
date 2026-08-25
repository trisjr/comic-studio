---
id: STORY-A-02
type: story
status: draft
created: 2026-08-24
---

# Story-Typeset-Layer-And-Bubble-Overlay

## 1. Story

Là tác giả truyện chữ, tôi muốn thoại được render bằng overlay layer tách khỏi ảnh, để sửa một câu thoại không phải sinh lại ảnh.

## 2. Part of

- Epic cha: [Epic-Image-Generation-Pipeline](../Epics/Epic-Image-Generation-Pipeline.md)
- BRD: [BRD-001-Image-Generation-Pipeline](../../020-Requirements/BRD/BRD-001-Image-Generation-Pipeline.md)
- Use Case liên quan: [UC-07-Edit-Bubble-And-Dialogue-In-Panel](../../020-Requirements/Use-Cases/UC-07-Edit-Bubble-And-Dialogue-In-Panel.md) (tiêu thụ overlay layer này), [UC-06-Generate-Panel-And-Pick-Variant](../../020-Requirements/Use-Cases/UC-06-Generate-Panel-And-Pick-Variant.md)

## 3. Bối cảnh & nguồn

- `MVP-Scope §3` hạng mục **A2**: *"Typeset layer + bubble overlay (composite ra trang thật có thoại)"* — `🟡 thô` tại MVP0. CF-8.11c: *"nổ ngay ở panel có thoại đầu tiên, tức trong MVP0"*.
- `Roadmap` Pre-cycle 09/2026, exit criterion **G1-e** (trong `P-2`): *"100% panel có thoại được typeset bằng overlay layer; 0 panel dựa vào model render chữ trong ảnh"*. `Roadmap §4 X-c`: typeset layer phải có "ngay ở panel có thoại đầu tiên" — *"Pre-cycle 09/2026 — trong MVP0"*.
- `Glossary.md` term `typeset layer`: *"Tầng chữ tách khỏi ảnh, không nướng vào pixel. Ảnh được sinh không có chữ (`text, letters, watermark, speech bubble` vào negative prompt), bubble và thoại render bằng code lên trên."*
- ⚠️ Story thuộc nhóm 5 Story `[MVP0]` của `findings/business-analyst.md` §4.9 — **INVEST không áp** (xem mục 6).

## 4. Acceptance Criteria

### Xác minh được

- [ ] **100%** panel có thoại trong bộ dữ liệu MVP0 dùng overlay layer để hiển thị chữ — đo bằng: đếm số panel có thoại / số panel dùng overlay, tỉ lệ phải bằng 100% (`G1-e`)
- [ ] **0** panel dựa vào model render chữ trực tiếp trong ảnh — đo bằng: kiểm tra ảnh gốc (trước khi overlay) không chứa chữ đọc được nào (`G1-e`)
- [ ] Prompt sinh ảnh chứa `text, letters, watermark, speech bubble` trong negative prompt cho 100% panel có thoại — đo bằng: kiểm tra log prompt gửi tới model
- [ ] Bubble + thoại được render bằng code (không phải bằng model) trên top của ảnh — đo bằng: kiểm tra pipeline composite có bước render text riêng, tách khỏi bước gọi model sinh ảnh

### Đường không hạnh phúc (unhappy path)

- [ ] Bubble overlay che mất vùng mặt nhân vật do ảnh gốc không chừa chỗ ⇒ panel phải được đánh dấu lỗi bố cục, không được xuất bản ở trạng thái này
- [ ] Model vẫn sinh ra chữ trong ảnh dù đã có negative prompt (model không tuân negative prompt) ⇒ panel đó **không** được tính vào tử số 100% của `G1-e`, phải ghi nhận là vi phạm và loại khỏi bộ đã duyệt
- [ ] Chữ tiếng Việt có dấu chồng (ví dụ "ế", "ữ", "ượ") bị lỗi hiển thị ở tầng overlay (font không đủ glyph) ⇒ phải phát hiện được bằng kiểm tra thủ công trên từng panel, vì **không có benchmark định lượng nào** cho trường hợp này (`findings/business-analyst.md` KT-9)

### Ràng buộc cứng không được vi phạm

—

### Story này KHÔNG làm

- Không xây UI kéo-thả bubble / sửa thoại trong editor — đó thuộc `Story-Edit-Bubble-And-Dialogue-In-Panel` (Epic-Minimum-Editor); Story này chỉ là cơ chế overlay bản thô của MVP0
- Không khai báo `text_safe_zone` trong panel spec — đó thuộc `Story-Text-Safe-Zone-In-Panel-Spec` (Epic-Comic-Director-And-Layout, hạng mục C6, mốc MVP2)
- Không hỗ trợ nhiều kiểu bubble hoặc SFX/narration box — các mục này còn `TBD` chưa có nguồn quyết định (`outline.md` ghi chú lô L7: 5 điểm `TBD` trong UC-07, writer *"từ chối tự thiết kế thêm"*)
- Không tối ưu font rendering cho ngôn ngữ khác ngoài tiếng Việt

## 5. Ước lượng

| Đại lượng | Giá trị | Ghi chú |
|---|---|---|
| `E_build` | ~8 giờ-người `[EM]` | Bản thô MVP0 (composite ảnh + text render đơn giản), một phần nhỏ hơn trong tổng 1–2 tuần của MVP0 (CF-8.4). Trong trần 16h, nhưng con số là ước lượng, không phải số đo |
| `E_hitl` | `TBD` | Việc kiểm tra "100% panel dùng overlay, 0 panel model render chữ" (`G1-e`) là kiểm tra một lần cho MVP0, chưa phải nghĩa vụ vận hành lặp lại theo chapter |

## 6. INVEST

`INVEST không áp — Story thuộc [MVP0]`. Lý do giống `Story-Generate-Panel-With-Reference-And-VLM-Select`: `MVP-Scope §3.1` + `Roadmap §3.1` — code MVP0 là lát cắt mua thông tin, không phải nền sản phẩm.

**Definition of Done — 5 tiêu chí gate G1** (`MVP-Scope §7.2`):

- [ ] `G1-a` Consistency nhân vật ≥70% — **thuộc `Story-Generate-Panel-With-Reference-And-VLM-Select`, không thuộc Story này**
- [ ] `G1-b` N tối thiểu ≤3 — **thuộc Story kia**
- [ ] `G1-c` `reject_rate` có số và verdict phân loại đúng dải — **thuộc Story kia**
- [ ] `G1-d` Panel 2–3 nhân vật — **thuộc Story kia**
- [ ] `G1-e` 100% panel có thoại dùng overlay, 0 panel nhờ model render chữ — **Story này sở hữu**, xem AC-1. Đây cũng là điều kiện ra `P-2` của Roadmap Pre-cycle và exit criterion `X-c`.

⛔ Dùng đúng tên **MVP0** — `Glossary.md` cấm *"phase 0"*, *"spike"*, *"PoC"* (CẤM-11).

---

_Created by product-owner_
_Author: trisjr_
