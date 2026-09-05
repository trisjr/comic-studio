# AI Coding
"""
run_mvp0.py
Script MVP0 — lam DUNG MOT VIEC: generate PAGE (D-1) voi reference + N=3
candidate + VLM select. ⛔ Khong UI, ⛔ khong database (`MVP-Scope §3.1`,
o `A5` = ❌).

⚠️ CODE NAY SE BI VUT. `MVP-Scope §3.1` / `Roadmap §3.1`: "Code cua MVP0 KHONG
phai nen cua san pham — viet de tra loi cau hoi roi BO; giu lai KET LUAN va
DU LIEU." ⇒ Neu thay minh sap viet migration, config loader, hay abstraction
da provider trong file nay: DUNG LAI.

HAI STAGE — ⭐ stage `refs` la BAT BUOC truoc `pages`:
  refs   — sinh character sheet cho tung nhan vat tu MO TA CHU trong Story
           Bible. Nguoi chon tay 1 anh/nhan vat lam canonical reference.
           ⚠️ Ly do stage nay ton tai: Story Bible mo ta nhan vat bang CHU,
           nhung pipeline can ANH reference. ⛔ Khong co buoc nay thi
           "generate voi reference" ⛔ khong chay duoc.
  pages  — moi page YAML duoi mvp0/pages/<page_id>.yaml duoc compile thanh
           MOT prompt duy nhat (D-1), dung reference DA CHON, sinh N=3
           candidate/page, roi VLM xep hang. G1 van cham theo TUNG PANEL —
           `crop_page.py` cat anh trang thanh panel SAU khi co anh trang.

Cach dung:
    python3 scripts/mvp0/run_mvp0.py refs --dry-run
    python3 scripts/mvp0/run_mvp0.py refs
    # -> chon tay 1 anh/nhan vat, copy vao mvp0/refs/<char_id>.png
    python3 scripts/mvp0/run_mvp0.py pages --dry-run
    python3 scripts/mvp0/run_mvp0.py pages
    python3 scripts/mvp0/run_mvp0.py pages --page ch01_page001 --dry-run
    python3 scripts/mvp0/run_mvp0.py pages -n 3
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
PAGES_DIR = MVP0 / "pages"
# `CF-3.1` `[OFF]` — mac dinh cho MOI page, ⛔ khong retry-on-failure
N_CANDIDATES = 3

# Nhip nghi giua hai request sinh anh. Nguon: quan sat thuc nghiem 2026-08-31
# — 4 request lien tiep (~3.5 req/phut) cham `Throttling.RateQuota`; nhip 30s
# (~1.3 req/phut) chay 8/8 request sach. Day la pacing phong ngua, ⛔ khong
# phai retry-on-failure (`CF-3.1` giu nguyen). So RPM that cua account xem
# trong trang quota cua Model Studio console.
SECONDS_BETWEEN_IMAGE_CALLS = 30


def load_bible():
    data = yaml.safe_load((MVP0 / "story-bible.yaml").read_text(encoding="utf-8"))
    return {entity["id"]: entity for entity in data["nhan_vat"]}


def load_pages(only_ids=None):
    """Doc mvp0/pages/<page_id>.yaml, sap xep theo ten file. Bo qua README."""
    if not PAGES_DIR.exists():
        return []
    pages = []
    for path in sorted(PAGES_DIR.glob("*.yaml")):
        page_id = path.stem
        if only_ids and page_id not in only_ids:
            continue
        doc = yaml.safe_load(path.read_text(encoding="utf-8"))
        pages.append((page_id, doc))
    return pages


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

    Dung `BASE_STYLE_CORE` chu ⛔ KHONG dung `BASE_STYLE` (= BASE_STYLE_CHARACTER):
    ban CHARACTER duoc soan cho panel truyen nen ket thuc bang "NOT a character
    model sheet, NOT multiple angle views, NOT standing on blank white background"
    — dung nguyen van o day thi prompt tu phu dinh dong model-sheet ngay ke tiep.
    CORE chi mang art direction, ⛔ khong mang rang buoc khung hinh.

    Ten nhan vat lay `ten_en`: prompt gui cho image model la tieng Anh, ten tieng
    Viet co dau lot vao lam nhieu token.
    """
    ref = entity.get("canonical_reference_en") or entity["canonical_reference"]
    strip = compile_prompt.strip_meta
    name = entity.get("ten_en") or entity["ten"]
    parts = [
        compile_prompt.BASE_STYLE_CORE,
        "2D anime character design model sheet, multiple angle views, clean neutral background, front view and three-quarter view, pure 2D anime drawing, flat cel shading",
        f"{name}: {strip(ref['khuon_mat'])} {strip(ref['mat'])} {strip(ref['toc'])} {strip(ref['trang_phuc'])}",
    ]
    if "dac_diem_rieng" in ref:
        parts.append(strip(ref["dac_diem_rieng"]))
    return ". ".join(p.replace("\n", " ").strip() for p in parts if p)


