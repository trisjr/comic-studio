---
description: Tiếp tục thực hiện một change - tạo artifact kế tiếp (Thử nghiệm)
---

Tiếp tục thực hiện một change bằng cách tạo artifact kế tiếp.

**Input**: Tùy chọn chỉ định tên change sau lệnh `/opsx-continue` (ví dụ: `/opsx-continue add-auth`). Nếu bỏ trống, kiểm tra xem có thể suy luận từ context hội thoại hay không. Nếu mơ hồ hoặc không rõ ràng, bạn BẮT BUỘC phải prompt để hiển thị các change khả dụng.

**Các bước thực hiện (Steps)**

1. **Nếu không cung cấp tên change, prompt để lựa chọn**

   Chạy lệnh `openspec list --json` để lấy danh sách các active change, sắp xếp theo thời gian chỉnh sửa mới nhất. Sau đó sử dụng **tool AskUserQuestion** để người dùng chọn change muốn tiếp tục.

   Hiển thị top 3-4 change mới chỉnh sửa gần đây nhất làm các tùy chọn, bao gồm:
   - Tên change
   - Schema (lấy từ trường `schema` nếu có, ngược lại mặc định là "spec-driven")
   - Status (ví dụ: "0/5 tasks", "complete", "no tasks")
   - Thời gian chỉnh sửa gần nhất (từ trường `lastModified`)

   Đánh dấu change mới chỉnh sửa gần đây nhất là "(Khuyến nghị)" (Recommended) vì khả năng cao đây là cái người dùng muốn tiếp tục.

   **QUAN TRỌNG**: KHÔNG được đoán hoặc tự động chọn một change. Luôn để người dùng lựa chọn.

2. **Kiểm tra trạng thái hiện tại**
   ```bash
   openspec status --change "<name>" --json
   ```
   Parse JSON để hiểu trạng thái hiện tại. Kết quả trả về bao gồm:
   - `schemaName`: Workflow schema đang được sử dụng (ví dụ: "spec-driven")
   - `artifacts`: Mảng các artifact kèm trạng thái của chúng ("done", "ready", "blocked")
   - `isComplete`: Boolean cho biết tất cả các artifact đã hoàn thành hay chưa

3. **Hành động dựa trên trạng thái (status)**:

   ---

   **Nếu tất cả các artifact đã hoàn thành (`isComplete: true`)**:
   - Chúc mừng người dùng
   - Hiển thị trạng thái cuối cùng bao gồm cả schema đã sử dụng
   - Gợi ý: "Tất cả các artifact đã được tạo! Bạn có thể bắt đầu implement change này hoặc archive nó."
   - DỪNG LẠI

   ---

   **Nếu các artifact đã sẵn sàng để tạo** (trạng thái hiển thị các artifact với `status: "ready"`):
   - Chọn artifact ĐẦU TIÊN có `status: "ready"` từ output của lệnh status
   - Lấy instructions cho nó:
     ```bash
     openspec instructions <artifact-id> --change "<name>" --json
     ```
   - Parse JSON. Các trường quan trọng là:
     - `context`: Background của dự án (đây là ràng buộc dành cho BẠN - KHÔNG đưa vào output)
     - `rules`: Các quy tắc riêng của artifact (đây là ràng buộc dành cho BẠN - KHÔNG đưa vào output)
     - `template`: Cấu trúc để sử dụng cho file output của bạn
     - `instruction`: Hướng dẫn riêng cho từng schema
     - `outputPath`: Nơi sẽ ghi artifact
     - `dependencies`: Các artifact đã hoàn thành cần đọc để lấy context
   - **Tạo file artifact**:
     - Đọc bất kỳ file dependency nào đã hoàn thành để lấy context
     - Sử dụng `template` làm cấu trúc - điền nội dung vào các phần tương ứng
     - Áp dụng `context` và `rules` làm các ràng buộc khi viết - nhưng KHÔNG copy chúng vào trong file
     - Ghi vào đường dẫn output được chỉ định trong instructions
   - Hiển thị những gì đã được tạo và những gì đã được mở khóa (unlocked)
   - DỪNG LẠI sau khi tạo xong MỘT artifact

   ---

   **Nếu không có artifact nào sẵn sàng (tất cả đều bị chặn - blocked)**:
   - Trường hợp này không nên xảy ra với một schema hợp lệ
   - Hiển thị status và gợi ý kiểm tra lại các vấn đề phát sinh

4. **Sau khi tạo artifact, hiển thị tiến độ (progress)**
   ```bash
   openspec status --change "<name>"
   ```

**Output**

Sau mỗi lần gọi, hãy hiển thị:
- Artifact nào đã được tạo
- Schema workflow đang được sử dụng
- Tiến độ hiện tại (N/M hoàn thành)
- Những artifact nào hiện đã được mở khóa
- Prompt: "Chạy `/opsx-continue` để tạo artifact tiếp theo"

**Hướng dẫn tạo Artifact (Artifact Creation Guidelines)**

Loại artifact và mục đích của chúng phụ thuộc vào từng schema. Sử dụng trường `instruction` từ output instructions để hiểu cần tạo cái gì.

Các pattern artifact phổ biến:

**spec-driven schema** (proposal → specs → design → tasks):
- **proposal.md**: Hỏi người dùng về change nếu chưa rõ ràng. Điền vào các phần: Why (Tại sao), What Changes (Những gì thay đổi), Capabilities (Các khả năng), Impact (Tác động).
  - Phần Capabilities là cực kỳ quan trọng - mỗi capability được liệt kê sẽ cần một file spec riêng.
- **specs/<capability>/spec.md**: Tạo một file spec cho mỗi capability được liệt kê trong phần Capabilities của proposal (sử dụng tên capability, không phải tên change).
- **design.md**: Tài liệu hóa các quyết định kỹ thuật, kiến trúc và cách tiếp cận implementation.
- **tasks.md**: Chia nhỏ quá trình implementation thành các task có checkbox.

Đối với các schema khác, hãy làm theo trường `instruction` từ output của CLI.

**Guardrails**

- Chỉ tạo MỘT artifact cho mỗi lần gọi
- Luôn đọc các artifact phụ thuộc (dependency artifact) trước khi tạo cái mới
- Không bao giờ nhảy cóc artifact hoặc tạo sai thứ tự
- Nếu context không rõ ràng, hãy hỏi người dùng trước khi tạo
- Xác minh file artifact đã tồn tại sau khi ghi trước khi đánh dấu tiến độ
- Sử dụng trình tự artifact của schema, đừng tự giả định tên artifact cụ thể
- **QUAN TRỌNG**: `context` và `rules` là các ràng buộc cho BẠN, không phải nội dung cho file
  - KHÔNG copy các block `<context>`, `<rules>`, `<project_context>` vào trong artifact
  - Những nội dung này hướng dẫn bạn viết, nhưng không bao giờ được xuất hiện trong output
