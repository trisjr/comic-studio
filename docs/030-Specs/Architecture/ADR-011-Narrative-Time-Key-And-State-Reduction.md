---
id: ADR-011
type: adr
status: draft
project: comic-studio
created: 2026-08-29
---

# ADR-011: Khoá thời gian tự sự và mô hình rút gọn trạng thái

Related to: [SDD-Comic-Studio](./SDD-Comic-Studio.md)

## Context

> [!IMPORTANT]
> ⛔ **Đây là ADR `record-only`.** Mọi quyết định ở mục `Decision` **đã CHỐT ở Phase 1**. ADR này **đóng băng** chúng, ⛔ không quyết thêm.
>
> ⭐ **Đây là NỀN của DB schema `story`.** Các file `docs/030-Specs/Schema/DB-Entity-*.md` sắp viết sẽ **trỏ về tài liệu này** để lấy ngữ nghĩa của `event`, `timeline_id`, `story_order`, `reading_order` và ranh giới `resolveState()`. Vì vậy mục `Decision` được đánh số `D1`…`D12` để trích dẫn được ở mức từng điều.

### Vấn đề gốc: `(chapter, scene)` **sai âm thầm**

`(chapter, scene)` là **thứ tự người đọc gặp sự kiện** (**syuzhet**), không phải **thứ tự sự việc thực sự xảy ra** (**fabula**). Dùng nó làm khoá thời gian thì:

> *"`(chapter, scene)` là **thứ tự đọc**, không phải **thứ tự sự việc xảy ra** ⇒ nó **sai âm thầm ở mọi flashback**, không crash, chỉ corrupt dữ liệu. Panel hồi tưởng sẽ render trang phục/vết thương của hiện tại."*
> — `BR-002-08`, [BRD-002](../../020-Requirements/BRD/BRD-002-Story-Intelligence.md)

Đây là loại lỗi **tệ nhất** để phát hiện muộn: không có exception, không có alert, chỉ có dữ liệu sai. Vì vậy [MVP-Scope §3 `B4`](../../010-Planning/MVP-Scope.md) ghi *"**phải sửa trước dòng code đầu tiên**"* và [Roadmap §6.2](../../010-Planning/Roadmap.md) xếp nó là **phụ thuộc CỨNG** của mọi bảng timeline ở MVP1 ([Story-Fix-Narrative-Time-Key](../../022-User-Stories/Backlog/Story-Fix-Narrative-Time-Key.md) §3 Bối cảnh & nguồn).

### Ranh giới quyền lực: LLM phát event, **code sở hữu state**

⭐ Nguyên tắc chi phối cả module `story` (`SRS-FR-05` · `BR-002-06`, [BRD-002](../../020-Requirements/BRD/BRD-002-Story-Intelligence.md)):

> *"Trạng thái của một entity tại một thời điểm được **tính**, không được lưu sẵn: `state_at(N) = reduce(events)`. **Code sở hữu state, LLM chỉ phát event.**"*

Ranh giới này **đang được một lint rule ở CI bảo vệ**: `comic` gọi `story` **DUY NHẤT** qua `resolveState()` và `getBible()` (`SRS-NFR-04` — xem `D3` của [ADR-009](./ADR-009-Modular-Monolith-Three-Schemas.md)). Tức đây không phải một lời khuyên thiết kế, nó là một ràng buộc **có cơ chế cưỡng chế đang chạy**.

### Ràng buộc phạm vi của tài liệu này

| Thuộc ADR-011 | ⛔ KHÔNG thuộc ADR-011 |
|---|---|
| Khoá thời gian, mô hình event, phép `reduce`, seam đọc state, trục Identity/Appearance | **DDL đầy đủ** — *"sẽ được đặc tả tại tầng 030-Specs"* ([SRS §3.B](../../020-Requirements/SRS-Comic-Studio.md)) ⇒ lô `DB-Entity-*` |
| Việc `resolveState()`/`getBible()` **là seam duy nhất** | Cơ chế **cưỡng chế** seam (lint rule) ⇒ [ADR-009](./ADR-009-Modular-Monolith-Three-Schemas.md) |
| Ràng buộc *"LLM chỉ phát event"* | **Chọn provider LLM** + prompt/cache policy ⇒ [ADR-008](./ADR-008-LLM-Provider-And-Usage-Boundaries.md) |
| — | **Chapter parse + text clean** (`SRS-FR-06`) — nằm cùng mục SRS nhưng ⛔ **không** thuộc lô ghi chép này |

