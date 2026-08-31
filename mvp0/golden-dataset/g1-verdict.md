<!-- AI Coding -->

# Verdict gate `G1` — phiếu ghi kết quả

> [!CAUTION]
> ⭐ **Phiếu này chỉ được điền SAU KHI [`scoring-sheet.csv`](./scoring-sheet.csv) đã chấm xong, và ngưỡng ở [`threshold-signoff.md`](../threshold-signoff.md) đã ký TRƯỚC đó.**
>
> ⛔ **Không sửa ngưỡng ở đây.** Ngưỡng đã đóng ở phiếu ký. Phiếu này chỉ ghi **số đo** và **verdict** ([MVP-Scope §7](../../docs/010-Planning/MVP-Scope.md)).

**Ngày chấm**: `__________` · **Người chấm**: `__________` · **Run dùng để chấm**: `__________`

## Mục lục

- [1. Năm tiêu chí — số đo và cỡ mẫu](#1-năm-tiêu-chí--số-đo-và-cỡ-mẫu)
- [2. Đo thêm — regen ratio `p50`/`p90`](#2-đo-thêm--regen-ratio-p50p90)
- [3. Readability — dữ liệu song song](#3-readability--dữ-liệu-song-song)
- [4. Verdict](#4-verdict)
- [5. Tài liệu tham khảo](#5-tài-liệu-tham-khảo)

---

## 1. Năm tiêu chí — số đo và cỡ mẫu

> [!WARNING]
> ⚠️ **Cột `Cỡ mẫu` ⛔ KHÔNG được để trống.** Báo một tỉ lệ mà ⛔ không nói mẫu là biến phép đo trên vài tấm ảnh thành một tuyên bố về năng lực model — đúng thứ [MVP-Scope §7](../../docs/010-Planning/MVP-Scope.md) gọi là *"gate biến thành nghi lễ"*.

| # | Tiêu chí | Ngưỡng PASS | Số đo | **Cỡ mẫu** | Đạt? |
|:-:|---|---|---|---|:-:|
| `G1-a` | Consistency nhân vật | **≥70%** panel | `____%` | `n = ____` | ☐ |
| `G1-b` | `N` tối thiểu | **N ≤ 3** | `N = ____` | `n = ____` panel chạy lại ở `N=2` | ☐ |
| `G1-c` | Human-reject rate sau VLM-select | **≤30%** | `____%` | `n = ____` panel VLM đã chọn | ☐ |
| `G1-d` | Panel 2 nhân vật — trục **identity** | **≥60%** | `____%` | ⚠️ `n = ____` | ☐ |
| `G1-d` | Panel 2 nhân vật — trục **attribute binding** | **≥60%** | `____%` | ⚠️ `n = ____` | ☐ |
| `G1-d` | Panel 3 nhân vật | ⛔ **không có ngưỡng chặn** — đo và báo cáo | `____%` | ⚠️ `n = ____` | — |
| `G1-e` | Đường đi của chữ | **100%** overlay · **0** model-render | `____` overlay / `____` model-render | `n = ____` panel có thoại | ☐ |

> [!CAUTION]
> ⭐ **`G1-d` với `n=3` — dải PASS-CÓ-ĐIỀU-KIỆN ⛔ KHÔNG TỒN TẠI trên thang đo.**
>
> Với bộ panel script hiện có: **n=3** panel hai nhân vật (14, 15, 18) và **n=1** panel ba nhân vật (16). Giá trị quan sát được **chỉ có thể là** `0 · 33 · 67 · 100%` ⇒ dải `50–60%` ⛔ không đạt tới được, và **một** panel hỏng làm verdict tụt **33 điểm phần trăm**.
>
> ⇒ Chọn **một** trong hai, ghi rõ vào [mục 4](#4-verdict):
>
> - ☐ **Nâng cỡ mẫu** trước khi chấm — bổ sung một chương có hội thoại nhiều người
> - ☐ **Ghi `G1-d` là đo-và-báo-cáo**, ⛔ không dùng làm điều kiện chặn

**Hai trục của `G1-d` chấm RIÊNG** (`CF-6.5` `[OFF]`: ID-Sim sụp từ **42.33** ở 2 người xuống **27.21** ở 3 người). ⛔ Không gộp hai trục thành một điểm.

## 2. Đo thêm — regen ratio `p50`/`p90`

⚠️ ⛔ **Không chặn `G1`, nhưng BẮT BUỘC có số**: thiếu nó thì **`G2` ⛔ KHÔNG CHẠY ĐƯỢC** — ⛔ không PASS mặc định ([Roadmap §6.2](../../docs/010-Planning/Roadmap.md) · `G2-a`).

```bash
python3 scripts/mvp0/regen_ratio.py
```

| Đại lượng | Giá trị | Ghi chú |
|---|---|---|
| `p50` | `______` | |
| `p90` | `______` | |
| Số panel tính được | `______` | Chỉ panel **đã có ảnh duyệt** |
| Số panel **loại khỏi phép tính** | `______` | `approved_candidate_index = none` ⇒ ⛔ chưa xong một vòng, ⛔ không được tính |
| Phân phối suy biến? | ☐ có ☐ không | ⚠️ Nếu mọi panel đều đúng `N` ảnh (⛔ không vòng nào lặp lại) thì `p50 = p90 = N` và con số này ⛔ **chưa mang thông tin về tỉ lệ regen thật** — ghi rõ, ⛔ đừng trình bày nó như một phép đo |

> [!WARNING]
> ⛔ **Thiếu dữ liệu thì ghi "⛔ KHÔNG ĐO ĐƯỢC", ⛔ không bao giờ ghi `0`.** `0` là một giá trị **trông rất tốt** — nó sẽ được đọc thành *"⛔ không ai regen"* thay vì *"chúng ta ⛔ không biết"* ([ADR-018](../../docs/030-Specs/Architecture/ADR-018-Usage-Event-And-Rollup-Model.md) `Q2`).

## 3. Readability — dữ liệu song song

⛔ **Không dùng để pass/fail `G1`.** Ghi lại vì `CF-10.10`: lỗi *"pass mọi check mà ⛔ không ai muốn đọc"* là **vô hình đối với chính hệ thống**.

| Giá trị | Số panel |
|---|---|
| `readable` | `______` |
| `not_readable` | `______` |
| `unscored` | `______` ⚠️ ⛔ không được ngầm coi là `readable` |
| ⭐ **Panel `pass` kỹ thuật nhưng `not_readable`** | `______` — đây là con số `CF-10.10` tồn tại để bắt |

## 4. Verdict

| Kết quả | Điều kiện | Chọn |
|---|---|:-:|
| **PASS** | 5/5 tiêu chí đạt | ☐ |
| **PASS CÓ ĐIỀU KIỆN** | `G1-a`, `G1-b`, `G1-e` đạt; `G1-c` ở `30–50%` **hoặc** `G1-d` ở `50–60%` | ☐ |
| **FAIL** | Bất kỳ tiêu chí nào vào vùng FAIL | ☐ |

**Nếu PASS CÓ ĐIỀU KIỆN** — ghi phần cứng hoá thêm: `G1-d` dưới ngưỡng ⇒ **≤2 nhân vật/panel** thay vì ≤3.

**Nếu FAIL** — ⚠️ **FAIL ≠ huỷ dự án**. Đường đầu tiên là **đổi định vị sang storyboard generator** ([MVP-Scope §7.2](../../docs/010-Planning/MVP-Scope.md)).

**Lý do verdict** (bắt buộc, ⛔ không để trống — đây là *"kết luận"* mà kỷ luật MVP0 đòi giữ lại sau khi vứt code):

```
______________________________________________________________
______________________________________________________________
```

**Số panel thực tế trong golden dataset**: `______` / mục tiêu 15–20.

> [!WARNING]
> ⚠️ Nếu dừng giữa chừng vì vượt ngân sách mà chưa đủ 15 panel: ghi **số thực tế** và **lý do dừng** ở trên. ⛔ **Không làm tròn lên 15** *"cho đủ"*.

## 5. Tài liệu tham khảo

| Tài liệu | Dùng khi |
|---|---|
| [Chay-MVP0 Bước 4–5](../../docs/060-Manuals/User-Guide/Chay-MVP0.md) | Cách chấm từng tiêu chí |
| [MVP-Scope §7.2](../../docs/010-Planning/MVP-Scope.md) | Nguồn gốc 5 tiêu chí `G1` và ba dải verdict |
| [`threshold-signoff.md`](../threshold-signoff.md) | Ngưỡng đã ký — ⛔ không sửa ở đây |
| [`README.md`](./README.md) | Schema bảng chấm, luật append-only |

---

_Created by Comic Studio_
_Author: trisjr_
