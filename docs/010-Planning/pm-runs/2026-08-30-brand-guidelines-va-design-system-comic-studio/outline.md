# Doc Plan: 2026-08-30-brand-guidelines-va-design-system-comic-studio

> **File này PM độc quyền chỉnh sửa.** Writer báo xong trong `SUMMARY` + `FILES_TOUCHED`, PM đối chiếu ownership rồi mới tick. ⛔ Không tick thay worker.
> **Quy ước link — theo RULE-001 quy tắc #5**: dùng **standard markdown link relative path** `[Text](./path.md)`. ⛔ **KHÔNG dùng wiki-link `[[...]]`** (mô tả trong `pm-doc.md` đã lỗi thời; RULE-001 `updated: 2026-08-24` là contract có hiệu lực).

## Hạng mục

| # | Tài liệu | Loại (RULE-001) | Đích | Template | Trạng thái đích | Writer | Lô | Xong |
|---|----------|-----------------|------|----------|-----------------|--------|----|------|
| 1 | Brand Guidelines | Design System (`G-4`) | `docs/040-Design/Design-System/Brand-Guidelines.md` | — (không có template chuyên biệt) | `draft` | `product-designer` | L1 | **[x]** |
| 2 | Foundations | Design System | `docs/040-Design/Design-System/Foundations.md` | — | `draft` | `product-designer` | L1 | **[x]** |
| 3 | Color Tokens | Design System | `docs/040-Design/Design-System/Color-Tokens.md` | — | `draft` | `product-designer` | L2 | **[x]** |
| 4 | Spacing & Layout | Design System | `docs/040-Design/Design-System/Spacing-And-Layout.md` | — | `draft` | `product-designer` | L2 | **[x]** |
| 5 | ⭐ Typography | Design System | `docs/040-Design/Design-System/Typography.md` | — | `draft` | `product-designer` | L3 | **[x]** |
| 6 | Components | Design System | `docs/040-Design/Design-System/Components.md` | — | `draft` | `product-designer` | L4 | **[x]** |
| 7 | Glossary (bổ sung nhóm design) | Glossary | `docs/999-Resources/Glossary.md` | — | `live` (giữ nguyên) | `business-analyst` | L5 | **[x]** |
| 8 | Design MOC | *(MOC — hiện **0 byte**)* | `docs/040-Design/Design-MOC.md` | theo MOC khác trong repo | `live` | **PM** | close | **[x]** |
| 9 | Index | Index | `docs/000-Index.md` | — | `live` (giữ nguyên) | **PM** | close | **[x]** |

> ⚠️ **`docs/999-Resources/Templates/` ⛔ KHÔNG có template nào cho Design System** (13 khuôn, đã liệt kê ở `000-Index.md`, không khuôn nào hợp). Writer tự dựng cấu trúc theo outline dưới đây — ⛔ **không** ép vào `Template-Spec.md` cho có.

## Frontmatter bắt buộc — áp cho cả 6 file Design System

```yaml
---
id: DS-{NNN}                 # DS-001 Brand-Guidelines … DS-006 Components
type: design-system
status: draft
project: comic-studio
owner: "@trisjr"
tags: [design-system, phase-3]
created: 2026-08-30
updated: 2026-08-30
---
```

`id` cấp cứng, ⛔ writer không tự đặt: `DS-001` Brand-Guidelines · `DS-002` Foundations · `DS-003` Color-Tokens · `DS-004` Spacing-And-Layout · `DS-005` Typography · `DS-006` Components.

---

## Outline từng tài liệu

### 1. `Brand-Guidelines.md` (L1)

