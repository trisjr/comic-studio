---
id: SPEC-API-EVAL-KIT
type: spec
status: draft
project: comic-studio
created: 2026-08-29
---

# Endpoint: Eval Kit & Golden Dataset

Đặc tả **ba endpoint** của bề mặt **đo lường chất lượng model** — đọc golden dataset regression, kích hoạt một lần chạy eval kit, và so sánh kết quả **theo thời gian** để phát hiện **silent model drift**.

> [!IMPORTANT]
> ⭐ **Đây là bề mặt VẬN HÀNH cho Founder-operator, ⛔ không phải bề mặt cho tác giả.** Nó ⛔ không nằm trong luồng sản xuất truyện; ⛔ không UC nào tiêu thụ nó — xem [mục 6](#6-uc-nào-tiêu-thụ). Neo của nó là `SRS-NFR-18`/`SRS-NFR-19` và hai Story.
> ⭐ **Giá trị của nó là một thứ duy nhất**: khi chất lượng ảnh tụt, trả lời được câu ***"model đổi, hay prompt của ta đổi?"***. Mất khả năng đó thì mọi tranh luận về chất lượng trở thành cảm tính.

## Mục lục

- [0. Ràng buộc xuyên-endpoint — TRỎ, ⛔ không lặp](#0-ràng-buộc-xuyên-endpoint--trỏ--không-lặp)
- [1. Resource](#1-resource)
- [2. Danh sách endpoint](#2-danh-sách-endpoint)
- [3. Invariant của resource](#3-invariant-của-resource)
- [4. Ranh giới — cái gì ⛔ KHÔNG có ở bề mặt này](#4-ranh-giới--cái-gì--không-có-ở-bề-mặt-này)
- [5. `TBD` còn lại](#5-tbd-còn-lại)
- [6. UC nào tiêu thụ](#6-uc-nào-tiêu-thụ)
- [7. Tài liệu tham khảo](#7-tài-liệu-tham-khảo)

---

## 0. Ràng buộc xuyên-endpoint — TRỎ, ⛔ không lặp

| Mã | Nguồn duy nhất | Áp ở đâu trong file này |
|---|---|---|
| `SDD-HG-01` | [SDD §6.3](../Architecture/SDD-Comic-Studio.md) | ⛔ **Không áp** — ⛔ không endpoint nào ở đây sinh `export_artifact` hay chạm trạng thái gate. ⚠️ Ghi ra vì `eval_run` **⛔ không giữ trạng thái human gate** (`QA-8`), và ⛔ không được nhầm hai thứ |
| `ADR-015` (queue + polling **2 giây**) | [ADR-015 `Q6`](../Architecture/ADR-015-Job-Queue-In-Postgres.md) | ⭐ [`EK-2`](#ek-2--post-v1evalruns) là **async** ⇒ dùng contract `CT-POLL-2S`. ⚠️ Độ rắn là **`MẶC ĐỊNH`** — ⛔ file này ⛔ không nâng thành `CHỐT`, ⛔ không đặt lại interval |
| `ADR-017` (`KC-4`, mã `Q4.x`) | [ADR-017 `Q2` + `Q4.3` `P-2` + `Q4.5`](../Architecture/ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md) | ⭐ [`EK-2`](#ek-2--post-v1evalruns) là endpoint ghi ⇒ tuân hợp đồng trích dẫn `Q4.7`. ⚠️ **`Q4.5` là mấu chốt**: `KC-4` ⛔ **không** phải *"một transaction cho cả vòng đời job"* |
| `ADR-006` (RLS) | [ADR-006 `D1`, `D2`, `D4.2`](../Architecture/ADR-006-RLS-Tenant-Context-Injection.md) | ⭐ Cả ba bảng **có `tenant_id`** ⇒ **RLS áp bình thường, ⛔ không ngoại lệ, ⛔ không carve-out** — ⚠️ **ngược hẳn** với [`Endpoint-Takedown-Public.md`](./Endpoint-Takedown-Public.md) |

> [!CAUTION]
> ⛔⛔ **`SRS-NFR-15` — ⛔ TUYỆT ĐỐI không endpoint nào trong file này gọi copyright / plagiarism / similarity detection.**
> ⚠️ Ở bề mặt này, cám dỗ mang **hình dạng kỹ thuật vô hại**: golden dataset đã có `content_hash` của từng item và `dataset_checksum` của cả tập ⇒ *"sẵn hash rồi, thêm một phép so khớp nội dung nữa thôi"*. ⛔ **KHÔNG.**
> ⭐ **Ranh giới chính xác**: hash ở đây dùng để trả lời ***"tập dữ liệu đo có bị đổi giữa hai lần chạy không"*** — một câu hỏi về **chính dữ liệu của ta**. Nó ⛔ **không bao giờ** được dùng để đối chiếu **chéo tenant** hay để phán đoán *"nội dung này giống tác phẩm nào"*. Lập luận đầy đủ: [Spec-Security-Legal-Compliance §5](../Security/Spec-Security-Legal-Compliance.md), [Threat-Model §5](../Security/Spec-Security-Threat-Model.md) — ⛔ file này ⛔ không viết lại.

---

## 1. Resource

| Hạng mục | Nội dung |
|---|---|
| **Bảng nguồn** | [`generation.golden_dataset_item`](../Schema/DB-Entity-Quality-Assets.md) · [`generation.eval_run`](../Schema/DB-Entity-Quality-Assets.md) — cả hai ở schema `generation`, **có `tenant_id`** |
| **Số endpoint** | **3** — đúng resource #16 của [findings/architect §4.1](../../010-Planning/pm-runs/2026-08-28-phase-2-architecture-design-comic-studio/findings/architect.md) |
| **Kích cỡ dataset** | ⭐ **15–20 panel** (`SRS-NFR-19`) — đếm các item `item_status = 'valid'` của **một** `dataset_version` |
| **Hai đường kích hoạt run** | (a) `trigger_kind='manual'` ⇒ [`EK-2`](#ek-2--post-v1evalruns); (b) ⭐ `trigger_kind='scheduled'` ⇒ **job theo đồng hồ** ([SDD §7.5](../Architecture/SDD-Comic-Studio.md)) — ⛔ **không phải endpoint**, ⛔ không có HTTP request ⇒ phải **bind tenant context tường minh** theo khuôn `D4.2` |
| **Neo requirement** | `SRS-NFR-18` (eval kit) · `SRS-NFR-19` (golden dataset regression) · `SRS-FR-23` (version pinning) |

---

## 2. Danh sách endpoint

> ⚠️ **Quy ước tiền tố path**: file này dùng `/v1/eval/…`. ⛔ **Chưa có quy ước tiền tố chung** cho 14 file `Endpoint-*` — xem [`EK-Q4`](#5-tbd-còn-lại).

### `EK-1` — `GET /v1/eval/golden-dataset`

Đọc **tập** golden dataset của một `dataset_version`.

| Hạng mục | Nội dung |
|---|---|
| **Method · Path** | `GET /v1/eval/golden-dataset` |
| **Auth** | ✅ **Bắt buộc** — người dùng đã xác thực, có tenant context |
| **Tenant** | ⭐ **Có** ⇒ RLS áp khuôn chuẩn `USING (tenant_id = public.current_tenant_id())`. ⛔ Vẫn phải viết `WHERE tenant_id = …` ở tầng ứng dụng — RLS là lớp **thứ hai** |
| **Transaction** | ⭐ Đọc trong **transaction tường minh** — query autocommit ⛔ không có context ⇒ trả **0 row** (`SET LOCAL`, [SDD §6.1](../Architecture/SDD-Comic-Studio.md)) |

**Query params**:

| Param | Kiểu | Ghi chú |
|---|---|---|
| `dataset_version` | `string` | ⭐ **Bắt buộc** — item ⛔ không có nghĩa ngoài một phiên bản tập |
| `item_status` | `enum` | `valid` (**mặc định**) \| `excluded_technical_error` \| `all` |

**Response `200 OK`**:

| Trường | Ghi chú |
|---|---|
| `dataset_version` | |
| ⭐ `valid_item_count` | ⭐ **Bắt buộc có mặt** — làm cho điều kiện *"15 ≤ n ≤ 20"* trở thành thứ **kiểm được từ API**, ⛔ không phải đếm tay. ⛔ Là `COUNT(*)` dẫn xuất, ⛔ **không** phải một cột lưu — giữ **một** nguồn sự thật |
| `excluded_count` | Số item `excluded_technical_error` — ⭐ để đối chiếu *"⛔ không có phần giao nhau"* với tập chính thức |
| `items[]` | `id`, `item_status`, `panel_spec`, `score_card`, `readability_verdict`, `content_hash`, `created_at`, `source_panel_id`, `source_generation_id` |
| ⭐ `items[].reference_image_key` · `items[].output_image_key` | ⭐⭐ **KEY object storage, ⛔ KHÔNG phải bytes, ⛔ không phải URL** — xem [`INV-API-EK-4`](#3-invariant-của-resource) |

**Mã lỗi**:

| Mã | Khi nào |
|:--:|---|
| `400` | Thiếu `dataset_version` · `item_status` ngoài danh mục đóng |
| `401` / `403` | ⛔ Không định danh / ⛔ không đủ quyền |
| `404` | ⭐ `dataset_version` ⛔ không có item nào **đọc được trong tenant context hiện tại**. ⚠️ **Cố ý gộp hai trường hợp** *"⛔ không tồn tại"* và *"⛔ không thuộc về bạn"* thành **một** phản hồi — đúng `C-5`, vì RLS làm truy vấn sai tenant trả 0 row và tầng API ⛔ **không được** biến sự khác biệt đó thành hai mã lỗi |
| `500` | |

---

### `EK-2` — `POST /v1/eval/runs`

Kích hoạt **một lần chạy eval kit** trên một `dataset_version`.

| Hạng mục | Nội dung |
|---|---|
| **Method · Path** | `POST /v1/eval/runs` |
| **Auth** | ✅ Bắt buộc |
| ⭐ **Async** | ✅ **Có** — enqueue một job, ⛔ **không** chạy đồng bộ. Trạng thái lấy bằng **polling 2 giây** theo `CT-POLL-2S` ([ADR-015 `Q6`](../Architecture/ADR-015-Job-Queue-In-Postgres.md), độ rắn **`MẶC ĐỊNH`**), ⛔ không WebSocket |
| ⭐ **Endpoint trạng thái** | ⛔ **KHÔNG có endpoint trạng thái riêng ở file này** — dùng bề mặt job chung của `Endpoint-Generation.md` (resource #10 đã gộp). ⚠️ Tạo một đường polling thứ hai là **tự đẻ nguồn sự thật thứ hai** cho vòng đời job |

**Request body** — ⭐ **đúng một trường**:

```json
{ "dataset_version": "gd-2026-08" }
```

⛔ **Trường ⛔ KHÔNG được nhận**: `trigger_kind` (⭐ server ghi `'manual'` — đường `'scheduled'` ⛔ không đi qua HTTP) · `model_id` / `model_version` (⭐ **lấy từ cấu hình pin tại thời điểm chạy**, ⛔ không từ client — nhận từ client là để người gọi **khai sai** model đã dùng, và **phá chính khả năng quy trách một delta cho model**) · `metrics` · `run_status` · bất kỳ trường điểm số nào.

**Response `202 Accepted`**:

```json
{ "job_id": "uuid", "dataset_version": "gd-2026-08", "dataset_checksum_at_enqueue": "…" }
```

> [!CAUTION]
> ⭐⭐ **⛔ Response ⛔ KHÔNG trả `run_id` — và đây là điều khoản quan trọng nhất của endpoint này.**
> ⭐ **Dòng `generation.eval_run` được ghi bởi worker Ở TRANSACTION HOÀN TẤT, ⛔ KHÔNG phải lúc enqueue.**
> **Lý do bị ép, ⛔ không phải sở thích**: `QA-12` bắt `eval_run` **append-only** (`REVOKE UPDATE`/`DELETE`) ⇒ một dòng tạo lúc enqueue sẽ **⛔ không bao giờ nhận được `run_status` cuối cùng của nó**. Và `run_status` chỉ có ba giá trị `valid` / `invalid_dataset_mismatch` / `failed` — ⛔ **không có giá trị "đang chạy"** ⇒ ghi trước là **tuyên bố một kết quả chưa biết**. Ghi `'valid'` trước khi đo xong chính là biến thể của lỗi mà `QA-7` cấm: ***chạy trên tập rỗng rồi báo "100% pass"***.
> ⇒ ⭐ **Trạng thái "đang chạy" sống ở `public.job`, ⛔ không ở `eval_run`.** Client theo dõi bằng `job_id` + polling 2 giây; `eval_run` xuất hiện ở [`EK-3`](#ek-3--get-v1evalruns) **khi và chỉ khi** phép đo đã có kết luận.

**Hai ranh giới transaction — ⛔ không gộp**:

| Transaction | Ghi gì | Neo |
|---|---|---|
| **(1) Lúc enqueue** (đường API) | `INSERT public.job` + `INSERT public.change_log` — ⭐ kích hoạt một lần đo là **hành động người dùng** (`KC-2`) | [ADR-017 `Q2` + `Q4.3` `P-2`](../Architecture/ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md) |
| **(2) Lúc hoàn tất** (đường worker) | `INSERT generation.eval_run` (một dòng, trạng thái cuối cùng) | ⭐ [ADR-017 `Q4.5`](../Architecture/ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md) — `KC-4` ⛔ **không** phải *"một transaction cho cả vòng đời job"* |

**Mã lỗi**:

| Mã | Khi nào | ⚠️ Ràng buộc |
|:--:|---|---|
| `400` | Thiếu / sai kiểu `dataset_version` · body có trường bị cấm ở trên | |
| `401` / `403` | | |
| `404` | ⭐ `dataset_version` ⛔ **không có item nào** đọc được trong tenant context ⇒ đây là **lỗi gõ sai**, ⛔ không phải một phép đo. ⛔ **Không** tạo run `failed` cho nó — làm vậy sẽ **bơm rác vào chính chuỗi so sánh theo thời gian** | Gộp hai trường hợp như [`EK-1`](#ek-1--get-v1evalgolden-dataset) (`C-5`) |
| `429` | Vượt rate limit per tenant (`C-6(a)` — đếm **số request**, ⛔ không đếm tiền); ngưỡng `T-10` `TBD` | |
| `500` | | |

> [!WARNING]
> ⚠️⛔ **`dataset_version` TỒN TẠI nhưng tập ⛔ không dùng được ⇒ ⛔ KHÔNG trả lỗi HTTP.**
> Tập tồn tại mà **0 item `valid`**, hoặc checksum lệch so với kỳ vọng ⇒ request **vẫn được nhận (`202`)**, job vẫn chạy, và ⭐ **worker ghi một dòng `eval_run` với `run_status = 'failed'` / `'invalid_dataset_mismatch'` + `failure_reason` ⛔ không `NULL`**.
> ⭐ **Vì sao ⛔ không fail-fast bằng `422`**: `QA-7` đòi thất bại phải **rõ ràng VÀ BỀN**. Một lần đo hỏng mà ⛔ không để lại dòng nào là một **khoảng trống im lặng** trong chuỗi so sánh — đúng thứ làm silent drift **⛔ không phát hiện được**. ⛔ Trả `422` rồi ⛔ không ghi gì là **giấu sự cố vào mã HTTP**.

---

### `EK-3` — `GET /v1/eval/runs`

Liệt kê các lần chạy để **so sánh theo thời gian** — câu truy vấn chính của `SRS-NFR-19`.

| Hạng mục | Nội dung |
|---|---|
| **Method · Path** | `GET /v1/eval/runs` |
| **Auth** | ✅ Bắt buộc · RLS khuôn chuẩn |

**Query params**:

| Param | Kiểu | Ghi chú |
|---|---|---|
| `dataset_version` | `string` | ⭐ Lọc theo **cùng một** phiên bản dataset — điều kiện để phép so sánh có nghĩa |
| `run_status` | `enum` | `valid` \| `invalid_dataset_mismatch` \| `failed` |
| `trigger_kind` | `enum` | `scheduled` \| `manual` |
| `order_by` | `enum` | `started_at_desc` (**mặc định**) — khớp index `idx_eval_version_time` |
| `limit` · `cursor` | | |

**Response `200 OK`** — mỗi dòng **bắt buộc** mang:

| Trường | ⭐ Vì sao **bắt buộc** |
|---|---|
| `run_status` · `failure_reason` | ⭐ Client ⛔ **không được** phải suy ra *"run này có dùng được không"* |
| `metrics` | ⭐ **≥1 chỉ số SỐ HỌC tổng hợp**, ⛔ không phải mô tả định tính. Object rỗng ⛔ không tồn tại (`QA-7`) |
| ⭐ `model_id` · `model_version` | ⭐⭐ **Thiếu chúng thì một delta ⛔ KHÔNG quy trách được cho model** — và toàn bộ mục đích của bề mặt này sụp. `SRS-FR-23`, `D-40` |
| `dataset_version` · `dataset_checksum` | ⭐ Hai run cùng `dataset_version` mà **khác** checksum ⇒ tập đã đổi ⇒ ⛔ **không so sánh trực tiếp được** |
| `prompt_compiler_ref` | ⚠️ Có thể `null` — khái niệm *version* của Visual Prompt Compiler **chưa tồn tại** ([`EK-Q2`](#5-tbd-còn-lại)). ⭐ `null` ở đây nghĩa là ***"⛔ không truy được phía prompt"***, ⛔ không phải *"prompt không đổi"* |
| `started_at` · `finished_at` · `trigger_kind` | |

⛔ **Trường ⛔ KHÔNG tồn tại trong response**: bất kỳ trường **chi phí** nào (`cost_usd`, tổng tiền…) — chi phí thuộc `usage_event`/`usage_daily` ([ADR-018](../Architecture/ADR-018-Usage-Event-And-Rollup-Model.md), `QA-8`); và bất kỳ trường **trạng thái human gate** nào.

**Mã lỗi**: `400` (param ngoài danh mục đóng) · `401` / `403` · `500`. ⭐ ⛔ **Không `404`** — danh sách rỗng là **`200` với mảng rỗng**, ⛔ không phải lỗi.

---

## 3. Invariant của resource

| Mã | Invariant | Cưỡng chế bằng |
|:--:|---|---|
| **`INV-API-EK-1`** ⭐⭐ | ⛔⛔ **⛔ KHÔNG endpoint nào, ⛔ KHÔNG trường nào nhận giá trị do MODEL sinh ra vào `score_card` hoặc `readability_verdict`.** VLM ⛔ **không được** tự chấm golden dataset thay người | ⭐ **Lý do**: dataset regression là thứ dùng để **phát hiện** model drift — chấm nó bằng một model là **mất điểm neo**, và cái đo được sẽ trôi **cùng chiều** với cái cần đo. Neo: `D-66`, [ADR-007 `Q7`](../Architecture/ADR-007-VLM-Provider-For-QA-Select.md), `QA-11`. ⭐ Điểm do VLM sinh sống ở bảng **khác** (`generation.vlm_evaluation`) và ⛔ không có đường vào hai cột này |
| **`INV-API-EK-2`** | ⛔ **`readability_verdict` ⛔ không suy được từ `score_card`**, và mặc định là `'not_scored'`, ⛔ **không** PASS ngầm định | `QA-3`. ⛔ Response ⛔ **không được** "gợi ý" giá trị readability từ điểm kỹ thuật, ⛔ không được ẩn `not_scored` khỏi danh sách |
| **`INV-API-EK-3`** ⭐ | ⛔ **⛔ Không endpoint nào SỬA hay XOÁ một item / một run.** ⛔ Không `PATCH`, ⛔ không `DELETE` trong file này | ⭐ `QA-1` (item **bất biến**, sửa ⇒ `dataset_version` **mới**) + `QA-12` (`eval_run` **append-only**). ⚠️ Một kết quả đo **sửa được** thì ⛔ không dùng để so sánh theo thời gian. Nền cưỡng chế: `REVOKE UPDATE`/`DELETE` khỏi role ứng dụng |
| **`INV-API-EK-4`** | ⛔ **⛔ Không bytes ảnh đi qua API này.** [`EK-1`](#ek-1--get-v1evalgolden-dataset) trả **key** object storage, ⛔ không trả URL, ⛔ không trả base64 | `B-4` / `QA-5`. ⭐ Xem ảnh đi qua **cơ chế signed URL đã có** ([ADR-004](../Architecture/ADR-004-Object-Storage-Vendor-And-Signed-URL.md), bề mặt của `Endpoint-Generation.md`) — ⛔ **không** đẻ endpoint cấp URL thứ hai; ⛔ không bao giờ public bucket |
| **`INV-API-EK-5`** | ⛔ **⛔ Không endpoint nào chạy đo mà ⛔ không để lại một dòng `eval_run`** khi job đã khởi động | `QA-7`. Test: chạy trên `dataset_version` có **0 item `valid`** ⇒ phải tồn tại dòng `run_status='failed'` + `failure_reason IS NOT NULL`. ⭐ ⛔ **Tuyệt đối không** có đường nào trả *"100% pass"* trên tập rỗng |
| **`INV-API-EK-6`** | ⭐ **`model_id` + `model_version` do SERVER ghi từ cấu hình pin**, ⛔ không từ client | `SRS-FR-23`, `D-40`. ⚠️ Nhận từ client = cho phép khai sai model đã dùng ⇒ **drift ⛔ không truy được**, mà đó là toàn bộ mục đích |
| **`INV-API-EK-7`** | ⛔ **⛔ Không endpoint nào ở đây đo hay báo cáo CHI PHÍ** | `QA-8` + [ADR-018](../Architecture/ADR-018-Usage-Event-And-Rollup-Model.md). ⚠️ Gộp chi phí vào đây làm **mờ** chuyện chi phí VLM chưa vào COGS — đúng thứ mà việc **tách** `Spec-Integration-VLM-QA-Select.md` đang cố giữ cho nhìn thấy được |
| **`INV-API-EK-8`** | ⛔ **⛔ Không FK cứng nào từ cụm này sang dữ liệu nghiệp vụ** ⇒ ⭐ **API phải chịu được tham chiếu mềm ⛔ không phân giải được** | `QA-6`. ⇒ `source_panel_id` / `source_generation_id` có thể trỏ tới thứ **đã biến mất** (takedown, dọn dữ liệu). ⛔ Endpoint ⛔ **không được** `500` hay ẩn cả item vì một tham chiếu chết — trả nguyên giá trị, ⛔ không join bắt buộc |
| **`INV-API-EK-9`** | ⭐ **Tài sản đo lường ⛔ KHÔNG bị takedown chạm tới** | `QA-6`, `QA-10`. ⇒ ⛔ **Không** endpoint nào ở đây kiểm `project_access_state`, và ngược lại ⛔ không đường takedown nào xoá dữ liệu của cụm này. ⚠️ Điều kiện giữ cho mệnh đề này **đúng**: `provider_refusal_log` ⛔ **không lưu nội dung người dùng thô** — ⛔ đừng phá nó bằng cách thêm prompt gốc vào bất kỳ response nào |
| **`INV-API-EK-10`** | ⛔ **RLS ⛔ không có ngoại lệ ở cụm này** | Cả ba bảng **có `tenant_id`** ⇒ policy tiêu chuẩn `USING (tenant_id = public.current_tenant_id())`, ⛔ không carve-out, ⛔ **không `BYPASSRLS`**. ⚠️ ⭐ **Ngược hẳn** [`Endpoint-Takedown-Public.md`](./Endpoint-Takedown-Public.md) — ⛔ đừng mang ngoại lệ của file đó sang đây |

---

## 4. Ranh giới — cái gì ⛔ KHÔNG có ở bề mặt này

> ⭐ Mục này liệt kê những thứ **cố ý vắng mặt**. ⛔ Đọc chúng thành *"thiếu sót"* rồi bổ sung là làm hỏng một ràng buộc.

| Vắng mặt | ⭐ Vì sao | Ai đóng phần còn lại |
|---|---|---|
| ⭐ **⛔ Không có đường GHI dataset qua API** — ⛔ không `POST /golden-dataset`, ⛔ không `PATCH` item | Hai lý do chồng nhau: (1) `QA-1` — item **bất biến**, mọi thay đổi ⇒ **`dataset_version` mới**, nên ⛔ ⛔ **không tồn tại** thao tác *"sửa item"* để mà đặt endpoint; (2) golden dataset của **MVP0** được ghi tay ra file, ⛔ **không có database** ⇒ đường nạp nó vào DB ở **MVP1** là **migration/vận hành**, ⛔ không phải API sản phẩm | ⚠️ Cách nạp một `dataset_version` mới ở MVP1 = [`EK-Q1`](#5-tbd-còn-lại) |
| ⛔ **Không endpoint chấm điểm của người** | Hệ quả trực tiếp của `QA-1`: một lần chấm lại **là** một `dataset_version` mới, ⛔ không phải một `UPDATE`. Lịch sử chấm lại đi qua `public.change_log` theo `KC-2`/`QA-4` | ⚠️ Cùng hàng [`EK-Q1`](#5-tbd-còn-lại) |
| ⛔ **Không endpoint kích hoạt run `scheduled`** | Đường định kỳ là **job theo đồng hồ** ([SDD §7.5](../Architecture/SDD-Comic-Studio.md)) — ⛔ không HTTP request ⇒ phải **bind tenant context tường minh** (`D4.2`), ⛔ không thừa hưởng từ request nào | ⚠️ **Tenant nào sở hữu golden dataset** = [`EK-Q3`](#5-tbd-còn-lại) |
| ⛔ **Không endpoint trạng thái job riêng** | Dùng bề mặt job chung (`Endpoint-Generation.md`) + `CT-POLL-2S`. ⚠️ Endpoint trạng thái job bị gọi **mỗi 2 giây / job / client** ⇒ nó ⛔ **không được** làm aggregate nặng hay join xuyên schema | — |
| ⛔ **Không endpoint đọc `provider_refusal_log`** | Bảng thứ ba của cụm `Quality Assets` phục vụ **tín hiệu abuse**, ⛔ không phải eval kit. Ngưỡng cảnh báo là hàng **LAI** — cơ chế CHỐT, **ngưỡng `TBD`** ⇒ ⛔ ⛔ không đẻ endpoint quanh một ngưỡng chưa có | **PM + Architect**, khi có dữ liệu thật từ MVP1 |

---

## 5. `TBD` còn lại

| Mã | Nội dung | Ai đóng | Khi nào |
|:--:|---|---|---|
| **`EK-Q1`** ⭐ | **Đường nạp một `dataset_version` mới ở MVP1** — migration, script vận hành, hay một endpoint admin? ⚠️ Gắn với hàng `TBD` đang mở của tầng schema: ⛔ **⛔ không có bảng cấp *TẬP* dataset** (SDD chốt closed list 38 entity) ⇒ ⛔ **không có chỗ ghi `stopped_reason`** khi MVP0 dừng giữa chừng và số panel **< 15** | **Architect + PM** | Trước migration đầu tiên của schema `generation` |
| **`EK-Q2`** | **Nội dung và định dạng của `prompt_compiler_ref`** — [ADR-014](../Architecture/ADR-014-Deterministic-Prompt-Compiler-And-Best-Of-N.md) ⛔ chưa định nghĩa khái niệm *version* cho Visual Prompt Compiler ⇒ ⛔ ⛔ không có gì để trỏ tới. ⚠️ Hệ quả cho API: một delta hiện **chỉ** quy trách được cho **model**, ⛔ chưa quy trách được cho **prompt** | **Architect + Engineer** | Khi ADR-014 hoặc lô schema prompt/vocabulary chốt |
| **`EK-Q3`** | **Tenant nào sở hữu golden dataset** khi nạp vào DB ở MVP1 — MVP0 *"⛔ không DB, ⛔ không tenant"*, nhưng `tenant_id NOT NULL` + RLS + job định kỳ đều cần một câu trả lời. ⛔ **Không tự gán một "tenant hệ thống"** | **Architect + PM** | Trước exit criterion `M1-6` |
| **`EK-Q4`** | **Ngưỡng** rate limit per tenant cho [`EK-2`](#ek-2--post-v1evalruns) (`T-10`) · **quy ước tiền tố path** chung cho 14 file `Endpoint-*` | **PM + Architect** (ngưỡng) · **PM** (path) | Sau khi đo tải · trước khi lô API được duyệt |
| **`EK-Q5`** | ⚠️ **Số item `valid` NGOÀI khoảng 15–20 thì `run_status` là gì** — ⛔ ⛔ không nguồn nào pin. ⭐ Điều file này **đã làm**: bắt `valid_item_count` xuất hiện trong response ⇒ điều kiện **nhìn thấy được**, ⛔ không bị nuốt. ⛔ **File này ⛔ không tự quyết** biến nó thành `failed`, vì nó dính hàng `stopped_reason` của [`EK-Q1`](#5-tbd-còn-lại) | **Architect + PM** | Cùng mốc `EK-Q1` |

---

## 6. UC nào tiêu thụ

> [!IMPORTANT]
> ⭐⭐ **⛔ KHÔNG Use Case nào tiêu thụ file này — và đó là ĐÚNG, ⛔ không phải một lỗ hổng coverage.**
> Tiêu chí nghiệm thu *"10 UC trong phạm vi đều có endpoint đứng sau mọi bước nghiệp vụ"* được đo trên **ma trận UC**; file này ⛔ **không đóng góp hàng nào** vào ma trận đó. Nó là bề mặt **vận hành**, neo vào **NFR + Story**, ⛔ không vào luồng người dùng.
> ⚠️ ⭐ Đây chính là hình dạng mà `findings/business-analyst §1.3` cảnh báo: **bộ lọc UC giới hạn phạm vi *BUILD*, ⛔ không giới hạn phạm vi *SCHEMA/NFR***. Dùng một mình ma trận UC để nghiệm thu sẽ **làm rơi đúng những bề mặt như file này**.

| Endpoint | Nguồn tiêu thụ | Ghi chú ràng buộc |
|---|---|---|
| [`EK-1`](#ek-1--get-v1evalgolden-dataset) | `SRS-NFR-19` · Story-Golden-Dataset-For-Regression | ⭐ `valid_item_count` làm phép đo *"15–20 panel"* kiểm được; `excluded_count` làm phép đối chiếu *"⛔ không có phần giao nhau"* kiểm được |
| [`EK-2`](#ek-2--post-v1evalruns) | `SRS-NFR-18` · Story-HITL-Gate-And-Eval-Kit | 🔒 ⛔ **Không** ghi `eval_run` lúc enqueue (`QA-12`); 🔒 tập rỗng/hỏng ⇒ **`failed` có dòng**, ⛔ không phải `422` im lặng |
| [`EK-3`](#ek-3--get-v1evalruns) | `SRS-NFR-19` · `SRS-FR-23` | 🔒 `model_id` + `model_version` **bắt buộc** trong mỗi dòng — thiếu thì drift ⛔ không truy được |
| ⛔ **⛔ Không endpoint nào** | Ghi lại phán đoán **readability của NGƯỜI** (Story-Record-Readability-Human-Judgement) | ⚠️ Có chủ đích — xem [mục 4](#4-ranh-giới--cái-gì--không-có-ở-bề-mặt-này) và [`EK-Q1`](#5-tbd-còn-lại). ⭐ Nghĩa vụ chấm là **liên tục**, ⛔ không dừng sau MVP0 ⇒ hàng này ⛔ không được để rơi |

---

## 7. Tài liệu tham khảo

| Tài liệu | Dùng cho phần nào |
|---|---|
| [DB-Entity-Quality-Assets](../Schema/DB-Entity-Quality-Assets.md) | ⭐ **Nguồn chuẩn của bảng, cột, `QA-1`…`QA-13`, index, RLS** |
| [ADR-007 — VLM Provider For QA-Select](../Architecture/ADR-007-VLM-Provider-For-QA-Select.md) | ⭐ `Q7` — `D-66`: ⛔ không dùng VLM tự chấm golden dataset thay người |
| [ADR-015 — Job Queue In Postgres](../Architecture/ADR-015-Job-Queue-In-Postgres.md) | `Q6` `CT-POLL-2S` (độ rắn **`MẶC ĐỊNH`**) · `Q5` error taxonomy mức job |
| [ADR-017 — Provenance Chain And One Transaction Boundary](../Architecture/ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md) | `Q2` · `Q4.3` `P-2` · ⭐ `Q4.5` ranh giới vòng đời job · `Q4.7` hợp đồng trích dẫn |
| [ADR-006](../Architecture/ADR-006-RLS-Tenant-Context-Injection.md) · [ADR-004](../Architecture/ADR-004-Object-Storage-Vendor-And-Signed-URL.md) · [ADR-018](../Architecture/ADR-018-Usage-Event-And-Rollup-Model.md) | RLS + `D4.2` job theo đồng hồ · signed URL · ranh giới đo chi phí |
| [SDD-Comic-Studio](../Architecture/SDD-Comic-Studio.md) | §3.1 vị trí schema · §4.1 `B-4` · §6.1 transaction tường minh · §6.4 audit chất lượng model · §7.5 job theo đồng hồ · §8.2 `S-5` |
| [Spec-Security-Threat-Model](../Security/Spec-Security-Threat-Model.md) · [Spec-Security-Legal-Compliance](../Security/Spec-Security-Legal-Compliance.md) | `C-5` · `C-6` · §5 anti-feature `SRS-NFR-15` |
| [SRS-Comic-Studio](../../020-Requirements/SRS-Comic-Studio.md) | `SRS-NFR-18` · `SRS-NFR-19` · `SRS-NFR-20` · `SRS-FR-23` · ⛔ `SRS-NFR-15` |
| [Story-Golden-Dataset-For-Regression](../../022-User-Stories/Backlog/Story-Golden-Dataset-For-Regression.md) · [Story-HITL-Gate-And-Eval-Kit](../../022-User-Stories/Backlog/Story-HITL-Gate-And-Eval-Kit.md) · [Story-Record-Readability-Human-Judgement](../../022-User-Stories/Backlog/Story-Record-Readability-Human-Judgement.md) | Cấu trúc endpoint · `QA-1`, `QA-3`, `QA-7` |
| [findings/architect §4.1](../../010-Planning/pm-runs/2026-08-28-phase-2-architecture-design-comic-studio/findings/architect.md) · [findings/business-analyst §1.3](../../010-Planning/pm-runs/2026-08-28-phase-2-architecture-design-comic-studio/findings/business-analyst.md) | Resource #16 · ranh giới nghiệm thu UC vs NFR |

---

_Created by architect_
_Author: trisjr_
