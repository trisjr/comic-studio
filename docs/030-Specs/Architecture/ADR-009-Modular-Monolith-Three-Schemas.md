---
id: ADR-009
type: adr
status: draft
project: comic-studio
created: 2026-08-29
---

# ADR-009: Modular monolith — 1 process · 1 PostgreSQL · 3 schema

Related to: [SDD-Comic-Studio](./SDD-Comic-Studio.md)

## Context

> [!IMPORTANT]
> ⛔ **Đây là ADR `record-only`.** Mọi quyết định trong mục `Decision` **đã được CHỐT ở Phase 1** và **không được mở lại ở Phase 2**. Vai trò của tài liệu này là **đóng băng** quyết định thành tài sản tri thức trích dẫn được, để một run sau **không vô tình mở lại** một câu hỏi đã đóng.
>
> Giá trị thật của ADR này nằm ở [Alternatives considered](#alternatives-considered) — *vì sao microservices bị loại* — và ở [Đã quyết ở đâu](#đã-quyết-ở-đâu) — truy được về file + mã requirement.

### Ràng buộc số một là ràng buộc PHÁP LÝ, không phải "đơn giản hơn"

Nghĩa vụ chứng minh *"đóng góp trí tuệ đáng kể và mang tính quyết định"* của con người bắt hệ thống phải commit **cùng một transaction**:

```
INSERT generation + INSERT change_log + INSERT usage_event  ⇒ bất khả phân
```

Đây là `KC-4` ([MVP-Scope](../../010-Planning/MVP-Scope.md) §6 `KC-4`), phát biểu ở tầng requirement là [`SRS-NFR-13`](../../020-Requirements/SRS-Comic-Studio.md) và ở tầng nghiệp vụ là [`BR-007-02`](../../020-Requirements/BRD/BRD-007-Legal-And-Compliance.md):

> *"Bằng chứng có thể thiếu ngẫu nhiên thì không phải bằng chứng."*

⭐ **Ràng buộc này MỘT MÌNH đủ để loại bỏ microservices và mọi kiến trúc 2-database.** Một transaction boundary không tồn tại xuyên hai database, và bất kỳ cơ chế thay thế nào (saga, outbox, eventual consistency) đều tạo ra đúng cái mà `KC-4` cấm: một cửa sổ thời gian trong đó bằng chứng **có thể** thiếu.

> [!WARNING]
> ⛔ **Đừng đọc lý do chính của ADR này thành *"monolith thì đơn giản hơn"*.** Đơn giản là **hệ quả dễ chịu**, không phải căn cứ. Nếu ngày mai đội có 20 người, `KC-4` vẫn loại microservices y như hôm nay.

### Lý do thứ hai: RLS không bảo vệ được join phía application

[`SRS-NFR-01`](../../020-Requirements/SRS-Comic-Studio.md) dựng RLS làm **lớp phòng thủ thứ hai** cho tenant isolation. Nhưng RLS có một giới hạn đã biết, ghi trong [Glossary](../../999-Resources/Glossary.md) mục `RLS` và nhắc lại ở [SRS §3.E khối `[!WARNING]`](../../020-Requirements/SRS-Comic-Studio.md):

> *"RLS không bảo vệ được join thực hiện phía application."*

Tách dữ liệu ra hai database **buộc** mọi join xuyên module chạy ở tầng ứng dụng ⇒ **phá đúng lớp phòng thủ mà `KC-5` tồn tại để dựng**. Xem [ADR-010](./ADR-010-Tenant-Isolation-With-RLS.md).

### Lý do thứ ba (phụ trợ, không phải căn cứ chính)

`CF-6.9` `[EM]`: multi-tenancy **đã ăn 15–25% effort** ([MVP-Scope](../../010-Planning/MVP-Scope.md) §3 `E1`, [Story-Modular-Monolith-Three-Schemas](../../022-User-Stories/Backlog/Story-Modular-Monolith-Three-Schemas.md) §3 Bối cảnh & nguồn). Với `bus factor = 1` và **không có code review** (`CF-1.2`), cộng thêm chi phí vận hành 3 service là chọn cách hỏng nhanh nhất.

### ⚠️ Bẫy cắt-lẫn phải đọc trước khi trích ADR này

> [!CAUTION]
> **`pgvector` KHÔNG bị cắt. `pgvector` được CỐ Ý ĐỂ MỞ.**
>
> [SRS §6.2 bẫy (a)](../../020-Requirements/SRS-Comic-Studio.md) và [BRD-002 §6](../../020-Requirements/BRD/BRD-002-Story-Intelligence.md) phân biệt tuyệt đối hai thứ nghe giống nhau:
>
> | Thứ | Trạng thái | Nguồn |
> |---|---|---|
> | **Vector DB riêng như một service** | ❌ **CẮT HẲN** khỏi thiết kế | `MVP-Scope §3 E6` · `SRS-NFR-21` |
> | **`pgvector` trong cùng PostgreSQL** | ❌ MVP0 · ❌ MVP1 · ❌ MVP2 · ⛔ MVP3 · ⛔ MVP4 · **🟡 Full Scope** *"khi có bằng chứng SQL+FTS không đủ"* | `MVP-Scope §3 B5` · `BRD-002` §6 |
>
> ⛔ **Viết một ADR kiểu *"cấm vector search"* là ĐÓNG MỘT CÁNH CỬA MÀ `B5` CỐ Ý ĐỂ MỞ.** ADR này **không cấm** `pgvector`. Nó chỉ ghi nhận: ở toàn horizon MVP0–MVP4, lời giải là **Story Bible *là* index của mình** + PostgreSQL **full-text search** (`BR-002-09`, [BRD-002](../../020-Requirements/BRD/BRD-002-Story-Intelligence.md)).
>
> Điều kiện mở lại đã ghi sẵn và **không cần một ADR mới để cho phép**: *"có bằng chứng cụ thể là SQL + FTS không đủ"*.

## Decision

### D1. Topology: 1 process · 1 PostgreSQL · **đúng 3** schema

`story` / `comic` / `generation`, **trong cùng một database** (`SRS-NFR-02`).

Điều kiện xác minh đã ghi sẵn ở [Story-Modular-Monolith-Three-Schemas](../../022-User-Stories/Backlog/Story-Modular-Monolith-Three-Schemas.md) §4 AC *"Xác minh được"*: truy vấn `information_schema.schemata` phải trả về đủ 3 tên schema **trong 1 database**.

### D2. Module boundary bằng **package + interface**, ⛔ KHÔNG HTTP nội bộ

`SRS-NFR-02` ghi tường minh *"module boundary bằng package + interface — **không HTTP nội bộ**"*. Đây là **seam #3** của [MVP-Scope §4.2](../../010-Planning/MVP-Scope.md).

### D3. Seam `comic` → `story` là **DUY NHẤT HAI HÀM**, cưỡng chế ở CI

| Cho phép | Cấm |
|---|---|
| `resolveState(entity, at_event)` | Mọi import trực tiếp vào nội bộ module `story` |
| `getBible()` | Mọi query từ module `comic` trỏ thẳng vào bảng của schema `story` |

- Cưỡng chế bằng **lint rule chạy trong CI** (`SRS-NFR-04` · `BR-005-06`, [BRD-005](../../020-Requirements/BRD/BRD-005-Multi-Tenancy-And-Platform.md)).
- Điều kiện xác minh: một PR cố tình vi phạm phải làm **CI FAIL** và **không merge được** ([Story-Modular](../../022-User-Stories/Backlog/Story-Modular-Monolith-Three-Schemas.md) §4 AC *"Xác minh được"* · *"Đường không hạnh phúc"*).
- ⭐ Ngữ nghĩa của hai hàm này thuộc [ADR-011](./ADR-011-Narrative-Time-Key-And-State-Reduction.md) — ADR-009 chỉ chốt **rằng chúng là seam duy nhất**.

### D4. Danh sách phủ định — bốn thứ bị **CẮT HẲN**

`SRS-NFR-21` · `MVP-Scope §3 E6` — `❌` ở **mọi** cột, kể cả Full Scope:

1. ⛔ **KHÔNG** microservices (3 service)
2. ⛔ **KHÔNG** 2 PostgreSQL
3. ⛔ **KHÔNG** Vector DB **riêng như một service**
4. ⛔ **KHÔNG** job queue ngoài Postgres

### D5. `pgvector` — ⚠️ **để mở**, không nằm trong D4

Xem khối `[!CAUTION]` ở mục `Context` — *"Bẫy cắt-lẫn phải đọc trước khi trích ADR này"*. ADR này **cố ý không** phát biểu một quy tắc cấm nào về `pgvector`.

### D6. Bảng platform / cross-cutting — ⛔ ADR này KHÔNG quyết

3 schema đặt tên theo module không phủ nhóm bảng cross-cutting (`tenant`, `user`, `membership`, `change_log`, `field_provenance`, `usage_event`, `usage_daily`, `job`, `credit_ledger`…). Vị trí schema của nhóm này **đã được [ADR-005](./ADR-005-Platform-Table-Schema-Placement.md) chốt** — ⛔ **không quyết lại ở đây**.

### D7. Ranh giới với các ADR khác — ⛔ không lặp nội dung

| Chủ đề | ADR sở hữu | ADR-009 chỉ dùng làm ngữ cảnh |
|---|---|---|
| Vị trí schema nhóm bảng platform | [ADR-005](./ADR-005-Platform-Table-Schema-Placement.md) | ✅ |
| Cơ chế bơm tenant context cho RLS | [ADR-006](./ADR-006-RLS-Tenant-Context-Injection.md) | ✅ |
| `tenant_id` + RLS như một thuộc tính toàn cục | [ADR-010](./ADR-010-Tenant-Isolation-With-RLS.md) | ✅ |
| Ngữ nghĩa `resolveState()` / `getBible()` | [ADR-011](./ADR-011-Narrative-Time-Key-And-State-Reduction.md) | ✅ |
| Schema bảng `job`, retry/backoff, `FOR UPDATE SKIP LOCKED`, transactional enqueue | `ADR-015-Job-Queue-In-Postgres` | ✅ |
| Nội dung nghĩa vụ provenance (`KC-1`…`KC-4`), `change_log`, `field_provenance` | `ADR-017-Provenance-Chain-And-One-Transaction-Boundary` | ✅ |

⇒ ADR-009 cung cấp **điều kiện kỹ thuật** cho `KC-4` (một DB ⇒ một transaction boundary); **nội dung nghĩa vụ audit** thuộc [BRD-007](../../020-Requirements/BRD/BRD-007-Legal-And-Compliance.md) và `ADR-017` ([Story-Modular](../../022-User-Stories/Backlog/Story-Modular-Monolith-Three-Schemas.md) §4 *"Ràng buộc cứng không được vi phạm"* · *"Story này KHÔNG làm"*).

## Alternatives considered

> ⭐ Đây là phần **giá trị nhất** của một ADR record-only: *vì sao phương án kia bị loại*. Mọi lý do dưới đây **trích từ nguồn Phase 1**, không phải suy luận mới. Chỗ nào là suy luận, em dán nhãn `[Kiến trúc suy luận]`.

### (a) Microservices — 3 service tách rời — ⛔ BỊ LOẠI

| # | Lý do bác | Nguồn |
|:--:|---|---|
| **1** ⭐ | **Mất transaction boundary.** `KC-4` đòi `generation` + `change_log` + `usage_event` commit **bất khả phân**. Không có transaction xuyên process/database. Mọi thay thế (saga / outbox / eventual consistency) đều để lại cửa sổ *"bằng chứng có thể thiếu"* ⇒ theo đúng phát biểu của `KC-4`, **không còn là bằng chứng** | `MVP-Scope` §6 `KC-4` · `SRS-NFR-13` · `BR-007-02` |
| **2** | **RLS không bảo vệ join phía application.** Tách service ⇒ join xuyên module dời lên tầng app ⇒ mất chính lớp phòng thủ mà `KC-5` dựng lên | `SRS §6.1` · `SRS §3.E` · `MVP-Scope §3 E6` |
| **3** | Multi-tenancy đã ăn **15–25%** effort `[EM]`; đội 1 người, `bus factor = 1`, không code review | `CF-6.9` · `CF-1.2` · `MVP-Scope` §3 `E1` |

⚠️ [MVP-Scope §4.2](../../010-Planning/MVP-Scope.md) ghi rõ lý do cắt này **MẠNH LÊN dưới mô hình SaaS**, không yếu đi — tức là *"sau này nhiều khách hơn thì tách"* **không phải** một đường lui hợp lệ.

### (b) Hai PostgreSQL (tách DB theo bounded context) — ⛔ BỊ LOẠI

Cùng lý do #1 của (a), ở dạng sắc hơn: `MVP-Scope §3 E6` ghi thẳng *"hai DB = mất transaction; RLS không bảo vệ được join phía ứng dụng"*. Đây là phương án **gần đúng nhất** với monolith và vì vậy là phương án **dễ bị mở lại nhất** — ghi ở đây để không phải tranh luận lại.

### (c) Vector DB riêng như một service — ⛔ BỊ LOẠI (nhưng ⚠️ đọc kỹ)

- Bị cắt hẳn ở `MVP-Scope §3 E6` · `SRS-NFR-21`.
- Lời giải thay thế **đã có tên**: *"Story Bible **là** index của mình"* + PostgreSQL **full-text search** (`BR-002-09`, [BRD-002](../../020-Requirements/BRD/BRD-002-Story-Intelligence.md)).
- ⚠️ **Việc bác phương án này KHÔNG kéo theo việc cấm `pgvector`** — xem `D5` ở mục `Decision`.

### (d) Job queue trên broker ngoài (Redis / SQS / RabbitMQ…) — ⛔ BỊ LOẠI

Nằm trong danh sách phủ định của `SRS-NFR-21`. Lý do cùng họ với (a)#1: enqueue trên broker ngoài **không** nằm trong transaction của Postgres. ⇒ Cơ chế thay thế và mọi tham số của nó thuộc `ADR-015`, ⛔ không đặc tả ở đây.

### (e) Ranh giới module bằng **quy ước + code review** thay vì lint rule — ⛔ BỊ LOẠI

`BR-005-06` ([BRD-005](../../020-Requirements/BRD/BRD-005-Multi-Tenancy-And-Platform.md)) phát biểu thẳng: ranh giới module phải được **cưỡng chế bằng lint rule, không bằng thoả thuận**. Bối cảnh làm nó thành bắt buộc: **1 dev, không có code review** (`CF-1.2`) ⇒ *"thoả thuận"* không có ai để thoả thuận với, và không có bước nào phát hiện vi phạm trước khi nó thành nợ kiến trúc.

### (f) HTTP nội bộ giữa các module trong cùng một process — ⛔ BỊ LOẠI

`SRS-NFR-02` loại tường minh. `[Kiến trúc suy luận]` — phương án này trả **toàn bộ chi phí của hệ phân tán** (serialize, timeout, retry, mất transaction) mà **không nhận được lợi ích nào** của nó, vì vẫn là một process.

### (g) ⚠️ Một phương án KHÔNG có trong hồ sơ

⛔ **Không có** hàng nguồn Phase 1 nào ghi lại việc *"gộp 3 schema thành 1 schema duy nhất"* đã được cân nhắc rồi bác. Phase 1 chốt thẳng **3 schema**. Em **không** dựng lại một câu chuyện bác bỏ không tồn tại — ai muốn mở câu hỏi đó phải mở nó như một quyết định mới, có ADR mới.

## Consequences

### Tích cực

- ⭐ `KC-4` đạt được **theo cấu trúc**, không phải theo kỷ luật: một database ⇒ một transaction boundary sẵn có. Exit criterion `M1-5` (*"test chứng minh chúng commit CÙNG MỘT transaction với artifact"*) trở nên **khả thi để PASS** ([Story-Modular](../../022-User-Stories/Backlog/Story-Modular-Monolith-Three-Schemas.md) §3 Bối cảnh & nguồn · §4 AC *"Xác minh được"*).
- RLS giữ được giá trị thật: mọi join nằm **trong** database ⇒ không có đường vòng qua tầng ứng dụng.
- Chi phí vận hành khớp với `bus factor = 1`; `R-21` ghi nguyên văn mitigation *"giữ dự án ở trạng thái **có thể bỏ dở và quay lại**: monolith (CF-9.2)"* ([BRD-005](../../020-Requirements/BRD/BRD-005-Multi-Tenancy-And-Platform.md) `R-21`).
- Seam `resolveState()` / `getBible()` giữ **đường nâng cấp** sang tách service về sau mà không phải viết lại ranh giới.

### Tiêu cực — chi phí thật của quyết định này

- **Blast radius một process.** Worker **chưa** tách process ở MVP1/MVP2: `E7` = `⛔` ở MVP1/MVP2, `✅` từ **MVP3** ([MVP-Scope](../../010-Planning/MVP-Scope.md) §3 `E7` · `SRS-NFR-03`) ⇒ trong horizon gần, một job nặng **có thể** ảnh hưởng đường API. Đây là `[OoH]` **đã biết và đã chấp nhận**, không phải sơ suất — kiến trúc phải chừa chỗ cho 2 entrypoint trên cùng image.
- **Một điểm scale duy nhất.** Một database phục vụ cả 3 module; một truy vấn xấu ở `comic` ảnh hưởng `story` và `generation`.
- **Lint rule là một bề mặt bảo trì.** Nó là thứ **duy nhất** giữ ranh giới module. Vô hiệu hoá nó (hoặc để nó rơi khỏi CI) không gây lỗi ngay — nó chỉ âm thầm biến monolith thành big ball of mud.
- **Story không chia nhỏ được.** [Story-Modular](../../022-User-Stories/Backlog/Story-Modular-Monolith-Three-Schemas.md) vỡ cả `I` và `S` (§6 INVEST): *"không có sub-slice 'theo từng schema' nào chứng minh được giá trị transaction boundary một mình"*. `E_build ≈ 14h` `[EM]`.
- **Rủi ro đọc nhầm về `pgvector`** là rủi ro thật và tái diễn — đó là lý do khối `[!CAUTION]` phải nằm ở đầu tài liệu chứ không phải trong phụ lục.

### Việc còn để `TBD` — ⛔ không được bịa

| Khoảng trống | Ai đóng | Khi nào |
|---|---|---|
| Lint tool cụ thể + cấu hình rule (phụ thuộc ngôn ngữ/framework) | [ADR-001](./ADR-001-Backend-And-Frontend-Tech-Stack.md) chốt nền tảng ⇒ engineer đặc tả rule ở tầng implementation | Trước khi dựng CI skeleton của MVP1 — AC *"PR vi phạm ⇒ CI FAIL"* cần rule tồn tại |
| Danh sách đầy đủ **bảng nghiệp vụ** thuộc từng schema | Lô `docs/030-Specs/Schema/DB-Entity-*.md` (architect) | Trước **migration số 1** |
| Thời điểm và cách tách worker thành process riêng (`E7`, MVP3) | PM khi mở horizon MVP3; ràng buộc đã ghi ở `SRS-NFR-03` | Khi PM mở horizon **MVP3** — ⛔ không sớm hơn (`E7` = `⛔` ở MVP1/MVP2) |

## Đã quyết ở đâu

> Bảng này là **hợp đồng truy vết** của ADR record-only. Mọi hàng đều đã đọc trực tiếp tại thời điểm viết; ⭐ neo bằng **mã requirement / tên mục**, ⛔ **không dùng số dòng** — số dòng mục ngay khi file nguồn đổi một ký tự.

| Quyết định | Mã `D-xx` | Nguồn (file + mã requirement) |
|---|:--:|---|
| Modular monolith: **1 process · 1 PostgreSQL · 3 schema** `story`/`comic`/`generation`; boundary bằng package + interface, ⛔ không HTTP nội bộ | `D-01` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) §3.E `SRS-NFR-02` · [MVP-Scope](../../010-Planning/MVP-Scope.md) §3 `E5` · [BRD-005](../../020-Requirements/BRD/BRD-005-Multi-Tenancy-And-Platform.md) `BR-005-05` |
| **Lint rule cấm import chéo module**; `comic` gọi `story` **DUY NHẤT** qua `resolveState()` + `getBible()`; cưỡng chế ở CI | `D-04` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) §3.E `SRS-NFR-04` · [BRD-005](../../020-Requirements/BRD/BRD-005-Multi-Tenancy-And-Platform.md) `BR-005-06` · [Story-Modular](../../022-User-Stories/Backlog/Story-Modular-Monolith-Three-Schemas.md) §4 AC *"Xác minh được"* · *"Đường không hạnh phúc"* |
| ⛔ **KHÔNG** microservices · **KHÔNG** 2 PostgreSQL · **KHÔNG** Vector DB riêng · **KHÔNG** job queue ngoài Postgres | `D-05` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) §6.1 `SRS-NFR-21` · [MVP-Scope](../../010-Planning/MVP-Scope.md) §3 `E6`, §4.2 |
| ⭐ **Lý do #1 cắt microservices/2-DB**: mất transaction boundary — `KC-4` đòi `generation` + `change_log` + `usage_event` commit bất khả phân | `D-05` ← `D-50` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) §3.G `SRS-NFR-13` · [MVP-Scope](../../010-Planning/MVP-Scope.md) §6 `KC-4` · [BRD-007](../../020-Requirements/BRD/BRD-007-Legal-And-Compliance.md) `BR-007-02` · [BRD-005](../../020-Requirements/BRD/BRD-005-Multi-Tenancy-And-Platform.md) `BR-005-09` |
| **Lý do #2**: RLS ⛔ không bảo vệ được join phía application ⇒ tách DB làm mất lớp phòng thủ của `KC-5` | `D-05` ← `D-10` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) §3.E khối `[!WARNING]` · §6.1 · [Glossary](../../999-Resources/Glossary.md) mục `RLS` |
| **Lý do #3** (phụ trợ): multi-tenancy đã ăn **15–25%** effort `[EM]`; 1 dev, không code review | — | `CF-6.9` · `CF-1.2` qua [MVP-Scope](../../010-Planning/MVP-Scope.md) §3 `E1` · [Story-Modular](../../022-User-Stories/Backlog/Story-Modular-Monolith-Three-Schemas.md) §3 Bối cảnh & nguồn |
| ⚠️ **`pgvector` CỐ Ý ĐỂ MỞ** — ⛔ không phải "đã cắt"; chỉ **Vector DB riêng** bị cắt hẳn. Full Scope `🟡` *"khi có bằng chứng SQL+FTS không đủ"* | `D-06` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) §6.2 bẫy (a) · [MVP-Scope](../../010-Planning/MVP-Scope.md) §3 `B5` · [BRD-002](../../020-Requirements/BRD/BRD-002-Story-Intelligence.md) §6 |
| Lời giải truy vấn ở MVP: **Story Bible là index của mình** + PostgreSQL full-text search | `D-06` | [BRD-002](../../020-Requirements/BRD/BRD-002-Story-Intelligence.md) `BR-002-09` |
| Worker là process triển khai riêng, **cùng codebase**, 2 entrypoint — `⛔` ở MVP1/MVP2, `✅` từ MVP3 ⇒ `[OoH]` | `D-02` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) §3.E `SRS-NFR-03` · [MVP-Scope](../../010-Planning/MVP-Scope.md) §3 `E7` |
| Bảng platform / cross-cutting nằm ở schema `public` — ⛔ ADR-009 không quyết lại | — | [ADR-005](./ADR-005-Platform-Table-Schema-Placement.md) |
| Cơ chế bơm tenant context (`SET LOCAL app.current_tenant`, role `app_worker`) — ⛔ ADR-009 không đặc tả | — | [ADR-006](./ADR-006-RLS-Tenant-Context-Injection.md) |
| Bảng ADR record-only + nhiệm vụ *"đóng băng, không mở lại"* | — | [findings/architect §2.2](../../010-Planning/pm-runs/2026-08-28-phase-2-architecture-design-comic-studio/findings/architect.md) · §2.3 (dòng `Cắt pgvector`) |

---

_Created by architect_
_Author: trisjr_
