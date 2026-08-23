---
description: Verify implementation matches change artifacts before archiving
---

Xác minh rằng một implementation khớp với các artifact của change (specs, tasks, design).

**Input**: Tùy chọn chỉ định tên change sau lệnh `/opsx-verify` (ví dụ: `/opsx-verify add-auth`). Nếu bỏ trống, kiểm tra xem có thể suy luận từ context hội thoại hay không. Nếu mơ hồ hoặc không rõ ràng, bạn BẮT BUỘC phải prompt để hiển thị các change khả dụng.

**Các bước thực hiện (Steps)**

1. **Nếu không cung cấp tên change, prompt để lựa chọn**

   Chạy lệnh `openspec list --json` để lấy danh sách các change khả dụng. Sử dụng **tool AskUserQuestion** để người dùng lựa chọn.

   Hiển thị các change có implementation task (artifact tasks tồn tại).
   Bao gồm schema đã sử dụng cho mỗi change nếu có.
   Đánh dấu các change có task chưa hoàn thành là "(In Progress)".

   **QUAN TRỌNG**: KHÔNG được đoán hoặc tự động chọn một change. Luôn để người dùng lựa chọn.

2. **Kiểm tra status để hiểu schema**
   ```bash
   openspec status --change "<name>" --json
   ```
   Parse JSON để hiểu:
   - `schemaName`: Workflow đang được sử dụng (ví dụ: "spec-driven")
   - Những artifact nào đang tồn tại cho change này

3. **Lấy thư mục change và tải các artifact**

   ```bash
   openspec instructions apply --change "<name>" --json
   ```

   Lệnh này trả về thư mục change và các context file. Đọc tất cả các artifact có sẵn từ `contextFiles`.

4. **Khởi tạo cấu trúc báo cáo xác minh (Verification Report)**

   Tạo một cấu trúc báo cáo với ba khía cạnh:
   - **Tính đầy đủ (Completeness)**: Theo dõi các task và mức độ bao phủ của spec (spec coverage)
   - **Tính chính xác (Correctness)**: Theo dõi việc implementation yêu cầu và mức độ bao phủ của scenario (scenario coverage)
   - **Tính gắn kết (Coherence)**: Theo dõi việc tuân thủ design và tính nhất quán của pattern

   Mỗi khía cạnh có thể có các vấn đề ở mức: CRITICAL (Nghiêm trọng), WARNING (Cảnh báo), hoặc SUGGESTION (Gợi ý).

5. **Xác minh Tính đầy đủ (Completeness)**

   **Hoàn thành Task**:
   - Nếu `tasks.md` tồn tại trong `contextFiles`, hãy đọc nó
   - Parse các checkbox: `- [ ]` (chưa xong) và `- [x]` (đã xong)
   - Đếm số task đã hoàn thành so với tổng số task
   - Nếu tồn tại task chưa xong:
     - Thêm lỗi CRITICAL cho mỗi task chưa xong
     - Khuyến nghị: "Hoàn thành task: <mô tả>" hoặc "Đánh dấu là đã xong nếu thực tế đã implement"

   **Độ bao phủ Spec (Spec Coverage)**:
   - Nếu tồn tại delta spec trong `openspec/changes/<name>/specs/`:
     - Trích xuất tất cả các yêu cầu (được đánh dấu với "### Requirement:")
     - Với mỗi yêu cầu:
       - Tìm kiếm trong codebase các từ khóa liên quan đến yêu cầu đó
       - Đánh giá xem implementation có khả năng đã tồn tại hay chưa
     - Nếu yêu cầu có vẻ chưa được implement:
       - Thêm lỗi CRITICAL: "Không tìm thấy yêu cầu: <tên yêu cầu>"
       - Khuyến nghị: "Implement yêu cầu X: <mô tả>"

6. **Xác minh Tính chính xác (Correctness)**

   **Ánh xạ Implementation yêu cầu (Requirement Implementation Mapping)**:
   - Với mỗi yêu cầu từ các delta spec:
     - Tìm kiếm bằng chứng implementation trong codebase
     - Nếu tìm thấy, ghi lại đường dẫn file và phạm vi dòng (line range)
     - Đánh giá xem implementation có khớp với ý định của yêu cầu hay không
     - Nếu phát hiện sự sai lệch:
       - Thêm WARNING: "Implementation có thể sai lệch so với spec: <chi tiết>"
       - Khuyến nghị: "Xem xét lại <file>:<lines> so với yêu cầu X"

   **Độ bao phủ Scenario (Scenario Coverage)**:
   - Với mỗi scenario trong delta spec (được đánh dấu với "#### Scenario:"):
     - Kiểm tra xem các điều kiện có được xử lý trong code hay không
     - Kiểm tra xem có test nào bao phủ scenario đó không
     - Nếu scenario có vẻ chưa được bao phủ:
       - Thêm WARNING: "Scenario chưa được bao phủ: <tên scenario>"
       - Khuyến nghị: "Thêm test hoặc implementation cho scenario: <mô tả>"

