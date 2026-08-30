# Run Plan: 2026-08-28-phase-2-architecture-design-comic-studio

**Lane**: doc · **Shape**: A (authoring) · **Tier**: T3 (điểm triage 3/4)

## Phases

| # | Phase | Agent | Song song? | Input | Output |
|---|-------|-------|-----------|-------|--------|
| 1 | Intake & Triage | PM | — | Yêu cầu gốc + `Phase-2-Architecture-Design.md` | `brief.md` |
| 2 | Analysis fan-out | `architect`, `business-analyst` | ✅ 2 lens | Tài liệu Phase 1 | `findings/*.md` — **đã xong** |
| 3 | **GATE** | PM + anh | — | findings | `run-plan.md` + duyệt |
| 4 | Doc plan | PM | — | findings | `outline.md` — **đã xong** |
| 5 | Soạn thảo | `architect` (17 lô), `security-auditor` (2), `business-analyst` (2) | ✅ theo wave | `outline.md` | 57 tài liệu + 2 file ngoài `030-Specs` |
| 6 | Verify & Close | `context-auditor`, `quality-assurance`, PM | ✅ 2 verifier | Deliverable | `verdict.md`, MOC, `cost.md` |

### Thứ tự wave — phụ thuộc thật, không phải thứ tự tuỳ ý

```
Wave A  L1 ∥ L2 ∥ L0*            8 ADR mở (+ SRS amendment nếu gate #2 duyệt)
   ↓    (ADR-005 chốt vị trí schema · ADR-006 chốt tenant context — cả schema lẫn API đều cần)
Wave B  L3 → L4                  SDD (MỘT file, hai lô TUẦN TỰ, writer mới mỗi lô)
   ↓    (Security Spec threat-model chạy TRÊN SDD — đúng câu lệnh mẫu của Phase-2)
Wave C  L5 ∥ L6 ∥ L7 ∥ L8        10 ADR record-only + schema đợt 1
Wave D  L9 ∥ L10 ∥ L11 ∥ L12     schema đợt 2 + API đợt 1
Wave E  L13 ∥ L14 ∥ L15 ∥ L16    API đợt 2 + integration đợt 1
Wave F  L17 ∥ L18 ∥ L20          integration đợt 2 + Security 1 + Glossary
Wave G  L19                      Security Legal-Compliance
Wave H  L21 ∥ L22                verify: context-auditor ∥ quality-assurance
```

> **Checkpoint `/compact` sau GATE và sau mỗi wave.** Run-state giữ đủ trạng thái để resume — đó là lý do nó tồn tại. PM main loop chiếm 37% chi phí ở run đo được trước đây; đây là cơ chế chặn nó.

## File ownership map

| Agent | Sở hữu (được ghi) | Cấm chạm |
|-------|-------------------|----------|
| `architect` (L1–L17, mỗi lô một writer MỚI) | **Đúng danh sách file của lô đó** trong `outline.md` §1 — PM dán nguyên văn vào `[OWNERSHIP]` | `*-MOC.md` · `docs/000-Index.md` · `outline.md` · `brief.md` · `findings/` · `docs/020-Requirements/` · `docs/022-User-Stories/` · file của lô khác |
| `security-auditor` (L18, L19) | `docs/030-Specs/Security/Spec-Security-*.md` | như trên + toàn bộ `Architecture/`, `Schema/`, `API/` (chỉ đọc) |
| `business-analyst` (L0) | `docs/020-Requirements/SRS-Comic-Studio.md` — **chỉ bảng §5.2** | như trên + `docs/030-Specs/` |
| `business-analyst` (L20) | `docs/999-Resources/Glossary.md` — **append-only** | như trên + `docs/030-Specs/` |
| `context-auditor` (L21) | `verdict.md` | **read-only toàn repo** ngoài file đó |
| `quality-assurance` (L22) | `verdict-qa.md` | **read-only toàn repo** ngoài file đó |
| **PM** | `outline.md` · `brief.md` · `findings/*.md` · **mọi `*-MOC.md`** · `docs/000-Index.md` · `cost.md` · `escalations.md` | — |

> ⛔ **`*-MOC.md` và `docs/000-Index.md` không bao giờ cấp cho worker.** Đây là điểm hội tụ của 21 writer — cấp cho hai người là cầm chắc ghi đè lẫn nhau.
> ⛔ **`docs/010-Planning/pm-runs/` của run CŨ** nằm ngoài phạm vi mọi lô — nó là dấu vết quyết định, không phải tài liệu cần chuẩn hoá.

## Kế hoạch dispatch theo lô

