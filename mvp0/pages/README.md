<!-- AI Coding -->

# mvp0/pages/

Thư mục chứa page YAML — đơn vị sinh ảnh (unit of generation) ở mức TRANG,
được soạn theo cấu trúc `mvp0/prompt-template.txt` (xem ví dụ đầy đủ tại
`mvp0/prompt-example.yaml`).

## Quy ước đặt tên

- `<page_id>.yaml` với `page_id = "chNN_pageNNN"` (`NN` = số chương 2 chữ số,
  `NNN` = số trang 3 chữ số), ví dụ `ch01_page001.yaml`.

## Ai đọc/ghi thư mục này

- Skill **`/mvp0-page-prompt`** ghi các file page YAML vào đây sau khi soạn
  từ `mvp0/chapters/chNN.md` + `mvp0/story-bible.yaml`.
- `python3 scripts/mvp0/lint_page_prompt.py mvp0/pages/` lint toàn bộ (hoặc
  một file cụ thể) trước khi dùng để sinh ảnh.
- `python3 scripts/mvp0/run_mvp0.py pages` đọc các file tại đây để sinh
  prompt + ảnh trang, ghi kết quả vào `mvp0/run-pages-<timestamp>/`.
- `python3 scripts/mvp0/crop_page.py mvp0/pages/<page_id>.yaml <page_image.png>`
  dùng `layout.rows` trong file page YAML để crop ảnh trang thành từng panel.

## Trạng thái artifact

- `mvp0/pages/` là artifact **Giữ** (kept) — thay thế cho
  `mvp0/panel-script-ch1.yaml` (đã retire), trong khi `mvp0/run-pages-*/`
  (prompt/ảnh/log của từng lần chạy) là **disposable**, có thể xoá an toàn.
