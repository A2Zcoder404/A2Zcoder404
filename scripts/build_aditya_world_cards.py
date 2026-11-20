#!/usr/bin/env python3
"""
build_aditya_world_cards.py
Generates the Three World cards (ENGINEERING, BUILDING, ACHIEVEMENTS) matching Avi Vashishta's
exact animation architecture and dimensions:
- Dimensions: 293.333 x 222 (viewBox 0 0 293.333 222)
- Inner card: 285.333 x 210, rx=14
- Animations: tilein, slidein, arrowin, roll (slot counter roll), sheen sweep, sonar ring
- Embedded WOFF fonts: Instrument Serif (normal + italic), Geist, Geist Mono

Cards:
1. cards/build.svg (Solid Blue #2f55ff - Computer Engineering)
2. cards/agents.svg (Solid Red #ef3b2d - 8 Repos)
3. cards/learn.svg (Solid Gold #f5a623 - 5 Awards)
"""

import os
import xml.etree.ElementTree as ET

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTS_CSS_PATH = os.path.join(BASE_DIR, "data", "hero_fonts.css")
CARDS_DIR = os.path.join(BASE_DIR, "cards")

ANIMATION_CSS = """
@keyframes rise{from{opacity:0;transform:translateY(16px)}to{opacity:1;transform:none}}
@keyframes fade{from{opacity:0}to{opacity:1}}
@keyframes grow{from{transform:scaleY(0)}to{transform:scaleY(1)}}
@keyframes pop{0%{opacity:0;transform:scale(.3)}70%{opacity:1;transform:scale(1.15)}100%{opacity:1;transform:none}}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.25}}
@keyframes nudge{0%,100%{transform:none}50%{transform:translateX(4px)}}
@keyframes nudgeup{0%,100%{transform:none}50%{transform:translate(3px,-3px)}}
.r{opacity:0;animation:rise .8s cubic-bezier(.2,.7,.2,1) both;transform-box:fill-box}
.f{opacity:0;animation:fade .9s ease-out both}
.g{transform-box:fill-box;transform-origin:bottom;transform:scaleY(0);animation:grow .8s cubic-bezier(.2,.7,.2,1) both}
.p{opacity:0;transform-box:fill-box;transform-origin:center;animation:pop .4s ease-out both}
.live{animation:pulse 1.6s ease-in-out infinite}
.n{transform-box:fill-box;animation:nudge 1.8s ease-in-out infinite}
.nu{transform-box:fill-box;animation:nudgeup 1.8s ease-in-out infinite}
@keyframes tilein{0%{opacity:0;transform:translateY(90px) scale(.6) rotate(-9deg)}55%{opacity:1;transform:translateY(-10px) scale(1.05) rotate(2deg)}75%{transform:translateY(3px) scale(.98) rotate(-.8deg)}90%{transform:translateY(-1px) scale(1.01) rotate(.2deg)}100%{opacity:1;transform:none}}
@keyframes slidein{from{opacity:0;transform:translateX(-26px)}to{opacity:1;transform:none}}
@keyframes arrowin{0%{opacity:0;transform:translateX(-30px)}60%{opacity:1;transform:translateX(6px)}100%{opacity:1;transform:none}}
@keyframes roll{from{transform:translateY(60px)}to{transform:none}}
@keyframes sheen{0%{transform:translateX(-260px) skewX(-20deg)}22%,100%{transform:translateX(420px) skewX(-20deg)}}
@keyframes ring{0%{opacity:.7;transform:scale(.2)}100%{opacity:0;transform:scale(2.4)}}
.ti{opacity:0;transform-box:fill-box;transform-origin:50% 60%;animation:tilein 1.1s cubic-bezier(.2,.8,.2,1) both}
.sl{opacity:0;transform-box:fill-box;animation:slidein .6s cubic-bezier(.2,.7,.2,1) both}
.ai{opacity:0;transform-box:fill-box;animation:arrowin .7s cubic-bezier(.2,.7,.2,1) both}
.ro{transform-box:fill-box;animation:roll .8s cubic-bezier(.15,.8,.2,1) both}
.sh{animation:sheen 5s ease-in-out infinite}
.rg{opacity:0;transform-box:fill-box;transform-origin:center;animation:ring 1s ease-out both}
@media (prefers-reduced-motion: reduce){.r,.f,.g,.p,.live,.n,.nu,.ti,.sl,.ai,.ro,.rg{animation:none!important;opacity:1!important;transform:none!important}.sh,.rg{display:none}}
""".strip()

