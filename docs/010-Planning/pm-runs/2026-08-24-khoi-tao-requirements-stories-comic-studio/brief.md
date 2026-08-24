# Brief: 2026-08-24-khoi-tao-requirements-stories-comic-studio

## Yêu cầu gốc

> Điều phối các nhân sự tiến hành xây dựng các tài liệu dưới đây
>
> | # | Artifact | Đường dẫn SSOT | Mô tả |
> |:--|:---------|:---------------|:------|
> | 1 | **PRD** | `docs/020-Requirements/PRD-{Project}.md` | Product Requirements Document — toàn bộ yêu cầu sản phẩm |
> | 2 | **SRS** | `docs/020-Requirements/SRS-{Project}.md` | Software Requirements Specification — yêu cầu kỹ thuật phần mềm |
> | 3 | **BRD** | `docs/020-Requirements/BRD/BRD-{NNN}-{Title}.md` | Business Requirements Document cho từng module |
> | 4 | **Use Cases** | `docs/020-Requirements/Use-Cases/UC-{NN}-{Title}.md` | Kịch bản sử dụng chi tiết (Actor, Flow, Alt Flow) |
> | 5 | **Epics** | `docs/022-User-Stories/Epics/Epic-{Title}.md` | Nhóm tính năng lớn (linked tới PRD) |
> | 6 | **User Stories** | `docs/022-User-Stories/Backlog/Story-{Title}.md` | Stories chuẩn INVEST (linked tới Epic) |
> | 7 | **Prioritized Backlog** _(PO)_ | `docs/022-User-Stories/Backlog-Priority.md` | Backlog đã sắp xếp ưu tiên (RICE/MoSCoW), đánh dấu MVP Stories |
> | 8 | **Glossary** _(cập nhật)_ | `knowledge-base/01-Metas/Glossary.md` | Đồng bộ thuật ngữ Ubiquitous Language |

**Lane**: doc
**Shape**: **A (authoring)** — bản chất là tạo mới 8 loại tài liệu ở tầng 020 + 022, không phải sửa hàng loạt tài liệu đã tồn tại. Cả `docs/020-Requirements/` và `docs/022-User-Stories/` hiện **chỉ có MOC + `.gitkeep`**, không có một tài liệu nội dung nào.

> **Vì sao KHÔNG phải Shape B**, dù run có một phần dọn dẹp: hai MOC đích (`Requirements-MOC.md`, `Stories-MOC.md`) đang chứa **link chết** kế thừa từ repo template (`PRD-TNMCORE-OS.md`, `Story-Request-OTP.md`, `Story-Verify-OTP.md` — cả ba không tồn tại). Nhưng hai file này **thuộc sở hữu PM** (điểm hội tụ MOC), việc sửa chúng nằm trong **close-step bắt buộc** của mọi run lane doc, không phải một sweep riêng. Phần "chuẩn hóa" ở đây là hệ quả tự nhiên của việc đăng ký tài liệu mới, không phải yêu cầu độc lập.

## Triage

| # | Câu hỏi | Đáp án | Lý do |
|---|---------|--------|-------|
| Q1 | Chạm > 1 tầng tài liệu? | **Có** | Chạm **4 tầng**: `020-Requirements` (PRD, SRS, BRD, UC), `022-User-Stories` (Epic, Story, Backlog-Priority), `999-Resources` (Glossary — xem xung đột đường dẫn ở *Open questions*), và lớp điều hướng `docs/000-Index.md` + 2 MOC. |
| Q2 | Sửa doc `approved` / đổi taxonomy hoặc naming convention? | **Có** | `docs/022-User-Stories/Backlog-Priority.md` **KHÔNG có trong bảng Document Type Mapping** của RULE-001 (`status: approved`). Loại tài liệu *"Prioritized Backlog"* chưa được đăng ký ⇒ quy tắc #7 của RULE-001 (*"KHÔNG ĐƯỢC tạo tài liệu mà không kiểm tra bảng Mapping trước"*) chặn việc tạo nó. Cần **một hàng additive** vào RULE-001, y như tiền lệ `MVP Scope` ở run `2026-08-23`. |
| Q3 | Mơ hồ — chưa rõ độc giả đích, phạm vi, thế nào là "xong"? | **Có** | Yêu cầu cho **loại** tài liệu và **đường dẫn**, không cho **số lượng** và **độ sâu**. Cụ thể chưa xác định: (a) bao nhiêu BRD module; (b) bao nhiêu Use Case và ở mức chi tiết nào; (c) Epic cắt theo module hay theo mốc MVP; (d) Story viết cho toàn Full Scope hay chỉ trong horizon Roadmap 09/2026–02/2027; (e) Backlog-Priority dùng RICE hay MoSCoW hay cả hai. Mỗi câu đổi khối lượng run **vài lần**. |
| Q4 | > 5 file hoặc > 1 ngày công? | **Có** *(được tính điểm — Q1 và Q2 đều Có)* | Ước lượng thô **30–50 file** tùy đáp án Q3. Vượt xa trần 5 file ở mọi biến thể scope. |

