# Run Plan: 2026-08-24-khoi-tao-requirements-stories-comic-studio

**Lane**: doc · **Shape**: A (authoring) · **Tier**: **T3** (4/4 điểm triage — điểm cao nhất có thể)

## Phases

| # | Phase | Agent | Song song? | Input | Output |
|---|-------|-------|-----------|-------|--------|
| 1 | Intake & Triage | PM | — | Yêu cầu gốc + 2 run trước | `brief.md` |
| 2a | Phân rã requirement (lens chịu lực) | `business-analyst` | ✅ với 2b, 2c | 5 file Planning + 2 Analysis + Glossary | `findings/business-analyst.md` |
| 2b | Ranh giới SRS ↔ 030-Specs | `architect` | ✅ | Analysis §5–6, MVP-Scope E/F/G | `findings/architect.md` |
| 2c | Framework ưu tiên + Story contract | `product-owner` | ✅ | MVP-Scope §1.1/§3/§7, Roadmap, OKRs | `findings/product-owner.md` |
| 3 | **GATE** | PM + anh | — | 2a + 2b + 2c | `run-plan.md` duyệt, 4 câu chốt |
| 4 | Doc plan | PM | — | 3 findings | `outline.md` |
| 5 | Soạn thảo — 20 lô | 8 loại writer | phần lớn ✅ | `outline.md` §2 + findings theo path | 72 file |
| 6 | Verify — 4 lô | `context-auditor` ×4 | ✅ | 72 deliverable | `verdict.md` |
| 7 | Close-step | PM | — | verdict | 2 MOC + `000-Index` + RULE-001 + `cost.md` + commit |

> **Ba lens của phase 2 đã chạy xong trước gate** (đúng thiết kế `pm-doc.md` Bước 2 — read-only, không chạm vùng deliverable). Cả ba trả `DONE`: 17 · 40 · 24 tool call trên trần 60.

## Tóm tắt phân tích (Bước 2)

Chi tiết: [findings/business-analyst.md](./findings/business-analyst.md) · [findings/architect.md](./findings/architect.md) · [findings/product-owner.md](./findings/product-owner.md)

1. ⭐⭐ **`MVP-Scope §3` có TÁM nhóm, không phải bảy.** Yêu cầu gốc và triage của PM đều nói *"BRD cho từng module"* trên giả định 7 module A–G. Nhóm **H. Chất lượng & vận hành** bị bỏ sót, và nó chứa H1 (HITL gate + eval kit = điều kiện khả thi **R9** của Charter), H2 (preference data = moat), H4 (export = *"thứ duy nhất người dùng thật sự nhận được"*), H6 (golden dataset, `✅` ở mọi mốc). ⇒ **8 BRD, 8 Epic.**
2. ⭐⭐ **Khoảng trống lớn nhất của tầng Requirements: KHÔNG có persona / JTBD / định nghĩa "đủ tốt"** trong toàn repo (`KT-1`). Analysis §3.2 đã gọi thẳng điều này. Repo có *phân khúc* (`[CHỐT]` tác giả truyện chữ không biết vẽ) nhưng không có persona. ⇒ PRD mục 3 **phải mở bằng `TBD` có cấu trúc** và writer báo `PARTIAL`. Không phân xử ngầm được.
3. **Trục Epic = module A–H, không phải mốc MVP0–MVP4.** Căn cứ từ chính repo: `MVP-Scope §1.1` phân định *"khi nào"* thuộc `Roadmap.md`. Epic theo mốc tạo nguồn sự thật **thứ hai** về thời gian, và nó vỡ ngay lần đầu lịch trượt — mà `Roadmap §1.3` tự xếp *"MVP1 tràn khỏi Q4/2026"* là rủi ro lịch số 1.
4. **Quy mô: 51 Story** — 41 trong horizon (1 có điều kiện) / 10 ngoài. **11 Use Case.** **7 Story được đánh dấu sẽ vỡ `Independent`/`Small`** kèm lý do không cắt được theo đường nào; **5 Story MVP0 mà INVEST không áp** (chúng là một vertical slice, DoD lấy từ 5 tiêu chí gate G1).
5. **SRS: 68 hàng requirement** (`SRS-FR-01…42` / `SRS-NFR-01…26`) — 55 CHỐT · 6 MẶC ĐỊNH · 7 CHƯA QUYẾT. **17 NFR có số đo được**, **14 NFR không có số nằm riêng dưới nhãn `TBD` và lens từ chối gán số**. Nguyên tắc phân định SRS ↔ 030 **không phải "WHAT vs HOW"** mà là **"đã-quyết + không-đảo-được-rẻ"** — vì `FOR UPDATE SKIP LOCKED` và key `tenant/{tenant_id}/{sha256}` đều là "how" nhưng retrofit sau là migration xuyên hệ thống.
6. ⭐ **Lens PO bác CẢ RICE lẫn MoSCoW**, không phải chọn một. RICE hỏng ở **cả tử số và mẫu số**: `Reach` không có mẫu số dân số (chưa có tenant nào, chưa có design partner), `Effort` không có đơn vị (`Roadmap §1.3` tự khai *"Tổng tuần-người: TBD"* cho cả 4 mốc). MoSCoW **trùng 1:1 và lossy hơn** hệ nhãn `✅🟡⛔❌` của `MVP-Scope §3` — MVP-Scope gán nhãn theo **5 cột mốc**, MoSCoW chỉ có **một nhãn vô hướng**. Thay bằng `UNLOCK-ORDER`. **Đây là điểm lệch khỏi chữ anh viết ⇒ câu gate #2.**
7. **AC = checklist 4 khối, KHÔNG Gherkin.** Lý do quyết định: exit criteria trong repo **đã** ở dạng assertion đo được (`M2-2`: *"insert panel 4 nhân vật bị **từ chối**, không phải bị **cảnh báo**"*); bọc vào `Given/When/Then` thêm ngữ pháp mà **mất khả năng đối chiếu 1:1** với exit criterion của mốc. `Small` neo vào **giờ-người** (`E_build ≤ 16h` / `E_hitl ≤ 2h/chapter`), không story point.
8. **57 canonical facts + 18 lệnh cấm tường minh** đã thu được (47 CF kế thừa giữ nguyên id, 10 CF mới). Ba caveat của `23% GRR` và lệnh **CẤM TRỪ `CF-6.8` cho `CF-6.7`** được trích nguyên văn.