WORLD_CONFIGS = [
    {
        "filename": "build.svg",
        "tag": "ENGINEERING",
        "badge_x": 126,
        "type": "multi_title",
        "title_lines": ["Computer", "Engineering"],
        "lines": [
            "Learning, experimenting and",
            "engineering beyond the",
            "classroom."
        ],
        "bg": "#2f55ff",
        "text_color": "#ffffff",
        "body_color": "#ffffff",
        "body_opacity": "0.92",
        "ring_color": "#ffffff",
        "ring_opacity": "0.5",
        "delay": 3.10
    },
    {
        "filename": "agents.svg",
        "tag": "BUILDING",
        "badge_x": 98,
        "type": "counter_roll",
        "final_num": 8,
        "label": "Repos",
        "roll_values": [0, 1, 2, 3, 4, 5, 6, 7, 8],
        "lines": [
            "Projects, experiments and ideas",
            "brought to life."
        ],
        "bg": "#ef3b2d",
        "text_color": "#ffffff",
        "body_color": "#ffffff",
        "body_opacity": "0.92",
        "ring_color": "#ffffff",
        "ring_opacity": "0.5",
        "delay": 3.35
    },
    {
        "filename": "learn.svg",
        "tag": "ACHIEVEMENTS",
        "badge_x": 134,
        "type": "counter_roll",
        "final_num": 5,
        "label": "Awards",
        "roll_values": [0, 1, 2, 3, 4, 5],
        "lines": [
            "3 First-place · 2 Second-place finishes."
        ],
        "bg": "#f5a623",
        "text_color": "#111111",
        "body_color": "#111111",
        "body_opacity": "0.88",
        "ring_color": "#111111",
        "ring_opacity": "0.20",
        "delay": 3.60
    }
]


def render_slot_counter(values, label, text_color, delay_start, duration=0.8):
    """
    Renders SVG text frames for counter slot animation matching Avi's exact technique.
    """
    num_steps = len(values)
    step_duration = duration / num_steps
    xml_parts = []
    
    for i, val in enumerate(values):
        t_begin = delay_start + i * step_duration
        t_next = delay_start + (i + 1) * step_duration
        
        if i == num_steps - 1:
            # Final resting frame remains visible
            xml_parts.append(
                f'<text x="22" y="112" font-family="\'Instrument Serif\', Georgia, serif" font-style="italic" font-size="44" fill="{text_color}" opacity="0">'
                f'{val} {label}'
                f'<set attributeName="opacity" to="1" begin="{t_begin:.3f}s"/>'
                f'</text>'
            )
        else:
            xml_parts.append(
                f'<text x="22" y="112" font-family="\'Instrument Serif\', Georgia, serif" font-style="italic" font-size="44" fill="{text_color}" opacity="0">'
                f'{val} {label}'
                f'<set attributeName="opacity" to="1" begin="{t_begin:.3f}s"/>'
                f'<set attributeName="opacity" to="0" begin="{t_next:.3f}s"/>'
                f'</text>'
            )
            
    return "".join(xml_parts)


