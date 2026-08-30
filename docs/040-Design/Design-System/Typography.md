---
id: DS-005
type: design-system
status: draft
project: comic-studio
owner: "@trisjr"
tags: [design-system, phase-3]
created: 2026-08-30
updated: 2026-08-30
---

# Typography

> **Part of:** [Design MOC](../Design-MOC.md)
> **Tuân theo:** [Foundations](./Foundations.md) §*Hợp đồng phát biểu token* (**CSS variable là NGUỒN, Tailwind chỉ THAM CHIẾU**) và §*Cách kiểm*
> **Ràng buộc gốc:** [ADR-001 — Backend & Frontend Tech Stack](../../030-Specs/Architecture/ADR-001-Backend-And-Frontend-Tech-Stack.md) `## Decision` **điều 8** + `## Consequences` §Tiêu cực **#5** · [ADR-013 — Typeset Layer Separate From Art](../../030-Specs/Architecture/ADR-013-Typeset-Layer-Separate-From-Art.md) `## Decision` **điều 6** + bảng `TBD` hàng *Font sẽ render*

> [!CAUTION]
> ⭐⭐ **Đây là file có chi phí hiểu sai cao nhất của tầng Design System.**
> Nó mô tả **hai** hệ font sống ở **hai runtime** khác nhau. Gộp chúng lại **⛔ không sinh ra một exception nào, ⛔ không sinh ra một dòng log nào** — hệ thống **vẫn chạy**, chỉ khác kết quả. Sai lệch **chỉ lộ ra sau khi ảnh đã được sinh**, tức **sau khi đã gọi image provider và đã tốn tiền**; và tại điểm đó `D-29` ([ADR-013](../../030-Specs/Architecture/ADR-013-Typeset-Layer-Separate-From-Art.md) `## Decision` điều **1**) cấm nướng chữ vào pixel ⇒ ⛔ **không có đường vá nhanh**.
> **Độc giả đích: AI assist sinh code VÀ người sẽ implement compositor.** ⇒ ưu tiên **quy tắc kiểm được**, ⛔ không phải văn xuôi thẩm mỹ.

## Mục lục