## Decision

### D1. **HAI trục thời gian tách bạch** trên event

| Trục | Nghĩa | Dùng để |
|---|---|---|
| `reading_order` | **syuzhet** — thứ tự người đọc gặp sự kiện | Trình bày, điều hướng theo mạch đọc |
| `story_order` | **fabula** — thứ tự sự việc thực sự xảy ra | ⭐ **Trục dùng cho MỌI as-of state query** |

⛔ **Không** được gộp hai trục. ⛔ **Không** bảng nào trong schema `story` được dùng `(chapter, scene)` làm khoá thời gian ([Story-Fix](../../022-User-Stories/Backlog/Story-Fix-Narrative-Time-Key.md) §4 AC *"Xác minh được"*).

### D2. `story_order` kiểu **`NUMERIC` sparse**, bước nhảy **1000**, **editable qua UI**

- Kiểu `NUMERIC`, cấp phát **thưa** với bước **1000** (`SRS-FR-04` · `BR-002-07`, [BRD-002](../../020-Requirements/BRD/BRD-002-Story-Intelligence.md)).
- **Người biên tập sửa được** thứ tự qua UI.
- `[Kiến trúc suy luận]` — bước thưa cho phép chèn một event vào giữa hai event có sẵn **mà không phải đánh số lại** chuỗi phía sau; đây là điều kiện để *"editable"* không biến thành một thao tác ghi hàng loạt.

### D3. `timeline_id` mang `kind` + `anchor_order`

- `kind` là **ENUM**: `main` / `flashback` / `parallel` / `dream` (`SRS-FR-04`).
- `anchor_order` neo nhánh vào trục chính.
- ⇒ Nhiều dòng thời gian song song cùng tồn tại mà không lẫn nhau.

### D4. State neo vào **`Event` mức SCENE**, ⛔ không phải mức chapter

Cho phép chia nhỏ hơn bằng **`beat_no`** (`SRS-FR-04` · `BR-002-07`, [BRD-002](../../020-Requirements/BRD/BRD-002-Story-Intelligence.md)).

### D5. Ràng buộc toàn vẹn ở tầng DB cho khoá thời gian

Insert một event **thiếu `story_order`** phải bị **từ chối** — ⛔ hệ thống **không được tự suy ra** giá trị mặc định từ `(chapter, scene)` ([Story-Fix](../../022-User-Stories/Backlog/Story-Fix-Narrative-Time-Key.md) §4 AC *"Đường không hạnh phúc"*).

### D6. `state_at(N) = reduce(events where story_order <= N)` — **hàm thuần**

Trạng thái được **tính**, ⛔ **không được lưu sẵn** (`SRS-FR-05` · `BR-002-06`, [BRD-002](../../020-Requirements/BRD/BRD-002-Story-Intelligence.md)).

Tính chất bắt buộc: **tất định** — gọi lại hai lần với cùng `N` cho hai output **giống hệt nhau** ([Story-Timeline-State-Resolver](../../022-User-Stories/Backlog/Story-Timeline-State-Resolver.md) §4 AC *"Xác minh được"*).

### D7. LLM **CHỈ phát event**; ⛔ không có đường ghi state

- Payload event do LLM phát, cho **MỘT** chapter: `entity`, `attribute`, `value`, `permanence`, `evidence_span`, `confidence` (`SRS-FR-05`).
- ⛔ **Không có đường code nào** cho phép LLM ghi trực tiếp vào bảng state — **chỉ `reduce(events)` mới sinh ra giá trị state**. Xác minh bằng rà soát quyền ghi ở tầng schema/service ([Story-Timeline-State-Resolver](../../022-User-Stories/Backlog/Story-Timeline-State-Resolver.md) §4 AC *"Xác minh được"*).

### D8. ⭐ **ĐÚNG MỘT** hàm `resolveState(entity, at_event)` trong toàn hệ thống

- Mọi truy vấn state đi qua nó (`SRS-NFR-10` · `BR-002-06`, [BRD-002](../../020-Requirements/BRD/BRD-002-Story-Intelligence.md)).
- Cùng với `getBible()`, đây là **API DUY NHẤT** để module `comic` đọc state của module `story` ([Story-Timeline-State-Resolver](../../022-User-Stories/Backlog/Story-Timeline-State-Resolver.md) §4 AC *"Xác minh được"*).
- **Hai guardrail KHÁC NHAU, ⛔ đừng gộp:**

