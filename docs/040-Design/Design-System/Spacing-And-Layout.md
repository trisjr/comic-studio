---
id: DS-004
type: design-system
status: draft
project: comic-studio
owner: "@trisjr"
tags: [design-system, phase-3]
created: 2026-08-30
updated: 2026-08-30
---

# Spacing & Layout

> **Part of:** [Design MOC](../Design-MOC.md)
> **Tuân theo:** [Foundations](./Foundations.md) §Hợp đồng phát biểu token (`HĐ-1`, `HĐ-2`, `HĐ-3`) + luật `L2`, `L4`
> **Ranh giới cứng:** [ADR-013 — Typeset Layer Separate From Art](../../030-Specs/Architecture/ADR-013-Typeset-Layer-Separate-From-Art.md) §Decision **2** — hình học nội dung là **toạ độ chuẩn hoá 0–1**, ⛔ không phải px của hệ này
> **Nguồn quyết định:** `G-2` (light default, khai đủ cặp) · `G-3` (WCAG 2.2 AA, luồng chính, **desktop-first**) — chốt tại gate run `2026-08-30-brand-guidelines-va-design-system-comic-studio`.

> [!IMPORTANT]
> ⭐ **Bảng tra cho AI assist sinh code** (`E2`), ⛔ không phải bài viết về layout.
> ⭐⭐ **Đọc [mục ranh giới](#-ranh-giới-hệ-này-không-quản-hình-học-panelbubble) TRƯỚC khi dùng bất kỳ token nào ở đây.** Đó là chỗ **dễ lẫn nhất của cả hệ**: một dev đọc lướt sẽ tưởng thang spacing áp được cho hình học panel/bubble. ⛔ **Không.**
> ⛔ File này ⛔ **không định nghĩa bất cứ thứ gì về chữ** (cỡ, line-height, họ font) — xem [Typography](./Typography.md) *(file thuộc lô khác)*.

## Mục lục

- [Thang spacing](#thang-spacing)
- [Radius / border / elevation](#radius--border--elevation)
- [Breakpoint](#breakpoint)
- [Z-index](#z-index)
- [⛔ Ranh giới: hệ này KHÔNG quản hình học panel/bubble](#-ranh-giới-hệ-này-không-quản-hình-học-panelbubble)
- [Tài liệu tham khảo](#tài-liệu-tham-khảo)

---

## Thang spacing

> [!NOTE]
> ⭐ **Nhãn: MỌI con số trong mục này là *quyết định Phase 3*.** Repo ⛔ không có tầng token nào trước đó, và ⛔ **không có một requirement nào** về spacing/layout ở tầng `docs/020-Requirements/`.
> Ngoại lệ nhãn **duy nhất**: ngưỡng **≥ 24 × 24 CSS px** là **hằng số quy phạm trích từ văn bản chuẩn WCAG 2.2** (SC 2.5.8) — ⛔ không phải số tự đặt.

**Cơ số: `4px`.** Vì sao 4 chứ ⛔ không phải 8: sản phẩm này là **editor dày đặc control** (danh sách dòng thoại, form spec panel, bảng có hàng chọn được) ⇒ cơ số 8 ép mọi khoảng cách nhỏ phải nhảy bậc và làm form phình. Cơ số 4 vẫn giữ được nhịp, ⛔ không mất kỷ luật.

| Token | Giá trị | Dùng cho |
|---|---|---|
| `--space-0` | `0` | Reset |
| `--space-1` | `4px` | Khoảng cách icon ↔ nhãn trong cùng một control |
| `--space-2` | `8px` | Padding trong của control nhỏ; gap giữa các item cùng nhóm |
| `--space-3` | `12px` | Padding ngang của input & button |
| `--space-4` | `16px` | ⭐ **Bậc mặc định**: padding của card, gap giữa hai nhóm field |
| `--space-5` | `20px` | Gap giữa các block trong một panel |
| `--space-6` | `24px` | Padding của vùng nội dung chính; gap giữa hai section |
| `--space-8` | `32px` | Khoảng cách giữa hai khối lớn |
| `--space-10` | `40px` | Padding dọc của vùng rỗng (empty state) |
| `--space-12` | `48px` | Tách vùng cấp trang |
| `--space-16` | `64px` | Đệm dọc lớn nhất được dùng |

> ⭐ **`L4` — luật cứng:** **mọi** khoảng cách **phải rơi vào thang**. ⛔ **CẤM `p-[13px]`** và mọi arbitrary value cho spacing. Một giá trị lệch thang là **token chết ngay tại chỗ dùng** ([Foundations](./Foundations.md) §Bốn luật hình dạng).
> ⚠️ Cơ số `4px` **trùng khuôn thang mặc định của Tailwind** (`1` = `0.25rem`) ⇒ ⛔ **không cần override `theme.spacing`**, chỉ cần **giới hạn tập bậc được dùng**. ⚠️ **Verify khi init** — đây là quy ước của thư viện, và repo ⛔ chưa có `package.json` để kiểm.

### Kích thước đích bấm — hệ quả của `G-3`

| Hạng mục | Giá trị | Nhãn nguồn |
|---|---|---|
| Ngưỡng tối thiểu của đích bấm | **≥ 24 × 24 CSS px** | ⭐ **Hằng số của chuẩn WCAG 2.2**, SC **2.5.8** (có ngoại lệ trong văn bản chuẩn) |
| Chiều cao control chuẩn của hệ này | **32px** | **Quyết định Phase 3** — chọn cao hơn ngưỡng để còn chỗ cho viền + vòng focus mà ⛔ không phải tính lại |
| Chiều cao control **đặc** (hàng trong bảng dày) | **28px** | **Quyết định Phase 3** — ⚠️ vẫn ≥ ngưỡng, nhưng **phải đệm vùng bấm** ra `32px` bằng padding trong suốt |

⚠️ **Chỉ vì desktop-first (`G-3`) ⛔ không có nghĩa được bỏ ngưỡng đích bấm** — SC 2.5.8 áp cho **con trỏ chuột**, ⛔ không chỉ cho cảm ứng.

---

## Radius / border / elevation

> ⭐ **Nhãn: mọi con số trong mục này là *quyết định Phase 3*.**

### Radius

| Token | Giá trị | Dùng cho |
|---|---|---|
| `--radius-sm` | `4px` | Badge, checkbox, chip trạng thái |
| `--radius-md` | `6px` | ⭐ **Bậc mặc định**: button, input, select |
| `--radius-lg` | `8px` | Card, popover, panel công cụ |
| `--radius-xl` | `12px` | Dialog, sheet |
| `--radius-full` | `9999px` | Avatar, indicator tròn |

> ⚠️ Bộ quy ước shadcn thường phát biểu radius bằng **một** biến gốc `--radius` rồi suy ra các bậc bằng phép trừ. ⭐ **Cột chuẩn ở đây là cột VAI TRÒ + giá trị**; cách phát biểu (một biến gốc hay năm biến) **verify khi init** — xem [Color Tokens](./Color-Tokens.md) §Bộ biến quy ước shadcn để hiểu vì sao ⛔ không chốt tên sẵn.

### Border

| Token | Giá trị | Ghi chú |
|---|---|---|
| `--border-width` | `1px` | Viền chung. **Màu** lấy từ `--border` / `--input` ở [Color Tokens](./Color-Tokens.md) |
| `--ring-width` | `2px` | Bề dày vòng focus — **quyết định Phase 3**; đủ dày để nhìn thấy ở mật độ dày của editor |
| `--ring-offset` | `2px` | Khoảng hở giữa vòng focus và control, để vòng focus ⛔ không chìm vào viền |

> ⭐ **Focus nhìn thấy được là BẮT BUỘC** (SC **2.4.7**, `G-3` — quyết định Phase 3). ⛔ **CẤM `outline: none`** mà ⛔ không thay bằng vòng focus khác. Tương phản của vòng focus đã audit ở [Color Tokens](./Color-Tokens.md) §Bảng audit contrast (hàng 22, 23).

### Elevation — thang ĐẶT TÊN, ⛔ không phải bóng tuỳ ý

`L4`: elevation dùng **thang cố định**. ⛔ Không có shadow nào nằm ngoài bốn bậc dưới.

| Token | Bậc | Dùng cho | Giá trị (light) |
|---|:--:|---|---|
| `--elevation-0` | 0 | Bề mặt phẳng, dính vào nền | `none` |
| `--elevation-1` | 1 | Card, panel công cụ | `0 1px 2px rgb(var(--shadow-color) / 0.06), 0 1px 3px rgb(var(--shadow-color) / 0.10)` |
| `--elevation-2` | 2 | Dropdown, popover, tooltip | `0 4px 6px rgb(var(--shadow-color) / 0.05), 0 10px 15px rgb(var(--shadow-color) / 0.10)` |
| `--elevation-3` | 3 | Dialog, sheet | `0 10px 20px rgb(var(--shadow-color) / 0.08), 0 20px 40px rgb(var(--shadow-color) / 0.14)` |

> ⭐ **Ranh giới file:** hình học bóng (offset · blur · thang bậc) ở **file này**; **màu gốc** `--shadow-color` khai ở [Color Tokens](./Color-Tokens.md) — nguồn duy nhất của mọi giá trị màu (`HĐ-1`). ⛔ Không hardcode màu bóng ở đây.

### ⭐ Elevation ở dark hoạt động KHÁC — nêu trước, ⛔ đừng phát hiện muộn

> **`G-2`:** light là default, dark **khai sẵn nhưng ⛔ chưa implement**. Thang elevation vẫn phải khai **đủ cặp** (`L2`).

| # | Điều |
|:--:|---|
| **1** | ⭐ **Bóng đổ gần như vô hình trên nền tối.** Trên nền sáng, bóng hoạt động vì nó **tối hơn nền**. Trên nền tối, một vệt tối trên nền tối ⇒ ⛔ **không còn tín hiệu độ sâu nào** |
| **2** | ⇒ **Ở dark, độ sâu được truyền bằng ĐỘ SÁNG BỀ MẶT, ⛔ không bằng bóng**: bậc càng cao thì bề mặt càng **sáng hơn** nền. Cặp token đã khai sẵn cho đúng việc này ở [Color Tokens](./Color-Tokens.md) §Giá trị dark — `--background` là bậc tối nhất, `--card`/`--popover` sáng hơn một bậc |
| **3** | ⇒ Ở dark, bóng **⛔ không bị bỏ**, nhưng đổi vai: nó chỉ còn là **viền mềm** để tách khối khỏi nền ⇒ tăng độ đục và đổi `--shadow-color` sang đen thuần (đã khai ở [Color Tokens](./Color-Tokens.md)) |
| **4** | ⇒ Ở dark, mỗi bậc elevation **phải đi kèm một viền `1px`** (`--border`) — ⛔ không dựa vào bóng một mình |

```css
/* Khai sẵn — chưa implement ở MVP (G-2) */
.dark {
  --elevation-1: 0 1px 2px rgb(var(--shadow-color) / 0.40), 0 1px 3px rgb(var(--shadow-color) / 0.50);
  --elevation-2: 0 4px 6px rgb(var(--shadow-color) / 0.45), 0 10px 15px rgb(var(--shadow-color) / 0.55);
  --elevation-3: 0 10px 20px rgb(var(--shadow-color) / 0.50), 0 20px 40px rgb(var(--shadow-color) / 0.65);
}
```

---

## Breakpoint

> [!CAUTION]
> ⭐⭐ **Toàn bộ mục này là *quyết định Phase 3*. ⛔ TUYỆT ĐỐI không viết như thể tầng 020 đã yêu cầu.**
> ⚠️ **Đã grep toàn `docs/020-Requirements/` cho `responsive` · `breakpoint` · `mobile` · `tablet` · `màn hình nhỏ` tại 2026-08-30 ⇒ `No matches found`, 0 hit.** ⛔ **Repo ⛔ KHÔNG có một requirement responsive nào.** Cùng kết luận với [Foundations](./Foundations.md) §Chuẩn accessibility.
> ⇒ Mọi con số dưới đây là **lựa chọn kỹ thuật của Phase 3**, ⛔ **không có deadline**, ⛔ **không phải nghĩa vụ**.

**`G-3`: desktop-first.** Vì sao — ⛔ không phải khẩu vị:

| # | Lý do |
|:--:|---|
| **1** | ⭐ Luồng chính là **editor dày đặc control**: form spec panel, danh sách dòng thoại, bảng có hàng chọn được, preview cạnh vùng làm việc. Đây là công việc **ngồi bàn**, ⛔ không phải công việc một tay |
| **2** | ⭐ `SRS-FR-16` (**CHỐT**) chốt *"heuristic **+** cho user **kéo tay**"* ⇒ có **thao tác kéo** trong luồng chính ⇒ màn hình nhỏ là môi trường **tệ nhất có thể** cho nó. ⚠️ Đường thay thế **không-kéo** là **bắt buộc** (SC **2.5.7**, `G-3`) và được đặc tả ở [Components](./Components.md) *(file thuộc lô khác)* — ⛔ file này ⛔ không thiết kế control |

| Token | Giá trị | Ý nghĩa trong hệ này |
|---|---|---|
| `--bp-sm` | `640px` | Ngưỡng nhỏ nhất được **hiển thị**, ⛔ **không cam kết luồng editor dùng được** |
| `--bp-md` | `768px` | Luồng **đọc-thôi** (xem preview, xem danh sách) phải dùng được từ bậc này |
| `--bp-lg` | `1024px` | ⭐ **Sàn CAM KẾT của luồng chính.** Dưới bậc này, luồng editor ⛔ không được cam kết |
| `--bp-xl` | `1280px` | ⭐ **Bậc thiết kế mặc định** — mọi wireframe vẽ ở đây trước |
| `--bp-2xl` | `1536px` | Bậc rộng: cho phép panel phụ mở đồng thời |

> ⚠️ Bộ giá trị này **trùng khuôn thang mặc định của Tailwind** ⇒ ⛔ không cần override; **verify khi init**. Thứ **là** quyết định Phase 3 chính là **chọn `--bp-lg` làm sàn cam kết** và **`--bp-xl` làm bậc thiết kế**.

### Khung layout của app shell

> ⭐ Đây là **chrome của editor** — thứ Design System **có** quyền quản ([Foundations](./Foundations.md) §Hệ thống này quản cái gì, hàng ⛔ không quản **#1** và **#7**). Mọi số: **quyết định Phase 3**.

| Token | Giá trị | Vai trò |
|---|---|---|
| `--layout-sidebar` | `280px` | Bề rộng cột điều hướng |
| `--layout-toolbar` | `48px` | Chiều cao thanh công cụ trên cùng |
| `--layout-gutter` | `24px` | Máng ngoài của vùng nội dung ở `--bp-xl` trở lên |
| `--layout-gutter-tight` | `16px` | Máng ngoài dưới `--bp-lg` |
| `--layout-content-max` | `1440px` | Bề rộng tối đa của vùng nội dung dạng văn bản/form |

> ⛔ `--layout-content-max` **⛔ KHÔNG áp cho vùng `--canvas`** (khung preview trang). Khung preview co giãn theo không gian còn lại; **nội dung bên trong nó ⛔ không thuộc hệ này** — xem [mục ranh giới](#-ranh-giới-hệ-này-không-quản-hình-học-panelbubble).

---

## Z-index

> ⭐ **Thang ĐẶT TÊN, ⛔ không phải số rời rạc rải rác trong code.** Mọi số: **quyết định Phase 3**.
> ⛔ **CẤM `z-[9999]`** và mọi arbitrary z-index. Một số rời rạc là một cuộc chạy đua vũ trang: người sau luôn cần **lớn hơn một chút**.

| Token | Giá trị | Lớp |
|---|:--:|---|
| `--z-base` | `0` | Nội dung thường |
| `--z-raised` | `100` | Phần tử nổi trong luồng (hàng đang hover, panel đang kéo) |
| `--z-sticky` | `200` | Header, toolbar, hàng tiêu đề bảng dính |
| `--z-dropdown` | `300` | Menu, select, combobox |
| `--z-overlay` | `400` | Scrim của modal (`--overlay` ở [Color Tokens](./Color-Tokens.md)) |
| `--z-modal` | `500` | Dialog, sheet |
| `--z-popover` | `600` | Popover mở **từ trong** dialog |
| `--z-toast` | `700` | Thông báo nổi |
| `--z-tooltip` | `800` | Tooltip — luôn trên cùng vì nó chỉ **mô tả** thứ khác |

**Ba luật đi kèm:**

| Mã | Luật |
|:--:|---|
| **Z-1** | ⭐ **Bước nhảy `100`** — cố ý thưa để còn chỗ chèn một lớp mới vào giữa mà ⛔ không phải đánh số lại toàn hệ |
| **Z-2** | ⭐ `--z-popover` **cao hơn** `--z-modal` — vì popover **mở từ bên trong** dialog là tình huống có thật (chọn entity trong form xác nhận). Xếp ngược ⇒ menu bị dialog che, và người ta sẽ vá bằng một số rời rạc |
| **Z-3** | ⚠️ Radix/shadcn render overlay bằng **portal ở gốc document** ⇒ thứ tự **DOM** cũng tham gia quyết định lớp phủ, ⛔ không chỉ `z-index`. **Verify khi init**: nếu bản init thật đã có thang riêng thì **ánh xạ vào thang này**, ⛔ không dựng thang thứ hai |

---

## ⛔ Ranh giới: hệ này KHÔNG quản hình học panel/bubble

> [!CAUTION]
> ⭐⭐ **ĐÂY LÀ CHỖ DỄ LẪN NHẤT CỦA CẢ HỆ.**
> Một dev đọc lướt file này sẽ tưởng thang spacing áp được cho **vị trí và kích thước của panel và bubble trong trang truyện**. ⛔ **KHÔNG.** Hai thứ đó nằm ở **hai hệ toạ độ khác nhau, do hai tài liệu khác nhau sở hữu.**

### Hai hệ — ⛔ không được trộn

| | **Hệ A — chrome của editor** | **Hệ B — hình học nội dung** |
|---|---|---|
| **Là gì** | Toolbar, sidebar, card, form, dialog, khung bao quanh preview | ⭐ Vị trí / kích thước / tỉ lệ của **panel**, **bubble**, **`text_safe_zone`** trong trang truyện |
| **Đơn vị** | `px` / `rem`, rơi vào [thang spacing](#thang-spacing) | ⭐ **Toạ độ chuẩn hoá `0–1`** trong `page_layout JSONB` |
| **Ai sở hữu** | **File này** | ⭐ [ADR-013](../../030-Specs/Architecture/ADR-013-Typeset-Layer-Separate-From-Art.md) §Decision **2** |
| **Neo khác** | `G-3` (desktop-first) | [MVP-Scope](../../010-Planning/MVP-Scope.md) §4.1 · [SRS](../../020-Requirements/SRS-Comic-Studio.md) §3.D ràng buộc **2** (mức độ rắn: **CHỐT**) |
| **Ai render** | Browser, đọc CSS token | ⭐ **Compositor server-side** — ⛔ **không đọc CSS token của frontend** |

⭐ **Ranh giới phát biểu bằng một câu:** Design System sở hữu **khung bao quanh** preview (toolbar, zoom, trạng thái loading); ⛔ **không** sở hữu **nội dung bên trong** nó ([Foundations](./Foundations.md) §Hệ thống này quản cái gì, hàng ⛔ không quản **#1** và **#7**).

### ⭐ Bốn lý do hai hệ ⛔ KHÔNG được trộn — mỗi lý do đủ để chốt

| # | Lý do | Neo |
|:--:|---|---|
| **1** | ⭐⭐ **Cùng một dữ liệu phải render ở nhiều độ phân giải.** `0–1` là **tỉ lệ**, ⛔ không gắn với một kích thước render nào ⇒ cùng dữ liệu ra được **thumbnail** và **bản in 300 DPI**. `px` **gắn chết** vào một kích thước ⇒ đặt bubble bằng px là **hỏng ngay khi đổi độ phân giải** | [ADR-013](../../030-Specs/Architecture/ADR-013-Typeset-Layer-Separate-From-Art.md) §Decision **2** (dẫn `SRS-FR-11`) |
| **2** | ⭐ **Đường nâng cấp không mất mát.** Layout giữ ở `0–1` **ngay từ MVP** để khi (nếu) lên canvas thật thì *"**không phải migrate dữ liệu**, chỉ thay lớp tương tác"*. Trộn px vào ⇒ **tự tạo ra một migration** cho đúng thứ đã cố ý tránh | [MVP-Scope](../../010-Planning/MVP-Scope.md) §4.1 |
| **3** | ⭐ **Compositor ⛔ không đọc được CSS.** Preview và export **dùng CHUNG một compositor server-side** ([ADR-013](../../030-Specs/Architecture/ADR-013-Typeset-Layer-Separate-From-Art.md) §Decision **8**: ⛔ *"KHÔNG viết renderer/compositor thứ hai"*). Một giá trị spacing khai trong `index.css` **⛔ không tồn tại** ở phía compositor ⇒ đặt hình học nội dung bằng token frontend là đặt nó ở **chỗ máy render ⛔ không nhìn thấy** | [ADR-013](../../030-Specs/Architecture/ADR-013-Typeset-Layer-Separate-From-Art.md) §Decision **8** |
| **4** | ⭐⭐ **Trộn hệ sẽ bắn sai reset gate.** `text_budget` **phụ thuộc diện tích panel**, và **diện tích panel đổi** là trigger `T1` ⇒ **reset gate #2 về `OPEN`** cho **mọi dòng thuộc panel bị ảnh hưởng**. ⚠️ **Hệ quả suy ra:** nếu diện tích panel được đo bằng px của viewport thì **mỗi lần người dùng zoom hoặc đổi kích thước cửa sổ, diện tích "đổi"** ⇒ `T1` bắn ⇒ **xoá công người dùng đã duyệt**. Đo trong hệ `0–1` thì zoom **⛔ không đổi gì cả** | [ADR-013](../../030-Specs/Architecture/ADR-013-Typeset-Layer-Separate-From-Art.md) §Decision **9** |

### Ba lệnh cấm cụ thể — kiểm được

| # | ⛔ Cấm | Trông như thế nào khi bị vi phạm |
|:--:|---|---|
| **1** | ⛔ Dùng `--space-*` hoặc bất kỳ giá trị `px` nào để đặt **vị trí / kích thước / khoảng cách của panel hoặc bubble** | Một dòng kiểu *"bubble cách mép panel `8px`"* trong bất kỳ file nào của tầng 040 |
| **2** | ⛔ Dùng `--radius-*` cho **bo góc của panel hoặc của bubble** trong trang truyện | Bubble bo `--radius-lg`. Hình dạng bubble là **dữ liệu**, do compositor vẽ |
| **3** | ⛔ Để **mức zoom của preview** ảnh hưởng tới hình học nội dung | Toạ độ bubble đổi khi người dùng zoom. Zoom là **chuyện của hệ A**; toạ độ `0–1` **⛔ không đổi theo zoom** |

> ⭐ Đây chính là điều `K-13` của [Foundations](./Foundations.md) §Cách kiểm nghiệm thu trên file này: ***"⛔ 0 mục đặt kích thước/vị trí panel hoặc bubble bằng px"***.

### Vậy file này quản gì quanh vùng preview?

| ✅ Quản | ⛔ Không quản |
|---|---|
| Khung bao, viền, elevation của **khối** preview | Hình học panel/bubble bên trong |
| Máng, gap giữa preview và panel công cụ | Kích thước trang truyện |
| Chiều cao toolbar chứa nút zoom | Mức zoom **áp vào nội dung** — đó là biến đổi hiển thị của ảnh, ⛔ không phải token layout |
| Nền của vùng preview — token `--canvas` ở [Color Tokens](./Color-Tokens.md) | Màu bên trong ảnh preview |

---

## Tài liệu tham khảo

> ⚠️ **Ghi nhận minh bạch:** tại **2026-08-30**, `ADR-013`, `SRS`, `MVP-Scope` đều ở `status: draft`. Repo ⛔ **chưa có `package.json`** ⇒ mọi giá trị trùng khuôn thư viện (thang spacing, breakpoint, cách phát biểu radius) **chưa verify được bằng code thật**.

**Trong Design System**:

- [Foundations](./Foundations.md) — ⭐ **đọc trước file này**: §Hợp đồng phát biểu token · §Bốn luật hình dạng (`L2`, `L4`) · §Cách kiểm (`K-4`, `K-13`)
- [Color Tokens](./Color-Tokens.md) — `--shadow-color`, `--border`, `--input`, `--ring`, `--overlay`, `--canvas`; §Bảng audit contrast (vòng focus, viền input)
- [Brand Guidelines](./Brand-Guidelines.md) — §Hướng màu chủ đạo
- [Typography](./Typography.md) *(file thuộc lô khác)* — mọi giá trị về chữ; ⛔ file này ⛔ không đặt cỡ chữ
- [Components](./Components.md) *(file thuộc lô khác)* — đường thay thế **không-kéo** (SC 2.5.7), ma trận state

**Ngoài Design System**:

- [Design MOC](../Design-MOC.md) — bản đồ tầng 040
- [ADR-013 — Typeset Layer Separate From Art](../../030-Specs/Architecture/ADR-013-Typeset-Layer-Separate-From-Art.md) — ⭐ §Decision **2** (toạ độ `0–1`) · **8** (một compositor) · **9** (hai trigger reset gate)
- [MVP Scope](../../010-Planning/MVP-Scope.md) — §4.1 (giữ layout ở `0–1`, ⛔ không phải migrate)
- [SRS — Comic Studio](../../020-Requirements/SRS-Comic-Studio.md) — §3.D ràng buộc **2** (`page_layout JSONB`, mức độ rắn **CHỐT**) · `SRS-FR-16` · §5.2 (⛔ không bịa số cho NFR)
- [RULE-001 — Documents Template](../../../knowledge-base/99-Templates/Documents-Template.md) — quy tắc **#5** (⛔ không wiki-link)

**Văn bản chuẩn ngoài repo**:

- **WCAG 2.2** (`w3.org`) — SC **2.5.8** (đích bấm ≥ 24 × 24 CSS px) · SC **2.4.7** (focus nhìn thấy được) · SC **2.5.7** (thao tác kéo có đường thay thế). ⚠️ Bảng ngưỡng trong repo là **bảng tra nhanh**, ⛔ không thay văn bản chuẩn.
