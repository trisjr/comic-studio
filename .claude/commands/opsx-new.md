---
description: Bắt đầu một change mới sử dụng experimental artifact workflow (OPSX)
---

Bắt đầu một change mới sử dụng phương pháp artifact-driven thử nghiệm.

**Input**: Đối số sau `/opsx-new` là tên change (dạng kebab-case), HOẶC một mô tả về những gì người dùng muốn xây dựng.

**Các bước thực hiện (Steps)**

1. **Nếu không có input nào được cung cấp, hãy hỏi người dùng muốn xây dựng cái gì**

   Sử dụng **tool AskUserQuestion** (dạng câu hỏi mở, không có tùy chọn sẵn) để hỏi:
   > "Bạn muốn thực hiện change nào? Hãy mô tả những gì bạn muốn xây dựng hoặc sửa chữa."

   Từ mô tả của họ, suy ra một tên ở dạng kebab-case (ví dụ: "add user authentication" → `add-user-auth`).

   **QUAN TRỌNG**: KHÔNG được tiếp tục nếu chưa hiểu người dùng muốn xây dựng cái gì.

2. **Xác định workflow schema**

   Sử dụng schema mặc định (bỏ qua `--schema`) trừ khi người dùng yêu cầu rõ ràng một workflow khác.

   **Chỉ sử dụng một schema khác nếu người dùng đề cập đến:**
   - Một tên schema cụ thể → sử dụng `--schema <name>`
   - "hiển thị các workflow" hoặc "có những workflow nào" → chạy lệnh `openspec schemas --json` và để họ chọn

   **Nếu không**: Bỏ qua `--schema` để sử dụng mặc định.

3. **Tạo thư mục change**
   ```bash
   openspec new change "<name>"
   ```
   Thêm `--schema <name>` chỉ khi người dùng yêu cầu một workflow cụ thể.
   Lệnh này tạo một scaffold change tại `openspec/changes/<name>/` với schema đã chọn.

4. **Hiển thị trạng thái (status) của artifact**
   ```bash
   openspec status --change "<name>"
   ```
   Lệnh này cho thấy những artifact nào cần được tạo và những cái nào đã sẵn sàng (các dependency đã được thỏa mãn).

5. **Lấy instructions cho artifact đầu tiên**
   Artifact đầu tiên phụ thuộc vào schema. Kiểm tra output của lệnh status để tìm artifact đầu tiên có status "ready".
   ```bash
   openspec instructions <first-artifact-id> --change "<name>"
   ```
   Lệnh này hiển thị template và context để tạo artifact đầu tiên.

6. **DỪNG LẠI và chờ chỉ thị từ người dùng**

**Output**

Sau khi hoàn thành các bước, hãy tóm tắt:
- Tên change và vị trí lưu trữ
- Schema/workflow đang được sử dụng và trình tự artifact của nó
- Trạng thái hiện tại (0/N artifact đã hoàn thành)
- Template cho artifact đầu tiên
- Prompt: "Sẵn sàng để tạo artifact đầu tiên chưa? Chạy `/opsx-continue` hoặc chỉ cần mô tả change này nói về điều gì và tôi sẽ soạn thảo (draft) nó."

**Guardrails**

- KHÔNG tạo bất kỳ artifact nào vào lúc này - chỉ hiển thị instructions
- KHÔNG tiến xa hơn bước hiển thị template cho artifact đầu tiên
- Nếu tên không hợp lệ (không phải dạng kebab-case), hãy yêu cầu một tên hợp lệ
- Nếu một change với tên đó đã tồn tại, hãy gợi ý sử dụng `/opsx-continue` thay thế
- Truyền `--schema` nếu sử dụng một workflow không phải mặc định
