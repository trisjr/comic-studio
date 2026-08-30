---
id: UC-01
type: use-case
status: draft
project: comic-studio
created: 2026-08-24
---

# UC-01 — Upload và ingest một chapter

> [!IMPORTANT]
> **Quy ước nhãn nguồn số liệu** (kế thừa nguyên vẹn từ bảng Canonical Facts — **số và nhãn là một cặp không tách rời**):
> `[OFF]` official/paper gốc · `[BCN]` báo cáo ngành có tên firm · `[TC]` thứ cấp · `[EM]` ước lượng hoặc phép nhân, **không phải số đo** · `[CHỐT]` quyết định của Founder tại gate.
>
> ⚠️ **Bẫy đánh số (CF-10.2 · CẤM-14)**: `GP-1`…`GP-5` là ID **hàng compliance** của [MVP-Scope.md](../../010-Planning/MVP-Scope.md) §3 nhóm G; `G0`/`G1`/`G2` là ID **gate**. Tài liệu này viết `GP-2` cho hàng opt-out — **không** viết tắt thành `G2`.

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
| **Secondary actor** | **Hệ thống** (pipeline ingest deterministic) · **Founder-operator** (chỉ khi phải rà log opt-out bị chặn) |
| **Mốc MVP** | **MVP1** — `MVP-Scope` §3 hàng `B1` ✅ và `GP-2` ✅. Ở **MVP0** chặng này là **viết tay** (`B1` = ❌ viết tay, và MVP0 **không có database**) |
| **BRD module** | [BRD-002 — Story Intelligence](../BRD/BRD-002-Story-Intelligence.md) (`BR-002-01`) + [BRD-007 — Legal And Compliance](../BRD/BRD-007-Legal-And-Compliance.md) (`BR-007-03`, `BR-007-07`) |
| **Điều kiện tiên quyết (precondition)** | (1) Tenant đã tồn tại, `tenant_id` có mặt trên mọi bảng nghiệp vụ + RLS đã bật — `KC-5`, `Roadmap` §2 **M1-1**. (2) Khoá thời gian `timeline_id` + `story_order` đã được chốt ở **pre-cycle 09/2026** (`BR-002-07`, phụ thuộc **cứng** theo `Roadmap` §6.2). (3) Tác giả đã đọc ToS có **user warrant + indemnify** (`BR-007-07`). (4) ⚠️ **`TBD` (KT-1)** — actor ở đây là **phân khúc** đã chốt (CF-1.5), **không phải một persona**: toàn repo chưa có persona / JTBD / định nghĩa *"đủ tốt"*; xem `findings/business-analyst.md` §6.2 `KT-1` |

## 2. Mục tiêu

Tác giả có một chapter truyện chữ đang nằm ở đâu đó ngoài hệ thống — thường là văn bản **scrape** từ một nền tảng đọc truyện, lẫn header/footer, quảng cáo, ghi chú của người dịch và ký tự lỗi. Sau khi kết thúc use case này, tác giả **biết chắc hai điều**: chapter đã **sạch** để hệ thống hiểu được, và chapter **hợp pháp để xử lý** — không mang tín hiệu bảo lưu quyền của người khác.

Giá trị nằm ở chỗ hai câu trả lời đó đến **trước** khi bất kỳ chi phí nào phát sinh. Rác không bị loại thì Story Bible sinh ra **entity giả** — và tác giả sẽ tưởng nhân vật *"Chương 12"* là một nhân vật thật. Tín hiệu opt-out không được kiểm ngay tại đây thì nội dung đã bị xử lý **trước khi biết mình không được xử lý** — `Risk-Register` `R-06` gọi đó là *"một vi phạm đã xảy ra hàng nghìn lần, không sửa hồi tố được"*. Đây là lý do bước ingest là nơi **DUY NHẤT** đặt phép kiểm này: nó là nơi file của tác giả **lần đầu** đi vào hệ thống (`KC-6`, CF-7.5 `[OFF]` tóm tắt, chi phí **~0**).

## 3. Main flow

