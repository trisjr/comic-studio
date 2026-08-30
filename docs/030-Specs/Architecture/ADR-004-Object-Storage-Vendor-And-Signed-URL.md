---
id: ADR-004
type: adr
status: accepted
project: comic-studio
created: 2026-08-29
updated: 2026-08-30
---

# ADR-004: Vendor object storage, chiến lược phát hành signed URL và luồng ingest

Related to: [SDD-Comic-Studio](./SDD-Comic-Studio.md)

## Context

> [!CAUTION]
> ⛔ **Bốn điều sau ĐÃ CHỐT ở `D-13` và ADR này KHÔNG mở lại** ([SRS-Comic-Studio](../../020-Requirements/SRS-Comic-Studio.md) §2.3, `SRS-FR-02`, §4.3):
> 1. Object storage **tách khỏi DB từ ngày đầu** — ⛔ không bao giờ lưu blob ảnh trong PostgreSQL.
> 2. Key là **`tenant/{tenant_id}/{sha256}`**; content-address **TRONG phạm vi một tenant**.
> 3. ⛔ **KHÔNG dedup chéo tenant** — dedup chéo mâu thuẫn trực tiếp với lập luận bản quyền.
> 4. **Signed URL có hạn**; ⛔ **không bao giờ public bucket**.

Cái còn mở: **vendor** (`SRS-NFR-08` — *"Tên vendor không xuất hiện ở bất kỳ tài liệu nào"*), **thời hạn signed URL** (`SRS` §5.2), và **chiến lược phát hành URL** (chưa tài liệu nào chạm tới).

### Ai tiêu thụ storage này

| Loại object | Đặc tính truy cập | Neo |
|---|---|---|
| Art của `generation` | Đọc lặp lại nhiều lần trong editor; ghi một lần | `D-44` |
| `canonical_reference` (reference sheet nhân vật) | ⭐ **Đọc lại cho gần như mọi panel** — `D-64` gọi *reference-sheet amortization* là **một trong hai chỗ ra tiền thật** | `D-64` · `SRS-NFR-12`, §5.2 |
| `export_artifact` (PDF ở MVP2) | Ghi một lần, tải một lần, file lớn | `D-68` · `SRS-FR-42` |
| File chương do user upload | Đi qua **ingest** — nơi **duy nhất** file của user lần đầu vào hệ thống | `D-52` · `SRS-FR-37` |

⇒ **Traffic đọc lớn hơn traffic ghi nhiều bậc**, và phần đọc lặp nhiều nhất chính là phần `D-64` đã chỉ tên. Đây là ràng buộc định hình việc chọn vendor.

### ⚠️ Một chỗ dễ đọc sai, phải làm rõ trước khi quyết

`D-20` nói *"spec là dữ liệu chính, **ảnh chỉ là output/cache**"* (`SRS` §2.1, `SRS-FR-07`). Nhưng `D-44` nói bit-exact reproducibility **không đạt được** — API không cho set seed, có silent model drift, và *"`seed` là provenance metadata, ⛔ không phải replay key"* (`SRS` §3.A).

**Đọc chung, hai câu đó có nghĩa**: ảnh là *"cache"* theo nghĩa **không phải nguồn sự thật của thiết kế** — nhưng nó ⛔ **KHÔNG** sinh lại được. Mất một object là mất **vĩnh viễn** một artifact, mà artifact đó là một mắt xích của chuỗi provenance (`D-47`, `D-49`) và của `change_log` (`D-48`) — thứ đang phục vụ mục tiêu chứng minh *decisive contribution*.

⇒ **Object storage này phải được đối xử như kho bằng chứng, không như thư mục cache.** Đây là làm rõ cách đọc hai quyết định đã CHỐT, ⛔ không phải đổi quyết định nào.

## Decision

### Tầng CHỐT — ⛔ không đổi mà không viết ADR mới

