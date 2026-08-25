---
id: MOC-STORIES
type: moc
status: live
created: 2026-02-04
updated: 2026-08-24
---

# 📂 022-User-Stories Map of Content

Tầng thực thi của kho tài liệu: **8 Epic** (nhóm tính năng, 1:1 với module `A–H`) → **41 User Story** trong horizon → **1 backlog đã xếp ưu tiên**.

> **Ranh giới quan trọng nhất của tầng này**: [Backlog-Priority](./Backlog-Priority.md) trả lời *"trong một mốc đã cho, Story nào làm trước"*. Nó **không** trả lời *"mốc nào đến khi nào"* — đó là [Roadmap](../010-Planning/Roadmap.md), và khi hai bên lệch nhau thì **`Roadmap` thắng tuyệt đối**: sửa hàng backlog, không sửa Roadmap.

## 🎯 Backlog đã xếp ưu tiên

| Tài liệu | Nội dung |
|---|---|
| [Backlog-Priority](./Backlog-Priority.md) | **51 hàng** = 41 Story có file + 10 Story ngoài horizon (`chưa có file`). Framework **`UNLOCK-ORDER`**, không phải RICE/MoSCoW — xem ghi chú dưới. Đánh dấu MVP Story bằng `⭐` theo quy tắc **suy ra được từ cột**, viết thành văn trong chính file. |

> ⚠️ **Yêu cầu gốc của Founder viết *"(RICE/MoSCoW)"*; cả hai framework đó đã bị bác tại gate** và thay bằng `UNLOCK-ORDER`. Lý do: RICE cần `Reach` và `Confidence` — hai đại lượng mà một sản phẩm **chưa có người dùng nào** không thể chấm mà không bịa; MoSCoW thì trùng vai với `MVP-Scope §3`, vốn **đã** phân loại xong từng hạng mục theo mốc. `UNLOCK-ORDER` xếp hạng theo *"cái gì mở khoá cái gì"* — hỏi đúng câu hỏi mà một backlog trong nội bộ một mốc cần trả lời.

## 📚 Epic (8) — 1:1 với module `MVP-Scope §3`

| Epic | Module | BRD cha | Story trong horizon |
|---|---|---|--:|
| [Epic-Image-Generation-Pipeline](./Epics/Epic-Image-Generation-Pipeline.md) | A · Pipeline sinh ảnh | [BRD-001](../020-Requirements/BRD/BRD-001-Image-Generation-Pipeline.md) | 5 |
| [Epic-Story-Intelligence](./Epics/Epic-Story-Intelligence.md) | B · Story Intelligence | [BRD-002](../020-Requirements/BRD/BRD-002-Story-Intelligence.md) | 4 |
| [Epic-Comic-Director-And-Layout](./Epics/Epic-Comic-Director-And-Layout.md) | C · Comic Director & Layout | [BRD-003](../020-Requirements/BRD/BRD-003-Comic-Director-And-Layout.md) | 7 |
| [Epic-Minimum-Editor](./Epics/Epic-Minimum-Editor.md) | D · Editor & UI | [BRD-004](../020-Requirements/BRD/BRD-004-Minimum-Editor.md) | 5 |
| [Epic-Multi-Tenancy-And-Platform](./Epics/Epic-Multi-Tenancy-And-Platform.md) | E · Multi-tenancy & hạ tầng | [BRD-005](../020-Requirements/BRD/BRD-005-Multi-Tenancy-And-Platform.md) | 5 |
| [Epic-Credit-And-Unit-Economics](./Epics/Epic-Credit-And-Unit-Economics.md) | F · Kinh tế & credit | [BRD-006](../020-Requirements/BRD/BRD-006-Credit-And-Unit-Economics.md) | 3 |
| [Epic-Legal-And-Compliance](./Epics/Epic-Legal-And-Compliance.md) | G · Pháp lý & compliance | [BRD-007](../020-Requirements/BRD/BRD-007-Legal-And-Compliance.md) | 6 |
| [Epic-Quality-And-Operations](./Epics/Epic-Quality-And-Operations.md) | H · Chất lượng & vận hành | [BRD-008](../020-Requirements/BRD/BRD-008-Quality-And-Operations.md) | 6 |

