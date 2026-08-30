---
id: INDEX-000
type: index
status: live
project: comic-studio
created: 2026-08-23
updated: 2026-08-30
---

# 📚 Documentation Master Index — comic-studio

> **Trang chủ của kho tài liệu.** Đây là **lớp điều hướng một cấp**: Index trỏ tới MOC, MOC trỏ tới tài liệu. Nội dung chi tiết không được copy lên đây — copy là tạo ra hai bản phải đồng bộ.
>
> Cấu trúc thư mục tuân theo [RULE-001 — Quy tắc Cấu trúc Tài liệu](../knowledge-base/99-Templates/Documents-Template.md).

## Mục lục

- [Dự án là gì](#dự-án-là-gì)
- [Bắt đầu từ đâu](#bắt-đầu-từ-đâu)
- [Bản đồ theo tầng Dewey](#bản-đồ-theo-tầng-dewey)
- [Run-state của PM](#run-state-của-pm)
- [Contract & quy ước](#contract--quy-ước)
- [Nợ kỹ thuật đã biết](#nợ-kỹ-thuật-đã-biết)

---

## Dự án là gì

`comic-studio` — nền tảng **SaaS thương mại multi-tenant** cho phép tác giả **tự upload truyện chữ của họ** và sinh ra comic pages, với Story Bible + Timeline State + Canonical References + Visual Prompt Compiler + Continuity Checker làm phần lõi.

| | |
|---|---|
| **Quy mô đội** | 1 người + AI assist |
| **Trạng thái** | Chưa có dòng code nào — đang ở giai đoạn planning |
| **Verdict thẩm định** | Khả thi có điều kiện — **chín điều kiện phải thoả đồng thời** |
| **Chặn lớn nhất** | Ba câu hỏi pháp lý về NĐ 134/2026 phải mang tới luật sư SHTT **trước khi thương mại hoá** |

---

## Bắt đầu từ đâu

Đọc theo đúng thứ tự này nếu anh (hoặc một agent) mới vào dự án:

| # | Tài liệu | Vì sao đọc |
|---|---|---|
| 1 | [Analysis-Comic-Studio-Concept](./050-Research/Analysis-Comic-Studio-Concept.md) | Thẩm định ý tưởng — 4 verdict, 9 điều kiện khả thi, 7 vấn đề phải sửa trước dòng code đầu tiên, unit economics. **Đọc cái này trước tất cả.** |
| 2 | [Charter-Comic-Studio](./010-Planning/Charter-Comic-Studio.md) | Mục tiêu, phạm vi, RACI, ràng buộc |
| 3 | [MVP-Scope](./010-Planning/MVP-Scope.md) | Ranh giới MVP vs Full Scope + ba gate Go/No-Go |
| 4 | [Roadmap](./010-Planning/Roadmap.md) · [OKRs](./010-Planning/OKRs.md) | Khi nào làm gì, và đo bằng gì |
| 5 | [Risk-Register](./010-Planning/Risk-Register.md) | Cái gì có thể giết dự án, và dấu hiệu nhận biết sớm |
| 6 | [Analysis-Market-Competitor-Landscape](./050-Research/Analysis-Market-Competitor-Landscape.md) | Thị trường, đối thủ, mô hình kinh doanh |
| — | [Request.md](./999-Resources/Request.md) | Concept gốc 894 dòng — kiến trúc 18 mục. Là **input** của mục 1, không phải kết luận |

---

## Bản đồ theo tầng Dewey

### 010 · Planning — [Planning-MOC](./010-Planning/Planning-MOC.md)

| Tài liệu | Nội dung |
|---|---|
| [Charter-Comic-Studio](./010-Planning/Charter-Comic-Studio.md) | Mục tiêu, phạm vi, Stakeholder Matrix (RACI), constraints |
| [Roadmap](./010-Planning/Roadmap.md) | Lộ trình 09/2026 → 02/2027 |
| [OKRs](./010-Planning/OKRs.md) | Q4/2026 + preview Q1/2027 |
| [Risk-Register](./010-Planning/Risk-Register.md) | Rủi ro + mitigation + trigger |
| [MVP-Scope](./010-Planning/MVP-Scope.md) | Ranh giới MVP vs Full Scope, Go/No-Go |

Thư mục con: `Sprints/` · `Estimates/` · `Implementation-Plans/` — *(chưa có tài liệu)*

### 020 · Requirements — [Requirements-MOC](./020-Requirements/Requirements-MOC.md)

**21 tài liệu.** Trục phân rã: **8 module `A–H`** lấy nguyên từ [MVP-Scope §3](./010-Planning/MVP-Scope.md), quan hệ **1 module ↔ 1 BRD ↔ 1 Epic** là 1:1:1.

| Tài liệu | Nội dung |
|---|---|
| [PRD-Comic-Studio](./020-Requirements/PRD-Comic-Studio.md) | Yêu cầu sản phẩm theo 8 module, ranh giới scope, success metrics. ⚠️ Mục *Người dùng & vấn đề* mở bằng `TBD` — repo **không có persona/JTBD** |
| [SRS-Comic-Studio](./020-Requirements/SRS-Comic-Studio.md) | Yêu cầu kỹ thuật + 17 NFR có số + 14 NFR `TBD` + mục **negative requirements** |
| `BRD/` — **8 file** | Một BRD cho mỗi module: [001 Pipeline sinh ảnh](./020-Requirements/BRD/BRD-001-Image-Generation-Pipeline.md) · [002 Story Intelligence](./020-Requirements/BRD/BRD-002-Story-Intelligence.md) · [003 Comic Director](./020-Requirements/BRD/BRD-003-Comic-Director-And-Layout.md) · [004 Editor](./020-Requirements/BRD/BRD-004-Minimum-Editor.md) · [005 Multi-tenancy](./020-Requirements/BRD/BRD-005-Multi-Tenancy-And-Platform.md) · [006 Credit](./020-Requirements/BRD/BRD-006-Credit-And-Unit-Economics.md) · [007 Pháp lý](./020-Requirements/BRD/BRD-007-Legal-And-Compliance.md) · [008 Chất lượng](./020-Requirements/BRD/BRD-008-Quality-And-Operations.md) |
| `Use-Cases/` — **11 file** | `UC-01`…`UC-11`: upload chapter → Story Bible → hai human gate → sinh trang → chọn panel → edit bubble → xếp trang → export → credit/BYOK → takedown. **Không UC nào có Exception flow rỗng** |

### 022 · User Stories — [Stories-MOC](./022-User-Stories/Stories-MOC.md)

**50 tài liệu**: 8 Epic (1:1 với module `A–H`) + 41 User Story trong horizon + 1 backlog đã xếp ưu tiên.

| Tài liệu | Nội dung |
|---|---|
| [Backlog-Priority](./022-User-Stories/Backlog-Priority.md) | **51 hàng** = 41 Story có file + 10 ngoài horizon. Framework **`UNLOCK-ORDER`** — **không** phải RICE/MoSCoW (cả hai bị bác tại gate: RICE cần `Reach`/`Confidence` mà sản phẩm chưa có người dùng không thể chấm; MoSCoW trùng vai với `MVP-Scope §3`) |
| `Epics/` — **8 file** | [Pipeline sinh ảnh](./022-User-Stories/Epics/Epic-Image-Generation-Pipeline.md) · [Story Intelligence](./022-User-Stories/Epics/Epic-Story-Intelligence.md) · [Comic Director](./022-User-Stories/Epics/Epic-Comic-Director-And-Layout.md) · [Editor](./022-User-Stories/Epics/Epic-Minimum-Editor.md) · [Multi-tenancy](./022-User-Stories/Epics/Epic-Multi-Tenancy-And-Platform.md) · [Credit](./022-User-Stories/Epics/Epic-Credit-And-Unit-Economics.md) · [Pháp lý](./022-User-Stories/Epics/Epic-Legal-And-Compliance.md) · [Chất lượng](./022-User-Stories/Epics/Epic-Quality-And-Operations.md) |
| `Backlog/` — **41 file** | `STORY-A-01`…`STORY-H-06`. AC là **checklist 4 khối, không Gherkin**; `Small` neo vào **giờ-người** (`E_build ≤ 16h`, `E_hitl ≤ 2h/chapter`); INVEST **không áp** cho 5 Story `[MVP0]` |
| `Active-Sprint/` | *(chưa có tài liệu; chưa có sprint nào chạy)* |

> **`Backlog-Priority` KHÔNG phải nguồn sự thật thứ tư về thời gian.** Nó trả lời *"trong một mốc đã cho, Story nào làm trước"*; [Roadmap](./010-Planning/Roadmap.md) sở hữu *"mốc nào đến khi nào"*. Lệch nhau ⇒ **sửa hàng backlog, không sửa Roadmap**. File này có guardrail cơ học: `grep` thấy bất kỳ ngày tháng nào trong đó là **đã drift**.

### 030 · Specs — [Specs-MOC](./030-Specs/Specs-MOC.md)

⭐ **57 tài liệu** — sản phẩm của **SDLC Phase 2 — Architecture Design**. Trạng thái: **53 `draft`** + ⭐ **4 `accepted`** (`ADR-001`…`ADR-004`, duyệt ở run `2026-08-30-dong-bo-srs-nfr-voi-adr`) *(đếm cơ học `grep -rln '^status: accepted' docs/030-Specs/` ngày 2026-08-30, ⛔ không trích lại)*.

| Nhóm | Số file | Nội dung |
|---|:--:|---|
| `Architecture/` | **19** | 1 SDD (5 sơ đồ Mermaid) + 18 ADR. ⭐ `SDD` §6.3 `SDD-HG-01` là **nguồn duy nhất** của *"không đường nào bypass hai human gate"*; `ADR-017` là **nguồn duy nhất** của `KC-4` |
| `Schema/` | **14** | `DB-Entity-*`, mỗi file có **ER diagram Mermaid**, invariant và RLS policy. `TEXT` + `CHECK` toàn tầng, ⛔ không Postgres enum type |
| `API/` | **21** | 14 `Endpoint-*` (tiền tố `/v1/`) + 7 `Spec-Integration-*` |
| `Security/` | **3** | Threat model · cô lập tenant · tuân thủ pháp lý. ⭐ Đã qua **review độc lập** (lô `L31`), ⛔ không phải tự tác giả duyệt |

> ⚠️ **`SRS-NFR-15` là anti-feature CHỐT**: hệ thống **KHÔNG được** có copyright / similarity detection — nó **tự phá miễn trừ Điều 198b**. Lý do đầy đủ ở [Spec-Security-Legal-Compliance](./030-Specs/Security/Spec-Security-Legal-Compliance.md).

### 035 · QA — [QA-MOC](./035-QA/QA-MOC.md)

*(chưa có tài liệu)* — thư mục con `Test-Plans/`, `Test-Cases/`, `Automation/`, `Reports/`, `Performance/` đã sẵn sàng.

### 040 · Design — [Design-MOC](./040-Design/Design-MOC.md)

⭐ **6 tài liệu** — sản phẩm của **SDLC Phase 3 — Product Design** (run `2026-08-30`). Toàn bộ `status: draft`.

| Tài liệu | Nội dung |
|---|---|
| [Foundations](./040-Design/Design-System/Foundations.md) | ⭐ **Đọc trước tiên.** Hợp đồng phát biểu token — **CSS variable là NGUỒN, Tailwind THAM CHIẾU**, một chiều. Kèm **checklist 14 mục `grep`** dùng nghiệm thu cơ học 5 file kia |
| [Brand-Guidelines](./040-Design/Design-System/Brand-Guidelines.md) | Tone, hướng màu, 4 actor có căn cứ. ⚠️ **Tên hiển thị vẫn `TBD`** (chủ: Founder) — `comic-studio` là project name, ⛔ không phải tên sản phẩm |
| [Color-Tokens](./040-Design/Design-System/Color-Tokens.md) | 17 cặp semantic nền/chữ đủ 2 cột light/dark · **27 hàng audit contrast có số — cả 27 đều ĐẠT**; 3 màu cố ý không đạt 3:1 nằm ở **bảng tách biệt** kèm phạm vi hẹp |
| [Typography](./040-Design/Design-System/Typography.md) | ⭐ **HAI hệ font, token ⛔ KHÔNG chung namespace**: font UI là CSS variable ở `apps/web`; font render vào ảnh là **tham số config của `apps/api`**, phải **đơn trị** |
| [Spacing-And-Layout](./040-Design/Design-System/Spacing-And-Layout.md) | Thang spacing, radius, elevation, breakpoint, z-index đặt tên + ranh giới với hệ toạ độ **0–1** của `ADR-013` |
| [Components](./040-Design/Design-System/Components.md) | 16 component không hoãn được `C-01`…`C-16` + ma trận state + **mục CẤM 8 hàng** |

> ⚠️ **Phase 3 CHƯA đóng — đạt 1/4 tiêu chí chuyển Phase.** Run `2026-08-30` cố ý chỉ làm bộ nền. `Wireframes/`, `Specs/` (User Flow + UI Spec), `Assets/` **chưa có tài liệu**, thuộc run sau.

> ⭐ **Ba ràng buộc xuyên suốt của tầng này**: (1) **hai hệ font ⛔ không được gộp** — gộp thì hỏng im lặng, chỉ lộ **sau khi đã sinh ảnh và tốn tiền**; (2) ⛔ **không có component bulk approve** (`API-HG-6` + `SDD-HG-01.1`); (3) **AI-disclosure indicator là BẮT BUỘC** (`SRS-FR-40`, CHỐT) — bằng chứng tuân thủ chỉ tồn tại dưới dạng UI.

### 050 · Research — [Research-MOC](./050-Research/Research-MOC.md)

| Tài liệu | Nội dung |
|---|---|
| [Analysis-Comic-Studio-Concept](./050-Research/Analysis-Comic-Studio-Concept.md) | Thẩm định ý tưởng — tài liệu nền tảng của cả dự án |
| [Analysis-Market-Competitor-Landscape](./050-Research/Analysis-Market-Competitor-Landscape.md) | TAM/SAM/SOM, đối thủ, pricing, retention, kênh phân phối |

Thư mục con: `Competitor-Analysis/` · `User-Interviews/` · `Surveys/` — *(chưa có tài liệu)*

### 060 · Manuals — [Manuals-MOC](./060-Manuals/Manuals-MOC.md)

*(chưa có tài liệu)* — `User-Guide/`, `Admin-Guide/` đã sẵn sàng.

### 070 · Deployment — [Deployment-MOC](./070-Deployment/Deployment-MOC.md)

*(chưa có tài liệu)* — `Releases/`, `Runbooks/` đã sẵn sàng.

### 080 · Operations — [Operations-MOC](./080-Operations/Operations-MOC.md)

*(chưa có tài liệu)* — `Incidents/`, `SLAs/` đã sẵn sàng.

### 090 · Archive

`docs/090-Archive/` — *(rỗng)*. Tài liệu bị thay thế chuyển vào đây với `status: deprecated`. **Không bao giờ xoá tài liệu.**

### 999 · Resources — [Resources-MOC](./999-Resources/Resources-MOC.md)

| Mục | Nội dung |
|---|---|
| [Glossary](./999-Resources/Glossary.md) | **123 thuật ngữ, 11 nhóm** *(đếm cơ học `grep -c '^- \*\*'` ngày 2026-08-30, ⛔ không trích lại)* — kiến trúc pipeline, mô hình dữ liệu, sinh ảnh, SaaS & multi-tenancy, requirements & tài liệu hoá, backlog & story engineering, **Design System & thương hiệu** (33 mục thêm ở Phase 3)… |
| [Request.md](./999-Resources/Request.md) | Concept gốc 894 dòng |
| `Meeting-Notes/` | *(chưa có tài liệu)* |

**`Templates/` — 13 khuôn** *(chưa MOC nào liệt kê chúng; index hoá tại đây)*:

[Analysis](./999-Resources/Templates/Template-Analysis.md) ⚠️stub · [Component](./999-Resources/Templates/Template-Component.md) · [Incident-Report](./999-Resources/Templates/Template-Incident-Report.md) · [PRD](./999-Resources/Templates/Template-PRD.md) · [Project-Charter](./999-Resources/Templates/Template-Project-Charter.md) · [Release-Notes](./999-Resources/Templates/Template-Release-Notes.md) · [Risk-Register](./999-Resources/Templates/Template-Risk-Register.md) · [SDD](./999-Resources/Templates/Template-SDD.md) · [Spec](./999-Resources/Templates/Template-Spec.md) · [SRS](./999-Resources/Templates/Template-SRS.md) · [Status-Report](./999-Resources/Templates/Template-Status-Report.md) · [Test-Plan](./999-Resources/Templates/Template-Test-Plan.md) · [WBS-ETA](./999-Resources/Templates/Template-WBS-ETA.md)

---

## Run-state của PM

[`010-Planning/pm-runs/`](./010-Planning/pm-runs/README.md) — sổ tay điều phối của `/pm-code` và `/pm-doc`. **Không phải deliverable**, và **không được chuẩn hoá** — nó là dấu vết quyết định tại thời điểm chạy.

| Run | Nội dung |
|---|---|
| `2026-08-23-danh-gia-y-tuong-comic-studio` | Thẩm định ý tưởng → sinh ra [Analysis-Comic-Studio-Concept](./050-Research/Analysis-Comic-Studio-Concept.md) |
| `2026-08-23-khoi-tao-tai-lieu-planning-comic-studio` | Khởi tạo 7 artifact planning → sinh ra toàn bộ tầng 010-Planning + cấu trúc Dewey + file này |
| `2026-08-24-khoi-tao-requirements-stories-comic-studio` | Khởi tạo tầng 020-Requirements (21 tài liệu) + tầng 022-User-Stories (50 tài liệu) + 15 thuật ngữ Glossary. **72 deliverable, 20 lô writer** |
| `2026-08-28-phase-2-architecture-design-comic-studio` | Phase 2 — Architecture Design → toàn bộ tầng [030-Specs](./030-Specs/Specs-MOC.md) (57 tài liệu). **46 lô writer** |
| `2026-08-30-brand-guidelines-va-design-system-comic-studio` | Phase 3 (phần nền) — [Brand Guidelines + Design System](./040-Design/Design-MOC.md) (6 tài liệu) + `Design-MOC` viết từ số 0 + 33 thuật ngữ Glossary. **5 lô writer**, 4 quyết định `G-1`…`G-4` của Founder tại gate |
| `2026-08-30-dong-bo-srs-nfr-voi-adr` | ⭐ Đồng bộ lệch tầng **020 ↔ 030** — `SRS-NFR-07`/`08`/`09` hạ khỏi `CHƯA QUYẾT` theo `ADR-001`…`ADR-004`; 4 ADR đó chuyển `accepted`. **21 điểm ở `SRS` + 15 điểm ripple nội dung tầng 030 + 4 ADR chuyển `accepted` + 4 điểm MOC/Index** *(đếm cơ học từ `git diff` ngày 2026-08-30, ⛔ không trích lại)*. **3 lô writer** + 2 pass verify. ⚠️ Đọc [`escalations.md` `E1`](./010-Planning/pm-runs/2026-08-30-dong-bo-srs-nfr-voi-adr/escalations.md) **trước khi** báo `ADR-001:16`/`:173` là lỗi — chúng ⛔ không phải lỗi |

---

## Contract & quy ước

| Tài liệu | Vai trò |
|---|---|
| [Documents-Template (RULE-001)](../knowledge-base/99-Templates/Documents-Template.md) | **Contract bắt buộc** — Document Type Mapping, cấu trúc Dewey, frontmatter, linking rules, validation checklist |
| [Knowledge Base Index](../knowledge-base/00-Index.md) | Chỉ mục của knowledge-base |

**Hai quy ước hay bị vi phạm nhất:**
1. Mọi tài liệu **phải** có YAML frontmatter đủ `id / type / status / created`.
2. Liên kết dùng **standard markdown link relative path** `[Text](./path.md)` — **KHÔNG** dùng wiki-link `[[...]]`.

---

## Nợ kỹ thuật đã biết

Ghi ở đây để minh bạch thay vì che giấu.

### Từ Phase 2 — Architecture Design

| # | Nợ | Mức | Chủ |
|---|---|---|---|
| **1** | ⭐ **`T-27` — lưu / mã hoá / THU HỒI API key BYOK của khách.** Lưu credential của **bên thứ ba** là hạng mục rủi ro cao nhất hệ thống. Seam phải có sớm (`SRS-FR-32` **cấm retrofit bằng chữ**) nhưng cơ chế thì ⛔ chưa có requirement nguồn ⇒ **cần một ADR mới** | **Cao** | Architect + Founder |
| **2** | ⭐ **Role thứ năm `app_operator` chưa có trong `SDD` §7.4 và `ADR-006`.** Hai endpoint admin takedown (`TD-2`/`TD-3`) là **xuyên tenant** và ⚠️ **đang BỊ CHẶN** cho tới khi mô hình quyền được sửa. Đây là **thay đổi mô hình quyền**, ⛔ không phải ripple tài liệu | **Cao** | Architect |
| **3** | `T-29` — nội dung/hình thức/thời hạn **thông báo cho tenant bị takedown**. ⚠️ Chính bước đó là **điều kiện tối thiểu để counter-notice tồn tại** | Cao | Founder + luật sư |
| **4** | ⚠️ **4 khoảng trống pháp lý** (`GAP-1`…`GAP-4`) — để dạng **câu hỏi cho luật sư**, ⛔ **không** phải rủi ro đã đánh giá. `GAP-3` là **chân đỡ** của cả lập luận `SRS-NFR-15` | Cao | PM + luật sư SHTT |
| **5** | `T-GEN-CL-ENQUEUE` — `SDD` §5.2 `F5` vẽ `INSERT change_log` lúc enqueue, nhưng danh mục `action_type` (**đóng**) ⛔ không có giá trị nào mang nghĩa *"ra lệnh generate"* | Trung bình | Architect + BA |
| **6** | Chuẩn `error_code` + error envelope cho 14 file API (`TBD-API-ENV`) — casing còn lẫn `UPPER_SNAKE`/`lower_snake` | Trung bình | Architect |
| **7** | `INV-14` có nên nâng lên `CHECK` liên cột không — PM ⛔ **không tái lập được** lý do worker nêu; xem [`E25`](./010-Planning/pm-runs/2026-08-28-phase-2-architecture-design-comic-studio/escalations.md) | Thấp | Architect |
| **8** | Còn **1 anchor gãy cứng + ~29 gãy mềm** ở `Architecture/` và `Schema/` (lô vá chỉ được cấp `API/` + `Security/`) | Thấp | — |

### Từ Phase 3 — Product Design (run `2026-08-30`)

| # | Nợ | Mức | Chủ |
|---|---|---|---|
| **1** | ⭐ **Tên hiển thị thương mại vẫn `TBD`.** `comic-studio` là **project name** (`Charter` §1), ⛔ không phải tên sản phẩm. Chặn dây chuyền: wordmark · favicon · microcopy · logo của bề mặt takedown công khai | **Cao** | Founder |
| **2** | ~~⚠️ **`ADR-013` mới nêu họ font + glyph coverage, CHƯA nêu hai ràng buộc sau** (license nhúng server-side · metric ổn định + pin version) — chỉ tồn tại ở tầng 040~~ ✅ **ĐÓNG** ở **2026-08-30** (lô đồng bộ `ADR-013`, ⛔ không phải một pm-run — ⛔ không có thư mục run-state): [ADR-013](./030-Specs/Architecture/ADR-013-Typeset-Layer-Separate-From-Art.md) nay có §*Bốn ràng buộc* đủ **`R-1`…`R-4`**, cross-link hai chiều với [Typography](./040-Design/Design-System/Typography.md) và ghi rõ **ADR-013 là nguồn sở hữu**. ⚠️ **Phần CHƯA đóng và ⛔ KHÔNG đóng được hôm nay: giá trị font cụ thể** — `ADR-013` chốt chủ là **Architect + Founder, sau MVP0, trước `G1-e`**; chọn trước khi có số đo là vi phạm chính `ADR-001`. ⭐ Ràng buộc khó nhất là **`R-4`**: đổi version font hỏng **im lặng**, ⛔ **không trigger nào bắt được** ⇒ pin version là hạng mục **Dockerfile** | **Cao** *(còn lại: chọn font, sau MVP0)* | Architect + Founder |
| **3** | ~~⚠️ **`ADR-013` ⛔ không cross-link tới `T-PL-BUDGET-UNIT`**, và ⛔ **không tài liệu nào nói ra thứ tự đóng hai `TBD`**~~ ✅ **ĐÓNG** ở **2026-08-30** (lô đồng bộ `ADR-013`, ⛔ không phải một pm-run — ⛔ không có thư mục run-state). Thứ tự đã chốt: ⭐ **`TBD-FONT` TRƯỚC, `T-PL-BUDGET-UNIT` SAU** — vì **hàm tính** `text_budget` từ diện tích phụ thuộc **metric của font** *(riêng phần **đơn vị** ký tự/từ thì ⛔ không phụ thuộc, chốt độc lập được)*. Cross-link hai chiều `ADR-013` ↔ [`Endpoint-Page-Layout`](./030-Specs/API/Endpoint-Page-Layout.md) ↔ `Typography`. ⚠️ Lịch hiện tại (`G1-e` 09/2026 trước `M2-3` 01–02/2027) **đã đúng chiều phụ thuộc — do trùng hợp, ⛔ không do ai ràng buộc** | ~~Trung bình~~ **đóng** | Architect + BA |
| **4** | **Bảng 27 hàng audit contrast trong [Color-Tokens](./040-Design/Design-System/Color-Tokens.md) được tính TAY** theo công thức relative luminance WCAG (làm tròn xuống). ✅ Verify pass đã **tính lại độc lập 15/27 hàng** (chọn mọi hàng sát ngưỡng: 4.34 · 4.41 · 4.75 · 4.79 · 4.82) — **khớp delta 0.00, 0 sai ngưỡng**. Vẫn nên **chạy lại bằng công cụ tự động khi init** cho 12 hàng còn lại, màu chồng alpha, và text trên ảnh preview | Thấp *(hạ từ Trung bình sau verify)* | — |
| **5** | ~~⚠️ **`SRS-NFR-09` (tầng 020) vẫn ghi framework frontend `CHƯA QUYẾT → TBD`** trong khi `ADR-001` (tầng 030) đã chốt. Lệch tầng, cần run đồng bộ 020↔030~~ ✅ **ĐÓNG** ở run `2026-08-30-dong-bo-srs-nfr-voi-adr`. Phạm vi thật rộng hơn: **cả ba** `SRS-NFR-07`/`08`/`09` cùng lệch ⇒ đồng bộ chung. ⚠️ **Đọc kỹ**: `ADR-001` xếp `shadcn/ui + Tailwind` ở tầng **MẶC ĐỊNH**, ⛔ **không phải CHỐT** — nên `SRS` nay ghi nhãn **LAI**, ⛔ cố ý không ghi CHỐT. ⚠️ Đường lui của `ADR-001` chỉ có ở mức **đổi cả cụm frontend**; ⛔ **riêng UI kit chưa có đường lui lẫn alternatives** — nợ để mở có chủ đích, xem [`escalations.md` `E7` #2](./010-Planning/pm-runs/2026-08-30-dong-bo-srs-nfr-voi-adr/escalations.md) | ~~Trung bình~~ **đóng** | Architect + BA |
| **6** | ⚠️ **`UC-09`, `UC-10`, `UC-11` bị lọt tag XML** của tool call vào cuối file (`</content>`) | Thấp | — |
| **7** | Mâu thuẫn `X-1` — độ rắn `D-45` (polling 2s) đọc ra hai kiểu: `SRS`+`ADR-015` ghi **MẶC ĐỊNH**, `ADR-001` xếp dưới *"⛔ không mở lại"*. ⛔ Không chặn Design System (trạng thái mô tả theo `job_status`, ⛔ không theo chu kỳ polling) | Thấp | Architect |
| **9** | 🆕 ⭐ **51 anchor trong-file gãy + 8 link gãy trên toàn `docs/`** — phát hiện ngày `2026-08-30` bằng [`scripts/check-doc-anchors.py`](../scripts/check-doc-anchors.py) *(chạy `python3 scripts/check-doc-anchors.py docs`, ⛔ không trích lại số)*. ⭐ **Nguyên nhân gốc của 13/51**: anchor có **em-dash `—`** viết dạng `#hệ-1-—-font-ui`, nhưng `github-slugger` **loại bỏ** `—` (nằm trong dải `U+2000–U+206F`) ⇒ slug thật là `#hệ-1--font-ui` (**hai** gạch nối). ⚠️ Đây là **mở rộng của nợ Phase 2 #8** (*"1 anchor gãy cứng + ~29 gãy mềm"*) — nay đã **đo được toàn cây**, ⛔ không còn là ước lượng. 8 link gãy còn lại nằm ở `pm-runs/` (run-state, ⛔ không phải deliverable) và placeholder có chủ ý của `Manuals-MOC` / `Deployment-MOC` | Thấp — điều hướng, ⛔ không sai nội dung | — |
| **8** | ⛔ **Không có template cho Design System** trong `999-Resources/Templates/` (13 khuôn, ⛔ không khuôn nào hợp). 6 file Phase 3 tự dựng cấu trúc ⇒ nếu muốn tái dùng, cần rút một `Template-Design-System.md` | Thấp | — |

### Từ các run trước

| # | Nợ | Mức |
|---|---|---|
| 1 | ~~[Specs-MOC](./030-Specs/Specs-MOC.md)~~ ✅ **đã viết** ở Phase 2 (57 tài liệu, 0 link gãy). ~~[Design-MOC](./040-Design/Design-MOC.md) **vẫn là file 0 byte**~~ ✅ **đã viết** ở Phase 3 (run `2026-08-30`) | ~~Cao~~ **đóng** |
| 2 | [Request.md](./999-Resources/Request.md) **thiếu hoàn toàn YAML frontmatter** — vi phạm RULE-001 quy tắc #3 | Trung bình |
| 3 | Còn **link chết loại-file** trong một số MOC (trỏ tới tài liệu chưa được viết) | Thấp — là placeholder có chủ ý |
| 4 | Phần lớn MOC chỉ có link thư mục, **chưa có mô tả nội dung** | Thấp |

> Link chết trỏ tới **thư mục** đã được gỡ trong run `2026-08-23-khoi-tao-tai-lieu-planning-comic-studio` bằng việc tạo đủ 32 thư mục Dewey còn thiếu.
