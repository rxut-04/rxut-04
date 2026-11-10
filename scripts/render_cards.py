#!/usr/bin/env python3
"""Renders animated SVG profile cards into ./cards from live GitHub data."""
import os
import json
import math
import datetime as dt
import urllib.request
from collections import defaultdict
from pathlib import Path
from xml.sax.saxutils import escape

USER = os.environ.get("GH_USER", "rxut-04")
TOKEN = os.environ["GH_TOKEN"]
STATIC = os.environ.get("STATIC") == "1"   # STATIC=1 -> final frame, no animation
OUT = Path("cards")
OUT.mkdir(exist_ok=True)

# ---------- EDIT THESE ----------
NAME = "Om Raut"
TAGLINE = "I build things that actually impress."
SUB1 = "Final-year IT student @ SVIT Nashik"
SUB2 = "Full-stack · Computer Vision · Hardware · Mobile"
STATUS = "Open to internships & collabs"
LEARN_BIG = "React"
LEARN_CAP = "learning now · DSA in Java"
# --------------------------------

BLUE, RED, YELLOW = "#2F55FF", "#EF3B2D", "#FDC518"
ACCENT = BLUE
PINK, SOFT, ROSE = BLUE, "#9DB0FF", "#6C85FF"
SERIF = "Georgia, 'Times New Roman', serif"
MONO = "ui-monospace, 'SF Mono', Menlo, Consolas, 'DejaVu Sans Mono', monospace"

THEMES = {
    "dark": dict(bg="#161616", ink="#F4F3F0", muted="#9A9A95", line="#2A2A2A",
                 ramp=["#1E2A5C", "#2F44A8", "#2F55FF", "#7C97FF"]),
    "light": dict(bg="#F4F3F0", ink="#111111", muted="#77756F", line="#E2E0DA",
                  ramp=["#C9D4FF", "#8FA6FF", "#4D6DFF", "#1A3BE0"]),
}

CSS = """
@keyframes rise{from{opacity:0;transform:translateY(14px)}to{opacity:1;transform:none}}
@keyframes pop{0%{opacity:0;transform:scale(.3)}70%{opacity:1;transform:scale(1.18)}100%{opacity:1;transform:scale(1)}}
@keyframes grow{from{transform:scaleY(0)}to{transform:scaleY(1)}}
@keyframes swing{0%{opacity:0;transform:translateY(46px) rotate(-6deg)}60%{opacity:1;transform:translateY(-7px) rotate(1.5deg)}100%{opacity:1;transform:none}}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.3}}
@keyframes ring{0%{transform:scale(.6);opacity:.8}100%{transform:scale(2.4);opacity:0}}
@keyframes nudge{0%,100%{transform:translateX(0)}50%{transform:translateX(7px)}}
@keyframes sweep{0%,55%{transform:translateX(-120px) skewX(-18deg)}100%{transform:translateX(950px) skewX(-18deg)}}
.rise{animation:rise .8s cubic-bezier(.2,.8,.2,1) both}
.pop{transform-box:fill-box;transform-origin:center;animation:pop .55s cubic-bezier(.2,.9,.3,1.2) both}
.bar{transform-box:fill-box;transform-origin:bottom;animation:grow .9s cubic-bezier(.2,.8,.2,1) both}
.swing{transform-box:fill-box;transform-origin:bottom left;animation:swing .95s cubic-bezier(.2,.9,.3,1.1) both}
.pulse{animation:pulse 2s ease-in-out infinite}
.ring{transform-box:fill-box;transform-origin:center;animation:ring 2.4s ease-out infinite}
.nudge{animation:nudge 1.6s ease-in-out infinite}
.sweep{animation:sweep 5s ease-in-out infinite}
@media (prefers-reduced-motion:reduce){*{animation:none!important}}
"""

TODAY = dt.datetime.utcnow().date()


