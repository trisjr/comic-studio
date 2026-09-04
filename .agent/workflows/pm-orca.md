# PM Orca — Sổ tay runtime Orca cho `/pm-code` và `/pm-doc`

> [!IMPORTANT]
> File này **không phải slash command** và **không có bản mirror** ở `.claude/commands/`. Nó là đích của một lệnh Read, chỉ nạp khi `pm-core.md` báo Orca khả dụng **và** PM sắp dispatch lô Orca đầu tiên. Run thuần lane Agent không bao giờ đọc file này — đó chính là lý do nó tách ra.
>
> Nền tảng nằm ở `.agent/workflows/pm-core.md`. Ở đây chỉ có thứ **riêng của runtime Orca**. Số đo được trích dẫn trong file này giải thích ở `.agent/workflows/pm-evidence.md`.

## Vì sao lane Orca tồn tại

**Worker chạy trên provider khác thì run không tiêu tốn quota Claude.** Subagent chiếm **63%** tổng chi phí run `2026-08-22` (xem `pm-evidence.md`). Đẩy phần đó sang provider khác là đòn bẩy lớn hơn mọi tối ưu context cộng lại.

| | **Lane Agent** (mặc định) | **Lane Orca** |
|---|---|---|
| Cơ chế | Agent tool, subagent in-process | Tiến trình CLI riêng trong terminal Orca |
| Persona / tool list | Harness cắt theo `.claude/agents/<role>.md` | **Không có** — chỉ còn prose trong `[CONSTRAINTS]` |
| Kênh hai chiều | Không | **Có** — `ask`/`reply` |
| Token Claude do worker tiêu thụ | Toàn bộ | **0** nếu worker là provider khác |

Mọi lý lẽ về overhead startup chỉ áp cho worker `--agent claude`; với worker provider khác, chi phí Claude bằng 0 nên phép so đó vô nghĩa.

Hai nguyên tắc bất biến của `pm-core.md` **đổi nghĩa** ở đây:

- **Nguyên tắc #2 (subagent không spawn được subagent)** — worker Orca **không** bị ràng buộc này: nó là tiến trình CLI đầy đủ với nguyên bộ tool của nó. Ràng buộc phải được nêu trong `[CONSTRAINTS]`; harness không còn bảo đảm hộ.
- **Nguyên tắc #3 (kênh hai chiều là `SendMessage`)** — lane Orca dùng kênh native `ask`/`reply` thay cho `SendMessage`, được runtime bảo chứng: worker đứng chờ, PM `reply`, worker đi tiếp với **context còn nguyên**, không respawn. Đã kiểm chứng trên cả worker `claude` lẫn `omp`. Đừng mang giới hạn của lane Agent sang đây — làm vậy là tự vứt đi đòn bẩy chi phí lớn nhất của lane này.

---

## Chọn runtime cho từng lô — test O1–O3

Orca khả dụng **không** có nghĩa là mọi lô đi Orca. Trước mỗi dispatch, trả lời ba câu:

| # | Câu hỏi | Nếu "Không" thì sao |
|---|---------|---------------------|
| O1 | PM kiểm được acceptance criteria **mà không phải tự làm lại việc đó**? | Không kiểm rẻ được thì không giao đi được — xem *Review và làm lại* |
| O2 | Spec flatten thành **một dòng** mà không mất điểm quyết định nào? | Việc còn điểm cần cân nhắc thì worker không có kênh để cân nhắc đúng |
| O3 | Output sai thì **vứt đi rẻ** — không mutation test dở, không migration nửa chừng, không state chung? | Làm lại tốn hơn làm đúng từ đầu |

**Cả ba = Có → Orca. Một câu = Không → lane Agent.** Ghi kết quả vào cột `Runtime` của lô đó trong `run-plan.md`; câu trượt là gì thì ghi luôn, đó là dữ liệu để chỉnh test này về sau.

Việc thường **đạt**: inventory/liệt kê máy móc, áp template lên nhiều file, sửa lặp có pattern rõ, soạn tài liệu đã có outline chốt và nguồn sự thật đầy đủ.

Việc thường **trượt**: chọn giữa hai phương án thiết kế, đổi contract/schema/taxonomy, phân tích phán đoán mà kết luận không kiểm được nếu không tự phân tích lại (`architect`, `security-auditor`, `business-analyst` ở Bước 2), và **mọi pass verify** — sai của verify là bỏ sót, mà bỏ sót thì không ai bắt được.

