---
id: ADR-018
type: adr
status: draft
project: comic-studio
created: 2026-08-29
---

# ADR-018: Mô hình `usage_event` và rollup `usage_daily`

Related to: [SDD-Comic-Studio](./SDD-Comic-Studio.md)

> [!IMPORTANT]
> **ADR record-only** — ghi lại `D-58`, `D-59`, `D-64`. ⛔ Không mở lại quyết định nào.
> ⚠️ **Một xung đột đã biết được GHI NHẬN và ROUTE đi, ⛔ ADR này KHÔNG giải** — xem [Consequences → xung đột `TBD-USAGE-VLM`](#-xung-đột-tbd-usage-vlm--ghi-nhận-và-route-đi-adr-này-không-giải).

---

## Context

### ⭐ Vì sao đo sớm là quyết định kiến trúc, ⛔ không phải việc của analytics

Anchor gốc của `D-58` (`CF-8.6`, dẫn qua [Story-Usage-Event-And-Daily-Rollup](../../022-User-Stories/Backlog/Story-Usage-Event-And-Daily-Rollup.md) mục 3): ⭐ ***"đo muộn nghĩa là định giá trong bóng tối hàng tháng"***.

Và nó ⛔ **không backfill được**: [Story-Generation-Cost-And-Model-Metadata](../../022-User-Stories/Backlog/Story-Generation-Cost-And-Model-Metadata.md) mục 3 dẫn Epic cha — *"Thiếu `cost_usd`/`model_id`/`model_version`/`attempt_no` từ đầu ⇒ COGS phải **ước lượng lại vĩnh viễn**"*.

⇒ Hai dữ liệu này là **đầu vào cứng của gate `G2`** (gate kinh tế sau MVP1):

| Tiêu chí `G2` | Cần gì | Ai cung cấp |
|---|---|---|
| **`G2-a`** | Regen ratio **p50 và p90** có giá trị **thực đo** từ `usage_daily`, trên **≥1 chapter hoàn chỉnh**. ⭐ ***"Không có dữ liệu ⇒ `G2` không chạy được, ⛔ không phải 'tạm PASS'"*** | `D-58` — exit criterion **`M1-7`** |
| **`G2-b`, `G2-c`** | Gross margin tính từ **COGS thực đo** — *"COGS lấy từ tổng `generation.cost_usd` thực, ⛔ **không** từ ước lượng"* | `D-59` |

### Quyết định đã CHỐT — ⛔ ADR này ghi lại, không mở lại

| Nội dung | Mã | Nguồn (mã requirement) | Độ rắn |
|---|:--:|---|:--:|
| `usage_event` **append-only** + rollup `usage_daily`; billing/metric là **hàm tổng hợp trên event thô**, ⛔ **không** counter tăng tại chỗ. **Regen ratio là metric first-class**, đo **p50/p90** từ MVP0. ⭐ Một lần best-of-N (N=3) tạo **đúng 3** `usage_event` row | `D-58` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) **`SRS-FR-30`** · `MVP-Scope §3 F1` · [Story-Usage-Event-And-Daily-Rollup](../../022-User-Stories/Backlog/Story-Usage-Event-And-Daily-Rollup.md) mục 4 | **CHỐT** |
| `cost_usd` + `model_id` + `model_version` + `attempt_no` trên **MỌI** `generation`, từ **generation ĐẦU TIÊN** — ⛔ dữ liệu lịch sử **không backfill được** | `D-59` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) **`SRS-FR-31`** · `MVP-Scope §3 F2` | **CHỐT** |
| ⛔ **Đừng dựa vào cache để cứu margin.** ⭐ Hai chỗ ra tiền thật là **reference-sheet amortization** và **idempotency** | `D-64` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) **`SRS-NFR-12`** · §5.2 | **CHỐT** |
| **N = 3** là mặc định cho **MỌI** panel (best-of-N), ⚠️ ⛔ **KHÔNG phải retry-on-failure** ⇒ mỗi panel tiêu tài nguyên **3 lần**, ⛔ không phải 1 | `D-37` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-FR-20` · `Charter §7 C8` `[OFF]` | **LAI** — N=3 `MẶC ĐỊNH` |

### Những gì ADR khác ĐÃ chốt — ⛔ không quyết lại

| Đã chốt ở đâu | Nội dung |
|---|---|
| [ADR-005](./ADR-005-Platform-Table-Schema-Placement.md) mục `Q1` | `public.usage_event`, `public.usage_daily` — schema `public`; tên đủ điều kiện bắt buộc (`G-3`) |
| ⭐ [ADR-017](./ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md) mục `Q4` | **`KC-4`** — `usage_event` là một trong ba bảng của transaction bất khả phân; `GR-2` (FK chống mồ côi), `GR-3` (append-only bằng `REVOKE`). ⛔ ADR này **không đặc tả lại `KC-4`** |
| [ADR-017](./ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md) mục `Q4.5` | ⚠️ **`TBD` về thứ tự gắn `usage_event` / `cost_usd` trong vòng đời job** — cùng một `TBD`, cùng một người đóng, cùng một file |
| [ADR-006](./ADR-006-RLS-Tenant-Context-Injection.md) | RLS + `tenant_id` (`KC-5`) — ⛔ không đặc tả lại |
| [ADR-007](./ADR-007-VLM-Provider-For-QA-Select.md) mục `Q8` | ⭐ **Cùng xung đột** với mục [`TBD-USAGE-VLM`](#-xung-đột-tbd-usage-vlm--ghi-nhận-và-route-đi-adr-này-không-giải) dưới đây — ⚠️ **hai ADR route về hai TÊN FILE khác nhau**, phải hợp nhất |
| [ADR-015](./ADR-015-Job-Queue-In-Postgres.md) mục `Q2` | ⚠️ `job.attempt_count` (hạ tầng) ⛔ **khác** `generation.attempt_no` (kinh tế/provenance) |
| [ADR-016](./ADR-016-Image-Provider-Adapter-And-Version-Pinning.md) | Adapter là nơi `cost_usd` / `model_id` / `model_version` **thực đo** được sinh ra |

---

## Decision

### Q1. `usage_event` là **append-only**, và append-only được cưỡng chế ở **tầng DB**

⛔ **Không có đường code nào và ⛔ không có quyền DB nào cho phép `UPDATE` / `DELETE` một dòng `usage_event` đã ghi.**

Phép đo (AC đã ký, [Story-Usage-Event-And-Daily-Rollup](../../022-User-Stories/Backlog/Story-Usage-Event-And-Daily-Rollup.md) mục 4): thử `UPDATE`/`DELETE` trực tiếp một dòng đã tồn tại ⇒ **bị từ chối ở tầng DB** (permission/constraint), ⛔ không dòng nào bị sửa hay biến mất.

⇒ Cơ chế là **`REVOKE UPDATE, DELETE`** khỏi mọi DB role ứng dụng — chính là guardrail **`GR-3`** của [ADR-017](./ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md) mục `Q4.6`. ⛔ ADR này **không** định nghĩa lại nó, chỉ ghi nhận rằng `usage_event` nằm dưới guardrail đó.

⭐ **Lý do append-only ⛔ không phải "cho an toàn"**: `Glossary` mục `usage_event` (dẫn qua [Story-Usage-Event-And-Daily-Rollup](../../022-User-Stories/Backlog/Story-Usage-Event-And-Daily-Rollup.md) mục 3): ***"Append-only là ĐIỀU KIỆN để nó dùng được làm căn cứ đối soát."*** Một bảng sửa được ⛔ không đối soát được với ai.

### Q2. Billing/metric là **hàm tổng hợp trên event thô** — ⛔ không counter tăng tại chỗ

| ✅ Được | ⛔ Cấm |
|---|---|
| `usage_daily` là **rollup dẫn xuất**, tính lại được từ `usage_event` | ⛔ Counter `UPDATE ... SET n = n + 1` ở bất kỳ đâu |
| Mọi số billing/metric là kết quả **truy vấn tổng hợp** trên event thô | ⛔ Lưu tổng như một trạng thái tự trị, ⛔ không truy nguyên được |

⇒ **Thuộc tính có được**: mọi con số công bố đều **truy về được** tới danh sách event sinh ra nó. ⚠️ Đây là điều kiện để `G2` chạy bằng **số thực** thay vì bằng niềm tin.

**`usage_daily` cho ra `p50` và `p90` regen ratio** của đúng ngày đó, tính từ `usage_event` của ngày đó — exit criterion **`M1-7`**.

⚠️ **Rollup lỗi phải NÓI RA là lỗi.** [Story-Usage-Event-And-Daily-Rollup](../../022-User-Stories/Backlog/Story-Usage-Event-And-Daily-Rollup.md) (unhappy path): rollup job crash giữa chừng ⇒ ngày đó **đánh dấu rõ là *"rollup thiếu/lỗi"***, ⛔ **KHÔNG được hiển thị ngầm định là regen ratio = 0**. ⭐ Vì `0` là một giá trị **trông rất tốt** — nó sẽ được đọc thành *"⛔ không ai regen"* thay vì *"chúng ta ⛔ không biết"*. ⇒ **`NULL`/trạng thái lỗi tường minh, ⛔ không bao giờ `0` ngầm định.** Cùng nguyên tắc với `cost_usd` khi provider timeout ([Q4](#q4-bốn-trường-bắt-buộc-trên-mọi-generation-d-59)).

### Q3. Idempotency key — chống đếm trùng

**Mỗi `usage_event` mang một idempotency key.** Cùng một sự kiện được gửi/ghi 2 lần do retry ở tầng gọi (network timeout, worker retry) ⇒ **`usage_daily` chỉ tính MỘT lần**.

Phép đo (AC đã ký, [Story-Usage-Event-And-Daily-Rollup](../../022-User-Stories/Backlog/Story-Usage-Event-And-Daily-Rollup.md) mục 4, unhappy path): gửi 2 lần cùng một sự kiện có **idempotency key giống nhau** ⇒ `usage_daily` chỉ tính 1 lần.

⭐ **Đây ⛔ KHÔNG phải một tối ưu — nó là ràng buộc đúng đắn**, vì [ADR-015](./ADR-015-Job-Queue-In-Postgres.md) mục `Q4.3` chốt job queue là **at-least-once**: lease hết hạn ⛔ không chứng minh worker đã chết ⇒ một job **sẽ** chạy lại. ⛔ Không có idempotency key thì mỗi lần chạy lại là một lần **đếm phồng chi phí** — và số phồng đó đi thẳng vào `G2`.

⚠️ **Song hành với `D-64`**: idempotency là ⭐ **một trong hai chỗ ra tiền thật** ([Q6](#q6--đừng-dựa-vào-cache-để-cứu-margin-d-64)).

⛔ **Hình dạng key (thành phần cấu tạo, `UNIQUE` constraint hay ràng buộc khác) = `TBD`, lô DB Schema đóng.** Nguồn chỉ nói *"có idempotency key"*, ⛔ không nói nó gồm gì.

### Q4. Bốn trường bắt buộc trên **MỌI** `generation` (`D-59`)

| Trường | Ràng buộc | Ghi chú |
|---|---|---|
| `cost_usd` | **thực đo** tại thời điểm generation **hoàn tất** | ⛔ **Không** phải ước lượng trước khi gọi |
| `model_id` | Model **THỰC SỰ được gọi** | ⛔ Không phải model dự kiến — provider có thể tự fallback ([ADR-016](./ADR-016-Image-Provider-Adapter-And-Version-Pinning.md)) |
| `model_version` | Ghi **riêng biệt**, ⛔ **không ghi đè** khi provider trả version khác dưới cùng `model_id` | Là dữ liệu để truy vết **silent model drift** |
| `attempt_no` | Tăng dần theo số lần gọi lại trong **cùng một logical generation request** | ⚠️ ⛔ **KHÔNG** phải `job.attempt_count` — [ADR-015](./ADR-015-Job-Queue-In-Postgres.md) mục `Q2` |

**Cả 4 trường ⛔ không NULL** trên mọi dòng phát sinh sau mốc triển khai (AC đã ký).

⚠️ **Ràng buộc `C8` — ⛔ không được gộp**: mỗi candidate trong 3 candidate của best-of-N phải có **dòng `generation` + `cost_usd` + `attempt_no` RIÊNG của chính nó**; ⛔ **không** gộp chi phí 3 candidate vào 1 dòng ([Story-Generation-Cost-And-Model-Metadata](../../022-User-Stories/Backlog/Story-Generation-Cost-And-Model-Metadata.md) mục 4).

⚠️ **Provider lỗi/timeout TRƯỚC khi trả cost** ⇒ dòng `generation` **vẫn được tạo**, với `cost_usd` ở **trạng thái rõ ràng là CHƯA BIẾT** — ⛔ **không phải `NULL` âm thầm, ⛔ không phải `0` ngầm định**, và ⛔ **không** bị bỏ sót hoàn toàn khỏi hệ thống. Hình dạng của *"trạng thái tường minh"* (cột phụ hay sentinel) = **`TBD`, lô DB Schema**.

### Q5. Ba `usage_event` cho một panel — và cái phải ghi **trước khi biết kết quả**

`D-37` chốt **N=3 cho MỌI panel** và ⚠️ ⛔ **không phải retry-on-failure** ⇒ mỗi panel tiêu tài nguyên **3 lần**, ⛔ **không phải 1**.

⇒ AC đã ký: *"Một lần sinh panel bằng best-of-N (N=3) tạo ra **đúng 3** `usage_event` row, mỗi row ứng với 1 candidate — đo bằng `COUNT(*)` = 3."*

⭐ **Và ba dòng đó phải được ghi TRƯỚC khi biết kết quả VLM-select** ([Story-Usage-Event-And-Daily-Rollup](../../022-User-Stories/Backlog/Story-Usage-Event-And-Daily-Rollup.md), unhappy path): VLM-select thất bại/timeout **sau khi cả 3 candidate đã sinh** (tài nguyên **đã tiêu**) ⇒ `usage_event` của cả 3 vẫn được ghi, ⛔ **không** bị bỏ sót vì lý do *"candidate không được chọn"*.

⇒ **Nguyên tắc**: `usage_event` ghi **việc tiêu tài nguyên đã xảy ra**, ⛔ **không phải** việc *"kết quả có dùng được không"*. Tiền đã tiêu là tiền đã tiêu.

⚠️ **Chống cộng dồn hai lần**: hai dòng `generation` tạo trùng do lỗi client-side (double submit) ⇒ tổng `cost_usd` dùng để tính COGS ⛔ **không được cộng dồn 2 lần** cho cùng một lần tiêu tài nguyên thực tế ([Story-Generation-Cost-And-Model-Metadata](../../022-User-Stories/Backlog/Story-Generation-Cost-And-Model-Metadata.md), unhappy path) — đây là mặt thứ hai của [Q3](#q3-idempotency-key--chống-đếm-trùng).

### Q6. ⛔ Đừng dựa vào cache để cứu margin (`D-64`)

⛔ **Cache ⛔ KHÔNG phải chiến lược margin.** Căn cứ: `CF-6.13` `[EM]` — hit rate chỉ **vài % → ~10%**, và ⭐ **`architect` TỰ KHAI đó là ước lượng** ⇒ [SRS](../../020-Requirements/SRS-Comic-Studio.md) §5.2 xếp *"Cache hit rate"* vào bảng `TBD` với ghi chú ⛔ ***"không dùng làm chỉ tiêu"*** (`R-17`).

⭐ **Hai chỗ ra tiền thật** ([SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-NFR-12`):

