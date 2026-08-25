---
id: EPIC-A
type: epic
status: draft
project: comic-studio
created: 2026-08-24
---

# Epic-A — Pipeline sinh ảnh (Image Generation Pipeline)

> [!IMPORTANT]
> **Quy ước nhãn nguồn số liệu** (kế thừa nguyên vẹn — **số và nhãn là một cặp không tách rời**):
> `[OFF]` nguồn official/paper gốc · `[BCN]` báo cáo ngành có tên firm · `[TC]` nguồn thứ cấp · `[EM]` ước lượng hoặc phép nhân, **không phải số đo** · `[CHỐT]` quyết định của Founder tại gate.
>
> Epic này **chỉ trích lại** số liệu từ tầng Planning/Requirements. Không tự tra lại, không tự tính lại.
>
> **Trục Epic**: cắt theo **module A–H**, **KHÔNG** theo mốc MVP0–MVP4. Lý do: [MVP-Scope §1.1](../../010-Planning/MVP-Scope.md) phân định *"khi nào"* thuộc [Roadmap.md](../../010-Planning/Roadmap.md); Epic theo mốc tạo nguồn sự thật **thứ hai** về thời gian. ⇒ Cột *Mốc* và cờ horizon nằm ở **tầng Story**, không ở tầng Epic.

## Mục lục

