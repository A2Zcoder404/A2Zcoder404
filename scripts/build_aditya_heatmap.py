import os
import re
import json
import urllib.request
from datetime import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
DATA_DIR = os.path.join(ROOT, "data")
CARDS_DIR = os.path.join(ROOT, "cards")
CACHE_FILE = os.path.join(DATA_DIR, "contributions_cache.json")

def get_font_and_css_block():
    css_path = os.path.join(DATA_DIR, "hero_fonts.css")
    if os.path.exists(css_path):
        with open(css_path, "r", encoding="utf-8") as f:
            return f.read()
    hero_path = os.path.join(CARDS_DIR, "hero.svg")
    if os.path.exists(hero_path):
        with open(hero_path, "r", encoding="utf-8") as f:
            content = f.read()
        m = re.search(r"<style>(.*?)</style>", content, re.DOTALL)
        if m:
            return m.group(1)
    raise ValueError("Could not find hero_fonts.css or cards/hero.svg for styles")

def fetch_contributions_data(username="A2Zcoder404"):
    url = f"https://github.com/users/{username}/contributions"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    html = ""
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=8) as resp:
            html = resp.read().decode("utf-8")
    except Exception as e:
        print(f"[!] Warning: Could not fetch live contributions from GitHub: {e}")

    if html:
        # Cache the html or parsed data
        try:
            with open(os.path.join(DATA_DIR, "contributions_raw.html"), "w", encoding="utf-8") as f:
                f.write(html)
        except Exception:
            pass
    elif os.path.exists(os.path.join(DATA_DIR, "contributions_raw.html")):
        with open(os.path.join(DATA_DIR, "contributions_raw.html"), "r", encoding="utf-8") as f:
            html = f.read()

    total_m = re.search(r"([\d,]+)\s+contributions\s+in\s+the\s+last\s+year", html) if html else None
    total_contribs = total_m.group(1) if total_m else "843"

    cell_pattern = re.compile(r'<td[^>]+data-date="(?P<date>[^"]+)"[^>]+id="(?P<id>[^"]+)"[^>]+data-level="(?P<level>\d+)"')
    tooltip_pattern = re.compile(r'<tool-tip[^>]+for="(?P<id>[^"]+)"[^>]*>(?P<text>.*?)</tool-tip>', re.DOTALL)

    cells = {m.group('id'): {'date': m.group('date'), 'level': int(m.group('level'))} for m in cell_pattern.finditer(html)}
    tooltips = {m.group('id'): m.group('text').strip() for m in tooltip_pattern.finditer(html)}

    days_grid = {}
    max_col = 0
    for cid, cdata in cells.items():
        m = re.search(r'contribution-day-component-(\d+)-(\d+)', cid)
        if m:
            r = int(m.group(1))
            c = int(m.group(2))
            max_col = max(max_col, c)
            tip = tooltips.get(cid, '')
            count_m = re.search(r'(\d+)\s+contribution', tip)
            count = int(count_m.group(1)) if count_m else 0
            days_grid[(c, r)] = {
                'date': cdata['date'],
                'level': cdata['level'],
                'count': count,
                'tooltip': tip
            }

    return total_contribs, days_grid, max_col