- **Độc giả đích**: AI assist sinh code + Founder. Đọc để biết **màu/tone nào được phép**, và **điều gì bị cấm nói**.
- **Cấu trúc**:
  `# Brand Guidelines` · `## Hệ này quản gì / ⛔ không quản gì` · `## Tên hiển thị` (⚠️ `TBD` có chủ) · `## Audience có căn cứ` (4 actor, ⛔ không persona) · `## Tone & personality` · `## Hướng màu chủ đạo` (trung tính + accent lạnh) · `## ⛔ Điều CẤM tuyệt đối trong mọi biểu đạt thương hiệu` · `## Bề mặt takedown công khai — nghĩa vụ pháp lý, ⛔ không phải điểm chạm marketing`
- **Nguồn sự thật**:
  `run-plan.md` §Gate `G-1` (tone + màu — **quyết định của anh**, ⛔ không phải suy diễn) · `findings/business-analyst.md` §4.2 (4 actor có anchor: tác giả truyện chữ · Founder-operator · chủ sở hữu quyền bên ngoài · độc giả/cơ quan quản lý) và §4.4 (bảng *"KHÔNG được neo vào"*) · `findings/product-designer.md` §1.2, §2.1 · ⭐ `SRS-NFR-15` + `docs/030-Specs/Security/Spec-Security-Legal-Compliance.md` (mục CẤM) · `escalations.md` `E4` (takedown), `E7` (tên `TBD`)
- **Tiêu chí xong**: (a) mục CẤM liệt kê đích danh ít nhất: badge "đã kiểm bản quyền", icon shield, nhãn "Original", messaging kiểu *"an tâm về bản quyền"* — kèm trích `SRS-NFR-15`; (b) mục tên hiển thị ghi `TBD` **có chủ**, ⛔ không có bất kỳ tên đề xuất nào; (c) audience chỉ gồm 4 actor có anchor, mỗi actor kèm UC/tài liệu chứng minh; (d) ⛔ **0 dòng persona**.

### 2. `Foundations.md` (L1)

- **Độc giả đích**: AI assist — đây là file nó đọc **trước tiên** để biết luật chơi của 4 file sau.
- **Cấu trúc**:
  `# Foundations` · `## Hệ thống này quản cái gì / ⛔ KHÔNG quản cái gì` · `## Kiến trúc token: primitive → semantic` · `## Hợp đồng phát biểu token` (CSS variable ↔ Tailwind ↔ shadcn) · `## Chiến lược light/dark` · `## Chuẩn accessibility` · `## Cách kiểm (checklist cơ học)`
- **Nguồn sự thật**:
  `ADR-001` §Decision điều **5, 6** + bảng *Tầng MẶC ĐỊNH* · `run-plan.md` `G-2` (light default, khai đủ cặp dark), `G-3` (WCAG 2.2 AA, desktop-first) · `findings/product-designer.md` §4.2, §4.3 · `findings/architect.md` `ARC-36`
- **Tiêu chí xong**: (a) mục *"⛔ KHÔNG quản cái gì"* nêu rõ hệ này **không quản hình học panel/bubble** (thuộc `ADR-013`) và **không quản font render vào ảnh**; (b) hợp đồng token phát biểu **một chiều phụ thuộc**: CSS variable là **nguồn**, Tailwind **tham chiếu** — ⛔ không đối xứng; (c) mục a11y ghi **WCAG 2.2 AA** kèm **SC 2.5.7** và nói rõ nó **sinh UI thật** ở `Components.md`; (d) ⭐ mọi tên biến shadcn dán nhãn **"quyết định Phase 3"**, ⛔ **KHÔNG** trích `ADR-001` làm nguồn (mâu thuẫn `X-2`).

### 3. `Color-Tokens.md` (L2)

- **Độc giả đích**: AI assist — bảng tra, ⛔ không phải bài luận về màu.
- **Cấu trúc**:
  `# Color Tokens` · `## Primitive palette` · `## Semantic mapping` (đủ **cặp `-foreground`**) · `## Bộ biến quy ước shadcn` · `## Giá trị dark (khai sẵn, chưa implement)` · `## Bảng audit contrast` · `## ⭐ Màu trạng thái: BA MỨC phải phân biệt được`
