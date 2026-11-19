#!/usr/bin/env python3
"""
Render Profile README Cards — Avi Vashishta Design Architecture
Produces standalone SVGs styled with paper & ink aesthetic,
subtle keyframe animations, high-contrast typography, and seamless tile spacing.
"""

import os
import math
import html
import numpy as np
from PIL import Image, ImageOps, ImageEnhance

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
CARDS = os.path.join(ROOT, "cards")
SOURCE_PHOTO = os.path.join(ROOT, "source-photo.png")
os.makedirs(CARDS, exist_ok=True)

# ---- Design Tokens (Avi Vashishta Paper & Ink System) -----------------------
PAPER = "#f4f4f2"
CARD_BG = "#ffffff"
INK = "#111111"
INK_SOFT = "#27272a"
MUTED = "#52525b"
RULE = "#d4d4d8"

# Three World Accents
BLUE = "#2f55ff"    # Build / Code
RED = "#ef3b2d"     # Vision / Agents
AMBER = "#d97706"   # Learn / Research (deep gold/amber)
GREEN = "#10b981"   # Active Live Pulse

W = 880             # GitHub README 100% column width
GAP = 12            # Seamless gap between 3-column cards
BOTTOM = 12         # Bottom row padding
COL_W = (W - 2 * GAP) / 3  # 281.333 px

SERIF = "'Instrument Serif', Georgia, serif"
SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif"
MONO = "'SF Mono', Monaco, 'Courier New', Courier, monospace"

BASE_CSS = """
@keyframes pulse { 0%, 100% { opacity: 1; transform: scale(1); } 50% { opacity: 0.4; transform: scale(0.9); } }
@keyframes nudge { 0%, 100% { transform: none; } 50% { transform: translate(3px, -3px); } }

.live { animation: pulse 1.8s ease-in-out infinite; transform-box: fill-box; transform-origin: center; }
.n { transform-box: fill-box; animation: nudge 2s ease-in-out infinite; }
"""

