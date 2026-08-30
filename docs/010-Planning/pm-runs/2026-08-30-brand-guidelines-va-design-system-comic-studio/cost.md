# Cost: 2026-08-30-brand-guidelines-va-design-system-comic-studio

> ⚠️ **Số subagent là ƯỚC LƯỢNG, ⛔ không phải số đo.** Tính theo đơn giá Opus `cache_read $0,5` · `cache_create $6,25` · `output $25` mỗi MTok. Số token thì **đo thật** từ `.message.usage` trong transcript.
> Nguồn: `~/.claude/projects/-Users-trisjr-Projects-Personal-comic-studio--claude-worktrees-phase-3-brand-design-system/b9b288a9-….jsonl` + `…/subagents/*.jsonl`.
> ⛔ **`cost-state` trong transcript KHÔNG bao gồm subagent** — bảng dưới cộng tay thư mục `subagents/`.

## Bảng chi phí

| Actor | Tool calls | Turns | cache_read | cache_create | output | ctx/turn | **$ ước** |
|---|---:|---:|---:|---:|---:|---:|---:|
| **PM (main loop)** | ~95 | **210** | 48,24M | 1,33M | 455k | **230k** | **43,80** |
| Lô 6 — verify (2 pass) | 54 + 20 | 155 | 17,33M | 1,19M | 77k | 112k | **18,06** |
| Lô 4 — `Components.md` | 45 | 96 | 9,61M | 1,41M | 64k | 100k | 15,18 |
| Lens — `business-analyst` | 33 | 53 | 5,74M | 1,30M | 58k | 108k | 12,44 |
| Lô 3 — `Typography.md` | 29 | 51 | 3,62M | 0,85M | 42k | 71k | 8,18 |
| Lens — `architect` | 29 | 51 | 4,05M | 0,75M | 56k | 79k | 8,08 |
| Lô 5 — `Glossary.md` | 35 | 64 | 6,43M | 0,46M | 38k | 100k | 7,02 |
| Lens — `product-designer` | 20 | 39 | 3,71M | 0,59M | 44k | 95k | 6,63 |
| Lô 1 — Brand + Foundations | 20 | 37 | 2,89M | 0,38M | 72k | 78k | 5,62 |
| Lô 2 — Color + Spacing | 19 | 36 | 2,28M | 0,37M | 66k | 63k | 5,13 |

**Tổng**: **103,9M `cache_read`** · **8,63M `cache_create`** · 909k `output` ≈ **$130,1**
**Tỷ lệ**: PM **33,7%** ($43,80) / subagent **66,3%** ($86,34)

## Vượt ngân sách

⭐ **⛔ KHÔNG lô nào vượt trần tool call đã cấp ở gate.** Cao nhất là Lô 4 với **45/60**. Verify chạy hai pass: **54/60** rồi **20/25** — mỗi pass đều dưới trần của nó.

> So sánh: run `2026-08-28` cấp trần trong **46/46** prompt mà vẫn có **8/46 lô vượt** (63→160 call), tiêu **$102 = 24%** chi phí subagent, ⛔ không lô nào bị chặn. Khác biệt ở run này ⛔ không phải nhờ trần — trần y hệt — mà nhờ **cắt lô nhỏ hơn**: lô lớn nhất chỉ có **2 file** hoặc **1 file nặng**, ⛔ không lô nào ôm cả một tầng tài liệu.

## Số lô thực tế so với plan

**7/6 lô** — vượt **17%**, dưới ngưỡng 50% nên ⛔ không cần biện minh dài. Lô thứ 7 là **verify pass 2**, phát sinh vì verify pass 1 tìm ra 2 CRITICAL. Đó là **chi phí của tính đúng đắn**, ⛔ không phải lỗi lập lịch.

## Phân bổ theo NHÓM MỤC ĐÍCH

| Nhóm | $ | % | Ghi chú |
|---|---:|---:|---|
| **PM điều phối** | 43,80 | **33,7%** | Triage · gate · outline · MOC · Index · vá CRITICAL · đo chi phí |
| **Sản xuất** (Lô 1–5) | 41,13 | **31,6%** | 6 file Design System + Glossary |
| **Phân tích** (3 lens) | 27,15 | **20,9%** | Dựng 38 ràng buộc + 19 surface + phạm vi tài liệu **trước** khi viết |
| ⭐ **Verify** (Lô 6, 2 pass) | 18,06 | **13,9%** | **Khoản SINH LỜI — đọc mục dưới** |
| Dọn dẹp | **0** | **0%** | ⛔ Không có lô dọn nào |
| Rework | **0** | **0%** | ⛔ Không dispatch lại writer nào; 2 CRITICAL do PM tự vá (3 dòng) |

