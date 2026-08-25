---
id: BACKLOG-PRIORITY-001
type: backlog-priority
status: draft
created: 2026-08-24
---

# Prioritized Backlog — comic-studio

> [!IMPORTANT]
> **Quy ước nhãn nguồn** (kế thừa nguyên vẹn từ tầng Planning và từ `findings/business-analyst.md`, số và nhãn là một cặp không tách rời): `[OFF]` official/paper gốc · `[BCN]` báo cáo ngành có tên firm · `[TC]` thứ cấp · `[EM]` ước lượng/ngưỡng tự định nghĩa — **không phải số đo** · `[CHỐT]` quyết định của Founder tại gate.
>
> **Tài liệu này là VIEW XẾP HẠNG DẪN XUẤT (derived ranking view), KHÔNG PHẢI nguồn sự thật độc lập.** Xung đột với `Roadmap.md` hoặc `MVP-Scope.md` ⇒ **`Roadmap`/`MVP-Scope` THẮNG TUYỆT ĐỐI** — hàng backlog sai phải được sửa hoặc xoá, không bao giờ sửa `Roadmap`/`MVP-Scope` để khớp bảng này.
>
> **22 nhãn `[* suy luận]`** (`[PO suy luận]` / `[Kiến trúc suy luận]` / `[Security suy luận]` / `[QA suy luận]`) xuất hiện trong các file `Story-*.md` khi writer phải tự suy lý do `I`/`S` vỡ hoặc tự neo anchor mà nguồn không đặt tên. Khi một giá trị trong bảng dưới đây dẫn xuất từ một ô mang nhãn đó, nhãn được **giữ nguyên**, không âm thầm biến mất.

## Mục lục

