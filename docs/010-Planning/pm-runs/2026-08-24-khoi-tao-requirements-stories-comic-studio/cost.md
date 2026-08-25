# Cost: 2026-08-24-khoi-tao-requirements-stories-comic-studio

> **Trạng thái file**: bảng số thô của wave 3 được ghi **ngay khi các lô báo về**, trước khi phần bài học được viết. Lý do: số liệu per-batch chỉ tồn tại trong text của notification; một lần compaction context là mất vĩnh viễn, và `cost.md` là close-step **bắt buộc** của lane doc. Ghi số trước, đúc kết sau.

## 1. Số đo per-batch — wave 3 (41 Story + 2 hạng mục cuối)

| Lô | Vai | Deliverable | Output token | Tool call | Thời gian (s) | Token / file |
|----|-----|-------------|-------------:|----------:|--------------:|-------------:|
| L11 | `product-owner` | 5 Story (Epic-A) | 200.186 | 30 | 852 | 40.037 |
| L12 | `product-owner` | 4 Story (Epic-B) | 177.647 | 30 | 603 | 44.412 |
| L13 | `product-owner` | 7 Story (Epic-C) | 169.400 | 31 | 702 | **24.200** |
| L14 | `product-owner` | 5 Story (Epic-D) | 164.449 | 25 | 624 | 32.890 |
| L15 | `architect` | 5 Story (Epic-E) | 207.063 | 38 | 632 | 41.413 |
| L16 | `product-owner` | 3 Story (Epic-F) | 185.117 | 35 | 500 | **61.706** |
| L17 | `security-auditor` | 6 Story (Epic-G) | 224.921 | 53 | 999 | 37.487 |
| L18 | `quality-assurance` | 6 Story (Epic-H) | 221.194 | 32 | 909 | 36.866 |
| **Tổng wave 3 (Story)** | | **41 Story** | **1.549.977** | **274** | — | **37.804** |
| L19 | `product-owner` | `Backlog-Priority.md` | _đang chờ_ | | | |
| L20 | `business-analyst` | `Glossary.md` (sửa) | _đang chờ_ | | | |

> **Số của wave 1 và wave 2 KHÔNG có trong file này.** Chúng nằm trong notification của các lô L1–L10, và context PM đã bị compaction **hai lần** trước khi `cost.md` được khởi tạo. Đây là **mất dữ liệu thật, không phải bỏ sót** — và nó chính là lý do bảng trên được ghi sớm thay vì để tới cuối run. Bài học đã có ngay: **khởi tạo `cost.md` cùng lúc với `outline.md`, không phải ở close-step.**

## 2. Hai quan sát đọc được ngay từ bảng

**2.1 `token / file` biến động 2,5 lần và KHÔNG tương quan với số file.**
`L13` viết **7 file** với **24.200 token/file** — rẻ nhất. `L16` viết **3 file** với **61.706 token/file** — đắt nhất, gấp **2,55×**. Nếu chi phí bám số file thì quan hệ phải ngược lại.

Nguyên nhân đọc được từ chính nội dung hai lô: `L16` là module `F` — **module dày số nhất của run**, và prompt của nó yêu cầu *"dùng budget dư để rà lại nhãn nguồn của **mọi** con số"*. Nó rà thật: giữ nguyên **cả hai** con số mâu thuẫn của Anifusion, giữ caveat *"SÀN không phải trần"* của `C7`. `L13` ngược lại — 7 Story cùng một domain (layout/comic-director), chia sẻ gần như cùng một tập anchor, nên chi phí đọc nguồn được **khấu hao trên 7 file**.

⇒ **Chi phí một lô bám vào "số nguồn khác nhau phải đọc", không bám vào "số file phải ghi".** Cắt lô theo Epic (cùng domain ⇒ cùng anchor) đã đúng; cắt lô theo số file sẽ sai.

**2.2 Tool call là chỉ báo tốt hơn token về độ khó xác minh.**
`L17` (pháp lý) dùng **53 tool call** — cao nhất, gấp **2,1×** `L14` (25 call). Nó không viết nhiều file hơn (6 vs 5). Nó **xác minh nhiều hơn**: `grep` để chứng minh hai văn bản cùng số 134 không bị trộn, `grep` để chứng minh Roadmap **không** có exit criterion cho hard-delete tenant (0 kết quả — một grep tốn tiền để chứng minh một sự vắng mặt).

⇒ Lô nào có ràng buộc *"không được bịa số hiệu"* thì **tool call tăng, không phải token tăng**. Khi ước lượng ngân sách cho lô kiểu này, nới **trần tool call** mới đúng chỗ; nới token là nới sai trục.

## 3. Bài học

_Viết sau khi verify L21–L24 và close-step hoàn tất — chưa có đủ dữ liệu để đúc kết phần này._

## 4. Tài liệu liên quan

- [Brief](./brief.md) · [Run plan](./run-plan.md) · [Outline](./outline.md) · [Escalations](./escalations.md)
- [cost.md của run trước](../2026-08-23-khoi-tao-tai-lieu-planning-comic-studio/cost.md) — nguồn của 5 bài học đã áp vào run này
