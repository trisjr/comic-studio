# AI Coding
"""
fix-doc-anchors.py
Sua co hoc cac anchor trong-file bi gay do SAI DANG SLUG, khong phai do drift.

Chi sua hai loai (A1, A2) — deu la loi go, khong doi y nghia tham chieu:
  A1 - anchor giu nguyen em-dash/en-dash, trong khi slugger LOAI BO chung.
  A2 - anchor sai SO LUONG dau gach noi (em-dash/emoji bi xoa sinh ra gach doi).

⛔ KHONG dong toi loai A3 (heading khong ton tai / da doi ten): do la dau vet
drift that, sua tu dong se AM THAM doi dich tham chieu. Phai co nguoi doc.

An toan: chi thay khi chuan hoa anchor khop DUNG MOT heading trong cung file.
Khop 0 hoac >=2 ung vien => bo qua va bao cao.

Cach dung:
    python3 scripts/fix-doc-anchors.py [thu-muc]           # mac dinh: docs
    python3 scripts/fix-doc-anchors.py docs --dry-run      # chi bao cao
"""

import re
import sys
import pathlib
import importlib.util

HEADING_PATTERN = re.compile(r"^#{1,6}\s+(.*)$", re.MULTILINE)
INLINE_ANCHOR_PATTERN = re.compile(r"\]\(#([^)]+)\)")
DASH_RUN_PATTERN = re.compile(r"-+")


def load_slugger():
    """Dung lai to_slug cua check-doc-anchors.py de hai script khong bao gio lech."""
    path = pathlib.Path(__file__).with_name("check-doc-anchors.py")
    spec = importlib.util.spec_from_file_location("check_doc_anchors", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.to_slug


def normalize(anchor):
    """Xoa em-dash/en-dash roi gop moi day gach noi thanh mot."""
    stripped = anchor.replace("—", "-").replace("–", "-")
    return DASH_RUN_PATTERN.sub("-", stripped).strip("-")


def resolve(anchor, slugs):
    if anchor in slugs:
        return None
    target = normalize(anchor)
    candidates = {slug for slug in slugs if normalize(slug) == target}
    return candidates.pop() if len(candidates) == 1 else None


def process(path, to_slug, is_dry_run):
    text = path.read_text(encoding="utf-8")
    slugs = {to_slug(heading) for heading in HEADING_PATTERN.findall(text)}
    fixed, skipped = [], []

    def replace(match):
        anchor = match.group(1)
        resolved = resolve(anchor, slugs)
        if resolved is None:
            if anchor not in slugs:
                skipped.append(anchor)
            return match.group(0)
        fixed.append((anchor, resolved))
        return f"](#{resolved})"

    updated = INLINE_ANCHOR_PATTERN.sub(replace, text)
    if fixed and not is_dry_run:
        path.write_text(updated, encoding="utf-8")
    return fixed, skipped


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    root = pathlib.Path(args[0] if args else "docs")
    is_dry_run = "--dry-run" in sys.argv
    to_slug = load_slugger()

    total_fixed = total_skipped = 0
    for path in sorted(root.rglob("*.md")):
        fixed, skipped = process(path, to_slug, is_dry_run)
        total_fixed += len(fixed)
        total_skipped += len(skipped)
        if fixed:
            print(f"{path}  ({len(fixed)} sua)")
            for old, new in fixed:
                print(f"  #{old}\n    -> #{new}")

    label = "SE SUA" if is_dry_run else "DA SUA"
    print(f"\n{label}: {total_fixed}  |  BO QUA (can nguoi doc): {total_skipped}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
