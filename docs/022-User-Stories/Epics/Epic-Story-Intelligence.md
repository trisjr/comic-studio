---
id: EPIC-B
type: epic
status: draft
project: comic-studio
created: 2026-08-24
---

# Epic-B — Story Intelligence

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

Implements: [PRD-Comic-Studio](../../020-Requirements/PRD-Comic-Studio.md#b-story-intelligence)

---

## 2. Mục tiêu Epic

Biến văn bản truyện thô thành **Story Bible** truy vấn được **theo thời điểm** — đây là **tài sản tích luỹ của người dùng**, là switching cost, và là ứng viên moat thật của comic-studio. Đối thủ chiến lược đánh trục **editor** (GlobalComix, *"the Figma for comics"*, `[TC]` CF-5.2/5.3); comic-studio đánh trục **Story Bible + Timeline State + Continuity**. Hệ quả requirement được ghi thẳng vào Epic này: **không đua editor** — giá trị nằm ở chỗ hệ thống trả lời được câu *"nhân vật này mặc gì ở chương 40"*, không ở chỗ canvas mượt hơn ai.

Ràng buộc chi phối cả Epic: **code sở hữu state, LLM chỉ phát event** (Analysis §5.5). Story Bible không phải một bản ghi tự do do LLM viết ra; nó là `state_at(N) = reduce(events)` — một phép reduce **tất định** trên chuỗi event, khoá bằng `timeline_id` + `story_order`. Epic-B **nằm TRỌN trong horizon** 09/2026 → 02/2027 `[CHỐT]` CF-8.1: một Story ở **pre-cycle 09/2026** (khoá thời gian — *"phải sửa TRƯỚC dòng code đầu tiên"*) và ba Story ở **MVP1**. Không Story nào rơi ra ngoài horizon.

---

## 3. Story trong horizon

> **Cột `I` / `S`**: chỉ chấm hai chữ INVEST mà việc cắt lô cần — **I** (Independent) và **S** (Small). `⚠️` = sẽ vỡ khi cắt lô ([findings §4.10](../../010-Planning/pm-runs/2026-08-24-khoi-tao-requirements-stories-comic-studio/findings/business-analyst.md)).
>
> **Cột *Mốc*** dùng quy ước `QC-3`: cờ gán theo **mốc đầu tiên** Story được giao.

| Story (link) | Mốc | I | S | Trạng thái |
|---|---|:-:|:-:|---|
| [Story-Fix-Narrative-Time-Key](../Backlog/Story-Fix-Narrative-Time-Key.md) | **pre-cycle 09/2026** → hoàn tất MVP1 | ⚠️ | ✅ | chưa có file |
| [Story-Chapter-Ingest-And-Text-Clean](../Backlog/Story-Chapter-Ingest-And-Text-Clean.md) | MVP1 | ✅ | ✅ | chưa có file |
| [Story-Story-Bible-Extraction](../Backlog/Story-Story-Bible-Extraction.md) | MVP1 | ✅ | ⚠️ | chưa có file |
| [Story-Timeline-State-Resolver](../Backlog/Story-Timeline-State-Resolver.md) | MVP1 | ⚠️ | ⚠️ | chưa có file |

**4/4 Story trong horizon có mặt.** Epic-B **TRONG horizon toàn bộ**.

> [!CAUTION]
> **`Story-Fix-Narrative-Time-Key` là ĐIỀU KIỆN TIÊN QUYẾT, không phải một lô song song** — đó là lý do cột `I` mang `⚠️`.
>
> Nó nằm **trong khoá** của mọi bảng timeline; [Roadmap §6.2](../../010-Planning/Roadmap.md) xếp đây là phụ thuộc **CỨNG**. Làm sau MVP1 = **migration toàn bộ**. Không có cách xếp nó song song với ba Story còn lại của Epic — ba Story kia đọc/ghi đúng cái khoá mà Story này định nghĩa. Nội dung: dùng `timeline_id` + `story_order` thay cho `(chapter, scene)`, tách **`syuzhet`** (thứ tự người đọc gặp sự kiện) khỏi **`fabula`** (thứ tự sự kiện thực sự xảy ra) — dùng `(chapter, scene)` làm khoá thời gian **sai âm thầm ở MỌI flashback**.
>
> `Story-Timeline-State-Resolver` vỡ **cả `I` và `S`**: nó là chỗ ranh giới *"code sở hữu state, LLM chỉ phát event"* được thực thi, và nó phụ thuộc trực tiếp vào khoá thời gian ở trên.

> [!NOTE]
> **`B5` (pgvector / vector search): KHÔNG tạo Story — ghi ra để không ai đi tìm một file không tồn tại.**
>
> [MVP-Scope §3](../../010-Planning/MVP-Scope.md) hàng `B5` = `❌` tới MVP2, `⛔` MVP3–MVP4, Full Scope chỉ `🟡` *"khi có bằng chứng SQL+FTS không đủ"*. CF-9.2: *"Story Bible **là** index của mình"*. Hạng mục này được ghi tại [PRD mục 6.3](../../020-Requirements/PRD-Comic-Studio.md#63-hoãn-ngoài-mvp--kèm-điều-kiện-mở-lại), **không** sinh Story.

---

## 4. Story ngoài horizon — chưa có file

**không có.**

Epic-B là một trong hai Epic **không có** Story nào rơi ra ngoài horizon 09/2026 → 02/2027 (cùng với [Epic-Comic-Director-And-Layout](./Epic-Comic-Director-And-Layout.md)). Cả **4/4** Story đều bắt đầu **và** hoàn tất trong horizon: `Story-Fix-Narrative-Time-Key` ở pre-cycle 09/2026, ba Story còn lại hoàn tất ở **MVP1** (10/2026 – 12/2026).

Mục này được giữ lại với giá trị *"không có"* tường minh — bỏ trống mục sẽ đọc thành *"chưa ai kiểm"*, và đó là hai trạng thái khác nhau.

---

## 5. Definition of Done cấp Epic

Nguồn: exit criteria của [Roadmap §2](../../010-Planning/Roadmap.md). Epic-B `Done` khi:

- [ ] **`P-4`**: khoá thời gian thay `(chapter, scene)` được viết ra dưới dạng **schema draft** ngay trong pre-cycle 09/2026 — **trước dòng code đầu tiên**, không phải sau.
- [ ] **`M1-2`**: pipeline ingest có **bước `text clean` là bước ĐẦU TIÊN**, chạy được trên **≥1 chapter scrape thật** (không phải văn bản sạch tự soạn). Nếu `text clean` không đứng đầu, Story Bible **sinh entity giả** từ quảng cáo và lời tác giả cuối chương (CF-8.7).
- [ ] **`M1-3`**: extraction đạt **≥80%** entity (nhân vật + địa điểm) khớp với Story Bible **viết tay của MVP0**. ⚠️ **Ngưỡng 80% là `[EM]` do `Roadmap` TỰ ĐỊNH NGHĨA** (CF-10.5) — ⛔ **cấm trích như số đo hoặc benchmark ngành**. Dưới ngưỡng ⇒ **tăng phần human-in-the-loop**, **không** kéo dài mốc.
- [ ] `state_at(N) = reduce(events)` trả về đúng trạng thái tại **một thời điểm bất kỳ**, và điều đó được chứng minh bằng **một test có flashback** — không phải bằng một chuỗi chương tuyến tính (nơi `(chapter, scene)` cũng "đúng").
- [ ] Ranh giới **code sở hữu state, LLM chỉ phát event** không bị vi phạm: không có đường nào để LLM ghi trực tiếp vào bảng state.
- [ ] Story Bible tách **Identity** (bất biến qua chương) khỏi **Appearance** (thay đổi theo trạng thái) — gộp hai thứ vào một field là **nguyên nhân của phần lớn lỗi consistency** (PRD `FR-B-02`).
- [ ] Mọi bảng của Epic-B có `tenant_id` + RLS (`KC-5`) và nằm trong schema `story` của modular monolith. Epic-B **không sở hữu** hai yêu cầu này — chủ là [Epic-Multi-Tenancy-And-Platform](./Epic-Multi-Tenancy-And-Platform.md) — nhưng chúng là **điều kiện `Done`** của Epic-B.
- [ ] ⚠️ **Ngưỡng không được sửa sau khi nhìn kết quả** (CẤM-16).

---

## 6. Tài liệu liên quan

### 6.1 Traceability — BRD cha

| Tầng | Tài liệu |
|---|---|
| Requirements (module) | [PRD-Comic-Studio §B. Story Intelligence](../../020-Requirements/PRD-Comic-Studio.md#b-story-intelligence) — `FR-B-01` … `FR-B-04` |
| **BRD cha** | [BRD-002-Story-Intelligence](../../020-Requirements/BRD/BRD-002-Story-Intelligence.md) |
| Yêu cầu phi chức năng | [SRS-Comic-Studio](../../020-Requirements/SRS-Comic-Studio.md) |

### 6.2 Use Case liên quan

| UC | Vai trò với Epic-B |
|---|---|
| [UC-01-Upload-And-Ingest-Chapter](../../020-Requirements/Use-Cases/UC-01-Upload-And-Ingest-Chapter.md) | Cửa vào của Epic — `text clean` là bước **đầu tiên**; cũng là nơi kiểm opt-out Điều 37b (`KC-6`, thuộc [Epic-Legal-And-Compliance](./Epic-Legal-And-Compliance.md)) |
| [UC-02-Review-And-Edit-Story-Bible](../../020-Requirements/Use-Cases/UC-02-Review-And-Edit-Story-Bible.md) | Nơi **moat lộ ra với khách hàng**. UI form thuộc [Epic-Minimum-Editor](./Epic-Minimum-Editor.md); dữ liệu và phép `reduce` thuộc Epic-B |
| [UC-03-Review-Panel-Script](../../020-Requirements/Use-Cases/UC-03-Review-Panel-Script.md) | Tiêu thụ đầu ra của Epic-B qua `resolveState()` / `getBible()` — Director không đọc trực tiếp bảng của schema `story` |

### 6.3 Tài liệu tham khảo

| Tài liệu | Epic-B trích mục nào |
|---|---|
| [MVP-Scope.md](../../010-Planning/MVP-Scope.md) | §3 nhóm B (B1–B5, `B5` không sinh Story) · §6 `KC-5` · §1.1 ranh giới ba tài liệu |
| [Roadmap.md](../../010-Planning/Roadmap.md) | §2 exit criteria `P-4`, `M1-2`, `M1-3` · §3.1 việc 3 (khoá thời gian) · §3.2 bổ sung #1 · §6.2 bảng phụ thuộc (`Story-Fix-Narrative-Time-Key` = phụ thuộc **cứng**) |
| [Glossary.md](../../999-Resources/Glossary.md) | `Story Bible` · `syuzhet vs fabula` · `timeline_id` · `MVP0` |
| [findings/business-analyst.md](../../010-Planning/pm-runs/2026-08-24-khoi-tao-requirements-stories-comic-studio/findings/business-analyst.md) | §2.3 trục Epic · §4.2 bảng Story · §4.10 bảy Story vỡ khi cắt lô · §5.2 canonical facts (CF-5.2/5.3, CF-9.2, CF-10.5) · §5.3 lệnh cấm |

---

_Created by product-owner_
_Author: trisjr_
