#!/usr/bin/env python3
"""
build_aditya_repo_cards.py
Generates the 3 featured repository cards matching Avi Vashishta's exact SVG architecture:
1. NOVATRACE (Pixel-Nova-v1-1/NOVATRACE)
2. AmoghaFoundation (Pixel-Nova-v1-1/AmoghaFoundation)
3. ZeStay (Pixel-Nova-v1-1/ZeStay)
"""

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTS_CSS_PATH = os.path.join(BASE_DIR, "data", "repo_fonts.css")
CARDS_DIR = os.path.join(BASE_DIR, "cards")

REPOS_CONFIG = [
    {
        "filename": "repo-novatrace.svg",
        "title": "NOVATRACE",
        "lines": [
            "AI email threat detection and",
            "forensics engine analyzing phishing,",
            "DKIM vectors &amp; anomalous headers."
        ],
        "footer": "Python  ·  Security ML",
        "accent": "#2f55ff",
        "delay": 4.60
    },
    {
        "filename": "repo-amogha.svg",
        "title": "AmoghaFoundation",
        "lines": [
            "Custom WordPress theme built for",
            "NGO website to showcase welfare work",
            "with easy-to-maintain templates."
        ],
        "footer": "PHP  ·  Internship",
        "accent": "#ef3b2d",
        "delay": 4.75
    },
    {
        "filename": "repo-zestay.svg",
        "title": "ZeStay",
        "lines": [
            "Smart PG and roommate discovery",
            "platform with compatibility matching",
            "and verified student housing."
        ],
        "footer": "React  ·  Fullstack",
        "accent": "#f5a623",
        "delay": 4.90
    }
]


def render_repo_card(cfg, css_content):
    title = cfg["title"]
    lines = cfg["lines"]
    footer = cfg["footer"]
    accent = cfg["accent"]
    delay = cfg["delay"]
    
    # In XML, ampersands in attributes and text must be &amp;
    safe_lines = [l if "&amp;" in l else l.replace("&", "&amp;") for l in lines]
    aria_label = f"{title}: " + " ".join(safe_lines)
    
    desc_xml = "".join([
        f'<text x="24" y="{72 + i * 21}" font-family="Geist, system-ui, -apple-system, sans-serif" font-size="14" fill="#3a3a3c">{line}</text>'
        for i, line in enumerate(safe_lines)
    ])

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="293.333" height="188" viewBox="0 0 293.333 188" role="img" aria-label="{aria_label}"><title>{aria_label}</title><style>{css_content}</style>
<rect width="285.3333333333333" height="176" rx="14" fill="#f3f3f1"/>
<g class="r" style="animation-delay:{delay:.2f}s">
  <rect x="24" y="30" width="8" height="8" rx="2" fill="{accent}"/>
  <text x="40" y="39" font-family="Geist, system-ui, -apple-system, sans-serif" font-weight="600" font-size="18" fill="#111111">{title}</text>
  {desc_xml}
  <text x="24" y="152" font-family="'Geist Mono', ui-monospace, SFMono-Regular, Menlo, monospace" font-size="12" fill="#6e6e73">{footer}</text>
</g>
</svg>'''
    return svg


def build_all_repo_cards():
    with open(FONTS_CSS_PATH, "r", encoding="utf-8") as f:
        css_content = f.read().strip()

    os.makedirs(CARDS_DIR, exist_ok=True)
    generated = []

    for cfg in REPOS_CONFIG:
        svg_content = render_repo_card(cfg, css_content)
        
        # Write to primary target
        primary_path = os.path.join(CARDS_DIR, cfg["filename"])
        with open(primary_path, "w", encoding="utf-8") as f:
            f.write(svg_content)
        generated.append(primary_path)

        print(f"[✓] Generated {cfg['filename']} (length: {len(svg_content)})")

    return generated


if __name__ == "__main__":
    build_all_repo_cards()
