---
id: SPEC-API-GENERATION
type: spec
status: draft
project: comic-studio
created: 2026-08-29
---

# Endpoint: Generation (sinh ảnh + trạng thái job)

Bề mặt API của **đường sinh ảnh** — luồng `F5`, luồng **dày ràng buộc nhất** của hệ thống. Generation và job ở chung một file vì job ⛔ **không có vòng đời độc lập**: chúng được `INSERT` trong **cùng một transaction** (`D-03`). Một file riêng cho *"get job"* sẽ mô tả một thứ không tồn tại một mình.

**Decided in:**

- [ADR-014 — Prompt compiler deterministic + best-of-N](../Architecture/ADR-014-Deterministic-Prompt-Compiler-And-Best-Of-N.md) — điều 1–3, 5–8, 10 (`D-34`…`D-39`, `D-44`)
- [ADR-015 — Job queue trong PostgreSQL](../Architecture/ADR-015-Job-Queue-In-Postgres.md) — `Q1` (transactional enqueue), `Q5` (taxonomy lỗi), ⭐ `Q6` (`CT-POLL-2S`)
- [ADR-016 — Image provider adapter + pin model version](../Architecture/ADR-016-Image-Provider-Adapter-And-Version-Pinning.md) — `Q1`, `Q2`, `Q3`
- [ADR-017 — Chuỗi provenance và MỘT transaction boundary](../Architecture/ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md) — `Q2`, `Q4.1`, `Q4.2`, `Q4.3` `P-2`, `Q4.5`
- [ADR-018 — Mô hình `usage_event` và rollup](../Architecture/ADR-018-Usage-Event-And-Rollup-Model.md) — `Q3`, `Q5`
- [ADR-007 — VLM provider cho QA-select](../Architecture/ADR-007-VLM-Provider-For-QA-Select.md) · [ADR-004 — Object storage + signed URL](../Architecture/ADR-004-Object-Storage-Vendor-And-Signed-URL.md) · [ADR-006 — RLS & tenant context](../Architecture/ADR-006-RLS-Tenant-Context-Injection.md)
- [SDD Comic Studio](../Architecture/SDD-Comic-Studio.md) — §5.2 `F5`, §6.2, §6.4
- [`DB-Entity-Generation.md`](../Schema/DB-Entity-Generation.md) · [`DB-Entity-Job-Queue.md`](../Schema/DB-Entity-Job-Queue.md) · [`DB-Entity-Provenance-And-Usage.md`](../Schema/DB-Entity-Provenance-And-Usage.md) · [`DB-Entity-Tenancy.md`](../Schema/DB-Entity-Tenancy.md) · [`DB-Entity-Credit-Ledger.md`](../Schema/DB-Entity-Credit-Ledger.md)

---

## 1. Resource

