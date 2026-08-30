---
id: SPEC-API-PAGE-LAYOUT
type: spec
status: draft
project: comic-studio
created: 2026-08-29
updated: 2026-08-30
---

# Endpoint: Page Layout

Bề mặt API của **bố cục trang**. Toàn bộ file này xoay quanh một sự thật đã chốt: ⭐ **`comic.page.page_layout JSONB` là NƠI LƯU DUY NHẤT của bố cục** (`D-22`) — template chỉ là **preset được copy vào chính cột đó**, ⛔ không có schema layout thứ hai.

Đây cũng là file chứa **nguồn phát của `T1`**: mọi endpoint ở đây đổi diện tích panel ⇒ tính lại `text_budget` ⇒ **reset gate 2**.

**Decided in:**

- [ADR-012 — Comic IR: spec là dữ liệu chính](../Architecture/ADR-012-Comic-IR-Spec-As-Primary-Data.md) — `## Decision` điều 5–8 (`D-22`, `D-23`, `D-24`)
- [ADR-013 — Typeset layer tách khỏi art](../Architecture/ADR-013-Typeset-Layer-Separate-From-Art.md) — `## Decision` điều 8–9 (`D-32`, `D-33` `T1`)
- [ADR-017 — Chuỗi provenance và MỘT transaction boundary](../Architecture/ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md) — `Q2`, `Q4.3` `P-2` (hàng `Endpoint-*` của `Q4.7`)
- [ADR-006 — RLS & tenant context injection](../Architecture/ADR-006-RLS-Tenant-Context-Injection.md)
- [SDD Comic Studio](../Architecture/SDD-Comic-Studio.md) — §5.1 `F3`, §5.3, §6.3 `SDD-HG-01`, §8.2 `S-6`
- [`DB-Entity-Comic-IR.md`](../Schema/DB-Entity-Comic-IR.md) — ⭐ quyết định *"`layout_template` là SEED DATA"* + `LT-1`…`LT-5`, `INV-5`, `INV-6`, `INV-10`
- [`DB-Entity-Dialogue-And-Gate.md`](../Schema/DB-Entity-Dialogue-And-Gate.md) — `INV-6`, `INV-7` (phạm vi reset `T1`)
- [`DB-Entity-Provenance-And-Usage.md`](../Schema/DB-Entity-Provenance-And-Usage.md) — danh mục `action_type` đóng

---

## 1. Resource

| Resource | Bảng / nơi lưu | Ghi chú |
|---|---|---|
| Bố cục của một trang | `comic.page.page_layout JSONB` | ⭐ **Nơi lưu duy nhất**, toạ độ **chuẩn hoá 0–1** |
| Preset đã áp | `comic.page.applied_template_key TEXT NULL` | ⭐ **Chỉ để provenance**, ⛔ **không phải khoá ngoại** (`LT-3`) |
| Registry preset | ⭐ **Hằng số versioned TRONG CODE (seed)** | ⛔ **KHÔNG có bảng `comic.layout_template`** — quyết định của [`DB-Entity-Comic-IR.md`](../Schema/DB-Entity-Comic-IR.md) |
| Diện tích/quota `emphasis` | `comic.panel.emphasis` + quota **cấu hình** phạm vi chapter | ⛔ Quota **không** cưỡng chế bằng `CHECK` (`INV-10`) |

---

## 2. Quy ước chung — ⛔ file này KHÔNG đặc tả lại bốn ràng buộc xuyên-endpoint

