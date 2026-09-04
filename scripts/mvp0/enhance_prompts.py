# AI Coding
"""
enhance_prompts.py
Su dung Qwen3.7-Plus de chuan hoa, chi tiet hoa va dong bo tinh lien mach
(visual and narrative continuity) cho toan bo cac panel cua mot chuong comic.

Dau vao:
  - mvp0/story-bible.yaml (nhan vat, trang thai, nhan dang)
  - mvp0/panel-script-chX.yaml (pages, panels, camera, beat, constraints)

Dau ra:
  - Truong `enhanced_prompt` duoc ghi thang vao tung panel trong panel script YAML.
"""

import os
import sys
import yaml
import pathlib
import argparse
from openai import OpenAI

ROOT = pathlib.Path(__file__).resolve().parents[2]
MVP0 = ROOT / "mvp0"

SYSTEM_PROMPT = """You are the Lead Visual Prompt Director for a premium Dark Xianxia Manhwa/Webcomic (similar to Solo Leveling, Reaper of the Drifting Moon, Nano Machine).
Your mission is to transform raw comic script panel specifications into rich, highly-detailed, production-ready visual prompts for an advanced image generation AI.

CRITICAL DIRECTIVES:
1. ART STYLE:
   Always enforce: "2D manhwa webcomic art style, dark xianxia fantasy comic art, graphic novel panel, clean sharp black ink lineart, flat cel shading with crisp shadow edges, dramatic high contrast, professional digital webtoon illustration, no 3D CGI, no 3D render, no photography, no 3D game engine".

2. VISUAL CONTINUITY ACROSS PAGES & PANELS:
   - Ensure the lighting, weather, time of day, and environmental props smoothly connect from the PREVIOUS panel and lead into the NEXT panel.
   - In flashbacks, maintain warm golden candlelight, opulent clan hall architecture, and soft luminous vignette edges.
   - In the cemetery graveyard, maintain oppressive pitch-black stormy skies, vivid crimson lightning, cold heavy rain, and crooked mossy tombstones.
   - When the same character appears across sequential panels, keep clothing tears, mud streaks, hair dishevelment, and injuries strictly consistent.

3. PANEL FRAMING & ANTI-MODEL-SHEET CONSTRAINTS:
   - For character panels: specify exact dynamic kinetic anatomy, body tension, expressive facial acting, cloth folds, camera perspective (e.g. low-angle foreshortening, dutch tilt), and tight integration with the environment.
     MUST include: "Single narrative comic book panel frame, storytelling scene, NOT a character model sheet, NOT multiple views, NOT isolated on white background, NOT standing on blank void".
   - For scenery/environment panels (0 characters): specify architectural details, weather FX, foreground/midground/background depth planes.
     MUST include: "Atmospheric establishing scenery and environment comic panel, pure scenery background, NO humans, NO people, NO characters, NO faces in frame".

4. LANGUAGE:
   Output ONLY the final expanded visual prompt in English as a single coherent paragraph. Do NOT include greetings, markdown headings, or conversational commentary.
"""


def load_bible():
    data = yaml.safe_load((MVP0 / "story-bible.yaml").read_text(encoding="utf-8"))
    return {entity["id"]: entity for entity in data["nhan_vat"]}


def get_client():
    api_key = os.environ.get("DASHSCOPE_API_KEY")
    if not api_key:
        raise RuntimeError("Thieu bien moi truong DASHSCOPE_API_KEY")
    return OpenAI(
        api_key=api_key,
        base_url="https://dashscope-intl.aliyuncs.com/compatible-mode/v1"
    )


def build_panel_context(panel, prev_p, next_p, bible):
    chars_info = []
    for cid in panel.get("characters", []):
        entity = bible.get(cid, {})
        name = entity.get("ten_en") or entity.get("ten", cid)
        ref = entity.get("canonical_reference_en") or entity.get("canonical_reference", {})
        chars_info.append(f"- {name}: {ref.get('khuon_mat', '')} {ref.get('toc', '')} {ref.get('trang_phuc', '')}")

    lines = [
        f"Panel {panel['panel_index']} (Page {panel.get('page_no', '?')}):",
        f"- Action: {panel.get('action_en') or panel.get('action')}",
        f"- Camera: {panel.get('camera', {})}",
        f"- Beat type: {panel.get('beat_type', '')}",
        f"- Visual constraints: {panel.get('visual_constraints_en') or panel.get('visual_constraints', {})}",
    ]
    if chars_info:
        lines.append("Characters in this panel:\n  " + "\n  ".join(chars_info))
    else:
        lines.append("Characters in this panel: NONE (Pure scenery/FX)")

    if prev_p:
        lines.insert(0, f"PREVIOUS PANEL {prev_p['panel_index']}: {prev_p.get('action_en') or prev_p.get('action')}")
    if next_p:
        lines.append(f"NEXT PANEL {next_p['panel_index']}: {next_p.get('action_en') or next_p.get('action')}")

    return "\n".join(lines)


def enhance_chapter(chapter_name, dry_run=False):
    client = get_client()
    bible = load_bible()
    script_path = MVP0 / f"panel-script-{chapter_name}.yaml"
    data = yaml.safe_load(script_path.read_text(encoding="utf-8"))

    all_panels = []
    for page in data["pages"]:
        for panel in page["panels"]:
            all_panels.append(panel)

    print(f"=== Chuẩn hóa & Chi tiết hóa Prompt cho {len(all_panels)} panel ({chapter_name}) ===")

    for i, panel in enumerate(all_panels):
        idx = panel["panel_index"]
        if panel.get("enhanced_prompt"):
            print(f"[Panel {idx:02d}] Đã có enhanced prompt ({len(panel['enhanced_prompt'])} chars) — bỏ qua")
            continue

        prev_p = all_panels[i - 1] if i > 0 else None
        next_p = all_panels[i + 1] if i < len(all_panels) - 1 else None
        user_prompt = build_panel_context(panel, prev_p, next_p, bible)

        print(f"\n[Panel {idx:02d}] Đang chuẩn hóa qua Qwen3.7-Plus...")

        if dry_run:
            print("  (Dry run - bỏ qua API call)")
            continue

        resp = client.chat.completions.create(
            model="qwen3.7-plus",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Generate the enhanced visual prompt for this panel:\n\n{user_prompt}"}
            ],
            temperature=0.7
        )
        enhanced = resp.choices[0].message.content.strip()
        panel["enhanced_prompt"] = enhanced
        print(f"  ✓ Prompt ({len(enhanced)} chars): {enhanced[:90]}...")
        script_path.write_text(yaml.dump(data, allow_unicode=True, sort_keys=False), encoding="utf-8")

    print(f"\n✅ Hoàn tất toàn bộ {len(all_panels)} enhanced prompts trong {script_path}")


def main():
    parser = argparse.ArgumentParser(description="Chuẩn hóa prompt comic panel qua Qwen3.7-Plus")
    parser.add_argument("--chapter", default="ch1", choices=["ch1", "ch2"])
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    enhance_chapter(args.chapter, args.dry_run)


if __name__ == "__main__":
    sys.exit(main())