1. **Code chỉ nói chuyện với tập con S3 API qua MỘT adapter**: `PutObject`, `GetObject`, `HeadObject`, `CopyObject`, `DeleteObject`, presign. ⛔ Không tính năng riêng của vendor. (Hiện thực trực tiếp của [ADR-002](./ADR-002-Hosting-Platform-And-Region.md) điều 6.) ⇒ **Đổi vendor = đổi endpoint + credential + một job copy**, ⛔ không sửa code nghiệp vụ.
2. **⛔ Không bao giờ public bucket.** Mọi lượt đọc đi qua signed URL **phát theo từng request** (`D-13`).
3. ⭐ **Signed URL ⛔ KHÔNG BAO GIỜ được lưu bền.** ⛔ Không ghi vào DB · ⛔ không ghi ra log (phải có quy tắc che trong logger) · ⛔ không nhúng vào file export · ⛔ không gửi trong email/webhook. **DB chỉ lưu `key`**; URL được sinh tại thời điểm dựng response.
   Lý do: một URL đã ký nằm trong log hoặc trong file PDF là một **public bucket thu nhỏ** có thời hạn — nó vô hiệu hoá chính điều 2.
4. **Đúng MỘT hằng số cấu hình cho TTL**, đọc từ biến môi trường. ⛔ Không rải giá trị TTL ở nhiều chỗ trong code. Mọi test phải chạy đúng với **TTL bất kỳ**, kể cả rất ngắn.
5. ⭐ **Client coi URL hết hạn là trạng thái BÌNH THƯỜNG, ⛔ không phải lỗi.** Gặp phản hồi hết hạn ⇒ xin URL mới qua API rồi thử lại **đúng một lần**; chỉ khi lần hai thất bại mới là lỗi hiển thị cho người dùng.
   Đây là điều biến con số TTL từ **quyết định kiến trúc** thành **tham số vận hành** — và là lý do ADR này có thể đóng phần cơ chế mà ⛔ không cần chờ con số.
6. **Ba lớp phát hành URL — khác nhau ở ĐƯỜNG, không ở vendor**:
   - **Đọc inline trong editor**: nhiều object, sống ngắn ⇒ URL được phát **theo lô, kèm ngay trong response của resource** (một page trả về URL cho mọi panel của nó). ⛔ Không có endpoint *"xin URL cho từng ảnh"* gọi N lần.
   - **Tải file export**: một object, người bấm rồi tải ⇒ endpoint riêng, phát **một lần cho một lượt tải**.
   - **Share link công khai**: ⛔ **ngoài phạm vi horizon này** — không yêu cầu nào đòi, và nó sẽ cần một mô hình thời hạn khác hẳn. Ghi ra để một run sau ⛔ không lặng lẽ nhét nó vào lớp thứ nhất.
7. ⭐ **Upload là HAI PHA** — bắt buộc bởi chính key schema đã CHỐT cộng `D-52`:
   - **Pha 1**: presigned `PUT` vào `tenant/{tenant_id}/incoming/{upload_id}`. Client ⛔ **không được** tự quyết key cuối, vì key chứa `sha256` mà **chỉ server mới tin được**.
   - **Pha 2 (server)**: tính `sha256` → chạy **kiểm opt-out Điều 37b** và **ghi log kèm timestamp kể cả khi *"không có signal"*** (`D-52`) → chặn nếu có signal bảo lưu → `CopyObject` sang `tenant/{tenant_id}/{sha256}` → xoá bản `incoming`.
   - ⛔ **Không object nào trong `incoming/` được coi là dữ liệu hợp lệ**, ⛔ không đường đọc nào của sản phẩm trỏ vào prefix đó.
8. **Bucket bật versioning. Credential của `api` và `worker` ⛔ KHÔNG có quyền `DeleteObject` trên prefix canonical.** Xoá chỉ đi qua **một đường riêng có đặc quyền** — chính là đường **hard-delete tenant đã kiểm thử** của `D-14`, **tách biệt** khỏi soft-delete của takedown (`D-54`).
   Lý do: xem mục *"Một chỗ dễ đọc sai"* ở trên. Một lỗi lập trình ⛔ không được phép xoá bằng chứng.
9. **⛔ Không dedup chéo tenant** (`D-13`). Hai tenant upload đúng cùng một file ⇒ **hai object, hai key, hai lần trả tiền lưu trữ**. Đây là chi phí **có chủ ý**, ⛔ không phải chỗ để tối ưu.

