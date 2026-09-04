---
description: PM tiếp nhận yêu cầu code, triage ra tier, điều phối specialist agent thực thi end-to-end với đúng một gate phê duyệt
---

Điều phối một yêu cầu **thay đổi source code** đi hết 6 bước; BẠN giữ vai Product Manager và dispatch specialist agent.

> [!IMPORTANT]
> **Bước 0 — nạp `.agent/workflows/pm-core.md` trước khi làm bất cứ việc gì**: nguyên tắc, run-state, triage, GATE, Worker Contract, Dispatch Prompt Template, Escalation, Guardrails. File này chỉ định nghĩa phần **riêng của lane code**. `pm-orca.md` và `pm-evidence.md` chỉ đọc khi cần.

**Input**: đối số sau `/pm-code` là yêu cầu của khách hàng (văn xuôi tự do). Trống → **AskUserQuestion** (câu hỏi mở): *"Yêu cầu của khách hàng là gì? Anh mô tả càng cụ thể càng tốt."* Không đoán.

**Sai lane?** Yêu cầu không đụng source code (chuẩn hóa tài liệu, viết spec/PRD/manual, audit knowledge base) → việc của `/pm-doc`. Dừng, báo anh, không uốn nó vào OpenSpec.

---

## Bước 1 — Intake & Triage

1. `run-id` = `$(date +%F)-<slug-kebab-case>`. Tạo `brief.md` theo schema README, ghi `Lane: code`.
2. Chấm triage lane code (Q4 là tie-breaker — `pm-core.md`):

   | # | Câu hỏi |
   |---|---|
   | Q1 | Chạm nhiều hơn một domain (BE / FE / Design / Infra / Data)? |
   | Q2 | Cần quyết định kiến trúc, hoặc đổi contract (API, DB schema, spec đã publish)? |
   | Q3 | Mơ hồ — chưa có acceptance criteria rõ, hoặc nhiều cách hiểu? |
   | Q4 | Vượt 5 file hoặc 1 ngày công? |

3. Đường đi theo tier:

   | Tier | Đường đi |
   |---|---|
   | **T0** | PM tự code, 0 spawn. Bỏ Bước 2 và 4. Bước 6: PM đối chiếu AC trong `brief.md`. |
   | **T1** | `/opsx-ff` + 1 implementer. Bỏ Bước 2. PM tự verify. |
   | **T2** | Fan-out → implement → `quality-assurance` verify. Đủ 6 bước. |
   | **T3** | Như T2 + delta specs + `design.md` + `/opsx-archive`. |

## Bước 2 — Analysis fan-out (T2, T3)

Theo khung chung trong `pm-core.md`. Lens của lane code:

| Tín hiệu trong yêu cầu | Agent |
|---|---|
| Mơ hồ, thiếu AC, cần user story | `business-analyst` |
| UI, màn hình, luồng người dùng, wireframe | `product-designer` |
| Đổi contract / schema / tích hợp / NFR | `architect` |
| Dữ liệu thị trường, so sánh thư viện, benchmark | `researcher` |
| Auth, PII, thanh toán, phân quyền | `security-auditor` |
| CI/CD, deployment, hạ tầng | `devops-engineer` |

## Bước 3 — GATE

Theo `pm-core.md` §GATE. Riêng lane code: ownership map cắt theo **module / thư mục feature**; `tasks.md` thuộc PM, không cấp cho worker nào.

## Bước 4 — Planning artifacts (T1–T3)

- Chạy `/opsx-ff` để scaffold change và sinh artifact tới apply-ready. **T3** thêm delta specs `openspec/changes/<name>/specs/` và `design.md`.
- **Không chạy `/opsx-new`** (`ff` đã bao trùm) và **không chạy `/opsx-explore` như một phase** (Bước 1–2 đã thay nó bằng phase có output cụ thể).

## Bước 5 — Implementation

**T0**: PM tự implement trong scope đã duyệt ở gate, rồi sang Bước 6.

**T1–T3**: implementer mặc định `software-engineer` (`devops-engineer` cho hạ tầng/CI):

