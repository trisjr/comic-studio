# Brief: 2026-08-23-danh-gia-y-tuong-comic-studio

## Yêu cầu gốc

> Em hãy điều phối agent phân tích @docs/999-Resources/Request.md xem ý tưởng của anh có phù hợp hay chưa, có khả thi hay không? Cần cải thiện, thay đổi gì không?

**Lane**: doc
**Shape**: A (authoring) — Tạo mới một tài liệu đánh giá; không phải sweep chuẩn hóa kho docs.
Lý do: `docs/` hiện chỉ có MOC rỗng và templates, không có tài liệu nội dung nào để chuẩn hóa.
Deliverable là một tài liệu phân tích mới, tra Document Type Mapping → `Analysis-{Topic}.md`.

## Đối tượng phân tích

`docs/999-Resources/Request.md` — 894 dòng, 18 mục, mô tả concept **comic-studio**:
pipeline chuyển novel/truyện chữ → comic pages, với Story Bible + Timeline state +
Canonical References + Visual Prompt Compiler + Continuity Checker làm moat.

## Triage

| # | Câu hỏi | Đáp án | Lý do |
|---|---------|--------|-------|
| Q1 | Chạm > 1 tầng tài liệu? | **Có** | Trả lời "khả thi hay không" bắt buộc xét đồng thời ba tầng: **050-Research** (khả thi công nghệ image consistency 2026, bối cảnh đối thủ), **030-Specs** (kiến trúc 3-layer, DB model, Visual Prompt Compiler, microservice split), **010-Planning** (thứ tự 4 MVP milestone, effort). Không tầng nào một mình đủ căn cứ. |
| Q2 | Sửa doc `approved` / đổi taxonomy? | **Không** | `RULE-001` (`status: approved`) được **tuân thủ**, không sửa. Không đổi naming convention hay cấu trúc Dewey. Không tạo thư mục top-level mới. |
| Q3 | Mơ hồ — chưa rõ độc giả đích / phạm vi / "xong"? | **Có** | `Request.md` là brainstorm kiến trúc, **không** nêu: quy mô team, ngân sách, deadline, thương mại hay cá nhân, nguồn truyện là IP tự sở hữu hay của người khác, target platform. "Khả thi" là hàm của các biến đó. Xử lý: đi theo Assumptions bên dưới, đưa các biến đổi kết luận nhiều nhất lên GATE hỏi anh. |
| Q4 | > 5 file hoặc > 1 ngày công? | **Không** (có tính điểm, vì Q1 = Có) | Ước lượng 1 tài liệu deliverable chính + 2 file phụ (Research-MOC, Glossary). Dưới trần 5 file. Nội dung nặng nhưng khối lượng file nhỏ. |

**Điểm**: 2/4 → **Tier**: **T2**
**Chọn tier thấp do phân vân**: Không.
Cân nhắc T3 vì phạm vi phân tích rất rộng (18 mục), nhưng T3 đòi sweep nhiều writer song song
+ rà toàn bộ MOC — không tương xứng với **một** tài liệu deliverable. T2 (fan-out → soạn thảo →
verify bởi agent khác) là đúng hình dạng công việc.
**Điều kiện escalate lên T3**: nếu sau fan-out anh yêu cầu tách thành nhiều deliverable
(ví dụ Analysis + ADR + Risk-Register + Roadmap), ghi vào `escalations.md` và báo anh trước khi đổi.

## Assumptions

- **A1 — Dự án cá nhân, quy mô rất nhỏ (1 dev, có AI assist), ngân sách tự bỏ.**
  Căn cứ: đường dẫn `Projects/Personal/comic-studio`, repo greenfield (`src/`, `test/` rỗng, 1 commit duy nhất).
  → **Sai thì hỏng ở đâu**: nếu thực tế là team có funding, phần "cắt scope MVP" trong khuyến nghị sẽ quá bảo thủ, và verdict khả thi sẽ bị đánh giá thấp hơn thực tế. Đưa lên GATE để anh xác nhận.
- **A2 — Chưa có dòng code nào.** Căn cứ: `src/` và `test/` rỗng, `openspec/changes/` rỗng.
  → **Sai thì hỏng ở đâu**: nếu đã có prototype, phân tích sẽ bỏ sót ràng buộc từ code thật. Đã verify bằng `find`, rủi ro thấp.
- **A3 — Nguồn truyện đầu vào chưa xác định là IP tự sở hữu hay của tác giả khác.**
  → **Sai thì hỏng ở đâu**: đây là biến làm thay đổi verdict **mạnh nhất** — mạnh hơn cả ngân sách. Nếu là truyện của người khác, sản phẩm là derivative work và rủi ro pháp lý chặn đường thương mại hóa, làm sụp phần lớn giá trị của "moat". Bắt buộc hỏi tại GATE.