# ---------------------------------------------------------------- data
def gql(query, variables):
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": query, "variables": variables}).encode(),
        headers={"Authorization": f"bearer {TOKEN}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req) as r:
        data = json.load(r)
    if "errors" in data:
        raise RuntimeError(data["errors"])
    return data["data"]


def fetch():
    meta = gql(
        """query($l:String!){user(login:$l){createdAt followers{totalCount}
        repositories(privacy:PUBLIC,ownerAffiliations:OWNER){totalCount}}}""",
        {"l": USER},
    )["user"]
    start = dt.datetime.strptime(meta["createdAt"], "%Y-%m-%dT%H:%M:%SZ")
    now = dt.datetime.utcnow()
    q = """query($l:String!,$f:DateTime!,$t:DateTime!){user(login:$l){
      contributionsCollection(from:$f,to:$t){contributionCalendar{
      weeks{contributionDays{date contributionCount}}}}}}"""
    daily, cur = {}, start
    while cur < now:
        end = min(cur + dt.timedelta(days=364), now)
        d = gql(q, {"l": USER, "f": cur.strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "t": end.strftime("%Y-%m-%dT%H:%M:%SZ")})
        for w in d["user"]["contributionsCollection"]["contributionCalendar"]["weeks"]:
            for day in w["contributionDays"]:
                daily[day["date"]] = day["contributionCount"]
        cur = end + dt.timedelta(days=1)
    return meta, daily


def streaks(daily):
    longest = run = 0
    prev = None
    for d in sorted(daily):
        if daily[d] > 0:
            cd = dt.date.fromisoformat(d)
            run = run + 1 if prev and (cd - prev).days == 1 else 1
            prev = cd
            longest = max(longest, run)
    cur, d = 0, TODAY
    if daily.get(d.isoformat(), 0) == 0:
        d -= dt.timedelta(days=1)
    while daily.get(d.isoformat(), 0) > 0:
        cur += 1
        d -= dt.timedelta(days=1)
    return cur, longest


def monthly(daily, n=24):
    m = defaultdict(int)
    for k, v in daily.items():
        m[k[:7]] += v
    y, mo, keys = TODAY.year, TODAY.month, []
    for _ in range(n):
        keys.append(f"{y:04d}-{mo:02d}")
        mo -= 1
        if mo == 0:
            y, mo = y - 1, 12
    keys.reverse()
    return [(k, m.get(k, 0)) for k in keys]


# ---------------------------------------------------------------- svg helpers
def card(w, h, inner, bg, line, defs="", wrap=""):
    static = "*{animation:none!important}" if STATIC else ""
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img">'
        f'<style>{CSS}{static}</style>'
        f'<defs><clipPath id="c"><rect width="{w}" height="{h}" rx="22"/></clipPath>{defs}</defs>'
        f'<g {wrap}>'
        f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="22" fill="{bg}" stroke="{line}" stroke-width="2"/>'
        f'<g clip-path="url(#c)"><rect class="sweep" x="0" y="-40" width="70" height="{h+80}" fill="{PINK}" opacity=".10"/></g>'
        f'{inner}</g></svg>'
    )


def dl(s):
    return f'style="animation-delay:{s}s"'


# ---------------------------------------------------------------- cards
def hero(t):
    W, H = 830, 290
    ink, mut = t["ink"], t["muted"]
    defs = (f'<linearGradient id="g" x1="0" x2="1"><stop offset="0" stop-color="{PINK}"/>'
            f'<stop offset="1" stop-color="{ROSE}"/></linearGradient>')
    term = [("$ whoami", PINK), ("om_raut", ink), ("$ ls stack/", PINK),
            ("fullstack  cv  hw  mobile", ink), ("$ status", PINK), ("building something big", ink)]
    lines = "".join(
        f'<text class="rise" {dl(1.0 + i * 0.28)} x="540" y="{98 + i * 27}" font-family="{MONO}" '
        f'font-size="13" fill="{c}">{escape(s)}</text>' for i, (s, c) in enumerate(term))
    inner = f'''
<circle class="pulse" cx="48" cy="50" r="5" fill="{PINK}"/>
<text class="rise" {dl(.1)} x="62" y="55" font-family="{MONO}" font-size="13" fill="{mut}">{escape(STATUS)}</text>
<text class="rise" {dl(.25)} x="42" y="140" font-family="{SERIF}" font-size="80" fill="url(#g)">{escape(NAME)}</text>
<text class="rise" {dl(.55)} x="46" y="184" font-family="{SERIF}" font-size="24" font-style="italic" fill="{ink}">{escape(TAGLINE)}</text>
<text class="rise" {dl(.75)} x="46" y="226" font-family="{MONO}" font-size="13.5" fill="{mut}">{escape(SUB1)}</text>
<text class="rise" {dl(.9)} x="46" y="248" font-family="{MONO}" font-size="13.5" fill="{mut}">{escape(SUB2)}</text>
<rect x="520" y="34" width="274" height="222" rx="14" fill="{t["line"]}" opacity=".45"/>
<circle cx="542" cy="54" r="5" fill="{PINK}"/><circle cx="560" cy="54" r="5" fill="{ROSE}"/><circle cx="578" cy="54" r="5" fill="{SOFT}"/>
{lines}
<rect class="pulse" x="716" y="221" width="8" height="15" fill="{PINK}"/>'''
    return card(W, H, inner, t["bg"], t["line"], defs)