- **Nguồn sự thật**:
  `run-plan.md` `G-1` (trung tính + accent lạnh), `G-2` (cặp dark), `G-3` (contrast AA) · `Foundations.md` §Hợp đồng phát biểu token (**L1 phải đóng trước**) · ⭐ `findings/business-analyst.md` §2.1 `C-01` — ba mức: **TỪ CHỐI ở tầng DB** (`M2-2`, `UC-03 EXC-1`, `UC-07 EX-7`, `UC-08 EX-6`) vs **CẢNH BÁO cho qua được** (`M2-3`, `UC-07 EX-1`) vs **thông tin** (`UC-09 EF-2`) · `ADR-013` §Decision 9 (trạng thái gate)
- **Tiêu chí xong**: (a) mọi semantic token có **cặp `-foreground`**, ⛔ không token nào đứng lẻ; (b) bảng audit contrast có **số tỷ lệ thật** cho mọi cặp text/nền của luồng chính, đối chiếu ngưỡng AA; (c) ⭐ ba mức alert có **ba dải màu phân biệt được**, kèm câu giải thích *vì sao trộn chúng là lỗi nghiệp vụ*; (d) accent lạnh **⛔ không đụng dải màu cảnh báo**; (e) mỗi token có cột giá trị dark.

### 4. `Spacing-And-Layout.md` (L2)

- **Độc giả đích**: AI assist.
- **Cấu trúc**:
  `# Spacing & Layout` · `## Thang spacing` · `## Radius / border / elevation` · `## Breakpoint` (desktop-first) · `## Z-index` · `## ⛔ Ranh giới: hệ này KHÔNG quản hình học panel/bubble`
- **Nguồn sự thật**:
  `MVP-Scope` §4.1 (toạ độ **0–1**) · `SRS` §3.D ràng buộc 2 · `ADR-013` §Decision 2 · `run-plan.md` `G-3` (desktop-first) · `Foundations.md` §Hợp đồng token
- **Tiêu chí xong**: (a) mục ranh giới nói rõ **toạ độ panel/bubble là hệ 0–1 do `ADR-013` sở hữu**, ⛔ không phải px của Design System — đây là chỗ dễ lẫn nhất; (b) z-index có **thang đặt tên**, ⛔ không phải số rời rạc; (c) breakpoint dán nhãn **"quyết định Phase 3"** (repo ⛔ không có requirement responsive nào — 0 hit).

### 5. ⭐ `Typography.md` (L3 — file rủi ro cao nhất run)

- **Độc giả đích**: AI assist **và** người sẽ implement compositor. Đây là file mà **hiểu sai thì hỏng sau khi đã tiêu tiền**.
- **Cấu trúc**:
  `# Typography` · `## ⭐ HAI HỆ FONT — ⛔ KHÔNG GỘP` · `## Hệ 1 — Font UI` (thang cỡ, weight, token, chạy ở browser) · `## Hệ 2 — Font render vào ảnh` (⛔ **chỉ ghi RÀNG BUỘC**, giá trị là `TBD` do `ADR-013` sở hữu) · `## Tiếng Việt: line-height & dấu chồng` · `## NFC / NFD` · `## Cỡ chữ bubble là HÀM của `text_budget`, ⛔ không phải giá trị chọn`
- **Nguồn sự thật**:
  ⭐ `ADR-001` §Decision **điều 8** + §Consequences **#5** (*"`Intl.Segmenter` giải quyết **ngắt**, KHÔNG giải quyết **đo**"*) · `ADR-013` §Decision 6 + hàng `TBD` *"Font sẽ render"* · `Glossary` mục *typeset layer*, *`text_budget`* · `findings/product-designer.md` §5.1–5.4 · `findings/architect.md` vùng B · `findings/business-analyst.md` §3.5 · `D-29` (cấm nướng chữ vào pixel)
