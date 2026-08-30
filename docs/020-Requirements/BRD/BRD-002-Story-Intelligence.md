---
id: BRD-002
type: brd
status: draft
project: comic-studio
created: 2026-08-24
---

# BRD-002 — Story Intelligence

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

Biến văn bản truyện thô thành **Story Bible** truy vấn được **theo thời điểm** — đây là tài sản tích luỹ của người dùng và là **ứng viên moat thật** của sản phẩm.

Story Bible không phải một bản tóm tắt văn xuôi mà là **dữ liệu**: nhân vật, quan hệ, địa điểm, vật phẩm, sự kiện, và trạng thái của chúng tại một thời điểm bất kỳ trong truyện. Vì nó tích luỹ theo thời gian, nó vừa là switching cost của khách hàng vừa là trục cạnh tranh duy nhất mà quy mô **1 dev** có lợi thế — đối thủ có funding đang đánh vào trục **editor** (CF-5.2/5.3 `[TC]`), còn trục *Story Bible + Timeline State + Continuity* là thiết kế dữ liệu, không phải nhân lực UI.

## 2. Phạm vi module

Bảng dưới đây là **nhóm B của [MVP-Scope.md](../../010-Planning/MVP-Scope.md) §3, trích nguyên nhãn từng mốc** — không đổi nhãn, không diễn giải lại nhãn. Bốn hàng `B1–B4` thuộc phạm vi module; hàng `B5` nằm ở [mục 5](#5-cái-module-này-không-làm).

| # | Hạng mục | MVP0 | MVP1 | MVP2 | MVP3 | MVP4 | Full Scope | Căn cứ (theo `MVP-Scope` §3) |
|---|---|:--:|:--:|:--:|:--:|:--:|:--:|---|
| **B1** | Chapter parse + **text clean** (regex/heuristic, deterministic) | ❌ viết tay | ✅ | ✅ | ✅ | ✅ | ✅ | CF-8.7 — *"text clean là bước ĐẦU TIÊN"* |
| **B2** | Story Bible extraction tự động (character, location, costume) | ❌ viết tay | ✅ | ✅ | ✅ | ✅ | ✅ | CF-8.4 (*"không code extraction"*) · CF-8.7 |
| **B3** | Timeline state resolver `state_at(N) = reduce(events)` | ❌ viết tay | ✅ | ✅ | ✅ | ✅ | ✅ | Analysis §5.5 — code sở hữu state, LLM chỉ phát event |
| **B4** | Khoá thời gian đúng (thay `(chapter, scene)`) | — | ✅ | ✅ | ✅ | ✅ | ✅ | Analysis §5.1 — sai âm thầm ở flashback; **phải sửa trước dòng code đầu tiên** |

> Cờ horizon (quy ước **QC-3**): cả bốn hàng **TRONG** horizon 09/2026–02/2027. `B4` được `Roadmap` xếp ở **pre-cycle 09/2026**, tức **trước dòng code đầu tiên** — không phải một lô song song mà là **điều kiện tiên quyết**.

## 3. Yêu cầu nghiệp vụ

| ID | Phát biểu yêu cầu | Căn cứ (file + mục) | Mốc MVP |
|---|---|---|---|
| **BR-002-01** | **`text clean` là bước ĐẦU TIÊN** của pipeline ingest: rác scrape (header/footer, quảng cáo, ghi chú dịch, ký tự lỗi) bị loại **trước khi** extraction chạy. Bước này là **deterministic** (regex/heuristic), không phải LLM. | `MVP-Scope` §3 B1 · CF-8.7 · `Roadmap` §2 exit criterion **M1-2** | MVP1 ✅ (MVP0 = ❌ viết tay) |
| **BR-002-02** | Nhân vật, địa điểm, trang phục được **rút ra tự động** từ chapter để người dùng không phải khai tay toàn bộ Story Bible. | `MVP-Scope` §3 B2 · CF-8.4 · CF-8.7 · `Roadmap` §2 **M1-3** | MVP1 ✅ (MVP0 = ❌ viết tay) |
| **BR-002-03** | Ngưỡng nghiệm thu của extraction: **≥80%** entity khớp bible viết tay. ⚠️ **`[EM]` — `Roadmap` §2 ghi nguyên văn *"ngưỡng do em định nghĩa"*; cấm trích như số đo hoặc benchmark ngành.** | CF-10.5 (`findings/business-analyst.md` §5.2) · `Roadmap` §2 **M1-3** | MVP1 |
| **BR-002-04** | Story Bible là **DỮ LIỆU có cấu trúc, truy vấn được theo thời điểm** — phân biệt tuyệt đối với một bản tóm tắt văn xuôi. | `Glossary` *Story Bible* | MVP1 ✅ |
| **BR-002-05** | Story Bible tách hai trục **Identity** (bất biến qua các chương — cấu trúc khuôn mặt, dấu hiệu nhận dạng) và **Appearance** (thay đổi theo trạng thái — trang phục, vết thương, tóc). Gộp hai thứ này vào một field là **nguyên nhân của phần lớn lỗi consistency**. | `Glossary` *Identity vs Appearance* | MVP1 ✅ |
| **BR-002-06** | Trạng thái của một entity tại một thời điểm được **tính**, không được lưu sẵn: `state_at(N) = reduce(events)`. **Code sở hữu state, LLM chỉ phát event.** Toàn hệ thống có **đúng MỘT** hàm `resolveState(entity, at_event)`. | `MVP-Scope` §3 B3 (dẫn Analysis §5.5) · [Risk-Register](../../010-Planning/Risk-Register.md#21-bảng-chính) R-15 (cột *Mitigation*: *"một hàm `resolveState` duy nhất"*) | MVP1 ✅ (MVP0 = ❌ viết tay) |
| **BR-002-07** | Khoá thời gian dùng **`timeline_id` + `story_order`**, tách khỏi `reading_order` — **không** dùng `(chapter, scene)`. `story_order` là `NUMERIC` sparse (bước 1000, editable); `timeline_id` có `kind` + `anchor_order`; state neo vào `Event` mức scene. Có **test guardrail cấm `ORDER BY chapter_no`**. | `MVP-Scope` §3 B4 (dẫn Analysis §5.1) · `Glossary` *syuzhet vs fabula*, *`timeline_id`* · [Risk-Register](../../010-Planning/Risk-Register.md#21-bảng-chính) R-15 cột *Mitigation* · `Roadmap` §6.2 (phụ thuộc **cứng**) | MVP1 ✅ — `Roadmap` xếp ở **pre-cycle 09/2026** |
| **BR-002-08** | Lý do nghiệp vụ của BR-002-07 phải được giữ trong spec: `(chapter, scene)` là **thứ tự đọc**, không phải **thứ tự sự việc xảy ra** ⇒ nó **sai âm thầm ở mọi flashback**, không crash, chỉ corrupt dữ liệu. Panel hồi tưởng sẽ render trang phục/vết thương của hiện tại. | `Glossary` *syuzhet vs fabula* · [Risk-Register](../../010-Planning/Risk-Register.md#21-bảng-chính) R-15 (cột *Trigger*) | Xuyên mọi mốc |
| **BR-002-09** | Truy vấn Story Bible được thực hiện bằng **SQL + full-text search trong Postgres** — *"Story Bible **là** index của mình"*. Không đưa một index vector nào vào MVP. | CF-9.2 (`findings/business-analyst.md` §5.2) · `MVP-Scope` §4.2 (dẫn Analysis §6.2) | MVP1 ✅ |
| **BR-002-10** | Module `comic` chỉ được gọi module `story` **qua đúng hai hàm** `resolveState()` và `getBible()`; luật này được **enforce bằng lint rule**, không bằng quy ước. | `MVP-Scope` §4.2 (*"Năm seam ĐÚNG chỗ vẫn giữ"*) | MVP1 ✅ |
| **BR-002-11** | Mọi trường của Story Bible do người dùng sửa phải sinh `field_provenance` + `change_log`; Story Bible là **hồ sơ chứng minh quyền của khách hàng**, không chỉ của Founder. | `MVP-Scope` §6 **KC-2**, **KC-3** · `MVP-Scope` §8.2 điểm 2 (nghĩa vụ xuất `change_log` + `field_provenance` cho từng tenant khi KILL) · `Glossary` *`field_provenance` / `change_log`* | MVP1 |

> **`TBD` — khoảng trống không nguồn nào trong repo trả lời được** (không được viết thành phát biểu chắc chắn):
>
> | # | Khoảng trống | Trạng thái |
> |---|---|---|
> | **KT-1** | ⭐ **KHÔNG CÓ persona / JTBD / định nghĩa "đủ tốt" trong toàn repo.** Repo có **phân khúc** (CF-1.5 `[CHỐT]` — *tác giả truyện chữ KHÔNG biết vẽ*) nhưng **không có persona**. Ảnh hưởng trực tiếp tới việc định nghĩa *"Story Bible đúng"* nghĩa là gì với người dùng | `TBD` |
> | **KT-2** | **Không có design partner, không có user interview nào** — `docs/050-Research/User-Interviews/` rỗng | `TBD` |
> | **CF-10.10** | Cạnh mọi metric kỹ thuật phải có **đúng một câu người trả lời**: *"trang này đọc có ổn không?"* — và câu trả lời **được ghi lại từ MVP0**. Tiêu chí này chưa được lượng hoá ở đâu | `TBD` (định tính, có nguồn) |
>
> Nguồn xác nhận khoảng trống: `findings/business-analyst.md` §6.2.

## 4. Ràng buộc & điều kiện chặn

### 4.1 Danh sách cứng `KC-x` mà module này chạm (`MVP-Scope` §6)

| # | Ràng buộc | Module B chạm ở đâu |
|---|---|---|
| **KC-5** | `tenant_id NOT NULL` trên **MỌI** bảng, là **cột ĐẦU TIÊN** của mọi composite index, cộng **Postgres RLS** — từ **MVP1, ngày đầu** | Story Bible là nhóm bảng **nhiều nhất** của hệ thống ⇒ nếu retrofit thì đây là chỗ đắt nhất. Bỏ sót một chỗ = **rò rỉ dữ liệu chéo tenant** = sự cố tồn vong. Cơ chế thuộc [BRD-005](./BRD-005-Multi-Tenancy-And-Platform.md) |
| **KC-6** | Kiểm **opt-out signal Điều 37b** ngay trong bước **ingest** — chi phí **~0** (CF-7.5 `[OFF]` tóm tắt) | Bước ingest là `B1` của module này ⇒ ràng buộc **bind vào đường dẫn của module B**, dù requirement pháp lý (`GP-2`) thuộc [BRD-007](./BRD-007-Legal-And-Compliance.md). Ingest là nơi **DUY NHẤT** file của user lần đầu vào hệ thống |
| **KC-2** | `change_log` ghi **mọi** hành động người dùng | Mỗi lần user sửa một entity của Story Bible (căn cứ của BR-002-11) |
| **KC-3** | `field_provenance` (mức field) + `generation.origin` | Story Bible có cả field do LLM rút ra và field do người sửa ⇒ **không phân biệt được thì không xác định được ranh giới phần được bảo hộ** |

### 4.2 Ràng buộc cấp dự án `C-x` (`Charter` §7)

| # | Ràng buộc | Hệ quả cho module B |
|---|---|---|
| **C1** | Đội **1 người + AI assist**, không funding `[CHỐT]` CF-1.2 | Extraction phải là hạng mục chia được cho một người; không xây pipeline NLP tự huấn luyện |
| **C5** | **Positioning disclosure-first, nhắm writer KHÔNG nhắm artist** | ⛔ **CẤM-17**: cấm đặt requirement cho phân khúc hoạ sĩ. Primary actor của mọi UC của module này là **tác giả truyện chữ không biết vẽ** (CF-1.5 `[CHỐT]`) |
| **C9** | Thứ tự milestone cố định, **MVP1 = Story Intelligence** CF-8.3 | ⚠️ **Bẫy đánh số** (CF-10.2): `findings/architect.md` §7.2 của run trước đánh số lại milestone (ở đó *"MVP1"* = Visual Generation Loop). **CF-8.3 là canon** |
| **C10** | Horizon 6 tháng **chưa được ai xác nhận là đủ cho 1 dev** `[CHỐT]` CF-8.1 + CF-8.13 | ⛔ **CẤM-08**: cấm nén lịch cho vừa khung |

### 4.3 Điều kiện chặn khác

| Điều kiện | Nội dung |
|---|---|
| **Phụ thuộc cứng của `B4`** | `Roadmap` §6.2 xếp khoá thời gian là **phụ thuộc cứng**: làm sau MVP1 = migration toàn bộ, vì `story_order` là giả định **lan khắp mọi module**. Đây là lý do nó nằm ở **pre-cycle**, trước dòng code đầu tiên |
| **Exit criteria trong horizon** | `Roadmap` §2 **M1-2** (text clean) và **M1-3** (≥80% `[EM]`) — xem BR-002-03 về nhãn của ngưỡng |
| **G0 — Pháp lý** | ⚠️ **KHÔNG chặn MVP0 và MVP1**; G0 chặn **thương mại hoá** (⛔ **CẤM-10**) |

## 5. Cái module này KHÔNG làm

| # | Không làm | Lý do + căn cứ | Điều kiện mở lại |
|---|---|---|---|
| 1 | **`B5` — `pgvector` / vector search.** ⚠️ **KHÔNG bị cấm vĩnh viễn.** Trích nguyên nhãn từng mốc của `MVP-Scope` §3 hàng `B5`: MVP0 **❌** · MVP1 **❌** · MVP2 **❌** · MVP3 **⛔** · MVP4 **⛔** · **Full Scope 🟡** | CF-9.2 · `MVP-Scope` §4.2 (Vector DB **bỏ hẳn khỏi MVP**) · Analysis §6.2 — *"Story Bible **là** index của mình"* ⇒ lời giải mặc định là **SQL + FTS** (BR-002-09) | **Có ghi trong `MVP-Scope`**: Full Scope 🟡 *"khi có bằng chứng SQL+FTS không đủ"*. Tức đây là **hoãn có điều kiện mở lại**, không phải cắt hẳn |
| 2 | **Vector DB *riêng* như một hạ tầng** | Đây là hàng **E6** (microservices + 2 PostgreSQL + Vector DB riêng + Job Queue riêng), **cắt hẳn** ở cả Full Scope, thuộc [BRD-005](./BRD-005-Multi-Tenancy-And-Platform.md) và `Charter` §5.2 *Scope Out*. ⚠️ **Đừng lẫn với mục 1**: một cái là **hoãn có điều kiện**, một cái là **cắt hẳn** | Không mở lại |
| 3 | **Không sinh bản tóm tắt văn xuôi thay cho dữ liệu** | `Glossary` *Story Bible*: phân biệt rõ với prose — Story Bible **là dữ liệu** | Không mở lại — đây là định nghĩa |
| 4 | **Không để LLM sở hữu state ở runtime** | Analysis §5.5 (dẫn qua `MVP-Scope` §3 B3): **code sở hữu state, LLM chỉ phát event**. `Glossary` *Error cascade*: cách duy nhất thắng phép nhân lỗi là chuyển vài tầng lên **100%** bằng code deterministic | Không mở lại |
| 5 | **Không dùng `(chapter, scene)` làm khoá thời gian ở bất kỳ đường dẫn nào** | `Glossary` *syuzhet vs fabula* · R-15 (cột *Trigger*: bất kỳ đường resolve state nào chứa `ORDER BY chapter_no`) | Không mở lại |
| 6 | **Không làm Story Bible editor (UI form)** | Đó là **thành phần #5** của editor tối thiểu (`MVP-Scope` §5.2, hàng `D1`), thuộc [BRD-004](./BRD-004-Minimum-Editor.md) — dù nó chính là *"nơi moat lộ ra với khách hàng"* | — (không bị cắt, chỉ khác chủ) |
| 7 | **Không sở hữu bước kiểm opt-out Điều 37b** | Requirement là `GP-2`, thuộc [BRD-007](./BRD-007-Legal-And-Compliance.md). Module B **chịu** KC-6 vì bước đó chạy **trong** ingest của mình (xem mục 4.1) | — |
| 8 | ⛔ **Không làm copyright detection / plagiarism check / "flag nội dung khả nghi"** | **Nghịch lý safe harbour** ([Risk-Register](../../010-Planning/Risk-Register.md#21-bảng-chính) R-04): điều kiện (a) của miễn trừ Điều 198b là **"không biết"** — bộ phát hiện tạo ra đúng tri thức mà luật đang miễn trừ cho việc không có. Đây là **anti-feature** | Chỉ sau khi luật sư SHTT Việt Nam xác nhận ranh giới (R-04 cột *Residual Risk*) |
| 9 | **Không viết requirement như thể phạm vi Điều 37a đã rõ** | ⛔ **CẤM-13** · CF-7.4: hiểu biết hiện tại dựa trên **bản tóm tắt, KHÔNG phải nguyên văn** (nguồn trả 403 / paywall). Khoảng trống **KT-5** và **G-01** | Khi luật sư đọc **nguyên văn** (câu **Q1** của gate G0) |

## 6. Rủi ro chính

> [!IMPORTANT]
> Tài liệu này **không tự chấm điểm rủi ro mới** và **không lập thang Probability × Impact riêng**. Thang, Score, Trigger, Mitigation và Owner do [Risk-Register.md](../../010-Planning/Risk-Register.md) sở hữu — bảng dưới đây **chỉ trỏ tới hàng tương ứng**.

| ID | Vì sao nó là rủi ro của module B | Rà tại |
|---|---|---|
| [R-15](../../010-Planning/Risk-Register.md#21-bảng-chính) | ⭐ Rủi ro **lõi** của module: khoá thời gian `(chapter, scene)` **sai âm thầm ở flashback**; hệ quả dây chuyền là checker *"sửa"* theo state sai — **tự động làm hỏng đúng những panel đang đúng** | Tại PR/migration đầu tiên chạm schema · G1 |
| [R-16](../../010-Planning/Risk-Register.md#21-bảng-chính) | Multi-tenancy **không có trong `Request.md` một dòng nào** nhưng chiếm **15–25% effort** `[EM]`; Story Bible là nhóm bảng đông nhất phải mang `tenant_id` | Tại PR/migration đầu tiên chạm schema |
| [R-06](../../010-Planning/Risk-Register.md#21-bảng-chính) | Điều 37b (opt-out) **không được kiểm trong bước ingest** — mà ingest là bước `B1` của module này | G0 · tại PR đầu tiên chạm ingest |
| [R-04](../../010-Planning/Risk-Register.md#21-bảng-chính) | **Nghịch lý safe harbour**: một dev sẽ làm ngược điều này *theo bản năng* vì "chủ động kiểm tra" nghe như hành vi có trách nhiệm | G0 |
| [R-01](../../010-Planning/Risk-Register.md#21-bảng-chính) | Provenance của field Story Bible (`field_provenance`, `change_log`) **không backfill được** | Tại PR/migration đầu tiên chạm schema |
| [R-18](../../010-Planning/Risk-Register.md#21-bảng-chính) | Đối thủ có funding đánh trục **editor**; trục của module này (*Story Bible + Timeline State + Continuity*) là trục phòng thủ được — nhưng khoảng cách hai định vị **có thể hẹp lại** | Hàng tháng |
| [G-01](../../010-Planning/Risk-Register.md#41-năm-khoảng-trống-không-gán-score) | Khoảng trống **không gán Score**: chỉ có **bản tóm tắt** Điều 37a, không có nguyên văn ⇒ chỉ luật sư đóng được | G0 |

## 7. Tài liệu liên quan

### 7.1 Traceability

| Quan hệ | Tài liệu |
|---|---|
| Implements | [PRD-Comic-Studio.md](../PRD-Comic-Studio.md) |
| Chi tiết kỹ thuật | [SRS-Comic-Studio.md](../SRS-Comic-Studio.md) |
| Epic tương ứng (1:1) | [Epic-Story-Intelligence.md](../../022-User-Stories/Epics/Epic-Story-Intelligence.md) |
| Use Case liên quan | [UC-01-Upload-And-Ingest-Chapter.md](../Use-Cases/UC-01-Upload-And-Ingest-Chapter.md) · [UC-02-Review-And-Edit-Story-Bible.md](../Use-Cases/UC-02-Review-And-Edit-Story-Bible.md) |
| BRD lân cận được trỏ trong tài liệu này | [BRD-003](./BRD-003-Comic-Director-And-Layout.md) (khách hàng chính của `resolveState()`) · [BRD-004](./BRD-004-Minimum-Editor.md) · [BRD-005](./BRD-005-Multi-Tenancy-And-Platform.md) · [BRD-007](./BRD-007-Legal-And-Compliance.md) |

### 7.2 Nguồn đã trích

- [MVP-Scope.md](../../010-Planning/MVP-Scope.md) — §3 nhóm B (nguồn của mục 2 và mục 5 hàng `B5`), §4.2, §6 KC-2/KC-3/KC-5/KC-6, §8.2
- [Charter-Comic-Studio.md](../../010-Planning/Charter-Comic-Studio.md) — §7 ràng buộc C1, C5, C9, C10
- [Risk-Register.md](../../010-Planning/Risk-Register.md) — §2.1 bảng chính (R-01, R-04, R-06, R-15, R-16, R-18), §4.1 G-01, §5 lịch rà soát
- [Roadmap.md](../../010-Planning/Roadmap.md) — §2 M1-2/M1-3, §6.2 phụ thuộc cứng
- [Glossary.md](../../999-Resources/Glossary.md) — *Story Bible*, *syuzhet vs fabula*, *`timeline_id`*, *Identity vs Appearance*, *`field_provenance` / `change_log`*, *Error cascade*
- [Analysis-Comic-Studio-Concept.md](../../050-Research/Analysis-Comic-Studio-Concept.md) — §5.1, §5.5, §6.2 (**dẫn qua** cột *Căn cứ* của `MVP-Scope` §3 và bảng Canonical Facts; tài liệu này **không sửa** Analysis — CẤM-18)
- [Documents-Template.md](../../../knowledge-base/99-Templates/Documents-Template.md) — RULE-001

---

_Created by Comic Studio — role `business-analyst`_
_Author: trisjr_
