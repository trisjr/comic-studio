---
id: BRD-004
type: brd
status: draft
project: comic-studio
created: 2026-08-24
---

# BRD-004 — Editor tối thiểu (module D: Editor & UI)

> [!IMPORTANT]
> **Quy ước nhãn nguồn số liệu** (kế thừa nguyên vẹn — **số và nhãn là một cặp không tách rời**):
> `[OFF]` nguồn official/paper gốc · `[BCN]` báo cáo ngành có tên firm · `[TC]` nguồn thứ cấp · `[EM]` ước lượng hoặc phép nhân, **không phải số đo** · `[CHỐT]` quyết định của Founder tại gate.
>
> Tài liệu này **chỉ trích lại** số liệu từ tầng Planning. Không tự tra lại, không tự tính lại, và **không thực hiện phép tính nào** trên các con số `[EM]`.

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

> Cho người dùng thực hiện — và **ghi lại** — quyết định sáng tạo của con người ở mức tối thiểu đủ để (a) sản phẩm dùng được, (b) thoả Điều 5a NĐ 134/2026.

Hai vế của mục tiêu này **không thay thế được cho nhau**. Một editor dùng được mà không ghi vết thì sản phẩm hợp pháp không chứng minh được; một cơ chế ghi vết mà không có chỗ nào cho người dùng ra quyết định thì không có gì để ghi.