| Mã | Ràng buộc | Nguồn **DUY NHẤT** | File này được làm gì |
|---|---|---|---|
| `SDD-HG-01` | Không đường nào bypass hai human gate | [SDD §6.3](../Architecture/SDD-Comic-Studio.md) | Trỏ theo mã `.4`, `.5` + hệ quả #1, #4, #5. ⛔ **Không đặc tả lại luật reset** |
| `KC-4` | Artifact + bằng chứng commit **một** transaction | [ADR-017 `Q4`](../Architecture/ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md) | Trỏ `Q2` + `Q4.3` `P-2` (`Q4.7`). ⛔ Không viết *"tầng DB cưỡng chế `KC-4`"* (`Q4.6`) |
| `CT-POLL-2S` | Polling **2 giây**, ⛔ không WebSocket. Độ rắn: **MẶC ĐỊNH**, ⛔ không nâng thành `CHỐT` | [ADR-015 `Q6`](../Architecture/ADR-015-Job-Queue-In-Postgres.md) | ⛔ **Không endpoint nào trong file này là async** — mọi endpoint đồng bộ |
| RLS + tenant context | Mọi query qua RLS với `app.current_tenant` | [ADR-006](../Architecture/ADR-006-RLS-Tenant-Context-Injection.md) | Cột `Auth` ghi *"tenant member"*; ⚠️ ngoại lệ `#5` — xem [§4.4](#44-5-get-layout-templates--đọc-registry-trong-code--không-phải-bảng) |

**Quy ước mã lỗi**: `HTTP status` + `error_code` `SCREAMING_SNAKE` ổn định. Chuẩn chung cho 14 file = `T-API-ERR` (đăng ký ở [`Endpoint-Panel-Script.md`](./Endpoint-Panel-Script.md)).

> [!CAUTION]
> ⛔ **`SRS-NFR-15` — ⛔ KHÔNG endpoint nào trong file này gọi copyright/similarity detection.** Anti-feature **có chủ ý**, ⛔ không phải tính năng bị hoãn.

---

## 3. Danh sách endpoint

| # | Method · Path | Auth | Request | Response | Mã lỗi |
|--:|---|---|---|---|---|
| 1 | `GET /v1/pages/{page_id}/layout` | tenant member | — | `200` `{page_id, page_layout, applied_template_key, panels[]: {id, panel_index, emphasis, text_budget}, gate_summary}` | `403 PROJECT_ACCESS_DISABLED` · `404 PAGE_NOT_FOUND` |
| 2 | `POST /v1/pages/{page_id}/layout:apply-template` | tenant member | `{template_key: string}` | `200` `{page_layout, applied_template_key, text_budget_changed[], gates_reset[]}` | `403 PROJECT_ACCESS_DISABLED` · `404 PAGE_NOT_FOUND` · `404 TEMPLATE_NOT_FOUND` · `409 TEMPLATE_PANEL_COUNT_MISMATCH` · `422 LAYOUT_COORDS_NOT_NORMALIZED` |
| 3 | `POST /v1/pages/{page_id}/panels:swap` | tenant member | `{panel_id_a: uuid, panel_id_b: uuid}` | `200` `{page_layout, panels[], text_budget_changed[], gates_reset[]}` | `403 PROJECT_ACCESS_DISABLED` · `404 PAGE_NOT_FOUND` · `409 PANEL_NOT_ON_PAGE` · `422 SWAP_REQUIRES_TWO_DISTINCT_PANELS` |
| 4 | `POST /v1/pages/{page_id}/panels:reorder` | tenant member | `{panel_ids: [uuid, …]}` — **hoán vị đầy đủ** tập panel của page | `200` `{page_layout, panels[], text_budget_changed[], gates_reset[]}` | `403 PROJECT_ACCESS_DISABLED` · `404 PAGE_NOT_FOUND` · `422 REORDER_NOT_A_PERMUTATION` |
| 5 | `GET /v1/layout-templates` | tenant member | — | `200` `{items[]: {template_key, panel_count, layout, registry_version}}` | — · ⭐ **MIỄN kiểm disable-access** (allowlist Nhóm C — registry là hằng số trong code, ⛔ không thuộc phạm vi project nào) |
| 6 | `GET /v1/pages/{page_id}/emphasis-suggestion` | tenant member | — | `200` `{suggestions[]: {panel_id, beat_type, current_emphasis, suggested_emphasis}, chapter_quota: {full_page_used, full_page_limit, large_used, large_limit}}` | `403 PROJECT_ACCESS_DISABLED` · `404 PAGE_NOT_FOUND` |

> [!IMPORTANT]
> ⭐ **Năm endpoint `#1`–`#4`, `#6` là "đường đọc/ghi NỘI DUNG trong phạm vi project"** ⇒ **đều** trả `403 PROJECT_ACCESS_DISABLED` khi project ở `disabled_by_takedown`. Chúng định danh bằng `page_id` và ⛔ **không** mang `project_id` trên path ⇒ phải **resolve ngược lên project** rồi mới kiểm cờ (`C3-K1`).
> Luật ở [`API-PRJ-4`](./Endpoint-Project.md#invariant-của-resource) — ⛔ file này **không chép lại**, chỉ trỏ theo mã: đi qua **đúng một** hàm dùng chung ở tầng service (`C3-K3`), **fail-closed** khi ⛔ không thấy row `public.project_access_state` (`C3-K2`). Cưỡng chế bằng **test bảng route toàn cục** khuôn `M1-1`, ⛔ **không** test per-endpoint (`C3-K4`). Danh sách đóng: [Threat Model §4.4](../Security/Spec-Security-Threat-Model.md#44--c-3-danh-sách-đóng-các-đường-đọc-phải-kiểm-cờ-disable-access).
> ⚠️ `#5` là phần tử **allowlist Nhóm C** — allowlist là **HẰNG SỐ trong repo**, thêm phần tử phải qua **review bảo mật** (`C3-K5`), ⛔ không qua PR sửa test.

⚠️ **Sáu endpoint, ⛔ không phải bảy.** [findings/architect §4.1](../../010-Planning/pm-runs/2026-08-28-phase-2-architecture-design-comic-studio/findings/architect.md) đếm **7** cho resource này với nhãn `[EM]` (*"⛔ không phải contract đã chốt"*). Chênh lệch được giải thích ở [§5](#5-endpoint--không-có--và-đó-là-chủ-ý), ⛔ không im lặng.

---

## 4. Chi tiết các endpoint có ràng buộc

### 4.1 Ba endpoint ghi (`#2`, `#3`, `#4`) — cùng một hợp đồng `T1`

⭐ **Cả ba đổi diện tích panel** ⇒ cùng đi qua **một** trình tự bắt buộc, ⛔ không endpoint nào được bỏ bước:

| Bước | Nội dung | Neo |
|:--:|---|---|
| 1 | Ghi `comic.page.page_layout` — toạ độ **0–1**, ⛔ không pixel | `INV-5` · `D-22` |
| 2 | **Tính lại `comic.panel.text_budget`** cho mọi panel đổi diện tích | `D-33` `T1` · `BR-003-12` |
| 3 | ⭐ **Reset gate 2** của **mọi `dialogue_line` thuộc panel bị ảnh hưởng** — bằng `DELETE FROM comic.human_gate_state` | `SDD-HG-01.5` · `INV-7` của [`DB-Entity-Dialogue-And-Gate.md`](../Schema/DB-Entity-Dialogue-And-Gate.md) |
| 4 | Ghi `public.change_log` | [ADR-017 `Q2`](../Architecture/ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md) |
| 5 | **Bốn bước trên nằm trong MỘT transaction**, boundary **per-request** | [ADR-017 `Q4.3`](../Architecture/ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md) `P-2` |
| 6 | ⭐ **Trả `gates_reset[]` trong response** | `SDD-HG-01` **hệ quả #4** |

```json
"gates_reset": [
  { "dialogue_line_id": "…", "panel_id": "…", "gate_kind": "dialogue_condensation" }
],
"text_budget_changed": [
  { "panel_id": "…", "text_budget_before": 42, "text_budget_after": 28 }
]
```

> [!WARNING]
> ⛔ **Reset im lặng là một lỗi contract, ⛔ không phải một tối ưu UX.** `SDD-HG-01` hệ quả #4 ghi nguyên văn: người dùng **phải biết** trang vừa rời trạng thái xuất bản được. Một response `200 OK` trống rỗng sau khi apply template = đúng thứ bị cấm.
> ⚠️ Và: reset ⛔ **không phải trường hợp biên** — [ADR-013](../Architecture/ADR-013-Typeset-Layer-Separate-From-Art.md) gọi nó là *"một vòng lặp bình thường của luồng biên tập"*.

**Ánh xạ `action_type` của `change_log`** — danh mục **đóng**:

| Endpoint | `action_type` | Trạng thái |
|---|---|---|
| `#2 apply-template` | `change_page_template` | ✅ giá trị có sẵn |
| `#3 swap` | `swap_panel` | ✅ giá trị có sẵn |
| `#4 reorder` | ⭐ `reorder_panel` | ✅ **Giá trị RIÊNG**, mở bởi **phán quyết BA lô `L29`** (`T-CL-REORDER-PANEL`, [`DB-Entity-Provenance-And-Usage.md`](../Schema/DB-Entity-Provenance-And-Usage.md)). ⛔ **KHÔNG dùng `swap_panel`**: `#3` đổi chỗ **đúng hai** panel, `#4` là **hoán vị đầy đủ N** panel — ghi cái sau bằng `swap_panel` là **hạ thấp** đóng góp *selection & arrangement* mà `KC-2` cần chứng minh. Mỏ neo: `UC-08` bước 7 liệt *chọn template · swap panel · **reorder*** là **ba** thao tác riêng, mỗi thao tác **một** row. ⚠️ Cách đọc cũ dựa vào [BA findings §1.4](../../010-Planning/pm-runs/2026-08-28-phase-2-architecture-design-comic-studio/findings/business-analyst.md) gộp *"Swap/reorder panel"* — nhưng đó là gộp **hạng mục công việc**, ⛔ **không** phải gộp **ngữ nghĩa bằng chứng**; BA đã đính chính ở `L29`. ⚠️ Một thao tác của người = **MỘT** row, ⛔ không phân rã thành N row `swap_panel` |

### 4.2 `#2 apply-template` — template là **copy**, ⛔ không phải liên kết

| Mã | Quy tắc | Nội dung |
|---|---|---|
| `LT-1` | Một hình dạng JSON | Preset dùng **đúng cùng** hình dạng với `page_layout`, toạ độ 0–1. ⛔ Không tầng dịch, ⛔ không renderer thứ hai |
| `LT-2` | ⭐ **Apply = materialize** | Endpoint **COPY** preset vào `page.page_layout`. Đường render ⛔ **không bao giờ** đọc registry — nó chỉ đọc `page_layout` |
| `LT-3` | `applied_template_key` chỉ để provenance | ⛔ **Không FK**, ⛔ không cột nào của đường render phụ thuộc nó |
| `LT-4` | Sửa hằng số preset ⛔ **không** làm trôi page đã apply | Là **tính chất**, không phải hệ quả phụ — bố cục đã materialize |

`409 TEMPLATE_PANEL_COUNT_MISMATCH`: preset có `k` ô mà page có `n ≠ k` panel. `[Kiến trúc suy luận]` — ⛔ **không tự thêm/bớt panel để cho vừa**; thêm/bớt panel là `split`/`merge`, thuộc [`Endpoint-Panel-Script.md`](./Endpoint-Panel-Script.md).

### 4.3 `#4 reorder` — `panel_index` và `page_layout` phải đi cùng nhau

`comic.panel.panel_index` là **thứ tự đọc**, có UNIQUE `(tenant_id, page_id, panel_index)`. ⇒ Request là **hoán vị đầy đủ**: thiếu hoặc thừa một `panel_id` ⇒ `422 REORDER_NOT_A_PERMUTATION`. ⛔ **Không** nhận hoán vị bộ phận rồi *"tự suy phần còn lại"* — đó là chỗ sinh trạng thái trung gian vi phạm UNIQUE.

### 4.4 `#5 GET layout-templates` — đọc registry TRONG CODE, ⛔ không phải bảng

| Điều | Nội dung |
|---|---|
| ⭐ **Nguồn dữ liệu** | **Hằng số versioned trong code (seed)** — ⛔ **không truy vấn DB**, vì ⛔ **không tồn tại bảng `comic.layout_template`** ([`DB-Entity-Comic-IR.md`](../Schema/DB-Entity-Comic-IR.md)) |
| **Hệ quả về tenant** | Danh sách preset là **toàn cục**, giống nhau cho mọi tenant ⇒ ⛔ **không có** vế RLS nào để áp ở endpoint này. Vẫn **yêu cầu đăng nhập** — ⛔ không mở thành bề mặt công khai |
| ⛔ **Cấm** | ⛔ **Không có** `POST` / `PATCH` / `DELETE` trên `/v1/layout-templates` — ⛔ không Story nào cho người dùng **tạo** template ([`DB-Entity-Comic-IR.md`](../Schema/DB-Entity-Comic-IR.md) lý do #2) |
| **Validate** | Registry được test CI validate bằng **cùng** hàm `comic.is_normalized_layout()` (`LT-5`) ⇒ `422 LAYOUT_COORDS_NOT_NORMALIZED` ở `#2` là **lưới an toàn**, ⛔ không phải đường kiểm chính |
| ⚠️ **Điều kiện đảo** | Xuất hiện requirement *"người dùng tự tạo/lưu template"* hoặc template **theo tenant** ⇒ thêm bảng `comic.layout_template` + RLS và nâng `applied_template_key` thành FK. ⛔ Chưa mở |

### 4.5 `#6 emphasis-suggestion` — đề xuất, ⛔ không phải quyết định

⚠️ `[Kiến trúc suy luận]` — mỏ neo: [BA findings §1.4](../../010-Planning/pm-runs/2026-08-28-phase-2-architecture-design-comic-studio/findings/business-analyst.md) `UC-08` **bước 2** (*"Lấy đề xuất phân bổ diện tích"*), một bước ⛔ chưa file API nào sở hữu.

| Điều | Nội dung |
|---|---|
| **Read-only tuyệt đối** | Endpoint ⛔ **không ghi** gì; ⛔ không sinh `change_log`; ⛔ không đổi `page_layout` |
| ⭐ **⛔ Không LLM ở runtime của endpoint này** | `emphasis` đã được **code phân bổ theo quota** lúc sinh panel script ([ADR-012](../Architecture/ADR-012-Comic-IR-Spec-As-Primary-Data.md) điều 7: *"LLM chỉ xếp hạng beat — CODE phân bổ quota"*). Endpoint chỉ **đọc lại** trạng thái đó + quota còn lại |
| **Quota** | *"tối đa 1 full page + 2–3 large panel"* mỗi chapter là **cấu hình**, ⛔ không hard-code, ⛔ không `CHECK` (`INV-10`) ⇒ response trả cả `*_used` và `*_limit`, ⛔ không chỉ trả *"còn/hết"* |
| ⛔ **Cấm** | ⛔ **Không trả điểm số thực** cho bố cục dưới bất kỳ tên nào (`score`, `weight`, `rank_value`…) — `D-24`, `SRS-NFR-22`, `INV-7`. ⚠️ `D-24` cắt **CƠ CHẾ**, giữ **MỤC TIÊU**: mục tiêu *"layout phản ánh narrative importance"* được đáp ứng bằng `beat_type` + quota, ⛔ không bằng vector 5 số thực |

---

## 5. Endpoint ⛔ KHÔNG có — và đó là chủ ý

| Endpoint vắng mặt | Vì sao ⛔ không ở đây | Ở đâu / trạng thái |
|---|---|---|
| ⭐ `POST /v1/pages/{page_id}/preview` — **request preview** | ⛔ **Không đặc tả hai lần.** Vòng đời preview artifact (`comic.preview_render`) và compositor **dùng chung** cho preview + export (`D-32`) thuộc một file khác | [`Endpoint-Preview-Export.md`](./Endpoint-Preview-Export.md). ⚠️ Mang theo `SDD-HG-01` **hệ quả #2**: **preview ⛔ KHÔNG bị chặn bởi gate** — người dùng phải preview được **trước** khi gate PASS, đó chính là cách họ đi tới PASS |
| ⭐ `PUT /v1/pages/{page_id}/layout` — **ghi hình học TỰ DO** | **Hai căn cứ độc lập.** (a) ⛔ **Không bước UC nào** yêu cầu kéo/chỉnh hình học tự do: `UC-08` ghi `page_layout` là **hiệu ứng** của bước 3 (template) và bước 4 (swap/reorder). (b) Editor hình học tự do là **canvas editor** — seam `S-6` `[OoH]` của [SDD §8.2](../Architecture/SDD-Comic-Studio.md), ⛔ ngoài horizon | ⛔ **Không mở ở MVP0–MVP2.** ⚠️ Seam đã chừa sẵn: toạ độ **0–1** (⛔ không pixel tuyệt đối) ⇒ mở canvas về sau chỉ **thay lớp tương tác**, ⛔ không migrate dữ liệu |
| `POST/PATCH/DELETE /v1/layout-templates` | ⛔ Không requirement nào cho người dùng tạo template; registry là **hằng số trong code** | [§4.4](#44-5-get-layout-templates--đọc-registry-trong-code--không-phải-bảng) |

⚠️ **Ghi chú về `PUT layout`**: kể cả khi có nhu cầu, nó ⛔ **chưa đặc tả được** — danh mục `action_type` đóng của `public.change_log` ⛔ không có giá trị nào cho *"sửa hình học tự do"*. Một endpoint ghi mà `change_log` bắt buộc của nó ⛔ không có `action_type` hợp lệ thì ⛔ **không phải một endpoint in-horizon**.

---

## 6. Invariant của resource

| Mã | Invariant | Neo |
|---|---|---|
| `API-PL-1` | ⭐ **`page.page_layout` là nơi lưu duy nhất của bố cục.** ⛔ Không endpoint nào ghi bố cục vào chỗ khác; ⛔ không response nào trả bố cục từ nguồn thứ hai | `D-22` · `INV-6` của [`DB-Entity-Comic-IR.md`](../Schema/DB-Entity-Comic-IR.md) |
| `API-PL-2` | ⭐ **Mọi toạ độ trong request/response là `0–1`**, ⛔ không pixel | `INV-5` · `S-6` |
| `API-PL-3` | ⭐ **Mọi endpoint đổi diện tích PHẢI trả `gates_reset[]`**; ⛔ không reset im lặng | `SDD-HG-01` hệ quả #4 · `SDD-HG-01.5` |
| `API-PL-4` | ⛔ **Không endpoint nào GHI trạng thái gate.** Reset là `DELETE` **hệ quả tự động**, ⛔ không phải tuỳ chọn của người dùng; ⛔ không có param `keep_gates` | `SDD-HG-01.2`, `.5` · `INV-7` của [`DB-Entity-Dialogue-And-Gate.md`](../Schema/DB-Entity-Dialogue-And-Gate.md) |
| `API-PL-5` | ⛔ **Không tham số nào bỏ qua gate** — không query param, không header, không body field, không role | `SDD-HG-01` hệ quả #1 · `SDD-HG-01.4` |
| `API-PL-6` | Apply template = **COPY** vào `page_layout`; `applied_template_key` **chỉ provenance**, ⛔ không FK | `LT-2`, `LT-3` |
| `API-PL-7` | ⛔ **Không bảng `layout_template`** ⇒ ⛔ không endpoint ghi registry; đường render ⛔ không đọc registry | [`DB-Entity-Comic-IR.md`](../Schema/DB-Entity-Comic-IR.md) |
| `API-PL-8` | ⛔ **Không điểm số thực cho bố cục** trong bất kỳ request/response nào | `D-24` · `SRS-NFR-22` · `INV-7` |
| `API-PL-9` | Ghi `page_layout` + tính lại `text_budget` + reset gate + `change_log` nằm trong **MỘT** transaction, boundary **per-request** | [ADR-017 `Q2`, `Q4.3` `P-2`](../Architecture/ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md) |
| `API-PL-10` | ⛔ **Không endpoint nào gọi copyright/similarity detection** | `SRS-NFR-15` |
| `API-PL-11` | ⛔ **Không endpoint nào trong file này enqueue `public.job`** — danh mục `job_type` đóng có đúng một giá trị `generate_panel` | [`DB-Entity-Job-Queue.md`](../Schema/DB-Entity-Job-Queue.md) |
| `API-PL-12` | ⭐ **`text_budget` là dẫn xuất** — ⛔ không request nào set trực tiếp. `text_budget` `NULL` ⇒ ⛔ chưa được chạy condensation (`SRS-FR-15`) | `INV-6` của [`DB-Entity-Dialogue-And-Gate.md`](../Schema/DB-Entity-Dialogue-And-Gate.md) |
| `API-PL-13` | ⭐ **`#1`–`#4`, `#6` kiểm cờ disable-access** ⇒ `disabled_by_takedown` (hoặc ⛔ thiếu row trạng thái) ⇒ `403 PROJECT_ACCESS_DISABLED`. ⚠️ **Ngoại lệ đúng một**: `#5 GET /v1/layout-templates` thuộc allowlist Nhóm C | [`API-PRJ-4`](./Endpoint-Project.md#invariant-của-resource) · [Threat Model §4.4](../Security/Spec-Security-Threat-Model.md#44--c-3-danh-sách-đóng-các-đường-đọc-phải-kiểm-cờ-disable-access) (`C3-K1`…`C3-K5`) |

---

## 7. UC nào tiêu thụ

| UC | Bước | Endpoint |
|---|---|---|
| `UC-08` | b1 — đọc `page_layout` + panel theo thứ tự đọc | `#1` |
| `UC-08` | b2 — lấy đề xuất phân bổ diện tích | `#6` |
| `UC-08` | b3 — chọn template | `#5` (liệt kê) → `#2` (áp dụng) |
| `UC-08` | b4 — swap / reorder panel | `#3`, `#4` |
| `UC-08` | b5 — ghi `page_layout` toạ độ 0–1 | hiệu ứng của `#2`, `#3`, `#4` — ⛔ **không** một endpoint ghi tự do ([§5](#5-endpoint--không-có--và-đó-là-chủ-ý)) |
| `UC-08` | b6 — ghi `change_log` | hiệu ứng của `#2`, `#3`, `#4` ([§4.1](#41-ba-endpoint-ghi-2-3-4--cùng-một-hợp-đồng-t1) bước 4) |
| `UC-08` | b7 — 🔒 tính lại `text_budget` + reset gate 2 | hiệu ứng của `#2`, `#3`, `#4` ([§4.1](#41-ba-endpoint-ghi-2-3-4--cùng-một-hợp-đồng-t1) bước 2–3, 6) |
| `UC-08` | b8 — kiểm `text_safe_zone` | đọc qua `#1`; ghi thuộc [`Endpoint-Panel-Script.md`](./Endpoint-Panel-Script.md) |
| `UC-08` | b9–b10 — yêu cầu preview, render composite server-side | ⛔ **không** ở file này — [`Endpoint-Preview-Export.md`](./Endpoint-Preview-Export.md) |
| `UC-05` | b2 — 🔒 tính `text_budget` từ diện tích panel | hiệu ứng của `#2`, `#3`, `#4` — ⭐ điều kiện tiên quyết để `UC-05` chạy được |
| `UC-07` | EX-2 đường (c) — cấp cho panel diện tích lớn hơn ⇒ kích hoạt lại `T1` | `#2`, `#3`, `#4` |

---

## 8. `TBD` còn lại — ⛔ không được bịa

| Mã | Khoảng trống | Ai đóng | Khi nào |
|---|---|---|---|
| ~~`T-PL-REORDER-CL`~~ ⇒ ✅ **ĐÃ ĐÓNG** bởi **phán quyết BA lô `L29`**: `#4 reorder` dùng giá trị **RIÊNG** `reorder_panel`, ⛔ **không** tái dụng `swap_panel`. Danh mục `action_type` của [`DB-Entity-Provenance-And-Usage.md`](../Schema/DB-Entity-Provenance-And-Usage.md) đã mở giá trị này ⇒ hai tầng **khớp nhau**. ⛔ Không còn hành vi nào của file này bị chặn bởi hàng này | — (đã đóng) | — |
| `T-PL-BUDGET-UNIT` | **Đơn vị của `text_budget`** (ký tự hay từ) và **hàm tính từ diện tích** — hàng đã đăng ký ở [`DB-Entity-Comic-IR.md`](../Schema/DB-Entity-Comic-IR.md). ⭐ **Hàm tính PHỤ THUỘC metric của font render** ⇒ phải đóng **SAU** `TBD-FONT` của [`ADR-013`](../Architecture/ADR-013-Typeset-Layer-Separate-From-Art.md) §*Thứ tự đóng hai `TBD`*. ⚠️ Đóng ngược thứ tự ⇒ hàm phải calibrate lại ⇒ `text_budget` đổi ⇒ **reset gate #2**, mà ⛔ **không trigger nào bắt được** vì diện tích panel ⛔ không đổi *(phần **đơn vị** thì ⛔ không phụ thuộc font — chốt độc lập được)* | **BA + Architect** | Trước gate `M2-3`, ⭐ **sau `G1-e`** |
| `T-PL-AFFECTED` | Quy tắc xác định *"panel bị ảnh hưởng"* khi apply template: mọi panel của page, hay chỉ panel có diện tích thực sự đổi. ⚠️ Chọn sai theo chiều rộng ⇒ reset thừa (phiền); theo chiều hẹp ⇒ **để lọt một gate PASS trên `text_budget` cũ** — đúng thứ `INV-6` của [`DB-Entity-Dialogue-And-Gate.md`](../Schema/DB-Entity-Dialogue-And-Gate.md) dò được. ⛔ Lô này không tự chọn | **Architect + Engineer** | Trước khi hiện thực `#2` |
| `T-API-ERR` | ⭐ Chuẩn `error_code` + error envelope (⛔ **chưa chốt**). ✅ **Tiền tố đường dẫn đã chốt `/v1/…`** (lô `L28a`) — chi tiết ở [`Endpoint-Panel-Script.md`](./Endpoint-Panel-Script.md) | **Architect** (một lô quét toàn thư mục) | Trước file API đầu tiên được implement |

---

## 9. Tài liệu tham khảo

- [SDD Comic Studio](../Architecture/SDD-Comic-Studio.md) — §5.1 `F3`, §5.3, §6.3, §8.2 `S-6`
- [ADR-012 — Comic IR: spec là dữ liệu chính, ảnh chỉ là output](../Architecture/ADR-012-Comic-IR-Spec-As-Primary-Data.md)
- [ADR-013 — Typeset layer tách khỏi art](../Architecture/ADR-013-Typeset-Layer-Separate-From-Art.md)
- [ADR-017 — Chuỗi provenance và MỘT transaction boundary](../Architecture/ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md)
- [`DB-Entity-Comic-IR.md`](../Schema/DB-Entity-Comic-IR.md) · [`DB-Entity-Dialogue-And-Gate.md`](../Schema/DB-Entity-Dialogue-And-Gate.md) · [`DB-Entity-Provenance-And-Usage.md`](../Schema/DB-Entity-Provenance-And-Usage.md)
- [UC-08 — Arrange Page And Preview](../../020-Requirements/Use-Cases/UC-08-Arrange-Page-And-Preview.md)
