#!/usr/bin/env python3
"""
Generate & Update GitHub Metric SVGs
Reads data/profile.json and updates assets/github-stats.svg & assets/language-stats.svg.
"""

import os
import json
import re

def update_stats():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    profile_json = os.path.join(script_dir, "..", "data", "profile.json")
    stats_svg = os.path.join(script_dir, "..", "assets", "github-stats.svg")
    lang_svg = os.path.join(script_dir, "..", "assets", "language-stats.svg")

    if not os.path.exists(profile_json):
        print(f"[!] {profile_json} not found. Run fetch_github_data.py first.")
        return

    with open(profile_json, "r", encoding="utf-8") as f:
        data = json.load(f)

    public_repos = data.get("public_repos", 8)
    followers = data.get("followers", 9)
    following = data.get("following", 8)
    total_bytes = data.get("total_code_bytes", 983876)
    kb_str = f"{total_bytes / 1024:.1f} KB"

    # Update github-stats.svg
    if os.path.exists(stats_svg):
        with open(stats_svg, "r", encoding="utf-8") as f:
            content = f.read()

        content = re.sub(r'id="stat-repos">[^<]+<', f'id="stat-repos">{public_repos}<', content)
        content = re.sub(r'id="stat-followers">[^<]+<', f'id="stat-followers">{followers}<', content)
        content = re.sub(r'>\d+\.?\d*\s*KB<', f'>{kb_str}<', content)

        with open(stats_svg, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"[✓] Updated {stats_svg} with live metrics (Repos: {public_repos}, Followers: {followers}, Code: {kb_str})")

    # Update language-stats.svg
    if os.path.exists(lang_svg):
        langs = data.get("language_distribution", {})
        if langs:
            with open(lang_svg, "r", encoding="utf-8") as f:
                lcontent = f.read()

            lcontent = re.sub(r'>\d+\.?\d*\s*KB\s*INDEXED<', f'>{kb_str} INDEXED<', lcontent)
            with open(lang_svg, "w", encoding="utf-8") as f:
                f.write(lcontent)
            print(f"[✓] Refreshed {lang_svg}")

if __name__ == "__main__":
    update_stats()
