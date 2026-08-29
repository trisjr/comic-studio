---
id: SPEC-API-STORY-BIBLE
type: spec
status: draft
project: comic-studio
created: 2026-08-29
---

# Endpoint: Story Bible

Story Bible là **cơ sở dữ liệu trạng thái có cấu trúc, truy vấn được theo thời điểm** — ⛔ không phải một bản tóm tắt văn xuôi. Resource này mang **ranh giới quyền lực** của toàn hệ thống: *"LLM chỉ phát event, **code sở hữu state**"*.

Bảng nguồn: [`story.bible_entity`](../Schema/DB-Entity-Story-Bible.md) · [`story.entity_attribute_event`](../Schema/DB-Entity-Story-Bible.md) · [`story.canonical_reference`](../Schema/DB-Entity-Story-Bible.md), đọc cùng [`story.event`](../Schema/DB-Entity-Narrative-Timeline.md).

> [!IMPORTANT]
> ⭐ **`SB-5` (`getBible`) và `SB-6` (`resolveState`) là API DUY NHẤT mà module `comic` được phép dùng để đọc dữ liệu của module `story`.**
> Ranh giới `B-1` ([SDD §4.1](../Architecture/SDD-Comic-Studio.md), [ADR-009](../Architecture/ADR-009-Modular-Monolith-Three-Schemas.md)) cấm `comic` **truy vấn** bảng schema `story`, và cấm này được **lint rule ở CI** cưỡng chế.
> ⚠️ Phân biệt hai mặt của cùng một seam: trong monolith, `comic` gọi **hàm service** `getBible()` / `resolveState()`; hai endpoint HTTP dưới đây là **cùng contract đó phơi ra cho client**, và cả hai đường **ủy quyền xuống ĐÚNG MỘT implementation**. ⛔ Một bản sao thứ hai của `resolveState()` — kể cả *"chỉ cho API"* — là vi phạm `D8`.

**Decided in:** [ADR-011](../Architecture/ADR-011-Narrative-Time-Key-And-State-Reduction.md) `D6`–`D13` · [ADR-009](../Architecture/ADR-009-Modular-Monolith-Three-Schemas.md) `B-1` · [ADR-017 `Q2`/`Q3`](../Architecture/ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md) · [ADR-006 `D3`](../Architecture/ADR-006-RLS-Tenant-Context-Injection.md) · [SDD §5.1 `F2`](../Architecture/SDD-Comic-Studio.md)

⭐ **Bốn ràng buộc xuyên-endpoint** (`SDD-HG-01` · `ADR-015` · `ADR-017` · `ADR-006`) và **quy ước chung `API-ENV-1`**: xem [`Endpoint-Project.md`](./Endpoint-Project.md). ⛔ File này **không lặp lại**.

---

## Hai trục — đọc trước bảng endpoint

| Trục | Sống ở đâu | Ghi bằng endpoint nào |
|---|---|---|
| ⭐ **Identity** — bất biến qua các chương (cấu trúc khuôn mặt, dấu hiệu nhận dạng) | `story.bible_entity.identity_facets` | `SB-2`, `SB-3` |
| ⭐ **Appearance** — thay đổi theo trạng thái (trang phục, vết thương, tóc) | `story.entity_attribute_event`, **neo vào một `event`** | `SB-8` |

⛔ **Gộp hai trục vào một field là *"nguyên nhân của phần lớn lỗi consistency"*** (`D12`). ⇒ ⛔ **Không endpoint nào của file này nhận một field mô tả tự do gộp cả hai.**

---

## Danh sách endpoint

### `SB-1` · `GET /v1/projects/{project_id}/bible-entities` — liệt kê entity

| Mục | Nội dung |
|---|---|
| **Method · Path** | `GET /v1/projects/{project_id}/bible-entities` |
| **Auth** | Bearer. Kiểm `access_state` (`API-PRJ-4` của [`Endpoint-Project.md`](./Endpoint-Project.md)) |
| **Request** | Query: `kind` (`character`\|`location`\|`costume`\|`prop`) · `needs_manual_confirmation` (`boolean`) · `q` (full-text) · `limit` · `cursor` |
| **Response `200`** | `{"items": [{"id","kind","name","aliases","identity_facets","needs_manual_confirmation","updated_at"}], "next_cursor"}` |
| **Mã lỗi** | `400 VALIDATION_FAILED` · `401` · `403 PROJECT_ACCESS_DISABLED` · `404 NOT_FOUND` |

