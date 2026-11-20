#!/usr/bin/env python3
"""
build_aditya_world_cards.py
Generates the Three World cards (BUILD, AGENTS, LEARN) in Avi Vashishta's exact
vibrant solid card layout:
1. build.svg (Solid Blue #2f55ff)
2. agents.svg (Solid Red #ef3b2d)
3. learn.svg (Solid Gold #f5a623)
"""

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTS_CSS_PATH = os.path.join(BASE_DIR, "data", "hero_fonts.css")
CARDS_DIR = os.path.join(BASE_DIR, "cards")

WORLD_CONFIGS = [
    {
        "filename": "build.svg",
        "tag": "BUILD",
        "title": "4 systems",
        "lines": [
            "Fullstack applications, real-time HUDs",
            "&amp; clinical scheduling engines."
        ],
        "bg": "#2f55ff",
        "text_color": "#ffffff",
        "body_color": "#ffffff",
        "body_opacity": "0.92",
        "delay": 3.40
    },
    {
        "filename": "agents.svg",
        "tag": "AGENTS",
        "title": "Realtime AI",
        "lines": [
            "Autonomous decision models, MediaPipe",
            "vision tracking &amp; threat forensics."
        ],
        "bg": "#ef3b2d",
        "text_color": "#ffffff",
        "body_color": "#ffffff",
        "body_opacity": "0.92",
        "delay": 3.55
    },
    {
        "filename": "learn.svg",
        "tag": "LEARN",
        "title": "Engineering",
        "lines": [
            "Computer engineering, low-level",
            "systems &amp; a2zcoder404.com."
        ],
        "bg": "#f5a623",
        "text_color": "#111111",
        "body_color": "#111111",
        "body_opacity": "0.85",
        "delay": 3.70
    }
]


def render_world_card(cfg, css_content):
    tag = cfg["tag"]
    title = cfg["title"]
    lines = cfg["lines"]
    bg = cfg["bg"]
    tc = cfg["text_color"]
    bc = cfg["body_color"]
    b_op = cfg["body_opacity"]
    delay = cfg["delay"]

    safe_lines = [l if "&amp;" in l else l.replace("&", "&amp;") for l in lines]
    aria_label = f"{tag}: {title}. " + " ".join(safe_lines)

    desc_xml = "".join([
        f'<text x="24" y="{128 + i * 20}" font-family="Geist, system-ui, -apple-system, sans-serif" font-size="13" fill="{bc}" opacity="{b_op}">{l}</text>'
        for i, l in enumerate(safe_lines)
    ])

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="293.333" height="188" viewBox="0 0 293.333 188" role="img" aria-label="{aria_label}"><title>{aria_label}</title><style>{css_content}</style>
<rect width="285.3333333333333" height="176" rx="14" fill="{bg}"/>
<g class="r" style="animation-delay:{delay:.2f}s">
  <text x="24" y="38" font-family="'Geist Mono', ui-monospace, SFMono-Regular, Menlo, monospace" font-size="11" font-weight="700" letter-spacing="1.2" fill="{tc}">{tag}</text>
  <text class="n" x="254" y="38" font-family="'Geist Mono', ui-monospace, SFMono-Regular, Menlo, monospace" font-size="14" font-weight="700" fill="{tc}">→</text>
  <text x="22" y="94" font-family="'Instrument Serif', Georgia, serif" font-style="italic" font-size="38" fill="{tc}">{title}</text>
  {desc_xml}
</g>
</svg>'''
    return svg


def build_all_world_cards():
    with open(FONTS_CSS_PATH, "r", encoding="utf-8") as f:
        css_content = f.read().strip()

    os.makedirs(CARDS_DIR, exist_ok=True)
    generated = []

    for cfg in WORLD_CONFIGS:
        svg_content = render_world_card(cfg, css_content)
        card_path = os.path.join(CARDS_DIR, cfg["filename"])
        with open(card_path, "w", encoding="utf-8") as f:
            f.write(svg_content)
        generated.append(card_path)
        print(f"[✓] Generated {cfg['filename']} (length: {len(svg_content)})")

    return generated


if __name__ == "__main__":
    build_all_world_cards()
