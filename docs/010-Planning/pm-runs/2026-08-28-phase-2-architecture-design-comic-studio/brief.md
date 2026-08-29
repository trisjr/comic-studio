# Brief: 2026-08-28-phase-2-architecture-design-comic-studio

## Yêu cầu gốc

> Điều phối nhân sự thực hiện công việc theo `@/Users/trisjr/Projects/Tenomad/TNMCore-OS/knowledge-base/20-Project/SDLC-Phases/Phase-2-Architecture-Design.md`

**Lane**: doc
**Shape**: A (authoring) — tạo mới bộ tài liệu kiến trúc; `docs/030-Specs/` hiện chỉ có 4 thư mục con rỗng (`.gitkeep`) và một `Specs-MOC.md` **rỗng hoàn toàn**. Không có tài liệu cũ nào để chuẩn hóa, nên đây không phải sweep Shape B.

### Nguồn yêu cầu — trích nguyên văn (file nằm ngoài repo, dán vào đây để worker không phải đọc cross-repo)

`KB-SDLC-P2` — Phase 2: Thiết Kế Kiến Trúc (Architecture Design), `status: approved`.

| Thuộc tính | Chi tiết |
| :--- | :--- |
| Role chính | 🏗️ **Architect** |
| Support | 🛡️ **Security Auditor** (Threat Model) — 🛡️ **DevOps** (infra feasibility) — 🧪 **QA** (testability review) |
| Mục tiêu | Thiết kế kiến trúc hệ thống, chọn tech stack, định nghĩa API & Schema |
| Thư mục tác nghiệp | `docs/030-Specs/` |
| Skills gợi ý | `software-architecture`, `senior-architect`, `database-design`, `senior-backend` |

**Input cần có**: PRD + Use Cases (Phase 1) · NFR nếu có · Constraints về infra, budget, team size · Research Notes (Phase 0).

**Output (Artifacts)**:

| # | Artifact | Đường dẫn SSOT |
| :-- | :--- | :--- |
| 1 | SDD | `docs/030-Specs/Architecture/SDD-{Project}.md` |
| 2 | ADR | `docs/030-Specs/Architecture/ADR-{NNN}-{Title}.md` |
| 3 | Tech Stack ADR | `docs/030-Specs/Architecture/ADR-001-Tech-Stack.md` |
| 4 | API Specs | `docs/030-Specs/API/Endpoint-{Name}.md` |
| 5 | Integration Specs | `docs/030-Specs/API/Spec-Integration-{Name}.md` |
| 6 | DB Schema | `docs/030-Specs/Schema/DB-Entity-{Name}.md` |
| 7 | Security Spec _(Security Auditor)_ | `docs/030-Specs/Security/Spec-Security-{Name}.md` |

> [!IMPORTANT]
> **🛡️ Security Review Gate:** Bắt buộc mời Security Auditor thực hiện Threat Modeling cho kiến trúc trước khi chuyển sang Phase 3. Đây là checkpoint bảo mật đầu tiên.

**Tiêu chí chuyển Phase** (nguyên văn — đây là định nghĩa "xong" của run này):

- [ ] SDD có sơ đồ kiến trúc (Mermaid/Draw.io)
- [ ] Ít nhất 1 ADR cho quyết định tech stack
- [ ] API Specs cover hết các Use Cases chính
- [ ] DB Schema đã normalized và có ER Diagram
- [ ] ✅ **Security Spec đã được Security Auditor review**

### Phạm vi đã chốt với anh (AskUserQuestion, 2026-08-28)

**Toàn bộ MVP — MVP0 (6 stories) + MVP1 (10) + MVP2 (8) = 24 stories.** Loại trừ 19 story còn lại của Full Scope. Kiến trúc vẫn phải chừa đường mở rộng cho phần Full Scope, nhưng không viết spec cho nó ở run này.

---

## Triage

| # | Câu hỏi | Đáp án | Lý do |
|---|---------|--------|-------|
| Q1 | Chạm > 1 tầng tài liệu? | **Có** | Trọng tâm là `030-Specs` (cả 4 thư mục con: Architecture / API / Schema / Security). Ngoài ra gần như chắc chắn phải bổ sung `999-Resources/Glossary.md` — thuật ngữ lõi của kiến trúc này (Comic IR, Timeline State, Visual Prompt Compiler, Canonical Reference) chưa được chuẩn hóa, mà Glossary hiện chỉ là stub. Có thể chạm `020-Requirements/NFR-Comic-Studio.md` nếu BA lens xác nhận SRS chưa bao đủ NFR. **Điều kiện hạ**: nếu BA lens kết luận SRS đã bao đủ NFR *và* không thuật ngữ nào cần chuẩn hóa, Q1 tụt về Không → tier còn 2 điểm. |
| Q2 | Sửa doc `approved`, hoặc đổi taxonomy / naming convention / template dùng chung? | **Không** | Toàn bộ deliverable là tài liệu **mới**. Mọi loại artifact của Phase 2 đều **đã có sẵn hàng** trong Document Type Mapping của RULE-001 (ADR, SDD, Endpoint, Spec-Integration, DB-Entity, Spec-Security, DFD) — không phải thêm hàng, không phải sửa RULE-001. Tài liệu Phase 1 (`PRD`, `SRS`, `UC-*`) chỉ được **đọc**, không sửa. |
| Q3 | Mơ hồ — chưa rõ độc giả đích, phạm vi, hoặc thế nào là "xong"? | **Có** | "Xong" thì rõ (5 tiêu chí chuyển phase ở trên). Nhưng **phạm vi thì không**: bằng chứng là chính việc phải dùng AskUserQuestion ngay Bước 1 để chốt MVP-vs-Full. Còn mơ hồ chưa giải: **độ hạt file** — `Endpoint-*.md` cắt theo resource hay theo từng endpoint, và bao nhiêu `DB-Entity-*.md`. Con số này chỉ có sau khi architect lens enumerate; chốt tại gate. |
| Q4 | > 5 file hoặc > 1 ngày công? | **Có** (tính điểm — hợp lệ vì Q1 = Có) | Ước lượng 15–20 tài liệu cho phạm vi 24 MVP stories, trải trên 4 sub-domain kỹ thuật khác nhau. Vượt xa trần 5 file. |

