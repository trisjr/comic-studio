---
id: SPEC-API-PREVIEW-EXPORT
type: spec
status: draft
project: comic-studio
created: 2026-08-29
---

# Endpoint: Preview & Export (kèm provenance readout)

Bề mặt API của **đường thành phẩm**: preview là composite **read-only trong hệ thống**, export là thành phẩm **rời khỏi hệ thống**, và cả hai là output của **đúng một compositor** (`D-32`). Resource *AI disclosure / provenance readout* nằm cùng file vì nghĩa vụ nhúng **dấu máy đọc** phát sinh ở **export path** (`D-55`) ⇒ chúng là **một bề mặt nghĩa vụ**.

**Serves:** [UC-08 — Arrange Page And Preview](../../020-Requirements/Use-Cases/UC-08-Arrange-Page-And-Preview.md) bước 9–10 · [UC-09 — Export Chapter](../../020-Requirements/Use-Cases/UC-09-Export-Chapter.md) bước 1–9

**Nguồn ràng buộc** (⛔ file này **không** đặc tả lại, chỉ trỏ theo mã):

| Ràng buộc | Nguồn duy nhất |
|---|---|
| Điều kiện chặn xuất bản | [SDD §6.3 `SDD-HG-01.4`](../Architecture/SDD-Comic-Studio.md) |
| Cơ chế cưỡng chế ở tầng DB: trigger + vị từ `comic.export_is_permitted()`, quy tắc `HG-DB-1`…`HG-DB-6` | ⭐ [`DB-Entity-Preview-And-Export.md`](../Schema/DB-Entity-Preview-And-Export.md) — ⛔ **không chép lại** |
| `change_log` cùng transaction (`KC-4`) | [ADR-017 `Q2`, `Q4.3` `P-2`](../Architecture/ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md) |
| Tenant context + RLS | [ADR-006 `D3`](../Architecture/ADR-006-RLS-Tenant-Context-Injection.md) |
| Contract polling cho tác vụ async | [ADR-015 `Q6` `CT-POLL-2S`](../Architecture/ADR-015-Job-Queue-In-Postgres.md) — ⚠️ đọc [`API-PE-6`](#invariant-của-resource) trước khi dùng |
| Signed URL: ⛔ không lưu bền, phát theo lô / theo lượt tải | [ADR-004](../Architecture/ADR-004-Object-Storage-Vendor-And-Signed-URL.md) điều 3, 6 |

---

## ⭐ Phân vai hai tầng cưỡng chế — đọc trước khi đọc mã lỗi

> [!IMPORTANT]
> ⭐ **`SDD-HG-01.4` được cưỡng chế ở HAI tầng, dùng ĐÚNG MỘT vị từ `comic.export_is_permitted()`** ([`DB-Entity-Preview-And-Export.md`](../Schema/DB-Entity-Preview-And-Export.md) `HG-DB-1`). ⛔ **Không có nguồn sự thật thứ hai** — chỉ có **hai thời điểm đánh giá cùng một vị từ**.

| Tầng | Vai trò | Cái mà API contract phải làm |
|---|---|---|
| ⭐ **Service** | **Đường của người dùng** | Gọi vị từ **trước** khi composite. Từ chối ⇒ `409` với **danh sách page thiếu gate nào**, đọc được, hành động được. **Và ghi audit lần từ chối** |
| ⭐ **Trigger DB** | **Lưới fail-closed** | ⛔ **KHÔNG BAO GIỜ được nổ trong production.** Mỗi lần nổ = **một tín hiệu sự cố** (đã có đường ghi bỏ qua tầng service), ⛔ **không** phải một luồng người dùng |

⭐ **Hệ quả trực tiếp lên mã lỗi — đây là chỗ dễ làm sai nhất của file này:**

- Trigger nổ ⇒ ⛔ **TUYỆT ĐỐI không** map thành `409`. Map thành `409` là **giấu một sự cố** dưới dạng một lỗi nghiệp vụ bình thường ⇒ tầng service hỏng sẽ ⛔ không bao giờ bị phát hiện.
- Trigger nổ ⇒ trả **`500`** cho client **và** phát **alert vận hành**. ⚠️ Người dùng ⛔ không làm gì được với lỗi này; nó ⛔ không phải lỗi của họ.
- ⇒ **Phép đo vận hành**: số lần trigger nổ trong production **phải là `0`**. Khác `0` ⇒ điều tra đường ghi, ⛔ không nới trigger.

> [!WARNING]
> ⚠️ **Lần export BỊ TỪ CHỐI phải ghi `public.change_log` ở TRANSACTION RIÊNG.**
> Lý do là cơ học, ⛔ không phải khẩu vị: trigger `RAISE EXCEPTION` **rollback toàn bộ transaction**, kể cả dòng audit vừa ghi trong chính transaction đó (`HG-DB-3`). ⇒ Handler phải commit dòng audit **độc lập** với transaction bị chặn.
> ⚠️ Điều này ⛔ **không** mâu thuẫn `KC-4`: `INV-12` áp cho lần export **THÀNH CÔNG** (artifact + `change_log` cùng transaction). Lần **từ chối** ⛔ không sinh artifact ⇒ ⛔ không có gì để bất khả phân với nó.

---

## Danh sách endpoint

> **Auth**: mọi endpoint yêu cầu **session người dùng thật** trong **một transaction tường minh** có tenant context ([ADR-006 `D3`](../Architecture/ADR-006-RLS-Tenant-Context-Injection.md)). ID ngoài tenant ⇒ **`404`** (RLS `0 row`, fail-closed), ⛔ không `403`.

| # | Method · Path | Mục đích |
|--:|---|---|
| `E-PE-1` | `POST /v1/pages/{page_id}/preview` | Yêu cầu render composite **read-only** cho **một page** |
| `E-PE-2` | `GET /v1/chapters/{chapter_id}/preview` | Đọc preview của cả chapter = **N mục cấp page** |
| `E-PE-3` | `POST /v1/chapters/{chapter_id}/export` | Yêu cầu export **một chapter hoàn chỉnh** |
| `E-PE-4` | `GET /v1/exports/{export_id}` | Đọc metadata + phát **URL tải một lượt** |
| `E-PE-5` | `GET /v1/pages/{page_id}/provenance` | ⭐ Provenance readout — nghĩa vụ AI disclosure |

---

### `E-PE-1` · `POST /v1/pages/{page_id}/preview`

| | |
|---|---|
| **Auth** | Session người dùng + tenant context |
| **Request** | Path: `page_id`. Body ⛔ rỗng — ⚠️ ⛔ **không** tham số nào ảnh hưởng nội dung render |
| **Response `200`** | `{ preview: { id, page_id, input_digest, compositor_version, rendered_at, url }, cache_hit: bool, gate_summary: { … } }` |

- ⭐ **Đơn vị là PAGE, ⛔ không có preview cấp chapter** (Quyết định #2 của [`DB-Entity-Preview-And-Export.md`](../Schema/DB-Entity-Preview-And-Export.md)). Preview cả chapter = gọi endpoint này N lần **hoặc** đọc `E-PE-2`.
- ⭐ **Preview ⛔ KHÔNG bị chặn bởi human gate** — hệ quả #2 của `SDD-HG-01`: người dùng **phải** preview được **trước** khi gate PASS, vì đó chính là cách họ đi tới PASS. ⇒ ⛔ **Không** `409` vì gate ở endpoint này.
- ⚠️ **Bất đối xứng đó HẸP đúng phạm vi hai human gate** (`HG-DB-6`): preview vẫn chịu RLS, **và vẫn kiểm `disable-access`**. ⛔ Đọc *"preview miễn gate"* thành *"preview miễn mọi kiểm"* là sai.
- ⭐ **Cache theo `input_digest`**: digest khớp ⇒ trả row cũ (`cache_hit = true`), ⛔ không render lại. Digest lệch ⇒ render mới ⇒ **row mới** (row là bất biến, ⛔ không sửa row cũ).
- `url` là signed URL **sinh tại thời điểm dựng response**; ⛔ **không** lưu bền, ⛔ không log ([ADR-004](../Architecture/ADR-004-Object-Storage-Vendor-And-Signed-URL.md) điều 3). Client coi URL hết hạn là **trạng thái bình thường**, xin lại **đúng một lần** rồi mới báo lỗi (điều 5).
- `gate_summary` mang trạng thái tổng hợp gate của page — để client ⛔ **không phải tự suy ra** điều kiện `.4` (hệ quả #5 của `SDD-HG-01`).
- ⛔ **Không có trạng thái *"đang render"*** — row tồn tại ⇔ artifact đã xong (`INV-3`). ⇒ ⛔ Không `202`, ⛔ không job id, ⛔ không polling.

| Mã lỗi | Khi nào |
|---|---|
| `404` | `page_id` ⛔ không thấy dưới RLS |
| `403 PROJECT_ACCESS_DISABLED` | ⭐ Project ở trạng thái **disable-access** do takedown. ⚠️ **⛔ Không thấy row `project_access_state` ⇒ CŨNG từ chối** — fail-closed, ⛔ tuyệt đối không đọc *"thiếu dòng"* thành `'active'`. Mã dùng chung theo [`API-PRJ-4`](./Endpoint-Project.md#invariant-của-resource) |
| `422` | Page ⛔ chưa có `page_layout` ⇒ ⛔ không có gì để composite |
| `500` | Compositor lỗi. ⚠️ ⛔ **Không** để lại row `preview_render` nào — thất bại ⇒ ⛔ không row (`INV-3`) |

---

### `E-PE-2` · `GET /v1/chapters/{chapter_id}/preview`

| | |
|---|---|
| **Auth** | Session người dùng + tenant context |
| **Request** | Path: `chapter_id` |
| **Response `200`** | `{ chapter_id, pages: [ { page_id, page_index, preview: { id, input_digest, compositor_version, rendered_at, url } \| null, is_current: bool, gate_summary } ] }` |

- ⭐ **Phạm vi chapter là một phép GỘP Ở TẦNG ĐỌC, ⛔ không phải một artifact thứ hai.** Số mục trả về = **số page đã có layout**; page chưa có layout ⛔ không xuất hiện.
- `preview = null` ⇒ page đó **chưa từng render**; `is_current = false` ⇒ đã render nhưng `input_digest` ⛔ **không còn khớp** đầu vào hiện tại ⇒ client phải gọi `E-PE-1`. ⚠️ ⛔ **Không có cột `is_stale` trong DB** — đây là **giá trị dẫn xuất tại thời điểm đọc**, ⛔ không materialize (`INV-4`).
- ⭐ Signed URL được phát **theo lô, kèm ngay trong response này** ([ADR-004](../Architecture/ADR-004-Object-Storage-Vendor-And-Signed-URL.md) điều 6 lớp 1). ⛔ **Không có** endpoint *"xin URL cho từng preview"* gọi N lần.
- ⛔ **Endpoint này ⛔ không render.** Nó chỉ đọc. Render là `E-PE-1`.

| Mã lỗi | Khi nào |
|---|---|
| `404` | `chapter_id` ⛔ không thấy dưới RLS |
| `403 PROJECT_ACCESS_DISABLED` | Project ở trạng thái disable-access (hoặc ⛔ không thấy row trạng thái) — [`API-PRJ-4`](./Endpoint-Project.md#invariant-của-resource) |

---

### `E-PE-3` · `POST /v1/chapters/{chapter_id}/export`

| | |
|---|---|
| **Auth** | ⭐ Session **người dùng thật** — `exported_by_user_id` là **người**, ⛔ không phải một cờ cấu hình |
| **Request** | `{ format: "pdf" }` |
| **Response `201`** | `{ export: { id, chapter_id, format, page_count, compositor_version, machine_readable_marking, exported_by_user_id, exported_at, url } }` |

⭐ **Thứ tự bắt buộc trong handler — ⛔ không đảo được** ([UC-09](../../020-Requirements/Use-Cases/UC-09-Export-Chapter.md) bước 2–3 **phải** đứng trước bước composite):

1. Đánh giá vị từ dùng chung ⇒ ⛔ **không thoả thì DỪNG**. ⚠️ Kiểm **sau** composite nghĩa là **đã tạo thành phẩm của page chưa duyệt**.
2. Composite server-side, **tái dùng compositor của preview** — `compositor_version` **cùng một hằng số** (`INV-1`).
3. Nhúng **dấu máy đọc** ở export path, ghi lại **cách đã áp dụng** vào `machine_readable_marking` (⛔ không backfill được).
4. `INSERT export_artifact` + `change_log` `action_type = 'export'` **cùng một transaction** ([ADR-017 `Q4.1`](../Architecture/ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md)).

- ⭐ **Phạm vi export = đúng một chapter hoàn chỉnh.** ⛔ **Không** tham số phạm vi từng phần (`page_from`/`page_to`/danh sách page) — export từng phần là hàng `TBD` của Founder, ⛔ không phải một tham số bị quên.
- ⭐ **`format` là danh mục ĐÓNG, hiện chỉ `"pdf"`.** ⛔ Không phải thiếu sót: CBZ/webtoon là MVP3, **ngoài horizon**; nghĩa vụ là **từ chối** định dạng chưa có, ⛔ không nhận rồi sinh file rỗng.
- ⛔ **⛔ KHÔNG tồn tại tham số `force`, `skip_gates`, `admin_override`, `is_draft_export` dưới bất kỳ tên nào** — ⛔ không query param, ⛔ không header, ⛔ không field body, ⛔ không scope/role (`INV-5`, `SDD-HG-01.4`).
- Export thất bại giữa chừng ⇒ ⛔ **không row nào tồn tại**; ⛔ không có *"export dở được đánh dấu thành công"* (`INV-3`).

| Mã lỗi | Khi nào — ⚠️ đọc kèm [phân vai hai tầng](#-phân-vai-hai-tầng-cưỡng-chế--đọc-trước-khi-đọc-mã-lỗi) |
|---|---|
| `409` `gates_not_passed` | ⭐ **Đường người dùng.** Body **phải** liệt kê **page nào thiếu gate nào** — ⛔ không phải một câu *"chưa đủ điều kiện"*. ⚠️ Bao gồm cả trường hợp gate 2 **đã hết hiệu lực** vì `text_budget` đổi sau lần PASS |
| `403` `PROJECT_ACCESS_DISABLED` | ⭐ Project ở disable-access do takedown; **hoặc ⛔ không thấy row trạng thái** ⇒ **từ chối** (fail-closed). Mã dùng chung theo [`API-PRJ-4`](./Endpoint-Project.md#invariant-của-resource) |
| `422` `unsupported_format` | `format` ngoài danh mục đóng |
| `422` `empty_chapter` | Chapter ⛔ không có page nào đủ điều kiện ⇒ `page_count` sẽ là `0`, mà ⛔ **không tồn tại export rỗng** (`INV-9`) |
| `404` | `chapter_id` ⛔ không thấy dưới RLS |
| ⭐ `500` `gate_guard_tripped` | ⭐⛔ **Trigger DB đã nổ** ⇒ **tín hiệu sự cố**, ⛔ **không** phải luồng người dùng. ⚠️ ⛔ **TUYỆT ĐỐI không** map về `409`. Phải phát alert vận hành |

⚠️ **Ghi audit lần từ chối** (`409` `gates_not_passed`, `403` `PROJECT_ACCESS_DISABLED`, và `500`): bắt buộc, ở **transaction RIÊNG** (`HG-DB-3`, `CO-EX-2`). ⭐ **Giá trị `action_type` = `export_denied`** — đã có trong danh mục đóng của `public.change_log` ([`DB-Entity-Provenance-And-Usage.md`](../Schema/DB-Entity-Provenance-And-Usage.md), lô Schema `L28b`), và chính `INV-CL-6` của file đó dùng đúng tên này. ⛔ **TUYỆT ĐỐI không** dùng `'export'` cho lần từ chối — làm vậy là **đếm một lần từ chối như một lần export thành công**.

> [!CAUTION]
> ⭐ **Transaction RIÊNG là bắt buộc, ⛔ không phải khẩu vị.** Trigger `RAISE EXCEPTION` chặn export ⇒ **rollback TOÀN BỘ** transaction, **kể cả** dòng `change_log` vừa ghi trong chính transaction ấy ⇒ audit **biến mất đúng lúc cần nhất**. Đây là `INV-CL-6` của [`DB-Entity-Provenance-And-Usage.md`](../Schema/DB-Entity-Provenance-And-Usage.md); cưỡng chế ở **tầng ứng dụng + test CI** (`E-PE-3`, `API-PE-4`), ⛔ **không** phải một constraint DB. ⚠️ ⛔ Điều này ⛔ **không** mâu thuẫn `KC-4`: lần từ chối ⛔ không sinh artifact ⇒ ⛔ không có gì để bất khả phân với nó.

---

### `E-PE-4` · `GET /v1/exports/{export_id}`

| | |
|---|---|
| **Auth** | Session người dùng + tenant context |
| **Request** | Path: `export_id` |
| **Response `200`** | `{ id, chapter_id, format, page_count, compositor_version, machine_readable_marking, exported_by_user_id, exported_at, download_url }` |

- ⭐ `download_url` là signed URL **phát một lần cho một lượt tải** ([ADR-004](../Architecture/ADR-004-Object-Storage-Vendor-And-Signed-URL.md) điều 6 lớp 2) — khác lớp *"đọc inline theo lô"* của `E-PE-2`.
- ⛔ **Endpoint này ⛔ không nhận `object_key` từ client.** Key **đọc ra từ DB dưới RLS** rồi mới ký. ⚠️ Một endpoint ký key do client gửi là một **public bucket thu nhỏ** — nó vô hiệu hoá chính điều 2 của ADR-004.
- ⛔ Không `PATCH`, ⛔ không `DELETE` trên resource này: `comic.export_artifact` là **append-only** (`INV-10`) — bằng chứng sửa được ⛔ không phải bằng chứng.
- ⛔ Không có *"share link công khai"* — ngoài phạm vi horizon, và nó cần một mô hình thời hạn khác hẳn.

| Mã lỗi | Khi nào |
|---|---|
| `404` | `export_id` ⛔ không thấy dưới RLS |
| `403 PROJECT_ACCESS_DISABLED` | Project đã chuyển sang disable-access **sau** lần export ⇒ ⛔ không phát URL tải mới. ⚠️ ⛔ Điều này ⛔ không thu hồi được file đã tải trước đó — xem [`API-PE-7`](#invariant-của-resource) |

---

### `E-PE-5` · `GET /v1/pages/{page_id}/provenance`

| | |
|---|---|
| **Auth** | Session người dùng + tenant context |
| **Request** | Path: `page_id`. Query: `?scope=page\|panel` (mặc định `page`) |
| **Response `200`** | `{ page_id, panels: [ { panel_id, approved_generation: { id, model_id, model_version, attempt_no }, field_provenance: [ { entity_table, entity_id, field_name, origin, generation_id, change_log_id, created_at } ], human_actions: [ { action_type, actor_user_id, occurred_at } ] } ], disclosure: { … } }` |

- ⭐ Phục vụ nghĩa vụ **AI disclosure** theo **diễn giải RỘNG** (`SRS-FR-39`) — đây là quyết định đã chốt, ⛔ không phải một hàng `TBD`.
- ⭐ **`origin` chỉ nhận `'ai'` / `'ai_edited'` / `'human'` như DB lưu.** ⛔ Không API nào *"đơn giản hoá"* ba giá trị này thành hai — chính `'ai_edited'` là thứ vẽ ra ranh giới phần được bảo hộ.
- ⭐ **Provenance của một field là LỊCH SỬ, ⛔ không phải trạng thái.** Response trả **nhiều** dòng cho cùng một field là **đúng**; *"hiện hành"* = dòng `created_at` mới nhất. ⛔ ⛔ Không endpoint nào được gộp/khử trùng làm mất dòng cũ (`ADR-017 Q3`, race hai generation đồng thời).
- ⛔ **Read-only tuyệt đối.** ⛔ Không có `POST`/`PATCH` provenance — provenance là **hệ quả** của hành động, ⛔ không phải thứ khai báo được.
- ⛔ **⛔ Endpoint này ⛔ KHÔNG chạy, ⛔ không gọi, ⛔ không trả kết quả copyright / plagiarism / similarity detection** (`SRS-NFR-15`). ⚠️ Đây là chỗ phản xạ nghề nghiệp sẽ làm ngược: *"đã có provenance thì thêm kiểm trùng cho chắc"* — thêm nó là **tự phá miễn trừ Điều 198b**.

| Mã lỗi | Khi nào |
|---|---|
| `404` | `page_id` ⛔ không thấy dưới RLS |
| `422` | `scope` ngoài tập hợp lệ |

---

## Invariant của resource

| # | Invariant | Neo |
|:--:|---|---|
| `API-PE-1` | ⭐ **Preview và export dùng ĐÚNG MỘT compositor** ⇒ `compositor_version` trong response của `E-PE-1` và `E-PE-3` cho cùng một page **phải bằng nhau**. Lệch ⇒ đã có renderer thứ hai | `D-32` · `INV-1` |
| `API-PE-2` | ⭐ **Đường sinh `export_artifact` gọi ĐÚNG MỘT vị từ dùng chung**; ⛔ tầng service ⛔ không tự viết lại phép kiểm | `HG-DB-1` · `SDD-HG-01.4` |
| `API-PE-3` | ⭐ **Trigger nổ ⇒ `500` + alert, ⛔ KHÔNG `409`.** Số lần nổ trong production phải là `0` | `HG-DB-2` |
| `API-PE-4` | ⚠️ **Lần từ chối ghi audit ở transaction RIÊNG**; lần thành công ghi artifact + `change_log` **cùng** transaction | `HG-DB-3` · `INV-12` |
| `API-PE-5` | ⭐ **⛔ Không endpoint nào nhận `object_key` từ client rồi ký.** Key đọc ra từ DB dưới RLS. Signed URL ⛔ không lưu bền, ⛔ không log, ⛔ không nhúng vào file export | [ADR-004](../Architecture/ADR-004-Object-Storage-Vendor-And-Signed-URL.md) điều 3, 6 · `INV-6` |
| ⭐ `API-PE-6` | ⚠️ **⛔ Preview và export KHÔNG đi qua hàng đợi ở horizon này** ⇒ ⛔ **không** job id, ⛔ **không** polling, ⛔ không `202`. Danh mục `job_type` là **đóng** và **loại tường minh** hai việc này. ⇒ Hai endpoint `POST` là **đồng bộ trong request**. ⚠️ **Nếu** một run sau chuyển chúng thành async: (1) thêm giá trị vào `job_type` **ở [`DB-Entity-Job-Queue.md`](../Schema/DB-Entity-Job-Queue.md) TRƯỚC**, (2) client contract khi đó là `CT-POLL-2S` của [ADR-015 `Q6`](../Architecture/ADR-015-Job-Queue-In-Postgres.md) — ⛔ **không** phát minh interval khác | `CO-EX-3` · [`DB-Entity-Job-Queue.md`](../Schema/DB-Entity-Job-Queue.md) |
| `API-PE-7` | ⚠️ **Vị từ được đánh giá TẠI THỜI ĐIỂM GHI**, ⛔ không phải lúc client đọc màn hình. Một lần reset gate commit **sau** khi export đã commit là một **trạng thái mới**, ⛔ không phải một lần bypass. ⇒ Artifact đã ra khỏi hệ thống thì ⛔ **không thu hồi được** | `INV-4` của [`DB-Entity-Comic-IR.md`](../Schema/DB-Entity-Comic-IR.md) · `SDD-HG-01.5` |
| `API-PE-8` | ⛔ **Preview ⛔ không mở đường xuất bản.** Một lần preview thành công ⛔ **không** là bằng chứng gate đã PASS, ⛔ không rút ngắn bất kỳ điều kiện nào của `E-PE-3` | [UC-08](../../020-Requirements/Use-Cases/UC-08-Arrange-Page-And-Preview.md) bước 10 |
| `API-PE-9` | ⛔ **Export ⛔ KHÔNG tiêu thụ `preview_render`.** Export chạy compositor **trực tiếp** trên dữ liệu nguồn; preview là **cache để xem** | Quyết định #2 lý do 3 |
| ⭐ `API-PE-10` | ⭐ **Compositor render DỮ LIỆU KHÔNG TIN CẬY ⇒ an toàn render là ràng buộc bắt buộc, ⛔ không phải tuỳ chọn.** Hai endpoint `POST` của file này là **bề mặt API kích hoạt** compositor, và cái compositor vẽ vào ảnh gồm **văn bản do người dùng nhập** (thoại, tên nhân vật, tên file). ⇒ Mọi lựa chọn cơ chế render phải thoả ràng buộc của `C-10`. ⚠️ ⛔ **File này ⛔ KHÔNG chốt cơ chế** — cơ chế phụ thuộc `SRS-NFR-09` còn `TBD` ⇒ xem [`TBD` còn lại](#tbd-còn-lại) | ⭐ `C-10` · `TM-F6-3` của [`Spec-Security-Threat-Model.md`](../Security/Spec-Security-Threat-Model.md) |

### ⭐ `input_digest` — đóng `CO-EX-4` ở mức API contract

[`DB-Entity-Preview-And-Export.md`](../Schema/DB-Entity-Preview-And-Export.md) `CO-EX-4` route **tiền ảnh** của `input_digest` về **lô API**. Chốt ở mức đủ để hiện thực, ⛔ không hơn:

> **`DG-1`**: `input_digest = sha256(canonical_json(payload))`, trong đó `canonical_json` **sắp khoá theo thứ tự từ điển**, ⛔ không khoảng trắng thừa, số **chuỗi hoá không mất chữ số** (toạ độ là `NUMERIC`, ⛔ không float).

`payload` phủ **đúng bốn** thành phần mà `CO-EX-4` bắt buộc, ⛔ không thêm:

| # | Thành phần | Ghi chú |
|:--:|---|---|
| 1 | `page_layout` của page | Nguồn duy nhất của bố cục (`D-22`) |
| 2 | `object_key` của **generation đã duyệt** cho từng panel, theo thứ tự panel | ⛔ Không phải signed URL — URL đổi mỗi request, ⛔ **không được** vào digest |
| 3 | Toàn bộ `comic.bubble` của các panel, **theo `reading_order`** | Đường đọc `ix_bubble_panel_order` |
| 4 | `compositor_version` | Đổi compositor ⇒ digest đổi ⇒ **buộc render lại** |

⚠️ **⛔ Ba thứ KHÔNG vào digest**: signed URL (phù du), `rendered_at` (hệ quả chứ không phải đầu vào), trạng thái human gate (preview ⛔ không phụ thuộc gate).

---

## UC nào tiêu thụ

| UC · bước | Endpoint |
|---|---|
| [UC-08](../../020-Requirements/Use-Cases/UC-08-Arrange-Page-And-Preview.md) bước 9 (yêu cầu preview) | `E-PE-1` |
| [UC-08](../../020-Requirements/Use-Cases/UC-08-Arrange-Page-And-Preview.md) bước 10 (composite server-side read-only) | `E-PE-1`, `E-PE-2` |
| [UC-09](../../020-Requirements/Use-Cases/UC-09-Export-Chapter.md) bước 1 (chọn hành động Export) | `E-PE-3` |
| [UC-09](../../020-Requirements/Use-Cases/UC-09-Export-Chapter.md) bước 2 (🔒 kiểm **cả hai** gate trước mọi việc khác) | `E-PE-3` bước 1 của handler ⇒ `409 gates_not_passed` |
| [UC-09](../../020-Requirements/Use-Cases/UC-09-Export-Chapter.md) bước 3 (🔒 kiểm disable-access) | `E-PE-3` ⇒ `403 PROJECT_ACCESS_DISABLED` |
| [UC-09](../../020-Requirements/Use-Cases/UC-09-Export-Chapter.md) bước 4 (danh sách định dạng khả dụng theo mốc) | ⚠️ Danh mục đóng `pdf` — client đọc từ hằng số contract; ngoài danh mục ⇒ `422` |
| [UC-09](../../020-Requirements/Use-Cases/UC-09-Export-Chapter.md) bước 5–7 (xác nhận · composite · nhúng watermark) | `E-PE-3` bước 2–3 của handler |
| [UC-09](../../020-Requirements/Use-Cases/UC-09-Export-Chapter.md) bước 8 (ghi `change_log`) | `E-PE-3` bước 4 — cùng transaction |
| [UC-09](../../020-Requirements/Use-Cases/UC-09-Export-Chapter.md) bước 9 (trả file) | `E-PE-4` |
| Nghĩa vụ AI disclosure Điều 11 (`SRS-FR-39`) | `E-PE-5` |

⚠️ **Phạm vi build**: trong 24 Story chỉ có **PDF của 1 chapter**; CBZ + webtoon là MVP3, **ngoài horizon**.

---

## `TBD` còn lại

| Khoảng trống | Ai đóng | Khi nào |
|---|---|---|
| ~~**`action_type` cho lần export BỊ TỪ CHỐI**~~ ⇒ ✅ **ĐÃ ĐÓNG** bởi lô Schema **`L28b`**: danh mục `public.change_log.action_type` đã mở giá trị **RIÊNG** `export_denied`, mỏ neo là `UC-09` `EF-1`/`EF-3` + `CO-EX-2` + chính `E-PE-3` này ([`DB-Entity-Provenance-And-Usage.md`](../Schema/DB-Entity-Provenance-And-Usage.md)). ⇒ Hai tầng **khớp nhau**; ⛔ không còn hành vi nào của `E-PE-3` bị chặn bởi hàng này. ⚠️ Ràng buộc **transaction RIÊNG** (`INV-CL-6`) vẫn nguyên hiệu lực | — (đã đóng) | — |
| **Export TỪNG PHẦN** — nguồn ⛔ không trả lời ⇒ `E-PE-3` giữ phạm vi **một chapter**, ⛔ không tham số phạm vi | **Founder** (PM mang câu hỏi lên) | Trước khi Story export vào Active Sprint |
| **Tập giá trị `machine_readable_marking`** — phụ thuộc `SRS-NFR-16` và phạm vi khoản 4 Điều 11 | **Luật sư** → PM → Architect | Trước mốc tuân thủ theo `GP-4` |
| **Thời hạn signed URL** — ⛔ không quyết ở đây; dùng **đúng một** hằng số của [ADR-004](../Architecture/ADR-004-Object-Storage-Vendor-And-Signed-URL.md) điều 4 | **Founder + dev** | Theo ADR-004 |
| Hình dạng chính xác của `disclosure` trong response `E-PE-5` (cái gì phải hiển thị cho người đọc cuối) | **Luật sư + PM** | Cùng lúc với `machine_readable_marking` |
| ⭐ **Cơ chế render an toàn của compositor** (`C-10`) — ⛔ chưa chọn được vì `SRS-NFR-09` (framework) còn `TBD`. ⚠️ Ràng buộc lên lựa chọn tương lai **đã chốt sẵn** ở `C-10` của [`Spec-Security-Threat-Model.md`](../Security/Spec-Security-Threat-Model.md); ⛔ **lô này ⛔ không thiết kế lại chúng**, chỉ **nhận chủ sở hữu** qua `API-PE-10` | **Architect** (bề mặt API kích hoạt compositor nằm ở file này) | **Phase 4** — trước khi compositor đầu tiên chạy |

---

## Tài liệu tham khảo

- [SDD — Comic Studio](../Architecture/SDD-Comic-Studio.md) §5.3, §6.3
- [ADR-013 — Typeset Layer Separate From Art](../Architecture/ADR-013-Typeset-Layer-Separate-From-Art.md)
- [ADR-004 — Object Storage Vendor And Signed URL](../Architecture/ADR-004-Object-Storage-Vendor-And-Signed-URL.md)
- [ADR-006 — RLS Tenant Context Injection](../Architecture/ADR-006-RLS-Tenant-Context-Injection.md)
- [ADR-010 — Tenant Isolation With RLS](../Architecture/ADR-010-Tenant-Isolation-With-RLS.md)
- [ADR-015 — Job Queue In Postgres](../Architecture/ADR-015-Job-Queue-In-Postgres.md)
- [ADR-017 — Provenance Chain And One Transaction Boundary](../Architecture/ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md)
- [`DB-Entity-Preview-And-Export.md`](../Schema/DB-Entity-Preview-And-Export.md) · [`DB-Entity-Typeset-Layer.md`](../Schema/DB-Entity-Typeset-Layer.md) · [`DB-Entity-Provenance-And-Usage.md`](../Schema/DB-Entity-Provenance-And-Usage.md) · [`DB-Entity-Job-Queue.md`](../Schema/DB-Entity-Job-Queue.md)
- [Story-Server-Side-Page-And-Chapter-Preview](../../022-User-Stories/Backlog/Story-Server-Side-Page-And-Chapter-Preview.md)
