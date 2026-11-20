#!/usr/bin/env python3
"""
Fetch GitHub Profile & Repository Telemetry
Queries the GitHub REST API for @A2ZCoder404, aggregates codebase language byte
counts, calculates percentage distributions, and exports to data/profile.json.
"""

import os
import json
import urllib.request
import urllib.error

USERNAME = "A2Zcoder404"
BASE_URL = f"https://api.github.com/users/{USERNAME}"
REPOS_URL = f"https://api.github.com/users/{USERNAME}/repos?per_page=100&sort=updated"

def get_headers():
    token = os.environ.get("GITHUB_TOKEN")
    headers = {
        "User-Agent": "A2ZCoder404-Profile-Pipeline",
        "Accept": "application/vnd.github.v3+json"
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers

def fetch_json(url):
    req = urllib.request.Request(url, headers=get_headers())
    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        print(f"[Warning] HTTP {e.code} while fetching {url}: {e.reason}")
        return None
    except Exception as e:
        print(f"[Warning] Request failed for {url}: {e}")
        return None

def main():
    print(f"[*] Fetching telemetry for GitHub user @{USERNAME}...")
    user_data = fetch_json(BASE_URL)
    if not user_data:
        print("[!] Failed to fetch primary user profile; using existing cache if available.")
        return

    repos_data = fetch_json(REPOS_URL) or []
    print(f"[+] Retrieved {len(repos_data)} public repositories.")

    language_totals = {}
    repos_summary = []

    for repo in repos_data:
        if repo.get("fork", False):
            continue
        
        name = repo.get("name")
        desc = repo.get("description") or ""
        primary_lang = repo.get("language") or "Other"
        stars = repo.get("stargazers_count", 0)
        forks = repo.get("forks_count", 0)
        html_url = repo.get("html_url")
        homepage = repo.get("homepage")

        # Fetch detailed languages for repo
        langs_url = repo.get("languages_url")
        repo_langs = fetch_json(langs_url) or {}

        for lang, byte_count in repo_langs.items():
            language_totals[lang] = language_totals.get(lang, 0) + byte_count

        repos_summary.append({
            "name": name,
            "description": desc,
            "primary_language": primary_lang,
            "languages": repo_langs,
            "stars": stars,
            "forks": forks,
            "url": html_url,
            "homepage": homepage
        })

    total_bytes = sum(language_totals.values())
    lang_percentages = {}
    if total_bytes > 0:
        for lang, byte_count in sorted(language_totals.items(), key=lambda x: x[1], reverse=True):
            pct = (byte_count / total_bytes) * 100
            lang_percentages[lang] = {
                "bytes": byte_count,
                "percentage": round(pct, 1)
            }

    profile_payload = {
        "username": user_data.get("login", USERNAME),
        "name": user_data.get("name", "Aditya Mohan Nair"),
        "bio": user_data.get("bio", ""),
        "avatar_url": user_data.get("avatar_url", ""),
        "blog": user_data.get("blog", "https://striveforexcellence.in/"),
        "twitter": user_data.get("twitter_username", "zcoder404"),
        "public_repos": user_data.get("public_repos", len(repos_summary)),
        "followers": user_data.get("followers", 0),
        "following": user_data.get("following", 0),
        "created_at": user_data.get("created_at", ""),
        "total_code_bytes": total_bytes,
        "language_distribution": lang_percentages,
        "repositories": repos_summary
    }

    # Ensure output dir exists
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, "..", "data", "profile.json")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(profile_payload, f, indent=2)

    print(f"[✓] Saved updated telemetry to {output_path}")
    print(f"[+] Total Codebase: {total_bytes:,} bytes across {len(language_totals)} languages.")
    for lang, stats in list(lang_percentages.items())[:5]:
        print(f"    - {lang}: {stats['percentage']}% ({stats['bytes']:,} bytes)")

if __name__ == "__main__":
    main()