**Điểm**: 3/4 → **Tier**: T3

**Chọn tier thấp do phân vân**: Không — nhưng đây là chỗ cần nói thẳng. Nếu Q1 tụt về Không (theo điều kiện đã ghi ở trên) thì điểm còn 2 → T2. Em vẫn **đề xuất chạy T3**, và trình lý do nâng tại gate thay vì nhảy tier ngầm:

1. **Phase contract bắt buộc một security review độc lập** ("Security Review Gate") — điều này tự nó loại trừ đường T1/T2-một-writer-tự-kiểm, vì `pm-core.md` cấm verify bởi chính agent đã viết.
2. Bốn sub-domain (Architecture / API / Schema / Security) có ownership rời nhau tự nhiên → fan-out song song là đường rẻ hơn một writer chạy dài (`turns^1.74`).
3. `Specs-MOC.md` rỗng và `000-Index.md` phải cập nhật cho SDD — đúng phần close-step mà T3 mô tả.

---

## Assumptions

- **Đích ghi là repo `comic-studio` này, không phải repo `TNMCore-OS`** — file Phase-2 là knowledge-base *quy trình* dùng chung, cột "Thư mục tác nghiệp" ghi đường dẫn tương đối `docs/030-Specs/`, và toàn bộ Phase 1 (PRD, SRS, 11 UC, 8 BRD, 8 Epic, 43 Story) đã nằm sẵn ở repo này. → **Sai thì hỏng ở đâu**: toàn bộ deliverable đặt nhầm repo, Phase 1 và Phase 2 ly tán, mọi relative link gãy.
- **Dùng standard markdown relative link `[Tên](./path.md)`, TUYỆT ĐỐI không dùng wiki-link `[[...]]`** — RULE-001 quy tắc #5 cấm wiki-link tường minh; `pm-doc.md` Bước 5 có nhắc `[[Document-Name]]` nhưng RULE-001 mới hơn (`updated: 2026-08-24`), `status: approved`, và chính `pm-doc.md` tuyên nó là *contract của lane này*. → **Sai thì hỏng ở đâu**: link không phân giải được, Connectivity check ở Bước 6 fail hàng loạt, phải viết lại toàn bộ phần liên kết. Ràng buộc này phải nằm trong `[CONSTRAINTS]` của **mọi** dispatch, không chỉ ghi ở đây.
- **`.agent/roles/` KHÔNG tồn tại ở repo này** (đã verify bằng `ls`) — dù `pm-core.md` Dispatch Prompt Template có dòng `Nạp .agent/roles/<role>.md`. Persona thật nằm ở `.claude/agents/<role>.md` (runtime tự nạp khi spawn). Dispatch sẽ trỏ worker tới role memory `knowledge-base/45-Role-Memory/<role>/` — path có thật, và `learning-loop.md` §4 bắt buộc đọc. → **Sai thì hỏng ở đâu**: worker tốn turn đi tìm file không tồn tại, hoặc báo BLOCKED ngay turn đầu.
- **Docs là SSOT duy nhất — không có code để đối chiếu.** `src/` và `test/` tồn tại nhưng **rỗng hoàn toàn** (đã verify), `000-Index.md` xác nhận "Chưa có dòng code nào". → **Sai thì hỏng ở đâu**: worker nào đi tìm implementation để reverse-engineer sẽ đốt sạch ngân sách tool call mà không thu được gì.
- **Kiến trúc thiết kế cho MVP nhưng không được đóng cửa với Full Scope** — 19 story ngoài MVP vẫn nằm trong backlog đã biết. → **Sai thì hỏng ở đâu**: schema và API contract phải phá đi làm lại ở Phase sau, tức là đúng cái rủi ro mà option "chỉ MVP0+MVP1" bị loại vì nó.

---

## Open questions

- **Độ hạt file `Endpoint-*.md`** — theo *resource* (gộp CRUD của một tài nguyên vào một file) hay theo *từng endpoint*? Em nghiêng về theo resource để tránh nổ 25+ file. **Ai trả lời**: PM chốt tại gate, sau khi có con số enumerate từ architect lens. **Chặn**: Bước 4 (outline).
- **Số lượng `DB-Entity-*.md` và `ADR-*.md`** — chưa biết cho tới khi architect lens đếm xong. **Chặn**: Bước 4.
- **Có mời `devops-engineer` khảo sát infra feasibility không?** Phase-2 liệt nó ở cột Support, nhưng Phase 2 không sinh artifact DevOps nào (Deployment thuộc `070-*`, phase sau). **Ai trả lời**: anh, tại gate.
- **`.claude/commands/pm-core.md` đã bị xóa ở commit `90a990f`** trong khi `pm-code.md`, `pm-doc.md` và `docs/010-Planning/pm-runs/README.md` đều vẫn tham chiếu nó như dependency bắt buộc. Run này nạp lại nội dung bằng `git show 90a990f^:.claude/commands/pm-core.md` — nội dung có thật, không suy đoán. **Ai trả lời**: anh, tại gate. Đây là việc **ngoài lane doc** (sửa command file), nên em chỉ báo, không tự khôi phục trong run này.
