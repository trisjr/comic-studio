---
id: ADR-017
type: adr
status: draft
project: comic-studio
created: 2026-08-29
---

# ADR-017: Chuỗi provenance và MỘT transaction boundary (`KC-4`)

Related to: [SDD-Comic-Studio](./SDD-Comic-Studio.md)

> [!IMPORTANT]
> **ADR này là NGUỒN DUY NHẤT của `KC-4`.** [findings/architect §3.5](../../010-Planning/pm-runs/2026-08-28-phase-2-architecture-design-comic-studio/findings/architect.md) ghi thẳng: invariant `KC-4` **cắt ngang** `DB-Entity-Generation.md` và `DB-Entity-Provenance-And-Usage.md` ⇒ *"đặt nó ở **ADR-017** (nguồn duy nhất) và để hai file schema **trỏ tới**, ⛔ **không copy nội dung** — tránh tạo nguồn sự thật thứ hai."*
> ⇒ Mọi file DB Schema / API / Security cần `KC-4` **phải trỏ về [mục Q4](#q4-kc-4--đặc-tả-chuẩn-để-file-khác-trỏ-tới)**, ⛔ không đặc tả lại.

---

## Context

### ⭐ Đây là quyết định PHÁP LÝ trước khi là quyết định kỹ thuật

⛔ **Lý do tồn tại của cả ADR này KHÔNG phải *"cho nhất quán dữ liệu"*.** Nhất quán dữ liệu là **hệ quả phụ**. Lý do chính là:

**NĐ 134/2026/NĐ-CP, Điều 5a** `[OFF]` (`CF-7.2` / `CF-7.3`, dẫn qua [Story-Provenance-Chain-Parent-Generation](../../022-User-Stories/Backlog/Story-Provenance-Chain-Parent-Generation.md) mục 3): tác phẩm AI-assisted **chỉ** được bảo hộ nếu con người có *"substantial and decisive intellectual contribution to the creative process"*; tác phẩm do AI tạo hoàn toàn **không được bảo hộ**. Kèm theo là nghĩa vụ **lưu prompts, inputs, intermediate drafts**.

Ba mệnh đề nối tiếp — đọc liền mạch:

1. **Prompt một mình KHÔNG chứng minh được *"decisive contribution"*.** ([SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-FR-35`). Cái chứng minh được là **chuỗi lựa chọn của con người**: chọn generation X thay vì Y, sửa thoại, đổi camera, kéo bubble, export.
2. ⇒ Bằng chứng nằm ở `KC-1` (chuỗi lineage) + `KC-2` (`change_log`) + `KC-3` (`field_provenance` + `origin`) — **cả ba, không phải một**.
3. ⇒ **`KC-4`**: nếu ba thứ đó có thể thiếu **ngẫu nhiên** so với artifact chúng chứng minh, thì chúng **không phải bằng chứng**. [SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-NFR-13` viết đúng câu này: *"Bằng chứng có thể thiếu ngẫu nhiên thì không phải bằng chứng."*

**Hậu quả khi hỏng — nêu thẳng, không giảm nhẹ**: mất `KC-2`/`KC-4` là **mất bảo hộ bản quyền** cho những artifact bị hụt bằng chứng, **vĩnh viễn** — vì [Story-Provenance-Chain](../../022-User-Stories/Backlog/Story-Provenance-Chain-Parent-Generation.md) mục 3 (`Valuable-I`) ghi rõ **không backfill được**: mọi generation quá khứ giữ `parent = NULL` mãi mãi, và một `change_log` row đã không được ghi thì không có nguồn nào tái tạo lại nó. Đây là lý do `KC-1`…`KC-4` nằm trong `MVP-Scope §6` — **danh sách không mở ra thương lượng scope**.

⚠️ **Một transaction rollback ở đây không phải "mất một dòng log". Nó là một artifact có thể bán được, mà chủ nhân không chứng minh được quyền tác giả.**

### Quyết định đã CHỐT — ⛔ ADR này ghi lại, không mở lại

| Nội dung | Mã | `KC` | Nguồn (mã requirement) |
|---|:--:|:--:|---|
| `parent_generation_id` (**nullable FK**) + `relation_kind ENUM('retry','variation','refine','continuity_fix')` — từ **MIGRATION SỐ 1**, không phải backlog. ⛔ **Không backfill được** | `D-47` | `KC-1` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-FR-34` · [Story-Provenance-Chain](../../022-User-Stories/Backlog/Story-Provenance-Chain-Parent-Generation.md) AC-1 |
| `change_log` **append-only** ghi **MỌI** hành động người dùng — kể cả *"chọn generation X thay vì Y"*, sửa thoại, đổi camera, kéo bubble, **export**. ⭐ *"Prompt một mình không chứng minh được decisive contribution"* | `D-48` | `KC-2` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-FR-35` · §3.D · §4.1 |
| `field_provenance` ở **mức FIELD** + `generation.origin ENUM('ai','ai_edited','human')` | `D-49` | `KC-3` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-FR-36` |
| ⭐ **`KC-1` + `KC-2` + `KC-3` phải commit CÙNG MỘT TRANSACTION với artifact mà chúng chứng minh**: `INSERT generation` + `INSERT change_log` + `INSERT usage_event` **bất khả phân** | `D-50` | `KC-4` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-NFR-13` · [Story-Provenance-Committed-In-Same-Transaction](../../022-User-Stories/Backlog/Story-Provenance-Committed-In-Same-Transaction.md) |
| **Guardrail tầng DB**: mọi `INSERT` vào `generation` **thiếu `origin` phải FAIL ở tầng DB**, ⛔ không phải chỉ cảnh báo ở tầng ứng dụng | `D-51` | — | [SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-NFR-14` · [Story-Provenance-Chain](../../022-User-Stories/Backlog/Story-Provenance-Chain-Parent-Generation.md) AC-2 |
| ⛔ **KHÔNG UI duyệt CÂY generation** (tree view / diff / branch-merge) — flat list theo `created_at` + `approved_generation_id` là đủ. ⚠️ **Cắt UI, KHÔNG cắt cột dữ liệu** | `D-56` | — | [SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-NFR-23` |

### Những gì ADR khác ĐÃ chốt và ADR này ⛔ KHÔNG quyết lại

| Đã chốt ở đâu | Nội dung | ADR này dùng nó thế nào |
|---|---|---|
| [ADR-005](./ADR-005-Platform-Table-Schema-Placement.md) mục `Q1` | `change_log`, `field_provenance`, `usage_event`, `usage_daily` nằm ở schema **`public`** (`public.change_log`, `public.usage_event`…) | Là **tiền đề** của [Q4.4](#q44-kc-4-là-transaction-span-nhiều-schema--và-đó-không-phải-vấn-đề) |
| [ADR-005](./ADR-005-Platform-Table-Schema-Placement.md) mục Alternatives `(c)` | Lý do ⛔ **loại** phương án rải `change_log` theo module chủ sở hữu — nó phá *"một `change_log` duy nhất"* và qua đó phá **điều kiện kiểm chứng** của `KC-4` | Trích dẫn, ⛔ không lập luận lại |
| `D-01` / `D-05` ([SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-NFR-02`, `SRS-NFR-21`) | Modular monolith **1 process · 1 PostgreSQL · 3 schema** `story`/`comic`/`generation`; ⛔ **không** microservices, ⛔ **không** 2 PostgreSQL — lý do nêu thẳng là **2 DB = mất transaction boundary (`KC-4`)** | Là **điều kiện cần** của [Q4.3](#q43-commit-cùng-transaction-nghĩa-là-gì--năm-thuộc-tính-kiểm-chứng-được) |
| [ADR-006](./ADR-006-RLS-Tenant-Context-Injection.md) | RLS + cơ chế bơm tenant context (`app.current_tenant`, phạm vi transaction); ba DB role | `change_log` cũng phải có `tenant_id` và tuân RLS như mọi bảng khác (`KC-5`) — ⛔ ADR này không đặc tả lại RLS |
| `D-44` ([SRS](../../020-Requirements/SRS-Comic-Studio.md) §3.A) | Mục tiêu bảng `generation` là **auditability + lineage**, ⛔ **không phải reproducibility**; `seed` là provenance metadata, ⛔ không phải replay key | Là lý do ADR này không yêu cầu bất kỳ đảm bảo *"tái sinh ra đúng ảnh cũ"* nào |

---

## Decision

### Q1. Chuỗi lineage (`KC-1`) — hình dạng chốt

`generation` mang **hai** trường quan hệ, có mặt từ **migration số 1**:

| Trường | Kiểu | Nullable | Ý nghĩa |
|---|---|:--:|---|
| `parent_generation_id` | FK → `generation.id` | ✅ **có** | Generation gốc mà bản này dẫn xuất từ. `NULL` = **generation đầu chuỗi**, ⛔ **không phải lỗi dữ liệu** |
| `relation_kind` | `ENUM('retry','variation','refine','continuity_fix')` | theo `parent` | Bản chất của quan hệ dẫn xuất |

⛔ **Bốn giá trị enum là danh sách đóng của Phase 1** ([SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-FR-34`). Thêm giá trị thứ 5 là **mở lại `D-47`** ⇒ phải qua ADR mới, không phải qua migration lặng lẽ.

⚠️ **`relation_kind = 'continuity_fix'` phải trỏ được về generation gốc.** [Story-Provenance-Chain](../../022-User-Stories/Backlog/Story-Provenance-Chain-Parent-Generation.md) (unhappy path) bắt chặn record mồ côi nghiệp vụ **ở tầng ứng dụng trước khi tạo record** — hình dạng ràng buộc cụ thể (`CHECK` hay validation) thuộc lô DB Schema.

### Q2. `change_log` (`KC-2`) — phạm vi ghi và điểm cưỡng chế

**Ghi MỌI hành động của người dùng**, gồm cả loại hành động mà một dev sẽ theo bản năng coi là *"không phải thay đổi dữ liệu"*: **chọn generation X thay vì Y**, sửa thoại, đổi camera, kéo bubble, **export** ([SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-FR-35`, §3.D, §4.1).

⭐ **Điểm cưỡng chế là MỘT middleware/hook ở tầng service, ⛔ không phải kỷ luật của từng developer.** [Story-Change-Log-On-Every-Editor-Action](../../022-User-Stories/Backlog/Story-Change-Log-On-Every-Editor-Action.md) đặt AC đúng chỗ này: mọi endpoint ghi của editor đi qua **cùng một** middleware `change_log`, và endpoint nào ghi dữ liệu mà bỏ qua middleware **làm test FAIL**. Lý do kiến trúc: `bus factor = 1`, ⛔ **không có code review** (`CF-1.2` `[CHỐT]`, dẫn qua [SRS](../../020-Requirements/SRS-Comic-Studio.md) §2.2) — guardrail phải là **cơ chế**, không phải quy trình.

`change_log` là **append-only** và có `tenant_id` (`KC-5`). ⛔ ADR này không định nghĩa danh mục `action_type`; nó bị chặn bởi *"⛔ không tự phát minh thêm `action_type` ngoài các hành động mà 4 Story editor thực sự có"* ⇒ **`TBD`, lô DB Schema đóng**.

### Q3. `field_provenance` + `origin` (`KC-3`) — mức FIELD, không phải mức row

| Thành phần | Mức | Ràng buộc |
|---|---|---|
| `generation.origin` | **row** (`generation`) | `ENUM('ai','ai_edited','human')`, **`NOT NULL`** ⇒ xem [Q5](#q5-guardrail-tầng-db-cho-origin-d-51) |
| `field_provenance` | ⭐ **field** | Một field bị người dùng sửa tay mang `origin = 'human'` / `'ai_edited'` **cho đúng field đó**, ⛔ không phải cho toàn bộ generation |

⭐ **Vì sao mức field, không phải mức row**: [Story-Provenance-Chain](../../022-User-Stories/Backlog/Story-Provenance-Chain-Parent-Generation.md) mục 6 nói thẳng — *"có `parent_generation_id` mà thiếu `field_provenance` ⇒ **không xác định được ranh giới phần được bảo hộ**"*. Điều 5a bảo hộ **phần đóng góp của con người**; nếu chỉ biết *"row này đã bị người sửa"* thì ranh giới đó không vẽ được. ⇒ `KC-1` và `KC-3` **không cắt rời được** — cắt thành hai lô cho ra **hai lô đều không đủ** chứng minh Điều 5a.

⚠️ **Race**: hai request tạo generation đồng thời cho cùng một panel ⛔ **không được ghi đè `field_provenance` của nhau** — cả hai dòng phải tồn tại. Đây là ràng buộc **đọc cùng** [Q4.3](#q43-commit-cùng-transaction-nghĩa-là-gì--năm-thuộc-tính-kiểm-chứng-được) thuộc tính `P-2`.

---

### Q4. `KC-4` — đặc tả chuẩn để file khác TRỎ tới

> **Đây là mục mà `DB-Entity-Generation.md`, `DB-Entity-Provenance-And-Usage.md` và các file `Endpoint-*` sẽ trích dẫn.** Nó được viết để **tự đủ**: ai đọc riêng mục Q4 phải biết chính xác phải làm gì và phải test gì, ⛔ không cần đọc thêm file khác.

#### Q4.1 Phát biểu chuẩn (normative)

> **`KC-4`** — Với **mỗi** artifact `generation` được hệ thống tạo ra, bản thân artifact đó và **toàn bộ bằng chứng chứng minh nó** phải đi vào database trong **MỘT** transaction PostgreSQL **duy nhất**: hoặc **tất cả** cùng commit, hoặc **không dòng nào** tồn tại. ⛔ **Không có trạng thái trung gian nào là hợp lệ.**

#### Q4.2 Chính xác những bảng nào

| # | Bảng (tên đủ điều kiện) | Schema | Vai trò trong transaction | Bắt buộc? |
|:--:|---|:--:|---|:--:|
| 1 | `generation.generation` | `generation` | **Artifact** — thứ được chứng minh. Mang `KC-1` (`parent_generation_id`, `relation_kind`) và `KC-3` (`origin`) | ✅ **luôn** |
| 2 | `public.change_log` | `public` | **`KC-2`** — hành động của con người dẫn tới artifact này | ✅ **khi có hành động người dùng** |
| 3 | `public.usage_event` | `public` | Bản ghi tiêu tài nguyên gắn với artifact | ⚠️ *"nếu nghiệp vụ có phát sinh usage"* — xem [cảnh báo phạm vi](#q45-cảnh-báo-phạm-vi--kc-4-không-phải-một-transaction-cho-cả-vòng-đời-job) |
| 4 | `public.field_provenance` | `public` | **`KC-3`** mức field, cho các field mà artifact này sinh ra hoặc sửa | ✅ **khi có field bị ghi/sửa** |

⚠️ **Tên đủ điều kiện là bắt buộc** trong mọi migration và mọi câu SQL — guardrail `G-3` của [ADR-005](./ADR-005-Platform-Table-Schema-Placement.md). ⛔ Không dựa vào `search_path` để phân giải.

⚠️ **Điều kiện "bắt buộc?" ở hàng 2–4 KHÔNG phải cửa thoát.** Nó nói *"khi nghiệp vụ có sinh ra dòng đó thì dòng đó nằm trong cùng transaction"*, ⛔ **không** nói *"được phép hoãn dòng đó sang sau"*. Nguyên văn ràng buộc: `INSERT generation` + `INSERT change_log` + `INSERT usage_event` **bất khả phân** ([SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-NFR-13`).

#### Q4.3 "Commit cùng transaction" nghĩa là gì — năm thuộc tính kiểm chứng được

⛔ Cụm *"cùng một transaction"* **không được đọc như một khẩu hiệu**. Nó có đúng năm thuộc tính, mỗi thuộc tính có một phép đo. Nguồn: [Story-Provenance-Committed-In-Same-Transaction](../../022-User-Stories/Backlog/Story-Provenance-Committed-In-Same-Transaction.md) mục 4.

| Mã | Thuộc tính | Phép đo (chính là AC đã ký) |
|:--:|---|---|
| **`P-1`** | **All-or-nothing xuyên cả nhóm bảng.** Raise exception ngay sau khi ghi `generation` nhưng **trước** khi ghi `change_log` ⇒ **toàn bộ** rollback về **0 dòng mới** trên **cả nhóm** | Test tự động; ⚠️ nghiệm thu **là một TEST, không phải một màn hình** |
| **`P-2`** | **Boundary là PER-REQUEST.** Hai generation tạo gần như đồng thời cho hai panel khác nhau ⛔ **không** chia sẻ hay trộn transaction; rollback của request A ⛔ không ảnh hưởng commit của request B | Test 2 request song song |
| **`P-3`** | **⛔ Không `usage_event` mồ côi.** Một process khác (ví dụ worker sinh ảnh) ghi `usage_event` cho một `generation` **chưa commit** ⇒ phải **bị từ chối hoặc chờ đúng transaction** | Test; cưỡng chế nền bằng **FK** — xem [Q4.6](#q46-guardrail--cái-gì-db-cưỡng-chế-được-và-cái-gì-không) |
| **`P-4`** | **Abort bất thường cũng phải sạch.** Deadlock / timeout / OOM giữa chừng ⇒ ⛔ **không** dòng nào của nhóm được giữ lại một phần | Test gây deadlock có chủ đích |
| **`P-5`** | **MỘT connection pool tới MỘT PostgreSQL instance.** Toàn bộ đường ghi provenance nằm trong cùng một pool; ⛔ **không gọi sang service/DB khác** để ghi `change_log` hay `usage_event` | Kiểm cấu hình kết nối + test CI |

⭐ **`P-5` chính là chỗ `KC-4` gặp `D-01`/`D-05`.** Hai PostgreSQL, hoặc một service HTTP nội bộ nằm giữa artifact và bằng chứng của nó, làm `P-1` **không thể đạt được về nguyên lý** — không phải *"khó"*, mà là **không tồn tại transaction nào bao được cả hai**. Đó là lý do [SRS](../../020-Requirements/SRS-Comic-Studio.md) (**`SRS-NFR-21`**, `D-05`) cắt microservices và 2 DB, và nêu đúng lý do: **2 DB = mất transaction boundary `KC-4`**.

**Exit criterion neo vào**: `M1-5` (Roadmap §2, mốc MVP1) — *"5 hạng mục provenance tồn tại, **và có test chứng minh chúng commit CÙNG MỘT transaction với artifact**"*. Tiêu chí #1 (5 cột tồn tại) thuộc [Story-Provenance-Chain](../../022-User-Stories/Backlog/Story-Provenance-Chain-Parent-Generation.md); **tiêu chí #2 chính là `P-1`…`P-5`**.

#### Q4.4 `KC-4` là transaction span nhiều schema — và đó KHÔNG phải vấn đề

⚠️ **Đọc kỹ mục này trước khi ai đó "sửa cho gọn".**

[ADR-005](./ADR-005-Platform-Table-Schema-Placement.md) đã chốt: `change_log`, `field_provenance`, `usage_event` ở schema **`public`**; còn `generation` ở schema **`generation`** (`D-01`). ⇒ **`KC-4` là một transaction span BA schema** (`generation` + `public`, và gián tiếp `comic`/`story` khi hành động editor chạm dữ liệu module).

**Điều đó hoàn toàn hợp lệ.** Một transaction PostgreSQL có phạm vi là **DATABASE**, ⛔ **không phải SCHEMA**. Schema chỉ là namespace. Chừng nào tất cả các bảng nằm trong **một** database (`D-01`: 1 PostgreSQL), một `BEGIN … COMMIT` bao được tất cả, **không cần** 2PC, ⛔ **không cần** distributed transaction, ⛔ **không cần** outbox. [ADR-005](./ADR-005-Platform-Table-Schema-Placement.md) mục Context đã ghi đúng câu này: *"Không ràng buộc vị trí schema (transaction Postgres span được nhiều schema trong cùng database)"*.

⭐ **Cái SẼ VỠ nếu rải `change_log` theo module không phải là "span nhiều schema" — mà là TÍNH DUY NHẤT của nó.** Lý do đầy đủ nằm ở [ADR-005](./ADR-005-Platform-Table-Schema-Placement.md) mục Alternatives `(c)`, ⛔ **không lặp lại ở đây**. Tóm tắt một dòng để người đọc biết mình đang tra cái gì: `story.change_log` + `comic.change_log` + `generation.change_log` phá quy tắc *"một `change_log` duy nhất"*, và qua đó **phá chính điều kiện kiểm chứng của `KC-4`** — không còn một bảng nào để hỏi *"toàn bộ bằng chứng của artifact này có đủ không"*.

| Mệnh đề | Đúng/Sai | Ghi chú |
|---|:--:|---|
| *"`KC-4` span nhiều schema ⇒ phải gộp về một schema"* | ❌ **SAI** | Postgres không quan tâm schema trong phạm vi một transaction |
| *"`KC-4` span nhiều schema ⇒ phải dùng 2PC / outbox"* | ❌ **SAI** | Chỉ đúng khi span nhiều **database** — mà `D-01` cấm |
| *"Có thể rải `change_log` ra từng schema module cho gọn"* | ❌ **SAI** | Phá tính duy nhất ⇒ [ADR-005](./ADR-005-Platform-Table-Schema-Placement.md) Alternatives `(c)` |
| *"`KC-4` cần đúng một database và đúng một connection pool"* | ✅ **ĐÚNG** | `P-5`; `D-01` + `D-05` |

#### Q4.5 Cảnh báo phạm vi — `KC-4` KHÔNG phải "một transaction cho cả vòng đời job"

⛔ **Đây là chỗ dễ đọc quá tay nhất của toàn bộ ADR.** `KC-4` ràng buộc **artifact và bằng chứng của chính artifact đó**. Nó ⛔ **không** nói *"cả pipeline sinh panel chạy trong một transaction"* — điều đó bất khả thi vì có lời gọi provider bên ngoài ở giữa.

Ba mảnh sự thật trong repo **cùng đúng**, và chúng vẽ ra vùng chưa được pin:

1. `D-03` ([SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-FR-25`): **enqueue** là `INSERT generation` + `INSERT job` trong **một** transaction ⇒ ⛔ không bao giờ có job mồ côi. Xem [ADR-015](./ADR-015-Job-Queue-In-Postgres.md).
2. `D-59` ([SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-FR-31`): `cost_usd` là giá trị **thực đo tại thời điểm generation hoàn tất**, ⛔ không phải ước lượng trước khi gọi.
3. [Story-Usage-Event-And-Daily-Rollup](../../022-User-Stories/Backlog/Story-Usage-Event-And-Daily-Rollup.md) (unhappy path): 3 `usage_event` của 3 candidate **vẫn được ghi** ngay cả khi VLM-select **thất bại sau đó** — tài nguyên đã tiêu thì phải có bản ghi.

⇒ **Invariant mà ADR này chốt** (và là thứ file khác được phép trỏ tới):

> Với **mỗi** dòng `generation`, dòng đó cùng `change_log` của nó, `field_provenance` của nó và `usage_event` của nó là **bất khả phân**.

⇒ **`TBD` được route đi, ⛔ ADR này KHÔNG tự giải**: *thứ tự chính xác trong vòng đời job — dòng `usage_event` gắn vào lần `INSERT generation` nào (lúc enqueue, hay lúc mỗi candidate hoàn tất), và `cost_usd` thực đo đi vào bằng `INSERT` hay `UPDATE` trên cùng dòng đó.* ⚠️ ⛔ **Không nguồn Phase 1 nào pin việc này** ⇒ **ai đóng: Architect, lô DB Schema**, trong [`DB-Entity-Provenance-And-Usage.md`](../Schema/DB-Entity-Provenance-And-Usage.md) + [`DB-Entity-Generation.md`](../Schema/DB-Entity-Generation.md), **trước khi hai file đó được duyệt**. Ràng buộc bắt buộc mang theo: lời giải phải giữ **cả** `P-1`…`P-5` **và** tính append-only của `usage_event` (`D-58`, xem [ADR-018](./ADR-018-Usage-Event-And-Rollup-Model.md)).

#### Q4.6 Guardrail — cái gì DB cưỡng chế được, và cái gì KHÔNG

⚠️ **Mục này phải đọc trung thực, vì một câu sai ở đây sẽ được mọi file DB Schema kế thừa.**

**Cưỡng chế ĐƯỢC ở tầng DB** — dùng đúng cơ chế PostgreSQL, ⛔ không phụ thuộc code:

| Mã | Guardrail | Cưỡng chế bằng | Bảo vệ điều gì |
|:--:|---|---|---|
| **`GR-1`** | `generation.origin` **`NOT NULL`** | Ràng buộc `NOT NULL` + `ENUM` | `D-51`/`KC-3` — `INSERT` thiếu `origin` **FAIL ở tầng DB** |
| **`GR-2`** | `usage_event.generation_id` là **FK** tới `generation` | Foreign key | `P-3` — ⛔ không có `usage_event` mồ côi. FK **không thoả được** nếu dòng `generation` chưa tồn tại trong cùng transaction |
| **`GR-3`** | `change_log` / `usage_event` **append-only** | ⛔ **REVOKE `UPDATE`, `DELETE`** khỏi mọi DB role ứng dụng | `D-48` + `D-58` — [Story-Usage-Event](../../022-User-Stories/Backlog/Story-Usage-Event-And-Daily-Rollup.md) AC bắt *"bị từ chối ở **tầng DB** (permission/constraint)"* |
| **`GR-4`** | `parent_generation_id` là **FK** self-reference, **nullable** | Foreign key | `KC-1` — ⛔ chuỗi lineage không trỏ vào hư vô; `NULL` vẫn hợp lệ |
| **`GR-5`** | RLS + `tenant_id` trên `change_log`, `field_provenance`, `usage_event` | RLS policy | `KC-5` — ⛔ đặc tả ở [ADR-006](./ADR-006-RLS-Tenant-Context-Injection.md), **không lặp lại ở đây** |

**⛔ KHÔNG cưỡng chế được ở tầng DB — nói thẳng:**

> ⚠️ **⛔ Không có ràng buộc PostgreSQL nào cưỡng chế được bản thân TÍNH NGUYÊN TỬ của `KC-4`.** Không `CHECK`, không trigger, không constraint nào có thể bắt *"nếu anh insert `generation` thì anh **phải** insert `change_log` trong cùng transaction này"* — vì tại thời điểm ràng buộc chạy, transaction chưa kết thúc và DB không biết cái gì **sẽ** được ghi tiếp.

⇒ `KC-4` được cưỡng chế bằng **ba lớp, không lớp nào thay thế được lớp nào**:

| Lớp | Cơ chế | Chặn được gì |
|:--:|---|---|
| **L1 — Kiến trúc** | `D-01`/`D-05`: **1 database, 1 connection pool** ⇒ transaction bao được cả nhóm bảng | Chặn **lớp lỗi bất khả thi**: 2 DB thì `P-1` không tồn tại |
| **L2 — Cơ chế trong code** | **Một** middleware `change_log` ở tầng service (xem [Q2](#q2-change_log-kc-2--phạm-vi-ghi-và-điểm-cưỡng-chế)); mọi đường ghi đi qua nó, trong **cùng** unit-of-work với ghi nghiệp vụ | Chặn *"dev quên gọi"* — bằng cơ chế dùng chung, ⛔ không bằng kỷ luật |
| **L3 — Test trong CI** | `P-1`…`P-5` + test *"endpoint bỏ qua middleware ⇒ FAIL"* | Chặn **hồi quy**: cái gì hôm nay đúng mà mai gãy thì CI đỏ |

⭐ **⛔ Đừng viết ở bất kỳ file nào rằng "tầng DB cưỡng chế `KC-4`".** Câu đúng là: **tầng DB cưỡng chế các CỘT và tính APPEND-ONLY (`GR-1`…`GR-5`); tính NGUYÊN TỬ được cưỡng chế bằng kiến trúc 1-DB (`L1`) + middleware (`L2`) + test CI (`L3`).**

#### Q4.7 Hợp đồng trích dẫn — file khác trỏ về đây thế nào

| File sắp viết | Trỏ về mục nào | ⛔ Không được làm |
|---|---|---|
| [`DB-Entity-Generation.md`](../Schema/DB-Entity-Generation.md) | [Q4.1](#q41-phát-biểu-chuẩn-normative) + [Q4.2](#q42-chính-xác-những-bảng-nào) + `GR-1`, `GR-4` | ⛔ Không đặc tả lại `KC-4`; ⛔ không tự quyết thứ tự vòng đời của [Q4.5](#q45-cảnh-báo-phạm-vi--kc-4-không-phải-một-transaction-cho-cả-vòng-đời-job) mà không ghi ra là mình đang đóng `TBD` đó |
| [`DB-Entity-Provenance-And-Usage.md`](../Schema/DB-Entity-Provenance-And-Usage.md) | [Q4.1](#q41-phát-biểu-chuẩn-normative)…[Q4.6](#q46-guardrail--cái-gì-db-cưỡng-chế-được-và-cái-gì-không) | ⛔ Không copy nội dung `KC-4` — [findings §3.5](../../010-Planning/pm-runs/2026-08-28-phase-2-architecture-design-comic-studio/findings/architect.md) cấm tạo nguồn sự thật thứ hai |
| `Endpoint-*` (mọi endpoint ghi) | [Q2](#q2-change_log-kc-2--phạm-vi-ghi-và-điểm-cưỡng-chế) + [Q4.3](#q43-commit-cùng-transaction-nghĩa-là-gì--năm-thuộc-tính-kiểm-chứng-được) `P-2` | ⛔ Không mô tả `change_log` như *"tuỳ endpoint"* |
| `Spec-Security-*` | [Q4.6](#q46-guardrail--cái-gì-db-cưỡng-chế-được-và-cái-gì-không) `GR-3` + [ADR-006](./ADR-006-RLS-Tenant-Context-Injection.md) | ⛔ Không tự đặt quyền `UPDATE`/`DELETE` cho role ứng dụng trên hai bảng append-only |

---

### Q5. Guardrail tầng DB cho `origin` (`D-51`)

`generation.origin` là **`NOT NULL`**. `INSERT` thiếu nó **bị DB từ chối**, ⛔ **không phải** bị cảnh báo ở tầng ứng dụng ([SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-NFR-14`).

⭐ **Lý do đặt ở tầng DB chứ không ở code — đã có sẵn trong nguồn**, ⛔ không phải sở thích của ADR này: [SRS](../../020-Requirements/SRS-Comic-Studio.md) §2.2 nêu Founder ở vai operator, đội **1 người**, `bus factor = 1`, **⛔ không có code review** ⇒ *"lý do guardrail đặt ở **tầng DB** chứ không ở code"*. Guardrail ở code chỉ mạnh bằng người review nó; ở đây **không có người review**.

⚠️ Generation đầu chuỗi (`parent_generation_id = NULL`) **vẫn phải** có `origin` xác định (`'ai'` hoặc `'human'`) — `NULL` parent hợp lệ, `NULL` origin **thì không**.

### Q6. ⚠️ Cắt UI cây ≠ cắt cột dữ liệu (`D-56`)

⛔ **Đây là một bẫy cắt lẫn, và nó đã được cảnh báo hai lần trong repo.**

| Bị cắt | Được giữ |
|---|---|
| ❌ **UI duyệt CÂY generation**: tree view, diff view, branch-merge — cắt hẳn ở **mọi** mốc, kể cả Full Scope ([SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-NFR-23`) | ✅ **Cột `parent_generation_id` + `relation_kind`** — bắt buộc từ **migration số 1** (`D-47`, `KC-1`) |
| Thay bằng: **flat list** theo `created_at` + `approved_generation_id` | ✅ `field_provenance`, `origin`, `change_log` — nguyên vẹn |

⚠️ **`CẤM-09`** ([Story-Provenance-Chain](../../022-User-Stories/Backlog/Story-Provenance-Chain-Parent-Generation.md) mục 3): *"cắt UI cây generation (`D6` = ❌) **không** đồng nghĩa cắt cột dữ liệu `parent_generation_id` (`KC-1` = bắt buộc). **Hai quyết định độc lập và trái chiều**."*

⇒ **Quy tắc cho mọi file sau**: một tài liệu nào viết *"vì đã cắt UI cây nên không cần lưu quan hệ cha-con"* là **vi phạm `KC-1`** và phải bị chặn ở review. Cột không có UI đọc **vẫn là bằng chứng pháp lý hợp lệ**; UI là cách con người xem, ⛔ không phải điều kiện tồn tại của dữ liệu.

### Q7. Ranh giới — ADR này ⛔ KHÔNG quyết cái gì

| ⛔ Không quyết | Ai quyết |
|---|---|
| Vị trí schema của `change_log` / `usage_event` / `field_provenance` | Đã quyết ở [ADR-005](./ADR-005-Platform-Table-Schema-Placement.md) — ⛔ không mở lại |
| Policy RLS cụ thể, cơ chế bơm tenant context | Đã quyết ở [ADR-006](./ADR-006-RLS-Tenant-Context-Injection.md) — ⛔ không đặc tả lại |
| DDL đầy đủ, kiểu cột, index, danh mục `action_type` | Architect, lô **DB Schema** |
| Mô hình đếm `usage_event` và chi phí VLM | [ADR-018](./ADR-018-Usage-Event-And-Rollup-Model.md) ghi nhận, lô **DB Schema** giải |
| Chính sách purge / retention cho hai bảng append-only | `TBD` — xem [Consequences](#việc-còn-để-tbd--không-được-bịa) |

---

## Alternatives considered

### (a) Ghi provenance **bất đồng bộ** sau khi commit artifact (outbox / event bus / background writer) — ⛔ LOẠI

**Nội dung**: commit `generation` trước cho nhanh, đẩy `change_log` + `usage_event` vào outbox hoặc queue, một worker ghi sau.

**Điểm mạnh phải ghi nhận trung thực**: đây là pattern chuẩn công nghiệp, giảm thời gian giữ lock, làm đường ghi nóng ngắn hơn, và chịu tải tốt hơn khi ghi bằng chứng đắt.

**⛔ Vì sao vẫn LOẠI**: nó tạo ra **đúng** failure mode mà `KC-4` tồn tại để chặn. Outbox cho **eventual** consistency — nghĩa là tồn tại một cửa sổ thời gian trong đó artifact có mà bằng chứng chưa có, và nếu worker chết trong cửa sổ đó thì **bằng chứng thiếu vĩnh viễn** mà **không ai biết**. [SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-NFR-13` gọi tên chính xác: *"Bằng chứng có thể thiếu ngẫu nhiên thì không phải bằng chứng."* Trong bối cảnh Điều 5a, *"eventual"* là một từ **không có nghĩa pháp lý**: khi tranh chấp xảy ra, hồ sơ hoặc đủ hoặc không đủ, ⛔ không có trạng thái *"sẽ đủ"*. Đây cũng là phương án mà `D-05` đã loại ở cấp topology (2 DB / microservices) — chấp nhận nó ở tầng code là **lách chính quyết định đó**.

### (b) Rải `change_log` theo module chủ sở hữu — ⛔ LOẠI

⛔ **Đã LOẠI ở [ADR-005](./ADR-005-Platform-Table-Schema-Placement.md) Alternatives `(c)`.** ADR này ⛔ **không lập luận lại**, chỉ ghi nhận hệ quả với `KC-4`: cái vỡ **không phải** *"span nhiều schema"* (điều đó hợp lệ — xem [Q4.4](#q44-kc-4-là-transaction-span-nhiều-schema--và-đó-không-phải-vấn-đề)) mà là **tính DUY NHẤT** của `change_log`, tức là điều kiện kiểm chứng của `KC-4`.

### (c) Provenance ở **mức row** thay vì **mức field** — ⛔ LOẠI

**Nội dung**: chỉ giữ `generation.origin`, bỏ bảng `field_provenance`; suy ra phần đóng góp của con người từ `change_log`.

**Điểm mạnh**: bớt một bảng, bớt một đường ghi trong transaction nóng, ⇒ trực tiếp giảm rủi ro của `KC-4`.

**⛔ Vì sao LOẠI**: `D-49` là `CHỐT` và nằm trong `MVP-Scope §6`. Về nội dung: *"có `parent_generation_id` mà thiếu `field_provenance` ⇒ **không xác định được ranh giới phần được bảo hộ**"*. Điều 5a bảo hộ **phần đóng góp**, ⇒ không vẽ được ranh giới thì hồ sơ **không dùng được**, bất kể `change_log` đầy đủ tới đâu.

### (d) Guardrail `origin` ở **tầng ứng dụng** (validation + cảnh báo) — ⛔ LOẠI

**Điểm mạnh**: thông báo lỗi thân thiện hơn, dễ test unit, không cần migration khi đổi quy tắc.

**⛔ Vì sao LOẠI**: `D-51` là `CHỐT` và [SRS](../../020-Requirements/SRS-Comic-Studio.md) §2.2 nêu thẳng lý do — `bus factor = 1`, ⛔ **không có code review**. Một guardrail ở code mà không có người review là một guardrail **chỉ tồn tại tới lần refactor đầu tiên**. Ràng buộc `NOT NULL` thì tồn tại cho tới khi có người **cố ý** viết migration để gỡ nó — và migration thì để lại dấu vết.

### (e) Cắt luôn cột `parent_generation_id` vì UI cây đã bị cắt — ⛔ LOẠI

**Nội dung**: `D6` = `❌ cắt hẳn` ⇒ không ai đọc quan hệ cha-con ⇒ bỏ cột cho gọn.

**⛔ Vì sao LOẠI**: đây chính là **bẫy cắt lẫn** mà `CẤM-09` tồn tại để chặn — xem [Q6](#q6--cắt-ui-cây--cắt-cột-dữ-liệu-d-56). Và nó **không đảo ngược được**: [SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-FR-34` ghi *"từ migration số 1, không phải backlog"*, [Story-Provenance-Chain](../../022-User-Stories/Backlog/Story-Provenance-Chain-Parent-Generation.md) ghi **không backfill được**. Tiết kiệm được một cột, mất bảo hộ cho toàn bộ generation của giai đoạn đó.

### (f) Best-effort provenance + **reconcile job** chạy đêm để vá dòng thiếu — ⛔ LOẠI

**Điểm mạnh**: có vẻ giữ được cả tốc độ lẫn tính đầy đủ.

**⛔ Vì sao LOẠI**: reconcile job **bịa lại** bằng chứng từ suy luận, không phải ghi lại sự thật đã quan sát. Một `change_log` row do job đêm suy ra ⛔ **không** chứng minh được *"con người đã chọn X thay vì Y"* — nó chỉ chứng minh *"hệ thống đoán rằng có ai đó đã chọn"*. Ngoài ra nó **đụng thẳng `GR-3`**: `change_log` và `usage_event` là append-only với `UPDATE`/`DELETE` bị `REVOKE` ⇒ job vá dữ liệu **không có quyền** để chạy, và cấp quyền cho nó là gỡ chính guardrail đó.

---

## Consequences

### ⛔ Hệ quả BẮT BUỘC ĐỌC

1. **Mọi đường ghi tạo `generation` đều là đường nóng của `KC-4`.** ⇒ ⛔ Không được có *"đường tắt"* nào tạo `generation` mà không đi qua unit-of-work chung: không script vận hành, không seed, không admin tool. Một đường tắt = một lỗ hổng bằng chứng.
2. **`KC-4` là ràng buộc chặn `MVP1`, không phải mục tiêu chất lượng.** Exit criterion `M1-5` tiêu chí #2 **là một test**, và [Story-Provenance-Committed](../../022-User-Stories/Backlog/Story-Provenance-Committed-In-Same-Transaction.md) ghi rõ nó ⛔ **không có UI để demo**.
3. **⛔ Không backfill được.** Đây là lý do `KC-1`/`KC-3` phải ở **migration số 1**, và là lý do `BLOCKER-04` được mô tả là *"chặn MỌI THỨ"*.

### Tích cực

- **Một nguồn duy nhất cho `KC-4`** ⇒ hai file DB Schema và mọi file API trỏ về đây thay vì tự đặc tả ⇒ ⛔ không có nguy cơ ba phiên bản `KC-4` lệch nhau âm thầm.
- **Hình dạng đơn giản nhất có thể**: một database, một transaction, một `change_log`, một `usage_event` — kế thừa trực tiếp từ [ADR-005](./ADR-005-Platform-Table-Schema-Placement.md). ⛔ Không 2PC, ⛔ không outbox, ⛔ không saga.
- **Guardrail nằm đúng tầng**: cột và append-only ở DB (`GR-1`…`GR-5`), nguyên tử ở kiến trúc + test — mỗi thứ ở nơi nó thật sự cưỡng chế được.
- Chuỗi lineage đầy đủ mở sẵn đường cho `D6` (UI cây) nếu tương lai mở lại — **dữ liệu đã có**, chỉ thiếu màn hình.

### Tiêu cực — chi phí thật của quyết định này

- **Transaction dài hơn và chạm nhiều bảng hơn** ⇒ nhiều lock hơn, khả năng deadlock cao hơn dưới tải. Đây là chi phí **đã chấp nhận**, ⛔ không phải khiếm khuyết cần tối ưu bằng cách nới `KC-4`.
- **`KC-4` ràng buộc topology vĩnh viễn**: chừng nào `KC-4` còn hiệu lực, ⛔ **không thể** tách `generation` sang database khác. Mọi đề xuất scale-out trong tương lai phải mở lại **ADR này** trước, không phải mở lại `ADR-009`/`D-05` sau.
- **Middleware `change_log` là điểm nghẽn kiến trúc**: [Story-Change-Log](../../022-User-Stories/Backlog/Story-Change-Log-On-Every-Editor-Action.md) mục 5 tự khai `E_build = 20h` `[EM]` **vượt trần 16h**, và ⛔ **không split được** — vì split để lại component chưa được bảo vệ giữa chừng.
- **Hai bảng append-only tăng vô hạn.** [SRS](../../020-Requirements/SRS-Comic-Studio.md) §5.2 (hàng `b-3`) nêu thẳng: `change_log` (`SRS-FR-35`) và `usage_event` (`SRS-FR-30`) append-only **tăng vô hạn nếu không có chính sách purge** — mà thời hạn retention lại là **câu hỏi pháp lý** cùng nhóm chờ luật sư với `SRS-NFR-17`.

### Việc còn để `TBD` — không được bịa

| `TBD` | Ai đóng | Khi nào |
|---|---|---|
| ⭐ **Thứ tự gắn `usage_event` / `cost_usd` trong vòng đời job** ([Q4.5](#q45-cảnh-báo-phạm-vi--kc-4-không-phải-một-transaction-cho-cả-vòng-đời-job)) — ⛔ không nguồn Phase 1 nào pin | **Architect, lô DB Schema** | Trước khi [`DB-Entity-Provenance-And-Usage.md`](../Schema/DB-Entity-Provenance-And-Usage.md) + [`DB-Entity-Generation.md`](../Schema/DB-Entity-Generation.md) được duyệt |
| Danh mục `action_type` của `change_log` — ⛔ [Story-Change-Log](../../022-User-Stories/Backlog/Story-Change-Log-On-Every-Editor-Action.md) cấm phát minh thêm ngoài hành động 4 Story editor thực sự có | Architect (lô DB Schema) + PO | Cùng mốc trên |
| DDL của `field_provenance` (khoá tự nhiên, hình dạng tham chiếu tới field) | Architect (lô DB Schema) | Cùng mốc trên |
| Hình dạng ràng buộc cho *"`continuity_fix` phải trỏ được về gốc"* (`CHECK` DB hay validation ứng dụng) | Architect (lô DB Schema) | Cùng mốc trên |
| **Retention / purge policy** cho `change_log` + `usage_event` — ⚠️ là **câu hỏi pháp lý**, cùng nhóm chờ luật sư với `SRS-NFR-17` ([SRS](../../020-Requirements/SRS-Comic-Studio.md) §5.2, `b-3`) | PM + luật sư SHTT | Trước khi hai bảng đủ lớn để thành vấn đề vận hành |
| Ba câu hỏi pháp lý Điều 5a mang tới luật sư SHTT (`SRS-NFR-17`) | PM + luật sư SHTT | ⛔ Điều kiện chặn là **CHỐT**, nội dung trả lời `TBD` |

---

## Đã quyết ở đâu

| Quyết định | Mã `D-xx` | Nguồn (file + mã requirement) |
|---|:--:|---|
| `parent_generation_id` (nullable FK) + `relation_kind ENUM('retry','variation','refine','continuity_fix')`, từ **migration số 1**, ⛔ không backfill được | `D-47` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) **`SRS-FR-34`** · `MVP-Scope §6 KC-1` · [Story-Provenance-Chain-Parent-Generation](../../022-User-Stories/Backlog/Story-Provenance-Chain-Parent-Generation.md) mục 4 AC-1 |
| `change_log` append-only ghi **MỌI** hành động người dùng, kể cả *"chọn generation X thay vì Y"* và **export**; *"prompt một mình không chứng minh được decisive contribution"* | `D-48` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) **`SRS-FR-35`** · §3.D · §4.1 · `MVP-Scope §6 KC-2` · [Story-Change-Log-On-Every-Editor-Action](../../022-User-Stories/Backlog/Story-Change-Log-On-Every-Editor-Action.md) mục 4 |
| `field_provenance` mức **field** + `generation.origin ENUM('ai','ai_edited','human')` | `D-49` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) **`SRS-FR-36`** · `MVP-Scope §6 KC-3` |
| ⭐ **`KC-4`**: `KC-1`+`KC-2`+`KC-3` commit **CÙNG MỘT TRANSACTION** với artifact; `INSERT generation` + `INSERT change_log` + `INSERT usage_event` **bất khả phân** | `D-50` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) **`SRS-NFR-13`** · `MVP-Scope §6 KC-4` · [Story-Provenance-Committed-In-Same-Transaction](../../022-User-Stories/Backlog/Story-Provenance-Committed-In-Same-Transaction.md) mục 4 |
| **Guardrail tầng DB**: `INSERT` vào `generation` thiếu `origin` **FAIL ở tầng DB** | `D-51` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) **`SRS-NFR-14`** · [Story-Provenance-Chain-Parent-Generation](../../022-User-Stories/Backlog/Story-Provenance-Chain-Parent-Generation.md) mục 4 AC-2 |
| Lý do guardrail đặt ở **tầng DB** chứ không ở code: `bus factor = 1`, ⛔ **không có code review** | `D-51` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) §2.2 (`CF-1.2` `[CHỐT]`) |
| ⛔ **KHÔNG UI duyệt cây generation**; flat list `created_at` + `approved_generation_id`; ⚠️ **cắt UI ⛔ không cắt cột** | `D-56` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) **`SRS-NFR-23`** · `MVP-Scope §3 D6` vs `§6 KC-1` · `CẤM-09` |
| Modular monolith **1 process · 1 PostgreSQL · 3 schema** — điều kiện cần của `P-5` | `D-01` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) **`SRS-NFR-02`** · §2.3 · §4.3 |
| ⛔ **KHÔNG** microservices, ⛔ **KHÔNG** 2 PostgreSQL — lý do nêu thẳng: **2 DB = mất transaction boundary `KC-4`** | `D-05` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) **`SRS-NFR-21`** · `MVP-Scope §4.2` (`CF-9.2` lý do 2) |
| `change_log` / `field_provenance` / `usage_event` / `usage_daily` nằm ở schema **`public`**; `generation` ở schema `generation` ⇒ `KC-4` span nhiều schema | `D-01` | [ADR-005](./ADR-005-Platform-Table-Schema-Placement.md) mục `Q1` — ⛔ ADR này **không quyết lại** |
| Lý do ⛔ loại phương án rải `change_log` theo module (phá **tính DUY NHẤT**) | — | [ADR-005](./ADR-005-Platform-Table-Schema-Placement.md) mục Alternatives `(c)` — ⛔ **không lập luận lại** |
| Cặp policy RLS của `app_worker`, cơ chế bơm tenant context, `KC-5` | `D-09`, `D-10` | [ADR-006](./ADR-006-RLS-Tenant-Context-Injection.md) — ⛔ ADR này **không đặc tả lại RLS** |
| Transactional enqueue `INSERT generation` + `INSERT job` trong **một** transaction (⚠️ **khác** `KC-4`, xem [Q4.5](#q45-cảnh-báo-phạm-vi--kc-4-không-phải-một-transaction-cho-cả-vòng-đời-job)) | `D-03` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) **`SRS-FR-25`** · [ADR-015](./ADR-015-Job-Queue-In-Postgres.md) |
| `usage_event` append-only + rollup `usage_daily`; billing là **hàm tổng hợp trên event thô** | `D-58` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) **`SRS-FR-30`** · [ADR-018](./ADR-018-Usage-Event-And-Rollup-Model.md) |
| `cost_usd` **thực đo tại thời điểm generation hoàn tất** — tiền đề của cảnh báo phạm vi [Q4.5](#q45-cảnh-báo-phạm-vi--kc-4-không-phải-một-transaction-cho-cả-vòng-đời-job) | `D-59` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) **`SRS-FR-31`** · [Story-Generation-Cost-And-Model-Metadata](../../022-User-Stories/Backlog/Story-Generation-Cost-And-Model-Metadata.md) mục 4 |
| Mục tiêu bảng `generation` là **auditability + lineage**, ⛔ không phải reproducibility | `D-44` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) §3.A |
| **Căn cứ pháp lý**: NĐ 134/2026/NĐ-CP **Điều 5a** `[OFF]` — *"substantial and decisive intellectual contribution"*; AI-only ⛔ không được bảo hộ; nghĩa vụ lưu prompts/inputs/intermediate drafts | — | `CF-7.2` / `CF-7.3` `[OFF]`, dẫn qua [Story-Provenance-Chain-Parent-Generation](../../022-User-Stories/Backlog/Story-Provenance-Chain-Parent-Generation.md) mục 3 |
| Exit criterion **`M1-5`** — 5 hạng mục provenance tồn tại **và** có **test** chứng minh commit cùng transaction | — | `Roadmap §2` mốc MVP1, dẫn qua [Story-Provenance-Committed-In-Same-Transaction](../../022-User-Stories/Backlog/Story-Provenance-Committed-In-Same-Transaction.md) mục 3 |
| `change_log` + `usage_event` append-only **tăng vô hạn** nếu không có purge; retention là câu hỏi pháp lý | — | [SRS](../../020-Requirements/SRS-Comic-Studio.md) §5.2 (hàng `b-3`) |
| ⛔ Không tự gán số cho hàng `TBD` | — | [SRS](../../020-Requirements/SRS-Comic-Studio.md) §5.2 |
| ⭐ `KC-4` **cắt ngang** hai file DB Entity ⇒ đặt ở **ADR-017** làm nguồn duy nhất, hai file schema **trỏ tới**, ⛔ không copy | — | [findings/architect §3.5](../../010-Planning/pm-runs/2026-08-28-phase-2-architecture-design-comic-studio/findings/architect.md) |

---

_Created by system-architect_
_Author: trisjr_
