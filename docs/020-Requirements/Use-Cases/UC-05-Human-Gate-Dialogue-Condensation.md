---
id: UC-05
type: use-case
status: draft
project: comic-studio
created: 2026-08-24
---

# UC-05 — Human Gate: Dialogue Condensation

> Part of: [Epic-Comic-Director-And-Layout](../../022-User-Stories/Epics/Epic-Comic-Director-And-Layout.md)
> Requirement gốc: [BRD-003 — Comic Director & Layout](../BRD/BRD-003-Comic-Director-And-Layout.md) (`BR-003-11`, `BR-003-12`, `BR-003-13`, `BR-003-14`)

> [!CAUTION]
> Đây là **human gate bắt buộc thứ hai**, không phải một bước tuỳ chọn và **không được dồn sang MVP4** (`MVP-Scope` §3 hàng **C7**, CF-8.8). Tiêu chí nghiệm thu **M2-4** không đo *"có một màn hình xác nhận"* — nó đo **sự VẮNG MẶT của một đường code bypass**: không tồn tại đường nào xuất bản page mà chưa qua cả hai gate.

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
| **Primary actor** | **Tác giả truyện chữ** — người không biết vẽ, chủ sở hữu nội dung gốc (CF-1.5 `[CHỐT]`) |
| **Secondary actor** | **LLM condenser** (thực hiện phép nén, không có quyền quyết định cuối) · **Hệ thống** (Layout Director đã chốt layout, tính `text_budget`, ghi `change_log`, giữ trạng thái gate) |
| **Mốc MVP** | **MVP2** (`MVP-Scope` §3 hàng **C7** = `✅` từ MVP2; `❌` MVP0, `⛔` MVP1) |
| **BRD module** | [BRD-003 — Comic Director & Layout](../BRD/BRD-003-Comic-Director-And-Layout.md) |
| **Điều kiện tiên quyết** | **(P1)** Trang đã có **layout chốt** — mỗi panel đã có diện tích dưới dạng **toạ độ chuẩn hoá 0–1** trong `page_layout JSONB` và đã khai `text_safe_zone`. ⛔ **Ràng buộc thứ tự cứng: `dialogue condensation` phải chạy SAU layout**, vì `text_budget` phụ thuộc **diện tích panel** (`BR-003-12`, `Glossary` *dialogue condensation*) — đây là **ràng buộc**, không phải một tối ưu hoá. <br> **(P2)** Mỗi dòng thoại của trang đã có **speaker được xác nhận** ở [UC-04 — Human Gate: Speaker Attribution](./UC-04-Human-Gate-Speaker-Attribution.md), vì bản nén được đọc và duyệt **theo từng người nói**. ⚠️ **`TBD`** — nguồn chỉ nêu tường minh ràng buộc *"phải chạy sau layout"*; thứ tự **giữa hai gate** không được phát biểu trực tiếp ở đâu, `findings/business-analyst.md` §4.10 chỉ nói hai gate *"chỉ xong **cùng nhau**"*. Không suy diễn thêm. <br> **(P3)** `Panel Specification` của trang hợp lệ ở tầng DB (gồm CHECK constraint **≤3 nhân vật/panel**, `BR-003-05`/`M2-2`) |
| **Trạng thái kết thúc (thành công)** | Gate #2 của trang chuyển **PASS**; mỗi xác nhận/sửa đã sinh một `change_log` row; đường xuất bản trang **chỉ mở** khi cả gate #1 và gate #2 PASS |
| **Trạng thái kết thúc (thất bại)** | Gate #2 giữ nguyên **OPEN**. Trang **không thể** được xuất bản. Không tồn tại hành động nào của người dùng hay cấu hình nào của hệ thống làm nó xuất bản được |

---

## 2. Mục tiêu

### 2.1 Giá trị cho actor

Tác giả truyện chữ **giữ được quyền quyết định cuối cùng về nghĩa của lời nhân vật mình viết**.

