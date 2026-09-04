---
description: Cỗ máy phác thảo (Drafting Engine) - Chuyển hoá ý tưởng thô thành đặc tả Prompt hoàn chỉnh thông qua One-shot RAG thay vì chat liên tục.
author: trisjr
---
# Workflow: OPSX Refine (Drafting Engine)

**Mục đích:** Xử lý các ý tưởng thô hoặc yêu cầu mơ hồ từ người dùng, biến chúng thành file đặc tả thao tác (Prompt/Spec) hoàn chỉnh mà không vướng vào luồng chat Socratic liên tục (gây tốn Attention Budget/Tokens).

**Khi nào sử dụng:** 
Khi người dùng chạy lệnh `/opsx-refine [ý tưởng thô]`.

---

## Các Bước Triển Khai (The Engine)

### Bước 1: Tư duy 1-Shot (Silent RAG)
Ngay khi nhận lệnh, bạn KHÔNG ĐƯỢC đặt câu hỏi ngược lại cho người dùng. Thay vào đó, hãy lặng lẽ:
1. Phân tích đối số `[ý tưởng thô]`.
2. Truy xuất danh sách các file đang mở (Active Documents) từ thẻ `<ADDITIONAL_METADATA>` do IDE cung cấp để lấy ngữ cảnh. **Nếu không có Active Documents**, hãy tự động xem xét `search_web` hoặc dùng `grep_search` với phạm vi hẹp để tự tìm ngữ cảnh (Tuyệt đối không dùng tool scan code quét diện rộng bừa bãi).
3. Xác định loại tác vụ (UI fix, Business Logic refactor, Create new component, Document generation, v.v.).
4. Tạo một tên file động mang tính mô tả theo định dạng **`kebab-case`** chuẩn (chữ thường, không dấu, không ký tự đặc biệt, cách nhau bằng dấu gạch ngang). Ví dụ: `draft-fix-auth-bug.md`.

### Bước 2: Tạo File Bản Nháp (Generate Action)
Dựa vào những gì thu thập ở Bước 1, sử dụng công cụ tạo file chuyên dụng (như `write_to_file`) để KHỞI TẠO HOẶC GHI ĐÈ file nháp tại địa chỉ:
📂 `.agent/tmp/[tên_file_động_vừa_tạo].md`

### Bước 3: Cấu trúc Handoff File (Format Chuẩn)
Nội dung của file `[tên_file_động].md` được sinh ra phải tuân thủ nghiêm ngặt cấu trúc mở rộng của CO-STAR Software Engineering dưới đây. 
**QUAN TRỌNG - CHUYỂN USER TRỞ THÀNH NGƯỜI DUYỆT (REVIEWER):** 
Tuyệt đối tránh sử dụng tag `[TODO: ...]`. Việc này làm đứt gãy luồng tư duy và gây áp lực lên người dùng. Thay vào đó, AI BẮT BUỘC PHẢI tự lập luận và đưa ra Đề xuất/Giả định dựa trên Best-Practice hoặc Context của hệ thống. Hãy điền sẵn một phương án khả thi nhất để người dùng chỉ việc "Đọc và Duyệt" (Xóa/sửa nếu họ không đồng ý). Ví dụ: `[Đề xuất của AI: Dùng Node.js vì dự án đang thiên về JS. Không dùng package nào khác]`.

