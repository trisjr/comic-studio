# Rule Index — rule nào nằm ở đâu

`.claude/rules/` = auto-load vào **mọi** session và **mọi** subagent. Chỉ giữ ở đây các rule luôn đúng, luôn cần.
SSOT của toàn bộ rule là `.agent/rules/` (được git track). Các rule tình huống nằm ở đó và **phải đọc theo yêu cầu**:

| Đọc `.agent/rules/...` | Khi nào bắt buộc đọc |
|------------------------|----------------------|
| `clickup-mcp-formatting.md` | Trước khi tạo/sửa task ClickUp qua MCP (`/create-task`, `/opsx:submit`, `brd-to-clickup`) |
| `scripts-management.md` | Trước khi tạo file script mới (`.js`, `.py`, `.sh`) |
| `learning-loop.md` | Khi kết thúc một task đáng đúc kết (`/memo`) |
| `reasoner-planner.md`, `sequential-thinking.md`, `create-file-markdown.md` | Khi workflow hoặc role định nghĩa yêu cầu rõ |

Không copy nội dung các file trên vào `.claude/rules/` — đó là cố ý bỏ khỏi auto-load để tiết kiệm context mỗi lần spawn subagent.
