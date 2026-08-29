---
id: ADR-012
type: adr
status: draft
project: comic-studio
created: 2026-08-29
---

# ADR-012: Comic IR — spec là dữ liệu chính, ảnh chỉ là output

Related to: [SDD-Comic-Studio](./SDD-Comic-Studio.md)

## Context

> [!IMPORTANT]
> ⛔ **ADR này là RECORD-ONLY.** Nó **không quyết** gì mới. Mục đích duy nhất: **đóng băng** sáu quyết định đã CHỐT ở Phase 1 (`D-20`…`D-25`) thành một tài liệu trích dẫn được, để một run sau **không vô tình mở lại**. Chỗ nào Phase 1 để trống thì ở đây là `TBD` kèm **tên người đóng**, ⛔ không phải chỗ để em điền.

`comic-studio` có **một nguyên tắc chi phối toàn hệ thống**, và nó là nguyên tắc *kiến trúc dữ liệu*, không phải nguyên tắc *sản phẩm*: **spec là dữ liệu chính, ảnh chỉ là output** (`SRS-FR-07`, [SRS-Comic-Studio](../../020-Requirements/SRS-Comic-Studio.md) §3.C). Mọi thứ khác trong tầng `comic` là hệ quả của nó:

- Vì spec là dữ liệu chính nên **sửa một field rẻ hơn re-roll cả ảnh** — đó là toàn bộ luận điểm giá trị của editor tối thiểu ([Story-Comic-IR-Panel-Specification](../../022-User-Stories/Backlog/Story-Comic-IR-Panel-Specification.md) §1).
- Vì spec **tách khỏi granularity render** nên đổi per-panel ↔ whole-page **không đổi data model** (`SRS-FR-33`) — đường lui của gate `G2` tồn tại được là nhờ điều này.
- Vì spec là nơi khai `text_safe_zone` nên ràng buộc typesetting đi **ngược** vào compiler (`SRS-FR-13`), thay vì phát hiện muộn lúc bubble đã che mặt nhân vật.

### Vì sao phải viết ADR này ngay bây giờ

ADR-012 là **nền của DB schema `comic`**. Các file `DB-Entity-*` của schema `comic` sắp được viết sẽ **trỏ về đây** thay vì tự diễn giải lại Phase 1. Nếu không đóng băng, mỗi file schema sẽ tự đọc lại `SRS` một lần và **sáu cách đọc khác nhau** sẽ lọt vào DDL.

### ⚠️ Hai chỗ dễ bị hiểu nhầm — đọc trước `## Decision`

**(a) *"Ảnh chỉ là cache"* KHÔNG có nghĩa *"ảnh xoá được"*.**

Chữ *"cache"* ở `SRS-FR-07` mang đúng **một** nghĩa: ảnh **không phải nguồn sự thật của thiết kế** — thiết kế nằm ở spec, và spec một mình đủ để mô tả trang truyện. Nó **không** mang nghĩa *"tái tạo được nên mất cũng không sao"*.

Lý do: `D-44` (ghi ở [ADR-014](./ADR-014-Deterministic-Prompt-Compiler-And-Best-Of-N.md)) chốt rằng **bit-exact reproducibility không đạt được** — nhiều API không cho set seed, và provider cập nhật weights dưới cùng một tên model (silent model drift). Chạy lại compiler với **cùng** spec cho ra **cùng** prompt, nhưng **không** cho ra cùng pixel.

⇒ **Mất một object trong storage là mất VĨNH VIỄN một mắt xích provenance**, không phải mất một bản cache có thể hâm nóng lại. Ảnh là **bằng chứng** cho chuỗi lineage (`KC-1`…`KC-7`), và *"bằng chứng có thể thiếu ngẫu nhiên thì không phải bằng chứng"* (`SRS-NFR-13`).

⛔ Vì vậy **cấm** mọi thiết kế sau ở tầng schema và tầng vận hành:
- ⛔ TTL / eviction policy tự động trên object của generation đã được `approved_generation_id` trỏ tới.
- ⛔ Đối xử bucket ảnh như cache tier có thể regenerate on-miss.
- ⛔ Suy ra *"không cần backup vì tái tạo được"*.