| Guardrail | Bảo vệ điều gì | Mã | Cơ chế |
|---|---|:--:|---|
| **Lint rule ở CI** | Seam `comic` → `story` chỉ đi qua `resolveState()`/`getBible()` | `D-04` · `SRS-NFR-04` | CI **FAIL** khi có import vi phạm |
| **Test guardrail** | ⛔ **Không được có `ORDER BY chapter_no`** trong **bất kỳ** đường resolve state nào | `D-17` · `SRS-NFR-10` | Test tự động |

Trigger rủi ro đã đăng ký: `R-15` ([Risk-Register §2.1](../../010-Planning/Risk-Register.md)) cột *trigger* — *"hoặc có nhiều hơn một hàm truy vấn state trong codebase"*.

### D9. `reduce` **cô lập theo `timeline_id`**

Hai event có **cùng `story_order`** nhưng **khác `timeline_id`** (ví dụ giấc mơ chạy song song mạch chính) là **hai chuỗi độc lập** — `state_at` ⛔ **không được gộp** chúng vào cùng một chuỗi reduce ([Story-Timeline-State-Resolver](../../022-User-Stories/Backlog/Story-Timeline-State-Resolver.md) §4 AC *"Đường không hạnh phúc"* · [Story-Fix](../../022-User-Stories/Backlog/Story-Fix-Narrative-Time-Key.md) §4 AC *"Xác minh được"*).

### D10. *"Chưa có state"* là một câu trả lời **tường minh**

Gọi `state_at(N)` với `N` nhỏ hơn `story_order` của event đầu tiên của entity ⇒ trả về *"chưa có state"* **phân biệt được** với *"có state nhưng rỗng"*. ⛔ Không trả record rỗng hay giá trị mặc định gây hiểu nhầm ([Story-Timeline-State-Resolver](../../022-User-Stories/Backlog/Story-Timeline-State-Resolver.md) §4 AC *"Đường không hạnh phúc"*).

### D11. ⛔ **Không cache lệch nguồn**

Sửa hoặc xoá một event ⇒ lần gọi `state_at` **tiếp theo** phải phản ánh thay đổi, ⛔ không dùng lại giá trị đã tính trước đó. Sửa `story_order` của một event cũng vậy ([Story-Timeline-State-Resolver](../../022-User-Stories/Backlog/Story-Timeline-State-Resolver.md) §4 AC *"Đường không hạnh phúc"* · [Story-Fix](../../022-User-Stories/Backlog/Story-Fix-Narrative-Time-Key.md) §4 AC *"Đường không hạnh phúc"*).

### D12. Story Bible tách **HAI TRỤC**: Identity và Appearance

| Trục | Nghĩa | Ví dụ trong nguồn |
|---|---|---|
| **Identity** | **Bất biến** qua các chương | Cấu trúc khuôn mặt, dấu hiệu nhận dạng |
| **Appearance** | **Thay đổi theo trạng thái** | Trang phục, vết thương, tóc |

⛔ **Gộp hai thứ vào một field là lỗi thiết kế** — nguồn ghi thẳng nó là *"**nguyên nhân của phần lớn lỗi consistency**"* (`BR-002-05`, [BRD-002](../../020-Requirements/BRD/BRD-002-Story-Intelligence.md) · [UC-02](../../020-Requirements/Use-Cases/UC-02-Review-And-Edit-Story-Bible.md) bước 3).

⇒ Hệ quả cho schema: thuộc tính **Appearance phải khai nó neo vào event nào**; Identity thì không ([UC-02](../../020-Requirements/Use-Cases/UC-02-Review-And-Edit-Story-Bible.md) bước 7).

### D13. Hợp đồng với lô `DB-Entity-*` — cái gì được quyết ở đâu

| Lô `DB-Entity-*` **PHẢI tuân theo** | Lô `DB-Entity-*` **được quyền đặc tả** |
|---|---|
| `D1`–`D5` (khoá thời gian) · `D6`–`D11` (mô hình reduce) · `D12` (hai trục) | Tên bảng, kiểu cột chi tiết, PK/FK/index cụ thể, ràng buộc `CHECK`, migration |
| `tenant_id` là cột đầu mọi composite index ([ADR-010](./ADR-010-Tenant-Isolation-With-RLS.md)) | Giá trị cụ thể của `permanence`, ngữ nghĩa chi tiết `beat_no` — xem mục `TBD` |