`dialogue condensation` nén thoại gốc — với web-novel dịch thường **30–80 từ** — xuống mức bubble đọc thoải mái **~8–20 từ**, tức hệ số **2–5×** (`Glossary` *dialogue condensation*). Ở hệ số đó, đây **không phải** một phép định dạng: nó là **hành vi biên tập CÓ MẤT**. Cái bị mất có thể là sắc thái, có thể là một mệnh đề điều kiện, có thể là chính thông tin làm câu thoại đó tồn tại trong chương. Vì vậy nguồn kết luận: **cần LLM *và* cần người review** — không phải một trong hai.

Ba giá trị cụ thể actor nhận được:

| # | Giá trị | Vì sao actor cần nó |
|---|---|---|
| 1 | **Không bị âm thầm đổi nghĩa** | Một câu thoại nén sai nghĩa vẫn *"trông hợp lý"* trên trang. Không ai phát hiện được nó ngoài người đã viết bản gốc |
| 2 | **Thoại là phần được bảo hộ, và việc actor duyệt nó là bằng chứng** | Mỗi lần xác nhận / sửa sinh một `change_log` row (`BR-003-14`, **KC-2**). Prompt một mình **không** chứng minh được *"decisive contribution"*; *"người đã sửa thoại"* thì có |
| 3 | **Không phải tự đo chữ vừa bubble hay không** | Hệ thống tính `text_budget` từ diện tích panel và `text_safe_zone`; actor chỉ phán xét **nghĩa**, không phải kích thước |

### 2.2 Giá trị cho nền tảng

Gate này là một nửa của exit criterion **M2-4**. Nửa còn lại là [UC-04](./UC-04-Human-Gate-Speaker-Attribution.md), và **hai nửa chỉ "xong" cùng nhau** — vì M2-4 là thuộc tính của **pipeline xuất bản**, không của một màn hình (`findings/business-analyst.md` §4.10, `BR-003-13`).

---

## 3. Main flow

> Mỗi bước ghi rõ **actor nào làm**. Bước 9 là bước làm cho UC này trở thành *gate* thay vì *màn hình*.

| # | Actor | Hành động | Neo nguồn |
|---|---|---|---|
| 1 | **Hệ thống** | Đọc `page_layout JSONB` của trang đã chốt layout: với mỗi panel, lấy diện tích (toạ độ chuẩn hoá **0–1**) và `text_safe_zone` đã khai trong `Panel Specification` | `BR-003-04`, `BR-003-08` |
| 2 | **Hệ thống** | Tính **`text_budget`** cho từng bubble của từng panel **từ diện tích panel đó**. Đây là lý do bước này không thể chạy trước layout | `BR-003-12` · `Glossary` *dialogue condensation* |
| 3 | **Hệ thống** | Nạp **thoại gốc** của từng panel kèm **speaker đã xác nhận** ở [UC-04](./UC-04-Human-Gate-Speaker-Attribution.md) | (P2) |
| 4 | **LLM condenser** | Nén mỗi dòng thoại xuống `text_budget` tương ứng, trả về **bản nén** và **giữ nguyên bản gốc** (bản gốc không bị ghi đè) | `BR-003-11` |
| 5 | **Hệ thống** | Trình cho tác giả **từng cặp `gốc → nén`** theo thứ tự đọc của trang, kèm cờ cho những dòng **vẫn vượt `text_budget`** sau khi nén | `BR-003-11` |
| 6 | **Tác giả truyện chữ** | Đọc và **so sánh nghĩa** từng cặp: bản nén có còn nói đúng điều bản gốc nói không | §2.1 |
| 7 | **Tác giả truyện chữ** | Với **mỗi** dòng thoại, ra đúng một trong ba quyết định: **chấp nhận** bản nén · **sửa tay** · **yêu cầu nén lại** | §4 AF-1, AF-2 |
| 8 | **Hệ thống** | Ghi một **`change_log` row cho mỗi** quyết định ở bước 7 — kể cả khi quyết định chỉ là *"chấp nhận"*. Với dòng bị sửa tay, ghi `field_provenance` ở mức field | `BR-003-14` · **KC-2**, **KC-3** |
| 9 | **Hệ thống** | Chuyển gate #2 của trang sang **PASS** **chỉ khi 100%** dòng thoại của trang đã có một quyết định ở bước 7. Còn **một** dòng chưa quyết ⇒ gate vẫn **OPEN** | `M2-4` |
| 10 | **Hệ thống** | Mở đường xuất bản trang **chỉ khi cả gate #1 (speaker attribution) và gate #2 (điều kiện này) đều PASS**. ⛔ **Không tồn tại đường đi nào vòng qua bước này** — không có flag cấu hình, không có tham số API, không có role admin, không có nhánh *"tạm bypass để test"*. Điều kiện nghiệm thu là **sự VẮNG MẶT của đường code bypass**, không phải sự tồn tại của màn hình ở bước 5 | `M2-4` · `BR-003-13` |