**(b) Toạ độ chuẩn hoá 0–1 là ĐƯỜNG NÂNG CẤP, không phải một chi tiết lưu trữ.**

`page_layout JSONB` lưu bố cục bằng **toạ độ chuẩn hoá 0–1**. Đây là *"đường nâng cấp không mất mát"*: nếu về sau dựng canvas thật bằng thư viện có sẵn thì **không phải migrate dữ liệu**, chỉ thay lớp tương tác ([UC-08](../../020-Requirements/Use-Cases/UC-08-Arrange-Page-And-Preview.md) callout mở đầu điều 1, `MVP-Scope §4.1`, `CF-9.1`).

Đây chính là **lý do việc cắt infinite canvas ở MVP là hợp lệ**: cắt **lớp tương tác**, ⛔ **không** cắt khả năng. Cùng một dữ liệu render được **thumbnail** và **bản in 300 DPI** (`SRS-FR-11`) — độc lập với DPI là hệ quả trực tiếp của việc không lưu pixel.

⇒ Đọc `0–1` thành *"đơn vị lưu trữ, đổi sang pixel cho tiện cũng được"* là **đóng một cánh cửa đang mở**.

---

## Decision

### Tầng CHỐT — ⛔ bất biến, không đổi mà không viết ADR mới

**1. `Panel Specification` là bản ghi dữ liệu chính của tầng `comic` (`D-20`).**
Ảnh sinh ra **liên kết tới spec qua khoá ngoại**; ⛔ **không có ảnh nào tồn tại mà không trỏ về một spec** ([Story-Comic-IR-Panel-Specification](../../022-User-Stories/Backlog/Story-Comic-IR-Panel-Specification.md) AC). Một spec trả về **0 hoặc nhiều** ảnh — quan hệ 1-n, chiều phụ thuộc chỉ đi một hướng: `ảnh → spec`.

**2. Panel spec TÁCH KHỎI granularity render (`D-20`).**
Một page **compile được nhiều panel spec thành một prompt**. Đây là điều kiện để `SRS-FR-33` (per-panel là mặc định, whole-page là đường lui đã thiết kế sẵn) đổi được **mà không đổi data model**. ⛔ Không được nhúng giả định *"1 spec = 1 ảnh"* vào bất kỳ khoá, ràng buộc, hay index nào.

**3. Trần ≤3 nhân vật/panel là `CHECK` constraint ở TẦNG DB (`D-21`).**
⛔ **Không** phải guideline trong prompt, ⛔ **không** phải cảnh báo UI. Tiêu chí nghiệm thu nguyên văn của exit criterion `M2-2`: *"insert panel 4 nhân vật **bị từ chối**, **không phải** bị cảnh báo"*.

Hình dạng bắt buộc, kế thừa từ [Story-Enforce-Max-Three-Characters-Per-Panel](../../022-User-Stories/Backlog/Story-Enforce-Max-Three-Characters-Per-Panel.md):
- Constraint đặt trên bảng panel **hoặc** bảng liên kết `panel–character`.
- Chặn **cả đường `UPDATE`** (thêm nhân vật thứ 4 vào panel đã có 3), không chỉ `INSERT`.
- Chặn được **race**: hai transaction đồng thời mỗi cái thêm 1 nhân vật vào panel đang có 2 **không** được để lọt panel 4 nhân vật. Constraint ở tầng DB thoả điều này tự nhiên vì kiểm tại thời điểm commit, không phải tại thời điểm đọc.
- Ngưỡng là **giá trị cấu hình được tại MỘT chỗ duy nhất** (mặc định `3`), ⛔ không hard-code rải rác.