> Đây là chọn **runtime** cho một lô, không phải đổi **lane**. Guardrail *"Không đổi lane giữa chừng"* của `pm-core.md` nói về `code` vs `doc` và vẫn giữ nguyên hiệu lực.

## Review và làm lại — bắt buộc với mọi lô Orca

Worker Orca không có persona do harness cắt, không auto-load `.claude/rules/`, và chất lượng output của model đang pin **chưa được đo lần nào** — mới chỉ kiểm chứng đường ống. Vì vậy **không có output Orca nào được tính là xong khi PM chưa nghiệm thu.**

1. **Trước khi dispatch**: prompt phải có section `[ACCEPT]` — checklist AC tường minh, do PM viết. Thiếu `[ACCEPT]` thì không được dispatch Orca. Viết không nổi checklist tức là lô đó đã trượt O1.
2. **Sau khi worker báo `worker_done`**: PM chạy checklist theo kiểu **diff-scoped** — `git diff --stat` rồi đọc hunk đã đổi, đối chiếu `filesModified` với ownership. **Không** đọc lại toàn bộ file.
3. **Trượt checklist** → tạo **Task MỚI** với feedback dán nguyên văn vào `[SCENE]`: điểm `[ACCEPT]` nào trượt, đường dẫn trong `filesModified`, bằng chứng từ diff. Dispatch đã settle thì không mở lại được, `--outcome failed` cũng không dùng ở đây (xem *PARTIAL ở lane Orca*).
    - **Phải nói rõ worker mới bắt đầu từ trạng thái working tree nào.** Mặc định là **sửa tại chỗ** trên output cũ. Nhưng nếu output cũ không an toàn để xây tiếp — test đỏ, cấu trúc sai, file đặt nhầm chỗ — thì PM `git checkout -- <filesModified>` **trước khi** dispatch, và ghi việc đã revert vào entry `escalations.md`. Bỏ qua bước này là để worker sau thừa hưởng một working tree hỏng như thể đó là việc thật. Luật này áp cho cả worker fallback ở mục 4.
4. **Trần: tối đa MỘT lần làm lại.** Trượt lần hai → lô đó **rơi về lane Agent**, không thử lần ba. Redo không giới hạn trên một model không làm nổi việc sẽ đốt quota provider kia và context PM trong khi tiết kiệm Claude bằng **0** — đúng thứ lane này sinh ra để tránh.
5. **Ghi lại**: mỗi vòng redo một entry trong `escalations.md`; tổng số vòng redo và số lô phải fallback về Agent vào `cost.md`.

> Nghiệm thu **không phải ngoại lệ** của guardrail *"PM đọc SUMMARY, không đọc lại toàn bộ file"* trong `pm-core.md` — nó chính là điều kiện xét duyệt. O1 đã lọc từ trước: lô nào PM không check rẻ được thì lô đó không được giao sang Orca. Hai luật nói cùng một điều từ hai phía.

---

## Ánh xạ theo lane

### Lane code

**Roster**: lô nào đi Orca thì chạy bằng recipe hai bước với `omp` pin model; role chỉ còn là **prose trong `[ROLE]` + đường dẫn `.agent/roles/<role>.md`** cho worker tự đọc, không còn được harness cắt tool. PM luôn ở lại Claude.

| Bước | Ánh xạ sang Orca |
|---|---|
| **Bước 2** — lens **máy móc** (khảo sát cây thư mục, liệt kê call-site, dựng bảng inventory) | 1 Task + 1 terminal riêng. `--report-path` trỏ `findings/<role>.md`. Song song được, nhưng là N lệnh CLI tuần tự chứ không phải một message nhiều tool use. |
| **Bước 2** — lens **phán đoán** (`architect`, `security-auditor`, `business-analyst`, `researcher`) | **Ở lại lane Agent.** Trượt O1: kết luận của các lens này không kiểm được nếu PM không tự phân tích lại. |
| **Bước 5** — mỗi lô | Theo test O1–O3. Đạt: sửa lặp có pattern rõ, áp template, boilerplate, task đã chốt cách làm. Trượt: đổi contract/schema, chọn giữa hai phương án thiết kế, lô có mutation test (trượt O3). Tick `tasks.md` từ **`filesModified` trong payload**, không đọc prose. |
| **Bước 6** — mọi pass verify | **Ở lại lane Agent.** Sai của verify là **bỏ sót**, không checklist nào bắt được — trượt O1. |