### Mâu thuẫn / khoảng trống — đưa vào tài liệu dưới dạng `TBD`, KHÔNG phân xử ngầm

- **7 mâu thuẫn nội bộ repo** (`MT-1`→`MT-7`) và **14 khoảng trống** (`KT-1`→`KT-14`) — chi tiết `findings/business-analyst.md` §6.
- **`GP-4` AI disclosure: hai nguồn trong repo mô tả phạm vi KHÁC NHAU.** `Charter §7 C4` chốt cách xử lý: thiết kế theo diễn giải **rộng** cho tới khi luật sư chốt. Writer ghi cả hai cách đọc, không chọn một.
- **`Template-SRS.md` thực tế chỉ có 5 mục đánh số**, không phải 7 như PM ghi trong prompt lens. Lens đã flag và **không tự thêm 2 mục** — đúng kỷ luật. `outline.md` §2.2 chốt cấu trúc 6 mục.
- **`Story-Tier-1-Sellable-Without-Image-Gen` là một LỰA CHỌN `[EM]`, không phải kế hoạch đã chốt** (`Roadmap §5.2`), gated on G0 PASS + M2-5 + M2-6 + quyết định Founder tại G2. Cờ của nó là `[TRONG HORIZON — CÓ ĐIỀU KIỆN]`.

## Bảng đích tài liệu (tra Document Type Mapping — RULE-001)

| Loại tài liệu | Có trong Mapping? | Thư mục đích | Naming | Số file | `type` | `status` đích |
|---|---|---|---|---:|---|---|
| PRD | ✅ `PRD-{ProjectName}.md` | `docs/020-Requirements/` | `PRD-Comic-Studio.md` | 1 | `prd` | `draft` |
| SRS | ✅ `SRS-{ProjectName}.md` | `docs/020-Requirements/` | `SRS-Comic-Studio.md` | 1 | `srs` | `draft` |
| BRD | ✅ `BRD-{NNN}-{Title}.md` | `docs/020-Requirements/BRD/` | `BRD-001…008-*` | 8 | `brd` | `draft` |
| Use Case | ✅ `UC-{NN}-{Title}.md` | `docs/020-Requirements/Use-Cases/` | `UC-01…11-*` | 11 | `use-case` | `draft` |
| Epic | ✅ `Epic-{Title}.md` | `docs/022-User-Stories/Epics/` | `Epic-*` | 8 | `epic` | `draft` |
| User Story | ✅ `Story-{Title}.md` | `docs/022-User-Stories/Backlog/` | `Story-*` | 41 | `story` | `draft` |
| **Prioritized Backlog** | ❌ **KHÔNG có** | `docs/022-User-Stories/` | `Backlog-Priority.md` | 1 | `backlog-priority` | `draft` |
| Glossary | ✅ `Glossary.md` | `docs/999-Resources/` | `Glossary.md` (**sửa**) | 1 | `glossary` | `live` (giữ) |
| | | | **Tổng** | **72** | | |