## 📝 User Story (41) — [`Backlog/`](./Backlog/)

### A · Pipeline sinh ảnh
| id | Story |
|---|---|
| `STORY-A-01` | [Story-Generate-Panel-With-Reference-And-VLM-Select](./Backlog/Story-Generate-Panel-With-Reference-And-VLM-Select.md) |
| `STORY-A-02` | [Story-Typeset-Layer-And-Bubble-Overlay](./Backlog/Story-Typeset-Layer-And-Bubble-Overlay.md) |
| `STORY-A-03` | [Story-Deterministic-Visual-Prompt-Compiler](./Backlog/Story-Deterministic-Visual-Prompt-Compiler.md) |
| `STORY-A-04` | [Story-Image-Provider-Adapter](./Backlog/Story-Image-Provider-Adapter.md) |
| `STORY-A-05` | [Story-Job-Queue-In-Postgres](./Backlog/Story-Job-Queue-In-Postgres.md) |

### B · Story Intelligence
| id | Story |
|---|---|
| `STORY-B-01` | [Story-Fix-Narrative-Time-Key](./Backlog/Story-Fix-Narrative-Time-Key.md) |
| `STORY-B-02` | [Story-Chapter-Ingest-And-Text-Clean](./Backlog/Story-Chapter-Ingest-And-Text-Clean.md) |
| `STORY-B-03` | [Story-Story-Bible-Extraction](./Backlog/Story-Story-Bible-Extraction.md) |
| `STORY-B-04` | [Story-Timeline-State-Resolver](./Backlog/Story-Timeline-State-Resolver.md) |

### C · Comic Director & Layout
| id | Story |
|---|---|
| `STORY-C-01` | [Story-Comic-IR-Panel-Specification](./Backlog/Story-Comic-IR-Panel-Specification.md) |
| `STORY-C-02` | [Story-Auto-Director-Scene-To-Page-Panel](./Backlog/Story-Auto-Director-Scene-To-Page-Panel.md) |
| `STORY-C-03` | [Story-Layout-Rubric-Beat-Type-And-Emphasis-Quota](./Backlog/Story-Layout-Rubric-Beat-Type-And-Emphasis-Quota.md) |
| `STORY-C-04` | [Story-Enforce-Max-Three-Characters-Per-Panel](./Backlog/Story-Enforce-Max-Three-Characters-Per-Panel.md) |
| `STORY-C-05` | [Story-Text-Safe-Zone-In-Panel-Spec](./Backlog/Story-Text-Safe-Zone-In-Panel-Spec.md) |
| `STORY-C-06` | [Story-Human-Gate-Speaker-Attribution](./Backlog/Story-Human-Gate-Speaker-Attribution.md) |
| `STORY-C-07` | [Story-Human-Gate-Dialogue-Condensation](./Backlog/Story-Human-Gate-Dialogue-Condensation.md) |

### D · Editor & UI
| id | Story |
|---|---|
| `STORY-D-01` | [Story-Story-Bible-Editor-Form](./Backlog/Story-Story-Bible-Editor-Form.md) |
| `STORY-D-02` | [Story-Change-Log-On-Every-Editor-Action](./Backlog/Story-Change-Log-On-Every-Editor-Action.md) |
| `STORY-D-03` | [Story-Page-Template-Layout-And-Swap-Panel](./Backlog/Story-Page-Template-Layout-And-Swap-Panel.md) |
| `STORY-D-04` | [Story-Server-Side-Page-And-Chapter-Preview](./Backlog/Story-Server-Side-Page-And-Chapter-Preview.md) |
| `STORY-D-05` | [Story-Bubble-Text-Overlay-Editor](./Backlog/Story-Bubble-Text-Overlay-Editor.md) |

