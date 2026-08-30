---
id: UC-10
type: use-case
status: draft
project: comic-studio
created: 2026-08-24
---

# UC-10 — Quản lý credit và BYOK

> [!CAUTION]
> ⚠️ **UC NÀY NẰM NGOÀI HORIZON 09/2026–02/2027.** Credit ledger ở **MVP3**, BYOK ở **MVP4** — [`Roadmap` §5.1](../../010-Planning/Roadmap.md#51-cái-gì-rơi-ra-khỏi-092026022027) xếp **credit ledger + hard quota (`X-b`)**, **BYOK** và **mọi gói trả phí CÓ image gen** vào danh sách **rơi ra khỏi horizon**. Tài liệu này tồn tại để **kiến trúc không bị retrofit** (`BR-006-06`: *"thiết kế cho **ba** tầng ngay từ đầu, không retrofit"*), **không** để lập kế hoạch sprint gần.
>
> ⛔ **BYOK là tuỳ chọn MỞ KHOÁ, KHÔNG phải điều kiện để dùng sản phẩm** (CF-2.4 `[CHỐT]`). Vì vậy trong tài liệu này **BYOK nằm ở `## 4. Alternative flow`, không nằm ở main flow** — vị trí cấu trúc là một cách cưỡng chế: đặt BYOK vào main flow là đọc ngược mô hình đã chốt.

**Quy ước nhãn nguồn** (kế thừa nguyên vẹn — *số và nhãn là một cặp không tách rời*): `[OFF]` official/paper gốc · `[BCN]` báo cáo ngành có tên firm · `[TC]` thứ cấp · `[EM]` ước lượng/phép nhân, **không phải số đo** · `[CHỐT]` quyết định của Founder tại gate.

## Mục lục

1. [Thông tin](#1-thông-tin)
2. [Mục tiêu](#2-mục-tiêu)
3. [Main flow](#3-main-flow)
4. [Alternative flow](#4-alternative-flow)
5. [Exception flow](#5-exception-flow)
6. [Tài liệu liên quan](#6-tài-liệu-liên-quan)

---

## 1. Thông tin

| Trường | Giá trị |
|---|---|
| **Primary actor** | **Tác giả truyện chữ — power user** (CF-1.5 `[CHỐT]`, không biết vẽ). ⚠️ *"Power user"* ở đây **không phải một persona mới**: findings §6.2 `KT-1` ghi rõ **repo KHÔNG CÓ persona / JTBD**. Nó là **một trạng thái sử dụng** — người vượt ngưỡng **~125 ảnh/tháng** `[TC]`. [R-07](../../010-Planning/Risk-Register.md) đi xa hơn: *"phân khúc mục tiêu chính **là** power user"* |
| **Secondary actor** | **Founder với vai operator** — sở hữu `hold reaper`, hard quota, và các đường lui của gate `G2` ([AF-3](#4-alternative-flow)). **Vendor billing** là **hệ thống ngoài**, không phải actor người: `E4` = **mua billing, không tự viết** |
| **Mốc MVP** | **MVP3 — credit ledger + hard quota** (`F3`, `F4`; exit criteria **`M3-1`, `M3-2`, `M3-3`**) · **MVP4 — BYOK** (`F5`). ⛔ **CẢ HAI ĐỀU NGOÀI HORIZON** (`Roadmap` §5.1 · `C10`) |
| **BRD module** | [BRD-006 — Credit And Unit Economics](../BRD/BRD-006-Credit-And-Unit-Economics.md) — `BR-006-03`, `BR-006-04`, `BR-006-05`, `BR-006-06`. Phụ thuộc chéo: [BRD-005](../BRD/BRD-005-Multi-Tenancy-And-Platform.md) (`E4` mua billing · `E5` một transaction boundary) · [BRD-001](../BRD/BRD-001-Image-Generation-Pipeline.md) (`A5` job queue, `A7` whole-page) · [BRD-007](../BRD/BRD-007-Legal-And-Compliance.md) (`KC-4`) |
| **Điều kiện tiên quyết** | (1) ⭐ **`G0` PASS** — *"Bật thanh toán (bất kỳ tầng nào)"* bị `G0` **chặn CỨNG** (`Roadmap` §6.2); (2) **`X-b` hoàn tất** — credit ledger + hold + `CHECK (available >= 0)` + reaper + hard quota, **trước bản trả phí ĐẦU TIÊN CÓ image gen** (CF-8.11b); (3) `usage_event` + `usage_daily` đã có từ **MVP1** (`BR-006-01`) — không có nó thì không có gì để đối soát; (4) `tenant_id` + RLS (`KC-5`) — số dư là dữ liệu per-tenant |

### 1.1 Mô hình đã CHỐT — ba tầng, và vị trí của BYOK trong đó

| Tầng | Nội dung | Vai trò | UC-10 có tham gia? |
|---|---|---|---|
| **Tầng 1** | **$4–8/tháng, KHÔNG có image gen** — Story Bible + Comic IR + layout + versioning + export. Margin **~90%**, **không cần API key** | ⭐ **CỬA VÀO** | **KHÔNG** — xem [AF-2](#4-alternative-flow). Người dùng vào sản phẩm **trước khi** gặp API key hay credit |
| **Tầng 2** | **Credit pack KHÔNG hết hạn**, managed inference, cho user **< ~125 ảnh/tháng** `[TC]` | Đường chính của **user thường** | ✅ **Đây là `## 3. Main flow`** |
| **Tầng 3** | **BYOK — tuỳ chọn MỞ KHOÁ** cho power user vượt ngưỡng | Van xả COGS | ✅ nhưng ở **`## 4. Alternative flow`** (`AF-1`) |

Nguồn: `Charter` §7 `C2` `[CHỐT]` (CF-2.1→CF-2.4) — **đã chốt tại gate, không mở lại trong horizon này**. `MVP-Scope` §3 `F5`, `F6`.

### 1.2 ⚠️ BYOK có đánh đổi phải nêu — và đó là rủi ro sản phẩm số 1

> [!WARNING]
> `Glossary.md` term *BYOK*: *"Xoá hoàn toàn rủi ro COGS và làm biến mất xung đột giữa tính năng cốt lõi và margin. ⚠️ **Đánh đổi: friction cao với người dùng non-technical ⇒ onboarding flow trở thành rủi ro sản phẩm số 1.**"*
>
> Hệ quả bắt buộc lên UC này: **mô hình 3 tầng là CẤU TRÚC NÉ rủi ro đó, không phải cách GIẢI nó** ([BRD-006](../BRD/BRD-006-Credit-And-Unit-Economics.md) mục 1.1). Nghĩa là: khi BYOK gặp lỗi, **đường lui luôn là Tầng 1 hoặc Tầng 2 — không bao giờ là "hướng dẫn user kiên trì hơn"**. Xem [`EF-4`](#5-exception-flow).
>
> ⚠️ **Độ lớn của ma sát: KHÔNG ĐO ĐƯỢC** — [R-23](../../010-Planning/Risk-Register.md) là `mitigating` và khoảng trống `G-08` ghi rõ chưa có số. ⛔ UC này **không** gán một tỉ lệ drop-off nào.

### 1.3 Ngưỡng ~125 ảnh/tháng và một hệ quả phải ghi lại

**Ngưỡng phân tuyến Tầng 2 / Tầng 3: ~125 ảnh/tháng** `[TC]` (CF-2.5 — nguồn là **bên bán managed** nhưng khuyến nghị **ngược chiều lợi ích của họ** ⇒ chấp nhận được; ⛔ **không nâng lên `[OFF]`**).

> [!CAUTION]
> **1 chapter @N=3 = 180 ảnh** ⚠️ `[EM]` (CF-3.9 — phép nhân **60 ảnh/chapter** ⚠️ `[EM]` CF-3.3 × **N=3** `[OFF]`; CF-3.3 là **giả định của `researcher` run trước, KHÔNG phải số đo**) ⇒ **vượt ngưỡng ~125 ngay ở chapter đầu tiên**.
>
> Hệ quả phải viết đúng sắc thái (`BR-006-09` · `MVP-Scope` `G2-d`): nếu đo được rằng **phần lớn user hoạt động vượt ngưỡng**, thì *"BYOK không còn là **tuỳ chọn mở khoá** trên thực tế"* — và đó là **một PHÁT HIỆN PHẢI GHI LẠI, KHÔNG phải một lỗi đo**, cũng **không phải** một lệnh đổi cửa vào ([BRD-006](../BRD/BRD-006-Credit-And-Unit-Economics.md) mục 5 hàng 3).

---

## 2. Mục tiêu

**Người dùng nắm được và điều khiển được chi phí biến đổi của mình**: nạp credit, thấy số dư và mức tiêu, hoặc — nếu vượt ngưỡng — **bật BYOK để tự chịu COGS**.

Nhìn từ phía nền tảng, cùng một luồng có một mục tiêu thứ hai: **cưỡng chế chi phí TRƯỚC khi nó xảy ra**. Hai chữ *"trước khi"* là toàn bộ nội dung của module F ([BRD-006](../BRD/BRD-006-Credit-And-Unit-Economics.md) mục 1) — vì **mỗi lần generate là tiền thật đã tiêu và không hoàn lại được**.

| # | Điều làm UC này khác các UC còn lại | Căn cứ |
|---|---|---|
| **1** | **Nó không tạo ra artifact nào.** Mọi UC khác của tác giả sinh ra dữ liệu truyện; UC-10 chỉ đổi **quyền được tiêu tài nguyên** | `MVP-Scope` §3 nhóm `F` |
| **2** | **Cơ chế phải là cưỡng chế tự động ở TẦNG DB, không phải quy trình do người canh** — vì đội là **1 người + AI assist**, *"không có người thứ hai để canh"* | `Charter` §7 `C1` `[CHỐT]` (CF-1.2) · [BRD-006](../BRD/BRD-006-Credit-And-Unit-Economics.md) mục 4.2 |
| **3** | **Sai ở đây không hiện ra như một lỗi.** Thiếu `hold reaper` thì lỗi **rỉ chậm** thành *"có credit mà không generate được"* — `Glossary.md` gọi đây là **loại lỗi khó chẩn đoán nhất** | `Glossary.md` *hold reaper* · CF-6.12 |

⛔ **Ngoài mục tiêu**: UC này **không** định giá, **không** mở subscription phẳng *"unlimited"* và **không** mở free tier kiểu *"100 ảnh/ngày"* (CF-2.7 · `CẤM-17` — *"cấm đưa vào PRD dưới bất kỳ dạng nào"*, **không có điều kiện mở lại**).

---

## 3. Main flow

**Bối cảnh mốc: MVP3 — Tầng 2, credit pack không hết hạn, managed inference.** ⚠️ **NGOÀI horizon.**

| # | Actor thực hiện | Hành động | Căn cứ |
|---|---|---|---|
| **1** | **Tác giả truyện chữ** | Mở mục quản lý credit trong workspace của tenant mình | `KC-5` (`tenant_id` + RLS — số dư là dữ liệu per-tenant) |
| **2** | **Hệ thống** | Hiển thị **ba số tách bạch**: credit **khả dụng** (`available`), credit **đang bị HOLD**, và **mức tiêu** theo rollup `usage_daily`. ⛔ Không gộp `available` với credit đang hold — đó chính là nguồn của cảm giác *"có credit mà không generate được"* | `BR-006-01` · `BR-006-03` · `Glossary.md` *credit ledger + hold*, *`usage_event`* |
| **3** | **Tác giả truyện chữ** | Chọn mua một **credit pack** — **không hết hạn** | CF-2.3 `[CHỐT]` · `MVP-Scope` §3 `F6`/`F5` bối cảnh 3 tầng |
| **4** | **Hệ thống** | Chuyển sang **vendor billing đã mua** — ⛔ **không tự viết luồng thanh toán** | `MVP-Scope` §3 `E4` (*mua billing*) → [BRD-005](../BRD/BRD-005-Multi-Tenancy-And-Platform.md) |
| **5** | **Vendor billing** *(hệ thống ngoài)* | Xử lý thanh toán và trả kết quả về | `E4` |
| **6** | **Hệ thống** | Ghi **một dòng append-only** vào **credit ledger** cho lần nạp. Ledger là **append-only** để dùng được làm **căn cứ đối soát** | `BR-006-03` · `MVP-Scope` §6 **`KC-7`** · `Glossary.md` *`usage_event`* (append-only là điều kiện đối soát) |
| **7** | **Tác giả truyện chữ** | Bắt đầu một lượt sinh panel (luồng của [UC-06](./UC-06-Generate-Panel-And-Pick-Variant.md)) | `MVP-Scope` §3 `A1` |
| **8** | **Hệ thống** | ⭐ **TRƯỚC KHI ENQUEUE**: cưỡng chế **hard quota** (⛔ **không đếm sau**) rồi đặt **HOLD** với **reserve 3 credit/panel** — vì **N = 3 là mặc định cho MỌI panel**, **không phải retry-on-failure**. Lớp cuối là `CHECK (available >= 0)` **ở tầng DB**, **không bypass được bằng code** | `Roadmap` §2 **`M3-2`**, **`M3-3`** · CF-8.11b · CF-6.12 · CF-3.1/3.2 `[OFF]` · `MVP-Scope` §6 `KC-7` |
| **9** | **Hệ thống** | **Chỉ khi hold thành công** thì enqueue job vào queue trong Postgres | `MVP-Scope` §3 `A5` · `Roadmap` §4 việc **`X-b`** (*"Check-rồi-gọi là race condition"*) |
| **10** | **Hệ thống** | Khi job hoàn tất: **settle** hold thành khoản trừ thật, đồng thời ghi `usage_event` **append-only** kèm `cost_usd` + `model_id` + `model_version` + `attempt_no`. Ba INSERT `generation` + `change_log` + `usage_event` **commit CÙNG MỘT transaction** | `BR-006-01`, `BR-006-02` · `MVP-Scope` §6 **`KC-4`** · [BRD-007](../BRD/BRD-007-Legal-And-Compliance.md) `BR-007-02` |
| **11** | **Hệ thống — `hold reaper`** *(job nền theo chu kỳ; **Founder vai operator** là người sở hữu và cấu hình nó)* | Thu hồi các hold **quá hạn `expires_at`** về `available` | `BR-006-03` · `Roadmap` §2 **`M3-1`** · `Glossary.md` *hold reaper* |
| **12** | **Tác giả truyện chữ** | Thấy số dư và mức tiêu đã cập nhật; biết mình còn generate được bao nhiêu **trước khi** bắt đầu lượt sau | `BR-006-01` |

> [!IMPORTANT]
> **Thứ tự bước 8 → 9 là bản chất của UC này, không phải chi tiết triển khai.**
>
> Đảo lại thành *check rồi gọi* là **race condition**: **10 job đồng thời đều thấy đủ số dư và đều chạy** ⇒ **vượt trần** ([R-14](../../010-Planning/Risk-Register.md) · CF-6.12). `M3-1` đo đúng điều này bằng một test: *"10 job đồng thời trên số dư đủ cho 5 job ⇒ **đúng 5 job chạy**"*.
>
> Và reserve **phải là 3, không phải 1**: *"reserve 1 credit rồi tính sau = **hợp lệ hoá số dư âm**"* — tức *"hệ thống được thiết kế để **vượt trần trong trường hợp bình thường**"* (`MVP-Scope` §6.1). ⛔ `CẤM-03`: **cấm lấy chất lượng của N=3 mà tính chi phí của N=2**; hạ N là đổi chất lượng lấy margin ⇒ **phải chạy lại `G1`**, không phải chỉ `G2`.

---

## 4. Alternative flow

| ID | Nhánh | Ai làm gì | Căn cứ |
|---|---|---|---|
| **AF-1** ⭐ | **Bật BYOK — tuỳ chọn MỞ KHOÁ (MVP4)** | **Tác giả (power user)** vượt ngưỡng **~125 ảnh/tháng** `[TC]` chọn bật BYOK và nhập API key của provider. **Hệ thống** dùng key đó cho các lần generate của tenant ⇒ **user tự chịu COGS**, xoá xung đột giữa tính năng cốt lõi và margin. ⛔ **Đây là đường MỞ KHOÁ cho người đã ở trong sản phẩm — KHÔNG phải cửa vào, KHÔNG phải điều kiện dùng sản phẩm** (CF-2.4 `[CHỐT]`). ⚠️ **MVP4 — NGOÀI horizon** | `MVP-Scope` §3 `F5` · `BR-006-05` · CF-2.4 `[CHỐT]` · CF-2.5 `[TC]` · `Glossary.md` *BYOK* |
| **AF-2** | **Người dùng Tầng 1 — UC này KHÔNG phát sinh** | **Tác giả** dùng Tầng 1 (**$4–8/tháng, KHÔNG image gen**): Story Bible + Comic IR + layout + versioning + export. **Không cần credit, không cần API key.** Đây là **cửa vào** của mô hình và là lý do BYOK không bao giờ trở thành rào | `MVP-Scope` §3 `F6` · CF-2.2 `[CHỐT]` (margin ~90%) · `BR-006-07`. ⚠️ Việc **có bán Tầng 1 trong horizon hay không** là một **LỰA CHỌN `[EM]`** — xem [mục 6.2](#62-brd-phụ-thuộc-chéo) |
| **AF-3** | **Đường lui khi gate `G2` FAIL** — actor đổi sang **Founder (operator)** | **Founder** đi theo **ba đường lui đã thiết kế sẵn, theo thứ tự**: (1) đổi granularity render sang **whole-page** — ⭐ **data model KHÔNG phải đổi**; (2) whole-page là mặc định, **per-panel trở thành hành động TRẢ PHÍ**; (3) đẩy **BYOK lên đường chính** cho nhóm vượt ngưỡng. ⛔ Đường **BỊ LOẠI TƯỜNG MINH**: hạ `N` từ 3 xuống 1 | `MVP-Scope` §7.3 · `BR-006-10` · CF-10.7 ⚠️ **hai caveat**: `+40%` margin của whole-page **vẫn DƯỚI dải kỳ vọng 50–60%** `[BCN]`, và phép so sánh **lệch hạng nguồn** (`[EM]` vs `[BCN]`) ⇒ *"đừng coi nó là lời giải cuối"* |
| **AF-4** | **Đo tỉ lệ user vượt ngưỡng (`G2-d`)** — **Founder (operator)** | **Hệ thống** cung cấp số; **Founder** đọc kết quả. Nếu phần lớn user hoạt động vượt **~125 ảnh/tháng** `[TC]` ⇒ ghi lại *"BYOK không còn là tuỳ chọn mở khoá trên thực tế"* như **một phát hiện**, ⛔ **không** như một lỗi đo, ⛔ **không** như một lệnh đổi cửa vào | `MVP-Scope` §7.3 `G2-d` · `BR-006-09` · CF-3.9 `[EM]` |

---

## 5. Exception flow

**Sáu nhánh. Ba nhánh đầu là ba lỗi độc lập của `KC-7`; nhánh `EF-5` là nhánh mà `Glossary.md` gọi là khó chẩn đoán nhất.**

| ID | Điều kiện phát sinh | Ai làm gì | Kết cục | Căn cứ |
|---|---|---|---|---|
| **EF-1** ⭐ | **`available` không đủ để hold `3 × số panel`** | **Hệ thống** **TỪ CHỐI ngay tại bước 8 — TRƯỚC khi enqueue**, nêu rõ cần thêm bao nhiêu credit | Job **không được tạo**, **không có lời gọi provider nào**. ⛔ Không tồn tại đường *"cứ chạy rồi trừ sau"* — **đếm sau là pattern bị cấm** | CF-8.11b · `Roadmap` §2 **`M3-3`** · [BRD-006](../BRD/BRD-006-Credit-And-Unit-Economics.md) mục 5 hàng 5 |
| **EF-2** | **Nhiều job đồng thời cùng thấy đủ số dư** (race condition) | **Hệ thống** dựa vào `CHECK (available >= 0)` **ở tầng DB** làm lớp cuối — **không bypass được bằng code ứng dụng** | Chỉ số job mà số dư cho phép được chạy. Đo bằng test `M3-1`: **10 job đồng thời trên số dư đủ cho 5 ⇒ đúng 5 job chạy** | `Roadmap` §2 **`M3-1`** · CF-6.12 · [R-14](../../010-Planning/Risk-Register.md) |
| **EF-3** | **Job crash / treo SAU khi hold đã đặt** | **`hold reaper`** (Founder vai operator sở hữu) thu hồi hold khi quá `expires_at` | Credit trở về `available`. ⚠️ **Thiếu reaper thì hold treo VĨNH VIỄN** ⇒ rỉ chậm thành *"có credit mà không generate được"* — **loại lỗi khó chẩn đoán nhất** | `Glossary.md` *hold reaper* · CF-6.12 · `MVP-Scope` §6 `KC-7` (c) |
| **EF-4** ⭐ | **BYOK thất bại**: user **không lấy được API key** ở provider · key **nhập sai / hết hiệu lực** · key **hết quota phía provider** | **Hệ thống** báo lỗi **nêu rõ đây là giới hạn của key của user, không phải lỗi truyện của họ**, và **đưa đường lui về Tầng 2 (credit pack) hoặc Tầng 1 (không image gen)** | ⛔ **Không** biến BYOK thành điều kiện tiếp tục dùng sản phẩm. Căn cứ: onboarding BYOK là **rủi ro sản phẩm số 1** với người dùng **non-technical**, và mô hình 3 tầng là **cấu trúc né** rủi ro đó. ⚠️ **Độ lớn ma sát: không đo được** (`G-08`) ⇒ ⛔ không gán tỉ lệ drop-off | `Glossary.md` *BYOK* · CF-2.4 `[CHỐT]` · [R-23](../../010-Planning/Risk-Register.md) · `BR-006-05` |
| **EF-5** | **`hold reaper` sai chu kỳ**: thu hồi hold của một job **đang chạy chậm** nhưng còn sống | **Founder (operator)** — đây là **residual risk đã được ghi trước**, không phải một sự cố bất ngờ | ⚠️ **`user mất credit oan`** — nguyên văn residual của [R-14](../../010-Planning/Risk-Register.md). **Cơ chế phân biệt *"job còn sống"* vs *"job đã chết"* và chu kỳ reaper: `TBD`** — không nguồn nào trong repo đặt con số này, ⛔ **không tự gán** | [R-14](../../010-Planning/Risk-Register.md) residual · `BR-006-03` |
| **EF-6** | **Thanh toán ở vendor billing thất bại** | **Vendor billing** trả kết quả thất bại; **Hệ thống** **không ghi dòng nạp nào** vào ledger | Số dư không đổi. Vì ledger là **append-only**, một dòng nạp ghi sai **không xoá được** — nên điều kiện ghi phải là **kết quả xác nhận từ vendor**, không phải ý định thanh toán | `E4` → [BRD-005](../BRD/BRD-005-Multi-Tenancy-And-Platform.md) · `BR-006-03` (append-only) |

> [!CAUTION]
> **`EF-1`, `EF-2`, `EF-3` là BA LỖI ĐỘC LẬP của cùng một `KC-7`** — `MVP-Scope` §6 liệt kê chúng riêng vì **sửa một cái không sửa hai cái kia**: (a) check-rồi-gọi là race condition; (b) reserve 1 credit/panel là hợp lệ hoá số dư âm; (c) thiếu reaper là hold treo vĩnh viễn. **Bốn thành phần của `KC-7` là một bộ không tách** (`BR-006-03`).

---

## 6. Tài liệu liên quan

### 6.1 Traceability lên tầng trên

| Quan hệ | Tài liệu |
|---|---|
| **Part of (Epic)** | [Epic-Credit-And-Unit-Economics](../../022-User-Stories/Epics/Epic-Credit-And-Unit-Economics.md) |
| **Requirement cha** | [BRD-006 — Credit And Unit Economics](../BRD/BRD-006-Credit-And-Unit-Economics.md) — `BR-006-03` (ledger + hold + reaper), `BR-006-04` (hard quota trước enqueue), `BR-006-05` (BYOK mở khoá), `BR-006-06` (thiết kế cho ba tầng, không retrofit), `BR-006-09`, `BR-006-10` |
| **Sản phẩm** | [PRD-Comic-Studio](../PRD-Comic-Studio.md) — mục *Kinh tế & credit* |
| **Hệ thống** | [SRS-Comic-Studio](../SRS-Comic-Studio.md) |

### 6.2 BRD phụ thuộc chéo

| BRD | Vì sao liên quan |
|---|---|
| [BRD-005 — Multi-Tenancy And Platform](../BRD/BRD-005-Multi-Tenancy-And-Platform.md) | `E4` **mua billing, không tự viết** (bước 4–5) · `E5` **một** transaction boundary — điều kiện để `KC-4` thực hiện được (bước 10) · `E1`/`KC-5` số dư per-tenant |
| [BRD-001 — Image Generation Pipeline](../BRD/BRD-001-Image-Generation-Pipeline.md) | `A5` job queue trong Postgres (bước 9) · `A7` **whole-page** — requirement kỹ thuật của **đường lui #1** ở `AF-3` · `A6` fairness per tenant (*seam kinh tế*) |
| [BRD-007 — Legal And Compliance](../BRD/BRD-007-Legal-And-Compliance.md) | `KC-4` — `usage_event` là **một trong ba INSERT** phải commit cùng transaction · `BLOCKER-03` (hard quota chưa có ⇒ **chặn bản trả phí đầu tiên**) |
| [BRD-008 — Quality And Operations](../BRD/BRD-008-Quality-And-Operations.md) | `H4` export — **điều kiện doanh thu của Tầng 1**. ⚠️ Việc bán Tầng 1 trong horizon là một **LỰA CHỌN `[EM]`** của `Roadmap` §5.2, **không phải kế hoạch đã chốt**: gated on **`G0` PASS + `M2-5` + `M2-6` + quyết định Founder tại `G2`** |

### 6.3 Use Case liền kề

| UC | Quan hệ |
|---|---|
| [UC-06 — Generate Panel And Pick Variant](./UC-06-Generate-Panel-And-Pick-Variant.md) | Nơi credit **thực sự bị tiêu** — bước 7→10 của UC này chạy bên trong đó |
| [UC-09 — Export Chapter](./UC-09-Export-Chapter.md) | Đường giá trị của **Tầng 1** (`AF-2`) — không tiêu credit, không cần API key |
| [UC-01 — Upload And Ingest Chapter](./UC-01-Upload-And-Ingest-Chapter.md) | Nơi **abuse control cho upload** cần có **ngay ở MVP1**, dù `X-b` (quota + ledger) ở MVP3 — `Roadmap` §4 lưu ý phạm vi của `X-b` |

### 6.4 Tài liệu tham khảo

| Tài liệu | Phần được dùng ở đây |
|---|---|
| [MVP-Scope.md](../../010-Planning/MVP-Scope.md) | **§3 nhóm F** (`F1`–`F6`) · §3 `A1`, `A5`, `E4` · **§6 `KC-7`**, `KC-4`, `KC-5` · **§6.1** (ba hiểu nhầm về `KC-7`) · **§7.3 gate `G2`** (`G2-a`, `G2-d`, ba đường lui, đường bị cấm) |
| [Roadmap.md](../../010-Planning/Roadmap.md) | §2 exit criteria **`M3-1`, `M3-2`, `M3-3`** · **§4 việc `X-b`** (trigger: *trước bản trả phí ĐẦU TIÊN CÓ image gen*; kèm lưu ý **abuse control cần ngay ở MVP1**) · **§5.1** (credit ledger, hard quota, BYOK, mọi gói trả phí có image gen **rơi ra ngoài horizon**) · §5.2 · **§6.2** (`G0` PASS chặn cứng **bật thanh toán bất kỳ tầng nào**) |
| [Charter-Comic-Studio.md](../../010-Planning/Charter-Comic-Studio.md) | §7 `C1` (1 người ⇒ cưỡng chế ở tầng DB) · **`C2`** (mô hình 3 tầng `[CHỐT]`) · `C6` (margin kỳ vọng **50–60%** `[BCN]`, không phải 80%) · `C7` (**$12,06/chapter là SÀN, không phải trần** — `CẤM-04`) · `C8` (**N=3**, `CẤM-03`) · `C10` |
| [Risk-Register.md](../../010-Planning/Risk-Register.md) | `R-07` (power user), `R-14` (race condition ở ledger + residual *"user mất credit oan"*), `R-23` (ma sát BYOK, `mitigating`), `R-09`, `R-11` · khoảng trống `G-08` |
| [Glossary.md](../../999-Resources/Glossary.md) | ***BYOK*** (đánh đổi + rủi ro sản phẩm số 1) · ***credit ledger + hold*** · ***hold reaper*** · ***`usage_event`*** · *seam kinh tế vs seam kỹ thuật* |
| [findings/business-analyst.md](../../010-Planning/pm-runs/2026-08-24-khoi-tao-requirements-stories-comic-studio/findings/business-analyst.md) | **§3.2** hàng `UC-10` (actor · mục tiêu · BRD · mốc · anchor) · §5.2 CF-2.1→2.5, CF-2.7, CF-3.1/3.2, CF-3.3, CF-3.9, CF-6.12, CF-8.11b, CF-10.7 · §5.3 `CẤM-03`, `CẤM-04`, `CẤM-15`, `CẤM-16`, `CẤM-17` · §6.2 `KT-1`, `KT-10` |
| [Documents-Template.md](../../../knowledge-base/99-Templates/Documents-Template.md) | `RULE-001` — thư mục `docs/020-Requirements/Use-Cases/`, naming `UC-{NN}-{Title}.md`, frontmatter, **standard markdown link** (quy tắc #5) |

> ⛔ **Không link tới `docs/030-Specs/`** — tầng technical spec chưa tồn tại và nằm ngoài scope của run này.
>
> ⛔ **`CẤM-15`**: tài liệu này **không tự tra lại và không tự tính lại** bất kỳ con số nào đã có trong bảng CF. Con số duy nhất là phép nhân đã có sẵn (CF-3.9 = CF-3.3 × N) và nó được trích **kèm nguyên nhãn `[EM]` của cả hai thừa số**.

---

_Use Case by Comic Studio — role `business-analyst`._
_Author: trisjr_
</content>
