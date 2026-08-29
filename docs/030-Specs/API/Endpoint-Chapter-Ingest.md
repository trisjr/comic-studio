---
id: SPEC-API-CHAPTER-INGEST
type: spec
status: draft
project: comic-studio
created: 2026-08-29
---

# Endpoint: Chapter & Ingest

Resource `chapter` là **cửa duy nhất** để nội dung của bên thứ ba đi vào hệ thống. Vì thế nó ⛔ không phải một resource CRUD bình thường: **hai nghĩa vụ pháp lý** neo vào đúng một endpoint của file này — **checkbox cam kết quyền** (`SRS-FR-41`) và **kiểm opt-out Điều 37b kèm timestamp** (`SRS-FR-37`, `KC-6`).

Bảng nguồn: [`story.chapter`](../Schema/DB-Entity-Narrative-Timeline.md) · ⭐ [`story.ingest_check`](../Schema/DB-Entity-Compliance-And-Takedown.md) · ⭐ [`story.text_clean_report`](../Schema/DB-Entity-Compliance-And-Takedown.md).

> [!WARNING]
> ⚠️ **`ingest_check` và `text_clean_report` thuộc schema `story`** — tên đủ điều kiện là `story.ingest_check` và `story.text_clean_report`.
> ⛔ **KHÔNG phải `public.ingest_check`.** Chúng mang `tenant_id` và sống cùng dữ liệu nghiệp vụ của module `M1`; **trong cụm compliance**, chỉ `public.takedown_request` và `public.project_access_state` mới ở `public` (⚠️ các bảng platform khác — `public.change_log`, `public.usage_event`, `public.tenant` — cũng ở `public` theo [ADR-005](../Architecture/ADR-005-Platform-Table-Schema-Placement.md) `Q1`). Guardrail `G-3` của [ADR-005](../Architecture/ADR-005-Platform-Table-Schema-Placement.md) bắt **luôn** schema-qualify, ⛔ không dựa vào `search_path`.

**Decided in:** [SDD §5.1 `F1`](../Architecture/SDD-Comic-Studio.md) · [SDD §5.4](../Architecture/SDD-Comic-Studio.md) · [ADR-006 `D3`](../Architecture/ADR-006-RLS-Tenant-Context-Injection.md) · [ADR-017 `Q2`/`Q4`](../Architecture/ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md) · [ADR-011](../Architecture/ADR-011-Narrative-Time-Key-And-State-Reduction.md) `D1`–`D2` (hai trục thời gian) · [ADR-015 `Q6`](../Architecture/ADR-015-Job-Queue-In-Postgres.md)

⭐ **Bốn ràng buộc xuyên-endpoint** (`SDD-HG-01` · `ADR-015` · `ADR-017` · `ADR-006`) và **quy ước chung `API-ENV-1`**: xem [`Endpoint-Project.md`](./Endpoint-Project.md). ⛔ File này **không lặp lại**.

---

## Thứ tự cố định của `F1` — ⛔ không đảo, ⛔ không có tham số bỏ qua