| # | Chỗ ra tiền thật | Vì sao thật |
|:--:|---|---|
| 1 | **Reference-sheet amortization** | Chi phí dựng reference sheet trải trên **nhiều** panel dùng lại nó ⇒ tiết kiệm là **cấu trúc**, ⛔ không phụ thuộc trùng lặp ngẫu nhiên |
| 2 | ⭐ **Idempotency** | ⛔ Không trả tiền hai lần cho **cùng một** lần tiêu tài nguyên — xem [Q3](#q3-idempotency-key--chống-đếm-trùng). Đây là **tiết kiệm chắc chắn**, ⛔ không phải xác suất |

⇒ **Quy tắc cho mọi file sau**: ⛔ **không tài liệu nào được đưa cache hit rate vào một phép tính margin, ⛔ không đặt nó thành chỉ tiêu nghiệm thu, và ⛔ không dùng nó làm lý do hoãn một hạng mục đo lường.** Nếu một ước lượng margin cần cache mới PASS, thì ước lượng đó **chưa PASS**.

### Q7. Ranh giới — ADR này ⛔ KHÔNG quyết cái gì

| ⛔ Không quyết | Ai quyết |
|---|---|
| ⭐ **`KC-4`** | [ADR-017](./ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md) mục `Q4` — ⛔ nguồn duy nhất |
| Vị trí schema của `usage_event` / `usage_daily` | [ADR-005](./ADR-005-Platform-Table-Schema-Placement.md) mục `Q1` |
| RLS / `tenant_id` (`KC-5`) | [ADR-006](./ADR-006-RLS-Tenant-Context-Injection.md) |
| DDL, hình dạng idempotency key, cấu trúc `usage_daily`, cách đánh dấu *"rollup lỗi"* | Architect, lô **DB Schema** |
| ⭐ **Mô hình đếm chi phí VLM** | ⛔ **`TBD-USAGE-VLM`** — route sang lô DB Schema, xem dưới |
| **Credit ledger / HOLD / hold reaper / hard quota** (`D-60`, `D-61`, `KC-7`) | `ADR-019` — `[OoH]` MVP3. ⚠️ Nhưng `D-62` cấm retrofit **ba tầng giá** ⇒ schema phải **chừa chỗ ngay** |
| Tính/công bố gross margin, chạy gate `G2` | **Founder tại đúng thời điểm gate** — [Story-Usage-Event-And-Daily-Rollup](../../022-User-Stories/Backlog/Story-Usage-Event-And-Daily-Rollup.md) mục 4 nói rõ Story chỉ cung cấp **dữ liệu đầu vào** |
| UI hiển thị usage cho end-user | ⛔ **Không có yêu cầu này trong nguồn** ở horizon hiện tại |
| Chính sách purge/retention cho `usage_event` append-only | PM + luật sư — [SRS](../../020-Requirements/SRS-Comic-Studio.md) §5.2 (`b-3`) |

---

## Alternatives considered

### (a) Counter tăng tại chỗ (`UPDATE ... SET n = n + 1`) thay vì event thô — ⛔ LOẠI (Phase 1 đã loại)

**Điểm mạnh phải ghi nhận trung thực**: một dòng thay vì hàng triệu dòng; đọc số hiện tại là một lần `SELECT` rẻ; ⛔ không cần rollup job, ⛔ không cần lo bảng phình.

**⛔ Vì sao LOẠI**: `D-58` chốt *"billing/metric là **hàm tổng hợp trên event thô**, ⛔ **không** counter tăng tại chỗ"* ([SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-FR-30`). Lý do: một counter ⛔ **không trả lời được câu hỏi *"con số này gồm những gì"***. Khi `G2` hỏi *"regen ratio p90 là bao nhiêu"*, counter chỉ có **tổng** — ⛔ không có phân phối, ⛔ không có p50/p90, ⛔ không đối soát được. Và counter ⛔ **không** append-only ⇒ mất luôn tính *"căn cứ đối soát"*. ⚠️ Retrofit từ counter sang event là **không backfill được**: lịch sử đã bị nén thành một số.

### (b) `usage_event` cho phép `UPDATE` để sửa số liệu sai — ⛔ LOẠI

**Điểm mạnh**: sửa được lỗi ghi nhầm mà ⛔ không phải viết event bù.

**⛔ Vì sao LOẠI**: append-only là **điều kiện** để bảng dùng được làm căn cứ đối soát (`Glossary`), và AC đã ký đo bằng *"`UPDATE`/`DELETE` bị từ chối ở **tầng DB**"*. Một bảng đối soát mà sửa được thì bên kia bàn đàm phán ⛔ không có lý do gì tin nó. ⇒ Sửa sai bằng **event bù** (compensating event), ⛔ không bằng `UPDATE`. Đây cũng là guardrail `GR-3` của [ADR-017](./ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md) — cấp lại quyền `UPDATE` là gỡ luôn guardrail của `KC-4`.

### (c) Gộp 3 candidate của một panel thành **1** `usage_event` (và 1 `generation`) — ⛔ LOẠI

**Điểm mạnh**: bảng nhỏ hơn 3 lần; `COUNT(*)` theo panel đơn giản; rollup rẻ hơn.

**⛔ Vì sao LOẠI**: vi phạm **thẳng** ràng buộc `C8` và AC đã ký của **cả hai** Story (`F1` và `F2`). Sâu hơn: N=3 là **mặc định cho MỌI panel**, ⛔ **không phải retry-on-failure** ⇒ gộp lại sẽ làm người đọc số hiểu nhầm rằng một panel = một lần tiêu tài nguyên, đúng **cách khoản chi phí ×3 biến mất khỏi mô hình tài chính**. Và `attempt_no` mất nghĩa hoàn toàn.

### (d) Tính regen ratio **trực tiếp** từ `usage_event` mỗi lần cần, bỏ `usage_daily` — ⛔ LOẠI

**Điểm mạnh**: ⛔ không có bảng dẫn xuất ⇒ ⛔ không có nguy cơ lệch giữa rollup và event thô; ⛔ không có rollup job để crash.

**⛔ Vì sao LOẠI**: `D-58` chốt **cả hai** — event thô **và** rollup `usage_daily`. `M1-7` phát biểu đúng theo `usage_daily` (*"`usage_daily` có p50/p90 regen ratio ⇒ `G2` chạy được"*). Về kỹ thuật: p50/p90 trên toàn bộ lịch sử event là truy vấn **ngày càng đắt** trên một bảng **tăng vô hạn**, chạy ngay trên database nghiệp vụ đã phải phục vụ câu CLAIM job ([ADR-015](./ADR-015-Job-Queue-In-Postgres.md)). ⇒ Rollup là **ranh giới tách tải phân tích khỏi tải nghiệp vụ**, ⛔ không phải tối ưu sớm.

### (e) Dựa vào **cache** để kéo margin về mục tiêu — ⛔ LOẠI (Phase 1 đã loại)

**Điểm mạnh**: nếu hit rate cao, đây là khoản tiết kiệm ⛔ không cần đổi gì trong sản phẩm.

**⛔ Vì sao LOẠI**: `D-64` ([SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-NFR-12`) cấm thẳng, và con số duy nhất tồn tại là `[EM]` **vài % → ~10%** do chính lens `architect` **tự khai là ước lượng** ⇒ [SRS](../../020-Requirements/SRS-Comic-Studio.md) §5.2 xếp vào `TBD` với ghi chú ⛔ *"không dùng làm chỉ tiêu"*. Xây một mô hình margin trên một con số ước lượng chưa đo là **đúng loại sai số** mà `D-59` (cost thực đo) tồn tại để thay thế.

### (f) Ghi `usage_event` **sau khi** biết candidate nào được chọn — ⛔ LOẠI

**Điểm mạnh**: bảng chỉ chứa những gì *"thật sự dùng"*, số liệu trông sạch hơn.

**⛔ Vì sao LOẠI**: vi phạm AC unhappy-path đã ký — VLM-select timeout **sau khi 3 candidate đã sinh** thì tài nguyên **đã tiêu**, và cả 3 dòng vẫn phải có. ⛔ Ghi sau nghĩa là mọi lần VLM lỗi sẽ **xoá sạch chi phí thật khỏi sổ sách** — và VLM lỗi là một trạng thái hợp lệ, ⛔ không phải ngoại lệ hiếm.

---

## Consequences

### ⛔ Hệ quả BẮT BUỘC ĐỌC — chi phí và con số COGS

⚠️ **Mọi con số COGS trong repo đang thiếu chi phí VLM.** [SRS](../../020-Requirements/SRS-Comic-Studio.md) §4.3 và §5.2: chi phí VLM call để score N candidate là phần **CHƯA TÍNH** của `CF-3.5`. [SRS](../../020-Requirements/SRS-Comic-Studio.md) §5.1 + `CẤM-04`: **`$12,06`/chapter là SÀN, ⛔ KHÔNG phải trần**.
⇒ ⛔ Bỏ nhãn này khi nhân một ước lượng là lỗi mà [SRS](../../020-Requirements/SRS-Comic-Studio.md) §1.2 gọi là ***"rửa sạch khoảng trống"***.

### ⭐ Xung đột `TBD-USAGE-VLM` — GHI NHẬN và ROUTE đi, ADR này KHÔNG giải

> [!CAUTION]
> ⛔ **Đây là một `TBD` được route, ⛔ KHÔNG phải một quyết định.** ADR này ⛔ **không chọn lời giải**.

**Xung đột, phát biểu đầy đủ:**

| Vế | Nội dung | Nguồn |
|:--:|---|---|
| **A** | AC **đã ký**: *"một lần sinh panel best-of-N (N=3) tạo ra **đúng 3** `usage_event` row, mỗi row ứng với 1 candidate — đo bằng **`COUNT(*)` = 3**"* | [Story-Usage-Event-And-Daily-Rollup](../../022-User-Stories/Backlog/Story-Usage-Event-And-Daily-Rollup.md) mục 4 |
| **B** | Chi phí **VLM call** (chấm N candidate) là **chi phí THẬT**, và là phần **CHƯA TÍNH** của `CF-3.5` ⇒ nó phải **đo được** | [SRS](../../020-Requirements/SRS-Comic-Studio.md) §4.3, §5.2 · [findings §7 G7](../../010-Planning/pm-runs/2026-08-28-phase-2-architecture-design-comic-studio/findings/architect.md) |

⇒ **Va chạm**: nếu VLM call ghi thêm một `usage_event` row cho **cùng panel đó**, `COUNT(*)` thành **4** ⇒ **AC vế A FAIL**. Nếu ⛔ không ghi, thì **chi phí VLM biến mất** ⇒ vi phạm vế B.

**⭐ Ràng buộc KÉP bắt buộc mang theo cho người giải:**

1. ✅ **AC vế A phải PASS** — nó là artefact Phase 1 **đã ký**; đổi nó phải **qua PM**, ⛔ không phải qua lô Schema tự quyết.
2. ✅ **Chi phí VLM ⛔ KHÔNG ĐƯỢC BIẾN MẤT** — ⛔ *"không đo"* ⛔ **không phải** một lời giải. Đó chính là cách khoản chi phí này biến mất khỏi mô hình tài chính **lần thứ hai**.

| Hạng mục | Nội dung |
|---|---|
| **Ai đóng** | **Architect, ở lô DB Schema** |
| **Ở đâu** | ⭐ [`DB-Entity-Provenance-And-Usage.md`](../Schema/DB-Entity-Provenance-And-Usage.md) — tên file chuẩn theo [findings/architect §3.5](../../010-Planning/pm-runs/2026-08-28-phase-2-architecture-design-comic-studio/findings/architect.md) |
| **Khi nào** | **Trước khi** file đó được duyệt |
| **Hướng cần cân nhắc** — ⛔ **CHƯA CHỌN** | (i) thêm cột phân loại để `COUNT(*)` của AC lọc theo loại candidate · (ii) bảng đo riêng cho VLM · (iii) sửa AC (⇒ **bắt buộc qua PM**) |

> [!WARNING]
> ⚠️⚠️ **LỆCH TÊN FILE PHẢI HỢP NHẤT — ⛔ đừng để lô DB Schema vấp.**
> [ADR-007](./ADR-007-VLM-Provider-For-QA-Select.md) mục `Q8` route **CÙNG MỘT** xung đột này, nhưng ghi tên đích là **`DB-Entity-Usage-Event.md`**.
> [findings/architect §3.5](../../010-Planning/pm-runs/2026-08-28-phase-2-architecture-design-comic-studio/findings/architect.md) chốt tên file là ⭐ **`DB-Entity-Provenance-And-Usage.md`** (gộp `change_log`, `field_provenance`, `usage_event`, `usage_daily`) — ⛔ **không có** file `DB-Entity-Usage-Event.md` trong danh sách entity đề xuất.
> ⇒ ⭐ **`TBD-USAGE-VLM` là MỘT hàng, ⛔ không phải hai.** Đích đúng là **`DB-Entity-Provenance-And-Usage.md`**.
> ⚠️ ADR này ⛔ **không sửa** [ADR-007](./ADR-007-VLM-Provider-For-QA-Select.md) (ngoài quyền sở hữu của lô này) ⇒ **ghi nhận lệch tên ở đây**, và **ai đóng**: Architect ở lô DB Schema **phải hợp nhất hai hàng thành một** trước khi giải.

### Tích cực

- **`G2` chạy được bằng số thực** — `G2-a` từ `usage_daily`, `G2-b`/`G2-c` từ tổng `generation.cost_usd`, ⛔ không từ ước lượng.
- **Mọi con số truy nguyên được** về danh sách event sinh ra nó ⇒ đối soát được với provider và với khách hàng.
- **Append-only + idempotency** cho một sổ sách **⛔ không đếm trùng và ⛔ không sửa lén** — hai thuộc tính mà một mô hình counter ⛔ không có.
- **Dữ liệu drift có sẵn**: `model_id` + `model_version` trên mọi generation cho phép truy vết khi nghi ngờ ([ADR-016](./ADR-016-Image-Provider-Adapter-And-Version-Pinning.md)).
- ⭐ **`D-64` chặn sẵn một lối thoát giả**: khi margin không đẹp, cám dỗ đầu tiên là hứa hẹn cache. Quyết định này ⛔ đóng lối đó **trước khi** áp lực xuất hiện.

### Tiêu cực — chi phí thật

- **`usage_event` tăng vô hạn.** N=3 cho **MỌI** panel, 1 chapter @N=3 = **180 ảnh** `[EM]` ⇒ **180 dòng/chapter/tenant** chỉ riêng ảnh. ⚠️ [SRS](../../020-Requirements/SRS-Comic-Studio.md) §5.2 (`b-3`): append-only **tăng vô hạn nếu ⛔ không có chính sách purge**, mà retention lại là **câu hỏi pháp lý** chờ luật sư.
- **`usage_daily` là dữ liệu dẫn xuất** ⇒ có thể lệch với event thô nếu rollup lỗi. Bù bằng yêu cầu *"rollup lỗi phải nói ra là lỗi"* — nhưng đó là **quy trình cộng đánh dấu**, ⛔ không phải cơ chế tự chữa.
- **Idempotency key là nghĩa vụ thường trực** đặt lên **mọi** điểm ghi `usage_event` sau này, ⛔ không phải việc làm một lần.
- ⚠️ **`usage_event` nằm trong transaction nóng của `KC-4`** ⇒ 3 dòng cho mỗi panel đi vào cùng transaction với artifact. Đây là chi phí **đã chấp nhận** ở [ADR-017](./ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md), ⛔ không phải thứ được nới ở đây.
- **Hai khái niệm "attempt" cùng tồn tại** (`generation.attempt_no` vs `job.attempt_count`) ⇒ chỗ dễ gộp nhầm nhất, và gộp nhầm là **làm sai COGS**.

### Việc còn để `TBD` — ⛔ không được bịa

| `TBD` | Ai đóng | Khi nào |
|---|---|---|
| ⭐ **`TBD-USAGE-VLM`** — mô hình đếm chi phí VLM vs AC `COUNT(*) = 3`; ⚠️ kèm **hợp nhất lệch tên file** với [ADR-007](./ADR-007-VLM-Provider-For-QA-Select.md) `Q8` | **Architect (lô DB Schema)** | Trước khi [`DB-Entity-Provenance-And-Usage.md`](../Schema/DB-Entity-Provenance-And-Usage.md) được duyệt |
| **Chi phí VLM per-call** và tổng khoản thiếu của `CF-3.5` — ⛔ không có số trong repo | PM + Architect | Sau đo MVP0 |
| Thứ tự gắn `usage_event` / `cost_usd` trong vòng đời job — ⚠️ **cùng một `TBD`** với [ADR-017](./ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md) mục `Q4.5` | Architect (lô DB Schema) | Cùng mốc trên |
| Hình dạng **idempotency key**; cấu trúc `usage_daily`; cách đánh dấu *"rollup thiếu/lỗi"*; cách biểu diễn `cost_usd` *"chưa biết"* | Architect (lô DB Schema) | Cùng mốc trên |
| **Regen ratio p50/p90 thực tế** — ⭐ *"biến quyết định của cả mô hình tài chính, MVP0 phải đo"* | Engineer đo, PM đọc | MVP0 → `M1-7` |
| **Cache hit rate** — `[EM]` vài % → ~10%, ⛔ **không dùng làm chỉ tiêu** | ⛔ **Không ai** *"chốt"* — chỉ đo | MVP0 |
| Chính sách **purge / retention** cho `usage_event` — ⚠️ câu hỏi **pháp lý** | PM + luật sư SHTT | Trước khi bảng đủ lớn để thành vấn đề vận hành |
| Chỗ chừa cho **ba tầng giá** (`D-62` cấm retrofit) và cho credit ledger (`D-60`, `[OoH]` MVP3) | Architect (lô DB Schema) + `ADR-019` | Trước khi lô DB Schema được duyệt |

---

## Đã quyết ở đâu

| Quyết định | Mã `D-xx` | Nguồn (file + mã requirement) |
|---|:--:|---|
| `usage_event` **append-only** + rollup `usage_daily`; billing/metric là **hàm tổng hợp trên event thô**, ⛔ không counter tăng tại chỗ; **regen ratio là metric first-class** (p50/p90 từ MVP0) | `D-58` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) **`SRS-FR-30`** · `MVP-Scope §3 F1` |
| ⭐ Một lần best-of-N (N=3) tạo **đúng 3** `usage_event` row (đo bằng `COUNT(*)`); append-only **cưỡng chế ở tầng DB**; **idempotency key** chống đếm trùng; **rollup lỗi phải nói ra là lỗi**, ⛔ không hiển thị `0` | `D-58` | [Story-Usage-Event-And-Daily-Rollup](../../022-User-Stories/Backlog/Story-Usage-Event-And-Daily-Rollup.md) mục 4 (*"Xác minh được"* + *"unhappy path"*) |
| ⭐ *"Append-only là **ĐIỀU KIỆN** để nó dùng được làm **căn cứ đối soát**"* | `D-58` | `Glossary` mục `usage_event`, dẫn qua [Story-Usage-Event-And-Daily-Rollup](../../022-User-Stories/Backlog/Story-Usage-Event-And-Daily-Rollup.md) mục 3 |
| ⭐ *"Đo muộn nghĩa là **định giá trong bóng tối hàng tháng**"* (`CF-8.6`) | `D-58` | [Story-Usage-Event-And-Daily-Rollup](../../022-User-Stories/Backlog/Story-Usage-Event-And-Daily-Rollup.md) mục 3 |
| Exit criterion **`M1-7`**: `usage_daily` có p50/p90 regen ratio ⇒ `G2` chạy được; **`G2-a`**: ⛔ *"không có dữ liệu ⇒ `G2` **không chạy được**, ⛔ không phải 'tạm PASS'"* | `D-58` | `Roadmap §2` + `MVP-Scope §7.3`, dẫn qua [Story-Usage-Event-And-Daily-Rollup](../../022-User-Stories/Backlog/Story-Usage-Event-And-Daily-Rollup.md) mục 3 |
| `cost_usd` + `model_id` + `model_version` + `attempt_no` trên **MỌI** generation, từ generation **ĐẦU TIÊN**; ⛔ **không backfill được** | `D-59` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) **`SRS-FR-31`** · `MVP-Scope §3 F2` |
| `cost_usd` **thực đo** lúc hoàn tất; `model_id` là model **thực sự được gọi**; `model_version` khác ⇒ **ghi riêng biệt, ⛔ không ghi đè**; `attempt_no` tăng dần; provider lỗi ⇒ cost ở **trạng thái tường minh**, ⛔ không `NULL` âm thầm / `0` ngầm định | `D-59` | [Story-Generation-Cost-And-Model-Metadata](../../022-User-Stories/Backlog/Story-Generation-Cost-And-Model-Metadata.md) mục 4 |
| **`G2-b`/`G2-c`**: *"COGS lấy từ tổng `generation.cost_usd` **thực**, ⛔ **không** từ ước lượng"* | `D-59` | `MVP-Scope §7.3`, dẫn qua [Story-Generation-Cost-And-Model-Metadata](../../022-User-Stories/Backlog/Story-Generation-Cost-And-Model-Metadata.md) mục 3 |
| ⛔ **Đừng dựa vào cache để cứu margin**; ⭐ hai chỗ ra tiền thật: **reference-sheet amortization** + **idempotency** | `D-64` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) **`SRS-NFR-12`** |
| **Cache hit rate** chỉ có `[EM]` vài % → ~10%, `architect` **tự khai là ước lượng** ⇒ ⛔ **không dùng làm chỉ tiêu** (`R-17`) | `D-64` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) §5.2 |
| **N = 3** mặc định cho **MỌI** panel, ⚠️ ⛔ **không phải retry-on-failure**; ⛔ mỗi candidate phải có `generation` + `cost_usd` + `attempt_no` **riêng**, ⛔ không gộp (`C8`) | `D-37` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-FR-20` · §5.1 · `Charter §7 C8` `[OFF]` |
| ⭐ **`KC-4`** — `usage_event` nằm trong transaction bất khả phân với `generation` + `change_log`; guardrail `GR-2` (FK), `GR-3` (append-only bằng `REVOKE`) | `D-50` | [ADR-017](./ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md) mục `Q4` — ⛔ **nguồn duy nhất**, ADR này không đặc tả lại |
| `public.usage_event` / `public.usage_daily` ở schema **`public`**; tên đủ điều kiện bắt buộc | `D-01` (hệ quả) | [ADR-005](./ADR-005-Platform-Table-Schema-Placement.md) mục `Q1` |
| Job queue **at-least-once** ⇒ idempotency là **điều kiện đúng đắn**, ⛔ không phải tối ưu | `D-03` | [ADR-015](./ADR-015-Job-Queue-In-Postgres.md) mục `Q4.3` |
| ⚠️ `generation.attempt_no` ⛔ **khác** `job.attempt_count` | `D-59` | [ADR-015](./ADR-015-Job-Queue-In-Postgres.md) mục `Q2` |
| ⛔ Chi phí VLM là phần **CHƯA TÍNH** của `CF-3.5`; **`$12,06`/chapter là SÀN, ⛔ không phải trần** (`CẤM-04`); ⛔ bỏ nhãn = *"rửa sạch khoảng trống"* | — | [SRS](../../020-Requirements/SRS-Comic-Studio.md) §4.3 · §5.2 · §5.1 · §1.2 · [findings §7 G7](../../010-Planning/pm-runs/2026-08-28-phase-2-architecture-design-comic-studio/findings/architect.md) |
| ⭐ Cùng xung đột `COUNT(*)=3` vs chi phí VLM đã được route ở **[ADR-007](./ADR-007-VLM-Provider-For-QA-Select.md) mục `Q8`** — ⚠️ **lệch tên file đích, phải hợp nhất** | — | [ADR-007](./ADR-007-VLM-Provider-For-QA-Select.md) `Q8` vs [findings/architect §3.5](../../010-Planning/pm-runs/2026-08-28-phase-2-architecture-design-comic-studio/findings/architect.md) |
| Kiến trúc billing/ledger/onboarding đỡ **BA tầng ngay từ đầu, ⛔ không retrofit** | `D-62` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) **`SRS-FR-32`** |
| Credit ledger append-only + **HOLD 3 credit/panel trước enqueue** + `CHECK(available >= 0)` tầng DB + hold reaper — `[OoH]` MVP3 | `D-60` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) **`SRS-FR-28`** · §3.F · `MVP-Scope §6 KC-7` |
| `usage_event` append-only **tăng vô hạn** nếu ⛔ không có purge; retention là **câu hỏi pháp lý** | — | [SRS](../../020-Requirements/SRS-Comic-Studio.md) §5.2 (`b-3`) |
| **Regen ratio p50/p90 thực tế** là *"biến quyết định của cả mô hình tài chính, MVP0 phải đo"* | — | [SRS](../../020-Requirements/SRS-Comic-Studio.md) §5.2 |
| ⛔ **Không tự gán số** cho hàng `TBD` | — | [SRS](../../020-Requirements/SRS-Comic-Studio.md) §5.2 |

---

_Created by system-architect_
_Author: trisjr_