## Alternatives considered

> ⭐ Phần giá trị nhất của ADR record-only. Lý do bác trích từ nguồn Phase 1; chỗ nào là suy luận, em dán nhãn `[Kiến trúc suy luận]`.

### (a) Giữ `(chapter, scene)` làm khoá thời gian — ⛔ BỊ LOẠI

| # | Lý do bác | Nguồn |
|:--:|---|---|
| **1** ⭐ | `(chapter, scene)` là **thứ tự đọc**, không phải **thứ tự sự việc xảy ra** ⇒ **sai âm thầm ở MỌI flashback**: ⛔ không crash, chỉ **corrupt dữ liệu** | `BR-002-08` ([BRD-002](../../020-Requirements/BRD/BRD-002-Story-Intelligence.md)) · [SRS §3.B](../../020-Requirements/SRS-Comic-Studio.md) |
| **2** | Hậu quả cụ thể, nhìn thấy được ở output: *"Panel hồi tưởng sẽ render **trang phục/vết thương của hiện tại**"* | `BR-002-08` ([BRD-002](../../020-Requirements/BRD/BRD-002-Story-Intelligence.md)) |
| **3** | Sửa **sau** khi có dữ liệu là một cuộc migration xuyên module ⇒ `B4` yêu cầu *"phải sửa **trước dòng code đầu tiên**"*; `Roadmap` xếp **pre-cycle 09/2026**, exit criterion `P-4` | [MVP-Scope](../../010-Planning/MVP-Scope.md) §3 `B4` · [Story-Fix](../../022-User-Stories/Backlog/Story-Fix-Narrative-Time-Key.md) §3 Bối cảnh & nguồn |

### (b) **Một trục thời gian duy nhất** (bỏ `reading_order` hoặc bỏ `story_order`) — ⛔ BỊ LOẠI

`SRS-FR-04` và `BR-002-07` ([BRD-002](../../020-Requirements/BRD/BRD-002-Story-Intelligence.md)) đều phát biểu ở dạng **hai trục tách bạch**. `[Kiến trúc suy luận]` — bỏ `story_order` là quay lại đúng (a); bỏ `reading_order` thì mất khả năng trình bày theo mạch đọc, tức mất chính thứ tự mà tác phẩm được xuất bản. Hai trục phục vụ hai câu hỏi khác nhau và **không suy ra được nhau** khi có flashback.

### (c) **Lưu sẵn (materialize) state** trong một bảng thay vì tính — ⛔ BỊ LOẠI

`BR-002-06` ([BRD-002](../../020-Requirements/BRD/BRD-002-Story-Intelligence.md)) loại tường minh: trạng thái *"được **tính**, **không được lưu sẵn**"*. `[Kiến trúc suy luận]` — nguồn không ghi lý do nguyên văn, nhưng ràng buộc `D11` trong chính hồ sơ làm phương án này không tương thích: event **sửa được** và `story_order` **editable qua UI** ⇒ mọi giá trị lưu sẵn có thể lệch nguồn ngay sau một thao tác biên tập, và không có cơ chế nào trong hồ sơ đảm bảo phát hiện được sự lệch đó.

### (d) **LLM ghi thẳng state** (thay vì chỉ phát event) — ⛔ BỊ LOẠI

`SRS-FR-05`: *"**code sở hữu state**, LLM chỉ phát event"*. Điều kiện xác minh đã ghi thành AC kiểm chứng được: ⛔ không endpoint/service nào ghi bảng state từ output LLM mà không qua `reduce` ([Story-Timeline-State-Resolver](../../022-User-Stories/Backlog/Story-Timeline-State-Resolver.md) §4 AC *"Xác minh được"*).

`[Kiến trúc suy luận]` — điều phương án này đánh mất là **khả năng sửa**: một event sai có `evidence_span` và `confidence` để người truy ngược và sửa; một giá trị state do LLM ghi thẳng thì không có nguồn để đối chiếu.

### (e) **Nhiều hàm truy vấn state** rải trong codebase — ⛔ BỊ LOẠI

