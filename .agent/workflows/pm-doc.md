---
description: PM tiếp nhận yêu cầu tài liệu (viết mới hoặc chuẩn hóa kho docs), triage ra tier, điều phối specialist agent với đúng một gate phê duyệt
---

Điều phối một yêu cầu **về tài liệu** đi hết 6 bước (thêm bước đăng ký MOC khi đóng); BẠN giữ vai Product Manager và dispatch specialist agent.

> [!IMPORTANT]
> **Bước 0 — nạp `.agent/workflows/pm-core.md` trước khi làm bất cứ việc gì.** File này chỉ định nghĩa phần **riêng của lane tài liệu**.
> Contract của lane là **RULE-001** `knowledge-base/99-Templates/Documents-Template.md` — PM chỉ đọc hai mục *Document Type Mapping* và *Required Folder Structure* tại Bước 3 (định đích cho từng tài liệu); writer tự đọc đủ RULE-001 khi được dispatch (T0: PM là writer nên đọc đủ). Không nạp cả file ở Bước 0, không dán nội dung nó vào prompt.
> `pm-orca.md` và `pm-evidence.md` chỉ đọc khi cần.

**Input**: đối số sau `/pm-doc` là yêu cầu (văn xuôi tự do). Trống → **AskUserQuestion** (câu hỏi mở): *"Yêu cầu tài liệu của anh là gì? Viết mới hay chuẩn hóa cái đang có?"* Không đoán.

**Sai lane?** Yêu cầu thực chất là thay đổi source code → `/pm-code`. Viết tài liệu *mô tả* code vẫn thuộc lane này; sửa code cho khớp tài liệu thì không.

---

## Hai shape của yêu cầu

Xác định shape **tại Bước 1**, trước khi chấm triage.

| | **Shape A — Authoring** | **Shape B — Normalization sweep** |
|---|---|---|
| Dấu hiệu | "viết PRD…", "soạn runbook…", "làm user guide…" | "chuẩn hóa docs…", "rà lại…", "thống nhất thuật ngữ…" |
| Bản chất | Tạo mới 1 hoặc vài tài liệu | Sửa hàng loạt tài liệu đã có |
| Việc đặc thù | Tra Document Type Mapping → chọn đích + template | **Phase inventory bắt buộc** trước khi plan |
| Rủi ro chính | Sai thư mục, thiếu frontmatter, không link MOC | Sửa nửa vời → kho docs tự mâu thuẫn |

Yêu cầu lai (viết mới + dọn cái cũ) → **Shape B**, phần viết mới là một hạng mục của sweep.

---

## Bước 1 — Intake & Triage

1. `run-id` = `$(date +%F)-<slug-kebab-case>`. Tạo `brief.md` theo schema README, ghi `Lane: doc` và `Shape: A | B` kèm lý do.
2. Chấm triage lane doc (Q4 là tie-breaker — `pm-core.md`; **ngoại lệ: Shape B luôn tính điểm Q4**, vì sweep tự thân đã cross-cutting):

   | # | Câu hỏi |
   |---|---|
   | Q1 | Chạm nhiều hơn một tầng tài liệu (Planning / Requirements / Stories / Specs / QA / Design / Research / Manuals / Deployment / Operations / Marketing)? |
   | Q2 | Sửa tài liệu `status: approved`, hoặc đổi taxonomy / naming / template dùng chung? (= "đổi contract" của lane này) |
   | Q3 | Mơ hồ — chưa rõ độc giả đích, phạm vi, hoặc thế nào là "xong"? |
   | Q4 | Vượt 5 file hoặc 1 ngày công? |

3. Đường đi theo tier. **Trần spawn là số bắt buộc trình ở GATE; vượt nó là escalation** (ghi `escalations.md` + báo anh *trước* khi dispatch):

   | Tier | Đường đi | Trần spawn cả run |
   |---|---|---|
   | **T0** | PM tự viết/sửa. Bỏ Bước 2, 4. Vẫn làm Bước 6 close-step. | **0** |
   | **T1** | 1 writer + 1 verify pass judgment. Bỏ Bước 2, vẫn viết `outline.md`. | **2** (3 nếu có fix round) |
   | **T2** | Analysis/inventory fan-out → soạn thảo → 2 verify pass judgment. | **≤7** (kể cả fix + re-verify) |
   | **T3** | Như T2 + nhiều writer song song + ≤3 verify pass + cập nhật `000-Index.md` + rà toàn bộ MOC liên quan. | **≤12** |

   PM pre-check nhóm máy móc (Bước 6.0) là `grep` của PM — **không tính vào trần spawn**.

