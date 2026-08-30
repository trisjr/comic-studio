---
id: BRD-007
type: brd
status: draft
project: comic-studio
created: 2026-08-24
---

# BRD-007 — Pháp lý & compliance

> [!CAUTION]
> **Đây là BRD chứa rủi ro nhị phân duy nhất của dự án.** Mọi module khác: trả lời sai thì sản phẩm **kém hơn**. Module này: trả lời sai thì sản phẩm **bất hợp pháp hoặc không tồn tại** (CF-7.9 · `Glossary.md` *rủi ro nhị phân*).
>
> ⚠️ **Quy ước ID bắt buộc (CF-10.2 · CẤM-14)**: `GP-1`…`GP-5` là **các hàng compliance** của `MVP-Scope` §3 nhóm G. `G0` / `G1` / `G2` là **tên ba Go/No-Go gate** ở `MVP-Scope` §7. **Cấm viết tắt `G1` cho `GP-1`.** Trộn hai hệ ID này làm câu văn đổi nghĩa hoàn toàn.
>
> ⛔ **Tài liệu này KHÔNG đưa ra ý kiến pháp lý.** Nó **trích và cấu trúc hoá** những gì repo đã ghi, kèm nhãn nguồn nguyên trạng. Chỗ nào repo chưa trả lời được thì ghi `TBD` + câu hỏi phải mang tới luật sư SHTT Việt Nam.

**Quy ước nhãn nguồn** (kế thừa nguyên vẹn — *số và nhãn là một cặp không tách rời*): `[OFF]` official/paper gốc · `[BCN]` báo cáo ngành có tên firm · `[TC]` thứ cấp · `[EM]` ước lượng/phép nhân (**không phải số đo**) · `[CHỐT]` quyết định của Founder tại gate.

## Mục lục

