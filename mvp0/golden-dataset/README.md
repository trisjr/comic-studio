<!-- AI Coding -->

# Golden dataset MVP0 — bảng chấm `P-6`

> Đây là **nơi cố định** của golden dataset. Nó ⛔ **không** nằm trong `run-*/` — thư mục đó nằm trong [`.gitignore`](../../.gitignore) và sẽ mất cùng code MVP0.
>
> [!CAUTION]
> ⭐ **Golden dataset ⛔ KHÔNG bị vứt cùng code MVP0.** `H6` là `✅` ở **mọi** mốc MVP0–MVP4 và là **đầu vào của eval kit `M1-6`** ([MVP-Scope §3](../../docs/010-Planning/MVP-Scope.md) · [Roadmap §6.2](../../docs/010-Planning/Roadmap.md)). Script sinh ảnh thì vứt; **kết luận và dữ liệu thì giữ**.

## Mục lục

- [1. Vì sao bảng chấm phải tồn tại TRƯỚC tấm ảnh đầu tiên](#1-vì-sao-bảng-chấm-phải-tồn-tại-trước-tấm-ảnh-đầu-tiên)
- [2. Bốn trường mỗi panel](#2-bốn-trường-mỗi-panel)
- [3. Schema `scoring-sheet.csv`](#3-schema-scoring-sheetcsv)
- [4. Luật ghi — append-only, ⛔ không ghi đè](#4-luật-ghi--append-only-⛔-không-ghi-đè)
- [5. `readability_verdict` — cột tách biệt, ⛔ không suy từ điểm kỹ thuật](#5-readability_verdict--cột-tách-biệt-⛔-không-suy-từ-điểm-kỹ-thuật)
- [6. Quy trình chấm một panel](#6-quy-trình-chấm-một-panel)
- [7. Tài liệu tham khảo](#7-tài-liệu-tham-khảo)

---

## 1. Vì sao bảng chấm phải tồn tại TRƯỚC tấm ảnh đầu tiên

Ba lý do độc lập, mỗi lý do tự đủ:

| # | Lý do | Nguồn |
|:-:|---|---|
| **1** | **Định nghĩa trước, đo sau.** *"Không sửa ngưỡng sau khi nhìn thấy kết quả — đó là cách một gate biến thành nghi lễ."* Dựng bảng chấm sau khi đã xem ảnh là cùng một lỗi ở dạng nhẹ hơn: cột nào cũng có thể được chọn cho **khớp** với ảnh vừa thấy | [MVP-Scope §7](../../docs/010-Planning/MVP-Scope.md) · [`threshold-signoff.md`](../threshold-signoff.md) |
| **2** | ⭐ **Câu trả lời readability ⛔ không backfill được.** `Story-Record-Readability-Human-Judgement` là **`I2`** — *"không làm bây giờ ⇒ dữ liệu quá khứ mất vĩnh viễn"*. Người chấm xong, đóng máy, thì cảm nhận *"trang này đọc có ổn không"* ⛔ không tái tạo lại được từ ảnh | [Story-Record-Readability-Human-Judgement](../../docs/022-User-Stories/Backlog/Story-Record-Readability-Human-Judgement.md) · [Backlog-Priority §3.1](../../docs/022-User-Stories/Backlog-Priority.md) |
| **3** | `run-*/` **nằm trong `.gitignore`**. Chấm vào một file trong đó = chấm vào thứ sẽ biến mất | [`.gitignore`](../../.gitignore) · [Chay-MVP0 Bước 5](../../docs/060-Manuals/User-Guide/Chay-MVP0.md) |

⚠️ **Hình dạng "log tay" là ĐÚNG cho MVP0, ⛔ không phải sự tạm bợ.** [MVP-Scope §3](../../docs/010-Planning/MVP-Scope.md) hàng `F1` ghi ô MVP0 là **`🟡 log tay`** — CSV append-only chính là hình dạng đó. ⛔ **Đừng** dựng database hay migration ở đây; đó là dấu hiệu sớm của rủi ro *"spike biến thành nền móng"* ([Roadmap §3.1](../../docs/010-Planning/Roadmap.md)).

## 2. Bốn trường mỗi panel

[Chay-MVP0 Bước 5](../../docs/060-Manuals/User-Guide/Chay-MVP0.md) đòi **15–20 panel**, mỗi panel đủ **bốn** trường:

| # | Trường | Ở đâu |
|:-:|---|---|
| 1 | **Panel Specification** | ⛔ Không copy — trỏ tới `panel_index` trong [`panel-script-ch1.yaml`](../panel-script-ch1.yaml) / [`ch2`](../panel-script-ch2.yaml). Một nguồn sự thật, ⛔ không nhân bản |
| 2 | **Ảnh reference** | `mvp0/refs/<char_id>.png` — canonical reference **đã chọn tay** (thư mục do người tạo ở [Bước 2](../../docs/060-Manuals/User-Guide/Chay-MVP0.md)) |
| 3 | **Ảnh output** | `panels/panel-NNN/approved.png` — copy từ `run-*/candidates/` **ngay sau khi chấm**, vì thư mục nguồn sẽ mất |
| 4 | ⭐ **Bảng chấm** | [`scoring-sheet.csv`](./scoring-sheet.csv) — file này |

⚠️ **Copy ảnh output là một bước NGƯỜI làm, ⛔ không có script nào tự làm.** Ảnh đã duyệt nằm trong `run-*/` là ảnh đang **chờ bị xoá**.

### Bố cục thư mục

```
mvp0/golden-dataset/
├── README.md              ← file này
├── scoring-sheet.csv      ← bảng chấm, append-only
├── g1-verdict.md          ← verdict 5 tiêu chí, ghi sau khi chấm xong
└── panels/
    └── panel-016/
        └── approved.png   ← ảnh đã duyệt, copy tay từ run-*/candidates/
```

## 3. Schema `scoring-sheet.csv`

**13 cột, cố định.** ⛔ Không thêm/bớt cột — [`scripts/mvp0/regen_ratio.py`](../../scripts/mvp0/regen_ratio.py) đọc file này theo tên cột.

| # | Cột | Giá trị hợp lệ | Ý nghĩa |
|:-:|---|---|---|
| 1 | `scored_at` | ISO 8601, ví dụ `2026-09-02T21:30+07:00` | Thời điểm chấm. ⭐ Cột quyết định **bản ghi nào còn hiệu lực** — xem [mục 4](#4-luật-ghi--append-only-⛔-không-ghi-đè) |
| 2 | `panel_index` | `1`–`42` | Neo tới panel script. ⛔ Không dùng số trang |
| 3 | `run_dir` | ví dụ `run-panels-ch1-20260902-213000` | Thư mục sinh ra ảnh. Giữ lại **dù thư mục đã bị xoá** — đó là dấu vết truy nguyên duy nhất còn lại |
| 4 | `n_used` | số nguyên ≥1 | Số candidate **thực có** ở vòng đó. ⭐ Đây là dữ liệu chấm `G1-b` (so tỉ lệ đạt ở `N=2` với `N=3`) |
| 5 | `approved_candidate_index` | `0`–`n_used-1`, hoặc `none` | Candidate **người** chọn. `none` = ⛔ không candidate nào dùng được ⇒ panel này chưa có ảnh duyệt |
| 6 | `g1a_consistency` | `consistent` · `inconsistent` · `na` | *"Nhận ra cùng một người mà ⛔ không cần được nhắc không?"* · `na` = panel ⛔ không có nhân vật |
| 7 | `g1c_human_verdict` | `pass` · `fail` | Người chấm **SAU KHI** VLM đã xếp hạng. ⚠️ Đây là **phép đo `G1-c`**, ⛔ không phải điểm của VLM |
| 8 | `g1d_identity` | `ok` · `wrong` · `na` | Trục 1 của `G1-d`: **đúng người** |
| 9 | `g1d_attribute_binding` | `ok` · `wrong` · `na` | Trục 2 của `G1-d`: trang phục/vật phẩm gắn **đúng người**. ⚠️ Hai trục chấm **riêng**, ⛔ không gộp thành một điểm |
| 10 | `g1e_text_path` | `overlay` · `model_render` · `na` | Đường đi của chữ. `na` = panel ⛔ không có thoại. ⚠️ **Một** dòng `model_render` là **trượt `G1-e`** |
| 11 | ⭐ `readability_verdict` | `readable` · `not_readable` · `unscored` | *"Trang này đọc có ổn không?"* — xem [mục 5](#5-readability_verdict--cột-tách-biệt-⛔-không-suy-từ-điểm-kỹ-thuật) |
| 12 | `refusal_count` | số nguyên ≥0 | Số candidate bị provider từ chối ở vòng đó, đếm từ `refusals.jsonl`. ⚠️ Ghi **riêng**, ⛔ không trộn vào `g1c_human_verdict` |
| 13 | `note` | text, bọc trong `"` nếu có dấu phẩy | Ghi chú tự do. Chỗ ghi *"vì sao"* |

> [!WARNING]
> ⚠️ **`refusal_count` ⛔ KHÔNG được trộn vào `g1c_human_verdict`.** Provider từ chối và người loại ảnh là **hai nguyên nhân khác loại**. Trộn chúng làm `reject_rate` của `G1-c` **mất nghĩa** — con số ra được ⛔ không trả lời được câu hỏi mà `G1-c` tồn tại để hỏi (*"VLM-select có cắt được công người, hay chỉ thêm chi phí?"*). Từ chối là dữ liệu của **`C-7`** ([Analysis-MVP0-Requirements](../../docs/050-Research/Analysis-MVP0-Requirements.md)), ⛔ không phải của `G1-c`.

## 4. Luật ghi — append-only, ⛔ không ghi đè

⭐ **Chấm lại một panel = THÊM một dòng mới, ⛔ không sửa dòng cũ.**

- **Bản ghi còn hiệu lực** của một panel = dòng có `scored_at` **muộn nhất** cho `panel_index` đó.
- Mọi dòng cũ **giữ nguyên** làm lịch sử.

**Vì sao ⛔ không cho ghi đè** — hai lý do:

1. `Story-Record-Readability-Human-Judgement` (unhappy path): *"với 1 Founder duy nhất chấm (**bus factor = 1**, ⛔ không có second rater), nếu Founder đổi câu trả lời cho cùng một panel ở hai thời điểm khác nhau, bản ghi phải giữ **lịch sử cả hai lần chấm**"*. ⭐ Với một người chấm duy nhất, **lịch sử đổi ý là thứ gần nhất với một second rater** mà MVP0 có được.
2. Cùng nguyên tắc với `usage_event`: *"append-only là **điều kiện** để nó dùng được làm **căn cứ đối soát**"* ([Glossary](../../docs/999-Resources/Glossary.md)). Sửa được thì ⛔ không đối soát được.

## 5. `readability_verdict` — cột tách biệt, ⛔ không suy từ điểm kỹ thuật

Đây là **cột số 11**, nằm **riêng** khỏi `g1a`…`g1e`. Bốn luật, cả bốn đều là AC đã ký của [Story-Record-Readability-Human-Judgement](../../docs/022-User-Stories/Backlog/Story-Record-Readability-Human-Judgement.md):

| # | Luật |
|:-:|---|
| **1** | Enum **cố định**: `readable` (*đọc ổn*) · `not_readable` (*⛔ không ổn*) · `unscored` (*chưa chấm*). ⛔ Không văn bản tự do |
| **2** | ⭐ Mặc định là **`unscored`**, ⛔ **không** phải `readable`. Bỏ qua một panel do chạy dồn dập ⇒ ghi `unscored` **tường minh**, ⛔ không để trống, ⛔ không PASS ngầm định |
| **3** | ⛔ **Không** suy giá trị này từ `g1a`…`g1e`. Panel `pass` kỹ thuật mà `not_readable` là một **trạng thái hợp lệ và phải giữ được** — đó chính là lỗi `CF-10.10` mà cột này tồn tại để bắt: *"pass mọi check mà ⛔ không ai muốn đọc"* |
| **4** | ⛔ **Không** để VLM trả lời thay người. `CF-10.10`: đây là **đúng một câu người trả lời** |

> [!CAUTION]
> ⛔ **Cột này KHÔNG dùng để tự động pass/fail gate `G1`.** Nó là dữ liệu **song song**, ⛔ không thay thế 5 tiêu chí `G1` ([MVP-Scope §7.2](../../docs/010-Planning/MVP-Scope.md)). Nó cũng ⛔ **không dừng lại sau MVP0** — nghĩa vụ ghi là **liên tục** từ MVP0 trở đi.

## 6. Quy trình chấm một panel

1. Mở cả `n_used` candidate của panel trong `run-*/candidates/`. ⛔ **Đừng xoá cái nào** — cả ba là dữ liệu chấm `G1-c`.
2. Xem xếp hạng VLM trong `results.jsonl`. ⚠️ VLM **chỉ xếp hạng**; lựa chọn cuối là của người — và **chính lựa chọn đó là phép đo `G1-c`**.
3. Chọn một candidate (hoặc `none`), copy thành `panels/panel-NNN/approved.png`.
4. **Thêm một dòng** vào [`scoring-sheet.csv`](./scoring-sheet.csv). Đủ 13 cột.
5. Trả lời câu readability **ngay lúc này**, ⛔ không hoãn — xem [mục 1](#1-vì-sao-bảng-chấm-phải-tồn-tại-trước-tấm-ảnh-đầu-tiên) lý do 2.

**Ví dụ một dòng** (panel 16 — 3 nhân vật, ca khó nhất):

```csv
2026-09-02T21:30+07:00,16,run-panels-ch1-20260902-213000,3,1,consistent,pass,ok,wrong,na,readable,0,"Vat pham gan sai nguoi: chuoi hat cua lam_uyen sang nhan vat ben canh"
```

⭐ Đọc dòng trên: panel này `g1c_human_verdict=pass` nhưng `g1d_attribute_binding=wrong` — **hai trục độc lập**, và đó là lý do `G1-d` chấm riêng khỏi `G1-c`.

⚠️ Sau khi chấm xong, tính regen ratio `p50`/`p90` — ⛔ **thiếu nó thì `G2` KHÔNG CHẠY ĐƯỢC**, ⛔ không PASS mặc định:

```bash
python3 scripts/mvp0/regen_ratio.py
```

Rồi ghi verdict 5 tiêu chí vào [`g1-verdict.md`](./g1-verdict.md) — **kèm cỡ mẫu**.

## 7. Tài liệu tham khảo

| Tài liệu | Dùng khi |
|---|---|
| [Chay-MVP0 Bước 4–5](../../docs/060-Manuals/User-Guide/Chay-MVP0.md) | Cách chấm từng tiêu chí `G1` và ngưỡng PASS |
| [MVP-Scope §7.2](../../docs/010-Planning/MVP-Scope.md) | Nguồn gốc 5 tiêu chí `G1` |
| [`threshold-signoff.md`](../threshold-signoff.md) | Phiếu ký ngưỡng — ký **trước** khi chấm |
| [Story-Record-Readability-Human-Judgement](../../docs/022-User-Stories/Backlog/Story-Record-Readability-Human-Judgement.md) | AC của cột `readability_verdict` |
| [Story-Golden-Dataset-For-Regression](../../docs/022-User-Stories/Backlog/Story-Golden-Dataset-For-Regression.md) | AC của golden dataset (`H6`/`P-6`) |
| [ADR-018](../../docs/030-Specs/Architecture/ADR-018-Usage-Event-And-Rollup-Model.md) | Luật *"rollup lỗi phải nói ra là lỗi"* — nền của `regen_ratio.py` |

---

_Created by Comic Studio_
_Author: trisjr_