## Bước 2 — Analysis / Inventory fan-out (T2, T3)

Theo khung chung trong `pm-core.md`, cộng:

- **Shape B — inventory bắt buộc, chạy trước mọi lens khác.** Dispatch `context-auditor` liệt kê: đường dẫn từng file trong phạm vi, `id`/`type`/`status`/`updated`, MOC nào trỏ tới, link chết, nội dung trùng, thuật ngữ lệch. Nó **tự ghi** `findings/inventory.md` — bảng dài hàng trăm dòng, PM không chép lại.
- Lens của lane doc:

| Tín hiệu trong yêu cầu | Agent |
|---|---|
| Kho hiện có: link chết, trùng lặp, orphan, lệch thuật ngữ | `context-auditor` |
| Nghiệp vụ, user story, AC, PRD/BRD/SRS | `business-analyst` |
| ADR, SDD, API spec, DB schema, tích hợp | `architect` |
| Design system, user flow, wireframe spec | `product-designer` |
| Dữ liệu ngoài: đối thủ, thị trường, công nghệ | `researcher` |
| Test plan, test case, tài liệu QA | `quality-assurance` |
| Runbook, deploy guide, release notes, SLA | `devops-engineer` |
| Threat model, security spec, tuân thủ | `security-auditor` |

## Bước 3 — GATE

Theo `pm-core.md` §GATE, cộng bốn mục riêng:

- **Bảng đích tài liệu**: mỗi hạng mục `loại → thư mục đích → tên file`, tra từ Document Type Mapping của RULE-001. Không tự chế đường dẫn.
- **Ownership**: **mọi `*-MOC.md` và `docs/000-Index.md` thuộc PM**, không cấp cho worker nào — đó là điểm hội tụ của mọi writer. Writer chỉ sở hữu file nội dung của mình.
- **`Độ dài đích` + `Mức neo code` từng hạng mục**, kèm câu trích nguyên văn yêu cầu mức chi tiết của anh mà hai con số đó suy ra từ. Đây là hai đòn bẩy chi phí lớn nhất của lane doc — anh phải thấy chúng *trước* khi duyệt.
- **Ước lượng token** theo `pm-core.md` §GATE với hệ số **0.25M/call**:

  ```
  Ước lượng: Σ(ngân sách lô) × 0.25M = <N>M ≈ <X>% session 5h
  Trần spawn tier <T>: <n> · Dự phòng: 1 fix round (20 call = 5M)
  ```

## Bước 4 — Doc plan (T1–T3)

Thay cho `/opsx-ff` bên lane code. Viết `docs/010-Planning/pm-runs/<run-id>/outline.md`:

```markdown
# Doc Plan: <run-id>

## Hạng mục
| # | Tài liệu | Loại (RULE-001) | Đích | Template | Trạng thái đích | Writer | Độ dài đích | Xong |
|---|----------|-----------------|------|----------|-----------------|--------|-------------|------|

## Outline từng tài liệu
### <tài liệu 1>
- **Độc giả đích**: <ai đọc, để làm gì>
- **Cấu trúc**: <heading cấp 1-2>
- **Nguồn sự thật**: <file/code/finding là căn cứ — writer không được bịa>
- **Độ dài đích**: <N dòng ±15%> — suy từ mức chi tiết anh yêu cầu, KHÔNG từ tiền lệ
- **Mức neo code**: neo file (mặc định) | neo dòng cho điểm phải sửa | neo dòng toàn bộ
- **Tiêu chí xong**: <đo được, tối đa 8 gạch đầu dòng>

## Link phải tạo
| Từ | Tới (relative path) | Quan hệ (RULE-001 §Linking Rules) |

## MOC cần cập nhật
| MOC | Mục thêm/sửa |
```

- `outline.md` do **PM độc quyền chỉnh sửa** — writer báo trong `SUMMARY`, PM tick sau khi đối chiếu `FILES_TOUCHED`.
- **Mỗi tài liệu phải có *Nguồn sự thật*.** Prose sai không có compiler bắt — nó trôi thẳng vào kho tri thức.
- **T3**: thêm mục *Ripple* — tài liệu nào đang trích dẫn phạm vi này và sẽ lệch sau khi sửa.

