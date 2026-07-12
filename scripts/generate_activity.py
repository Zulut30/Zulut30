#!/usr/bin/env python3
"""Generate a self-contained GitHub activity dashboard SVG."""

from __future__ import annotations

import argparse
import json
import math
import os
import urllib.request
from collections import Counter
from datetime import date, datetime, timedelta, timezone
from html import escape
from pathlib import Path


GRAPHQL_URL = "https://api.github.com/graphql"
REST_URL = "https://api.github.com"
LANGUAGE_COLORS = {
    "Python": "#38bdf8",
    "TypeScript": "#2563eb",
    "JavaScript": "#f59e0b",
    "PHP": "#a78bfa",
    "Go": "#22d3ee",
    "C#": "#8b5cf6",
    "HTML": "#fb7185",
    "CSS": "#60a5fa",
    "Shell": "#94a3b8",
}


def request_json(url: str, token: str, payload: dict | None = None):
    body = None if payload is None else json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=body,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "User-Agent": "manacost-profile-dashboard",
            "Content-Type": "application/json",
            "X-GitHub-Api-Version": "2022-11-28",
        },
        method="POST" if body else "GET",
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def fetch_data(login: str, token: str):
    query = """
      query($login: String!) {
        user(login: $login) {
          contributionsCollection {
            contributionCalendar {
              totalContributions
              weeks {
                contributionDays { contributionCount date weekday }
              }
            }
          }
        }
      }
    """
    graph = request_json(
        GRAPHQL_URL,
        token,
        {"query": query, "variables": {"login": login}},
    )
    if graph.get("errors"):
        raise RuntimeError(graph["errors"])
    calendar = graph["data"]["user"]["contributionsCollection"]["contributionCalendar"]

    user = request_json(f"{REST_URL}/users/{login}", token)
    repos = request_json(
        f"{REST_URL}/users/{login}/repos?per_page=100&type=owner&sort=updated",
        token,
    )
    owned = [repo for repo in repos if not repo["fork"] and not repo["archived"]]
    return {
        "calendar": calendar,
        "public_repos": user["public_repos"],
        "stars": sum(repo["stargazers_count"] for repo in owned),
        "languages": Counter(repo["language"] for repo in owned if repo["language"]),
    }


def streaks(days: list[dict]) -> tuple[int, int]:
    active = {date.fromisoformat(day["date"]) for day in days if day["contributionCount"] > 0}
    if not active:
        return 0, 0

    longest = 0
    run = 0
    previous = None
    for active_day in sorted(active):
        run = run + 1 if previous and active_day == previous + timedelta(days=1) else 1
        longest = max(longest, run)
        previous = active_day

    cursor = date.today()
    if cursor not in active:
        cursor -= timedelta(days=1)
    current = 0
    while cursor in active:
        current += 1
        cursor -= timedelta(days=1)
    return current, longest


def sparkline(values: list[int], x: float, y: float, width: float, height: float) -> str:
    if not values:
        return ""
    peak = max(max(values), 1)
    points = []
    for index, value in enumerate(values):
        px = x + index * width / max(len(values) - 1, 1)
        py = y + height - (value / peak) * height
        points.append((px, py))
    line = " ".join(f"{px:.1f},{py:.1f}" for px, py in points)
    area = f"M {x:.1f},{y + height:.1f} L " + " L ".join(
        f"{px:.1f},{py:.1f}" for px, py in points
    ) + f" L {x + width:.1f},{y + height:.1f} Z"
    return (
        f'<path d="{area}" fill="url(#chartFill)"/>'
        f'<polyline points="{line}" fill="none" stroke="url(#brand)" '
        'stroke-width="3" stroke-linejoin="round" stroke-linecap="round"/>'
    )


