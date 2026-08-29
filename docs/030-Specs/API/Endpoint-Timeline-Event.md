---
id: SPEC-API-TIMELINE-EVENT
type: spec
status: draft
project: comic-studio
created: 2026-08-29
---

# Endpoint: Timeline & Event

Resource này phơi ra **khoá thời gian tự sự** của hệ thống. Nó nhỏ về số endpoint nhưng là nơi một lỗi **⛔ không crash, chỉ sai âm thầm** — panel hồi tưởng render state của hiện tại (`R-15`).

Bảng nguồn: [`story.timeline`](../Schema/DB-Entity-Narrative-Timeline.md) · [`story.event`](../Schema/DB-Entity-Narrative-Timeline.md).

> [!IMPORTANT]
> ⭐ **Hai trục, ⛔ không gộp** (`ADR-011 D1`):
> `story_order` = **fabula** — thứ tự sự việc **xảy ra**. ⭐ Trục dùng cho **MỌI** truy vấn as-of state.
> `reading_order` = **syuzhet** — thứ tự người đọc **gặp** sự kiện. ⛔ **Không được dùng để sắp xếp trong bất kỳ đường resolve state nào** (`D8`, guardrail `D-17`).
> ⛔ **⛔ Không tồn tại `chapter_no`/`scene_no` làm khoá thời gian** ở bất kỳ request/response nào của file này.

**Decided in:** [ADR-011](../Architecture/ADR-011-Narrative-Time-Key-And-State-Reduction.md) `D1`–`D6`, `D9`, `D11` · [ADR-017 `Q2`](../Architecture/ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md) · [ADR-006 `D3`](../Architecture/ADR-006-RLS-Tenant-Context-Injection.md) · [SDD §5.1 `F1`/`F2`](../Architecture/SDD-Comic-Studio.md)

⭐ **Bốn ràng buộc xuyên-endpoint** (`SDD-HG-01` · `ADR-015` · `ADR-017` · `ADR-006`) và **quy ước chung `API-ENV-1`**: xem [`Endpoint-Project.md`](./Endpoint-Project.md). ⛔ File này **không lặp lại**.

---

## Danh sách endpoint

### `TE-1` · `GET /v1/projects/{project_id}/timelines` — liệt kê mạch thời gian

| Mục | Nội dung |
|---|---|
| **Method · Path** | `GET /v1/projects/{project_id}/timelines` |
| **Auth** | Bearer. Kiểm `access_state` (`API-PRJ-4` của [`Endpoint-Project.md`](./Endpoint-Project.md)) |
| **Request** | Query: `kind`? (`main`\|`flashback`\|`parallel`\|`dream`) · `limit` · `cursor` |
| **Response `200`** | `{"items": [{"id","kind","anchor_order","label","chapter_count","event_count","created_at"}], "next_cursor"}` |
| **Mã lỗi** | `400 VALIDATION_FAILED` · `401` · `403 PROJECT_ACCESS_DISABLED` · `404 NOT_FOUND` |

⭐ `timeline` là **đơn vị cô lập của phép `reduce`** (`D9`) ⇒ endpoint này là đường để client biết mình được phép truyền `timeline_id` nào cho `resolveState` ([`Endpoint-Story-Bible.md`](./Endpoint-Story-Bible.md) `SB-6`).

### `TE-2` · `POST /v1/projects/{project_id}/timelines` — tạo mạch thời gian

| Mục | Nội dung |
|---|---|
| **Method · Path** | `POST /v1/projects/{project_id}/timelines` |
| **Auth** | Bearer. ⭐ Định danh người dùng thật |
| **Request** | `{"kind", "label", "anchor_order"?: <NUMERIC>}` |
| **Response `201`** | Timeline vừa tạo + `{"change_log_id"}` |
| **Mã lỗi** | `400 VALIDATION_FAILED` · `400 UNKNOWN_FIELD` · `401` · `403 PROJECT_ACCESS_DISABLED` · `404 NOT_FOUND` · **`409 TIMELINE_MAIN_EXISTS`** · **`422 ANCHOR_ORDER_RULE_VIOLATED`** |

