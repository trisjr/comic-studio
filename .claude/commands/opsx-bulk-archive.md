---
description: Archive cùng lúc nhiều completed change
---

Archive nhiều completed change trong một thao tác duy nhất.

Skill này cho phép bạn batch-archive các change, xử lý các xung đột spec một cách thông minh bằng cách kiểm tra codebase để xác định những gì thực sự đã được implement.

**Input**: Không yêu cầu (sẽ prompt để lựa chọn)

**Các bước thực hiện (Steps)**

1. **Lấy danh sách các active change**

   Chạy lệnh `openspec list --json` để lấy tất cả các active change.

   Nếu không có active change nào, thông báo cho người dùng và dừng lại.

2. **Prompt để lựa chọn change**

   Sử dụng **tool AskUserQuestion** với tính năng đa chọn (multi-select) để người dùng chọn:
   - Hiển thị mỗi change kèm theo schema tương ứng
   - Bao gồm tùy chọn "All changes" (Tất cả change)
   - Cho phép chọn bất kỳ số lượng nào (chọn 1 cũng được, nhưng 2 trở lên là trường hợp sử dụng phổ biến)

   **QUAN TRỌNG**: KHÔNG được tự động chọn. Luôn để người dùng lựa chọn.

3. **Batch validation - Thu thập trạng thái cho tất cả các change đã chọn**

   Với mỗi change được chọn, thu thập:

   a. **Trạng thái Artifact** - Chạy `openspec status --change "<name>" --json`
      - Parse list `schemaName` và `artifacts`
      - Ghi chú artifact nào đã `done` và artifact nào ở trạng thái khác

   b. **Mức độ hoàn thành task** - Đọc `openspec/changes/<name>/tasks.md`
      - Đếm số lượng `- [ ]` (chưa xong) so với `- [x]` (đã xong)
      - Nếu không có file tasks, ghi chú là "No tasks"

   c. **Delta specs** - Kiểm tra thư mục `openspec/changes/<name>/specs/`
      - Liệt kê các capability spec đang tồn tại
      - Với mỗi spec, trích xuất tên yêu cầu (các dòng khớp với `### Requirement: <name>`)

4. **Phát hiện xung đột spec (Spec Conflict)**

   Xây dựng một bản đồ (map) theo dạng `capability -> [các change tác động vào nó]`:

   ```
   auth -> [change-a, change-b]  <- XUNG ĐỘT (2+ change)
   api  -> [change-c]            <- OK (chỉ có 1 change)
   ```

   Xung đột xảy ra khi có từ 2 change trở lên đã chọn có delta spec cho cùng một capability.

5. **Giải quyết xung đột một cách thông minh (Agentically)**

   **Với mỗi xung đột**, hãy điều tra codebase:

   a. **Đọc các delta spec** từ mỗi change gây xung đột để hiểu những gì mỗi bên tuyên bố thêm mới/chỉnh sửa

   b. **Tìm kiếm bằng chứng implementation trong codebase**:
      - Tìm code đang implement các yêu cầu từ mỗi delta spec
      - Kiểm tra các file, function hoặc test liên quan

   c. **Xác định cách giải quyết (Resolution)**:
      - Nếu chỉ có duy nhất một change thực tế đã được implement -> sync spec của change đó
      - Nếu cả hai đều đã implement -> áp dụng theo thứ tự thời gian (cái cũ trước, cái mới ghi đè sau)
      - Nếu không cái nào được implement -> bỏ qua sync spec, cảnh báo cho người dùng

   d. **Ghi lại giải quyết** cho mỗi xung đột:
      - Spec của change nào sẽ được áp dụng
      - Theo thứ tự nào (nếu cả hai)
      - Cơ sở lý luận (Rationale - những gì đã tìm thấy trong codebase)

6. **Hiển thị bảng trạng thái tổng hợp**

   Hiển thị một bảng tóm tắt tất cả các change:

   ```
   | Change               | Artifacts | Tasks | Specs   | Xung đột   | Status |
   |---------------------|-----------|-------|---------|-----------|--------|
   | schema-management   | Done      | 5/5   | 2 delta | Không     | Ready  |
   | project-config      | Done      | 3/3   | 1 delta | Không     | Ready  |
   | add-oauth           | Done      | 4/4   | 1 delta | auth (!)  | Ready* |
   | add-verify-skill    | 1 left    | 2/5   | Không   | Không     | Warn   |
   ```

   Đối với các xung đột, hiển thị cách giải quyết:
   ```
   * Giải quyết xung đột:
     - auth spec: Sẽ áp dụng add-oauth sau đó là add-jwt (cả hai đều đã implement, theo thứ tự thời gian)
   ```

   Đối với các change chưa hoàn thiện, hiển thị cảnh báo:
   ```
   Cảnh báo:
   - add-verify-skill: 1 artifact chưa xong, 3 task chưa xong
   ```

7. **Xác nhận thao tác hàng loạt (Batch Operation)**

   Sử dụng **tool AskUserQuestion** để xác nhận một lần duy nhất:

   - "Archive N change?" với các tùy chọn dựa trên trạng thái
   - Các tùy chọn có thể bao gồm:
     - "Archive tất cả N change"
     - "Chỉ archive N change đã sẵn sàng (bỏ qua những cái chưa xong)"
     - "Hủy bỏ"

   Nếu có các change chưa hoàn thiện, phải làm rõ rằng chúng sẽ được archive kèm theo cảnh báo.