def build_heatmap_svg(output_path=None):
    if output_path is None:
        output_path = os.path.join(CARDS_DIR, "heatmap.svg")

    total_contribs, days_grid, max_col = fetch_contributions_data("A2Zcoder404")
    css_content = get_font_and_css_block()

    # Color palette (Avi Vashishta cobalt blue scale)
    COLORS = {
        0: "#e2e2de",  # None
        1: "#c8d3ff",  # Low
        2: "#94a8ff",  # Medium-low
        3: "#6280ff",  # Medium
        4: "#2f55ff",  # High
        5: "#1a3be0",  # Peak
    }

    # If GitHub only gave levels 0-4, map count to level 5 if high count
    rect_elements = []
    months_seen = set()
    month_labels = []

    # Columns 0 to max_col (52 columns = 53 weeks)
    for c in range(max_col + 1):
        x = 44 + c * 15
        for r in range(7):
            if (c, r) in days_grid:
                day_data = days_grid[(c, r)]
                date_str = day_data['date']
                count = day_data['count']
                base_lvl = day_data['level']

                # Compute color
                if count == 0:
                    fill = COLORS[0]
                elif count >= 30:
                    fill = COLORS[5]
                elif count >= 15 or base_lvl == 4:
                    fill = COLORS[4]
                elif count >= 8 or base_lvl == 3:
                    fill = COLORS[3]
                elif count >= 3 or base_lvl == 2:
                    fill = COLORS[2]
                else:
                    fill = COLORS[1]

                # Animation delay: cascade diagonal wave
                delay = 1.00 + (c * 0.03) + (r * 0.02)
                y = 96 + r * 15

                count_phrase = f"{count} contribution" if count == 1 else f"{count} contributions"
                tip_title = f"{date_str}: {count_phrase}"

                rect_elements.append(
                    f'<rect class="p" style="animation-delay:{delay:.2f}s" x="{x}" y="{y}" width="12" height="12" rx="3" fill="{fill}"><title>{tip_title}</title></rect>'
                )

                # Month label check
                dt = datetime.strptime(date_str, "%Y-%m-%d")
                m_name = dt.strftime("%b")
                if dt.day <= 7 and m_name not in months_seen and x < 680:
                    months_seen.add(m_name)
                    month_labels.append((x, m_name))

    # Format month text elements
    month_svg_tags = []
    for mx, mname in month_labels:
        month_svg_tags.append(
            f'<text x="{mx}" y="217" font-family="\'Geist Mono\', ui-monospace, SFMono-Regular, Menlo, monospace" font-size="11" fill="#6e6e73">{mname}</text>'
        )

    month_markup = ''.join(month_svg_tags)
    rects_markup = ''.join(rect_elements)

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="880.000" height="257" viewBox="0 0 880.000 257" role="img" aria-label="Contribution graph: {total_contribs} contributions in the last year"><title>Contribution graph: {total_contribs} contributions in the last year</title><style>{css_content}</style>
<rect width="880" height="245" rx="14" fill="#f3f3f1"/>
<text class="r" style="animation-delay:0.80s" x="42" y="62" font-family="'Instrument Serif', Georgia, serif" font-size="34" fill="#111111">Every day, <tspan font-style="italic" fill="#2f55ff">in blue</tspan></text>
<text class="f" style="animation-delay:0.80s" x="836" y="60" text-anchor="end" font-family="'Geist Mono', ui-monospace, SFMono-Regular, Menlo, monospace" font-size="12" letter-spacing="1" fill="#6e6e73">REFRESHED DAILY</text>
{rects_markup}
<g class="f" style="animation-delay:2.40s">{month_markup}
<text x="744" y="217" text-anchor="end" font-family="'Geist Mono', ui-monospace, SFMono-Regular, Menlo, monospace" font-size="11" fill="#6e6e73">less</text>
<rect x="752" y="207" width="11" height="11" rx="2.5" fill="#e2e2de"/><rect x="766" y="207" width="11" height="11" rx="2.5" fill="#c8d3ff"/><rect x="780" y="207" width="11" height="11" rx="2.5" fill="#94a8ff"/><rect x="794" y="207" width="11" height="11" rx="2.5" fill="#6280ff"/><rect x="808" y="207" width="11" height="11" rx="2.5" fill="#2f55ff"/><rect x="822" y="207" width="11" height="11" rx="2.5" fill="#1a3be0"/>
<text x="838" y="217" font-family="'Geist Mono', ui-monospace, SFMono-Regular, Menlo, monospace" font-size="11" fill="#6e6e73">more</text></g>
</svg>'''

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"[✓] Successfully generated {output_path} (length: {len(svg)}, total contributions: {total_contribs})")

if __name__ == "__main__":
    build_heatmap_svg()
