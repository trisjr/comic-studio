---
description: Sync delta specs từ một change sang main specs
---

Sync delta specs từ một change sang main specs.

Đây là một thao tác **do agent điều khiển** - bạn sẽ đọc các delta spec và trực tiếp chỉnh sửa main spec để áp dụng các thay đổi. Điều này cho phép việc merge diễn ra một cách thông minh (ví dụ: thêm một scenario mà không cần copy toàn bộ yêu cầu).

**Input**: Tùy chọn chỉ định tên change sau lệnh `/opsx-sync` (ví dụ: `/opsx-sync add-auth`). Nếu bỏ trống, kiểm tra xem có thể suy luận từ context hội thoại hay không. Nếu mơ hồ hoặc không rõ ràng, bạn BẮT BUỘC phải prompt để hiển thị các change khả dụng.

**Các bước thực hiện (Steps)**

1. **Nếu không cung cấp tên change, prompt để lựa chọn**

   Chạy lệnh `openspec list --json` để lấy danh sách các change khả dụng. Sử dụng **tool AskUserQuestion** để người dùng lựa chọn.

   Hiển thị các change có delta spec (nằm trong thư mục `specs/`).

   **QUAN TRỌNG**: KHÔNG được đoán hoặc tự động chọn một change. Luôn để người dùng lựa chọn.

2. **Tìm các delta spec**

   Tìm các file delta spec trong `openspec/changes/<name>/specs/*/spec.md`.

   Mỗi file delta spec chứa các phần như:
   - `## ADDED Requirements` - Các yêu cầu mới cần thêm
   - `## MODIFIED Requirements` - Các thay đổi trên yêu cầu hiện có
   - `## REMOVED Requirements` - Các yêu cầu cần xóa
   - `## RENAMED Requirements` - Các yêu cầu cần đổi tên (định dạng FROM:/TO:)

   Nếu không tìm thấy delta spec nào, thông báo cho người dùng và dừng lại.

3. **Với mỗi delta spec, áp dụng thay đổi vào main specs**

   Với mỗi capability có delta spec tại `openspec/changes/<name>/specs/<capability>/spec.md`:

   a. **Đọc delta spec** để hiểu các thay đổi dự kiến

   b. **Đọc main spec** tại `openspec/specs/<capability>/spec.md` (có thể chưa tồn tại)

   c. **Áp dụng các thay đổi một cách thông minh**:

      **ADDED Requirements:**
      - Nếu yêu cầu chưa tồn tại trong main spec → thêm nó vào
      - Nếu yêu cầu đã tồn tại → cập nhật nó cho khớp (xử lý như một MODIFIED ngầm định)

      **MODIFIED Requirements:**
      - Tìm yêu cầu trong main spec
      - Áp dụng các thay đổi - việc này có thể là:
        - Thêm các scenario mới (không cần copy các cái hiện có)
        - Chỉnh sửa các scenario hiện có
        - Thay đổi mô tả yêu cầu (description)
      - Bảo toàn các scenario/nội dung không được đề cập trong bản delta

      **REMOVED Requirements:**
      - Xóa toàn bộ khối yêu cầu khỏi main spec

      **RENAMED Requirements:**
      - Tìm yêu cầu FROM, đổi tên nó thành TO

   d. **Tạo main spec mới** nếu capability đó chưa tồn tại:
      - Tạo `openspec/specs/<capability>/spec.md`
      - Thêm phần Purpose (có thể ngắn gọn, đánh dấu là TBD)
      - Thêm phần Requirements với các yêu cầu ADDED

4. **Hiển thị tổng kết (Summary)**

   Sau khi áp dụng tất cả các thay đổi, hãy tóm tắt:
   - Những capability nào đã được cập nhật
   - Những thay đổi nào đã được thực hiện (yêu cầu được thêm mới/chỉnh sửa/xóa/đổi tên)

**Tham chiếu Định dạng Delta Spec (Delta Spec Format Reference)**

```markdown
## ADDED Requirements

### Requirement: New Feature
Hệ thống PHẢI thực hiện một điều gì đó mới.

#### Scenario: Basic case
- **WHEN** người dùng làm X
- **THEN** hệ thống thực hiện Y

## MODIFIED Requirements

### Requirement: Existing Feature
#### Scenario: New scenario to add
- **WHEN** người dùng làm A
- **THEN** hệ thống thực hiện B

## REMOVED Requirements

### Requirement: Deprecated Feature

## RENAMED Requirements

- FROM: `### Requirement: Old Name`
- TO: `### Requirement: New Name`
```

**Nguyên tắc chính: Merge Thông minh (Intelligent Merging)**

Khác với việc merge theo chương trình (programmatic merging), bạn có thể áp dụng các **cập nhật từng phần (partial updates)**:
- Để thêm một scenario, chỉ cần đưa scenario đó vào phần MODIFIED - đừng copy các scenario hiện có
- Bản delta đại diện cho *ý định* (intent), không phải là sự thay thế toàn bộ
- Sử dụng phán đoán của bạn để merge các thay đổi một cách hợp lý

**Output khi thành công**

```
## Specs Đã Sync: <change-name>

Các main spec đã được cập nhật:

**<capability-1>**:
- Đã thêm yêu cầu: "New Feature"
- Đã chỉnh sửa yêu cầu: "Existing Feature" (thêm 1 scenario)

**<capability-2>**:
- Đã tạo file spec mới
- Đã thêm yêu cầu: "Another Feature"

Các main spec hiện đã được cập nhật. Change này vẫn duy trì trạng thái active - hãy archive khi quá trình implementation hoàn tất.
```

**Guardrails**

- Đọc cả delta spec và main spec trước khi thực hiện thay đổi
- Bảo toàn nội dung hiện có không được đề cập trong bản delta
- Nếu có điều gì chưa rõ, hãy yêu cầu làm rõ
- Hiển thị những gì bạn đang thay đổi trong quá trình thực hiện
- Thao tác này phải có tính lũy đẳng (idempotent) - chạy hai lần kết quả phải như nhau