**4. Ngưỡng đổi từ `3` xuống `2` chỉ xảy ra bằng quyết định người, tại gate (`D-21`).**
Nếu gate `G1-d` không đạt ngưỡng, trần siết xuống **≤2 ngay trong schema** (`BR-003-06`). ⛔ Hệ thống **không** tự siết; Story chỉ bảo đảm cơ chế **có thể** đổi ngưỡng bằng một thay đổi.

**5. Bố cục lưu bằng toạ độ chuẩn hoá **0–1** trong `page_layout JSONB`, và đó là NƠI LƯU DUY NHẤT (`D-22`).**
**Template chỉ là preset ghi vào CÙNG schema đó** — ⛔ **không có schema thứ hai cho template** ([UC-08](../../020-Requirements/Use-Cases/UC-08-Arrange-Page-And-Preview.md) bước 6). ⛔ **KHÔNG viết renderer từ đầu** (`CF-9.1`).

**6. Layout quyết định bằng rubric rời rạc + bảng tra deterministic (`D-23`).**
Đầu vào của bảng tra:
| Đầu vào | Ai sinh ra | Kiểu |
|---|---|---|
| `beat_type` | rubric **enum có anchor example** | rời rạc |
| `dialogue_density` | ⭐ **code đếm** | dẫn xuất |
| `character_count` | ⭐ **code đếm** | dẫn xuất |

Cộng thêm **emphasis budget theo phạm vi chapter**. `findings/architect.md` §1.4 `D-23` ghi mức trần cụ thể: *"tối đa **1 full page + 2–3 large panel**"* — con số này là **cấu hình**, ⛔ không hard-code.

**7. ⭐ LLM CHỈ XẾP HẠNG BEAT — CODE PHÂN BỔ QUOTA (`D-23`).**
Đây là ranh giới cứng, cùng họ với `SRS-FR-05` (*"LLM chỉ phát event, **code sở hữu state**"*) và `SRS-FR-17` (*"không LLM ở compiler runtime"*):

> LLM nhận các beat trong **một chapter** và trả về **thứ hạng**. Sau đó **code** — không phải LLM — duyệt thứ hạng đó và **phân bổ** emphasis theo quota còn lại.

⛔ Cấm: để LLM trả thẳng *"panel này full page"*. ⛔ Cấm: để LLM biết quota còn bao nhiêu rồi tự cân. Lý do: quota là **ràng buộc toàn cục trên phạm vi chapter**; giao nó cho một hàm không xác định là làm mất tính kiểm chứng được của toàn bộ `D-23`, và biến `D-24` thành vô nghĩa (xem điều 8).

**8. ⛔ CẮT HẲN Layout Score 5 số thực (`D-24`) — `SRS-NFR-22`.**
⚠️ Đây là **cắt CƠ CHẾ, GIỮ MỤC TIÊU**. Mục tiêu *"layout phản ánh narrative importance"* **vẫn còn nguyên** và được đáp ứng bằng điều 6 + điều 7. ⛔ Đọc `D-24` thành *"bỏ luôn ý tưởng layout theo tầm quan trọng"* là **cắt nhầm**.

**9. `text_safe_zone` + `text_budget` + `negative_space_hint` là FIELD CỦA PANEL SPEC (`D-25`).**
Và Visual Prompt Compiler **phải truyền yêu cầu chỗ trống xuống prompt** — ⭐ ràng buộc đi **NGƯỢC** từ typesetting vào compiler.

Đây không phải một tối ưu hoá. `text_safe_zone` thiếu thì *"bubble che mặt nhân vật và **phải sinh lại toàn bộ ảnh đã làm**"* ([UC-08](../../020-Requirements/Use-Cases/UC-08-Arrange-Page-And-Preview.md) P2, `BR-003-08`). Hình dạng bắt buộc, kế thừa từ [Story-Text-Safe-Zone-In-Panel-Spec](../../022-User-Stories/Backlog/Story-Text-Safe-Zone-In-Panel-Spec.md):
- ≥1 vùng **toạ độ chuẩn hoá 0–1** (cùng hệ với `page_layout`, điều 5).
- Tính theo **bố cục thực tế** của panel; ⛔ không phải một vùng cố định giống nhau cho mọi panel.
- Panel gần kín khung ⇒ trả `text_safe_zone` **rỗng hoặc tối thiểu kèm cảnh báo**; ⛔ **không** ép một vùng đè lên nhân vật *"cho có"*.
- Panel **không** thoại ⇒ vẫn tính `text_safe_zone` (dự phòng thêm thoại sau).

