# AI Coding
"""
lint_page_prompt.py
Deterministic linter cho page YAML (`mvp0/pages/<page_id>.yaml`) theo template
`mvp0/prompt-template.txt`. KHONG goi LLM — chi kiem tra cau truc, tham chieu
cheo, va bat bien layout/typeset bang code thuan (D-34 / SRS-FR-17).

Muc dich: bat loi truoc khi page YAML duoc dua vao `run_mvp0.py pages`, vi
loi cau truc (rows khong khop 1.0, panel thieu character_id hop le, text
render vao anh...) chi lo ra sau khi da ton chi phi sinh anh that.

Cach dung:
    python3 scripts/mvp0/lint_page_prompt.py mvp0/pages/
    python3 scripts/mvp0/lint_page_prompt.py mvp0/pages/ch01_page001.yaml

Moi dong output la mot finding: "<file>: ERROR|WARN <code> <message>".
Exit code 0 neu khong co ERROR nao, 1 neu nguoc lai (WARN khong lam fail).

Khi lint ca thu muc, cac check ve panel_index (L05) duoc gop tren toan bo
tap file de kiem tra tinh lien tuc 1..N tren toan chuong.
"""

import pathlib
import sys

import yaml

TOLERANCE = 0.001


def _fmt(finding):
    file_name, level, code, message = finding
    return "{}: {} {} {}".format(file_name, level, code, message)


def _get(data, *path, default=None):
    current = data
    for key in path:
        if not isinstance(current, dict) or key not in current:
            return default
        current = current[key]
    return current


def check_top_level_keys(file_name, data):
    findings = []
    required = ["page", "characters", "panels", "style", "negative_constraints"]
    for key in required:
        if key not in data:
            findings.append((file_name, "ERROR", "L01", "missing top-level key '{}'".format(key)))
    if _get(data, "page", "layout", "rows") is None:
        findings.append((file_name, "ERROR", "L01", "missing page.layout.rows"))
    return findings


def check_rows_sum_and_order(file_name, data):
    findings = []
    rows = _get(data, "page", "layout", "rows", default=[])
    if not rows:
        return findings
    sorted_rows = sorted(rows, key=lambda row: row.get("y", 0))
    total_h = sum(row.get("h", 0) for row in rows)
    if abs(total_h - 1.0) > TOLERANCE:
        findings.append((file_name, "ERROR", "L02", "sum of rows[].h = {} (expected 1.0)".format(total_h)))
    expected_y = 0.0
    for row in sorted_rows:
        actual_y = row.get("y", 0)
        if abs(actual_y - expected_y) > TOLERANCE:
            findings.append((
                file_name, "ERROR", "L02",
                "row {} y={} does not match cumulative h={}".format(row.get("row"), actual_y, expected_y),
            ))
        expected_y += row.get("h", 0)
    return findings


def check_panel_row_membership(file_name, data):
    findings = []
    rows = _get(data, "page", "layout", "rows", default=[])
    panels = _get(data, "panels", default=[])
    panel_by_id = {panel.get("id"): panel for panel in panels}
    row_panel_ids = set()
    for row in rows:
        for panel_id in row.get("panels", []):
            row_panel_ids.add(panel_id)
            if panel_id not in panel_by_id:
                findings.append((file_name, "ERROR", "L03", "row {} references unknown panel '{}'".format(row.get("row"), panel_id)))
                continue
            panel = panel_by_id[panel_id]
            if panel.get("row") != row.get("row"):
                findings.append((file_name, "ERROR", "L03", "panel '{}' row={} does not match layout row {}".format(panel_id, panel.get("row"), row.get("row"))))
            if abs(panel.get("relative_height", -1) - row.get("h", 0)) > TOLERANCE:
                findings.append((file_name, "ERROR", "L03", "panel '{}' relative_height does not match row {} h".format(panel_id, row.get("row"))))
        row_width = sum(panel_by_id.get(panel_id, {}).get("relative_width", 0) for panel_id in row.get("panels", []))
        if abs(row_width - 1.0) > TOLERANCE:
            findings.append((file_name, "ERROR", "L03", "row {} relative_width sums to {} (expected 1.0)".format(row.get("row"), row_width)))
    for panel_id in panel_by_id:
        if panel_id not in row_panel_ids:
            findings.append((file_name, "ERROR", "L03", "panel '{}' is not listed in any layout row".format(panel_id)))
    return findings


