import re
import urllib.request
from datetime import datetime, timedelta
from collections import defaultdict

url = 'https://github.com/users/A2Zcoder404/contributions'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    'Cache-Control': 'no-cache'
}
req = urllib.request.Request(url, headers=headers)
with urllib.request.urlopen(req) as resp:
    html = resp.read().decode('utf-8')

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
current_streak = 0
curr = 0

for d in day_records:
    if d['count'] > 0:
        curr += 1
        if curr > longest_streak:
            longest_streak = curr
    else:
        curr = 0

# Check if streak is active up to latest day
# Today or yesterday
rev = list(reversed(day_records))
streak_active = 0
for d in rev:
    if d['count'] > 0:
        streak_active += 1
    else:
        # If today has 0 but yesterday had contributions, or check
        if d == rev[0] and d['count'] == 0:
            continue
        break

print(f'Total contributions: {total_contribs}')
print(f'Active days: {active_days} / {total_days}')
print(f'Busiest day: {busiest_day["count"]} on {busiest_day["date"]}')
print(f'Longest streak: {longest_streak} days, Active streak: {streak_active} days')

# Aggregate by month (last 12 months)
# Get all months present
monthly_counts = defaultdict(int)
for d in day_records:
    # Key as YYYY-MM
    m_key = d['dt'].strftime('%Y-%m')
    monthly_counts[m_key] += d['count']

# Get the last 12 months in chronological order
sorted_months = sorted(monthly_counts.keys())
last_12_months = sorted_months[-12:]
print('\nLast 12 months:')
for m in last_12_months:
    dt_m = datetime.strptime(m, '%Y-%m')
    name = dt_m.strftime('%b')
    print(f'  {m} ({name}): {monthly_counts[m]}')