#### `Độ dài đích` — hiệu chuẩn từ yêu cầu của anh, không từ tiền lệ

| Mức chi tiết anh yêu cầu | Một chức năng nhỏ | Một module / epic |
|---|---|---|
| "đủ để xây dựng, không cần chi tiết" | **150–250 dòng** | 300–400 dòng |
| không nói gì (mặc định) | 200–300 dòng | 400–500 dòng |
| "chi tiết", "đầy đủ mọi trường hợp" | 350–500 dòng | 600+ dòng, **cắt thành nhiều tài liệu** |

- Writer **viết đúng target ngay từ đầu — cấm viết dài rồi cắt** (nêu thẳng trong `[TASK]`). Vượt >15% mà chưa xong → `PARTIAL` + handoff note, không tự nới; target sai là lỗi của PM, PM sửa `outline.md` rồi dispatch tiếp.
- Độ dài là **biến nhân của cả run**: doc dài hơn → verify surface lớn hơn → nhiều finding hơn → fix round to hơn.

#### `Mức neo code` — mặc định là neo file

Áp cho mọi tài liệu có khẳng định về code hiện có.

| Mức | Writer ghi gì | Khi nào |
|---|---|---|
| **`neo file`** (mặc định) | `path/to/file.ts` + tên symbol. **Không** xác minh số dòng. | Mọi tài liệu, trừ khi anh yêu cầu khác |
| `neo dòng cho điểm phải sửa` | Neo dòng chỉ cho vị trí SE **bắt buộc phải sửa**; bối cảnh dùng neo file | Anh yêu cầu rõ, hoặc tài liệu là hướng dẫn thi hành từng bước |
| `neo dòng toàn bộ` | `file.ts:120-135` cho mọi khẳng định | Chỉ khi anh chốt tại gate và chấp nhận giá |

- Xác minh `file:line` biến doc writer thành code worker, rồi verify trả tiền lần hai cho cùng việc. Neo file giảm ~40% call của writer và xoá phần lớn surface của pass Correctness.
- Tài liệu neo file ghi một dòng ở đầu mục kỹ thuật: *"Đường dẫn là neo file; số dòng đổi theo thời gian, định vị bằng tên symbol."*
- Không xác minh được ở mức đã chọn → `TBD` + `PARTIAL`. **Không bịa neo.**

## Bước 5 — Soạn thảo

**T0**: PM tự viết trong scope đã duyệt, rồi sang Bước 6.

**T1–T3**: dispatch writer theo cột *Writer* của `outline.md`:

1. **Một dispatch = một tài liệu** (Shape A) hoặc **một lô ≈3–5 file** (Shape B). Không giao cả `outline.md` hay cả sweep cho một writer. Số tài liệu dùng để *cắt*; **trần tool call** bên dưới mới *chặn*:

   #### Trần lane doc — KHÔNG dùng con số 60 của lane code

   | Loại lô | Trần | Ghi chú |
   |---|---|---|
   | **Writer** — một tài liệu, `neo file` | **30** | +10 nếu `neo dòng cho điểm phải sửa`; +20 nếu `neo dòng toàn bộ` |
   | **Writer** — một lô 3–5 file sweep (Shape B) | **35** | Sửa tại chỗ, không sáng tác |
   | **Verify** — một pass | **20** | Không phụ thuộc tier |
   | **Fix round** | **20** | Chỉ mục `CRITICAL` |
   | **Inventory** (Shape B, Bước 2) | **35** | Việc là `Glob`/`Grep`, không đọc sâu |

   Trần thấp đi kèm hai thứ làm việc nhỏ lại thật: `Độ dài đích` và `neo file`. Cắt trần mà không cắt hai thứ kia thì writer chỉ trả `PARTIAL` liên tục.
