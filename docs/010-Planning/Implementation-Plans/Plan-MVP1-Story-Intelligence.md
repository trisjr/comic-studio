---
id: PLAN-001
type: implementation-plan
status: draft
project: comic-studio
owner: "@trisjr"
tags: [mvp1, story-intelligence, multi-tenancy, provenance, planning]
linked-to: "../Roadmap.md"
created: 2026-09-05
updated: 2026-09-05
---

# Plan MVP1 — Story Intelligence (10/2026 – 12/2026)

> [!IMPORTANT]
> **Quy ước nhãn nguồn số liệu** — kế thừa nguyên vẹn từ [MVP-Scope.md](../MVP-Scope.md) và [Roadmap.md](../Roadmap.md):
> `[OFF]` nguồn official/paper gốc · `[BCN]` báo cáo ngành có tên firm · `[TC]` nguồn thứ cấp · `[EM]` ước lượng hoặc phép nhân, **⛔ không phải số đo** · `[CHỐT]` quyết định của Founder tại gate.
>
> Tài liệu này trả lời *"làm gì, theo thứ tự nào, trong bao nhiêu giờ, và xong nghĩa là gì"*. Nó ⛔ **không** định nghĩa lại phạm vi MVP1 (đó là [MVP-Scope §3](../MVP-Scope.md#3-bảng-mvp-vs-full-scope)) và ⛔ **không** định nghĩa lại gate (đó là [MVP-Scope §7](../MVP-Scope.md#7-gono-go-decision)).

## Mục lục

1. [Tài liệu này giải quyết việc gì](#1-tài-liệu-này-giải-quyết-việc-gì)
2. [Điểm xuất phát thực tế — đã verify](#2-điểm-xuất-phát-thực-tế--đã-verify)
3. [Ba nợ kỹ thuật MVP1 thừa kế](#3-ba-nợ-kỹ-thuật-mvp1-thừa-kế)
4. [Phạm vi MVP1 — vào, ra, và ba khoảng trống](#4-phạm-vi-mvp1--vào-ra-và-ba-khoảng-trống)
5. [Số học capacity — nói thẳng trước khi lập lịch](#5-số-học-capacity--nói-thẳng-trước-khi-lập-lịch)
6. [Van xả xếp sẵn & ngưỡng kích](#6-van-xả-xếp-sẵn--ngưỡng-kích)
7. [Đường găng & thứ tự sprint](#7-đường-găng--thứ-tự-sprint)
8. [Exit criteria M1-1…M1-7 — ai trả, ở sprint nào](#8-exit-criteria-m1-1m1-7--ai-trả-ở-sprint-nào)
9. [Gate G2 — verdict đã biết trước](#9-gate-g2--verdict-đã-biết-trước)
10. [Rủi ro & tín hiệu sớm](#10-rủi-ro--tín-hiệu-sớm)
11. [Tài liệu tham khảo](#11-tài-liệu-tham-khảo)

---

## 1. Tài liệu này giải quyết việc gì

[Roadmap §2](../Roadmap.md#2-bảng-lộ-trình-tổng) cấp cho MVP1 một **khoảng thời gian** (10–12/2026) và một cột *Effort ước tính* ghi **`Tổng tuần-người: TBD`**. Đó là một phân bổ, ⛔ không phải một kế hoạch. Tài liệu này biến `TBD` đó thành:

| Câu hỏi | Trả lời ở |
|---|---|
| Chính xác những story nào thuộc MVP1 | [§4](#4-phạm-vi-mvp1--vào-ra-và-ba-khoảng-trống) |
| Mỗi story bao nhiêu giờ, tổng bao nhiêu, có vừa không | [§5](#5-số-học-capacity--nói-thẳng-trước-khi-lập-lịch) · [WBS-MVP1](../Estimates/WBS-MVP1.md) |
| Nếu ⛔ không vừa thì cắt gì, cắt lúc nào, ai quyết | [§6](#6-van-xả-xếp-sẵn--ngưỡng-kích) |
| Làm theo thứ tự nào để ⛔ không kẹt phụ thuộc | [§7](#7-đường-găng--thứ-tự-sprint) |
| Mỗi sprint xong nghĩa là gì | [Sprint-001](../Sprints/Sprint-001.md) … [Sprint-006](../Sprints/Sprint-006.md) |

### 1.1 Ranh giới với ba tài liệu kề

| Tài liệu | Trả lời | ⛔ Không trả lời |
|---|---|---|
| [MVP-Scope.md](../MVP-Scope.md) | Cái gì vào MVP1 | Bao nhiêu giờ, thứ tự nào |
| [Roadmap.md](../Roadmap.md) | Khi nào, mốc nào trước mốc nào | Chia sprint, phân bổ giờ |
| [OKRs.md](../OKRs.md) | Thành công cuối Q4 trông như thế nào | Đường đi tới đó |
| **Plan này** | **Đường đi: story → sprint → giờ → DoD** | Vì sao dự án đáng làm ([Charter](../Charter-Comic-Studio.md)) |

---

## 2. Điểm xuất phát thực tế — đã verify

> [!NOTE]
> Mọi dòng dưới đây được kiểm bằng `ls` / `grep` / `git log` tại thời điểm viết (`2026-09-05`), ⛔ không suy đoán từ tài liệu.

| Hạng mục | Trạng thái thực tế | Bằng chứng |
|---|---|---|
| **MVP0** | ⛔ **Khép theo quyết định Founder** ngày `2026-09-05`, ⛔ **không phải** `G1` PASS | [`mvp0/golden-dataset/g1-verdict.md §5.1`](../../../mvp0/golden-dataset/g1-verdict.md) |
| **Gate `G1`** | **0/5** tiêu chí có số · `p50`/`p90` ⛔ không có · golden dataset **`0`** panel / mục tiêu 15–20 | cùng nguồn, §5 |
| **Migration** | `0001_foundation.sql` — 3 schema (`story`/`comic`/`generation`) + guardrail `public` + `current_tenant_id()` + grant 3 role. ⛔ **Chưa một bảng nghiệp vụ nào** | `apps/backend/db/migrations/` |
| **Backend** | Dispatcher 4 lệnh + 3 module rỗng + health controller + S3 adapter + 2 file invariant test | `apps/backend/src/` |
| **Frontend** | ⛔ **Chưa tồn tại** — `apps/` chỉ có `backend` | `ls apps/` |
| **CI** | ⛔ **Chưa tồn tại** — ⛔ không có `.github/workflows/` | `ls .github/` |
| **Backlog** | 41 story có AC + INVEST + ước lượng. **26 story** thuộc MVP1 | `docs/022-User-Stories/Backlog/` |
| **Contracts** | `packages/contracts` mới có `primitives/` (identifiers, decimal) | `packages/contracts/src/` |

⭐ **Điều đáng chú ý nhất**: nền kiến trúc đã đúng (3 schema, hàm tenant context, 3 DB role tách quyền) nhưng **⛔ chưa có một dòng dữ liệu nghiệp vụ nào**. Đây là vị trí lý tưởng để áp `KC-5` — `tenant_id` được cài **trước khi** có dữ liệu thật, đúng như [MVP-Scope §6](../MVP-Scope.md#6-không-được-cắt--danh-sách-cứng) đòi hỏi.

---

## 3. Ba nợ kỹ thuật MVP1 thừa kế

### 3.1 Nợ #1 — `G1` chưa từng được đo `[CHỐT]`

[Roadmap §6.2](../Roadmap.md#62-bảng-phụ-thuộc) xếp *"**`G1` PASS** chặn toàn bộ MVP1 → MVP4"* là phụ thuộc **CỨNG**. `G1` ⛔ không PASS, cũng ⛔ không FAIL — nó **chưa được đo**.

| | |
|---|---|
| **Quyết định Founder** `2026-09-05` | MVP1 đi tiếp trên tiền đề **chưa kiểm chứng**; ⛔ **không** chèn data probe sinh ảnh vào MVP1 |
| **Hệ quả chấp nhận** | Câu hỏi *"tiền đề sản phẩm còn đứng không"* vẫn **NGUYÊN**, chưa trả lời, suốt 3 tháng MVP1 |
| **Nợ chuyển đi đâu** | **MVP3** — mốc đầu tiên có image pipeline thật để đo lại 5 tiêu chí `G1` |
| **Việc phải làm ở MVP1** | Ghi hàng mới vào [Risk-Register](../Risk-Register.md): *"MVP1–MVP2 xây trên tiền đề kỹ thuật chưa đo"* |

### 3.2 Nợ #2 — golden dataset ⛔ không có ảnh ⇒ eval kit đổi trục đo

`M1-6` đòi *"eval kit chạy được trên golden dataset của MVP0 và cho ra số"*. Golden dataset hiện có **`0`** panel ảnh, và MVP1 `A1 = ⛔` nên ⛔ không sinh thêm ảnh nào.

⭐ **Lối ra ⛔ không phải bỏ eval kit** — mà là đo **đúng thứ MVP1 thực sự sản xuất ra**:

| | Golden dataset mức ẢNH (MVP0 dự kiến) | ⭐ Golden dataset mức TEXT (MVP1 thực tế) |
|---|---|---|
| Ground truth | 15–20 panel có bảng chấm | [`mvp0/story-bible.yaml`](../../../mvp0/story-bible.yaml) **viết tay** + [`mvp0/chapters/ch01.md`](../../../mvp0/chapters/ch01.md) |
| Đo cái gì | Consistency nhân vật, N tối thiểu, human-reject rate | **Extraction recall/precision** entity (nhân vật + địa điểm) |
| Thoả tiêu chí nào | `G1-a`…`G1-e` | ⭐ **`M1-3`** (≥80% entity khớp) · ⭐ **`M1-6`** (eval kit cho ra số) · `KR2.2` · `KR2.3` |
| Cần sinh ảnh ⛔ không | **Có** | ⛔ **Không** |

⚠️ `[EM]` — **diễn giải của em, ⛔ không có trong CF.** Căn cứ: `M1-3` và `KR2.2` vốn đã định nghĩa phép đo bằng *"khớp Story Bible **viết tay** của MVP0"* — một phép đo thuần text. `M1-6` ⛔ không nói golden dataset **phải** là ảnh. Trục ảnh chuyển sang MVP3 cùng nợ #1.

### 3.3 Nợ #3 — `G2` mất toàn bộ đầu vào

Xem [§9](#9-gate-g2--verdict-đã-biết-trước). Đây là nợ có hệ quả xa nhất và đã có quyết định `[CHỐT]`.

---

## 4. Phạm vi MVP1 — vào, ra, và ba khoảng trống

### 4.1 Vào MVP1 — 26 story

Nguồn: cột **MVP1** của [MVP-Scope §3](../MVP-Scope.md#3-bảng-mvp-vs-full-scope). `✅` = làm đầy đủ · `🟡` = làm một phần.

| Hàng scope | Story | ID | `E_build` | Nguồn ước lượng |
|---|---|---|--:|---|
| `E2` ✅ | [Tenant-User-Membership-As-Three-Entities](../../022-User-Stories/Backlog/Story-Tenant-User-Membership-As-Three-Entities.md) | `STORY-E-02` | 8h | story |
| `E1` ✅ | [Tenant-Id-And-RLS-Everywhere](../../022-User-Stories/Backlog/Story-Tenant-Id-And-RLS-Everywhere.md) | `STORY-E-01` | 24h | story |
| `E5` ✅ | [Modular-Monolith-Three-Schemas](../../022-User-Stories/Backlog/Story-Modular-Monolith-Three-Schemas.md) | `STORY-E-05` | 6h | 14h story − 8h đã xong (PR #24) |
| `E3` ✅ | [Per-Tenant-Object-Storage-No-Cross-Dedup](../../022-User-Stories/Backlog/Story-Per-Tenant-Object-Storage-No-Cross-Dedup.md) | `STORY-E-03` | 10h | story |
| `E4` ✅ | [Buy-Authentication-Provider](../../022-User-Stories/Backlog/Story-Buy-Authentication-Provider.md) | `STORY-E-04` | 12h | story |
| `GP-2` ✅ | [Opt-Out-Check-At-Ingest](../../022-User-Stories/Backlog/Story-Opt-Out-Check-At-Ingest.md) | `STORY-G-03` | 12h | ⚠️ `[EM]` PM — story ghi `TBD` |
| `GP-5` ✅ | [ToS-User-Warrant-And-Tenant-Hard-Delete](../../022-User-Stories/Backlog/Story-ToS-User-Warrant-And-Tenant-Hard-Delete.md) | `STORY-G-04` | 18h | ⚠️ `[EM]` PM — story ghi `TBD` |
| `B4` ✅ | [Fix-Narrative-Time-Key](../../022-User-Stories/Backlog/Story-Fix-Narrative-Time-Key.md) | `STORY-B-01` | 8h | story |
| `GP-1` ✅ | [Provenance-Chain-Parent-Generation](../../022-User-Stories/Backlog/Story-Provenance-Chain-Parent-Generation.md) | `STORY-G-01` | 14h | ⚠️ `[EM]` PM — story ghi `TBD` |
| `GP-1` ✅ | [Change-Log-On-Every-Editor-Action](../../022-User-Stories/Backlog/Story-Change-Log-On-Every-Editor-Action.md) | `STORY-D-02` | 20h | story (vượt trần 16h, lý do đã ghi) |
| `F2` ✅ | [Generation-Cost-And-Model-Metadata](../../022-User-Stories/Backlog/Story-Generation-Cost-And-Model-Metadata.md) | `STORY-F-02` | 10h | story |
| `F1` ✅ | [Usage-Event-And-Daily-Rollup](../../022-User-Stories/Backlog/Story-Usage-Event-And-Daily-Rollup.md) | `STORY-F-01` | 12h | story |
| `KC-4` ✅ | [Provenance-Committed-In-Same-Transaction](../../022-User-Stories/Backlog/Story-Provenance-Committed-In-Same-Transaction.md) | `STORY-G-02` | 12h | ⚠️ `[EM]` PM — story ghi `TBD` |
| `A5` ✅ | [Job-Queue-In-Postgres](../../022-User-Stories/Backlog/Story-Job-Queue-In-Postgres.md) | `STORY-A-05` | 12h | story |
| `H2` ✅ | [Log-Preference-Data](../../022-User-Stories/Backlog/Story-Log-Preference-Data.md) | `STORY-H-04` | 10h | story |
| `H5` 🟡 | [Minimum-Abuse-Controls](../../022-User-Stories/Backlog/Story-Minimum-Abuse-Controls.md) | `STORY-H-05` | 4h | ⚠️ `[EM]` PM — 8h full, phần 🟡 của MVP1 |
| `GP-3` 🟡 | [Safe-Harbour-Checklist-Article-198b](../../022-User-Stories/Backlog/Story-Safe-Harbour-Checklist-Article-198b.md) | `STORY-G-05` | 6h | ⚠️ `[EM]` PM — story ghi `TBD` |
| `B1` ✅ | [Chapter-Ingest-And-Text-Clean](../../022-User-Stories/Backlog/Story-Chapter-Ingest-And-Text-Clean.md) | `STORY-B-02` | 10h | story |
| `B2` ✅ | [Story-Bible-Extraction](../../022-User-Stories/Backlog/Story-Story-Bible-Extraction.md) | `STORY-B-03` | 18h | story (vượt trần, lý do đã ghi) |
| `B3` ✅ | [Timeline-State-Resolver](../../022-User-Stories/Backlog/Story-Timeline-State-Resolver.md) | `STORY-B-04` | 20h | story (vượt trần, lý do đã ghi) |
| `H1` ✅ | [HITL-Gate-And-Eval-Kit](../../022-User-Stories/Backlog/Story-HITL-Gate-And-Eval-Kit.md) | `STORY-H-03` | 24h | story (vượt trần, lý do đã ghi) |
| `H6` ✅ | [Golden-Dataset-For-Regression](../../022-User-Stories/Backlog/Story-Golden-Dataset-For-Regression.md) | `STORY-H-01` | 6h | story — ⭐ đổi sang trục TEXT, xem [§3.2](#32-nợ-2--golden-dataset-⛔-không-có-ảnh-⇒-eval-kit-đổi-trục-đo) |
| `D1` 🟡 #5 | [Story-Bible-Editor-Form](../../022-User-Stories/Backlog/Story-Story-Bible-Editor-Form.md) | `STORY-D-01` | 14h | story |
| `C1` ✅ | [Comic-IR-Panel-Specification](../../022-User-Stories/Backlog/Story-Comic-IR-Panel-Specification.md) | `STORY-C-01` | 20h | story (vượt trần, lý do đã ghi) |
| — | ⭐ **`NEW-01` CI pipeline** | `TBD` | 8h | ⚠️ `[EM]` PM — [§4.3](#43-ba-khoảng-trống-backlog--⛔-chưa-story-nào-phủ) |
| — | ⭐ **`NEW-02` LLM provider adapter** | `TBD` | 8h | ⚠️ `[EM]` PM — [§4.3](#43-ba-khoảng-trống-backlog--⛔-chưa-story-nào-phủ) |
| — | ⭐ **`NEW-03` Frontend app scaffold** | `TBD` | 10h | ⚠️ `[EM]` PM — [§4.3](#43-ba-khoảng-trống-backlog--⛔-chưa-story-nào-phủ) |
| — | Chạy `G2` + ghi verdict | — | 4h | ⚠️ `[EM]` PM — [§9](#9-gate-g2--verdict-đã-biết-trước) |

**Tổng kỹ thuật: 340 giờ-người** `[EM]`.

### 4.2 Ra khỏi MVP1 — và vì sao

| Hạng mục | Trạng thái MVP1 | Vì sao ⛔ không làm bây giờ |
|---|---|---|
| `A1` Generate panel + VLM select | ⛔ | Code MVP0 làm rồi và **bị vứt theo kỷ luật spike**. Xây lại ở MVP3 là *scale-up*, ⛔ không phải khám phá (CF-8.9) |
| `A4` Adapter đa provider | ⛔ | ⛔ Không có gì để sinh ảnh ở MVP1 ⇒ adapter ⛔ không có người gọi |
| `A2` Typeset · `A3` Prompt compiler | 🟡 **giữ nguyên mức MVP0** | Cả hai `🟡` ở MVP0 **và** `🟡` ở MVP1 ⇒ ⛔ không tiến thêm. `0h` trong WBS. ⚠️ `[EM]` diễn giải của em từ bảng scope |
| `C2`…`C7` Director, rubric, ≤3 nhân vật, `text_safe_zone`, hai human gate | ⛔ | Toàn bộ `⛔ ở MVP1, ✅ từ MVP2` theo MVP-Scope §3 |
| `D3`, `D4`, `D5` Editor thành phần #1–#4 | ⛔ | MVP1 chỉ có **thành phần #5** (Story Bible editor) — [MVP-Scope §5](../MVP-Scope.md#5-editor-tối-thiểu--ranh-giới-chi-tiết) |
| `F3`/`F4` Credit ledger + hard quota | ⛔ | MVP3, *trước bản trả phí có image gen* (CF-8.11b) |
| `H4` Export PDF/CBZ | ⛔ | MVP2 preview server-side trước |
| ⭐ `GP-4` AI disclosure (`STORY-G-06`) | ⛔ **đẩy sang MVP2** `[CHỐT]` | **Van xả #1 đã kích.** GP-4 = `🟡` ở **cả** MVP1 và MVP2, `✅` mãi MVP3; deadline tuân thủ **~01/03/2027**. Ở MVP1 ⛔ chưa có export path (`H4 = ⛔`) nên nửa AC về nhúng watermark ⛔ không thực thi được |

### 4.3 Ba khoảng trống backlog — ⛔ chưa story nào phủ

> [!CAUTION]
> Ba hạng mục dưới đây **⛔ không tồn tại trong `docs/022-User-Stories/Backlog/`** nhưng MVP1 ⛔ **không chạy được nếu thiếu**. Đã verify bằng `ls` và `grep`. Chúng cần được viết thành story trước khi sprint tương ứng bắt đầu.

| # | Khoảng trống | Ai đòi nó | Vì sao ⛔ không thể bỏ | `[EM]` |
|---|---|---|---|--:|
| `NEW-01` | **CI pipeline** (`lint` + `typecheck` + invariant test trên PostgreSQL thật) | `KR1.1` và `KR1.2` đều ghi tần suất đo là ***"Mỗi commit trong CI"*** | ⛔ Không có CI thì hai KR quan trọng nhất của `O1` ⛔ không có cơ chế đo. Và với **1 dev ⛔ không code review** (`C1`), CI là lớp kiểm tra duy nhất | 8h |
| `NEW-02` | **LLM provider adapter** | `STORY-B-03` extraction phải gọi LLM | Có [`Spec-Integration-LLM-Provider.md`](../../030-Specs/API/Spec-Integration-LLM-Provider.md) và [`ADR-008`](../../030-Specs/Architecture/ADR-008-LLM-Provider-And-Usage-Boundaries.md), ⛔ nhưng không có story. Backlog chỉ có `STORY-A-04` cho **image** provider (`⛔` ở MVP1) | 8h |
| `NEW-03` | **Frontend app scaffold** (`apps/web`: Vite + React + TS + TanStack Query + shadcn/ui) | `STORY-D-01` Story Bible editor là UI | `apps/` hiện chỉ có `backend`. [`ADR-001`](../../030-Specs/Architecture/ADR-001-Backend-And-Frontend-Tech-Stack.md) đã chốt stack — việc còn lại là dựng, ⛔ không phải quyết | 10h |

---

## 5. Số học capacity — nói thẳng trước khi lập lịch

> [!CAUTION]
> `CF-8.13` `[CHỐT]`: *"**Cấm nén lịch cho vừa khung.**"* Mục này tồn tại để tuân thủ điều đó — nó trình bày con số thật, kể cả khi con số đó ⛔ không đẹp.

### 5.1 Capacity thực

| | |
|---|---|
| **Nhịp làm việc** | **30 giờ/tuần** `[CHỐT]` Founder, `2026-09-05` |
| **Cửa sổ** | `05/10/2026` (thứ Hai) → `31/12/2026` = **12 tuần + 4 ngày** |
| **Capacity** | `12 × 30 + 4 × 6` = **384 giờ-người** |
| **Ngày 01–02/10** | 2 ngày setup môi trường, ⛔ không tính vào sprint |

### 5.2 Tải thực

| Khối | Giờ | Nguồn |
|---|--:|---|
| 26 story MVP1 + 3 khoảng trống + chạy `G2` | **340h** | [§4.1](#41-vào-mvp1--26-story) · [WBS-MVP1](../Estimates/WBS-MVP1.md) |
| ⭐ **`O4` go-to-market** — 12 post + 12 trang SEO + 20 cuộc trò chuyện | **46h** `[EM]` | [OKRs §3 O4](../OKRs.md) — `KR4.1`, `KR4.2`, `KR4.3` |
| **TỔNG** | **386h** | |

### 5.3 ⭐ Kết luận trung thực

```
Tải 386h / Capacity 384h = 100,5%
Đệm = −2h  ⇒  KHÔNG CÓ ĐỆM
```

> [!WARNING]
> **Đây ⛔ không phải một cảnh báo hình thức.** Ở mức 100,5%, **bất kỳ story nào vượt ước lượng 1% là mốc trượt**. Với **1 dev ⛔ không code review** và **7/26 story mang ước lượng `[EM]` do PM đặt** (⛔ không phải từ story), xác suất một story vượt ước lượng ⛔ không nhỏ.
>
> ⭐ **`O4` là khối bị bỏ quên**: 46h công việc go-to-market đã cam kết trong OKR Q4 mà ⛔ chưa lịch kỹ thuật nào tính vào. Nó ⛔ không phải việc tuỳ chọn — `KR4.3` (20 cuộc trò chuyện tác giả) là **cách duy nhất** lấp khoảng trống *willingness-to-pay*, và `Roadmap` đặt hạn cho nó là **trước 31/12/2026**.

⇒ Vì ⛔ không được nén lịch, và vì Founder đã chọn kích **đúng một** van xả, kế hoạch này đi tiếp với **cơ chế van xả xếp sẵn** ở [§6](#6-van-xả-xếp-sẵn--ngưỡng-kích) thay vì giả vờ rằng 386h vừa 384h.

---

## 6. Van xả xếp sẵn & ngưỡng kích

⭐ **Nguyên tắc**: quyết định cắt scope được **xếp sẵn theo thứ tự và gắn ngưỡng số** *từ hôm nay*, để khi tràn xảy ra thì đó là **một bước đã hoạch định**, ⛔ không phải một cuộc thương lượng dưới áp lực.

### 6.1 Ngưỡng kích

Cuối **mỗi sprint**, tính:

```
burn_tích_luỹ = Σ(giờ thực đã tiêu) / Σ(giờ kế hoạch tới hết sprint đó)
```

| `burn_tích_luỹ` | Hành động |
|---|---|
| ≤ **105%** | ⛔ Không làm gì. Ghi số vào retro sprint |
| > **105%** | ⭐ **Kích van kế tiếp trong danh sách 6.2 ngay tại retro**, ⛔ không đợi sprint sau |
| > **120%** | Kích **hai** van cùng lúc + báo cáo lại toàn bộ mốc `31/12` với Founder |

### 6.2 Danh sách van, theo thứ tự kích

| Thứ tự | Van | Tiết kiệm | Mất gì | Trạng thái |
|:-:|---|--:|---|---|
| **#1** | `STORY-G-06` AI disclosure → MVP2 | **4h** | Gần như ⛔ không mất gì — GP-4 `🟡` ở cả MVP1 lẫn MVP2, deadline `~01/03/2027`, và ở MVP1 ⛔ chưa có export path để nhúng marker | ✅ **ĐÃ KÍCH** `[CHỐT]` `2026-09-05` |
| **#2** | `STORY-C-01` Comic IR → thu về **schema tối thiểu** (giữ đủ cột + FK tới Story Bible; đẩy `CHECK` constraint và enforcement sang MVP2) | **8h** | Ít — **mọi thứ tiêu thụ Comic IR** (`C2`…`C7`) đều `⛔` ở MVP1. Xây đầy đủ bây giờ là xây cho ⛔ không ai dùng | ⏸ chờ ngưỡng |
| **#3** | `KR4.2` — hoãn 12 trang SEO sang Q1/2027 | **24h** | 3 tháng đầu tiên cho SEO ngấm. ⚠️ `KR4.2` dựa trên **quan sát SERP** `[EM]`, ⛔ không phải số traffic đo được ⇒ đây là KR có nền chứng cứ yếu nhất của `O4`. `KR4.1` và `KR4.3` **⛔ không được cắt** | ⏸ chờ ngưỡng |
| **#4** | `STORY-D-01` + `NEW-03` frontend → MVP2 | **24h** | ⚠️ **Nặng.** [Roadmap §3.2](../Roadmap.md#32-mvp1--story-intelligence-102026--122026) gọi Story Bible editor là *"nơi moat **lộ ra với khách hàng**"*, và ⛔ không có UI thì `KR4.3` (20 cuộc trò chuyện tác giả) ⛔ không có gì để cho xem | ⏸ **van cuối** |

⛔ **⛔ Không có van #5.** Nếu đã kích cả bốn mà vẫn tràn, đó là tín hiệu mốc `31/12/2026` sai chứ ⛔ không phải scope sai — và [Roadmap §1.3](../Roadmap.md#13-điều-không-chắc-chắn-ngay-bên-trong-phần-chứa-được) đã chấp nhận trước khả năng mốc trượt.

### 6.3 ⛔ Điều CẤM khi tràn

| ⛔ Cấm | Vì sao |
|---|---|
| Cắt `STORY-E-01` hoặc bất kỳ phần nào của `tenant_id` + RLS | `KC-5` — *"⛔ không có cách nào xác minh đã sửa hết"*. `tenant_id` trên 8/10 bảng = **vẫn rò rỉ** |
| Cắt bất kỳ mục nào trong 5 hạng mục provenance | `KC-1`…`KC-4` — ⛔ **không backfill được** (`CF-7.3`) |
| Cắt `STORY-G-03` opt-out Điều 37b | `KC-6` — chi phí vận hành **~0** `[OFF]`, và đây là nơi **duy nhất** file user lần đầu vào hệ thống |
| Bỏ test rò rỉ chéo tenant để "chạy nhanh hơn" | `M1-1` là **DoD nhị phân**, ⛔ không phải % bảng đã sửa |
| Giảm `E_build` trên giấy mà ⛔ không giảm phạm vi | Nén lịch trá hình — vi phạm `CF-8.13` |

---

## 7. Đường găng & thứ tự sprint

### 7.1 Ràng buộc thứ tự — cái gì chặn cái gì

```text
        ┌─────────────────────────────────────────────────────┐
        │  S1  E-02 → E-01 (tenant_id + RLS)  ⭐ CHẶN MỌI BẢNG │
        │      E-05 (còn lại) · NEW-01 CI                      │
        └──────────────────────┬───────────────────────────────┘
                               ▼
        ┌─────────────────────────────────────────────────────┐
        │  S2  E-03 storage · E-04 auth                        │
        │      G-03 opt-out ─┐  ⭐ CHẶN B-02 (phải chạy TRƯỚC) │
        │      G-04 hard-delete                                │
        └──────────────────────┬───────────────────────────────┘
                               ▼
        ┌─────────────────────────────────────────────────────┐
        │  S3  B-01 khoá thời gian ⭐ CHẶN B-04                │
        │      G-01 provenance · D-02 change_log · F-02 cost   │
        └──────────────────────┬───────────────────────────────┘
                               ▼
        ┌─────────────────────────────────────────────────────┐
        │  S4  F-01 usage_event ─┐                             │
        │      G-02 same-transaction ◄─ cần G-01 + D-02 + F-01 │
        │      A-05 job queue · H-04 preference                │
        │      H-05 abuse 🟡 · G-05 safe harbour 🟡            │
        └──────────────────────┬───────────────────────────────┘
                               ▼
        ┌─────────────────────────────────────────────────────┐
        │  S5  NEW-02 LLM adapter → B-02 ingest → B-03 extract │
        │      B-04 timeline resolver  (cần B-01 + B-03)       │
        └──────────────────────┬───────────────────────────────┘
                               ▼
        ┌─────────────────────────────────────────────────────┐
        │  S6  NEW-03 FE scaffold → D-01 editor                │
        │      H-01 golden dataset → H-03 eval kit (cần B-03)  │
        └──────────────────────┬───────────────────────────────┘
                               ▼
        ┌─────────────────────────────────────────────────────┐
        │  Tuần gate 28–31/12   C-01 Comic IR · G2 verdict     │
        └─────────────────────────────────────────────────────┘
```

### 7.2 Vì sao thứ tự này, ⛔ không phải thứ tự khác

| Quyết định thứ tự | Lý do |
|---|---|
| ⭐ **`E-01` ở sprint đầu tiên, ⛔ không muộn hơn** | `KC-5`: retrofit `tenant_id` vào schema **đã có dữ liệu** là migration đắt nhất tồn tại. Hiện `0001` ⛔ chưa tạo bảng nghiệp vụ nào ⇒ **đây là thời điểm rẻ nhất, và nó ⛔ không quay lại** |
| **`NEW-01` CI cũng ở S1** | `KR1.1`/`KR1.2` đo *"mỗi commit"*. CI dựng sau ⇒ mọi commit trước đó ⛔ không được đo, và với 1 dev ⛔ không code review thì đó là vùng mù |
| ⭐ **`G-03` opt-out TRƯỚC `B-02` ingest** | AC của `G-03`: *"bước kiểm opt-out chạy **trước** mọi bước xử lý nội dung khác"*. Làm ngược thứ tự = phải sửa lại pipeline |
| **`B-01` khoá thời gian trước `B-04`** | [Roadmap §6.2](../Roadmap.md#62-bảng-phụ-thuộc): *"sai âm thầm ở flashback; nằm trong khoá nên sửa sau = migration toàn bộ"* — phụ thuộc **CỨNG** |
| **`G-02` sau `G-01` + `D-02` + `F-01`** | `G-02` là **test** chứng minh cả ba bảng commit cùng transaction. ⛔ Không có đủ ba bảng thì ⛔ không có gì để test |
| **`C-01` Comic IR ở tuần cuối** | ⛔ Không có gì ở MVP1 tiêu thụ Comic IR (`C2`…`C7` đều `⛔`). Đặt cuối ⇒ nó tự nhiên trở thành **van #2** nếu tràn, ⛔ không phải một quyết định phải bàn lại |

### 7.3 Lịch sprint

| Sprint | Ngày | Chủ đề | Giờ KT | Giờ `O4` | Tổng |
|---|---|---|--:|--:|--:|
| [001](../Sprints/Sprint-001.md) | `05/10` – `16/10` | Nền tenancy ⛔ không retrofit được | 46 | 7 | 53 |
| [002](../Sprints/Sprint-002.md) | `19/10` – `30/10` | Cửa pháp lý & đường vào của dữ liệu | 52 | 8 | 60 |
| [003](../Sprints/Sprint-003.md) | `02/11` – `13/11` | Provenance — bằng chứng ⛔ không thiếu ngẫu nhiên | 52 | 8 | 60 |
| [004](../Sprints/Sprint-004.md) | `16/11` – `27/11` | Sổ cái sử dụng & ranh giới transaction | 56 | 8 | 64 |
| [005](../Sprints/Sprint-005.md) | `30/11` – `11/12` | Story Intelligence — ingest → extraction → timeline | 56 | 8 | 64 |
| [006](../Sprints/Sprint-006.md) | `14/12` – `25/12` | Editor & eval kit — nơi moat lộ ra | 54 | 7 | 61 |
| **Tuần gate** | `28/12` – `31/12` | Comic IR + chạy `G2` + retro MVP1 | 24 | 0 | 24 |
| | | **TỔNG** | **340** | **46** | **386** |

⚠️ Bốn sprint giữa vượt capacity danh nghĩa `60h/sprint`. Đó là **hệ quả trực tiếp của 100,5% load** ở [§5.3](#53--kết-luận-trung-thực), ⛔ không phải lỗi phân bổ — và là lý do cơ chế van xả tồn tại.

---

## 8. Exit criteria `M1-1`…`M1-7` — ai trả, ở sprint nào

Nguồn: cột *Điều kiện ra* của [Roadmap §2](../Roadmap.md#2-bảng-lộ-trình-tổng), mốc MVP1.

| # | Nội dung | Story trả | Sprint | Cách nghiệm thu |
|---|---|---|:-:|---|
| `M1-1` | `tenant_id NOT NULL` **100%** bảng nghiệp vụ · RLS **100%** bảng có `tenant_id` · **test rò rỉ chéo tenant PASS** | `E-01`, `E-02` | **S1** | Test tự động: query tenant A trả về **`0`** row của tenant B. ⭐ DoD là **test PASS**, ⛔ không phải số bảng đã sửa |
| `M1-2` | Pipeline ingest có **text clean là bước ĐẦU TIÊN**, chạy trên **≥1 chapter scrape thật** | `B-02`, `G-03` | **S5** | Chạy end-to-end; kiểm bằng mắt rằng quảng cáo / lời tác giả cuối chương ⛔ không sinh entity giả |
| `M1-3` | Extraction đạt **≥80%** entity khớp Story Bible viết tay MVP0 ⚠️ ngưỡng `[EM]` | `B-03`, `H-01`, `H-03` | **S6** | Eval kit chấm trên golden dataset **mức TEXT** — xem [§3.2](#32-nợ-2--golden-dataset-⛔-không-có-ảnh-⇒-eval-kit-đổi-trục-đo) |
| `M1-4` | **100%** file upload đi qua bước kiểm **opt-out Điều 37b** | `G-03` | **S2** | `số ingest_event có cờ đã-kiểm / tổng số upload = 100%` |
| `M1-5` | **5/5** hạng mục provenance tồn tại **và có test** chứng minh commit **cùng một transaction** | `G-01`, `D-02`, `F-01`, `G-02` | **S4** | Test rollback: raise exception giữa chừng ⇒ **⛔ không** row nào trong ba bảng sống sót |
| `M1-6` | Eval kit chạy được trên golden dataset và **cho ra số** | `H-01`, `H-03` | **S6** | Tồn tại một báo cáo eval **có số**, sinh tự động, ⛔ không chấm bằng ấn tượng |
| `M1-7` | `usage_daily` có `p50`/`p90` regen ratio ⇒ `G2` chạy được | `F-01` | ⛔ **⛔ KHÔNG TRẢ ĐƯỢC** | Xem [§9](#9-gate-g2--verdict-đã-biết-trước) — MVP1 `A1 = ⛔` ⇒ ⛔ không có generation để đếm regen |

> [!CAUTION]
> ⭐ **`M1-7` là exit criterion duy nhất của MVP1 mà kế hoạch này ⛔ KHÔNG trả được**, và điều đó **đã biết từ hôm nay** `[CHỐT]`. `F-01` vẫn xây đầy đủ (`usage_event` + rollup `usage_daily`) — cấu trúc có, chỉ ⛔ không có dữ liệu image generation chảy vào. Khi MVP3 bật pipeline, `M1-7` được trả **⛔ không cần sửa schema**.

---

## 9. Gate `G2` — verdict đã biết trước

### 9.1 Vì sao `G2` ⛔ không chạy được

[MVP-Scope §7.3](../MVP-Scope.md#73-g2--gate-kinh-tế-sau-mvp1) đòi bốn tiêu chí. Đối chiếu với phạm vi MVP1 (`A1 = ⛔`, `A4 = ⛔` — ⛔ **không một tấm ảnh nào được sinh**):

| Tiêu chí | Đòi hỏi | Trạng thái | Vì sao |
|:-:|---|:-:|---|
| `G2-a` | Regen ratio `p50`/`p90` từ `usage_daily`, **≥1 chapter hoàn chỉnh** | ⛔ | MVP0 `P-3` **KHÔNG ĐẠT**; MVP1 ⛔ không sinh ảnh ⇒ ⛔ không có regen để đếm |
| `G2-b` | Margin `p50` trong dải **50–60%** `[BCN]`, COGS từ **`cost_usd` thực đo** | ⛔ | ⛔ Không có row `generation` ⇒ ⛔ không có `cost_usd` thực |
| `G2-c` | Margin `p90` **> 0%** | ⛔ | Cùng lý do |
| `G2-d` | Tỉ lệ user vượt **~125 ảnh/tháng** `[TC]` | ⛔ | ⛔ Không có ảnh/tháng để đếm |

⇒ Theo **đúng bảng kết quả của chính `MVP-Scope §7.3`**: *"`G2-a` ⛔ không đạt ⇒ **lùi gate**, ⛔ không PASS mặc định. **Thiếu dữ liệu ⛔ không phải bằng chứng tốt**."*

### 9.2 Việc phải làm trong tuần gate

| Việc | Vì sao vẫn phải làm |
|---|---|
| Ghi verdict `G2` = ⭐ **`KHÔNG CHẠY ĐƯỢC`** ra văn bản, kèm bốn dòng lý do ở [§9.1](#91-vì-sao-g2-⛔-không-chạy-được) | `KR3.2` đòi *"`G2` có verdict được ghi ra văn bản (PASS / FAIL / **KHÔNG CHẠY ĐƯỢC**) **trước 31/12/2026**"* ⇒ ⭐ **`KR3.2` vẫn ĐẠT** |
| Ghi rõ `KR3.1` ⛔ **KHÔNG ĐẠT** và lý do | `KR3.1` đòi `usage_daily` có `p50`/`p90` thực đo. ⛔ Không đạt là ⛔ không đạt — ⛔ không viết lại KR cho vừa kết quả |
| Chuyển câu hỏi kinh tế sang **MVP3**, ghi vào [Risk-Register](../Risk-Register.md) | Sau 3 tháng MVP1 vẫn ⛔ **chưa biết mô hình giá có sống được không**. Đó là rủi ro phải ở trên bảng, ⛔ không phải trong đầu |
| ⛔ **Không** tick `PASS`, ⛔ **không** tick `FAIL` | Cùng kỷ luật mà `g1-verdict.md` đã áp cho `G1`: tick một dải kết luận khi ⛔ không có số đo là **bịa ra một phép đo chưa từng xảy ra** |

---

## 10. Rủi ro & tín hiệu sớm

| # | Rủi ro | Mức | Tín hiệu sớm | Xử lý |
|:-:|---|:-:|---|---|
| `P-R1` | ⭐ **Load 100,5% ⇒ ⛔ không đệm** | **Cao** | `burn_tích_luỹ` > 105% ở retro bất kỳ sprint nào | Kích van kế tiếp theo [§6](#6-van-xả-xếp-sẵn--ngưỡng-kích). ⛔ **Không** nén ước lượng |
| `P-R2` | **7/26 story mang ước lượng `[EM]` do PM đặt**, ⛔ không phải từ story | **Cao** | Story đầu tiên trong nhóm này vượt >30% ước lượng | Ước lượng lại **cả 7**, ⛔ không chỉ story đang làm. Cập nhật [WBS-MVP1](../Estimates/WBS-MVP1.md) |
| `P-R3` | Khối multi-tenancy **15–25%** `[EM]` làm tràn (rủi ro lịch số 1 của cả roadmap) | **Cao** | `E-01` vượt 24h mà test rò rỉ chưa PASS | *"**Mua auth và billing, đừng viết**"* (Analysis §5.7). `E-04` là **mua**, ⛔ không tự viết |
| `P-R4` | Extraction kém trên truyện tiếng Việt scrape thật | Trung bình | `M1-3` dưới 80% ở lần chấm đầu | Tăng phần human-in-the-loop, ⛔ **không** kéo dài mốc |
| `P-R5` | Provenance bị commit tách rời artifact | **Cao về hậu quả** | Thấy code ghi `change_log` ở một service call khác | `M1-5` đòi **test** chứng minh cùng transaction — ⛔ không phải review bằng mắt |
| `P-R6` | ⭐ **MVP1–MVP2 xây trên tiền đề kỹ thuật chưa đo** (`G1` chưa chạy) | **Cao** | — (đã hiện thực hoá) | Ghi hàng mới vào [Risk-Register](../Risk-Register.md). Đo lại `G1` ở MVP3 |
| `P-R7` | Rơi vào cám dỗ build canvas | Trung bình | Bắt đầu viết zoom/pan hoặc hình học panel tự do | [MVP-Scope §4.1](../MVP-Scope.md#41-canvas-editor-14--cắt-một-phần-cf-91). MVP1 chỉ có **thành phần #5** |
| `P-R8` | `O4` bị bỏ rơi vì áp lực kỹ thuật | Trung bình | Hết một sprint mà ⛔ không có post nào | `KR4.3` (20 cuộc trò chuyện) ⛔ **không được cắt** — nó là cách duy nhất lấp khoảng trống *willingness-to-pay*. Van #3 chỉ cắt `KR4.2` |

---

## 11. Tài liệu tham khảo

### 11.1 Tài liệu trong repo

- [Roadmap.md](../Roadmap.md) — khung thời gian, đường găng, exit criteria `M1-1`…`M1-7`
- [MVP-Scope.md](../MVP-Scope.md) — bảng scope `§3`, danh sách cứng `KC-1`…`KC-7` `§6`, định nghĩa gate `§7`
- [OKRs.md](../OKRs.md) — `O1`…`O4` chu kỳ Q4/2026 và cách chấm
- [Charter-Comic-Studio.md](../Charter-Comic-Studio.md) — ràng buộc cấp dự án `C1`…`C9`
- [Risk-Register.md](../Risk-Register.md) — nơi `P-R6` và nợ `G2` phải được ghi vào
- [WBS-MVP1.md](../Estimates/WBS-MVP1.md) — bảng phân rã giờ chi tiết, nguồn của mọi con số ở `§5`
- [Sprint-001](../Sprints/Sprint-001.md) … [Sprint-006](../Sprints/Sprint-006.md) — mục tiêu, story, DoD từng sprint
- [`mvp0/golden-dataset/g1-verdict.md`](../../../mvp0/golden-dataset/g1-verdict.md) — biên bản khép MVP0 và sáu kết luận về hành vi model
- [`apps/backend/README.md`](../../../apps/backend/README.md) — cấu trúc backend hiện có và guardrail đang được cưỡng chế

### 11.2 ADR ràng buộc kế hoạch này

- [ADR-001](../../030-Specs/Architecture/ADR-001-Backend-And-Frontend-Tech-Stack.md) — stack cho `NEW-03`
- [ADR-006](../../030-Specs/Architecture/ADR-006-RLS-Tenant-Context-Injection.md) · [ADR-010](../../030-Specs/Architecture/ADR-010-Tenant-Isolation-With-RLS.md) — cách `E-01` phải được cài
- [ADR-008](../../030-Specs/Architecture/ADR-008-LLM-Provider-And-Usage-Boundaries.md) — ràng buộc cho `NEW-02`
- [ADR-011](../../030-Specs/Architecture/ADR-011-Narrative-Time-Key-And-State-Reduction.md) — cơ sở của `B-01` và `B-04`
- [ADR-015](../../030-Specs/Architecture/ADR-015-Job-Queue-In-Postgres.md) — cơ sở của `A-05`
- [ADR-017](../../030-Specs/Architecture/ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md) — cơ sở của `G-01` và `G-02`
- [ADR-018](../../030-Specs/Architecture/ADR-018-Usage-Event-And-Rollup-Model.md) — cơ sở của `F-01`

---

_Created by product-manager_
_Author: trisjr_
