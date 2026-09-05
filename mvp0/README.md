# MVP0 — Dữ liệu viết tay & Môi trường thực nghiệm

> Thư mục này chứa **dữ liệu đầu vào viết tay** và **kết quả thực nghiệm** của MVP0, ⛔ không phải tài liệu dự án.
>
> **Hiện trạng**: Đã clear toàn bộ dữ liệu của truyện cũ; sẵn sàng tiếp nhận **chương truyện mới** để khởi động lại vòng thử nghiệm Gate G1.

## Kỷ luật MVP0 — Cái gì vứt, cái gì giữ

> *"Code của MVP0 KHÔNG phải nền của sản phẩm — viết để trả lời câu hỏi rồi **bỏ**; giữ lại **kết luận và dữ liệu**."* — [MVP-Scope §3.1](../docs/010-Planning/MVP-Scope.md) · [Roadmap §3.1](../docs/010-Planning/Roadmap.md)

| Thành phần | Số phận |
|---|---|
| Script sinh ảnh, adapter, compiler (`scripts/mvp0/`) | ⛔ **Vứt** sau khi có số đo và chuyển giao sang MVP1 |
| `story-bible.yaml` · `panel-script-ch1.yaml` | ✅ **Giữ** — là nguyên liệu tái dựng golden dataset |
| Golden dataset (ảnh approved + bảng chấm `scoring-sheet.csv`) | ✅ **Giữ vĩnh viễn** — `H6` là `✅` ở **mọi** mốc MVP0–MVP4, đầu vào của eval kit `M1-6` |

⛔ **Không** tạo database, migration hay ORM trong thư mục này.

---

## Cấu trúc thư mục hiện tại

```
mvp0/
├── README.md                  ← Hướng dẫn và trạng thái này
├── story-bible.yaml           ← [Template] Đặc tả nhân vật của chương mới
├── panel-script-ch1.yaml      ← [Template] Kịch bản phân cảnh của chương mới
├── threshold-signoff.md       ← Phiếu ký nhận ngưỡng Gate G1 (ký TRƯỚC khi sinh ảnh)
├── typeset-corpus.json        ← Corpus text tiếng Việt để kiểm tra typeset
├── refs/                      ← Nơi lưu canonical reference images đã duyệt (1 file/nhân vật)
│   └── selection-log.md       ← Bảng ghi nhận provenance khi chọn ảnh ref
└── golden-dataset/            ← Dữ liệu chấm điểm Gate G1 (giữ vĩnh viễn)
    ├── README.md
    ├── scoring-sheet.csv      ← Bảng chấm 13 cột (append-only)
    ├── g1-verdict.md          ← Phiếu kết luận 5 tiêu chí Gate G1
    └── panels/                ← Thư mục chứa các ảnh panel đã được duyệt
```

---

## Quy trình vận hành khi có chương truyện mới

### 1. Soạn thảo nguyên liệu đầu vào
1. **Story Bible** (`mvp0/story-bible.yaml`): Định nghĩa 2–3 nhân vật chính của chương (gồm `id`, `ten`, `ten_en`, `dien_mao`, `trang_phuc`, `canonical_reference_en`).
2. **Panel Script** (`mvp0/panel-script-ch1.yaml`): Viết kịch bản phân cảnh cho chương mới (khuyến nghị 15–25 panel, tối đa 3 nhân vật/panel, có `text_safe_zone` và phân bổ loại cảnh/beat).

### 2. Chuẩn hóa & nâng cao prompt (Tùy chọn nhưng khuyến nghị)
Chạy script tự động tối ưu tính liền mạch thị giác (continuity, cinematic lighting, 2D manhwa lineart) qua Qwen3.7-Plus:
```bash
python3 scripts/mvp0/enhance_prompts.py --chapter ch1
```

### 3. Ký nhận ngưỡng kỹ thuật
Kiểm tra và ký nhận các ngưỡng trong `mvp0/threshold-signoff.md` **TRƯỚC** khi gọi API sinh ảnh.

### 4. Sinh và chọn Canonical References (Stage `refs`)
```bash
python3 scripts/mvp0/run_mvp0.py refs --dry-run
python3 scripts/mvp0/run_mvp0.py refs
```
* Duyệt ảnh candidate trong `mvp0/run-refs-<timestamp>/candidates/`.
* Chọn 1 ảnh tốt nhất cho mỗi nhân vật, lưu vào `mvp0/refs/<char_id>.png`.
* Ghi nhận quyết định vào `mvp0/refs/selection-log.md`.

### 5. Sinh Panel và VLM Ranking (Stage `panels`)
Chạy thăm dò trước một vài panel rủi ro:
```bash
python3 scripts/mvp0/run_mvp0.py panels --chapter ch1 --dry-run
python3 scripts/mvp0/run_mvp0.py panels --chapter ch1 --panels 1 2 3 -n 3
```
Sau đó chạy toàn bộ chapter:
```bash
python3 scripts/mvp0/run_mvp0.py panels --chapter ch1 -n 3
```

### 6. Chấm điểm Golden Dataset & Đóng Gate G1
1. Chọn candidate ưng ý cho từng panel, copy vào `mvp0/golden-dataset/panels/panel-NNN/approved.png`.
2. Ghi điểm vào `mvp0/golden-dataset/scoring-sheet.csv` (13 cột, điền nhận định `readability_verdict`).
3. Chạy tính `regen_ratio` ($p_{50}/p_{90}$):
   ```bash
   python3 scripts/mvp0/regen_ratio.py
   ```
4. Điền số đo và chốt verdict tại `mvp0/golden-dataset/g1-verdict.md`.