**Điểm**: **4/4** → **Tier**: **T3**

**Chọn tier thấp do phân vân**: Không. 4/4 là điểm cao nhất có thể; không có phân vân nào để áp *quy tắc phân vân*. Đường đi T3 là bắt buộc: analysis fan-out → gate → nhiều writer song song → verify bởi `context-auditor` → cập nhật `000-Index.md` + rà toàn bộ MOC liên quan.

## Assumptions

1. **`docs/999-Resources/Glossary.md` là SSOT của Ubiquitous Language sản phẩm, KHÔNG phải `knowledge-base/01-Metas/Glossary.md`.**
   → **sai thì hỏng ở đâu**: thuật ngữ domain `comic-studio` bị ghi vào từ điển của **hệ điều hành TNMCORE-OS** (một kho khác, độc giả khác, đang mô tả `Spec-Driven Development`, `MCP`, `Agentic AI`), tạo ra hai nguồn thuật ngữ mâu thuẫn. Đây là câu hỏi gate — xem *Open questions* #1.

2. **Nguồn sự thật của toàn bộ requirement là 5 tài liệu Planning + 2 Analysis đã có trong repo**, không phải suy diễn mới.
   → **sai thì hỏng ở đâu**: PRD/SRS/BRD trở thành tầng thứ hai bịa ra yêu cầu không có căn cứ, và sẽ mâu thuẫn với `MVP-Scope.md` — tài liệu đã chốt ranh giới scope. Ràng buộc chống ảo giác cứng nhất của run này: **mọi requirement phải truy được về một mục cụ thể** trong `MVP-Scope.md` §3 / `Charter` §4–5 / `Analysis-Comic-Studio-Concept` / `Roadmap` §3.

3. ~~**`MVP-Scope.md` §3 đã cho sẵn phân rã module A–G** (7 nhóm).~~ ❌ **ASSUMPTION NÀY SAI — đã sửa sau Bước 2.**
   `MVP-Scope.md` §3 thực tế có **TÁM** nhóm: A Pipeline sinh ảnh · B Story Intelligence · C Comic Director & Layout · D Editor & UI · E Multi-tenancy & hạ tầng · F Kinh tế & credit · G Pháp lý & compliance · **H Chất lượng & vận hành (H1–H6)**. PM chấm triage khi chỉ đọc 80 dòng đầu của bảng nên bỏ sót nhóm H; `findings/business-analyst.md` §1.2 bắt được.
   **Vì sao đây là một sai sót đáng kể, không phải chi tiết**: nhóm H chứa **H1** (HITL gate + eval kit — chính là điều kiện khả thi **R9** của `Charter` §4), **H2** (log preference data — *"moat thật"*), **H4** (export — *"thứ **duy nhất** trong MVP4 người dùng thật sự nhận được"*) và **H6** (golden dataset, `✅` ở **mọi** mốc). Chạy theo bảng 7 module sẽ **im lặng đánh rơi cả bốn hàng này** khỏi tầng Requirements.
   → **Quyết định**: `QC-1` = **8 module**, `BRD-008-Quality-And-Operations.md` được thêm vào. Ghi ở `outline.md` §0.
   → **sai thì hỏng ở đâu (bản đã sửa)**: nếu tự chế một phân rã module khác với `MVP-Scope §3`, kho tài liệu có hai taxonomy module song song và mọi cross-reference giữa tầng 010 và 020 đứt.

