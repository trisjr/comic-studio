---
id: ADR-015
type: adr
status: draft
project: comic-studio
created: 2026-08-29
updated: 2026-08-30
---

# ADR-015: Job queue nằm trong PostgreSQL

Related to: [SDD-Comic-Studio](./SDD-Comic-Studio.md)

> [!IMPORTANT]
> **ADR này là NGUỒN DUY NHẤT của contract *"polling 2 giây"*** ([Q6](#q6--polling-2-giây--nguồn-duy-nhất-của-contract-này)). Mọi file `Endpoint-*` cần trạng thái job **phải trỏ về đây**, ⛔ không tự đặt lại interval.
> **Đây là ADR LAI**: cơ chế **CHỐT** (ghi lại, ⛔ không mở lại) · policy vận hành **MỞ** (ADR này quyết, ở tầng design) · **`N`** của `in_flight_per_tenant` là **`TBD`** — ⛔ **không con số nào trong repo**.

---

## Context

### Cơ chế đã CHỐT — ⛔ ADR này ghi lại, không mở lại

| Nội dung | Mã | Nguồn (mã requirement) | Độ rắn |
|---|:--:|---|:--:|
| **Job queue nằm TRONG PostgreSQL**, ⛔ không broker ngoài; claim bằng `SELECT … FOR UPDATE SKIP LOCKED`; **transactional enqueue** (`INSERT generation` + `INSERT job` trong **một** transaction) ⇒ ⛔ **không bao giờ có job mồ côi** | `D-03` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) **`SRS-FR-25`** · §2.3 · §4.3 · `MVP-Scope §3 A5` | **CHỐT** |
| Câu **CLAIM job PHẢI CHỨA** điều kiện fairness per tenant: `in_flight_per_tenant < N` — ⚠️ *"nhồi vào sau là sửa lại **đúng câu SQL nóng nhất**"* | `D-42` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) **`SRS-FR-26`** · §5.2 · `MVP-Scope §3 A6` | **LAI** — cơ chế **CHỐT**, **`N` = `TBD`** |
| Cập nhật trạng thái job cho client bằng **polling 2 giây**, ⛔ không WebSocket | `D-45` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) **`SRS-NFR-06`** · §4.1 · §4.4 · §5.1 | **MẶC ĐỊNH** — đường lui ghi rõ |
| ⛔ **KHÔNG** job queue ngoài Postgres (nằm trong danh sách negative của `D-05`) | `D-05` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) **`SRS-NFR-21`** · `MVP-Scope §3 E6` | **CHỐT** (negative) |

### ⭐ Phần MỞ — `SRS` xếp rõ vào tầng design

[SRS](../../020-Requirements/SRS-Comic-Studio.md) §1.3 (bảng *"cố ý không thuộc phạm vi SRS"*) ghi thẳng: *"DDL đầy đủ, API contract, thuật toán chi tiết, **error taxonomy, retry policy per provider** | Thuộc tầng design — **sẽ được đặc tả tại tầng 030-Specs**"*.

