# Brief: 2026-08-23-khoi-tao-tai-lieu-planning-comic-studio

## Yêu cầu gốc

> Dựa trên các thông tin đã đánh giá ở run 2026-08-23-danh-gia-y-tuong-comic-studio, em hãy điều phối nhân thủ để phân tích, xác định yêu cầu và khởi tạo các tài liệu dưới đây
>
> | # | Artifact | Đường dẫn SSOT | Mô tả |
> |:--|:---------|:---------------|:------|
> | 1 | **Project Charter** | `docs/010-Planning/Charter-{Project}.md` | Mục tiêu, phạm vi, Stakeholder Matrix (RACI), constraints |
> | 2 | **Product Roadmap** | `docs/010-Planning/Roadmap.md` | Lộ trình phát triển tổng thể (3-6 tháng) |
> | 3 | **OKRs** | `docs/010-Planning/OKRs.md` | Mục tiêu & Kết quả then chốt |
> | 4 | **Risk Register** | `docs/010-Planning/Risk-Register.md` | Danh sách rủi ro và kế hoạch giảm thiểu |
> | 5 | **MVP Scope** | `docs/010-Planning/MVP-Scope.md` | Ranh giới MVP vs Full Scope, Go/No-Go Decision |
> | 6 | **Cấu trúc thư mục** | `docs/` (toàn bộ Dewey) | Khởi tạo cấu trúc docs/ theo Documents-Template |
> | 7 | **Research Notes** _(Researcher)_ | `docs/050-Research/Analysis-{Topic}.md` | Kết quả nghiên cứu đối thủ, thị trường |

**Lane**: doc

**Shape**: **A (authoring)** — tạo mới 6 tài liệu nội dung + khởi tạo scaffolding thư mục.

Lý do **không** phải Shape B, dù thoạt nhìn hạng mục #6 giống "dọn kho docs": Shape B là **sửa hàng loạt tài liệu đã tồn tại** cho khớp một quy ước. Ở đây **không tài liệu nội dung nào bị viết lại**. Hai file `Roadmap.md` và `OKRs.md` tuy đã tồn tại nhưng đang là **stub 10 dòng** (`*(Content to be added)*`) — điền nội dung vào stub là *authoring*, không phải *normalization*. Hạng mục #6 là **tạo thư mục rỗng** theo cấu trúc bắt buộc của RULE-001, không đụng nội dung file nào.

> Nợ kỹ thuật kho docs (MOC rỗng, link chết trong `Resources-MOC.md`) **đã được ghi nhận từ run trước** và vẫn thuộc một run Shape B riêng. Xem mục *Ngoài scope* bên dưới.

## Nguồn sự thật của run này

| Nguồn | Vai trò |
|---|---|
| [Analysis-Comic-Studio-Concept.md](../../../050-Research/Analysis-Comic-Studio-Concept.md) (1.148 dòng) | Deliverable chính của run trước — 4 verdict, 9 điều kiện khả thi, 7 vấn đề phải sửa, lộ trình MVP0–3, unit economics |
| `pm-runs/2026-08-23-danh-gia-y-tuong-comic-studio/findings/*.md` (5 file, 2.532 dòng) | Findings thô của 4 lens — hiệu ứng, effort %, số liệu benchmark |
| `pm-runs/2026-08-23-danh-gia-y-tuong-comic-studio/escalations.md` | **E1** (đáp án gate: SaaS thương mại, user tự upload, 1 dev) và **E2** (N=3, chi phí $12,06/chapter) |
| [Request.md](../../../999-Resources/Request.md) (894 dòng) | Concept gốc — kiến trúc 18 mục |
| `knowledge-base/99-Templates/Documents-Template.md` (RULE-001) | Contract của lane doc |
| `docs/999-Resources/Templates/Template-Project-Charter.md`, `Template-Risk-Register.md` | Khuôn có sẵn cho hạng mục #1 và #4 |

## Bối cảnh đã chốt từ run trước (KHÔNG hỏi lại)

Ba câu này anh đã trả lời tại gate của run trước; chúng là tiền đề bất biến của mọi tài liệu trong run này:

| | |
|---|---|
| **Bản chất sản phẩm** | **SaaS thương mại multi-tenant** — nền tảng cho **người khác tự upload truyện của họ** |
| **Quy mô đội** | **1 mình anh + AI assist** |
| **Rủi ro IP đầu vào** | Chuyển sang người upload; nền tảng phát sinh nghĩa vụ safe harbour + TDM thương mại |

