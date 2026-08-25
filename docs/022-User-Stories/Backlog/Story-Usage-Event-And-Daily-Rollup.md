---
id: STORY-F-01
type: story
status: draft
created: 2026-08-24
---

# Story-Usage-Event-And-Daily-Rollup

## 1. Story

Là Founder (operator), tôi muốn mọi lần tiêu tài nguyên được ghi append-only và rollup theo ngày, với regen ratio là metric first-class, để không định giá trong bóng tối hàng tháng

## 2. Part of

- Epic cha: [Epic-Credit-And-Unit-Economics](../Epics/Epic-Credit-And-Unit-Economics.md)
- BRD: [BRD-006-Credit-And-Unit-Economics](../../020-Requirements/BRD/BRD-006-Credit-And-Unit-Economics.md)
- Use Case liên quan: [UC-06-Generate-Panel-And-Pick-Variant](../../020-Requirements/Use-Cases/UC-06-Generate-Panel-And-Pick-Variant.md) — nơi best-of-N (N=3) thật sự tiêu tài nguyên, tức nơi `usage_event` được phát sinh (Epic cha mục 6.2)

## 3. Bối cảnh & nguồn

- [MVP-Scope §3](../../010-Planning/MVP-Scope.md#3-bảng-mvp-vs-full-scope) hạng mục **F1**: *"`usage_event` append-only + rollup `usage_daily` (regen ratio là metric first-class)"* — `🟡 log tay` tại MVP0 → `✅` từ MVP1 tới Full Scope. Anchor gốc: CF-8.6 · `findings/architect.md` B4.3 — *"đo muộn nghĩa là định giá trong bóng tối hàng tháng"*.
- [Roadmap §2](../../010-Planning/Roadmap.md#2-bảng-lộ-trình-tổng) mốc **MVP1**, exit criterion **M1-7**: *"`usage_daily` có p50/p90 regen ratio ⇒ [G2](../../010-Planning/MVP-Scope.md#73-g2--gate-kinh-tế-sau-mvp1) chạy được"*. Đây là **đầu vào bắt buộc** của tiêu chí **G2-a** ([MVP-Scope §7.3](../../010-Planning/MVP-Scope.md#73-g2--gate-kinh-tế-sau-mvp1)): *"Regen ratio p50 và p90 có giá trị thực đo từ `usage_daily`, trên ≥1 chapter hoàn chỉnh... Không có dữ liệu ⇒ G2 không chạy được, không phải 'tạm PASS'"*. [Roadmap §6.2](../../010-Planning/Roadmap.md#62-bảng-phụ-thuộc) xếp hàng này là phụ thuộc **CỨNG** của G2.
- [Glossary.md](../../999-Resources/Glossary.md) mục `usage_event`: *"Bảng append-only ghi mọi lần tiêu tài nguyên. Append-only là điều kiện để nó dùng được làm căn cứ đối soát."*
- [Charter §7](../../010-Planning/Charter-Comic-Studio.md#7-ràng-buộc-constraints) **C8** `[OFF]` CF-3.1/3.2: **N = 3 là mặc định cho MỌI panel** (best-of-N), **KHÔNG** phải retry-on-failure — mỗi panel sinh ra đúng 3 lần tiêu tài nguyên, không phải 1.

## 4. Acceptance Criteria

### Xác minh được

- [ ] Bảng `usage_event` chỉ hỗ trợ INSERT, không có đường code hay quyền DB nào cho phép UPDATE/DELETE một row đã ghi — đo bằng: thử UPDATE/DELETE trực tiếp một `usage_event` đã tồn tại, bị từ chối ở tầng DB (permission/constraint), không có row nào bị sửa hay biến mất
- [ ] Một lần sinh panel bằng best-of-N (N=3) tạo ra đúng **3** `usage_event` row, mỗi row ứng với 1 candidate — đo bằng: trigger sinh 1 panel, query `COUNT(*)` `usage_event` của panel đó = 3
- [ ] `usage_daily` rollup mỗi ngày cho ra **p50 và p90** của regen ratio, tính từ `usage_event` của đúng ngày đó — đo bằng: chạy rollup cho 1 ngày có ≥1 chapter hoàn chỉnh, query `usage_daily` trả về giá trị p50 và p90 khác NULL
- [ ] Dữ liệu `usage_daily` của MVP1 đủ để chạy tiêu chí **G2-a** ([MVP-Scope §7.3](../../010-Planning/MVP-Scope.md#73-g2--gate-kinh-tế-sau-mvp1)) — đo bằng: query `usage_daily` trên ≥1 chapter hoàn chỉnh trả về **cả** p50 **và** p90 có giá trị số, thoả trực tiếp điều kiện "có dữ liệu để tính" của G2-a

### Đường không hạnh phúc (unhappy path)

- [ ] Rollup job của một ngày bị crash giữa chừng (worker chết) — ngày đó được đánh dấu rõ là **"rollup thiếu/lỗi"**, KHÔNG được hiển thị ngầm định là regen ratio = 0 — đo bằng: kill rollup job giữa chừng, query `usage_daily` của ngày đó trả về trạng thái lỗi tường minh, không trả về 0
- [ ] Cùng một `usage_event` bị gửi/ghi 2 lần do retry ở tầng gọi (network timeout, worker retry) — rollup không đếm trùng — đo bằng: gửi 2 lần cùng một sự kiện có idempotency key giống nhau, `usage_daily` chỉ tính 1 lần
- [ ] VLM-select thất bại/timeout **sau khi cả 3 candidate đã sinh** (tài nguyên đã tiêu) — `usage_event` của cả 3 candidate vẫn được ghi trước khi biết kết quả select, không bị bỏ sót vì lý do "candidate không được chọn" — đo bằng: giả lập VLM-select timeout, query `usage_event` vẫn có đủ 3 row cho panel đó

### Ràng buộc cứng không được vi phạm

- `C8` ([Charter §7](../../010-Planning/Charter-Comic-Studio.md#7-ràng-buộc-constraints)): N=3 là mặc định cho MỌI panel, KHÔNG phải retry-on-failure — `usage_event` phải phản ánh đúng 3 lần tiêu tài nguyên trên mỗi panel, không được gộp 3 candidate thành 1 sự kiện hay chỉ ghi sự kiện khi có lỗi

### Story này KHÔNG làm

- Không ghi `cost_usd` / `model_id` / `model_version` / `attempt_no` trên `generation` — đó là `Story-Generation-Cost-And-Model-Metadata` (F2), Story khác trong cùng Epic
- Không implement credit ledger, HOLD, hay hold reaper — đó là `Story-Credit-Ledger-With-Hold-Before-Enqueue` (F3, MVP3, ngoài horizon)
- Không tính hay công bố gross margin, không tự chạy/kết luận gate G2 — Story chỉ cung cấp **dữ liệu đầu vào** (p50/p90); quyết định PASS/FAIL/KHÔNG CHẠY ĐƯỢC của G2 thuộc Founder tại đúng thời điểm gate ([MVP-Scope §7.3](../../010-Planning/MVP-Scope.md#73-g2--gate-kinh-tế-sau-mvp1))
- Không có UI hiển thị usage cho end-user — không có yêu cầu này trong nguồn tại horizon này

## 5. Ước lượng

| Đại lượng | Giá trị | Ghi chú |
|---|---|---|
| `E_build` | ~12 giờ-người `[EM]` | Bảng append-only + cơ chế chặn UPDATE/DELETE + job rollup theo ngày + tính p50/p90. Trong trần 16h — không có breakdown nguồn, ước lượng riêng của writer |
| `E_hitl` | 0 | Không tạo HITL gate; ghi log và rollup là tự động, không cần người xác nhận mỗi chapter |

## 6. INVEST

- **I (Independent)**: ✅ — theo bảng [`findings/business-analyst.md` §4.6](../../010-Planning/pm-runs/2026-08-24-khoi-tao-requirements-stories-comic-studio/findings/business-analyst.md#46-epic-credit-and-unit-economics-brd-006--3-trong-1-có-điều-kiện--3-ngoài). Độc lập về deliverable: bảng `usage_event` + rollup không chờ Story nào khác trong Epic-F để tự hoàn thành (F2 chỉ bổ sung thêm cột vào `generation`, không đổi cấu trúc `usage_event`).
- **S (Small)**: ✅ — theo cùng bảng nguồn. Phạm vi hẹp: một bảng append-only + một job rollup theo ngày, nằm gọn trong trần `E_build ≤ 16h`.

---

_Created by product-owner_
_Author: trisjr_