### E · Multi-tenancy & hạ tầng
| id | Story |
|---|---|
| `STORY-E-01` | [Story-Tenant-Id-And-RLS-Everywhere](./Backlog/Story-Tenant-Id-And-RLS-Everywhere.md) |
| `STORY-E-02` | [Story-Tenant-User-Membership-As-Three-Entities](./Backlog/Story-Tenant-User-Membership-As-Three-Entities.md) |
| `STORY-E-03` | [Story-Per-Tenant-Object-Storage-No-Cross-Dedup](./Backlog/Story-Per-Tenant-Object-Storage-No-Cross-Dedup.md) |
| `STORY-E-04` | [Story-Buy-Authentication-Provider](./Backlog/Story-Buy-Authentication-Provider.md) |
| `STORY-E-05` | [Story-Modular-Monolith-Three-Schemas](./Backlog/Story-Modular-Monolith-Three-Schemas.md) |

### F · Kinh tế & credit
| id | Story |
|---|---|
| `STORY-F-01` | [Story-Usage-Event-And-Daily-Rollup](./Backlog/Story-Usage-Event-And-Daily-Rollup.md) |
| `STORY-F-02` | [Story-Generation-Cost-And-Model-Metadata](./Backlog/Story-Generation-Cost-And-Model-Metadata.md) |
| `STORY-F-03` | [Story-Tier-1-Sellable-Without-Image-Gen](./Backlog/Story-Tier-1-Sellable-Without-Image-Gen.md) |

### G · Pháp lý & compliance
| id | Story |
|---|---|
| `STORY-G-01` | [Story-Provenance-Chain-Parent-Generation](./Backlog/Story-Provenance-Chain-Parent-Generation.md) |
| `STORY-G-02` | [Story-Provenance-Committed-In-Same-Transaction](./Backlog/Story-Provenance-Committed-In-Same-Transaction.md) |
| `STORY-G-03` | [Story-Opt-Out-Check-At-Ingest](./Backlog/Story-Opt-Out-Check-At-Ingest.md) |
| `STORY-G-04` | [Story-ToS-User-Warrant-And-Tenant-Hard-Delete](./Backlog/Story-ToS-User-Warrant-And-Tenant-Hard-Delete.md) |
| `STORY-G-05` | [Story-Safe-Harbour-Checklist-Article-198b](./Backlog/Story-Safe-Harbour-Checklist-Article-198b.md) |
| `STORY-G-06` | [Story-AI-Disclosure-Article-11](./Backlog/Story-AI-Disclosure-Article-11.md) |

> ⚠️ **Hai văn bản pháp lý cùng số 134 — KHÔNG được trộn.** `Luật số 134/2025/QH15` (Điều 11 · **khoản 4 Điều 11** · Điều 8, hiệu lực **01/03/2026**) là căn cứ của `STORY-G-06`. `NĐ 134/2026/NĐ-CP` (Điều 5a · 37a · 37b, hiệu lực **09/04/2026**) là căn cứ của `STORY-G-01` và `STORY-G-03`. Số hiệu *"Điều 11"* trong tên file `STORY-G-06` đã được xác minh ở **năm nguồn độc lập**.

### H · Chất lượng & vận hành
| id | Story |
|---|---|
| `STORY-H-01` | [Story-Golden-Dataset-For-Regression](./Backlog/Story-Golden-Dataset-For-Regression.md) |
| `STORY-H-02` | [Story-Record-Readability-Human-Judgement](./Backlog/Story-Record-Readability-Human-Judgement.md) |
| `STORY-H-03` | [Story-HITL-Gate-And-Eval-Kit](./Backlog/Story-HITL-Gate-And-Eval-Kit.md) |
| `STORY-H-04` | [Story-Log-Preference-Data](./Backlog/Story-Log-Preference-Data.md) |
| `STORY-H-05` | [Story-Minimum-Abuse-Controls](./Backlog/Story-Minimum-Abuse-Controls.md) |
| `STORY-H-06` | [Story-Export-Chapter-To-PDF-CBZ-Webtoon](./Backlog/Story-Export-Chapter-To-PDF-CBZ-Webtoon.md) |