- **Tiêu chí xong**: (a) ⭐ hai hệ font ở **hai mục H2 riêng**, và nói rõ **token ⛔ KHÔNG chung namespace** — font render ⛔ **không phải** CSS variable mà là **tham số config của `apps/api`**; (b) mục hệ 2 ghi **font render phải ĐƠN TRỊ, ⛔ không fallback stack**, kèm lý do (nó là **tham số đầu vào của thuật toán wrap**); (c) giá trị font render để `TBD` **có chủ** (Architect + Founder), ⛔ **run này KHÔNG chốt**; (d) có mục nêu **gộp một bộ thì hỏng ở đâu**: ngắt theo font A + vẽ bằng font B ⇒ dấu bị mép bubble cắt, **chỉ lộ sau khi ảnh đã sinh**, `D-29` ⛔ chặn đường vá nhanh; (e) line-height tiếng Việt tính đến **dấu chồng hai tầng**, ⛔ không copy giá trị mặc định của font Latin.

### 6. `Components.md` (L4)

- **Độc giả đích**: AI assist.
- **Cấu trúc**:
  `# Components` · `## Inventory theo nhóm màn hình` · `## Ánh xạ shadcn/Radix: dùng nguyên / mở rộng / tự build` · `## Ma trận state` (default·hover·focus·active·disabled·loading·error·empty) · `## Ba pattern đặc thù sản phẩm` · `## ⛔ Component KHÔNG được đặc tả ở run này`
- **Nguồn sự thật**:
  ⭐ `findings/business-analyst.md` §2.1 (`C-01`…`C-13` nền) + §2.2 (`C-14`…`C-16` **không hoãn được**) + §2.3 (danh sách **cấm**) · `findings/architect.md` vùng C, D, E · `MVP-Scope` §5.2 (5 thành phần bắt buộc) · `SRS` §3.D (`SRS-FR-10/12/14/16`, `SRS-NFR-06`, `SRS-NFR-23`) · `run-plan.md` `G-3` (SC 2.5.7)
- **Tiêu chí xong**:
  (a) phủ đủ **16 component không hoãn được** `C-01`…`C-16`;
  (b) ⭐ `C-01` Alert đặc tả **ba mức phân biệt được** kèm ví dụ UC cho từng mức;
  (c) ⭐ **SC 2.5.7**: `C-20` kéo bubble có **đường thao tác thay thế không-kéo** được đặc tả thật;
  (d) ⛔ **KHÔNG có component "Duyệt cả trang" / bulk approve** (`API-HG-6`), ⛔ **không control pre-selected** (`SDD-HG-01.1`);
  (e) **Preview và Export là hai bề mặt riêng** — Preview ⛔ không bị gate chặn, Export bị;
  (f) `C-10` AI-disclosure indicator có mặt (`SRS-FR-40`, **CHỐT**);
  (g) mục cấm liệt kê đích danh: tree/diff/branch generation (`D6`) · Layout Score (`C4`) · inpainting brush (`D5`) · infinite canvas (`D2`) · mọi dashboard copyright detection (`SRS-NFR-15`);
  (h) ⛔ **không** đặc tả component operator (`escalations.md` `E5`);
  (i) mọi latency/performance chưa có số ⇒ ghi `TBD`, ⛔ **không tự điền**.

### 7. `Glossary.md` — bổ sung (L5)

- **Độc giả đích**: mọi agent về sau.
- **Cấu trúc**: **append một nhóm mới** vào cấu trúc 10 nhóm sẵn có. ⛔ **Không sửa 69 thuật ngữ đang có.**
- **Nguồn sự thật**: 6 file Design System **đã viết xong** (L1–L4 phải đóng trước) + `findings/product-designer.md` §7.
- **Tiêu chí xong**: (a) mọi thuật ngữ rút từ **file đã tồn tại**, mỗi mục trỏ về file định nghĩa nó; (b) ⛔ **0 thuật ngữ nào được thêm mà không xuất hiện trong 6 file đó**; (c) `updated:` bump sang `2026-08-30`; (d) ⛔ không đụng nhóm cũ.

