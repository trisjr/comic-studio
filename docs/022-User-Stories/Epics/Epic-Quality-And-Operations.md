---
id: EPIC-H
type: epic
status: draft
project: comic-studio
created: 2026-08-24
---

# Epic-H — Chất lượng & vận hành

> [!IMPORTANT]
> **Quy ước nhãn nguồn số liệu** (kế thừa nguyên vẹn — **số và nhãn là một cặp không tách rời**):
> `[OFF]` nguồn official/paper gốc · `[BCN]` báo cáo ngành có tên firm · `[TC]` nguồn thứ cấp · `[EM]` ước lượng hoặc phép nhân, **không phải số đo** · `[CHỐT]` quyết định của Founder tại gate.
>
> Epic này **chỉ trích lại** số liệu từ tầng Planning và Requirements. Không tự tra lại, không tự tính lại (`CẤM-15`).
>
> **Tên đúng của mốc khám phá là `MVP0`.** ⛔ `CẤM-11`: không dùng *"phase 0"*, *"spike"*, *"PoC"* — [Glossary.md](../../999-Resources/Glossary.md) ghi *"một tên duy nhất cho khái niệm này"*.

## Mục lục

1. [Implements](#1-implements)
2. [Mục tiêu Epic](#2-mục-tiêu-epic)
3. [Story trong horizon](#3-story-trong-horizon)
4. [Story ngoài horizon — chưa có file](#4-story-ngoài-horizon--chưa-có-file)
5. [Definition of Done cấp Epic](#5-definition-of-done-cấp-epic)
6. [Tài liệu liên quan](#6-tài-liệu-liên-quan)

---

## 1. Implements

Implements: [PRD-Comic-Studio §4 — H. Chất lượng & vận hành](../../020-Requirements/PRD-Comic-Studio.md#h-chất-lượng--vận-hành)

> Anchor trên trỏ tới **H3 `H. Chất lượng & vận hành`** trong [PRD mục 4](../../020-Requirements/PRD-Comic-Studio.md#4-yêu-cầu-chức-năng-theo-8-module) — nơi chứa `FR-H-01`…`FR-H-06`. PRD §4.0 quy ước 4 ghi rõ **cấu trúc tám H3 là contract cứng**: đổi tên hoặc đổi thứ tự H3 ⇒ link này chết.

---

## 2. Mục tiêu Epic

> Làm cho **mọi thay đổi về sau đo được**: HITL gate, eval kit, golden dataset, preference data, export, abuse control. Không có Epic này thì **mọi thay đổi prompt/model là thay đổi mù**.

| # | Điều làm Epic này khác các Epic khác | Hệ quả lên backlog |
|---|---|---|
| 1 | Hai Story sớm nhất của cả backlog nằm ở đây (**MVP0**) | Với hai Story đó, **INVEST không áp** — xem [mục 3](#3-story-trong-horizon) và [mục 5.2](#52-dod-của-hai-story-mvp0--đo-bằng-gate-g1-không-bằng-gherkin) |
| 2 | `H4` **export** không phải một tính năng editor — nó là **điều kiện doanh thu** | Không có export ở MVP2 thì **Tầng 1 không bán được** và horizon 6 tháng khép lại với **$0** (CF-8.10 · [Roadmap §5.2](../../010-Planning/Roadmap.md#52--hệ-quả-tích-cực-thứ-có-thể-bán-được-trong-horizon)) |
| 3 | `H2` **preference data** gần như miễn phí nhưng **không ghi từ đầu thì mất vĩnh viễn** dữ liệu giai đoạn đầu | Analysis §12 gọi đây là **moat thật** — *"một khoản đầu tư, trả hai lần"* |
| 4 | Epic **vắt biên** horizon: **6 Story trong / 1 Story ngoài** | Story ngoài duy nhất là `Continuity Checker` (`H3`, MVP4) |
| 5 | Epic này sở hữu đơn vị đo thật của một đội 1 người | Đơn vị đo của HITL gate là **giờ-người**, không phải token: *"với một người làm một mình, **đây mới là ràng buộc thật**, không phải chi phí API"* |

### 2.1 `Continuity Checker` — định nghĩa canon, chỉ có MỘT nghĩa

> [!CAUTION]
> ⭐ **`Continuity Checker` = QA-based selection giữa N candidate** — nó trả lời câu *"trong N cái này, cái nào **consistent hơn**"*.
>
> ⛔ **KHÔNG phải** *"gắn nhãn ✓/✗ từng attribute rồi autofix"*. Định nghĩa đó **đã bị bác** (`CẤM-12` · CF-8.10), và [Glossary.md](../../999-Resources/Glossary.md) ghi *"mọi tài liệu mới phải dùng nghĩa sau"*. Lý do sâu hơn: kiểm trang phục của nhân vật X đòi giải **re-identification** trước — mà đó **chính là** bài toán checker được lập ra để giải, tức một vòng lặp logic.
>
> ⚠️ **Độ phủ 40–60% số panel** `[EM]` CF-6.11 — **ước lượng, KHÔNG phải số đo** — và **PHẢI nói rõ với user**: *"đừng để họ hiểu là được bảo vệ toàn diện"*. Giấu điều này = **lời hứa sản phẩm không giữ được**. Đây là nội dung của exit criterion **M4-2**.

### 2.2 `best-of-N` ≠ `retry-on-failure`

> [!CAUTION]
> ⛔ **`best-of-N` (N=3) chạy trên MỌI panel như MẶC ĐỊNH**, không chỉ khi panel lỗi — *"performance saturates at N=3"* `[OFF]` CF-3.1/3.2. **`retry-on-failure`** là một cơ chế khác hoàn toàn.
>
> **Nhầm hai khái niệm này là nguồn của sai số chi phí +50%.** Điều này áp trực tiếp lên Epic-H vì eval kit và golden dataset **đo trên output của best-of-N**: nếu bảng chấm được lập với giả định *"chỉ retry khi lỗi"* thì mọi số nó sinh ra là số của một hệ thống khác.
>
> ⛔ `CẤM-03`: cấm lấy chất lượng của N=3 mà tính chi phí của N=2. Hạ N ⇒ **phải chạy lại G1**, không phải chỉ G2.

---

## 3. Story trong horizon

**6 Story** — horizon **09/2026 → 02/2027** `[CHỐT]` CF-8.1.

> **Cách đọc cột `I` / `S`**: chỉ chấm **I** (Independent) và **S** (Small). `⚠️` = sẽ vỡ · **`n/a [MVP0]`** = INVEST **không áp** cho Story đó (lý do ở [mục 5.2](#52-dod-của-hai-story-mvp0--đo-bằng-gate-g1-không-bằng-gherkin)).
>
> ⚠️ **File Story chưa tồn tại** — chúng được tạo ở lô sau với **đúng** những tên dưới đây.

| Story (link) | Mốc | I | S | Trạng thái |
|---|---|:-:|:-:|---|
| [Story-Golden-Dataset-For-Regression](../Backlog/Story-Golden-Dataset-For-Regression.md) | **MVP0** | `n/a [MVP0]` | `n/a [MVP0]` | `[TRONG HORIZON]` · hoàn tất **MVP0**, và `✅` ở **mọi** mốc sau · 15–20 panel có **spec + reference + ảnh + bảng chấm của con người**. Là **tài sản dùng suốt vòng đời**, không phải artifact của MVP0. Exit criterion **P-6**; chặn **mềm** eval kit **M1-6** |
| [Story-Record-Readability-Human-Judgement](../Backlog/Story-Record-Readability-Human-Judgement.md) | **MVP0** | `n/a [MVP0]` | `n/a [MVP0]` | `[TRONG HORIZON]` · hoàn tất **liên tục** · cạnh mọi metric kỹ thuật có **đúng một câu người trả lời** — *"trang này đọc có ổn không?"* — và câu trả lời **được GHI LẠI từ MVP0** (CF-10.10). *"Vừa là metric chất lượng thật, vừa là dữ liệu preference cho moat"* |
| [Story-HITL-Gate-And-Eval-Kit](../Backlog/Story-HITL-Gate-And-Eval-Kit.md) | MVP1 | ✅ | ⚠️ | `[TRONG HORIZON]` · hoàn tất **MVP1** · ⚠️ **ngay tại MVP1, KHÔNG dồn MVP4** (CF-8.7) — là điều kiện khả thi **R9** của [Charter §4](../../010-Planning/Charter-Comic-Studio.md#4-yêu-cầu-cấp-cao). Eval kit phải **sinh ra SỐ**, không chấm bằng ấn tượng |
| [Story-Log-Preference-Data](../Backlog/Story-Log-Preference-Data.md) | MVP1 | ⚠️ | ✅ | `[TRONG HORIZON]` · hoàn tất **MVP1** · ⚠️ **vỡ `I`**: nó là nhãn gắn vào **mỗi lần người dùng chấp nhận/từ chối một gợi ý** ⇒ nó sống bên trong các luồng của Epic khác, không tự đứng riêng. Nhưng *"gần như miễn phí, và không ghi từ đầu thì **mất vĩnh viễn** dữ liệu giai đoạn đầu"* |
| [Story-Minimum-Abuse-Controls](../Backlog/Story-Minimum-Abuse-Controls.md) | MVP1 (🟡) | ✅ | ✅ | `[TRONG HORIZON]` · hoàn tất **MVP2** · rate limit/tenant · giới hạn upload · log mỗi lần provider từ chối. ⚠️ Lưu ý phạm vi của [Roadmap §4](../../010-Planning/Roadmap.md#4-ba-việc-xen-ngang) **X-b**: *"abuse control cho upload thì **cần ngay ở MVP1**"* — kể cả khi credit ledger còn ở MVP3 |
| [Story-Export-Chapter-To-PDF-CBZ-Webtoon](../Backlog/Story-Export-Chapter-To-PDF-CBZ-Webtoon.md) | MVP2 (PDF) | ✅ | ⚠️ | `[TRONG HORIZON]` · hoàn tất **MVP3** (đủ định dạng) · *"Thứ **DUY NHẤT** trong MVP4 mà người dùng thật sự nhận được"* ⇒ đã được **kéo lên sớm** (CF-8.10). ⚠️ Là **điều kiện doanh thu** của Tầng 1 (`FR-F-06`), không phải một tính năng editor. Exit criterion **M2-5** |

---

## 4. Story ngoài horizon — chưa có file

**1 Story** — ở **MVP4**, **NGOÀI horizon** `[EM]` CF-10.8.

| Story (link) | Mốc | I | S | Vì sao ngoài horizon + ràng buộc phải giữ nguyên | Trạng thái tài liệu |
|---|---|:-:|:-:|---|---|
| `Story-Continuity-Checker-As-N-Candidate-Selection` | MVP4 | ⚠️ | ⚠️ | `H3` đạt `✅` ở **MVP4**; MVP3 và MVP4 **rơi ra ngoài** horizon ([Roadmap §5.1](../../010-Planning/Roadmap.md#51-cái-gì-rơi-ra-khỏi-092026022027)). ⭐ **Chỉ có MỘT nghĩa: QA-based selection giữa N candidate** — *"trong N cái này, cái nào consistent hơn"*. ⛔ **KHÔNG** phải gắn nhãn ✓/✗ từng attribute rồi autofix (`CẤM-12`). ⚠️ Độ phủ **40–60% số panel** `[EM]` CF-6.11 — **phải nói rõ với user** (**M4-2**). Hệ quả trong horizon: checker chưa có ⇒ **chưa được hứa gì với user về nó** | **chưa có file** |

> ⚠️ **Không tách UC riêng cho checker.** Nó là **N-candidate selection bên trong** [UC-06](../../020-Requirements/Use-Cases/UC-06-Generate-Panel-And-Pick-Variant.md), không phải một luồng người dùng riêng — [findings §3.3](../../010-Planning/pm-runs/2026-08-24-khoi-tao-requirements-stories-comic-studio/findings/business-analyst.md).

---

## 5. Definition of Done cấp Epic

### 5.1 Điều kiện ra trong horizon — nguồn là `Roadmap` §2

| # | Tiêu chí | Nguồn |
|---|---|---|
| 1 | **Golden dataset tồn tại dưới dạng file** — spec + reference + ảnh + **bảng chấm** | **P-6** |
| 2 | **Eval kit chạy được trên golden dataset của MVP0 và cho ra SỐ** | **M1-6** |
| 3 | HITL gate tồn tại ở **MVP1**, không dồn về sau | `FR-H-01` · CF-8.7 · **R9** |
| 4 | Mỗi lần người dùng **chấp nhận / từ chối** một gợi ý đều được ghi làm **preference data** | `FR-H-02` |
| 5 | Rate limit per tenant + giới hạn upload + log provider từ chối — **abuse control cho upload có ngay ở MVP1** | `FR-H-05` · [Roadmap §4](../../010-Planning/Roadmap.md#4-ba-việc-xen-ngang) **X-b** lưu ý phạm vi |
| 6 | ⭐ **Export ra PDF của 1 chapter HOÀN CHỈNH** từ preview server-side | **M2-5** |
| 7 | Câu *"trang này đọc có ổn không?"* có **câu trả lời được ghi lại**, từ MVP0 và **liên tục** sau đó | CF-10.10 · Analysis §3.2 |

> ⚠️ **Tiêu chí #6 là điều kiện doanh thu, không phải một hạng mục UI.** Nó là một trong bốn cửa của `Story-Tier-1-Sellable-Without-Image-Gen` ([Epic-F](./Epic-Credit-And-Unit-Economics.md)). Trượt `M2-5` ⇒ Tầng 1 không bán được trong horizon.

### 5.2 DoD của hai Story MVP0 — đo bằng gate `G1`, không bằng Gherkin

> [!IMPORTANT]
> `MVP-Scope` §3.1 và [Roadmap §3.1](../../010-Planning/Roadmap.md#31-pre-cycle-092026--ba-việc-trước-dòng-code-đầu-tiên) đều ghi kỷ luật bắt buộc: **code của MVP0 KHÔNG phải nền của sản phẩm — viết để trả lời câu hỏi rồi bỏ, giữ lại kết luận và dữ liệu.**
>
> Với `Story-Golden-Dataset-For-Regression` và `Story-Record-Readability-Human-Judgement`, chấm INVEST là **chấm sai đối tượng**: chúng không cần `Independent` (là một lát cắt xuyên tầng), và tiêu chí `Valuable` của chúng là **thông tin đo được**, không phải tính năng giao cho khách. ⇒ Cột `I`/`S` ghi **`n/a [MVP0]`**.
>
> **Definition of Done của hai Story này là 5 tiêu chí của gate [G1](../../010-Planning/MVP-Scope.md#72-g1--gate-kỹ-thuật-sau-mvp0)**, không phải Acceptance Criteria kiểu Gherkin:
>
> | Tiêu chí `G1` | Nội dung | Nhãn |
> |---|---|---|
> | **G1-a** | consistency **≥70%** | ⚠️ `[EM]` |
> | **G1-b** | **N ≤3** | `[OFF]` CF-3.1/3.2 |
> | **G1-c** | **≤30%** ⇒ PASS · 30–50% ⇒ có điều kiện · **>50%** ⇒ FAIL | ⚠️ `[EM]` **ngưỡng do writer run trước ĐỊNH NGHĨA TẠI RUN ĐÓ, KHÔNG CÓ NGUỒN NGOÀI** (CF-10.4) |
> | **G1-d** | panel **2 nhân vật ≥60%**; panel **3 nhân vật: đo và báo cáo, KHÔNG đặt ngưỡng chặn** | ⚠️ `[EM]` cùng cảnh báo như `G1-c` |
> | **G1-e** | **100%** panel có thoại dùng overlay; **0** panel nhờ model render chữ | — |
>
> ⛔ `CẤM-16`: **cấm sửa ngưỡng gate sau khi nhìn thấy kết quả** — *"đó là cách một gate biến thành nghi lễ"*. Ngưỡng được định nghĩa **TRƯỚC** khi đo.
>
> ⚠️ Trích `G1-c` / `G1-d` mà bỏ nhãn `[EM]` ⇒ chúng **mạo danh benchmark ngành**.

### 5.3 Điều kiện ra ngoài horizon — ghi ra để không mất dấu

| # | Tiêu chí | Nguồn |
|---|---|---|
| 8 | Continuity Checker hoạt động ở dạng **N-candidate selection**, **không phải flag+autofix** | **M4-1** · CF-8.10 — MVP4, **NGOÀI horizon** |
| 9 | Độ phủ checker được **CÔNG BỐ VỚI USER** đúng mức **40–60% số panel** `[EM]` CF-6.11 | **M4-2** — *"đừng để họ hiểu là được bảo vệ toàn diện"* |
| 10 | Export đủ định dạng (PDF / CBZ / webtoon) | `FR-H-04` (MVP3) |

> ⚠️ **Tiêu chí #9 là một nghĩa vụ giao tiếp, không phải một tính năng.** Nó là tiêu chí duy nhất trong cả bốn Epic E/F/G/H mà *"xong"* nghĩa là **một con số đã được nói ra với người dùng**.

### 5.4 Ba điều KHÔNG thuộc DoD của Epic này

1. ⛔ **Không** có tiêu chí *"cập nhật MOC"* — **PM giữ MOC** ở close-step của run.
2. ⛔ **Không** có tiêu chí về credit ledger / hard quota — thuộc [Epic-F](./Epic-Credit-And-Unit-Economics.md), `KC-7`. `H5` chỉ sở hữu **abuse control**, không sở hữu cưỡng chế chi phí.
3. ⛔ **Không** có tiêu chí nào định nghĩa lại `Continuity Checker` theo nghĩa cũ — `CẤM-12`.

---

## 6. Tài liệu liên quan

### 6.1 BRD cha & tầng Requirements

| Quan hệ | Tài liệu | Ghi chú |
|---|---|---|
| **BRD cha** | [BRD-008-Quality-And-Operations](../../020-Requirements/BRD/BRD-008-Quality-And-Operations.md) | **1:1 với Epic này** |
| PRD | [PRD-Comic-Studio — H. Chất lượng & vận hành](../../020-Requirements/PRD-Comic-Studio.md#h-chất-lượng--vận-hành) | `FR-H-01`…`FR-H-06` |
| NFR chi tiết | [SRS-Comic-Studio](../../020-Requirements/SRS-Comic-Studio.md) | *Determinism* và *Cost observability* là hai trục NFR mà eval kit đo |
| Epic phụ thuộc chéo | [Epic-Credit-And-Unit-Economics](./Epic-Credit-And-Unit-Economics.md) · [Epic-Image-Generation-Pipeline](./Epic-Image-Generation-Pipeline.md) · [Epic-Minimum-Editor](./Epic-Minimum-Editor.md) | export là **điều kiện doanh thu** Tầng 1 · golden dataset đo output của pipeline · preference data phát sinh trong editor; export **tái dùng compositor** của preview |

### 6.2 Use Case liên quan

| Use Case | Vì sao liên quan |
|---|---|
| [UC-09 — Export Chapter](../../020-Requirements/Use-Cases/UC-09-Export-Chapter.md) | Hiện thực hoá `H4` — *"lấy thành phẩm ra khỏi hệ thống"*. Exit criterion **M2-5** |
| [UC-06 — Generate Panel And Pick Variant](../../020-Requirements/Use-Cases/UC-06-Generate-Panel-And-Pick-Variant.md) | Nơi *"chọn X thay vì Y"* xảy ra ⇒ nguồn của **preference data** (`H2`), và là nơi **`H3` Continuity Checker sống bên trong** (không phải một UC riêng) |
| [UC-01 — Upload And Ingest Chapter](../../020-Requirements/Use-Cases/UC-01-Upload-And-Ingest-Chapter.md) | Nơi **abuse control cho upload** (`H5`) được cưỡng chế — giới hạn dung lượng / số upload, rate limit per tenant |

### 6.3 Tài liệu tham khảo

- [MVP-Scope.md](../../010-Planning/MVP-Scope.md) — **§3** nhóm H (`H1`…`H6`, nguồn của [mục 3](#3-story-trong-horizon) và [mục 4](#4-story-ngoài-horizon--chưa-có-file)) · **§3.1** kỷ luật MVP0 · **§7.2** [G1](../../010-Planning/MVP-Scope.md#72-g1--gate-kỹ-thuật-sau-mvp0) 5 tiêu chí (nguồn của [mục 5.2](#52-dod-của-hai-story-mvp0--đo-bằng-gate-g1-không-bằng-gherkin)) · **§7.3** [G2](../../010-Planning/MVP-Scope.md#73-g2--gate-kinh-tế-sau-mvp1)
- [Roadmap.md](../../010-Planning/Roadmap.md) — **§2** exit criteria **P-6**, **M1-6**, **M2-5**, **M4-1**, **M4-2** (nguồn của [mục 5](#5-definition-of-done-cấp-epic)) · **§3.1** kỷ luật MVP0 · **§4** **X-b** lưu ý phạm vi abuse control · **§5.1**, **§5.2** · §6.2 (golden dataset chặn **mềm** eval kit)
- [Charter-Comic-Studio.md](../../010-Planning/Charter-Comic-Studio.md) — **§4** điều kiện khả thi **R9** · **§8** giả định **A9** (độ phủ checker **40–60%** `[EM]`)
- [Glossary.md](../../999-Resources/Glossary.md) — `Continuity Checker` (định nghĩa **đã được sửa lại**) · `VLM autorater` · `HITL gate` · `eval kit` · `preference data` · `MVP0`
- [findings/business-analyst.md](../../010-Planning/pm-runs/2026-08-24-khoi-tao-requirements-stories-comic-studio/findings/business-analyst.md) — **§2.3** · **§4.8** (bảng 7 Story của Epic này) · **§4.9** (năm Story MVP0 — INVEST không áp) · **§4.10** · **§5.2** canonical facts CF-6.11, CF-8.7, CF-8.10, CF-10.4, CF-10.10 · **§5.3** lệnh cấm `CẤM-03`, `CẤM-11`, `CẤM-12`, `CẤM-16`
- [Analysis-Comic-Studio-Concept.md](../../050-Research/Analysis-Comic-Studio-Concept.md) — §3.2 (câu hỏi *"trang này đọc có ổn không?"*) · §12 (preference data là **moat thật**). ⛔ **Không sửa tài liệu này** (`CẤM-18`)
- [Documents-Template.md](../../../knowledge-base/99-Templates/Documents-Template.md) — **RULE-001**: thư mục, naming `Epic-{Title}.md`, frontmatter, **standard markdown link** (⛔ cấm wiki-link `[[...]]`)

> ⛔ **Không link tới `docs/030-Specs/`** — tầng technical spec chưa tồn tại và nằm ngoài scope của run này.
