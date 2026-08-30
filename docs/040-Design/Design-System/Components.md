---
id: DS-006
type: design-system
status: draft
project: comic-studio
owner: "@trisjr"
tags: [design-system, phase-3]
created: 2026-08-30
updated: 2026-08-30
---

# Components

> **Part of:** [Design MOC](../Design-MOC.md)
> **Đọc trước:** [Foundations](./Foundations.md) — §*Hợp đồng phát biểu token* · §*Chuẩn accessibility* · §*Cách kiểm*
> **Tiêu thụ token của:** [Color Tokens](./Color-Tokens.md) · [Typography](./Typography.md) · [Spacing & Layout](./Spacing-And-Layout.md)
> **Nguồn nghiệp vụ:** [SRS](../../020-Requirements/SRS-Comic-Studio.md) §3.D · [SDD](../../030-Specs/Architecture/SDD-Comic-Studio.md) §6.3 · [MVP-Scope](../../010-Planning/MVP-Scope.md) §5.2

> [!IMPORTANT]
> ⭐ **File này ⛔ KHÔNG định nghĩa một giá trị nào.** Hex, cỡ chữ, bậc spacing thuộc bốn file kia (`HĐ-1`) — ở đây chỉ **tham chiếu tên token** và nói **ráp chúng thành cái gì**. Định nghĩa trùng chỗ ⇒ hai nơi phải đồng bộ, và một trong hai sẽ lệch.
> ⭐ **Đây là file khép lại bộ 6.** Bốn file trước định nghĩa *nguyên liệu*; file này là chỗ **ba ràng buộc kiến trúc nguy hiểm nhất hạ cánh thành UI cụ thể** — nếu không, chúng ⛔ không có nhà ở đâu cả.
> **Độc giả đích là AI assist sinh code** (`E2`) ⇒ mỗi component phát biểu bằng **bốn thứ kiểm được**: *tên · surface · ánh xạ thư viện · tập state đóng*.

## Mục lục

