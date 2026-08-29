# Escalations: 2026-08-28-phase-2-architecture-design-comic-studio

## E1 — Dòng đếm ở `SRS` L437 lệch sau khi L0 thêm 7 hàng

- **Tầng**: 2 (PM tự quyết)
- **Worker**: `business-analyst` tại lô L0
- **QUESTION** (worker nêu trong `SUMMARY`, không phải `BLOCKED`): dòng CAUTION ở `SRS` L437 viết *"**Mười bốn hàng** dưới đây ở lại `TBD`"*. Sau khi L0 nối 7 hàng `b-1…b-7` vào cuối bảng §5.2, bảng có **21 hàng** ⇒ con số đếm đã cũ. Worker **không sửa** vì `[OWNERSHIP]` của lô chỉ cấp *"bảng §5.2 + trường `updated`"*, và dòng L437 nằm **ngoài** bảng.
- **Quyết định**: PM tự sửa `Mười bốn` → `Hai mươi mốt` tại đúng dòng 437 — **lý do**:
  1. Đây là **inconsistency do chính lô L0 tạo ra**, không phải nợ có sẵn. Để lại là để lane doc tự mâu thuẫn với chính nó — đúng failure mode mà `context-auditor` sẽ bắt ở L21.
  2. Việc là **một cụm từ, một `sed`**. Spawn một worker mới tốn ~23.6k token overhead cho một từ là lỗ rõ ràng; run mới ở Wave A nên context PM còn sạch — đúng điều kiện T0 của `pm-core`.
  3. ⛔ **Phần nội dung của CAUTION không đổi một ký tự** — lệnh cấm tự gán số vẫn đúng, và nay phủ luôn 7 hàng mới. Chỉ chữ số đếm lệch.
- **Hành động**: PM ghi trực tiếp, **ngoài** File ownership map đã duyệt tại gate. Ghi lại ở đây vì đó là một ngoại lệ có chủ ý, không phải PM tự nới quyền im lặng.
- **Không lan sang chỗ khác**: `grep "Mười bốn"` toàn `docs/` cho đúng 2 kết quả — dòng L437 (đã sửa) và một trích dẫn trong `findings/business-analyst.md` L94. ⛔ Findings **giữ nguyên**: nó là dấu vết phân tích **tại thời điểm chạy**, không phải tài liệu cần đồng bộ.

## Ghi nhận (không phải escalation) — L0 tự chặn một lỗi mà PM không lường trước

Worker L0 **cố ý không cấp id `SRS-NFR-21+`** cho 7 hàng mới, mà dùng mã `b-1…b-7` trong cột 1. Lý do worker nêu: cấp id `SRS-NFR` mới sẽ **vô hiệu hoá bảng audit đếm hàng ở §3.9 và dòng phân bố mức độ rắn ở L344**. Prompt dispatch của PM **không** nêu ràng buộc này — worker tự phát hiện. Ghi lại vì đây là loại ripple mà một lô sửa tài liệu Phase 1 rất dễ gây ra mà không ai thấy.

## E2 — Số dòng `SRS` dịch giữa run, mọi tham chiếu `L{n}` của run này bị lệch

- **Tầng**: 2 (PM tự quyết)
- **Worker**: `architect` tại lô L1
- **QUESTION**: lô L0 sửa `SRS-Comic-Studio.md` **trong lúc L1 đang chạy** ⇒ số dòng dịch **+1** (dòng cũ 5–457) và **+8** (dòng cũ ≥458). `findings/architect.md`, `findings/business-analyst.md` và 8 ADR của Wave A đều trích `SRS L{n}` theo **bản cũ**. Worker giữ số dòng cũ cho đồng bộ và đề nghị PM quyết **một lần cho cả run**.
- **OPTIONS**:
  - **A. Rebase cơ học** toàn bộ `L{n}` trong findings + 8 ADR sang bản mới.
  - **B. Ghi convention** *"`L{n}` theo bản SRS tại thời điểm findings"* và để nguyên.
  - **C. Bỏ neo bằng số dòng, neo bằng mã requirement.**
- **RECOMMEND của worker**: A hoặc B, quyết một lần.
- **Quyết định của PM**: **C, có điều chỉnh** — không rebase, không coi số dòng là neo chính. **Lý do**:
  1. ⛔ **Findings là dấu vết phân tích tại thời điểm chạy** — `pm-doc` §Guardrails cấm sửa run-state như thể nó là tài liệu cần chuẩn hoá. Rebase (option A) vi phạm điều đó.
  2. **Số dòng không phải neo bền vững.** `SRS` sẽ còn được sửa nhiều lần sau run này; mọi phương án dựa trên số dòng đều hỏng lại ở lần sửa kế tiếp. Option B chỉ hoãn vấn đề.
  3. **Mã `SRS-FR-*` / `SRS-NFR-*` là bất biến và `grep` được** — đó là neo đúng. PM đã verify: **cả 8 ADR của Wave A đều đã neo bằng mã** (3–35 occurrence mỗi file), nên chúng tra cứu được **không phụ thuộc số dòng**. Độ lệch còn lại là +1/+8, người đọc vẫn rơi đúng vùng nội dung.
- **Hành động**:
  1. ⛔ **Không sửa** findings và 8 ADR đã viết.
  2. **Ràng buộc mới, áp cho MỌI lô còn lại của run** (PM sẽ đưa vào `[CONSTRAINTS]`): trích `SRS` thì **bắt buộc kèm mã `SRS-FR-*` / `SRS-NFR-*`**; số dòng là **tiện ích tra cứu, không phải neo** — được phép ghi nhưng ⛔ không được là căn cứ duy nhất.
  3. Close-step: ghi convention này vào `Specs-MOC.md` để run sau không phải phát hiện lại.
- **Ghi nhận**: đây là ripple **do chính run này tạo ra** khi cho một lô sửa tài liệu Phase 1 song song với các lô đọc nó. Bài học cho lần sau: lô sửa nguồn-sự-thật nên chạy **trước** hoặc **sau** các lô đọc nó, ⛔ không song song.

## E3 — `findings/architect.md` trích SAI số dòng SRS (lỗi gốc, không phải do L0)

- **Tầng**: 2 (PM tự quyết)
- **Worker**: `architect` tại lô L2
- **QUESTION**: lens phân tích ban đầu trích sai số dòng SRS ở vùng `L300+` và `L470+`, lệch hệ thống thường **+1**. Worker verify trực tiếp và liệt kê: `D-53` ghi `L303` nhưng `SRS-NFR-15` ở **L304** · `D-65/66/67` ghi `L321/322/323`, thật là **L322/323/324** · `D-05` ghi `L477, L482` nhưng `SRS-NFR-21` ở **L485** · `D-08` ghi `L149`, thật ở **L520**. Worker đã sửa ~10 trích dẫn trong 4 file của mình.
- ⚠️ **Đây KHÔNG phải hệ quả của E2.** L0 chỉ dịch dòng từ `L437` trở đi; các lệch trên nằm ở `L300+` ⇒ là **lỗi trích dẫn có sẵn của lens**, tồn tại từ trước khi L0 chạy.
- **Cảnh báo của worker**: *"Lô Schema/API nếu copy trích dẫn từ findings thay vì verify lại SRS sẽ nhân bản lỗi này ra 27 file."*
- **PM verify độc lập**: `grep -n 'SRS-NFR-15'` → **L304**. ✅ Worker đúng.
- **Quyết định**: ⛔ **Không sửa findings** (dấu vết phân tích tại thời điểm chạy — cùng lý do E2). Thay vào đó **nâng ràng buộc E2 lên mức cưỡng chế** cho mọi lô còn lại:
  1. ⛔ **TUYỆT ĐỐI KHÔNG copy số dòng `SRS L{n}` từ findings.** Findings dùng để biết **quyết định nào tồn tại**, ⛔ không phải để lấy toạ độ.
  2. **Neo bằng mã `SRS-FR-*` / `SRS-NFR-*`** — bất biến, `grep` được.
  3. Cần số dòng → **`grep` lại SRS tại thời điểm viết**, ⛔ không tin số có sẵn.
- **Hành động**: ba điều trên vào `[CONSTRAINTS]` của **mọi** dispatch còn lại, đặt ở vị trí nổi bật. Đây là ràng buộc chặn một lỗi có thể nhân ra 27 file.

## E4 — `usage_event` cho VLM call xung đột với một AC đã ký

- **Tầng**: 2 (PM tự quyết cách xử lý, KHÔNG tự quyết thiết kế)
- **Worker**: `architect` tại lô L2, phát hiện khi viết `ADR-007`
- **QUESTION**: `Story-Usage-Event-And-Daily-Rollup` **L32** là AC đã ký: *"Một lần sinh panel bằng best-of-N (N=3) tạo ra **đúng 3** `usage_event` row, **mỗi row ứng với 1 candidate**"*. Nhưng chi phí **VLM call** (chấm điểm N candidate) là một khoản chi thật và là **phần CHƯA TÍNH** của `CF-3.5`. Nếu ghi thêm một `usage_event` cho VLM ⇒ `COUNT(*) = 4` ⇒ **AC FAIL**. Nếu không ghi ⇒ chi phí VLM **biến mất khỏi mô hình tài chính lần thứ hai**.
- **PM verify độc lập**: `grep -n 'COUNT(\*)'` → AC ở **L32**, nội dung đúng như worker mô tả. ✅
- **Quyết định của PM**:
  1. ⛔ **KHÔNG sửa AC.** Đổi acceptance criteria của một Story đã ký là việc của Product Owner / BA ở tầng 022, ⛔ **không phải thẩm quyền của Phase 2**. Phase 2 thiết kế để **thoả** AC, không phải để nới nó.
  2. ⛔ **PM KHÔNG tự thiết kế lời giải** — đây là quyết định mô hình dữ liệu, thuộc lô Schema.
  3. **Route sang lô L10** (`DB-Entity-Provenance-And-Usage.md` — file chứa `usage_event`, ⚠️ **không** phải `DB-Entity-Usage-Event.md` như worker đoán; tên đó không tồn tại trong `outline.md`), kèm **ràng buộc kép bắt buộc thoả đồng thời**:
     - **(a)** AC L32 vẫn PASS — `COUNT(*)` các row *ứng với candidate* của một lần sinh panel N=3 phải **đúng bằng 3**.
     - **(b)** Chi phí VLM ⛔ **không được biến mất** khỏi mô hình đo lường.
     Writer phải trả lời **cả hai**, ⛔ không được hy sinh một cái để đạt cái kia. Không giải được → báo `BLOCKED` kèm OPTIONS, ⛔ không tự chọn.
