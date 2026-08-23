---
description: Archive một completed change trong workflow thử nghiệm
---

Archive một completed change trong workflow thử nghiệm.

**Input**: Tùy chọn chỉ định tên change sau lệnh `/opsx-archive` (ví dụ: `/opsx-archive add-auth`). Nếu bỏ trống, kiểm tra xem có thể suy luận từ context hội thoại không. Nếu mơ hồ hoặc không rõ ràng, bạn BẮT BUỘC phải prompt để hiển thị các change khả dụng.

**Các bước thực hiện (Steps)**

1. **Nếu không cung cấp tên change, prompt để lựa chọn**

   Chạy lệnh `openspec list --json` để lấy danh sách các change khả dụng. Sử dụng **tool AskUserQuestion** để người dùng chọn.

   Chỉ hiển thị các change đang hoạt động (chưa được archive).
   Bao gồm thông tin schema được sử dụng cho mỗi change nếu có.

   **QUAN TRỌNG**: KHÔNG được đoán hoặc tự động chọn một change. Luôn để người dùng lựa chọn.

2. **Kiểm tra trạng thái hoàn thiện của artifact**

   Chạy lệnh `openspec status --change "<name>" --json` để kiểm tra mức độ hoàn thiện của artifact.

   Parse JSON để hiểu:
   - `schemaName`: Workflow đang được sử dụng
   - `artifacts`: Danh sách các artifact kèm trạng thái của chúng (`done` hoặc khác)

   **Nếu bất kỳ artifact nào chưa ở trạng thái `done`:**
   - Hiển thị cảnh báo liệt kê các artifact chưa hoàn thiện
   - Prompt người dùng xác nhận để tiếp tục
   - Chỉ tiếp tục nếu người dùng xác nhận

3. **Kiểm tra trạng thái hoàn thành của task**

   Đọc file tasks (thường là `tasks.md`) để kiểm tra các task chưa hoàn thành.

   Đếm số task được đánh dấu `- [ ]` (chưa xong) so với `- [x]` (đã xong).

   **Nếu tìm thấy các task chưa hoàn thành:**
   - Hiển thị cảnh báo cho biết số lượng task chưa hoàn thành
   - Prompt người dùng xác nhận để tiếp tục
   - Chỉ tiếp tục nếu người dùng xác nhận

   **Nếu không có file tasks:** Tiếp tục mà không cần cảnh báo liên quan đến task.

4. **Đánh giá trạng thái sync của delta spec**

   Kiểm tra các delta spec tại `openspec/changes/<name>/specs/`. Nếu không tồn tại, tiếp tục mà không cần prompt sync.

   **Nếu tồn tại delta spec:**
   - So sánh từng delta spec với main spec tương ứng tại `openspec/specs/<capability>/spec.md`
   - Xác định những thay đổi sẽ được áp dụng (thêm mới, chỉnh sửa, xóa, đổi tên)
   - Hiển thị bảng tổng hợp các thay đổi trước khi prompt

   **Các tùy chọn prompt:**
   - Nếu cần thay đổi: "Sync ngay bây giờ (khuyến nghị)", "Archive mà không sync"
   - Nếu đã sync: "Archive ngay", "Vẫn sync lại", "Hủy bỏ"

   Nếu người dùng chọn sync, thực hiện logic của `/opsx-sync`. Tiếp tục archive bất kể lựa chọn là gì.

5. **Thực hiện Archive**

   Tạo thư mục archive nếu chưa tồn tại:
   ```bash
   mkdir -p openspec/changes/archive
   ```

   Tạo tên mục tiêu sử dụng ngày hiện tại: `YYYY-MM-DD-<change-name>`

   **Kiểm tra xem mục tiêu đã tồn tại chưa:**
   - Nếu có: Báo lỗi, gợi ý đổi tên archive hiện tại hoặc sử dụng ngày khác
   - Nếu không: Di chuyển thư mục change vào archive

   ```bash
   mv openspec/changes/<name> openspec/changes/archive/YYYY-MM-DD-<name>
   ```

6. **Hiển thị tổng kết (Summary)**

   Hiển thị thông tin tổng kết sau khi hoàn tất archive bao gồm:
   - Tên change
   - Schema đã sử dụng
   - Vị trí lưu trữ archive
   - Trạng thái sync spec (đã sync / bỏ qua sync / không có delta spec)
   - Ghi chú về các cảnh báo (artifact hoặc task chưa hoàn thiện)

**Output khi thành công**

```
## Archive Hoàn Tất

**Change:** <change-name>
**Schema:** <schema-name>
**Đã archive tại:** openspec/changes/archive/YYYY-MM-DD-<name>/
**Specs:** ✓ Đã sync với main specs

Tất cả artifact đã xong. Tất cả task đã xong.
```

**Output khi thành công (Không có Delta Spec)**

```
## Archive Hoàn Tất

**Change:** <change-name>
**Schema:** <schema-name>
**Đã archive tại:** openspec/changes/archive/YYYY-MM-DD-<name>/
**Specs:** Không có delta spec

Tất cả artifact đã xong. Tất cả task đã xong.
```

**Output khi thành công kèm Cảnh báo**

```
## Archive Hoàn Tất (kèm cảnh báo)

**Change:** <change-name>
**Schema:** <schema-name>
**Đã archive tại:** openspec/changes/archive/YYYY-MM-DD-<name>/
**Specs:** Đã bỏ qua sync (người dùng chọn bỏ qua)

**Cảnh báo:**
- Đã archive với 2 artifact chưa hoàn thiện
- Đã archive với 3 task chưa hoàn thiện
- Việc sync delta spec đã bị bỏ qua (người dùng chọn bỏ qua)

Hãy xem lại archive nếu hành động này không phải chủ ý của bạn.
```

**Output khi lỗi (Archive đã tồn tại)**

```
## Archive Thất Bại

**Change:** <change-name>
**Mục tiêu:** openspec/changes/archive/YYYY-MM-DD-<name>/

Thư mục archive đích đã tồn tại.

**Các tùy chọn:**
1. Đổi tên archive hiện có
2. Xóa archive hiện có nếu đó là bản trùng lặp
3. Chờ đến ngày khác để thực hiện archive
```

**Guardrails**

- Luôn prompt để chọn change nếu chưa được cung cấp
- Sử dụng artifact graph (`openspec status --json`) để kiểm tra mức độ hoàn thiện
- Không chặn việc archive khi có cảnh báo - chỉ thông báo và yêu cầu xác nhận
- Bảo toàn file `.openspec.yaml` khi di chuyển vào archive (nó sẽ di chuyển cùng thư mục)
- Hiển thị tổng kết rõ ràng về những gì đã diễn ra
- Nếu yêu cầu sync, hãy sử dụng phương pháp `/opsx-sync` (do agent điều khiển)
- Nếu tồn tại delta spec, luôn chạy đánh giá sync và hiển thị bảng tổng hợp trước khi prompt
