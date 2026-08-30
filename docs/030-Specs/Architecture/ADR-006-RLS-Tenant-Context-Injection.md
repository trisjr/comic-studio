---
id: ADR-006
type: adr
status: draft
project: comic-studio
created: 2026-08-29
---

# ADR-006: Cơ chế bơm tenant context vào session PostgreSQL cho RLS

Related to: [SDD-Comic-Studio](./SDD-Comic-Studio.md)

## Context

> [!IMPORTANT]
> ⛔ **Phase 1 CHỐT rằng RLS phải bật. Phase 1 KHÔNG quyết cách policy biết tenant hiện tại là ai.** Đây là **quyết định mới của Phase 2** ([findings/architect §7 G4](../../010-Planning/pm-runs/2026-08-28-phase-2-architecture-design-comic-studio/findings/architect.md)). Lập luận bên dưới là giá trị của tài liệu này.

### ⚠️ Một hiệu chỉnh so với findings §7 G4 — phải đọc trước

`§7 G4` viết: *"Cách policy biết tenant hiện tại là ai thì **không tài liệu nào nói**"*, và chỉ dẫn `Story-Tenant-Id-And-RLS-Everywhere` AC *"RLS bật trên 100% bảng có `tenant_id`"*.

Khi đọc trực tiếp cùng Story đó, ADR này tìm thấy **hai dòng AC nữa mà `§7 G4` không dẫn**, và chúng neo nhiều hơn `§7 G4` mô tả:

| Dòng AC (§4 *"Đường không hạnh phúc"*) | Nguyên văn (trích) | Neo cái gì |
|---|---|---|
| [AC *"fail-closed 0 row"*](../../022-User-Stories/Backlog/Story-Tenant-Id-And-RLS-Everywhere.md) | *"Một session không set biến **`app.current_tenant`** (hoặc set giá trị không hợp lệ) bị RLS chặn trả về **0 row** thay vì lỗi 500 không kiểm soát được"* | ⭐ **Tên biến session**: `app.current_tenant`. ⭐ Hành vi bắt buộc: **fail-closed 0 row**, ⛔ không phải exception |
| [AC *"⛔ không rò context qua connection pool"*](../../022-User-Stories/Backlog/Story-Tenant-Id-And-RLS-Everywhere.md) | *"Hai request đồng thời từ hai tenant khác nhau tái sử dụng cùng một connection trong pool **không làm rò rỉ biến `app.current_tenant`** sang request kia"* | ⭐ Rò rỉ qua **connection pool** là một AC, không phải một lo ngại lý thuyết |

