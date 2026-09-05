# AI Coding
"""
crop_page.py
Cat MOT anh trang (sinh boi run_mvp0.py stage `pages`, D-1) thanh tung anh
panel rieng, theo hinh hoc khai bao trong `layout.rows` cua page YAML.

⛔ Thuan tuy hinh hoc — ⛔ khong LLM, ⛔ khong VLM. G1 van cham THEO TUNG
PANEL (golden-dataset/panels/panel-NNN/, scoring-sheet.csv cot panel_index)
nen buoc nay BAT BUOC chay sau khi co anh trang, truoc khi cham G1.

Cach tinh box (pixel) cua tung panel:
  - Truc doc: row["y"], row["h"] (ty le 0-1 cua chieu cao trang).
  - Truc ngang: cong don `relative_width` cua cac panel TRONG CUNG MOT ROW,
    theo thu tu khai bao trong row["panels"] — thu tu nay DA la thu tu doc
    trai-sang-phai neu `page.reading_direction = left_to_right` (mac dinh);
    neu `right_to_left` thi panel DAU TIEN trong danh sach nam BEN PHAI.

Cach dung:
    python3 scripts/mvp0/crop_page.py mvp0/pages/ch01_page001.yaml <page.png> --out <dir>

Dau ra:
    <out>/panel-<panel_index:03d>.png  (moi panel mot file)
    <out>/crop-manifest.json           (page_id, image, box pixel tung panel)
"""

import sys
import json
import pathlib
import argparse

import yaml
from PIL import Image


def _row_lookup(layout):
    rows = layout.get("rows", [])
    by_panel_id = {}
    for row in rows:
        by_panel_id.update({panel_id: row for panel_id in row.get("panels", [])})
    return rows, by_panel_id


def _panel_x_span(panel_id, row, panels_by_id, reading_direction):
    panel_ids = row.get("panels", [])
    ordered = panel_ids if reading_direction != "right_to_left" else list(reversed(panel_ids))

    x = 0.0
    for pid in ordered:
        width = panels_by_id[pid].get("relative_width", 0.0)
        if pid == panel_id:
            return x, x + width
        x += width
    raise KeyError(f"Panel '{panel_id}' ⛔ khong nam trong row['panels'] cua layout")


def compute_panel_boxes(page_doc, image_size):
    """Tra list dict {panel_index, panel_id, box} — box la pixel (left, top, right, bottom)."""
    page = page_doc["page"]
    layout = page["layout"]
    reading_direction = page.get("reading_direction", "left_to_right")
    rows, row_by_panel_id = _row_lookup(layout)
    panels_by_id = {panel["id"]: panel for panel in page_doc.get("panels", [])}

    width_px, height_px = image_size
    boxes = []
    for panel in page_doc.get("panels", []):
        panel_id = panel["id"]
        row = row_by_panel_id.get(panel_id)
        if row is None:
            raise KeyError(f"Panel '{panel_id}' ⛔ khong xuat hien trong bat ky row nao cua layout")

        x0, x1 = _panel_x_span(panel_id, row, panels_by_id, reading_direction)
        y0, y1 = row["y"], row["y"] + row["h"]

        if "panel_index" not in panel:
            raise KeyError(f"Panel '{panel_id}' thieu panel_index — chay lint_page_prompt.py truoc")
        panel_index = panel["panel_index"]
        boxes.append({
            "panel_index": panel_index,
            "panel_id": panel_id,
            "box": [round(x0 * width_px), round(y0 * height_px),
                    round(x1 * width_px), round(y1 * height_px)],
        })
    return boxes


def crop_page(page_yaml_path, image_path, out_dir):
    page_doc = yaml.safe_load(pathlib.Path(page_yaml_path).read_text(encoding="utf-8"))
    page_id = page_doc["page"]["page_id"]

    image = Image.open(image_path)
    boxes = compute_panel_boxes(page_doc, image.size)

    out_dir = pathlib.Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    manifest = {"page_id": page_id, "image": str(image_path), "panels": []}
    for entry in boxes:
        crop = image.crop(tuple(entry["box"]))
        out_path = out_dir / f"panel-{entry['panel_index']:03d}.png"
        crop.save(out_path)
        manifest["panels"].append(entry)

    (out_dir / "crop-manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    return manifest


def main():
    parser = argparse.ArgumentParser(description="Cat anh trang thanh panel theo layout.rows")
    parser.add_argument("page_yaml", help="Duong dan mvp0/pages/<page_id>.yaml")
    parser.add_argument("page_image", help="Anh trang da sinh (png)")
    parser.add_argument("--out", required=True, help="Thu muc dau ra")
    args = parser.parse_args()

    manifest = crop_page(args.page_yaml, args.page_image, args.out)
    print(f"Cat {len(manifest['panels'])} panel tu {manifest['image']} -> {args.out}")
    for entry in manifest["panels"]:
        print(f"  panel-{entry['panel_index']:03d}  ({entry['panel_id']})  box={entry['box']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