def check_dominant_panel(file_name, data):
    findings = []
    dominant = _get(data, "page", "layout", "dominant_panel")
    panel_ids = {panel.get("id") for panel in _get(data, "panels", default=[])}
    if dominant is not None and dominant not in panel_ids:
        findings.append((file_name, "ERROR", "L04", "dominant_panel '{}' not found in panels".format(dominant)))
    return findings


def check_panel_index_local(file_name, data):
    findings = []
    panels = _get(data, "panels", default=[])
    seen = set()
    indices = []
    for panel in panels:
        index = panel.get("panel_index")
        if not isinstance(index, int):
            findings.append((file_name, "ERROR", "L05", "panel '{}' missing integer panel_index".format(panel.get("id"))))
            continue
        if index in seen:
            findings.append((file_name, "ERROR", "L05", "duplicate panel_index {} within file".format(index)))
        seen.add(index)
        indices.append(index)
    return findings, indices


def check_panel_index_global(all_indices):
    findings = []
    duplicates = {index for index in all_indices if all_indices.count(index) > 1}
    for index in sorted(duplicates):
        findings.append(("<all files>", "ERROR", "L05", "duplicate panel_index {} across files".format(index)))
    unique_sorted = sorted(set(all_indices))
    if unique_sorted:
        expected = list(range(1, unique_sorted[-1] + 1))
        gaps = [index for index in expected if index not in unique_sorted]
        if gaps:
            findings.append(("<all files>", "WARN", "L05", "panel_index gaps in 1..N range: {}".format(gaps)))
    return findings


def check_character_count(file_name, data):
    findings = []
    for panel in _get(data, "panels", default=[]):
        count = panel.get("character_count")
        actual = len(panel.get("characters", []))
        if count is not None and count > 3:
            findings.append((file_name, "ERROR", "L06", "panel '{}' character_count={} exceeds 3".format(panel.get("id"), count)))
        if count != actual:
            findings.append((file_name, "ERROR", "L06", "panel '{}' character_count={} does not match len(characters)={}".format(panel.get("id"), count, actual)))
    return findings


def check_character_id_references(file_name, data):
    findings = []
    character_ids = {character.get("id") for character in _get(data, "characters", default=[])}
    for panel in _get(data, "panels", default=[]):
        for character_ref in panel.get("characters", []):
            character_id = character_ref.get("character_id")
            if character_id not in character_ids:
                findings.append((file_name, "ERROR", "L07", "panel '{}' references unknown character_id '{}'".format(panel.get("id"), character_id)))
        for dialogue in _get(panel, "typeset", "dialogue", default=[]):
            speaker = dialogue.get("speaker")
            if speaker not in character_ids:
                findings.append((file_name, "ERROR", "L07", "panel '{}' dialogue speaker '{}' not in characters".format(panel.get("id"), speaker)))
    return findings


def check_silhouette_cues(file_name, data):
    findings = []
    characters = _get(data, "characters", default=[])
    if len(characters) > 3:
        findings.append((file_name, "ERROR", "L08", "characters count={} exceeds 3".format(len(characters))))
    elif len(characters) == 3:
        findings.append((file_name, "WARN", "L08", "characters count=3 (max allowed)"))
    seen = {}
    for character in characters:
        cue = character.get("silhouette_cue")
        if not cue:
            findings.append((file_name, "ERROR", "L08", "character '{}' has empty silhouette_cue".format(character.get("id"))))
            continue
        key = cue.strip().lower()
        if key in seen:
            findings.append((file_name, "ERROR", "L08", "silhouette_cue duplicated between '{}' and '{}'".format(seen[key], character.get("id"))))
        seen[key] = character.get("id")
    return findings


def check_text_policy(file_name, data):
    findings = []
    render_flag = _get(data, "text_policy", "render_text_in_image")
    if render_flag is not False:
        findings.append((file_name, "ERROR", "L09", "text_policy.render_text_in_image must be exactly false"))
    for panel in _get(data, "panels", default=[]):
        zones = panel.get("text_safe_zone")
        if not zones:
            findings.append((file_name, "ERROR", "L09", "panel '{}' has no text_safe_zone".format(panel.get("id"))))
            continue
        for zone in zones:
            if any(key not in zone for key in ("x", "y", "w", "h")):
                findings.append((file_name, "ERROR", "L09", "panel '{}' text_safe_zone missing x/y/w/h".format(panel.get("id"))))
                continue
            if not all(0 <= zone[key] <= 1 for key in ("x", "y", "w", "h")):
                findings.append((file_name, "ERROR", "L09", "panel '{}' text_safe_zone values out of [0,1]".format(panel.get("id"))))
            if zone["x"] + zone["w"] > 1 + TOLERANCE:
                findings.append((file_name, "ERROR", "L09", "panel '{}' text_safe_zone x+w > 1".format(panel.get("id"))))
            if zone["y"] + zone["h"] > 1 + TOLERANCE:
                findings.append((file_name, "ERROR", "L09", "panel '{}' text_safe_zone y+h > 1".format(panel.get("id"))))
    return findings