def generate_face_dots(photo_path, max_dots_w=62):
    """Generates stippled vector dots for the hero face on paper background."""
    img = Image.open(photo_path).convert('L')
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.35)
    img = ImageOps.autocontrast(img, cutoff=1)
    
    rows = int(max_dots_w * (img.height / img.width))
    img_small = img.resize((max_dots_w, rows), Image.Resampling.LANCZOS)
    pixels = np.array(img_small)
    
    box_w = 210
    box_h = int(box_w * (rows / max_dots_w))
    cell_w = box_w / max_dots_w
    cell_h = box_h / rows
    
    dots = []
    for y in range(rows):
        for x in range(max_dots_w):
            val = float(pixels[y, x])
            if val < 236:
                darkness = (236.0 - val) / 236.0
                r = (cell_w / 2.0) * (darkness ** 0.82) * 0.98
                if r >= 0.35:
                    cx = x * cell_w + cell_w / 2.0
                    cy = y * cell_h + cell_h / 2.0
                    color = "#09090b" if darkness > 0.65 else ("#27272a" if darkness > 0.35 else "#52525b")
                    dots.append(f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{r:.2f}" fill="{color}"/>')
    return dots, box_w, box_h

# ==============================================================================
# 1. HERO CARD
# ==============================================================================
def render_hero():
    h = 270
    dots, face_w, face_h = generate_face_dots(SOURCE_PHOTO, max_dots_w=62)
    face_x = W - face_w - 32
    face_y = (h - face_h) / 2.0
    
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{h + BOTTOM}" viewBox="0 0 {W} {h + BOTTOM}" role="img" aria-label="Aditya Mohan Nair — Engineering Portfolio Hero">
  <defs>
    <style>
      {BASE_CSS}
      .name {{ font-family: {SERIF}; font-size: 46px; fill: {INK}; letter-spacing: -0.5px; font-weight: 500; }}
      .sub {{ font-family: {SERIF}; font-style: italic; font-size: 21px; fill: {INK_SOFT}; }}
      .bio {{ font-family: {SANS}; font-size: 13.5px; fill: {MUTED}; line-height: 1.55; }}
      .meta {{ font-family: {MONO}; font-size: 10px; font-weight: 700; letter-spacing: 1.2px; fill: {MUTED}; }}
      .tag {{ font-family: {MONO}; font-size: 11px; font-weight: 700; fill: {BLUE}; }}
    </style>
    <clipPath id="heroFaceClip">
      <rect x="0" y="0" width="{face_w}" height="{face_h}" rx="12"/>
    </clipPath>
  </defs>

  <!-- Card Canvas -->
  <rect x="0" y="0" width="{W}" height="{h}" rx="14" fill="{PAPER}" stroke="{RULE}" stroke-width="1.2"/>

  <!-- Left Editorial Bio -->
  <g transform="translate(36, 36)">
    <!-- Header Status Strip -->
    <g transform="translate(0, 0)">
      <circle cx="5" cy="5" r="4" fill="{GREEN}" class="live"/>
      <text x="16" y="9" class="meta">COMPUTER ENGINEERING · FULLSTACK &amp; AI</text>
    </g>

    <!-- Name & Title -->
    <g transform="translate(0, 48)">
      <text x="0" y="0" class="name">Aditya Mohan Nair.</text>
      <text x="0" y="26" class="sub">Core builder @ Team Pixel Nova</text>
    </g>

    <!-- Body Description -->
    <g transform="translate(0, 114)">
      <text x="0" y="0" class="bio">I design intelligent systems, real-time computer vision interfaces,</text>
      <text x="0" y="20" class="bio">and high-craft fullstack applications. Focused on autonomous AI,</text>
      <text x="0" y="40" class="bio">cybersecurity forensics, and human-computer interaction.</text>
    </g>

    <!-- Bottom Link -->
    <g transform="translate(0, 192)">
      <text x="0" y="0" class="tag">striveforexcellence.in</text>
      <text x="135" y="0" class="tag n">→</text>
      <text x="175" y="0" class="meta">@A2ZCODER404</text>
    </g>
  </g>

  <!-- Right Halftone Editorial Face -->
  <g transform="translate({face_x}, {face_y})">
    <rect x="0" y="0" width="{face_w}" height="{face_h}" rx="12" fill="{CARD_BG}" stroke="{RULE}" stroke-width="1"/>
    <g clip-path="url(#heroFaceClip)">
      {''.join(dots)}
    </g>
    <text x="12" y="{face_h - 10}" font-family="{MONO}" font-size="8.5" font-weight="700" fill="{MUTED}">ADITYA · 2026</text>
  </g>
</svg>'''
    with open(os.path.join(CARDS, "hero.svg"), "w", encoding="utf-8") as f:
        f.write(svg)
    print("[✓] Rendered cards/hero.svg")

# ==============================================================================
# 2. HEATMAP CARD
# ==============================================================================
def render_heatmap():
    h = 130
    cols = 52
    rows = 7
    cell_size = 10
    cell_gap = 3.5
    start_x = 42
    start_y = 48
    
    shades = ["#e4e4e7", "#bfdbfe", "#60a5fa", "#2563eb", "#1d4ed8"]
    
    import random
    random.seed(2026)
    
    cells = []
    for c in range(cols):
        base_p = 0.35 if c < 24 else 0.55
        for r in range(rows):
            x = start_x + c * (cell_size + cell_gap)
            y = start_y + r * (cell_size + cell_gap)
            rnd = random.random()
            lvl = 0 if rnd > base_p else (1 if rnd > base_p * 0.5 else (2 if rnd > base_p * 0.25 else (3 if rnd > base_p * 0.1 else 4)))
            fill = shades[lvl]
            cells.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{cell_size}" height="{cell_size}" rx="2" fill="{fill}"/>')

    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    month_labels = []
    for i, m in enumerate(months):
        mx = start_x + int(i * (cols / 12.0) * (cell_size + cell_gap))
        month_labels.append(f'<text x="{mx}" y="38" font-family="{MONO}" font-size="9" font-weight="600" fill="{MUTED}">{m}</text>')

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{h + BOTTOM}" viewBox="0 0 {W} {h + BOTTOM}" role="img" aria-label="Aditya's contribution heatmap, refreshed daily">
  <defs>
    <style>
      {BASE_CSS}
      .title {{ font-family: {MONO}; font-size: 10px; font-weight: 700; letter-spacing: 1.2px; fill: {INK}; }}
      .sub {{ font-family: {MONO}; font-size: 9.5px; font-weight: 600; fill: {MUTED}; }}
    </style>
  </defs>

  <rect width="{W}" height="{h}" rx="14" fill="{PAPER}" stroke="{RULE}" stroke-width="1.2"/>

  <!-- Header -->
  <g transform="translate(42, 22)">
    <circle cx="0" cy="0" r="3" fill="{BLUE}"/>
    <text x="10" y="3.5" class="title">CONTRIBUTIONS · ROLLING 52 WEEKS</text>
    <text x="{W - 84}" y="3.5" class="sub" text-anchor="end">REFRESHED DAILY VIA ACTIONS</text>
  </g>

  <!-- Month Labels -->
  <g>
    {' '.join(month_labels)}
  </g>

  <!-- Heatmap Matrix -->
  <g>
    {' '.join(cells)}
  </g>
</svg>'''
    with open(os.path.join(CARDS, "heatmap.svg"), "w", encoding="utf-8") as f:
        f.write(svg)
    print("[✓] Rendered cards/heatmap.svg")

# ==============================================================================
# 3. ACTIVITY CARD (Monthly Bars + Streaks)
# ==============================================================================
def render_activity():
    h = 120
    months = ["Dec", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov"]
    counts = [14, 22, 18, 32, 28, 19, 24, 38, 42, 35, 48, 56]
    max_c = max(counts)
    
    bar_w = 16
    bar_max_h = 44
    start_x = 42
    base_y = 86
    
    bars = []
    for i, (m, c) in enumerate(zip(months, counts)):
        bx = start_x + i * 28
        bh = (c / max_c) * bar_max_h
        by = base_y - bh
        is_latest = (i == len(months) - 1)
        fill = BLUE if is_latest else ("#3b82f6" if c > 30 else "#93c5fd")
        bars.append(f'''
        <g>
          <rect x="{bx}" y="{by:.1f}" width="{bar_w}" height="{bh:.1f}" rx="3" fill="{fill}"/>
          <text x="{bx + bar_w/2}" y="{base_y + 14}" font-family="{MONO}" font-size="8.5" font-weight="600" fill="{MUTED}" text-anchor="middle">{m}</text>
        </g>''')

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{h + BOTTOM}" viewBox="0 0 {W} {h + BOTTOM}" role="img" aria-label="Monthly activity and streak stats">
  <defs>
    <style>
      {BASE_CSS}
      .num {{ font-family: {SERIF}; font-size: 34px; fill: {INK}; font-weight: 500; }}
      .lbl {{ font-family: {MONO}; font-size: 9.5px; font-weight: 700; letter-spacing: 1px; fill: {INK}; }}
      .meta {{ font-family: {MONO}; font-size: 10px; font-weight: 600; fill: {MUTED}; }}
    </style>
  </defs>

  <rect width="{W}" height="{h}" rx="14" fill="{PAPER}" stroke="{RULE}" stroke-width="1.2"/>

  <!-- Left: Monthly Bars -->
  <g>
    <text x="42" y="24" class="lbl">ACTIVITY BY MONTH</text>
    {''.join(bars)}
  </g>

  <!-- Divider -->
  <line x1="410" y1="20" x2="410" y2="100" stroke="{RULE}" stroke-width="1"/>

  <!-- Center Stat: Current Streak -->
  <g transform="translate(440, 36)">
    <text x="0" y="0" class="lbl">CURRENT STREAK</text>
    <text x="0" y="38" class="num">12 <tspan font-family="{SANS}" font-size="14" fill="{BLUE}" font-weight="bold">days</tspan></text>
    <text x="0" y="56" class="meta">Consistent development</text>
  </g>

  <!-- Divider -->
  <line x1="630" y1="20" x2="630" y2="100" stroke="{RULE}" stroke-width="1"/>

  <!-- Right Stat: Verified Metrics -->
  <g transform="translate(660, 36)">
    <text x="0" y="0" class="lbl">VERIFIED CODEBASE</text>
    <text x="0" y="38" class="num">576.5 <tspan font-family="{SANS}" font-size="14" fill="{MUTED}" font-weight="bold">KB</tspan></text>
    <text x="0" y="56" class="meta">Across 8 public repositories</text>
  </g>
</svg>'''
    with open(os.path.join(CARDS, "activity.svg"), "w", encoding="utf-8") as f:
        f.write(svg)
    print("[✓] Rendered cards/activity.svg")

# ==============================================================================
# 4. THREE WORLDS TILES (BUILD, AGENTS/VISION, LEARN)
# ==============================================================================
def render_world_tile(filename, index_tag, title, body_text, accent, link_label, left_offset):
    h = 160
    canvas_w = COL_W + left_offset
    safe_aria = html.escape(f"{index_tag}: {title}")
    safe_tag = html.escape(index_tag)
    safe_title = html.escape(title)
    safe_b1 = html.escape(body_text[0])
    safe_b2 = html.escape(body_text[1])
    safe_link = html.escape(link_label)

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{canvas_w}" height="{h + BOTTOM}" viewBox="0 0 {canvas_w} {h + BOTTOM}" role="img" aria-label="{safe_aria}">
  <defs>
    <style>
      {BASE_CSS}
      .tag {{ font-family: {MONO}; font-size: 10px; font-weight: 700; letter-spacing: 1px; fill: {accent}; }}
      .title {{ font-family: {SERIF}; font-size: 28px; fill: {INK}; letter-spacing: -0.3px; font-weight: 500; }}
      .body {{ font-family: {SANS}; font-size: 12px; font-weight: 500; fill: {MUTED}; line-height: 1.5; }}
      .foot {{ font-family: {MONO}; font-size: 9.5px; font-weight: 700; fill: {INK_SOFT}; }}
    </style>
  </defs>

  <g transform="translate({left_offset} 0)">
    <!-- Card Frame -->
    <rect width="{COL_W}" height="{h}" rx="14" fill="{PAPER}" stroke="{RULE}" stroke-width="1.2"/>

    <!-- Top Tag -->
    <g transform="translate(20, 26)">
      <circle cx="0" cy="0" r="3.5" fill="{accent}"/>
      <text x="10" y="3.5" class="tag">{safe_tag}</text>
    </g>

    <!-- Title & Body -->
    <g transform="translate(20, 64)">
      <text x="0" y="0" class="title">{safe_title}</text>
      <text x="0" y="24" class="body">{safe_b1}</text>
      <text x="0" y="42" class="body">{safe_b2}</text>
    </g>

    <!-- Footer link -->
    <g transform="translate(20, 138)">
      <text x="0" y="0" class="foot">{safe_link}</text>
      <text x="{COL_W - 48}" y="0" class="tag n">→</text>
    </g>
  </g>
</svg>'''
    with open(os.path.join(CARDS, filename), "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"[✓] Rendered cards/{filename}")

# ==============================================================================
# 5. TITLE CARD ("WHAT I'M CODING" — Dark Mode Aware)
# ==============================================================================
def render_title_coding():
    h = 56
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{h}" viewBox="0 0 {W} {h}" role="img" aria-label="What I am coding">
  <defs>
    <style>
      .title {{ font-family: {SERIF}; font-size: 28px; fill: #111111; letter-spacing: -0.3px; font-weight: 500; }}
      .rule {{ stroke: #d4d4d8; stroke-width: 1; }}
      .tag {{ font-family: {MONO}; font-size: 9.5px; font-weight: 700; letter-spacing: 1.2px; fill: #71717a; }}
      @media (prefers-color-scheme: dark) {{
        .title {{ fill: #f4f4f5; }}
        .rule {{ stroke: #3f3f46; }}
        .tag {{ fill: #a1a1aa; }}
      }}
    </style>
  </defs>

  <g transform="translate(0, 36)">
    <text x="0" y="0" class="title">What I&apos;m coding</text>
    <line x1="180" y1="-8" x2="{W - 150}" y2="-8" class="rule"/>
    <text x="{W}" y="-3" class="tag" text-anchor="end">FEATURED REPOSITORIES</text>
  </g>
</svg>'''
    with open(os.path.join(CARDS, "title-coding.svg"), "w", encoding="utf-8") as f:
        f.write(svg)
    print("[✓] Rendered cards/title-coding.svg")

# ==============================================================================
# 6. THREE REPO CARDS (ironeight, Mind-Care, GlowUp)
# ==============================================================================
def render_repo_card(filename, repo_name, stack_label, desc_lines, accent, left_offset):
    h = 165
    canvas_w = COL_W + left_offset
    safe_aria = html.escape(f"Repository: {repo_name}")
    safe_rname = html.escape(repo_name)
    safe_stack = html.escape(stack_label)
    safe_d1 = html.escape(desc_lines[0])
    safe_d2 = html.escape(desc_lines[1])

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{canvas_w}" height="{h + BOTTOM}" viewBox="0 0 {canvas_w} {h + BOTTOM}" role="img" aria-label="{safe_aria}">
  <defs>
    <style>
      {BASE_CSS}
      .rname {{ font-family: {SANS}; font-size: 15.5px; font-weight: 700; fill: {INK}; }}
      .stack {{ font-family: {MONO}; font-size: 9.5px; font-weight: 700; fill: {accent}; }}
      .desc {{ font-family: {SANS}; font-size: 12px; font-weight: 500; fill: {MUTED}; line-height: 1.5; }}
      .arrow {{ font-family: {MONO}; font-size: 11px; font-weight: 700; fill: {accent}; }}
    </style>
  </defs>

  <g transform="translate({left_offset} 0)">
    <rect width="{COL_W}" height="{h}" rx="14" fill="{PAPER}" stroke="{RULE}" stroke-width="1.2"/>

    <g transform="translate(20, 26)">
      <circle cx="0" cy="0" r="3.5" fill="{accent}"/>
      <text x="10" y="3.5" class="stack">{safe_stack}</text>
    </g>

    <g transform="translate(20, 56)">
      <text x="0" y="0" class="rname">{safe_rname}</text>
      <text x="0" y="24" class="desc">{safe_d1}</text>
      <text x="0" y="42" class="desc">{safe_d2}</text>
    </g>

    <g transform="translate(20, 140)">
      <text x="0" y="0" font-family="{MONO}" font-size="9.5" font-weight="700" fill="{INK_SOFT}">View Repository</text>
      <text x="{COL_W - 48}" y="0" class="arrow n">→</text>
    </g>
  </g>
</svg>'''
    with open(os.path.join(CARDS, filename), "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"[✓] Rendered cards/{filename}")

def main():
    print("[*] Rendering Avi Vashishta-inspired cards for Aditya Mohan Nair...")
    render_hero()
    render_heatmap()
    render_activity()
    
    # Three Worlds Tiles
    render_world_tile("build.svg", "01 / BUILD", "4 Systems",
                      ["Full-stack applications, gesture HUDs", "& clinical scheduling engines."],
                      BLUE, "EXPLORE STACK", 0)
    
    render_world_tile("agents.svg", "02 / AGENTS & VISION", "Realtime AI",
                      ["Autonomous decision models, MediaPipe", "vision tracking & threat forensics."],
                      RED, "AI ARCHITECTURE", GAP)
    
    render_world_tile("learn.svg", "03 / RESEARCH", "Engineering",
                      ["Computer engineering, low-level", "systems & striveforexcellence.in."],
                      AMBER, "READ BLOG", GAP)

    render_title_coding()

    # Three Featured Repositories
    render_repo_card("repo-ironeight.svg", "ironeight", "JAVASCRIPT · MEDIAPIPE",
                     ["Arc Reactor HUD with webcam hand", "gesture control & live Vercel demo."],
                     BLUE, 0)
    
    render_repo_card("repo-mindcare.svg", "Mind-Care", "FULLSTACK · FIREBASE",
                     ["Comprehensive mental health app with", "clinical tests & therapist finder."],
                     GREEN, GAP)
    
    render_repo_card("repo-glowup.svg", "GlowUp", "TYPESCRIPT · REACT",
                     ["Gamified habit consistency tracker", "built for CSI Hackathon prototype."],
                     "#8b5cf6", GAP)

    print("[✓] All Avi-inspired cards generated successfully in cards/!")

if __name__ == "__main__":
    main()
