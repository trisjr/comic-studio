---
id: SPEC-INT-TAKEDOWN-INTAKE
type: spec
status: draft
project: comic-studio
created: 2026-08-29
---

# Spec Integration: Takedown Intake

Serves: [Story-Safe-Harbour-Checklist-Article-198b](../../022-User-Stories/Backlog/Story-Safe-Harbour-Checklist-Article-198b.md) · [UC-11](../../020-Requirements/Use-Cases/UC-11-Handle-Takedown-Request.md)
Decided in: [ADR-006 `D6`](../Architecture/ADR-006-RLS-Tenant-Context-Injection.md) · [ADR-010 `D7`](../Architecture/ADR-010-Tenant-Isolation-With-RLS.md) · [ADR-005](../Architecture/ADR-005-Platform-Table-Schema-Placement.md)

> [!CAUTION]
> ⭐⛔ **Ba điều phải nắm trước khi đọc tiếp:**
> 1. Bề mặt này **KHÔNG auth, KHÔNG tenant context** ⇒ ⛔ **RLS không áp được ở đó.** Đây là **ngoại lệ DUY NHẤT** của mô hình RLS trong toàn hệ thống — và nó ⛔ **không phải lỗ hổng**, nó là **hình dạng bắt buộc của một nghĩa vụ pháp lý**.
> 2. ⭐ **Timestamp tiếp nhận do HỆ THỐNG ghi** là **mốc đếm SLA 72 giờ** — tức là **bằng chứng**.
> 3. ⚠️ `T-29` (thông báo cho tenant bị takedown) ⛔ **KHÔNG được đóng ở file này** — xem [§3](#3-cái-gì-còn-mở).

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

File này đặc tả **bề mặt tiếp nhận yêu cầu hạ nội dung từ chủ sở hữu quyền** — một actor **NGOÀI hệ thống**, ⛔ không có tài khoản, ⛔ không thuộc tenant nào.

⚠️ **Integration này nửa kỹ thuật, nửa thủ tục.** Phần *"đăng ký đầu mối với Bộ VHTTDL"* là **hành động hành chính offline**, ⛔ **không phải integration code** — nhưng nó nằm trong cùng một nghĩa vụ và ⛔ không được tách rời khỏi bản mô tả này (xem [§2.4](#24-đăng-ký-đầu-mối-với-bộ-vhttdl--hành-động-hành-chính-offline)).

⚠️ **Phạm vi**: STRIDE chi tiết của bề mặt này thuộc [Spec-Security-Threat-Model §3.7](../Security/Spec-Security-Threat-Model.md); nghĩa vụ pháp lý và bằng chứng thuộc [Spec-Security-Legal-Compliance §6](../Security/Spec-Security-Legal-Compliance.md); hình dạng bảng thuộc [`DB-Entity-Compliance-And-Takedown.md`](../Schema/DB-Entity-Compliance-And-Takedown.md). ⛔ **File này ⛔ không lặp lại chúng** — nó ghi **bề mặt tích hợp** và **hành vi khi hỏng**.

---

## 2. Cái gì đã CHỐT

### 2.1 Bề mặt không auth, không tenant context

`public.takedown_request` là bề mặt **CÔNG KHAI, ⛔ không cần tài khoản** (`SRS-FR-38`, `D-54`) ⇒ ở thời điểm `INSERT` ⛔ **không có tenant nào để bơm vào context** ⇒ ⛔ **không viết được vị từ `tenant_id = current_tenant_id()`**.

**Cách xử lý đã chốt** ([ADR-006 `D6`](../Architecture/ADR-006-RLS-Tenant-Context-Injection.md)) — ⛔ file này ⛔ không phát minh thêm:

| # | Điều |
|:--:|---|
| 1 | Đường này chạy dưới role riêng **`app_public_intake`**, quyền **CHỈ `INSERT`** vào `public.takedown_request` |
| 2 | ⛔ **KHÔNG** giải bằng `BYPASSRLS`; ⛔ **KHÔNG** cho role này `SELECT` **bất kỳ bảng nghiệp vụ nào** |
| 3 | RLS vẫn **bật + `FORCE`** trên bảng; đúng **một** policy `FOR INSERT TO app_public_intake WITH CHECK (true)`, ⛔ **không** policy `SELECT` ⇒ mặc định là **fail-closed, 0 dòng** cho mọi session |
| 4 | Người gửi ⛔ **không** đọc lại được yêu cầu của mình qua database — xác nhận tiếp nhận là **ID + timestamp trả ở tầng ứng dụng** |
| 5 | ⭐ **Quy tắc chung rút ra**: cơ chế bơm context ⛔ **không được giả định mọi session DB đều có tenant** |

⚠️ **`public.takedown_request` ⛔ KHÔNG có cột `tenant_id`** — ngoại lệ đã được lường trước. Lý do đầy đủ (đặc biệt: `ON DELETE CASCADE` sẽ **xoá mất hồ sơ SLA của chính nền tảng**) nằm ở [`DB-Entity-Compliance-And-Takedown.md`](../Schema/DB-Entity-Compliance-And-Takedown.md) — ⛔ file này ⛔ không lặp lại.

### 2.2 Hai kênh tiếp nhận — một đường ghi

**Form web** + **email `copyright@`** (`SRS-FR-38`) ⇒ cột `channel` với `CHECK (channel IN ('web_form','email'))`.
⭐ **Hai kênh, nhưng ⛔ chỉ MỘT đường ghi** — xem [§4.1](#41-hai-kênh-một-đường-ghi).

### 2.3 Timestamp tiếp nhận là BẰNG CHỨNG

> **`INV-TR-1`** — `received_at` **do hệ thống ghi**, ⛔ **không nhận từ client**. Cưỡng chế: `DEFAULT now()` + role `app_public_intake` ⛔ **không được** cấp quyền ghi cột này.

⭐ **Lý do**: đây là **mốc đếm SLA 72 giờ** (`SRS-FR-38` chốt **72 giờ** `[OFF]` — nhãn nguồn giữ nguyên, ⛔ không rửa sạch). *"Nhận giá trị từ bên ngoài là để người khác đặt lại đồng hồ nghĩa vụ của mình."*
**Phép đo SLA**: `project_access_state.disabled_at − takedown_request.received_at ≤ 72h`. Hai cột có mặt đầy đủ ⇒ nghĩa vụ **đo được**.
⚠️ **72 giờ là PHÉP ĐO, ⛔ không phải constraint** — một `CHECK` chỉ chạy khi có dòng được ghi, mà trường hợp nguy hiểm nhất (*"quá 72 giờ mà ⛔ chưa ai làm gì"*) là trường hợp ⛔ **không có dòng nào để `CHECK`**. Xem `TD-E8` ở [§5](#5-retry--error-taxonomy).

### 2.4 Đăng ký đầu mối với Bộ VHTTDL — hành động hành chính offline

| Hạng mục | Nội dung |
|---|---|
| **Nội dung nghĩa vụ** | Đăng ký **đầu mối (email + số điện thoại)** với **Bộ VHTTDL** |
| ⛔ **Bằng chứng trong hệ thống** | ⛔⛔ **KHÔNG CÓ ARTIFACT NÀO.** Bằng chứng là **giấy tờ đăng ký ngoài hệ thống** |
| ⚠️ **Hệ quả** | ⭐ **Security Review Gate ⛔ KHÔNG kiểm được hàng này từ codebase** — phải kiểm bằng **checklist vận hành** |
| **Ai đóng · khi nào** | **Founder/PM** · **trước khi mở cho người ngoài upload** (`BLOCKER-02`) |

⇒ ⛔ **Đừng đi tìm một endpoint hay một bảng cho hàng này.** Ghi ra tường minh để một lô sau ⛔ không tưởng nó đã được code phủ.

### 2.5 Xử lý = soft-delete + disable-access, ⛔ KHÔNG hard delete

| Mã | Ràng buộc |
|:--:|---|
| `INV-TR-3` | ⛔ **KHÔNG hard-delete** khi xử lý takedown. Cơ chế **duy nhất** là đổi `access_state`. **Dữ liệu PHẢI GIỮ cho counter-notice** (`D-54`) |
| — | ⭐ **Hai đường xoá TÁCH BIỆT, ⛔ không gộp**: takedown (`L-4`) ≠ hard-delete tenant (`L-7`, `D-14`). Bảng đối chiếu đầy đủ ở [ADR-010 `D7`](../Architecture/ADR-010-Tenant-Isolation-With-RLS.md) — ⛔ file này ⛔ không lặp lại |
| `INV-PAS-3` | Một project ⇒ **đúng một** dòng `public.project_access_state` (`PK (project_id)`) ⇒ **N đơn trùng lặp → MỘT** trạng thái, ⛔ không chồng chéo |
| `INV-PAS-4` | ⭐ **Mọi đường đọc và export kiểm `access_state`** — điểm cưỡng chế là `SDD-HG-01.4` qua **đúng một** hàm dùng chung; ⛔ không `force`, ⛔ không `skip_gates`, ⛔ không `admin_override` |
| `CO-2` | ⛔ **Không đường code nào được suy ra trạng thái takedown từ `story.project.deleted_at`.** Hai cột đọc **độc lập** |

### 2.6 ⛔ `SRS-NFR-15` — cấm tuyệt đối của luồng này

⛔ **Không quét · ⛔ không flag · ⛔ không chấm điểm *"nghi vấn bản quyền"* ở luồng takedown**, và ⛔ **không gọi bất kỳ dịch vụ copyright / plagiarism / similarity detection nào** để *"thẩm định"* một đơn.

⭐ **Lý do — và vì sao đây là chỗ phản xạ nghề nghiệp làm ngược**: điều kiện **(a)** của miễn trừ theo **Điều 198b** là ***"không biết"***. Xây (hoặc mua) một bộ phát hiện **tạo ra đúng cái tri thức mà luật đang miễn trừ cho việc KHÔNG CÓ** ⇒ **tự phá miễn trừ của chính mình**. Lập luận đầy đủ: [Spec-Security-Legal-Compliance §5](../Security/Spec-Security-Legal-Compliance.md) — ⛔ file này ⛔ không lặp lại.

⚠️ **Ranh giới ĐƯỢC PHÉP, ⛔ không được đọc nới ra**:

| Việc | Cho phép? |
|---|:--:|
| **Tiếp nhận và xử lý thông báo từ chủ quyền** (chính là bề mặt này) | ✅ **ĐƯỢC** — tri thức đến **từ bên ngoài**, và **xử lý trong 72h** chính là điều kiện (c) của miễn trừ |
| Đọc **opt-out signal do chính chủ quyền gắn vào file** (ở ingest, ⛔ không ở đây) | ✅ **ĐƯỢC** |
| Hệ thống **tự suy đoán** một nội dung *"có thể"* thuộc về ai đó | ⛔ **KHÔNG** |
| Rate limit, validate định dạng, abuse control | ✅ **ĐƯỢC** — ⛔ lệnh cấm ⛔ không áp cho những thứ này |

### 2.7 Người đánh giá, ⛔ không tự động

⭐ **Bước quyết định hạ nội dung là một NGƯỜI đánh giá** (founder ở vai operator), ⛔ **không phải tự động hạ theo đơn**. Đây là biện pháp đã có cho `TM-F7-1` (*"takedown giả mạo làm vũ khí DoS"*) — [Spec-Security-Threat-Model §3.7](../Security/Spec-Security-Threat-Model.md).

### 2.8 Abuse control — cơ chế CHỐT, ngưỡng MỞ, kèm một ràng buộc ngược chiều

`SRS-NFR-20` chốt **cơ chế** rate limit. ⚠️ **Nhưng ở riêng bề mặt này có một ràng buộc ngược chiều với mọi bề mặt khác**:

> ⭐⛔ **Ngưỡng ⛔ KHÔNG được chặt tới mức làm MẤT một đơn hợp lệ.** Mất một đơn là **mất chính điều kiện miễn trừ** — thiệt hại lớn hơn nhiều lần so với việc chịu một ít spam.

⇒ Ở mọi bề mặt khác, nghi ngờ thì **siết**. Ở bề mặt này, nghi ngờ thì **nới, và bù bằng đường phân loại của operator**. Ngưỡng cụ thể là `T-10` ([§3](#3-cái-gì-còn-mở)).

### 2.9 Hai ràng buộc xuyên suốt áp cho bề mặt này

| Mã | Nội dung |
|:--:|---|
| `C-4` | ⛔ **Dữ liệu cá nhân của người nộp đơn** (email, số điện thoại) ⛔ không được lọt vào log — cùng danh sách che với signed URL và token ([Spec-Security-Threat-Model §4.2](../Security/Spec-Security-Threat-Model.md)) |
| `C-3` | **Kiểm disable-access ở MỌI đường đọc — qua đúng một hàm**; ⚠️ danh sách *"mọi đường đọc"* phải được **đóng ở lô API** |

---

## 3. Cái gì còn MỞ

> ⛔ **Mục này ⛔ không đóng hàng nào.**

| # | `TBD` | Nội dung | Ai đóng | Khi nào |
|:--:|---|---|---|---|
| 1 | ⭐ **`T-29`** | **Nội dung / hình thức / thời hạn thông báo cho tenant bị takedown.** ⚠️ Chính bước đó là **điều kiện tối thiểu để counter-notice tồn tại** ⇒ ⛔ chưa có nó thì counter-notice ⛔ **chưa có đường tồn tại**. ⛔⛔ **File này ⛔ KHÔNG đóng, và ⛔ không gợi ý nội dung** — kể cả một gợi ý cũng là đóng nó. ⭐ Lý do: hàng này **chạm trực tiếp điều kiện miễn trừ Điều 198b** ⇒ là **quyết định pháp lý**, ⛔ không phải quyết định bảo mật hay kiến trúc (`security-auditor` đã **từ chối nhận việc** và PM **chấp nhận** lời từ chối) | **Founder + luật sư**, **PM điều phối** — theo PM run-state `E22` | ⛔ **Chưa có mốc**; chặn tính đầy đủ của luồng counter-notice |
| 2 | **`T-24`** (`b-4`) | **Bảo vệ dữ liệu cá nhân / quyền riêng tư của người nộp đơn.** ⚠️ `SRS-FR-38` **bắt buộc thu email + số điện thoại** của người **NGOÀI hệ thống** — ⛔ không tài khoản, ⛔ không tenant, ⛔ không nằm trong mô hình `KC-5`. ⚠️ Và dòng `takedown_request` **sống lâu hơn** tenant liên quan | **Luật sư** | Cùng gói `SRS-NFR-17` |
| 3 | — | ⭐ **Danh sách trường BẮT BUỘC của một đơn HỢP LỆ.** ⛔ Chưa xác định (nguyên văn văn bản pháp luật chưa đọc được) ⇒ ⛔ **không đặt `NOT NULL`**: đặt bây giờ là **bịa một nghĩa vụ pháp lý và biến nó thành ràng buộc DB** — một đơn thật, hợp lệ theo luật, có thể **bị DB từ chối** và **đồng hồ SLA ⛔ không bao giờ bắt đầu** | **Luật sư SHTT → PM** | Trước `BLOCKER-02` |
| 4 | **`T-10`** | **Ngưỡng rate limit** cho bề mặt công khai. ⚠️ Ràng buộc đã chốt lên con số tương lai: ⛔ **không được** làm mất một đơn hợp lệ ([§2.8](#28-abuse-control--cơ-chế-chốt-ngưỡng-mở-kèm-một-ràng-buộc-ngược-chiều)) | **PM + Architect** | Sau khi đo tải |
| 5 | **`T-23`** (`b-3`) | **Chính sách lưu giữ / xoá** cho nhóm dữ liệu này. ⚠️ Căng thẳng có thật: giữ lâu = giữ dữ liệu cá nhân của người ngoài; xoá sớm = **xoá bằng chứng** | **PM + Luật sư** | Cùng gói `SRS-NFR-17` |
| 6 | — | ⭐ **Ai được `SELECT`/`UPDATE` `public.takedown_request` để OPERATOR xử lý** (`received → needs_more_info / rejected / actioned`). ⛔ **Không nguồn nào pin.** Hai đường khả dĩ: (a) một role thứ **năm** `app_operator` — ⚠️ **sửa `SDD` §7.4**, ⛔ ngoài quyền sở hữu lô này; (b) đi qua đường **owner/vận hành** đã tồn tại. ⛔ **File này ⛔ không tự phát minh role** | **`Spec-Security-*` + `ADR-006`/`SDD` §7.4** | Trước khi công cụ takedown **chạy thật** (`BLOCKER-02`) |
| 7 | — | ⚠️ **Cơ chế biến một email `copyright@` thành một dòng DB.** ⛔ Chưa nguồn nào chốt (đọc thư tự động? operator chép tay?). ⭐ **Invariant giữ nguyên bất kể cơ chế nào**: `received_at` **do hệ thống ghi TẠI THỜI ĐIỂM TIẾP NHẬN** (`INV-TR-1`), `channel = 'email'`. ⚠️ **Rủi ro phải nói ra**: nếu operator chép tay muộn, mốc SLA bị **dời về sau thời điểm thật** ⇒ hồ sơ nói ta nhận muộn hơn thực tế. **Hệ quả pháp lý của độ lệch đó là câu hỏi luật sư**, ⛔ file này ⛔ không kết luận | **Architect + Founder** (cơ chế) · **luật sư** (hệ quả pháp lý) | Trước `BLOCKER-02` |
| 8 | `R-02` | **Cơ chế đếm ngược / cảnh báo SLA** (chống trường hợp *"quá 72h mà ⛔ chưa ai làm gì"*) — thuộc **tầng vận hành**, dựa trên index SLA đã có | **Lô API + vận hành** | Điều kiện của `BLOCKER-02` |
| 9 | — | **Thủ tục counter-notice và điều kiện khôi phục.** ⛔ Repo **CHỈ** nói *"dữ liệu được giữ cho counter-notice"*, ⛔ **không định nghĩa THỦ TỤC** ⇒ ⛔ **không tạo bảng `counter_notice`** (thiết kế bảng cho một thủ tục chưa tồn tại là **bịa nghĩa vụ pháp lý**) | **Luật sư SHTT → PM** | Trước thương mại hoá |

⚠️ **Hình dạng endpoint công khai** (đường dẫn, payload, mã trả về) thuộc `Endpoint-Takedown-Public.md` của **lô API** — ⛔ file này ⛔ không đặc tả, chỉ ràng buộc **hành vi** ở [§4](#4-interface--seam) và [§5](#5-retry--error-taxonomy).

---

## 4. Interface / seam

### 4.1 Hai kênh, một đường ghi

| Kênh | `channel` | Đường vào |
|---|---|---|
| Form web công khai | `'web_form'` | Endpoint công khai → role `app_public_intake` → `INSERT` |
| Email `copyright@` | `'email'` | ⚠️ Cơ chế chưa chốt (hàng #7 của [§3](#3-cái-gì-còn-mở)) → **cùng một** đường `INSERT` |

> ⭐⛔ **Ràng buộc cứng**: kênh email ⛔ **KHÔNG được có một đường ghi thứ hai** bỏ qua quy tắc `received_at` hay bỏ qua role `app_public_intake`. **Hai kênh, một đường ghi, một quy tắc timestamp** — nếu không, ta có **hai loại bằng chứng SLA với hai độ tin cậy khác nhau**.

### 4.2 Tính chất của đường ghi — ba điều ⛔ không được nới

1. **Chỉ `INSERT`** vào `public.takedown_request`.
2. ⛔ **Không `SELECT`** bất kỳ bảng nghiệp vụ nào — kể cả *"để tra xem project có tồn tại không"*.
3. ⛔ **Không `BYPASSRLS`** dưới bất kỳ lý do nào.

⚠️ Ba điều này là **một trong ba bề mặt đặc quyền cố định** phải review như code bảo mật (`C-11`, [Spec-Security-Threat-Model §4.2](../Security/Spec-Security-Threat-Model.md)).

### 4.3 Đầu ra cho người gửi

- **Xác nhận tiếp nhận = `id` + `received_at`**, trả ở **tầng ứng dụng**.
- ⛔ **Không trả bất kỳ thông tin nội bộ nào**: ⛔ không xác nhận project/nội dung có tồn tại hay không, ⛔ không trả trạng thái xử lý, ⛔ không trả tên tenant. Bề mặt này ⛔ **không được trở thành một oracle** để dò sự tồn tại của tài nguyên (cùng tinh thần `C-5`).
- Người gửi **mô tả nội dung bị khiếu nại bằng lời của họ** — họ ⛔ không biết khoá nội bộ của ta; `project_id` do **operator** xác định sau khi đánh giá, ⛔ **không** do người gửi cung cấp.

### 4.4 Đường xử lý của operator

`received` → `needs_more_info` / `rejected` / `actioned`; khi `actioned` ⇒ ghi `public.project_access_state` (`access_state = 'disabled_by_takedown'`, `disabled_at`, `disabled_by_request_id`).
⚠️ **Quyền DB cho đường này ⛔ chưa được pin** — hàng #6 của [§3](#3-cái-gì-còn-mở). ⛔ File này ⛔ không tự cấp.

### 4.5 ⛔ Sáu anti-seam — ⛔ CẤM, kèm lý do

| ⛔ Cấm | Vì sao |
|---|---|
| ⛔ **Nhận `received_at` từ client** | `INV-TR-1`. Để người khác đặt lại đồng hồ nghĩa vụ của mình |
| ⛔ **Tự động hạ nội dung theo đơn** | Biến bề mặt công khai thành **vũ khí DoS** nhắm vào tenant bất kỳ (`TM-F7-1`) |
| ⛔ **Hard delete để "làm cho xong" takedown** | `INV-TR-3`. Phá mất **chính bằng chứng** counter-notice |
| ⛔ **Cấp `SELECT` cho `app_public_intake`** *"cho tiện tra cứu"* | `TM-F7-3`. Nới một bề mặt ⛔ không auth |
| ⛔ **Gọi dịch vụ similarity/copyright detection để thẩm định đơn** | `SRS-NFR-15` — [§2.6](#26--srs-nfr-15--cấm-tuyệt-đối-của-luồng-này) |
| ⛔ **Suy trạng thái takedown từ `story.project.deleted_at`** | `CO-2`. Hai khái niệm khác nhau, hai chủ thể khác nhau |

---

## 5. Retry & error taxonomy

> ⭐⛔ **Nguyên tắc trùm — và nó NGƯỢC với mọi integration khác trong repo này:**
> ở bề mặt này, ⭐ **mất một đơn hợp lệ = mất chính điều kiện miễn trừ**. ⇒ ⛔ **Không được fail im lặng**. Khi ⛔ không ghi được, hệ thống phải **báo lỗi cứng cho người gửi** và **chỉ sang kênh thứ hai** — ⛔ tuyệt đối không trả một xác nhận mà phía sau ⛔ không có dòng DB nào.

| Mã | Tình huống | Hành vi bắt buộc | ⛔ Cấm |
|:--:|---|---|---|
| `TD-E1` | **DB ⛔ không ghi được** (mất kết nối, lỗi quyền) | Trả **lỗi rõ ràng** + hướng người gửi sang kênh `copyright@`. Ghi sự cố ở mức báo động | ⛔⛔ **Không trả xác nhận tiếp nhận.** Một `id` + timestamp mà ⛔ không có dòng DB là **bằng chứng SLA GIẢ** — tệ hơn hẳn việc thừa nhận lỗi. ⛔ Cũng không *"nhận vào bộ nhớ rồi ghi sau"* |
| `TD-E2` | **Đơn thiếu trường** | ⭐ **Vẫn tiếp nhận**: ghi dòng, `status = 'needs_more_info'`, và ⭐ **đồng hồ SLA ĐÃ CHẠY**. Tính hợp lệ đánh giá ở **tầng nghiệp vụ** | ⛔ **Không từ chối ở tầng DB** (`INV-TR-2`) — danh sách trường bắt buộc là `TBD` (hàng #3 của [§3](#3-cái-gì-còn-mở)) |
| `TD-E3` | **Đơn trùng lặp** (một người nộp nhiều lần, hoặc nhiều người cùng một nội dung) | **Ghi N dòng — đó là đúng.** Chống chồng chéo **trạng thái** đã có ở tầng cấu trúc: `PK (project_id)` ⇒ **N đơn → MỘT** dòng `project_access_state` (`INV-PAS-3`) | ⛔ **Không dedup đơn** — mỗi đơn là một sự kiện pháp lý riêng có mốc thời gian riêng |
| `TD-E4` | **Vượt rate limit** | Trả mã từ chối **kèm chỉ dẫn sang kênh email**. ⚠️ Ngưỡng phải tuân [§2.8](#28-abuse-control--cơ-chế-chốt-ngưỡng-mở-kèm-một-ràng-buộc-ngược-chiều) | ⛔ **Không im lặng bỏ request.** ⛔ Không siết tới mức mất đơn hợp lệ |
| `TD-E5` | **Spam / flood** làm ngập bảng và **che đơn thật** | Cơ chế: rate limit (`T-10`) + **đường phân loại của operator** (`rejected`) | ⛔ **Không giải bằng cách để máy tự thẩm định giá trị pháp lý của đơn** — đó là `SRS-NFR-15` ở một hình dạng khác |
| `TD-E6` | Đơn nhắm vào project **đã bị hard-delete** trước đó | **Vẫn tiếp nhận bình thường**; `project_id` để `NULL`. Dòng đơn **tồn tại độc lập** với vòng đời project (`ON DELETE SET NULL`) | ⛔ Không coi là lỗi, ⛔ không từ chối |
| `TD-E7` | **Kênh email**: thư ⛔ không parse được / bounce | ⛔ **Không im lặng bỏ.** Phải có đường đưa nó thành một dòng với `channel = 'email'` và timestamp tiếp nhận. ⚠️ Cơ chế chưa chốt — hàng #7 của [§3](#3-cái-gì-còn-mở) | ⛔ Không để một thư hợp lệ biến mất trong hộp thư |
| `TD-E8` | ⭐ **Quá 72 giờ mà ⛔ chưa ai làm gì** | ⚠️ ⛔ **Không `CHECK` nào bắt được** — trường hợp này ⛔ **không có dòng nào để `CHECK`**. Cơ chế **đếm ngược/cảnh báo thuộc tầng vận hành** (`R-02`, hàng #8 của [§3](#3-cái-gì-còn-mở)) | ⛔ **File này ⛔ không kết luận hệ quả pháp lý của việc trễ SLA** — đó là câu hỏi luật sư |
| `TD-E9` | Operator **hạ nhầm** project | Truy vết đã có: `INV-PAS-2` bắt mọi disable-access **truy được về đúng một đơn**; `restored_at` có chỗ ghi khi khôi phục | ⚠️ **Thủ tục dẫn tới khôi phục = `TBD`** (hàng #9 của [§3](#3-cái-gì-còn-mở)). ⛔ Không tự định nghĩa |

⚠️ **Hai quy tắc bao trùm bảng trên:**
1. ⛔ **Không log dữ liệu cá nhân của người nộp đơn** (`C-4`).
2. ⛔ **Không có hàng nào retry tự động vào chỗ của con người**: bước đánh giá là **người**, ⛔ không phải một job có backoff.

---

## 6. Chi phí

> ⛔ **Không dán giá.** Và ⚠️ **chi phí của integration này ⛔ KHÔNG phải chi phí per-call** — đây là chỗ dễ đánh giá sai nhất.

| Loại | Nội dung |
|---|---|
| ⭐ **Chi phí vận hành người — trục chính** | **SLA 72 giờ** đòi một **người** đánh giá có mặt trong 72 giờ, **kể cả cuối tuần**. Với `SRS` §1.3 (**1 dev**), đây là **ràng buộc vận hành thật**, ⛔ không phải chi tiết. Nó ⛔ **không giảm được bằng code** — vì `2.7` cấm tự động hạ nội dung |
| **Chi phí hạ tầng** | Gần như không đáng kể: một endpoint công khai + một hộp thư. ⚠️ Nhưng bề mặt **công khai** kéo theo chi phí **rate limit + quan sát** (`T-10`) |
| **Chi phí hành chính** | Đăng ký đầu mối với **Bộ VHTTDL** ([§2.4](#24-đăng-ký-đầu-mối-với-bộ-vhttdl--hành-động-hành-chính-offline)) — chi phí **thủ tục**, ⛔ không phải chi phí kỹ thuật |
| ⭐ **Chi phí ẩn LỚN NHẤT — và nó là chi phí PHÁP LÝ** | Một đơn **bị mất** hoặc **xử lý trễ** ⇒ mất **điều kiện miễn trừ**. Đây là lý do toàn bộ [§5](#5-retry--error-taxonomy) ưu tiên *"⛔ không mất đơn"* **cao hơn** *"chặt tay với spam"* |
| ⛔ **Không thuộc COGS mỗi chapter** | Bề mặt này ⛔ **không** sinh `usage_event` và ⛔ **không** nằm trong chuỗi chi phí sinh ảnh |

---

## Tài liệu tham khảo

**Tầng 020 — Requirements**
- [SRS-Comic-Studio](../../020-Requirements/SRS-Comic-Studio.md) — `SRS-FR-38` (`D-54`) · `SRS-NFR-01` · `SRS-NFR-05` (`D-14`) · `SRS-NFR-15` · `SRS-NFR-17` · `SRS-NFR-20` · §5.2 hàng `b-3`, `b-4`
- [UC-11](../../020-Requirements/Use-Cases/UC-11-Handle-Takedown-Request.md) — `EF-1`, `EF-2`, `EF-3`, `AF-1`
- [UC-09](../../020-Requirements/Use-Cases/UC-09-Export-Chapter.md) — điểm cưỡng chế `access_state`

**Tầng 022 — User Stories**
- [Story-Safe-Harbour-Checklist-Article-198b](../../022-User-Stories/Backlog/Story-Safe-Harbour-Checklist-Article-198b.md)
- [Story-Minimum-Abuse-Controls](../../022-User-Stories/Backlog/Story-Minimum-Abuse-Controls.md)

**Tầng 030 — Architecture** *(chỉ đọc, ⛔ không sửa)*
- [ADR-006 `D6`](../Architecture/ADR-006-RLS-Tenant-Context-Injection.md) — role `app_public_intake`, bề mặt ⛔ không có tenant
- [ADR-010 `D7`](../Architecture/ADR-010-Tenant-Isolation-With-RLS.md) — hai đường xoá tách biệt
- [ADR-005](../Architecture/ADR-005-Platform-Table-Schema-Placement.md) — vị trí `public.takedown_request`
- [SDD-Comic-Studio](../Architecture/SDD-Comic-Studio.md) — §5.4 (`F7`), §6.3 (`SDD-HG-01.4`), §7.4 (bốn DB role)

**Tầng 030 — Schema**
- [`DB-Entity-Compliance-And-Takedown.md`](../Schema/DB-Entity-Compliance-And-Takedown.md) — ⭐ nguồn duy nhất của hình dạng bảng, `INV-TR-1`…`INV-TR-3`, `INV-PAS-1`…`INV-PAS-5`, `CO-2`

**Tầng 030 — Security** *(⛔ không lặp lại nội dung)*
- [Spec-Security-Legal-Compliance](../Security/Spec-Security-Legal-Compliance.md) — §5 (`SRS-NFR-15`), §6 (bề mặt takedown), §8 (`T-23`, `T-24`, `T-29`)
- [Spec-Security-Threat-Model](../Security/Spec-Security-Threat-Model.md) — §3.7 (`TM-F7-1`…`TM-F7-7`), §4.2 (`C-3`, `C-4`, `C-5`, `C-11`)
- [Spec-Security-Tenant-Isolation](../Security/Spec-Security-Tenant-Isolation.md)

**Tầng 010 — Planning**
- [PM run-state](../../010-Planning/pm-runs/2026-08-28-phase-2-architecture-design-comic-studio/escalations.md) — `E22` (chủ mới của `T-29`)
- [MVP-Scope](../../010-Planning/MVP-Scope.md) — `KC-6`
- ⚠️ `BLOCKER-02` (*"mở cho người ngoài upload"*) được định nghĩa ở [Spec-Security-Legal-Compliance §1.2](../Security/Spec-Security-Legal-Compliance.md), ⛔ **không** ở `MVP-Scope`

**Spec anh em** *(⛔ chưa tồn tại tại thời điểm viết — nêu bằng plain text, ⛔ cố ý không tạo link)*: `Endpoint-Takedown-Public.md` (hình dạng endpoint) của lô API.
