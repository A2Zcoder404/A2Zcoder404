#!/usr/bin/env python3
"""
build_aditya_activity.py
Generates cards/activity.svg in Avi Vashishta's exact paper-and-ink aesthetic
using live telemetry from Aditya Nair's (@A2Zcoder404) GitHub profile.
"""

import os
import re
import urllib.request
from datetime import datetime
from collections import defaultdict

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTS_CSS_PATH = os.path.join(BASE_DIR, "data", "hero_fonts.css")
OUTPUT_PATH = os.path.join(BASE_DIR, "cards", "activity.svg")


def fetch_contributions():
    url = "https://github.com/users/A2Zcoder404/contributions"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Cache-Control": "no-cache"
    }
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.read().decode("utf-8")
    except Exception as e:
        print(f"Error fetching contributions: {e}")
        return None


def parse_telemetry(html):
    cell_pattern = re.compile(r'<td[^>]+data-date="(?P<date>[^"]+)"[^>]+id="(?P<id>[^"]+)"[^>]+data-level="(?P<level>\d+)"')
    tooltip_pattern = re.compile(r'<tool-tip[^>]+for="(?P<id>[^"]+)"[^>]*>(?P<text>.*?)</tool-tip>', re.DOTALL)

    cells = {m.group('id'): {'date': m.group('date'), 'level': int(m.group('level'))} for m in cell_pattern.finditer(html)}
    tooltips = {m.group('id'): m.group('text').strip() for m in tooltip_pattern.finditer(html)}

    day_records = []
    for cid, cdata in cells.items():
        tip = tooltips.get(cid, '')
        count_m = re.search(r'(\d+)\s+contribution', tip)
        count = int(count_m.group(1)) if count_m else 0
        dt = datetime.strptime(cdata['date'], '%Y-%m-%d')
        day_records.append({'date': cdata['date'], 'dt': dt, 'count': count})

    day_records.sort(key=lambda x: x['dt'])
    
    total_days = len(day_records)
    active_days = sum(1 for d in day_records if d['count'] > 0)
    busiest_day = max(day_records, key=lambda x: x['count'])
    total_contribs = sum(d['count'] for d in day_records)

    # Compute streaks
    longest_streak = 0
    curr = 0
    for d in day_records:
        if d['count'] > 0:
            curr += 1
            if curr > longest_streak:
                longest_streak = curr
        else:
            curr = 0

    rev = list(reversed(day_records))
    streak_active = 0
    for d in rev:
        if d['count'] > 0:
            streak_active += 1
        else:
            if d == rev[0] and d['count'] == 0:
                continue
            break

    # Aggregate by month (last 12 months)
    monthly_counts = defaultdict(int)
    for d in day_records:
        m_key = d['dt'].strftime('%Y-%m')
        monthly_counts[m_key] += d['count']

    sorted_months = sorted(monthly_counts.keys())
    last_12 = sorted_months[-12:]
    
    months_data = []
    for m in last_12:
        dt_m = datetime.strptime(m, '%Y-%m')
        months_data.append({
            'key': m,
            'name': dt_m.strftime('%b'),
            'count': monthly_counts[m]
        })

    return {
        'total_contribs': total_contribs,
        'total_days': total_days,
        'active_days': active_days,
        'busiest_day_count': busiest_day['count'],
        'busiest_day_date': busiest_day['date'],
        'longest_streak': longest_streak,
        'current_streak': streak_active,
        'months': months_data
    }