`SRS-NFR-10` đòi **đúng MỘT** `resolveState(entity, at_event)`. Đây là mitigation đã đăng ký của `R-15`, và *"có nhiều hơn một hàm truy vấn state trong codebase"* là **trigger** của chính rủi ro đó ([Risk-Register §2.1](../../010-Planning/Risk-Register.md) · [BRD-002](../../020-Requirements/BRD/BRD-002-Story-Intelligence.md)).

`[Kiến trúc suy luận]` — với nhiều đường resolve, test guardrail *"không `ORDER BY chapter_no`"* mất ý nghĩa: nó chỉ chứng minh được điều gì khi tập đường cần kiểm là **một**.

### (f) Module `comic` **đọc thẳng bảng** của schema `story` — ⛔ BỊ LOẠI

`SRS-NFR-04` · `BR-005-06` ([BRD-005](../../020-Requirements/BRD/BRD-005-Multi-Tenancy-And-Platform.md)): ranh giới cưỡng chế bằng **lint rule, không bằng thoả thuận**. Xác minh: ⛔ không query nào từ `comic` trỏ trực tiếp vào bảng schema `story` ngoài hai hàm seam ([Story-Timeline-State-Resolver](../../022-User-Stories/Backlog/Story-Timeline-State-Resolver.md) §4 AC *"Xác minh được"*). Lập luận đầy đủ ở `(e)` của [ADR-009](./ADR-009-Modular-Monolith-Three-Schemas.md).

### (g) **Gộp Identity và Appearance** vào một field — ⛔ BỊ LOẠI

`BR-002-05` ([BRD-002](../../020-Requirements/BRD/BRD-002-Story-Intelligence.md)) gọi thẳng đây là *"**nguyên nhân của phần lớn lỗi consistency**"*. Cùng phát biểu ở [UC-02](../../020-Requirements/Use-Cases/UC-02-Review-And-Edit-Story-Bible.md) bước 3. Đây là một trong số ít quyết định mà nguồn ghi cả **triệu chứng** lẫn **nguyên nhân**, nên ⛔ không cần và không được diễn giải lại.

### (h) Dùng **`pgvector`** để tăng tốc truy vấn state — ⛔ KHÔNG dùng ở MVP, ⚠️ **không bị cấm vĩnh viễn**

[Story-Timeline-State-Resolver](../../022-User-Stories/Backlog/Story-Timeline-State-Resolver.md) §4 *"Story này KHÔNG làm"* ghi rõ cả hai vế: không dùng ở mốc này, **nhưng không bị cấm vĩnh viễn** (Full Scope `🟡` *"khi có bằng chứng SQL+FTS không đủ"*). ⇒ Xem khối `[!CAUTION]` của [ADR-009](./ADR-009-Modular-Monolith-Three-Schemas.md). ⛔ **Đừng đọc mục này thành một lệnh cấm.**

### (i) ⚠️ Hai phương án **KHÔNG có trong hồ sơ**

⛔ Không hàng nguồn Phase 1 nào ghi lại việc cân nhắc rồi bác: (1) một sơ đồ đánh số **dày** (integer liên tiếp) thay cho `NUMERIC` sparse; (2) neo state ở **mức chapter** như một lựa chọn có cân nhắc. Nguồn chốt thẳng `NUMERIC` sparse bước 1000 và mức scene. Em **không** dựng lại câu chuyện bác bỏ không tồn tại — ai muốn đổi phải mở nó như một quyết định mới, có ADR mới.

## Consequences

### Tích cực

- ⭐ **Flashback đúng theo cấu trúc**, không theo kỷ luật: mọi as-of query đi qua `story_order` nên không tồn tại đường code nào trả kết quả theo thứ tự đọc.
- Điều kiện xác minh là một **test có flashback cụ thể**, ⛔ không chấp nhận thay bằng test trên chuỗi chương tuyến tính ([Story-Timeline-State-Resolver](../../022-User-Stories/Backlog/Story-Timeline-State-Resolver.md) §4 AC *"Xác minh được"*).
- **Một đường resolve duy nhất** ⇒ guardrail có chỗ để gắn, và lỗi state có **một** nơi để sửa.
- **Sai sót của LLM bị giới hạn ở tầng đề xuất event** — mỗi event mang `evidence_span` + `confidence` để người truy ngược; state luôn là hệ quả tính được của tập event đã duyệt.
- 13 file `DB-Entity-*` sắp viết có **một mỏ neo duy nhất** cho ngữ nghĩa thời gian ⇒ ⛔ không phát sinh 13 cách hiểu.

### Tiêu cực — chi phí thật

