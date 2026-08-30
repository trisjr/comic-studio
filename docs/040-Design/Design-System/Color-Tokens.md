---
id: DS-003
type: design-system
status: draft
project: comic-studio
owner: "@trisjr"
tags: [design-system, phase-3]
created: 2026-08-30
updated: 2026-08-30
---

# Color Tokens

> **Part of:** [Design MOC](../Design-MOC.md)
> **Tuân theo:** [Foundations](./Foundations.md) §Hợp đồng phát biểu token (`HĐ-1`, `HĐ-2`, `HĐ-3`) + bốn luật hình dạng (`L1`–`L4`)
> **Nguồn hướng màu:** [Brand Guidelines](./Brand-Guidelines.md) §Hướng màu chủ đạo
> **Nguồn quyết định:** `G-1` (trung tính + accent lạnh) · `G-2` (light default, khai đủ cặp) · `G-3` (WCAG 2.2 AA, luồng chính, desktop-first) — chốt tại gate run `2026-08-30-brand-guidelines-va-design-system-comic-studio`.

> [!IMPORTANT]
> ⭐ **Đây là BẢNG TRA cho AI assist sinh code, ⛔ không phải bài luận về màu.** Độc giả đích là `E2` của run ⇒ mọi mục phải **copy-paste được** hoặc **grep được**.
> ⭐ **File này là NGUỒN DUY NHẤT của mọi giá trị màu trong hệ.** Ai cần một màu ⇒ lấy token ở đây; ⛔ không khai lại hex ở file khác, ⛔ không arbitrary value tại chỗ dùng (`HĐ-3`).
> ⛔ **File này ⛔ không định nghĩa bất cứ thứ gì về font/cỡ chữ** — xem [Typography](./Typography.md) *(file thuộc lô khác)*.

## Mục lục