### `TBD` — ⛔ lô này KHÔNG đóng

| Khoảng trống | Vì sao chưa đóng được | **Ai đóng** | Khi nào |
|---|---|---|---|
| `layout_template` là **bảng catalog** hay **seed data / hằng số trong code**? | Nguyên văn Phase 1 (*"template chỉ là preset ghi vào CÙNG schema đó"*, *"không có schema thứ hai cho template"*) **thoả cả hai cách đọc** — xem `findings/architect.md` §7 `G14`. Cả hai đều **không** vi phạm điều 5. Chọn một là **quyết định mới**, ngoài mandate record-only của ADR này | **Architect tại lô DB Schema** (file `DB-Entity-*` sở hữu `page_layout`), PM duyệt | Trước khi viết DDL của schema `comic` |
| Danh sách **trường bắt buộc đầy đủ** của `Panel Specification` (ngoài 5 trường tối thiểu đã ký ở Story) | Story chỉ ký **tối thiểu** 5 trường; tập đầy đủ chưa ai đặc tả | **Architect tại lô DB Schema** | Cùng lúc với DDL |

---

## Alternatives considered

> Mục này là **lý do các phương án kia bị LOẠI**, ghi lại để không phải tranh luận lại. ⛔ Không phải một danh sách mở.

### (a) Ảnh là dữ liệu chính, spec chỉ là metadata sinh ra ảnh — ⛔ LOẠI

**Vì sao có vẻ hợp lý**: đây là mô hình mặc định của gần như mọi công cụ AI image hiện có. Người dùng nghĩ bằng ảnh, và lưu ảnh là đủ để hiển thị.

**Vì sao bị loại**:
1. **Sửa một chi tiết trở thành re-roll cả ảnh.** Toàn bộ luận điểm giá trị của editor tối thiểu — *"sửa một field thay vì re-roll cả ảnh"* — biến mất.
2. **Mất đường lui `G2`.** `SRS-FR-33` đòi đổi per-panel ↔ whole-page **không đổi data model**. Nếu ảnh là dữ liệu chính thì granularity render **chính là** granularity lưu trữ ⇒ đổi granularity = migrate toàn bộ.
3. **Không có chỗ khai `text_safe_zone`.** Ràng buộc ngược từ typesetting (`SRS-FR-13`) cần một nơi khai **trước khi** ảnh tồn tại. Không có spec thì không có nơi đó, và bubble che mặt trở thành lỗi phát hiện muộn.
4. **Không có neo cho lineage.** `parent_generation_id` cần một thực thể ổn định để nhiều generation cùng trỏ về. Nếu ảnh là gốc thì mỗi lần regenerate sinh một gốc mới.

### (b) Trần ≤3 nhân vật đặt ở tầng prompt / validation phía application — ⛔ LOẠI

**Vì sao có vẻ hợp lý**: mềm hơn, dễ nới khi gặp cảnh đông người, không phải migrate khi đổi ngưỡng.

**Vì sao bị loại**:
1. **Đúng tiêu chí nghiệm thu đo điều ngược lại.** `M2-2` đo *"insert panel 4 nhân vật **bị từ chối**, không phải bị cảnh báo"*. Cảnh báo mềm **không thoả `M2-2`**.
2. **Thất bại âm thầm ở chỗ đau nhất.** Nền của quyết định là `CF-6.5` `[OFF]`: ID-Sim **42.33** (2 nhân vật) → **27.21** (3) → **2.67** (4) → **0.52** (5). Bậc `3 → 4` là một **vực**, không phải một dốc. Vượt trần không báo lỗi mà chỉ ra ảnh sai identity — đúng kiểu lỗi mà `R-12` cảnh báo.
3. **Validation phía application không chặn được race.** Đọc-rồi-ghi từ hai transaction đồng thời lọt panel 4 nhân vật; chỉ constraint tại commit mới chặn được.
4. ⚠️ **Caveat `CF-6.4` KHÔNG làm lỏng quyết định.** `SRS-FR-08` ghi rõ bằng chứng mang caveat: *"không benchmark độc lập nào đo frontier model ở 2–3 nhân vật ⇒ MVP0 phải tự đo"*. Caveat này là lý do có gate `G1-d`, ⛔ **không** phải lý do hạ constraint xuống tầng mềm.

