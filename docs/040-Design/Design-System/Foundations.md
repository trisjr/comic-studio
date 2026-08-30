---
id: DS-002
type: design-system
status: draft
project: comic-studio
owner: "@trisjr"
tags: [design-system, phase-3]
created: 2026-08-30
updated: 2026-08-30
---

# Foundations

> **Part of:** [Design MOC](../Design-MOC.md)
> **Implements:** [ADR-001 — Backend & Frontend Tech Stack](../../030-Specs/Architecture/ADR-001-Backend-And-Frontend-Tech-Stack.md) §Decision điều **5**, **6** + bảng *Tầng MẶC ĐỊNH* hàng **Frontend & UI**
> **Nguồn quyết định:** `G-2` (light/dark) và `G-3` (accessibility) — chốt tại gate run `2026-08-30-brand-guidelines-va-design-system-comic-studio`.

> [!IMPORTANT]
> ⭐ **Đây là file phải đọc TRƯỚC bốn file còn lại của Design System.** Nó ⛔ **không chứa một giá trị nào** — nó chứa **luật chơi**: token được phát biểu ở đâu, ai phụ thuộc ai, chuẩn a11y là gì, và [kiểm bằng cách nào](#cách-kiểm-checklist-cơ-học).
> **Độc giả đích là AI assist sinh code** (`E2` của run) ⇒ ưu tiên **quy tắc kiểm được bằng grep** hơn văn xuôi triết lý thiết kế.

## Mục lục

- [Hệ thống này quản cái gì / ⛔ KHÔNG quản cái gì](#hệ-thống-này-quản-cái-gì---không-quản-cái-gì)
- [Kiến trúc token: primitive → semantic](#kiến-trúc-token-primitive--semantic)
- [Hợp đồng phát biểu token](#hợp-đồng-phát-biểu-token)
- [Chiến lược light/dark](#chiến-lược-lightdark)
- [Chuẩn accessibility](#chuẩn-accessibility)
- [Cách kiểm (checklist cơ học)](#cách-kiểm-checklist-cơ-học)
- [Tài liệu tham khảo](#tài-liệu-tham-khảo)

---

## Hệ thống này quản cái gì / ⛔ KHÔNG quản cái gì

### ✅ Quản

| Hạng mục | Phát biểu ở |
|---|---|
| Hai tầng token và luật hình dạng của chúng | [Kiến trúc token](#kiến-trúc-token-primitive--semantic) |
| ⭐ Chiều phụ thuộc giữa CSS variable và Tailwind | [Hợp đồng phát biểu token](#hợp-đồng-phát-biểu-token) |
| **Hình dạng file** mà bốn file lô sau bắt buộc phải có | [Hợp đồng phát biểu token](#hợp-đồng-phát-biểu-token) |
| Chiến lược light/dark của toàn hệ | [Chiến lược light/dark](#chiến-lược-lightdark) |
| ⭐ **Chuẩn accessibility — đây là chỗ DUY NHẤT phát biểu chuẩn** | [Chuẩn accessibility](#chuẩn-accessibility) |
| Checklist nghiệm thu cơ học cho cả tầng `docs/040-Design/Design-System/` | [Cách kiểm](#cách-kiểm-checklist-cơ-học) |

### ⛔ KHÔNG quản

| # | ⛔ Không quản | Ai sở hữu · trạng thái |
|:--:|---|---|
| **1** | ⭐⭐ **Hình học panel / bubble** — vị trí, kích thước, tỉ lệ của panel và bubble trong trang truyện | Layout là **toạ độ chuẩn hoá 0–1** trong `page_layout JSONB` — [ADR-013](../../030-Specs/Architecture/ADR-013-Typeset-Layer-Separate-From-Art.md) §Decision **2** · [MVP-Scope](../../010-Planning/MVP-Scope.md) §4.1 · [SRS](../../020-Requirements/SRS-Comic-Studio.md) §3.D ràng buộc **2**. ⇒ Design System sở hữu **chrome của editor**, ⛔ **không** sở hữu hình học nội dung. ⚠️ Nhầm chỗ này là **sinh token spacing cho thứ ⛔ không được đo bằng spacing** |
| **2** | ⭐⭐ **Font sẽ render vào ảnh** (họ font, glyph coverage tiếng Việt, fallback stack) | ⚠️ Là **`TBD` do [ADR-013](../../030-Specs/Architecture/ADR-013-Typeset-Layer-Separate-From-Art.md) sở hữu** — chủ: **Architect + Founder**, thời điểm: **sau MVP0, trước gate `G1-e`**. [Typography](./Typography.md) *(lô sau)* chỉ được **ghi lại ràng buộc**, ⛔ **không chọn font**, ⛔ không viết fallback stack. ⛔ File này ⛔ không gợi ý tên font nào |
| **3** | Giá trị cụ thể của màu · chữ · spacing · component | [Color Tokens](./Color-Tokens.md) · [Typography](./Typography.md) · [Spacing & Layout](./Spacing-And-Layout.md) · [Components](./Components.md) — *cả bốn thuộc lô sau, link có chủ ý* |
| **4** | Tên hiển thị · logo · wordmark · tone of voice | [Brand Guidelines](./Brand-Guidelines.md) — tên hiển thị là **`TBD` có chủ (Founder)** |
| **5** | **i18n / l10n strategy** (locale switching, RTL, plural rules) | [SRS](../../020-Requirements/SRS-Comic-Studio.md) §5.2 hàng `b-6` = **`TBD`**; [ADR-001](../../030-Specs/Architecture/ADR-001-Backend-And-Frontend-Tech-Stack.md) bảng `TBD` ghi rõ ADR đó *"đóng việc CHỌN ngôn ngữ/framework, ⛔ **KHÔNG** đóng"* hàng này. ⛔ Design System không khai chiến lược i18n |
| **6** | Mọi **NFR có đơn vị** chưa có số trong repo (latency, uptime, rate limit, dung lượng upload, TTL signed URL) | ⛔ **Không tự điền.** Bịa một con số performance là lỗi **nghiêm trọng hơn** để trống nó — con số bịa sẽ được tầng design và tầng QA dùng làm **chuẩn nghiệm thu** ([SRS](../../020-Requirements/SRS-Comic-Studio.md) §5.2) |
| **7** | **Nội dung bên trong preview trang/chapter** | Preview là **ảnh server-side trả về, read-only** ([MVP-Scope](../../010-Planning/MVP-Scope.md) §5.2 thành phần **#4**). Design System sở hữu **khung bao quanh** (toolbar, zoom, trạng thái loading), ⛔ không sở hữu nội dung bên trong |

---

## Kiến trúc token: primitive → semantic

> **Nhãn: toàn bộ mục này là *quyết định Phase 3*.** Repo ⛔ không có tầng token nào trước đó — `docs/040-Design/` rỗng hoàn toàn tại 2026-08-30.

**Hai tầng, một chiều:**

| Tầng | Là gì | Ai được đọc |
|---|---|---|
| **primitive** | Giá trị thô, ⛔ **không mang nghĩa sử dụng**: thang màu, thang spacing, thang cỡ chữ, thang radius | **Chỉ** tầng semantic |
| **semantic** | **Vai trò sử dụng**: nền cấp gốc, bề mặt nổi, nhấn chính, viền, vòng focus, nền cảnh báo… | Component code |

⛔ **Component ⛔ KHÔNG được tiêu thụ trực tiếp primitive.** Dừng ở tầng primitive là dừng **đúng một tầng trước** chỗ code cần.

### Bốn luật hình dạng — áp cho cả bốn file lô sau

| Mã | Luật | Hỏng thế nào nếu vi phạm |
|:--:|---|---|
| **L1** | ⭐ Mỗi semantic token **nền** **PHẢI** có một token **chữ** đi kèm (quy ước cặp `-foreground`) | Thiếu cặp ⇒ **mọi phép kiểm contrast phải làm lại bằng tay ở từng chỗ dùng**. Đây là bẫy đặc trưng nhất khi mang style từ công cụ thiết kế sang: style thường chỉ có fill |
| **L2** | ⭐⭐ Mỗi semantic token **PHẢI** có **đúng hai giá trị**: light **và** dark. ⛔ **Không tồn tại token chỉ có ở một mode** | Retrofit dark = đi tìm mọi hex đã lỡ hardcode. Xem [Chiến lược light/dark](#chiến-lược-lightdark) |
| **L3** | Đặt tên theo **vai trò**, ⛔ **không theo bảng màu** (`Blue/500`, `Gray/900`) | Code cần token **ngữ nghĩa**; tên theo bảng màu buộc mọi chỗ dùng phải tự quyết nghĩa |
| **L4** | Elevation dùng **thang cố định**; spacing **phải rơi vào thang** | Shadow tuỳ ý ⇒ mỗi layer một arbitrary value. Gap ⛔ không rơi vào thang ⇒ `p-[13px]` ⇒ **token chết ngay tại chỗ dùng** |

---

## Hợp đồng phát biểu token

> [!IMPORTANT]
> ⭐⭐ **MỘT CHIỀU PHỤ THUỘC — ⛔ KHÔNG ĐỐI XỨNG:**
> **CSS variable là NGUỒN. Tailwind theme chỉ THAM CHIẾU vào nó.**

### Ba điều khoản

| Mã | Điều khoản |
|:--:|---|
| **HĐ-1** | **Nguồn duy nhất** của mọi giá trị token là block CSS variable trong `apps/web/src/index.css`: `:root {}` cho light, `.dark {}` cho dark |
| **HĐ-2** | `tailwind.config.ts` **chỉ được** `theme.extend` **trỏ vào** `var(--…)`. ⛔ **CẤM hardcode hex trong `tailwind.config`** — đó là **nguồn sự thật thứ hai** |
| **HĐ-3** | Component **chỉ** đọc token **semantic**. ⛔ Không đọc primitive, ⛔ không dùng arbitrary value cho màu |

### ⭐ Vì sao một chiều — bốn lý do, mỗi lý do đủ để chốt

| # | Lý do |
|:--:|---|
| **1** | ⭐⭐ **shadcn ⛔ KHÔNG phải một dependency.** [ADR-001](../../030-Specs/Architecture/ADR-001-Backend-And-Frontend-Tech-Stack.md) bảng *Tầng MẶC ĐỊNH*, hàng **Frontend & UI**, ghi nguyên văn: *"component code nằm **trực tiếp trong repo**, không vendor lock-in và **tối ưu cho AI assist (`R1`)**"*. ⇒ Ta **sở hữu** file component. Token lệch quy ước thì ⛔ không có ai upstream sửa hộ — **phải sửa tay từng file**, tức **mất đúng lợi thế `R1` mà ADR-001 mua shadcn về** |
| **2** | shadcn có **tập biến ngữ nghĩa quy ước sẵn** mà component code đọc thẳng. Nếu Design System đặt tên riêng rồi ⛔ không map, mỗi component phải sửa tay ở mọi chỗ dùng — nhân với **1 dev, ⛔ không code review** (`R1`) |
| **3** | Dark mode trong quy ước shadcn là **override CÙNG bộ biến dưới một selector**, ⛔ không phải một palette thứ hai ⇒ đó chính là nguồn của luật **L2** |
| **4** | ⭐ **Repo đã có tiền lệ đúng khuôn này ở tầng hợp đồng API**: [ADR-001](../../030-Specs/Architecture/ADR-001-Backend-And-Frontend-Tech-Stack.md) §Decision **điều 6** — *"Một `packages/contracts` là nguồn sự thật của hợp đồng API… ⛔ Không khai báo kiểu request/response hai lần"*. Hợp đồng token ở đây là **cùng khuôn**, áp cho tầng trình bày: một nguồn, các tầng khác **tham chiếu**, ⛔ không khai hai lần |

⚠️ **Ghi trước cho lô dark (⛔ đừng phát hiện muộn)**: [ADR-001](../../030-Specs/Architecture/ADR-001-Backend-And-Frontend-Tech-Stack.md) §Decision **điều 5** chốt *"Frontend là SPA thuần, ⛔ không SSR, ⛔ không server action"* ⇒ ⛔ **không có FOUC do server render sai theme**. **Nhưng** khi dark thật sự ship, nếu theme được đọc từ `localStorage` **sau** paint thì vẫn có flash ⇒ cần một **script chặn nhỏ trong `index.html`**. Ở MVP chỉ có light ⇒ ⛔ chưa cần; ghi ở đây để lô dark ⛔ không phải tự phát hiện lại.

### ⛔ Tên biến — vùng ảo giác nguy hiểm nhất của cả run

> [!CAUTION]
> ⛔⛔ **Danh sách tên biến dưới đây là *QUYẾT ĐỊNH PHASE 3*. Nó ⛔ KHÔNG phải nội dung của `ADR-001`.**
> `ADR-001` chốt *"dùng **shadcn/ui + Tailwind CSS**"* và ⛔ **KHÔNG nêu một tên biến CSS nào** — đã đọc toàn văn §Decision. Trích `ADR-001` làm nguồn cho tên biến là **gieo một neo giả vào tầng 040** (mâu thuẫn `X-2`, đã bị lens `architect` bắt trong bản nháp của PM).
> ⚠️ **Tên biến là quy ước của thư viện shadcn và thay đổi theo version.** Repo hiện ⛔ **chưa có một `package.json` nào** — đã verify tại 2026-08-30 bằng `Glob **/package.json` ⇒ **0 kết quả** ⇒ ⛔ **không verify được version**.
> ⇒ ⭐ **Cột chuẩn của bảng dưới là cột VAI TRÒ.** Tên chính xác **PHẢI verify khi khởi tạo dự án** (đọc `components.json` + file CSS do bản `init` thật sinh ra), ⛔ **không chép từ trí nhớ và trình bày như sự thật đã kiểm**.

| Vai trò (⭐ **đây mới là phần chuẩn**) | Tên quy ước dự kiến | Bắt buộc có cặp chữ (**L1**) |
|---|---|:--:|
| Nền cấp gốc của app shell | `--background` — *quyết định Phase 3, ⚠️ cần verify* | ✅ `--foreground` |
| **Nhấn chính** — hành động chính; ⭐ **nguồn là accent thương hiệu** ([Brand Guidelines](./Brand-Guidelines.md)) | `--primary` — *quyết định Phase 3, ⚠️ cần verify* | ✅ (cặp `-foreground` tương ứng) |
| Bề mặt nổi của chrome (card, popover, panel công cụ) | ⚠️ **Tên: verify khi init** | ✅ |
| Nền hành động **thứ cấp** | ⚠️ **Tên: verify khi init** | ✅ |
| Nền **trầm** cho text phụ / trạng thái disabled | ⚠️ **Tên: verify khi init** | ✅ |
| Nền hành động **phá huỷ** (xoá, reset) | ⚠️ **Tên: verify khi init** | ✅ |
| **Viền** chung và viền của input | ⚠️ **Tên: verify khi init** | ⛔ Không (⛔ không phải nền) |
| **Vòng focus** | ⚠️ **Tên: verify khi init** | ⛔ Không |

⚠️ **Bộ quy ước ⛔ không phủ hết nhu cầu của sản phẩm này.** Ví dụ đã biết: hệ **alert ba mức** xuất hiện ở **13 surface**. Token cho các mức đó là **bổ sung của dự án** ⇒ khai ở [Color Tokens](./Color-Tokens.md) *(lô sau)* kèm nhãn **quyết định Phase 3**, và **vẫn phải thoả L1 + L2**.

### ⭐ Hình dạng file bắt buộc cho lô sau

Repo ⛔ **chưa có dòng code nào** (verify: **0** `package.json`). ⇒ Cách **duy nhất** để tầng token ⛔ không thành tài liệu chết là phát biểu nó dưới **đúng hình dạng file mà code sẽ có**:

| Bắt buộc | Ở đâu |
|---|---|
| Một block `:root {}` + `.dark {}` **copy-paste được** vào `apps/web/src/index.css` | [Color Tokens](./Color-Tokens.md) *(lô sau)* |
| Một block `theme.extend` **copy-paste được** vào `tailwind.config.ts`, chỉ chứa `var(--…)` | [Color Tokens](./Color-Tokens.md) *(lô sau)* |

⛔ **Không phải một bảng hex trong markdown.** Đây là khác biệt giữa một Design System **dùng được** và một Design System **được đọc một lần** — và nó khớp với `E2`: **độc giả đích là AI assist sinh code**.

---

## Chiến lược light/dark

> **`G-2` — chốt tại gate:** **Light là default; token khai ĐỦ CẶP light/dark ngay.** Dark ⛔ **chưa implement ở MVP**.

**Vì sao light là default** — ⛔ không phải khẩu vị: **preview trang comic có nền trắng giấy**. Đặt trang trắng lên chrome tối làm **lệch chính cảm nhận độ sáng/tương phản của tấm ảnh người dùng đang đánh giá** — mà họ đang đánh giá để trả lời *"trang này đọc có ổn không?"*, proxy *"đủ tốt"* **duy nhất** repo có ([PRD](../../020-Requirements/PRD-Comic-Studio.md) §3.3).

**Vì sao vẫn khai đủ cặp ngay**: bất đối xứng chi phí — **rẻ khi làm từ đầu, đắt khi retrofit**. Dark trong quy ước shadcn là override **cùng bộ biến**; retrofit nghĩa là đi tìm mọi hex đã lỡ hardcode ở mọi component. Chi phí khai sẵn ≈ **một cột trong bảng token**.

| ✅ **⛔ KHÔNG được hoãn** | ⏸️ **Được hoãn** |
|---|---|
| **L2** — mọi semantic token có **đủ hai giá trị** | Switcher UI đổi theme |
| **HĐ-2** — ⛔ không hex trong `tailwind.config` | Nghiệm thu contrast cho **cột dark** |
| Selector `.dark {}` **tồn tại** trong `index.css` kể cả khi ⛔ chưa ai bật | Asset/ảnh có biến thể dark |
| | Script chặn flash trong `index.html` (xem [hợp đồng token](#hợp-đồng-phát-biểu-token)) |

> ⚠️ **Một quyết định bổ sung — dán nhãn cho đúng**: **vùng preview / canvas giữ nền trung tính CỐ ĐỊNH ở cả hai mode**.
> Nhãn: **quyết định Phase 3**, là **hệ quả của chính lý do `G-2`** (⛔ không để mode làm lệch cảm nhận trang truyện) — ⛔ **không phải** nội dung đã chốt tại gate. Giá trị cụ thể ở [Color Tokens](./Color-Tokens.md) *(lô sau)*.

---

## Chuẩn accessibility

> [!CAUTION]
> ⚠️ **Accessibility ⛔ KHÔNG phải requirement kế thừa** (`ARC-37`). Toàn `docs/020-Requirements/` ⛔ **không có một dòng nào** về WCAG / accessibility / contrast / responsive — đã grep, **0 hit là requirement**.
> ⇒ Toàn bộ mục này là **quyết định mới của Phase 3**, chốt tại gate `G-3`. ⛔ **TUYỆT ĐỐI không viết *"theo SRS"*, *"theo NFR"*, *"theo yêu cầu phi chức năng"*** cho bất kỳ dòng nào ở đây.

**Chuẩn: WCAG 2.2 Level AA.** **Phạm vi: giới hạn ở luồng chính. Thiết bị đích: desktop-first.**

### Vì sao AA — ⛔ không A, ⛔ không AAA

| # | Lý do |
|:--:|---|
| **1** | ⭐ **AA là mức công cụ tự động kiểm được phần lớn** (contrast, accessible name, focus visible, target size). Với **1 dev, ⛔ không code review** (`R1`), thứ duy nhất chạy được đều đặn là **kiểm tự động**. AAA đòi phán đoán người ⇒ chi phí **thường trực**, ⛔ không trả nổi |
| **2** | **AA là mức shadcn/Radix đã đỡ sẵn phần đắt nhất** — focus trap, roving tabindex, ARIA của dialog/popover/select. [ADR-001](../../030-Specs/Architecture/ADR-001-Backend-And-Frontend-Tech-Stack.md) mua shadcn về **chính vì** *"tối ưu cho AI assist (`R1`)"* ⇒ chọn AA là **tiêu thụ cái đã trả tiền** |
| **3** | ⚠️ ⛔ **Không có nghĩa vụ pháp lý nào trong repo bắt a11y.** Các nghĩa vụ đã biết đều ⛔ không động tới accessibility ⇒ AA là lựa chọn **kỹ thuật**, ⛔ **không phải tuân thủ**, và ⛔ **không có deadline** |

### ⭐ SC 2.5.7 Dragging Movements — hệ quả sinh UI thật

`SRS-FR-16` (**CHỐT**) chốt *"heuristic **+** cho user **kéo tay**"*, và [MVP-Scope](../../010-Planning/MVP-Scope.md) §5.2 thành phần **#2** liệt kê **kéo bubble, kéo đuôi trỏ**.

⇒ **WCAG 2.2 SC 2.5.7** đòi **mọi thao tác kéo phải có một đường thay thế KHÔNG-KÉO** (ví dụ: nút nudge theo bước, hoặc nhập toạ độ).

> ⚠️ ⭐ **Đây ⛔ không phải một dòng CSS — nó sinh UI thật và effort thật.**
> **`Foundations.md` là chỗ DUY NHẤT phát biểu chuẩn.** **UI thật được đặc tả ở [Components](./Components.md)** *(lô sau — link có chủ ý)*. ⛔ File này ⛔ không thiết kế control thay thế.

### Ngưỡng — nguồn là văn bản chuẩn, ⛔ không phải NFR của repo

| Hạng mục | Ngưỡng | SC |
|---|---|---|
| Tương phản text thường | **≥ 4.5:1** | 1.4.3 |
| Tương phản text lớn | **≥ 3:1** | 1.4.3 |
| Tương phản thành phần UI & đồ hoạ mang nghĩa | **≥ 3:1** | 1.4.11 |
| Kích thước đích bấm/chạm | **≥ 24×24 CSS px** (có ngoại lệ trong văn bản chuẩn) | 2.5.8 |
| Focus nhìn thấy được | Bắt buộc | 2.4.7 |
| Thao tác kéo có đường thay thế | Bắt buộc | **2.5.7** |

> ⚠️ **Nhãn nguồn — đọc kỹ, đây là chỗ dễ dán sai:**
> - Các ngưỡng trên là **hằng số quy phạm trích từ văn bản WCAG 2.2**. Chúng ⛔ **không phải NFR của repo**, ⛔ **không phải số tự đặt**, và ⛔ **không mang `[EM]`** (dán `[EM]` là mô tả sai một hằng số của chuẩn thành ước lượng của mình).
> - Thứ **là** quyết định Phase 3 chính là **việc CHỌN chuẩn WCAG 2.2 AA và giới hạn phạm vi** — `G-3`.
> - ⚠️ **Số hiệu SC và các ngoại lệ phải mở đúng văn bản chuẩn trên `w3.org` khi audit.** Bảng này là **bảng tra nhanh**, ⛔ không thay văn bản chuẩn.

### Ranh giới a11y ⛔ không cứu được — và cơ hội đã có sẵn dữ liệu

Sản phẩm này có một bề mặt mà a11y ⛔ **không cứu được**: **bản thân trang truyện**. Art là ảnh model sinh; thành phẩm là ảnh sau composite ⇒ screen reader ⛔ không đọc được.

**Nhưng** repo **đã có sẵn** dữ liệu để làm điều gần nhất: `dialogue_source` là **string bất biến** và `dialogue_rendered` là string người sửa được ([ADR-013](../../030-Specs/Architecture/ADR-013-Typeset-Layer-Separate-From-Art.md) §Decision **5**).
⇒ Text alternative cho page là **dữ liệu ĐÃ CÓ**, ⛔ không phải công việc mới.
⚠️ Ghi ở đây như một **cơ hội**, ⛔ **không phải requirement** — vì ⛔ chưa ai yêu cầu.

⛔ **Không khai i18n/RTL trong tầng a11y** — [SRS](../../020-Requirements/SRS-Comic-Studio.md) §5.2 `b-6` vẫn là `TBD` (`ARC-38`).

---

## Cách kiểm (checklist cơ học)

> ⭐ **Checklist này là hợp đồng nghiệm thu của bốn file lô sau**, ⛔ không phải lời khuyên chung chung. Người hoặc agent khác phải kiểm được **bằng grep hoặc bằng mắt**, ⛔ không cần hiểu ý đồ thiết kế.
> Phạm vi mặc định: `docs/040-Design/Design-System/**`.

| # | Kiểm bằng cách nào | Kết quả **phải** thấy | Neo |
|:--:|---|---|---|
| **K-1** | `grep -rn "\[\[" docs/040-Design/` | **0 hit** — ⛔ không wiki-link | RULE-001 quy tắc **#5** |
| **K-2** | `grep -rniE "theo SRS\|theo NFR\|theo yêu cầu" docs/040-Design/` | **Mọi hit** grep ngược ra được **một hàng thật** của [SRS](../../020-Requirements/SRS-Comic-Studio.md) §5.1 | `ARC-36` |
| **K-3** | `grep -rniE "WCAG\|accessibility\|a11y\|contrast\|tương phản" docs/040-Design/` | **Mọi hit** mang nhãn **quyết định Phase 3**; ⛔ **0 hit** viện dẫn SRS/NFR | `ARC-37` |
| **K-4** | Liệt kê **mọi số có đơn vị** (ms, s, px, %, MB) trong tầng 040 | Mỗi số có **neo [SRS](../../020-Requirements/SRS-Comic-Studio.md) §5.1** *hoặc* nhãn **quyết định Phase 3** *hoặc* nhãn **hằng số của chuẩn WCAG 2.2** | `ARC-35`, `ARC-36` |
| **K-5** | `grep -rniE "bản quyền\|copyright\|plagiar\|similarity\|tương đồng\|đạo văn\|original\|shield\|verified" docs/040-Design/` | ⚠️ ⛔ **KHÔNG phải quy tắc 0 hit** — **mọi hit phải đọc lại nghĩa**. Hit hợp lệ chỉ thuộc: *tiếp nhận thông báo takedown*, *đọc opt-out signal do chủ quyền gắn*, hoặc *phát biểu lệnh cấm* | `ARC-28`, `ARC-29`; [Brand Guidelines](./Brand-Guidelines.md) §Điều CẤM |
| **K-6** | Mở [Color Tokens](./Color-Tokens.md), **đếm cột giá trị** của bảng semantic | **Mọi** semantic token có **đủ 2 cột** light + dark; ⛔ **0 token** chỉ tồn tại ở một mode | **L2**, `G-2` |
| **K-7** | Với **mỗi** semantic token **nền**, tìm token chữ đi kèm | ⛔ **0 token nền** thiếu cặp `-foreground` | **L1** |
| **K-8** | `grep -niE "#[0-9a-fA-F]{3,8}"` **bên trong block `theme.extend`** của [Color Tokens](./Color-Tokens.md) | **0 hit** — Tailwind chỉ được trỏ `var(--…)` | **HĐ-2** |
| **K-9** | `grep -rn "ADR-001" docs/040-Design/Design-System/` rồi **đọc câu chứa mỗi hit** | ⛔ **0 câu** trích `ADR-001` làm nguồn cho **tên biến CSS** | Mâu thuẫn `X-2` |
| **K-10** | Mở mục *font render* của [Typography](./Typography.md) | Mang **`TBD`** + owner **Architect + Founder**; ⛔ **không có tên họ font nào**, ⛔ không fallback stack | [ADR-013](../../030-Specs/Architecture/ADR-013-Typeset-Layer-Separate-From-Art.md) bảng `TBD` |
| **K-11** | `grep -rniE "kéo\|drag" docs/040-Design/Design-System/Components.md` | **Mọi** thao tác kéo có **đường thay thế không-kéo** được đặc tả | **SC 2.5.7**, `G-3` |
| **K-12** | `grep -rniE "i18n\|l10n\|locale\|RTL\|đa ngôn ngữ" docs/040-Design/` | **Mọi hit** trỏ [SRS](../../020-Requirements/SRS-Comic-Studio.md) §5.2 `b-6` = **`TBD`** | `ARC-38` |
| **K-13** | Đọc [Spacing & Layout](./Spacing-And-Layout.md) | ⛔ **0 mục** đặt kích thước/vị trí **panel hoặc bubble** bằng px; hình học đó là **toạ độ 0–1** | [ADR-013](../../030-Specs/Architecture/ADR-013-Typeset-Layer-Separate-From-Art.md) §Decision **2** |
| **K-14** | Đọc mục *Audience* và *Tone of voice* của [Brand Guidelines](./Brand-Guidelines.md) | Đối tượng là **writer**; ⛔ **0 dòng** nhắm hay nói với **cộng đồng hoạ sĩ**; ⛔ **0 dòng persona** | `ARC-34`; [PRD](../../020-Requirements/PRD-Comic-Studio.md) §3.3 |

---

## Tài liệu tham khảo

> ⚠️ **Ghi nhận minh bạch (`X-3`)**: tại **2026-08-30**, các tài liệu neo bên dưới (`ADR-001`, `ADR-013`, `SDD`, `SRS`) đều ở `status: draft`. File này là tài liệu tầng 040 neo vào một nền **chưa `approved`**.
> ⚠️ **`E1` của run**: bản `ADR-001` trong worktree (đã có `shadcn/ui + Tailwind CSS`) được PM chốt là **bản đúng** và là **input read-only**; run này ⛔ không commit `ADR-001`.

**Trong Design System** *(bốn file dưới thuộc lô sau — link có chủ ý, chưa tồn tại tại thời điểm viết)*:

- [Brand Guidelines](./Brand-Guidelines.md) — tone · hướng màu chủ đạo · điều CẤM
- [Color Tokens](./Color-Tokens.md) — **nguồn duy nhất** của giá trị màu; phải chứa block `:root{}`/`.dark{}` + `theme.extend`
- [Typography](./Typography.md) — hai hệ font; mục *font render* giữ `TBD`
- [Spacing & Layout](./Spacing-And-Layout.md) — thang spacing, radius, breakpoint, z-index
- [Components](./Components.md) — inventory · ma trận state · **đường thay thế không-kéo (SC 2.5.7)**

**Ngoài Design System**:

- [Design MOC](../Design-MOC.md) — bản đồ tầng 040
- [ADR-001 — Backend & Frontend Tech Stack](../../030-Specs/Architecture/ADR-001-Backend-And-Frontend-Tech-Stack.md) — §Decision điều **5**, **6** · bảng *Tầng MẶC ĐỊNH* hàng **Frontend & UI** · bảng `TBD`
- [ADR-013 — Typeset Layer Separate From Art](../../030-Specs/Architecture/ADR-013-Typeset-Layer-Separate-From-Art.md) — §Decision **2**, **5** · bảng `TBD` hàng *font sẽ render*
- [SRS — Comic Studio](../../020-Requirements/SRS-Comic-Studio.md) — §3.D · §5.1 · §5.2 (`b-6`) · `SRS-FR-16`
- [PRD — Comic Studio](../../020-Requirements/PRD-Comic-Studio.md) — §3.3
- [MVP Scope](../../010-Planning/MVP-Scope.md) — §4.1 (toạ độ 0–1) · §5.2 thành phần **#2**, **#4**
- [RULE-001 — Documents Template](../../../knowledge-base/99-Templates/Documents-Template.md) — quy tắc **#5** (⛔ không wiki-link) · §Document Type Mapping

**Hồ sơ quyết định của run** (`2026-08-30-brand-guidelines-va-design-system-comic-studio`):

- [run-plan.md](../../010-Planning/pm-runs/2026-08-30-brand-guidelines-va-design-system-comic-studio/run-plan.md) — §Gate `G-2`, `G-3`
- [escalations.md](../../010-Planning/pm-runs/2026-08-30-brand-guidelines-va-design-system-comic-studio/escalations.md) — `E1` (ADR-001 chưa commit) · `E2` (độc giả đích)
- [findings/product-designer.md](../../010-Planning/pm-runs/2026-08-30-brand-guidelines-va-design-system-comic-studio/findings/product-designer.md) — §4.2 (một chiều phụ thuộc) · §4.3 (năm cạm bẫy) · §4.4 (hình dạng file)
- [findings/architect.md](../../010-Planning/pm-runs/2026-08-30-brand-guidelines-va-design-system-comic-studio/findings/architect.md) — `ARC-35`…`ARC-38` · mâu thuẫn `X-2`, `X-3`
