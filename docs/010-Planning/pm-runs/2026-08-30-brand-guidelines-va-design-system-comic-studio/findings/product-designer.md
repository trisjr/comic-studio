# Findings — product-designer

> Lens thiết kế của Bước 2 (Analysis fan-out), run `2026-08-30-brand-guidelines-va-design-system-comic-studio`.
> Đây là **phân tích để PM lập plan**, ⛔ không phải nội dung Design System. Mọi khẳng định về repo đều có neo `file.md §mục`.
> Quy ước nhãn kế thừa từ Charter: `[OFF]` nguồn gốc · `[CHỐT]` quyết định của anh · `[EM]` **ước lượng, không phải số đo**.

---

## Kết luận của worker

### 0. Bốn thứ em phải nói trước, vì mọi mục sau đều dựa vào

| # | Sự thật | Neo |
|---|---|---|
| **F-1** | `docs/040-Design/` **rỗng hoàn toàn** — chỉ có 4 file `.gitkeep` và `Design-MOC.md` **0 byte**. ⇒ Run này viết trên nền trắng, ⛔ không có Design System cũ để kế thừa hay mâu thuẫn | `Glob docs/040-Design/**` · `docs/000-Index.md` §040-Design |
| **F-2** | Repo **KHÔNG có persona, JTBD, hay định nghĩa *"đủ tốt"*** — `TBD-1`…`TBD-5`, đã được xác minh và thừa nhận tường minh | `PRD-Comic-Studio.md` §3.3 |
| **F-3** | Repo **KHÔNG có một dòng nào** về a11y / WCAG / dark mode / responsive / contrast màu / logo / màu thương hiệu. Em đã grep toàn `docs/` — 0 hit là requirement UI (chi tiết ở [mục 6](#6-accessibility--dark-mode)) | grep `docs/` |
| **F-4** | **Chưa có dòng code nào** — `src/`, `test/` rỗng, verify bằng `find` tại thời điểm viết ADR-001 | `Charter` §1 `[OFF]` CF-1.3 · `ADR-001` §Context |

⇒ Hệ quả bao trùm lên cả run: Design System này **đi trước code**. Nó không mô tả cái đang có; nó **đặt ra cái sắp có**. Đó là lý do [mục 4](#4-tầng-token-phải-phát-biểu-bằng-ngôn-ngữ-nào) đòi token phải phát biểu dưới **đúng hình dạng file mà code sẽ có**, ⛔ không phải bảng hex trong markdown.

---

### 1. Sản phẩm này là gì, và điều đó ràng buộc brand thế nào

#### 1.1 Ba câu trả lời có căn cứ

| Câu hỏi | Trả lời | Neo |
|---|---|---|
| **Phục vụ ai** | **Tác giả truyện chữ (writer) KHÔNG biết vẽ.** ⛔ *Không* nhắm hoạ sĩ — đây là **loại trừ tường minh**, không phải ưu tiên | `Charter` §1 + §5.2 `[CHỐT]` CF-1.5 · `PRD` §3.1 (`CẤM-17`: cấm viết Use Case cho actor *"hoạ sĩ"*) |
| **Bán cái gì** | **SaaS multi-tenant, ba tầng**: T1 **$4–8/tháng KHÔNG image gen** (Story Bible + Comic IR + layout + versioning + export) · T2 credit pack managed inference (<~125 ảnh/tháng) · T3 **BYOK là tuỳ chọn MỞ KHOÁ**, ⛔ không phải điều kiện dùng | `Charter` §7 **C2** `[CHỐT]` CF-2.1–2.5 |
| **Đối thủ trông thế nào** | Ngách **không có unicorn nào**. Dashtoon $20,1M/465 người ⇒ ⛔ **không phải đối thủ tool** (là content studio). Anifusion: **solo founder, €20/mo, $833 MRR, có lãi, $0 marketing**. ComicInk: iOS, <1K downloads. ⭐ Comp thật là **Novelcrafter** (novel writing): **220.000+ authors** `[OFF]`, 4 tier **$4–20**, tier rẻ nhất **KHÔNG có AI** | `Analysis-Market-Competitor-Landscape` §2.3, §3.1, §3.2 Kết luận 1, §4.1 |

#### 1.2 Bốn ràng buộc brand rút ra được — có neo, ⛔ không suy diễn

| # | Ràng buộc | Vì sao |
|---|---|---|
| **B-1** | ⛔ **Ngôn ngữ hình ảnh KHÔNG được mượn code hình của công cụ vẽ** (brush, palette hoạ sĩ, canvas, bút cảm ứng) | `Charter` §7 **C5**: positioning **bắt buộc** là *"nhắm writer KHÔNG nhắm artist"*, và *"cấm marketing vào cộng đồng hoạ sĩ"* — căn cứ `[TC]` CF-5.6: Naver Webtoon bị **boycott**, BlueLine Studio bị **buộc vẽ lại**. Một brand trông như Procreate là tự đặt mình vào cộng đồng đã có tiền lệ tẩy chay |
| **B-2** | **Disclosure-first là một phần của brand, không phải một dòng chân trang** | `Charter` §7 **C5** + `SRS-FR-40` (user **phải nhận biết** đang tương tác với hệ thống AI) + `Glossary` mục *AI disclosure (Điều 11)*. Pattern từ research: *"covert use can corrode brand trust more than disclosure ever could"* (`Analysis-Market` §6.2). Đây là chỗ brand và compliance **trùng nhau** |
| **B-3** | Brand phải trông tốt ở **avatar · OG image · screenshot** TRƯỚC khi trông tốt ở landing page | Kênh đã có bằng chứng là **build-in-public trên X** ($0 spend, Anifusion) + **Discord tác giả**; ❌ Show HN là kênh **chết** (2 điểm/2 comment `[OFF]`) — `Analysis-Market` §6.1, §6.3 |
| **B-4** | Brand chủ yếu phục vụ **app shell sau đăng nhập**; landing/marketing là **tài sản tĩnh riêng** | `ADR-001` §Alternatives **E** lý do 3: *"SEO không phải yêu cầu: toàn bộ sản phẩm nằm sau đăng nhập"* + §Consequences tiêu cực **#6(a)**: landing page *"phải là tài sản tĩnh riêng, không dùng lại app"* |

#### 1.3 Khoảng trống persona — và brand neo vào cái gì thay thế

⛔ **Em KHÔNG bịa persona.** `PRD` §3.1 phát biểu thẳng ranh giới: *"**Phân khúc ≠ persona**. 'Tác giả truyện chữ không biết vẽ' trả lời câu **ai không phải khách hàng**. Nó **không** trả lời: người đó bao nhiêu tuổi, viết trên nền tảng nào, đã trả tiền cho công cụ gì… và **họ gọi cái gì là 'đủ tốt'**."*

Năm mảnh **có thật** mà brand được phép neo vào, xếp theo độ chắc:

| # | Neo thay thế | Nguồn | Độ chắc |
|---|---|---|---|
| 1 | **Phân khúc + loại trừ** — writer không biết vẽ, ⛔ không nhắm artist | `Charter` §1, §5.2 | `[CHỐT]` |
| 2 | **Positioning C5** — disclosure-first | `Charter` §7 C5 | `[CHỐT]` |
| 3 | **Mô hình 3 tầng C2** — brand phải nói được *"tier rẻ nhất không có AI vẫn đáng tiền"* | `Charter` §7 C2 | `[CHỐT]` |
| 4 | **Comp Novelcrafter** — 220K authors chứng minh cộng đồng **viết** chấp nhận AI tool ở quy mô lớn, trong khi cộng đồng **vẽ** boycott | `Analysis-Market` §4.1, §6.2 | `[OFF]` (nhưng ⚠️ *"220K authors không rõ là user hay paying user"* — §7 khoảng trống **3.d**) |
| 5 | **Proxy *"đủ tốt"* duy nhất repo có**: cạnh **mọi** metric kỹ thuật phải có đúng một câu người trả lời — ***"trang này đọc có ổn không?"*** | `PRD` §3.3, thực thi tại `FR-H-06`/`FR-H-02` | ⚠️ `PRD` §3.3 ghi rõ: **proxy này KHÔNG phải persona**, là ngưỡng do **chính người build** đặt |

> ⚠️ **Hệ quả bắt buộc cho writer ở Bước 5** (`PRD` §3.3 hệ quả #2): *"Mọi ngưỡng UX trong tầng này là ngưỡng **tự đặt**, phải mang nhãn `[EM]`."* ⇒ Mọi con số UX trong Design System (contrast, target size, thang spacing, breakpoint) **phải mang `[EM]`**. Viết chúng như sự thật đã đo là vi phạm quy ước của tầng Requirements.

**Ba thứ ⛔ tuyệt đối không có trong repo, và ⛔ agent không được sinh ra**: **tên hiển thị thương mại** (`comic-studio` là *project name* — `Charter` §1, ⛔ không phải tên sản phẩm đã chốt) · **màu thương hiệu** (0 hit) · **logo** (0 hit).

---

### 2. Brand Guidelines nên gồm những mục nào

Ràng buộc cắt: **1 người + AI assist, ⛔ không funding, ⛔ không ngân sách marketing** (`Charter` §7 **C1** `[CHỐT]`), sản phẩm **sau đăng nhập** (B-4). ⇒ ⛔ Không bê brand book doanh nghiệp.

#### 2.1 Bảy mục tối thiểu đủ dùng

| # | Mục | Nội dung | Ai quyết |
|---|---|---|---|
| **BG-1** | **Định vị & audience** | Phân khúc, cái ⛔ không nhắm, positioning disclosure-first. ~1 trang, chủ yếu **trích lại** Charter chứ ⛔ không phát minh | Agent viết được (đã `[CHỐT]`) |
| **BG-2** | **Tên & cách viết tên** | Tên hiển thị · viết hoa/gạch nối · có tagline không · dùng trong câu thế nào | ⚠️ **ANH QUYẾT** |
| **BG-3** | **Tone & voice** | Hướng tone (3–5 tính từ) + do/don't + mẫu câu cho **5 loại text hay gặp**: empty state · error · gate prompt · cảnh báo tốn tiền · AI disclosure | ⚠️ **ANH QUYẾT hướng**; agent viết phần thực thi |
| **BG-4** | **Hướng màu chủ đạo** | Agent đưa **2–3 hướng** kèm lập luận; ⛔ **agent không tự chốt hex** | ⚠️ **ANH QUYẾT** |
| **BG-5** | **Tài sản tối thiểu** | **Chỉ 4 thứ**: wordmark · favicon · OG image · avatar X/Discord (theo **B-3**). ⛔ Không clear-space rule, ⛔ không co-branding, ⛔ không print spec | Agent đề xuất sau BG-2/BG-4 |
| **BG-6** | ⭐ **Ngôn ngữ hình ảnh — ĐƯỢC và KHÔNG ĐƯỢC** | Hiện thực trực tiếp của **B-1**. Cộng quy tắc dùng ảnh sản phẩm: mọi screenshot chứa ảnh AI phải kèm disclosure (hệ quả `SRS-FR-39`/`FR-40`) | Agent viết được |
| **BG-7** | **Nguyên tắc AI disclosure trong UI** | ⛔ Không phải mục brand truyền thống, nhưng ở dự án này **nó LÀ brand** (**B-2**). ⚠️ Đây là nghĩa vụ có **deadline ~01/03/2027** `[OFF]`, và `Glossary` cảnh báo ⛔ **đừng gộp** với *disclosure-first positioning* — cùng chữ, hai khái niệm | Agent viết ràng buộc; ⚠️ **phạm vi nghĩa vụ còn `TBD` chờ luật sư** |

#### 2.2 ⛔ Cắt khỏi brand book — và vì sao

Photography style · illustration system · motion/sonic branding · merchandising · brand architecture · co-branding · print spec.
Lý do chung: **C1** (1 người, ⛔ không ngân sách marketing) + **B-4** (sản phẩm sau đăng nhập). Mỗi mục trên đòi một tài sản phải **sản xuất và bảo trì** mà ⛔ không có surface nào tiêu thụ nó.

#### 2.3 Ba (bốn) thứ BẮT BUỘC anh quyết — agent ⛔ không quyết thay được

Khớp với `brief.md` **Q-B**, em xác nhận và **đề xuất thêm một câu thứ tư** vì nó rẻ khi hỏi cùng lúc và đắt khi hỏi muộn:

| | Câu hỏi | Vì sao agent không quyết được |
|---|---|---|
| **1** | **Tên hiển thị** | `comic-studio` là project name (`Charter` §1). Tên thương mại là quyết định kinh doanh + pháp lý, ⛔ không phải quyết định thiết kế |
| **2** | **Tone & personality** | Không có persona (`PRD` §3.3 `TBD-1/2`), ⛔ không có user interview nào (`docs/050-Research/User-Interviews/` **rỗng**). Agent chọn tone = agent bịa audience |
| **3** | **Hướng màu chủ đạo** | 0 căn cứ trong repo. Đây là chỗ ảo giác dễ trông có thẩm quyền nhất |
| **4** | ⭐ **Dark mode: light hay dark là default** | ⛔ Không phải câu hỏi thẩm mỹ — nó quyết định **hình dạng của mọi color token** ngay ở file đầu tiên. Xem [mục 6.2](#62-dark-mode). Hỏi sau = retrofit |

---

### 3. Design System chia thành mấy tài liệu

#### 3.1 Ràng buộc cứng đã tra bảng

| Ràng buộc | Giá trị | Neo |
|---|---|---|
| Thư mục đích | `docs/040-Design/Design-System/` | `Documents-Template.md` §Document Type Mapping, hàng **Design System** |
| Naming convention | `{Component}.md` | cùng nguồn |
| Nhóm 040-Design đăng ký | **đúng 4 loại**: Design System · Wireframe · User Flow · Prototype Spec — ⛔ **không có hàng Brand Guidelines** | cùng nguồn |
| Frontmatter bắt buộc | `id` · `type` · `status` · `created` | `Documents-Template.md` §Bản mẫu Frontmatter + §Validation Checklist |
| Tối thiểu Phase 3 | **Color Tokens · Typography · Spacing · Components** | trích yếu Phase 3 (PM cấp) |

⚠️ **Ghi chú về `{Component}.md`**: convention này cho thấy thư mục được thiết kế để cuối cùng chứa **một file / một component** (`Panel-Card.md`, `Bubble-Editor.md`…). Nhưng RULE-001 tự thừa nhận bảng này khớp theo **quy ước LỎNG** (changelog 2026-08-24: *"nó KHÔNG phải slug nghĩa đen… khớp theo quy ước LỎNG đã có sẵn"*, tiền lệ: hàng *User Story* ↔ `type: story`). ⇒ Tên kiểu `Typography.md` / `Foundations.md` nằm trong độ lỏng đã được chấp nhận. **Em nêu để PM biết, ⛔ không tự kết luận.**

#### 3.2 Đề xuất: **5 file** cho lô foundation

> ⭐ **Quyết định cắt scope quan trọng nhất của mục này**: run này viết **bộ nền**, ⛔ **KHÔNG** viết spec từng component. Lý do: chưa có **wireframe nào** (`docs/040-Design/Wireframes/` rỗng) và chưa có **persona** (`PRD` §3.3). Viết 12 spec per-component lúc này là viết tiểu thuyết — nó sẽ phải bỏ đi khi wireframe xuất hiện. Per-component `{Component}.md` thuộc **run sau**.

| # | Tên file | Nội dung chính (H1–H2) | Nguồn sự thật trong repo | Độ dài `[EM]` |
|---|---|---|---|---|
| **1** | `Foundations.md` | `# Foundations` · `## Hệ thống này quản cái gì / ⛔ KHÔNG quản cái gì` · `## Kiến trúc token (primitive → semantic)` · `## Hợp đồng phát biểu token` (CSS var ↔ Tailwind ↔ shadcn) · `## Chiến lược light/dark` · `## Chuẩn accessibility` · `## Cách kiểm` | `ADR-001` §Decision **5, 6** + bảng *Tầng MẶC ĐỊNH* · `Documents-Template.md` · ⚠️ a11y & dark mode: **repo không có nguồn** ⇒ là **đề xuất mới**, cần anh duyệt | ~150–250 dòng |
| **2** | `Color-Tokens.md` | `# Color Tokens` · `## Primitive palette` · `## Semantic mapping` (đủ **cặp `-foreground`**) · `## Bộ biến quy ước shadcn` · `## Giá trị dark` · `## Bảng audit contrast` · `## Màu trạng thái của hai human gate` | ⚠️ **chờ `BG-4`** (anh chốt hướng màu) · `ADR-001` *Tầng MẶC ĐỊNH* (shadcn/Tailwind) · trạng thái gate: `ADR-013` §Decision **9** | ~150–200 dòng |
| **3** | ⭐ `Typography.md` | `# Typography` · `## HAI hệ font — ⛔ không gộp` · `## Font UI` (thang cỡ, weight, token) · `## Font render — ⛔ TBD do ADR-013 sở hữu` (chỉ ghi **ràng buộc**) · `## Tiếng Việt: line-height & dấu chồng` · `## NFC/NFD` · `## Cỡ chữ bubble là HÀM của text_budget, ⛔ không phải giá trị chọn` | ⭐ `ADR-001` §Decision **điều 8** + §Consequences **#5** · `ADR-013` §Decision **6** + `TBD` hàng *"Font sẽ render"* · `Glossary` *typeset layer*, *`text_budget`* · `pm-runs/2026-08-23-danh-gia-y-tuong-comic-studio/findings/researcher.md` (line-height tiếng Việt) | **~250–350 dòng — dài nhất** |
| **4** | `Spacing-And-Layout.md` | `# Spacing & Layout` · `## Thang spacing` · `## Radius / border / elevation` · `## Breakpoint` · `## Z-index` · `## ⛔ Ranh giới: hệ này KHÔNG quản hình học panel/bubble` | `MVP-Scope` §4.1 (toạ độ **0–1**) · `SRS` §3.D ràng buộc **2** · `ADR-013` §Decision **2** | ~120–180 dòng |
| **5** | `Components.md` | `# Components` · `## Inventory theo 5 thành phần editor` · `## Ánh xạ shadcn/Radix: dùng nguyên / mở rộng / tự build` · `## Ma trận state` (default·hover·focus·active·disabled·loading·error·empty) · `## Ba pattern đặc thù sản phẩm` (polling 2s · human gate + **reset** · cảnh báo tốn tiền) | `MVP-Scope` §5.2 (**5 thành phần bắt buộc**) · `SRS` §3.D (`SRS-FR-10/12/14/16`, `SRS-NFR-06`, `SRS-NFR-23`) · `SRS-FR-21` variant picker · `ADR-001` *Tầng MẶC ĐỊNH* · `ADR-013` §Decision **9** (T1/T2 reset) | ~250–350 dòng |

**Lô writer**: `1+2+3` (lô A, nặng vì `Typography.md`) → `4+5` (lô B). Mỗi lô ≤ 3 file, ⛔ dưới trần 3–5.

**Phương án thay thế nếu PM muốn ánh xạ 1:1 tuyệt đối với 4 tối thiểu của Phase 3**: bỏ `Foundations.md`, đẩy hợp đồng token vào đầu `Color-Tokens.md` và a11y vào `Components.md`. ⛔ **Em không khuyến nghị**: nó nhét câu trả lời của [mục 4](#4-tầng-token-phải-phát-biểu-bằng-ngôn-ngữ-nào) — thứ áp cho **cả 4 file** — vào bên trong một file, và làm mất chỗ duy nhất phát biểu chuẩn a11y (⇒ tiêu chí gate ⛔ không kiểm cơ học được).

#### 3.3 Brand Guidelines đặt ở đâu — ý kiến chuyên môn (⚠️ anh chốt tại gate)

`brief.md` **Q-A** đã nêu hai đường. Em xếp hạng:

**⭐ Em đề xuất (a)** — map vào hàng `Design System` sẵn có ⇒ `docs/040-Design/Design-System/Brand-Guidelines.md`, ⛔ không sửa RULE-001.

Lý do **thiết kế** (không chỉ lý do quy trình): Brand Guidelines ở dự án này ⛔ **không phải một brand book độc lập** — nó là **tầng trên cùng của cùng một token graph**. Màu thương hiệu **chính là** nguồn của `--primary`; tone của voice **chính là** nguồn của microcopy trong `Components.md`. Tách sang category riêng tạo ra **hai nơi phải đồng bộ cho cùng một giá trị hex** — đúng thứ `docs/000-Index.md` mở đầu cảnh báo: *"copy là tạo ra hai bản phải đồng bộ"*. Với **1 người**, đặt cùng thư mục rẻ hơn về chi phí bảo trì.

**Điểm yếu của (a) — nêu thẳng**: `type:` trong frontmatter sẽ phải mang một giá trị lỏng, và `Brand-Guidelines` không thật sự là một `{Component}`.

**Điểm mạnh của (b)** (thêm hàng additive): RULE-001 đã có **hai tiền lệ additive** — *MVP Scope* (2026-08-23) và *Prioritized Backlog* (2026-08-24), cả hai đều vì đúng lý do này (quy tắc #7 chặn tạo tài liệu chưa tra được bảng). ⇒ (b) ⛔ **không** phải hành động ngoại lệ, và nó sạch hơn về mặt taxonomy.

⇒ **Chênh lệch nhỏ. Đây là quyết định của anh, ⛔ không phải của em.**

---

### 4. Tầng token phải phát biểu bằng ngôn ngữ nào

#### 4.1 Nền đã chốt

`ADR-001` §Decision **điều 5**: *"Frontend là SPA thuần, ⛔ không SSR, ⛔ không server action."*
`ADR-001` bảng *Tầng MẶC ĐỊNH*, hàng **Frontend & UI**: *"Vite + React + TypeScript, TanStack Query, **shadcn/ui + Tailwind CSS**… `shadcn/ui` (Radix Primitives) + Tailwind CSS quản lý toàn bộ UI Shell, Form (tích hợp Zod contracts), Modal, Review Gates; **component code nằm trực tiếp trong repo**, không vendor lock-in và **tối ưu cho AI assist (`R1`)**."*

#### 4.2 Trả lời: **CẢ HAI — nhưng một chiều phụ thuộc, ⛔ không đối xứng**

> **CSS variable theo quy ước shadcn là NGUỒN. Tailwind theme chỉ THAM CHIẾU vào nó.**

Năm lý do kỹ thuật, mỗi lý do đủ để chốt:

| # | Lý do |
|---|---|
| **1** | shadcn ⛔ **không phải một dependency** — ADR-001 ghi rõ *"component code nằm trực tiếp trong repo"*. Ta **sở hữu** file component, nên **phải sửa tay** mọi chỗ token không khớp. Token khớp sẵn = ⛔ không phải sửa gì |
| **2** | shadcn có một **tập biến ngữ nghĩa quy ước sẵn** mà component code đọc thẳng. Nếu Design System đặt tên riêng (`--brand-500`, `--surface-1`) rồi ⛔ không map, mọi component phải sửa tay ⇒ **mất đúng lợi thế mà ADR-001 mua nó về** (`R1` — 1 dev + AI assist) |
| **3** | Dark mode trong quy ước shadcn = **override CÙNG bộ biến dưới một selector**, ⛔ không phải một palette thứ hai. ⇒ ràng buộc hình dạng cho `Color-Tokens.md`: **mọi semantic token phải có đúng hai giá trị**; ⛔ không được tồn tại token chỉ có ở một mode |
| **4** | Tailwind là **tầng tiêu thụ**: `theme.extend` trỏ vào `var(--…)` để có `bg-primary`, `text-muted-foreground`. ⛔ **Cấm hardcode hex trong `tailwind.config`** — đó là nguồn sự thật thứ hai |
| **5** | SPA thuần ⛔ không SSR (điều 5) ⇒ ⛔ không có FOUC do server render sai theme, ⚠️ **nhưng** có flash nếu theme đọc `localStorage` **sau** paint. Cần một script chặn nhỏ trong `index.html`. Chi tiết nhỏ, nhưng writer sẽ quên nếu không ghi |

> ⚠️ **Ranh giới xác thực — bắt buộc đưa vào contract của writer Bước 5**: repo **chỉ chốt** *"dùng shadcn/ui + Tailwind"* (`ADR-001`). **Danh sách tên biến cụ thể là quy ước của thư viện, ⛔ KHÔNG phải nội dung repo này.** Writer **phải verify danh sách theo phiên bản shadcn thực tế** tại thời điểm khởi tạo repo, ⛔ **không chép từ trí nhớ**. Đây là chỗ ảo giác dễ lọt nhất của cả run.

#### 4.3 Năm cạm bẫy khi Design System viết kiểu Figma-first

| # | Bẫy | Hỏng thế nào khi map sang shadcn |
|---|---|---|
| **1** | **Đặt tên theo bảng màu, ⛔ không theo vai trò** (`Blue/500`, `Gray/900`) | shadcn cần token **ngữ nghĩa**. Dừng ở tầng primitive là dừng **đúng một tầng trước** chỗ code cần |
| **2** | ⭐ **Thiếu cặp `-foreground`** | Bẫy đặc trưng nhất của shadcn: mỗi nền có một chữ đi kèm. Figma style thường chỉ có fill. Thiếu cặp ⇒ **mọi contrast check phải làm lại tay ở từng chỗ dùng** |
| **3** | **Elevation bằng shadow tuỳ ý** | Figma cho mỗi layer một shadow riêng; Tailwind chỉ có thang cố định. 9 shadow khác nhau = 9 arbitrary value trong code |
| **4** | **Spacing ⛔ không rơi vào thang** | Auto-layout cho gap 13px; thang Tailwind 4px ⇒ `p-[13px]`. **Token chết ngay tại chỗ dùng** |
| **5** | ⭐ **Vẽ bubble/panel bằng pixel** | Layout là **toạ độ chuẩn hoá 0–1** trong `page_layout JSONB` (`MVP-Scope` §4.1 · `SRS` §3.D ràng buộc 2 · `ADR-013` §Decision 2). Design System ⛔ **không sở hữu** hình học panel/bubble — chỉ sở hữu **chrome của editor**. Nhầm chỗ này là sinh token spacing cho thứ ⛔ không được đo bằng spacing |

#### 4.4 Hệ quả lên hình dạng tài liệu

Vì **chưa có dòng code nào** (`F-4`), cách duy nhất để Design System không thành tài liệu chết là phát biểu nó dưới **đúng hình dạng file mà code sẽ có**:
- một block `:root {}` + `.dark {}` **copy-paste được** vào `apps/web/src/index.css`;
- một block `theme.extend` **copy-paste được** vào `tailwind.config.ts`.

⛔ **Không phải bảng hex trong markdown.** Đây là khác biệt giữa một Design System dùng được và một Design System được đọc một lần.

---

### 5. ⭐ HAI HỆ FONT — mục quan trọng nhất

#### 5.1 Nguyên văn ràng buộc

`ADR-001` §Decision **điều 8**:
> *"**Wrap tiếng Việt (`R3`) nằm CÙNG runtime với compositor.** Chuẩn hoá **NFC** ngay tại biên ingest; ngắt dòng theo **grapheme cluster + word boundary** bằng `Intl.Segmenter` (ECMA-402, ICU-backed, có sẵn trong Node LTS); ⛔ **không** được wrap ở frontend rồi gửi kết quả xuống, ⛔ **không** được wrap bằng font khác font sẽ render."*

`ADR-001` §Consequences **#5**: *"`Intl.Segmenter` giải quyết **ngắt**, KHÔNG giải quyết **đo**… Wrap đúng = *segmentation* **+** *đo bằng chính font sẽ render*."*

`ADR-013` §Decision **6** ghi lại nguyên ba ràng buộc đó và **⛔ không chọn lại**. `ADR-013` §Alternatives **(f)** LOẠI *"preview render client-side"*, dẫn đúng điều 8 làm căn cứ.

`ADR-013` bảng `TBD`, hàng **"Font sẽ render (họ font, glyph coverage tiếng Việt)"**: chủ là **Architect + Founder**, **sau MVP0**, **trước gate `G1-e`**. Lý do chưa đóng: rủi ro *"font không đủ glyph"* phải phát hiện **bằng kiểm thủ công**, vì ⛔ **không có benchmark định lượng nào**.

#### 5.2 Kết luận: **CÓ — bắt buộc tách. Và tách sâu hơn "hai mục trong một file"**

Hai thứ này thuộc **hai runtime, hai chủ, hai vòng đời quyết định** khác nhau:

| Chiều | **Font UI** | **Font render** |
|---|---|---|
| Chạy ở đâu | Browser, `apps/web` (SPA — `ADR-001` điều 5) | Node, **cùng runtime compositor** (`ADR-001` điều 8) |
| Ai nhìn thấy | Tác giả, trong lúc biên tập | ⭐ **Người đọc cuối**, trong sản phẩm giao đi |
| Đo bằng gì | Browser tự đo; ⛔ không ai phụ thuộc số đo đó | Compositor **phải tự đo** để wrap (`ADR-001` §Consequences #5) |
| Sai thì sao | Chữ xấu — sửa bằng **một dòng CSS** | ⭐ **Hỏng sản phẩm.** `ADR-001` §Context `R3` nguyên văn: *"wrap sai dấu tiếng Việt là **hỏng sản phẩm**, không phải lỗi cosmetic"* |
| Đổi được không | Bất cứ lúc nào, chi phí ~0 | Đổi = **wrap lại toàn bộ**; mọi bubble đã duyệt phải **đo lại** |
| **Ai chốt** | Product Designer đề xuất → **anh duyệt**, trong phạm vi run này | ⛔ **Architect + Founder, sau MVP0** — `ADR-013` `TBD`. ⛔ **RUN NÀY KHÔNG ĐƯỢC CHỐT** |
| Rủi ro riêng | — | **glyph coverage tiếng Việt** — phát hiện **thủ công**, ⛔ không có benchmark |

#### 5.3 Sáu hệ quả lên Design System

| # | Hệ quả |
|---|---|
| **H-1** | `Typography.md` phải có **hai mục cấp 2 tách hẳn**, và mục *Font render* mở bằng callout ⛔ *"đây là `TBD` do `ADR-013` sở hữu; mục này ghi **RÀNG BUỘC**, ⛔ không chọn font"*. ⭐ Đây **đúng khuôn** mà `ADR-013` đã dùng cho `D-30` (*"⛔ không chọn lại thư viện ở đây — xem ADR-001 điều 8"*). Em đề xuất Design System **kế thừa nguyên khuôn đó** vì nó đã chạy đúng một lần trong repo này |
| **H-2** | ⭐ **Token hai hệ ⛔ KHÔNG được chung namespace.** Font UI là CSS variable (`--font-sans`…) tiêu thụ bởi Tailwind. Font render ⛔ **không phải CSS variable** — nó là **tham số cấu hình của compositor server-side**, sống ở config của `apps/api`, ⛔ không sống ở `apps/web`. Nhét nó vào Tailwind theme là **mời một dev tương lai render bubble ở client** — đường đã bị `ADR-013` §Alternatives **(f)** LOẠI tường minh |
| **H-3** | **Type scale của UI ⛔ không áp cho bubble.** Cỡ chữ bubble là **hàm của `text_budget`** — mà `text_budget` *"tính từ diện tích panel"* và là **field của panel spec**, ⛔ không nằm ở tầng typeset (`Glossary` *`text_budget`* · `SRS-FR-13` · `ADR-012` `D-25`). ⇒ Design System phát biểu **QUY TẮC**, ⛔ không phát biểu **GIÁ TRỊ** |
| **H-4** | **Line-height tiếng Việt là mục riêng, và áp cho CẢ HAI hệ.** Căn cứ duy nhất repo có: `pm-runs/2026-08-23-danh-gia-y-tuong-comic-studio/findings/researcher.md` — *"line-height phải rộng hơn tiếng Anh vì dấu chồng ('ữ', 'ế') ăn không gian phía trên"*. ⚠️ Đây là **findings của run trước, ⛔ KHÔNG phải requirement đã chốt** — phải mang đúng nhãn đó. Nó áp cả cho UI (form Story Bible đầy tên nhân vật có dấu), ⛔ không chỉ cho bubble |
| **H-5** | **NFC là ràng buộc của biên ingest, ⛔ không phải của Design System** — nhưng `Typography.md` **phải nhắc**, vì đây là chỗ designer vô tình phá: dán một chuỗi mẫu **NFD** làm ví dụ, rồi dev copy nguyên vào test fixture. `ADR-001` §Consequences #5 đòi nghiệm thu **cả NFC và NFD cho ra CÙNG kết quả ngắt dòng** |
| **H-6** | ⚠️ **Preview ⛔ không phải một component của Design System.** `MVP-Scope` §5.2 thành phần **#4** là *"Preview trang + chapter render **server-side**, read-only"* — nó là **một tấm ảnh server trả về**. Design System sở hữu **khung bao quanh** (toolbar, zoom, trạng thái loading khi polling 2s — `SRS-NFR-06`), ⛔ **không sở hữu nội dung bên trong**. ⚠️ Giữ đúng ranh giới tinh vi của `ADR-013` §Alternatives (f): **ĐƯỢC PHÉP** hiển thị bubble trong editor ở client (thành phần **#2**, phạm vi **một panel**, là **lớp tương tác**) — **KHÁC** preview trang/chapter (thành phần **#4**). ⛔ Hai thứ khác nhau, không gộp |

#### 5.4 Gộp làm một thì hỏng gì — bốn đường, mỗi đường đủ để chốt

| # | Đường hỏng |
|---|---|
| **(a)** | ⭐ **Hỏng IM LẶNG, ⛔ không lỗi nào nổi lên.** Nếu `Typography.md` chỉ có một hệ font, cách tự nhiên nhất để dùng nó là đặt font đó vào CSS rồi render bubble ở client cho nhanh — đúng phương án **(f)** đã bị LOẠI. Và **nó chạy được**, chỉ khác kết quả với export. Người dùng duyệt trên preview rồi nhận file khác: `ADR-013` §Alternatives **(e)** lý do 1 gọi đây là *"lỗi **không phát hiện được** cho tới khi khách hàng phàn nàn"* |
| **(b)** | **Vi phạm trực tiếp hai lệnh cấm nguyên văn** của `ADR-001` điều 8. Một font chung nghĩa là webfont browser phải bằng font file server-side — mà hai thứ đó ⛔ **không bao giờ đảm bảo cùng metric** (fallback, hinting, subset) |
| **(c)** | **Đóng hộ một `TBD` có chủ.** `ADR-013` giao font render cho **Architect + Founder, sau MVP0**. Viết một tên font vào ô đó là đóng **thay người khác** và đóng **trước khi có số đo** — đúng thứ `ADR-001` từ chối làm với thư viện compositor: *"⛔ không dán tên kèm con số khi chưa đo"* |
| **(d)** | **Mất chỗ ghi rủi ro glyph coverage.** Rủi ro này chỉ áp cho font render và ⛔ **không có benchmark định lượng**. Gộp hai hệ ⇒ rủi ro hoặc bị áp nhầm lên font UI (vô nghĩa — browser có fallback), hoặc **biến mất khỏi tài liệu** |

---

### 6. Accessibility & dark mode

#### 6.0 ⛔ Trạng thái repo — nói thẳng trước khi đề xuất

Em đã grep toàn `docs/` với `WCAG|accessibility|a11y|dark mode|contrast|tương phản|responsive|mobile|logo`. Kết quả:

| Từ khoá | Hit | Thực chất |
|---|:--:|---|
| `WCAG` · `accessibility` · `a11y` · `dark mode` · `logo` | **0** | ⛔ **Không tồn tại trong repo** |
| `tương phản` | 3 | ⛔ **Không phải contrast màu** — là *tương phản nhịp kể chuyện* (`Analysis` §5.3 emphasis quota) |
| `mobile` | 1 | `Analysis-Market` §5.2 — RevenueCat đo *mobile subscription app*, là metric retention, ⛔ không phải yêu cầu responsive |

Đối chiếu: `SRS` có **17 NFR có số + 14 NFR `TBD`** (`docs/000-Index.md`) — ⛔ **không NFR nào về usability/a11y**. Và `PRD` §3.3 hệ quả **#2** phát biểu thẳng: *"Acceptance Criteria **không có ngưỡng usability do người ngoài đặt**. Mọi ngưỡng UX trong tầng này là ngưỡng **tự đặt**, phải mang nhãn `[EM]`."*

⇒ ⛔ **Repo KHÔNG có requirement nào về a11y hay dark mode.** Mọi thứ dưới đây là **đề xuất MỚI**, cần anh duyệt tại gate, và ⛔ **không được viết như thể đã có yêu cầu**.

#### 6.1 A11y — đề xuất **WCAG 2.2 Level AA**, có giới hạn phạm vi `[EM]`

Ba lý do chọn **AA** (⛔ không A, ⛔ không AAA) cho sản phẩm **1 người**:

| # | Lý do |
|---|---|
| **1** | ⭐ **AA là mức công cụ tự động kiểm được phần lớn** — contrast ratio, accessible name, focus visible, target size. Với **1 dev ⛔ không code review** (`ADR-001` `R1`), thứ duy nhất chạy được đều đặn là **kiểm tự động**. AAA đòi phán đoán người (7:1, ⛔ ít ngoại lệ) ⇒ chi phí **thường trực**, ⛔ không trả nổi |
| **2** | **AA là mức shadcn/Radix đã đỡ sẵn phần đắt nhất** — focus trap, roving tabindex, ARIA của dialog/popover/select. `ADR-001` mua shadcn về **chính vì** *"tối ưu cho AI assist (`R1`)"*. Chọn AA = **tiêu thụ cái đã trả tiền**; chọn AAA = tự viết lại phần Radix không cover |
| **3** | ⚠️ **⛔ Không có nghĩa vụ pháp lý nào trong repo bắt a11y.** Bốn nghĩa vụ đã biết (NĐ 134/2026 Điều 5a · Điều 37b opt-out · Điều 198b safe harbour · Luật TTNT 2025 Điều 11) đều ⛔ không động tới accessibility ⇒ AA là lựa chọn **kỹ thuật**, ⛔ **không phải tuân thủ**. Nói rõ để ⛔ không ai tưởng có deadline |

**Giới hạn phạm vi bắt buộc phải ghi** ⭐: sản phẩm này có một bề mặt mà a11y ⛔ **không cứu được** — **bản thân trang truyện**. Art là ảnh model sinh; thành phẩm là ảnh sau composite. Screen reader ⛔ không đọc được. **Nhưng** repo **đã có sẵn** dữ liệu để làm điều gần nhất: `dialogue_source` là **string bất biến** và `dialogue_rendered` là string người sửa được (`ADR-013` §Decision **5**). ⇒ **Text alternative cho page là dữ liệu ĐÃ CÓ, ⛔ không phải công việc mới.** Ghi vào `Foundations.md` như một **cơ hội**, ⛔ **không phải requirement** — vì ⛔ chưa ai yêu cầu.

⭐ **Một chỗ AA đụng thẳng vào một requirement CHỐT — đáng đưa lên gate**: `SRS-FR-16` chốt *"heuristic **+** cho user **kéo tay**"*, và `MVP-Scope` §5.2 thành phần **#2** liệt kê *kéo bubble, kéo đuôi trỏ*. WCAG 2.2 **SC 2.5.7 (Dragging Movements)** đòi **có đường thay thế không-kéo** (ví dụ: nút nudge, hoặc nhập toạ độ). ⇒ Đây ⛔ không phải một dòng CSS — **nó sinh ra UI thật và effort thật**. PM nên đưa vào gate như một hệ quả scope, ⛔ không để nó lộ ra ở Bước 5.

Các ngưỡng cụ thể (contrast 4.5:1 / 3:1, target ≥24×24 CSS px…) thuộc nội dung `Foundations.md`, ⛔ em không viết ở đây — nhưng **tất cả phải mang `[EM]`** theo `PRD` §3.3.

#### 6.2 Dark mode

⛔ **Repo không có requirement nào. Em ⛔ không suy diễn thành "đã yêu cầu".**

Ba dữ kiện thật để anh quyết:

| # | Dữ kiện |
|---|---|
| **1** | ⭐ **shadcn làm dark mode gần như miễn phí NẾU quyết từ đầu, và đắt nếu retrofit** — vì quy ước là override **cùng bộ biến**. Retrofit = đi tìm mọi hex đã lỡ hardcode. Đây **đúng dạng bất đối xứng** mà `MVP-Scope` §2 **NT-3** dùng để quyết `KC-1`/`KC-5`: *"rẻ khi làm từ đầu, không thể sửa về sau"* ⇒ **định nghĩa cả hai bộ giá trị token ngay từ đầu**; còn **switcher UI** thì hoãn được |
| **2** | ⚠️ **Có một lập luận NGƯỢC, và ở sản phẩm này nó mạnh hơn**: bề mặt trung tâm của editor là **ảnh comic** và **preview trang in 300 DPI** — trang thành phẩm có nền **trắng giấy**. Đặt trang trắng lên chrome tối làm **lệch cảm nhận độ sáng/tương phản của chính tấm ảnh người dùng đang duyệt** — mà họ đang duyệt để trả lời ***"trang này đọc có ổn không?"*** (`PRD` §3.3 — proxy *"đủ tốt"* **duy nhất** repo có). ⇒ Em đề xuất **vùng preview/canvas giữ nền trung tính CỐ ĐỊNH ở cả hai mode**; chrome đổi theo mode |
| **3** | ⛔ **Em KHÔNG dùng lập luận *"editor ảnh dùng lâu nên phải dark"***. Repo ⛔ không có dữ liệu thời lượng phiên nào, ⛔ không có persona (`PRD` §3.3 `TBD-1`), ⛔ không có user interview nào (`docs/050-Research/User-Interviews/` **rỗng**). Nó là câu **nghe hợp lý mà không có căn cứ** — đúng loại suy diễn `PRD` §3.3 cảnh báo |

**Đề xuất chốt (⚠️ toàn bộ `[EM]`)**: token **hai bộ giá trị từ đầu** + **light là default** + **vùng preview trung tính cố định** + **switcher hoãn**. Ba trong bốn cái này rẻ khi làm từ đầu và đắt khi retrofit ⇒ nên hỏi anh **cùng lúc với `BG-4`** (xem [mục 2.3 câu 4](#23-ba-bốn-thứ-bắt-buộc-anh-quyết--agent--không-quyết-thay-được)).

---

### 7. Thuật ngữ Glossary chưa có, đáng bổ sung

`Glossary.md` có **69 thuật ngữ / 10 nhóm**. Nhóm ***Chữ & trình bày*** có 5 mục: `typeset layer` · `text_safe_zone` · `dialogue condensation` · `speaker attribution` · `text_budget`.
⛔ **Không có một thuật ngữ design system nào.** Em đã verify bằng grep: `grapheme` / `NFC` / `NFD` / `Unicode combining` / `design token` / `font` — **0 hit** (hit duy nhất của *"token"* là token LLM ở mục `HITL gate`).

Đề xuất bổ sung (⛔ **run này không viết Glossary** — đây là kiến nghị cho PM):

| Ưu tiên | Thuật ngữ | Vì sao |
|---|---|---|
| ⭐⭐ | **font UI vs font render** | Cặp **dễ gộp nhầm nhất, hậu quả nặng nhất** ([mục 5](#5--hai-hệ-font--mục-quan-trọng-nhất)). Glossary **đã có tiền lệ** dùng headword để **chống nhầm**: `hard quota` tồn tại để chống nhầm với `credit ledger + hold`; `HITL gate` vs `human gate` |
| ⭐⭐ | **grapheme cluster** · **NFC / NFD** | `ADR-001` điều 8 dùng cả ba làm ràng buộc CHỐT, mà Glossary ⛔ chưa định nghĩa cái nào |
| ⭐ | **design token** (+ phân biệt **primitive** vs **semantic**) | Xuất hiện khắp 5 file Design System |
| ⭐ | **semantic color pair (`-foreground`)** | Quy ước shadcn; là bẫy #2 ở [mục 4.3](#43-năm-cạm-bẫy-khi-design-system-viết-kiểu-figma-first) |
| — | **WCAG AA** · **dark mode token override** | Chỉ bổ sung **sau khi** anh duyệt hai đề xuất ở [mục 6](#6-accessibility--dark-mode) |

---

### 8. Ba việc em đề nghị PM đưa lên gate

| # | Việc | Vì sao không giải được ở tầng worker |
|---|---|---|
| **G-1** | **`BG-2` tên hiển thị · `BG-3` tone · `BG-4` hướng màu · + dark-mode default** | Quyết định của anh. Agent quyết thay = bịa audience/brand — vi phạm `ANTI-HALLUCINATION` và `PRD` §3.3 |
| **G-2** | **Vị trí của Brand Guidelines** (`brief.md` **Q-A**) | Chặn Bước 5: quy tắc **#7** của RULE-001 cấm tạo tài liệu chưa tra được bảng. Em đã xếp hạng ở [3.3](#33-brand-guidelines-đặt-ở-đâu--ý-kiến-chuyên-môn-anh-chốt-tại-gate), ⛔ không chốt |
| **G-3** | ⭐ **WCAG 2.2 SC 2.5.7 sinh ra UI thật** — cần đường thay thế không-kéo cho *kéo bubble / kéo đuôi trỏ* (`SRS-FR-16` · `MVP-Scope` §5.2 #2) | Đây là **hệ quả scope**, ⛔ không phải chi tiết thiết kế. Để lộ ra ở Bước 5 là muộn |

### 9. Ba lằn ranh em đề nghị ghi thẳng vào contract của writer (Bước 5)

1. ⛔ **Writer KHÔNG được chọn font render** — `ADR-013` `TBD` có chủ (**Architect + Founder, sau MVP0**). Chỉ được **ghi lại ràng buộc**.
2. ⛔ **Writer KHÔNG được chép danh sách biến shadcn từ trí nhớ** — phải verify theo phiên bản thực tế (xem callout [4.2](#42-trả-lời-cả-hai--nhưng-một-chiều-phụ-thuộc--không-đối-xứng)).
3. ⛔ **Mọi ngưỡng UX phải mang nhãn `[EM]`** — `PRD` §3.3 hệ quả #2. ⛔ Không con số UX nào trong repo là số đo.