`[ACCEPT]` của lane code phải kiểm được **từ diff**: test nào phải xanh, file nào phải đổi, pattern nào phải xuất hiện. *"Code sạch"* không phải acceptance criteria.

### Lane doc

**Roster**: như trên. PM giữ độc quyền `outline.md`, mọi `*-MOC.md` và `docs/000-Index.md` — worker Orca không bao giờ được cấp các file này.

| Bước | Ánh xạ sang Orca |
|---|---|
| **Bước 2** — **inventory** (Shape B) | Lô hợp Orca nhất của cả lane: đầu ra là bảng sự kiện — đường dẫn, `id`/`type`/`status`/`updated`, MOC trỏ tới, link chết — PM đối chiếu tại chỗ bằng `ls`/`grep`, đúng tinh thần O1. `--report-path` trỏ `findings/inventory.md`; bảng dài hàng trăm dòng vẫn do worker tự ghi, PM chỉ đọc. |
| **Bước 2** — lens **phán đoán** (`business-analyst`, `architect`, `product-designer`) | **Ở lại lane Agent.** Trượt O1. |
| **Bước 5** — mỗi tài liệu (Shape A) / mỗi lô (Shape B) | Theo test O1–O3. Đạt: outline đã chốt, **Nguồn sự thật đã đủ**, việc còn lại là soạn theo template — và Shape B normalization (bump frontmatter, sửa link, đổi thuật ngữ đồng loạt) gần như luôn đạt. Trượt: outline còn ô trống, nguồn còn `TBD`, hoặc tài liệu phải tự quyết cấu trúc. Tick `outline.md` từ **`filesModified` trong payload**. |
| **Bước 6** — mọi pass verify | **Ở lại lane Agent.** Trượt O1. |

**Rủi ro đặc thù lane doc phải bù bằng prompt.** Worker `omp` chỉ nạp `CLAUDE.md` + `AGENTS.md`, **không** nạp `.claude/rules/`. Mà lane này sống bằng contract:

- `[CONSTRAINTS]` **bắt buộc** nêu đường dẫn `knowledge-base/99-Templates/Documents-Template.md` (RULE-001) và yêu cầu worker đọc trước khi viết. Không có nó, worker sẽ đặt sai thư mục, thiếu frontmatter, quên bump `updated`.
- Nhắc lại trong `[CONSTRAINTS]`: **không chạm file MOC và `000-Index.md`**; không bịa số liệu/ngày/tên người, thiếu nguồn thì ghi `TBD`.
- `[ACCEPT]` phải kiểm được từ diff: frontmatter đủ field, đặt đúng thư mục Dewey, link phân giải được, không có `TBD` ngoài chỗ đã cho phép. *"Viết mạch lạc"* không phải acceptance criteria.

> Verify cross-model-family (`omp` verify thứ Claude vừa viết) vẫn là ý tưởng có giá — nó không thừa hưởng cùng điểm mù, và failure mode của prose là *"sai mà trôi lọt"*. Nhưng chất lượng model đang pin **chưa đo lần nào**; để dành cho vòng sau, sau khi có số nghiệm thu ở `cost.md`.

---

## Thủ tục dispatch

### Bước 0 bắt buộc

```bash
orca skills get orchestration
```

Grammar của `orca orchestration` **đổi giữa các release**. Mọi flag viết trong file này là **minh hoạ**, không phải nguồn sự thật — luôn lấy grammar thật từ lệnh trên trước khi dispatch. Đừng đoán subcommand từ trí nhớ.

### Precondition checklist trước mỗi run có lô Orca

1. `orca status --json` → runtime ready.
2. **Pin `WT_ID`** — làm trước mọi lệnh khác có `--worktree`. Xem *Worktree binding* ngay dưới.
3. Re-resolve terminal handle **của chính PM** từ `orca terminal list --json` — **không** truyền `--worktree`. Xem *Worktree binding*.
4. `orca skills get orchestration`.
5. Mỗi agent CLI **no-prompt** (không update notice, không session picker) và **còn quota**.
6. **PM không phải là worker.** Nếu prompt của chính BẠN chứa preamble Orca thì BẠN là worker, và `worker-start` sẽ fail `nested_worker_depth_exceeded` (mặc định nested depth = 1). Không có lệnh CLI nào hỏi được điều này — tự kiểm tra prompt của mình.

