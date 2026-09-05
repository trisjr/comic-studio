# MVP0 — Dữ liệu viết tay & Môi trường thực nghiệm

> Thư mục này chứa **dữ liệu đầu vào viết tay** và **kết quả thực nghiệm** của MVP0, ⛔ không phải tài liệu dự án.
>
> **Hiện trạng**: Đã chuyển sang đơn vị sinh ảnh **cấp trang (page-level)**; sẵn sàng tiếp nhận **chương truyện mới** để khởi động lại vòng thử nghiệm Gate G1.

## Kỷ luật MVP0 — Cái gì vứt, cái gì giữ

> *"Code của MVP0 KHÔNG phải nền của sản phẩm — viết để trả lời câu hỏi rồi **bỏ**; giữ lại **kết luận và dữ liệu**."* — [MVP-Scope §3.1](../docs/010-Planning/MVP-Scope.md) · [Roadmap §3.1](../docs/010-Planning/Roadmap.md)

| Thành phần | Số phận |
|---|---|
| Script sinh ảnh, adapter, compiler (`scripts/mvp0/`) | ⛔ **Vứt** sau khi có số đo và chuyển giao sang MVP1 |
| `story-bible.yaml` · `mvp0/pages/*.yaml` | ✅ **Giữ** — là nguyên liệu tái dựng golden dataset |
| `panel-script-ch1.yaml` | ⛔ **Đã retired** — thay bằng `mvp0/pages/<page_id>.yaml` (một file/trang) |
| `scripts/mvp0/enhance_prompts.py` | ⛔ **Đã retired** — authoring bằng LLM chuyển hẳn sang skill `/mvp0-page-prompt`, ⛔ không còn ở trong script |
| Golden dataset (ảnh approved + bảng chấm `scoring-sheet.csv`) | ✅ **Giữ vĩnh viễn** — `H6` là `✅` ở **mọi** mốc MVP0–MVP4, đầu vào của eval kit `M1-6` |

⛔ **Không** tạo database, migration hay ORM trong thư mục này.

## Ranh giới LLM

⭐ **LLM chỉ được gọi ở bước authoring (skill `/mvp0-page-prompt`)** — nơi lập page plan và soạn nội dung page YAML từ chương truyện. **Toàn bộ script trong `scripts/mvp0/` PHẢI deterministic, ⛔ TUYỆT ĐỐI không gọi LLM/VLM tại runtime** (`D-34` / `SRS-FR-17`). `compile_prompt.py` chỉ làm việc serializer: đọc page YAML đã được người duyệt, trả về `text_prompt` + `conditioning_set` bằng bảng tra cố định.

---

## Cấu trúc thư mục hiện tại

```
mvp0/
├── README.md                  ← Hướng dẫn và trạng thái này
├── story-bible.yaml           ← [Template] Đặc tả nhân vật + bối cảnh của chương mới (nhan_vat + boi_canh)
├── chapters/                  ← Văn bản chương truyện thô, đầu vào của page plan
│   └── chNN.md                ← Chương NN (2 chữ số)
├── pages/                     ← Page YAML đã lint — đơn vị gửi đi sinh ảnh (✅ Giữ)
│   └── chNN_pageNNN.yaml       ← 1 file/trang, page_id = "chNN_pageNNN"
├── prompt-template.txt        ← Sơ đồ trường bắt buộc của page YAML (tham khảo khi soạn)
├── prompt-example.yaml        ← Ví dụ page YAML đầy đủ, đúng schema
├── threshold-signoff.md       ← Phiếu ký nhận ngưỡng Gate G1 (ký TRƯỚC khi sinh ảnh)
├── typeset-corpus.json        ← Corpus text tiếng Việt để kiểm tra typeset
├── refs/                      ← Nơi lưu canonical reference images đã duyệt (1 file/entry `nhan_vat`, mỗi biến thể một file)
│   └── selection-log.md       ← Bảng ghi nhận provenance khi chọn ảnh ref
└── golden-dataset/            ← Dữ liệu chấm điểm Gate G1 (giữ vĩnh viễn)
    ├── README.md
    ├── scoring-sheet.csv      ← Bảng chấm 13 cột (append-only)
    ├── g1-verdict.md          ← Phiếu kết luận 5 tiêu chí Gate G1
    └── panels/                ← Thư mục chứa các ảnh panel đã được duyệt (crop từ page candidate)
```

---

## Quy trình vận hành khi có chương truyện mới

### 1. Đặt văn bản chương
Lưu nguyên văn chương mới tại `mvp0/chapters/chNN.md` (`NN` là số thứ tự 2 chữ số, ví dụ `ch01.md`).

### 2. Soạn Story Bible
Điền `mvp0/story-bible.yaml` với hai nhóm khóa cấp cao nhất:
- `nhan_vat` (list): mỗi nhân vật gồm `id`, `ten`, `ten_en`, `vai_tro`, `tuoi`, `gioi_tinh`, `dien_mao{...}`, `trang_phuc{...}`, `dau_an{...}`, `canonical_reference` (đường dẫn `mvp0/refs/<id>.png`), `canonical_reference_en{khuon_mat, toc, trang_phuc,...}`, và năm trường tiếng Anh **mới** dùng 1:1 bởi `prompt-template.txt`: `vai_tro_en`, `silhouette_cue_en`, `body_type_relative_en`, `color_language_en`, `personality_en`.
- `boi_canh` (list bối cảnh): mỗi bối cảnh gồm `id`, `ten`, `ten_en`, `setting_en`, `environment_en`, `lighting_default_en`, `props_en` (list).

