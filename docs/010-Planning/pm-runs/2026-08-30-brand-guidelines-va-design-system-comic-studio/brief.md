# Brief: 2026-08-30-brand-guidelines-va-design-system-comic-studio

## Yêu cầu gốc

> Điều phối nhân sự thực hiện phân tích và xác định Brand guidelines & Design system cho dự án theo @/Users/trisjr/Projects/Tenomad/TNMCore-OS/knowledge-base/20-Project/SDLC-Phases/Phase-3-Product-Design.md
> Sau khi chốt thì sẽ bắt đầu thực hiện khởi tạo các tài liệu khác ở turn (run) sau

**Lane**: doc
**Shape**: A (authoring) — lý do: `docs/040-Design/` hiện **không có tài liệu nội dung nào** (chỉ `Design-MOC.md` rỗng 0 byte). Không có gì để chuẩn hoá ⇒ đây là tạo mới, không phải normalization sweep. Không lai Shape B: run này không đụng tài liệu đã tồn tại ở tầng khác, ngoài MOC/Index (PM giữ) và `Glossary.md`.

**Worktree**: `.claude/worktrees/phase-3-brand-design-system`, branch `worktree-phase-3-brand-design-system`.

### Phạm vi được cắt tường minh bởi anh

Phase 3 định nghĩa **5 artifact**. Anh chốt run này **chỉ làm Design System + Brand Guidelines**, phần còn lại sang run sau:

| # | Artifact Phase 3 | Run này? | Ghi chú |
|---|---|:--:|---|
| — | **Brand Guidelines** | ✅ | Phase 3 §2 liệt kê là **Input** *"(nếu có)"* — dự án **chưa có** ⇒ phải tự sinh trước, nếu không Design System không có gì để neo |
| 1 | **Design System** (`docs/040-Design/Design-System/`) | ✅ | Color Tokens, Typography, Spacing, Components |
| 2 | Wireframes (`Wireframes/WF-*.png`) | ❌ | Run sau |
| 3 | User Flow (`Specs/UF-*.md`) | ❌ | Run sau |
| 4 | UI Specs (`Specs/Proto-*.md`) | ❌ | Run sau |
| 5 | Assets (`Assets/`) | ❌ | Run sau |

> ⚠️ **Hệ quả phải nói thẳng**: 4 tiêu chí chuyển Phase ở Phase 3 §6 sẽ **chỉ đạt 1/4** sau run này (*"Design System có đủ Colors, Typography, Spacing"*). Ba tiêu chí còn lại (Wireframe, User Flow, UI Specs có đủ trạng thái) phụ thuộc run sau. **Run này không đóng được Phase 3** — và đó đúng là ý anh.

## Triage

| # | Câu hỏi | Đáp án | Lý do |
|---|---------|--------|-------|
| Q1 | Chạm > 1 tầng tài liệu? | **Có** | Deliverable nội dung nằm ở `040-Design/Design-System/` **và** `999-Resources/Glossary.md`. Design System sinh ra một lớp thuật ngữ mới (design token, semantic color, elevation, focus ring, type scale…) mà `Glossary.md` (69 thuật ngữ, 10 nhóm, `status: live`, 177 dòng) hiện **không có nhóm nào** phủ. Đây là **quyết định phạm vi của PM**, không phải sự thật khách quan — anh cắt Glossary tại gate thì Q1 → Không. ⚠️ MOC và `000-Index.md` **không** được tính vào Q1: mọi run lane doc đều phải cập nhật chúng; tính vào thì Q1 luôn = Có và câu hỏi mất nghĩa. |
| Q2 | Sửa doc `approved` / đổi taxonomy? | **Có** | RULE-001 (`status: approved`) §Document Type Mapping, nhóm **040-Design**, chỉ đăng ký **4 loại**: Design System · Wireframe · User Flow · Prototype Spec. **Không có hàng nào cho *Brand Guidelines***, mà quy tắc #7 cấm tạo tài liệu chưa tra được bảng. Phải chốt tại gate — xem *Open questions* **Q-A**. Đường (b) là sửa tài liệu `approved`. |
| Q3 | Mơ hồ / chưa rõ độc giả đích? | **Có** | Ba khoảng trống thật, đã verify chứ không suy diễn: (1) `PRD-Comic-Studio` §*Người dùng & vấn đề* mở bằng `TBD` — repo **không có persona/JTBD** nào (`000-Index.md` ghi nhận tường minh) ⇒ brand không có audience để neo; (2) **chưa có brand direction nào tồn tại** — tên hiển thị, tone, personality, màu chủ đạo đều chưa ai quyết, và đó là quyết định của anh, không phải của agent; (3) chưa rõ **độc giả đích của chính Design System**: với `R1` (1 dev + AI assist), nó là spec để **AI sinh code Tailwind/shadcn**, hay tài liệu cho designer người đọc? Hai đích cho ra hai tài liệu rất khác nhau. |
| Q4 | > 5 file hoặc > 1 ngày công? | **Có** | Ước 6–9 file nội dung. **Được tính điểm** vì Q1 = Có (đúng luật tie-breaker `/pm-doc` Bước 1.3). |