Bỏ qua mục 5 (kiểm agent CLI) là rủi ro treo run giữa Bước 5 của workflow: prompt khởi động làm fail `agent_readiness`/`dispatch_input`, và PM **không tự gỡ được** (xem *Guardrails*).

Bỏ qua mục 2 thì tệ hơn — nó không treo run, nó để run chạy **trót lọt trên sai checkout**.

### Worktree binding — pin một lần, dùng suốt run

`current` / `active` **không** đọc `ORCA_WORKTREE_ID`. Đo thật: chúng resolve bằng cách đi ngược từ **process cwd** lên tới worktree Orca-managed gần nhất — unset env vẫn ra kết quả y hệt, và chỉ trả `selector_not_found` khi cwd nằm ngoài mọi worktree. Đứng bên trong repo thì phép đi ngược đó **luôn tìm được một cái gì đó**: cwd lệch một tầng là lệnh rơi về checkout cha — **im lặng, không lỗi** — và worker sẽ sửa sai checkout.

Vì vậy pin id **một lần** ở đầu run:

```bash
orca worktree current --json     # → .result.worktree.id, .result.worktree.path
git rev-parse --show-toplevel
```

**Assert `.result.worktree.path` == `git rev-parse --show-toplevel`.** Lệch → **abort run**, không dispatch gì, báo anh kèm cả hai đường dẫn. Khớp → lấy `.result.worktree.id` (dạng `<repoId>::<absolutePath>`) làm `WT_ID`, và **ghi vào `brief.md`** ở field `Worktree:` (schema tại `pm-core.md` mục *Run-state*).

Từ đó **mọi lệnh đặt worker** (`terminal create`, `worker-start`) truyền `--worktree id:<WT_ID>`, tuyệt đối không truyền `current`. Lý do không chỉ là an toàn cwd: `brief.md` là thứ sống sót qua `/compact`, nên sau compact PM lấy lại đúng worktree từ đĩa chứ không resolve lại từ cwd hiện thời.

Ngoại lệ duy nhất: **tìm handle của chính PM thì không truyền `--worktree`** — xem *Hai worktree, không phải một* ngay dưới.

> Worktree lồng do tool khác tạo (`EnterWorktree`, `git worktree add .claude/worktrees/<name>`) **được Orca auto-adopt** — kiểm chứng thật: vừa tạo xong thì `orca worktree current` đã ra đúng path + branch, và `terminal create --worktree id:<WT_ID>` spawn terminal có `pwd` đúng worktree đó. Nhưng adoption là thứ **phải xác nhận bằng assert ở trên**, không phải thứ được giả định: nếu Orca chưa adopt, `current` trả về checkout cha một cách hoàn toàn "hợp lệ".

#### Hai worktree, không phải một

**Terminal Orca gắn `worktreeId` lúc nó SINH RA, không theo cwd của tiến trình bên trong.** Nên khi PM đổi checkout giữa phiên (`EnterWorktree`, `cd`), terminal của PM vẫn nằm ở worktree cũ, và hai thứ dưới đây **tách nhau ra**:

| | Lấy từ | Dùng cho |
|---|---|---|
| **`WT_ID`** — worktree PM đang thao tác | `orca worktree current` + assert (ở trên) | Mọi `--worktree` khi **đặt worker**: `terminal create`, `worker-start` |
| **`COORD_WT`** — worktree chứa terminal của PM | field `worktreeId` của chính row handle PM | Chỉ để biết PM đang đứng ở đâu. **Không** dùng để đặt worker |

Đo thật đúng tình huống này: PM mở tab ở checkout cha rồi `EnterWorktree` sang `.claude/worktrees/<x>` → `WT_ID` = nested (đúng), nhưng `terminal list --worktree id:<WT_ID>` trả **danh sách rỗng** (`liveTerminalCount: 0`) trong khi 3 terminal thật đều mang `worktreeId` của checkout cha. Vì vậy **tuyệt đối không scope việc tìm handle của PM theo `WT_ID`** — làm vậy là PM không tìm nổi `--from` của chính mình:

```bash
orca terminal list --json     # KHÔNG truyền --worktree; mỗi row tự mang worktreeId
```

