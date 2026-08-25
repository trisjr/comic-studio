---
id: UC-08
type: use-case
status: draft
project: comic-studio
created: 2026-08-24
---

# UC-08 — Sắp trang và xem trang thành phẩm

> Part of: [Epic-Comic-Director-And-Layout](../../022-User-Stories/Epics/Epic-Comic-Director-And-Layout.md) · [Epic-Minimum-Editor](../../022-User-Stories/Epics/Epic-Minimum-Editor.md)
> Requirement gốc: [BRD-003 — Comic Director & Layout](../BRD/BRD-003-Comic-Director-And-Layout.md) (`BR-003-03`, `BR-003-04`, `BR-003-08`) + [BRD-004 — Minimum Editor](../BRD/BRD-004-Minimum-Editor.md) (`BR-004-02`, `BR-004-03`, `BR-004-06`, `BR-004-07`)

> [!IMPORTANT]
> **UC này quan trọng hơn vẻ ngoài của nó.** *Selection & arrangement* — việc **chọn** panel nào và **sắp** chúng ra sao — là phần **ĐƯỢC BẢO HỘ bản quyền** theo **tiền lệ Zarya of the Dawn** (`Glossary` *Layout Director*: *"Cùng với Comic IR, output của nó là phần **được bảo hộ bản quyền** theo tiền lệ Zarya of the Dawn"*). Một UC trông như *"kéo thả cho đẹp"* thực chất là nơi quyền tác giả của actor được tạo ra và được ghi vết.

> [!CAUTION]
> **Hai ranh giới kỹ thuật cứng:**
> 1. ⛔ **Layout lưu bằng toạ độ chuẩn hoá 0–1 trong `page_layout JSONB`**; **template chỉ là các preset ghi vào CÙNG schema đó**. Đây là *"đường nâng cấp không mất mát"*: nếu về sau lên canvas thật bằng thư viện có sẵn thì **không phải migrate dữ liệu**, chỉ thay lớp tương tác. **KHÔNG viết renderer từ đầu** (`MVP-Scope` §4.1, `BR-003-04`, `BR-004-07`).
> 2. ⛔ **KHÔNG dùng `Layout Score` số thực.** Cơ chế 5 số thực **đã bị CẮT HẲN** (`MVP-Scope` §3 hàng **C4** = `❌` ở **mọi** cột kể cả Full Scope; CF-9.3 — *không có prior art*, *"chưa ai làm vì không đáng"*). Cái được giữ là **mục tiêu** *"bố cục có nhịp theo narrative importance"*; cái bị bỏ là **cơ chế điểm số**. Thay bằng **rubric `beat_type` rời rạc + bảng tra deterministic + emphasis quota theo chapter**.

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
| **Primary actor** | **Tác giả truyện chữ** (CF-1.5 `[CHỐT]`) |
| **Secondary actor** | **Hệ thống** — **Layout Director** (đề xuất phân bổ diện tích theo rubric `beat_type` + emphasis quota), **compositor server-side** (render preview PNG/PDF, tái dùng compositor của export **H4**), và tầng ghi `change_log` |
| **Mốc MVP** | **MVP2** — thành phần **#3** *(template layout, swap/reorder panel: **3–4%** `[EM]`)* và thành phần **#4** *(preview trang + chapter render server-side, read-only: **3–5%** `[EM]`)* của editor tối thiểu; `MVP-Scope` §3 hàng **C3** = `✅` MVP2, **D1** = `🟡` MVP2 |
| **BRD module** | [BRD-003 — Comic Director & Layout](../BRD/BRD-003-Comic-Director-And-Layout.md) + [BRD-004 — Minimum Editor](../BRD/BRD-004-Minimum-Editor.md) |
| **Điều kiện tiên quyết** | **(P1)** Trang đã có tập panel với `Panel Specification` hợp lệ, do Director sinh và đã duyệt ở [UC-03](./UC-03-Review-Panel-Script.md). <br> **(P2)** **Mỗi panel đã khai `text_safe_zone` ngay trong `Panel Specification`** — thiếu nó thì bubble che mặt nhân vật và **phải sinh lại toàn bộ ảnh đã làm** (`BR-003-08`, `Glossary` *`text_safe_zone`*). <br> **(P3)** `page_layout JSONB` tồn tại như nơi lưu duy nhất của bố cục, ở dạng **toạ độ chuẩn hoá 0–1** (`BR-004-07`). <br> **(P4)** Để **preview** thì panel cần có ảnh đã chọn ([UC-06](./UC-06-Generate-Panel-And-Pick-Variant.md)) và `typeset layer` ([UC-07](./UC-07-Edit-Bubble-And-Dialogue-In-Panel.md)); panel chưa có ảnh hiển thị dạng ô trống trong preview |
| **Trạng thái kết thúc (thành công)** | Bố cục trang được ghi vào `page_layout JSONB` dạng toạ độ **0–1**; **mỗi** thao tác sắp đặt của actor đã sinh một `change_log` row; actor đã xem được **trang thành phẩm** dưới dạng composite **read-only** |
| **Trạng thái kết thúc (thất bại)** | `page_layout JSONB` giữ nguyên trạng thái trước đó. ⚠️ **Preview thành công KHÔNG đồng nghĩa trang được xuất bản** — xuất bản vẫn đòi **cả hai** human gate PASS (`M2-4`) |