> [!IMPORTANT]
> **Vì sao không có một Alternative flow "bỏ qua gate".**
> Trong một UC thông thường, nhánh *"người dùng chọn bỏ qua"* là một alternative flow hợp lệ. Ở đây nó **không tồn tại về mặt thiết kế**: rủi ro được xử lý ở `Roadmap` §3.3 là *"hai human gate bị **tạm bypass để test** rồi quên bật lại"*, và cách xử lý là đo bằng **sự vắng mặt của đường code**, **không** bằng cấu hình. Một nhánh bypass có điều kiện — dù chỉ dành cho môi trường test — **là** đường code bypass. Sự thiếu vắng nhánh đó trong mục 4 dưới đây là **có chủ ý**, không phải sót.

---

## 4. Alternative flow

| ID | Điều kiện kích hoạt | Luồng | Kết quả với gate |
|---|---|---|---|
| **AF-1** | Ở bước 7, tác giả **sửa tay** thay vì nhận bản nén của LLM | Tác giả nhập câu thoại của mình. Hệ thống kiểm câu đó so với `text_budget` và báo ngay nếu vượt (→ EX-1). Hệ thống ghi `change_log` + `field_provenance` cho field đó với `origin` phản ánh **do người viết** | Dòng đó tính là **đã quyết**. Gate tiến về PASS bình thường |
| **AF-2** | Ở bước 7, tác giả **yêu cầu nén lại** (kèm hoặc không kèm chỉ dẫn) | Quay lại bước 4 cho **riêng dòng đó**. ⚠️ Đây là một lần gọi **LLM cho text**, **không** phải một lần sinh ảnh — nó **không** tiêu chi phí image generation và **không** thuộc phạm vi *"generation không undo được"* của `BR-004-08` | Dòng đó **chưa quyết** cho tới khi tác giả chấp nhận hoặc sửa tay |
| **AF-3** | Thoại gốc **đã vừa** `text_budget`, LLM không cần nén gì | Hệ thống vẫn trình cặp `gốc → gốc` ở bước 5. **Tác giả vẫn phải xác nhận.** Không có nhánh *"tự động PASS vì không cần nén"* — nếu có, đó chính là một đường bypass theo dữ liệu | Cần một quyết định như mọi dòng khác |
| **AF-4** | Trang có panel **không có thoại** | Panel đó không sinh dòng nào để duyệt. Gate của **trang** vẫn tính trên tập dòng thoại thực có; trang không có dòng thoại nào thì gate #2 PASS ngay ở bước 9 do tập rỗng | PASS hợp lệ (tập rỗng), không phải bypass |
| **AF-5** | Tác giả muốn **chia một dòng thoại dài thành hai bubble** thay vì nén | ⚠️ **`TBD`** — nguồn hiện có (`MVP-Scope` §3 C6/C7, `Glossary` *dialogue condensation*, `BR-003-08`…`BR-003-14`) **không** nói gì về việc tách dòng thoại thành nhiều bubble. Không thiết kế thêm ở tầng UC này | `TBD` |

