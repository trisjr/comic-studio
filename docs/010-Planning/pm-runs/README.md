---
id: PM-RUNS
type: reference
status: draft
created: 2026-08-07
---

# PM Runs — Run-state của `/pm-code` và `/pm-doc`

Mỗi lần chạy `/pm-code` hoặc `/pm-doc` sinh ra một thư mục `<YYYY-MM-DD>-<slug>/` tại đây. Đây là **sổ tay điều phối của PM**, không phải deliverable — deliverable nằm ở `openspec/changes/`, `docs/`, hoặc source code tùy lane và tier.

| Định nghĩa | Đường dẫn |
|---|---|
| Phần lõi dùng chung (nguyên tắc, GATE, Worker Contract, Escalation) | `.claude/commands/pm-core.md` |
| Lane code | `.claude/commands/pm-code.md` |
| Lane tài liệu | `.claude/commands/pm-doc.md` |

> Các run trước ngày 2026-08-10 được sinh bởi command `/pm-run` — tiền thân của `/pm-code`. Run-state cũ giữ nguyên tên command tại thời điểm chạy, vì nó là dấu vết lịch sử.

## Cấu trúc một run

```
<YYYY-MM-DD>-<slug>/
├── brief.md          Bắt buộc — input gốc, lane, chấm triage, tier, assumptions
├── run-plan.md       Bắt buộc từ T1 — phase, agent assignment, file ownership
├── outline.md        Chỉ lane doc, từ T1 — bảng hạng mục tài liệu, outline, MOC cần cập nhật
├── findings/         Chỉ T2, T3 — output analysis fan-out, mỗi lens một file
│   └── <role>.md
├── escalations.md    Tạo khi có escalation đầu tiên, không tạo sẵn
├── verdict.md        Bắt buộc từ T2 — kết quả verification
└── cost.md           Bắt buộc từ T1 — chi phí token đo được của run
```

Tier thấp sinh ít file hơn. T0 chỉ có `brief.md`. Bên lane code, vai trò theo dõi tiến độ do `openspec/changes/<name>/tasks.md` đảm nhiệm thay cho `outline.md`.

## Schema từng file

### `brief.md`

```markdown
# Brief: <run-id>

## Yêu cầu gốc
<nguyên văn input của khách hàng — không diễn giải lại, không rút gọn>

**Lane**: code | doc
**Shape**: A (authoring) | B (normalization sweep) — chỉ lane doc, kèm lý do

## Triage
| # | Câu hỏi | Đáp án | Lý do |
|---|---------|--------|-------|
| Q1 | Chạm > 1 domain (code) / > 1 tầng tài liệu (doc)? | Có/Không | ... |
| Q2 | Đổi kiến trúc, contract (code) / sửa doc `approved`, đổi taxonomy (doc)? | Có/Không | ... |
| Q3 | Mơ hồ, thiếu AC / chưa rõ độc giả đích? | Có/Không | ... |
| Q4 | > 5 file hoặc > 1 ngày công? | Có/Không | ... |

**Điểm**: N/4 → **Tier**: T<n>
**Chọn tier thấp do phân vân**: Có/Không — nếu Có, ghi rõ tier còn lại là gì và
điều kiện nào sẽ kích hoạt escalate lên.

## Assumptions
- <giả định đang đi theo> → **sai thì hỏng ở đâu**: <hệ quả>

## Open questions
- <câu chưa có lời giải, ai sẽ trả lời, chặn phase nào>
```

### `run-plan.md`

```markdown
# Run Plan: <run-id>

## Phases
| # | Phase | Agent | Song song? | Input | Output |
|---|-------|-------|-----------|-------|--------|

## File ownership map
| Agent | Sở hữu (được ghi) | Cấm chạm |
|-------|-------------------|----------|

> Lane doc: điền sẵn cột *Cấm chạm* của mọi writer bằng `*-MOC.md`, `docs/000-Index.md`, `outline.md`.
> Đây là failure mode số một của lane doc — nhiều writer, một điểm hội tụ.

> Các tập ownership PHẢI rời nhau tuyệt đối. Không cắt rời được → chỉ dùng 1 implementer.
> File theo dõi tiến độ luôn thuộc về PM, không cấp cho worker nào: `tasks.md` (lane code),
> `outline.md` (lane doc). Lane doc còn giữ thêm mọi file `*-MOC.md` và `docs/000-Index.md` —
> đó là điểm hội tụ của mọi writer.

## Artifact sẽ tạo/sửa ngoài run-state
- <đường dẫn> — <mục đích>

## Gate
- Trình ngày: <YYYY-MM-DD>
- Kết quả: Duyệt / Duyệt kèm điều chỉnh / Từ chối
- Điều chỉnh của anh: <nếu có>
```

