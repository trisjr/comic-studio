---
id: SPEC-API-HUMAN-GATES
type: spec
status: draft
project: comic-studio
created: 2026-08-29
---

# Endpoint: Human Gates (speaker attribution + dialogue condensation)

Bề mặt API của **hai human gate**. Hai gate ở chung một file vì `M2-4` là **thuộc tính của cả hai**: `UC-04` bước 9 ghi nguyên văn *"hai gate chỉ **xong** CÙNG NHAU"* — tách file là mất đúng ràng buộc quan trọng nhất.

> [!IMPORTANT]
> ⭐⭐ **File này đặc tả BỀ MẶT API của gate — ⛔ KHÔNG đặc tả LUẬT của gate.**
> Luật (định nghĩa gate, mặc định `OPEN`, ai được ghi `PASS`, điều kiện chặn export, quy tắc reset, `change_log`, bảo toàn `dialogue_source`) có **nguồn DUY NHẤT** là [SDD §6.3 `SDD-HG-01`](../Architecture/SDD-Comic-Studio.md).
> ⇒ Mọi chỗ cần luật, file này **trỏ bằng mã điều khoản** (`SDD-HG-01.1`…`.7`). ⛔ **Không chép nội dung.** Nếu SDD §6.3 đổi, file này ⛔ **không được** trở thành một phiên bản lệch.

**Decided in:**

- [SDD Comic Studio](../Architecture/SDD-Comic-Studio.md) — ⭐ §6.3 `SDD-HG-01` (**nguồn duy nhất**), §5.3
- [ADR-013 — Typeset layer tách khỏi art](../Architecture/ADR-013-Typeset-Layer-Separate-From-Art.md) — `D-28` (hai field thoại), `D-33` (`T1`/`T2`)
- [ADR-017 — Chuỗi provenance và MỘT transaction boundary](../Architecture/ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md) — `Q2`, `Q4.3` `P-2` (hàng `Endpoint-*` của `Q4.7`)
- [ADR-008 — LLM provider và ranh giới sử dụng](../Architecture/ADR-008-LLM-Provider-And-Usage-Boundaries.md) — bước nén thoại
- [ADR-006 — RLS & tenant context injection](../Architecture/ADR-006-RLS-Tenant-Context-Injection.md)
- [`DB-Entity-Dialogue-And-Gate.md`](../Schema/DB-Entity-Dialogue-And-Gate.md) — ⭐ nguồn chuẩn tên bảng/cột, `INV-1`…`INV-11`, *"hai câu ghi chuẩn tắc"*
- [`DB-Entity-Comic-IR.md`](../Schema/DB-Entity-Comic-IR.md) — `comic.panel.text_budget`

---

## 1. Resource

| Resource | Bảng DB | Ghi chú |
|---|---|---|
| Dòng thoại | `comic.dialogue_line` | ⭐ **HAI field thoại**: `dialogue_source` (**BẤT BIẾN**) + `dialogue_rendered` (người sửa được) |
| Sự kiện `PASS` đang có hiệu lực | `comic.human_gate_state` | ⭐ **Row tồn tại ⇔ `PASS`; row vắng mặt ⇔ `OPEN`.** ⛔ Không cột `state` |
| Trạng thái gate mức page | ⛔ **không bảng nào** | ⭐ Giá trị **dẫn xuất**, ⛔ không materialize (`INV-9`) |

**Hai `gate_kind` — danh mục đóng bằng `CHECK`**: `speaker_attribution` · `dialogue_condensation`. ⛔ Không giá trị thứ ba.

---

## 2. Quy ước chung — ⛔ file này KHÔNG đặc tả lại bốn ràng buộc xuyên-endpoint