⇒ **Kết luận chính xác**: `SRS` (tầng requirement) **không** nói gì về cơ chế — phần đó `§7 G4` đúng. Nhưng **AC của Story đã giả định sẵn một cơ chế biến session (GUC) mang tên `app.current_tenant`**. ADR này **lấy tên biến từ AC *"fail-closed 0 row"*, không tự đặt**, và ghi nhận rằng phương án *"DB role riêng mỗi tenant"* **không chỉ bị loại vì đánh đổi** — nó làm chính AC *"fail-closed 0 row"* mất đối tượng để đo (xem [Alternatives (C)](#c-db-role-riêng-cho-mỗi-tenant)).

> [!NOTE]
> Brief của lô này nêu tên biến là `app.tenant_id`. **Nguồn sự thật là [Story AC *"fail-closed 0 row"*](../../022-User-Stories/Backlog/Story-Tenant-Id-And-RLS-Everywhere.md): `app.current_tenant`.** ADR này dùng tên trong Story. Chênh lệch đã báo PM ở `SUMMARY` của lô — nếu PM muốn đổi tên biến thì phải sửa Story trước, không phải sửa ADR.

### Những gì đã CHỐT

- `D-09` ([SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-NFR-01`): `tenant_id NOT NULL` mọi bảng nghiệp vụ · cột **đầu tiên** mọi composite index · **PostgreSQL RLS là lớp phòng thủ thứ hai** · shared DB + shared schema, ⛔ không schema-per-tenant, ⛔ không db-per-tenant.
- `D-10` ([SRS](../../020-Requirements/SRS-Comic-Studio.md) §3.E (khối `[!WARNING]`)): ⛔ **cấm** viết tenant isolation thành *"filter `tenant_id` ở tầng ứng dụng"*. Lý do nguyên văn: với **1 dev không có code review**, RLS **biến lỗi lập trình thành no-op thay vì rò rỉ dữ liệu chéo tenant**. Giới hạn đã biết: RLS **không** bảo vệ join thực hiện phía application.
- `D-02` ([SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-NFR-03`): worker là **process triển khai riêng**, cùng codebase, 2 entrypoint. ⛔ **Không có HTTP request** ở đường worker.
- `D-03` ([SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-FR-25`) + `D-42` ([SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-FR-26`): job queue trong Postgres; claim bằng `FOR UPDATE SKIP LOCKED`; câu CLAIM **phải chứa** `in_flight_per_tenant < N`.
- `ADR-005`: `job` nằm ở `public.job`, có `tenant_id`.

### Bốn câu hỏi thật sự mở

1. `SET LOCAL` (phạm vi transaction) hay `SET` (phạm vi session)?
2. Ai bơm, ở đâu trong vòng đời một request?
3. **Worker không có HTTP request thì lấy tenant ở đâu — và khoảng hở giữa lúc claim job và lúc set context xử lý thế nào?**
4. Bề mặt **không có tenant** (takedown intake, `M9` — *"không auth, không tenant context"* theo [findings §6.1](../../010-Planning/pm-runs/2026-08-28-phase-2-architecture-design-comic-studio/findings/architect.md)) thì làm gì?

### ⛔ Mâu thuẫn cứng phải giải, không phải chi tiết

`D-42` bắt câu CLAIM chứa `in_flight_per_tenant < N` ⇒ **`public.job` phải có `tenant_id`** ⇒ theo `D-09` nó là bảng có `tenant_id` và phải bật RLS ⇒ ([Story AC *"RLS bật trên 100% bảng có `tenant_id`"*](../../022-User-Stories/Backlog/Story-Tenant-Id-And-RLS-Everywhere.md) đo *"RLS bật trên 100% bảng có `tenant_id`"*).

Nhưng worker **chưa biết tenant** tại thời điểm claim — nó claim **chính là để biết**. Với RLS bật và context rỗng, theo hành vi fail-closed của AC *"fail-closed 0 row"*, worker thấy **0 row** và **không bao giờ claim được job nào**.

⇒ Đây là **deadlock thiết kế**. Không giải nó thì worker không chạy; giải sai thì mất toàn bộ giá trị `D-10` dựng lên.

---

## Decision

### D1. Cơ chế: GUC phạm vi **transaction**, tên `app.current_tenant`

```sql
SET LOCAL app.current_tenant = '<tenant_uuid>';
```

- ⭐ **`SET LOCAL`, ⛔ KHÔNG `SET`.** `SET LOCAL` chỉ sống trong transaction hiện tại và **tự hết hiệu lực ở `COMMIT` hoặc `ROLLBACK`** ⇒ điểm reset là tự động, không phụ thuộc việc ai đó nhớ gọi `RESET`. Đây chính là cơ chế thoả [Story AC *"⛔ không rò context qua connection pool"*](../../022-User-Stories/Backlog/Story-Tenant-Id-And-RLS-Everywhere.md) (không rò qua pool).
- ⛔ **Cấm `set_config('app.current_tenant', ..., false)`** (tham số thứ ba `false` = phạm vi session) — tương đương `SET`, mang đúng rủi ro rò rỉ.

### D2. Policy đọc context qua **một hàm helper duy nhất**, không đọc `current_setting` rải rác

Ràng buộc từ [Story AC *"fail-closed 0 row"*](../../022-User-Stories/Backlog/Story-Tenant-Id-And-RLS-Everywhere.md): biến **chưa set** *hoặc* **set giá trị không hợp lệ** đều phải cho **0 row**, ⛔ **không được ném exception**.

- `current_setting('app.current_tenant')` **ném lỗi** khi biến chưa set ⇒ vi phạm AC *"fail-closed 0 row"*.
- `current_setting('app.current_tenant', true)` trả `NULL` khi chưa set ⇒ thoả nửa đầu của AC *"fail-closed 0 row"*.
- Nhưng ép kiểu một chuỗi **không hợp lệ** sang `uuid` vẫn **ném lỗi** ⇒ vi phạm nửa sau của AC *"fail-closed 0 row"*.

⇒ **Quyết định**: đúng **một** hàm `public.current_tenant_id()` (theo `ADR-005`, hàm platform nằm ở `public`), `STABLE`, có xử lý ngoại lệ để **trả `NULL` thay vì ném** khi giá trị không ép kiểu được. Mọi policy viết theo đúng một dạng:

```sql
USING (tenant_id = public.current_tenant_id())
```

- `NULL` ⇒ so sánh cho `NULL` ⇒ row bị lọc ⇒ **0 row, không exception**. Thoả trọn AC *"fail-closed 0 row"*.
- Giữ được so sánh **cùng kiểu** (`uuid = uuid`) ⇒ index trên `tenant_id` vẫn dùng được. ⛔ **Không** viết policy dạng `tenant_id::text = current_setting(...)` — nó thoả AC *"fail-closed 0 row"* nhưng làm hỏng đúng cái index mà `D-09` bắt đặt `tenant_id` lên cột đầu.
- ⚠️ Chi phí thực thi của hàm có khối xử lý ngoại lệ **chưa được đo** ⇒ `TBD`. ⛔ Không gán số ([SRS](../../020-Requirements/SRS-Comic-Studio.md) §5.2). **Ai đóng**: Engineer, khi có bộ test tải đầu tiên (MVP0/MVP1). Đường lui nếu đo thấy đắt: validate định dạng ở tầng ứng dụng **trước** khi `SET LOCAL`, để hàm helper thành phép ép kiểu trần — nhưng ⛔ chỉ được làm sau khi có số đo, và ⛔ không được bỏ test của AC *"fail-closed 0 row"*.

### D3. Đường **API** — có HTTP request

Trình tự **bắt buộc**, đóng gói trong **đúng một** middleware/interceptor, không được lặp lại ở chỗ khác:

1. Xác thực request qua auth vendor (`D-12`, vendor `TBD` — `ADR-003`) ⇒ có `user_id`.
2. Phân giải `user_id` → `tenant_id` qua **`membership`** (`D-11`: dữ liệu nghiệp vụ trỏ `tenant_id`, ⛔ không trỏ `user_id`).
3. `BEGIN` — mở transaction tường minh.
4. `SET LOCAL app.current_tenant = <tenant_id>`.
5. Chạy handler **bên trong** transaction đó.
6. `COMMIT` / `ROLLBACK` ⇒ context tự biến mất.

⚠️ **Vòng lặp ở bước 2 — phải gọi tên**: để đọc `membership` cần tenant context, mà phải đọc `membership` mới biết tenant. Giải bằng **đúng một** hàm `SECURITY DEFINER` hẹp: nhận `user_id`, trả **duy nhất** `tenant_id`, ⛔ không trả gì khác, ⛔ không nhận tham số nào khác. Đây là **bề mặt đặc quyền duy nhất** của đường API và phải được review như code bảo mật.
⛔ Chi tiết policy RLS cho `tenant` / `user` / `membership` **không thuộc ADR này** — thuộc lô **DB Schema** (`ADR-005` [Q4](./ADR-005-Platform-Table-Schema-Placement.md)).

### D4. Đường **Worker** — ⛔ KHÔNG có HTTP request (đây là phần khó thật)

#### D4.1 Giải deadlock bằng một carve-out **hẹp, tường minh, một bảng**

- Worker chạy dưới **DB role riêng** `app_worker`.
- `app_worker` có **đúng một** đặc quyền thêm so với role API: **một cặp policy trên `public.job`** (và ⛔ chỉ trên bảng đó), xuyên tenant:

| Policy | Phạm vi row | ⚠️ Vì sao đúng phạm vi này |
|---|---|---|
| **`SELECT`** | Job ở trạng thái **claim được** **VÀ** job đang **in-flight** | ⭐ **Bắt buộc phải gồm cả in-flight.** `D-42` bắt câu CLAIM chứa `in_flight_per_tenant < N` ⇒ có một **subquery đếm job đang chạy** của tenant đó, và subquery ấy **cũng đi qua RLS**. Nếu policy chỉ lộ row *"claim được"*, phép đếm luôn trả **0**, điều kiện fairness **không bao giờ ràng buộc** — và nó hỏng **im lặng**, đúng failure mode mà [D4.3](#d43--khoảng-hở-giữa-claim-và-set-context--gọi-đúng-tên-nó) cảnh báo |
| **`UPDATE`** | ⛔ **Chỉ** job ở trạng thái **claim được** | Worker chỉ được **giành** job chưa ai giữ. ⛔ Không được sửa job đang in-flight của tenant khác — đọc để đếm là đủ, ⛔ không cần quyền ghi |
- ⛔ **TUYỆT ĐỐI KHÔNG cấp `BYPASSRLS` cho `app_worker`.** `BYPASSRLS` xoá RLS trên **mọi** bảng, ở đúng process phục vụ **nhiều tenant nhất** — nó huỷ chính xác thứ `D-10` tồn tại để dựng.
- ⛔ `app_worker` **không** có policy xuyên tenant trên bất kỳ **bảng nghiệp vụ** nào. Với bảng nghiệp vụ, nó chịu đúng cùng một policy như đường API.

#### D4.2 Trình tự bắt buộc — tất cả trong **MỘT** transaction

| Bước | Câu lệnh | Ghi chú |
|:--:|---|---|
| 1 | `BEGIN` | |
| 2 | `SELECT ... FROM public.job WHERE <claimable> AND <in_flight_per_tenant < N> ... FOR UPDATE SKIP LOCKED` | `D-03` + `D-42`; chạy dưới policy carve-out `D4.1` |
| 3 | `SET LOCAL app.current_tenant = <job.tenant_id>` | ⭐ **Statement KẾ TIẾP NGAY LẬP TỨC.** ⛔ Không statement nghiệp vụ nào chen giữa |
| 4 | Toàn bộ công việc + `INSERT generation` + `INSERT change_log` + `INSERT usage_event` (`KC-4`, `D-50`) | Chạy **sau** bước 3 ⇒ đã có context |
| 5 | `COMMIT` / `ROLLBACK` | `SET LOCAL` tự hết hiệu lực ⇒ worker quay lại vòng lặp ở trạng thái **không tenant**, là trạng thái an toàn mặc định |

⇒ Enqueue (`D-03`: `INSERT generation` + `INSERT job` cùng transaction) chạy ở đường API dưới context của tenant đó; claim chạy ở đường worker dưới carve-out. Hai đường không dùng chung role.

#### D4.3 ⚠️ Khoảng hở giữa claim và set context — gọi đúng tên nó

**Khoảng hở tồn tại**: từ sau bước 2 đến trước bước 3, session worker **đã giữ row `job` nhưng chưa có tenant context**. Nó dài **đúng một statement**.

**Trong khoảng đó chuyện gì xảy ra**:

- Mọi truy vấn vào bảng nghiệp vụ trả **0 row** (fail-closed theo [Story AC *"fail-closed 0 row"*](../../022-User-Stories/Backlog/Story-Tenant-Id-And-RLS-Everywhere.md)). ⇒ **An toàn về rò rỉ**: không có đường nào đọc được dữ liệu tenant khác.
- ⚠️ Nhưng nó **sai âm thầm**: code nhận được *"không có gì"* thay vì một lỗi ồn ào. Với một pipeline, *"không có gì"* dễ bị xử lý thành *"bỏ qua"* — hỏng dữ liệu mà không có alert. **Đây là failure mode nguy hiểm hơn rò rỉ ở chỗ nó không để lại dấu vết.**

⭐ **Rủi ro thật KHÔNG phải khoảng hở tự nó** — nó dài một statement và fail-closed. Rủi ro thật là **phản ứng của một dev khi gặp `0 row`**: cách "sửa" theo bản năng là **nới quyền role worker** (cấp `BYPASSRLS`, hoặc thêm policy xuyên tenant cho bảng nghiệp vụ). Làm vậy là xoá lớp phòng thủ mà `D-10` dựng lên, và **với 1 dev không code review thì không ai chặn giúp**. ⇒ Guardrail dưới đây **phải cưỡng chế được**, không được là lời khuyên.

#### D4.4 Bốn guardrail cưỡng chế được

| # | Guardrail | Cưỡng chế bằng |
|:--:|---|---|
| **W-1** | Chạy một truy vấn nghiệp vụ **ngay sau bước 2, trước bước 3** phải trả **0 row** | Test tự động — biến hành vi fail-closed từ *giả định* thành *test*. ⛔ Không để nó là niềm tin |
| **W-2** | Role `app_worker` **không** có `BYPASSRLS`; danh sách policy áp cho nó **đúng bằng** danh sách trong `D4.1` (**đúng một cặp** `SELECT`/`UPDATE`, chỉ trên `public.job`, đúng phạm vi row đã nêu) | Test CI: `pg_roles.rolbypassrls = false` cho `app_worker`; đối chiếu `pg_policies` với hằng số trong repo; lệch ⇒ CI đỏ |
| **W-2b** | Test **fairness thật sự ràng buộc**: seed một tenant có `N` job đang in-flight, gọi CLAIM ⇒ phải trả **0 job** của tenant đó | Test — chặn đúng kịch bản *"subquery đếm ra 0 nên `in_flight_per_tenant < N` luôn đúng"*. ⚠️ Chạy được sau khi **N** hết `TBD` |
| **W-3** | Giữa câu CLAIM (bước 2) và câu `SET LOCAL` (bước 3) ⛔ **không được có statement nào khác**. Cưỡng chế bằng cách gói hai bước vào **đúng một** hàm `claimJobAndBindTenant()` — đây là seam tương đương `resolveState()` của `D-04`: **một đường duy nhất, lint rule chặn mọi đường khác** | Lint rule ở CI (mẫu `D-04`, [SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-NFR-04`): ⛔ cấm mọi truy vấn trực tiếp vào `public.job` ngoài hàm đó |
| **W-4** | Sau `COMMIT`/`ROLLBACK`, `public.current_tenant_id()` phải trả `NULL` trên chính connection đó | Test — cùng bộ với [Story AC *"⛔ không rò context qua connection pool"*](../../022-User-Stories/Backlog/Story-Tenant-Id-And-RLS-Everywhere.md) |

#### D4.5 Một hướng làm khoảng hở bằng 0 — ⚠️ `TBD`, ⛔ chưa được giả định là chạy

Về lý thuyết có thể gộp bước 2 và 3 thành **một** statement (CTE claim + `set_config('app.current_tenant', ..., true)` lấy giá trị từ chính CTE đó), khi đó khoảng hở bằng 0.

⚠️ **Chưa verify.** Thứ tự đánh giá của `set_config` bên trong một CTE **không được PostgreSQL đảm bảo theo trực giác đọc từ trên xuống**, và một cơ chế bảo mật **không được xây trên hành vi không được đảm bảo**.

- **Ai đóng**: Engineer, ở MVP1, bằng một test thật.
- **Nếu verify PASS**: đây là hình thức mạnh hơn `W-1`…`W-3` (loại bỏ khoảng hở thay vì canh giữ nó) và ADR này phải được cập nhật.
- **Nếu verify FAIL hoặc chưa chạy**: `D4.2` + `W-1`…`W-4` là phương án hiệu lực. ⛔ Không được viết code dựa trên giả định nó chạy.

### D5. Connection pool

- `SET LOCAL` sống trong transaction ⇒ **`COMMIT`/`ROLLBACK` là điểm reset tự động**. Đây là **lý do chính** chọn `SET LOCAL` thay vì `SET`.
- ⇒ Cơ chế này **an toàn với cả session-mode lẫn transaction-mode pooling**. Một `SET` mức session thì **không** — nó dính vào connection và đi theo connection về pool.
- **Hệ quả bắt buộc**: ⭐ **mọi truy vấn chạm dữ liệu tenant phải nằm trong một transaction tường minh.** Query chạy ở chế độ autocommit **không** có context ⇒ trả 0 row. Chấp nhận có ý thức: fail-closed, đúng AC *"fail-closed 0 row"*.
- ⛔ **Cấm** `SET app.current_tenant` (không có `LOCAL`) và `set_config(..., false)` ở mọi nơi trong codebase — cưỡng chế bằng **lint/grep rule ở CI**. Một lần quên `RESET` là một lần rò tenant sang request kế tiếp dùng lại connection đó.
- Test [Story AC *"⛔ không rò context qua connection pool"*](../../022-User-Stories/Backlog/Story-Tenant-Id-And-RLS-Everywhere.md) (hai tenant xen kẽ trên cùng pool) là **AC đã có sẵn** — không cần đặt thêm chỉ tiêu, chỉ cần chạy.

### D6. Bề mặt **không có tenant** — takedown intake (`M9`)

Công cụ tiếp nhận takedown là **công khai, không cần tài khoản** (`D-54`, [SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-FR-38`) ⇒ **không có tenant để bơm**.

- Đường này chạy dưới role riêng `app_public_intake`, quyền **chỉ** `INSERT` vào `public.takedown_request` (`ADR-005`).
- ⛔ **Không** giải bằng cách cho đường này bypass RLS, và ⛔ **không** cho nó `SELECT` bất kỳ bảng nghiệp vụ nào.
- ⇒ **Quy tắc chung**: cơ chế bơm context ⛔ **không được giả định mọi session DB đều có tenant**. Ba loại session tồn tại hợp lệ: **có tenant** (API, worker sau bước 3), **không tenant nhưng có carve-out hẹp** (worker ở bước 2, intake), và **owner/migration**.

### D7. Migration và vận hành

Migration chạy dưới **role owner riêng**, tách khỏi `app_api` / `app_worker` / `app_public_intake`. ⛔ Role ứng dụng không có quyền DDL — đây cũng là điều kiện để `G-1` của `ADR-005` (`REVOKE CREATE ON SCHEMA public`) có nghĩa.

> [!WARNING]
> `D-09` gọi RLS là **lớp phòng thủ thứ hai**. ⇒ Code ứng dụng **vẫn phải** viết `WHERE tenant_id = ...`; RLS ⛔ **không thay thế** nó. Lý do: `D-10` ghi rõ RLS **không** bảo vệ join thực hiện phía application ([SRS](../../020-Requirements/SRS-Comic-Studio.md) §3.E (khối `[!WARNING]`)). Đọc ADR này thành *"có RLS rồi nên khỏi filter"* là hiểu ngược.

---

## Alternatives considered

### (A) `SET LOCAL app.current_tenant` (phạm vi transaction) — ⭐ ĐÃ CHỌN

**Điểm mạnh**: reset tự động ở ranh giới transaction ⇒ thoả AC *"⛔ không rò context qua connection pool"* **bằng cơ chế**, không bằng kỷ luật; tương thích cả hai chế độ pooling; một dòng SQL, không có DDL per tenant; policy đọc qua một hàm ⇒ có đúng một chỗ để review.

**Điểm yếu**: buộc **mọi** truy vấn phải trong transaction tường minh; phụ thuộc vào việc middleware/`claimJobAndBindTenant()` là **đường duy nhất** — nếu ai đó mở connection thẳng thì không có gì set context (⇒ trả 0 row, fail-closed, nhưng im lặng).

### (B) `SET` mức session + `RESET` / `DISCARD ALL` thủ công khi trả connection về pool

**⛔ Loại vì**:

1. **Một lần quên reset = một lần rò tenant.** Chi phí bảo trì rơi đúng vào chỗ [SRS](../../020-Requirements/SRS-Comic-Studio.md) §3.E (khối `[!WARNING]`) mô tả là điểm yếu của dự án này: *"1 dev không có code review"*. Cơ chế phải chịu được việc con người quên — `SET LOCAL` chịu được, `SET` thì không.
2. **Không dùng được với transaction-mode pooling**: một connection vật lý phục vụ nhiều transaction của nhiều tenant, biến session không đi theo transaction.
3. Nó là phương án **dễ trượt [Story AC *"⛔ không rò context qua connection pool"*](../../022-User-Stories/Backlog/Story-Tenant-Id-And-RLS-Everywhere.md) nhất** — mà AC *"⛔ không rò context qua connection pool"* là AC đã ký, không phải mong muốn.

### (C) DB role riêng cho **mỗi tenant**

**Nội dung**: `CREATE ROLE tenant_<id>` mỗi khi tạo tenant; policy so `current_user`; kết nối bằng role tương ứng hoặc `SET ROLE`.

**Điểm mạnh — ghi nhận trung thực**: cưỡng chế ở **tầng kết nối**, không phụ thuộc kỷ luật code. Về mặt lý thuyết đây là mô hình mạnh nhất trong ba phương án.

**⛔ Lý do loại — bốn tầng**:

1. ⭐ **Nó làm AC *"fail-closed 0 row"* mất đối tượng đo.** [Story AC *"fail-closed 0 row"*](../../022-User-Stories/Backlog/Story-Tenant-Id-And-RLS-Everywhere.md) đo *"một session **không set biến `app.current_tenant`**"* — câu này chỉ có nghĩa nếu tồn tại một biến session. Chọn (C) ⇒ phải **sửa AC của một Story đã duyệt ở Phase 1**. Đây là **lý do loại mạnh nhất**, và nó **verify được**, không phải suy đoán về đánh đổi.
2. **Vận hành không chịu nổi ở sản phẩm self-serve**: mỗi lần đăng ký tenant là một thao tác **DDL** (`CREATE ROLE` + `GRANT`) trong đường đăng ký người dùng. Pool phải phân mảnh theo role (mỗi role một pool con) ⇒ số connection tăng theo số tenant.
3. **Không giải được đường worker.** Worker vẫn phải claim job **xuyên tenant** rồi mới biết đóng vai role nào ⇒ vẫn cần đúng carve-out của `D4.1`, cộng thêm một `SET ROLE` giữa transaction. Nó **thêm** một bề mặt đặc quyền, không **bớt**.
4. **Nhu cầu mà (C) phục vụ đã bị hoãn khỏi horizon.** Cô lập mạnh mức kết nối là nhu cầu enterprise; `D-08` / `SRS-NFR-26` hoãn SSO/SAML, team nhiều thành viên có role, custom domain / white-label, multi-region khỏi horizon ([SRS](../../020-Requirements/SRS-Comic-Studio.md) §6.3, hàng `SRS-NFR-26`).

**Đường quay lại nếu cần**: nếu ngày nào có một tenant enterprise yêu cầu cô lập tầng kết nối, (C) áp được **cho riêng tenant đó** mà không cần bỏ (A) — hai cơ chế cùng tồn tại vì policy có thể kiểm cả `current_user` lẫn `public.current_tenant_id()`. Ghi lại để không ai coi (A) là cánh cửa đóng vĩnh viễn.

### (D) Bơm context ở **tầng connection pool** (pooler/proxy tự set biến theo credential của connection)

**⛔ Loại vì**: (i) đẩy một quyết định bảo mật ra một thành phần hạ tầng **chưa được chọn** — hosting/PaaS còn `TBD` (`ADR-002`, [SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-NFR-07`); (ii) để pooler biết tenant thì connection phải mang danh tính tenant ⇒ **suy biến về (C)** và thừa kế trọn bốn vấn đề của (C); (iii) đặt lớp bảo vệ vào một tiến trình mà test của [Story AC *"⛔ không rò context qua connection pool"*](../../022-User-Stories/Backlog/Story-Tenant-Id-And-RLS-Everywhere.md) không chạm tới được từ tầng ứng dụng.

### (E) Cấp `BYPASSRLS` cho role worker (hoặc cho role ứng dụng)

**⛔ Loại thẳng.** Nó xoá lớp phòng thủ `D-09`/`D-10` dựng lên, ở đúng process phục vụ nhiều tenant nhất, để đổi lấy việc tiết kiệm **một** câu `SET LOCAL`. Ghi ở đây **không phải** vì nó là ứng viên, mà vì nó là cách "sửa" mà một dev gặp `0 row` sẽ tìm tới đầu tiên — và `W-2` tồn tại để làm CI đỏ khi ai đó làm vậy.

### (F) Không RLS, chỉ filter `tenant_id` ở tầng ứng dụng

**⛔ Không phải một phương án**: `D-10` ([SRS](../../020-Requirements/SRS-Comic-Studio.md) §3.E (khối `[!WARNING]`)) **cấm tường minh**. Ghi ở đây chỉ để đóng cửa, tránh một run sau mở lại.

---

## Consequences

### Tích cực

- ⭐ **27 file `DB-Entity-*` / `Endpoint-*` ở lô sau có một khuôn duy nhất để chép**: mọi bảng có `tenant_id` khai policy dạng `USING (tenant_id = public.current_tenant_id())`; mọi endpoint khai *"chạy trong một transaction đã có `app.current_tenant`"*.
- Rò rỉ qua pool được chặn **bằng cơ chế** (`SET LOCAL` tự hết hạn), không bằng kỷ luật.
- Trạng thái mặc định của mọi session là **không có tenant** ⇒ mọi lỗi thiếu context biểu hiện thành **0 row**, không thành rò rỉ. Đúng phát biểu của `D-10`: *"biến lỗi lập trình thành no-op"*.
- Bề mặt đặc quyền của toàn hệ thống rút về **ba điểm đếm được**: hàm `SECURITY DEFINER` phân giải `user → tenant` (`D3`), policy carve-out trên `public.job` (`D4.1`), role intake chỉ-INSERT (`D6`). Ba điểm này review được trong một buổi.
- `KC-4` (`D-50`) không bị ảnh hưởng: cả ba `INSERT` nằm sau bước 3, trong cùng transaction đã có context.

### Tiêu cực — chi phí thật

- **Mọi truy vấn phải trong transaction tường minh.** Kể cả read đơn lẻ. Đây là ràng buộc lan khắp codebase và không có ngoại lệ.
- **Fail-closed là con dao hai lưỡi.** Thiếu context ⇒ `0 row` ⇒ **không có alert**. Bug biểu hiện thành *"dữ liệu trống"* chứ không thành *"lỗi"*, khó debug hơn. `W-1` biến hành vi này thành test, nhưng ⛔ không xoá được bản chất khó chịu của nó.
- **Khoảng hở ở worker tồn tại thật** (`D4.3`) và chỉ được canh giữ bằng `W-1`…`W-4`, không bị loại bỏ — trừ khi `D4.5` verify PASS.
- **Một policy carve-out xuyên tenant tồn tại trên `public.job`.** Nó hẹp, nhưng nó tồn tại, và nó là chỗ duy nhất trong hệ thống mà một câu SELECT nhìn thấy nhiều tenant. ⇒ Phải nằm trong danh sách review bảo mật cố định.
- **Chi phí thực thi của `public.current_tenant_id()` chưa đo** ⇒ mọi ước lượng hiệu năng của lô sau không được coi khoản này bằng 0.
- **Thêm ba DB role** (`app_api`, `app_worker`, `app_public_intake`) + role owner ⇒ cấu hình kết nối phức tạp hơn một chuỗi connection string duy nhất; đụng `ADR-002` (hosting) khi cấu hình secret.

### Việc còn để `TBD` — ⛔ không được bịa

| Việc | Vì sao không quyết ở đây | Ai đóng | Khi nào |
|---|---|---|:--|
| **N** của `in_flight_per_tenant < N` | ⛔ **Không con số nào trong repo** ([SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-FR-26`); [SRS](../../020-Requirements/SRS-Comic-Studio.md) §5.2 cấm tự gán số | PM + Architect | Sau khi MVP0 đo tải thật |
| Verify kỹ thuật `D4.5` (CTE + `set_config` một statement) | Cơ chế bảo mật không xây trên hành vi chưa được đảm bảo | Engineer | MVP1, bằng test thật |
| Chi phí thực thi hàm helper `D2` | Chưa có bộ test tải | Engineer | MVP0/MVP1 |
| Policy RLS cho `tenant` / `user` / `membership` | Thuộc mô hình dữ liệu, không thuộc cơ chế bơm context | Architect (lô DB Schema) | Trước khi `DB-Entity-Tenant.md` duyệt |
| Vendor auth (nguồn của `user_id` ở `D3` bước 1) | `SRS-NFR-08` = `TBD` ([SRS](../../020-Requirements/SRS-Comic-Studio.md) §3.E) | `ADR-003` | Lô ADR-001…004 (song song) |
| Tải khác của queue trong horizon (rollup `usage_daily`, extraction, composite preview/export — [findings §7 G5](../../010-Planning/pm-runs/2026-08-28-phase-2-architecture-design-comic-studio/findings/architect.md)): chạy dạng **job per tenant** (⇒ hợp `D4.2` nguyên trạng) hay cần một read carve-out riêng | Architect (lô DB Schema) | Khi đặc tả `DB-Entity-Job.md` / `DB-Entity-Usage-Daily.md` |
| Chế độ pooling cụ thể (session-mode hay transaction-mode) | Phụ thuộc hosting, `SRS-NFR-07` = `TBD` ([SRS](../../020-Requirements/SRS-Comic-Studio.md) §3.E) | `ADR-002` | Lô ADR-001…004 (song song) — ⭐ **`SET LOCAL` an toàn với cả hai**, nên quyết định này **không bị chặn** bởi ADR-002 |

---

## Đã quyết ở đâu

| Quyết định | Mã `D-xx` | Nguồn (file + mã requirement) |
|---|:--:|---|
| RLS là lớp phòng thủ thứ hai · `tenant_id NOT NULL` mọi bảng nghiệp vụ · cột đầu mọi composite index · shared DB + shared schema | `D-09` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-NFR-01` |
| ⛔ Cấm tenant isolation bằng filter tầng ứng dụng; RLS biến lỗi lập trình thành no-op; RLS ⛔ không bảo vệ join phía application | `D-10` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) §3.E (khối `[!WARNING]`) |
| `tenant` / `user` / `membership` ba entity riêng; dữ liệu nghiệp vụ trỏ `tenant_id`, ⛔ không trỏ `user_id` | `D-11` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-FR-01` |
| Mua auth, ⛔ không tự viết (vendor `TBD`) | `D-12` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-FR-03` · `SRS-NFR-08` |
| Worker là **process triển khai riêng**, cùng codebase, 2 entrypoint ⇒ ⛔ không có HTTP request | `D-02` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-NFR-03` |
| Job queue trong Postgres; claim `FOR UPDATE SKIP LOCKED`; transactional enqueue | `D-03` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-FR-25` |
| Câu CLAIM phải chứa `in_flight_per_tenant < N`; **N = `TBD`** | `D-42` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-FR-26` · §5.2 |
| Lint rule cưỡng chế seam ở CI (mẫu áp dụng cho `W-3`) | `D-04` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-NFR-04` |
| **`KC-4`** — `generation` + `change_log` + `usage_event` cùng một transaction | `D-50` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-NFR-13` |
| Takedown công khai, ⛔ không cần tài khoản ⇒ bề mặt không tenant | `D-54` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-FR-38` |
| Hoãn khỏi horizon: SSO/SAML · team nhiều thành viên có role · custom domain / white-label · multi-region · fine-tune riêng từng tenant | `D-08` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-NFR-26` (§6.3) |
| ⛔ Không tự gán số cho hàng `TBD` | — | [SRS](../../020-Requirements/SRS-Comic-Studio.md) §5.2 |
| **Tên biến `app.current_tenant`** + hành vi **fail-closed 0 row**, ⛔ không exception | *(chưa có mã `D-xx`)* | [Story-Tenant-Id-And-RLS-Everywhere](../../022-User-Stories/Backlog/Story-Tenant-Id-And-RLS-Everywhere.md) **AC *"fail-closed 0 row"*** |
| ⛔ Không rò `app.current_tenant` qua connection pool dùng lại | *(chưa có mã `D-xx`)* | [Story-Tenant-Id-And-RLS-Everywhere](../../022-User-Stories/Backlog/Story-Tenant-Id-And-RLS-Everywhere.md) **AC *"⛔ không rò context qua connection pool"*** |
| RLS bật + ≥1 policy trên 100% bảng có `tenant_id` | — | [Story-Tenant-Id-And-RLS-Everywhere](../../022-User-Stories/Backlog/Story-Tenant-Id-And-RLS-Everywhere.md) AC *"RLS bật trên 100% bảng có `tenant_id`"* |
| Bảng platform (gồm `job`) nằm ở `public` | — | [ADR-005](./ADR-005-Platform-Table-Schema-Placement.md) |
| ⛔ **CHƯA quyết ở Phase 1**: cơ chế bơm tenant context | — | [findings/architect §7 G4](../../010-Planning/pm-runs/2026-08-28-phase-2-architecture-design-comic-studio/findings/architect.md) |
