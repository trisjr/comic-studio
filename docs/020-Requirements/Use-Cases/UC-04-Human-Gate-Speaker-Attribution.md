---
id: UC-04
type: use-case
status: draft
project: comic-studio
created: 2026-08-24
---

# UC-04 — Human gate: xác nhận speaker attribution

> [!CAUTION]
> **Đây là một HUMAN GATE BẮT BUỘC, không bypass được.** Tiêu chí nghiệm thu của nó — `Roadmap` §2 exit criterion **M2-4** — được đo bằng **sự VẮNG MẶT của một đường code bypass**, **không** bằng sự tồn tại của một màn hình xác nhận. CF-8.8: gate này *"không phải tuỳ chọn, không dồn sang MVP4"*.

> [!IMPORTANT]
> **Quy ước nhãn nguồn số liệu** (kế thừa nguyên vẹn từ bảng Canonical Facts — **số và nhãn là một cặp không tách rời**):
> `[OFF]` official/paper gốc · `[BCN]` báo cáo ngành có tên firm · `[TC]` thứ cấp · `[EM]` ước lượng hoặc phép nhân, **không phải số đo** · `[CHỐT]` quyết định của Founder tại gate.

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
| **Primary actor** | **Tác giả truyện chữ** (không biết vẽ) — CF-1.5 `[CHỐT]`. ⛔ **CẤM-17**: không đặt requirement cho phân khúc hoạ sĩ |
| **Secondary actor** | **LLM** (đề xuất gán người nói) · **Hệ thống** (pipeline xuất bản — nơi gate được **cưỡng chế**, và nơi `change_log` được ghi) |
| **Mốc MVP** | **MVP2** — `MVP-Scope` §3 hàng `C7` ✅ (MVP0 = ❌, MVP1 = ⛔). ⛔ **Không** dồn sang MVP4 (CF-8.8) |
| **BRD module** | [BRD-003 — Comic Director And Layout](../BRD/BRD-003-Comic-Director-And-Layout.md) (`BR-003-10`, `BR-003-13`, `BR-003-14`) |
| **Điều kiện tiên quyết (precondition)** | (1) [UC-03](./UC-03-Review-Panel-Script.md) đã hoàn tất: panel script — **Comic IR (Comic Intermediate Representation)** — của chapter đã được tác giả duyệt, mỗi panel có `text_safe_zone`. (2) Layout đã xong — vì gate thứ hai ([UC-05](./UC-05-Human-Gate-Dialogue-Condensation.md)) **phải chạy SAU layout** do `text_budget` phụ thuộc diện tích panel (`BR-003-12`). (3) `change_log` + `field_provenance` sẵn sàng và commit **cùng transaction** với artifact (`KC-2`, `KC-3`, `KC-4`). (4) ⚠️ **`TBD` (KT-1)** — actor là **phân khúc** đã chốt (CF-1.5), **không phải một persona**; xem `findings/business-analyst.md` §6.2 `KT-1` |

## 2. Mục tiêu

Tác giả xác nhận rằng **mỗi dòng thoại trong chapter được gán đúng người nói**. Đây là một trong hai điểm trong toàn pipeline mà một con người **bắt buộc** phải ra quyết định trước khi trang được xuất bản.

Lý do gate này tồn tại là **chi phí lỗi bất đối xứng**: `Glossary` *speaker attribution* ghi nguyên văn — *"một dòng gán sai làm hỏng cả trang trong mắt người đọc"*. Không có một cơ chế tự động nào bù lại được điều đó. Một panel có màu sai thì trang vẫn đọc được; một câu thoại gán cho sai nhân vật thì người đọc **mất niềm tin vào cả trang**, và họ không quay lại đọc phần còn lại để kiểm chứng.

Con số làm gate này thành nghĩa vụ chứ không phải một tính năng — **trích nguyên nhãn và nguyên caveat**:

| Tình huống | Tỉ lệ lỗi speaker attribution | Nhãn |
|---|---|---|
| **3+ người nói, có tự sự chen vào** | **30–50%** | ⚠️ `[EM]` |
| **Câu ngắn / thán từ** | **40–60%** | ⚠️ `[EM]` |

> **Điều kiện của hai con số trên**: đó là tỉ lệ lỗi **nếu không có anchor + constrained decoding** (`Glossary` *speaker attribution*; CF-6.10).
> ⚠️ **CF-6.10 là ƯỚC LƯỢNG, KHÔNG PHẢI SỐ ĐO.** `findings/business-analyst.md` §5.2 ghi nguyên văn: *"Ước lượng, KHÔNG phải số đo. Chi phí lỗi **bất đối xứng** — một dòng gán sai làm hỏng cả trang"*. `BRD-003` §3 xếp *"tỉ lệ lỗi thật của speaker attribution"* vào `TBD` (`G-04`): **không có benchmark nào đo speaker attribution trên văn bản truyện chữ tiếng Việt ở cấu hình này** ⇒ MVP2 **thiết kế như thể tỉ lệ lỗi ở cận trên**.
> ⚠️ **Anchor + constrained decoding là ĐIỀU KIỆN trong phát biểu ước lượng, không phải một tính năng được thiết kế trong use case này.** Gate tồn tại **bất kể** hệ thống có dùng chúng hay không — vì chính tỉ lệ lỗi là `TBD`.