2. Trích **toàn văn outline của đúng tài liệu / lô đó** vào `[TASK]` — không đưa đường dẫn `outline.md`, không đưa outline hạng mục khác.
3. Dispatch theo ownership map đã duyệt. Tuần tự là mặc định (xong lô → PM tick → writer MỚI); song song chỉ khi ownership rời nhau. Shape B cắt theo **file hoặc thư mục con**, không cắt theo "chủ đề" vì chủ đề chồng lấn file.
4. **Ràng buộc bắt buộc trong mọi prompt writer** — đây là nhóm tiêu chí máy móc của Bước 6 dịch thành rule đầu vào; nêu đủ, vì không còn pass verify nào soát chúng:
   - Tuân thủ **RULE-001**: đúng thư mục, naming convention, frontmatter đủ `id / type / status / created`. Sửa file đã có → **bump `updated: <YYYY-MM-DD>`**.
   - **Link chuẩn markdown + relative path** `[Tên](../020-Requirements/PRD-X.md)`. RULE-001 **cấm wiki-link `[[...]]`** — tài liệu cũ còn dùng là tiền lệ sai, không copy.
   - **Không chạm `*-MOC.md` hay `000-Index.md`** — PM giữ.
   - **`Độ dài đích: <N> dòng ±15%`** — viết đúng target ngay, cấm viết dài rồi cắt. **`Mức neo code: <mức>`** theo `outline.md`.
   - Không bịa số liệu, ngày tháng, tên người, quyết định lịch sử. Không có nguồn → `TBD` + `PARTIAL`.
   - **Tự soát trước khi trả về, ghi kết quả trong `SUMMARY`**: `wc -l` trong target ±15% · frontmatter đủ 4 field · không còn dấu vết tool-call (`</content>`, `</invoke>`, `<invoke`) hay markdown hỏng cuối file · mọi link tương đối trỏ tới file có thật.
5. Worker trả về → đối chiếu `FILES_TOUCHED` với ownership → tick `outline.md`.

## Bước 6 — Verification & Close

Tài liệu viết xong mà không ai trỏ tới thì coi như không tồn tại.

1. **Verify — agent KHÁC agent đã viết**, mặc định `context-auditor`. Tiêu chí chia theo thứ *quyết định được bằng `grep`* và thứ *không*:

   **Nhóm máy móc — KHÔNG dispatch agent.** Completeness (đủ hạng mục, frontmatter đủ, `updated` đã bump, độ dài trong target ±15%) · Connectivity (link phân giải được, không orphan) · Correctness **tầng neo** (file/symbol được trỏ tới có tồn tại) · Hygiene (không dấu vết tool-call, không markdown hỏng).

   **Nhóm judgment — đáng trả tiền cho agent.** Correctness **tầng nội dung** (khẳng định có khớp *logic* của Nguồn sự thật không — neo trả lời "chỗ đó có tồn tại?", nội dung trả lời "điều tài liệu nói về nó có đúng?") · Coherence (không mâu thuẫn tài liệu liền kề, không trùng nội dung đã có, thuật ngữ nhất quán; `docs/999-Resources/Glossary.md` còn là stub nên không đủ làm chuẩn — thuật ngữ mới đáng chuẩn hóa thì đề xuất bổ sung Glossary như một hạng mục).

   #### Verify theo tier — nhóm máy móc KHÔNG BAO GIỜ được dispatch

   **Bước 6.0 — PM pre-check, bắt buộc mọi tier, ~2–3 tool call, 0 spawn**, chạy trước mọi pass:

   ```bash
   grep -c "^id:\|^type:\|^status:\|^created:" <file>        # frontmatter đủ 4 field
   grep -n "</content>\|</invoke>\|<invoke\|^</" <file>       # residue tool-call (kỳ vọng: rỗng)
   grep -o "](\.\.*/[^)]*\.md)" <file> | ...                  # link target có tồn tại
   wc -l <file>                                              # trong Độ dài đích ±15%
   ```

   | Tier | Nhóm máy móc | Nhóm judgment | Spawn | Trần |
   |---|---|---|---|---|
   | **T0** | PM pre-check | PM tự đọc (tài liệu nhỏ: đọc một lần rẻ hơn một spawn + một verdict) | **0** | — |
   | **T1** | PM pre-check | **Đúng MỘT dispatch**: Correctness-nội-dung + Coherence → `verdict.md` | **1** | 20 |
   | **T2** | PM pre-check | **2 pass** song song: Correctness-nội-dung ∥ Coherence | 2 | 20 mỗi pass |
   | **T3** | PM pre-check | ≤**3 pass**: cắt theo tầng tài liệu hoặc nhóm khẳng định, `verdict-<pass>.md` | ≤3 | 20 mỗi pass |

   - **Pass judgment chạy `model: opus`** — ghi vào cột `Model` của `run-plan.md`. Default `sonnet` của `context-auditor` là cho inventory và audit máy móc, không cho Correctness-nội-dung / Coherence. Inventory (Bước 2) giữ `sonnet` hoặc `haiku`.
   - Rule ở prompt writer *giảm* lỗi máy móc, pre-check bắt phần còn lại — cần cả hai, bỏ một là để rác trôi vào kho tri thức.
   - Thêm `quality-assurance` **chỉ khi** có acceptance criteria kiểm chứng được (test plan, test case) — tính là một pass nữa trong bảng.
   - Đây là carve-out khỏi *Verify cũng phải cắt lô* của `pm-core.md`: cắt pass áp từ T2; **ngân sách thì không có carve-out**.
   - **Verdict mở đầu bằng bảng tóm tắt ≤20 dòng**, thân ≤150 dòng mỗi pass. Nêu trong `[TASK]`.