### ⭐ Verify là khoản SINH LỜI, ⛔ không phải overhead

`pm-core.md` cảnh báo: một `cost.md` trình bày verify lẫn trong *"phần không sinh nội dung mới"* là tài liệu **gây hại** — nó dụ run sau cắt đúng thứ rẻ nhất và đáng giá nhất. Ở run này, **$18,06** mua được:

- **2 CRITICAL** — cả hai là **lỗi đếm trong câu tóm tắt một bảng**, và **một trong hai là lỗi của PM** ở `Design-MOC.md` + `000-Index.md`, tức **hai file ⛔ không ai khác nhìn vào**. ⛔ Không có verify pass thì lỗi đó đóng run cùng deliverable.
- **1 WARNING sinh ra từ chính bản vá của PM** — callout mới trỏ *"cột cuối"* trong khi cột cuối mang nghĩa **ngược lại**. Bắt được vì PM **cố ý yêu cầu soi lại phần mình vừa sửa**.
- **Bằng chứng dương cho phần kỹ thuật**: tính lại độc lập **15/27 hàng contrast** (thực tế phủ 17/27) — **khớp delta 0,00**; `V-1`…`V-8` PASS 8/8; checklist 14/14; 0 link gãy; 90 headword Glossary cũ nguyên vẹn (verify bằng `git diff`).

⇒ Verify **⛔ không** chỉ tìm lỗi; nó **biến "tôi tin là đúng" thành "đã kiểm bằng lệnh này, kết quả này"**. Đó là thứ 13,9% mua được.

## Guardrail cần cập nhật trong `pm-core.md`

| # | Số cũ | Đo được ở run này | Đề nghị |
|---|---|---|---|
| **1** | *"PM đắt gấp **2,75 lần** worker mỗi turn"* (run `2026-08-28`: PM `$0,316` vs worker `$0,115`) | PM **$0,209**/turn · worker **$0,148**/turn ⇒ **1,41 lần** | ⭐ **Cập nhật thành một khoảng `1,4–2,8×`**, ⛔ không phải hằng số. Chênh lệch thu hẹp khi PM ⛔ **không** tự đọc lại file writer vừa ghi và ⛔ **không** tự ôm lô quét (Glossary giao worker). Nhưng ctx/turn của PM vẫn **230k** so với **63–112k** của worker — ⭐ **PM vẫn là chỗ duy nhất luật siêu tuyến tính còn hiệu lực** |
| **2** | *"`cache_create` đắt gấp 12,5 lần `cache_read`… ⛔ đừng chỉ báo cáo `cache_read`"* | **8,63M `cache_create` = $53,9 ≈ 41% tổng chi phí**, so với 103,9M `cache_read` = $52,0 ≈ 40% | ⭐ **Nâng mức cảnh báo.** Ở run này `cache_create` **đắt HƠN** `cache_read` về tuyệt đối, dù ít hơn **12 lần** về token. Run nhiều lô ngắn ⇒ nhiều lần dựng cache mới ⇒ đây là **cái giá thật của việc cắt lô**, và nó ⛔ chưa được nêu ở mục *Cắt nhỏ dispatch* |
| **3** | Chế độ B — *"lô được cắt ngắn ⇒ gần tuyến tính, `k ≈ 0,94`"* | `$/turn` theo nhóm: <40 turns **0,148** · 40–60 **0,152** · 60–100 **0,150** · ≥150 **0,117** | ✅ **Xác nhận lại chế độ B.** `$/turn` gần **hằng số** qua mọi nhóm kích thước, lô dài nhất lại **rẻ nhất** mỗi turn. ⛔ Không cần sửa |
| **4** | Overhead spawn *"~23,6k token, thực tế nay thấp hơn ~1,5k"* | Chưa đo lại ở run này | ⚠️ **Nợ đo.** Cần lấy `cache_read` turn đầu của 9 subagent để hiệu chuẩn |

## Điều đáng ghi nhất về chi phí run này

⭐ **0% dọn dẹp và 0% rework** — so với run `2026-08-28` có **dọn dẹp 20,9% + rework 22,9% = 43,8%**.

Nguyên nhân trực tiếp, ⛔ không phải may mắn: run đó để lô **sửa** `SRS` chạy **cùng lúc** với hai lô **đọc** `SRS` ⇒ ba hệ toạ độ số dòng ⇒ 8 lô dọn. Run này áp đúng guardrail sinh ra từ bài học đó — **Lô 1 chạy một mình trước** vì `Foundations.md` là nguồn của 4 file sau, và Lô 2 ‖ Lô 3 chỉ song song **sau khi** Lô 1 đã đóng. Chi phí của kỷ luật đó là **một lô tuần tự thêm**; khoản tiết kiệm là **43,8% ngân sách** mà run trước phải trả.
