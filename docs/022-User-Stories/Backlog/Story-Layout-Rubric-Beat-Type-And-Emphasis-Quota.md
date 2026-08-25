---
id: STORY-C-03
type: story
status: draft
created: 2026-08-24
---

# Story-Layout-Rubric-Beat-Type-And-Emphasis-Quota

## 1. Story

Là tác giả truyện chữ, tôi muốn **panel quan trọng được cấp diện tích lớn hơn theo một bảng tra rời rạc**, để **bố cục có nhịp mà không cần một điểm số không kiểm chứng được**.

## 2. Part of

- Epic cha: [Epic-Comic-Director-And-Layout](../Epics/Epic-Comic-Director-And-Layout.md)
- BRD cha: [BRD-003-Comic-Director-And-Layout](../../020-Requirements/BRD/BRD-003-Comic-Director-And-Layout.md)
- UC liên quan: [UC-08-Arrange-Page-And-Preview](../../020-Requirements/Use-Cases/UC-08-Arrange-Page-And-Preview.md)

## 3. Bối cảnh & nguồn

- `MVP-Scope.md` §3 hạng mục **C3** — *"Layout: rubric `beat_type` + emphasis quota (rời rạc, bảng tra)"*: `❌` ở MVP0, `⛔` ở MVP1, `✅` từ MVP2. Căn cứ: CF-8.8 · CF-9.3.
- `MVP-Scope.md` §4.3 *"Layout Score số thực — CẮT (CF-9.3)"*: quyết định là cắt **cơ chế** 5 số thực, **giữ mục tiêu** (layout theo narrative importance) → thay bằng rubric `beat_type` rời rạc + bảng tra deterministic + emphasis quota theo chapter. Lý do cắt: không có prior art, *"chưa ai làm vì không đáng"*, không kiểm chứng được đúng/sai.
- `Roadmap.md` mốc **MVP2**, exit criterion tổng quát **M2-1** (Director sinh page/panel tự động) là điều kiện ra gần nhất áp dụng cho hạng mục này — Roadmap không có một `M2-x` riêng cho rubric; §3.3 mục *"Nội dung theo CF-8.8"* liệt kê *"Bỏ Layout Score số thực → rubric `beat_type` + emphasis quota"* là điều chỉnh #1 trong bốn điều chỉnh của MVP2, căn cứ CF-9.3.
- `Layout Score` (`Glossary.md`): điểm đánh giá bố cục trang; cơ chế **số thực đã bị cắt** (không đo được, không calibrate được, tạo cảm giác chính xác giả); thay bằng rubric rời rạc + emphasis quota. Mục tiêu giữ, cơ chế bỏ.

## 4. Acceptance Criteria

### Xác minh được

- [ ] Mỗi panel spec có trường `beat_type` nhận giá trị từ một tập enum rời rạc cố định (ví dụ: climax, reaction, transition, establishing) — đo bằng: 100% panel spec sinh ra ở MVP2 có `beat_type` thuộc enum, không có giá trị tự do.
- [ ] Bảng tra `beat_type → diện tích panel` là deterministic: cùng một `beat_type` luôn cho ra cùng một hạng diện tích (ví dụ: cùng bucket lớn/vừa/nhỏ) — đo bằng: chạy bảng tra 2 lần trên cùng input, kết quả diện tích giống hệt nhau.
- [ ] Emphasis quota theo chapter được cưỡng chế: số panel được gán hạng "lớn" trong một chapter không vượt quá quota đã định nghĩa cho chapter đó — đo bằng: đếm panel hạng lớn trong 1 chapter test, so với quota cấu hình.

### Đường không hạnh phúc (unhappy path)

- [ ] Chapter có số beat "climax" vượt quota cho phép: hệ thống phải có quy tắc tie-break rõ ràng (ví dụ theo thứ tự xuất hiện) thay vì gán ngẫu nhiên hoặc gán tất cả đều lớn — đo bằng: test chapter có 5 climax với quota 2, kiểm tra đúng 2 panel được gán hạng lớn theo quy tắc đã định nghĩa.
- [ ] Panel không xác định được `beat_type` (dữ liệu scene thiếu tín hiệu) rơi vào giá trị mặc định tường minh (ví dụ "transition"), không được để trống hoặc gây lỗi dừng pipeline — đo bằng: test input scene thiếu tín hiệu, kiểm tra panel spec vẫn có `beat_type` hợp lệ.

### Ràng buộc cứng không được vi phạm

- —

### Story này KHÔNG làm

- [ ] KHÔNG cài đặt cơ chế Layout Score 5 số thực dưới bất kỳ hình thức nào — hạng mục `C4` đã **cắt hẳn** (`CF-9.3`); mục tiêu narrative importance được giữ, nhưng cơ chế số thực không được viết lại dưới tên khác.
- [ ] KHÔNG tự sinh page/panel từ scene — đó là `Story-Auto-Director-Scene-To-Page-Panel` (rubric này tiêu thụ output của Director, không thay thế nó).
- [ ] KHÔNG cung cấp UI cho người dùng tự chỉnh diện tích panel — đó là template layout / swap panel thuộc Epic-Minimum-Editor.

## 5. Ước lượng

| Đại lượng | Giá trị | Ghi chú |
|---|---|---|
| `E_build` | **~10 giờ-người** `[EM]` | Dưới trần 16h — bảng tra rời rạc + quota là logic có kích thước hữu hạn, không phụ thuộc mô hình ML. |
| `E_hitl` | **0 giờ-người/chapter** | Không tạo human gate; rubric chạy tự động trong Director. |

## 6. INVEST

- **I (Independent)**: ✅ Có thể ship và đo độc lập với `Story-Enforce-Max-Three-Characters-Per-Panel` và `Story-Text-Safe-Zone-In-Panel-Spec` — cả ba cùng mở rộng schema Comic IR nhưng không phụ thuộc lẫn nhau về logic.
- **S (Small)**: ✅ Bảng tra + quota là logic đóng gói được trong phạm vi ≤16 giờ-người, không lan sang các thành phần khác.

---

_Created by product-owner_
_Author: trisjr_
