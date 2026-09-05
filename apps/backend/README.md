# Backend — `apps/backend`

> Modular monolith của comic-studio. Một image, hai process type, một PostgreSQL.
>
> Tài liệu này mô tả **cách chạy** và **vì sao cấu trúc có hình dạng này**. Nó ⛔ không định nghĩa lại quyết định kiến trúc — mọi ràng buộc đều neo về ADR tương ứng ở [`docs/030-Specs/Architecture/`](../../docs/030-Specs/Architecture/).

## Mục lục

1. [Chạy lần đầu](#1-chạy-lần-đầu)
2. [Bốn lệnh của một image](#2-bốn-lệnh-của-một-image)
3. [Cấu trúc thư mục và vì sao](#3-cấu-trúc-thư-mục-và-vì-sao)
4. [Guardrail nào được cưỡng chế bằng gì](#4-guardrail-nào-được-cưỡng-chế-bằng-gì)
5. [Cái gì CỐ Ý chưa có](#5-cái-gì-cố-ý-chưa-có)
6. [Tài liệu tham khảo](#6-tài-liệu-tham-khảo)

---

## 1. Chạy lần đầu

```bash
cp .env.example .env          # rồi điền ba DB_APP_*_PASSWORD
pnpm install
pnpm db:up                    # postgres + minio qua docker compose
pnpm backend db:bootstrap     # tạo ba DB role từ biến môi trường
pnpm backend migrate          # chạy migration dưới role owner
pnpm backend test             # 9 invariant, chạy trên PostgreSQL thật
pnpm backend dev              # process api tại http://localhost:3000/health
```

> [!IMPORTANT]
> **`db:bootstrap` phải chạy TRƯỚC `migrate`.** Migration `0001` cấp quyền cho ba role `app_api` / `app_worker` / `app_public_intake`, nên ba role đó phải tồn tại trước. Thứ tự ngược lại làm migration lỗi ngay dòng `GRANT`.

⚠️ **`pnpm db:up` là stack của DEV và CI, ⛔ không phải hình triển khai production.** [ADR-002](../../docs/030-Specs/Architecture/ADR-002-Hosting-Platform-And-Region.md) CHỐT #4 đòi PostgreSQL **managed** có PITR và một đường restore đã diễn tập, và chính ADR đó đã **bác** phương án *"VPS + Docker Compose"* cho production.

## 2. Bốn lệnh của một image

[ADR-001](../../docs/030-Specs/Architecture/ADR-001-Backend-And-Frontend-Tech-Stack.md) CHỐT #2: `apps/backend` build ra **đúng một** image; mọi vai trò là một `argv[2]` khác nhau trên cùng image digest đó.

| Lệnh | Vai trò | DB role |
|---|---|---|
| `node dist/main.js api` | Process HTTP. ⛔ Không chứa vòng lặp worker, ⛔ không scheduler trong process | `app_api` |
| `node dist/main.js worker` | Process xử lý job, ⛔ không mở cổng nào | `app_worker` |
| `node dist/main.js migrate` | Chạy migration SQL thô | owner |
| `node dist/main.js db:bootstrap` | Tạo/cập nhật ba DB role ứng dụng | owner |

⭐ **Job theo đồng hồ chỉ được GỌI một trong bốn lệnh trên** ([ADR-002](../../docs/030-Specs/Architecture/ADR-002-Hosting-Platform-And-Region.md) điều 3). ⛔ Không một dòng logic nghiệp vụ nào được sống trong cấu hình cron của platform — cron của vendor là *trigger*, ⛔ không phải *code*.

## 3. Cấu trúc thư mục và vì sao

```
apps/backend/
├── db/migrations/          ⭐ NGUỒN SỰ THẬT của schema — SQL thô, append-only
├── src/
│   ├── main.ts             dispatcher: api | worker | migrate | db:bootstrap
│   ├── entrypoints/        mỗi lệnh một file, dùng chung một đồ thị DI
│   ├── modules/            ba module nghiệp vụ ↔ ba schema Postgres
│   │   ├── story/          M1 Ingest & Compliance · M2 Story Intelligence
│   │   ├── comic/          M3 Director · M4 Human Gates · M6 Typeset
│   │   └── generation/     M5 Generation Pipeline
│   ├── platform/           bảng nhóm platform ở schema `public` (ADR-005)
│   │   ├── tenancy/        khoá object storage, tenant context
│   │   └── health/         liveness của riêng process api
│   └── infra/              adapter hạ tầng, ⛔ không chứa logic nghiệp vụ
│       ├── config/         zod schema cho biến môi trường, fail-fast
│       ├── db/             pool theo role, transaction, migrator
│       ├── logging/        pino ra stdout, redact signed URL
│       └── storage/        port + adapter đúng tập con S3
└── test/invariants/        test chạy trên PostgreSQL thật, ⛔ không mock DB
```

### 3.1 Ba tầng, một chiều phụ thuộc

```
modules/  ──▶  platform/  ──▶  infra/
```

Chiều này **một hướng và được lint cưỡng chế**. Ngoại lệ duy nhất là job handler: module *đăng ký* handler vào registry của `platform/jobs` thay vì `platform` *import* module — đó là đảo chiều (inversion), ⛔ không phải import ngược.

### 3.2 Vì sao module là thư mục, ⛔ không phải workspace package

Mọi import xuyên module đi qua barrel `index.ts` của module đó. Khi nào cần tách thành package thật (ví dụ có consumer thứ hai), chỉ đổi alias — ⛔ không sửa một dòng `import` nào. Đây là *"mở rộng được"* mà ⛔ không phải trả trước chi phí của một vòng build cho mỗi module, thứ đắt với đội **1 người**.

### 3.3 ⚠️ Sổ migration nằm ở schema `ops`, ⛔ KHÔNG ở `public`

[ADR-005](../../docs/030-Specs/Architecture/ADR-005-Platform-Table-Schema-Placement.md) `G-2` định nghĩa `public` là **closed list** gồm đúng 12 bảng nghiệp vụ, và có test CI đối chiếu danh sách đó. Đặt `schema_migration` vào `public` sẽ làm test đó đỏ, hoặc buộc phải nới chính cái test là lý do nó tồn tại.

⚠️ **Cần Architect xác nhận**: schema `ops` là **quyết định của lần khởi tạo này**, ⛔ chưa có trong ADR nào. Nó chứa **đúng một** bảng hạ tầng và ⛔ không chứa dữ liệu nghiệp vụ.

## 4. Guardrail nào được cưỡng chế bằng gì

⭐ Theo `R-1` của [SDD §4](../../docs/030-Specs/Architecture/SDD-Comic-Studio.md): một ranh giới **⛔ không có cơ chế cưỡng chế** thì trong repo này coi như **⛔ không tồn tại**.

| Ràng buộc | Cưỡng chế bằng | Đã kiểm bằng cách |
|---|---|---|
| `B-1` — `comic` chỉ gọi `story` qua barrel | ESLint `no-restricted-imports` | Import sâu cố ý ⇒ lint **đỏ**; import qua barrel ⇒ **xanh** |
| `B-2` / `W-3` — chỉ `claim.ts` chạm `public.job` | ESLint `no-restricted-syntax` trên chuỗi SQL | Chuỗi chứa `public.job` ở file khác ⇒ lint **đỏ** |
| [ADR-006](../../docs/030-Specs/Architecture/ADR-006-RLS-Tenant-Context-Injection.md) `D5` — cấm `SET` mức session | ESLint `no-restricted-syntax` | `SET app.current_tenant` ⇒ lint **đỏ** |
| [ADR-001](../../docs/030-Specs/Architecture/ADR-001-Backend-And-Frontend-Tech-Stack.md) — cột `NUMERIC` ⛔ không ép sang `number` | ESLint chặn `parseFloat` + kiểu `DecimalString` có brand | `parseFloat` ⇒ lint **đỏ** |
| Chiều phụ thuộc ba tầng | ESLint `no-restricted-imports` | `platform` → `modules` và `infra` → `platform` ⇒ lint **đỏ** |
| [ADR-005](../../docs/030-Specs/Architecture/ADR-005-Platform-Table-Schema-Placement.md) `G-1` — ⛔ không tạo object ở `public` | `REVOKE CREATE` trong migration `0001` | `app_api` chạy `CREATE TABLE public.x` ⇒ **permission denied** |
| [ADR-005](../../docs/030-Specs/Architecture/ADR-005-Platform-Table-Schema-Placement.md) `G-3` — dùng tên đủ điều kiện | `search_path` rỗng đặt ở **tham số khởi động** kết nối | Đặt lúc mở kết nối, ⛔ không phải một câu `SET` chạy sau |
| AC *"fail-closed 0 row"* | `public.current_tenant_id()` có khối `EXCEPTION` | 5 test invariant trên PostgreSQL thật |
| Migration append-only | Checksum SHA-256 lưu trong `ops.schema_migration` | Sửa file đã chạy ⇒ migrator **dừng và báo** |

## 5. Cái gì CỐ Ý chưa có

⚠️ Những mục dưới đây **⛔ không phải thiếu sót** — chúng phụ thuộc một quyết định chưa đóng, và viết trước là **bịa ra quyết định đó**.

| Chưa có | Chặn bởi | Ai đóng |
|---|---|---|
| Mọi bảng nghiệp vụ, gồm `tenant` / `user` / `membership` | Policy RLS cho ba bảng định danh còn mở ([ADR-005](../../docs/030-Specs/Architecture/ADR-005-Platform-Table-Schema-Placement.md) `Q4`) | Architect, lô DB Schema |
| Bảng `public.job` + `claimJobAndBindTenant()` | `N` của `in_flight_per_tenant < N` là `TBD` (`T-6`) | PM + Architect, sau đo tải |
| Vòng lặp claim của worker | Cùng lý do trên. ⛔ Viết nửa vời sẽ tạo đúng khoảng hở mà [ADR-006](../../docs/030-Specs/Architecture/ADR-006-RLS-Tenant-Context-Injection.md) `W-3` tồn tại để đóng | — |
| `JwksGuard` + interceptor bơm tenant context | Spike verify vendor auth (`T-4`, tối đa 1 ngày) | Dev, kickoff MVP1 |
| DB role thứ năm `app_operator` | Thay đổi **mô hình quyền**, là nợ kỹ thuật đã ghi ở [SDD §7.4](../../docs/030-Specs/Architecture/SDD-Comic-Studio.md) | Architect |
| Compositor + sinh PDF 300 DPI | Thư viện shaping tiếng Việt chưa được đánh giá bằng số đo | Dev, sau spike |
| Con số TTL của signed URL | `TBD` có chủ đích ([ADR-004](../../docs/030-Specs/Architecture/ADR-004-Object-Storage-Vendor-And-Signed-URL.md)); hệ thống chạy đúng với **TTL bất kỳ** | Dev đề xuất, Founder duyệt |

## 6. Tài liệu tham khảo

- [ADR-001 — Tech stack backend và frontend](../../docs/030-Specs/Architecture/ADR-001-Backend-And-Frontend-Tech-Stack.md)
- [ADR-002 — Hosting platform và region](../../docs/030-Specs/Architecture/ADR-002-Hosting-Platform-And-Region.md)
- [ADR-004 — Object storage và signed URL](../../docs/030-Specs/Architecture/ADR-004-Object-Storage-Vendor-And-Signed-URL.md)
- [ADR-005 — Vị trí schema của bảng platform](../../docs/030-Specs/Architecture/ADR-005-Platform-Table-Schema-Placement.md)
- [ADR-006 — Bơm tenant context cho RLS](../../docs/030-Specs/Architecture/ADR-006-RLS-Tenant-Context-Injection.md)
- [ADR-009 — Modular monolith, ba schema](../../docs/030-Specs/Architecture/ADR-009-Modular-Monolith-Three-Schemas.md)
- [SDD — Bản thiết kế hệ thống](../../docs/030-Specs/Architecture/SDD-Comic-Studio.md)
- [Roadmap §3.2 — MVP1 Story Intelligence](../../docs/010-Planning/Roadmap.md)
