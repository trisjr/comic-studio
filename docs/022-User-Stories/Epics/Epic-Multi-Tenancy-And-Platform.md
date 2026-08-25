---
id: EPIC-E
type: epic
status: draft
project: comic-studio
created: 2026-08-24
---

# Epic-E — Multi-tenancy & hạ tầng

> [!IMPORTANT]
> **Quy ước nhãn nguồn số liệu** (kế thừa nguyên vẹn — **số và nhãn là một cặp không tách rời**):
> `[OFF]` nguồn official/paper gốc · `[BCN]` báo cáo ngành có tên firm · `[TC]` nguồn thứ cấp · `[EM]` ước lượng hoặc phép nhân, **không phải số đo** · `[CHỐT]` quyết định của Founder tại gate.
>
> Epic này **chỉ trích lại** số liệu từ tầng Planning và Requirements. Không tự tra lại, không tự tính lại (`CẤM-15`).
>
> **Trục Epic của backlog này cắt theo MODULE A–H, 1:1 với 8 BRD — KHÔNG cắt theo mốc MVP.** Lý do: [MVP-Scope §1.1](../../010-Planning/MVP-Scope.md#11-ranh-giới-ba-tài-liệu) phân định *"khi nào"* thuộc [Roadmap.md](../../010-Planning/Roadmap.md); Epic theo mốc tạo **nguồn sự thật thứ hai** về thời gian. Cột *Mốc* và cờ horizon vì vậy nằm ở **tầng Story**, không ở tầng Epic.

## Mục lục

1. [Implements](#1-implements)
2. [Mục tiêu Epic](#2-mục-tiêu-epic)
3. [Story trong horizon](#3-story-trong-horizon)
4. [Story ngoài horizon — chưa có file](#4-story-ngoài-horizon--chưa-có-file)
5. [Definition of Done cấp Epic](#5-definition-of-done-cấp-epic)
6. [Tài liệu liên quan](#6-tài-liệu-liên-quan)

---

## 1. Implements

Implements: [PRD-Comic-Studio §4 — E. Multi-tenancy & hạ tầng](../../020-Requirements/PRD-Comic-Studio.md#e-multi-tenancy--hạ-tầng)

> Anchor trên trỏ tới **H3 `E. Multi-tenancy & hạ tầng`** trong [PRD mục 4](../../020-Requirements/PRD-Comic-Studio.md#4-yêu-cầu-chức-năng-theo-8-module) — nơi chứa `FR-E-01`…`FR-E-06`. PRD §4.0 quy ước 4 ghi rõ **cấu trúc tám H3 là contract cứng**: đổi tên hoặc đổi thứ tự H3 ⇒ link này chết.

---

## 2. Mục tiêu Epic

> **Nền multi-tenant an toàn từ commit đầu tiên**: `tenant_id` + RLS + storage tách tenant, trên kiến trúc **modular monolith**.

| # | Điều làm Epic này khác các Epic khác | Hệ quả lên backlog |
|---|---|---|
| 1 | Sản phẩm là **SaaS thương mại multi-tenant** — nền tảng cho **người khác tự upload truyện của họ** `[CHỐT]` CF-1.1 | `tenant_id` không phải một tính năng, nó là **tiền đề của mọi bảng** ⇒ Story `Story-Tenant-Id-And-RLS-Everywhere` phải nằm ở **lô đầu tiên**, không phải lô sớm |
| 2 | Khối này chiếm **15–25%** effort `[EM]` CF-6.9 mà thiết kế ý tưởng gốc **không nhắc một dòng** | Ước thiếu thì *"nó không lấy chỗ của tính năng — nó lấy chỗ của **thời gian không tồn tại**"* ([Charter §8](../../010-Planning/Charter-Comic-Studio.md#8-giả-định-assumptions) A7) |
| 3 | Rò rỉ dữ liệu chéo tenant là **sự cố tồn vong**, không phải một bug | Definition of Done của Epic là **một test PASS**, không phải một danh sách bảng đã sửa — xem [mục 5](#5-definition-of-done-cấp-epic) |
| 4 | Hai trong sáu yêu cầu của module (`FR-E-04` billing, `FR-E-06` worker riêng) rơi vào **MVP3** | Epic **vắt biên** horizon 09/2026–02/2027: 5 Story trong, 2 Story ngoài |

> ⚠️ **Con số 15–25% là `[EM]`** — ước lượng của lens kiến trúc, **không phải số đo**. ⛔ Nó **không** được trừ đi hay cộng vào con số effort editor **~20–25%** `[EM]` CF-6.7 (mẫu số **SaaS — đã bao gồm chính khối multi-tenancy này**): `CẤM-01`, xem [MVP-Scope §5.1](../../010-Planning/MVP-Scope.md#51--cảnh-báo-mẫu-số--đọc-trước-khi-nhìn-bất-kỳ-con-số--nào).

**Ranh giới**: Epic này sở hữu **nền** (isolation, định danh, storage, module boundary, process topology). Nó **không** sở hữu `usage_event` / credit ledger (→ [Epic-F](./Epic-Credit-And-Unit-Economics.md)), không sở hữu `change_log` / provenance (→ [Epic-G](./Epic-Legal-And-Compliance.md)), không sở hữu job queue của pipeline sinh ảnh (→ `BRD-001`, hàng `A5`/`A6`).

---

## 3. Story trong horizon

**5 Story** — horizon **09/2026 → 02/2027** `[CHỐT]` CF-8.1.

> **Cách đọc cột `I` / `S`**: chỉ chấm hai chữ của INVEST mà việc cắt lô cần — **I** (Independent) và **S** (Small). `⚠️` = sẽ vỡ · `⚠️⚠️` = vỡ ở mức nặng nhất của cả backlog.
>
> ⚠️ **File Story chưa tồn tại** — chúng được tạo ở lô sau với **đúng** những tên dưới đây. Tên khác = link chết vĩnh viễn.

| Story (link) | Mốc | I | S | Trạng thái |
|---|---|:-:|:-:|---|
| [Story-Tenant-Id-And-RLS-Everywhere](../Backlog/Story-Tenant-Id-And-RLS-Everywhere.md) | **MVP1 — ngày đầu** | ⚠️⚠️ | ⚠️⚠️ | `[TRONG HORIZON]` · ⚠️⚠️ **vỡ CẢ `I` VÀ `S` ở mức nặng nhất của cả backlog**: chạm **100% bảng nghiệp vụ** + 100% composite index + 100% query, và **không có sub-slice nào "xong" mà có nghĩa** — `tenant_id` trên 8/10 bảng = **vẫn rò rỉ**. `MVP-Scope` **KC-5**: *"không có cách nào xác minh đã sửa hết"* ⇒ DoD là **test rò rỉ chéo tenant PASS (M1-1)**, KHÔNG phải số bảng đã sửa |
| [Story-Tenant-User-Membership-As-Three-Entities](../Backlog/Story-Tenant-User-Membership-As-Three-Entities.md) | MVP1 | ✅ | ✅ | `[TRONG HORIZON]` · ba entity riêng **kể cả khi quan hệ đang là 1:1** — chuẩn bị cho ngày bán gói team mà không migrate mô hình định danh |
| [Story-Per-Tenant-Object-Storage-No-Cross-Dedup](../Backlog/Story-Per-Tenant-Object-Storage-No-Cross-Dedup.md) | MVP1 | ✅ | ✅ | `[TRONG HORIZON]` · `tenant/{tenant_id}/{sha256}`; ⚠️ **dedup chéo tenant mâu thuẫn TRỰC TIẾP với lập luận bản quyền** của dự án |
| [Story-Buy-Authentication-Provider](../Backlog/Story-Buy-Authentication-Provider.md) | MVP1 | ✅ | ✅ | `[TRONG HORIZON]` · *"tự viết auth là cách nhanh nhất để một dev đốt hai tháng và vẫn có lỗ hổng"* ⇒ luồng signup/tạo tenant do **vendor sở hữu**, Story là yêu cầu **cấu hình** |
| [Story-Modular-Monolith-Three-Schemas](../Backlog/Story-Modular-Monolith-Three-Schemas.md) | MVP1 | ⚠️ | ⚠️ | `[TRONG HORIZON]` · 1 process · 1 PostgreSQL · 3 schema (`story` / `comic` / `generation`); luật module `comic` gọi `story` **chỉ qua** `resolveState()` và `getBible()`, **cưỡng chế bằng lint rule** |

> **Hai hàng nguồn KHÔNG sinh Story** — ghi ra để không ai đi tìm:
> - **`E6`** microservices + Vector DB riêng: `❌` **cắt hẳn**, thuộc *Scope Out* của [Charter §5.2](../../010-Planning/Charter-Comic-Studio.md#5-phạm-vi). ⚠️ **Vector DB riêng của `E6` ≠ `pgvector` của `B5`** — hai quyết định khác nhau ([BRD-005 §5.2](../../020-Requirements/BRD/BRD-005-Multi-Tenancy-And-Platform.md#52--phân-biệt-bắt-buộc-vector-db-riêng-của-e6--pgvector-của-b5)).
> - **`E8`** SSO/SAML, custom domain, white-label, multi-region: `⛔` Full Scope, **không có mốc**.

---

## 4. Story ngoài horizon — chưa có file

**2 Story** — cả hai ở **MVP3 (từ 03/2027)**, tức **NGOÀI horizon** `[EM]` CF-10.8.

| Story (link) | Mốc | Vì sao nằm ngoài horizon | Trạng thái tài liệu |
|---|---|---|---|
| `Story-Buy-Billing-Provider` | MVP3 | `FR-E-04` đạt `✅ +billing` ở MVP3. Gói trả phí **CÓ image gen** (Tầng 2/Tầng 3) rơi ra khỏi horizon ([Roadmap §5.1](../../010-Planning/Roadmap.md#51-cái-gì-rơi-ra-khỏi-092026022027)) ⇒ billing provider chưa cần trong horizon. **Mua, không tự viết** — *"không tự xây một hệ thống tiền tệ"* | **chưa có file** |
| `Story-Worker-As-Separate-Process-Same-Codebase` | MVP3 | `FR-E-06`: 2 entrypoint, **CÙNG codebase**. Là **seam kinh tế**, không phải seam kỹ thuật — worker chết mà API vẫn sống. Exit criterion **M3-4** (test kill process) nằm ở MVP3 | **chưa có file** |

> ⚠️ **Hai Story này không được "kéo vào cho đủ"**: `MVP-Scope` §4.2 xếp *1 process* là một phần của quyết định modular monolith. Tách worker sớm là mở lại một quyết định đã chốt, không phải làm sớm một việc tốt.

---

## 5. Definition of Done cấp Epic

### 5.1 Điều kiện ra trong horizon — nguồn là `Roadmap` §2

| # | Tiêu chí | Nguồn |
|---|---|---|
| 1 | **`tenant_id NOT NULL` trên 100% bảng nghiệp vụ** | **M1-1** |
| 2 | **RLS policy bật trên 100% bảng có `tenant_id`** | **M1-1** |
| 3 | ⭐ **Test rò rỉ chéo tenant PASS** — query của tenant A **không trả về 1 row nào** của tenant B | **M1-1** |
| 4 | Object storage dùng prefix `tenant/{tenant_id}/{sha256}`; **không có** đường dedup chéo tenant | `FR-E-03` · [Analysis §5.7](../../050-Research/Analysis-Comic-Studio-Concept.md) #4 |
| 5 | `tenant` / `user` / `membership` tồn tại là **ba** entity; không có bảng nào gộp hai vai | `FR-E-02` |
| 6 | Auth do **vendor** cung cấp; trong repo **không tồn tại** code tự viết cho luồng định danh | `FR-E-04` |
| 7 | Lint rule cưỡng chế `comic → story` **chỉ qua** `resolveState()` và `getBible()`, chạy trong CI | `FR-E-05` · CF-9.2 |

> [!IMPORTANT]
> ⭐ **Definition of Done của `Story-Tenant-Id-And-RLS-Everywhere` là tiêu chí #3 — TEST RÒ RỈ CHÉO TENANT PASS (`M1-1`) — KHÔNG phải số bảng đã sửa.**
>
> Vì sao phải viết tường minh: `MVP-Scope` **KC-5** ghi *"không có cách nào xác minh đã sửa hết"*. Một báo cáo *"đã thêm `tenant_id` cho 8/10 bảng"* nghe như tiến độ 80%, nhưng thực tế là **vẫn rò rỉ** — tức 0% giá trị. Đếm bảng là một chỉ số **có thể tăng trong khi kết quả vẫn là thất bại**; chỉ có test mới là thước.
>
> Hệ quả cắt lô: Story này **không được tách** thành "RLS cho schema `story`" + "RLS cho schema `comic`". Nó chỉ có hai trạng thái: **PASS** hoặc **chưa xong**.

### 5.2 Điều kiện ra ngoài horizon — ghi ra để không mất dấu

| # | Tiêu chí | Nguồn |
|---|---|---|
| 8 | Worker chết mà API vẫn phục vụ được (**test kill process**) | **M3-4** — MVP3, **NGOÀI horizon** |
| 9 | Billing provider được tích hợp trước bản trả phí có image gen | `FR-E-04` (MVP3) · [Roadmap §5.1](../../010-Planning/Roadmap.md#51-cái-gì-rơi-ra-khỏi-092026022027) |

### 5.3 Ba điều KHÔNG thuộc DoD của Epic này

1. ⛔ **Không** có tiêu chí *"cập nhật MOC"* — **PM giữ MOC** ở close-step của run, không phải Epic.
2. ⛔ **Không** có tiêu chí về `usage_event`, credit ledger, hard quota — thuộc [Epic-F](./Epic-Credit-And-Unit-Economics.md), `KC-7`.
3. ⛔ **Không** có tiêu chí về `change_log` / `field_provenance` / ràng buộc cùng transaction — thuộc [Epic-G](./Epic-Legal-And-Compliance.md), `KC-1`…`KC-4`. ⚠️ Nhưng **`KC-4` phụ thuộc Story `Story-Modular-Monolith-Three-Schemas` của Epic này** (một DB ⇒ một transaction boundary): đây là phụ thuộc chéo Epic, không phải một hạng mục bị bỏ.

---

## 6. Tài liệu liên quan

### 6.1 BRD cha & tầng Requirements

| Quan hệ | Tài liệu | Ghi chú |
|---|---|---|
| **BRD cha** | [BRD-005-Multi-Tenancy-And-Platform](../../020-Requirements/BRD/BRD-005-Multi-Tenancy-And-Platform.md) | **1:1 với Epic này** — traceability là một link, không phải một ma trận |
| PRD | [PRD-Comic-Studio — E. Multi-tenancy & hạ tầng](../../020-Requirements/PRD-Comic-Studio.md#e-multi-tenancy--hạ-tầng) | `FR-E-01`…`FR-E-06` |
| NFR chi tiết | [SRS-Comic-Studio](../../020-Requirements/SRS-Comic-Studio.md) | *Tenant isolation* là trục NFR số 1 của SRS |
| Epic phụ thuộc chéo | [Epic-Credit-And-Unit-Economics](./Epic-Credit-And-Unit-Economics.md) · [Epic-Legal-And-Compliance](./Epic-Legal-And-Compliance.md) | billing 3 tầng · `KC-4` cùng transaction, `GP-5` hard-delete tenant |

### 6.2 Use Case liên quan

**Epic-E không sở hữu Use Case nào — và đó là CÓ CHỦ Ý, không phải thiếu sót** ([BRD-005 §7.2](../../020-Requirements/BRD/BRD-005-Multi-Tenancy-And-Platform.md#72-use-case)):

- Luồng **signup / tạo tenant** không có UC vì `E4` là *"mua auth, không tự viết"* ⇒ luồng đó do **vendor sở hữu**; viết spec cho thứ mình không điều khiển là spec không thực thi được.
- `tenant_id` + RLS, modular monolith, storage tách tenant là **thuộc tính xuyên suốt hệ thống** (NFR/schema requirement), **không** phải một tương tác goal-level của actor ⇒ chúng được kiểm chứng bằng **test rò rỉ chéo tenant** (`M1-1`), không bằng một màn hình.
- Hệ quả: Epic-E xuất hiện như **precondition** trong **mọi** UC có dữ liệu người dùng — ví dụ [UC-01 — Upload And Ingest Chapter](../../020-Requirements/Use-Cases/UC-01-Upload-And-Ingest-Chapter.md) là nơi đầu tiên biên tenant bị vận dụng trên dữ liệu thật.

### 6.3 Tài liệu tham khảo

- [MVP-Scope.md](../../010-Planning/MVP-Scope.md) — **§3** nhóm E (nguồn của [mục 3](#3-story-trong-horizon) và [mục 4](#4-story-ngoài-horizon--chưa-có-file)) · **§6 KC-5** (và `KC-4` qua phụ thuộc chéo) · **§4.2** (cắt microservices) · §1.1 (ranh giới ba tài liệu) · §7 ba gate
- [Roadmap.md](../../010-Planning/Roadmap.md) — **§2** exit criteria **M1-1**, **M3-4** (nguồn của [mục 5](#5-definition-of-done-cấp-epic)) · **§5.1** (MVP3 rơi ra ngoài horizon)
- [Charter-Comic-Studio.md](../../010-Planning/Charter-Comic-Studio.md) — §5.2 *Scope Out* (`E6`) · §7 ràng buộc · §8 giả định **A7** (multi-tenancy **15–25%** `[EM]`)
- [Glossary.md](../../999-Resources/Glossary.md) — `tenant_id` · `RLS` · *seam kinh tế vs seam kỹ thuật* · `MVP0`
- [findings/business-analyst.md](../../010-Planning/pm-runs/2026-08-24-khoi-tao-requirements-stories-comic-studio/findings/business-analyst.md) — **§2.3** (trục Epic) · **§4.5** (bảng 7 Story của Epic này) · **§4.10** (Story vỡ khi cắt lô) · **§5.2** bảng canonical facts · **§5.3** 18 lệnh cấm
- [Documents-Template.md](../../../knowledge-base/99-Templates/Documents-Template.md) — **RULE-001**: thư mục, naming `Epic-{Title}.md`, frontmatter, và quy tắc **standard markdown link** (⛔ cấm wiki-link `[[...]]`)

> ⛔ **Không link tới `docs/030-Specs/`** — tầng technical spec chưa tồn tại và nằm ngoài scope của run này.
