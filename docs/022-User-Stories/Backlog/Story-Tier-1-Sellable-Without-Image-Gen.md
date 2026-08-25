---
id: STORY-F-03
type: story
status: draft
created: 2026-08-24
---

# Story-Tier-1-Sellable-Without-Image-Gen

## 1. Story

Là tác giả truyện chữ, tôi muốn mua gói Story Bible + Comic IR + layout + versioning + export mà KHÔNG có image gen, để dùng phần giá trị lõi mà không cần API key

## 2. Part of

- Epic cha: [Epic-Credit-And-Unit-Economics](../Epics/Epic-Credit-And-Unit-Economics.md)
- BRD: [BRD-006-Credit-And-Unit-Economics](../../020-Requirements/BRD/BRD-006-Credit-And-Unit-Economics.md)
- Use Case liên quan: [UC-09-Export-Chapter](../../020-Requirements/Use-Cases/UC-09-Export-Chapter.md) — **điều kiện doanh thu** của Tầng 1 (`M2-5`): không có export ở MVP2 thì Tầng 1 không bán được. UC thuộc `BRD-008` nhưng là **tiền đề** trực tiếp của Story này (Epic cha [mục 6.2](../Epics/Epic-Credit-And-Unit-Economics.md#62-use-case-liên-quan)). ⚠️ [UC-10-Manage-Credit-And-BYOK](../../020-Requirements/Use-Cases/UC-10-Manage-Credit-And-BYOK.md) là UC "chính chủ" của `BRD-006` nhưng **không áp dụng cho Story này** — Tầng 1 không có image gen nên không cần credit ledger hay BYOK

## 3. Bối cảnh & nguồn

> [!WARNING]
> ⚠️ **Đây là Story CÓ ĐIỀU KIỆN — không phải một increment sẵn sàng làm ngay khi nhặt lên.** [Roadmap §5.2](../../010-Planning/Roadmap.md#52--hệ-quả-tích-cực-thứ-có-thể-bán-được-trong-horizon) ghi nguyên văn: *"Đây là một **lựa chọn**, không phải một kế hoạch đã chốt. Nó cần founder quyết định tại G2... Ghi ra đây để anh **thấy được lựa chọn**, không phải để mặc định chọn nó."*
>
> **Điều kiện phải thoả ĐỒNG THỜI cả 4, trước khi Story này được coi là "sẵn sàng bán"** (Epic cha [mục 3](../Epics/Epic-Credit-And-Unit-Economics.md#3-story-trong-horizon) + [mục 5.1 tiêu chí #5](../Epics/Epic-Credit-And-Unit-Economics.md#51-điều-kiện-ra-trong-horizon--nguồn-là-roadmap-2)):
> 1. **G0 PASS** — gate pháp lý ([MVP-Scope §7.1](../../010-Planning/MVP-Scope.md#71-g0--gate-pháp-lý)), vì bán Tầng 1 là "dòng code thương mại đầu tiên".
> 2. **M2-5** — export ra **PDF của 1 chapter hoàn chỉnh** từ preview server-side đã hoàn thành ở MVP2 ([Roadmap §2](../../010-Planning/Roadmap.md#2-bảng-lộ-trình-tổng)).
> 3. **M2-6** — checklist safe harbour Điều 198b hoàn thành **nếu** trigger "mở cho người ngoài upload" đã đến ([Roadmap §2](../../010-Planning/Roadmap.md#2-bảng-lộ-trình-tổng) · [Roadmap §4 X-a](../../010-Planning/Roadmap.md#4-ba-việc-xen-ngang)).
> 4. **Quyết định tường minh của Founder tại gate G2** ([MVP-Scope §7.3](../../010-Planning/MVP-Scope.md#73-g2--gate-kinh-tế-sau-mvp1)) — không tự động chuyển sang "đang bán" chỉ vì code đã xong.
>
> Thiếu **bất kỳ một** trong bốn ⇒ Story này **KHÔNG** được coi là Ready để đưa vào bán, bất kể trạng thái kỹ thuật.

- [MVP-Scope §3](../../010-Planning/MVP-Scope.md#3-bảng-mvp-vs-full-scope) hạng mục **F6**: *"Tầng 1 bán được: Story Bible + Comic IR + layout + versioning + export, **KHÔNG image gen**"* — `❌` MVP0, `⛔` MVP1, `🟡 khả dĩ` tại MVP2, `✅` từ MVP3. Anchor gốc: CF-2.2 `[CHỐT]` — margin **~90%**, **không cần API key**.
- [Roadmap §5.2](../../010-Planning/Roadmap.md#52--hệ-quả-tích-cực-thứ-có-thể-bán-được-trong-horizon) `[EM]` — suy luận của lens `business-analyst`, **không có trong bảng canonical facts**: *"Tầng 1 ≈ MVP1 + MVP2 + export"*, tức **nằm gọn trong horizon** 09/2026–02/2027 nếu 3 điều kiện đầu (G0, M2-5, M2-6) đạt. Neo kỳ vọng đi kèm bắt buộc: **SOM năm 1 $4K–14K ARR ≈ $300–1.200 MRR, 30–80 paying user** ⚠️ `[EM]` CF-4.4 — thang **trăm đô/tháng**, không phải nghìn; đối chiếu **Anifusion** — solo founder, **$833 MRR**, có lãi, **~2 năm** kể từ launch, **$0 marketing** `[TC]` CF-4.5 (⚠️ nguồn mâu thuẫn: nguồn khác ghi **$5.000/tháng**; **$9/mo** vs **€20/mo** — ghi cả hai, không chọn một, theo `CẤM-07`).
- Epic cha [mục 3](../Epics/Epic-Credit-And-Unit-Economics.md#3-story-trong-horizon) đánh dấu `⭐` cho Story này và ghi rõ *"⛔ Không được làm phẳng thành 'trong horizon'"*.

## 4. Acceptance Criteria

### Xác minh được

- [ ] Story này CHỈ được đánh dấu trạng thái **"sẵn sàng bán"** khi có bằng chứng cả **4** điều kiện đồng thời đạt: bản ghi G0 PASS, exit criterion M2-5 đã tick, exit criterion M2-6 đã tick (hoặc trigger X-a chưa đến), và quyết định bằng văn bản của Founder tại gate G2 — đo bằng: kiểm tra tồn tại đủ 4 artifact/bản ghi xác nhận; thiếu 1 trong 4 ⇒ trạng thái phải là **"không sẵn sàng"**, không có trạng thái trung gian "sẵn sàng một phần"
- [ ] Tài khoản đăng ký gói Tầng 1 hoàn thành trọn vẹn luồng **upload → Story Bible → panel script (Comic IR) → layout → export PDF** của ≥1 chapter mà **không có bất kỳ lời gọi image-gen provider nào** được thực hiện trong suốt luồng đó — đo bằng: theo dõi log gọi provider trong toàn bộ phiên làm việc của tài khoản Tầng 1, số lời gọi image-gen = 0
- [ ] Mô hình subscription/tenant phân biệt được tài khoản Tầng 1 với Tầng 2/Tầng 3 mà **không cần retrofit schema** khi Tầng 2/3 được bật sau — đo bằng: tồn tại cột/enum phân loại tầng trên entity subscription, đổi tầng của một tài khoản không yêu cầu migration cấu trúc bảng

### Đường không hạnh phúc (unhappy path)

- [ ] Người dùng Tầng 1 cố gắng trigger một hành động sinh ảnh (gọi trực tiếp endpoint sinh ảnh, hoặc qua đường vòng khác) — hệ thống **từ chối**, không âm thầm tính phí hay tự động nâng cấp tầng — đo bằng: gọi endpoint sinh ảnh từ tài khoản Tầng 1, nhận lỗi từ chối rõ ràng (ví dụ `403 plan-not-allowed`), không có `generation` nào được tạo ra
- [ ] Gate G2 kết luận **FAIL** hoặc **KHÔNG CHẠY ĐƯỢC** ([MVP-Scope §7.3](../../010-Planning/MVP-Scope.md#73-g2--gate-kinh-tế-sau-mvp1)) trước khi Founder ra quyết định — Story này **không tự động** chuyển sang trạng thái "đang bán" dù mọi phần kỹ thuật đã sẵn sàng — đo bằng: kiểm tra không tồn tại cơ chế publish tự động khi thiếu bản ghi quyết định tường minh của Founder
- [ ] Trigger "mở cho người ngoài upload" ([Roadmap §4 X-a](../../010-Planning/Roadmap.md#4-ba-việc-xen-ngang)) xảy ra **trước** khi M2-6 hoàn thành — hệ thống không cho phép tài khoản mới ngoài tập tenant hiện có đăng ký Tầng 1 cho tới khi checklist safe harbour tick xong — đo bằng: thử đăng ký Tầng 1 mới từ một danh tính ngoài hệ thống trước khi M2-6 được đánh dấu hoàn thành, bị chặn

### Ràng buộc cứng không được vi phạm

- Không có `KC-x` / `C-x` / `AG-x` áp trực tiếp riêng cho Story này. Ràng buộc thay thế là **bộ 4 điều kiện gate/exit-criterion** đã liệt kê ở [mục 3](#3-bối-cảnh--nguồn): **G0** ([MVP-Scope §7.1](../../010-Planning/MVP-Scope.md#71-g0--gate-pháp-lý)) · **M2-5**, **M2-6** ([Roadmap §2](../../010-Planning/Roadmap.md#2-bảng-lộ-trình-tổng)) · quyết định Founder tại **G2** ([MVP-Scope §7.3](../../010-Planning/MVP-Scope.md#73-g2--gate-kinh-tế-sau-mvp1)). Vi phạm — tức bán Tầng 1 khi thiếu 1 trong 4 — là vi phạm ràng buộc cứng của chính Story này, không phải một rủi ro chấp nhận được

### Story này KHÔNG làm

- Không implement credit ledger, HOLD, hard quota, hay BYOK — các cơ chế đó thuộc `F3`/`F4`/`F5` (`Story-Credit-Ledger-With-Hold-Before-Enqueue`, `Story-Hard-Quota-Enforced-Before-Enqueue`, `Story-BYOK-As-Unlock-Option`), ngoài horizon (MVP3/MVP4), và **không cần thiết cho Tầng 1** vì Tầng 1 không có image gen
- Không tự quyết định "bán Tầng 1 hay không" thay Founder — quyết định thương mại hoá thuộc thẩm quyền Founder tại gate G2; Story này chỉ dựng sẵn khả năng kỹ thuật để quyết định đó thực thi được ngay khi PASS
- Không implement export PDF / CBZ / webtoon — đó là `Story-Export-Chapter-To-PDF-CBZ-Webtoon` (Epic-Quality-And-Operations, `H4`); Story này chỉ **tiêu thụ** kết quả export làm điều kiện tiên quyết (M2-5)
- Không implement checklist safe harbour Điều 198b — đó là `Story-Safe-Harbour-Checklist-Article-198b` (Epic-Legal-And-Compliance, `GP-3`); Story này chỉ **tiêu thụ** M2-6 làm điều kiện

## 5. Ước lượng

| Đại lượng | Giá trị | Ghi chú |
|---|---|---|
| `E_build` | ~10 giờ-người `[EM]` | Logic phân loại tầng subscription + chặn endpoint image-gen cho tài khoản Tầng 1 + gắn trạng thái "sẵn sàng bán" vào 4 điều kiện tiền đề. Trong trần 16h. ⚠️ Con số này **chỉ đo phần code tier-gating** — phần lớn "effort" thật để Tầng 1 bán được nằm ở `M2-5` (export) và `M2-6` (safe harbour), là hai Story riêng, **không cộng vào đây** |
| `E_hitl` | 0 | Story này không tạo HITL gate mới; các human gate của pipeline xuất bản (M2-4) thuộc Epic-C, không phải Story này |

## 6. INVEST

- **I (Independent)**: ⚠️ `[PO suy luận]` — theo bảng [`findings/business-analyst.md` §4.6](../../010-Planning/pm-runs/2026-08-24-khoi-tao-requirements-stories-comic-studio/findings/business-analyst.md#46-epic-credit-and-unit-economics-brd-006--3-trong-1-có-điều-kiện--3-ngoài) Story này mang cờ `⚠️` cho `I` nhưng **không có hàng chi tiết** trong [§4.10](../../010-Planning/pm-runs/2026-08-24-khoi-tao-requirements-stories-comic-studio/findings/business-analyst.md#410-bảy-story-sẽ-vỡ-khi-cắt-lô--pm-cần-biết-trước). Lý do suy ra từ chính dữ liệu bảng: Story này **không tự đứng được** — nó phụ thuộc chặt vào kết quả của 3 tiền đề nằm ở 2 Epic khác (`M2-5` thuộc Epic-Quality-And-Operations, `M2-6` thuộc Epic-Legal-And-Compliance) cộng với **G0 PASS** (hoạt động pháp lý ngoài backlog) và **một quyết định thương mại của Founder tại gate G2** mà lịch của nó không do backlog kiểm soát. "Xong về kỹ thuật" và "sẵn sàng về sản phẩm" là hai trạng thái tách rời ở đúng Story này — khác mọi Story còn lại của Epic-F.
- **S (Small)**: ⚠️ `[PO suy luận]` — cùng lý do gốc: `E_build` đo được và nhỏ (~10h) cho **riêng phần code tier-gating**, nhưng kích thước thật của việc "làm cho Tầng 1 bán được" bị che khuất bởi việc Story này là một **cổng tổng hợp** (aggregation gate) của 3 tiền đề độc lập. Ghi một số giờ nhỏ cho riêng Story này tạo ảo giác nó rẻ, trong khi giá trị sản phẩm thật của nó phụ thuộc tiến độ của 2 Epic khác và thời điểm quyết định của Founder — những thứ không nằm trong `E_build`/`E_hitl` của chính Story.

---

_Created by product-owner_
_Author: trisjr_