- `kind` thuộc **đúng bốn giá trị** của `D3` — ⛔ không thêm. Giá trị ngoài danh mục ⇒ `422 UNPROCESSABLE`.
- ⭐ **`422 ANCHOR_ORDER_RULE_VIOLATED`**: `anchor_order IS NULL` ⇔ `kind = 'main'` (`INV-2`, `CHECK ((kind = 'main') = (anchor_order IS NULL))`). ⇒ nhánh ⛔ không phải `main` **bắt buộc** khai neo; `main` **bắt buộc** ⛔ không khai.
- ⭐ **`409 TIMELINE_MAIN_EXISTS`**: mỗi project có **tối đa một** timeline `kind='main'` (UNIQUE partial index). ⛔ Không tham số `force`.
- Ghi `public.change_log` **cùng transaction**.

### `TE-3` · `GET /v1/projects/{project_id}/events` — liệt kê event mức scene

| Mục | Nội dung |
|---|---|
| **Method · Path** | `GET /v1/projects/{project_id}/events` |
| **Auth** | Bearer. Kiểm `access_state` (`API-PRJ-4`) |
| **Request** | Query: `timeline_id`? · `chapter_id`? · `story_order_gte`? · `story_order_lte`? · ⭐ `order_by` (`story_order`\|`reading_order`, **bắt buộc khai tường minh**) · `limit` · `cursor` |
| **Response `200`** | `{"items": [{"id","chapter_id","timeline_id","story_order","reading_order","beat_no","summary","attribute_event_count","updated_at"}], "next_cursor"}` |
| **Mã lỗi** | `400 VALIDATION_FAILED` · **`400 ORDER_BY_REQUIRED`** · `401` · `403 PROJECT_ACCESS_DISABLED` · `404 NOT_FOUND` |

> [!WARNING]
> ⭐ **`order_by` ⛔ KHÔNG có mặc định ẩn.**
> Sắp xếp theo trục sai là lỗi **im lặng**: kết quả vẫn trả về, vẫn có thứ tự, chỉ là **sai ở mọi flashback**. Bắt client khai tường minh là cách rẻ nhất để lỗi đó ⛔ không bao giờ mặc định xảy ra.
> ⛔ **⛔ Không nhận `order_by=chapter_no`, ⛔ không nhận `order_by=created_at`.** Danh mục **đóng**, hai giá trị.

⭐ `story_order_gte`/`story_order_lte` là **đúng hình dạng của `reduce`** và chạy trên index nóng nhất của schema `story`: `(tenant_id, timeline_id, story_order)`.
⛔ **⛔ Không có filter theo `beat_no`** và ⛔ không có `order_by=beat_no` — `beat_no` ⛔ **không tham gia khoá sắp xếp** (`INV-5`). Một filter như thế là tín hiệu thiết kế gợi ý điều ngược lại.

### `TE-4` · `PATCH /v1/events/{event_id}` — sửa event ⭐ nơi `story_order` được biên tập

| Mục | Nội dung |
|---|---|
| **Method · Path** | `PATCH /v1/events/{event_id}` |
| **Auth** | Bearer. ⭐ Định danh người dùng thật |
| **Request** | `{"story_order"?, "reading_order"?, "timeline_id"?, "beat_no"?, "summary"?}` — ít nhất một field |
| **Response `200`** | Xem khối *Response* dưới bảng |
| **Mã lỗi** | `400 VALIDATION_FAILED` · `400 UNKNOWN_FIELD` · `401` · `403 PROJECT_ACCESS_DISABLED` · `404 NOT_FOUND` · **`409 EVENT_ORDER_CONFLICT`** · **`422 STORY_ORDER_REQUIRED`** · `422 TIMELINE_PROJECT_MISMATCH` |