## 3. Main flow

| # | Actor | Bước |
|---|---|---|
| 1 | **Hệ thống** | Sau khi panel script được duyệt và layout đã xong, tách các dòng thoại của chapter theo panel mà chúng thuộc về |
| 2 | **LLM** | **Đề xuất** người nói cho từng dòng thoại, dựa trên văn bản gốc và danh sách nhân vật có mặt trong panel (≤3 nhân vật/panel theo `BR-003-05`) |
| 3 | **Hệ thống** | Đặt mọi dòng thoại vào trạng thái **`chưa xác nhận`**. ⛔ **Không có trạng thái mặc định nào là *"đã xác nhận"***: đề xuất của LLM **không** tự trở thành xác nhận của con người |
| 4 | **Tác giả** | Mở gate speaker attribution của chapter và đọc từng dòng thoại kèm người nói được đề xuất |
| 5 | **Tác giả** | Với **mỗi** dòng thoại: **xác nhận** người nói được đề xuất, hoặc **gán lại** cho nhân vật khác trong panel |
| 6 | **Hệ thống** | Mỗi lần xác nhận / sửa ở bước 5 sinh một **`change_log`** row — xác nhận của con người là **bằng chứng đóng góp trí tuệ**, không chỉ là một bước UI (`BR-003-14`, `KC-2`); ghi kèm `field_provenance` (`KC-3`) và **commit cùng một transaction** với chính dòng thoại (`KC-4`) |
| 7 | **Hệ thống** | Đếm số dòng thoại còn ở trạng thái `chưa xác nhận` của chapter |
| 8 | **Hệ thống** | ⛔ **Cưỡng chế gate**: nếu số ở bước 7 **> 0**, page/chapter **KHÔNG thể xuất bản**. **KHÔNG TỒN TẠI đường code nào xuất bản page mà chưa qua gate này — kể cả cờ cấu hình, kể cả chế độ *"auto-approve"*** (`BRD-003` §5 mục 6; `Roadmap` §2 **M2-4**) |
| 9 | **Tác giả** | Đi tiếp sang gate thứ hai — [UC-05 — dialogue condensation](./UC-05-Human-Gate-Dialogue-Condensation.md). **Hai gate chỉ *"xong"* CÙNG NHAU**, vì tiêu chí `M2-4` là thuộc tính của **pipeline xuất bản**, không phải của một màn hình (`BR-003-13`) |
| 10 | **Hệ thống** | Chỉ khi **cả hai** gate đã hoàn tất cho một page, page đó mới đủ điều kiện xuất bản |