Nguyên tắc chi phối toàn module là **NT-2** của [MVP-Scope §2](../../010-Planning/MVP-Scope.md#2-nguyên-tắc-cắt-scope): *nghĩa vụ pháp lý đặt lên tầng **DỮ LIỆU**, không đặt lên tầng **UI***. Hệ quả trực tiếp: **UI được tự do chọn cái rẻ; dữ liệu provenance thì không được cắt một dòng nào.**

### 1.1 ⚠️ Cảnh báo mẫu số — đọc trước khi nhìn bất kỳ con số % nào trong tài liệu này

> [!WARNING]
> **CF-6.7 và CF-6.8 là HAI MẪU SỐ KHÁC NHAU. ⛔ CẤM TRỪ CF-6.8 CHO CF-6.7** (`CẤM-01`).
>
> | Con số | Giá trị | Mẫu số | Nhãn |
> |---|---|---|---|
> | **CF-6.7** — Editor tối thiểu | **~20–25%** | **SaaS** — *đã bao gồm* khối multi-tenancy, billing, auth, moderation | `[EM]` |
> | **CF-6.8** — §14 đầy đủ (canvas editor) | **50–60%** | **Công cụ cá nhân** — *không* gồm multi-tenancy, billing, auth, moderation | `[EM]` |
>
> Phép tính `50–60% − 20–25% = 25–40% tiết kiệm` là **SAI VỀ MẶT SỐ HỌC**, vì hai tử số đứng trên hai mẫu số khác nhau. Nó tạo ra một con số **vô nghĩa nhưng trông chính xác**.
>
> **Điều duy nhất được phép kết luận**, giữ nguyên định tính: *"vẫn tiết kiệm được khoảng một nửa effort của hạng mục đắt nhất"*. Phần tiết kiệm đó là **ngân sách** cho khối multi-tenancy **15–25%** `[EM]` (CF-6.9, [BRD-005](./BRD-005-Multi-Tenancy-And-Platform.md)) — không phải lãi (NT-4).
>
> **Cả hai con số đều là `[EM]`** — ước lượng của lens kiến trúc, **không phải số đo**. Đừng lập kế hoạch như thể chúng là dữ liệu.
>
> **Chênh lệch có nguồn (CF-10.3)**: cộng năm thành phần ở [mục 2.1](#21-năm-thành-phần-bắt-buộc-của-d1) ra **20–30%**, không phải 20–25% — chênh lệch này **có từ nguồn** (`Analysis-Comic-Studio-Concept` §6.1 đưa cả năm khoảng **và** tổng *"~20–25%"*, hai thứ không khớp ở biên trên). Con số chuẩn để trích là **~20–25%** của CF-6.7; **đọc biên trên 25% như một ước lượng lạc quan**; cần con số thận trọng khi lập ngân sách thời gian ⇒ dùng **30%**.
>
> ⛔ Không tài liệu con nào của BRD-004 được phép **cộng, trừ, nhân, chia** các con số trên (`CẤM-15`).

---

## 2. Phạm vi module

Bảng dưới là **các hàng của nhóm `D. Editor & UI`** trong [MVP-Scope §3](../../010-Planning/MVP-Scope.md#3-bảng-mvp-vs-full-scope) mà BRD-004 **bao**. Nhãn từng mốc copy nguyên bảng gốc.

**Ký hiệu**: ✅ có đầy đủ · 🟡 có một phần / bản tối thiểu · ⛔ hoãn sang mốc sau · ❌ **cắt hẳn, không có trong Full Scope**

| # | Hạng mục | MVP0 | MVP1 | MVP2 | MVP3 | MVP4 | Full Scope | Căn cứ |
|---|---|:--:|:--:|:--:|:--:|:--:|:--:|---|
| **D1** | Editor tối thiểu — 5 thành phần (chi tiết [mục 2.1](#21-năm-thành-phần-bắt-buộc-của-d1)) | ❌ | 🟡 #5 Story Bible editor | 🟡 +#3 template layout, +#4 preview server-side, **bắt đầu** #2 bubble/text | ✅ đủ 5 (hoàn tất #2, thêm #1 panel card) | ✅ | ✅ | CF-6.7 **~20–25%** `[EM]`, **mẫu số SaaS** |
| **D7** | Expression sheet đầy đủ mỗi nhân vật | ❌ | ⛔ | ⛔ | 🟡 3 góc + 3 biểu cảm | 🟡 | ✅ | Analysis §6.3 — ứng viên cắt sâu cùng loại |

> Năm hàng còn lại của nhóm D (**D2, D3, D4, D5, D6**) nằm ở [mục 5](#5-cái-module-này-không-làm). Mỗi hàng của nhóm D xuất hiện **đúng một lần** trong tài liệu này.

### 2.1 Năm thành phần BẮT BUỘC của D1

Nguồn: [MVP-Scope §5.2](../../010-Planning/MVP-Scope.md#52-năm-thành-phần-bắt-buộc-2025--em-mẫu-số-saas). Cột `% effort` là **`[EM]`, mẫu số SaaS** — xem [cảnh báo mẫu số](#11--cảnh-báo-mẫu-số--đọc-trước-khi-nhìn-bất-kỳ-con-số--nào-trong-tài-liệu-này).

| # | Thành phần | Vì sao bắt buộc | % effort (mẫu số SaaS) `[EM]` | Mốc |
|---|---|---|---|---|
| **1** | **Panel card**: form spec + ảnh preview + `Regenerate` + **variant picker** | Chính là vòng lặp *iterative*. Variant picker là hành động sáng tạo **rẻ nhất mà giá trị pháp lý cao nhất** — chọn = authorship, ghi được vào `change_log` | **5–7%** | MVP3 |
| **2** | **Bubble/text overlay editor trong phạm vi MỘT panel** (kéo bubble, sửa thoại, chọn kiểu, kéo đuôi trỏ) | Ba lý do **độc lập**: (a) thoại do người viết là phần **được bảo hộ**; (b) bubble che mặt là lỗi không thể tự động tránh; (c) không sửa được thoại thì mọi lần sửa chữ thành một lần regenerate ảnh — **đốt tiền**. Đây là *"canvas bị giới hạn trong một khung"*, **không** phải scene graph tự do | **5–8%** | MVP2–MVP3 |
| **3** | **Page**: chọn **template layout**, đổi chỗ / swap panel giữa các ô, reorder | Sắp đặt panel là quyết định sáng tạo của con người (*selection & arrangement*). Chỉ cần **rời rạc**, không cần hình học liên tục | **3–4%** | MVP2 |
| **4** | **Preview trang + chapter render server-side** (composite PNG/PDF), read-only | Khách phải **thấy thành phẩm mới trả tiền**. Rẻ vì tái dùng compositor của export (H4, thuộc BRD-008) | **3–5%** | MVP2 |
| **5** | **Story Bible editor** (form: character, costume, location, state theo event) | Đây mới là nơi moat **lộ ra với khách hàng**. Vẫn là form + list | **4–6%** | MVP1 |
| — | **Tổng editor tối thiểu** | | **~20–25%** `[EM]` | |

> **Ràng buộc thiết kế xuyên suốt cả 5 thành phần** (nguồn: [MVP-Scope §5.2](../../010-Planning/MVP-Scope.md#52-năm-thành-phần-bắt-buộc-2025--em-mẫu-số-saas) callout): **mọi hành động của người dùng trong editor phải sinh một `change_log` row — kể cả hành động chỉ là "chọn ảnh này thay vì ảnh kia"**. Đây là điều kiện làm cho việc cắt canvas ([MVP-Scope §4.1](../../010-Planning/MVP-Scope.md#41-canvas-editor-14--cắt-một-phần-cf-91)) **hợp pháp**. Không có nó thì việc cắt canvas trở thành **cắt luôn lá chắn pháp lý** ⇒ đã nâng thành `BR-004-06`.

---

## 3. Yêu cầu nghiệp vụ

| ID | Phát biểu | Căn cứ (file + mục) | Mốc MVP |
|---|---|---|---|
| **BR-004-01** | Người dùng phải **sửa được Story Bible bằng form** — character, costume, location, state theo event. Không cần canvas, không cần graph editor; là form + list | `MVP-Scope` [§5.2](../../010-Planning/MVP-Scope.md#52-năm-thành-phần-bắt-buộc-2025--em-mẫu-số-saas) thành phần **#5** (**4–6%** `[EM]`) · §3 hàng **D1** | **MVP1** |
| **BR-004-02** | Người dùng phải **chọn được template layout trang**, đổi chỗ / swap panel giữa các ô, và reorder. Sắp đặt chỉ cần **rời rạc** — **không** cần hình học liên tục | `MVP-Scope` §5.2 thành phần **#3** (**3–4%** `[EM]`) · §3 **D1** (`🟡` ở MVP2) | **MVP2** |
| **BR-004-03** | Người dùng phải **xem được preview trang và chapter dưới dạng composite render server-side** (PNG/PDF), **read-only**. Lý do nghiệp vụ: khách phải **thấy thành phẩm mới trả tiền** | `MVP-Scope` §5.2 thành phần **#4** (**3–5%** `[EM]`, tái dùng compositor của H4) · §3 **D1** | **MVP2** |
| **BR-004-04** | Người dùng phải **kéo bubble, sửa thoại, chọn kiểu bubble và kéo đuôi trỏ trong phạm vi MỘT panel**. Ba lý do độc lập: (a) thoại do người viết là phần **được bảo hộ**; (b) bubble che mặt là lỗi không tự động tránh được; (c) không sửa được thoại thì mỗi lần sửa chữ thành một lần regenerate ảnh — **đốt tiền** | `MVP-Scope` §5.2 thành phần **#2** (**5–8%** `[EM]`, *"canvas bị giới hạn trong một khung"*) · §3 **A2** (typeset layer, thuộc BRD-001) | **MVP2** bắt đầu → **MVP3** hoàn tất |
| **BR-004-05** | Người dùng phải có **panel card**: form spec + ảnh preview + `Regenerate` + **variant picker**. Variant picker là hành động sáng tạo **rẻ nhất mà giá trị pháp lý cao nhất** — *chọn = authorship* | `MVP-Scope` §5.2 thành phần **#1** (**5–7%** `[EM]`) · §6 **KC-2** | **MVP3** |
| **BR-004-06** | ⭐ **MỌI hành động của người dùng trong editor phải sinh một `change_log` row — kể cả hành động chỉ là *"chọn generation X thay vì Y"***. Đây là điều kiện làm cho việc cắt canvas **hợp pháp**: prompt một mình **không** chứng minh được *"decisive contribution"*; cái chứng minh được là *người đã chọn X thay vì Y, đã sửa thoại, đã đổi camera, đã kéo bubble* | `MVP-Scope` §5.2 callout *ràng buộc xuyên suốt* · [§6](../../010-Planning/MVP-Scope.md#6-không-được-cắt--danh-sách-cứng) **KC-2** · CF-7.2 `[OFF]` (NĐ 134/2026 Điều 5a) | **MVP1** |
| **BR-004-07** | Layout trang phải được lưu dưới dạng **toạ độ chuẩn hoá 0–1** trong `page_layout JSONB` **ngay từ MVP**; template chỉ là các preset ghi vào **cùng** schema đó. Mục đích: đường nâng cấp lên canvas thật **không phải migrate dữ liệu**, chỉ thay lớp tương tác. ⛔ **Không viết renderer từ đầu** | `MVP-Scope` [§4.1](../../010-Planning/MVP-Scope.md#41-canvas-editor-14--cắt-một-phần-cf-91) *"đường nâng cấp không mất mát"* · CF-9.1 | **MVP2** (cùng `BR-004-02`) |
| **BR-004-08** | Undo/redo chỉ có ở phạm vi **cục bộ** (trong form + vị trí bubble). **Không có undo qua generation** — một `Regenerate` **tiêu tiền thật và không hoàn lại được** ⇒ UX **phải nói rõ** điều này với người dùng, không để họ suy đoán | `MVP-Scope` [§5.3](../../010-Planning/MVP-Scope.md#53-bốn-thành-phần-hoãn) hàng **#7** (*"điều kiện mở lại: không mở lại theo dạng này; đúng hơn là làm rõ UX rằng generation không undo được"*) | ⚠️ `[EM]` **MVP3** — em gán theo mốc của thành phần #1 (nơi `Regenerate` xuất hiện trong UI). `MVP-Scope` **không** gán mốc cho hàng này |
| **BR-004-09** | Mỗi nhân vật có **expression sheet** — ở bản tối thiểu là **3 góc + 3 biểu cảm** tham chiếu; đầy đủ chỉ ở Full Scope. Mục đích: panel cần biểu cảm khác **không phải sinh lại identity** | `MVP-Scope` §3 hàng **D7** · Analysis §6.3 | **MVP3** (`🟡` 3 góc + 3 biểu cảm) → Full Scope `✅` |
| **BR-004-10** | ⛔ **Việc cắt UI duyệt cây generation (D6) KHÔNG được kéo theo việc cắt cột dữ liệu lineage.** Mọi `generation` sinh ra từ editor vẫn phải mang `parent_generation_id` + `relation_kind` + `field_provenance` + `generation.origin`. Điều kiện chặn của BRD-004; **requirement gốc thuộc BRD-007** (nhóm `GP-1`, KC-1/KC-3) | `MVP-Scope` [§3.1](../../010-Planning/MVP-Scope.md#31-ba-ô-đáng-chú-ý-nhất-trong-bảng) (*"cắt UI cây generation, giữ nguyên cột `parent_generation_id`"*) · [§6.1](../../010-Planning/MVP-Scope.md#61-ba-hiểu-nhầm-hay-gặp-về-danh-sách-này) · **KC-1**, **KC-3** · `CẤM-09` | **MVP1** (theo KC-1/KC-3) |

> **Ghi chú traceability**: `BR-004-01` → thành phần #5 · `BR-004-02` → #3 · `BR-004-03` → #4 · `BR-004-04` → #2 · `BR-004-05` → #1. Năm thành phần bắt buộc của [MVP-Scope §5.2](../../010-Planning/MVP-Scope.md#52-năm-thành-phần-bắt-buộc-2025--em-mẫu-số-saas) được phủ **đủ 5/5**.

---

## 4. Ràng buộc & điều kiện chặn

### 4.1 Danh sách cứng — `KC-x` của [MVP-Scope §6](../../010-Planning/MVP-Scope.md#6-không-được-cắt--danh-sách-cứng) mà module này chạm

| KC | Nội dung | Quan hệ với BRD-004 | Không giữ thì hỏng thế nào |
|---|---|---|---|
| **KC-2** ⭐ | `change_log` ghi **mọi** hành động người dùng — kể cả *"chọn generation X thay vì Y"*. Từ **MVP1**. Chi phí: một bảng append-only | **Đây là KC do BRD-004 trực tiếp sinh dữ liệu vào.** Mọi thành phần editor (#1–#5) đều là một nguồn ghi `change_log` ⇒ `BR-004-06` là **Definition of Done xuyên suốt**, không phải một tính năng rời | **Prompt một mình không chứng minh được *"decisive contribution"***. Không có `change_log` ⇒ không có bằng chứng ⇒ **Điều 5a không thoả** |
| **KC-1** | `parent_generation_id` (nullable FK) + `relation_kind ENUM('retry','variation','refine','continuity_fix')`. Từ **MVP1**. Chi phí: hai cột | BRD-004 **không sở hữu** KC-1, nhưng mọi `Regenerate` / chọn variant trong editor đều **phải** ghi đúng lineage ⇒ là **điều kiện chặn** của `BR-004-05` | Tác phẩm của Founder **và của khách hàng** **không được bảo hộ bản quyền ở Việt Nam** (CF-7.2 `[OFF]`). Và **không backfill được** |
| **KC-3** | `field_provenance` (mức field) + `generation.origin ENUM('ai','ai_edited','human')`. Từ **MVP1** | Là thứ **làm cho việc cắt canvas hợp pháp** — nó phân định phần nào do người, phần nào do AI trên chính các field mà editor sửa | Không xác định được **ranh giới phần được bảo hộ** |
| **KC-4** | KC-1 + KC-2 + KC-3 phải **commit CÙNG MỘT TRANSACTION** với artifact mà chúng chứng minh | Mọi lần lưu của editor là một transaction gồm *thay đổi spec* + `change_log` (+ `generation` nếu có regenerate). Phụ thuộc **cứng** vào monolith 1 DB của [BRD-005](./BRD-005-Multi-Tenancy-And-Platform.md) (E5) | *"Bằng chứng có thể thiếu ngẫu nhiên thì không phải bằng chứng."* Audit trail commit tách rời artifact là audit trail **không đáng tin về mặt pháp lý** |

### 4.2 Ràng buộc cấp dự án — `C-x` của [Charter §7](../../010-Planning/Charter-Comic-Studio.md#7-ràng-buộc-constraints)

| C | Ràng buộc | Hệ quả bắt buộc với BRD-004 |
|---|---|---|
| **C1** | **Đội 1 người + AI assist. Không funding, không ngân sách marketing** `[CHỐT]` CF-1.2 | Đây là **lý do quyết định** của việc cắt canvas: canvas editor là software engineering thuần, khó thật, và **không AI nào viết hộ được phần khó** (state machine, perf với hàng trăm ảnh, undo trên side-effect không hoàn lại, race khi user sửa spec trong lúc generation đang bay). Một dev chọn build canvas trước là *"gần như chắc chắn không bao giờ tới được phần AI"* ([MVP-Scope §4.1](../../010-Planning/MVP-Scope.md#41-canvas-editor-14--cắt-một-phần-cf-91)) |
| **C9** | **Thứ tự milestone cố định: MVP0 → MVP1 → MVP2 → MVP3 → MVP4** CF-8.3 | Không đảo thứ tự để *"làm phần dễ trước"*. Thành phần #5 ở MVP1, #3/#4 ở MVP2, #1 ở MVP3 — **không kéo #1 lên trước #5** vì #5 là nơi moat lộ ra với khách |
| **C10** | **Horizon 6 tháng (09/2026–02/2027) CHƯA được ai xác nhận là đủ cho 1 dev** `[CHỐT]` CF-8.1 + CF-8.13 | ⛔ **Cấm nén lịch cho vừa khung** (`CẤM-08`). Theo [Roadmap §5.1](../../010-Planning/Roadmap.md#51-cái-gì-rơi-ra-khỏi-092026022027), **MVP3 rơi ra ngoài horizon** ⇒ thành phần **#1 (panel card + variant picker)** và **D7 (expression sheet)** nằm **NGOÀI** horizon |
| **C6 / C7 / C8** | Margin **50–60%** `[BCN]` · chi phí **$12,06/chapter là SÀN** `[EM tính từ OFF]` · **N=3 mặc định cho MỌI panel** `[OFF]` | Liên quan **gián tiếp nhưng chặn**: `BR-004-04` (sửa thoại không phải regenerate ảnh) và `BR-004-08` (không undo qua generation) tồn tại **vì mỗi lần generate tiêu tiền thật**. Chi tiết kinh tế thuộc [BRD-006](./BRD-006-Credit-And-Unit-Economics.md) |

### 4.3 Điều kiện chặn về cách trích số liệu

⛔ Mọi tài liệu con của BRD-004 (Epic, Story, UC, ticket) **phải** tuân thủ [mục 1.1](#11--cảnh-báo-mẫu-số--đọc-trước-khi-nhìn-bất-kỳ-con-số--nào-trong-tài-liệu-này): trích thì trích **nguyên cặp *số + nhãn `[EM]` + mẫu số***, và **không thực hiện phép tính nào** trên chúng (`CẤM-01`, `CẤM-15`).

---

## 5. Cái module này KHÔNG làm

Năm hàng còn lại của nhóm `D` trong [MVP-Scope §3](../../010-Planning/MVP-Scope.md#3-bảng-mvp-vs-full-scope). Cột *Nhãn theo mốc* copy nguyên bảng gốc theo thứ tự `MVP0 · MVP1 · MVP2 · MVP3 · MVP4 · Full Scope`.

| Hàng | Thành phần | Nhãn theo mốc | Thành phần [§5.3](../../010-Planning/MVP-Scope.md#53-bốn-thành-phần-hoãn) | Lý do hoãn/cắt | **Điều kiện mở lại** |
|---|---|---|:--:|---|---|
| **D2** | Infinite canvas, zoom/pan cả chapter, hình học panel tự do, panel xoay / không chữ nhật | ❌ · ❌ · ❌ · ⛔ · ⛔ · 🟡 *nếu có bằng chứng khách cần* | **#6** | **Chi phí lớn nhất, giá trị tăng thêm nhỏ nhất** ở bản trả phí đầu (CF-9.1) | Có **bằng chứng đo được** rằng khách rời đi vì thiếu nó. Khi làm: dùng `tldraw` / `konva` / `fabric.js` sau một spike riêng — ⛔ **không viết renderer từ đầu** |
| **D3** | Undo/redo xuyên toàn bộ state phân tán | ❌ · ❌ · ❌ · ⛔ · ⛔ · ⛔ | **#7** | Chỉ undo **cục bộ** trong form + vị trí bubble. **Không undo qua generation** — một `Regenerate` tiêu tiền thật và không hoàn lại được | **Không mở lại theo dạng này**; đúng hơn là **làm rõ UX** rằng generation không undo được ⇒ đã nâng thành `BR-004-08` |
| **D4** | Realtime collaboration | ❌ · ❌ · ❌ · ❌ · ⛔ · 🟡 *khi bán gói team* | **#8** | **1 user = 1 tenant** ở bản đầu (CF-9.1) | Khi **bán gói team** — mà `membership` (E2, [BRD-005](./BRD-005-Multi-Tenancy-And-Platform.md)) đã chuẩn bị sẵn cho ngày đó |
| **D5** | Inpainting brush / drawing tools | ❌ · ❌ · ❌ · ❌ · ⛔ · 🟡 *kèm `generation.origin='ai_edited'`* | **#9** | Cần, nhưng **không phải để bán được bản đầu** | Khi làm: **bắt buộc** set `generation.origin='ai_edited'` (KC-3) |
| **D6** ⛔ | UI duyệt **cây** generation (tree view / diff / branch-merge) | ❌ · ❌ · ❌ · ❌ · ❌ · ❌ **cắt hẳn** | — | Flat list `created_at` + `approved_generation_id` đủ **95% giá trị** (Analysis §6.3–6.4). Là hạng mục bị **loại khỏi thiết kế**, không phải bị hoãn | **KHÔNG có điều kiện mở lại trong `MVP-Scope`.** Em không đặt thêm điều kiện nào |

### 5.1 ⛔ Bẫy chết người của module này: D6 ≠ KC-1

> [!CAUTION]
> **Cắt UI cây generation KHÔNG phải cắt cột dữ liệu lineage.** Đây là hai quyết định **độc lập và trái chiều** — `MVP-Scope` [§6.1](../../010-Planning/MVP-Scope.md#61-ba-hiểu-nhầm-hay-gặp-về-danh-sách-này) xếp việc gộp chúng làm một vào danh sách *"ba hiểu nhầm hay gặp"*, và [§3.1](../../010-Planning/MVP-Scope.md#31-ba-ô-đáng-chú-ý-nhất-trong-bảng) gọi đây là cặp *"rất dễ bị gộp làm một khi cắt scope"*.
>
> | | **D6 — UI duyệt cây** | **KC-1 / KC-3 — cột dữ liệu** |
> |---|---|---|
> | Trạng thái | ❌ **cắt hẳn**, không có trong Full Scope | ✅ **bắt buộc từ MVP1**, trong danh sách cứng |
> | Bản chất | Tầng **UI** — tự do chọn cái rẻ (NT-2) | Tầng **DỮ LIỆU** — **hồ sơ pháp lý** theo NĐ 134/2026 **Điều 5a** (CF-7.3 `[OFF]`) |
> | Thay thế được không | Có — flat list `created_at` + `approved_generation_id` đủ 95% giá trị | **Không.** Và **không backfill được** — thêm cột sau thì mọi generation quá khứ có `parent = NULL` **vĩnh viễn** |
>
> ⇒ **Gộp nhầm hai thứ này là mất bảo hộ bản quyền** — của Founder **và của khách hàng của Founder**. Đây là `CẤM-09`, và [MVP-Scope §4.4](../../010-Planning/MVP-Scope.md#44--parent_generation--không-cắt-đây-là-một-sự-tự-thu-hồi) ghi lại nó dưới dạng **một sự tự thu hồi công khai** của PM run trước — dấu vết quyết định, không phải một khuyến nghị.

### 5.2 Ba thứ khác BRD-004 không sở hữu

| Hạng mục | Ai sở hữu | Vì sao ghi ra đây |
|---|---|---|
| `parent_generation_id` / `relation_kind` / `field_provenance` / `generation.origin` / `change_log` **schema** | [BRD-007](./BRD-007-Legal-And-Compliance.md) (nhóm `GP-1`, KC-1→KC-4) | BRD-004 là **nguồn ghi** dữ liệu vào chúng (`BR-004-06`, `BR-004-10`), không phải nơi định nghĩa schema |
| **Export PDF / CBZ / webtoon** (H4) | [BRD-008](./BRD-008-Quality-And-Operations.md) | `BR-004-03` (preview) **tái dùng compositor của export** — quan hệ phụ thuộc, không phải quan hệ sở hữu |
| **Typeset layer + bubble overlay ở tầng render** (A2) | [BRD-001](./BRD-001-Image-Generation-Pipeline.md) | BRD-004 sở hữu **tương tác của người dùng** trên overlay đó (`BR-004-04`), không sở hữu cơ chế composite |

---

## 6. Rủi ro chính

Sổ rủi ro là [Risk-Register.md](../../010-Planning/Risk-Register.md). ⛔ **Tài liệu này không tự chấm điểm rủi ro mới** — chỉ trỏ tới hàng đã có.

| Rủi ro | Vì sao liên quan tới BRD-004 |
|---|---|
| [**R-01**](../../010-Planning/Risk-Register.md#21-bảng-chính) — Pháp lý, Score **9** (cao nhất bảng) | Không lưu provenance từ generation **đầu tiên** ⇒ mất bảo hộ và **không backfill được**. BRD-004 là nơi rủi ro này **hiện thực hoá qua hành vi người dùng**: mỗi hành động editor không sinh `change_log` là một mảnh bằng chứng mất vĩnh viễn (`BR-004-06`) |
| [**R-13**](../../010-Planning/Risk-Register.md#21-bảng-chính) — Kỹ thuật, `accepted` | Props chỉ **4.19/5** `[OFF]` — thấp nhất trong 4 metric của CANVAS. Mitigation đã chấp nhận là *"sửa tay ở editor tối thiểu"* ⇒ editor tối thiểu là **đường lui đã được ghi nhận** cho một rủi ro kỹ thuật, không chỉ là một tính năng |
| [**R-18**](../../010-Planning/Risk-Register.md#21-bảng-chính) — Thị trường/Cạnh tranh | GlobalComix ($13M, mua lại INKR, định vị *"the Figma for comics"*) đánh **đúng trục editor**. Mitigation đã chốt: **không cạnh tranh ở trục editor** ⇒ củng cố quyết định cắt canvas ở [mục 5](#5-cái-module-này-không-làm), và là lý do BRD-004 **cố ý** giữ phạm vi tối thiểu |
| [**R-21**](../../010-Planning/Risk-Register.md#21-bảng-chính) — Vận hành, `accepted` | **Bus factor = 1.** Mitigation nêu thẳng *"mọi ràng buộc pháp lý nằm ở tầng dữ liệu chứ không ở tầng UI (CF-9.1)"* — đó chính là NT-2, nguyên tắc chi phối toàn bộ BRD-004 |

---

## 7. Tài liệu liên quan

### 7.1 Tầng Requirements & Backlog

| Loại | Tài liệu | Quan hệ |
|---|---|---|
| PRD | [PRD-Comic-Studio.md](../PRD-Comic-Studio.md) | BRD-004 chi tiết hoá mục *Editor tối thiểu* của PRD |
| SRS | [SRS-Comic-Studio.md](../SRS-Comic-Studio.md) | Yêu cầu hệ thống tương ứng |
| Epic | [Epic-Minimum-Editor.md](../../022-User-Stories/Epics/Epic-Minimum-Editor.md) | Epic 1:1 với BRD-004 |
| BRD liên quan | [BRD-005](./BRD-005-Multi-Tenancy-And-Platform.md) (E5 — một transaction boundary cho KC-4) · [BRD-006](./BRD-006-Credit-And-Unit-Economics.md) (vì sao `Regenerate` không undo được) · [BRD-007](./BRD-007-Legal-And-Compliance.md) (chủ sở hữu KC-1→KC-4) · [BRD-008](./BRD-008-Quality-And-Operations.md) (compositor của export) | Phụ thuộc chéo |

### 7.2 Use Case

| UC | Yêu cầu nghiệp vụ mà nó thực hiện |
|---|---|
| [UC-02 — Review & Edit Story Bible](../Use-Cases/UC-02-Review-And-Edit-Story-Bible.md) | `BR-004-01`, `BR-004-06` |
| [UC-06 — Generate Panel & Pick Variant](../Use-Cases/UC-06-Generate-Panel-And-Pick-Variant.md) | `BR-004-05`, `BR-004-06`, `BR-004-08`, `BR-004-10` |
| [UC-07 — Edit Bubble & Dialogue In Panel](../Use-Cases/UC-07-Edit-Bubble-And-Dialogue-In-Panel.md) | `BR-004-04`, `BR-004-06` |
| [UC-08 — Arrange Page & Preview](../Use-Cases/UC-08-Arrange-Page-And-Preview.md) | `BR-004-02`, `BR-004-03`, `BR-004-07` |

### 7.3 Nguồn Planning & Research

- [MVP-Scope.md](../../010-Planning/MVP-Scope.md) — **§3** nhóm D (nguồn của [mục 2](#2-phạm-vi-module) và [mục 5](#5-cái-module-này-không-làm)) · **§5 toàn bộ** (§5.1 cảnh báo mẫu số, §5.2 năm thành phần bắt buộc, §5.3 bốn thành phần hoãn) · §3.1, §4.1, §4.4, §6, §6.1
- [Charter-Comic-Studio.md](../../010-Planning/Charter-Comic-Studio.md) — **§7** ràng buộc C1–C10 · §8 giả định A6 (⚠️ cảnh báo mẫu số CF-6.7 vs CF-6.8)
- [Roadmap.md](../../010-Planning/Roadmap.md) — **§5.1** (MVP3 rơi ra ngoài horizon ⇒ thành phần #1 và D7 nằm ngoài)
- [Risk-Register.md](../../010-Planning/Risk-Register.md) — R-01, R-13, R-18, R-21
- [Glossary.md](../../999-Resources/Glossary.md) — `field_provenance` / `change_log`, `Generation` / `parent_generation`
- [Analysis-Comic-Studio-Concept.md](../../050-Research/Analysis-Comic-Studio-Concept.md) — §6.1 (năm khoảng % thành phần), §6.3–6.4 (generation lineage, flat list đủ 95% giá trị). ⛔ **Không sửa tài liệu này** (`CẤM-18`) — nó là dấu vết quyết định tại thời điểm viết

> ⛔ **Không link tới `docs/030-Specs/`**: tầng technical spec chưa tồn tại và nằm ngoài scope của run này.

---

_BRD by Comic Studio — role `business-analyst`._
_Author: trisjr_
