---
id: STORY-D-03
type: story
status: draft
created: 2026-08-24
---

# Story-Page-Template-Layout-And-Swap-Panel

## 1. Story

Là tác giả truyện chữ, tôi muốn **chọn template trang và đổi chỗ panel giữa các ô**, để **quyết định sắp đặt là của tôi** (*selection & arrangement*)

## 2. Part of

- Epic cha: [Epic-Minimum-Editor](../Epics/Epic-Minimum-Editor.md)
- BRD: [BRD-004-Minimum-Editor](../../020-Requirements/BRD/BRD-004-Minimum-Editor.md)
- Use Case liên quan: [UC-08-Arrange-Page-And-Preview](../../020-Requirements/Use-Cases/UC-08-Arrange-Page-And-Preview.md) — đây là thành phần `#3` của UC-08

## 3. Bối cảnh & nguồn

Đây là **thành phần bắt buộc `#3`**, chiếm **3–4%** `[EM]` effort (mẫu số SaaS) — [MVP-Scope §5.2](../../010-Planning/MVP-Scope.md#52-năm-thành-phần-bắt-buộc-2025-em-mẫu-số-saas), hàng `D1`/`C3` của [MVP-Scope §3](../../010-Planning/MVP-Scope.md). Layout phải lưu dưới dạng **toạ độ chuẩn hoá 0–1** trong `page_layout JSONB` ngay từ MVP — [MVP-Scope §4.1](../../010-Planning/MVP-Scope.md#41-canvas-editor-14--cắt-một-phần-cf-91): *"template chỉ là preset ghi vào cùng schema"*, để đường nâng cấp lên canvas thật về sau **không phải migrate dữ liệu** và **không viết renderer từ đầu**.

Không có exit criterion `M2-x` được đánh số riêng **cho tên thành phần này** trong bảng exit criteria chi tiết của [Roadmap §2](../../010-Planning/Roadmap.md#2-bảng-lộ-trình-tổng) (M2-1…M2-6 đều nói về Director tự động, giới hạn nhân vật, `text_safe_zone`, human gate, export, safe harbour). **Ghi nhận khoảng trống này tường minh, không bịa số**: cột *Deliverable* của hàng mốc MVP2 trong cùng bảng đó liệt kê nguyên văn *"Template layout + swap panel"* như một phần sản phẩm phải giao ở MVP2.

Anchor exit criterion dùng cho Story này (suy luận của PO, cùng khuôn mà [Epic-Minimum-Editor mục 5](../Epics/Epic-Minimum-Editor.md#5-definition-of-done-cấp-epic) đã dùng để gắn Story Bible editor vào `M1-3`): **M2-5** — *"export ra PDF của 1 chapter hoàn chỉnh từ preview server-side"*. Layout/swap panel là **input bắt buộc** của preview: không có `page_layout` đã được sắp đặt thì preview server-side không có gì để ghép thành composite, nên M2-5 không đạt được nếu thành phần `#3` chưa chạy. Đây là suy luận của PO, không phải phát biểu trực tiếp của nguồn.

## 4. Acceptance Criteria

### Xác minh được

- [ ] Tác giả chọn một **template layout** có sẵn cho một trang (ví dụ lưới 4 ô, lưới 6 ô) — đo bằng: sau khi chọn, `page_layout` của trang trong DB chứa toạ độ 0–1 khớp đúng template đã chọn
- [ ] Tác giả **đổi chỗ (swap)** hai panel giữa hai ô của cùng một trang — đo bằng: `GET` lại `page_layout`, vị trí của hai panel đã hoán đổi đúng, các panel khác không đổi
- [ ] Tác giả **reorder** thứ tự đọc của các panel trong trang (khi thứ tự đọc khác thứ tự vị trí hình học) — đo bằng: field thứ tự đọc (`reading_order`) trả về đúng dãy số sau khi sắp lại
- [ ] Toạ độ lưu trong `page_layout JSONB` là **số thực trong khoảng [0, 1]** cho mọi panel — đo bằng: validate schema, giá trị ngoài [0,1] bị từ chối khi ghi
- [ ] Mỗi lần chọn template hoặc swap panel sinh **đúng một** `change_log` row (đo bằng: query `change_log` sau hành động trả về đúng 1 row mới, khớp `Story-Change-Log-On-Every-Editor-Action`)

### Đường không hạnh phúc (unhappy path)

- [ ] Tác giả cố swap một panel vào một ô đã có panel khác trong cùng thao tác — hệ thống phải hoán đổi cả hai (swap thật), không được để một panel biến mất khỏi trang (đo bằng: sau swap, tổng số panel trên trang không đổi)
- [ ] Tác giả chọn một template có **số ô ít hơn** số panel hiện có trên trang — hệ thống từ chối áp template đó và báo lỗi rõ ràng, không tự động xoá panel dư ra (đo bằng: request áp template bị từ chối, `page_layout` giữ nguyên trạng thái trước đó)
- [ ] Hai request swap panel gửi gần như đồng thời trên cùng một trang (race condition) — trạng thái cuối cùng phải nhất quán với **một trong hai** thứ tự thao tác, không được sinh ra layout không hợp lệ (đo bằng: sau hai request đồng thời, `page_layout` vẫn validate schema hợp lệ và có đúng 2 `change_log` row tương ứng)
- [ ] Tác giả thao tác trên trang thuộc `tenant_id` khác — request bị từ chối bởi RLS (đo bằng: response lỗi, `page_layout` ở tenant gốc không đổi)

### Ràng buộc cứng không được vi phạm

- `KC-2` — mọi hành động chọn template/swap/reorder sinh `change_log` row
- `KC-5` — thao tác qua `tenant_id` + RLS

### Story này KHÔNG làm

- Không cho phép **hình học panel tự do** (kéo cạnh, xoay, panel không chữ nhật) — đó là `D6`/hạng mục hoãn (infinite canvas), không mở trong Story này
- Không tự động **gợi ý** template dựa trên nội dung scene — đó thuộc phạm vi Director tự động (Epic-C), Story này chỉ nhận template do Director hoặc tác giả chọn
- Không viết renderer canvas từ đầu — chỉ ghi/đọc toạ độ chuẩn hoá vào `page_layout JSONB` theo đúng ràng buộc [MVP-Scope §4.1](../../010-Planning/MVP-Scope.md#41-canvas-editor-14--cắt-một-phần-cf-91)
- Không thực hiện việc **render ảnh composite** của trang — đó là `Story-Server-Side-Page-And-Chapter-Preview`

## 5. Ước lượng

| Đại lượng | Giá trị | Ghi chú |
|---|---|---|
| `E_build` | **12h** `[EM]` | Trong trần 16h. UI chọn template rời rạc + thao tác swap/reorder trên toạ độ chuẩn hoá, không cần hình học liên tục |
| `E_hitl` | **0h/chapter** | Không phải HITL gate — đây là thao tác sáng tạo tuỳ chọn của tác giả, không phải bước xác nhận bắt buộc trước khi xuất bản |

## 6. INVEST

- **I (Independent)**: ✅ — theo bảng §4.4 của `findings/business-analyst.md`. Deliverable độc lập với 4 Story còn lại của Epic-D (dùng chung schema `page_layout JSONB` nhưng không cần Story khác hoàn thành trước để tự nó hoạt động, ngoại trừ ràng buộc chung `Story-Change-Log-On-Every-Editor-Action` đã khai ở AC-1)
- **S (Small)**: ✅ — theo bảng §4.4. `E_build` 12h nằm trong trần 16h; phạm vi giới hạn ở thao tác rời rạc trên toạ độ, không phải hình học tự do

---

_Created by product-owner_
_Author: trisjr_