> ⚠️ **Hàng *Prioritized Backlog* là vấn đề contract — câu gate #3.** Đường dẫn anh chỉ định (`docs/022-User-Stories/Backlog-Priority.md`) **nằm đúng trong hệ Dewey**, nên không vi phạm guardrail *"không tạo thư mục ngoài Dewey"*. Vấn đề duy nhất: **loại tài liệu chưa được đăng ký** trong bảng Mapping của RULE-001 (`status: approved`), và RULE-001 quy tắc #7 cấm tạo tài liệu chưa tra bảng. Tiền lệ có sẵn: hàng `MVP Scope` được thêm additive tại gate run `2026-08-23`.

> **`status: draft` cho toàn bộ 72 file là cố ý.** `Charter §9` còn **ba điều kiện chặn cấp dự án chưa gỡ**, trong đó có tư vấn luật sư SHTT trước khi thương mại hoá. Một PRD `approved` khi ba blocker còn treo là tự tuyên bố sai. Chúng chuyển `approved` khi anh ra quyết định Go/No-Go.

> ⚠️ **Glossary — câu gate #1.** Yêu cầu chỉ `knowledge-base/01-Metas/Glossary.md`; RULE-001 Mapping chỉ `docs/999-Resources/Glossary.md`. Hai file **đều tồn tại và khác nhau về bản chất**: file `docs/` là từ điển domain `comic-studio` (54 term: `Story Bible`, `Comic IR`, `best-of-N`, `tenant_id`…); file `knowledge-base/` là từ điển **hệ điều hành TNMCORE-OS** (`Spec-Driven Development`, `MCP`, `Agentic AI`, `Dewey Decimal System`). Ubiquitous Language của **sản phẩm** thuộc file thứ nhất.

## File ownership map

| Agent | Sở hữu (được ghi) | Cấm chạm |
|-------|-------------------|----------|
| `business-analyst` (2a) | `findings/business-analyst.md` | toàn bộ phần còn lại — ✅ đã tuân thủ |
| `architect` (2b) | `findings/architect.md` | như trên — ✅ đã tuân thủ |
| `product-owner` (2c) | `findings/product-owner.md` | như trên — ✅ đã tuân thủ |
| **PM** | `pm-runs/<run-id>/**` · **mọi `*-MOC.md`** · **`docs/000-Index.md`** · `knowledge-base/99-Templates/Documents-Template.md` | — |
| `business-analyst` #1 (L1) | `docs/020-Requirements/PRD-Comic-Studio.md` | MOC, `000-Index`, `outline.md`, file của writer khác |
| `architect` #1 (L2) | `docs/020-Requirements/SRS-Comic-Studio.md` | như trên **+ toàn bộ `docs/030-Specs/`** |
| `business-analyst` #2 (L3) | `BRD/BRD-001-*`, `BRD-002-*`, `BRD-003-*` | như trên |
| `business-analyst` #3 (L4) | `BRD/BRD-004-*`, `BRD-005-*`, `BRD-006-*` | như trên |
| `security-auditor` #1 (L5a) | `BRD/BRD-007-Legal-And-Compliance.md` | như trên |
| `quality-assurance` #1 (L5b) | `BRD/BRD-008-Quality-And-Operations.md` | như trên |
| `business-analyst` #4 (L6) | `Use-Cases/UC-01…04-*` (4 file) | như trên |
| `product-designer` (L7) | `Use-Cases/UC-05…08-*` (4 file) | như trên |
| `business-analyst` #5 (L8) | `Use-Cases/UC-09…11-*` (3 file) | như trên |
| `product-owner` #1 (L9) | `Epics/Epic-Image-Generation-Pipeline`, `-Story-Intelligence`, `-Comic-Director-And-Layout`, `-Minimum-Editor` | như trên |
| `product-owner` #2 (L10) | `Epics/Epic-Multi-Tenancy-And-Platform`, `-Credit-And-Unit-Economics`, `-Legal-And-Compliance`, `-Quality-And-Operations` | như trên |
| `product-owner` #3–#6, `architect` #2, `security-auditor` #2, `quality-assurance` #2 (L11–L18) | **8 lô Story rời nhau theo Epic** — mỗi writer chỉ ghi đúng các `Backlog/Story-*.md` của Epic mình được giao | như trên **+ Story của Epic khác** |
| `product-owner` #7 (L19) | `docs/022-User-Stories/Backlog-Priority.md` | như trên |
| `business-analyst` #6 (L20) | `docs/999-Resources/Glossary.md` | như trên |
| `context-auditor` #1–#4 (L21–L24) | — *(verify read-only)* | toàn bộ repo |