Khớp theo `title` của session để lấy handle, rồi đọc `worktreeId` của **chính row đó** làm `COORD_WT`. `--worktree all` **không hợp lệ** ở `terminal list` (trả `selector_not_found`) — bỏ hẳn flag mới là cách liệt kê chéo worktree.

> `ORCA_TERMINAL_HANDLE` trong env có thể trỏ tới handle **không tồn tại ở bất kỳ worktree nào** — đo thật: env báo một handle mà `terminal list` (mọi worktree) không có row nào khớp. Đây là bằng chứng cụ thể cho luật *"Không tin env"*: env chỉ dùng làm gợi ý để khớp, không bao giờ dùng làm `--from`.

### Recipe dispatch (đã kiểm chứng)

`worker-start --agent <x> --model <y>` **chỉ nhận** model cho Claude/Codex/Cursor. Với `omp` nó trả `invalid_argument — "Agent omp does not support launch-time model selection"`. Muốn pin model, hoặc muốn thêm `--tools` / `--append-system-prompt`, phải đi đường hai bước:

```bash
orca terminal create --worktree id:<WT_ID> --title <lô> \
  --command 'omp --model google-antigravity/gemini-3.8-flash-high' --json
orca terminal wait --terminal <h> --for tui-idle --timeout-ms 120000 --json
orca orchestration worker-start --task <task_id> --terminal <h> --worktree id:<WT_ID> --from <coord> --json
# … check --wait → reply nếu có question → ack → NGHIỆM THU …
orca orchestration worker-release --dispatch <d> --json   # sẽ trả retained
orca terminal close --terminal <h> --json                 # BẮT BUỘC, xem Guardrails
```

**`--worktree` của `worker-start` mô tả worktree của terminal đang reuse**, không phải chỗ tạo mới. `--help` ghi thẳng: *"When reusing `--terminal`, pass `--worktree` for that terminal; `current` means the coordinator worktree."* Truyền `id:<WT_ID>` giữ cho `terminal create` và `worker-start` nói về đúng một worktree; truyền `current` thì hai lệnh resolve **độc lập** từ cwd và có thể lệch nhau mà không báo gì.

**Không truyền `--approval-mode`.** Đo thật: `--approval-mode write` auto-approve Write/Edit nhưng **vẫn hỏi Bash** — mà lệnh `worker_done` chính là Bash, nên worker treo vĩnh viễn ở dialog approval. Config mặc định của omp đã cho qua đúng những gì cần (4/4 worker report trót lọt, gồm cả tạo file + sửa file).

> **Recipe trên KHÔNG hạn chế tool.** `omp` có `--tools=<danh sách>` / `--no-tools` / `--append-system-prompt`, và về lý thuyết đó là chỗ khôi phục lại thứ mà agent definition từng cắt hộ. Nhưng **chưa kiểm chứng** tên tool mà omp nhận, và cấm nhầm một tool cần thiết sẽ làm worker chết giữa lô. Ở v1, tool-restriction là **prose trong `[CONSTRAINTS]`**, không phải flag. Muốn nâng cấp thì đo trước trên một lô read-only rồi mới đưa `--tools` vào recipe này.

### Bảng flag — sai flag thì lệnh **im lặng fail**

| Lệnh | Chỉ định người gửi bằng |
|---|---|
| `task-create`, `worker-start`, `send`, `ask`, `reply`, `run-current`, `run-use` | `--from <handle>` |
| `check` | `--terminal <handle>` hoặc `--run <id>` — **không có `--from`** |
| `worker-stop`, `worker-release`, `terminal read`, `terminal close` | không nhận cả hai |

Nuốt stderr (`2>/dev/null`) mà truyền sai flag thì lệnh trả rỗng và trông y hệt "không có tin nhắn". Luôn kiểm tra `"ok"` trong output.

### Recover khi handle stale

`ORCA_TERMINAL_HANDLE` có thể lệch giữa phiên (session migrate, compact). Triệu chứng: mọi lệnh fail `no_active_sender_terminal`, và `check --run <id>` fail `consumer_fenced`.

Cách sửa: re-resolve handle thật từ `orca terminal list --json` — **không** truyền `--worktree`, khớp theo `title` của session — rồi truyền `--from` / `--terminal` theo bảng trên. **Không** tin env.