## 🗂️ Thư mục khác

- [`Active-Sprint/`](./Active-Sprint/) — *(chưa có tài liệu; chưa có sprint nào chạy)*

> ⚠️ **Hai link chết đã gỡ**: MOC này từng trỏ tới `Story-Request-OTP.md` và `Story-Verify-OTP.md` — hai file **chưa bao giờ tồn tại**, kế thừa từ repo template và **không thuộc domain `comic-studio`**. Ghi lại việc gỡ thay vì gỡ im lặng.

---

## 📐 Quy ước bắt buộc của tầng này

1. **Acceptance Criteria là CHECKLIST 4 khối, KHÔNG Gherkin**: `Xác minh được` · `Đường không hạnh phúc` · `Ràng buộc cứng không được vi phạm` · `Story này KHÔNG làm`. Ba khối đầu tiên và khối cuối **không được rỗng**.
2. **Mỗi dòng của khối `Xác minh được` phải THẤT BẠI ĐƯỢC**, và cách đo ghi ngay trong dòng đó. *"insert panel 4 nhân vật bị từ chối"* hợp lệ; *"schema hỗ trợ giới hạn nhân vật"* không hợp lệ — không có cách nào chứng minh nó sai.
3. **`Small` của INVEST neo vào giờ-người, không story point, không ngày công**: `E_build ≤ 16h`, `E_hitl ≤ 2h/chapter`. Vượt `E_build` ⇒ ghi lý do thành văn. Vượt `E_hitl` ⇒ `escalate`, **không** tự split.
4. **INVEST KHÔNG áp cho 5 Story `[MVP0]`** (`STORY-A-01`, `STORY-A-02`, `STORY-C-01`, `STORY-H-01`, `STORY-H-02`) — DoD của chúng lấy từ **5 tiêu chí gate G1** ([MVP-Scope §7.2](../010-Planning/MVP-Scope.md)). Dùng đúng chữ **MVP0**; Glossary **cấm** *"phase 0"*, *"spike"*, *"PoC"*.
5. **10 Story ngoài horizon KHÔNG có file** — chúng là hàng trong Epic cha và hàng trong `Backlog-Priority` với `Trạng thái tài liệu = chưa có file`. Đây là **nợ có chủ đích**: một Story file cho việc cách đây 6+ tháng sẽ bị viết lại trước khi có ai nhặt nó.
6. **22 nhãn `[* suy luận]` trên 11 file Story** — đánh dấu chỗ writer tự suy lý do `I`/`S` vỡ hoặc tự neo anchor mà nguồn không đặt tên. Nợ **có chủ đích và grep được**; nó hợp lệ vì được đánh dấu, không vì nó đúng.

## 📚 Tài liệu liên quan

- [Requirements MOC](../020-Requirements/Requirements-MOC.md) — PRD, SRS, 8 BRD, 11 Use Case: nguồn của mọi Epic ở đây
- [Roadmap](../010-Planning/Roadmap.md) — **thắng tuyệt đối** khi lệch với `Backlog-Priority`
- [MVP-Scope](../010-Planning/MVP-Scope.md) — cái gì vào mốc nào, và ba gate Go/No-Go
- [Glossary](../999-Resources/Glossary.md) — 69 thuật ngữ, gồm `E_build` / `E_hitl` / `UNLOCK-ORDER` / `human gate`
- [Documentation Master Index](../000-Index.md) · [RULE-001](../../knowledge-base/99-Templates/Documents-Template.md)