## Triage

| # | Câu hỏi | Đáp án | Lý do |
|---|---------|--------|-------|
| Q1 | Chạm > 1 tầng tài liệu? | **Có** | Ba tầng tối thiểu: **010-Planning** (5 tài liệu: Charter, Roadmap, OKRs, Risk-Register, MVP-Scope), **050-Research** (Research Notes), và **toàn bộ hệ Dewey** (`docs/000-Index.md` chưa tồn tại + 11 MOC + ~20 thư mục còn thiếu). Hạng mục #6 tự thân đã chạm mọi tầng. |
| Q2 | Sửa doc `approved` / đổi taxonomy? | **Có** | **`MVP-Scope.md` KHÔNG có trong bảng Document Type Mapping của RULE-001** (`status: approved`). RULE-001 quy tắc #7 cấm tạo tài liệu mà chưa tra bảng — đã tra, không có. Tạo nó là **mở rộng taxonomy**; đăng ký chính thức là **sửa một tài liệu approved**. Quyết định này đưa lên GATE. |
| Q3 | Mơ hồ — chưa rõ độc giả đích / phạm vi / "xong"? | **Không** | Yêu cầu nêu đích danh 7 artifact kèm **đường dẫn SSOT** và mô tả nội dung từng cái. Nguồn sự thật rõ (run trước). Độc giả đích rõ: anh — người ra quyết định build/không build. Các biến còn lại (horizon roadmap, chu kỳ OKR) là **judgment call thường quy**, xử bằng assumption A1–A2 chứ không cần hỏi. |
| Q4 | > 5 file hoặc > 1 ngày công? | **Có** (có tính điểm, vì Q1 = Có) | 6 tài liệu nội dung + `000-Index.md` + ~20 thư mục + ≥3 MOC phải cập nhật + Glossary. Vượt xa trần 5 file. |

**Điểm**: **3/4** → **Tier**: **T3**

**Chọn tier thấp do phân vân**: **Không.**
Có cân nhắc T2: nếu quyết định *không* đăng ký `MVP-Scope` vào RULE-001 mà chỉ đặt file theo đường dẫn anh chỉ định, Q2 rơi về Không → 2/4 → T2. Nhưng hình dạng công việc vẫn là T3 bất kể Q2: **nhiều writer song song trên các tài liệu ghép chặt** + **bắt buộc tạo `000-Index.md`** + **rà nhiều MOC** — đó chính xác là ba việc đặc thù mà `pm-doc.md` gán cho T3. Chấm T2 rồi vẫn phải làm đủ việc của T3 là tự lừa mình.

## Assumptions

- **A1 — Horizon Roadmap: 09/2026 → 02/2027 (6 tháng), mốc bắt đầu là tuần đầu tháng 09/2026.**
  Căn cứ: yêu cầu ghi "3-6 tháng"; hôm nay 23/08/2026; run trước kết luận **ba việc phải làm trước dòng code đầu tiên** (trong đó có tư vấn luật sư SHTT) nên không thể lấy hôm nay làm mốc khởi công.
  → **Sai thì hỏng ở đâu**: mọi ngày tháng trong Roadmap và OKRs lệch theo. Rẻ để sửa (một bảng), nên không đáng chiếm một câu hỏi gate.

- **A2 — Chu kỳ OKR: Q4/2026 (10–12/2026) là chu kỳ chính, kèm preview Q1/2027.**
  Căn cứ: Q3/2026 chỉ còn ~5 tuần tính từ hôm nay — quá ngắn để làm một chu kỳ OKR có nghĩa. Giai đoạn 09/2026 (MVP0 + pháp lý) được đặt là **pre-cycle**, đo bằng gate chứ không bằng OKR.
  → **Sai thì hỏng ở đâu**: chỉ đổi nhãn chu kỳ, không đổi nội dung Key Result.

- **A3 — Tài liệu viết bằng Tiếng Việt, giữ nguyên technical term.** Căn cứ: `.claude/rules/create-file-markdown.md`.

- **A4 — Độc giả đích là anh (người ra quyết định), thứ cấp là chính các AI agent của TNMCORE-OS ở các run sau.**
  → **Sai thì hỏng ở đâu**: nếu để pitch cho investor, Charter cần thêm mục *Financial projection* và Research Notes cần TAM có phương pháp chặt hơn. Đã cấp cho `researcher` một phần market sizing để phòng trường hợp này.

