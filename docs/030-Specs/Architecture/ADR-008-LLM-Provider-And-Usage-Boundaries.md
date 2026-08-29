---
id: ADR-008
type: adr
status: draft
project: comic-studio
created: 2026-08-29
---

# ADR-008: Provider LLM và ranh giới sử dụng LLM

Related to: [SDD-Comic-Studio](./SDD-Comic-Studio.md)

## Context

### Năm việc — và chỉ năm việc — được dùng LLM

| # | Việc | Module | Ranh giới đã CHỐT | Nguồn |
|--:|---|:--:|---|---|
| 1 | **Extraction** — phát `event` cho Story Bible | `M2` | LLM chỉ phát **event** (`entity, attribute, value, permanence, evidence_span, confidence`) cho **một** chapter; ⭐ **code sở hữu state** | `D-16` · [SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-FR-05` |
| 2 | **Speaker proposal** — đề xuất người nói | `M4` | LLM bị **constrained** vào tập nhân vật **có mặt trong scene**; **`UNKNOWN` là giá trị hợp lệ**; anchor **regex chạy TRƯỚC** LLM; lưu `speaker_confidence` | `D-26` · [SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-FR-14` |
| 3 | **Condensation** — nén thoại theo `text_budget` | `M4` | Là **human gate #2**, ⛔ không tuỳ chọn; chạy **SAU layout** vì `text_budget` phụ thuộc diện tích panel | `D-26`, `D-27` · [SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-FR-14`, `SRS-FR-15` |
| 4 | **Beat ranking** — xếp hạng beat trong chapter | `M3` | ⭐ LLM **chỉ xếp hạng**; **code phân bổ** theo emphasis quota; `dialogue_density` và `character_count` **do code đếm** | `D-23` · [SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-FR-09` |
| 5 | **Offline vocabulary** — soạn từ vựng `field value → cụm từ` | `M5` | **Offline một lần** → **người review** → **lưu vào bảng**. Là **dữ liệu**, ⛔ **không phải runtime** | `D-36` · [SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-FR-19` |

### Cái chưa ai quyết

⛔ **Không tài liệu Phase 1 nào chọn provider LLM** ([findings §5 hàng #3](../../010-Planning/pm-runs/2026-08-28-phase-2-architecture-design-comic-studio/findings/architect.md)). Phần mở của ADR này: **provider + prompt/versioning/cache policy**. ⛔ Ranh giới sử dụng thì **không mở**.

### ⛔ Năm ranh giới ĐÃ CHỐT — ADR này ghi lại, ⛔ không mở lại

| # | Ranh giới | Mã | Nguồn |
|:--:|---|:--:|---|
| **(a)** | LLM **chỉ phát event**, ⭐ **code sở hữu state**. `state_at(N) = reduce(events where story_order <= N)` là **hàm thuần** | `D-16` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-FR-05` |
| **(b)** | ⛔ **KHÔNG có LLM ở Visual Prompt Compiler runtime.** Compiler là **code deterministic**: tra bảng, sắp thứ tự, dedup, precedence ladder, constraint budget, drop log | `D-34` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-FR-17` |
| **(c)** | LLM chỉ xuất hiện trong compiler ở **HAI chỗ hẹp**, và **PHẢI CACHE**: (i) từ vựng offline → bảng; (ii) dịch action tự do → cụm pose khi từ vựng chưa có entry, **cache theo hash của action text**. *"Ngoài hai việc đó: không có LLM trong compiler"* | `D-36` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-FR-19` |
| **(d)** | LLM **constrained** vào nhân vật có mặt trong scene; **`UNKNOWN` hợp lệ**; ⛔ **không tồn tại đường code nào bypass hai human gate — kể cả cờ cấu hình** | `D-26` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-FR-14` |
| **(e)** | LLM **chỉ xếp hạng** beat; ⭐ **code phân bổ quota** emphasis theo phạm vi chapter | `D-23` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-FR-09` |

⚠️ Ranh giới **upstream** cũng đã chốt: `D-18` — **chapter parse + text clean là bước ĐẦU TIÊN** của pipeline và là **code deterministic** (regex/heuristic), ⛔ **không LLM** ([SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-FR-06`).

---

## Decision

### Q1. Một interface `LlmProvider`, năm **task profile** tách biệt

- **Một** seam adapter duy nhất (mẫu `D-40`, [SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-FR-23`): một interface, đổi provider không đổi code gọi.
- Nhưng **năm task profile riêng**: mỗi việc trong bảng trên có **prompt template riêng · version riêng · schema output riêng · cấu hình model riêng**.
- ⛔ **Không dùng chung một prompt cho nhiều việc.** Năm việc có năm tập giá trị đầu ra đóng khác nhau (`event` schema · tập nhân vật trong scene + `UNKNOWN` · text theo `text_budget` · thứ hạng beat · cụm từ vựng); gộp prompt là cách nhanh nhất để một ràng buộc của việc này rò sang việc kia.
- ⇒ Đổi provider **cho riêng một việc** phải làm được mà không chạm bốn việc còn lại.

### Q2. Output phải **structured / constrained**, ⛔ không phải văn xuôi tự do

| Việc | Đầu ra bắt buộc | Vì sao ràng buộc này không thương lượng |
|---|---|---|
| Extraction | Danh sách `event` đúng schema `D-16` | `state_at(N)` là **hàm thuần** trên event; một field lệch schema ⇒ state sai âm thầm |
| Speaker proposal | Giá trị thuộc **tập đóng** = {nhân vật có mặt trong scene} ∪ {`UNKNOWN`} | `D-26`. ⛔ Nếu output tự do, model sẽ **bịa tên nhân vật** — đúng thứ constraint tồn tại để chặn |
| Condensation | Text + độ dài đo được so `text_budget` | `D-27`: `text_budget` là ràng buộc từ layout đi ngược vào |
| Beat ranking | **Thứ hạng** beat | `D-23`. ⛔ Output ⛔ **không được chứa** quyết định panel size / full-page — đó là việc của code |
| Offline vocabulary | Cặp `field value → cụm từ` để **người review** rồi ghi bảng | `D-36`: là **dữ liệu**, không phải runtime |

### Q3. Versioning — ghi **cùng lúc** ba thứ với mọi output

Mọi artifact do LLM sinh ra phải ghi kèm: **`prompt_template_id` · `prompt_version` · `model_id` · `model_version`**.

- Mẫu lấy từ `D-40` (pin model version tường minh, [SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-FR-23`) và `D-59` (`model_id` + `model_version` + `attempt_no` trên **MỌI** generation, [SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-FR-31`).
- ⚠️ `D-59` cảnh báo: dữ liệu lịch sử **không backfill được** ⇒ bốn trường này phải có từ **bản ghi đầu tiên**, không phải backlog.
- Không có bốn trường này thì khi chất lượng đổi, ⛔ không phân biệt được *"đổi model"* với *"đổi prompt"* với *"đổi dữ liệu đầu vào"*.

### Q4. `field_provenance` — LLM phải trả về ở **mức field**

`D-49` ([SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-FR-36`) bắt provenance **mức FIELD**: field nào do LLM rút, field nào người khai/sửa.

⇒ ⭐ **Hợp đồng adapter phải trả về theo field**, ⛔ không trả một khối text rồi để tầng gọi tự bóc. Nếu adapter trả khối, `field_provenance` chỉ ghi được *"cả cụm này do AI"* — mất đúng độ hạt mà `KC-3` yêu cầu.

⇒ Hệ quả với `KC-4` (`D-50`, [SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-NFR-13`): bản ghi `field_provenance` phải commit **cùng transaction** với artifact ⇒ **lời gọi LLM phải hoàn tất TRƯỚC khi mở transaction ghi**. ⛔ Không giữ transaction mở trong lúc chờ mạng.

### Q5. Cache policy — ⛔ đúng hai chỗ, và ⛔ KHÔNG phải chiến lược chi phí

- **Hai chỗ duy nhất có cache LLM trong compiler** (`D-36`): (i) từ vựng offline → **bảng**; (ii) action tự do → cụm pose, **cache theo hash của action text**.
- ⛔ **Ngoài hai chỗ đó, không có cache LLM trong compiler.** Đây là nguyên văn của `D-36`, không phải diễn giải.
- ⭐ **Bốn việc còn lại (extraction, speaker, condensation, beat ranking) ⛔ KHÔNG nằm trong compiler** ⇒ `D-36` không cấp phép cache cho chúng. Nếu sau này muốn cache một trong bốn việc đó, phải mở một quyết định riêng và cân nhắc rằng chúng đứng **trước** hai human gate — cache một đề xuất đã bị người sửa là cách làm hỏng `D-28` (edit của người phải **khoá lại** khỏi bị re-run ghi đè, [SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-FR-12`).
- > [!WARNING]
  > ⛔ **Đừng dựa vào cache để cứu margin** — `D-64` ([SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-NFR-12`). Hai chỗ ra tiền thật là **reference-sheet amortization** và **idempotency**. Cache ở ADR này tồn tại để giữ compiler **deterministic và ổn định**, ⛔ **không phải** để giảm hoá đơn. Đọc ngược là hiểu sai `D-36` **và** `D-64`.

### Q6. Provider = **`TBD`**, tiêu chí chọn thì chốt ngay

⛔ ADR này **không chọn vendor**: [SRS](../../020-Requirements/SRS-Comic-Studio.md) §5.2 cấm tự gán số, và các biến quyết định (chi phí per-token cho 5 việc, chất lượng extraction trên văn bản tiếng Việt dài) **chưa có phép đo nào trong repo**.

**Tiêu chí chọn, theo thứ tự**:

| # | Tiêu chí | Neo |
|--:|---|---|
| **1** | **Constrained / structured output** — ép được tập giá trị đóng và schema | Điều kiện cần của `D-16`, `D-26`, `D-23`. ⛔ Không đạt ⇒ loại, không bù được bằng prompt |
| **2** | **Version pinning tường minh** | `D-40` + [Q3](#q3-versioning--ghi-cùng-lúc-ba-thứ-với-mọi-output); phòng silent model drift |
| **3** | **Cửa sổ ngữ cảnh đủ cho một chapter** | `D-16` phát event cho **một chapter** ⇒ **chapter là đơn vị ngữ cảnh**, không phải đoạn |
| **4** | **Chất lượng tiếng Việt** | ⚠️ *Suy luận, không phải quyết định Phase 1*: `D-30` bắt wrap tiếng Việt hiểu Unicode combining marks ([SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-FR-16`) ⇒ locale mục tiêu là tiếng Việt. ⛔ Không tài liệu nào phát biểu tiêu chí này tường minh |
| **5** | **Batch / async** | Pipeline vốn async (`D-03`); là **mong muốn**, ⛔ không phải CHỐT — `D-41` chỉ chốt batch cho **image** |
| **6** | **Chi phí per-token** | Chỉ so được sau khi (1) và (3) đã lọc |

**Ai đóng**: Architect + PM. **Khi nào**: sau khi MVP0 có dữ liệu chất lượng extraction/speaker đầu tiên (`D-65` bắt **HITL gate + eval kit ngay tại MVP1** và **log preference data từ MVP1** — [SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-NFR-18` ⇒ đã có sẵn cơ chế sinh dữ liệu để quyết).

### Q7. Bốn đường ⛔ CẤM — mỗi đường một guardrail cưỡng chế được

| ⛔ Cấm | Neo | Cưỡng chế bằng |
|---|---|---|
| Import LLM adapter từ module compiler (`M5` — Visual Prompt Compiler) | `D-34` ([SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-FR-17`) | **Lint rule ở CI** (mẫu `D-04`, [SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-NFR-04`): compiler ⛔ không được import `LlmProvider`. Hai chỗ hẹp của `D-36` đọc **bảng đã cache**, ⛔ không gọi provider |
| Ghi state trực tiếp từ output LLM | `D-16`, `D-17` ([SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-FR-05`, `SRS-NFR-10`) | Test guardrail: state **chỉ** đến từ `resolveState()` — `D-17` bắt có **đúng một** hàm; cộng test *"⛔ không có `ORDER BY chapter_no` trong bất kỳ đường resolve state nào"* |
| Cờ cấu hình bypass hai human gate | `D-26` ([SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-FR-14`) | Test: ⛔ **không tồn tại** tham số/cờ nào cho phép chuyển một page sang trạng thái xuất bản khi gate còn `OPEN` |
| ⭐ Dùng LLM để phát hiện *"truyện này có thể có bản quyền của người khác"* (copyright / plagiarism / similarity) | `D-53` — **ANTI-FEATURE** ([SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-NFR-15`) | ⚠️ **Prompt review**: ⛔ không prompt nào của 5 task profile được chứa câu hỏi loại đó. Lý do: nó tạo ra **đúng tri thức** mà điều kiện *"không biết"* của miễn trừ Điều 198b đang miễn trừ. ⚠️ Đây là chỗ *"một dev sẽ làm ngược theo bản năng"* |

### Q8. Ghi lại mọi lần provider từ chối

`D-67` ([SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-NFR-20`) bắt **ghi lại mọi lần provider từ chối vì content policy** — áp cho **cả LLM**, không chỉ image provider. Ngưỡng rate limit đi kèm là **`TBD`** ([SRS](../../020-Requirements/SRS-Comic-Studio.md) §5.2), ⛔ không gán số ở đây.

---

## Alternatives considered

### (a) Một interface + năm task profile — ⭐ ĐÃ CHỌN

**Điểm mạnh**: một seam để đổi provider; năm prompt/version độc lập ⇒ đổi được từng việc; quy trách nhiệm được khi chất lượng đổi.
**Điểm yếu**: năm prompt template phải bảo trì, năm chuỗi version phải theo dõi — với **1 dev** đây là chi phí thật, không nhỏ.

### (b) Một prompt / một cấu hình chung cho cả năm việc

**Điểm hấp dẫn**: ít thứ phải bảo trì nhất — đúng ràng buộc *"1 dev + AI assist"*.

**⛔ Loại vì**: năm việc có **năm tập giá trị đầu ra đóng khác nhau**. `D-26` bắt speaker phải bị constrained vào **tập nhân vật có mặt trong scene** — ràng buộc này **không tồn tại** ở bốn việc kia. Một prompt chung nghĩa là hoặc bỏ ràng buộc đó (vi phạm `D-26`), hoặc áp nó cho cả năm việc (vô nghĩa). Ngoài ra, một prompt chung ⇒ **một version chung** ⇒ sửa prompt cho beat ranking làm đổi hành vi extraction mà không ai biết.

### (c) Nhiều provider khác nhau cho từng việc ngay từ MVP

**Điểm mạnh thật**: mỗi việc dùng model hợp nhất; giảm phụ thuộc một vendor.

**⛔ Loại (ở thời điểm này)**: với **1 dev**, nó nhân lên số credential, số hạn mức, số failure mode, số hoá đơn phải đối soát — trong khi ⛔ **chưa có dữ liệu nào** nói việc nào cần model khác. ⚠️ Đây là **loại vì chưa đúng lúc**, không phải loại vĩnh viễn: [Q1](#q1-một-interface-llmprovider-năm-task-profile-tách-biệt) cố ý giữ năm task profile riêng **chính là** để mở đường này mà không phải refactor.

### (d) Chốt luôn một vendor trong ADR này

**⛔ Loại**: cùng lý do `ADR-007` [Q4](./ADR-007-VLM-Provider-For-QA-Select.md). [SRS](../../020-Requirements/SRS-Comic-Studio.md) §1.3 nói rõ *"Chọn giúp … làm tầng design **mất quyền quyết định thật** và tạo một *quyết định* **không ai chịu trách nhiệm**"* — và cũng nói lựa chọn vendor *"**sẽ được đặc tả tại tầng 030-Specs**"*. ⇒ ADR này chốt **seam + tiêu chí + guardrail** ngay, và đặt việc chốt tên vào một **gate có dữ liệu** (`D-65`, eval kit MVP1), không phải một suy đoán hôm nay.

### (e) Gộp `ADR-007` (VLM) và ADR này thành một *"Model Provider Strategy"*

[findings §2.1](../../010-Planning/pm-runs/2026-08-28-phase-2-architecture-design-comic-studio/findings/architect.md) ghi ADR-008 là **🟡 tuỳ chọn**, *"gộp được vào ADR-007"*.

**⛔ Loại — và ghi lại cái giá để lần sau không ai gộp mà không biết**: [findings §5 lưu ý #1](../../010-Planning/pm-runs/2026-08-28-phase-2-architecture-design-comic-studio/findings/architect.md) nói tách VLM khỏi image provider là *"bắt buộc, không phải sở thích"*, vì gộp **che mất khoản chi phí VLM chưa được tính**. Cùng logic áp ở đây: LLM và VLM có **ràng buộc chọn khác nhau** (constrained text output vs nhiều ảnh trong một call), **ranh giới sử dụng khác nhau** (LLM có 5 ranh giới CHỐT ở [Context](#context); VLM thì không), và **vị trí trong pipeline khác nhau** (LLM đứng **trước** hai human gate; VLM đứng **sau** khi ảnh đã sinh). Gộp ⇒ năm ranh giới của LLM bị pha loãng trong một tài liệu nói về chấm ảnh.

### (f) Fine-tune / LoRA riêng cho các việc LLM

**⛔ Loại**: `D-08` / `SRS-NFR-26` hoãn **fine-tune riêng từng tenant** khỏi horizon ([SRS](../../020-Requirements/SRS-Comic-Studio.md)). ⚠️ *"Hoãn ≠ cắt hẳn"* — §6.3 để cửa ở Full Scope; ghi lại để không ai đọc thành cấm vĩnh viễn.

### (g) Tự host model LLM mở

**⛔ Loại**: `D-07` / `SRS-NFR-11` — ⛔ **không mua GPU**; API cho main path; self-host **chỉ** cho LoRA train / upscale / inpainting ([SRS](../../020-Requirements/SRS-Comic-Studio.md)). Cả năm việc đều nằm trên main path.

### (h) Cache rộng hơn hai chỗ để giảm chi phí

**⛔ Loại kép**: `D-36` **CHỐT** đúng hai chỗ ([SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-FR-19`), **và** `D-64` cấm coi cache là chiến lược margin ([SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-NFR-12`). Hai quyết định độc lập cùng chặn hướng này.

---

## Consequences

### Tích cực

- ⭐ **Năm ranh giới CHỐT trở thành tài sản trích dẫn được**, kèm **guardrail cưỡng chế được** ([Q7](#q7-bốn-đường--cấm--mỗi-đường-một-guardrail-cưỡng-chế-được)) chứ không phải lời nhắc trong prompt. Đây là giá trị lớn nhất của tài liệu này — lớn hơn phần chọn provider.
- `Spec-Integration-LLM-Provider.md` viết được ngay ở mức **seam**, không chờ vendor.
- Bốn trường version ([Q3](#q3-versioning--ghi-cùng-lúc-ba-thứ-với-mọi-output)) làm **silent model drift** có dấu vết để lần, và phân biệt được *"đổi model"* với *"đổi prompt"*.
- `field_provenance` mức field ([Q4](#q4-field_provenance--llm-phải-trả-về-ở-mức-field)) giữ `KC-3` đúng độ hạt mà nghĩa vụ pháp lý cần.
- Năm task profile riêng ⇒ đường nâng cấp sang phương án (c) mở sẵn, ⛔ không cần refactor.

### Tiêu cực

- **Năm prompt template + năm chuỗi version phải bảo trì** với **1 dev**. Đây là chi phí thật; nó chỉ đáng nếu bốn trường version thực sự được ghi và thực sự được đọc khi có sự cố.
- **`D-16` bắt đơn vị ngữ cảnh là một chapter** ⇒ mỗi lời gọi extraction mang cả chapter. Chi phí per-call theo độ dài chapter — ⛔ **không có số nào trong repo** để ước lượng.
- **Lời gọi LLM phải hoàn tất trước khi mở transaction ghi** ([Q4](#q4-field_provenance--llm-phải-trả-về-ở-mức-field)) ⇒ luồng code dài hơn *"gọi và ghi trong một hàm"*, và trạng thái *"đã gọi xong nhưng chưa ghi"* phải xử lý tường minh.
- **Provider `TBD`** ⇒ lô API sau viết `Spec-Integration-LLM-Provider.md` ở **mức seam**, ⛔ không mức vendor. Retry policy và error taxonomy per provider vẫn `TBD` — [SRS](../../020-Requirements/SRS-Comic-Studio.md) §1.3 xếp rõ chúng vào tầng design.
- **Tiêu chí #1 (constrained output) là tiêu chí loại.** Nếu ứng viên tốt nhất về chất lượng tiếng Việt lại yếu về structured output, ⛔ **không được bù bằng prompt** — phải quay lại PM. Rủi ro đã biết, không phải rủi ro ẩn.

### ⚠️ Về chi phí — không được suy diễn

> [!WARNING]
> Repo chỉ tuyên bố **tường minh** rằng khoản **chi phí VLM** là phần **chưa tính** của `CF-3.5` ([SRS](../../020-Requirements/SRS-Comic-Studio.md) §4.3 · §5.2) — xem [ADR-007](./ADR-007-VLM-Provider-For-QA-Select.md).
>
> ⛔ **Với chi phí LLM cho 5 việc, ⛔ không có dòng nào trong repo xác nhận nó đã được tính hay chưa.** ⇒ Đối xử như **chưa xác định**. ⛔ **Không** cộng, ⛔ **không** trừ, ⛔ **không** suy nó vào con số `$12,06/chapter` — con số đó là **SÀN, không phải trần** ([SRS](../../020-Requirements/SRS-Comic-Studio.md) `CẤM-04`).
>
> Bỏ nhãn khi nhân một ước lượng là lỗi [SRS](../../020-Requirements/SRS-Comic-Studio.md) §1.2 gọi là **"rửa sạch"** khoảng trống.
>
> **Ai đóng**: PM, khi mô hình tài chính được cập nhật sau MVP0.

### Việc còn để `TBD` — ⛔ không được bịa

| Việc | Ai đóng | Khi nào |
|---|---|:--|
| **Tên provider LLM** | Architect + PM | Sau MVP0/MVP1, dựa trên eval kit của `D-65` |
| **Chi phí LLM per chapter** cho 5 việc | PM | Khi cập nhật mô hình tài chính sau MVP0 |
| Retry policy + error taxonomy per provider | Architect (lô API) | Trong `Spec-Integration-LLM-Provider.md` |
| Ngưỡng rate limit / giới hạn upload (`D-67`) | PM + Architect | [SRS](../../020-Requirements/SRS-Comic-Studio.md) §5.2 để `TBD`; sau đo tải |
| Nội dung cụ thể của 5 prompt template + rubric `beat_type` (enum + anchor example của `D-23`) | Architect + Engineer | Lô Spec chi tiết của `M2`/`M3`/`M4` |
| Có cache cho 4 việc ngoài compiler hay không | Architect | Chỉ mở khi có số đo; ⚠️ phải cân với `D-28` (khoá edit của người) |

---

## Đã quyết ở đâu

| Quyết định | Mã `D-xx` | Nguồn (file + mã requirement) |
|---|:--:|---|
| LLM **chỉ phát event**; ⭐ **code sở hữu state**; `state_at(N)=reduce(events)` là hàm thuần; event cho **một** chapter | `D-16` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-FR-05` |
| **Đúng MỘT** hàm `resolveState()`; test guardrail ⛔ không `ORDER BY chapter_no` | `D-17` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-NFR-10` |
| Chapter parse + text clean là bước **ĐẦU TIÊN**, **code deterministic**, ⛔ **không LLM** | `D-18` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-FR-06` |
| Layout bằng rubric `beat_type` + code đếm `dialogue_density`/`character_count`; ⭐ **LLM chỉ xếp hạng**, **code phân bổ quota** | `D-23` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-FR-09` |
| **HAI human gate bắt buộc**; LLM **constrained** vào nhân vật có mặt trong scene; **`UNKNOWN` hợp lệ**; regex anchor **trước** LLM; `speaker_confidence`; ⛔ **không đường bypass, kể cả cờ cấu hình** | `D-26` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-FR-14` |
| Condensation nằm **SAU layout** vì `text_budget` phụ thuộc diện tích panel | `D-27` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-FR-15` |
| **Hai field thoại**: `dialogue_source` bất biến · `dialogue_rendered` — **edit của người phải KHOÁ LẠI** khỏi bị re-run ghi đè | `D-28` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-FR-12` |
| ⛔ **KHÔNG LLM ở Visual Prompt Compiler runtime**; compiler là code deterministic | `D-34` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-FR-17` |
| LLM trong compiler chỉ ở **HAI chỗ hẹp**, **PHẢI CACHE**; ngoài hai việc đó ⛔ không có LLM trong compiler | `D-36` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-FR-19` |
| **Adapter per provider** + **pin model version tường minh** (mẫu áp cho LLM) | `D-40` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-FR-23` |
| ⛔ **Không mua GPU**; API cho main path; self-host chỉ LoRA train / upscale / inpainting | `D-07` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-NFR-11` |
| Wrap tiếng Việt phải dùng thư viện hiểu **Unicode combining marks** | `D-30` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-FR-16` |
| `field_provenance` **mức FIELD** + `generation.origin` | `D-49` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-FR-36` |
| **`KC-4`** — provenance commit **cùng một transaction** với artifact | `D-50` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-NFR-13` |
| `cost_usd` + `model_id` + `model_version` + `attempt_no` trên **MỌI** generation; ⛔ không backfill được | `D-59` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-FR-31` |
| ⛔ **Đừng dựa vào cache để cứu margin**; hai chỗ ra tiền thật là reference-sheet amortization và idempotency | `D-64` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-NFR-12` |
| **HITL gate + eval kit ngay tại MVP1**; **log preference data từ MVP1** | `D-65` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-NFR-18` |
| Ghi lại **mọi** lần provider từ chối vì content policy; ngưỡng số = `TBD` | `D-67` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-NFR-20` · §5.2 |
| ⛔ **ANTI-FEATURE**: ⛔ không bộ phát hiện bản quyền / plagiarism / similarity trước khi luật sư xác nhận | `D-53` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-NFR-15` |
| Hoãn khỏi horizon: **fine-tune riêng từng tenant** (hoãn ≠ cắt hẳn) | `D-08` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-NFR-26` |
| Lint rule cấm import chéo module, cưỡng chế ở CI (mẫu cho [Q7](#q7-bốn-đường--cấm--mỗi-đường-một-guardrail-cưỡng-chế-được)) | `D-04` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-NFR-04` |
| Job queue trong Postgres ⇒ pipeline vốn async | `D-03` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-FR-25` |
| ⛔ Không tự gán số cho hàng `TBD` | — | [SRS](../../020-Requirements/SRS-Comic-Studio.md) §5.2 |
| COGS `$12,06`/chapter là **SÀN**, ⛔ không phải trần (`CẤM-04`) | — | [SRS](../../020-Requirements/SRS-Comic-Studio.md) `CẤM-04` |
| Lựa chọn vendor thuộc tầng **030-Specs**; ⛔ chọn giúp ở tầng trên tạo *"quyết định"* không ai chịu trách nhiệm | — | [SRS](../../020-Requirements/SRS-Comic-Studio.md) §1.3 |
| ⛔ **CHƯA quyết ở Phase 1**: provider LLM | — | [findings/architect §5 hàng #3](../../010-Planning/pm-runs/2026-08-28-phase-2-architecture-design-comic-studio/findings/architect.md) |
