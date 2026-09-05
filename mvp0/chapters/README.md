<!-- AI Coding -->

# mvp0/chapters/

Thư mục chứa văn bản gốc của từng chương truyện, dùng làm input để soạn page
YAML (`mvp0/pages/`).

## Quy ước đặt tên

- `chNN.md` với `NN` là số chương viết 2 chữ số, ví dụ `ch01.md`, `ch02.md`.

## Ai đọc thư mục này

- Slash command **`/mvp0-page-prompt mvp0/chapters/chNN.md`** đọc file chương
  tại đây, kết hợp với `mvp0/story-bible.yaml`, để soạn ra các file
  `mvp0/pages/chNN_pageNNN.yaml` theo cấu trúc `mvp0/prompt-template.txt`.

## Trạng thái artifact

- `mvp0/chapters/` là artifact **Giữ** (kept) — nội dung gốc của chương, không
  bị xoá hay coi là tạm thời, khác với các thư mục `mvp0/run-pages-*/` (disposable).