Đường hợp lệ cho cảnh đông người: **shot xa / silhouette / crop** (`BR-003-07`), ⛔ không phải nới trần.

### (c) Layout Score 5 số thực — ⛔ LOẠI (`SRS-NFR-22`)

**Vì sao có vẻ hợp lý**: một vector 5 chiều cho phép xếp hạng mượt, nội suy, và tối ưu bố cục bằng hàm mục tiêu.

**Vì sao bị loại**: **không có prior art** — *"chưa ai làm vì không đáng"* (`CF-9.3`, `Analysis §6.3`). Năm số thực do LLM sinh **không kiểm chứng được**: không cách nào nói một điểm `3.7` là đúng hay sai, nên không cách nào test, không cách nào regression. Rubric rời rạc có anchor example thì **so được với anchor**.

⚠️ Loại **cơ chế**, ⛔ **không** loại mục tiêu — thay bằng `D-23`.

### (d) Để LLM quyết luôn emphasis (full page / large panel) thay vì chỉ xếp hạng — ⛔ LOẠI

**Vì sao có vẻ hợp lý**: ít bước hơn, LLM đã đọc chapter nên nó "biết" chỗ nào quan trọng.

**Vì sao bị loại**: emphasis budget là **ràng buộc toàn cục trên phạm vi chapter**. Một hàm không xác định, chạy trên từng beat, **không giữ được bất biến toàn cục** — nó sẽ cấp full page cho 6 beat rồi mới phát hiện hết quota. Tách *xếp hạng* (LLM) khỏi *phân bổ* (code) là cách duy nhất giữ quota kiểm chứng được, và là cùng một khuôn với `SRS-FR-05` và `SRS-FR-17`.

### (e) Schema thứ hai cho layout template (catalog riêng, hình dạng riêng) — ⛔ LOẠI

**Vì sao có vẻ hợp lý**: template là dữ liệu tĩnh do hệ thống sở hữu, page layout là dữ liệu động do user sở hữu — tách ra trông sạch hơn.

**Vì sao bị loại**: hai hình dạng dữ liệu cho **cùng một khái niệm bố cục** nghĩa là **hai renderer** hoặc **một tầng dịch**. Cả hai đều vi phạm `CF-9.1` (*"không viết renderer từ đầu"*) và làm mất tính chất *"đổi template = một click"* (`SRS-FR-10`). Nguyên văn: *"template chỉ là các preset ghi vào **CÙNG** schema đó"*.

⚠️ Việc template được **materialize** từ một catalog table hay từ hằng số trong code **vẫn để `TBD`** (xem `## Decision`) — đó là câu hỏi *nguồn của preset*, không phải câu hỏi *schema của bố cục*.

### (f) Lưu bố cục bằng toạ độ pixel theo một canvas cố định — ⛔ LOẠI

**Vì sao có vẻ hợp lý**: đỡ phải nhân/chia, debug dễ hơn, khớp trực tiếp với cái compositor cần.

**Vì sao bị loại**: khoá cứng vào **một** kích thước. Cùng một dữ liệu phải render được **thumbnail** và **bản in 300 DPI** (`SRS-FR-11`); pixel-space làm điều đó thành một phép scale có mất mát, và làm đường nâng cấp lên canvas trở thành **migrate dữ liệu** thay vì thay lớp tương tác.

---

## Consequences