| # | Actor | Bước |
|---|---|---|
| 1 | **Tác giả** | Chọn tác phẩm (hoặc tạo tác phẩm mới) và mở màn hình upload chapter |
| 2 | **Tác giả** | Nạp file văn bản chapter và khai `timeline_id` + vị trí `story_order` của chapter trong tác phẩm (`BR-002-07`) |
| 3 | **Tác giả** | **Tick checkbox cam kết quyền** (*user warrant*) ngay tại bước upload — không phải chỉ ở trang ToS (`BR-007-07`) |
| 4 | **Hệ thống** | Nhận file và ghi nhận nó thuộc `tenant_id` hiện tại (`KC-5`) |
| 5 | **Hệ thống** | **Kiểm opt-out signal Điều 37b** trên file vừa nhận: đọc metadata / biện pháp bảo vệ công nghệ / thông tin quản lý quyền dạng máy đọc / thông báo công khai từ tổ chức quản lý tập thể — **bốn kênh bảo lưu quyền** theo NĐ 134/2026 Điều 37b (`BR-007-03`) |
| 6 | **Hệ thống** | **Log kết quả kiểm kèm timestamp** — kể cả khi kết quả là *"không có signal"*. `Roadmap` §2 **M1-4** đo bằng **100%** file upload đi qua bước kiểm này (`BR-007-03`) |
| 7 | **Hệ thống** | Chạy **`text clean`** — **bước ĐẦU TIÊN của chặng xử lý nội dung**, trước khi extraction chạy: loại header/footer, quảng cáo, ghi chú dịch, ký tự lỗi. Bước này **deterministic** (regex/heuristic), **không phải LLM** (`BR-002-01`, CF-8.7, `Roadmap` §2 **M1-2**) |
| 8 | **Hệ thống** | Tách chapter thành `Event` mức scene theo khoá thời gian đã khai ở bước 2 — đây là nơi state sẽ được neo vào (`BR-002-06`) |
| 9 | **Hệ thống** | Báo cho tác giả: chapter đã ingest xong, kèm **tóm tắt những gì đã bị `text clean` loại bỏ** và **kết quả phép kiểm opt-out** |
| 10 | **Tác giả** | Đối chiếu tóm tắt ở bước 9. Nếu chấp nhận, chapter chuyển sang trạng thái sẵn sàng cho [UC-02](./UC-02-Review-And-Edit-Story-Bible.md) |

> **Ranh giới thứ tự — hai câu dễ đọc thành mâu thuẫn, thực ra không.** *"`text clean` là bước ĐẦU TIÊN"* (CF-8.7) nói về **chặng xử lý nội dung**: không có bước LLM nào được chạy trước nó. *"Kiểm opt-out ngay tại ingest"* (`KC-6`) nói về **thời điểm nhận file**: phép kiểm đọc **metadata và nhãn quyền**, không xử lý nội dung. Vì vậy bước 5–6 đứng trước bước 7 mà **không** vi phạm CF-8.7 — và đặt bước 5 sau bước 7 thì đã **biến đổi** nội dung trước khi biết mình có quyền, đúng cái mà `KC-6` cấm.

## 4. Alternative flow

| # | Nhánh | Diễn biến |
|---|---|---|
| **ALT-1** | **MVP0 — làm tay, không có hệ thống** | `MVP-Scope` §3 `B1` = ❌ **viết tay** ở MVP0, và MVP0 **không có database** (§3.1). Ở mốc này **Founder-operator** tự làm sạch một chapter duy nhất bằng tay và ghi kết quả ra file phẳng. Dùng đúng tên **MVP0** — ⛔ **CẤM-11** cấm gọi *"phase 0"*, *"spike"*, *"PoC"* |
| **ALT-2** | **Tác giả tự dán văn bản thay vì nạp file** | Bước 2 nhận nội dung dán trực tiếp. Bước 5 vẫn chạy: khi không có metadata file, phép kiểm dựa trên **thông báo công khai từ tổ chức quản lý tập thể** và nội dung nhãn quyền nhúng trong văn bản; **kết quả vẫn được log kèm timestamp** — `Roadmap` §2 **M1-4** đo **100%** file upload, không có ngoại lệ theo kênh nạp |
| **ALT-3** | **Tác giả từ chối kết quả `text clean` ở bước 10** | Tác giả sửa lại văn bản gốc và nạp lại từ bước 2. Toàn bộ flow chạy lại — **kể cả bước 5–6**, vì đây là một file mới đi vào hệ thống |
| **ALT-4** | **Chapter là hồi tưởng (flashback) thuộc một nhánh thời gian khác** | Ở bước 2 tác giả khai `timeline_id` của nhánh đó, không phải nhánh chính. Đây chính là trường hợp mà `(chapter, scene)` **sai âm thầm** — nó là **thứ tự đọc**, không phải thứ tự sự việc xảy ra (`BR-002-08`, `Glossary` *syuzhet vs fabula*) |

## 5. Exception flow