def render_world_card(cfg, fonts_css):
    tag = cfg["tag"]
    badge_x = cfg["badge_x"]
    bg = cfg["bg"]
    tc = cfg["text_color"]
    bc = cfg["body_color"]
    b_op = cfg["body_opacity"]
    rc = cfg["ring_color"]
    ro = cfg["ring_opacity"]
    delay = cfg["delay"]
    lines = cfg["lines"]
    
    safe_lines = [l.replace("&", "&amp;") if "&amp;" not in l else l for l in lines]

    # Aria label & title content
    if cfg["type"] == "multi_title":
        title_summary = " ".join(cfg["title_lines"])
        slot_height = 80
        title_markup = (
            f'<g clip-path="url(#slot)">'
            f'<g class="ro" style="animation-delay:{delay + 0.45:.2f}s">\n'
            f'    <text x="22" y="90" font-family="\'Instrument Serif\', Georgia, serif" font-style="italic" font-size="34" fill="{tc}">{cfg["title_lines"][0]}</text>\n'
            f'    <text x="22" y="122" font-family="\'Instrument Serif\', Georgia, serif" font-style="italic" font-size="34" fill="{tc}">{cfg["title_lines"][1]}</text>\n'
            f'  </g>'
            f'</g>'
        )
    else:
        title_summary = f"{cfg['final_num']} {cfg['label']}"
        slot_height = 66
        counter_inner = render_slot_counter(
            cfg["roll_values"],
            cfg["label"],
            tc,
            delay + 0.45,
            duration=0.85
        )
        title_markup = (
            f'<g clip-path="url(#slot)">'
            f'<g class="ro" style="animation-delay:{delay + 0.45:.2f}s">\n'
            f'    {counter_inner}\n'
            f'  </g>'
            f'</g>'
        )

    aria_label = f"{tag}: {title_summary}. " + " ".join(safe_lines)

    # Body lines layout
    if len(safe_lines) == 3:
        desc_markup = "\n  ".join([
            f'<text class="r" style="animation-delay:{delay + 0.75 + i * 0.10:.2f}s" x="24" y="{154 + i * 19}" font-family="Geist, system-ui, -apple-system, sans-serif" font-size="13.5" fill="{bc}" opacity="{b_op}">{l}</text>'
            for i, l in enumerate(safe_lines)
        ])
    elif len(safe_lines) == 1:
        desc_markup = f'<text class="r" style="animation-delay:{delay + 0.75:.2f}s" x="24" y="162" font-family="Geist, system-ui, -apple-system, sans-serif" font-size="13.5" fill="{bc}" opacity="{b_op}">{safe_lines[0]}</text>'
    else:
        desc_markup = "\n  ".join([
            f'<text class="r" style="animation-delay:{delay + 0.75 + i * 0.10:.2f}s" x="24" y="{156 + i * 22}" font-family="Geist, system-ui, -apple-system, sans-serif" font-size="14" fill="{bc}" opacity="{b_op}">{l}</text>'
            for i, l in enumerate(safe_lines)
        ])

    badge_markup = (
        f'<g class="ai" style="animation-delay:{delay + 0.50:.2f}s">'
        f'<g class="n" style="animation-delay:{delay + 1.30:.2f}s">'
        f'<rect x="{badge_x}" y="27" width="14" height="14" rx="3" fill="#58a6ff"/>'
        f'<path d="M{badge_x + 3.5} 37.5 L{badge_x + 10.5} 30.5 M{badge_x + 6.5} 30.5 H{badge_x + 10.5} V34.5" stroke="#ffffff" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round" fill="none"/>'
        f'</g>'
        f'</g>'
    )

    combined_css = f"{fonts_css}\n{ANIMATION_CSS}"

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="293.333" height="222" viewBox="0 0 293.333 222" role="img" aria-label="{aria_label}"><title>{aria_label}</title><style>{combined_css}</style>
<defs>
  <clipPath id="card"><rect width="285.3333333333333" height="210" rx="14"/></clipPath>
  <clipPath id="slot"><rect x="0" y="55" width="285.3333333333333" height="{slot_height}"/></clipPath>
  <linearGradient id="gl" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/>
    <stop offset=".5" stop-color="#fff" stop-opacity=".35"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
</defs>
<g class="ti" style="animation-delay:{delay:.2f}s">
  <g clip-path="url(#card)">
    <rect width="285.3333333333333" height="210" fill="{bg}"/>
    <circle class="rg" style="animation-delay:{delay + 0.50:.2f}s" cx="245.33333333333331" cy="170" r="60" fill="none" stroke="{rc}" stroke-opacity="{ro}" stroke-width="2"/>
    <rect class="sh" style="animation-delay:{delay + 1.40:.2f}s" x="0" y="-20" width="90" height="250" fill="url(#gl)" transform="translate(-260 0)"/>
  </g>
  <text class="sl" style="animation-delay:{delay + 0.35:.2f}s" x="24" y="38" font-family="'Geist Mono', ui-monospace, SFMono-Regular, Menlo, monospace" font-size="12" letter-spacing="1.2" fill="{tc}">{tag}</text>
  {badge_markup}
  {title_markup}
  {desc_markup}
</g>
</svg>'''
    return svg


def build_all_world_cards():
    with open(FONTS_CSS_PATH, "r", encoding="utf-8") as f:
        fonts_css = f.read().strip()

    os.makedirs(CARDS_DIR, exist_ok=True)
    generated = []

    for cfg in WORLD_CONFIGS:
        svg_content = render_world_card(cfg, fonts_css)
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
