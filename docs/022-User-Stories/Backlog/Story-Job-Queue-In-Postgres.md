---
id: STORY-A-05
type: story
status: draft
created: 2026-08-24
---

# Story-Job-Queue-In-Postgres

## 1. Story

Là Founder (operator), tôi muốn enqueue job trong cùng transaction với dữ liệu nghiệp vụ, để không có job mồ côi và không cần thêm một hạ tầng queue.

## 2. Part of

- Epic cha: [Epic-Image-Generation-Pipeline](../Epics/Epic-Image-Generation-Pipeline.md)
- BRD: [BRD-001-Image-Generation-Pipeline](../../020-Requirements/BRD/BRD-001-Image-Generation-Pipeline.md)
- Use Case liên quan: [UC-06-Generate-Panel-And-Pick-Variant](../../020-Requirements/Use-Cases/UC-06-Generate-Panel-And-Pick-Variant.md) (job sinh panel được enqueue qua cơ chế này từ MVP1 trở đi)

## 3. Bối cảnh & nguồn

- `MVP-Scope §3` hạng mục **A5**: *"Job queue trong Postgres (`FOR UPDATE SKIP LOCKED`, transactional enqueue)"* — `❌` tại MVP0 (không cần, MVP0 không có DB) → `✅` tại MVP1. Anchor: Analysis §6.2 — *"MVP0 là script + file phẳng, không DB"*. CF-9.2: modular monolith 1 process / 1 PostgreSQL.
- `Roadmap §2` mốc **MVP1** (10/2026–12/2026): Deliverable của MVP1 là *"Monolith chạy được: ingest → text clean → extraction → timeline state → Story Bible editor. `tenant_id` + RLS. Provenance đầy đủ. HITL gate + eval kit. `usage_event` + `usage_daily`"*.
  ⚠️ **Job queue KHÔNG có exit criterion `M1-x` riêng trong `Roadmap §2`** — đúng như Epic cha (`Epic-Image-Generation-Pipeline.md` mục 5) đã ghi tường minh: *"Hạng mục này không có exit criterion `M-x` riêng trong Roadmap §2 — nó nằm ở cột Deliverable của mốc MVP1. Đừng gán cho nó một `M-number` mà nguồn không cấp."* Anchor Roadmap dùng ở đây là **mốc MVP1** (`Roadmap §2` hàng MVP1, cột Deliverable) làm exit-criterion-cấp-mốc, thay vì một `M1-x` cụ thể — ghi rõ khoảng trống này thay vì bịa số.
- CF-9.2: lý do kiến trúc — RLS không bảo vệ join phía ứng dụng; nghĩa vụ audit đòi một transaction boundary duy nhất; multi-tenancy đã ăn **15–25%** effort `[EM]`.

## 4. Acceptance Criteria

### Xác minh được

- [ ] Việc tạo job (enqueue) và việc ghi dữ liệu nghiệp vụ liên quan (ví dụ tạo `generation` row) commit trong **CÙNG MỘT** database transaction — đo bằng: test rollback transaction giữa chừng, xác nhận cả job lẫn dữ liệu nghiệp vụ đều **KHÔNG** tồn tại (all-or-nothing)
- [ ] Worker claim job bằng `SELECT ... FOR UPDATE SKIP LOCKED` — đo bằng: kiểm tra câu SQL claim job đúng cú pháp này
- [ ] Hai worker chạy đồng thời không bao giờ claim cùng một job — đo bằng: test chạy N worker song song trên M job, tổng số job được xử lý = M, không job nào bị xử lý 2 lần
- [ ] Không tồn tại job "mồ côi" (job có trong queue mà không có dữ liệu nghiệp vụ tương ứng, hoặc ngược lại) sau khi hệ thống chạy ổn định — đo bằng: query đối chiếu số job đã enqueue với số bản ghi nghiệp vụ tương ứng, phải khớp 100%

### Đường không hạnh phúc (unhappy path)

- [ ] Worker bị kill giữa lúc đang xử lý job đã claim ⇒ job **không** bị kẹt vĩnh viễn ở trạng thái "đang xử lý", một worker khác xử lý được — đo bằng: test kill process worker giữa chừng rồi khởi động worker mới, xác nhận job được xử lý tiếp
- [ ] Transaction enqueue job bị rollback do lỗi ở bước ghi dữ liệu nghiệp vụ ⇒ job **không** được tạo ra (không phát sinh job mồ côi từ trường hợp này)
- [ ] Nhiều job cùng tranh chấp một hàng khoá (lock contention cao) ⇒ `SKIP LOCKED` phải đảm bảo worker bỏ qua hàng đang bị khoá và lấy hàng khác, không bị block chờ vô hạn

### Ràng buộc cứng không được vi phạm

- `KC-4` (`MVP-Scope §6`): mọi `generation` do pipeline tạo ra phải commit cùng transaction với `change_log` + `usage_event` — job queue là cơ chế enqueue cho các generation này, transaction boundary của job phải tương thích với `KC-4` (`Epic-Image-Generation-Pipeline.md` mục 5 ghi rõ Epic-A *"là nơi nó bị vi phạm dễ nhất"*).

### Story này KHÔNG làm

- Không triển khai fairness per tenant trong câu CLAIM job — đó là `Story-Fairness-Per-Tenant-Job-Claim` (MVP3, ngoài horizon)
- Không dùng hạ tầng message queue riêng (Redis, RabbitMQ, SQS...) — chủ ý dùng Postgres để giữ modular monolith 1 DB (CF-9.2)
- Không triển khai worker như process riêng biệt (2 entrypoint) — đó là hạng mục E7 (`Epic-Multi-Tenancy-And-Platform`), ngoài phạm vi Story này
- Không định nghĩa credit ledger / hold reserve cho job — đó thuộc `Story-Credit-Ledger-With-Hold-Before-Enqueue` (`Epic-Credit-And-Unit-Economics`)

## 5. Ước lượng

| Đại lượng | Giá trị | Ghi chú |
|---|---|---|
| `E_build` | ~12 giờ-người `[EM]` | Trong trần 16h. Không có breakdown nguồn, ước lượng riêng của writer |
| `E_hitl` | 0 | Job queue là hạ tầng thuần, không tạo nghĩa vụ giờ-người lặp lại theo chapter |

## 6. INVEST

`I`: ✅ — Job queue là hạ tầng độc lập về deliverable; các Story khác dùng nó nhưng không cần sửa Story này để tự hoàn thành.

`S`: ✅ — Phạm vi rõ: enqueue transactional + claim bằng `SKIP LOCKED`, không phụ thuộc hạng mục fairness (đã tách sang `Story-Fairness-Per-Tenant-Job-Claim` ở MVP3).

---

_Created by product-owner_
_Author: trisjr_