- **A4 — Tài liệu deliverable viết bằng Tiếng Việt, giữ nguyên technical term.**
  Căn cứ: `.claude/rules/create-file-markdown.md`.
- **A5 — Độc giả đích của tài liệu là chính anh** (người ra quyết định build/không build), không phải investor hay team ngoài.
  → **Sai thì hỏng ở đâu**: nếu để pitch cho người khác, tài liệu cần thêm phần market sizing và business model mà run này không làm.

## Quyết định contract (PM phân xử ngay tại Bước 1)

- **Xung đột `pm-doc.md` vs `RULE-001` về kiểu link.** `pm-doc.md` Bước 4/5 yêu cầu wiki-link `[[Document-Name]]`; `RULE-001` mục *Các quy tắc nghiêm ngặt* #5 và *Linking Rules* yêu cầu **standard markdown link relative path** và ghi rõ **KHÔNG dùng wiki-link**.
  → **Phân xử: theo `RULE-001`.** Lý do: `RULE-001` có `status: approved` và `updated: 2026-03-03`, được `pm-doc.md` Bước 0 chỉ định là "contract của lane này". Command file là quy trình, contract là chuẩn. Mọi link trong run này dùng `[Text](./relative/path.md)`.
- **`.agent/roles/` không tồn tại.** `pm-core.md` (Nguyên tắc 1) và Dispatch Prompt Template trỏ tới `.agent/roles/<role>.md`, nhưng thư mục đó không có trong repo. Persona thực tế nằm trong chính agent definition ở `.claude/agents/<role>.md` (tool Agent tự nạp).
  → **Phân xử**: bỏ dòng `[ROLE] Nạp .agent/roles/...` khỏi prompt dispatch, thay bằng trỏ tới `knowledge-base/45-Role-Memory/<role>/` (bắt buộc theo `learning-loop.md`). PM đã đọc `45-Role-Memory/product-manager/000-Core-Memory.md`.
- **`Request.md` chưa được commit** (git status `AM` ở checkout gốc, absent khỏi `HEAD`). Worktree branch từ `origin/main` nên không có file này.
  → **Hành động đã làm**: copy `Request.md` từ checkout gốc vào worktree **trước** mọi dispatch. Nếu không, mọi worker đọc file sẽ không thấy gì.

## Nợ kỹ thuật phát hiện được — NGOÀI scope run này

Ghi lại để không mất dấu, **không** tự ý sửa (Shape A, không phải sweep):

1. **`docs/000-Index.md` KHÔNG tồn tại**, dù `RULE-001` *Cấu trúc thư mục bắt buộc* ghi "BẮT BUỘC phải có". `docs/999-Resources/Resources-MOC.md` đang link tới `../000-Index.md` → **link chết**.
2. **`docs/999-Resources/Templates/Template-Daily-Report.md` KHÔNG tồn tại**, nhưng `Resources-MOC.md` đang link tới → **link chết**. Đồng thời 13 template đang có thật thì **không** template nào được liệt kê trong MOC đó.
3. **`docs/999-Resources/Templates/Template-Analysis.md` là stub** — chỉ có frontmatter + dòng "(Content to be added)". Không dùng được làm khuôn. → `outline.md` của run này chính là contract cấu trúc thật.
4. **`docs/999-Resources/Glossary.md` chỉ có 3 thuật ngữ về OTP** — di sản từ dự án khác, không liên quan comic-studio. Đúng như `pm-doc.md` Bước 6 cảnh báo: không đủ làm chuẩn đối chiếu terminology.
5. **11 MOC đều rỗng nội dung**, chỉ có frontmatter + vài dòng link thư mục.

→ Đề xuất: chạy một run `/pm-doc` Shape B riêng để dọn. Không trộn vào run này.

## Open questions

| # | Câu hỏi | Ai trả lời | Chặn phase nào |
|---|---------|-----------|----------------|
| OQ1 | Nguồn truyện là IP anh tự sở hữu, hay truyện của tác giả khác? | Anh — tại GATE | Không chặn fan-out; chặn phần *Rủi ro pháp lý* của tài liệu (Bước 5) |
| OQ2 | Mục tiêu là công cụ cá nhân, hay sản phẩm thương mại/SaaS? | Anh — tại GATE | Không chặn fan-out; quyết định độ sâu phần *Moat & Go-to-market* |
| OQ3 | Có ràng buộc ngân sách cứng cho chi phí inference/GPU không? | Anh — tại GATE | Không chặn fan-out; quyết định khuyến nghị self-host vs API |

> Cả ba câu **không** chặn Bước 2: ba lens của fan-out (kiến trúc, công nghệ/đối thủ, AI pipeline)
> đều **bất biến** với ba câu này. Gộp chúng vào đúng một lượt AskUserQuestion tại GATE
> thay vì hỏi hai lần — quan trọng vì run này chạy dưới dạng background job.