| Mã | Ràng buộc | Nguồn **DUY NHẤT** | File này được làm gì |
|---|---|---|---|
| `SDD-HG-01` | Hai human gate | [SDD §6.3](../Architecture/SDD-Comic-Studio.md) | ⭐ Hiện thực hoá **5 hệ quả bắt buộc cho file API** thành route/param/field/mã lỗi — xem [§5](#5-invariant-của-resource). ⛔ Không chép điều khoản |
| `KC-4` | Artifact + bằng chứng, **một** transaction | [ADR-017 `Q4`](../Architecture/ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md) | Trỏ `Q2` + `Q4.3` `P-2`. ⛔ Không viết *"tầng DB cưỡng chế `KC-4`"* (`Q4.6`) |
| `CT-POLL-2S` | Polling **2 giây**, ⛔ không WebSocket. Độ rắn **MẶC ĐỊNH**, ⛔ không nâng thành `CHỐT` | [ADR-015 `Q6`](../Architecture/ADR-015-Job-Queue-In-Postgres.md) | ⛔ **Không endpoint nào ở đây là async** — kể cả `#3` gọi LLM ([§4.3](#43-3-dialoguecondense--gọi-llm-nhưng--không-ghi-gì)) |
| RLS + tenant context | Mọi query qua RLS với `app.current_tenant` | [ADR-006](../Architecture/ADR-006-RLS-Tenant-Context-Injection.md) | Cột `Auth`; ⚠️ `#5` còn đòi **định danh người dùng thật** — xem [§4.5](#45-5-gatespass---đường-duy-nhất-ghi-pass) |

**Quy ước mã lỗi**: `HTTP status` + `error_code` `SCREAMING_SNAKE` ổn định (`T-API-ERR`).

> [!CAUTION]
> ⛔ **`SRS-NFR-15` — ⛔ KHÔNG endpoint nào trong file này gọi copyright/similarity detection.** Anti-feature **có chủ ý**.

---

## 3. Danh sách endpoint

| # | Method · Path | Auth | Request | Response | Mã lỗi |
|--:|---|---|---|---|---|
| 1 | `GET /v1/panels/{panel_id}/dialogue-lines` | tenant member | — | `200` `{items[]: DialogueLine, panel: {text_budget, text_budget_unit}}` | `403 PROJECT_ACCESS_DISABLED` · `404 PANEL_NOT_FOUND` |
| 2 | `PATCH /v1/dialogue-lines/{id}/speaker` | tenant member | `{speaker_id: uuid \| null}` — ⭐ `null` ≡ **`UNKNOWN`**, giá trị **hợp lệ** | `200` `{dialogue_line}` | `403 PROJECT_ACCESS_DISABLED` · `403 FIELD_NOT_WRITABLE` · `404 DIALOGUE_LINE_NOT_FOUND` · `422 BIBLE_ENTITY_NOT_FOUND` · `409 SPEAKER_LOCKED_BY_PASSED_GATE` ⚠️ **blocked-by-TBD** |
| 3 | `POST /v1/panels/{panel_id}/dialogue:condense` | tenant member | `{}` | `200` `{proposals[]: {dialogue_line_id, dialogue_source, proposed_rendered, fits_budget, is_locked}}` | `403 PROJECT_ACCESS_DISABLED` · `404 PANEL_NOT_FOUND` · `409 TEXT_BUDGET_NOT_COMPUTED` · `502 LLM_PROVIDER_ERROR` |
| 4 | `PATCH /v1/dialogue-lines/{id}/rendered` | tenant member | `{dialogue_rendered: string}` | `200` `{dialogue_line, gates_reset[]}` | `403 PROJECT_ACCESS_DISABLED` · `403 FIELD_NOT_WRITABLE` · `404 DIALOGUE_LINE_NOT_FOUND` · `409 TEXT_BUDGET_NOT_COMPUTED` |
| 5 | `POST /v1/dialogue-lines/{id}/gates/{gate_kind}:pass` | ⭐ tenant member — **người dùng thật** | `{}` | `201` `{dialogue_line_id, gate_kind, passed_by_user_id, passed_at, text_budget_at_pass, page_gate_summary}` | `400 BATCH_GATE_PASS_NOT_ALLOWED` · `403 PROJECT_ACCESS_DISABLED` · `403 SERVICE_ACTOR_NOT_ALLOWED` · `404 DIALOGUE_LINE_NOT_FOUND` · `409 GATE_ALREADY_PASSED` · `409 TEXT_BUDGET_NOT_COMPUTED` · `422 UNKNOWN_GATE_KIND` |
| 6 | `GET /v1/pages/{page_id}/gate-status` | tenant member | — | `200` `{page_id, dialogue_line_total, per_gate: {speaker_attribution: {passed, open}, dialogue_condensation: {passed, open}}, blocking_lines[]}` | `403 PROJECT_ACCESS_DISABLED` · `404 PAGE_NOT_FOUND` |

⭐ **Sáu endpoint, và ⛔ KHÔNG có endpoint thứ bảy** — xem [§6](#6-endpoint--không-có--và-đó-là-điểm-của-file-này).

> [!IMPORTANT]
> ⭐ **Cả sáu endpoint là "đường đọc/ghi NỘI DUNG trong phạm vi project"** ⇒ **đều** trả `403 PROJECT_ACCESS_DISABLED` khi project ở `disabled_by_takedown`. Chúng định danh bằng `panel_id` / `dialogue_line_id` / `page_id` và ⛔ **không** mang `project_id` trên path ⇒ phải **resolve ngược lên project** rồi mới kiểm cờ (`C3-K1`).
> Luật ở [`API-PRJ-4`](./Endpoint-Project.md#invariant-của-resource) — ⛔ file này **không chép lại**, chỉ trỏ theo mã: đi qua **đúng một** hàm dùng chung ở tầng service (`C3-K3`), **fail-closed** khi ⛔ không thấy row `public.project_access_state` (`C3-K2`). Cưỡng chế bằng **test bảng route toàn cục** khuôn `M1-1`, ⛔ **không** test per-endpoint (`C3-K4`). Danh sách đóng: [Threat Model §4.4](../Security/Spec-Security-Threat-Model.md#44--c-3-danh-sách-đóng-các-đường-đọc-phải-kiểm-cờ-disable-access).
> ⚠️ Kiểm cờ chạy **trước** mọi kiểm gate và mọi kiểm field ⇒ `#5 gates:pass` **⛔ không PASS được** trên project đang bị hạ. ⛔ Đây ⛔ **không** phải một `admin_override` mới — nó là **thêm một điều kiện chặn**, ⛔ không phải một đường mở.

---

## 4. Chi tiết các endpoint có ràng buộc

### 4.1 `DialogueLine` — field ghi được và field ⛔ BẤT BIẾN

| Field | Ghi được qua API? | Cưỡng chế |
|---|:--:|---|
| `dialogue_source` · `source_span` | ⛔ **KHÔNG** | ⭐ **Quyền mức cột ở tầng DB**: hai cột này ⛔ không nằm trong danh sách `GRANT UPDATE` ⇒ mọi `UPDATE` chạm chúng **bị DB từ chối** (`INV-1`). API trả `403 FIELD_NOT_WRITABLE` **trước** khi tới DB — ⛔ hai lớp, ⛔ không lớp nào thay lớp kia. Neo: `SDD-HG-01.7` |
| `dialogue_rendered` | ✅ qua `#4` | Ghi ⇒ `is_human_edited = true` |
| `is_human_edited` | ⛔ trực tiếp | ⭐ **Cờ khoá** do `#4` đặt. ⛔ Không endpoint nào **hạ** cờ — hạ cờ = mở lại đường re-run ghi đè công người dùng (`INV-2`, `SDD-HG-01.7`) |
| `speaker_id` | ✅ qua `#2` | `NULL` ≡ `UNKNOWN` — ⛔ **không** cột thứ ba, ⛔ không sentinel |
| `speaker_confidence` | ⛔ | Do bước gán tự động ghi. Response **luôn** trả kèm để UI **hiện cờ khi thấp** (`SDD-HG-01.3`) |
| Trạng thái gate | ⛔ | Dẫn xuất từ sự tồn tại row `comic.human_gate_state`; ghi **chỉ** qua `#5` |

⭐ **Cách phân biệt *"chưa gán"* với *"người đã quyết là UNKNOWN"***: bằng **chính sự tồn tại của row gate 1** (`INV-5`), ⛔ không bằng một field bổ sung. ⇒ Response của `#1` trả **cả hai** `speaker_id` và trạng thái gate 1 của cùng dòng; client ⛔ không được suy một cái từ cái kia.

### 4.2 `#2 PATCH speaker` — ⚠️ một hành vi CÒN MỞ, ⛔ không tự quyết

| Điều | Nội dung |
|---|---|
| Ghi được | `speaker_id` (uuid hoặc `null`) |
| `change_log` | ⭐ `action_type = 'assign_speaker'` — ⛔ **KHÔNG phải `edit_dialogue`**. ✅ Đóng bởi **phán quyết BA lô `L29`** (`T-CL-SPEAKER`, [`DB-Entity-Provenance-And-Usage.md`](../Schema/DB-Entity-Provenance-And-Usage.md)): endpoint này ⛔ **không chạm nội dung thoại**, nên một row `edit_dialogue` sẽ **nói sai việc đã xảy ra**; và `UC-04` `ALT-3` đòi việc sửa nội dung sinh `change_log` **RIÊNG** ⇒ hai hành động ⛔ không được dùng chung một giá trị. Nằm **cùng transaction** với thay đổi ([ADR-017 `Q2`](../Architecture/ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md)) |
| ⛔ **Cấm** | ⛔ Endpoint này **không** ghi `PASS`. Gán speaker và xác nhận gate là **hai hành động khác nhau** (`SDD-HG-01.2`, `.3`) |
| ⚠️ **Blocked-by-TBD** | Sửa `speaker_id` của một dòng **đã PASS gate 1** thì sao? `SDD-HG-01.5` định nghĩa reset **chỉ** cho gate 2 (`T1`, `T2`); ⛔ **không hàng nguồn nào** nói về gate 1. Hai ứng xử ứng viên — ⛔ **lô này không chọn**: **(a)** chặn bằng `409 SPEAKER_LOCKED_BY_PASSED_GATE`; **(b)** cho sửa và reset gate 1 về `OPEN`. ⚠️ Chọn sai theo chiều (b) mà không có luật ⇒ tạo một **vòng lặp duyệt**; theo chiều (a) mà không có luật ⇒ khoá cứng một dữ liệu sai. Hàng `TBD` **đã đăng ký** tại [`DB-Entity-Dialogue-And-Gate.md`](../Schema/DB-Entity-Dialogue-And-Gate.md) — xem [`T-HG-GATE1-RESET`](#8-tbd-còn-lại---không-được-bịa) |

### 4.3 `#3 dialogue:condense` — gọi LLM nhưng ⛔ KHÔNG ghi gì

| Điều | Nội dung |
|---|---|
| ⭐ **⛔ Endpoint này KHÔNG ghi DB** | Nó trả **đề xuất**; người quyết bằng `#4`. Căn cứ cấu trúc: ⛔ **không tồn tại bảng đề xuất** nào trong tầng `Schema/` ⇒ ⛔ không có đích để ghi. ⚠️ Đây là **quyết định**, ⛔ không phải thiếu sót: `dialogue_rendered` là *"bản người duyệt"*, ⛔ không phải *"bản LLM vừa nghĩ ra"* (`D-28`) |
| 🔒 **Thứ tự bắt buộc** | `comic.panel.text_budget IS NULL` ⇒ `409 TEXT_BUDGET_NOT_COMPUTED`. ⭐ Đây là hình thức API của *"condensation chạy SAU layout"* (`SRS-FR-15`); cùng ràng buộc đó còn được cưỡng chế ở tầng DB bởi `INV-6` của [`DB-Entity-Dialogue-And-Gate.md`](../Schema/DB-Entity-Dialogue-And-Gate.md) |
| ⭐ **Tôn trọng cờ khoá** | Dòng có `is_human_edited = true` ⇒ response đánh dấu `is_locked: true` và ⛔ **không** kèm `proposed_rendered`. ⛔ Không đường re-run nào ghi đè bản người đã sửa (`SDD-HG-01.7`, `INV-2`) |
| ⛔ **Không async** | ⛔ Không enqueue `public.job` — danh mục `job_type` đóng có **đúng một** giá trị `generate_panel` ([`DB-Entity-Job-Queue.md`](../Schema/DB-Entity-Job-Queue.md)) ⇒ ⛔ không `job_id`, ⛔ không `CT-POLL-2S` |
| ⛔ **Không PASS** | ⛔ Không có nhánh tự động PASS **kể cả khi bản nén đã vừa budget** (`SDD-HG-01.2`) |
| ⚠️ **Chi phí** | Endpoint gọi LLM ⇒ chi phí thật, nhưng ⛔ **không** nằm trong rate limit `RL-1` (khoá `(tenant_id, action)`, `action ∈ {upload, generate}` — [`DB-Entity-Tenancy.md`](../Schema/DB-Entity-Tenancy.md)). ⛔ Lô này không tự mở rộng danh mục `action` |

### 4.4 `#4 PATCH rendered` — nguồn phát của `T2`

| Bước | Nội dung | Neo |
|:--:|---|---|
| 1 | Ghi `dialogue_rendered`, đặt `is_human_edited = true` | `D-28` · `INV-2` |
| 2 | ⭐ **Reset gate 2 của ĐÚNG DÒNG ĐÓ** — `DELETE FROM comic.human_gate_state WHERE … AND gate_kind = 'dialogue_condensation'`. ⛔ **Không lan sang dòng khác** | `SDD-HG-01.5` (`T2`) · `INV-7` |
| 3 | Ghi `change_log` `action_type = 'edit_dialogue'` | [ADR-017 `Q2`](../Architecture/ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md) |
| 4 | Ba bước trên trong **MỘT** transaction, boundary **per-request** | [ADR-017 `Q4.3`](../Architecture/ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md) `P-2` |
| 5 | ⭐ Trả `gates_reset[]` — ⛔ **không reset im lặng** | `SDD-HG-01` hệ quả #4 |

⚠️ **Sửa thoại TRƯỚC khi gate 2 chạy lần đầu** ⇒ `gates_reset[]` **rỗng** (⛔ không có gì để reset) — nhưng bản do người viết **vẫn phải đi qua `#5`**. ⛔ Không có nhánh tự động PASS (`ADR-013` `AF-5` của `UC-07`).

⚠️ **Ba lựa chọn của `UC-05` bước 6** ánh xạ thế nào: *"nhận bản nén"* và *"sửa tay"* đều là một lời gọi `#4` với nội dung tương ứng. Lựa chọn thứ ba — *"giữ nguyên bản gốc"* — ⛔ **không nguồn nào nói nó ghi gì vào `dialogue_rendered`** ⇒ [`T-HG-KEEP-SOURCE`](#8-tbd-còn-lại---không-được-bịa). ⛔ Lô này không tự gán ngữ nghĩa.

### 4.5 `#5 gates:pass` — ⭐ ĐƯỜNG DUY NHẤT ghi `PASS`

⭐ **Một endpoint cho CẢ HAI gate**, phân biệt bằng `{gate_kind}` trên path. Lý do: ràng buộc *"chỉ hành động của con người mới chuyển `OPEN → PASS`"* (`SDD-HG-01.2`) phải được cưỡng chế **ở đúng một chỗ**; hai route song song là hai chỗ để lệch.

| Điều | Nội dung | Neo |
|---|---|---|
| **Ghi gì** | `INSERT INTO comic.human_gate_state (tenant_id, dialogue_line_id, gate_kind, passed_by_user_id, passed_at, text_budget_at_pass)` | *"Hai câu ghi chuẩn tắc"* của [`DB-Entity-Dialogue-And-Gate.md`](../Schema/DB-Entity-Dialogue-And-Gate.md) |
| ⭐ **Định danh người thật** | `passed_by_user_id` lấy từ **phiên đăng nhập**, ⛔ **không** từ body. `NOT NULL` + FK `→ public.user` là cưỡng chế nền | `SDD-HG-01.2` · `SDD-HG-01` hệ quả #3 · `INV-3` |
| ⛔ **Actor dịch vụ bị chặn** | Đường `app_worker` / cron / job ⛔ **không** gọi được ⇒ `403 SERVICE_ACTOR_NOT_ALLOWED` | `SDD-HG-01.2` |
| ⭐ **`text_budget_at_pass`** | Bắt buộc **khi và chỉ khi** `gate_kind = 'dialogue_condensation'`; server đọc từ `comic.panel.text_budget`, ⛔ **không** nhận từ client. `text_budget IS NULL` ⇒ `409 TEXT_BUDGET_NOT_COMPUTED` | `INV-6` |
| ⛔ **Cấm batch** | Path nhận **đúng một** `dialogue_line_id`; ⛔ **không** biến thể nhận mảng, ⛔ không `:pass-all`, ⛔ không `?scope=page`. Gửi mảng ⇒ `400 BATCH_GATE_PASS_NOT_ALLOWED` | `UC-04` (cấm batch-approve) · `SDD-HG-01.2` |
| ⛔ **Không câu ghi thứ ba** | PK `(tenant_id, dialogue_line_id, gate_kind)` đã tồn tại ⇒ `409 GATE_ALREADY_PASSED`. ⛔ **Không `UPDATE`, ⛔ không `UPSERT … DO NOTHING`** — *"⛔ không có câu ghi thứ ba"* | [`DB-Entity-Dialogue-And-Gate.md`](../Schema/DB-Entity-Dialogue-And-Gate.md) |
| **`change_log`** | Một row `action_type = 'human_gate_pass'`, commit **cùng transaction** với row gate | `SDD-HG-01.6` · [ADR-017 `Q2`](../Architecture/ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md) |
| ⭐ **Gate 1 PASS với `UNKNOWN` là HỢP LỆ** | `speaker_id IS NULL` ⛔ **không** chặn `#5`. `PASS` nghĩa là *"người đã xem"*, ⛔ không nghĩa là *"hệ thống đã biết"* | `SDD-HG-01.3` · `INV-5` |
| **Response** | Trả kèm `page_gate_summary` để client ⛔ không phải tự suy điều kiện `SDD-HG-01.4` | `SDD-HG-01` hệ quả #5 |

### 4.6 `#6 gate-status` — đọc dẫn xuất, ⛔ không set được

| Điều | Nội dung |
|---|---|
| **Nguồn số** | Đếm `comic.dialogue_line` trong phạm vi page **so với** đếm row `comic.human_gate_state` cho **từng** `gate_kind`; hai con số lệch ⇒ còn `OPEN`. Hình dạng truy vấn thuộc [`DB-Entity-Dialogue-And-Gate.md`](../Schema/DB-Entity-Dialogue-And-Gate.md) |
| ⛔ **Read-only tuyệt đối** | ⛔ Không `PUT`/`PATCH`/`POST` nào trên đường dẫn này. Trạng thái gate mức page là **dẫn xuất**, ⛔ không materialize (`INV-9`) |
| `blocking_lines[]` | Danh sách `dialogue_line_id` đang chặn, kèm `gate_kind` — để người dùng **đi tới `PASS`**, ⛔ không phải để hiển thị một nút bỏ qua |
| ⚠️ **⛔ KHÔNG phải phép kiểm export** | Phép kiểm `SDD-HG-01.4` chạy ở tầng server qua **đúng một** hàm dùng chung, thuộc đường sinh `export_artifact` ([`Endpoint-Preview-Export.md`](./Endpoint-Preview-Export.md)). ⛔ **Không** được dựa vào endpoint này để quyết định cho export — ⛔ và ⛔ không dựa vào việc UI ẩn nút (`SDD-HG-01` hệ quả #2) |

---

## 5. Invariant của resource

⭐ **Năm hàng đầu là hiện thực hoá đúng 5 *"hệ quả bắt buộc cho 14 file API"* của [SDD §6.3](../Architecture/SDD-Comic-Studio.md)** — file này là nơi chúng có hiệu lực dày nhất.

| Mã | Invariant | Điều khoản nguồn |
|---|---|---|
| `API-HG-1` | ⛔ **Không endpoint nào nhận tham số bỏ qua gate** — ⛔ không query param, ⛔ không header, ⛔ không body field, ⛔ không scope/role. ⛔ Không `force`, `skip_gates`, `auto_approve`, `admin_override` | `SDD-HG-01` hệ quả #1 (`.2`, `.4`) |
| `API-HG-2` | ⛔ **Không endpoint nào trong file này sinh `export_artifact`** và ⛔ không endpoint nào ở đây được dùng thay phép kiểm `.4` | `SDD-HG-01` hệ quả #2 (`.4`) |
| `API-HG-3` | Endpoint ghi `PASS` (`#5`) đòi **định danh người dùng thật** và sinh `change_log` **cùng transaction** | `SDD-HG-01` hệ quả #3 (`.2`, `.6`) |
| `API-HG-4` | Endpoint sửa `dialogue_rendered` (`#4`) **trả `gates_reset[]`**; ⛔ không reset im lặng | `SDD-HG-01` hệ quả #4 (`.5`) |
| `API-HG-5` | Mọi response đọc mang trạng thái gate tổng hợp (`#1` mức dòng, `#5`/`#6` mức page) | `SDD-HG-01` hệ quả #5 (`.4`) |
| `API-HG-6` | ⭐ **`#5` là đường DUY NHẤT ghi `PASS`.** ⛔ Không endpoint thứ hai, ⛔ không batch, ⛔ không seed/migration/admin tool | `SDD-HG-01.1`, `.2` |
| `API-HG-7` | ⭐ **⛔ KHÔNG tồn tại endpoint xoá/huỷ `PASS`.** Reset là **hệ quả tự động** của `T1`/`T2`, ⛔ không phải một hành động API | `SDD-HG-01.5` · `INV-7` |
| `API-HG-8` | `dialogue_source` + `source_span` **BẤT BIẾN** qua mọi endpoint; hai lớp chặn: API `403` + quyền mức cột ở DB | `SDD-HG-01.7` · `INV-1` |
| `API-HG-9` | ⭐ `PASS` gate 2 ⛔ **không thể** xảy ra khi `comic.panel.text_budget IS NULL` — cưỡng chế ở **cả** API (`409`) **và** DB (`INV-6`) | `SRS-FR-15` · `INV-6` |
| `API-HG-10` | ⛔ **Không endpoint nào trong file này enqueue `public.job`** | [`DB-Entity-Job-Queue.md`](../Schema/DB-Entity-Job-Queue.md) |
| `API-HG-11` | ⛔ **Không endpoint nào gọi copyright/similarity detection** | `SRS-NFR-15` |
| `API-HG-12` | Mọi đường ghi sinh `change_log` cùng transaction; boundary **per-request** (`P-2`) | [ADR-017 `Q2`, `Q4.3`](../Architecture/ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md) |
| `API-HG-13` | ⭐ **Cả sáu endpoint kiểm cờ disable-access** ⇒ `disabled_by_takedown` (hoặc ⛔ thiếu row trạng thái) ⇒ `403 PROJECT_ACCESS_DISABLED`, **trước** mọi kiểm gate. ⛔ Không endpoint nào của file này nằm trong allowlist miễn kiểm | [`API-PRJ-4`](./Endpoint-Project.md#invariant-của-resource) · [Threat Model §4.4](../Security/Spec-Security-Threat-Model.md#44--c-3-danh-sách-đóng-các-đường-đọc-phải-kiểm-cờ-disable-access) Nhóm B (`C3-K1`…`C3-K4`) |

---

## 6. Endpoint ⛔ KHÔNG có — và đó là ĐIỂM của file này

| Endpoint vắng mặt | Vì sao |
|---|---|
| ⭐ `DELETE /v1/dialogue-lines/{id}/gates/{gate_kind}` | ⛔ **Không tồn tại hành động người dùng *"bỏ PASS"*.** Chỉ có `INSERT` (người) và `DELETE` (hệ quả tự động `T1`/`T2`) — *"⛔ không có câu ghi thứ ba"*. Một endpoint huỷ PASS là **đúng đường bypass** mà `M2-4` đo |
| ⭐ `POST /v1/pages/{page_id}/gates:pass-all` (batch) | ⛔ **Cấm batch-approve** (`UC-04`). Batch biến *"người đã xem từng dòng"* thành một cú click — phá đúng ngữ nghĩa của `PASS` |
| `PATCH /v1/pages/{page_id}/gate-status` | Trạng thái mức page là **dẫn xuất**, ⛔ không materialize ⇒ ⛔ không có gì để ghi (`INV-9`) |
| `POST …:condense` với `auto_accept=true` | ⛔ Không có nhánh tự động PASS **kể cả khi thoại đã vừa budget** (`SDD-HG-01.2`) |

---

## 7. UC nào tiêu thụ

| UC | Bước | Endpoint |
|---|---|---|
| `UC-04` | b1–b3 — tách dòng thoại, sinh đề xuất speaker, đặt mọi dòng ở *"chưa xác nhận"* | Hệ quả của ingest/panel-script; trạng thái *"chưa xác nhận"* = **vắng mặt row** gate 1 (`SDD-HG-01.1`) |
| `UC-04` | b4 — đọc danh sách dòng thoại + đề xuất | `#1` |
| `UC-04` | b5 — xác nhận / gán lại từng dòng | `#2` (gán) → `#5` (xác nhận, `gate_kind = speaker_attribution`) |
| `UC-04` | b6 — đếm dòng *"chưa xác nhận"* | `#6` |
| `UC-04` | b7–b8 — 🔒 cưỡng chế gate ở đường xuất bản | ⛔ **không** ở file này — [`Endpoint-Preview-Export.md`](./Endpoint-Preview-Export.md), qua `SDD-HG-01.4` |
| `UC-05` | b1–b2 — đọc `page_layout`/`text_safe_zone`, 🔒 tính `text_budget` | [`Endpoint-Page-Layout.md`](./Endpoint-Page-Layout.md) |
| `UC-05` | b3 — nạp thoại gốc + speaker đã xác nhận | `#1` |
| `UC-05` | b4 — gọi nén thoại | `#3` |
| `UC-05` | b5 — trình cặp `gốc → nén` | `#3` (response `proposals[]`) |
| `UC-05` | b6 — quyết định 3 lựa chọn / dòng | `#4` (⚠️ lựa chọn *"giữ nguyên bản gốc"* = `T-HG-KEEP-SOURCE`) |
| `UC-05` | b7 — chuyển gate 2 `PASS` | `#5` (`gate_kind = dialogue_condensation`) |
| `UC-05` | b8 — 🔒 mở đường xuất bản khi **cả hai** gate PASS | ⛔ **không** ở file này — `SDD-HG-01.4` |
| `UC-07` | b8 — 🔒 reset gate 2 khi nội dung thoại đổi | `#4` (`T2`) |
| `UC-08` | b7 — 🔒 reset gate 2 khi diện tích đổi | [`Endpoint-Page-Layout.md`](./Endpoint-Page-Layout.md) (`T1`) |

---

## 8. `TBD` còn lại — ⛔ không được bịa

| Mã | Khoảng trống | Ai đóng | Khi nào |
|---|---|---|---|
| `T-HG-GATE1-RESET` | ⭐ **Gate 1 có reset không khi `speaker_id` bị sửa SAU khi đã PASS?** Hàng đã đăng ký tại [`DB-Entity-Dialogue-And-Gate.md`](../Schema/DB-Entity-Dialogue-And-Gate.md); ⚠️ **giờ nó chặn một hành vi API** — `#2` ⛔ không đặc tả hết được (mã `409 SPEAKER_LOCKED_BY_PASSED_GATE` chỉ có hiệu lực ở ứng xử **(a)**) | **PM/BA + Architect** | Trước khi hai Story human gate vào Active Sprint (MVP2) |
| `T-HG-KEEP-SOURCE` | Lựa chọn *"giữ nguyên bản gốc"* của `UC-05` bước 6 ghi gì vào `dialogue_rendered` (copy nguyên văn `dialogue_source`, hay để `NULL`), và nó có đủ điều kiện PASS gate 2 không | **BA + Architect** | Cùng mốc trên |
| `T-HG-BUDGET-UNIT` | **Đơn vị `text_budget`** (ký tự / từ) — response `#1` trả `text_budget_unit` nên ⛔ chưa điền được. Hàng đã đăng ký ở [`DB-Entity-Comic-IR.md`](../Schema/DB-Entity-Comic-IR.md) | **BA + Architect** | Trước gate `M2-3` |
| `T-HG-CONFIDENCE` | Ngưỡng *"thấp"* của `speaker_confidence` để UI hiện cờ — `SDD-HG-01.3` chốt **có cờ**, ⛔ không cho con số | **BA/Founder** sau MVP0 | Trước gate `M2-3` |
| `T-API-ERR` | ⭐ Chuẩn `error_code` + error envelope (⛔ **chưa chốt**). ✅ **Tiền tố đường dẫn đã chốt `/v1/…`** (lô `L28a`) — chi tiết ở [`Endpoint-Panel-Script.md`](./Endpoint-Panel-Script.md) | **Architect** (một lô quét toàn thư mục) | Trước file API đầu tiên được implement |

---

## 9. Tài liệu tham khảo

- ⭐ [SDD Comic Studio §6.3 — `SDD-HG-01`](../Architecture/SDD-Comic-Studio.md) — **nguồn duy nhất của luật gate**
- [ADR-013 — Typeset layer tách khỏi art](../Architecture/ADR-013-Typeset-Layer-Separate-From-Art.md)
- [ADR-017 — Chuỗi provenance và MỘT transaction boundary](../Architecture/ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md)
- [ADR-008 — LLM provider và ranh giới sử dụng](../Architecture/ADR-008-LLM-Provider-And-Usage-Boundaries.md)
- [`DB-Entity-Dialogue-And-Gate.md`](../Schema/DB-Entity-Dialogue-And-Gate.md) · [`DB-Entity-Comic-IR.md`](../Schema/DB-Entity-Comic-IR.md) · [`DB-Entity-Tenancy.md`](../Schema/DB-Entity-Tenancy.md)
- [UC-04 — Human Gate Speaker Attribution](../../020-Requirements/Use-Cases/UC-04-Human-Gate-Speaker-Attribution.md) · [UC-05 — Human Gate Dialogue Condensation](../../020-Requirements/Use-Cases/UC-05-Human-Gate-Dialogue-Condensation.md)