- [Primitive palette](#primitive-palette)
- [Semantic mapping](#semantic-mapping)
- [Bộ biến quy ước shadcn](#bộ-biến-quy-ước-shadcn)
- [Giá trị dark (khai sẵn, chưa implement)](#giá-trị-dark-khai-sẵn-chưa-implement)
- [Bảng audit contrast](#bảng-audit-contrast)
- [⭐ Màu trạng thái: BA MỨC phải phân biệt được](#-màu-trạng-thái-ba-mức-phải-phân-biệt-được)
- [Tài liệu tham khảo](#tài-liệu-tham-khảo)

---

## Primitive palette

> **Nhãn: toàn bộ giá trị trong mục này là *quyết định Phase 3*.** Repo ⛔ không có tầng token nào trước đó.
> ⚠️ **Về `L3` (đặt tên theo vai trò, ⛔ không theo bảng màu):** `L3` áp cho **tầng semantic** — tầng mà component tiêu thụ. Tầng primitive **theo bản chất là thang màu** ([Foundations](./Foundations.md) §Kiến trúc token: primitive = *"thang màu, thang spacing…"*) và **⛔ component ⛔ không được đọc nó** (`HĐ-3`) ⇒ tên dạng thang ở đây là hợp lệ, và **chỉ hợp lệ ở đây**.

### Vì sao đúng bốn dải này — ⛔ không phải khẩu vị

| Dải | Vai trò | Neo |
|---|---|---|
| **neutral** (xám ám lạnh) | Toàn bộ chrome: nền, bề mặt, viền, text | `G-1` lý do **1**: *"Artwork là nội dung; chrome phải lùi"* |
| **indigo** | ⭐ Accent thương hiệu ⇒ nguồn của vai trò *nhấn chính* | `G-1`; [Brand Guidelines](./Brand-Guidelines.md) ràng buộc kế thừa **1** |
| **red** + **amber** + **green** | Dải trạng thái: TỪ CHỐI · CẢNH BÁO · thành công | Xem [BA MỨC](#-màu-trạng-thái-ba-mức-phải-phân-biệt-được) |
| ⭐ **⛔ KHÔNG có dải blue riêng cho mức THÔNG TIN** | Mức THÔNG TIN dùng **neutral** | Xem [ràng buộc (d)](#ràng-buộc-accent-lạnh--không-được-đụng-dải-cảnh-báo) — blue-info sẽ **va vào chính accent indigo** |

### Thang giá trị

| Thang | Các bậc (hex) |
|---|---|
| `--neutral-0` … `--neutral-950` | `#FFFFFF` · `#F8FAFC` · `#F1F5F9` · `#E2E8F0` · `#CBD5E1` · `#94A3B8` · `#64748B` · `#475569` · `#334155` · `#1E293B` · `#0F172A` · `#020617` |
| `--indigo-50` … `--indigo-900` | `#EEF2FF` · `#E0E7FF` · `#C7D2FE` · `#A5B4FC` · `#818CF8` · `#6366F1` · `#4F46E5` · `#4338CA` · `#3730A3` · `#312E81` |
| `--red-50` … `--red-900` | `#FEF2F2` · `#FEE2E2` · `#FCA5A5` · `#F87171` · `#EF4444` · `#DC2626` · `#B91C1C` · `#991B1B` · `#450A0A` |
| `--amber-50` … `--amber-900` | `#FFFBEB` · `#FEF3C7` · `#FCD34D` · `#FBBF24` · `#F59E0B` · `#D97706` · `#B45309` · `#92400E` · `#451A03` |
| `--green-50` … `--green-900` | `#F0FDF4` · `#DCFCE7` · `#86EFAC` · `#4ADE80` · `#22C55E` · `#16A34A` · `#15803D` · `#166534` · `#052E16` |

### Block CSS — nửa PRIMITIVE của `:root {}`

> ⚠️ Đây là **nửa trên** của **cùng một** block `:root {}` trong `apps/web/src/index.css`. Nửa dưới (semantic) ở [mục sau](#block-css--nửa-semantic-của-root-). Dán **nối tiếp nhau**, ⛔ không tách thành hai block.

```css
:root {
  /* primitive — neutral (chrome) */
  --neutral-0:   #FFFFFF;
  --neutral-50:  #F8FAFC;
  --neutral-100: #F1F5F9;
  --neutral-200: #E2E8F0;
  --neutral-300: #CBD5E1;
  --neutral-400: #94A3B8;
  --neutral-500: #64748B;
  --neutral-600: #475569;
  --neutral-700: #334155;
  --neutral-800: #1E293B;
  --neutral-900: #0F172A;
  --neutral-950: #020617;

  /* primitive — indigo (accent thương hiệu) */
  --indigo-100: #E0E7FF;
  --indigo-300: #A5B4FC;
  --indigo-400: #818CF8;
  --indigo-600: #4F46E5;
  --indigo-700: #4338CA;
  --indigo-950: #1E1B4B;

  /* primitive — trạng thái */
  --red-50:    #FEF2F2;
  --red-300:   #FCA5A5;
  --red-400:   #F87171;
  --red-600:   #DC2626;
  --red-700:   #B91C1C;
  --red-950:   #450A0A;
  --amber-50:  #FFFBEB;
  --amber-300: #FCD34D;
  --amber-400: #FBBF24;
  --amber-700: #B45309;
  --amber-800: #92400E;
  --amber-950: #451A03;
  --green-50:  #F0FDF4;
  --green-300: #86EFAC;
  --green-400: #4ADE80;
  --green-700: #15803D;
  --green-950: #052E16;
```

---

## Semantic mapping

> ⭐ **Đây là tầng DUY NHẤT component được đọc** (`HĐ-3`). Mọi hàng đều có **đủ hai cột giá trị** light + dark (`L2`, `G-2`) và mọi token **nền** đều có **cặp `-foreground`** (`L1`).

### Bảng semantic — nền và chữ

| # | Vai trò (⭐ phần chuẩn) | Token nền | Light | Token chữ | Light | Dark (nền → chữ) |
|:--:|---|---|---|---|---|---|
| 1 | Nền cấp gốc của app shell | `--background` | `--neutral-0` | `--foreground` | `--neutral-900` | `--neutral-950` → `--neutral-100` |
| 2 | Bề mặt nổi: card, panel công cụ | `--card` | `--neutral-0` | `--card-foreground` | `--neutral-900` | `--neutral-900` → `--neutral-100` |
| 3 | Bề mặt nổi tạm: popover, dropdown | `--popover` | `--neutral-0` | `--popover-foreground` | `--neutral-900` | `--neutral-900` → `--neutral-100` |
| 4 | Nền **trầm**: text phụ, vùng đọc-thôi, hàng disabled | `--muted` | `--neutral-100` | `--muted-foreground` | `--neutral-600` | `--neutral-800` → `--neutral-400` |
| 5 | ⭐ **Nhấn chính** — hành động chính; nguồn là accent thương hiệu | `--primary` | `--indigo-600` | `--primary-foreground` | `--neutral-0` | `--indigo-400` → `--neutral-900` |
| 6 | Hành động **thứ cấp** | `--secondary` | `--neutral-100` | `--secondary-foreground` | `--neutral-900` | `--neutral-800` → `--neutral-100` |
| 7 | ⚠️ Bề mặt **hover/selected** của item trong list & menu (⛔ **không** phải accent thương hiệu — xem [bẫy tên biến](#bẫy-tên-biến-accent-của-shadcn--không-phải-accent-thương-hiệu)) | `--accent` | `--neutral-100` | `--accent-foreground` | `--neutral-900` | `--neutral-800` → `--neutral-100` |
| 8 | Nền hành động **phá huỷ** (xoá tenant, reset) | `--destructive` | `--red-600` | `--destructive-foreground` | `--neutral-0` | `--red-400` → `--red-950` |
| 9 | ⭐ Alert mức **TỪ CHỐI** — bề mặt nhạt | `--danger-subtle` | `--red-50` | `--danger-subtle-foreground` | `--red-700` | `--red-950` → `--red-300` |
| 10 | ⭐ Alert mức **TỪ CHỐI** — bề mặt đặc (badge, viền, icon) | `--danger` | `--red-700` | `--danger-foreground` | `--neutral-0` | `--red-400` → `--red-950` |
| 11 | ⭐ Alert mức **CẢNH BÁO** — bề mặt nhạt | `--warning-subtle` | `--amber-50` | `--warning-subtle-foreground` | `--amber-800` | `--amber-950` → `--amber-300` |
| 12 | ⭐ Alert mức **CẢNH BÁO** — bề mặt đặc | `--warning` | `--amber-700` | `--warning-foreground` | `--neutral-0` | `--amber-400` → `--amber-950` |
| 13 | ⭐ Alert mức **THÔNG TIN** — bề mặt nhạt | `--info-subtle` | `--neutral-100` | `--info-subtle-foreground` | `--neutral-700` | `--neutral-800` → `--neutral-300` |
| 14 | ⭐ Alert mức **THÔNG TIN** — bề mặt đặc | `--info` | `--neutral-500` | `--info-foreground` | `--neutral-0` | `--neutral-400` → `--neutral-900` |
| 15 | Trạng thái **thành công** (gate `PASS`, job xong) — nhạt | `--success-subtle` | `--green-50` | `--success-subtle-foreground` | `--green-700` | `--green-950` → `--green-300` |
| 16 | Trạng thái **thành công** — đặc | `--success` | `--green-700` | `--success-foreground` | `--neutral-0` | `--green-400` → `--green-950` |
| 17 | ⭐ **Vùng canvas / preview trang** — trung tính **CỐ ĐỊNH ở cả hai mode** | `--canvas` | `--neutral-200` | `--canvas-foreground` | `--neutral-900` | `--neutral-200` → `--neutral-900` |

> ⭐ **Hàng 17 là hàng cố ý giống nhau ở hai mode.** Đây ⛔ **không** phải lỗi thiếu giá trị dark — nó là **hệ quả của chính lý do `G-2`** ([Foundations](./Foundations.md) §Chiến lược light/dark): preview trang comic có **nền trắng giấy**; nếu khung bao quanh đổi theo mode thì **cảm nhận độ sáng của tấm ảnh người dùng đang đánh giá bị lệch**. Nhãn: **quyết định Phase 3**.
> ⚠️ Hàng 8 và hàng 10 **cùng dải đỏ nhưng ⛔ không được gộp**: `--destructive` là **hành động của NGƯỜI** (nút bấm được), `--danger` là **phán quyết của HỆ THỐNG** (một trạng thái, ⛔ không bấm được). Gộp ⇒ người dùng bấm vào một câu thông báo. Giá trị khác bậc (`--red-600` vs `--red-700`) để hai thứ ⛔ không trông y hệt.

### Bảng semantic — token ⛔ KHÔNG cần cặp `-foreground`

> Miễn trừ `L1` cho đúng bốn token dưới, theo [Foundations](./Foundations.md) §Tên biến (hai hàng cuối bảng ghi ⛔ **không** cần cặp chữ vì ⛔ không phải nền chứa text).

| Token | Vai trò | Light | Dark | Vì sao miễn `L1` |
|---|---|---|---|---|
| `--border` | Viền phân tách **trang trí** (card, separator) | `--neutral-200` | `--neutral-700` | ⛔ Không chứa text |
| `--input` | ⭐ Viền của **control nhập liệu** — là thứ **duy nhất** chỉ ra ranh giới của input | `--neutral-500` | `--neutral-500` | ⛔ Không chứa text, **nhưng phải đạt ≥ 3:1** vì nó mang thông tin (xem [audit](#bảng-audit-contrast)) |
| `--ring` | Vòng focus | `--indigo-600` | `--indigo-300` | ⛔ Không chứa text; phải đạt ≥ 3:1 với nền kề |
| `--overlay` | Scrim sau modal | `rgb(2 6 23 / 0.60)` | `rgb(2 6 23 / 0.75)` | Là **màn che**, ⛔ không chứa text — text nằm trên `--popover`/`--card` của dialog |

| Token phụ trợ | Vai trò | Light | Dark |
|---|---|---|---|
| `--shadow-color` | ⭐ Màu gốc của elevation, dạng RGB triplet để hợp thành alpha. **Hình học bóng** (offset/blur/thang) thuộc [Spacing & Layout](./Spacing-And-Layout.md); **giá trị màu** thuộc file này | `15 23 42` | `0 0 0` |

### Block CSS — nửa SEMANTIC của `:root {}`

```css
  /* semantic — bề mặt & chữ */
  --background: var(--neutral-0);
  --foreground: var(--neutral-900);
  --card: var(--neutral-0);
  --card-foreground: var(--neutral-900);
  --popover: var(--neutral-0);
  --popover-foreground: var(--neutral-900);
  --muted: var(--neutral-100);
  --muted-foreground: var(--neutral-600);

  /* semantic — hành động */
  --primary: var(--indigo-600);
  --primary-foreground: var(--neutral-0);
  --secondary: var(--neutral-100);
  --secondary-foreground: var(--neutral-900);
  --accent: var(--neutral-100);
  --accent-foreground: var(--neutral-900);
  --destructive: var(--red-600);
  --destructive-foreground: var(--neutral-0);

  /* semantic — alert BA MỨC + thành công */
  --danger: var(--red-700);
  --danger-foreground: var(--neutral-0);
  --danger-subtle: var(--red-50);
  --danger-subtle-foreground: var(--red-700);
  --warning: var(--amber-700);
  --warning-foreground: var(--neutral-0);
  --warning-subtle: var(--amber-50);
  --warning-subtle-foreground: var(--amber-800);
  --info: var(--neutral-500);
  --info-foreground: var(--neutral-0);
  --info-subtle: var(--neutral-100);
  --info-subtle-foreground: var(--neutral-700);
  --success: var(--green-700);
  --success-foreground: var(--neutral-0);
  --success-subtle: var(--green-50);
  --success-subtle-foreground: var(--green-700);

  /* semantic — vùng nội dung, viền, focus, scrim */
  --canvas: var(--neutral-200);
  --canvas-foreground: var(--neutral-900);
  --border: var(--neutral-200);
  --input: var(--neutral-500);
  --ring: var(--indigo-600);
  --overlay: rgb(2 6 23 / 0.60);
  --shadow-color: 15 23 42;
}
```

### Block `theme.extend` cho `tailwind.config.ts`

> `HĐ-2`: Tailwind **chỉ được tham chiếu**. ⛔ **0 hex** trong block này — đây là điều `K-8` kiểm.

```ts
export default {
  theme: {
    extend: {
      colors: {
        background: "var(--background)",
        foreground: "var(--foreground)",
        card: { DEFAULT: "var(--card)", foreground: "var(--card-foreground)" },
        popover: { DEFAULT: "var(--popover)", foreground: "var(--popover-foreground)" },
        muted: { DEFAULT: "var(--muted)", foreground: "var(--muted-foreground)" },
        primary: { DEFAULT: "var(--primary)", foreground: "var(--primary-foreground)" },
        secondary: { DEFAULT: "var(--secondary)", foreground: "var(--secondary-foreground)" },
        accent: { DEFAULT: "var(--accent)", foreground: "var(--accent-foreground)" },
        destructive: { DEFAULT: "var(--destructive)", foreground: "var(--destructive-foreground)" },
        danger: { DEFAULT: "var(--danger)", foreground: "var(--danger-foreground)" },
        "danger-subtle": { DEFAULT: "var(--danger-subtle)", foreground: "var(--danger-subtle-foreground)" },
        warning: { DEFAULT: "var(--warning)", foreground: "var(--warning-foreground)" },
        "warning-subtle": { DEFAULT: "var(--warning-subtle)", foreground: "var(--warning-subtle-foreground)" },
        info: { DEFAULT: "var(--info)", foreground: "var(--info-foreground)" },
        "info-subtle": { DEFAULT: "var(--info-subtle)", foreground: "var(--info-subtle-foreground)" },
        success: { DEFAULT: "var(--success)", foreground: "var(--success-foreground)" },
        "success-subtle": { DEFAULT: "var(--success-subtle)", foreground: "var(--success-subtle-foreground)" },
        canvas: { DEFAULT: "var(--canvas)", foreground: "var(--canvas-foreground)" },
        border: "var(--border)",
        input: "var(--input)",
        ring: "var(--ring)",
        overlay: "var(--overlay)",
      },
    },
  },
};
```

---

## Bộ biến quy ước shadcn

> [!CAUTION]
> ⛔⛔ **Toàn bộ danh sách tên biến trong file này là *QUYẾT ĐỊNH PHASE 3*.**
> ⚠️ [ADR-001](../../030-Specs/Architecture/ADR-001-Backend-And-Frontend-Tech-Stack.md) chốt **stack** (*shadcn/ui + Tailwind CSS*) và ⛔ **KHÔNG nêu một tên biến CSS nào** — vì vậy ⛔ **không có câu nào trong file này trích ADR-001 làm nguồn cho tên biến**. Đây là điều `K-9` kiểm.
> ⚠️ Repo ⛔ **chưa có `package.json`** ⇒ ⛔ **không verify được version của shadcn** ⇒ tên biến **PHẢI kiểm lại khi khởi tạo dự án** (đọc `components.json` + file CSS do bản `init` thật sinh ra).

### Ba nhóm tên — mức độ chắc chắn ⛔ không như nhau

| Nhóm | Token | Trạng thái tên |
|---|---|---|
| **A — tên quy ước phổ biến** | `--background` · `--foreground` · `--primary` · `--primary-foreground` | *Quyết định Phase 3*, ⚠️ **cần verify khi init** |
| **B — vai trò chắc, tên chưa chắc** | Bề mặt nổi · hành động thứ cấp · nền trầm · hành động phá huỷ · viền · viền input · vòng focus | ⭐ **Cột chuẩn là cột VAI TRÒ** ở [bảng semantic](#semantic-mapping). ⚠️ **Tên: verify khi init** |
| **C — bổ sung của dự án** | `--danger-*` · `--warning-*` · `--info-*` · `--success-*` · `--canvas*` · `--overlay` · `--shadow-color` | ⭐ ⛔ **Không** thuộc bộ quy ước nào — là **quyết định Phase 3** của riêng sản phẩm này. Vẫn phải thoả `L1` + `L2` |

### Bẫy tên biến: `accent` của shadcn ⛔ không phải accent thương hiệu

> [!WARNING]
> ⭐ **Đây là chỗ dễ sai nhất khi map hướng màu vào bộ biến.**
> Trong bộ quy ước, `--accent` là **bề mặt hover/selected của item trong list & menu** — một màu **trầm, gần như vô hình**. Accent **thương hiệu** (indigo) ánh xạ vào **`--primary`**, ⛔ **không** vào `--accent`.
> Đổ indigo vào `--accent` ⇒ **mọi hàng list bị hover đều sáng rực màu thương hiệu** ⇒ vi phạm thẳng lý do **1** của `G-1` (*chrome phải lùi*), và làm hỏng luôn phân biệt *"đang hover"* với *"đang là hành động chính"*.

### Bẫy định dạng giá trị

> ⚠️ Định dạng mà bộ quy ước dùng cho biến màu (**channel triplet HSL** kiểu `0 0% 100%` dùng qua `hsl(var(--x))`, hay **OKLCH**, hay hex thẳng) **thay đổi theo version** và ⛔ **không verify được ở thời điểm này**.
> ⇒ Khi init: **chuyển ĐỊNH DẠNG cho khớp bản init thật, ⛔ KHÔNG đổi GIÁ TRỊ.** Giá trị nguồn là cột hex ở [Primitive palette](#primitive-palette). Đổi giá trị ⇒ [bảng audit contrast](#bảng-audit-contrast) **mất hiệu lực toàn bộ**.

### Ranh giới file — ⛔ không lấn sang lô khác

| Thứ | Ở đâu |
|---|---|
| Cỡ chữ, cân nặng chữ, line-height, họ font | [Typography](./Typography.md) *(file thuộc lô khác)* — ⛔ file này ⛔ không đặt một giá trị chữ nào |
| Hình học bóng, thang spacing, radius, breakpoint, z-index | [Spacing & Layout](./Spacing-And-Layout.md) |
| Component nào dùng token nào, ma trận state | [Components](./Components.md) *(file thuộc lô khác)* |

---

## Giá trị dark (khai sẵn, chưa implement)

> **`G-2` — chốt tại gate:** **Light là default. Dark ⛔ CHƯA implement ở MVP**, nhưng token khai **đủ cặp ngay** ⇒ ⛔ không retrofit về sau.
> ⭐ Selector `.dark {}` **phải tồn tại** trong `index.css` kể cả khi ⛔ chưa ai bật nó ([Foundations](./Foundations.md) §Chiến lược light/dark, cột *⛔ KHÔNG được hoãn*).

> [!NOTE]
> ⚠️ **Nghiệm thu contrast cho cột dark là việc ĐƯỢC HOÃN** ([Foundations](./Foundations.md) §Chiến lược light/dark, cột *Được hoãn*).
> ⇒ [Bảng audit contrast](#bảng-audit-contrast) chỉ chứa số **thật** cho **light**. Cột dark ở đây là **giá trị đã khai**, ⛔ **chưa audit** — ⛔ **không được ghi *"đạt AA"*** cho dark khi chưa có số. Trước khi bật dark: audit lại **toàn bộ** cặp bằng đúng phương pháp ở mục audit.

```css
.dark {
  --background: var(--neutral-950);
  --foreground: var(--neutral-100);
  --card: var(--neutral-900);
  --card-foreground: var(--neutral-100);
  --popover: var(--neutral-900);
  --popover-foreground: var(--neutral-100);
  --muted: var(--neutral-800);
  --muted-foreground: var(--neutral-400);

  --primary: var(--indigo-400);
  --primary-foreground: var(--neutral-900);
  --secondary: var(--neutral-800);
  --secondary-foreground: var(--neutral-100);
  --accent: var(--neutral-800);
  --accent-foreground: var(--neutral-100);
  --destructive: var(--red-400);
  --destructive-foreground: var(--red-950);

  --danger: var(--red-400);
  --danger-foreground: var(--red-950);
  --danger-subtle: var(--red-950);
  --danger-subtle-foreground: var(--red-300);
  --warning: var(--amber-400);
  --warning-foreground: var(--amber-950);
  --warning-subtle: var(--amber-950);
  --warning-subtle-foreground: var(--amber-300);
  --info: var(--neutral-400);
  --info-foreground: var(--neutral-900);
  --info-subtle: var(--neutral-800);
  --info-subtle-foreground: var(--neutral-300);
  --success: var(--green-400);
  --success-foreground: var(--green-950);
  --success-subtle: var(--green-950);
  --success-subtle-foreground: var(--green-300);

  --canvas: var(--neutral-200);
  --canvas-foreground: var(--neutral-900);
  --border: var(--neutral-700);
  --input: var(--neutral-500);
  --ring: var(--indigo-300);
  --overlay: rgb(2 6 23 / 0.75);
  --shadow-color: 0 0 0;
}
```

### Ba điều đã biết trước cho lô dark

| # | Điều |
|:--:|---|
| **1** | ⭐ `--canvas` **cố ý giữ nguyên** giá trị ở `.dark` — xem ghi chú hàng 17 ở [semantic mapping](#semantic-mapping) |
| **2** | Ở dark, **đảo cực foreground của bề mặt đặc**: `--danger`/`--warning`/`--success` chuyển sang bậc **sáng** với chữ **tối**. Giữ nguyên bậc tối của light trên nền tối sẽ làm badge biến mất vào nền |
| **3** | Bóng đổ hoạt động **khác hẳn** trên nền tối — xử lý ở [Spacing & Layout](./Spacing-And-Layout.md) §Radius / border / elevation, ⛔ không xử lý ở file này |

---

## Bảng audit contrast

> [!IMPORTANT]
> ⭐ **Nhãn nguồn — đọc trước khi dùng bảng:**
> - **Chuẩn WCAG 2.2 Level AA, phạm vi luồng chính, desktop-first** là **quyết định Phase 3** (`G-3`), phát biểu tại [Foundations](./Foundations.md) §Chuẩn accessibility. ⛔ **Không** phải requirement kế thừa — toàn `docs/020-Requirements/` ⛔ không có một dòng nào về chủ đề này.
> - **Ngưỡng 4.5:1 và 3:1 là hằng số quy phạm trích từ văn bản chuẩn WCAG 2.2** (SC 1.4.3 và SC 1.4.11) — ⛔ **không phải số tự đặt**, ⛔ không phải NFR của repo.
> - **Cách tính cột *Tỷ lệ***: công thức relative luminance của WCAG (sRGB, hệ số `0.2126 / 0.7152 / 0.0722`), tỷ lệ `(L1 + 0.05) / (L2 + 0.05)`, **làm tròn XUỐNG** 2 chữ số thập phân ⇒ số ghi ở đây **≤ số thật**.
> - ⚠️ Bảng này là **bảng tra**, ⛔ **không thay phép đo trên UI thật**: màu chồng alpha, scrim, và text đặt trên ảnh preview **phải đo lại tại chỗ**.
> - Phạm vi: **light mode**. Dark ⛔ chưa audit — [xem mục trên](#giá-trị-dark-khai-sẵn-chưa-implement).

### Cặp text / nền của luồng chính

| # | Cặp | Chữ | Nền | **Tỷ lệ** | Ngưỡng áp dụng | Kết luận |
|:--:|---|---|---|:--:|---|:--:|
| 1 | Text chính trên nền app | `#0F172A` | `#FFFFFF` | **17.85:1** | 4.5:1 (text thường) | ✅ |
| 2 | Text chính trên bề mặt trầm nhất | `#0F172A` | `#F8FAFC` | **17.06:1** | 4.5:1 | ✅ |
| 3 | Text chính trên `--muted` | `#0F172A` | `#F1F5F9` | **16.29:1** | 4.5:1 | ✅ |
| 4 | ⭐ Text trên vùng `--canvas` (khung preview) | `#0F172A` | `#E2E8F0` | **14.48:1** | 4.5:1 | ✅ |
| 5 | Text phụ trên nền app | `#475569` | `#FFFFFF` | **7.57:1** | 4.5:1 | ✅ |
| 6 | Text phụ trên `--muted` | `#475569` | `#F1F5F9` | **6.91:1** | 4.5:1 | ✅ |
| 7 | ⭐ Chữ trên nút **nhấn chính** | `#FFFFFF` | `#4F46E5` | **6.28:1** | 4.5:1 | ✅ |
| 8 | ⭐ Text/link màu nhấn trên nền app | `#4F46E5` | `#FFFFFF` | **6.28:1** | 4.5:1 | ✅ |
| 9 | Chữ trên nút nhấn chính ở trạng thái **nhấn xuống** | `#FFFFFF` | `#4338CA` | **7.90:1** | 4.5:1 | ✅ |
| 10 | Chữ trên nút **phá huỷ** | `#FFFFFF` | `#DC2626` | **4.82:1** | 4.5:1 | ✅ |

### Cặp của BA MỨC alert + thành công

| # | Cặp | Chữ | Nền | **Tỷ lệ** | Ngưỡng | Kết luận |
|:--:|---|---|---|:--:|---|:--:|
| 11 | ⭐ **TỪ CHỐI** — chữ trên bề mặt nhạt | `#B91C1C` | `#FEF2F2` | **5.91:1** | 4.5:1 | ✅ |
| 12 | ⭐ **TỪ CHỐI** — chữ trên bề mặt đặc | `#FFFFFF` | `#B91C1C` | **6.46:1** | 4.5:1 | ✅ |
| 13 | ⭐ **CẢNH BÁO** — chữ trên bề mặt nhạt | `#92400E` | `#FFFBEB` | **6.83:1** | 4.5:1 | ✅ |
| 14 | ⭐ **CẢNH BÁO** — chữ trên bề mặt đặc | `#FFFFFF` | `#B45309` | **5.02:1** | 4.5:1 | ✅ |
| 15 | ⭐ **THÔNG TIN** — chữ trên bề mặt nhạt | `#334155` | `#F1F5F9` | **9.45:1** | 4.5:1 | ✅ |
| 16 | ⭐ **THÔNG TIN** — chữ trên bề mặt đặc | `#FFFFFF` | `#64748B` | **4.75:1** | 4.5:1 | ✅ |
| 17 | Thành công — chữ trên bề mặt nhạt | `#15803D` | `#F0FDF4` | **4.79:1** | 4.5:1 | ✅ |
| 18 | Thành công — chữ trên bề mặt đặc | `#FFFFFF` | `#15803D` | **5.01:1** | 4.5:1 | ✅ |
| 19 | Chữ chung trên bề mặt TỪ CHỐI nhạt | `#0F172A` | `#FEF2F2` | **16.32:1** | 4.5:1 | ✅ |
| 20 | Chữ chung trên bề mặt CẢNH BÁO nhạt | `#0F172A` | `#FFFBEB` | **17.21:1** | 4.5:1 | ✅ |

### Thành phần UI & đồ hoạ mang nghĩa (ngưỡng 3:1 — SC 1.4.11)

| # | Thành phần | Màu | Nền kề | **Tỷ lệ** | Kết luận |
|:--:|---|---|---|:--:|:--:|
| 21 | ⭐ **Viền input** `--input` | `#64748B` | `#FFFFFF` | **4.75:1** | ✅ |
| 22 | ⭐ **Vòng focus** `--ring` trên nền app | `#4F46E5` | `#FFFFFF` | **6.28:1** | ✅ |
| 23 | ⭐ **Vòng focus** trên bề mặt trầm | `#4F46E5` | `#F8FAFC` | **6.00:1** | ✅ |
| 24 | Viền/icon của alert **TỪ CHỐI** | `#DC2626` | `#FEF2F2` | **4.41:1** | ✅ |
| 25 | Viền/icon của alert **CẢNH BÁO** | `#B45309` | `#FFFBEB` | **4.84:1** | ✅ |
| 26 | Viền/icon của alert **THÔNG TIN** | `#64748B` | `#F1F5F9` | **4.34:1** | ✅ |
| 27 | Viền/icon **thành công** | `#15803D` | `#F0FDF4` | **4.79:1** | ✅ |

### ⛔ Ba màu KHÔNG đạt 3:1 — và vì sao vẫn được dùng

> ⚠️ **Ba màu dưới đây nằm NGOÀI bảng 27 hàng ở trên.** Bảng 27 hàng là các cặp của luồng chính và **cả 27 đều đạt ngưỡng**; ba màu này được tách riêng vì chúng **cố ý không đạt** và chỉ hợp lệ trong phạm vi hẹp đã ghi ở cột cuối. ⛔ Đừng gộp hai bảng khi trích dẫn — chúng trả lời hai câu hỏi khác nhau.

| Màu | Nền | **Tỷ lệ** | Được dùng cho | ⛔ CẤM dùng cho |
|---|---|:--:|---|---|
| `#E2E8F0` (`--border`) | `#FFFFFF` | **1.23:1** | Đường phân tách **trang trí** — ⛔ không mang thông tin | ⛔ Viền của bất kỳ control nào; ⛔ ranh giới duy nhất của một vùng bấm được |
| `#CBD5E1` | `#FFFFFF` | **1.48:1** | Nền của track/rãnh trang trí | ⛔ Text; ⛔ icon mang nghĩa; ⛔ viền input |
| `#94A3B8` | `#FFFFFF` | **2.56:1** | Chữ của **trạng thái disabled** (SC 1.4.3 loại trừ text của control không hoạt động) | ⛔ Mọi text đang hoạt động; ⛔ mọi thành phần UI mang nghĩa |

> ⭐ **Đây là lý do `--input` ⛔ KHÔNG dùng cùng giá trị với `--border`.** Trực giác nói *"viền là viền"*, nhưng viền input là thứ **duy nhất** nói cho người dùng biết ô nhập ở đâu ⇒ nó **mang thông tin** ⇒ **≥ 3:1**; còn separator giữa hai card thì ⛔ không.

---

## ⭐ Màu trạng thái: BA MỨC phải phân biệt được

> [!CAUTION]
> ⭐⭐ **Đây là mục quan trọng nhất của file.** Alert ba mức xuất hiện ở **13 surface** — nhiều nhất toàn hệ ⇒ **sai một lần là sai xuyên 13 màn hình**.

### Vì sao trộn ba mức là lỗi NGHIỆP VỤ, ⛔ không phải lỗi thẩm mỹ

⭐ **Ba mức trả lời ba câu hỏi khác nhau về *quyền hành động của người dùng*:** *"việc này đã bị chặn"* · *"việc này đi tiếp được nhưng anh nên nhìn lại"* · *"việc này bình thường, chỉ là chưa có"*.

⇒ **Nếu chúng trông giống nhau, người dùng học cách bỏ qua cả ba.** Và cái bị bỏ qua cùng lượt chính là mức **TỪ CHỐI** — mức mà [findings/business-analyst](../../010-Planning/pm-runs/2026-08-30-brand-guidelines-va-design-system-comic-studio/findings/business-analyst.md) §2.1 `C-01` ghi nguyên văn: ***"bị từ chối, KHÔNG PHẢI bị cảnh báo"***.

⚠️ Đây là lý do màu ở đây ⛔ **không được chọn theo thẩm mỹ**: một cảnh báo bị hiểu nhầm thành thông tin ⇒ người dùng đi tiếp với một trang sai; một **từ chối** bị hiểu nhầm thành cảnh báo ⇒ người dùng **ngồi chờ một thao tác đã không bao giờ xảy ra**.

### Ba mức — token, màu, và UC thật

| Mức | Nghĩa nghiệp vụ | Token | Dải màu | ⭐ UC thật (nguyên văn nguồn) |
|---|---|---|---|---|
| ⛔ **TỪ CHỐI** ở tầng DB/pipeline | Hệ thống **đã chặn**. ⛔ Không có nút *"cứ tiếp tục"* | `--danger-subtle` / `--danger` | **Đỏ** `--red-700` | `M2-2` — ***"bị từ chối, KHÔNG PHẢI bị cảnh báo"*** (`UC-03` `EXC-1`, `UC-07` `EX-7`, `UC-08` `EX-6`) · `M2-4` từ chối export (`UC-09` `EF-1`) · chặn opt-out (`UC-01` `EXC-1`) |
| ⚠️ **CẢNH BÁO** cho qua được | Đi tiếp **được**, nhưng có hệ quả người dùng nên biết | `--warning-subtle` / `--warning` | **Hổ phách** `--amber-700` / `--amber-800` | `M2-3` bubble **đè vùng mặt** (`UC-07` `EX-1`) · sửa `story_order` (`UC-02` `EXC-5`) |
| ℹ️ **THÔNG TIN** không phải lỗi | ⛔ **Không có gì hỏng cả.** Chỉ là một sự thật về phạm vi hiện tại | `--info-subtle` / `--info` | ⭐ **Trung tính** `--neutral-500` / `--neutral-700` | CBZ / webtoon ***"chưa có"*** (`UC-09` `EF-2`) |

### ⭐ Vì sao mức THÔNG TIN là TRUNG TÍNH, ⛔ không phải xanh dương

| # | Lý do |
|:--:|---|
| **1** | ⭐ **Xanh dương va thẳng vào accent thương hiệu.** `--primary` là indigo (`G-1`) ⇒ một info alert màu xanh sẽ **trông y hệt một hành động chính**. Người dùng đi tìm nút bấm trong một câu thông báo |
| **2** | ⭐ **Trung tính nói đúng nghĩa của mức này.** `UC-09` `EF-2` là *"chưa có"* — ⛔ không phải lỗi, ⛔ không phải cảnh báo, ⛔ không phải hành động. Màu trung tính là **màu duy nhất ⛔ không đòi phản ứng** |
| **3** | **Trung tính giữ được lý do 1 của `G-1`**: chrome lùi lại sau artwork. Info alert là mức xuất hiện **thường xuyên nhất** — nó ⛔ không được là thứ sáng nhất màn hình |

### ⛔ Màu MỘT MÌNH ⛔ không đủ để phân biệt ba mức

> [!WARNING]
> ⭐ **Đỏ và hổ phách nằm gần nhau trên trục sắc độ** — với người mù màu đỏ-lục (protanopia/deuteranopia), **mức TỪ CHỐI và mức CẢNH BÁO có thể sụp vào nhau**. Ngưỡng contrast ở [bảng audit](#bảng-audit-contrast) ⛔ **không** cứu được việc này: contrast đo *chữ trên nền*, ⛔ không đo *mức này khác mức kia*.
> ⇒ **Quyết định Phase 3 — ràng buộc cứng cho lô component:** mỗi mức **BẮT BUỘC** mang **ba tín hiệu đồng thời**, ⛔ không được rút xuống còn một:
> 1. **Cặp token màu riêng** (mục này) — ⛔ không chia sẻ token giữa hai mức
> 2. **Icon riêng, hình dạng khác nhau** — ⛔ không phải cùng một icon đổi màu
> 3. **Nhãn chữ nói thẳng mức độ** — người dùng đọc được *"đã bị từ chối"* mà ⛔ không cần nhìn màu
>
> ⛔ **File này ⛔ không đặc tả icon và nhãn** — chúng thuộc [Components](./Components.md) *(file thuộc lô khác)*. File này chỉ chốt: **token màu ⛔ không được là tín hiệu duy nhất.**

### Ràng buộc: accent lạnh ⛔ KHÔNG được đụng dải cảnh báo

> **`G-1` lý do 2 (nguyên văn [Brand Guidelines](./Brand-Guidelines.md)):** *"nếu accent thương hiệu rơi vào dải hổ phách/đỏ/xanh lá của trạng thái, người dùng ⛔ không phân biệt được 'đây là hành động chính' với 'đây là cảnh báo'"*.

**Cách hệ này tránh — bốn ràng buộc grep được:**

| # | Ràng buộc | Kiểm bằng |
|:--:|---|---|
| **1** | Accent thương hiệu chỉ nằm ở dải **indigo**; dải trạng thái chỉ nằm ở **red / amber / green / neutral**. ⭐ **Hai tập ⛔ không giao nhau** | Đọc [Primitive palette](#primitive-palette): ⛔ 0 bậc dùng chung |
| **2** | ⛔ **CẤM dùng `--primary` để biểu đạt trạng thái** (kể cả *"đang xử lý"*, *"đã lưu"*) | `grep` chỗ dùng `--primary` — phải là **hành động bấm được** hoặc **link** |
| **3** | ⛔ **CẤM dùng token trạng thái cho hành động chính** — nút chính ⛔ không bao giờ màu đỏ/hổ phách/xanh lá. Ngoại lệ **duy nhất**: `--destructive` cho hành động phá huỷ, và nó là một **vai trò riêng** (hàng 8) | Đọc [semantic mapping](#semantic-mapping) |
| **4** | ⭐ **Mức THÔNG TIN ⛔ không được là xanh dương** — nếu không, ràng buộc 1 tự vỡ từ bên trong | `grep -n "info" ` block `:root` — giá trị phải là bậc `--neutral-*` |

**Câu hỏi kiểm bắt buộc** trước khi chốt **bất kỳ** giá trị màu mới ([Brand Guidelines](./Brand-Guidelines.md) §Hướng màu chủ đạo):
> ***"Màu này có cạnh tranh với artwork mà người dùng đang đánh giá không? Nó có bị nhầm với một mức cảnh báo không?"***

### Một hệ quả từ tầng dữ liệu: trạng thái gate ⛔ không phải trạng thái vĩnh viễn

⚠️ [ADR-013](../../030-Specs/Architecture/ADR-013-Typeset-Layer-Separate-From-Art.md) §Decision **9** quy định **hai trigger reset gate**: `T1` (diện tích panel đổi) reset **mọi dòng thuộc panel bị ảnh hưởng**; `T2` (nội dung thoại bị sửa) reset **đúng một dòng**.

⇒ Ràng buộc lên token: một dòng đang mang màu **thành công** (`PASS`) **có thể quay về trạng thái chưa duyệt (`OPEN`) mà ⛔ không cần người dùng làm gì với chính dòng đó**.
⇒ ⛔ **Không được coi `--success` là trạng thái cuối** — ⛔ không có token *"đã xong vĩnh viễn"* trong hệ này, và mọi chỗ hiển thị `PASS` phải **đảo được về `OPEN`**.
⚠️ Cách hiển thị chuyển đổi đó (badge, counter, thông báo) thuộc [Components](./Components.md) *(file thuộc lô khác)*.

---

## Tài liệu tham khảo

> ⚠️ **Ghi nhận minh bạch:** tại **2026-08-30**, các tài liệu neo bên dưới (`ADR-013`, `SRS`, `MVP-Scope`) đều ở `status: draft`. Repo ⛔ **chưa có `package.json`** ⇒ mọi tên biến và định dạng giá trị ở đây **chưa verify được bằng code thật**.

**Trong Design System**:

- [Foundations](./Foundations.md) — ⭐ **đọc trước file này**: §Hợp đồng phát biểu token · §Chiến lược light/dark · §Chuẩn accessibility · §Cách kiểm (`K-6`, `K-7`, `K-8`, `K-9`)
- [Brand Guidelines](./Brand-Guidelines.md) — §Hướng màu chủ đạo (`G-1`) · §Điều CẤM tuyệt đối
- [Spacing & Layout](./Spacing-And-Layout.md) — hình học bóng đổ tiêu thụ `--shadow-color` của file này
- [Typography](./Typography.md) *(file thuộc lô khác)* — mọi giá trị về chữ
- [Components](./Components.md) *(file thuộc lô khác)* — icon + nhãn của ba mức alert, ma trận state

**Ngoài Design System**:

- [Design MOC](../Design-MOC.md) — bản đồ tầng 040
- [ADR-013 — Typeset Layer Separate From Art](../../030-Specs/Architecture/ADR-013-Typeset-Layer-Separate-From-Art.md) — §Decision **9** (hai trigger reset gate)
- [SRS — Comic Studio](../../020-Requirements/SRS-Comic-Studio.md) — §5.2 (⛔ không bịa số cho NFR)
- [findings/business-analyst.md](../../010-Planning/pm-runs/2026-08-30-brand-guidelines-va-design-system-comic-studio/findings/business-analyst.md) — ⭐ §2.1 `C-01` (alert ba mức, 13 surface)
- [RULE-001 — Documents Template](../../../knowledge-base/99-Templates/Documents-Template.md) — quy tắc **#5** (⛔ không wiki-link)

**Văn bản chuẩn ngoài repo**:

- **WCAG 2.2** (`w3.org`) — SC **1.4.3** (4.5:1 · 3:1) · SC **1.4.11** (3:1 cho thành phần UI) · SC **1.4.1** (⛔ màu ⛔ không được là tín hiệu duy nhất) · SC **2.4.7** (focus nhìn thấy được). ⚠️ Bảng ngưỡng trong repo là **bảng tra nhanh**, ⛔ không thay văn bản chuẩn.