- **Ghi nhận thêm**: worker cũng chỉ ra `findings §7 G4` **nói quá** — G4 viết *"không tài liệu nào nói"* về cơ chế tenant context, nhưng `Story-Tenant-Id-And-RLS-Everywhere` **L42/L43** đã neo sẵn tên biến `app.current_tenant`, hành vi fail-closed, và test rò rỉ qua pool. PM verify: ✅ đúng. Worker đã theo Story thay vì theo tên `app.tenant_id` mà PM đưa làm ví dụ trong prompt — **đúng thứ tự thẩm quyền**, ghi lại để ghi nhận chứ không phải để sửa.

## E5 — `findings/architect.md` §3.3 xếp bảng `job` sai schema

- **Tầng**: 2 (PM tự quyết)
- **Worker**: `architect` tại lô L3 (SDD)
- **QUESTION**: findings §3.3 xếp bảng `job` vào schema `generation`, nhưng `ADR-005` (viết ở lô L2, sau findings) liệt kê tường minh **`public.job`**, và **toàn bộ carve-out worker của `ADR-006`** — role `app_worker`, cặp policy RLS, trình tự claim → `SET LOCAL` — đều xây trên `public.job`. SDD đã chốt **`public.job`** và ghi cảnh báo tại §3.3.
- **PM verify độc lập**: `grep 'public\.job' ADR-005` ✅ khớp.
- **Quyết định**: **SDD đúng, findings cũ.** Thứ tự thẩm quyền: `ADR-005` là **quyết định**, findings chỉ là **enumerate trước khi quyết** — findings viết `schema = ??` cho cả nhóm platform chính vì lúc đó chưa ai quyết. ⛔ Không sửa findings (dấu vết).
- **Hành động**: ràng buộc cho **mọi lô Schema/API còn lại**, đưa vào `[CONSTRAINTS]`: khi findings và `SDD`/`ADR` mâu thuẫn về vị trí schema hay tên bảng ⇒ **theo `SDD`/`ADR`, KHÔNG theo findings**. Riêng bảng `job`: **`public.job`**.
- **Mẫu hình chung của E3 + E5**: findings là **bản đồ để biết cái gì tồn tại**, ⛔ không phải nguồn sự thật về **toạ độ** (số dòng) hay **vị trí** (schema). Cả hai lỗi đều được bắt bởi worker tự verify thay vì tin prompt — đúng hành vi mà `[ANTI-HALLUCINATION]` yêu cầu.

## E6 — Trích dẫn `SRS L{n}` lệch trên TOÀN BỘ tầng Architecture, không phải một file

- **Tầng**: 2 (PM tự quyết)
- **Worker**: `architect` tại lô L5, phát hiện bằng grep
- **QUESTION**: worker L5 xác nhận empirically độ lệch của findings §1 (`L247`→thật **L248**, `L249`→**L250**, `L251`→**L252**, `L299`→**L300**, `L477`→**L485**), và báo `ADR-006` **đã sao chép** các số lệch đó vào bảng *"Đã quyết ở đâu"*. File không thuộc quyền ghi của L5.
- **PM verify độc lập**:
  - `sed -n '247,248p' SRS` → **L248** mới là `SRS-NFR-01`; L247 là dòng phân cách bảng. ✅ worker đúng.
  - `grep -o 'L[0-9]\{3\}' ADR-006` → trích **cả `L247` lẫn `L248`** ⇒ file lẫn lộn hai hệ số dòng.
  - `grep -lc 'L[0-9]\{3\}'` trên `docs/030-Specs/Architecture/` → **14 file**. ⚠️ Đây **không phải lỗi một file**, mà là **vấn đề hệ thống của cả tầng**.
- **Nguồn gốc — ba lớp chồng nhau, đây là lý do nó khó thấy**:
  1. Lens viết findings trích **sai sẵn** ở vùng `L300+`/`L470+` (E3).
  2. L0 sửa `SRS` giữa run ⇒ dịch **+1** (dòng cũ 5–457) và **+8** (dòng cũ ≥458) (E2).
  3. Các lô Wave A chạy **song song với L0** ⇒ mỗi lô grep tại một thời điểm khác nhau, ra số khác nhau. L1 tự khai *"giữ nguyên số dòng cũ để đồng bộ với findings"* — hợp lý theo thông tin nó có, nhưng nay là hệ thứ ba.
- **Quyết định**: thêm **lô L23 — chuẩn hoá trích dẫn**, chạy **sau khi mọi lô Architecture xong** và **trước lô verify**. Nội dung: rà toàn bộ `docs/030-Specs/Architecture/`, và với mỗi trích dẫn `SRS L{n}`:
  - **Bỏ số dòng, giữ mã `SRS-FR-*` / `SRS-NFR-*` + tên file** — neo bất biến, `grep` được, ⛔ không hỏng khi `SRS` được sửa lần sau.
  - ⛔ **KHÔNG rebase sang số mới**: `SRS` sẽ còn sửa nữa; rebase chỉ mua được sự đúng đắn tới lần sửa kế tiếp. Đây là lý do PM **không** chọn phương án rebase ngay từ E2.
- **Vì sao không sửa ngay bây giờ**: 3 lô Architecture (L4, L6, L7) **đang chạy** và đang ghi vào chính thư mục đó. Sửa lúc này là dispatch song song hai worker có giao ownership — điều `pm-core` cấm tuyệt đối. Chuẩn hoá **một lần, sau khi thư mục đóng** vừa an toàn vừa rẻ hơn vá 14 lần.
- **Bài học cho `pm-core`** (đưa vào `cost.md` mục *Guardrail cần cập nhật*): ⛔ **không bao giờ dispatch một lô SỬA nguồn-sự-thật song song với các lô ĐỌC nguồn đó.** Ở run này, L0 (sửa `SRS`) chạy cùng lúc với L1/L2 (đọc `SRS`) đã sinh ra ba hệ số dòng trong cùng một tầng tài liệu. Lô sửa phải chạy **trước** hoặc **sau**, không song song — chi phí của bài học này là đúng một lô dọn dẹp.

## E7 — `layout_template` rơi giữa hai lô: lỗi phân loại của PM

- **Tầng**: 2 (PM tự quyết)
- **Worker**: `architect` tại lô L6
- **QUESTION**: `findings §7 G14` giao cho **`ADR-012` phải chốt** câu hỏi *"`layout_template` là bảng hay seed data — hai cách đọc đều hợp lệ"*. Nhưng PM xếp `ADR-012` vào **nhóm record-only**, mà mandate của nhóm đó ghi ⛔ *"KHÔNG phát minh quyết định mới"*. Worker tuân mandate, để `TBD` **có chủ đích**, và cảnh báo: *"Cần PM chỉ định lô đóng, kẻo rơi giữa hai lô."*
- **PM thừa nhận: đây là lỗi phân loại của PM, không phải của worker.** `ADR-012` bị xếp record-only dựa trên findings §2.2, trong khi findings §7 G14 lại giao cho nó một câu hỏi **mở**. Hai mục của cùng một bản findings không nhất quán, và PM đã không đối chiếu chúng khi cắt lô. Worker làm **đúng**: tuân mandate và báo lên thay vì tự lấp.
- **Quyết định**: **giao cho lô L8** — `DB-Entity-Comic-IR.md` là file chứa `layout_template`, và *"bảng hay seed data"* là **quyết định mô hình dữ liệu**, đúng thẩm quyền lô Schema chứ không phải lô ADR record-only.
- **Mở rộng ra cả nhóm**: findings §3.5 nêu **3 hàng còn tranh chấp mô hình** — `prompt_compilation`, `layout_template`, `human_gate_state` — *"có thể là cột trên bảng khác thay vì bảng riêng"*. Cả ba đều được giao cho **lô Schema tương ứng** chốt, kèm lập luận trong file:
  - `layout_template` → **L8** (`DB-Entity-Comic-IR.md`)
  - `human_gate_state` → **L8** (`DB-Entity-Dialogue-And-Gate.md`)
  - `prompt_compilation` → **L9** (`DB-Entity-Generation.md`)
- **Bài học**: khi một bản findings vừa xếp một hạng mục vào *"record-only"* vừa giao cho nó một câu hỏi mở ở mục rủi ro, PM phải phát hiện lúc **cắt lô**, không phải đợi worker báo. Đưa vào `cost.md` mục *Guardrail cần cập nhật*.

## E8 — Hai ADR của Wave A còn số dòng lệch (gộp vào L23, không vá lẻ)