def graph(t, daily):
    W, H = 830, 205
    start = TODAY - dt.timedelta(days=(TODAY.weekday() + 1) % 7 + 52 * 7)
    days = [start + dt.timedelta(days=i) for i in range(53 * 7)]
    vals = {d: daily.get(d.isoformat(), 0) for d in days if d <= TODAY}
    mx = max(1, max(vals.values()))
    total = sum(vals.values())
    ramp = t["ramp"]
    cells, labels = "", ""
    for i, d in enumerate(days):
        if d > TODAY:
            continue
        wk, row = divmod(i, 7)
        v = vals[d]
        lvl = 0 if v == 0 else min(4, max(1, math.ceil(4 * v / mx)))
        col = t["line"] if lvl == 0 else ramp[lvl - 1]
        x, y = 20 + wk * 15, 62 + row * 15
        cells += f'<rect class="pop" {dl(round(.2 + wk * .015, 3))} x="{x}" y="{y}" width="12" height="12" rx="3" fill="{col}"/>'
        if row == 0 and d.day <= 7:
            labels += f'<text x="{x}" y="54" font-family="{MONO}" font-size="10" fill="{t["muted"]}">{d.strftime("%b")}</text>'
    legend = "".join(f'<rect x="{680 + i * 16}" y="180" width="12" height="12" rx="3" fill="{c}"/>'
                     for i, c in enumerate([t["line"]] + ramp))
    inner = f'''
<text class="rise" x="20" y="34" font-family="{SERIF}" font-size="21" fill="{t["ink"]}">Contribution graph</text>
<text class="rise" {dl(.1)} x="810" y="34" text-anchor="end" font-family="{MONO}" font-size="12" fill="{PINK}">{total:,} in the last year</text>
{labels}{cells}
<text x="640" y="190" font-family="{MONO}" font-size="10" fill="{t["muted"]}">less</text>{legend}
<text x="752" y="190" font-family="{MONO}" font-size="10" fill="{t["muted"]}">more</text>'''
    return card(W, H, inner, t["bg"], t["line"])