8. **Thực hiện archive cho từng change đã xác nhận**

   Xử lý các change theo thứ tự đã xác định (tôn trọng quy trình giải quyết xung đột):

   a. **Sync specs** nếu tồn tại delta spec:
      - Sử dụng phương pháp openspec-sync-specs (merge thông minh do agent điều khiển)
      - Đối với các xung đột, áp dụng theo thứ tự đã giải quyết
      - Theo dõi xem việc sync đã được thực hiện hay chưa

   b. **Thực hiện archive**:
      ```bash
      mkdir -p openspec/changes/archive
      mv openspec/changes/<name> openspec/changes/archive/YYYY-MM-DD-<name>
      ```

   c. **Theo dõi kết quả** cho mỗi change:
      - Thành công: đã archive thành công
      - Thất bại: lỗi trong quá trình archive (ghi lại lỗi)
      - Bỏ qua: người dùng chọn không archive (nếu có)

9. **Hiển thị tổng kết**

   Hiển thị kết quả cuối cùng:

   ```
   ## Batch Archive Hoàn Tất

   Đã archive 3 change:
   - schema-management-cli -> archive/2026-01-19-schema-management-cli/
   - project-config -> archive/2026-01-19-project-config/
   - add-oauth -> archive/2026-01-19-add-oauth/

   Đã bỏ qua 1 change:
   - add-verify-skill (người dùng chọn không archive change chưa xong)

   Tổng kết Sync Spec:
   - 4 delta spec đã được sync vào main specs
   - 1 xung đột đã được giải quyết (auth: áp dụng cả hai theo thứ tự thời gian)
   ```

   Nếu có bất kỳ thất bại nào:
   ```
   Thất bại 1 change:
   - some-change: Thư mục archive đã tồn tại
   ```

**Ví dụ về Giải quyết xung đột**

Ví dụ 1: Chỉ một bên được implement
```
Xung đột: specs/auth/spec.md bị tác động bởi [add-oauth, add-jwt]

Kiểm tra add-oauth:
- Delta thêm yêu cầu "OAuth Provider Integration"
- Tìm kiếm codebase... tìm thấy src/auth/oauth.ts đang implement luồng OAuth

Kiểm tra add-jwt:
- Delta thêm yêu cầu "JWT Token Handling"
- Tìm kiếm codebase... không tìm thấy implementation cho JWT

Giải quyết: Chỉ có add-oauth là đã được implement. Sẽ chỉ sync spec của add-oauth.
```

Ví dụ 2: Cả hai đều được implement
```
Xung đột: specs/api/spec.md bị tác động bởi [add-rest-api, add-graphql]

Kiểm tra add-rest-api (tạo ngày 2026-01-10):
- Delta thêm yêu cầu "REST Endpoints"
- Tìm kiếm codebase... tìm thấy src/api/rest.ts

Kiểm tra add-graphql (tạo ngày 2026-01-15):
- Delta thêm yêu cầu "GraphQL Schema"
- Tìm kiếm codebase... tìm thấy src/api/graphql.ts

Giải quyết: Cả hai đều đã implement. Sẽ áp dụng spec của add-rest-api trước,
sau đó đến spec của add-graphql (theo thứ tự thời gian, cái mới hơn sẽ được ưu tiên).
```

**Output khi thành công**

```
## Batch Archive Hoàn Tất

Đã archive N change:
- <change-1> -> archive/YYYY-MM-DD-<change-1>/
- <change-2> -> archive/YYYY-MM-DD-<change-2>/

Tổng kết Sync Spec:
- N delta spec đã được sync vào main specs
- Không có xung đột (hoặc: M xung đột đã được giải quyết)
```

**Output khi thành công một phần**

```
## Batch Archive Hoàn Tất (một phần)

Đã archive N change:
- <change-1> -> archive/YYYY-MM-DD-<change-1>/

Đã bỏ qua M change:
- <change-2> (người dùng chọn không archive change chưa xong)

Thất bại K change:
- <change-3>: Thư mục archive đã tồn tại
```

**Output khi không có change nào**

```
## Không có change nào để Archive

Không tìm thấy active change nào. Sử dụng `/opsx-new` để tạo một change mới.
```

**Guardrails**

- Cho phép bất kỳ số lượng change nào (1 cũng được, nhưng 2 trở lên là trường hợp phổ biến)
- Luôn prompt để lựa chọn, không bao giờ tự động chọn
- Phát hiện xung đột spec sớm và giải quyết bằng cách kiểm tra codebase
- Khi cả hai change đều đã được implement, áp dụng spec theo thứ tự thời gian
- Chỉ bỏ qua sync spec khi thiếu implementation (phải cảnh báo người dùng)
- Hiển thị rõ ràng trạng thái của từng change trước khi xác nhận
- Sử dụng xác nhận duy nhất cho toàn bộ batch
- Theo dõi và báo cáo tất cả các kết quả (thành công/bỏ qua/thất bại)
- Bảo toàn `.openspec.yaml` khi di chuyển vào archive
- Tên thư mục archive đích sử dụng ngày hiện tại: `YYYY-MM-DD-<name>`
- Nếu thư mục archive đích đã tồn tại, change đó sẽ thất bại nhưng vẫn tiếp tục xử lý những cái khác
