---
id: SPEC-API-BUBBLE-TYPESET
type: spec
status: draft
project: comic-studio
created: 2026-08-29
---

# Endpoint: Bubble & Typeset

Bề mặt API của **tầng chữ** — `comic.bubble`. Đây là nửa **bên phải** ranh giới art ↔ chữ (`D-29`, `SRS-FR-11`): string đặt trên toạ độ chuẩn hoá, ⛔ **không** pixel.

**Serves:** [UC-07 — Edit Bubble And Dialogue In Panel](../../020-Requirements/Use-Cases/UC-07-Edit-Bubble-And-Dialogue-In-Panel.md) bước 3–9 · [UC-08 — Arrange Page And Preview](../../020-Requirements/Use-Cases/UC-08-Arrange-Page-And-Preview.md) (đường đọc của compositor)

**Nguồn ràng buộc** (⛔ file này **không** đặc tả lại, chỉ trỏ theo mã):

| Ràng buộc | Nguồn duy nhất |
|---|---|
| Hai human gate + điều kiện chặn xuất bản | [SDD §6.3 `SDD-HG-01`](../Architecture/SDD-Comic-Studio.md) |
| `change_log` cùng transaction (`KC-4`) | [ADR-017 `Q2`, `Q4.3` `P-2`](../Architecture/ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md) |
| Tenant context + RLS trên mọi truy vấn | [ADR-006 `D3`](../Architecture/ADR-006-RLS-Tenant-Context-Injection.md) |
| Polling `CT-POLL-2S` cho tác vụ async | [ADR-015 `Q6`](../Architecture/ADR-015-Job-Queue-In-Postgres.md) — ⚠️ **⛔ không endpoint nào của file này là async** |
| Hình dạng bảng, index, invariant `T-1`…`T-12` | [`DB-Entity-Typeset-Layer.md`](../Schema/DB-Entity-Typeset-Layer.md) |
| Typeset tách khỏi art, một compositor, reset gate | [ADR-013](../Architecture/ADR-013-Typeset-Layer-Separate-From-Art.md) |

---

## Danh sách endpoint

> **Auth**: mọi endpoint dưới đây yêu cầu **session người dùng thật** và chạy trong **một transaction tường minh** có tenant context ([ADR-006 `D3`](../Architecture/ADR-006-RLS-Tenant-Context-Injection.md)). ⚠️ ID không thuộc tenant hiện tại đọc ra **`0 row`** ⇒ trả **`404`**, ⛔ **không** `403` — fail-closed, ⛔ không tiết lộ sự tồn tại ([ADR-010 `D9`](../Architecture/ADR-010-Tenant-Isolation-With-RLS.md)).

| # | Method · Path | Mục đích |
|--:|---|---|
| `E-BT-1` | `GET /v1/panels/{panel_id}/bubbles` | Đọc **toàn bộ** typeset layer của một panel, theo `reading_order` |
| `E-BT-2` | `POST /v1/panels/{panel_id}/bubbles` | Tạo một bubble gắn vào một `dialogue_line` |
| `E-BT-3` | `PATCH /v1/bubbles/{bubble_id}` | Sửa **hình học** bubble (vị trí, kích thước, tail) |
| `E-BT-4` | `PUT /v1/panels/{panel_id}/bubbles/reading-order` | ⭐ Đặt lại **thứ tự đọc** cho **toàn bộ** bubble của panel — **một lần ghi nguyên tử** |
| `E-BT-5` | `DELETE /v1/bubbles/{bubble_id}` | Xoá một bubble |