- [⭐ HAI HỆ FONT — ⛔ KHÔNG GỘP](#-hai-hệ-font-—--không-gộp)
- [Hệ 1 — Font UI](#hệ-1-—-font-ui)
- [Hệ 2 — Font render vào ảnh](#hệ-2-—-font-render-vào-ảnh)
- [Tiếng Việt: line-height & dấu chồng](#tiếng-việt-line-height--dấu-chồng)
- [NFC / NFD](#nfc--nfd)
- [Cỡ chữ bubble là HÀM của `text_budget`, ⛔ không phải giá trị chọn](#cỡ-chữ-bubble-là-hàm-của-text_budget--không-phải-giá-trị-chọn)
- [Tài liệu tham khảo](#tài-liệu-tham-khảo)

---

## ⭐ HAI HỆ FONT — ⛔ KHÔNG GỘP

> [!IMPORTANT]
> ⭐⭐ **Hai hệ font này ⛔ KHÔNG phải hai giá trị của cùng một token.** Chúng khác nhau **về bản chất spec**: một bên là **lựa chọn thẩm mỹ**, một bên là **tham số đầu vào của thuật toán ngắt dòng**. Vì vậy chúng nằm ở **hai mục cấp 2 riêng**, và token của chúng ⛔ **KHÔNG chung namespace**.

| Chiều | **Hệ 1 — Font UI** | **Hệ 2 — Font render vào ảnh** |
|---|---|---|
| Chạy ở đâu | **Browser**, `apps/web` (SPA — [ADR-001](../../030-Specs/Architecture/ADR-001-Backend-And-Frontend-Tech-Stack.md) `## Decision` điều **5**) | ⭐ **Node, cùng runtime với compositor** ([ADR-001](../../030-Specs/Architecture/ADR-001-Backend-And-Frontend-Tech-Stack.md) `## Decision` điều **8**) |
| Ai nhìn thấy | Tác giả, trong lúc biên tập | ⭐ **Người đọc cuối**, trong sản phẩm giao đi |
| Bản chất | Lựa chọn **thẩm mỹ / brand** | ⭐ **Tham số kỹ thuật** — đầu vào của thuật toán wrap |
| Đo bằng gì | Browser tự đo; ⛔ **không ai phụ thuộc số đo đó** | Compositor **phải tự đo** để wrap đúng |
| **Fallback stack** | ✅ **Được phép** — browser giải quyết | ⛔ **KHÔNG** — phải [ĐƠN TRỊ](#hệ-2-—-font-render-vào-ảnh) |
| Sai thì hỏng ở đâu | Chữ xấu trên màn hình — sửa bằng **một dòng CSS** | ⭐ **Hỏng sản phẩm cuối**: chữ tràn / dấu bị mép bubble cắt **trong ảnh đã sinh** |
| Đổi được không | Bất cứ lúc nào, chi phí ~0 | Đổi = **wrap lại toàn bộ**; mọi bubble đã duyệt phải **đo lại** |
| **Ai chốt** | Product Designer đề xuất → **Founder duyệt**, khi init dự án | ⛔ **Architect + Founder**, **sau MVP0, trước gate `G1-e`** — `TBD` do [ADR-013](../../030-Specs/Architecture/ADR-013-Typeset-Layer-Separate-From-Art.md) sở hữu |
| Trạng thái tại **2026-08-30** | Ô trống **được phép điền bất cứ lúc nào** | ⛔ **`TBD` CÓ CHỦ — run này KHÔNG chốt** |

### ⭐ Câu chịu lực — nguyên văn, ⛔ không diễn giải lại

[ADR-001](../../030-Specs/Architecture/ADR-001-Backend-And-Frontend-Tech-Stack.md) `## Decision` **điều 8** (**CHỐT**):

> *"**Wrap tiếng Việt (`R3`) nằm CÙNG runtime với compositor.** Chuẩn hoá **NFC** ngay tại biên ingest; ngắt dòng theo **grapheme cluster + word boundary** bằng `Intl.Segmenter` (ECMA-402, ICU-backed, có sẵn trong Node LTS); ⛔ **không** được wrap ở frontend rồi gửi kết quả xuống, ⛔ **không** được wrap bằng font khác font sẽ render."*

[ADR-001](../../030-Specs/Architecture/ADR-001-Backend-And-Frontend-Tech-Stack.md) `## Consequences` §Tiêu cực **#5** — ⭐ **đây là câu giải thích vì sao phải có hai hệ font**:

> *"**`Intl.Segmenter` giải quyết ngắt, KHÔNG giải quyết đo.** Nó cho ranh giới grapheme/word đúng chuẩn Unicode, nhưng **không** biết chữ rộng bao nhiêu pixel. Wrap đúng = *segmentation* **+** *đo bằng chính font sẽ render*. Đây là lý do điều 8 của `## Decision` bắt wrap ở cùng runtime với compositor."*

⇒ Đọc thẳng: **font ⛔ không phải một thuộc tính trình bày ở đây — nó là một nửa của phép tính.** Nửa kia (`Intl.Segmenter`) đã được [ADR-001](../../030-Specs/Architecture/ADR-001-Backend-And-Frontend-Tech-Stack.md) chốt; ⛔ **file này không mở lại**.

### ⭐ Token của hai hệ ⛔ KHÔNG chung namespace

| | **Hệ 1 — Font UI** | **Hệ 2 — Font render** |
|---|---|---|
| Phát biểu ở đâu | **CSS variable** trong `apps/web/src/index.css`, Tailwind `theme.extend` **trỏ vào** `var(--…)` — [Foundations](./Foundations.md) `HĐ-1`, `HĐ-2` | ⭐ **Tham số config của `apps/api`** — cùng runtime với compositor |
| ⛔ Cấm | ⛔ Hardcode `font-family` thẳng trong component | ⛔ **Khai thành CSS variable** · ⛔ **đưa vào Tailwind theme** · ⛔ nạp bằng webfont ở browser |

⚠️ **Vì sao lệnh cấm bên phải là lệnh cấm cứng, ⛔ không phải sở thích tổ chức file:**

| # | Lý do |
|:--:|---|
| **1** | ⭐ Đặt font render vào Tailwind theme là **mời một dev tương lai render bubble ở client** — vì lúc đó font đã "có sẵn ở frontend", việc vẽ bubble tại chỗ trở thành đường dễ đi nhất. Đó **đúng** phương án [ADR-013](../../030-Specs/Architecture/ADR-013-Typeset-Layer-Separate-From-Art.md) §Alternatives **(f)** *"Preview render client-side"* đã **LOẠI tường minh** |
| **2** | Compositor **dùng chung cho preview và export** ([ADR-013](../../030-Specs/Architecture/ADR-013-Typeset-Layer-Separate-From-Art.md) `## Decision` điều **8**, `D-32`) ⇒ ⛔ **không tồn tại renderer thứ hai** để mà có font thứ hai. Một font sống ở `apps/web` ⛔ **không thể** là font mà compositor đo |
| **3** | Webfont mà browser tải xuống và file font mà server nạp ⛔ **không bao giờ được đảm bảo cùng metric** (biến thể subset, hinting, fallback lúc chưa tải xong). Hai metric khác nhau ⇒ hai kết quả ngắt dòng khác nhau |

### ⭐ Gộp làm một thì hỏng gì — đường hỏng cụ thể

**Chiều nguy hiểm là chiều mặc định của nghề**: designer chọn một font đẹp, hợp brand, khai vào Typography spec, và **dùng nó cho cả bubble**. Đường hỏng đi như sau:

1. Compositor server-side cần đo bề rộng chuỗi để wrap ⇒ nó đo bằng metric của **font A** (font UI được khai trong spec).
2. Runtime server **có thể không có** font A ⇒ nó **fallback âm thầm** sang **font B** — hoặc font A ở server là một biến thể/subset khác với bản browser tải.
3. ⇒ **Ngắt dòng tính theo font A, glyph vẽ bằng font B.** Chiều rộng thực ⛔ **khác** chiều rộng đã tính.
4. ⇒ Biểu hiện đúng ba thứ mà nghiệm thu MVP0 của [ADR-001](../../030-Specs/Architecture/ADR-001-Backend-And-Frontend-Tech-Stack.md) `## Consequences` **#5** bắt phải test: **(a)** ký tự bị tách khỏi dấu của nó khi xuống dòng · **(b)** ⭐ **dấu tiếng Việt bị mép bubble cắt cụt** · **(c)** chuỗi NFD và NFC tương đương cho ra ngắt dòng **khác nhau**.

| # | Vì sao đây là loại lỗi tệ nhất |
|:--:|---|
| **(a)** | ⭐ **Hỏng IM LẶNG.** ⛔ Không exception, ⛔ không log, ⛔ không test đơn vị nào đỏ — hệ thống **vẫn chạy**, chỉ **khác kết quả**. [ADR-013](../../030-Specs/Architecture/ADR-013-Typeset-Layer-Separate-From-Art.md) §Alternatives **(e)** gọi đúng dạng này là *"lỗi **không phát hiện được** cho tới khi khách hàng phàn nàn"* |
| **(b)** | ⭐ **Lộ ra SAU KHI đã tiêu tiền.** Điểm hỏng nằm ở **bước composite**, tức sau khi đã gọi image provider để sinh art. Và `D-29` cấm nướng chữ vào pixel ⇒ ⛔ **không có đường vá nhanh**: không thể "sửa tạm bằng cách vẽ đè chữ vào ảnh" |
| **(c)** | **Vi phạm trực tiếp hai lệnh cấm nguyên văn** của [ADR-001](../../030-Specs/Architecture/ADR-001-Backend-And-Frontend-Tech-Stack.md) điều 8: ⛔ *"không được wrap ở frontend rồi gửi kết quả xuống"* và ⛔ *"không được wrap bằng font khác font sẽ render"* |
| **(d)** | **Mất chỗ ghi rủi ro glyph coverage.** Rủi ro *"font không đủ glyph tiếng Việt"* chỉ áp cho hệ render và ⛔ **không có benchmark định lượng nào** ([ADR-013](../../030-Specs/Architecture/ADR-013-Typeset-Layer-Separate-From-Art.md) bảng `TBD`). Gộp hai hệ ⇒ rủi ro hoặc bị áp nhầm lên font UI (vô nghĩa — browser có fallback), hoặc **biến mất khỏi tài liệu** |
| **(e)** | **Đóng hộ một `TBD` có chủ.** Xem [Hệ 2](#hệ-2-—-font-render-vào-ảnh) |

⚠️ **Chiều ngược lại (lấy font render làm font chung) ⛔ không phá pipeline** — nó chỉ làm UI xấu và ràng buộc thừa. Ghi ra để ⛔ **không ai "giải quyết" vấn đề bằng cách gộp về phía đó rồi tưởng đã xong**: gộp kiểu gì cũng vẫn là **một** hệ, và vẫn mất chỗ ghi `TBD` + rủi ro glyph.

### Cách kiểm hai mục font này

> Đối chiếu [Foundations](./Foundations.md) §*Cách kiểm* — mục dưới là phần của checklist đó **rơi vào file này**.

| # | Kiểm bằng cách nào | Kết quả **phải** thấy |
|:--:|---|---|
| **K-10** | Mở mục [Hệ 2 — Font render](#hệ-2-—-font-render-vào-ảnh) | Mang **`TBD`** + owner **Architect + Founder**; ⛔ **không có tên họ font nào**, ⛔ không fallback stack |
| **`ARC-08`** | Đếm số hệ font được khai trong file | **≥ 2**, đặt **tên khác nhau**, mỗi hệ ghi rõ **render bởi ai** |
| **`ARC-09`** | `grep` mọi tên họ font gắn với **hệ render** | ⛔ **0 hit** — ô đó là `TBD` |
| **`ARC-10`** | Tìm dấu phẩy trong khai báo họ font của **hệ render** | ⛔ **0 hit** — đơn trị, ⛔ không fallback stack |
| **`ARC-11`** | `grep -niE "ngắt dòng\|text-wrap\|hyphens\|word-break"` | **Mọi hit** nói về **compositor server-side** *hoặc* là **trích nguyên văn** `ADR-001`; ⛔ 0 hit đặc tả wrap thoại ở tầng frontend |
| **`ARC-12`** | Đọc [NFC / NFD](#nfc--nfd) | ⛔ **0 dòng** khai một chuẩn hoá Unicode thứ hai ở frontend; mọi phép đếm ký tự trong UI khai rõ là **grapheme cluster** và **không chuẩn tắc** |

---

## Hệ 1 — Font UI

**Phạm vi:** chrome của editor — app shell, form, bảng, dialog, toolbar, nhãn, thông báo. Render bởi **browser**, trong `apps/web`.

**Bản chất:** đây là **ô trống được phép điền bất cứ lúc nào**, ⛔ **KHÔNG phải một `TBD` có chủ như [Hệ 2](#hệ-2-—-font-render-vào-ảnh)**. Phân biệt hai thứ này là điểm dễ lẫn nhất của file:

| | Hệ 1 — họ font chưa điền | Hệ 2 — `TBD-FONT` |
|---|---|---|
| Vì sao chưa có | Repo ⛔ **chưa có `package.json` nào** tại 2026-08-30 ⇒ chưa có bước init để verify | ⛔ **Không có benchmark định lượng** cho lỗi thiếu glyph; phải **đo ở MVP0** |
| Ai điền | Product Designer đề xuất → **Founder duyệt**, khi init `apps/web` | ⛔ **Architect + Founder** |
| Điền sai thì sao | Sửa một dòng CSS | ⭐ **Wrap lại toàn bộ**, mọi bubble đã duyệt phải đo lại |

### Ràng buộc mà font UI phải thoả

| # | Ràng buộc | Vì sao |
|:--:|---|---|
| **U-1** | **Phủ đủ dấu tiếng Việt** (dấu chồng: `ế`, `ộ`, `ữ`) — ⚠️ **verify khi init**, ⛔ không giả định | Form Story Bible đầy tên nhân vật có dấu; thiếu glyph ⇒ browser fallback từng ký tự ⇒ chữ **nhảy font giữa câu** |
| **U-2** | ✅ **Được phép** khai **fallback stack**, và stack **phải kết thúc bằng generic family** (`sans-serif` / `monospace`) | Browser tự giải quyết; và ⛔ **không ai phụ thuộc số đo** của font UI ⇒ tính bất định của stack ở đây là **vô hại** |
| **U-3** | Có **một họ mono** cho dữ liệu kỹ thuật (id, toạ độ, mã lỗi) | Các bề mặt này hiển thị chuỗi cần so sánh bằng mắt |
| **U-4** | ⛔ **Thang cỡ chữ của hệ này KHÔNG áp cho bubble** | Xem [Cỡ chữ bubble là HÀM của `text_budget`](#cỡ-chữ-bubble-là-hàm-của-text_budget--không-phải-giá-trị-chọn) |

### Hình dạng file bắt buộc — CSS variable là **NGUỒN**

> [!IMPORTANT]
> Theo [Foundations](./Foundations.md) `HĐ-1` / `HĐ-2`: **giá trị sống trong CSS variable**, Tailwind **chỉ trỏ vào** `var(--…)`.
> ⚠️ **Tên biến dưới đây là *quyết định Phase 3*, kèm nhãn ⚠️ *cần verify khi init*** — quy ước của thư viện shadcn thay đổi theo version và repo ⛔ chưa có `package.json` để verify. ⛔ **Tên biến KHÔNG phải nội dung của `ADR-001`** — ADR đó chốt *stack*, ⛔ không nêu một tên biến CSS nào ([Foundations](./Foundations.md) §*Tên biến — vùng ảo giác nguy hiểm nhất*).

```css
/* apps/web/src/index.css — phần typography.
   Block màu thuộc Color-Tokens.md (file thuộc lô khác). */
:root {
  /* Họ font: điền khi init, sau khi Founder duyệt. Fallback stack ĐƯỢC PHÉP ở hệ UI. */
  --font-sans: <họ font UI>, system-ui, sans-serif;
  --font-mono: <họ font mono>, ui-monospace, monospace;

  /* Thang cỡ chữ — quyết định Phase 3 */
  --text-xs:   0.75rem;
  --text-sm:   0.875rem;
  --text-base: 1rem;
  --text-lg:   1.125rem;
  --text-xl:   1.25rem;
  --text-2xl:  1.5rem;

  /* Line-height — quyết định Phase 3; đã nới cho tiếng Việt, xem mục dấu chồng */
  --leading-tight:   1.30;
  --leading-snug:    1.45;
  --leading-normal:  1.60;
  --leading-relaxed: 1.75;

  /* Weight — quyết định Phase 3 */
  --font-weight-normal:   400;
  --font-weight-medium:   500;
  --font-weight-semibold: 600;
}
```

```ts
// tailwind.config.ts — theme.extend CHỈ được trỏ var(--…). ⛔ Không giá trị literal.
theme: {
  extend: {
    fontFamily: {
      sans: ['var(--font-sans)'],
      mono: ['var(--font-mono)'],
    },
    fontSize: {
      xs:   ['var(--text-xs)',   { lineHeight: 'var(--leading-normal)' }],
      sm:   ['var(--text-sm)',   { lineHeight: 'var(--leading-normal)' }],
      base: ['var(--text-base)', { lineHeight: 'var(--leading-normal)' }],
      lg:   ['var(--text-lg)',   { lineHeight: 'var(--leading-snug)'   }],
      xl:   ['var(--text-xl)',   { lineHeight: 'var(--leading-snug)'   }],
      '2xl':['var(--text-2xl)',  { lineHeight: 'var(--leading-tight)'  }],
    },
  },
}
```

### Vai trò → token (⭐ cột chuẩn là cột **vai trò**)

| Vai trò trong chrome | Cỡ | Line-height | Weight |
|---|---|---|---|
| Tiêu đề màn hình | `--text-2xl` | `--leading-tight` | `--font-weight-semibold` |
| Tiêu đề khối / card | `--text-lg` | `--leading-snug` | `--font-weight-semibold` |
| Body, nội dung form, nhãn dài | `--text-base` | `--leading-normal` | `--font-weight-normal` |
| Nhãn control, nút, ô bảng | `--text-sm` | `--leading-normal` | `--font-weight-medium` |
| Chú thích, trạng thái phụ, metadata | `--text-xs` | `--leading-normal` | `--font-weight-normal` |

> ⚠️ **Nhãn nguồn — đọc kỹ:** **mọi số** trong hai block code và bảng trên là **quyết định Phase 3**. Chúng ⛔ **không phải NFR của repo**, ⛔ **không neo vào một hàng requirement nào**, và ⛔ **không phải kết quả đo**. Chúng là thang khởi điểm để code chạy được, chỉnh được tự do khi init.
> ⚠️ Chuẩn a11y (tương phản, kích thước đích) phát biểu ở **đúng một chỗ**: [Foundations](./Foundations.md) §*Chuẩn accessibility* — **quyết định Phase 3** (`G-3`). ⛔ File này không phát biểu lại chuẩn.
> ⚠️ Giá trị **màu chữ** ⛔ không thuộc file này ⇒ [Color Tokens](./Color-Tokens.md) *(file thuộc lô khác)*.

---

## Hệ 2 — Font render vào ảnh

> [!CAUTION]
> ⛔⛔ **Đây là một `TBD` do [ADR-013](../../030-Specs/Architecture/ADR-013-Typeset-Layer-Separate-From-Art.md) SỞ HỮU. Mục này ghi RÀNG BUỘC, ⛔ KHÔNG chọn font.**
> **Chủ:** ⭐ **Architect + Founder** · **Thời điểm:** **sau MVP0, trước gate `G1-e`**.
> ⛔ **Run này KHÔNG chốt.** Viết một tên font vào ô này là **đóng thay người khác** và **đóng trước khi có số đo** — đúng thứ [ADR-001](../../030-Specs/Architecture/ADR-001-Backend-And-Frontend-Tech-Stack.md) từ chối làm với thư viện compositor: *"⛔ không dán tên kèm con số khi chưa đo"*.
> ⭐ Đây **đúng khuôn** mà [ADR-013](../../030-Specs/Architecture/ADR-013-Typeset-Layer-Separate-From-Art.md) `## Decision` điều **6** đã dùng cho `D-30` (*"⛔ Không chọn lại thư viện ở đây — xem `ADR-001` điều 8"*). Design System **kế thừa nguyên khuôn đó**.

**Phạm vi:** chữ **bên trong bubble của trang truyện thành phẩm**. Render bởi **compositor server-side**, cùng runtime với bước wrap, trong `apps/api`.

| Hạng mục | Trạng thái | Chủ | Thời điểm |
|---|---|---|---|
| **Họ font sẽ render** | ⛔ **`TBD`** | **Architect + Founder** | Sau MVP0, trước gate `G1-e` |
| **Glyph coverage tiếng Việt** của font đó | ⛔ **`TBD`** — ⚠️ ⛔ **không có benchmark định lượng nào**, chỉ phát hiện được bằng **kiểm thủ công từng panel** | **Architect + Founder** | Cùng lúc trên |
| **Line-height / leading của bubble** | ⛔ **`TBD`** — là **dẫn xuất từ metric của font thật**, ⛔ không chọn trước được | **Architect + Founder** | Sau khi hai hàng trên đóng |

### ⭐ Nó ⛔ KHÔNG phải CSS variable — nó là **tham số config của `apps/api`**

| | |
|---|---|
| **Sống ở đâu** | Config của **`apps/api`** — cùng image, cùng runtime với compositor ([ADR-001](../../030-Specs/Architecture/ADR-001-Backend-And-Frontend-Tech-Stack.md) `## Decision` điều **2**: *một image, hai command*) |
| **File font sống ở đâu** | Đóng gói **cùng image của `apps/api`**, ⛔ không tải qua mạng lúc composite |
| ⛔ **Cấm** | ⛔ Khai thành CSS variable · ⛔ đưa vào Tailwind theme · ⛔ nạp bằng webfont ở `apps/web` · ⛔ để `apps/web` và `apps/api` khai hai nguồn font khác nhau |

⚠️ **Vì sao lệnh cấm này quan trọng hơn nó trông:** Tailwind theme là **bề mặt mà một dev tương lai đọc để biết "font của sản phẩm là gì"**. Đặt font render ở đó là **mời họ vẽ bubble ngay tại client** — đường mà [ADR-013](../../030-Specs/Architecture/ADR-013-Typeset-Layer-Separate-From-Art.md) §Alternatives **(f)** đã **LOẠI tường minh**, với lý do nguyên văn: preview client-side *"không thể là compositor của export"*.

### ⭐ ĐƠN TRỊ — ⛔ KHÔNG fallback stack

> **Ràng buộc:** hệ render khai **đúng một** họ font, resolve ra **đúng một** file font xác định. ⛔ **Không dấu phẩy. ⛔ Không generic family. ⛔ Không "nếu thiếu thì dùng cái kia".**

**Lý do — ⛔ đây không phải lựa chọn thẩm mỹ:**

1. Font render là **tham số đầu vào của thuật toán wrap** ([ADR-001](../../030-Specs/Architecture/ADR-001-Backend-And-Frontend-Tech-Stack.md) `## Consequences` **#5**: *"Wrap đúng = segmentation **+** đo bằng chính font sẽ render"*).
2. Một fallback stack nghĩa là **⛔ không biết trước font nào thực sự đo** — việc chọn phụ thuộc vào cái gì có mặt trong runtime tại thời điểm chạy.
3. ⇒ **Phép đo mất tính xác định** ⇒ kết quả wrap ⛔ không tái lập được ⇒ cùng một chuỗi thoại có thể ngắt khác nhau giữa hai lần chạy, hoặc giữa preview và export.
4. ⇒ Điều này phá thẳng [ADR-013](../../030-Specs/Architecture/ADR-013-Typeset-Layer-Separate-From-Art.md) `## Decision` điều **8**: preview và export **dùng chung compositor** để *"cái người dùng duyệt **là** cái họ nhận"*.

⚠️ **Đối chiếu với [Hệ 1](#hệ-1-—-font-ui)**: font UI **được phép** fallback stack **chính vì** ⛔ **không ai phụ thuộc số đo của nó**. Tính bất định vô hại ở một hệ và gây hỏng sản phẩm ở hệ kia — đó là toàn bộ lý do hai hệ này ⛔ **không được gộp**.

### Bốn ràng buộc mà font render phải thoả (khi `TBD` được đóng)

> ⭐ **Cả bốn ràng buộc dưới đây nay đã được ghi vào chính [ADR-013](../../030-Specs/Architecture/ADR-013-Typeset-Layer-Separate-From-Art.md) §*Bốn ràng buộc mà font render phải thoả*** *(đồng bộ `2026-08-30`)*. ⭐ **ADR-013 là nguồn sở hữu**; bảng này là **bản đối chiếu ở tầng 040**, ⛔ không phải nguồn thứ hai. Lệch nhau ⇒ sửa **cả hai trong cùng một run**.

| # | Ràng buộc | Suy ra từ đâu |
|:--:|---|---|
| **R-1** | ⭐ **Đơn trị** — một họ font, resolve xác định, ⛔ không fallback stack | [ADR-001](../../030-Specs/Architecture/ADR-001-Backend-And-Frontend-Tech-Stack.md) điều **8** (*"⛔ không được wrap bằng font khác font sẽ render"*) + `## Consequences` **#5** |
| **R-2** | ⭐ **Phủ đủ dấu tiếng Việt**, gồm **dấu chồng hai tầng** (`ế`, `ữ`, `ợ`) — và phủ **bằng glyph dựng sẵn hoặc mark positioning đúng**, ⛔ không phải bằng cách vẽ chồng tuỳ ý | Nghiệm thu MVP0 của [ADR-001](../../030-Specs/Architecture/ADR-001-Backend-And-Frontend-Tech-Stack.md) **#5** (corpus có dấu chồng) · [ADR-013](../../030-Specs/Architecture/ADR-013-Typeset-Layer-Separate-From-Art.md) §Lý do **#2** |
| **R-3** | **License cho phép nhúng và dùng server-side** trong image phân phối | Hệ quả của điều **8** (font phải nằm **cùng runtime** với compositor) + điều **2** của [ADR-001](../../030-Specs/Architecture/ADR-001-Backend-And-Frontend-Tech-Stack.md) (file font đi theo image build một lần, push lên registry) ⇒ đây là **nhúng server-side**, ⛔ không phải webfont |
| **R-4** | ⭐ **Metric ổn định giữa các version** — và version font **phải được pin**, đổi version xử lý như **đổi font** | Đổi font = **wrap lại toàn bộ**, mọi bubble đã duyệt phải **đo lại**. Một bản cập nhật font đổi metric làm **mọi phép đo cũ hết hiệu lực im lặng** — cùng dạng hỏng với [đường hỏng ở trên](#-hai-hệ-font-—--không-gộp) |

### Nghiệm thu khi `TBD` đóng — ⛔ không được bỏ qua

[ADR-001](../../030-Specs/Architecture/ADR-001-Backend-And-Frontend-Tech-Stack.md) `## Consequences` **#5** ghi nguyên văn:

> *"**Nghiệm thu bắt buộc ở spike MVP0** (⛔ không được bỏ qua): corpus tiếng Việt gồm **cả NFC và NFD**, có dấu chồng (`ế`, `ữ`, `ợ`), render ở 300 DPI, kiểm tra (a) không ký tự nào bị tách khỏi dấu của nó khi xuống dòng, (b) không dấu nào bị cắt cụt bởi mép bubble, (c) chuỗi NFD và chuỗi NFC tương đương cho ra **cùng** kết quả ngắt dòng."*

⚠️ Ba tiêu chí đó là **hằng số của [ADR-001](../../030-Specs/Architecture/ADR-001-Backend-And-Frontend-Tech-Stack.md)**, ⛔ không phải ngưỡng do Design System đặt. Con số **300 DPI** cũng vậy.

> [!WARNING]
> ⛔ **Mọi phát biểu về ngắt dòng trong file này đều nói về compositor server-side.**
> Nếu editor có hiển thị thoại ở client, đó là **hiển thị KHÔNG chuẩn tắc**: nó ⛔ **không phải** kết quả wrap thật, và kết quả ngắt của nó ⛔ **KHÔNG BAO GIỜ** được gửi xuống backend ([ADR-001](../../030-Specs/Architecture/ADR-001-Backend-And-Frontend-Tech-Stack.md) điều 8: *"⛔ không được wrap ở frontend rồi gửi kết quả xuống"*).
> ⇒ ⛔ Design System **không đặc tả** `text-wrap` / `hyphens` / `word-break` cho **thoại bubble**. Component của editor đặc tả ở [Components](./Components.md) *(file thuộc lô khác)*, và phải mang đúng nhãn *không chuẩn tắc*.

---

## Tiếng Việt: line-height & dấu chồng

**Vấn đề vật lý:** tiếng Việt đặt **dấu thanh + dấu mũ/móc trên cùng một nguyên âm** — `ế`, `ộ`, `ữ`, `ượ`. Đó là **dấu chồng hai tầng** ⇒ **chiều cao thực của một dòng lớn hơn Latin thuần** ở cùng cỡ chữ.

> ⛔⛔ **KHÔNG copy giá trị line-height mặc định của một font Latin.** Mặc định đó được chỉnh cho chữ ⛔ **không có tầng dấu thứ hai**; áp thẳng vào tiếng Việt ⇒ dấu của dòng dưới **chạm hoặc chồng** vào phần bụng chữ của dòng trên.

**Căn cứ duy nhất repo có** — [findings/researcher.md](../../010-Planning/pm-runs/2026-08-23-danh-gia-y-tuong-comic-studio/findings/researcher.md) của run `2026-08-23`:

> *"Với tiếng Việt, thêm ràng buộc: line-height phải rộng hơn tiếng Anh vì dấu chồng ("ữ", "ế") ăn không gian phía trên; wrap phải dùng thư viện hiểu Unicode combining marks."*

> ⚠️ **Nhãn nguồn:** đây là **findings của một run trước**, ⛔ **KHÔNG phải requirement đã chốt**, và ⛔ **không kèm số đo nào**. Nó phát biểu **chiều** (rộng hơn), ⛔ không phát biểu **lượng**.

### Áp cho **cả hai** hệ, nhưng bằng hai cách khác nhau

| | **Hệ 1 — Font UI** | **Hệ 2 — Font render** |
|---|---|---|
| Có số trong file này không | ✅ Có — bảng token ở [Hệ 1](#hệ-1-—-font-ui) | ⛔ **KHÔNG. 0 số.** |
| Số đó là gì | **Quyết định Phase 3**: đã nới rộng so với mặc định Latin theo **chiều** mà findings nêu. ⛔ **Không phải kết quả đo**, ⛔ không trình bày như đã đo | Leading của bubble là **dẫn xuất từ metric của font thật** (ascender, cap height, chiều cao vùng dấu) ⇒ ⛔ **không chọn trước khi `TBD-FONT` đóng** |
| Sai thì hỏng ở đâu | Chữ chật trên form — sửa một token | ⭐ **Dấu bị mép bubble cắt** trong ảnh đã sinh — tiêu chí **(b)** của nghiệm thu MVP0 |
| Vì sao vẫn áp cho UI | Form Story Bible, danh sách nhân vật, bảng thoại **đầy chữ có dấu** — đây ⛔ không phải vấn đề riêng của bubble | — |

⚠️ **Ranh giới ⛔ không được vượt:** **chiều cao và kích thước của chính cái bubble** ⛔ **không thuộc file này**. Hình học panel/bubble là **toạ độ chuẩn hoá 0–1** ([ADR-013](../../030-Specs/Architecture/ADR-013-Typeset-Layer-Separate-From-Art.md) `## Decision` điều **2**), ⛔ không phải px của Design System — xem [Foundations](./Foundations.md) §*⛔ KHÔNG quản* hàng **1**, và [Spacing & Layout](./Spacing-And-Layout.md) *(file thuộc lô khác)*.

---

## NFC / NFD

[ADR-001](../../030-Specs/Architecture/ADR-001-Backend-And-Frontend-Tech-Stack.md) `## Decision` **điều 8** (**CHỐT**): *"Chuẩn hoá **NFC** ngay tại biên ingest."*

### ⭐ Vì sao đây là **điều kiện cần của phép đo đúng**, ⛔ không phải chi tiết lưu trữ

Cùng một chữ `ế` có **hai** cách biểu diễn Unicode: một code point dựng sẵn (**NFC**), hoặc một nguyên âm cơ sở + các combining mark rời (**NFD**). Với **con người** chúng là một chữ. Với **thuật toán đo** chúng là **hai chuỗi khác nhau**:

| Hệ quả | Vì sao |
|---|---|
| ⭐ **Đo ra chiều rộng khác nhau** | Font có thể có glyph dựng sẵn cho dạng NFC, còn dạng NFD phải dựng bằng mark positioning ⇒ advance width ⛔ không đảm bảo bằng nhau |
| **Ranh giới grapheme khác nhau** | `Intl.Segmenter` gom cluster đúng ở cả hai dạng, nhưng **số phần tử và nội dung cluster khác nhau** ⇒ mọi phép đếm dựa trên đó lệch |
| ⇒ **Ngắt dòng khác nhau** | Cùng một câu thoại, người dùng ⛔ không phân biệt được, nhưng compositor cho ra **hai kết quả** |

⇒ Chuẩn hoá NFC ⛔ **không phải** một quy ước lưu trữ cho gọn — nó là thứ làm cho **phép đo có một đáp án duy nhất**. Nghiệm thu **(c)** của [ADR-001](../../030-Specs/Architecture/ADR-001-Backend-And-Frontend-Tech-Stack.md) `## Consequences` **#5** đo đúng điều này: *"chuỗi NFD và chuỗi NFC tương đương cho ra **cùng** kết quả ngắt dòng"*.

### ⛔ Ba lệnh cấm cho tầng Design System

| # | ⛔ Cấm | Vì sao |
|:--:|---|---|
| **N-1** | ⛔ **Dán chuỗi mẫu tiếng Việt ở dạng NFD** vào bất kỳ tài liệu design, mockup hay ví dụ nào | ⭐ Đây là chỗ designer vô tình phá hệ thống: một chuỗi mẫu NFD được copy nguyên vào **test fixture**, rồi test pass trên đúng cái sai. **Mọi chuỗi mẫu tiếng Việt trong tầng 040 phải là NFC.** |
| **N-2** | ⛔ **Khai một chuẩn hoá Unicode thứ hai ở frontend** (NFD, NFKC…) | Chuẩn hoá xảy ra ở **đúng một chỗ**: biên ingest, phía server. Hai nơi chuẩn hoá = hai nguồn sự thật cho cùng một chuỗi |
| **N-3** | ⛔ **Đếm ký tự bằng `.length`** trong bất kỳ UI nào | Với dấu chồng, `.length` đếm **code unit**, ⛔ không đếm chữ. Mọi bộ đếm ký tự trong UI phải đếm theo **grapheme cluster**, và phải khai rõ nó là **hiển thị không chuẩn tắc** — ⛔ **không phải** nguồn sự thật của `text_budget` |

⚠️ **Ranh giới:** chiến lược **i18n / l10n** (đa ngôn ngữ, locale, RTL, collation) ⛔ **không thuộc Design System và ⛔ không được suy ra từ mục này**. [SRS](../../020-Requirements/SRS-Comic-Studio.md) §5.2 hàng **`b-6`** vẫn là **`TBD`**. Mục này chỉ nói về **một** thứ: chuẩn hoá Unicode như **điều kiện của phép đo**.

---

## Cỡ chữ bubble là HÀM của `text_budget`, ⛔ không phải giá trị chọn

> [!IMPORTANT]
> ⭐ **Design System phát biểu QUAN HỆ, ⛔ không phát biểu GIÁ TRỊ.** ⛔ **Không tồn tại một "type scale cho bubble"** trong tầng 040. Thang cỡ chữ ở [Hệ 1](#hệ-1-—-font-ui) áp cho **chrome của editor**, ⛔ **không áp cho chữ trong bubble**.

### `text_budget` là gì — verify trước khi dùng

| Điều đã verify | Nguồn |
|---|---|
| **Trần độ dài thoại của một bubble**, **tính từ diện tích panel** và `text_safe_zone` | [Glossary](../../999-Resources/Glossary.md) mục *`text_budget`* |
| Là **field của panel spec** (`comic.panel`), ⛔ **không nằm ở tầng typeset** | [Glossary](../../999-Resources/Glossary.md) · `ADR-012` `## Decision` điều **9** (trích gián tiếp qua [DB-Entity-Typeset-Layer](../../030-Specs/Schema/DB-Entity-Typeset-Layer.md) §Nguồn) |
| Là **giá trị DẪN XUẤT** — ⛔ **không request nào set trực tiếp**; `NULL` ⇒ chưa chạy condensation | [Endpoint-Page-Layout](../../030-Specs/API/Endpoint-Page-Layout.md) `API-PL-12` |
| **Đổi diện tích panel ⇒ tính lại `text_budget` ⇒ reset human gate #2 về `OPEN`** | [ADR-013](../../030-Specs/Architecture/ADR-013-Typeset-Layer-Separate-From-Art.md) `## Decision` điều **9** (`D-33`, `T1`/`T2`) |

### Quan hệ — phát biểu được ngay hôm nay

Cỡ chữ render trong một bubble bị **ràng buộc đồng thời** bởi ba thứ, ⛔ không phải do ai chọn:

1. **`text_budget` của panel** — trần độ dài thoại, tự nó đã là hàm của **diện tích panel**;
2. **Hình học bubble** — vùng khả dụng, sinh ra từ `text_safe_zone` và toạ độ **0–1** ([ADR-013](../../030-Specs/Architecture/ADR-013-Typeset-Layer-Separate-From-Art.md) điều **2**), ⛔ không phải px của Design System;
3. **Metric của font render** — chiều rộng thực của chuỗi, đo bằng **chính font sẽ render** ([ADR-001](../../030-Specs/Architecture/ADR-001-Backend-And-Frontend-Tech-Stack.md) `## Consequences` **#5**), cộng phần chiều cao mà [dấu chồng](#tiếng-việt-line-height--dấu-chồng) chiếm.

⇒ Cả ba đều là **đầu vào của compositor tại thời điểm composite**, ⛔ **không có cái nào là hằng số của Design System**.

### ⛔ Công thức là `TBD` CÓ CHỦ — file này ⛔ không phát biểu công thức

| Khoảng trống | Trạng thái | **Chủ** | Khi nào |
|---|---|---|---|
| **Đơn vị của `text_budget`** (ký tự hay từ) và **hàm tính từ diện tích panel** — `T-PL-BUDGET-UNIT` | ⛔ **`TBD`** | ⭐ **BA + Architect** | Trước gate `M2-3` |
| **Ánh xạ `text_budget` → cỡ chữ render** | ⛔ **`TBD`** — phụ thuộc **cả** hàng trên **và** `TBD-FONT` ([Hệ 2](#hệ-2-—-font-render-vào-ảnh)). ⭐ **Thứ tự đóng đã được chốt**: `TBD-FONT` **TRƯỚC**, hàm tính `text_budget` **SAU** — [ADR-013](../../030-Specs/Architecture/ADR-013-Typeset-Layer-Separate-From-Art.md) §*Thứ tự đóng hai `TBD`* | **Architect** (sau khi hai `TBD` kia đóng) | Sau MVP0 |

⚠️ ⛔ **Không bịa một công thức ở đây.** Một công thức bịa sẽ được tầng code và tầng QA dùng làm **chuẩn nghiệm thu** — và nó sẽ sai theo đúng kiểu im lặng đã mô tả ở [mục hai hệ font](#-hai-hệ-font-—--không-gộp).

### ⛔ Điều KHÔNG được suy ra từ file này

- ⛔ Không suy ra rằng file này chọn font render — [ADR-013](../../030-Specs/Architecture/ADR-013-Typeset-Layer-Separate-From-Art.md) sở hữu `TBD` đó, chủ là **Architect + Founder**.
- ⛔ Không suy ra rằng thang cỡ chữ UI dùng được cho bubble.
- ⛔ Không suy ra một công thức `text_budget`, một đơn vị của nó, hay một cỡ chữ bubble cụ thể.
- ⛔ Không suy ra một **danh mục kiểu bubble** (speech / thought / shout / whisper) — đó là `TBD` có chủ (**PM hỏi Founder**), [ADR-013](../../030-Specs/Architecture/ADR-013-Typeset-Layer-Separate-From-Art.md) bảng `TBD`.
- ⛔ Không suy ra rằng editor được phép wrap thoại rồi gửi kết quả xuống backend.
- ⛔ Không suy ra một chiến lược i18n/l10n — [SRS](../../020-Requirements/SRS-Comic-Studio.md) §5.2 `b-6` = **`TBD`**.

---

## Tài liệu tham khảo

> ⚠️ **Ghi nhận minh bạch**: tại **2026-08-30**, các tài liệu neo bên dưới (`ADR-001`, `ADR-013`, `SRS`, các spec tầng 030) đều ở `status: draft`. File này neo vào một nền **chưa `approved`**.
> ⚠️ Bản `ADR-001` trong worktree là **input read-only** của run này — ⛔ run này không commit `ADR-001`, và ⛔ không sửa bất kỳ ADR nào.

**Trong Design System**:

- [Foundations](./Foundations.md) — ⭐ **phải đọc trước**: hợp đồng phát biểu token (`HĐ-1`…`HĐ-3`), luật hình dạng `L1`…`L4`, chuẩn accessibility (**quyết định Phase 3**, `G-3`), §*Cách kiểm*
- [Brand Guidelines](./Brand-Guidelines.md) — tone của mọi chữ trong app shell
- [Color Tokens](./Color-Tokens.md) *(file thuộc lô khác)* — giá trị **màu chữ**; ⛔ file Typography không định nghĩa màu
- [Spacing & Layout](./Spacing-And-Layout.md) *(file thuộc lô khác)* — thang spacing; ⛔ file Typography không định nghĩa spacing
- [Components](./Components.md) *(file thuộc lô khác)* — component của editor, gồm hiển thị thoại **không chuẩn tắc** ở client

**Ngoài Design System**:

- [Design MOC](../Design-MOC.md) — bản đồ tầng 040
- ⭐⭐ [ADR-001 — Backend & Frontend Tech Stack](../../030-Specs/Architecture/ADR-001-Backend-And-Frontend-Tech-Stack.md) — `## Decision` điều **2**, **5**, **8** · `## Consequences` §Tiêu cực **#5** (segmentation ≠ đo · nghiệm thu MVP0)
- ⭐ [ADR-013 — Typeset Layer Separate From Art](../../030-Specs/Architecture/ADR-013-Typeset-Layer-Separate-From-Art.md) — `## Decision` điều **1**, **2**, **6**, **8**, **9** · §Alternatives **(e)**, **(f)** · bảng `TBD` hàng *Font sẽ render*
- [DB-Entity-Typeset-Layer](../../030-Specs/Schema/DB-Entity-Typeset-Layer.md) — `T-9` (NFC tại biên ingest) · `TBD-FONT`
- [Endpoint-Page-Layout](../../030-Specs/API/Endpoint-Page-Layout.md) — `API-PL-12` (`text_budget` là dẫn xuất) · `T-PL-BUDGET-UNIT` (đơn vị + hàm tính = `TBD`, chủ **BA + Architect**)
- ⭐ [ADR-013 — Typeset layer tách khỏi art](../../030-Specs/Architecture/ADR-013-Typeset-Layer-Separate-From-Art.md) — **sở hữu `TBD-FONT`**; §*Bốn ràng buộc mà font render phải thoả* (`R-1`…`R-4`) · §*Thứ tự đóng hai `TBD`* (`TBD-FONT` **trước** `T-PL-BUDGET-UNIT`)
- [Glossary](../../999-Resources/Glossary.md) — mục *typeset layer* · *`text_budget`* · *dialogue condensation*
- [SRS — Comic Studio](../../020-Requirements/SRS-Comic-Studio.md) — §5.2 hàng `b-6` (i18n/l10n = `TBD`)
- [RULE-001 — Documents Template](../../../knowledge-base/99-Templates/Documents-Template.md) — quy tắc **#5** (⛔ không wiki-link)

**Hồ sơ quyết định của run** (`2026-08-30-brand-guidelines-va-design-system-comic-studio`):

- [findings/product-designer.md](../../010-Planning/pm-runs/2026-08-30-brand-guidelines-va-design-system-comic-studio/findings/product-designer.md) — §5.1–5.4 (hai hệ font · sáu hệ quả `H-1`…`H-6` · bốn đường hỏng)
- [findings/architect.md](../../010-Planning/pm-runs/2026-08-30-brand-guidelines-va-design-system-comic-studio/findings/architect.md) — vùng **B**: `ARC-08`…`ARC-12`
- [findings/business-analyst.md](../../010-Planning/pm-runs/2026-08-30-brand-guidelines-va-design-system-comic-studio/findings/business-analyst.md) — §3.5 (hai hệ font, không phải một)
- [findings/researcher.md (run 2026-08-23)](../../010-Planning/pm-runs/2026-08-23-danh-gia-y-tuong-comic-studio/findings/researcher.md) — line-height tiếng Việt rộng hơn tiếng Anh vì dấu chồng ⚠️ **findings, ⛔ không phải requirement**
