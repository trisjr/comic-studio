# Run Plan: 2026-08-23-khoi-tao-tai-lieu-planning-comic-studio

**Lane**: doc · **Shape**: A (authoring) · **Tier**: **T3** (3/4 điểm triage)

## Phases

| # | Phase | Agent | Song song? | Input | Output |
|---|-------|-------|-----------|-------|--------|
| 1 | Intake & Triage | PM | — | Yêu cầu gốc + run trước | `brief.md` |
| 2a | Inventory kho docs (**kiêm probe Write-block**) | `context-auditor` | ✅ với 2b | RULE-001, `docs/**` | `findings/inventory.md` |
| 2b | Market sizing + đối thủ (delta) | `researcher` | ✅ với 2a | findings run trước, web | text → PM ghi `findings/researcher.md` |
| 3 | **GATE** | PM + anh | — | 2a + 2b | `run-plan.md` duyệt, 3 câu chốt |
| 4 | Doc plan + **bảng canonical facts** | PM | — | Analysis run trước | `outline.md` |
| 5a | Scaffolding Dewey + `000-Index.md` | **PM** | trước 5b | `findings/inventory.md` | ~20 thư mục + `docs/000-Index.md` |
| 5b-1 | Charter | `business-analyst` | ✅ | `outline.md` §Charter | `Charter-Comic-Studio.md` |
| 5b-2 | MVP-Scope + Roadmap | `architect` | ✅ | `outline.md` §MVP + §Roadmap | 2 file `010-Planning/` |
| 5b-3 | Risk Register | `security-auditor` | ✅ | `outline.md` §Risk | `Risk-Register.md` |
| 5b-4 | Research Notes | `business-analyst` (instance 2) | ✅ | `findings/researcher.md` | `Analysis-Market-Competitor-Landscape.md` |
| 5b-5 | OKRs | `product-owner` | ⛔ **tuần tự sau 5b-2** | Roadmap + MVP-Scope đã chốt | `OKRs.md` |
| 6 | Verify | `context-auditor` (instance mới) | — | 6 deliverable | `verdict.md` |
| 7 | Close-step | PM | — | verdict | MOC, Glossary, `cost.md`, commit |

> **Vì sao 5b-5 tuần tự**: Key Result của OKR phải trỏ tới đúng mốc trong Roadmap và đúng ranh giới trong MVP-Scope. Viết song song thì hai bên tự suy diễn ra hai bộ số. Đây là chỗ ghép chặt nhất của cả run.

> **Vì sao `context-auditor` vẫn được làm verifier dù đã chạy phase 2a**: nó không viết **deliverable** nào — 2a chỉ sinh run-state read-only. Phase 6 dùng **instance mới, context sạch**, không thừa hưởng kết luận của 2a. Guardrail "verify phải khác agent đã thực thi" nhắm vào **writer**, và không writer nào của phase 5b là `context-auditor`.

## File ownership map

| Agent | Sở hữu (được ghi) | Cấm chạm |
|-------|-------------------|----------|
| `context-auditor` (2a) | `pm-runs/<run-id>/findings/inventory.md` | **Toàn bộ phần còn lại của repo.** Không tạo thư mục, không tạo `000-Index.md`, không sửa MOC |
| `researcher` (2b) | — *(không có tool Write)* | Toàn bộ repo |
| **PM** | `pm-runs/<run-id>/**`, **mọi `*-MOC.md`**, **`docs/000-Index.md`**, `docs/999-Resources/Glossary.md`, mọi thư mục mới | — |
| `business-analyst` #1 (5b-1) | `docs/010-Planning/Charter-Comic-Studio.md` | `*-MOC.md`, `docs/000-Index.md`, `outline.md`, mọi file của writer khác |
| `architect` (5b-2) | `docs/010-Planning/MVP-Scope.md`, `docs/010-Planning/Roadmap.md` | như trên |
| `security-auditor` (5b-3) | `docs/010-Planning/Risk-Register.md` | như trên |
| `business-analyst` #2 (5b-4) | `docs/050-Research/Analysis-Market-Competitor-Landscape.md` | như trên |
| `product-owner` (5b-5) | `docs/010-Planning/OKRs.md` | như trên |
| `context-auditor` (6) | — *(verify read-only)* | Toàn bộ repo |

**Các tập ownership rời nhau tuyệt đối** — 6 deliverable, 5 writer, không file nào có hai chủ.
**Điểm hội tụ (`*-MOC.md`, `000-Index.md`, `outline.md`) thuộc về PM, không cấp cho bất kỳ worker nào.**

