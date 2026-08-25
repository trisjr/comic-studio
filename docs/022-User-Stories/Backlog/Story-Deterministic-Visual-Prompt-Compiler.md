---
id: STORY-A-03
type: story
status: draft
created: 2026-08-24
---

# Story-Deterministic-Visual-Prompt-Compiler

## 1. Story

Là tác giả truyện chữ, tôi muốn cùng một `Panel Specification` luôn cho ra cùng một prompt, để panel sai là do spec sai, không do hệ thống ngẫu nhiên.

## 2. Part of

- Epic cha: [Epic-Image-Generation-Pipeline](../Epics/Epic-Image-Generation-Pipeline.md)
- BRD: [BRD-001-Image-Generation-Pipeline](../../020-Requirements/BRD/BRD-001-Image-Generation-Pipeline.md)
- Use Case liên quan: [UC-06-Generate-Panel-And-Pick-Variant](../../020-Requirements/Use-Cases/UC-06-Generate-Panel-And-Pick-Variant.md) (compiler biến spec thành prompt trong luồng sinh panel), [UC-03-Review-Panel-Script](../../020-Requirements/Use-Cases/UC-03-Review-Panel-Script.md) (panel script/Comic IR là input của compiler)

## 3. Bối cảnh & nguồn

- `MVP-Scope §3` hạng mục **A3**: *"Visual Prompt Compiler deterministic (lookup + policy, không LLM ở runtime)"* — `🟡 script` tại MVP0. Analysis §5.5: *"compiler deterministic là điều kiện cần để bảng `Generation` có nghĩa"*.
- `Roadmap` Pre-cycle 09/2026, exit criterion **P-2**: gate `G1` cần SỐ cho 5 tiêu chí; compiler tất định là điều kiện để `G1-a`…`G1-d` (do `Story-Generate-Panel-With-Reference-And-VLM-Select` đo) tách được lỗi "do spec sai" khỏi lỗi "do hệ thống ngẫu nhiên".
- `Glossary.md` term `Visual Prompt Compiler`: *"Phải là code deterministic, không phải LLM: tra bảng field value → cụm từ, sắp thứ tự, dedup, xử lý xung đột theo precedence ladder, thực thi constraint budget và ghi log ràng buộc bị drop."* Term `Precedence ladder`: *"Identity refs ở bậc cao nhất (không bao giờ bị drop); camera angle/composition/props phụ bị drop đầu tiên."*

## 4. Acceptance Criteria

### Xác minh được

- [ ] Cùng một `Panel Specification` (input y hệt) chạy qua compiler 2 lần liên tiếp cho ra prompt text giống hệt nhau byte-for-byte — đo bằng: so sánh string output của 2 lần chạy
- [ ] Compiler chạy được và sinh ra prompt ngay cả khi không có API key / network sinh ảnh bị chặn — đo bằng: chạy compiler trong môi trường bị cắt network, xác nhận prompt vẫn sinh ra được (chứng minh compiler không gọi LLM/API nào ở runtime)
- [ ] Khi vượt constraint budget, ràng buộc bị drop tuân đúng precedence ladder: identity refs không bao giờ bị drop; camera angle/composition/props phụ bị drop trước — đo bằng: test case cố tình vượt budget, kiểm tra thứ tự ràng buộc bị loại trong log
- [ ] Mỗi lần drop một ràng buộc do vượt constraint budget, compiler ghi log ràng buộc đã bị drop — đo bằng: kiểm tra log output có dòng ghi nhận tương ứng

### Đường không hạnh phúc (unhappy path)

- [ ] `Panel Specification` chứa field không có trong bảng tra (field value → cụm từ) ⇒ compiler phải báo lỗi rõ ràng, không được tự bịa cụm từ hoặc bỏ qua âm thầm
- [ ] Hai ràng buộc xung đột nhau cùng ở bậc cao nhất của precedence ladder (ví dụ hai identity ref mâu thuẫn) ⇒ compiler phải dừng và yêu cầu sửa spec, không tự chọn một bên
- [ ] Constraint budget bị vượt tới mức toàn bộ ràng buộc identity refs cũng phải drop mới vừa ⇒ đây là lỗi thiết kế spec, compiler phải từ chối sinh prompt thay vì sinh một prompt thiếu identity

### Ràng buộc cứng không được vi phạm

—

### Story này KHÔNG làm

- Không tự sửa hoặc gợi ý sửa `Panel Specification` khi phát hiện lỗi — chỉ báo lỗi; việc sửa spec thuộc về `Story-Comic-IR-Panel-Specification` / con người
- Không gọi provider sinh ảnh — đó là việc của `Story-Image-Provider-Adapter`
- Không tối ưu độ dài prompt cho một provider cụ thể ngoài phạm vi tối thiểu cần cho MVP0
- Không xử lý panel spec dạng whole-page (nhiều panel gộp một prompt) — thuộc `Story-Whole-Page-Render-Granularity` (MVP3, ngoài horizon)

## 5. Ước lượng

| Đại lượng | Giá trị | Ghi chú |
|---|---|---|
| `E_build` | ~14 giờ-người `[EM]` | Trong trần 16h. Không có breakdown per-task trong nguồn, ước lượng riêng của writer |
| `E_hitl` | 0 | Compiler là code deterministic, không tạo nghĩa vụ giờ-người lặp lại theo chapter |

## 6. INVEST

`I`: ✅ — Compiler là một thành phần tách biệt về deliverable (nhận spec, trả prompt); không cần sửa các Story khác để hoàn thành.

`S`: ⚠️ — Epic cha (`Epic-Image-Generation-Pipeline.md` mục 3) đánh dấu cờ vỡ cho Story này, nhưng `findings/business-analyst.md` §4.10 (danh sách 7 Story vỡ có lý do tường minh) **không liệt kê** Story này. Lý do dưới đây là **suy luận của writer** (`[PO]`), không phải trích nguyên văn nguồn: theo `Glossary.md`, compiler phải xử lý đồng thời toàn bộ precedence ladder + constraint budget cho mọi loại field trong `Panel Specification` để logic drop-ràng-buộc có nghĩa; tách nhỏ theo từng loại field riêng lẻ (ví dụ chỉ làm "camera angle" trước, "identity" sau) sẽ cho ra một compiler chưa tất định đúng nghĩa cho tới khi đủ mọi loại field. Ghi lại để PM đối chiếu với writer gốc của `Epic-Image-Generation-Pipeline` nếu cần xác nhận.

⚠️ Story này **mở ở MVP0 nhưng KHÔNG thuộc** danh sách 5 Story `[MVP0]` `n/a` của `findings/business-analyst.md` §4.9 — theo đúng ghi chú của Epic cha, Story này **vẫn được chấm INVEST bình thường** như trên.

---

_Created by product-owner_
_Author: trisjr_
