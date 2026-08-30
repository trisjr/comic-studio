# Findings — architect

> Lens **READ-ONLY** của Bước 2 fan-out, run `2026-08-30-brand-guidelines-va-design-system-comic-studio`.
> Tài liệu này **phát biểu ràng buộc đang có**, ⛔ không thiết kế Design System, ⛔ không đề xuất đổi kiến trúc. Không file nào ngoài file này bị chạm.
>
> **Nguồn đã đọc trực tiếp**: [ADR-001](../../../../030-Specs/Architecture/ADR-001-Backend-And-Frontend-Tech-Stack.md) (toàn văn) · [ADR-013](../../../../030-Specs/Architecture/ADR-013-Typeset-Layer-Separate-From-Art.md) (`Context` + `Decision`) · [SDD](../../../../030-Specs/Architecture/SDD-Comic-Studio.md) §6.3, §6.4 · [SRS](../../../../020-Requirements/SRS-Comic-Studio.md) §3 (các hàng FR/NFR được trích), §4, §5.1, §5.2, §5.3 · [Spec-Security-Legal-Compliance](../../../../030-Specs/Security/Spec-Security-Legal-Compliance.md) §5, §6, `L-6` · [Spec-Security-Threat-Model](../../../../030-Specs/Security/Spec-Security-Threat-Model.md) (grep `SDD-HG-01`, `SRS-NFR-15`, `L-6`) · [DB-Entity-Job-Queue](../../../../030-Specs/Schema/DB-Entity-Job-Queue.md) · [DB-Entity-Typeset-Layer](../../../../030-Specs/Schema/DB-Entity-Typeset-Layer.md) · [DB-Entity-Dialogue-And-Gate](../../../../030-Specs/Schema/DB-Entity-Dialogue-And-Gate.md) · [DB-Entity-Generation](../../../../030-Specs/Schema/DB-Entity-Generation.md) · [Endpoint-Human-Gates](../../../../030-Specs/API/Endpoint-Human-Gates.md) · [Endpoint-Preview-Export](../../../../030-Specs/API/Endpoint-Preview-Export.md) · [Story-AI-Disclosure-Article-11](../../../../022-User-Stories/Backlog/Story-AI-Disclosure-Article-11.md) · [000-Index](../../../../000-Index.md) §Nợ kỹ thuật · [Charter](../../../Charter-Comic-Studio.md) §7 `C5` · [OKRs](../../../OKRs.md) §6 `AG-2`.
>
> **Đã verify bản ADR-001**: `grep -c shadcn` = **2** ⇒ đúng bản có `shadcn/ui + Tailwind CSS`.

---

## Kết luận của worker

### 0. Cách đọc tài liệu này

Mỗi ràng buộc mang **một mã `ARC-xx`** và đủ **4 thành phần**: *phát biểu · nguồn · vi phạm trông như thế nào · phát hiện bằng cách nào*. Mã `ARC-xx` chỉ có nghĩa **trong run này** — nó ⛔ không phải một mã requirement mới của repo, và writer ở Bước 5 ⛔ không được trích `ARC-xx` như một nguồn; phải trích **cột Nguồn**.

**Ba nhãn độ rắn**, lấy đúng theo cách ADR-001 và SRS tự dán nhãn:

| Nhãn | Nghĩa | Design System được làm gì |
|---|---|---|
| **CHỐT** | ⛔ Không có đường lui. Đổi = viết ADR mới thay thế | Neo vào thoải mái, ⛔ không cần dự phòng |
| **MẶC ĐỊNH** | Đã chọn, **đường lui ghi rõ** ở `## Consequences` | Neo vào **nhưng phải dán nhãn**; tách tầng để đảo được mà không viết lại toàn bộ |
| **`TBD`** | ⛔ Chưa có căn cứ | ⛔ **Không tự điền**. Ghi `TBD` + owner + thời điểm đóng |

> [!CAUTION]
> ⛔ **Quy tắc số một cho writer Bước 5**: một con số hay một tên riêng **không truy được về nguồn trong repo** thì để `TBD`. Bịa nó ở tầng 040 tạo một nguồn sự thật giả mà tầng 020/030 không có — và Bước 6 sẽ không bắt được nếu chính tài liệu Design System trông tự tin.

---

### 1. Vùng A — Tech stack UI đã chốt

#### 1.1 ⭐ Đâu là CHỐT, đâu là MẶC ĐỊNH — đọc trước khi neo bất cứ gì

[ADR-001](../../../../030-Specs/Architecture/ADR-001-Backend-And-Frontend-Tech-Stack.md) chia `## Decision` thành **hai tầng có tên khác nhau**, và `## Consequences` đóng lại bằng một câu dứt khoát:

> *"⛔ Ba dòng **CHỐT** (một ngôn ngữ TypeScript · SQL thô là nguồn sự thật schema · API là hợp đồng duy nhất) **không có đường lui** — đổi chúng là viết ADR mới thay thế ADR này."*

