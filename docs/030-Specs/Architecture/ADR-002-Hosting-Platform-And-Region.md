---
id: ADR-002
type: adr
status: accepted
project: comic-studio
created: 2026-08-29
updated: 2026-08-30
---

# ADR-002: Hosting platform, mô hình triển khai và region

Related to: [SDD-Comic-Studio](./SDD-Comic-Studio.md)

## Context

`SRS-NFR-07` (*"Hosting / PaaS / container platform / region đặt máy"*) là **`CHƯA QUYẾT` → `TBD`**: [SRS-Comic-Studio](../../020-Requirements/SRS-Comic-Studio.md) §3.E ghi *"Không anchor được — grep toàn `docs/010-Planning/`, `Analysis`, `Glossary` không có quyết định nào"*, và §4.2 lặp lại *"sẽ được đặc tả tại tầng 030-Specs"*.

Run Phase 2 này **không spawn một lens DevOps riêng**. ⇒ ADR này cũng là nơi trả lời câu hỏi *"kiến trúc đã chọn có phù hợp cloud-native không"* — xem mục [Kiểm cloud-native](#kiểm-cloud-native-12-factor).

### Ràng buộc kế thừa (⛔ không mở lại)

| Ràng buộc | Mã | Hệ quả cho platform |
|---|---|---|
| Hai entrypoint (`api`, `worker`) trên **cùng một image**, khác command; *"worker chết mà API vẫn sống"* | `D-02` | Platform phải chạy được **≥2 process type từ một artifact** |
| ⛔ **Không mua GPU** — API cho main path | `D-07` | ⛔ Không chọn platform vì GPU. Compute là CPU thuần |
| **Hoãn multi-region** khỏi horizon | `D-08` | ⛔ **Một region.** Không thiết kế cho nhiều region, không mở lại ở ADR này |
| Job queue **trong PostgreSQL**, ⛔ không broker ngoài | `D-03`, `D-05` | ⛔ Không dùng queue/pub-sub của platform |
| Object storage **tách khỏi DB từ ngày đầu** | `D-13` | Storage nằm **ngoài** runtime — xem [ADR-004](./ADR-004-Object-Storage-Vendor-And-Signed-URL.md) |
| Đội **1 người + AI assist** | `SRS` §1.3 | ⛔ Không Kubernetes. Mọi giờ dành cho hạ tầng là giờ không dành cho sản phẩm |

### Hai ràng buộc dẫn xuất mà không tài liệu nào nói thẳng — nhưng quyết định platform

1. **Database này chứa bằng chứng pháp lý, không chỉ dữ liệu nghiệp vụ.** `change_log` append-only ghi mọi hành động người dùng (`D-48`), chuỗi provenance `parent_generation_id` (`D-47`), và `KC-4` bắt ba thứ đó commit cùng một transaction với artifact chúng chứng minh (`D-50`) — *"Bằng chứng có thể thiếu ngẫu nhiên thì không phải bằng chứng."* Mất database **không phải** mất dữ liệu có thể sinh lại; đó là mất khả năng chứng minh *decisive contribution*.
   ⇒ **PostgreSQL phải là managed service có PITR và backup tự động**, kể cả khi `RPO/RTO/backup retention` vẫn là `TBD` (`SRS` §5.2).
2. **Hệ thống cần một cái đồng hồ.** Hold reaper cho `expires_at` (`D-60`), rollup `usage_daily` (`D-58`), golden dataset regression chạy **định kỳ** (`D-66`), và SLA tiếp nhận takedown **72 giờ** (`D-54`) đều cần scheduled execution.
   ⇒ Platform phải có scheduled job, hoặc phải chấp nhận một process thứ ba.

### Vì sao phải quyết bây giờ

Lựa chọn platform quyết định hình dạng của Dockerfile, của cấu hình, và của đường deploy — tức là quyết định ngay ở commit đầu tiên. Và nó là đầu vào của [ADR-004](./ADR-004-Object-Storage-Vendor-And-Signed-URL.md) (vendor storage) lẫn ADR-006 (connection pooling ảnh hưởng cách bơm tenant context).

## Decision

### Tầng CHỐT — mô hình triển khai, ⛔ không đổi mà không viết ADR mới

1. **Container PaaS được quản lý.** ⛔ Không Kubernetes (tự quản hay managed). ⛔ Không tự quản VM cho main path.
2. **Build một lần → một image → hai process type.** Image được build, push lên registry và **cả `api` lẫn `worker` deploy cùng một image digest**, khác command. Đây là cách thoả `D-02` mà **không** phụ thuộc ngữ nghĩa build của platform nào.
   ⚠️ **Sắc thái của `E7`**: `D-02` là **CHỐT** về việc *hai entrypoint tồn tại từ commit đầu tiên*; còn *tách deploy thật sự* chỉ `✅` từ **MVP3**. ⇒ Ở MVP1/MVP2, chạy hai process trên cùng một instance **không vi phạm** ADR này, miễn là hai command đã tồn tại và tách được bằng cấu hình.
3. **Scheduled job chỉ được phép GỌI một subcommand của chính image đó.** ⛔ Không một dòng logic nghiệp vụ nào sống trong cấu hình cron của platform. Cron của vendor là *trigger*, không phải *code*.
4. **PostgreSQL là managed service có PITR + backup tự động + một đường restore ĐÃ DIỄN TẬP.** ⛔ Không self-host Postgres trên VM. Diễn tập restore là **điều kiện phát hành**, không phải hạng mục backlog — kể cả khi chưa có số RPO/RTO.
5. **Đúng MỘT region**, đặt tại điểm hiện diện gần Việt Nam nhất mà platform có (thực tế: **Singapore**). ⛔ Không thiết kế multi-region (`D-08`).
6. ⭐ **Portability guardrail — đây là phần bền nhất của ADR này.** ⛔ **Cấm** để primitive độc quyền của platform rò vào code:
   - ⛔ không queue/pub-sub của vendor (`D-03` đã cấm broker ngoài — điều này chỉ là hệ quả);
   - ⛔ không SDK secret manager — cấu hình **chỉ** qua biến môi trường;
   - ⛔ không API object storage riêng của vendor — **chỉ** tập con S3 (`PutObject`, `GetObject`, `HeadObject`, `DeleteObject`, presign);
   - ⛔ không ghi log ra file — log ra `stdout`/`stderr`;
   - ⛔ không lưu trạng thái trên đĩa cục bộ của instance.

   **Tiêu chí kiểm (kiểm được bằng mắt, không cần chạy)**: *đổi platform = đổi target deploy + connection string + biến môi trường; ⛔ không sửa một dòng code nghiệp vụ nào.*

### Tầng MẶC ĐỊNH — đã chọn, có đường lui

**Render, region Singapore** — ánh xạ trực tiếp: `Web Service` (`api`) · `Background Worker` (`worker`) · `Cron Job` (đồng hồ) · `Managed PostgreSQL`. Lý do chọn: đây là platform có **ít khái niệm nhất** vẫn phủ đủ bốn thứ trên, và bốn thứ đó là toàn bộ nhu cầu hạ tầng của kiến trúc này.

> [!WARNING]
> ⚠️ **Phải verify trước khi mua, ⛔ không được coi là đã xác nhận trong ADR này**: (a) region Singapore có sẵn cho **cả** compute lẫn managed Postgres; (b) PITR/backup tự động thuộc gói nào; (c) giới hạn của cron job. **Owner: dev · Mốc: trước lần deploy MVP0 đầu tiên.** ⛔ ADR này **không dán giá** cho bất kỳ dòng nào — mọi con số chi phí phải đo, không phỏng đoán.

**Thang đường lui đã ghi rõ:**

| Bậc | Phương án | Kích hoạt khi |
|:--:|---|---|
| 1 | **Fly.io** (`[processes]` từ một image) + managed Postgres bên thứ ba | Render thiếu region/khả năng cần thiết, nhưng vẫn muốn PaaS nhẹ |
| 2 | **GCP Cloud Run + Cloud SQL** (`asia-southeast1`) | Khi proximity tới image provider mặc định (Gemini, `D-40`) trở thành yếu tố **đo được**, không phải phỏng đoán |
| 3 | **AWS ECS Fargate + RDS** (`ap-southeast-1`) | Khi compliance hoặc scale đòi kiểm soát mạng/IAM chi tiết |

Nhờ điều 6 (portability guardrail), cả ba bậc đều là **thay đổi cấu hình**, không phải viết lại.

### `TBD` — ⛔ không tự gán

| Chưa quyết | Vì sao | Ai đóng | Khi nào |
|---|---|---|---|
| Uptime/availability SLA · RPO/RTO/backup retention · throughput job/giờ · ngưỡng cảnh báo queue depth | `SRS` §5.2 **cấm gán số** cho nhóm NFR này; ràng buộc gần nhất chỉ là **định tính**: *"worker chết mà API vẫn sống"* (`SRS` `SRS-NFR-03`) | Founder + dev, sau khi MVP0 có số đo | Sau MVP0 |
| **Nghĩa vụ lưu trữ dữ liệu trong lãnh thổ Việt Nam** theo pháp luật an ninh mạng | ⛔ **Không tài liệu nào trong repo trả lời**, và em ⛔ không khẳng định nội dung pháp lý | **Luật sư SHTT/tuân thủ** — nhập vào cùng gói câu hỏi của `SRS-NFR-17` (`SRS` §3.G) | Trước khi có khách hàng trả tiền |
| Có cần CDN trước ảnh không | Phụ thuộc vendor storage | Dev | [ADR-004](./ADR-004-Object-Storage-Vendor-And-Signed-URL.md) + số đo MVP0 |
| **Mã hoá dữ liệu (at rest / in transit) + quản lý secret** · **mục tiêu scalability/capacity** · **stack observability** | `SRS` §5.2: hàng `b-1` và `b-5` neo vào **`SRS-NFR-07`** — tức neo vào chính ADR này; hàng `b-7` thì ⛔ **không** neo vào `SRS-NFR-07` (`SRS` ghi *"chưa ai phát biểu observability thành một hạng mục"*), nhưng ADR này vẫn được nêu tên ở đó vì nó **tuyên bố ⛔ không đóng** hàng ấy. ⚠️ **ADR này đóng việc CHỌN platform, ⛔ KHÔNG đóng ba hàng đó**: điều 6 chỉ quyết *cách nạp cấu hình* (biến môi trường), ⛔ không quyết nghĩa vụ mã hoá hay ngưỡng quy mô | Dev (`b-1`, `b-7`) · Founder + dev (`b-5`) | Sau khi platform được mua và MVP0 có số đo |

> ⚠️ Hàng thứ hai là **reopen trigger duy nhất được ghi trước** của ADR này: nếu luật sư trả lời *"dữ liệu phải nằm trong lãnh thổ Việt Nam"*, thì **cả ADR-002 và ADR-004 phải mở lại**. Ghi trước để việc mở lại là *thực thi kế hoạch*, không phải *sự cố*.

### Kiểm cloud-native (12-factor)

| Yếu tố | Kiến trúc này | Đạt? |
|---|---|:--:|
| Codebase | Một repo, hai entrypoint (`D-02`) | ✅ |
| Config | Chỉ biến môi trường (điều 6) | ✅ |
| Backing services | Postgres + object storage là resource gắn qua URL/credential | ✅ |
| Build / release / run | Build một lần → image digest → deploy (điều 2) | ✅ |
| Processes | Stateless; ⛔ không state trên đĩa cục bộ (điều 6) | ✅ |
| Concurrency | Scale ngang bằng cách thêm instance `worker`; fairness per tenant nằm trong câu CLAIM (`D-42`) | ✅ |
| Disposability | Worker claim job bằng `FOR UPDATE SKIP LOCKED` ⇒ instance chết giữa chừng thì job quay lại hàng đợi | ✅ |
| Dev/prod parity | Cùng image, khác biến môi trường | ✅ |
| Logs | `stdout` (điều 6) | ✅ |
| Admin processes | Subcommand của cùng image (điều 3) | ✅ |

**Một độ lệch có chủ ý, và nó là CHỐT**: backing service cho queue **không phải** một message broker mà là chính PostgreSQL (`D-03`). Điều này **không phá cloud-native** — trạng thái queue nằm ở tầng dữ liệu được quản lý, process vẫn disposable và stateless, và ta đổi lấy thứ broker ngoài **không** cho được: *transactional enqueue* — `INSERT generation` và `INSERT job` trong **một** transaction, nên ⛔ không bao giờ có job mồ côi. Với 1 dev, một backing service ít hơn cũng là một trang runbook ít hơn.

## Alternatives considered

### A. Kubernetes (EKS / GKE / k3s tự quản)

- **Ưu điểm thật**: mô hình process/job/cronjob khớp gần như 1-1 với nhu cầu; portable nhất về lý thuyết.
- **Loại vì**: vi phạm trực diện `SRS` §1.3. Với một người, Kubernetes là một sản phẩm phụ phải vận hành song song với sản phẩm chính. Lợi ích của nó (multi-service orchestration, autoscaling tinh vi) đều nằm ở những bài toán mà `D-01` (modular monolith) và `D-08` (hoãn multi-region) đã **cố ý loại bỏ**.

### B. VPS + Docker Compose (Hetzner / DigitalOcean / VPS Việt Nam)

- **Ưu điểm thật**: rẻ nhất, kiểm soát cao nhất, và VPS đặt tại Việt Nam là câu trả lời sẵn nếu nghĩa vụ lưu trữ trong nước là có thật.
- **Loại vì vị trí của rủi ro, không phải vì năng lực**: nó buộc ta **tự vận hành PostgreSQL** — backup, PITR, vá lỗi, failover. Mà theo ràng buộc dẫn xuất #1 ở trên, database này là **kho bằng chứng pháp lý**. Đặt trách nhiệm backup của kho bằng chứng lên một người không có on-call là đánh cược sai chỗ.
- ⚠️ **Giữ lại như phương án dự phòng có điều kiện**: nếu luật sư xác nhận nghĩa vụ lưu trữ trong nước, phương án này quay lại bàn — nhưng khi đó *"managed Postgres"* trở thành yêu cầu đi mua ở nhà cung cấp trong nước, ⛔ không phải bỏ điều 4.

### C. Serverless function thuần (Lambda / function của platform frontend)

- **Ưu điểm thật**: không phải nghĩ về instance, trả theo lần gọi, hợp với API có traffic thấp lúc đầu.
- **Loại vì ba lý do độc lập**:
  1. Worker là **long-lived claim loop** đọc Postgres bằng `FOR UPDATE SKIP LOCKED` (`D-03`) — mô hình function chạy theo sự kiện phải giả lập vòng lặp này bằng cron mịn, làm hỏng đúng thuộc tính đang mua.
  2. Sinh ảnh đi qua **batch API** (`D-41`), job dài — đụng trần thời gian chạy của function.
  3. Nhiều instance function × connection Postgres là bài toán connection pooling đã biết, và nó **va trực tiếp** vào ADR-006 (`SET LOCAL` phải nằm đúng connection của transaction).

### D. GCP Cloud Run + Cloud SQL

- **Ưu điểm thật**: cùng nhà với image provider mặc định (Gemini, `D-40`); `asia-southeast1` là Singapore; scale-to-zero cho `api`.
- **Không loại — hạ xuống bậc 2 của thang đường lui**: mô hình request-driven buộc `worker` phải cấu hình `min-instances` và CPU always-allocated để giữ claim loop, tức là trả tiền như một service thường nhưng chịu thêm ràng buộc; cộng bề mặt cấu hình (IAM, VPC connector tới Cloud SQL) lớn hơn hẳn. Với `SRS` §1.3, chi phí đó chưa được biện minh **cho tới khi** proximity tới Gemini được **đo**, chứ không phải phỏng đoán.

### E. AWS ECS Fargate + RDS

- **Ưu điểm thật**: chuẩn công nghiệp, task definition từ cùng một image là hiện thực rất sạch của `D-02`, RDS là managed Postgres trưởng thành nhất, `ap-southeast-1` sẵn có.
- **Không loại — là bậc 3 của thang đường lui**: bề mặt cấu hình ban đầu (VPC, subnet, security group, ALB, IAM role, task definition) là nhiều ngày công cho một người, đổi lại năng lực (kiểm soát mạng, compliance) mà horizon MVP0–MVP2 **chưa cần**. Đây là quyết định *"chưa phải bây giờ"*, ⛔ không phải *"không bao giờ"*.

### F. Fly.io + Postgres của Fly

- **Ưu điểm thật**: khối `[processes]` chạy nhiều process type từ **đúng một image** là khớp với `D-02` sát nghĩa đen nhất trong tất cả phương án; có điểm hiện diện gần Việt Nam.
- **Loại một nửa**: phần runtime giữ lại làm **bậc 1** của thang đường lui; phần database **không** — vì Postgres của Fly về bản chất là *bạn tự vận hành trên hạ tầng của họ*, đụng thẳng điều 4 của `## Decision`. Dùng Fly thì phải ghép với managed Postgres bên thứ ba.

### G. Multi-region từ đầu · H. Mua GPU / self-host inference cho main path

⛔ **Không phải phương án và ⛔ không được đọc thành phương án.** `D-08` đã **CHỐT** hoãn multi-region; `D-07` đã **CHỐT** không mua GPU. Hai mục này tồn tại **chỉ để** một run sau không tưởng rằng chúng bị bỏ sót khi cân nhắc.

## Consequences

### Tích cực

- Toàn bộ hạ tầng gói gọn trong **bốn khái niệm**: một image, hai process type, một scheduled job, một managed database. Runbook ngắn là runbook được đọc.
- Portability guardrail (điều 6) biến *"chọn sai platform"* từ rủi ro kiến trúc thành rủi ro hoá đơn — chi phí đảo ngược được giới hạn **trước khi** ta biết mình chọn đúng hay sai.
- Disposability của worker được `D-03` cho không: instance chết giữa job thì job quay lại hàng đợi, ⛔ không cần cơ chế bù trừ riêng.

### Tiêu cực — cái gì trở nên KHÓ HƠN

1. **Một region ⇒ một điểm hỏng.** Sự cố region = downtime toàn hệ thống. Không có SLA nào bị vi phạm (uptime là `TBD`), nhưng Founder phải biết điều này **trước** khi bán, không phải sau.
2. **Người dùng ngoài Đông Nam Á chịu latency.** `D-08` đã chấp nhận đánh đổi này; ADR-002 chỉ ghi lại nó ở dạng vận hành.
3. **PaaS quản lý ⇒ trần kiểm soát.** Hệ quả #1 của [ADR-001](./ADR-001-Backend-And-Frontend-Tech-Stack.md) nói compositing 300 DPI là CPU-bound và phải chạy ở worker. Khi đó **instance type của worker trở thành nút thắt** — và trên PaaS ta chọn từ một thực đơn, không phải từ thị trường. Đây là chỗ nhiều khả năng phải leo thang đường lui nhất.
4. **Cấm primitive độc quyền ⇒ phải trả bằng tay.** Mỗi scheduled task là một subcommand ta tự viết và tự test, thay vì một ô cấu hình trên dashboard. Đây là chi phí có chủ ý để mua tính đảo ngược.
5. **Self-host cho LoRA train / upscale (`D-07` cho phép) KHÔNG nằm trên platform này.** Phần đó phải là compute riêng thuê theo giờ, gọi qua adapter. ⛔ Đừng kỳ vọng ADR này đã đỡ nó — nó chưa.
6. **Diễn tập restore là công việc thật, có lịch.** Không có số RPO/RTO **không** miễn nghĩa vụ chứng minh đường restore chạy được. Một bản backup chưa từng restore là một giả định, không phải một bản backup.

## Đã quyết ở đâu

### Kế thừa từ Phase 1 — ⛔ ADR này KHÔNG mở lại

| Quyết định | Mã `D-xx` | Nguồn (file + mã requirement) |
|---|---|---|
| Đội **1 người + AI assist**, không funding (`CF-1.2`) | — (ràng buộc bao trùm) | [SRS-Comic-Studio](../../020-Requirements/SRS-Comic-Studio.md) §1.3 |
| Worker là **process riêng, cùng codebase** — 2 entrypoint 1 image; *"worker chết mà API vẫn sống"* | `D-02` | `SRS` `SRS-NFR-03` · §2.3 · `MVP-Scope` §3 `E7` |
| Job queue **trong PostgreSQL**, `FOR UPDATE SKIP LOCKED`, transactional enqueue | `D-03` | `SRS` `SRS-FR-25` · §2.3 · §4.3 |
| ⛔ Không microservices · ⛔ không 2 PostgreSQL · ⛔ không job queue ngoài Postgres | `D-05` | `SRS` `SRS-NFR-21` · §6.1 |
| ⛔ **Không mua GPU** — API cho main path; self-host **chỉ** cho LoRA train / upscale / inpainting | `D-07` | `SRS` `SRS-NFR-11` · §2.3 · §4.2 |
| **Hoãn multi-region** khỏi horizon | `D-08` | `SRS` `SRS-NFR-26` · §2.3 · `MVP-Scope` §3 `E8` |
| Object storage tách khỏi DB từ ngày đầu | `D-13` | `SRS` `SRS-FR-02` · §2.3 · §4.3 |
| Fairness per tenant nằm **trong câu CLAIM** | `D-42` | `SRS` `SRS-FR-26` · §5.2 |
| Batch API, ⛔ không realtime API | `D-41` | `SRS` `SRS-FR-24` · §4.3 |
| `change_log` append-only ghi **mọi** hành động người dùng | `D-48` | `SRS` `SRS-FR-35` · §3.D · §4.1 |
| `KC-4`: provenance commit **cùng một transaction** với artifact | `D-50` | `SRS` `SRS-NFR-13` |
| Rollup `usage_daily` từ `usage_event` append-only | `D-58` | `SRS` `SRS-FR-30` |
| Hold reaper cho `expires_at` của credit hold | `D-60` | `SRS` `SRS-FR-28` · §3.F |
| Golden dataset regression chạy **định kỳ** | `D-66` | `SRS` `SRS-NFR-19` · §5.1 |
| SLA tiếp nhận takedown **72 giờ** `[OFF]` | `D-54` | `SRS` `SRS-FR-38` · §4.4 · §5.1 |
| ⛔ Cấm gán số cho nhóm NFR `TBD` ở `SRS` §5.2 (uptime, RPO/RTO, throughput, queue depth alert) | — | `SRS` §5.2 |

### ADR này quyết (phần Phase 1 **cố ý** để mở)

| Quyết định | Mã | Nguồn (file + mã requirement) |
|---|---|---|
| Hosting / PaaS / container platform / region đặt máy | `SRS-NFR-07` (`CHƯA QUYẾT` → `TBD`) | `SRS` §3.E · §4.2 · [findings/architect](../../010-Planning/pm-runs/2026-08-28-phase-2-architecture-design-comic-studio/findings/architect.md) §1.8, §2.1 |