7. **Xác minh Tính gắn kết (Coherence)**

   **Tuân thủ Design (Design Adherence)**:
   - Nếu `design.md` tồn tại trong `contextFiles`:
     - Trích xuất các quyết định chính (tìm các phần như "Decision:", "Approach:", "Architecture:")
     - Xác minh implementation có tuân theo các quyết định đó không
     - Nếu phát hiện mâu thuẫn:
       - Thêm WARNING: "Không tuân thủ quyết định design: <quyết định>"
       - Khuyến nghị: "Cập nhật implementation hoặc sửa lại design.md cho khớp với thực tế"
   - Nếu không có `design.md`: Bỏ qua bước kiểm tra tuân thủ design, ghi chú "Không có design.md để xác minh"

   **Tính nhất quán của Code Pattern**:
   - Xem xét code mới về tính nhất quán với các pattern của dự án
   - Kiểm tra cách đặt tên file, cấu trúc thư mục, coding style
   - Nếu tìm thấy các sai lệch đáng kể:
     - Thêm SUGGESTION: "Sai lệch code pattern: <chi tiết>"
     - Khuyến nghị: "Cân nhắc tuân theo pattern của dự án: <ví dụ>"

8. **Tạo Báo cáo Xác minh (Verification Report)**

   **Bảng điểm tổng quát (Summary Scorecard)**:
   ```
   ## Báo cáo Xác minh: <change-name>

   ### Tổng kết
   | Khía cạnh     | Trạng thái       |
   |--------------|------------------|
   | Tính đầy đủ  | X/Y task, N req  |
   | Tính chính xác| M/N req bao phủ  |
   | Tính gắn kết | Tuân thủ/Vấn đề  |
   ```

   **Các vấn đề theo thứ tự ưu tiên**:

   1. **CRITICAL** (Phải sửa trước khi archive):
       - Các task chưa hoàn thành
       - Các yêu cầu chưa được implement
       - Mỗi mục đi kèm với khuyến nghị cụ thể, có thể thực hiện được

   2. **WARNING** (Nên sửa):
       - Sự sai lệch giữa spec/design
       - Thiếu bao phủ scenario
       - Mỗi mục đi kèm với khuyến nghị cụ thể

   3. **SUGGESTION** (Có thể sửa để tốt hơn):
       - Sự không nhất quán về pattern
       - Các cải thiện nhỏ
       - Mỗi mục đi kèm với khuyến nghị cụ thể

   **Đánh giá cuối cùng**:
   - Nếu có lỗi CRITICAL: "Tìm thấy X lỗi nghiêm trọng. Hãy sửa trước khi archive."
   - Nếu chỉ có cảnh báo: "Không có lỗi nghiêm trọng. Cần cân nhắc Y cảnh báo. Sẵn sàng để archive (kèm theo các cải thiện đã ghi chú)."
   - Nếu tất cả đều ổn: "Tất cả kiểm tra đã vượt qua. Sẵn sàng để archive."

**Các quy tắc xác minh (Verification Heuristics)**

- **Tính đầy đủ**: Tập trung vào các mục khách quan trong checklist (checkbox, danh sách yêu cầu)
- **Tính chính xác**: Sử dụng tìm kiếm từ khóa, phân tích đường dẫn file, suy luận hợp lý - không yêu cầu sự chắc chắn tuyệt đối
- **Tính gắn kết**: Tìm kiếm những sự mâu thuẫn rõ ràng, không soi xét quá kỹ về style
- **False Positives (Dương tính giả)**: Khi không chắc chắn, ưu tiên SUGGESTION hơn WARNING, WARNING hơn CRITICAL
- **Tính thực thi (Actionability)**: Mọi vấn đề phải đi kèm khuyến nghị cụ thể với tham chiếu file/dòng code nếu có thể

**Xử lý khi thiếu thông tin (Graceful Degradation)**

- Nếu chỉ có `tasks.md`: chỉ xác minh việc hoàn thành task, bỏ qua kiểm tra spec/design
- Nếu có tasks + specs: xác minh tính đầy đủ và chính xác, bỏ qua design
- Nếu có đầy đủ artifact: xác minh cả ba khía cạnh
- Luôn ghi chú những kiểm tra nào đã bị bỏ qua và lý do

**Định dạng Output**

Sử dụng markdown rõ ràng với:
- Bảng cho tóm tắt bảng điểm (summary scorecard)
- Các danh sách được nhóm cho các vấn đề (CRITICAL/WARNING/SUGGESTION)
- Tham chiếu code theo định dạng: `file.ts:123`
- Các khuyến nghị cụ thể, có thể thực hiện được
- Không sử dụng các gợi ý mơ hồ như "cân nhắc xem xét"