- ⭐ **`story_order` editable qua UI là yêu cầu CHỐT** (`D-15`, `D2`) ⇒ endpoint này tồn tại vì ràng buộc nghiệp vụ, ⛔ không phải vì tiện.
- ⭐ **`409 EVENT_ORDER_CONFLICT`**: `(tenant_id, timeline_id, story_order)` là **UNIQUE** (`INV-4`). ⛔ **Server ⛔ không tự dịch giá trị sang chỗ trống** — hai event cùng `(timeline_id, story_order)` là hai phần tử **không so sánh được**, làm `reduce` phụ thuộc plan của Postgres ⇒ **mất tính tất định** của `D6`. `details` trả `conflicting_event_id` + `suggested_story_order` (trung điểm) để client hỏi lại người dùng.
- **Quy tắc cấp phát** (`D2`): giá trị mới = `max(story_order) + 1000` trong phạm vi `timeline_id`; chèn giữa hai event = **trung điểm**. ⛔ **⛔ Không tái sử dụng giá trị cũ** (`D11`).
- ⭐ **`422 STORY_ORDER_REQUIRED`**: ⛔ **không** nhận `story_order: null`. `INV-1` — `NOT NULL`, ⛔ **không `DEFAULT`**, và ⛔ hệ thống **⛔ không tự suy ra** giá trị từ `(chapter, scene)`.
- `beat_no` sửa được nhưng ⛔ **không đổi thứ tự resolve** (`INV-5`). Muốn chia nhỏ hơn scene ⇒ **cấp một `story_order` riêng** (bước 1000 chừa sẵn chỗ), ⛔ không dùng `beat_no`.
- `timeline_id` sửa được (một scene hồi tưởng nằm trong chapter mạch chính) nhưng phải **cùng `project`** — `422 TIMELINE_PROJECT_MISMATCH`, nền là composite FK `(tenant_id, …, project_id)` (`INV-3`).

**Response `200`** — ⭐ **cảnh báo là một phần của contract, ⛔ không phải chuyện của UI**:

```json
{
  "id": "…",
  "timeline_id": "…",
  "story_order": 2500,
  "reading_order": 3000,
  "beat_no": null,
  "summary": "…",
  "change_log_id": "…",
  "state_recompute_warning": {
    "story_order_changed": true,
    "affected_attribute_event_count": 7,
    "affected_panel_ids": ["…"],
    "message": "resolveState() se tra ket qua khac cho cac panel da sinh"
  }
}
```

> [!IMPORTANT]
> ⭐ **`state_recompute_warning` BẮT BUỘC có mặt khi `story_order` hoặc `timeline_id` đổi.**
> `UC-02` `EXC-5` chốt: hệ thống **cảnh báo** rằng thay đổi này làm `resolveState()` trả kết quả khác cho các panel **đã sinh**, và ghi `change_log`. `R-15`: khoá thời gian sai ⇒ **panel hồi tưởng render state của hiện tại** — lỗi ⛔ không crash, chỉ sai âm thầm. ⇒ ⛔ **Cảnh báo phải hiện, ⛔ không được ẩn**, và cách duy nhất bảo đảm điều đó ở mọi client là đặt nó vào **response**.
> ⚠️ Đây ⛔ **không phải** một xác nhận hai bước: endpoint **vẫn thực hiện** thay đổi. `D-15` cho phép biên tập; nghĩa vụ là **nói ra hệ quả**, ⛔ không phải chặn.

