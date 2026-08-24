---
id: UC-06
type: use-case
status: draft
project: comic-studio
created: 2026-08-24
---

# UC-06 — Sinh panel và chọn variant

> Part of: [Epic-Image-Generation-Pipeline](../../022-User-Stories/Epics/Epic-Image-Generation-Pipeline.md) · [Epic-Minimum-Editor](../../022-User-Stories/Epics/Epic-Minimum-Editor.md)
> Requirement gốc: [BRD-001 — Image Generation Pipeline](../BRD/BRD-001-Image-Generation-Pipeline.md) (`BR-001-01`…`BR-001-06`, `BR-001-11`, `BR-001-12`) + [BRD-004 — Minimum Editor](../BRD/BRD-004-Minimum-Editor.md) (`BR-004-05`, `BR-004-06`, `BR-004-08`)

> [!CAUTION]
> **Hai lỗi đọc UC này phải tránh — chúng là hai lỗi khác nhau:**
> 1. ⛔ **`best-of-N` KHÔNG phải `retry-on-failure`.** `best-of-N` với **N=3** chạy trên **MỌI** panel như **mặc định**, không phải chỉ khi panel lỗi. Paper ghi *"Performance saturates at N=3"* (CF-3.1 `[OFF]`). **Nhầm hai khái niệm là nguồn của sai số chi phí +50%** (`Glossary` *best-of-N*, `BR-001-02`, `CẤM-03`). `retry-on-failure` có mặt trong UC này — ở **EX-1**, và **chỉ** ở đó.
> 2. ⛔ **Ở MVP0 đây là một SCRIPT, chưa có UI variant picker.** UI chỉ có từ **MVP3** (`MVP-Scope` §5.2 thành phần **#1**). Đọc mục 3 như trạng thái đích MVP3; trạng thái MVP0 nằm ở **AF-1**.

## Mục lục

1. [Thông tin](#1-thông-tin)
2. [Mục tiêu](#2-mục-tiêu)
3. [Main flow](#3-main-flow)
4. [Alternative flow](#4-alternative-flow)
5. [Exception flow](#5-exception-flow)
6. [Tài liệu liên quan](#6-tài-liệu-liên-quan)

---

## 1. Thông tin

| Hạng mục | Nội dung |
|---|---|
| **Primary actor** | **Tác giả truyện chữ** (CF-1.5 `[CHỐT]` — không nhắm phân khúc hoạ sĩ, `CẤM-17`) |
| **Secondary actor** | **VLM** (chấm N candidate và **đề xuất** một — không có quyền quyết định cuối từ MVP3) · **Image provider** qua adapter riêng (Gemini 3 Pro Image / FLUX.2, `BR-001-06`) · **Hệ thống** (Visual Prompt Compiler deterministic, job queue trong Postgres, credit ledger + hold, ghi provenance) |
| **Mốc MVP** | **MVP0** — dạng **script**, làm *"đúng một việc này"* (CF-8.4; `MVP-Scope` §3 hàng **A1** = `✅` MVP0) → **MVP3** — có **variant picker UI** trên panel card (`MVP-Scope` §5.2 thành phần **#1**, `BR-004-05`). ⚠️ `MVP-Scope` §3 A1 ghi `⛔` ở MVP1–MVP2 rồi `✅` lại từ MVP3 |
| **BRD module** | [BRD-001 — Image Generation Pipeline](../BRD/BRD-001-Image-Generation-Pipeline.md) + [BRD-004 — Minimum Editor](../BRD/BRD-004-Minimum-Editor.md) |
| **Điều kiện tiên quyết** | **(P1)** Panel đã có **`Panel Specification` hợp lệ và đã được duyệt** ở [UC-03 — Review Panel Script](./UC-03-Review-Panel-Script.md). *Hợp lệ* gồm ràng buộc **≤3 nhân vật/panel** là **CHECK constraint ở tầng DB** — một spec 4 nhân vật **không tồn tại được** để đi tới bước sinh (xem **EX-3**). <br> **(P2)** Nhân vật trong panel đã có **`Canonical Reference`** — ảnh reference là **điều kiện đầu vào**, không phải mô tả bằng text prompt (`BR-001-01`). <br> **(P3)** Từ MVP3: tenant có **đủ ≥3 credit khả dụng** cho panel này để hold được ghi trước khi enqueue (`BR-001-12`, **KC-7**). <br> **(P4)** Từ MVP1: mọi bản ghi provenance (`parent_generation_id`, `relation_kind`, `origin`, `change_log`) commit được **cùng một transaction** với artifact (**KC-4**) |
| **Trạng thái kết thúc (thành công)** | Panel có **một** generation được chọn (`approved_generation_id`); **mỗi lần chọn** đã sinh một `change_log` row; ảnh đã chọn **không chứa chữ** (thoại sẽ được overlay ở [UC-07](./UC-07-Edit-Bubble-And-Dialogue-In-Panel.md)); hold đã kết chuyển thành tiêu thực + `usage_event` |
| **Trạng thái kết thúc (thất bại)** | Panel **không** có generation nào được chọn. Nếu đã gọi provider thì **chi phí đã tiêu là thật và không hoàn lại** (`BR-004-08`) — đây là lý do không có undo qua generation |

---

## 2. Mục tiêu

### 2.1 Giá trị cho actor

Tác giả truyện chữ **có được một panel dùng được mà không phải tự chấm từng ảnh — và hành động chọn của mình được ghi nhận là hành động sáng tạo**.

Đây là điểm quan trọng nhất của UC này, và nó không phải một điểm thẩm mỹ:

> **Hành động CHỌN của con người chính là `authorship`.**
> `MVP-Scope` §5.2 thành phần **#1** ghi: variant picker là *hành động sáng tạo **rẻ nhất mà giá trị pháp lý cao nhất*** — **chọn = authorship**. Và callout *ràng buộc xuyên suốt* của cùng mục yêu cầu: mọi hành động của người dùng trong editor phải sinh một `change_log` row — ***kể cả hành động chỉ là "chọn ảnh này thay vì ảnh kia"*** (**KC-2**, `BR-004-06`).

| # | Giá trị | Vì sao actor cần nó |
|---|---|---|
| 1 | **Không phải tự chấm từng ảnh** | Hệ thống dựng 3 candidate và VLM **đề xuất** một; actor phán xét trên một tập nhỏ đã được sàng, không trên một dòng ảnh vô định |
| 2 | **Quyền override, và override được ghi lại** | Actor chọn khác VLM là bằng chứng đóng góp trí tuệ mạnh nhất mà UC này sinh ra (AF-2) |
| 3 | **Chi phí minh bạch trước khi tiêu** | Hold **3 credit/panel** được ghi **trước** khi enqueue, vì **N=3 là mặc định cho mọi panel** — không phải trường hợp xấu (**KC-7**, `BR-001-12`) |
| 4 | **Ảnh không nướng chữ vào pixel** | Ảnh sinh ra **không có chữ**; sửa một câu thoại về sau **không** kéo theo một lần sinh lại ảnh (`BR-001-03`, [UC-07](./UC-07-Edit-Bubble-And-Dialogue-In-Panel.md)) |

### 2.2 Ranh giới — cái UC này KHÔNG làm

| Không thuộc UC-06 | Thuộc đâu |
|---|---|
| Viết / sửa `Panel Specification` | [UC-03 — Review Panel Script](./UC-03-Review-Panel-Script.md) |
| Đặt bubble, sửa thoại trên ảnh đã chọn | [UC-07](./UC-07-Edit-Bubble-And-Dialogue-In-Panel.md) |
| Sắp panel lên trang, preview trang | [UC-08](./UC-08-Arrange-Page-And-Preview.md) |
| **UI duyệt cây generation** (tree view / diff / branch-merge) | ⛔ **Cắt hẳn** (`MVP-Scope` §3 hàng **D6**). ⚠️ Nhưng **cột dữ liệu lineage vẫn bắt buộc** — cắt UI **không** kéo theo cắt `parent_generation_id` (`CẤM-09`, `BR-004-10`) |
| `Continuity Checker` như một luồng riêng | Không tồn tại như luồng riêng: nó **là** N-candidate selection **bên trong** UC này (`findings/business-analyst.md` §3.3, `CẤM-12`). Dạng flag + autofix đã bị bác (CF-8.10) |
| Nạp / theo dõi credit, bật BYOK | [UC-10 — Manage Credit & BYOK](./UC-10-Manage-Credit-And-BYOK.md) |

---

## 3. Main flow

> Trạng thái đích **MVP3** (có variant picker UI). Trạng thái **MVP0** (script) ở **AF-1**.
> Mỗi bước ghi rõ **actor nào làm**.

| # | Actor | Hành động | Neo nguồn |
|---|---|---|---|
| 1 | **Tác giả truyện chữ** | Trên **panel card** của một panel đã duyệt spec, ra lệnh sinh ảnh (`Generate` / `Regenerate`) | `BR-004-05` |
| 2 | **Hệ thống** (Visual Prompt Compiler) | Compile `Panel Specification` thành prompt bằng **code deterministic** — tra bảng `field value → cụm từ`, sắp thứ tự, dedup, giải xung đột theo `precedence ladder`, thực thi `constraint budget`, **ghi log ràng buộc bị drop**. Cùng một spec ⇒ **cùng một** prompt | `BR-001-04`, `BR-001-05` |
| 3 | **Hệ thống** | Đưa `text, letters, watermark, speech bubble` vào **negative prompt** — ảnh phải được sinh **không có chữ** | `BR-001-03` · `G1-e` |
| 4 | **Hệ thống** | **HOLD 3 credit** cho panel này trên credit ledger **TRƯỚC** khi enqueue. ⛔ Không gọi provider trước khi hold được ghi. Reserve là **3, không phải 1**, chính vì **N=3 là mặc định** | `BR-001-12` · **KC-7** |
| 5 | **Hệ thống** | Enqueue job **trong cùng transaction** với dữ liệu nghiệp vụ; worker lấy job bằng `FOR UPDATE SKIP LOCKED` trong Postgres ⇒ **không có job mồ côi** | `BR-001-07` |
| 6 | **Image provider** (qua adapter) | Sinh **N = 3 candidate** cho panel này, mỗi candidate có **ảnh `Canonical Reference` của nhân vật làm điều kiện đầu vào**. ⛔ **N=3 là mặc định cho MỌI panel — đây KHÔNG phải phản ứng với một panel lỗi** | `BR-001-01`, `BR-001-02` · CF-3.1 `[OFF]` |
| 7 | **VLM** | Chấm 3 candidate và **đề xuất một** (preselect). Đây là *N-candidate selection* — cũng chính là hình thức canon của `Continuity Checker` | `BR-001-01` · CF-8.10 |
| 8 | **Hệ thống** | Trình **cả 3 candidate** cùng đề xuất của VLM lên panel card (**variant picker**, từ MVP3) | `BR-004-05` |
| 9 | **Tác giả truyện chữ** | **CHỌN một candidate** — đồng ý với đề xuất của VLM, hoặc **override** sang candidate khác (→ AF-2). ⭐ **Hành động chọn này là `authorship`** | `MVP-Scope` §5.2 #1 |
| 10 | **Hệ thống** | Ghi `approved_generation_id` **và một `change_log` row cho lần chọn đó** — kể cả khi actor chỉ *"chọn ảnh này thay vì ảnh kia"*. Ghi kèm `parent_generation_id` + `relation_kind` + `origin` + `field_provenance`, **commit cùng một transaction** với artifact | **KC-1**…**KC-4** · `BR-001-11`, `BR-004-06` |
| 11 | **Hệ thống** | Kết chuyển hold thành **tiêu thực** trên ledger và ghi `usage_event` (append-only) — `cost_usd`, `model_id`, `model_version`, `attempt_no` | `MVP-Scope` §3 **F1**, **F2** |
| 12 | **Hệ thống** | Đặt candidate đã chọn làm ảnh hiện hành của panel. Ảnh này **không chứa chữ** ⇒ thoại được render bằng `typeset layer` ở [UC-07](./UC-07-Edit-Bubble-And-Dialogue-In-Panel.md) | `BR-001-03` |

> [!NOTE]
> **Hai candidate không được chọn KHÔNG bị xoá khỏi lineage.** Chúng là bằng chứng cho *"người đã chọn X thay vì Y"* — thứ chứng minh `decisive contribution`, mà `prompt` một mình **không** chứng minh được (**KC-2**). Cái bị cắt là **UI duyệt cây** (D6), **không** phải dữ liệu (`CẤM-09`).

---

## 4. Alternative flow

| ID | Điều kiện kích hoạt | Luồng | Ghi chú mốc |
|---|---|---|---|
| **AF-1** | **MVP0 — chưa có UI, chưa có DB** | UC chạy dưới dạng **script**: bước 1 là chạy script tay, bước 4–5 **không tồn tại** (MVP0 **không có database**, `MVP-Scope` §3.1 — không hold, không job queue), bước 8–9 **không có variant picker**; **VLM chọn** và kết quả được ghi tay ra CSV/file phẳng để đủ dữ liệu đo. Provenance ở MVP0 là `🟡` ghi tay; *"generation đầu tiên"* có nghĩa pháp lý = generation đầu tiên của **sản phẩm thật, tức MVP1** (`MVP-Scope` §3.1) | **MVP0** · gọi đúng tên **MVP0**, không dùng tên khác (`CẤM-11`) |
| **AF-2** | Ở bước 9, tác giả **override** đề xuất của VLM | Hệ thống ghi `approved_generation_id` trỏ tới candidate mà **người** chọn, cùng một `change_log` row. ⭐ Đây là **bằng chứng đóng góp trí tuệ mạnh nhất** UC này sinh ra: không phải *"AI đề xuất và người bấm OK"*, mà *"người đã chọn khác AI"* | MVP3 |
| **AF-3** | Tác giả **không chấp nhận cả 3** candidate | Tác giả ra lệnh `Regenerate`: quay lại bước 2 và sinh **một lượt 3 candidate mới**, ghi `parent_generation_id` trỏ về lượt trước với `relation_kind` phù hợp (`retry` / `variation`). ⚠️ Lượt mới **hold thêm 3 credit** và **tiêu tiền thật** — `Regenerate` **không** undo được (`BR-004-08`) | MVP3 |
| **AF-4** | Tác giả kết luận **spec sai**, không phải ảnh sai | Sang [UC-03](./UC-03-Review-Panel-Script.md) sửa field của spec, rồi quay lại UC-06 từ bước 1. Lượt sinh sau ghi `relation_kind = 'refine'`. Sửa spec **không** thuộc UC-06 | MVP2+ |
| **AF-5** | Vận hành chọn **whole-page render granularity** thay vì per-panel | Hệ thống compile **nhiều** `Panel Specification` thành **MỘT** prompt whole-page. Đây là **đường lui #1 khi gate G2 FAIL** và nó **không đổi data model**, vì spec — không phải ảnh — là dữ liệu chính | `BR-001-09` · MVP3 `🟡` → MVP4 — **NGOÀI HORIZON** |
| **AF-6** | Tenant bật **BYOK** và tự chịu COGS | Luồng sinh ảnh không đổi; phần thay đổi là ai trả tiền provider. Cơ chế thuộc [UC-10](./UC-10-Manage-Credit-And-BYOK.md), **không** thuộc UC-06 | MVP4 — **NGOÀI HORIZON** |

---

## 5. Exception flow

| ID | Ngoại lệ | Xử lý | Ranh giới cần giữ |
|---|---|---|---|
| **EX-1** | **Lời gọi provider cho một candidate lỗi / timeout / bị provider từ chối** | Hệ thống **retry đúng lời gọi đã lỗi** (`retry-on-failure`), ghi `attempt_no` tăng và log việc provider từ chối. Mục tiêu vẫn là **đủ 3 candidate** | ⛔ **Đây là chỗ duy nhất `retry-on-failure` xuất hiện trong UC này, và nó KHÁC `best-of-N`.** `best-of-N` (bước 6) là **mặc định trên mọi panel**; `retry-on-failure` là **xử lý lỗi**. Retry **không** làm N khác 3, và **không** biến N=3 thành *"chỉ dùng khi panel lỗi"* (`BR-001-02`, `Glossary` *best-of-N*) |
| **EX-2** | **Không hold được 3 credit** (số dư không đủ) ở bước 4 | Hệ thống **TỪ CHỐI enqueue** và **không gọi provider**. `CHECK (available >= 0)` ở **tầng DB** là lớp chặn cuối; hard quota cưỡng chế **trước** khi enqueue, **không đếm sau** | ⛔ Không có nhánh *"gọi provider rồi tính tiền sau"* — check-rồi-gọi là **race condition**: 10 job đồng thời đều thấy đủ số dư (CF-6.12). Hạ reserve xuống 1 credit là **hợp pháp hoá số dư âm** (`MVP-Scope` §6.1) |
| **EX-3** | **Spec có 4 nhân vật** trong một panel | ⛔ Panel đó **không tới được bước 1**: insert bị **DB TỪ CHỐI** bởi CHECK constraint — **bị từ chối, KHÔNG phải bị cảnh báo** (`M2-2`). Đường đi hợp lệ duy nhất là giải cảnh đông người bằng **shot xa / silhouette / crop** ở [UC-03](./UC-03-Review-Panel-Script.md), **không** bằng cách nhồi thêm nhân vật | Căn cứ CF-6.5 `[OFF]`: ID-Sim **42.33** (2 nhân vật) → **27.21** (3) → **2.67** (4) → **0.52** (5). Từ 4 nhân vật, `attribute binding` thất bại gần hoàn toàn — ảnh *trông hợp lý* nhưng **gắn sai áo cho sai người**. ⚠️ Nếu gate **G1-d** không đạt ngưỡng, trần siết xuống **≤2** ngay trong schema (`BR-003-06`) |
| **EX-4** | Provider trả về candidate **có chữ nướng vào pixel** (bất chấp negative prompt) | Candidate đó bị coi là **FAIL** và không được đưa lên variant picker. Ngưỡng nghiệm thu **G1-e** là **100%** panel có thoại dùng overlay và **0** panel nhờ model render chữ ⇒ *"chấp nhận tạm một panel có chữ"* làm FAIL exit criterion | ⛔ Không có nhánh *"dùng tạm ảnh có chữ rồi sửa sau"*: nướng chữ vào pixel nghĩa là mỗi lần sửa thoại thành **một lần regenerate ảnh** (`Glossary` *typeset layer*) |
| **EX-5** | **Worker chết sau khi hold đã ghi** nhưng trước khi job xong | **Hold reaper** giải phóng hold theo `expires_at`. Thiếu reaper thì hold treo **vĩnh viễn** ⇒ khách *"có credit mà không generate được"* — `MVP-Scope` **KC-7** xếp đây là loại lỗi phải chặn từ đầu. Worker chết mà API vẫn phục vụ được (`M3-4`) | MVP3 |
| **EX-6** | Tác giả muốn **undo** một lượt generate đã chạy | ⛔ **Không có undo qua generation** — một lượt `Regenerate` **tiêu tiền thật và không hoàn lại được**. Undo chỉ tồn tại ở phạm vi **cục bộ** (form + vị trí bubble). UX **phải nói rõ** điều này, không để actor suy đoán | `BR-004-08` · `MVP-Scope` §5.3 hàng **#7** (D3 hoãn) |
| **EX-7** | Provider đổi weights dưới **cùng một tên model** (`silent model drift`) | Không có cách chặn từ phía hệ thống. Điều bắt buộc là **ghi đủ** `model_id` + `model_version` + `seed` như **provenance metadata**. ⚠️ Mục tiêu của bảng `Generation` là **AUDITABILITY + LINEAGE**, **không phải reproducibility bit-exact**; `seed` **không** phải replay key | `BR-001-10` · `MVP-Scope` §4.4 |

---

## 6. Tài liệu liên quan

### 6.1 Traceability

| Liên kết | Tài liệu | Điểm neo |
|---|---|---|
| Requirement gốc (pipeline) | [BRD-001 — Image Generation Pipeline](../BRD/BRD-001-Image-Generation-Pipeline.md) | `BR-001-01` (best-of-N, N=3, reference là điều kiện đầu vào) · `BR-001-02` (**≠ retry-on-failure**) · `BR-001-03` (ảnh không có chữ) · `BR-001-04`/`05` (compiler deterministic, precedence ladder) · `BR-001-06` (adapter) · `BR-001-07` (queue trong Postgres) · `BR-001-11` (provenance cùng transaction) · `BR-001-12` (hold 3 credit) |
| Requirement gốc (editor) | [BRD-004 — Minimum Editor](../BRD/BRD-004-Minimum-Editor.md) | `BR-004-05` (panel card + variant picker) · `BR-004-06` (`change_log` mọi hành động) · `BR-004-08` (không undo qua generation) · `BR-004-10` (cắt D6 ≠ cắt lineage) |
| Epic | [Epic-Image-Generation-Pipeline](../../022-User-Stories/Epics/Epic-Image-Generation-Pipeline.md) · [Epic-Minimum-Editor](../../022-User-Stories/Epics/Epic-Minimum-Editor.md) | `Story-Generate-Panel-With-Reference-And-VLM-Select` · `Story-Panel-Card-With-Variant-Picker` |
| Sản phẩm | [PRD-Comic-Studio](../PRD-Comic-Studio.md) · [SRS-Comic-Studio](../SRS-Comic-Studio.md) | — |
| UC thượng nguồn | [UC-03 — Review Panel Script](./UC-03-Review-Panel-Script.md) | Nguồn của `Panel Specification` hợp lệ (P1) |
| UC hạ nguồn | [UC-07](./UC-07-Edit-Bubble-And-Dialogue-In-Panel.md) · [UC-08](./UC-08-Arrange-Page-And-Preview.md) | Ảnh không chữ ⇒ `typeset layer` · panel đã chọn ⇒ sắp lên trang |
| UC liên quan | [UC-10 — Manage Credit & BYOK](./UC-10-Manage-Credit-And-BYOK.md) | Cơ chế ledger, hold, BYOK |
| Exit criterion | [Roadmap](../../010-Planning/Roadmap.md) §2 | **G1-e** (100% panel có thoại dùng overlay, 0 panel nhờ model render chữ) · **M2-2** (≤3 nhân vật là CHECK constraint, *bị từ chối* không phải *bị cảnh báo*) · **M3-1**, **M3-2** (hold 3 credit/panel), **M3-4** |
| Ranh giới scope | [MVP-Scope](../../010-Planning/MVP-Scope.md) §3 hàng **A1**–**A7**, **C5**, **D6** · §5.2 thành phần **#1** · §6 **KC-1**…**KC-4**, **KC-7** | — |

### 6.2 Nguồn đã trích

| Nguồn | Phần | Dùng cho |
|---|---|---|
| [MVP-Scope.md](../../010-Planning/MVP-Scope.md) | §3 **A1**–**A7**, **C5**, **D6**, **F1**, **F2** · §3.1 (MVP0 không có DB; nghĩa pháp lý của *"generation đầu tiên"*) · §4.4 (auditability ≠ reproducibility) · §5.2 **#1** (*"chọn = authorship"*) + callout `change_log` · §5.3 **#7** · §6 **KC-1**…**KC-4**, **KC-7** · §6.1 (ba hiểu nhầm) | Mốc, ranh giới, nghĩa vụ provenance, cơ chế hold |
| [Roadmap.md](../../010-Planning/Roadmap.md) | §2 exit criteria **G1-e**, **M2-2**, **M3-1**…**M3-4** · §4 hàng **X-c** | Ngưỡng đo |
| [Glossary.md](../../999-Resources/Glossary.md) | *best-of-N (N=3)* · *typeset layer* · *Canonical Reference* · *attribute binding* · *Visual Prompt Compiler* · *precedence ladder* · *constraint budget* · *credit ledger + hold* · *Continuity Checker* | Phân biệt best-of-N vs retry-on-failure; nghĩa canon của các term |
| [BRD-001-Image-Generation-Pipeline.md](../BRD/BRD-001-Image-Generation-Pipeline.md) · [BRD-004-Minimum-Editor.md](../BRD/BRD-004-Minimum-Editor.md) | §3 toàn bộ bảng yêu cầu | Requirement gốc mọi bước |
| `docs/010-Planning/pm-runs/2026-08-24-khoi-tao-requirements-stories-comic-studio/findings/business-analyst.md` | §3.2 (hàng **UC-06**) · §3.3 (Continuity Checker **không** là UC riêng) · §5.3 **CẤM-03**, **CẤM-09**, **CẤM-11**, **CẤM-12**, **CẤM-17** | Phạm vi UC, các lệnh cấm áp dụng |

> [!NOTE]
> **Quy ước nhãn nguồn số liệu** — kế thừa từ [MVP-Scope](../../010-Planning/MVP-Scope.md): `[OFF]` official/paper gốc · `[BCN]` báo cáo ngành có tên firm · `[TC]` nguồn thứ cấp · `[EM]` **ước lượng, không phải số đo** · `[CHỐT]` quyết định của founder tại gate. Copy một con số sang tài liệu khác thì **copy cả nhãn** (`CẤM-15`).