**Không scope lệnh này bằng `--worktree`, cả `current` lẫn `id:<WT_ID>`.** Cả hai đều sai theo hai kiểu khác nhau: `id:<WT_ID>` trả rỗng vì terminal của PM đăng ký ở `COORD_WT` chứ không ở worktree PM đang thao tác (xem *Hai worktree, không phải một*); còn `current` thì tệ hơn — handle stale hay xảy ra sau session migrate hoặc `/compact`, đúng lúc cwd dễ lệch nhất, mà `current` không bao giờ báo lỗi: nó trả về checkout cha rồi `terminal list` in ra một danh sách trông hoàn toàn bình thường của **sai worktree**.

Còn `WT_ID` dùng cho việc **đặt worker** thì lấy từ field `Worktree:` trong `brief.md`, không resolve lại bằng `current`.

### Chờ worker

`check --wait` phải chạy với `run_in_background: true` và `--timeout-ms ≤ 600000` (trần của Bash tool là 600s — đặt 900000 như ví dụ trong guide sẽ chạm trần tool trước). Dùng rolling wait, không sleep/poll. Timeout hoặc `count: 0` là **checkpoint**, không phải worker chết.

---

## Worker Contract — lane Orca

Orca **tự inject một preamble ~90 dòng** cấp sẵn lệnh `worker_done` / `heartbeat` / `ask` / `escalation` đã điền `--from` và `--dispatch-capability`. Preamble đó **thay thế** khối `STATUS/FILES_TOUCHED/SUMMARY` của lane Agent — không lặp lại nó trong prompt.

| Lane Agent | Orca native |
|---|---|
| `STATUS: DONE` | `--outcome succeeded` |
| `FILES_TOUCHED` | `--files-modified` → vào payload, có cấu trúc, PM đối chiếu ownership từ đó |
| `SUMMARY` | `--body` — preamble bắt buộc **đúng 3 câu**: đã làm gì / phát hiện gì / còn lại gì |
| `BLOCKED` + QUESTION/OPTIONS/RECOMMEND | `ask --question --options` — **blocking, giữ nguyên context** |
| `PARTIAL` | Không có outcome tương ứng. Xem ngay dưới |
| — | `--report-path` → trỏ `findings/<role>.md` |

**PARTIAL ở lane Orca — `Task` = một lô, không phải cả feature.** Outcome chỉ có `succeeded | failed`; `failed` sẽ đánh dấu Task hỏng và circuit-break sau 3 lần liên tiếp, nên không dùng nó cho việc chạm ngân sách. Cách đúng: worker gửi `worker_done --outcome succeeded` kèm **handoff note trong `--body`**, rồi PM `task-create` một Task MỚI cho phần dư. Để câu `succeeded` không phải nói dối, spec của lô **phải** ghi rõ *"làm hết phần vừa ngân sách rồi báo cáo"*.

**Ngân sách** giữ nguyên con số 60 của `pm-core.md`, nhưng **heartbeat không tính vào trần** — nó là tín hiệu liveness do preamble bắt buộc, không phải công việc. Trần ở đây không còn chặn tiền Claude (worker provider khác tốn 0 token Claude); nó chặn **runaway thời gian và chất lượng** — một worker lặp vô hạn vẫn làm treo run và vẫn đốt quota của provider kia.

**Bốn luật cứng** (đều rút ra từ kiểm chứng thật, vi phạm là treo run):

1. **PM không bao giờ viết sẵn lệnh `ask`/`worker_done` vào prompt.** Preamble cấp lệnh đã kèm capability token; lệnh trần trả `dispatch_capability_invalid`. Chỉ cần bảo worker *"dùng đúng lệnh trong preamble"*.
2. **Spec phải là MỘT dòng.** Spec nhiều dòng fail `dispatch_input` với `omp` (2/2 lần); `claude` thì nuốt được. Flatten `[TASK]` thành một dòng, giữ nguyên toàn văn, thay xuống dòng bằng dấu phân cách.
3. **Worker không được dùng `AskUserQuestion`.** Preamble Orca cấm thẳng: nó mở TUI mà coordinator không nhìn thấy → worker treo vĩnh viễn chờ người.
4. **Worker không tự nạp `.claude/rules/`.** Worker `omp` chỉ nạp `CLAUDE.md` + `AGENTS.md`. Rule nào cần thì **nêu tên file** trong `[CONSTRAINTS]` cho nó tự Read.