**Các tập ownership rời nhau tuyệt đối** — 72 deliverable, không file nào có hai chủ.
**Điểm hội tụ (`*-MOC.md`, `000-Index.md`, `outline.md`, RULE-001) thuộc PM, không cấp cho bất kỳ worker nào.**

## Kế hoạch dispatch theo lô & ngân sách

| Lô | Nội dung | File | Worker | Chạy | Ngân sách |
|---|---|---:|---|---|---:|
| L1 | PRD | 1 | `business-analyst` | ✅ song song L2 | 60 |
| L2 | SRS | 1 | `architect` | ✅ | 60 |
| L3 | BRD-001…003 | 3 | `business-analyst` #2 | ✅ | 60 |
| L4 | BRD-004…006 | 3 | `business-analyst` #3 | ✅ | 60 |
| L5a | BRD-007 Legal | 1 | `security-auditor` | ✅ | 60 |
| L5b | BRD-008 Quality | 1 | `quality-assurance` | ✅ | 60 |
| L6 | UC-01…04 | 4 | `business-analyst` #4 | ⛔ sau L1, L3–L5 | 60 |
| L7 | UC-05…08 | 4 | `product-designer` | ⛔ sau L1, L3–L5 | 60 |
| L8 | UC-09…11 | 3 | `business-analyst` #5 | ⛔ sau L1, L3–L5 | 60 |
| L9 | Epic A–D | 4 | `product-owner` | ⛔ sau L1 | 60 |
| L10 | Epic E–H | 4 | `product-owner` #2 | ⛔ sau L1 | 60 |
| L11 | Story Epic-A | 5 | `product-owner` #3 | ⛔ sau L9 | 60 |
| L12 | Story Epic-B | 4 | `product-owner` #4 | ⛔ sau L9 | 60 |
| L13 | Story Epic-C | 7 | `product-owner` #5 | ⛔ sau L9 | 60 |
| L14 | Story Epic-D | 5 | `product-owner` #6 | ⛔ sau L9 | 60 |
| L15 | Story Epic-E | 5 | `architect` #2 | ⛔ sau L10 | 60 |
| L16 | Story Epic-F | 3 | `product-owner` #7 | ⛔ sau L10 | 60 |
| L17 | Story Epic-G | 6 | `security-auditor` #2 | ⛔ sau L10 | 60 |
| L18 | Story Epic-H | 6 | `quality-assurance` #2 | ⛔ sau L10 | 60 |
| L19 | `Backlog-Priority.md` | 1 | `product-owner` #8 | ⛔ **tuần tự sau L11–L18** | 60 |
| L20 | Glossary (sửa) | 1 | `business-analyst` #6 | ⛔ sau L19 | 60 |
| L21 | **Verify** tầng 020 (PRD+SRS+8 BRD+11 UC) | 21 | `context-auditor` #1 | ✅ | 60 |
| L22 | **Verify** tầng 022 (8 Epic + 41 Story) | 49 | `context-auditor` #2 | ✅ | 60 |
| L23 | **Verify** cross-cutting (CF · traceability · link graph · Backlog-Priority · Glossary) | — | `context-auditor` #3 | ✅ | 60 |
| L24 | **Verify** close-step (2 MOC + `000-Index` + RULE-001) | — | `context-auditor` #4 | ⛔ sau close-step | 60 |

