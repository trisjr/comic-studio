---
id: UC-07
type: use-case
status: draft
project: comic-studio
created: 2026-08-24
---

# UC-07 — Sửa bubble và thoại trong một panel

> Part of: [Epic-Minimum-Editor](../../022-User-Stories/Epics/Epic-Minimum-Editor.md) · [Epic-Image-Generation-Pipeline](../../022-User-Stories/Epics/Epic-Image-Generation-Pipeline.md)
> Requirement gốc: [BRD-004 — Minimum Editor](../BRD/BRD-004-Minimum-Editor.md) (`BR-004-04`, `BR-004-06`, `BR-004-08`) + [BRD-001 — Image Generation Pipeline](../BRD/BRD-001-Image-Generation-Pipeline.md) (`BR-001-03`)

> [!CAUTION]
> **Hai ranh giới của UC này, cả hai đều là ranh giới cứng:**
> 1. ⛔ **`typeset layer` tách khỏi ảnh — KHÔNG nướng chữ vào pixel.** Ảnh được sinh **không có chữ** (`text, letters, watermark, speech bubble` nằm ở **negative prompt**); bubble và thoại được render bằng **code** lên trên. Không có tầng này thì **sửa một câu thoại = một lần regenerate ảnh** (`Glossary` *typeset layer*, `BR-001-03`). Ngưỡng nghiệm thu **G1-e**: **100%** panel có thoại dùng overlay, **0** panel nhờ model render chữ.
> 2. ⛔ **Phạm vi bị giới hạn trong MỘT panel.** `MVP-Scope` §5.2 thành phần **#2** ghi nguyên văn: đây là *"canvas bị giới hạn trong một khung"*, **không** phải scene graph tự do. **KHÔNG** infinite canvas (**D2** hoãn), **KHÔNG** inpainting brush (**D5** hoãn), **KHÔNG** undo xuyên state phân tán (**D3** — chỉ undo **cục bộ**, và **không undo qua generation** vì đã tiêu tiền thật).

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
| **Secondary actor** | **Hệ thống** (render `typeset layer` bằng code, hiển thị `text_safe_zone`, kiểm `text_budget`, ghi `change_log` + `field_provenance`, giữ trạng thái human gate #2). ⛔ **Không có secondary actor nào là image provider trong UC này** — mọi thao tác ở đây **không gọi image generation** |
| **Mốc MVP** | **MVP0** — typeset `🟡` **thô** (`MVP-Scope` §3 hàng **A2**; CF-8.11c: *"nổ ngay ở panel có thoại đầu tiên, tức trong MVP0"*) → **MVP2** bắt đầu thành phần **#2** của editor tối thiểu → **MVP3** hoàn tất (`MVP-Scope` §5.2 #2, **5–8%** `[EM]`) |
| **BRD module** | [BRD-001 — Image Generation Pipeline](../BRD/BRD-001-Image-Generation-Pipeline.md) + [BRD-004 — Minimum Editor](../BRD/BRD-004-Minimum-Editor.md) |
| **Điều kiện tiên quyết** | **(P1)** Panel đã có **một ảnh được chọn** từ [UC-06](./UC-06-Generate-Panel-And-Pick-Variant.md), và ảnh đó **không chứa chữ**. <br> **(P2)** `Panel Specification` của panel đã khai **`text_safe_zone`** — vùng được giữ trống để đặt bubble (`BR-003-08`; thiếu nó thì bubble che mặt nhân vật và **phải sinh lại toàn bộ ảnh đã làm**). <br> **(P3)** Panel đã có **layout** (diện tích panel) ⇒ có `text_budget`, vì `text_budget` phụ thuộc diện tích panel (`BR-003-12`). <br> **(P4)** Mỗi dòng thoại đã có **speaker xác nhận** ở [UC-04](./UC-04-Human-Gate-Speaker-Attribution.md) — đuôi trỏ (tail) phải trỏ về **một người nói xác định** |
| **Trạng thái kết thúc (thành công)** | `typeset layer` của panel được cập nhật; **mỗi** thao tác của actor đã sinh một `change_log` row; **không có** lần gọi image generation nào phát sinh; nếu nội dung thoại bị đổi thì trạng thái gate #2 của dòng đó đã được **reset về OPEN** |
| **Trạng thái kết thúc (thất bại)** | `typeset layer` giữ nguyên trạng thái trước đó (undo **cục bộ** khả dụng). Ảnh panel **không** bị ảnh hưởng — vì chữ chưa bao giờ nằm trong pixel của nó |

---

## 2. Mục tiêu

### 2.1 Giá trị cho actor

Tác giả truyện chữ **đặt được bubble và viết được thoại của mình lên panel mà không lần nào phải đốt thêm tiền API**.

`MVP-Scope` §5.2 thành phần **#2** nêu **ba lý do độc lập** khiến thành phần này bắt buộc — độc lập nghĩa là **bác một lý do vẫn còn hai lý do kia**:

| Lý do | Phát biểu | Giá trị actor nhận |
|---|---|---|
| **(a)** | **Thoại do người viết là phần được bảo hộ** | Việc actor viết / sửa thoại là đóng góp trí tuệ có thể chứng minh (`change_log` + `field_provenance`, **KC-2**, **KC-3**) |
| **(b)** | **Bubble che mặt là lỗi không thể tự động tránh** | Actor có quyền kéo bubble đi chỗ khác, thay vì chấp nhận một trang bị hỏng |
| **(c)** | **Không sửa được thoại thì mọi lần sửa chữ thành một lần regenerate ảnh — *đốt tiền*** | Sửa chữ **không** tiêu credit sinh ảnh. Đây là hệ quả trực tiếp của `typeset layer` |

### 2.2 Ranh giới — cái UC này KHÔNG làm

| Không thuộc UC-07 | Vì sao / thuộc đâu |
|---|---|
| Sửa **pixel của ảnh** (xoá vật thể, vẽ thêm, tô lại) | ⛔ **Inpainting brush / drawing tools = D5, HOÃN** (`MVP-Scope` §3 D5, §5.3 #9). Đường duy nhất để đổi nội dung ảnh là sửa spec + sinh lại ở [UC-06](./UC-06-Generate-Panel-And-Pick-Variant.md) — **tiêu tiền thật** |
| Kéo bubble **sang panel khác**, zoom/pan cả chapter, panel xoay / không chữ nhật | ⛔ **Infinite canvas = D2, HOÃN.** Phạm vi là *"canvas bị giới hạn trong một khung"* (`MVP-Scope` §5.2 #2, §5.3 #6) |
| Undo **xuyên toàn bộ state phân tán**, undo một lần generate | ⛔ **D3, HOÃN.** Chỉ undo **cục bộ** (trong form + vị trí bubble). **Không undo qua generation** — `Regenerate` tiêu tiền thật, không hoàn lại. UX **phải nói rõ**, không để actor suy đoán (`BR-004-08`) |
| Chọn template trang, đổi chỗ panel, xem trang thành phẩm | [UC-08](./UC-08-Arrange-Page-And-Preview.md) |
| **Nén** thoại và **xác nhận** bản nén | [UC-05](./UC-05-Human-Gate-Dialogue-Condensation.md) — UC-07 **không** thay thế gate đó (xem **EX-6**) |
| Thêm / bớt nhân vật trong panel, đổi camera | [UC-03](./UC-03-Review-Panel-Script.md) (sửa `Panel Specification`) — xem **EX-7** |
| Chi tiết giao diện: nút nằm đâu, màu gì, kích thước bao nhiêu | Thuộc tầng `docs/040-Design/` — **ngoài scope** của tài liệu Use Case |

---

## 3. Main flow

> Trạng thái đích **MVP3** (thành phần #2 hoàn tất). Trạng thái **MVP0** (typeset thô) ở **AF-1**.
> Mỗi bước ghi rõ **actor nào làm**. Bước 7 là bước mang toàn bộ giá trị kinh tế của UC này.

| # | Actor | Hành động | Neo nguồn |
|---|---|---|---|
| 1 | **Tác giả truyện chữ** | Mở **một** panel đã có ảnh được chọn để sửa bubble/thoại | `BR-004-04` |
| 2 | **Hệ thống** | Render ảnh panel (**không chữ**) làm nền, và `typeset layer` **tách rời** phía trên. Hiển thị **`text_safe_zone`** đã khai trong `Panel Specification` như vùng được giữ trống để đặt bubble | `BR-001-03`, `BR-003-08` |
| 3 | **Hệ thống** | Nạp các dòng thoại của panel kèm **speaker** đã xác nhận, đặt mỗi bubble ở vị trí mặc định **trong `text_safe_zone`** | (P4) · `BR-003-08` |
| 4 | **Tác giả truyện chữ** | **Kéo bubble** tới vị trí mong muốn **trong phạm vi panel này** | `BR-004-04` |
| 5 | **Tác giả truyện chữ** | **Sửa nội dung thoại** trong bubble | `BR-004-04` — lý do (a) |
| 6 | **Tác giả truyện chữ** | **Chọn kiểu bubble** và **kéo đuôi trỏ (tail)** về phía người nói. ⚠️ **`TBD`** — nguồn chỉ ghi *"chọn kiểu"*; **danh mục kiểu bubble cụ thể chưa được định nghĩa ở đâu trong repo**, và tài liệu này **không tự đặt ra** | `BR-004-04` |
| 7 | **Hệ thống** | Render mọi thay đổi ở bước 4–6 **bằng code lên `typeset layer`**. ⛔ **Không gọi image generation. Không ghi chữ vào pixel của ảnh. Không tiêu một credit sinh ảnh nào** | `BR-001-03` · `G1-e` |
| 8 | **Hệ thống** | Kiểm câu thoại vừa sửa so với **`text_budget`** của panel và báo ngay nếu vượt (→ **EX-2**); kiểm bubble có đè ra ngoài `text_safe_zone` hay không (→ **EX-1**) | `BR-003-12`, `M2-3` |
| 9 | **Hệ thống** | Ghi một **`change_log` row cho mỗi** thao tác của actor — kéo bubble, sửa thoại, đổi kiểu, kéo tail. Với thoại do actor tự viết, ghi `field_provenance` ở mức field với `origin` phản ánh **do người viết**. Bản ghi **commit cùng một transaction** với artifact | `BR-004-06` · **KC-2**, **KC-3**, **KC-4** |
| 10 | **Hệ thống** | ⛔ Nếu **nội dung thoại** bị đổi ở bước 5 mà dòng đó **đã PASS** human gate #2, **reset trạng thái gate #2 của đúng dòng đó về OPEN** và yêu cầu xác nhận lại ở [UC-05](./UC-05-Human-Gate-Dialogue-Condensation.md). **Không reset = tạo ra một đường bypass ⇒ vi phạm `M2-4`** — dù màn hình gate vẫn tồn tại | `M2-4` · `BR-003-13` |
| 11 | **Tác giả truyện chữ** | Kết thúc phiên sửa. Xem panel trong ngữ cảnh cả trang ở [UC-08](./UC-08-Arrange-Page-And-Preview.md) | `BR-004-03` |

> [!IMPORTANT]
> **Bước 7 là lý do UC này tồn tại.** Nếu bước 7 được hiện thực bằng cách nhờ model render chữ, thì UC-07 vẫn *"chạy được"* trên màn hình nhưng: **(i)** exit criterion **G1-e** FAIL (yêu cầu **0** panel nhờ model render chữ); **(ii)** mọi lần sửa chữ trở thành một lần **regenerate ảnh** — đúng cái mà lý do (c) tồn tại để ngăn.

---

## 4. Alternative flow

| ID | Điều kiện kích hoạt | Luồng | Ghi chú mốc |
|---|---|---|---|
| **AF-1** | **MVP0 — typeset `🟡` thô** | Không có editor tương tác: bubble + thoại được composite bằng **script** lên ảnh panel, vị trí lấy từ file cấu hình viết tay. ⛔ **Vẫn bắt buộc phải có**, ngay ở **panel có thoại đầu tiên** — bỏ qua typeset ở MVP0 nghĩa là mọi đánh giá consistency được thực hiện trên **ảnh không có chữ**, tức **đánh giá sai đối tượng** (`Roadmap` §4 hàng **X-c**, CF-8.11c) | **MVP0** · `MVP-Scope` §3 **A2** |
| **AF-2** | Actor **giữ nguyên vị trí bubble mặc định** mà hệ thống đặt trong `text_safe_zone` | Không có thao tác nào ⇒ **không sinh `change_log` row** ở bước 9 cho vị trí. `change_log` ghi **hành động của người dùng**, không ghi trạng thái mặc định của hệ thống | MVP2+ |
| **AF-3** | Panel **không có thoại** | `typeset layer` của panel rỗng. UC kết thúc ngay sau bước 2 — không có bubble nào để kéo | MVP0+ |
| **AF-4** | Actor **hoàn tác** một thao tác vừa làm | Undo **cục bộ** trong phạm vi form + vị trí bubble được phép. ⛔ Undo **không** vượt ra khỏi phạm vi đó và **không** đi qua một lần generation (→ **EX-3**) | `BR-004-08` · `MVP-Scope` §5.3 #7 |
| **AF-5** | Actor sửa thoại **trước khi** gate #2 chạy lần đầu | Không có gì để reset ở bước 10 — dòng đó chưa từng PASS. Bản do actor viết trở thành đầu vào của [UC-05](./UC-05-Human-Gate-Dialogue-Condensation.md) và **vẫn phải đi qua gate** (`UC-05` AF-3: không có nhánh tự động PASS) | MVP2 |
| **AF-6** | Actor muốn thêm **SFX / narration box / caption** ngoài bubble thoại | ⚠️ **`TBD`** — nguồn (`MVP-Scope` §5.2 #2, `BR-004-04`) chỉ liệt kê **bốn** thao tác: *kéo bubble, sửa thoại, chọn kiểu, kéo đuôi trỏ*. Không thiết kế thêm ở tầng UC này | `TBD` |

---

## 5. Exception flow

| ID | Ngoại lệ | Xử lý | Ranh giới cần giữ |
|---|---|---|---|
| **EX-1** | **Bubble đè ra ngoài `text_safe_zone` / che mặt nhân vật** | Hệ thống **cảnh báo** và chỉ rõ vùng vi phạm; actor kéo bubble về vùng an toàn hoặc chấp nhận có ý thức. Ngưỡng nghiệm thu: typeset **không đè vùng mặt** ở **≥95%** panel. ⚠️ **`[EM]`** — `Roadmap` §2 **M2-3** ghi nguyên văn *"ngưỡng do em định nghĩa"*; **cấm** trích như số đo hoặc benchmark ngành (`BR-003-09`) | Đây là **cảnh báo**, đúng bản chất `M2-3` (ngưỡng tỷ lệ). ⛔ Không nhầm với `M2-2` — thứ **bị TỪ CHỐI ở tầng DB** là **số nhân vật/panel**, không phải vị trí bubble (xem **EX-7**) |
| **EX-2** | **Câu thoại vừa sửa vượt `text_budget`** của panel | Hệ thống báo mức vượt. Actor có đúng ba đường: **(a)** viết ngắn hơn; **(b)** sang [UC-05](./UC-05-Human-Gate-Dialogue-Condensation.md) nén lại; **(c)** sang [UC-08](./UC-08-Arrange-Page-And-Preview.md) cấp cho panel diện tích lớn hơn. ⚠️ Đường (c) đổi `text_budget` ⇒ kích hoạt `UC-05` **EX-4** (reset gate) | `text_budget` phụ thuộc **diện tích panel** ⇒ mọi đường xử lý đều dẫn về ràng buộc cứng `layout → condensation` (`BR-003-12`) |
| **EX-3** | Actor muốn **undo một lần generate ảnh** (hoặc undo xuyên nhiều state) | ⛔ **Từ chối.** Không có undo qua generation: một `Regenerate` **tiêu tiền thật và không hoàn lại được**. Hệ thống **phải nói rõ** điều này ở UX thay vì để actor phát hiện sau. Undo xuyên toàn bộ state phân tán là **D3 — hoãn**, và `MVP-Scope` §5.3 #7 ghi điều kiện mở lại là *"không mở lại theo dạng này"* | `BR-004-08` |
| **EX-4** | Actor muốn **sửa nội dung ảnh** (xoá vật thể, vẽ thêm, tô lại) trong khi đang sửa bubble | ⛔ **Không có công cụ nào trong UC này làm được việc đó** — inpainting brush / drawing tools là **D5, hoãn**. Đường hợp lệ duy nhất: sửa `Panel Specification` ở [UC-03](./UC-03-Review-Panel-Script.md) rồi sinh lại ở [UC-06](./UC-06-Generate-Panel-And-Pick-Variant.md) — **tiêu credit thật**. Khi D5 được mở lại, bắt buộc set `generation.origin = 'ai_edited'` | `MVP-Scope` §3 **D5** · §5.3 #9 |
| **EX-5** | Actor kéo bubble **ra ngoài khung panel** / muốn làm việc trên nhiều panel cùng lúc | ⛔ Hệ thống **giới hạn thao tác trong khung panel đang mở**. Phạm vi là *"canvas bị giới hạn trong một khung"*; infinite canvas là **D2, hoãn** (chi phí lớn nhất, giá trị tăng thêm nhỏ nhất). Muốn làm việc ở cấp trang thì sang [UC-08](./UC-08-Arrange-Page-And-Preview.md) | `MVP-Scope` §5.2 #2 · §5.3 #6 |
| **EX-6** | Thoại bị sửa **sau khi** human gate #2 đã PASS, và hệ thống **không** reset gate | ⛔ **Đây là một khiếm khuyết của pipeline xuất bản, không phải một lựa chọn của người dùng.** Nếu tồn tại, nó **là** một đường bypass và **`M2-4` FAIL** — vì `M2-4` đo *"không tồn tại đường code nào xuất bản page mà chưa qua cả hai gate"*, chứ không đo sự tồn tại của màn hình gate. Hành vi đúng: bước 10 của main flow **reset gate #2 về OPEN** cho dòng đó | `M2-4` · `BR-003-13` · [UC-05](./UC-05-Human-Gate-Dialogue-Condensation.md) **EX-5** |
| **EX-7** | Actor muốn **thêm một nhân vật vào panel** (ví dụ để có người thứ tư cho đuôi trỏ chỉ tới) | ⛔ Việc này **không** nằm trong UC-07 — nó là sửa `Panel Specification` ([UC-03](./UC-03-Review-Panel-Script.md)). Và nếu panel đã có 3 nhân vật thì thao tác đó **bị DB TỪ CHỐI**: trần **≤3 nhân vật/panel** là **CHECK constraint ở tầng DB** — *insert panel 4 nhân vật **bị từ chối**, **không phải** bị cảnh báo* (`M2-2`). Đường hợp lệ: giải cảnh đông người bằng **shot xa / silhouette / crop** (`BR-003-07`) | Căn cứ CF-6.5 `[OFF]`: ID-Sim **42.33** (2 nhân vật) → **27.21** (3) → **2.67** (4) → **0.52** (5). Từ 4 nhân vật, `attribute binding` thất bại gần hoàn toàn |
| **EX-8** | **Ảnh panel bị thay** (actor sinh lại và chọn candidate khác ở [UC-06](./UC-06-Generate-Panel-And-Pick-Variant.md)) sau khi bubble đã đặt xong | Vì `typeset layer` **tách khỏi ảnh**, nội dung thoại **không** mất theo ảnh. Nhưng vị trí bubble được đặt theo ảnh cũ có thể không còn phù hợp với ảnh mới ⇒ actor cần kiểm lại. ⚠️ **`TBD`** — nguồn **không** phát biểu hành vi hệ thống trong tình huống này (giữ nguyên vị trí, hay đặt lại vào `text_safe_zone`, hay cảnh báo). Không suy diễn thêm | `BR-001-03` (tách tầng) cho phần *"thoại không mất"*; phần hành vi còn lại là `TBD` |

---

## 6. Tài liệu liên quan

### 6.1 Traceability

| Liên kết | Tài liệu | Điểm neo |
|---|---|---|
| Requirement gốc (editor) | [BRD-004 — Minimum Editor](../BRD/BRD-004-Minimum-Editor.md) | `BR-004-04` (kéo bubble / sửa thoại / chọn kiểu / kéo đuôi trỏ trong **MỘT** panel; ba lý do a/b/c) · `BR-004-06` (`change_log` mọi hành động) · `BR-004-08` (undo cục bộ, không undo qua generation) |
| Requirement gốc (pipeline) | [BRD-001 — Image Generation Pipeline](../BRD/BRD-001-Image-Generation-Pipeline.md) | `BR-001-03` (`typeset layer` tách khỏi ảnh, negative prompt, ngưỡng **G1-e**) |
| Requirement liên đới | [BRD-003 — Comic Director & Layout](../BRD/BRD-003-Comic-Director-And-Layout.md) | `BR-003-08` (`text_safe_zone`) · `BR-003-09` (ngưỡng **≥95%** `[EM]`) · `BR-003-12` (`text_budget` theo diện tích panel) · `BR-003-13` (đo gate bằng vắng mặt đường bypass) |
| Epic | [Epic-Minimum-Editor](../../022-User-Stories/Epics/Epic-Minimum-Editor.md) · [Epic-Image-Generation-Pipeline](../../022-User-Stories/Epics/Epic-Image-Generation-Pipeline.md) | `Story-Bubble-Text-Overlay-Editor` · `Story-Typeset-Layer-And-Bubble-Overlay` |
| Sản phẩm | [PRD-Comic-Studio](../PRD-Comic-Studio.md) · [SRS-Comic-Studio](../SRS-Comic-Studio.md) | — |
| UC thượng nguồn | [UC-06](./UC-06-Generate-Panel-And-Pick-Variant.md) | Nguồn của ảnh panel **không chữ** (P1) |
| UC liên đới | [UC-04](./UC-04-Human-Gate-Speaker-Attribution.md) · [UC-05](./UC-05-Human-Gate-Dialogue-Condensation.md) · [UC-08](./UC-08-Arrange-Page-And-Preview.md) | Speaker cho đuôi trỏ · gate #2 bị reset khi sửa thoại (**EX-6**) · `text_budget` và ngữ cảnh trang |
| Exit criterion | [Roadmap](../../010-Planning/Roadmap.md) §2, §4 | **G1-e** · **M2-3** (≥95% `[EM]`) · **M2-4** · hàng **X-c** (typeset ở panel có thoại đầu tiên) |
| Ranh giới scope | [MVP-Scope](../../010-Planning/MVP-Scope.md) §3 hàng **A2**, **D1**, **D2**, **D3**, **D5** · §5.2 thành phần **#2** · §5.3 **#6**, **#7**, **#9** · §6 **KC-2**…**KC-4** | — |

### 6.2 Nguồn đã trích

| Nguồn | Phần | Dùng cho |
|---|---|---|
| [MVP-Scope.md](../../010-Planning/MVP-Scope.md) | §3 **A2**, **D1**–**D5** · §5.2 thành phần **#2** (*"canvas bị giới hạn trong một khung"*, **5–8%** `[EM]`, ba lý do a/b/c) + callout `change_log` · §5.3 **#6**, **#7**, **#9** · §6 **KC-2**, **KC-3**, **KC-4** | Phạm vi một panel, các thành phần bị hoãn, nghĩa vụ provenance |
| [Roadmap.md](../../010-Planning/Roadmap.md) | §2 **M2-3**, **M2-4** · §3.1 việc 2 (bẫy *"bỏ qua typeset"*) · §4 hàng **X-c** | Ngưỡng đo, lý do typeset phải có từ MVP0 |
| [Glossary.md](../../999-Resources/Glossary.md) | *typeset layer* · *`text_safe_zone`* · *dialogue condensation* · *Panel Specification* · *attribute binding* | Định nghĩa canon các term |
| [BRD-001](../BRD/BRD-001-Image-Generation-Pipeline.md) · [BRD-003](../BRD/BRD-003-Comic-Director-And-Layout.md) · [BRD-004](../BRD/BRD-004-Minimum-Editor.md) | §3 bảng yêu cầu nghiệp vụ | Requirement gốc mọi bước |
| `docs/010-Planning/pm-runs/2026-08-24-khoi-tao-requirements-stories-comic-studio/findings/business-analyst.md` | §3.2 (hàng **UC-07**) · §5.3 lệnh cấm | Phạm vi UC, kỷ luật trích số |

> [!NOTE]
> **Quy ước nhãn nguồn số liệu** — kế thừa từ [MVP-Scope](../../010-Planning/MVP-Scope.md): `[OFF]` official/paper gốc · `[BCN]` báo cáo ngành có tên firm · `[TC]` nguồn thứ cấp · `[EM]` **ước lượng, không phải số đo** · `[CHỐT]` quyết định của founder tại gate. Copy một con số sang tài liệu khác thì **copy cả nhãn** (`CẤM-15`).
