---
id: UC-11
type: use-case
status: draft
project: comic-studio
created: 2026-08-24
---

# UC-11 — Gửi và xử lý yêu cầu hạ nội dung (takedown)

> [!CAUTION]
> ⚠️ **ĐÂY LÀ UC DUY NHẤT CÓ PRIMARY ACTOR LÀ NGƯỜI NGOÀI HỆ THỐNG.**
>
> Mọi UC khác của bộ 11 có actor là **tác giả truyện chữ** (khách hàng) hoặc **Founder**. UC-11 có actor là **chủ sở hữu quyền** — một người **chưa từng đăng ký tài khoản** và **có thể không bao giờ đăng ký**. Founder chỉ là **secondary actor với vai operator**.
>
> Đặt sai actor ở đây làm **sai cả mục đích tài liệu**: đây là **cơ chế giữ miễn trừ trung gian theo Điều 198b**, ⛔ **KHÔNG phải một tính năng cho khách hàng**. Căn cứ cắt UC: findings §3.1 — *"Nghĩa vụ pháp lý có actor NGOÀI hệ thống thì phải có UC riêng"*.

> [!WARNING]
> ⛔ **TÀI LIỆU NÀY KHÔNG ĐƯA RA Ý KIẾN PHÁP LÝ MỚI.** Nó **trích và cấu trúc hoá** những gì repo đã ghi, kèm **nhãn nguồn nguyên trạng**. Chỗ nào repo chưa trả lời được thì ghi **`TBD`** kèm câu hỏi phải mang tới **luật sư SHTT Việt Nam**.
>
> ⚠️ **Nhãn nguồn phải mang theo**: CF-7.6 (Điều 198b, SLA 72 giờ, đăng ký đầu mối) là `[OFF]` **TÓM TẮT**, **chưa đọc được nguyên văn** — thuvienphapluat + nhansu trả **403**, IAPP **paywall** (findings §6.2 `KT-5`). [BRD-007](../BRD/BRD-007-Legal-And-Compliance.md) mục 4.5: trích mà bỏ nhãn này làm chúng **mạo danh nguyên văn điều luật**.
>
> ⚠️ **`CẤM-14`**: `GP-3` là **hàng compliance** của `MVP-Scope` §3 nhóm G. `G0`/`G1`/`G2` là **tên ba gate**. ⛔ **Không viết tắt `G3` cho `GP-3`.**

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
| **Primary actor** | ⚠️ **Chủ sở hữu quyền — BÊN NGOÀI HỆ THỐNG.** Không có tài khoản, không thuộc tenant nào, không phải khách hàng, và **có thể không bao giờ trở thành khách hàng**. Người này chỉ tương tác với nền tảng qua **một công cụ tiếp nhận công khai** |
| **Secondary actor** | **Founder với vai operator** — người đánh giá yêu cầu và thực hiện hành động hạ nội dung. ⚠️ **bus factor = 1**: không có người thứ hai (`Charter` §7 `C1` `[CHỐT]` — 1 người + AI assist) ⇒ SLA 72 giờ là nghĩa vụ của **một người** |
| **Mốc MVP** | **MVP2** — `GP-3` = `🟡` ở MVP1, `✅` ở MVP2; exit criterion **`M2-6`**. ⚠️ **hoặc SỚM HƠN nếu trigger đến sớm hơn** (`BR-007-04` · `Roadmap` §4 việc **`X-a`**) |
| **BRD module** | [BRD-007 — Legal And Compliance](../BRD/BRD-007-Legal-And-Compliance.md) — hàng `GP-3`, requirement **`BR-007-04`**. Đường **tách biệt** với `BR-007-08` (hard-delete tenant). Phụ thuộc chéo: [BRD-008](../BRD/BRD-008-Quality-And-Operations.md) (`H5` abuse controls) · [BRD-005](../BRD/BRD-005-Multi-Tenancy-And-Platform.md) (`KC-5` phạm vi project/tenant) |
| **Điều kiện tiên quyết** | (1) ⭐ **Công cụ tiếp nhận takedown đã tồn tại** — form + email `copyright@`; luật cho phép *"chương trình máy tính, email, hoặc cổng thông tin điện tử"*; (2) ⭐ **Đầu mối liên hệ (email + số điện thoại) đã ĐĂNG KÝ với Bộ Văn hoá, Thể thao và Du lịch**; (3) **Quy trình `SLA 72 giờ` đã tồn tại dưới dạng quy trình, không chỉ ý định**. ⚠️ **CẢ BA phải xong TRƯỚC một TRIGGER, KHÔNG neo vào một ngày** — xem [mục 1.1](#11--điều-kiện-thời-điểm-neo-vào-trigger-không-neo-vào-ngày) |

### 1.1 ⭐ Điều kiện thời điểm: neo vào TRIGGER, không neo vào ngày

> [!IMPORTANT]
> **Trigger (nguyên văn `Roadmap` §4 việc `X-a`): *"Trước lần đầu mở cho NGƯỜI NGOÀI upload"*.**
>
> `Roadmap` §4 giải thích vì sao neo vào trigger chứ không neo vào ngày: *"Neo vào ngày thì dễ bị dời; neo vào trigger thì **không thể 'làm sau' mà vẫn hợp lệ**."*
>
> Và vì sao không được dồn cuối, nguyên văn: *"**Một lần upload của người ngoài mà chưa có đường takedown là đã tạo ra nghĩa vụ pháp lý KHÔNG RÚT LẠI ĐƯỢC.** Rẻ để làm trước, không sửa được sau."*
>
> `Roadmap` §6.2 xếp phụ thuộc **`X-a` safe harbour → mở cho người ngoài upload** là **CỨNG** (CF-8.11a). `Charter` §9.3 **`BLOCKER-02`**: checklist safe harbour Điều 198b chưa hoàn tất ⇒ **chặn việc mở cho người ngoài upload** (không chặn dùng nội bộ).

### 1.2 ⛔ Takedown KHÁC hard-delete tenant — hai đường TÁCH BIỆT

> [!CAUTION]
> **Gộp hai thứ này là một lỗi.** [BRD-007](../BRD/BRD-007-Legal-And-Compliance.md) đã **tách chúng thành hai `BR` row**, và UC này giữ đúng phân biệt đó.
>
> | | **Takedown — `BR-007-04`** (luồng của UC này) | **Hard-delete tenant — `BR-007-08`** (KHÔNG thuộc UC này) |
> |---|---|---|
> | **Ai khởi xướng** | **Chủ sở hữu quyền — người NGOÀI** | **Tenant / chủ tài khoản** — người TRONG hệ thống |
> | **Cơ chế** | **soft-delete + disable-access ở CẤP PROJECT** | **xoá cứng toàn bộ dữ liệu tenant**, kỷ luật `ON DELETE CASCADE` trên **mọi** FK |
> | **Dữ liệu sau đó** | ⭐ **PHẢI GIỮ** — *"dữ liệu còn phải giữ cho **counter-notice**"* | **Không còn** — và đường này **phải đã được KIỂM THỬ** |
> | **Vì sao tồn tại** | Điều kiện giữ **miễn trừ Điều 198b** | Quyền rút khỏi hệ thống phải là quyền **thực thi được, không phải lời hứa** |
> | **Hàng nguồn** | `MVP-Scope` §3 **`GP-3`** | `MVP-Scope` §3 **`GP-5`** |
>
> ⛔ **`BR-007-04` ghi tường minh: takedown là "KHÔNG hard delete".** Thực hiện takedown bằng cách xoá cứng là **phá mất chính bằng chứng** mà counter-notice cần — và với dữ liệu provenance thì **không backfill được** (CF-7.3).

---

## 2. Mục tiêu

**Mục tiêu của primary actor (chủ sở hữu quyền):** gửi được một yêu cầu hạ nội dung **mà không cần đăng ký tài khoản**, và **nội dung bị hạ trong vòng 72 giờ**.

**Mục tiêu của nền tảng (bối cảnh, không phải mục tiêu của actor):** giữ được **miễn trừ trung gian theo Điều 198b Luật SHTT** (sửa đổi 2022 — Luật 07/2022/QH15, chuyển hoá từ Điều 12.55 EVFTA) — miễn trừ này **có điều kiện, không tự động** (`[OFF]` tóm tắt qua [BRD-007](../BRD/BRD-007-Legal-And-Compliance.md) mục 1).

| # | Điều làm UC này khác mọi UC còn lại | Căn cứ |
|---|---|---|
| **1** | **Actor không phải người dùng sản phẩm** ⇒ **không có onboarding, không có tài khoản, không có tenant context**. Công cụ tiếp nhận phải **công khai và dùng được bởi người chưa từng biết sản phẩm** | findings §3.1 nguyên tắc 4 · `BR-007-04` (a) |
| **2** | **Nó là nghĩa vụ, không phải giá trị.** Không có user story nào của khách hàng dẫn tới đây. Nó tồn tại vì `Charter` §9.3 **`BLOCKER-02`** | `Charter` §9.3 · [R-02](../../010-Planning/Risk-Register.md) |
| **3** | **Nó bị giới hạn bởi một con số thời gian: 72 giờ** — con số duy nhất trong bộ 3 UC này mang tính chất **cưỡng chế bên ngoài**, không do dự án tự định nghĩa | CF-7.6 `[OFF]` **tóm tắt** |
| **4** | **Nó vận hành dưới một câu hỏi pháp lý CHƯA CÓ CÂU TRẢ LỜI** — xem [`EF-5`](#5-exception-flow) | findings §6.2 `KT-6` · `MVP-Scope` §7.1 câu **`Q3`** |

⛔ **Ngoài mục tiêu — anti-feature phải nêu thẳng:** UC này **KHÔNG** xây bộ phát hiện bản quyền chủ động.

> [!WARNING]
> **Nghịch lý safe harbour** ([BRD-007](../BRD/BRD-007-Legal-And-Compliance.md) mục 5.2 · [R-04](../../010-Planning/Risk-Register.md)): điều kiện miễn trừ **(a)** của Điều 198b là **"không biết"** nội dung đó xâm phạm quyền. Nên **xây một bộ phát hiện *"truyện này có thể có bản quyền của người khác"* có thể PHÁ chính miễn trừ của mình** — vì nó **tạo ra đúng tri thức mà luật đang miễn trừ cho việc không có**.
>
> Nguyên văn: *"Một dev sẽ làm ngược điều này theo bản năng, vì 'chủ động kiểm tra' nghe như hành vi có trách nhiệm."*
>
> ⇒ Trong main flow, **Founder đánh giá yêu cầu ĐÃ NHẬN**; ⛔ **hệ thống không quét, không flag, không chấm điểm nghi vấn**. Phân biệt với việc **ĐƯỢC PHÉP** (`BR-007-03`): đọc **opt-out signal do chính chủ quyền gắn vào file** là **dữ kiện khách quan** — *"Đọc nhãn không tạo ra tri thức suy đoán."*

---

## 3. Main flow

**Bối cảnh mốc: MVP2 (`GP-3` = `✅`, exit criterion `M2-6`) — hoặc sớm hơn nếu trigger `X-a` đến sớm hơn.**

| # | Actor thực hiện | Hành động | Căn cứ |
|---|---|---|---|
| **1** | **Chủ sở hữu quyền (bên ngoài)** | Phát hiện trên nền tảng một nội dung mà mình cho là xâm phạm quyền của mình | Analysis §5.7 #5 (nguyên văn: *"takedown và yêu cầu xoá dữ liệu **SẼ** đến"*) |
| **2** | **Chủ sở hữu quyền (bên ngoài)** | Gửi yêu cầu hạ nội dung qua **công cụ tiếp nhận công khai**: **form** hoặc **email `copyright@`**. ⛔ **Không cần đăng ký tài khoản, không cần đăng nhập.** Luật cho phép *"chương trình máy tính, email, hoặc cổng thông tin điện tử"* | `BR-007-04` (a) · `MVP-Scope` §3 `GP-3` · Analysis §8.3 item 1. Lý do chọn *form + email* thay vì hệ thống ticket: `Charter` §7 `C1` — **đội 1 người** |
| **3** | **Hệ thống** | Ghi nhận yêu cầu kèm **timestamp tiếp nhận** — ⭐ **đây là mốc bắt đầu đếm `SLA 72 giờ`** | CF-7.6 `[OFF]` **tóm tắt** · `BR-007-04` (c) |
| **4** | **Hệ thống** | Gửi **xác nhận đã nhận** về địa chỉ liên hệ mà người yêu cầu cung cấp | `BR-007-04` (a) — công cụ tiếp nhận phải là một **đường hai chiều**, không phải một hộp thư đen |
| **5** | **Founder (operator)** | **Đánh giá yêu cầu dựa trên dữ kiện có trong chính yêu cầu đó.** ⛔ **Hệ thống KHÔNG quét, KHÔNG flag, KHÔNG chấm điểm nghi vấn** — xem anti-feature ở [mục 2](#2-mục-tiêu) | [BRD-007](../BRD/BRD-007-Legal-And-Compliance.md) mục 5.2 · [R-04](../../010-Planning/Risk-Register.md) |
| **6** | **Founder (operator)** | ⭐ Thực hiện **soft-delete + disable-access ở CẤP PROJECT** trong **72 giờ** kể từ timestamp ở bước 3. ⛔ **KHÔNG hard delete** — **dữ liệu phải được giữ cho counter-notice** | **`BR-007-04` (c)** · `MVP-Scope` §3 `GP-3` · CF-7.6 `[OFF]` **tóm tắt** |
| **7** | **Hệ thống** | Ghi hành động vào **`change_log`** kèm timestamp (`KC-2` yêu cầu ghi **mọi** hành động), commit **cùng transaction** với thay đổi trạng thái theo `KC-4`. **Dữ liệu gốc giữ nguyên** | `MVP-Scope` §6 `KC-2`, `KC-4` · `BR-007-01`, `BR-007-02` |
| **8** | **Founder (operator)** | **Phản hồi người yêu cầu** kết quả xử lý, **trong SLA 72 giờ** | `BR-007-04` (c) · `Roadmap` §2 **`M2-6`** |
| **9** | **Founder (operator)** | Thông báo cho **tenant sở hữu project bị hạ**. ⚠️ Đây là **điều kiện tối thiểu để counter-notice tồn tại được** — nhưng **nội dung, hình thức và thời hạn của thông báo: `TBD`**, xem [`AF-1`](#4-alternative-flow) | Suy ra từ `BR-007-04` (c) *"dữ liệu còn phải giữ cho counter-notice"*. ⚠️ **Thủ tục cụ thể KHÔNG có trong repo** |
| **10** | **Chủ sở hữu quyền (bên ngoài)** | Nhận phản hồi. Kết thúc UC: nội dung đã không còn truy cập được, **trong 72 giờ**, và **đầu mối liên hệ đã đăng ký với Bộ VHTTDL** là nơi mọi trao đổi tiếp theo đi qua | `BR-007-04` (b) |

> [!NOTE]
> **Bước 3 phải xảy ra TRƯỚC bước 5.** Lý do là bản chất chứng minh: **`SLA 72 giờ` chỉ chứng minh được nếu có một timestamp tiếp nhận được ghi bởi hệ thống**, không phải bởi ký ức của Founder. Cùng nguyên tắc `KC-4` của [BRD-007](../BRD/BRD-007-Legal-And-Compliance.md): *"Bằng chứng có thể thiếu ngẫu nhiên thì không phải bằng chứng."*

---

## 4. Alternative flow

| ID | Nhánh | Ai làm gì | Căn cứ / trạng thái |
|---|---|---|---|
| **AF-1** ⚠️ | **Counter-notice — tenant phản đối việc hạ nội dung** | **Tenant (chủ project bị hạ)** gửi phản đối; **Founder (operator)** xem xét; dữ liệu vẫn còn nguyên nên **về mặt kỹ thuật có thể phục hồi** | ⚠️ **`TBD` — repo CHỈ nói rằng DỮ LIỆU ĐƯỢC GIỮ CHO counter-notice, KHÔNG định nghĩa THỦ TỤC.** Không có nguồn nào trong repo cho: các trường bắt buộc của counter-notice · thời hạn phản đối · điều kiện và thủ tục phục hồi truy cập · ai chịu trách nhiệm nếu phục hồi sai. ⛔ **UC này KHÔNG phát minh thời hạn hay bước phục hồi.** ⇒ **Câu hỏi mang tới luật sư SHTT**, xem [mục 6.4](#64-ba-câu-hỏi-tbd-phải-mang-tới-luật-sư-shtt) |
| **AF-2** | **Trigger đến SỚM hơn MVP2** | **Founder (operator)** phải hoàn tất checklist `GP-3` **trước** khi mở cho người ngoài upload, **bất kể đang ở mốc nào** | `BR-007-04` (*"MVP2 — hoặc **sớm hơn** nếu trigger đến sớm hơn"*) · `Roadmap` §4 `X-a` · `Charter` §9.3 `BLOCKER-02`. ⚠️ Đây **không** là một nhánh tuỳ chọn: nó là nhánh mà **thời điểm quyết định, không phải lịch trình quyết định** |
| **AF-3** | **Yêu cầu đến trong giai đoạn CHƯA mở cho người ngoài** (MVP0 / MVP1, dữ liệu là của chính Founder) | **Founder (operator)** vẫn xử lý yêu cầu, nhưng **nghĩa vụ trung gian chưa phát sinh** ở thời điểm đó | `Roadmap` §6.1 bảng: MVP0 và MVP1 — *"Không có người ngoài upload ⇒ **không phát sinh nghĩa vụ safe harbour**"*. Đây chính là lý do trigger được neo vào *"mở cho người ngoài upload"*, chứ không vào *"có dữ liệu trên hệ thống"* |
| **AF-4** | **Người yêu cầu đòi XOÁ VĨNH VIỄN dữ liệu** | **Founder (operator)** giải thích rằng takedown là **soft-delete + disable-access cấp project** và dữ liệu **phải được giữ cho counter-notice** ⇒ yêu cầu xoá vĩnh viễn **NGOÀI luồng này** | ⛔ Đường hard-delete (`BR-007-08`) là đường **tách biệt** và do **tenant** khởi xướng, không do người ngoài. Xem [mục 1.2](#12--takedown-khác-hard-delete-tenant--hai-đường-tách-biệt). ⚠️ Việc một yêu cầu của người ngoài **có thể buộc** xoá vĩnh viễn hay không: **`TBD`** — không nguồn nào trong repo trả lời |

---

## 5. Exception flow

**Năm nhánh. `EF-5` là nhánh đặc biệt: nó không phải lỗi vận hành mà là một khoảng trống pháp lý bao trùm toàn bộ UC.**

| ID | Điều kiện phát sinh | Ai làm gì | Kết cục / trạng thái | Căn cứ |
|---|---|---|---|---|
| **EF-1** | **Thông tin trong yêu cầu không đủ để xác định nội dung bị khiếu nại** | **Founder (operator)** phản hồi **yêu cầu bổ sung thông tin** qua đúng đầu mối đã đăng ký. ⛔ **Không** tự đi tìm/quét để đoán nội dung nào đang bị nhắm tới — đó là hành vi rơi vào anti-feature [R-04](../../010-Planning/Risk-Register.md) | ⚠️ **`TBD` hai thứ**: (a) **danh sách trường bắt buộc** của một yêu cầu hợp lệ — findings §6.2 **`KT-5`**: nguyên văn NĐ 17/2023 và NĐ 134/2026 **chưa đọc được** (403 / paywall); (b) **đồng hồ `SLA 72 giờ` có tạm dừng khi chờ bổ sung hay không** — ⛔ **không nguồn nào trong repo nói, không tự phân xử** | `KT-5` · CF-7.4 ⚠️ `[OFF]` **tóm tắt** · `CẤM-13` |
| **EF-2** ⭐ | **Quá 72 giờ mà yêu cầu chưa được xử lý** | **Founder (operator)** — không có người thứ hai để chuyển giao (**bus factor = 1**) | ⚠️ **Điều kiện miễn trừ Điều 198b có nguy cơ không thoả.** Đây chính là nội dung của [R-02](../../010-Planning/Risk-Register.md) (Score **6**, `open`, owner **`security-auditor`**) và của `Charter` §9.3 **`BLOCKER-02`**. ⛔ UC này **không** đưa ra kết luận pháp lý về hệ quả của việc trễ — đó là câu hỏi luật sư | [R-02](../../010-Planning/Risk-Register.md) · `Charter` §9.3 · CF-7.6 `[OFF]` **tóm tắt** |
| **EF-3** | **Project/tenant đã bị XOÁ CỨNG bởi chính tenant (`BR-007-08`) TRƯỚC khi yêu cầu đến** | **Founder (operator)** phản hồi rằng nội dung **không còn tồn tại trên hệ thống** | ⚠️ Hệ quả kép phải ghi ra: **không còn gì để soft-delete**, và **cũng không còn dữ liệu cho counter-notice**. Đây là điểm **duy nhất hai đường tách biệt của [mục 1.2](#12--takedown-khác-hard-delete-tenant--hai-đường-tách-biệt) gặp nhau** — và chúng gặp nhau ở một trạng thái **không thể đảo ngược** | `BR-007-08` (`ON DELETE CASCADE`, đường đã kiểm thử) · `MVP-Scope` §3 `GP-5` |
| **EF-4** ⛔ | **Một yêu cầu takedown thúc đẩy ý định "chủ động kiểm tra để phòng ngừa các trường hợp tương tự"** | **Founder (operator)** **DỪNG** — đây là **anti-feature**, không phải một cải tiến | ⛔ **Cấm tường minh**: không backlog item / issue / PR mang tên kiểu `copyright detection`, `plagiarism check`, `flag nội dung khả nghi`, `similarity scan` — **trước khi** có xác nhận của luật sư. Lý do: điều kiện miễn trừ **(a)** là **"không biết"** ⇒ tự tạo ra tri thức đó **PHÁ** chính miễn trừ. **Điều kiện mở lại**: luật sư xác nhận ranh giới giữa *"đọc nhãn"* và *"suy đoán"* | [BRD-007](../BRD/BRD-007-Legal-And-Compliance.md) mục 5.2 · [R-04](../../010-Planning/Risk-Register.md) cột *Dấu hiệu sớm* |
| **EF-5** ⚠️ | **Nền tảng có thực sự được coi là *"doanh nghiệp cung cấp dịch vụ trung gian"* để hưởng miễn trừ Điều 198b hay không** — khi nó **không chỉ *lưu trữ* mà còn *xử lý/biến đổi*** nội dung của user | **Founder (operator)** vẫn thực hiện đầy đủ main flow — vì làm đủ mà chưa chắc được miễn trừ **rẻ hơn** không làm | ⚠️ **`TBD` — đây là câu `Q3` của gate `G0`**, và trạng thái hiện tại là **CHƯA ENGAGE luật sư** (`Charter` §9.1). findings §6.2 **`KT-6`**: NĐ 17 chỉ nói *"lưu trữ nội dung số theo yêu cầu"*; *"Hosting thuần có safe harbour rõ; **'hosting + processing' là vùng chưa test**"*. ⛔ UC này **không** tự phân xử câu này | `MVP-Scope` §7.1 câu **`Q3`** · `KT-6` · CF-7.8/7.9 · `Charter` §9.1 **`BLOCKER-01`** |

> [!IMPORTANT]
> **Ranh giới của `BLOCKER-01` — chống hiểu nhầm đắt nhất** (`CẤM-10`): `EF-5` **không** có nghĩa là *"phải chờ luật sư mới được làm gì"*. `G0` chặn **THƯƠNG MẠI HOÁ**, **không** chặn MVP0–MVP1. Quy tắc khi chưa engage luật sư (`Risk-Register` §3 `RB-01`): **được làm** MVP0 → MVP1 với dữ liệu của chính Founder và **xây đủ checklist 198b** · **không được làm**: mở cho **người ngoài** upload; thu **bất kỳ khoản tiền nào**.
>
> ⇒ Chính vì thế **checklist `GP-3` được xây TRƯỚC khi biết câu trả lời của `Q3`**. `Charter` §9.2 gọi việc đọc ngược lại là *"cách hiểu nhầm đắt nhất mà tài liệu này có thể gây ra"*.

---

## 6. Tài liệu liên quan

### 6.1 Traceability lên tầng trên

| Quan hệ | Tài liệu |
|---|---|
| **Part of (Epic)** | [Epic-Legal-And-Compliance](../../022-User-Stories/Epics/Epic-Legal-And-Compliance.md) |
| **Requirement cha** | [BRD-007 — Legal And Compliance](../BRD/BRD-007-Legal-And-Compliance.md) — hàng `GP-3`, **`BR-007-04`** (a) công cụ tiếp nhận · (b) đăng ký đầu mối Bộ VHTTDL · (c) **SLA 72 giờ** bằng soft-delete + disable-access cấp project. **Đường tách biệt**: `BR-007-08` (hard-delete tenant) |
| **Sản phẩm** | [PRD-Comic-Studio](../PRD-Comic-Studio.md) — mục *Pháp lý & compliance* |
| **Hệ thống** | [SRS-Comic-Studio](../SRS-Comic-Studio.md) |

### 6.2 BRD phụ thuộc chéo

| BRD | Vì sao liên quan |
|---|---|
| [BRD-008 — Quality And Operations](../BRD/BRD-008-Quality-And-Operations.md) | `H5` **abuse controls** — `Roadmap` §4 việc `X-b` lưu ý: *"abuse control cho upload thì cần **ngay ở MVP1**"*. Trông như tiền đề của safe harbour nhưng là hàng nhóm **H**, không phải nhóm **G** |
| [BRD-005 — Multi-Tenancy And Platform](../BRD/BRD-005-Multi-Tenancy-And-Platform.md) | `KC-5` `tenant_id` + RLS + storage tách tenant — điều kiện để *"disable-access ở **cấp project**"* là một hành động có phạm vi xác định. Cũng là nơi `ON DELETE CASCADE` của `BR-007-08` sống |
| [BRD-004 — Minimum Editor](../BRD/BRD-004-Minimum-Editor.md) | Nơi `change_log` **được sinh ra** (bước 7). BRD-007 sở hữu **nghĩa vụ**, BRD-004 sở hữu **hành động sinh dữ liệu** |

### 6.3 Use Case liền kề

| UC | Quan hệ |
|---|---|
| [UC-01 — Upload And Ingest Chapter](./UC-01-Upload-And-Ingest-Chapter.md) | Nơi **trigger của UC này ra đời**: *"lần đầu mở cho NGƯỜI NGOÀI upload"*. Cũng là nơi `BR-007-03` (opt-out Điều 37b) và checkbox **user warrant** (`BR-007-07`) sống |
| [UC-09 — Export Chapter](./UC-09-Export-Chapter.md) | Trạng thái `disable-access` do UC này tạo ra là nguyên nhân của `EF-3` bên UC-09 |

### 6.4 Ba câu hỏi `TBD` phải mang tới luật sư SHTT

> ⛔ **UC này KHÔNG trả lời chúng.** `Roadmap` §3.1 việc 1: *"Việc của pre-cycle là **gửi đi và nhận về bằng văn bản** — không phải tự trả lời."*

| # | Câu hỏi | Xuất hiện ở đâu trong UC này | Nguồn |
|---|---|---|---|
| **1** | **Câu `Q3` của gate `G0`** — nền tảng có được coi là *"doanh nghiệp cung cấp dịch vụ trung gian"* để hưởng miễn trừ Điều 198b không, khi nó **không chỉ lưu trữ mà còn xử lý/biến đổi** nội dung của user? | [`EF-5`](#5-exception-flow) | `MVP-Scope` §7.1 `Q3` · findings §6.2 `KT-6` |
| **2** | **Thủ tục counter-notice**: các trường bắt buộc · thời hạn phản đối · điều kiện và thủ tục phục hồi truy cập · trách nhiệm nếu phục hồi sai | [`AF-1`](#4-alternative-flow) | **KHÔNG CÓ CĂN CỨ TRONG REPO** — repo chỉ nói dữ liệu **được giữ** cho counter-notice (`BR-007-04` c) |
| **3** | **Danh sách trường bắt buộc của một yêu cầu takedown hợp lệ**, và **`SLA 72 giờ` có tạm dừng khi chờ bổ sung thông tin hay không** | [`EF-1`](#5-exception-flow) | findings §6.2 **`KT-5`** — nguyên văn NĐ 17/2023 và NĐ 134/2026 **chưa đọc được**: cov.gov.vn chỉ có bản giới thiệu; thuvienphapluat + nhansu **403**; IAPP **paywall** |

### 6.5 Tài liệu tham khảo

| Tài liệu | Phần được dùng ở đây |
|---|---|
| [MVP-Scope.md](../../010-Planning/MVP-Scope.md) | §3 nhóm G hàng **`GP-3`** (và `GP-5` để phân biệt) · §6 `KC-2`, `KC-4`, `KC-5` · **§7.1 gate `G0`** câu `Q3` |
| [Roadmap.md](../../010-Planning/Roadmap.md) | **§4 việc `X-a`** (trigger: *trước lần đầu mở cho NGƯỜI NGOÀI upload*; *"không thể 'làm sau' mà vẫn hợp lệ"*) và lưu ý `X-b` về abuse control ở MVP1 · §2 exit criterion **`M2-6`** · **§6.1** (`G0` chặn thương mại hoá, **không** chặn MVP0/MVP1) · §6.2 (phụ thuộc **CỨNG**: `X-a` → mở cho người ngoài upload) |
| [Charter-Comic-Studio.md](../../010-Planning/Charter-Comic-Studio.md) | §7 `C1` (đội **1 người** ⇒ chọn *form + email `copyright@`* thay vì hệ thống ticket; bus factor = 1) · §9.1 **`BLOCKER-01`** + trạng thái **CHƯA ENGAGE luật sư** · §9.2 ranh giới · §9.3 **`BLOCKER-02`** |
| [Risk-Register.md](../../010-Planning/Risk-Register.md) | **`R-02`** (safe harbour chưa đủ điều kiện — Score 6, owner `security-auditor`) · **`R-04`** (nghịch lý safe harbour) · §3 **`RB-01`** (rủi ro nhị phân, **cố ý KHÔNG có Score**) |
| [Glossary.md](../../999-Resources/Glossary.md) | *rủi ro nhị phân* · *Go/No-Go gate* · *disclosure-first positioning* · *`field_provenance` / `change_log`* |
| [findings/business-analyst.md](../../010-Planning/pm-runs/2026-08-24-khoi-tao-requirements-stories-comic-studio/findings/business-analyst.md) | **§3.1** nguyên tắc 4 (*"nghĩa vụ pháp lý có actor NGOÀI hệ thống thì phải có UC riêng"*) · **§3.2** hàng `UC-11` · §5.2 CF-7.6, CF-7.8/7.9, CF-8.11a, CF-10.2 · §5.3 `CẤM-10`, `CẤM-13`, `CẤM-14`, `CẤM-18` · §6.2 `KT-5`, `KT-6` |
| [Documents-Template.md](../../../knowledge-base/99-Templates/Documents-Template.md) | `RULE-001` — thư mục `docs/020-Requirements/Use-Cases/`, naming `UC-{NN}-{Title}.md`, frontmatter, **standard markdown link** (quy tắc #5) |

> ⛔ **`CẤM-18`**: không sửa [`Analysis-Comic-Studio-Concept.md`](../../050-Research/Analysis-Comic-Studio-Concept.md) — nó là **dấu vết quyết định tại thời điểm viết**. Tài liệu này **link sang**, không sửa. Nội dung của **ba văn bản riêng biệt** — **Điều 198b** (thuộc `Luật số 07/2022/QH15`), **`NĐ 17/2023/NĐ-CP`**, và **`NĐ 134/2026/NĐ-CP`** (Điều 5a/37a/37b) — được dẫn **QUA repo**, ⛔ **không tra lại nguồn ngoài** (`CẤM-15`). ⚠️ **Điều 198b KHÔNG thuộc NĐ 134** — bản trước viết ba tham chiếu này dạng gạch chéo `198b / NĐ 17 / NĐ 134`, dễ đọc nhầm thành một; verify L23 nêu và đã tách rõ.
>
> ⛔ **Không link tới `docs/030-Specs/`** — tầng technical spec chưa tồn tại và nằm ngoài scope của run này.

---

_Use Case by Comic Studio — role `business-analyst`._
_Author: trisjr_
</content>
