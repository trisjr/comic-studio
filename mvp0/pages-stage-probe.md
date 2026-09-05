<!-- AI Coding -->

# Probe stage `pages` — `ch01_page001` · Báo cáo chặn

> [!NOTE]
> ✅ **Lỗi chặn ĐÃ ĐÓNG ngày `2026-09-05`** bằng cách đổi model — xem [§7](#7-quyết-định-của-founder--đổi-model) và [§8](#8-kết-quả-sau-khi-đổi-model--qwen-image-20-pro-2026-06-22). Chương 1 đã sinh xong **33/33 ảnh** đúng khổ trang.
>
> §1–§6 dưới đây giữ nguyên làm **hồ sơ chẩn đoán**: chúng ghi lại vì sao cấu hình cũ hỏng và bằng chứng nào dẫn tới quyết định đổi model. ⛔ Không đọc §1–§6 như trạng thái hiện tại.

**Probe chẩn đoán**: `2026-09-05` · run `mvp0/run-pages-20260905-223242` · 3 image call · 0 refusal
**Run chương 1**: `2026-09-05` · run `mvp0/run-pages-20260905-231040` · 33 image call · 0 refusal

## Mục lục

- [1. Probe này hỏi gì](#1-probe-này-hỏi-gì)
- [2. Hai lỗi chặn](#2-hai-lỗi-chặn)
- [3. VLM-select ⛔ không bắt được lỗi nào](#3-vlm-select--không-bắt-được-lỗi-nào)
- [4. Cái probe đã chứng minh là CHẠY ĐƯỢC](#4-cái-probe-đã-chứng-minh-là-chạy-được)
- [5. Hệ quả cho `g1-verdict.md` §4.3](#5-hệ-quả-cho-g1-verdictmd-43)
- [6. Việc phải làm trước khi chạy lại](#6-việc-phải-làm-trước-khi-chạy-lại)
  - [6.1. Ba hướng cho mục 1](#61-ba-hướng-cho-mục-1)
- [7. Quyết định của Founder — đổi model](#7-quyết-định-của-founder--đổi-model)
- [8. Kết quả sau khi đổi model](#8-kết-quả-sau-khi-đổi-model--qwen-image-20-pro-2026-06-22)
  - [8.2. Vì sao chốt `--no-refs`](#82-vì-sao-chốt---no-refs--số-đo--không-phải-cảm-tính)
  - [8.4. Số đo run chương 1](#84-số-đo-run-chương-1--mvp0run-pages-20260905-231040)
  - [8.5. Ba việc còn lại](#85-ba-việc-còn-lại-xếp-theo-mức-nặng)
- [9. Tài liệu tham khảo](#9-tài-liệu-tham-khảo)

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

## 7. Quyết định của Founder — đổi model

| | |
|---|---|
| **Ngày** | `2026-09-05` |
| **Người quyết** | **TrisJr (Founder)** — chỉ đạo trực tiếp trong phiên, ghi nhận bởi TNMCORE-OS |
| **Nội dung** | Đổi sang **`qwen-image-2.0-pro-2026-06-22`** và sinh lại chương 1 |
| **Ràng buộc kèm theo** | ⭐ **Các panel PHẢI nằm trong MỘT ảnh** — ⛔ tuyệt đối không tách từng panel sinh riêng lẻ |

⇒ Ràng buộc này **loại hướng B** ở [§6.1](#61-ba-hướng-cho-mục-1) và **giữ nguyên `D-1`** (đơn vị sinh ảnh cấp trang). Kết quả thực thi ở [§8](#8-kết-quả-sau-khi-đổi-model--qwen-image-20-pro-2026-06-22).

## 8. Kết quả sau khi đổi model — `qwen-image-2.0-pro-2026-06-22`

> [!IMPORTANT]
> ✅ **Lỗi chặn ở [§2](#2-hai-lỗi-chặn) ĐÃ ĐÓNG.** Founder chỉ định đổi model ngày `2026-09-05`. Chương 1 đã sinh xong: **33/33 ảnh, đúng `1024x1536`, 0 refusal**, và ⛔ **không còn tấm minh họa cảnh đơn nào** — mọi ảnh đều là trang có khung panel.
>
> ⇒ Hướng **D** ở [§6.1](#61-ba-hướng-cho-mục-1) trở thành **vô nghĩa** — ⛔ không cần canvas kẻ sẵn nữa. Hướng **A/B/C** cũng khép lại: đường thắng là *model mới + `size` tường minh + ⛔ không đính ref*.

### 8.1. Ba thay đổi đã làm

| # | Thay đổi | Vì sao |
|:-:|---|---|
| 1 | `IMAGE_T2I_MODEL_ID` và `IMAGE_EDIT_MODEL_ID` → `qwen-image-2.0-pro-2026-06-22` | Founder chỉ định. ✅ **Đã verify id có thật** trên account qua `GET /compatible-mode/v1/models` (165 model) — snapshot có ngày ⇒ thỏa `IP-C3` |
| 2 | Gửi `size` tường minh lên API, lấy từ `page.target_resolution` | Đóng lỗi B. Ảnh ra `1024x1536` thay vì `1376x768` |
| 3 | Cờ `--no-refs` cho stage `pages` | Để **đo được** cả hai cách nối ref thay vì đoán |

### 8.2. Vì sao chốt `--no-refs` — số đo, ⛔ không phải cảm tính

Model mới ✅ **có** nhận ảnh đầu vào (verify bằng 1 call thật, `status_code 200`). Nên cả hai cấu hình đều chạy được, và cả hai đã được probe với cùng `size`, cùng prompt, mỗi bên 1 call:

| | `--no-refs` (run `230610`) | Có ref (run `230813`) | Đặc tả |
|---|---|---|---|
| Row / panel | **4 row / 8 panel** | 6 row / 11 panel | 4 row / 5 panel |
| Khung hình | ✅ `1024x1536` | ✅ `1024x1536` | `1024x1536` |
| Lỗi riêng | Trang phục `tu_ba_ba` đổi màu (tím → cam) | ⛔ **Row 3–4 lặp lại gần y hệt nhau** | — |

⭐ **Cấu hình có ref thua ở chính tiêu chí Founder đặt ra.** Việc row 3–4 nhân đôi là dấu vết còn lại của hành vi *edit*: model vẫn nhân bản chủ thể trong ảnh ref thay vì dựng cảnh mới. Trang phục nhất quán hơn ⛔ không bù được 6 panel thừa.

> [!WARNING]
> ⚠️ **Cái giá đã biết của `--no-refs`: `mvp0/refs/*.png` ⛔ KHÔNG còn được dùng ở stage `pages`.** Nhân vật chỉ còn neo bằng chữ. Trang phục `tu_ba_ba` đổi tím → cam ngay trong một trang là biểu hiện trực tiếp.
>
> ⇒ Đây sẽ là **số đo `G1-a`**, ⛔ **không phải** lỗi đường ống — và nó ⛔ không được lẫn với các sai lệch tầng ref ở [`g1-verdict.md` §4.2](./golden-dataset/g1-verdict.md), vốn giờ đã **⛔ không còn liên quan** tới ảnh trang.

### 8.3. Hai thay đổi phụ, làm TRƯỚC khi bắn 33 call

**a. Compiler đếm hộ, ⛔ không bắt model đếm.** Khối `PAGE` cũ liệt kê `panels: panel_02, panel_03` — một **danh sách phải đếm**. Giờ ghi thẳng con số:

```
panel_count: exactly 5 panels on this page, laid out in exactly 4 horizontal rows.
row 2: y 0.22 to 0.46, exactly 2 panel(s): panel_02, panel_03
```

Kết quả trên `ch01_page001`: **8 panel → 6 panel** (đặc tả 5). ⇒ Có tác dụng, ⛔ **chưa đủ**.

**b. `VLM_RUBRIC` viết lại sang cấp page.** Rubric cũ hỏi 2 trục và mở đầu bằng *"chấm ứng viên cho CÙNG một **panel**"*. Rubric mới hỏi **5 trục** — `layout` (bắt **đếm** panel thực tế), `aspect_ratio`, `no_text`, `identity`, `constraints` (bắt **đọc lại từng dòng** `NEGATIVE_CONSTRAINTS`) — và chặn cứng: `verdict` ⛔ **không được** là `pass` nếu sai layout hoặc có chữ.

### 8.4. Số đo run chương 1 — `mvp0/run-pages-20260905-231040`

| Đại lượng | Giá trị |
|---|---|
| Ảnh sinh | **33/33** · 0 refusal · 0 dropped constraint |
| Kích thước | **33/33** đúng `1024x1536` |
| Verdict VLM | `pass` **7** · `fail` **10** · `unclear` **16** |
| `layout_ok` | **12/33** candidate · **6/11** trang có ít nhất 1 candidate đạt |
| `no_text_ok` | **30/33** — chỉ `ch01_page005` dính, cả 3/3 |
| `constraints_ok` | **12/33** |
| `identity_ok` | **25/33** |

> [!CAUTION]
> ⚠️ **⛔ KHÔNG chép bảng này vào `scoring-sheet.csv`.** Đây là **số của máy**, và VLM vẫn sai: trang `ch01_page001` được chấm `layout_ok` với `panel_count_seen: 5`, nhưng soi mắt thấy **6 panel** (row 4 ra 2 panel, đặc tả 1). ⇒ Rubric mới **tốt hơn nhiều** nhưng ⛔ **chưa phải** thước đo thay được người. `G1` vẫn chấm bằng mắt.

### 8.5. Ba việc còn lại, xếp theo mức nặng

| # | Vấn đề | Bằng chứng | Ghi chú |
|:-:|---|---|---|
| 1 | ⛔ **Model vẽ text của prompt vào ảnh** | `ch01_page005` **3/3** candidate có caption kiểu *"Panel 21: Granny…"*, thậm chí cả đoạn spec *"age 70; body_type…"* | ⚠️ Vi phạm `G1-e` nặng nhất từ trước tới nay. Nghi vấn: prompt trang này dài nhất nhóm và nhãn `panel_NN` bị đọc thành **chữ cần vẽ** |
| 2 | ⚠️ Layout vẫn lệch | 12/33 candidate đạt; `page001` ra 6 panel thay vì 5 | Đã cải thiện lớn nhờ [§8.3a](#83-hai-thay-đổi-phụ-làm-trước-khi-bắn-33-call), ⛔ chưa đóng |
| 3 | ⚠️ Trang phục đổi giữa các panel | `tu_ba_ba` tím → cam ngay trong `page001` | Hệ quả đã biết của `--no-refs` — là **số đo `G1-a`**, ⛔ không phải bug |

⭐ **Bước người làm tiếp theo**: soi 33 ảnh bằng mắt, chọn candidate mỗi trang, `crop_page.py`, rồi mới chấm `scoring-sheet.csv`. ⛔ Máy ⛔ không làm thay bước này.

## 9. Tài liệu tham khảo

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
