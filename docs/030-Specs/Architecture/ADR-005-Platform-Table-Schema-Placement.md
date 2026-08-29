---
id: ADR-005
type: adr
status: draft
project: comic-studio
created: 2026-08-29
---

# ADR-005: Vị trí schema cho nhóm bảng platform / cross-cutting

Related to: [SDD-Comic-Studio](./SDD-Comic-Studio.md)

## Context

> [!IMPORTANT]
> ⛔ **Đây KHÔNG phải là ADR ghi lại một quyết định của Phase 1.** Không tài liệu Phase 1 nào gán schema cho nhóm bảng dưới đây. Lens `architect` đã grep toàn bộ [SRS-Comic-Studio](../../020-Requirements/SRS-Comic-Studio.md), `MVP-Scope` và 12 Story kiến trúc để xác nhận điều đó ([findings/architect §7 G3](../../010-Planning/pm-runs/2026-08-28-phase-2-architecture-design-comic-studio/findings/architect.md)). Đây là **quyết định mới sinh ra ở Phase 2**, do PM phân xử. Phần lập luận bên dưới **chính là** giá trị của tài liệu này — không có nó thì quyết định này không ai chịu trách nhiệm được.

### Vấn đề

`D-01` **CHỐT**: modular monolith — **1 process · 1 PostgreSQL · đúng 3 schema** `story` / `comic` / `generation` ([SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-NFR-02`).

Nhưng **9 bảng platform / cross-cutting không thuộc schema nào theo tên**:

| # | Bảng | Vì sao không thuộc 3 schema | Tầng phạm vi |
|--:|---|---|:--:|
| 1 | `tenant` | Đơn vị cô lập dữ liệu — đứng trên cả 3 module | `[24⭐]` |
| 2 | `user` | Định danh, do auth vendor mua ngoài sở hữu; bảng này chỉ giữ ánh xạ | `[24⭐]` |
| 3 | `membership` | Quan hệ `user` ↔ `tenant` | `[24⭐]` |
| 4 | `change_log` | **Cross-cutting**: ghi hành động ở mọi module | `[H-non⭐]` |
| 5 | `field_provenance` | **Cross-cutting**: trỏ tới field của `story`, `comic` lẫn `generation` | `[24⭐]` |
| 6 | `usage_event` | **Cross-cutting**: đo tiêu tài nguyên của mọi module | `[24⭐]` |
| 7 | `usage_daily` | Rollup của `usage_event` | `[24⭐]` |
| 8 | `job` | Hàng đợi — là **đường giao tiếp DUY NHẤT** giữa API và Worker | `[H-non⭐]` |
| 9 | `credit_ledger` | Kinh tế — trên tenant, không trên artifact | `[OoH]` MVP3 |

Ba bảng khác cũng mang schema `??` trong [findings §3.4](../../010-Planning/pm-runs/2026-08-28-phase-2-architecture-design-comic-studio/findings/architect.md): `takedown_request`, `project_access_state`, `credit_hold`. Quyết định của ADR này **áp cho toàn bộ nhóm P**, không chỉ 9 hàng trên.

### Những gì Phase 1 ĐÃ neo (và giới hạn của các mỏ neo đó)

| Mỏ neo | Nói gì | ⚠️ Không nói gì |
|---|---|---|
| [SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-NFR-02` | *"3 schema (`story` / `comic` / `generation`)"* — **CHỐT** | Bảng nào nằm ở schema nào |
| [Story-Modular-Monolith-Three-Schemas](../../022-User-Stories/Backlog/Story-Modular-Monolith-Three-Schemas.md) AC *"đúng 3 schema Postgres"* | AC đo: *"Database có đúng 3 schema Postgres `story`, `comic`, `generation` trong **cùng một** database — đo bằng: truy vấn `information_schema.schemata`, xác nhận **đủ 3 tên schema tồn tại**"* | Cách đo là **presence-based** (*"đủ 3 tên tồn tại"*), không phải **census-based** (*"không có schema thứ 4"*) |
| [Story-Modular-Monolith-Three-Schemas](../../022-User-Stories/Backlog/Story-Modular-Monolith-Three-Schemas.md) AC *"3 INSERT trong cùng một transaction"* | `generation` ở schema `generation`; `change_log` và `usage_event` chỉ được nhắc là *"cùng một transaction"* | ⛔ **Không nêu schema** của `change_log` / `usage_event` |
| [SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-NFR-13` (`KC-4`) | `INSERT generation` + `INSERT change_log` + `INSERT usage_event` **bất khả phân** | Không ràng buộc vị trí schema (transaction Postgres span được nhiều schema trong cùng database) |
| [SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-NFR-01` | `tenant_id NOT NULL` mọi bảng nghiệp vụ, cột đầu mọi composite index, RLS lớp phòng thủ thứ hai | Không nói bảng platform có phải *"bảng nghiệp vụ"* hay không |

### Ràng buộc bao quanh quyết định

- `D-50` / `KC-4`: bằng chứng pháp lý phải commit cùng transaction với artifact ([SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-NFR-13`).
- `D-48`: `change_log` **append-only ghi MỌI hành động người dùng** ([SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-FR-35`) — tiền đề của lập luận *"decisive contribution"*.
- `D-03` + `D-42`: câu **CLAIM job** là *"câu SQL nóng nhất"*, phải chứa `in_flight_per_tenant < N` ngay từ đầu ([SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-FR-25`, `SRS-FR-26`).
- `D-04`: lint rule cấm import chéo module, `comic` → `story` chỉ qua `resolveState()` / `getBible()` ([SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-NFR-04`).
- `D-58`: `usage_daily` là rollup trên `usage_event` thô, cho **p50/p90 regen ratio** ([SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-FR-30`).

---

## Decision

### Q1. Nhóm bảng platform / cross-cutting nằm ở schema `public`

⭐ **Quyết định (PM phân xử, Phase 2)**: đặt toàn bộ **nhóm P** vào schema **`public`** của **cùng một** PostgreSQL database với `story` / `comic` / `generation`.

Tên đủ điều kiện dùng trong mọi tài liệu Schema và API sau này: `public.tenant`, `public.user`, `public.membership`, `public.change_log`, `public.field_provenance`, `public.usage_event`, `public.usage_daily`, `public.job`, `public.credit_ledger`, `public.takedown_request`, `public.project_access_state`, `public.credit_hold`.

### Q2. Quy tắc phân loại — một câu, không có vùng xám

> Bảng thuộc **đúng một** module nghiệp vụ `M1`–`M6` ⇒ nằm ở schema của module đó (`story` / `comic` / `generation`).
> Bảng thuộc tầng nền tảng (`M7`), tầng cross-cutting (`M8`), tầng pháp lý (`M9`) hoặc tầng kinh tế (`M10`) ⇒ nằm ở `public`.

⛔ **Không có bảng nghiệp vụ nào của `M1`–`M6` được đặt ở `public`.** Chiều ngược lại cũng vậy: không bảng nhóm P nào được đặt vào 3 schema module.

### Q3. Bốn guardrail bắt buộc đi kèm

Quyết định này **chỉ an toàn nếu có guardrail**. `public` là schema mặc định của PostgreSQL, nên nếu không chặn, nó sẽ trôi thành nơi chứa mọi thứ.

| # | Guardrail | Cưỡng chế bằng |
|--:|---|---|
| **G-1** | `REVOKE CREATE ON SCHEMA public FROM PUBLIC` và khỏi role ứng dụng. Chỉ role owner chạy migration mới tạo được object ở `public` | Migration số 1 + test quyền |
| **G-2** | Danh sách bảng trong `public` là **closed list** — đúng bằng bảng ở [Q1](#q1-nhóm-bảng-platform--cross-cutting-nằm-ở-schema-public). Thêm bảng mới vào `public` **phải sửa ADR này trước** | Test CI: liệt kê `information_schema.tables WHERE table_schema='public'`, so với danh sách hằng số trong repo; lệch ⇒ CI đỏ |
| **G-3** | `search_path` khai tường minh ở tầng kết nối; ⛔ mọi câu SQL trong migration và trong code dùng **tên đủ điều kiện** (`public.job`, `generation.generation`…), không dựa vào `search_path` để phân giải | Lint / code review checklist |
| **G-4** | Mọi bảng nhóm P **có `tenant_id`** vẫn tuân `D-09`: `tenant_id NOT NULL`, cột đầu mọi composite index, bật RLS. Cơ chế bơm context: xem `ADR-006` | Test đã có sẵn ở [Story-Tenant-Id-And-RLS-Everywhere](../../022-User-Stories/Backlog/Story-Tenant-Id-And-RLS-Everywhere.md) §4 AC *"Xác minh được"* |

### Q4. Ba bảng là ngoại lệ đã biết của `G-4` — ⛔ ADR này KHÔNG quyết

`tenant`, `user`, `membership` là **định danh**, không phải *"dữ liệu nghiệp vụ thuộc về một tenant"* theo nghĩa thông thường (một row `tenant` không thuộc về chính nó theo cách một row `panel` thuộc về một tenant). Policy RLS cho ba bảng này là bài toán riêng, và nó dính vào vòng lặp *"cần tenant context để đọc, mà phải đọc mới biết tenant"* — xem `ADR-006` mục **Đường API**.

| Việc còn mở | Ai đóng | Khi nào |
|---|---|---|
| Policy RLS cụ thể cho `public.tenant` / `public.user` / `public.membership` | Architect, ở lô **DB Schema** | Trước khi `DB-Entity-Tenant.md` được duyệt |
| `public.takedown_request` là bề mặt **không auth, không tenant context** (`M9`) ⇒ không áp được RLS theo tenant | Architect, ở lô **DB Schema** + `ADR-006` | Cùng mốc trên |

---

## Alternatives considered

### (a) Thêm schema thứ 4 tên `platform`

**Nội dung**: `CREATE SCHEMA platform`, đặt cả 12 bảng nhóm P vào đó. Database có 4 schema: `story`, `comic`, `generation`, `platform`.

**Điểm mạnh — phải ghi nhận trung thực**: về mặt **kỹ thuật thuần**, đây là phương án **sạch nhất**. Tên đủ điều kiện tự nói lên tầng kiến trúc (`platform.change_log` đọc là *"bảng cross-cutting"*, `public.change_log` thì không). Nó cho phép phân quyền theo schema (`GRANT ... ON SCHEMA platform`), tách được quyền tầng nền tảng khỏi quyền tầng nghiệp vụ chỉ bằng một câu lệnh. Nó cũng làm `G-2` không cần thiết, vì ranh giới đặt tên tự cưỡng chế.

**⛔ Lý do loại**: nó **đổi một quyết định CHỐT**.

- [SRS](../../020-Requirements/SRS-Comic-Studio.md) phát biểu `SRS-NFR-02` là *"**3 schema** (`story` / `comic` / `generation`)"*, cột **Mức độ rắn** của chính hàng đó ghi **CHỐT** — nhãn cao nhất, nghĩa là *"không mở lại"*.
- [Story-Modular-Monolith-Three-Schemas](../../022-User-Stories/Backlog/Story-Modular-Monolith-Three-Schemas.md) AC *"đúng 3 schema Postgres"* dựng AC đo *"database có **đúng 3 schema**"*.
- **Phase 2 không có thẩm quyền mở lại một quyết định CHỐT của Phase 1.** Lý do loại ở đây là **lý do thẩm quyền, không phải lý do kỹ thuật** — và ADR này ghi thẳng điều đó thay vì nguỵ trang nó thành một lập luận kỹ thuật.

**⚠️ Một điểm phải nói rõ để không ai hiểu nhầm về sau**: cách đo của `Story-Modular` AC *"đúng 3 schema Postgres"* là **presence-based** (*"xác nhận đủ 3 tên schema tồn tại"*). Nếu ai đó đọc nó thành census-based (*"database chỉ có đúng 3 schema, không hơn"*) thì **cả phương án (b) cũng trượt** — vì `public` (và `information_schema`, `pg_catalog`) **luôn tồn tại** trong mọi database PostgreSQL mặc định. Không có cách đọc chặt nào mà một database PostgreSQL thật thoả được. ⇒ Cách đọc đúng của AC *"đúng 3 schema Postgres"* là presence-based, và phương án (b) **không thêm bất kỳ schema nào** so với một database PostgreSQL trống.

**Nếu muốn mở lại**: đường đi là **PM/stakeholder sửa `SRS-NFR-02`**, không phải một ADR Phase 2 tự quyết. Chi phí di chuyển sau này: `ALTER TABLE ... SET SCHEMA` (xem [Consequences](#consequences)).

### (b) Đặt vào schema `public` — ⭐ ĐÃ CHỌN

**Nội dung**: xem [Decision](#decision).

**Điểm mạnh**: không đụng bất kỳ quyết định CHỐT nào; không thêm schema so với database mặc định; `KC-4` vẫn là **một** transaction trên **một** database; `change_log` vẫn là **một** bảng duy nhất; câu CLAIM job vẫn chạy trên **một** bảng.

**Điểm yếu — không được giấu**: mất tín hiệu ngữ nghĩa trong tên, mất khả năng phân quyền theo schema, và `public` có xu hướng trôi thành bãi rác. Ba guardrail `G-1`, `G-2`, `G-3` tồn tại **chính xác** để bù ba điểm yếu này. **Nếu guardrail không được dựng thì quyết định này mất phần lớn giá trị** — đây là điều kiện, không phải khuyến nghị.

### (c) Rải theo module chủ sở hữu (mỗi schema một bảng `change_log`)

**Nội dung**: `story.change_log`, `comic.change_log`, `generation.change_log`; tương tự cho `usage_event`, `field_provenance`, `job`.

**⛔ Lý do loại — bốn tầng, tầng đầu là nặng nhất**:

1. **Phá quy tắc *"một `change_log` duy nhất"*, và qua đó phá điều kiện kiểm chứng của `KC-4`.**
   ⚠️ Cần chính xác về mặt kỹ thuật: transaction PostgreSQL **vẫn span được** nhiều schema trong cùng một database, nên lý do loại **KHÔNG phải** *"không commit chung được"*. Lý do thật là: **định tuyến trở thành một quyết định runtime không ai cưỡng chế được.**
   Ví dụ cụ thể, lấy thẳng từ `D-48` ([SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-FR-35`): hành động *"chọn generation X thay vì Y"* diễn ra trong **editor** (`M6`, schema `comic`) nhưng đối tượng là một **`generation`** (`M5`, schema `generation`). Ghi vào bảng nào?
   - Ghi vào cả hai ⇒ **đếm trùng**, mất tính *"một dòng sự thật append-only"*.
   - Ghi vào một ⇒ mọi đường truy vấn bằng chứng phải `UNION` 3 bảng, và **không có gì cưỡng chế** rằng quy tắc định tuyến luôn được tuân thủ.
   `KC-4` phát biểu: *"bằng chứng có thể thiếu ngẫu nhiên thì không phải bằng chứng"* ([SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-NFR-13`). Chứng minh tính bất khả phân trên **một** bảng là **một** test. Trên **ba** bảng phân mảnh là ba test **cộng** một quy tắc định tuyến do con người nhớ — với **1 dev không code review**, đó là chỗ sẽ thủng.

2. **Phá `usage_daily`.** `D-58` bắt rollup ra **p50/p90 regen ratio** từ `usage_event` thô ([SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-FR-30`). Rải ra 3 bảng ⇒ mọi rollup thành aggregate xuyên bảng, và AC *"một lần best-of-N (N=3) tạo đúng **3** `usage_event` row"* ([Story-Usage-Event-And-Daily-Rollup](../../022-User-Stories/Backlog/Story-Usage-Event-And-Daily-Rollup.md) AC *"đúng 3 `usage_event` row"* — đo bằng `COUNT(*)`) không còn đo được trên một bảng.

3. **Phá câu SQL nóng nhất.** `D-03` + `D-42` ([SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-FR-25`, `SRS-FR-26`): câu CLAIM dùng `FOR UPDATE SKIP LOCKED` **và** phải chứa `in_flight_per_tenant < N`. Rải `job` ra 3 bảng ⇒ claim phải quét 3 bảng, `SKIP LOCKED` mất tính nguyên tử của một câu, fairness per tenant phải tính xuyên bảng. [SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-FR-26` cảnh báo thẳng: *"nhồi vào sau là sửa lại đúng câu SQL nóng nhất"*.

4. **Đụng `D-04`.** Mỗi module ghi `change_log` của riêng nó ⇒ mọi module đều phải chạm bảng của schema khác khi truy vấn bằng chứng xuyên module, tạo đúng loại phụ thuộc chéo mà lint rule ([SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-NFR-04`) tồn tại để chặn.

### (d) Biến thể đã cân nhắc và bỏ: giữ `public` nhưng dùng tiền tố tên bảng (`platform_change_log`)

**Loại** vì nó chỉ mô phỏng ngữ nghĩa của (a) bằng quy ước đặt tên, không lấy lại được khả năng phân quyền theo schema, mà lại làm mọi tên bảng dài hơn và tạo một quy ước nữa phải nhớ. `G-2` (closed list kiểm ở CI) đạt được cùng mục tiêu với chi phí thấp hơn và **cưỡng chế được**, thay vì trông vào kỷ luật đặt tên.

---

## Consequences

### Tích cực

- ⭐ **13 file `DB-Entity-*` và 14 file `Endpoint-*`/`Spec-Integration-*` ở lô sau có đúng MỘT quy tắc để trỏ tới** ([Q2](#q2-quy-tắc-phân-loại--một-câu-không-có-vùng-xám)). Trước ADR này, 27 file đó không có căn cứ nào để viết tên đủ điều kiện.
- **Không đụng quyết định CHỐT nào** của Phase 1. `SRS-NFR-02` giữ nguyên, `Story-Modular` AC *"đúng 3 schema Postgres"* vẫn PASS.
- `KC-4` giữ nguyên hình dạng đơn giản nhất: một database, một transaction, một `change_log`, một `usage_event`.
- Câu CLAIM job vẫn là một câu trên một bảng ⇒ `D-42` nhồi được vào đúng chỗ `SRS-FR-26` yêu cầu.
- Migration số 1 không cần `CREATE SCHEMA` thêm; ít bề mặt cấu hình `search_path` hơn.

### Tiêu cực — chi phí thật của quyết định này

- **Mất tín hiệu ngữ nghĩa trong tên đủ điều kiện.** `public.change_log` không tự nói nó là bảng cross-cutting. Bù bằng `G-2` (closed list ở CI) và bằng chính tài liệu này — tức là bù bằng **quy trình**, không phải bằng **cơ chế**. Quy trình yếu hơn cơ chế.
- **Không phân quyền được theo schema.** Muốn tách quyền *"role này chỉ đọc tầng platform"* phải cấp quyền ở **mức bảng**, dài hơn và dễ sót hơn `GRANT ... ON SCHEMA`.
- **`public` có xu hướng trôi.** Nếu `G-1` (`REVOKE CREATE`) không được dựng ở migration số 1, mọi object tạo vội (bảng tạm, view thử nghiệm) sẽ mặc định rơi vào `public` và closed list `G-2` sẽ liên tục đỏ cho tới khi ai đó tắt test — đây là failure mode thực tế nhất của quyết định này.
- **Vị trí của extension là một câu hỏi bị đẩy về sau.** Extension PostgreSQL cài mặc định vào `public` sẽ nằm chung với bảng nhóm P và làm `G-2` phức tạp thêm. `D-06` ghi rõ `pgvector` **không bị cấm** (chỉ `❌` toàn horizon MVP0–MVP4, [SRS](../../020-Requirements/SRS-Comic-Studio.md) §2.3 · `SRS-NFR-21` · §6.2) ⇒ ngày nào bật, câu hỏi này quay lại. ⛔ ADR này **không** tự đặt ra một schema `extensions` — làm vậy là tự mâu thuẫn với chính lập luận loại (a). **Ai đóng**: Architect, khi extension đầu tiên được đề xuất; phải sửa ADR này.
- **Không phải quyết định không thể đảo — và cần ghi lại giá.** Đường di chuyển `public` → `platform` là `ALTER TABLE ... SET SCHEMA` (rẻ ở tầng DDL), nhưng kéo theo: sửa mọi tên đủ điều kiện trong code và trong 27 tài liệu spec, sửa `search_path`, tạo lại grant, và **kiểm lại mọi RLS policy**. Chi phí tăng theo số tài liệu đã viết ⇒ **nếu định đảo thì đảo trước lô Schema, không phải sau**.

### Việc còn để `TBD`

| Việc | Ai đóng | Khi nào |
|---|---|---|
| Policy RLS cho `tenant` / `user` / `membership` | Architect (lô DB Schema) + `ADR-006` | Trước khi `DB-Entity-Tenant.md` được duyệt |
| Xử lý bề mặt không tenant của `takedown_request` (`M9`) | Architect (lô DB Schema) + `ADR-006` | Cùng mốc trên |
| Vị trí extension khi extension đầu tiên xuất hiện | Architect | Khi có đề xuất, phải sửa ADR này |
| ⚠️ **`user` là từ khoá SQL** ⇒ `public.user` phải quote (`public."user"`) ở mọi câu lệnh. `D-11` đặt tên **entity** là `user` ([SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-FR-01`) nhưng ⛔ không đặt tên **bảng** ⇒ chọn giữ nguyên tên (kèm quote) hay đổi tên bảng là quyết định của lô Schema | Architect (lô DB Schema) | Trong `DB-Entity-User.md`; quyết xong phải phản ánh lại vào [Q1](#q1-nhóm-bảng-platform--cross-cutting-nằm-ở-schema-public) |
| `credit_ledger` / `credit_hold` là `[OoH]` MVP3 — chừa chỗ ngay theo `D-62` ([SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-FR-32` cấm retrofit ba tầng giá) | Architect (lô DB Schema) | Cùng lô Schema, ở mức *"reserve chỗ"* |

---

## Đã quyết ở đâu

| Quyết định | Mã `D-xx` | Nguồn (file + mã requirement) |
|---|:--:|---|
| Modular monolith · 1 process · 1 PostgreSQL · **3 schema** `story`/`comic`/`generation` | `D-01` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-NFR-02` · [Story-Modular-Monolith-Three-Schemas](../../022-User-Stories/Backlog/Story-Modular-Monolith-Three-Schemas.md) AC *"đúng 3 schema Postgres"* |
| Lint rule cấm import chéo module; `comic` → `story` chỉ qua `resolveState()` / `getBible()` | `D-04` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-NFR-04` |
| ⛔ Không microservices (3 service) · ⛔ không 2 PostgreSQL · ⛔ không Vector DB riêng · ⛔ không job queue ngoài Postgres | `D-05` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) **`SRS-NFR-21`** |
| `pgvector` **không bị cấm** nhưng `❌` toàn horizon MVP0–MVP4 | `D-06` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) **§2.3** · **`SRS-NFR-21`** · §6.2 (*"Bẫy (a) — `pgvector` KHÔNG bị cấm"*) |
| Job queue trong PostgreSQL; claim `FOR UPDATE SKIP LOCKED`; transactional enqueue | `D-03` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-FR-25` |
| Câu CLAIM phải chứa `in_flight_per_tenant < N` (**N = `TBD`**) | `D-42` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-FR-26` · §5.2 |
| `tenant_id NOT NULL` mọi bảng nghiệp vụ + cột đầu mọi composite index + RLS | `D-09` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-NFR-01` |
| `tenant` / `user` / `membership` là **ba entity riêng** | `D-11` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-FR-01` |
| `change_log` append-only ghi **MỌI** hành động người dùng | `D-48` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-FR-35` |
| `field_provenance` mức field + `generation.origin` | `D-49` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-FR-36` |
| **`KC-4`**: `generation` + `change_log` + `usage_event` commit **cùng một transaction** | `D-50` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-NFR-13` · [Story-Modular-Monolith-Three-Schemas](../../022-User-Stories/Backlog/Story-Modular-Monolith-Three-Schemas.md) §4 AC *"3 INSERT trong cùng một transaction"* · *"⛔ không partial commit"* |
| `usage_event` append-only + rollup `usage_daily` (p50/p90 regen ratio) | `D-58` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-FR-30` · [Story-Usage-Event-And-Daily-Rollup](../../022-User-Stories/Backlog/Story-Usage-Event-And-Daily-Rollup.md) AC *"đúng 3 `usage_event` row"* |
| `credit_ledger` append-only + `CHECK (available >= 0)` ở tầng DB | `D-60` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-FR-28` |
| Ba tầng giá phải đỡ được từ đầu, ⛔ không retrofit | `D-62` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-FR-32` |
| ⛔ **CHƯA quyết ở Phase 1**: schema của nhóm bảng platform | — | [findings/architect §7 G3](../../010-Planning/pm-runs/2026-08-28-phase-2-architecture-design-comic-studio/findings/architect.md) · §3.4 (cột Schema = `??`) |