## Kế hoạch dispatch theo lô & ngân sách

| Lô | Nội dung | Worker | Chạy | Ngân sách tool call |
|---|---|---|---|---:|
| L1 | Inventory docs + probe Write | `context-auditor` | ✅ song song L2 | 60 |
| L2 | Market sizing + đối thủ | `researcher` | ✅ song song L1 | 60 |
| L3 | Charter (1 file) | `business-analyst` | ✅ song song L4-L6 | 60 |
| L4 | MVP-Scope + Roadmap (2 file) | `architect` | ✅ | 60 |
| L5 | Risk Register (1 file) | `security-auditor` | ✅ | 60 |
| L6 | Research Notes (1 file) | `business-analyst` #2 | ✅ | 60 |
| L7 | OKRs (1 file) | `product-owner` | ⛔ sau L4 | 60 |
| L8 | Verify 6 deliverable | `context-auditor` | — | 60 |

**Tổng ngân sách cấp**: 8 lô × 60 = **480 tool call**. Lane doc không có phụ cấp mutation-test.
Không lô nào vượt 2 file ⇒ nằm trong heuristic 3–5 file.

## Hai biến thể của Bước 5 — chọn theo kết quả probe

Run trước ghi nhận subagent bị chặn `Write` (*"Subagents should return findings as text, not write report files"*), khiến PM tiêu **79% output token**. Guardrail không nằm trong `settings.json` ⇒ là hành vi harness, chưa rõ còn hiệu lực không.

| | **Biến thể 1 — Write hoạt động** | **Biến thể 2 — Write bị chặn** |
|---|---|---|
| Kích hoạt khi | `findings/inventory.md` xuất hiện trên đĩa sau L1 | `context-auditor` trả text kèm báo `Write` bị chặn |
| Bước 5b | Dispatch 5 writer như bảng trên | **PM tự viết cả 6 tài liệu.** Writer bị hạ vai trò thành *lens soạn thảo*: chỉ dispatch cho những mục thật khó (Risk Register scoring, MVP Go/No-Go criteria), trả về đoạn văn, PM ghép |
| Lý do | Đúng thiết kế của `pm-doc.md` | `cost.md` run trước bài học #1: *"dispatch chỉ để nhận text rồi tự ghi thì đắt hơn tự viết"*. Và 6 tài liệu này là **synthesis 100–250 dòng từ nguồn PM đã có trong context**, khác hẳn tài liệu nghiên cứu 1.148 dòng của run trước |
| Rủi ro | Writer lệch nhau ở các con số dùng chung | Context PM phình, chi phí `turns^1.74` |
| Giảm thiểu | **Bảng canonical facts trong `outline.md`** — mọi số dùng chung do PM chốt sẵn **kèm nhãn caveat**, writer copy nguyên cặp *số + nhãn*, cấm tự suy ra số mới | Ghi file ngay sau mỗi tài liệu, không giữ nháp trong context |

**Kết quả probe**: ⏳ *chưa chạy* → ghi vào `brief.md` mục *Kết quả probe* khi có.

## Ràng buộc bắt buộc cho mọi dispatch writer