- **Mỗi lần đọc state là một phép `reduce`.** Chi phí tăng theo số event; hồ sơ đã lường trước điều này bằng một AC riêng cho *"chuỗi event dài (40+ event ảnh hưởng cùng một nhân vật)"* ([Story-Timeline-State-Resolver](../../022-User-Stories/Backlog/Story-Timeline-State-Resolver.md) §4 AC *"Đường không hạnh phúc"*).
- ⭐ **Tối ưu hiển nhiên nhất bị rào lại.** `D6` cấm lưu sẵn và `D11` cấm cache lệch nguồn ⇒ mọi lớp cache về sau **phải** mang theo cơ chế vô hiệu hoá khi event đổi. Đây là chi phí thiết kế thường trực, không phải một lần.
- **Chất lượng dữ liệu phụ thuộc người.** `story_order` **editable qua UI** ⇒ một thao tác biên tập sai làm sai state của toàn bộ đoạn phía sau, và ⛔ không có cơ chế nào trong hồ sơ tự phát hiện điều đó.
- **Migration dữ liệu MVP0 có phần thủ công**: bản ghi viết tay không gán được `story_order` hợp lệ phải bị đánh dấu *"cần xác nhận thủ công"*, ⛔ không được âm thầm bỏ qua hay gán sai ([Story-Fix](../../022-User-Stories/Backlog/Story-Fix-Narrative-Time-Key.md) §4 AC *"Đường không hạnh phúc"*).
- **Hai trục = hai thứ phải giữ đồng bộ về mặt nghiệp vụ.** Mô hình đúng hơn nhưng cũng khó giải thích hơn cho người dùng cuối so với *"chương mấy, cảnh mấy"*.

### Việc còn để `TBD` — ⛔ không được bịa

| Khoảng trống | Ai đóng | Khi nào |
|---|---|---|
| **DDL đầy đủ** của `event` / `timeline` / bảng entity-state — [SRS §3.B](../../020-Requirements/SRS-Comic-Studio.md) ghi thẳng *"sẽ được đặc tả tại tầng 030-Specs"* | Lô `docs/030-Specs/Schema/DB-Entity-*.md` (architect) | Trước **migration số 1** của schema `story` |
| Tập giá trị hợp lệ của **`permanence`** — nguồn chỉ liệt kê nó là một field của event payload, ⛔ không liệt kê giá trị | Lô `DB-Entity-*` + BA (cần chốt cùng ngữ nghĩa nghiệp vụ) | Trước khi `Story-Story-Bible-Extraction` vào Active Sprint |
| Ngữ nghĩa và quy tắc cấp phát **`beat_no`** (chỉ biết nó dùng để chia nhỏ trong một scene) | Lô `DB-Entity-*` (architect) | Cùng lúc chốt DDL `story.event` — trước **migration số 1** |
| ⚠️ **Không có exit criterion `M1-x` nào đặt tên trực tiếp cho resolver** — `M1-3` đo **extraction**, ⛔ không đo phép `reduce`. Anchor đang dùng tạm là `P-4` | **PM** — [Story-Timeline-State-Resolver](../../022-User-Stories/Backlog/Story-Timeline-State-Resolver.md) §3 Bối cảnh & nguồn ghi đây là **khoảng trống nguồn cần báo cáo** | Trước khi PM chấm exit criterion gate `M1` |

## Đã quyết ở đâu

> Bảng truy vết. Mọi nguồn được đọc trực tiếp tại thời điểm viết, ⛔ không sao chép từ tài liệu trung gian. ⭐ Neo bằng **mã requirement / tên mục**, ⛔ **không dùng số dòng** — số dòng mục ngay khi file nguồn đổi một ký tự.