**Tổng ngân sách cấp**: 24 lô × 60 = **1.440 tool call**. Lane doc không có phụ cấp mutation-test.
**Ước lượng chi phí thô**: 24 spawn × ~0,4M (chi phí cố định 15 turn đầu, đo run trước) ≈ **9,6M** sàn, cộng phần chạy thật. Cộng cả PM main loop, run này ở thang **20–40M cache read** — gấp 2–3 lần run `2026-08-23` (116M tổng thì không, run đó đã là 116M; run này ước **150–250M**). Đây là con số anh cần thấy trước khi duyệt.

### ⚠️ Lệch tường minh khỏi `pm-doc.md` Bước 5 mục 1 — **giải tại gate, không giải ngầm**

`pm-doc.md` ghi: *"Một dispatch = một tài liệu (Shape A)"*. Run này **cố tình vi phạm** với BRD (3/lô), UC (3–4/lô), Epic (4/lô), Story (3–7/lô).

**Số học biện minh**: 72 file × 1 dispatch = **72 spawn**. Chi phí cố định mỗi spawn đo được ở run `2026-08-23` là **~0,37M** cho 15 turn đầu ⇒ **~26,6M chỉ tiền khởi động**, trước khi viết một chữ nào. Cắt xuống 20 lô writer ⇒ **~7,4M**, tiết kiệm **~19M**.

**Vì sao cắt lô như vậy vẫn an toàn**: `pm-core.md` nói rõ **số file là để CẮT lô, ngân sách tool call là thứ CHẶN**. Mỗi lô Story ≤7 file, mỗi file ~60–100 dòng, cùng một Epic ⇒ **cùng một tập nguồn** (một bảng findings + cùng nhóm `MVP-Scope §3`) ⇒ chi phí đọc được khấu hao, không nhân lên. Lô nào chạm trần 60 thì trả `PARTIAL` và PM cắt tiếp — cơ chế chặn vẫn nguyên vẹn.

## Ràng buộc bắt buộc cho mọi dispatch writer

