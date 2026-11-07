"""Build the HyperFrames composition from edit.json, camera-plan.json, brand.json and graphics.py.

Run through `npm run build` from the repo root (it sets the working directory to the job folder).
Output: composition/index.html, compositions/captions.html, compositions/graphics.html, captions.json.
Everything on screen comes from these sources; never hand-edit the generated HTML.
"""
from pathlib import Path
from html import escape
import json
import re
import sys

from PIL import ImageFont

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import graphics  # noqa: E402

JOB = HERE.parents[1]
COMP = HERE / 'composition'
(COMP / 'compositions').mkdir(parents=True, exist_ok=True)

edit = json.loads((HERE / 'edit.json').read_text())
cam = json.loads((HERE / 'camera-plan.json').read_text())
brand = json.loads((JOB / 'work/brand-kit/brand.json').read_text())
pal, cap, typo = brand['palette'], brand['captions'], brand['typography']

duration = edit['duration']
cuts = {c['id']: c for c in edit['cuts']}
paper_cuts = set(edit.get('paper_cuts') or [])
footage = edit.get('footage') or 'assets/media/footage.mp4'
music = edit.get('music')
font = ImageFont.truetype(str(JOB / 'work/brand-kit/fonts' / f"Inter-{typo['caption_weight']}.ttf"), cap['font_size'])

# ---- captions: one group per punctuation mark, never wider than two lines ----
groups = []
for cut in edit['cuts']:
    words = [w for w in edit['words'] if w['cut'] == cut['id']]
    chunk = []

    def flush():
        if chunk:
            groups.append(dict(text=' '.join(w['text'] for w in chunk), start=chunk[0]['start'],
                               end=chunk[-1]['end'], words=list(chunk), cut=cut['id']))
            chunk.clear()

    for w in words:
        trial = ' '.join(x['text'] for x in chunk + [w])
        if chunk and font.getlength(trial) > cap['max_line_width'] * 2:
            flush()
        chunk.append(w)
        if re.search(r'[,.;:!?]["”’]*$', w['text']):
            flush()
    flush()

for i, g in enumerate(groups):
    nxt = groups[i + 1]['start'] if i + 1 < len(groups) else duration
    c = cuts[g['cut']]
    g['start'] = max(g['start'], c['start'])
    g['end'] = min(nxt, c['start'] + c['duration'], max(g['end'] + cap['tail'], g['start'] + cap['min_duration']))
(HERE / 'captions.json').write_text(json.dumps(groups, indent=2) + '\n')

# ---- camera: pin the neck anchor, change only scale ----
sx, sy = cam['source_anchor']
tx, ty = cam['screen_anchor']
plan = [dict(time=c['time'], scale=c['scale'], x=round(tx - sx * c['scale'], 3), y=round(ty - sy * c['scale'], 3)) for c in cam['cuts']]

# ---- shared CSS ----
fontcss = ''.join(
    f"@font-face{{font-family:Inter;src:url('assets/fonts/inter-latin-{w}-normal.woff2');font-weight:{w};font-display:block}}"
    for w in sorted({typo['hook_weight'], typo['caption_weight'], typo['body_weight']}))
base = fontcss + f"""
@font-face{{font-family:Caveat;src:url('assets/fonts/caveat-variable.ttf');font-weight:400 700;font-display:block}}
#root{{position:absolute;inset:0;color:{pal['ink']};font-family:Inter,sans-serif;--ink:{pal['ink']};--paper:{pal['paper']};--accent:{pal['accent']};--problem:{pal.get('problem', '#B8453C')}}}
.clip{{position:absolute;inset:0}}
.paper{{position:absolute;inset:0;background:#fff}}
.paper:before{{content:'';position:absolute;inset:0;background-color:var(--paper);background-image:linear-gradient(rgba(20,43,91,.065) 1px,transparent 1px),linear-gradient(90deg,rgba(20,43,91,.065) 1px,transparent 1px);background-size:48px 48px;mask-image:linear-gradient(90deg,transparent 8px,#000 80px,#000 calc(100% - 80px),transparent calc(100% - 8px)),linear-gradient(transparent 8px,#000 80px,#000 calc(100% - 80px),transparent calc(100% - 8px));mask-composite:intersect}}
.svg{{position:absolute;inset:0;width:1080px;height:1920px}}
.svg text{{text-anchor:middle;dominant-baseline:middle;fill:var(--ink);font-size:40px;font-weight:700}}
.outline{{stroke:var(--ink);stroke-width:4;fill:none;stroke-linecap:round;stroke-linejoin:round}}
.accent{{stroke:var(--accent);stroke-width:9;fill:none;stroke-linecap:round}}
.problem{{stroke:var(--problem)}}
.svg .hand{{font-family:Caveat;font-size:43px;font-weight:600}}
.diagram-stage{{position:absolute;inset:0;transform:translateY(-88px)}}
.quote{{position:absolute;left:180px;top:660px;width:720px;text-align:center;font-size:40px;font-weight:700;line-height:1.2;color:var(--problem)}}
.caption{{position:absolute;left:{cap['x']}px;top:{cap['y']}px;width:{cap['width']}px;text-align:center;color:{pal.get('footage_text', '#fff')};font-size:{cap['font_size']}px;line-height:1.17;font-weight:{typo['caption_weight']};letter-spacing:-1px}}
.caption .inner{{display:inline-block;max-width:{cap['width']}px;text-shadow:0 2px 4px rgba(0,0,0,.85);-webkit-text-stroke:1.3px rgba(0,0,0,.65);paint-order:stroke fill}}
.caption.paper-cap{{color:var(--ink)}}
.caption.paper-cap .inner{{text-shadow:none;-webkit-text-stroke:0}}
.caption span.em{{color:var(--accent)}}
.caption.paper-cap span.em{{color:var(--ink);text-decoration:underline;text-decoration-color:var(--accent);text-decoration-thickness:7px;text-underline-offset:8px}}
"""

