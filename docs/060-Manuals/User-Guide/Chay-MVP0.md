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
- [Bước 3 — Sinh panel](#bước-3--sinh-panel)
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
| **2** | **Verify hai model id** trong [`scripts/mvp0/providers.py`](../../../scripts/mvp0/providers.py) | Hai hằng số là **tên sản phẩm** lấy từ tài liệu, ⛔ **chưa đối chiếu** với model id thật của API |
| **3** | **Chốt ngân sách** | Chương comic #1: **~$8,84** · trọn chương chữ: **~$16,88** ⚠️ vượt trần `~$12`. Trần thực tế `~$50` |

### Kỷ luật ⛔ không được quên

> **Code của MVP0 KHÔNG phải nền của sản phẩm — viết để trả lời câu hỏi rồi bỏ; giữ lại kết luận và dữ liệu.**

⚠️ **Dấu hiệu đang trượt khỏi kỷ luật**: thấy mình bắt đầu viết migration, config loader, hay abstraction đa provider ⇒ **dừng lại**. MVP0 ⛔ **không có database**.

---

## Bước 1 — Chuẩn bị môi trường

```bash
pip install google-genai pyyaml
export GEMINI_API_KEY="..."   # ⛔ KHÔNG hardcode vào file nào
```

⚠️ Nếu quên `GEMINI_API_KEY`, script dừng ngay với thông báo rõ — ⛔ nó ⛔ không chạy tiếp bằng giá trị rỗng.

**Kiểm nhanh ⛔ không tốn tiền:**

```bash
python3 scripts/mvp0/run_mvp0.py panels --chapter all --dry-run
```

Kỳ vọng: **42 panel** compile sạch, in ra số reference và số ràng buộc bị drop mỗi panel.

---

## Bước 2 — Sinh canonical reference

⭐ **Bước này bắt buộc chạy trước.** Story Bible mô tả nhân vật bằng **chữ**; pipeline cần **ảnh**. ⛔ Không có ảnh reference thì *"generate panel với reference"* ⛔ không chạy được.

```bash
python3 scripts/mvp0/run_mvp0.py refs --dry-run   # xem prompt
python3 scripts/mvp0/run_mvp0.py refs             # 3 nhân vật × 3 candidate = 9 ảnh (~$1,21)
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

## Bước 3 — Sinh panel

```bash
python3 scripts/mvp0/run_mvp0.py panels --chapter ch1 --dry-run
python3 scripts/mvp0/run_mvp0.py panels --chapter ch1
```

**Chạy thử vài panel trước khi chạy cả chương** — rẻ hơn nhiều lần:

```bash
python3 scripts/mvp0/run_mvp0.py panels --chapter ch1 --panels 9 16 21
```

⭐ Ba panel này chọn có chủ ý: **9** (1 nhân vật, ảnh lớn) · **16** (⭐ **3 nhân vật + attribute binding** — panel khó nhất) · **21** (0 nhân vật, `text_safe_zone` rỗng).

### Output sinh ra

| File | Nội dung | Dùng để |
|---|---|---|
| `prompts/panel-NNN.txt` | Prompt đã compile | Debug khi ảnh ra sai |
| `candidates/panel-NNN-cK.png` | **Cả 3** candidate — ⛔ không xoá cái nào | Chấm `G1-c` |
| `results.jsonl` | Một dòng/panel + xếp hạng VLM | Chấm `G1-b`, `G1-d` |
| `usage.jsonl` | Một dòng/**candidate** | Tính cost, regen ratio `p50/p90` |
| `refusals.jsonl` | Mọi lần provider từ chối | ⚠️ Dữ liệu cho `C-7` |
| `dropped_constraints.jsonl` | Ràng buộc bị cắt do vượt budget | Hiểu vì sao panel thiếu chi tiết |

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
> Chương này chỉ có **n=3** panel hai nhân vật (14, 15, 18) và **n=1** panel ba nhân vật (16). Với `n=3`, giá trị quan sát được chỉ có thể là `0 · 33 · 67 · 100%` ⇒ **dải PASS-CÓ-ĐIỀU-KIỆN `50–60%` ⛔ không tồn tại trên thang đo**, và **một** panel hỏng làm verdict tụt **33 điểm**.
>
> ⇒ Báo `67%` mà ⛔ không nói `n=3` là biến phép đo trên **ba tấm ảnh** thành tuyên bố về năng lực model.

### Đo thêm — ⛔ không chặn `G1` nhưng bắt buộc có số

**Regen ratio `p50` / `p90`**, tính từ `usage.jsonl`. ⚠️ Thiếu nó thì **`G2` ⛔ KHÔNG CHẠY ĐƯỢC** — ⛔ không PASS mặc định ([Roadmap §6.2](../../010-Planning/Roadmap.md)).

---

## Bước 5 — Ghi verdict và golden dataset

**Verdict `G1`** — ghi đủ **cả năm** tiêu chí kèm số và cỡ mẫu:

| Kết quả | Điều kiện | Hành động |
|---|---|---|
| **PASS** | 5/5 đạt | Đi tiếp MVP1 |
| **PASS CÓ ĐIỀU KIỆN** | `G1-a`,`G1-b`,`G1-e` đạt; `G1-c` ở `30–50%` **hoặc** `G1-d` ở `50–60%` | Đi tiếp, **cứng hoá thêm**: `G1-d` dưới ngưỡng ⇒ **≤2 nhân vật/panel** thay vì ≤3 |
| **FAIL** | Bất kỳ tiêu chí nào vào vùng FAIL | **Đổi cách tiếp cận** — ⚠️ **FAIL ≠ huỷ dự án**; đường đầu tiên là đổi định vị sang storyboard generator |

**Golden dataset (`P-6`)** — 15–20 panel, mỗi panel đủ **4 trường**: Panel Specification · ảnh reference · ảnh output · bảng chấm.

> [!CAUTION]
> ⭐ **Golden dataset ⛔ KHÔNG bị vứt cùng code.** `H6` là `✅` ở **mọi** mốc MVP0–MVP4 và là đầu vào eval kit `M1-6`. Lưu ở vị trí **cố định**, độc lập với thư mục `run-*/` — vì thư mục đó nằm trong `.gitignore`.
>
> ⚠️ Nếu dừng giữa chừng vì vượt ngân sách mà chưa đủ 15 panel: ghi rõ **số panel thực tế** và **lý do dừng**, ⛔ **không** làm tròn lên 15 *"cho đủ"*.

---

## Xử lý sự cố

| Triệu chứng | Nguyên nhân | Xử lý |
|---|---|---|
| `Thieu bien moi truong GEMINI_API_KEY` | Chưa export | `export GEMINI_API_KEY="..."` |
| `Thieu reference mvp0/refs/<id>.png` | Chưa chạy bước 2, hoặc chưa copy tay | Quay lại [Bước 2](#bước-2--sinh-canonical-reference) |
| Model id sai / `404` | Hằng số là **tên sản phẩm**, ⛔ chưa verify | Sửa `IMAGE_MODEL_ID` / `VLM_MODEL_ID` trong `providers.py` |
| `refusals.jsonl` có nhiều dòng | Content policy — panel **18** (kiếm xuyên ngực + máu) là chỗ rủi ro nhất | ⚠️ **⛔ Đừng bỏ qua**: từ chối nhiều làm `reject_rate` **trộn hai nguyên nhân khác loại** ⇒ verdict `G1-c` mất nghĩa. Ghi lại rồi cân nhắc đổi `action` của panel đó |
| Panel thiếu chi tiết đã ghi trong spec | Vượt constraint budget | Xem `dropped_constraints.jsonl` — ⛔ **không** nới budget; giảm số ràng buộc trong panel script |
| Nhân vật mặc sai trang phục | `state_ref` sai hoặc thiếu | Kiểm `visual_constraints.state_ref` khớp `moc` trong Story Bible |
| VLM lỗi nhưng ảnh đã sinh | ⭐ **Trạng thái hợp lệ**, ⛔ không phải hỏng | Ảnh vẫn được giữ, `usage` vẫn đã ghi. Chấm tay hoặc chạy lại **chỉ** phần chấm |
| Chi vượt **~$25** mà chưa đủ 8 panel liền nhau | Lặp quá nhiều vòng | Trần thực tế `~$50`. Vượt ⇒ **dừng**, kết luận với dữ liệu đang có |

---

## Tài liệu tham khảo

| Tài liệu | Dùng khi |
|---|---|
| [MVP-Scope §7.2](../../010-Planning/MVP-Scope.md) | Nguồn gốc của 5 tiêu chí `G1` |
| [Roadmap §3.1](../../010-Planning/Roadmap.md) | Ba việc pre-cycle, bảng rủi ro MVP0 |
| [Analysis-MVP0-Requirements](../../050-Research/Analysis-MVP0-Requirements.md) | Phiếu `C-1…C-8`, 8 phát hiện, 6 câu hỏi mở |
| [`mvp0/README.md`](../../../mvp0/README.md) | Bất biến đã cài vào code, giới hạn đo lường |
| [`mvp0/threshold-signoff.md`](../../../mvp0/threshold-signoff.md) | Phiếu ký ngưỡng `[EM]` |
| [ADR-001](../../030-Specs/Architecture/ADR-001-Backend-And-Frontend-Tech-Stack.md) `#5` | Nghiệm thu tiếng Việt NFC/NFD |
| [ADR-007](../../030-Specs/Architecture/ADR-007-VLM-Provider-For-QA-Select.md) | Hợp đồng VLM, 5 tiêu chí chốt vendor |

---

_Created by TNMCORE-OS_
_Author: trisjr_
