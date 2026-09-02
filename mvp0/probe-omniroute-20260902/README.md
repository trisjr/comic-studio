<!-- Knowledge Base -->
# Probe OmniRoute — 2026-09-02

Bằng chứng thô của một lần thăm dò: **OmniRoute local (v3.8.48) có thay được Alibaba Model Studio cho MVP0 không?**

Provider được test: `antigravity` · model `antigravity/gemini-3.1-flash-image`.

> [!IMPORTANT]
> **Kết luận vận hành: ⛔ KHÔNG dùng OmniRoute cho MVP0.** Founder chốt ngày `2026-09-02` — pipeline sinh ảnh tiếp tục gọi thẳng Alibaba Model Studio. Code adapter thử nghiệm đã được revert; thư mục này giữ lại **lý do**, để lần sau ⛔ không phải probe lại từ đầu.

## Kết luận

| Đường API | Kết quả | Bằng chứng |
|---|---|---|
| `/v1/images/generations` (t2i, ⛔ không ảnh input) | ✅ **Chạy** — JPEG 1024×1024 | `t2i-apple.jpg` |
| `/v1/images/edits` (multipart, có reference) | ⛔ **400 hard block** | `edits-400.json` |
| `/v1/chat/completions` + ảnh input | ⛔ **200 nhưng mất ảnh** | `chat-completions-drops-image.sse.txt` |
| `/v1/images/generations` + field `image` | ⛔ **200, field bị bỏ qua âm thầm** | `ignored-image-field-bamboo.jpg` |
| `/v1/responses` + ảnh input | ⚠️ **Chưa kết luận** — 502 do quota cạn, ⛔ không phải do API |

⇒ Stage `refs` chạy được. **Stage `panels` ⛔ không** — không có reference conditioning.

## Đọc từng bằng chứng

### `t2i-apple.jpg`
Prompt: *"A single red apple on a white table, photorealistic"*. Ảnh JPEG 1024×1024, có C2PA metadata của Google. Đường t2i hoạt động thật.

### `edits-400.json`
```
Image edit is not supported for built-in provider "antigravity".
Use chatgpt-web or a custom OpenAI-compatible image provider.
```
Chặn ở tầng gateway, ⛔ không phải lỗi tạm thời. Model `antigravity/gemini-3-pro-image-preview` cũng trả cùng lỗi này.

### `chat-completions-drops-image.sse.txt`
Input: ảnh reference `lam_uyen.png` + prompt vẽ lại nhân vật đó. Stream trả `HTTP 200`, `finish_reason: stop`, 1497 reasoning token — model **tự nói nó đã vẽ xong** (*"This image should be sent"*), nhưng mọi `delta` chỉ chứa `reasoning_content`, ⛔ không có `content` nào. Gateway đánh rơi phần ảnh khi convert sang format OpenAI. Lặp lại ở cả `stream: true` và `stream: false`.

### `ignored-image-field-bamboo.jpg` — ⚠️ kiểu hỏng nguy hiểm nhất
Request gửi kèm field `image` = ảnh reference của **Lâm Uyển** (nam, tóc dài đen, áo choàng rách đen). Ảnh trả về là một **nữ sinh mặc đồng phục sailor Nhật** trong rừng tre.

Field `image` bị bỏ qua hoàn toàn — nhưng response vẫn `HTTP 200`. Nếu để stage `panels` chạy qua đường này, 8 panel đầu của `ch1` (`characters: []`) sẽ "thành công" bằng t2i thuần và chỉ panel 9 mới lộ vấn đề ⇒ ra một dataset lai hai pipeline, và phép đo `G1` sẽ đo nhầm.

⭐ **Bài học rộng hơn `HTTP 200` ⛔ không phải bằng chứng đúng.** Kiểu hỏng này chỉ phát hiện được bằng cách **nhìn vào output thật**, ⛔ không phải bằng cách đọc status code.

## Vì sao không chọn OmniRoute — hai lý do

1. **Thiếu năng lực bắt buộc** — ⛔ không có reference conditioning thì stage `panels` ⛔ không chạy được, mà `panels` chính là câu hỏi cốt lõi của MVP0.

2. ⭐ **Gateway âm thầm sửa payload** — đây mới là lý do nặng hơn. Với một pipeline dùng để **ĐO** (`G1`), một lớp trung gian có thể lặng lẽ đổi input là rủi ro sai lệch nghiêm trọng: ⛔ không biết mình đang đo cái gì. Gọi thẳng Alibaba ít lớp hơn, dễ truy vết hơn.

⚠️ Ba vấn đề đầu nằm ở **chính gateway**, ⛔ không phải ở provider — và thông báo lỗi của OmniRoute gợi ý nó **có** hỗ trợ image edit với provider khác. Vậy đây là kết luận về **tổ hợp OmniRoute + antigravity cho bài toán MVP0**, ⛔ không phải phán xét chung về OmniRoute.

## Giới hạn của lần thăm dò này

- ⚠️ **Quota `antigravity` cạn giữa chừng** (`RESOURCE_EXHAUSTED`, reset sau ~4h41m tính từ 16:35 — khoảng **21:15**). Lần thăm dò tiêu ~3 ảnh. Vì vậy `/v1/responses` ⛔ chưa kết luận được, và ⛔ chưa chạy được stage `refs` end-to-end trên quota thật.
- ⚠️ **Header `x-omniroute-*` chưa xác minh trên đường ảnh.** Mới chỉ quan sát được trên stream của `/v1/chat/completions`; response `200` của `/v1/images/generations` ⛔ chưa bắt header lần nào (lần thử duy nhất rơi vào 429). Nếu ai thử lại đường này, đừng giả định các header đó tồn tại.
- ⚠️ `output_format: png` ⛔ chưa test được — OmniRoute trả JPEG, trong khi pipeline lưu đuôi `.png`.

## Nếu sau này muốn thử lại

Đường chưa thử: nối **chính DashScope vào OmniRoute như custom OpenAI-compatible image provider** — lúc đó `/v1/images/edits` có thể mở. ⚠️ Nhưng nó chèn thêm một lớp vào đúng chỗ cần sạch để đổi lấy ⛔ không gì cả, vì vẫn trả tiền cho Alibaba.

Chỗ OmniRoute thực sự đáng dùng là **chạy Claude Code / coding agent trên model free** — một bài toán ⛔ hoàn toàn tách khỏi pipeline sinh ảnh.

## Tài liệu tham khảo

- `scripts/mvp0/providers.py` — adapter Alibaba (⛔ không còn nhánh OmniRoute)
- `ADR-007` Q4 — việc chốt vendor đặt ở gate cuối MVP0
- `D-59` — `cost_usd` thiếu giá thì ghi `null`, ⛔ không bao giờ ghi `0`
