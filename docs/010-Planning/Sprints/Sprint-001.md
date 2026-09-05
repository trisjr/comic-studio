---
id: SPRINT-001
type: sprint
status: draft
project: comic-studio
owner: "@trisjr"
tags: [mvp1, sprint, multi-tenancy, rls, ci]
linked-to: "../Implementation-Plans/Plan-MVP1-Story-Intelligence.md"
created: 2026-09-05
updated: 2026-09-05
---

# Sprint 001 — Nền tenancy ⛔ không retrofit được

| | |
|---|---|
| **Thời gian** | `05/10/2026` – `16/10/2026` (2 tuần) |
| **Capacity** | 60h · **Kỹ thuật 46h** + `O4` 7h = **53h** |
| **Mốc** | MVP1 — [Plan §7.3](../Implementation-Plans/Plan-MVP1-Story-Intelligence.md#73-lịch-sprint) |
| **Exit criteria trả** | ⭐ `M1-1` |
| **OKR phục vụ** | `O1` / `KR1.1` |

## Mục lục

1. [Mục tiêu sprint](#1-mục-tiêu-sprint)
2. [Story](#2-story)
3. [Thứ tự làm & vì sao](#3-thứ-tự-làm--vì-sao)
4. [Definition of Done](#4-definition-of-done)
5. [Rủi ro sprint này](#5-rủi-ro-sprint-này)
6. [Retro checklist](#6-retro-checklist)
7. [Tài liệu tham khảo](#7-tài-liệu-tham-khảo)

---

## 1. Mục tiêu sprint

> ⭐ **Mọi bảng nghiệp vụ sinh ra từ sprint này trở đi đã đúng ngay từ dòng `CREATE TABLE` đầu tiên.**

Đây là sprint có **cửa sổ cơ hội hẹp nhất của cả MVP1**. Migration `0001` cố ý ⛔ chưa tạo một bảng nghiệp vụ nào, nghĩa là `tenant_id` có thể được cài **trước khi tồn tại một dòng dữ liệu thật**. `KC-5` nói thẳng: retrofit vào schema **đã có dữ liệu** là *"migration đắt nhất tồn tại, và ⛔ **không có cách nào xác minh đã sửa hết**"*.

⇒ Cửa sổ này ⛔ **không quay lại**. Đó là lý do `E-01` nằm ở sprint 1 chứ ⛔ không phải sprint 3.

---

## 2. Story

| Mã | Story | `E_build` | AC chính |
|---|---|--:|---|
| `E-02` | [Tenant-User-Membership-As-Three-Entities](../../022-User-Stories/Backlog/Story-Tenant-User-Membership-As-Three-Entities.md) | 8h | Ba entity riêng kể cả khi quan hệ là 1:1 |
| `E-01` | [Tenant-Id-And-RLS-Everywhere](../../022-User-Stories/Backlog/Story-Tenant-Id-And-RLS-Everywhere.md) | 24h | ⭐ Test rò rỉ chéo tenant PASS |
| `E-05` | [Modular-Monolith-Three-Schemas](../../022-User-Stories/Backlog/Story-Modular-Monolith-Three-Schemas.md) — phần còn lại | 6h | Ba schema trong **một** database, boundary được cưỡng chế |
| `NEW-01` | ⚠️ **CI pipeline** — ⛔ **chưa có story, phải viết trước khi làm** | 8h | `lint` + `typecheck` + invariant test chạy trên PostgreSQL thật, mỗi commit |
| | **Cộng kỹ thuật** | **46h** | |
| | `O4` — 2 post + 1 cuộc trò chuyện tác giả | 7h | `KR4.1`, `KR4.3` |

---

## 3. Thứ tự làm & vì sao

| # | Việc | Vì sao ở vị trí này |
|:-:|---|---|
| 1 | `NEW-01` **CI trước tiên** | `KR1.1` và `KR1.2` đo *"**mỗi commit** trong CI"*. Dựng CI sau nghĩa là mọi commit của chính sprint này ⛔ không được đo. Với **1 dev ⛔ không code review** (`C1`), CI là lớp kiểm tra **duy nhất** |
| 2 | `E-05` hoàn tất boundary | Ba schema đã tồn tại từ `0001`; phần còn lại là cưỡng chế boundary giữa module. Phải xong **trước** khi bảng đầu tiên ra đời, nếu ⛔ không thì bảng đặt sai schema |
| 3 | `E-02` ba entity | `E-01` **tiêu thụ** cột `tenant_id` mà `E-02` cung cấp. Làm ngược thì `E-01` ⛔ không có gì để trỏ FK về |
| 4 | `E-01` `tenant_id` + RLS | Việc lớn nhất sprint. Đặt cuối để mọi bảng nó chạm đều đã ở đúng schema |

---

## 4. Definition of Done

### ⭐ DoD nhị phân — ⛔ không thương lượng

> [!CAUTION]
> `M1-1` được nghiệm thu bằng ⭐ **test rò rỉ chéo tenant PASS**, ⛔ **KHÔNG** bằng *"đã thêm `tenant_id` cho N/M bảng"*. Đếm bảng là chỉ số **có thể tăng trong khi kết quả vẫn là thất bại** — `tenant_id` trên 8/10 bảng = **vẫn rò rỉ**.

- [ ] Seed 2 tenant A và B có dữ liệu; **mọi** query chạy dưới session tenant A trả về ⭐ **`0` row** thuộc tenant B
- [ ] `tenant_id NOT NULL` trên **100%** bảng nghiệp vụ của cả ba schema — đo bằng script liệt kê bảng và kiểm ràng buộc; **`0`** bảng thiếu
- [ ] `tenant_id` là **cột đầu tiên** của **mọi** composite index — đo bằng truy vấn `pg_index` + `pg_attribute`; **`0`** index sai thứ tự
- [ ] RLS bật (`ROW LEVEL SECURITY` + ≥1 `CREATE POLICY`) trên **100%** bảng có `tenant_id` — số bảng trong `pg_policies` **bằng đúng** số bảng có cột `tenant_id`

### Đường ⛔ không hạnh phúc

- [ ] Insert row nghiệp vụ thiếu `tenant_id` bị **DB từ chối ở tầng constraint** — ⛔ không phải bị chặn bởi validation tầng ứng dụng
- [ ] Session ⛔ chưa set `app.current_tenant`, hoặc set giá trị ⛔ không hợp lệ ⇒ trả về ⭐ **`0` row**, ⛔ **không** ném exception (fail-closed, theo `ADR-006 D2`)
- [ ] Hai request từ hai tenant khác nhau tái dùng **cùng một connection trong pool** ⛔ không làm rò rỉ `app.current_tenant` sang request kia — test tải N request xen kẽ

### Hạ tầng

- [ ] Ba entity `tenant` / `user` / `membership` tồn tại **riêng biệt**, kể cả khi quan hệ hiện tại là 1:1
- [ ] Ba schema `story` / `comic` / `generation` nằm trong **một** database; boundary giữa module được cưỡng chế bằng lint rule hoặc test, ⛔ không bằng quy ước
- [ ] CI chạy `lint` + `typecheck` + toàn bộ invariant test trên **PostgreSQL thật** ở mỗi push, và **fail build** khi test đỏ
- [ ] `NEW-01` đã được viết thành story trong `Backlog/` **trước khi** code — có AC và có DoD

---

## 5. Rủi ro sprint này

| Rủi ro | Tín hiệu sớm | Xử lý |
|---|---|---|
| ⭐ `E-01` vượt 24h mà test rò rỉ ⛔ chưa PASS | Hết tuần 1 mà RLS mới bật trên một phần bảng | ⛔ **Không** giảm phạm vi — `KC-5` cấm. Mượn giờ từ `O4` của sprint này, bù lại ở S2 |
| RLS ⛔ không bảo vệ join thực hiện phía application | Thấy code join dữ liệu hai tenant ở tầng service | Glossary ghi rõ giới hạn này. Kiểm bằng đọc code, ⛔ không kỳ vọng RLS bắt hộ |
| Rò rỉ `app.current_tenant` qua connection pool | Test tải xen kẽ hai tenant fail không ổn định | Đây là AC bắt buộc, ⛔ không phải "nice to have" — bug loại này ⛔ không tái hiện đều nên dễ bị bỏ qua |
| CI ⛔ không dựng được PostgreSQL service container | Invariant test đỏ trên CI nhưng xanh ở máy | Invariant test **đã** cần Postgres thật — đây là ràng buộc đã biết, ⛔ không phải phát hiện mới |

---

## 6. Retro checklist

- [ ] Tính `burn_tích_luỹ` = giờ thực / **53h**. Ghi số vào retro
- [ ] `burn_tích_luỹ` > **105%** ⇒ ⭐ **kích van #2** ngay tại retro ([Plan §6.2](../Implementation-Plans/Plan-MVP1-Story-Intelligence.md#62-danh-sách-van-theo-thứ-tự-kích))
- [ ] `E-01` có vượt ước lượng ⛔ không? Nếu >30% ⇒ ước lượng lại **cả 7 story `[EM]`** (`P-R2`)
- [ ] `NEW-01` mất bao nhiêu giờ thật? Đây là ước lượng PM đầu tiên được kiểm chứng ⇒ hiệu chỉnh `NEW-02`, `NEW-03` theo tỉ lệ lệch
- [ ] `M1-1` đã PASS chưa? Nếu chưa, **⛔ không mở Sprint 002** — mọi bảng của S2 sẽ kế thừa lỗi

---

## 7. Tài liệu tham khảo

- [Plan-MVP1-Story-Intelligence.md](../Implementation-Plans/Plan-MVP1-Story-Intelligence.md) — kế hoạch master
- [WBS-MVP1.md](../Estimates/WBS-MVP1.md) — nguồn giờ
- [MVP-Scope §6](../MVP-Scope.md#6-không-được-cắt--danh-sách-cứng) — `KC-5`
- [ADR-006](../../030-Specs/Architecture/ADR-006-RLS-Tenant-Context-Injection.md) · [ADR-009](../../030-Specs/Architecture/ADR-009-Modular-Monolith-Three-Schemas.md) · [ADR-010](../../030-Specs/Architecture/ADR-010-Tenant-Isolation-With-RLS.md)
- [Spec-Security-Tenant-Isolation](../../030-Specs/Security/Spec-Security-Tenant-Isolation.md)
- [`apps/backend/db/migrations/0001_foundation.sql`](../../../apps/backend/db/migrations/0001_foundation.sql) — nền hiện có

---

_Created by product-manager_
_Author: trisjr_