---

## 5. Exception flow

| ID | Ngoại lệ | Xử lý | Trạng thái gate |
|---|---|---|---|
| **EX-1** | Bản nén (hoặc bản sửa tay) **vẫn vượt `text_budget`** | Hệ thống **từ chối** đánh dấu dòng đó là đã quyết và nêu rõ mức vượt. Tác giả có đúng hai đường: **(a)** viết ngắn hơn; **(b)** sang [UC-08 — Arrange Page & Preview](./UC-08-Arrange-Page-And-Preview.md) để cấp cho panel đó diện tích lớn hơn. ⚠️ Đường (b) **đổi `text_budget`** ⇒ kích hoạt **EX-4** | **OPEN** |
| **EX-2** | Bản nén **làm mất nghĩa** — mất một mệnh đề, đổi sắc thái, hoặc bỏ chính thông tin làm câu thoại tồn tại | Tác giả **reject**. Hệ thống **không được** auto-accept sau một số lần reject, **không được** hạ tiêu chuẩn, **không được** đề nghị *"tạm chấp nhận và sửa sau"* — vì *"sửa sau"* khi trang đã xuất bản là đúng cái mà gate này tồn tại để ngăn. Tác giả sang AF-1 (sửa tay) hoặc AF-2 (nén lại) | **OPEN** cho tới khi có quyết định |
| **EX-3** | **LLM condenser lỗi / timeout / provider từ chối** ở bước 4 | Hệ thống báo lỗi và giữ dòng đó ở trạng thái **chưa có bản nén**. Cho phép thử lại, hoặc cho phép tác giả tự viết bản ngắn (AF-1). ⛔ **Không có nhánh *"LLM lỗi nên bỏ qua gate"*** — lỗi hạ tầng **không** sinh ra quyền xuất bản | **OPEN** |
| **EX-4** | **Layout của trang bị đổi SAU khi gate #2 đã PASS** (đổi template, swap panel, panel được cấp diện tích khác — [UC-08](./UC-08-Arrange-Page-And-Preview.md)) | Diện tích panel đổi ⇒ `text_budget` đổi ⇒ **bản nén đã duyệt không còn được duyệt trên đúng ràng buộc**. Hệ thống **reset gate #2 về OPEN** cho các dòng thuộc panel bị ảnh hưởng và yêu cầu xác nhận lại. Đây là hệ quả trực tiếp của `BR-003-12` (thứ tự cứng `layout → condensation`) | **OPEN** trở lại |
| **EX-5** | **Thoại bị sửa SAU khi gate #2 đã PASS**, qua [UC-07 — Edit Bubble & Dialogue In Panel](./UC-07-Edit-Bubble-And-Dialogue-In-Panel.md) | Hệ thống **reset trạng thái gate của đúng dòng thoại đó** về OPEN và yêu cầu xác nhận lại trước khi trang xuất bản được. Nếu không reset, sửa-thoại-sau-gate **chính là một đường bypass** và **M2-4 bị vi phạm** — dù màn hình gate vẫn tồn tại | **OPEN** trở lại cho dòng đó |
| **EX-6** | Tác giả rời giữa phiên duyệt (đóng tab, mất mạng) | Các dòng đã quyết giữ nguyên quyết định và `change_log` đã ghi; các dòng chưa quyết vẫn **chưa quyết**. Gate không tự PASS theo thời gian, **không có timeout dẫn tới auto-approve** | **OPEN** |

---

## 6. Tài liệu liên quan

### 6.1 Traceability