| Resource | Bảng DB | Vai trò trong file này |
|---|---|---|
| Lần compile prompt | `generation.prompt_compilation` | Ghi ở đường API, **lúc enqueue** |
| Mắt xích sinh ảnh | `generation.generation` | ⭐ Phân biệt bằng `generation_kind` — xem [§4.1](#41-generation_kind--một-dòng-request-nhiều-dòng-candidate) |
| Điểm chấm VLM | `generation.vlm_evaluation` | Chỉ **đọc** ở file này |
| Đơn vị công việc | `public.job` | ⭐ `job_type = 'generate_panel'` — **giá trị duy nhất** của danh mục đóng |
| Bản ghi tiêu tài nguyên | `public.usage_event` | ⭐ **Đồng nhất: một dòng = một image candidate.** ⛔ Không endpoint nào ở đây ghi nó — xem [§4.5](#45-usage_event-và-chi-phí-vlm--quyết-định-c) |
| Chi phí VLM-select | `generation.vlm_scoring_call` | ⭐ Bảng **riêng**, ⛔ **không** trong `usage_event` |
| Lựa chọn của người | `comic.panel.approved_generation_id` | Ghi bởi `#4` |

---

## 2. Quy ước chung — ⛔ file này KHÔNG đặc tả lại bốn ràng buộc xuyên-endpoint

| Mã | Ràng buộc | Nguồn **DUY NHẤT** | File này được làm gì |
|---|---|---|---|
| `SDD-HG-01` | Hai human gate | [SDD §6.3](../Architecture/SDD-Comic-Studio.md) | Trỏ `.4` + hệ quả #1. ⚠️ **Sinh ảnh ⛔ KHÔNG bị chặn bởi gate** — `.4` chặn **xuất bản**, ⛔ không chặn sinh ảnh (xem `API-GEN-13`) |
| `KC-4` | Artifact + bằng chứng, **một** transaction | [ADR-017 `Q4`](../Architecture/ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md) | Trỏ `Q2` + `Q4.3` `P-2` (`Q4.7`), và `Q4.1`/`Q4.2` tại `#4`. ⛔ Không viết *"tầng DB cưỡng chế `KC-4`"* (`Q4.6`). ⚠️ Nhớ `Q4.5`: `KC-4` ⛔ **không** phải *"một transaction cho cả vòng đời job"* |
| `CT-POLL-2S` | Polling **2 giây**, ⛔ không WebSocket / SSE / long-poll. ⭐ Độ rắn **MẶC ĐỊNH**, ⛔ **không nâng thành `CHỐT`** | [ADR-015 `Q6`](../Architecture/ADR-015-Job-Queue-In-Postgres.md) | Thiết kế `#6` **rẻ để gọi lặp** ([§4.6](#46-6-trạng-thái-job--endpoint-bị-gọi-nhiều-nhất-hệ-thống)). ⛔ Không tự đặt lại interval, ⛔ không mô tả nó là *"cấu hình tuỳ client"* |
| RLS + tenant context | Mọi query qua RLS; worker `claimJobAndBindTenant()` | [ADR-006](../Architecture/ADR-006-RLS-Tenant-Context-Injection.md) | Cột `Auth`. ⛔ Cơ chế bơm context ⛔ không lặp ở đây |

**Quy ước mã lỗi**: `HTTP status` + `error_code` `SCREAMING_SNAKE` ổn định (`T-API-ERR`).

> [!CAUTION]
> ⛔ **`SRS-NFR-15` — ⛔ KHÔNG endpoint nào trong file này gọi copyright detection / similarity detection.**
> ⚠️ **Chỗ dễ đọc nhầm nhất của cả 14 file nằm đúng ở đây**: hệ thống **có** một VLM chấm ảnh — nhưng nó là **Continuity Checker** (nhất quán nhân vật/bối cảnh giữa N candidate), ⛔ **không** phải checker bản quyền. ⛔ Không thêm một *"similarity score với tác phẩm khác"* vào `#2`/`#3` dưới bất kỳ tên nào. Anti-feature **có chủ ý** ([SDD §5.4](../Architecture/SDD-Comic-Studio.md)).

---

## 3. ⭐ Chống lạm dụng chi phí ở MVP1–MVP2 = RATE LIMIT, ⛔ KHÔNG phải HOLD credit

> [!IMPORTANT]
> ⭐ **Quyết định của Founder tại gate Phase 2** ([escalations `E9`](../../010-Planning/pm-runs/2026-08-28-phase-2-architecture-design-comic-studio/escalations.md), 2026-08-29): thay cho **HOLD credit** ở `UC-06` bước 3–4, ở **MVP1–MVP2** hệ thống dùng **rate limit per tenant cho hành động `generate`**.
> ⇒ `Endpoint-Generation.md` là **file API chịu trách nhiệm** cho contract này.

| # | Diễn giải bắt buộc | Hệ quả trên contract của `#1` |
|:--:|---|---|
| 1 | Mở rộng **đúng cơ chế đã có** (rate limit per tenant, đang áp cho `upload`) sang `generate` | ⛔ Không cơ chế thứ hai |
| 2 | ⭐ **Đếm SỐ REQUEST trong một khung thời gian, ⛔ KHÔNG đếm tiền/credit** | Bộ đếm tăng **1 mỗi lời gọi `#1`**, ⛔ không nhân theo `N`, ⛔ không theo `cost_usd` |
| 3 | ⛔ **Không entity kiểu ledger, ⛔ không bảng `credit_*` cho việc này** | ⛔ `#1` không đọc/ghi `public.credit_ledger` hay `public.credit_hold` — hai bảng đó **tồn tại rỗng** trong toàn horizon (`CR-5` của [`DB-Entity-Credit-Ledger.md`](../Schema/DB-Entity-Credit-Ledger.md)) |
| 4 | Áp **độc lập theo `tenant_id`** | Một tenant chạm ngưỡng ⛔ không ảnh hưởng tenant khác |
| 5 | ⭐ **Fail-safe**: bộ đếm mất do restart ⇒ về trạng thái **an toàn (chặn tạm)**, ⛔ **không mặc định cho qua** | Mất state ⇒ `429`, ⛔ không `200` |
| 6 | ⭐ **Ngưỡng để `TBD`** (`SRS-NFR-20`) | ⛔ **Không con số nào trong file này** — kể cả trong ví dụ, kể cả trong `Retry-After`. Hàng `T-10` |

> [!IMPORTANT]
> ⭐ **Mã lỗi `429` của `#1` là `RATE_LIMITED`, ⛔ KHÔNG phải một mã riêng.** ⚠️ Đính chính ở lô **`L34`**: bản trước của file này dùng ~~`GENERATE_RATE_LIMIT_EXCEEDED`~~ trong khi bảng mã dùng chung `API-ENV-1` ([`Endpoint-Project.md`](./Endpoint-Project.md)) đã chốt `429 RATE_LIMITED`. Đó là **hai TÊN cho MỘT điều kiện**, ⛔ không phải hai điều kiện ⇒ **rút tên riêng**, dùng mã dùng chung.
>
> ⭐ **Vì sao ⛔ không giữ hai mã**: danh mục `code` là **đóng** (`API-ENV-1`), và khoá đếm của `RL-1` đã là `(tenant_id, action)` với `action ∈ {upload, generate}` ⇒ *"vượt rate limit"* là **một** điều kiện có tham số, ⛔ không phải hai điều kiện. ⚠️ **Ngữ nghĩa riêng của `generate` theo `E9` (đếm số REQUEST, fail-safe chặn tạm khi mất state, ngưỡng `TBD`) ⛔ KHÔNG mất đi** — nhưng đó là **hành vi phía server**, ⛔ **không** phải nhánh mà client rẽ theo tên mã. ⛔ Không client nào cần phân biệt hai tên để xử lý đúng.
>
> ⚠️ ⛔ **Không** thêm trường phân biệt `action` vào `details` ở lô này: hình dạng `details` thuộc `TBD-API-ENV` **còn mở** — quyết ở đây là nhét một quyết định contract vào một lần đổi tên.

**State sống ở đâu** — quyết định của lô Schema, ⭐ file này **trỏ, ⛔ không quyết lại**: `RL-1` của [`DB-Entity-Tenancy.md`](../Schema/DB-Entity-Tenancy.md) chốt state của rate limit ⛔ **KHÔNG** là một entity trong data model — nó là **state vận hành phù du ở tầng ứng dụng, trong tiến trình**, khoá đếm `(tenant_id, action)` với `action ∈ {upload, generate}`.

> [!CAUTION]
> ⛔ **Ba lệnh cấm cấu trúc — chép từ [`DB-Entity-Tenancy.md`](../Schema/DB-Entity-Tenancy.md) vì chúng là ràng buộc trực tiếp lên đường code của `#1`:**
> đường rate limit ⛔ **không được đọc `generation.generation.cost_usd`**, ⛔ **không được đếm dòng `public.usage_event`**, ⛔ **không được tham chiếu bất kỳ bảng `credit_*` nào.**
> Lý do: đếm theo tiền biến rate limit thành **hard quota cưỡng chế chi phí** — đúng thứ thuộc `KC-7`/MVP3 và đúng thứ anti-scope của `Story-Minimum-Abuse-Controls` cấm.

⚠️ **`UC-06` bước 3 (*"HOLD 3 credit TRƯỚC enqueue"*) vì vậy ⛔ KHÔNG hiện thực trọn vẹn ở horizon này** — đó là hàng `T-25` ở [SDD §9.1](../Architecture/SDD-Comic-Studio.md), một **quyết định sản phẩm đã được đưa ra**, ⛔ không phải một bước bị quên. **Vị trí** của HOLD trong luồng (`trước enqueue`, ⛔ không phải *check-rồi-gọi*) vẫn giữ nguyên như seam `S-2` — ⛔ không được để trống cho tương lai chèn vào sau.

---

## 4. Danh sách endpoint

| # | Method · Path | Auth | Request | Response | Mã lỗi |
|--:|---|---|---|---|---|
| 1 | `POST /v1/panels/{panel_id}/generations` | tenant member | `{relation_kind?: 'retry'\|'variation'\|'refine'\|'continuity_fix', parent_generation_id?: uuid, emphasis_note?: string}` | `202` `{request_generation_id, job_id, prompt_compilation_id, degradations[]}` | `403 PROJECT_ACCESS_DISABLED` · `404 PANEL_NOT_FOUND` · `409 PANEL_SPEC_INCOMPLETE` · `422 PROMPT_COMPILE_UNKNOWN_FIELD` · `422 PROMPT_COMPILE_CONFLICT` · `422 PROMPT_COMPILE_BUDGET_EXCEEDED` · `422 UNKNOWN_RELATION_KIND` · ⭐ `429 RATE_LIMITED` |
| 2 | `GET /v1/panels/{panel_id}/generations` | tenant member | query: `?generation_kind=`, `?request_generation_id=` | `200` `{items[]: GenerationSummary, checker_coverage}` | `403 PROJECT_ACCESS_DISABLED` · `404 PANEL_NOT_FOUND` |
| 3 | `GET /v1/generations/{generation_id}` | tenant member | — | `200` `GenerationDetail` (kèm `vlm_evaluation`) | `403 PROJECT_ACCESS_DISABLED` · `404 GENERATION_NOT_FOUND` |
| 4 | `PUT /v1/panels/{panel_id}/approved-generation` | tenant member | `{generation_id: uuid}` | `200` `{panel_id, approved_generation_id, change_log_id}` | `403 PROJECT_ACCESS_DISABLED` · `404 PANEL_NOT_FOUND` · `404 GENERATION_NOT_FOUND` · `409 GENERATION_NOT_CANDIDATE` · `409 GENERATION_NOT_FOR_THIS_PANEL` · `422 GENERATION_HAS_NO_ARTIFACT` |
| 5 | `GET /v1/generations/{generation_id}/image-url` | tenant member | — | `200` `{url, expires_at}` | `403 PROJECT_ACCESS_DISABLED` · `404 GENERATION_NOT_FOUND` · `422 GENERATION_HAS_NO_ARTIFACT` |
| 6 | `GET /v1/jobs/{job_id}` | tenant member | — | `200` `{job_id, status, attempt_count, max_attempts, run_after, last_error_class, request_generation_id}` | `403 PROJECT_ACCESS_DISABLED` · `404 JOB_NOT_FOUND` |
| 7 | `GET /v1/panels/{panel_id}/jobs` | tenant member | query: `?status=` | `200` `{items[]: JobSummary}` | `403 PROJECT_ACCESS_DISABLED` · `404 PANEL_NOT_FOUND` |

> [!CAUTION]
> ⚠️⭐ **Trước lô này file chỉ phủ `#5` — phủ MỘT PHẦN nguy hiểm hơn ⛔ không phủ**, vì nó tạo cảm giác *"file này đã lo rồi"*. Nay **cả bảy** endpoint kiểm cờ disable-access: `#3` trả `GenerationDetail` (**prompt đã compile + đánh giá VLM** của nội dung đã bị hạ), `#6`/`#7` trả trạng thái job — ⛔ **không** endpoint nào trong số đó được miễn chỉ vì path ⛔ không mang `project_id` (`C3-K1`: định danh bằng `panel_id` / `generation_id` / `job_id` ⇒ **resolve ngược lên project** rồi mới kiểm).
> Luật ở [`API-PRJ-4`](./Endpoint-Project.md#invariant-của-resource) — ⛔ file này **không chép lại**, chỉ trỏ theo mã: **đúng một** hàm dùng chung ở tầng service (`C3-K3`), **fail-closed** khi ⛔ không thấy row `public.project_access_state` (`C3-K2`). Cưỡng chế bằng **test bảng route toàn cục** khuôn `M1-1`, ⛔ **không** test per-endpoint (`C3-K4`). Danh sách đóng: [Threat Model §4.4](../Security/Spec-Security-Threat-Model.md#44--c-3-danh-sách-đóng-các-đường-đọc-phải-kiểm-cờ-disable-access).
> ⛔ **`deleted_at` ⛔ KHÔNG BAO GIỜ được đọc thành trạng thái takedown** — hai cột độc lập (`C3-K7`).

---

## 4bis. Chi tiết các endpoint có ràng buộc

### 4.1 `generation_kind` — một dòng `request`, nhiều dòng `candidate`

⭐ **Quyết định `CO-1.1` phương án (a)** ([escalations `E17`](../../010-Planning/pm-runs/2026-08-28-phase-2-architecture-design-comic-studio/escalations.md)) — hình dạng đã áp ở [`DB-Entity-Generation.md`](../Schema/DB-Entity-Generation.md):

| `generation_kind` | Ghi lúc nào | Bốn trường `D-59` (`attempt_no`, `model_id`, `model_version`, `cost_usd`) | Ai ghi |
|---|---|---|---|
| `'request'` | ⭐ **Lúc enqueue** — ⛔ chưa gọi provider lần nào | ⛔ **luôn `NULL`** (`G-6`); `cost_status` cũng `NULL` (`G-5`) | Đường API — `#1` |
| `'candidate'` | ⭐ **Lúc hoàn tất** một lời gọi provider | ⭐ **`NOT NULL`** (trừ `cost_usd` khi `cost_status = 'unknown_provider_error'`) | Đường worker — ⛔ **không phải bề mặt API** |

⛔ **Tuyệt đối không ghi *model dự kiến* vào dòng `request`** — `model_id` là model **THỰC SỰ ĐƯỢC GỌI**, vì provider có thể tự fallback.

⇒ Hệ quả cho response: `#1` trả `request_generation_id` (dòng cấp request), ⛔ **không** trả `model_id`/`cost_usd` — chúng chưa tồn tại và ⛔ **không** được đoán trước.

### 4.2 `#1` — nội dung transaction enqueue

| Bước | Câu ghi | Neo |
|:--:|---|---|
| 1 | **Kiểm rate limit** (đếm request, per tenant) — ⛔ trước mọi việc khác | [§3](#3--chống-lạm-dụng-chi-phí-ở-mvp1mvp2--rate-limit--không-phải-hold-credit) |
| 2 | **Compile deterministic** → `INSERT generation.prompt_compilation` (`text_prompt`, `conditioning_set`, `negative_prompt`, `compiler_version`, `input_spec_hash`, `output_hash`) | [ADR-014](../Architecture/ADR-014-Deterministic-Prompt-Compiler-And-Best-Of-N.md) điều 1, 3 |
| 3 | `INSERT generation.generation` với `generation_kind = 'request'`, `origin = 'ai'`, `parent_generation_id` (nếu là `retry`/`variation`/`refine`/`continuity_fix`) | `GR-1`, `GR-4` · `SRS-FR-34` |
| 4 | `INSERT public.job` với `job_type = 'generate_panel'`, `payload = {"generation_id": …}` | [ADR-015 `Q1`](../Architecture/ADR-015-Job-Queue-In-Postgres.md) |
| 5 | ⭐ **`COMMIT` — bốn bước trên là MỘT transaction** ⇒ ⛔ không job mồ côi, ⛔ không `generation` chờ mãi mà không có job đẩy đi | `D-03` · [ADR-015 `Q1`](../Architecture/ADR-015-Job-Queue-In-Postgres.md) |

⛔ **Ba thứ `#1` KHÔNG làm:**

| ⛔ Không làm | Vì sao |
|---|---|
| ⛔ **Không `INSERT public.usage_event`** | `U-2`: lúc enqueue ⛔ chưa tiêu tài nguyên nào; ghi trước là ghi một sự kiện **chưa xảy ra** ([`DB-Entity-Provenance-And-Usage.md`](../Schema/DB-Entity-Provenance-And-Usage.md)) |
| ⛔ **Không HOLD credit, ⛔ không chạm `credit_*`** | Quyết định gate Phase 2 — [§3](#3--chống-lạm-dụng-chi-phí-ở-mvp1mvp2--rate-limit--không-phải-hold-credit) |
| ⛔ **Không gọi provider** | Provider chỉ được gọi ở đường worker, sau khi job được claim (`FOR UPDATE SKIP LOCKED`) |

> [!WARNING]
> ⚠️ **Một chênh lệch phải ghi ra, ⛔ không im lặng**: sơ đồ [SDD §5.2 `F5`](../Architecture/SDD-Comic-Studio.md) vẽ `INSERT change_log` **ở bước enqueue**. Contract trên **⛔ không có** bước đó, vì hai căn cứ:
> 1. [ADR-015 `Q1`](../Architecture/ADR-015-Job-Queue-In-Postgres.md) định nghĩa enqueue là `INSERT generation` + `INSERT job`, ⛔ không nêu `change_log`.
> 2. Danh mục `action_type` **đóng** của `public.change_log` ⛔ **không có giá trị nào** cho *"ra lệnh generate"*, và bảng đó được định nghĩa là *"một dòng = **một hành động của con người**"* ([`DB-Entity-Provenance-And-Usage.md`](../Schema/DB-Entity-Provenance-And-Usage.md)). `UC-06` đặt `change_log` ở **bước 9 (approve)**, ⛔ không ở bước enqueue.
> ⇒ File này theo **ADR + Schema**. Chênh lệch với sơ đồ đi vào báo cáo ripple (tầng `Architecture/` đã đóng), ⛔ **không tự sửa SDD**, ⛔ **không tự nới `CHECK`**. Xem [`T-GEN-CL-ENQUEUE`](#7-tbd-còn-lại---không-được-bịa).

**Ba mã lỗi compile — ⛔ compiler im lặng thì không bao giờ sai** ([ADR-014](../Architecture/ADR-014-Deterministic-Prompt-Compiler-And-Best-Of-N.md) điều 2):

| Tình huống | Mã lỗi | Hành vi bắt buộc |
|---|---|---|
| Spec chứa field **không có trong bảng tra** | `422 PROMPT_COMPILE_UNKNOWN_FIELD` | **Báo lỗi rõ ràng** — ⛔ không tự bịa cụm từ, ⛔ không bỏ qua âm thầm |
| Hai ràng buộc xung đột **cùng bậc cao nhất** của precedence ladder | `422 PROMPT_COMPILE_CONFLICT` | **Dừng và yêu cầu sửa spec** — ⛔ không tự chọn một bên |
| Budget vượt tới mức **identity refs cũng phải drop** | `422 PROMPT_COMPILE_BUDGET_EXCEEDED` | **Từ chối sinh prompt** — đây là **lỗi thiết kế spec**, ⛔ không sinh prompt thiếu identity |

⭐ **`degradations[]` trong response `202` là bắt buộc**: mọi ràng buộc thị giác bị loại do vượt constraint budget phải trồi lên tới người dùng, ⛔ không chìm xuống thành ảnh xấu (`SRS-FR-17`; guardrail observability #2 của [SDD §6.4](../Architecture/SDD-Comic-Studio.md)). ⭐ **Identity refs ⛔ KHÔNG BAO GIỜ bị drop** — nếu buộc phải drop thì đã là `422` ở hàng cuối bảng trên.

### 4.3 `#2` / `#3` — đọc candidate, và ba thứ ⛔ KHÔNG được bóp méo

| Điều | Nội dung |
|---|---|
| ⭐ **Giữ CẢ N candidate** | ⛔ **Hai candidate không được chọn KHÔNG bị xoá khỏi lineage** (`UC-06`). Cưỡng chế nền: `parent_generation_id … ON DELETE RESTRICT` ⇒ ⛔ **không có endpoint `DELETE` generation** trong file này |
| ⭐ **`unclear` là giá trị hợp lệ HẠNG NHẤT** | Response trả `verdict ∈ {pass, fail, unclear}` **nguyên trạng**. ⛔ Không map `unclear` sang `pass`/`fail`, ⛔ không coi nó là `NULL`, ⛔ không coi là lỗi |
| ⭐ **VLM chỉ *preselect*** | `is_preselected = true` là **gợi ý**, ⛔ **không** tự thành lựa chọn của người. Người chọn bằng `#4`. ⛔ **Không có `[Fix automatically]`**, ⛔ không endpoint auto-approve, ⛔ không tham số `apply_preselected=true` |
| **Side-by-side** | `#2` trả **đủ** N candidate để client hiện side-by-side; ⛔ không lọc bớt theo `verdict` |
| **`check_results`** | Mỗi check kèm `mode ∈ {report_only, influencing}` **của chính lần chấm đó** — ⭐ mặc định mọi check là `report_only` ([ADR-007 `Q3`](../Architecture/ADR-007-VLM-Provider-For-QA-Select.md)). ⛔ Không đọc mode từ một cấu hình toàn cục lúc hiển thị |
| ⭐ **`checker_coverage`** | Bắt buộc trong response `#2`, dạng *"đã kiểm **N/M** panel, **M−N** panel không kiểm được vì có nhiều nhân vật"*. ⭐ Đây là **FR minh bạch** (`SRS-FR-22`, `D-39`), ⛔ **không phải chỉ tiêu chất lượng** ⇒ ⛔ **không được giấu con số này để trông đẹp hơn** |
| **Trường provenance** | `#3` trả `generation_kind`, `parent_generation_id`, `relation_kind`, `origin`, `attempt_no`, `model_id`, `model_version`, `cost_usd`, `cost_status`, `seed`, `degradations`, `completed_at` |
| ⚠️ **`seed`** | ⭐ **PROVENANCE METADATA, ⛔ KHÔNG PHẢI REPLAY KEY** (`D-44`). ⛔ Response ⛔ không được gợi ý *"chạy lại cho ra đúng ảnh này"*; mục tiêu là **auditability + lineage**, ⛔ không phải reproducibility |
| ⚠️ **`cost_status`** | `'unknown_provider_error'` phải hiện **tường minh**, ⛔ không hiển thị ngầm là `0`, ⛔ không ẩn đi ([ADR-018 `Q4`](../Architecture/ADR-018-Usage-Event-And-Rollup-Model.md)) |

⚠️ **`N = 3` là MẶC ĐỊNH, ⛔ không phải bất biến** (`D-37`); best-of-N ⛔ **không phải retry-on-failure** — sinh N candidate cho **MỌI** panel rồi chọn 1. ⇒ ⛔ Client ⛔ không được hard-code `3`; đọc theo số phần tử trả về.

### 4.4 `#4` — ⭐ hành động AUTHORSHIP, nội dung transaction

⭐ Đây là điểm mà *"decisive contribution"* được ghi lại. Transaction gồm **đúng ba** câu ghi:

| Bước | Câu ghi | Neo |
|:--:|---|---|
| 1 | `UPDATE comic.panel SET approved_generation_id = :generation_id` | `E-4` · `INV-12` của [`DB-Entity-Comic-IR.md`](../Schema/DB-Entity-Comic-IR.md) |
| 2 | `INSERT public.change_log` với ⭐ `action_type = 'select_generation'`, `origin = 'human'`, `detail` = *generation nào được chọn thay generation nào* | [ADR-017 `Q2`](../Architecture/ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md) · `SRS-FR-35` |
| 3 | `INSERT public.field_provenance` cho field `approved_generation_id`, `origin = 'human'`, `change_log_id` trỏ bước 2 | [ADR-017 `Q3`, `Q4.2`](../Architecture/ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md) hàng 4 |
| 4 | ⭐ **Một transaction, boundary per-request** | [ADR-017 `Q4.1`, `Q4.3`](../Architecture/ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md) `P-2` |

> [!IMPORTANT]
> ⛔ **HAI thứ `#4` KHÔNG làm — và cả hai đều trái với mô tả trong `findings/architect §4.1` hàng #9.** Nguồn thắng là **Schema + quyết định gate**:
> 1. ⛔ **KHÔNG ghi `public.usage_event`.** Dòng usage được `INSERT` **trong chính transaction ghi dòng `generation` của candidate đó**, tức **lúc candidate hoàn tất** (`U-1`), và **ba dòng candidate được ghi TRƯỚC khi biết kết quả VLM-select** (`U-3`). ⇒ Tới lúc `#4` chạy, `usage_event` **đã tồn tại**. Ghi thêm ở đây là **đếm đôi**.
> 2. ⛔ **KHÔNG settle hold.** ⛔ Không có HOLD ở MVP1–MVP2 ([§3](#3--chống-lạm-dụng-chi-phí-ở-mvp1mvp2--rate-limit--không-phải-hold-credit), `CR-5`).

**Ba mã lỗi có ràng buộc**:

| Mã lỗi | Điều kiện | Vì sao |
|---|---|---|
| `409 GENERATION_NOT_CANDIDATE` | `generation_kind = 'request'` | ⛔ Dòng cấp request ⛔ không có artifact — nó ⛔ không phải một *"bản"* để duyệt |
| `409 GENERATION_NOT_FOR_THIS_PANEL` | Generation không thuộc chuỗi của panel này | Đường tra `panel → prompt_compilation → generation` nằm **trọn trong schema `generation`** (`G-9`) |
| `422 GENERATION_HAS_NO_ARTIFACT` | `image_object_key IS NULL` | Lần gọi ⛔ không tạo ra artifact (lỗi/bị từ chối) ⇒ ⛔ không có gì để duyệt |

⭐ **Đổi lựa chọn được**: `approved_generation_id` ⛔ **KHÔNG** UNIQUE, ⛔ không `NOT NULL` (`INV-12`) ⇒ mỗi lần đổi là **một** `change_log` mới, ⛔ không ghi đè bằng chứng cũ.

### 4.5 `usage_event` và chi phí VLM — quyết định `(C)`

> [!IMPORTANT]
> ⭐ **`public.usage_event` là bảng ĐỒNG NHẤT: một dòng = MỘT image candidate đã sinh.** ⛔ Không cột phân loại, ⛔ không dòng nào không ứng với một candidate ([`E20`](../../010-Planning/pm-runs/2026-08-28-phase-2-architecture-design-comic-studio/escalations.md)).
> ⇒ Một lần best-of-N với `N = 3` tạo **ĐÚNG 3** dòng; `COUNT(*)` cho một request có **trần = 3**.
> ⭐ **Chi phí VLM-select nằm ở bảng RIÊNG `generation.vlm_scoring_call`**, ⛔ **KHÔNG** trong `usage_event`, ⛔ **không** trong `generation.vlm_evaluation` (bảng đó giữ **điểm chấm**, bảng kia giữ **tiền**).

| Điều | Nội dung | Neo |
|---|---|---|
| ⛔ **Không endpoint nào trong file này ghi `usage_event`** | Cả 7 endpoint đều không. Đường ghi là **transaction hoàn tất candidate ở worker** | `U-1`, `U-2`, `U-3` |
| **Tiền đã tiêu là tiền đã tiêu** | Dòng usage tồn tại **kể cả** khi candidate đó không được chọn, và **kể cả** khi VLM-select timeout sau khi 3 candidate đã sinh | `U-3` · [ADR-018 `Q5`](../Architecture/ADR-018-Usage-Event-And-Rollup-Model.md) |
| **VLM lỗi sau khi đã gọi** | Dòng `vlm_scoring_call` **vẫn được ghi** với `cost_state = 'unknown'`. ⛔ Không xoá dòng, ⛔ không ghi `0` | `U-4b` |
| ⛔ **Không `UPDATE` để bổ sung cost về sau** | Sửa sai bằng **event bù**, ⛔ không bằng `UPDATE` (append-only `GR-3`) | `U-5` |
| **Ràng buộc để lại cho lô Integration** | `provider_call_ref` và `vlm_call_ref` phải **bền qua retry** (sinh **trước** lời gọi, lưu cùng kết quả) — ⛔ không sinh lại mỗi lần worker nhặt job | Đích: [`Spec-Integration-Image-Provider.md`](./Spec-Integration-Image-Provider.md) · [`Spec-Integration-VLM-QA-Select.md`](./Spec-Integration-VLM-QA-Select.md) |

### 4.6 `#6` trạng thái job — endpoint bị gọi nhiều nhất hệ thống

| Điều | Nội dung |
|---|---|
| `CT-POLL-2S` | Client poll **mỗi 2 giây** cho mỗi job đang chạy. ⛔ Không WebSocket, ⛔ không SSE, ⛔ không long-poll. ⭐ Độ rắn **MẶC ĐỊNH** — ⛔ **không nâng thành `CHỐT`**; đường lui là *"tiền đề đảo (generation nhanh hơn nhiều) thì mở lại được"* |
| ⭐ **Phải RẺ** | ⛔ **Không aggregate nặng, ⛔ không join xuyên schema** ([ADR-015 `Q6`](../Architecture/ADR-015-Job-Queue-In-Postgres.md)). ⇒ Response lấy **chỉ** từ `public.job` (+ `payload->>'generation_id'`). ⛔ **Không** đếm candidate đã sinh, ⛔ không kèm điểm VLM, ⛔ không kèm `cost_usd` — muốn những thứ đó thì gọi `#2` |
| **`status`** | Đúng 5 giá trị của danh mục đóng: `queued`, `running`, `succeeded`, `failed_permanent`, `failed_exhausted` ([ADR-015 `Q5`](../Architecture/ADR-015-Job-Queue-In-Postgres.md)) |
| **`last_error_class`** | Đúng 5 giá trị: `transient_infra`, `transient_provider`, `permanent_input`, `permanent_policy`, `permanent_unknown`. ⚠️ `permanent_unknown` **phải xuất hiện được trong chẩn đoán**, ⛔ không im lặng |
| ⛔ **Không rò rỉ** | ⛔ Response ⛔ không trả `claimed_by`, ⛔ không trả `last_error_detail` thô nếu nó có thể chứa dấu vết cấu hình provider; `last_error_detail` ⛔ **không được chứa secret/API key** ngay từ lúc ghi |
| **`#7` khác `#6`** | ⚠️ `#7` phải đi qua **hai schema** (`generation` để tra panel → generation, `public` để tra job qua `payload`) ⇒ ⛔ **không nằm trên đường polling**, ⛔ **không được dùng thay `#6`**. Nó phục vụ màn hình lịch sử, gọi **thưa** |

### 4.7 `#5` signed URL — ⛔ không bao giờ là blob

| Điều | Nội dung |
|---|---|
| **Hình dạng** | Trả **URL có chữ ký** + `expires_at`. ⛔ **Không stream bytes qua API**, ⛔ **không base64 trong JSON** |
| **Key** | `tenant/{tenant_id}/{sha256}` — content-address **trong phạm vi tenant** ([ADR-004](../Architecture/ADR-004-Object-Storage-Vendor-And-Signed-URL.md)) |
| ⛔ **Không blob trong DB** | `B-4` — ⛔ không cột binary ở bất kỳ bảng nào |
| **TTL** | Thuộc [ADR-004](../Architecture/ADR-004-Object-Storage-Vendor-And-Signed-URL.md) — ⛔ file này **không đặt con số** |
| `403 PROJECT_ACCESS_DISABLED` | Project đang ở trạng thái **disable-access** do takedown ⇒ ⛔ không cấp URL. Nguồn trạng thái: `public.project_access_state` ([`DB-Entity-Compliance-And-Takedown.md`](../Schema/DB-Entity-Compliance-And-Takedown.md)). ⚠️ **Fail-closed**: ⛔ không thấy row ⇒ **cũng từ chối** (`C3-K2`) |
| ⛔ **Không TTL/eviction** trên object mà panel đã duyệt trỏ tới | Mất một object = mất **vĩnh viễn** một mắt xích provenance (`D-44`, `INV-11`) |

> [!WARNING]
> ⭐ **Ranh giới thành thật của việc kiểm cờ (`C3-K6`)** — một **signed URL đã phát TRƯỚC** khi takedown có hiệu lực **vẫn đọc được cho tới khi hết TTL**, và ⛔ **không thu hồi được**. ⇒ Kiểm cờ chặn **việc CẤP quyền đọc**, ⛔ **không** chặn quyền đọc **đã rời khỏi hệ thống**.
> ⚠️ **Cận trên của cửa sổ đó chính là `T-7`** (TTL của signed URL, thuộc [ADR-004](../Architecture/ADR-004-Object-Storage-Vendor-And-Signed-URL.md) — ⛔ file này không đặt số). ⇒ ⛔ **KHÔNG được** tuyên bố *"nội dung đã bị hạ hoàn toàn"* trong khi `T-7` còn mở. Xem [Threat Model §4.4](../Security/Spec-Security-Threat-Model.md#44--c-3-danh-sách-đóng-các-đường-đọc-phải-kiểm-cờ-disable-access) `C3-K6`.

---

## 5. Invariant của resource

| Mã | Invariant | Neo |
|---|---|---|
| `API-GEN-1` | ⭐ **Enqueue là transactional**: `prompt_compilation` + `generation('request')` + `job` trong **MỘT** transaction ⇒ ⛔ không job mồ côi | `D-03` · [ADR-015 `Q1`](../Architecture/ADR-015-Job-Queue-In-Postgres.md) |
| `API-GEN-2` | ⭐ **⛔ Không HOLD credit ở MVP1–MVP2.** Chống lạm dụng = **rate limit đếm SỐ REQUEST**; ⛔ không đọc `cost_usd`, ⛔ không đếm `usage_event`, ⛔ không chạm `credit_*` | [`E9`](../../010-Planning/pm-runs/2026-08-28-phase-2-architecture-design-comic-studio/escalations.md) · `RL-1` · `CR-5` |
| `API-GEN-3` | ⛔ **Không con số ngưỡng rate limit** ở bất kỳ đâu trong file này (`T-10`) | `SRS-NFR-20` |
| `API-GEN-4` | Rate limit **fail-safe**: mất state ⇒ **chặn tạm** (`429`), ⛔ không mặc định cho qua | `E9` điều 5 |
| `API-GEN-5` | ⭐ **`public.usage_event` đồng nhất: 1 dòng = 1 image candidate**; `N = 3` ⇒ **đúng 3** dòng. ⛔ Không endpoint nào ở đây ghi nó | `U-1`…`U-3` · [`E20`](../../010-Planning/pm-runs/2026-08-28-phase-2-architecture-design-comic-studio/escalations.md) |
| `API-GEN-6` | ⭐ **Chi phí VLM ở `generation.vlm_scoring_call`**, ⛔ không ở `usage_event`, ⛔ không ở `vlm_evaluation` | [`DB-Entity-Provenance-And-Usage.md`](../Schema/DB-Entity-Provenance-And-Usage.md) |
| `API-GEN-7` | `#4` là **hành động authorship**: `approved_generation_id` + `change_log('select_generation')` + `field_provenance` trong **một** transaction. ⛔ Không ghi `usage_event`, ⛔ không settle hold | [ADR-017 `Q4.1`, `Q4.2`](../Architecture/ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md) |
| `API-GEN-8` | ⛔ **Không endpoint `DELETE` generation.** Candidate không được chọn ⛔ **không bị xoá khỏi lineage** | `UC-06` · `GR-4` (`ON DELETE RESTRICT`) |
| `API-GEN-9` | ⭐ **VLM chỉ preselect.** ⛔ Không auto-approve, ⛔ không `[Fix automatically]`, ⛔ không tham số áp dụng preselect. **Người chọn** | `D-38` |
| `API-GEN-10` | ⭐ **`unclear` là giá trị hợp lệ hạng nhất** — trả nguyên trạng | `D-38` · `INV` của [`DB-Entity-Generation.md`](../Schema/DB-Entity-Generation.md) |
| `API-GEN-11` | ⭐ **`checker_coverage` phải hiện tường minh**; ⛔ không giấu để trông đẹp hơn | `SRS-FR-22` · `D-39` |
| `API-GEN-12` | ⭐ **`degradations[]` (drop log) phải trả về**; identity refs ⛔ **không bao giờ** bị drop | `SRS-FR-17` · [ADR-014](../Architecture/ADR-014-Deterministic-Prompt-Compiler-And-Best-Of-N.md) |
| `API-GEN-13` | ⚠️ **Sinh ảnh ⛔ KHÔNG bị chặn bởi hai human gate** — `SDD-HG-01.4` chặn **xuất bản**, ⛔ không chặn sinh ảnh. ⛔ **Nhưng** ⛔ vẫn không endpoint nào ở đây nhận tham số bỏ qua gate | `SDD-HG-01.4` + hệ quả #1 |
| `API-GEN-14` | ⛔ **Không blob qua API**; ảnh chỉ đi qua signed URL | `B-4` · [ADR-004](../Architecture/ADR-004-Object-Storage-Vendor-And-Signed-URL.md) |
| `API-GEN-15` | `CT-POLL-2S`: `#6` rẻ, ⛔ không aggregate nặng, ⛔ không join xuyên schema; ⛔ không kênh push | [ADR-015 `Q6`](../Architecture/ADR-015-Job-Queue-In-Postgres.md) |
| `API-GEN-16` | ⛔ **Không endpoint nào gọi copyright/similarity detection.** VLM là **Continuity Checker**, ⛔ không phải checker bản quyền | `SRS-NFR-15` |
| `API-GEN-17` | ⛔ **`#1` không gọi provider**; ⛔ không đường tắt nào tạo `generation` ngoài unit-of-work chung (⛔ không script vận hành, ⛔ không seed, ⛔ không admin tool) | [ADR-017 `## Consequences`](../Architecture/ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md) điều 1 |
| `API-GEN-18` | ⛔ **`attempt_count` (job) ≠ `attempt_no` (generation)** — ⛔ không endpoint nào trộn hai giá trị này vào một field response | [ADR-015 `Q2`](../Architecture/ADR-015-Job-Queue-In-Postgres.md) · [`DB-Entity-Job-Queue.md`](../Schema/DB-Entity-Job-Queue.md) |
| `API-GEN-19` | ⭐ **Cả BẢY endpoint kiểm cờ disable-access** ⇒ `disabled_by_takedown` (hoặc ⛔ thiếu row trạng thái) ⇒ `403 PROJECT_ACCESS_DISABLED` — ⛔ **không** riêng `#5`. Hai đường job (`#6`, `#7`) ⛔ không được miễn vì path ⛔ không mang `project_id`. ⛔ `deleted_at` ⛔ không bao giờ đọc thành trạng thái takedown | [`API-PRJ-4`](./Endpoint-Project.md#invariant-của-resource) · [Threat Model §4.4](../Security/Spec-Security-Threat-Model.md#44--c-3-danh-sách-đóng-các-đường-đọc-phải-kiểm-cờ-disable-access) Nhóm B (`C3-K1`…`C3-K4`, `C3-K7`) |
| `API-GEN-20` | ⚠️ **Signed URL phát TRƯỚC takedown ⛔ không thu hồi được** ⇒ cận trên của cửa sổ đọc là `T-7`; ⛔ không tuyên bố *"đã hạ hoàn toàn"* khi `T-7` còn mở | `C3-K6` · [`API-PE-7`](./Endpoint-Preview-Export.md#invariant-của-resource) · [ADR-004](../Architecture/ADR-004-Object-Storage-Vendor-And-Signed-URL.md) |

---

## 6. UC nào tiêu thụ

| UC | Bước | Endpoint |
|---|---|---|
| `UC-06` | b1 — ra lệnh `Generate` / `Regenerate` | `#1` |
| `UC-06` | b2 — compile spec → prompt (deterministic) | `#1` ([§4.2](#42-1--nội-dung-transaction-enqueue) bước 2) |
| `UC-06` | b3 — 🔒 HOLD 3 credit trước enqueue | ⚠️ **⛔ không hiện thực ở horizon này** — thay bằng rate limit ([§3](#3--chống-lạm-dụng-chi-phí-ở-mvp1mvp2--rate-limit--không-phải-hold-credit)); hàng `T-25` của [SDD §9.1](../Architecture/SDD-Comic-Studio.md) |
| `UC-06` | b4 — 🔒 enqueue job trong cùng transaction | `#1` ([§4.2](#42-1--nội-dung-transaction-enqueue) bước 3–5) |
| `UC-06` | b5 — gọi provider qua adapter, `N = 3` candidate | ⛔ **đường worker**, ⛔ không phải bề mặt API — [`Spec-Integration-Image-Provider.md`](./Spec-Integration-Image-Provider.md) |
| `UC-06` | b6 — VLM chấm + đề xuất | ⛔ đường worker — [`Spec-Integration-VLM-QA-Select.md`](./Spec-Integration-VLM-QA-Select.md) |
| `UC-06` | b7 — đọc 3 candidate + đề xuất | `#2`, `#3`, `#5` |
| `UC-06` | b8 — chọn / override candidate | `#4` |
| `UC-06` | b9 — ghi `approved_generation_id` + lineage + `change_log` | `#4` ([§4.4](#44-4---hành-động-authorship-nội-dung-transaction)) |
| `UC-06` | b10 — settle hold + ghi `usage_event` | ⚠️ **⛔ không ở `#4`**: `usage_event` ghi lúc **candidate hoàn tất** (`U-1`); settle hold ⛔ không tồn tại ở horizon này |
| `UC-06` | b11 — poll trạng thái job (2s) | `#6` (+ `#7` cho lịch sử) |
| `UC-07` | b1–b2 — mở panel đã có ảnh, trả ảnh nền | `#5` (ảnh); typeset layer thuộc [`Endpoint-Bubble-Typeset.md`](./Endpoint-Bubble-Typeset.md) |

---

## 7. `TBD` còn lại — ⛔ không được bịa

| Mã | Khoảng trống | Ai đóng | Khi nào |
|---|---|---|---|
| ⭐ `T-10` | **Ngưỡng rate limit `generate`** (số request / độ dài cửa sổ) và ngưỡng `upload` | **PM / Founder**, sau số đo MVP0 (`SRS-NFR-20`) | Trước khi bật cưỡng chế thật |
| `T-GEN-CL-ENQUEUE` | ⭐ Chênh lệch giữa sơ đồ [SDD §5.2 `F5`](../Architecture/SDD-Comic-Studio.md) (*"INSERT change_log lúc enqueue"*) và danh mục `action_type` **đóng** ⛔ không có giá trị nào cho *"ra lệnh generate"*. Hoặc sơ đồ được đính chính, hoặc danh mục được mở kèm mỏ neo | **Architect (sở hữu SDD) + PM** | Trước khi `UC-06` bước 1 vào Active Sprint |
| `T-GEN-N` | **Giá trị `N` cuối cùng** — `N = 3` là **MẶC ĐỊNH**, ngân sách giữ ở 3. ⛔ Client ⛔ không hard-code | **PM tại gate `G1`**, sau verdict MVP0 | Sau MVP0 |
| `T-GEN-INFLIGHT` | **`N` của `in_flight_per_tenant < N`** trong câu CLAIM — ⛔ không con số nào trong repo. ⚠️ Ảnh hưởng gián tiếp `#6`: job có thể ở `queued` lâu vì fairness, ⛔ không phải vì lỗi | **PM + Architect**, sau tải thật MVP0 | Cùng mốc `T-10` |
| `T-GEN-LEASE` | **Thời hạn lease** (`public.job.lease_expires_at`) — quyết định sau bao lâu một job kẹt quay lại `queued`; ảnh hưởng ngữ nghĩa `attempt_count` mà `#6` trả | **Architect + Engineer** | Sau MVP0 |
| `T-GEN-URL-TTL` | **TTL của signed URL** — thuộc [ADR-004](../Architecture/ADR-004-Object-Storage-Vendor-And-Signed-URL.md), ⛔ file này không đặt số | **Architect tại ADR-004** | Trước khi hiện thực `#5` |
| `T-API-ERR` | ⭐ Chuẩn `error_code` + error envelope (⛔ **chưa chốt**). ✅ **Tiền tố đường dẫn đã chốt `/v1/…`** (lô `L28a`) — chi tiết ở [`Endpoint-Panel-Script.md`](./Endpoint-Panel-Script.md) | **Architect** (một lô quét toàn thư mục) | Trước file API đầu tiên được implement |

---

## 8. Tài liệu tham khảo

- [SDD Comic Studio](../Architecture/SDD-Comic-Studio.md) — §5.2 `F5`, §6.2, §6.4, §9.1 `T-25`
- [ADR-014 — Visual Prompt Compiler deterministic + best-of-N](../Architecture/ADR-014-Deterministic-Prompt-Compiler-And-Best-Of-N.md)
- [ADR-015 — Job queue trong PostgreSQL](../Architecture/ADR-015-Job-Queue-In-Postgres.md)
- [ADR-016 — Image provider adapter + pin model version](../Architecture/ADR-016-Image-Provider-Adapter-And-Version-Pinning.md)
- [ADR-017 — Chuỗi provenance và MỘT transaction boundary](../Architecture/ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md)
- [ADR-018 — Mô hình `usage_event` và rollup](../Architecture/ADR-018-Usage-Event-And-Rollup-Model.md)
- [ADR-007 — VLM provider cho QA-select](../Architecture/ADR-007-VLM-Provider-For-QA-Select.md) · [ADR-004 — Object storage & signed URL](../Architecture/ADR-004-Object-Storage-Vendor-And-Signed-URL.md)
- [`DB-Entity-Generation.md`](../Schema/DB-Entity-Generation.md) · [`DB-Entity-Job-Queue.md`](../Schema/DB-Entity-Job-Queue.md) · [`DB-Entity-Provenance-And-Usage.md`](../Schema/DB-Entity-Provenance-And-Usage.md) · [`DB-Entity-Tenancy.md`](../Schema/DB-Entity-Tenancy.md) · [`DB-Entity-Credit-Ledger.md`](../Schema/DB-Entity-Credit-Ledger.md)
- [UC-06 — Generate Panel And Pick Variant](../../020-Requirements/Use-Cases/UC-06-Generate-Panel-And-Pick-Variant.md)