## Dispatch Prompt Template — biến thể Orca

Cùng bộ section của `pm-core.md`, **trừ `[CONTRACT]`** (preamble Orca đã cấp contract rồi, viết thêm là mâu thuẫn), **cộng `[ACCEPT]`**, và **thêm lại `[ROLE]` + `[ANTI-HALLUCINATION]`** — worker Orca không có persona từ `.claude/agents/` lẫn rule auto-load từ `.claude/rules/`, nên hai phần mà lane Agent bỏ đi phải quay lại đây bằng prose.

```
[SCENE] … [ROLE] … [TASK] … [OWNERSHIP] … [CONTEXT] …
[ACCEPT] Lô này được nghiệm thu khi: <checklist, mỗi dòng một điều kiện PM kiểm được từ diff>
[CONSTRAINTS] <ràng buộc thường> + đọc <rule file> trước khi bắt đầu
  + KHÔNG dùng tool spawn agent/workflow, tự làm phần việc này
  + KHÔNG dùng AskUserQuestion — cần hỏi thì dùng đúng lệnh `ask` trong preamble
[BUDGET] <N> tool call cho lô này; heartbeat không tính. Chạm trần → worker_done kèm handoff note.
[ORCA] Báo cáo bằng đúng các lệnh trong preamble ở đầu prompt, không tự chế lệnh.
[ANTI-HALLUCINATION] …
```

Bốn khác biệt bắt buộc so với template gốc:

- **Phải có `[ACCEPT]`** — checklist acceptance criteria tường minh, mỗi dòng một điều kiện kiểm được. Nó phục vụ hai phía: worker biết đích, PM có thứ để nghiệm thu. Không viết được checklist thì lô này không đủ điều kiện đi Orca.
- **Toàn bộ spec phải flatten thành MỘT dòng.** Giữ nguyên toàn văn `[TASK]`, chỉ thay xuống dòng bằng dấu phân cách. Đây là ràng buộc kỹ thuật của `dispatch_input`, không phải sở thích trình bày.
- **`[CONSTRAINTS]` phải nêu tên file rule cần đọc.** Worker Orca không auto-load `.claude/rules/` và cũng không có sẵn rule index. Vẫn **không** dán nguyên văn rule vào prompt.
- **`[CONSTRAINTS]` phải cấm tool spawn agent.** Worker Orca có nguyên bộ tool của CLI đó, kể cả tool spawn subagent — mà nested depth guard của Orca **không** chặn được thứ đó (nó chỉ đếm ở tầng `worker-start`). Một worker fan-out ngầm sẽ không hiện trong `worker-list`, tức nằm ngoài mọi accounting của PM.

## Escalation — phần khác lane Agent

Ba tầng của `pm-core.md` giữ nguyên; chỉ cơ chế đổi:

| Tầng | Lane Orca |
|------|-----------|
| 1 | Worker gọi `ask --question --options` và **đứng chờ**, giữ nguyên context. |
| 2 | PM `reply --id <msg_id>`, ghi vào `escalations.md`. **Không respawn** — worker đi tiếp ngay. |
| 3 | PM hỏi anh bằng **AskUserQuestion**, rồi `reply` câu trả lời xuống worker đang chờ. |

**Tầng 2 là đòn bẩy chi phí chính của lane này**: nó xoá hẳn vòng "worker chết → worker mới nạp lại context từ đầu". Đã kiểm chứng: sau khi `reply` trả về, worker báo lại nguyên vẹn toàn bộ tiến độ và tool result trước đó.

- Câu hỏi `ask` bị timeout thì **vẫn treo ở trạng thái pending**. Resume bằng chính message ID cũ (`ask --resume <id>`), tuyệt đối không hỏi lại câu mới — sẽ tạo ra hai luồng câu hỏi trùng nhau không phân biệt được.
- v1 **chỉ dùng `ask`**. Message type `escalation` không có cơ chế chờ chặn phía worker và ngữ nghĩa tiếp diễn của nó chưa rõ — chưa dùng cho tới khi đo được.

---

## Guardrails riêng lane Orca