def render_dashboard(login: str, data: dict) -> str:
    weeks = data["calendar"]["weeks"][-53:]
    days = [day for week in weeks for day in week["contributionDays"]]
    current_streak, longest_streak = streaks(days)
    weekly = [sum(day["contributionCount"] for day in week["contributionDays"]) for week in weeks]
    total = data["calendar"]["totalContributions"]
    generated = datetime.now(timezone.utc).strftime("%d %b %Y")

    width, height = 1200, 650
    parts = [f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
  <title id="title">{escape(login)} GitHub activity</title>
  <desc id="desc">{total} contributions, {data['public_repos']} public repositories, {data['stars']} stars, and a {current_streak} day current streak.</desc>
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#050b16"/><stop offset="1" stop-color="#0b1b32"/></linearGradient>
    <linearGradient id="brand" x1="0" y1="0" x2="1" y2="0"><stop stop-color="#22d3ee"/><stop offset=".62" stop-color="#38bdf8"/><stop offset="1" stop-color="#f59e0b"/></linearGradient>
    <linearGradient id="chartFill" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#38bdf8" stop-opacity=".32"/><stop offset="1" stop-color="#38bdf8" stop-opacity=".015"/></linearGradient>
    <filter id="glow"><feGaussianBlur stdDeviation="5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
    <style>
      text {{ font-family: Inter, Segoe UI, Arial, sans-serif; }}
      .muted {{ fill: #7f93aa; }} .label {{ fill: #91a5ba; font-size: 13px; font-weight: 600; letter-spacing: 1.5px; }}
      .value {{ fill: #f8fafc; font-size: 30px; font-weight: 700; }} .small {{ fill: #647b92; font-size: 12px; }}
      .section {{ fill: #d8e5f1; font-size: 15px; font-weight: 700; letter-spacing: 1.5px; }}
    </style>
  </defs>
  <rect x="1" y="1" width="1198" height="648" rx="26" fill="url(#bg)" stroke="#1d3854" stroke-width="2"/>
  <circle cx="1040" cy="90" r="150" fill="#38bdf8" opacity=".035"/>
  <circle cx="1060" cy="70" r="92" fill="#f59e0b" opacity=".025"/>
  <text x="56" y="54" fill="#f8fafc" font-size="20" font-weight="700" letter-spacing="2.2">ACTIVITY</text>
  <rect x="56" y="68" width="172" height="3" rx="1.5" fill="url(#brand)"/>
  <text x="1144" y="54" text-anchor="end" class="small">LAST 12 MONTHS · UPDATED {generated.upper()}</text>
''']

    metrics = [
        (f"{total:,}".replace(",", " "), "CONTRIBUTIONS", "12-month total"),
        (str(data["public_repos"]), "PUBLIC REPOS", "shipping in public"),
        (str(data["stars"]), "REPOSITORY STARS", "across owned projects"),
        (f"{current_streak} d", "CURRENT STREAK", f"longest · {longest_streak} d"),
    ]
    for index, (value, label, context) in enumerate(metrics):
        x = 56 + index * 276
        parts.append(f'''
  <g transform="translate({x} 96)">
    <rect width="252" height="98" rx="16" fill="#0b1727" stroke="#193149"/>
    <rect x="0" y="0" width="4" height="98" rx="2" fill="{'#f59e0b' if index == 3 else '#38bdf8'}"/>
    <text x="22" y="43" class="value">{value}</text>
    <text x="22" y="67" class="label">{label}</text>
    <text x="22" y="86" class="small">{context}</text>
  </g>''')

    parts.append('''
  <g transform="translate(56 230)">
    <text x="0" y="0" class="section">WEEKLY MOMENTUM</text>
    <text x="720" y="0" class="section">PROJECT MIX</text>
    <line x1="0" y1="134" x2="660" y2="134" stroke="#1b334b"/>
    <line x1="0" y1="92" x2="660" y2="92" stroke="#13283d"/>
    <line x1="0" y1="50" x2="660" y2="50" stroke="#13283d"/>
''')
    parts.append(sparkline(weekly, 0, 20, 660, 114))
    month_labels = [(0, "12M AGO"), (26, "6M"), (52, "NOW")]
    for index, label in month_labels:
        x = index * 660 / 52
        parts.append(f'<text x="{x:.1f}" y="154" text-anchor="{"start" if index == 0 else "end" if index == 52 else "middle"}" class="small">{label}</text>')

    languages = data["languages"].most_common(5)
    max_language = max((count for _, count in languages), default=1)
    for index, (language, count) in enumerate(languages):
        y = 26 + index * 30
        bar_width = 150 * count / max_language
        color = LANGUAGE_COLORS.get(language, "#64748b")
        parts.append(f'''
    <text x="720" y="{y + 11}" fill="#c5d4e3" font-size="13">{escape(language)}</text>
    <rect x="820" y="{y}" width="150" height="10" rx="5" fill="#101f31"/>
    <rect x="820" y="{y}" width="{bar_width:.1f}" height="10" rx="5" fill="{color}"/>
    <text x="1088" y="{y + 11}" text-anchor="end" class="small">{count} repos</text>
''')
    parts.append('  </g>')

    parts.append('''
  <g transform="translate(56 438)">
    <text x="0" y="0" class="section">CONTRIBUTION RHYTHM</text>
    <text x="970" y="0" text-anchor="end" class="small">LESS</text>
    <circle cx="989" cy="-5" r="4" fill="#0c3a52"/><circle cx="1004" cy="-5" r="4" fill="#0e6078"/><circle cx="1019" cy="-5" r="4" fill="#18a5c1"/><circle cx="1034" cy="-5" r="4" fill="#38bdf8"/>
    <text x="1088" y="0" text-anchor="end" class="small">MORE</text>
''')
    cell, gap = 15, 5
    counts = [day["contributionCount"] for day in days]
    peak = max(counts, default=1)
    palette = ["#0b1727", "#0c3a52", "#0e6078", "#18a5c1", "#38bdf8"]
    for week_index, week in enumerate(weeks):
        for day in week["contributionDays"]:
            count = day["contributionCount"]
            level = 0 if count == 0 else min(4, max(1, math.ceil(count / peak * 4)))
            x = week_index * (cell + gap)
            y = 24 + day["weekday"] * (cell + gap)
            parts.append(
                f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="4" fill="{palette[level]}">'
                f'<title>{escape(day["date"])}: {count} contributions</title></rect>'
            )
    parts.append('''
  </g>
  <path d="M56 621H1144" stroke="url(#brand)" stroke-opacity=".32"/>
  <text x="56" y="637" class="small">MANACOST DEV · BUILDING IN PUBLIC</text>
  <text x="1144" y="637" text-anchor="end" class="small">github.com/''' + escape(login) + '''</text>
</svg>''')
    return "".join(parts)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--user", required=True)
    parser.add_argument("--output", default="dist/activity-dashboard.svg")
    args = parser.parse_args()
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if not token:
        raise SystemExit("GH_TOKEN or GITHUB_TOKEN is required")

    data = fetch_data(args.user, token)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_dashboard(args.user, data), encoding="utf-8")
    print(f"Generated {output}")


if __name__ == "__main__":
    main()
