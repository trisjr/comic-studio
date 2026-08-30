---
id: SPEC-INT-LLM-PROVIDER
type: spec
status: draft
project: comic-studio
created: 2026-08-29
---

# Spec-Integration-LLM-Provider — adapter LLM và ranh giới sử dụng

Related to: [ADR-008](../Architecture/ADR-008-LLM-Provider-And-Usage-Boundaries.md) · [ADR-014](../Architecture/ADR-014-Deterministic-Prompt-Compiler-And-Best-Of-N.md) · [ADR-015](../Architecture/ADR-015-Job-Queue-In-Postgres.md) · [ADR-017](../Architecture/ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md) · [SDD](../Architecture/SDD-Comic-Studio.md)

> [!IMPORTANT]
> ⭐ **Giá trị lớn nhất của file này ⛔ KHÔNG phải phần chọn provider** — mà là **năm ranh giới sử dụng đã CHỐT** ở [§2](#2-cái-gì-đã-chốt), biến thành **hợp đồng interface cưỡng chế được** thay vì lời nhắc trong prompt.

---

## 1. Mục đích

File này đóng phần `P-8` của [SDD §9.2](../Architecture/SDD-Comic-Studio.md) — *"retry / backoff policy + error taxonomy per provider"* — cho **đường gọi LLM**, và đặc tả hợp đồng adapter mà [ADR-008](../Architecture/ADR-008-LLM-Provider-And-Usage-Boundaries.md) `Q1`–`Q5` để lại cho tầng này.

Ba việc file này làm:

1. Biến **năm ranh giới CHỐT** (`D-16`, `D-34`, `D-36`, `D-26`, `D-23`) thành **ràng buộc của interface**, kèm cơ chế cưỡng chế.
2. **Phân loại lỗi LLM** thành đúng năm lớp của [ADR-015](../Architecture/ADR-015-Job-Queue-In-Postgres.md) `Q5`.
3. Nói **trung thực** về chi phí LLM: [ADR-008](../Architecture/ADR-008-LLM-Provider-And-Usage-Boundaries.md) tuyên bố nó là *"chưa xác định"* và ⛔ **không route về `usage_event`** ⇒ ⛔ **file này KHÔNG phát minh một mô hình đếm chi phí LLM.**

⛔ **File này ⛔ KHÔNG chọn vendor, ⛔ không viết nội dung 5 prompt template, ⛔ không đặc tả DDL.**

---

## 2. Cái gì đã CHỐT

### 2.1 Năm việc — và CHỈ năm việc — được dùng LLM

| # | Việc | Module | Ranh giới đã CHỐT | Mã |
|--:|---|:--:|---|:--:|
| 1 | **Extraction** — phát `event` cho Story Bible | `M2` | LLM chỉ phát **event** (`entity, attribute, value, permanence, evidence_span, confidence`) cho **MỘT chapter**; ⭐ **CODE SỞ HỮU STATE** | `D-16` · `SRS-FR-05` |
| 2 | **Speaker proposal** — đề xuất người nói | `M4` | LLM bị **CONSTRAINED** vào tập nhân vật **có mặt trong scene**; ⭐ **`UNKNOWN` là giá trị HỢP LỆ**; anchor **regex chạy TRƯỚC** LLM; lưu `speaker_confidence` | `D-26` · `SRS-FR-14` |
| 3 | **Condensation** — nén thoại theo `text_budget` | `M4` | Là **human gate #2**, ⛔ không tuỳ chọn; chạy **SAU layout** vì `text_budget` phụ thuộc diện tích panel | `D-26`, `D-27` · `SRS-FR-14`, `SRS-FR-15` |
| 4 | **Beat ranking** — xếp hạng beat trong chapter | `M3` | ⭐ LLM **CHỈ XẾP HẠNG**; **CODE PHÂN BỔ** theo emphasis quota; `dialogue_density` và `character_count` **do CODE đếm** | `D-23` · `SRS-FR-09` |
| 5 | **Offline vocabulary** — soạn từ vựng `field value → cụm từ` | `M5` | **Offline một lần** → **NGƯỜI REVIEW** → **lưu vào bảng**. Là **DỮ LIỆU**, ⛔ **không phải runtime** | `D-36` · `SRS-FR-19` |

⚠️ **Ranh giới upstream cũng đã chốt**: `D-18` — **chapter parse + text clean là bước ĐẦU TIÊN** của pipeline và là **code deterministic** (regex/heuristic), ⛔ **không LLM** (`SRS-FR-06`).

### 2.2 Năm ranh giới — ⛔ ⛔ KHÔNG mở lại

| # | Ranh giới | Mã | Nguồn |
|:--:|---|:--:|---|
| **(a)** | LLM **chỉ phát event**, ⭐ **code sở hữu state**. `state_at(N) = reduce(events where story_order <= N)` là **HÀM THUẦN** | `D-16` | `SRS-FR-05` |
| **(b)** | ⛔⛔ **KHÔNG có LLM ở Visual Prompt Compiler RUNTIME.** Compiler là **code deterministic**: tra bảng, sắp thứ tự, dedup, precedence ladder, constraint budget, drop log | `D-34` | `SRS-FR-17` |
| **(c)** | LLM xuất hiện trong compiler ở **ĐÚNG HAI CHỖ HẸP**, và **PHẢI CACHE**: (i) từ vựng offline → **bảng**; (ii) dịch action tự do → cụm pose khi từ vựng chưa có entry, **cache theo hash của action text**. *"Ngoài hai việc đó: không có LLM trong compiler"* | `D-36` | `SRS-FR-19` |
| **(d)** | LLM **constrained** vào nhân vật có mặt trong scene; **`UNKNOWN` hợp lệ**; ⛔ **không tồn tại đường code nào bypass hai human gate — KỂ CẢ CỜ CẤU HÌNH** | `D-26` | `SRS-FR-14` |
| **(e)** | LLM **chỉ xếp hạng** beat; ⭐ **code phân bổ quota** emphasis theo phạm vi chapter | `D-23` | `SRS-FR-09` |

### 2.3 Seam và versioning

| # | Nội dung | Mã |
|--:|---|:--:|
| `LP-C1` | **MỘT interface `LlmProvider`** — một seam duy nhất, đổi provider ⛔ không đổi code gọi (mẫu `D-40`) | `D-40` · `SRS-FR-23` |
| `LP-C2` | ⭐ **NĂM task profile RIÊNG**: mỗi việc có **prompt template riêng · version riêng · schema output riêng · cấu hình model riêng**. ⛔ **Không dùng chung một prompt cho nhiều việc** | [ADR-008](../Architecture/ADR-008-LLM-Provider-And-Usage-Boundaries.md) `Q1` |
| `LP-C3` | Đổi provider **cho RIÊNG một việc** phải làm được mà ⛔ không chạm bốn việc còn lại | [ADR-008](../Architecture/ADR-008-LLM-Provider-And-Usage-Boundaries.md) `Q1` |
| `LP-C4` | Output phải **STRUCTURED / CONSTRAINED**, ⛔ **không phải văn xuôi tự do** | [ADR-008](../Architecture/ADR-008-LLM-Provider-And-Usage-Boundaries.md) `Q2` |
| `LP-C5` | ⭐ Ghi **CÙNG LÚC BỐN trường** với mọi output: **`prompt_template_id` · `prompt_version` · `model_id` · `model_version`** | [ADR-008](../Architecture/ADR-008-LLM-Provider-And-Usage-Boundaries.md) `Q3` |
| `LP-C6` | ⭐ Adapter trả về **THEO FIELD**, ⛔ không trả một khối text rồi để tầng gọi tự bóc | `D-49` · `SRS-FR-36` |
| `LP-C7` | ⭐ **Lời gọi LLM phải HOÀN TẤT TRƯỚC khi mở transaction ghi.** ⛔ Không giữ transaction mở trong lúc chờ mạng | `D-50` · `SRS-NFR-13` (`KC-4`) |
| `LP-C8` | ⛔ **Không mua GPU** — cả năm việc đều nằm trên main path | `D-07` · `SRS-NFR-11` |
| `LP-C9` | Ghi lại **MỌI** lần provider từ chối vì content policy | `D-67` · `SRS-NFR-20` |

> [!WARNING]
> ⚠️ **`LP-C5` — bốn trường này ⛔ KHÔNG BACKFILL ĐƯỢC** (`D-59`). Chúng phải có từ **bản ghi ĐẦU TIÊN**, ⛔ không phải một hàng backlog.
> ⛔ Không có bốn trường này thì khi chất lượng đổi, ⛔ **không phân biệt được** *"đổi model"* với *"đổi prompt"* với *"đổi dữ liệu đầu vào"*.

### 2.4 Cache — ⛔ đúng hai chỗ, và ⛔ KHÔNG phải chiến lược chi phí

- **Hai chỗ duy nhất** có cache LLM trong compiler (`D-36`): (i) từ vựng offline → **bảng**; (ii) action tự do → cụm pose, **cache theo hash của action text**.
- ⛔ **Ngoài hai chỗ đó, ⛔ không có cache LLM trong compiler.**
- ⭐ **Bốn việc còn lại (extraction, speaker, condensation, beat ranking) ⛔ KHÔNG nằm trong compiler** ⇒ `D-36` ⛔ **không cấp phép cache** cho chúng.

> [!CAUTION]
> ⛔⛔ **ĐỪNG DỰA VÀO CACHE ĐỂ CỨU MARGIN** (`D-64`, `SRS-NFR-12`).
> Hai chỗ ra tiền thật là **reference-sheet amortization** và **idempotency**. Cache ở đây tồn tại để giữ compiler **deterministic và ổn định**, ⛔ **không phải** để giảm hoá đơn. Đọc ngược là hiểu sai `D-36` **và** `D-64` cùng lúc.
> ⚠️ Thêm nữa: bốn việc kia đứng **TRƯỚC** hai human gate — cache một đề xuất **đã bị người sửa** là cách làm hỏng `D-28` (edit của người phải **KHOÁ LẠI** khỏi bị re-run ghi đè, `SRS-FR-12`).

### 2.5 Bốn đường ⛔ CẤM — mỗi đường một guardrail cưỡng chế được

| ⛔ Cấm | Neo | Cưỡng chế bằng |
|---|---|---|
| **Import LLM adapter từ module compiler** (`M5` — Visual Prompt Compiler) | `D-34` · `SRS-FR-17` | ⭐ **Lint rule ở CI** (mẫu `D-04`, `SRS-NFR-04`): compiler ⛔ không được import `LlmProvider`. Hai chỗ hẹp của `D-36` **đọc BẢNG đã cache**, ⛔ không gọi provider |
| **Ghi state trực tiếp từ output LLM** | `D-16` · `D-17` · `SRS-FR-05`, `SRS-NFR-10` | Test guardrail: state **chỉ** đến từ `resolveState()` — `D-17` bắt có **ĐÚNG MỘT** hàm; cộng test *"⛔ không có `ORDER BY chapter_no` trong bất kỳ đường resolve state nào"* |
| **Cờ cấu hình bypass hai human gate** | `D-26` · `SRS-FR-14` | Test: ⛔ **không tồn tại** tham số/cờ nào cho phép chuyển một page sang trạng thái xuất bản khi gate còn `OPEN` |
| ⭐ Dùng LLM phát hiện *"truyện này có thể có bản quyền của người khác"* (copyright / plagiarism / similarity) | `D-53` · **`SRS-NFR-15`** | ⚠️ **PROMPT REVIEW**: ⛔ **không prompt nào của 5 task profile** được chứa câu hỏi loại đó. ⭐ Lý do: nó tạo ra **đúng tri thức** mà điều kiện *"không biết"* của miễn trừ **Điều 198b** đang miễn trừ ⇒ **tự phá miễn trừ**. Đây là chỗ *"một dev sẽ làm ngược theo bản năng"* |

---

## 3. Cái gì còn MỞ

⛔ **File này ⛔ KHÔNG chọn vendor**: [SRS](../../020-Requirements/SRS-Comic-Studio.md) §5.2 cấm tự gán số, và các biến quyết định (chi phí per-token cho 5 việc, chất lượng extraction trên văn bản tiếng Việt dài) ⛔ **chưa có phép đo nào trong repo**.

| Mã | `TBD` | Ai đóng | Khi nào |
|---|---|---|---|
| `LP-T1` | ⭐ **Tên provider LLM** | **Architect + PM** | Sau MVP0/MVP1, dựa trên **eval kit của `D-65`** (`SRS-NFR-18` bắt HITL gate + eval kit **ngay tại MVP1** và **log preference data từ MVP1** ⇒ cơ chế sinh dữ liệu để quyết đã có sẵn) |
| `LP-T2` | ⭐ **Chi phí LLM per chapter** cho 5 việc — xem [§6](#6-chi-phí) | **PM** | Khi cập nhật mô hình tài chính sau MVP0 |
| `LP-T3` | **Ánh xạ mã lỗi thô của provider → năm lớp lỗi**. ⛔ Không viết được trước khi `LP-T1` đóng | **Engineer** | Sau `LP-T1`, khi viết adapter |
| `LP-T4` | **Ngưỡng rate limit** / giới hạn upload đi kèm `D-67` | **PM + Architect** | Sau đo tải |
| `LP-T5` | **Nội dung cụ thể của 5 prompt template** + rubric `beat_type` (enum + anchor example của `D-23`) | **Architect + Engineer** | Lô Spec chi tiết của `M2` / `M3` / `M4` (hàng `P-10`) |
| `LP-T6` | **Có cache cho 4 việc ngoài compiler hay không** | **Architect** | ⭐ **Chỉ mở khi có số đo**; ⚠️ phải cân với `D-28` (khoá edit của người) |
| `LP-T7` | ⭐ **Cơ chế đo chi phí LLM** — hiện ⛔ **không có bảng nào** giữ khoản này | **PM (quyết có đo hay không)** rồi **Architect (lô Schema)** nếu có | Sau MVP0 — xem [§6.3](#63--vì-sao-file-này--không-tự-thiết-kế-mô-hình-đếm-chi-phí-llm) và [RIPPLE](#7-ripple--những-gì-file-này--không-tự-sửa-được) |

### 3.1 Tiêu chí chọn vendor — CHỐT ngay, theo đúng thứ tự

| # | Tiêu chí | Loại | Neo |
|--:|---|:--:|---|
| **1** | ⭐ **Constrained / structured output** — ép được **tập giá trị đóng** và schema | ⛔ **LOẠI** | Điều kiện **cần** của `D-16`, `D-26`, `D-23`. ⛔ Không đạt ⇒ loại, ⛔ **không bù được bằng prompt** |
| **2** | **Version pinning tường minh** | ⛔ **LOẠI** | `D-40` + `LP-C5`; phòng **silent model drift** |
| **3** | **Cửa sổ ngữ cảnh đủ cho MỘT CHAPTER** | ⛔ **LOẠI** | `D-16` phát event cho **một chapter** ⇒ ⭐ **chapter là đơn vị ngữ cảnh**, ⛔ không phải đoạn |
| **4** | **Chất lượng tiếng Việt** | cộng điểm | ⚠️ **Suy luận, ⛔ không phải quyết định Phase 1**: `D-30` bắt wrap tiếng Việt hiểu **Unicode combining marks** (`SRS-FR-16`) ⇒ locale mục tiêu là tiếng Việt. ⛔ Không tài liệu nào phát biểu tiêu chí này tường minh |
| **5** | **Batch / async** | ⚠️ mong muốn | Pipeline vốn async (`D-03`); ⛔ **không phải CHỐT** — `D-41` chỉ chốt batch cho **image** |
| **6** | **Chi phí per-token** | cộng điểm | Chỉ so được **sau khi (1) và (3) đã lọc** |

> [!WARNING]
> ⚠️ **Rủi ro ĐÃ BIẾT**: nếu ứng viên tốt nhất về **chất lượng tiếng Việt** lại **yếu về structured output** ⇒ ⛔ **không được bù bằng prompt** — phải **quay lại PM**. Tiêu chí #1 là tiêu chí **loại**, ⛔ không phải tiêu chí cộng điểm.

---

## 4. Interface / seam

### 4.1 Một interface, năm task profile

```
LlmProvider.invoke(task_profile, input, tenant_credential) -> LlmResult
```

| Thành phần của một `task_profile` | Ràng buộc |
|---|---|
| `prompt_template_id` | Định danh template của **riêng** việc đó (`LP-C2`) |
| `prompt_version` | Chuỗi version **độc lập** với bốn việc kia |
| `output_schema` | Schema đóng của **riêng** việc đó — xem [§4.2](#42-năm-schema-output-bắt-buộc) |
| `model_id` · `model_version` | Pin tường minh; ⛔ đổi cho **riêng một việc** phải làm được (`LP-C3`) |
| ⭐ `tenant_credential` | ⭐ Nhận **THEO TENANT ở chữ ký hàm**, ⛔ không đọc thẳng biến môi trường toàn cục — cùng khuôn seam `S-4` |

⛔ **Không dùng chung một prompt cho nhiều việc.** Năm việc có **năm tập giá trị đầu ra đóng khác nhau**; gộp prompt là cách nhanh nhất để một ràng buộc của việc này **rò sang** việc kia — và một prompt chung ⇒ **một version chung** ⇒ sửa prompt cho beat ranking làm **đổi hành vi extraction mà ⛔ không ai biết**.

### 4.2 Năm schema output bắt buộc

| Việc | Đầu ra bắt buộc | Vì sao ràng buộc này ⛔ không thương lượng |
|---|---|---|
| **Extraction** | Danh sách `event` **đúng schema `D-16`** | `state_at(N)` là **hàm thuần** trên event; một field lệch schema ⇒ **state sai ÂM THẦM** |
| **Speaker proposal** | Giá trị thuộc **TẬP ĐÓNG** = {nhân vật có mặt trong scene} ∪ {`UNKNOWN`} | `D-26`. ⛔ Nếu output tự do, model sẽ **BỊA TÊN NHÂN VẬT** — đúng thứ constraint tồn tại để chặn |
| **Condensation** | Text + **độ dài đo được** so `text_budget` | `D-27`: `text_budget` là ràng buộc **từ layout đi ngược vào** |
| **Beat ranking** | **THỨ HẠNG** beat | `D-23`. ⛔ Output ⛔ **không được chứa** quyết định panel size / full-page — đó là việc của **code** |
| **Offline vocabulary** | Cặp `field value → cụm từ` để **NGƯỜI REVIEW** rồi ghi bảng | `D-36`: là **DỮ LIỆU**, ⛔ không phải runtime |

⭐ **`UNKNOWN` ở việc #2 là giá trị HỢP LỆ**, ⛔ không phải lỗi, ⛔ không phải `NULL` — cùng hạng với `unclear` của đường VLM.

### 4.3 ⭐ Trả về THEO FIELD — điều kiện của `field_provenance`

`D-49` (`SRS-FR-36`) bắt provenance ở **MỨC FIELD**: field nào do LLM rút, field nào người khai/sửa.

⇒ ⭐ **Adapter phải trả về theo field.** ⛔ Trả một khối text rồi để tầng gọi tự bóc ⇒ `field_provenance` chỉ ghi được *"cả cụm này do AI"* — **mất đúng độ hạt** mà `KC-3` yêu cầu.

Mỗi field trả về mang kèm bốn trường của `LP-C5` (`prompt_template_id`, `prompt_version`, `model_id`, `model_version`).

### 4.4 ⭐ Ranh giới transaction — `KC-4`

> ⭐ **Lời gọi LLM phải HOÀN TẤT TRƯỚC khi mở transaction ghi** (`LP-C7`).

Lý do: `KC-4` (`D-50`, `SRS-NFR-13`) bắt bản ghi `field_provenance` commit **CÙNG MỘT TRANSACTION** với artifact. ⛔ Giữ transaction mở trong lúc chờ mạng là hỏng cả hai ràng buộc cùng lúc.

⇒ **Hai hệ quả bắt buộc xử lý tường minh:**

1. Trạng thái *"đã gọi xong nhưng chưa ghi"* là trạng thái **THẬT** — luồng code dài hơn *"gọi và ghi trong một hàm"*.
2. ⭐ **Một lỗi transient xảy ra ở bước ghi ⇒ ⛔ KHÔNG để lại artifact bán phần**: transaction rollback, và output LLM đã trả về **hoặc được giữ lại để ghi lại, hoặc lời gọi phải lặp** — đó là chi phí thật của retry ở đường này.

### 4.5 ⛔ Ranh giới với compiler — seam phải nhìn thấy được

| Ai gọi `LlmProvider` | Ai ⛔ KHÔNG được gọi |
|---|---|
| `M2` (extraction) · `M3` (beat ranking) · `M4` (speaker, condensation) | ⛔⛔ **`M5` — Visual Prompt Compiler**, ở **runtime** |
| Công cụ **offline** soạn từ vựng (việc #5) — chạy ngoài luồng runtime | ⛔ Bất kỳ đường nào nằm trong lời gọi compile của một panel |

⭐ **Hai chỗ hẹp của `D-36` ĐỌC BẢNG ĐÃ CACHE, ⛔ KHÔNG GỌI PROVIDER.** Đây là điểm dễ hiểu sai nhất của toàn bộ file: `D-36` cấp phép cho **dữ liệu** đến từ LLM, ⛔ **không** cấp phép cho **lời gọi** LLM ở runtime compiler.

⇒ Cưỡng chế: **lint rule ở CI** cấm module compiler import `LlmProvider` ([§2.5](#25-bốn-đường--cấm--mỗi-đường-một-guardrail-cưỡng-chế-được)).

---

## 5. Retry & error taxonomy

### 5.1 Đường phân chia trách nhiệm

> ⭐ **Adapter PHÂN LOẠI lỗi. Job queue QUYẾT ĐỊNH làm gì với lớp đó** — cùng đường phân chia với hai integration kia ([ADR-015](../Architecture/ADR-015-Job-Queue-In-Postgres.md) `Q7`).

### 5.2 Năm lớp lỗi — danh sách đóng

| `error_class` | Quy tắc phân loại **ở đường LLM** | Hệ quả |
|---|---|:--|
| `transient_infra` | Lỗi **trước khi** request rời tiến trình; DB timeout / deadlock ở bước ghi **sau** khi đã gọi | ✅ Retry + backoff |
| `transient_provider` | LLM **timeout**, **rate limit**, lỗi tạm thời phía provider | ✅ Retry + backoff |
| `permanent_input` | ⭐ **Input vượt cửa sổ ngữ cảnh** (chapter quá dài — tiêu chí #3 của [§3.1](#31-tiêu-chí-chọn-vendor--chốt-ngay-theo-đúng-thứ-tự) tồn tại để chặn); payload sai; `model_id`/`model_version` ⛔ không tồn tại | ⛔ Không retry ⇒ `failed_permanent` |
| ⭐ `permanent_policy` | LLM **từ chối vì content policy** | ⛔ Không retry. ⭐ **BẮT BUỘC ghi `generation.provider_refusal_log`** với `provider_kind = 'llm'` — xem [§5.4](#54-permanent_policy--nghĩa-vụ-ghi-nhật-ký-d-67) |
| `permanent_unknown` | ⛔ Chưa phân loại được | ⛔ Không retry; ⚠️ **phải xuất hiện trong chẩn đoán**, ⛔ không im lặng |

⛔ **File này KHÔNG liệt kê mã lỗi thô của một provider cụ thể** — `LP-T1` chưa đóng thì ⛔ không có provider nào để tra mã. Hàng `LP-T3`.

### 5.3 ⭐ Lỗi SCHEMA của output — một lớp riêng phải xử lý tường minh

⚠️ **Output không parse được / không khớp `output_schema` ⛔ KHÔNG phải một lỗi mạng, và ⛔ KHÔNG được nuốt.**

| Tình huống | Xử lý bắt buộc |
|---|---|
| Output ⛔ không khớp schema đóng | ⛔ **KHÔNG "sửa mềm"**, ⛔ không đoán ý, ⛔ không rơi về văn xuôi tự do |
| Speaker proposal trả một tên **ngoài** tập nhân vật có mặt trong scene | ⭐ **Từ chối giá trị đó** — ⛔ không ghi vào state. `UNKNOWN` là đường đúng, ⛔ không phải *"chọn cái gần đúng nhất"* |
| Beat ranking trả kèm quyết định panel size | ⭐ **Bỏ phần vượt ranh giới** — `D-23` chốt code phân bổ quota, ⛔ không phải LLM |

⚠️ **Phân loại**: lỗi schema **lặp lại có hệ thống** là dấu hiệu tiêu chí #1 (constrained output) ⛔ không được thoả ⇒ đó là **tín hiệu phải quay lại PM**, ⛔ không phải một hàng retry.

### 5.4 `permanent_policy` — nghĩa vụ ghi nhật ký (`D-67`)

`D-67` (`SRS-NFR-20`) áp cho **cả ba** đường gọi ngoài. Đích ghi: **`generation.provider_refusal_log`** với `provider_kind = 'llm'`, `error_class = 'permanent_policy'`, `provider_error_code` **thô** (⛔ giữ nguyên, không diễn giải lại), `refusal_reason` chuẩn hoá (⛔ không nêu được ⇒ `unspecified_by_provider`).

⚠️ **`model_version` ở đường LLM**: bảng cho phép `NULL` vì ⛔ *"đường LLM chưa có ADR nào bắt pin"* ở tầng requirement — ⭐ **nhưng `LP-C5` của file này BẮT ghi bốn trường version với mọi output** ⇒ ⛔ **adapter LLM ⛔ không được để `NULL`**. Đây là ràng buộc **chặt hơn** schema, ⛔ không mâu thuẫn với nó.

⛔ **Không ghi nội dung người dùng thô** vào bảng này — ⛔ không prompt đã gửi, ⛔ không đoạn văn nguồn, ⛔ không tên nhân vật (`QA-10`).

### 5.5 Backoff

⛔ File này ⛔ không đặt lại policy. Backoff **luỹ thừa có jitter** qua `run_after`, `max_attempts` mặc định **5** (`[EM]` — ⛔ **không phải chỉ tiêu NFR**) — [ADR-015](../Architecture/ADR-015-Job-Queue-In-Postgres.md) `Q4`.

⚠️ **Đặc thù đường LLM**: retry một lời gọi LLM **có chi phí thật**, nhưng ⛔ **chưa có bảng nào đếm nó** ([§6](#6-chi-phí)) ⇒ số lần retry ở đường này hiện ⛔ **không quan sát được bằng dữ liệu chi phí**. Đây là lỗ **đã biết**, ⛔ không phải sơ suất — hàng `LP-T7`.

---

## 6. Chi phí

### 6.1 ⭐ Trạng thái trung thực — ⛔ không được suy diễn

> [!CAUTION]
> ⭐⭐ **Repo chỉ tuyên bố TƯỜNG MINH rằng khoản chi phí VLM là phần CHƯA TÍNH của `CF-3.5`.**
>
> ⛔ **Với chi phí LLM cho 5 việc, ⛔ KHÔNG có dòng nào trong repo xác nhận nó đã được tính hay chưa.**
> ⇒ ⭐ **Đối xử như CHƯA XÁC ĐỊNH.** ⛔ **Không cộng, ⛔ không trừ, ⛔ không suy** nó vào con số `$12,06`/chapter.
>
> `$12,06`/chapter @N=3 là **SÀN, ⛔ KHÔNG phải trần** (`CẤM-04`). Bỏ nhãn khi nhân một ước lượng là lỗi mà [SRS](../../020-Requirements/SRS-Comic-Studio.md) §1.2 gọi là **"rửa sạch khoảng trống"**.
>
> **Ai đóng**: **PM**, khi mô hình tài chính được cập nhật sau MVP0 (`LP-T2`).

⚠️ **Một dữ kiện phải nói ra vì nó chi phối độ lớn**: `D-16` bắt **đơn vị ngữ cảnh là MỘT CHAPTER** ⇒ mỗi lời gọi extraction mang **cả chapter**. Chi phí per-call theo **độ dài chapter** — ⛔ **không có số nào trong repo** để ước lượng.

### 6.2 ⭐ Chi phí LLM hiện ⛔ KHÔNG được đo ở đâu cả

| Bảng | Có giữ chi phí LLM không | Vì sao |
|---|:--:|---|
| `public.usage_event` | ⛔ **KHÔNG** | ⭐ Bảng **ĐỒNG NHẤT**: một dòng = **một image candidate**. ⛔ Không cột phân loại, ⛔ không dòng nào không ứng với một candidate (`E20`). ⭐ Cột `event_kind` **đã bị BỎ**, và việc bỏ đó **đã được VERIFY** chính bằng lý do *"chi phí LLM ⛔ không route về `usage_event`"* |
| `generation.generation` | ⛔ **KHÔNG** | `cost_usd` ở đó là chi phí **sinh ảnh** của một candidate |
| `generation.vlm_scoring_call` | ⛔ **KHÔNG** | Một dòng = **một lời gọi VLM** |
| ⭐ **Chưa bảng nào** | — | ⭐ **Đây là phát biểu trung thực về trạng thái hiện tại, ⛔ không phải một lỗ hổng bị bỏ quên** |

> [!WARNING]
> ⛔⛔ **Adapter LLM ⛔ TUYỆT ĐỐI KHÔNG được ghi một dòng nào vào `public.usage_event`.**
> AC đã ký đo bằng `COUNT(*)` **TRẦN** trên `usage_event` của một panel = **3**. Thêm bất kỳ dòng nào khác ⇒ **AC FAIL** và phép cộng COGS **đếm đôi**.
> `CHECK (cost_state = 'carried_by_generation')` làm việc thêm đó **thất bại ồn ào** ở migration — ⛔ đó là guardrail, ⛔ không phải cột thừa.

### 6.3 ⭐ Vì sao file này ⛔ KHÔNG tự thiết kế mô hình đếm chi phí LLM

Ba lý do, xếp theo độ nặng:

1. ⭐ **Ngoài thẩm quyền.** Một bảng kiểu `llm_call` là **quyết định về MÔ HÌNH DỮ LIỆU** — thuộc **lô DB Schema**, ⛔ không thuộc lô API. `Schema/` hiện **đã đóng**. Tiền lệ đúng khuôn: [ADR-007](../Architecture/ADR-007-VLM-Provider-For-QA-Select.md) `Q8` **cũng ⛔ không tự giải** mâu thuẫn `COUNT(*) = 3` mà **chuyển cho lô Schema** — và lô đó đã đóng nó bằng `generation.vlm_scoring_call`.
2. ⭐ **Chưa có ai yêu cầu đo.** Khoản VLM có một **tuyên bố tường minh** rằng nó là phần chưa tính ⇒ có nghĩa vụ đo. Khoản LLM ⛔ **không có tuyên bố nào** ⇒ ⛔ **không được suy ra nghĩa vụ**, cũng ⛔ không được suy ra là không cần. **PM phải quyết trước** (`LP-T7`).
3. **Thêm một bảng "cho chắc" là vi phạm quy tắc** *"⛔ không cột nào vào vì chắc là cần"* mà tầng Schema đang giữ.

⚠️ ⇒ Hàng `LP-T7` là một **RIPPLE thật**, ⛔ không phải một `TBD` trang trí. Xem [§7](#7-ripple--những-gì-file-này--không-tự-sửa-được).

### 6.4 ⛔ Cái gì vẫn CHƯA đo được ở đường này

| Khoản | Vì sao | Ai đóng | Khi nào |
|---|---|---|---|
| ⭐ **Chi phí LLM per chapter** cho 5 việc (`LP-T2`) | ⛔ Không có số; đơn vị ngữ cảnh là **cả chapter** | **PM** | Khi cập nhật mô hình tài chính sau MVP0 |
| ⭐ **Có đo chi phí LLM hay không, và bằng cơ chế gì** (`LP-T7`) | ⛔ Chưa bảng nào giữ; ⛔ ngoài thẩm quyền lô này | **PM** quyết → **Architect** (lô Schema) hiện thực | Sau MVP0 |
| **Chi phí retry ở đường LLM** | Hệ quả trực tiếp của `LP-T7` | như trên | như trên |
| ⭐ **Chi phí VLM per-call** | ⛔ Không thuộc file này | PM + Architect | [Spec-Integration-VLM-QA-Select](./Spec-Integration-VLM-QA-Select.md) `VS-T2` |

⚠️ ⛔ **Cho tới khi hai hàng đầu đóng, MỌI tài liệu trích số COGS phải mang nhãn *"SÀN — chưa cộng VLM; chi phí LLM chưa xác định"*.**

---

## 7. RIPPLE — những gì file này ⛔ không tự sửa được

| Điểm chạm | Nội dung | Ai xử lý |
|---|---|---|
| ⭐ `Schema/` (đã đóng) | ⛔ **Không tồn tại bảng nào đo chi phí LLM.** File này **cố ý ⛔ không thiết kế** một bảng như vậy — đó là quyết định của lô DB Schema, và phải có **PM quyết trước** rằng khoản này có nghĩa vụ đo hay không (`LP-T7`) | PM → Architect (lô Schema) |
| Lô Spec `M2` / `M3` / `M4` | 5 prompt template + rubric `beat_type` (`LP-T5`, hàng `P-10`) — file này chốt **schema output**, ⛔ không chốt **nội dung prompt** | Architect + Engineer |
| CI | ⭐ **Lint rule cấm compiler import `LlmProvider`** ([§2.5](#25-bốn-đường--cấm--mỗi-đường-một-guardrail-cưỡng-chế-được)) chưa tồn tại trong repo — nó là **điều kiện cưỡng chế** của `D-34`, ⛔ không phải một lời nhắc | Engineer, khi dựng CI |
| `Specs-MOC.md` | ⛔ Đang rỗng; `RULE-001` bắt cập nhật index | PM / owner của MOC |

---

## Tài liệu tham khảo

- [ADR-008 — Provider LLM và ranh giới sử dụng LLM](../Architecture/ADR-008-LLM-Provider-And-Usage-Boundaries.md)
- [ADR-014 — Visual Prompt Compiler deterministic và best-of-N](../Architecture/ADR-014-Deterministic-Prompt-Compiler-And-Best-Of-N.md)
- [ADR-015 — Job queue trong Postgres](../Architecture/ADR-015-Job-Queue-In-Postgres.md)
- [ADR-017 — Chuỗi provenance và ranh giới một transaction](../Architecture/ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md)
- [ADR-018 — `usage_event` và mô hình rollup](../Architecture/ADR-018-Usage-Event-And-Rollup-Model.md)
- [SDD-Comic-Studio](../Architecture/SDD-Comic-Studio.md) — `P-8`, `P-10`
- [DB-Entity-Provenance-And-Usage](../Schema/DB-Entity-Provenance-And-Usage.md) — `public.usage_event`, `public.field_provenance`
- [DB-Entity-Quality-Assets](../Schema/DB-Entity-Quality-Assets.md) — `generation.provider_refusal_log`
- [Spec-Integration-VLM-QA-Select](./Spec-Integration-VLM-QA-Select.md)
- [Spec-Integration-Image-Provider](./Spec-Integration-Image-Provider.md)
- [SRS-Comic-Studio](../../020-Requirements/SRS-Comic-Studio.md)

---

_Created by system-architect_
_Author: trisjr_