```markdown
# 🎯 Yêu Cầu Thực Thi (Generated Draft)

> **Hướng dẫn:** Anh hãy review (đọc duyệt) bảng đặc tả dưới đây. Em đã tự động điền các phương án kỹ thuật Best-practice khả thi nhất dựa trên Context hiện tại. Nếu có điểm nào chưa ưng ý, anh cứ sửa trực tiếp nhé. 
> Tùy thuộc vào bản chất của bản nháp này, bước tiếp theo có thể là:
> - **Thay đổi nhỏ (Quick Fix):** Chỉ thị trực tiếp cho AI thực thi ngay lập tức mà không cần tạo Spec.
> - **Triển khai Code bài bản:** Gõ lệnh `/opsx-ff` (Tạo Change & Fast-forward thực thi).
> - **Đại tu / Tạo Feature mới:** Gõ lệnh `/opsx-new` để lập kế hoạch tuần tự theo chuẩn OpenSpec.
> - **Lưu thành tài liệu:** Gõ lệnh yêu cầu AI lưu vào thư mục `docs/` phù hợp.

## 1. Mục tiêu cốt lõi (Objective)
[Bản dịch ý tưởng thô thành mục tiêu hành động cụ thể]

## 2. Ngữ cảnh & Phạm vi (Context & Scope)
- **Files liên quan:** [Tên các file từ thẻ ADDITIONAL_METADATA. ĐỪNG để TODO, hãy tự chọn các file liên quan nhất. Nếu lúc trước context trống, tự đề xuất file cần sửa]
- **Tình trạng hiện tại:** [Mô tả bug/hiện trạng đã suy luận]
- **Dữ liệu mồi / Kịch bản:** [Tự đề xuất kịch bản giả lập hoặc dữ liệu mẫu phù hợp]

## 3. Ràng buộc Kỹ thuật (Technical Constraints)
- [Tự đề xuất các ràng buộc an toàn. Ví dụ: "Tuân thủ quy hoạch thư mục /scripts", "Không dùng thư viện ngoài nếu không cần thiết", "Đảm bảo tuân thủ TNMCORE-OS Rules"]

## 4. Skills & Role Đề xuất (Recommended Identity)
- **Role:** [BẮT BUỘC: Đề xuất Role phù hợp nhất. VD: `Software Engineer` nếu code, `Product Manager` nếu design tài liệu]
- **Skills:** [Đề xuất chính xác tên Tool/Skill cần gọi. VD: `clickup-expert`, `typescript-expert`]

## 5. Hành vi kỳ vọng (Expected Behavior / Output)
- [Liệt kê chi tiết luồng chạy do AI đề nghị. Càng chi tiết tỷ lệ thành công ở khâu thực thi càng cao]

## 6. Tiêu chuẩn Hoàn thành (Definition of Done)
- [Tự đề xuất các tiêu chí nghiệm thu chặt chẽ. Ví dụ: Test phải pass với 3 edge cases, không có lỗi linter, UI không vỡ trên Mobile...]
```

### Bước 4: Chuyển Giao (Handoff Message)
Sau khi tạo file xong, in ra màn hình thông báo ĐỘC NHẤT, rõ ràng và DỪNG LẠI (Tuyệt đối không tạo thêm vòng chat). **Tùy biến câu lệnh đề xuất** trong thông báo sao cho phù hợp với loại tác vụ (VD: Code thì gợi ý `/opsx-ff`, Docs thì gợi ý lưu file, Flow lớn thì gợi ý `/opsx-new`). Tuyệt đối không rập khuôn luôn luôn khuyên dùng `/opsx-ff` nếu tác vụ không khớp:

> 🚀 **Đã khởi tạo bản nháp Prompt thành công!**
> 
> Em đã chắt lọc xong ý tưởng của anh và đóng gói thành bản nháp tại: `.agent/tmp/[tên_file_động_vừa_tạo].md`.
> 
> Nhờ anh mở file lên để **Review** lại các đề xuất/giả định kỹ thuật nghen. Khi nào anh thấy bản vẽ đã "Chín", anh có thể chỉ thị bước tiếp theo tuỳ tình huống (ví dụ: Kêu em thực thi bằng **`/opsx-ff`**, dùng **`/opsx-new`** để tách nhánh thay đổi lớn, hoặc chỉ đơn giản là lưu lại thành Spec Specs).

---

## 🛑 Guardrails (Quy Tắc Ràng Buộc Sinh Tồn)
- **Zero-Conversation Rule:** KHÔNG CHAT CHIT. Người dùng thích làm "Sếp" (Review), không thích làm "Học sinh" (Điền vào chỗ trống). Hãy phác thảo giải pháp/đề xuất tự tin nhất của bạn. Nếu sai, họ sẽ sửa. Tuyệt đối không dùng `[TODO]`.
- **Strict Isolation:** Nhiệm vụ duy nhất của luồng này là sinh ra file nháp `.md`. Cố tình đụng vào source code của hệ thống hoặc sinh ra các files khác là VI PHẠM KỶ LUẬT.
