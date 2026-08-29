---
id: SPEC-INT-IMAGE-PROVIDER
type: spec
status: draft
project: comic-studio
created: 2026-08-29
---

# Spec-Integration-Image-Provider — adapter provider sinh ảnh

Related to: [ADR-016](../Architecture/ADR-016-Image-Provider-Adapter-And-Version-Pinning.md) · [ADR-014](../Architecture/ADR-014-Deterministic-Prompt-Compiler-And-Best-Of-N.md) · [ADR-015](../Architecture/ADR-015-Job-Queue-In-Postgres.md) · [ADR-018](../Architecture/ADR-018-Usage-Event-And-Rollup-Model.md) · [SDD](../Architecture/SDD-Comic-Studio.md)

> [!IMPORTANT]
> ⭐ **VLM QA-select là integration RIÊNG, ⛔ KHÔNG phải một hàm của adapter này** — xem [Spec-Integration-VLM-QA-Select](./Spec-Integration-VLM-QA-Select.md).
> Gộp hai file làm **che mất** chuyện chi phí VLM chưa được cộng vào bất kỳ con số COGS nào ([ADR-007](../Architecture/ADR-007-VLM-Provider-For-QA-Select.md) `Q1`, Alternatives `(a)`).

---

## 1. Mục đích

File này đóng hàng `P-8` của [SDD §9.2](../Architecture/SDD-Comic-Studio.md) — *"retry / backoff policy + error taxonomy per provider"* — cho **đường gọi image provider**, và đặc tả **hình dạng hợp đồng** mà [ADR-016](../Architecture/ADR-016-Image-Provider-Adapter-And-Version-Pinning.md) `Q1` cố ý để lại cho tầng này.

Ba việc file này làm:

1. Ghi lại **seam đã CHỐT** dưới dạng hợp đồng gọi được — ⛔ không mở lại quyết định nào của [ADR-016](../Architecture/ADR-016-Image-Provider-Adapter-And-Version-Pinning.md).
2. **Phân loại lỗi provider** thành đúng năm lớp lỗi mà [ADR-015](../Architecture/ADR-015-Job-Queue-In-Postgres.md) `Q5` đã định nghĩa — adapter **phân loại**, job queue **quyết định**.
3. Nói rõ **tiền đi đâu**: `cost_usd` thực đo nằm ở đâu, và ⛔ **cái gì vẫn chưa đo được**.

⛔ **File này KHÔNG chọn vendor mới, ⛔ không nới version pinning, ⛔ không đặc tả DDL** (`Architecture/`, `Schema/` đã đóng).

---

## 2. Cái gì đã CHỐT

### 2.1 Seam — ⛔ không mở lại

| # | Nội dung | Mã | Nguồn |
|--:|---|:--:|---|
| `IP-C1` | **Một interface, nhiều provider.** ⛔ **Không một dòng code nghiệp vụ nào gọi thẳng SDK provider.** Mọi lời gọi nằm trong module adapter | `D-40` | `SRS-FR-23` · [ADR-016](../Architecture/ADR-016-Image-Provider-Adapter-And-Version-Pinning.md) `Q1` |
| `IP-C2` | **Phép đo của seam (AC đã ký)**: đổi Gemini → FLUX.2 chỉ thay **implementation** của adapter; ⛔ không sửa compiler / queue / business logic. Nghiệm thu bằng adapter thứ hai (test/dummy) | `D-40` | [ADR-016](../Architecture/ADR-016-Image-Provider-Adapter-And-Version-Pinning.md) `Q1` |
| `IP-C3` | **Pin `model_version` TƯỜNG MINH trong config.** ⛔ Không chuỗi rỗng, ⛔ không `latest`, ⛔ không alias của provider. ⚠️ **Ràng buộc cứng — ⛔ không nới** | `D-40` | `SRS-FR-23` · [ADR-016](../Architecture/ADR-016-Image-Provider-Adapter-And-Version-Pinning.md) `Q2` |
| `IP-C4` | **`model_id` ghi là model THỰC SỰ ĐƯỢC GỌI**, ⛔ không phải model dự kiến. Provider tự fallback giữa chừng ⇒ ghi model thật | `D-40` + `D-59` | [ADR-016](../Architecture/ADR-016-Image-Provider-Adapter-And-Version-Pinning.md) `Q1` · [DB-Entity-Generation](../Schema/DB-Entity-Generation.md) |
| `IP-C5` | **`model_version` khác nhau dưới cùng `model_id` ghi RIÊNG BIỆT, ⛔ không ghi đè** — dữ liệu để truy vết **silent model drift** | `D-59` | `SRS-FR-31` · [ADR-016](../Architecture/ADR-016-Image-Provider-Adapter-And-Version-Pinning.md) `Q2` |
| `IP-C6` | **Batch API là chế độ gọi MẶC ĐỊNH**, ⛔ không realtime. Chế độ gọi là **thuộc tính cấu hình được của adapter**, ⛔ không hardcode | `D-41` | `SRS-FR-24` · [ADR-016](../Architecture/ADR-016-Image-Provider-Adapter-And-Version-Pinning.md) `Q3` |
| `IP-C7` | Adapter nhận **MỘT ĐƠN VỊ RENDER** (một hoặc nhiều panel spec đã compile). ⛔ **Không giả định đơn vị đó luôn là "đúng một panel"** | `D-46` | `SRS-FR-33` · `SRS-FR-07` · [ADR-016](../Architecture/ADR-016-Image-Provider-Adapter-And-Version-Pinning.md) `Q4` |
| `IP-C8` | **MVP0 có đúng MỘT adapter cố định.** ⛔ Không multi-provider fallback tự động trong cùng một lần chạy; ⛔ không tự chọn provider theo giá thấp nhất ở runtime | `D-40` | [ADR-016](../Architecture/ADR-016-Image-Provider-Adapter-And-Version-Pinning.md) `Q5`, Alternatives `(b)`, `(c)` |
| `IP-C9` | ⛔ **Không mua GPU** — API cho main path; self-host **chỉ** cho LoRA train / upscale / inpainting | `D-07` | `SRS-NFR-11` |