> [!CAUTION]
> **Nói tường minh, vì đây là toàn bộ nội dung của exit criterion `M2-4`: KHÔNG CÓ ĐƯỜNG ĐI NÀO VÒNG QUA BƯỚC NÀY.**
>
> | Đường bị cấm | Vì sao |
> |---|---|
> | Cờ cấu hình / feature flag *"tắt gate"* | `Roadmap` §2 **M2-4** đo bằng **sự VẮNG MẶT của đường code bypass**. Một cờ tồn tại nghĩa là đường tồn tại, dù mặc định đang tắt |
> | Chế độ *"auto-approve"* khi LLM tự tin cao | `BRD-003` §5 mục 6 ghi rõ: **kể cả chế độ *"auto-approve"***. Tỉ lệ lỗi thật là `TBD` (`G-04`) ⇒ *"tự tin cao"* không có căn cứ đo được để làm ngưỡng |
> | Batch approve *"xác nhận tất cả"* mà không đọc | Xác nhận là **bằng chứng đóng góp trí tuệ** (`BR-003-14`, CF-7.2 `[OFF]` Điều 5a). Một cú click cho 200 dòng không phải là 200 quyết định |
> | Dồn gate sang MVP4 | CF-8.8: *"không phải tuỳ chọn, **không dồn sang MVP4**"*. `MVP-Scope` §3 `C7` = ✅ tại **MVP2** |
> | Bỏ qua gate cho page *"chỉ có một nhân vật"* | Xem [`ALT-2`](#4-alternative-flow) — nhánh đó **giảm công**, **không** bỏ gate. Trạng thái `chưa xác nhận` vẫn phải chuyển thành `đã xác nhận` bởi một hành động của con người |
>
> `BRD-003` §5 mục 6 ghi điều kiện mở lại là: **không mở lại trong Full Scope**.

## 4. Alternative flow

| # | Nhánh | Diễn biến |
|---|---|---|
| **ALT-1** | **Tác giả xác nhận theo từng page thay vì cả chapter** | Bước 4–6 chạy ở phạm vi một page. Bước 8 cưỡng chế **ở cấp page**: page nào đủ thì page đó xuất bản được, page khác vẫn bị chặn. Đây là nhánh **giảm kích thước lô công việc của con người** — đơn vị đo của một HITL gate là **giờ-người**, không phải token (`Glossary` *HITL gate*) |
| **ALT-2** | **Panel chỉ có đúng MỘT nhân vật có mặt** | Hệ thống hiển thị dòng thoại kèm người nói **duy nhất khả dĩ**, nên bước 5 rút xuống một cú xác nhận. ⛔ **Đây là giảm công, KHÔNG phải bỏ gate**: trạng thái `chưa xác nhận` chỉ chuyển sang `đã xác nhận` bằng **một hành động của con người**, và hành động đó vẫn sinh `change_log` |
| **ALT-3** | **Tác giả sửa lại chính nội dung thoại trong khi đang gán người nói** | Được phép; nhưng nội dung thoại là artifact của gate thứ hai. Việc sửa sinh `change_log` riêng, và ⚠️ **nén thoại vẫn phải chạy SAU layout** (`BR-003-12`) ⇒ sửa nội dung ở đây **không** thay thế cho [UC-05](./UC-05-Human-Gate-Dialogue-Condensation.md) |
| **ALT-4** | **Tác giả quay lại sửa panel script vì thoại không khớp panel** | Quay về [UC-03](./UC-03-Review-Panel-Script.md). Khi panel script đổi (nhân vật có mặt thay đổi), các dòng thoại thuộc panel đó **quay về trạng thái `chưa xác nhận`** — xem `EXC-4` |
| **ALT-5** | **Tác giả tạm dừng giữa chapter và quay lại sau** | Trạng thái xác nhận của từng dòng được lưu; tác giả tiếp tục từ dòng chưa xác nhận đầu tiên. Không có timeout nào tự động xác nhận phần còn lại |

## 5. Exception flow

| # | Nhánh ngoại lệ | Diễn biến & xử lý |
|---|---|---|
| **EXC-1** | **LLM không gán được người nói cho một dòng** (thoại xen tự sự, không có anchor trong văn bản) | Dòng đó hiển thị **không có đề xuất** và ở trạng thái `chưa xác nhận`. **Tác giả buộc phải gán tay** — không có đường bỏ trống. Đây là tình huống mà CF-6.10 gán tỉ lệ lỗi **30–50%** (3+ người có tự sự chen) ⚠️ `[EM]`, **ước lượng, không phải số đo** |
| **EXC-2** | **Dòng thoại là câu ngắn / thán từ** (*"Hả?"*, *"Ừ."*) | Hệ thống **đánh dấu là dòng rủi ro cao** và hiển thị ngữ cảnh trước/sau để tác giả quyết. Đây là tình huống CF-6.10 gán tỉ lệ lỗi **40–60%** ⚠️ `[EM]` — **ước lượng, KHÔNG phải số đo**; MVP2 **thiết kế như thể tỉ lệ lỗi ở cận trên** (`BRD-003` §3 `G-04`) |
| **EXC-3** | ⛔ **Tác giả (hoặc một API client) cố xuất bản page khi còn dòng `chưa xác nhận`** | Thao tác **bị TỪ CHỐI** ở tầng pipeline xuất bản, không phải bị cảnh báo ở tầng UI. Page giữ trạng thái `pending`. **Đây chính là phép đo của `M2-4`**: không tồn tại đường code nào xuất bản page mà chưa qua **cả hai** gate. Nếu tồn tại một đường như vậy, đó là **FAIL của exit criterion mốc MVP2**, không phải một bug UI |
| **EXC-4** | **Panel script bị sửa SAU khi thoại đã được xác nhận** (nhân vật bị xoá khỏi panel, panel bị gộp/tách) | Các dòng thoại của panel đó **quay về `chưa xác nhận`**, kèm `change_log` ghi lý do invalidate. Người nói đã được gán cho một nhân vật **không còn có mặt** trong panel là một xác nhận **không còn giá trị** — giữ nó lại là để một gate đã qua bảo lãnh cho một trang chưa được duyệt |
| **EXC-5** | **Tác giả huỷ giữa chừng và rời khỏi gate** | Page/chapter giữ trạng thái **`pending`** và **không xuất bản được**. Không có timeout, không có auto-approve, không có *"xác nhận phần còn lại theo đề xuất của LLM"*. ⛔ Một gate có nhánh tự thoát thì không phải gate (`Glossary` *Go/No-Go gate*: *"một gate không có nhánh FAIL thì không phải gate"*) |
| **EXC-6** | **Ghi `change_log` thất bại trong khi xác nhận đã được nhận** | Toàn bộ transaction **rollback** — xác nhận **không** được ghi, dòng thoại trở về `chưa xác nhận`. `KC-4`: *"bằng chứng có thể thiếu ngẫu nhiên thì không phải bằng chứng"*. Một xác nhận không có log là một gate **đã đi qua mà không để lại dấu vết pháp lý** — tệ hơn cả việc chưa đi qua, vì nó trông như đã xong |
| **EXC-7** | **Gate này hoàn tất nhưng gate `dialogue condensation` chưa** | Page **vẫn không xuất bản được**. `BR-003-13`: **hai gate chỉ *"xong"* cùng nhau**, vì `M2-4` là thuộc tính của **pipeline xuất bản**. Trạng thái đúng để hiển thị cho tác giả là *"gate 1/2 đã xong"*, **không** phải *"đã sẵn sàng xuất bản"* |

## 6. Tài liệu liên quan

### 6.1 Traceability

| Quan hệ | Tài liệu |
|---|---|
| Part of | [Epic-Comic-Director-And-Layout.md](../../022-User-Stories/Epics/Epic-Comic-Director-And-Layout.md) |
| BRD nguồn | [BRD-003 — Comic Director And Layout](../BRD/BRD-003-Comic-Director-And-Layout.md) — `BR-003-10`, `BR-003-12`, `BR-003-13`, `BR-003-14` |
| BRD ràng buộc pháp lý của `change_log` | [BRD-007 — Legal And Compliance](../BRD/BRD-007-Legal-And-Compliance.md) — `BR-007-01`, `BR-007-02` |
| Requirement cấp sản phẩm | [PRD-Comic-Studio.md](../PRD-Comic-Studio.md) · chi tiết kỹ thuật: [SRS-Comic-Studio.md](../SRS-Comic-Studio.md) |
| Use Case trước | [UC-03 — Review Panel Script](./UC-03-Review-Panel-Script.md) |
| **Gate bắt buộc thứ hai — cặp không tách rời** | [UC-05 — Human Gate Dialogue Condensation](./UC-05-Human-Gate-Dialogue-Condensation.md) |
| Use Case tiêu thụ output của hai gate | [UC-07 — Edit Bubble And Dialogue In Panel](./UC-07-Edit-Bubble-And-Dialogue-In-Panel.md) · [UC-08 — Arrange Page And Preview](./UC-08-Arrange-Page-And-Preview.md) |

### 6.2 Nguồn đã trích (Tài liệu tham khảo)

- [MVP-Scope.md](../../010-Planning/MVP-Scope.md) — §3 hàng `C7` (*"không phải tuỳ chọn, không dồn sang MVP4"*) và `C5` · §6 `KC-2`, `KC-3`, `KC-4` · §5.2 (ràng buộc xuyên suốt: *"mọi hành động của người dùng phải sinh một `change_log` row"*)
- [Roadmap.md](../../010-Planning/Roadmap.md) — §2 exit criterion **M2-4**: *"hai human gate (speaker attribution + dialogue condensation) **không bypass được**: không tồn tại đường code nào xuất bản page mà chưa qua cả hai"*
- [Risk-Register.md](../../010-Planning/Risk-Register.md) — `R-01` (xác nhận ở human gate là bằng chứng pháp lý, không backfill được) · `G-04` (khoảng trống **không gán Score**: tỉ lệ lỗi thật của speaker attribution)
- [Glossary.md](../../999-Resources/Glossary.md) — *speaker attribution* (lỗi **30–50%** / **40–60%** nếu không có anchor + constrained decoding; chi phí lỗi **bất đối xứng**), *HITL gate* (đơn vị đo là **giờ-người**), *dialogue condensation*, *Go/No-Go gate*
- [Documents-Template.md](../../../knowledge-base/99-Templates/Documents-Template.md) — RULE-001
- `docs/010-Planning/pm-runs/2026-08-24-khoi-tao-requirements-stories-comic-studio/findings/business-analyst.md` — §3.1 (*"mỗi human gate bắt buộc phải là một UC riêng… không tồn tại đường code bypass"*), §3.2 hàng **UC-04**, §4.10 (hai gate chỉ xong cùng nhau), §5.2 CF-6.10 ⚠️ `[EM]` + CF-8.8 + CF-7.2, §5.3 (CẤM-17), §6.2 `KT-1`

---

_Created by TNMCORE-OS — role `business-analyst`_
_Author: trisjr_