2. `verdict.md` — T2/T3 PM tổng hợp từ các `verdict-<pass>.md`.

3. **Fix round — trần MỘT vòng, chỉ `CRITICAL`.**

   | Mức | Xử lý |
   |---|---|
   | `CRITICAL` — khẳng định sai/bịa, link chết, sai thư mục, thiếu frontmatter, thiếu hạng mục đã duyệt | Fix round 1 |
   | `WARNING`, `SUGGESTION` — diễn đạt, thứ tự mục, chỗ có thể chi tiết hơn | **Ghi `verdict.md` làm nợ + báo anh. KHÔNG dispatch.** |

   - Một dispatch, worker MỚI, trần **20 call**, prompt chứa **chỉ các mục `CRITICAL`** — không dán cả verdict, không dán pass khác. Không tự vá rồi tuyên bố xong.
   - Re-verify **chỉ các mục đã sửa**: **T0/T1 PM tự làm, 0 spawn** (PM không viết bản fix nên vẫn độc lập); **T2/T3 một dispatch, trần 10 call**.
   - Còn `CRITICAL` sau vòng 1 → **dừng, AskUserQuestion**: còn lỗi gì, chi phí một vòng nữa, lựa chọn giao kèm nợ. **Không tự chạy vòng 2.**

4. **Close-step — PM tự làm, bắt buộc mọi tier** (tương đương `/opsx-archive`):
   - Cập nhật **MOC của thư mục cha** cho từng tài liệu mới/đổi tên; `docs/000-Index.md` nếu là tài liệu lớn (PRD, SDD, MTP, Roadmap).
   - Tài liệu bị thay thế → chuyển `docs/090-Archive/` + `status: deprecated`, **không xóa**. Thư mục chưa tồn tại thì tạo theo RULE-001.
   - Chạy *Validation Checklist* của RULE-001 lần cuối trên toàn danh sách.

5. `cost.md` theo `pm-core.md`, rồi báo cáo theo mục *Output*, kèm: MOC đã cập nhật; **`WARNING`/`SUGGESTION` chưa xử** (nợ có chủ ý của trần một fix round); **ước lượng token ở gate vs thực tế** và **`Độ dài đích` vs độ dài thật** — lệch >50% thì ghi lý do vào `cost.md` và cập nhật hệ số ở `pm-evidence.md`.

---

## Guardrails riêng lane doc

- **Không bê trần 60 của lane code sang đây**; không cắt verify thành nhiều pass ở T0/T1; không dispatch agent cho nhóm máy móc; không gộp hai tầng Correctness; không đặt `Độ dài đích` bằng tiền lệ; không để writer xác minh `file:line` khi mức là `neo file`.
- **Trần một fix round, chỉ `CRITICAL`.** Cần vòng hai → AskUserQuestion.
- **Không tạo thư mục top-level ngoài hệ Dewey của RULE-001.** Không có chỗ cho tài liệu → hỏi anh.
- **Không xóa tài liệu.** Lỗi thời → `status: deprecated` + `090-Archive/`.
- **Không sửa run-state của run cũ** trong `pm-runs/`. Sweep Shape B loại thư mục này khỏi phạm vi ngay tại gate.
- **MOC và `000-Index.md` không bao giờ cấp cho worker.**
- **Không coi "đã viết xong file" là xong.** Chưa đăng ký MOC thì run chưa đóng.
- **Shape B: không sửa nửa vời.** Không đủ sức làm hết → cắt scope **tại gate**, không cắt ngầm giữa chừng.
