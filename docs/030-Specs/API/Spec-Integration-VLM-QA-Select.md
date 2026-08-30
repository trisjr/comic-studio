---
id: SPEC-INT-VLM-QA-SELECT
type: spec
status: draft
project: comic-studio
created: 2026-08-29
---

# Spec-Integration-VLM-QA-Select — adapter VLM cho QA-select giữa N candidate

Related to: [ADR-007](../Architecture/ADR-007-VLM-Provider-For-QA-Select.md) · [ADR-014](../Architecture/ADR-014-Deterministic-Prompt-Compiler-And-Best-Of-N.md) · [ADR-015](../Architecture/ADR-015-Job-Queue-In-Postgres.md) · [ADR-018](../Architecture/ADR-018-Usage-Event-And-Rollup-Model.md) · [SDD](../Architecture/SDD-Comic-Studio.md)

---

## 1. Mục đích

⭐ **File này tồn tại TÁCH RIÊNG khỏi [Spec-Integration-Image-Provider](./Spec-Integration-Image-Provider.md), và sự tách đó là BẮT BUỘC, ⛔ không phải sở thích.**

> Gộp hai file **làm che mất** chuyện **chi phí VLM chưa được cộng vào bất kỳ con số COGS nào** — và đó chính là khoản làm `$12,06`/chapter là **SÀN** chứ ⛔ không phải trần ([ADR-007](../Architecture/ADR-007-VLM-Provider-For-QA-Select.md) Alternatives `(a)`, [ADR-016](../Architecture/ADR-016-Image-Provider-Adapter-And-Version-Pinning.md) Alternatives `(f)`).

Ba lý do kỹ thuật độc lập nữa, ⛔ để ⛔ không ai đọc sự tách này thành một chi tiết trình bày:

1. **Hai vòng đời model version.** Đổi model ảnh và đổi model chấm là hai sự kiện độc lập ⇒ pin riêng, quy trách nhiệm riêng khi chất lượng đổi.
2. **Hai đường lỗi khác nhau.** *"Ảnh sinh xong nhưng chấm hỏng"* là một trạng thái **HỢP LỆ** đã được đặc tả — ⛔ không phải *"cả job fail"*.
3. **Hai ràng buộc chọn vendor khác nhau.** Tiêu chí *"nhận nhiều ảnh trong MỘT call"* ⛔ không liên quan gì tới tiêu chí chọn provider sinh ảnh.

⚠️ **Kể cả khi hai vendor TRÙNG NHAU, hai adapter vẫn tách.** Trùng vendor là một chi tiết **cấu hình**, ⛔ không phải một sự thật kiến trúc.