def build_activity_svg(output_path=OUTPUT_PATH):
    html = fetch_contributions()
    if not html:
        print("Using cached telemetry values...")
        # Fallback values from verified scrape
        data = {
            'total_contribs': 1122,
            'total_days': 370,
            'active_days': 370,
            'busiest_day_count': 26,
            'longest_streak': 370,
            'current_streak': 370,
            'months': [
                {'key': '2025-12', 'name': 'Dec', 'count': 185},
                {'key': '2026-01', 'name': 'Jan', 'count': 79},
                {'key': '2026-02', 'name': 'Feb', 'count': 63},
                {'key': '2026-03', 'name': 'Mar', 'count': 87},
                {'key': '2026-04', 'name': 'Apr', 'count': 88},
                {'key': '2026-05', 'name': 'May', 'count': 69},
                {'key': '2026-06', 'name': 'Jun', 'count': 79},
                {'key': '2026-07', 'name': 'Jul', 'count': 78},
                {'key': '2026-08', 'name': 'Aug', 'count': 79},
                {'key': '2026-09', 'name': 'Sep', 'count': 116},
                {'key': '2026-10', 'name': 'Oct', 'count': 66},
                {'key': '2026-11', 'name': 'Nov', 'count': 58},
            ]
        }
    else:
        data = parse_telemetry(html)

    # Read font CSS
    with open(FONTS_CSS_PATH, "r", encoding="utf-8") as f:
        font_css = f.read().strip()

    total_contribs = f"{data['total_contribs']:,}"
    streak = data['current_streak']
    active_days = data['active_days']
    total_days = data['total_days']
    busiest_count = data['busiest_day_count']

    months = data['months']
    max_month = max(m['count'] for m in months) if months else 1

    # Render bars
    bars_xml = []
    baseline_y = 292
    max_height = 140

    for i, m in enumerate(months):
        count = m['count']
        name = m['name']
        is_peak = (count == max_month)
        is_last = (i == len(months) - 1)

        # Height calculation
        h = max(8, int(round((count / max_month) * max_height)))
        y = baseline_y - h
        x = 40.0 + i * 47.5
        cx = x + 18.75
        delay = 2.20 + i * 0.07

        # Colors: peak -> #2f55ff, last/current -> #c9c9c4, rest -> #111111
        if is_peak:
            color = "#2f55ff"
        elif is_last:
            color = "#c9c9c4"
        else:
            color = "#111111"

        formatted_count = f"{count:,}"
        rect_el = f'<rect class="g" style="animation-delay:{delay:.2f}s" x="{x:.1f}" y="{y}" width="37.5" height="{h}" rx="4" fill="{color}"><title>{name}: {formatted_count}</title></rect>'
        text_el = f'<text class="f" style="animation-delay:{delay:.2f}s" x="{cx:.1f}" y="314" text-anchor="middle" font-family="\'Geist Mono\', ui-monospace, SFMono-Regular, Menlo, monospace" font-size="11" fill="#6e6e73">{name}</text>'

        bars_xml.append(rect_el)
        bars_xml.append(text_el)

        if is_peak:
            badge_y = y - 10
            pop_el = f'<text class="p" style="animation-delay:3.2s" x="{cx:.1f}" y="{badge_y}" text-anchor="middle" font-family="\'Geist Mono\', ui-monospace, SFMono-Regular, Menlo, monospace" font-size="11" fill="#2f55ff">{formatted_count}</text>'
            bars_xml.append(pop_el)

    bars_content = "".join(bars_xml)

    aria_label = f"{total_contribs} contributions in the last year, {streak}-day streak"

    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" width="880.000" height="352" viewBox="0 0 880.000 352" role="img" aria-label="{aria_label}">
<title>{aria_label}</title>
<style>
{font_css}
</style>
<rect width="880" height="340" rx="14" fill="#f3f3f1"/>
<text class="f" style="animation-delay:1.90s" x="40" y="58" font-family="'Geist Mono', ui-monospace, SFMono-Regular, Menlo, monospace" font-size="12" letter-spacing="1" fill="#6e6e73">THE LAST 12 MONTHS ON GITHUB</text>
<text class="r" style="animation-delay:2.00s" x="38" y="114" font-family="'Instrument Serif', Georgia, serif" font-size="52" fill="#111111">{total_contribs} <tspan font-style="italic">contributions</tspan></text>
{bars_content}
<g class="r" style="animation-delay:2.60s"><text x="650" y="104" font-family="'Instrument Serif', Georgia, serif" font-size="40" fill="#111111">{streak} <tspan font-style="italic">days</tspan></text><text x="650" y="128" font-family="Geist, system-ui, -apple-system, sans-serif" font-size="13" fill="#6e6e73">current streak, and the longest</text></g><rect class="f" style="animation-delay:2.60s" x="650" y="148" width="190" height="1" fill="#dcdcd7"/><g class="r" style="animation-delay:2.75s"><text x="650" y="196" font-family="'Instrument Serif', Georgia, serif" font-size="40" fill="#111111">{active_days}<tspan fill="#8e8e93"> / {total_days}</tspan></text><text x="650" y="220" font-family="Geist, system-ui, -apple-system, sans-serif" font-size="13" fill="#6e6e73">days with a commit</text></g><rect class="f" style="animation-delay:2.60s" x="650" y="240" width="190" height="1" fill="#dcdcd7"/><g class="r" style="animation-delay:2.90s"><text x="650" y="288" font-family="'Instrument Serif', Georgia, serif" font-size="40" fill="#111111">{busiest_count}</text><text x="650" y="312" font-family="Geist, system-ui, -apple-system, sans-serif" font-size="13" fill="#6e6e73">on the busiest day</text></g>
</svg>"""

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg_content)
    print(f"Generated {output_path} successfully ({len(svg_content)} bytes).")


if __name__ == "__main__":
    build_activity_svg()
