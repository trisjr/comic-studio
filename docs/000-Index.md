---
id: INDEX-000
type: index
status: live
project: comic-studio
created: 2026-08-23
updated: 2026-08-23
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

*(chưa có tài liệu)* — thư mục con `BRD/`, `Use-Cases/` đã sẵn sàng.

### 022 · User Stories — [Stories-MOC](./022-User-Stories/Stories-MOC.md)

*(chưa có tài liệu)* — thư mục con `Epics/`, `Active-Sprint/`, `Backlog/` đã sẵn sàng.

### 030 · Specs — [Specs-MOC](./030-Specs/Specs-MOC.md)

⚠️ **MOC hiện là file rỗng 0 byte** — chưa dùng được, xem [Nợ kỹ thuật](#nợ-kỹ-thuật-đã-biết).
*(chưa có tài liệu)* — thư mục con `Architecture/`, `API/`, `Schema/`, `Security/` đã sẵn sàng.

### 035 · QA — [QA-MOC](./035-QA/QA-MOC.md)

*(chưa có tài liệu)* — thư mục con `Test-Plans/`, `Test-Cases/`, `Automation/`, `Reports/`, `Performance/` đã sẵn sàng.

### 040 · Design — [Design-MOC](./040-Design/Design-MOC.md)

⚠️ **MOC hiện là file rỗng 0 byte** — chưa dùng được.
*(chưa có tài liệu)* — thư mục con `Wireframes/`, `Design-System/`, `Specs/`, `Assets/` đã sẵn sàng.

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
| [Glossary](./999-Resources/Glossary.md) | 40 thuật ngữ, 7 nhóm — kiến trúc pipeline, mô hình dữ liệu, sinh ảnh, SaaS & multi-tenancy… |
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

Ghi ở đây để minh bạch thay vì che giấu. Cả bốn mục thuộc một run `/pm-doc` **Shape B** riêng, không phải run nào ở trên.

| # | Nợ | Mức |
|---|---|---|
| 1 | [Specs-MOC](./030-Specs/Specs-MOC.md) và [Design-MOC](./040-Design/Design-MOC.md) là **file 0 byte** — không có cả frontmatter | Cao |
| 2 | [Request.md](./999-Resources/Request.md) **thiếu hoàn toàn YAML frontmatter** — vi phạm RULE-001 quy tắc #3 | Trung bình |
| 3 | Còn **link chết loại-file** trong một số MOC (trỏ tới tài liệu chưa được viết) | Thấp — là placeholder có chủ ý |
| 4 | Phần lớn MOC chỉ có link thư mục, **chưa có mô tả nội dung** | Thấp |

> Link chết trỏ tới **thư mục** đã được gỡ trong run `2026-08-23-khoi-tao-tai-lieu-planning-comic-studio` bằng việc tạo đủ 32 thư mục Dewey còn thiếu.