1. [Mục đích & ranh giới](#1-mục-đích--ranh-giới)
2. [Cách đọc bảng backlog](#2-cách-đọc-bảng-backlog)
3. [Backlog theo mốc](#3-backlog-theo-mốc)
4. [MVP Stories — danh sách rút gọn](#4-mvp-stories--danh-sách-rút-gọn)
5. [Story chưa xếp được](#5-story-chưa-xếp-được)
6. [Lịch chấm lại](#6-lịch-chấm-lại)
7. [Tài liệu tham khảo](#7-tài-liệu-tham-khảo)

---

## 1. Mục đích & ranh giới

**Độc giả đích**: Founder khi chọn *"làm gì tiếp"* trong phạm vi một mốc đã được `Roadmap` ấn định.

| Tài liệu | Trả lời câu hỏi | KHÔNG trả lời |
|---|---|---|
| [Roadmap.md](../010-Planning/Roadmap.md) | **Khi nào, theo thứ tự nào, exit criteria từng mốc** | Thứ tự trong nội bộ một mốc |
| [MVP-Scope.md](../010-Planning/MVP-Scope.md) | **Cái gì vào MVP0–MVP4, cái gì bị cắt/hoãn, Go/No-Go** | Ngày tháng, thứ tự thời gian |
| [OKRs.md](../010-Planning/OKRs.md) | **Đo thành công bằng gì** | Việc nào làm trước |
| **`Backlog-Priority.md`** *(tài liệu này)* | **Trong MỘT mốc đã cho: Story nào làm trước Story nào, và Story nào là MVP Story** | **Mốc nào đến khi nào — và bất kỳ ngày tháng nào** (→ `Roadmap`) · nội dung + Acceptance Criteria của Story (→ `Story-{Title}.md`) |

> [!CAUTION]
> **`Roadmap.md` THẮNG. Luôn luôn. Không có ngoại lệ.**
>
> `Backlog-Priority.md` là **VIEW XẾP HẠNG DẪN XUẤT**, **KHÔNG** phải nguồn độc lập. Nếu `Backlog-Priority` và `Roadmap`/`MVP-Scope` nói khác nhau ⇒ **HÀNG BACKLOG ĐÓ SAI**, không phải `Roadmap` sai. Xử lý = sửa hoặc **xoá hàng đó**. Không bao giờ sửa `Roadmap.md` để khớp bảng backlog. (Mượn nguyên luật đã có ở `OKRs.md` §1.1: *"KR đó sai, không phải Roadmap sai"*.)
>
> ⛔ **Guardrail cơ học: CẤM mọi ngày tháng.** File này chỉ được chứa **tên mốc** (`Pre-cycle/MVP0`, `MVP1`, `MVP2`, `MVP3`, `MVP4`). Bất kỳ định dạng năm dương lịch, ký hiệu quý lịch, hay đơn vị thời lượng lịch (loại "N đơn vị 7-ngày", "đơn vị 30-ngày thứ N") nào xuất hiện trong file này là **đã drift** — chỉ `Roadmap.md` được giữ độc quyền những thứ đó.

**Bốn cơ chế giữ đồng bộ** (kế thừa nguyên từ `findings/product-owner.md` §2.3):

| # | Cơ chế | Nội dung |
|---|---|---|
| **S1** | Cột `Anchor` bắt buộc, không được trống | Mỗi hàng phải trích ≥1 hạng mục `MVP-Scope §3` **và** ≥1 exit criterion `Roadmap` (dạng `P-x`/`M1-x`/`M2-x`/`G1-x`). Không trích được ⇒ đưa vào [mục 5](#5-story-chưa-xếp-được) |
| **S2** | Hai cột kế thừa, CẤM chấm lại | `Mốc` và `Scope-Label` là **copy** từ `MVP-Scope §3` / `Roadmap §2`, không phải phán đoán mới của file này |
| **S3** | CẤM ngày tháng | Xem guardrail ở trên |
| **S4** | Cùng nhịp rà với OKR, không thêm nhịp | Xem [mục 6](#6-lịch-chấm-lại) |

---

## 2. Cách đọc bảng backlog

> [!NOTE]
> **Framework là `UNLOCK-ORDER`, KHÔNG PHẢI RICE, KHÔNG PHẢI MoSCoW.** Hai framework đó đã bị bác tại gate của run (`findings/product-owner.md` §1). Cột kế thừa (`Mốc`, `Scope-Label`) chấm một lần ở `MVP-Scope.md`/`Roadmap.md`, copy nguyên sang đây. Cột `I`/`B`/`G` và toàn bộ `Rank` là **đề xuất của `product-owner`, Founder chốt** — không phải số đo.

### 2.1 Rank — lexicographic 3 khoá, chỉ trong phạm vi một mốc

Không nhân, không cộng, **không có điểm tổng**. So khoá 1 trước; bằng nhau thì so khoá 2; bằng nữa thì khoá 3. `Rank` (cột `#`) reset về `1` ở mỗi mốc.

| Khoá | Thang | Định nghĩa |
|---|---|---|
| **1. `I` — Irreversibility** | `I2` | Không backfill được — không làm bây giờ ⇒ dữ liệu/quyền quá khứ mất **vĩnh viễn** |
| | `I1` | Sửa sau được, nhưng là migration trên dữ liệu thật |
| | `I0` | Sửa sau gần như miễn phí |
| **2. `B` — Blocking degree** | `B2` | Nằm trên một hàng **Cứng** của `Roadmap §6.2` (bảng phụ thuộc) |
| | `B1` | Chặn ≥1 Story khác một cách quan sát được, nhưng không nằm trên hàng `Cứng` nào của §6.2 |
| | `B0` | Không chặn gì |
| **3. `G` — Gate proximity** | `G2` | Story **chính là** một exit criterion (`P-x`/`M1-x`/`M2-x`/`G1-x`) |
| | `G1` | Cần thiết **để** exit criterion đó đo được, nhưng không tự nó là con số |
| | `G0` | Không nằm trên đường tới gate/exit criterion nào của mốc |

**Tie-break khi I/B/G bão hoà (đã xảy ra thật trong `MVP1`)**, theo đúng thứ tự T1→T4:

| # | Tie-break | Áp dụng trong file này |
|---|---|---|
| **T1** | Phụ thuộc kỹ thuật trực tiếp, quan sát được (A chặn B ⇒ A trước B) | Ví dụ: `Chapter-Ingest-And-Text-Clean` trước `Story-Bible-Extraction` (M1-2 là bước ĐẦU TIÊN trước extraction); `Tenant-Id-And-RLS-Everywhere` trước mọi Story multi-tenant khác (Roadmap §6.2: *"chặn mọi tính năng multi-tenant sau đó"*) |
| **T2** | `E_hitl` thấp trước | Áp khi T1 không phân biệt được |
| **T3** | `E_build` thấp trước | Áp khi T1, T2 vẫn bằng nhau. **Quy ước cho `TBD`**: một `E_build`/`E_hitl` đã biết luôn xếp trước một giá trị `TBD` ở cùng bậc — đây là quy ước đọc bảng, không phải so sánh số học, vì `TBD` không phải 0 |
| **T4** | Founder quyết, ghi 1 dòng lý do vào cột `Ghi chú` | ⚠️ **Không dùng được trong lần dựng bảng này** — writer không có kênh hỏi Founder. Ở những hàng lẽ ra cần T4, cột `Ghi chú` ghi *"T4 chờ Founder — thứ tự tạm theo id"* thay vì bịa lý do Founder |

### 2.2 Schema 15 cột (cố định, không thêm/bớt)

| # | Cột | Ý nghĩa |
|---|---|---|
| 1 | `#` | `Rank` trong mốc, reset về 1 ở mỗi mốc |
| 2 | `Story` | Link tới Story |
| 3 | `Epic` | Epic cha |
| 4 | `Mốc` | Kế thừa từ `MVP-Scope §1.3`/`Roadmap §2` — cấm chấm lại |
| 5 | `MVP` | `⭐` hoặc để trống |
| 6 | `Hạng mục` | ID `MVP-Scope §3` (`A1`…`H6`) |
| 7 | `Scope-Label` | Kế thừa từ ô giao (hạng mục × mốc) của `MVP-Scope §3` — cấm chấm lại |
| 8 | `I` | `I2`\|`I1`\|`I0` |
| 9 | `B` | `B2`\|`B1`\|`B0` |
| 10 | `G` | `G2`\|`G1`\|`G0` |
| 11 | `E_build` | Giờ-người Founder để implement, hoặc `TBD` |
| 12 | `E_hitl` | Giờ-người/chapter cho HITL gate mà Story tạo/tiêu thụ, `0`, hoặc `TBD` |
| 13 | `Anchor` | `MVP-Scope §3 {ID} · Roadmap {exit-criterion}` |
| 14 | `Ràng buộc cứng` | `KC-1`…`KC-7` hoặc `—` |
| 15 | `Ghi chú` | Chỉ dùng cho lý do T4 |

> [!WARNING]
> **Cột 11 và 12 là hai đại lượng KHÁC NHAU, cấm cộng/trừ cho nhau** — `E_build` là chi phí một lần, `E_hitl` là nghĩa vụ lặp lại vĩnh viễn mỗi chapter. Cùng loại cảnh báo với `CF-6.7` vs `CF-6.8` (`MVP-Scope §5.1`).

### 2.3 Đánh dấu `⭐` MVP Story — quy tắc suy ra được từ cột

> **`⭐` ⟺ `Mốc ∈ {Pre-cycle/MVP0, MVP1, MVP2}` VÀ `Scope-Label ∈ {✅, 🟡}` VÀ `G ∈ {G2, G1}`.**
>
> ⚠️ **Đúng MỘT ngoại lệ, xem footnote tại [§3.1](#31-pre-cyclemvp0)**: hàng `Story-Fix-Narrative-Time-Key` có `Scope-Label = —` (ô giao `B4` × MVP0 trong `MVP-Scope §3` thật sự là `—`, không thuộc enum `{✅,🟡,⛔,❌}` — copy nguyên theo quy tắc *"cấm chấm lại"*) nhưng **vẫn** được `⭐` vì `P-4`/`B4` là `I2`/`B2`/`G2`. Ngoại lệ này **cần Founder xác nhận** tại lần chấm lại đầu tiên. Ghi ở đây để công thức tự đủ — verify L22 nêu rằng phải đọc chéo §3.1 mới phát hiện được.

Nghĩa là: *"Story bắt buộc phải xong để một exit criterion của một mốc trong horizon đạt được"*. Horizon = `Pre-cycle/MVP0` + `MVP1` + `MVP2` (Roadmap §1.2: MVP3/MVP4 nằm ngoài horizon — xem `Roadmap.md` cho khung thời gian chính xác, không lặp lại ở đây). Mọi hàng trong [mục 3](#3-backlog-theo-mốc) đã nằm trong horizon nên điều kiện 1 luôn đúng ở đó; `⭐` do đó phụ thuộc thuần vào `Scope-Label` và `G`.

> [!WARNING]
> Điều kiện `G ∈ {G2, G1}` **cố ý loại** một số hàng `✅`/`🟡` trong horizon — không phải lỗi bỏ sót. Hai ví dụ thật: `Story-Log-Preference-Data` (H2, `✅` ở MVP1 nhưng không ứng với exit criterion `M1-x` nào ⇒ `G0`, không `⭐`) và `Story-Minimum-Abuse-Controls` (H5, `🟡` ở MVP1, chỉ được nhắc trong ghi chú Roadmap §4 X-b ⇒ `G0`, không `⭐`). Hai Story này **vẫn phải làm ở MVP1** — nhãn `Scope-Label` là bắt buộc — nhưng không phải *MVP Story* theo nghĩa hẹp trên.

---

## 3. Backlog theo mốc

> Cột `Hạng mục` dùng ID của `MVP-Scope §3`. Khi 2 Story cùng chạm một hạng mục cha (ví dụ `D1` — Editor tối thiểu 5 thành phần, hoặc `GP-1` — 5 cột provenance), `Scope-Label` copy nguyên ô giao (hạng mục × mốc) của hạng mục cha đó cho cả hai Story. `Rank` reset về `1` ở mỗi H3 dưới đây.

### 3.1 Pre-cycle/MVP0

> ⚠️ **Ghi chú mốc**: 5 trong 8 Story dưới đây thuộc nhóm **"5 Story MVP0 — INVEST không áp"** (`findings/business-analyst.md` §4.9): `Story-Generate-Panel-With-Reference-And-VLM-Select`, `Story-Typeset-Layer-And-Bubble-Overlay`, `Story-Comic-IR-Panel-Specification`, `Story-Golden-Dataset-For-Regression`, `Story-Record-Readability-Human-Judgement`. `Rank` vẫn áp cho cả nhóm (UNLOCK-ORDER không phải INVEST), chỉ có tiêu chí `Small`/`Independent` là được miễn.
>
> ⚠️ **Ngoại lệ cơ học ở hàng `Story-Fix-Narrative-Time-Key`**: ô `Scope-Label` của hạng mục `B4` tại cột MVP0 trong `MVP-Scope §3` là `—` (không phải một trong bốn ký hiệu `✅`/`🟡`/`⛔`/`❌`) — **copy nguyên `—` theo đúng quy tắc S2 "cấm chấm lại"**, không suy diễn thành `🟡`. Story này được xếp vào mốc `Pre-cycle/MVP0` vì đó là **exit criterion `P-4`** của `Roadmap §2` (schema draft khoá thời gian), một hoạt động Pre-cycle mà bảng `MVP-Scope §3` (vốn chỉ có cột MVP0…MVP4) không có ký hiệu tương ứng. Vì `P-4`/`B4` rõ ràng là `I2`/`B2`/`G2` theo đúng cụm đã nêu ở `findings/product-owner.md` §1.4(c), hàng này **vẫn được đánh dấu `⭐`** dù `Scope-Label` không nằm trong enum `{✅,🟡}` — ngoại lệ này cần Founder xác nhận lại tại lần chấm lại đầu tiên.

| # | Story | Epic | Mốc | MVP | Hạng mục | Scope-Label | I | B | G | E_build | E_hitl | Anchor | Ràng buộc cứng | Ghi chú |
|--:|---|---|---|:--:|---|:--:|:--:|:--:|:--:|---|---|---|---|---|
| 1 | [Story-Fix-Narrative-Time-Key](./Backlog/Story-Fix-Narrative-Time-Key.md) | [Epic-Story-Intelligence](./Epics/Epic-Story-Intelligence.md) | Pre-cycle/MVP0 | ⭐ | B4 | — | I2 | B2 | G2 | 8h `[EM]` | 0 | MVP-Scope §3 B4 · Roadmap P-4 · §6.2 (chặn mọi bảng timeline MVP1) | — | Xem ngoại lệ `Scope-Label` ở trên |
| 2 | [Story-Record-Readability-Human-Judgement](./Backlog/Story-Record-Readability-Human-Judgement.md) | [Epic-Quality-And-Operations](./Epics/Epic-Quality-And-Operations.md) | Pre-cycle/MVP0 | | H6 | ✅ | I2 | B0 | G0 | ~4h `[EM]` | TBD | MVP-Scope §3 H6 · Roadmap P-6 (anchor `[QA suy luận]` — không có mã exit-criterion riêng cho readability) | — | |
| 3 | [Story-Golden-Dataset-For-Regression](./Backlog/Story-Golden-Dataset-For-Regression.md) | [Epic-Quality-And-Operations](./Epics/Epic-Quality-And-Operations.md) | Pre-cycle/MVP0 | ⭐ | H6 | ✅ | I1 | B1 | G2 | ~6h `[EM]` | 0 | MVP-Scope §3 H6 · Roadmap P-6 · §6.2 (dòng "Mềm" — chặn eval kit M1-6) | — | |
| 4 | [Story-Comic-IR-Panel-Specification](./Backlog/Story-Comic-IR-Panel-Specification.md) | [Epic-Comic-Director-And-Layout](./Epics/Epic-Comic-Director-And-Layout.md) | Pre-cycle/MVP0 | ⭐ | C1 | 🟡 | I1 | B1 | G1 | ~20h `[EM]` — vượt trần | 0 | MVP-Scope §3 C1 · Roadmap G1-d (nền cho C5/C6 cắm vào) | — | |
| 5 | [Story-Generate-Panel-With-Reference-And-VLM-Select](./Backlog/Story-Generate-Panel-With-Reference-And-VLM-Select.md) | [Epic-Image-Generation-Pipeline](./Epics/Epic-Image-Generation-Pipeline.md) | Pre-cycle/MVP0 | ⭐ | A1 | ✅ | I0 | B1 | G2 | ~24h `[EM]` — vượt trần (MVP0, trần Small không áp) | TBD | MVP-Scope §3 A1 · Roadmap G1-a, G1-c · CF-8.4, CF-3.1 | — | |
| 6 | [Story-Typeset-Layer-And-Bubble-Overlay](./Backlog/Story-Typeset-Layer-And-Bubble-Overlay.md) | [Epic-Image-Generation-Pipeline](./Epics/Epic-Image-Generation-Pipeline.md) | Pre-cycle/MVP0 | ⭐ | A2 | 🟡 | I0 | B1 | G2 | ~8h `[EM]` | TBD | MVP-Scope §3 A2 · Roadmap G1-e (100% panel overlay, 0 model-render) | — | |
| 7 | [Story-Deterministic-Visual-Prompt-Compiler](./Backlog/Story-Deterministic-Visual-Prompt-Compiler.md) | [Epic-Image-Generation-Pipeline](./Epics/Epic-Image-Generation-Pipeline.md) | Pre-cycle/MVP0 | ⭐ | A3 | 🟡 | I0 | B1 | G1 | ~14h `[EM]` | 0 | MVP-Scope §3 A3 · Roadmap G1-d (spec sai vs hệ thống ngẫu nhiên) | — | |
| 8 | [Story-Image-Provider-Adapter](./Backlog/Story-Image-Provider-Adapter.md) | [Epic-Image-Generation-Pipeline](./Epics/Epic-Image-Generation-Pipeline.md) | Pre-cycle/MVP0 | | A4 | 🟡 | I0 | B1 | G0 | ~6h `[EM]` | 0 | MVP-Scope §3 A4 · Roadmap G1-a/G1-c (hỗ trợ, không tự nó là con số đo) · CF-3.4 | — | |

### 3.2 MVP1

> `E-01 Tenant-Id-And-RLS-Everywhere` xếp #1 vì `Roadmap §6.2` gọi thẳng tên: *"chặn mọi tính năng multi-tenant sau đó"* — mọi Story chạm bảng nghiệp vụ (F, G, phần lớn D) đều phụ thuộc trực tiếp (T1) vào cột `tenant_id` mà Story này tạo ra.

| # | Story | Epic | Mốc | MVP | Hạng mục | Scope-Label | I | B | G | E_build | E_hitl | Anchor | Ràng buộc cứng | Ghi chú |
|--:|---|---|---|:--:|---|:--:|:--:|:--:|:--:|---|---|---|---|---|
| 1 | [Story-Tenant-Id-And-RLS-Everywhere](./Backlog/Story-Tenant-Id-And-RLS-Everywhere.md) | [Epic-Multi-Tenancy-And-Platform](./Epics/Epic-Multi-Tenancy-And-Platform.md) | MVP1 | ⭐ | E1 | ✅ | I2 | B2 | G2 | ~24h `[EM]` — vượt trần, ghi lý do | 0 | MVP-Scope §6 KC-5 · §3 E1 · Roadmap M1-1 · §6.2 | KC-5 | |
| 2 | [Story-Usage-Event-And-Daily-Rollup](./Backlog/Story-Usage-Event-And-Daily-Rollup.md) | [Epic-Credit-And-Unit-Economics](./Epics/Epic-Credit-And-Unit-Economics.md) | MVP1 | ⭐ | F1 | ✅ | I2 | B2 | G2 | ~12h `[EM]` | 0 | MVP-Scope §3 F1 · Roadmap M1-7 · §6.2 (dòng regen ratio → G2, Cứng) · CF-8.6 | — | |
| 3 | [Story-Provenance-Chain-Parent-Generation](./Backlog/Story-Provenance-Chain-Parent-Generation.md) | [Epic-Legal-And-Compliance](./Epics/Epic-Legal-And-Compliance.md) | MVP1 | ⭐ | GP-1 | ✅ | I2 | B2 | G2 | TBD | 0 | MVP-Scope §6 KC-1, KC-3 · §3 GP-1 · Roadmap M1-5 · §6.2 (dòng KC-1…KC-7, Cứng) | KC-1, KC-3 | |
| 4 | [Story-Provenance-Committed-In-Same-Transaction](./Backlog/Story-Provenance-Committed-In-Same-Transaction.md) | [Epic-Legal-And-Compliance](./Epics/Epic-Legal-And-Compliance.md) | MVP1 | ⭐ | GP-1 | ✅ | I2 | B2 | G2 | TBD | 0 | MVP-Scope §6 KC-4 · Roadmap M1-5 (test cùng transaction) · §6.2 | KC-4 | |
| 5 | [Story-Opt-Out-Check-At-Ingest](./Backlog/Story-Opt-Out-Check-At-Ingest.md) | [Epic-Legal-And-Compliance](./Epics/Epic-Legal-And-Compliance.md) | MVP1 | ⭐ | GP-2 | ✅ | I2 | B2 | G2 | TBD | 0 | MVP-Scope §6 KC-6 · §3 GP-2 · Roadmap M1-4 · §6.2 · CF-7.5 | KC-6 | |
| 6 | [Story-Change-Log-On-Every-Editor-Action](./Backlog/Story-Change-Log-On-Every-Editor-Action.md) | [Epic-Minimum-Editor](./Epics/Epic-Minimum-Editor.md) | MVP1 | | D1 | 🟡 | I2 | B2 | G0 | 20h `[EM]` — vượt trần, ghi lý do (không split được) | 0h/chapter | MVP-Scope §6 KC-2 · §5.2 (ràng buộc xuyên suốt 5 thành phần) · Roadmap §6.2 (dòng KC-1…KC-7, Cứng) — không ứng với một `M1-x` số riêng | KC-2 | |
| 7 | [Story-Generation-Cost-And-Model-Metadata](./Backlog/Story-Generation-Cost-And-Model-Metadata.md) | [Epic-Credit-And-Unit-Economics](./Epics/Epic-Credit-And-Unit-Economics.md) | MVP1 | | F2 | ✅ | I2 | B1 | G0 | ~10h `[EM]` | 0 | MVP-Scope §3 F2 ("không backfill được") · Roadmap (đóng góp cho COGS, không phải M1-x riêng) · Analysis §5.7 #3 | — | |
| 8 | [Story-Log-Preference-Data](./Backlog/Story-Log-Preference-Data.md) | [Epic-Quality-And-Operations](./Epics/Epic-Quality-And-Operations.md) | MVP1 | | H2 | ✅ | I2 | B0 | G0 | ~10h `[EM]` | 0 | MVP-Scope §3 H2 · Roadmap (không ứng exit-criterion `M1-x` nào — xem cảnh báo §2.3) · CF-8.7 | — | Cố ý không `⭐` — xem cảnh báo mục 2.3 |
| 9 | [Story-Chapter-Ingest-And-Text-Clean](./Backlog/Story-Chapter-Ingest-And-Text-Clean.md) | [Epic-Story-Intelligence](./Epics/Epic-Story-Intelligence.md) | MVP1 | ⭐ | B1 | ✅ | I1 | B1 | G2 | 10h `[EM]` | 0 | MVP-Scope §3 B1 · Roadmap M1-2 (text clean = bước ĐẦU TIÊN) · CF-8.7 | — | |
| 10 | [Story-Story-Bible-Extraction](./Backlog/Story-Story-Bible-Extraction.md) | [Epic-Story-Intelligence](./Epics/Epic-Story-Intelligence.md) | MVP1 | ⭐ | B2 | ✅ | I1 | B1 | G2 | 18h `[EM]` — vượt trần, ghi lý do | 0 (cho Story này — phần review offload sang `Story-Story-Bible-Editor-Form`) | MVP-Scope §3 B2 · Roadmap M1-3 (≥80% `[EM]`) | — | |
| 11 | [Story-HITL-Gate-And-Eval-Kit](./Backlog/Story-HITL-Gate-And-Eval-Kit.md) | [Epic-Quality-And-Operations](./Epics/Epic-Quality-And-Operations.md) | MVP1 | ⭐ | H1 | ✅ | I1 | B1 | G2 | ~24h `[EM]` — vượt trần, ghi lý do `[QA suy luận]` | TBD | MVP-Scope §3 H1 · Roadmap M1-6 · Charter §4 R9 | — | |
| 12 | [Story-Tenant-User-Membership-As-Three-Entities](./Backlog/Story-Tenant-User-Membership-As-Three-Entities.md) | [Epic-Multi-Tenancy-And-Platform](./Epics/Epic-Multi-Tenancy-And-Platform.md) | MVP1 | ⭐ | E2 | ✅ | I1 | B1 | G1 | ~8h `[EM]` | 0 | MVP-Scope §3 E2 · Roadmap M1-1 (mô hình định danh hỗ trợ test rò rỉ chéo tenant) · Analysis §5.7 #2 | — | |
| 13 | [Story-Modular-Monolith-Three-Schemas](./Backlog/Story-Modular-Monolith-Three-Schemas.md) | [Epic-Multi-Tenancy-And-Platform](./Epics/Epic-Multi-Tenancy-And-Platform.md) | MVP1 | ⭐ | E5 | ✅ | I1 | B1 | G1 | ~14h `[EM]` | 0 | MVP-Scope §3 E5 · Roadmap M1-5 (transaction boundary cho test "cùng commit") · CF-9.2 | — | |
| 14 | [Story-Per-Tenant-Object-Storage-No-Cross-Dedup](./Backlog/Story-Per-Tenant-Object-Storage-No-Cross-Dedup.md) | [Epic-Multi-Tenancy-And-Platform](./Epics/Epic-Multi-Tenancy-And-Platform.md) | MVP1 | | E3 | ✅ | I1 | B1 | G0 | ~10h `[EM]` | 0 | MVP-Scope §3 E3 · Roadmap M1-1 (storage riêng, hỗ trợ tinh thần cách ly tenant) · Analysis §5.7 #4 | — | |
| 15 | [Story-Buy-Authentication-Provider](./Backlog/Story-Buy-Authentication-Provider.md) | [Epic-Multi-Tenancy-And-Platform](./Epics/Epic-Multi-Tenancy-And-Platform.md) | MVP1 | | E4 | ✅ | I1 | B1 | G0 | ~12h `[EM]` | 0 | MVP-Scope §3 E4 · Roadmap (tiền đề để có user đăng nhập cho mọi M1-x) · Analysis §5.7 | — | |
| 16 | [Story-Timeline-State-Resolver](./Backlog/Story-Timeline-State-Resolver.md) | [Epic-Story-Intelligence](./Epics/Epic-Story-Intelligence.md) | MVP1 | | B3 | ✅ | I1 | B1 | G0 | 20h `[EM]` — vượt trần, ghi lý do | 0 | MVP-Scope §3 B3 · Roadmap (hỗ trợ tính đúng của Story Bible dùng bởi M2-1 sau này) · Analysis §5.5 | — | |
| 17 | [Story-ToS-User-Warrant-And-Tenant-Hard-Delete](./Backlog/Story-ToS-User-Warrant-And-Tenant-Hard-Delete.md) | [Epic-Legal-And-Compliance](./Epics/Epic-Legal-And-Compliance.md) | MVP1 | | GP-5 | ✅ | I1 | B1 | G0 | TBD | 0 | MVP-Scope §3 GP-5 · Roadmap (không có `M1-x` riêng — chuẩn bị năng lực cho takedown sẽ đến) · Analysis §5.7 #5 | — | |
| 18 | [Story-Minimum-Abuse-Controls](./Backlog/Story-Minimum-Abuse-Controls.md) | [Epic-Quality-And-Operations](./Epics/Epic-Quality-And-Operations.md) | MVP1 | | H5 | 🟡 | I1 | B0 | G0 | ~8h `[EM]` | 0 | MVP-Scope §3 H5 · Roadmap §4 X-b (nhắc trong ghi chú, không phải `M1-x` riêng — xem cảnh báo §2.3) | — | Cố ý không `⭐` — xem cảnh báo mục 2.3 |
| 19 | [Story-AI-Disclosure-Article-11](./Backlog/Story-AI-Disclosure-Article-11.md) | [Epic-Legal-And-Compliance](./Epics/Epic-Legal-And-Compliance.md) | MVP1 | | GP-4 | 🟡 | I1 | B0 | G0 | TBD | 0 | MVP-Scope §3 GP-4 · Roadmap (không có `M1-x` riêng, deadline tuân thủ neo vào CF-7.7) | — | |
| 20 | [Story-Job-Queue-In-Postgres](./Backlog/Story-Job-Queue-In-Postgres.md) | [Epic-Image-Generation-Pipeline](./Epics/Epic-Image-Generation-Pipeline.md) | MVP1 | | A5 | ✅ | I0 | B1 | G0 | ~12h `[EM]` | 0 | MVP-Scope §3 A5 · Roadmap (hạ tầng chạy job, không phải `M1-x` riêng) | — | |
| 21 | [Story-Story-Bible-Editor-Form](./Backlog/Story-Story-Bible-Editor-Form.md) | [Epic-Minimum-Editor](./Epics/Epic-Minimum-Editor.md) | MVP1 | | D1 | 🟡 | I0 | B0 | G0 | 14h `[EM]` | ~0,5h/chapter `[EM]` | MVP-Scope §5.2 #5 · §3 D1 · Roadmap (hỗ trợ M1-3, review phần dưới ngưỡng 80%) | — | |

### 3.3 MVP2

> `Story-Human-Gate-Speaker-Attribution` xếp trước `Story-Human-Gate-Dialogue-Condensation` theo đúng trình tự `UC-04` → `UC-05` đã có trong nguồn (`findings/business-analyst.md` §3, cả hai đều bắt buộc cho `M2-4`) — đây là suy luận `[PO suy luận]` từ trình tự tài liệu, không phải một hàng `Cứng` được đặt tên tường minh ở `Roadmap §6.2`.

| # | Story | Epic | Mốc | MVP | Hạng mục | Scope-Label | I | B | G | E_build | E_hitl | Anchor | Ràng buộc cứng | Ghi chú |
|--:|---|---|---|:--:|---|:--:|:--:|:--:|:--:|---|---|---|---|---|
| 1 | [Story-Safe-Harbour-Checklist-Article-198b](./Backlog/Story-Safe-Harbour-Checklist-Article-198b.md) | [Epic-Legal-And-Compliance](./Epics/Epic-Legal-And-Compliance.md) | MVP2 | ⭐ | GP-3 | ✅ | I1 | B2 | G2 | TBD | 0 giờ-người/chapter (SLA 72h là nghĩa vụ theo sự kiện, không theo chapter) | MVP-Scope §3 GP-3 · Roadmap M2-6 · §6.2 (dòng X-a, Cứng) · CF-7.6 | — | |
| 2 | [Story-Enforce-Max-Three-Characters-Per-Panel](./Backlog/Story-Enforce-Max-Three-Characters-Per-Panel.md) | [Epic-Comic-Director-And-Layout](./Epics/Epic-Comic-Director-And-Layout.md) | MVP2 | ⭐ | C5 | ✅ | I1 | B1 | G2 | ~6h `[EM]` | 0 | MVP-Scope §3 C5 · Roadmap M2-2 (CHECK constraint tầng DB) · CF-6.5 | — | |
| 3 | [Story-Human-Gate-Speaker-Attribution](./Backlog/Story-Human-Gate-Speaker-Attribution.md) | [Epic-Comic-Director-And-Layout](./Epics/Epic-Comic-Director-And-Layout.md) | MVP2 | ⭐ | C7 | ✅ | I1 | B1 | G2 | ~14h `[EM]` | TBD | MVP-Scope §3 C7 · Roadmap M2-4 (không bypass được) · CF-6.10 | — | |
| 4 | [Story-Human-Gate-Dialogue-Condensation](./Backlog/Story-Human-Gate-Dialogue-Condensation.md) | [Epic-Comic-Director-And-Layout](./Epics/Epic-Comic-Director-And-Layout.md) | MVP2 | ⭐ | C7 | ✅ | I1 | B1 | G2 | ~14h `[EM]` | TBD | MVP-Scope §3 C7 · Roadmap M2-4 (không bypass được) | — | |
| 5 | [Story-Auto-Director-Scene-To-Page-Panel](./Backlog/Story-Auto-Director-Scene-To-Page-Panel.md) | [Epic-Comic-Director-And-Layout](./Epics/Epic-Comic-Director-And-Layout.md) | MVP2 | ⭐ | C2 | ✅ | I0 | B1 | G2 | ~16h `[EM]` — ở trần | 0 | MVP-Scope §3 C2 · Roadmap M2-1 · CF-8.8 | — | |
| 6 | [Story-Text-Safe-Zone-In-Panel-Spec](./Backlog/Story-Text-Safe-Zone-In-Panel-Spec.md) | [Epic-Comic-Director-And-Layout](./Epics/Epic-Comic-Director-And-Layout.md) | MVP2 | ⭐ | C6 | ✅ | I0 | B1 | G2 | ~12h `[EM]` | 0 | MVP-Scope §3 C6 · Roadmap M2-3 (≥95% `[EM]`) · CF-8.8 | — | |
| 7 | [Story-Export-Chapter-To-PDF-CBZ-Webtoon](./Backlog/Story-Export-Chapter-To-PDF-CBZ-Webtoon.md) | [Epic-Quality-And-Operations](./Epics/Epic-Quality-And-Operations.md) | MVP2 | ⭐ | H4 | 🟡 | I0 | B1 | G2 | ~28h `[EM]` — vượt trần, ghi lý do | 0 | MVP-Scope §3 H4 · Roadmap M2-5 (PDF của 1 chapter hoàn chỉnh) · CF-8.10 | — | Phạm vi Story gồm cả CBZ/webtoon ngoài horizon; `E_build` ghi cho toàn bộ tên gọi |
| 8 | [Story-Server-Side-Page-And-Chapter-Preview](./Backlog/Story-Server-Side-Page-And-Chapter-Preview.md) | [Epic-Minimum-Editor](./Epics/Epic-Minimum-Editor.md) | MVP2 | ⭐ | D1 | 🟡 | I0 | B1 | G1 | 10h `[EM]` | 0h/chapter | MVP-Scope §5.2 #4 · §3 D1 · Roadmap (tái dùng compositor, hỗ trợ đo M2-5) | — | |
| 9 | [Story-Layout-Rubric-Beat-Type-And-Emphasis-Quota](./Backlog/Story-Layout-Rubric-Beat-Type-And-Emphasis-Quota.md) | [Epic-Comic-Director-And-Layout](./Epics/Epic-Comic-Director-And-Layout.md) | MVP2 | | C3 | ✅ | I0 | B1 | G0 | ~10h `[EM]` | 0 | MVP-Scope §3 C3 · Roadmap (đầu vào cho M2-1, không tự nó là con số) · CF-8.8, CF-9.3 | — | |
| 10 | [Story-Tier-1-Sellable-Without-Image-Gen](./Backlog/Story-Tier-1-Sellable-Without-Image-Gen.md) | [Epic-Credit-And-Unit-Economics](./Epics/Epic-Credit-And-Unit-Economics.md) | MVP2 | | F6 | 🟡 | I0 | B0 | G0 | ~10h `[EM]` (chỉ phần tier-gating) | 0 | MVP-Scope §3 F6 · Roadmap §5.2 (lựa chọn `[EM]`, gated on G0 PASS + M2-5 + M2-6) · CF-2.2 | — | **Có điều kiện** — không phải kế hoạch đã chốt, xem `findings/business-analyst.md` §4.6 |
| 11 | [Story-Page-Template-Layout-And-Swap-Panel](./Backlog/Story-Page-Template-Layout-And-Swap-Panel.md) | [Epic-Minimum-Editor](./Epics/Epic-Minimum-Editor.md) | MVP2 | | D1 | 🟡 | I0 | B0 | G0 | 12h `[EM]` | 0h/chapter | MVP-Scope §5.2 #3 · §3 D1 · Roadmap (deliverable MVP2, không phải `M2-x` riêng) | — | |
| 12 | [Story-Bubble-Text-Overlay-Editor](./Backlog/Story-Bubble-Text-Overlay-Editor.md) | [Epic-Minimum-Editor](./Epics/Epic-Minimum-Editor.md) | MVP2 | | D1 | 🟡 | I0 | B0 | G0 | 18h `[EM]` — vượt trần, ghi lý do | ~1h/chapter `[EM]` | MVP-Scope §5.2 #2 · §3 D1 · Roadmap (deliverable MVP2–MVP3, không phải `M2-x` riêng) | — | Bắt đầu MVP2, hoàn tất MVP3 (ngoài horizon) theo nguồn |

---

## 4. MVP Stories — danh sách rút gọn

> Chỉ liệt kê **link**, không copy lại dữ liệu (chống lệch nội bộ với [mục 3](#3-backlog-theo-mốc)). Quy tắc đánh dấu: [mục 2.3](#23-đánh-dấu--mvp-story--quy-tắc-suy-ra-được-từ-cột). **24/41 Story trong horizon** đạt `⭐`.

### Pre-cycle/MVP0 (6)

- [Story-Fix-Narrative-Time-Key](./Backlog/Story-Fix-Narrative-Time-Key.md)
- [Story-Golden-Dataset-For-Regression](./Backlog/Story-Golden-Dataset-For-Regression.md)
- [Story-Comic-IR-Panel-Specification](./Backlog/Story-Comic-IR-Panel-Specification.md)
- [Story-Generate-Panel-With-Reference-And-VLM-Select](./Backlog/Story-Generate-Panel-With-Reference-And-VLM-Select.md)
- [Story-Typeset-Layer-And-Bubble-Overlay](./Backlog/Story-Typeset-Layer-And-Bubble-Overlay.md)
- [Story-Deterministic-Visual-Prompt-Compiler](./Backlog/Story-Deterministic-Visual-Prompt-Compiler.md)

### MVP1 (10)

- [Story-Tenant-Id-And-RLS-Everywhere](./Backlog/Story-Tenant-Id-And-RLS-Everywhere.md)
- [Story-Usage-Event-And-Daily-Rollup](./Backlog/Story-Usage-Event-And-Daily-Rollup.md)
- [Story-Provenance-Chain-Parent-Generation](./Backlog/Story-Provenance-Chain-Parent-Generation.md)
- [Story-Provenance-Committed-In-Same-Transaction](./Backlog/Story-Provenance-Committed-In-Same-Transaction.md)
- [Story-Opt-Out-Check-At-Ingest](./Backlog/Story-Opt-Out-Check-At-Ingest.md)
- [Story-Chapter-Ingest-And-Text-Clean](./Backlog/Story-Chapter-Ingest-And-Text-Clean.md)
- [Story-Story-Bible-Extraction](./Backlog/Story-Story-Bible-Extraction.md)
- [Story-HITL-Gate-And-Eval-Kit](./Backlog/Story-HITL-Gate-And-Eval-Kit.md)
- [Story-Tenant-User-Membership-As-Three-Entities](./Backlog/Story-Tenant-User-Membership-As-Three-Entities.md)
- [Story-Modular-Monolith-Three-Schemas](./Backlog/Story-Modular-Monolith-Three-Schemas.md)

### MVP2 (8)

- [Story-Safe-Harbour-Checklist-Article-198b](./Backlog/Story-Safe-Harbour-Checklist-Article-198b.md)
- [Story-Enforce-Max-Three-Characters-Per-Panel](./Backlog/Story-Enforce-Max-Three-Characters-Per-Panel.md)
- [Story-Human-Gate-Speaker-Attribution](./Backlog/Story-Human-Gate-Speaker-Attribution.md)
- [Story-Human-Gate-Dialogue-Condensation](./Backlog/Story-Human-Gate-Dialogue-Condensation.md)
- [Story-Auto-Director-Scene-To-Page-Panel](./Backlog/Story-Auto-Director-Scene-To-Page-Panel.md)
- [Story-Text-Safe-Zone-In-Panel-Spec](./Backlog/Story-Text-Safe-Zone-In-Panel-Spec.md)
- [Story-Export-Chapter-To-PDF-CBZ-Webtoon](./Backlog/Story-Export-Chapter-To-PDF-CBZ-Webtoon.md)
- [Story-Server-Side-Page-And-Chapter-Preview](./Backlog/Story-Server-Side-Page-And-Chapter-Preview.md)

---

## 5. Story chưa xếp được

> 10 Story `[NGOÀI HORIZON]` từ `findings/business-analyst.md` §4.1–§4.8. **Không có file** trong `docs/022-User-Stories/Backlog/` (quyết định wave 3 — xem `outline.md` §1.2: một Story file cho việc cách 6+ tháng sẽ bị viết lại trước khi có ai nhặt nó). Traceability đi qua **Epic cha** (mục *Story ngoài horizon*), không qua link file ở đây — do đó cột `Story` là **text thuần**, không phải markdown link. `Rank = TBD` cho toàn bộ mục này: `Roadmap §2` chỉ có 2 exit criterion cho `MVP4` (`M4-1`, `M4-2`) và `MVP3` chưa có ngày — rank *"trong một mốc"* vô nghĩa khi mốc đó chưa đủ dữ liệu exit criteria để so `G`.

| Story (tên file, chưa tạo) | Epic | Mốc | Hạng mục | Trạng thái tài liệu | Lý do `Rank = TBD` |
|---|---|---|---|---|---|
| `Story-Fairness-Per-Tenant-Job-Claim` | [Epic-Image-Generation-Pipeline](./Epics/Epic-Image-Generation-Pipeline.md) | MVP3 | A6 | chưa có file | Ngoài horizon — chưa có ngày cho MVP3, không đủ dữ liệu exit-criteria để xếp `G` |
| `Story-Whole-Page-Render-Granularity` | [Epic-Image-Generation-Pipeline](./Epics/Epic-Image-Generation-Pipeline.md) | MVP3 | A7 | chưa có file | Ngoài horizon — đường lui tuỳ chọn của G2, chưa chốt có cần hay không |
| `Story-Panel-Card-With-Variant-Picker` | [Epic-Minimum-Editor](./Epics/Epic-Minimum-Editor.md) | MVP3 | D1 | chưa có file | Ngoài horizon — thành phần #1 editor, hoàn tất ở MVP3 |
| `Story-Character-Expression-Sheet` | [Epic-Minimum-Editor](./Epics/Epic-Minimum-Editor.md) | MVP3 | D7 | chưa có file | Ngoài horizon — chỉ `🟡` (3 góc + 3 biểu cảm) ở MVP3, `✅` ở Full Scope |
| `Story-Buy-Billing-Provider` | [Epic-Multi-Tenancy-And-Platform](./Epics/Epic-Multi-Tenancy-And-Platform.md) | MVP3 | E4 | chưa có file | Ngoài horizon — billing gắn liền X-b (hard quota + credit ledger), cả cụm ngoài horizon |
| `Story-Worker-As-Separate-Process-Same-Codebase` | [Epic-Multi-Tenancy-And-Platform](./Epics/Epic-Multi-Tenancy-And-Platform.md) | MVP3 | E7 | chưa có file | Ngoài horizon — `M3-4`, chưa có ngày |
| `Story-Credit-Ledger-With-Hold-Before-Enqueue` | [Epic-Credit-And-Unit-Economics](./Epics/Epic-Credit-And-Unit-Economics.md) | MVP3 | F3 (KC-7) | chưa có file | Ngoài horizon — `M3-1`/`M3-2`, chưa có ngày. Dù `I2` rõ ràng (KC-7), không đủ dữ liệu `G` để so trong mốc chưa xác định thời lượng |
| `Story-Hard-Quota-Enforced-Before-Enqueue` | [Epic-Credit-And-Unit-Economics](./Epics/Epic-Credit-And-Unit-Economics.md) | MVP3 | F4 | chưa có file | Ngoài horizon — `M3-3`, chưa có ngày |
| `Story-BYOK-As-Unlock-Option` | [Epic-Credit-And-Unit-Economics](./Epics/Epic-Credit-And-Unit-Economics.md) | MVP4 | F5 | chưa có file | Ngoài horizon — `MVP4` chỉ có 2 exit criterion tổng (`M4-1`, `M4-2`), không cái nào thuộc F5 |
| `Story-Continuity-Checker-As-N-Candidate-Selection` | [Epic-Quality-And-Operations](./Epics/Epic-Quality-And-Operations.md) | MVP4 | H3 | chưa có file | Ngoài horizon — chính là `M4-1`/`M4-2`, nhưng `MVP4` không có ngày ⇒ không xếp `Rank` nội bộ được với các Story MVP4 khác (hiện chỉ có 1 Story MVP4 khác — BYOK — nên "trong một mốc" cũng chưa có ý nghĩa thống kê) |

---

## 6. Lịch chấm lại

> Kế thừa nguyên 4 trigger của `findings/product-owner.md` §1.4(d) — **không tạo nhịp mới**.

| # | Trigger | Vì sao |
|---|---|---|
| 1 | Sau verdict mỗi gate `G0`/`G1`/`G2` | Verdict đổi được cả `Scope-Label` (ví dụ `G1-d` FAIL ⇒ đổi `C5` — đã xảy ra trong `MVP-Scope §7.2`) |
| 2 | Khi `MVP-Scope.md` hoặc `Roadmap.md` thay đổi | Hai cột kế thừa (`Mốc`, `Scope-Label`) phải đối chiếu lại cơ học |
| 3 | Khi thêm Story mới vào backlog | Bảng phải mở rộng, `Rank` trong mốc bị chèn có thể phải dịch |
| 4 | Rà hàng tháng, ngày cuối tháng | Dùng đúng nhịp đã có ở `OKRs §1.2`, không tạo nhịp mới |

⛔ **KHÔNG chấm lại theo chu kỳ 7 ngày.** Nhịp 7 ngày của `OKRs §1.2` chỉ hỏi *"số đã nhúc nhích chưa"* — không phải nhịp xếp lại thứ tự.

---

## 7. Tài liệu tham khảo

- [Roadmap.md](../010-Planning/Roadmap.md)
- [MVP-Scope.md](../010-Planning/MVP-Scope.md)
- [OKRs.md](../010-Planning/OKRs.md)
- [Charter-Comic-Studio.md](../010-Planning/Charter-Comic-Studio.md)
- [Stories-MOC](./Stories-MOC.md)
- [Glossary](../999-Resources/Glossary.md)


