# AI Coding
"""
run_mvp0.py
Script MVP0 — lam DUNG MOT VIEC: generate panel voi reference + N=3 candidate
+ VLM select. ⛔ Khong UI, ⛔ khong database (`MVP-Scope §3.1`, o `A5` = ❌).

⚠️ CODE NAY SE BI VUT. `MVP-Scope §3.1` / `Roadmap §3.1`: "Code cua MVP0 KHONG
phai nen cua san pham — viet de tra loi cau hoi roi BO; giu lai KET LUAN va
DU LIEU." ⇒ Neu thay minh sap viet migration, config loader, hay abstraction
da provider trong file nay: DUNG LAI.

HAI STAGE — ⭐ stage `refs` la BAT BUOC truoc `panels`:
  refs   — sinh character sheet cho tung nhan vat tu MO TA CHU trong Story
           Bible. Nguoi chon tay 1 anh/nhan vat lam canonical reference.
           ⚠️ Ly do stage nay ton tai: Story Bible mo ta nhan vat bang CHU,
           nhung pipeline can ANH reference. ⛔ Khong co buoc nay thi
           "generate voi reference" ⛔ khong chay duoc.
  panels — dung reference DA CHON, sinh N=3 candidate/panel, roi VLM xep hang.

Cach dung:
    python3 scripts/mvp0/run_mvp0.py refs   --dry-run
    python3 scripts/mvp0/run_mvp0.py refs
    # -> chon tay 1 anh/nhan vat, copy vao mvp0/refs/<char_id>.png
    python3 scripts/mvp0/run_mvp0.py panels --chapter ch1 --dry-run
    python3 scripts/mvp0/run_mvp0.py panels --chapter ch1
"""

import os
import sys
import json
import time
import pathlib
import argparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import yaml
import compile_prompt
import providers

ROOT = pathlib.Path(__file__).resolve().parents[2]
MVP0 = ROOT / "mvp0"
REFS_DIR = MVP0 / "refs"
N_CANDIDATES = 3  # `CF-3.1` `[OFF]` — mac dinh cho MOI panel, ⛔ khong retry-on-failure


def load_bible():
    data = yaml.safe_load((MVP0 / "story-bible.yaml").read_text(encoding="utf-8"))
    return {entity["id"]: entity for entity in data["nhan_vat"]}


def load_panels(chapter):
    files = ["ch1", "ch2"] if chapter == "all" else [chapter]
    panels = []
    for name in files:
        data = yaml.safe_load((MVP0 / f"panel-script-{name}.yaml").read_text(encoding="utf-8"))
        for page in data["pages"]:
            for panel in page["panels"]:
                panels.append({**panel, "page_no": page["page_no"]})
    return panels


def make_run_dir(stage):
    run_dir = MVP0 / f"run-{stage}-{time.strftime('%Y%m%d-%H%M%S')}"
    (run_dir / "prompts").mkdir(parents=True)
    (run_dir / "candidates").mkdir()
    return run_dir


