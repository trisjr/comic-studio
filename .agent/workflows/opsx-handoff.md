---
description: Tóm tắt phiên làm việc, kết xuất Handoff Report và kết thúc phiên
---

# Workflow: Session Handoff

**Mục đích:** Khi User muốn kết thúc phiên làm việc hiện tại, đóng gói ngữ cảnh nhằm phục vụ việc đổi Role hoặc đơn giản là ngăn ngừa tràn Context (tràn Token/Attention Budget). Workflow này sẽ tự động thu thập fact từ cuộc hội thoại và gen ra bài tóm tắt chuẩn xác mà không cần User giải thích.

**Khi nào sử dụng:**
Khi User chạy lệnh `/opsx-handoff` hoặc yêu cầu "Hãy handoff / tóm tắt phiên chat này để tôi đổi role".

---

## Các Bước Triển Khai (The Handoff Engine)

### Bước 1: Suy luận Ngữ cảnh & Role (Silent Analysis)

Ngay khi có lệnh, Agent KHÔNG đặt câu hỏi. Thay vào đó, hãy lặng lẽ:

1. **Tự động nhận diện Role**: Tự xác định xem mình đang đứng ở vị trí chuyên môn nào trong phiên thao tác gần nhất. **Lưu ý cực kỳ quan trọng:** Phải sử dụng đúng chức danh chuyên môn (VD: Senior AI Engineer, Product Owner, Software Engineer, v.v.). Khi làm tên file, tự động viết liền các từ (VD: `SeniorAIEngineer`).
2. **Rà soát lịch sử (Conversation Log)**: Quét lại những câu giao tiếp và các tool đã gọi. Chỉ nhặt ra các FACTS. **(Quy tắc Anti-Hallucination: Tuyệt đối không phỏng đoán những việc chưa hề xảy ra trong phiên).**

### Bước 2: Nhận diện Các File bị ảnh hưởng (Hard-verification)

**Quy tắc Anti-Hallucination khắt khe:** Trước khi xác định danh sách Affected Files, Agent **BẮT BUỘC** phải gọi công cụ kiểm tra để XÁC MINH SỰ TỒN TẠI của file. Không bao giờ được phép đoán đường dẫn hoặc chỉ dựa vào văn bản trò chuyện cục bộ.

> 💡 _Mẹo Tối Ưu (Token & Latency):_ Để tránh việc phải gọi Tool `list_dir` nhiều lần gây lãng phí tài nguyên, Agent hãy ĐƯỢC ƯU TIÊN chạy 1 lệnh bằng `run_command` (ví dụ: `git status -s` hoặc `git diff --name-only`) để thu thập và lọc ra hàng loạt các File có biến động thực tế.

Sau đó, chia file ra làm 2 nhóm:

1. **Files modified (Verified):** Những file thực sự tạo/sửa (dễ dàng xác định qua `git`).
2. **Dependencies analyzed (Context):** Những file chỉ đọc để lấy ngữ cảnh (nếu có dùng `view_file` trong quá trình làm).

### Bước 3: Kết xuất Báo cáo Handoff

Sử dụng công cụ `write_to_file` (hoặc tương tự) để BẮT BUỘC lưu trữ kết quả xuống thư mục tạm.

- **Quy tắc đường dẫn:** `/tmp/handoffs/Handoff-{YYYY-MM-DD}-{Role}.md` (Đổi `{...}` thành giá trị thực tế).
- **Quy tắc Format (Sử dụng Template dưới đây):**

```markdown
# 🔄 Comprehensive Session Handoff Report

- **Date:** [YYYY-MM-DD HH:mm]
- **Role Output:** [Chức danh chuyên môn]
- **Validation Status:** [Đã xác minh / Chưa xác minh (Chỉ dùng Chưa xác minh nếu không thể chạy check)]
- **Confidence Score:** [Mức độ chắc chắn của Agent đối với tính trọn vẹn của Handoff này, từ 1-100%]

## 1. Session Goals & Main Context

- **Mục tiêu ban đầu:** [Mô tả chi tiết mục tiêu của phiên làm việc]
- **Phạm vi hoàn thành:** [Tiến độ thực tế so với mục tiêu ban đầu. Tập trung vào facts thay vì hứa hẹn]

## 2. Key Decisions & Technical Choices

- **[Tên quyết định 1]**
  - _Context:_ [Bối cảnh dẫn tới quyết định]
  - _Tại sao (Why):_ [Lý do chọn phương án này]
- **[Tên quyết định 2]**
  - _Context & Why:_ ...

## 3. Affected Files & Artifacts

_Chỉ liệt kê các file khi chắc chắn chúng hợp lệ (Đã Hard-verify bằng Tool)._

**A. Files modified (Verified)**

- `[Đường dẫn file 1]` - **[Tạo mới/Đã sửa]** - _Chi tiết thay đổi/lý do..._

**B. Dependencies analyzed (Context)**

- `[Đường dẫn file 2]` - **[Đã đọc]** - _Dùng để tham chiếu luồng..._

## 4. Environment & Tool Trace

_Dấu vết thực thi các công cụ hoặc command để người tới sau nắm rõ môi trường:_

- **Lệnh (Commands) đã chạy:**
  - `[lệnh 1]` - _Kết quả/Ý nghĩa..._
- **Công cụ (Tools/Scripts) đã dùng:** [Liệt kê nếu quan trọng để phiên sau tiếp tục sử dụng]

## 5. Known Issues, Bugs & Blockers

- **Lỗi chưa fix:** [Chi tiết mã lỗi, nguyên nhân nghi ngờ, và các cách đã thử nhưng thất bại]
- **Blockers:** [Các rào cản cản trở tiến độ cần Role/Team member khác hỗ trợ giải quyết]

## 6. Next Actions (Checklist cho phiên sau)

- [ ] Tham số/Context cần nạp ngay: [Điền]
- [ ] Nhiệm vụ 1: [Ghi chú chi tiết cách thực hiện phần còn lại]
- [ ] Nhiệm vụ 2: [Ghi chú chi tiết]

## 7. New Knowledge / Rules (Tùy chọn)

- [Liệt kê các bài học, Rule hệ thống mới phát hiện ra, hoặc Preference/sở thích mới của User để phục vụ cho lệnh /memo sau này]
```

### Bước 4: Thông báo Dừng (Handoff Complete)

Sau khi lưu file thành công, hãy đưa ra một thông điệp CLI ngắn gọn, ngầu và kết thúc (Tuyệt đối không hỏi thêm "Tôi có thể giúp gì nữa không?"):

> 📦 **Handoff Report đã lưu thành công vào thư mục tạm!**
>
> Báo cáo được lưu tại: `tmp/handoffs/[tên-file].md`
>
> Tránh dính vào source code sạch sẽ! Gợi ý: Hãy gõ lệnh **`/wake-up`** cùng tên Role mới và yêu cầu Agent nạp file Handoff trên để bắt đầu ca trực mới không vết gãy nhé!
