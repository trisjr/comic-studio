---
id: UC-02
type: use-case
status: draft
project: comic-studio
created: 2026-08-24
---

# UC-02 — Duyệt và sửa Story Bible

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
| **Secondary actor** | **LLM** (extraction — chỉ **phát event**, không sở hữu state) · **Hệ thống** (`resolveState()`, `change_log`, `field_provenance`) · **Founder-operator** (chỉ ở nhánh MVP0 khi Story Bible được khai tay, và khi ghi lại số đo của `M1-3`) |
| **Mốc MVP** | **MVP1** — `MVP-Scope` §3 hàng `B2`, `B3` ✅ và `D1` `🟡` **thành phần #5 Story Bible editor** (`MVP-Scope` §5.2, **4–6%** effort `[EM]`, mẫu số SaaS) |
| **BRD module** | [BRD-002 — Story Intelligence](../BRD/BRD-002-Story-Intelligence.md) (`BR-002-02`…`BR-002-08`, `BR-002-11`) + [BRD-004 — Minimum Editor](../BRD/BRD-004-Minimum-Editor.md) (`BR-004-01`) |
| **Điều kiện tiên quyết (precondition)** | (1) [UC-01](./UC-01-Upload-And-Ingest-Chapter.md) đã hoàn tất cho ≥1 chapter: văn bản đã qua `text clean` và đã qua phép kiểm opt-out Điều 37b. (2) Khoá thời gian `timeline_id` + `story_order` đã chốt (`BR-002-07`). (3) `change_log` + `field_provenance` đã tồn tại và commit **cùng một transaction** với artifact — `KC-2`, `KC-3`, `KC-4`. (4) ⚠️ **`TBD` (KT-1)** — actor là **phân khúc** đã chốt (CF-1.5), **không phải một persona**: repo chưa có persona / JTBD / định nghĩa *"đủ tốt"*, nên *"Story Bible đúng"* với người dùng chưa có định nghĩa nghiệm thu; xem `findings/business-analyst.md` §6.2 `KT-1` |

## 2. Mục tiêu

Tác giả xác nhận hoặc sửa những gì hệ thống đã rút ra được từ chapter: **nhân vật, trang phục, địa điểm, và trạng thái theo event**. Giá trị trực tiếp là tác giả **không phải khai tay toàn bộ Story Bible** (`BR-002-02`) — hệ thống làm phần thô, con người sửa phần sai. Giá trị sâu hơn: mọi panel về sau đều đọc từ Story Bible, nên một sai sót được sửa **ở đây** rẻ hơn nhiều lần so với sửa nó sau khi đã sinh ảnh.

Đây cũng là **nơi moat lộ ra với khách hàng**. `Glossary` định nghĩa Story Bible là *"cơ sở dữ liệu trạng thái có cấu trúc… truy vấn được theo thời điểm"*, **phân biệt rõ với một bản tóm tắt văn xuôi**: Story Bible là **dữ liệu**, không phải prose. Nó là **tài sản tích luỹ theo thời gian của người dùng**, nên cũng là switching cost và là **ứng viên moat thật**. Mỗi lần tác giả sửa một field ở đây, tác phẩm của họ đắt hơn một chút và khó rời khỏi hệ thống hơn một chút — và đồng thời, `change_log` + `field_provenance` sinh ra ở mỗi lần sửa chính là **hồ sơ chứng minh quyền tác giả của khách**, không chỉ của Founder (`BR-002-11`).

## 3. Main flow

