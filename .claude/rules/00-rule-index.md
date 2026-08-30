# Rule Index — rule nào nằm ở đâu

`.claude/rules/` = **SSOT của toàn bộ rule**, được git track, auto-load vào **mọi** session và **mọi** subagent.

> [!WARNING]
> ⚠️ **Đính chính `2026-08-30`**: bản trước của file này khai *"SSOT của toàn bộ rule là `.agent/rules/`"* và liệt kê 5 rule tình huống nằm ở đó.
> ⛔ **Thư mục `.agent/` KHÔNG TỒN TẠI** trong repo *(kiểm cơ học `ls -la .agent` → `No such file or directory`; `git ls-files .agent/` → 0 hit)*. Cả 5 file được nhắc đều đang nằm trong chính `.claude/rules/`.
> ⇒ Index cũ trỏ vào hư không: một agent làm theo nó sẽ đi tìm file ⛔ không có, rồi **bỏ qua rule** thay vì đọc nó.
> Dấu vết còn lại của thư mục cũ: `.gitignore` có dòng `.agent/.DS_Store`.

## Toàn bộ rule hiện có

### Luôn đúng, luôn cần — đọc mặc định

| File | Nội dung |
|---|---|
| [`communication.md`](./communication.md) | Định danh Comic Studio, ngôn ngữ hội thoại, gate phê duyệt, chống ảo giác |
| [`mindset.md`](./mindset.md) | Dual-System Thinking, Systems Thinking, Role Guidance Protocol |
| [`clean-code.md`](./clean-code.md) | SOLID/DRY/KISS/YAGNI, header `AI Coding`, naming, giới hạn độ dài file |
| [`security.md`](./security.md) | Phạm vi hoạt động, quản lý secret, thao tác nhạy cảm |
| ⭐ [`git-commit-format.md`](./git-commit-format.md) | Commit message · branch · PR title — **100% tiếng Anh**, ⛔ cấm tiếng Việt không dấu |

### Đọc theo yêu cầu — chỉ nạp khi tình huống chạm tới

| File | Khi nào bắt buộc đọc |
|---|---|
| [`clickup-mcp-formatting.md`](./clickup-mcp-formatting.md) | Trước khi tạo/sửa task ClickUp qua MCP (`/create-task`, `/opsx-submit`, `brd-to-clickup`) |
| [`scripts-management.md`](./scripts-management.md) | Trước khi tạo file script mới (`.js`, `.py`, `.sh`) |
| [`learning-loop.md`](./learning-loop.md) | Khi kết thúc một task đáng đúc kết (`/memo`) |
| [`create-file-markdown.md`](./create-file-markdown.md) | Khi tạo file markdown mới |
| [`reasoner-planner.md`](./reasoner-planner.md) · [`sequential-thinking.md`](./sequential-thinking.md) | Khi workflow hoặc role định nghĩa yêu cầu rõ |

## ⚠️ Đánh đổi đang chấp nhận — token cost

Mọi file trong `.claude/rules/` được **auto-load vào từng subagent spawn**. Nhóm *"đọc theo yêu cầu"* ở trên hiện **vẫn bị auto-load** vì cùng nằm trong thư mục này — đó là **cái giá của việc gộp SSOT về một chỗ** sau khi `.agent/` biến mất.

⇒ Nếu chi phí này trở nên đáng kể, hướng xử lý đúng là **tái lập `.agent/rules/` làm nơi chứa rule tình huống** và cập nhật lại index — ⛔ **không phải** xoá rule khỏi git để tiết kiệm context.