1. [Business goal](#1-business-goal)
2. [Phạm vi module](#2-phạm-vi-module)
3. [Yêu cầu nghiệp vụ](#3-yêu-cầu-nghiệp-vụ)
4. [Ràng buộc & điều kiện chặn](#4-ràng-buộc--điều-kiện-chặn)
5. [Cái module này KHÔNG làm](#5-cái-module-này-không-làm)
6. [Rủi ro chính](#6-rủi-ro-chính)
7. [Tài liệu liên quan](#7-tài-liệu-liên-quan)
8. [Tài liệu tham khảo](#8-tài-liệu-tham-khảo)

---

## 1. Business goal

**Giữ được bảo hộ bản quyền cho tác phẩm của Founder VÀ của khách hàng, và giữ được miễn trừ trung gian.**

Đây là phát biểu mục tiêu lấy nguyên từ [`findings/business-analyst.md`](../../010-Planning/pm-runs/2026-08-24-khoi-tao-requirements-stories-comic-studio/findings/business-analyst.md) §1.1 hàng BRD-007. Ba chữ load-bearing trong đó:

| Chữ | Vì sao nó là chữ quan trọng |
|---|---|
| **VÀ của khách hàng** | Sản phẩm là **SaaS thương mại multi-tenant** (CF-1.1 `[CHỐT]`) — nền tảng cho **người khác** upload truyện **của họ**. Hồ sơ provenance vì thế là bằng chứng phục vụ **khách hàng của Founder** chứng minh quyền của họ, không chỉ của Founder. `MVP-Scope` §4.4: nghĩa vụ này *"không chỉ giữ nguyên — nó MẠNH LÊN dưới SaaS"* |
| **bảo hộ bản quyền** | **NĐ 134/2026/NĐ-CP Điều 5a** `[OFF]`: tác phẩm AI-assisted **chỉ** được bảo hộ nếu con người có *"đóng góp trí tuệ đáng kể và mang tính quyết định"* (`Glossary.md` term *`Generation` / `parent_generation`*) — nguyên văn tiếng Anh trong repo: *"substantial and decisive intellectual contribution to the creative process"* (Analysis §6.4 · CF-7.2 `[OFF]`). **Tác phẩm do AI tạo hoàn toàn: KHÔNG được bảo hộ** |
| **miễn trừ trung gian** | **Điều 198b Luật SHTT** (sửa đổi 2022, Luật 07/2022/QH15 — Analysis §8.3) miễn trừ trách nhiệm cho *"doanh nghiệp cung cấp dịch vụ trung gian"*, nhưng **có điều kiện, không tự động** |

### 1.1 Nguyên tắc xuyên suốt — `NT-2`

> **`MVP-Scope` §2 `NT-2` — Nghĩa vụ pháp lý đặt lên tầng DỮ LIỆU, không đặt lên tầng UI.**
>
> Trích nguyên: *"Yêu cầu 'iterative, interactive process' của bảo hộ bản quyền là yêu cầu về **quyết định sáng tạo của con người có được ghi nhận hay không** — không phải yêu cầu về công nghệ render UI. Một form editor có ghi vết đầy đủ (`change_log`, `field_provenance`, `generation.origin`) thoả nghĩa vụ đó y hệt một canvas editor."*
>
> Hệ quả, nguyên văn: *"**UI được tự do chọn cái rẻ; dữ liệu provenance thì không được cắt một dòng nào.**"*

`NT-2` là **lý do hợp pháp** của quyết định cắt canvas editor (CF-9.1 · `MVP-Scope` §4.1). Nó cũng là lý do BRD-007 gần như không chứa requirement UI: mọi requirement ở đây là requirement về **dữ liệu, quy trình và văn bản pháp lý**.

⛔ **Cảnh báo cắt-lẫn quan trọng nhất của cả repo** — xem chi tiết ở [mục 5.3](#53-d6--cắt-ui-cây-generation-không-cắt-cột-dữ-liệu): `NT-2` **cho phép** cắt UI cây generation (`D6` = `❌` cắt hẳn), nhưng **cấm** cắt cột `parent_generation_id` (`KC-1` = bắt buộc). Gộp nhầm hai thứ này là **mất bảo hộ bản quyền**.

---

## 2. Phạm vi module

Module này bao **năm hàng nhóm `G. Pháp lý & compliance`** của `MVP-Scope` §3. Nhãn từng mốc copy nguyên từ bảng gốc.

**Ký hiệu** (nguyên văn `MVP-Scope` §3): `✅` có đầy đủ · `🟡` có một phần / bản tối thiểu · `⛔` hoãn sang mốc sau · `❌` **cắt hẳn, không có trong Full Scope**.

| # | Hạng mục | MVP0 | MVP1 | MVP2 | MVP3 | MVP4 | Full Scope | Căn cứ (nguyên văn cột *Căn cứ*) |
|---|---|:--:|:--:|:--:|:--:|:--:|:--:|---|
| **GP-1** | `parent_generation_id` + `relation_kind` + `change_log` + `field_provenance` + `generation.origin` | 🟡 ghi tay | ✅ | ✅ | ✅ | ✅ | ✅ | CF-7.3 `[OFF]` — **hồ sơ pháp lý bắt buộc, không backfill được** |
| **GP-2** | Kiểm **opt-out signal Điều 37b** ngay trong bước ingest | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | CF-7.5 `[OFF]` — chi phí ~0, phải nằm ở nơi file user lần đầu vào hệ thống |
| **GP-3** | Checklist safe harbour **Điều 198b**: takedown, đăng ký đầu mối Bộ VHTTDL, SLA **72 giờ** | ❌ | 🟡 | ✅ | ✅ | ✅ | ✅ | CF-7.6 `[OFF]` · CF-8.11a — **trước khi mở cho người ngoài upload** |
| **GP-4** | AI disclosure (Luật TTNT 2025) | ❌ | 🟡 | 🟡 | ✅ | ✅ | ✅ | CF-7.7 `[OFF]` — deadline tuân thủ **~01/03/2027**; ⚠️ hai nguồn mô tả phạm vi **khác nhau** |
| **GP-5** | ToS + user warrant + `ON DELETE CASCADE` + đường hard-delete tenant đã kiểm thử | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | Analysis §5.7 #5 — takedown **sẽ** đến |

### 2.1 Hai ô cần đọc kỹ trước khi lập kế hoạch

| Ô | Điều phải hiểu đúng |
|---|---|
| **`GP-1` = `🟡` ở MVP0, `✅` ở MVP1** | CF-7.3 nói *"không lưu từ generation đầu tiên thì vĩnh viễn không có"*. `MVP-Scope` §3.1 diễn giải *"generation đầu tiên"* theo nghĩa pháp lý = **generation đầu tiên của sản phẩm thật, tức MVP1**, vì MVP0 là spike bị vứt (không có database). ⚠️ `MVP-Scope` §3.1 **tự khai đây là `[EM]` diễn giải của writer run trước, KHÔNG có trong bảng CF** — findings §6.1 `MT-7`. **Giữ nguyên nhãn `[EM]` khi trích.** MVP0 chỉ cần ghi tay ra CSV/file để đủ dữ liệu đo |
| **`GP-4` = `🟡` ở MVP1 và MVP2, `✅` ở MVP3** | Theo quy ước `QC-3` của run này (cờ gán theo **mốc đầu tiên** hạng mục được giao): **MVP1 (`🟡`) — hoàn tất ở MVP3 (NGOÀI HORIZON)**. Deadline tuân thủ **~01/03/2027** nằm **ngay sau** horizon 09/2026–02/2027 (`Charter` §7 `C4`) ⇒ phần `🟡` trong horizon là phần **không được để rơi** |

---

## 3. Yêu cầu nghiệp vụ

**Mọi yêu cầu dưới đây có căn cứ.** Không hàng nào là suy luận mới của tài liệu này. Cột *Mốc MVP* dùng đúng hệ `MVP0 → MVP1 → MVP2 → MVP3 → MVP4` (`Charter` §7 `C9` · CF-8.3 là canon).

| ID | Phát biểu | Căn cứ (file + mục) | Mốc MVP |
|---|---|---|---|
| **BR-007-01** | **Mọi generation phải lưu đủ năm hạng mục provenance**: `parent_generation_id` (nullable FK) + `relation_kind ENUM('retry','variation','refine','continuity_fix')` + `change_log` (ghi **mọi** hành động người dùng, kể cả *"chọn generation X thay vì Y"*) + `field_provenance` (mức field) + `generation.origin ENUM('ai','ai_edited','human')`. Đây là **hồ sơ pháp lý bắt buộc, KHÔNG backfill được** | `MVP-Scope` §3 `GP-1` · §6 `KC-1`, `KC-2`, `KC-3` · §4.4 · CF-7.2 / CF-7.3 `[OFF]` (NĐ **134/2026/NĐ-CP** **Điều 5a**) · `Roadmap` §2 **M1-5** · `Charter` §9.3 **BLOCKER-04** | MVP0 `🟡` ghi tay → **MVP1** `✅` (diễn giải `[EM]`, xem [mục 2.1](#21-hai-ô-cần-đọc-kỹ-trước-khi-lập-kế-hoạch)) |
| **BR-007-02** | **`generation` + `change_log` + `usage_event` phải commit CÙNG MỘT transaction** với artifact mà chúng chứng minh. Đo bằng **một test**, không bằng một màn hình | `MVP-Scope` §6 `KC-4` (*"Bằng chứng có thể thiếu ngẫu nhiên thì không phải bằng chứng"*) · §4.2 lý do 2 · CF-9.2 · `Roadmap` §2 **M1-5** (*"có test chứng minh"*) | **MVP1** |
| **BR-007-03** | **Kiểm opt-out signal Điều 37b ngay tại bước ingest** — đọc metadata / rights-management-info của file user upload, **log kết quả kèm timestamp**, **chặn nếu có signal bảo lưu**. Bốn kênh bảo lưu quyền theo NĐ 134/2026 Điều 37b: metadata · biện pháp bảo vệ công nghệ · thông tin quản lý quyền dạng máy đọc · thông báo công khai từ tổ chức quản lý tập thể. **Chi phí xây ≈ 0, chi phí chạy = 0** | `MVP-Scope` §3 `GP-2` · §6 `KC-6` · CF-7.5 `[OFF]` tóm tắt · Analysis §8.3 item 6 · `Roadmap` §2 **M1-4** (**100%** file upload đi qua bước kiểm) · `Risk-Register` **R-06** | **MVP1** |
| **BR-007-04** | **Checklist safe harbour Điều 198b**: (a) **công cụ tiếp nhận takedown** — form + email `copyright@` (luật cho phép *"chương trình máy tính, email, hoặc cổng thông tin điện tử"*); (b) **đăng ký đầu mối liên hệ (email + số điện thoại) với Bộ Văn hoá, Thể thao và Du lịch**; (c) **SLA 72 giờ** thực hiện bằng **soft-delete + disable-access ở cấp project**, **KHÔNG hard delete** — dữ liệu còn phải giữ cho counter-notice. ⚠️ **Điều kiện thời điểm neo vào TRIGGER, không neo vào ngày**: *trước lần đầu mở cho **NGƯỜI NGOÀI** upload* | `MVP-Scope` §3 `GP-3` · CF-7.6 `[OFF]` tóm tắt · CF-8.11a · Analysis §8.3 checklist item 1–3 · **`Roadmap` §4 việc X-a** (trigger) · `Roadmap` §2 **M2-6** · `Charter` §9.3 **BLOCKER-02** · `Risk-Register` **R-02** | **MVP2** — hoặc **sớm hơn** nếu trigger đến sớm hơn |
| **BR-007-05** | **Phải có cơ chế để người dùng nhận biết khi đang tương tác với hệ thống AI** (Điều 11 — minh bạch, Luật TTNT 2025). Kết hợp ràng buộc positioning **disclosure-first** của `Charter` §7 `C5` | Analysis §8.4 bảng điều khoản (Điều 11) · CF-7.7 `[OFF]` · `Charter` §7 `C5` · `Glossary.md` *disclosure-first positioning* · `Risk-Register` **R-03** | MVP1 `🟡` → hoàn tất **MVP3** (NGOÀI HORIZON) |
| **BR-007-06** | **Nội dung do AI tạo phải được đánh dấu bằng định dạng máy đọc** (khoản 4 Điều 11). Hệ quả kiến trúc, nguyên văn Analysis §8.4: cần **AI provenance metadata field ở cấp page/panel**, và **export path phải nhúng được machine-readable watermark** — *"Đây là requirement, không phải nice-to-have"*. ⚠️ **SynthID** của model provider (đã nhúng sẵn trong Nano Banana Pro) **có thoả nghĩa vụ hay không: `TBD` — phải verify, không giả định**. ⚠️ **Phạm vi thật của nghĩa vụ: `TBD`** — xem [mục 3.1](#31-gp-4--hai-cách-đọc-trong-repo-mâu-thuẫn-về-phạm-vi) | `MVP-Scope` §3 `GP-4` · CF-7.7 `[OFF]` ⚠️ *hai nguồn mô tả phạm vi KHÁC NHAU* · Analysis §8.4 · `Charter` §7 `C4` · `MVP-Scope` §7.1 câu **Q2** · `Risk-Register` **R-03** | MVP1 `🟡` → hoàn tất **MVP3** (NGOÀI HORIZON) · **deadline tuân thủ ~01/03/2027** |
| **BR-007-07** | **ToS phải có ba pattern phòng tuyến hợp đồng** mà **mọi** đối thủ đều có: (1) **user warrant + indemnify** — buộc user cam kết có quyền với truyện họ upload; (2) **assign toàn bộ quyền output cho user** kèm disclaimer về **tính bất định pháp lý theo jurisdiction**; (3) **DMCA designated agent** đăng ký với US Copyright Office — **chỉ khi** nhắm thị trường Mỹ. Checkbox cam kết quyền phải gắn vào **bước upload**, không chỉ ở trang ToS | `MVP-Scope` §3 `GP-5` · Analysis §8.3 (*"Ba pattern ToS nhất quán trong ngành, nên copy"*) · `Risk-Register` **R-05** | **MVP1** |
| **BR-007-08** | **Đường xoá cứng toàn bộ dữ liệu tenant phải tồn tại VÀ đã được kiểm thử** — kỷ luật `ON DELETE CASCADE` trên mọi FK. Đây là đường **tách biệt** với soft-delete của `BR-007-04`. Quyền rút khỏi hệ thống phải là quyền **thực thi được, không phải lời hứa**. Nguyên văn Analysis §5.7 #5: *"FK lỏng thì xoá một tenant biến thành khảo cổ học thủ công, và sót dữ liệu là rủi ro pháp lý"* | `MVP-Scope` §3 `GP-5` · Analysis §5.7 quyết định #5 (*"takedown và yêu cầu xoá dữ liệu **sẽ** đến"*) · Analysis §8.3 checklist item 3 (lý do tách hai đường) · `MVP-Scope` §8.2 | **MVP1** |
| **BR-007-09** | **Khi KILL, phải xuất dữ liệu đầy đủ cho từng tenant — gồm cả `change_log` + `field_provenance`**, vì đó là **hồ sơ chứng minh quyền tác giả của khách**. Kèm: thông báo trước **≥30 ngày** cho mọi tenant đang trả phí; **ngừng thu tiền ngay tại thời điểm thông báo**, không đợi hết chu kỳ | `MVP-Scope` §8.2 (*"nghĩa vụ khi KILL — dừng có trật tự"*, ba mục) · §6 `KC-2`, `KC-3` · §8.1 điều kiện `K1`–`K5` | Nghĩa vụ **có hiệu lực từ khi có tenant trả phí đầu tiên**. Cơ chế export dùng chung với `H4` — thuộc [BRD-008](./BRD-008-Quality-And-Operations.md) |

### 3.1 `GP-4` — hai cách đọc trong repo, mâu thuẫn về phạm vi

> [!WARNING]
> **CF-7.7 `[OFF]` ghi rõ: HAI NGUỒN MÔ TẢ PHẠM VI KHÁC NHAU.** Tài liệu này **không chọn một cách đọc rồi trình bày như sự thật.** Cả hai được ghi ra kèm nhãn mâu thuẫn.

**Văn bản gốc**: `LUẬT TRÍ TUỆ NHÂN TẠO 2025` — **Luật số 134/2025/QH15**, Quốc hội khoá XV Kỳ họp thứ 10 thông qua **10/12/2025**, **hiệu lực 01/03/2026**. Điều 8 chuyển tiếp: hệ thống đang tồn tại có **12 tháng** (lĩnh vực ngoài y tế/giáo dục/tài chính) để tuân thủ ⇒ comic-studio: **deadline ~01/03/2027** (Analysis §8.4 `[OFF]`).

> ⚠️ **Đừng lẫn hai số hiệu `134`**: **NĐ 134/2026/NĐ-CP** (Điều 5a / 37a / 37b, hiệu lực **09/04/2026**, sửa đổi NĐ 17/2023) là văn bản **khác** với **Luật số 134/2025/QH15** (khoản 4 Điều 11, hiệu lực **01/03/2026**). Hai văn bản, hai nghĩa vụ, cùng con số.

| Cách đọc | Phát biểu | Nguồn trong repo | Hệ quả kỹ thuật nếu đúng |
|---|---|---|---|
| **Đọc HẸP** | Nghĩa vụ gắn nhãn dễ nhận biết **chỉ** áp cho nội dung AI tạo/chỉnh sửa nhằm ***"mô phỏng người thật hoặc sự kiện thực tế"*** ⇒ comic với nhân vật **hư cấu** có thể **không** rơi vào phạm vi | Analysis §8.4 bảng *khoản 4 Điều 11*, câu đầu · `Charter` §9.1 câu **2** | Gần như là **một dòng metadata** |
| **Đọc RỘNG** | Nhà cung cấp phải bảo đảm nội dung do hệ thống AI tạo ra được **đánh dấu bằng định dạng máy đọc** theo quy định của Chính phủ — **không** giới hạn ở *"mô phỏng người thật"* ⇒ áp cho **mọi** nội dung AI | Analysis §8.4 bảng *khoản 4 Điều 11*, câu thứ hai · findings §6.1 `MT-6` | Là **một hạng mục kỹ thuật ở export path** + provenance field cấp page/panel |

> ⚠️ **Nhãn mâu thuẫn (findings §6.1 `MT-6`)**: hai mô tả này đến từ **cùng một nguồn** và **có thể mâu thuẫn về phạm vi**; và **không đọc được nguyên văn điều luật** (thuvienphapluat và luatminhkhue đều trả **403** — Analysis §8.4 · findings §6.2 `KT-5`).

**Cách xử lý đã chốt — `Charter` §7 `C4`:**

> *"Vì phạm vi chưa rõ, phải **thiết kế theo diễn giải rộng** (mọi nội dung AI) **cho tới khi luật sư chốt**."*

⇒ `BR-007-06` được viết theo **diễn giải RỘNG**. Phạm vi thật vẫn là **`TBD`**, và nó là **câu Q2 của gate `G0`**:

> **Câu hỏi phải mang tới luật sư SHTT** (nguyên văn `MVP-Scope` §7.1 **Q2**): *"Khoản 4 Điều 11 Luật TTNT 2025 — nghĩa vụ đánh dấu định dạng máy đọc áp cho **mọi** nội dung AI, hay chỉ nội dung *'mô phỏng người thật hoặc sự kiện thực tế'*? Watermark của provider (SynthID) có thoả không?"*

---

## 4. Ràng buộc & điều kiện chặn

### 4.1 `KC-x` — các mục KHÔNG ĐƯỢC CẮT mà module này chạm

`MVP-Scope` §6 là *"danh sách **duy nhất** trong tài liệu này **không mở ra thương lượng scope**"*. Module này chạm **năm trong bảy** mục. Chung một tính chất: **rẻ khi làm từ đầu, không thể sửa về sau**.

| # | Bắt buộc giữ | Từ mốc | Chi phí giữ | Không giữ thì hỏng thế nào (gist nguyên trạng) |
|---|---|---|---|---|
| **KC-1** | `parent_generation_id` (nullable FK) + `relation_kind ENUM(...)` | MVP1 | Hai cột | Tác phẩm của Founder **và của khách hàng** **không được bảo hộ bản quyền ở Việt Nam** (CF-7.2 `[OFF]`). Và **không backfill được** — thêm cột sau thì mọi generation quá khứ có `parent = NULL` **vĩnh viễn** (CF-7.3) |
| **KC-2** | `change_log` ghi **mọi** hành động người dùng — kể cả *"chọn generation X thay vì Y"* | MVP1 | Một bảng append-only | **Prompt một mình không chứng minh được *"decisive contribution"***. Cái chứng minh được là *người đã chọn X thay vì Y, đã sửa thoại, đã đổi camera, đã kéo bubble*. Không có `change_log` ⇒ không có bằng chứng ⇒ **Điều 5a không thoả** |
| **KC-3** | `field_provenance` (mức field) + `generation.origin ENUM('ai','ai_edited','human')` | MVP1 | Một cột enum + một bảng phụ | Không phân biệt được phần nào do người, phần nào do AI ⇒ **không xác định được ranh giới phần được bảo hộ**. Cũng là thứ làm cho **việc cắt canvas hợp pháp** |
| **KC-4** | **Cả ba mục `KC-1`, `KC-2`, `KC-3` phải commit CÙNG MỘT TRANSACTION** với artifact mà chúng chứng minh | MVP1 | Kỷ luật code + monolith 1 DB | *"Bằng chứng có thể thiếu ngẫu nhiên thì không phải bằng chứng."* Audit trail commit tách rời artifact là audit trail **không đáng tin về mặt pháp lý** (CF-9.2 lý do 2) |
| **KC-6** | Kiểm **opt-out signal Điều 37b** ngay trong bước **ingest** | MVP1 | **~0** (CF-7.5 `[OFF]`) | Đây là nơi **duy nhất** file của user lần đầu đi vào hệ thống. Kiểm ở chỗ khác nghĩa là **đã xử lý nội dung có opt-out trước khi biết**. Chi phí bằng 0 mà bỏ qua là lựa chọn **không có lý do nào biện minh** |

**Hai `KC-x` KHÔNG thuộc module này** (ghi ra để không hàng nào trông như bị bỏ rơi): `KC-5` (`tenant_id` + RLS) → [BRD-005](./BRD-005-Multi-Tenancy-And-Platform.md) · `KC-7` (credit ledger + hold + reaper) → [BRD-006](./BRD-006-Credit-And-Unit-Economics.md).

### 4.2 `C-x` — ràng buộc `Charter` §7 mà module này chịu

| # | Ràng buộc | Nhãn | Hệ quả bắt buộc lên module này |
|---|---|---|---|
| **C4** | **Deadline pháp lý ~01/03/2027** — AI disclosure là nghĩa vụ **nội địa Việt Nam** theo Luật TTNT 2025. ⚠️ kèm caveat: **hai nguồn mô tả phạm vi KHÁC NHAU** | `[OFF]` CF-7.7 | Deadline nằm **ngay sau** horizon 09/2026–02/2027 ⇒ **phải thiết kế theo diễn giải RỘNG (mọi nội dung AI) cho tới khi luật sư chốt**. Đây là căn cứ trực tiếp của `BR-007-06` |
| **C5** | **Positioning bắt buộc: disclosure-first, nhắm writer KHÔNG nhắm artist** | phân tích PM CF-5.7, dựa trên `[TC]` CF-5.6 | Kênh cộng đồng là kênh **có rủi ro ngược**. Cấm marketing vào cộng đồng hoạ sĩ. Với module này: disclosure không phải chi phí tuân thủ mà là **ràng buộc phân phối** (`Glossary.md` *disclosure-first positioning*) |
| **C1** | **Đội 1 người + AI assist, không funding** | `[CHỐT]` CF-1.2 | Mọi hạng mục compliance phải **chia được cho một người**. Đây là lý do checklist Điều 198b chọn *form + email `copyright@`* thay vì một hệ thống ticket — luật cho phép (Analysis §8.3 item 1) |
| **C9** | **Thứ tự milestone cố định MVP0 → MVP1 → MVP2 → MVP3 → MVP4** | CF-8.3 | Cột *Mốc MVP* ở [mục 3](#3-yêu-cầu-nghiệp-vụ) dùng đúng hệ này. ⚠️ `findings/architect.md` §7.2 của run trước **đánh số lại** milestone — **CF-8.3 là canon** (CF-10.2) |

### 4.3 Điều kiện chặn — `Charter` §9

> [!IMPORTANT]
> `Charter` §9 có **bốn** điều kiện chặn: **một** ở cấp dự án (§9.1 `BLOCKER-01`) và **ba** điều kiện chặn phụ (§9.3 `BLOCKER-02` / `-03` / `-04`). **Ba trong bốn thuộc nhóm G — tức thuộc BRD này.** Giữ nguyên phân biệt §9.1 vs §9.3, không làm phẳng thành *"ba blocker"*.

| ID | Mục | Điều kiện chặn | Chặn cái gì | Thuộc module này? |
|---|---|---|---|---|
| **BLOCKER-01** | `Charter` §9.1 | **Ba câu hỏi luật sư SHTT (CF-7.8) chưa có câu trả lời bằng văn bản** | **THƯƠNG MẠI HOÁ** — không thu tiền, không mở cho người ngoài upload | ✅ **CÓ** — nhưng là một **hoạt động**, không phải requirement. Xem [mục 5.1](#51-brd-này-không-trả-lời-ba-câu-hỏi-luật-sư) |
| **BLOCKER-02** | `Charter` §9.3 | **Checklist safe harbour Điều 198b chưa hoàn tất** (neo CF-7.6, CF-8.11a) | Chặn việc **mở cho người ngoài upload** (không chặn dùng nội bộ) | ✅ **CÓ** — `GP-3` / `BR-007-04` |
| **BLOCKER-03** | `Charter` §9.3 | **Hard quota cưỡng chế trước khi enqueue chưa có** (neo CF-6.12, CF-8.11b) | Chặn **bản trả phí đầu tiên** | ❌ **KHÔNG** — thuộc `KC-7` / nhóm F ⇒ [BRD-006](./BRD-006-Credit-And-Unit-Economics.md) |
| **BLOCKER-04** | `Charter` §9.3 | **Provenance chain chưa ghi từ generation đầu tiên** (neo `[OFF]` CF-7.3) | Chặn **MỌI THỨ** — vì **không backfill được** | ✅ **CÓ** — `GP-1` / `BR-007-01` |

### 4.4 Ranh giới của `BLOCKER-01` — chống hiểu nhầm đắt nhất

> [!NOTE]
> **`BLOCKER-01` / gate `G0` chặn THƯƠNG MẠI HOÁ, KHÔNG chặn MVP0–MVP1.**
>
> `Charter` §9.2 gọi việc đọc nó thành *"phải chờ luật sư mới được viết dòng code đầu tiên"* là **"cách hiểu nhầm đắt nhất mà tài liệu này có thể gây ra"** (findings §5.3 **CẤM-10**). MVP0 (~$12, 1–2 tuần, dùng nội dung của **chính Founder**) không tạo ra nghĩa vụ mà ba câu hỏi đang hỏi.
>
> Quy tắc quyết định khi **chưa engage luật sư** (`Risk-Register` §3 `RB-01`): **được làm** MVP0 → MVP1 với dữ liệu của chính Founder, xây đủ hồ sơ provenance và checklist 198b · **không được làm**: mở cho **người ngoài** upload; thu **bất kỳ khoản tiền nào**.

**Trạng thái hiện tại: CHƯA ENGAGE luật sư** (`Charter` §9.1).

### 4.5 Ràng buộc về chất lượng nguồn — bắt buộc mang theo

| # | Ràng buộc | Nguồn |
|---|---|---|
| **CẤM-13** | **CẤM viết requirement như thể phạm vi Điều 37a đã rõ** — hiểu biết hiện tại dựa trên **bản tóm tắt, KHÔNG phải nguyên văn** (nguồn gốc trả **403** / **paywall**) | CF-7.4 ⚠️ `[OFF]` **tóm tắt** · findings §6.2 `KT-5` |
| **CẤM-14** | **CẤM lẫn hệ ID `GP-n` (compliance) với `G0`/`G1`/`G2` (gate)** | `MVP-Scope` §3 nhóm G vs §7 · CF-10.2 |
| **CẤM-09** | **CẤM gộp *"cắt UI cây generation (`D6`)"* với *"cắt lineage (`KC-1`)"*.** Hai quyết định **độc lập và trái chiều** | `MVP-Scope` §3.1, §6.1 |
| **CẤM-18** | **CẤM sửa `Analysis-Comic-Studio-Concept.md`** — nó là **dấu vết quyết định tại thời điểm viết**. Tài liệu mới **link sang**, không sửa | `Charter` §10 |

⚠️ **Nhãn nguồn phải mang theo cho cả nhóm**: CF-7.5, CF-7.6 là `[OFF]` **tóm tắt**; CF-7.4 là `[OFF]` **tóm tắt** và **chưa đọc được nguyên văn**. Trích mà bỏ nhãn này làm chúng **mạo danh nguyên văn điều luật**.

---

## 5. Cái module này KHÔNG làm

### 5.1 BRD này KHÔNG trả lời ba câu hỏi luật sư

> [!CAUTION]
> **Ba câu hỏi `Q1` / `Q2` / `Q3` của gate `G0` là một HOẠT ĐỘNG, KHÔNG phải một requirement.** Chúng thuộc `Roadmap` §3.1 **việc 1** (*"Mang ba câu CF-7.8 tới luật sư SHTT Việt Nam"*) và exit criterion `Roadmap` §2 **P-1**.
>
> `Roadmap` §3.1 việc 1 nói thẳng: *"Việc của pre-cycle là **gửi đi và nhận về bằng văn bản** — không phải tự trả lời."*
>
> Lý do không đưa chúng vào backlog dưới dạng requirement/Story, nguyên văn findings §4.7: *"Đó là **hoạt động**, không phải increment sản phẩm. Đưa nó vào backlog là **biến một blocker thành một ticket có thể 'dời sprint sau'**."*

**Ba câu hỏi — trích để mang đi, KHÔNG trả lời tại đây** (`MVP-Scope` §7.1):

| # | Câu hỏi | Trạng thái |
|---|---|---|
| **Q1** | **Điều 37a NĐ 134/2026** có áp cho *inference-time extraction* trên nội dung do user upload, hay chỉ áp cho *huấn luyện* model? | **`TBD`** — ⚠️ điều luật hiện **chỉ đọc được qua bản tóm tắt** (CF-7.4, `KT-5`) |
| **Q2** | **Khoản 4 Điều 11 Luật TTNT 2025** — nghĩa vụ đánh dấu định dạng máy đọc áp cho *mọi* nội dung AI, hay chỉ nội dung *"mô phỏng người thật hoặc sự kiện thực tế"*? **Watermark của provider (SynthID) có thoả không?** | **`TBD`** — hai nguồn mô tả phạm vi khác nhau (xem [mục 3.1](#31-gp-4--hai-cách-đọc-trong-repo-mâu-thuẫn-về-phạm-vi)) |
| **Q3** | Nền tảng có được coi là **"doanh nghiệp cung cấp dịch vụ trung gian"** để hưởng miễn trừ **Điều 198b** không, khi nó không chỉ *lưu trữ* mà còn **xử lý/biến đổi** nội dung của user? | **`TBD`** — `KT-6`: NĐ 17 chỉ nói *"lưu trữ nội dung số theo yêu cầu"*. *"Hosting thuần có safe harbour rõ; 'hosting + processing' là vùng chưa test"* |

**Tiêu chí PASS của `G0` là sự tồn tại của một artifact** (văn bản tư vấn) **+ phân loại nhị phân trên nội dung của nó** (`🟢 CHO PHÉP` / `🟡 CHO PHÉP CÓ ĐIỀU KIỆN` / `🔴 CHẶN`) — *"Không có chỗ nào cho 'cảm thấy ổn'"* (`MVP-Scope` §7.1). BRD này **không** tự chấm ba trạng thái đó.

### 5.2 KHÔNG xây bộ phát hiện bản quyền chủ động — đây là ANTI-FEATURE

> [!WARNING]
> **Nghịch lý safe harbour — điểm phản trực giác nhất của cả bản thẩm định** (Analysis §8.3 · `Risk-Register` **R-04**).
>
> Điều kiện miễn trừ **(a)** của Điều 198b là **"không biết"** nội dung đó xâm phạm quyền. Nghĩa là **xây một bộ phát hiện *"truyện này có thể có bản quyền của người khác"* có thể PHÁ chính miễn trừ của mình** — vì nó **tạo ra đúng tri thức mà luật đang miễn trừ cho việc không có**.
>
> *"Một dev sẽ làm ngược điều này theo bản năng, vì 'chủ động kiểm tra' nghe như hành vi có trách nhiệm."*

**Cấm tường minh**: không backlog item / issue / PR mang tên kiểu `copyright detection`, `plagiarism check`, `flag nội dung khả nghi`, `similarity scan` — **trước khi** có xác nhận của luật sư (`Risk-Register` **R-04** cột *Dấu hiệu sớm*).

**Phân biệt rõ với việc ĐƯỢC PHÉP** (`BR-007-03`): đọc **opt-out signal do chính chủ quyền gắn vào file** là **dữ kiện khách quan**, không phải tri thức suy đoán. Nguyên văn Analysis §8.3: *"Đọc nhãn không tạo ra tri thức suy đoán."*

**Điều kiện mở lại**: luật sư xác nhận ranh giới giữa *"đọc nhãn"* và *"suy đoán"* — hiện là khoảng trống mở (`Risk-Register` **R-04** cột *Rủi ro còn lại*).

### 5.3 `D6` — cắt UI cây generation, KHÔNG cắt cột dữ liệu

> [!CAUTION]
> **Đây là bẫy cắt-lẫn quan trọng nhất của cả repo. Viết ra thành văn để không ai gộp nhầm.**
>
> | Thứ | Trạng thái | Nguồn |
> |---|---|---|
> | **UI duyệt cây generation** (`D6`: tree view / diff / branch-merge) | **`❌` CẮT HẲN** ở mọi mốc, kể cả Full Scope | `MVP-Scope` §3 hàng `D6` · Analysis §6.3–6.4 |
> | **Cột dữ liệu `parent_generation_id`** (+ `relation_kind`) | **BẮT BUỘC** — `KC-1`, không mở ra thương lượng | `MVP-Scope` §6 `KC-1` · §3 `GP-1` |
>
> **Cắt UI, KHÔNG cắt cột dữ liệu.** `MVP-Scope` §3.1 gọi đây là cặp *"rất dễ bị gộp làm một khi cắt scope — và gộp nhầm thì **mất bảo hộ bản quyền**"*. `MVP-Scope` §6.1 xếp *"cắt UI cây generation nghĩa là cắt lineage"* vào **ba hiểu nhầm hay gặp**, và trả lời: *"**Không.** Cắt UI (`D6` = `❌`), giữ nguyên dữ liệu (`KC-1` = bắt buộc). Đây là hai quyết định **độc lập và trái chiều**."*
>
> Đây chính là `NT-2` đang vận hành. Thay thế cho tree view: **flat list theo `created_at` + `approved_generation_id`** — *"đủ 95% giá trị"* (Analysis §6.3).

**Hệ quả**: BRD-007 **không** chứa requirement UI cho lineage, và **không** sinh Use Case `UC-Review-Generation-Tree` (findings §3.3). Nhưng `BR-007-01` **vẫn là requirement cứng**. **Không mở lại `D6`.**

### 5.4 KHÔNG đưa ra diễn giải pháp lý mới

Tài liệu này **trích và cấu trúc hoá**. Nó **không**:

- chọn một trong hai cách đọc `GP-4` rồi trình bày như sự thật (xem [mục 3.1](#31-gp-4--hai-cách-đọc-trong-repo-mâu-thuẫn-về-phạm-vi));
- khẳng định Điều 37a có/không áp cho comic-studio (**CẤM-13** — hiểu biết dựa trên **bản tóm tắt**);
- khẳng định SaaS *xử lý/biến đổi* nội dung có được coi là *"dịch vụ trung gian"* (`KT-6`);
- khẳng định SynthID thoả hay không thoả nghĩa vụ đánh dấu (*"phải verify, không giả định"* — Analysis §8.4);
- tự tra lại hoặc tự tính lại con số nào đã có trong bảng CF (**CẤM-15**).

Mọi chỗ trên đứng ở trạng thái **`TBD`** kèm câu hỏi tương ứng ở [mục 5.1](#51-brd-này-không-trả-lời-ba-câu-hỏi-luật-sư).

### 5.5 KHÔNG thuộc module này

| Hạng mục | Thuộc về | Vì sao dễ bị gán sai vào đây |
|---|---|---|
| `tenant_id` + Postgres RLS + object storage tách tenant (`E1`, `E3`, `KC-5`) | [BRD-005](./BRD-005-Multi-Tenancy-And-Platform.md) | **KHÔNG dedup chéo tenant** có lập luận bản quyền (Analysis §5.7 #4: dedup chéo *"mâu thuẫn trực tiếp với chính lập luận bản quyền"*) ⇒ nghe như compliance, nhưng cơ chế và effort nằm ở nhóm E |
| Credit ledger + hold + hard quota (`KC-7`, `BLOCKER-03`) | [BRD-006](./BRD-006-Credit-And-Unit-Economics.md) | `BLOCKER-03` nằm cùng `Charter` §9.3 với hai blocker của nhóm này |
| Editor tối thiểu 5 thành phần — nơi `change_log` **được sinh ra** | [BRD-004](./BRD-004-Minimum-Editor.md) | `KC-2` yêu cầu ghi *mọi* hành động editor. BRD-007 sở hữu **nghĩa vụ**; BRD-004 sở hữu **hành động sinh ra dữ liệu** |
| Export PDF / CBZ / webtoon (`H4`) — cơ chế của `BR-007-09` và của watermark ở export path | [BRD-008](./BRD-008-Quality-And-Operations.md) | Nghĩa vụ pháp lý dùng **chung** đường export, nhưng đường export là hạng mục nhóm H |
| Abuse controls tối thiểu (`H5`) | [BRD-008](./BRD-008-Quality-And-Operations.md) | `Roadmap` §4 việc `X-b` lưu ý: *"abuse control cho upload thì cần ngay ở MVP1"* — trông như tiền đề của safe harbour, nhưng là hàng nhóm H |

---

## 6. Rủi ro chính

**Sổ rủi ro đầy đủ: [`Risk-Register.md`](../../010-Planning/Risk-Register.md).** Mục này **chỉ trỏ**, **không tự chấm điểm rủi ro mới** — thêm một Score ở đây là tạo ra một hệ đánh giá thứ hai không ai bảo trì.

### 6.1 Rủi ro nhị phân — KHÔNG nằm chung thang Probability × Impact

> [!CAUTION]
> **`RB-01` không phải một hàng trong bảng `Risk-Register` §2, và cố ý KHÔNG có Score.**
>
> `Glossary.md` term *rủi ro nhị phân*: *"Rủi ro mà trả lời sai không làm sản phẩm **kém hơn** mà làm nó **bất hợp pháp hoặc không tồn tại**. Nó **không nằm chung thang Probability × Impact** với rủi ro thường, **vì thang đó giả định hậu quả liên tục**."*
>
> `Risk-Register` §1.3 điểm 3 và §3, nguyên văn: *"Nhân một xác suất **chưa ai biết** với một impact **không phải 'làm lại một phần' mà là 'không tồn tại'** cho ra một con số trông giống dữ liệu nhưng không mang thông tin."* Và: *"Một rủi ro nhị phân chưa kiểm **luôn phải xếp trên mọi rủi ro liên tục**, bất kể Score của chúng là bao nhiêu."*

⇒ **Cấm** so `RB-01` với `R-01`…`R-23` bằng phép so Score. Thang `Probability × Impact` của `Risk-Register` §1.1 định nghĩa `Impact = 3` là *"chặn ra mắt hoặc đe doạ sự tồn tại"* — thang **kết thúc** ở đó, nên nó không biểu diễn được *"sản phẩm không được phép tồn tại"*.

| Rủi ro | Nội dung (gist) | Score | Trạng thái |
|---|---|---|---|
| **[`RB-01`](../../010-Planning/Risk-Register.md#3-rủi-ro-nhị-phân--tách-riêng)** | Ba câu hỏi `Q1`/`Q2`/`Q3` phải mang tới luật sư SHTT Việt Nam **TRƯỚC khi thương mại hoá** | **cố ý KHÔNG có Score** | `Charter` §9.1 — **CHƯA ENGAGE luật sư** |

### 6.2 Sáu rủi ro pháp lý đã được Score — trỏ sang `Risk-Register` §2.1

Không lặp lại nội dung, không sửa Score. Cột *Owner* copy nguyên trạng.

| ID | Gist | Score (nguyên trạng) | Trạng thái | Owner | Ràng buộc / requirement tương ứng |
|---|---|:--:|---|---|---|
| **`R-01`** | Không lưu provenance từ generation **ĐẦU TIÊN** ⇒ mất bảo hộ bản quyền và **KHÔNG BACKFILL ĐƯỢC** | **9** | open | `architect` | `KC-1`–`KC-4` · `BR-007-01`, `BR-007-02` · `BLOCKER-04` |
| **`R-02`** | Safe harbour Điều 198b chưa đủ điều kiện (chưa có công cụ takedown, chưa đăng ký đầu mối, chưa có quy trình SLA 72 giờ) | **6** | open | **`security-auditor`** | `GP-3` · `BR-007-04` · `BLOCKER-02` |
| **`R-03`** | Deadline Luật TTNT 2025 **~01/03/2027** rơi **ngay sau** horizon; ⚠️ hai nguồn mô tả phạm vi khác nhau | **6** | open | **`security-auditor`** | `GP-4` · `BR-007-05`, `BR-007-06` · `C4` |
| **`R-04`** | **Nghịch lý safe harbour** — build bộ phát hiện bản quyền **PHÁ** chính miễn trừ Điều 198b | **6** | open | **`security-auditor`** | anti-feature ở [mục 5.2](#52-không-xây-bộ-phát-hiện-bản-quyền-chủ-động--đây-là-anti-feature) |
| **`R-05`** | ToS thiếu ba pattern phòng tuyến hợp đồng mà **mọi** đối thủ đều có | **4** | open | `business-analyst` | `GP-5` · `BR-007-07` |
| **`R-06`** | Điều 37b (opt-out) không được kiểm trong bước ingest ⇒ *"một vi phạm đã xảy ra hàng nghìn lần, không sửa hồi tố được"* | **4** | open | `architect` | `KC-6` · `BR-007-03` |

> ⚠️ **Ghi chú về `R-01` (Score 9 = *Nghiêm trọng*)**: `Risk-Register` §1.2 định nghĩa mức này là *"**chặn công việc khác** cho tới khi hạ được"*. Đây là rủi ro **duy nhất** của cả sổ có Score 9, và nó nằm trong module này. Cột *Rủi ro còn lại* của nó ghi: **"Không có đường lùi."**

### 6.3 Khoảng trống — cố ý KHÔNG gán Score

`Risk-Register` §1.3 điểm 3: gán một Score cho thứ *"chưa đo được"* là **biến "không biết" thành "đã đánh giá"**, và đó là *"loại sai tệ nhất trong một tài liệu rủi ro"*.

| Khoảng trống | Chặn cái gì | Nguồn xác nhận |
|---|---|---|
| **`KT-5`** — **nguyên văn Điều 37a / 37b / 37c NĐ 134/2026** chưa đọc được: cov.gov.vn chỉ có bản giới thiệu; thuvienphapluat + nhansu **403**; IAPP **paywall** | Độ chắc chắn của `BR-007-03` và của câu `Q1` | findings §6.2 `KT-5` · CF-7.4 · Analysis §11 điểm 6 |
| **`KT-6`** — Điều 198b có áp cho SaaS **xử lý/biến đổi** nội dung (không phải hosting thuần) hay không | `BR-007-04` và câu `Q3` | findings §6.2 `KT-6` · Analysis §11 điểm 9 |
| **Phạm vi khoản 4 Điều 11** — hai cách đọc, không phân xử được trong repo | `BR-007-06` và câu `Q2` | findings §6.1 `MT-6` · CF-7.7 `[OFF]` |
| **SynthID có thoả nghĩa vụ đánh dấu hay không** | Chi phí thật của `BR-007-06`: *một dòng metadata* vs *một hạng mục kỹ thuật ở export path* | Analysis §8.4 (*"Phải verify, không giả định"*) · `Risk-Register` **R-03** |

---

## 7. Tài liệu liên quan

### 7.1 Traceability tầng requirement

| Quan hệ | Tài liệu |
|---|---|
| **Chi tiết hoá** | [PRD-Comic-Studio](../PRD-Comic-Studio.md) — mục *Yêu cầu chức năng theo 8 module*, nhóm **G. Pháp lý & compliance** |
| **Yêu cầu phi chức năng** | [SRS-Comic-Studio](../SRS-Comic-Studio.md) — NFR compliance |
| **Epic tương ứng** | [Epic-Legal-And-Compliance](../../022-User-Stories/Epics/Epic-Legal-And-Compliance.md) — 6 Story trong horizon / 0 ngoài (findings §4.7) |

### 7.2 Use Case liên quan

| UC | Vai trò với module này |
|---|---|
| [UC-01 — Upload And Ingest Chapter](../Use-Cases/UC-01-Upload-And-Ingest-Chapter.md) | Nơi `BR-007-03` (opt-out Điều 37b) sống — **bước ingest là nơi DUY NHẤT file của user lần đầu vào hệ thống**. Cũng là nơi gắn checkbox user warrant của `BR-007-07` |
| [UC-11 — Handle Takedown Request](../Use-Cases/UC-11-Handle-Takedown-Request.md) | Luồng của `BR-007-04`. **Primary actor là chủ sở hữu quyền — một actor NGOÀI hệ thống** (findings §3.1: *"Nghĩa vụ pháp lý có actor NGOÀI hệ thống thì phải có UC riêng"*) |

### 7.3 Module liên quan trong cùng tầng BRD

[BRD-004 — Minimum Editor](./BRD-004-Minimum-Editor.md) (sinh `change_log`) · [BRD-005 — Multi-Tenancy And Platform](./BRD-005-Multi-Tenancy-And-Platform.md) (`KC-5`) · [BRD-006 — Credit And Unit Economics](./BRD-006-Credit-And-Unit-Economics.md) (`KC-7`, `BLOCKER-03`) · [BRD-008 — Quality And Operations](./BRD-008-Quality-And-Operations.md) (export path, abuse controls).

---

## 8. Tài liệu tham khảo

### 8.1 Tài liệu trong repo

| Tài liệu | Dùng cho mục nào |
|---|---|
| [MVP-Scope.md](../../010-Planning/MVP-Scope.md) | §3 nhóm G (`GP-1`…`GP-5`) → [mục 2](#2-phạm-vi-module) · §2 `NT-2` → [mục 1.1](#11-nguyên-tắc-xuyên-suốt--nt-2) · §4.4 (tự thu hồi `parent_generation`) → [mục 5.3](#53-d6--cắt-ui-cây-generation-không-cắt-cột-dữ-liệu) · §6 `KC-1`…`KC-4`, `KC-6` + §6.1 → [mục 4.1](#41-kc-x--các-mục-không-được-cắt-mà-module-này-chạm) · §7.0–§7.1 gate `G0` → [mục 5.1](#51-brd-này-không-trả-lời-ba-câu-hỏi-luật-sư) · §8.1 `K1` + §8.2 → `BR-007-09` |
| [Charter-Comic-Studio.md](../../010-Planning/Charter-Comic-Studio.md) | §7 `C1`, `C4`, `C5`, `C9` → [mục 4.2](#42-c-x--ràng-buộc-charter-7-mà-module-này-chịu) · §9.1 `BLOCKER-01` · §9.2 ranh giới · §9.3 `BLOCKER-02`/`-03`/`-04` → [mục 4.3](#43-điều-kiện-chặn--charter-9) |
| [Roadmap.md](../../010-Planning/Roadmap.md) | §2 exit criteria `P-1`, `M1-4`, `M1-5`, `M2-6` → cột *Căn cứ* [mục 3](#3-yêu-cầu-nghiệp-vụ) · §3.1 việc 1 → [mục 5.1](#51-brd-này-không-trả-lời-ba-câu-hỏi-luật-sư) · §4 việc `X-a` (trigger, không phải ngày) → `BR-007-04` |
| [Risk-Register.md](../../010-Planning/Risk-Register.md) | §1.1–§1.3 thang và giới hạn của thang · §2.1 `R-01`…`R-06` · §3 `RB-01` → [mục 6](#6-rủi-ro-chính) |
| [Analysis-Comic-Studio-Concept.md](../../050-Research/Analysis-Comic-Studio-Concept.md) | §5.7 #4, #5 · §6.3–6.4 · §8.3 checklist Điều 198b + nghịch lý safe harbour + ba pattern ToS · §8.4 Luật TTNT 2025 · §8.5 ba câu luật sư. ⛔ **CẤM-18 — không sửa file này** |
| [Glossary.md](../../999-Resources/Glossary.md) | Term *`Generation` / `parent_generation`* · *`field_provenance` / `change_log`* · *rủi ro nhị phân* · *Go/No-Go gate* · *disclosure-first positioning* |
| [findings/business-analyst.md](../../010-Planning/pm-runs/2026-08-24-khoi-tao-requirements-stories-comic-studio/findings/business-analyst.md) | §1.1 hàng BRD-007 (business goal) · §1.3 hàng `D6` · §3.2 UC-01/UC-11 · §4.7 sáu Story · §5.2 CF-7.1→7.9, CF-8.11a, CF-9.1, CF-10.2 · §5.3 CẤM-09/10/13/14/15/18 · §6.1 `MT-6`, `MT-7` · §6.2 `KT-5`, `KT-6` |
| [Documents-Template.md](../../../knowledge-base/99-Templates/Documents-Template.md) | `RULE-001` — thư mục `docs/020-Requirements/BRD/`, naming `BRD-{NNN}-{Title}.md`, frontmatter, **standard markdown link** (quy tắc #5) |

### 8.2 Văn bản pháp luật được dẫn — QUA repo, không tra lại

> ⛔ **Mọi số hiệu, ngày và tên cơ quan dưới đây trích nguyên văn từ tài liệu trong repo.** Tài liệu này **không tra nguồn ngoài** và **không tự tính lại** (**CẤM-15**). Nguồn ngoài gốc nằm ở `Analysis-Comic-Studio-Concept.md` mục *Tài liệu tham khảo → Pháp lý*.

| Văn bản | Điều khoản dùng ở đây | Mốc thời gian (nguyên trạng) | Nhãn |
|---|---|---|---|
| **Nghị định 134/2026/NĐ-CP** (sửa đổi/bổ sung NĐ 17/2023/NĐ-CP hướng dẫn Luật SHTT) | **Điều 5a** (bảo hộ tác phẩm AI-assisted + nghĩa vụ lưu **prompts, inputs, intermediate drafts**) · **Điều 37a** (TDM) · **Điều 37b** (opt-out) | ban hành **06/04/2026**, **hiệu lực 09/04/2026** | `[OFF]` — ⚠️ **Điều 37a/37b chỉ đọc được qua BẢN TÓM TẮT** (CF-7.4, `KT-5`) |
| **Luật SHTT sửa đổi 2022 — Luật 07/2022/QH15** | **Điều 198b** (miễn trừ trách nhiệm cho doanh nghiệp cung cấp dịch vụ trung gian; chuyển hoá từ **Điều 12.55 EVFTA**) | — | `[OFF]` tóm tắt (CF-7.6) |
| **LUẬT TRÍ TUỆ NHÂN TẠO 2025 — Luật số 134/2025/QH15** | **Điều 11** (minh bạch) · **khoản 4 Điều 11** (gắn nhãn + đánh dấu định dạng máy đọc) · **Điều 8** (chuyển tiếp **12 tháng**) | thông qua **10/12/2025**, **hiệu lực 01/03/2026** ⇒ deadline tuân thủ của comic-studio **~01/03/2027** | `[OFF]` — ⚠️ **hai nguồn mô tả phạm vi khoản 4 Điều 11 KHÁC NHAU** |
| **Nghị định 17/2023/NĐ-CP** | Nghĩa vụ notice-and-takedown; đầu mối liên hệ với **Bộ Văn hoá, Thể thao và Du lịch** | — | `[OFF]` tóm tắt qua Analysis §8.3 |

---

_Generated by Comic Studio — role `security-auditor`._
_Author: trisjr_