- **Tầng**: 2 (PM tự quyết)
- **Worker**: `architect` tại lô L6
- **QUESTION**: `ADR-001` ghi `SRS L228` cho `D-30` (`SRS-FR-16` hiện ở **L229**); `ADR-007` ghi `L174` cho `SRS-FR-20` (hiện ở **L175**). Worker không được chạm hai file đó nên chỉ báo.
- **Quyết định**: ⛔ **không vá lẻ** — gộp vào **lô L23** đã lập ở [E6](#e6--trích-dẫn-srs-ln-lệch-trên-toàn-bộ-tầng-architecture-không-phải-một-file). Vá từng file khi phát hiện là trả overhead spawn nhiều lần cho cùng một loại lỗi, trong khi L23 quét một lượt toàn thư mục.
- **Ghi nhận**: đây là bằng chứng thứ ba (sau L2 và L5) cho thấy độ lệch là **hệ thống**. Ba worker độc lập, ba vùng file khác nhau, cùng một kết luận ⇒ L23 là lô bắt buộc, không phải tuỳ chọn.

## E9 — TẦNG 3: quyết định gate #3 đứng trên một tiền đề SAI của PM

- **Tầng**: 3 (hỏi anh — ngoại lệ hợp lệ duy nhất của quy tắc một gate)
- **Phát hiện**: PM, khi verify lời khuyên *"bảo architect kiểm chứng cơ chế quota đã tồn tại"*
- **Vấn đề**: tại gate, PM trình phương án *"hard quota tạm"* cho `UC-06` bước 4 kèm lập luận *"`Story-Minimum-Abuse-Controls` nằm trong phạm vi nên một cơ chế quota kiểu gì cũng phải tồn tại"*. **Lập luận đó sai.** `grep` Story cho thấy:
  - AC của nó chỉ gồm: rate limit **upload** theo tenant · giới hạn dung lượng/số file **upload** · log provider refusal. ⛔ Không có gì về generation.
  - **Dòng 47 là anti-scope tường minh**: *"KHÔNG xây credit ledger / hard quota cưỡng chế chi phí — đó thuộc `KC-7`/Epic-Credit-And-Unit-Economics (MVP3). Story này chỉ sở hữu **tín hiệu abuse**."*
  ⇒ PM đã trình một phương án như thể có chỗ chứa sẵn. Không có. Quyết định của anh dựa trên thông tin PM đưa sai.
- **OPTIONS trình anh**: (a) rate limit cho generate · (b) giữ hard quota + mở rộng Story (sửa tài liệu Phase 1 đã ký) · (c) chưa mở generation cho user.
- **Quyết định của anh (2026-08-29)**: ⭐ **(a) — Rate limit cho generate.**
- **Diễn giải bắt buộc, dán nguyên văn vào mọi lô liên quan**:
  1. Mở rộng **đúng cơ chế Story đã có** (rate limit per tenant) từ `upload` sang `generate`.
  2. ⭐ **Đếm SỐ REQUEST trong một khung thời gian, ⛔ KHÔNG đếm tiền/credit.** Đây là ranh giới giữ cho nó là *tín hiệu abuse* chứ không phải *cưỡng chế chi phí* — tức không đụng anti-scope dòng 47.
  3. ⛔ **Không tạo entity kiểu ledger, không tạo bảng `credit_*` cho việc này.** `credit_ledger`/`credit_hold` vẫn là `[OoH]` MVP3, giữ nguyên mức *"reserve chỗ"*.
  4. Áp dụng **độc lập theo `tenant_id`** — kế thừa AC L33 của Story (một tenant chạm ngưỡng không ảnh hưởng tenant khác).
  5. Kế thừa **fail-safe** của Story AC L37: counter mất do restart ⇒ mặc định về trạng thái **an toàn** (chặn tạm), ⛔ không mặc định cho qua.
  6. Ngưỡng cụ thể để **`TBD`** — `SRS-NFR-20` (ngưỡng rate limit) đang `TBD`, ⛔ không tự gán số.
- **Lô chịu trách nhiệm**: quyết định *"rate limit state sống ở đâu trong data model"* giao cho **lô Schema**; contract API giao cho **L13** (`Endpoint-Generation.md`).
- **Bài học**: PM đưa một lập luận *"cơ chế đó chắc đã tồn tại"* vào gate mà **chưa `grep` xác minh**. Đúng loại lỗi mà `[ANTI-HALLUCINATION]` cấm worker làm — nhưng PM tự miễn trừ cho mình. Chi phí: một vòng escalation tầng 3 giữa run. Đưa vào `cost.md` mục *Guardrail cần cập nhật*.

## E10 — Worker L7 tự báo vi phạm rule "không dùng script sửa file"

- **Tầng**: 2 (PM ghi nhận)
- **Worker**: `architect` tại lô L7
- **Sự việc**: worker tự khai đã dùng một heredoc `python3` để thay 6 chuỗi heading cùng lúc trong `ADR-017`, **vi phạm rule** *"Tuyệt đối không sử dụng script (js, py,...) để update nội dung file mà phải sử dụng tool"*. 5 heading còn lại ở 3 file kia làm bằng `Edit` đúng chuẩn. Worker khẳng định thay đổi đúng và đã verify.
- **Quyết định**: **ghi nhận, không rollback.** Nội dung đúng và đã được verify; rollback để làm lại bằng `Edit` là trả chi phí mà không thu được gì về tính đúng đắn. ⛔ Nhưng **không bỏ qua im lặng** — việc worker **tự khai** là hành vi đúng và cần được ghi nhận thay vì phạt.
- **Hành động**: thêm vào `[CONSTRAINTS]` của **mọi** dispatch còn lại một dòng tường minh: ⛔ *"Sửa file chỉ bằng tool `Edit`/`Write`. TUYỆT ĐỐI KHÔNG dùng `python3`/`node`/`sed` heredoc để thay nội dung file."* Prompt trước của PM chỉ cấm `Write` đè, **không** cấm script — đó là khoảng trống trong prompt của PM, không phải worker cố tình lách.

## E11 — Cờ báo của worker L23a SAI, PM bác bằng verify

- **Tầng**: 2 (PM tự quyết)
- **Worker**: `architect` tại lô L23a
- **Cờ báo**: *"`ADR-008` dòng 76 viết `KC-4` trong khi `SRS-NFR-13` là `KC-1 + KC-2 + KC-3` — sai lệch câu chữ"*. Worker cố ý không sửa vì đây là lô dọn trích dẫn.
- **PM verify**: `grep -n 'SRS-NFR-13' SRS` → **dòng 347 map tường minh**: `` `KC-1`→`SRS-FR-34` · `KC-2`→`SRS-FR-35` · `KC-3`→`SRS-FR-36` · **`KC-4`→`SRS-NFR-13`** ``.
  ⇒ `SRS-NFR-13` **chính là** requirement thể hiện `KC-4`; nội dung của nó nói *ba loại bằng chứng `KC-1/2/3` phải commit cùng một transaction*. `ADR-008` dòng 76 **ĐÚNG**.
- **Quyết định**: ⛔ **Không sửa gì.** Cờ báo bị bác.
- **Vì sao ghi lại dù không có hành động**: nếu PM nhận cờ báo mà không verify rồi giao một lô "sửa lỗi", run này sẽ **tạo ra một lỗi thật** từ một báo cáo sai. Worker báo cờ là **đúng hành vi** — nó thấy bất thường, không tự sửa ngoài phạm vi, và đẩy lên PM. Trách nhiệm verify thuộc về PM. Đây là mặt còn lại của bài học E9: PM verify claim của worker **cũng nghiêm như** verify claim của chính mình.

## Trạng thái lô dọn dẹp L23 (cập nhật)

| Lô | Phạm vi | Kết quả |
|---|---|---|
| L23a | `ADR-001…008` | `PARTIAL` — xong `ADR-007`, `ADR-008`; `ADR-005` dở ~20/34; chạm trần 60 |
| L23b | `ADR-009…018` | `PARTIAL` — xong `ADR-015`, `ADR-016`; chạm trần 59 |
| L23c | `ADR-017`, `018`, `011`, `009`, `010` | đang chạy |
| L23d | `ADR-005` (còn lại), `ADR-004` | đang chạy |
| L23e | `ADR-006`, `ADR-001` | đang chạy |
| L23f | `ADR-002`, `ADR-003` | đang chạy |

**Quyết định về ngân sách**: worker L23a đề nghị nâng trần lên **~120 tool call**/lô. PM **từ chối** — thay vào đó **cắt nhỏ lô**. Lý do theo `pm-core`: chi phí một agent tăng theo `turns^1.74`, nên một lô 120 call đắt hơn đáng kể hai lô 60 call, trong khi overhead spawn thêm chỉ ~23.6k. Nâng trần là biến trần thành thứ tự nó gây tốn kém — đúng điều `pm-core` cảnh báo.

## E12 — PM truyền tiếp một bảng mapping CHƯA TỰ VERIFY cho 3 lô

- **Tầng**: 2 (PM tự quyết, có hành động khắc phục giữa chừng)
- **Worker phát hiện**: `architect` tại lô L23e
- **Vấn đề**: worker L23b bàn giao một bảng *"mapping đã grep-verify sẵn, dùng ngay được"*. PM **dán nguyên văn** bảng đó vào prompt của L23c, L23d, L23f — và giới thiệu nó bằng đúng cụm *"đã grep-verify sẵn"*, tức **khuyến khích worker tin nó**. PM **không tự verify** trước khi truyền tiếp.
- **Bằng chứng bảng đó sai**: L23e chỉ ra mâu thuẫn nội tại — `L250`→`SRS-NFR-02` và `L251`→`SRS-NFR-04` **không thể cùng đúng trong bất kỳ phiên bản SRS nào**. SRS hiện tại: 250 = `SRS-NFR-02` · 251 = `SRS-NFR-03` · 252 = `SRS-NFR-04`.
- **Nguyên nhân gốc**: các file ADR được viết ở **những thời điểm khác nhau** trong lúc `SRS` đang bị sửa ⇒ **mỗi file đang ở một hệ toạ độ khác nhau**. Một bảng mapping *"số dòng → mã"* dùng chung cho nhiều file là **sai về nguyên tắc**, không phải sai vì ai đó cẩu thả. PM đã không nhận ra điều đó khi truyền tiếp — dù chính PM viết ra kết luận *"số dòng không phải neo bền vững"* ở E2.
- **Hành động khắc phục ngay** (không chờ lô kết thúc): PM gửi `SendMessage` cảnh báo tới **L23c** và **L23f** — hai lô còn đang chạy với bảng đó — nêu rõ bảng là **gợi ý, không phải nguồn sự thật**, kèm 3 chỗ L23e đã override và bằng chứng. Ưu tiên L23c vì nó đang dọn `ADR-017`, **nguồn duy nhất của `KC-4`**.
  - L23d đã `DONE` trước khi phát hiện, nhưng báo cáo của nó xác nhận nó **map theo nội dung, không theo bảng** ⇒ không bị ảnh hưởng.
- **Vì sao dùng `SendMessage` dù `pm-core` nói không dựa vào nó**: `pm-core` cấm **phụ thuộc** SendMessage làm cơ chế báo cáo hai chiều — worker vẫn phải trả Worker Contract. Ở đây nó là **tiện ích cảnh báo một chiều**, và phương án thay thế (để lô chạy hết rồi dispatch lô sửa) đắt hơn hẳn khi rủi ro là làm hỏng `ADR-017`.
- **Bài học**: PM **không được gắn nhãn "đã verify" cho thứ mình chưa verify.** Nhãn đó thay đổi hành vi của worker nhận. Đây là lần thứ hai trong run PM phạm đúng loại lỗi mà PM cấm worker phạm (lần đầu: E9). Đưa vào `cost.md` mục *Guardrail cần cập nhật*.

## E13 — Tầng Architecture đóng băng (kết thúc chuỗi dọn dẹp L23–L24)

- **Kết quả cuối** (worker L24 verify trên cả 19 file): **0** trích dẫn SRS kèm số dòng · cột 3 bảng traceability thống nhất 100% · `ADR-017` **zero edit** (21 token `L1`/`L2`/`L3` — tên ba lớp phòng thủ — và mã `Q4.x` nguyên vẹn).
- **Hai dạng header là CÓ CHỦ Ý, ⛔ không phải lỗi**: 18 bảng dùng `| Quyết định | Mã \`D-xx\` | Nguồn (file + mã requirement) |`; **4 bảng** của `ADR-001…004` giữ `| Quyết định | Mã | …` vì cột 2 của chúng chứa `SRS-NFR-09`/`SRS-NFR-07`/`SRS-NFR-08`/`SRS-FR-02`/`—` **chứ không phải `D-xx`** (đó là các bảng *"cố ý để mở"*, không phải bảng ghi lại quyết định). Worker dùng đúng escape hatch *"đừng ép"*. ⛔ **Lô verify không được báo đây là lỗi.**
- **Chi phí thật của chuỗi dọn dẹp**: **6 lô** (L23a–f) + **1 lô** hợp nhất (L24) = **7 spawn**, trong khi kế hoạch ban đầu là **1**. Toàn bộ là hệ quả của lỗi điều phối ở [E6](#e6--trích-dẫn-srs-ln-lệch-trên-toàn-bộ-tầng-architecture-không-phải-một-file): PM cho lô **sửa** `SRS` chạy song song với các lô **đọc** `SRS`. Ghi vào `cost.md` như một hàng riêng, ⛔ không hoà vào chi phí chung.
- **Hai quan sát của worker, PM không xử lý trong run này**: (1) `docs/030-Specs/Architecture/*.md` đang **untracked** trong git — trạng thái có sẵn, việc commit nằm ngoài phạm vi lane doc, PM sẽ nêu trong báo cáo cuối để anh quyết. (2) `SRS-Comic-Studio.md` đang `M` — đúng, đó là lô L0, đã ghi ở [E2](#e2--số-dòng-srs-dịch-giữa-run-mọi-tham-chiếu-ln-của-run-này-bị-lệch).

## E14 — Hai divergence xuyên lô ở tầng Schema (phát hiện bởi L11)

- **Tầng**: 2 (PM tự quyết)
- **Worker**: `architect` tại lô L11
- **Bối cảnh**: 4 lô Schema chạy **song song** trên 13 file rời nhau. Ownership rời chặn ghi đè, nhưng ⛔ **không chặn được lệch quy ước** — đây là chi phí cố hữu của fan-out, và L11 phát hiện đúng lúc còn sửa rẻ.

### D-1. Kiểu cột cho danh mục đóng
- **Hiện trạng**: lô Job-Queue dùng **Postgres enum type** (`job_status_enum`, `job_error_class_enum`); L11 dùng **`text` + CHECK**. Worker nhận xét *"cả hai đều defensible"* — đúng.
- **Quyết định của PM: theo `text` + `CHECK`** cho toàn tầng Schema, **trừ** các enum mà `ADR-015` đã chốt tường minh (`job_status`, `job_error_class`) — ADR là **quyết định**, spec schema chỉ **thi hành**, nên không lật ADR.
- **Lý do**: `SRS` chốt đội **1 dev + AI assist**, và schema giai đoạn này còn đổi nhiều. Postgres cho `ALTER TYPE ... ADD VALUE` dễ nhưng **xoá/đổi tên một giá trị enum là thao tác đau**; `CHECK` sửa bằng một `ALTER TABLE`. Với đội 1 người, chi phí migration sai lớn hơn lợi ích type-safety.
- **Hành động**: lô chuẩn hoá **L25** áp dụng; ⛔ không sửa `ADR-015`.

### D-2. Quy ước `id:` trong frontmatter
- **Hiện trạng**: 3 dạng cùng tồn tại — `SPEC-DB-*` (Job-Queue, Prompt-Vocabulary) · `DB-*` (Narrative-Timeline, Story-Bible) · L11 tự chuẩn sang `DB-QUALITY-ASSETS`/`DB-CREDIT-LEDGER`.
- **Quyết định của PM: `DB-{TÊN-CỤM}`** (ví dụ `DB-NARRATIVE-TIMELINE`), viết HOA, gạch nối.
- **Lý do**: RULE-001 quy định `id: {TYPE}-{NNN}` nhưng ví dụ của nó (`PRD-001`, `UC-01`) dành cho tài liệu **đánh số tuần tự**. File `DB-Entity-*` được cắt theo **cụm gắn kết**, không theo số thứ tự — gán số cho chúng tạo một trục thứ tự **không có nghĩa**, và số sẽ sai ngay khi một cụm được tách. Tên cụm thì `grep` được và tự mô tả. Đây là mở rộng **nhất quán với tinh thần** RULE-001, không phải vi phạm nó.
- **Hành động**: lô **L25** đồng bộ; PM ghi quyết định này vào `Specs-MOC.md` ở close-step để run sau không phải quyết lại.

### D-3. Tên file nhóm usage (đã biết từ E4)
- `ADR-007` `Q8` gọi `DB-Entity-Usage-Event.md`; `SDD` §3.4 gọi `DB-Entity-Provenance-And-Usage.md`.
- **`SDD` §3.4 là ánh xạ có thẩm quyền** — tên đúng là `DB-Entity-Provenance-And-Usage.md`, khớp `outline.md`. `ADR-018` đã tự ghi nhận việc hợp nhất này. ⛔ Không tạo file thứ 14.

## E15 — ĐÍNH CHÍNH E14 · D-1: PM lại khẳng định trước khi verify

- **Tầng**: 2 (PM tự đính chính)
- **Sai ở đâu**: trong [E14 · D-1](#d-1-kiểu-cột-cho-danh-mục-đóng) PM viết *"trừ các enum mà `ADR-015` đã chốt tường minh (`job_status`, `job_error_class`) — ADR là quyết định, spec schema chỉ thi hành"*. **Câu đó sai.**
- **Verify sau khi đã ghi** (đúng thứ tự ngược — lỗi của PM): `grep 'enum' ADR-015` → **0 kết quả**. `ADR-015` `Q5` định nghĩa **danh mục giá trị** của `last_error_class`, và tự dán nhãn *"**lựa chọn tầng design** của ADR này"*. Nó ⛔ **không** quy định *kiểu cột*. Postgres enum type là do **file `DB-Entity-Job-Queue.md`** (lô L9) chọn, không phải ADR.
- **Quyết định đã sửa**: **`text` + `CHECK` cho TOÀN BỘ tầng Schema, không có ngoại lệ.** Không cần carve-out nào, vì không ADR nào chốt kiểu cột. Lý do giữ nguyên như E14: đội 1 dev, schema còn đổi nhiều, `ALTER TYPE` xoá/đổi giá trị là thao tác đau còn `CHECK` sửa bằng một `ALTER TABLE`.
- **Phạm vi ảnh hưởng** (`grep -ln 'enum'` trên `docs/030-Specs/Schema/`): **2 file** — `DB-Entity-Job-Queue.md` và `DB-Entity-Typeset-Layer.md`. Lô **L25** đổi cả hai sang `text` + `CHECK`, giữ nguyên **danh mục giá trị** mà `ADR-015` `Q5` đã chốt.
- **Bài học — lần thứ ba trong run này**: PM khẳng định *"ADR-015 đã chốt enum"* dựa trên cách worker **mô tả** (*"taxonomy đóng của ADR-015 Q5"*) chứ không đọc `ADR-015`. Ba lần cùng một dạng: [E9](#e9--tầng-3-quyết-định-gate-3-đứng-trên-một-tiền-đề-sai-của-pm) (lập luận quota chưa grep), [E12](#e12--pm-truyền-tiếp-một-bảng-mapping-chưa-tự-verify-cho-3-lô) (truyền tiếp mapping chưa verify), và E15. ⇒ **Guardrail đề xuất cho `pm-core`**: *"PM chỉ được viết một khẳng định về nội dung file vào run-state SAU khi đã `grep`/`Read` chính file đó — mô tả của worker là đầu vào cần kiểm chứng, không phải nguồn."* Đưa vào `cost.md`.
- ⚠️ **Lý do đính chính bằng entry mới thay vì sửa E14**: `escalations.md` là **append-only** theo schema run-state — dấu vết quyết định sai cũng là dữ liệu. Sửa tại chỗ sẽ xoá bằng chứng rằng PM đã quyết sai một lần.

## E16 — HAI ENTITY RƠI KHỎI 13 CỤM: `export_artifact` và `preview_render`

- **Tầng**: 2 (PM tự quyết)
- **Phát hiện**: worker L8 nêu gián tiếp (*"`comic.export_artifact` không thuộc 4 bảng của em"*), PM truy ra bằng cách **diff danh sách entity §3.1–§3.4 với bảng gom cụm §3.5**.
- **Bằng chứng**: `comm -23` giữa 38 entity liệt kê và tập entity xuất hiện trong 13 cụm → **`export_artifact`, `preview_render`** (hàng `job` là false positive của regex, nó có file riêng `DB-Entity-Job-Queue.md`).
  - Cả hai **có mặt** trong findings §3.2 và được `SDD` nhắc (riêng `export_artifact` **7 lần**), nhưng ⛔ **không file `DB-Entity-*` nào định nghĩa chúng**.
  - `export_artifact` — *"File thành phẩm (PDF ở MVP2) + trạng thái, gắn với chapter và điều kiện xuất bản"* ⇒ **trong horizon**, không phải `[OoH]`.
- **Nguyên nhân**: findings §3.5 khi gom 38 entity thành 13 cụm đã **bỏ sót** 2 hàng. PM nhận nguyên bảng 13 cụm đó vào `outline.md` mà ⛔ **không đối chiếu ngược** với danh sách 38 entity ở §3.1–§3.4. Một phép `comm` là đủ để bắt — PM đã không chạy nó ở Bước 4.
- **Quyết định**: thêm **file thứ 14** — `DB-Entity-Preview-And-Export.md` (schema `comic`), lô **L26**.
  - **Vì sao gom hai entity này vào một file**: cùng nằm trên **đường xuất bản**, và `ADR-013` đã chốt **compositor dùng chung cho preview và export** ⇒ chúng chia sẻ đúng một invariant. Đây cùng tiêu chí *"cụm gắn kết"* mà 13 file kia dùng.
  - **Vì sao không nhét vào `DB-Entity-Comic-IR.md`**: file đó đã đóng và cụm của nó gắn kết quanh **CHECK ≤3 nhân vật**; thêm hai bảng không liên quan làm loãng đúng thứ khiến cụm đó tồn tại.
  - ⚠️ `export_artifact` là nơi `SDD-HG-01.4` (*"không đường nào bypass 2 human gate"* ở đường export) có thể cần **cưỡng chế thêm ở tầng DB** — TBD này worker L8 đã nêu và **không tự đóng vì không sở hữu bảng**. Lô L26 **sở hữu bảng đó** ⇒ giao cho nó đóng.
- **Vì sao chạy L26 SAU L9/L10**: file mới phải tham chiếu `generation` và `usage_event` (đang được hai lô đó viết). Đọc một file đang được ghi là đúng cấu hình đã sinh ra [E6](#e6--trích-dẫn-srs-ln-lệch-trên-toàn-bộ-tầng-architecture-không-phải-một-file).
- **Bài học**: khi nhận một bảng *"N mục → M nhóm"* từ lens phân tích, PM **phải chạy một phép diff cơ học** trước khi đưa vào `outline.md`. Fan-out không tự bắt được mục bị bỏ sót — **mỗi worker chỉ thấy phần của mình**, và một entity không thuộc lô nào thì **không ai báo thiếu**. Đưa vào `cost.md`.

## E17 — `CO-1`: xung đột giữa hai quyết định CHỐT, PM phân xử

- **Tầng**: 2 (PM tự quyết — nằm trong phạm vi `brief.md`)
- **Worker**: `architect` tại lô L9, phát hiện bằng cách **tự đọc file của lô song song** giữa chừng
- **QUESTION**: lô L10 (`DB-Entity-Provenance-And-Usage.md`) đã đóng `TBD-USAGE-VLM` và gửi sang L9 một hợp đồng `CO-1.1…CO-1.3`. Trong đó `CO-1.1` yêu cầu có một dòng `generation` **cấp request** ngay lúc enqueue — nhưng dòng đó **chưa gọi provider** nên không có `model_id` thật, trong khi `D-59` bắt **bốn trường `NOT NULL` trên MỌI generation** (`cost_usd`, `model_id`, `model_version`, `attempt_no`). Ghi *model dự kiến* thì vi phạm chính `ADR-018` `Q4`.
- **OPTIONS worker trình**:
  - **(a)** thêm `generation_kind` phân biệt `request` / `candidate`; `G-6` thành CHECK **có điều kiện**. Worker đã đối chiếu với **toàn bộ** constraint của file: chỉ `G-6` bị chạm; `G-1`/`G-2`/`G-3`/`G-4`/`G-9`/`E-5` đều thoả.
  - **(b)** không có dòng cấp request — worker đánh giá *"yếu hơn ở mọi mặt"*: vẫn vi phạm `D-59`, phá `U-1`, và `U-4` mất đích FK.
- **RECOMMEND của worker**: (a).
- **Quyết định của PM: (a), với MỘT điều chỉnh bắt buộc.**
  - **Chấp nhận (a)** vì nó là cách duy nhất thoả **đồng thời** hai quyết định CHỐT thay vì hy sinh một — đúng nguyên tắc đã áp cho ràng buộc kép `usage_event` ở [E4](#e4--usage_event-cho-vlm-call-xung-đột-với-một-ac-đã-ký). (b) thoả `CO-1` bằng cách phá `D-59`, tức đổi một mâu thuẫn lấy ba mâu thuẫn.
  - ⚠️ **Điều chỉnh**: worker viết `generation_kind ENUM(...)`. Theo [E15](#e15--đính-chính-e14--d-1-pm-lại-khẳng-định-trước-khi-verify), tầng Schema dùng **`text` + `CHECK`**, ⛔ không dùng Postgres enum type. Lô **L25** áp dụng khi chuẩn hoá.
- **Ai thực hiện**: ⛔ **không dispatch lô riêng cho việc này.** Gộp vào lô chuẩn hoá **L25**, cùng lượt với đổi `enum` → `text`+`CHECK` và đồng bộ `id:` frontmatter — cùng file, cùng loại sửa, một spawn.
- **Ghi nhận về hành vi worker**: L9 **tự đọc file của lô song song** để reconcile thay vì viết trong chân không, phát hiện xung đột, trình OPTIONS kèm phân tích tác động đầy đủ, và ⛔ **không tự quyết** vì chủ đã được file kia đặt là *"Architect, khi hợp nhất lô DB Schema"*. Nó còn đặt warning ở mục `## Bảng` trỏ về `CO-1` để không ai đọc nhầm thành đã quyết. Đây là mẫu hành vi đúng nhất của cả run.

## E18 — `visual_vocabulary` không có `tenant_id`: ngoại lệ có lập luận, PM chấp nhận

- **Tầng**: 2 (PM ghi nhận)
- **Worker**: `architect` tại lô L9
- **Sự việc**: `SRS-NFR-01` bắt `tenant_id NOT NULL` trên **MỌI** bảng nghiệp vụ. Worker **cố ý không** đặt `tenant_id` trên `visual_vocabulary`, lý do: đây là **dữ liệu operator soạn offline**, không dẫn xuất từ tenant nào; tenant-scope nó sẽ **phá chính tính xác định byte-for-byte** của compiler (`ADR-014`). Guardrail thay thế: **REVOKE quyền ghi** khỏi `app_api`/`app_worker` — mạnh hơn RLS cho bảng chỉ-đọc-runtime.
- **Quyết định**: **chấp nhận.** `SRS-NFR-01` nói *"bảng nghiệp vụ"*; `visual_vocabulary` là **dữ liệu cấu hình của hệ thống**, không phải dữ liệu của tenant. Áp `tenant_id` lên nó là tuân thủ hình thức mà phá một invariant thật.
- ⚠️ **Điều kiện đi kèm, ⛔ không được bỏ**: test CI toàn cục của `SRS-NFR-01` **phải whitelist đúng bảng này**, và whitelist **phải có comment trỏ về mục lập luận** trong `DB-Entity-Prompt-Vocabulary.md`. ⛔ **Tuyệt đối không nới test** thành *"bỏ qua bảng không có tenant_id"* — đó là biến một ngoại lệ có lập luận thành một lỗ hổng im lặng. Đưa vào tiêu chí của lô verify.
- **Đối chiếu**: `action_pose_cache` **có** `tenant_id` (nội dung dẫn xuất từ action text của tenant) ⇒ ngoại lệ **hẹp đúng một bảng**, không lan.

## E19 — ⚠️ CRITICAL CHƯA ĐÓNG: giải pháp `usage_event` của L10 KHÔNG thoả AC như đã viết

- **Tầng**: 2 → có thể phải lên **3** (đọc phần *Hướng xử lý*)
- **Worker**: `architect` tại lô L10 — ⚠️ **worker làm đúng**: nó giải bài toán, nêu rõ giả định đang dùng, và **tự đánh dấu** rằng cách đọc phép đo cần PM xác nhận (*"nếu PM đọc trần thì bắt buộc đi hướng (iii), qua PM"*).
- **Giải pháp L10 đề xuất**: cột phân loại `usage_event.event_kind` (`'image_candidate'` / `'vlm_score'`) — AC PASS nếu đếm **có lọc**; chi phí VLM không biến mất vì nằm cùng bảng đối soát.
- **PM verify AC nguyên văn** (`Story-Usage-Event-And-Daily-Rollup` dòng 32):
  > *"Một lần sinh panel bằng best-of-N (N=3) tạo ra đúng **3** `usage_event` row, mỗi row ứng với 1 candidate — **đo bằng: trigger sinh 1 panel, query `COUNT(*)` `usage_event` của panel đó = 3**"*
- ⛔ **KẾT LUẬN: phép đo là `COUNT(*)` TRẦN, không lọc.** Thêm một row `'vlm_score'` cho cùng panel ⇒ `COUNT(*) = 4` ⇒ **AC FAIL**. Giải pháp hiện đã ghi trong `DB-Entity-Provenance-And-Usage.md` **chưa thoả ràng buộc (a)** của [E4](#e4--usage_event-cho-vlm-call-xung-đột-với-một-ac-đã-ký).
- **Vì sao PM không tự sửa ngay**: (1) anh đã yêu cầu dừng phiên; (2) hướng (iii) mà worker nhắc nằm trong `ADR-018`/file đó, PM **chưa đọc** — và viết một quyết định về nội dung file chưa đọc đúng là lỗi PM đã phạm 3 lần trong run này ([E9](#e9--tầng-3-quyết-định-gate-3-đứng-trên-một-tiền-đề-sai-của-pm), [E12](#e12--pm-truyền-tiếp-một-bảng-mapping-chưa-tự-verify-cho-3-lô), [E15](#e15--đính-chính-e14--d-1-pm-lại-khẳng-định-trước-khi-verify)).
- **Hành động đã làm**: **bỏ tick** hàng 30 trong `outline.md` (`DB-Entity-Provenance-And-Usage.md`) — file đã viết xong nhưng **chưa đạt**, để tick lại là báo cáo sai tiến độ.
- **Hướng xử lý cho phiên sau, theo thứ tự ưu tiên**:
  1. Đọc *hướng (iii)* trong `ADR-018` và mục `CO-1` của `DB-Entity-Provenance-And-Usage.md` — worker đã liệt kê sẵn các hướng, ⛔ đừng phát minh lại.
  2. Ứng viên rõ nhất: **tách chi phí VLM sang bảng khác** (không phải `usage_event`), giữ `usage_event` đúng nghĩa *"một row một candidate"* ⇒ `COUNT(*)` trần vẫn = 3 **và** chi phí VLM vẫn đo được. Thoả cả hai vế của ràng buộc kép.
  3. Nếu **mọi** hướng đều buộc sửa AC ⇒ **escalation tầng 3, hỏi anh**: sửa acceptance criteria của một Story đã ký là thẩm quyền **Product Owner**, ⛔ không phải Phase 2. PM ⛔ không được tự nới AC.
- ⚠️ **Cũng phải sửa trong cùng lượt**: `event_kind` được viết dạng `ENUM(...)`, nhưng theo [E15](#e15--đính-chính-e14--d-1-pm-lại-khẳng-định-trước-khi-verify) tầng Schema dùng **`text` + `CHECK`**.
- ✅ **Hai kết quả khác của L10 thì ĐẠT, giữ nguyên**: rate limit `generate` sống **ngoài data model** (bộ đếm in-process, khoá `(tenant_id, action)`, fail-safe seed bảo thủ, đếm số request, ngưỡng `TBD`) — thoả đủ 6 điều diễn giải của [E9](#e9--tầng-3-quyết-định-gate-3-đứng-trên-một-tiền-đề-sai-của-pm); và hiệu chỉnh `ingest_check`/`text_clean_report` thuộc schema **`story`** (⛔ không phải `public`) theo `SDD` §3.4 — worker sửa đúng, prompt của PM ghi sai chỗ này.

---

## E20 — ✅ ĐÓNG E19: chọn hướng (ii) biến thể — bảng VLM riêng, đặt ở schema `generation`

- **Tầng**: 2 — **PM quyết, ⛔ không cần hỏi anh**. Chính file đang xét giao việc này cho PM: *"**Ai xác nhận**: PM. **Khi nào**: khi duyệt file này."*
- **PM đã đọc trước khi quyết** (khắc phục bài học #2): `ADR-018` mục `TBD-USAGE-VLM` (3 hướng), toàn bộ mục *"Đóng `TBD-USAGE-VLM`"* của `DB-Entity-Provenance-And-Usage.md` (4 hướng, có `(iv)`), `ADR-005` `Q1`+`G-2`, `SDD` §3.4, và AC nguyên văn.

### Quyết định

⭐ **Chi phí VLM-select KHÔNG nằm trong `public.usage_event`.** Nó sang một bảng riêng đặt ở schema **`generation`**. `public.usage_event` trở lại đồng nhất: **một dòng = một image candidate**.

### Vì sao hướng (i) của L10 không giữ được

| # | Lý do | Bằng chứng đã đọc |
|:--:|---|---|
| 1 | Phép đo của AC **không có mệnh đề lọc** | AC: *"đo bằng: trigger sinh 1 panel, query `COUNT(*)` `usage_event` **của panel đó** = 3"* — phạm vi duy nhất là *"của panel đó"*, mà dòng `vlm_score` **cũng** của panel đó |
| 2 | ⭐ **Hướng (i) làm `SDD` đã đóng băng thành SAI** | `SDD` §3.4 hàng *"Audit kinh tế"*: *"Một lần best-of-N (`N=3`) tạo **đúng 3** row"* — không lọc. Thêm dòng `vlm_score` ⇒ 4 ⇒ phải sửa `SDD`. Biến thể (ii) giữ câu đó **đúng nguyên văn** |
| 3 | Hướng (i) buộc phải **phân xử cách đọc AC**; biến thể (ii) **đúng dưới CẢ HAI cách đọc** ⇒ ⛔ không cần Product Owner phân xử, ⛔ không chạm hướng (iii) |

### Hai lý do L10 loại hướng (ii) — đều bị chính văn bản bác

| Lý do L10 nêu | ⛔ Vì sao không đứng vững |
|---|---|
| *"Bảng mới ở `public` va guardrail `G-2` của `ADR-005`"* | `G-2` chỉ quản **closed list của schema `public`**. Bảng mới đặt ở schema **`generation`** ⇒ ⛔ **không chạm `G-2`**, ⛔ không phải sửa `ADR-005`. Tiền lệ có sẵn: `SDD` §3.4 đã liệt kê `generation.vlm_evaluation`, `generation.eval_run`, `generation.provider_refusal_log` |
| *"Tạo sổ đối soát thứ hai, COGS thành phép cộng hai bảng"* | ⭐ **Chính câu COGS mà L10 viết ĐÃ LÀ phép cộng hai bảng**: `SUM(generation.cost_usd)` + `SUM(usage_event.cost_usd WHERE event_kind='vlm_score')`. Và dòng `image_candidate` *"luôn mang `cost_state='carried_by_generation'` + `cost_usd IS NULL`"* ⇒ `usage_event` **đóng góp 0** vào COGS. Đổi bảng nguồn của số hạng thứ hai ⇒ COGS **vẫn đúng hai số hạng**. Số bảng ⛔ **không tăng** |

⚠️ **Cơ chế chống *"chi phí VLM biến mất"* không phải là ở chung bảng — mà là ở `usage_daily`.** Ba cột `vlm_call_count` / `vlm_cost_usd` / `vlm_cost_unknown_count` vẫn là **first-class** ở tầng rollup — chỉ đổi **bảng nguồn**. Mặt báo cáo mà `G2-a` và COGS đọc **không đổi một dòng**.

### Điều PM ⛔ KHÔNG làm

- ⛔ **Không phân xử cách đọc AC** — vì lời giải không cần tới nó. Tranh luận đó để mở, vô hại.
- ⛔ **Không sửa AC** (hướng (iii)) — thẩm quyền Product Owner.
- ⛔ **Không sửa `SDD`/`ADR` đã đóng băng** — biến thể (ii) được chọn **chính vì** nó không đòi hỏi điều đó.

---

## E21 — Sổ ripple từ L27 + L26: 8 hạng mục, chia chủ rõ ràng

- **Tầng**: 2 (PM ghi nhận và phân công)
- **Nguồn**: mục `RIPPLE` trong Worker Contract của **L27** và **L26**. ⭐ Cả hai worker **báo cáo thay vì tự sửa** — đúng ràng buộc *"cần thay đổi ở file khác ⇒ ghi vào RIPPLE"*.
- ✅ **L27 và L26 đều đã được PM verify độc lập** trước khi tick (⛔ không tick theo lời khai): L27 — câu đo AC ⛔ không còn mệnh đề lọc, `event_kind` chỉ còn trong phần lập luận, 0 Postgres enum, 0 wiki-link, 0 trích số dòng. L26 — 0 enum, 0 wiki-link, 0 trích số dòng, có ER diagram, `status: draft`.

| # | Ripple | Chủ | Ghi chú |
|:--:|---|---|---|
| 1 | ⚠️ **`SDD` §3.1 lạc hậu**: câu *"**38 entity** trên **4 schema**"* → **39**, và subgraph `E3` (schema `generation`) thiếu `vlm_scoring_call` | **PM, close-step** | ✅ PM đã **tự grep verify** (`SDD` dòng 164 và 172), ⛔ không tin mô tả của worker. ⭐ Đây là **liệt kê mô tả**, ⛔ **không phải** guardrail closed-list như `G-2` (`G-2` chỉ quản schema `public`) ⇒ **quyết định `E20` vẫn đứng vững** |
| 2 | ⚠️ **`SDD` §6.3 + §9 hàng `P-2`**: `SDD-HG-01.4` nay **đã đóng** bởi L26 → cần đánh dấu ĐÃ ĐÓNG + trỏ file mới | **PM, close-step** | `SDD` đóng băng ⇒ ⛔ worker không được chạm |
| 3 | `DB-Entity-Generation.md` còn câu lạc hậu *"Chi phí VLM đo ở `public.usage_event`"* → đổi thành `generation.vlm_scoring_call`. ⚠️ Vế cấm `vlm_evaluation` **vẫn đúng**, giữ nguyên | **L25a** | |
| 4 | `DB-Entity-Dialogue-And-Gate.md` — hàng `TBD` cho `SDD-HG-01.4` → đánh dấu đã đóng, trỏ `DB-Entity-Preview-And-Export.md` | **L25a** | |
| 5 | `CO-EX-1`: ⛔ không nguồn nào pin grant `SELECT` trên `public.project_access_state` cho role chạy `INSERT` export — trigger `SECURITY INVOKER` cần nó | **L25a** (`DB-Entity-Compliance-And-Takedown.md`) | Cũng là đầu vào cho lô verify Security |
| 6 | `CO-EX-2`: lần export **bị từ chối** cần một loại hành động `public.change_log`, ghi ở **transaction riêng** — vì trigger `RAISE` sẽ rollback cả `change_log` nếu cùng transaction | **L25a** (`DB-Entity-Provenance-And-Usage.md`) | ⭐ File này **đã hết bận** sau L27 |
| 7 | `CO-EX-3`: nếu sau này có nguồn nói export/preview chạy async ⇒ thêm `job_type` + grant `INSERT` cho `app_worker` | ⛔ **không hành động** | Điều kiện chưa xảy ra — ⛔ không làm trước (YAGNI) |
| 8 | Frontmatter `id:` toàn tầng Schema chưa thống nhất (`SPEC-DB-*` vs `DB-*`) | **L25b** | Sửa cơ học trên **14 file** ⇒ ⛔ **không song song với lô nào** |

### Hai quyết định worker tự chốt — PM chấp nhận

| Quyết định | PM đánh giá |
|---|---|
| **L26 đóng `SDD-HG-01.4` theo hướng CÓ trigger ở tầng DB** — và hoá giải phản biện *"hai nguồn sự thật"* bằng cách cho trigger **và** tầng service gọi **đúng một vị từ** `comic.export_is_permitted()` | ✅ **Chấp nhận.** Lập luận đúng chỗ đau nhất của dự án: `bus factor = 1`, ⛔ không code review ⇒ *"lint rule là lời hứa, trigger là cấu trúc"*. Và `M2-4` đo bằng **vắng mặt đường bypass** — mà psql/migration/code path thứ hai đều lách được tầng service |
| **L27 BỎ HẲN cột `event_kind`** thay vì giữ một-giá-trị *"cho tương lai"* | ✅ **Chấp nhận** — và ⭐ nó **verify bằng `grep` trước khi bỏ** (⛔ không tồn tại loại `usage_event` nào có tài liệu ngoài image candidate; `ADR-008` tuyên bố chi phí LLM là *"chưa xác định"* và ⛔ không route về `usage_event`), rồi **ghi bằng chứng đó vào file**. Đúng chuẩn *"verify, ⛔ không giả định"* mà run này đã phải học 3 lần |

### Một câu hỏi để mở — ⛔ không phải blocker
**L26**: `AF-4` (export **từng phần**) vẫn `TBD` do Founder. Worker giữ `chapter_id NOT NULL` và ghi đường mở rộng là **bảng liên kết cộng thêm**, ⛔ không nới cột.
⇒ ✅ **PM đồng ý**: đây là lựa chọn bảo thủ đúng — nới cột bây giờ là quyết thay Founder một việc chưa được hỏi.

---

## E22 — Kết quả wave A: Security Gate, và 5 quyết định PM

- **Tầng**: 2. **Lô liên quan**: L18, L19, L20.
- ✅ **Cả 5 file đều được PM verify độc lập trước khi tick**: 0 wiki-link · 0 trích số dòng · **0 link gãy** (kiểm bằng `realpath` từng đích) · `status: draft` · ⛔ không file Security nào trích `DB-Entity-Provenance-And-Usage.md` (file đang bị L27 sửa lúc đó).

### 1. ⭐ Cảnh báo chéo giữa hai lô Security — ĐÃ GIẢI, ⛔ không có xung đột

L19 gửi kèm một cảnh báo *"chặn gate"*: L18 ⛔ **không được** xếp *"thiếu content scanning"* vào cột lỗ hổng, vì `SRS-NFR-15` chốt đó là **anti-feature có chủ ý**.
✅ **PM kiểm: L18 ⛔ không phạm** — nó **chủ động** viết chính quy tắc đó vào file, kèm **tam giác phân biệt**: đọc opt-out signal = **bắt buộc** · ghi provider refusal = **bắt buộc** · tự dò tương đồng = **CẤM** vì phá điều kiện *"không biết"* của Điều 198b.
⇒ ⭐ **Hai lens độc lập, hai file, cùng một kết luận.** Đây là tín hiệu ràng buộc `SRS-NFR-15` đã nằm đúng chỗ chứ ⛔ không phải may mắn — và là **kết quả có giá trị nhất của Security Gate**, vì đây đúng là chỗ phản xạ nghề nghiệp của security auditor sẽ làm ngược.

### 2. `T-25` — ⛔ KHÔNG còn mở: đã được **anh** đóng ở `E9`

Ba chỗ trong `Spec-Security-Threat-Model.md` và một chỗ trong `Spec-Security-Tenant-Isolation.md` còn ghi `T-25` là *"PM hỏi Founder, trước lô API"*.
⛔ **Sai — nó đã được đóng.** `T-25` hỏi *"biện pháp chống lạm dụng chi phí nào có hiệu lực ở MVP1–MVP2: chỉ rate limit, hay hard quota tạm"* — **đúng câu hỏi của [E9](#e9--tầng-3-quyết-định-gate-3-đứng-trên-một-tiền-đề-sai-của-pm)**, và anh đã chọn **rate limit cho `generate`, đếm số request, ⛔ không đếm tiền**.
- **Nguyên nhân**: prompt của PM cho L19 **thiếu** ràng buộc rate limit (L18 có, L19 ⛔ không) ⇒ ⚠️ **lỗi của PM, ⛔ không phải của worker**.
- **Sửa**: **PM tự sửa 4 chỗ** — đây là tri thức PM sở hữu (một quyết định của anh), ⛔ không giao cho worker diễn giải lại.

### 3. `T-27` (BYOK key) — PM gán chủ, ⛔ và KHÔNG đóng trong run này

L18 gọi đây là **hạng mục rủi ro cao nhất của cả hệ thống** (lưu credential của **bên thứ ba**; một key lẫn sang tenant khác là rò rỉ tài sản của người khác), và ⛔ **không tài liệu nào trong repo gán chủ**.
- ✅ **PM gán chủ: Architect + Founder** (chọn cơ chế KMS **kéo theo** `ADR-002` hosting).
- ⛔ **PM KHÔNG đóng nó ở run này**: đóng đúng nghĩa cần **một ADR mới** — mà đó là **mở rộng phạm vi** ngoài kế hoạch anh đã duyệt. ⛔ Tự ý làm là quyết thay anh.
- ⇒ Ghi thành **hàng nợ kỹ thuật số 1** trong `000-Index.md` ở close-step. Tiêu chí thoát Phase 2 ⛔ **không** đòi đóng mọi rủi ro — nó đòi Security Spec **được review**, và việc chỉ ra hạng mục vô chủ này **chính là** giá trị của bước review.

### 4. `T-29` — L18 **từ chối nhận việc**, PM chấp nhận lời từ chối

`ADR-010` nêu `security-auditor` là ứng viên đóng `T-29` (thông báo cho tenant bị takedown). L18 **từ chối**, lý do: nó **tương tác trực tiếp với điều kiện miễn trừ Điều 198b**.
✅ **PM chấp nhận.** Từ chối đúng: đây là **quyết định pháp lý**, ⛔ không phải quyết định bảo mật. Chủ mới: **Founder + luật sư**, PM điều phối. ⭐ Một worker biết nói *"việc này không thuộc thẩm quyền tôi"* đáng tin hơn một worker nhận hết.

### 5. Glossary §5.3 — PM **duyệt cả 3** headword

L20 hỏi ý anh về 3 headword hạ tầng. ⛔ **Đây là tầng 2, PM quyết** — `outline.md` đã ghi `findings §5.3` **trong danh sách nguồn** của L20 ngay từ đầu, nên đây là **hoàn tất phạm vi**, ⛔ không phải mở rộng.
- `usage_daily` — ⭐ mạnh nhất: `usage_event` đã có headword mà thiếu vế rollup là **để hở nửa cặp**, đúng chỗ dễ đẻ ra counter tăng tại chỗ.
- `in_flight_per_tenant` — cơ chế nằm trong **chính câu CLAIM job**; ⚠️ định nghĩa **phải giữ `N = TBD`**, ⛔ cấm gán số.
- `hard quota` — giữ để chống nhầm với `credit ledger + hold`. ⚠️ Định nghĩa phải nói rõ nó **KHÔNG** được chọn cho MVP1–MVP2 (`E9`).
⇒ Giao **L25b**.

---

## E23 — ⏳ CHỜ VERIFY: hai mâu thuẫn chéo lô ở tầng API do L15 báo

- **Tầng**: 2. **Trạng thái**: ⏳ **ghi nhận, CHƯA phân xử** — L12 và L14 lúc đó **vẫn đang chạy**, nên L15 có thể đã đọc **trạng thái dở dang**. ⛔ PM ⛔ không phân xử trước khi tự verify trên bản cuối.

| # | Mâu thuẫn | Vì sao nó quan trọng |
|:--:|---|---|
| 1 | ⭐ **Cùng một điều kiện, hai mã lỗi**: `Endpoint-Project.md` (L12) trả **`403 PROJECT_ACCESS_DISABLED`**; `Endpoint-Preview-Export.md` (L14) trả **`409`** | ⚠️ **Cả hai cùng viện `SDD-HG-01.4` và cùng nói *"đúng một hàm dùng chung"*** — mà **một hàm ⛔ không thể phát ra hai mã**. Đây ⛔ không phải bất đồng phong cách, nó là **hai file mô tả sai về cùng một đoạn code sẽ được viết** |
| 2 | Tiền tố path phân kỳ: `/v1/` vs `/api/v1/` | Nhỏ nhưng lan ra **14 file**; sửa sau đắt hơn sửa bây giờ |

- **PM phải làm khi cả 6 lô API xong**: (1) tự đọc bản cuối của hai file, xác nhận mâu thuẫn còn thật; (2) chốt **một** mã lỗi và **một** tiền tố path; (3) giao lô sửa.
- ⚠️ **Bài học đang hình thành**: fan-out 6 lô cùng viết một tầng API thì **contract chung phải được chốt TRƯỚC** (tiền tố path, bảng mã lỗi chuẩn), ⛔ không để mỗi lô tự chọn. PM đã chốt 4 ràng buộc xuyên-endpoint nhưng **quên hai thứ tầm thường nhất** — và đúng hai thứ đó phân kỳ.
- ⭐ **Ghi nhận L15**: nó **chủ động đọc file của lô song song** để đối chiếu, phát hiện mâu thuẫn, và ⛔ **không tự phân xử** vì hai file đó ngoài phạm vi sở hữu. Cùng mẫu hành vi đã khen ở [E17](#e17--co-1-xung-đột-giữa-hai-quyết-định-chốt-pm-phân-xử).

### Một câu hỏi L15 để mở — `TD-Q1`
⛔ Chưa nguồn nào pin **ai được `SELECT`/`UPDATE` `public.takedown_request`**: cần role thứ 5 `app_operator` (⇒ phải sửa `SDD` §7.4) hay đi đường owner? Và `membership` **chưa có mô hình role/permission**.
⇒ Nó **chặn triển khai** hai endpoint admin `TD-2`/`TD-3`. **Ai đóng**: Architect + `Spec-Security-*`, phải sửa `SDD` §7.4 ⇒ ⛔ **ngoài phạm vi run này** (tầng Architecture đã đóng băng) ⇒ **nợ kỹ thuật**, ghi vào `000-Index.md` ở close-step.

---

## E24 — ⚠️ Tầng Schema BỎ SÓT một seam mà `SDD` bắt buộc: phân biệt chi phí BYOK

- **Tầng**: 2 (PM quyết). **Phát hiện**: cảnh báo phụ của **L16**, ⛔ không phải hạng mục nó được giao.
- ✅ **PM đã tự verify cả hai vế**, ⛔ không nhận lời khai:

| Vế | Kết quả grep |
|---|---|
| `SDD` **có** bắt buộc không? | ✅ **CÓ** — §8.2 `S-4`: *"**`generation.cost_usd` phải PHÂN BIỆT ĐƯỢC** chi phí trên key của ta và chi phí trên key của khách. Nếu không, mọi hàng lịch sử trộn hai loại tiền, và dữ liệu lịch sử ⛔ **không backfill được**"* (`SRS-FR-31`) |
| Tầng Schema **có** thực hiện không? | ⛔ **KHÔNG** — grep `byok`/`key của khách`/`cost_bearer`/`key_owner` trên **cả 14 file** ⇒ **rỗng**. `S-4` ⛔ không được file Schema nào nhắc tới |

### Vì sao đây là lỗi thật, ⛔ không phải chuyện để sau

⭐ Nó thuộc đúng nhóm **`KC-1`/`KC-7`**: *"seam phải có sớm vì lịch sử ⛔ không backfill được"*. BYOK là `[OoH]` **MVP4**, nhưng **cột phân biệt** thì ⛔ **không phải** thứ MVP4 — thiếu nó, **mọi dòng `generation` sinh ra từ MVP1 trở đi đều trộn hai loại tiền vĩnh viễn**. Đến MVP4 mới thêm cột thì mọi dữ liệu trước đó **mất khả năng tách COGS**, và ⛔ không có cách nào chữa.

⚠️ **Vì sao fan-out ⛔ không tự bắt được**: `S-4` nằm ở `SDD` **§8.2 (danh sách seam)**, trong khi mọi lô Schema được trỏ tới **§3.x (bản đồ entity)**. ⛔ Không lô nào có §8.2 trong nguồn ⇒ **không ai thấy mình thiếu**. Đây là **cùng cơ chế lỗi** với [E16](#e16--hai-entity-rơi-khỏi-13-cụm-export_artifact-và-preview_render) — thiếu một phép đối chiếu cơ học, chỉ khác chiều: E16 sót **entity**, E24 sót **seam**.

### Quyết định

- **Sửa trong run này** — đây là **thiếu sót của deliverable**, ⛔ không phải mở rộng phạm vi: `SDD` là nguồn sự thật của tầng Schema, và tầng Schema đã bỏ sót một điều `SDD` bắt buộc.
- **Mức độ**: *"reserve chỗ"* — đúng mức `DB-Entity-Credit-Ledger.md` đang dùng. ⛔ **Không** đặc tả cơ chế lưu/mã hoá key (đó là `T-27`, cần ADR mới, ngoài phạm vi).
- ⛔ **CHƯA dispatch được**: `DB-Entity-Generation.md` **đang bị L13/L14 ĐỌC**. Ghi một file đang có lô khác đọc đúng là [bài học #1](#4-ba-bài-học-của-pm-phải-đưa-vào-pm-coremd) đã tốn 7 lô. ⇒ **Xếp hàng sau khi 6 lô API xong.**

### Hạng mục gộp vào **một lô sửa cuối** (`L28`)
1. **`E24`** — cột phân biệt chi phí BYOK trên `generation.generation` (mức *"reserve chỗ"*).
2. ✅ **`E23` mục 1 — ĐÃ VERIFY TRÊN BẢN CUỐI: L15 ĐÚNG, mâu thuẫn là THẬT.** ⚠️ **Giả thuyết của PM *"L15 nhầm hai điều kiện khác nhau"* là SAI** — bằng chứng đếm được:
   - `403 PROJECT_ACCESS_DISABLED`: **22 lần, 5 file**. `409 PROJECT_ACCESS_DISABLED`: **0 lần**.
   - `Endpoint-Preview-Export.md` dòng 84 dùng **`409` trần** cho đúng điều kiện đó (*"Project ở trạng thái disable-access do takedown"*) — ⛔ không kèm tên mã.
   - ⭐ Và nó **mâu thuẫn với một invariant đã ghi**: `API-PRJ-4` nói *"**Mọi** endpoint đọc/ghi NỘI DUNG (… **preview, export** …) ⇒ `403 PROJECT_ACCESS_DISABLED`, qua **đúng một** hàm dùng chung"*.
   - ⇒ ⭐ **CHỐT `403`.** ~~Sửa **một dòng**~~ → ⚠️ **thực tế 5 dòng**, xem đính chính ngay dưới.
   - ⚠️ **ĐÍNH CHÍNH — phép đếm của PM sai vì grep phân biệt HOA/thường.** PM grep `409 PROJECT_ACCESS_DISABLED` ra **0** và kết luận *"chỉ một chỗ dùng `409` trần"*. L28a phát hiện file còn dùng **`409 project_access_disabled` viết THƯỜNG** ở 2 chỗ nữa ⇒ tổng cộng **5 vị trí** disable-access, ⛔ không phải 1. **Sửa đúng 1 dòng như PM chỉ định sẽ để file tự vi phạm chính `API-PRJ-4`** mà hạng mục này sinh ra để cưỡng chế. ⇒ ✅ Worker **sửa đủ 5 và báo lại**, ⛔ không im lặng làm theo lệnh sai. ⭐ **Bài học cho PM: mọi grep dùng làm căn cứ quyết định phải chạy `-i`** — đây là lần thứ hai grep của PM thiếu (lần trước: enum type ⛔ không có hậu tố `_enum`, [E24](#e24--️-tầng-schema-bỏ-sót-một-seam-mà-sdd-bắt-buộc-phân-biệt-chi-phí-byok)).
   - ⚠️ **Sửa hẹp, ⛔ đừng đổi nhầm**: file đó **còn một `409` KHÁC** (dòng 35) cho **human gate chưa PASS** — điều kiện khác, mã `409` **đúng**, ⛔ **giữ nguyên**.
3. ✅ **`E23` mục 2 — ĐÃ VERIFY: phân kỳ là THẬT, và cắt đúng theo lô.** `/v1/` = **10 file**; `/api/v1/` = **4 file** và **cả 4 đều của L14** (`Bubble-Typeset`, `Preview-Export`, `Tenancy`, `Usage-And-Credit`).
   - ⇒ ⭐ **CHỐT `/v1/`** (đa số áp đảo). Sửa 4 file của L14.
   - ⚠️ Đây là bằng chứng sạch cho luận điểm ở trên: phân kỳ **không ngẫu nhiên** — nó **cắt đúng ranh giới lô**. Mỗi worker tự nhất quán; cái thiếu là **contract giữa các lô**, và đó là việc của PM.
4. ⭐ **`public.change_log.action_type` là danh mục ĐÓNG mà thiếu giá trị** (L14 báo) cho: **export BỊ TỪ CHỐI** (`CO-EX-2`) · **tạo membership** · **tạo/xoá/sắp xếp bubble** (chỉ có `move_bubble`). ⭐ L14 xử lý đúng: ⛔ không phát minh giá trị, ⛔ không **tái dụng thầm lặng** một giá trị gần đúng — tái dụng thầm lặng chính là cách `change_log` mất giá trị làm bằng chứng.

> ⚠️ **`CO-EX-2` là lỗi của PM, ⛔ không phải của worker.** [E21](#e21--sổ-ripple-từ-l27--l26-8-hạng-mục-chia-chủ-rõ-ràng) hàng 6 đã giao nó cho **L25a** — nhưng prompt PM gửi L25a chỉ liệt **5 hạng mục và bỏ sót đúng hàng này**. Nó nằm im cho tới khi L14 **độc lập gặp lại**. ⇒ ⭐ **Bài học**: giao việc trong sổ escalation ⛔ **không đảm bảo** việc đó vào prompt — PM phải **đối chiếu sổ ↔ prompt** trước khi dispatch, đúng loại đối chiếu cơ học mà [E16](#e16--hai-entity-rơi-khỏi-13-cụm-export_artifact-và-preview_render) và [E24](#e24--️-tầng-schema-bỏ-sót-một-seam-mà-sdd-bắt-buộc-phân-biệt-chi-phí-byok) đều đã dạy.

### ✅ Hạng mục theo dõi — ĐÃ GIẢI, ⛔ không có lỗ
L14 loại đường ghi `dialogue_rendered` khỏi `Endpoint-Bubble-Typeset.md` (đúng — Schema nói *"bubble không sở hữu thoại"*) và **L13 đã nhận nó** ở `Endpoint-Human-Gates.md`.
⭐ **Hai lô hội tụ độc lập**: L14 nói *"nhường đường ghi về Human-Gates"*, L13 nói *"không có route collision, hai file khớp nhau"* — ⛔ không lô nào được PM bảo phải khớp với lô kia. ⇒ `UC-07` bước 4 **không có lỗ**.

### `action_type` — lỗi HỆ THỐNG, ⛔ không phải ba sự cố lẻ
**Ba lô độc lập** (L12, L13, L14) đều đâm vào **cùng một bức tường**: `public.change_log.action_type` là **danh mục ĐÓNG** nhưng thiếu giá trị cho hành động có thật. Tổng hợp:

| Nguồn | Hành động thiếu giá trị |
|---|---|
| L14 | export **BỊ TỪ CHỐI** (`CO-EX-2`) · tạo **membership** · **tạo/xoá/sắp xếp** bubble (chỉ có `move_bubble`) |
| L13 | sửa panel spec (ngoài `camera`) · **split/merge** panel · **duyệt** panel script |
| L12 | duyệt ingest · duyệt bible |

⭐ **Cả ba lô đều xử lý ĐÚNG**: ⛔ không phát minh giá trị, ⛔ không **tái dụng thầm lặng** một giá trị gần đúng. Tái dụng thầm lặng chính là cách `change_log` **mất giá trị làm bằng chứng** — mà đó là `KC-2`.
⚠️ **Hai cách đọc rộng cần BA xác nhận, ⛔ không tự quyết**: `reorder` → `swap_panel`? · `gán speaker` → `edit_dialogue`?
⇒ Gộp vào **`L28`**, ⛔ không vá lẻ từng file.

### E25 — Kết quả verify, và MỘT chỗ PM không đồng ý nhưng ⛔ không lật

> ⚠️ Mục này nằm giữa `E24` về mặt thứ tự đọc nhưng ghi **sau** — xem như phần bổ sung của sổ.

**Ba lô verify** (`L21` context-auditor · `L22` quality-assurance · `L31` security review **độc lập**) đã chạy trên 57 tài liệu. Kết quả và các lô sửa (`L33`, `L34`, `L36`, `L37`) ghi ở phần thân run. Hai điều đáng lưu vĩnh viễn:

#### 1. ⭐ *"Author == reviewer"* là một lỗ THẬT, ⛔ không phải chuyện hình thức
Tiêu chí thoát ghi *"Security Spec **đã được Security Auditor review**"*, nhưng ba file `Spec-Security-*` do **chính** `security-auditor` **VIẾT**. PM đã tick tiêu chí đó mà ⛔ không nhận ra. `L22` gọi tên nó.
⇒ PM chạy `L31` — **cặp mắt thứ hai, context mới**. Nó tìm ra **hai thứ tác giả về nguyên tắc KHÔNG THỂ thấy**:
- **Bề mặt operator xuyên tenant** (`TD-2`/`TD-3`) — sinh ra ở tầng API **SAU** khi threat model được viết. Threat model vẫn tuyên bố *"bề mặt đặc quyền rút về **ba** điểm"*.
- **`C-3` là lời hứa**: nó giao cho *"lô API"* đóng danh sách *"mọi đường đọc"*; lô API chạy xong mà **4 file ⛔ không hề nhắc `access_state`** ⇒ **nội dung đã takedown vẫn đọc được theo đặc tả**. Người viết `C-3` ⛔ **không có cách nào biết** điều đó.
⭐ **Bài học cho `pm-core.md`**: khi một tiêu chí gate nói *"X được **review** bởi vai trò R"* mà lô sản xuất **cũng** là R ⇒ **PM PHẢI chạy một lô R thứ hai với context mới**. ⛔ Cùng một agent role ⛔ không tự review được đầu ra của chính nó — ⛔ không phải vì nó cẩu thả, mà vì **giả định của nó là điểm mù của nó**.

#### 2. ⚠️ Một chỗ PM ⛔ KHÔNG đồng ý, và ⛔ cũng không lật
`INV-14` (`DB-Entity-Narrative-Timeline.md`) chốt: điều kiện *"phải duyệt ingest trước khi duyệt bible"* (`409 INGEST_NOT_APPROVED` của `SB-7`) được cưỡng chế ở **tầng ứng dụng**, ⛔ không bằng `CHECK` liên cột. Lý do worker nêu: *"một `CHECK` ở đây khoá luôn cả trường hợp chapter `superseded` vẫn giữ lịch sử duyệt"*.
- ⚠️ **PM ⛔ không tái lập được lý do đó**: `INV-13` chốt `ingest_approved_at` ⛔ **không bao giờ** bị ghi về `NULL` ⇒ một `CHECK` dạng `bible_approved_at IS NULL OR ingest_approved_at IS NOT NULL` **vẫn đúng** với chapter `superseded`.
- ⚠️ Và nó **đi ngược nguyên tắc của chính dự án** — *"đội 1 dev, ⛔ không code review ⇒ lint rule là **lời hứa**, trigger/constraint là **cấu trúc**"* — nguyên tắc mà `L26` đã dùng để chốt trigger trên `export_artifact`.
- ⛔ **PM vẫn KHÔNG lật.** Lý do: (a) worker đã **đọc file, nêu lý do cụ thể, tự đánh dấu *"vắng mặt constraint là CHỦ Ý"*** kèm cơ chế kiểm thay thế — đó là một vị trí có lập luận, ⛔ không phải sơ suất; (b) PM chỉ có **một phân tích nhanh**, ⛔ không phải bằng chứng ngược; (c) ⭐ lật một quyết định có lập luận bằng trực giác của PM **chính là** hình dạng của [E9](#e9--tầng-3-quyết-định-gate-3-đứng-trên-một-tiền-đề-sai-của-pm) — sai lầm đắt nhất của run này.
- ⇒ ⭐ **Ghi thành câu hỏi cho Architect ở Phase 3**, ⛔ không phải một sửa đổi ở Phase 2: *"`INV-14` có nên nâng lên `CHECK` liên cột không — và lý do 'superseded' có thật sự chặn không?"*

### Ba hạng mục nhỏ thêm vào `L28` (từ L13)
1. `origin='ai'` trên dòng `generation` cấp request là **suy luận của worker** (`G-6` chỉ phủ 4 trường của `D-59`) ⇒ cần Schema **xác nhận hoặc bác**.
2. `T-HG-GATE1-RESET` nay **chặn một hành vi API**: `PATCH speaker` trên dòng đã PASS gate 1. Worker liệt 2 ứng xử ứng viên và ⛔ **không chọn** — đúng thẩm quyền.
3. ⚠️ **Ripple `SDD` (close-step, ⛔ không sửa ở lô worker)**: `SDD` §5.2 `F5` vẽ `INSERT change_log` **lúc enqueue** — mâu thuẫn `ADR-015` `Q1` + danh mục `action_type`. L13 theo `ADR`/`Schema` (đúng ràng buộc #2) và ghi chênh lệch lại. PM xử ở close-step.