def run_refs(is_dry_run, only_character=None):
    bible = load_bible()
    if only_character:
        bible = {k: v for k, v in bible.items() if k == only_character}
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
                time.sleep(SECONDS_BETWEEN_IMAGE_CALLS)
                continue
            (run_dir / "candidates" / f"{char_id}-c{index}.png").write_bytes(result["image_bytes"])
            append_jsonl(run_dir / "usage.jsonl",
                         {k: v for k, v in result.items() if k != "image_bytes"} |
                         {"stage": "refs", "character_id": char_id})
            time.sleep(SECONDS_BETWEEN_IMAGE_CALLS)

    print(f"\n-> {run_dir}")
    if not is_dry_run:
        print(f"⭐ Buoc NGUOI lam: chon 1 anh/nhan vat, luu thanh {REFS_DIR}/<char_id>.png")
    return run_dir


def load_reference_images(conditioning_set):
    """Doc anh reference DA CHON. ⛔ Thieu anh la loi cung — ⛔ khong chay tiep."""
    images = []
    for ref_path in conditioning_set:
        path = ROOT / ref_path
        if not path.exists():
            raise FileNotFoundError(
                f"Thieu reference {path}. Chay stage `refs` truoc, roi chon tay 1 anh/nhan vat."
            )
        images.append(path.read_bytes())
    return images


def _panel_indices(page_doc):
    return [panel["panel_index"] for panel in page_doc.get("panels", []) if "panel_index" in panel]


def run_pages(only_ids, is_dry_run, n_candidates=N_CANDIDATES):
    pages = load_pages(only_ids)
    run_dir = make_run_dir("pages")
    print(f"Stage pages — {len(pages)} trang x N={n_candidates} = "
          f"{len(pages) * n_candidates} anh\n")

    for page_id, page_doc in pages:
        text_prompt, conditioning_set, dropped = compile_prompt.compile_page(page_doc)
        (run_dir / "prompts" / f"{page_id}.txt").write_text(text_prompt, encoding="utf-8")

        panel_indices = _panel_indices(page_doc)
        if dropped:
            append_jsonl(run_dir / "dropped_constraints.jsonl",
                         {"page_id": page_id, "dropped": dropped})

        print(f"  {page_id}  {len(page_doc.get('panels', []))} panel  "
              f"{len(conditioning_set)} ref  {len(dropped)} drop  [{len(text_prompt)}c]")
        if is_dry_run:
            continue

        references = load_reference_images(conditioning_set)
        candidates, refused = [], 0
        for candidate_index in range(n_candidates):
            try:
                result = providers.generate_candidate(text_prompt, references, candidate_index)
            except providers.ProviderRefusal as refusal:
                refused += 1
                append_jsonl(run_dir / "refusals.jsonl",
                             {"page_id": page_id, "candidate_index": candidate_index,
                              "reason": str(refusal)})
                time.sleep(SECONDS_BETWEEN_IMAGE_CALLS)
                continue
            path = run_dir / "candidates" / f"{page_id}-c{candidate_index}.png"
            path.write_bytes(result["image_bytes"])
            candidates.append(result)
            # ⭐ Ghi usage NGAY sau khi sinh — ⛔ KHONG doi ket qua VLM.
            # Nguon: Story-Usage-Event AC — "usage_event cua ca 3 candidate VAN
            # duoc ghi truoc khi biet ket qua select". panel_indices o day cho
            # regen_ratio.py cong don ve tung panel (D-1 giu G1 per-panel).
            append_jsonl(run_dir / "usage.jsonl",
                         {k: v for k, v in result.items() if k != "image_bytes"} |
                         {"stage": "pages", "page_id": page_id, "panel_indices": panel_indices})
            time.sleep(SECONDS_BETWEEN_IMAGE_CALLS)

        record = {"page_id": page_id, "panel_indices": panel_indices,
                  "characters": [c.get("id") for c in page_doc.get("characters", [])],
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
        print("⭐ Buoc NGUOI lam: chay `crop_page.py` de cat anh trang thanh "
              "tung panel, roi cham pass/fail TUNG PANEL (`G1-c`) bang mat "
              "(`G1-a`/`G1-d`).")
    return run_dir


def main():
    parser = argparse.ArgumentParser(description="MVP0 — reference + N=3 + VLM select (page-level, D-1)")
    parser.add_argument("stage", choices=["refs", "pages"])
    parser.add_argument("--dry-run", action="store_true",
                        help="Chi compile va in prompt — ⛔ khong goi API, ⛔ khong ton tien")
    parser.add_argument("--character", help="Chi sinh reference cho 1 character_id")
    parser.add_argument("--page", dest="pages", nargs="*",
                         help="Chi chay vai page_id (vi du ch01_page001)")
    parser.add_argument("-n", "--candidates", type=int, default=N_CANDIDATES,
                        help=f"So luong candidate moi trang (mac dinh: {N_CANDIDATES})")
    args = parser.parse_args()

    if args.stage == "refs":
        run_refs(args.dry_run, args.character)
    else:
        run_pages(args.pages, args.dry_run, args.candidates)
    return 0


if __name__ == "__main__":
    sys.exit(main())