1. **RULE-001** — đúng thư mục, đúng naming convention, frontmatter đủ `id / type / status / created`.
2. ⛔ **Standard markdown link relative path `[Text](./path.md)`. CẤM wiki-link `[[...]]`** (RULE-001 quy tắc #5). Có tiền lệ được duyệt ở run `2026-08-23`.
3. ⛔ **Không chạm `*-MOC.md`, `docs/000-Index.md`, `outline.md`, RULE-001** — PM giữ. Kể cả khi DoD mục **D5** của `findings/product-owner.md` yêu cầu cập nhật `Stories-MOC.md`: **PM override, writer không làm.**
4. ⛔ **Không link tới bất kỳ file nào trong `docs/030-Specs/`** — tầng rỗng, `Specs-MOC.md` 0 byte, ngoài scope. Link như vậy là link chết ngay khi tạo.
5. **Mọi con số dùng chung copy từ `findings/business-analyst.md` §5.2, kèm NGUYÊN nhãn nguồn và NGUYÊN caveat.** Cấm tự suy ra số mới từ số đã có nhãn `[EM]` mà không mang nhãn theo. **Ba lệnh cấm phải dán nguyên văn vào mọi prompt**: CẤM TRỪ `CF-6.8` cho `CF-6.7` · `23% GRR` phải mang đủ ba caveat · `Continuity Checker` chỉ có nghĩa QA-based selection giữa N candidate và `best-of-N` ≠ `retry-on-failure`.
6. **Không bịa số liệu, ngày tháng, tên người, quyết định lịch sử, persona.** Không có nguồn → ghi `TBD` kèm lý do và báo `PARTIAL`.
7. **Sửa file đã có → bump `updated: 2026-08-24`, giữ nguyên `id` / `created` / `status`.** Chỉ áp cho L20 (Glossary). Ghi đè frontmatter cũ là **lỗi im lặng** — verify kiểm riêng điểm này.
8. Tiếng Việt, technical term giữ nguyên tiếng Anh (`.claude/rules/create-file-markdown.md`). Tên file ASCII (`QC-2`).
9. **Ngân sách 60 tool call. Còn dưới trần thì TIẾP TỤC LÀM — chỉ dừng khi thật sự chạm trần.** (`cost.md` run trước: `researcher` tự cắt scope ở 51/60 vì *"hết ngân sách"* khi còn 9 call.)

## Bốn tiêu chí verify + hai tiêu chí bổ sung

| # | Tiêu chí | Lô |
|---|---|---|
| 1 | **Completeness** — đủ hạng mục `outline.md`, frontmatter đủ trường, `updated` đã bump | L21, L22 |
| 2 | **Correctness** — nội dung khớp *Nguồn sự thật*, 0 khẳng định không căn cứ | L21, L22 |
| 3 | **Coherence** — không mâu thuẫn tài liệu liền kề, thuật ngữ nhất quán với `Glossary.md` | L21, L22, L23 |
| 4 | **Connectivity** — mọi link phân giải được, 0 file orphan, 0 link tới `030-Specs/` | L23 |
| 5 | **Canonical facts sweep** — 57 CF: đối chiếu **mọi nơi** chúng xuất hiện, kiểm giá trị **và** nhãn **và** caveat | L23 |
| 6 | **Khuyến nghị bị rơi** — sweep từng khuyến nghị trong `outline.md` + 3 findings xem có landed không | L23 |

> Tiêu chí 5 và 6 là **mặc định, không phải tuỳ chọn** — `cost.md` run trước bài học #4: biến tiêu chí 6 thành yêu cầu tường minh cho kết quả **0 khuyến nghị bị rơi**, và đó là *"thay đổi rẻ nhất có tỉ suất cao nhất"*.
> **L24 tồn tại vì bài học #5**: lỗi MAJOR `M-1` của run trước là do **PM tự sửa Glossary ở close-step sau khi verify đã chạy**. Run này Glossary có writer (L20, trong scope L23) **và** close-step của PM có verify pass riêng (L24).
> **PM tự chạy check cơ học trước** khi dispatch verify: frontmatter đủ trường, link target tồn tại, `grep` ngày tháng trong `Backlog-Priority.md`. Để verifier tiêu call vào correctness/coherence chứ không vào việc `grep` thay được.

## Gate

- **Trình ngày**: 2026-08-24 — một lượt `AskUserQuestion`, 4 câu
- **Kết quả**: ✅ **Duyệt như plan — cả 4 câu theo đúng đề xuất của PM**, không điều chỉnh

| Câu | Nội dung | Đáp án của anh |
|---|---|---|
| 1 | Glossary ghi vào file nào? | ⭐ **`docs/999-Resources/Glossary.md`** — từ điển domain, đúng RULE-001 Mapping |
| 2 | Framework ưu tiên: RICE/MoSCoW hay `UNLOCK-ORDER`? | ⭐ **`UNLOCK-ORDER`** |
| 3 | `Backlog-Priority.md` chưa có trong RULE-001 Mapping | ⭐ **Thêm 1 hàng additive** |
| 4 | Duyệt scope 72 file / 24 lô? | ⭐ **Duyệt như plan — 72 file** |

### Hệ quả của đáp án gate

1. **Glossary: chỉ sửa `docs/999-Resources/Glossary.md`.** `knowledge-base/01-Metas/Glossary.md` **không bị chạm** trong run này — nó là từ điển của hệ điều hành TNMCORE-OS, phạm vi khác. Ghi vào *Nợ lại* nếu về sau anh muốn đồng bộ hai chiều.
2. **`UNLOCK-ORDER` là framework chính thức của `Backlog-Priority.md`.** Hệ quả bắt buộc: tài liệu **không được** có cột `RICE Score` hay nhãn `Must/Should/Could/Won't`; cột `Mốc` và `Scope-Label` là **kế thừa, cấm chấm lại**. Writer L19 nhận `findings/product-owner.md` §1.4 + §3 làm contract.
3. **RULE-001 được sửa ở close-step, KHÔNG sửa trước** — writer không đụng tới nó. Đúng một hàng additive vào Document Type Mapping, bump `updated`, ghi nhật ký theo khuôn comment đã có ở đầu file.
4. **10 Story ngoài horizon: không tạo file.** Chúng là hàng trong Epic cha (mục 4) + hàng trong `Backlog-Priority.md` với `Trạng thái tài liệu = chưa có file`. Đây là **nợ có chủ đích, đã khai báo**, không phải bỏ sót.
5. **Không escalation nào phát sinh tại gate** ⇒ chưa tạo `escalations.md`.