⚠️ **`affected_panel_ids` là dữ liệu của schema `comic`** ⇒ nó được lấy qua tầng service ở **hướng `comic → story`** hợp lệ, ⛔ **không phải** bằng một câu join từ `story` sang `comic`. Xem [`TBD-API-TE-1`](#tbd-còn-lại---không-được-bịa).

---

## Invariant của resource

| Mã | Invariant | Cưỡng chế bằng |
|:--:|---|---|
| **`API-TE-1`** | ⭐ **Hai trục ⛔ không gộp và ⛔ không có mặc định ẩn.** `order_by` bắt buộc ở `TE-3`; ⛔ ⛔ không giá trị `chapter_no`/`created_at` | `400 ORDER_BY_REQUIRED`; `D1` · `D8` · guardrail `D-17` |
| **`API-TE-2`** | ⭐ `story_order` ⛔ **không được thiếu và ⛔ không được suy ra** | `422 STORY_ORDER_REQUIRED`; `INV-1` `NOT NULL` ⛔ không `DEFAULT` |
| **`API-TE-3`** | ⭐ `(tenant_id, timeline_id, story_order)` **DUY NHẤT**; ⛔ server ⛔ không tự dịch để tránh xung đột | `409 EVENT_ORDER_CONFLICT`; `INV-4` — điều kiện của tính tất định `D6` |
| **`API-TE-4`** | ⭐ **Đổi `story_order`/`timeline_id` ⇒ response BẮT BUỘC mang `state_recompute_warning`** | `UC-02` `EXC-5` · `R-15`; test CI: sửa `story_order` của một event có panel tham chiếu ⇒ field ⛔ không được vắng |
| **`API-TE-5`** | Mỗi thay đổi `story_order` sinh **1** `public.change_log`, commit **cùng transaction**; ⛔ giá trị cũ ⛔ không được dùng lại | [ADR-017 `Q2`](../Architecture/ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md#q2-change_log-kc-2--phạm-vi-ghi-và-điểm-cưỡng-chế) · `D11` |
| **`API-TE-6`** | ⛔ **`beat_no` ⛔ không tham gia khoá sắp xếp** — ⛔ không filter, ⛔ không `order_by`, ⛔ không index gợi ý điều ngược lại | `INV-5` · `D13` |
| **`API-TE-7`** | ⭐ **Tối đa MỘT timeline `kind='main'` mỗi project**; nhánh khác **bắt buộc** có `anchor_order` | `409 TIMELINE_MAIN_EXISTS` · `422 ANCHOR_ORDER_RULE_VIOLATED`; `INV-2` |
| **`API-TE-8`** | ⛔ **⛔ Không endpoint TẠO/XOÁ `story.event` thủ công ở lô này** | Event sinh ở chặng 8 của `F1` ([`Endpoint-Chapter-Ingest.md`](./Endpoint-Chapter-Ingest.md)); ⛔ không event mồ côi (`EXC-3`). Xem [`TBD-API-TE-2`](#tbd-còn-lại---không-được-bịa) |
| **`API-TE-9`** | Event và `chapter`/`timeline` của nó **luôn cùng `project`** và cùng `tenant` | `422 TIMELINE_PROJECT_MISMATCH`; nền là composite FK `(tenant_id, …, project_id)` (`INV-3`), ⛔ không phải validation tầng ứng dụng đơn thuần |
| **`API-TE-10`** | ⛔ **⛔ Không endpoint nào gọi copyright / plagiarism / similarity detection** | `SRS-NFR-15` — xem [khối anti-feature](./Endpoint-Project.md#-anti-feature-srs-nfr-15--đọc-trước-khi-đề-xuất-tính-năng-mới) |

---

## UC nào tiêu thụ

| UC | Bước | Endpoint | Ghi chú ràng buộc |
|---|---|---|---|
| [UC-01](../../020-Requirements/Use-Cases/UC-01-Upload-And-Ingest-Chapter.md) | bước 2 — tác giả khai `timeline_id` | `TE-1` (chọn), `TE-2` (tạo nhánh mới) | ⛔ Chạy **trước** `CH-1` của [`Endpoint-Chapter-Ingest.md`](./Endpoint-Chapter-Ingest.md) |
| [UC-01](../../020-Requirements/Use-Cases/UC-01-Upload-And-Ingest-Chapter.md) | bước 8 — tách `Event` mức scene, đọc lại kết quả | `TE-3` | Event **được ghi** ở `CH-1`, ⛔ không ở đây |
| [UC-01](../../020-Requirements/Use-Cases/UC-01-Upload-And-Ingest-Chapter.md) | `ALT-4` — chapter là hồi tưởng thuộc nhánh khác | `TE-2` (`kind='flashback'` + `anchor_order`) | ⭐ Trường hợp `(chapter, scene)` **sai âm thầm** |
| [UC-02](../../020-Requirements/Use-Cases/UC-02-Review-And-Edit-Story-Bible.md) | bước 8 — duyệt state theo event | `TE-3` + `SB-6` của [`Endpoint-Story-Bible.md`](./Endpoint-Story-Bible.md) | `TE-3` cấp danh sách `event_id` để truyền vào `at_event` |
| [UC-02](../../020-Requirements/Use-Cases/UC-02-Review-And-Edit-Story-Bible.md) | `EXC-5` — sửa `story_order` của event đã có panel tham chiếu | ⭐ `TE-4` | ⭐ `API-TE-4` — cảnh báo bắt buộc |
| [UC-03](../../020-Requirements/Use-Cases/UC-03-Review-Panel-Script.md) | bước 2 — Director đọc `Event` | `TE-3` (đường client) · seam `comic → story` dùng `SB-6` | ⛔ `comic` ⛔ không truy vấn thẳng bảng `story` (`B-1`) |

---

## `TBD` còn lại — ⛔ không được bịa

| Khoảng trống | Ai đóng | Khi nào |
|---|---|---|
| **`TBD-API-TE-1`** — cách lấy `affected_panel_ids` mà ⛔ không vi phạm `B-1`: một hàm service ở hướng `comic → story`, hay một sự kiện nội bộ. ⛔ **Không nguồn nào** pin hình dạng này | **Architect**, lô Spec chi tiết `M2`/`M3` | Trước implementation `TE-4` |
| **`TBD-API-TE-2`** — có cần endpoint **tạo/xoá event thủ công** không (tác giả muốn chèn một scene ⛔ không có trong văn bản). ⛔ Repo im lặng; ⛔ không tự mở đường vì `EXC-3` cấm event mồ côi | **BA + PM** | Trước lô API kế tiếp |
| **Ngữ nghĩa nghiệp vụ của `beat_no`** (kế thừa `TBD` của lô Schema) — lô này chỉ đóng phần **API** (`API-TE-6`) | **BA + Architect** | Trước khi Director tiêu thụ `beat_no` |
| Ngữ nghĩa `reading_order` khi hai chapter thuộc **hai `timeline` khác nhau** cùng nằm trong một mạch đọc tuyến tính ⇒ ảnh hưởng `order_by=reading_order` của `TE-3` | **BA** | Trước `Story-Chapter-Ingest-And-Text-Clean` vào Active Sprint |

---

## Tài liệu tham khảo

- [Endpoint-Project.md](./Endpoint-Project.md) — `API-ENV-1`, `API-PRJ-4`, anti-feature `SRS-NFR-15`
- [Endpoint-Chapter-Ingest.md](./Endpoint-Chapter-Ingest.md) · [Endpoint-Story-Bible.md](./Endpoint-Story-Bible.md)
- [ADR-011 — Narrative Time Key And State Reduction](../Architecture/ADR-011-Narrative-Time-Key-And-State-Reduction.md) · [ADR-017](../Architecture/ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md) · [ADR-006](../Architecture/ADR-006-RLS-Tenant-Context-Injection.md) · [ADR-009](../Architecture/ADR-009-Modular-Monolith-Three-Schemas.md)
- [SDD Comic Studio](../Architecture/SDD-Comic-Studio.md) — §4.1 `B-1`, §5.1 `F1`/`F2`, §6.1
- [DB-Entity-Narrative-Timeline.md](../Schema/DB-Entity-Narrative-Timeline.md) · [DB-Entity-Story-Bible.md](../Schema/DB-Entity-Story-Bible.md)
- [UC-01](../../020-Requirements/Use-Cases/UC-01-Upload-And-Ingest-Chapter.md) · [UC-02](../../020-Requirements/Use-Cases/UC-02-Review-And-Edit-Story-Bible.md) · [UC-03](../../020-Requirements/Use-Cases/UC-03-Review-Panel-Script.md)
- [Story-Timeline-State-Resolver](../../022-User-Stories/Backlog/Story-Timeline-State-Resolver.md) · [Story-Chapter-Ingest-And-Text-Clean](../../022-User-Stories/Backlog/Story-Chapter-Ingest-And-Text-Clean.md)
- [SRS Comic Studio](../../020-Requirements/SRS-Comic-Studio.md) — `SRS-FR-04`, `SRS-FR-05`, `SRS-FR-35`, `SRS-NFR-01`, `SRS-NFR-10`, `SRS-NFR-15`