- **A5 — `{Project}` trong `Charter-{Project}.md` = `Comic-Studio`** → `docs/010-Planning/Charter-Comic-Studio.md`.
  Căn cứ: tên repo `comic-studio`; RULE-001 naming `Charter-{ProjectName}.md` dùng PascalCase-hyphen.

- **A6 — `{Topic}` trong Research Notes = `Market-Competitor-Landscape`** → `docs/050-Research/Analysis-Market-Competitor-Landscape.md`.
  Căn cứ: phải khác `Analysis-Comic-Studio-Concept.md` đã tồn tại; nội dung yêu cầu là "đối thủ, thị trường".

- **A7 — Mô hình kinh doanh (BYOK vs credit-based) CHƯA chốt** — đây là biến chảy vào Charter *constraints*, OKR *key result*, và MVP-Scope *Go/No-Go*. **Đưa lên GATE**, không tự quyết.
  → **Sai thì hỏng ở đâu**: nếu tự chọn sai, cả 5 tài liệu 010-Planning phải viết lại phần kinh tế — đây là lý do nó xứng đáng một câu hỏi gate thay vì một assumption.

## Quyết định contract (PM phân xử ngay tại Bước 1)

- **Xung đột `pm-doc.md` vs `RULE-001` về kiểu link** — giữ nguyên phân xử của run trước: **theo RULE-001**, dùng standard markdown link relative path `[Text](./path.md)`, **KHÔNG** wiki-link `[[...]]`. Lý do: RULE-001 `status: approved`, và chính `pm-doc.md` Bước 0 chỉ định nó là contract của lane.

- **`.agent/roles/` không tồn tại** — giữ nguyên phân xử của run trước: bỏ dòng `[ROLE] Nạp .agent/roles/...`, persona lấy từ agent definition mà tool Agent tự nạp.

- **Guardrail `Write` của subagent** — run trước ghi nhận subagent bị chặn `Write` (*"Subagents should return findings as text, not write report files"*), khiến PM tiêu **79% output token** của cả run. Guardrail này **không nằm trong `settings.json`** (đã grep, 0 hit) ⇒ là hành vi harness, có thể khác ở session này.
  → **Phân xử: PROBE, không giả định.** Dispatch `context-auditor` ở Bước 2 được cấp quyền tự ghi `findings/inventory.md`. File có xuất hiện trên đĩa hay không quyết định biến thể dispatch của Bước 5. Cả hai biến thể được ghi sẵn trong `run-plan.md`; kết quả probe ghi lại tại mục *Kết quả probe* bên dưới.

- **`researcher` không có tool `Write`** (tools: `Read, Glob, Grep, WebFetch, WebSearch`) — điều này **chắc chắn**, không phụ thuộc probe. Nó luôn trả text; PM ghi `findings/researcher.md` một lần duy nhất, writer sau đó tham chiếu **bằng đường dẫn**, không quote lại.

## Kết quả probe Write-block

> Điền sau khi `context-auditor` của Bước 2 trả về.

| | |
|---|---|
| Subagent ghi được file? | ✅ **CÓ.** `context-auditor` tự ghi `findings/inventory.md` — 28.841 bytes, worker tự xác minh bằng `ls -l`. PM không chạm nội dung. |
| Biến thể Bước 5 được chọn | **Biến thể 1 — dispatch writer thật** |
| Ghi chú | Xem mục *Kết luận cuối về guardrail* bên dưới — giả thuyết ban đầu của PM đã bị dữ liệu ở Bước 5 bác bỏ. |

> **Giá trị của việc probe thay vì giả định**: nếu tin theo run trước và chọn Biến thể 2, PM sẽ tự viết cả 6 tài liệu và lặp lại đúng tỉ lệ 79% output token của run trước — trong khi thực tế đường rẻ hơn đang mở.

### Kết luận cuối về guardrail (sửa lại sau Bước 5)

**Giả thuyết ban đầu của PM SAI.** Ngay sau probe, PM ghi giả thuyết: *"harness từ chối ghi ngoài worktree; run này gọi `EnterWorktree` trước mọi dispatch nên subagent thừa hưởng cwd hợp lệ."* Dữ liệu Bước 5 bác bỏ nó.

**Điều thật sự quan sát được** — bốn writer, cùng một worktree, cùng một cách dispatch:

| Writer | File đích | `Write` |
|---|---|---|
| `context-auditor` | `findings/inventory.md` | ✅ ghi được |
| `business-analyst` #1 | `Charter-Comic-Studio.md` | ✅ ghi được |
| `security-auditor` | `Risk-Register.md` | ✅ ghi được |
| `architect` | `MVP-Scope.md`, `Roadmap.md` | ✅ ghi được |
| `business-analyst` #2 | **`Analysis-Market-Competitor-Landscape.md`** | ❌ **BỊ CHẶN 2 lần, deterministic** |

⇒ **Guardrail bám theo MẪU TÊN FILE, không theo worktree và cũng không theo loại agent.** Nó chặn filename trông giống *"report/analysis .md file"* — đúng nghĩa đen của thông báo lỗi run trước (*"Subagents should return findings as text, not write report files"*). Run trước bị chặn ở `business-analyst` viết một tài liệu **Analysis** — cùng một mẫu.

**Hệ quả thực dụng cho các run sau** (đây là thứ đáng giữ, không phải bản thân giả thuyết):

1. **Dispatch writer vẫn là mô hình đúng cho lane doc** — 4/5 writer ghi được bình thường. Kết luận *"PM tự viết, không dispatch writer"* ở `cost.md` run trước là **tổng quát hoá quá mức từ một mẫu**.
2. **Ngoại lệ hẹp và dự đoán được**: tài liệu có tên khớp `Analysis-*` / `*-report.md`. Với những file đó, dispatch writer để **soạn nội dung**, PM ghi file. Chi phí: nội dung đi qua context PM một lần.
3. **Writer đã hành xử đúng khi bị chặn**: không tìm đường lách (không stub-then-Edit, không nhờ agent khác, không dùng Bash để ghi), trả toàn văn kèm báo `BLOCKED`. Ràng buộc chống-lách trong prompt dispatch đã phát huy tác dụng — **giữ nguyên câu đó cho các run sau**.

> **Bài học phương pháp**: PM ghi một giả thuyết nhân quả sau **một** quan sát thành công. Đúng ra phải ghi *"chưa biết vì sao"* — vì một quan sát dương tính không phân biệt được giữa "guardrail đã gỡ" và "guardrail không áp cho trường hợp này". Việc gắn nhãn nó là **giả thuyết chưa đối chứng** ngay từ đầu là thứ đã cứu nó khỏi thành một kết luận sai nằm lại trong run-state.

## Ngoài scope run này

Ghi lại để không mất dấu, **không** tự ý làm:

1. **Dọn nợ kho docs (Shape B)** — 11 MOC rỗng nội dung, 2 link chết trong `Resources-MOC.md` (`../000-Index.md`, `Template-Daily-Report.md`), 13 template có thật không được liệt kê trong MOC nào. Run này **có** tạo `000-Index.md` (vì nó là hạng mục #6 và RULE-001 ghi "BẮT BUỘC phải có"), nhưng **không** viết lại nội dung 11 MOC — chỉ cập nhật MOC của thư mục có tài liệu mới.
2. **`Template-Analysis.md` là stub** — không dùng được làm khuôn. `outline.md` của run này là contract cấu trúc thật.
3. **Nội dung `docs/999-Resources/Templates/`** — không đụng.
4. **Thư mục `Competitor-Analysis/`** được scaffolding tạo ra nhưng **để rỗng** trong run này; tài liệu đối thủ đi vào một file `Analysis-{Topic}.md` duy nhất theo đúng yêu cầu #7.

## Open questions

| # | Câu hỏi | Ai trả lời | Chặn phase nào |
|---|---------|-----------|----------------|
| OQ1 | Mô hình kinh doanh: **BYOK** (khuyến nghị #1 của run trước) hay **credit-based** hay hoãn quyết? | Anh — tại GATE | **Chặn Bước 5** — chảy vào Charter constraints, OKR KR, MVP-Scope Go/No-Go. Không chặn Bước 2. |
| OQ2 | `MVP-Scope` chưa có trong Document Type Mapping. Bổ sung một hàng vào RULE-001 (`approved`) ngay bây giờ, hay chỉ đặt file và ghi nhận khoảng trống? | Anh — tại GATE | Không chặn Bước 2; chặn close-step |
| OQ3 | Duyệt run plan như trình bày? | Anh — tại GATE | Chặn Bước 4 trở đi |

> Cả ba **không** chặn Bước 2. Hai lens của fan-out (inventory kho docs, market sizing) **bất biến** với cả ba câu. Gom đúng một lượt `AskUserQuestion` tại GATE — quan trọng vì run này chạy dưới dạng background job.
