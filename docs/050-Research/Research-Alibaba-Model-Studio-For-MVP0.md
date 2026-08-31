---
id: RESEARCH-ALIBABA-MODEL-STUDIO-MVP0
type: research
status: draft
project: comic-studio
owner: "@trisjr"
tags: [mvp0, provider, alibaba, qwen, dashscope]
created: 2026-08-31
---

# Research — Alibaba Cloud Model Studio cho hai vai trò provider của MVP0

> Xác minh năng lực **Alibaba Cloud Model Studio** (DashScope) cho hai vai trò provider vận hành của MVP0 — sinh ảnh có reference và VLM QA-select — làm căn cứ cho quyết định đổi provider vận hành ngày `2026-08-31`.
>
> ⚠️ **Đây là căn cứ cho LỰA CHỌN VẬN HÀNH, ⛔ không phải căn cứ chốt vendor.** Việc chốt vendor thật vẫn nằm ở gate cuối MVP0 theo [ADR-007](../030-Specs/Architecture/ADR-007-VLM-Provider-For-QA-Select.md) `Q4`, với 5 tiêu chí `Q5`.

## Mục lục

- [Phương pháp và giới hạn xác minh](#phương-pháp-và-giới-hạn-xác-minh)
- [1. Vai trò sinh ảnh — reference image là điều kiện cứng](#1-vai-trò-sinh-ảnh--reference-image-là-điều-kiện-cứng)
- [2. Vai trò VLM QA-select — đối chiếu 5 tiêu chí ADR-007 Q5](#2-vai-trò-vlm-qa-select--đối-chiếu-5-tiêu-chí-adr-007-q5)
- [3. Cơ chế API](#3-cơ-chế-api)
- [4. Giá — trạng thái xác minh](#4-giá--trạng-thái-xác-minh)
- [5. Account, region và free quota](#5-account-region-và-free-quota)
- [6. Content moderation — rủi ro mở lớn nhất](#6-content-moderation--rủi-ro-mở-lớn-nhất)
- [Kết luận](#kết-luận)
- [Tài liệu tham khảo](#tài-liệu-tham-khảo)

## Phương pháp và giới hạn xác minh

Nghiên cứu thực hiện `2026-08-31` trên tài liệu chính thức `alibabacloud.com/help/en/model-studio/*`. **Giới hạn**: môi trường nghiên cứu bị proxy chặn đọc trực tiếp trang pricing và một số trang help, nên các mục **VERIFIED** được xác nhận qua trích đoạn search-index của đúng trang tài liệu chính thức (tiêu đề + nội dung trích), ⛔ không phải đọc trọn trang. Mọi thứ không xác nhận được theo cách đó đều gắn nhãn **⛔ NOT VERIFIED** — đặc biệt là **toàn bộ con số giá**.

⇒ Hệ quả thực hành: giá không được hardcode vào repo. Founder đọc bảng giá thật trong console rồi điền vào `.env` (xem [`.env.example`](../../.env.example)), đúng `SRS §5.2` — *"bịa một con số performance là lỗi nghiêm trọng hơn để trống nó"*.

## 1. Vai trò sinh ảnh — reference image là điều kiện cứng

Yêu cầu của pipeline: text prompt + **1–3 ảnh reference** (identity — precedence ladder ⛔ không bao giờ drop) → 1 candidate. Model chỉ nhận text ⛔ không dùng được cho stage `panels`.

| Model | Ảnh input | Sync/Async | Trạng thái xác minh |
|---|---|---|---|
| ⭐ `qwen-image-edit-plus` | **1–3 ảnh** + 1 text; output 1–6 ảnh | **Sync** (docs: *"Asynchronous interfaces are not supported"*) | ✅ VERIFIED — khớp chính xác trần `INV-2` ≤3 nhân vật |
| `qwen-image-edit-max` | 1–3 ảnh (cùng họ edit) | Sync | ✅ VERIFIED — có free quota 100 ảnh |
| `qwen-image-max` (t2i, có snapshot `qwen-image-max-2025-12-30`) | 0 (text-to-image) | Sync | ✅ VERIFIED — dùng cho stage `refs` |
| `wan2.7-image-pro` | tối đa **9 ảnh**; docs ghi đích danh *"character-consistent multi-image generation"* | **Async** (submit + poll, URL kết quả sống 24h) | ✅ VERIFIED — ứng viên dự phòng nếu chất lượng edit-plus không đạt |
| `wan2.5-i2i-preview` / `wan2.6-image` | nhiều ảnh / tối đa 4 | Async | ✅ VERIFIED (max ảnh của 2.5: ⛔ NOT VERIFIED) |
| `wanx-style-repaint-v1` (Wan 2.1 legacy) | — | — | ⛔ NOT VERIFIED trên endpoint quốc tế 2026 — ⛔ không xây trên nó |

**Định dạng input**: ✅ VERIFIED — nhận public URL **hoặc Base64 data URI** `data:image/png;base64,...`, PNG/JPG/WEBP..., ≤10 MB/ảnh sau encode, cạnh tốt nhất 384–3072 px. ⇒ Khớp pipeline hiện tại (reference đọc từ file PNG local, ⛔ không cần upload storage).

**Lựa chọn cho MVP0**: `qwen-image-edit-plus` (panels) + `qwen-image-max` (refs) — ưu tiên **sync** để script vứt-đi khỏi gánh plumbing submit/poll + tải URL 24h của họ Wan. `wan2.7-image-pro` ghi lại làm ứng viên xem xét ở gate cuối nếu chất lượng consistency của edit-plus không đạt `G1-a`.

## 2. Vai trò VLM QA-select — đối chiếu 5 tiêu chí ADR-007 Q5

| # | Tiêu chí `Q5` | Kết quả trên Qwen-VL | Trạng thái |
|--:|---|---|---|
| **1** | Nhận nhiều ảnh trong **MỘT** call (tiêu chí **loại**) | Visual-understanding models *"support single or multiple image inputs"*; N=3 nằm rất xa trần (giới hạn thực là token: ≤16.384 token/ảnh, 131.072 token/request) | ✅ **PASS — VERIFIED** |
| **2** | Structured output ổn định | `response_format={"type":"json_object"}` — hỗ trợ họ Qwen3-VL-Plus/Flash và Qwen-VL-Max/Plus (⛔ trừ alias `latest`); message phải chứa chữ "JSON" (rubric đã có); model hybrid-thinking phải tắt thinking (`enable_thinking=false`) | ✅ **PASS — VERIFIED** |
| **3** | Version pinning tường minh | Có snapshot dated (mẫu `qwen-vl-max-2025-01-25`); pin bằng chính model id | ✅ Đạt — pin snapshot khi console cho phép |
| **4** | Batch / async (mong muốn, ⛔ không phải CHỐT) | Model Studio có batch cho LLM/VL | 🟡 Chưa cần ở MVP0 |
| **5** | Chi phí per-call | Chỉ so được sau khi đo — chính là khoản `CF-3.5` **chưa tính**; adapter mới ghi `vlm_tokens` mỗi call để gate cuối có số | ⏳ Đo ở MVP0 |
| — | Model chọn | ⭐ `qwen3-vl-plus` (commercial, JSON mode, multi-image). ⚠️ `qwen3-vl-max` ⛔ **không tìm thấy trong docs chính thức** — ⛔ đừng spec nó | ✅ |

## 3. Cơ chế API

| Hạng mục | Giá trị | Trạng thái |
|---|---|---|
| Endpoint OpenAI-compatible (Singapore) | `https://dashscope-intl.aliyuncs.com/compatible-mode/v1` | ✅ VERIFIED |
| Endpoint native DashScope (Singapore) | `https://dashscope-intl.aliyuncs.com/api/v1` | ✅ VERIFIED |
| Sinh ảnh qua OpenAI-compatible? | ⛔ **KHÔNG** — Qwen-Image/Wan chỉ có đường native (`multimodal-generation/generation`, SDK `MultiModalConversation.call`) | ✅ VERIFIED |
| VLM qua OpenAI-compatible? | ✅ Có — chat completions + `image_url` (nhận Base64 data URI) + `response_format` | ✅ VERIFIED |
| SDK | `pip install dashscope` (native) · `pip install openai` trỏ base_url về compatible-mode | ✅ VERIFIED |
| Region | Key và endpoint Bắc Kinh vs Singapore **tách rời**, ⛔ không dùng lẫn | ✅ VERIFIED |
| Billing rule | Chỉ tính tiền ảnh **sinh thành công**; call fail ⛔ không tính, ⛔ không trừ free quota | ✅ VERIFIED |

⭐ Hai vai trò buộc phải đi **hai đường API khác nhau** — vô tình củng cố đúng yêu cầu *"hai adapter tách riêng"* của `ADR-007` `Q1`.

## 4. Giá — trạng thái xác minh

> [!CAUTION]
> ⛔ **Không con số nào dưới đây được verify từ trang pricing chính thức** (bị chặn khi nghiên cứu). Chúng là số nguồn thứ ba, **mâu thuẫn lẫn nhau**, chỉ dùng làm **dải quy hoạch**: sinh ảnh **$0.02–$0.075/ảnh** (`qwen-image-edit-plus` ~$0.03–0.06 · `qwen-image` ~$0.035–0.075 · họ wan ~$0.02–0.075); VLM `qwen3-vl-plus` ~$0.14–0.20/M token input — một call chấm 3 ảnh (~2–4K token) là **dưới 1 cent** theo mọi nguồn.
>
> ⇒ **Nguồn sự thật duy nhất**: bảng giá trong console Model Studio (trang `model-pricing`). Founder điền số đọc được vào `.env` (`MVP0_IMAGE_PRICE_T2I_USD` / `MVP0_IMAGE_PRICE_EDIT_USD`).

**Ý nghĩa với ngân sách MVP0** (nếu dải trên đúng): 126 ảnh ≈ **$2,52–$9,45** — lần đầu nằm **trong** trần `~$12` (`CF-3.11`), so với ~$16,88 (vượt 41%) theo giá Gemini `$0.134`.

## 5. Account, region và free quota

- Region khả dụng: Beijing · Virginia · **Singapore** · Tokyo · Frankfurt · Hong Kong; Singapore = deployment scope International — ✅ VERIFIED.
- Kích hoạt per-region trong console; cần balance ≥ 0, có thể cần real-name verification — ✅ VERIFIED. Dùng được từ Việt Nam: ⛔ không có danh sách quốc gia trong docs ⇒ ⛔ NOT VERIFIED trên giấy — **Founder đã tự xác nhận bằng cách kích hoạt thật** (bước 1 của kế hoạch, `2026-08-31`).
- **Free quota người dùng mới** — ✅ VERIFIED: 90 ngày kể từ kích hoạt; ~**1M token/model** cho các model Qwen chủ lực (tính riêng từng model, gồm VL); **100 ảnh** cho `qwen-image-max` và `qwen-image-edit-max`; chỉ tính real-time inference; đồng hồ ⛔ không tạm dừng. Quota riêng cho `qwen-image-edit-plus`/wan: ⛔ NOT VERIFIED — xem trong console.

## 6. Content moderation — rủi ro mở lớn nhất

- ✅ VERIFIED cơ chế: mọi call sinh ảnh kiểm duyệt **input** (prompt, negative prompt, ảnh input) **và output**; vi phạm trả `DataInspectionFailed` (hoặc `IPInfringementSuspect`) — adapter map hai mã này vào `ProviderRefusal` → `refusals.jsonl` (`D-67`).
- ⛔ **Không có safety settings chỉnh được** cho sinh ảnh trên endpoint quốc tế (khác Gemini có `safetySettings`); ngưỡng với fantasy violence ⛔ không công bố; so sánh độ nghiêm với Gemini ⛔ không có nguồn chính thức. Lời đồn cộng đồng nghiêng về "nghiêm" — là **giai thoại**, ⛔ không phải bằng chứng.
- ⇒ **Nghĩa vụ trước khi ký ngưỡng**: batch thăm dò 10–20 prompt (gồm panel **18** — kiếm xuyên ngực + máu, ca `C-7` rủi ro nhất) trong free quota, đếm tỉ lệ `DataInspectionFailed`. Tỉ lệ cao ⇒ đổi `action` các panel rủi ro hoặc quay lại Gemini **trước khi** sinh ảnh thật — thời điểm đó chi phí chuyển đổi bằng 0.

## Kết luận

1. **Cả hai điều kiện cứng PASS** trên giấy: `qwen-image-edit-plus` nhận 1–3 reference (khớp `INV-2`), `qwen3-vl-plus` nhận N ảnh một call + JSON mode (tiêu chí loại `Q5` #1, #2).
2. **Kinh tế nghiêng về Alibaba** theo dải giá tham khảo (⛔ chưa verify chính thức) + free quota 90 ngày — nhưng số đưa vào gate phải là số console/thực đo.
3. **Hai việc mở chặn việc "chạy thật"**: điền giá verified vào `.env`, và batch thăm dò content moderation cho fantasy violence.
4. Quyết định này **⛔ không đụng** tầng spec Phase 2 (`Spec-Integration-Image-Provider` vẫn ghi Gemini làm mặc định sản phẩm) — vendor sản phẩm chốt ở gate cuối MVP0 bằng số đo, đúng `ADR-007` `Q4`.

## Tài liệu tham khảo

Tất cả thuộc `https://www.alibabacloud.com/help/en/model-studio/` (truy cập `2026-08-31`):

- `qwen-image-edit-api` · `qwen-image-generation-and-editing-api-reference` — họ Qwen-Image edit/t2i, input 1–3 ảnh, Base64, sync
- `qwen-vl-compatible-with-openai` · `vision` — Qwen-VL multi-image qua OpenAI-compatible
- `json-mode` · `qwen-structured-output` — `response_format: json_object`, ràng buộc thinking mode
- `compatibility-of-openai-with-dashscope` · `install-sdk` — endpoint quốc tế, SDK
- `wan2-7-image-pro` · `wan-image-generation-and-editing-api-reference` · `wan-image-edit` · `wan2-5-image-edit-api-reference` — họ Wan, async task, URL 24h
- `models` · `regions` · `new-free-quota` · `new-free-quota-validity-adjustment` — lineup model, region, free quota
- `error-code` · `text-to-image` — mã `DataInspectionFailed` / `IPInfringementSuspect`, kiểm duyệt input + output
- `model-pricing` — trang giá chính thức (⚠️ ⛔ chưa đọc được từ môi trường nghiên cứu — nguồn sự thật để Founder đối chiếu)

Nội bộ: [ADR-007](../030-Specs/Architecture/ADR-007-VLM-Provider-For-QA-Select.md) · [Spec-Integration-Image-Provider](../030-Specs/API/Spec-Integration-Image-Provider.md) · [`mvp0/README.md`](../../mvp0/README.md) · [Chạy MVP0](../060-Manuals/User-Guide/Chay-MVP0.md)

---

_Created by Comic Studio_
_Author: trisjr_