| # | Actor | Bước |
|---|---|---|
| 1 | **Hệ thống** | Sau khi chapter qua `text clean`, kích hoạt chặng extraction cho chapter đó |
| 2 | **LLM** | Rút ra **nhân vật, địa điểm, trang phục** từ văn bản chapter và **phát event** mức scene. ⚠️ LLM **chỉ phát event**; **code sở hữu state** (`BR-002-06`, `MVP-Scope` §3 `B3`) |
| 3 | **Hệ thống** | Ghi entity và event vào Story Bible, tách hai trục **Identity** (bất biến qua các chương) và **Appearance** (thay đổi theo trạng thái) — gộp hai thứ này vào một field là **nguyên nhân của phần lớn lỗi consistency** (`BR-002-05`) |
| 4 | **Hệ thống** | Đánh dấu provenance cho từng field: field nào do LLM rút ra, field nào do người khai — `field_provenance`, `KC-3` |
| 5 | **Tác giả** | Mở **Story Bible editor** — form + list, không canvas, không graph editor (`BR-004-01`, `MVP-Scope` §5.2 thành phần **#5**) |
| 6 | **Tác giả** | Duyệt danh sách **nhân vật**: xác nhận đúng, sửa tên/mô tả sai, **xoá entity giả** do rác văn bản sinh ra, thêm nhân vật bị bỏ sót |
| 7 | **Tác giả** | Duyệt **trang phục** và **địa điểm** theo cùng cách; với trang phục, khai nó thuộc trục **Appearance** và neo vào event nào |
| 8 | **Tác giả** | Duyệt **state theo event**: xác nhận rằng tại event N, nhân vật X đang ở trạng thái nào (trang phục, vết thương, tóc) |
| 9 | **Hệ thống** | Với **mỗi** hành động sửa ở bước 6–8, sinh **một `change_log` row** và cập nhật `field_provenance`, **commit cùng một transaction** với chính field được sửa (`BR-002-11`, `KC-2`, `KC-3`, `KC-4`) |
| 10 | **Hệ thống** | Tính lại trạng thái theo `state_at(N) = reduce(events)` qua **đúng MỘT** hàm `resolveState(entity, at_event)` của toàn hệ thống (`BR-002-06`) |
| 11 | **Tác giả** | Truy vấn thử: *"tại chương 40, nhân vật X mặc gì"* — và thấy đúng trang phục của chương 40, không phải của hiện tại |
| 12 | **Tác giả** | Đánh dấu Story Bible của chapter là đã duyệt. Chapter sẵn sàng cho [UC-03](./UC-03-Review-Panel-Script.md) |

> **Ngưỡng nghiệm thu của chặng extraction**: **≥80%** entity (nhân vật + địa điểm) khớp với Story Bible viết tay của **MVP0** — `Roadmap` §2 exit criterion **M1-3**. ⚠️ **`[EM]` — `Roadmap` §2 ghi nguyên văn *"ngưỡng do em định nghĩa"*; cấm trích như số đo hoặc benchmark ngành** (CF-10.5). Nghĩa nghiệp vụ của ngưỡng này: nó đo **công sức còn lại của con người** ở bước 6–8, không đo *"chất lượng AI"*.

## 4. Alternative flow

| # | Nhánh | Diễn biến |
|---|---|---|
| **ALT-1** | **MVP0 — Story Bible viết tay** | `MVP-Scope` §3 `B2`, `B3` = ❌ **viết tay** ở MVP0, và CF-8.4 ghi rõ MVP0 *"không code extraction"*. **Founder-operator** khai tay Story Bible của một chapter duy nhất. Chính bản viết tay này về sau là **mốc so** của **M1-3**. Dùng đúng tên **MVP0** — ⛔ **CẤM-11** |
| **ALT-2** | **Tác giả tự khai một entity trước khi extraction chạy** | Tác giả thêm nhân vật bằng tay ở bước 5. `field_provenance` ghi `human`; extraction về sau **không được ghi đè** field do người khai — trật tự này là điều làm cho ranh giới *"phần nào do người, phần nào do AI"* xác định được (`KC-3`) |
| **ALT-3** | **Chapter là hồi tưởng — state phải đọc theo nhánh thời gian khác** | Bước 10–11 chạy trên `timeline_id` của nhánh hồi tưởng. Đây là lý do khoá thời gian **không** dùng `(chapter, scene)`: nó là **thứ tự đọc**, không phải thứ tự sự việc xảy ra, nên **sai âm thầm ở mọi flashback** — không crash, chỉ corrupt dữ liệu (`BR-002-08`, `Glossary` *syuzhet vs fabula*) |
| **ALT-4** | **Tác giả chỉ tra Story Bible, không sửa gì** | Truy vấn đọc thực hiện bằng **SQL + full-text search trong Postgres** — *"Story Bible **là** index của mình"*; **không** có index vector nào trong MVP (`BR-002-09`). Không có hành động sửa ⇒ không sinh `change_log` |
| **ALT-5** | **Tác giả duyệt Story Bible xuyên nhiều chapter một lượt** | Bước 6–8 chạy trên tập entity hợp nhất của nhiều chapter cùng `timeline_id`. State vẫn được **tính**, không lưu sẵn, nên không có bước hợp nhất riêng nào cần thêm (`BR-002-06`) |

## 5. Exception flow

| # | Nhánh ngoại lệ | Diễn biến & xử lý |
|---|---|---|
| **EXC-1** | **Chặng extraction thất bại hoặc trả về rỗng** | Hệ thống báo lỗi cụ thể, giữ chapter ở trạng thái *đã ingest, chưa có bible*. Tác giả có hai đường: **retry** extraction, hoặc **khai tay** entity qua **ALT-2**. ⛔ Không tự tạo entity rác để *"có gì đó hiển thị"* — một entity giả tốn nhiều công sửa hơn một danh sách rỗng |
| **EXC-2** | **Extraction sinh entity giả từ rác văn bản** (ví dụ *"Chương 12"*, tên người dịch, tên nền tảng đọc truyện thành nhân vật) | Tác giả xoá ở bước 6; mỗi lần xoá sinh `change_log`. **Nguyên nhân gốc nằm ở [UC-01](./UC-01-Upload-And-Ingest-Chapter.md)**: `text clean` là bước ĐẦU TIÊN chính là để chặn trường hợp này (`BR-002-01`, CF-8.7). Nếu số entity giả lớn, đường xử lý đúng là quay lại UC-01 sửa văn bản gốc, **không** phải xoá tay từng dòng |
| **EXC-3** | **Extraction đạt dưới ngưỡng `M1-3` ≥80%** `[EM]` | Đây là **FAIL của exit criterion mốc MVP1**, không phải lỗi của một chapter. Tác giả vẫn dùng được sản phẩm (sửa tay nhiều hơn), nhưng **Founder-operator** phải ghi lại số đo. ⛔ **CẤM-16**: **không sửa ngưỡng sau khi nhìn thấy kết quả** — *"đó là cách một gate biến thành nghi lễ"* (`MVP-Scope` §7) |
| **EXC-4** | **Hai event mâu thuẫn về cùng một trạng thái tại cùng một thời điểm** (ví dụ hai event nói nhân vật X mặc hai bộ khác nhau tại cùng event) | `resolveState()` không được **đoán**. Hệ thống hiển thị xung đột cho tác giả và **buộc tác giả chọn**; lựa chọn đó sinh `change_log` — *"chọn A thay vì B"* chính là dạng bằng chứng mà `KC-2` yêu cầu. Không có tự động phân xử: state là thứ **code sở hữu**, và code không có căn cứ để phân xử ý định của tác giả |
| **EXC-5** | **Tác giả sửa `story_order` của một event đã có panel tham chiếu** | Hệ thống cảnh báo rằng thay đổi này làm `resolveState()` trả kết quả khác cho các panel đã sinh, và ghi `change_log`. ⚠️ `Risk-Register` `R-15`: khoá thời gian sai ⇒ **panel hồi tưởng render state của hiện tại**. Đây là lỗi **không crash, chỉ sai âm thầm** — nên cảnh báo phải hiện, không được ẩn |
| **EXC-6** | **Ghi `change_log` thất bại trong khi field đã được sửa** | Toàn bộ transaction **rollback** — field không được sửa. `KC-4`: ba mục provenance phải commit **cùng một transaction** với artifact chúng chứng minh, vì *"bằng chứng có thể thiếu ngẫu nhiên thì không phải bằng chứng"*. Chấp nhận sửa mà mất log là chấp nhận mất hồ sơ chứng minh quyền của **khách hàng**, không chỉ của Founder |
| **EXC-7** | **Tác giả yêu cầu xoá toàn bộ dữ liệu tác phẩm** | Đường hard-delete tenant/tác phẩm phải **tồn tại và đã được kiểm thử** (`BR-007-08`). Story Bible là nhóm bảng **nhiều nhất** của hệ thống, nên đây cũng là chỗ dễ sót dữ liệu nhất — kỷ luật `ON DELETE CASCADE` trên mọi FK. Cơ chế thuộc [BRD-007](../BRD/BRD-007-Legal-And-Compliance.md) |

## 6. Tài liệu liên quan

### 6.1 Traceability

| Quan hệ | Tài liệu |
|---|---|
| Part of | [Epic-Story-Intelligence.md](../../022-User-Stories/Epics/Epic-Story-Intelligence.md) · [Epic-Minimum-Editor.md](../../022-User-Stories/Epics/Epic-Minimum-Editor.md) |
| BRD nguồn | [BRD-002 — Story Intelligence](../BRD/BRD-002-Story-Intelligence.md) · [BRD-004 — Minimum Editor](../BRD/BRD-004-Minimum-Editor.md) |
| Ràng buộc pháp lý của `change_log` / `field_provenance` | [BRD-007 — Legal And Compliance](../BRD/BRD-007-Legal-And-Compliance.md) |
| Requirement cấp sản phẩm | [PRD-Comic-Studio.md](../PRD-Comic-Studio.md) · chi tiết kỹ thuật: [SRS-Comic-Studio.md](../SRS-Comic-Studio.md) |
| Use Case trước | [UC-01 — Upload And Ingest Chapter](./UC-01-Upload-And-Ingest-Chapter.md) |
| Use Case kế tiếp | [UC-03 — Review Panel Script](./UC-03-Review-Panel-Script.md) |

### 6.2 Nguồn đã trích (Tài liệu tham khảo)

- [MVP-Scope.md](../../010-Planning/MVP-Scope.md) — §3 hàng `B2`, `B3`, `B4`, `B5`, `D1` · §5.2 thành phần **#5** (**4–6%** `[EM]`) và ràng buộc xuyên suốt *"mọi hành động của người dùng phải sinh một `change_log` row"* · §6 `KC-2`, `KC-3`, `KC-4`, `KC-5` · §7 (nguyên tắc chung của gate)
- [Roadmap.md](../../010-Planning/Roadmap.md) — §2 exit criterion **M1-3** (**≥80%** ⚠️ `[EM]`, *"ngưỡng do em định nghĩa"*) · §2 **M1-5** · §6.2
- [Risk-Register.md](../../010-Planning/Risk-Register.md) — `R-15` (khoá thời gian sai ⇒ panel hồi tưởng render state của hiện tại)
- [Glossary.md](../../999-Resources/Glossary.md) — *Story Bible* (dữ liệu, không phải prose; tài sản tích luỹ; ứng viên moat thật), *Identity vs Appearance*, *syuzhet vs fabula*, *`timeline_id`*, *`field_provenance` / `change_log`*, *MVP0*
- [Documents-Template.md](../../../knowledge-base/99-Templates/Documents-Template.md) — RULE-001
- `docs/010-Planning/pm-runs/2026-08-24-khoi-tao-requirements-stories-comic-studio/findings/business-analyst.md` — §3.2 hàng **UC-02**, §5.2 (CF-1.5, CF-8.4, CF-8.7, CF-10.5), §5.3 (CẤM-11, CẤM-16, CẤM-17), §6.2 `KT-1`

---

_Created by TNMCORE-OS — role `business-analyst`_
_Author: trisjr_