### ⭐ Hợp đồng mà 13 file `DB-Entity-*` của schema `comic` kế thừa

> Các file schema sắp viết **trỏ về mục này**, ⛔ không tự diễn giải lại `SRS`.

| # | Ràng buộc bắt buộc xuất hiện trong DDL | Neo |
|---|---|---|
| 1 | `CHECK` trần nhân vật/panel ở **tầng DB**, chặn cả `INSERT` và `UPDATE`, ngưỡng đọc từ **một** chỗ cấu hình (mặc định `3`) | `D-21` · `M2-2` |
| 2 | Khoá ngoại **ảnh → spec** là `NOT NULL`; ⛔ không có ảnh mồ côi | `D-20` · `STORY-C-01` |
| 3 | Spec thiếu trường bắt buộc bị **DB từ chối**, ⛔ không phải log cảnh báo | `STORY-C-01` |
| 4 | Spec tham chiếu `character_id` không tồn tại trong Story Bible bị từ chối **tại thời điểm ghi**, ⛔ không phải phát hiện muộn lúc sinh ảnh | `STORY-C-01` |
| 5 | `page_layout JSONB` là **nơi lưu duy nhất** của bố cục; template ghi vào cùng schema | `D-22` |
| 6 | Mọi toạ độ trong `page_layout` và `text_safe_zone` là **0–1**; ⛔ không pixel | `D-22` · `D-25` |
| 7 | `text_safe_zone`, `text_budget`, `negative_space_hint` là **field của panel spec**, ⛔ không nằm ở tầng typeset | `D-25` |
| 8 | ⛔ Không khoá / index / constraint nào được giả định *"1 spec = 1 ảnh"* | `D-20` · `SRS-FR-33` |
| 9 | ⛔ Không cột nào lưu Layout Score hay bất kỳ vector điểm số thực nào cho bố cục | `D-24` · `SRS-NFR-22` |

### Tích cực

1. **Editor tối thiểu trở nên khả thi trong ngân sách.** Sửa spec thay vì re-roll ảnh là lý do năm thành phần editor nằm vừa trong `~20–25%` effort `[EM]` (`CF-6.7`; ⚠️ `CẤM-01`: không trừ con số này cho `CF-6.8`).
2. **Đường lui `G2` mở sẵn, không tốn gì.** Đổi render granularity không chạm data model.
3. **Đường lên canvas mở sẵn, không tốn gì.** Toạ độ 0–1 ⇒ thay lớp tương tác, không migrate.
4. **Bubble che mặt trở thành lỗi bắt được SỚM.** `text_safe_zone` khai ở spec ⇒ compiler biết trước khi tốn tiền sinh ảnh.
5. **Trần nhân vật thành sự thật kiểm chứng được**, không phải một lời hứa trong prompt.

### Tiêu cực — cái gì trở nên KHÓ HƠN

1. **Director phải sinh spec ĐẦY ĐỦ trước khi có ảnh nào.** Không có đường *"sinh ảnh trước, mô tả sau"*. Chi phí này trả trước và không tránh được.
2. **Cảnh đông người không giải bằng cách nới trần.** Phải giải bằng shot xa / silhouette / crop ⇒ Director phức tạp hơn, và một số cảnh nguồn sẽ **không** dựng được đúng ý.
3. **`text_safe_zone` tính từ bố cục thực tế là một bài toán khó ở chính nó.** Panel gần kín khung có thể trả về vùng rỗng ⇒ luồng phải xử lý được trạng thái *"không có chỗ đặt bubble"* thay vì giả định luôn có.
4. **Rubric rời rạc kém mượt hơn điểm số thực.** Beat rơi vào ranh giới hai `beat_type` sẽ bị chấm cứng. Lối thoát đã có: **đổi layout template bằng một click** (`SRS-FR-10`) — ⚠️ đây là requirement của lô khác, nhắc ở đây để không ai tưởng rubric là đường một chiều.
5. ⛔ **Object storage KHÔNG được vận hành như cache.** Xem callout (a) ở `## Context`. Điều này ràng buộc cả chính sách backup lẫn bất kỳ eviction nào — và nó **đắt hơn** một cache thật.