> [!CAUTION]
> ⚠️ **`IP-C7` là hình thức của SEAM ÂM `S-5`** ([SDD §8.1](../Architecture/SDD-Comic-Studio.md)): chừa chỗ ở đây nghĩa là ⛔ **KHÔNG SIẾT** — một adapter viết cứng theo giả định *"đúng một panel"* là **đóng đường lui của gate `G2`** một cách im lặng, và ⛔ không có gì trong repo để nhìn thấy nó.

### 2.2 Provider mặc định và đường lui — ⛔ dùng đúng, ⛔ không tự đổi

| Hạng mục | Giá trị | Nhãn |
|---|---|:--:|
| **Provider MẶC ĐỊNH** | **Gemini 3 Pro Image**, gọi qua **batch API** | `MẶC ĐỊNH` |
| **Đường lui đã ghi rõ** | **FLUX.2 pro** — `$0.03` | `[OFF]` |
| Chế độ gọi đường lui ngân sách | **standard** (`CF-3.11` lấy giá standard làm **trần an toàn** MVP0) | `[OFF]` |
| Đường lui granularity | **whole-page** — dùng khi gate `G2` ⛔ không PASS, ⛔ **không đổi data model** | `D-46` |
| ⛔ **CẤM** | Hạ **N** từ 3 xuống 1 để cứu margin | `CF-10.7` · `CẤM-03` |

⚠️ **Đổi provider là quyết định VẬN HÀNH có người bấm nút**, ⛔ không phải logic runtime ([ADR-016](../Architecture/ADR-016-Image-Provider-Adapter-And-Version-Pinning.md) `Q5`).

### 2.3 Ba đường ⛔ CẤM

