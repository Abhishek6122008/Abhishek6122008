"""leetcode.svg: solved donut by difficulty, beats-% bars, contest rating, streaks,
weekly submissions for the last year and top topics. Data from fetch_leetcode.py."""
import math
from datetime import date, timedelta

from common import BORDER, FG, MUTED, PANEL, esc, load, window, write_svg

W, H = 860, 400
EASY, MEDIUM, HARD = "#00b8a3", "#ffc01e", "#ff375f"
LC = "#ffa116"
DIFFS = [("Easy", EASY), ("Medium", MEDIUM), ("Hard", HARD)]
CH = {10: 6.0, 11: 6.6, 12: 7.2, 13: 7.8}  # monospace advance per font size


def donut(lc, cx, cy, r):
    solved = [lc["solved"].get(d, 0) for d, _ in DIFFS]
    total = sum(solved) or 1
    circ = 2 * math.pi * r
    gap = 3 if sum(1 for s in solved if s) > 1 else 0
    out = [f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{BORDER}" stroke-width="10"/>']
    cum = 0.0
    for k, ((_, color), n) in enumerate(zip(DIFFS, solved)):
        seg = circ * n / total
        if seg > gap:
            out.append(
                f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{color}" stroke-width="10" '
                f'stroke-dasharray="0 {circ:.1f}" stroke-dashoffset="{-cum:.1f}" transform="rotate(-90 {cx} {cy})">'
                f'<animate attributeName="stroke-dasharray" from="0 {circ:.1f}" to="{seg - gap:.1f} {circ:.1f}" '
                f'begin="{0.6 + k * 0.45:.2f}s" dur="0.7s" fill="freeze" calcMode="spline" keySplines=".3 .7 .3 1" keyTimes="0;1"/></circle>'
            )
        cum += seg
    out.append(
        f'<g class="fin" style="animation-delay:.4s" text-anchor="middle">'
        f'<text x="{cx}" y="{cy + 6}" font-size="34" font-weight="800" fill="{FG}">{lc["solved"].get("All", total)}</text>'
        f'<text x="{cx}" y="{cy + 26}" font-size="11" fill="{MUTED}">solved</text></g>'
    )
    return "".join(out)


def difficulty_bars(lc, x, y, bw):
    out = []
    for k, (d, color) in enumerate(DIFFS):
        ry = y + k * 52
        beats = lc.get("beats", {}).get(d)
        right = (
            f'<text x="{x + bw}" y="{ry}" font-size="11" fill="{MUTED}" text-anchor="end">beats '
            f'<tspan fill="{color}" font-weight="700">{beats:.1f}%</tspan></text>'
            if beats is not None else ""
        )
        fill = bw * (beats if beats is not None else 100 * lc["solved"].get(d, 0) / max(1, lc["total"].get(d, 1))) / 100
        out.append(
            f'<g class="fin" style="animation-delay:{0.5 + k * 0.15:.2f}s">'
            f'<text x="{x}" y="{ry}" font-size="13" font-weight="700" fill="{color}">{d}</text>'
            f'<text x="{x + 72}" y="{ry}" font-size="15" font-weight="700" fill="{FG}">{lc["solved"].get(d, 0)}'
            f'<tspan font-size="11" font-weight="400" fill="{MUTED}"> / {lc["total"].get(d, 0):,}</tspan></text>{right}'
            f'<rect x="{x}" y="{ry + 10}" width="{bw}" height="6" rx="3" fill="{BORDER}"/>'
            f'<rect x="{x}" y="{ry + 10}" width="0" height="6" rx="3" fill="{color}">'
            f'<animate attributeName="width" from="0" to="{fill:.1f}" begin="{0.9 + k * 0.2:.2f}s" dur="1.1s" fill="freeze" '
            f'calcMode="spline" keySplines=".2 .8 .2 1" keyTimes="0;1"/></rect></g>'
        )
    return "".join(out)


def contest_block(lc, x, y):
    c = lc.get("contest")
    rows = []
    if c and c.get("attended"):
        rows.append(f'<text x="{x}" y="{y}" font-size="11" fill="{MUTED}">contest rating</text>')
        rows.append(f'<text x="{x}" y="{y + 40}" font-size="40" font-weight="800" fill="url(#lcGrad)">{round(c["rating"])}</text>')
        rows.append(
            f'<text x="{x}" y="{y + 64}" font-size="12" fill="{FG}">top {c["top_percentage"]:g}%'
            f'<tspan fill="{MUTED}">  ·  {c["attended"]} contests</tspan></text>'
        )
    else:
        rows.append(f'<text x="{x}" y="{y}" font-size="11" fill="{MUTED}">global rank</text>')
        rows.append(f'<text x="{x}" y="{y + 40}" font-size="34" font-weight="800" fill="url(#lcGrad)">#{lc["ranking"]:,}</text>')
    rows.append(
        f'<text x="{x}" y="{y + 102}" font-size="20" font-weight="800" fill="{LC}">{lc["current_streak"]}d'
        f'<tspan font-size="11" font-weight="400" fill="{MUTED}" dx="6">current streak</tspan></text>'
    )
    rows.append(
        f'<text x="{x}" y="{y + 124}" font-size="11" fill="{MUTED}">{lc["max_streak"]}d best  ·  {lc["active_days"]} active days</text>'
    )
    return "".join(f'<g class="fin" style="animation-delay:{0.7 + k * 0.12:.2f}s">{r}</g>' for k, r in enumerate(rows))


def weekly(lc, x0, base, width, hmax):
    cal = {date.fromisoformat(d): n for d, n in lc.get("calendar", {}).items()}
    today = date.today()
    start = today - timedelta(days=364)
    start -= timedelta(days=(start.weekday() + 1) % 7)  # back up to Sunday
    weeks = (today - start).days // 7 + 1
    counts = [sum(cal.get(start + timedelta(days=w * 7 + i), 0) for i in range(7)) for w in range(weeks)]
    peak = max(counts) or 1
    step = width / weeks
    bw = step - 3.5
    out, months, last = [], [], None
    for w, n in enumerate(counts):
        x = x0 + w * step
        wk = start + timedelta(days=w * 7)
        tip = f"<title>{n} submissions · week of {wk.strftime('%b %d')}</title>"
        if n:
            h = 4 + (hmax - 4) * n / peak
            op = 0.45 + 0.55 * n / peak
            out.append(
                f'<rect class="b" style="animation-delay:{1.2 + w * 0.02:.2f}s" x="{x:.1f}" y="{base - h:.1f}" width="{bw:.1f}" '
                f'height="{h:.1f}" rx="2" fill="url(#barGrad)" opacity="{op:.2f}">{tip}</rect>'
            )
        else:
            out.append(f'<rect x="{x:.1f}" y="{base - 2}" width="{bw:.1f}" height="2" rx="1" fill="{BORDER}">{tip}</rect>')
        for i in range(7):
            d = wk + timedelta(days=i)
            if d.day == 1 and d.month != last and w < weeks - 2:
                months.append(f'<text x="{x:.1f}" y="{base + 15}" font-size="10" fill="{MUTED}">{d.strftime("%b")}</text>')
                last = d.month
    return "".join(out) + "".join(months), sum(counts)


def topic_chips(lc, x, y, xmax):
    out = []
    for k, (tag, n) in enumerate(lc.get("top_tags", {}).items()):
        label_w = len(tag) * CH[11] + 6 + len(str(n)) * CH[11]
        w = label_w + 20
        if x + w > xmax:
            break
        out.append(
            f'<g class="fin" style="animation-delay:{2.2 + k * 0.08:.2f}s">'
            f'<rect x="{x:.1f}" y="{y - 14}" width="{w:.1f}" height="20" rx="10" fill="{PANEL}" stroke="{BORDER}"/>'
            f'<text x="{x + 10:.1f}" y="{y}" font-size="11" fill="{FG}">{esc(tag)}<tspan dx="6" fill="{LC}">{n}</tspan></text></g>'
        )
        x += w + 8
    return "".join(out)


def main():
    lc = load("leetcode.json")
    if not lc:
        print("no data/leetcode.json, skipping leetcode.svg (run fetch_leetcode.py)")
        return

    head = f"leetcode.com/u/{lc['username']}"
    bars, subs = weekly(lc, 36, 322, W - 72, 46)
    badge = lc["badges"][0] if lc.get("badges") else ""
    badge_svg = (
        f'<g class="fin" style="animation-delay:2.6s"><text x="{W - 36}" y="378" font-size="11" fill="{LC}" text-anchor="end">'
        f'&#9670; {esc(badge)}</text></g>' if badge else ""
    )
    chips_max = W - 36 - (len(badge) + 2) * CH[11] - 16 if badge else W - 36
    langs = lc.get("languages", {})
    lang_note = f"  ·  mostly {next(iter(langs))}" if langs else ""

    defs = f"""
<linearGradient id="lcGrad" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{LC}"/><stop offset="1" stop-color="{MEDIUM}"/></linearGradient>
<linearGradient id="barGrad" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="{LC}"/><stop offset="1" stop-color="{MEDIUM}"/></linearGradient>
<radialGradient id="halo" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="{LC}" stop-opacity="0.14"/><stop offset="1" stop-color="{LC}" stop-opacity="0"/></radialGradient>
<style>
  .fin {{ opacity: 0; animation: fin .6s ease-out forwards; }}
  @keyframes fin {{ to {{ opacity: 1; }} }}
  .b {{ transform-box: fill-box; transform-origin: 50% 100%; transform: scaleY(0); animation: rise .7s cubic-bezier(.2,1.3,.4,1) forwards; }}
  @keyframes rise {{ to {{ transform: scaleY(1); }} }}
</style>"""
    body = f"""
<text x="36" y="62" font-size="13" fill="{FG}"><tspan fill="{LC}">$</tspan> leetcode --user {esc(lc['username'])} --stats</text>
<text x="{W - 36}" y="62" font-size="11" fill="{MUTED}" text-anchor="end">{esc(head)}</text>
<circle cx="132" cy="168" r="96" fill="url(#halo)"/>
{donut(lc, 132, 168, 60)}
{difficulty_bars(lc, 248, 118, 300)}
<line x1="582" y1="96" x2="582" y2="238" stroke="{BORDER}"/>
{contest_block(lc, 610, 106)}
<g class="fin" style="animation-delay:1s"><text x="36" y="262" font-size="11" fill="{MUTED}">submissions per week  ·  <tspan fill="{FG}">{subs:,}</tspan> in the last year{esc(lang_note)}</text></g>
{bars}
{topic_chips(lc, 36, 378, chips_max)}
{badge_svg}
"""
    write_svg("leetcode.svg", window(W, H, "leetcode.sh", body, defs))


if __name__ == "__main__":
    main()
