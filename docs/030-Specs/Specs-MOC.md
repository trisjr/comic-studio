---
id: MOC-030
type: moc
status: live
project: comic-studio
created: 2026-08-30
updated: 2026-08-30
---

# Specs MOC — bản đồ tầng đặc tả (Phase 2)

> [!NOTE]
> **57 tài liệu** sinh ra ở **SDLC Phase 2 — Architecture Design**. Trạng thái: **53 `draft`** + ⭐ **4 `accepted`** — [ADR-001](./Architecture/ADR-001-Backend-And-Frontend-Tech-Stack.md), [ADR-002](./Architecture/ADR-002-Hosting-Platform-And-Region.md), [ADR-003](./Architecture/ADR-003-Auth-And-Billing-Vendor-Selection.md), [ADR-004](./Architecture/ADR-004-Object-Storage-Vendor-And-Signed-URL.md) được duyệt ở run `2026-08-30-dong-bo-srs-nfr-voi-adr` vì tầng 020 hạ nhãn `SRS-NFR-07/08/09` dựa trên chúng.
> Hồ sơ quyết định của run nằm ở [pm-runs/2026-08-28-phase-2-architecture-design-comic-studio](../010-Planning/pm-runs/2026-08-28-phase-2-architecture-design-comic-studio/escalations.md) — mọi mã `E{n}` trong các file spec đều trỏ về đó.

## Mục lục