### Tầng MẶC ĐỊNH — vendor

**Cloudflare R2**. Hai lý do neo vào ràng buộc, không neo vào sở thích:
1. **Tương thích S3 API** ⇒ thoả điều 1 mà ⛔ không tốn adapter riêng.
2. **Trục chi phí của hệ thống này là băng thông ĐỌC, không phải dung lượng lưu.** `D-64` đã chỉ đích danh *reference-sheet amortization* là một trong hai chỗ ra tiền thật, và reference sheet được đọc lại cho gần như mọi panel. R2 được chọn vì **mô hình giá của nó không tính phí egress** — đây là **tiêu chí lựa chọn**, ⛔ không phải một con số em khẳng định.

**Thang đường lui**: `1.` **AWS S3** (`ap-southeast-1`, cùng region với bậc 3 của [ADR-002](./ADR-002-Hosting-Platform-And-Region.md)) · `2.` **Backblaze B2** · `3.` object storage của chính PaaS (chỉ khi chấp nhận khoá vendor — đụng ADR-002 điều 6).

> [!WARNING]
> ⚠️ **Phải verify trước khi mua, ⛔ ADR này không xác nhận thay**: (a) tập con S3 ở điều 1 **và presign** tương thích đầy đủ; (b) **versioning** khả dụng (điều 8); (c) khả năng **ràng buộc vị trí lưu trữ** — vì reopen trigger về lưu trữ dữ liệu trong nước ở [ADR-002](./ADR-002-Hosting-Platform-And-Region.md) áp cho cả ADR này; (d) mô hình giá tại thời điểm mua. **Owner: dev · Mốc: trước lần deploy MVP0 đầu tiên.** ⛔ **Không dán giá vào ADR.**

### `TBD` — con số TTL, ⛔ KHÔNG tự gán

**Thời hạn signed URL ở lại `TBD`.** Đây là **kết quả đúng, không phải chỗ trống bị bỏ quên**: `SRS` §5.2 liệt kê *"Thời hạn signed URL"* trong bảng NFR `TBD` ở `SRS` §5.2 mà `SRS` §5.2 cấm tường minh — *"⛔ Không tự gán số cho bất kỳ hàng nào dưới đây. Bịa một con số performance là lỗi nghiêm trọng hơn để trống nó."*

Nhưng ADR này **đóng được toàn bộ phần không cần số**:

| Hạng mục | Nội dung |
|---|---|
| **Ai đóng** | **Dev** đề xuất, **Founder** duyệt |
| **Khi nào** | **MVP1**, khi editor có luồng thật để đo — ⛔ không sớm hơn, vì trước đó mọi con số đều là phỏng đoán |
| **Đầu vào còn thiếu** | (a) thời gian tải một page 300 DPI trên đường truyền thực; (b) một phiên editor mở bao lâu giữa hai lần lấy dữ liệu; (c) có hay không tính năng share link (hiện tại: **không**, điều 6) |
| **Ràng buộc lên con số tương lai** *(quyết được ngay, ⛔ không cần số)* | TTL phải **ngắn hơn** thời hạn của token phiên đăng nhập · TTL của URL export ⛔ **không được** dài hơn TTL đọc inline chỉ vì tiện · ⛔ **không có** TTL vô hạn hay tính bằng ngày · một giá trị duy nhất cho mọi lớp cho tới khi có số đo chứng minh cần tách |
| **Vì sao không chặn** | Điều 4 + điều 5 làm cho hệ thống chạy đúng với **TTL bất kỳ**. Con số là tham số vận hành, ⛔ không phải điều kiện để bắt đầu code |

## Alternatives considered

### A. Public bucket + URL "khó đoán" · B. Lưu blob trong PostgreSQL

⛔ **Không phải phương án và ⛔ không được đọc thành phương án.** `D-13` đã **CHỐT**: ⛔ *"không bao giờ public bucket"*, ⛔ *"không bao giờ lưu blob ảnh trong Postgres"* (`SRS-FR-02`, §2.3). Mục này tồn tại **chỉ để** một run sau không tưởng rằng chúng bị bỏ sót khi cân nhắc.

