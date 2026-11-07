"""Paper diagram scenes for the starter video.

build(edit, cuts, palette) returns a list of scenes. Each scene is a dict:
  id        unique element id
  start/end composition seconds
  svg       inner HTML drawn on the paper (SVG or divs, 1080x1920 coordinates)
  timeline  GSAP calls appended to the graphics timeline; helpers available:
            draw('#path', t, dur)  strokes a path in
            arrow('#path', t)      strokes a shaft then its head ('#path' + 'h')
            show('#el', t)         fades an element in
Return [] for a video with no diagrams. Replace this example with your own scenes;
keep the drawing rules in ../../notes/paper-grid-format.json.
"""
import math


def person(x, y, r=30, ident=''):
    s = r / 30
    return (f'<g id="{ident}" transform="translate({x} {y})"><circle class="outline" r="{r}"/>'
            f'<g transform="scale({s})"><circle class="outline" cy="-8" r="6.5"/>'
            f'<path class="outline" d="M-13 12 C-12 0 12 0 13 12"/></g></g>')


def arrow_geometry(x, y, cx=540, cy=960, inner=82, outer=48, inbound=False):
    """Shaft from the centre node edge to just outside the target node, with a straight tip."""
    dx, dy = x - cx, y - cy
    length = math.hypot(dx, dy)
    ux, uy = dx / length, dy / length
    ax, ay = cx + ux * inner, cy + uy * inner
    bx, by = x - ux * outer, y - uy * outer
    if inbound:
        ax, ay, bx, by = bx, by, ax, ay
    dx, dy = bx - ax, by - ay
    length = math.hypot(dx, dy)
    ux, uy = dx / length, dy / length
    nx, ny = -uy, ux
    ex, ey = bx - ux * 20, by - uy * 20
    mx, my = (ax + ex) / 2 + nx * 3, (ay + ey) / 2 + ny * 3
    path = f'M{ax:.2f} {ay:.2f} Q{mx:.2f} {my:.2f} {ex:.2f} {ey:.2f} L{bx:.2f} {by:.2f}'
    head = (f'M{bx - ux * 13 + nx * 7:.2f} {by - uy * 13 + ny * 7:.2f} L{bx:.2f} {by:.2f} '
            f'L{bx - ux * 13 - nx * 7:.2f} {by - uy * 13 - ny * 7:.2f}')
    return path, head


def build(edit, cuts, palette):
    paper_cuts = edit.get('paper_cuts') or []
    if not paper_cuts:
        return []
    first = cuts[paper_cuts[0]]
    t0, t1 = first['start'], first['start'] + first['duration']

    # Example: you in the middle, three people connected to you. Everything centred on 540,960.
    svg = ['<svg class="svg" viewBox="0 0 1080 1920" aria-label="Three people connect to you">'
           '<g id="network" data-layout-allow-overlap>']
    timeline = []
    coords = [(540 + 300 * math.cos(a), 960 + 150 * math.sin(a)) for a in (math.pi * 7 / 6, math.pi * 11 / 6, math.pi / 2)]
    for i, (x, y) in enumerate(coords):
        shaft, head = arrow_geometry(x, y)
        svg.append(f'<g class="outline"><path id="out-{i}" d="{shaft}"/><path id="out-{i}h" d="{head}"/></g>')
        svg.append(person(round(x, 2), round(y, 2), 30, ident=f'user-{i}'))
        t = t0 + 0.9 + i * 0.35
        timeline.append(f"show('#user-{i}',{t:.3f});arrow('#out-{i}',{t + 0.08:.3f});")
    svg.append('<g id="owner"><circle class="outline" cx="540" cy="960" r="60"/>'
               '<circle class="outline" cx="540" cy="942" r="10"/>'
               '<path class="outline" d="M521 969 C521 952 559 952 559 969"/>'
               '<text x="540" y="1050" style="font-size:36px">You</text></g>')
    svg.append('</g></svg>')
    timeline.insert(0, f"tl.fromTo('#owner',{{opacity:0,scale:1.4,svgOrigin:'540 960'}},{{opacity:1,scale:1,svgOrigin:'540 960',duration:.6,ease:'power2.out',immediateRender:true}},{t0 + 0.2:.3f});")

    return [{
        'id': 'scene-network',
        'start': t0,
        'end': t1,
        'beat': 'Who depends on you',
        'svg': ''.join(svg),
        'timeline': '\n'.join(timeline),
    }]
