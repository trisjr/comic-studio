---
id: STORY-C-04
type: story
status: draft
created: 2026-08-24
---

# Story-Enforce-Max-Three-Characters-Per-Panel

## 1. Story

Là Founder (architect), tôi muốn **panel có 4 nhân vật bị DB TỪ CHỐI, không phải bị cảnh báo**, để **attribute binding không thất bại âm thầm**.

## 2. Part of

- Epic cha: [Epic-Comic-Director-And-Layout](../Epics/Epic-Comic-Director-And-Layout.md)
- BRD cha: [BRD-003-Comic-Director-And-Layout](../../020-Requirements/BRD/BRD-003-Comic-Director-And-Layout.md)
- UC liên quan: [UC-03-Review-Panel-Script](../../020-Requirements/Use-Cases/UC-03-Review-Panel-Script.md)

## 3. Bối cảnh & nguồn

- `MVP-Scope.md` §3 hạng mục **C5** — *"Cứng hoá ≤3 nhân vật/panel trong schema Comic IR"*: `🟡 kỷ luật tay` ở MVP0, `⛔` ở MVP1, `✅` từ MVP2. Căn cứ: CF-6.5 `[OFF]` — ID-Sim **42.33** (2 nhân vật) → **27.21** (3) → **2.67** (4) → **0.52** (5), *"near-complete failure beyond three subjects"*.
- `Roadmap.md` mốc **MVP2**, exit criterion **M2-2**: *"≤3 nhân vật/panel là CHECK constraint ở tầng DB — đo bằng: insert panel 4 nhân vật bị từ chối, không phải bị cảnh báo"*.
- `Charter-Comic-Studio.md` §7 **C3** — ràng buộc kiến trúc bắt buộc cho hạng mục này (lưu ý: không nhầm với `MVP-Scope §3` hạng mục `C3` là rubric layout — hai ID trùng ký hiệu nhưng khác tài liệu, phải luôn viết đủ "`Charter §7 C3`" khi trích).
- **attribute binding** (`Glossary.md`): việc model gắn đúng thuộc tính (trang phục, vật phẩm) cho đúng nhân vật trong panel nhiều người. Thất bại gần hoàn toàn từ 4 nhân vật trở lên — ảnh trông hợp lý nhưng gắn sai áo cho sai người.
- ⚠️ **Điều kiện siết ngưỡng**: `MVP-Scope §7.2` bảng kết luận gate G1 — nếu MVP0 đo `G1-d` (panel 2 nhân vật) dưới ngưỡng 50–60%, `Roadmap §3.3` ghi rõ hệ quả: *"cứng hoá thêm ≤2 nhân vật/panel thay vì ≤3 trong schema (đổi C5 ở bảng mục 3)"*. Story này phải implement ngưỡng **hiện tại là 3**, nhưng schema phải cho phép đổi ngưỡng thành 2 mà không cần thiết kế lại (ví dụ: hằng số cấu hình, không hard-code số 3 rải rác).

## 4. Acceptance Criteria

### Xác minh được

- [ ] Có `CHECK` constraint ở tầng DB trên bảng panel (hoặc bảng liên kết panel–character) giới hạn số nhân vật/panel ≤ ngưỡng cấu hình (mặc định 3) — đo bằng: insert 1 panel với đúng 3 nhân vật thành công.
- [ ] Insert panel với 4 nhân vật bị DB từ chối tại thời điểm ghi (lỗi constraint violation), không phải chỉ ghi log cảnh báo rồi vẫn lưu được — đo bằng: test insert panel 4 nhân vật, kiểm tra transaction bị rollback với lỗi constraint.
- [ ] Ngưỡng số nhân vật tối đa là một giá trị cấu hình được (không hard-code rải rác trong code), có thể đổi từ 3 xuống 2 bằng một thay đổi tại một chỗ duy nhất — đo bằng: đổi cấu hình ngưỡng, insert panel 3 nhân vật sau khi đổi bị từ chối.

### Đường không hạnh phúc (unhappy path)

- [ ] Panel được insert qua đường update (thêm nhân vật thứ 4 vào panel đã có 3 nhân vật) cũng bị `CHECK` constraint chặn giống như insert — đo bằng: test UPDATE thêm nhân vật thứ 4 vào panel hiện có, kiểm tra bị từ chối.
- [ ] Race condition: hai transaction đồng thời cùng thêm nhân vật vào một panel đang có 2 nhân vật (mỗi transaction thêm 1) không được để lọt panel có 4 nhân vật do đọc-rồi-ghi không khoá — đo bằng: test hai transaction đồng thời, kiểm tra tổng kết quả cuối cùng ≤3 nhân vật (constraint ở tầng DB tự nhiên chặn được trường hợp này vì kiểm tra tại thời điểm commit, không phải tại thời điểm đọc).

### Ràng buộc cứng không được vi phạm

- `Charter §7 C3` — ràng buộc kiến trúc: ≤3 nhân vật/panel phải nằm ở tầng schema, không phải guideline trong prompt.

### Story này KHÔNG làm

- [ ] KHÔNG giải quyết cảnh đông người bằng cách nới trần lên >3 — cảnh đông giải bằng shot xa / silhouette / crop, là trách nhiệm của `Story-Auto-Director-Scene-To-Page-Panel`, không phải của Story này.
- [ ] KHÔNG cảnh báo qua UI thay cho từ chối ở DB — cảnh báo mềm không thoả `M2-2`.
- [ ] KHÔNG tự động siết ngưỡng xuống 2 — việc siết ngưỡng chỉ xảy ra sau khi Founder đọc verdict `G1-d` của MVP0 và quyết định tại gate; Story này chỉ đảm bảo cơ chế **có thể** đổi ngưỡng dễ dàng.

## 5. Ước lượng

| Đại lượng | Giá trị | Ghi chú |
|---|---|---|
| `E_build` | **~6 giờ-người** `[EM]` | Một `CHECK` constraint + test insert/update/race condition — phạm vi hẹp, dưới trần 16h. |
| `E_hitl` | **0 giờ-người/chapter** | Ràng buộc DB thuần, không tạo nghĩa vụ review lặp lại cho người. |

## 6. INVEST

- **I (Independent)**: ✅ Mở rộng schema Comic IR bằng một constraint độc lập, không phụ thuộc logic của rubric hay `text_safe_zone`.
- **S (Small)**: ✅ Một constraint + bộ test — nhỏ, tự chứa, đúng nghĩa `Small` theo giờ-người.

---

_Created by product-owner_
_Author: trisjr_