*(Ghi thêm cho phương án B, vì nó hay quay lại dưới dạng "cho tiện": blob trong Postgres làm phình đúng cái database đang phải giữ PITR cho **bằng chứng pháp lý** — xem [ADR-002](./ADR-002-Hosting-Platform-And-Region.md). Nó biến mọi lần backup thành backup của hàng chục GB ảnh.)*

### C. Proxy mọi ảnh qua API, ⛔ không dùng signed URL

- **Ưu điểm thật — và phải thừa nhận là ưu điểm thật**: đây là phương án **chặt nhất về bảo mật**. Mọi lượt đọc đi qua code của ta ⇒ kiểm tra được `membership` ở từng byte, ghi được log truy cập đầy đủ, ⛔ không có URL nào tồn tại ngoài phiên.
- **Loại vì hai lý do**:
  1. `D-13` đã **CHỐT** *"signed URL có hạn"* — chọn proxy là mở lại một quyết định đã đóng.
  2. Kể cả nếu chưa chốt: mọi byte ảnh sẽ đi qua process `api`, mà [ADR-001](./ADR-001-Backend-And-Frontend-Tech-Stack.md) hệ quả #1 đã ghi Node là single-thread. Biến API thành CDN là cách chắc chắn nhất phá vỡ *"worker chết mà API vẫn sống"* — từ phía ngược lại.
- **Cái ta giữ lại từ phương án này**: điều 3 (URL không bao giờ lưu bền) chính là cách lấy phần lớn lợi ích bảo mật của proxy mà ⛔ không trả chi phí băng thông của nó.

### D. Content-address toàn cục + dedup chéo tenant

- **Ưu điểm thật**: tiết kiệm dung lượng thật, và về mặt kỹ thuật thuần tuý thì `sha256` là khoá dedup hoàn hảo.
- **Loại vì `D-13` đã CHỐT — và lý do đáng ghi lại nguyên vẹn**: dedup chéo tenant tạo **một object dùng chung giữa hai chủ thể pháp lý khác nhau**, mâu thuẫn trực tiếp với lập luận bản quyền của toàn bộ nhánh `KC-1…KC-7`. Nó còn mở một **kênh rò rỉ thông tin**: từ việc một upload trả về *"đã tồn tại"*, một tenant suy ra được tenant khác có cùng file.
- ⚠️ Ghi ra tường minh vì đây là chỗ **sẽ có người muốn "tối ưu" lại** khi nhìn hoá đơn lưu trữ.

### E. Upload một pha — presigned `PUT` thẳng vào key cuối

- **Ưu điểm thật**: ít code nhất, ít round trip nhất, và là mô hình phổ biến nhất ngoài đời.
- **Loại vì hai lý do độc lập**:
  1. Key cuối chứa `sha256`. Để client tự tính và tự đặt key là **tin vào một giá trị do client cung cấp** cho chính khoá định danh nội dung — mở đường ghi đè và ghi nhầm.
  2. `D-52` bắt buộc kiểm opt-out Điều 37b **ngay trong bước ingest**, vì *"ingest là nơi DUY NHẤT file của user lần đầu vào hệ thống"*. Upload một pha đặt object vào vị trí hợp lệ **trước khi** kiểm — tức là hệ thống có một khoảnh khắc chứa dữ liệu chưa được kiểm ở đúng chỗ dữ liệu hợp lệ nằm.
- Điều 7 (hai pha + prefix `incoming/`) là cách rẻ nhất giữ cả hai tính chất.

### F. AWS S3 (`ap-southeast-1`) làm mặc định

- **Ưu điểm thật**: là **định nghĩa** của S3 API nên rủi ro tương thích bằng không; trưởng thành nhất; trùng region với bậc 3 của thang đường lui ở [ADR-002](./ADR-002-Hosting-Platform-And-Region.md) ⇒ nếu sau này chuyển sang ECS thì mọi thứ về cùng một nhà.
- **Không loại — là bậc 1 của thang đường lui.** Xuống dưới R2 vì đúng một lý do: mô hình tính phí băng thông đọc, mà băng thông đọc là trục chi phí của hệ thống này (`D-64`).