def append_jsonl(path, record):
    with open(path, "a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False) + "\n")


def character_sheet_prompt(entity):
    """Prompt sinh character sheet — deterministic, ⛔ khong LLM.

    Moi field di qua `strip_meta` — chu thich meta trong Story Bible ma vao
    prompt se THANH NOI DUNG VE (bang chung: run-refs-20260831-223131, 3/3
    anh lam_phu bi ve them nguoi la tu cau "⛔ khong gan cho nguoi phu nu
    ao trang").
    """
    ref = entity["canonical_reference"]
    strip = compile_prompt.strip_meta
    parts = [
        compile_prompt.BASE_STYLE,
        "character reference sheet, neutral grey background, front view and three-quarter view",
        f"{entity['ten']}: {strip(ref['khuon_mat'])} {strip(ref['toc'])} {strip(ref['trang_phuc'])}",
    ]
    if "vat_pham" in ref:
        parts.append(strip(ref["vat_pham"]))
    if "dac_diem_khong_doi" in ref:
        parts.append(strip(ref["dac_diem_khong_doi"]))
    return ". ".join(p.replace("\n", " ").strip() for p in parts if p)


def run_refs(is_dry_run):
    bible = load_bible()
    run_dir = make_run_dir("refs")
    print(f"Stage refs — {len(bible)} nhan vat x {N_CANDIDATES} candidate\n")

    for char_id, entity in bible.items():
        prompt = character_sheet_prompt(entity)
        (run_dir / "prompts" / f"{char_id}.txt").write_text(prompt, encoding="utf-8")
        print(f"  {char_id}: {prompt[:88]}...")
        if is_dry_run:
            continue
        for index in range(N_CANDIDATES):
            try:
                result = providers.generate_candidate(prompt, [], index)
            except providers.ProviderRefusal as refusal:
                append_jsonl(run_dir / "refusals.jsonl",
                             {"stage": "refs", "character_id": char_id,
                              "candidate_index": index, "reason": str(refusal)})
                print(f"    ⛔ candidate {index}: bi tu choi")
                continue
            (run_dir / "candidates" / f"{char_id}-c{index}.png").write_bytes(result["image_bytes"])
            append_jsonl(run_dir / "usage.jsonl",
                         {k: v for k, v in result.items() if k != "image_bytes"} |
                         {"stage": "refs", "character_id": char_id})

    print(f"\n-> {run_dir}")
    if not is_dry_run:
        print(f"⭐ Buoc NGUOI lam: chon 1 anh/nhan vat, luu thanh {REFS_DIR}/<char_id>.png")
    return run_dir


def load_reference_images(panel):
    """Doc anh reference DA CHON. ⛔ Thieu anh la loi cung — ⛔ khong chay tiep."""
    images = []
    for char_id in panel.get("characters", []):
        path = REFS_DIR / f"{char_id}.png"
        if not path.exists():
            raise FileNotFoundError(
                f"Thieu reference {path}. Chay stage `refs` truoc, roi chon tay 1 anh/nhan vat."
            )
        images.append(path.read_bytes())
    return images


def run_panels(chapter, is_dry_run, only):
    bible = load_bible()
    panels = load_panels(chapter)
    if only:
        wanted = set(only)
        panels = [p for p in panels if p["panel_index"] in wanted]

    run_dir = make_run_dir(f"panels-{chapter}")
    print(f"Stage panels — {len(panels)} panel x N={N_CANDIDATES} = "
          f"{len(panels) * N_CANDIDATES} anh\n")

    for panel in panels:
        index = panel["panel_index"]
        text_prompt, conditioning_set, dropped = compile_prompt.compile_panel(panel, bible)
        (run_dir / "prompts" / f"panel-{index:03d}.txt").write_text(text_prompt, encoding="utf-8")

        if dropped:
            append_jsonl(run_dir / "dropped_constraints.jsonl",
                         {"panel_index": index, "dropped": dropped})

        print(f"  panel {index:2d}  {len(conditioning_set)} ref  "
              f"{len(dropped)} drop  {text_prompt[:56]}...")
        if is_dry_run:
            continue

        references = load_reference_images(panel)
        candidates, refused = [], 0
        for candidate_index in range(N_CANDIDATES):
            try:
                result = providers.generate_candidate(text_prompt, references, candidate_index)
            except providers.ProviderRefusal as refusal:
                refused += 1
                append_jsonl(run_dir / "refusals.jsonl",
                             {"panel_index": index, "candidate_index": candidate_index,
                              "reason": str(refusal)})
                continue
            path = run_dir / "candidates" / f"panel-{index:03d}-c{candidate_index}.png"
            path.write_bytes(result["image_bytes"])
            candidates.append(result)
            # ⭐ Ghi usage NGAY sau khi sinh — ⛔ KHONG doi ket qua VLM.
            # Nguon: Story-Usage-Event AC — "usage_event cua ca 3 candidate VAN
            # duoc ghi truoc khi biet ket qua select".
            append_jsonl(run_dir / "usage.jsonl",
                         {k: v for k, v in result.items() if k != "image_bytes"} |
                         {"stage": "panels", "panel_index": index})

        record = {"panel_index": index, "page_no": panel["page_no"],
                  "character_count": panel["character_count"],
                  "characters": panel.get("characters", []),
                  "candidates_generated": len(candidates), "candidates_refused": refused,
                  "dropped_constraints": dropped}

        if candidates:
            try:
                record["vlm_scoring"] = providers.score_candidates(
                    [c["image_bytes"] for c in candidates], text_prompt)
            except Exception as exc:
                # ⭐ Anh da sinh xong nhung cham hong la TRANG THAI HOP LE,
                # ⛔ khong phai that bai chung — `ADR-007` Q6. Anh van duoc giu.
                record["vlm_scoring"] = None
                record["vlm_error"] = str(exc)

        append_jsonl(run_dir / "results.jsonl", record)

    print(f"\n-> {run_dir}")
    if not is_dry_run:
        print("⭐ Buoc NGUOI lam: cham pass/fail tung panel SAU khi VLM chon "
              "(day chinh la phep do `G1-c`), va cham `G1-a`/`G1-d` bang mat.")
    return run_dir


def main():
    parser = argparse.ArgumentParser(description="MVP0 — reference + N=3 + VLM select")
    parser.add_argument("stage", choices=["refs", "panels"])
    parser.add_argument("--chapter", default="ch1", choices=["ch1", "ch2", "all"])
    parser.add_argument("--dry-run", action="store_true",
                        help="Chi compile va in prompt — ⛔ khong goi API, ⛔ khong ton tien")
    parser.add_argument("--panels", type=int, nargs="*", help="Chi chay vai panel_index")
    args = parser.parse_args()

    if args.stage == "refs":
        run_refs(args.dry_run)
    else:
        run_panels(args.chapter, args.dry_run, args.panels)
    return 0


if __name__ == "__main__":
    sys.exit(main())