⭐ `q` chạy bằng **full-text search của PostgreSQL** — *"Story Bible **là** index của mình"*. ⛔ **Không index vector nào trong MVP**; thêm một tham số `semantic=true` là mở một hạng mục hạ tầng mà ⛔ không nguồn nào cho phép.
⭐ `needs_manual_confirmation=true` phục vụ màn hình *"cần xác nhận thủ công"* — ⭐ đây là **cách trùng tên được xử lý**, ⛔ **không** bằng constraint: hai entity trùng tên khác hoa/thường **vẫn cùng tồn tại và truy vấn được**, hệ thống ⛔ **không tự merge âm thầm**.

### `SB-2` · `POST /v1/projects/{project_id}/bible-entities` — tạo entity (người khai)

| Mục | Nội dung |
|---|---|
| **Method · Path** | `POST /v1/projects/{project_id}/bible-entities` |
| **Auth** | Bearer. ⭐ Định danh người dùng thật |
| **Request** | `{"kind", "name", "aliases"?: [], "identity_facets"?: {}}` |
| **Response `201`** | Entity vừa tạo + `{"change_log_id"}` |
| **Mã lỗi** | `400 VALIDATION_FAILED` · `400 UNKNOWN_FIELD` · `401` · `403 PROJECT_ACCESS_DISABLED` · `404 NOT_FOUND` · `422 UNPROCESSABLE` (`kind` ngoài bốn giá trị) |

