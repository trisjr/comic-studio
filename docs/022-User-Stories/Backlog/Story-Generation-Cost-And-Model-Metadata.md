---
id: STORY-F-02
type: story
status: draft
created: 2026-08-24
---

# Story-Generation-Cost-And-Model-Metadata

## 1. Story

Là Founder (operator), tôi muốn mọi `generation` mang `cost_usd` + `model_id` + `model_version` + `attempt_no`, để tính được COGS thực và phát hiện được silent model drift

## 2. Part of

- Epic cha: [Epic-Credit-And-Unit-Economics](../Epics/Epic-Credit-And-Unit-Economics.md)
- BRD: [BRD-006-Credit-And-Unit-Economics](../../020-Requirements/BRD/BRD-006-Credit-And-Unit-Economics.md)
- Use Case liên quan: [UC-06-Generate-Panel-And-Pick-Variant](../../020-Requirements/Use-Cases/UC-06-Generate-Panel-And-Pick-Variant.md) — nơi mỗi `generation` row được tạo ra và mang chi phí/metadata thực của lần gọi provider đó

## 3. Bối cảnh & nguồn

- [MVP-Scope §3](../../010-Planning/MVP-Scope.md#3-bảng-mvp-vs-full-scope) hạng mục **F2**: *"`cost_usd` + `model_id` + `model_version` + `attempt_no` trên mọi `generation`"* — `🟡 CSV` tại MVP0 → `✅` từ MVP1 tới Full Scope. Anchor gốc: Analysis §5.7 #3 — **không backfill được**.
- [Roadmap §2](../../010-Planning/Roadmap.md#2-bảng-lộ-trình-tổng) **không có exit criterion `M1-x` riêng đặt tên cho F2** — khoảng trống này được ghi ra thay vì bịa số. Anchor Roadmap dùng ở đây là **mốc-level Deliverable của MVP1** (cột *Deliverable*, hàng MVP1: *"Monolith chạy được... `usage_event` + `usage_daily`"*) làm phạm vi mốc, **cộng với** liên kết trực tiếp tới tiêu chí **G2-b** và **G2-c** ([MVP-Scope §7.3](../../010-Planning/MVP-Scope.md#73-g2--gate-kinh-tế-sau-mvp1)): *"Gross margin tính từ COGS thực đo... COGS lấy từ tổng `generation.cost_usd` thực, **không** từ ước lượng"*. Không có 4 trường này, G2-b/G2-c **không có cách nào chạy bằng số thực**.
- Epic cha [mục 2](../Epics/Epic-Credit-And-Unit-Economics.md#2-mục-tiêu-epic) hàng 2: *"Hai Story `MVP1` (`F1`, `F2`) là **dữ liệu KHÔNG BACKFILL ĐƯỢC**. Thiếu `cost_usd`/`model_id`/`model_version`/`attempt_no` từ đầu ⇒ COGS phải **ước lượng lại vĩnh viễn**"*.
- [Charter §7](../../010-Planning/Charter-Comic-Studio.md#7-ràng-buộc-constraints) **C7** `[EM tính từ OFF]` CF-3.5: chi phí sàn **$12,06/chapter @N=3** — **cấm dùng như chi phí thực tế** trong bất kỳ tính toán margin nào mà không nêu nó là sàn. Đây chính xác là loại sai số mà `cost_usd` thực đo (Story này) phải thay thế.

## 4. Acceptance Criteria

### Xác minh được

- [ ] Mọi `generation` row (từ thời điểm Story này triển khai trở đi) có đủ 4 trường `cost_usd`, `model_id`, `model_version`, `attempt_no` không NULL — đo bằng: query 100% `generation` row phát sinh sau mốc triển khai, 0 row nào thiếu bất kỳ trường nào trong 4 trường
- [ ] `cost_usd` được ghi bằng giá trị **thực đo** tại thời điểm generation hoàn tất, không phải ước lượng trước khi gọi — đo bằng: so sánh giá trị `cost_usd` lưu với response cost/usage thực tế của provider call tương ứng, khớp
- [ ] `model_version` thay đổi giữa hai lần gọi liên tiếp cùng `model_id` (silent model drift từ phía provider) được ghi nhận riêng biệt, không bị ghi đè — đo bằng: giả lập 2 lần gọi cùng `model_id` nhưng provider trả `model_version` khác nhau, query trả về đúng 2 giá trị `model_version` phân biệt trên 2 `generation` row tương ứng
- [ ] `attempt_no` tăng dần đúng theo số lần gọi lại trong cùng một logical generation request — đo bằng: giả lập 1 request bị retry 2 lần, 3 `generation` row tương ứng có `attempt_no` lần lượt là 1, 2, 3

### Đường không hạnh phúc (unhappy path)

- [ ] Provider trả lỗi/timeout **trước khi** trả về cost thực — `generation` row vẫn được tạo ra và đánh dấu `cost_usd` ở trạng thái rõ ràng là chưa biết (không phải NULL âm thầm, không phải 0 ngầm định), KHÔNG bị bỏ sót hoàn toàn khỏi hệ thống — đo bằng: giả lập timeout, `generation` row tồn tại và có nhãn trạng thái cost tường minh
- [ ] Provider tự động fallback sang một model khác giữa lúc request đang chạy — `model_id` ghi lại đúng model **thực sự được gọi**, không phải model dự kiến ban đầu — đo bằng: giả lập fallback, `generation.model_id` khớp với model thực tế xuất hiện trong log của provider call
- [ ] Hai `generation` record cho cùng một candidate bị tạo trùng do lỗi client-side (double submit) — tổng `cost_usd` dùng để tính COGS không được cộng dồn 2 lần cho cùng một lần tiêu tài nguyên thực tế — đo bằng: gửi trùng, tổng `cost_usd` tính vào COGS chỉ tính đúng 1 lần chi phí thực đã phát sinh

### Ràng buộc cứng không được vi phạm

- `C8` ([Charter §7](../../010-Planning/Charter-Comic-Studio.md#7-ràng-buộc-constraints)): N=3 là mặc định cho MỌI panel — mỗi candidate trong 3 candidate của best-of-N phải có `generation` row + `cost_usd` + `attempt_no` **riêng của chính nó**, không được gộp chi phí của 3 candidate vào 1 row duy nhất

### Story này KHÔNG làm

- Không tính hay hiển thị gross margin / kết luận gate G2 — đó là hoạt động của Founder tại gate ([MVP-Scope §7.3](../../010-Planning/MVP-Scope.md#73-g2--gate-kinh-tế-sau-mvp1)), Story này chỉ đảm bảo `cost_usd` thực đo tồn tại để phép tính đó dùng được
- Không backfill dữ liệu cho `generation` đã tạo **trước** khi Story này chạy — đúng bản chất "không backfill được" của F2; `generation` cũ thiếu 4 trường này giữ nguyên trạng thái thiếu, không giả lập số liệu hồi tố
- Không implement `usage_event` / rollup `usage_daily` — đó là `Story-Usage-Event-And-Daily-Rollup` (F1), Story khác trong cùng Epic
- Không xây cơ chế cảnh báo tự động (alerting) khi phát hiện model drift — Story chỉ đảm bảo dữ liệu được ghi đủ để phát hiện được bằng query/thủ công, không xây hệ thống alert

## 5. Ước lượng

| Đại lượng | Giá trị | Ghi chú |
|---|---|---|
| `E_build` | ~10 giờ-người `[EM]` | Thêm 4 cột vào `generation` + logic ghi giá trị thực tại thời điểm mỗi candidate call hoàn tất/thất bại. Trong trần 16h — không có breakdown nguồn, ước lượng riêng của writer |
| `E_hitl` | 0 | Ghi metadata là tự động theo mỗi lần gọi provider, không tạo nghĩa vụ giờ-người lặp lại theo chapter |

## 6. INVEST

- **I (Independent)**: ✅ — theo bảng [`findings/business-analyst.md` §4.6](../../010-Planning/pm-runs/2026-08-24-khoi-tao-requirements-stories-comic-studio/findings/business-analyst.md#46-epic-credit-and-unit-economics-brd-006--3-trong-1-có-điều-kiện--3-ngoài). Story này chỉ thêm cột vào `generation` đã tồn tại (từ pipeline sinh ảnh của Epic-A) — không chờ `Story-Usage-Event-And-Daily-Rollup` (F1) để tự hoàn thành, dù cả hai cùng phục vụ gate G2.
- **S (Small)**: ✅ — theo cùng bảng nguồn. Phạm vi hẹp: 4 cột + logic ghi tại thời điểm gọi provider, nằm gọn trong trần `E_build ≤ 16h`.

---

_Created by product-owner_
_Author: trisjr_
