<!-- AI Coding -->

# Probe stage `pages` — `ch01_page001` · Báo cáo chặn

> [!CAUTION]
> ⛔ **KHÔNG chạy `run_mvp0.py pages` cho cả chương cho tới khi hai lỗi ở [§2](#2-hai-lỗi-chặn) được đóng.**
>
> Probe 3 ảnh đã chứng minh: stage `pages` hiện ⛔ **không sinh ra trang truyện**. Chi 33 call còn lại sẽ mua về 33 tấm minh họa đơn sai tỉ lệ — ⛔ không dùng chấm `G1` được.

**Ngày probe**: `2026-09-05` · **Run**: `mvp0/run-pages-20260905-223242` · **Chi phí**: 3 image call + 1 VLM call · **Refusal**: 0

## Mục lục

- [1. Probe này hỏi gì](#1-probe-này-hỏi-gì)
- [2. Hai lỗi chặn](#2-hai-lỗi-chặn)
- [3. VLM-select ⛔ không bắt được lỗi nào](#3-vlm-select--không-bắt-được-lỗi-nào)
- [4. Cái probe đã chứng minh là CHẠY ĐƯỢC](#4-cái-probe-đã-chứng-minh-là-chạy-được)
- [5. Hệ quả cho `g1-verdict.md` §4.3](#5-hệ-quả-cho-g1-verdictmd-43)
- [6. Việc phải làm trước khi chạy lại](#6-việc-phải-làm-trước-khi-chạy-lại)
  - [6.1. Ba hướng cho mục 1](#61-ba-hướng-cho-mục-1)
- [7. Tài liệu tham khảo](#7-tài-liệu-tham-khảo)

---

## 1. Probe này hỏi gì

`README` Bước 6 yêu cầu thăm dò vài trang rủi ro trước khi chạy cả chương. Probe này còn có một lý do mạnh hơn: stage `refs` gọi `qwen-image` (T2I, ⛔ không ref), còn stage `pages` có `conditioning_set` ⛔ không rỗng nên gọi **`qwen-image-edit`** — model **chưa từng được gọi lần nào** trong dự án. Probe chính là phép verify model id mà `providers.py` dòng 36 đòi.

Đầu vào: `ch01_page001` — 5 panel, 2 ref (`tu_ba_ba`, `ma_lao`), prompt 11.836 ký tự, **0 dropped constraint**.

## 2. Hai lỗi chặn

### 2.1. Lỗi A — ảnh ra ⛔ KHÔNG có panel nào

Cả **3/3** candidate là **một tấm minh họa cảnh đơn**, ⛔ không phải trang truyện 5 panel. Khối `PAGE` trong prompt mô tả rõ 4 row với tọa độ `y` (`row 1: y 0.0 to 0.22`…) — model bỏ qua **toàn bộ**.

⇒ `crop_page.py` ⛔ **không cắt được** panel theo `layout.rows`, nên ⛔ không có panel nào để ghi vào `scoring-sheet.csv`. Toàn bộ dây chuyền chấm `G1` **đứt ngay tại đây**.

### 2.2. Lỗi B — tỉ lệ khung sai, và ⛔ không ai gửi nó lên API

| | Yêu cầu | Thực tế |
|---|---|---|
| `aspect_ratio` | `2:3` (dọc) | **16:9 (ngang)** |
| `target_resolution` | `1024x1536` | **1376x768** — cả 3/3 candidate |

**Nguyên nhân bề mặt**: `providers.py::_call_image_api` chỉ gửi `model`, `messages`, `result_format`, `n`, `prompt_extend`, `watermark` — ⛔ **KHÔNG có tham số `size`**. Hai trường `aspect_ratio` / `target_resolution` của page YAML chỉ tồn tại dưới dạng **chữ trong prompt**.

⭐ **Nhưng nguyên nhân gốc sâu hơn thế** — đo được bằng một phép so tỉ lệ:

| | Kích thước | Tỉ lệ |
|---|---|---|
| Ảnh ref đầu vào (`mvp0/refs/*.png`, cả 8/8) | `1664x928` | **1.793** |
| Ảnh trang đầu ra (cả 3/3 candidate) | `1376x768` | **1.792** |
| Page YAML yêu cầu | `1024x1536` | 0.667 |

⇒ Output **echo đúng tỉ lệ của ảnh đầu vào**, ⛔ không phải một tỉ lệ mặc định của model. Nói cách khác: `qwen-image-edit` đang coi ảnh ref là **ảnh gốc cần chỉnh sửa**, ⛔ **không phải** tài liệu tham chiếu nhân vật. Nó **biến tấm character sheet thành một cảnh**, và giữ nguyên khung hình của tấm đó.

> [!IMPORTANT]
> ⭐ **Lỗi A và lỗi B là MỘT lỗi, ⛔ không phải hai.** Model ⛔ không bỏ qua layout vì prompt yếu; nó bỏ qua layout vì **⛔ không được giao việc dựng trang** — nó được giao việc *edit một tấm ảnh có sẵn*. Trang nhiều panel dọc 2:3 ⛔ không phải là kết quả mà thao tác edit này có thể tạo ra.
>
> ⇒ ⛔ **Thêm tham số `size` một mình ⛔ KHÔNG đóng được lỗi này.** Nó có thể ép được khung hình, nhưng ⛔ không làm model dựng ra 5 panel. Đây là **sai lựa chọn công cụ**, ⛔ không phải thiếu tham số.

### 2.3. Vi phạm `NEGATIVE_CONSTRAINTS` quan sát bằng mắt

Prompt cấm tường minh, ảnh vẫn vi phạm:

| Ràng buộc trong prompt | c0 | c1 | c2 |
|---|:-:|:-:|:-:|
| *"Do not render any letters, words, speech bubbles…"* | ✅ Sạch chữ | ⛔ **Chữ Hán cháy vào ảnh** — 2 biển đỏ treo dọc + nhãn trên hũ sành | ✅ Sạch chữ |
| *"Do not give Elder Ma a left arm or a visible left hand"* | ⛔ Đủ hai tay, hai bàn tay trần | ⛔ Đủ hai tay, cầm gậy | ⛔ Đủ hai tay |
| *"Do not show any moon, stars, lanterns, torches…"* | ⛔ Trăng tròn + đèn lồng + dây đèn | ⛔ Trăng tròn + đèn dầu | ⛔ Trăng + sao + đèn bão |
| *"Do not introduce additional villagers, animals, or creatures"* | — | ⛔ Nhiều dân làng đứng nền sau | ⛔ Tàu thủy hơi nước ngoài biển |
| Bối cảnh `boi_canh` — làng núi hẻo lánh | ⚠️ Có sông + nhà mái cong kiểu đền | ⚠️ Giống quầy hàng/miếu hơn là làng | ⛔ **Bờ biển**, ⛔ không phải làng núi |
| 4 tượng đá ở 4 góc làng | ⛔ Chỉ 1 tượng, đứng giữa suối | ⛔ Tượng bán thân bày trên bệ như hàng hóa | ⛔ ⛔ Không có tượng nào |

> [!CAUTION]
> ⚠️ **Guard `G1-e` ⛔ KHÔNG giữ được — 1/3 candidate có chữ cháy vào ảnh.**
>
> Prompt cấm chữ **hai lần** (khối `TYPESET` **và** khối `NEGATIVE_CONSTRAINTS`), model vẫn vẽ chữ Hán vào `c1`. Đây là **rủi ro trực tiếp** cho tiêu chí `G1-e` (*100% overlay · 0 model-render*) — và nó lặp lại đúng hiện tượng đã gặp ở tầng `refs`, nơi `yeu_phu_nguoi-c2` và `tan_muc_thieu_nien-c1` bị loại vì cùng lý do ([`refs/selection-log.md` §3](./refs/selection-log.md)).
>
> ⇒ Chữ-cháy quan sát được tới giờ: **refs ít nhất 2/42** · **pages 1/3**. ⚠️ Con số phía `refs` là **cận dưới**, ⛔ không phải tỉ lệ: `selection-log.md` chỉ ghi lại ứng viên **bị loại**, nên ⛔ không phải cả 42 tấm đều được soi chữ. Cỡ mẫu ⛔ còn quá nhỏ để kết luận, nhưng đủ để nói: cấm bằng chữ ⛔ **không phải** một bảo đảm.

## 3. VLM-select ⛔ không bắt được lỗi nào

| Candidate | VLM verdict | Sự thật quan sát bằng mắt |
|---|---|---|
| `c0` | **`pass`** · `identity_ok: true` · `attribute_binding_ok: true` · **`confidence: 0.98`** | ⛔ Ma Lão **đủ hai tay** · ⛔ có trăng · ⛔ có đèn lồng · ⛔ không có panel |
| `c2` | **`pass`** · `identity_ok: true` · `attribute_binding_ok: true` | ⛔ Bờ biển + tàu thủy · ⛔ đủ hai tay · ⛔ không có tượng |
| `c1` | `unclear` · `confidence: 0.45` | ⛔ **Chữ Hán cháy vào ảnh** · ⛔ đủ hai tay · ⛔ có trăng · ⛔ nhiều dân làng thừa |

⚠️ ⭐ **Chi tiết đắt nhất của bảng trên**: `c1` là candidate **duy nhất** VLM hạ hạng — và nó cũng là candidate **duy nhất có chữ cháy vào ảnh**. Nhưng lý do VLM đưa ra nói về **bối cảnh và tượng**, ⛔ **không hề nhắc tới chữ**. ⇒ VLM đánh trúng ⛔ không phải nhờ nhìn ra vi phạm nặng nhất. Đây là **đúng vì lý do sai** — ⛔ không được tính là bằng chứng rằng VLM-select đang hoạt động.

⚠️ VLM ghi nguyên văn *"Elder Ma (single right arm, knotted left sleeve…) are accurate"* cho một tấm ảnh mà **Ma Lão có đủ hai cánh tay trần**. Đây là **hallucination khẳng định**, ⛔ không phải chấm lỏng.

⭐ **Nguyên nhân gốc**: `VLM_RUBRIC` vẫn là **rubric cấp panel** của thời kỳ trước — mở đầu bằng *"Bạn đang chấm {n} ứng viên ảnh cho CÙNG một **panel** truyện tranh"* và *"Đặc tả **panel**"*. Nó chỉ hỏi **2 trục**: `identity` và `attribute_binding`. Nó ⛔ **không hỏi**:

- Ảnh có đúng số panel theo `layout.rows` ⛔ không
- Ảnh có đúng `aspect_ratio` ⛔ không
- Ảnh có vi phạm khối `NEGATIVE_CONSTRAINTS` ⛔ không

⇒ Rubric ⛔ không được cập nhật khi dự án chuyển đơn vị sinh ảnh từ panel sang page.

> [!WARNING]
> ⚠️ **⛔ KHÔNG được lấy số này làm `G1-c`.** `G1-c` đo *"tỉ lệ người loại sau khi VLM đã chọn"* trên một VLM **chấm đúng việc**. VLM hiện đang chấm **sai đề bài**, nên `reject_rate = 100%` ở đây đo **lỗi rubric**, ⛔ không đo năng lực của lớp VLM-select. Ghi số này vào `scoring-sheet.csv` sẽ làm hỏng `G1-c`.

## 4. Cái probe đã chứng minh là CHẠY ĐƯỢC

⛔ Đừng đọc báo cáo này thành *"mọi thứ hỏng"*. Bốn thứ đã được verify:

| Hạng mục | Kết quả |
|---|---|
| Model id `qwen-image-edit` | ✅ **Gọi được**, 3/3 thành công, **0 refusal** |
| Đường ống `compile → API → lưu ảnh → usage.jsonl` | ✅ Chạy trọn vẹn, ⛔ không exception |
| Ghi `usage.jsonl` trước khi biết kết quả VLM | ✅ Đúng `Story-Usage-Event AC` |
| Trung thực chi phí | ✅ `cost_usd: null` · `cost_status: "reference_price_missing"` — đúng `SRS §5.2`, ⛔ không bịa số |
| Dry-run cả chương | ✅ 11/11 trang compile · 0 dropped constraint |
| Guard `G1-e` (cấm chữ) | ⛔ **KHÔNG đạt** — 1/3 có chữ Hán cháy vào ảnh (xem [§2.3](#23-vi-phạm-negative_constraints-quan-sát-bằng-mắt)) |

⭐ **Probe làm đúng việc của nó**: chi **3 call** để chặn **33 call** sắp bị đổ vào một cấu hình hỏng.

## 5. Hệ quả cho `g1-verdict.md` §4.3

Bảng §4.3 hỏi *"tầng `pages` có sửa được lỗi loại 2 ⛔ không?"*. Probe này ⛔ **CHƯA trả lời được** — và ⛔ **không được** điền vào bảng đó.

⭐ **Lý do**: `NEGATIVE_CONSTRAINTS` đã được gửi lên đúng như thiết kế, nhưng model đang chạy ở một chế độ **⛔ không phải chế độ ta muốn đo** (sinh minh họa đơn, sai tỉ lệ, có thể đang coi ref image là *ảnh gốc để edit* thay vì *tài liệu tham chiếu nhân vật*). Kết luận *"pages ⛔ không sửa được loại 2"* rút ra từ cấu hình hỏng này sẽ là một **kết luận sai được ghi vĩnh viễn** vào tài liệu mà kỷ luật MVP0 nói là phải **giữ lại**.

⇒ §4.3 chỉ được điền sau khi [§6](#6-việc-phải-làm-trước-khi-chạy-lại) đóng xong và có một run **hợp lệ**.

## 6. Việc phải làm trước khi chạy lại

| # | Việc | Loại | Ghi chú |
|:-:|---|---|---|
| 1 | ⭐ **Chọn lại cách đưa ref vào model** — đây là việc gốc | ⚠️ **Quyết định thiết kế, cần Founder** | Ba hướng ở [§6.1](#61-ba-hướng-cho-mục-1). Mọi việc khác phụ thuộc mục này |
| 2 | Gửi `size` lên API từ `target_resolution` | Sửa `providers.py` + `run_mvp0.py` | ⚠️ **⛔ Không đủ một mình** — xem [§2.2](#22-lỗi-b--tỉ-lệ-khung-sai-và--không-ai-gửi-nó-lên-api). Chỉ làm sau khi mục 1 chốt |
| 3 | Viết lại `VLM_RUBRIC` sang **cấp page** | Sửa `providers.py` | Thêm trục: đúng số panel · đúng `aspect_ratio` · ⛔ vi phạm `NEGATIVE_CONSTRAINTS` · ⛔ có chữ cháy vào ảnh |
| 4 | Bổ sung `MVP0_IMAGE_PRICE_T2I_USD` / `MVP0_IMAGE_PRICE_EDIT_USD` vào `.env` | Cấu hình | ⛔ Không bịa — lấy từ bảng giá console |
| 5 | Theo dõi tỉ lệ chữ-cháy như một **số đo**, ⛔ không coi là đã đóng | Kỷ luật đo | `G1-e` đòi **0** model-render. Cấm 2 lần bằng chữ vẫn lọt 1/3 ⇒ phải đếm ở mọi run sau |

### 6.1. Ba hướng cho mục 1

| | Hướng | Được gì | Mất gì |
|:-:|---|---|---|
| **A** | Bỏ ref khỏi `content`, dùng **`qwen-image` (T2I)** — nhân vật chỉ mô tả bằng chữ. Prompt đã có sẵn đầy đủ `CHARACTERS` | Model ⛔ không còn "ảnh gốc để edit" ⇒ **có cơ hội dựng trang thật**; ép được `size` | ⛔ Mất neo hình ảnh ⇒ `G1-a` (consistency) nhiều khả năng tụt. Chính là thứ MVP0 muốn đo |
| **B** ⭐ | Sinh **từng panel** (T2I + ref cho panel đó), rồi ghép trang bằng code deterministic | Giữ được ref; ⛔ không đòi model làm việc nó ⛔ không làm được; ghép trang là bài toán đã giải | ⚠️ **Đảo ngược `D-1`** (đơn vị sinh ảnh cấp trang) — cần Founder duyệt |
| **C** | Tìm model/endpoint nhận ref như **conditioning** (IP-Adapter / reference-only), ⛔ không như ảnh cần edit | Giữ cả ref lẫn layout trang | ⚠️ Cần nghiên cứu xem DashScope có endpoint như vậy ⛔ không — có thể ⛔ không tồn tại |

⭐ **Em đề xuất hướng B**. Lý do: nó là hướng **duy nhất ⛔ không đánh cược** — A đánh cược rằng bỏ ref vẫn giữ được `G1-a` (đúng thứ đang cần đo, ⛔ không nên đem ra cược); C đánh cược rằng một endpoint như vậy tồn tại. B ⛔ không cược gì: ref vẫn dùng được, ghép ảnh là code thuần. Cái giá của B là **thật và đã biết trước** — phải xin đảo `D-1` — và một cái giá đã biết thì rẻ hơn một canh bạc.

> [!IMPORTANT]
> ⭐ **Mục 1 là quyết định của Founder, ⛔ không phải quyết định kỹ thuật thuần.** Hướng B đảo ngược `D-1` (*đơn vị sinh ảnh cấp trang*) đã ghi trong `README`. ⇒ Phải escalate, ⛔ không tự chọn.

> [!NOTE]
> ⛔ **Ngưỡng `G1` ⛔ KHÔNG đổi.** [`threshold-signoff.md`](./threshold-signoff.md) đã ký `2026-09-05` và probe này ⛔ không chạm vào. Đây là lỗi **đường ống**, ⛔ không phải kết quả đo.

## 7. Tài liệu tham khảo

| Tài liệu | Liên quan gì |
|---|---|
| [`README.md` Bước 6](./README.md) | Quy trình thăm dò trước khi chạy cả chương |
| [`golden-dataset/g1-verdict.md` §4.1 · §4.3](./golden-dataset/g1-verdict.md) | Phân loại lỗi loại 1 / loại 2; bảng §4.3 còn bỏ trống |
| [`threshold-signoff.md`](./threshold-signoff.md) | Ngưỡng `G1` đã ký, ⛔ không đổi |
| [`refs/selection-log.md` §0](./refs/selection-log.md) | Biên bản duyệt tạm mở khóa stage `pages` |
| `scripts/mvp0/providers.py` | `_call_image_api` (lỗi B) · `VLM_RUBRIC` (§3) |

---

_Created by TNMCORE-OS_
_Author: trisjr_