def months(t, daily):
    W, H = 830, 300
    data = monthly(daily)
    n = len(data)
    mx = max(1, max(v for _, v in data))
    best = max(range(n), key=lambda i: data[i][1])
    cur, longest = streaks(daily)
    active = sum(1 for v in daily.values() if v > 0)
    bd, bc = max(daily.items(), key=lambda kv: kv[1])
    x0, x1, base, max_h = 30, 800, 190, 120
    slot = (x1 - x0) / n
    bw = slot * 0.62
    bars = ""
    for i, (k, v) in enumerate(data):
        h = max(3, v / mx * max_h) if v else 3
        x = x0 + i * slot + (slot - bw) / 2
        col = ACCENT if i == best else (t["ink"] if v else t["line"])
        bars += (f'<rect class="bar" {dl(round(.2 + i * .04, 2))} x="{x:.1f}" y="{base - h:.1f}" '
                 f'width="{bw:.1f}" height="{h:.1f}" rx="4" fill="{col}"/>')
        if (n - 1 - i) % 3 == 0:
            lab = dt.date(int(k[:4]), int(k[5:7]), 1).strftime("%b %y")
            bars += (f'<text x="{x + bw / 2:.1f}" y="{base + 18}" text-anchor="middle" font-family="{MONO}" '
                     f'font-size="10" fill="{t["muted"]}">{lab}</text>')
    bk, bv = data[best]
    bx = x0 + best * slot + slot / 2
    bh = max(3, bv / mx * max_h)
    best_lab = dt.date(int(bk[:4]), int(bk[5:7]), 1).strftime("%b %Y")
    chips_data = [("current streak", f"{cur} days"), ("longest streak", f"{longest} days"),
                  ("active days", f"{active}"),
                  (f"busiest day · {dt.date.fromisoformat(bd).strftime('%b %d')}", f"{bc}")]
    cw = (770 - 3 * 14) / 4
    chips = ""
    for i, (lab, val) in enumerate(chips_data):
        x = 30 + i * (cw + 14)
        chips += (f'<g class="rise" {dl(1.4 + i * .12)}>'
                  f'<rect x="{x:.1f}" y="226" width="{cw:.1f}" height="58" rx="12" fill="{t["line"]}" opacity=".55"/>'
                  f'<text x="{x + 14:.1f}" y="246" font-family="{MONO}" font-size="10.5" fill="{t["muted"]}">{escape(lab)}</text>'
                  f'<text x="{x + 14:.1f}" y="274" font-family="{SERIF}" font-size="24" fill="{t["ink"]}">{escape(val)}</text></g>')
    inner = f'''
<text class="rise" x="30" y="38" font-family="{SERIF}" font-size="21" fill="{t["ink"]}">Contributions per month</text>
<text class="rise" {dl(.1)} x="800" y="38" text-anchor="end" font-family="{MONO}" font-size="12" fill="{PINK}">best: {best_lab}</text>
{bars}
<text class="pop" {dl(1.3)} x="{bx:.1f}" y="{base - bh - 8:.1f}" text-anchor="middle" font-family="{MONO}" font-size="12" font-weight="bold" fill="{PINK}">{bv}</text>
{chips}'''
    return card(W, H, inner, t["bg"], t["line"])


def tile(label, big, cap, bg, ink, delay, bigsize=64):
    W, H = 270, 200
    inner = f'''
<circle class="ring" cx="236" cy="38" r="12" fill="none" stroke="{ink}" stroke-width="2"/>
<circle cx="236" cy="38" r="5" fill="{ink}"/>
<text x="24" y="44" font-family="{MONO}" font-size="13" letter-spacing="3" fill="{ink}" opacity=".75">{label}</text>
<text class="pop" {dl(delay + .5)} x="24" y="124" font-family="{SERIF}" font-size="{bigsize}" fill="{ink}">{escape(big)}</text>
<text class="rise" {dl(delay + .7)} x="24" y="154" font-family="{MONO}" font-size="12.5" fill="{ink}">{escape(cap)}</text>
<text class="nudge" x="246" y="182" text-anchor="end" font-family="{SERIF}" font-size="30" fill="{ink}">→</text>'''
    return card(W, H, inner, bg, bg, wrap=f'class="swing" {dl(delay)}')


# ---------------------------------------------------------------- main
if __name__ == "__main__":
    meta, daily = fetch()
    for name, t in THEMES.items():
        (OUT / f"hero-{name}.svg").write_text(hero(t), encoding="utf-8")
        (OUT / f"graph-{name}.svg").write_text(graph(t, daily), encoding="utf-8")
        (OUT / f"months-{name}.svg").write_text(months(t, daily), encoding="utf-8")
    repos = meta["repositories"]["totalCount"]
    followers = meta["followers"]["totalCount"]
    (OUT / "build.svg").write_text(tile("BUILD", str(repos), "public repos on GitHub", BLUE, "#FFFFFF", 2.2), encoding="utf-8")
    (OUT / "learn.svg").write_text(tile("LEARN", LEARN_BIG, LEARN_CAP, RED, "#FFFFFF", 2.5, 54), encoding="utf-8")
    (OUT / "connect.svg").write_text(tile("CONNECT", str(followers), "followers · say hi", YELLOW, "#111111", 2.8), encoding="utf-8")
    print("Cards written to ./cards")
