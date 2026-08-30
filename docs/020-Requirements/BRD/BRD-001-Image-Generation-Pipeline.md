---
id: BRD-001
type: brd
status: draft
project: comic-studio
created: 2026-08-24
---

# BRD-001 — Pipeline sinh ảnh (Image Generation Pipeline)

> [!IMPORTANT]
> **Quy ước nhãn nguồn số liệu** (kế thừa nguyên vẹn từ bảng Canonical Facts — **số và nhãn là một cặp không tách rời**):
> `[OFF]` official/paper gốc · `[BCN]` báo cáo ngành có tên firm · `[TC]` thứ cấp · `[EM]` ước lượng hoặc phép nhân, **không phải số đo** · `[CHỐT]` quyết định của Founder tại gate.
>
> **Ký hiệu mốc** (giữ nguyên từ [MVP-Scope.md](../../010-Planning/MVP-Scope.md) §3): ✅ có đầy đủ · 🟡 có một phần / bản tối thiểu · ⛔ hoãn sang mốc sau · ❌ **cắt hẳn, không có trong Full Scope**.

## Mục lục

1. [Business goal](#1-business-goal)
2. [Phạm vi module](#2-phạm-vi-module)
3. [Yêu cầu nghiệp vụ](#3-yêu-cầu-nghiệp-vụ)
4. [Ràng buộc & điều kiện chặn](#4-ràng-buộc--điều-kiện-chặn)
5. [Cái module này KHÔNG làm](#5-cái-module-này-không-làm)
6. [Rủi ro chính](#6-rủi-ro-chính)
7. [Tài liệu liên quan](#7-tài-liệu-liên-quan)

---

## 1. Business goal

Sinh được panel có nhân vật nhất quán từ một `Panel Specification`, ở chi phí và chất lượng cho phép **bán được**. Đây là hàng duy nhất trong tám module tạo ra artifact mà khách hàng **nhìn thấy** — mọi module khác đều là điều kiện để hàng này chạy đúng.

Vì thế module này cũng là nơi tiền đề của cả sản phẩm được kiểm trước tiên: nguyên tắc bao trùm của scope là *"sinh một ảnh trong tuần đầu tiên, dù bằng tay, dù chỉ 8 panel"* (CF-8.12), và code của **MVP0** làm **đúng một việc** — generate panel với reference + N candidate + VLM select (CF-8.4). Nếu tiền đề này không đứng, biết sau **1–2 tuần** thay vì sau 4 tháng.

## 2. Phạm vi module

Bảng dưới đây là **nhóm A của [MVP-Scope.md](../../010-Planning/MVP-Scope.md) §3, trích nguyên nhãn từng mốc** — không đổi nhãn, không diễn giải lại nhãn. Cả bảy hàng `A1–A7` thuộc phạm vi module này.

| # | Hạng mục | MVP0 | MVP1 | MVP2 | MVP3 | MVP4 | Full Scope | Căn cứ (theo `MVP-Scope` §3) |
|---|---|:--:|:--:|:--:|:--:|:--:|:--:|---|
| **A1** | Generate panel: reference + N candidate + VLM select | ✅ | ⛔ | ⛔ | ✅ | ✅ | ✅ | CF-8.4 (code MVP0 làm **đúng một việc** này) · CF-3.1 N=3 `[OFF]` |
| **A2** | Typeset layer + bubble overlay (composite ra trang thật có thoại) | 🟡 thô | 🟡 | 🟡 | ✅ | ✅ | ✅ | CF-8.11c — *"nổ ngay ở panel có thoại đầu tiên, tức trong MVP0"* |
| **A3** | Visual Prompt Compiler **deterministic** (lookup + policy, không LLM ở runtime) | 🟡 script | 🟡 | 🟡 | ✅ | ✅ | ✅ | Analysis §5.5 — compiler deterministic là **điều kiện cần** để bảng `Generation` có nghĩa |
| **A4** | Adapter đa provider (Gemini 3 Pro Image, FLUX.2) | 🟡 1 adapter | ⛔ | ⛔ | ✅ | ✅ | ✅ | Analysis §6.2 seam #4 · CF-3.4 `[OFF]` |
| **A5** | Job queue trong Postgres (`FOR UPDATE SKIP LOCKED`, transactional enqueue) | ❌ không cần | ✅ | ✅ | ✅ | ✅ | ✅ | Analysis §6.2 — MVP0 là script + file phẳng, không DB |
| **A6** | Fairness per tenant trong câu CLAIM job | ⛔ | ⛔ | ⛔ | ✅ | ✅ | ✅ | Analysis §6.2 seam kinh tế — nhồi vào sau là sửa đúng câu SQL nóng nhất |
| **A7** | **Whole-page render granularity** (đường lui của G2) | ⛔ | ⛔ | ⛔ | 🟡 tuỳ chọn | ✅ | ✅ | Analysis §9b.3 — spec tách khỏi ảnh nên **đổi granularity không đổi data model** |

> Cờ horizon (quy ước **QC-3** của run: gán theo **mốc đầu tiên** hạng mục được giao): `A1–A5` **TRONG** horizon 09/2026–02/2027 · `A6`, `A7` **NGOÀI** horizon.

## 3. Yêu cầu nghiệp vụ

| ID | Phát biểu yêu cầu | Căn cứ (file + mục) | Mốc MVP |
|---|---|---|---|
| **BR-001-01** | Mỗi panel được sinh bằng **best-of-N với N = 3 là mặc định cho MỌI panel**: hệ thống dựng N candidate từ ảnh reference của nhân vật, rồi một VLM chọn **một** candidate. Ảnh reference là **điều kiện đầu vào**, không phải mô tả bằng text prompt. | `MVP-Scope` §3 A1 · CF-3.1 `[OFF]` arXiv 2604.13452 *"performance saturates at N=3"* · `Charter` §7 C8 · `Glossary` *best-of-N (N=3)*, *Canonical Reference* | MVP0 ✅ (⛔ MVP1–MVP2, ✅ lại từ MVP3) |
| **BR-001-02** | ⛔ **`best-of-N` phải được hiện thực như mặc định trên mọi panel, KHÔNG phải `retry-on-failure`.** Hạ N là **đổi chất lượng lấy margin** ⇒ phải chạy lại gate **G1**, không phải chỉ G2. | CF-3.2 `[OFF]` · `Charter` §7 C8 · `MVP-Scope` §7.3 callout WARNING · `findings/business-analyst.md` §5.3 **CẤM-03** · `Glossary` *best-of-N* (*"nhầm hai khái niệm này là nguồn của sai số chi phí +50%"*) | Xuyên mọi mốc |
| **BR-001-03** | Thoại được render bằng **typeset layer tách khỏi ảnh** (bubble + chữ vẽ bằng code lên trên), ảnh được sinh **không có chữ** — `text, letters, watermark, speech bubble` nằm ở negative prompt. Sửa một câu thoại **không** được kéo theo một lần sinh lại ảnh. | `MVP-Scope` §3 A2 · CF-8.11c · `Glossary` *typeset layer* · ngưỡng đo `MVP-Scope` §7.2 **G1-e** (**100%** panel có thoại dùng overlay · **0** panel nhờ model render chữ) | MVP0 🟡 thô → MVP3 ✅ |
| **BR-001-04** | `Visual Prompt Compiler` là **code deterministic**, không phải LLM ở runtime: cùng một `Panel Specification` luôn cho ra **cùng một** prompt. Bản chất là tra bảng `field value → cụm từ`, sắp thứ tự, dedup, giải xung đột theo **precedence ladder**, thực thi **constraint budget** và **ghi log ràng buộc bị drop**. | `MVP-Scope` §3 A3 (dẫn Analysis §5.5) · `Glossary` *Visual Prompt Compiler*, *precedence ladder*, *constraint budget* | MVP0 🟡 script → MVP3 ✅ |
| **BR-001-05** | Trong `precedence ladder`, **identity reference ở bậc cao nhất và không bao giờ bị drop**; camera angle / composition / props phụ là nhóm bị drop **đầu tiên** khi vượt `constraint budget`. | `Glossary` *precedence ladder*, *constraint budget* (vượt trần thì thêm ràng buộc **làm giảm** chất lượng do instruction dilution) · `Glossary` *Identity vs Appearance* | MVP0 (cùng A3) → MVP3 ✅ |
| **BR-001-06** | Mỗi image provider được truy cập qua **một adapter riêng**; đổi provider là **thay adapter**, không sửa pipeline. Giá đầu vào do provider đặt và **không đàm phán được** ⇒ nó không được khoá cứng sản phẩm. | `MVP-Scope` §3 A4 (dẫn Analysis §6.2 seam #4) · CF-3.4 `[OFF]` Gemini 3 Pro Image **$0.134** standard / **$0.067** batch · FLUX.2 pro **$0.03** | MVP0 🟡 1 adapter → MVP3 ✅ |
| **BR-001-07** | Job sinh ảnh được **enqueue trong cùng transaction** với dữ liệu nghiệp vụ và được lấy ra bằng `FOR UPDATE SKIP LOCKED` **trong Postgres** — không thêm một hạ tầng queue riêng. Hệ quả: **không có job mồ côi**. | `MVP-Scope` §3 A5 · CF-9.2 (modular monolith: 1 process / 1 PostgreSQL / 3 schema) | MVP1 ✅ (MVP0 = ❌ không cần — MVP0 **không có database**, `MVP-Scope` §3.1) |
| **BR-001-08** | Câu CLAIM job phải **fairness per tenant**: một tenant không chiếm hết worker, để tenant khác không thấy sản phẩm treo. | `MVP-Scope` §3 A6 (dẫn Analysis §6.2 *seam kinh tế*) · `Glossary` *seam kinh tế vs seam kỹ thuật* | MVP3 ✅ — **NGOÀI horizon** |
| **BR-001-09** | Pipeline phải hỗ trợ **whole-page render granularity**: compile **nhiều** `Panel Specification` thành **MỘT** prompt whole-page. Đây là **đường lui #1 khi gate G2 FAIL**, và nó **không đổi data model** — vì spec, không phải ảnh, là dữ liệu chính. | `MVP-Scope` §3 A7 · `MVP-Scope` §7.3 *"Nếu FAIL — đường lui"* #1 (dẫn Analysis §9b.3) · `Glossary` *Panel Specification* | MVP3 🟡 tuỳ chọn → MVP4 ✅ — **NGOÀI horizon** |
| **BR-001-10** | Mục tiêu của bảng `Generation` là **AUDITABILITY + LINEAGE**, **không phải reproducibility bit-exact**: `seed` là **provenance metadata**, không phải replay key. Lý do: nhiều API không cho set seed, và provider cập nhật weights dưới cùng một tên model (**silent model drift**). | `MVP-Scope` §4.4 (đoạn *"Điều chỉnh cách diễn đạt, không phải cách làm"*) · `Glossary` *`Generation` / `parent_generation`* | MVP1 ✅ (theo diễn giải `MVP-Scope` §3.1 — xem mục 4) |
| **BR-001-11** | Mọi lần sinh ảnh ghi **`parent_generation_id` + `relation_kind` + `origin`**, và bản ghi đó **commit cùng một transaction** với artifact mà nó chứng minh. | `MVP-Scope` §6 **KC-1**, **KC-3**, **KC-4** · CF-7.3 `[OFF]` · CF-9.4 (PM run trước **tự thu hồi** khuyến nghị cắt `parent_generation`) | MVP1 (`MVP-Scope` §3 GP-1 = ✅ MVP1; hàng GP thuộc [BRD-007](./BRD-007-Legal-And-Compliance.md)) |
| **BR-001-12** | Trước khi enqueue một panel, hệ thống **HOLD 3 credit/panel** — vì **N=3 là mặc định cho mọi panel**, không phải trường hợp xấu. Pipeline **không được** gọi provider trước khi hold được ghi. | `MVP-Scope` §6 **KC-7** · CF-6.12 · `Glossary` *credit ledger + hold* (cơ chế ledger thuộc [BRD-006](./BRD-006-Credit-And-Unit-Economics.md)) | MVP3 — trước bản trả phí có image gen |

> **`TBD` — ba khoảng trống không nguồn nào trong repo trả lời được** (không được viết thành số):
>
> | # | Khoảng trống | Trạng thái |
> |---|---|---|
> | **KT-7** | Benchmark độc lập đo frontier model ở **2–3 nhân vật/panel** — **KHÔNG TỒN TẠI** trong dữ liệu công khai ⇒ **MVP0 là phép đo đầu tiên** | `TBD` |
> | **KT-8** | **Human-reject rate sau VLM-select** — **chưa ai công bố con số này** (CF-8.5 (3)) | `TBD` |
> | **KT-9** | Benchmark định lượng **render tiếng Việt có dấu** của bất kỳ image model; đặc biệt thiếu số cho chữ chồng hai dấu (*"ế"*, *"ữ"*, *"ượ"*) | `TBD` |
>
> Nguồn xác nhận khoảng trống: `findings/business-analyst.md` §6.2.

## 4. Ràng buộc & điều kiện chặn

### 4.1 Danh sách cứng `KC-x` mà module này chạm (`MVP-Scope` §6)

| # | Ràng buộc | Module A chạm ở đâu |
|---|---|---|
| **KC-1** | `parent_generation_id` (nullable FK) + `relation_kind ENUM('retry','variation','refine','continuity_fix')` — từ **MVP1** | Mọi row `generation` do pipeline tạo. **Không backfill được**: thêm cột sau thì mọi generation quá khứ có `parent = NULL` **vĩnh viễn** (CF-7.3 `[OFF]`) |
| **KC-2** | `change_log` ghi **mọi** hành động người dùng — kể cả *"chọn generation X thay vì Y"* | Hành động **chọn candidate** trong best-of-N là hành động sáng tạo rẻ nhất mà giá trị pháp lý cao nhất ⇒ phải sinh một `change_log` row |
| **KC-3** | `field_provenance` (mức field) + `generation.origin ENUM('ai','ai_edited','human')` | Pipeline là nơi `origin` được đặt lần đầu |
| **KC-4** | KC-1 + KC-2 + KC-3 **commit CÙNG MỘT TRANSACTION** với artifact chúng chứng minh | *"Bằng chứng có thể thiếu ngẫu nhiên thì không phải bằng chứng."* Đây là một trong ba lý do **cấm tách DB** (CF-9.2 lý do 2) |
| **KC-7** | Credit ledger + **HOLD trước khi enqueue** + **reserve 3 credit/panel** + `CHECK (available >= 0)` ở tầng DB + **hold reaper** | Ràng buộc trực tiếp lên đường enqueue của A5: **check-rồi-gọi là race condition** (CF-6.12) |

> ⚠️ **Thời điểm bắt đầu nghĩa vụ provenance là một diễn giải, không phải một CF.** CF-7.3 nói *"không lưu từ generation đầu tiên thì vĩnh viễn không có"* (đọc thô là MVP0); `MVP-Scope` §3.1 diễn giải *"generation đầu tiên của sản phẩm thật, tức MVP1"* và **tự khai đây là `[EM]` diễn giải của writer run trước, không có trong CF** (mâu thuẫn **MT-7**, `findings/business-analyst.md` §6.1). Tài liệu này dùng diễn giải MVP1 **và giữ nguyên nhãn đó**.

### 4.2 Ràng buộc cấp dự án `C-x` (`Charter` §7)

| # | Ràng buộc | Hệ quả cho module A |
|---|---|---|
| **C1** | Đội **1 người + AI assist**, không funding, không ngân sách marketing `[CHỐT]` CF-1.2 | Mọi hạng mục của module phải chia được cho một người |
| **C3** | **Trần cứng ≤3 nhân vật/panel**, cứng hoá trong Comic IR `[OFF]` CF-6.5 | Pipeline **giả định** trần này đã được schema cưỡng chế; việc cưỡng chế thuộc [BRD-003](./BRD-003-Comic-Director-And-Layout.md) |
| **C6** | Gross margin kỳ vọng **50–60%**, không phải 80% `[BCN]` CF-3.10 (ICONIQ 52%, Bessemer 50–60%) | Mọi lựa chọn granularity/provider của module bị đo bằng dải này |
| **C7** | Chi phí **sàn** **$12,06/chapter** @N=3, Gemini batch — **là SÀN, không phải trần** (chưa tính VLM call để score 3 candidate) `[EM tính từ OFF]` CF-3.5 | ⛔ **CẤM-04**: cấm dùng $12,06 như chi phí thực tế mà không nêu nó là sàn |
| **C8** | **N = 3 là mặc định cho MỌI panel** (best-of-N), **KHÔNG phải retry-on-failure** `[OFF]` CF-3.1/3.2 | Ràng buộc lõi của BR-001-01 và BR-001-02. Hold reserve phải là **3 credit/panel** |
| **C9** | Thứ tự milestone cố định **MVP0 → MVP1 → MVP2 → MVP3 → MVP4** CF-8.3 | Không đảo thứ tự để *"làm phần dễ trước"* |
| **C10** | Horizon 6 tháng (09/2026–02/2027) **chưa được ai xác nhận là đủ cho 1 dev** `[CHỐT]` CF-8.1 + CF-8.13 | ⛔ **CẤM-08**: cấm nén lịch cho vừa khung. `A6`, `A7` **rơi ra ngoài** horizon |

### 4.3 Điều kiện chặn theo gate (`MVP-Scope` §7)

| Gate | Chặn cái gì của module A | Ngưỡng liên quan |
|---|---|---|
| **G1 — Kỹ thuật** (cuối 09/2026, sau MVP0) | Chặn việc đi tiếp MVP1 | **G1-a** consistency **≥70%** · **G1-b** N **≤3** · **G1-c** human-reject rate **≤30%** PASS / 30–50% có điều kiện / **>50%** FAIL · **G1-d** panel 2 nhân vật **≥60%** (panel 3 nhân vật: **đo và báo cáo, không đặt ngưỡng chặn**) · **G1-e** **100%** overlay / **0** panel nhờ model render chữ. ⚠️ **G1-c và G1-d là `[EM]` — ngưỡng do writer run trước ĐỊNH NGHĨA TẠI RUN ĐÓ, không có nguồn ngoài** (CF-10.4). Trích mà bỏ nhãn này là để chúng **mạo danh benchmark ngành** |
| **G2 — Kinh tế** (cuối Q4/2026, sau MVP1) | Chặn mô hình giá, và là gate mở đường lui `A7` | `MVP-Scope` §7.3. **G2 thiếu dữ liệu ⇒ KHÔNG CHẠY ĐƯỢC, không PASS mặc định** (CF-10.6) |
| **G0 — Pháp lý** | ⚠️ **KHÔNG chặn MVP0 và MVP1.** G0 chặn **thương mại hoá** | ⛔ **CẤM-10** — `Charter` §9.2 gọi việc đọc sai điều này là *"cách hiểu nhầm đắt nhất"* |

## 5. Cái module này KHÔNG làm

| # | Không làm | Lý do + căn cứ | Điều kiện mở lại |
|---|---|---|---|
| 1 | **Không hạ N xuống dưới 3 để cứu margin** | `MVP-Scope` §7.3 callout: đây là **đường KHÔNG được đi** khi G2 FAIL. Hạ N là đổi chất lượng lấy margin ⇒ phải chạy lại **G1** (CẤM-03) | Chỉ khi chạy lại **G1** với N mới và G1 PASS |
| 2 | **Không hiện thực `best-of-N` dưới dạng `retry-on-failure`** | Hai khái niệm khác nhau. `best-of-N` chạy trên **mọi** panel như mặc định, không phải chỉ khi panel lỗi (`Glossary` *best-of-N*; CF-3.1/3.2 `[OFF]`) | Không mở lại — đây là định nghĩa, không phải scope |
| 3 | **Không nhờ model render chữ vào pixel ảnh** | `MVP-Scope` §7.2 **G1-e**: **0** panel được dựa vào model render chữ; chữ đi qua typeset layer (`Glossary` *typeset layer*) | Không mở lại trong Full Scope |
| 4 | **Không làm `Continuity Checker`** — và tuyệt đối không gọi bước VLM-select của pipeline bằng tên đó | Hàng **H3** thuộc [BRD-008](./BRD-008-Quality-And-Operations.md). ⛔ **CẤM-12**: nghĩa canon của `Continuity Checker` là **QA-based selection giữa N candidate** (*"trong N cái này, cái nào consistent hơn"*), **KHÔNG** phải gắn nhãn ✓/✗ từng attribute rồi autofix — định nghĩa cũ đã bị bác (`Glossary` *Continuity Checker*; CF-8.10) | Chỉ nếu Full Scope đổi checker trở lại dạng flag+autofix — điều mà CF-8.10 đã bác |
| 5 | **Không sở hữu độ phủ của checker, và không được để user hiểu là được bảo vệ toàn diện** | CF-6.11 độ phủ **40–60% số panel** ⚠️ `[EM]` **ước lượng, KHÔNG phải số đo** — *"phải nói rõ với user"*. Khoảng trống **G-05** của `Risk-Register` §4.1 | Khi có số đo thật từ MVP0/MVP1 |
| 6 | **Không làm UI chọn variant, không làm bubble editor** | Pipeline chỉ **sinh** candidate và chạy VLM-select; thành phần **#1 panel card + variant picker** và **#2 bubble/text overlay editor** là editor tối thiểu, thuộc [BRD-004](./BRD-004-Minimum-Editor.md) (`MVP-Scope` §5.2) | — (hai thành phần đó **không** bị cắt, chỉ khác chủ) |
| 7 | **Không làm infinite canvas / undo xuyên state / realtime collab / inpainting brush** | Hàng **D2–D5**, thuộc [BRD-004](./BRD-004-Minimum-Editor.md); CF-9.1 hoãn cả bốn | Theo `MVP-Scope` §5.3 — của module D, không của module này |
| 8 | **Không sở hữu credit ledger, hard quota, `usage_event`** | Nhóm **F**, thuộc [BRD-006](./BRD-006-Credit-And-Unit-Economics.md). Module A **chịu** ràng buộc KC-7 nhưng không xây ledger | — |
| 9 | **Không sở hữu eval kit, golden dataset, log preference data** | Nhóm **H** (H1, H2, H6), thuộc [BRD-008](./BRD-008-Quality-And-Operations.md) — dù chính output của module A là thứ bị đo | — |
| 10 | **Không dựa vào cache để cứu margin** | CF-6.13 hit rate **vài % tới ~10%** ⚠️ `[EM]` `architect` **tự khai là ước lượng**; khoảng trống **G-10** | Khi có hit rate **đo được** từ traffic thật |

## 6. Rủi ro chính

> [!IMPORTANT]
> Tài liệu này **không tự chấm điểm rủi ro mới** và **không lập thang Probability × Impact riêng**. Thang, Score, Trigger, Mitigation và Owner do [Risk-Register.md](../../010-Planning/Risk-Register.md) sở hữu — bảng dưới đây **chỉ trỏ tới hàng tương ứng**.

| ID | Vì sao nó là rủi ro của module A | Rà tại |
|---|---|---|
| [R-12](../../010-Planning/Risk-Register.md#21-bảng-chính) | Multi-character panel 2–3 nhân vật **chưa có benchmark độc lập** — hàng load-bearing của cả verdict khả thi | G1 |
| [R-10](../../010-Planning/Risk-Register.md#21-bảng-chính) | Không giảm được N xuống dưới 3 ⇒ COGS sàn không giảm được | G1 |
| [R-08](../../010-Planning/Risk-Register.md#21-bảng-chính) | **$12,06/chapter là SÀN, không phải trần** — chưa tính VLM call để score 3 candidate | G1 |
| [R-13](../../010-Planning/Risk-Register.md#21-bảng-chính) | Props là metric thấp nhất trong bốn metric của CANVAS | G1 |
| [R-22](../../010-Planning/Risk-Register.md#21-bảng-chính) | Phụ thuộc provider + **silent model drift** — chất lượng tụt mà **không lỗi nào được ném ra** | Hàng tuần |
| [R-01](../../010-Planning/Risk-Register.md#21-bảng-chính) | Provenance không lưu từ generation đầu tiên ⇒ **không backfill được** | Tại PR/migration đầu tiên chạm schema |
| [R-14](../../010-Planning/Risk-Register.md#21-bảng-chính) | Race condition ở credit ledger trên đúng đường enqueue của A5 | Tại PR/migration đầu tiên chạm schema |
| [R-17](../../010-Planning/Risk-Register.md#21-bảng-chính) | Dựa vào cache để cứu margin | — |
| [G-05](../../010-Planning/Risk-Register.md#41-năm-khoảng-trống-không-gán-score) · [G-07](../../010-Planning/Risk-Register.md#42-khoảng-trống-nằm-bên-trong-một-rủi-ro-đã-được-score) | Hai **khoảng trống không gán Score**: độ phủ thật của checker; **số ảnh/chapter = 60** ⚠️ `[EM]` là **giả định, không phải số đo** | G1 |

## 7. Tài liệu liên quan

### 7.1 Traceability

| Quan hệ | Tài liệu |
|---|---|
| Implements | [PRD-Comic-Studio.md](../PRD-Comic-Studio.md) |
| Chi tiết kỹ thuật | [SRS-Comic-Studio.md](../SRS-Comic-Studio.md) |
| Epic tương ứng (1:1) | [Epic-Image-Generation-Pipeline.md](../../022-User-Stories/Epics/Epic-Image-Generation-Pipeline.md) |
| Use Case liên quan | [UC-06-Generate-Panel-And-Pick-Variant.md](../Use-Cases/UC-06-Generate-Panel-And-Pick-Variant.md) · [UC-07-Edit-Bubble-And-Dialogue-In-Panel.md](../Use-Cases/UC-07-Edit-Bubble-And-Dialogue-In-Panel.md) |
| BRD lân cận được trỏ trong tài liệu này | [BRD-003](./BRD-003-Comic-Director-And-Layout.md) (nguồn của `Panel Specification`) · [BRD-004](./BRD-004-Minimum-Editor.md) · [BRD-006](./BRD-006-Credit-And-Unit-Economics.md) · [BRD-007](./BRD-007-Legal-And-Compliance.md) · [BRD-008](./BRD-008-Quality-And-Operations.md) |

### 7.2 Nguồn đã trích

- [MVP-Scope.md](../../010-Planning/MVP-Scope.md) — §3 nhóm A (nguồn của mục 2), §3.1, §4.2, §4.4, §6 KC-1…KC-4 + KC-7, §7.2 G1, §7.3 G2 + đường lui
- [Charter-Comic-Studio.md](../../010-Planning/Charter-Comic-Studio.md) — §7 ràng buộc C1, C3, C6–C10
- [Risk-Register.md](../../010-Planning/Risk-Register.md) — §2.1 bảng chính, §4 khoảng trống, §5 lịch rà soát
- [Roadmap.md](../../010-Planning/Roadmap.md) — mốc và exit criteria (tài liệu duy nhất trả lời *"khi nào"*)
- [Glossary.md](../../999-Resources/Glossary.md) — *best-of-N (N=3)*, *Continuity Checker*, *Visual Prompt Compiler*, *precedence ladder*, *constraint budget*, *typeset layer*, *Panel Specification*, *credit ledger + hold*, *seam kinh tế vs seam kỹ thuật*
- [Analysis-Comic-Studio-Concept.md](../../050-Research/Analysis-Comic-Studio-Concept.md) — §4.2, §5.5, §6.2, §9b.3 (**dẫn qua** cột *Căn cứ* của `MVP-Scope` §3 và bảng Canonical Facts; tài liệu này **không sửa** Analysis — CẤM-18)
- [Documents-Template.md](../../../knowledge-base/99-Templates/Documents-Template.md) — RULE-001

---

_Created by Comic Studio — role `business-analyst`_
_Author: trisjr_
