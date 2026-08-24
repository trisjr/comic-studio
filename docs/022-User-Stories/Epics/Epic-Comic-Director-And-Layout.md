---
id: EPIC-C
type: epic
status: draft
project: comic-studio
created: 2026-08-24
---

# Epic-C — Comic Director & Layout

> [!IMPORTANT]
> **Quy ước nhãn nguồn số liệu** (kế thừa nguyên vẹn — **số và nhãn là một cặp không tách rời**):
> `[OFF]` nguồn official/paper gốc · `[BCN]` báo cáo ngành có tên firm · `[TC]` nguồn thứ cấp · `[EM]` ước lượng hoặc phép nhân, **không phải số đo** · `[CHỐT]` quyết định của Founder tại gate.
>
> Epic này **chỉ trích lại** số liệu từ tầng Planning/Requirements. Không tự tra lại, không tự tính lại.
>
> ⛔ **CẤM lẫn hai hệ ID** (CẤM-14): `GP-1`…`GP-5` là hàng compliance của [MVP-Scope §3](../../010-Planning/MVP-Scope.md) nhóm G; `G0` / `G1` / `G2` là **gate**. Trong Epic này, mọi `G1` / `G2` đều là **gate**.
>
> **Trục Epic**: cắt theo **module A–H**, **KHÔNG** theo mốc MVP0–MVP4. ⇒ Cột *Mốc* và cờ horizon nằm ở **tầng Story**, không ở tầng Epic.

## Mục lục

