<!-- AI Coding -->

# Verdict gate `G1` — phiếu ghi kết quả

> [!CAUTION]
> ⭐ **Phiếu này chỉ được điền SAU KHI [`scoring-sheet.csv`](./scoring-sheet.csv) đã chấm xong, và ngưỡng ở [`threshold-signoff.md`](../threshold-signoff.md) đã ký TRƯỚC đó.**
>
> ⛔ **Không sửa ngưỡng ở đây.** Ngưỡng đã đóng ở phiếu ký. Phiếu này chỉ ghi **số đo** và **verdict** ([MVP-Scope §7](../../docs/010-Planning/MVP-Scope.md)).

**Ngày chấm**: `2026-09-05` · **Người chấm**: **TrisJr (Founder)** — review bằng mắt ngoài phiên · **Run dùng để chấm**: `mvp0/run-pages-20260905-231040` (33 ảnh, ⛔ **không** crop thành panel)

> [!CAUTION]
> ⛔ **PHIẾU NÀY ⛔ KHÔNG CHỨA MỘT SỐ ĐO NÀO.** MVP0 được **khép bằng quyết định của Founder**, ⛔ **không phải** bằng phép đo `G1`. Biên bản khép ở [§5.1](#51-biên-bản-khép-gate--quyết-định-founder).
>
> ⇒ ⛔ **Không đọc phiếu này như một verdict `G1`.** Mọi ô dưới đây ghi `⛔ KHÔNG ĐO ĐƯỢC` là **sự thật**, ⛔ không phải chỗ chờ điền nốt.

## Mục lục

- [1. Năm tiêu chí — số đo và cỡ mẫu](#1-năm-tiêu-chí--số-đo-và-cỡ-mẫu)
- [2. Đo thêm — regen ratio `p50`/`p90`](#2-đo-thêm--regen-ratio-p50p90)
- [3. Readability — dữ liệu song song](#3-readability--dữ-liệu-song-song)
- [4. Hạn chế đã biết ở tầng canonical reference](#4-hạn-chế-đã-biết-ở-tầng-canonical-reference)
- [5. Verdict](#5-verdict)
  - [5.1. Biên bản khép gate — quyết định Founder](#51-biên-bản-khép-gate--quyết-định-founder)
  - [5.2. Hệ quả kéo theo — cái gì mất đầu vào](#52-hệ-quả-kéo-theo--cái-gì-mất-đầu-vào)
- [6. Tài liệu tham khảo](#6-tài-liệu-tham-khảo)

---

## 1. Năm tiêu chí — số đo và cỡ mẫu

> [!WARNING]
> ⚠️ **Cột `Cỡ mẫu` ⛔ KHÔNG được để trống.** Báo một tỉ lệ mà ⛔ không nói mẫu là biến phép đo trên vài tấm ảnh thành một tuyên bố về năng lực model — đúng thứ [MVP-Scope §7](../../docs/010-Planning/MVP-Scope.md) gọi là *"gate biến thành nghi lễ"*.

| # | Tiêu chí | Ngưỡng PASS | Số đo | **Cỡ mẫu** | Đạt? |
|:-:|---|---|---|---|:-:|
| `G1-a` | Consistency nhân vật | **≥70%** panel | ⛔ **KHÔNG ĐO ĐƯỢC** | `n = 0` panel đã chấm | ⛔ |
| `G1-b` | `N` tối thiểu | **N ≤ 3** | ⛔ **KHÔNG ĐO ĐƯỢC** — ⛔ không có run `N=2` đối chứng | `n = 0` | ⛔ |
| `G1-c` | Human-reject rate sau VLM-select | **≤30%** | ⛔ **KHÔNG ĐO ĐƯỢC** | `n = 0` panel VLM đã chọn | ⛔ |
| `G1-d` | Panel 2 nhân vật — trục **identity** | **≥60%** | ⛔ **KHÔNG ĐO ĐƯỢC** | ⚠️ `n = 0` (⛔ chưa chấm; cỡ mẫu **có sẵn** là 24 panel) | ⛔ |
| `G1-d` | Panel 2 nhân vật — trục **attribute binding** | **≥60%** | ⛔ **KHÔNG ĐO ĐƯỢC** | ⚠️ `n = 0` (⛔ chưa chấm; cỡ mẫu **có sẵn** là 24 panel) | ⛔ |
| `G1-d` | Panel 3 nhân vật | ⛔ **không có ngưỡng chặn** — đo và báo cáo | ⛔ **KHÔNG ĐO ĐƯỢC** | ⚠️ `n = 0` (⛔ chưa chấm; cỡ mẫu **có sẵn** là 4 panel) | — |
| `G1-e` | Đường đi của chữ | **100%** overlay · **0** model-render | ⛔ **KHÔNG ĐO ĐƯỢC** theo đúng định nghĩa (đếm trên **trang composite có bubble**, mà trang composite ⛔ chưa tồn tại) | `n = 0` panel có thoại | ⛔ |

> [!CAUTION]
> ⚠️ **`G1-e` — có quan sát, nhưng ⛔ KHÔNG phải số đo.** Run `231040` ghi nhận `ch01_page005` **3/3** candidate bị model vẽ chữ vào ảnh ([`pages-stage-probe.md` §8.5](../pages-stage-probe.md)). Ngưỡng `G1-e` là **0 model-render** ⇒ quan sát này **⛔ nghịch ngưỡng**.
>
> ⛔ Nhưng nó ⛔ **không được** ghi thành *"`G1-e` FAIL"*: `MVP-Scope §7.2` định nghĩa `G1-e` đếm trên **trang composite có typeset overlay**, và MVP0 ⛔ **chưa bao giờ dựng trang composite nào**. Đây là **tín hiệu cảnh báo mang sang MVP1**, ⛔ không phải một verdict.

⭐ **Cỡ mẫu đã đếm sẵn nhưng ⛔ chưa dùng**: `threshold-signoff.md` ghi chương 1 có **56 panel / 11 trang** — 2 nhân vật: **24** · 3 nhân vật: **4** · 1 nhân vật: **23** · 0 nhân vật: **5**. Nguyên liệu để chấm **⛔ không thiếu**; thứ thiếu là **bước crop và bước chấm**.

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
| `p50` | ⛔ **KHÔNG ĐO ĐƯỢC** | |
| `p90` | ⛔ **KHÔNG ĐO ĐƯỢC** | |
| Số panel tính được | **0** | `regen_ratio.py` chỉ tính panel **đã có ảnh duyệt** — ⛔ không panel nào được duyệt |
| Số panel **loại khỏi phép tính** | **56 / 56** | `approved_candidate_index = none` trên toàn bộ ⇒ ⛔ chưa panel nào xong một vòng |
| Phân phối suy biến? | ☐ có ☐ không — ⛔ **không áp dụng** | ⛔ Không có phân phối để xét |

> [!CAUTION]
> ⭐ **Đây là hệ quả nặng nhất của việc khép MVP0 sớm, ⛔ không phải một ô trống vô hại.**
>
> `MVP-Scope §7.2` nói regen ratio *"⛔ **không** chặn `G1` nhưng **là đầu vào bắt buộc của `G2`**"*, và `G2-a` quy định thiếu dữ liệu ⇒ `G2` **⛔ KHÔNG CHẠY ĐƯỢC**, ⛔ không PASS mặc định. MVP0 đóng lại mà ⛔ không sinh ra `p50`/`p90` ⇒ `G2` giờ phụ thuộc **hoàn toàn** vào `usage_daily` của MVP1 (`M1-7`), ⛔ không còn nguồn thứ hai để đối chứng.

> [!WARNING]
> ⛔ **Thiếu dữ liệu thì ghi "⛔ KHÔNG ĐO ĐƯỢC", ⛔ không bao giờ ghi `0`.** `0` là một giá trị **trông rất tốt** — nó sẽ được đọc thành *"⛔ không ai regen"* thay vì *"chúng ta ⛔ không biết"* ([ADR-018](../../docs/030-Specs/Architecture/ADR-018-Usage-Event-And-Rollup-Model.md) `Q2`).

## 3. Readability — dữ liệu song song

⛔ **Không dùng để pass/fail `G1`.** Ghi lại vì `CF-10.10`: lỗi *"pass mọi check mà ⛔ không ai muốn đọc"* là **vô hình đối với chính hệ thống**.

| Giá trị | Số panel |
|---|---|
| `readable` | **0** |
| `not_readable` | **0** |
| `unscored` | **56** ⚠️ ⛔ không được ngầm coi là `readable` — toàn bộ chương 1 nằm ở đây |
| ⭐ **Panel `pass` kỹ thuật nhưng `not_readable`** | ⛔ **KHÔNG ĐO ĐƯỢC** — đây là con số `CF-10.10` tồn tại để bắt, và nó ⛔ **không được bắt** ở MVP0 |

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
| Cụt tay/chân (`ma_lao`, `gia_gia_que`, `truong_thon`) | ⛔ **KHÔNG KẾT LUẬN ĐƯỢC** | ⛔ Không panel nào được chấm bằng mắt |
| Lưng gù (`tu_ba_ba`) | ⛔ **KHÔNG KẾT LUẬN ĐƯỢC** | ⛔ Không panel nào được chấm bằng mắt |
| Tuổi `tan_muc_thieu_nien` | ⛔ **KHÔNG KẾT LUẬN ĐƯỢC** | ⛔ Không panel nào được chấm bằng mắt |

> [!IMPORTANT]
> ⭐ **Có một thay đổi làm câu hỏi của §4.3 ⛔ KHÔNG còn đúng đề nữa** — phải ghi lại, ⛔ không được để người sau đọc bảng trên mà tưởng chỉ thiếu công chấm.
>
> Run `231040` chạy với cờ **`--no-refs`** ⇒ `mvp0/refs/*.png` ⛔ **không hề được gửi** lên model ở stage `pages` ([`pages-stage-probe.md` §8.2](../pages-stage-probe.md)). Mà §4.3 hỏi *"tầng `pages` có **sửa** được sai lệch nằm trong ảnh ref ⛔ không?"* — câu hỏi này chỉ có nghĩa khi ref **được dùng**.
>
> ⇒ Trên run `231040`, các sai lệch ở [§4.2](#42-sai-lệch-tồn-đọng-trong-mvp0refspng-đã-chọn) **⛔ không còn liên quan** tới ảnh trang: nhân vật ở tầng page chỉ được neo **bằng chữ**. Muốn trả lời §4.3 cho đúng đề, phải chạy lại bằng cấu hình **có ref** (`qwen-image-3.0` + khối `REFERENCE_IMAGES` thuần khẳng định, [§8.8](../pages-stage-probe.md)) — việc đó ⛔ **không** nằm trong MVP0 nữa.

## 5. Verdict

| Kết quả | Điều kiện | Chọn |
|---|---|:-:|
| **PASS** | 5/5 tiêu chí đạt | ☐ |
| **PASS CÓ ĐIỀU KIỆN** | `G1-a`, `G1-b`, `G1-e` đạt; `G1-c` ở `30–50%` **hoặc** `G1-d` ở `50–60%` | ☐ |
| **FAIL** | Bất kỳ tiêu chí nào vào vùng FAIL | ☐ |
| ⭐ **KHÉP KHÔNG ĐO** — ⚠️ ⛔ **không phải** một verdict của `MVP-Scope §7.2` | Founder khép MVP0 khi ⛔ **chưa** tiêu chí nào có số | ☑ |

> [!CAUTION]
> ⭐ **Vì sao ⛔ KHÔNG tick vào PASS, PASS CÓ ĐIỀU KIỆN, hay FAIL.**
>
> Cả ba dải đó là **kết luận rút ra từ số đo**. Ở đây ⛔ **không có số đo nào** ⇒ tick bất kỳ ô nào trong ba ô cũng là **bịa ra một phép đo chưa từng xảy ra**. Kể cả `FAIL` — `FAIL` là một **phát hiện** (*"tiền đề ⛔ không đứng"*), ⛔ không phải chỗ đổ mọi thứ chưa làm xong.
>
> ⇒ Dòng thứ tư được thêm vào **chỉ để nói đúng sự thật**, và nó ⛔ **không** sửa ngưỡng nào ở [`threshold-signoff.md`](../threshold-signoff.md). Tiền lệ có sẵn: `G2-a` của `MVP-Scope §7.3` đã quy định *"**KHÔNG CHẠY ĐƯỢC** ⇒ **lùi gate**, ⛔ không PASS mặc định. Thiếu dữ liệu ⛔ không phải bằng chứng tốt"* — phiếu này áp đúng tinh thần đó cho `G1`.

**Lý do verdict** (bắt buộc, ⛔ không để trống — đây là *"kết luận"* mà kỷ luật MVP0 đòi giữ lại sau khi vứt code):

```
Founder review 33 anh cua run 20260905-231040 bang mat va quyet dinh KHEP MVP0,
chuyen sang MVP1, thay vi chi them API call de hoan tat vong cham diem.

Gate G1 KHONG duoc do. Khong tieu chi nao trong 5 tieu chi co so.
Golden dataset dung lai o muc "spec + ref + page YAML", KHONG co anh panel
va KHONG co bang cham.

Day la mot quyet dinh dieu phoi nguon luc, KHONG phai mot ket luan ky thuat.
Cau hoi ma MVP0 sinh ra de tra loi -- "tien de san pham con dung khong" --
van con NGUYEN, chua duoc tra loi.
```

**Số panel thực tế trong golden dataset**: **`0`** / mục tiêu 15–20.

> [!WARNING]
> ⚠️ Nếu dừng giữa chừng vì vượt ngân sách mà chưa đủ 15 panel: ghi **số thực tế** và **lý do dừng** ở trên. ⛔ **Không làm tròn lên 15** *"cho đủ"*.
>
> ⇒ Số thực tế là **`0`**, và lý do dừng ⛔ **không phải** ngân sách — là **quyết định khép mốc**. Ghi đúng như vậy.

### 5.1. Biên bản khép gate — quyết định Founder

| | |
|---|---|
| **Ngày** | `2026-09-05` |
| **Người quyết** | **TrisJr (Founder)** — chỉ đạo trực tiếp trong phiên, ghi nhận bởi TNMCORE-OS |
| **Nội dung** | Đã review ảnh chương 1; **khép MVP0**, ⛔ không chạy tiếp vòng crop + chấm điểm |
| **Hình thức** | ⚠️ **Khép theo quyết định** — ⛔ **không phải** `G1` PASS |
| **Cái được giữ lại** | `story-bible.yaml` · `mvp0/chapters/ch01.md` · 11 page YAML · 8 canonical ref · **toàn bộ kết luận kỹ thuật** trong [`pages-stage-probe.md`](../pages-stage-probe.md) |
| **Cái ⛔ không có** | `scoring-sheet.csv` (0 dòng) · `panels/` (rỗng) · `p50`/`p90` · verdict `G1` đo được |

⭐ **Giá trị thật MVP0 để lại ⛔ không phải là số `G1`** — mà là **chuỗi kết luận về hành vi model**, thứ mà kỷ luật `MVP-Scope §3.1` gọi là *"giữ lại kết luận và dữ liệu"*:

| # | Kết luận đã mua được bằng tiền API |
|:-:|---|
| 1 | ⭐ **Prompt chỉ được chứa thứ mình MUỐN thấy trên trang.** Tả tấm character sheet → model vẽ tấm sheet. Ghi toạ độ `0.22` → model vẽ chữ `0.22` lên lề. Model ⛔ **không phân biệt** *dữ liệu điều khiển* với *nội dung cần vẽ* |
| 2 | ⭐ **Cấm bằng chữ ⛔ KHÔNG phải một bảo đảm.** Cấm chữ **hai lần** trong prompt, model vẫn vẽ chữ Hán vào ảnh |
| 3 | ⭐ **Lối khẳng định thắng lối phủ định.** Mệnh đề `do_not_copy` ⛔ không ngăn được model chép sheet; bỏ hẳn phần mô tả sheet thì ngăn được |
| 4 | ⭐ **"Nhận được ref" ⛔ KHÔNG bằng "dùng được ref."** Model càng bám ref giỏi thì trang càng hỏng (dán nguyên pose, nhân đôi row) |
| 5 | ⭐ **VLM-select hallucinate khẳng định.** Nó ghi *"Elder Ma (single right arm…) are accurate"* cho tấm ảnh mà nhân vật **có đủ hai tay** ⇒ ⛔ **không** được tin VLM thay mắt người ở MVP1 |
| 6 | ⭐ **Quota là chuyện của từng model, ⛔ không phải của cả account** — `403` ở một model ⛔ không có nghĩa hết đường |

### 5.2. Hệ quả kéo theo — cái gì mất đầu vào

> [!CAUTION]
> ⭐ **Mục này tồn tại để hệ quả ⛔ không diễn ra âm thầm.** Khép `G1` ⛔ không đo ⛔ không phải một việc cục bộ trong `mvp0/` — nó rút đầu vào của bốn thứ đã cam kết ở nơi khác.

| # | Cam kết ở đâu | Nội dung | Trạng thái sau khi khép |
|:-:|---|---|---|
| 1 | [Roadmap mục 2](../../docs/010-Planning/Roadmap.md) `P-2` | *"`G1` có **SỐ** cho cả 5 tiêu chí và verdict được ghi"* | ⛔ **KHÔNG ĐẠT** |
| 2 | [Roadmap mục 2](../../docs/010-Planning/Roadmap.md) `P-3` | *"regen ratio **p50 và p90** có giá trị số"* | ⛔ **KHÔNG ĐẠT** |
| 3 | [Roadmap mục 2](../../docs/010-Planning/Roadmap.md) `P-6` | *"golden dataset tồn tại dưới dạng file (spec + ref + **ảnh** + **bảng chấm**)"* | 🟡 **ĐẠT MỘT NỬA** — có spec + ref, ⛔ không có ảnh panel + bảng chấm |
| 4 | [MVP-Scope §7.3](../../docs/010-Planning/MVP-Scope.md) `G2-a` | Regen ratio là **đầu vào bắt buộc** của `G2` | ⚠️ `G2` giờ phụ thuộc **hoàn toàn** vào `usage_daily` của MVP1 (`M1-7`), ⛔ mất nguồn đối chứng |
| 5 | [Roadmap mục 3](../../docs/010-Planning/Roadmap.md) `M1-6` | *"eval kit chạy được trên **golden dataset của MVP0** và cho ra số"* | ⚠️ **Mất baseline** — eval kit MVP1 ⛔ không có bộ ảnh + điểm chuẩn để so hồi quy |
| 6 | [Roadmap mục 3](../../docs/010-Planning/Roadmap.md) `M1-3` | *"extraction ≥80% khớp **Story Bible viết tay của MVP0**"* | ✅ **⛔ Không ảnh hưởng** — `story-bible.yaml` được giữ nguyên |

⚠️ ⭐ **Mục 5 là hệ quả đắt nhất, và nó ⛔ không hiển thị ngay.** `Roadmap mục 6` xếp *"Golden dataset của MVP0 → eval kit MVP1"* là phụ thuộc **mềm** — *"có thể dựng lại, nhưng dựng lại **tốn tiền API lần hai**"*. ⇒ Cái giá của việc khép sớm ⛔ không mất đi, nó chỉ **dời sang MVP1**.

⇒ ⭐ **Việc phải làm ở MVP1, ⛔ không được quên**: khi dựng eval kit (`M1-6`), phải **cấp lại ngân sách API** để sinh bộ ảnh baseline — hoặc chấp nhận eval kit chạy ⛔ **không** có điểm chuẩn hồi quy.

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