| ⛔ Cấm | Neo | Cưỡng chế bằng |
|---|---|---|
| ⭐ Gọi **dịch vụ copyright / plagiarism / similarity detection** từ adapter này | `D-53` · **`SRS-NFR-15`** | ⚠️ **ANTI-FEATURE có chủ ý** — nó tạo ra đúng tri thức mà điều kiện *"không biết"* của miễn trừ **Điều 198b** đang miễn trừ. Đây là chỗ *"một dev sẽ làm ngược theo bản năng"*. Review code + review cấu hình adapter |
| Dùng **`latest`** hoặc alias provider thay cho version pin | `D-40` · `D-66` | Test cấu hình: khởi động fail nếu `model_version` rỗng / bằng `latest` |
| **Adapter tự retry bên trong** một lời gọi provider | `D-59` · [ADR-015](../Architecture/ADR-015-Job-Queue-In-Postgres.md) `Q4.1` | Xem [§5.4](#54-adapter--không-tự-retry-bên-trong) — đây là đường **đốt tiền không có vết** |

---

## 3. Cái gì còn MỞ

⛔ **Không hàng nào dưới đây được điền bằng suy đoán.** [SRS](../../020-Requirements/SRS-Comic-Studio.md) §5.2: *"Bịa một con số performance là lỗi nghiêm trọng hơn để trống nó."*

| Mã | `TBD` | Ai đóng | Khi nào |
|---|---|---|---|
| `IP-T1` | **Bảng ánh xạ mã lỗi thô của Gemini 3 Pro Image → năm lớp lỗi** ([§5.2](#52-năm-lớp-lỗi--adapter-phân-loại-job-queue-quyết-định)). ⛔ File này chốt **quy tắc phân loại**, ⛔ không bịa mã lỗi chưa verify được | Engineer | Khi viết adapter đầu tiên, đối chiếu tài liệu provider **thật** |
| `IP-T2` | **Cơ chế lưu `provider_call_ref`** sao cho bền qua retry ([§4.4](#44-idempotency-key--ràng-buộc-được-route-về-file-này)) — cột / bảng / khoá | Architect (lô Schema kế tiếp) + Engineer | Trước khi adapter đầu tiên chạy. ⚠️ `Schema/` hiện đã đóng ⇒ xem [RIPPLE](#7-ripple--những-gì-file-này--không-tự-sửa-được) |
| `IP-T3` | **Trần backoff** cụ thể và **thời hạn lease** — phụ thuộc thời gian sinh panel p50/p95 mà `SRS` §5.2 cấm gán số | Architect + Engineer | Sau khi MVP0 đo thời gian sinh panel thật |
| `IP-T4` | **Ngưỡng rate limit** đi kèm `D-67` | PM + Architect | Sau đo tải |
| `IP-T5` | **Ngưỡng định lượng kích hoạt từng bậc đường lui** (`CF-3.11` / whole-page / FLUX.2) | PM | Tại gate `G2`, sau MVP1 |
| `IP-T6` | **N tối thiểu** (`CF-8.5`). ⚠️ **Budget vẫn phải tính ở N=3**; ⛔ đổi N ⇒ **chạy lại `G1`** (`CẤM-03`) | PM | Sau đo MVP0 |
| `IP-T7` | **Cơ chế lưu / mã hoá / thu hồi credential theo tenant** (BYOK — seam `S-4`). ⚠️ File này chốt **chỗ cắm**, ⛔ không chốt cơ chế bảo vệ key | **Architect + Founder** — hàng `T-27` của [SDD §9.1](../Architecture/SDD-Comic-Studio.md) | Trước MVP4. ⚠️ **Đóng đúng nghĩa cần một ADR MỚI ⇒ ⛔ ngoài phạm vi run Phase 2 này** ⇒ mang theo như **nợ kỹ thuật**, ⛔ không coi là đã đóng |
| `IP-T8` | **Thời hạn signed URL** cho artifact ảnh | **Dev đề xuất, Founder duyệt** (theo [ADR-004](../Architecture/ADR-004-Object-Storage-Vendor-And-Signed-URL.md)) | [ADR-004](../Architecture/ADR-004-Object-Storage-Vendor-And-Signed-URL.md) — ⛔ ngoài phạm vi file này |

---

## 4. Interface / seam

### 4.1 Input — hai output của compiler, ⛔ không gộp chuỗi

| Trường | Nguồn | Ràng buộc |
|---|---|---|
| `render_unit` | `generation.prompt_compilation.render_unit_kind` | `'panel'` (mặc định) \| `'page'` (đường lui `G2`). ⭐ Adapter **phải xử lý được cả hai** (`IP-C7`) |
| `text_prompt` | `generation.prompt_compilation.text_prompt` | Output **thứ nhất** của compiler: mô tả cảnh |
| ⭐ `conditioning_set` | `generation.prompt_compilation.conditioning_set` | Output **thứ hai**: identity reference **và prop quan trọng**, mỗi phần tử `{entity_id, object_key, sha256}`. ⛔ **Không được cạnh tranh với `text_prompt` trong cùng một chuỗi** (`D-35`, `SRS-FR-18`); prop là **ENTITY RIÊNG**, ⛔ không mô tả bằng chữ (`D-43`, `SRS-FR-27`) |
| `negative_prompt` | `generation.prompt_compilation.negative_prompt` | Đi thẳng vào lời gọi provider, ⛔ không nối vào `text_prompt` |
| `model_id` · `model_version` | Config adapter | ⛔ Pin tường minh (`IP-C3`) |
| `call_mode` | Config adapter | `batch` (mặc định) \| `standard`. ⛔ Đổi chế độ ⛔ **không** kéo theo thay đổi data model (`IP-C6`) |
| ⭐ `tenant_credential` | Tham số **ở chữ ký hàm** | ⭐ **Adapter nhận credential THEO TENANT ở chữ ký hàm, ⛔ không đọc thẳng biến môi trường toàn cục** — [SDD §8.2 `S-4`](../Architecture/SDD-Comic-Studio.md) route ràng buộc này đích danh về file này |

⚠️ **Reference image đi vào adapter bằng `object_key`, ⛔ KHÔNG BAO GIỜ bằng blob** — quy tắc `B-4`, key dạng `tenant/{tenant_id}/{sha256}`.

### 4.2 Output — hợp lệ

| Trường | Đích ghi | Ràng buộc |
|---|---|---|
| `image_object_key` | `generation.generation.image_object_key` | Key object storage. ⛔ Không bytes trong DB |
| `model_id` · `model_version` | `generation.generation` | Model **thực sự được gọi** (`IP-C4`, `IP-C5`) |
| ⭐ `cost_usd` | `generation.generation.cost_usd` | ⭐ **THỰC ĐO tại thời điểm hoàn tất**, ⛔ **không phải ước lượng trước khi gọi** (`D-59`) |
| ⭐ `cost_status` | `generation.generation.cost_status` | `'measured'` \| `'unknown_provider_error'` — `TEXT` + `CHECK`, ⛔ **không** Postgres enum type (`E15`). ⛔ Không `NULL` âm thầm, ⛔ không `0` ngầm định |
| `attempt_no` | `generation.generation.attempt_no` | Số thứ tự lần gọi trong **cùng một logical generation request**. ⚠️ ⛔ **KHÔNG phải `public.job.attempt_count`** |
| `provider_call_ref` | Xem [§4.4](#44-idempotency-key--ràng-buộc-được-route-về-file-này) | Định danh **một lời gọi provider thực tế** |
| `seed` | `generation.generation.seed` | ⭐ **PROVENANCE METADATA, ⛔ KHÔNG PHẢI REPLAY KEY** (`D-44`). `NULL` hợp lệ — nhiều API ⛔ không cho set seed |

⚠️ **Mỗi candidate của best-of-N là MỘT dòng `generation.generation` riêng với `generation_kind = 'candidate'`** — ⛔ không gộp, ⛔ không ghi đè lẫn nhau (hợp đồng #7 của [ADR-014](../Architecture/ADR-014-Deterministic-Prompt-Compiler-And-Best-Of-N.md); phán quyết `CO-1.1` / `E17`).

### 4.3 Output — lỗi

Adapter **trả về lớp lỗi đã phân loại**, ⛔ **không để lỗi rơi tự do làm crash caller**. Hình dạng trả về:

| Trường | Nội dung |
|---|---|
| `error_class` | Đúng **một** trong năm lớp của [§5.2](#52-năm-lớp-lỗi--adapter-phân-loại-job-queue-quyết-định) |
| `provider_error_code` | ⭐ Mã lỗi **thô** do provider trả, **giữ nguyên** — ⛔ không diễn giải lại |
| `error_detail` | Mô tả ngắn cho chẩn đoán. ⛔ **Không chứa secret**, ⛔ không chứa nội dung người dùng thô |
| `refusal_reason` | ⭐ Chỉ khi `error_class = 'permanent_policy'`. Provider ⛔ không nêu lý do ⇒ ghi **tường minh** `unspecified_by_provider`, ⛔ không để trống, ⛔ không `NULL` âm thầm |

### 4.4 Idempotency key — ràng buộc được route về file này

[DB-Entity-Provenance-And-Usage](../Schema/DB-Entity-Provenance-And-Usage.md) chốt hình dạng và **route phần còn lại về đúng file này**:

```
idempotency_key = {generation_id} : {provider_call_ref}
```

> **Quy tắc `IK-1`** (nhắc lại, ⛔ không diễn giải lại): key định danh **một lần TIÊU TÀI NGUYÊN THỰC**, ⛔ **không phải một lần GỬI**.

⭐ **Nghĩa vụ của adapter — và đây là phần file này phải nói:**

1. `provider_call_ref` do **adapter** cấp, **một lần cho mỗi lời gọi provider thực tế** — adapter là nơi **duy nhất** biết một lời gọi đã thực sự xảy ra.
2. ⭐ **`provider_call_ref` phải BỀN QUA RETRY**: sinh **TRƯỚC** lời gọi, lưu **cùng** kết quả. ⛔ **Không được sinh lại ở mỗi lần worker nhặt job.**
3. Worker retry **chuyển tiếp cùng một lời gọi** ⇒ cùng `ref` ⇒ cùng key ⇒ `UNIQUE (tenant_id, idempotency_key)` từ chối dòng thứ hai. Một lời gọi **MỚI** ⇒ `ref` mới ⇒ dòng mới — **đúng**, vì tài nguyên đã tiêu thêm một lần.

⚠️ **Cơ chế lưu cụ thể của `ref` = `IP-T2`.** ⛔ File này ⛔ không tự thêm cột — `Schema/` đã đóng.
⚠️ ⛔ **Đây không phải tối ưu.** [ADR-015](../Architecture/ADR-015-Job-Queue-In-Postgres.md) `Q4.3` chốt job queue là **at-least-once**: một job **sẽ** chạy lại. ⛔ Không có key thì mỗi lần chạy lại là một lần **đếm phồng chi phí**, và số phồng đó đi thẳng vào gate `G2`.

### 4.5 Ranh giới transaction

⛔ **Lời gọi provider phải HOÀN TẤT TRƯỚC khi mở transaction ghi.** ⛔ Không giữ transaction mở trong lúc chờ mạng — `KC-4` (`D-50`, `SRS-NFR-13`) bắt provenance commit **cùng một transaction** với artifact, và một lời gọi mạng nằm giữa transaction đó phá cả hai ràng buộc cùng lúc ([SDD §8.2 `S-3`](../Architecture/SDD-Comic-Studio.md) nêu đúng lớp lỗi này).

⇒ Trạng thái *"đã gọi xong nhưng chưa ghi"* là trạng thái **thật** và phải xử lý **tường minh** — đó chính là lý do `provider_call_ref` phải bền (`§4.4` điều 2).

---

## 5. Retry & error taxonomy

### 5.1 Đường phân chia trách nhiệm — ⛔ không nhập nhằng

> ⭐ **Adapter PHÂN LOẠI lỗi của provider. Job queue QUYẾT ĐỊNH làm gì với lớp đó.**
> [ADR-015](../Architecture/ADR-015-Job-Queue-In-Postgres.md) `Q7` phát biểu nguyên đường phân chia này; file này chỉ đặc tả **vế phân loại**.

### 5.2 Năm lớp lỗi — adapter phân loại, job queue quyết định

Năm lớp dưới đây là **danh sách đóng của [ADR-015](../Architecture/ADR-015-Job-Queue-In-Postgres.md) `Q5`** — ⛔ file này ⛔ không thêm lớp thứ sáu.

| `error_class` | Quy tắc phân loại **ở đường image provider** | Job queue làm gì |
|---|---|:--|
| `transient_infra` | Lỗi xảy ra **trước khi request rời tiến trình**: DB timeout, deadlock, mất kết nối nội bộ | ✅ Retry + backoff. ⛔ **Không** phát sinh dòng `candidate` / `cost_usd` mới **nếu chưa gọi provider** |
| `transient_provider` | Provider **timeout**, **rate limit**, lỗi tạm thời phía provider (họ tự tuyên bố là retryable), lỗi mạng **sau khi** request đã rời tiến trình | ✅ Retry + backoff. ⚠️ Xem [§5.3](#53-lỗi-sau-khi-đã-gọi--vấn-đề-tiền-đã-tiêu) |
| `permanent_input` | Payload sai, `conditioning_set` trỏ artifact **đã bị xoá**, ảnh reference ⛔ không đọc được, model_id/version cấu hình ⛔ không tồn tại | ⛔ **Không** retry ⇒ job `failed_permanent` |
| ⭐ `permanent_policy` | Provider **từ chối vì content policy** | ⛔ **Không** retry ⇒ `failed_permanent`. ⭐ **BẮT BUỘC ghi `generation.provider_refusal_log`** — xem [§5.5](#55-permanent_policy--nghĩa-vụ-ghi-nhật-ký-d-67) |
| `permanent_unknown` | ⛔ **Chưa phân loại được** | ⛔ Không retry; ⚠️ **phải xuất hiện được trong chẩn đoán**, ⛔ không im lặng |

⚠️ **`permanent_unknown` là lớp HỢP LỆ, ⛔ không phải chỗ để nhét mọi thứ chưa buồn đọc.** Một mã lỗi rơi vào đây là **tín hiệu** rằng `IP-T1` còn thiếu một hàng, ⛔ không phải một kết cục chấp nhận được lâu dài.

> [!WARNING]
> ⛔ **File này KHÔNG liệt kê mã lỗi thô của Gemini 3 Pro Image.** Danh sách mã lỗi cụ thể phải đối chiếu **tài liệu provider thật** tại thời điểm viết adapter — bịa ra một bảng mã không verify được là đúng lớp lỗi mà [SRS](../../020-Requirements/SRS-Comic-Studio.md) §5.2 cấm. ⇒ Hàng `IP-T1`, **Engineer đóng**.
> Cái file này chốt là **quy tắc phân loại** ở cột giữa — đủ để viết adapter, đủ để review một bảng ánh xạ khi nó xuất hiện.

### 5.3 Lỗi SAU khi đã gọi — vấn đề "tiền đã tiêu"

⚠️ **Một lỗi `transient_provider` xảy ra SAU khi request đã rời tiến trình ⛔ KHÔNG chứng minh rằng provider chưa tính tiền.**

Quy tắc bắt buộc:

1. Nếu adapter **có** `provider_call_ref` và **có** bằng chứng lời gọi đã xảy ra ⇒ ghi dòng `candidate` với `cost_status = 'unknown_provider_error'` và `cost_usd = NULL`. ⛔ **Không** ghi `0`.
2. ⛔ **`'unknown_provider_error'` TUYỆT ĐỐI không được gộp thành `0`** — *"chưa biết"* ⛔ không phải *"miễn phí"*.
3. Rollup **bắt buộc lọc** `WHERE generation_kind = 'candidate' AND cost_status = 'measured'` và **báo riêng** số dòng `unknown_provider_error` — ⛔ không được để chúng biến mất khỏi báo cáo ([DB-Entity-Generation](../Schema/DB-Entity-Generation.md) `G-5`).
4. Retry sau đó là **lời gọi MỚI** ⇒ `provider_call_ref` mới ⇒ `attempt_no` mới ⇒ dòng `candidate` mới. **Đúng** — vì tài nguyên có thể đã tiêu hai lần thật.

### 5.4 Adapter ⛔ KHÔNG tự retry bên trong

> [!CAUTION]
> ⛔⛔ **Adapter ⛔ KHÔNG được tự retry một lời gọi provider bên trong chính nó.**
> **Lý do**: mỗi lời gọi provider thật có `cost_usd` thật (`D-59`). Retry nội bộ tạo ra **N lần tiêu tiền** nhưng chỉ **một** giá trị trả về ⇒ `attempt_no`, `cost_usd`, `usage_event` chỉ ghi được **một** lần ⇒ phần còn lại là **tiền tiêu không có vết**. Đó là **đúng con số** mà gate `G2` dựa vào.
> ⇒ Retry là **thẩm quyền của job queue** ([ADR-015](../Architecture/ADR-015-Job-Queue-In-Postgres.md) `Q4`), vì chỉ ở đó mỗi lần thử mới sinh ra một `attempt_no` và một dòng chi phí tương ứng.

**Ngoại lệ duy nhất được phép**: retry ở tầng **transport** cho lỗi xảy ra **trước khi request rời tiến trình** (ví dụ mở kết nối thất bại) — vì ⛔ chưa có lời gọi nào, ⛔ chưa có tiền nào tiêu. Lớp này là `transient_infra`.

### 5.5 `permanent_policy` — nghĩa vụ ghi nhật ký (`D-67`)

`D-67` (`SRS-NFR-20`) bắt **ghi lại MỌI lần provider từ chối vì content policy** — ⛔ không được nuốt lỗi này.

Đích ghi: **`generation.provider_refusal_log`** ([DB-Entity-Quality-Assets](../Schema/DB-Entity-Quality-Assets.md)), với `provider_kind = 'image'`.

| Cột | Adapter cấp giá trị nào |
|---|---|
| `provider_kind` | `'image'` |
| `provider_id` | Định danh provider/adapter đã trả về từ chối |
| `model_id` · `model_version` | Model đang gọi khi bị từ chối. ⚠️ Đường image **đã bắt pin** (`IP-C3`) ⇒ `model_version` ⛔ không được `NULL` ở đường này |
| `error_class` | `'permanent_policy'` — cột này có `CHECK (error_class = 'permanent_policy')` |
| `provider_error_code` | Mã **thô**, ⛔ giữ nguyên |
| `refusal_reason` | Lý do đã chuẩn hoá; ⛔ không nêu được ⇒ `unspecified_by_provider` |
| `job_id` · `generation_id` | Tham chiếu **mềm**, ⛔ **KHÔNG FK**. `NULL` hợp lệ khi từ chối xảy ra trước khi có dòng tương ứng |

> [!WARNING]
> ⛔ **Adapter ⛔ KHÔNG được ghi nội dung người dùng thô vào bảng này** — ⛔ không prompt đã gửi, ⛔ không đoạn văn nguồn, ⛔ không tên nhân vật (`QA-10`). Đó chính là thứ giữ cho mệnh đề *"cụm này không bị takedown chạm tới"* **đúng**, thay vì chỉ là một mong muốn.

### 5.6 Backoff — tham số do job queue sở hữu

⛔ File này ⛔ **không đặt lại** policy backoff. Nhắc lại để adapter ⛔ không tự làm trùng:

| Tham số | Giá trị | Nhãn |
|---|---|:--:|
| Chiến lược | Luỹ thừa cơ số 2, **có jitter** (chống thundering herd) | [ADR-015](../Architecture/ADR-015-Job-Queue-In-Postgres.md) `Q4.2` |
| `max_attempts` mặc định | **5** | `[EM]` — lựa chọn tầng design, ⛔ **không phải chỉ tiêu NFR** |
| Hiện thực | `run_after = now() + backoff(attempt_count)` rồi **nhả job ra** — worker ⛔ không ngủ chờ | [ADR-015](../Architecture/ADR-015-Job-Queue-In-Postgres.md) `Q4.2` |
| Trần backoff · thời hạn lease | ⛔ **`TBD`** — `IP-T3` | `SRS` §5.2 cấm gán số |

---

## 6. Chi phí

### 6.1 ⛔ Nhãn bắt buộc mang theo mọi con số dưới đây

> [!CAUTION]
> ⭐ **MỌI con số chi phí trong file này là SÀN.**
> Chi phí VLM call để score N candidate là phần **CHƯA TÍNH** của `CF-3.5` ⇒ **`$12,06`/chapter @N=3 là SÀN, ⛔ KHÔNG phải trần** (`CẤM-04`).
> ⛔ **Không được** nhân con số này ra để suy margin, giá bán hay điểm hoà vốn mà ⛔ không mang kèm nhãn *"sàn — chưa cộng VLM"*. Bỏ nhãn khi nhân một ước lượng là lỗi mà [SRS](../../020-Requirements/SRS-Comic-Studio.md) §1.2 gọi là **"rửa sạch khoảng trống"**.
> ⇒ Khoản thiếu được đo ở đâu và ai đóng: xem [Spec-Integration-VLM-QA-Select §6](./Spec-Integration-VLM-QA-Select.md).

### 6.2 Giá tham chiếu — tất cả đều `[OFF]`

| Hạng mục | Giá | Nhãn |
|---|---|:--:|
| Gemini 3 Pro Image — standard | `$0.134` | `[OFF]` `CF-3.4` |
| Gemini 3 Pro Image — batch | `$0.067` | `[OFF]` `CF-3.4` |
| FLUX.2 pro (đường lui) | `$0.03` | `[OFF]` |
| Trần chi phí MVP0 | **~$12** (giá standard) · ~$6 nếu batch — ⭐ **lấy số cao làm trần an toàn** | `[EM tính từ OFF]` `CF-3.11` |

⚠️ **Bốn hàng trên là giá tham chiếu tại thời điểm Phase 1, ⛔ không phải cam kết của provider.** `cost_usd` ghi vào DB là **thực đo**, ⛔ không phải các số này (`D-59`).

### 6.3 Tiền nằm ở đâu — một nguồn sự thật, ⛔ không hai

| Khoản | Bảng | Cột | Ghi chú |
|---|---|---|---|
| ⭐ **Chi phí sinh ảnh** | `generation.generation` | `cost_usd` + `cost_status` | ⭐ **Nguồn sự thật DUY NHẤT** của tiền ảnh |
| Sự kiện tiêu tài nguyên | `public.usage_event` | `cost_state = 'carried_by_generation'` | ⭐ **Đúng một giá trị hợp lệ** — chi phí ảnh là của `generation.generation.cost_usd`, ⛔ **không** của dòng này. `cost_usd` ở bảng đó **luôn `NULL`** |
| ⛔ **Chi phí VLM** | `generation.vlm_scoring_call` | — | ⛔ **KHÔNG** thuộc phạm vi file này |

⭐ **`public.usage_event` là bảng ĐỒNG NHẤT: một dòng = MỘT image candidate đã sinh.** ⛔ Không cột phân loại, ⛔ không dòng nào không ứng với một candidate (`E20`).

> [!WARNING]
> ⛔⛔ **Adapter ⛔ TUYỆT ĐỐI KHÔNG được thêm một loại dòng mới vào `public.usage_event`.**
> AC đã ký đo bằng `COUNT(*)` **trần** trên `usage_event` của một panel = **3** (một dòng = một image candidate). Thêm bất kỳ dòng nào khác ⇒ **AC FAIL** và phép cộng COGS **đếm đôi**.
> `CHECK (cost_state = 'carried_by_generation')` làm việc thêm đó **thất bại ồn ào** ở migration — ⛔ đó là guardrail, ⛔ không phải cột thừa ([DB-Entity-Provenance-And-Usage](../Schema/DB-Entity-Provenance-And-Usage.md) `INV-UE-3`).

### 6.4 ⛔ Cái gì vẫn CHƯA đo được ở đường này

| Khoản chưa đo | Vì sao | Ai đóng | Khi nào |
|---|---|---|---|
| ⭐ **Chi phí VLM per-call** và tổng khoản thiếu của `CF-3.5` | ⛔ **Không có số nào trong repo** | PM + Architect | Sau đo MVP0 — [ADR-007](../Architecture/ADR-007-VLM-Provider-For-QA-Select.md) sở hữu hàng này |
| **Chi phí LLM** cho 5 việc | [ADR-008](../Architecture/ADR-008-LLM-Provider-And-Usage-Boundaries.md) tuyên bố **chưa xác định**; ⛔ không route về `usage_event` | PM | Khi cập nhật mô hình tài chính sau MVP0 |
| **Số dòng `unknown_provider_error`** thành tiền | Theo định nghĩa là *"chưa biết"* | — | ⭐ ⛔ **Không bao giờ** được quy thành `0`; báo **riêng** |
| **Định nghĩa số học của regen ratio** (tử/mẫu/đơn vị quan sát) | ⛔ Không nguồn nào trong repo định nghĩa | PM (định nghĩa metric) + Engineer (đo MVP0) | MVP0 |

⚠️ **Chi phí trên key của tenant BYOK phải PHÂN BIỆT ĐƯỢC** với chi phí trên key của ta ngay từ dòng đầu tiên — dữ liệu lịch sử ⛔ **không backfill được** (`SRS-FR-31`). Cơ chế phân biệt: hàng `IP-T7` + [RIPPLE](#7-ripple--những-gì-file-này--không-tự-sửa-được).

---

## 7. RIPPLE — những gì file này ⛔ không tự sửa được

| Điểm chạm | Nội dung | Ai xử lý |
|---|---|---|
| `Schema/` (đã đóng) | ⛔ **Nơi lưu chuẩn hoá của `provider_call_ref` chưa được chỉ định** (`IP-T2`). `idempotency_key` là **dẫn xuất** của nó, nhưng nơi giữ chính `ref` giữa hai lần worker nhặt job thì chưa file schema nào nói. ⚠️ **`public.job.payload` (`JSONB`) ⛔ KHÔNG mặc nhiên là câu trả lời** — nó bị ràng buộc là ***"tham chiếu tới artifact nghiệp vụ"*** và ⛔ *"không nhét dữ liệu nghiệp vụ vào đây"*; ⛔ **không có** cột `result`. ⇒ Cần một quyết định tường minh, ⛔ không phải một giả định | Architect, lô Schema kế tiếp |
| `Schema/` (đã đóng) | ⛔ **Chưa có cột phân biệt chi phí BYOK** trên `generation.generation` (seam `S-4`) — chỉ là **cảnh báo**, ⛔ không phải yêu cầu thêm cột ngay ở MVP0 | Architect, khi `S-4` được mở |
| `Specs-MOC.md` | ⛔ Đang rỗng; `RULE-001` bắt cập nhật index cho ba file `Spec-Integration-*` | PM / owner của MOC |

---

## Tài liệu tham khảo

- [ADR-016 — Adapter image provider và pin model version](../Architecture/ADR-016-Image-Provider-Adapter-And-Version-Pinning.md)
- [ADR-014 — Visual Prompt Compiler deterministic và best-of-N](../Architecture/ADR-014-Deterministic-Prompt-Compiler-And-Best-Of-N.md)
- [ADR-015 — Job queue trong Postgres](../Architecture/ADR-015-Job-Queue-In-Postgres.md)
- [ADR-018 — `usage_event` và mô hình rollup](../Architecture/ADR-018-Usage-Event-And-Rollup-Model.md)
- [ADR-007 — Provider VLM cho QA-select](../Architecture/ADR-007-VLM-Provider-For-QA-Select.md)
- [SDD-Comic-Studio](../Architecture/SDD-Comic-Studio.md) — `P-8`, seam `S-4`, `S-5`
- [DB-Entity-Generation](../Schema/DB-Entity-Generation.md)
- [DB-Entity-Provenance-And-Usage](../Schema/DB-Entity-Provenance-And-Usage.md)
- [DB-Entity-Quality-Assets](../Schema/DB-Entity-Quality-Assets.md)
- [SRS-Comic-Studio](../../020-Requirements/SRS-Comic-Studio.md) — nguồn của mọi mã `SRS-FR-*` / `SRS-NFR-*`

---

_Created by system-architect_
_Author: trisjr_