---

## Link phải tạo (standard markdown, RULE-001 §Linking Rules)

| Từ | Tới | Quan hệ |
|---|---|---|
| Cả 6 file Design System | `../Design-MOC.md` | `Part of:` — điều hướng ngược lên MOC |
| `Brand-Guidelines.md` | `./Color-Tokens.md` | màu thương hiệu là **nguồn** của `--primary` |
| `Foundations.md` | `./Color-Tokens.md` · `./Typography.md` · `./Spacing-And-Layout.md` · `./Components.md` | hợp đồng token áp cho cả 4 |
| `Foundations.md` | `../../030-Specs/Architecture/ADR-001-Backend-And-Frontend-Tech-Stack.md` | `Implements:` — stack đã chốt |
| `Typography.md` | `../../030-Specs/Architecture/ADR-013-Typeset-Layer-Separate-From-Art.md` | ⭐ sở hữu `TBD` font render |
| `Typography.md` | `../../030-Specs/Architecture/ADR-001-…md` | điều 8 wrap tiếng Việt |
| `Components.md` | `../../020-Requirements/SRS-Comic-Studio.md` | nguồn `SRS-FR-*` / `SRS-NFR-*` |
| `Components.md` | `../../030-Specs/Architecture/SDD-Comic-Studio.md` | `SDD-HG-01` cấm bypass gate |
| `Brand-Guidelines.md` | `../../030-Specs/Security/Spec-Security-Legal-Compliance.md` | `SRS-NFR-15` anti-feature |

> ⛔ **Writer KHÔNG được sửa file đích của các link trên** — chỉ trỏ tới. Mọi file đích nằm ngoài ownership.

## MOC cần cập nhật — **PM giữ, ⛔ không cấp cho worker**

| MOC | Mục thêm/sửa |
|---|---|
| `docs/040-Design/Design-MOC.md` | **Viết từ số 0** (hiện 0 byte): frontmatter + bảng 6 tài liệu Design System + ghi rõ `Wireframes/`, `Specs/`, `Assets/` **chưa có tài liệu, thuộc run sau** |
| `docs/000-Index.md` | §*040 · Design*: thay dòng *"⚠️ MOC hiện là file rỗng 0 byte"* bằng bảng 6 tài liệu · §*Nợ kỹ thuật* → gỡ khoản *"Design-MOC vẫn là file 0 byte"* · §*Run-state* → thêm hàng run này · §*999 Resources* → cập nhật số thuật ngữ Glossary |

## Ripple (T3) — tài liệu đang trích dẫn phạm vi này

| Tài liệu | Ảnh hưởng | Xử lý |
|---|---|---|
| `docs/000-Index.md` | Nêu đích danh *"Design-MOC vẫn là file 0 byte"* ở **hai chỗ** (§040 và §Nợ kỹ thuật) | PM sửa ở close-step |
| `docs/030-Specs/Architecture/ADR-013-*.md` | Sở hữu `TBD` font render mà `Typography.md` sẽ trỏ tới | ⛔ **Không sửa** — `Typography.md` chỉ **trỏ**, ⛔ không chốt hộ |
| `docs/020-Requirements/SRS-Comic-Studio.md` | `SRS-NFR-09` vẫn ghi frontend `CHƯA QUYẾT` trong khi `ADR-001` đã chốt (`X-5`) | ⛔ **Ngoài lane** — ghi vào *Nợ*, run đồng bộ 020↔030 xử lý |
| `docs/035-QA/**` | WCAG 2.2 AA (`G-3`) sẽ thành **chuẩn nghiệm thu** của tầng QA | Chưa có tài liệu QA nào ⇒ ⛔ không ripple ngay; ghi vào *Nợ* để Phase QA biết |
