#!/usr/bin/env python3
"""
build_aditya_world_cards.py
Generates the Three World cards (ENGINEERING, BUILDING, RECOGNITION) in Avi Vashishta's exact
vibrant solid card layout:
1. build.svg (Solid Blue #2f55ff - Computer Engineering)
2. agents.svg (Solid Red #ef3b2d - 8 Repos)
3. learn.svg (Solid Gold #f5a623 - 5 Recognitions)
"""

import os
import xml.etree.ElementTree as ET

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTS_CSS_PATH = os.path.join(BASE_DIR, "data", "hero_fonts.css")
CARDS_DIR = os.path.join(BASE_DIR, "cards")

WORLD_CONFIGS = [
    {
        "filename": "build.svg",
        "tag": "ENGINEERING",
        "badge_x": 120,
        "title": ["Computer", "Engineering"],
        "lines": [
            "Learning, experimenting and",
            "engineering beyond the",
            "classroom."
        ],
        "bg": "#2f55ff",
        "text_color": "#ffffff",
        "body_color": "#ffffff",
        "body_opacity": "0.92",
        "delay": 3.40
    },
    {
        "filename": "agents.svg",
        "tag": "BUILDING",
        "badge_x": 96,
        "title": "8 Repos",
        "title_size": 38,
        "lines": [
            "Projects, experiments and ideas",
            "brought to life."
        ],
        "bg": "#ef3b2d",
        "text_color": "#ffffff",
        "body_color": "#ffffff",
        "body_opacity": "0.92",
        "delay": 3.55
    },
    {
        "filename": "learn.svg",
        "tag": "RECOGNITION",
        "badge_x": 120,
        "title": "5 Recognitions",
        "title_size": 34,
        "lines": [
            "3 First-place finishes · 2 Second-",
            "place finishes."
        ],
        "bg": "#f5a623",
        "text_color": "#111111",
        "body_color": "#111111",
        "body_opacity": "0.88",
        "delay": 3.70
    }
]


def render_world_card(cfg, css_content):
    tag = cfg["tag"]
    badge_x = cfg["badge_x"]
    title = cfg["title"]
    lines = cfg["lines"]
    bg = cfg["bg"]
    tc = cfg["text_color"]
    bc = cfg["body_color"]
    b_op = cfg["body_opacity"]
    delay = cfg["delay"]

    safe_lines = [l if "&amp;" in l else l.replace("&", "&amp;") for l in lines]
    
    if isinstance(title, list):
        title_str = " ".join(title)
        title_xml = (
            f'<text x="22" y="72" font-family="\'Instrument Serif\', Georgia, serif" font-style="italic" font-size="30" fill="{tc}">{title[0]}</text>\n'
            f'  <text x="22" y="100" font-family="\'Instrument Serif\', Georgia, serif" font-style="italic" font-size="30" fill="{tc}">{title[1]}</text>'
        )
    else:
        title_str = title
        tsize = cfg.get("title_size", 38)
        title_xml = f'<text x="22" y="92" font-family="\'Instrument Serif\', Georgia, serif" font-style="italic" font-size="{tsize}" fill="{tc}">{title}</text>'

    aria_label = f"{tag}: {title_str}. " + " ".join(safe_lines)

    # Calculate body lines layout
    if len(safe_lines) == 3:
        font_size = 12
        desc_xml = "\n  ".join([
            f'<text x="24" y="{126 + i * 17}" font-family="Geist, system-ui, -apple-system, sans-serif" font-size="{font_size}" fill="{bc}" opacity="{b_op}">{l}</text>'
            for i, l in enumerate(safe_lines)
        ])
    else:
        font_size = 13
        desc_xml = "\n  ".join([
            f'<text x="24" y="{128 + i * 18}" font-family="Geist, system-ui, -apple-system, sans-serif" font-size="{font_size}" fill="{bc}" opacity="{b_op}">{l}</text>'
            for i, l in enumerate(safe_lines)
        ])

    badge_xml = (
        f'<g class="n">\n'
        f'    <rect x="{badge_x}" y="27" width="14" height="14" rx="3" fill="#58a6ff"/>\n'
        f'    <path d="M{badge_x + 3.5} 37.5 L{badge_x + 10.5} 30.5 M{badge_x + 6.5} 30.5 H{badge_x + 10.5} V34.5" stroke="#ffffff" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round" fill="none"/>\n'
        f'  </g>'
    )

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="293.333" height="188" viewBox="0 0 293.333 188" role="img" aria-label="{aria_label}"><title>{aria_label}</title><style>{css_content}</style>
<rect width="285.3333333333333" height="176" rx="14" fill="{bg}"/>
<g class="r" style="animation-delay:{delay:.2f}s">
  <text x="24" y="38" font-family="'Geist Mono', ui-monospace, SFMono-Regular, Menlo, monospace" font-size="11" font-weight="700" letter-spacing="1.2" fill="{tc}">{tag}</text>
  {badge_xml}
  {title_xml}
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
        # XML sanity check
        try:
            ET.fromstring(svg_content)
        except ET.ParseError as e:
            raise ValueError(f"XML parse error in {cfg['filename']}: {e}")

        card_path = os.path.join(CARDS_DIR, cfg["filename"])
        with open(card_path, "w", encoding="utf-8") as f:
            f.write(svg_content)
        generated.append(card_path)
        print(f"[✓] Generated {cfg['filename']} (length: {len(svg_content)})")

    return generated


if __name__ == "__main__":
    build_all_world_cards()