⇒ **ADR này ĐƯỢC QUYỀN quyết ba thứ**, và đánh dấu chúng là **lựa chọn tầng design** (⛔ không phải quyết định Phase 1):
1. Schema bảng `job` ([Q2](#q2-schema-bảng-publicjob--lựa-chọn-tầng-design))
2. Retry / backoff policy ([Q4](#q4-retry--backoff--lựa-chọn-tầng-design))
3. **Error taxonomy ở mức JOB** ([Q5](#q5-error-taxonomy-mức-job--lựa-chọn-tầng-design)) — ⚠️ xem ranh giới với error taxonomy **per provider** ở [Q7](#q7-ranh-giới--adr-này-không-quyết-cái-gì)

### Những gì ADR khác ĐÃ chốt — ⛔ không quyết lại

| Đã chốt ở đâu | Nội dung |
|---|---|
| [ADR-005](./ADR-005-Platform-Table-Schema-Placement.md) mục `Q1` | Bảng job là **`public.job`** (nhóm platform / cross-cutting). Tên đủ điều kiện là **bắt buộc** trong mọi câu SQL (guardrail `G-3`) |
| ⭐ [ADR-006](./ADR-006-RLS-Tenant-Context-Injection.md) mục `D4.1`, `W-2`, `W-2b` | Role `app_worker` có **đúng một cặp policy** trên `public.job` (⛔ chỉ bảng đó), xuyên tenant; ⛔ **TUYỆT ĐỐI KHÔNG** `BYPASSRLS`. ⚠️ Xem [Q3](#q3--fairness-nằm-trong-câu-claim--và-nó-phụ-thuộc-adr-006-để-không-hỏng-im-lặng) |
| [ADR-006](./ADR-006-RLS-Tenant-Context-Injection.md) mục `D4` | Cơ chế bơm tenant context cho worker (⛔ không có HTTP request), GUC `app.current_tenant` phạm vi transaction |
| [ADR-017](./ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md) mục `Q4` | **`KC-4`** — ⚠️ **khác** transactional enqueue của `D-03`; xem [Q1](#q1-transactional-enqueue--và-ranh-giới-với-kc-4) |
| `D-02` ([SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-NFR-03`) | Worker là **process triển khai riêng, CÙNG codebase** — 2 entrypoint (`api`, `worker`), khác command. Yêu cầu: *"worker chết mà API vẫn sống"*. ⚠️ `E7` = `⛔` ở MVP1/MVP2 ⇒ **`[OoH]`**, kiến trúc phải **chừa chỗ** |

---

## Decision

### Q1. Transactional enqueue — và ranh giới với `KC-4`

**Enqueue = `INSERT generation` + `INSERT public.job` trong MỘT transaction.** ⇒ ⛔ Không bao giờ có job mồ côi, và ⛔ không bao giờ có `generation` chờ mãi mà không có job đẩy nó đi.

Phép đo (chính là AC đã ký ở [Story-Job-Queue-In-Postgres](../../022-User-Stories/Backlog/Story-Job-Queue-In-Postgres.md) mục 4): rollback transaction giữa chừng ⇒ xác nhận **cả job lẫn dữ liệu nghiệp vụ đều KHÔNG tồn tại** (all-or-nothing).

> [!WARNING]
> ⚠️ **`D-03` (transactional enqueue) và `KC-4` là HAI ràng buộc khác nhau — ⛔ đừng gộp.**
> - **`D-03`** ràng buộc: `generation` ↔ `job`.
> - **`KC-4`** ràng buộc: `generation` ↔ `change_log` + `usage_event` + `field_provenance` — [ADR-017](./ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md) mục `Q4`.
>
> [Story-Job-Queue-In-Postgres](../../022-User-Stories/Backlog/Story-Job-Queue-In-Postgres.md) mục 4 (*"ràng buộc cứng"*) nêu đúng quan hệ giữa hai cái: **transaction boundary của job phải TƯƠNG THÍCH với `KC-4`** — và ghi rõ Epic-A *"là nơi nó bị vi phạm dễ nhất"*.
> ⇒ ⛔ **ADR này KHÔNG đặc tả `KC-4`.** Trỏ về [ADR-017](./ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md) mục `Q4`.

### Q2. Schema bảng `public.job` — **lựa chọn tầng design**

> ⚠️ **Nhãn**: đây là lựa chọn của **ADR này ở tầng design** ([SRS](../../020-Requirements/SRS-Comic-Studio.md) §1.3), ⛔ **không phải** quyết định Phase 1. DDL đầy đủ (kiểu cột chính xác, index cuối cùng) thuộc **lô DB Schema**.

| Cột | Mục đích | Ghi chú |
|---|---|---|
| `id` | Khoá chính | |
| ⭐ `tenant_id` | Chủ sở hữu job | **Bắt buộc** — `D-09`; là **điều kiện tồn tại** của `in_flight_per_tenant` ([Q3](#q3--fairness-nằm-trong-câu-claim--và-nó-phụ-thuộc-adr-006-để-không-hỏng-im-lặng)). Kéo theo: bật RLS ([ADR-006](./ADR-006-RLS-Tenant-Context-Injection.md)) |
| `job_type` | Loại công việc | Danh mục giá trị: `TBD`, lô DB Schema |
| `payload` | Tham chiếu tới artifact nghiệp vụ (ví dụ `generation_id`) | ⛔ **Không** nhét dữ liệu nghiệp vụ vào payload — job **trỏ** tới dữ liệu, không **là** dữ liệu |
| `status` | Trạng thái vòng đời | Xem [Q5](#q5-error-taxonomy-mức-job--lựa-chọn-tầng-design) |
| `run_after` | Sớm nhất được claim từ lúc nào | Là cơ chế hiện thực **backoff** ([Q4](#q4-retry--backoff--lựa-chọn-tầng-design)) và là **điều kiện claim** |
| `attempt_count` | Số lần đã thử | ⚠️ **Khác** `generation.attempt_no` — xem cảnh báo dưới |
| `max_attempts` | Trần thử lại của job này | Giá trị mặc định: [Q4](#q4-retry--backoff--lựa-chọn-tầng-design) |
| `claimed_at` / `lease_expires_at` | Dấu vết lượt claim đang chạy | ⭐ Là cơ chế **chống job kẹt vĩnh viễn** khi worker chết ([Q4.3](#q43-worker-chết-giữa-chừng--job-phải-quay-lại-được)) |
| `claimed_by` | Định danh worker instance | Phục vụ chẩn đoán, ⛔ không phải khoá |
| `last_error_class` / `last_error_detail` | Phân loại lỗi lần gần nhất | [Q5](#q5-error-taxonomy-mức-job--lựa-chọn-tầng-design) |
| `created_at` / `updated_at` | Thời gian | |

**Index tối thiểu** (⚠️ hình dạng cuối cùng thuộc lô DB Schema):
- Index phục vụ **câu CLAIM** — cột dẫn đầu là **`tenant_id`**, theo `D-10`: *"`tenant_id` là cột đầu của mọi composite index"* ([ADR-006](./ADR-006-RLS-Tenant-Context-Injection.md)). ⛔ Đây **không** là chi tiết tuỳ chọn: RLS thêm một predicate `tenant_id` vào **mọi** truy vấn, index không dẫn đầu bằng `tenant_id` làm câu SQL nóng nhất mất index.
- Index phục vụ **đếm in-flight** theo `(tenant_id, status)`.

> [!CAUTION]
> ⚠️ **`job.attempt_count` ⛔ KHÔNG phải `generation.attempt_no`.**
> `generation.attempt_no` là cột **bắt buộc theo `D-59`** ([SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-FR-31`) và mang ý nghĩa **kinh tế/provenance**: mỗi lần gọi provider tốn tiền thật đều có một dòng `generation` riêng với `attempt_no` riêng ([ADR-018](./ADR-018-Usage-Event-And-Rollup-Model.md)).
> `job.attempt_count` là **hạ tầng**: bao nhiêu lần worker nhặt job này lên.
> ⛔ **Dùng một cột cho cả hai là xoá mất chi phí thật.** Một job retry vì lỗi hạ tầng (DB timeout trước khi gọi provider) ⛔ **không** làm phát sinh chi phí; một `attempt_no` mới **thì có**.

### Q3. ⭐ Fairness nằm TRONG câu CLAIM — và nó phụ thuộc `ADR-006` để không hỏng im lặng

**Câu CLAIM là MỘT câu SQL**, mang **cả ba** thứ cùng lúc:

```
SELECT ... FROM public.job
WHERE  <claimable: status + run_after <= now()>
  AND  <fairness: in_flight_per_tenant < N>
ORDER  BY ...
FOR UPDATE SKIP LOCKED
LIMIT  ...
```

⛔ **Fairness ⛔ KHÔNG được tách ra thành bước lọc riêng ở tầng ứng dụng.** `D-42` nêu thẳng lý do: *"nhồi vào sau là sửa lại **đúng câu SQL nóng nhất**"* ([SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-FR-26`). Lọc phía app sau khi đã claim cũng **không tương đương** — job đã bị lock, và hai worker chạy song song vẫn vượt trần cùng lúc.

> [!CAUTION]
> ⭐⚠️ **CẢNH BÁO FAILURE MODE — hỏng IM LẶNG. Đọc trước khi viết câu CLAIM.**
> Điều kiện `in_flight_per_tenant < N` có một **subquery đếm job đang chạy** của tenant đó — và **subquery ấy CŨNG đi qua RLS**.
> ⇒ Nếu policy `SELECT` của `app_worker` chỉ lộ row *"claim được"* mà **không phủ row đang in-flight**, phép đếm **luôn trả 0**, điều kiện fairness **không bao giờ ràng buộc** — và ⛔ **nó không báo lỗi**. Câu SQL vẫn chạy, worker vẫn nhận job, chỉ có fairness là không tồn tại.
> ⇒ ⛔ **Đây là ràng buộc đã được [ADR-006](./ADR-006-RLS-Tenant-Context-Injection.md) mục `D4.1` chốt: policy `SELECT` của `app_worker` PHẢI phủ CẢ hai loại row (claim được **VÀ** in-flight).**
> ⛔ **ADR này KHÔNG đặc tả lại RLS.** Trỏ [ADR-006](./ADR-006-RLS-Tenant-Context-Injection.md): mục `D4.1` (nội dung cặp policy) · `W-2` (test đối chiếu `pg_policies`, `rolbypassrls = false`) · ⭐ `W-2b` (**test fairness thật sự ràng buộc**: seed một tenant có `N` job in-flight, gọi CLAIM ⇒ phải trả **0 job** của tenant đó).

> [!WARNING]
> ⛔ **`N` = `TBD`. ⛔ ADR này KHÔNG chọn số.**
> [SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-FR-26` (§5.2): *"`Analysis §6.2` viết đúng chữ `N`, **không cho giá trị**"*. [SRS](../../020-Requirements/SRS-Comic-Studio.md) §5.2 cấm tự gán số: *"Bịa một con số performance là **lỗi nghiêm trọng hơn để trống nó**"*.
> **Ai đóng: PM + Architect · Khi nào: sau khi MVP0 đo tải thật** — ⚠️ **cùng chủ và cùng mốc với hàng `TBD` tương ứng trong [ADR-006](./ADR-006-RLS-Tenant-Context-Injection.md)**, ⛔ hai ADR không được để hai đáp án khác nhau.
> ⚠️ **Hệ quả vận hành phải chấp nhận**: test `W-2b` của [ADR-006](./ADR-006-RLS-Tenant-Context-Injection.md) **chỉ chạy được sau khi `N` hết `TBD`** ⇒ cho tới lúc đó, fairness có **cấu trúc** nhưng chưa có **bằng chứng nó ràng buộc**. Đây là lỗ **hợp lệ**, ⛔ không được lấp bằng một số bịa.

### Q4. Retry / backoff — **lựa chọn tầng design**

> ⚠️ **Nhãn**: ⛔ ⛔ Không nguồn Phase 1 nào đặt policy này. Đây là lựa chọn của **ADR này**, ở tầng design ([SRS](../../020-Requirements/SRS-Comic-Studio.md) §1.3). Nó **đổi được bằng config**, ⛔ không phải hằng số kiến trúc.

#### Q4.1 Chỉ retry lỗi **transient**, ⛔ không retry lỗi **permanent**

Quyết định retry **do phân loại lỗi quyết định**, ⛔ không do đếm số lần — xem [Q5](#q5-error-taxonomy-mức-job--lựa-chọn-tầng-design). ⛔ Retry mù một lỗi permanent là **đốt tiền thật** (mỗi lần gọi provider có `cost_usd`) mà không có cơ hội thành công.

#### Q4.2 Backoff **luỹ thừa có jitter**, hiện thực bằng `run_after`

Worker **không** ngủ chờ. Khi một job thất bại tạm thời, worker ghi `run_after = now() + backoff(attempt_count)` rồi **nhả job ra**. ⇒ Backoff không giữ worker slot, và job tự động không claim được cho tới khi tới hạn.

| Tham số | Giá trị mặc định | Nhãn |
|---|---|---|
| Chiến lược | Luỹ thừa cơ số 2, **có jitter** | ⭐ Jitter là bắt buộc: ⛔ không có nó thì mọi job fail cùng lúc sẽ quay lại **cùng lúc** (thundering herd) |
| `max_attempts` mặc định | **5** | **`[EM]` — lựa chọn tầng design của ADR này**, ⛔ không có nguồn |
| Trần backoff | Có trần, ⛔ không tăng vô hạn | Giá trị cụ thể: config |

⛔ **Ba con số trên KHÔNG được đọc thành chỉ tiêu NFR.** Chúng là **mặc định khởi động**, ⛔ không phải cam kết. Latency, throughput job/giờ và queue depth alert **ở lại `TBD`** — [SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-FR-25` (§5.2): *"Throughput job/giờ, queue depth alert threshold | **Không có**"*, và §5.2 cấm gán số.

#### Q4.3 Worker chết giữa chừng ⇒ job phải quay lại được

**Cơ chế: lease có hạn.** Worker claim ⇒ đặt `lease_expires_at`. Worker sống thì gia hạn; worker chết thì lease hết hạn và job **trở lại claim được**.

Phép đo (AC đã ký, [Story-Job-Queue-In-Postgres](../../022-User-Stories/Backlog/Story-Job-Queue-In-Postgres.md) mục 4): kill process worker giữa chừng rồi khởi động worker mới ⇒ job **được xử lý tiếp**, ⛔ không kẹt vĩnh viễn ở trạng thái *"đang xử lý"*.

⚠️ **Hệ quả bắt buộc: job handler phải chịu được chạy lại (at-least-once).** Lease hết hạn ⛔ không chứng minh worker đã chết — nó có thể chỉ đang chậm. ⇒ Đường ghi kết quả **phải idempotent**. ⭐ Điều này khớp thẳng với `D-64`: **idempotency là một trong hai chỗ ra tiền thật** ([ADR-018](./ADR-018-Usage-Event-And-Rollup-Model.md)) — ở đây nó ⛔ không phải tối ưu chi phí, mà là **điều kiện đúng đắn**.

⚠️ **Thời hạn lease cụ thể = `TBD`** — nó phụ thuộc thời gian sinh panel p50/p95, mà [SRS](../../020-Requirements/SRS-Comic-Studio.md) §5.2 xếp vào nhóm ⛔ **cấm gán số**. **Ai đóng: Architect + Engineer, sau khi MVP0 đo thời gian sinh panel thật.**

### Q5. Error taxonomy mức **JOB** — **lựa chọn tầng design**

> ⚠️ **Nhãn**: lựa chọn tầng design của ADR này. ⚠️ **Ranh giới**: đây là taxonomy ở **mức job/hạ tầng**. Error taxonomy **per provider** (timeout, rate limit, content policy reject của từng nhà cung cấp) thuộc [ADR-016](./ADR-016-Image-Provider-Adapter-And-Version-Pinning.md) + `Spec-Integration-Image-Provider.md` — xem [Q7](#q7-ranh-giới--adr-này-không-quyết-cái-gì).

**Trạng thái job** (danh sách đóng ở tầng này):

| `status` | Nghĩa | Có claim được không |
|---|---|:--:|
| `queued` | Chờ, đủ điều kiện claim khi `run_after <= now()` | ✅ |
| `running` | Đã claim, lease còn hạn | ⛔ (nhưng ⭐ **PHẢI được đếm** bởi subquery in-flight — [Q3](#q3--fairness-nằm-trong-câu-claim--và-nó-phụ-thuộc-adr-006-để-không-hỏng-im-lặng)) |
| `succeeded` | Xong | ⛔ |
| `failed_permanent` | ⛔ Không retry — lỗi thuộc lớp permanent | ⛔ |
| `failed_exhausted` | Đã hết `max_attempts` cho lỗi transient | ⛔ |

**Lớp lỗi** (`last_error_class`) — quyết định retry hay không:

| Lớp | Ví dụ | Xử lý |
|---|---|---|
| `transient_infra` | DB timeout, deadlock, mất kết nối | ✅ Retry + backoff. ⛔ **Không** phát sinh `generation`/`cost_usd` mới nếu chưa gọi provider |
| `transient_provider` | Provider timeout, rate limit | ✅ Retry + backoff. ⚠️ Phân loại **do adapter cung cấp** — [ADR-016](./ADR-016-Image-Provider-Adapter-And-Version-Pinning.md) |
| `permanent_input` | Payload sai, artifact tham chiếu đã bị xoá | ⛔ **Không** retry ⇒ `failed_permanent` |
| ⭐ `permanent_policy` | Provider **từ chối vì content policy** | ⛔ **Không** retry ⇒ `failed_permanent`. ⚠️ **`D-67` bắt GHI LẠI MỌI lần** provider từ chối vì content policy ([SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-NFR-20`) — ⛔ không được nuốt lỗi này |
| `permanent_unknown` | Chưa phân loại được | ⛔ Không retry; ⚠️ **phải xuất hiện được trong chẩn đoán**, ⛔ không im lặng |

⛔ **Quy tắc bao trùm: một job thất bại phải để lại TRẠNG THÁI RÕ RÀNG, ⛔ không bao giờ biến mất.** Nó phản chiếu đúng nguyên tắc của [Story-Generation-Cost-And-Model-Metadata](../../022-User-Stories/Backlog/Story-Generation-Cost-And-Model-Metadata.md) mục 4: provider lỗi trước khi trả cost ⇒ dòng `generation` **vẫn tồn tại** với trạng thái cost **tường minh là chưa biết**, ⛔ **không phải `NULL` âm thầm, ⛔ không phải `0` ngầm định**.

### Q6. ⭐ Polling 2 giây — NGUỒN DUY NHẤT của contract này

> **`CT-POLL-2S`** — Client lấy trạng thái job bằng cách **poll endpoint trạng thái với chu kỳ 2 giây**. ⛔ **Không WebSocket**, ⛔ không SSE, ⛔ không long-poll.

Nguồn: [SRS](../../020-Requirements/SRS-Comic-Studio.md) **`SRS-NFR-06`**; nhắc lại ở §4.1 (*"Trạng thái job hiển thị cho client | `SRS-NFR-06` (polling **2 giây**)"*), §4.4 (*"Client ↔ API cho trạng thái job | **Polling 2 giây**, không WebSocket"*) và §5.1 (bảng con số: *"Polling interval trạng thái job | **2 giây**"*).

**Lý do** (nguyên văn trong nguồn): *"generation mất hàng chục giây, polling là quá đủ"*.

**Độ rắn: `MẶC ĐỊNH`, ⛔ không phải `CHỐT`** — và đường lui đã được ghi **ngay trong chính lý do**: [SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-NFR-06` nói *"tiền đề đảo (generation nhanh hơn nhiều) thì mở lại được"*. ⇒ Điều kiện mở lại là **một tiền đề đo được**, ⛔ không phải sở thích UX.

**Hợp đồng cho mọi file `Endpoint-*` sắp viết:**

| Điều | Nội dung |
|---|---|
| ✅ Được làm | Trỏ về mục này bằng mã `CT-POLL-2S`; thiết kế endpoint trạng thái job **rẻ để gọi lặp** |
| ⛔ Không được làm | Tự đặt lại interval; mô tả interval như *"có thể cấu hình tuỳ client"*; thêm kênh push |
| ⚠️ Phải mang theo | Interval **2 giây** là `MẶC ĐỊNH` — file nào trích phải giữ nguyên nhãn đó, ⛔ không nâng thành `CHỐT` |

⚠️ Endpoint trạng thái job bị gọi **mỗi 2 giây cho mỗi job đang chạy, cho mỗi client** ⇒ nó là một trong những endpoint bị gọi nhiều nhất hệ thống. ⛔ Nó **không được** làm aggregate nặng hay join xuyên schema.

### Q7. Ranh giới — ADR này KHÔNG quyết cái gì

| ⛔ Không quyết | Ai quyết |
|---|---|
| Cặp policy RLS của `app_worker`, cơ chế bơm tenant context | Đã quyết ở [ADR-006](./ADR-006-RLS-Tenant-Context-Injection.md) — ⛔ không đặc tả lại |
| Vị trí schema của bảng job (`public.job`) | Đã quyết ở [ADR-005](./ADR-005-Platform-Table-Schema-Placement.md) |
| ⭐ **`KC-4`** | Đã quyết ở [ADR-017](./ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md) mục `Q4` — ⛔ không lặp lại |
| ⭐ **Error taxonomy PER PROVIDER** + retry policy per provider | [ADR-016](./ADR-016-Image-Provider-Adapter-And-Version-Pinning.md) + `Spec-Integration-Image-Provider.md`. **Đường phân chia**: adapter **phân loại** lỗi của provider ⇒ trả về một trong các lớp ở [Q5](#q5-error-taxonomy-mức-job--lựa-chọn-tầng-design); job queue **quyết định làm gì** với lớp đó |
| Credit HOLD trước enqueue (`D-60`, `KC-7`) | `ADR-019` — `[OoH]` MVP3. ⚠️ **Nhưng schema `job` phải chừa chỗ**: `D-60` bắt HOLD xảy ra **TRƯỚC** enqueue |
| **`N`** của `in_flight_per_tenant` | ⛔ **`TBD`** — PM + Architect, sau MVP0 |
| Throughput job/giờ, queue depth alert, latency | ⛔ **`TBD`** — [SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-FR-25` · §5.2 |

---

## Alternatives considered

### (a) Broker ngoài: Redis / RabbitMQ / SQS — ⛔ LOẠI (Phase 1 đã loại)

**Điểm mạnh phải ghi nhận trung thực**: broker chuyên dụng cho throughput cao hơn, có sẵn công cụ vận hành, dead-letter queue, delayed message, và ⛔ không đặt tải polling lên chính database nghiệp vụ.

**⛔ Vì sao LOẠI — đây là quyết định của Phase 1, ⛔ không phải của ADR này**: `D-05` liệt *"⛔ **KHÔNG** job queue ngoài Postgres"* vào danh sách negative ([SRS](../../020-Requirements/SRS-Comic-Studio.md) **`SRS-NFR-21`**), và `D-03` chốt *"trong PostgreSQL, ⛔ không broker ngoài"* ([SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-FR-25`, §4.3). Lý do gốc là **transactional enqueue**: broker ngoài ⛔ **không** tham gia được vào transaction của database ⇒ *"insert row rồi publish message"* luôn có một cửa sổ mà một trong hai đã xảy ra còn cái kia thì chưa ⇒ **job mồ côi**, đúng thứ `D-03` tồn tại để loại. [Story-Job-Queue-In-Postgres](../../022-User-Stories/Backlog/Story-Job-Queue-In-Postgres.md) mục 4 (*"Story này KHÔNG làm"*) ghi lại chủ ý: *"⛔ không dùng hạ tầng message queue riêng (Redis, RabbitMQ, SQS...) — chủ ý dùng Postgres để giữ modular monolith 1 DB"*.

Cộng thêm: một hạ tầng nữa cho đội **1 người**, `bus factor = 1` ([SRS](../../020-Requirements/SRS-Comic-Studio.md) §2.2).

### (b) WebSocket / SSE cho trạng thái job — ⛔ LOẠI (Phase 1 đã loại)

**Điểm mạnh**: cập nhật tức thời, ⛔ không có polling rác.

**⛔ Vì sao LOẠI**: `D-45` / `SRS-NFR-06` ([SRS](../../020-Requirements/SRS-Comic-Studio.md) §3.D) chốt polling 2 giây, ⛔ không WebSocket, với lý do *"generation mất hàng chục giây, polling là quá đủ"*. ⚠️ Độ rắn là `MẶC ĐỊNH` ⇒ **mở lại được**, nhưng **chỉ khi tiền đề đảo**: generation trở nên nhanh hơn nhiều. ⛔ Mở lại vì *"WebSocket hiện đại hơn"* ⛔ **không** phải lý do hợp lệ.

### (c) `LISTEN` / `NOTIFY` của PostgreSQL thay vì polling ở phía worker — ⛔ LOẠI

> ⚠️ **Nhãn: đây là phân tích tầng design của ADR này, ⛔ KHÔNG phải một phương án bị Phase 1 loại.** ⛔ Không nguồn Phase 1 nào nhắc tới `LISTEN`/`NOTIFY`.

**Điểm mạnh**: worker biết ngay có job mới, giảm độ trễ nhặt job xuống gần 0, ⛔ không tốn query rỗng.

**⛔ Vì sao vẫn LOẠI cho MVP**: `NOTIFY` là **fire-and-forget** — worker mất kết nối trong lúc có notify thì notify đó **mất luôn** ⇒ vẫn **bắt buộc** phải có một vòng polling dự phòng, tức là thêm một cơ chế mà ⛔ không bỏ được cơ chế nào. Ngoài ra `NOTIFY` ⛔ không mang được điều kiện fairness (`D-42`) — worker vẫn phải chạy đúng câu CLAIM để biết mình **được phép** lấy job nào. ⇒ Thêm phức tạp, ⛔ không bớt phần nào. Đây là chỗ áp nguyên tắc **KISS**; ⚠️ ⛔ **không được ghi vào bất kỳ tài liệu nào rằng "Phase 1 đã cấm `LISTEN`/`NOTIFY`"** — Phase 1 im lặng về nó.

### (d) Fairness bằng **hàng đợi riêng cho mỗi tenant** thay vì điều kiện trong câu CLAIM — ⛔ LOẠI

**Điểm mạnh**: cô lập tenant tuyệt đối; ⛔ không có subquery đếm trong câu SQL nóng.

**⛔ Vì sao LOẠI**: `D-42` chốt fairness nằm **trong câu CLAIM** ([SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-FR-26`). Ngoài ra, hàng đợi per-tenant biến số lượng đối tượng hạ tầng thành **hàm của số tenant** — với một SaaS thì đó là chi phí vận hành tăng tuyến tính theo tăng trưởng, đúng thứ đội 1 người ⛔ không chịu nổi. Và nó ⛔ **không** loại bỏ được nhu cầu trần in-flight, chỉ đổi chỗ nó.

### (e) Lọc fairness ở tầng ứng dụng **sau khi claim** — ⛔ LOẠI

**Điểm mạnh**: câu SQL đơn giản hơn, dễ đọc, dễ test.

**⛔ Vì sao LOẠI**: ⛔ **không tương đương về mặt đúng đắn**. Job đã bị `FOR UPDATE` lock trước khi lọc ⇒ worker giữ lock rồi trả lại, tạo churn. Tệ hơn: hai worker chạy song song đều thấy *"tenant này chưa đủ N"* rồi cùng nhận ⇒ **vượt trần**. Đây chính là loại race mà `D-42` tồn tại để chặn, và [SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-FR-26` gọi tên hệ quả: *"nhồi vào sau là sửa lại **đúng câu SQL nóng nhất**"*.

### (f) Retry **mọi** lỗi cho tới `max_attempts` (⛔ không phân loại) — ⛔ LOẠI

> ⚠️ **Nhãn: phân tích tầng design của ADR này.**

**Điểm mạnh**: ⛔ không cần error taxonomy, ⛔ không cần adapter phân loại lỗi, code ngắn.

**⛔ Vì sao LOẠI**: mỗi lần gọi provider có `cost_usd` **thật** (`D-59`). Retry mù 5 lần một lỗi `permanent_policy` là trả tiền 5 lần cho một kết quả chắc chắn thất bại, và làm bẩn dữ liệu COGS mà `G2` dựa vào. Nó cũng chôn mất tín hiệu mà `D-67` bắt phải ghi lại (**mọi** lần provider từ chối vì content policy — [SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-NFR-20`).

---

## Consequences

### Tích cực

- **⛔ Không thêm hạ tầng nào.** Một PostgreSQL đã có sẵn phục vụ luôn queue ⇒ giữ nguyên hình dạng `D-01`, và giữ `KC-4` ở dạng đơn giản nhất ([ADR-017](./ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md)).
- **⛔ Không bao giờ có job mồ côi** — đây là thuộc tính **cấu trúc** do transactional enqueue, ⛔ không phải thứ đạt được bằng cẩn thận.
- **`FOR UPDATE SKIP LOCKED` cho đúng ngữ nghĩa cần**: N worker song song trên M job ⇒ tổng job xử lý = M, ⛔ không job nào bị xử lý 2 lần, và ⛔ ⛔ không worker nào bị **block chờ vô hạn** vì lock contention.
- **Fairness có cấu trúc từ ngày đầu** — chỉ còn thiếu **giá trị `N`**, ⛔ không thiếu **cơ chế**. ⇒ Khi `N` được chốt, đó là đổi một hằng số, ⛔ không phải sửa câu SQL nóng nhất.
- **Chừa chỗ cho `D-02`**: worker là process riêng cùng codebase; queue trong DB làm *"worker chết mà API vẫn sống"* thành **mặc định**, ⛔ không phải tính năng phải xây.

### Tiêu cực — chi phí thật

- **Queue đặt tải lên chính database nghiệp vụ.** Polling của worker + endpoint trạng thái (mỗi **2 giây**/job/client) đều chạm PostgreSQL. ⚠️ Trần chịu tải ⛔ **không đo được** cho tới khi **có số đo thật trên platform đã chọn** ([ADR-002](./ADR-002-Hosting-Platform-And-Region.md): Render · Singapore, **MẶC ĐỊNH**) — [SRS](../../020-Requirements/SRS-Comic-Studio.md) §5.2 (`b-5`) vẫn `TBD`, ghi thẳng: `SRS-NFR-02` là `CHỐT` nhưng **chưa có con số quy mô nào để chứng minh nó đủ**.
- **Câu CLAIM là điểm nóng nhất và cũng là điểm mong manh nhất.** Nó mang đồng thời: RLS predicate + subquery fairness + `SKIP LOCKED` + `ORDER BY`. ⭐ Và failure mode tệ nhất của nó là **im lặng** ([Q3](#q3--fairness-nằm-trong-câu-claim--và-nó-phụ-thuộc-adr-006-để-không-hỏng-im-lặng)) ⇒ ⛔ **không được refactor nó nếu chưa có test `W-2b`** của [ADR-006](./ADR-006-RLS-Tenant-Context-Injection.md).
- **At-least-once, ⛔ không phải exactly-once.** Lease hết hạn có thể chạy lại một job vẫn đang chạy ⇒ **mọi handler phải idempotent**. Đây là nghĩa vụ thường trực đặt lên **mọi** job type sau này, ⛔ không phải việc làm một lần.
- **⛔ Không có observability như một hạng mục.** [SRS](../../020-Requirements/SRS-Comic-Studio.md) §5.2 (`b-7`): *"Chưa ai phát biểu observability thành một hạng mục"*, và `queue depth alert threshold` là một hàng `TBD`. ⇒ Queue này chạy **mà chưa có ngưỡng cảnh báo** — lỗ **hợp lệ**, phải ghi ra chứ ⛔ không lấp bằng số bịa.
- **Hai khái niệm "attempt" cùng tồn tại** (`job.attempt_count` vs `generation.attempt_no`) ⇒ chi phí nhận thức thường trực, và là chỗ dễ gộp nhầm nhất. Bù bằng cảnh báo tường minh ở [Q2](#q2-schema-bảng-publicjob--lựa-chọn-tầng-design) + assertion ở lô DB Schema.

### Việc còn để `TBD` — ⛔ không được bịa

| `TBD` | Ai đóng | Khi nào |
|---|---|---|
| ⭐ **`N`** của `in_flight_per_tenant < N` — ⛔ **không con số nào trong repo** ([SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-FR-26`) | **PM + Architect** | Sau khi MVP0 đo tải thật — ⚠️ **cùng mốc với hàng tương ứng của [ADR-006](./ADR-006-RLS-Tenant-Context-Injection.md)** |
| Throughput job/giờ · **queue depth alert threshold** ([SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-FR-25`) | PM + Architect | Sau MVP0 |
| Thời hạn **lease** (phụ thuộc thời gian sinh panel p50/p95, đang `TBD`) | Architect + Engineer | Sau khi MVP0 đo thời gian sinh panel |
| DDL đầy đủ của `public.job`: kiểu cột, danh mục `job_type`, hình dạng index cuối cùng | Architect (lô **DB Schema**) | Trước khi [`DB-Entity-Job-Queue.md`](../Schema/DB-Entity-Job-Queue.md) được duyệt |
| Ánh xạ chi tiết **lỗi provider → lớp lỗi job** ([Q5](#q5-error-taxonomy-mức-job--lựa-chọn-tầng-design)) | Architect, trong [ADR-016](./ADR-016-Image-Provider-Adapter-And-Version-Pinning.md) + `Spec-Integration-Image-Provider.md` | Trước khi adapter đầu tiên chạy |
| Chỗ chừa cho **HOLD credit trước enqueue** (`D-60`, `KC-7`, `[OoH]` MVP3) | Architect (lô DB Schema) + `ADR-019` | Trước khi [`DB-Entity-Job-Queue.md`](../Schema/DB-Entity-Job-Queue.md) được duyệt |
| Thứ tự `ORDER BY` của câu CLAIM (FIFO thuần hay có ưu tiên) | Architect (lô DB Schema) | Cùng mốc trên |

---

## Đã quyết ở đâu

| Quyết định | Mã `D-xx` | Nguồn (file + mã requirement) |
|---|:--:|---|
| **Job queue nằm TRONG PostgreSQL**, ⛔ không broker ngoài; claim bằng `SELECT … FOR UPDATE SKIP LOCKED`; **transactional enqueue** (`INSERT generation` + `INSERT job` một transaction) ⇒ ⛔ không job mồ côi | `D-03` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) **`SRS-FR-25`** · §2.3 · §4.3 · `MVP-Scope §3 A5` · [Story-Job-Queue-In-Postgres](../../022-User-Stories/Backlog/Story-Job-Queue-In-Postgres.md) mục 4 |
| Câu **CLAIM phải chứa** `in_flight_per_tenant < N`; ⚠️ *"nhồi vào sau là sửa lại đúng câu SQL nóng nhất"*; ⛔ **`N` = `TBD`** | `D-42` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) **`SRS-FR-26`** · §5.2 · `MVP-Scope §3 A6` |
| ⭐ **Polling 2 giây** cho trạng thái job, ⛔ không WebSocket; đường lui = tiền đề đảo | `D-45` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) **`SRS-NFR-06`** · §4.1 · §4.4 · §5.1 |
| ⛔ **KHÔNG** job queue ngoài Postgres (danh sách negative) | `D-05` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) **`SRS-NFR-21`** · `MVP-Scope §3 E6` |
| Modular monolith **1 process · 1 PostgreSQL · 3 schema** | `D-01` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) **`SRS-NFR-02`** · §2.3 · §4.3 |
| Worker là **process riêng, CÙNG codebase**, 2 entrypoint; *"worker chết mà API vẫn sống"*; `[OoH]` tới MVP3 nhưng phải **chừa chỗ** | `D-02` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-NFR-03` · `MVP-Scope §3 E7` |
| `tenant_id` trên mọi bảng + là **cột đầu mọi composite index** + RLS | `D-09`, `D-10` | [ADR-006](./ADR-006-RLS-Tenant-Context-Injection.md) — ⛔ ADR này **không đặc tả lại RLS** |
| ⭐ Role `app_worker` có **đúng một cặp policy** trên `public.job`; ⭐ policy `SELECT` **PHẢI phủ cả row in-flight**, ⛔ nếu không subquery đếm luôn ra 0 và **fairness hỏng im lặng**; ⛔ **KHÔNG** `BYPASSRLS` | `D-42` (hệ quả) | [ADR-006](./ADR-006-RLS-Tenant-Context-Injection.md) mục `D4.1`, `W-2`, ⭐ `W-2b` |
| Bảng job là **`public.job`** (nhóm platform); tên đủ điều kiện bắt buộc (`G-3`) | `D-01` (hệ quả) | [ADR-005](./ADR-005-Platform-Table-Schema-Placement.md) mục `Q1` |
| ⭐ **`KC-4`** — ⚠️ **khác** transactional enqueue; transaction boundary của job phải **tương thích** với `KC-4` | `D-50` | [ADR-017](./ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md) mục `Q4` · [SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-NFR-13` · [Story-Job-Queue-In-Postgres](../../022-User-Stories/Backlog/Story-Job-Queue-In-Postgres.md) mục 4 |
| **Adapter per image provider** — nguồn phân loại lỗi provider cho [Q5](#q5-error-taxonomy-mức-job--lựa-chọn-tầng-design) | `D-40` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-FR-23` · [ADR-016](./ADR-016-Image-Provider-Adapter-And-Version-Pinning.md) |
| `cost_usd` + `model_id` + `model_version` + **`attempt_no`** trên **MỌI** `generation` — ⚠️ ⛔ khác `job.attempt_count` | `D-59` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) **`SRS-FR-31`** · [Story-Generation-Cost-And-Model-Metadata](../../022-User-Stories/Backlog/Story-Generation-Cost-And-Model-Metadata.md) mục 4 |
| Ghi lại **MỌI** lần provider từ chối vì **content policy** | `D-67` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) **`SRS-NFR-20`** |
| **HOLD credit TRƯỚC khi enqueue** (check-rồi-gọi là race condition) — `[OoH]` MVP3, schema phải **chừa chỗ** | `D-60` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) **`SRS-FR-28`** · `MVP-Scope §6 KC-7` |
| ⭐ **Idempotency là một trong hai chỗ ra tiền thật**; ⛔ đừng dựa vào cache cứu margin | `D-64` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) **`SRS-NFR-12`** · [ADR-018](./ADR-018-Usage-Event-And-Rollup-Model.md) |
| ⭐ **Error taxonomy + retry policy thuộc TẦNG DESIGN**, được đặc tả tại `030-Specs` | — | [SRS](../../020-Requirements/SRS-Comic-Studio.md) **§1.3** (bảng ngoài phạm vi SRS) |
| ⛔ **Không** throughput job/giờ, ⛔ **không** queue depth alert threshold trong repo | — | [SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-FR-25` (§5.2) |
| ⛔ Observability chưa được phát biểu thành một hạng mục | — | [SRS](../../020-Requirements/SRS-Comic-Studio.md) §5.2 (`b-7`) |
| ⛔ **Không tự gán số** cho hàng `TBD`; *"bịa một con số performance là lỗi nghiêm trọng hơn để trống nó"* | — | [SRS](../../020-Requirements/SRS-Comic-Studio.md) §5.2 |
| `bus factor = 1`, ⛔ **không có code review** ⇒ guardrail phải là **cơ chế** | — | [SRS](../../020-Requirements/SRS-Comic-Studio.md) §2.2 (`CF-1.2` `[CHỐT]`) |

---

_Created by system-architect_
_Author: trisjr_