- [Đọc theo thứ tự nào](#đọc-theo-thứ-tự-nào)
- [1. Architecture — 19 file](#1-architecture--19-file)
- [2. Schema — 14 file](#2-schema--14-file)
- [3. API — 21 file](#3-api--21-file)
- [4. Security — 3 file](#4-security--3-file)
- [Bốn ràng buộc xuyên suốt](#bốn-ràng-buộc-xuyên-suốt)
- [Tài liệu tham khảo](#tài-liệu-tham-khảo)

## Đọc theo thứ tự nào

| Bạn là ai | Đọc gì trước |
|---|---|
| Người viết **migration đầu tiên** | [SDD](#1-architecture--19-file) §3 → toàn bộ [Schema](#2-schema--14-file) |
| Người **implement API** | [SDD](#1-architecture--19-file) §6.3 (`SDD-HG-01`) → [Schema](#2-schema--14-file) của resource → [Endpoint](#3-api--21-file) tương ứng |
| Người **review bảo mật / pháp lý** | [Security](#4-security--3-file) cả 3 file → `ADR-006`, `ADR-010`, `ADR-017` |
| Người muốn biết **vì sao lại thế** | [ADR](#1-architecture--19-file) tương ứng — mỗi ADR có mục *"đã quyết ở đâu"* |

---

## 1. Architecture — 19 file

`docs/030-Specs/Architecture/`

| Tài liệu | Quyết định gì |
|---|---|
| [SDD — Comic Studio](./Architecture/SDD-Comic-Studio.md) | ⭐ **Tài liệu gốc của tầng này.** Sơ đồ kiến trúc (5 khối Mermaid) · ba schema module · sáu luồng dữ liệu · **§6.3 `SDD-HG-01`** là **nguồn duy nhất** của *"không đường nào bypass hai human gate"* · §8 danh sách seam · §9 sổ `TBD` |
| [ADR-001 — Backend & Frontend Tech Stack](./Architecture/ADR-001-Backend-And-Frontend-Tech-Stack.md) | Ngôn ngữ, framework, ORM/query builder |
| [ADR-002 — Hosting Platform & Region](./Architecture/ADR-002-Hosting-Platform-And-Region.md) | Nền tảng chạy và vùng đặt máy. ⚠️ **Mở lại** nếu `T-22` (lưu trữ dữ liệu trong nước) trả lời *"phải"* |
| [ADR-003 — Auth & Billing Vendor Selection](./Architecture/ADR-003-Auth-And-Billing-Vendor-Selection.md) | ⚠️ Vendor auth **⛔ KHÔNG sở hữu `tenant_id`** — `public.tenant`/`user`/`membership` là nguồn duy nhất |
| [ADR-004 — Object Storage & Signed URL](./Architecture/ADR-004-Object-Storage-Vendor-And-Signed-URL.md) | ⛔ Không ký signed URL cho key nhận từ client. Artifact ảnh **⛔ không sinh lại được** ⇒ là kho bằng chứng, ⛔ không phải cache |
| [ADR-005 — Platform Table Schema Placement](./Architecture/ADR-005-Platform-Table-Schema-Placement.md) | Bảng platform ở schema `public`. ⭐ **`G-2`: danh sách bảng `public` là closed list** — thêm bảng phải sửa ADR này trước |
| [ADR-006 — RLS Tenant Context Injection](./Architecture/ADR-006-RLS-Tenant-Context-Injection.md) | Cách bơm tenant context vào mọi transaction |
| [ADR-007 — VLM Provider For QA Select](./Architecture/ADR-007-VLM-Provider-For-QA-Select.md) | VLM chấm best-of-N. ⛔ **Không dùng VLM tự chấm thay người** cho golden dataset |
| [ADR-008 — LLM Provider & Usage Boundaries](./Architecture/ADR-008-LLM-Provider-And-Usage-Boundaries.md) | Ranh giới dùng LLM. ⚠️ Chi phí LLM là **"chưa xác định"**, ⛔ không route về `usage_event` |
| [ADR-009 — Modular Monolith, Three Schemas](./Architecture/ADR-009-Modular-Monolith-Three-Schemas.md) | Một DB, ba schema module `story`/`comic`/`generation` + `public` |
| [ADR-010 — Tenant Isolation With RLS](./Architecture/ADR-010-Tenant-Isolation-With-RLS.md) | Cô lập tenant bằng RLS — nền của `KC-5` |
| [ADR-011 — Narrative Time Key & State Reduction](./Architecture/ADR-011-Narrative-Time-Key-And-State-Reduction.md) | Khoá thời gian tự sự và cách rút trạng thái |
| [ADR-012 — Comic IR As Primary Data](./Architecture/ADR-012-Comic-IR-Spec-As-Primary-Data.md) | ⭐ *"Spec là dữ liệu chính, ảnh chỉ là output"* |
| [ADR-013 — Typeset Layer Separate From Art](./Architecture/ADR-013-Typeset-Layer-Separate-From-Art.md) | Tách lớp chữ khỏi lớp tranh; compositor **dùng chung** cho preview và export |
| [ADR-014 — Deterministic Prompt Compiler & Best-Of-N](./Architecture/ADR-014-Deterministic-Prompt-Compiler-And-Best-Of-N.md) | Compiler xác định byte-for-byte; `N=3` cho **mọi** panel |
| [ADR-015 — Job Queue In Postgres](./Architecture/ADR-015-Job-Queue-In-Postgres.md) | Queue trong Postgres (`FOR UPDATE SKIP LOCKED`) · **polling 2s** là contract chung · `in_flight_per_tenant < N`, ⭐ `N` = `TBD` |
| [ADR-016 — Image Provider Adapter & Version Pinning](./Architecture/ADR-016-Image-Provider-Adapter-And-Version-Pinning.md) | Adapter + ghim version model |
| [ADR-017 — Provenance Chain & One-Transaction Boundary](./Architecture/ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md) | ⭐ **Nguồn duy nhất của `KC-4`** — trỏ theo mã `Q4.x`, ⛔ không chép nội dung |
| [ADR-018 — Usage Event & Rollup Model](./Architecture/ADR-018-Usage-Event-And-Rollup-Model.md) | `usage_event` append-only · rollup là **hàm tổng hợp**, ⛔ không counter tăng tại chỗ |

> ⚠️ **`ADR-019` chưa tồn tại.** Nhiều file nhắc tới nó như nơi đặc tả credit ledger (`[OoH]` MVP3) — ⛔ đừng trỏ link tới nó cho tới khi nó được viết.

## 2. Schema — 14 file

`docs/030-Specs/Schema/` — mỗi file có **ER diagram Mermaid**, bảng cột, invariant, RLS policy.

| Tài liệu | Cụm entity |
|---|---|
| [DB-Entity-Narrative-Timeline](./Schema/DB-Entity-Narrative-Timeline.md) | `chapter`, timeline, event — trục thời gian tự sự |
| [DB-Entity-Story-Bible](./Schema/DB-Entity-Story-Bible.md) | `bible_entity`, `canonical_reference` |
| [DB-Entity-Comic-IR](./Schema/DB-Entity-Comic-IR.md) | `page`, `panel`, `panel_character` — ⭐ nơi cưỡng chế **≤3 nhân vật/panel** |
| [DB-Entity-Dialogue-And-Gate](./Schema/DB-Entity-Dialogue-And-Gate.md) | `dialogue_line`, `human_gate_state` — hai human gate |
| [DB-Entity-Typeset-Layer](./Schema/DB-Entity-Typeset-Layer.md) | Lớp bubble/chữ, toạ độ chuẩn hoá 0–1 |
| [DB-Entity-Preview-And-Export](./Schema/DB-Entity-Preview-And-Export.md) | `preview_render`, `export_artifact` — ⭐ nơi **`SDD-HG-01.4` được cưỡng chế thêm bằng trigger** |
| [DB-Entity-Generation](./Schema/DB-Entity-Generation.md) | `generation` (`generation_kind` = `request`/`candidate`), `prompt_compilation`, ⭐ `cost_bearer` (seam BYOK, `SDD` §8.2 `S-4`) |
| [DB-Entity-Prompt-Vocabulary](./Schema/DB-Entity-Prompt-Vocabulary.md) | `visual_vocabulary` (⚠️ **cố ý không có `tenant_id`**), `action_pose_cache` |
| [DB-Entity-Job-Queue](./Schema/DB-Entity-Job-Queue.md) | `public.job` — DDL, câu CLAIM, index |
| [DB-Entity-Tenancy](./Schema/DB-Entity-Tenancy.md) | `tenant`, `user`, `membership` + policy RLS |
| [DB-Entity-Provenance-And-Usage](./Schema/DB-Entity-Provenance-And-Usage.md) | ⭐ `change_log`, `field_provenance`, `usage_event`, `usage_daily`, **`generation.vlm_scoring_call`** |
| [DB-Entity-Compliance-And-Takedown](./Schema/DB-Entity-Compliance-And-Takedown.md) | `ingest_check`, `text_clean_report`, `takedown_request`, `project_access_state` |
| [DB-Entity-Quality-Assets](./Schema/DB-Entity-Quality-Assets.md) | `golden_dataset_item`, `eval_run`, `provider_refusal_log` |
| [DB-Entity-Credit-Ledger](./Schema/DB-Entity-Credit-Ledger.md) | `credit_ledger`, `credit_hold` — ⚠️ **`[OoH]` MVP3, mức "reserve chỗ"** |

> ⚠️ **Hai ngoại lệ có chủ ý, ⛔ đừng "sửa"**: `visual_vocabulary` không có `tenant_id` (guardrail thay thế là REVOKE quyền ghi) · `generation.vlm_scoring_call` nằm ở schema `generation` nhưng được đặc tả trong `DB-Entity-Provenance-And-Usage`.
> ⚠️ Toàn tầng dùng **`TEXT` + `CHECK`**, ⛔ **không** Postgres enum type.

## 3. API — 21 file

`docs/030-Specs/API/` — 14 `Endpoint-*` + 7 `Spec-Integration-*`. Tiền tố path thống nhất **`/v1/`**.

### 14 Endpoint

| Tài liệu | Resource |
|---|---|
| [Endpoint-Project](./API/Endpoint-Project.md) | ⭐ Nơi đặt `API-PRJ-4`: **mọi** đường đọc/ghi nội dung kiểm `access_state` ⇒ `403 PROJECT_ACCESS_DISABLED` |
| [Endpoint-Chapter-Ingest](./API/Endpoint-Chapter-Ingest.md) | Nạp chapter · ⭐ log opt-out check **kể cả khi âm tính** (`KC-6`) |
| [Endpoint-Story-Bible](./API/Endpoint-Story-Bible.md) | Bible entity, attribute event |
| [Endpoint-Timeline-Event](./API/Endpoint-Timeline-Event.md) | Timeline và event |
| [Endpoint-Panel-Script](./API/Endpoint-Panel-Script.md) | Panel spec |
| [Endpoint-Page-Layout](./API/Endpoint-Page-Layout.md) | Bố cục trang |
| [Endpoint-Human-Gates](./API/Endpoint-Human-Gates.md) | ⭐ **Đường DUY NHẤT** ghi PASS cho cả hai gate; ⛔ không tồn tại endpoint xoá PASS |
| [Endpoint-Generation](./API/Endpoint-Generation.md) | Sinh ảnh · ⭐ **rate limit đếm SỐ REQUEST**, ⛔ không đếm tiền |
| [Endpoint-Bubble-Typeset](./API/Endpoint-Bubble-Typeset.md) | Bubble, thứ tự đọc |
| [Endpoint-Preview-Export](./API/Endpoint-Preview-Export.md) | ⭐ Preview **⛔ KHÔNG** bị chặn bởi human gate; export **thì có**, và có trigger DB làm lưới fail-closed |
| [Endpoint-Tenancy](./API/Endpoint-Tenancy.md) | `/me`, membership |
| [Endpoint-Usage-And-Credit](./API/Endpoint-Usage-And-Credit.md) | Đọc usage/rollup · ⚠️ phần credit là **seam chưa mở** |
| [Endpoint-Takedown-Public](./API/Endpoint-Takedown-Public.md) | ⭐ Bề mặt **không auth, không tenant context ⇒ RLS ⛔ không áp được**. `received_at` là mốc **SLA 72h** |
| [Endpoint-Eval-Kit](./API/Endpoint-Eval-Kit.md) | Golden dataset, eval run — phục vụ **0 UC**, đúng thiết kế |

### 7 Spec-Integration

| Tài liệu | Ranh giới ngoài |
|---|---|
| [Spec-Integration-Image-Provider](./API/Spec-Integration-Image-Provider.md) | Provider sinh ảnh, version pinning |
| [Spec-Integration-VLM-QA-Select](./API/Spec-Integration-VLM-QA-Select.md) | ⭐ **Tách khỏi Image Provider là bắt buộc** — gộp lại là che mất chuyện chi phí VLM chưa vào COGS |
| [Spec-Integration-LLM-Provider](./API/Spec-Integration-LLM-Provider.md) | LLM · chi phí **chưa xác định** |
| [Spec-Integration-Auth-Provider](./API/Spec-Integration-Auth-Provider.md) | ⚠️ Vendor **⛔ không sở hữu `tenant_id`** |
| [Spec-Integration-Object-Storage](./API/Spec-Integration-Object-Storage.md) | ⛔ Cấm ký URL cho key từ client |
| [Spec-Integration-Takedown-Intake](./API/Spec-Integration-Takedown-Intake.md) | ⭐ Mất một đơn hợp lệ = **mất miễn trừ** ⇒ ⛔ cấm fail im lặng |
| [Spec-Integration-Billing-Provider](./API/Spec-Integration-Billing-Provider.md) | ⚠️ **`[OoH]`, mức "reserve chỗ"** |

## 4. Security — 3 file

`docs/030-Specs/Security/` — đây là **Security Review Gate** chặn chuyển Phase 3.

| Tài liệu | Nội dung |
|---|---|
| [Spec-Security-Threat-Model](./Security/Spec-Security-Threat-Model.md) | Tài sản · bề mặt tấn công · STRIDE trên các luồng · biện pháp `C-*` |
| [Spec-Security-Tenant-Isolation](./Security/Spec-Security-Tenant-Isolation.md) | ⭐ Catalog **đường vòng** `BP-*` — ⛔ không dừng ở *"đã bật RLS"* |
| [Spec-Security-Legal-Compliance](./Security/Spec-Security-Legal-Compliance.md) | Nghĩa vụ theo `KC-1`…`KC-7` · **4 khoảng trống pháp lý** dạng câu hỏi cho luật sư |

## Bốn ràng buộc xuyên suốt

⛔ **Bốn ràng buộc này ⛔ KHÔNG được lặp lại nội dung ở bất kỳ file nào — luôn trỏ theo mã.**

| # | Ràng buộc | Nguồn duy nhất |
|:--:|---|---|
| 1 | Không đường nào bypass hai human gate | [`SDD-HG-01`](./Architecture/SDD-Comic-Studio.md) §6.3 |
| 2 | Job queue + **polling 2s** | [ADR-015](./Architecture/ADR-015-Job-Queue-In-Postgres.md) |
| 3 | Chuỗi provenance + ranh giới một transaction (`KC-4`) | [ADR-017](./Architecture/ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md) mã `Q4.x` |
| 4 | Tenant context + RLS | [ADR-006](./Architecture/ADR-006-RLS-Tenant-Context-Injection.md) |

> [!WARNING]
> ⛔ **`SRS-NFR-15` — anti-feature CHỐT**: hệ thống **KHÔNG được** có copyright / plagiarism / similarity detection. Tự dò tương đồng **phá điều kiện *"không biết"*** của miễn trừ trách nhiệm Điều 198b. Đây là chỗ phản xạ nghề nghiệp sẽ làm ngược — lý do đầy đủ ở [Spec-Security-Legal-Compliance](./Security/Spec-Security-Legal-Compliance.md) §5.

## Tài liệu tham khảo

- [SRS — Comic Studio](../020-Requirements/SRS-Comic-Studio.md) — registry `SRS-FR-*` / `SRS-NFR-*`
- [Use Cases](../020-Requirements/Use-Cases/) — `UC-01`…`UC-11`
- [Glossary](../999-Resources/Glossary.md) — 75 headword
- [Hồ sơ quyết định của run Phase 2](../010-Planning/pm-runs/2026-08-28-phase-2-architecture-design-comic-studio/escalations.md) — mọi mã `E{n}`