### `outline.md` — chỉ lane doc

Bảng hạng mục + outline từng tài liệu + wiki-link và MOC phải cập nhật. Schema đầy đủ nằm ở Bước 4 của `.claude/commands/pm-doc.md`.

Hai ràng buộc không được bỏ:
- Mỗi tài liệu phải khai **Nguồn sự thật** — căn cứ để writer viết. Không có nguồn thì writer ghi `TBD` và báo `PARTIAL`, tuyệt đối không bịa.
- Chỉ PM tick cột *Xong*, sau khi đã đối chiếu `FILES_TOUCHED` của writer.

### `findings/<role>.md`

Dán nguyên văn `SUMMARY` của worker, cộng thêm phần PM tự ghi:

```markdown
# Findings — <role>

## Kết luận của worker
<nguyên văn SUMMARY>

## PM đọc được gì
- <điều ảnh hưởng tới run plan>

## Mâu thuẫn với lens khác
- <nếu có — nêu rõ mâu thuẫn với ai, và PM phân xử thế nào, hoặc đã đẩy lên gate>
```

### `escalations.md`

Append-only. Không sửa entry cũ, chỉ thêm entry mới.

```markdown
# Escalations: <run-id>

## E1 — <tiêu đề ngắn>
- **Tầng**: 2 (PM tự quyết) | 3 (hỏi user)
- **Worker**: <agent> tại phase <n>
- **QUESTION**: <nguyên văn>
- **OPTIONS**: A… / B… / C…
- **RECOMMEND của worker**: <…>
- **Quyết định**: <…> — **lý do**: <…>
- **Hành động**: dispatch worker mới với câu trả lời inline / đổi tier / cắt scope
```

### `verdict.md`

```markdown
# Verdict: <run-id>

| Khía cạnh | Trạng thái |
|-----------|-----------|
| Completeness | X/Y task, N requirement |
| Correctness | M/N requirement được bao phủ |
| Coherence | Tuân thủ / Có vấn đề |
| Connectivity | Chỉ lane doc — link phân giải được, không file orphan |

## CRITICAL
- <phải sửa trước khi đóng run>

## WARNING
- <nên sửa>

## SUGGESTION
- <có thể cải thiện>

**Người verify**: <agent> — phải KHÁC agent đã implement.
Mặc định: `quality-assurance` (lane code), `context-auditor` (lane doc).
**Kết luận**: Đóng được / Quay lại Bước 5
```

### `cost.md`

Sinh ở close-step (xem `.claude/commands/pm-core.md`). Số lấy bằng cách cộng `.message.usage` trong
`~/.claude/projects/<slug>/<session>.jsonl` (main loop) và `<session>/subagents/*.jsonl` — đo, không nhớ.

```markdown
# Cost: <run-id>

| Actor | Tool calls | Turns | cache_read | ctx/turn |
|---|---:|---:|---:|---:|
| PM (main loop) | — | | | |
| <lô N — mô tả> | | | | |

**Tổng**: <X>M — PM <a>% / subagent <b>%

## Vượt ngân sách
- <lô nào, cấp bao nhiêu tool call, dùng hết bao nhiêu, vì sao>

## Số lô thực tế vs plan
<n>/<m> lô. Vượt >50% thì nêu lý do — lô nở thêm để khoá một requirement chưa có test là
chi phí của tính đúng đắn, không phải lỗi. Mục này để nó hiện ra, không phải để phán xét.

## Guardrail cần cập nhật
- <số nào trong pm-core.md đã lệch so với đo được ở run này, hoặc "không có">
```

## Quy ước

- Run-state được **commit vào repo**. Nó là dấu vết quyết định, có giá trị truy vết về sau — đặc biệt phần `escalations.md`.
- Không xóa run cũ. Run thất bại cũng giữ lại, vì lý do thất bại chính là dữ liệu.
- Không nhét secret, token, hay dữ liệu khách hàng nhạy cảm vào bất kỳ file nào ở đây.