## Consequences

### Tích cực

- Chi phí đổi vendor storage được giới hạn trước: adapter một tập con S3 + một job copy. Cùng dạng bảo hiểm mà [ADR-002](./ADR-002-Hosting-Platform-And-Region.md) điều 6 và [ADR-003](./ADR-003-Auth-And-Billing-Vendor-Selection.md) điều 2 đã mua ở hai tầng khác.
- **Con số TTL không chặn việc bắt đầu code** — nhờ điều 4 và điều 5. Đây là cách ADR này tuân `SRS` §5.2 mà vẫn giao được một quyết định dùng được.
- Điều 7 khiến `D-52` (kiểm Điều 37b tại ingest) có **đúng một chỗ** để cưỡng chế, thay vì rải rác ở mọi đường upload.
- Điều 8 khiến việc mất bằng chứng do lỗi lập trình trở thành **bất khả**, chứ không phải *"khó xảy ra"* — cùng tinh thần với `D-10` (*"RLS biến lỗi lập trình thành no-op thay vì rò rỉ"*).

### Tiêu cực — cái gì trở nên KHÓ HƠN

1. **Trả tiền lưu trữ trùng lặp** (điều 9). Có chủ ý, và ⛔ không được "tối ưu" lại — nhưng phải nói thẳng với Founder rằng hoá đơn storage sẽ cao hơn mức lý thuyết.
2. **Upload thêm một round trip và thêm một loại rác.** Object mồ côi trong `incoming/` (client bỏ ngang giữa hai pha) cần **một scheduled job dọn dẹp** — nối thẳng vào [ADR-002](./ADR-002-Hosting-Platform-And-Region.md) điều 3 (cron chỉ gọi subcommand). Đây là một hạng mục công việc thật, ⛔ không phải chi tiết.
3. **URL không lưu ⇒ phải ký lại mỗi lần.** Mở một page 4 panel là ký 4 URL mỗi lần tải. Điều 6 (phát theo lô) giữ cho nó là **một** lần dựng response, ⛔ không phải N lần gọi API — nhưng response sẽ lớn hơn và CPU ký là chi phí thật trên đường nóng.
4. **Frontend phải có đường refetch từ ngày đầu** (điều 5), ⛔ không phải thêm sau khi gặp lỗi lần đầu ở production. Nếu bỏ qua, TTL ngắn sẽ hiện ra dưới dạng *"ảnh thỉnh thoảng hỏng"* — loại lỗi tốn nhiều ngày nhất để chẩn đoán.
5. **⛔ Cấm `DeleteObject` ⇒ rác tích luỹ có chủ ý.** `D-58` ghi rõ một lần best-of-N (N=3) tạo **đúng 3** `usage_event` row ⇒ mỗi panel có **ba** `generation`. Nếu mỗi `generation` có artifact riêng thì dung lượng lưu trữ **nhân 3 theo số panel**.
   ⚠️ **Việc có giữ artifact của candidate không được chọn hay không là quyết định của ADR-014 và của `DB-Entity-Generation`, ⛔ KHÔNG phải của ADR này.** ADR này chỉ ghi trước rằng: **nếu giữ**, đó là trục chi phí lưu trữ chính, và ⛔ nó vẫn không được xoá bằng đường thông thường (điều 8).
6. **`SRS` §5.2 vẫn để lại một lỗ tường minh trong spec** — `Endpoint-Generation.md` (lô sau) sẽ ghi TTL là `TBD` và trỏ về mục này. Đó là kết quả đúng theo `SRS` §5.2, ⛔ không phải khiếm khuyết cần lấp.
7. **Reopen trigger dùng chung với [ADR-002](./ADR-002-Hosting-Platform-And-Region.md)**: nếu luật sư trả lời rằng dữ liệu phải nằm trong lãnh thổ Việt Nam, **cả hai ADR mở lại cùng lúc** — vendor storage và platform phải được chọn lại như một cặp, ⛔ không tách rời.

## Đã quyết ở đâu

