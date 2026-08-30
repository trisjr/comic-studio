---
id: SPEC-API-PANEL-SCRIPT
type: spec
status: draft
project: comic-studio
created: 2026-08-29
---

# Endpoint: Panel Script (Comic IR)

Bề mặt API của **Panel Specification** — bản ghi dữ liệu chính của tầng `comic`. Đây là nơi *"spec là dữ liệu chính, ảnh chỉ là output"* trở thành một contract gọi được: mọi endpoint ở đây ghi/đọc **spec**, ⛔ không endpoint nào ở đây chạm tới ảnh.

**Decided in:**

- [ADR-012 — Comic IR: spec là dữ liệu chính](../Architecture/ADR-012-Comic-IR-Spec-As-Primary-Data.md) — `## Decision` điều 1–3, 6–9 (`D-20`, `D-21`, `D-23`, `D-25`)
- [ADR-017 — Chuỗi provenance và MỘT transaction boundary](../Architecture/ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md) — `Q2`, `Q4.3` `P-2` (hợp đồng trích dẫn cho file `Endpoint-*` ở `Q4.7`)
- [ADR-006 — RLS & tenant context injection](../Architecture/ADR-006-RLS-Tenant-Context-Injection.md) — đường API chạy dưới role `app_api`
- [SDD Comic Studio](../Architecture/SDD-Comic-Studio.md) — §5.1 `F3`, §6.3 `SDD-HG-01`
- [`DB-Entity-Comic-IR.md`](../Schema/DB-Entity-Comic-IR.md) — nguồn chuẩn của tên bảng/cột, `INV-1`…`INV-12`
- [`DB-Entity-Dialogue-And-Gate.md`](../Schema/DB-Entity-Dialogue-And-Gate.md) — trạng thái gate dẫn xuất
- [`DB-Entity-Job-Queue.md`](../Schema/DB-Entity-Job-Queue.md) — danh mục `job_type` **đóng**
- [`DB-Entity-Provenance-And-Usage.md`](../Schema/DB-Entity-Provenance-And-Usage.md) — danh mục `action_type` **đóng**

---

## 1. Resource

| Resource | Bảng DB sở hữu | File schema |
|---|---|---|
| `page` | `comic.page` | [`DB-Entity-Comic-IR.md`](../Schema/DB-Entity-Comic-IR.md) |
| `panel` (Panel Specification) | `comic.panel` | [`DB-Entity-Comic-IR.md`](../Schema/DB-Entity-Comic-IR.md) |
| liên kết nhân vật của panel | `comic.panel_character` | [`DB-Entity-Comic-IR.md`](../Schema/DB-Entity-Comic-IR.md) |

⛔ **Ba thứ resource này KHÔNG sở hữu** — trỏ, ⛔ không đặc tả lại:

| Thứ | File sở hữu |
|---|---|
| Bố cục (`page.page_layout`), template, swap/reorder | [`Endpoint-Page-Layout.md`](./Endpoint-Page-Layout.md) |
| Thoại, speaker, hai human gate | [`Endpoint-Human-Gates.md`](./Endpoint-Human-Gates.md) |
| Ảnh, `approved_generation_id`, job | [`Endpoint-Generation.md`](./Endpoint-Generation.md) |

---

## 2. Quy ước chung — ⛔ file này KHÔNG đặc tả lại bốn ràng buộc xuyên-endpoint

| Mã | Ràng buộc | Nguồn **DUY NHẤT** | File này được làm gì |
|---|---|---|---|
| `SDD-HG-01` | Không đường nào bypass hai human gate | [SDD §6.3](../Architecture/SDD-Comic-Studio.md) | Chỉ **trỏ theo mã điều khoản** (`.2`, `.4`, `.5`) và hiện thực hoá 5 *"hệ quả bắt buộc cho 14 file API"* |
| `KC-4` | Artifact + bằng chứng commit **một** transaction | [ADR-017 `Q4`](../Architecture/ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md) | Trỏ `Q2` + `Q4.3` `P-2` theo đúng hàng `Endpoint-*` của [`Q4.7`](../Architecture/ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md). ⛔ **Không viết** *"tầng DB cưỡng chế `KC-4`"* (`Q4.6`) |
| `CT-POLL-2S` | Polling **2 giây** cho tác vụ async, ⛔ không WebSocket | [ADR-015 `Q6`](../Architecture/ADR-015-Job-Queue-In-Postgres.md) | ⚠️ **⛔ Không endpoint nào trong file này là tác vụ async** — xem `API-PS-6` |
| RLS + tenant context | Mọi query đi qua RLS với `app.current_tenant` | [ADR-006](../Architecture/ADR-006-RLS-Tenant-Context-Injection.md) | Cột `Auth` của bảng endpoint chỉ ghi *"tenant member"* — cơ chế bơm context ⛔ không lặp ở đây |

