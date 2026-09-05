# Git Commit & Branch Format

Quy tắc bắt buộc cho mọi commit message, branch name, PR title và PR body của dự án.

## 1. Ngôn ngữ — 100% TIẾNG ANH

> [!IMPORTANT]
> **Commit message, branch name, PR title, PR body và task comment BẮT BUỘC dùng 100% tiếng Anh.**
> Nguồn: `.claude/commands/opsx/submit.md` §*Inline Git Rules & Language* — dòng `MANDATORY LANGUAGE`.

### Ranh giới với `communication.md` — ⛔ KHÔNG mâu thuẫn

| Bề mặt | Ngôn ngữ | Căn cứ |
|---|---|---|
| Hội thoại với User, tài liệu trong `docs/`, `knowledge-base/` | **Tiếng Việt** | `communication.md` #1 · `create-file-markdown.md` |
| ⭐ **Git artifact** (commit, branch, PR, task comment) | **Tiếng Anh** | `communication.md` #2 (*dịch sang Tiếng Anh trước khi thực thi*) · `opsx/submit.md` |

Git artifact là **đầu ra kỹ thuật đi ra ngoài phạm vi hội thoại** — nó sống trên GitHub, được đọc bởi công cụ CI, reviewer và người ngoài dự án. Đó là lý do nó thuộc nhóm "thực thi", ⛔ không thuộc nhóm "hội thoại".

### ⛔ CẤM tuyệt đối: tiếng Việt không dấu

⛔ **Không được viết tiếng Việt bỏ dấu** (`va`, `dong`, `sua`, `chot`, `thu tu`) trong bất kỳ git artifact nào.

⭐ **Lý do — mất thông tin, ⛔ không phải vấn đề thẩm mỹ**: tiếng Việt bỏ dấu là phép biến đổi **mất mát và không đảo ngược được**. Một chuỗi `va` có thể là `và` / `vá` / `vã` / `vạ`; `dong` có thể là `đóng` / `dòng` / `đồng` / `động`. Người đọc `git log` sáu tháng sau **⛔ không khôi phục được nghĩa gốc**, và ⛔ không có cách nào kiểm chứng mình đoán đúng.

⇒ Nếu đang định viết tiếng Việt không dấu, hãy **viết tiếng Anh**. ⛔ Không có phương án thứ ba.

## 2. Commit message

### Cấu trúc

```
<type>(<scope>): <description>

<body — tuỳ chọn, giải thích TẠI SAO>
```

- `<type>` — một trong: `feat` · `fix` · `refactor` · `chore` · `docs` · `ci`
- `<scope>` — module nghiệp vụ hoặc tầng bị đụng, viết thường
- `<description>` — viết thường, ⛔ **không dấu chấm cuối câu**
- Dòng subject nên giữ **dưới 72 ký tự**; body xuống dòng ở khoảng 72 ký tự

### Chất lượng description — nêu KẾT QUẢ, ⛔ không nêu thao tác

Người đọc ⛔ chưa mở diff phải hiểu được **điều gì bây giờ đúng mà trước đó chưa đúng**. Gọi tên năng lực nghiệp vụ, rủi ro đã đóng, hoặc bảo đảm đã thêm — ⛔ không liệt kê file đã sửa.

| | Ví dụ |
|---|---|
| ✅ | `docs(specs): close font constraint gap between adr-013 and design system` |
| ✅ | `fix(auth): reject expired refresh tokens on the admin plane` |
| ⛔ | `docs(specs): update files` |
| ⛔ | `fix(auth): fix bug` |

### Body — giải thích "tại sao", ⛔ không giải thích "cái gì"

Diff đã nói *cái gì*. Body dùng để ghi lại **lý do quyết định**, phương án đã loại, và ràng buộc đã phát hiện — thứ ⛔ không đọc ra được từ code.

## 3. Branch name

```
<type>/<GITHUB_USERNAME>/<short-description>
```

- **Toàn bộ viết thường**, dùng gạch nối thay khoảng trắng
- Ví dụ: `docs/trisjr/phase-3-brand-design-system`

## 4. PR title

```
<Scope> — Capitalized description
```

- `<Scope>` là **module nghiệp vụ** viết Title Case (`Design System`, `Comic Director`), hoặc **acronym trần** nếu nó vốn là acronym (`API`, `CLI`, `UI`)
- ⛔ **Không** dùng tên thư mục thô làm scope
- Áp đúng chuẩn chất lượng ở mục 2: nêu kết quả, ⛔ không nêu thao tác

## 5. ⛔ Điều CẤM

| ⛔ Cấm | Vì sao |
|---|---|
| `git add .` | Kéo vào file ⛔ ngoài phạm vi task. Luôn liệt kê file tường minh |
| Commit tại Hub Root | Trừ khi `ALLOW_COMMIT_HUB_ROOT=true` trong `.env` |
| Commit `package.json` / `package-lock.json` khi task ⛔ không đụng tới thư viện | Làm nhiễu lịch sử dependency |
| Bỏ dấu tiếng Việt | Xem mục 1 — mất thông tin ⛔ không khôi phục được |
| Secret trong commit message | `security.md` §2 |

## 6. Push code từ worktree — đi qua `/opsx:submit`

> [!IMPORTANT]
> Khi đang làm việc trong một git worktree (`.claude/worktrees/...`) và cần đưa code lên remote, ⛔ **không `git push` trực tiếp**. Thay vào đó chạy **`/opsx:submit`** để branch, commit, push và PR đi cùng một chuẩn.

Tham số cố định khi gọi từ worktree:

| Tham số `/opsx:submit` | Giá trị | Hệ quả |
|---|---|---|
| Task/Ticket Link | `[N/A]` | ⛔ Không pause hỏi link · Bỏ qua **Step 5** (comment ClickUp/GitHub Issue) |
| Logwork | **Không** | Bỏ qua **Step 6** (`tnm task log`) |

Các bước còn lại (Step 1–4) giữ nguyên: branch đúng mục 3, commit đúng mục 2, PR title đúng mục 4, `--base` là branch gốc của worktree, `--assignee @me`.

⭐ **Lý do**: worktree được tạo cho job nền hoặc phiên song song, thường ⛔ không gắn ticket và ⛔ không cần logwork. Nhưng branch name, commit và PR body vẫn phải chuẩn, và `/opsx:submit` là nơi duy nhất bảo đảm điều đó. Push tay bỏ qua toàn bộ kiểm tra này.

Nếu branch của worktree **đã được push** trước khi rule này có hiệu lực, vẫn chạy `/opsx:submit` cho phần PR (Step 4), ⛔ không tạo PR bằng `gh pr create` tay ngoài workflow.

## 7. Nợ đã biết

⚠️ **Lịch sử commit trước ngày `2026-08-30` ⛔ KHÔNG tuân thủ rule này** — phần lớn là tiếng Việt không dấu, một số ít tiếng Anh. ⛔ **Không rewrite lịch sử để sửa**: các commit đó đã nằm trong PR đã merge, viết lại sẽ phá checkout của mọi bản sao. Rule này áp cho **commit từ nay về sau**.