### Điều KHÔNG được suy ra từ ADR này

- ⛔ Không suy ra rằng ảnh xoá được (callout (a)).
- ⛔ Không suy ra rằng mục tiêu *"layout theo narrative importance"* bị cắt (`D-24` cắt **cơ chế**).
- ⛔ Không suy ra rằng cắt canvas là cắt khả năng canvas (callout (b)).
- ⛔ Không suy ra `layout_template` là bảng, cũng không suy ra nó không phải bảng — đó là `TBD` có chủ.

---

## Đã quyết ở đâu

> ⛔ Mọi hàng dưới đây **đã CHỐT ở Phase 1**. ADR này chỉ ghi lại. Neo bằng **mã requirement**, ⛔ không neo bằng số dòng (số dòng của `SRS` đã thay đổi trong run và không còn tin được).

| Quyết định | Mã `D-xx` | Nguồn (file + mã requirement) |
|---|:--:|---|
| **Spec là dữ liệu chính, ảnh chỉ là output**; panel spec **tách khỏi granularity render** — một page compile được nhiều panel spec thành một prompt | `D-20` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) **`SRS-FR-07`** (§3.C) · **`SRS-FR-33`** (§3.F, đường lui `G2`) · §2.1 (*"nguyên tắc kiến trúc chi phối toàn bộ"*) · `MVP-Scope §3 C1`, `A7` · [Story-Comic-IR-Panel-Specification](../../022-User-Stories/Backlog/Story-Comic-IR-Panel-Specification.md) |
| **Trần ≤3 nhân vật/panel là `CHECK` constraint ở TẦNG DB** — insert panel 4 nhân vật **bị từ chối**, ⛔ không phải bị cảnh báo | `D-21` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) **`SRS-FR-08`** (§3.C) · `MVP-Scope §3 C5` · `Charter §7 C3` `[OFF]` `CF-6.5` · `Charter §4 R1` · `R-12` · exit criterion **`M2-2`** · [UC-03](../../020-Requirements/Use-Cases/UC-03-Review-Panel-Script.md) bước 7 · [UC-08](../../020-Requirements/Use-Cases/UC-08-Arrange-Page-And-Preview.md) **EX-6** · [Story-Enforce-Max-Three-Characters-Per-Panel](../../022-User-Stories/Backlog/Story-Enforce-Max-Three-Characters-Per-Panel.md) |
| ID-Sim theo số nhân vật: **42.33** (2) → **27.21** (3) → **2.67** (4) → **0.52** (5) — nền định lượng của trần | `D-21` | `CF-6.5` `[OFF]` (trích trong [UC-08](../../020-Requirements/Use-Cases/UC-08-Arrange-Page-And-Preview.md) **EX-6**) |
| Caveat `CF-6.4` (*không benchmark độc lập ở 2–3 nhân vật ⇒ MVP0 tự đo*) ⛔ **không làm lỏng** quyết định; siết `3 → 2` chỉ sau verdict gate **`G1-d`** | `D-21` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) **`SRS-FR-08`** (ghi chú caveat trong chính hàng) · `BR-003-06` · [Story-Enforce-Max-Three-Characters-Per-Panel](../../022-User-Stories/Backlog/Story-Enforce-Max-Three-Characters-Per-Panel.md) §"Không làm" |
| **Bố cục lưu bằng toạ độ chuẩn hoá 0–1 trong `page_layout JSONB`**; **template chỉ là preset ghi vào CÙNG schema**, ⛔ không có schema thứ hai; đường nâng cấp lên canvas **không phải migrate** | `D-22` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) §3.D callout `[!IMPORTANT]` **mục 2** (⚠️ mục này **không mang mã `SRS-FR` riêng**; nó dẫn **`SRS-FR-11`** cho phần *"cùng dữ liệu render thumbnail và bản in 300 DPI"*) · `MVP-Scope §4.1` · `CF-9.1` · [UC-08](../../020-Requirements/Use-Cases/UC-08-Arrange-Page-And-Preview.md) callout điều 1, **P3**, **bước 6** · `BR-004-07` · `BR-003-04` |
| **Rubric `beat_type` rời rạc** (enum có anchor example) + `dialogue_density` **code đếm** + `character_count` **code đếm** → **bảng tra deterministic**; cộng **emphasis budget phạm vi chapter** | `D-23` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) **`SRS-FR-09`** (§3.C) · `MVP-Scope §3 C3` · `CF-9.3` · `Analysis §5.3` (A)+(B) |
| ⭐ **LLM chỉ XẾP HẠNG beat trong chapter — CODE phân bổ theo quota** | `D-23` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) **`SRS-FR-09`** (nguyên văn: *"LLM chỉ **xếp hạng** beat trong chapter, code phân bổ theo quota"*) · cùng khuôn với **`SRS-FR-05`** và **`SRS-FR-17`** |
| Mức trần emphasis cụ thể: **tối đa 1 full page + 2–3 large panel** trên phạm vi chapter | `D-23` | `findings/architect.md` §1.4 hàng `D-23` (dẫn `Analysis §5.3`) — ⚠️ **không** xuất hiện thành con số trong `SRS-FR-09`; xử lý như **cấu hình** |
| ⛔ **CẮT HẲN Layout Score 5 số thực** — cắt **cơ chế**, ⚠️ **GIỮ mục tiêu** (layout theo narrative importance), thay bằng `D-23` | `D-24` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) **`SRS-NFR-22`** (§6.1 Negative requirements) · `MVP-Scope §3 C4` (`❌ cắt hẳn`) · `CF-9.3` · `Analysis §6.3` |
| `text_safe_zone` + `text_budget` + `negative_space_hint` là **field của panel spec**; compiler **phải truyền yêu cầu chỗ trống xuống prompt** — ràng buộc đi **NGƯỢC** từ typesetting vào compiler | `D-25` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) **`SRS-FR-13`** (§3.C) · `MVP-Scope §3 C6` (`CF-8.8`) · `Analysis §5.4` lý do 2 · [Story-Text-Safe-Zone-In-Panel-Spec](../../022-User-Stories/Backlog/Story-Text-Safe-Zone-In-Panel-Spec.md) · `BR-003-08` · `BR-003-09` (ngưỡng **≥95%** `[EM]`, exit criterion **`M2-3`**) |
| ⚠️ *"Ảnh là cache"* ⛔ **không** kéo theo *"ảnh tái tạo được / xoá được"* — bit-exact **không** đạt được ⇒ mất object là **mất vĩnh viễn** một mắt xích provenance | `D-44` (ghi ở [ADR-014](./ADR-014-Deterministic-Prompt-Compiler-And-Best-Of-N.md)) | [SRS](../../020-Requirements/SRS-Comic-Studio.md) §3.A callout `[!CAUTION]` (*"`seed` là provenance metadata, không phải replay key"*) · **`SRS-NFR-13`** (*"bằng chứng có thể thiếu ngẫu nhiên thì không phải bằng chứng"*) |

### Khoảng trống — ⛔ ADR này KHÔNG đóng

| Khoảng trống | Nguồn ghi nhận | **Ai đóng** |
|---|---|---|
| `layout_template` = **bảng catalog** hay **seed data / hằng số**? Nguyên văn Phase 1 thoả **cả hai** cách đọc | `findings/architect.md` §7 **`G14`** | **Architect tại lô DB Schema** + PM duyệt tại gate |
| Tập **đầy đủ** trường bắt buộc của `Panel Specification` (Story chỉ ký **5 trường tối thiểu**) | [Story-Comic-IR-Panel-Specification](../../022-User-Stories/Backlog/Story-Comic-IR-Panel-Specification.md) AC-1 | **Architect tại lô DB Schema** |

---

_Ghi lại bởi System Architect — lô L6 (record-only), Phase 2._
_Author: trisjr_