| # | Nhánh ngoại lệ | Diễn biến & xử lý |
|---|---|---|
| **EXC-1** | ⛔ **Phát hiện opt-out signal Điều 37b** | Bước 5 tìm thấy tín hiệu bảo lưu quyền ở **một trong bốn kênh**. **Hệ thống CHẶN** — chapter **không** đi tiếp sang `text clean`. Kết quả kiểm + kênh phát hiện + timestamp được **log** (`BR-007-03`). Tác giả nhận thông báo nêu rõ nội dung này có bảo lưu quyền và hệ thống không xử lý. **Founder-operator** rà log định kỳ theo `Risk-Register` `R-06`. ⛔ **Không có đường cấu hình nào cho phép bỏ qua phép kiểm này** — `KC-6` nằm trong danh sách *"không được cắt"*, và `Roadmap` §2 **M1-4** đo bằng **100%** file đi qua bước kiểm |
| **EXC-2** | **Tác giả không tick checkbox cam kết quyền** | Bước 3 không hoàn tất ⇒ **upload không được nhận**. Checkbox là điều kiện của `BR-007-07` (*user warrant + indemnify*) và phải gắn vào **bước upload**, không chỉ ở trang ToS. Không có nó thì phòng tuyến hợp đồng của nền tảng khuyết đúng chỗ mọi đối thủ đều có |
| **EXC-3** | **File không đọc được / sai định dạng / rỗng sau `text clean`** | Bước 7 trả về nội dung rỗng hoặc lỗi giải mã. Hệ thống **từ chối** chapter, giữ nguyên trạng thái tác phẩm và báo lý do cụ thể cho tác giả. **Không** tạo `Event` mồ côi — nếu không, `story_order` có lỗ và mọi phép `reduce(events)` về sau đọc trên dữ liệu khuyết |
| **EXC-4** | **`text clean` loại quá tay, xoá cả nội dung truyện** | Tác giả phát hiện ở bước 10 khi đọc tóm tắt *"những gì đã bị loại"*. Tác giả từ chối và đi theo **ALT-3**. Đây là lý do bước 9 **bắt buộc** hiển thị phần bị loại: `text clean` là deterministic nên nó sai **một cách nhất quán**, và cách duy nhất phát hiện là cho người xem |
| **EXC-5** | **Tác giả nạp lại đúng chapter đã ingest trước đó** | Hệ thống báo trùng theo `timeline_id` + `story_order` và yêu cầu tác giả chọn: **thay thế** (chapter cũ bị đánh dấu superseded, mọi hành động sinh `change_log` — `KC-2`) hoặc **huỷ**. ⛔ Không âm thầm ghi đè: dữ liệu bị ghi đè âm thầm làm hồ sơ provenance mất một mắt (`KC-2`, `BR-007-01`) |
| **EXC-6** | **Rò rỉ chéo tenant khi ingest** | Nếu chapter được ghi thiếu `tenant_id` hoặc RLS chưa bật trên bảng liên quan, đây **không** phải lỗi của luồng này mà là vi phạm `KC-5` ⇒ chặn ở tầng schema. Nghiệm thu ở `Roadmap` §2 **M1-1** (*test rò rỉ chéo tenant PASS*). Cơ chế thuộc [BRD-005](../BRD/BRD-005-Multi-Tenancy-And-Platform.md) |

## 6. Tài liệu liên quan

### 6.1 Traceability

| Quan hệ | Tài liệu |
|---|---|
| Part of | [Epic-Story-Intelligence.md](../../022-User-Stories/Epics/Epic-Story-Intelligence.md) · [Epic-Legal-And-Compliance.md](../../022-User-Stories/Epics/Epic-Legal-And-Compliance.md) |
| BRD nguồn | [BRD-002 — Story Intelligence](../BRD/BRD-002-Story-Intelligence.md) · [BRD-007 — Legal And Compliance](../BRD/BRD-007-Legal-And-Compliance.md) |
| Ràng buộc multi-tenancy | [BRD-005 — Multi-Tenancy And Platform](../BRD/BRD-005-Multi-Tenancy-And-Platform.md) |
| Requirement cấp sản phẩm | [PRD-Comic-Studio.md](../PRD-Comic-Studio.md) · chi tiết kỹ thuật: [SRS-Comic-Studio.md](../SRS-Comic-Studio.md) |
| Use Case kế tiếp | [UC-02 — Review And Edit Story Bible](./UC-02-Review-And-Edit-Story-Bible.md) |
| Use Case cùng nhóm nghĩa vụ pháp lý | [UC-11 — Handle Takedown Request](./UC-11-Handle-Takedown-Request.md) |

### 6.2 Nguồn đã trích (Tài liệu tham khảo)

- [MVP-Scope.md](../../010-Planning/MVP-Scope.md) — §3 hàng `B1`, `B4`, `GP-2`, `GP-5` · §3.1 (MVP0 không có database) · §6 `KC-2`, `KC-5`, `KC-6`
- [Roadmap.md](../../010-Planning/Roadmap.md) — §2 exit criteria **M1-1**, **M1-2**, **M1-4** · §6.2 (phụ thuộc **cứng** của khoá thời gian)
- [Risk-Register.md](../../010-Planning/Risk-Register.md) — `R-06` (opt-out không kiểm tại ingest)
- [Glossary.md](../../999-Resources/Glossary.md) — *Story Bible*, *syuzhet vs fabula*, *`timeline_id`*, *`tenant_id`*, *RLS*, *MVP0*, *`field_provenance` / `change_log`*
- [Documents-Template.md](../../../knowledge-base/99-Templates/Documents-Template.md) — RULE-001 (naming, frontmatter, standard markdown link)
- `docs/010-Planning/pm-runs/2026-08-24-khoi-tao-requirements-stories-comic-studio/findings/business-analyst.md` — §3.1 (nguyên tắc cắt UC), §3.2 hàng **UC-01**, §5.2 (canonical facts CF-1.5, CF-7.5, CF-8.7, CF-10.2), §5.3 (CẤM-11, CẤM-14, CẤM-17), §6.2 `KT-1`

---

_Created by Comic Studio — role `business-analyst`_
_Author: trisjr_
