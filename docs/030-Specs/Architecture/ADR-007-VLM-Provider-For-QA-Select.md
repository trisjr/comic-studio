---
id: ADR-007
type: adr
status: draft
project: comic-studio
created: 2026-08-29
---

# ADR-007: Provider VLM cho QA-select giữa N candidate

Related to: [SDD-Comic-Studio](./SDD-Comic-Studio.md)

## Context

### Cơ chế đã CHỐT — ⛔ ADR này không mở lại

| Nội dung | Mã | Nguồn |
|---|:--:|---|
| **best-of-N**: sinh **N candidate cho MỌI panel** rồi **VLM QA-select 1**. ⚠️ ⛔ **KHÔNG phải retry-on-failure**. N mặc định = **3** | `D-37` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-FR-20` |
| **Continuity Checker = QA-based selection giữa N candidate**; output là **hàng đợi review được xếp hạng**; ⛔ cắt hẳn `[Fix automatically]`; giữ **cả hai** version, side-by-side, **NGƯỜI CHỌN**, ⛔ không bao giờ tự áp dụng; **`unclear` là câu trả lời hợp lệ hạng nhất** | `D-38` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-FR-21` |
| Phải **hiện tường minh độ phủ** của checker cho user | `D-39` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-FR-22` |

### Cái chưa ai quyết

⛔ **Không tài liệu Phase 1 nào chọn provider VLM** ([findings §5 hàng #2](../../010-Planning/pm-runs/2026-08-28-phase-2-architecture-design-comic-studio/findings/architect.md)).

### ⚠️ Đây là integration KHÁC image provider — ⛔ không gộp

`D-40` ([SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-FR-23`) đã chốt **adapter per image provider**. VLM QA-select là **integration thứ hai, riêng biệt**, không phải một hàm của adapter ảnh. [findings §5 lưu ý #1](../../010-Planning/pm-runs/2026-08-28-phase-2-architecture-design-comic-studio/findings/architect.md) nói thẳng lý do: **gộp chúng làm che mất chuyện chi phí VLM chưa được tính vào bất kỳ con số COGS nào.**

Ba lý do kỹ thuật độc lập nữa: hai vòng đời model version khác nhau (pin riêng); hai đường lỗi khác nhau (ảnh sinh xong nhưng chấm hỏng là một trạng thái hợp lệ — xem [Story-Usage-Event AC *"VLM-select thất bại sau khi cả 3 candidate đã sinh"*](../../022-User-Stories/Backlog/Story-Usage-Event-And-Daily-Rollup.md)); hai đường chi phí phải đo **tách** thì mới bù được khoản đang thiếu.

### ⛔ Khoản chi phí đang thiếu

[SRS](../../020-Requirements/SRS-Comic-Studio.md) §4.3 ghi trong bảng External Interfaces: *"VLM (QA-select giữa N candidate) | Cơ chế **CHỐT**; ⚠️ **chi phí VLM call để score N candidate là phần CHƯA TÍNH** của `CF-3.5` ⇒ không có số"*.
[SRS](../../020-Requirements/SRS-Comic-Studio.md) §5.2 lặp lại trong bảng `TBD`: *"Chi phí VLM call để score N candidate | `CF-3.5` ghi rõ đây là phần **chưa tính** ⇒ không có số"*.
[SRS](../../020-Requirements/SRS-Comic-Studio.md) §5.1: *"COGS sàn/chapter | **$12,06** @N=3, Gemini batch — ⛔ **là SÀN, không phải trần** (chưa tính VLM call để score 3 candidate)"*, kèm `CẤM-04`.

⇒ Xem [Consequences](#consequences). Đây là phần **bắt buộc** của ADR này.

---

## Decision

### Q1. VLM QA-select là một integration riêng, có adapter riêng

- Một interface `VlmQaSelector`, ⛔ **không** gộp vào adapter image provider của `D-40`.
- File spec tương ứng ở lô sau: `Spec-Integration-VLM-QA-Select.md`, ⛔ **tách khỏi** `Spec-Integration-Image-Provider.md`.
- Nằm trong module `M5` (Generation Pipeline). ⚠️ ⛔ **Không** được gọi từ Visual Prompt Compiler — `D-34` cấm LLM/VLM ở compiler runtime ([SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-FR-17`). QA-select chạy **sau** khi N candidate đã sinh xong, là một bước riêng của pipeline.

### Q2. Hợp đồng của adapter — chốt hình dạng, chưa chốt vendor

| Mặt | Nội dung | Neo vào |
|---|---|---|
| **Input** | N candidate (storage key, ⛔ không phải blob — `D-13`) · panel spec ràng buộc (identity reference, trần ≤3 nhân vật) · bộ câu hỏi kiểm tra | `D-13`, `D-21` |
| **Output** | **Danh sách xếp hạng** + mỗi candidate một `verdict ∈ {pass, fail, unclear}` + lý do ngắn + `confidence` | `D-38` — output là *"hàng đợi review được xếp hạng"* |
| **`unclear`** | ⭐ Là giá trị **hạng nhất**. ⛔ **Không** map thành `fail`, ⛔ **không** map thành `pass`, ⛔ **không** ép thành số rồi cắt ngưỡng | `D-38` ([SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-FR-21`) |
| **Quyền hạn** | Adapter **chỉ xếp hạng và giải thích**. ⛔ **Không** tự chọn thay người ở đường có `[Fix automatically]`; giữ cả N candidate, hiển thị side-by-side | `D-38` |
| **Version** | Pin `model_id` + `model_version` tường minh trong config; ghi vào bản ghi chấm của **mọi** lần gọi | mẫu `D-40` ([SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-FR-23`) + `D-59` ([SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-FR-31`) |
| **Từ chối vì content policy** | Ghi lại **mọi** lần provider từ chối | `D-67` ([SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-NFR-20`) |

### Q3. Chế độ mặc định khi khởi động: **report-only**

[SRS](../../020-Requirements/SRS-Comic-Studio.md) §5.1 đặt cổng chất lượng: *"precision ≥ ~0.7 trên ≥ 100 panel dán nhãn tay, **trước khi bật một check nào** — kể cả `face`"* (nhãn `[EM]`).

⇒ ⭐ **Trạng thái mặc định của mọi check là report-only.** Bật một check thành *"có ảnh hưởng tới lựa chọn"* chỉ sau khi cổng §5.1 PASS cho **chính check đó**. ⛔ Không bật cả cụm một lượt.

### Q4. Provider = **`TBD`** — và lý do không phải là sự lười

⛔ ADR này **không chọn vendor**, vì:

1. Biến quyết định chính là **chi phí per-call × N × số panel/chapter**, mà [SRS](../../020-Requirements/SRS-Comic-Studio.md) §5.2 ghi rõ con số đó **không tồn tại trong repo**.
2. [SRS](../../020-Requirements/SRS-Comic-Studio.md) §5.2 cấm tuyệt đối tự gán số: *"Bịa một con số performance là lỗi nghiêm trọng hơn để trống nó."*
3. Hai đại lượng quyết định khác cũng chưa có: **`N` tối thiểu** (`CF-8.5`, mỗi bậc N giảm ≈33% COGS — [SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-FR-20`) và **human-reject rate sau VLM-select** ([SRS](../../020-Requirements/SRS-Comic-Studio.md) §5.2 ghi *"chưa ai công bố con số này"*). Chọn vendor trước khi có hai số này là chọn mù.

**Ai đóng**: PM + Architect. **Khi nào**: tại gate cuối **MVP0**, khi ba phép đo bắt buộc của MVP0 có kết quả.

### Q5. Nhưng chốt được ngay: **tiêu chí chọn**, theo thứ tự

Để 14 file API ở lô sau không bị chặn, ADR này chốt **tiêu chí**, không chốt tên:

| # | Tiêu chí | Vì sao ở thứ tự này |
|--:|---|---|
| **1** | **Nhận nhiều ảnh trong MỘT call** để so sánh N candidate trong cùng ngữ cảnh | Nếu provider chỉ nhận 1 ảnh/call thì **bản chất bài toán đổi**: từ *"so sánh N"* thành *"chấm điểm từng cái rồi so số"*, và chi phí nhân N. Đây là tiêu chí **loại**, không phải tiêu chí **cộng điểm** |
| **2** | **Structured output ổn định**, map thẳng vào `{pass, fail, unclear}` | `D-38` bắt `unclear` là giá trị hạng nhất ⇒ output tự do phải parse là chỗ `unclear` bị bóp méo thành `fail` |
| **3** | **Version pinning tường minh** | `D-40` + `D-44`/`D-66`: **silent model drift** là rủi ro đã được nêu tên; không pin được thì không phát hiện được drift |
| **4** | **Batch / async mode** | `D-41` chốt batch cho **image** ([SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-FR-24`). Với VLM đây là **mong muốn**, ⛔ không phải CHỐT — pipeline đã async nên batch là fit tự nhiên |
| **5** | **Chi phí per-call** | Chỉ **so sánh được** sau khi (1) đã lọc — vì nếu phải gọi N lần thì đơn giá per-call không nói lên gì |

### Q6. Hành vi khi VLM lỗi / timeout — ⛔ không được tự chọn

[Story-Usage-Event AC *"VLM-select thất bại sau khi cả 3 candidate đã sinh"*](../../022-User-Stories/Backlog/Story-Usage-Event-And-Daily-Rollup.md) đã đặc tả đúng tình huống này: *"VLM-select thất bại/timeout **sau khi cả 3 candidate đã sinh** (tài nguyên đã tiêu) — `usage_event` của cả 3 candidate **vẫn được ghi** trước khi biết kết quả select"*.

⇒ Hành vi bắt buộc:

- Giữ **cả N candidate**, đẩy vào **hàng đợi review của người**, đánh dấu trạng thái tương đương `unclear`.
- ⛔ **Không** tự chọn candidate đầu tiên. ⛔ **Không** coi lỗi VLM là lỗi của cả job generation.
- `usage_event` của N candidate **đã** được ghi trước đó ⇒ ⛔ không rollback chúng.

### Q7. Ba đường ⛔ CẤM

| ⛔ | Vì sao | Neo |
|---|---|---|
| VLM **không** được dùng để tự chấm golden dataset thay người | `D-66`: *"⛔ Không dùng VLM tự chấm thay người"* — dataset regression là thứ dùng để **phát hiện** model drift, chấm nó bằng một model là mất điểm neo | [SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-NFR-19` |
| VLM **không** được tự áp dụng bản sửa | `D-38`: giữ cả hai version, **người chọn** | [SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-FR-21` |
| VLM **không** được dùng để phát hiện *"truyện này có thể có bản quyền của người khác"* | `D-53` — **ANTI-FEATURE**: nó tạo ra đúng tri thức mà điều kiện *"không biết"* của miễn trừ Điều 198b đang miễn trừ. ⚠️ Đây là chỗ *"một dev sẽ làm ngược theo bản năng"* | [SRS](../../020-Requirements/SRS-Comic-Studio.md) **`SRS-NFR-15`** |

### Q8. Một xung đột phải chuyển cho lô DB Schema — ⛔ ADR này không tự quyết

Chi phí VLM phải đo được, nhưng:

[Story-Usage-Event AC *"đúng 3 `usage_event` row"*](../../022-User-Stories/Backlog/Story-Usage-Event-And-Daily-Rollup.md) là AC đã ký: *"Một lần sinh panel bằng best-of-N (N=3) tạo ra **đúng 3** `usage_event` row, mỗi row ứng với 1 candidate — đo bằng: trigger sinh 1 panel, query **`COUNT(*)`** `usage_event` của panel đó **= 3**"*.

⇒ Nếu VLM call ghi thêm một `usage_event` row cho **cùng panel đó**, `COUNT(*)` thành **4** và **AC *"đúng 3 `usage_event` row"* FAIL**.

⚠️ Đây là mâu thuẫn thật giữa *"phải đo được chi phí VLM"* và *"đúng 3 row"*. **ADR này không giải** — nó là quyết định về mô hình dữ liệu.

- **Ai đóng**: Architect ở lô **DB Schema**, trong `DB-Entity-Usage-Event.md`.
- **Khi nào**: trước khi `DB-Entity-Usage-Event.md` được duyệt.
- Hướng cần cân nhắc (⛔ chưa chọn): thêm cột phân loại để `COUNT(*)` của AC lọc theo loại candidate · hoặc một bảng đo riêng cho VLM · hoặc sửa AC *"đúng 3 `usage_event` row"* (⇒ phải qua PM vì đó là artefact Phase 1 đã ký).
- ⛔ **Không** được giải bằng cách **không đo** chi phí VLM — đó chính là cách khoản chi phí này biến mất khỏi mô hình tài chính lần thứ hai.

---

## Alternatives considered

### (a) Gộp VLM vào adapter image provider (`D-40`) — ⛔ LOẠI

**Điểm hấp dẫn**: nếu vendor image và vendor VLM là một, gộp lại tiết kiệm một adapter, một bộ credential, một đường lỗi.

**⛔ Lý do loại**:

1. ⭐ **Gộp làm che khoản chi phí đang thiếu.** [findings §5 lưu ý #1](../../010-Planning/pm-runs/2026-08-28-phase-2-architecture-design-comic-studio/findings/architect.md): *"#2 tách khỏi #1 là **bắt buộc, không phải sở thích**"*. Chi phí VLM chỉ có cơ hội được tính nếu nó có một đường đo riêng.
2. **Hai vòng đời version.** Đổi model ảnh và đổi model chấm là hai sự kiện độc lập; gộp ⇒ một lần pin cho cả hai ⇒ mất khả năng quy trách nhiệm khi chất lượng đổi.
3. **Hai trạng thái lỗi khác nhau**: *"sinh xong nhưng chấm hỏng"* là trạng thái **hợp lệ** đã được đặc tả ([Story-Usage-Event AC *"VLM-select thất bại sau khi cả 3 candidate đã sinh"*](../../022-User-Stories/Backlog/Story-Usage-Event-And-Daily-Rollup.md)). Gộp adapter ⇒ dễ bị code thành *"cả job fail"*.
4. **Ràng buộc chọn vendor khác nhau**: tiêu chí #1 của [Q5](#q5-nhưng-chốt-được-ngay-tiêu-chí-chọn-theo-thứ-tự) (nhiều ảnh trong một call) không liên quan gì tới tiêu chí chọn provider sinh ảnh.

⇒ Kể cả khi hai vendor **trùng nhau**, hai adapter vẫn tách. Trùng vendor là một chi tiết cấu hình, không phải một sự thật kiến trúc.

### (b) Chọn luôn vendor VLM = vendor image provider mặc định — ⛔ LOẠI

`D-40` ghi provider ảnh mặc định (Gemini batch) với đường lui FLUX.2 ([SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-FR-23`). Kéo mặc định đó sang VLM nghe hợp lý.

**⛔ Loại**: `D-40` là quyết định về **provider sinh ảnh**, được ra bởi lập luận về **chất lượng ảnh và giá ảnh**. Suy nó sang VLM là **mở rộng phạm vi của một quyết định ra ngoài căn cứ của nó** — đúng loại thao tác mà [SRS](../../020-Requirements/SRS-Comic-Studio.md) §1.2 gọi là *"rửa sạch khoảng trống"*. Nếu sau đo đạc mà cùng vendor là lựa chọn tốt nhất, ADR này ghi nhận nó ở gate MVP0 **kèm số**, không phải bây giờ **kèm suy đoán**.

### (c) ⛔ Bỏ VLM, cho người chấm N candidate ngay từ MVP — LOẠI

**Điểm mạnh thật**: bỏ được một provider, một khoản chi phí chưa biết, một điểm lỗi. Và `D-38` vốn đã bắt **người chọn** ở đường continuity fix.

**⛔ Loại**: `D-37`/`D-38` **CHỐT** rằng Continuity Checker **là** QA-based selection giữa N candidate ([SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-FR-20`, `SRS-FR-21`). Bỏ VLM là **cắt cơ chế đã CHỐT** — ngoài thẩm quyền Phase 2. Ngoài ra `D-39` bắt hiện **độ phủ** *"đã kiểm N/M panel"* ([SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-FR-22`) — phát biểu này chỉ có nghĩa khi tồn tại một checker tự động.

### (d) Tự host model VLM mở — ⛔ LOẠI

`D-07` ([SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-NFR-11`): **⛔ Không mua GPU.** API cho main path; self-host **chỉ** cho LoRA train, upscale, inpainting. QA-select nằm trên main path ⇒ ⛔ không self-host.

### (e) Chốt luôn một vendor bây giờ để 27 file sau không phải chờ — ⛔ LOẠI

**⛔ Loại**: [Q2](#q2-hợp-đồng-của-adapter--chốt-hình-dạng-chưa-chốt-vendor) + [Q5](#q5-nhưng-chốt-được-ngay-tiêu-chí-chọn-theo-thứ-tự) đã đủ để viết `Spec-Integration-VLM-QA-Select.md` ở mức **seam** — chính là mức mà `D-40` chứng minh là đủ dùng cho image provider. ⇒ Không file nào bị chặn thật sự. Đổi lại, chốt vendor không căn cứ sẽ tạo ra một *"quyết định"* mà [SRS](../../020-Requirements/SRS-Comic-Studio.md) **§1.3** đã đẩy ra ngoài phạm vi của chính nó: *"Chọn giúp ở SRS làm tầng design **mất quyền quyết định thật** và tạo một *quyết định* **không ai chịu trách nhiệm**"*. ⚠️ Cùng câu đó, [SRS](../../020-Requirements/SRS-Comic-Studio.md) §1.3 nói rõ lựa chọn vendor *"**sẽ được đặc tả tại tầng 030-Specs**"* — tức **đúng tầng này**. ⇒ ADR-007 **không** né trách nhiệm: nó chốt seam + tiêu chí ngay, và đặt việc chốt tên vào **một gate có số đo** (MVP0) thay vì một suy đoán hôm nay.

---

## Consequences

### ⛔ Hệ quả BẮT BUỘC ĐỌC — chi phí và con số COGS

> [!WARNING]
> ⭐ **Chi phí VLM call để score N candidate là phần CHƯA TÍNH của `CF-3.5`** ([SRS](../../020-Requirements/SRS-Comic-Studio.md) §4.3 · §5.2).
>
> ⇒ **Mọi con số COGS hiện có trong repo — cụ thể `$12,06/chapter` @N=3 — là SÀN, KHÔNG PHẢI TRẦN** ([SRS](../../020-Requirements/SRS-Comic-Studio.md) `CẤM-04`).
>
> ⛔ **Không được đọc `$12,06` như chi phí thực tế đã đủ.** ⛔ Không được nhân nó ra để suy margin, giá bán, hay điểm hoà vốn mà không mang kèm nhãn *"sàn — chưa cộng VLM"*. Bỏ nhãn khi nhân một ước lượng là lỗi mà [SRS](../../020-Requirements/SRS-Comic-Studio.md) §1.2 gọi là **"rửa sạch khoảng trống"** ([findings §7 G7](../../010-Planning/pm-runs/2026-08-28-phase-2-architecture-design-comic-studio/findings/architect.md)).
>
> Con số đúng của khoản thiếu: **`TBD`**. ⛔ ADR này ⛔ **không** ước lượng nó. **Ai đóng**: PM + Architect, sau khi MVP0 đo. Đến lúc đó, mọi tài liệu Phase 2 phải mang nhãn *"sàn"*.

### Tích cực

- Chi phí VLM **có một đường riêng để được đo** — điều kiện cần để nó thôi biến mất khỏi mô hình tài chính. Đây là lý do tồn tại chính của ADR này, mạnh hơn cả việc chọn vendor.
- `Spec-Integration-VLM-QA-Select.md` viết được ngay ở mức seam, không chờ vendor.
- `unclear` được bảo vệ bằng hợp đồng interface ([Q2](#q2-hợp-đồng-của-adapter--chốt-hình-dạng-chưa-chốt-vendor)), không bằng lời nhắc trong prompt ⇒ khó bị bóp thành `fail` ở một lần refactor.
- Report-only mặc định ([Q3](#q3-chế-độ-mặc-định-khi-khởi-động-report-only)) ⇒ một VLM chấm kém **không** làm hỏng output trước khi cổng §5.1 chứng minh nó đủ tốt.
- Pin version + ghi `model_id`/`model_version` mọi lần chấm ⇒ silent model drift (`D-44`, `D-66`) có dấu vết để lần.

### Tiêu cực

- **Thêm một provider = thêm một điểm phụ thuộc ngoài**: một bộ credential, một hạn mức, một chính sách nội dung có thể từ chối (`D-67`), một bề mặt drift.
- **Một khoản chi phí chưa biết độ lớn nằm trên main path của mọi panel.** Nó nhân theo **N** và theo **số panel**, tức là nhân theo đúng hai đại lượng lớn nhất của mô hình chi phí.
- **Chưa chọn vendor ⇒ tiêu chí #1 của [Q5](#q5-nhưng-chốt-được-ngay-tiêu-chí-chọn-theo-thứ-tự) có thể làm hỏng giả định.** Nếu tất cả ứng viên đều **không** nhận nhiều ảnh trong một call, chi phí nhân N và bài toán đổi bản chất ⇒ phải quay lại `D-37` với PM. Đây là rủi ro **đã biết**, không phải rủi ro ẩn.
- **Độ phủ 40–60%** (`D-39`, [SRS](../../020-Requirements/SRS-Comic-Studio.md) §5.1, nhãn `[EM]`) phải **công bố cho user** — ⚠️ nó là **FR minh bạch**, ⛔ **không phải chỉ tiêu chất lượng để đạt**. Đọc ngược nó thành KPI là hiểu sai `D-39`.
- Mâu thuẫn `COUNT(*) = 3` ở [Q8](#q8-một-xung-đột-phải-chuyển-cho-lô-db-schema---adr-này-không-tự-quyết) là **nợ mở** — nếu lô Schema không xử lý, hoặc AC *"đúng 3 `usage_event` row"* FAIL, hoặc chi phí VLM lại không được đo.

### Việc còn để `TBD` — ⛔ không được bịa

| Việc | Ai đóng | Khi nào |
|---|---|:--|
| **Tên provider VLM** | PM + Architect | Gate cuối MVP0, khi có số đo |
| **Chi phí VLM per-call** và tổng khoản thiếu của `CF-3.5` | PM + Architect | Sau đo MVP0 |
| **N tối thiểu** (`CF-8.5`, [SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-FR-20`) — ⚠️ budget vẫn phải tính ở **N=3** | PM | Sau đo MVP0 |
| **Human-reject rate sau VLM-select** ([SRS](../../020-Requirements/SRS-Comic-Studio.md) §5.2: *"chưa ai công bố con số này"*) | Engineer đo, PM đọc | MVP0 |
| Mô hình đo chi phí VLM vs AC `COUNT(*) = 3` ([Q8](#q8-một-xung-đột-phải-chuyển-cho-lô-db-schema---adr-này-không-tự-quyết)) | Architect (lô DB Schema) | Trước khi `DB-Entity-Usage-Event.md` duyệt |
| Bộ câu hỏi kiểm tra cụ thể của checker + cổng precision cho **từng** check | Architect + Engineer | Trước khi bật check đầu tiên, theo [SRS](../../020-Requirements/SRS-Comic-Studio.md) §5.1 |

---

## Đã quyết ở đâu

| Quyết định | Mã `D-xx` | Nguồn (file + mã requirement) |
|---|:--:|---|
| **best-of-N** cho MỌI panel rồi VLM QA-select 1; ⛔ không phải retry-on-failure; N mặc định **3** | `D-37` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-FR-20` |
| Continuity Checker = QA-based selection; output là hàng đợi xếp hạng; giữ cả hai version, **người chọn**; **`unclear` hợp lệ hạng nhất** | `D-38` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-FR-21` |
| Phải hiện **độ phủ** checker cho user — FR minh bạch, ⛔ không phải chỉ tiêu chất lượng | `D-39` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-FR-22` · §5.1 |
| **Adapter per image provider** + pin model version (mẫu áp dụng cho VLM) | `D-40` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-FR-23` |
| Batch API, ⛔ không realtime (áp cho **image**) | `D-41` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-FR-24` |
| ⛔ **Không LLM/VLM ở compiler runtime** | `D-34` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-FR-17` |
| ⛔ **Không mua GPU**; API cho main path | `D-07` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-NFR-11` |
| Mục tiêu bảng `Generation` là **auditability + lineage**, ⛔ không phải reproducibility; `seed` là provenance | `D-44` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) **§3.A** (khối `[!CAUTION]`) |
| `cost_usd` + `model_id` + `model_version` + `attempt_no` trên **MỌI** generation | `D-59` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-FR-31` |
| Golden dataset regression 15–20 panel; ⛔ **không dùng VLM tự chấm thay người** | `D-66` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) **`SRS-NFR-19`** · §5.1 |
| Ghi lại **mọi** lần provider từ chối vì content policy | `D-67` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) **`SRS-NFR-20`** |
| ⛔ **ANTI-FEATURE**: không có bộ phát hiện bản quyền/plagiarism trước khi luật sư xác nhận | `D-53` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) **`SRS-NFR-15`** |
| `usage_event` append-only; **một lần best-of-N (N=3) ⇒ đúng 3 row** | `D-58` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-FR-30` · [Story-Usage-Event-And-Daily-Rollup](../../022-User-Stories/Backlog/Story-Usage-Event-And-Daily-Rollup.md) **AC *"đúng 3 `usage_event` row"***, **AC *"VLM-select thất bại sau khi cả 3 candidate đã sinh"*** |
| Cổng chất lượng: **precision ≥ ~0.7 trên ≥100 panel dán nhãn tay** trước khi bật một check nào (`[EM]`) | — | [SRS](../../020-Requirements/SRS-Comic-Studio.md) §5.1 |
| **COGS sàn `$12,06`/chapter là SÀN, ⛔ không phải trần** (`CẤM-04`) | — | [SRS](../../020-Requirements/SRS-Comic-Studio.md) `CẤM-04` |
| ⛔ Chi phí VLM là phần **CHƯA TÍNH** của `CF-3.5` | — | [SRS](../../020-Requirements/SRS-Comic-Studio.md) §4.3 · §5.2 |
| ⛔ Không tự gán số cho hàng `TBD` | — | [SRS](../../020-Requirements/SRS-Comic-Studio.md) §5.2 |
| ⛔ **CHƯA quyết ở Phase 1**: provider VLM | — | [findings/architect §5 hàng #2](../../010-Planning/pm-runs/2026-08-28-phase-2-architecture-design-comic-studio/findings/architect.md) |
