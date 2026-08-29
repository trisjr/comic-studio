---
id: SPEC-INT-OBJECT-STORAGE
type: spec
status: draft
project: comic-studio
created: 2026-08-29
---

# Spec Integration: Object Storage

Serves: [Story-Per-Tenant-Object-Storage-No-Cross-Dedup](../../022-User-Stories/Backlog/Story-Per-Tenant-Object-Storage-No-Cross-Dedup.md) · [UC-01](../../020-Requirements/Use-Cases/UC-01-Upload-And-Ingest-Chapter.md) · [UC-09](../../020-Requirements/Use-Cases/UC-09-Export-Chapter.md)
Decided in: [ADR-004](../Architecture/ADR-004-Object-Storage-Vendor-And-Signed-URL.md) · [ADR-002](../Architecture/ADR-002-Hosting-Platform-And-Region.md) · [ADR-010](../Architecture/ADR-010-Tenant-Isolation-With-RLS.md)

> [!CAUTION]
> ⭐⛔ **Hai câu quan trọng nhất của file này:**
> 1. ⛔ **KHÔNG BAO GIỜ ký signed URL cho một object key nhận TỪ CLIENT.** Key **phải** được đọc ra từ DB **dưới RLS**. Lộ khoá ký = **public bucket ⛔ không giới hạn thời gian**.
> 2. ⭐ Object storage này là **KHO BẰNG CHỨNG**, ⛔ **không phải thư mục cache**: artifact ảnh ⛔ **KHÔNG sinh lại được** (`seed` là **provenance metadata**, ⛔ **không phải replay key** — `D-44`).

## Mục lục

