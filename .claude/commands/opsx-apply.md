---
description: Thực thi các task từ một OpenSpec change (Thử nghiệm)
---

Thực thi các task từ một OpenSpec change.

**Input**: Tùy chọn chỉ định tên change (ví dụ: `/opsx-apply add-auth`). Nếu bỏ trống, kiểm tra xem có thể suy luận từ context hội thoại hay không. Nếu mơ hồ hoặc không rõ ràng, bạn BẮT BUỘC phải prompt để hiển thị các change có sẵn.

**Các bước thực hiện (Steps)**

1. **Chọn change**

   Nếu tên change được cung cấp, hãy sử dụng nó. Ngược lại:
   - Suy luận từ context hội thoại nếu người dùng đã đề cập đến một change
   - Tự động chọn nếu chỉ có duy nhất một change đang hoạt động (active change)
   - Nếu mơ hồ, chạy lệnh `openspec list --json` để lấy danh sách các change khả dụng và sử dụng **tool AskUserQuestion** để người dùng lựa chọn

   Luôn thông báo: "Đang sử dụng change: <name>" và cách để ghi đè (ví dụ: `/opsx-apply <other>`).

2. **Kiểm tra status để hiểu schema**
   ```bash
   openspec status --change "<name>" --json
   ```
   Parse JSON để hiểu:
   - `schemaName`: Workflow đang được sử dụng (ví dụ: "spec-driven")
   - Artifact nào chứa các task (thường là "tasks" đối với spec-driven, kiểm tra status đối với các loại khác)

3. **Lấy instructions để apply**

   ```bash
   openspec instructions apply --change "<name>" --json
   ```

   Lệnh này trả về:
   - Đường dẫn các context file (thay đổi tùy theo schema)
   - Progress (tổng số, đã hoàn thành, còn lại)
   - Danh sách task kèm theo status
   - Dynamic instruction dựa trên trạng thái hiện tại

   **Xử lý các trạng thái (states):**
   - Nếu `state: "blocked"` (thiếu artifact): hiển thị thông tin, gợi ý sử dụng `/opsx-continue`
   - Nếu `state: "all_done"`: chúc mừng người dùng, gợi ý archive
   - Ngược lại: tiến hành implementation

4. **Đọc các context file**

   Đọc các file được liệt kê trong `contextFiles` từ output của instructions apply.
   Các file phụ thuộc vào schema đang được sử dụng:
   - **spec-driven**: proposal, specs, design, tasks
   - Các schema khác: làm theo `contextFiles` từ output của CLI

5. **Hiển thị progress hiện tại**

   Hiển thị:
   - Schema đang được sử dụng
   - Progress: "N/M task đã hoàn thành"
   - Tổng quan về các task còn lại
   - Dynamic instruction từ CLI

6. **Thực thi tasks (vòng lặp cho đến khi hoàn thành hoặc bị chặn)**

   Đối với mỗi task còn trống (pending task):
   - Hiển thị task đang được thực hiện
   - Thực hiện các thay đổi code cần thiết
   - Giữ các thay đổi ở mức tối giản và tập trung (focused)
   - Đánh dấu task đã hoàn thành trong tasks file: `- [ ]` → `- [x]`
   - Tiếp tục sang task kế tiếp

   **Tạm dừng (Pause) nếu:**
   - Task không rõ ràng → yêu cầu làm rõ (clarification)
   - Quá trình implementation phát hiện vấn đề về design → gợi ý cập nhật artifact
   - Gặp lỗi hoặc rào cản (blocker) → báo cáo và chờ hướng dẫn
   - Người dùng ngắt quãng

7. **Khi hoàn thành hoặc tạm dừng, hiển thị status**

   Hiển thị:
   - Các task đã hoàn thành trong session này
   - Progress tổng thể: "N/M task đã hoàn thành"
   - Nếu tất cả đã xong: gợi ý archive
   - Nếu bị tạm dừng: giải thích lý do và chờ hướng dẫn

**Output trong quá trình Implementation**

```
## Đang thực hiện: <change-name> (schema: <schema-name>)

Đang xử lý task 3/7: <task description>
[...quá trình implementation đang diễn ra...]
✓ Task hoàn thành

Đang xử lý task 4/7: <task description>
[...quá trình implementation đang diễn ra...]
✓ Task hoàn thành
```

**Output khi hoàn thành**

```
## Implementation Hoàn Tất

**Change:** <change-name>
**Schema:** <schema-name>
**Progress:** 7/7 task đã hoàn thành ✓

### Đã hoàn thành trong Session này
- [x] Task 1
- [x] Task 2
...

Tất cả nhiệm vụ đã hoàn thành! Sẵn sàng để archive change này.
```

**Output khi tạm dừng (Gặp vấn đề)**

```
## Tạm dừng Implementation

**Change:** <change-name>
**Schema:** <schema-name>
**Progress:** 4/7 task đã hoàn thành

### Vấn đề gặp phải
<mô tả vấn đề>

**Các tùy chọn:**
1. <tùy chọn 1>
2. <tùy chọn 2>
3. Cách tiếp cận khác

Bạn muốn thực hiện điều gì tiếp theo?
```

**Guardrails**

- Tiếp tục thực hiện các task cho đến khi hoàn thành hoặc bị chặn (blocked)
- Luôn đọc các context file trước khi bắt đầu (từ output của instructions apply)
- Nếu task mơ hồ, hãy tạm dừng và hỏi trước khi thực thi
- Nếu implementation phát hiện vấn đề, hãy tạm dừng và gợi ý cập nhật artifact
- Giữ các thay đổi code tối giản và nằm trong phạm vi của từng task
- Cập nhật checkbox của task ngay sau khi hoàn thành từng task
- Tạm dừng khi gặp lỗi, rào cản hoặc yêu cầu không rõ ràng - không được đoán
- Sử dụng `contextFiles` từ output của CLI, không tự ý giả định tên file cụ thể

**Tích hợp Workflow linh hoạt (Fluid Workflow Integration)**

Skill này hỗ trợ mô hình "actions trên một change":

- **Có thể gọi bất cứ lúc nào**: Trước khi tất cả artifact hoàn thành (nếu đã có task), sau khi thực thi một phần, xen kẽ với các hành động khác
- **Cho phép cập nhật artifact**: Nếu implementation phát hiện vấn đề về design, hãy gợi ý cập nhật artifact - không bị khóa cứng vào từng giai đoạn, hãy làm việc một cách linh hoạt
