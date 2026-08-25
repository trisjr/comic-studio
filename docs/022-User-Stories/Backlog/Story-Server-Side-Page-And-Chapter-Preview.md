---
id: STORY-D-04
type: story
status: draft
created: 2026-08-24
---

# Story-Server-Side-Page-And-Chapter-Preview

## 1. Story

Là tác giả truyện chữ, tôi muốn **xem trang / chương thành phẩm dưới dạng ảnh composite**, để **thấy thành phẩm trước khi trả tiền**

## 2. Part of

- Epic cha: [Epic-Minimum-Editor](../Epics/Epic-Minimum-Editor.md)
- BRD: [BRD-004-Minimum-Editor](../../020-Requirements/BRD/BRD-004-Minimum-Editor.md)
- Use Case liên quan: [UC-08-Arrange-Page-And-Preview](../../020-Requirements/Use-Cases/UC-08-Arrange-Page-And-Preview.md) — đây là thành phần `#4` của UC-08

## 3. Bối cảnh & nguồn

Đây là **thành phần bắt buộc `#4`** của hàng **`D1`** ([MVP-Scope §3](../../010-Planning/MVP-Scope.md)), chiếm **3–5%** `[EM]` effort (mẫu số SaaS) — [MVP-Scope §5.2](../../010-Planning/MVP-Scope.md#52-năm-thành-phần-bắt-buộc-2025-em-mẫu-số-saas): *"Preview trang + chapter render server-side (composite PNG/PDF), read-only. Khách phải thấy thành phẩm mới trả tiền. Rẻ vì tái dùng compositor của export (H4)"*.

Anchor exit criterion: **M2-5** ([Roadmap §2](../../010-Planning/Roadmap.md#2-bảng-lộ-trình-tổng), mốc MVP2): *"export ra PDF của 1 chapter hoàn chỉnh từ preview server-side"*. [Epic-Minimum-Editor mục 5](../Epics/Epic-Minimum-Editor.md#5-definition-of-done-cấp-epic) đã ghi rõ phân công: *"Epic-D sở hữu preview; Epic-H sở hữu export. Preview Done khi compositor tái dùng được cho export — không phải hai đường render"*.

## 4. Acceptance Criteria

### Xác minh được

- [ ] Tác giả yêu cầu preview **một trang** đã có `page_layout` và panel đã sinh ảnh — hệ thống trả về **một ảnh composite PNG** thể hiện đúng vị trí panel theo `page_layout` (đo bằng: so khớp thủ công vị trí panel trong ảnh trả về với toạ độ 0–1 đã lưu)
- [ ] Tác giả yêu cầu preview **cả chapter** (nhiều trang) — hệ thống trả về composite cho **từng trang** của chapter, đúng thứ tự (đo bằng: số ảnh trả về = số trang đã có layout, thứ tự khớp `page_number`)
- [ ] Preview bao gồm **bubble/thoại đã typeset** (không phải ảnh trơn không chữ) — đo bằng: ảnh composite của trang có ít nhất 1 panel chứa thoại hiển thị được text overlay, khớp với dữ liệu bubble đã lưu
- [ ] Preview là **read-only** — không có thao tác nào trong luồng xem preview ghi thay đổi vào `page_layout` hoặc panel (đo bằng: gọi API preview nhiều lần liên tiếp, dữ liệu `page_layout`/panel trong DB không đổi)
- [ ] Compositor dùng để render preview là **cùng một compositor** dùng cho export PDF (`Story-Export-Chapter-To-PDF-CBZ-Webtoon` của Epic-Quality-And-Operations) — đo bằng: kiểm tra code path, cả hai đường gọi cùng một hàm/service render, không phải hai implementation riêng

### Đường không hạnh phúc (unhappy path)

- [ ] Yêu cầu preview một trang **chưa có đủ ảnh panel** (một số panel chưa sinh xong) — hệ thống trả về trạng thái rõ ràng (ví dụ placeholder + thông báo) thay vì lỗi 500 hoặc ảnh composite thiếu panel mà không cảnh báo (đo bằng: response phân biệt được "đang chờ" với "lỗi hệ thống")
- [ ] Yêu cầu preview một chapter **rỗng** (chưa có trang nào có layout) — hệ thống trả về thông báo rõ ràng, không crash (đo bằng: response có mã lỗi/thông điệp xác định, không phải exception không xử lý)
- [ ] Render preview thất bại giữa chừng (ví dụ timeout khi ghép nhiều trang lớn) — hệ thống không để lại file tạm rác hoặc trạng thái "đang render" treo vĩnh viễn (đo bằng: sau timeout, request preview mới vẫn chạy được, không bị khoá bởi job cũ)
- [ ] Tác giả yêu cầu preview một chapter thuộc `tenant_id` khác — request bị từ chối bởi RLS (đo bằng: response lỗi, không ảnh composite nào được trả về)

### Ràng buộc cứng không được vi phạm

- `KC-5` — truy vấn dữ liệu để render preview phải qua `tenant_id` + RLS
- — (không có `change_log` bắt buộc cho hành động **xem** preview, vì đây là thao tác read-only, không phải hành động sáng tạo — xem mục *Story này KHÔNG làm*)

### Story này KHÔNG làm

- Không **xuất file** PDF/CBZ/webtoon cho khách tải về — đó là `Story-Export-Chapter-To-PDF-CBZ-Webtoon` (Epic-Quality-And-Operations, `H4`). Story này chỉ tạo ảnh composite để **xem trong app**
- Không ghi `change_log` cho hành động xem preview — xem là read-only, không phải quyết định sáng tạo cần chứng minh provenance
- Không cho phép **sửa** nội dung ngay trong màn hình preview — sửa bubble/thoại thuộc `Story-Bubble-Text-Overlay-Editor`, sửa layout thuộc `Story-Page-Template-Layout-And-Swap-Panel`
- Không tối ưu hiệu năng render cho quy mô sản xuất lớn (đó là mối quan tâm của MVP3 pipeline, ngoài horizon)

## 5. Ước lượng

| Đại lượng | Giá trị | Ghi chú |
|---|---|---|
| `E_build` | **10h** `[EM]` | Trong trần 16h. Chủ yếu là wiring gọi compositor dùng chung (tái dùng, không viết renderer mới) + endpoint đọc `page_layout` + cache ảnh composite |
| `E_hitl` | **0h/chapter** | Không phải HITL gate — xem trước là thao tác tự chọn của tác giả, không phải bước xác nhận bắt buộc |

## 6. INVEST

- **I (Independent)**: ✅ — theo bảng §4.4 của `findings/business-analyst.md`. Phụ thuộc **dữ liệu** vào `Story-Page-Template-Layout-And-Swap-Panel` (cần `page_layout` tồn tại để render) nhưng deliverable của nó (endpoint preview) là một lát cắt riêng, khai tường minh phụ thuộc này thay vì giả định độc lập tuyệt đối (đúng diễn giải `Independent` cho đội một người theo `findings/product-owner.md` §4.1)
- **S (Small)**: ✅ — theo bảng §4.4. `E_build` 10h nằm sâu trong trần 16h nhờ tái dùng compositor của export (H4), không viết renderer từ đầu

---

_Created by product-owner_
_Author: trisjr_