| Thứ chạm Design System | Ở đâu trong ADR-001 | Độ rắn | Hệ quả |
|---|---|:--:|---|
| **SPA thuần, ⛔ không SSR, ⛔ không server action; API là hợp đồng duy nhất** | `## Decision` Tầng CHỐT **điều 5** | **CHỐT** | Mọi cơ chế theme/token phải chạy **hoàn toàn client-side** |
| **`packages/contracts` (zod) là nguồn sự thật hợp đồng; ⛔ không khai kiểu hai lần** | `## Decision` Tầng CHỐT **điều 6** | **CHỐT** | Form spec ⛔ không được định nghĩa lại luật validate |
| **Wrap tiếng Việt cùng runtime với compositor** | `## Decision` Tầng CHỐT **điều 8** | **CHỐT** | Xem toàn bộ [mục 2](#2-vùng-b--điều-8-hai-hệ-font-là-ràng-buộc-cứng-nhất-của-run-này) |
| **TypeScript một ngôn ngữ duy nhất** | `## Decision` Tầng CHỐT **điều 1** | **CHỐT** | Token phải tiêu thụ được bằng TS/CSS, ⛔ không phải bằng một DSL cần build chain lạ |
| **Vite + React + TypeScript · TanStack Query · shadcn/ui (Radix) + Tailwind CSS** | `## Decision` **Tầng MẶC ĐỊNH**, hàng *Frontend & UI* | ⚠️ **MẶC ĐỊNH** | Có đường lui — `## Consequences` §*Đường lui đã ghi rõ*: *"Vite/React không đủ cho editor ⇒ chỉ đổi **frontend**; API và hợp đồng không đổi — chi phí **Thấp**"* |
| **pnpm workspace `apps/web` là bundle tĩnh** | `## Decision` Tầng MẶC ĐỊNH, hàng *Repo* | MẶC ĐỊNH | Không có build step server-side cho HTML |

> [!IMPORTANT]
> ⭐ **Đây là chỗ Design System dễ xây sai nền nhất.** Toàn bộ tầng token nếu viết thẳng bằng cú pháp `shadcn/ui` + Tailwind thì nó đang đứng trên một dòng **MẶC ĐỊNH có chi phí đảo ngược THẤP** — ADR-001 tự nói việc đổi frontend là rẻ. ⇒ Design System phải **tách hai tầng**: (a) tầng token **trung lập** (tên semantic + giá trị), (b) tầng **ánh xạ** vào Tailwind theme / shadcn component. Đảo (b) không được kéo theo viết lại (a).

#### 1.2 Bảng ràng buộc vùng A

| ID | Phát biểu ràng buộc | Nguồn | Vi phạm trông như thế nào | Phát hiện bằng cách nào |
|---|---|---|---|---|
| **`ARC-01`** | Design System **PHẢI** phát biểu token ở dạng **tiêu thụ được trực tiếp** bởi Tailwind theme + component `shadcn/ui` đặt trong repo | `ADR-001` `## Decision` Tầng MẶC ĐỊNH hàng *Frontend & UI*; `## Consequences` §Tích cực (dòng `shadcn/ui + Tailwind CSS` tích hợp Zod contracts qua React Hook Form) — **MẶC ĐỊNH** | Token khai bằng một hệ không dùng được: file Figma-only, Style Dictionary chưa có trong repo, SCSS variable, hoặc theme object của một thư viện khác | Mỗi token phải có **một dòng ví dụ tiêu thụ** trong Tailwind/CSS. Token nào không có ⇒ chưa dùng được |
| **`ARC-02`** | Design System ⛔ **KHÔNG được** đặc tả bất kỳ cơ chế nào cần server render HTML | `ADR-001` `## Decision` **điều 5** (**CHỐT**); `## Alternatives considered` **E** (loại Next.js vì 3 lý do độc lập) | *"critical CSS inline do server render"* · *"đọc theme từ cookie ở server để tránh flash"* · *"dùng `next/font`"* · *"server component cho danh sách chapter"* | `grep -in "SSR\|server component\|server action\|Next.js\|next/"` trong `docs/040-Design/**` ⇒ mọi hit phải giải thích được |
| **`ARC-03`** | Component spec **PHẢI** neo vào **Radix Primitives** semantics; ⛔ không đặc tả thư viện component thứ hai, ⛔ không CSS-in-JS runtime | `ADR-001` Tầng MẶC ĐỊNH hàng *Frontend & UI* (`shadcn/ui` = Radix Primitives) — ⚠️ **MẶC ĐỊNH** | Bảng component liệt kê `MUI Dialog`, `Ant Table`, `Chakra`, `styled-components`, `emotion` | Liệt kê **mọi tên thư viện** xuất hiện trong Design System; tên ngoài `{shadcn/ui, Radix, Tailwind}` ⇒ cờ |
| **`ARC-04`** | Mọi phát biểu ràng buộc kỹ thuật trong Design System **PHẢI mang nhãn** `CHỐT` / `MẶC ĐỊNH` / `TBD` kèm neo | `ADR-001` `## Decision` (hai tầng có tên); `## Consequences` §*Đường lui đã ghi rõ* + câu chốt ba dòng CHỐT | *"shadcn/ui là quyết định bất biến của dự án"* (nâng MẶC ĐỊNH thành CHỐT) · *"SPA-only là lựa chọn hiện tại, sau này thêm SSR cũng được"* (hạ CHỐT thành MẶC ĐỊNH) | Đếm: mọi câu chứa *"phải/không được"* có nhãn độ rắn không |
| **`ARC-05`** | Form/validation spec ⛔ **KHÔNG được** định nghĩa lại kiểu hay luật validate — phải **dẫn xuất** từ zod schema ở `packages/contracts` | `ADR-001` `## Decision` **điều 6** (**CHỐT**, *"⛔ Không khai báo kiểu request/response hai lần"*); `## Consequences` §Tích cực | Bảng *"quy tắc validate cho Input"*: `tên project ≤ 50 ký tự`, `email regex …` viết thẳng trong Design System | Mọi luật nghiệp vụ ở mục Form phải **trỏ** `packages/contracts`; luật nào đứng một mình = nguồn sự thật thứ hai |
| **`ARC-06`** | Component hiển thị **tiền / credit / khoá thứ tự** **PHẢI** nhận **chuỗi decimal**, ⛔ không nhận `number` | `ADR-001` `## Consequences` §Tiêu cực **#3** (`pg` trả `NUMERIC` về **chuỗi**; ⛔ cấm `parseFloat`/`Number()` trên `reading_order`/`story_order` `D-15`, `cost_usd` `D-59`, mọi cột credit `D-60`) | `<CreditBadge value: number />` · *"format tiền: `value.toFixed(2)`"* · *"sort theo `reading_order` bằng `a - b`"* | Đọc mọi prop hiển thị số tiền/credit/thứ tự trong Design System; kiểu `number` ⇒ cờ |
| **`ARC-07`** | Spacing/size token bằng `px`/`rem` **chỉ áp cho UI chrome**; ⛔ **không** áp cho hình học **panel / bubble** — nơi đó là **toạ độ chuẩn hoá 0–1** | `ADR-001` `## Context` (`D-22`, `D-29`); `ADR-013` `## Decision` **điều 2**; `DB-Entity-Typeset-Layer` `T-1` (`CHECK` 0–1 **ở tầng DB**), `T-4` (*"⛔ không cột nào của `comic.bubble` chứa pixel"*) — **CHỐT** | *"bubble padding = 8px"* · *"grid panel 12 cột, gutter 16px"* đặt chung bảng với token UI | Mọi token spacing phải khai **phạm vi áp dụng**; `grep -n "px"` trong mục nói về bubble/panel/layout |

---

### 2. Vùng B — Điều 8: hai hệ font là ràng buộc cứng nhất của run này

#### 2.1 ⭐ Trả lời dứt khoát: PHẢI tách **hai** hệ font, và chúng khác nhau **về bản chất spec**, không chỉ khác giá trị

| | **Hệ 1 — UI font** | **Hệ 2 — Render font (typeset)** |
|---|---|---|
| Ai render | **Trình duyệt**, trong `apps/web` | ⭐ **Compositor server-side** (cùng runtime với wrap) |
| Bản chất | Lựa chọn **thẩm mỹ / brand** | ⭐ **Đầu vào của thuật toán ngắt dòng** — một tham số kỹ thuật |
| Fallback stack | ✅ Được phép (`font-family: A, B, sans-serif`) | ⛔ **KHÔNG** — phải **đơn trị**, vì wrap *đo bằng chính font sẽ render* |
| Sai thì hỏng ở đâu | Xấu ở màn hình, sửa bằng một dòng CSS | ⭐ **Hỏng sản phẩm cuối** — chữ tràn / dấu bị cắt trong ảnh đã sinh, phát hiện **sau khi đã tốn tiền** |
| Hiện đã chốt chưa | Chưa ai quyết — quyết định **mới của Phase 3** | ⛔ **`TBD-FONT`** — owner **Architect + Founder**, đóng **sau MVP0, trước gate `G1-e`** |

**Căn cứ, nguyên văn:**

- [ADR-001](../../../../030-Specs/Architecture/ADR-001-Backend-And-Frontend-Tech-Stack.md) `## Decision` **điều 8** (**CHỐT**): wrap tiếng Việt *"nằm CÙNG runtime với compositor"*; chuẩn hoá **NFC** tại biên ingest; ngắt theo **grapheme cluster + word boundary** bằng `Intl.Segmenter`; ⛔ *"không được wrap ở frontend rồi gửi kết quả xuống"*; ⛔ *"không được wrap bằng font khác font sẽ render"*.
- [ADR-001](../../../../030-Specs/Architecture/ADR-001-Backend-And-Frontend-Tech-Stack.md) `## Consequences` §Tiêu cực **#5** — ⭐ **đây là câu giải thích vì sao phải tách hai hệ font**: *"`Intl.Segmenter` giải quyết **ngắt**, KHÔNG giải quyết **đo**… Wrap đúng = segmentation **+** đo bằng **chính font sẽ render**."* Kèm nghiệm thu bắt buộc ở spike MVP0: corpus **cả NFC và NFD**, dấu chồng (`ế`, `ữ`, `ợ`), render **300 DPI**, ba tiêu chí (a)(b)(c).
- [ADR-013](../../../../030-Specs/Architecture/ADR-013-Typeset-Layer-Separate-From-Art.md) `## Decision` **điều 6** lặp lại đúng ba ràng buộc đó; **điều 8** chốt *compositor DÙNG CHUNG cho preview và export* (`D-32`) ⇒ ⛔ **không có renderer thứ hai** để mà dùng font thứ hai.
- [ADR-013](../../../../030-Specs/Architecture/ADR-013-Typeset-Layer-Separate-From-Art.md) §Lý do **#2**: model render chữ tiếng Việt *"hỏng **âm thầm** trong pixel"* — đây chính là mô tả cách lỗi font sẽ biểu hiện.
- [DB-Entity-Typeset-Layer](../../../../030-Specs/Schema/DB-Entity-Typeset-Layer.md) `T-9` (NFC tại biên ingest, *"wrap phải chạy ở cùng runtime với compositor và đo bằng chính font sẽ render"*) và `TBD-FONT`.

#### 2.2 ⭐ Nếu Typography spec chỉ khai **một** bộ font — hỏng ở đâu trong pipeline

Có hai chiều, và chỉ **một** chiều là thảm hoạ:

1. ⭐ **Chiều nguy hiểm — lấy font UI làm font chung.** Đây là chiều **mặc định của nghề**: designer chọn một web font đẹp, hợp brand, khai vào Typography spec. Compositor server-side khi đó phải đo bề rộng bằng metric của một font mà **runtime server có thể không có** ⇒ nó fallback âm thầm sang font khác. Kết quả: **ngắt dòng tính theo font A, glyph vẽ bằng font B**. Điểm hỏng cụ thể trong pipeline:
   - **Bước composite** (dùng chung cho preview và export — `D-32`, ADR-013 điều 8) là nơi hỏng.
   - Biểu hiện: đúng ba thứ mà nghiệm thu MVP0 của ADR-001 `## Consequences` #5 bắt phải test — **(a)** ký tự bị tách khỏi dấu khi xuống dòng, **(b)** dấu bị **cắt cụt bởi mép bubble**, **(c)** NFD và NFC cho ra ngắt dòng khác nhau.
   - ⭐ **Thời điểm phát hiện là vấn đề lớn hơn bản thân lỗi**: nó chỉ lộ ra **sau khi ảnh đã sinh**, tức sau khi đã gọi image API và đã tốn tiền — và tại đó thì `D-29` cấm nướng chữ vào pixel nên không có đường vá nhanh.
   - Nếu font còn **thiếu glyph tiếng Việt**, `TBD-FONT` ghi rõ: ⛔ *"không có benchmark định lượng nào"*, chỉ phát hiện được bằng **kiểm thủ công từng panel** ⇒ chi phí phát hiện là công người, không phải CI.
2. **Chiều vô hại — lấy font render làm font chung.** UI editor bị buộc dùng một font phục vụ in ấn: xấu, ràng buộc thừa, nhưng ⛔ không phá pipeline. Ghi ra để không ai *"giải quyết"* vấn đề bằng cách gộp về phía này rồi tưởng đã xong.

> [!WARNING]
> ⚠️ **Không có tài liệu nào trong repo đang nói ra điều này.** `TBD-FONT` chỉ khai *"font sẽ render"*; ⛔ không dòng nào nói *"font UI là một thứ khác"*. Nếu Design System không tách, ⛔ **sẽ không có tài liệu nào tách hộ** — và đây là loại lỗi mà cả 19 ADR đều không bắt được, vì nó phát sinh **ở tầng 040**.

#### 2.3 Bảng ràng buộc vùng B

| ID | Phát biểu ràng buộc | Nguồn | Vi phạm trông như thế nào | Phát hiện bằng cách nào |
|---|---|---|---|---|
| **`ARC-08`** | Typography spec **PHẢI tách tối thiểu hai hệ font**, đặt **tên khác nhau**, khai **thang đo riêng**, và nói rõ hệ nào render ở đâu | `ADR-001` `## Decision` **điều 8** + `## Consequences` §Tiêu cực **#5**; `ADR-013` `## Decision` **điều 6**, **điều 8** — **CHỐT** | Mục *Typography* có **đúng một** bảng `Heading / Body / Caption` và một dòng `font-family`, dùng chung cho cả giao diện lẫn bubble | Đếm số hệ font được khai trong Design System. **< 2 ⇒ FAIL**. Và: mỗi hệ có ghi *"render bởi ai"* không |
| **`ARC-09`** | ⛔ **KHÔNG được chốt tên họ font render.** Phải để `TBD` kèm owner + thời điểm | `DB-Entity-Typeset-Layer` `TBD-FONT` (owner **Architect + Founder**; *sau MVP0, trước gate `G1-e`*); `ADR-013` bảng `TBD` hàng *Font sẽ render* | *"Font typeset: Be Vietnam Pro 400"* viết như đã chốt | `grep` mọi tên font trong Design System; tên nào gắn với hệ render mà ⛔ không mang chữ `TBD` ⇒ cờ |
| **`ARC-10`** | Font render **PHẢI** được khai **đơn trị** + kèm yêu cầu **glyph coverage tiếng Việt (dấu chồng)**; ⛔ không khai bằng CSS fallback stack | `ADR-001` điều 8 (*"⛔ không wrap bằng font khác font sẽ render"*) + `## Consequences` #5 (nghiệm thu corpus dấu chồng `ế`, `ữ`, `ợ`); `TBD-FONT` | `font-family: "X", "Y", sans-serif` đặt ở mục font render ⇒ font thực tế **không xác định** | Mục font render có dấu phẩy trong khai báo họ font ⇒ cờ ngay |
| **`ARC-11`** | ⛔ **KHÔNG được** đặc tả thuật toán ngắt dòng / hyphenation / `text-wrap` / `word-break` cho **thoại bubble** ở tầng frontend. Nếu editor hiển thị thoại, phải khai rõ đó là hiển thị **không chuẩn tắc** và ⛔ kết quả ngắt dòng đó **không bao giờ được gửi xuống backend** | `ADR-001` điều 8 (*"⛔ không wrap ở frontend rồi gửi kết quả xuống"*); `ADR-013` điều 6 — **CHỐT** | *"Bubble component dùng `text-wrap: pretty` + `hyphens: auto`"* · *"editor tự tính số dòng để cảnh báo vượt `text_budget`"* rồi POST số dòng đó lên | `grep -in "word-break\|hyphens\|text-wrap\|line-break\|ngắt dòng"`; và kiểm mọi luồng có gửi chuỗi **đã ngắt** lên API không |
| **`ARC-12`** | ⛔ **KHÔNG được** khai một chuẩn hoá Unicode thứ hai ở frontend. Mọi phép **đếm ký tự** trong UI phải đếm theo **grapheme cluster** và phải khai rõ nó ⛔ **không** phải nguồn sự thật của `text_budget` | `ADR-001` điều 8 (**NFC** tại biên ingest, grapheme cluster + `Intl.Segmenter`); `DB-Entity-Typeset-Layer` `T-9`; `text_budget` là field của `comic.panel` (`ADR-012` `Decision` điều 9 — ⚠️ *trích gián tiếp* qua `DB-Entity-Typeset-Layer` §Nguồn và §*Ba field ⛔ KHÔNG ở tầng typeset*) | *"Character counter hiển thị `value.length`"* · *"chuẩn hoá NFD trước khi so sánh"* · counter được trình bày như thứ quyết định gate 2 | Mọi mô tả đếm ký tự trong Design System: có nói *grapheme cluster* không, có nói *không chuẩn tắc* không |
| **`ARC-13`** | ⛔ **KHÔNG được** phát minh **danh mục kiểu bubble** (speech / thought / shout / whisper) hay hình dạng **SFX / narration box / caption** | `DB-Entity-Typeset-Layer` `TBD-BUBBLE-KIND` (⭐ *chặn DDL*, owner **PM hỏi Founder**) và `TBD-SFX-NARRATION`; `ADR-013` bảng `TBD` | Design System vẽ sẵn 4 variant bubble kèm token cho từng loại | Mọi variant bubble phải trỏ `TBD-BUBBLE-KIND`; danh mục cụ thể ⇒ cờ |

---

### 3. Vùng C — Ràng buộc từ tương tác thời gian thực (`D-45`, polling 2 giây)

#### 3.1 Danh mục trạng thái là **ĐÓNG** — Design System phải phủ đúng nó

[DB-Entity-Job-Queue](../../../../030-Specs/Schema/DB-Entity-Job-Queue.md) §*Danh mục `job_status`* (nguồn: `ADR-015` `Q5`, *"⛔ file này không thêm/bớt giá trị"*), cưỡng chế bằng `CHECK (status IN (…))`:

| `job_status` | Ý nghĩa UI tương ứng |
|---|---|
| `queued` | Đã nhận, **chưa chạy** — đang xếp hàng |
| `running` | Đang chạy |
| `succeeded` | Xong |
| `failed_permanent` | ⭐ Hỏng **không retry được** |
| `failed_exhausted` | ⭐ Hỏng **sau khi đã hết lượt retry** |

⭐ **Hai trạng thái thất bại, ⛔ không phải một.** `J-6` cưỡng chế `CHECK (status <> 'failed_permanent' OR last_error_class IS NOT NULL)` và tương tự cho `failed_exhausted` ⇒ *"job thất bại phải để lại trạng thái RÕ RÀNG, ⛔ không bao giờ biến mất"*. Một Design System khai `loading / success / error` là **thiếu một trạng thái và mất luôn lớp lỗi**.

#### 3.2 ⭐ Một Design System không khai trạng thái chờ dài thì thiếu cái gì

Lý do gốc của `D-45`, nguyên văn [ADR-015](../../../../030-Specs/Architecture/ADR-015-Job-Queue-In-Postgres.md): *"generation mất **hàng chục giây**, polling là quá đủ"*. Cộng với `ADR-001` `## Consequences` §Tiêu cực **#1** (compositing 300 DPI là **CPU-bound**, ⛔ cấm chạy trong request handler ⇒ phải qua worker). Bốn thứ **bắt buộc phải có spec**, thiếu cái nào cũng là lỗ:

1. **`queued` ≠ `running`** — người dùng phải phân biệt được *"chưa tới lượt"* và *"đang chạy"*. Gộp làm một là giấu thông tin duy nhất giải thích vì sao phải chờ.
2. **Trạng thái chờ nhiều chục giây** — ⛔ không dùng chung component với thao tác tức thời (spinner trong nút). Phải sống được qua **reload trang** và **rời màn hình rồi quay lại**, vì job nằm ở server chứ không ở tab trình duyệt.
3. **`stale` / refetch nền** — polling 2 giây trên một tầng *"data-fetching có **cache** + polling"* (`ADR-001` `## Context`, dòng `D-45`) nghĩa là mỗi nhịp poll là một lần lấy lại dữ liệu **đã có sẵn trên màn hình**. Nếu Design System không tách *"tải lần đầu"* khỏi *"đang làm mới trên nền"*, UI sẽ **nhấp nháy skeleton mỗi 2 giây**. *(Suy ra trực tiếp từ hai nguồn trên — ⛔ không có tài liệu nào phát biểu sẵn câu này.)*
4. **Hai loại thất bại + lớp lỗi** — xem `ARC-17`.

#### 3.3 Bảng ràng buộc vùng C

| ID | Phát biểu ràng buộc | Nguồn | Vi phạm trông như thế nào | Phát hiện bằng cách nào |
|---|---|---|---|---|
| **`ARC-14`** | Design System **PHẢI** khai bộ trạng thái async phủ **đúng 5 giá trị** của danh mục `job_status` | `DB-Entity-Job-Queue` §*Danh mục `job_status`* (nguồn `ADR-015` `Q5`); `J-6` | Bảng State chỉ có `idle / loading / success / error` | Đếm: **5 giá trị**, và có tách `failed_permanent` / `failed_exhausted` không |
| **`ARC-15`** | ⛔ **KHÔNG được** đặc tả component dựa trên **WebSocket / SSE / long-poll** | `D-45` (`ADR-001` `## Context` + bảng *Đã quyết ở đâu*); `SRS-NFR-06`; `ADR-015` `Q6` **`CT-POLL-2S`**: *"⛔ Không WebSocket, ⛔ không SSE, ⛔ không long-poll"*. ⚠️ Độ rắn **MẶC ĐỊNH** (SRS §3: đường lui = **tiền đề đảo**, tức generation nhanh hơn nhiều; ⛔ *"WebSocket hiện đại hơn"* **không** phải lý do hợp lệ) | *"Realtime toast khi job xong"* · *"live progress bar"* · *"connection status dot"* · *"presence / ai đang xem trang này"* | `grep -in "realtime\|thời gian thực\|websocket\|SSE\|streaming\|live"` |
| **`ARC-16`** | **PHẢI** có spec riêng cho **tiến trình nhiều chục giây**, sống được qua reload và qua việc rời màn hình | `ADR-015` (lý do `D-45`: *"generation mất hàng chục giây"*); `ADR-001` `## Consequences` §Tiêu cực **#1** | Generate panel dùng spinner trong nút; đóng modal là mất dấu job | Có component tiến trình dài không; nó có mô tả hành vi sau reload không |
| **`ARC-17`** | Component lỗi **PHẢI** nhận **một mã lớp lỗi**, ⛔ không phải chuỗi tự do. **Nhưng** ⛔ **không được tự chốt format mã lỗi** | `ADR-015` `Q5` (`job_error_class`, phân loại **do adapter cung cấp** — `ADR-016` `Q1`); `J-6`. ⚠️ Chặn: [000-Index](../../../../000-Index.md) §*Nợ kỹ thuật* **#6** — chuẩn `error_code` + error envelope cho 14 file API là `TBD-API-ENV`, *"casing còn lẫn `UPPER_SNAKE`/`lower_snake`"*, chủ **Architect** | Error component chỉ có prop `message: string` · **hoặc** ngược lại: Design System tự chốt *"mọi mã lỗi là `UPPER_SNAKE`"* | Error component có prop lớp lỗi không; và có dán `TBD` trỏ `TBD-API-ENV` không |
| **`ARC-18`** | ⛔ **KHÔNG được** khai polling interval khác **2 giây** cho tác vụ async | `ADR-015` `Q6` `CT-POLL-2S`; `Endpoint-Preview-Export` `API-PE-6` (nếu chuyển async về sau thì *"client contract khi đó là `CT-POLL-2S`* — ⛔ **không phát minh interval khác**") | *"Poll mỗi 1s cho cảm giác mượt hơn"* | `grep` mọi con số kèm `s`/`giây` ở mục trạng thái async |
| **`ARC-19`** | **Preview và export ⛔ KHÔNG đi qua hàng đợi** ở horizon này ⇒ ⛔ không job id, ⛔ không polling, ⛔ không `202` cho hai luồng đó | `Endpoint-Preview-Export` **`API-PE-6`** (*"Hai endpoint `POST` là **đồng bộ trong request**"*) | Design System khai màn *"Đang tạo preview…"* theo khuôn job queue có job id | Đối chiếu: luồng preview/export trong Design System có mượn ngôn ngữ job/polling không |

---

### 4. Vùng D — Human gate: ràng buộc ⛔ không được làm mềm

#### 4.1 Nguồn duy nhất

[SDD](../../../../030-Specs/Architecture/SDD-Comic-Studio.md) **§6.3 `SDD-HG-01`** — grep xác nhận **là nguồn duy nhất**, được [000-Index](../../../../000-Index.md), [Specs-MOC](../../../../030-Specs/Specs-MOC.md), [Spec-Security-Threat-Model](../../../../030-Specs/Security/Spec-Security-Threat-Model.md) và [DB-Entity-Dialogue-And-Gate](../../../../030-Specs/Schema/DB-Entity-Dialogue-And-Gate.md) **trỏ về, ⛔ không đặc tả lại**. Bảy điều khoản `.1`…`.7` + năm *Hệ quả bắt buộc cho 14 file API*, hiện thực ở `API-HG-1`…`API-HG-13`.

> [!CAUTION]
> ⭐⭐ **Đây là vùng mà một quyết định UI vô hại về thẩm mỹ phá một invariant kiến trúc.** Nguyên văn [UC-07 `EX-6`](../../../../020-Requirements/Use-Cases/UC-07-Edit-Bubble-And-Dialogue-In-Panel.md) trích trong `ADR-013`: *"`M2-4` đo **'không tồn tại đường code nào xuất bản page mà chưa qua cả hai gate'**, chứ **không** đo sự tồn tại của màn hình gate."* ⇒ **màn hình gate vẫn hiển thị đầy đủ mà `M2-4` vẫn FAIL**.

#### 4.2 Component gate ⛔ KHÔNG được thiết kế theo kiểu cho phép bỏ qua

| ID | Phát biểu ràng buộc | Nguồn | Vi phạm trông như thế nào | Phát hiện bằng cách nào |
|---|---|---|---|---|
| **`ARC-20`** | ⛔ **KHÔNG được** đặc tả bất kỳ affordance bỏ qua gate nào: `skip`, *"duyệt tất cả"*, `bulk approve`, auto-advance, *"tự duyệt khi confidence cao"* | `SDD-HG-01.2` (⛔ *không job, không LLM, không worker, không cron, không cờ cấu hình, không biến môi trường, không tham số API*); Hệ quả API **#1**; `API-HG-1`; ⭐ **`API-HG-6`**: *"`#5` là đường **DUY NHẤT** ghi `PASS`. ⛔ Không endpoint thứ hai, ⛔ **không batch**"* | Nút **"Duyệt cả trang"** · checkbox *"áp dụng cho các dòng còn lại"* · toggle *"tự động duyệt khi `speaker_confidence` > 0.9"* · wizard tự nhảy bước khi mọi dòng đã xem | `grep -in "skip\|bỏ qua\|duyệt tất cả\|approve all\|bulk\|hàng loạt\|tự động duyệt"`; và: component gate có mô tả thao tác **theo từng dòng** không |
| **`ARC-21`** | Control quyết định `PASS` ⛔ **KHÔNG được** có giá trị **mặc định đã chọn sẵn** | ⭐ `SDD-HG-01.1`: *"Trạng thái mặc định của mỗi gate là `OPEN`. ⛔ **Không tồn tại trạng thái mặc định 'đã xác nhận'**"*; `DB-Entity-Dialogue-And-Gate` §2 (`PASS` đòi `INSERT` mang `passed_by_user_id NOT NULL`) | Radio *"Người nói"* pre-select ứng viên confidence cao nhất **và** nút PASS đọc thẳng giá trị đó · checkbox xác nhận `defaultChecked` | Mọi control trong khối gate phải khai **`default: none`**; hit nào có `defaultValue`/`defaultChecked` ⇒ đọc lại |
| **`ARC-22`** | **PHẢI** có spec hiển thị **`gates_reset[]`** — ⛔ reset **không được im lặng**, và thông báo ⛔ không được **tự biến mất** | `SDD-HG-01.5`; Hệ quả API **#4** (*"⛔ Không được reset im lặng — người dùng phải biết trang vừa **rời trạng thái xuất bản được**"*); `API-HG-4`; Threat Model `TM-F4-2` | ⛔ Không có component nào cho việc này · **hoặc** dùng **toast tự tắt 3s** — mất thông tin ⇒ trên thực tế vẫn là reset im lặng | Có component trạng thái **bền** mang danh sách gate bị reset không; nếu là toast ⇒ cờ |
| **`ARC-23`** | **PHẢI** có cờ `speaker_confidence` thấp; **VÀ** `UNKNOWN` là giá trị **hợp lệ** — ⛔ UI **không được chặn** PASS khi speaker là `UNKNOWN` | ⭐ `SDD-HG-01.3` (*"PASS nghĩa là **người đã xem**, ⛔ không nghĩa là hệ thống đã biết"*); `SRS-FR-14` (**CHỐT**); `DB-Entity-Dialogue-And-Gate` cột `speaker_confidence` | Không có cờ confidence · **hoặc** *"nút Xác nhận bị disable khi chưa chọn người nói"* — làm **cứng hơn** spec, cũng là sai | Hai phép kiểm: cờ tồn tại; và ⛔ không có luật validate nào chặn `UNKNOWN` |
| **`ARC-24`** | Design System ⛔ **KHÔNG được** trình bày *"ẩn/disable nút export"* như **biện pháp bảo đảm**. UI **phản ánh**, server **cưỡng chế** | Hệ quả API **#2**: *"⛔ Không dựa vào việc **UI ẩn nút**"*; Threat Model `TM-F6-1` (*"⭐ Export CHÍNH LÀ đường bypass nếu nó không kiểm hai gate"*) | *"Nút Export disabled khi chưa đủ gate ⇒ đảm bảo không xuất bản được"* | Mọi câu chứa *"đảm bảo / ngăn / chặn"* trong Design System phải nói rõ điểm cưỡng chế nằm ở server |
| **`ARC-25`** | **PHẢI** tách **Preview** và **Export** thành hai bề mặt khác nhau: ⚠️ **Preview ⛔ KHÔNG bị chặn bởi gate** (đúng thiết kế); **Export** bị chặn bởi gate **VÀ** disable-access | Hệ quả API **#2** (⚠️ nguyên văn: *"Preview ⛔ KHÔNG bị chặn bởi gate — người dùng phải preview được **trước** khi gate PASS, đó chính là cách họ đi tới PASS"*); `ADR-013` `## Decision` **điều 8**; `SDD-HG-01.4`; `TM-F6-2` | Một component *"Render"* dùng chung, khoá theo cùng một điều kiện ⇒ chặn luôn preview ⇒ **phá đường người dùng đi tới PASS** | Đếm: Design System có **hai** luồng riêng không; điều kiện khoá của từng luồng có khác nhau không |
| **`ARC-26`** | `403 PROJECT_ACCESS_DISABLED` **PHẢI** có bề mặt hiển thị **riêng**, ⛔ không gộp với lỗi gate | `API-HG-13` (*"cả sáu endpoint kiểm cờ disable-access… **trước** mọi kiểm gate"*); `SDD-HG-01.4` (gộp **cả hai** điều kiện); Threat Model §4.4 `C3-K1`…`C3-K4` | Một Empty/Error state chung cho mọi `403` ⇒ project bị takedown hiện thông báo *"chưa qua gate"* | Bảng error state có phân biệt hai nguyên nhân không |
| **`ARC-27`** | Variant picker ⛔ **KHÔNG được** tự áp dụng lựa chọn; **PHẢI** giữ **cả hai** version side-by-side; và **`unclear` là câu trả lời hợp lệ hạng nhất** | `SRS-FR-21` (**CHỐT**): *"Cắt hẳn `[Fix automatically]`… giữ **cả hai** version, hiển thị side-by-side, **người chọn**, không bao giờ tự áp dụng. `unclear` là câu trả lời hợp lệ **hạng nhất**"* | Nút *"Áp dụng bản tốt nhất"* · picker chỉ có 2 lựa chọn A/B mà ⛔ không có *"chưa rõ"* | Picker có **đúng ba** lối ra không (A · B · `unclear`); có nút auto-apply không |

---

### 5. Vùng E — Anti-feature `SRS-NFR-15` và nghĩa vụ AI disclosure

#### 5.1 ⭐ CÓ — có bề mặt UI **không được phép tồn tại**

`SRS-NFR-15` là **anti-feature CHỐT**. Nguyên văn [Spec-Security-Legal-Compliance](../../../../030-Specs/Security/Spec-Security-Legal-Compliance.md) §5: xây bộ phát hiện *"tạo ra đúng cái tri thức mà luật đang miễn trừ cho việc **KHÔNG CÓ** ⇒ ⭐ **tự phá miễn trừ của chính mình**"*. Và §5.2 quy tắc **#2**: một đề xuất quét nội dung là *"**VI PHẠM một requirement CHỐT**, ⛔ không phải một cải tiến. Xử lý: **từ chối tại review**, ⛔ không thương lượng phạm vi"*.

⇒ Áp thẳng vào Design System / Brand Guidelines, **các bề mặt sau ⛔ KHÔNG được tồn tại**:

- ⛔ Badge / nhãn *"đã kiểm bản quyền"*, *"copyright checked"*, *"bản quyền an toàn"*.
- ⛔ Icon `shield` / `shield-check` / `verified` **mang nghĩa bản quyền** trong iconography set.
- ⛔ Nhãn *"Original"* / *"100% original"* / *"nội dung gốc"* gắn lên tác phẩm.
- ⛔ Điểm số hay thang màu *"copyright risk"* / *"similarity score"* / *"độ tương đồng"*.
- ⛔ Empty state hay cảnh báo *"phát hiện nội dung tương đồng"*.
- ⛔ **Brand messaging** kiểu *"an tâm về bản quyền"* — brand voice cũng là một bề mặt.

> [!WARNING]
> ⚠️ **Ranh giới ⛔ không được đọc quá** ([Spec-Security-Threat-Model](../../../../030-Specs/Security/Spec-Security-Threat-Model.md) §5): `SRS-NFR-15` cấm **phát hiện tương đồng nội dung**. Nó ⛔ **không** cấm rate limit, kiểm kích thước file, kiểm định dạng, log truy cập, `provider_refusal_log`. ⇒ Design System **VẪN** được khai trạng thái *file sai định dạng*, *vượt hạn mức*, *provider từ chối*. Đọc `SRS-NFR-15` thành *"cấm mọi kiểm tra trên upload"* là **sai theo chiều ngược lại**.

#### 5.2 ⭐ AI disclosure — CÓ, đây là yêu cầu **bắt buộc có bề mặt UI**

Trả lời dứt khoát: **CÓ**. Và nó là **nghĩa vụ duy nhất trong hệ thống mà bằng chứng tuân thủ là một bề mặt UI, ⛔ không phải một hàng dữ liệu.** Nguyên văn [Spec-Security-Legal-Compliance](../../../../030-Specs/Security/Spec-Security-Legal-Compliance.md) hàng **`L-6`**:

> *"Một **bề mặt UI** + có thể một trường cấu hình cấp hệ thống. ⚠️ **Nhỏ về kỹ thuật, ⛔ không được rơi** vì có deadline tuân thủ (`SRS-FR-40`)… Nghĩa vụ này ⛔ **không để lại hàng dữ liệu nào** ⇒ Security Review Gate ⛔ **không kiểm được nó từ database**. Bằng chứng phải là **ảnh chụp UI + hàng checklist ở tầng release**, ⛔ không phải một query."*

⇒ Nếu **Design System không khai component này thì ⛔ không có tài liệu nào khác khai nó** — và `SRS-FR-40` (**CHỐT**) rơi im lặng cho tới deadline **~01/03/2027**.

| ID | Phát biểu ràng buộc | Nguồn | Vi phạm trông như thế nào | Phát hiện bằng cách nào |
|---|---|---|---|---|
| **`ARC-28`** | ⛔ **KHÔNG được** tồn tại bề mặt UI nào biểu đạt phán đoán *"nội dung này có/không vi phạm bản quyền"* (badge, icon shield, nhãn *Original*, điểm rủi ro, cảnh báo tương đồng, brand messaging) | `SRS-NFR-15` (**CHỐT**); `Spec-Security-Legal-Compliance` §5.2 quy tắc **1–4**, §5.3 bảng ranh giới; `DB-Entity-Compliance-And-Takedown` **`INV-IC-5`** (*"⛔ không cột nào biểu diễn suy đoán vi phạm"*); `API-HG-11` | Icon set có `shield-check` gán nghĩa bản quyền · badge *"Original"* trong bảng component · tagline *"an tâm về bản quyền"* | `grep -in "bản quyền\|copyright\|plagiar\|similarity\|tương đồng\|đạo văn\|original\|shield\|verified"` trong `docs/040-Design/**` ⇒ **mọi hit phải đọc lại nghĩa**, ⛔ không lướt |
| **`ARC-29`** | Nếu Design System khai component cho kết quả **ingest check**, nó **PHẢI** phát biểu đúng ngữ nghĩa *"phát hiện **opt-out signal do chủ sở hữu gắn**"*; ⛔ không đặt tên/copy thành *"kiểm tra vi phạm"* | `Spec-Security-Legal-Compliance` §5.3: *"**Đọc nhãn không tạo ra tri thức suy đoán**"* — được phép; **suy đoán** thì không. `SRS-FR-37` · `KC-6` (⚠️ *trích gián tiếp* qua [Glossary](../../../../999-Resources/Glossary.md) mục *opt-out signal* và §5.3) | Component tên `CopyrightCheckResult` cho đúng chức năng đọc opt-out signal | Đọc **tên + copy** của mọi component liên quan ingest; ngữ nghĩa sai ⇒ cờ dù chức năng đúng |
| **`ARC-30`** | **PHẢI** khai **AI-disclosure indicator** hiển thị **tại điểm tương tác AI** (generate, pick variant), và nó ⛔ **không được** có biến thể ẩn/tắt được | `SRS-FR-40` (**CHỐT**); `Spec-Security-Legal-Compliance` `L-6` (*"một **bề mặt UI**"*, bằng chứng = **ảnh chụp UI**); `Spec-Security-Threat-Model` hàng `L-6`: *"⛔ **không được** là một cờ cấu hình **tắt được** — cùng khuôn `SDD-HG-01.2`"*; `Story-AI-Disclosure-Article-11` AC #1 (*"⛔ không phải chỉ ghi trong ToS"*) | ⛔ Không có component nào · **hoặc** có prop `showAiBadge={false}` / *"ẩn trong chế độ tập trung"* · **hoặc** disclosure chỉ nằm ở footer/ToS | Component tồn tại không; có prop/variant tắt được không; nó xuất hiện ở màn **generate** và **variant picker** không |
| **`ARC-31`** | Provenance marker cấp page/panel **PHẢI** biểu đạt **đủ ba** giá trị `origin`, đặc biệt trạng thái **hỗn hợp** `ai_edited` — ⛔ không gộp về *"AI"* hay *"human"* | `SRS-FR-39` (**CHỐT**, *"thiết kế theo diễn giải **RỘNG**"*); `DB-Entity-Generation` §danh mục đóng: `origin` ∈ `('ai','ai_edited','human')`; `Story-AI-Disclosure-Article-11` §*Đường không hạnh phúc* (nội dung hỗn hợp ⛔ không được gắn nhãn sai lệch) | Badge chỉ có 2 trạng thái `AI` / `Human` | Đếm **3** giá trị; có variant cho `ai_edited` không |
| **`ARC-32`** | ⛔ **KHÔNG được** viết bất kỳ khẳng định tuân thủ nào (*"đã tuân thủ Luật TTNT 2025"*, *"watermark hợp chuẩn"*) | Phạm vi **khoản 4 Điều 11** là `TBD` (`Story-AI-Disclosure` §3 — *hai cách đọc HẸP/RỘNG, ghi cả hai, ⛔ không chọn một*); `SRS-NFR-16` (**CHƯA QUYẾT → `TBD`**: SynthID có thoả nghĩa vụ hay không — *"phải verify, ⛔ không giả định"*) | Brand Guidelines có dòng *"Tuân thủ đầy đủ quy định về nội dung AI"* | `grep -in "tuân thủ\|compliant\|hợp chuẩn\|đạt chuẩn"`; mọi hit phải trỏ `TBD` |
| **`ARC-33`** | **PHẢI** khai component **công bố độ phủ checker** dạng *"đã kiểm N/M panel, M−N panel không kiểm được vì có nhiều nhân vật"* | `SRS-FR-22` (**CHỐT** — *"đây là **FR minh bạch**, **không phải** chỉ tiêu chất lượng"*); `SDD` §6.4 guardrail **#3**: *"⛔ Không được **giấu** con số này để trông đẹp hơn"* | ⛔ Không có · **hoặc** hiển thị một phần trăm làm tròn lên, giấu mẫu số và giấu lý do | Component tồn tại; có **cả tử số, mẫu số và lý do** không |
| **`ARC-34`** | Brand Guidelines ⛔ **KHÔNG được** nhắm hay nói với **cộng đồng hoạ sĩ**; positioning là **disclosure-first, nhắm writer** | [Charter](../../../Charter-Comic-Studio.md) §7 **`C5`** (*"Cấm marketing vào cộng đồng hoạ sĩ"*); [OKRs](../../../OKRs.md) §6 **`AG-2`** (*"Kênh cộng đồng là kênh **CÓ RỦI RO NGƯỢC**, không trung tính"*) — **CHỐT** | Brand persona / tone viết cho *"nghệ sĩ số"*; moodboard mượn ngôn ngữ cộng đồng vẽ; tagline *"dành cho người sáng tạo hình ảnh"* | Đọc mục *Audience* và *Tone of voice*: đối tượng có phải **writer** không |

---

### 6. Vùng F — NFR chạm UI: cái nào có số, cái nào phải để `TBD`

[SRS](../../../../020-Requirements/SRS-Comic-Studio.md) §5 chia rõ: **§5.1 — 17 hàng có chỉ tiêu** · **§5.2 — 14 hàng `TBD`** (đã đếm lại từng bảng, khớp; nguồn gốc: [findings/architect run 2026-08-24](../../2026-08-24-khoi-tao-requirements-stories-comic-studio/findings/architect.md) §3.1/§3.2). SRS mở mục này bằng: *"⚠️ **Copy số thì copy cả nhãn.** Nhãn `[EM]` nghĩa là *khoảng trống dữ liệu được thừa nhận*, **không phải sự thật đã đo**."*

#### 6.1 ✅ Có số — Design System **được** dùng, kèm nhãn

| Chỉ tiêu | Số | Neo | Chạm UI ở đâu |
|---|---|---|---|
| Polling trạng thái job | **2 giây** | `SRS-NFR-06` (⚠️ **MẶC ĐỊNH**) | Nhịp cập nhật mọi trạng thái async |
| best-of-N | **N = 3** candidate/panel | `CF-3.1` `[OFF]` | Variant picker hiển thị **3** ứng viên |
| Trần nhân vật/panel | **≤ 3** | `CF-6.5` `[OFF]` | Validation + empty/limit state của panel |
| Hold reserve credit | **3 credit/panel** | `MVP-Scope §6 KC-7` | Copy của màn xác nhận trừ credit |
| Độ phủ Continuity Checker | **40–60%** | `CF-6.11` `[EM]` ⚠️ | ⭐ **Con số phải CÔNG BỐ** (`SRS-FR-22`), ⛔ **không** phải chỉ tiêu để đạt |
| Takedown SLA | **72 giờ** | `CF-7.6` `[OFF]` | Copy của bề mặt takedown công khai |
| Deadline AI disclosure | **~01/03/2027** | `Charter §7 C4` `[OFF]` ⚠️ *hai nguồn mô tả phạm vi khác nhau* | Mốc thời gian, ⛔ không phải nhãn tuân thủ |
| Emphasis budget/chapter | **1 full page + 2–3 large panel** | `Analysis §5.3` `[EM]` | Ràng buộc layout, ⛔ chưa phải quy tắc UI |

#### 6.2 ⛔ `TBD` — Design System **KHÔNG được tự điền**

`Latency / response time API` · `Thời gian sinh một panel p50/p95` · `Uptime / availability SLA` · `Rate limit per tenant` · `Giới hạn dung lượng / số file upload` · `Thời hạn signed URL` · `RPO / RTO / backup retention` — cùng 7 hàng còn lại của SRS §5.2 (không chạm UI).

| ID | Phát biểu ràng buộc | Nguồn | Vi phạm trông như thế nào | Phát hiện bằng cách nào |
|---|---|---|---|---|
| **`ARC-35`** | Mọi con số **chỉ tiêu** trong Design System **PHẢI** truy được về SRS §5.1; không truy được ⇒ ghi **`TBD`** | `SRS` §5.1 / §5.2 / §5.3 | *"Skeleton hiển thị nếu request > **300ms**"* · *"Upload tối đa **10MB**"* · *"Signed URL hết hạn sau **15 phút**"* · *"Toast tắt sau 5s **theo NFR**"* | Liệt kê mọi số có đơn vị **thời gian / dung lượng / phần trăm**; số nào ⛔ không có neo và ⛔ không mang nhãn *quyết định Phase 3* ⇒ cờ |
| **`ARC-36`** | Design System **VẪN được** đặt giá trị thiết kế (animation duration, skeleton delay, breakpoint) — nhưng **PHẢI** dán nhãn *"quyết định mới của Phase 3"*, ⛔ **không** dán *"theo NFR/SRS"* | `SRS` §5.2 (⛔ không có hàng nào); `SRS` §5.3 (*"⚠️ hai con số `[EM]` **KHÔNG được nâng** thành NFR chỉ tiêu"*) | *"Theo yêu cầu hiệu năng của SRS, transition = 150ms"* — gán một nguồn không tồn tại | Mọi câu chứa *"theo SRS / theo NFR / theo yêu cầu"* phải grep ngược ra được hàng thật |
| **`ARC-37`** | ⚠️ **Accessibility ⛔ KHÔNG phải requirement kế thừa.** Design System được đặt mục tiêu a11y, nhưng **PHẢI** khai đó là **quyết định mới của Phase 3** | ⭐ **grep toàn `docs/` cho `WCAG` · `accessibility` · `khả năng tiếp cận` · `contrast ratio`**: chỉ **2 hit**, ở [findings/business-analyst run 2026-08-28](../../2026-08-28-phase-2-architecture-design-comic-studio/findings/business-analyst.md) §2.4 và ở **brief của chính run này** ⇒ ⛔ **không hit nào trong `docs/020-Requirements/`**. BA findings §2.4 đã verify độc lập và kết luận: *"⛔ không hit nào là một requirement"* | *"Đạt WCAG 2.1 AA **theo yêu cầu phi chức năng**"* · *"contrast ratio 4.5:1 **theo SRS**"* | `grep -in "WCAG\|a11y\|accessibility\|contrast"` trong `docs/040-Design/**`; mỗi hit phải mang nhãn nguồn **Phase 3** |
| **`ARC-38`** | ⛔ **KHÔNG được** khai một **i18n strategy** (locale switching, RTL, plural rules) như ràng buộc kế thừa | `SRS` §5.2 hàng **`b-6`**: artifact duy nhất là `SRS-FR-16` — một FR về **typesetting**, *"**không phải NFR ngôn ngữ**"*; nội dung đa ngôn ngữ *"chưa bao giờ được phát biểu thành requirement"*. `ADR-001` bảng `TBD`: ⚠️ *"ADR này đóng việc CHỌN ngôn ngữ/framework, ⛔ **KHÔNG** đóng"* hàng i18n/l10n — owner **Dev đề xuất, Founder duyệt**, *sau khi stack dựng, trước MVP1* | *"Typography hỗ trợ `vi-VN` và `en-US`"* · token RTL mirroring | `grep -in "i18n\|l10n\|locale\|RTL\|đa ngôn ngữ"`; mọi hit phải trỏ `b-6` là `TBD` |

---

### 7. Mâu thuẫn phát hiện được — ⛔ em KHÔNG phân xử, để PM

| # | Mâu thuẫn | Hai phía | Vì sao nó chạm Design System | Đề nghị của em |
|:--:|---|---|---|---|
| **`X-1`** | **Độ rắn của `D-45` / `SRS-NFR-06` đọc ra hai kiểu** | [SRS](../../../../020-Requirements/SRS-Comic-Studio.md) §3 hàng `SRS-NFR-06` và [ADR-015](../../../../030-Specs/Architecture/ADR-015-Job-Queue-In-Postgres.md) đều ghi **`MẶC ĐỊNH` — mở lại được khi tiền đề đảo**. Nhưng [ADR-001](../../../../030-Specs/Architecture/ADR-001-Backend-And-Frontend-Tech-Stack.md) liệt kê `D-45` dưới tiêu đề *"Ràng buộc kế thừa mà stack phải đỡ được **(⛔ không mở lại)**"* | Nếu writer đọc ADR-001 trước, `D-45` thành **CHỐT** ⇒ Design System dán sai nhãn cho toàn bộ tầng trạng thái async | ⚠️ **Có thể chỉ là bẫy đọc lướt**: chữ *"⛔ không mở lại"* của ADR-001 nhiều khả năng nói *"ADR **này** không mở lại"*, ⛔ không phải *"bất biến vĩnh viễn"*. ⇒ Design System lấy nhãn từ **SRS** (**MẶC ĐỊNH**) và ⛔ tuyệt đối không tự nới. **PM xác nhận cách đọc.** |
| **`X-2`** | **Brief của run này gán cho ADR-001 một nội dung ADR-001 ⛔ không có** | [brief.md](../brief.md) §Assumptions **#2**: *"design token phải phát biểu bằng Tailwind theme + **CSS variable theo quy ước shadcn** (`--background`, `--foreground`, `--primary`…)"*. ⛔ **ADR-001 không nêu một tên biến nào** — em đã đọc toàn văn | Writer Bước 5 sẽ trích **ADR-001** làm nguồn cho **tên biến** ⇒ gieo một neo giả vào tài liệu tầng 040 | Quy ước đặt tên biến là **quyết định mới của Phase 3** (hợp lệ, và nên chọn theo shadcn) — nhưng **PHẢI** dán nhãn Phase 3, ⛔ không trích ADR-001 |
| **`X-3`** | **Mọi tài liệu neo đều `status: draft`** | `ADR-001`, `ADR-013`, `SDD-Comic-Studio`, `SRS-Comic-Studio` — cả bốn đều `status: draft` (đã đọc frontmatter) | Design System sẽ là tài liệu tầng 040 neo vào một nền chưa `approved`; cộng thêm `Q-C` của brief (thay đổi ADR-001 **chưa commit** ở checkout gốc) | Ghi nhận **minh bạch** trong Design System: *"neo vào ADR/SDD/SRS ở trạng thái `draft` tại 2026-08-30"*. ⛔ Không phải việc của em để đổi status |

---

### 8. Nợ kỹ thuật Phase 2 có chạm UI — writer phải biết trước

Từ [000-Index](../../../../000-Index.md) §*Nợ kỹ thuật đã biết* (8 khoản Phase 2), **ba** khoản chạm bề mặt UI:

| # | Nợ | Mức | Hệ quả lên Design System |
|:--:|---|:--:|---|
| **2** | Role thứ năm `app_operator` chưa có; hai endpoint admin takedown `TD-2`/`TD-3` **đang BỊ CHẶN** | **Cao** | ⛔ **Không thiết kế màn hình vận hành takedown**. `Spec-Security-Legal-Compliance` §6.1: *"⭐ `L-4(c)` (SLA 72h) ⛔ **chưa chạy được trên thực tế**"*. Bề mặt **công khai** `TD-1` thì đã CHỐT ⇒ được thiết kế |
| **6** | Chuẩn `error_code` + error envelope (`TBD-API-ENV`), casing còn lẫn | Trung bình | Xem `ARC-17` — ⛔ không tự chốt format mã lỗi |
| **8** | Còn 1 anchor gãy cứng + ~29 gãy mềm ở `Architecture/` và `Schema/` | Thấp | Link từ Design System sang hai thư mục đó phải **verify từng cái**, ⛔ không copy anchor từ MOC |

---

### 9. Ba câu trả lời dứt khoát cho PM (tóm tắt vùng B, C, D, E)

1. **Mấy hệ font?** — ⭐ **HAI**, tối thiểu. Font UI (browser) và font render (compositor) khác nhau **về bản chất spec**: font render là **tham số của thuật toán wrap**, phải **đơn trị**, ⛔ không fallback stack, và tên cụ thể hiện là **`TBD-FONT`**. Khai một bộ font ⇒ hỏng ở **bước composite**, biểu hiện là dấu bị cắt / chữ tràn bubble, và **chỉ lộ ra sau khi ảnh đã sinh**.
2. **Trạng thái UI nào bắt buộc?** — Phủ đúng **5 giá trị** của danh mục đóng `job_status` (`queued`, `running`, `succeeded`, `failed_permanent`, `failed_exhausted`), **cộng** trạng thái *refetch nền* (vì cache + poll 2 giây) và **cộng** một khuôn chờ dài sống được qua reload. Thiếu chờ dài ⇒ Design System thiếu đúng cái mà sản phẩm này dành phần lớn thời gian ở trong.
3. **Bề mặt nào bị cấm / bắt buộc?** — **Cấm**: mọi biểu đạt phán đoán bản quyền (`ARC-28`). **Bắt buộc**: AI-disclosure indicator tại điểm tương tác (`ARC-30`) — vì `L-6` nói thẳng bằng chứng tuân thủ là **một bề mặt UI**, ⛔ không phải một hàng dữ liệu; ⛔ không có Design System thì nghĩa vụ này ⛔ không có nhà.

---

### 10. Checklist verify cho Bước 6

Mỗi dòng là một phép kiểm **nhị phân**, chạy được bằng `grep` hoặc bằng một câu hỏi đếm được.

- [ ] Đếm số **hệ font** trong Typography spec — phải **≥ 2**, mỗi hệ ghi rõ *render bởi ai* (`ARC-08`)
- [ ] Tên họ font render mang `TBD` + owner **Architect + Founder** (`ARC-09`); mục font render ⛔ không có fallback stack (`ARC-10`)
- [ ] `grep -in "word-break\|hyphens\|text-wrap\|ngắt dòng"` ⇒ ⛔ không hit nào áp cho bubble (`ARC-11`)
- [ ] Đếm **5** giá trị `job_status`, có tách hai loại `failed` (`ARC-14`)
- [ ] `grep -in "realtime\|websocket\|SSE\|live"` ⇒ 0 hit (`ARC-15`)
- [ ] `grep -in "skip\|duyệt tất cả\|approve all\|bulk\|hàng loạt\|tự động duyệt"` ⇒ 0 hit (`ARC-20`)
- [ ] ⛔ Không control nào trong khối gate có `defaultValue`/`defaultChecked` (`ARC-21`)
- [ ] Có component **bền** (⛔ không phải toast) cho `gates_reset[]` (`ARC-22`)
- [ ] Preview và Export là **hai** bề mặt, điều kiện khoá **khác nhau** (`ARC-25`)
- [ ] Variant picker có **ba** lối ra (A · B · `unclear`), ⛔ không auto-apply (`ARC-27`)
- [ ] `grep -in "bản quyền\|copyright\|similarity\|tương đồng\|original\|shield\|verified"` ⇒ mọi hit đọc lại nghĩa (`ARC-28`)
- [ ] AI-disclosure component tồn tại, ⛔ không prop tắt được, có mặt ở generate + variant picker (`ARC-30`)
- [ ] Provenance marker có **3** giá trị, có variant `ai_edited` (`ARC-31`)
- [ ] Có component công bố độ phủ checker với **tử số + mẫu số + lý do** (`ARC-33`)
- [ ] Audience của Brand Guidelines là **writer**, ⛔ không phải hoạ sĩ (`ARC-34`)
- [ ] Mọi con số có đơn vị đều có neo SRS §5.1 **hoặc** nhãn *quyết định Phase 3* (`ARC-35`, `ARC-36`)
- [ ] `grep -in "WCAG\|accessibility\|contrast"` ⇒ mọi hit mang nhãn Phase 3, ⛔ không viện dẫn SRS (`ARC-37`)
- [ ] `grep -in "i18n\|locale\|RTL"` ⇒ mọi hit trỏ `b-6` = `TBD` (`ARC-38`)
- [ ] Mọi phát biểu ràng buộc có nhãn `CHỐT` / `MẶC ĐỊNH` / `TBD` + neo (`ARC-04`)

---

## Tài liệu tham khảo

- [ADR-001 — Backend And Frontend Tech Stack](../../../../030-Specs/Architecture/ADR-001-Backend-And-Frontend-Tech-Stack.md) — `## Decision` Tầng CHỐT điều 1–8 · Tầng MẶC ĐỊNH · `## Consequences` §Tiêu cực #1, #3, #5 · §Đường lui
- [ADR-013 — Typeset Layer Separate From Art](../../../../030-Specs/Architecture/ADR-013-Typeset-Layer-Separate-From-Art.md) — `## Decision` điều 1–9 · bảng `TBD`
- [ADR-015 — Job Queue In Postgres](../../../../030-Specs/Architecture/ADR-015-Job-Queue-In-Postgres.md) — `Q5` error taxonomy · `Q6` `CT-POLL-2S`
- [SDD — Comic Studio](../../../../030-Specs/Architecture/SDD-Comic-Studio.md) — **§6.3 `SDD-HG-01`** (nguồn duy nhất) · §6.4 observability
- [SRS — Comic Studio](../../../../020-Requirements/SRS-Comic-Studio.md) — §3 (`SRS-FR-10/11/12/14/16/21/22/39/40`, `SRS-NFR-06/15`) · §5.1 · §5.2 · §5.3
- [Spec-Security-Legal-Compliance](../../../../030-Specs/Security/Spec-Security-Legal-Compliance.md) — §5 anti-feature · §6 takedown · `L-6`
- [Spec-Security-Threat-Model](../../../../030-Specs/Security/Spec-Security-Threat-Model.md) — §5 · `TM-F4-*` · `TM-F6-*` · `L-6`
- [DB-Entity-Job-Queue](../../../../030-Specs/Schema/DB-Entity-Job-Queue.md) · [DB-Entity-Typeset-Layer](../../../../030-Specs/Schema/DB-Entity-Typeset-Layer.md) · [DB-Entity-Dialogue-And-Gate](../../../../030-Specs/Schema/DB-Entity-Dialogue-And-Gate.md) · [DB-Entity-Generation](../../../../030-Specs/Schema/DB-Entity-Generation.md) · [DB-Entity-Compliance-And-Takedown](../../../../030-Specs/Schema/DB-Entity-Compliance-And-Takedown.md)
- [Endpoint-Human-Gates](../../../../030-Specs/API/Endpoint-Human-Gates.md) `API-HG-1`…`API-HG-13` · [Endpoint-Preview-Export](../../../../030-Specs/API/Endpoint-Preview-Export.md) `API-PE-6`
- [Story-AI-Disclosure-Article-11](../../../../022-User-Stories/Backlog/Story-AI-Disclosure-Article-11.md)
- [Charter](../../../Charter-Comic-Studio.md) §7 `C5` · [OKRs](../../../OKRs.md) §6 `AG-2` · [000-Index](../../../../000-Index.md) §Nợ kỹ thuật đã biết
- [findings/architect — run 2026-08-24](../../2026-08-24-khoi-tao-requirements-stories-comic-studio/findings/architect.md) §3.1 (17 NFR có số) · §3.2 (14 NFR `TBD`)
- [findings/business-analyst — run 2026-08-28](../../2026-08-28-phase-2-architecture-design-comic-studio/findings/business-analyst.md) §2.4 (verify: accessibility ⛔ không phải requirement)