⭐ **Biến thể nhân vật (variant)** — khi một nhân vật có nhiều hình dạng theo **thời gian** (độ tuổi, timeline) hoặc theo **biến thân**, mỗi hình dạng là **MỘT entry riêng ở cấp `nhan_vat`**, ⛔ không lồng vào nhau. Lý do: `run_mvp0.py` stage `refs` duyệt phẳng `nhan_vat` và sinh đúng một character sheet cho mỗi entry — đơn vị mà pipeline tiêu thụ là *"thứ có reference image riêng"*, tức chính là variant. Dùng hai trường metadata `nhan_vat_goc` (id nhân vật gốc, để nhóm) và `bien_the` (mô tả hình dạng); script bỏ qua cả hai.

| Ràng buộc kéo theo | Chi tiết |
|---|---|
| Ngân sách `characters` | Variant tính riêng như một nhân vật độc lập: giới hạn **≤ 3 `characters`/page** (lint `L08` báo ERROR nếu vượt) và ngân sách **2–3 nhân vật lặp lại** của `G1-d` |
| `silhouette_cue_en` | Các variant có thể cùng xuất hiện một trang **BẮT BUỘC** khác cue — `L08` bắt trùng |
| `canonical_reference_en` | Phải đủ bốn khóa `khuon_mat`, `mat`, `toc`, `trang_phuc` cho **mọi** entry, kể cả biến thân phi nhân — `run_mvp0.py::character_sheet_prompt` truy cập trực tiếp, thiếu khóa là `KeyError` |

### 3. Lập page plan & soạn page YAML — Skill `/mvp0-page-prompt`
```bash
/mvp0-page-prompt mvp0/chapters/ch01.md
```
Skill đọc chương, đề xuất page plan (số trang, số panel/trang, `panel_index` toàn cục xuyên suốt chương), chờ người duyệt, rồi sinh từng `mvp0/pages/chNN_pageNNN.yaml` theo `prompt-template.txt`. Trong page YAML: các trường văn xuôi (`continuity.spatial`, `composition`, `panel_purpose`...) được phép dùng tên nhân vật; các trường **cấu trúc** (`characters[].id`, `panels[].characters[].character_id`, `typeset.dialogue[].speaker`) **BẮT BUỘC** dùng `character_id`. Lint ngay sau khi sinh:
```bash
python3 scripts/mvp0/lint_page_prompt.py mvp0/pages/
```

### 4. Ký nhận ngưỡng kỹ thuật
Kiểm tra và ký nhận các ngưỡng trong `mvp0/threshold-signoff.md` **TRƯỚC** khi gọi API sinh ảnh.

### 5. Sinh và chọn Canonical References (Stage `refs`)
```bash
python3 scripts/mvp0/run_mvp0.py refs --dry-run
python3 scripts/mvp0/run_mvp0.py refs
```
* Duyệt ảnh candidate trong `mvp0/run-refs-<timestamp>/candidates/`.
* Chọn 1 ảnh tốt nhất cho **mỗi entry `nhan_vat`** (mỗi biến thể một ảnh), lưu vào `mvp0/refs/<char_id>.png`.
* Ghi nhận quyết định vào `mvp0/refs/selection-log.md`.

### 6. Sinh Trang (Stage `pages`)

> [!CAUTION]
> ⛔ **CHẶN — ⛔ không chạy bước này cho cả chương.** Probe `ch01_page001` ngày `2026-09-05` cho thấy `qwen-image-edit` đang coi ảnh ref là **ảnh gốc cần edit**, nên trả về **một tấm minh họa cảnh đơn** theo đúng tỉ lệ ảnh ref (`1.79`), ⛔ **không phải** trang nhiều panel dọc `2:3`.
>
> ⇒ Đọc [`pages-stage-probe.md`](./pages-stage-probe.md) trước. Bước này chỉ mở lại sau khi mục 1 ở §6 của báo cáo đó được Founder chốt.

Thăm dò trước một vài trang rủi ro:
```bash
python3 scripts/mvp0/run_mvp0.py pages --dry-run
python3 scripts/mvp0/run_mvp0.py pages --page ch01_page001 -n 3
```
Sau đó chạy toàn bộ chương:
```bash
python3 scripts/mvp0/run_mvp0.py pages -n 3
```
Output nằm ở `mvp0/run-pages-<timestamp>/`: `prompts/<page_id>.txt` (prompt tiếng Anh **paste-ready**, cũng dùng tay được để thử trong Gemini), `candidates/<page_id>-c<k>.png`, `usage.jsonl` (mỗi dòng là 1 candidate trang, có `page_id` + `panel_indices`), `results.jsonl`, `refusals.jsonl`, `dropped_constraints.jsonl`.

### 7. Crop trang thành panel & Chấm điểm Golden Dataset
1. Chọn candidate trang ưng ý, crop theo `layout.rows` của page YAML:
   ```bash
   python3 scripts/mvp0/crop_page.py mvp0/pages/ch01_page001.yaml mvp0/run-pages-<timestamp>/candidates/ch01_page001-c1.png --out mvp0/golden-dataset/panels/
   ```
2. Ghi điểm **từng panel** vào `mvp0/golden-dataset/scoring-sheet.csv` (13 cột, schema không đổi; `panel_index` lấy từ page YAML, là chỉ số toàn cục xuyên suốt chương).
3. Chạy tính `regen_ratio` ($p_{50}/p_{90}$) — đếm theo `run-pages-*/usage.jsonl`, mỗi candidate trang cộng +1 cho **mọi** `panel_index` trong `panel_indices` của nó:
   ```bash
   python3 scripts/mvp0/regen_ratio.py
   ```
4. Điền số đo và chốt verdict tại `mvp0/golden-dataset/g1-verdict.md`.