| Quyết định | Mã `D-xx` | Nguồn (file + mã requirement) |
|---|:--:|---|
| **Thay hẳn `(chapter, scene)`**: hai trục `reading_order` / `story_order`; `story_order` `NUMERIC` **sparse** bước **1000**, **editable**; `timeline_id` có `kind ENUM(main/flashback/parallel/dream)` + `anchor_order`; state neo vào `Event` **mức scene** (chia nhỏ bằng `beat_no`) | `D-15` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) §3.B `SRS-FR-04` · [MVP-Scope](../../010-Planning/MVP-Scope.md) §3 `B4` · [BRD-002](../../020-Requirements/BRD/BRD-002-Story-Intelligence.md) `BR-002-07` · [Story-Fix-Narrative-Time-Key](../../022-User-Stories/Backlog/Story-Fix-Narrative-Time-Key.md) §4 AC *"Xác minh được"* |
| **Lý do không thể hoãn**: `(chapter, scene)` sai âm thầm ở mọi flashback — ⛔ không crash, chỉ corrupt dữ liệu | `D-15` | [BRD-002](../../020-Requirements/BRD/BRD-002-Story-Intelligence.md) `BR-002-08` · [SRS §3.B](../../020-Requirements/SRS-Comic-Studio.md) · [Glossary](../../999-Resources/Glossary.md) mục *syuzhet vs fabula* |
| `state_at(N) = reduce(events where story_order <= N)` là **hàm thuần**; LLM **chỉ phát event** (`entity, attribute, value, permanence, evidence_span, confidence`) cho **một** chapter; ⭐ **code sở hữu state** | `D-16` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) §3.B `SRS-FR-05` · [MVP-Scope](../../010-Planning/MVP-Scope.md) §3 `B3` · [BRD-002](../../020-Requirements/BRD/BRD-002-Story-Intelligence.md) `BR-002-06` · [UC-02](../../020-Requirements/Use-Cases/UC-02-Review-And-Edit-Story-Bible.md) bước 2 |
| **ĐÚNG MỘT** hàm `resolveState(entity, at_event)` + **test guardrail** ⛔ không `ORDER BY chapter_no` trong bất kỳ đường resolve state nào | `D-17` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) §3.B `SRS-NFR-10` · [Risk-Register §2.1](../../010-Planning/Risk-Register.md) `R-15` cột *Mitigation*/*trigger* |
| Story Bible tách **hai trục Identity / Appearance**; gộp vào một field là **nguyên nhân của phần lớn lỗi consistency** | `D-19` | [BRD-002](../../020-Requirements/BRD/BRD-002-Story-Intelligence.md) `BR-002-05` · [UC-02](../../020-Requirements/Use-Cases/UC-02-Review-And-Edit-Story-Bible.md) bước 3, bước 7 |
| **Lint rule ở CI đang bảo vệ** seam `resolveState()` / `getBible()` — `comic` gọi `story` **duy nhất** qua hai hàm này | `D-04` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) §3.E `SRS-NFR-04` · [BRD-005](../../020-Requirements/BRD/BRD-005-Multi-Tenancy-And-Platform.md) `BR-005-06` · [ADR-009](./ADR-009-Modular-Monolith-Three-Schemas.md) `D3` |
| Hành vi biên của resolver: tất định · cô lập theo `timeline_id` · *"chưa có state"* tường minh · ⛔ không cache lệch nguồn · chuỗi event dài không bỏ sót | — | [Story-Timeline-State-Resolver](../../022-User-Stories/Backlog/Story-Timeline-State-Resolver.md) §4 AC *"Xác minh được"* + *"Đường không hạnh phúc"* |
| Ràng buộc toàn vẹn: insert event thiếu `story_order` bị **từ chối**, ⛔ không suy ra mặc định từ `(chapter, scene)` | — | [Story-Fix-Narrative-Time-Key](../../022-User-Stories/Backlog/Story-Fix-Narrative-Time-Key.md) §4 AC *"Đường không hạnh phúc"* |
| ⚠️ `pgvector` **không dùng ở MVP nhưng KHÔNG bị cấm vĩnh viễn** (Full Scope `🟡`) | `D-06` | [Story-Timeline-State-Resolver](../../022-User-Stories/Backlog/Story-Timeline-State-Resolver.md) §4 *"Story này KHÔNG làm"* · [MVP-Scope](../../010-Planning/MVP-Scope.md) §3 `B5` · [ADR-009](./ADR-009-Modular-Monolith-Three-Schemas.md) |
| **DDL đầy đủ** thuộc tầng 030-Specs, ⛔ không thuộc ADR này | — | [SRS §3.B](../../020-Requirements/SRS-Comic-Studio.md) |
| Nhiệm vụ *"đóng băng, không mở lại"* của ADR-011 và danh sách `D-15`/`D-16`/`D-17`/`D-19` | — | [findings/architect §2.2](../../010-Planning/pm-runs/2026-08-28-phase-2-architecture-design-comic-studio/findings/architect.md) · §1.3 |

---

_Created by architect_
_Author: trisjr_
