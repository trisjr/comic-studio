---
id: EPIC-G
type: epic
status: draft
project: comic-studio
created: 2026-08-24
---

# Epic-G — Pháp lý & compliance

> [!IMPORTANT]
> **Quy ước nhãn nguồn số liệu** (kế thừa nguyên vẹn — **số và nhãn là một cặp không tách rời**):
> `[OFF]` nguồn official/paper gốc · `[BCN]` báo cáo ngành có tên firm · `[TC]` nguồn thứ cấp · `[EM]` ước lượng hoặc phép nhân, **không phải số đo** · `[CHỐT]` quyết định của Founder tại gate.
>
> Epic này **chỉ trích lại** những gì tầng Planning và Requirements đã ghi. **⛔ Không đưa ra ý kiến pháp lý mới** — mọi phát biểu dưới đây đều mang nhãn nguồn. Không tự tra lại, không tự tính lại (`CẤM-15`).

> [!WARNING]
> **Hai hệ đánh số, CẤM để lẫn vào nhau** (`CẤM-14`): **`GP-1`…`GP-5`** là **hàng compliance** của [MVP-Scope §3](../../010-Planning/MVP-Scope.md#3-bảng-mvp-vs-full-scope). Còn **`G0` / `G1` / `G2`** là **ba gate Go/No-Go** của [MVP-Scope §7](../../010-Planning/MVP-Scope.md#7-gono-go-decision). ⛔ **Không viết tắt `G1` cho `GP-1`.**

## Mục lục

1. [Implements](#1-implements)
2. [Mục tiêu Epic](#2-mục-tiêu-epic)
3. [Story trong horizon](#3-story-trong-horizon)
4. [Story ngoài horizon — chưa có file](#4-story-ngoài-horizon--chưa-có-file)
5. [Definition of Done cấp Epic](#5-definition-of-done-cấp-epic)
6. [Tài liệu liên quan](#6-tài-liệu-liên-quan)

---

## 1. Implements

Implements: [PRD-Comic-Studio §4 — G. Pháp lý & compliance](../../020-Requirements/PRD-Comic-Studio.md#g-pháp-lý--compliance)

> Anchor trên trỏ tới **H3 `G. Pháp lý & compliance`** trong [PRD mục 4](../../020-Requirements/PRD-Comic-Studio.md#4-yêu-cầu-chức-năng-theo-8-module) — nơi chứa `FR-G-01`…`FR-G-05`. PRD §4.0 quy ước 4 ghi rõ **cấu trúc tám H3 là contract cứng**: đổi tên hoặc đổi thứ tự H3 ⇒ link này chết.

---

## 2. Mục tiêu Epic

> Giữ được **bảo hộ bản quyền cho tác phẩm của Founder VÀ của khách hàng**, và giữ được **miễn trừ trung gian**. Đây là nhóm chứa **rủi ro nhị phân duy nhất** của cả dự án.

| # | Điều làm Epic này khác các Epic khác | Hệ quả lên backlog |
|---|---|---|
| 1 | **Rủi ro nhị phân**: mọi rủi ro khác trả lời sai thì sản phẩm **kém hơn**; nhóm này trả lời sai thì sản phẩm **bất hợp pháp** (CF-7.8/7.9) | Không có Story nào của Epic này được dời với lý do *"chưa cấp thiết"* |
| 2 | Dữ liệu provenance **KHÔNG BACKFILL ĐƯỢC** — *"không lưu từ generation đầu tiên thì **vĩnh viễn** không có"* `[OFF]` CF-7.1/7.2/7.3 | Bốn trong sáu Story nằm ở **MVP1**, không phải vì tiện lịch mà vì **sau đó là quá muộn** |
| 3 | **6/6 Story bắt đầu trong horizon** — Epic duy nhất trong bốn Epic E/F/G/H không có Story nào rơi ra ngoài | [Mục 4](#4-story-ngoài-horizon--chưa-có-file) ghi *"không có"*, không phải để trống |
| 4 | Hai nghĩa vụ của Epic này neo vào **TRIGGER**, không neo vào ngày | `GP-3` neo vào *"trước lần đầu mở cho NGƯỜI NGOÀI upload"*; nghĩa vụ AI disclosure neo vào **deadline pháp lý ~01/03/2027** `[OFF]` CF-7.7 — **nằm ngay sau horizon và không dịch theo lịch dự án** |

### 2.1 Nguyên tắc chi phối cả Epic

Nghĩa vụ pháp lý *"iterative, interactive process"* đặt lên **tầng DỮ LIỆU (audit event), KHÔNG đặt lên tầng CANVAS** (CF-9.1). ⇒ **UI được tự do chọn cái rẻ; dữ liệu provenance thì không được cắt một dòng nào.**

Hệ quả trực tiếp: ⛔ `CẤM-09` — **cấm gộp *"cắt UI cây generation (`D6`)"* với *"cắt lineage (`KC-1`)"***. Hai quyết định **độc lập và trái chiều**: `D6` bị **cắt hẳn**, còn cột dữ liệu `KC-1` **vẫn bắt buộc**.

### 2.2 Hai giới hạn hiểu biết phải mang theo

> [!CAUTION]
> 1. ⛔ **CẤM viết requirement như thể phạm vi Điều 37a đã rõ** (`CẤM-13` · ⚠️ CF-7.4). Hiểu biết hiện tại dựa trên **bản tóm tắt, KHÔNG phải nguyên văn** — nguồn gốc trả `403` hoặc paywall. **Luật sư phải đọc nguyên văn.**
> 2. ⚠️ **`TBD`**: Điều 198b có áp cho SaaS **xử lý/biến đổi** nội dung (không phải hosting thuần) hay không — **chưa ai trả lời**. Đây là **câu Q3 của G0**.
>
> Và điều dễ đọc sai nhất của cả bộ tài liệu: ⛔ **`BLOCKER-01` / gate `G0` chặn THƯƠNG MẠI HOÁ, KHÔNG chặn MVP0–MVP1** (`CẤM-10` · [Charter §9.2](../../010-Planning/Charter-Comic-Studio.md#9-tiêu-chí-thành-công--gono-go)). Đọc thành *"phải chờ luật sư mới được viết dòng code đầu tiên"* là **cách hiểu nhầm đắt nhất** mà tài liệu này có thể gây ra.

---

## 3. Story trong horizon

**6 Story** — **6/6** bắt đầu trong horizon **09/2026 → 02/2027** `[CHỐT]` CF-8.1.

> **Cách đọc cột `I` / `S`**: chỉ chấm **I** (Independent) và **S** (Small). `⚠️` = sẽ vỡ · `⚠️⚠️` = vỡ ở mức nặng nhất của cả backlog.
>
> ⚠️ **File Story chưa tồn tại** — chúng được tạo ở lô sau với **đúng** những tên dưới đây.

| Story (link) | Mốc | I | S | Trạng thái |
|---|---|:-:|:-:|---|
| [Story-Provenance-Chain-Parent-Generation](../Backlog/Story-Provenance-Chain-Parent-Generation.md) | MVP1 | ⚠️⚠️ | ⚠️ | `[TRONG HORIZON]` · hoàn tất **MVP1** · ⚠️⚠️ **vỡ `I`**: `KC-1` + `KC-3` **gắn với nhau về giá trị pháp lý** — có `parent_generation_id` mà thiếu `field_provenance` ⇒ **không xác định được ranh giới phần được bảo hộ**. Cắt thành hai lô cho ra **hai lô đều không đủ** chứng minh Điều 5a. Là **BLOCKER-04 — chặn MỌI THỨ** |
| [Story-Provenance-Committed-In-Same-Transaction](../Backlog/Story-Provenance-Committed-In-Same-Transaction.md) | MVP1 | ⚠️⚠️ | ⚠️⚠️ | `[TRONG HORIZON]` · hoàn tất **MVP1** · ⚠️⚠️ **`KC-4` là một THUỘC TÍNH của ba Story khác, không phải một feature**. Nó phụ thuộc [`Story-Modular-Monolith-Three-Schemas`](../Backlog/Story-Modular-Monolith-Three-Schemas.md) (một DB ⇒ một transaction boundary) và **được chứng minh bằng một TEST, không bằng một màn hình** — *"bằng chứng có thể thiếu ngẫu nhiên thì không phải bằng chứng"* |
| [Story-Opt-Out-Check-At-Ingest](../Backlog/Story-Opt-Out-Check-At-Ingest.md) | MVP1 | ✅ | ✅ | `[TRONG HORIZON]` · hoàn tất **MVP1** · `KC-6`; chi phí **~0** `[OFF]` CF-7.5. Bước ingest là nơi **DUY NHẤT** file của user lần đầu vào hệ thống ⇒ kiểm ở chỗ khác nghĩa là **đã xử lý nội dung có opt-out trước khi biết** |
| [Story-ToS-User-Warrant-And-Tenant-Hard-Delete](../Backlog/Story-ToS-User-Warrant-And-Tenant-Hard-Delete.md) | MVP1 | ✅ | ⚠️ | `[TRONG HORIZON]` · hoàn tất **MVP1** · `GP-5`, `ON DELETE CASCADE` + đường hard-delete tenant **ĐÃ KIỂM THỬ**. *"Đường thoát phải được xây cùng lúc với đường vào"*; khi kill có trật tự, mỗi tenant phải xuất được **cả `change_log` + `field_provenance`** — đó là hồ sơ chứng minh quyền tác giả **của khách** ([MVP-Scope §8](../../010-Planning/MVP-Scope.md#8-điều-kiện-thoát-kill-criteria)) |
| [Story-Safe-Harbour-Checklist-Article-198b](../Backlog/Story-Safe-Harbour-Checklist-Article-198b.md) | MVP2 | ✅ | ⚠️ | `[TRONG HORIZON]` · hoàn tất **MVP2**, *hoặc sớm hơn nếu trigger đến sớm* · `GP-3`: công cụ takedown · đăng ký đầu mối với **Bộ VHTTDL** · **SLA 72 giờ** `[OFF]` CF-7.6 · **KHÔNG chủ động rà soát nội dung** · user warrant + indemnify trong ToS · kiểm opt-out trước khi xử lý — **tick đủ 6/6**. ⚠️ Neo vào **TRIGGER** *trước lần đầu mở cho NGƯỜI NGOÀI upload*, **không neo vào một ngày**. Là **BLOCKER-02** |
| [Story-AI-Disclosure-Article-11](../Backlog/Story-AI-Disclosure-Article-11.md) | MVP1 (🟡) | ✅ | ⚠️ | `[TRONG HORIZON]` · **hoàn tất MVP3 (NGOÀI horizon)** theo quy ước cờ **QC-3** (cờ gán theo mốc **đầu tiên** Story được giao) · `GP-4`, nghĩa vụ AI disclosure của **Luật TTNT 2025** — nghĩa vụ **nội địa Việt Nam**, deadline tuân thủ **~01/03/2027** `[OFF]` CF-7.7. ⚠️ **HAI NGUỒN MÔ TẢ PHẠM VI KHÁC NHAU** ⇒ **thiết kế theo diễn giải RỘNG cho tới khi luật sư chốt**; phạm vi thật là **`TBD`** và nó là **câu Q2 của G0** |

> **Ghi chú về tên file `Story-AI-Disclosure-Article-11`**: tên này được **copy nguyên** từ [findings §4.7](../../010-Planning/pm-runs/2026-08-24-khoi-tao-requirements-stories-comic-studio/findings/business-analyst.md) — lô sau phải tạo Story bằng **đúng** tên đó. Nội dung nghĩa vụ mà repo ghi lại là **AI disclosure theo Luật TTNT 2025** (`GP-4` · `[OFF]` CF-7.7); Epic này **không** khẳng định thêm bất kỳ số hiệu điều luật nào ngoài những gì repo đã ghi.

---

## 4. Story ngoài horizon — chưa có file

**KHÔNG CÓ.**

| Story ngoài horizon | Trạng thái tài liệu |
|---|---|
| **không có** — **6/6** Story của Epic-G bắt đầu trong horizon (`GP-4` hoàn tất ở MVP3 nhưng **bắt đầu** ở MVP1 🟡, nên theo quy ước **QC-3** nó là `[TRONG HORIZON]`) | — |

> [!IMPORTANT]
> ⛔ **Epic-G KHÔNG có Story cho gate `G0`** (ba câu hỏi CF-7.8 gửi luật sư SHTT). **Đây là chủ ý, không phải bỏ sót.**
>
> **Vì sao**: `G0` là một **hoạt động**, không phải một increment sản phẩm. Nó đã có chủ: [Roadmap §3.1](../../010-Planning/Roadmap.md#31-pre-cycle-092026--ba-việc-trước-dòng-code-đầu-tiên) **việc 1** và exit criterion **P-1** (*3/3 câu CF-7.8 đã gửi tới **một luật sư SHTT VN có tên**, có xác nhận đã nhận*).
>
> **Đưa nó vào backlog là biến một BLOCKER thành một ticket có thể "dời sprint sau".** Đó là cơ chế mà rủi ro nhị phân duy nhất của dự án bị làm cho trông giống một hạng mục thương lượng được.
>
> ⚠️ Và nhắc lại `CẤM-10` để ghi chú này không bị đọc lệch: **`G0` chặn THƯƠNG MẠI HOÁ, KHÔNG chặn MVP0–MVP1.** Không có Story cho `G0` **không** có nghĩa là `G0` không quan trọng — nghĩa là nó được theo dõi ở tầng **gate/Roadmap**, đúng tầng của nó.

---

## 5. Definition of Done cấp Epic

### 5.1 Điều kiện ra — nguồn là `Roadmap` §2

| # | Tiêu chí | Nguồn |
|---|---|---|
| 1 | **5 hạng mục provenance** (`parent_generation_id`, `relation_kind`, `change_log`, `field_provenance`, `generation.origin`) **tồn tại** | **M1-5** |
| 2 | ⭐ **Có TEST chứng minh 5 hạng mục đó commit CÙNG MỘT transaction** với artifact mà chúng chứng minh | **M1-5** · `KC-4` |
| 3 | **100%** file upload đi qua bước kiểm **opt-out Điều 37b** | **M1-4** · `KC-6` |
| 4 | `ON DELETE CASCADE` + đường **hard-delete tenant đã kiểm thử**; tenant xuất được **cả `change_log` + `field_provenance`** | `FR-G-05` · [MVP-Scope §8](../../010-Planning/MVP-Scope.md#8-điều-kiện-thoát-kill-criteria) |
| 5 | Checklist safe harbour Điều 198b hoàn thành **6/6 mục** — **nếu** trigger *"mở cho người ngoài upload"* đã đến | **M2-6** · [Roadmap §4](../../010-Planning/Roadmap.md#4-ba-việc-xen-ngang) **X-a** |
| 6 | Nghĩa vụ AI disclosure được **thiết kế theo diễn giải RỘNG**; phạm vi thật giữ nhãn **`TBD`** cho tới khi luật sư chốt (**Q2 của G0**) | `FR-G-04` · ⚠️ CF-7.7 |

> ⚠️ **Tiêu chí #2 là một TEST, không phải một màn hình.** `KC-4` là **thuộc tính của ba Story khác** — nó không có UI để demo. Nghiệm thu bằng cách khác (ví dụ *"đã thấy đủ 5 cột trong DB"*) **không** chứng minh được điều mà `M1-5` yêu cầu.
>
> ⚠️ **Tiêu chí #1 và #2 chỉ "xong" cùng nhau.** Có `parent_generation_id` mà thiếu `field_provenance` ⇒ **không xác định được ranh giới phần được bảo hộ** — hai lô đều không đủ chứng minh Điều 5a.

### 5.2 Bốn điều KHÔNG thuộc DoD của Epic này

1. ⛔ **Không** có tiêu chí nào cho **gate `G0`** — lý do đã ghi tường minh ở [mục 4](#4-story-ngoài-horizon--chưa-có-file). `G0` thuộc `Roadmap §3.1` việc 1 + **P-1**.
2. ⛔ **Không** có tiêu chí *"cập nhật MOC"* — **PM giữ MOC** ở close-step của run.
3. ⛔ **Không** có tiêu chí về UI cây generation (`D6`) — **`D6` bị cắt hẳn**, nhưng ⚠️ **cột dữ liệu `KC-1` vẫn bắt buộc** (`CẤM-09`). Đây là cặp mà [MVP-Scope §3.1](../../010-Planning/MVP-Scope.md#3-bảng-mvp-vs-full-scope) gọi là *"rất dễ bị gộp làm một"*.
4. ⛔ **Không** có tiêu chí nào diễn giải phạm vi **Điều 37a** — `CẤM-13`. Repo chỉ có **bản tóm tắt**; việc đọc nguyên văn thuộc luật sư.

---

## 6. Tài liệu liên quan

### 6.1 BRD cha & tầng Requirements

| Quan hệ | Tài liệu | Ghi chú |
|---|---|---|
| **BRD cha** | [BRD-007-Legal-And-Compliance](../../020-Requirements/BRD/BRD-007-Legal-And-Compliance.md) | **1:1 với Epic này** |
| PRD | [PRD-Comic-Studio — G. Pháp lý & compliance](../../020-Requirements/PRD-Comic-Studio.md#g-pháp-lý--compliance) | `FR-G-01`…`FR-G-05` |
| NFR chi tiết | [SRS-Comic-Studio](../../020-Requirements/SRS-Comic-Studio.md) | *Auditability & lineage* là trục NFR số 2 của SRS |
| Epic phụ thuộc chéo | [Epic-Multi-Tenancy-And-Platform](./Epic-Multi-Tenancy-And-Platform.md) · [Epic-Minimum-Editor](./Epic-Minimum-Editor.md) · [Epic-Credit-And-Unit-Economics](./Epic-Credit-And-Unit-Economics.md) | `KC-4` cần **một** transaction boundary (modular monolith) · `change_log` phát sinh trong editor · `usage_event` là một trong ba thứ phải commit cùng transaction |

### 6.2 Use Case liên quan

| Use Case | Vì sao liên quan |
|---|---|
| [UC-01 — Upload And Ingest Chapter](../../020-Requirements/Use-Cases/UC-01-Upload-And-Ingest-Chapter.md) | Nơi **opt-out Điều 37b** (`GP-2` / `KC-6`) sống — bước ingest là nơi **DUY NHẤT** file của user lần đầu vào hệ thống. Cũng là nơi gắn checkbox **user warrant** của `GP-5` |
| [UC-11 — Handle Takedown Request](../../020-Requirements/Use-Cases/UC-11-Handle-Takedown-Request.md) | Luồng của `GP-3`. **Primary actor là chủ sở hữu quyền — một actor NGOÀI hệ thống**; SLA **72 giờ** `[OFF]` CF-7.6 |
| [UC-06 — Generate Panel And Pick Variant](../../020-Requirements/Use-Cases/UC-06-Generate-Panel-And-Pick-Variant.md) | Nơi *"đã chọn X thay vì Y"* xảy ra — hành động sáng tạo **rẻ nhất mà giá trị pháp lý cao nhất**, và là nơi `parent_generation_id` + `relation_kind` được ghi |

### 6.3 Tài liệu tham khảo

- [MVP-Scope.md](../../010-Planning/MVP-Scope.md) — **§3** nhóm G (`GP-1`…`GP-5`, nguồn của [mục 3](#3-story-trong-horizon)) · **§6 KC-1, KC-2, KC-3, KC-4, KC-6** · **§7** ba gate, [G0](../../010-Planning/MVP-Scope.md#71-g0--gate-pháp-lý) và ba câu hỏi · **§8** (nghĩa vụ khi KILL) · **§4** (`§4.4` `parent_generation` **KHÔNG CẮT**)
- [Roadmap.md](../../010-Planning/Roadmap.md) — **§2** exit criteria **P-1**, **M1-4**, **M1-5**, **M2-6** (nguồn của [mục 5](#5-definition-of-done-cấp-epic)) · **§3.1** việc 1 (chủ sở hữu của `G0`) · **§4** **X-a**
- [Charter-Comic-Studio.md](../../010-Planning/Charter-Comic-Studio.md) — **§7** ràng buộc **C4** · **§9** `BLOCKER-01`, `BLOCKER-02`, `BLOCKER-04` và §9.2 (`CẤM-10`)
- [Glossary.md](../../999-Resources/Glossary.md) — `field_provenance / change_log` · `usage_event` · `HITL gate` · `MVP0`
- [findings/business-analyst.md](../../010-Planning/pm-runs/2026-08-24-khoi-tao-requirements-stories-comic-studio/findings/business-analyst.md) — **§2.3** · **§4.7** (bảng 6 Story của Epic này + ghi chú *"không có Story cho G0"*) · **§4.10** (hai Story provenance vỡ INVEST) · **§5.2** canonical facts CF-7.1…CF-7.9, CF-10.1, CF-10.2 · **§5.3** lệnh cấm `CẤM-09`, `CẤM-10`, `CẤM-13`, `CẤM-14`
- [Documents-Template.md](../../../knowledge-base/99-Templates/Documents-Template.md) — **RULE-001**: thư mục, naming `Epic-{Title}.md`, frontmatter, **standard markdown link** (⛔ cấm wiki-link `[[...]]`)

> ⛔ **Không link tới `docs/030-Specs/`** — tầng technical spec chưa tồn tại và nằm ngoài scope của run này.
