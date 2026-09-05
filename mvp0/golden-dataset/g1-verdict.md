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
- [4. Hạn chế đã biết ở tầng canonical reference](#4-hạn-chế-đã-biết-ở-tầng-canonical-reference)
- [5. Verdict](#5-verdict)
- [6. Tài liệu tham khảo](#6-tài-liệu-tham-khảo)

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
> ⭐ **`G1-d` — lưu ý cỡ mẫu panel nhiều nhân vật.**
>
> Kiểm tra cỡ mẫu panel 2 nhân vật và 3 nhân vật trong panel script của chương mới trước khi chấm. Nếu cỡ mẫu quá nhỏ (ví dụ $n \le 3$), dải PASS-CÓ-ĐIỀU-KIỆN (50–60%) có thể không tồn tại trên thang đo.
>
> ⇒ Luôn ghi kèm cỡ mẫu $n = \dots$ khi báo cáo kết quả `G1-d`.
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

## 4. Hạn chế đã biết ở tầng canonical reference

> [!CAUTION]
> ⭐ **Đọc mục này TRƯỚC khi chấm `G1-a`.** Các sai lệch dưới đây đã có sẵn **trong chính ảnh reference** khi chọn (`2026-09-05`), ⛔ **không phải** lỗi nhất quán của model ở tầng page. Chấm chúng vào `G1-a` là **đo nhầm** — nó biến một giới hạn đã biết của `refs` thành một tuyên bố sai về năng lực giữ nhân vật của model.

### 4.1. Hai loại lỗi — ⛔ không gộp

| Loại | Bản chất | Sửa được bằng chữ? | Bằng chứng |
|---|---|---|---|
| **Loại 1 — dữ kiện ⛔ không tới được prompt** | `character_sheet_prompt` chỉ đọc **5 khóa** `canonical_reference_en` (`khuon_mat`, `mat`, `toc`, `trang_phuc`, `dac_diem_rieng`) + `ten_en`. Nó ⛔ **không** đọc `tuoi`, `gioi_tinh`, `body_type_relative_en`, `silhouette_cue_en`, `personality_en`, và gửi **0 negative constraint** | ✅ **Có** — chuyển dữ kiện vào 5 khóa đó | `yeu_phu_bo` vẽ ra chân dung nửa người có vai áo cho tới khi hình dạng bốn chân được đưa vào `dac_diem_rieng`; `tan_muc_thieu_nien` ra thanh niên 18–20 cho tới khi tuổi được đưa vào `khuon_mat` |
| **Loại 2 — model cưỡng lại trong khung model sheet** | Prompt `refs` mở đầu bằng *"2D anime character design model sheet, multiple angle views"*. Convention này kéo mọi thứ về **giải phẫu người tiêu chuẩn** | ⛔ **Không** — dữ kiện ĐÃ nằm đúng khóa mà vẫn bị bỏ qua | `tu_ba_ba` có *"pronounced hunched back"* trong `dac_diem_rieng` nhưng 3/3 candidate vẽ lưng thẳng |

### 4.2. Sai lệch tồn đọng trong `mvp0/refs/*.png` đã chọn

| char_id | Bible yêu cầu | Ref thực tế | Loại | Hệ quả khi chấm |
|---|---|---|---|---|
| `ma_lao` | Chỉ còn **tay phải**; vai trái là đường may tròn, tay áo rỗng thắt nút | Đủ **hai tay** | 2 | ⛔ Không tính vào `G1-a` |
| `gia_gia_que` | **Cụt chân phải** trên gối, chống gậy gỗ | Đủ **hai chân** | 2 | ⛔ Không tính vào `G1-a` |
| `truong_thon` | **Chỉ còn thân mình** — hai vai cụt tròn, thân hết dưới hông | Đủ **tay, chân, bàn chân** | 2 | ⛔ Không tính vào `G1-a` |
| `tu_ba_ba` | **Lưng gù rõ** (`silhouette_cue` chính) | Lưng thẳng | 2 | ⚠️ `silhouette_cue` của nhân vật này ⛔ **không đo được** ở chương 1 |
| `tan_muc_thieu_nien` | **11 tuổi** | ⛔ Không còn là người lớn 18–20, nhưng **vẫn lệch — đọc ra ~7–9 tuổi** | **1 → 2** (xem §4.2b) | ⚠️ Ghi rõ khi đọc mọi số đo tỉ lệ chiều cao — cả dàn nhân vật lấy `Qin Mu at eleven` làm thước đo |
| `tan_muc_thieu_nien` | Tóc **buộc hờ sau gáy** · ⛔ không có quần | Búi tó **trên đỉnh đầu** · có **quần đen** | 2 | ⛔ Không tính vào `G1-a`. ⚠️ Có ở **cả** run gốc lẫn run sửa ⇒ ⛔ không phải hồi quy do sửa chữ |

### 4.2b. Tuổi `tan_muc_thieu_nien` — hai giả thuyết đã thử, kết quả thật

⭐ Ghi lại đầy đủ vì đây là **kết luận** mà kỷ luật MVP0 đòi giữ lại sau khi vứt code — ⛔ không phải nhật ký thao tác.

| Vòng | Giả thuyết | Chữ đã dùng | Kết quả thật |
|:-:|---|---|---|
| **0** | — | `khuon_mat: "Delicate handsome boyish face..."` | ⛔ **Thanh niên 18–20**, 3/3 |
| **1** | Loại 1 — tuổi ⛔ không tới được prompt vì nằm ở `tuoi` / `body_type_relative_en` | ⚠️ Đổi **4 thứ cùng lúc**: tuổi vào `khuon_mat` · bỏ `"handsome"` · `"child-sized"` vào `trang_phuc` · `"head large relative to a short slim body"` vào `dac_diem_rieng` | ✅ **Hết người lớn** — giả thuyết loại 1 **đúng**. ⚠️ Nhưng quá đà, ra ~7–8. *Lúc đó nghi mệnh đề tỉ lệ đầu là thủ phạm* |
| **2** | Còn dư loại 1 — thay tính từ tỉ lệ bằng **neo chiều cao đo được** lấy từ `chieu_cao_the_trang` | `"a slim eleven-year-old standing about shoulder-high to an adult"` (bỏ hẳn mệnh đề tỉ lệ đầu) | ⛔ **Thất bại.** Tỉ lệ đầu/thân ⛔ **không đổi** (~1:4.5, vẫn ~7–9 tuổi), 3/3. ⚠️ Lại còn sinh thêm **băng vải quấn tay** — món ⛔ không có trong bible |

> [!WARNING]
> ⚠️ **Vòng 2 BÁC BỎ nghi vấn của vòng 1.** Vòng 1 đổi 4 thứ cùng lúc nên ⛔ không tách được nguyên nhân. Vòng 2 cô lập đúng một biến — bỏ hẳn mệnh đề `"head large..."` — và tỉ lệ **⛔ không nhúc nhích**. ⇒ Mệnh đề đó **⛔ KHÔNG phải thủ phạm**. Nét trẻ con cách điệu đến từ chính chữ `"eleven-year-old boy"` gặp khung model sheet.

> [!IMPORTANT]
> ⭐ **Kết luận: mốc 11 tuổi là lỗi LOẠI 2, ⛔ không phải loại 1 còn sót.**
>
> Loại 1 **có thật và đã đóng** ở vòng 1 — bằng chứng là *"người lớn → trẻ con"*. Nhưng khoảng cách còn lại (*trẻ con ~7–9* → *đúng 11*) **⛔ không nhúc nhích** trước một neo chiều cao cụ thể, đo được, lấy thẳng từ bible. ⇒ Khung *"2D anime character design model sheet"* áp một **tỉ lệ trẻ em cách điệu** mà chữ trong 5 khóa ⛔ không điều khiển được.
>
> ⇒ ⛔ **Không chi thêm call cho hướng "viết chữ khác đi"** ở tầng `refs`. Nếu cần đúng 11 tuổi, đòn bẩy còn lại nằm **ngoài** 5 khóa: sửa `character_sheet_prompt` để gửi `body_type_relative_en`, hoặc bỏ cụm *"character model sheet"* khỏi prompt `refs` — cả hai đều là **sửa script**, ⛔ ngoài phạm vi MVP0 hiện tại.

**Ref giữ lại là vòng 1 (`172723/c2`), ⛔ không phải vòng 2** — cùng độ lệch tuổi, nhưng vòng 2 có thêm băng vải quấn tay, tức là **nhiều sai lệch hơn**.

### 4.3. Điều mục này ⛔ CHƯA kết luận

⚠️ `refs` gửi **0 negative constraint**; tầng `pages` thì **có** khối `NEGATIVE_CONSTRAINTS`. ⇒ ⛔ **Chưa thể kết luận** rằng loại 2 cũng hỏng ở tầng page. Sau khi chạy `pages`, quay lại đây và ghi kết quả thật:

| Sai lệch | `pages` có sửa được ⛔ không? | Ghi chú |
|---|---|---|
| Cụt tay/chân (`ma_lao`, `gia_gia_que`, `truong_thon`) | ☐ có ☐ không | |
| Lưng gù (`tu_ba_ba`) | ☐ có ☐ không | |
| Tuổi `tan_muc_thieu_nien` | ☐ có ☐ không | |

## 5. Verdict

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

## 6. Tài liệu tham khảo

| Tài liệu | Dùng khi |
|---|---|
| [Chay-MVP0 Bước 4–5](../../docs/060-Manuals/User-Guide/Chay-MVP0.md) | Cách chấm từng tiêu chí |
| [MVP-Scope §7.2](../../docs/010-Planning/MVP-Scope.md) | Nguồn gốc 5 tiêu chí `G1` và ba dải verdict |
| [`threshold-signoff.md`](../threshold-signoff.md) | Ngưỡng đã ký — ⛔ không sửa ở đây |
| [`README.md`](./README.md) | Schema bảng chấm, luật append-only |

---

_Created by Comic Studio_
_Author: trisjr_
