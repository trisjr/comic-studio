---
id: STORY-E-05
type: story
status: draft
created: 2026-08-24
---

# Story-Modular-Monolith-Three-Schemas

## 1. Story

Là **Founder (architect)**, tôi muốn **1 process, 1 PostgreSQL, 3 schema (`story`/`comic`/`generation`) với luật `comic` gọi `story` CHỈ qua `resolveState()` và `getBible()`**, để **giữ được một transaction boundary cho nghĩa vụ audit**

## 2. Part of

- Epic cha: [Epic-Multi-Tenancy-And-Platform](../Epics/Epic-Multi-Tenancy-And-Platform.md)
- BRD: [BRD-005-Multi-Tenancy-And-Platform](../../020-Requirements/BRD/BRD-005-Multi-Tenancy-And-Platform.md) — `BR-005-05`, `BR-005-06`, `BR-005-09`
- Use Case liên quan: Epic-E **không sở hữu UC riêng** ([BRD-005 §7.2](../../020-Requirements/BRD/BRD-005-Multi-Tenancy-And-Platform.md#72-use-case)) — module boundary là NFR/schema requirement, không phải một tương tác goal-level của actor. Story này là **điều kiện kỹ thuật nền** cho nghĩa vụ provenance mà [BRD-007-Legal-And-Compliance](../../020-Requirements/BRD/BRD-007-Legal-And-Compliance.md) sở hữu nội dung nghiệp vụ (`KC-4`).

## 3. Bối cảnh & nguồn

Đây là hàng **`E5`** của [MVP-Scope §3](../../010-Planning/MVP-Scope.md#3-bảng-mvp-vs-full-scope): *"Modular monolith: 1 process, 1 PostgreSQL, 3 schema (`story`/`comic`/`generation`)"* — `❌` ở MVP0 → `✅` từ **MVP1**. Căn cứ: CF-9.2 — lý do cắt microservices *"MẠNH LÊN dưới SaaS"*: (1) RLS không bảo vệ join phía ứng dụng, (2) nghĩa vụ audit đòi **một** transaction boundary, (3) multi-tenancy đã ăn **15–25%** effort `[EM]` CF-6.9 ([MVP-Scope §4.2](../../010-Planning/MVP-Scope.md#42-microservices--vector-db-12--cắt-cf-92)). Đây cũng là **seam #3** của [MVP-Scope §4.2](../../010-Planning/MVP-Scope.md#42-microservices--vector-db-12--cắt-cf-92): module boundary bằng package + interface, **không** HTTP nội bộ, với luật `comic` gọi `story` chỉ qua `resolveState()` và `getBible()`.

Exit criterion tương ứng là **`M1-5`** của [Roadmap §2](../../010-Planning/Roadmap.md#2-bảng-lộ-trình-tổng), mốc **MVP1**: *"5 hạng mục provenance ... và có **test chứng minh chúng commit CÙNG MỘT transaction** với artifact"* — điều kiện kỹ thuật để `M1-5` PASS được chính là 1 process/1 PostgreSQL mà Story này dựng lên (`KC-4` của [MVP-Scope §6](../../010-Planning/MVP-Scope.md#6-không-được-cắt--danh-sách-cứng): *"bằng chứng có thể thiếu ngẫu nhiên thì không phải bằng chứng"*).

## 4. Acceptance Criteria

### Xác minh được

- [ ] Database có đúng 3 schema Postgres `story`, `comic`, `generation` trong **cùng một** database — đo bằng: truy vấn `information_schema.schemata`, xác nhận đủ 3 tên schema tồn tại trong 1 database
- [ ] Toàn bộ codebase deploy như **1 process/1 deploy unit chính** (worker tách process riêng là hạng mục của Story khác, ngoài horizon) — đo bằng: kiểm tra cấu hình deploy chỉ có 1 entrypoint chính cho toàn bộ business logic tại thời điểm Story này chạy
- [ ] Lint rule chạy trong CI chặn mọi import trực tiếp từ module `comic` vào nội bộ module `story`, ngoại trừ đúng 2 hàm `resolveState()` và `getBible()` — đo bằng: thêm một import vi phạm vào một PR test, kỳ vọng CI **FAIL**
- [ ] `INSERT` vào bảng `generation` (schema `generation`) cùng `INSERT` vào `change_log` và `INSERT` vào `usage_event` chạy được trong **cùng một** transaction Postgres — đo bằng: test transaction rollback giữa chừng, xác nhận cả 3 insert đều biến mất, không có insert nào còn sót lại (điều kiện kỹ thuật cho `KC-4`)

### Đường không hạnh phúc (unhappy path)

- [ ] Một PR cố tình import nội bộ module `story` từ `comic` (không qua `resolveState`/`getBible`) bị CI chặn, không merge được — đo bằng: mở PR test trên nhánh riêng, kỳ vọng CI đỏ
- [ ] Nếu transaction giữa `generation`/`change_log`/`usage_event` fail ở bước cuối, không được để lại state một phần (partial commit) — đo bằng: inject lỗi ở bước insert thứ 3, kiểm tra 2 bước trước cũng bị rollback hoàn toàn

### Ràng buộc cứng không được vi phạm

- `KC-4` ([MVP-Scope §6](../../010-Planning/MVP-Scope.md#6-không-được-cắt--danh-sách-cứng)): Story này cung cấp **điều kiện kỹ thuật** (1 DB ⇒ 1 transaction boundary); nội dung nghĩa vụ audit thuộc [BRD-007-Legal-And-Compliance](../../020-Requirements/BRD/BRD-007-Legal-And-Compliance.md)

### Story này KHÔNG làm

- Không tách microservices, không tách database thứ hai, không dựng Vector DB riêng — `E6`, **cắt hẳn**, không có điều kiện mở lại trong `MVP-Scope`
- Không dựng HTTP nội bộ giữa các module — module boundary là package + interface, không phải network call
- Không tách worker thành process triển khai riêng — thuộc `Story-Worker-As-Separate-Process-Same-Codebase` (MVP3, ngoài horizon)
- Không định nghĩa nội dung nghiệp vụ của `change_log`/`field_provenance`/`generation.origin` — thuộc [Epic-Legal-And-Compliance](../Epics/Epic-Legal-And-Compliance.md), `KC-1`…`KC-3`

## 5. Ước lượng

| Đại lượng | Giá trị | Ghi chú |
|---|---|---|
| `E_build` | **~14h** `[EM]` | Trong trần 16h — thiết lập 3 schema trong 1 database, viết lint rule CI cưỡng chế ranh giới module, và viết test transaction 3-insert-cùng-commit |
| `E_hitl` | **0** | Story không tạo ra hoặc tiêu thụ HITL gate lặp lại theo chapter — đây là một quyết định kiến trúc/topology chạy một lần |

## 6. INVEST

⚠️ **Vỡ cả `I` và `S`** theo cờ tại [`findings/business-analyst.md` §4.5](../../010-Planning/pm-runs/2026-08-24-khoi-tao-requirements-stories-comic-studio/findings/business-analyst.md#45-epic-multi-tenancy-and-platform-brd-005--5-trong--2-ngoài), nhưng Story này **không có hàng chi tiết trong §4.10**. Lý do dưới đây là **`[Kiến trúc suy luận]`** — tự suy từ dữ liệu bảng, không phải trích nguyên văn từ nguồn:

> **`[Kiến trúc suy luận]`**: Quyết định "1 process, 1 PostgreSQL, 3 schema" là một quyết định kiến trúc **nền tảng, không chia nhỏ được theo schema mà vẫn giữ nguyên giá trị nó tồn tại để mang lại**. Dựng schema `story` trước rồi `comic`/`generation` sau (hoặc ngược lại) không kiểm chứng được **`KC-4`** — giá trị "một transaction boundary duy nhất" chỉ tồn tại khi cả 3 schema đã ở trong cùng 1 database VÀ lint rule ranh giới module đã được cưỡng chế trên toàn bộ codebase liên quan. Một triển khai từng phần (ví dụ: chỉ có schema `story`, chưa có `comic`) không chứng minh được gì về transaction boundary hay về ranh giới `comic → story`, tương tự cách `Story-Tenant-Id-And-RLS-Everywhere` không tách được theo bảng vì DoD là một thuộc tính toàn cục (`M1-5` cần cả 3 bảng `generation`/`change_log`/`usage_event` commit cùng transaction, không phải một bảng riêng lẻ).

- **I (Independent)**: ⚠️ — là điều kiện tiên quyết kỹ thuật cho `KC-4` mà [Epic-Legal-And-Compliance](../Epics/Epic-Legal-And-Compliance.md) phụ thuộc chéo vào ([Epic cha mục 5.3](../Epics/Epic-Multi-Tenancy-And-Platform.md#53-ba-điều-không-thuộc-dod-của-epic-này)); không thể xếp song song hoàn toàn với các Story tiêu thụ transaction boundary này.
- **S (Small)**: ⚠️ — không có sub-slice "theo từng schema" nào chứng minh được giá trị transaction boundary một mình; giá trị chỉ xuất hiện khi cả 3 schema + lint rule cùng tồn tại.

---

_Created by architect_
_Author: trisjr_
