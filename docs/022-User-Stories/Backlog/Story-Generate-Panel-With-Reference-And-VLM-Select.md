---
id: STORY-A-01
type: story
status: draft
created: 2026-08-24
---

# Story-Generate-Panel-With-Reference-And-VLM-Select

## 1. Story

Là tác giả truyện chữ, tôi muốn sinh 3 ứng viên cho một panel từ ảnh reference rồi để VLM chọn 1, để có panel dùng được mà không phải tự chấm từng ảnh.

## 2. Part of

- Epic cha: [Epic-Image-Generation-Pipeline](../Epics/Epic-Image-Generation-Pipeline.md)
- BRD: [BRD-001-Image-Generation-Pipeline](../../020-Requirements/BRD/BRD-001-Image-Generation-Pipeline.md)
- Use Case liên quan: [UC-06-Generate-Panel-And-Pick-Variant](../../020-Requirements/Use-Cases/UC-06-Generate-Panel-And-Pick-Variant.md)

## 3. Bối cảnh & nguồn

- `MVP-Scope §3` hạng mục **A1**: *"Generate panel: reference + N candidate + VLM select"* — `✅` tại MVP0. CF-8.4: *"code MVP0 làm đúng một việc này"*. CF-3.1/3.2 `[OFF]`: N=3 best-of-N, *"performance saturates at N=3"*.
- `Roadmap` Pre-cycle 09/2026, exit criterion **P-2**: *"[G1] có SỐ cho cả 5 tiêu chí và verdict được ghi (PASS / PASS CÓ ĐIỀU KIỆN / FAIL)"*. Story này là nguồn dữ liệu chính cho **4/5 tiêu chí** đó (`G1-a`, `G1-b`, `G1-c`, `G1-d`); `G1-e` (typeset) thuộc `Story-Typeset-Layer-And-Bubble-Overlay`.
- Ràng buộc kỹ thuật N=3: `Charter §7 C8` — *"N = 3 là mặc định cho MỌI panel, KHÔNG phải retry-on-failure"*. `OKRs §6 AG-7` (anti-goal): *"hạ N=3 xuống N thấp hơn để cứu margin"* — cấm.
- ⚠️ Story này thuộc nhóm 5 Story `[MVP0]` của `findings/business-analyst.md` §4.9 — **INVEST không áp** (xem mục 6).

## 4. Acceptance Criteria

### Xác minh được

- [ ] Consistency nhân vật đạt **≥70%** panel được nhận ra là cùng một nhân vật mà không cần retry — đo bằng: nhìn 8 panel liền nhau, chấm bằng mắt trên toàn bộ panel MVP0, ghi vào bảng kết quả (`G1-a`, `[EM]` ngưỡng do run trước định nghĩa)
- [ ] N tối thiểu để VLM-select ra panel đạt là **≤3** — đo bằng: chạy cùng bộ panel ở N=2 và N=3, so tỉ lệ panel đạt giữa hai lần chạy (`G1-b`)
- [ ] `reject_rate` sau VLM-select có **giá trị số được đo và ghi lại**, và verdict được phân loại theo đúng ba dải đã định nghĩa **TRƯỚC** khi đo (`≤30%` PASS · `30–50%` PASS CÓ ĐIỀU KIỆN · `>50%` FAIL) — đo bằng: `reject_rate = số panel người loại / tổng panel VLM đã chọn` (`G1-c`, `[EM]` ngưỡng do run trước định nghĩa, không có nguồn ngoài)
- [ ] Panel 2 nhân vật đạt **≥60%** đúng identity VÀ đúng attribute binding (trang phục/vật phẩm gắn đúng người) — đo bằng: chấm hai trục riêng trên từng panel (`G1-d`, `[EM]`)
- [ ] Panel 3 nhân vật: tỉ lệ đúng identity + đúng attribute binding được **đo và ghi vào báo cáo**, không dùng làm điều kiện PASS/FAIL (`G1-d`, phần không đặt ngưỡng chặn)
- [ ] Mỗi panel sinh ra đúng **3** ứng viên (N=3), không phải 1 hay 2 — đo bằng: đếm số file ảnh candidate sinh ra mỗi lần chạy script

### Đường không hạnh phúc (unhappy path)