- [1. Mục đích](#1-mục-đích)
- [2. Cái gì đã CHỐT](#2-cái-gì-đã-chốt)
- [3. Cái gì còn MỞ](#3-cái-gì-còn-mở)
- [4. Interface / seam](#4-interface--seam)
- [5. Retry & error taxonomy](#5-retry--error-taxonomy)
- [6. Chi phí](#6-chi-phí)
- [Tài liệu tham khảo](#tài-liệu-tham-khảo)

---

## 1. Mục đích

File này đặc tả **bề mặt tiếp xúc giữa hệ thống và object storage**: ai được ký URL cho cái gì, file của người dùng đi vào bằng đường nào, và hệ thống hành xử ra sao khi lớp lưu trữ hỏng.

⚠️ **Phạm vi**: quyết định vendor, chiến lược phát hành signed URL (9 điều) và luồng ingest hai pha đã đóng ở [ADR-004](../Architecture/ADR-004-Object-Storage-Vendor-And-Signed-URL.md). ⛔ File này ⛔ **không quyết lại** — nó kéo các quyết định đó xuống mức thi hành được và bổ sung phần chưa ai viết: **error taxonomy** và **hành vi retry**.

**Ai tiêu thụ**: art của `generation` · `canonical_reference` (reference sheet nhân vật — đọc lại cho **gần như mọi panel**) · `export_artifact` (PDF, MVP2) · file chương do user upload đi qua **ingest**.
⇒ ⭐ **Traffic đọc lớn hơn traffic ghi nhiều bậc.** Đây là ràng buộc định hình cả phần chi phí lẫn phần cơ chế.

---

## 2. Cái gì đã CHỐT

### 2.1 Bốn điều của `D-13` — ⛔ ⛔ không mở lại

| # | Nội dung | Neo |
|:--:|---|---|
| 1 | Object storage **tách khỏi DB từ ngày đầu** — ⛔ **không bao giờ** lưu blob ảnh trong PostgreSQL | `SRS-FR-02` |
| 2 | Key là **`tenant/{tenant_id}/{sha256}`**; content-address **TRONG phạm vi một tenant** | `SRS-FR-02` |
| 3 | ⛔ **KHÔNG dedup chéo tenant** — dedup chéo mâu thuẫn trực tiếp với lập luận bản quyền | `SRS-FR-02` |
| 4 | **Signed URL có hạn**; ⛔ **không bao giờ public bucket** | `SRS-FR-02` |

### 2.2 Kho bằng chứng, KHÔNG phải thư mục cache

`D-20` nói *"spec là dữ liệu chính, **ảnh chỉ là output/cache**"*. `D-44` nói bit-exact reproducibility ⛔ **không đạt được** — và *"`seed` là **provenance metadata**, ⛔ **không phải replay key**"*.

⇒ **Đọc chung**: ảnh là *"cache"* theo nghĩa ⛔ không phải nguồn sự thật của **thiết kế** — nhưng nó ⛔ **KHÔNG sinh lại được**. **Mất một object là mất VĨNH VIỄN một mắt xích của chuỗi provenance** (`KC-1`, `D-47`, `D-49`) và của `change_log` (`KC-2`, `D-48`) — thứ đang phục vụ mục tiêu chứng minh *decisive contribution*.

> [!IMPORTANT]
> ⭐ **Mọi hàng trong [§5](#5-retry--error-taxonomy) phải được đọc dưới ánh sáng của mục này.** Một `404` trên key canonical ⛔ **không phải cache miss** — nó là **sự cố dữ liệu**. Và ⛔ **không có hàng nào** trong file này được phép mang hình dạng *"xoá cho sạch rồi làm lại"*.

### 2.3 CẤM ký signed URL cho object key nhận TỪ CLIENT

> ⭐⛔ **Đây là điều quan trọng nhất của toàn bộ bề mặt này.**

> **`OS-SIGN-1`** — ⛔ **CẤM ký signed URL cho bất kỳ object key nào đến từ client** (query string, body, header, hay bất kỳ trường nào của request).
> ⭐ Key **phải** được **đọc ra từ DB dưới RLS** trong chính transaction đang phục vụ request, rồi mới đem đi ký.

**Vì sao ràng buộc này nặng hơn nó trông:**

| # | Lập luận |
|:--:|---|
| 1 | ⭐ **Vendor storage ⛔ KHÔNG kiểm gì ở thời điểm `GET`.** Nó chỉ kiểm **chữ ký còn hợp lệ hay không**. ⇒ ⭐ **Toàn bộ authorization của lớp lưu trữ xảy ra ở bước ĐỌC DB dưới RLS** — ⛔ không ở đâu khác |
| 2 | ⇒ Một đường ký nhận key từ client biến **khoá ký của ta** thành một **oracle**: ai gọi được đường đó thì ký được cho **key bất kỳ**, và bucket ⛔ **không có lớp phòng thủ thứ hai nào** phía sau. Đó đúng nghĩa là **public bucket ⛔ không giới hạn thời gian** — vô hiệu hoá điều 4 của `D-13` |
| 3 | Key chứa `sha256` — một giá trị **chỉ server mới tin được**. Nhận key từ client là **tin vào chính khoá định danh nội dung** do client cung cấp |
| 4 | ⚠️ **Ràng buộc này ⛔ không được cưỡng chế bởi RLS.** RLS bảo vệ **hàng trong DB**; nó ⛔ không biết gì về một chuỗi key đi thẳng từ HTTP vào hàm ký. ⇒ Phải cưỡng chế bằng **hình dạng chữ ký hàm + lint + test** — xem [§4.3](#43-hình-dạng-hàm-ký--nơi-ràng-buộc-được-cưỡng-chế) |

**Ngoại lệ DUY NHẤT — và nó ⛔ không phải ngoại lệ thật:**

⚠️ Pha 1 của upload là **presigned `PUT`** vào `tenant/{tenant_id}/incoming/{upload_id}`. Điều này ⛔ **không vi phạm `OS-SIGN-1`** vì: `upload_id` **do server sinh**, ⛔ không do client đặt; prefix `incoming/` ⛔ **không phải vị trí dữ liệu hợp lệ** và ⛔ không đường đọc nào của sản phẩm trỏ vào đó ([ADR-004](../Architecture/ADR-004-Object-Storage-Vendor-And-Signed-URL.md) điều 7). ⇒ Client ⛔ **vẫn không bao giờ** quyết định được key.

### 2.4 Chín điều của [ADR-004](../Architecture/ADR-004-Object-Storage-Vendor-And-Signed-URL.md) — ⛔ file này ⛔ không đặc tả lại, chỉ neo

| Điều | Nội dung tóm tắt |
|:--:|---|
| 1 | Code chỉ nói chuyện với **một tập con S3 API** qua **MỘT adapter**. ⛔ Không tính năng riêng của vendor |
| 2 | ⛔ **Không bao giờ public bucket**; mọi lượt đọc qua signed URL phát **theo từng request** |
| 3 | ⭐ **Signed URL ⛔ KHÔNG BAO GIỜ được lưu bền**: ⛔ không vào DB · ⛔ không vào log · ⛔ không nhúng vào file export · ⛔ không gửi trong email/webhook. **DB chỉ lưu `key`** |
| 4 | **Đúng MỘT hằng số cấu hình cho TTL**, đọc từ biến môi trường. Mọi test phải chạy đúng với **TTL bất kỳ** |
| 5 | ⭐ **Client coi URL hết hạn là trạng thái BÌNH THƯỜNG, ⛔ không phải lỗi** — xin URL mới rồi thử lại **đúng một lần** |
| 6 | **Ba lớp phát hành URL** — xem [§4.2](#42-ba-lớp-phát-hành-url) |
| 7 | ⭐ **Upload HAI PHA** — xem [§4.4](#44-upload-hai-pha--thứ-tự-bắt-buộc) |
| 8 | **Bucket bật versioning**; credential của `api` và `worker` ⛔ **KHÔNG có `DeleteObject`** trên prefix canonical. Xoá chỉ qua **đường hard-delete tenant đặc quyền** (`D-14`), **tách biệt** khỏi soft-delete của takedown (`D-54`) |
| 9 | ⛔ **Không dedup chéo tenant.** Hai tenant cùng một file ⇒ **hai object, hai key, hai lần trả tiền**. Chi phí **có chủ ý** |

### 2.5 Vendor mặc định và thang đường lui — ⛔ chưa phải quyết định cuối

**Mặc định: Cloudflare R2**, vì hai lý do neo vào ràng buộc: tương thích **S3 API** (thoả điều 1 mà ⛔ không tốn adapter riêng), và ⭐ **trục chi phí của hệ thống này là băng thông ĐỌC** — ⭐ *"mô hình giá ⛔ không tính phí egress"* là **tiêu chí lựa chọn**, ⛔ **không phải một con số file này khẳng định**.
**Thang đường lui**: `1.` AWS S3 (`ap-southeast-1`) · `2.` Backblaze B2 · `3.` object storage của chính PaaS (chỉ khi chấp nhận khoá vendor).

### 2.6 Bốn ràng buộc xuyên suốt áp cho bề mặt này

| Mã | Nội dung | Nguồn duy nhất |
|:--:|---|---|
| `C-4` | ⛔ **Signed URL (đầy đủ hoặc phần chữ ký) ⛔ không được lọt vào `stdout`/`stderr`.** Đây là chỗ điều 3 được **cưỡng chế**: test CI grep log của bộ test tích hợp | [Spec-Security-Threat-Model §4.2](../Security/Spec-Security-Threat-Model.md) |
| `C-8` (a) | **Endpoint storage đến CHỈ từ cấu hình** (biến môi trường), ⛔ **không bao giờ** từ dữ liệu người dùng hay từ response của provider ⇒ ⛔ không có đường SSRF | [Spec-Security-Threat-Model §4.2](../Security/Spec-Security-Threat-Model.md) |
| `C-8` (b) | **Bytes trả về là dữ liệu KHÔNG tin cậy**: giới hạn kích thước, kiểm định dạng **trước khi** decode | [Spec-Security-Threat-Model §4.2](../Security/Spec-Security-Threat-Model.md) |
| `C-9` | Điều khoản dữ liệu + **vị trí lưu trữ** của vendor phải verify **bằng văn bản** khi mua | [Spec-Security-Threat-Model §4.2](../Security/Spec-Security-Threat-Model.md) |

### 2.7 ⛔ `SRS-NFR-15` — và vì sao chỗ này đặc biệt dễ phạm

⛔ **Bề mặt này ⛔ không được gửi object, hash, hay bất kỳ dẫn xuất nội dung nào tới một dịch vụ copyright / plagiarism / similarity detection nào.**

⚠️ **Đây là chỗ dễ phạm nhất trong bảy integration**, vì key đã là **content-address `sha256`** — nó *"nghe như đã sẵn sàng"* cho một phép so khớp. ⛔ **Không.** `sha256` ở đây phục vụ **đúng một** việc: định danh nội dung **trong phạm vi MỘT tenant** (`D-13` điều 2–3). ⛔ Nó ⛔ không được dùng để so khớp chéo tenant, và ⛔ không được gửi ra ngoài hệ thống.
Lý do đầy đủ (điều kiện *"không biết"* của miễn trừ Điều 198b): [Spec-Security-Legal-Compliance §5](../Security/Spec-Security-Legal-Compliance.md) — ⛔ file này ⛔ không lặp lại.

⚠️ **Phân biệt bắt buộc**: đọc **opt-out signal do chính chủ quyền gắn vào file** ở bước ingest là ✅ **BẮT BUỘC** (`KC-6`, `D-52`) — *"đọc nhãn ⛔ không tạo ra tri thức suy đoán"*. ⛔ Đừng gộp hai việc này làm một.

---

## 3. Cái gì còn MỞ

> ⛔ **Mục này ⛔ không đóng hàng nào.**

| # | `TBD` | Nội dung | Ai đóng | Khi nào |
|:--:|---|---|---|---|
| 1 | **`T-7`** | ⭐ **TTL của signed URL.** ⛔⛔ **CẤM gán số** ở bất kỳ chỗ nào trong file này, **kể cả dưới dạng ví dụ** — `SRS` §5.2 cấm tường minh: *"bịa một con số performance là lỗi nghiêm trọng hơn để trống nó"*. **Ràng buộc lên con số tương lai đã chốt sẵn**: ngắn hơn TTL phiên đăng nhập · TTL của URL export ⛔ không dài hơn TTL đọc inline · ⛔ không vô hạn, ⛔ không tính bằng ngày · **một giá trị duy nhất cho mọi lớp** cho tới khi có số đo chứng minh cần tách | **Dev đề xuất, Founder duyệt** | **MVP1**, khi editor có luồng thật để đo |
| 2 | `SRS-NFR-08` | **Vendor cuối cùng.** R2 là **mặc định**, ⛔ không phải đã mua. Phải verify: (a) tập con S3 **và presign** tương thích đầy đủ · (b) **versioning** khả dụng · (c) khả năng **ràng buộc vị trí lưu trữ** · (d) mô hình giá tại thời điểm mua | **Dev** | Trước lần **deploy MVP0** đầu tiên |
| 3 | **`T-22`** | **Nghĩa vụ lưu trữ dữ liệu trong lãnh thổ Việt Nam.** ⚠️ **Reopen trigger đã ghi trước**: nếu đáp án là *"phải"* thì **[ADR-002](../Architecture/ADR-002-Hosting-Platform-And-Region.md) và [ADR-004](../Architecture/ADR-004-Object-Storage-Vendor-And-Signed-URL.md) mở lại CÙNG LÚC** — vendor storage và platform phải chọn lại **như một cặp** | **Luật sư SHTT / tuân thủ** | Trước khi có **khách trả tiền** |
| 4 | **`T-23`** (`b-3`) | **Chính sách lưu giữ / xoá dữ liệu** (retention, purge). ⚠️ Đụng thẳng [§2.2](#22-kho-bằng-chứng-không-phải-thư-mục-cache): purge sai chỗ = **xoá bằng chứng** | **PM + Luật sư** | Cùng gói `SRS-NFR-17` |
| 5 | **`T-16`** (`b-1`) | **Mã hoá at-rest / in-transit + quản lý secret** (credential của bucket). ⚠️ Phần **đã** quyết chỉ gồm: signed URL **có hạn**, ⛔ **không bao giờ** public bucket | **Dev** | Sau khi **platform được mua** |
| 6 | **`T-10`** | **Giới hạn dung lượng / số file upload** + ngưỡng rate limit. Hàng **LAI**: cơ chế **CHỐT** (`SRS-NFR-20`), chỉ **ngưỡng số** mở | **PM + Architect** | Sau khi đo tải |
| 7 | — | ⚠️ **Có giữ artifact của candidate KHÔNG được chọn hay không.** ⛔ **KHÔNG phải quyết định của file này** — thuộc `ADR-014` và [`DB-Entity-Generation.md`](../Schema/DB-Entity-Generation.md). File này chỉ ghi hệ quả: **nếu giữ**, đó là trục chi phí lưu trữ chính, và ⛔ nó **vẫn** không được xoá bằng đường thông thường (điều 8) | **Architect** (ADR-014 / lô Schema) | Đã có chủ |
| 8 | — | **Share link công khai**: ⛔ **ngoài phạm vi horizon này** — ⛔ không yêu cầu nào đòi, và nó cần một mô hình thời hạn **khác hẳn**. Ghi ra để một lô sau ⛔ không lặng lẽ nhét nó vào lớp đọc inline | — | ⛔ Chưa mở |

---

## 4. Interface / seam

### 4.1 Adapter — đúng một tập con S3

`PutObject` · `GetObject` · `HeadObject` · `CopyObject` · `DeleteObject` *(⚠️ chỉ đường đặc quyền, xem [§4.5](#45-quyền-và-đường-xoá))* · **presign**.
⛔ **Không tính năng riêng của vendor.** ⇒ **Đổi vendor = đổi endpoint + credential + một job copy**, ⛔ không sửa code nghiệp vụ.

### 4.2 Ba lớp phát hành URL

| Lớp | Hình dạng | Ràng buộc |
|---|---|---|
| **Đọc inline trong editor** | Nhiều object, sống ngắn ⇒ URL phát **theo lô, kèm ngay trong response của resource** (một page trả URL cho mọi panel của nó) | ⛔ **Không có endpoint *"xin URL cho từng ảnh"* gọi N lần** |
| **Tải file export** | Một object ⇒ endpoint riêng, phát **một lần cho một lượt tải** | Đi kèm điều kiện gate của [`DB-Entity-Preview-And-Export.md`](../Schema/DB-Entity-Preview-And-Export.md) |
| **Share link công khai** | ⛔ **Ngoài phạm vi** | Hàng #8 của [§3](#3-cái-gì-còn-mở) |

### 4.3 Hình dạng hàm ký — nơi ràng buộc được cưỡng chế

> ⭐ **Hàm ký nhận BẢN GHI ĐÃ ĐỌC TỪ DB (hoặc khoá chính của bản ghi đó), ⛔ KHÔNG nhận một chuỗi `key` đến từ tầng HTTP.**

| Cưỡng chế bằng | Nội dung |
|---|---|
| **Hình dạng chữ ký hàm** | ⛔ Hàm ký ⛔ không có tham số `key: string` mà giá trị có thể đi thẳng từ request. Đây là cách rẻ nhất: ràng buộc trở thành **thứ trình biên dịch nhìn thấy**, ⛔ không phải một quy ước |
| **Lint rule** | ⛔ Chặn mọi lời gọi presign lấy tham số từ đối tượng request |
| **Test** | Request kèm một key thuộc tenant khác ⇒ ⛔ **không** nhận được URL; phản hồi tuân `C-5` (⛔ không phân biệt *"không tồn tại"* với *"không thuộc về bạn"*) |

⚠️ **Vì sao phải cưỡng chế bằng máy, ⛔ không bằng kỷ luật**: `C-2` — đội **1 người, ⛔ không có code review** ⇒ *"một biện pháp chỉ tồn tại dưới dạng quy ước thì trong repo này coi như **không tồn tại**"*.

### 4.4 Upload hai pha — thứ tự bắt buộc

| Pha | Ai chạy | Nội dung |
|:--:|---|---|
| **1** | Client (URL do server ký) | Presigned `PUT` vào `tenant/{tenant_id}/incoming/{upload_id}`. ⭐ `upload_id` **do server sinh** |
| **2a** | Server | Tính `sha256` từ **object đã nằm trong `incoming/`** |
| **2b** | Server | ⭐ Chạy **kiểm opt-out Điều 37b** và **ghi log kèm timestamp KỂ CẢ KHI *"không có signal"*** (`D-52`, `KC-6`; `INV-IC-2` của [`DB-Entity-Compliance-And-Takedown.md`](../Schema/DB-Entity-Compliance-And-Takedown.md)) |
| **2c** | Server | **Chặn** nếu có signal bảo lưu ⇒ ⛔ **không copy** sang canonical |
| **2d** | Server | `CopyObject` sang `tenant/{tenant_id}/{sha256}` |
| **2e** | Server | Xoá bản `incoming` — ⛔ **chỉ sau khi copy được XÁC NHẬN** (xem `OBJ-E7`) |

⛔ **Không object nào trong `incoming/` được coi là dữ liệu hợp lệ**; ⛔ không đường đọc nào của sản phẩm trỏ vào prefix đó.
⚠️ **Ingest là nơi DUY NHẤT file của user lần đầu vào hệ thống** (`D-52`) ⇒ ⛔ thêm một kênh nạp ⛔ không đi qua pha 2b là **phá `KC-6`** (`C-1`), ⛔ không phải một thiếu sót nhỏ.

### 4.5 Quyền và đường xoá

- **Bucket bật versioning.**
- Credential của `api` và `worker` ⛔ **KHÔNG có `DeleteObject` trên prefix canonical** ⇒ **một lỗi lập trình ⛔ không được phép xoá bằng chứng** — cùng tinh thần `D-10` (*"RLS biến lỗi lập trình thành no-op thay vì rò rỉ"*).
- Xoá chỉ đi qua **một đường riêng có đặc quyền**: đường **hard-delete tenant đã kiểm thử** (`D-14`), **tách biệt** khỏi soft-delete của takedown (`D-54`).
- ⚠️ Job dọn `incoming/` là **một đường riêng, phạm vi hẹp đúng prefix `incoming/`** — ⛔ **không** được giải bằng cách cấp `DeleteObject` rộng hơn cho `api`/`worker`.

### 4.6 ⛔ Năm anti-seam — ⛔ CẤM, kèm lý do

| ⛔ Cấm | Vì sao |
|---|---|
| ⛔ **Ký URL cho key từ client** | `OS-SIGN-1` — [§2.3](#23-cấm-ký-signed-url-cho-object-key-nhận-từ-client) |
| ⛔ **Lưu bền signed URL** (DB, log, PDF export, email, webhook) | Điều 3 + `C-4`. Một URL đã ký nằm trong log hoặc trong PDF là **public bucket thu nhỏ có thời hạn** |
| ⛔ **Dedup chéo tenant** *"để tiết kiệm dung lượng"* | ⚠️ Chỗ **sẽ có người muốn tối ưu lại khi nhìn hoá đơn**. Nó tạo **một object dùng chung giữa hai chủ thể pháp lý khác nhau**, và mở **kênh rò rỉ**: từ *"đã tồn tại"* suy ra tenant khác có cùng file |
| ⛔ **Proxy mọi ảnh qua API** thay cho signed URL | `D-13` đã chốt signed URL; và biến API (single-thread) thành CDN phá *"worker chết mà API vẫn sống"* từ phía ngược lại |
| ⛔ **Upload một pha thẳng vào key cuối** | Đặt object vào **vị trí hợp lệ TRƯỚC khi kiểm** opt-out ⇒ hệ thống có một khoảnh khắc chứa dữ liệu chưa kiểm ở đúng chỗ dữ liệu hợp lệ nằm |

---

## 5. Retry & error taxonomy

> ⭐ **Ba loại, ⛔ không phải hai**: **transient** (retry được) · **permanent** (⛔ không retry) · ⭐ **sự cố dữ liệu** (⛔ không retry, **phải báo động**) — loại thứ ba tồn tại vì [§2.2](#22-kho-bằng-chứng-không-phải-thư-mục-cache).
> ⛔ **Không hàng nào được phép có hình dạng *"xoá cho sạch rồi làm lại"*.**

| Mã | Tình huống | Loại | Hành vi bắt buộc | ⛔ Cấm |
|:--:|---|:--:|---|---|
| `OBJ-E1` | `PutObject`/`GetObject`/`HeadObject`/`CopyObject` lỗi mạng hoặc `5xx` | transient | **Retry có backoff + jitter, số lần CÓ TRẦN.** An toàn vì content-address: ghi lại **cùng key, cùng nội dung** là **idempotent** | ⛔ Không retry vô hạn |
| `OBJ-E2` | ⭐ Client `GET` gặp **URL hết hạn** | ⭐ **BÌNH THƯỜNG** | Xin URL mới qua API rồi thử lại **đúng một lần**; **chỉ lần hai** thất bại mới là lỗi hiển thị cho người dùng (điều 5) | ⛔ **Không hiện lỗi ngay lần đầu** — làm vậy thì TTL ngắn hiện ra dưới dạng *"ảnh thỉnh thoảng hỏng"*, loại lỗi tốn nhiều ngày nhất để chẩn đoán |
| `OBJ-E3` | `403` **dai dẳng** sau khi đã làm mới URL | permanent | Lỗi **cấu hình / credential / lệch đồng hồ**. Báo lỗi, fail-closed | ⛔⛔ **Không "sửa" bằng cách nới quyền bucket** — đó là đường ngắn nhất tới public bucket |
| `OBJ-E4` | ⭐ `404` trên **key canonical** | ⭐ **sự cố dữ liệu** | **Báo động.** Đây ⛔ **không phải cache miss** — một mắt xích bằng chứng đã mất. Versioning (điều 8) là đường khôi phục **đầu tiên** phải thử | ⛔⛔ **Không tự sinh lại ảnh** — nó ⛔ **không sinh lại được** (`D-44`). Sinh một ảnh **mới** rồi đặt vào chỗ ảnh cũ là **giả mạo provenance** |
| `OBJ-E5` | `sha256` ⛔ không tính được / file hỏng / sai định dạng | permanent | **Từ chối** ở pha 2a; object `incoming` **giữ nguyên** cho job dọn dẹp. Kiểm định dạng **trước khi** decode (`C-8` b) | ⛔ Không đoán định dạng |
| `OBJ-E6` | Kiểm opt-out **có signal bảo lưu** | permanent *(đúng theo thiết kế)* | ⭐ **Chặn**: ⛔ không `CopyObject` sang canonical. **Dòng `ingest_check` vẫn phải được ghi** (`INV-IC-2`, `INV-IC-3`: `result <> 'no_signal'` ⇒ `blocked = TRUE`). Object `incoming` rơi vào đường dọn dẹp | ⛔ Không coi *"unreadable"*/*"conflicting"* là *"không có signal"* rồi cho qua |
| `OBJ-E7` | `CopyObject` thất bại **sau khi** check đã pass | transient | Retry (`OBJ-E1`). ⭐ **Xác nhận copy bằng `HeadObject` TRƯỚC KHI xoá bản `incoming`** | ⛔⛔ **Không xoá `incoming` trước khi copy được xác nhận** — làm vậy là **mất file của người dùng** giữa hai pha |
| `OBJ-E8` | Object **mồ côi** trong `incoming/` (client bỏ ngang) | bình thường | **Scheduled job dọn dẹp**, phạm vi **đúng prefix `incoming/`** ([ADR-002](../Architecture/ADR-002-Hosting-Platform-And-Region.md): cron chỉ gọi subcommand). Đây là **hạng mục công việc thật**, ⛔ không phải chi tiết | ⛔ Không cấp `DeleteObject` rộng hơn để làm việc này |
| `OBJ-E9` | **Presign thất bại** khi dựng response theo lô | permanent | ⭐ Presign là **phép tính cục bộ** ⇒ nó chỉ hỏng khi **cấu hình/credential hỏng**, tức hỏng cho **MỌI** object ⇒ **lỗi cấp response**, ⛔ không phải lỗi cấp từng ảnh. ⚠️ **Điều kiện kiểm lại**: nếu vendor được chọn đòi **gọi mạng** để presign, giả định này phải được kiểm lại ở bước verify vendor (hàng #2 của [§3](#3-cái-gì-còn-mở)) | ⛔ **Không trả response thiếu URL im lặng** — client sẽ hiển thị *"ảnh hỏng"* mà ⛔ không ai biết vì sao |
| `OBJ-E10` | **Vendor storage sập** | transient (ngoài tầm) | Đường **đọc** hỏng toàn cục — hiển thị lỗi trung thực. Đường **ghi** phải **fail-closed** | ⛔⛔ **Không ghi dòng DB *"đã có artifact"* khi object chưa nằm trong storage.** Ranh giới transaction thuộc [ADR-017](../Architecture/ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md) — ⛔ file này ⛔ không nới nó |

⚠️ **Hai quy tắc bao trùm bảng trên:**
1. ⛔ **Không log signed URL** ở bất kỳ hàng nào, kể cả trong thông báo lỗi (`C-4`).
2. **Frontend phải có đường refetch từ ngày đầu** (`OBJ-E2`) — ⛔ **không phải thêm sau khi gặp lỗi lần đầu ở production**.

---

## 6. Chi phí

> ⛔ **Không dán giá vào file này** ([ADR-004](../Architecture/ADR-004-Object-Storage-Vendor-And-Signed-URL.md)). Mọi con số tra **tại thời điểm mua**.

| Trục | Nội dung |
|---|---|
| ⭐ **Băng thông ĐỌC — trục chi phí chính** | `D-64` chỉ đích danh **reference-sheet amortization** là một trong **hai** chỗ ra tiền thật, và reference sheet được **đọc lại cho gần như mọi panel**. ⇒ Tiêu chí chọn vendor là **mô hình giá cho egress**, ⛔ không phải giá dung lượng |
| **Lưu trữ trùng lặp — có chủ ý** | ⛔ Không dedup chéo tenant (điều 9) ⇒ hoá đơn storage **cao hơn mức lý thuyết**. ⚠️ Phải nói thẳng với Founder, và ⛔ **không được "tối ưu" lại** |
| ⚠️ **Nhân 3 theo số panel — nếu giữ candidate** | `D-58`: một lần best-of-N (`N=3`) tạo **đúng 3** `usage_event` ⇒ mỗi panel có **ba** `generation`. **Nếu** mỗi `generation` có artifact riêng thì dung lượng **nhân 3**. ⛔ Quyết định giữ hay không **⛔ không thuộc file này** — hàng #7 của [§3](#3-cái-gì-còn-mở) |
| **CPU ký trên đường nóng** | URL ⛔ không lưu ⇒ **ký lại mỗi lần**. Mở một page 4 panel là ký 4 URL mỗi lần tải. Phát **theo lô** (điều 6) giữ cho nó là **một** lần dựng response, ⛔ không phải N lần gọi API — nhưng response lớn hơn và CPU ký là **chi phí thật** |
| **Versioning + ⛔ cấm `DeleteObject`** | ⇒ **rác tích luỹ có chủ ý**. Đây là giá của việc *"mất bằng chứng do lỗi lập trình"* trở thành **bất khả**, ⛔ không phải *"khó xảy ra"* |
| **Chi phí đổi vendor** | Đã được giới hạn trước: adapter một tập con S3 + **một job copy** |

---

## Tài liệu tham khảo

**Tầng 020 — Requirements**
- [SRS-Comic-Studio](../../020-Requirements/SRS-Comic-Studio.md) — `SRS-FR-02` (`D-13`) · `SRS-FR-07` (`D-20`) · `SRS-FR-30` (`D-58`) · `SRS-FR-34`–`SRS-FR-37` (`D-47`, `D-48`, `D-49`, `D-52`) · `SRS-NFR-01` · `SRS-NFR-05` (`D-14`) · `SRS-NFR-08` · `SRS-NFR-12` (`D-64`) · `SRS-NFR-15` · `SRS-NFR-20` · §5.2 (lệnh cấm gán số)
- [UC-01](../../020-Requirements/Use-Cases/UC-01-Upload-And-Ingest-Chapter.md) · [UC-09](../../020-Requirements/Use-Cases/UC-09-Export-Chapter.md)

**Tầng 022 — User Stories**
- [Story-Per-Tenant-Object-Storage-No-Cross-Dedup](../../022-User-Stories/Backlog/Story-Per-Tenant-Object-Storage-No-Cross-Dedup.md)

**Tầng 030 — Architecture** *(chỉ đọc, ⛔ không sửa)*
- [ADR-004 — Vendor object storage & signed URL](../Architecture/ADR-004-Object-Storage-Vendor-And-Signed-URL.md) — ⭐ nguồn duy nhất của 9 điều
- [ADR-002 — Hosting platform & region](../Architecture/ADR-002-Hosting-Platform-And-Region.md) — reopen trigger dùng chung (`T-22`)
- [ADR-010 — Cô lập tenant bằng RLS](../Architecture/ADR-010-Tenant-Isolation-With-RLS.md) — `D7` hai đường xoá
- [ADR-017 — Chuỗi provenance & một ranh giới transaction](../Architecture/ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md)
- [SDD-Comic-Studio](../Architecture/SDD-Comic-Studio.md) — §5.4 (`F1`), §7.5

**Tầng 030 — Schema**
- [`DB-Entity-Compliance-And-Takedown.md`](../Schema/DB-Entity-Compliance-And-Takedown.md) — `story.ingest_check`, `INV-IC-1`…`INV-IC-6`
- [`DB-Entity-Generation.md`](../Schema/DB-Entity-Generation.md) · [`DB-Entity-Preview-And-Export.md`](../Schema/DB-Entity-Preview-And-Export.md)

**Tầng 030 — Security** *(⛔ không lặp lại nội dung)*
- [Spec-Security-Threat-Model](../Security/Spec-Security-Threat-Model.md) — §4.2 `C-1`, `C-2`, `C-4`, `C-5`, `C-8`, `C-9`
- [Spec-Security-Legal-Compliance](../Security/Spec-Security-Legal-Compliance.md) — §5 (`SRS-NFR-15`), §8 (`T-7`, `T-16`, `T-22`, `T-23`)
- [Spec-Security-Tenant-Isolation](../Security/Spec-Security-Tenant-Isolation.md)

**Tầng 010 — Planning**
- [MVP-Scope](../../010-Planning/MVP-Scope.md) — `E3`
- [PM run-state](../../010-Planning/pm-runs/2026-08-28-phase-2-architecture-design-comic-studio/escalations.md)

**Spec anh em**
- [Spec-Integration-Image-Provider](./Spec-Integration-Image-Provider.md) — nơi artifact được **sinh ra**; file này lo nơi artifact được **giữ**
- *(⛔ chưa tồn tại tại thời điểm viết — nêu bằng plain text, ⛔ cố ý không tạo link)*: `Endpoint-Generation.md` và `Endpoint-*` của lô API (nơi TTL `T-7` được trỏ về).