---

## 2. Mục tiêu

### 2.1 Giá trị cho actor

Tác giả truyện chữ **quyết định nhịp đọc của trang mình, và thấy được thành phẩm trước khi trả tiền**.

| # | Giá trị | Neo nguồn |
|---|---|---|
| 1 | **Quyết định sắp đặt là của actor, và nó được bảo hộ** | *Selection & arrangement* là quyết định sáng tạo của con người; cùng với Comic IR, output của Layout Director là phần **được bảo hộ bản quyền** (tiền lệ **Zarya of the Dawn**). Mỗi thao tác sinh một `change_log` row ⇒ có bằng chứng, không chỉ có kết quả (**KC-2**) |
| 2 | **Bố cục có nhịp mà không phải tự chấm điểm gì** | Hệ thống đề xuất theo **rubric `beat_type` rời rạc + bảng tra deterministic + emphasis quota theo chapter** — panel quan trọng được cấp diện tích lớn hơn (`BR-003-03`) |
| 3 | **Chỉ cần rời rạc, nên rẻ và làm được** | Sắp đặt là **đổi chỗ / swap / reorder giữa các ô**, **không** cần hình học liên tục (`BR-004-02`). Đây là điều làm thành phần này khả thi với đội **1 người** (CF-1.2 `[CHỐT]`) |
| 4 | **Thấy thành phẩm mới trả tiền** | Preview là composite **render server-side**, **read-only**, và rẻ vì **tái dùng compositor của export** (`BR-004-03`, thành phần #4) |

### 2.2 Ranh giới — cái UC này KHÔNG làm

| Không thuộc UC-08 | Vì sao / thuộc đâu |
|---|---|
| **`Layout Score` 5 số thực** để tự động chấm bố cục | ⛔ **CẮT HẲN** — `MVP-Scope` §3 hàng **C4** là `❌` ở **mọi** cột, kể cả Full Scope. Mục tiêu giữ, **cơ chế bỏ** (`Glossary` *Layout Score*) |
| Hình học panel tự do: panel xoay, không chữ nhật, zoom/pan cả chapter | ⛔ **D2, HOÃN** (`MVP-Scope` §3 D2, §5.3 #6). Khi mở lại: dùng `tldraw`/`konva`/`fabric.js` sau một spike riêng — **không viết renderer từ đầu** |
| Tự chia scene thành page/panel | Thuộc **Director** (`BR-003-02`) và được duyệt ở [UC-03](./UC-03-Review-Panel-Script.md) |
| Sửa bubble / thoại trong panel | [UC-07](./UC-07-Edit-Bubble-And-Dialogue-In-Panel.md) |
| Nén thoại và xác nhận bản nén | [UC-05](./UC-05-Human-Gate-Dialogue-Condensation.md). ⚠️ UC-08 **cấp đầu vào** cho UC-05 (diện tích panel ⇒ `text_budget`) và có thể **làm mất hiệu lực** xác nhận cũ (**EX-2**) |
| Xuất file PDF / CBZ / webtoon để lấy ra khỏi hệ thống | [UC-09 — Export Chapter](./UC-09-Export-Chapter.md). Preview ở đây là **read-only**, **không** phải export |
| Chi tiết giao diện: template trông thế nào, nút nằm đâu | Thuộc tầng `docs/040-Design/` — **ngoài scope** của tài liệu Use Case |

---

## 3. Main flow

> Mỗi bước ghi rõ **actor nào làm**. Bước 8 là bước nối UC này với human gate #2.

| # | Actor | Hành động | Neo nguồn |
|---|---|---|---|
| 1 | **Tác giả truyện chữ** | Mở một trang cần sắp | `BR-004-02` |
| 2 | **Hệ thống** | Đọc bố cục hiện hành từ **`page_layout JSONB`** (toạ độ chuẩn hoá **0–1**) và trình các panel của trang theo **thứ tự đọc** | `BR-003-04`, `BR-004-07` |
| 3 | **Hệ thống** (Layout Director) | Đề xuất phân bổ diện tích: panel quan trọng lớn hơn, theo **rubric `beat_type` rời rạc + bảng tra deterministic + emphasis quota theo chapter**. ⛔ **Không có điểm số thực nào được tính, hiển thị hay lưu** | `BR-003-03` · `MVP-Scope` §4.3 |
| 4 | **Tác giả truyện chữ** | **Chọn template layout** cho trang | `BR-004-02` — thành phần **#3** |
| 5 | **Tác giả truyện chữ** | **Đổi chỗ / swap panel giữa các ô** và **reorder** thứ tự đọc. Thao tác là **rời rạc** — chọn ô, không phải kéo hình học liên tục | `BR-004-02` |
| 6 | **Hệ thống** | Ghi bố cục vào **`page_layout JSONB`** dưới dạng **toạ độ chuẩn hoá 0–1**. **Template chỉ là preset ghi vào CÙNG schema đó** — không có schema thứ hai cho template | `BR-004-07` · `MVP-Scope` §4.1 |
| 7 | **Hệ thống** | Ghi một **`change_log` row cho mỗi** thao tác ở bước 4–5 (chọn template, swap panel, reorder). ⭐ Đây là chỗ *selection & arrangement* biến từ **kết quả** thành **bằng chứng** | `BR-004-06` · **KC-2**, **KC-4** |
| 8 | **Hệ thống** | Diện tích panel đổi ⇒ **tính lại `text_budget`** cho các panel bị ảnh hưởng. ⛔ Nếu dòng thoại nào thuộc panel đó **đã PASS** human gate #2, **reset gate #2 về OPEN** và yêu cầu nén lại + xác nhận lại ở [UC-05](./UC-05-Human-Gate-Dialogue-Condensation.md). Đây là hệ quả trực tiếp của ràng buộc cứng **`layout → dialogue condensation`** | `BR-003-12` · [UC-05](./UC-05-Human-Gate-Dialogue-Condensation.md) **EX-4** |
| 9 | **Hệ thống** | Kiểm **`text_safe_zone`** của từng panel còn dùng được với ô mới; cảnh báo panel nào có nguy cơ bubble đè vùng mặt (ngưỡng **≥95%** panel không đè, ⚠️ **`[EM]`**) | `BR-003-08`, `BR-003-09` · `M2-3` |
| 10 | **Tác giả truyện chữ** | Yêu cầu **preview trang thành phẩm** | `BR-004-03` — thành phần **#4** |
| 11 | **Hệ thống** (compositor) | Render **composite server-side** (PNG/PDF) gồm ảnh panel + `typeset layer`, trả về **read-only**. Tái dùng compositor của export (**H4**) | `BR-004-03` |
| 12 | **Tác giả truyện chữ** | Xem trang thành phẩm và kết luận: chấp nhận, hoặc quay lại bước 4 | — |
| 13 | **Hệ thống** | ⚠️ Giữ nguyên trạng thái xuất bản: **preview KHÔNG mở đường xuất bản**. Trang chỉ xuất bản được khi **cả hai** human gate PASS ([UC-04](./UC-04-Human-Gate-Speaker-Attribution.md) + [UC-05](./UC-05-Human-Gate-Dialogue-Condensation.md)) | `M2-4` · `BR-003-13` |

> [!NOTE]
> **Preview được phép chạy TRƯỚC khi hai gate PASS.** Preview là **read-only** và không đưa nội dung ra ngoài hệ thống ⇒ nó không phải *"xuất bản"*, nên nó **không** là một đường bypass của `M2-4`. Ranh giới cần giữ đúng: `M2-4` chặn **xuất bản page**, không chặn **xem trước**.

---

## 4. Alternative flow

| ID | Điều kiện kích hoạt | Luồng | Ghi chú mốc |
|---|---|---|---|
| **AF-1** | Actor **giữ nguyên** đề xuất của Layout Director | Không có thao tác ⇒ **không sinh `change_log` row** cho sắp đặt. ⚠️ Hệ quả pháp lý cần biết: trang mà actor **không** thao tác gì thì phần *arrangement* của trang đó **không có** bằng chứng đóng góp từ actor. `MVP-Scope` §6 **KC-2** nêu rõ cái chứng minh được là *người đã chọn X thay vì Y* — trạng thái mặc định của hệ thống không chứng minh điều đó | MVP2 |
| **AF-2** | **Emphasis quota của chapter đã dùng hết** | Hệ thống **không cấp thêm** ô emphasis cho trang này; actor chọn hoặc đổi một panel emphasis đã cấp sang panel khác, hoặc giữ bố cục đều. Quota là **rời rạc theo chapter**, không phải một điểm số co giãn | `BR-003-03` · `MVP-Scope` §4.3 |
| **AF-3** | Actor muốn xem **cả chapter** thay vì một trang | Compositor render **chapter** dưới dạng composite read-only — cùng cơ chế bước 11, khác phạm vi (`BR-004-03` phủ **cả trang và chapter**) | MVP2 |
| **AF-4** | Actor muốn **lấy file ra khỏi hệ thống** | Sang [UC-09 — Export Chapter](./UC-09-Export-Chapter.md). Preview và export **dùng cùng compositor** nhưng là **hai UC khác nhau**: preview read-only trong hệ thống, export là bàn giao thành phẩm | MVP2 (PDF) → MVP3 |
| **AF-5** | **MVP0 / MVP1 — chưa có template UI** | Ở **MVP0** layout là **viết tay** (`MVP-Scope` §3 **C3** = `❌` MVP0, `⛔` MVP1). UC này chưa tồn tại như một luồng người dùng; bố cục nằm trong file YAML viết tay. ⚠️ Nhưng **dạng lưu trữ vẫn phải là toạ độ 0–1** ngay từ MVP để giữ đường nâng cấp không mất mát | `MVP-Scope` §4.1 |
| **AF-6** | Trang có panel **chưa có ảnh** | Preview vẫn render được, panel đó hiện dạng **ô trống**. Sắp đặt không đòi ảnh — vì **spec, không phải ảnh, là dữ liệu chính** (`BR-003-01`) | MVP2 |

---

## 5. Exception flow

| ID | Ngoại lệ | Xử lý | Ranh giới cần giữ |
|---|---|---|---|
| **EX-1** | **Template được chọn không đủ ô** cho số panel của trang | Hệ thống **từ chối** áp template đó và nêu rõ số ô so với số panel. ⛔ Không tự nhồi hai panel vào một ô, không tự bỏ panel. Đường hợp lệ: chọn template khác, hoặc đổi cách chia trang ở [UC-03](./UC-03-Review-Panel-Script.md) (việc của Director, `BR-003-02`) | Sắp đặt là **rời rạc**: mỗi panel một ô. Không có hình học liên tục để "co lại cho vừa" (`BR-004-02`) |
| **EX-2** | **Layout bị đổi sau khi human gate #2 đã PASS** | Diện tích panel đổi ⇒ `text_budget` đổi ⇒ bản nén đã duyệt **không còn được duyệt trên đúng ràng buộc** ⇒ hệ thống **reset gate #2 về OPEN** cho các dòng thuộc panel bị ảnh hưởng. Trang **không xuất bản được** cho tới khi actor xác nhận lại ở [UC-05](./UC-05-Human-Gate-Dialogue-Condensation.md) (mirror của `UC-05` **EX-4**) | Ràng buộc cứng `layout → condensation` (`BR-003-12`) không phải một tối ưu hoá — bỏ reset ở đây tạo ra một đường bypass và **`M2-4` FAIL** |
| **EX-3** | Actor muốn **hình học panel tự do**: panel xoay, không chữ nhật, chồng lấn, zoom/pan cả chapter | ⛔ **Từ chối — D2 HOÃN.** Lý do: *chi phí lớn nhất, giá trị tăng thêm nhỏ nhất* ở bản trả phí đầu. Điều kiện mở lại: **có bằng chứng đo được rằng khách rời đi vì thiếu nó**; khi làm thì dùng thư viện có sẵn sau một spike riêng, **không viết renderer từ đầu** | `MVP-Scope` §3 **D2** · §5.3 **#6** |
| **EX-4** | Actor (hoặc một yêu cầu về sau) muốn **một điểm số layout** để tự động chấm/chọn bố cục | ⛔ **Từ chối — `Layout Score` số thực đã CẮT HẲN**, không có cả trong Full Scope (`C4` = `❌` mọi cột). Căn cứ: **không có prior art**, không kiểm chứng được đúng/sai, và có phương án thay thế rẻ hơn nhiều lần (CF-9.3, NT-3 vế 1). Đường hợp lệ duy nhất là **rubric `beat_type` + emphasis quota rời rạc** | ⚠️ Cẩn thận cách diễn đạt: **mục tiêu** *"bố cục theo narrative importance"* **được giữ**; chỉ **cơ chế điểm số thực** bị bỏ (`Glossary` *Layout Score*) |
| **EX-5** | Một panel **thiếu `text_safe_zone`** trong `Panel Specification` | Hệ thống **báo lỗi ở tầng spec** và không coi trang là đã sắp xong. ⛔ Không có nhánh *"đặt bubble rồi tính sau"*: thiếu `text_safe_zone` nghĩa là bubble che mặt nhân vật và **phải sinh lại TOÀN BỘ ảnh đã làm** — thiệt hại đã tiêu tiền thật, không hoàn lại | `BR-003-08` · `Glossary` *`text_safe_zone`* · `M2-3` |
| **EX-6** | Actor muốn **thêm nhân vật vào một panel** để lấp một ô trông trống | ⛔ Không thuộc UC-08 (thuộc [UC-03](./UC-03-Review-Panel-Script.md)), và nếu panel đã có 3 nhân vật thì thao tác **bị DB TỪ CHỐI**: trần **≤3 nhân vật/panel** là **CHECK constraint ở tầng DB** — *insert panel 4 nhân vật **bị từ chối**, **không phải** bị cảnh báo* (`M2-2`). Đường hợp lệ: đổi template, hoặc giải cảnh đông người bằng **shot xa / silhouette / crop** (`BR-003-07`) | Căn cứ CF-6.5 `[OFF]`: ID-Sim **42.33** (2) → **27.21** (3) → **2.67** (4) → **0.52** (5). ⚠️ Nếu gate **G1-d** không đạt ngưỡng, trần siết xuống **≤2** ngay trong schema (`BR-003-06`) |
| **EX-7** | **Render preview lỗi / timeout** ở bước 11 | Preview là **read-only** ⇒ lỗi **không** làm hỏng `page_layout JSONB` hay bất kỳ artifact nào. Hệ thống báo lỗi, cho thử lại. ⛔ Không có nhánh *"coi như đã xem và cho xuất bản"* — và kể cả preview thành công cũng **không** mở đường xuất bản (bước 13) | `BR-004-03` (read-only) · `M2-4` |

---

## 6. Tài liệu liên quan

### 6.1 Traceability

| Liên kết | Tài liệu | Điểm neo |
|---|---|---|
| Requirement gốc (layout) | [BRD-003 — Comic Director & Layout](../BRD/BRD-003-Comic-Director-And-Layout.md) | `BR-003-03` (rubric `beat_type` + emphasis quota, **không** điểm số thực) · `BR-003-04` (toạ độ 0–1 trong `page_layout JSONB`) · `BR-003-07` (cảnh đông người) · `BR-003-08`/`09` (`text_safe_zone`, ngưỡng ≥95% `[EM]`) · `BR-003-12` (thứ tự `layout → condensation`) · `BR-003-13` (đo gate bằng vắng mặt đường bypass) |
| Requirement gốc (editor) | [BRD-004 — Minimum Editor](../BRD/BRD-004-Minimum-Editor.md) | `BR-004-02` (template layout, swap/reorder — thành phần #3) · `BR-004-03` (preview composite server-side, read-only — thành phần #4) · `BR-004-06` (`change_log` mọi hành động) · `BR-004-07` (toạ độ 0–1, **không viết renderer từ đầu**) |
| Epic | [Epic-Comic-Director-And-Layout](../../022-User-Stories/Epics/Epic-Comic-Director-And-Layout.md) · [Epic-Minimum-Editor](../../022-User-Stories/Epics/Epic-Minimum-Editor.md) | `Story-Layout-Rubric-Beat-Type-And-Emphasis-Quota` · `Story-Page-Template-Layout-And-Swap-Panel` · `Story-Server-Side-Page-And-Chapter-Preview` |
| Sản phẩm | [PRD-Comic-Studio](../PRD-Comic-Studio.md) · [SRS-Comic-Studio](../SRS-Comic-Studio.md) | — |
| UC thượng nguồn | [UC-03](./UC-03-Review-Panel-Script.md) · [UC-06](./UC-06-Generate-Panel-And-Pick-Variant.md) · [UC-07](./UC-07-Edit-Bubble-And-Dialogue-In-Panel.md) | Panel spec đã duyệt · ảnh đã chọn · `typeset layer` |
| UC hạ nguồn | [UC-05](./UC-05-Human-Gate-Dialogue-Condensation.md) · [UC-09](./UC-09-Export-Chapter.md) | UC-08 cấp `text_budget` cho UC-05; đổi layout ⇒ reset gate (**EX-2**) · export dùng cùng compositor |
| Exit criterion | [Roadmap](../../010-Planning/Roadmap.md) §2 | **M2-2** (≤3 nhân vật là CHECK constraint — *bị từ chối*, không *bị cảnh báo*) · **M2-3** (`text_safe_zone`, ≥95% `[EM]`) · **M2-4** (hai gate không bypass được) · **M2-5** (export PDF từ preview server-side) |
| Ranh giới scope | [MVP-Scope](../../010-Planning/MVP-Scope.md) §3 hàng **C3**, **C4**, **C5**, **C6**, **D1**, **D2**, **H4** · §4.1, §4.3 · §5.2 thành phần **#3**, **#4** · §5.3 **#6** · §6 **KC-2**, **KC-4** | — |

### 6.2 Nguồn đã trích

| Nguồn | Phần | Dùng cho |
|---|---|---|
| [MVP-Scope.md](../../010-Planning/MVP-Scope.md) | §3 **C3**, **C4** (`❌` mọi cột), **C5**, **C6**, **D1**, **D2**, **H4** · §4.1 (*"đường nâng cấp không mất mát"*, toạ độ 0–1, **không viết renderer từ đầu**) · §4.3 (cắt cơ chế, giữ mục tiêu) · §5.2 thành phần **#3** (**3–4%** `[EM]`) và **#4** (**3–5%** `[EM]`) + callout `change_log` · §5.3 **#6** · §6 **KC-2**, **KC-4** | Mốc, ranh giới, dạng lưu layout, lý do cắt `Layout Score` |
| [Roadmap.md](../../010-Planning/Roadmap.md) | §2 exit criteria **M2-2**…**M2-5** | Ngưỡng đo |
| [Glossary.md](../../999-Resources/Glossary.md) | *Layout Director* (**tiền lệ Zarya of the Dawn**) · *Layout Score* (cơ chế số thực **đã bị cắt**) · *`text_safe_zone`* · *Panel Specification* · *dialogue condensation* | Cơ sở bảo hộ *selection & arrangement*; định nghĩa canon |
| [BRD-003](../BRD/BRD-003-Comic-Director-And-Layout.md) · [BRD-004](../BRD/BRD-004-Minimum-Editor.md) | §3 bảng yêu cầu nghiệp vụ | Requirement gốc mọi bước |
| `docs/010-Planning/pm-runs/2026-08-24-khoi-tao-requirements-stories-comic-studio/findings/business-analyst.md` | §3.2 (hàng **UC-08**) · §5.3 lệnh cấm | Phạm vi UC, kỷ luật trích số |

> [!NOTE]
> **Quy ước nhãn nguồn số liệu** — kế thừa từ [MVP-Scope](../../010-Planning/MVP-Scope.md): `[OFF]` official/paper gốc · `[BCN]` báo cáo ngành có tên firm · `[TC]` nguồn thứ cấp · `[EM]` **ước lượng, không phải số đo** · `[CHỐT]` quyết định của founder tại gate. Copy một con số sang tài liệu khác thì **copy cả nhãn** (`CẤM-15`).