- ⭐ **Một transaction**: `INSERT story.bible_entity` + `INSERT public.field_provenance` (`origin='human'` ở **mức field**, [ADR-017 `Q3`](../Architecture/ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md#q3-field_provenance--origin-kc-3--mức-field-không-phải-mức-row)) + `INSERT public.change_log` — [`Q4.1`](../Architecture/ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md#q41-phát-biểu-chuẩn-normative), `Q4.3` `P-1`.
- ⛔ **Body ⛔ không nhận `origin`.** ⛔ Không tồn tại cột `origin` trên `bible_entity` — nó sống ở `public.field_provenance`; nhận nó từ client là tạo **nguồn sự thật thứ hai**.
- ⭐ **`ALT-2`**: entity do người khai **⛔ không được extraction ghi đè** ở lần chạy sau. Trật tự này chính là thứ làm ranh giới *"phần nào do người, phần nào do AI"* xác định được (`KC-3`).
- ⛔ **Không trả `409` khi trùng tên** — ⛔ không có UNIQUE trên `lower(name)`, và ⛔ **không được thêm**.

### `SB-3` · `PATCH /v1/bible-entities/{entity_id}` — sửa entity

| Mục | Nội dung |
|---|---|
| **Method · Path** | `PATCH /v1/bible-entities/{entity_id}` |
| **Auth** | Bearer. ⭐ Định danh người dùng thật |
| **Request** | `{"name"?, "aliases"?, "identity_facets"?, "needs_manual_confirmation"?}` — ít nhất một field |
| **Response `200`** | Entity sau khi sửa + `{"change_log_id"}` |
| **Mã lỗi** | `400 VALIDATION_FAILED` · `400 UNKNOWN_FIELD` · `401` · `403 PROJECT_ACCESS_DISABLED` · `404 NOT_FOUND` · `409 STALE_WRITE` (khi gửi `If-Match` lệch) · `422 IDENTITY_FACET_IS_APPEARANCE` |

- Mỗi field bị sửa ⇒ **một** dòng `public.field_provenance` (`origin='human'`) + **một** `public.change_log`, commit **cùng transaction** với chính field đó. ⛔ Ghi `change_log` thất bại ⇒ **toàn bộ rollback**, field ⛔ không được sửa (`EXC-6`).
- ⭐ `422 IDENTITY_FACET_IS_APPEARANCE`: `identity_facets` ⛔ **không** chứa trang phục / vết thương / tóc — những thứ đó là **Appearance** và phải đi qua `SB-8`. ⚠️ **Cưỡng chế tự động = `TBD`** (cần một danh mục key; ⛔ không bịa ở lô này) — xem [`TBD-API-SB-2`](#tbd-còn-lại---không-được-bịa). Cho tới khi có danh mục, ràng buộc này là **hợp đồng có ghi**, ⛔ không phải một validator im lặng.

### `SB-4` · `DELETE /v1/bible-entities/{entity_id}` — xoá entity giả

| Mục | Nội dung |
|---|---|
| **Method · Path** | `DELETE /v1/bible-entities/{entity_id}` |
| **Auth** | Bearer. ⭐ Định danh người dùng thật |
| **Request** | ⛔ Không body |
| **Response `200`** | `{"deleted": true, "attribute_event_deleted_count", "change_log_id"}` |
| **Mã lỗi** | `401` · `403 PROJECT_ACCESS_DISABLED` · `404 NOT_FOUND` · **`409 ENTITY_REFERENCED_BY_COMIC`** |

- ⭐ Phục vụ `UC-02` `EXC-2` — xoá entity rác do `text clean` sót (*"Chương 12"*, tên người dịch, tên nền tảng đọc truyện).
- ⭐ **`409 ENTITY_REFERENCED_BY_COMIC`**: entity đang được `comic.panel_character` hoặc `comic.dialogue_line.speaker_id` tham chiếu ⇒ **từ chối**. Căn cứ: `INV-5` của [`DB-Entity-Story-Bible.md`](../Schema/DB-Entity-Story-Bible.md) — FK chéo schema là **ràng buộc toàn vẹn**, và [ADR-012](../Architecture/ADR-012-Comic-IR-Spec-As-Primary-Data.md) hợp đồng #4 bắt spec tham chiếu `character_id` không tồn tại phải bị từ chối **tại thời điểm ghi**.
- ⚠️ **Nếu số entity giả lớn, đường xử lý ĐÚNG là quay lại [`Endpoint-Chapter-Ingest.md`](./Endpoint-Chapter-Ingest.md) sửa văn bản gốc**, ⛔ không phải xoá tay từng dòng — nguyên nhân gốc nằm ở `text clean` (`UC-02` `EXC-2`).
- ⚠️ **`TBD-API-SB-1`**: ngữ nghĩa xoá kèm `story.entity_attribute_event` (`ON DELETE CASCADE` hay `RESTRICT`) ⛔ **chưa được pin** ở lô Schema ⇒ ripple.

### `SB-5` · `GET /v1/projects/{project_id}/bible` — ⭐ `getBible()` · seam `comic → story` #1

| Mục | Nội dung |
|---|---|
| **Method · Path** | `GET /v1/projects/{project_id}/bible` |
| **Auth** | Bearer. Kiểm `access_state` (`API-PRJ-4`) |
| **Request** | Query: `kind`? (lọc) · `include_references` (`boolean`, mặc định `true`) |
| **Response `200`** | `{"project_id", "entities": [{…, "canonical_references": [{"id","object_key","is_primary","mime_type"}]}], "generated_at"}` |
| **Mã lỗi** | `400 VALIDATION_FAILED` · `401` · `403 PROJECT_ACCESS_DISABLED` · `404 NOT_FOUND` |

- ⭐ Trả **ảnh chụp Identity + canonical reference** của cả project — đủ để dựng `conditioning_set` khi sinh ảnh.
- ⛔ **Response ⛔ không chứa state theo thời điểm.** State chỉ đến từ `SB-6`. Nhét một `current_state` vào đây là dựng lại đúng cái *"bảng state"* mà `D6`/`INV-1` cấm — chỉ khác là nó nằm trong JSON thay vì trong Postgres.
- ⛔ **⛔ Không trả URL ảnh trực tiếp** — `object_key` được đổi thành signed URL ở resource riêng ([ADR-004](../Architecture/ADR-004-Object-Storage-Vendor-And-Signed-URL.md)); ⛔ không bucket public.

### `SB-6` · `GET /v1/bible-entities/{entity_id}/state` — ⭐ `resolveState()` · seam `comic → story` #2

| Mục | Nội dung |
|---|---|
| **Method · Path** | `GET /v1/bible-entities/{entity_id}/state?at_event={…}&timeline_id={…}` |
| **Auth** | Bearer. Kiểm `access_state` (`API-PRJ-4`) |
| **Request** | ⭐ `at_event` **bắt buộc** — hoặc một `event_id` (`UUID`), hoặc một giá trị `story_order` (`NUMERIC`). ⭐ `timeline_id` **bắt buộc** khi `at_event` là `story_order` |
| **Response `200`** | `{"entity_id","timeline_id","at_story_order","state": {…},"resolved_from_event_count","conflicts": [...]}` |
| **Mã lỗi** | **`400 AT_EVENT_REQUIRED`** · **`400 TIMELINE_ID_REQUIRED`** · `401` · `403 PROJECT_ACCESS_DISABLED` · `404 NOT_FOUND` |

> [!IMPORTANT]
> ⭐ **`at_event` ⛔ KHÔNG có giá trị mặc định — ⛔ không "hiện tại", ⛔ không "event mới nhất".**
> Một mặc định ẩn biến mọi truy vấn hồi tưởng thành *"state của hiện tại"* — lỗi **không crash, chỉ corrupt dữ liệu**, đúng `R-15`. `400 AT_EVENT_REQUIRED` là **cưỡng chế**, ⛔ không phải sự bất tiện.

- **Ngữ nghĩa**: `state_at(N) = reduce(events where story_order <= N)` trong phạm vi **một** `timeline_id`. ⭐ **Tất định** (`D6`): gọi lại hai lần với cùng `N` cho **hai output giống hệt nhau**.
- ⛔ **Hai event cùng `story_order`, khác `timeline_id` là hai chuỗi ĐỘC LẬP** — ⛔ `state_at` ⛔ không gộp (`INV-6`). Đó là lý do `timeline_id` bắt buộc.
- ⛔ **⛔ Không `ORDER BY chapter_no`** ở bất kỳ đường resolve nào — guardrail `D-17`, kiểm bằng lint rule ở CI.
- ⭐ **`conflicts` ≠ rỗng ⇒ resolver ⛔ KHÔNG đoán** (`UC-02` `EXC-4`). Endpoint vẫn trả `200`, field bị tranh chấp được đánh dấu `unresolved` kèm cả hai ứng viên; **UI buộc tác giả chọn**, và lựa chọn đó ghi qua `SB-8` + sinh `change_log` — *"chọn A thay vì B"* chính là dạng bằng chứng `KC-2` yêu cầu.
  ⚠️ ⛔ **Không trả `409` ở đây**: `409` biến một tình huống dữ liệu bình thường thành lỗi và **chặn** cả những field ⛔ không tranh chấp.
- ⛔ **⛔ Không có endpoint ghi state.** State được **tính**, ⛔ không lưu (`INV-1`, `INV-8`). ⛔ ⛔ Không tồn tại `PUT /state`, ⛔ không cache, ⛔ không snapshot.

### `SB-7` · `POST /v1/chapters/{chapter_id}/bible:approve` — đánh dấu bible đã duyệt

| Mục | Nội dung |
|---|---|
| **Method · Path** | `POST /v1/chapters/{chapter_id}/bible:approve` |
| **Auth** | Bearer. ⭐ Định danh người dùng thật |
| **Header** | `Idempotency-Key` bắt buộc |
| **Request** | `{}` — ⛔ không tham số |
| **Response `200`** | `{"chapter_id","bible_approved": true,"approved_at","change_log_id"}` |
| **Mã lỗi** | `401` · `403 PROJECT_ACCESS_DISABLED` · `404 NOT_FOUND` · `409 INGEST_NOT_APPROVED` · `409 CHAPTER_SUPERSEDED` |

- ⭐ `UC-02` bước 12 — chapter sẵn sàng cho `UC-03`. Trạng thái + `change_log` **cùng transaction**.
- ⛔ **Không có `auto_approve`, ⛔ không batch-approve.** Đây là hành động con người; và nó là **tiền đề của `F3`** (*"Bible đã duyệt → Director"* — [SDD §5.1](../Architecture/SDD-Comic-Studio.md)).
- ⚠️ ⛔ **Đây ⛔ KHÔNG phải một trong hai human gate.** Hai gate của `SDD-HG-01` là **speaker attribution** và **dialogue condensation**, ở mức `dialogue_line`. ⛔ Gọi bước này là *"gate"* làm loãng đúng thuật ngữ mà `SDD-HG-01` cần giữ chặt.
- ⚠️ **`TBD-API-SB-3`** — cột lưu trạng thái này ⛔ chưa tồn tại ở lô Schema (cùng dạng khoảng trống với `TBD-API-CH-1` của [`Endpoint-Chapter-Ingest.md`](./Endpoint-Chapter-Ingest.md)) ⇒ ripple.

### `SB-8` · `POST /v1/bible-entities/{entity_id}/attribute-events` — ghi event trục Appearance ⭐ `[+1 so với findings §4.1]`

> ⚠️ **Ghi chú độ hạt**: [findings §4.1](../../010-Planning/pm-runs/2026-08-28-phase-2-architecture-design-comic-studio/findings/architect.md) ước lượng **7** endpoint cho resource này và ⛔ **không liệt kê** đường ghi `story.entity_attribute_event`. Nhưng `UC-02` bước 7–8 (*"khai trang phục thuộc trục Appearance và **neo vào event nào**"*, *"duyệt state theo event"*) và `EXC-4` (*"buộc tác giả chọn"*) ⛔ **không thực hiện được** nếu thiếu nó. ⇒ Lô này thêm **đúng một** endpoint và **khai báo tường minh** thay vì để `UC-02` khuyết. Con số findings là **`[EM]` ở mức resource**, ⛔ không phải contract đã chốt.

| Mục | Nội dung |
|---|---|
| **Method · Path** | `POST /v1/bible-entities/{entity_id}/attribute-events` |
| **Auth** | Bearer. ⭐ Định danh người dùng thật |
| **Request** | `{"event_id", "attribute", "value", "permanence", "evidence_span"?: {"chapter_id","start","end"}, "confidence"}` |
| **Response `201`** | Event vừa ghi + `{"change_log_id"}` |
| **Mã lỗi** | `400 VALIDATION_FAILED` · `400 UNKNOWN_FIELD` · `401` · `403 PROJECT_ACCESS_DISABLED` · `404 NOT_FOUND` (entity/event) · **`422 EVENT_ID_REQUIRED`** · `422 CONFIDENCE_OUT_OF_RANGE` |

- ⭐ **`event_id` là `NOT NULL`** (`INV-3`): thuộc tính **Appearance phải khai nó neo vào event nào**. Thuộc tính **Identity** thì ⛔ **không** neo — nó đi qua `SB-3`.
- ⛔ **Body ⛔ không nhận `story_order` hay `timeline_id`** — `INV-2` cấm denormalize hai trục xuống bảng này. `story_order` **editable qua UI** (`SB-6`/[`Endpoint-Timeline-Event.md`](./Endpoint-Timeline-Event.md)) ⇒ một bản sao ở đây lệch ngay lần biên tập đầu tiên.
- `confidence ∈ [0,1]` (`INV-4`). `evidence_span` là offset **nửa mở** trên `story.chapter.clean_text` (`INV-6`) — đó là lý do `clean_text` bất biến trên thực tế.
- ⚠️ Tập giá trị hợp lệ của `permanence` = **`TBD`** ở lô Schema ⇒ lô này ⛔ **không** liệt kê giá trị và ⛔ **không** validate danh mục.

---

## Invariant của resource

| Mã | Invariant | Cưỡng chế bằng |
|:--:|---|---|
| **`API-SB-1`** | ⭐ **`SB-5` + `SB-6` là API DUY NHẤT `comic` đọc `story`**; cả hai ủy quyền xuống **đúng một** implementation `getBible()`/`resolveState()` | `B-1` + **lint rule ở CI**; test: `grep` toàn repo cho `resolveState` ⇒ đúng **một** định nghĩa |
| **`API-SB-2`** | ⭐ **⛔ Không endpoint nào ghi state.** State được **tính**, ⛔ không lưu | `INV-1`/`INV-8` — vắng mặt bảng state là **thuộc tính cấu trúc**, ⛔ không phải một `GRANT` phải nhớ |
| **`API-SB-3`** | ⭐ `at_event` **bắt buộc**, ⛔ không mặc định; `timeline_id` bắt buộc khi `at_event` là `story_order` | `400 AT_EVENT_REQUIRED` / `400 TIMELINE_ID_REQUIRED`; `D6`, `INV-6` |
| **`API-SB-4`** | ⭐ `resolveState` **tất định**: cùng `(entity, timeline_id, at_event)` ⇒ **byte-identical** response (bỏ qua `generated_at`) | Test CI gọi hai lần và so sánh; `INV-4` `(tenant_id, timeline_id, story_order)` UNIQUE là điều kiện nền |
| **`API-SB-5`** | ⭐ **⛔ Resolver ⛔ không phân xử xung đột** — trả `conflicts[]` và **buộc người chọn** | `EXC-4`; ⛔ ⛔ không tham số `auto_resolve`, ⛔ không heuristic *"lấy confidence cao hơn"* |
| **`API-SB-6`** | Mỗi hành động sửa của con người ⇒ **1** `public.change_log` + `public.field_provenance` mức field, commit **cùng transaction** với field | [ADR-017 `Q2`](../Architecture/ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md#q2-change_log-kc-2--phạm-vi-ghi-và-điểm-cưỡng-chế) + `Q4.3` `P-1`; `INV-10` |
| **`API-SB-7`** | Extraction ⛔ **không ghi đè** field do người khai | `origin` mức field (`ADR-017 Q3`) + `ALT-2` |
| **`API-SB-8`** | Hai trục Identity/Appearance ⛔ không gộp ở bất kỳ request/response nào | `D12`; `SB-3` vs `SB-8` là hai đường ghi tách biệt — ⚠️ cưỡng chế tự động cho `identity_facets` = `TBD` |
| **`API-SB-9`** | ⛔ **Trùng tên ⛔ không bị từ chối và ⛔ không tự merge** | ⛔ Không UNIQUE trên `lower(name)`; xử lý bằng `needs_manual_confirmation` + `UC-02` |
| **`API-SB-10`** | ⛔ **⛔ Không endpoint nào gọi copyright / plagiarism / similarity detection** | `SRS-NFR-15` — xem [khối anti-feature](./Endpoint-Project.md#-anti-feature-srs-nfr-15--đọc-trước-khi-đề-xuất-tính-năng-mới) |

---

## UC nào tiêu thụ

| UC | Bước | Endpoint | Ghi chú ràng buộc |
|---|---|---|---|
| [UC-02](../../020-Requirements/Use-Cases/UC-02-Review-And-Edit-Story-Bible.md) | bước 5 — mở Story Bible editor (form + list, ⛔ không canvas/graph) | `SB-1`, `SB-5` | |
| [UC-02](../../020-Requirements/Use-Cases/UC-02-Review-And-Edit-Story-Bible.md) | bước 6 — duyệt nhân vật: xác nhận / sửa / **xoá entity giả** / thêm nhân vật sót | `SB-2`, `SB-3`, `SB-4` | `EXC-2` |
| [UC-02](../../020-Requirements/Use-Cases/UC-02-Review-And-Edit-Story-Bible.md) | bước 7 — duyệt trang phục/địa điểm, khai trục Appearance **neo vào event** | `SB-8` | `INV-3` |
| [UC-02](../../020-Requirements/Use-Cases/UC-02-Review-And-Edit-Story-Bible.md) | bước 8 — duyệt state theo event | `SB-6`, `SB-8` | |
| [UC-02](../../020-Requirements/Use-Cases/UC-02-Review-And-Edit-Story-Bible.md) | bước 9 — mỗi hành động sửa ⇒ `change_log` + `field_provenance` cùng transaction | `SB-2`…`SB-4`, `SB-8` | `API-SB-6` · `EXC-6` |
| [UC-02](../../020-Requirements/Use-Cases/UC-02-Review-And-Edit-Story-Bible.md) | bước 10–11 — `state_at(N)`, *"tại chương 40 nhân vật X mặc gì"* | `SB-6` | ⭐ Câu truy vấn nghiệm thu của cả module |
| [UC-02](../../020-Requirements/Use-Cases/UC-02-Review-And-Edit-Story-Bible.md) | bước 12 — đánh dấu bible đã duyệt | `SB-7` | ⚠️ `TBD-API-SB-3` |
| [UC-02](../../020-Requirements/Use-Cases/UC-02-Review-And-Edit-Story-Bible.md) | `ALT-3` hồi tưởng · `ALT-4` chỉ tra không sửa · `EXC-4` xung đột | `SB-6` (`timeline_id`), `SB-1` (`q`) | `ALT-4` ⛔ không sinh `change_log` |
| [UC-03](../../020-Requirements/Use-Cases/UC-03-Review-Panel-Script.md) | bước 2 — Director đọc `Event` + gọi `resolveState()` | ⭐ `SB-5`, `SB-6` **và chỉ hai cái này** | `B-1` · `D-04` |
| [UC-06](../../020-Requirements/Use-Cases/UC-06-Generate-Panel-And-Pick-Variant.md) | bước 2 — compile prompt, dựng `conditioning_set` | `SB-5` (`canonical_references`) | ⛔ Không đường nào khác đọc bảng `story` |

---

## `TBD` còn lại — ⛔ không được bịa

| Khoảng trống | Ai đóng | Khi nào |
|---|---|---|
| **`TBD-API-SB-1`** — ngữ nghĩa `ON DELETE` của `entity_attribute_event` khi xoá entity (`CASCADE` vs `RESTRICT`) ⛔ chưa pin ở lô Schema | **Architect**, ripple sang lô Schema | Trước implementation `SB-4` |
| **`TBD-API-SB-2`** — danh mục key hợp lệ của `identity_facets` để cưỡng chế `422 IDENTITY_FACET_IS_APPEARANCE` bằng máy | **BA + Architect** | Trước `Story-Story-Bible-Extraction` vào Active Sprint |
| **`TBD-API-SB-3`** — cột lưu *"bible của chapter đã duyệt"* ⛔ chưa tồn tại | **Architect**, ripple sang lô Schema | Cùng lúc với `TBD-API-CH-1` |
| Tập giá trị `permanence` (kế thừa `TBD` của lô Schema) ⇒ `SB-8` ⛔ chưa validate danh mục | **BA + Architect** | Trước `Story-Story-Bible-Extraction` vào Active Sprint |
| Quy tắc `reduce` khi **hai attribute event khác nhau neo vào CÙNG một event** cho cùng `attribute` — quyết định hình dạng `conflicts[]` của `SB-6` | **Architect + BA**, khi đặc tả `resolveState()` | Trước `Story-Timeline-State-Resolver` vào Active Sprint |
| Endpoint **kích hoạt/retry extraction** (`UC-02` bước 1, `EXC-1`) — ⛔ không thuộc resource nào của findings §4.1 | **Architect + PM** — cùng hàng với `TBD-API-CH-3` | Trước lô API kế tiếp |

---

## Tài liệu tham khảo

- [Endpoint-Project.md](./Endpoint-Project.md) — `API-ENV-1`, `API-PRJ-4`, anti-feature `SRS-NFR-15`
- [Endpoint-Timeline-Event.md](./Endpoint-Timeline-Event.md) · [Endpoint-Chapter-Ingest.md](./Endpoint-Chapter-Ingest.md)
- [ADR-011 — Narrative Time Key And State Reduction](../Architecture/ADR-011-Narrative-Time-Key-And-State-Reduction.md) · [ADR-009 — Modular Monolith Three Schemas](../Architecture/ADR-009-Modular-Monolith-Three-Schemas.md) · [ADR-012 — Comic IR Spec As Primary Data](../Architecture/ADR-012-Comic-IR-Spec-As-Primary-Data.md) · [ADR-017](../Architecture/ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md) · [ADR-006](../Architecture/ADR-006-RLS-Tenant-Context-Injection.md) · [ADR-004](../Architecture/ADR-004-Object-Storage-Vendor-And-Signed-URL.md)
- [SDD Comic Studio](../Architecture/SDD-Comic-Studio.md) — §4.1 `B-1`, §5.1 `F2`/`F3`, §6.1
- [DB-Entity-Story-Bible.md](../Schema/DB-Entity-Story-Bible.md) · [DB-Entity-Narrative-Timeline.md](../Schema/DB-Entity-Narrative-Timeline.md)
- [UC-02 — Review And Edit Story Bible](../../020-Requirements/Use-Cases/UC-02-Review-And-Edit-Story-Bible.md) · [UC-03](../../020-Requirements/Use-Cases/UC-03-Review-Panel-Script.md)
- [Story-Story-Bible-Extraction](../../022-User-Stories/Backlog/Story-Story-Bible-Extraction.md) · [Story-Timeline-State-Resolver](../../022-User-Stories/Backlog/Story-Timeline-State-Resolver.md) · [Story-Story-Bible-Editor-Form](../../022-User-Stories/Backlog/Story-Story-Bible-Editor-Form.md)
- [SRS Comic Studio](../../020-Requirements/SRS-Comic-Studio.md) — `SRS-FR-04`, `SRS-FR-05`, `SRS-FR-35`, `SRS-NFR-01`, `SRS-NFR-10`, `SRS-NFR-13`, `SRS-NFR-15`