- **`worker-release` trên terminal do PM tự tạo luôn trả `retained` / `processAction: none`** (2/2 lần đo). Orca chỉ tự đóng terminal do chính `worker-start` tạo ra. Recipe hai bước vì thế **bắt buộc** kèm `orca terminal close --terminal <h>`, nếu không terminal tồn đọng sau mỗi lô.
- **`release` trả `retained` không phải lỗi.** Ngoài trường hợp trên, Orca cũng giữ lại terminal mà người dùng đã chạm vào (`retainedReason: user_takeover`). Ghi nhận và đi tiếp; **không** thay bằng `terminal close` nếu receipt báo `release_pending` hoặc `release_unknown` — làm theo đúng recovery action trong receipt.
- **Worker kẹt ở prompt là không cứu được từ phía PM.** Update notice, session picker, hay dialog approval đều làm fail `agent_readiness`/`dispatch_input`; và khi đó `terminal send` trả `agent_prompt_blocked` / `terminal_not_writable`, `worker-stop` trả `processAction: none`. **Chỉ người thật gỡ được.** Đây là lý do *Precondition checklist* bắt buộc kiểm agent CLI trước khi run.
- **Không bao giờ truyền `--worktree current`.** Nó resolve theo **process cwd**, không theo env, và trong repo thì luôn tìm được checkout cha nên **không bao giờ báo lỗi** — sai worktree trông y hệt đúng. Lệnh đặt worker dùng `id:<WT_ID>` từ `brief.md`; còn tìm handle của chính PM thì **bỏ hẳn `--worktree`**. Xem *Worktree binding*.
- **Không truyền `--approval-mode` cho worker `omp`.** Xem *Recipe dispatch*.
- **Kiểm tra quota provider trước khi run.** Một CLI hết quota vẫn khởi động bình thường rồi chết ở giữa lô (quan sát thật với `codex`: *"You've hit your usage limit… try again at …"*). Không có cách nào phát hiện việc này từ `worker-start`.
- **Overhead startup của worker `--agent claude` là 62.7k**, gấp 2.66× subagent — xem `pm-evidence.md`. Con số này **chỉ có ý nghĩa khi worker là Claude**; worker provider khác thì chi phí Claude bằng 0 và phép so này không dùng để quyết định gì.

## Close-step — nguồn số khác hẳn

- **Worker provider khác (`omp`, …) không có transcript trong `~/.claude/projects/`.** Không tìm ở đó. Dòng đầu tiên của `cost.md` phải ghi thẳng: **token Claude do worker tiêu thụ = 0** — đó là mục đích tồn tại của lane này, và nó phải hiện ra thành số.
- **Worker `--agent claude` của Orca là session top-level**, nằm ở `~/.claude/projects/<slug>/<uuid>.jsonl` chứ **không** trong `<session>/subagents/`. Nhận diện bằng cách snapshot danh sách file trước/sau khi dispatch.
- **Thay cho `cache_read`, đo bằng `worker-read`** (số turn, output) và số tool call worker tự báo. Đây là số thô hơn — ghi rõ trong `cost.md` rằng nó không so trực tiếp được với số của lane Agent.
- **Resource accounting bắt buộc**: chạy `orca orchestration worker-list --json`, ghi từng dispatch là `released` hay `retained` kèm `retainedReason`, và xác nhận mọi terminal do PM tạo đã `terminal close`. Terminal tồn đọng là nợ kỹ thuật của run, phải hiện trong báo cáo.
- **Nghiệm thu accounting bắt buộc**: số lô Orca đạt ngay lần đầu, số lô phải làm lại, số lô rơi về lane Agent sau khi trượt lần hai. Đây là thước đo **duy nhất** hiện có về chất lượng model đang pin — không có nó thì mỗi run lại chọn runtime bằng cảm tính. Tỷ lệ fallback cao thì thu hẹp phạm vi Orca lại, đừng nới trần redo.

Hai bảng dưới đây nối vào cuối `cost.md` (schema chung ở `docs/010-Planning/pm-runs/README.md`) cho run có lô Orca:

```markdown
## Resource accounting — chỉ lô Orca
| Dispatch ID | Worker | released / retained | Lý do retained | Terminal đã close? |
|---|---|---|---|---|

## Nghiệm thu accounting — chỉ lô Orca
| Lô | Đạt lần đầu? | Số vòng redo | Fallback về Agent? | Điểm `[ACCEPT]` bị trượt |
|---|---|---:|---|---|

**Tổng**: <a> lô đạt lần đầu / <b> lô phải làm lại / <c> lô fallback.
```