1. **RULE-001** — đúng thư mục, đúng naming convention, frontmatter đủ `id / type / status / created`.
2. **Standard markdown link relative path** `[Text](./path.md)`. **Cấm wiki-link `[[...]]`** (RULE-001 quy tắc #5).
3. ⚠️ **`Roadmap.md` và `OKRs.md` là SỬA, không phải TẠO.** Hai file đã tồn tại với `id: ROADMAP-001` / `id: OKRS-001`, `created: 2026-02-04`.
   → **Giữ nguyên `id` và `created`. Thêm `updated: 2026-08-23`.** Writer nào ghi đè frontmatter mới là **lỗi im lặng** — verify phải kiểm riêng điểm này.
4. **Không chạm `*-MOC.md` và `docs/000-Index.md`** — PM giữ.
5. **Mọi con số dùng chung phải copy từ bảng canonical facts của `outline.md`, kèm nguyên nhãn caveat của nó.** Cấm tự tính ra số mới từ số đã có nhãn "ước lượng" mà không mang nhãn theo — đây là failure mode E2 của run trước.
6. **Không bịa số liệu, ngày tháng, tên người, quyết định lịch sử.** Không có nguồn → ghi `TBD` và báo `PARTIAL`.
7. Tiếng Việt, technical term giữ nguyên tiếng Anh (`.claude/rules/create-file-markdown.md`).

## Artifact sẽ tạo/sửa ngoài run-state

| Đường dẫn | Tạo/Sửa | Mục đích | Hạng mục |
|---|---|---|---|
| `docs/000-Index.md` | **Tạo** | RULE-001 ghi "BẮT BUỘC phải có", hiện không tồn tại; `Resources-MOC.md` đang trỏ tới nó ⇒ link chết | #6 |
| `docs/010-Planning/Charter-Comic-Studio.md` | Tạo | Mục tiêu, phạm vi, RACI, constraints | #1 |
| `docs/010-Planning/Roadmap.md` | **Sửa** (stub → nội dung) | Lộ trình 09/2026 → 02/2027 | #2 |
| `docs/010-Planning/OKRs.md` | **Sửa** (stub → nội dung) | Q4/2026 + preview Q1/2027 | #3 |
| `docs/010-Planning/Risk-Register.md` | Tạo | Rủi ro + mitigation | #4 |
| `docs/010-Planning/MVP-Scope.md` | Tạo | Ranh giới MVP vs Full Scope, Go/No-Go | #5 |
| `docs/050-Research/Analysis-Market-Competitor-Landscape.md` | Tạo | Thị trường & đối thủ | #7 |
| ~20 thư mục Dewey + `.gitkeep` | Tạo | Cấu trúc bắt buộc RULE-001 | #6 |
| `docs/010-Planning/Planning-MOC.md` | Sửa | Đăng ký 5 tài liệu mới | close-step |
| `docs/050-Research/Research-MOC.md` | Sửa | Đăng ký Research Notes | close-step |
| `docs/999-Resources/Resources-MOC.md` | Sửa | Link `000-Index.md` hết chết sau khi tạo file | close-step |
| `docs/999-Resources/Glossary.md` | Sửa | Bổ sung term planning/business nếu phát sinh | close-step |

> **`.gitkeep` là bắt buộc** — git không track thư mục rỗng; thiếu nó thì toàn bộ hạng mục #6 biến mất khỏi commit.

## Bảng đích tài liệu (tra Document Type Mapping — RULE-001)

| # | Loại tài liệu | Có trong Mapping? | Thư mục đích | Tên file | `type` | `status` đích |
|---|---|---|---|---|---|---|
| 1 | Project Charter | ✅ `Charter-{ProjectName}.md` | `docs/010-Planning/` | `Charter-Comic-Studio.md` | `charter` | `draft` |
| 2 | Roadmap | ✅ `Roadmap.md` | `docs/010-Planning/` | `Roadmap.md` | `roadmap` | `draft` |
| 3 | OKRs | ✅ `OKRs.md` | `docs/010-Planning/` | `OKRs.md` | `okrs` | `draft` |
| 4 | Risk Register | ✅ `Risk-Register.md` | `docs/010-Planning/` | `Risk-Register.md` | `risk-register` | `draft` |
| 5 | **MVP Scope** | ❌ **KHÔNG có** | `docs/010-Planning/` | `MVP-Scope.md` | `mvp-scope` | `draft` |
| 6 | Index | ✅ (Cấu trúc bắt buộc) | `docs/` | `000-Index.md` | `index` | `live` |
| 7 | Research / Analysis | ✅ `Analysis-{Topic}.md` | `docs/050-Research/` | `Analysis-Market-Competitor-Landscape.md` | `research` | `draft` |

> ⚠️ **Hàng #5 là vấn đề contract** — xem câu hỏi gate Q2 bên dưới. Đường dẫn anh chỉ định (`docs/010-Planning/MVP-Scope.md`) **nằm đúng trong hệ Dewey**, nên không vi phạm guardrail "không tạo thư mục ngoài Dewey". Vấn đề duy nhất là **loại tài liệu chưa được đăng ký** trong bảng Mapping của RULE-001 (`status: approved`).

> **`status: draft` cho cả 5 tài liệu Planning là cố ý.** Run trước kết luận **ba việc phải làm trước dòng code đầu tiên**, trong đó có tư vấn luật sư SHTT. Một Charter `approved` khi ba điều kiện chặn chưa được gỡ là tự tuyên bố sai. Chúng chuyển `approved` khi anh ra quyết định Go/No-Go, không phải khi chúng được viết xong.

## Tóm tắt phân tích (Bước 2)

Chi tiết: [findings/inventory.md](./findings/inventory.md) · [findings/researcher.md](./findings/researcher.md)

1. **Probe thành công — `Write` hoạt động** ⇒ chọn **Biến thể 1**, dispatch writer thật. Tránh lặp lại tỉ lệ 79% output token của PM ở run trước.
2. **32 thư mục Dewey còn thiếu** + `docs/000-Index.md` chưa tồn tại. 25/31 link nội bộ trong MOC đang chết, **17 trong đó tự lành sau `mkdir`**.
3. **Hai template có khoảng trống chặn**: `Template-Project-Charter.md` **không có bảng RACI**; `Template-Risk-Register.md` có cột `Score` **không có công thức được định nghĩa ở bất kỳ đâu**. Không có khuôn nào cho Roadmap / OKRs / MVP-Scope ⇒ `outline.md` là contract cấu trúc duy nhất.
4. ⭐⭐ **TAM $14B là con số SAI để trích vào Charter.** SAM (công cụ cho tác giả) ước **$0,4–9M ARR** `[EM]`; **SOM năm 1 ≈ $4–14K ARR** `[EM]`, neo vào Anifusion — solo founder, **$833 MRR sau ~2 năm**. TAM webtoon đo **tiêu thụ nội dung**, comic-studio không lấy tiền từ độc giả.
5. ⭐⭐ **Khuyến nghị pricing của run trước bị điều chỉnh một nấc, không bị lật.** Cấu hình hybrid mà run trước giả định (*free = platform key, tier cao = BYOK*) **không tồn tại trong ngành**. Comp thật là **Novelcrafter** `[OFF]`: 220K tác giả, tier $4 **không có AI**, BYOK từ $8, nền tảng **không bao giờ bán inference**. Ngưỡng hòa vốn **~125 ảnh/tháng** chia đúng hai loại user của comic-studio.
6. **Hai rủi ro mới run trước bỏ sót**: **GlobalComix** ($13M, mua INKR, đội AI **typesetting**, định vị *"Figma for comics"*) và **Constella của WEBTOON** (rủi ro **nền tảng**, không phải đối thủ).
7. **23% GRR xác minh được tới nguồn gốc** (ChartMogul, ~3.500 công ty, dữ liệu 2025, lọc ≥$250K ARR) + dataset độc lập RevenueCat xác nhận cùng chiều. **Ba caveat bắt buộc đi kèm** mỗi lần trích.

### Mâu thuẫn chưa phân xử được — đẩy vào tài liệu dưới dạng khoảng trống, không phân xử ngầm

- **Anifusion**: run trước ghi `$9/mo`, delta ghi `€20/mo`; và `$833 MRR` vs `$5.000/tháng`. Cả hai đều `[TC]`, không nguồn nào chính chủ. ⇒ Research Notes ghi **cả hai kèm nhãn mâu thuẫn**, không chọn một rồi trình bày như sự thật.
- **"Credit pack né được 23% GRR"** (luận điểm run trước) — delta xác nhận **không có bằng chứng nào**. Nó là **lập luận logic, không phải số đo**. Mọi tài liệu phải ghi đúng như vậy.

## Gate

- **Trình ngày**: 2026-08-23 — một lượt `AskUserQuestion`, 3 câu
- **Kết quả**: ✅ **Duyệt như plan**, không điều chỉnh

| Câu | Đáp án của anh |
|---|---|
| Duyệt run plan (T3, 8 lô, 5 writer song song + PM giữ MOC/Index)? | **Duyệt như plan** — chạy đủ 7 artifact |
| Mô hình kinh doanh baseline? | ⭐ **Cấu hình 3 tầng kiểu Novelcrafter** — tier $4–8 **không có image gen** làm cửa vào → credit pack không hết hạn cho user thường (<125 ảnh/tháng) → **BYOK mở khóa** cho power user |
| `MVP-Scope` vs Document Type Mapping? | ⭐ **Bổ sung 1 hàng vào RULE-001** (additive), bump `updated` |

### Hệ quả của đáp án gate

1. **Pricing đã chốt ⇒ không còn biến chặn Bước 5.** Cả 5 tài liệu Planning dùng chung một baseline. Con số đi kèm bắt buộc: ngưỡng phân tuyến **125 ảnh/tháng**, tier không-AI **$4–8**, và **BYOK là tùy chọn mở khóa, không phải điều kiện để dùng sản phẩm**.
2. **RULE-001 sẽ được sửa ở close-step**, không sửa trước — writer không đụng tới nó. Đây là thay đổi **additive** duy nhất được phép trong run này: thêm đúng một hàng vào bảng Mapping, không đổi naming convention nào, không đổi cấu trúc thư mục nào.
3. **Không escalation nào phát sinh tại gate** ⇒ chưa tạo `escalations.md`.
