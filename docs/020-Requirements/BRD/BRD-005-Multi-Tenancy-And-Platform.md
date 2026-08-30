---
id: BRD-005
type: brd
status: draft
project: comic-studio
created: 2026-08-24
---

# BRD-005 — Multi-tenancy & hạ tầng (module E)

> [!IMPORTANT]
> **Quy ước nhãn nguồn số liệu** (kế thừa nguyên vẹn — **số và nhãn là một cặp không tách rời**):
> `[OFF]` nguồn official/paper gốc · `[BCN]` báo cáo ngành có tên firm · `[TC]` nguồn thứ cấp · `[EM]` ước lượng hoặc phép nhân, **không phải số đo** · `[CHỐT]` quyết định của Founder tại gate.
>
> Tài liệu này **chỉ trích lại** số liệu từ tầng Planning. Không tự tra lại, không tự tính lại (`CẤM-15`).

## Mục lục

1. [Business goal](#1-business-goal)
2. [Phạm vi module](#2-phạm-vi-module)
3. [Yêu cầu nghiệp vụ](#3-yêu-cầu-nghiệp-vụ)
4. [Ràng buộc & điều kiện chặn](#4-ràng-buộc--điều-kiện-chặn)
5. [Cái module này KHÔNG làm](#5-cái-module-này-không-làm)
6. [Rủi ro chính](#6-rủi-ro-chính)
7. [Tài liệu liên quan](#7-tài-liệu-liên-quan)

---

## 1. Business goal

> Nền multi-tenant an toàn từ commit đầu tiên: `tenant_id` + RLS + storage tách tenant, trên kiến trúc **modular monolith**. Khối này chiếm **15–25%** effort `[EM]` (CF-6.9) mà `Request.md` gốc **không nhắc một dòng**.

Ba điều làm module này khác các module khác:

| # | Đặc điểm | Hệ quả |
|---|---|---|
| 1 | **Sản phẩm là SaaS thương mại multi-tenant** — nền tảng cho **người khác tự upload truyện của họ** `[CHỐT]` CF-1.1 | `tenant_id` không phải một tính năng, nó là **tiền đề của mọi bảng** |
| 2 | Effort **15–25%** `[EM]` (CF-6.9) hoàn toàn **không có trong tài liệu gốc** | Nếu ước thiếu, *"nó không lấy chỗ của tính năng — nó lấy chỗ của **thời gian không tồn tại**"* ([Charter §8](../../010-Planning/Charter-Comic-Studio.md#8-giả-định-assumptions) A7) |
| 3 | Ngân sách cho khối này **đến từ** phần tiết kiệm của việc cắt canvas (NT-4) | Cắt canvas mà không hiểu điều này sẽ dẫn tới **ảo tưởng "còn dư thời gian"** ([MVP-Scope §2](../../010-Planning/MVP-Scope.md#2-nguyên-tắc-cắt-scope) NT-4) |

> ⚠️ **Con số 15–25% là `[EM]`** — ước lượng của lens kiến trúc, không phải số đo. ⛔ Nó **không** được trừ đi hay cộng vào con số effort editor **~20–25%** `[EM]` (CF-6.7, mẫu số **SaaS — đã bao gồm chính khối multi-tenancy này**) — xem cảnh báo mẫu số ở [MVP-Scope §5.1](../../010-Planning/MVP-Scope.md#51--cảnh-báo-mẫu-số--đọc-trước-khi-nhìn-bất-kỳ-con-số--nào) và `CẤM-01`.

---

## 2. Phạm vi module

Bảng dưới là **các hàng của nhóm `E. Multi-tenancy & hạ tầng`** trong [MVP-Scope §3](../../010-Planning/MVP-Scope.md#3-bảng-mvp-vs-full-scope) mà BRD-005 **bao**. Nhãn từng mốc copy nguyên bảng gốc.

**Ký hiệu**: ✅ có đầy đủ · 🟡 có một phần / bản tối thiểu · ⛔ hoãn sang mốc sau · ❌ **cắt hẳn, không có trong Full Scope**

| # | Hạng mục | MVP0 | MVP1 | MVP2 | MVP3 | MVP4 | Full Scope | Căn cứ |
|---|---|:--:|:--:|:--:|:--:|:--:|:--:|---|
| **E1** | `tenant_id NOT NULL` mọi bảng + cột **đầu tiên** mọi composite index + Postgres RLS | ❌ không DB | ✅ | ✅ | ✅ | ✅ | ✅ | CF-8.7 *"`tenant_id` từ ngày đầu"* · CF-6.9 **15–25%** `[EM]` |
| **E2** | `tenant` / `user` / `membership` là ba entity riêng (kể cả khi 1:1) | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | Analysis §5.7 quyết định #2 |
| **E3** | Object storage `tenant/{tenant_id}/{sha256}`, **không dedup chéo tenant** | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | Analysis §5.7 #4 — dedup chéo mâu thuẫn trực tiếp với lập luận bản quyền |
| **E4** | Mua auth + billing (không tự viết) | ❌ | ✅ auth | ✅ | ✅ +billing | ✅ | ✅ | Analysis §5.7 — *"tự viết auth là cách nhanh nhất để một dev đốt hai tháng và vẫn có lỗ hổng"* |
| **E5** | Modular monolith: 1 process, 1 PostgreSQL, 3 schema (`story`/`comic`/`generation`) | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | CF-9.2 — lý do **MẠNH LÊN** dưới SaaS |
| **E7** | Worker là process triển khai riêng, **cùng codebase** (2 entrypoint) | ❌ | ⛔ | ⛔ | ✅ | ✅ | ✅ | Analysis §6.2 seam kinh tế — worker chết mà API vẫn sống ⇒ không churn |

> Hai hàng còn lại của nhóm E (**E6**, **E8**) nằm ở [mục 5](#5-cái-module-này-không-làm). Mỗi hàng của nhóm E xuất hiện **đúng một lần** trong tài liệu này.

### 2.1 Năm seam ĐÚNG chỗ được giữ (miễn phí trong monolith)

Nguồn: [MVP-Scope §4.2](../../010-Planning/MVP-Scope.md#42-microservices--vector-db-12--cắt-cf-92). Đây là lý do việc cắt microservices **không** làm mất tính module hoá.

| Seam | Nội dung | Chủ sở hữu requirement |
|---|---|---|
| 1 | Async job interface `enqueue(spec) → job_id → poll` | **BRD-005** (`BR-005-08`) |
| 2 | Object Storage **content-addressed** | **BRD-005** (`BR-005-03`) |
| 3 | Module interface `story` / `comic` / `generation`, với luật `comic` gọi `story` **chỉ qua** `resolveState()` và `getBible()` — enforce bằng **lint rule** | **BRD-005** (`BR-005-06`) |
| 4 | Adapter per image provider | [BRD-001](./BRD-001-Image-Generation-Pipeline.md) (hàng A4) |
| 5 | Visual Prompt Compiler là **library thuần** | [BRD-001](./BRD-001-Image-Generation-Pipeline.md) (hàng A3) |

> `Glossary.md` phân định: **seam kinh tế** (worker process riêng, fairness per-tenant khi claim job, `usage_event` tách bạch) khác **seam kỹ thuật** (microservices). *"Với một dev, seam kinh tế đáng làm; seam kỹ thuật thì không."*

---

## 3. Yêu cầu nghiệp vụ

| ID | Phát biểu | Căn cứ (file + mục) | Mốc MVP |
|---|---|---|---|
| **BR-005-01** ⭐ | **MỌI** bảng nghiệp vụ phải có `tenant_id NOT NULL`, và `tenant_id` phải là **cột ĐẦU TIÊN** của **mọi** composite index; cộng thêm **Postgres RLS** làm lớp phòng thủ thứ hai. Điều kiện xác nhận **không** phải *"số bảng đã sửa"* mà là **test rò rỉ chéo tenant PASS** | `MVP-Scope` [§6](../../010-Planning/MVP-Scope.md#6-không-được-cắt--danh-sách-cứng) **KC-5** · §3 hàng **E1** · CF-8.7 · `Roadmap` §2 **M1-1** · `Glossary.md` *`tenant_id`*, *RLS* | **MVP1 — ngày đầu** |
| **BR-005-02** | `tenant` / `user` / `membership` phải là **ba entity riêng biệt**, kể cả khi quan hệ thực tế đang là **1:1**. Lý do nghiệp vụ: ngày bán **gói team** không phải migrate mô hình định danh | `MVP-Scope` §3 **E2** · Analysis §5.7 quyết định #2 · `MVP-Scope` §5.3 hàng #8 (*"`membership` đã chuẩn bị sẵn cho ngày đó"*) | **MVP1** |
| **BR-005-03** | File của tenant phải nằm ở đường dẫn `tenant/{tenant_id}/{sha256}` trong object storage, **content-addressed**, và ⛔ **KHÔNG dedup chéo tenant** trong bất kỳ trường hợp nào | `MVP-Scope` §3 **E3** · Analysis §5.7 #4 (*"dedup chéo mâu thuẫn trực tiếp với lập luận bản quyền"*) · `MVP-Scope` §4.2 seam #2 | **MVP1** |
| **BR-005-04** | **Mua** authentication (MVP1) và **mua** billing (MVP3) từ nhà cung cấp — ⛔ **không tự viết**. Lý do: *"tự viết auth là cách nhanh nhất để một dev đốt hai tháng và vẫn có lỗ hổng"* | `MVP-Scope` §3 **E4** (`✅ auth` ở MVP1, `✅ +billing` ở MVP3) · Analysis §5.7 | **MVP1** (auth) · **MVP3** (billing) |
| **BR-005-05** | Kiến trúc là **modular monolith**: **1 process · 1 PostgreSQL · 3 schema** (`story` / `comic` / `generation`). Object Storage tách khỏi DB | `MVP-Scope` §3 **E5** · [§4.2](../../010-Planning/MVP-Scope.md#42-microservices--vector-db-12--cắt-cf-92) · CF-9.2 | **MVP1** |
| **BR-005-06** | Ranh giới module phải được **cưỡng chế bằng lint rule**, không bằng thoả thuận: module `comic` gọi module `story` **CHỈ qua** `resolveState()` và `getBible()` | `MVP-Scope` §4.2 (năm seam đúng chỗ, seam #3) | **MVP1** |
| **BR-005-07** | Worker phải là **process triển khai riêng nhưng CÙNG codebase** (2 entrypoint). Giá trị nghiệp vụ: **worker chết mà API vẫn phục vụ được** ⇒ một sự cố sinh ảnh không làm khách mất truy cập vào dữ liệu của họ ⇒ không churn | `MVP-Scope` §3 **E7** · Analysis §6.2 *seam kinh tế* · `Roadmap` §2 **M3-4** | **MVP3** — ⚠️ **NGOÀI horizon** ([Roadmap §5.1](../../010-Planning/Roadmap.md#51-cái-gì-rơi-ra-khỏi-092026022027)) |
| **BR-005-08** | Giao tiếp giữa API và worker theo interface async **`enqueue(spec) → job_id → poll`**; cập nhật trạng thái bằng **polling 2s**, ⛔ **không dùng WebSocket** | `MVP-Scope` §4.2 (quyết định *"polling 2s thay WebSocket"*) + seam #1 | **MVP1** |
| **BR-005-09** ⭐ | Kiến trúc phải bảo đảm **một transaction boundary duy nhất** để `INSERT generation` + `INSERT change_log` + `INSERT usage_event` **commit cùng nhau**. Đây là hệ quả trực tiếp của việc chọn 1 PostgreSQL, và là **điều kiện tồn tại** của nghĩa vụ audit | `MVP-Scope` §6 **KC-4** · §4.2 lý do 2 (*"bằng chứng có thể thiếu ngẫu nhiên thì không phải bằng chứng"*) · `Roadmap` §2 **M1-5** | **MVP1** |

---

## 4. Ràng buộc & điều kiện chặn

### 4.1 Danh sách cứng — `KC-x` của [MVP-Scope §6](../../010-Planning/MVP-Scope.md#6-không-được-cắt--danh-sách-cứng) mà module này chạm

| KC | Nội dung | Quan hệ với BRD-005 | Không giữ thì hỏng thế nào |
|---|---|---|---|
| **KC-5** ⭐ | `tenant_id NOT NULL` trên **MỌI** bảng, là **cột ĐẦU TIÊN** của mọi composite index, cộng **Postgres RLS**. Từ **MVP1 — ngày đầu**. Chi phí: một cột + policy RLS | **KC do BRD-005 sở hữu trực tiếp** (`BR-005-01`) | Retrofit `tenant_id` vào schema **đã có dữ liệu thật** là *"một trong những migration đắt nhất tồn tại"*: phải sửa mọi bảng, mọi query, mọi index, và **không có cách nào xác minh đã sửa hết**. Bỏ sót một chỗ = **rò rỉ dữ liệu chéo tenant** = **sự cố tồn vong** với một SaaS. RLS là lớp phòng thủ thứ hai — với 1 dev **không có code review**, đây là *"bảo hiểm rẻ nhất tồn tại"* |
| **KC-4** | KC-1 + KC-2 + KC-3 phải **commit CÙNG MỘT TRANSACTION** với artifact mà chúng chứng minh. Chi phí: **kỷ luật code + monolith 1 DB** | BRD-005 **cung cấp điều kiện kỹ thuật** cho KC-4 (`BR-005-05`, `BR-005-09`); nội dung nghĩa vụ thuộc [BRD-007](./BRD-007-Legal-And-Compliance.md) | Audit trail commit tách rời artifact là audit trail **không đáng tin về mặt pháp lý** |

> ⚠️ **Vì sao KC-4 là ràng buộc CHẶN của quyết định kiến trúc, không phải một ghi chú**: chính nghĩa vụ audit này là **lý do #2** khiến việc tách 2 database bị loại ([MVP-Scope §4.2](../../010-Planning/MVP-Scope.md#42-microservices--vector-db-12--cắt-cf-92)). Đảo lại: nếu ai đó mở lại E6, người đó **phải trả lời được** KC-4 sẽ được thoả bằng cách nào.

### 4.2 Ràng buộc cấp dự án — `C-x` của [Charter §7](../../010-Planning/Charter-Comic-Studio.md#7-ràng-buộc-constraints)

| C | Ràng buộc | Hệ quả bắt buộc với BRD-005 |
|---|---|---|
| **C1** | **Đội 1 người + AI assist. Không funding, không ngân sách marketing** `[CHỐT]` CF-1.2 | Là lý do của `BR-005-04` (mua auth/billing) và của toàn bộ quyết định monolith. Với 1 dev **không có code review**, RLS là lớp phòng thủ **bắt buộc**, không phải tuỳ chọn |
| **C2** | **Mô hình 3 tầng kiểu Novelcrafter đã CHỐT — không mở lại trong horizon này** `[CHỐT]` CF-2.1→2.4 | *"Kiến trúc billing, credit ledger và onboarding phải được thiết kế cho **ba** tầng ngay từ đầu, **không retrofit**"* ⇒ ràng buộc trực tiếp lên `BR-005-04` (billing) và lên [BRD-006](./BRD-006-Credit-And-Unit-Economics.md) |
| **C9** | **Thứ tự milestone cố định: MVP0 → MVP1 → MVP2 → MVP3 → MVP4** CF-8.3 | **MVP0 không có database** — đó là chủ ý, không phải thiếu sót ([MVP-Scope §3.1](../../010-Planning/MVP-Scope.md#31-ba-ô-đáng-chú-ý-nhất-trong-bảng): *"nếu MVP0 bắt đầu có schema, nó đã trượt khỏi định nghĩa"*). Mọi hàng E vì thế là `❌` ở MVP0 |
| **C10** | **Horizon 6 tháng CHƯA được ai xác nhận là đủ cho 1 dev** `[CHỐT]` CF-8.1 + CF-8.13 | ⛔ **Cấm nén lịch cho vừa khung** (`CẤM-08`). Theo [Roadmap §5.1](../../010-Planning/Roadmap.md#51-cái-gì-rơi-ra-khỏi-092026022027), **MVP3 rơi ra ngoài** ⇒ `BR-005-04` (billing) và `BR-005-07` (worker process riêng) nằm **NGOÀI** horizon |

### 4.3 Ràng buộc về ngân sách effort

Khối này được cấp **15–25%** `[EM]` (CF-6.9), lấy từ phần tiết kiệm của quyết định cắt canvas theo **NT-4** ([MVP-Scope §2](../../010-Planning/MVP-Scope.md#2-nguyên-tắc-cắt-scope)): *phần effort tiết kiệm được **không phải lãi** — nó là ngân sách cho khối multi-tenancy mà `Request.md` gốc không nhắc một dòng*.

⛔ **Cấm** thực hiện phép trừ giữa con số này và các con số effort editor (`CẤM-01`, `CẤM-15`) — chúng đứng trên các mẫu số khác nhau.

---

## 5. Cái module này KHÔNG làm

Hai hàng còn lại của nhóm `E` trong [MVP-Scope §3](../../010-Planning/MVP-Scope.md#3-bảng-mvp-vs-full-scope). Cột *Nhãn theo mốc* copy nguyên bảng gốc theo thứ tự `MVP0 · MVP1 · MVP2 · MVP3 · MVP4 · Full Scope`.

> ⚠️ **Hai hàng này KHÁC LOẠI nhau** — đừng đọc thành một: **E6 là `❌` cắt hẳn** (bị **loại khỏi thiết kế**), **E8 là `⛔` hoãn** (còn trong Full Scope, chỉ chưa có mốc).

| Hàng | Hạng mục | Nhãn theo mốc | Loại | Lý do | Điều kiện mở lại |
|---|---|---|---|---|---|
| **E6** ⛔ | **Microservices (3 service) + 2 PostgreSQL + Vector DB riêng + Job Queue riêng** | ❌ · ❌ · ❌ · ❌ · ❌ · ❌ **cắt hẳn** | **Cắt hẳn — loại khỏi thiết kế** | Ba lý do ở [mục 5.1](#51--vì-sao-e6-bị-cắt-hẳn-ba-lý-do-mạnh-lên-dưới-saas) | **KHÔNG có điều kiện mở lại trong `MVP-Scope`.** Ai đề xuất mở lại phải bác được **cả ba** lý do ở mục 5.1, đặc biệt phải trả lời **KC-4** sẽ thoả bằng cách nào |
| **E8** | SSO/SAML, custom domain, white-label, multi-region | ❌ · ❌ · ❌ · ❌ · ❌ · ⛔ | **Hoãn — vẫn trong Full Scope** | Analysis §5.7 xếp vào nhóm *"Hoãn được"* | `MVP-Scope` **không** ghi điều kiện mở lại cụ thể; hàng này `⛔` ở cột Full Scope tức **chưa có mốc nào được gán**. Em không đặt thêm điều kiện nào |

### 5.1 ⛔ Vì sao E6 bị CẮT HẲN — ba lý do MẠNH LÊN dưới SaaS

Nguồn: [MVP-Scope §4.2](../../010-Planning/MVP-Scope.md#42-microservices--vector-db-12--cắt-cf-92) · CF-9.2. Điểm quan trọng: dưới mô hình SaaS multi-tenant, lý do cắt **mạnh lên**, không yếu đi.

| # | Lý do | Vì sao nó **chặn** việc tách DB |
|---|---|---|
| **1** | **RLS không bảo vệ được join thực hiện phía application** | State resolution là truy vấn **xuyên** `story` ↔ `comic`. Hai DB ⇒ join phía ứng dụng ⇒ **lớp phòng thủ thứ hai biến mất đúng ở đường dẫn dữ liệu nóng nhất**. `Glossary.md` (*RLS*) ghi cùng giới hạn này |
| **2** | **Nghĩa vụ audit đòi MỘT transaction boundary** | `INSERT generation` + `INSERT change_log` + `INSERT usage_event` phải commit **cùng nhau** (KC-4). *"Bằng chứng có thể thiếu ngẫu nhiên thì không phải bằng chứng."* Hai DB = **mất transaction** |
| **3** | **Ngân sách effort đã bị multi-tenancy ăn mất 15–25%** `[EM]` | Effort đó phải lấy từ đâu đó; lấy từ hạ tầng phân tán là lựa chọn hiển nhiên đúng (NT-4) |

### 5.2 ⚠️ Phân biệt bắt buộc: **Vector DB riêng của E6** ≠ **`pgvector` của B5**

> [!CAUTION]
> Hai thứ này **không phải một**, và gộp chúng lại sẽ cấm sai một hạng mục **không bị cấm**.
>
> | | **E6 — Vector DB riêng** | **B5 — `pgvector`** |
> |---|---|---|
> | Bản chất | **Một service / một datastore TÁCH RIÊNG**, đi cùng microservices + 2 PostgreSQL + Job Queue riêng | Một **extension trong chính PostgreSQL** đang có |
> | Trạng thái | `❌` **cắt hẳn — loại khỏi thiết kế** ở **mọi** cột, kể cả Full Scope | `❌` MVP0–MVP2 · `⛔` MVP3–MVP4 · **Full Scope `🟡`** *"khi có bằng chứng SQL+FTS không đủ"* |
> | Có bị cấm không | **Có** — nó phá lý do 1 và lý do 2 ở [mục 5.1](#51--vì-sao-e6-bị-cắt-hẳn-ba-lý-do-mạnh-lên-dưới-saas) | **KHÔNG bị cấm.** Nó chỉ **chưa được ưu tiên**, và có **điều kiện mở** rõ ràng |
> | Chủ sở hữu | **BRD-005** (mục này) | [**BRD-002**](./BRD-002-Story-Intelligence.md) — hàng **B5**, ngoài phạm vi BRD-005 |
>
> Lý do hiện tại chưa cần vector search: *"Story Bible **là** index của mình"* (CF-9.2 · Analysis §6.2). Đó là lý do **ưu tiên**, không phải lệnh cấm kỹ thuật.

### 5.3 Ba thứ khác BRD-005 không sở hữu

| Hạng mục | Ai sở hữu | Vì sao ghi ra đây |
|---|---|---|
| **Job queue trong Postgres** (`FOR UPDATE SKIP LOCKED`, transactional enqueue) — hàng **A5**; **fairness per tenant** khi CLAIM job — hàng **A6** | [BRD-001](./BRD-001-Image-Generation-Pipeline.md) | BRD-005 sở hữu **interface** `enqueue → poll` (`BR-005-08`), không sở hữu cơ chế queue |
| **`usage_event` / credit ledger / hard quota / mô hình 3 tầng** (F1–F6) | [BRD-006](./BRD-006-Credit-And-Unit-Economics.md) | `BR-005-09` chỉ bảo đảm **transaction boundary** để `usage_event` commit cùng artifact |
| **ToS + user warrant + `ON DELETE CASCADE` + đường hard-delete tenant đã kiểm thử** (GP-5) | [BRD-007](./BRD-007-Legal-And-Compliance.md) | *"Đường thoát phải được xây cùng lúc với đường vào"* ([MVP-Scope §8.2](../../010-Planning/MVP-Scope.md#82-nghĩa-vụ-khi-kill--dừng-có-trật-tự)) — nó **dựa trên** E3 của BRD-005 nhưng không thuộc BRD-005 |
| **Realtime collaboration** (D4) | [BRD-004](./BRD-004-Minimum-Editor.md) | Khác hàng, khác module: BRD-005 quyết định **transport là polling 2s, không WebSocket** (`BR-005-08`); còn *"nhiều người sửa cùng lúc"* là hàng D4 và đã hoãn ở BRD-004 |

---

## 6. Rủi ro chính

Sổ rủi ro là [Risk-Register.md](../../010-Planning/Risk-Register.md). ⛔ **Tài liệu này không tự chấm điểm rủi ro mới** — chỉ trỏ tới hàng đã có.

| Rủi ro | Vì sao liên quan tới BRD-005 |
|---|---|
| [**R-16**](../../010-Planning/Risk-Register.md#21-bảng-chính) — Kỹ thuật ⭐ | **Chính là rủi ro trung tâm của module này**: multi-tenancy *"không có trong `Request.md` một dòng nào"* nhưng chiếm **15–25%** effort `[EM]`. Trigger đã ghi sẵn: migration tạo bảng nghiệp vụ **không có** `tenant_id`; query không scope theo tenant lọt qua review; endpoint trả dữ liệu theo `id` mà không kiểm tenant ownership ⇒ ba trigger này là **checklist review** của `BR-005-01`. ⚠️ Cột *Residual Risk* của R-16 nhắc lại **cảnh báo hai mẫu số** |
| [**R-01**](../../010-Planning/Risk-Register.md#21-bảng-chính) — Pháp lý, Score **9** | BRD-005 là nơi **điều kiện kỹ thuật** của R-01 được bảo đảm: một DB ⇒ một transaction boundary ⇒ audit trail commit cùng artifact (`BR-005-09`, KC-4). Mất điều kiện này thì mitigation của R-01 **không thực thi được**, dù schema có đủ cột |
| [**R-21**](../../010-Planning/Risk-Register.md#21-bảng-chính) — Vận hành, `accepted` | **Bus factor = 1.** Mitigation ghi thẳng *"giữ dự án ở trạng thái **có thể bỏ dở và quay lại**: monolith (CF-9.2)"* ⇒ `BR-005-05` là một **quyết định vận hành**, không chỉ là quyết định kiến trúc |

---

## 7. Tài liệu liên quan

### 7.1 Tầng Requirements & Backlog

| Loại | Tài liệu | Quan hệ |
|---|---|---|
| PRD | [PRD-Comic-Studio.md](../PRD-Comic-Studio.md) | BRD-005 chi tiết hoá mục *Multi-tenancy & hạ tầng* của PRD |
| SRS | [SRS-Comic-Studio.md](../SRS-Comic-Studio.md) | Yêu cầu hệ thống tương ứng |
| Epic | [Epic-Multi-Tenancy-And-Platform.md](../../022-User-Stories/Epics/Epic-Multi-Tenancy-And-Platform.md) | Epic 1:1 với BRD-005 |
| BRD liên quan | [BRD-001](./BRD-001-Image-Generation-Pipeline.md) (A5/A6 job queue, seam #4/#5) · [BRD-002](./BRD-002-Story-Intelligence.md) (**B5 `pgvector` — phân biệt với E6**) · [BRD-004](./BRD-004-Minimum-Editor.md) (D4 realtime collab) · [BRD-006](./BRD-006-Credit-And-Unit-Economics.md) (billing 3 tầng, `usage_event`) · [BRD-007](./BRD-007-Legal-And-Compliance.md) (KC-4, GP-5) | Phụ thuộc chéo |

### 7.2 Use Case

**BRD-005 không có Use Case riêng trong danh sách UC của run này** — và đó là **có chủ ý**, không phải thiếu sót:

- Luồng **signup / tạo tenant** không có UC vì `E4` là *"mua auth, không tự viết"* ⇒ luồng đó do **vendor sở hữu**; viết spec cho thứ mình không điều khiển là spec không thực thi được ([findings §3.3](../../010-Planning/pm-runs/2026-08-24-khoi-tao-requirements-stories-comic-studio/findings/business-analyst.md)).
- `tenant_id` + RLS, monolith, storage tách tenant là **thuộc tính xuyên suốt hệ thống** (NFR/schema requirement), **không** phải một tương tác goal-level của actor ⇒ chúng được kiểm chứng bằng **test rò rỉ chéo tenant** (`Roadmap` §2 **M1-1**), không bằng một màn hình.
- Hệ quả: BRD-005 xuất hiện như **precondition** trong **mọi** UC có dữ liệu người dùng, thay vì có một UC riêng.

### 7.3 Nguồn Planning & Research

- [MVP-Scope.md](../../010-Planning/MVP-Scope.md) — **§3** nhóm E (nguồn của [mục 2](#2-phạm-vi-module) và [mục 5](#5-cái-module-này-không-làm)) · **§4.2** (cắt microservices, ba lý do, năm seam) · **§6** KC-4, KC-5 · §2 NT-3/NT-4 · §3.1 (MVP0 không có DB) · §8.2
- [Charter-Comic-Studio.md](../../010-Planning/Charter-Comic-Studio.md) — **§7** ràng buộc C1, C2, C9, C10 · §8 giả định **A7** (multi-tenancy 15–25% `[EM]`)
- [Roadmap.md](../../010-Planning/Roadmap.md) — **§5.1** (MVP3 rơi ra ngoài horizon ⇒ billing và worker process riêng nằm ngoài)
- [Risk-Register.md](../../010-Planning/Risk-Register.md) — R-16, R-01, R-21
- [Glossary.md](../../999-Resources/Glossary.md) — `tenant_id`, `RLS`, `seam kinh tế vs seam kỹ thuật`
- [Analysis-Comic-Studio-Concept.md](../../050-Research/Analysis-Comic-Studio-Concept.md) — §5.7 (bảy quyết định SaaS), §6.2 (năm seam). ⛔ **Không sửa tài liệu này** (`CẤM-18`)

> ⛔ **Không link tới `docs/030-Specs/`**: tầng technical spec chưa tồn tại và nằm ngoài scope của run này.

---

_BRD by Comic Studio — role `business-analyst`._
_Author: trisjr_
