# AI Coding
"""
check-doc-anchors.py
Kiem tra co hoc link va anchor trong kho tai lieu Markdown cua du an.

Phat hien hai loai loi:
  1. LINK GAY   - link tuong doi tro toi file khong ton tai.
  2. ANCHOR GAY - link `#anchor` trong cung file khong khop heading nao.

Thuat toan slug tuan theo github-slugger: ha chu thuong, loai bo dau cau
(bao gom em-dash U+2014, nam trong dai U+2000-U+206F), khoang trang -> gach noi.
Giu lai combining mark de anchor tieng Viet resolve dung.

Gioi han da biet:
  - Chi kiem anchor TRONG-FILE; anchor lien-file (file.md#anchor) chua kiem.
  - Chua mo hinh hoa quy tac heading trung ten cua github-slugger (append -1, -2).
  => Con so bao ra la CAN DUOI, khong phai tong.

Cach dung:
    python3 scripts/check-doc-anchors.py [thu-muc]    # mac dinh: docs
Exit code 1 neu con loi, 0 neu sach - dung duoc trong CI.
"""

import os
import re
import sys
import glob
import unicodedata

HEADING_PATTERN = re.compile(r"^#{1,6}\s+(.*)$", re.MULTILINE)
LINK_PATTERN = re.compile(r"\[([^\]]*)\]\(([^)]+)\)")
EXTERNAL_PREFIXES = ("http://", "https://", "mailto:", "#!")


def to_slug(heading_text):
    """Chuyen mot dong heading thanh anchor slug theo quy tac github-slugger."""
    text = heading_text.strip().lower().replace("`", "")
    characters = []
    for char in text:
        if char == " ":
            characters.append("-")
        elif char.isalnum() or char in "-_":
            characters.append(char)
        elif unicodedata.category(char).startswith("M"):
            characters.append(char)
    return "".join(characters)


def collect_anchors(content):
    return {to_slug(heading) for heading in HEADING_PATTERN.findall(content)}


FENCE_PATTERN = re.compile(r"^```.*?^```", re.MULTILINE | re.DOTALL)
INLINE_CODE_PATTERN = re.compile(r"`[^`\n]*`")


def strip_code(content):
    """Bo fenced block va inline code truoc khi do link.

    Bat buoc: kho tai lieu nay trich dan chinh cu phap link va wiki-link ben
    trong backtick de minh hoa RULE-001. Do nguyen van se bao duong tinh gia.
    """
    content = FENCE_PATTERN.sub("", content)
    return INLINE_CODE_PATTERN.sub("", content)


def check_file(path):
    """Tra ve danh sach loi cua mot file duoi dang (loai, link)."""
    with open(path, encoding="utf-8") as handle:
        raw = handle.read()
    content = strip_code(raw)

    anchors = collect_anchors(raw)
    base_dir = os.path.dirname(path)
    errors = []

    for _, link in LINK_PATTERN.findall(content):
        if link.startswith(EXTERNAL_PREFIXES):
            continue
        file_part, _, fragment = link.partition("#")
        if file_part:
            target = os.path.normpath(os.path.join(base_dir, file_part))
            if not os.path.exists(target):
                errors.append(("LINK GAY", link))
        elif fragment and fragment not in anchors:
            errors.append(("ANCHOR GAY", "#" + fragment))

    return errors


def main():
    root = sys.argv[1] if len(sys.argv) > 1 else "docs"
    total = 0

    for path in sorted(glob.glob(os.path.join(root, "**", "*.md"), recursive=True)):
        errors = check_file(path)
        if not errors:
            continue
        print(f"\n{path}  ({len(errors)} loi)")
        for kind, link in errors:
            print(f"  [{kind}] {link}")
        total += len(errors)

    print(f"\nTONG: {total} loi tren cay thu muc '{root}'")
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())