- [Inventory theo nhóm màn hình](#inventory-theo-nhóm-màn-hình)
- [Ánh xạ shadcn/Radix: dùng nguyên / mở rộng / tự build](#ánh-xạ-shadcnradix-dùng-nguyên--mở-rộng--tự-build)
- [Ma trận state](#ma-trận-state)
- [Ba pattern đặc thù sản phẩm](#ba-pattern-đặc-thù-sản-phẩm)
- [⛔ Component KHÔNG được đặc tả ở run này](#-component-không-được-đặc-tả-ở-run-này)
- [Tài liệu tham khảo](#tài-liệu-tham-khảo)

---

## Inventory theo nhóm màn hình

### 12 nhóm màn hình — component nào sống ở đâu

| # | Nhóm màn hình | Surface | Component | Trong horizon 09/2026–02/2027? |
|:--:|---|---|---|---|
| 1 | Workspace / tenant shell + danh sách tác phẩm | S-01 | `C-06` | ✅ |
| 2 | Khu vực ingest | S-02, S-03 | `C-01` `C-02` `C-03` `C-04` `C-05` `C-07` `C-14` | ✅ |
| 3 | Khu vực review Story Bible | S-04 | `C-01` `C-02` `C-04` `C-05` `C-06` `C-07` `C-08` `C-09` `C-10` | ✅ |
| 4 | Khu vực review panel script (Comic IR) | S-05 | `C-01` `C-02` `C-03` `C-04` `C-05` `C-06` `C-10` `C-11` | ✅ |
| 5 | ⭐ **Khu vực human gate** (hai gate — *"chỉ xong CÙNG NHAU"*) | S-06, S-07 | `C-01` `C-02` `C-03` `C-04` `C-06` `C-10` `C-11` `C-12` `C-13` | ✅ |
| 6 | Panel card + variant picker | S-08, S-09 | `C-01` `C-02` `C-04` `C-05` `C-07` `C-09` `C-10` `C-11` `C-12` | ⚠️ UI ngoài horizon (MVP3) |
| 7 | Editor panel / typeset | S-10 | `C-01` `C-05` `C-08` `C-09` `C-10` `C-11` + `C-20` | ⚠️ Bắt đầu MVP2, hoàn tất MVP3 |
| 8 | Editor trang + preview | S-11, S-12 | `C-01` `C-02` `C-03` `C-08` `C-11` `C-16` + `C-18` `C-19` | ✅ |
| 9 | Khu vực export | S-13 | `C-01` `C-02` `C-03` `C-06` `C-07` `C-13` `C-16` + `C-24` | ✅ (chỉ PDF ở MVP2) |
| 10 | Khu vực credit / billing / BYOK | S-14, S-15, S-16 | `C-01` `C-02` `C-03` `C-11` + `C-22` `C-23` | ⛔ **NGOÀI HORIZON** |
| 11 | ⭐ Khu vực takedown công khai (**shell riêng, ⛔ không đăng nhập**) | S-17, S-18 | `C-02` `C-07` `C-15` | ✅ |
| 12 | ⚠️ Khu vực operator (Founder) | S-19 | ⛔ **KHÔNG component nào** — [xem mục CẤM](#-component-không-được-đặc-tả-ở-run-này) | ⛔ **Mô hình quyền chưa tồn tại** |

> ⚠️ **Hai nhóm phá giả định *"một hệ thiết kế cho cả sản phẩm"*:**
> - **Nhóm 11** có actor **ngoài hệ thống, ⛔ không tài khoản, ⛔ không tenant context** ⇒ ⛔ không dùng lại được pattern nào của app đã đăng nhập. Quy tắc brand cho bề mặt này do [Brand Guidelines](./Brand-Guidelines.md) §*Bề mặt takedown công khai* sở hữu — ⛔ file này ⛔ không quyết lại.
> - **Nhóm 10** giao một phần bề mặt cho **vendor billing** ([MVP-Scope](../../010-Planning/MVP-Scope.md) `E4` = *mua auth + billing, ⛔ không tự viết*) ⇒ ⛔ Design System ⛔ không đặc tả màn hình thanh toán, chỉ đặc tả **điểm bàn giao**.
>   ⚠️ Mã `E4` **va chạm namespace**: `MVP-Scope` `E4` (điều kiện khả thi) ⛔ **không phải** `escalations.md` `E4` (takedown) của run này. Trong file này, `E4` **trần** luôn có nghĩa escalation; nghĩa `MVP-Scope` phải viết kèm tên tài liệu như dòng trên.

### 16 component ⛔ KHÔNG hoãn được — `C-01`…`C-16`

> Mã `C-xx` **giữ nguyên** để truy ngược về [findings/business-analyst](../../010-Planning/pm-runs/2026-08-30-brand-guidelines-va-design-system-comic-studio/findings/business-analyst.md) §2.1 (`C-01`…`C-13`, dùng ở **≥3 surface**) và §2.2 (`C-14`…`C-16`, dùng 1–2 chỗ nhưng mang **ràng buộc cứng**).
> Cột *Ánh xạ* là **tóm tắt**; nhóm đầy đủ + cảnh báo verify ở [mục ánh xạ](#ánh-xạ-shadcnradix-dùng-nguyên--mở-rộng--tự-build).

| Mã | Component | Surface | Ánh xạ | State bắt buộc (tập **đóng**) |
|:--:|---|---|---|---|
| **`C-01`** ⭐⭐ | **Alert / Callout — BA MỨC phân biệt được** | S-02, S-03, S-04, S-05, S-06, S-07, S-08, S-09, S-10, S-11, S-13, S-14, S-16 (**13**) | **Mở rộng** | `từ-chối` · `cảnh-báo` · `thông-tin` — ⛔ **không** state `dismissed` cho mức `từ-chối`; ⛔ **không** tự tắt theo thời gian. [Chi tiết ba mức](#-c-01-chi-tiết--ba-mức-mỗi-mức-một-uc-thật) |
| **`C-02`** | **Error state có LÝ DO CỤ THỂ + ĐƯỜNG XỬ LÝ** | S-02, S-03, S-04, S-05, S-07, S-08, S-12, S-13, S-14, S-16 (**10**) | **Mở rộng** của `C-01` | `error-có-retry` · `error-⛔-không-retry-được` · `error-cần-hành-động-của-người`. ⭐ Bắt buộc có prop **lớp lỗi**, ⛔ **không** chỉ `message: string` (`ARC-17`); ⚠️ format mã lỗi là **`TBD-API-ENV`**, chủ **Architect** ⇒ ⛔ file này ⛔ không chốt casing |
| **`C-03`** | **Status badge / state chip** | S-02, S-03, S-05, S-06, S-07, S-11, S-12, S-13, S-14 (**9**) | **Mở rộng** | Tập trạng thái nghiệp vụ đã đặt tên: `chưa xác nhận` / `đã xác nhận` · gate `OPEN` / `PASS` · `pending` · `gate 1/2 đã xong` · `superseded` · `disable-access` · *"chưa có ở mốc hiện tại"* · `available` / `hold`. ⛔ **KHÔNG gộp** — mỗi cái mang một hệ quả pháp lý hoặc kinh tế khác nhau |
| **`C-04`** | **Loading / long-running job** | S-03, S-04, S-05, S-07, S-08, S-12, S-13 (**7**) | **Tự build** | Đúng **5** giá trị `job_status` + `đang-làm-mới-trên-nền`. [Chi tiết](#b-trạng-thái-tiến-trình-async--phủ-đúng-danh-mục-đóng-job_status) |
| **`C-05`** | **Form + field-level control** (input · select · textarea · numeric) | S-02, S-04, S-05, S-08, S-10, S-16 (**6**) | **Dùng nguyên** + **mở rộng** | `default` · `hover` · `focus-visible` · `disabled` · `read-only` · `invalid` · ⭐ `locked-by-human-edit` (`SRS-FR-12` + `SDD-HG-01.7`: edit của người **phải khoá lại** khỏi bị re-run ghi đè) · `field-provenance` (xem `C-09`) |
| **`C-06`** | **Data list / table có hàng chọn được** | S-01, S-04, S-05, S-06, S-07, S-13 (**6**) | **Mở rộng** | Hàng: `default` · `hover` · `selected` · `focus-visible` · **state nghiệp vụ riêng của từng hàng** · ⭐ `định-vị-hàng-chưa-quyết-đầu-tiên` (`UC-04` `ALT-5`) — đây là **đường hợp lệ duy nhất** để giảm giờ-người ở màn gate |
| **`C-07`** | **Confirm dialog cho hành động ⛔ không đảo ngược được** | S-02, S-04, S-08, S-09, S-13, S-17 (**6**) | **Dùng nguyên** + **mở rộng** | `idle` · `đang-thực-thi` · `error`. ⭐ Bốn loại hành động ⛔ không rút lại được: `Regenerate` **tiêu tiền thật** (`BR-004-08` — *"UX **phải nói rõ**, ⛔ không để actor suy đoán"*) · hard-delete tenant · export ra ngoài · takedown soft-delete. Dùng `--destructive` (**hành động của NGƯỜI**), ⛔ **không** dùng `--danger` (**phán quyết của HỆ THỐNG**) |
| **`C-08`** | **Empty state** | S-04, S-07, S-10, S-12 (**4**) | **Mở rộng** | `rỗng-hợp-lệ` · `rỗng-vì-chưa-có-dữ-liệu` · ⭐ `ô-trống` (panel chưa có ảnh — `UC-08` `AF-6`, empty state **duy nhất** được mô tả ở mức hiển thị). ⛔ **CẤM tạo entity rác để "có gì đó hiển thị"** (`UC-02` `EXC-1`), ⛔ **cấm sinh panel script rỗng** (`UC-03` `EXC-2`) ⇒ empty state ở sản phẩm này là **quyết định nghiệp vụ: thà rỗng còn hơn giả** |
| **`C-09`** | **Provenance / origin indicator** | S-04, S-08, S-09, S-10 (**4**) | **Tự build** | Đúng **ba** giá trị `origin`: `ai` · `ai_edited` · `human` (`SRS-FR-36`, `ARC-31`) + mức field `field_provenance`. ⛔ **KHÔNG gộp `ai_edited` về một trong hai cực** — nội dung **hỗn hợp** phải đánh dấu đúng bản chất hỗn hợp |
| **`C-10`** ⭐ | **AI-disclosure indicator** | S-04, S-05, S-06, S-07, S-08/S-09 (**5** — mọi điểm chạm AI) | **Tự build** | `hiển-thị` — ⭐ **và ⛔ KHÔNG có state nào khác**. [Chi tiết](#-c-10-ai-disclosure--nghĩa-vụ-duy-nhất-mà-bằng-chứng-là-một-bề-mặt-ui) |
| **`C-11`** | **Budget / quota / ngưỡng** — mức hiện tại + trần + hệ quả khi vượt | S-05 (emphasis quota) · S-07, S-10 (`text_budget`) · S-08, S-14 (credit hold) (**5**) | **Tự build** | `trong-ngưỡng` · `sắp-cạn` · `đã-cạn-buộc-đánh-đổi` · `vượt-ngưỡng-bị-chặn`. ⭐ Ba khái niệm khác nhau, **một pattern**: trần **rời rạc**, vượt thì **bị chặn chứ ⛔ không co giãn** — `UC-03` `EXC-5`: *"nếu mọi panel đều được nhấn thì ⛔ không panel nào được nhấn"* |
| **`C-12`** | **Diff / side-by-side có NGƯỜI quyết** | S-07 (gốc→nén) · S-09 (candidate) · X-4 (`SRS-FR-21`) (**3**) | **Tự build** | ⭐ **Đúng ba lối ra**: `chọn-A` · `chọn-B` · `unclear`. `unclear` / `UNKNOWN` là câu trả lời **hợp lệ hạng nhất**, ⛔ **không** phải trạng thái lỗi. ⛔ **CẤM nút auto-apply** — `SRS-FR-21` (**CHỐT**) đã **cắt hẳn** `[Fix automatically]`; giữ **cả hai/cả ba** phương án, ⛔ **không bao giờ tự áp dụng** (`ARC-27`) |
| **`C-13`** | **Counter / progress theo đơn vị công việc còn lại** | S-06 (*"còn N dòng chưa xác nhận"*) · X-3 (*"đã kiểm N/M panel"*) · S-13 (page thiếu gate) (**3**) | **Mở rộng** | `còn-N-việc` · `đã-xong` · ⭐ `công-bố-độ-phủ`. `SRS-FR-22` (**CHỐT**) đòi **cả tử số, cả mẫu số, cả lý do**: *"đã kiểm **N/M** panel, **M−N** panel ⛔ không kiểm được vì có nhiều nhân vật"*. ⛔ **CẤM giấu con số này để trông đẹp hơn**, ⛔ cấm làm tròn lên rồi bỏ mẫu số (`ARC-33`) |
| **`C-14`** ⭐ | **Consent checkbox — cam kết quyền tại BƯỚC UPLOAD** | S-02 (**1**) | **Dùng nguyên** + **mở rộng** | `chưa-tick` (⇒ **upload ⛔ không được nhận**, `UC-01` `EXC-2`) · `đã-tick`. ⛔ **CẤM `defaultChecked`** — *quyết định Phase 3, suy ra từ mục đích của `SRS-FR-41`*: một cam kết đã tick sẵn ⛔ không còn là cam kết. Gắn vào **bước upload**, ⛔ **không chỉ ở trang ToS** |
| **`C-15`** ⭐ | **Public form ⛔ không cần đăng nhập** | S-17 (**1**) | **Tự build** | `trống` · `đang-gửi` · `đã-tiếp-nhận-có-timestamp` · `thiếu-thông-tin-cần-bổ-sung` (`UC-11` `EF-1`). ⚠️ **`TBD` ⛔ không được tự lấp**: (a) **danh sách trường bắt buộc**; (b) **SLA 72 giờ** (`CF-7.6` `[OFF]`) có tạm dừng khi chờ bổ sung hay không — ⛔ *"⛔ không nguồn nào trong repo nói"* |
| **`C-16`** | **Read-only composite viewer** | S-12, S-13 (**2**) | **Tự build** | `đang-composite` · `xong` · `error-có-retry` · `ô-trống` (`C-08`). ⭐ **Một implementation, HAI bề mặt** — [xem `P-2`](#p-2--preview-và-export-là-hai-bề-mặt-riêng) |

#### ⭐ `C-01` chi tiết — ba mức, mỗi mức một UC thật

> [!CAUTION]
> ⭐⭐ **Component quan trọng nhất của cả hệ này** — xuất hiện ở **13 surface** ⇒ **sai một lần là sai xuyên 13 màn hình**. Trộn ba mức là **lỗi nghiệp vụ, ⛔ không phải lỗi thẩm mỹ**: ba mức trả lời ba câu khác nhau về **quyền hành động của người dùng**.

| Mức | Câu nó trả lời | Token (⛔ định nghĩa ở [Color Tokens](./Color-Tokens.md), ⛔ **không** lặp hex ở đây) | ⭐ UC thật |
|---|---|---|---|
| ⛔ **TỪ CHỐI ở tầng DB/pipeline** | *"Việc này **đã bị chặn**."* ⛔ **Không** có nút *"cứ tiếp tục"* | `--danger-subtle` / `--danger-subtle-foreground`; viền & icon dùng `--danger` | `M2-2` — ***"bị từ chối, KHÔNG PHẢI bị cảnh báo"***: sửa panel thành ≥4 nhân vật (`UC-03` `EXC-1`) · thêm nhân vật thứ 4 khi đang đặt bubble (`UC-07` `EX-7`) · `UC-08` `EX-6`. Cộng: `M2-4` **từ chối export** (`UC-09` `EF-1`) · **chặn opt-out signal** (`UC-01` `EXC-1`) |
| ⚠️ **CẢNH BÁO cho qua được** | *"Đi tiếp **được**, nhưng anh nên nhìn lại."* Actor có quyền **chấp nhận có ý thức** | `--warning-subtle` / `--warning-subtle-foreground`; viền & icon dùng `--warning` | `M2-3` — bubble **đè ra ngoài `text_safe_zone` / che mặt** (`UC-07` `EX-1`) · sửa `story_order` của event đã có panel (`UC-02` `EXC-5`) — ⚠️ cảnh báo này **phải hiện, ⛔ không được ẩn** |
| ℹ️ **THÔNG TIN** | *"⛔ **Không có gì hỏng cả.** Chỉ là một sự thật về phạm vi hiện tại."* | `--info-subtle` / `--info-subtle-foreground`; ⭐ **trung tính**, ⛔ **không xanh dương** — xanh dương va thẳng vào `--primary` | CBZ / webtoon ***"chưa có"*** ở mốc hiện tại (`UC-09` `EF-2`) — ⚠️ **⛔ không phải lỗi** |

**Ba tín hiệu ĐỒNG THỜI — ràng buộc cứng, ⛔ không được rút xuống còn một** ([Color Tokens](./Color-Tokens.md) §*Màu MỘT MÌNH ⛔ không đủ*, **quyết định Phase 3**):

| # | Tín hiệu | Ai sở hữu |
|:--:|---|---|
| **1** | **Cặp token màu riêng** — ⛔ không chia sẻ token giữa hai mức | [Color Tokens](./Color-Tokens.md) |
| **2** | ⭐ **Icon riêng, HÌNH DẠNG khác nhau** — ⛔ **không phải cùng một icon đổi màu** | ⭐ **File này.** Ba hình dạng phân biệt được **khi in đen trắng**: mức `từ-chối` = hình **bát giác / biển cấm**; mức `cảnh-báo` = hình **tam giác**; mức `thông-tin` = hình **tròn**. *Quyết định Phase 3.* ⛔ **Cấm** icon `shield` / `verified` — [xem mục CẤM](#-component-không-được-đặc-tả-ở-run-này) |
| **3** | ⭐ **Nhãn chữ nói thẳng mức độ** — người dùng đọc được *"đã bị từ chối"* mà ⛔ **không cần nhìn màu** | ⭐ **File này.** Nhãn dùng `--text-sm` + `--font-weight-medium`. ⛔ **Cấm nhãn mơ hồ** kiểu *"Lưu ý"* cho mức `từ-chối` |

> ⭐ **Vì sao ba tín hiệu chứ ⛔ không phải một:** đỏ và hổ phách nằm gần nhau trên trục sắc độ ⇒ với người mù màu đỏ-lục, mức `từ-chối` và mức `cảnh-báo` **có thể sụp vào nhau**. Ngưỡng tương phản ⛔ **không cứu được** việc này — nó đo *chữ trên nền*, ⛔ không đo *mức này khác mức kia*. *(Chuẩn a11y phát biểu ở **đúng một chỗ**: [Foundations](./Foundations.md) §Chuẩn accessibility — **quyết định Phase 3**, `G-3`.)*
> ⚠️ **Hệ quả trực tiếp lên copy**: nếu một thông điệp đã bị hệ thống chặn mà UI viết *"cảnh báo"*, người dùng sẽ **ngồi chờ một thao tác đã không bao giờ xảy ra**.

#### ⭐ `C-10` AI disclosure — nghĩa vụ DUY NHẤT mà bằng chứng là một bề mặt UI

> [!IMPORTANT]
> ⭐⭐ **⛔ Không có component này thì nghĩa vụ pháp lý ⛔ KHÔNG CÓ NHÀ.** `L-6` nguyên văn: nghĩa vụ này ⛔ *"**không để lại hàng dữ liệu nào**"* ⇒ Security Review Gate ⛔ **không kiểm được nó từ database**; bằng chứng phải là **ảnh chụp UI + hàng checklist ở tầng release**, ⛔ **không phải một query**.
> ⇒ Nếu Design System ⛔ không khai component này thì ⛔ **không tài liệu nào khác khai nó**, và `SRS-FR-40` (**CHỐT**) rơi im lặng.

| Điều khoản | Nội dung |
|:--:|---|
| **`AD-1`** | Chỉ dẫn hiển thị **tại điểm tương tác với tính năng AI** — cụ thể: màn **generate** (S-08), **variant picker** (S-09), và các điểm chạm LLM ở S-04, S-05, S-06, S-07. AC-1 của `Story-AI-Disclosure-Article-11` nguyên văn: ⛔ ***"không phải chỉ ghi trong ToS"*** |
| **`AD-2`** | ⛔ **CẤM mọi biến thể ẩn/tắt được**: ⛔ không prop `showAiBadge={false}`, ⛔ không *"ẩn trong chế độ tập trung"*, ⛔ không cờ cấu hình — **cùng khuôn `SDD-HG-01.2`** (`ARC-30`) |
| **`AD-3`** | ⛔ **KHÔNG gộp với `C-09`.** `C-10` là **chỉ dẫn tại điểm tương tác** (*"anh đang làm việc với hệ thống AI"*); `C-09` là **nhãn nguồn gốc của một artifact đã có** (`ai` / `ai_edited` / `human`). Hai nghĩa khác nhau ⇒ gộp làm mất một trong hai |
| **`AD-4`** | ⛔ **CẤM viết khẳng định tuân thủ** trong copy của component này (*"đã tuân thủ Luật TTNT 2025"*, *"watermark hợp chuẩn"*) — phạm vi khoản 4 Điều 11 là **`TBD`**, và `SRS-NFR-16` (SynthID có thoả nghĩa vụ hay không) cũng là **`TBD`** (`ARC-32`). Component **thực hiện** nghĩa vụ, ⛔ **không tuyên bố** kết quả pháp lý |

### Lô hoãn được (`C-17`…`C-24`) — và một ngoại lệ ⛔ KHÔNG hoãn được

| Mã | Component | Surface | Trạng thái ở run này |
|:--:|---|---|---|
| `C-17` | Dual input: file upload **+** paste text | S-02 | ⏸️ Hoãn (`UC-01` b2 + `ALT-2`) |
| `C-18` | Template picker | S-11 | ⏸️ Hoãn (`UC-08` b4; `SRS-FR-10` — đổi layout template bằng **một click**) |
| `C-19` | Swap / reorder **RỜI RẠC** giữa các ô | S-11 | ⏸️ Hoãn. ⭐ *"**chọn ô**, ⛔ không phải kéo hình học liên tục"* (`BR-004-02`) ⇒ ⛔ **không** sinh nghĩa vụ SC 2.5.7, và **rẻ hơn nhiều so với vẻ ngoài** |
| **`C-20`** ⭐ | **Thao tác kéo trong khung giới hạn** (bubble + đuôi trỏ) | S-10 | ⚠️ **Nghịch lý — đọc [`P-3`](#p-3--mọi-thao-tác-kéo-phải-có-đường-thay-thế-không-kéo-sc-257)**: bản thân `C-20` hoãn được, **đường thay thế KHÔNG-KÉO thì ⛔ KHÔNG** |
| `C-21` | Conflict resolution buộc chọn | S-04 | ⏸️ Hoãn (`UC-02` `EXC-4` — `resolveState()` ⛔ **không được đoán**) |
| `C-22` | Hiển thị **ba số credit tách bạch** | S-14 | ⛔ **NGOÀI HORIZON** (MVP3) |
| `C-23` | API key input (BYOK) | S-16 | ⛔ **NGOÀI HORIZON** (MVP4); ⚠️ cách lưu/bảo vệ key là **`TBD`** (`b-2`) |
| `C-24` | Format availability list (*"chưa có ở mốc này"*) | S-13 | ⏸️ Hoãn (`UC-09` `EF-2` — dùng mức `thông-tin` của `C-01`) |

---

## Ánh xạ shadcn/Radix: dùng nguyên / mở rộng / tự build

> [!CAUTION]
> ⚠️⚠️ **Repo ⛔ CHƯA CÓ một `package.json` nào** — [Foundations](./Foundations.md) §*Tên biến* đã verify tại **2026-08-30** bằng `Glob **/package.json` ⇒ **0 kết quả**. ⇒ ⛔ **Không verify được version, ⛔ không verify được thư viện có component tên gì.**
> ⇒ ⭐ **Cột chuẩn của cả ba bảng dưới là cột *VAI TRÒ HÀNH VI*.** Mọi tên component của thư viện mang nhãn **⚠️ verify khi init** — đọc `components.json` + output thật của bản `init`, ⛔ **không chép từ trí nhớ và trình bày như sự thật đã kiểm**.
> ⚠️ ⭐ **Nhắc lại `HĐ-1`**: shadcn ⛔ **không phải một dependency** — **component code nằm trực tiếp trong repo** ⇒ ta **sở hữu** file. *"Dùng nguyên"* ở đây nghĩa là **⛔ không sửa hành vi**, ⛔ **không** nghĩa là *"import từ node_modules"*.

### A. Dùng nguyên — hành vi a11y đắt tiền đã được trả sẵn

> ⭐ Đây chính là **thứ [ADR-001](../../030-Specs/Architecture/ADR-001-Backend-And-Frontend-Tech-Stack.md) mua shadcn về để có**: focus trap, roving tabindex, ARIA của dialog/popover/select ([Foundations](./Foundations.md) §Chuẩn accessibility lý do **2**). Viết lại chúng bằng tay là **trả tiền hai lần cho cùng một hành vi**.

| Vai trò hành vi (⭐ **cột chuẩn**) | Dùng cho | Ánh xạ dự kiến | Việc của ta |
|---|---|---|---|
| **Modal có focus trap + trả focus về trigger** | `C-07`, và mọi confirm | ⚠️ *Dialog primitive* — **verify khi init** | Chỉ áp token + copy |
| **Modal cảnh báo có nút mặc định là HUỶ** | `C-07` cho hành động phá huỷ | ⚠️ *Alert-dialog primitive* — **verify khi init** | ⛔ Nút xác nhận ⛔ **không** được là nút nhận focus đầu tiên |
| **Lớp nổi tạm định vị theo trigger** (popover, dropdown) | `C-05`, menu hàng của `C-06` | ⚠️ *Popover / dropdown primitive* — **verify khi init** | Áp `--popover` / `--popover-foreground` |
| **Select có bàn phím + ARIA đầy đủ** | `C-05` | ⚠️ *Select primitive* — **verify khi init** | Áp token |
| **Checkbox / radio group có roving tabindex** | `C-14`, control quyết định của gate | ⚠️ *Checkbox / radio-group primitive* — **verify khi init** | ⭐ **Bắt buộc khai `default: none`** — [`P-1`](#p-1--human-gate--không-có-đường-tắt) |
| **Tooltip có thể mở bằng bàn phím** | Chú thích của `C-09`, `C-11` | ⚠️ *Tooltip primitive* — **verify khi init** | ⛔ Tooltip ⛔ **không** được là nơi **duy nhất** chứa thông tin bắt buộc |

### B. Mở rộng — primitive có sẵn, nhưng ngữ nghĩa sản phẩm thêm ràng buộc cứng

| Component | Primitive gần nhất | ⭐ Phần PHẢI thêm — ⛔ không có sẵn trong thư viện |
|---|---|---|
| `C-01` | ⚠️ *Alert* — verify khi init | **Ba mức** với **ba cặp token + ba hình dạng icon + ba nhãn chữ**; ⛔ **cấm** biến thể `dismissible` cho mức `từ-chối` |
| `C-02` | Kế thừa `C-01` mức `từ-chối` | **Lý do cụ thể + đường xử lý + prop lớp lỗi**. ⛔ Không UC nào chấp nhận error message chung chung: *"nêu rõ **mức vượt**"*, *"cần thêm **bao nhiêu** credit"*, *"liệt kê **page nào thiếu gate nào**"*, *"báo rõ **page/panel nào**"* |
| `C-03` | ⚠️ *Badge* — verify khi init | **Danh mục trạng thái nghiệp vụ đóng**; ⭐ **đảo được**: một badge `PASS` (`--success-subtle`) **phải quay về `OPEN` được** mà người dùng ⛔ không làm gì với chính dòng đó (`SDD-HG-01.5`) ⇒ ⛔ **`--success` KHÔNG phải trạng thái cuối** |
| `C-05` | ⚠️ *Form / label / input* — verify khi init | **Provenance mức field** + ⭐ **khoá field sau khi người sửa** (`SDD-HG-01.7`). ⚠️ Story Bible editor là **form + list, ⛔ KHÔNG canvas, ⛔ KHÔNG graph editor** (`BR-004-01`) |
| `C-06` | ⚠️ *Table* (⛔ nhiều khả năng ⛔ không phải Radix) — verify khi init | **State nghiệp vụ theo từng hàng** + **nhảy tới hàng chưa quyết đầu tiên** (`UC-04` `ALT-5`) |
| `C-07` | Dialog ở nhóm **A** | **Nói rõ hệ quả tiền / pháp lý trước khi bấm**: `Regenerate` **hold thêm credit và ⛔ không hoàn lại** |
| `C-08` | — | **Ba biến thể** + **lệnh cấm dữ liệu giả** |
| `C-13` | ⚠️ *Progress* — verify khi init | ⭐ **Tử số + mẫu số + LÝ DO**; ⛔ đơn vị là **giờ-người còn lại**, ⛔ không phải một thanh trang trí |

### C. Tự build — ⛔ không có primitive tương đương

| Component | Vì sao ⛔ không mượn được |
|---|---|
| `C-04` **Long-running job** | Danh mục `job_status` là **danh mục ĐÓNG của DB** (5 giá trị, cưỡng chế bằng `CHECK`), ⛔ không thư viện nào biết nó. Phải **sống được qua reload trang và qua việc rời màn hình rồi quay lại** — job nằm ở server, ⛔ không ở tab trình duyệt (`ARC-16`) |
| `C-09` **Provenance** | Ba giá trị `origin` là **enum của DB**, ⛔ không phải một badge nhị phân |
| `C-10` **AI disclosure** | Là **nghĩa vụ pháp lý**, ⛔ không phải một thành phần trình bày ⇒ ⛔ không được có API cho phép tắt |
| `C-11` **Budget / quota** | Ba khái niệm nghiệp vụ (emphasis quota, `text_budget`, credit hold) chung một pattern **trần rời rạc** |
| `C-12` **Diff ba lối ra** | Mọi picker của thư viện đều là **nhị phân hoặc n-phân KHÔNG có lối ra `unclear`** |
| `C-15` **Public intake shell** | Actor ⛔ **không có tài khoản** ⇒ ⛔ không dùng lại pattern nào của app đã đăng nhập |
| `C-16` **Read-only composite viewer** | Nội dung là **ảnh server-side trả về** — [Foundations](./Foundations.md) §*⛔ Không quản* **#7**: ta sở hữu **khung bao quanh**, ⛔ không sở hữu nội dung bên trong |
| **Bộ control thay thế không-kéo** | [`P-3`](#p-3--mọi-thao-tác-kéo-phải-có-đường-thay-thế-không-kéo-sc-257) — ⛔ không thư viện nào sinh sẵn cặp *"thao tác kéo ↔ đường thay thế tương đương"* |
| **Bảng thông báo `gates_reset[]`** | [`P-1`](#p-1--human-gate--không-có-đường-tắt) — phải **bền**, ⛔ không được tự biến mất |

---

## Ma trận state

### A. State tương tác — áp cho **mọi** control bấm được

| State | Điều kiện | Token / quy tắc |
|---|---|---|
| `default` | — | Theo vai trò: `--primary` (hành động chính) · `--secondary` (thứ cấp) · `--destructive` (phá huỷ) |
| `hover` | Con trỏ ở trên | Bậc nền kề; ⛔ **không** đổi sang một vai trò khác |
| `active` | Đang bấm xuống | Bậc đậm hơn `hover`; ⛔ không dịch chuyển layout |
| `focus-visible` | Nhận focus bằng bàn phím | ⭐ **BẮT BUỘC** vòng focus `--ring` — *"focus nhìn thấy được"* là **quyết định Phase 3** (`G-3`, chuẩn phát biểu ở [Foundations](./Foundations.md) §Chuẩn accessibility). ⛔ **CẤM `outline: none` mà ⛔ không thay bằng vòng khác** |
| `disabled` | ⛔ Không thao tác được | `--muted` / `--muted-foreground`. ⚠️ ⭐ **⛔ Không được dùng `disabled` để thay cho việc GIẢI THÍCH** — nếu nút export bị khoá, người dùng phải đọc được **page nào thiếu gate nào** (`C-02`), ⛔ không phải nhìn một nút xám câm |
| `loading` | Thao tác **tức thời** đang chạy | Chỉ báo trong nút. ⛔ **CẤM dùng cho tác vụ nhiều chục giây** ⇒ dùng `C-04` (`ARC-16`) |
| `read-only` | Hiển thị, ⛔ không sửa | ⛔ **Không** trông giống `disabled` — hai nghĩa khác nhau |

⚠️ **Kích thước đích bấm** của mọi state trên: giữ nguyên ngưỡng và chiều cao control ở [Spacing & Layout](./Spacing-And-Layout.md) §*Kích thước đích bấm* — ⛔ file này ⛔ **không lặp lại con số** (hằng số của chuẩn WCAG 2.2 + **quyết định Phase 3**, ⛔ không phải số của file này).

### B. Trạng thái tiến trình async — phủ ĐÚNG danh mục đóng `job_status`

> ⭐ **`ARC-14` — kiểm được bằng cách đếm.** Một Design System khai `loading / success / error` là **thiếu một trạng thái và mất luôn lớp lỗi**.

| `job_status` | Nghĩa UI | Component | Ghi chú bắt buộc |
|---|---|---|---|
| `queued` | Đã nhận, **chưa chạy** — đang xếp hàng | `C-04` | ⭐ ⛔ **KHÔNG gộp với `running`** — gộp là **giấu thông tin duy nhất giải thích vì sao phải chờ** |
| `running` | Đang chạy | `C-04` | Phải sống được qua **reload** và qua **rời màn hình rồi quay lại** |
| `succeeded` | Xong | `C-04` + `C-03` | — |
| `failed_permanent` | ⭐ Hỏng **⛔ không retry được** | `C-04` + `C-02` | ⛔ **Không** hiển thị nút *"Thử lại"* |
| `failed_exhausted` | ⭐ Hỏng **sau khi đã hết lượt retry** | `C-04` + `C-02` | ⛔ **Hai loại thất bại, ⛔ KHÔNG PHẢI MỘT** — mỗi loại đi kèm **một lớp lỗi**, ⛔ job thất bại ⛔ *"không bao giờ biến mất"* |
| *(⛔ không phải `job_status`)* `đang-làm-mới-trên-nền` | Dữ liệu **đã có trên màn hình**, đang được lấy lại | `C-04` | ⭐ ⛔ **CẤM hiện lại skeleton** ở nhịp này — tách *"tải lần đầu"* khỏi *"làm mới trên nền"*, nếu không UI **nhấp nháy ở mỗi nhịp cập nhật** |

> [!WARNING]
> ⚠️⚠️ **Hai lệnh cấm về con số — đọc kỹ, đây là chỗ dễ bịa nhất:**
> 1. ⛔ **KHÔNG tự điền latency/performance.** `Latency / response time API` và `Thời gian sinh một panel p50/p95` đều là **`TBD`** ([SRS](../../020-Requirements/SRS-Comic-Studio.md) §5.2). Thứ duy nhất nguồn nói là generation *"mất **hàng chục giây**"* — đó là **mô tả định tính, ⛔ không phải chỉ tiêu**. ⇒ Mọi ngưỡng kiểu *"hiện skeleton nếu chậm hơn X"* ở đây là **`TBD`** (`ARC-35`).
> 2. ⭐ ⛔ **KHÔNG hardcode chu kỳ polling như một hằng số thiết kế.** Cơ chế cập nhật là **polling** (`SRS-NFR-06`, độ rắn **MẶC ĐỊNH**), chu kỳ **2 giây** thuộc `ADR-015` `CT-POLL-2S`; Design System ⛔ **không phát minh chu kỳ khác** (`ARC-18`) **và cũng ⛔ không neo giao diện vào nó**. ⚠️ Độ rắn của `D-45` đang **⛔ chưa nhất quán giữa các ADR** (mâu thuẫn `X-1` — PM xác nhận cách đọc) ⇒ ⭐ **mô tả trạng thái theo `job_status`, ⛔ KHÔNG theo chu kỳ cập nhật.** Một component đọc `job_status` sống sót qua mọi lần chu kỳ đó đổi.
> 3. ⛔ **Không đặc tả component dựa trên kết nối đẩy** (`ARC-15`): ⛔ không *"thông báo tức thì khi job xong"*, ⛔ không *"thanh tiến trình chạy mượt"*, ⛔ không *"chấm trạng thái kết nối"*, ⛔ không *"ai đang xem trang này"*.

### C. State nghiệp vụ ⛔ KHÔNG được gộp

| Cặp bị nhầm | Vì sao ⛔ không gộp |
|---|---|
| `từ-chối` **vs** `cảnh-báo` (`C-01`) | `M2-2`: ***"bị từ chối, KHÔNG PHẢI bị cảnh báo"*** — một bên **đã bị chặn**, một bên **đi tiếp được** |
| `chưa xác nhận` **vs** `đã xác nhận` (`C-03`) | ⭐ `chưa xác nhận` là **mặc định của MỌI dòng**; ⛔ *"đã xác nhận"* **⛔ không bao giờ là mặc định** (`SDD-HG-01.1`) |
| `gate 1/2 đã xong` **vs** `sẵn sàng xuất bản` (`C-03`) | `UC-04` `EXC-7`: trạng thái đúng để hiển thị là ***"gate 1/2 đã xong"***, ⛔ **không phải *"đã sẵn sàng xuất bản"*** |
| `blocked-by-gate` **vs** `disable-access` (`C-02`) | ⭐ `403 PROJECT_ACCESS_DISABLED` **phải có bề mặt riêng** (`ARC-26`, `API-HG-13`) — một project bị takedown mà hiện thông báo *"chưa qua gate"* là **nói sai với người dùng** |
| `available` **vs** `hold` (`C-11`) | ⛔ **Không gộp** — *"đó chính là nguồn của cảm giác **có credit mà ⛔ không generate được**"* |
| `ai` **vs** `ai_edited` **vs** `human` (`C-09`) | Nội dung **hỗn hợp** phải đánh dấu đúng bản chất hỗn hợp |
| `rỗng` **vs** `lỗi` (`C-08` vs `C-02`) | *Thà rỗng còn hơn giả* — ⛔ rỗng ⛔ không phải một lỗi cần che |
| `--destructive` **vs** `--danger` | **Hành động của NGƯỜI** (bấm được) **vs** **phán quyết của HỆ THỐNG** (⛔ không bấm được). Gộp ⇒ người dùng **bấm vào một câu thông báo** |

---

## Ba pattern đặc thù sản phẩm

### `P-1` — Human gate: ⛔ KHÔNG có đường tắt

> [!CAUTION]
> ⭐⭐ **Đây là chỗ một quyết định UX *"tiện cho người dùng"* phá một invariant kiến trúc.**
> Nguồn duy nhất: [SDD](../../030-Specs/Architecture/SDD-Comic-Studio.md) §6.3 **`SDD-HG-01`** — ⛔ file này ⛔ **không đặc tả lại** bảy điều khoản, chỉ **hạ chúng xuống thành UI**.
> ⚠️ `M2-4` đo ***"⛔ không tồn tại đường code nào xuất bản page mà chưa qua cả hai gate"***, ⛔ **không** đo sự tồn tại của màn hình gate ⇒ ⭐ **màn hình gate hiển thị đầy đủ mà `M2-4` vẫn FAIL.**

#### ⛔ Lệnh cấm tường minh — ⛔ KHÔNG phải một ghi chú mờ nhạt

| Mã | ⛔ CẤM | Nguồn |
|:--:|---|---|
| **`HG-C1`** | ⛔⛔ **CẤM component *"Duyệt cả trang"* / *"Duyệt tất cả"* / bulk approve / batch approve** dưới **mọi** hình thức | ⭐ **`API-HG-6`** nguyên văn: ***"`#5` là đường DUY NHẤT ghi `PASS`. ⛔ Không endpoint thứ hai, ⛔ không batch, ⛔ không seed/migration/admin tool"*** · `SDD-HG-01.2` |
| **`HG-C2`** | ⛔ **CẤM checkbox *"áp dụng cho các dòng còn lại"*, ⛔ cấm select-all trên danh sách dòng thoại ở màn gate** | `SDD-HG-01.2`; Hệ quả API **#1** |
| **`HG-C3`** | ⛔ **CẤM auto-advance / wizard tự nhảy bước** khi mọi dòng đã được xem | `SDD-HG-01.2` — ⛔ *"không job, ⛔ không cron, ⛔ không cờ cấu hình"* |
| **`HG-C4`** | ⛔ **CẤM toggle *"tự động duyệt khi `speaker_confidence` cao"*** | `SDD-HG-01.2`; `ARC-20` |
| **`HG-C5`** | ⭐⭐ ⛔ **CẤM MỌI CONTROL PRE-SELECTED ở màn gate.** ⛔ Không radio pre-select ứng viên confidence cao nhất, ⛔ không checkbox `defaultChecked`, ⛔ không giá trị khởi tạo nào. **Mọi control trong khối gate PHẢI khai `default: none`** | ⭐ **`SDD-HG-01.1`**: ***"Trạng thái mặc định của mỗi gate là `OPEN`. ⛔ Không tồn tại trạng thái mặc định 'đã xác nhận'"*** |

> ⚠️ ⭐ **Ranh giới tinh tế — ⛔ đừng đọc quá:** hiển thị **đề xuất của LLM là HỢP LỆ** (`UC-04` b3 nói rõ speaker do LLM **đề xuất**). Thứ bị cấm là **đề xuất đó trở thành giá trị mặc định của control quyết định**. Nhìn thấy đề xuất ✅ · control đã chọn sẵn theo đề xuất ⛔.
> ⚠️ **Và ⛔ đừng làm CỨNG HƠN spec:** `UNKNOWN` là giá trị **hợp lệ** ⇒ ⛔ **CẤM luật validate nào chặn `PASS` khi speaker là `UNKNOWN`** (`SDD-HG-01.3`, `ARC-23`). *"PASS nghĩa là **người đã xem**, ⛔ không nghĩa là hệ thống đã biết."* Cờ `speaker_confidence` thấp **phải có**, nhưng nó là **thông tin**, ⛔ không phải một khoá.

#### ✅ Đường HỢP LỆ để giảm giờ-người

Áp lực làm nút *"duyệt cả trang"* là **có thật**: đơn vị đo của một HITL gate là **giờ-người**. Đường hợp lệ ⛔ **không phải** quyết hộ nhiều hàng bằng một cú bấm, mà là **rút ngắn quãng đường tới từng quyết định**:

| ✅ Được | ⛔ Không được |
|---|---|
| `C-06` **nhảy thẳng tới hàng chưa quyết đầu tiên** (`UC-04` `ALT-5`) | Quyết hộ nhiều hàng bằng một thao tác |
| `C-13` đếm **còn N dòng chưa xác nhận** | Ẩn số còn lại để trông như sắp xong |
| Phím tắt **cho từng hàng một** | Phím tắt *"duyệt hết phần còn lại"* |
| Hiện **ngữ cảnh trước/sau** cho câu ngắn / thán từ (`UC-04` `EXC-2`) | Tự gán khi ⛔ không có đề xuất — `UC-04` `EXC-1`: **⛔ không có đường bỏ trống** |

#### Thông báo `gates_reset[]` — ⛔ reset KHÔNG được im lặng

| Điều khoản | Nội dung |
|:--:|---|
| **`HG-R1`** | Reset là **hệ quả tự động**, ⛔ **không phải tuỳ chọn của người dùng** (`SDD-HG-01.5`). Hai trigger: diện tích panel đổi ⇒ reset **mọi dòng bị ảnh hưởng**; sửa `dialogue_rendered` ⇒ reset **đúng một dòng** |
| **`HG-R2`** | ⭐ Phải có một **bề mặt BỀN** liệt kê **gate nào của page/dòng nào vừa bị reset**. ⛔ **CẤM dùng thông báo tự tắt** — mất thông tin ⇒ trên thực tế **vẫn là reset im lặng** (`ARC-22`) |
| **`HG-R3`** | Copy phải nói thẳng điều đã xảy ra: trang vừa **rời trạng thái xuất bản được**. ⛔ Không viết mềm đi |

### `P-2` — Preview và Export là HAI bề mặt riêng

> [!CAUTION]
> ⭐⭐ **⛔ CẤM gộp thành một component *"Render"* dùng chung.**

| | **Preview** (S-12) | **Export** (S-13) |
|---|---|---|
| Bị gate chặn? | ⭐ ⛔ **KHÔNG** — **đúng thiết kế** | ✅ **CÓ** |
| Nguyên văn nguồn | Hệ quả API **#2**: *"Preview ⛔ **KHÔNG bị chặn bởi gate** — người dùng phải preview được **trước** khi gate PASS, **đó chính là cách họ đi tới PASS**"* | `SDD-HG-01.4`: chỉ sinh `export_artifact` khi **MỌI** dòng của **MỌI** panel của **MỌI** page ở `PASS` **CẢ HAI** gate, **VÀ** project ⛔ **không** ở trạng thái disable-access |
| Điều kiện khoá | ⛔ **Không có** | Gate **VÀ** disable-access — **hai nguyên nhân, hai bề mặt lỗi riêng** (`ARC-26`) |
| Hình dạng kỹ thuật | ⭐ **Đồng bộ trong request** (`API-PE-6`) ⇒ ⛔ **không job id, ⛔ không polling, ⛔ không `202`** (`ARC-19`) | Cùng khuôn `API-PE-6` ở horizon này |
| Component | `C-16` + `C-08` (`ô-trống`) | `C-16` + `C-02` + `C-13` |

**⭐ Vì sao gộp là SAI — ⛔ không phải chuyện tổ chức file:**

| # | Lý do |
|:--:|---|
| **1** | ⭐⭐ **Gộp ⇒ một điều kiện khoá dùng chung ⇒ preview bị khoá theo export ⇒ PHÁ CHÍNH ĐƯỜNG NGƯỜI DÙNG ĐI TỚI `PASS`.** Đây là một vòng tự khoá: gate cần người **nhìn thấy trang** mới quyết được, mà thứ cho họ nhìn thấy lại bị chính gate khoá |
| **2** | Hai bề mặt có **hai tập lỗi khác nhau**: preview lỗi là `error + retry` **⛔ không hỏng dữ liệu** (read-only); export lỗi có thể là `blocked-by-gate`, `blocked-by-takedown`, `incomplete-data`, `composite-failed` — và ⛔ **không trả file dở** |
| **3** | ⚠️ ⭐ **Dùng chung compositor ⛔ KHÔNG PHẢI dùng chung bề mặt.** `H4` / `CF-9.1` nói **⛔ không viết renderer thứ hai** — đó là ràng buộc về **implementation của `C-16`**, ⛔ **không** phải giấy phép gộp hai màn hình. `C-16` **spec một lần, dùng ở hai bề mặt có điều kiện vào khác nhau** |
| **4** | ⭐ `preview ≠ publishable` (`UC-08` b13, `M2-4`): **preview ⛔ KHÔNG mở đường xuất bản** ⇒ hai trạng thái này **phải phân biệt được trên UI**. Gộp component là xoá đúng sự phân biệt đó |

> [!WARNING]
> ⚠️ ⭐ **UI PHẢN ÁNH, SERVER CƯỠNG CHẾ** (`ARC-24`). Design System ⛔ **KHÔNG được** trình bày *"ẩn/disable nút export"* như **biện pháp bảo đảm**. Điểm cưỡng chế nằm ở **tầng service + trigger DB**; nút bị khoá ở UI chỉ là **phản ánh**. ⭐ Threat Model: *"**Export CHÍNH LÀ đường bypass** nếu nó ⛔ không kiểm hai gate"*.
> ⇒ Khi export bị khoá, `C-02` phải **liệt kê page nào thiếu gate nào** và **điều hướng về `UC-04`/`UC-05`** — ⛔ không có cờ *"export nháp"*, ⛔ không *"bỏ qua kiểm tra"*, ⛔ **không quyền admin nào vượt được** (⛔ không `force`, ⛔ không `skip_gates`, ⛔ không `admin_override`).

### `P-3` — Mọi thao tác kéo phải có ĐƯỜNG THAY THẾ KHÔNG-KÉO (SC 2.5.7)

> [!CAUTION]
> ⭐⭐ **Đây là UI THẬT và effort THẬT, ⛔ KHÔNG PHẢI một dòng CSS.**
> **Ràng buộc gốc:** WCAG 2.2 SC **2.5.7** *Dragging Movements* — **quyết định Phase 3**, chốt tại gate **`G-3`**; chuẩn phát biểu ở **đúng một chỗ**: [Foundations](./Foundations.md) §*Chuẩn accessibility*. ⛔ File này ⛔ không phát biểu lại chuẩn, chỉ **thiết kế control**.
> **Bề mặt sinh nghĩa vụ:** S-10 — `C-20` **kéo bubble** và **kéo đuôi trỏ** (`SRS-FR-16`, độ rắn **CHỐT**: *"heuristic **+** cho user **kéo tay**"*; [MVP-Scope](../../010-Planning/MVP-Scope.md) §5.2 thành phần **#2**).

#### ⚠️ Nghịch lý phải ghi rõ, ⛔ không lờ đi

> ⭐ `C-20` nằm ở **lô hoãn được** của BA (dùng ở **1** surface) — **nhưng đường thay thế không-kéo thì ⛔ KHÔNG hoãn được**, vì nó là **điều kiện của một chuẩn đã cam kết** (`G-3`), ⛔ không phải một tính năng tiện ích.
> ⇒ **Quy tắc phát hành, phát biểu thành câu kiểm được:** ***đường thay thế không-kéo là ĐIỀU KIỆN PHÁT HÀNH của `C-20`, ⛔ KHÔNG phải một hạng mục xếp sau.*** Hai thứ **vào cùng một increment** hoặc **⛔ không thứ nào vào cả**.
> ⚠️ **Vì sao ⛔ không thể tách:** nếu `C-20` ship trước và đường thay thế xếp sau, sản phẩm **đã vi phạm chuẩn ngay tại lần ship đó** — và món nợ này ⛔ không có deadline pháp lý ép trả, nên nó sẽ **⛔ không bao giờ được trả**.
> ⚠️ **Điểm ⛔ không bị nghịch lý:** `C-19` (swap/reorder trang) là thao tác **RỜI RẠC** — *"chọn ô"*, ⛔ **không phải kéo hình học liên tục** ⇒ nó ⛔ **không** sinh nghĩa vụ SC 2.5.7.

#### Đặc tả control thay thế — bốn đường, tất cả ⛔ đều KHÔNG cần kéo

| Mã | Control | Hành vi |
|:--:|---|---|
| **`DR-1`** | ⭐ **Chọn đối tượng bằng bàn phím** | Mỗi bubble và mỗi đuôi trỏ trong panel là **một item focus được**, có **accessible name** (ví dụ: *"bubble của <nhân vật>, dòng 2"*). ⛔ Không đối tượng nào **chỉ** chạm tới được bằng con trỏ |
| **`DR-2`** | ⭐ **Nudge bằng phím mũi tên** | Mũi tên = **một bước nhỏ**; `Shift` + mũi tên = **một bước lớn**. ⚠️ Đơn vị bước là **phân số của cạnh panel** (bước nhỏ = **1/100**, bước lớn = **1/10** — *quyết định Phase 3*), ⛔ **KHÔNG phải px**: hình học bubble là **toạ độ chuẩn hoá 0–1** ([Spacing & Layout](./Spacing-And-Layout.md) §*Ranh giới*) |
| **`DR-3`** | ⭐ **Nhập toạ độ trực tiếp** | Ô numeric cho `x`, `y` trong hệ **0–1** của panel, và một ô cho **điểm neo của đuôi trỏ**. Đây là đường **tương đương đầy đủ**: bất kỳ vị trí nào đạt được bằng thao tác kéo **đều đạt được bằng cách nhập số** |
| **`DR-4`** | **Nút nudge bấm được** | Bốn nút hướng, dùng lại bước của `DR-2` — dành cho người dùng con trỏ **⛔ không thao tác kéo được** (SC 2.5.7 áp cho **con trỏ**, ⛔ không chỉ cảm ứng) |

#### Ràng buộc chung của cả bốn đường

| # | Ràng buộc |
|:--:|---|
| **1** | ⭐ **Cùng một luật giới hạn khung**: kéo hay ⛔ không kéo, vị trí đều bị **giới hạn trong khung panel đang mở** (`UC-07` `EX-5`) — ⛔ **KHÔNG** infinite canvas |
| **2** | ⭐ **Cùng một cảnh báo**: đè ra ngoài `text_safe_zone` / che mặt ⇒ `C-01` mức **`cảnh-báo`** (`M2-3` — actor **có quyền chấp nhận có ý thức**), ⛔ **không** phải mức `từ-chối` |
| **3** | **Cùng một undo**: undo **cục bộ** trong panel. ⛔ **KHÔNG** undo qua generation — thao tác đó bị **từ chối** kèm lý do (`UC-07` `EX-3`) |
| **4** | ⛔ **CẤM chôn đường thay thế sau một menu *"nâng cao"*** — nó phải nằm **cùng thanh công cụ** với thao tác kéo. *Quyết định Phase 3.* Một đường thay thế mà ⛔ không ai tìm thấy thì tương đương ⛔ không có |
| **5** | ⛔ **CẤM viện dẫn ngoại lệ *"kéo là thiết yếu"*** để bỏ `DR-1`…`DR-4`. ⚠️ Số hiệu SC và các ngoại lệ **phải mở đúng văn bản chuẩn khi audit** — bảng ở [Foundations](./Foundations.md) là **bảng tra nhanh**, ⛔ không thay văn bản chuẩn |
| **6** | ⛔ **CẤM đường thay thế yêu cầu độ chính xác cao hơn** thao tác kéo (ví dụ: bắt gõ số có nhiều chữ số thập phân mới đặt được bubble vào chỗ hợp lý) |

---

## ⛔ Component KHÔNG được đặc tả ở run này

> [!CAUTION]
> ⭐⭐ **Mục này là lệnh cấm, ⛔ KHÔNG phải danh sách "chưa làm".** Vài mục dưới đây là thứ *"một dev sẽ làm ngược theo bản năng"* — và làm ngược thì **phá một requirement CHỐT hoặc một miễn trừ pháp lý**.

| # | ⛔ CẤM | Nguồn | Vì sao |
|:--:|---|---|---|
| **1** | **Tree view / diff view / branch-merge của generation** | `SRS-NFR-23` (**CHỐT**), `D6` **cắt hẳn** | Flat list theo `created_at` + `approved_generation_id` là **đủ**. ⚠️ ⭐ **Cắt UI, ⛔ KHÔNG cắt cột dữ liệu** — `parent_generation_id` **vẫn bắt buộc** (`CẤM-09`). Và ⛔ **không được suy ra một *"history panel"*** từ nghĩa vụ ghi `change_log`: repo bắt buộc **GHI** một row cho mọi hành động, ⛔ **không** bắt buộc **HIỂN THỊ** nó |
| **2** | ⭐ **Layout Score — hay BẤT KỲ hiển thị điểm số layout nào** | `SRS-NFR-22` (**CHỐT**), `C4` = ❌ ở **mọi** cột kể cả Full Scope | ⛔ ***"Không có điểm số thực nào được tính, hiển thị hay lưu"***. **Cắt cơ chế, GIỮ mục tiêu** (layout theo narrative importance ⇒ `SRS-FR-09`). ⇒ `UC-08` `EX-4`: yêu cầu điểm số layout bị **từ chối**. ⛔ Không thanh điểm, ⛔ không sao, ⛔ không nhãn *"bố cục tốt/khá"* |
| **3** | **Inpainting brush / drawing tools** | `D5` hoãn (`UC-07` `EX-4`) | Sửa pixel ⇒ ⛔ **không có công cụ nào làm được**; UI phải **từ chối và nói rõ lý do** |
| **4** | **Infinite canvas / zoom-pan cấp chapter / hình học tự do / xoay / chồng lấn** | `D2` hoãn (`UC-07` `EX-5`, `UC-08` `EX-3`) | *"Canvas bị **giới hạn trong một khung**"* — [xem `P-3` ràng buộc 1](#ràng-buộc-chung-của-cả-bốn-đường) |
| **5** | ⭐⭐ **MỌI dashboard *"nội dung khả nghi"* / copyright detection** | `SRS-NFR-15` (**CHỐT**, **anti-feature**); `ARC-28` | ⭐ **Nó PHÁ MIỄN TRỪ Điều 198b.** Điều kiện **(a)** của miễn trừ là ***"không biết"*** ⇒ xây bộ phát hiện là **tự tạo ra đúng cái tri thức mà luật đang miễn trừ cho việc KHÔNG CÓ**. ⇒ ⛔ **Cấm cụ thể**: badge *"đã kiểm bản quyền"* · icon `shield` / `verified` **mang nghĩa bản quyền** · nhãn *"nội dung gốc"* gắn lên tác phẩm · thang màu *"độ tương đồng"* · cảnh báo *"phát hiện nội dung tương đồng"*. ⚠️ Một đề xuất như vậy là ***"VI PHẠM một requirement CHỐT, ⛔ không phải một cải tiến"*** ⇒ **từ chối tại review, ⛔ không thương lượng phạm vi** |
| **6** | **Danh mục kiểu bubble cụ thể** | **`TBD`** tường minh (`UC-07` b6) | Nguồn chỉ ghi *"chọn kiểu"*; ⛔ **danh mục chưa được định nghĩa ở đâu trong repo** (SFX / narration box / caption cũng `TBD`) ⇒ `C-05` khai **một control chọn kiểu với danh mục rỗng chờ nguồn**, ⛔ **không tự đặt tên kiểu nào** |
| **7** | **Màn hình counter-notice** | **`TBD`** — thủ tục chưa có (`UC-11` `AF-1`) | *"UC này ⛔ **KHÔNG phát minh thời hạn hay bước phục hồi**"* ⇒ ⛔ không có gì để thiết kế |
| **8** | ⭐ **MỌI component của bề mặt operator** (S-19) | ⚠️ **Mô hình quyền ⛔ CHƯA TỒN TẠI** | ⭐ [SDD](../../030-Specs/Architecture/SDD-Comic-Studio.md) §7.4 khai **bốn** danh tính kết nối DB (`app_api`, `app_worker`, `app_public_intake`, owner/migration) và ghi rõ: ***"cần role THỨ NĂM `app_operator`, và ⛔ nó CHƯA được thêm vào đây"***; hai endpoint admin takedown (`TD-2`/`TD-3`) ***"VẪN BỊ CHẶN"***, cơ chế uỷ quyền operator là **`TD-Q1`** — ⛔ **CHƯA CÓ**. ⇒ ⭐ **Thiết kế UI cho một mô hình quyền chưa có là xây trên nền chưa đổ**: mọi giả định về *ai thấy được gì* sẽ phải vẽ lại khi role thứ năm được chốt. ⚠️ **Bề mặt CÔNG KHAI `TD-1` thì đã CHỐT** ⇒ `C-15` **được** đặc tả — hai thứ này ⛔ **không** cùng một bề mặt |

> [!WARNING]
> ⚠️ ⭐ **RANH GIỚI ⛔ KHÔNG ĐƯỢC ĐỌC QUÁ — sai theo chiều ngược lại cũng là sai.**
> `SRS-NFR-15` cấm **phát hiện tương đồng nội dung**. Nó ⛔ **KHÔNG** cấm: rate limit · kiểm kích thước file · kiểm định dạng · log truy cập · `provider_refusal_log`.
> ⇒ ✅ **Design System VẪN được** khai trạng thái *file sai định dạng*, *rỗng sau `text clean`*, *vượt hạn mức*, *provider từ chối*.
> ⇒ ✅ **VẪN được** khai component cho kết quả ingest check — **nhưng phải phát biểu đúng ngữ nghĩa**: ***"phát hiện opt-out signal do CHỦ SỞ HỮU QUYỀN gắn vào file"*** (một **dữ kiện khách quan**), ⛔ **không** đặt tên hay viết copy thành *"kiểm tra vi phạm"* (`ARC-29`). ⭐ **Đọc nhãn ⛔ không tạo ra tri thức suy đoán** — được phép; **suy đoán** thì ⛔ không. Tên component sai ngữ nghĩa ⇒ **bị cờ dù chức năng đúng**.

---

## Tài liệu tham khảo

> ⚠️ **Ghi nhận minh bạch (`X-3`)**: tại **2026-08-30**, các tài liệu neo bên dưới (`SRS`, `SDD`, `ADR-001`, `ADR-013`, `MVP-Scope`) đều ở `status: draft`, và repo ⛔ **chưa có `package.json`** ⇒ mọi ánh xạ thư viện ở đây **chưa verify được bằng code thật**.

**Trong Design System** *(⭐ bốn file dưới **sở hữu giá trị**; file này chỉ **tham chiếu tên token**)*:

- [Foundations](./Foundations.md) — §*Hợp đồng phát biểu token* (`HĐ-1`…`HĐ-3`, `L1`…`L4`) · §*Chuẩn accessibility* (**chỗ DUY NHẤT** phát biểu chuẩn) · §*Cách kiểm* (`K-1`…`K-14`)
- [Color Tokens](./Color-Tokens.md) — §*Semantic mapping* · §*Màu trạng thái: BA MỨC* (nguồn của `--danger*` / `--warning*` / `--info*`) · `--destructive` vs `--danger` · `--canvas` · `--ring`
- [Typography](./Typography.md) — §*HAI HỆ FONT* (font UI **≠** font render) · §*Vai trò → token* (`--text-*`, `--leading-*`, `--font-weight-*`) · cỡ chữ bubble là **hàm của `text_budget`**, công thức là **`TBD` có chủ**
- [Spacing & Layout](./Spacing-And-Layout.md) — §*Thang spacing* (`--space-*`) · §*Kích thước đích bấm* · §*Ranh giới: hệ này ⛔ không quản hình học panel/bubble* (toạ độ **0–1**)
- [Brand Guidelines](./Brand-Guidelines.md) — §*Điều CẤM* · §*Bề mặt takedown công khai* (quy tắc brand của `C-15`)

**Ngoài Design System**:

- [Design MOC](../Design-MOC.md) — bản đồ tầng 040
- [SRS — Comic Studio](../../020-Requirements/SRS-Comic-Studio.md) — §3.D (`SRS-FR-10`, `SRS-FR-12`, `SRS-FR-16`, `SRS-NFR-06`) · `SRS-FR-14`, `SRS-FR-21`, `SRS-FR-22`, `SRS-FR-36`, `SRS-FR-39`, `SRS-FR-40`, `SRS-FR-41` · `SRS-NFR-15`, `SRS-NFR-22`, `SRS-NFR-23` · §5.1 · §5.2
- [SDD — Comic Studio](../../030-Specs/Architecture/SDD-Comic-Studio.md) — ⭐ §6.3 **`SDD-HG-01`** (`.1`…`.7`, **nguồn duy nhất**) · §7.4 (bốn role DB + nợ `app_operator`)
- [ADR-001 — Backend & Frontend Tech Stack](../../030-Specs/Architecture/ADR-001-Backend-And-Frontend-Tech-Stack.md) — bảng *Tầng MẶC ĐỊNH* hàng **Frontend & UI** *(⚠️ ⛔ không phải nguồn của tên biến hay tên component — mâu thuẫn `X-2`)*
- [ADR-013 — Typeset Layer Separate From Art](../../030-Specs/Architecture/ADR-013-Typeset-Layer-Separate-From-Art.md) — §Decision **2** (toạ độ 0–1), **5** (`dialogue_source` bất biến), **8** (một compositor), **9** (hai trigger reset gate)
- [MVP Scope](../../010-Planning/MVP-Scope.md) — §5.2 (**năm thành phần bắt buộc** + ràng buộc `change_log` xuyên suốt) · §5.3 (bốn thành phần hoãn)

**Hồ sơ quyết định của run** (`2026-08-30-brand-guidelines-va-design-system-comic-studio`):

- [findings/business-analyst.md](../../010-Planning/pm-runs/2026-08-30-brand-guidelines-va-design-system-comic-studio/findings/business-analyst.md) — ⭐⭐ §1.1–1.2 (bề mặt S-01…S-19, X-1…X-6) · §1.3 (**12 nhóm màn hình**) · §2.1 (`C-01`…`C-13`) · §2.2 (`C-14`…`C-16`) · §2.3 (lô hoãn + **danh sách CẤM**)
- [findings/architect.md](../../010-Planning/pm-runs/2026-08-30-brand-guidelines-va-design-system-comic-studio/findings/architect.md) — ⭐ vùng **C** (`ARC-14`…`ARC-19`, danh mục `job_status`) · vùng **D** (`ARC-20`…`ARC-27`, human gate) · vùng **E** (`ARC-28`…`ARC-33`, anti-feature + AI disclosure) · §7 mâu thuẫn `X-1`, `X-2`, `X-3` · §8 nợ kỹ thuật chạm UI
- [run-plan.md](../../010-Planning/pm-runs/2026-08-30-brand-guidelines-va-design-system-comic-studio/run-plan.md) — gate `G-3` (chuẩn a11y)
- [escalations.md](../../010-Planning/pm-runs/2026-08-30-brand-guidelines-va-design-system-comic-studio/escalations.md) — `E2` (độc giả đích) · `E4` (takedown) · `E5` (operator ngoài scope)
- [RULE-001 — Documents Template](../../../knowledge-base/99-Templates/Documents-Template.md) — quy tắc **#5** (⛔ không wiki-link)