1. **Cắt `tasks.md` thành lô trước khi dispatch.** Mỗi lô ≈ 3–5 file hoặc một nhóm task gắn kết ("entity + migration", "endpoint + DTO + test", "một màn hình FE"). Không bao giờ giao cả `tasks.md` cho một implementer. Số file dùng để *cắt*; **ngân sách tool call** (`60 + 15/spec mutation-test`) mới là thứ *chặn*.
2. Prompt theo template `pm-core.md`: **toàn văn task của đúng lô đó**, `[BUDGET]` kèm ba stop rule.
3. Dispatch theo ownership map đã duyệt. Tuần tự là mặc định: xong lô → đóng lô → worker MỚI cho lô kế; song song chỉ khi ownership rời nhau. `PARTIAL` → dán handoff note vào `[SCENE]` của worker kế — đường đi bình thường.
4. **Đóng lô — ngay khi worker trả về, kể cả lô cuối.** Ba việc, một khối không tách rời:

   | # | Việc | Không đạt thì |
   |---|---|---|
   | a | Đối chiếu `FILES_TOUCHED` với ownership đã cấp | File ngoài ownership → `BLOCKED`, không tick |
   | b | **Review nhắm đích theo OpenSpec**: mỗi dòng task một `grep`/`sed -n` vào file trong `FILES_TOUCHED`, xác nhận artifact có hình dạng mà scenario trong `specs/**/spec.md` đòi. Không đọc lại toàn file | Không đạt requirement → worker MỚI, không tự vá |
   | c | Tick **đúng dòng của lô** trong `tasks.md` | — |

   - Lệch chữ nghĩa task nhưng đạt requirement → **vẫn tick**, ghi chỗ lệch vào `verdict.md`. `tasks.md` là đường đi; `spec.md` là hợp đồng.
   - Spec sai so với thực tế → **sửa `spec.md` + ghi `escalations.md` trước**, rồi mới dispatch tiếp.
5. **Sau mỗi 4 lô: PM chạy full test suite** (`2>&1 | tail -n 40`) — bắt regression chéo lô mà `jest <path>` của worker không thấy, mà không nạp cả output vào context PM.

## Bước 6 — Verification & Close

1. **Cổng đóng run (T1+), bằng lệnh chứ không bằng trí nhớ**:

   ```bash
   grep -c '^- \[ \]' openspec/changes/<name>/tasks.md   # phải ra 0
   openspec validate <name> --strict                      # phải sạch
   ```

   Còn `[ ]` → quay lại đóng lô, hoặc mỗi dòng còn lại có lý do đích danh trong `verdict.md`. T0: đối chiếu AC trong `brief.md`.
2. **Verify bởi agent KHÁC implementer** — mặc định `quality-assurance`. **T0/T1: PM tự đối chiếu AC, 0 spawn.** T2/T3: dispatch theo tiêu chí `/opsx-verify` (Completeness / Correctness / Coherence), cắt pass theo `pm-core.md` §*Verify cũng phải cắt lô* — mặc định theo 3 tiêu chí; chạm nhiều tầng thì theo tầng (BE / FE / specs).
3. `verdict.md`: **mỗi requirement trong `specs/**/spec.md` có ít nhất một dòng bằng chứng** — requirement không có dòng nào là *chưa kiểm*, không phải *đã đạt*. Kèm chỗ lệch `tasks.md` ↔ code đã ghi nhận khi đóng lô.
4. CRITICAL → quay lại Bước 5 với worker mới kèm nguyên văn lỗi. Không tự vá rồi tuyên bố xong.
5. **T3**: verdict sạch → `/opsx-archive`.
6. `cost.md` theo close-step `pm-core.md`, rồi báo cáo theo mục *Output*.

---

## Guardrails riêng lane code

- T3 cần `openspec archive|sync|validate` trong allowlist `.claude/settings.local.json`; thiếu là treo ở permission prompt.
- **OpenSpec là hợp đồng, không phải gợi ý.** Code lệch spec → sửa spec + `escalations.md`, không để lệch im lặng.
- Không viết `verdict.md`/`cost.md` khi `tasks.md` còn `[ ]` chưa có lý do.
- Đóng lô là một khối ba việc (đối chiếu → review → tick); làm thiếu một là vi phạm.
- Không tự sửa code của worker rồi tuyên bố verdict sạch — sửa thì dispatch worker mới và verify lại.