| # | Chặng | Ràng buộc |
|--:|---|---|
| 1 | Nhận request + xác thực + tenant context | [ADR-006 `D3`](../Architecture/ADR-006-RLS-Tenant-Context-Injection.md) |
| 2 | ⭐ Kiểm **checkbox cam kết quyền** | ⛔ Thiếu ⇒ **từ chối**, ⛔ không nhận file. `SRS-FR-41` · `UC-01` `EXC-2` |
| 3 | Gắn `tenant_id` cho nội dung vừa nhận | `KC-5` · `SRS-NFR-01` |
| 4 | ⭐ **Kiểm opt-out Điều 37b** trên metadata / nhãn quyền | ⛔ **Phải đứng TRƯỚC chặng 5** — `UC-01` §3 ghi rõ: đặt sau `text clean` là **đã biến đổi nội dung trước khi biết mình có quyền** |
| 5 | ⭐ **Ghi `story.ingest_check` kèm `checked_at`** — **kể cả khi `result='no_signal'`** | `KC-6` · `INV-IC-2`. Xem [`API-CH-2`](#invariant-của-resource) |
| 6 | `text clean` deterministic (regex/heuristic, ⛔ **không LLM**) | `SRS-FR-06` · `M1-2` |
| 7 | Ghi `story.text_clean_report` | `UC-01` `EXC-4` — deterministic nên sai **nhất quán**; cách duy nhất phát hiện là cho người xem |
| 8 | Tách `story.event` mức scene theo `timeline_id` + `story_order` đã khai | `SRS-FR-04` · ⛔ không event mồ côi (`EXC-3`) |

⚠️ **Chặng 4 đọc nhãn quyền, ⛔ không xử lý nội dung** ⇒ nó đứng trước chặng 6 mà **không** vi phạm *"`text clean` là bước đầu tiên của chặng xử lý nội dung"*.

> [!IMPORTANT]
> ⭐ **Toàn bộ chặng 2–8 chạy ĐỒNG BỘ trong request của `CH-1`, ⛔ không đi qua `public.job`.**
> Căn cứ: danh mục `job_type` của [`DB-Entity-Job-Queue.md`](../Schema/DB-Entity-Job-Queue.md) là **danh sách đóng** và có **đúng một** giá trị — `generate_panel`. ⛔ Thêm một `job_type` cho ingest vì *"chắc là async"* là **bịa**, và là vi phạm ranh giới `B-2` ([SDD §4.1](../Architecture/SDD-Comic-Studio.md)).
> ⇒ ⛔ **`CH-1` ⛔ không trả `job_id`, ⛔ không có đường polling.** Nếu một nguồn tương lai chuyển ingest sang async thì **cùng migration đó** phải thêm giá trị vào `CHECK (job_type IN …)` — và khi đó contract trạng thái là **`CT-POLL-2S`** ([ADR-015 `Q6`](../Architecture/ADR-015-Job-Queue-In-Postgres.md#q6--polling-2-giây--nguồn-duy-nhất-của-contract-này)), ⛔ không phải một cơ chế mới. Xem [`TBD-API-CH-2`](#tbd-còn-lại---không-được-bịa).

---

## Danh sách endpoint

### `CH-1` · `POST /v1/projects/{project_id}/chapters` — nạp chapter ⭐ endpoint chịu tải pháp lý

| Mục | Nội dung |
|---|---|
| **Method · Path** | `POST /v1/projects/{project_id}/chapters` |
| **Auth** | Bearer bắt buộc. Kiểm `access_state` theo `API-PRJ-4` |
| **Content-Type** | `multipart/form-data` (khi `source_kind='file'`) hoặc `application/json` (khi `source_kind='pasted_text'`) |
| **Header** | `Idempotency-Key` **bắt buộc** — endpoint có tác dụng phụ pháp lý |
| **Response `201`** | Xem khối *Response* dưới bảng |
| **Mã lỗi** | `400 VALIDATION_FAILED` · `400 UNKNOWN_FIELD` · `401 UNAUTHENTICATED` · `403 PROJECT_ACCESS_DISABLED` · `404 NOT_FOUND` (project/timeline) · **`409 INGEST_BLOCKED_OPTOUT`** · **`409 CHAPTER_DUPLICATE_ORDER`** · **`422 RIGHTS_WARRANT_REQUIRED`** · `422 CHAPTER_EMPTY_AFTER_CLEAN` · `422 CHAPTER_UNREADABLE` · `429 RATE_LIMITED` |

**Request**

| Field | Kiểu | Bắt buộc | Ghi chú |
|---|---|:--:|---|
| `source_kind` | `'file' \| 'pasted_text'` | ✅ | ⭐ **Cả hai kênh đều đi qua chặng 4–5.** `UC-01` `ALT-2` + `M1-4` = **100%**, ⛔ không ngoại lệ theo kênh nạp |
| `file` / `source_text` | binary / `TEXT` | ✅ | Đúng **một** trong hai, khớp `source_kind` |
| `title` | `TEXT` | ✅ | |
| `timeline_id` | `UUID` | ✅ | ⭐ **Tác giả khai**, ⛔ hệ thống không tự suy ra (`UC-01` bước 2 · `ALT-4`) |
| `story_order` | `NUMERIC` | ✅ | ⭐ Trục **fabula**. ⛔ **Không `DEFAULT`, ⛔ không tự suy từ `(chapter, scene)`** — `INV-1` của [`DB-Entity-Narrative-Timeline.md`](../Schema/DB-Entity-Narrative-Timeline.md) |
| `reading_order` | `NUMERIC` | ✅ | Trục **syuzhet**. ⛔ Không được dùng để sắp xếp trong bất kỳ đường resolve state nào |
| ⭐ `rights_warrant_accepted` | `boolean` | ✅ | ⭐ **Phải bằng `true` trong CHÍNH request này** |
| `supersedes_chapter_id` | `UUID` | ⛔ | Lựa chọn **thay thế** ở nhánh trùng — xem `409 CHAPTER_DUPLICATE_ORDER` |

> [!IMPORTANT]
> ⭐ **`rights_warrant_accepted` là một field của request upload, ⛔ KHÔNG phải một cờ trên tenant/ToS.**
> ⛔ Server **⛔ không được** chấp nhận thay thế bằng *"tenant này đã tick ở trang ToS rồi"*, ⛔ không cache, ⛔ không kế thừa từ lần upload trước. `SRS-FR-41` + `UC-01` `EXC-2` neo cam kết vào **hành vi nạp từng file**; một cờ cấp tài khoản làm phòng tuyến hợp đồng khuyết đúng chỗ nó cần chịu lực.
> Giá trị `false` hoặc vắng mặt ⇒ **`422 RIGHTS_WARRANT_REQUIRED`**, ⛔ và ⛔ **không dòng `story.chapter` nào được tạo**.

> [!WARNING]
> ⛔ **Danh sách field ⛔ KHÔNG TỒN TẠI — và ⛔ không được thêm ở bất kỳ run nào**: `skip_optout_check`, `force`, `bypass_check`, `dry_run`, `trusted_source`, `internal_upload`, `admin_override`.
> `KC-6` nằm trong danh sách *"không được cắt"* và `UC-01` `EXC-1` ghi thẳng: ⛔ **không có đường cấu hình nào cho phép bỏ qua phép kiểm này**. ⇒ `400 UNKNOWN_FIELD` với mọi field lạ là **cưỡng chế**, ⛔ không phải sự khắt khe hình thức.

**Response `201`** — ⭐ **luôn** mang bản ghi kiểm, kể cả khi âm tính:

```json
{
  "chapter_id": "…",
  "upload_ref": "…",
  "status": "active",
  "timeline_id": "…",
  "story_order": 3000,
  "reading_order": 3000,
  "ingest_check": {
    "result": "no_signal",
    "checked_at": "2026-08-29T…Z",
    "blocked": false,
    "signal_channel": null,
    "source_kind": "file"
  },
  "text_clean_report_id": "…",
  "event_count": 12,
  "ingest_approved": false
}
```

**Mã lỗi có ngữ nghĩa riêng**

| Mã | Điều kiện | Hành vi bắt buộc |
|---|---|---|
| **`409 INGEST_BLOCKED_OPTOUT`** | `result ∈ {'signal_found','unreadable','conflicting'}` ⇒ `blocked = TRUE` (`INV-IC-3`, fail-safe) | ⛔ **Chặn** — chapter ⛔ **không** đi tiếp sang `text clean`. ⛔ **Không** dòng `story.chapter`. ⭐ Dòng `story.ingest_check` **vẫn được ghi** với `chapter_id = NULL` và `upload_ref` do server cấp. Body lỗi mang `details: {upload_ref, result, signal_channel, checked_at}` |
| **`409 CHAPTER_DUPLICATE_ORDER`** | Đã có chapter `status='active'` cùng `(tenant_id, timeline_id, story_order)` — UNIQUE partial index | ⛔ **Không âm thầm ghi đè** (`INV-9` · `EXC-5`). `details: {conflicting_chapter_id}`. Tác giả **phải chọn**: gửi lại kèm `supersedes_chapter_id` (thay thế) hoặc huỷ |
| **`422 CHAPTER_EMPTY_AFTER_CLEAN`** | Chặng 6 trả nội dung rỗng | Từ chối chapter, ⛔ **không tạo `story.event` mồ côi** (`EXC-3`) — `story_order` có lỗ làm mọi `reduce(events)` về sau đọc trên dữ liệu khuyết |
| **`422 CHAPTER_UNREADABLE`** | File sai định dạng / lỗi giải mã | Như trên. ⚠️ Lưu ý ⛔ **không nhầm** với `result='unreadable'` của `ingest_check` — cái đó là **nhãn quyền** không đọc được và **bắt buộc chặn** |

**Nhánh thay thế** (`supersedes_chapter_id` có giá trị): trong **một** transaction — `INSERT` chapter mới + `UPDATE` chapter cũ `status='superseded'`, `superseded_by_chapter_id` + `INSERT public.change_log` ([ADR-017 `Q2`](../Architecture/ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md#q2-change_log-kc-2--phạm-vi-ghi-và-điểm-cưỡng-chế)).
⚠️ ⛔ **Không `UPDATE clean_text` tại chỗ** ở bất kỳ đâu: `INV-7` — `clean_text` là **mỏ neo của mọi `*_span`**, sửa tại chỗ làm **mọi span sai âm thầm**.

### `CH-2` · `GET /v1/projects/{project_id}/chapters` — liệt kê chapter

| Mục | Nội dung |
|---|---|
| **Method · Path** | `GET /v1/projects/{project_id}/chapters` |
| **Auth** | Bearer. Kiểm `access_state` (`API-PRJ-4`) |
| **Request** | Query: `timeline_id` · `status` (`active`\|`superseded`, mặc định `active`) · `order_by` (`reading_order`\|`story_order`, ⭐ **bắt buộc khai tường minh**) · `limit` · `cursor` |
| **Response `200`** | `{"items": [{"id","title","timeline_id","story_order","reading_order","status","superseded_by_chapter_id","ingested_at","has_clean_text","ingest_approved"}], "next_cursor"}` |
| **Mã lỗi** | `400 VALIDATION_FAILED` · `401` · `403 PROJECT_ACCESS_DISABLED` · `404 NOT_FOUND` |

⛔ **Response ⛔ không chứa `source_text`/`clean_text`** — hai cột này có thể rất lớn và ⛔ không có ngưỡng nào trong repo.
⭐ `order_by` **không có giá trị mặc định ẩn**: `story_order` và `reading_order` là **hai trục khác nhau** (`D1`), và một mặc định ẩn là đúng mẫu *"sai âm thầm ở mọi flashback"* mà `ADR-011` tồn tại để chặn.

### `CH-3` · `GET /v1/chapters/{chapter_id}` — đọc một chapter

| Mục | Nội dung |
|---|---|
| **Method · Path** | `GET /v1/chapters/{chapter_id}` |
| **Auth** | Bearer. Kiểm `access_state` (`API-PRJ-4`) |
| **Request** | Query: `include` (`clean_text` \| `source_text`, lặp được; mặc định **không** trả text) |
| **Response `200`** | Các field của `CH-2` + `clean_text`/`source_text` khi được yêu cầu |
| **Mã lỗi** | `400 VALIDATION_FAILED` · `401` · `403 PROJECT_ACCESS_DISABLED` · `404 NOT_FOUND` |

### `CH-4` · `GET /v1/chapters/{chapter_id}/ingest-report` — báo cáo ingest ⭐ bằng chứng đọc được

| Mục | Nội dung |
|---|---|
| **Method · Path** | `GET /v1/chapters/{chapter_id}/ingest-report` |
| **Auth** | Bearer. Kiểm `access_state` (`API-PRJ-4`) |
| **Request** | Path: `chapter_id`. ⛔ Không query param |
| **Response `200`** | `{"chapter_id", "ingest_check": {"result","checked_at","blocked","signal_channel","source_kind"}, "text_clean_report": {"removed_summary","original_char_count","cleaned_char_count","created_at"}}` |
| **Mã lỗi** | `401` · `403 PROJECT_ACCESS_DISABLED` · `404 NOT_FOUND` · `404 INGEST_REPORT_NOT_FOUND` |

⭐ Đây là endpoint phục vụ **`UC-01` bước 9–10** — *"tóm tắt những gì đã bị `text clean` loại bỏ"* + *"kết quả phép kiểm opt-out"*. Hai khối trong **một** response vì tác giả đối chiếu **cả hai** ở cùng một màn hình.
⚠️ `ingest_check` trong response này ⭐ **luôn khác `null`**: nếu nó `null` thì hoặc dữ liệu vi phạm `INV-IC-1`, hoặc chapter được tạo bằng một đường ⛔ không đi qua `CH-1` — **cả hai đều là sự cố tuân thủ**, ⛔ không phải trạng thái hợp lệ.

### `CH-5` · `POST /v1/chapters/{chapter_id}:approve-ingest` — tác giả chấp nhận kết quả ingest

| Mục | Nội dung |
|---|---|
| **Method · Path** | `POST /v1/chapters/{chapter_id}:approve-ingest` |
| **Auth** | Bearer. ⭐ Yêu cầu **định danh người dùng thật** — đây là hành động của con người |
| **Header** | `Idempotency-Key` bắt buộc |
| **Request** | `{}` — ⛔ không tham số. ⛔ **Không có `auto_approve`, ⛔ không có endpoint hàng loạt** |
| **Response `200`** | `{"chapter_id", "ingest_approved": true, "approved_at", "change_log_id"}` |
| **Mã lỗi** | `401` · `403 PROJECT_ACCESS_DISABLED` · `404 NOT_FOUND` · `409 INGEST_NOT_COMPLETED` (chưa có `text_clean_report`) · `409 CHAPTER_SUPERSEDED` |

- ⭐ Ghi `story.chapter.ingest_approved_at = now()` + một dòng `public.change_log` với ⭐ `action_type = 'approve_ingest'` **cùng một transaction** ([ADR-017 `Q4.1`](../Architecture/ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md#q41-phát-biểu-chuẩn-normative), `Q4.3` `P-1`; `INV-12` của [`DB-Entity-Narrative-Timeline.md`](../Schema/DB-Entity-Narrative-Timeline.md)). Giá trị `action_type` đã có trong danh mục đóng ([`DB-Entity-Provenance-And-Usage.md`](../Schema/DB-Entity-Provenance-And-Usage.md)).
- ⛔ **Không có endpoint "từ chối ingest".** `UC-01` `ALT-3` chốt đường từ chối là **sửa văn bản gốc và nạp lại từ đầu** — *"đây là một file mới đi vào hệ thống"*, và toàn bộ `F1` **chạy lại kể cả chặng 4–5**. Một endpoint `reject` sẽ gợi ý rằng có đường sửa tại chỗ; ⛔ không có.

> [!IMPORTANT]
> ✅ ⭐ **`TBD-API-CH-1` — ĐÃ ĐÓNG ở lô `L34`. Đích lưu trạng thái là cột `story.chapter.ingest_approved_at` (`TIMESTAMPTZ`, nullable)** — [`DB-Entity-Narrative-Timeline.md`](../Schema/DB-Entity-Narrative-Timeline.md), `INV-11`…`INV-13`.
> - `ingest_approved` trong response của `CH-2` (`GET /v1/projects/{project_id}/chapters`) là **giá trị DẪN XUẤT**: `ingest_approved_at IS NOT NULL`. ⛔ **Không** phải một cột boolean riêng.
> - `approved_at` mà `CH-5` trả về **chính là** cột đó ⇒ ⛔ không có cột thứ hai nào phải giữ đồng bộ.
> - ⭐ **`status` ⛔ KHÔNG bị đụng tới.** Danh mục vẫn **đúng hai** giá trị `('active','superseded')`: *"đã duyệt ingest"* **trực giao** với `status` — một chapter đã duyệt vẫn có thể bị `superseded` khi tác giả nạp lại (`UC-01` `ALT-3`). ⛔ Nhét nó thành giá trị thứ ba là mất một trong hai sự thật (`INV-11`).
> - ⭐ **Nạp lại ⇒ row `chapter` MỚI với `ingest_approved_at = NULL`** ⇒ phải gọi `CH-5` lại. ⛔ Không kế thừa trạng thái duyệt của bản cũ.
> - ⛔ **Không có cột `approved_by`**: bằng chứng **ai** duyệt sống ở dòng `change_log` `action_type = 'approve_ingest'`, và `CH-5` trả `change_log_id` để nối hai đầu.
>
> ⚠️ Contract quan sát được của `CH-5` ở trên **⛔ không đổi** so với bản trước.

---

## Invariant của resource

| Mã | Invariant | Cưỡng chế bằng |
|:--:|---|---|
| **`API-CH-1`** | ⭐ **Checkbox cam kết quyền là điều kiện của TỪNG lần nạp.** ⛔ Không cờ tenant/ToS nào thay thế được | Field bắt buộc trong `CH-1` + `422 RIGHTS_WARRANT_REQUIRED`; ⛔ ⛔ không đường code nào đọc giá trị này từ ngoài request |
| **`API-CH-2`** | ⭐⭐ **Mọi lần nạp sinh ĐÚNG ≥1 dòng `story.ingest_check` kèm `checked_at` — KỂ CẢ khi `result='no_signal'`.** ⭐ **Bản ghi ÂM TÍNH mới là bằng chứng**: phép đo `M1-4` là *"100% file upload đi qua bước kiểm"*, và nó chỉ chứng minh được bằng **những dòng nói "không có gì"**. ⛔ Bỏ ghi dòng âm tính làm **sập** phép đo 100% | `INV-IC-1`/`INV-IC-2`; ⚠️ ⛔ **không cưỡng chế được bằng constraint** (⛔ không có bảng *"lần nạp"* để đặt FK ngược) ⇒ cưỡng chế bằng **một stage bắt buộc trong `CH-1`** + đối chiếu số upload với số dòng log |
| **`API-CH-3`** | Chặng 4–5 đứng **trước** chặng 6; ⛔ không có tham số đảo thứ tự | `UC-01` bước 5–7 · `KC-6`; test CI: gửi upload có signal ⇒ ⛔ **0 dòng** `story.chapter`, **1 dòng** `story.ingest_check` với `blocked=true` |
| **`API-CH-4`** | Fail-safe: `result ≠ 'no_signal'` ⇒ `blocked = TRUE` ⇒ `409` | `INV-IC-3` `CHECK (result = 'no_signal' OR blocked)`. ⭐ `'unreadable'` và `'conflicting'` **bắt buộc chặn**, ⛔ ⛔ không được coi mặc định là *"không có signal"* rồi cho qua |
| **`API-CH-5`** | `upload_ref` do **server** cấp và có mặt **trước** khi biết nội dung có đi tiếp hay không | ⛔ Client ⛔ không gửi `upload_ref`. Đây là handle làm cho nhánh bị chặn (⛔ không có `chapter_id`) vẫn ghi log được |
| **`API-CH-6`** | `checked_at` và mọi timestamp bằng chứng do **server** ghi | ⛔ ⛔ Không nhận timestamp từ client ở bất kỳ endpoint nào — cùng nguyên tắc với `INV-TR-1` |
| **`API-CH-7`** | Trùng `(timeline_id, story_order)` ⇒ tác giả **phải chọn**; ⛔ không ghi đè âm thầm | UNIQUE partial index + `409 CHAPTER_DUPLICATE_ORDER` |
| **`API-CH-8`** | ⛔ **`clean_text` ⛔ không bao giờ bị `UPDATE` tại chỗ** qua bất kỳ endpoint nào | `INV-7`; đường duy nhất là chapter mới + `superseded` |
| **`API-CH-9`** | ⛔ **⛔ Không endpoint nào ở đây gọi copyright / plagiarism / similarity detection**, ⛔ không chấm điểm nghi vấn | ⭐ `SRS-NFR-15` — xem [khối anti-feature của `Endpoint-Project.md`](./Endpoint-Project.md#-anti-feature-srs-nfr-15--đọc-trước-khi-đề-xuất-tính-năng-mới). ⚠️ Opt-out check **đọc nhãn quyền do chủ sở hữu tự khai** ⇒ ⛔ không thuộc nhóm bị cấm |

---

## UC nào tiêu thụ

| UC | Bước | Endpoint | Ghi chú ràng buộc |
|---|---|---|---|
| [UC-01](../../020-Requirements/Use-Cases/UC-01-Upload-And-Ingest-Chapter.md) | bước 2 — nạp file + khai `timeline_id`/`story_order` | `CH-1` | ⛔ Hệ thống ⛔ không suy ra khoá thời gian |
| [UC-01](../../020-Requirements/Use-Cases/UC-01-Upload-And-Ingest-Chapter.md) | bước 3 — tick cam kết quyền | `CH-1` (`rights_warrant_accepted`) | `API-CH-1` · `EXC-2` |
| [UC-01](../../020-Requirements/Use-Cases/UC-01-Upload-And-Ingest-Chapter.md) | bước 4–6 — gắn tenant, kiểm opt-out, **log kèm timestamp** | `CH-1` (chặng 3–5) | ⭐ `API-CH-2` — bản ghi âm tính |
| [UC-01](../../020-Requirements/Use-Cases/UC-01-Upload-And-Ingest-Chapter.md) | bước 7–8 — `text clean` + tách `Event` | `CH-1` (chặng 6–8) | Event ghi vào [`Endpoint-Timeline-Event.md`](./Endpoint-Timeline-Event.md) đọc lại được |
| [UC-01](../../020-Requirements/Use-Cases/UC-01-Upload-And-Ingest-Chapter.md) | bước 9 — trả tóm tắt phần bị loại + kết quả opt-out | `CH-4` | ⛔ Không có bảng report thì ⛔ không có gì để hiển thị (`EXC-4`) |
| [UC-01](../../020-Requirements/Use-Cases/UC-01-Upload-And-Ingest-Chapter.md) | bước 10 — xác nhận ingest | `CH-5` | ✅ `TBD-API-CH-1` **đã đóng** (`ingest_approved_at`) |
| [UC-01](../../020-Requirements/Use-Cases/UC-01-Upload-And-Ingest-Chapter.md) | `ALT-2` dán text · `ALT-3` nạp lại · `EXC-5` trùng | `CH-1` (`source_kind`, `supersedes_chapter_id`) | ⛔ `ALT-2` ⛔ không được miễn chặng 4–5 |
| [UC-02](../../020-Requirements/Use-Cases/UC-02-Review-And-Edit-Story-Bible.md) | tiền đề bước 1 | `CH-5` | Chapter phải `ingest_approved` mới sang `UC-02` |

⚠️ **Ranh giới**: ⛔ endpoint **kích hoạt / retry extraction** (`UC-02` bước 1, `EXC-1`) ⛔ **không** thuộc file này và ⛔ **không** có hàng nào trong [findings §4.1](../../010-Planning/pm-runs/2026-08-28-phase-2-architecture-design-comic-studio/findings/architect.md) — xem ripple ở [`TBD`](#tbd-còn-lại---không-được-bịa).

---

## `TBD` còn lại — ⛔ không được bịa

| Khoảng trống | Ai đóng | Khi nào |
|---|---|---|
| ~~**`TBD-API-CH-1`**~~ ⇒ ✅ **ĐÃ ĐÓNG** ở lô `L34`: cột `story.chapter.ingest_approved_at` (`TIMESTAMPTZ` nullable) + `action_type = 'approve_ingest'` — [`DB-Entity-Narrative-Timeline.md`](../Schema/DB-Entity-Narrative-Timeline.md) `INV-11`…`INV-13`. ⛔ `CH-5` không còn bị chặn | — (đã đóng) | — |
| **`TBD-API-CH-2`** — ngưỡng kích thước chapter mà xử lý **đồng bộ** của `CH-1` không còn khả thi (và khi đó cần một `job_type` mới) — ⛔ **không có số đo nào trong repo** | **Engineer**, sau chương thật đầu tiên | Trước khi mở đăng ký ngoài Founder |
| **`TBD-API-CH-3`** — endpoint kích hoạt/retry **extraction** (`UC-02` bước 1 · `EXC-1`) ⛔ không thuộc resource nào của findings §4.1 | **Architect + PM** | Trước lô API kế tiếp |
| Định dạng file được chấp nhận + trần dung lượng của `CH-1` — ⛔ repo im lặng | **BA + Engineer** | Trước implementation |
| Cách phát hiện **bốn kênh** opt-out ở mức kỹ thuật (parser nào cho `metadata`, `technical_protection`, `rights_management_info`, `collective_management_notice`) | **Engineer**; ⛔ danh mục kênh thì **đóng**, ⛔ không thêm giá trị | Trước `Story-Opt-Out-Check-At-Ingest` vào Active Sprint |

---

## Tài liệu tham khảo

- [Endpoint-Project.md](./Endpoint-Project.md) — `API-ENV-1`, `API-PRJ-4`, khối anti-feature `SRS-NFR-15`
- [SDD Comic Studio](../Architecture/SDD-Comic-Studio.md) — §4.1, §5.1 `F1`, §5.4, §6.1
- [ADR-006](../Architecture/ADR-006-RLS-Tenant-Context-Injection.md) · [ADR-011](../Architecture/ADR-011-Narrative-Time-Key-And-State-Reduction.md) · [ADR-015](../Architecture/ADR-015-Job-Queue-In-Postgres.md) · [ADR-017](../Architecture/ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md) · [ADR-005](../Architecture/ADR-005-Platform-Table-Schema-Placement.md)
- [DB-Entity-Narrative-Timeline.md](../Schema/DB-Entity-Narrative-Timeline.md) · [DB-Entity-Compliance-And-Takedown.md](../Schema/DB-Entity-Compliance-And-Takedown.md) · [DB-Entity-Job-Queue.md](../Schema/DB-Entity-Job-Queue.md)
- [UC-01 — Upload And Ingest Chapter](../../020-Requirements/Use-Cases/UC-01-Upload-And-Ingest-Chapter.md)
- [Story-Opt-Out-Check-At-Ingest](../../022-User-Stories/Backlog/Story-Opt-Out-Check-At-Ingest.md) · [Story-Chapter-Ingest-And-Text-Clean](../../022-User-Stories/Backlog/Story-Chapter-Ingest-And-Text-Clean.md)
- [SRS Comic Studio](../../020-Requirements/SRS-Comic-Studio.md) — `SRS-FR-04`, `SRS-FR-06`, `SRS-FR-35`, `SRS-FR-37`, `SRS-FR-41`, `SRS-NFR-01`, `SRS-NFR-13`, `SRS-NFR-15`