# ---- graphics ----
scenes = graphics.build(edit, cuts, pal)
scene_html = ''.join(
    f'<div id="{s["id"]}" class="clip" data-start="{s["start"]}" data-duration="{s["end"] - s["start"]}" data-track-index="1" data-beat="{escape(s.get("beat", ""))}">'
    f'<div class="paper" data-layout-ignore></div><div class="diagram-stage">{s["svg"]}</div></div>' for s in scenes)
scene_timeline = '\n'.join(s.get('timeline', '') for s in scenes)
(COMP / 'compositions/graphics.html').write_text(f'''<template><style>{base}</style><div id="root" data-composition-id="graphics" data-width="1080" data-height="1920">
{scene_html}
</div><script>(function(){{const tl=gsap.timeline({{paused:true}});
function draw(id,t,d=.45){{const p=document.querySelector(id);const l=p.getTotalLength();tl.fromTo(p,{{opacity:0,strokeDasharray:l,strokeDashoffset:l}},{{opacity:1,strokeDashoffset:0,duration:d,ease:'power1.inOut',immediateRender:true}},t)}}
function arrow(id,t){{draw(id,t,.46);draw(id+'h',t+.42,.12)}}
function show(id,t){{tl.fromTo(id,{{opacity:0}},{{opacity:1,duration:.18,immediateRender:true}},t)}}
{scene_timeline}
window.__timelines=window.__timelines||{{}};window.__timelines.graphics=tl;}})();</script></template>''')

# ---- captions ----
emphasis = set(edit.get('emphasis') or [])
html = []
for i, g in enumerate(groups):
    toks = g['text'].split()
    br = -1
    if font.getlength(g['text']) > cap['max_line_width'] and len(toks) > 1:
        br = min(range(1, len(toks)), key=lambda n: max(font.getlength(' '.join(toks[:n])), font.getlength(' '.join(toks[n:]))))
    styled = ''
    for j, word in enumerate(toks):
        if j:
            styled += '<br>' if j == br else ' '
        clean = word.strip('.,;:!?"”’')
        styled += f'<span class="em">{escape(word)}</span>' if clean in emphasis else escape(word)
    paper = 'paper-cap' if g['cut'] in paper_cuts else ''
    html.append(f'<div id="cap-{i}" class="clip" data-start="{g["start"]}" data-duration="{g["end"] - g["start"]}" data-track-index="0">'
                f'<div class="caption {paper}"><span class="inner">{styled}</span></div></div>')
(COMP / 'compositions/captions.html').write_text(
    f'<template><style>{base}</style><div id="root" data-composition-id="captions" data-width="1080" data-height="1920">' + ''.join(html)
    + '</div><script>window.__timelines=window.__timelines||{};window.__timelines.captions=gsap.timeline({paused:true});</script></template>')

# ---- root composition ----
music_el = (f'<audio id="music-bed" class="clip" data-start="0" data-duration="{duration}" data-track-index="3" '
            f'data-volume="{edit.get("music_volume", 0.25)}" src="{music}"></audio>') if music else ''
graphics_el = (f'<div id="graphics-host" data-composition-id="graphics" class="clip" data-start="0" data-duration="{duration}" data-track-index="1" '
               f'data-track-kind="graphics" data-composition-src="compositions/graphics.html" data-layout-allow-overlap></div>') if scenes else ''
root = f'''<!doctype html><html lang="en" data-resolution="portrait"><head><meta charset="utf-8"><title>{escape(edit.get('title', 'Video'))}</title><script src="assets/vendor/gsap.min.js"></script><style>*{{box-sizing:border-box;margin:0}}html,body{{width:1080px;height:1920px;overflow:hidden;background:{pal['ink']}}}.clip{{position:absolute;inset:0}}video{{width:1080px;height:1920px;object-fit:cover}}#main{{width:1080px;height:1920px;position:relative}}</style></head><body><div id="main" data-composition-id="main" data-width="1080" data-height="1920" data-duration="{duration}"><video id="footage" class="clip" data-start="0" data-duration="{duration}" data-track-index="0" data-has-audio="true" src="{footage}" playsinline data-layout-ignore></video>{music_el}{graphics_el}<div id="captions-host" data-composition-id="captions" class="clip" data-start="0" data-duration="{duration}" data-track-index="2" data-track-kind="captions" data-composition-src="compositions/captions.html" data-layout-allow-overlap></div></div><script>window.__timelines=window.__timelines||{{}};const main=gsap.timeline({{paused:true}});window.__timelines.main=main;
const cameraPlan={json.dumps(plan)};
cameraPlan.forEach(c=>main.set('#footage',{{scale:c.scale,x:c.x,y:c.y,transformOrigin:'0 0'}},c.time));</script></body></html>'''
(COMP / 'index.html').write_text(root)
print(f'Built {duration:.3f}s: {len(groups)} caption groups, {len(scenes)} diagram scene(s), {len(plan)} camera cuts.')
