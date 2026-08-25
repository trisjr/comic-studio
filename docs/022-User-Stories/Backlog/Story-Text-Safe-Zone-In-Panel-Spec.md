---
id: STORY-C-05
type: story
status: draft
created: 2026-08-24
---

# Story-Text-Safe-Zone-In-Panel-Spec

## 1. Story

Là tác giả truyện chữ, tôi muốn **panel spec chừa sẵn vùng đặt bubble**, để **bubble không che mặt nhân vật và tôi không phải sinh lại ảnh**.

## 2. Part of

- Epic cha: [Epic-Comic-Director-And-Layout](../Epics/Epic-Comic-Director-And-Layout.md)
- BRD cha: [BRD-003-Comic-Director-And-Layout](../../020-Requirements/BRD/BRD-003-Comic-Director-And-Layout.md)
- UC liên quan: [UC-08-Arrange-Page-And-Preview](../../020-Requirements/Use-Cases/UC-08-Arrange-Page-And-Preview.md)

## 3. Bối cảnh & nguồn

- `MVP-Scope.md` §3 hạng mục **C6** — *"`text_safe_zone` trong panel spec"*: `⛔` ở MVP0 và MVP1, `✅` từ MVP2. Căn cứ: CF-8.8.
- `Roadmap.md` mốc **MVP2**, exit criterion **M2-3**: *"`text_safe_zone` có trong panel spec và typeset không đè vùng mặt ở ≥95% panel"*. ⚠️ Ngưỡng **95% là `[EM]` do `Roadmap` TỰ ĐỊNH NGHĨA** (CF-10.5) — cấm trích như số đo hoặc benchmark ngành.
- `text_safe_zone` (`Glossary.md`): vùng trong panel được giữ trống để đặt bubble, khai báo ngay trong `Panel Specification`. Thiếu nó thì bubble che mặt nhân vật và phải sinh lại toàn bộ ảnh đã làm.
- `Roadmap.md` §3.3 mục *"Nội dung theo CF-8.8"* điều chỉnh #3: *"Thêm `text_safe_zone` vào panel spec — bubble che mặt là lỗi không thể tự động tránh nếu spec không chừa chỗ"*.

## 4. Acceptance Criteria

### Xác minh được

- [ ] Mỗi panel spec do Director sinh ra (từ MVP2) có trường `text_safe_zone` mô tả ≥1 vùng toạ độ chuẩn hoá (0–1) không được đặt nhân vật/chi tiết quan trọng — đo bằng: 100% panel spec có trường `text_safe_zone` không rỗng.
- [ ] Với panel có thoại, bubble được typeset (qua `Story-Typeset-Layer-And-Bubble-Overlay` của Epic-A) nằm trong vùng `text_safe_zone` đã khai báo, không đè lên vùng mặt nhân vật — đo bằng: chạy typeset trên tập panel test có thoại, đếm tỉ lệ panel không đè vùng mặt ≥95% (`M2-3`, ⚠️ `[EM]`).
- [ ] `text_safe_zone` được tính toán dựa trên bố cục thực tế của panel (vị trí nhân vật, camera), không phải một vùng cố định giống nhau cho mọi panel — đo bằng: so sánh `text_safe_zone` của 2 panel có bố cục khác nhau, toạ độ khác nhau tương ứng.

### Đường không hạnh phúc (unhappy path)

- [ ] Panel có nhân vật chiếm gần toàn bộ khung hình (không còn vùng trống hợp lý): hệ thống phải trả về `text_safe_zone` rỗng hoặc tối thiểu kèm cảnh báo, không được ép một vùng đè lên nhân vật để "cho có" — đo bằng: test panel full-body close-up, kiểm tra `text_safe_zone` không chồng lên vùng nhân vật đã khai báo.
- [ ] Panel không có thoại (`dialogue` rỗng): `text_safe_zone` vẫn được tính (để dự phòng chỉnh sửa thêm thoại sau), nhưng không bắt buộc phải tồn tại bubble — đo bằng: test panel không thoại, kiểm tra spec vẫn hợp lệ dù không có bubble render.

### Ràng buộc cứng không được vi phạm

- —

### Story này KHÔNG làm

- [ ] KHÔNG tự render hay đặt bubble — đó là `Story-Typeset-Layer-And-Bubble-Overlay` (Epic-A); Story này chỉ khai báo vùng an toàn trong spec.
- [ ] KHÔNG cung cấp UI cho người dùng kéo/chỉnh `text_safe_zone` bằng tay — đó là Epic-Minimum-Editor (thành phần #2 bubble/text editor).
- [ ] KHÔNG tự động re-generate ảnh nếu bubble đè mặt — mục tiêu của Story này là **tránh** tình huống đó ngay từ spec, không phải cơ chế khắc phục sau khi đã xảy ra.

## 5. Ước lượng

| Đại lượng | Giá trị | Ghi chú |
|---|---|---|
| `E_build` | **~12 giờ-người** `[EM]` | Tính toán vùng an toàn dựa trên bố cục nhân vật là logic hình học có độ phức tạp vừa phải — dưới trần 16h. |
| `E_hitl` | **0 giờ-người/chapter** | Không tạo human gate; kiểm chứng ngưỡng 95% (`M2-3`) là việc đo tự động, không phải review thủ công mỗi chapter. |

## 6. INVEST

- **I (Independent)**: ✅ Mở rộng schema Comic IR bằng một trường độc lập với `C5` (ràng buộc số nhân vật) và rubric (`C3`); tiêu thụ bởi Story typeset của Epic-A nhưng không phụ thuộc ngược lại.
- **S (Small)**: ✅ Phạm vi là tính toán + khai báo một trường dữ liệu, nằm trong trần 16 giờ-người.

---

_Created by product-owner_
_Author: trisjr_
