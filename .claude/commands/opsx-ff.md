---
description: Tạo một change và tạo tất cả các artifact cần thiết cho implementation trong một lần
---

Fast-forward quá trình tạo artifact - tạo mọi thứ cần thiết để bắt đầu implementation.

**Input**: Đối số sau `/opsx-ff` là tên change (dạng kebab-case), HOẶC một mô tả về những gì người dùng muốn xây dựng.

**Các bước thực hiện (Steps)**

1. **Nếu không có input nào được cung cấp, hãy hỏi người dùng muốn xây dựng cái gì**

   Sử dụng **tool AskUserQuestion** (dạng câu hỏi mở, không có tùy chọn sẵn) để hỏi:
   > "Bạn muốn thực hiện change nào? Hãy mô tả những gì bạn muốn xây dựng hoặc sửa chữa."

   Từ mô tả của họ, suy ra một tên ở dạng kebab-case (ví dụ: "add user authentication" → `add-user-auth`).

   **QUAN TRỌNG**: KHÔNG được tiếp tục nếu chưa hiểu người dùng muốn xây dựng cái gì.

2. **Tạo thư mục change**
   ```bash
   openspec new change "<name>"
   ```
   Lệnh này tạo một scaffold change tại `openspec/changes/<name>/`.

3. **Lấy thứ tự xây dựng (build order) của artifact**
   ```bash
   openspec status --change "<name>" --json
   ```
   Parse JSON để lấy:
   - `applyRequires`: mảng các artifact ID cần thiết trước khi implementation (ví dụ: `["tasks"]`)
   - `artifacts`: danh sách tất cả các artifact cùng với status và dependency của chúng

4. **Tạo các artifact theo trình tự cho đến khi sẵn sàng để apply (apply-ready)**

   Sử dụng **tool TodoWrite** để theo dõi tiến độ qua các artifact.

   Vòng lặp qua các artifact theo thứ tự phụ thuộc (các artifact không có dependency chờ xử lý sẽ được làm trước):

   a. **Với mỗi artifact có trạng thái `ready` (các dependency đã được thỏa mãn)**:
      - Lấy instructions:
        ```bash
        openspec instructions <artifact-id> --change "<name>" --json
        ```
      - JSON instructions bao gồm:
        - `context`: Background của dự án (đây là ràng buộc cho BẠN - KHÔNG đưa vào output)
        - `rules`: Các quy tắc riêng của từng artifact (đây là ràng buộc cho BẠN - KHÔNG đưa vào output)
        - `template`: Cấu trúc sử dụng cho file output của bạn
        - `instruction`: Hướng dẫn riêng cho loại artifact này trong schema
        - `outputPath`: Nơi ghi hồ sơ artifact
        - `dependencies`: Các artifact đã hoàn thành cần đọc để lấy context
      - Đọc bất kỳ file dependency nào đã xong để lấy context
      - Tạo file artifact sử dụng `template` làm cấu trúc
      - Áp dụng `context` và `rules` làm các ràng buộc - nhưng KHÔNG copy chúng vào trong file
      - Hiển thị tiến độ ngắn gọn: "✓ Đã tạo <artifact-id>"

   b. **Tiếp tục cho đến khi tất cả các artifact trong `applyRequires` hoàn tất**
      - Sau khi tạo mỗi artifact, chạy lại lệnh `openspec status --change "<name>" --json`
      - Kiểm tra xem mọi artifact ID trong `applyRequires` đã có `status: "done"` trong mảng artifacts chưa
      - Dừng lại khi tất cả các artifact trong `applyRequires` đã xong

   c. **Nếu một artifact yêu cầu người dùng cung cấp thêm thông tin** (context không rõ ràng):
      - Sử dụng **tool AskUserQuestion** để làm rõ
      - Sau đó tiếp tục quá trình tạo

5. **Hiển thị status cuối cùng**
   ```bash
   openspec status --change "<name>"
   ```

**Output**

Sau khi hoàn thành tất cả các artifact, hãy tóm tắt:
- Tên change và vị trí lưu trữ
- Danh sách các artifact đã tạo kèm mô tả ngắn gọn
- Trạng thái sẵn sàng: "Tất cả artifact đã được tạo! Sẵn sàng cho implementation."
- Prompt: "Chạy `/opsx-apply` để bắt đầu implementation."

**Hướng dẫn tạo Artifact (Artifact Creation Guidelines)**

- Tuân theo trường `instruction` từ `openspec instructions` cho từng loại artifact
- Schema định nghĩa nội dung cho mỗi artifact - hãy làm theo đó
- Đọc các artifact phụ thuộc để lấy context trước khi tạo cái mới
- Sử dụng `template` làm điểm bắt đầu, điền nội dung dựa trên context

**Guardrails**

- Tạo TẤT CẢ các artifact cần thiết cho implementation (được định nghĩa trong `apply.requires` của schema)
- Luôn đọc các artifact phụ thuộc trước khi tạo cái mới
- Nếu context cực kỳ không rõ ràng, hãy hỏi người dùng - nhưng ưu tiên đưa ra các quyết định hợp lý để giữ đà tiến độ (momentum)
- Nếu một change với tên đó đã tồn tại, hãy hỏi người dùng muốn tiếp tục nó hay tạo một cái mới
- Xác minh từng file artifact tồn tại sau khi ghi trước khi tiến hành bước tiếp theo