def check_canonical_reference_exists(file_name, data, repo_root):
    findings = []
    for character in _get(data, "characters", default=[]):
        ref_path = character.get("canonical_reference")
        if not ref_path:
            continue
        if not (repo_root / ref_path).exists():
            findings.append((file_name, "WARN", "L10", "canonical_reference not found on disk: {}".format(ref_path)))
    return findings


def check_negative_constraints_duplication(file_name, data):
    findings = []
    continuity_text = " ".join(str(value) for value in _flatten(_get(data, "page", "continuity", default={}))).lower()
    for constraint in _get(data, "negative_constraints", default=[]):
        if constraint and constraint.strip().lower() in continuity_text:
            findings.append((file_name, "WARN", "L11", "negative_constraint duplicates continuity text: '{}'".format(constraint)))
    return findings


def _flatten(value):
    if isinstance(value, dict):
        for item in value.values():
            for leaf in _flatten(item):
                yield leaf
    elif isinstance(value, list):
        for item in value:
            for leaf in _flatten(item):
                yield leaf
    elif value is not None:
        yield value


def check_page_id_matches_stem(file_name, data, stem):
    findings = []
    page_id = _get(data, "page", "page_id")
    if not page_id:
        return findings
    import re
    if not re.match(r"^ch\d{2}_page\d{3}$", str(page_id)):
        findings.append((file_name, "WARN", "L12", "page_id '{}' does not match ^ch\\d{{2}}_page\\d{{3}}$".format(page_id)))
    if page_id != stem:
        findings.append((file_name, "WARN", "L12", "page_id '{}' does not match file stem '{}'".format(page_id, stem)))
    return findings


def lint_file(path, repo_root):
    file_name = str(path)
    with open(path, "r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):
        return [(file_name, "ERROR", "L01", "file is empty or not a mapping")], []

    findings = []
    findings.extend(check_top_level_keys(file_name, data))
    findings.extend(check_rows_sum_and_order(file_name, data))
    findings.extend(check_panel_row_membership(file_name, data))
    findings.extend(check_dominant_panel(file_name, data))
    index_findings, indices = check_panel_index_local(file_name, data)
    findings.extend(index_findings)
    findings.extend(check_character_count(file_name, data))
    findings.extend(check_character_id_references(file_name, data))
    findings.extend(check_silhouette_cues(file_name, data))
    findings.extend(check_text_policy(file_name, data))
    findings.extend(check_canonical_reference_exists(file_name, data, repo_root))
    findings.extend(check_negative_constraints_duplication(file_name, data))
    findings.extend(check_page_id_matches_stem(file_name, data, path.stem))
    return findings, indices


def collect_target_files(target_path):
    if target_path.is_dir():
        return sorted(
            path for path in target_path.glob("*.yaml")
            if path.stem.lower() != "readme"
        )
    return [target_path]


def main():
    if len(sys.argv) != 2:
        print("usage: python3 scripts/mvp0/lint_page_prompt.py <dir-or-file>")
        return 1

    target_path = pathlib.Path(sys.argv[1])
    if not target_path.exists():
        print("path not found: {}".format(target_path))
        return 1

    repo_root = pathlib.Path(__file__).resolve().parents[2]
    files = collect_target_files(target_path)
    if not files:
        print("no yaml files found under {}".format(target_path))
        return 1

    all_findings = []
    all_indices = []
    for path in files:
        findings, indices = lint_file(path, repo_root)
        all_findings.extend(findings)
        all_indices.extend(indices)

    if target_path.is_dir():
        all_findings.extend(check_panel_index_global(all_indices))

    for finding in all_findings:
        print(_fmt(finding))

    has_error = any(level == "ERROR" for _, level, _, _ in all_findings)
    return 1 if has_error else 0


if __name__ == "__main__":
    sys.exit(main())