**Quy ước mã lỗi**: mỗi lỗi = `HTTP status` + `error_code` dạng `SCREAMING_SNAKE` **ổn định** (client bắt theo `error_code`, ⛔ không bắt theo message). ⚠️ Chuẩn đặt tên chung cho cả 14 file API **vẫn chưa chốt** — ⭐ theo dõi ở **một sổ duy nhất**: `TBD-API-ENV` của [`Endpoint-Project.md`](./Endpoint-Project.md), nơi bản nháp `API-ENV-1` đang sống. ⛔ Hàng `T-API-ERR` của file này ⛔ **không** còn theo dõi câu hỏi đó.

> [!CAUTION]
> ⛔ **`SRS-NFR-15` — ⛔ KHÔNG endpoint nào trong file này gọi copyright detection / similarity detection / chấm điểm nghi vấn bản quyền.** Đây là **anti-feature có chủ ý** ([SDD §5.4](../Architecture/SDD-Comic-Studio.md)), ⛔ không phải một tính năng bị hoãn. Thêm nó vào bất kỳ endpoint nào ở đây là **vi phạm ràng buộc pháp lý đã ký**.

---

## 3. Danh sách endpoint

| # | Method · Path | Auth | Request | Response | Mã lỗi |
|--:|---|---|---|---|---|
| 1 | `POST /v1/chapters/{chapter_id}/panel-script:generate` | tenant member | `{}` — ⛔ **không tham số nào** đổi ràng buộc | `201` `{page_ids[], panel_count, degraded_notes[]}` | `403 PROJECT_ACCESS_DISABLED` · `404 CHAPTER_NOT_FOUND` · `409 BIBLE_NOT_APPROVED` · `409 PANEL_SCRIPT_ALREADY_EXISTS` · `422 DIRECTOR_OUTPUT_INCOMPLETE` · `502 LLM_PROVIDER_ERROR` |
| 2 | `GET /v1/chapters/{chapter_id}/pages` | tenant member | query: `?page_no_from`, `?page_no_to` | `200` `{items[]: {id, page_no, panel_count, applied_template_key, gate_summary}}` | `403 PROJECT_ACCESS_DISABLED` · `404 CHAPTER_NOT_FOUND` |
| 3 | `GET /v1/panels/{panel_id}` | tenant member | — | `200` `PanelSpec` (xem [§4.3](#43-hình-dạng-panelspec)) | `403 PROJECT_ACCESS_DISABLED` · `404 PANEL_NOT_FOUND` |
| 4 | `PATCH /v1/panels/{panel_id}` | tenant member | `PanelSpecPatch` — xem [§4.4](#44-4-patch-panel--bảng-field-ghi-được) | `200` `{panel, gates_reset[]}` | `403 PROJECT_ACCESS_DISABLED` · `403 FIELD_NOT_WRITABLE` · `404 PANEL_NOT_FOUND` · `409 PANEL_CHARACTER_LIMIT_EXCEEDED` · `422 PANEL_REQUIRED_FIELD_MISSING` · `422 LAYOUT_COORDS_NOT_NORMALIZED` · `422 BIBLE_ENTITY_NOT_FOUND` |
| 5 | `POST /v1/panels/{panel_id}:split` | tenant member | `{}` | `200` `{page_layout, panels[], gates_reset[]}` | `403 PROJECT_ACCESS_DISABLED` · `404 PANEL_NOT_FOUND` · `409 PANEL_SPLIT_NOT_ALLOWED` · `422 PANEL_REQUIRED_FIELD_MISSING` |
| 6 | `POST /v1/pages/{page_id}/panels:merge` | tenant member | `{panel_ids: [uuid, …]}` (≥2, cùng `page_id`, liền kề theo `panel_index`) | `200` `{page_layout, panels[], gates_reset[]}` | `403 PROJECT_ACCESS_DISABLED` · `404 PAGE_NOT_FOUND` · `409 PANEL_MERGE_NOT_ADJACENT` · `409 PANEL_CHARACTER_LIMIT_EXCEEDED` |
| 7 | `POST /v1/chapters/{chapter_id}/panel-script:approve` | tenant member | `{}` | `200` `{chapter_id, approved_at, approved_by_user_id}` | `403 PROJECT_ACCESS_DISABLED` · `404 CHAPTER_NOT_FOUND` · `409 PANEL_SCRIPT_INCOMPLETE` — ⚠️ **blocked-by-TBD**, xem [`T-PS-APPROVE`](#7-tbd-còn-lại---không-được-bịa) |

> [!IMPORTANT]
> ⭐ **Cả bảy endpoint là "đường đọc/ghi NỘI DUNG trong phạm vi project"** ⇒ **đều** trả `403 PROJECT_ACCESS_DISABLED` khi project ở `disabled_by_takedown`. Chúng định danh bằng `chapter_id` / `page_id` / `panel_id` và ⛔ **không** mang `project_id` trên path ⇒ phải **resolve ngược lên project** rồi mới kiểm cờ (`C3-K1`).
> Luật ở [`API-PRJ-4`](./Endpoint-Project.md#invariant-của-resource) — ⛔ file này **không chép lại**, chỉ trỏ theo mã: đi qua **đúng một** hàm dùng chung ở tầng service (`C3-K3`), **fail-closed** khi ⛔ không thấy row `public.project_access_state` (`C3-K2`). Cưỡng chế bằng **test bảng route toàn cục** khuôn `M1-1`, ⛔ **không** test per-endpoint (`C3-K4`). Danh sách đóng: [Threat Model §4.4](../Security/Spec-Security-Threat-Model.md#44--c-3-danh-sách-đóng-các-đường-đọc-phải-kiểm-cờ-disable-access).
> ⚠️ `#4` mang **hai** mã khác nhau cùng status `403` — `PROJECT_ACCESS_DISABLED` (phạm vi project) và `FIELD_NOT_WRITABLE` (phạm vi field). ⛔ **Không gộp**: kiểm cờ chạy **trước**, ⛔ không phụ thuộc nội dung patch.

✅ ⭐ **Endpoint #4, #5, #6 ⛔ KHÔNG còn bị chặn** — `edit_panel_field`, `split_panel`, `merge_panel` đã có trong danh mục `action_type` (lô Schema **`L28b`**) ⇒ **`UC-03` bước 9 đi được**. ⚠️ Phần dư của `T-CL-PANEL-EDIT` **chỉ còn đúng hai field** (`text_safe_zone_warning`, `negative_space_hint`) của `#4` — đọc [§4.4](#44-4-patch-panel--bảng-field-ghi-được) trước khi hiện thực.

---

## 4. Chi tiết các endpoint có ràng buộc

### 4.1 `#1 panel-script:generate` — ⭐ ĐỒNG BỘ, ⛔ không đi qua hàng đợi

| Điều | Nội dung |
|---|---|
| ⭐ **Sự thật kiểm chứng được** | Danh mục `job_type` của `public.job` là **danh sách ĐÓNG** và ở MVP0–MVP2 có **đúng MỘT giá trị `generate_panel`** ([`DB-Entity-Job-Queue.md`](../Schema/DB-Entity-Job-Queue.md)). ⇒ ⛔ **Không tồn tại `job_type` nào để enqueue việc này.** |
| **Hệ quả contract** | Endpoint chạy **đồng bộ**: một request → một response mang kết quả. ⛔ **Không** trả `job_id`, ⛔ **không** áp `CT-POLL-2S` (⛔ không có job để poll) |
| ⛔ **Cấm** | ⛔ Thêm một giá trị `job_type` vì *"chắc là async"* — [`DB-Entity-Job-Queue.md`](../Schema/DB-Entity-Job-Queue.md) gọi đúng hành vi đó là **bịa**. Mở danh mục = sửa [ADR-015](../Architecture/ADR-015-Job-Queue-In-Postgres.md) trước |
| **Thứ tự bắt buộc** | Bible **đã duyệt** → Director ([SDD §5.1](../Architecture/SDD-Comic-Studio.md) `F3`) ⇒ `409 BIBLE_NOT_APPROVED` là điều kiện tiên quyết, ⛔ không phải cảnh báo |
| **Ranh giới module** | Endpoint đọc dữ liệu schema `story` **chỉ qua** `resolveState()` / `getBible()` (`B-1`, `D-04`) — hai hàm này thuộc [`Endpoint-Story-Bible.md`](./Endpoint-Story-Bible.md), ⛔ file này không đặc tả lại |
| **Phân bổ diện tích** | LLM **chỉ xếp hạng beat**; **code** phân bổ `emphasis` theo quota chapter ([ADR-012](../Architecture/ADR-012-Comic-IR-Spec-As-Primary-Data.md) điều 7). ⛔ Response ⛔ không được chứa một *"điểm số layout"* dưới bất kỳ tên nào (`INV-7`, `SRS-NFR-22`) |
| `409 PANEL_SCRIPT_ALREADY_EXISTS` | `[Kiến trúc suy luận]` — chapter đã có panel script ⇒ **buộc chọn** thay thế hoặc huỷ, ⛔ **không ghi đè âm thầm**. Cùng khuôn với `INV-9` của [`DB-Entity-Narrative-Timeline.md`](../Schema/DB-Entity-Narrative-Timeline.md) |

⚠️ **Endpoint này gọi LLM ⇒ phát sinh chi phí thật, nhưng ⛔ KHÔNG nằm trong rate limit `RL-1`.** `RL-1` ([`DB-Entity-Tenancy.md`](../Schema/DB-Entity-Tenancy.md)) chốt khoá đếm `(tenant_id, action)` với `action ∈ {upload, generate}`, và `generate` ở đó là **hành động sinh ảnh của `UC-06`**. ⛔ File này **không tự mở rộng** danh mục `action` — xem [`T-PS-RL`](#7-tbd-còn-lại---không-được-bịa).

### 4.2 Trạng thái gate trong response đọc — cưỡng chế `SDD-HG-01` hệ quả #5

Mọi response của `#2` và `#3` mang `gate_summary`, để client ⛔ **không phải tự suy ra** điều kiện `SDD-HG-01.4`:

```json
"gate_summary": {
  "dialogue_line_total": 12,
  "speaker_attribution_passed": 12,
  "dialogue_condensation_passed": 7
}
```

| Điều | Nội dung |
|---|---|
| **Nguồn số** | Đếm `comic.dialogue_line` trong phạm vi **so với** đếm row `comic.human_gate_state` cho **từng** `gate_kind` ([`DB-Entity-Dialogue-And-Gate.md`](../Schema/DB-Entity-Dialogue-And-Gate.md)) |
| ⛔ **Cấm** | ⛔ Không materialize giá trị này thành cột (`INV-9`); ⛔ không endpoint nào trong file này **ghi** được nó (`SDD-HG-01.2`) |
| ⚠️ **⛔ Không phải điều kiện export** | `gate_summary` là **thông tin hiển thị**. Phép kiểm chặn export chạy ở tầng server qua **đúng một** hàm dùng chung (`SDD-HG-01.4`), thuộc [`Endpoint-Preview-Export.md`](./Endpoint-Preview-Export.md) |

### 4.3 Hình dạng `PanelSpec`

| Nhóm field | Field | Ghi chú |
|---|---|---|
| Định danh | `id`, `page_id`, `panel_index` | read-only |
| Năm trường bắt buộc | `action`, `camera`, `visual_constraints`, `text_safe_zone`, và (ở mức page) `page_layout` | `NOT NULL` ở tầng DB, ⛔ **không `DEFAULT`** (`INV-1`) |
| Rubric | `beat_type`, `emphasis` | Danh mục đóng bằng `CHECK`. ⚠️ Tập giá trị `beat_type` **chưa đóng** — [`DB-Entity-Comic-IR.md`](../Schema/DB-Entity-Comic-IR.md) |
| Typesetting | `text_safe_zone_warning`, `text_budget`, `negative_space_hint` | `text_budget` là **dẫn xuất từ diện tích** ⇒ read-only ở API này |
| Nhân vật | `character_ids[]`, `character_count` | `character_count` do trigger duy trì ⇒ read-only |
| Liên kết ảnh | `approved_generation_id` | read-only ở file này — ghi thuộc [`Endpoint-Generation.md`](./Endpoint-Generation.md) |
| Gate | `gate_summary` | dẫn xuất, read-only ([§4.2](#42-trạng-thái-gate-trong-response-đọc--cưỡng-chế-sdd-hg-01-hệ-quả-5)) |

⛔ **⛔ KHÔNG có field hình học** (`x`, `y`, `w`, `h`, `area`) trong `PanelSpec` — bố cục **chỉ** sống ở `comic.page.page_layout` (`D-22`, `INV-6`). Gửi field hình học ⇒ `403 FIELD_NOT_WRITABLE`.

### 4.4 `#4 PATCH panel` — bảng field ghi được

| Field | Ghi được? | `action_type` của `change_log` | Ghi chú |
|---|:--:|---|---|
| `camera` | ✅ | `change_camera` | Giá trị **có sẵn** trong danh mục đóng |
| ⭐ `action` · `visual_constraints` · `text_safe_zone` · `beat_type` · `emphasis` · `character_ids[]` | ✅ | ⭐ `edit_panel_field` | ⭐ **ĐÃ MỞ KHOÁ.** Lô Schema **`L28b`** đã bổ sung giá trị này vào danh mục đóng, mỏ neo là [UC-03](../../020-Requirements/Use-Cases/UC-03-Review-Panel-Script.md) bước 9 + chính bảng này ([`DB-Entity-Provenance-And-Usage.md`](../Schema/DB-Entity-Provenance-And-Usage.md)). ⚠️ Sáu field này là **đúng tập được liệt kê** trong mỏ neo của giá trị. ⛔ `camera` **giữ nguyên** `change_camera`, ⛔ không nuốt vào `edit_panel_field` |
| ⚠️ `text_safe_zone_warning` · `negative_space_hint` | ⚠️ **blocked-by-TBD** | ⛔ **chưa có giá trị nào** | ⚠️ **Hai field này ⛔ KHÔNG nằm trong tập liệt kê của `edit_panel_field`** ⇒ ⛔ **không** được mở kèm theo. Xem [`T-CL-PANEL-EDIT`](#7-tbd-còn-lại---không-được-bịa) — ⛔ tái dụng `edit_panel_field` cho chúng chính là *"tái dụng thầm lặng"* mà danh mục cấm |
| `text_budget` · `character_count` · `approved_generation_id` · `panel_index` · `page_id` · `tenant_id` · `project_id` | ⛔ | — | `403 FIELD_NOT_WRITABLE` |
| Field hình học bất kỳ | ⛔ | — | `403 FIELD_NOT_WRITABLE` (`D-22`) |

**Ánh xạ lỗi từ tầng DB lên HTTP** — ⭐ DB **từ chối**, API **dịch**; ⛔ không có nhánh *"cảnh báo rồi cho qua"*:

| Vi phạm ở tầng DB | Mã lỗi HTTP | Neo |
|---|---|---|
| `character_count` vượt 3 (`ck_panel_max_characters`, kể cả đường `UPDATE` và đường race) | `409 PANEL_CHARACTER_LIMIT_EXCEEDED` | `INV-2`, `INV-3`, `INV-4` · `M2-2` |
| Một trong năm trường bắt buộc bị đẩy về `NULL` | `422 PANEL_REQUIRED_FIELD_MISSING` | `INV-1` |
| Toạ độ trong `text_safe_zone` ngoài `[0,1]` | `422 LAYOUT_COORDS_NOT_NORMALIZED` | `INV-5` |
| `character_ids[]` trỏ `bible_entity` không tồn tại (FK chéo schema) | `422 BIBLE_ENTITY_NOT_FOUND` | `INV-8` — từ chối **tại thời điểm ghi**, ⛔ không phát hiện muộn lúc sinh ảnh |

⚠️ **`PATCH panel` ⛔ KHÔNG đổi hình học ⇒ ⛔ KHÔNG kích hoạt `T1`.** Trường `gates_reset[]` trong response của `#4` vì vậy **luôn rỗng** ở horizon hiện tại; nó có mặt để hình dạng response của `#4`/`#5`/`#6` **đồng nhất**, ⛔ không phải chỗ chừa mơ hồ.

### 4.5 `#5 split` và `#6 merge` — hai endpoint đổi hình học

| Điều | Nội dung |
|---|---|
| ⭐ **`action_type` của `change_log`** | ⭐ `#5 split` ⇒ `split_panel`; `#6 merge` ⇒ `merge_panel`. **Hai giá trị RIÊNG**, đã có trong danh mục đóng (lô Schema **`L28b`**, mỏ neo [UC-03](../../020-Requirements/Use-Cases/UC-03-Review-Panel-Script.md) bước 9 — [`DB-Entity-Provenance-And-Usage.md`](../Schema/DB-Entity-Provenance-And-Usage.md)). ⛔ **Không** gộp hai hành động vào một giá trị, ⛔ không tái dụng `edit_panel_field` |
| ⭐ **Đổi tập panel ⇒ đổi `page_layout` ⇒ tính lại `text_budget`** | ⇒ kích hoạt `T1` ⇒ **reset gate 2** của **mọi dòng thuộc panel bị ảnh hưởng** (`SDD-HG-01.5`) |
| ⭐ **Bắt buộc trả `gates_reset[]`** | Cưỡng chế `SDD-HG-01` **hệ quả #4**: ⛔ **không được reset im lặng** — người dùng phải biết trang vừa rời trạng thái xuất bản được. Mỗi phần tử: `{dialogue_line_id, gate_kind: "dialogue_condensation"}` |
| **Panel mới của `split`** | `[Kiến trúc suy luận]` — kế thừa `action` / `camera` / `visual_constraints` từ panel gốc để thoả `INV-1`; `text_safe_zone` **tính lại** theo hình học mới. ⚠️ Người dùng vẫn phải sửa — kế thừa ⛔ không phải *"đã đúng"* |
| **`merge` và trần ≤3** | Hợp nhất hai panel mỗi bên 2 nhân vật ⇒ DB **từ chối** ⇒ `409 PANEL_CHARACTER_LIMIT_EXCEEDED`. ⛔ Không có nhánh *"gộp rồi cắt bớt nhân vật giúp"* |
| ⚠️ **Chưa đóng** | Quy tắc **chia hình học** khi split, và **phân lại `comic.dialogue_line`** giữa các panel khi split/merge — ⛔ **không nguồn nào trong repo** quy định. Xem [`T-PS-SPLIT`](#7-tbd-còn-lại---không-được-bịa) |

### 4.6 `#7 panel-script:approve` — ⚠️ reserve chỗ, ⛔ CHƯA hiện thực được

> [!WARNING]
> ⭐ **Endpoint này có mỏ neo nghiệp vụ (`UC-03` bước 10) và ĐÃ CÓ `action_type`, nhưng ⛔ VẪN KHÔNG có đích lưu trữ.**
> - ✅ **Đã có `action_type`**: lô Schema **`L28b`** mở giá trị `approve_panel_script` ([`DB-Entity-Provenance-And-Usage.md`](../Schema/DB-Entity-Provenance-And-Usage.md)). ⚠️ Hàng danh mục đó nói rõ nó **chỉ mở giá trị**, ⛔ **không** chọn thay đích lưu trạng thái.
> - ⛔ **Vẫn không cột trạng thái**: `comic.page` và `comic.panel` ⛔ không có cột duyệt nào ([`DB-Entity-Comic-IR.md`](../Schema/DB-Entity-Comic-IR.md)); `story.chapter` có cột duyệt **ingest** (`ingest_approved_at`) nhưng đó là ⛔ **một khái niệm khác** — ⛔ **TUYỆT ĐỐI không** tái dụng nó cho *"panel script đã duyệt"* ([`DB-Entity-Narrative-Timeline.md`](../Schema/DB-Entity-Narrative-Timeline.md)).
> ⇒ Route và hình dạng response được **giữ chỗ**, trạng thái vẫn là **blocked-by-TBD** (`T-PS-APPROVE`, ⭐ **đã thu hẹp về đúng câu hỏi đích lưu trữ**). ⛔ **Không tự thêm cột** — tầng `Schema/` đã đóng.

⚠️ **⛔ Đây KHÔNG phải một human gate.** `SDD-HG-01` định nghĩa **đúng hai** gate (`speaker_attribution`, `dialogue_condensation`) ở mức `dialogue_line`. *"Duyệt panel script"* là một mốc biên tập, ⛔ **không** là điều kiện chặn export và ⛔ **không** được cài vào phép kiểm `SDD-HG-01.4`.

---

## 5. Invariant của resource

| Mã | Invariant | Neo |
|---|---|---|
| `API-PS-1` | ⛔ **Không endpoint nào trong file này GHI trạng thái hai human gate.** Gate chỉ xuất hiện dưới dạng **giá trị đọc dẫn xuất** | `SDD-HG-01.2` · `INV-9` của [`DB-Entity-Dialogue-And-Gate.md`](../Schema/DB-Entity-Dialogue-And-Gate.md) |
| `API-PS-2` | ⛔ **Không endpoint nào nhận tham số bỏ qua gate** — ⛔ không query param, ⛔ không header, ⛔ không field body, ⛔ không scope/role. ⛔ Không `force`, không `skip_gates`, không `admin_override` | `SDD-HG-01` hệ quả #1 · `INV-8` của [`DB-Entity-Dialogue-And-Gate.md`](../Schema/DB-Entity-Dialogue-And-Gate.md) |
| `API-PS-3` | Endpoint đổi hình học (`#5`, `#6`) **phải trả `gates_reset[]`**; ⛔ không reset im lặng | `SDD-HG-01` hệ quả #4 · `SDD-HG-01.5` |
| `API-PS-4` | Response đọc `page`/`panel` mang `gate_summary` | `SDD-HG-01` hệ quả #5 |
| `API-PS-5` | ⛔ **Không field hình học trên `panel`** ở cả request lẫn response | `D-22` · `INV-6` của [`DB-Entity-Comic-IR.md`](../Schema/DB-Entity-Comic-IR.md) |
| `API-PS-6` | ⛔ **Không endpoint nào trong file này enqueue `public.job`** | Danh mục `job_type` đóng — [`DB-Entity-Job-Queue.md`](../Schema/DB-Entity-Job-Queue.md) |
| `API-PS-7` | Đọc dữ liệu schema `story` **chỉ qua** `resolveState()` / `getBible()` | `B-1` · `D-04` · [SDD §4.1](../Architecture/SDD-Comic-Studio.md) |
| `API-PS-8` | ⛔ **Không endpoint nào gọi copyright/similarity detection** | `SRS-NFR-15` · [SDD §5.4](../Architecture/SDD-Comic-Studio.md) |
| `API-PS-9` | Mọi đường ghi sinh `change_log` **trong cùng transaction** với thay đổi; boundary là **per-request** (`P-2`) | [ADR-017 `Q2` + `Q4.3`](../Architecture/ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md) |
| `API-PS-10` | ⛔ **Không response nào chứa điểm số thực cho bố cục**, dưới bất kỳ tên nào | `D-24` · `SRS-NFR-22` · `INV-7` |
| `API-PS-11` | Vi phạm constraint tầng DB được **dịch** thành mã lỗi 4xx tường minh; ⛔ **không** biến thành cảnh báo, ⛔ không nuốt thành `500` | `M2-2` (*"bị từ chối, không phải bị cảnh báo"*) |
| `API-PS-12` | ⭐ **Cả bảy endpoint kiểm cờ disable-access** ⇒ `disabled_by_takedown` (hoặc ⛔ thiếu row trạng thái) ⇒ `403 PROJECT_ACCESS_DISABLED`. ⛔ Không endpoint nào của file này nằm trong allowlist miễn kiểm | [`API-PRJ-4`](./Endpoint-Project.md#invariant-của-resource) · [Threat Model §4.4](../Security/Spec-Security-Threat-Model.md#44--c-3-danh-sách-đóng-các-đường-đọc-phải-kiểm-cờ-disable-access) Nhóm B (`C3-K1`…`C3-K4`) |

---

## 6. UC nào tiêu thụ

| UC | Bước | Endpoint |
|---|---|---|
| `UC-03` | b1 — yêu cầu sinh panel script cho chapter | `#1` |
| `UC-03` | b2 — đọc `Event` + gọi `resolveState()` | `#1` (bên trong, qua `B-1`) |
| `UC-03` | b3–b6 — phân chia scene→page→panel, cấp diện tích, ghi `page_layout`, khai `text_safe_zone` | `#1` |
| `UC-03` | b7 — ghi `Panel Specification` | `#1` |
| `UC-03` | b8 — đọc panel script | `#2`, `#3` |
| `UC-03` | b9 — sửa panel | `#4`, `#5`, `#6` |
| `UC-03` | b10 — đánh dấu đã duyệt | `#7` ⚠️ blocked-by-TBD |
| `UC-04` | b1 — tách dòng thoại theo panel | ⛔ **không** ở file này — [`Endpoint-Human-Gates.md`](./Endpoint-Human-Gates.md) |
| `UC-08` | b1 — đọc panel theo thứ tự đọc | `#2`, `#3` (bố cục thì ở [`Endpoint-Page-Layout.md`](./Endpoint-Page-Layout.md)) |

---

## 7. `TBD` còn lại — ⛔ không được bịa

| Mã | Khoảng trống | Ai đóng | Khi nào |
|---|---|---|---|
| `T-CL-PANEL-EDIT` ⭐ **ĐÃ THU HẸP** | ✅ **Phần lớn đã đóng** bởi lô Schema **`L28b`**: `edit_panel_field` (sáu field của [§4.4](#44-4-patch-panel--bảng-field-ghi-được)), `split_panel`, `merge_panel` đều đã vào danh mục ⇒ ⛔ **`UC-03` bước 9 KHÔNG còn bị chặn**. ⚠️ **Phần còn mở, đúng hai field**: `text_safe_zone_warning` và `negative_space_hint` ⛔ **không** nằm trong tập liệt kê của `edit_panel_field` ⇒ hoặc danh mục cần một giá trị nữa, hoặc hai field đó là **dẫn xuất read-only**. ⛔ Lô này ⛔ không tự chọn | **BA (mỏ neo yêu cầu) + Architect (mở `CHECK` hoặc chốt read-only)** | Trước khi hai field đó được mở cho `#4` |
| `T-PS-APPROVE` ⭐ **ĐÃ THU HẸP** | ✅ **`action_type` đã có**: `approve_panel_script` (lô Schema **`L28b`**). ⚠️ **Còn mở, đúng một câu hỏi**: ⭐ **đích LƯU trạng thái *"panel script đã duyệt"*** — một cột trên `comic.page`, một cột trên `story.chapter`, hay **chỉ** một `change_log` row là đủ. ⛔ **Không** tái dụng `story.chapter.ingest_approved_at` (khái niệm khác) và ⛔ **không** thêm giá trị thứ ba vào `status` | **Architect + PM** | Trước khi `#7` được implement |
| `T-PS-SPLIT` | Quy tắc **chia hình học** khi split và **phân lại `dialogue_line`** khi split/merge | **BA + Architect** | Trước khi hiện thực `#5`/`#6` |
| `T-PS-RL` | Endpoint `#1` gọi LLM (chi phí thật) nhưng ⛔ **không** nằm trong `RL-1`. Có mở `action` thứ ba cho rate limit không? | **PM/Founder** (cùng chủ với ngưỡng `SRS-NFR-20`) | Sau số đo MVP0 |
| `T-PS-LATENCY` | Nếu MVP0 đo thấy LLM của `#1` **vượt request timeout**, đường đúng là **thêm một `job_type`** ⇒ phải sửa danh mục đóng qua [ADR-015](../Architecture/ADR-015-Job-Queue-In-Postgres.md) trước. ⛔ Không lách bằng background thread | **Architect + Engineer** | Sau MVP0 |
| `T-API-ERR` | ⭐ **Ba quy ước chung cho 14 file API**: (a) ⇒ ⭐ **KHÔNG THEO DÕI Ở ĐÂY NỮA** — chuẩn đặt tên `error_code` + hình dạng error envelope là **cùng một câu hỏi** với [`TBD-API-ENV`](./Endpoint-Project.md) và ⭐ **`TBD-API-ENV` là SỔ ĐĂNG KÝ CHÍNH**; ⚠️ câu hỏi ⛔ **vẫn MỞ**, chỉ là **một sổ thay vì hai**. Lý do chọn: bản nháp quy ước `API-ENV-1` (envelope + danh mục `code` dùng chung) **sống trong `Endpoint-Project.md`** ⇒ giữ câu hỏi cạnh câu trả lời nháp để ⛔ không trôi lần thứ hai; (b) ✅ **ĐÃ CHỐT `/v1/…`** cho tiền tố đường dẫn (lô `L28a`, đã quét đủ 14 file); (c) ⛔ **chưa chốt** — quy ước đặt tên hành động (`:verb` vs sub-resource). ⇒ Hàng này còn theo dõi **đúng (c)** | **Architect (một lô quét toàn thư mục)** — (a) theo `TBD-API-ENV` | Trước khi file API đầu tiên được implement |
| `T-PS-BEAT` | Tập giá trị đóng của `beat_type` (đang khởi tạo bằng 4 giá trị ví dụ) | **BA + Founder** — hàng đã đăng ký ở [`DB-Entity-Comic-IR.md`](../Schema/DB-Entity-Comic-IR.md) | Trước Active Sprint |

---

## 8. Tài liệu tham khảo

- [SDD Comic Studio](../Architecture/SDD-Comic-Studio.md) — §5.1 `F3`, §6.3 `SDD-HG-01`
- [ADR-012 — Comic IR: spec là dữ liệu chính, ảnh chỉ là output](../Architecture/ADR-012-Comic-IR-Spec-As-Primary-Data.md)
- [ADR-015 — Job queue trong PostgreSQL](../Architecture/ADR-015-Job-Queue-In-Postgres.md)
- [ADR-017 — Chuỗi provenance và MỘT transaction boundary](../Architecture/ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md)
- [ADR-006 — RLS & tenant context injection](../Architecture/ADR-006-RLS-Tenant-Context-Injection.md)
- [`DB-Entity-Comic-IR.md`](../Schema/DB-Entity-Comic-IR.md) · [`DB-Entity-Dialogue-And-Gate.md`](../Schema/DB-Entity-Dialogue-And-Gate.md) · [`DB-Entity-Job-Queue.md`](../Schema/DB-Entity-Job-Queue.md) · [`DB-Entity-Provenance-And-Usage.md`](../Schema/DB-Entity-Provenance-And-Usage.md)
- [UC-03 — Review Panel Script](../../020-Requirements/Use-Cases/UC-03-Review-Panel-Script.md)
