---
id: COST-2026-08-30-DONG-BO-SRS-NFR-VOI-ADR
type: run-cost
run: 2026-08-30-dong-bo-srs-nfr-voi-adr
status: done
created: 2026-08-30
---

# Cost — run đồng bộ `SRS` ↔ `ADR`

> ⚠️ **Số `$` là ƯỚC LƯỢNG, ⛔ không phải số đo.** Đơn giá Opus: `cache_read` **$0,5** · `cache_create` **$6,25** · `output` **$25** mỗi MTok. **Token thì đo thật** từ `.message.usage` trong transcript.
> Nguồn: `~/.claude/projects/…-phase-3-brand-design-system/b9b288a9-….jsonl` + `…/subagents/agent-*.jsonl`.
> ⚠️ **Cách tính PM**: transcript chính gộp **cả run trước**. PM run này = tổng (429 turn · 100,62M read) **trừ** phần run `2026-08-30-brand-guidelines…` đã ghi (210 turn · 48,24M read). ⚠️ Run này có **một lần compaction** giữa chừng, nên con số PM là **cận dưới**.

## Bảng chi phí

| Actor | Tool calls | Turns | cache_read | cache_create | output | ctx/turn | **$ ước** |
|---|---:|---:|---:|---:|---:|---:|---:|
| **PM (main loop)** | ~40 | **219** | 52,38M | 0,80M | 321k | **239k** | **39,23** |
| Lens — `architect` | 28 | 49 | 3,39M | 0,79M | 54k | 69k | **7,96** |
| Lô 4a — verify pass 1 | 29 | 59 | 5,05M | 0,45M | 54k | 86k | **6,71** |
| Lô 1 — `SRS` (`business-analyst`) | 43 | 79 | 5,85M | 0,33M | 30k | 74k | 5,74 |
| Lô 2b — Architecture (`architect`) | 48 | 77 | 4,46M | 0,22M | 23k | 58k | 4,19 |
| Lô 4b — verify pass 2 | 25 | 46 | 2,57M | 0,25M | 38k | 56k | 3,80 |
| Lô 2a — Security/API/Schema | 32 | 65 | 3,62M | 0,25M | 16k | 56k | 3,76 |

**Tổng**: **77,3M `cache_read`** · **3,09M `cache_create`** · 536k `output` ≈ **$71,4**
**Tỷ lệ**: PM **55,0%** ($39,23) / subagent **45,0%** ($32,16)

## Vượt ngân sách

⭐ **⛔ KHÔNG lô nào vượt trần.** Cao nhất là Lô 2b với **48/60**. Verify pass 2 dùng **25/25** — chạm trần đúng bằng ngân sách được cấp, ⛔ không vượt.

## Số lô thực tế so với plan

**6/5 lô** — vượt **20%**. Lô thứ 6 là **verify pass 2**, phát sinh vì pass 1 tìm ra 3 WARNING **đều nằm ở phần PM tự sửa**. Đó là **chi phí của tính đúng đắn**, ⛔ không phải lỗi lập lịch — và nó **sinh lời**, xem mục dưới.

## Phân bổ theo NHÓM MỤC ĐÍCH

| Nhóm | $ | % | Ghi chú |
|---|---:|---:|---|
| **PM điều phối** | 39,23 | **55,0%** | Triage · gate 4 câu · outline · close-step · **vá 5 WARNING của chính mình** · đo chi phí |
| **Sản xuất** (Lô 1, 2a, 2b) | 13,69 | **19,2%** | 21 điểm `SRS` + 15 điểm ripple + 4 ADR accept |
| ⭐ **Verify** (2 pass) | 10,51 | **14,7%** | **Khoản SINH LỜI — đọc mục dưới** |
| **Phân tích** (1 lens) | 7,96 | **11,2%** | Dựng bản đồ 19 + 16 điểm sửa **trước** khi viết; bác 1 tiền đề sai của PM |
| Dọn dẹp | **0** | **0%** | ⛔ Không có lô dọn nào |
| Rework | **0** | **0%** | ⛔ Không dispatch lại writer nào — cả 5 WARNING đều do PM tự vá |

### ⭐ Verify là khoản SINH LỜI — run này là bằng chứng mạnh nhất từ trước tới nay

**$10,51 (14,7%)** mua được **5 WARNING**, và ⭐ **cả 5 đều là lỗi của PM**, nằm ở **6 điểm PM tự sửa mà ⛔ không writer nào review**:

| Pass | Mã | Lỗi | Vì sao ⛔ không ai khác bắt được |
|:--:|---|---|---|
| 1 | `W-1` | `000-Index:178` ghi *"16 điểm ripple"* — PM cộng header hai lô trong `outline` thay vì đếm `git diff` | ⭐ **Đúng lỗi `E9`/`E10`** mà PM dựng `K-1` để chặn **writer** — rồi tự mắc |
| 1 | `W-2` | `000-Index:220` nói shadcn *"MẶC ĐỊNH có đường lui"*, mâu thuẫn `E7` #2 của **chính run này** | Rủi ro thật: lô sau đọc Index trước ⇒ **đóng mất** khoản nợ cố ý để mở |
| 1 | `W-3` | `ADR-006:270` còn `(vendor TBD)`, tự mâu thuẫn với `:257` **cách 13 dòng** | Dòng này ⛔ không nằm trong bảng *Ripple* lập tại gate ⇒ ⛔ không ai được giao kiểm |
| 2 | `N-1` | Con số ripple phải là **15**, PM vá thành `14` | ⭐ **Chính patch `W-3` sinh thêm điểm thứ 15.** PM trích lại `14` từ pass 1 mà ⛔ không đếm lại sau khi tự vá — và dòng đó **tự dán nhãn** *"đếm cơ học, ⛔ không trích lại"* |
| 2 | `N-2` | `E1` dùng toạ độ **pre-shift** — `ADR-001:15` nay là **dòng trống**, `:172` là **dòng phân cách bảng** | Run này chèn `updated:` vào dòng 7 ⇒ mọi dòng ≥7 dịch **+1**. ⭐ Một **rào chắn** *"đừng sửa dòng này"* đang trỏ vào dòng trống |

⇒ ⭐ **Kết luận cứng: điểm yếu nhất của lane này ⛔ không phải writer — mà là PM.** Writer có `[CONSTRAINTS]`, có tự nghiệm thu, có người review. PM ⛔ **không có gì cả** trừ verify pass. Ba lô writer báo `DONE` và **cả ba đều đúng**; 100% WARNING đến từ PM.

## Guardrail cần cập nhật trong `pm-core.md`

| # | Số cũ | Đo được ở run này | Đề nghị |
|---|---|---|---|
| **1** | *"PM đắt gấp **2,75 lần** worker mỗi turn"* → run trước đo **1,41×**, đề nghị đổi thành khoảng `1,4–2,8×` | PM **$0,179**/turn · worker **$0,086**/turn ⇒ ⭐ **2,09×** | ✅ **XÁC NHẬN khoảng `1,4–2,8×`.** Ba run cho `2,75` · `1,41` · `2,09` — nằm gọn trong khoảng. ⛔ Đừng dùng hằng số |
| **2** | *"PM vẫn là chỗ duy nhất luật siêu tuyến tính còn hiệu lực"* | ctx/turn: PM **239k** · worker **56–86k** | ✅ **XÁC NHẬN, và mạnh hơn trước.** PM gấp **2,8–4,3×** worker về ctx/turn |
| **3** | *"`cache_create` đắt hơn `cache_read` về tuyệt đối"* (run trước: 41% vs 40%) | `create` **$19,3 = 27,1%** · `read` **$38,7 = 54,2%** | ⚠️ **Phụ thuộc số lô, ⛔ không phải hằng số.** Run trước **9 lô** ⇒ create 41%; run này **6 lô** ⇒ create 27%. Đề nghị phát biểu lại: *"`cache_create` ≈ **$3–6 mỗi lô** dựng mới; cắt thêm một lô ⇒ trả thêm khoảng đó"* |
| **4** | Tỷ lệ PM/subagent | Run trước **33,7/66,3** · run này ⭐ **55,0/44,9** | ⚠️ **Đảo chiều.** Nguyên nhân: run này chỉ có **1 lens + 3 writer nhỏ**, trong khi PM phải tự làm close-step, tự vá 5 WARNING, và chịu **một lần compaction**. ⇒ Run *sweep nhỏ* có hình dạng chi phí **ngược** với run *sản xuất lớn* |
| **5** | — (mới) | Verify **14,7%** bắt **5/5 lỗi**, tất cả của PM | ⭐ **Đề nghị thêm guardrail**: *"Với run mà PM tự tay sửa file (close-step, MOC, Index), **verify pass 2 soi riêng bản vá của PM là BẮT BUỘC**, ⛔ không phải tuỳ chọn."* Hai run liên tiếp, pass 2 đều bắt được lỗi **sinh ra từ chính bản vá của PM** |

## Điều đáng ghi nhất về chi phí run này

⭐ **0% dọn dẹp, 0% rework — hai run liên tiếp.** Guardrail *"lô đọc ⛔ không chạy song song với lô sửa cùng file"* lại đúng: Lô 1 (`SRS`) chạy **một mình**, Lô 2a ‖ 2b chỉ song song **sau khi** `SRS` đã land — vì `SDD:458` **trích nguyên văn** hàng `b-7` của `SRS`.

⚠️ **Nhưng bảng *Ripple* lập tại gate ⛔ KHÔNG đủ.** Hai điểm sửa (`ADR-002:85`, `ADR-006:270`) là **lệch do chính run này sinh ra**, ⛔ không có trong plan — chiếm **2/15** điểm ripple. Bài học: với Shape B, *"quét hết phạm vi đã duyệt ở gate"* là **điều kiện cần, ⛔ chưa đủ**; phải có một pass **đọc lại chính diff của mình** để tìm lệch mới sinh.

---

_Created by TNMCORE-OS (PM)_
_Author: trisjr_
