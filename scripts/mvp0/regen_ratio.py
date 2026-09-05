# AI Coding
"""
regen_ratio.py
Tinh regen ratio `p50`/`p90` cua MVP0 tu `usage.jsonl` + bang cham golden
dataset. ⚠️ Thieu con so nay thi `G2` ⛔ KHONG CHAY DUOC — ⛔ khong PASS mac
dinh (`Roadmap §6.2` · `MVP-Scope §7.3` `G2-a`).

⚠️ CODE NAY SE BI VUT cung phan con lai cua MVP0 (`MVP-Scope §3.1`). Giu lai
la KET LUAN (`p50`/`p90` ghi vao `g1-verdict.md`), ⛔ khong phai script nay.

DINH NGHIA DUNG O DAY — ⚠️ `[EM]`, CAN FOUNDER XAC NHAN:
    regen_ratio(panel) = tong so anh da sinh cho panel do / 1 anh duoc duyet
Tong duoc cong qua MOI thu muc `run-panels-*` (unit cu, panel-level) VA
`run-pages-*` (D-1, page-level — moi candidate cua 1 trang cong +1 cho MOI
`panel_index` trong `panel_indices` cua trang do, vi mot anh trang chua
nhieu panel), nen mot panel phai chay lai vong hai se co ratio ~2N.

⚠️ ⛔ KHONG co cong thuc regen ratio nao trong repo. Da kiem: `Glossary`,
`ADR-018`, `MVP-Scope §7.3`, `Analysis-Comic-Studio-Concept` — ca bon deu goi
ten metric nay ma ⛔ khong dinh nghia phep chia. Cho gan nhat la "he so
regenerate 2x/3x" (`Analysis` §826, tu khai la ⛔ khong co du lieu nganh), va
dinh nghia tren la cach doc khop voi no. ⇒ Founder phai xac nhan truoc khi con
so nay di vao `G2`.

HAI KY LUAT CUNG (`ADR-018` Q2):
  - Thieu du lieu ⇒ NOI RA la thieu. ⛔ KHONG BAO GIO tra `0`: `0` la mot gia
    tri trong rat tot, no se duoc doc thanh "⛔ khong ai regen" thay vi
    "chung ta ⛔ khong biet".
  - Panel chua co anh duyet (`approved_candidate_index = none`) bi LOAI khoi
    phep tinh va dem RIENG — no ⛔ chua xong mot vong, ⛔ khong phai ratio thap.

Cach dung:
    python3 scripts/mvp0/regen_ratio.py
"""

import csv
import json
import math
import pathlib
import collections

ROOT = pathlib.Path(__file__).resolve().parents[2]
MVP0 = ROOT / "mvp0"
SHEET = MVP0 / "golden-dataset" / "scoring-sheet.csv"


def count_images_per_panel():
    """Dem so anh da sinh cho tung panel, cong qua MOI thu muc run-panels-*
    (unit cu, panel-level) VA run-pages-* (D-1, page-level).
    """
    counts = collections.Counter()
    run_dirs = sorted(MVP0.glob("run-panels-*")) + sorted(MVP0.glob("run-pages-*"))
    for run_dir in run_dirs:
        usage = run_dir / "usage.jsonl"
        if not usage.exists():
            continue
        for line in usage.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            record = json.loads(line)
            if record.get("stage") == "panels" and "panel_index" in record:
                counts[record["panel_index"]] += 1
            elif record.get("stage") == "pages":
                for panel_index in record.get("panel_indices", []):
                    counts[panel_index] += 1
    return counts, run_dirs


def read_effective_rows():
    """Ban ghi con hieu luc = dong co `scored_at` MUON NHAT cho moi panel.

    Dong cu ⛔ khong bi bo — chung la lich su doi y, thu gan nhat voi mot
    second rater ma MVP0 co duoc (bus factor = 1).
    """
    if not SHEET.exists():
        return {}
    latest = {}
    with open(SHEET, encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            index = int(row["panel_index"])
            if index not in latest or row["scored_at"] > latest[index]["scored_at"]:
                latest[index] = row
    return latest


def percentile(values, rank):
    """Nearest-rank: p_k = sorted[ceil(k/100 * n) - 1]. ⛔ Khong noi suy."""
    ordered = sorted(values)
    position = math.ceil(rank / 100 * len(ordered))
    return ordered[max(position - 1, 0)]


def report_missing(counts, effective):
    """In ly do KHONG DO DUOC. ⛔ Khong tra `0` de thay the."""
    print("⛔ KHONG DO DUOC — regen ratio ⛔ khong co gia tri\n")
    if not counts:
        print("  Ly do: ⛔ khong tim thay dong `stage=panels` nao trong "
              "mvp0/run-panels-*/usage.jsonl hoac mvp0/run-pages-*/usage.jsonl")
    if not effective:
        print(f"  Ly do: bang cham {SHEET.relative_to(ROOT)} ⛔ chua co dong nao")
    print("\n⚠️ Ghi \"⛔ KHONG DO DUOC\" vao g1-verdict.md muc 2. "
          "⛔ KHONG ghi `0` — xem `ADR-018` Q2.")


def main():
    counts, run_dirs = count_images_per_panel()
    effective = read_effective_rows()
    print(f"Doc {len(run_dirs)} thu muc run-panels-*/run-pages-* · "
          f"{len(counts)} panel co anh · {len(effective)} panel da cham\n")

    if not counts or not effective:
        report_missing(counts, effective)
        return

    ratios, unapproved, unscored = {}, [], []
    for index, row in sorted(effective.items()):
        if row["approved_candidate_index"].strip() == "none":
            unapproved.append(index)
        elif index not in counts:
            unscored.append(index)
        else:
            ratios[index] = counts[index]

    for index, ratio in ratios.items():
        print(f"  panel {index:2d}  {ratio} anh / 1 duyet  = {ratio:.1f}")

    if not ratios:
        print("\n⛔ KHONG DO DUOC — ⛔ khong panel nao vua co anh vua co ban ghi duyet")
        return

    values = list(ratios.values())
    print(f"\n  p50 = {percentile(values, 50):.1f}   "
          f"p90 = {percentile(values, 90):.1f}   (n = {len(values)} panel)")

    if len(set(values)) == 1:
        print(f"\n⚠️ PHAN PHOI SUY BIEN — moi panel deu dung {values[0]} anh, "
              "⛔ khong vong nao lap lai.\n"
              "   ⇒ `p50 = p90 = N` la HE QUA CUA THIET KE (N=3 co dinh, ⛔ khong "
              "retry-on-failure),\n"
              "     ⛔ CHUA phai mot phep do ve ti le regen that. Ghi ro dieu nay "
              "vao g1-verdict.md.")

    if unapproved:
        print(f"\n⚠️ LOAI khoi phep tinh — {len(unapproved)} panel co "
              f"`approved_candidate_index = none`: {unapproved}\n"
              "   ⇒ Panel nay ⛔ CHUA xong mot vong, ⛔ khong phai ratio thap.")
    if unscored:
        print(f"\n⚠️ Da cham nhung ⛔ khong tim thay anh trong usage.jsonl: {unscored}\n"
              "   ⇒ Thu muc run-*/ co the da bi xoa. Ratio cua panel nay ⛔ khong tinh lai duoc.")

    print("\n⚠️ Dinh nghia phep chia la `[EM]` — CAN FOUNDER XAC NHAN truoc khi "
          "con so nay di vao `G2`. Xem docstring dau file.")


if __name__ == "__main__":
    main()
