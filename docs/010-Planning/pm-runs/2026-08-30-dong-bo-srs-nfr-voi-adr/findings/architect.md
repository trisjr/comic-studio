---
id: FINDINGS-ARCHITECT-2026-08-30
type: findings
role: architect
run: 2026-08-30-dong-bo-srs-nfr-voi-adr
status: done
mode: READ-ONLY (khảo sát — ⛔ em không sửa file nào ngoài file này)
created: 2026-08-30
---

# 🏗️ Findings — Architect · Đồng bộ lệch tầng `SRS` (020) ↔ `ADR` (030)

## Mục lục

- [0. Bối cảnh bắt buộc đọc trước](#0-bối-cảnh-bắt-buộc-đọc-trước)
- [1. Bảng ánh xạ — ADR nào đóng requirement `TBD` nào](#1-bảng-ánh-xạ--adr-nào-đóng-requirement-tbd-nào)
- [2. Danh sách chính xác mọi dòng phải sửa ở tầng 020](#2-danh-sách-chính-xác-mọi-dòng-phải-sửa-ở-tầng-020)
- [3. Ripple — tầng 030 viện dẫn `SRS-NFR-09` còn `TBD`](#3-ripple--tầng-030-viện-dẫn-srs-nfr-09-còn-tbd)
- [4. `ADR-001` có mâu thuẫn nội tại không](#4-adr-001-có-mâu-thuẫn-nội-tại-không)
- [5. Vấn đề phát hiện thêm — report-only](#5-vấn-đề-phát-hiện-thêm--report-only)
- [6. Tài liệu tham khảo](#6-tài-liệu-tham-khảo)

---

## 0. Bối cảnh bắt buộc đọc trước

> [!IMPORTANT]
> **Kết luận của em dựa trên bản `ADR-001` CHƯA COMMIT trong worktree này.**
> Đã verify: `grep -c shadcn docs/030-Specs/Architecture/ADR-001-Backend-And-Frontend-Tech-Stack.md` → **`2`** (hàng *Frontend & UI* ở `ADR-001:58` và một dòng ở `## Consequences` `ADR-001:117`). ⇒ Bản em đọc là bản Founder đã sửa, PM đã đồng bộ. Nếu bản commit cuối khác bản này, ⛔ **mọi kết luận về `SRS-NFR-09` phải đọc lại**.

> [!WARNING]
> **Bốn ADR đều đang `status: draft`** (`ADR-001:4`, `ADR-002:4`, `ADR-003:4`, `ADR-004:4`).
> Đây là câu hỏi **governance PM phải quyết trước khi land**: đóng một hàng requirement tầng 020 bằng một ADR còn `draft` có hợp lệ không? Repo đã có tiền lệ dùng `draft` làm mốc chặn — `ADR-010:176` viết *"Khi `ADR-003` chuyển khỏi `draft` — trước MVP1"*. ⛔ Em **không tự quyết**; xem [§5 mục 5.1](#51-bốn-adr-còn-draft--câu-hỏi-governance-chặn).

**Đã đọc và tôn trọng**: `docs/010-Planning/pm-runs/2026-08-28-phase-2-architecture-design-comic-studio/escalations.md:184` — 4 bảng của `ADR-001…004` **cố ý** dùng header `| Quyết định | Mã | Nguồn |` vì cột 2 chứa `SRS-NFR-*` chứ ⛔ không phải `D-xx`. ⛔ Em **không đề xuất sửa** header đó, và §4 dưới đây dựa trực tiếp vào chính ghi chú này.

**Hai điều PM đã xác định — em verify lại và XÁC NHẬN ĐÚNG, ⛔ không bác**:
1. `ADR-001:168` có heading `### ADR này quyết (phần Phase 1 **cố ý** để mở)`; hàng đầu tiên của bảng là `ADR-001:172` = `SRS-NFR-09`. ✅ Đúng.
2. `SRS` còn hai hàng `CHƯA QUYẾT` cùng họ: `SRS-NFR-07` (`SRS:256`) và `SRS-NFR-08` (`SRS:257`). ✅ Đúng — và **cả hai đều đã được ADR nhận việc**.

**Quét toàn bộ 19 file `docs/030-Specs/Architecture/`**: chỉ **ĐÚNG BỐN** file có heading `### ADR này quyết (phần Phase 1 cố ý để mở)` — `ADR-001:168`, `ADR-002:185`, `ADR-003:169`, `ADR-004:167`. ⛔ Không có ADR thứ năm nào đóng một hàng `CHƯA QUYẾT` của `SRS`. (`ADR-015:15` có cụm chữ *"ADR này quyết"* nhưng nằm trong câu văn, ⛔ không phải heading, và nó tuyên bố ngược lại: *"`N` của `in_flight_per_tenant` là `TBD` — ⛔ không con số nào trong repo"* ⇒ **⛔ không đóng** `SRS-FR-26`.)

---

## 1. Bảng ánh xạ — ADR nào đóng requirement `TBD` nào

### 1.1 Định nghĩa trọng tài (nguồn: `SRS:50`)

Nguyên văn `SRS-Comic-Studio.md:50`:

> `| **Mức độ rắn** | **Độ cứng của quyết định** | **CHỐT** đã quyết, không mở lại · **MẶC ĐỊNH** đã chọn nhưng có đường lui ghi rõ · **CHƯA QUYẾT** → phải ghi `TBD` |`

⭐ **Trục của cả lô**: có **đường lui ghi rõ** ⇒ là **MẶC ĐỊNH**, ⛔ **KHÔNG** phải **CHỐT**. Đây chính là chỗ dễ đóng nhầm.

### 1.2 Bảng ánh xạ

| ADR | Mục *"ADR này quyết"* có tồn tại? | Requirement nó tuyên bố đóng | **Thực sự đã CHỐT hay chưa?** | Bằng chứng (`file:line`) |
|---|---|---|---|---|
| **`ADR-001`** Tech stack BE/FE | ✅ Có — `ADR-001:168` | `SRS-NFR-09` (*Ngôn ngữ / framework backend & frontend, ORM & migration tool*) | ⭐ **LAI, ⛔ KHÔNG phải CHỐT thuần.** Ba tầng cùng tồn tại trong một ADR: **CHỐT** (8 điều) + **MẶC ĐỊNH** (5 hàng, đường lui ghi rõ) + **`TBD`** (4 hàng vẫn mở) | `ADR-001:168`, `:170-172`; tầng CHỐT `:41-50`; tầng MẶC ĐỊNH `:52-60`; tầng `TBD` `:62-69`; đường lui `:130-136`; ba dòng CHỐT không đường lui `:138` |
| **`ADR-002`** Hosting & Region | ✅ Có — `ADR-002:185` | `SRS-NFR-07` (*Hosting / PaaS / container platform / region*) | ⭐ **LAI, nghiêng MẶC ĐỊNH.** Mô hình triển khai **CHỐT** (6 điều); **platform + region cụ thể là MẶC ĐỊNH** (Render · Singapore) kèm thang đường lui 3 bậc **và** điều kiện *"phải verify trước khi mua"*. ⚠️ Còn một **reopen trigger ghi trước** | `ADR-002:185`, `:189`; tầng CHỐT `:43-58`; tầng MẶC ĐỊNH `:60-75`; cảnh báo verify `:64-65`; thang đường lui `:69-73`; reopen trigger `:82`, `:86` |
| **`ADR-003`** Auth & Billing vendor | ✅ Có — `ADR-003:169` | `SRS-NFR-08` — **phần auth + billing** (phần object storage đẩy sang `ADR-004`, tuyên bố ở `ADR-003:19`) | ⭐ **ĐÓNG MỘT NỬA.** Seam (8 điều) **CHỐT**; **auth vendor = MẶC ĐỊNH (Clerk)** + thang đường lui + 3 tiêu chí spike. ⛔ **Billing vendor VẪN `CHƯA QUYẾT` → `TBD`**, có chủ đích, vì ràng buộc chặn **ngoài kỹ thuật** (quốc gia pháp nhân bán hàng) | `ADR-003:169`, `:173-175`; seam CHỐT `:45-55`; MẶC ĐỊNH auth `:57-66`; ⭐ **`TBD` billing `:71-79`**; hàng tự khai *"ở lại `TBD` có chủ đích"* `:175` |
| **`ADR-004`** Object Storage & Signed URL | ✅ Có — `ADR-004:167` | `SRS-NFR-08` — **phần object storage** | ⭐ **LAI.** Chiến lược phát hành signed URL (9 điều) **CHỐT**; **vendor = MẶC ĐỊNH (Cloudflare R2)** + thang đường lui + 4 điều phải verify trước khi mua. ⛔ **Con số TTL vẫn `TBD`** (nhưng đó là hàng `§5.2` của `SRS`, ⛔ không phải `SRS-NFR-08`) | `ADR-004:167`, `:171-172`; MẶC ĐỊNH vendor `:66-72`; verify `:74-75`; `TBD` TTL `:77-89` |
| `ADR-005`…`ADR-018`, `SDD` | ⛔ Không có mục này | — | ⛔ **Không ADR nào khác đóng một hàng `CHƯA QUYẾT` của `SRS`** | `grep -rn "ADR này quyết" docs/030-Specs/Architecture/` → chỉ 4 kết quả heading + 1 kết quả trong câu văn (`ADR-015:15`) |

### 1.3 ⭐ Ba dòng **CHỐT không đường lui** của `ADR-001`

Nguyên văn `ADR-001:138`:

> `⛔ Ba dòng **CHỐT** (một ngôn ngữ TypeScript · SQL thô là nguồn sự thật schema · API là hợp đồng duy nhất) **không có đường lui** — đổi chúng là viết ADR mới thay thế ADR này.`

Ba dòng đó, truy ngược về `## Decision`:

| # | Dòng CHỐT không đường lui | Neo |
|:--:|---|---|
| 1 | **Một ngôn ngữ duy nhất cho API, worker và frontend: TypeScript trên Node.js LTS** | `ADR-001:43` (điều 1) |
| 2 | **Migration là file SQL thô, đánh số, append-only — và nó là NGUỒN SỰ THẬT của schema** | `ADR-001:45` (điều 3) |
| 3 | **Frontend là SPA thuần; API là hợp đồng DUY NHẤT giữa web và dữ liệu** | `ADR-001:47` (điều 5) |

### 1.4 ⭐ Vì sao `SRS-NFR-09` ⛔ KHÔNG được ghi thành **CHỐT** thuần

`ADR-001` **tự phân tầng** đúng ba mức của `SRS:50`:

| Tầng trong `ADR-001` | Nội dung | Ánh xạ sang `SRS:50` |
|---|---|---|
| `ADR-001:41-50` — *"Tầng CHỐT — bất biến kiến trúc"* | 8 điều; **3 điều không đường lui** (`:138`) | **CHỐT** |
| `ADR-001:52-60` — *"Tầng MẶC ĐỊNH — đã chọn, đường lui ghi rõ ở `## Consequences`"* | NestJS · Drizzle trên `node-postgres` · Vite+React+TS+TanStack Query+**shadcn/ui+Tailwind** · pnpm workspace · ESLint boundary rule | **MẶC ĐỊNH** — chính tiêu đề mục đã tự khai |
| `ADR-001:62-69` — *"`TBD` — chưa có căn cứ, ⛔ không tự gán"* | (a) thư viện compositor + sinh PDF · (b) **pin phiên bản Node LTS** · (c) compositor trong `worker_threads` hay tách job · (d) i18n + observability (**tuyên bố ⛔ KHÔNG đóng**) | **CHƯA QUYẾT** → `TBD` |

⇒ **Kết luận trọng tài**: `SRS-NFR-09` sau `ADR-001` là một hàng **LAI**, ⛔ không phải CHỐT, và cũng ⛔ không phải MẶC ĐỊNH thuần — vì **hai** hạng mục nằm **trong chính phạm vi phát biểu của `SRS-NFR-09`** (*"ngôn ngữ / framework"*) vẫn mở: **`(b)` pin phiên bản Node LTS** là tham số của *"ngôn ngữ"*, **`(a)` thư viện compositor + sinh PDF** là tham số của *"framework backend"*.

Đây đúng **mẫu hình LAI** mà `SRS:58-60` đã định nghĩa sẵn: *"cơ chế đã khẳng định, `TBD` chỉ áp cho tham số"*.

---

## 2. Danh sách chính xác mọi dòng phải sửa ở tầng 020

> [!NOTE]
> **Cách đọc bảng**: cột *Nguyên văn hiện tại* là chuỗi **cắt gọn nhưng nguyên trạng** đủ để PM `grep` ra. ⛔ Em không viết lại toàn bộ ô bảng dài — PM sửa **mệnh đề lý do**, giữ nguyên phần còn lại.
> **File duy nhất phải sửa ở tầng 020**: `docs/020-Requirements/SRS-Comic-Studio.md`. ✅ Đã grep `PRD-Comic-Studio.md` — ⛔ **không có** dòng nào nói framework/ngôn ngữ/vendor/hosting chưa quyết (`PRD:296` chỉ nói *"Mua auth + billing, không tự viết"*, ⛔ không gắn `TBD` vendor). ✅ Đã kiểm **Mục lục** `SRS:19-25` — chỉ có 7 mục cấp 1, ⛔ **không cần sửa**.

### 2.A — Nhóm BẮT BUỘC nếu chỉ đồng bộ `SRS-NFR-09` (yêu cầu gốc của anh)

| # | `file:line` | Nguyên văn hiện tại (trích nguyên trạng) | Nội dung đề xuất | Lý do |
|:--:|---|---|---|---|
| **A1** | `SRS-Comic-Studio.md:149` | `\| Ngôn ngữ / framework backend & frontend \| `TBD` \| `SRS-NFR-09` \|` | `\| Ngôn ngữ / framework backend & frontend \| **TypeScript trên Node.js LTS** (CHỐT) · NestJS · Drizzle trên `node-postgres` · Vite + React + TS + TanStack Query + shadcn/ui + Tailwind (MẶC ĐỊNH, đường lui ghi rõ) — [ADR-001] \| `SRS-NFR-09` \|` | Bảng §2.3 *Operating Environment* đang tóm tắt trạng thái đã quyết. `ADR-001:43`, `:52-60` đã quyết. ⚠️ **Việc tạo link** phụ thuộc quyết định ở **A8** |
| **A2** | `SRS-Comic-Studio.md:258` | `\| **SRS-NFR-09** \| Ngôn ngữ / framework backend & frontend \| Không anchor được. `CF-1.3` `[OFF]`: *"chưa có dòng nào"* — `src/`, `test/`, `openspec/changes/` đều rỗng \| **CHƯA QUYẾT** → `TBD` \|` | Cột 3 → `**ADR-001** (tầng 030) — viết khi `src/`/`test/` còn rỗng, tức tại thời điểm chi phí đảo ngược thấp nhất`. Cột 4 → `**LAI** — **CHỐT**: một ngôn ngữ **TypeScript/Node.js LTS** · SQL thô là nguồn sự thật schema · API là hợp đồng duy nhất (⛔ ba dòng này **không có đường lui**) · **MẶC ĐỊNH**: NestJS, Drizzle, Vite+React+TanStack Query+shadcn/ui+Tailwind — đường lui ghi rõ ở `ADR-001` §*Đường lui* · **CHƯA QUYẾT** → `TBD`: **phiên bản Node LTS pin cụ thể** và **thư viện compositor + sinh PDF**` | ⭐ Hàng chi tiết — trục chính. Cột 4 **phải copy nguyên trạng cả phần mô tả đường lui** vì `SRS:163` quy định *"đường lui là **một phần của nhãn**"* |
| **A3** | `SRS-Comic-Studio.md:460` | `…Ảnh hưởng font / collation / full-text-search config — phụ thuộc ngôn ngữ & framework còn `TBD` (`SRS-NFR-09`) \| `SRS-FR-16`, `SRS-NFR-09` \|` | Đổi mệnh đề cuối cột 2 thành: `…Ảnh hưởng font / collation / full-text-search config. ⚠️ **`ADR-001` (đóng `SRS-NFR-09`) tuyên bố tường minh ⛔ KHÔNG đóng hàng này**: *"`D-30` là một FR về typesetting, ⛔ không phải NFR ngôn ngữ"*. Ai đóng: **Dev đề xuất, Founder duyệt** · Khi nào: **sau khi stack được dựng, trước MVP1**` | ⭐ **Hàng vẫn `TBD`, nhưng LÝ DO SAI.** Mệnh đề *"phụ thuộc `SRS-NFR-09` còn `TBD`"* ⛔ không còn đúng. Nguồn thay thế: `ADR-001:69` |
| **A4** | `SRS-Comic-Studio.md:461` | `…stack telemetry phụ thuộc hosting (`SRS-NFR-07`) và framework (`SRS-NFR-09`) còn `TBD` \| `SRS-NFR-20`, `SRS-FR-25`, `SRS-NFR-09` \|` | Đổi mệnh đề cuối cột 2 thành: `…⚠️ **Cả `ADR-001` lẫn `ADR-002` đều tuyên bố tường minh ⛔ KHÔNG đóng hàng này** — chọn ngôn ngữ/framework và chọn platform ⛔ không tương đương với việc phát biểu observability thành một hạng mục. Ai đóng: **Dev** · Khi nào: **sau khi platform được mua và MVP0 có số đo**` | ⭐ Cùng lỗi như A3. Nguồn thay thế: `ADR-001:69` **và** `ADR-002:84`. ⚠️ Lưu ý ripple ngược: `SDD-Comic-Studio.md:457` đang **trích** hàng này — xem [§3 hàng R6](#3-ripple--tầng-030-viện-dẫn-srs-nfr-09-còn-tbd) |
| **A5** | `SRS-Comic-Studio.md:345` | `Phân bố theo mức độ rắn (`findings/architect.md §2.8`): **CHỐT** thuần **55** · **MẶC ĐỊNH** **6** (thuần 4: `SRS-NFR-06`, `SRS-FR-24`, `SRS-FR-33`, `SRS-NFR-25`; lai 2: `SRS-FR-20`, `SRS-FR-23`) · **CHƯA QUYẾT** → `TBD` **7** (thuần 4: `SRS-NFR-07`, `SRS-NFR-08`, `SRS-NFR-09`, `SRS-NFR-16`; lai 3: `SRS-FR-26`, `SRS-NFR-20`, `SRS-NFR-17`).` | ⭐ **Xem [§2.1 Phép tính](#21--câu-đếm-srs345--tính-lại-và-ghi-rõ-phép-tính)** — kết quả khác nhau theo phạm vi PM chọn | Câu đếm phải khớp tổng **68** (`SRS:343`) |
| **A6** | `SRS-Comic-Studio.md:58` **và** `:60` | `:58` → `#### b. Năm hàng **LAI** — cơ chế CHỐT, tham số bên trong chưa quyết`<br>`:60` → ``SRS-FR-20` · `SRS-FR-23` · `SRS-FR-26` · `SRS-NFR-17` · `SRS-NFR-20`. Cách đọc đúng:…` | Nếu `SRS-NFR-09` được gắn nhãn **LAI** ⇒ `:58` → `#### b. **Sáu** hàng **LAI**…` và `:60` thêm `SRS-NFR-09` vào danh sách. Nếu đồng bộ cả 07/08 ⇒ `**Tám** hàng LAI`, thêm cả `SRS-NFR-07`, `SRS-NFR-08` | ⭐ **PM chưa grep ra dòng này.** Đây là dòng **duy nhất** trong `SRS` liệt kê danh sách LAI theo tên; bỏ sót là để lại một mâu thuẫn nội tại mới ngay trong `§1.2` |
| **A7** | `SRS-Comic-Studio.md:95` | `\| Lựa chọn vendor (auth / billing / object storage), hosting / PaaS / region, ngôn ngữ & framework \| Không tài liệu nào quyết. … ⇒ `TBD` (mục 5.2), **sẽ được đặc tả tại tầng 030-Specs** \|` | Giữ nguyên **lý do lịch sử** (*"chọn giúp ở SRS làm tầng design mất quyền quyết định thật"* — lập luận đó vẫn đúng), đổi mệnh đề cuối: `⇒ `TBD` tại tầng 020, **đã được đặc tả tại tầng 030-Specs** (`ADR-001`…`ADR-004`); phần **billing vendor** vẫn `TBD`` | Câu *"sẽ được đặc tả"* (thì tương lai) ⛔ không còn đúng — tầng 030 đã tồn tại và đã đặc tả. §1.3 *Ngoài phạm vi* |
| **A8** | ⭐ `SRS-Comic-Studio.md:15` | `…mọi chi tiết hiện thực còn lại (DDL đầy đủ, API contract, thuật toán, tham số hoá, lựa chọn vendor) **sẽ được đặc tả tại tầng 030-Specs** — tầng đó **chưa tồn tại tại thời điểm viết**, nên SRS này **không tạo bất kỳ link nào** trỏ vào đó.` | Đề xuất: `…**đã được đặc tả tại tầng 030-Specs** — tầng đó đã tồn tại, và SRS này **được phép link** vào các `ADR-001`…`ADR-004` ở những hàng đã được đóng.` | ⭐⭐ **PM chưa grep ra dòng này và nó CHẶN A1/A2.** Đây là **chính sách toàn tài liệu**: `SRS` hiện tự cấm mình tạo link vào 030. Nếu ⛔ không sửa `:15` mà A1/A2 vẫn thêm link ⇒ tạo mâu thuẫn nội tại mới. **PM phải quyết trước**: (a) sửa `:15` rồi link ⭐ *em đề xuất*; hay (b) giữ `:15`, và A1/A2 chỉ ghi tên ADR bằng **văn bản thuần, ⛔ không link** |
| **A9** | `SRS-Comic-Studio.md:7` | `updated: 2026-08-29` | `updated: 2026-08-30` | Bắt buộc theo kỷ luật front-matter khi file thay đổi |

### 2.B — Nhóm bổ sung nếu PM đồng bộ **cả** `SRS-NFR-07` + `SRS-NFR-08` (⭐ em đề xuất làm cùng lô)

> **Vì sao nên làm cùng lô**: `ADR-002`/`ADR-003`/`ADR-004` đã nhận việc và đã ra quyết định (`ADR-002:189`, `ADR-003:173-175`, `ADR-004:171`). Để `NFR-07`/`NFR-08` ở `CHƯA QUYẾT` là **cùng một loại lệch tầng**, chỉ khác mã số. Sửa sau = mở lại đúng những dòng vừa động vào (`:345`, `:58`, `:60`, `:95`, `:263`) ⇒ đúng cái bẫy đã làm đắt run `2026-08-28`.

| # | `file:line` | Nguyên văn hiện tại (trích) | Nội dung đề xuất | Lý do |
|:--:|---|---|---|---|
| **B1** | `SRS-Comic-Studio.md:148` | `\| Hosting / PaaS / container platform / region \| `TBD` \| `SRS-NFR-07` \|` | `\| Hosting / PaaS / container platform / region \| **Container PaaS được quản lý · một image hai process · managed Postgres có PITR · ĐÚNG MỘT region gần VN nhất** (CHỐT) · **Render, region Singapore** (MẶC ĐỊNH, thang đường lui 3 bậc) — [ADR-002] \| `SRS-NFR-07` \|` | `ADR-002:43-58`, `:60-75` |
| **B2** | `SRS-Comic-Studio.md:256` | `\| **SRS-NFR-07** \| … \| **Không anchor được** — grep toàn `docs/010-Planning/`… \| **CHƯA QUYẾT** → `TBD` \|` | Cột 3 → `**ADR-002** (tầng 030)`. Cột 4 → `**LAI** — **CHỐT**: container PaaS được quản lý (⛔ không Kubernetes) · build một lần → một image → hai process type · managed PostgreSQL có PITR + **restore đã diễn tập** · **đúng MỘT region** · portability guardrail · **MẶC ĐỊNH**: **Render, region Singapore** — thang đường lui ghi rõ: `1.` Fly.io · `2.` GCP Cloud Run + Cloud SQL · `3.` AWS ECS Fargate + RDS. ⚠️ **Reopen trigger ghi trước**: nếu luật sư trả lời *"dữ liệu phải nằm trong lãnh thổ Việt Nam"* thì **cả `ADR-002` và `ADR-004` mở lại**` | ⭐ Reopen trigger (`ADR-002:82`, `:86`) là lý do hàng này ⛔ **không được** ghi CHỐT thuần |
| **B3** | `SRS-Comic-Studio.md:257` | `\| **SRS-NFR-08** \| Vendor cụ thể của auth / billing / object storage \| `MVP-Scope §3 E4` chỉ quyết *"mua"*… \| **CHƯA QUYẾT** → `TBD` \|` | Cột 3 → `**ADR-003** (auth, billing) · **ADR-004** (object storage)`. Cột 4 → `**LAI** — **CHỐT**: seam đổi vendor (`ADR-003` 8 điều: vendor ⛔ không sở hữu `tenant`/`membership`, `external_auth_id` `UNIQUE`, JWT qua JWKS, ⛔ custom claim **không bao giờ** là nguồn sự thật cho `tenant_id`; `ADR-004` 9 điều signed URL) · **MẶC ĐỊNH**: **auth = Clerk**, **object storage = Cloudflare R2** — thang đường lui + tiêu chí spike ghi rõ, ⛔ **chưa mua** · ⭐ **CHƯA QUYẾT** → `TBD`: **vendor billing** — chặn bởi **quốc gia pháp nhân bán hàng**, ⛔ không tài liệu nào trong repo trả lời. Ai đóng: **Founder** + dev · Khi nào: **trước MVP3** (seam vẫn phải có từ MVP1)` | ⭐ **⛔ Tuyệt đối không ghi `SRS-NFR-08` thành MẶC ĐỊNH thuần** — sẽ **đóng hộ** vendor billing, thứ `ADR-003:71-79` cố ý để mở |
| **B4** | `SRS-Comic-Studio.md:263` | `> Ba hàng `TBD` ở trên **là câu trả lời đúng, không phải chỗ trống bị bỏ quên**: … Lựa chọn vendor / hosting / framework **sẽ được đặc tả tại tầng 030-Specs**.` | `> Ba hàng trên **đã được đóng ở tầng 030-Specs** (`ADR-001`, `ADR-002`, `ADR-003`, `ADR-004`), phần lớn ở mức **MẶC ĐỊNH có đường lui ghi rõ**, ⛔ không phải **CHỐT**. ⭐ **Phần duy nhất còn `TBD` thật là vendor billing** (`ADR-003`) — chặn bởi quyết định pháp nhân của Founder, ⛔ không phải bởi thiếu phân tích kỹ thuật.` | Cả câu hiện tại (số đếm *"ba hàng `TBD`"* + thì tương lai *"sẽ được"*) đều sai sau đồng bộ |
| **B5** | `SRS-Comic-Studio.md:375` | `\| Hosting / container platform / region \| `TBD` — **sẽ được đặc tả tại tầng 030-Specs** \| `SRS-NFR-07` \|` | `\| Hosting / container platform / region \| **Render · region Singapore** (MẶC ĐỊNH, đường lui 3 bậc) trên container PaaS được quản lý (CHỐT) — `ADR-002` \| `SRS-NFR-07` \|` | §4.2 Hardware Interfaces |
| **B6** | `SRS-Comic-Studio.md:385` | `\| Auth & billing \| **Mua, không tự viết**; vendor `TBD` \| `SRS-FR-03`, `SRS-NFR-08` \|` | `\| Auth & billing \| **Mua, không tự viết**; **vendor auth = Clerk (MẶC ĐỊNH, chưa mua)**; ⭐ **vendor billing vẫn `TBD`** \| `SRS-FR-03`, `SRS-NFR-08` \|` | §4.3 Software Interfaces — phải phân biệt hai nửa |
| **B7** | `SRS-Comic-Studio.md:386` | `\| Object storage \| Key `tenant/{tenant_id}/{sha256}`, … ; vendor `TBD` \| `SRS-FR-02`, `SRS-NFR-08` \|` | Đổi mệnh đề cuối: `…; **vendor = Cloudflare R2 (MẶC ĐỊNH, chưa mua — 4 hạng mục phải verify)**` | `ADR-004:66-75` |
| **B8** | `SRS-Comic-Studio.md:455` (`b-1`) | `…Cơ chế mã hoá và nơi giữ secret phụ thuộc hosting platform (`SRS-NFR-07`) và vendor (`SRS-NFR-08`) — **cả hai còn `TBD`**…` | Đổi mệnh đề: `…⚠️ **`ADR-002` tuyên bố tường minh ⛔ KHÔNG đóng hàng này**: điều 6 chỉ quyết *cách nạp cấu hình* (biến môi trường), ⛔ không quyết nghĩa vụ mã hoá. Ai đóng: **Dev** · Khi nào: sau khi platform được mua` | ⭐ Hàng **vẫn `TBD`**, nhưng lý do *"cả hai còn `TBD`"* ⛔ sai. Nguồn thay thế: `ADR-002:84` |
| **B9** | `SRS-Comic-Studio.md:456` (`b-2`) | `…Phụ thuộc vendor secret manager còn `TBD` (`SRS-NFR-08`) \| `SRS-FR-32`, `SRS-NFR-08` \|` | Đổi mệnh đề: `…Phụ thuộc **cơ chế giữ secret chưa được thiết kế** — `ADR-002` điều 6 cấm SDK secret manager của vendor (chỉ biến môi trường), nên nơi giữ key BYOK ⛔ **chưa có lời giải**. ⭐ **Đóng đúng nghĩa cần một ADR MỚI** (nợ kỹ thuật số 1). Ai đóng: **Architect + Founder**` | Hàng vẫn `TBD`; lý do phải đổi. Nguồn: `ADR-002:53`, `Spec-Security-Threat-Model.md:85`, `SDD-Comic-Studio.md:777` |
| **B10** | `SRS-Comic-Studio.md:459` (`b-5`) | `…trần tài nguyên chỉ xác định được **sau khi chọn hosting platform** (`SRS-NFR-07` còn `TBD`)…` | Đổi mệnh đề: `…trần tài nguyên chỉ xác định được **sau khi có số đo thật trên platform đã chọn** (`ADR-002`: Render/Singapore, MẶC ĐỊNH) — ⚠️ **`ADR-002` tuyên bố ⛔ KHÔNG đóng hàng này**. Ai đóng: **Founder + dev** · Khi nào: sau MVP0` | Hàng vẫn `TBD`; lý do phải đổi. Nguồn: `ADR-002:84` |

### 2.1 ⭐ Câu ĐẾM `SRS:345` — tính lại và ghi rõ phép tính

**Quy tắc phân loại đã được suy ra từ chính dữ liệu hiện có (verify 5/5 hàng LAI)**: một hàng **LAI** được xếp vào **rổ của thành phần YẾU NHẤT (mở nhất)** của nó, và **chỉ đếm ĐÚNG MỘT LẦN** (nên tổng luôn = **68**, khớp `SRS:343`).

| Hàng LAI | Cấu trúc | Rổ được xếp | Nguồn |
|---|---|---|---|
| `SRS-FR-20` | CHỐT + MẶC ĐỊNH | **MẶC ĐỊNH** | `SRS:175`, `:345` |
| `SRS-FR-23` | CHỐT + MẶC ĐỊNH | **MẶC ĐỊNH** | `SRS:178`, `:345` |
| `SRS-FR-26` | CHỐT + `TBD` | **CHƯA QUYẾT** | `SRS:181`, `:345` |
| `SRS-NFR-17` | CHỐT + `TBD` | **CHƯA QUYẾT** | `SRS:309`, `:345` |
| `SRS-NFR-20` | CHỐT + `TBD` | **CHƯA QUYẾT** | `SRS:324`, `:345` |

**Kiểm tra tổng hiện tại**: `55 + 6 + 7 = 68` ✅ (khớp `SRS:343`).

> [!WARNING]
> ⭐ **Em BÁC một tiền đề trong brief.** Brief ghi *"Đóng một hàng `TBD` **làm sai cả ba con số này**"*. ⛔ **Không đúng — dù đọc theo phương án nào.**
> **Lý do**: con số thứ nhất là **`CHỐT` thuần**. ⛔ Không hàng nào trong `NFR-07/08/09` trở thành **CHỐT thuần**, vì cả ba ADR đều **tự khai có tầng MẶC ĐỊNH kèm đường lui** (`ADR-001:52`, `ADR-002:60`, `ADR-003:57`, `ADR-004:66`). ⇒ **`CHỐT` thuần đứng yên ở `55`** trong mọi phương án. Chỉ **hai** con số sau đổi (và ở Phương án 1 thì **không con số nào** đổi — chỉ phần trong ngoặc đổi).
> ⛔ PM **đừng "sửa" con số `55`** — nó đang đúng.

#### Phương án 1 — chỉ đồng bộ `SRS-NFR-09`, gắn nhãn **LAI** (đúng quy tắc yếu-nhất)

`SRS-NFR-09` còn `TBD` ở hai tham số (`ADR-001:66`, `:67`) ⇒ vẫn nằm rổ **CHƯA QUYẾT**, chỉ chuyển từ *thuần* → *lai*.

```
CHỐT thuần        : 55  (không đổi)
MẶC ĐỊNH          : 6   (không đổi — thuần 4, lai 2)
CHƯA QUYẾT → TBD  : 7   (không đổi — nhưng thuần 4 → 3, lai 3 → 4)
Tổng: 55 + 6 + 7 = 68 ✅
```

Câu đề xuất cho `SRS:345`:
`… **CHỐT** thuần **55** · **MẶC ĐỊNH** **6** (thuần 4: `SRS-NFR-06`, `SRS-FR-24`, `SRS-FR-33`, `SRS-NFR-25`; lai 2: `SRS-FR-20`, `SRS-FR-23`) · **CHƯA QUYẾT** → `TBD` **7** (thuần 3: `SRS-NFR-07`, `SRS-NFR-08`, `SRS-NFR-16`; lai 4: `SRS-FR-26`, `SRS-NFR-20`, `SRS-NFR-17`, `SRS-NFR-09`).`
⇒ Kéo theo **A6**: `:58` → *"**Sáu** hàng LAI"*, `:60` thêm `SRS-NFR-09`.

#### Phương án 2 — chỉ đồng bộ `SRS-NFR-09`, gắn nhãn **MẶC ĐỊNH thuần**

(Coi hai `TBD` còn lại của `ADR-001` là tham số **tầng design**, ⛔ ngoài phạm vi phát biểu của `SRS-NFR-09`.)

```
CHỐT thuần        : 55            (không đổi)
MẶC ĐỊNH          : 6 → 7         (thuần 4 → 5, thêm SRS-NFR-09)
CHƯA QUYẾT → TBD  : 7 → 6         (thuần 4 → 3, bỏ SRS-NFR-09)
Tổng: 55 + 7 + 6 = 68 ✅
```
⇒ ⛔ **Không** kéo theo A6.
⚠️ **Rủi ro của phương án này**: nó **giấu** việc *phiên bản Node LTS* và *thư viện compositor/PDF* chưa chọn — đúng loại thông tin mà `SRS:437` cấm làm mờ.

#### ⭐ Phương án 3 — đồng bộ CẢ BA (`NFR-07` + `NFR-08` + `NFR-09`), quy tắc yếu-nhất — **em đề xuất**

| Hàng | Cấu trúc sau ADR | Rổ mới |
|---|---|---|
| `SRS-NFR-07` | CHỐT + MẶC ĐỊNH (⛔ không còn `TBD` trong phạm vi phát biểu của nó) | **MẶC ĐỊNH** (lai) |
| `SRS-NFR-08` | CHỐT + MẶC ĐỊNH + ⭐ **`TBD` vendor billing** | **CHƯA QUYẾT** (lai) |
| `SRS-NFR-09` | CHỐT + MẶC ĐỊNH + ⭐ **`TBD` Node LTS pin, thư viện compositor** | **CHƯA QUYẾT** (lai) |

```
CHỐT thuần        : 55            (không đổi)
MẶC ĐỊNH          : 6 → 7         thuần 4 (giữ nguyên) + lai 2 → 3 (thêm SRS-NFR-07)
CHƯA QUYẾT → TBD  : 7 → 6         thuần 4 → 1 (chỉ còn SRS-NFR-16)
                                  + lai 3 → 5 (thêm SRS-NFR-08, SRS-NFR-09)
Kiểm: thuần 1 + lai 5 = 6 ✅
Tổng: 55 + 7 + 6 = 68 ✅
Tổng hàng LAI: 3 (rổ MẶC ĐỊNH) + 5 (rổ CHƯA QUYẾT) = 8
```

Câu đề xuất cho `SRS:345`:
`… **CHỐT** thuần **55** · **MẶC ĐỊNH** **7** (thuần 4: `SRS-NFR-06`, `SRS-FR-24`, `SRS-FR-33`, `SRS-NFR-25`; lai 3: `SRS-FR-20`, `SRS-FR-23`, `SRS-NFR-07`) · **CHƯA QUYẾT** → `TBD` **6** (thuần 1: `SRS-NFR-16`; lai 5: `SRS-FR-26`, `SRS-NFR-20`, `SRS-NFR-17`, `SRS-NFR-08`, `SRS-NFR-09`).`
⇒ Kéo theo **A6**: `:58` → *"**Tám** hàng LAI"*, `:60` thêm cả ba mã.

> **⭐ Vì sao em đề xuất Phương án 3**: (a) áp đúng quy tắc mà chính `SRS` đang dùng cho 5 hàng LAI hiện có, ⛔ không phát minh quy ước mới; (b) ⛔ không đóng hộ vendor billing và ⛔ không giấu hai tham số còn mở của `ADR-001`; (c) dọn một lần, ⛔ không để lại lô hai — đúng bài học `2026-08-28`.

### 2.2 ⚠️ Hàng em ĐÃ KIỂM và kết luận ⛔ KHÔNG cần sửa

| `file:line` | Nguyên văn (trích) | Vì sao ⛔ không sửa |
|---|---|---|
| `SRS-Comic-Studio.md:337` | `\| **E. Multi-tenancy & hạ tầng** \| … `SRS-NFR-07`…`SRS-NFR-09` \| **11** \|` | Đây là bảng **đếm số hàng**, ⛔ không phải đếm mức độ rắn. Số hàng ⛔ không đổi ⇒ `11` vẫn đúng |
| `SRS-Comic-Studio.md:19-25` (Mục lục) | 7 mục cấp 1 | ⛔ Không có mục nào nói tới framework/vendor/hosting |
| `SRS-Comic-Studio.md:60` (nửa sau câu) | `Cách đọc đúng: **cơ chế đã khẳng định**, `TBD` **chỉ áp cho tham số**…` | Nguyên tắc vẫn đúng; chỉ **danh sách mã** ở nửa đầu cần bổ sung (A6) |
| `PRD-Comic-Studio.md` (toàn file) | `PRD:296` chỉ nói *"Mua auth + billing, không tự viết"* | ✅ Đã grep `TBD`/`vendor`/`hosting`/`stack`/`ngôn ngữ`/`framework`/`NestJS`/`React` — ⛔ **không có** phát biểu *"chưa quyết framework/ngôn ngữ"* nào. Các `TBD` của PRD (`TBD-1`…`TBD-5`, mục 3.3) là **persona/JTBD**, ⛔ không liên quan |
| `Requirements-MOC.md` | — | ⛔ Ngoài ownership của lô này (`*-MOC.md`) |

---

## 3. Ripple — tầng 030 viện dẫn *"`SRS-NFR-09` còn `TBD`"*

### 3.1 ⭐ Câu hỏi khó: `C-10` có tự động đóng theo không?

> [!CAUTION]
> ⛔ **KHÔNG. `C-10` VẪN MỞ.** ⛔ Đừng đóng hộ một `TBD` bảo mật.

**Lập luận, từng bước:**

1. **Cái gì `C-10` đòi hỏi** (`Spec-Security-Threat-Model.md:292`): ba ràng buộc lên **engine render** — ⛔ không nạp tài nguyên ngoài (remote URL / file cục bộ / entity ngoài); ⛔ không để chuỗi người dùng vào ngữ cảnh có thể thực thi; có **trần tài nguyên**. Ba ràng buộc này ⛔ **không phải** thuộc tính của *ngôn ngữ*, mà của **thư viện/engine cụ thể**.
2. **Cái gì `ADR-001` ĐÃ quyết liên quan tới compositor**: `ADR-001:50` (điều 8) chốt **cơ chế NGẮT DÒNG** — chuẩn hoá NFC tại biên ingest, ngắt theo grapheme cluster + word boundary bằng `Intl.Segmenter`, wrap **cùng runtime với compositor**. ⚠️ Đó là **tính đúng đắn typesetting**, ⛔ **không phải** thuộc tính bảo mật của `C-10`.
3. **Cái gì `ADR-001` KHÔNG quyết** — nguyên văn `ADR-001:66`, hàng đầu của bảng `TBD`:
   `| Thư viện compositor + sinh PDF (shaping tiếng Việt, 300 DPI) | Không tài liệu nào trong repo đánh giá; ⛔ không dán tên kèm con số khi chưa đo | Dev | **Spike MVP0**, nghiệm thu bằng test ở `## Consequences` |`
   ⇒ **Engine render — đúng cái mà `C-10` ràng buộc — vẫn CHƯA ĐƯỢC CHỌN.**
4. **Một `TBD` thứ hai còn liên quan**: `ADR-001:68` — *"Compositor chạy trong `worker_threads` hay tách hẳn thành job"* — chưa quyết; và `ADR-001:121` (`## Consequences` tiêu cực #1) cấm chạy compositor trong request handler. Trần tài nguyên của `C-10` phụ thuộc mô hình chạy này.

⇒ **Phát biểu lý do ĐÚNG để PM viết lại**:

> ⛔ Chưa chọn được cơ chế render an toàn — ⚠️ **⛔ không phải** vì `SRS-NFR-09` còn `TBD` (`ADR-001` đã đóng việc chọn ngôn ngữ/framework), mà vì **`ADR-001` §`TBD` hàng 1 để mở *"thư viện compositor + sinh PDF"*** và hàng 3 để mở *"compositor chạy trong `worker_threads` hay tách job"*. Chọn TypeScript/Node **thu hẹp** không gian phương án nhưng ⛔ **không chọn** engine. Ba ràng buộc bảo mật của `C-10` **đã CHỐT sẵn** và là **tiêu chí nghiệm thu bắt buộc của spike MVP0**.

> [!WARNING]
> ⚠️ **Xung đột CHỦ SỞ HỮU + MỐC mà PM phải phân xử** (em phát hiện, ⛔ không tự quyết):
> - `Spec-Security-Threat-Model.md:292` & `:521` ghi **ai đóng: Architect**, mốc *"lô API / `Spec-Integration-*`"*; `Endpoint-Preview-Export.md:249` ghi **Architect**, mốc **Phase 4**.
> - `ADR-001:66` ghi **ai đóng: Dev**, mốc **spike MVP0**.
> **Cách hoà giải em đề xuất** (⛔ chưa áp dụng): tách hai việc — **Architect sở hữu TẬP RÀNG BUỘC** (đã CHỐT ở `C-10`, ⛔ không cần làm lại) · **Dev sở hữu việc CHỌN thư viện thoả tập ràng buộc đó**, tại **spike MVP0**, và `C-10` trở thành **tiêu chí nghiệm thu của spike**. ⇒ Mốc thật là **MVP0**, **sớm hơn** *"Phase 4"* đang ghi.

### 3.2 Bảng ripple đầy đủ

| # | `file:line` | Nguyên văn hiện tại (trích) | Cần sửa? | Nội dung đề xuất |
|:--:|---|---|:--:|---|
| **R1** | `docs/030-Specs/Security/Spec-Security-Threat-Model.md:292` | `…⚠️ ⛔ Chưa chọn được cơ chế cụ thể vì `SRS-NFR-09` (framework) còn `TBD` ⇒ **ai đóng: Architect, ở lô API/`Spec-Integration-*`**, trước khi compositor đầu tiên chạy` | ✅ **CÓ** | `…⚠️ ⛔ Chưa chọn được cơ chế cụ thể — ⛔ **không phải** vì `SRS-NFR-09` (đã đóng bởi `ADR-001`), mà vì **`ADR-001` §`TBD` để mở *"thư viện compositor + sinh PDF"*** và *"compositor trong `worker_threads` hay tách job"*. ⇒ **Ràng buộc: Architect (đã CHỐT ở hàng này) · Chọn thư viện: Dev, tại spike MVP0, nghiệm thu bằng chính ba ràng buộc trên**` |
| **R2** | `docs/030-Specs/Security/Spec-Security-Threat-Model.md:521` | `\| **mới** \| ⭐ **Cơ chế render an toàn của compositor** (`C-10`, `TM-F6-3`) — ⛔ chưa chọn được vì `SRS-NFR-09` còn `TBD` \| **Architect**, lô API / `Spec-Integration-*` \| Trước khi compositor đầu tiên chạy \|` | ✅ **CÓ** | Cột 1 → `…⛔ chưa chọn được vì **`ADR-001` §`TBD` chưa chọn thư viện compositor + sinh PDF**`. Cột 2/3 → theo hoà giải ở §3.1 (**Dev**, **spike MVP0**) — ⚠️ **PM quyết** |
| **R3** | `docs/030-Specs/API/Endpoint-Preview-Export.md:200` (`API-PE-10`) | `…⚠️ ⛔ **File này ⛔ KHÔNG chốt cơ chế** — cơ chế phụ thuộc `SRS-NFR-09` còn `TBD` ⇒ xem [`TBD` còn lại](#tbd-còn-lại)` | ✅ **CÓ** | `…⚠️ ⛔ **File này ⛔ KHÔNG chốt cơ chế** — cơ chế phụ thuộc **`ADR-001` §`TBD` (thư viện compositor + sinh PDF)**, ⛔ không phải `SRS-NFR-09` ⇒ xem [`TBD` còn lại](#tbd-còn-lại)` |
| **R4** | `docs/030-Specs/API/Endpoint-Preview-Export.md:249` | `\| ⭐ **Cơ chế render an toàn của compositor** (`C-10`) — ⛔ chưa chọn được vì `SRS-NFR-09` (framework) còn `TBD`. …\| **Architect** … \| **Phase 4** — trước khi compositor đầu tiên chạy \|` | ✅ **CÓ** | Cột 1 → thay mệnh đề lý do như R3. Cột 3 → cân nhắc **MVP0 (spike)** thay vì **Phase 4** — ⚠️ **PM quyết**, xem cảnh báo §3.1 |
| **R5** | `docs/030-Specs/Architecture/SDD-Comic-Studio.md:62` (`R-6`) | `\| **R-6** \| **Một ngôn ngữ** cho api + worker + web; **một** hợp đồng API \| Không context-switch giữa ba runtime cho một người — [ADR-001](…) \| `SRS-NFR-09` \|` | ⛔ **KHÔNG** | Hàng này chỉ **neo** `R-6` vào `SRS-NFR-09` và link `ADR-001`. Nó ⛔ **không hề** khẳng định `SRS-NFR-09` còn `TBD`. Sau đồng bộ, nó **đúng hơn trước** |
| **R6** | `docs/030-Specs/Architecture/SDD-Comic-Studio.md:457` | `> [SRS §5.2](…) hàng `b-7` ghi rõ hạng mục này **phụ thuộc `SRS-NFR-07` và `SRS-NFR-09`**; cả [ADR-001](…) lẫn [ADR-002](…) đều tuyên bố **không đóng** hàng này.` | ⚠️ **CÓ ĐIỀU KIỆN** | Nửa sau (*"cả `ADR-001` lẫn `ADR-002` đều tuyên bố không đóng"*) **hiện đang ĐÚNG** (`ADR-001:69`, `ADR-002:84`). Nửa đầu là **trích dẫn `SRS §5.2` hàng `b-7`** — nếu PM land **A4** (sửa `SRS:461`) thì câu trích này **phải được đồng bộ theo**, nếu không hai tầng lại lệch. ⇒ **Sửa CÙNG LÔ với A4, ⛔ không sửa rời** |
| **R7** | `docs/030-Specs/Architecture/ADR-001-…md:15` | `` `SRS-NFR-09` (…) là **`CHƯA QUYẾT` → `TBD`** … `` | ⛔ **KHÔNG** | Xem [§4](#4-adr-001-có-mâu-thuẫn-nội-tại-không) |
| **R8** | `docs/030-Specs/Architecture/ADR-001-…md:69` | `…⚠️ **ADR này đóng việc CHỌN ngôn ngữ/framework, ⛔ KHÔNG đóng hai hàng đó.**…` | ⛔ **KHÔNG** | ⭐ Đây là **dòng chịu lực** chứng minh `b-6`/`b-7` ⛔ không được đóng theo. Chính nó là **nguồn** cho đề xuất A3/A4. ⛔ Chạm vào là làm mất bằng chứng |
| **R9** | `docs/030-Specs/Architecture/ADR-001-…md:172` | `\| Ngôn ngữ / framework backend & frontend, ORM & migration tool \| `SRS-NFR-09` (`CHƯA QUYẾT` → `TBD`) \| … \|` | ⛔ **KHÔNG** | Xem [§4](#4-adr-001-có-mâu-thuẫn-nội-tại-không) |

### 3.3 Ripple BỔ SUNG — PM chưa grep ra (chỉ áp dụng nếu đồng bộ `NFR-07`/`NFR-08`)

| # | `file:line` | Nguyên văn (trích) | Cần sửa? | Ghi chú |
|:--:|---|---|:--:|---|
| **R10** | `docs/030-Specs/Architecture/ADR-006-RLS-Tenant-Context-Injection.md:256` | `\| Vendor auth (nguồn của `user_id` ở `D3` bước 1) \| `SRS-NFR-08` = `TBD` ([SRS](…) §3.E) \| `ADR-003` \| Lô ADR-001…004 (song song) \|` | ✅ **CÓ** (nếu đồng bộ 08) | Đây là bảng *"phụ thuộc chờ đóng"*; `ADR-003` **đã** ra quyết định. Đề xuất cột 2 → `` `SRS-NFR-08` phần **auth = MẶC ĐỊNH (Clerk)** theo `ADR-003`; ⛔ phần **billing vẫn `TBD`** `` |
| **R11** | `docs/030-Specs/Architecture/ADR-006-RLS-Tenant-Context-Injection.md:258` | `\| Chế độ pooling cụ thể … \| Phụ thuộc hosting, `SRS-NFR-07` = `TBD` … \| `ADR-002` \| … ⭐ **`SET LOCAL` an toàn với cả hai**, nên quyết định này **không bị chặn** \|` | ✅ **CÓ** (nếu đồng bộ 07) | Cột 2 → `Phụ thuộc hosting — `ADR-002` chọn **Render (MẶC ĐỊNH)**; chế độ pooling cụ thể vẫn chờ cấu hình thực tế`. ⭐ Kết luận *"không bị chặn"* ⛔ **giữ nguyên** |
| **R12** | `docs/030-Specs/Architecture/ADR-015-Job-Queue-In-Postgres.md:272` | `…⚠️ Trần chịu tải ⛔ **không đo được** cho tới khi chốt hosting (`SRS-NFR-07` còn `TBD`) — [SRS](…) §5.2 (`b-5`)…` | ✅ **CÓ** (nếu đồng bộ 07) | Đề xuất: `…cho tới khi **có số đo thật trên platform đã chọn** (`ADR-002`: Render/Singapore, MẶC ĐỊNH); `SRS` §5.2 (`b-5`) vẫn `TBD`…`. ⭐ **Kết luận ⛔ không đổi** — trần tải vẫn chưa đo |
| **R13** | `docs/030-Specs/Schema/DB-Entity-Tenancy.md:95` | `…`SRS-NFR-08` để **vendor** ở trạng thái `TBD`; [ADR-003](…) chốt **nguyên tắc** … chứ ⛔ không chốt danh sách trường…` | ✅ **CÓ** (nếu đồng bộ 08) | Đề xuất: `…`SRS-NFR-08` để **vendor auth ở mức MẶC ĐỊNH (Clerk), ⛔ chưa mua**; [ADR-003] chốt **nguyên tắc**…`. ⭐ **Kết luận ⛔ không đổi** — vẫn ⛔ không thêm cột `email` |
| **R14** | `docs/030-Specs/Schema/DB-Entity-Tenancy.md:312` | `\| Danh sách **trường đồng bộ từ vendor auth** vào `public."user"` \| PM + Architect ([ADR-003](…), `SRS-NFR-08`) \| Khi chốt vendor \|` | ⚠️ **TUỲ CHỌN** | *"Khi chốt vendor"* nay có thể ghi cụ thể hơn: *"Khi spike Clerk đạt/trượt 3 tiêu chí — kickoff MVP1"* (`ADR-003:69`) |
| **R15** | `docs/030-Specs/API/Spec-Integration-Auth-Provider.md:189` | `…· `SRS-NFR-08` (vendor `TBD`) · …` | ⚠️ **TUỲ CHỌN** | Trong mục *Tài liệu tham khảo*. Đổi thành `` `SRS-NFR-08` (vendor auth = MẶC ĐỊNH, billing `TBD`) `` cho chính xác |
| **R16** | `docs/000-Index.md:219` | `\| **5** \| ⚠️ **`SRS-NFR-09` (tầng 020) vẫn ghi framework frontend `CHƯA QUYẾT → TBD`** … Lệch tầng, cần run đồng bộ 020↔030 \| Trung bình \| Architect + BA \|` | ✅ **CÓ** — ⛔ **NGOÀI ownership của em** | ⭐ Đây là **hàng rủi ro mô tả chính lô này**. Sau khi PM land, hàng này phải được **đóng/gạch**. ⛔ Em ⛔ không chạm `docs/000-Index.md` |

### 3.4 Đã kiểm và kết luận ⛔ KHÔNG cần sửa

| `file:line` | Vì sao |
|---|---|
| `Spec-Security-Threat-Model.md:85` (`b-2`) | *"Phụ thuộc `b-1` và `SRS-NFR-08`"* — vẫn **đúng**: `b-1` chưa đóng, vendor billing + nơi giữ secret chưa đóng |
| `DB-Entity-Generation.md:486` (`T-27`) | *"phụ thuộc `SRS-NFR-08` (vendor + **nơi giữ secret**)"* — nơi giữ secret vẫn chưa có lời giải (`ADR-002:53` cấm SDK secret manager) ⇒ vẫn đúng |
| `SDD-Comic-Studio.md:724`, `:777` | Nhóm *Vendor và mua sắm*; `T-27` là nợ kỹ thuật số 1 — vẫn đúng |
| `ADR-010:176` | *"Khi `ADR-003` chuyển khỏi `draft` — trước MVP1"* — `ADR-003:4` vẫn `draft` ⇒ vẫn đúng |
| `Spec-Integration-Billing-Provider.md:65` | Mô tả **chính xác** rằng vendor billing ở lại `TBD` có chủ đích — ⭐ đây là tầng 030 **đang đúng**, và là bằng chứng mạnh cho **B3** |
| `Spec-Integration-Object-Storage.md:128` | *"R2 là **mặc định**, ⛔ không phải đã mua"* — đúng nguyên tắc MẶC ĐỊNH |
| `Spec-Integration-Auth-Provider.md:92` | *"Clerk là **mặc định**, ⛔ không phải đã mua"* — đúng |
| `SDD-Comic-Studio.md:811` | *"`SRS-FR-20`, `SRS-FR-23`, `SRS-FR-26`, `SRS-NFR-17`, `SRS-NFR-20` là **năm hàng LAI**"* | ⚠️ **CÓ ĐIỀU KIỆN** — nếu PM land **A6** (đổi *Năm* → *Sáu/Tám* hàng LAI ở `SRS:58`, `:60`) thì dòng `SDD:811` này **cũng phải đồng bộ**, nếu không lại lệch tầng. ⭐ **PM chưa grep ra dòng này** |

> [!IMPORTANT]
> ⭐ **`SDD-Comic-Studio.md:811` là ripple bị bỏ sót nguy hiểm nhất của lô này** — nó **hard-code con số "năm"** và **liệt kê đủ 5 mã**. Nếu PM sửa `SRS:58`/`:60` mà quên `SDD:811`, ta tạo ra **đúng loại lệch tầng** mà lô này đang đi dọn. Em đưa nó lên đây thay vì để trong bảng "không cần sửa".

---

## 4. `ADR-001` có mâu thuẫn nội tại không?

### ⛔ KHÔNG. Cả hai dòng ĐÚNG như đang có. ⛔ Không sửa dòng nào.

**Dòng `ADR-001:15`** — nằm trong `## Context`.

Nguyên văn: `` `SRS-NFR-09` (*"Ngôn ngữ / framework backend & frontend"*) là **`CHƯA QUYẾT` → `TBD`** — [SRS-Comic-Studio](…) §3.E ghi rõ *"Không anchor được"*… Đây là quyết định có **chi phí đảo ngược thấp nhất của toàn dự án ngay lúc này**… ``

`## Context` của một ADR **theo định nghĩa** là ảnh chụp thế giới **TRƯỚC** quyết định. Sửa nó thành *"`SRS-NFR-09` đã đóng"* sẽ:
1. **Phá chính chuỗi biện minh của ADR** — câu *"chi phí đảo ngược thấp nhất ngay lúc này"* chỉ có nghĩa khi tiền đề *"chưa có dòng code nào"* đúng;
2. **Tạo vòng lặp logic**: ADR đóng `SRS-NFR-09` lại viện dẫn `SRS-NFR-09` đã đóng;
3. **Xoá dấu vết audit** — mất khả năng trả lời *"tại thời điểm quyết, ta biết gì?"*.

**Dòng `ADR-001:172`** — nằm trong bảng `### ADR này quyết (phần Phase 1 **cố ý** để mở)`.

Nguyên văn: `| Ngôn ngữ / framework backend & frontend, ORM & migration tool | `SRS-NFR-09` (`CHƯA QUYẾT` → `TBD`) | `SRS` §3.E · [findings/architect](…) §1.8, §2.1 |`

Cột 2 của bảng này là cột **`Mã`** — và `escalations.md:184` đã ghi tường minh vì sao header của 4 bảng `ADR-001…004` **cố ý khác** 18 bảng còn lại:

> `4 bảng của ADR-001…004 giữ | Quyết định | Mã | … | vì cột 2 của chúng chứa SRS-NFR-09/SRS-NFR-07/SRS-NFR-08/SRS-FR-02/— chứ không phải D-xx (đó là các bảng "cố ý để mở", không phải bảng ghi lại quyết định).`

⇒ Ngữ nghĩa của bảng là: *"requirement này **đang** mở, và ADR này là **nơi đóng** nó"*. Chú thích `(CHƯA QUYẾT → TBD)` chính là **trạng thái ĐẦU VÀO** mà ADR nhận việc. ⛔ Nó ⛔ không mâu thuẫn với `ADR-001:52-60`, vì hai dòng nói về **hai thời điểm khác nhau**.

### ⚠️ Rủi ro thật, và cách phòng — PM quyết

Sau khi `SRS:258` được viết lại thành **LAI**/**MẶC ĐỊNH**, một lô sau `diff` `ADR-001:172` với `SRS:258` sẽ thấy `CHƯA QUYẾT → TBD` ≠ nhãn mới và **có thể "sửa" nhầm `ADR-001`** — ⭐ đúng loại lỗi đã làm run `2026-08-28` thành lô đắt nhất.

Hai cách phòng (⛔ em ⛔ không thực hiện cách nào):

| | Phương án | Đánh giá |
|:--:|---|---|
| **(a)** ⭐ **em đề xuất** | **Giữ nguyên `ADR-001:15` và `:172`**, và ghi vào `escalations.md` của run này một dòng: *"`ADR-001:15` và `:172` mô tả **trạng thái ĐẦU VÀO**, ⛔ lô sau không được báo là lỗi"* | Đúng mô hình `escalations.md:184` đã dùng thành công cho header 4 bảng. **Chi phí bằng 0**, ⛔ không chạm file tầng 030 nào |
| **(b)** | Chú thích thêm `(trạng thái đầu vào tại thời điểm viết ADR)` vào cột 2 của `ADR-001:172` (và 3 ADR còn lại cho nhất quán) | Rõ hơn cho người đọc mới, nhưng là **sửa 4 ADR** — ⛔ ngoài phạm vi lô khảo sát này, và mở lại tầng Architecture vừa được *"đóng băng"* ở `escalations.md:181` (`E13`) |

---

## 5. Vấn đề phát hiện thêm — report-only

### 5.1 Bốn ADR còn `draft` — câu hỏi governance CHẶN

`ADR-001:4`, `ADR-002:4`, `ADR-003:4`, `ADR-004:4` đều là `status: draft`. Repo **đã dùng `draft` làm mốc chặn thật**: `ADR-010:176` ghi *"Khi `ADR-003` chuyển khỏi `draft` — trước MVP1"*.

⇒ **Câu hỏi PM phải trả lời trước khi land §2**: hạ nhãn `SRS-NFR-07/08/09` khỏi `CHƯA QUYẾT` dựa trên bốn ADR **`draft`** — có hợp lệ?

| | Phương án | Đánh giá |
|:--:|---|---|
| **(a)** ⭐ **em đề xuất** | Chuyển `ADR-001…004` sang `status: accepted` **cùng lô** với việc sửa `SRS` | Nhãn tầng 020 và trạng thái tầng 030 khớp nhau tại **một thời điểm**. ⚠️ Cần kiểm ripple `ADR-010:176` |
| **(b)** | Giữ `draft`, sửa `SRS` và ghi thêm *"nguồn: `ADR-001` (`draft`)"* vào cột 3 | Trung thực nhưng để lại một hàng phải sửa **lần hai** khi ADR được accept — đúng bẫy "lô thứ hai" |
| **(c)** | Hoãn toàn bộ đến khi ADR được accept | An toàn nhất về governance nhưng để lệch tầng tồn tại thêm, và `000-Index.md:219` đã ghi nhận nó là rủi ro |

### 5.2 `ADR-001` §Đường lui chỉ phủ **3/5** hàng MẶC ĐỊNH

`ADR-001:52-60` liệt **5** hàng MẶC ĐỊNH; `ADR-001:132-136` (bảng *Đường lui đã ghi rõ*) chỉ có **3** hàng: NestJS→Fastify · Drizzle→Kysely/`pg` · Vite/React→đổi frontend.

⇒ **`pnpm workspace`** (`ADR-001:59`) và **`ESLint boundary rule`** (`ADR-001:60`) đang ở *"MẶC ĐỊNH mà **thiếu đường lui ghi rõ**"* — ⛔ không thoả định nghĩa MẶC ĐỊNH của `SRS:50`.
⚠️ **Hệ quả cho lô này**: khi PM viết cột *Mức độ rắn* cho `SRS:258`, ⛔ **đừng khẳng định** *"toàn bộ tầng MẶC ĐỊNH đều có đường lui"* — chỉ 3/5 có. ⛔ Em ⛔ không sửa `ADR-001`; đây là hạng mục cho một lô sau.

### 5.3 `shadcn/ui + Tailwind` chưa có đường lui, và chưa xuất hiện ở `## Alternatives`

Hai vị trí duy nhất nhắc `shadcn` là `ADR-001:58` (tầng MẶC ĐỊNH) và `ADR-001:117` (`## Consequences` tích cực). Bảng đường lui `ADR-001:136` chỉ nói *"Vite/React không đủ cho editor ⇒ chỉ đổi **frontend**"* — ⛔ không nói riêng về UI kit. Và `## Alternatives considered` (`ADR-001:71-107`) ⛔ không có mục nào cân nhắc UI kit thay thế.
⇒ Về hình thức, `shadcn/ui + Tailwind` là một lựa chọn **MẶC ĐỊNH thiếu cả đường lui lẫn alternatives**. ⛔ **Report-only** — đây là bản sửa chưa commit của Founder, em ⛔ không đụng.

### 5.4 `SRS:437` — lệnh cấm gán số vẫn nguyên hiệu lực

Nguyên văn: *"⛔ **Không tự gán số cho bất kỳ hàng nào dưới đây.** … **Hai mươi mốt hàng** dưới đây **ở lại `TBD`**."*
⚠️ **Con số `21` phải được kiểm lại** nếu PM sửa các hàng `b-1`, `b-2`, `b-5`, `b-6`, `b-7` (A3, A4, B8, B9, B10). ⭐ **Theo phân tích của em, cả 5 hàng đó VẪN ở lại `TBD`** — chỉ đổi *mệnh đề lý do*, ⛔ không đổi trạng thái ⇒ **`21` vẫn đúng, ⛔ không sửa**. Em ghi ra để PM ⛔ không "sửa" nhầm một con số đang đúng (cùng loại với con số `55` ở `:345`).

---

## 6. Tài liệu tham khảo

- [`docs/020-Requirements/SRS-Comic-Studio.md`](../../../../020-Requirements/SRS-Comic-Studio.md) — `:7`, `:15`, `:19-25`, `:50`, `:58`, `:60`, `:95`, `:148`, `:149`, `:163`, `:256`, `:257`, `:258`, `:263`, `:337`, `:343`, `:345`, `:375`, `:385`, `:386`, `:437`, `:455`, `:456`, `:459`, `:460`, `:461`
- [`docs/020-Requirements/PRD-Comic-Studio.md`](../../../../020-Requirements/PRD-Comic-Studio.md) — đã grep, ⛔ không có dòng nào cần sửa
- [`docs/030-Specs/Architecture/ADR-001-Backend-And-Frontend-Tech-Stack.md`](../../../../030-Specs/Architecture/ADR-001-Backend-And-Frontend-Tech-Stack.md) — ⚠️ **bản chưa commit**; `:4`, `:15`, `:41-50`, `:52-60`, `:62-69`, `:117`, `:121`, `:130-138`, `:168-172`
- [`docs/030-Specs/Architecture/ADR-002-Hosting-Platform-And-Region.md`](../../../../030-Specs/Architecture/ADR-002-Hosting-Platform-And-Region.md) — `:4`, `:15`, `:43-58`, `:60-75`, `:82`, `:84`, `:86`, `:185`, `:189`
- [`docs/030-Specs/Architecture/ADR-003-Auth-And-Billing-Vendor-Selection.md`](../../../../030-Specs/Architecture/ADR-003-Auth-And-Billing-Vendor-Selection.md) — `:4`, `:19`, `:45-55`, `:57-69`, `:71-79`, `:169`, `:173-175`
- [`docs/030-Specs/Architecture/ADR-004-Object-Storage-Vendor-And-Signed-URL.md`](../../../../030-Specs/Architecture/ADR-004-Object-Storage-Vendor-And-Signed-URL.md) — `:4`, `:22`, `:66-75`, `:77-89`, `:167`, `:171-172`
- [`docs/030-Specs/Architecture/SDD-Comic-Studio.md`](../../../../030-Specs/Architecture/SDD-Comic-Studio.md) — `:62`, `:457`, `:811`
- [`docs/030-Specs/Security/Spec-Security-Threat-Model.md`](../../../../030-Specs/Security/Spec-Security-Threat-Model.md) — `:85`, `:292`, `:521`
- [`docs/030-Specs/API/Endpoint-Preview-Export.md`](../../../../030-Specs/API/Endpoint-Preview-Export.md) — `:200`, `:249`
- [`docs/030-Specs/Architecture/ADR-006-RLS-Tenant-Context-Injection.md`](../../../../030-Specs/Architecture/ADR-006-RLS-Tenant-Context-Injection.md) — `:256`, `:258`
- [`docs/030-Specs/Architecture/ADR-015-Job-Queue-In-Postgres.md`](../../../../030-Specs/Architecture/ADR-015-Job-Queue-In-Postgres.md) — `:15`, `:272`
- [`docs/030-Specs/Schema/DB-Entity-Tenancy.md`](../../../../030-Specs/Schema/DB-Entity-Tenancy.md) — `:95`, `:312`
- `docs/010-Planning/pm-runs/2026-08-28-phase-2-architecture-design-comic-studio/escalations.md` — `:181` (`E13`), `:184` (⭐ hai dạng header là **có chủ ý**)
- `docs/000-Index.md:219` — hàng rủi ro số 5, ⛔ **ngoài ownership của em**

---

_Findings by Architect — lô khảo sát READ-ONLY, run `2026-08-30-dong-bo-srs-nfr-voi-adr`_
_Author: trisjr_
