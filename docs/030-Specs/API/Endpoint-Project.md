---
id: SPEC-API-PROJECT
type: spec
status: draft
project: comic-studio
created: 2026-08-29
---

# Endpoint: Project

Resource `project` là **aggregate gốc "tác phẩm"** của một tenant. Nó tồn tại trong lô API vì hai lý do độc lập nhau: (a) nó là **đơn vị phạm vi** của mọi resource còn lại (`chapter`, `timeline`, `event`, `bible_entity`, `page`, `panel`); (b) nó là **đơn vị của disable-access khi takedown** (`UC-11` bước 6).

Bảng nguồn: [`story.project`](../Schema/DB-Entity-Narrative-Timeline.md) và [`public.project_access_state`](../Schema/DB-Entity-Compliance-And-Takedown.md). ⚠️ **Hai bảng, hai khái niệm, ⛔ không gộp** — xem [`API-PRJ-2`](#invariant-của-resource).

**Decided in:**

- [SDD Comic Studio](../Architecture/SDD-Comic-Studio.md) — §4.1 ranh giới, §5.4 `F1`/`F7`, [§6.3 `SDD-HG-01`](../Architecture/SDD-Comic-Studio.md#63-sdd-hg-01--không-đường-nào-bypass-hai-human-gate--nguồn-duy-nhất)
- [ADR-006 — RLS & tenant context injection](../Architecture/ADR-006-RLS-Tenant-Context-Injection.md) — `D3` (trình tự đường API), `D5`
- [ADR-017 — Provenance chain & one transaction boundary](../Architecture/ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md) — `Q2`, `Q4.1`, `Q4.3`
- [ADR-015 — Job queue trong Postgres](../Architecture/ADR-015-Job-Queue-In-Postgres.md) — `Q6` (`CT-POLL-2S`)
- [ADR-010 — Cô lập tenant bằng `tenant_id` + RLS](../Architecture/ADR-010-Tenant-Isolation-With-RLS.md) — `D1`, `D7`

---

## ⛔ Bốn ràng buộc xuyên-endpoint — TRỎ theo mã, ⛔ KHÔNG lặp lại nội dung

> [!IMPORTANT]
> ⭐ **Bốn hàng dưới đây có nguồn duy nhất ở nơi khác.** File API ⛔ **không đặc tả lại**, ⛔ không diễn giải lại, ⛔ không tạo biến thể. Bảng này là **chỉ mục**, không phải nội dung.
> ⭐ **Ba file API còn lại của lô này trỏ về bảng này** thay vì lặp lại: [`Endpoint-Chapter-Ingest.md`](./Endpoint-Chapter-Ingest.md) · [`Endpoint-Story-Bible.md`](./Endpoint-Story-Bible.md) · [`Endpoint-Timeline-Event.md`](./Endpoint-Timeline-Event.md).

| Mã | Ràng buộc | Nguồn duy nhất |
|---|---|---|
| **`SDD-HG-01`** | ⛔ Không đường nào bypass hai human gate. ⛔ Không endpoint nào nhận tham số bỏ qua gate — không query param, không header, không field body, không scope | [SDD §6.3](../Architecture/SDD-Comic-Studio.md#63-sdd-hg-01--không-đường-nào-bypass-hai-human-gate--nguồn-duy-nhất) — trích theo ID điều khoản `SDD-HG-01.1`…`.7` |
| **`ADR-015`** | Job queue nằm trong Postgres; **`CT-POLL-2S`** — client lấy trạng thái tác vụ async bằng **polling 2 giây**, ⛔ không WebSocket/SSE/long-poll | [ADR-015 `Q6`](../Architecture/ADR-015-Job-Queue-In-Postgres.md#q6--polling-2-giây--nguồn-duy-nhất-của-contract-này) |
| **`ADR-017`** | Chuỗi provenance + **ranh giới một transaction** (`KC-4`): artifact và bằng chứng của nó cùng commit hoặc không dòng nào tồn tại | [ADR-017 `Q4.1`](../Architecture/ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md#q41-phát-biểu-chuẩn-normative) · [`Q4.2`](../Architecture/ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md#q42-chính-xác-những-bảng-nào) · [`Q4.3`](../Architecture/ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md#q43-commit-cùng-transaction-nghĩa-là-gì--năm-thuộc-tính-kiểm-chứng-được) `P-1`…`P-5` · [`Q2`](../Architecture/ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md#q2-change_log-kc-2--phạm-vi-ghi-và-điểm-cưỡng-chế) |
| **`ADR-006`** | Tenant context injection + RLS: GUC `app.current_tenant` đặt bằng `SET LOCAL`, mọi handler chạy **bên trong** một transaction tường minh | [ADR-006 `D3`](../Architecture/ADR-006-RLS-Tenant-Context-Injection.md) (đường API), `D2`, `D5` |

⚠️ **Hệ quả duy nhất mà file API phải tự nhớ**: `SET LOCAL` có phạm vi transaction ⇒ **mọi endpoint chạy trong một transaction tường minh**; query ở chế độ autocommit trả **0 row**, và `0 row` là **fail-closed**, ⛔ không phải *"không có dữ liệu"*.

---

## Quy ước chung — ⭐ `API-ENV-1`, nguồn duy nhất cho cả bốn file của lô

> ⚠️ [`Specs-MOC.md`](../Specs-MOC.md) đang rỗng và ⛔ **không nguồn nào trong repo** chốt envelope lỗi HTTP. ⇒ Lô này đặt khuôn dưới đây và ghi nó là `TBD-API-ENV` cần được nâng lên thành nguồn chung khi 14 file API hoàn tất — xem [`TBD` còn lại](#tbd-còn-lại---không-được-bịa).

| Điểm | Quy ước |
|---|---|
| Base path | `/v1` |
| Auth | `Authorization: Bearer <token>` do auth vendor cấp ([ADR-003](../Architecture/ADR-003-Auth-And-Billing-Vendor-Selection.md), vendor `TBD`). Middleware chạy đúng trình tự [ADR-006 `D3`](../Architecture/ADR-006-RLS-Tenant-Context-Injection.md) 1→6 |
| Tenant | ⛔ **Không endpoint nào nhận `tenant_id` từ client** — không body, không query, không header. `tenant_id` chỉ đến từ bước 2 của `ADR-006 D3` |
| Envelope lỗi | `{"error": {"code": "<MÃ>", "message": "<mô tả>", "details": {…}}}` — `code` là **danh mục đóng**, ⛔ không sinh mã ad-hoc trong code |
| Trường lạ trong body | ⛔ **Từ chối** — `400 UNKNOWN_FIELD`. ⭐ Đây là cưỡng chế trực tiếp của quy tắc *"⛔ không tham số bỏ qua gate"* (`SDD-HG-01` hệ quả #1): một body **lỏng** là chỗ một cờ `force`/`skip_gates` chui vào mà ⛔ không ai thấy |
| Phân trang | Cursor-based: `?limit=` (mặc định 50, trần 200) + `?cursor=`; response `{"items": [...], "next_cursor": "…"}` |
| Idempotency | Endpoint `POST` **có tác dụng phụ pháp lý** (upload chapter, approve) nhận header `Idempotency-Key`. ⚠️ Cơ chế lưu key = `TBD` |

### Mã lỗi dùng chung — `API-ENV-1`

| HTTP | `code` | Khi nào |
|:--:|---|---|
| `400` | `VALIDATION_FAILED` | Body/query sai kiểu, thiếu field bắt buộc |
| `400` | `UNKNOWN_FIELD` | Body chứa field ⛔ không thuộc contract |
| `401` | `UNAUTHENTICATED` | Thiếu/hỏng token |
| `403` | `FORBIDDEN` | Đã xác thực nhưng ⛔ không có quyền trên tenant |
| `403` | `PROJECT_ACCESS_DISABLED` | ⭐ Project đang `disabled_by_takedown` — xem [`API-PRJ-4`](#invariant-của-resource) |
| `404` | `NOT_FOUND` | ⭐ Bao gồm cả **tài nguyên thuộc tenant khác**: RLS trả 0 row ⇒ 404. ⛔ **Không** trả 403 ở trường hợp này — 403 xác nhận tài nguyên **có tồn tại** ⇒ biến API thành **existence oracle** chéo tenant |
| `409` | `CONFLICT` | Xung đột trạng thái; mã cụ thể hơn được khai ở từng file |
| `422` | `UNPROCESSABLE` | Cú pháp đúng nhưng vi phạm một ràng buộc nghiệp vụ |
| `429` | `RATE_LIMITED` | ⭐ **Mã DUY NHẤT cho mọi lần vượt rate limit ở toàn tầng API — phủ CẢ `upload` VÀ `generate`.** Xem `RL-1`…`RL-4` của [`DB-Entity-Tenancy.md`](../Schema/DB-Entity-Tenancy.md): khoá đếm là `(tenant_id, action)` với `action ∈ {upload, generate}` ⇒ **một điều kiện, một mã**. ⛔ **Không** tồn tại mã riêng cho `generate` — tên cũ `GENERATE_RATE_LIMIT_EXCEEDED` đã **rút** ở lô `L34` ([`Endpoint-Generation.md`](./Endpoint-Generation.md) §3) |
| `500` | `INTERNAL` | ⛔ Không rò rỉ chi tiết SQL/provider |

---

## Danh sách endpoint

### `PRJ-1` · `GET /v1/projects` — liệt kê tác phẩm

| Mục | Nội dung |
|---|---|
| **Method · Path** | `GET /v1/projects` |
| **Auth** | Bearer bắt buộc. Tenant context theo [ADR-006 `D3`](../Architecture/ADR-006-RLS-Tenant-Context-Injection.md) |
| **Request** | Query: `include_deleted` (`boolean`, mặc định `false`) · `limit` · `cursor` |
| **Response `200`** | `{"items": [{"id", "title", "created_at", "updated_at", "deleted_at", "access_state"}], "next_cursor"}` |
| **Mã lỗi** | `400 VALIDATION_FAILED` · `401 UNAUTHENTICATED` |

⭐ `access_state` **luôn có mặt** trong mọi response của resource này. Bỏ nó đi buộc client tự suy ra trạng thái takedown từ `deleted_at` — đúng điều `CO-2` của [`DB-Entity-Compliance-And-Takedown.md`](../Schema/DB-Entity-Compliance-And-Takedown.md) cấm.
⛔ **Không có filter `access_state`** ở lô này: lọc bỏ project bị takedown khỏi danh sách làm tác giả mất đường duy nhất để nhìn thấy nó.

### `PRJ-2` · `POST /v1/projects` — tạo tác phẩm

| Mục | Nội dung |
|---|---|
| **Method · Path** | `POST /v1/projects` |
| **Auth** | Bearer bắt buộc |
| **Request** | `{"title": "<TEXT, 1..200>"}` |
| **Response `201`** | `{"id", "title", "access_state": "active", "created_at"}` |
| **Mã lỗi** | `400 VALIDATION_FAILED` · `400 UNKNOWN_FIELD` · `401 UNAUTHENTICATED` · `429 RATE_LIMITED` |

> [!IMPORTANT]
> ⭐ **Một transaction, ba việc**: `INSERT story.project` + `INSERT public.project_access_state` (`'active'`) + `INSERT public.change_log` — commit **cùng nhau** theo [`ADR-017 Q4.1`](../Architecture/ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md#q41-phát-biểu-chuẩn-normative) và `Q4.3` `P-1`.
> ⚠️ Đây là **cưỡng chế của `INV-PAS-5`/`CO-3`** ([`DB-Entity-Compliance-And-Takedown.md`](../Schema/DB-Entity-Compliance-And-Takedown.md)): ⛔ không project nào được tồn tại mà thiếu dòng trạng thái. Lý do là **fail-closed** — đường đọc ⛔ **không bao giờ** được diễn giải *"thiếu dòng"* thành `'active'`, vì như thế một dòng bị mất sẽ **mở lại** một project đang bị takedown mà ⛔ không báo lỗi nào.

⛔ **Body ⛔ không nhận `access_state`, `tenant_id`, `deleted_at`, `id`.** Trường lạ ⇒ `400 UNKNOWN_FIELD`.

### `PRJ-3` · `GET /v1/projects/{project_id}` — đọc một tác phẩm

| Mục | Nội dung |
|---|---|
| **Method · Path** | `GET /v1/projects/{project_id}` |
| **Auth** | Bearer bắt buộc |
| **Request** | Path: `project_id` (`UUID`) |
| **Response `200`** | `{"id", "title", "created_at", "updated_at", "deleted_at", "access_state", "disabled_at", "chapter_count", "timeline_count"}` |
| **Mã lỗi** | `400 VALIDATION_FAILED` · `401 UNAUTHENTICATED` · `404 NOT_FOUND` |

⭐ **Endpoint này ⛔ KHÔNG trả `403 PROJECT_ACCESS_DISABLED`** — nó **luôn** trả 200 kèm `access_state`. Xem [`API-PRJ-4`](#invariant-của-resource): nếu cả metadata cũng bị chặn thì tác giả ⛔ không còn đường nào biết vì sao nội dung của mình biến mất.
⛔ **Không trả `disabled_by_request_id`** cho tenant — nội dung yêu cầu takedown thuộc bề mặt operator, ⛔ không thuộc bề mặt tenant.

### `PRJ-4` · `PATCH /v1/projects/{project_id}` — sửa / xoá mềm

| Mục | Nội dung |
|---|---|
| **Method · Path** | `PATCH /v1/projects/{project_id}` |
| **Auth** | Bearer bắt buộc |
| **Request** | `{"title"?: "<TEXT>", "deleted"?: <boolean>}` — ít nhất một field |
| **Response `200`** | Như `PRJ-3` |
| **Mã lỗi** | `400 VALIDATION_FAILED` · `400 UNKNOWN_FIELD` · `401 UNAUTHENTICATED` · `403 PROJECT_ACCESS_DISABLED` · `404 NOT_FOUND` · `422 UNPROCESSABLE` |

- `deleted: true` ⇒ ghi `story.project.deleted_at = now()`; `deleted: false` ⇒ về `NULL`. ⛔ **Không `DELETE` vật lý** — đường hard-delete duy nhất là hard-delete **tenant** ([ADR-010 `D7`](../Architecture/ADR-010-Tenant-Isolation-With-RLS.md)), do tenant khởi xướng, ⛔ không phải đường này.
- ⛔ **Body ⛔ không nhận `access_state`.** ⭐ **⛔ Không tồn tại endpoint nào trên bề mặt tenant ghi được `public.project_access_state`** — đó là hệ quả một chiều của đường takedown (`UC-11`), và một `PATCH` mở cột đó ra chính là **đường undo takedown do chính người bị takedown bấm**.
- Ghi `public.change_log` **cùng transaction** ([`ADR-017 Q2`](../Architecture/ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md#q2-change_log-kc-2--phạm-vi-ghi-và-điểm-cưỡng-chế)).

---

## Invariant của resource

| Mã | Invariant | Cưỡng chế bằng |
|:--:|---|---|
| **`API-PRJ-1`** | ⭐ `story.project` + `public.project_access_state` (`'active'`) sinh ra trong **một** transaction; ⛔ không project nào thiếu dòng trạng thái | `PRJ-2` + `INV-PAS-5`/`CO-3` của [`DB-Entity-Compliance-And-Takedown.md`](../Schema/DB-Entity-Compliance-And-Takedown.md); test CI: `COUNT(story.project) = COUNT(public.project_access_state)` |
| **`API-PRJ-2`** | ⭐ `deleted_at` và `access_state` được đọc **độc lập**; ⛔ không đường code nào suy ra trạng thái takedown từ `deleted_at` | `CO-2`. Response luôn mang **cả hai** field ⇒ client ⛔ không có lý do gì để suy diễn |
| **`API-PRJ-3`** | ⛔ **Bề mặt tenant ⛔ không ghi được `access_state`** ở bất kỳ endpoint nào của toàn hệ thống | Vắng mặt field trong mọi request schema + `400 UNKNOWN_FIELD` |
| **`API-PRJ-4`** | ⭐ **Mọi endpoint đọc/ghi NỘI DUNG trong phạm vi project** (`chapter`, `event`, `timeline`, `bible_entity`, `page`, `panel`, `generation`, preview, export) kiểm `access_state`; `disabled_by_takedown` ⇒ `403 PROJECT_ACCESS_DISABLED`. ⚠️ **Ngoại lệ đúng một**: `PRJ-3` **vẫn trả 200** | `INV-PAS-4` + [`SDD-HG-01.4`](../Architecture/SDD-Comic-Studio.md#63-sdd-hg-01--không-đường-nào-bypass-hai-human-gate--nguồn-duy-nhất) (vế *"project không ở trạng thái disable-access"*), qua **đúng một** hàm dùng chung ở tầng service |
| **`API-PRJ-5`** | Tài nguyên của tenant khác trả **`404`**, ⛔ không phải `403` | `API-ENV-1`; RLS trả 0 row ⇒ handler ⛔ không phân biệt được *"không tồn tại"* với *"của tenant khác"* — và đó là **tính chất mong muốn** |
| **`API-PRJ-6`** | ⛔ **Không endpoint nào của resource này gọi copyright / plagiarism / similarity detection**, ⛔ không chấm điểm nghi vấn, ⛔ không quét, ⛔ không flag | ⭐ `SRS-NFR-15` — **anti-feature CÓ CHỦ Ý**. Xem [khối anti-feature](#-anti-feature-srs-nfr-15--đọc-trước-khi-đề-xuất-tính-năng-mới) |

---

## ⛔ Anti-feature `SRS-NFR-15` — đọc TRƯỚC khi đề xuất tính năng mới

> [!WARNING]
> ⛔ **⛔ KHÔNG endpoint nào trong toàn bộ lô API gọi copyright detection, plagiarism check, similarity scoring, hay bất kỳ dạng "chấm điểm nghi vấn vi phạm" nào.**
> ⚠️ Đây ⛔ **không phải** một tính năng bị hoãn vì thiếu nguồn lực. Nó là **anti-feature có chủ ý**: chủ động quét và chấm điểm tạo ra **tri thức thực tế về vi phạm** ở phía nền tảng — và chính tri thức đó **tự phá miễn trừ trách nhiệm theo Điều 198b**.
> ⇒ Một PR thêm cột `similarity_score`, một job `scan_for_infringement`, hay một field `suspicion_level` vào bất kỳ response nào là **vi phạm `SRS-NFR-15`**, ⛔ không phải một cải tiến. `INV-IC-5` của [`DB-Entity-Compliance-And-Takedown.md`](../Schema/DB-Entity-Compliance-And-Takedown.md) đã cấm điều tương đương ở tầng schema; ⭐ hàng này cấm ở **tầng API**.
> ⚠️ Phân biệt: **opt-out check Điều 37b** ([`Endpoint-Chapter-Ingest.md`](./Endpoint-Chapter-Ingest.md)) ⛔ **không** thuộc nhóm bị cấm — nó **đọc nhãn quyền do chủ sở hữu tự khai**, ⛔ không suy đoán gì về nội dung.

---

## UC nào tiêu thụ

| UC | Bước | Endpoint | Ghi chú ràng buộc |
|---|---|---|---|
| [UC-01 Upload & Ingest Chapter](../../020-Requirements/Use-Cases/UC-01-Upload-And-Ingest-Chapter.md) | bước 1 — *"Chọn tác phẩm (hoặc tạo tác phẩm mới)"* | `PRJ-1`, `PRJ-2`, `PRJ-3` | `PRJ-2` phải hoàn tất **trước** mọi endpoint của [`Endpoint-Chapter-Ingest.md`](./Endpoint-Chapter-Ingest.md) |
| [UC-11 Handle Takedown Request](../../020-Requirements/Use-Cases/UC-11-Handle-Takedown-Request.md) | bước 6 — *"soft-delete + disable-access cấp project"* | ⭐ **Chỉ đọc**: `PRJ-1`, `PRJ-3` | ⛔ Hành động disable-access **⛔ KHÔNG** nằm ở file này — nó thuộc bề mặt operator của `Endpoint-Takedown-Public.md` (lô khác). File này chỉ **phản ánh** trạng thái |
| Mọi UC còn lại (`UC-02`…`UC-09`) | — | Gián tiếp | `project_id` là phạm vi của mọi resource; `API-PRJ-4` là điều kiện chặn dùng chung của tất cả |

⚠️ **Ranh giới của file này** — ba thứ ⛔ **KHÔNG** thuộc đây: (a) tạo/sửa `timeline` ⇒ [`Endpoint-Timeline-Event.md`](./Endpoint-Timeline-Event.md); (b) mọi thao tác trên `public.takedown_request` ⇒ `Endpoint-Takedown-Public.md`; (c) `GET /me`, tenant, membership ⇒ `Endpoint-Tenancy.md`.

---

## `TBD` còn lại — ⛔ không được bịa

| Khoảng trống | Ai đóng | Khi nào |
|---|---|---|
| ⭐ **`TBD-API-ENV`** — ⛔ **VẪN MỞ.** Envelope lỗi + danh mục `code` của toàn bộ 14 file API chưa có nguồn chung; lô này đặt khuôn `API-ENV-1` **ở phạm vi 4 file**. ⚠️ ⭐ **Đây là SỔ ĐĂNG KÝ CHÍNH của câu hỏi này**: mệnh đề **(a)** của `T-API-ERR` ([`Endpoint-Panel-Script.md`](./Endpoint-Panel-Script.md)) hỏi **đúng cùng một thứ** và ⛔ **không** còn theo dõi song song — ⛔ đừng mở lại sổ thứ hai. `T-API-ERR` giữ mệnh đề **(c)** (quy ước `:verb` vs sub-resource), là câu hỏi **khác** | **Architect**, khi 14 file `Endpoint-*` hoàn tất ⇒ nâng lên `Specs-MOC` hoặc một file `Spec-API-Conventions` | Trước khi Engineer sinh OpenAPI |
| Cơ chế lưu `Idempotency-Key` (bảng? TTL? phạm vi tenant?) — ⛔ **không nguồn nào trong repo** nói tới | **Architect + Engineer** | Trước khi `Endpoint-Generation.md` vào implementation |
| **Nội dung thông báo** cho tenant khi project bị `disabled_by_takedown` (`403` nói gì, có nêu lý do không) — ⛔ repo im lặng, và đây là câu hỏi **pháp lý** trước khi là câu hỏi UX | **PM + luật sư SHTT** | Trước khi `UC-11` có trigger thật |
| Trần `limit` = 200 và mặc định 50 là **`[EM]`** — ⛔ không có số đo nào trong repo | **Engineer**, sau khi có tenant thật đầu tiên | Trước khi mở đăng ký ngoài Founder |

---

## Tài liệu tham khảo

- [SDD Comic Studio](../Architecture/SDD-Comic-Studio.md) — §4.1, §5.4, §6.1, §6.3
- [ADR-006 — RLS Tenant Context Injection](../Architecture/ADR-006-RLS-Tenant-Context-Injection.md) · [ADR-010 — Tenant Isolation With RLS](../Architecture/ADR-010-Tenant-Isolation-With-RLS.md)
- [ADR-015 — Job Queue In Postgres](../Architecture/ADR-015-Job-Queue-In-Postgres.md) · [ADR-017 — Provenance Chain And One Transaction Boundary](../Architecture/ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md)
- [ADR-003 — Auth And Billing Vendor Selection](../Architecture/ADR-003-Auth-And-Billing-Vendor-Selection.md)
- [DB-Entity-Narrative-Timeline.md](../Schema/DB-Entity-Narrative-Timeline.md) · [DB-Entity-Compliance-And-Takedown.md](../Schema/DB-Entity-Compliance-And-Takedown.md) · [DB-Entity-Tenancy.md](../Schema/DB-Entity-Tenancy.md)
- [UC-01 — Upload And Ingest Chapter](../../020-Requirements/Use-Cases/UC-01-Upload-And-Ingest-Chapter.md) · [UC-11 — Handle Takedown Request](../../020-Requirements/Use-Cases/UC-11-Handle-Takedown-Request.md)
- [SRS Comic Studio](../../020-Requirements/SRS-Comic-Studio.md) — `SRS-FR-35`, `SRS-FR-38`, `SRS-NFR-01`, `SRS-NFR-05`, `SRS-NFR-13`, `SRS-NFR-15`