**Điểm**: 4/4 → **Tier**: T3

**Chọn tier thấp do phân vân**: **Không**. Cả 4 câu "Có" đều có căn cứ cứng, và run đúng hình dạng T3: nhiều writer song song trên file rời nhau + phải cập nhật `000-Index.md` (Design System là tài liệu lớn) + phải viết `Design-MOC.md` từ số 0.

> Điểm mong manh nhất là **Q1**. Anh cắt `Glossary.md` khỏi scope ⇒ điểm còn 3/4 — **vẫn T3**, tier không đổi. Ghi ra để khỏi phải chấm lại.

## Assumptions

1. **`docs/040-Design/` trống hoàn toàn** ⇒ không có ripple lên tài liệu design đang tồn tại.
   → **sai thì hỏng ở đâu**: đã verify bằng `find docs -type f -name "*.md"` — chỉ có `Design-MOC.md` (0 byte). Rủi ro ≈ 0.

2. **ADR-001 là ràng buộc cứng của Design System**: frontend = Vite + React + TS + TanStack Query + **shadcn/ui (Radix Primitives) + Tailwind CSS**, SPA thuần ⛔ không SSR.
   → **sai thì hỏng ở đâu**: design token phải phát biểu bằng ngôn ngữ dùng được ngay trong stack này. ADR-001 bị đảo ⇒ toàn bộ tầng token viết lại.
   → ⚠️ **ĐÃ SỬA sau lens `architect` (mâu thuẫn `X-2`)**. Bản đầu của assumption này viết *"CSS variable theo quy ước shadcn (`--background`, `--foreground`, `--primary`…)"* và **gán nội dung đó cho ADR-001**. Sai: ADR-001 ⛔ **không nêu một tên biến CSS nào**. Đó là **quy ước của thư viện shadcn**, hợp lệ để chọn nhưng là **quyết định của Phase 3**, ⛔ không phải nội dung kế thừa từ Phase 2.
   → **Hệ quả bắt buộc cho Bước 5**: writer khai tên biến token phải dán nhãn *"quyết định Phase 3"* và verify tên theo **version shadcn thật**, ⛔ tuyệt đối không trích `ADR-001` làm nguồn cho danh sách tên biến, ⛔ không chép từ trí nhớ.
   → ⚠️ **Thay đổi này CHƯA COMMIT ở checkout gốc** (`git status`: `M ADR-001`). Worktree được tạo từ base ref nên nhận **bản cũ, không có shadcn**. **PM đã copy bản anh đang sửa sang worktree** để worker đọc đúng hệ toạ độ. Hệ quả: `git status` của worktree hiện `M ADR-001` — đây **không phải deliverable của run**, xem *Open questions* **Q-C** để chốt cách xử lý khi commit.

3. **Wrap tiếng Việt là ràng buộc THIẾT KẾ, không chỉ ràng buộc backend.** ADR-001 `## Decision` điều 8: chuẩn hoá **NFC** tại biên ingest; ngắt dòng theo **grapheme cluster + word boundary** bằng `Intl.Segmenter`; ⛔ **không** wrap ở frontend; ⛔ **không** wrap bằng font khác font sẽ render.
   → **sai thì hỏng ở đâu**: Typography spec **bắt buộc** tách hai hệ font — *font UI* (giao diện editor) và *font render vào ảnh comic* (bubble/typeset layer). Gộp làm một là vi phạm điều 8 ngay ở tầng thiết kế, và lỗi này chỉ lộ ra khi đã sinh ảnh. Đây là ràng buộc **dễ bị bỏ sót nhất** của run.

4. **Persona chưa tồn tại và run này KHÔNG tự sinh persona.** Brand guidelines neo vào audience **đã có căn cứ trong repo** (`Analysis-Market-Competitor-Landscape.md`, `Charter-Comic-Studio` §Stakeholder/RACI, `MVP-Scope`), và khai `TBD` ở mọi chỗ cần persona thật.
   → **sai thì hỏng ở đâu**: nếu run tự bịa persona, nó tạo **nguồn sự thật giả** ở tầng 040 mà tầng 020 không có — đúng loại ảo giác `/pm-doc` cảnh báo là *"trôi thẳng vào kho tri thức"*. Thà `TBD` + `PARTIAL`.

