---
id: STORY-A-04
type: story
status: draft
created: 2026-08-24
---

# Story-Image-Provider-Adapter

## 1. Story

Là Founder (operator), tôi muốn đổi image provider bằng cách thay adapter, để giá đầu vào của provider không khoá cứng sản phẩm.

## 2. Part of

- Epic cha: [Epic-Image-Generation-Pipeline](../Epics/Epic-Image-Generation-Pipeline.md)
- BRD: [BRD-001-Image-Generation-Pipeline](../../020-Requirements/BRD/BRD-001-Image-Generation-Pipeline.md)
- Use Case liên quan: [UC-06-Generate-Panel-And-Pick-Variant](../../020-Requirements/Use-Cases/UC-06-Generate-Panel-And-Pick-Variant.md) (adapter là điểm gọi model sinh ảnh trong luồng đó)

## 3. Bối cảnh & nguồn

- `MVP-Scope §3` hạng mục **A4**: *"Adapter đa provider (Gemini 3 Pro Image, FLUX.2)"* — `🟡 1 adapter` tại MVP0. Anchor: Analysis §6.2 seam #4. CF-3.4 `[OFF]`: Gemini 3 Pro Image **$0.134** standard / **$0.067** batch; FLUX.2 pro **$0.03**.
- `Roadmap` Pre-cycle 09/2026: MVP0 dùng đúng một adapter, chi phí **~$12** `[EM tính từ OFF]` (CF-3.11), số cao làm trần an toàn. Exit criterion **P-2** (gate `G1` cần số đo) — số đo đó chỉ đo được thông qua đúng một adapter cố định của Story này.

## 4. Acceptance Criteria

### Xác minh được

- [ ] Việc gọi provider sinh ảnh đi qua một interface/abstraction chung, không gọi thẳng SDK của provider từ code nghiệp vụ — đo bằng: kiểm tra code, mọi lời gọi provider nằm trong module adapter
- [ ] Đổi provider (ví dụ từ Gemini sang FLUX.2) chỉ cần thay implementation của adapter, không cần sửa code gọi compiler/queue/business logic — đo bằng: viết thử một adapter thứ hai (test/dummy) và xác nhận phần còn lại của hệ thống không đổi
- [ ] Adapter ghi lại `model_id` + `model_version` cho mỗi lần gọi — đo bằng: kiểm tra log/response có đủ hai trường này

### Đường không hạnh phúc (unhappy path)

- [ ] Provider trả lỗi (timeout, rate limit, content policy reject) ⇒ adapter phải phân loại lỗi và trả về cho caller một trạng thái rõ ràng, không để lỗi rơi tự do làm crash toàn bộ script
- [ ] Provider đổi giá hoặc đổi weights dưới cùng một tên model (silent model drift) ⇒ Story không tự phát hiện được (ngoài phạm vi MVP0), nhưng adapter phải ghi `model_version` để về sau có thể truy vết khi có nghi ngờ drift

### Ràng buộc cứng không được vi phạm

—

### Story này KHÔNG làm

- Không tự động chuyển đổi qua lại giữa nhiều provider trong cùng một lần chạy (multi-provider fallback) — MVP0 chỉ có 1 adapter cố định
- Không tối ưu chi phí bằng cách tự động chọn provider theo giá thấp nhất — đó là quyết định vận hành, không phải yêu cầu kỹ thuật của Story này
- Không xử lý billing/BYOK cho provider (thuộc Epic-Credit-And-Unit-Economics)

## 5. Ước lượng

| Đại lượng | Giá trị | Ghi chú |
|---|---|---|
| `E_build` | ~6 giờ-người `[EM]` | 1 adapter, trong trần 16h. Ước lượng riêng, không có breakdown nguồn |
| `E_hitl` | 0 | Không tạo nghĩa vụ giờ-người lặp lại |

## 6. INVEST

`I`: ✅ — Adapter là một module tách biệt, thay được độc lập với compiler/queue.

`S`: ✅ — Phạm vi rõ, 1 adapter duy nhất cho MVP0, không phụ thuộc Story khác để hoàn thành.

⚠️ Story này **mở ở MVP0 nhưng KHÔNG thuộc** danh sách 5 Story `[MVP0]` `n/a` của `findings/business-analyst.md` §4.9 — theo đúng ghi chú của Epic cha, Story này **vẫn được chấm INVEST bình thường** như trên.

---

_Created by product-owner_
_Author: trisjr_
