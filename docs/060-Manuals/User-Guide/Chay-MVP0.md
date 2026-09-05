---
id: GUIDE-MVP0
type: user-guide
status: draft
project: comic-studio
owner: "@trisjr"
tags: [mvp0, van-hanh, gate-g1, huong-dan]
created: 2026-08-31
---

# Hướng dẫn chạy MVP0

> Hướng dẫn vận hành **từng bước** cho Founder-operator chạy MVP0 và ra được verdict gate `G1`.
>
> ⛔ Tài liệu này ⛔ **không** giải thích *vì sao* MVP0 tồn tại — đó là việc của [MVP-Scope §7.2](../../010-Planning/MVP-Scope.md) và [Analysis-MVP0-Requirements](../../050-Research/Analysis-MVP0-Requirements.md). Ở đây chỉ có **cách làm**.

## Mục lục

- [Trước khi bắt đầu](#trước-khi-bắt-đầu)
- [Bước 1 — Chuẩn bị môi trường](#bước-1--chuẩn-bị-môi-trường)
- [Bước 2 — Sinh canonical reference](#bước-2--sinh-canonical-reference)
- [Bước 3 — Sinh trang & crop panel](#bước-3--sinh-trang--crop-panel)
- [Bước 4 — Chấm gate `G1`](#bước-4--chấm-gate-g1)
- [Bước 5 — Ghi verdict và golden dataset](#bước-5--ghi-verdict-và-golden-dataset)
- [Xử lý sự cố](#xử-lý-sự-cố)
- [Tài liệu tham khảo](#tài-liệu-tham-khảo)

---

## Trước khi bắt đầu

### ⛔ Ba việc bắt buộc làm TRƯỚC khi sinh tấm ảnh đầu tiên

| # | Việc | Vì sao ⛔ không hoãn được |
|:-:|---|---|
| **1** | **Ký [`mvp0/threshold-signoff.md`](../../../mvp0/threshold-signoff.md)** | [MVP-Scope §7](../../010-Planning/MVP-Scope.md): *"Không sửa ngưỡng sau khi nhìn thấy kết quả — **đó là cách một gate biến thành nghi lễ**."* Ký sau khi thấy số ⛔ **không có giá trị** |
| **2** | **Verify ba model id** trong [`scripts/mvp0/providers.py`](../../../scripts/mvp0/providers.py) | Ba hằng số (`IMAGE_T2I_MODEL_ID` · `IMAGE_EDIT_MODEL_ID` · `VLM_MODEL_ID`) là **tên model** lấy từ tài liệu Model Studio, ⛔ **chưa đối chiếu** với console của account thật; pin **snapshot có ngày** khi console cho phép |
| **3** | **Chốt ngân sách theo giá đã verify** | Công thức: trọn chương chữ = **126 ảnh** × giá/ảnh đọc từ console (điền vào `.env`). Mốc Gemini cũ: ~$16,88 vượt trần `~$12`; dải Alibaba ⚠️ chưa verify: ~$2,52–$9,45. Trần thực tế `~$50`. Xem khối ngân sách trong [`mvp0/README.md`](../../../mvp0/README.md) |

### Kỷ luật ⛔ không được quên

> **Code của MVP0 KHÔNG phải nền của sản phẩm — viết để trả lời câu hỏi rồi bỏ; giữ lại kết luận và dữ liệu.**

⚠️ **Dấu hiệu đang trượt khỏi kỷ luật**: thấy mình bắt đầu viết migration, config loader, hay abstraction đa provider ⇒ **dừng lại**. MVP0 ⛔ **không có database**.

---

## Bước 1 — Chuẩn bị môi trường

```bash
pip install dashscope openai pyyaml
cp .env.example .env              # điền DASHSCOPE_API_KEY + 2 giá tham chiếu — ⛔ KHÔNG commit .env
set -a && source .env && set +a   # nạp biến môi trường vào shell
```

⚠️ Nếu quên `DASHSCOPE_API_KEY`, script dừng ngay với thông báo rõ — ⛔ nó ⛔ không chạy tiếp bằng giá trị rỗng. Key phải là của region **Singapore** — key Bắc Kinh ⛔ không dùng được với endpoint `dashscope-intl`.

**Kiểm nhanh ⛔ không tốn tiền:**

```bash
python3 scripts/mvp0/lint_page_prompt.py mvp0/pages/
python3 scripts/mvp0/run_mvp0.py pages --dry-run
```

Kỳ vọng: toàn bộ page YAML trong `mvp0/pages/` lint sạch và compile sạch, in ra số reference và số ràng buộc bị drop mỗi trang.

---

## Bước 2 — Sinh canonical reference

⭐ **Bước này bắt buộc chạy trước.** Story Bible mô tả nhân vật bằng **chữ**; pipeline cần **ảnh**. ⛔ Không có ảnh reference thì *"generate panel với reference"* ⛔ không chạy được.

```bash
python3 scripts/mvp0/run_mvp0.py refs --dry-run   # xem prompt
python3 scripts/mvp0/run_mvp0.py refs             # 3 nhân vật × 3 candidate = 9 ảnh `qwen-image-max` — nằm gọn trong free quota 100 ảnh nếu còn hạn
```

### ⭐ Việc của con người — ⛔ không giao cho máy

Mở `mvp0/run-refs-<timestamp>/candidates/`, với **mỗi** nhân vật chọn **đúng một** ảnh, rồi:

```bash
mkdir -p mvp0/refs
cp mvp0/run-refs-<timestamp>/candidates/lam_uyen-c1.png   mvp0/refs/lam_uyen.png
cp mvp0/run-refs-<timestamp>/candidates/lam_phu-c0.png    mvp0/refs/lam_phu.png
cp mvp0/run-refs-<timestamp>/candidates/bach_y_nu-c2.png  mvp0/refs/bach_y_nu.png
```

**Chọn theo thứ tự ưu tiên:**

1. Khuôn mặt **rõ và dễ nhận lại** — đây là thứ `G1-a` đo suốt 42 panel
2. Trang phục đúng màu Story Bible — `lam_uyen` **đen**, `lam_phu` **nâu sẫm**, `bach_y_nu` **trắng**
3. Vật phẩm phân biệt hiện rõ — nhẫn ngọc **lục** của `lam_phu`, trường kiếm của `bach_y_nu`

> [!IMPORTANT]
> ⭐ **Đây là quyết định sáng tạo đầu tiên của con người trong toàn pipeline** — đúng loại mà **Điều 5a** NĐ 134/2026 đòi hỏi để tác phẩm được bảo hộ.
>
> Ở MVP0 thì **ghi tay** (⛔ không có DB). Ở MVP1 nó **bắt buộc** sinh một dòng `change_log` (`KC-2`). ⇒ Ghi lại: chọn ảnh nào, **vì sao**, ngày nào.

---

## Bước 3 — Sinh trang & crop panel

⭐ **Đơn vị gửi đi sinh ảnh giờ là TRANG (page-level), ⛔ không phải panel.** Một page YAML (`mvp0/pages/<page_id>.yaml`, viết theo `mvp0/prompt-template.txt`) gộp nhiều panel vào một request; ảnh trang sinh ra sau đó được **crop** thành từng panel theo `layout.rows` để chấm điểm `G1` như cũ.

Trước tiên phải có page YAML — dùng skill `/mvp0-page-prompt` (xem [`mvp0/README.md`](../../../mvp0/README.md) mục "Quy trình vận hành") để lập page plan và soạn page YAML từ `mvp0/chapters/chNN.md`, rồi lint:

```bash
python3 scripts/mvp0/lint_page_prompt.py mvp0/pages/ch01_page001.yaml
```

Sinh trang:

```bash
python3 scripts/mvp0/run_mvp0.py pages --dry-run
python3 scripts/mvp0/run_mvp0.py pages
```

**Chạy thử vài trang trước khi chạy cả chương** — rẻ hơn nhiều lần:

```bash
python3 scripts/mvp0/run_mvp0.py pages --page ch01_page001 ch01_page005 -n 3
```

### Output sinh ra

| File | Nội dung | Dùng để |
|---|---|---|
| `prompts/<page_id>.txt` | Prompt tiếng Anh đã compile — **paste-ready**, dùng tay được để thử thủ công trong Gemini | Debug khi ảnh ra sai, hoặc thử nhanh ngoài pipeline |
| `candidates/<page_id>-cK.png` | **Cả N** candidate của trang — ⛔ không xoá cái nào | Nguồn crop panel, chấm `G1-c` |
| `results.jsonl` | Một dòng/trang + xếp hạng VLM | Chấm `G1-b`, `G1-d` |
| `usage.jsonl` | Một dòng/**candidate trang**, kèm `page_id` và `panel_indices` (danh sách `panel_index` thuộc trang đó) | Tính cost, regen ratio `p50/p90` |
| `refusals.jsonl` | Mọi lần provider từ chối | ⚠️ Dữ liệu cho `C-7` |
| `dropped_constraints.jsonl` | Ràng buộc bị cắt do vượt budget | Hiểu vì sao trang thiếu chi tiết |

Sau khi chọn candidate trang ưng ý, crop thành từng panel:

```bash
python3 scripts/mvp0/crop_page.py mvp0/pages/ch01_page001.yaml mvp0/run-pages-<timestamp>/candidates/ch01_page001-c1.png --out mvp0/golden-dataset/panels/
```

`crop_page.py` đọc `layout.rows` trong page YAML để cắt ảnh trang thành `panel-NNN.png` theo đúng `panel_index` toàn cục — golden-dataset và `scoring-sheet.csv` **giữ nguyên schema cấp panel**.

---

## Bước 4 — Chấm gate `G1`

⚠️ **Định nghĩa trước, đo sau.** Ngưỡng đã ký ở bước chuẩn bị — ⛔ đến đây ⛔ **không** sửa.

| # | Chấm gì | Cách chấm | Ngưỡng PASS |
|:-:|---|---|---|
| `G1-a` | Consistency nhân vật | Nhìn **8 panel liền nhau**, tự hỏi *"có nhận ra cùng một người mà ⛔ không cần được nhắc không?"* | **≥70%** |
| `G1-b` | `N` tối thiểu | Chạy lại cùng bộ panel ở `N=2`, so tỉ lệ panel đạt | **N ≤ 3** |
| `G1-c` | Human-reject rate | Chấm pass/fail từng panel **SAU KHI** VLM đã xếp hạng. `reject_rate = số panel người loại / tổng panel VLM chọn` | **≤30%** |
| `G1-d` | Panel nhiều nhân vật | Hai trục **riêng**: (1) đúng người · (2) trang phục/vật phẩm gắn **đúng người** | 2 nhân vật **≥60%** |
| `G1-e` | Đường đi của chữ | Đếm trên trang composite | **100%** overlay, **0** model-render |

> [!WARNING]
> ⭐ **`G1-d` — bắt buộc ghi kèm cỡ mẫu.**
>
> Với cỡ mẫu nhỏ (ví dụ `n=3` panel nhiều nhân vật), giá trị quan sát được chỉ rơi vào một số điểm rời rạc trên thang đo (`0 · 33 · 67 · 100%` với `n=3`) ⇒ **dải PASS-CÓ-ĐIỀU-KIỆN `50–60%` có thể ⛔ không tồn tại trên thang đo**, và **một** panel hỏng có thể làm verdict tụt hàng chục điểm.
>
> ⇒ Báo phần trăm mà ⛔ không nói rõ `n` là biến phép đo trên vài tấm ảnh thành tuyên bố về năng lực model.

### ⭐ Ghi điểm vào đâu — ⛔ không phải vào `run-*/`

Mỗi panel chấm xong ⇒ **thêm một dòng** vào [`mvp0/golden-dataset/scoring-sheet.csv`](../../../mvp0/golden-dataset/scoring-sheet.csv) (13 cột, schema ở [`golden-dataset/README.md`](../../../mvp0/golden-dataset/README.md)). `panel_index` lấy từ page YAML (chỉ số toàn cục xuyên suốt chương), ⛔ không dùng số trang.

| Luật | Vì sao |
|---|---|
| **Append-only** — chấm lại thì **thêm dòng**, ⛔ không sửa dòng cũ | Với 1 người chấm (bus factor = 1), ⭐ **lịch sử đổi ý là thứ gần nhất với một second rater** mà MVP0 có |
| ⭐ Trả lời `readability_verdict` **ngay lúc chấm** | `I2` — ⛔ **không backfill được**. Đóng máy rồi thì cảm nhận *"trang này đọc có ổn không"* ⛔ không tái tạo lại từ ảnh |
| `refusal_count` ghi **riêng**, ⛔ không trộn vào `G1-c` | Provider từ chối và người loại là **hai nguyên nhân khác loại** — trộn làm `reject_rate` mất nghĩa |
| Ảnh output panel lấy từ output của `crop_page.py`, copy sang `golden-dataset/panels/panel-NNN/approved.png` | Cả `run-pages-*/` lẫn output crop tạm đều nằm trong `.gitignore` — ảnh ở đó là ảnh **đang chờ bị xoá** |

### Đo thêm — ⛔ không chặn `G1` nhưng bắt buộc có số

**Regen ratio `p50` / `p90`**, tính từ `run-pages-*/usage.jsonl` (script vẫn đọc tương thích ngược `run-panels-*/usage.jsonl` nếu còn). ⚠️ Thiếu nó thì **`G2` ⛔ KHÔNG CHẠY ĐƯỢC** — ⛔ không PASS mặc định ([Roadmap §6.2](../../010-Planning/Roadmap.md)).

```bash
python3 scripts/mvp0/regen_ratio.py
```

⚠️ **Hai điều script này sẽ nói thẳng, đọc kỹ trước khi trích số:**

1. **Định nghĩa phép chia là `[EM]`** — ⛔ **không** tài liệu nào trong repo định nghĩa công thức regen ratio (đã kiểm `Glossary`, `ADR-018`, `MVP-Scope §7.3`, `Analysis`). Script đếm theo trang: **mỗi candidate trang cộng +1 cho mọi `panel_index` trong `panel_indices` của nó** — nghĩa là một trang phải regen thì **tất cả panel thuộc trang đó** cùng cộng thêm một lượt. Cần Founder xác nhận trước khi số này đi vào `G2`.
2. ⭐ **Phân phối có thể suy biến.** Nếu ⛔ không trang nào phải chạy lại vòng hai thì `p50 = p90 = N` — đó là **hệ quả của thiết kế** (`N=3` cố định, ⛔ không retry-on-failure), ⛔ **chưa** phải một phép đo về tỉ lệ regen thật.

---

## Bước 5 — Ghi verdict và golden dataset

**Verdict `G1`** — điền vào [`mvp0/golden-dataset/g1-verdict.md`](../../../mvp0/golden-dataset/g1-verdict.md), đủ **cả năm** tiêu chí kèm số và **cỡ mẫu**:

| Kết quả | Điều kiện | Hành động |
|---|---|---|
| **PASS** | 5/5 đạt | Đi tiếp MVP1 |
| **PASS CÓ ĐIỀU KIỆN** | `G1-a`,`G1-b`,`G1-e` đạt; `G1-c` ở `30–50%` **hoặc** `G1-d` ở `50–60%` | Đi tiếp, **cứng hoá thêm**: `G1-d` dưới ngưỡng ⇒ **≤2 nhân vật/panel** thay vì ≤3 |
| **FAIL** | Bất kỳ tiêu chí nào vào vùng FAIL | **Đổi cách tiếp cận** — ⚠️ **FAIL ≠ huỷ dự án**; đường đầu tiên là đổi định vị sang storyboard generator |

**Golden dataset (`P-6`)** — 15–20 panel, mỗi panel đủ **4 trường**: Panel Specification (nay trỏ tới `panel_index` trong `mvp0/pages/<page_id>.yaml`) · ảnh reference · ảnh output (crop từ page candidate) · bảng chấm. Vị trí cố định: [`mvp0/golden-dataset/`](../../../mvp0/golden-dataset).

> [!CAUTION]
> ⭐ **Golden dataset ⛔ KHÔNG bị vứt cùng code.** `H6` là `✅` ở **mọi** mốc MVP0–MVP4 và là đầu vào eval kit `M1-6`. Lưu ở vị trí **cố định**, độc lập với thư mục `run-*/` — vì thư mục đó nằm trong `.gitignore`.
>
> ⚠️ Nếu dừng giữa chừng vì vượt ngân sách mà chưa đủ 15 panel: ghi rõ **số panel thực tế** và **lý do dừng**, ⛔ **không** làm tròn lên 15 *"cho đủ"*.

---

## Xử lý sự cố

| Triệu chứng | Nguyên nhân | Xử lý |
|---|---|---|
| `Thieu bien moi truong DASHSCOPE_API_KEY` | Chưa nạp `.env` | `set -a && source .env && set +a` (tạo `.env` từ `.env.example` nếu chưa có) |
| `Thieu reference mvp0/refs/<id>.png` | Chưa chạy bước 2, hoặc chưa copy tay | Quay lại [Bước 2](#bước-2--sinh-canonical-reference) |
| Model id sai / `Model not exist` | Hằng số là **tên model từ tài liệu**, ⛔ chưa verify với console | Sửa `IMAGE_T2I_MODEL_ID` / `IMAGE_EDIT_MODEL_ID` / `VLM_MODEL_ID` trong `providers.py`, pin snapshot có ngày |
| `InvalidParameter` khi sinh ảnh | Model đang pin ⛔ không nhận một param (`n` / `watermark` / `prompt_extend`) | Đối chiếu API reference của model đó trong docs Model Studio, bỏ param không hỗ trợ khỏi `_call_image_api` |
| `DataInspectionFailed` / `IPInfringementSuspect` | Content moderation của Alibaba — kiểm **cả input lẫn output**, ⛔ không chỉnh được mức | Đã ghi tự động vào `refusals.jsonl` (`D-67`) — là dữ liệu `C-7`. Tỉ lệ cao ở batch thăm dò ⇒ cân nhắc đổi mô tả hành động của panel trong page YAML; `prompts/<page_id>.txt` cũng paste-ready để thử tay trong Gemini khi cần đối chiếu |
| `refusals.jsonl` có nhiều dòng | Content policy — panel có hành động bạo lực/nhạy cảm là chỗ rủi ro nhất | ⚠️ **⛔ Đừng bỏ qua**: từ chối nhiều làm `reject_rate` **trộn hai nguyên nhân khác loại** ⇒ verdict `G1-c` mất nghĩa. Ghi lại rồi cân nhắc đổi mô tả panel đó trong page YAML |
| Panel thiếu chi tiết đã ghi trong spec | Vượt constraint budget | Xem `dropped_constraints.jsonl` — ⛔ **không** nới budget; giảm số ràng buộc trong page YAML |
| Nhân vật mặc sai trang phục | Story Bible thiếu/sai trường EN (`canonical_reference_en`, `color_language_en`...) | Kiểm các trường EN của nhân vật trong `story-bible.yaml` khớp mô tả trong page YAML |
| VLM lỗi nhưng ảnh đã sinh | ⭐ **Trạng thái hợp lệ**, ⛔ không phải hỏng | Ảnh vẫn được giữ, `usage` vẫn đã ghi. Chấm tay hoặc chạy lại **chỉ** phần chấm |
| Chi vượt **~$25** mà chưa đủ 8 panel liền nhau | Lặp quá nhiều vòng | Trần thực tế `~$50`. Vượt ⇒ **dừng**, kết luận với dữ liệu đang có |
| `lint_page_prompt.py` báo lỗi thiếu `panel_index` hoặc `character_id` sai | Page YAML chưa khớp `prompt-template.txt`, hoặc dùng tên nhân vật thay vì `character_id` ở trường cấu trúc | Sửa lại theo D4: trường cấu trúc (`characters[].id`, `panels[].characters[].character_id`, `typeset.dialogue[].speaker`) BẮT BUỘC dùng `character_id` |

---

## Tài liệu tham khảo

| Tài liệu | Dùng khi |
|---|---|
| [MVP-Scope §7.2](../../010-Planning/MVP-Scope.md) | Nguồn gốc của 5 tiêu chí `G1` |
| [Roadmap §3.1](../../010-Planning/Roadmap.md) | Ba việc pre-cycle, bảng rủi ro MVP0 |
| [Analysis-MVP0-Requirements](../../050-Research/Analysis-MVP0-Requirements.md) | Phiếu `C-1…C-8`, 8 phát hiện, 6 câu hỏi mở |
| [`mvp0/README.md`](../../../mvp0/README.md) | Bất biến đã cài vào code, giới hạn đo lường |
| [`mvp0/threshold-signoff.md`](../../../mvp0/threshold-signoff.md) | Phiếu ký ngưỡng `[EM]` |
| [`mvp0/golden-dataset/README.md`](../../../mvp0/golden-dataset/README.md) | Schema 13 cột của bảng chấm, luật append-only, luật `readability_verdict` |
| [`mvp0/golden-dataset/g1-verdict.md`](../../../mvp0/golden-dataset/g1-verdict.md) | Phiếu ghi verdict `G1` — Bước 5 điền vào đây |
| [ADR-001](../../030-Specs/Architecture/ADR-001-Backend-And-Frontend-Tech-Stack.md) `#5` | Nghiệm thu tiếng Việt NFC/NFD |
| [ADR-007](../../030-Specs/Architecture/ADR-007-VLM-Provider-For-QA-Select.md) | Hợp đồng VLM, 5 tiêu chí chốt vendor |

---

_Created by Comic Studio_
_Author: trisjr_