1. [Implements](#1-implements)
2. [Mục tiêu Epic](#2-mục-tiêu-epic)
3. [Story trong horizon](#3-story-trong-horizon)
4. [Story ngoài horizon — chưa có file](#4-story-ngoài-horizon--chưa-có-file)
5. [Definition of Done cấp Epic](#5-definition-of-done-cấp-epic)
6. [Tài liệu liên quan](#6-tài-liệu-liên-quan)

---

## 1. Implements

Implements: [PRD-Comic-Studio](../../020-Requirements/PRD-Comic-Studio.md#c-comic-director--layout)

---

## 2. Mục tiêu Epic

Chuyển **scene → page → panel** dưới dạng **Comic IR (Comic Intermediate Representation)**, và **khoá cứng các ràng buộc kỹ thuật vào schema thay vì vào prompt**. Đây là mệnh đề nghiệp vụ trung tâm của Epic: một ràng buộc nằm trong prompt là một **lời đề nghị** với model; cùng ràng buộc đó nằm trong `CHECK` constraint của DB là một **luật**. Panel có 4 nhân vật phải bị **DB TỪ CHỐI**, không phải bị cảnh báo — vì `attribute binding` thất bại gần hoàn toàn từ 4 người: ID-Sim **42.33** (2 nhân vật) → **27.21** (3) → **2.67** (4) → **0.52** (5), *"near-complete failure beyond three subjects"* `[OFF]` CF-6.5. ⚠️ Ngưỡng **có thể siết xuống ≤2** nếu tiêu chí `G1-d` dưới ngưỡng.

Giá trị nghiệp vụ thứ hai: **panel là spec, không phải ảnh**. Ảnh là **output phái sinh** ⇒ sửa một field thay vì re-roll cả ảnh — [Analysis §4.2](../../050-Research/Analysis-Comic-Studio-Concept.md) xếp Comic IR là hàng **rủi ro thấp nhất** của bảng khả thi. Giá trị thứ ba là **hai human gate bắt buộc** (speaker attribution, dialogue condensation): chúng không phải tính năng UX mà là **cấu trúc trách nhiệm** — điểm mà một con người thật ra một quyết định, và là căn cứ *"substantial and decisive intellectual contribution"* của Điều 5a. Epic-C **nằm TRỌN trong horizon** `[CHỐT]` CF-8.1: một Story ở **MVP0** (Comic IR bản YAML viết tay) và sáu Story ở **MVP2** (01/2027 – 02/2027).

---

## 3. Story trong horizon

> **Cột `I` / `S`**: chỉ chấm hai chữ INVEST mà việc cắt lô cần — **I** (Independent) và **S** (Small). `⚠️` = sẽ vỡ khi cắt lô ([findings §4.10](../../010-Planning/pm-runs/2026-08-24-khoi-tao-requirements-stories-comic-studio/findings/business-analyst.md)). `n/a [MVP0]` = **INVEST không áp**.
>
> **Cột *Mốc*** dùng quy ước `QC-3`: cờ gán theo **mốc đầu tiên** Story được giao.

| Story (link) | Mốc | I | S | Trạng thái |
|---|---|:-:|:-:|---|
| [Story-Comic-IR-Panel-Specification](../Backlog/Story-Comic-IR-Panel-Specification.md) | MVP0 (YAML viết tay) → hoàn tất MVP1 | `n/a [MVP0]` ⚠️ | `n/a [MVP0]` ⚠️ | chưa có file |
| [Story-Auto-Director-Scene-To-Page-Panel](../Backlog/Story-Auto-Director-Scene-To-Page-Panel.md) | MVP2 | ✅ | ⚠️ | chưa có file |
| [Story-Layout-Rubric-Beat-Type-And-Emphasis-Quota](../Backlog/Story-Layout-Rubric-Beat-Type-And-Emphasis-Quota.md) | MVP2 | ✅ | ✅ | chưa có file |
| [Story-Enforce-Max-Three-Characters-Per-Panel](../Backlog/Story-Enforce-Max-Three-Characters-Per-Panel.md) | MVP2 | ✅ | ✅ | chưa có file |
| [Story-Text-Safe-Zone-In-Panel-Spec](../Backlog/Story-Text-Safe-Zone-In-Panel-Spec.md) | MVP2 | ✅ | ✅ | chưa có file |
| [Story-Human-Gate-Speaker-Attribution](../Backlog/Story-Human-Gate-Speaker-Attribution.md) | MVP2 | ⚠️ | ⚠️ | chưa có file |
| [Story-Human-Gate-Dialogue-Condensation](../Backlog/Story-Human-Gate-Dialogue-Condensation.md) | MVP2 | ⚠️ | ⚠️ | chưa có file |

**7/7 Story trong horizon có mặt.** Epic-C **TRONG horizon toàn bộ**.

> [!WARNING]
> **`Story-Comic-IR-Panel-Specification` mang HAI dấu, và cả hai đều bắt buộc.**
>
> (1) `n/a [MVP0]` — ở bản **YAML viết tay** của MVP0, nó thuộc năm Story mà **INVEST không áp** ([findings §4.9](../../010-Planning/pm-runs/2026-08-24-khoi-tao-requirements-stories-comic-studio/findings/business-analyst.md)): [MVP-Scope §3.1](../../010-Planning/MVP-Scope.md) và [Roadmap §3.1](../../010-Planning/Roadmap.md) đều ghi kỷ luật **code của MVP0 KHÔNG phải nền của sản phẩm — viết để trả lời câu hỏi rồi bỏ, giữ lại kết luận và dữ liệu**. Definition of Done của bản MVP0 là **5 tiêu chí gate `G1`** ([MVP-Scope §7.2](../../010-Planning/MVP-Scope.md)), không phải Acceptance Criteria kiểu Gherkin. ⛔ Dùng **đúng** tên **MVP0** — [Glossary](../../999-Resources/Glossary.md) cấm *"phase 0"*, *"spike"*, *"PoC"* (CẤM-11).
>
> (2) `⚠️` — **vượt khỏi bản YAML viết tay**, nó thuộc bảy Story **vỡ khi cắt lô** ([findings §4.10](../../010-Planning/pm-runs/2026-08-24-khoi-tao-requirements-stories-comic-studio/findings/business-analyst.md)): schema Comic IR là nơi `C5` (≤3 nhân vật) và `C6` (`text_safe_zone`) cắm vào ⇒ nó không độc lập với hai Story đó, và nó **không nhỏ**.
>
> Bỏ một trong hai dấu là mất một nửa thông tin PM cần để cắt lô.

> [!CAUTION]
> **Hai human gate chỉ "xong" CÙNG NHAU — đó là lý do cả hai mang `⚠️` ở cột `I`.**
>
> Chúng được đo bằng exit criterion **`M2-4`: sự VẮNG MẶT của đường code bypass** — *"không tồn tại đường code nào xuất bản page mà chưa qua cả hai"*. Đó là thuộc tính của **pipeline xuất bản**, không của một màn hình ⇒ ship một gate và hoãn gate kia thì `M2-4` **FAIL**, và [Roadmap §2](../../010-Planning/Roadmap.md) đã ghi sẵn rủi ro *"hai human gate bị tạm bypass để test rồi quên bật lại"* — `M2-4` đo bằng **code**, không bằng **cấu hình**.
>
> Thêm một ràng buộc **thứ tự** từ [Glossary](../../999-Resources/Glossary.md): **dialogue condensation phải chạy SAU layout**, vì `text_budget` phụ thuộc diện tích panel. Nén thoại gốc **30–80 từ** (web-novel dịch) xuống **~8–20 từ**, hệ số **2–5×** — là **hành vi biên tập CÓ MẤT** ⇒ cần LLM **và** cần người review.
>
> Lỗi speaker attribution: **30–50%** (3+ người có tự sự chen) / **40–60%** (câu ngắn, thán từ) — ⚠️ `[EM]` CF-6.10, **ước lượng, KHÔNG phải số đo**. Chi phí lỗi **bất đối xứng**: một dòng gán sai làm hỏng **cả trang**.

> [!NOTE]
> **`C4` (Layout Score 5 số thực): CẮT HẲN — nhưng mục tiêu được GIỮ. Không sinh Story cho `C4`.**
>
> CF-9.3: **cơ chế** Layout Score 5 số thực bị cắt (không có prior art; *"chưa ai làm vì không đáng"*), **mục tiêu** *"layout theo narrative importance"* **vẫn còn** và được thực hiện bởi `Story-Layout-Rubric-Beat-Type-And-Emphasis-Quota` — một **bảng tra rời rạc, tất định** cộng quota nhấn mạnh theo chapter. ⛔ Đừng đọc/viết như thể cả mục tiêu bị cắt. Hạng mục `C4` được ghi tại [PRD mục 6.2](../../020-Requirements/PRD-Comic-Studio.md#62-cắt-hẳn--không-có-trong-full-scope).

---

## 4. Story ngoài horizon — chưa có file

**không có.**

Epic-C là một trong hai Epic **không có** Story nào rơi ra ngoài horizon 09/2026 → 02/2027 (cùng với [Epic-Story-Intelligence](./Epic-Story-Intelligence.md)). Cả **7/7** Story đều bắt đầu **và** hoàn tất trong horizon: `Story-Comic-IR-Panel-Specification` mở ở MVP0 và hoàn tất ở MVP1; sáu Story còn lại hoàn tất ở **MVP2** (01/2027 – 02/2027).

Mục này được giữ lại với giá trị *"không có"* tường minh — bỏ trống mục sẽ đọc thành *"chưa ai kiểm"*, và đó là hai trạng thái khác nhau.

---

## 5. Definition of Done cấp Epic

Nguồn: exit criteria của [Roadmap §2](../../010-Planning/Roadmap.md) mốc MVP2. Epic-C `Done` khi:

- [ ] **`M2-1`**: Director sinh page/panel **tự động** cho **≥1 chapter** mà **không cần panel script viết tay**.
- [ ] **`M2-2`**: **≤3 nhân vật/panel là `CHECK` constraint ở tầng DB** — đo bằng: **insert panel 4 nhân vật BỊ TỪ CHỐI**, không phải bị cảnh báo. ⚠️ Nếu MVP0 đo panel 2 nhân vật **dưới** ngưỡng `G1-d`, `M2-2` **đổi thành cứng hoá ≤2 nhân vật/panel** thay vì ≤3 ([Roadmap §2](../../010-Planning/Roadmap.md) mốc MVP2, ô *Gate liên quan*).
- [ ] **`M2-3`**: `text_safe_zone` có trong panel spec **và** typeset không đè vùng mặt ở **≥95%** panel. ⚠️ **Ngưỡng 95% là `[EM]` do `Roadmap` TỰ ĐỊNH NGHĨA** (CF-10.5) — ⛔ **cấm trích như số đo hoặc benchmark ngành**.
- [ ] **`M2-4`**: **hai human gate không bypass được** — *"không tồn tại đường code nào xuất bản page mà chưa qua cả hai"*. ⚠️ Đo bằng **sự vắng mặt của đường code**, **không** bằng một flag cấu hình.
- [ ] Comic IR / `Panel Specification` là **dữ liệu chính**; ảnh là **output phái sinh**. Sửa một panel = sửa **một field của spec**, không phải re-roll ảnh.
- [ ] Ràng buộc kỹ thuật nằm trong **schema**, không nằm trong **prompt** — kiểm bằng câu hỏi: *"nếu model phớt lờ prompt, ràng buộc còn được giữ không?"* Câu trả lời phải là **có**.
- [ ] **Thứ tự bắt buộc** được thực thi: `dialogue condensation` chạy **sau** layout (`text_budget` phụ thuộc diện tích panel).
- [ ] Mỗi lần người dùng chấp nhận / từ chối gợi ý tại hai gate sinh một `change_log` row + **preference data** (`KC-2`, `H2`). Epic-C **không sở hữu** hai hạng mục này — chủ là [Epic-Legal-And-Compliance](./Epic-Legal-And-Compliance.md) và [Epic-Quality-And-Operations](./Epic-Quality-And-Operations.md) — nhưng hai human gate là **nơi sinh dữ liệu đó dày nhất**.
- [ ] ⚠️ **Ngưỡng không được sửa sau khi nhìn kết quả** (CẤM-16) — *"đó là cách một gate biến thành nghi lễ"*.

---

## 6. Tài liệu liên quan

### 6.1 Traceability — BRD cha

| Tầng | Tài liệu |
|---|---|
| Requirements (module) | [PRD-Comic-Studio §C. Comic Director & Layout](../../020-Requirements/PRD-Comic-Studio.md#c-comic-director--layout) — `FR-C-01` … `FR-C-07` |
| **BRD cha** | [BRD-003-Comic-Director-And-Layout](../../020-Requirements/BRD/BRD-003-Comic-Director-And-Layout.md) |
| Yêu cầu phi chức năng | [SRS-Comic-Studio](../../020-Requirements/SRS-Comic-Studio.md) |

### 6.2 Use Case liên quan

| UC | Vai trò với Epic-C |
|---|---|
| [UC-03-Review-Panel-Script](../../020-Requirements/Use-Cases/UC-03-Review-Panel-Script.md) | Duyệt / sửa panel script (Comic IR) **trước khi tiêu bất kỳ đồng tiền API nào** |
| [UC-04-Human-Gate-Speaker-Attribution](../../020-Requirements/Use-Cases/UC-04-Human-Gate-Speaker-Attribution.md) | Human gate bắt buộc **#1** — không bypass được (`M2-4`) |
| [UC-05-Human-Gate-Dialogue-Condensation](../../020-Requirements/Use-Cases/UC-05-Human-Gate-Dialogue-Condensation.md) | Human gate bắt buộc **#2** — chỉ "xong" **cùng** UC-04 |
| [UC-08-Arrange-Page-And-Preview](../../020-Requirements/Use-Cases/UC-08-Arrange-Page-And-Preview.md) | Tiêu thụ template layout + rubric của Epic-C; UI thuộc [Epic-Minimum-Editor](./Epic-Minimum-Editor.md) |

### 6.3 Tài liệu tham khảo

| Tài liệu | Epic-C trích mục nào |
|---|---|
| [MVP-Scope.md](../../010-Planning/MVP-Scope.md) | §3 nhóm C (C1–C7; `C4` cắt hẳn, không sinh Story) · §3.1 kỷ luật MVP0 · §4.3 rubric thay Layout Score · §6 `KC-2` · §7.2 gate `G1` |
| [Roadmap.md](../../010-Planning/Roadmap.md) | §2 exit criteria `M2-1`, `M2-2`, `M2-3`, `M2-4` + ô rủi ro *"tạm bypass rồi quên bật lại"* · §3.1 kỷ luật MVP0 |
| [Glossary.md](../../999-Resources/Glossary.md) | `Comic IR` · `Panel Specification` · `text_safe_zone` · `dialogue condensation` · `Layout Score` · `MVP0` |
| [findings/business-analyst.md](../../010-Planning/pm-runs/2026-08-24-khoi-tao-requirements-stories-comic-studio/findings/business-analyst.md) | §2.3 trục Epic · §4.3 bảng Story · §4.9 năm Story MVP0 · §4.10 bảy Story vỡ khi cắt lô · §5.2 canonical facts (CF-6.5, CF-6.10, CF-9.3, CF-10.4, CF-10.5) · §5.3 lệnh cấm (CẤM-11, CẤM-14, CẤM-16) |

---

_Created by product-owner_
_Author: trisjr_