> [!IMPORTANT]
> ⭐ **Cả năm endpoint đều là "đường đọc/ghi NỘI DUNG trong phạm vi project"** ⇒ **đều** trả `403 PROJECT_ACCESS_DISABLED` khi project ở `disabled_by_takedown`. Chúng định danh bằng `panel_id` / `bubble_id` và ⛔ **không** mang `project_id` trên path ⇒ phải **resolve ngược lên project** rồi mới kiểm cờ (`C3-K1`).
> Luật ở [`API-PRJ-4`](./Endpoint-Project.md#invariant-của-resource) — ⛔ file này **không chép lại**, chỉ trỏ theo mã: đi qua **đúng một** hàm dùng chung ở tầng service (`C3-K3`), **fail-closed** khi ⛔ không thấy row `public.project_access_state` (`C3-K2`). Cưỡng chế bằng **test bảng route toàn cục** khuôn `M1-1`, ⛔ **không** test per-endpoint (`C3-K4`). Danh sách đóng: [Threat Model §4.4](../Security/Spec-Security-Threat-Model.md#44--c-3-danh-sách-đóng-các-đường-đọc-phải-kiểm-cờ-disable-access).

---

### `E-BT-1` · `GET /v1/panels/{panel_id}/bubbles`

| | |
|---|---|
| **Auth** | Session người dùng + tenant context |
| **Request** | Path: `panel_id` (UUID). ⛔ Không query param nào lọc/bỏ qua ràng buộc |
| **Response `200`** | `{ panel_id, bubbles: [ { id, dialogue_line_id, bubble_kind, x, y, w, h, tail_x, tail_y, reading_order, placement_origin, updated_at } ] }` — **sắp xếp theo `reading_order` tăng dần** |

- Thứ tự trả về **là dữ liệu**, ⛔ không phải hệ quả của toạ độ (`SRS-FR-16`) — đường đọc dùng `ix_bubble_panel_order`.
- Toạ độ luôn là **số chuẩn hoá 0–1 trong hệ quy chiếu PANEL** (`T-1`, `T-2`). ⛔ Không endpoint nào trả pixel; ⛔ không client nào được gửi pixel.
- `bubble_kind` được trả **nguyên trạng** như DB lưu; ⛔ **danh mục giá trị chưa chốt** — xem [`TBD-BUBBLE-KIND`](#tbd-còn-lại).

| Mã lỗi | Khi nào |
|---|---|
| `401` | ⛔ Không có session hợp lệ |
| `403` `PROJECT_ACCESS_DISABLED` | Project chứa panel này ở **disable-access** do takedown (hoặc ⛔ không thấy row trạng thái) — [`API-PRJ-4`](./Endpoint-Project.md#invariant-của-resource) |
| `404` | `panel_id` ⛔ không tồn tại **hoặc** không thuộc tenant hiện tại (RLS `0 row`) |

---

### `E-BT-2` · `POST /v1/panels/{panel_id}/bubbles`

| | |
|---|---|
| **Auth** | Session người dùng + tenant context |
| **Request** | `{ dialogue_line_id, bubble_kind?, x, y, w, h, tail_x?, tail_y?, reading_order }` |
| **Response `201`** | Object bubble như `E-BT-1` |

- `dialogue_line_id` là **bắt buộc** ở horizon MVP0–MVP2 — ⛔ **không tồn tại** bubble không gắn dòng thoại ([`DB-Entity-Typeset-Layer.md`](../Schema/DB-Entity-Typeset-Layer.md), ghi chú nullability). ⇒ ⛔ **Không** chấp nhận `null` *"cho SFX/narration"*; hạng mục đó còn `TBD`.
- Bubble tạo bởi người ⇒ `placement_origin = 'manual'`. Bubble do auto-placement ghi ⇒ `'auto'` — ⛔ **không** phải tham số của endpoint này, mà là hệ quả của **đường ghi** (`T-7`).
- Ghi **một** `public.change_log` row **cùng transaction** ([ADR-017 `Q2`](../Architecture/ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md), `T-8`) với ⭐ `action_type = 'create_bubble'` — giá trị **đã có** trong danh mục đóng ([`DB-Entity-Provenance-And-Usage.md`](../Schema/DB-Entity-Provenance-And-Usage.md), lô Schema `L28b`). ⛔ **Không** tái dụng `move_bubble`.

| Mã lỗi | Khi nào |
|---|---|
| `400` | Thiếu trường bắt buộc; `dialogue_line_id` là `null` |
| `403` `PROJECT_ACCESS_DISABLED` | Project chứa panel này ở **disable-access** do takedown (hoặc ⛔ không thấy row trạng thái) — [`API-PRJ-4`](./Endpoint-Project.md#invariant-của-resource) |
| `404` | `panel_id` hoặc `dialogue_line_id` ⛔ không thấy dưới RLS |
| `409` | ⭐ `reading_order` đã có bubble khác chiếm — `UNIQUE (tenant_id, panel_id, reading_order)` (`T-6`). ⚠️ Client sửa bằng `E-BT-4`, ⛔ không bằng cách thử số khác trong vòng lặp |
| `422` | Toạ độ vi phạm `T-1` (`x+w > 1`, `w <= 0`…) hoặc tail nửa vời `T-5` (`tail_x` có mà `tail_y` không) |

---

### `E-BT-3` · `PATCH /v1/bubbles/{bubble_id}`

| | |
|---|---|
| **Auth** | Session người dùng + tenant context |
| **Request** | `{ x?, y?, w?, h?, tail_x?, tail_y?, bubble_kind? }` — **partial** |
| **Response `200`** | Object bubble sau khi sửa |

- ⭐ **Mọi lần ghi thành công qua endpoint này đặt `placement_origin = 'manual'`.** Đây là cách `T-7` được cưỡng chế: lần auto-placement sau ⛔ **không được** ghi đè bubble người đã kéo. ⛔ `placement_origin` ⛔ **không** phải trường của request — client ⛔ không set được nó về `'auto'`.
- ⚠️ **Endpoint này ⛔ KHÔNG reset human gate #2.** Hai trigger reset của `SDD-HG-01.5` là **`text_budget` đổi** và **`dialogue_rendered` đổi**; ⛔ không cái nào xảy ra ở đây. ⚠️ Đọc `T-12` của [`DB-Entity-Typeset-Layer.md`](../Schema/DB-Entity-Typeset-Layer.md): `T-7` bảo vệ **vị trí**, `T-12` reset **trạng thái duyệt của dòng thoại** — ⛔ nhầm hai cái là **thêm** một reset không có nguồn, hoặc **bỏ** một reset bắt buộc.
- ⛔ **Endpoint này ⛔ không gọi image generation, ⛔ không tiêu credit sinh ảnh, ⛔ không ghi chữ vào pixel** ([UC-07](../../020-Requirements/Use-Cases/UC-07-Edit-Bubble-And-Dialogue-In-Panel.md) bước 5, `D-29`).
- Sinh `change_log` `action_type = 'move_bubble'` cùng transaction (`T-8`).

| Mã lỗi | Khi nào |
|---|---|
| `403` `PROJECT_ACCESS_DISABLED` | Project chứa bubble này ở **disable-access** do takedown (hoặc ⛔ không thấy row trạng thái) — [`API-PRJ-4`](./Endpoint-Project.md#invariant-của-resource) |
| `404` | `bubble_id` ⛔ không thấy dưới RLS |
| `422` | Vi phạm `T-1` hoặc `T-5`; hoặc `bubble_kind` ngoài `CHECK` khi danh mục đã chốt |

---

### `E-BT-4` · `PUT /v1/panels/{panel_id}/bubbles/reading-order`

| | |
|---|---|
| **Auth** | Session người dùng + tenant context |
| **Request** | `{ order: [ bubble_id, bubble_id, … ] }` — ⭐ **phải liệt kê ĐỦ và ĐÚNG** tập bubble hiện có của panel |
| **Response `200`** | Danh sách bubble sau khi đặt lại, theo thứ tự mới |

> ⭐ **Vì sao đây là một endpoint riêng chứ không phải `PATCH` từng bubble** — lý do **suy ra từ schema, ⛔ không phải sở thích**: `UNIQUE (tenant_id, panel_id, reading_order)` (`T-6`) làm cho phép **hoán vị** hai bubble ⛔ **không thể** biểu diễn bằng hai lần `PATCH` độc lập — lần ghi thứ nhất đã va `UNIQUE`. Một endpoint nhận **toàn bộ hoán vị** và ghi trong **một** transaction là hình dạng duy nhất thoả `T-6` mà ⛔ không cần giá trị trung gian giả.

- ⛔ **Không giải bằng cách gán tạm một `reading_order` âm/lớn rồi sửa lại.** Giá trị trung gian là trạng thái sai đọc được bởi request khác trong cùng khoảnh khắc.
- Sinh **một** `change_log` với ⭐ `action_type = 'reorder_bubble'` cho **cả** thao tác sắp xếp, ⛔ không phải N dòng — thao tác của người là **một**. ⚠️ Giá trị này ⛔ **khác** `reorder_panel` (reorder ở tầng page layout) và ⛔ **khác** `move_bubble` (kéo **một** bubble) — [`DB-Entity-Provenance-And-Usage.md`](../Schema/DB-Entity-Provenance-And-Usage.md).

| Mã lỗi | Khi nào |
|---|---|
| `403` `PROJECT_ACCESS_DISABLED` | Project chứa panel này ở **disable-access** do takedown (hoặc ⛔ không thấy row trạng thái) — [`API-PRJ-4`](./Endpoint-Project.md#invariant-của-resource) |
| `404` | `panel_id` ⛔ không thấy; hoặc một `bubble_id` trong `order` ⛔ không thuộc panel đó |
| `409` | ⭐ Tập `order` ⛔ **không khớp** tập bubble hiện có của panel (thiếu, thừa, hoặc trùng ID) — ⚠️ nghĩa là client đang làm việc trên bản đọc **cũ**; ⛔ không tự lấp phần thiếu |
| `422` | `order` rỗng |

---

### `E-BT-5` · `DELETE /v1/bubbles/{bubble_id}`

| | |
|---|---|
| **Auth** | Session người dùng + tenant context |
| **Request** | Path: `bubble_id` |
| **Response `204`** | ⛔ Không body |

- Xoá bubble ⛔ **không** xoá `comic.dialogue_line`. Bubble **hiển thị** thoại, ⛔ không **sở hữu** thoại ⇒ dòng thoại vẫn tồn tại và vẫn nằm trong phạm vi vị từ `SDD-HG-01.4`.
- ⚠️ Hệ quả phải nói ra: xoá bubble ⛔ **không** làm một dòng thoại *"biến mất khỏi điều kiện export"*. ⛔ Đây ⛔ không phải một đường lách gate.
- Sau khi xoá, `reading_order` của các bubble còn lại **giữ nguyên** (dãy có lỗ là hợp lệ — `T-6` chỉ cấm trùng). Muốn dồn lại ⇒ gọi `E-BT-4`.
- Sinh `change_log` cùng transaction với ⭐ `action_type = 'delete_bubble'` — giá trị **đã có** trong danh mục đóng ([`DB-Entity-Provenance-And-Usage.md`](../Schema/DB-Entity-Provenance-And-Usage.md), lô Schema `L28b`).

| Mã lỗi | Khi nào |
|---|---|
| `403` `PROJECT_ACCESS_DISABLED` | Project chứa bubble này ở **disable-access** do takedown (hoặc ⛔ không thấy row trạng thái) — [`API-PRJ-4`](./Endpoint-Project.md#invariant-của-resource) |
| `404` | `bubble_id` ⛔ không thấy dưới RLS |

---

## Invariant của resource

| # | Invariant | Cưỡng chế ở đâu |
|:--:|---|---|
| `API-BT-1` | ⭐ **⛔ Không endpoint nào của file này nhận, trả, hay sinh `object key` / signed URL.** Ảnh nền của panel là nửa **bên trái** ranh giới `B-4` | Ranh giới `B-4` ([SDD §4.1](../Architecture/SDD-Comic-Studio.md)) · [ADR-004](../Architecture/ADR-004-Object-Storage-Vendor-And-Signed-URL.md) điều 3 |
| `API-BT-2` | ⭐ **⛔ Không endpoint nào gọi image generation.** Render typeset là **code**, ⛔ không phải một lần sinh ảnh | [UC-07](../../020-Requirements/Use-Cases/UC-07-Edit-Bubble-And-Dialogue-In-Panel.md) bước 5 · [ADR-013](../Architecture/ADR-013-Typeset-Layer-Separate-From-Art.md) |
| `API-BT-3` | **Mọi ghi sinh đúng một `change_log` row, cùng transaction** | [ADR-017 `Q2`](../Architecture/ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md) · `T-8` |
| `API-BT-4` | ⛔ **Không tham số nào bỏ qua human gate**, ⛔ không `force`, ⛔ không `skip_gates` | `SDD-HG-01.4` hệ quả #1 |
| `API-BT-5` | ⭐ **Ghi qua `E-BT-3` luôn đặt `placement_origin = 'manual'`; client ⛔ không set được `'auto'`** | `T-7` |
| `API-BT-6` | ⛔ **Không endpoint nào của file này chạy async** ⇒ ⛔ không job, ⛔ không polling. `job_type` là **danh mục đóng** và ⛔ không chứa typeset | [`DB-Entity-Job-Queue.md`](../Schema/DB-Entity-Job-Queue.md) |
| `API-BT-7` | Toạ độ trên dây là **`NUMERIC` chuẩn hoá 0–1**, ⛔ không float pixel — preview và export phải cho ra **cùng một trang** | `T-1`, `T-2` · `D-32` |
| `API-BT-8` | ⭐ **Cả năm endpoint kiểm cờ disable-access** ⇒ `disabled_by_takedown` (hoặc ⛔ thiếu row trạng thái) ⇒ `403 PROJECT_ACCESS_DISABLED`. ⛔ Không endpoint nào của file này nằm trong allowlist miễn kiểm | [`API-PRJ-4`](./Endpoint-Project.md#invariant-của-resource) · [Threat Model §4.4](../Security/Spec-Security-Threat-Model.md#44--c-3-danh-sách-đóng-các-đường-đọc-phải-kiểm-cờ-disable-access) Nhóm B (`C3-K1`…`C3-K4`) |

### ⛔ Ba thứ KHÔNG nằm ở file này

| ⛔ Không ở đây | Ở đâu | Vì sao |
|---|---|---|
| ⭐ **Sửa nội dung thoại** (`dialogue_rendered`) | `Endpoint-Human-Gates.md` (resource #8, *patch rendered*) | ⚠️ **Đây là một sai lệch CÓ CHỦ Ý so với [findings §4.1](../../010-Planning/pm-runs/2026-08-28-phase-2-architecture-design-comic-studio/findings/architect.md)** (hàng #11 ghi *"patch text"*). Schema chốt ngược lại: *"Bubble hiển thị thoại, ⛔ không **sở hữu** thoại"*. Text sống ở `comic.dialogue_line`, và **cả hai** ràng buộc chịu lực của nó — khoá chống ghi đè (`SDD-HG-01.7`) và reset gate #2 (`SDD-HG-01.5`) — sống ở **mức dòng thoại**. Một đường ghi thứ hai qua bubble là **đường bypass** của cả hai ⇒ `M2-4` FAIL |
| Ảnh nền panel + signed URL đọc inline | Đường đọc `page`/`panel` (`Endpoint-Panel-Script.md`) | [ADR-004](../Architecture/ADR-004-Object-Storage-Vendor-And-Signed-URL.md) điều 6: URL phát **theo lô, kèm trong response của resource**; ⛔ **không có** endpoint *"xin URL cho từng ảnh"* |
| `text_safe_zone`, `text_budget`, `negative_space_hint` | `comic.panel` ([`DB-Entity-Comic-IR.md`](../Schema/DB-Entity-Comic-IR.md)) | [ADR-012](../Architecture/ADR-012-Comic-IR-Spec-As-Primary-Data.md) điều 9 — field của **panel spec**, ⛔ không của tầng typeset. Kiểm đè safe zone là việc của compositor/validator, đọc từ panel |

---

## UC nào tiêu thụ

| UC · bước | Endpoint |
|---|---|
| [UC-07](../../020-Requirements/Use-Cases/UC-07-Edit-Bubble-And-Dialogue-In-Panel.md) bước 2 (typeset layer tách rời) | `E-BT-1` — ⚠️ nửa **ảnh nền** do đường đọc panel phục vụ, ⛔ không phải endpoint này |
| [UC-07](../../020-Requirements/Use-Cases/UC-07-Edit-Bubble-And-Dialogue-In-Panel.md) bước 4 (ghi vị trí bubble, kiểu bubble, tail) | `E-BT-2`, `E-BT-3`, `E-BT-4`, `E-BT-5` |
| [UC-07](../../020-Requirements/Use-Cases/UC-07-Edit-Bubble-And-Dialogue-In-Panel.md) bước 4 (**nội dung thoại**) | ⛔ **Không ở file này** — `Endpoint-Human-Gates.md` |
| [UC-07](../../020-Requirements/Use-Cases/UC-07-Edit-Bubble-And-Dialogue-In-Panel.md) bước 5 (render typeset bằng code) | ⛔ Không phải một endpoint — compositor, `Endpoint-Preview-Export.md` |
| [UC-07](../../020-Requirements/Use-Cases/UC-07-Edit-Bubble-And-Dialogue-In-Panel.md) bước 7 (ghi `change_log`) | Hệ quả của `E-BT-2`…`E-BT-5`, ⛔ không phải endpoint riêng |
| [UC-07](../../020-Requirements/Use-Cases/UC-07-Edit-Bubble-And-Dialogue-In-Panel.md) bước 8 (reset gate #2 khi thoại đổi) | ⛔ Không ở file này — trigger là **thoại**, ⛔ không phải bubble |
| [UC-08](../../020-Requirements/Use-Cases/UC-08-Arrange-Page-And-Preview.md) bước 10 (composite server-side) | `E-BT-1` là **đường đọc** mà compositor dùng (`ix_bubble_panel_order`) |

⚠️ **Phạm vi build**: toàn bộ **editor tương tác** của [UC-07](../../020-Requirements/Use-Cases/UC-07-Edit-Bubble-And-Dialogue-In-Panel.md) (kéo bubble, chọn kiểu, kéo tail) nằm **NGOÀI 24 Story** ([Story-Bubble-Text-Overlay-Editor](../../022-User-Stories/Backlog/Story-Bubble-Text-Overlay-Editor.md)). Trong 24 chỉ có [Story-Typeset-Layer-And-Bubble-Overlay](../../022-User-Stories/Backlog/Story-Typeset-Layer-And-Bubble-Overlay.md) — MVP0, composite bằng script. ⇒ File này là **contract**, ⛔ **không** là cam kết lịch build.

---

## `TBD` còn lại

| Khoảng trống | Ai đóng | Khi nào |
|---|---|---|
| ~~**`action_type` cho TẠO / XOÁ / SẮP XẾP LẠI bubble**~~ ⇒ ✅ **ĐÃ ĐÓNG** bởi lô Schema **`L28b`**: danh mục mở **ba giá trị RIÊNG** `create_bubble` (`E-BT-2`), `reorder_bubble` (`E-BT-4`), `delete_bubble` (`E-BT-5`) — ⛔ cách đọc *"`move_bubble` là giá trị bao trùm"* **BỊ BÁC** ([`DB-Entity-Provenance-And-Usage.md`](../Schema/DB-Entity-Provenance-And-Usage.md)). ⇒ `T-8` được thoả cho **mọi** thao tác typeset; ⛔ không còn endpoint nào của file này bị chặn bởi hàng này | — (đã đóng) | — |
| ⭐ **`TBD-BUBBLE-KIND`** — danh mục kiểu bubble ⛔ **chưa chốt** ⇒ `bubble_kind` trong request/response của `E-BT-2`, `E-BT-3` ⛔ **chưa có tập giá trị hợp lệ**, và `422` của nó ⛔ chưa cưỡng chế được | **PM / Founder** (theo [`DB-Entity-Typeset-Layer.md`](../Schema/DB-Entity-Typeset-Layer.md)) | Trước migration đầu tiên chạm `comic.bubble` |
| SFX / narration box / caption ⇒ có nới `dialogue_line_id` nullable không (ảnh hưởng `400` của `E-BT-2`) | **PM / Founder** | Ngoài horizon MVP0–MVP2 |
| Đường ghi **auto-placement** (heuristic đặt bubble lần đầu) là endpoint hay bước nội bộ của pipeline | **Architect**, lô sau | Khi [Story-Bubble-Text-Overlay-Editor](../../022-User-Stories/Backlog/Story-Bubble-Text-Overlay-Editor.md) vào scope |

---

## Tài liệu tham khảo

- [ADR-013 — Typeset Layer Separate From Art](../Architecture/ADR-013-Typeset-Layer-Separate-From-Art.md)
- [ADR-012 — Comic IR Spec As Primary Data](../Architecture/ADR-012-Comic-IR-Spec-As-Primary-Data.md)
- [ADR-004 — Object Storage Vendor And Signed URL](../Architecture/ADR-004-Object-Storage-Vendor-And-Signed-URL.md)
- [ADR-006 — RLS Tenant Context Injection](../Architecture/ADR-006-RLS-Tenant-Context-Injection.md)
- [ADR-017 — Provenance Chain And One Transaction Boundary](../Architecture/ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md)
- [SDD — Comic Studio](../Architecture/SDD-Comic-Studio.md)
- [`DB-Entity-Typeset-Layer.md`](../Schema/DB-Entity-Typeset-Layer.md) · [`DB-Entity-Dialogue-And-Gate.md`](../Schema/DB-Entity-Dialogue-And-Gate.md) · [`DB-Entity-Comic-IR.md`](../Schema/DB-Entity-Comic-IR.md)
- [Story-Typeset-Layer-And-Bubble-Overlay](../../022-User-Stories/Backlog/Story-Typeset-Layer-And-Bubble-Overlay.md)