| Liên kết | Tài liệu | Điểm neo |
|---|---|---|
| Requirement gốc | [BRD-003 — Comic Director & Layout](../BRD/BRD-003-Comic-Director-And-Layout.md) | `BR-003-11` (gate #2) · `BR-003-12` (chạy sau layout) · `BR-003-13` (đo bằng vắng mặt đường bypass) · `BR-003-14` (`change_log` mỗi xác nhận) · `BR-003-08` (`text_safe_zone`) |
| Epic | [Epic-Comic-Director-And-Layout](../../022-User-Stories/Epics/Epic-Comic-Director-And-Layout.md) | Story `Story-Human-Gate-Dialogue-Condensation` |
| Sản phẩm | [PRD-Comic-Studio](../PRD-Comic-Studio.md) · [SRS-Comic-Studio](../SRS-Comic-Studio.md) | — |
| Gate song sinh | [UC-04 — Human Gate: Speaker Attribution](./UC-04-Human-Gate-Speaker-Attribution.md) | Hai gate chỉ *"xong"* **cùng nhau** (`findings/business-analyst.md` §4.10) |
| UC thượng nguồn | [UC-08 — Arrange Page & Preview](./UC-08-Arrange-Page-And-Preview.md) | Cấp `text_budget` cho UC này; đổi layout ⇒ **EX-4** |
| UC hạ nguồn | [UC-07 — Edit Bubble & Dialogue In Panel](./UC-07-Edit-Bubble-And-Dialogue-In-Panel.md) | Sửa thoại sau gate ⇒ **EX-5** |
| Exit criterion | [Roadmap](../../010-Planning/Roadmap.md) §2 | **M2-4** — *"hai human gate không bypass được: không tồn tại đường code nào xuất bản page mà chưa qua cả hai"* |
| Ranh giới scope | [MVP-Scope](../../010-Planning/MVP-Scope.md) §3 hàng **C7**, **C6** · §5.2 (ràng buộc `change_log` xuyên suốt) · §6 **KC-2**, **KC-3** | — |

### 6.2 Nguồn đã trích

| Nguồn | Phần | Dùng cho |
|---|---|---|
| [MVP-Scope.md](../../010-Planning/MVP-Scope.md) | §3 hàng **C6**, **C7** · §5.2 callout *ràng buộc xuyên suốt* · §6 **KC-2**, **KC-3** | Mốc MVP2, tính bắt buộc của gate, nghĩa vụ `change_log` |
| [Roadmap.md](../../010-Planning/Roadmap.md) | §2 exit criterion **M2-4** · §3.3 bảng rủi ro (*"tạm bypass để test rồi quên bật lại"*) | Cách đo gate, lý do không có nhánh bypass |
| [Glossary.md](../../999-Resources/Glossary.md) | *dialogue condensation* · *`text_safe_zone`* · *Panel Specification* · *Layout Director* | **30–80 từ → ~8–20 từ**, hệ số **2–5×**, *"phải chạy sau layout"*, *"hành vi biên tập có mất"* |
| [BRD-003-Comic-Director-And-Layout.md](../BRD/BRD-003-Comic-Director-And-Layout.md) | §3 `BR-003-04`, `BR-003-08`, `BR-003-11`…`BR-003-14` | Requirement gốc của mọi bước main flow |
| `docs/010-Planning/pm-runs/2026-08-24-khoi-tao-requirements-stories-comic-studio/findings/business-analyst.md` | §3.2 (hàng **UC-05**) · §4.10 (hai gate chỉ xong cùng nhau) · §5.3 lệnh cấm | Phạm vi UC, ràng buộc thứ tự, kỷ luật trích số |

> [!NOTE]
> **Quy ước nhãn nguồn số liệu** — kế thừa từ [MVP-Scope](../../010-Planning/MVP-Scope.md): `[OFF]` official/paper gốc · `[BCN]` báo cáo ngành có tên firm · `[TC]` nguồn thứ cấp · `[EM]` **ước lượng, không phải số đo** · `[CHỐT]` quyết định của founder tại gate. Copy một con số sang tài liệu khác thì **copy cả nhãn**.