1. [Implements](#1-implements)
2. [Mục tiêu Epic](#2-mục-tiêu-epic)
3. [Story trong horizon](#3-story-trong-horizon)
4. [Story ngoài horizon — chưa có file](#4-story-ngoài-horizon--chưa-có-file)
5. [Definition of Done cấp Epic](#5-definition-of-done-cấp-epic)
6. [Tài liệu liên quan](#6-tài-liệu-liên-quan)

---

## 1. Implements

Implements: [PRD-Comic-Studio](../../020-Requirements/PRD-Comic-Studio.md#a-pipeline-sinh-ảnh)

---

## 2. Mục tiêu Epic

Sinh được panel có nhân vật nhất quán từ một `Panel Specification`, ở chi phí và chất lượng cho phép **bán được**. Đây là module **duy nhất** tạo ra artifact mà khách hàng nhìn thấy — mọi module khác đều là điều kiện để module này chạy đúng. Giá trị nghiệp vụ của Epic không nằm ở *"gọi được API sinh ảnh"* (việc đó ai cũng làm được), mà nằm ở ba thứ: (a) **best-of-N với N=3** làm mặc định cho **mọi** panel — *"performance saturates at N=3"* `[OFF]` CF-3.1/3.2; ⚠️ đây là **best-of-N, KHÔNG phải retry-on-failure**, và ⛔ **CẤM lấy chất lượng của N=3 mà tính chi phí của N=2** (CẤM-03); (b) **typeset layer tách khỏi ảnh** để sửa một câu thoại không biến thành một lần đốt tiền API (CF-8.11c); (c) **Visual Prompt Compiler tất định** để *"panel sai là do spec sai, không do hệ thống ngẫu nhiên"*.

Epic này **vắt biên horizon 09/2026 → 02/2027** `[CHỐT]` CF-8.1: bốn Story mở ở **MVP0** (lát cắt mua thông tin cho gate `G1`), một Story ở **MVP1** (job queue trong Postgres), và **hai** Story rơi hẳn ra ngoài horizon ở MVP3–MVP4 `[EM]` CF-10.8. Hệ quả về kỳ vọng: trong horizon, Epic-A **không** giao một pipeline sinh ảnh ở quy mô sản xuất — nó giao **số cho gate `G1`** và **nền hạ tầng job** để MVP3 scale-up chứ không phải khám phá lại (CF-8.9).

---

## 3. Story trong horizon

> **Cột `I` / `S`**: chỉ chấm hai chữ INVEST mà việc cắt lô cần — **I** (Independent) và **S** (Small). `⚠️` = sẽ vỡ khi cắt lô ([findings §4.10](../../010-Planning/pm-runs/2026-08-24-khoi-tao-requirements-stories-comic-studio/findings/business-analyst.md)). `n/a [MVP0]` = **INVEST không áp** (xem callout ngay dưới bảng).
>
> **Cột *Mốc*** dùng quy ước `QC-3`: cờ gán theo **mốc đầu tiên** Story được giao, kèm mốc hoàn tất khi hạng mục vắt biên.

| Story (link) | Mốc | I | S | Trạng thái |
|---|---|:-:|:-:|---|
| [Story-Generate-Panel-With-Reference-And-VLM-Select](../Backlog/Story-Generate-Panel-With-Reference-And-VLM-Select.md) | MVP0 → hoàn tất MVP3 (**NGOÀI**) | `n/a [MVP0]` | `n/a [MVP0]` | chưa có file |
| [Story-Typeset-Layer-And-Bubble-Overlay](../Backlog/Story-Typeset-Layer-And-Bubble-Overlay.md) | MVP0 (bản thô) → hoàn tất MVP3 (**NGOÀI**) | `n/a [MVP0]` | `n/a [MVP0]` | chưa có file |
| [Story-Deterministic-Visual-Prompt-Compiler](../Backlog/Story-Deterministic-Visual-Prompt-Compiler.md) | MVP0 (script) → hoàn tất MVP3 (**NGOÀI**) | ✅ | ⚠️ | chưa có file |
| [Story-Image-Provider-Adapter](../Backlog/Story-Image-Provider-Adapter.md) | MVP0 (1 adapter) → hoàn tất MVP3 (**NGOÀI**) | ✅ | ✅ | chưa có file |
| [Story-Job-Queue-In-Postgres](../Backlog/Story-Job-Queue-In-Postgres.md) | MVP1 | ✅ | ✅ | chưa có file |

**5/5 Story trong horizon có mặt.**

> [!WARNING]
> **Hai Story đầu bảng mang nhãn `MVP0` — INVEST KHÔNG áp, và đó là chủ ý.**
>
> [MVP-Scope §3.1](../../010-Planning/MVP-Scope.md) và [Roadmap §3.1](../../010-Planning/Roadmap.md) đều ghi cùng một kỷ luật bắt buộc: **code của MVP0 KHÔNG phải nền của sản phẩm — viết để trả lời câu hỏi rồi bỏ, giữ lại kết luận và dữ liệu.** Với hai Story này, chấm `Independent` / `Small` là **chấm sai đối tượng**: chúng là một **lát cắt xuyên tầng**, và tiêu chí `Valuable` của chúng là **thông tin đo được**, không phải tính năng giao cho khách. Definition of Done của chúng là **5 tiêu chí gate `G1`** ([MVP-Scope §7.2](../../010-Planning/MVP-Scope.md)), không phải Acceptance Criteria kiểu Gherkin.
>
> ⛔ Dùng **đúng** tên **MVP0** — [Glossary](../../999-Resources/Glossary.md) cấm *"phase 0"*, *"spike"*, *"PoC"* (CẤM-11).
>
> ⚠️ `Story-Deterministic-Visual-Prompt-Compiler` và `Story-Image-Provider-Adapter` **cũng** mở ở MVP0 nhưng **không** thuộc danh sách năm Story `n/a` của [findings §4.9](../../010-Planning/pm-runs/2026-08-24-khoi-tao-requirements-stories-comic-studio/findings/business-analyst.md) ⇒ chúng **vẫn được chấm INVEST bình thường**.

---

## 4. Story ngoài horizon — chưa có file

| Story (link) | Mốc | I | S | Trạng thái tài liệu |
|---|---|:-:|:-:|---|
| `Story-Fairness-Per-Tenant-Job-Claim` | MVP3 | ⚠️ | ✅ | chưa có file |
| `Story-Whole-Page-Render-Granularity` | MVP3 (🟡) → hoàn tất MVP4 | ✅ | ⚠️ | chưa có file |

**2/2 Story ngoài horizon có mặt.** Tổng Epic-A = **7 Story** (5 trong / 2 ngoài).

> `Story-Whole-Page-Render-Granularity` là **đường lui đã thiết kế sẵn** của gate `G2` ([MVP-Scope §7.3](../../010-Planning/MVP-Scope.md) đường lui #1): whole-page @N=3 cho **+40%** margin vs per-panel @N=3 cho **−141%** `[EM]` CF-10.7. ⚠️ **Hai caveat bắt buộc đi kèm**: (a) **+40% vẫn DƯỚI dải kỳ vọng 50–60%** `[BCN]` CF-3.10 — nó cứu tình trạng lỗ, **không** đưa margin về mức chuẩn ngành; (b) phép so sánh **lệch hạng nguồn** (`[EM]` vs `[BCN]`) ⇒ kết luận *"vẫn dưới chuẩn"* đúng về hướng nhưng **không đủ chắc để làm ngưỡng gate**. ⛔ Đường **KHÔNG được đi**: hạ N từ 3 xuống 1.

---

## 5. Definition of Done cấp Epic

Epic-A **không** được đánh `Done` bằng phép cộng Story. Nó `Done` khi các điều kiện dưới đây đồng thời thoả — nguồn là exit criteria của [Roadmap §2](../../010-Planning/Roadmap.md) và 5 tiêu chí gate `G1` của [MVP-Scope §7.2](../../010-Planning/MVP-Scope.md).

**Phần trong horizon — bắt buộc:**

- [ ] **`P-2`**: gate `G1` có **SỐ cho cả 5 tiêu chí** và verdict được ghi (`PASS` / `PASS CÓ ĐIỀU KIỆN` / `FAIL`). ⚠️ `G1-c` và `G1-d` là ngưỡng do run trước **tự định nghĩa**, `[EM]`, **không có nguồn ngoài** (CF-10.4) — trích mà bỏ nhãn này là để chúng **mạo danh benchmark ngành**.
- [ ] **`P-3`**: regen ratio có giá trị số cho **p50 và p90** ⇒ đầu vào của gate `G2`.
- [ ] **`G1-e`**: **100%** panel có thoại dùng **overlay layer**, và **0** panel nhờ model render chữ. Đây là tiêu chí biến `Story-Typeset-Layer-And-Bubble-Overlay` từ *"đẹp thì làm"* thành **điều kiện ra của MVP0** (CF-8.11c: typeset *"nổ ngay ở panel có thoại đầu tiên"*).
- [ ] **Job queue trong Postgres** (`MVP-Scope §3` hàng **`A5`** · CF-9.2): enqueue **trong cùng transaction** với dữ liệu nghiệp vụ, claim bằng `FOR UPDATE SKIP LOCKED` ⇒ **không có job mồ côi** và **không thêm một hạ tầng queue riêng**. ⚠️ Hạng mục này **không có exit criterion `M-x` riêng** trong [Roadmap §2](../../010-Planning/Roadmap.md) — nó nằm ở cột *Deliverable* của mốc MVP1. Đừng gán cho nó một `M-number` mà nguồn không cấp.
- [ ] **N=3 là mặc định cho MỌI panel**, không phải chỉ khi panel lỗi. ⛔ Bất kỳ thay đổi hạ `N` là **đổi chất lượng lấy margin** ⇒ **phải chạy lại `G1`, không phải chỉ `G2`** (CẤM-03).
- [ ] Mọi `generation` do Epic-A tạo ra commit **cùng transaction** với `change_log` + `usage_event` — `KC-4`. Epic-A **không sở hữu** yêu cầu này (chủ là [Epic-Legal-And-Compliance](./Epic-Legal-And-Compliance.md)) nhưng **là nơi nó bị vi phạm dễ nhất**.
- [ ] ⚠️ **Ngưỡng không được sửa sau khi nhìn kết quả** (CẤM-16) — *"đó là cách một gate biến thành nghi lễ"*.

**Phần ngoài horizon — ghi ra để không ai đánh `Done` sớm:**

- [ ] **`M3-4`** (worker chết mà API vẫn phục vụ được) và fairness per tenant trong câu `CLAIM` job ⇒ **MVP3, NGOÀI horizon**.
- [ ] Whole-page render granularity chỉ được kích hoạt như **đường lui của `G2`**, và **data model KHÔNG phải đổi** khi kích hoạt.

---

## 6. Tài liệu liên quan

### 6.1 Traceability — BRD cha

| Tầng | Tài liệu |
|---|---|
| Requirements (module) | [PRD-Comic-Studio §A. Pipeline sinh ảnh](../../020-Requirements/PRD-Comic-Studio.md#a-pipeline-sinh-ảnh) — `FR-A-01` … `FR-A-07` |
| **BRD cha** | [BRD-001-Image-Generation-Pipeline](../../020-Requirements/BRD/BRD-001-Image-Generation-Pipeline.md) |
| Yêu cầu phi chức năng | [SRS-Comic-Studio](../../020-Requirements/SRS-Comic-Studio.md) |

### 6.2 Use Case liên quan

| UC | Vai trò với Epic-A |
|---|---|
| [UC-06-Generate-Panel-And-Pick-Variant](../../020-Requirements/Use-Cases/UC-06-Generate-Panel-And-Pick-Variant.md) | Luồng chính của Epic — sinh panel best-of-N (N=3) và **chọn** ứng viên |
| [UC-07-Edit-Bubble-And-Dialogue-In-Panel](../../020-Requirements/Use-Cases/UC-07-Edit-Bubble-And-Dialogue-In-Panel.md) | Tiêu thụ **typeset layer** của `FR-A-02`; UI thuộc [Epic-Minimum-Editor](./Epic-Minimum-Editor.md) |

### 6.3 Tài liệu tham khảo

| Tài liệu | Epic-A trích mục nào |
|---|---|
| [MVP-Scope.md](../../010-Planning/MVP-Scope.md) | §3 nhóm A (A1–A7) · §3.1 kỷ luật MVP0 · §6 `KC-4` · §7.2 gate `G1` · §7.3 đường lui `G2` |
| [Roadmap.md](../../010-Planning/Roadmap.md) | §2 exit criteria `P-2`, `P-3`, `M1-7`, `M3-4` · §3.1 kỷ luật MVP0 · §4 `X-c` typeset |
| [Glossary.md](../../999-Resources/Glossary.md) | `MVP0` · `Panel Specification` · `Visual Prompt Compiler` · `precedence ladder` · `constraint budget` · `typeset layer` · `Continuity Checker` |
| [findings/business-analyst.md](../../010-Planning/pm-runs/2026-08-24-khoi-tao-requirements-stories-comic-studio/findings/business-analyst.md) | §2.3 trục Epic · §4.1 bảng Story · §4.9 năm Story MVP0 · §4.10 bảy Story vỡ khi cắt lô · §5.2 canonical facts · §5.3 lệnh cấm |

---

_Created by product-owner_
_Author: trisjr_