### Kế thừa từ Phase 1 — ⛔ ADR này KHÔNG mở lại

| Quyết định | Mã `D-xx` | Nguồn (file + mã requirement) |
|---|---|---|
| ⭐ Object storage **tách khỏi DB từ ngày đầu**; key **`tenant/{tenant_id}/{sha256}`**; content-address **trong phạm vi tenant**; ⛔ **KHÔNG dedup chéo tenant**; **signed URL có hạn**; ⛔ **không bao giờ public bucket** | `D-13` | [SRS-Comic-Studio](../../020-Requirements/SRS-Comic-Studio.md) §2.3, `SRS-FR-02`, §4.3 · `MVP-Scope` §3 `E3` |
| `tenant_id` là trục phân vùng của mọi thứ; RLS là lớp phòng thủ thứ hai | `D-09` | `SRS-NFR-01` |
| Kỷ luật `ON DELETE CASCADE` + **một đường hard-delete tenant đã kiểm thử**, tách biệt khỏi soft-delete của takedown | `D-14` | `SRS-NFR-05` |
| **Spec là dữ liệu chính, ảnh là output/cache** | `D-20` | `SRS` §2.1, `SRS-FR-07` |
| ⭐ Mục tiêu bảng `Generation` là **auditability + lineage**, ⛔ **không phải reproducibility**; `seed` ⛔ không phải replay key | `D-44` | `SRS` §3.A · `MVP-Scope` §4.4 (*"mục tiêu đúng của `Generation` là AUDITABILITY + LINEAGE"*) |
| `parent_generation_id` + `relation_kind` từ **migration số 1**, ⛔ không backfill được | `D-47` | `SRS-FR-34` |
| `change_log` append-only ghi **mọi** hành động người dùng, kể cả **export** | `D-48` | `SRS` §3.D, `SRS-FR-35`, §4.1 |
| `field_provenance` mức FIELD + `generation.origin` | `D-49` | `SRS-FR-36` |
| ⭐ **Kiểm opt-out Điều 37b NGAY TRONG BƯỚC INGEST**, log kết quả kèm timestamp **kể cả khi không có signal**, chặn nếu có signal bảo lưu | `D-52` | `SRS-FR-37` · `MVP-Scope` §6 `KC-6` · `UC-01` b5–b6 |
| Takedown = **soft-delete + disable-access ở cấp project**, ⛔ **không hard delete** | `D-54` | `SRS-FR-38`, §4.4, §5.1 · `UC-11` b2, b3, b6 |
| Một lần best-of-N (N=3) tạo **đúng 3** `usage_event` row | `D-58` | `SRS-FR-30` |
| ⛔ **Đừng dựa vào cache để cứu margin**; hai chỗ ra tiền thật là **reference-sheet amortization** và **idempotency** | `D-64` | `SRS-NFR-12`, §5.2 |
| Export PDF ở MVP2 | `D-68` | `SRS-FR-42` · `MVP-Scope` §3 `H4` |
| ⛔ Cấm gán số cho bảng NFR `TBD` ở `SRS` §5.2 — trong đó có **thời hạn signed URL** | — | `SRS` §5.2 |

### ADR này quyết (phần Phase 1 **cố ý** để mở)

| Quyết định | Mã | Nguồn (file + mã requirement) |
|---|---|---|
| **Vendor object storage** (MẶC ĐỊNH: Cloudflare R2) + thang đường lui | `SRS-NFR-08` (`CHƯA QUYẾT` → `TBD`) | `SRS` §3.E · [findings/architect](../../010-Planning/pm-runs/2026-08-28-phase-2-architecture-design-comic-studio/findings/architect.md) §1.8, §2.1 |
| **Chiến lược phát hành signed URL** (9 điều ở tầng CHỐT) — chưa tài liệu Phase 1 nào chạm tới | — | Dẫn xuất từ `D-13`, `D-52`, `D-14`, `D-44` |
| **Thời hạn signed URL** — ở lại `TBD` **có chủ đích**, kèm owner, mốc và ràng buộc lên con số tương lai | `SRS-FR-02` | `SRS` §5.2 (lệnh cấm gán số) |