- [ ] Cả 3 candidate đều bị VLM chấm dưới ngưỡng chấp nhận ⇒ panel phải được đánh dấu "cần chạy lại", **không** được tự động chọn candidate tệ nhất trong 3
- [ ] Ảnh reference nhân vật bị thiếu hoặc không đọc được ⇒ script phải dừng và báo lỗi rõ ràng cho panel đó, không generate mà thiếu reference
- [ ] Chi phí API vượt trần an toàn **~$25** mà chưa đủ 8 panel liền nhau để chấm consistency ⇒ dừng lại, ghi số đã đo, kết luận với dữ liệu đang có — không tiếp tục chi tới hết ngân sách (`Roadmap §3.1` rủi ro MVP0 "Tràn ngân sách vì lặp nhiều vòng")
- [ ] VLM trả về lựa chọn không nằm trong 3 candidate đã sinh (lỗi định dạng response) ⇒ panel bị đánh dấu lỗi kỹ thuật, không tính vào mẫu đo `G1-a`…`G1-d`

### Ràng buộc cứng không được vi phạm

- `Charter §7 C8` / `OKRs §6 AG-7`: cấm lấy chất lượng đo được ở N=3 để suy ra hoặc biện minh chi phí ở N=2 (tương đương lệnh cấm CẤM-03 của `findings/business-analyst.md` §5.3). Hạ N là đổi chất lượng lấy margin — phải chạy lại **G1**, không phải chỉ G2.

### Story này KHÔNG làm

- Không lưu generation vào database — MVP0 không có DB, chỉ có script + file phẳng (`MVP-Scope §3.1`)
- Không bao gồm typeset layer / bubble overlay (thuộc `Story-Typeset-Layer-And-Bubble-Overlay`)
- Không triển khai Continuity Checker như một cơ chế sản phẩm hoàn chỉnh — ở MVP0 đây chỉ là một lần VLM-select thô, chưa phải cơ chế N-candidate selection đầy đủ của hạng mục H3
- Không hỗ trợ nhiều adapter provider — chỉ dùng 1 adapter cố định cho MVP0 (thuộc `Story-Image-Provider-Adapter`)
- Không tối ưu chi phí ngoài phạm vi **~$12–25** đã cấp cho MVP0 (CF-3.11)

## 5. Ước lượng

| Đại lượng | Giá trị | Ghi chú |
|---|---|---|
| `E_build` | ~24 giờ-người `[EM]` | Không có breakdown per-task trong nguồn; suy ra từ CF-8.4 (toàn bộ MVP0 = 1–2 tuần cho một người, script này là phần lõi chiếm phần lớn thời lượng đó). **Vượt trần 16h** — nhưng xem mục 6: Story `[MVP0]`, trần `Small` của khuôn INVEST không áp cho nhóm này |
| `E_hitl` | `TBD` | MVP0 là lát cắt dùng một lần rồi bỏ, không phải quy trình lặp lại theo chapter. Chi phí chấm `G1-a`…`G1-d` là chi phí **đo một lần** để ra ngưỡng, không phải nghĩa vụ vận hành lặp lại — số `E_hitl` thật cho vận hành sản xuất chỉ có ý nghĩa **sau khi** MVP0 chạy xong (`findings/product-owner.md` §4.3 W8) |

## 6. INVEST

`INVEST không áp — Story thuộc [MVP0]`. Lý do (`findings/business-analyst.md` §4.9, `MVP-Scope §3.1`, `Roadmap §3.1`): code của MVP0 không phải nền của sản phẩm — viết để trả lời câu hỏi rồi bỏ, giữ lại kết luận và dữ liệu. Story này là một lát cắt xuyên tầng để mua thông tin cho gate G1, không phải một tính năng giao cho khách; tiêu chí `Valuable` của nó là **thông tin đo được**, không phải tính năng.

**Definition of Done — 5 tiêu chí gate G1** (`MVP-Scope §7.2`, thay cho Acceptance Criteria kiểu Gherkin thông thường):

- [ ] `G1-a` Consistency nhân vật ≥70% (Story này sở hữu — xem AC-1)
- [ ] `G1-b` N tối thiểu ≤3 (Story này sở hữu — xem AC-1)
- [ ] `G1-c` `reject_rate` có số và verdict phân loại đúng dải (Story này sở hữu — xem AC-1)
- [ ] `G1-d` Panel 2 nhân vật ≥60% đúng identity + attribute binding; panel 3 nhân vật đo và báo cáo (Story này sở hữu — xem AC-1)
- [ ] `G1-e` 100% panel có thoại dùng overlay, 0 panel nhờ model render chữ — **thuộc `Story-Typeset-Layer-And-Bubble-Overlay`, không thuộc Story này**; liệt kê tại đây chỉ để đủ danh sách 5 tiêu chí gate

⛔ Dùng đúng tên **MVP0** — `Glossary.md` cấm *"phase 0"*, *"spike"*, *"PoC"* (CẤM-11).

---

_Created by product-owner_
_Author: trisjr_
