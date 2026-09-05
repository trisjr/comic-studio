---
id: ROADMAP-001
type: roadmap
status: draft
created: 2026-02-04
updated: 2026-08-23
---

# Product Roadmap — comic-studio

> [!IMPORTANT]
> **Quy ước nhãn nguồn số liệu** (kế thừa nguyên vẹn từ bảng Canonical Facts):
> `[OFF]` nguồn official/paper gốc · `[BCN]` báo cáo ngành có tên firm · `[TC]` nguồn thứ cấp · `[EM]` ước lượng, **không phải số đo** · `[CHỐT]` quyết định của founder tại gate.
>
> Tài liệu này trả lời *"khi nào và theo thứ tự nào"*. Nó **không** trả lời *"cái gì vào MVP"* — đó là [MVP-Scope.md](./MVP-Scope.md). Ba gate **G0 / G1 / G2** dùng trong tài liệu này được **định nghĩa tại [MVP-Scope.md mục 7](./MVP-Scope.md#7-gono-go-decision)**; ở đây chỉ tham chiếu, không định nghĩa lại.

## Mục lục

1. [Khung thời gian & giả định](#1-khung-thời-gian--giả-định)
2. [Bảng lộ trình tổng](#2-bảng-lộ-trình-tổng)
3. [Chi tiết từng mốc](#3-chi-tiết-từng-mốc)
4. [Ba việc xen ngang](#4-ba-việc-xen-ngang)
5. [Ngoài horizon](#5-ngoài-horizon)
6. [Phụ thuộc & đường găng](#6-phụ-thuộc--đường-găng)
7. [Tài liệu tham khảo](#7-tài-liệu-tham-khảo)

---

## 1. Khung thời gian & giả định

### 1.1 Horizon

| | |
|---|---|
| **Horizon** | **09/2026 → 02/2027** (6 tháng) `[CHỐT]` CF-8.1 |
| **Chu kỳ OKR** | **Q4/2026** (10–12/2026) là chu kỳ chính + **preview Q1/2027**. Tháng **09/2026 là pre-cycle**, đo bằng **gate** không bằng OKR `[CHỐT]` CF-8.2 |
| **Nguồn lực** | **1 người + AI assist.** Không funding, không ngân sách marketing `[CHỐT]` CF-1.2 |
| **Điểm xuất phát** | **Chưa có dòng code nào** — `src/`, `test/`, `openspec/changes/` đều rỗng `[OFF]` CF-1.3 |
| **Thứ tự milestone** | **MVP0 → MVP1 → MVP2 → MVP3 → MVP4**, cố định `[CHỐT]` CF-8.3 |

### 1.2 ⚠️ CF-8.13 — trả lời tường minh trước khi anh đọc bất cứ dòng nào phía dưới

> [!CAUTION]
> **CF-8.13**: *"Chưa ai xác nhận 6 tháng đủ cho 1 dev. Writer Roadmap **BẮT BUỘC** nêu rõ nếu khung 09/2026–02/2027 không chứa hết MVP0–MVP3, và nói thẳng cái gì rơi ra ngoài. **Cấm nén lịch cho vừa khung.**"*

**Câu trả lời: KHÔNG. Khung 09/2026–02/2027 KHÔNG chứa hết MVP0–MVP3.**

| | Nội dung |
|---|---|
| **Chứa được trong horizon** | **MVP0** (09/2026) · **MVP1** (10–12/2026) · **MVP2** (01–02/2027) |
| **Rơi ra ngoài horizon** | **MVP3** (Visual Generation ở quy mô sản xuất) · **MVP4** (Production System) · **mọi gói trả phí CÓ image gen** (Tầng 2 và Tầng 3, CF-2.3/2.4) |
| **Nhãn của kết luận này** | `[EM]` — **ước lượng của em tại run này.** Không có nguồn nào trong bảng CF xác nhận nó |

**Bốn bước lập luận, để anh kiểm tra được từng bước thay vì phải tin kết luận:**

**Bước 1 — Nói thẳng điều mà số học KHÔNG cho phép kết luận.** Trong toàn bộ bảng Canonical Facts, **chỉ có ĐÚNG MỘT thời lượng tuyệt đối**: MVP0 = **1–2 tuần** (CF-8.4). Mọi ước lượng effort còn lại — CF-6.7 **~20–25%** `[EM]`, CF-6.8 **50–60%** `[EM]`, CF-6.9 **15–25%** `[EM]` — đều là **tỉ lệ phần trăm không có mẫu số tính bằng person-month**. Vì vậy câu hỏi *"6 tháng có đủ không"* **không thể được trả lời bằng phép tính** từ dữ liệu hiện có. Một ước lượng bottom-up theo tuần-người cho MVP1/MVP2/MVP3 hiện là **`TBD`** — chưa ai làm, và tài liệu này không bịa ra nó.

**Bước 2 — Ràng buộc lịch cứng do chính gate sinh ra.** [Gate G2](./MVP-Scope.md#73-g2--gate-kinh-tế-sau-mvp1) được chốt ở **cuối Q4/2026, sau MVP1**. Điều đó **buộc MVP1 phải kết thúc trước 31/12/2026**. Vậy 10–12/2026 (3 tháng) là của MVP1, và **chỉ còn 01–02/2027 (2 tháng)** cho *cả* MVP2 *và* MVP3.

**Bước 3 — Khối lượng của ba khối lớn nhất.** Cộng hai con số nằm trong CF, **cùng mẫu số SaaS**:

| Khối | Effort | Nhãn |
|---|---|---|
| Editor tối thiểu | **20–25%** | `[EM]` CF-6.7 (mẫu số SaaS) |
| Multi-tenancy | **15–25%** | `[EM]` CF-6.9 |
| **Tổng hai khối** | **35–50%** | `[EM]` ⚠️ **phép cộng của em** — theo quy tắc CF #3, kết quả của một phép tính trên số CF phải mang nhãn `[EM]` |
| Pipeline lõi (story → panel → generate → composite), *tham chiếu bổ trợ* | **35–45%** | `[EM]` ước lượng của lens kiến trúc, [Analysis §5.7](../050-Research/Analysis-Comic-Studio-Concept.md) — ⚠️ **con số này KHÔNG có trong bảng CF**, dẫn trực tiếp từ nguồn |
| **Tổng ba khối** | **70–95%** | `[EM]` phép cộng của em |

Ba khối này trải từ MVP1 đến MVP3, và **MVP3 gánh phần lớn của khối pipeline lõi**. Chúng chiếm gần **toàn bộ** ngân sách effort của sản phẩm — phần còn lại (**5–30%** `[EM]`) phải đủ cho compliance, billing, export, vận hành và eval kit.

**Bước 4 — Kết luận.** Hai tháng (01–02/2027) cho **MVP2** — Comic Director tự động, rubric layout, `text_safe_zone`, cứng hoá ≤3 nhân vật/panel, **hai human gate bắt buộc** (CF-8.8) — đã là một lịch chật. Nhét thêm **MVP3** vào cùng hai tháng đó chính là hành vi mà CF-8.13 gọi tên: **nén lịch cho vừa khung**. Tài liệu này **không làm điều đó**. MVP3 bắt đầu từ **03/2027**, nằm ngoài horizon.

### 1.3 Điều KHÔNG chắc chắn ngay bên trong phần "chứa được"

Nói rõ để anh không đọc bảng mục 2 như một lời hứa:

| Rủi ro lịch | Nội dung | Hệ quả nếu xảy ra |
|---|---|---|
| **MVP1 có thể tràn khỏi Q4/2026** | MVP1 gánh **toàn bộ** khối multi-tenancy **15–25%** `[EM]` (CF-6.9) — khối mà `Request.md` gốc **không nhắc một dòng** — cộng Story Intelligence, provenance đầy đủ, HITL gate và eval kit. Ba tháng cho ngần đó việc với 1 dev là **giả định, không phải ước lượng** | MVP1 trượt ⇒ **G2 trượt theo** ⇒ MVP2 bị đẩy hết ra ngoài horizon, và horizon chỉ còn chứa MVP0 + MVP1 |
| **Không có ước lượng bottom-up** | `TBD` — chưa có WBS hay ETA cho MVP1/MVP2/MVP3 | Mọi con số lịch ở mục 2 là **phân bổ (allocation)**, không phải **ước lượng (estimate)**. Đây là hai thứ khác nhau và bảng mục 2 ghi rõ cột nào là cái nào |
| **Hệ số AI assist chưa biết** | Không có dữ liệu nào trong CF về việc AI assist rút ngắn được bao nhiêu % thời gian của 1 dev cho **loại công việc này** | `TBD`. Không được dùng "có AI nên nhanh hơn" làm lý do rút ngắn lịch |

### 1.4 Giả định của lộ trình — mỗi cái kèm "sai thì hỏng ở đâu"

| # | Giả định | Nhãn | Sai thì hỏng ở đâu |
|---|---|---|---|
| A1 | Horizon 09/2026–02/2027 | `[CHỐT]` CF-8.1 | Nếu horizon co lại, thứ rơi ra đầu tiên là MVP2, không phải MVP1 |
| A2 | Q4/2026 là chu kỳ OKR chính; 09/2026 đo bằng gate | `[CHỐT]` CF-8.2 | Nếu đo pre-cycle bằng OKR, MVP0 sẽ bị tính là "chậm" trong khi nó đang làm đúng việc: **mua thông tin** |
| A3 | MVP0 chi ~**$12** ở giá standard **$0.134**/ảnh (~**$6** nếu batch) — **lấy số cao làm trần an toàn** vì cần vòng lặp nhanh nên batch khó dùng | `[EM tính từ OFF]` CF-3.11 | Lập ngân sách theo số thấp rồi phát hiện batch không dùng được ⇒ hết tiền giữa vòng lặp. Trần thực tế lên tới ~$50 nếu lặp nhiều vòng (Analysis §10) |
| A4 | Rủi ro kỹ thuật của MVP1–MVP2 **thấp hơn** MVP3, vì Story Bible extraction và Comic IR đều ✅ đã giải được | Analysis §4.2 | Nếu extraction không đạt trên truyện tiếng Việt scrape thật, MVP1 phồng lên và đẩy mọi thứ phía sau |
| A5 | Không có dev thứ hai xuất hiện trong horizon | `[CHỐT]` CF-1.2 | Bus factor = 1 — xem [MVP-Scope K5](./MVP-Scope.md#8-điều-kiện-thoát-kill-criteria) |

---

## 2. Bảng lộ trình tổng

> [!NOTE]
> **Cột *Khoảng thời gian* là PHÂN BỔ, không phải ƯỚC LƯỢNG.** Chỉ MVP0 có thời lượng đến từ nguồn (**1–2 tuần**, CF-8.4). Các mốc còn lại được **cấp** một khoảng thời gian theo ràng buộc gate, chưa được **ước lượng bottom-up** — xem [mục 1.3](#13-điều-không-chắc-chắn-ngay-bên-trong-phần-chứa-được).

| Mốc | Khoảng thời gian | Mục tiêu | Deliverable | **Điều kiện ra (exit criteria)** | Effort ước tính |
|---|---|---|---|---|---|
| **Pre-cycle 09/2026** | 09/2026 (~4 tuần) · MVP0 chiếm **1–2 tuần** (CF-8.4) | **Mua thông tin, không xây sản phẩm.** Biết tiền đề còn đứng hay không, và biết luật có chặn hay không | (1) Hồ sơ 3 câu hỏi gửi luật sư SHTT · (2) MVP0 chạy được: 1 chapter, ~8–30 panel, trang composite **có speech bubble** · (3) Schema draft: khoá thời gian mới + danh sách phải-có-từ-ngày-đầu · (4) Golden dataset 15–20 panel | **P-1** 3/3 câu CF-7.8 đã gửi tới **một luật sư SHTT VN có tên**, có xác nhận đã nhận · **P-2** [G1](./MVP-Scope.md#72-g1--gate-kỹ-thuật-sau-mvp0) có **SỐ cho cả 5 tiêu chí** và verdict được ghi (PASS / PASS CÓ ĐIỀU KIỆN / FAIL) · **P-3** regen ratio **p50 và p90** có giá trị số · **P-4** khoá thời gian thay `(chapter, scene)` được viết ra dưới dạng schema draft · **P-5** danh sách phải-có-trong-schema chốt = **7 mục KC-1…KC-7** của [MVP-Scope mục 6](./MVP-Scope.md#6-không-được-cắt--danh-sách-cứng) · **P-6** golden dataset tồn tại dưới dạng file (spec + ref + ảnh + bảng chấm) | **1–2 tuần** (CF-8.4) + thời gian chờ luật sư (`TBD`, không do em kiểm soát) |
| **MVP1 — Story Intelligence** | 10/2026 – 12/2026 (~3 tháng) | Sản phẩm thật **có nền dữ liệu đúng ngay từ commit đầu**: multi-tenant, có provenance, có eval | Monolith chạy được: ingest → text clean → extraction → timeline state → Story Bible editor. `tenant_id` + RLS. Provenance đầy đủ. HITL gate + eval kit. `usage_event` + `usage_daily` | **M1-1** `tenant_id NOT NULL` trên **100%** bảng nghiệp vụ; RLS policy bật trên **100%** bảng có `tenant_id`; **test rò rỉ chéo tenant PASS** (query của tenant A không trả về 1 row nào của tenant B) · **M1-2** pipeline ingest có **bước text clean là bước ĐẦU TIÊN**, chạy được trên ≥1 chapter scrape thật · **M1-3** extraction đạt **≥80%** entity (nhân vật + địa điểm) khớp với Story Bible viết tay của MVP0 — ⚠️ ngưỡng 80% là `[EM]` do em định nghĩa · **M1-4** **100%** file upload đi qua bước kiểm **opt-out Điều 37b** · **M1-5** 5 hạng mục provenance (`parent_generation_id`, `relation_kind`, `change_log`, `field_provenance`, `generation.origin`) tồn tại, **và có test chứng minh chúng commit CÙNG MỘT transaction** với artifact · **M1-6** eval kit chạy được trên golden dataset của MVP0 và cho ra số · **M1-7** `usage_daily` có p50/p90 regen ratio ⇒ **[G2](./MVP-Scope.md#73-g2--gate-kinh-tế-sau-mvp1) chạy được** | Gồm **toàn bộ** multi-tenancy **15–25%** `[EM]` (CF-6.9) + thành phần #5 editor tối thiểu (Story Bible editor, **4–6%** `[EM]`). Tổng tuần-người: **`TBD`** |
| **MVP2 — Comic Director** | 01/2027 – 02/2027 (~2 tháng) | Tự động hoá chặng scene → page → panel, và **khoá cứng các ràng buộc kỹ thuật vào schema** | Director tự động. Rubric `beat_type` + emphasis quota. `text_safe_zone`. Template layout + swap panel. Preview/export server-side. Hai human gate | **M2-1** Director sinh page/panel tự động cho **≥1 chapter** mà không cần panel script viết tay · **M2-2** **≤3 nhân vật/panel là CHECK constraint ở tầng DB** — đo bằng: insert panel 4 nhân vật **bị từ chối**, không phải bị cảnh báo · **M2-3** `text_safe_zone` có trong panel spec và typeset không đè vùng mặt ở **≥95%** panel — ⚠️ ngưỡng 95% là `[EM]` do em định nghĩa · **M2-4** **hai human gate (speaker attribution + dialogue condensation) không bypass được**: không tồn tại đường code nào xuất bản page mà chưa qua cả hai · **M2-5** export ra **PDF của 1 chapter hoàn chỉnh** từ preview server-side · **M2-6** checklist safe harbour Điều 198b hoàn thành **nếu** trigger "mở cho người ngoài upload" đã đến | Thành phần #2, #3, #4 editor tối thiểu (**11–17%** `[EM]`, phép cộng của em từ CF-6.7). Tổng tuần-người: **`TBD`** |
| **MVP3 — Visual Generation** | **03/2027 trở đi — NGOÀI HORIZON** | **Scale-up, không phải khám phá** — rủi ro đã được MVP0 kiểm trước (CF-8.9) | Pipeline sinh ảnh ở quy mô sản xuất. Credit ledger + hold. Hard quota. Worker process riêng. Fairness per tenant | **M3-1** credit ledger có **hold trước enqueue**, `CHECK (available >= 0)`, **hold reaper** — đo bằng test: 10 job đồng thời trên số dư đủ cho 5 job ⇒ đúng 5 job chạy · **M3-2** hold reserve = **3 credit/panel** (CF-6.12, vì N=3) · **M3-3** hard quota cưỡng chế **trước** khi enqueue, không đếm sau · **M3-4** worker chết mà API vẫn phục vụ được (test kill process) | Phần lớn khối pipeline lõi **35–45%** `[EM]` (Analysis §5.7, ngoài CF). Tổng tuần-người: **`TBD`** |
| **MVP4 — Production** | **NGOÀI HORIZON** | Hoàn thiện thứ người dùng thật sự nhận được | Continuity Checker dạng **N-candidate selection**. Batch. Export đầy đủ định dạng | **M4-1** Continuity Checker hoạt động ở dạng **N-candidate selection**, không phải flag+autofix (CF-8.10) · **M4-2** độ phủ checker được **công bố với user** đúng mức **40–60% số panel** `[EM]` (CF-6.11) — *"đừng để họ hiểu là được bảo vệ toàn diện"* | **`TBD`** |

---

## 3. Chi tiết từng mốc

### 3.1 Pre-cycle 09/2026 — ba việc **trước dòng code đầu tiên**

> Analysis §12 kết luận **ba việc trước dòng code đầu tiên**, theo đúng thứ tự đó. Mục này là ba việc đó, không hơn.

| | |
|---|---|
| **Input** | Bản thẩm định [Analysis-Comic-Studio-Concept.md](../050-Research/Analysis-Comic-Studio-Concept.md) · [MVP-Scope.md](./MVP-Scope.md) · **~$12** ngân sách API `[EM tính từ OFF]` (CF-3.11) · 1 chapter truyện chữ có bản quyền rõ ràng |
| **Output** | Xem cột *Deliverable* của bảng mục 2 |
| **Gate liên quan** | Khởi động **[G0](./MVP-Scope.md#71-g0--gate-pháp-lý)** (gửi câu hỏi) · Chạy và kết luận **[G1](./MVP-Scope.md#72-g1--gate-kỹ-thuật-sau-mvp0)** |
| **Đo bằng** | **Gate, không phải OKR** `[CHỐT]` CF-8.2 |

#### Việc 1 — Mang ba câu CF-7.8 tới luật sư SHTT Việt Nam

Ba câu Q1/Q2/Q3 và bối cảnh phải đưa kèm đã được soạn sẵn tại [MVP-Scope mục 7.1](./MVP-Scope.md#71-g0--gate-pháp-lý). Việc của pre-cycle là **gửi đi và nhận về bằng văn bản** — không phải tự trả lời.

⚠️ **Đây là việc có thời gian chờ không do mình kiểm soát** (`TBD`), nên nó là việc **khởi động trước tiên** trong tháng, chạy song song với MVP0. Nó **không chặn** MVP0 hay MVP1 — xem [mục 6](#6-phụ-thuộc--đường-găng).

#### Việc 2 — Chạy MVP0 (CF-8.4 → CF-8.6)

> [!CAUTION]
> ⛔ **KẾT QUẢ THỰC TẾ — MVP0 đã KHÉP ngày `2026-09-05` theo quyết định Founder, ⛔ KHÔNG PHẢI `G1` PASS.**
>
> Bảng kế hoạch bên dưới giữ nguyên làm **hồ sơ chủ đích ban đầu**. Cái thực sự xảy ra:
>
> | Exit criterion | Yêu cầu | Thực tế |
> |---|---|---|
> | `P-2` | `G1` có **SỐ** cho cả 5 tiêu chí + verdict được ghi | ⛔ **KHÔNG ĐẠT** — 0/5 tiêu chí có số |
> | `P-3` | regen ratio **p50 và p90** có giá trị số | ⛔ **KHÔNG ĐẠT** |
> | `P-6` | golden dataset có spec + ref + **ảnh** + **bảng chấm** | 🟡 **NỬA** — có spec + ref + 11 page YAML; ⛔ không có ảnh panel, ⛔ không có bảng chấm |
>
> ⭐ **Cái MVP0 thực sự mua được**: 33 ảnh trang chương 1 đã sinh, và **sáu kết luận về hành vi model** — ghi tại [`mvp0/golden-dataset/g1-verdict.md` §5.1](../../mvp0/golden-dataset/g1-verdict.md). Đúng kỷ luật *"giữ lại **kết luận** và dữ liệu"*, ⛔ chỉ thiếu đúng phần **số đo**.
>
> ⚠️ **Hệ quả phải theo dõi**: `G2-a` mất một nguồn đầu vào (còn mỗi `usage_daily` của MVP1) · `M1-6` **mất baseline hồi quy** ⇒ dựng lại eval kit sẽ **tốn tiền API lần hai**, đúng như [mục 6](#6-phụ-thuộc--đường-găng) đã cảnh báo khi xếp phụ thuộc này là *"mềm"*.

| Hạng mục | Nội dung |
|---|---|
| **Thời lượng** | **1–2 tuần** (CF-8.4) |
| **Chi phí** | **~$12** `[EM tính từ OFF]` (CF-3.11) — số cao làm trần an toàn |
| **Phạm vi** | **1 chapter duy nhất.** Story Bible cho 2–3 nhân vật **viết tay**. Panel script ~8–30 panel **viết tay** |
| **Code** | **Đúng một việc**: generate panel với reference + N candidate + VLM select. **Không UI, không database** — script + file phẳng |
| **Kỷ luật bắt buộc** | **Code của spike KHÔNG phải nền của sản phẩm.** Viết để trả lời câu hỏi rồi **bỏ**; giữ lại **kết luận và dữ liệu**. Nếu không nói rõ điều này trước, spike sẽ biến thành nền móng tạm bợ — đây là bẫy phổ biến nhất khi làm spike (`findings/architect.md` §7.3) |
| **Đo ba chỉ số** | (1) consistency · (2) N tối thiểu · (3) ⭐ **human-reject rate sau VLM-select** — chỉ số này **chưa ai công bố**, và nó quyết định checker có cắt được công người hay chỉ thêm chi phí (CF-8.5) |
| **Đo thêm, gần như miễn phí** | **Multi-character panel 2–3 nhân vật** (CF-6.4 — hàng load-bearing) và **regen ratio thực tế p50/p90** (CF-8.6 — biến quyết định của cả mô hình tài chính) |

**Rủi ro chính của MVP0:**

| Rủi ro | Dấu hiệu sớm | Xử lý |
|---|---|---|
| **Spike biến thành nền móng** | Bắt đầu thấy mình viết migration, viết config loader, viết abstraction cho provider | Dừng lại. MVP0 không có DB (xem [MVP-Scope §3.1](./MVP-Scope.md#31-ba-ô-đáng-chú-ý-nhất-trong-bảng)) |
| **Tràn ngân sách vì lặp nhiều vòng** | Chi vượt ~$25 mà chưa đủ 8 panel liền nhau để chấm | Trần thực tế ~$50 (Analysis §10). Vượt trần ⇒ dừng, ghi lại số đã đo, kết luận với dữ liệu đang có |
| **Chấm consistency bằng cảm tính** | Không có bảng chấm, chỉ có ấn tượng | Ngưỡng và cách đo đã định nghĩa sẵn tại [G1](./MVP-Scope.md#72-g1--gate-kỹ-thuật-sau-mvp0). **Định nghĩa trước, đo sau** |
| **Bỏ qua typeset** | Trang composite không có speech bubble | CF-8.11c: typeset **nổ ngay ở panel có thoại đầu tiên**, tức **trong MVP0**. Đây là exit criterion G1-e |

#### Việc 3 — Sửa khoá thời gian và chốt danh sách phải-có-trong-schema

- **Sửa khoá thời gian `(chapter, scene)`** — Analysis §5.1: khoá này **sai âm thầm ở flashback**. Đây là loại lỗi không báo lỗi, chỉ cho ra kết quả sai. Phải sửa **trước** dòng code sản phẩm đầu tiên, vì nó nằm trong khoá của mọi bảng timeline.
- **Chốt danh sách phải-có-trong-schema từ ngày đầu** = **7 mục KC-1…KC-7** tại [MVP-Scope mục 6](./MVP-Scope.md#6-không-được-cắt--danh-sách-cứng). Tất cả có chung tính chất: **rẻ khi làm từ đầu, không backfill được**.

---

### 3.2 MVP1 — Story Intelligence (10/2026 – 12/2026)

| | |
|---|---|
| **Input** | Verdict G1 · schema draft + danh sách KC-1…KC-7 · golden dataset của MVP0 · quyết định kiến trúc: **modular monolith** (CF-9.2) |
| **Output** | Xem cột *Deliverable* bảng mục 2 |
| **Gate liên quan** | **Chạy [G2](./MVP-Scope.md#73-g2--gate-kinh-tế-sau-mvp1) ở cuối mốc** (cuối Q4/2026) |
| **Chu kỳ OKR** | **Q4/2026 — chu kỳ chính** `[CHỐT]` CF-8.2. Key Result nằm ở [OKRs.md](./OKRs.md) |

**Nội dung theo CF-8.7** — MVP1 giữ nguyên phạm vi gốc (upload, parser, extraction, timeline, Story Bible) **và thêm năm thứ**, không thứ nào được đẩy sang mốc sau:

| # | Bổ sung vào MVP1 | Vì sao **phải** ở đây, không ở chỗ khác |
|---|---|---|
| 1 | **Text clean là bước ĐẦU TIÊN** | Rác scrape (quảng cáo, lời tác giả cuối chương, *"xin ủng hộ phiếu đề cử"*) đi vào extraction sẽ sinh entity giả. Là job của **code deterministic**, không phải LLM (Analysis §5.5) |
| 2 | **`tenant_id` từ ngày đầu** | Retrofit vào schema **đã có dữ liệu thật** là migration đắt nhất tồn tại, và **không có cách nào xác minh đã sửa hết** (KC-5) |
| 3 | **HITL gate + eval kit ngay tại đây**, không dồn MVP4 | Không có eval kit thì mọi thay đổi prompt/model về sau là **thay đổi mù**. Và golden dataset để chạy eval **đã có sẵn** từ MVP0 |
| 4 | **Log preference data** | Đây là **moat thật** (không phải 5 thành phần kỹ thuật). Gần như miễn phí, chỉ cần thiết kế để ghi lại. Và nó **dùng chung đúng cơ chế** mà luật VN buộc phải có ⇒ *một khoản đầu tư, trả hai lần* |
| 5 | **Kiểm opt-out Điều 37b trong bước ingest** | Chi phí **~0** (CF-7.5 `[OFF]`), và đây là nơi **duy nhất** file của user lần đầu đi vào hệ thống |

**Rủi ro chính của MVP1:**

| Rủi ro | Mức | Xử lý |
|---|---|---|
| **Khối multi-tenancy 15–25% `[EM]` làm tràn 3 tháng** | **Cao** — đây là rủi ro lịch số 1 của cả roadmap | **Mua auth và billing, đừng viết** (Analysis §5.7). Tự viết auth là cách nhanh nhất để một dev đơn lẻ đốt hai tháng và vẫn có lỗ hổng |
| Extraction kém trên truyện tiếng Việt scrape thật | Trung bình | Đã có ngưỡng đo M1-3 (≥80% so bible viết tay). Dưới ngưỡng ⇒ tăng phần human-in-the-loop, **không** kéo dài mốc |
| Provenance bị commit tách rời artifact | Cao về hậu quả | M1-5 yêu cầu **test** chứng minh cùng transaction. *"Bằng chứng có thể thiếu ngẫu nhiên thì không phải bằng chứng"* (CF-9.2 lý do 2) |
| Rơi vào cám dỗ build canvas | Trung bình | [MVP-Scope mục 4.1](./MVP-Scope.md#41-canvas-editor-14--cắt-một-phần-cf-91). MVP1 chỉ có **thành phần #5** (Story Bible editor) |

---

### 3.3 MVP2 — Comic Director (01/2027 – 02/2027)

| | |
|---|---|
| **Input** | Story Bible + timeline state chạy được từ MVP1 · kết quả G2 · golden dataset đã mở rộng |
| **Output** | Xem cột *Deliverable* bảng mục 2 |
| **Gate liên quan** | Không có gate mới. **Hệ quả của G1-d có thể áp vào đây**: nếu MVP0 đo panel 2 nhân vật dưới ngưỡng, M2-2 đổi thành **cứng hoá ≤2 nhân vật/panel** thay vì ≤3 |
| **Chu kỳ OKR** | **Preview Q1/2027** `[CHỐT]` CF-8.2 |

**Nội dung theo CF-8.8** — giữ Comic Director, nhưng bốn điều chỉnh:

| # | Điều chỉnh | Căn cứ |
|---|---|---|
| 1 | **Bỏ Layout Score số thực → rubric `beat_type` + emphasis quota** | CF-9.3 — không prior art, *"chưa ai làm vì không đáng"* |
| 2 | **Cứng hoá ≤3 nhân vật/panel** — trong **schema**, không phải guideline trong prompt | CF-6.5 `[OFF]`: ID-Sim **42.33** (2) → **27.21** (3) → **2.67** (4) → **0.52** (5); *"near-complete failure beyond three subjects"*. Corroborate: ComicInk hard-code trần **5 nhân vật**/issue, TaleAtelier **6 named characters**/project `[TC]` CF-6.6 |
| 3 | **Thêm `text_safe_zone` vào panel spec** | CF-8.8 — bubble che mặt là lỗi không thể tự động tránh nếu spec không chừa chỗ |
| 4 | **HAI human gate bắt buộc: speaker attribution + dialogue condensation** — *không phải tuỳ chọn, không dồn sang MVP4* | CF-8.8. Lý do định lượng: speaker attribution lỗi **30–50%** (3+ người) / **40–60%** (câu ngắn) ⚠️ `[EM]` **ước lượng, KHÔNG phải số đo** (CF-6.10) |

**Rủi ro chính của MVP2:**

| Rủi ro | Xử lý |
|---|---|
| Hai human gate bị "tạm bypass để test" rồi quên bật lại | M2-4 đo bằng **sự vắng mặt của đường code bypass**, không bằng cấu hình |
| Directing nhồi hết nhân vật vào một panel | Directing phải **thiên vị panel một nhân vật vì lý do kỹ thuật** — và LLM không biết điều đó nếu không được nói (Analysis §5.6). Đây là khuyến nghị **xuyên tầng**: xuất phát từ giới hạn Layer 3, thực thi ở Layer 2 |
| MVP2 tràn sang 03/2027 | Đã được chấp nhận trong [mục 1.3](#13-điều-không-chắc-chắn-ngay-bên-trong-phần-chứa-được). **Không nén để vừa khung** (CF-8.13) |

---

### 3.4 MVP3 — Visual Generation (**ngoài horizon**, từ 03/2027)

Giữ trong tài liệu này để đường găng đầy đủ, nhưng **nằm ngoài 09/2026–02/2027**.

| | |
|---|---|
| **Input** | Comic IR đầy đủ từ MVP2 · verdict G2 (bao gồm quyết định granularity per-panel hay whole-page) · adapter provider |
| **Output** | Pipeline sinh ảnh ở quy mô sản xuất + credit ledger + hard quota |
| **Gate liên quan** | **G0 chặn ở đây** nếu MVP3 là mốc bật thanh toán cho gói có image gen. Xem [mục 6](#6-phụ-thuộc--đường-găng) |
| **Rủi ro chính** | Thấp hơn mức thông thường: **rủi ro đã được MVP0 kiểm trước** ⇒ đây là **scale-up, không phải khám phá** (CF-8.9). Rủi ro còn lại là vận hành: race condition ở credit ledger, hold treo vĩnh viễn nếu thiếu hold reaper (CF-6.12), noisy neighbour nếu thiếu fairness per tenant |

---

## 4. Ba việc xen ngang

> CF-8.11 — **ba việc mà §18 gốc của `Request.md` không có.** Điểm quan trọng của mục này: **mỗi việc được neo vào một TRIGGER, không neo vào một ngày.** Neo vào ngày thì dễ bị dời; neo vào trigger thì không thể "làm sau" mà vẫn hợp lệ.

| # | Việc | **Trigger — làm trước khi cái gì xảy ra** | Đặt ở mốc nào | Vì sao **không** được dồn cuối |
|---|---|---|---|---|
| **X-a** | **Checklist safe harbour Điều 198b**: công cụ takedown · đăng ký đầu mối với **Bộ VHTTDL** · **SLA 72 giờ** `[OFF]` (CF-7.6) | **Trước lần đầu mở cho NGƯỜI NGOÀI upload** | **MVP2** (exit criterion M2-6) — hoặc **sớm hơn** nếu trigger đến sớm hơn | Một lần upload của người ngoài mà chưa có đường takedown là đã tạo ra nghĩa vụ pháp lý **không rút lại được**. Rẻ để làm trước, không sửa được sau |
| **X-b** | **Hard quota cưỡng chế TRƯỚC khi enqueue** + credit ledger + **hold reserve 3 credit/panel** + `CHECK (available >= 0)` + hold reaper (CF-6.12) | **Trước bản trả phí ĐẦU TIÊN CÓ image gen** (tức Tầng 2, CF-2.3) | **MVP3** (M3-1…M3-3) — **ngoài horizon** | *Check-rồi-gọi là race condition.* Free tier là **nghĩa vụ tài chính không giới hạn** nếu không chặn ở đúng đây. ⚠️ **Lưu ý phạm vi**: nếu trong horizon chỉ bán **Tầng 1 không có image gen** (CF-2.2), X-b chưa cần — nhưng **abuse control cho upload thì cần ngay ở MVP1** (giới hạn dung lượng/số upload, rate limit per tenant) |
| **X-c** | **Typeset layer + bubble overlay** (CF-8.11c) | **Ngay ở panel có thoại đầu tiên** | **Pre-cycle 09/2026 — trong MVP0** (exit criterion G1-e) | Nếu để tới sau, mọi đánh giá consistency ở MVP0 được thực hiện trên ảnh **không có chữ** — tức là đánh giá sai đối tượng. Trang thật có chữ, và chữ che mất một phần ảnh |

---

## 5. Ngoài horizon

### 5.1 Cái gì rơi ra khỏi 09/2026–02/2027

Trả lời trực tiếp cho CF-8.13. Đây là danh sách **rơi ra**, không phải danh sách **bị cắt** — mọi mục dưới đây vẫn nằm trong Full Scope của [MVP-Scope mục 3](./MVP-Scope.md#3-bảng-mvp-vs-full-scope).

| Rơi ra | Mốc dự kiến | Hệ quả trực tiếp phải chấp nhận |
|---|---|---|
| **MVP3 — Visual Generation ở quy mô sản xuất** | Từ **03/2027** | Trong horizon, sản phẩm **không có pipeline sinh ảnh chạy tự động ở quy mô**. MVP0 đã chứng minh nó **làm được**, nhưng chứng minh ≠ vận hành |
| **MVP4 — Production System** (Continuity Checker N-candidate, batch, export đầy đủ) | Sau MVP3 | Continuity Checker chưa có ⇒ độ phủ **40–60% số panel** `[EM]` (CF-6.11) chưa tồn tại ⇒ chưa được hứa gì với user về nó |
| **Gói trả phí CÓ image gen** — Tầng 2 (credit pack) và Tầng 3 (BYOK), CF-2.3/2.4 | Sau MVP3 | Không có doanh thu từ inference trong horizon. **Cũng có nghĩa: không có COGS inference trong horizon** — G2 chạy trên dữ liệu MVP0 + MVP1, không trên dữ liệu khách thật |
| **Credit ledger + hard quota** (X-b) | MVP3 | Không mở free tier có image gen trước khi có ledger. **Không có ngoại lệ** |
| **Canvas đầy đủ, realtime collab, inpainting, SSO/SAML** | Không có mốc | Đã hoãn tại [MVP-Scope mục 5.3](./MVP-Scope.md#53-bốn-thành-phần-hoãn) và bảng D2–D5, E8 |

### 5.2 ⭐ Hệ quả tích cực: thứ **có thể bán được** trong horizon

Nếu MVP3 rơi ra ngoài, câu hỏi tự nhiên là *"vậy trong 6 tháng có bán được gì không?"* Câu trả lời không phải "không":

**Tầng 1 (CF-2.2 `[CHỐT]`): $4–8/tháng, KHÔNG có image gen** — Story Bible editor + Comic IR + layout + versioning + export. **Margin ~90%, không cần API key.**

Đối chiếu với lộ trình: nội dung của Tầng 1 ≈ **MVP1 + MVP2 + export**. Tức là **Tầng 1 nằm gọn trong horizon**.

| | |
|---|---|
| **Nhãn** | `[EM]` — **suy luận của em**, không có trong bảng CF |
| **Điều kiện để đúng** | (1) Export/preview server-side phải hoàn thành ở MVP2 (exit M2-5) · (2) Checklist safe harbour X-a phải xong trước khi mở cho người ngoài (M2-6) · (3) **[G0](./MVP-Scope.md#71-g0--gate-pháp-lý) phải PASS** — đây là "dòng code thương mại đầu tiên" |
| **Vì sao nó khớp với CF-8.10** | CF-8.10 nói *"nâng ưu tiên export lên sớm — thứ **duy nhất** người dùng thật sự nhận được"*. Nếu Tầng 1 là thứ bán được trong horizon thì export **không còn là hạng mục MVP4** mà là **điều kiện doanh thu**. Đây là chỗ CF-8.10 có ý nghĩa vận hành cụ thể |
| **Neo thực tế để không kỳ vọng quá** | **SOM năm 1: $4K–14K ARR ≈ $300–1.200 MRR, 30–80 paying user** ⚠️ `[EM]` (CF-4.4). Neo: **Anifusion** — solo founder, **$833 MRR**, có lãi, **~2 năm** kể từ launch, **$0 marketing** `[TC]` (CF-4.5, ⚠️ **nguồn mâu thuẫn**: nguồn khác ghi $5.000/tháng; giá $9/mo vs €20/mo — ghi cả hai, không chọn một) |

> [!WARNING]
> Đây là một **lựa chọn**, không phải một kế hoạch đã chốt. Nó cần founder quyết định tại G2, và nó đánh đổi: bán Tầng 1 sớm nghĩa là **có khách thật, có nghĩa vụ safe harbour thật, có support thật** — trong khi 1 dev vẫn đang xây MVP3. Ghi ra đây để anh **thấy được lựa chọn**, không phải để mặc định chọn nó.

---

## 6. Phụ thuộc & đường găng

### 6.1 ⭐ Điều dễ hiểu nhầm nhất của cả tài liệu

> [!IMPORTANT]
> **G0 (gate pháp lý) chặn THƯƠNG MẠI HOÁ. G0 KHÔNG chặn MVP0 và MVP1.**
>
> Nói cách khác: **không phải "chờ luật sư mới được code"**.

Lý do rành mạch:

| Hoạt động | G0 có chặn không | Vì sao |
|---|---|---|
| **MVP0** — 1 chapter của chính mình, không có khách, không thu tiền, code bị vứt sau đó | **KHÔNG** | Không có người ngoài upload ⇒ không phát sinh nghĩa vụ safe harbour. Không thu tiền ⇒ không phải *"khai thác thương mại"* |
| **MVP1** — xây schema, multi-tenancy, provenance, extraction; dữ liệu là của chính mình | **KHÔNG** | Đây là xây **năng lực**, không phải **cung cấp dịch vụ**. Và trớ trêu thay: chính MVP1 xây ra **hồ sơ provenance** mà Điều 5a đòi hỏi — hoãn MVP1 để chờ G0 là hoãn đúng thứ giúp thoả G0 |
| **Mở cho NGƯỜI NGOÀI upload** | **CÓ** — cộng thêm X-a (safe harbour) | Nghĩa vụ trung gian phát sinh đúng tại thời điểm này |
| **Bật thanh toán** (bất kỳ tầng nào) | **CÓ — chặn cứng** | Đây là *"dòng code thương mại đầu tiên"*. **Rủi ro nhị phân duy nhất** (CF-7.9): trả lời sai thì sản phẩm **bất hợp pháp**, không phải kém hơn |

**Hệ quả thực tế**: G0 được **khởi động ngay tuần đầu 09/2026** và chạy **song song** với MVP0/MVP1, chính vì thời gian chờ luật sư (`TBD`) nằm ngoài tầm kiểm soát. Nếu đợi G0 xong mới bắt đầu, cả lộ trình trượt theo một biến mà mình không điều khiển được.

### 6.2 Bảng phụ thuộc

| Cái này | Chặn cái kia | Loại phụ thuộc |
|---|---|---|
| **G1 PASS** (cuối 09/2026) | Toàn bộ MVP1 → MVP4 | **Cứng.** G1 FAIL ⇒ đổi cách tiếp cận hoặc đổi định vị trước khi đầu tư tiếp ([MVP-Scope §7.2](./MVP-Scope.md#72-g1--gate-kỹ-thuật-sau-mvp0)) |
| **Sửa khoá thời gian `(chapter, scene)`** (pre-cycle, việc 3) | Mọi bảng timeline của MVP1 | **Cứng.** Sai âm thầm ở flashback; nằm trong khoá nên sửa sau = migration toàn bộ |
| **7 mục KC-1…KC-7 có mặt trong schema MVP1** | Giá trị pháp lý của **mọi** generation về sau | **Cứng và một chiều.** **Không backfill được** (CF-7.3) |
| **`tenant_id` + RLS ở MVP1** | Mọi tính năng multi-tenant sau đó | **Cứng.** Retrofit là migration đắt nhất tồn tại (KC-5) |
| **MVP1 kết thúc trước 31/12/2026** | **G2** chạy đúng lịch | **Cứng theo định nghĩa gate.** Trượt ⇒ G2 trượt ⇒ MVP2 bị đẩy ra ngoài horizon |
| **regen ratio p50/p90 có số** (từ MVP0 + `usage_daily` MVP1) | **G2** | **Cứng.** Thiếu dữ liệu ⇒ G2 **KHÔNG CHẠY ĐƯỢC**, không PASS mặc định |
| **G2 verdict** (per-panel hay whole-page) | Thiết kế pipeline của **MVP3** | **Mềm về dữ liệu, cứng về effort.** ⭐ **Data model KHÔNG phải đổi** — spec tách khỏi ảnh (Analysis §9b.3). Nhưng compiler và compositor thì đổi |
| **X-a safe harbour** | Mở cho người ngoài upload | **Cứng** (CF-8.11a) |
| **X-b hard quota + credit ledger** | Bản trả phí có image gen | **Cứng** (CF-8.11b, CF-6.12) |
| **G0 PASS** | **Bật thanh toán** — bất kỳ tầng nào | **Cứng.** ⚠️ **Không** chặn MVP0/MVP1 — xem [mục 6.1](#61--điều-dễ-hiểu-nhầm-nhất-của-cả-tài-liệu) |
| **Golden dataset của MVP0** | Eval kit ở MVP1 (M1-6) | **Mềm** — có thể dựng lại, nhưng dựng lại tốn tiền API lần hai |

### 6.3 Đường găng (critical path)

```text
Tuần 1, 09/2026 ──┬── [G0] gửi 3 câu hỏi tới luật sư SHTT  ─────────────────┐
                  │        (thời gian chờ TBD, chạy song song)             │
                  │                                                         │
                  └── MVP0 (1–2 tuần) ──► [G1] cuối 09/2026                │
                                              │                             │
                                              ▼ PASS                        │
                              Sửa khoá thời gian + chốt KC-1…KC-7          │
                                              │                             │
                                              ▼                             │
                              MVP1  10–12/2026  ──► [G2] cuối Q4/2026      │
                                              │                             │
                                              ▼ PASS                        │
                              MVP2  01–02/2027                              │
                                              │                             │
                        ══════ hết horizon 02/2027 ══════                   │
                                              │                             │
                                              ▼                             ▼
                              MVP3  từ 03/2027 ◄──────── [G0] phải PASS trước khi bật thanh toán
                                              │
                                              ▼
                              MVP4
```

**Đọc sơ đồ này theo hai nhánh:**

- **Nhánh dọc (kỹ thuật)** là đường găng thật của effort: MVP0 → G1 → MVP1 → G2 → MVP2 → …
- **Nhánh phải (pháp lý)** chạy **song song** và chỉ **giao lại** ở điểm bật thanh toán. Đây chính là hình ảnh của [mục 6.1](#61--điều-dễ-hiểu-nhầm-nhất-của-cả-tài-liệu).

**Điểm mong manh nhất của đường găng**: **MVP1 phải vừa 3 tháng**. Nó gánh khối multi-tenancy **15–25%** `[EM]` (CF-6.9) mà `Request.md` gốc không nhắc một dòng, cộng toàn bộ Story Intelligence và provenance. Nếu chỉ có một chỗ để theo dõi sát trong cả roadmap, đó là chỗ này.

---

## 7. Tài liệu tham khảo

### 7.1 Tài liệu trong repo

- [MVP-Scope.md](./MVP-Scope.md) — **định nghĩa ba gate G0/G1/G2**, ranh giới MVP, danh sách không được cắt, kill criteria
- [Charter-Comic-Studio.md](./Charter-Comic-Studio.md) — biện minh dự án, ràng buộc cấp dự án, RACI
- [OKRs.md](./OKRs.md) — Objective và Key Result cho pre-cycle 09/2026, Q4/2026, preview Q1/2027
- [Risk-Register.md](./Risk-Register.md) — sổ rủi ro, lịch rà soát theo gate
- [Analysis-Comic-Studio-Concept.md](../050-Research/Analysis-Comic-Studio-Concept.md) — §5.1 khoá thời gian · §5.5–5.7 · §6 ba thứ nên cắt · §9b.3 xung đột M13 · §10 lộ trình MVP0 · §12 ba việc trước dòng code đầu tiên
- [findings/architect.md](./pm-runs/2026-08-23-danh-gia-y-tuong-comic-studio/findings/architect.md) — §7.1–7.3 thứ tự milestone và ngưỡng gate · §B4 credit ledger + hold
- [outline.md](./pm-runs/2026-08-23-khoi-tao-tai-lieu-planning-comic-studio/outline.md) — bảng **Canonical Facts** CF-1 → CF-9

### 7.2 Nguồn ngoài được dẫn qua bảng Canonical Facts

| Nội dung | Nguồn | Nhãn |
|---|---|---|
| N=3 saturation, CANVAS metrics | [arXiv 2604.13452](https://arxiv.org/html/2604.13452v1) | `[OFF]` |
| CogCanvas ID-Sim theo số nhân vật | [arXiv 2606.15867](https://arxiv.org/html/2606.15867) | `[OFF]` |
| Nghị định 134/2026/NĐ-CP (hiệu lực 09/04/2026), Điều 5a / 37a / 37b / 198b | [Cục Bản quyền tác giả](https://cov.gov.vn/tin-tuc/gioi-thieu-nghi-dinh-so-1342026ndcp-quy-dinh-ve-quyen-tac-gia-quyen-lien-quan-168925.html) · [Baker McKenzie](https://www.bakermckenzie.com/en/insight/publications/2026/05/vietnam-redefining-copyright-for-ai) | `[OFF]` · ⚠️ Điều 37a **dựa trên bản tóm tắt, không phải nguyên văn** (CF-7.4) |
| Giá ảnh Gemini 3 Pro Image / FLUX.2 pro | CF-3.4 | `[OFF]` |
| Mô hình 3 tầng — comp Novelcrafter | [novelcrafter.com/pricing](https://www.novelcrafter.com/pricing) | `[OFF]` |

> [!NOTE]
> Danh sách URL đầy đủ nằm ở mục *Tài liệu tham khảo* của [Analysis-Comic-Studio-Concept.md](../050-Research/Analysis-Comic-Studio-Concept.md).
