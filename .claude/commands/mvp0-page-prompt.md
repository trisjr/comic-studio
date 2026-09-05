---
description: Chuyển một chương truyện (chapter text) thành các page prompt YAML theo prompt-template.txt, có human gate ở bước lập page-plan
---

# Workflow: /mvp0-page-prompt — Chapter → Page Prompt YAML

Skill này biên soạn prompt sinh ảnh **cấp trang (page-level)** cho MVP0: đọc một chương truyện thô, lập page-plan, rồi viết YAML từng trang vào `mvp0/pages/<page_id>.yaml` theo đúng `mvp0/prompt-template.txt`. Scoring G1 vẫn ở cấp panel (không đổi) — panel được crop ra từ page image sau khi generate.

**Input**: đối số sau `/mvp0-page-prompt` là đường dẫn tới `mvp0/chapters/chNN.md`. Trống → **AskUserQuestion**: *"Anh cho em đường dẫn file chương truyện (mvp0/chapters/chNN.md)?"*. Không đoán đường dẫn.

---

## Bước 0 — Load context (chỉ đọc, không ghi)

Đọc tuần tự:
1. File chương truyện (`chNN.md`) — nội dung văn xuôi.
2. `mvp0/story-bible.yaml` — hai top-level key `nhan_vat` (list nhân vật) và `boi_canh` (list bối cảnh).
3. `mvp0/prompt-template.txt` — cấu trúc bắt buộc của page YAML.
4. `mvp0/prompt-example.yaml` — ví dụ tham chiếu cách điền template.

**Kiểm tra bible coverage**: liệt kê mọi nhân vật và bối cảnh xuất hiện trong chương. Nếu có nhân vật/bối cảnh nào **không tồn tại** trong `nhan_vat` hoặc `boi_canh` của bible → **DỪNG LẠI**, báo cho anh danh sách còn thiếu, và đề nghị anh bổ sung vào `mvp0/story-bible.yaml` trước. Bible là **nguồn sự thật duy nhất** — skill **không được tự bịa** entry mới cho bible, kể cả tạm thời.

Nếu bible thiếu các field tiếng Anh mới (`silhouette_cue_en`, `body_type_relative_en`, `color_language_en`, `personality_en` cho nhân vật; `setting_en`, `environment_en`, `lighting_default_en`, `props_en` cho bối cảnh) cần cho template → cũng dừng và báo anh bổ sung, không tự suy diễn nội dung.

---

## Bước 1 — Page plan (HUMAN GATE — bắt buộc chờ phê duyệt)

Chia chương thành các trang theo nguyên tắc:
- Mỗi trang **4–6 panel**.
- Mỗi panel **tối đa 3 nhân vật**.
- Cả chương chỉ nên có **2–3 nhân vật lặp lại** làm nhân vật chính (đúng ràng buộc G1-d về sample size).
- `panel_index` là số nguyên **tuần tự toàn chương**, đánh liên tục qua các trang (không reset về 1 ở trang mới) — để khớp naming `golden-dataset/panels/panel-NNN/` và `regen_ratio.py`.

Trình bày kế hoạch dưới dạng **bảng gọn**, mỗi dòng một panel:

| page_id | panel_index | beat_type | characters (id) | setting (id) | dominant_panel |
|---|---|---|---|---|---|

Kèm theo mỗi page một dòng `purpose` ngắn. Sau bảng, nêu rõ: *"Đây là page-plan, chưa phải YAML. Anh duyệt để em viết YAML từng trang không?"* và **dừng lại chờ anh xác nhận** (đúng `communication.md` §3 — Plan & Approve). **Tuyệt đối không viết file YAML nào ở bước này.**

---

## Bước 2 — Viết page YAML (sau khi được duyệt)

Với mỗi page đã duyệt, tạo `mvp0/pages/<page_id>.yaml` (`page_id = "chNN_pageNNN"`) đúng cấu trúc `prompt-template.txt`:

- **PAGE / LAYOUT / CONTINUITY / TEXT_POLICY**: `render_text_in_image: false` luôn luôn. `continuity.setting` chép từ `boi_canh.setting_en`; `continuity.environment` dựa trên `boi_canh.environment_en` (có thể lồng thêm `props_en`); `boi_canh.lighting_default_en` là **default** cho `environment` prose và cho `lighting.source` của từng panel (đúng cách `prompt-example.yaml` làm với "Cold moonlight is the only light source"). Template CONTINUITY **không có key `lighting`** riêng — không tự thêm key lạ, tránh lint fail vì unknown key.
  `continuity.progression`, `spatial`, `time_span`, `wardrobe` — viết mới từ nội dung chương (không có sẵn trong bible); `spatial` mô tả ai trái/ai phải bằng **tên nhân vật** (prose, được phép dùng tên).
- **CHARACTERS block**: chiếu **mechanically** (không tự sáng tác) từ `nhan_vat` trong bible:
  - `name` ← `ten_en`
  - `canonical_reference` = `mvp0/refs/<id>.png`
  - `reference_instruction` = chuỗi cố định "Match the face, hairstyle, and outfit of the attached reference image exactly." (theo `prompt-example.yaml`)
  - `silhouette_cue` ← `silhouette_cue_en`
  - `identity.gender/age` ← `gioi_tinh`/`tuoi` (dịch sang tiếng Anh)
  - `identity.body_type` ← `body_type_relative_en`
  - `style.color_language` (theo nhân vật) ← `color_language_en`
  - `personality` ← `personality_en`
  - `appearance` / `outfit` ← các field trong `canonical_reference_en`
- **PANELS**: cùng với `progression/spatial/time_span/wardrobe` ở CONTINUITY, đây là phần **được tác giả hóa (authored) fresh** từ nội dung chương — action, pose, camera, lighting, text_safe_zone, typeset. Mọi field khác của page YAML là chiếu mechanically từ bible. Mỗi panel giữ `panel_index` đã chốt ở Bước 1.
  - `text_safe_zone` không đặt mặt/focal detail.
  - `typeset.dialogue[].speaker` dùng `character_id`, không dùng tên (D4).
- **NEGATIVE_CONSTRAINTS**: không lặp lại nội dung đã khai ở CONTINUITY; chỉ thêm các cấm riêng (đổi silhouette cue, thêm nhân vật lạ, đảo trái/phải...).
- Toàn bộ nội dung viết bằng **tiếng Anh** (đây là prompt gửi cho image model).

> [!IMPORTANT]
> Field cấu trúc (`characters[].id`, `panels[].characters[].character_id`, `typeset.dialogue[].speaker`) **BẮT BUỘC dùng `character_id`**. Field văn xuôi (`continuity.spatial`, `composition`, `panel_purpose`...) **được phép dùng tên nhân vật** để dễ đọc (D4).

---

## Bước 3 — Lint

Chạy:

```
python3 scripts/mvp0/lint_page_prompt.py mvp0/pages/
```

Sửa từng lỗi lint cho tới khi pass sạch. Không báo cáo Bước 4 khi lint còn lỗi.

---

## Bước 4 — Report

Báo cáo cho anh:
1. Danh sách file page YAML đã tạo (`mvp0/pages/<page_id>.yaml`).
2. Khoảng `panel_index` (min–max) của cả chương.
3. Số lượng panel theo `character_count` (1 / 2 / 3) — để anh soi cảnh báo sample-size của G1-d.
4. Nhắc: `mvp0/threshold-signoff.md` phải được ký trước khi generate ảnh thật.
5. Lệnh tiếp theo: `python3 scripts/mvp0/run_mvp0.py pages --dry-run`.

---

## Guardrails

- **LLM chỉ viết YAML, không bao giờ gọi image API** trực tiếp trong skill này — sinh ảnh là việc của `run_mvp0.py` + `providers.py` (D-34 / SRS-FR-17: không LLM call trong scripts).
- **character_id vs tên (D4)**: field cấu trúc dùng `character_id`; field prose được dùng tên. Không lẫn lộn hai loại.
- **Không sửa `mvp0/story-bible.yaml` từ trong skill này.** Bible thiếu gì thì dừng lại và nhờ anh bổ sung ở Bước 0 — skill không tự thêm/sửa entry.
- Không viết YAML trước khi page-plan ở Bước 1 được anh duyệt.
- Panel trong một trang: tối đa 3 nhân vật/panel; cả chương tối đa 2–3 nhân vật lặp lại.