| Lô | Nội dung | Số file | Writer | Ngân sách |
|:--:|---|:--:|---|--:|
| L0* | SRS §5.2 — 7 hàng NFR | 1 | business-analyst | 60 |
| L1 | ADR-001…004 (stack, hosting, vendor auth/billing, storage) | 4 | architect | 60 |
| L2 | ADR-005…008 (schema placement, RLS context, VLM, LLM) | 4 | architect | 60 |
| L3 | SDD §1–7 | 1 | architect | 60 |
| L4 | SDD §8–9 | 1 | architect | 60 |
| L5 | ADR-009, 010, 011 | 3 | architect | 60 |
| L6 | ADR-012, 013, 014 | 3 | architect | 60 |
| L7 | ADR-015, 016, 017, 018 | 4 | architect | 60 |
| L8 | Schema: Narrative-Timeline, Story-Bible, Comic-IR, Dialogue-And-Gate | 4 | architect | 60 |
| L9 | Schema: Typeset-Layer, Generation, Prompt-Vocabulary, Job-Queue | 4 | architect | 60 |
| L10 | Schema: Tenancy, Provenance-And-Usage, Compliance-And-Takedown | 3 | architect | 60 |
| L11 | Schema: Quality-Assets, Credit-Ledger | 2 | architect | 60 |
| L12 | API: Project, Chapter-Ingest, Story-Bible, Timeline-Event | 4 | architect | 60 |
| L13 | API: Panel-Script, Page-Layout, Human-Gates, Generation | 4 | architect | 60 |
| L14 | API: Bubble-Typeset, Preview-Export, Tenancy, Usage-And-Credit | 4 | architect | 60 |
| L15 | API: Takedown-Public, Eval-Kit | 2 | architect | 60 |
| L16 | Integration: Image-Provider, VLM-QA-Select, LLM-Provider | 3 | architect | 60 |
| L17 | Integration: Auth, Object-Storage, Takedown-Intake, Billing | 4 | architect | 60 |
| L18 | Security: Threat-Model, Tenant-Isolation | 2 | security-auditor | 60 |
| L19 | Security: Legal-Compliance | 1 | security-auditor | 60 |
| L20 | Glossary delta 18 headword | 1 | business-analyst | 60 |
| L21 | Verify — Completeness/Correctness/Coherence/Connectivity | 0 (read-only) | context-auditor | 60 |
| L22 | Verify — 2 track nghiệm thu + tiêu chí chuyển phase | 0 (read-only) | quality-assurance | 60 |

**Tổng: 23 lô × 60 = ~1.380 tool call** (L0 có điều kiện; không có lô nào cần phụ cấp mutation-test — lane doc). Đây là **ước lượng thô của cả run** và em nói thẳng: **đây là một run lớn**. Con số này hiện ra ở đây đúng để anh nhìn thấy trước khi duyệt, không phải để giấu vào giữa chừng.

## Artifact sẽ tạo/sửa ngoài run-state

- `docs/030-Specs/Architecture/` — **20 file** (1 SDD + 19 ADR, trong đó ADR-019 hoãn)
- `docs/030-Specs/Schema/` — **13 file** `DB-Entity-*`
- `docs/030-Specs/API/` — **21 file** (14 `Endpoint-*` + 7 `Spec-Integration-*`)
- `docs/030-Specs/Security/` — **3 file** `Spec-Security-*`
- `docs/030-Specs/Specs-MOC.md` — viết mới (PM, close-step)
- `docs/000-Index.md` — sửa §030 + mục Nợ kỹ thuật (PM, close-step)
- `docs/020-Requirements/Requirements-MOC.md` — sửa L12 + quy ước #4 (PM, close-step, ripple)
- `docs/999-Resources/Glossary.md` — append 18 headword
- `docs/020-Requirements/SRS-Comic-Studio.md` — **chỉ khi gate #2 duyệt**

## Assumptions (chi tiết ở `brief.md`)

1. Đích ghi là repo `comic-studio`, không phải `TNMCore-OS`.
2. Standard markdown link, ⛔ không wiki-link — RULE-001 override phần văn bản của `pm-doc.md`.
3. `.agent/roles/` không tồn tại → dispatch trỏ `knowledge-base/45-Role-Memory/<role>/`.
4. Mọi deliverable `status: draft` — approve là quyết định Founder tại Go/No-Go.
5. **G3 tự phân xử**: `ADR-005` đi hướng đặt bảng platform vào `public`. Hai phương án kia tự loại — thêm schema thứ 4 đụng quyết định CHỐT *"3 schema"*, rải theo module phá `KC-4`. **Sai thì hỏng ở đâu**: nếu anh muốn schema thứ 4, `ADR-005` + 13 file schema phải sửa lại đường dẫn schema.
6. **G4 KHÔNG phải câu hỏi gate**: cơ chế bơm tenant context nằm trong nhóm Phase 1 **cố ý để mở** → là deliverable `ADR-006`.
7. **G12**: link một chiều `030` → `020`; ⛔ không chạm `SRS` để thêm link xuống.
8. **Không spawn `devops-engineer`.** Phase-2 liệt DevOps ở cột Support, nhưng phase này **không sinh artifact DevOps nào** (Deployment thuộc tầng `070`, phase sau), và infra feasibility đã nằm trong `ADR-002`. Spawn một lens không có deliverable là trả ~23.6k overhead lấy về một ý kiến không ai sở hữu.

## Gate

- **Trình ngày**: 2026-08-29
- **Kết quả**: ✅ **Duyệt — chạy hết**
- **Bốn quyết định của anh tại gate**:
  1. **Phạm vi = toàn horizon MVP0–MVP2 (41 story)**, không phải 24 `⭐`. Lý do: `⭐` là bộ lọc *"chặn exit criterion"*, không phải bộ lọc build — hai lens hội tụ độc lập vào kết luận này. ⚠️ **Hệ quả lan xuống mọi lô**: 3 tầng `[24⭐]` / `[H-non⭐]` / `[OoH]` trong findings **đều thuộc phạm vi**; `[OoH]` vẫn giữ mức *"reserve chỗ"*.
  2. **NFR: bổ sung 7 hàng `b-1…b-7` vào `SRS` §5.2** (phương án B). ⇒ **L0 kích hoạt**, và **L18/L19 (Security) phải chờ L0 xong**.
  3. **UC-06: hard quota tạm** thay HOLD credit ở MVP1–MVP2. ⚠️ Ràng buộc kiểm chứng: `Story-Minimum-Abuse-Controls` nằm trong phạm vi, nên một cơ chế quota **đã phải tồn tại** — writer `Endpoint-Generation.md` phải verify và neo vào Story đó, ⛔ không tự phát minh cơ chế mới.
  4. **Duyệt run plan** — chạy thẳng tới hết, không hỏi lại trừ Escalation Protocol tầng 3.
- **Điều chỉnh của anh**: không có. Cả bốn câu chọn đúng phương án PM đề xuất.