⇒ Mục [§6 Chi phí](#6-chi-phí) là **phần bắt buộc** của file này, ⛔ không phải phần phụ lục.

---

## 2. Cái gì đã CHỐT

### 2.1 Cơ chế — ⛔ không mở lại

| # | Nội dung | Mã | Nguồn |
|--:|---|:--:|---|
| `VS-C1` | **best-of-N**: sinh **N candidate cho MỌI panel** rồi **VLM QA-select 1**. ⚠️ ⛔ **KHÔNG phải retry-on-failure.** `N` mặc định = **3** | `D-37` | `SRS-FR-20` |
| `VS-C2` | **Continuity Checker = QA-based selection giữa N candidate.** Output là **hàng đợi review được XẾP HẠNG**. ⛔ Cắt hẳn `[Fix automatically]`; giữ **CẢ HAI** version, **side-by-side**, ⭐ **NGƯỜI CHỌN**, ⛔ không bao giờ tự áp dụng | `D-38` | `SRS-FR-21` |
| `VS-C3` | ⭐ **`unclear` là câu trả lời hợp lệ HẠNG NHẤT.** ⛔ Không map thành `fail`, ⛔ không map thành `pass`, ⛔ không ép thành số rồi cắt ngưỡng, ⛔ không phải `NULL`, ⛔ không phải lỗi | `D-38` | `SRS-FR-21` |
| `VS-C4` | Phải **hiện tường minh ĐỘ PHỦ** của checker cho user (*"đã kiểm N/M panel"*) | `D-39` | `SRS-FR-22` |
| `VS-C5` | **Integration RIÊNG, adapter riêng** (`VlmQaSelector`), ⛔ không gộp vào adapter image provider | `D-40` (mẫu) | [ADR-007](../Architecture/ADR-007-VLM-Provider-For-QA-Select.md) `Q1` |
| `VS-C6` | Nằm trong module **`M5`**, chạy **SAU** khi N candidate đã sinh xong. ⚠️ ⛔ **Không được gọi từ Visual Prompt Compiler** — `D-34` cấm LLM/VLM ở compiler runtime | `D-34` | `SRS-FR-17` · [ADR-007](../Architecture/ADR-007-VLM-Provider-For-QA-Select.md) `Q1` |
| `VS-C7` | **Pin `model_id` + `model_version` tường minh** trong config; ghi vào bản ghi chấm của **MỌI** lần gọi | `D-40` + `D-59` | `SRS-FR-23` · `SRS-FR-31` |
| `VS-C8` | ⭐ **Chế độ mặc định của MỌI check là `report_only`.** Bật một check thành `influencing` **chỉ sau khi** cổng chất lượng PASS cho **CHÍNH check đó**. ⛔ Không bật cả cụm một lượt | — | [ADR-007](../Architecture/ADR-007-VLM-Provider-For-QA-Select.md) `Q3` |
| `VS-C9` | ⛔ **Không mua GPU** — QA-select nằm trên main path ⇒ ⛔ không self-host | `D-07` | `SRS-NFR-11` |
| `VS-C10` | Ghi lại **MỌI** lần provider từ chối vì content policy | `D-67` | `SRS-NFR-20` |

### 2.2 Cổng chất lượng để bật một check — đã CHỐT, ⛔ không thương lượng

> **precision ≥ ~0.7 trên ≥ 100 panel dán nhãn TAY, TRƯỚC KHI BẬT MỘT CHECK NÀO — kể cả `face`** (nhãn `[EM]`).

⇒ Trạng thái mặc định của mọi check là **`report_only`** (`VS-C8`). ⛔ Một check chưa qua cổng của **chính nó** ⛔ không được ảnh hưởng tới lựa chọn.

⚠️ **Độ phủ 40–60%** (`D-39`, nhãn `[EM]`) phải **công bố cho user** — ⭐ nó là **FR MINH BẠCH**, ⛔ **không phải chỉ tiêu chất lượng để đạt**. Đọc ngược nó thành KPI là hiểu sai `D-39`.

### 2.3 Ba đường ⛔ CẤM

| ⛔ Cấm | Vì sao | Neo |
|---|---|---|
| ⭐ VLM **tự chấm golden dataset thay người** | Dataset regression là thứ dùng để **phát hiện** model drift; chấm nó bằng một model là **mất điểm neo**. ⭐ `score_card` của `generation.golden_dataset_item` do **NGƯỜI** chấm (`QA-11`) | `D-66` · **`SRS-NFR-19`** |
| VLM **tự áp dụng bản sửa** | `D-38`: giữ cả hai version, **người chọn**. ⛔ Preselect **KHÔNG** tự thành lựa chọn của người (`E-4`) | `D-38` · `SRS-FR-21` |
| ⭐ VLM phát hiện *"truyện này có thể có bản quyền của người khác"* (copyright / plagiarism / similarity) | ⚠️ **ANTI-FEATURE CÓ CHỦ Ý**: nó tạo ra **đúng tri thức** mà điều kiện *"không biết"* của miễn trừ **Điều 198b** đang miễn trừ ⇒ nó **tự phá miễn trừ**. Đây là chỗ *"một dev sẽ làm ngược theo bản năng"* | `D-53` · **`SRS-NFR-15`** |

> [!CAUTION]
> ⛔ **Cưỡng chế của hàng thứ ba là REVIEW BỘ CÂU HỎI KIỂM TRA.** ⛔ Không một `check_key` nào của checker được chứa câu hỏi loại *"ảnh này có giống tác phẩm nào không"*, *"nhân vật này có phải nhân vật có bản quyền không"*. Ràng buộc này áp **trước khi luật sư xác nhận**, ⛔ không có ngoại lệ kỹ thuật.

---

## 3. Cái gì còn MỞ

⛔ **File này ⛔ KHÔNG chọn vendor** — và lý do ⛔ không phải sự lười ([ADR-007](../Architecture/ADR-007-VLM-Provider-For-QA-Select.md) `Q4`): biến quyết định chính là **chi phí per-call × N × số panel/chapter**, mà con số đó ⛔ **không tồn tại trong repo**. Chọn vendor trước khi có nó là **chọn mù**.

| Mã | `TBD` | Ai đóng | Khi nào |
|---|---|---|---|
| `VS-T1` | ⭐ **Tên provider VLM** | **PM + Architect** | **Gate cuối MVP0**, khi ba phép đo bắt buộc của MVP0 có kết quả |
| `VS-T2` | ⭐ **Chi phí VLM per-call** và tổng khoản thiếu của `CF-3.5` | **PM + Architect** | Sau đo MVP0 |
| `VS-T3` | **N tối thiểu** (`CF-8.5`, mỗi bậc `N` giảm ≈33% COGS). ⚠️ **Budget vẫn phải tính ở N=3**; ⛔ đổi N ⇒ **chạy lại `G1`** (`CẤM-03`) | **PM** | Sau đo MVP0 |
| `VS-T4` | **Human-reject rate sau VLM-select** — [SRS](../../020-Requirements/SRS-Comic-Studio.md) §5.2 ghi *"chưa ai công bố con số này"* | **Engineer đo, PM đọc** | MVP0 |
| `VS-T5` | **Bộ câu hỏi kiểm tra cụ thể** của checker + **cổng precision cho TỪNG check** | **Architect + Engineer** | Trước khi bật check đầu tiên |
| `VS-T6` | **Cơ chế lưu `vlm_call_ref`** bền qua retry ([§4.4](#44-idempotency-key--ràng-buộc-được-route-về-file-này)) | Architect (lô Schema kế tiếp) + Engineer | Trước khi adapter VLM đầu tiên chạy. ⚠️ `Schema/` đã đóng ⇒ xem [RIPPLE](#7-ripple--những-gì-file-này--không-tự-sửa-được) |
| `VS-T7` | **Ánh xạ mã lỗi thô của provider VLM → năm lớp lỗi**. ⛔ Không viết được trước khi `VS-T1` đóng | Engineer | Sau `VS-T1`, khi viết adapter |
| `VS-T8` | **Ngưỡng rate limit** đi kèm `D-67` cho đường VLM | PM + Architect | Sau đo tải |

### 3.1 Tiêu chí chọn vendor — CHỐT ngay, theo đúng thứ tự

Để `VS-T1` ⛔ không chặn file này, tiêu chí đã được chốt sẵn:

| # | Tiêu chí | Loại | Vì sao ở thứ tự này |
|--:|---|:--:|---|
| **1** | ⭐ **Nhận NHIỀU ẢNH trong MỘT call** để so sánh N candidate trong cùng ngữ cảnh | ⛔ **LOẠI** | Nếu provider chỉ nhận 1 ảnh/call thì **bản chất bài toán đổi**: từ *"so sánh N"* thành *"chấm điểm từng cái rồi so số"*, và **chi phí nhân N** |
| **2** | **Structured output ổn định**, map thẳng vào `{pass, fail, unclear}` | ⛔ **LOẠI** | `VS-C3` bắt `unclear` là giá trị hạng nhất ⇒ output tự do phải parse là **chỗ `unclear` bị bóp méo thành `fail`** |
| **3** | **Version pinning tường minh** | ⛔ **LOẠI** | ⛔ Không pin được ⇒ ⛔ không phát hiện được **silent model drift** |
| **4** | **Batch / async mode** | ⚠️ mong muốn | Pipeline đã async nên batch là fit tự nhiên. ⛔ **Không phải CHỐT** — `D-41` chỉ chốt batch cho **image** |
| **5** | **Chi phí per-call** | cộng điểm | Chỉ **so sánh được sau khi (1) đã lọc** — nếu phải gọi N lần thì đơn giá per-call ⛔ không nói lên gì |

> [!WARNING]
> ⚠️ **Rủi ro ĐÃ BIẾT, ⛔ không phải rủi ro ẩn**: nếu **tất cả** ứng viên đều ⛔ **không** nhận nhiều ảnh trong một call ⇒ chi phí nhân `N` và bài toán đổi bản chất ⇒ **phải quay lại `D-37` với PM**, ⛔ không được tự xử lý ở tầng adapter.

---

## 4. Interface / seam

### 4.1 Hợp đồng `VlmQaSelector`

**Input:**

| Trường | Ràng buộc |
|---|---|
| `candidates[]` | ⭐ **N candidate dạng `object_key`, ⛔ KHÔNG phải blob** (`D-13`). Mỗi phần tử neo về một dòng `generation.generation` có `generation_kind = 'candidate'` |
| `panel_spec_constraints` | Identity reference của panel + trần **≤ 3 nhân vật** (`D-21`) |
| `check_set` | Bộ câu hỏi kiểm tra + **`mode` của từng check** (`report_only` \| `influencing`) — nội dung cụ thể là `VS-T5` |
| `model_id` · `model_version` | ⛔ Pin tường minh (`VS-C7`) |
| ⭐ `tenant_credential` | ⭐ Nhận **THEO TENANT ở chữ ký hàm**, ⛔ không đọc thẳng biến môi trường toàn cục — cùng khuôn seam `S-4` của đường image |

**Output:**

| Trường | Đích ghi (`generation.vlm_evaluation`) | Ràng buộc |
|---|---|---|
| `selection_run_id` | `selection_run_id` | Gom N candidate được chấm **cùng một lượt**. ⛔ Không phải FK — nó là **định danh của một lần gọi adapter** |
| ⭐ `verdict` | `verdict` | `'pass'` \| `'fail'` \| `'unclear'` — `TEXT` + `CHECK`, ⛔ **không** Postgres enum type (`E15`) |
| `confidence` | `confidence` | `NULL` **hợp lệ** khi provider ⛔ không cung cấp |
| `reason` | `reason` | Lý do **ngắn** — phần *"giải thích"* của hợp đồng |
| ⭐ `rank` | `rank` | Thứ hạng trong **hàng đợi review được xếp hạng** (`VS-C2`) |
| `is_preselected` | `is_preselected` | ⛔ **Preselect KHÔNG tự thành lựa chọn của người** (`E-4`) |
| `check_results` | `check_results` | `{check_key, verdict, mode}` với `mode ∈ {report_only, influencing}` |
| `model_id` · `model_version` | `model_id` · `model_version` | Model **thực sự được gọi**; ghi **riêng biệt**, ⛔ không ghi đè |

> [!IMPORTANT]
> ⭐ **`mode` nằm TRONG `check_results` của TỪNG DÒNG, ⛔ không phải một cấu hình toàn cục đọc lúc báo cáo.**
> Lý do: bật một check thành `influencing` chỉ sau khi cổng chất lượng PASS **cho chính check đó** ⇒ bản ghi lịch sử phải nhớ **LÚC ĐÓ** check nào đang ảnh hưởng tới lựa chọn.

### 4.2 Quyền hạn của adapter — ⛔ ranh giới cứng

| Adapter ĐƯỢC làm | Adapter ⛔ KHÔNG được làm |
|---|---|
| Xếp hạng N candidate | ⛔ Tự **chọn** thay người |
| Giải thích lý do từng verdict | ⛔ Tự **áp dụng** bản sửa |
| Đánh dấu `is_preselected` | ⛔ Coi `is_preselected` là quyết định cuối |
| Trả `unclear` | ⛔ Map `unclear` sang `pass` / `fail` / `NULL` |
| Chấm theo `check_set` được cấu hình | ⛔ Thêm câu hỏi về **bản quyền / plagiarism / similarity** (`SRS-NFR-15`) |
| — | ⛔ Chấm **golden dataset** thay người (`D-66`) |

### 4.3 ⛔ Adapter này KHÔNG ghi tiền vào `vlm_evaluation`

> [!WARNING]
> ⛔ **`generation.vlm_evaluation` KHÔNG có cột `cost_usd` — và đó ⛔ KHÔNG phải một quyết định bỏ đo.**
> `vlm_evaluation` giữ **ĐIỂM CHẤM**; `generation.vlm_scoring_call` giữ **TIỀN**. Thêm `cost_usd` vào `vlm_evaluation` là tạo **nguồn sự thật thứ hai** cho cùng một khoản chi.
> ⇒ Xem [§6.2](#62--chi-phí-vlm-đo-ở-đâu--và-vì-sao-ở-đó).

### 4.4 Idempotency key — ràng buộc được route về file này

[DB-Entity-Provenance-And-Usage](../Schema/DB-Entity-Provenance-And-Usage.md) chốt hình dạng và **route phần còn lại về đúng adapter này**:

```
idempotency_key = {generation_id} : {vlm_call_ref}
```

- `generation_id` trỏ dòng `generation.generation` **cấp request** (`generation_kind = 'request'`, **đã commit** trước bước chấm điểm) — giữ nguyên tinh thần `GR-2`: ⛔ **không có dòng chi phí mồ côi**.
- ⭐ **`vlm_call_ref` phải BỀN QUA RETRY**: sinh **TRƯỚC** lời gọi VLM, lưu **cùng** kết quả. ⛔ **Không sinh lại mỗi lần worker nhặt job.**
- Khoá này là **RIÊNG của bảng `vlm_scoring_call`**, có `UNIQUE (tenant_id, idempotency_key)` riêng ⇒ ⛔ không còn khả năng đụng khoá với `usage_event` (đó là lý do thành phần `{event_kind}` bị bỏ khỏi khoá — `E20`).

⚠️ **Cơ chế lưu cụ thể của `vlm_call_ref` = `VS-T6`.** ⛔ File này ⛔ không tự thêm cột — `Schema/` đã đóng.

---

## 5. Retry & error taxonomy

### 5.1 ⭐ Hành vi khi VLM lỗi / timeout — CHỐT, ⛔ không được tự chọn

Tình huống đã được đặc tả nguyên trạng: **VLM-select thất bại / timeout SAU KHI cả N candidate đã sinh** — tức **tài nguyên đã tiêu**.

| Bắt buộc | ⛔ Cấm |
|---|---|
| Giữ **CẢ N candidate** | ⛔ Tự chọn candidate **đầu tiên** |
| Đẩy vào **hàng đợi review của NGƯỜI** | ⛔ Coi lỗi VLM là **lỗi của cả job generation** |
| Đánh dấu trạng thái **tương đương `unclear`** | ⛔ Rollback `usage_event` của N candidate — chúng **đã** được ghi trước đó, ⛔ và tiền đã tiêu là tiền đã tiêu |

⭐ ***"Ảnh sinh xong nhưng chấm hỏng" là một TRẠNG THÁI HỢP LỆ***, ⛔ không phải một lỗi cần dọn dẹp. Đây là một trong bốn lý do hai adapter phải tách ([§1](#1-mục-đích)).

### 5.2 Năm lớp lỗi — adapter phân loại, job queue quyết định

Cùng **danh sách đóng** của [ADR-015](../Architecture/ADR-015-Job-Queue-In-Postgres.md) `Q5` — ⛔ file này ⛔ không thêm lớp thứ sáu.

| `error_class` | Quy tắc phân loại **ở đường VLM** | Hệ quả |
|---|---|:--|
| `transient_infra` | Lỗi **trước khi** request rời tiến trình | ✅ Retry + backoff. ⛔ Chưa gọi ⇒ ⛔ **không** ghi `vlm_scoring_call` |
| `transient_provider` | VLM **timeout**, **rate limit**, lỗi tạm thời phía provider | ✅ Retry + backoff. ⚠️ Nếu lời gọi **đã rời tiến trình** ⇒ xem [§5.3](#53-lỗi-sau-khi-đã-gọi--tiền-vlm-đã-tiêu) |
| `permanent_input` | `object_key` của candidate ⛔ không đọc được; `check_set` sai cấu hình; `model_id`/`model_version` ⛔ không tồn tại | ⛔ Không retry ⇒ áp [§5.1](#51--hành-vi-khi-vlm-lỗi--timeout--chốt--không-được-tự-chọn) |
| ⭐ `permanent_policy` | VLM **từ chối vì content policy** | ⛔ Không retry. ⭐ **BẮT BUỘC ghi `generation.provider_refusal_log`** với `provider_kind = 'vlm'` — xem [§5.4](#54-permanent_policy--nghĩa-vụ-ghi-nhật-ký-d-67) |
| `permanent_unknown` | ⛔ Chưa phân loại được | ⛔ Không retry; ⚠️ **phải xuất hiện trong chẩn đoán**, ⛔ không im lặng |

⚠️ **Với MỌI lớp permanent, hệ quả ở [§5.1](#51--hành-vi-khi-vlm-lỗi--timeout--chốt--không-được-tự-chọn) vẫn áp**: N candidate ⛔ không bị vứt, job generation ⛔ không bị đánh fail.

⛔ **File này KHÔNG liệt kê mã lỗi thô của một provider cụ thể** — `VS-T1` chưa đóng thì ⛔ không có provider nào để tra mã. Hàng `VS-T7`.

### 5.3 Lỗi SAU khi đã gọi — tiền VLM đã tiêu

Quy tắc song song với đường image, ⛔ **không được bỏ qua vì "chỉ là chấm điểm"**:

1. Có `vlm_call_ref` và có bằng chứng lời gọi đã xảy ra ⇒ ghi dòng `generation.vlm_scoring_call` với `cost_state = 'unknown'` và `cost_usd = NULL`.
2. ⛔ **`'unknown'` TUYỆT ĐỐI không được gộp thành `0`** — *"chưa biết"* ⛔ **không phải** *"miễn phí"*.
3. Số dòng đó nổi lên báo cáo qua cột `public.usage_daily.vlm_cost_unknown_count`, **báo RIÊNG**, ⛔ không cộng vào `vlm_cost_usd`.
4. ⭐ **Adapter ⛔ KHÔNG tự retry bên trong** — cùng lý do với đường image: mỗi lời gọi VLM thật là **tiền thật**, và retry nội bộ tạo ra tiền tiêu **không có vết**. Retry là thẩm quyền của job queue.

### 5.4 `permanent_policy` — nghĩa vụ ghi nhật ký (`D-67`)

`D-67` (`SRS-NFR-20`) áp cho **cả ba** đường gọi ngoài, ⛔ **không chỉ image provider**.

Đích ghi: **`generation.provider_refusal_log`** với `provider_kind = 'vlm'`, `error_class = 'permanent_policy'`, `provider_error_code` **thô**, `refusal_reason` chuẩn hoá (⛔ không nêu được ⇒ `unspecified_by_provider`).

⚠️ **`model_version` ở đường VLM ⛔ không được `NULL`** — `VS-C7` đã bắt pin tường minh.
⛔ **Không ghi nội dung người dùng thô** vào bảng này (`QA-10`).

### 5.5 Backoff

⛔ File này ⛔ không đặt lại policy. Backoff **luỹ thừa có jitter** qua `run_after`, `max_attempts` mặc định **5** (`[EM]`, ⛔ **không phải chỉ tiêu NFR**) — [ADR-015](../Architecture/ADR-015-Job-Queue-In-Postgres.md) `Q4`. Trần backoff và thời hạn lease: `TBD`, [Spec-Integration-Image-Provider](./Spec-Integration-Image-Provider.md) hàng `IP-T3`.

---

## 6. Chi phí

> [!CAUTION]
> ⭐⭐ **ĐÂY LÀ LÝ DO TỒN TẠI CỦA FILE NÀY.** ⛔ Không được cắt gọn mục này khi trích dẫn.

### 6.1 ⛔ Khoản chi phí đang thiếu — phát biểu chính xác

> ⭐ **Chi phí VLM call để score N candidate là phần CHƯA TÍNH của `CF-3.5`.**
>
> ⇒ **MỌI con số COGS hiện có trong repo — cụ thể `$12,06`/chapter @N=3 — là SÀN, ⛔ KHÔNG PHẢI TRẦN** (`CẤM-04`).
>
> ⛔ **Không được đọc `$12,06` như chi phí thực tế đã đủ.** ⛔ Không được nhân nó ra để suy margin, giá bán hay điểm hoà vốn mà ⛔ không mang kèm nhãn *"sàn — chưa cộng VLM"*. Bỏ nhãn khi nhân một ước lượng là lỗi mà [SRS](../../020-Requirements/SRS-Comic-Studio.md) §1.2 gọi là **"rửa sạch khoảng trống"**.
>
> ⭐ **Con số đúng của khoản thiếu: `TBD` (`VS-T2`).** ⛔ File này ⛔ **KHÔNG ước lượng nó.**

⚠️ **Vì sao khoản này lớn**: nó nhân theo **`N`** và theo **số panel** — tức nhân theo đúng **hai đại lượng lớn nhất** của mô hình chi phí, và nó nằm trên **main path của MỌI panel**.

### 6.2 ⭐ Chi phí VLM đo ở ĐÂU — và VÌ SAO ở đó

| Khoản | Bảng | Đơn vị của một dòng |
|---|---|---|
| ⭐ **Tiền VLM-select** | **`generation.vlm_scoring_call`** (schema `generation`) | ⭐ **MỘT lời gọi provider VLM đã xảy ra** — ⛔ không phải một candidate, ⛔ không phải một điểm chấm |
| Điểm chấm | `generation.vlm_evaluation` | Một candidate trong một lần QA-select |
| ⛔ **KHÔNG ở đây** | `public.usage_event` | Một **image candidate** đã sinh |

⭐ **`generation.vlm_scoring_call` là NGUỒN SỰ THẬT DUY NHẤT của khoản chi phí VLM-select.**

> [!CAUTION]
> ⛔⛔ **VÌ SAO ⛔ KHÔNG nằm trong `public.usage_event` — đây là phần phải hiểu, ⛔ không phải phần phải nhớ:**
>
> **AC đã ký** đo bằng `COUNT(*)` **TRẦN** trên `usage_event` của một panel = **3** — một lần sinh panel best-of-N (N=3) tạo ra **đúng 3** dòng, mỗi dòng ứng với **1 image candidate**.
> ⇒ Thêm **một** dòng VLM cho **cùng panel đó** làm `COUNT(*)` thành **4** ⇒ ⭐ **AC FAIL**.
>
> Đây là **mâu thuẫn thật** giữa *"phải đo được chi phí VLM"* và *"đúng 3 row"*. Hàng `TBD-USAGE-VLM` ([ADR-007](../Architecture/ADR-007-VLM-Provider-For-QA-Select.md) `Q8` · [ADR-018](../Architecture/ADR-018-Usage-Event-And-Rollup-Model.md) · [SDD §9.2 `P-1`](../Architecture/SDD-Comic-Studio.md)) **đã được ĐÓNG** ở [DB-Entity-Provenance-And-Usage](../Schema/DB-Entity-Provenance-And-Usage.md), mục *"Đóng `TBD-USAGE-VLM`"*, bằng **một bảng đo RIÊNG** đặt ở schema `generation` (`E20`).
> ⇒ `public.usage_event` **giữ nguyên là bảng ĐỒNG NHẤT**: ⛔ không cột phân loại, ⛔ không dòng nào không ứng với một image candidate.
>
> ⛔ ***"Không đo" ⛔ KHÔNG phải một lời giải*** — đó chính là cách khoản chi phí này biến mất khỏi mô hình tài chính **LẦN THỨ HAI**.

**Ba cột của bảng mà adapter phải cấp giá trị:**

| Cột | Ràng buộc |
|---|---|
| `idempotency_key` | `{generation_id} : {vlm_call_ref}` — xem [§4.4](#44-idempotency-key--ràng-buộc-được-route-về-file-này) |
| `cost_usd` | **Thực đo** của **chính lời gọi này**. ⚠️ `NULL` ⛔ **không** có nghĩa *"bằng 0"* |
| ⭐ `cost_state` | `'measured'` \| `'unknown'` — `TEXT` + `CHECK`, ⛔ không Postgres enum type. ⛔ **`'unknown'` TUYỆT ĐỐI không gộp thành `0`** |

⚠️ **Bảng này là APPEND-ONLY** (`REVOKE UPDATE, DELETE` khỏi mọi DB role ứng dụng) — ⭐ *"Append-only là ĐIỀU KIỆN để nó dùng được làm căn cứ đối soát."* Một bảng chi phí sửa được thì ⛔ không đối soát được với ai. ⇒ Adapter chỉ `INSERT`, ⛔ không `UPDATE` một dòng đã ghi.

### 6.3 ⭐ Cơ chế chống *"chi phí VLM biến mất"* — nằm ở mặt báo cáo

Cơ chế đó ⛔ **không** nằm ở chỗ *"chung một bảng thô"*. Nó nằm ở **`public.usage_daily`**, nơi ba cột `vlm_*` là **first-class**:

| Cột `usage_daily` | Nguồn | Ý nghĩa |
|---|---|---|
| `vlm_call_count` | `generation.vlm_scoring_call` | Số lời gọi VLM trong ngày |
| `vlm_cost_usd` | `generation.vlm_scoring_call` | Tổng `cost_usd` của các dòng `cost_state = 'measured'` |
| ⭐ `vlm_cost_unknown_count` | `generation.vlm_scoring_call` | Số lời gọi `cost_state = 'unknown'`. ⛔ **Không được gộp vào `vlm_cost_usd` như số 0** |

⇒ ⭐ Khoản chi phí VLM ⛔ **không thể biến mất bằng cách bị quên**: một ngày có `rollup_state = 'complete'` mà `vlm_call_count IS NULL` là **vi phạm invariant** — CI/test bắt được, ⛔ không phải trông vào việc ai đó nhớ viết `JOIN`.

⚠️ **Hệ quả vận hành**: một lần chạy rollup đọc **HAI** bảng thô; **hỏng ở bất kỳ bảng nào** ⇒ ngày đó ⛔ **không được** mang `rollup_state = 'complete'`.

### 6.4 ⛔ Cái gì vẫn CHƯA đo được

| Khoản | Vì sao | Ai đóng | Khi nào |
|---|---|---|---|
| ⭐ **Chi phí VLM per-call** (`VS-T2`) | ⛔ **Không có số nào trong repo**; phụ thuộc `VS-T1` chưa đóng | **PM + Architect** | Sau đo MVP0 |
| **Tổng khoản thiếu của `CF-3.5`** | Là tích của `VS-T2` × `N` × số panel/chapter — cả ba đều chưa chốt | **PM + Architect** | Sau đo MVP0 |
| **Human-reject rate sau VLM-select** (`VS-T4`) | *"Chưa ai công bố con số này"* | **Engineer đo, PM đọc** | MVP0 |
| **N tối thiểu** (`VS-T3`) | `CF-8.5` — một trong ba chỉ số bắt buộc MVP0 phải đo | **PM** | Sau đo MVP0 |

⚠️ ⛔ **Cho tới khi bốn hàng trên đóng, MỌI tài liệu Phase 2 trích số COGS phải mang nhãn *"SÀN"*.**

---

## 7. RIPPLE — những gì file này ⛔ không tự sửa được

| Điểm chạm | Nội dung | Ai xử lý |
|---|---|---|
| `Schema/` (đã đóng) | ⛔ **Nơi lưu chuẩn hoá của `vlm_call_ref` chưa được chỉ định** (`VS-T6`) — song song với `provider_call_ref` của đường image. ⚠️ **`public.job.payload` (`JSONB`) ⛔ KHÔNG mặc nhiên là câu trả lời**: nó bị ràng buộc là ***"tham chiếu tới artifact nghiệp vụ"***, và ⛔ **không có** cột `result`. ⇒ Một quyết định tường minh, ⛔ không phải một giả định | Architect, lô Schema kế tiếp |
| Mô hình tài chính | Mọi con số COGS trong repo hiện **thiếu chi phí VLM** ⇒ cần một lần cập nhật **có nhãn** sau MVP0, ⛔ không phải một lần *"làm tròn"* | PM |
| `Specs-MOC.md` | ⛔ Đang rỗng; `RULE-001` bắt cập nhật index | PM / owner của MOC |

---

## Tài liệu tham khảo

- [ADR-007 — Provider VLM cho QA-select giữa N candidate](../Architecture/ADR-007-VLM-Provider-For-QA-Select.md)
- [ADR-014 — Visual Prompt Compiler deterministic và best-of-N](../Architecture/ADR-014-Deterministic-Prompt-Compiler-And-Best-Of-N.md)
- [ADR-015 — Job queue trong Postgres](../Architecture/ADR-015-Job-Queue-In-Postgres.md)
- [ADR-016 — Adapter image provider và pin model version](../Architecture/ADR-016-Image-Provider-Adapter-And-Version-Pinning.md)
- [ADR-018 — `usage_event` và mô hình rollup](../Architecture/ADR-018-Usage-Event-And-Rollup-Model.md)
- [SDD-Comic-Studio](../Architecture/SDD-Comic-Studio.md) — `P-1`, `P-8`
- [DB-Entity-Provenance-And-Usage](../Schema/DB-Entity-Provenance-And-Usage.md) — `generation.vlm_scoring_call`, `public.usage_daily`
- [DB-Entity-Generation](../Schema/DB-Entity-Generation.md) — `generation.vlm_evaluation`
- [DB-Entity-Quality-Assets](../Schema/DB-Entity-Quality-Assets.md) — `generation.provider_refusal_log`, `generation.golden_dataset_item`
- [Spec-Integration-Image-Provider](./Spec-Integration-Image-Provider.md)
- [SRS-Comic-Studio](../../020-Requirements/SRS-Comic-Studio.md)

---

_Created by system-architect_
_Author: trisjr_