5. **`.agent/roles/` KHÔNG tồn tại trong repo này** — đã verify (`ls: .agent: No such file or directory`). Định nghĩa role nằm ở `.claude/agents/*.md`, runtime tự nạp khi dispatch.
   → **sai thì hỏng ở đâu**: `pm-core.md` §Dispatch Prompt Template ghi `Nạp .agent/roles/<role>.md`. Dán nguyên văn dòng đó vào prompt sẽ khiến worker đi đọc **đường dẫn không tồn tại** — tốn tool call, có thể sinh `BLOCKED` giả. Prompt dispatch của run này **bỏ dòng đó**. Tương tự, `.claude/rules/00-rule-index.md` trỏ `.agent/rules/` cũng không tồn tại ⇒ không viện dẫn đường dẫn đó trong `[CONSTRAINTS]`.

6. **`Glossary.md` KHÔNG còn là stub.** `/pm-doc` Bước 6 mô tả nó *"~12 dòng, không đủ làm chuẩn đối chiếu"* — mô tả đó **đã lỗi thời**: thực đo **177 dòng, 69 thuật ngữ, `status: live`**.
   → **sai thì hỏng ở đâu**: nếu verify pass tin theo mô tả cũ, nó sẽ bỏ qua bước đối chiếu thuật ngữ — trong khi Glossary hiện **đủ tư cách làm chuẩn**. Tiêu chí *Coherence* ở Bước 6 phải đối chiếu thật.

## Open questions

| # | Câu hỏi | Ai trả lời | Chặn phase nào |
|---|---|---|---|
| **Q-A** | *Brand Guidelines* đăng ký vào RULE-001 thế nào? (a) map vào hàng `Design System` sẵn có ⇒ `docs/040-Design/Design-System/Brand-Guidelines.md`, không sửa RULE-001; (b) thêm **một hàng additive** vào Document Type Mapping. | **Anh** — tại gate | Chặn Bước 5 (writer không được ghi khi chưa tra được bảng) |
| **Q-B** | Brand direction: tên hiển thị, tone & personality, hướng màu chủ đạo. | **Anh** — tại gate | Chặn hạng mục Brand Guidelines |
| **Q-C** | Thay đổi ADR-001 (`shadcn/ui + Tailwind`) chưa commit. Coi là đã chốt để neo Design System vào? Và có commit nó cùng run này không? | **Anh** — tại gate | Chặn toàn bộ tầng token |
| **Q-D** | `Glossary.md` có nằm trong scope run này không? | **Anh** — tại gate | Ảnh hưởng Q1, **không** đổi tier |
| **Q-E** | Độc giả đích của Design System: spec cho AI sinh code, hay tài liệu cho người đọc? | **Anh** — tại gate | Quyết định độ chi tiết của mọi file |

> **Q-B** và **Q-E** là quyết định business/thẩm mỹ của anh, thuộc **Tầng 3 Escalation**. Agent không được tự quyết thay — đó là chỗ ảo giác đắt nhất của lane doc.

## Bước 2 — lens đã chọn và lens đã cắt

| Lens | Chọn? | Lý do |
|---|:--:|---|
| `product-designer` | ✅ | Lens chính — Design System, token, accessibility, component inventory |
| `architect` | ✅ | Ràng buộc kỹ thuật: ADR-001 stack, điều 8 wrap tiếng Việt, typeset layer (ADR-013), SPA + polling 2s |
| `business-analyst` | ✅ | Liệt kê **surface UI thật** từ 11 UC + NFR liên quan UI/a11y/i18n trong SRS + khoảng trống persona |
| `context-auditor` | ❌ | `040-Design/` trống ⇒ **không có gì để audit**. Shape A không bắt buộc inventory. Vai trò của nó dồn về Bước 6 (verify). |
| `researcher` | ❌ | Repo **đã có** `Analysis-Market-Competitor-Landscape.md` + `Analysis-Comic-Studio-Concept.md` làm neo thị trường. Web research về *"brand cho comic SaaS"* cho ra kết quả generic, dễ thành ảo giác có vẻ uy tín. **Escalate lên nếu** gate thấy Brand Guidelines thiếu căn cứ thị trường. |
| `quality-assurance` | ❌ | Run này không sinh acceptance criteria kiểm chứng được. Bước 6 dùng `context-auditor`. |