4. **`status: draft` cho toàn bộ deliverable của run này.**
   → **sai thì hỏng ở đâu**: `Charter` §9 còn **ba điều kiện chặn cấp dự án chưa gỡ** (trong đó có tư vấn luật sư SHTT trước khi thương mại hoá). Đặt `approved` cho một PRD khi ba blocker còn treo là tự tuyên bố sai. Chúng chuyển `approved` khi anh ra quyết định Go/No-Go.

5. **RULE-001 quy tắc #5 thắng hướng dẫn wiki-link trong `pm-doc.md`.**
   → RULE-001 ghi rõ: *"BẮT BUỘC sử dụng standard markdown links `[Display Name](./relative-path/file.md)`. **KHÔNG** dùng wiki-links `[[...]]`"*, trong khi `pm-doc.md` Bước 5 mục 4 lại yêu cầu `[[Document-Name]]`. RULE-001 là **contract của lane** (`pm-doc.md` Bước 0 tự nói vậy) ⇒ dùng markdown link. **sai thì hỏng ở đâu**: link không phân giải được trong mọi viewer markdown chuẩn, và lệch với 100% link đang tồn tại trong repo.

6. **Không lô nào của run này ghi file khớp mẫu `Analysis-*` hoặc `*-report.md`** ⇒ guardrail chặn `Write` mà `cost.md` run trước khoanh vùng được **không áp vào run này**; dispatch writer thật là an toàn.
   → **sai thì hỏng ở đâu**: nếu guardrail rộng hơn dự đoán, writer báo `BLOCKED` và PM phải tự ghi — làm phình context PM (bài học #1 của run trước, PM đã chiếm 62% output token).

## Open questions

1. **Glossary ghi vào đâu?** — Yêu cầu chỉ `knowledge-base/01-Metas/Glossary.md`; RULE-001 Document Type Mapping chỉ `docs/999-Resources/Glossary.md`. **Hai file đều tồn tại và có nội dung khác nhau về bản chất**: file trong `docs/` là từ điển domain `comic-studio` (54 term, đã có `Story Bible`, `Comic IR`, `best-of-N`…); file trong `knowledge-base/` là từ điển **hệ điều hành TNMCORE-OS**. → **anh trả lời tại gate**, chặn hạng mục #8.
2. **Phạm vi Story: toàn Full Scope hay chỉ horizon Roadmap 09/2026–02/2027?** — chênh nhau khoảng **2–3 lần** số file. → **anh trả lời tại gate**, chặn hạng mục #6 và #7.
3. **Epic cắt theo module A–G hay theo mốc MVP0–MVP4?** — quyết định này lan sang cấu trúc link của Story và cột nhóm của Backlog-Priority. → PM đề xuất tại gate dựa trên `findings/business-analyst.md`.
4. **`Backlog-Priority.md` — thêm hàng vào RULE-001 hay đổi đường dẫn?** → **anh trả lời tại gate**, chặn hạng mục #7.
5. **Backlog-Priority có trở thành nguồn sự thật thứ tư về thứ tự làm việc không?** — `Roadmap.md` (khi nào, thứ tự nào), `MVP-Scope.md` (cái gì vào mốc nào), `OKRs.md` (đo bằng gì) đã chia nhau ba vai. Cần định nghĩa ranh giới của Backlog-Priority **trước khi viết**, nếu không nó mâu thuẫn với ba file kia. → PM chốt tại Bước 4, đưa vào `outline.md` mục *Nguồn sự thật*.

## Kết quả probe `Write`

Không cần probe riêng: `cost.md` run `2026-08-23` đã khoanh vùng guardrail **bám mẫu tên file** (`Analysis-*`, `*-report.md`), với 5/6 writer ghi được bình thường. Không deliverable nào của run này khớp mẫu đó. Vẫn theo dõi: writer nào báo `Write` bị chặn thì ghi vào `escalations.md` ngay.
