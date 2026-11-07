# Paper grid / visual prototype

15 seconds, 1080 x 1920, 30 fps. Silent motion study of the paper-diagram style; a reference for drawing your own scenes in `graphics.py`. No footage, no synthesized voice.

One sheet of paper stays in place. Brand hook weight for headlines, caption weight for diagram labels, body weight for supporting labels. Palette from `../brand-kit/brand.json`. Grid: uniform 48px micro squares at 6.5% ink opacity. White outer 8px; a 72px fade into paper on all edges. No major grid. Ink outlines, accent marks. No camera drift, bouncing text, neon glow or fake interface.

0-2s: hook on frame zero; owner circle draws. 2-5.5s: three requests connect to the owner, accent underline marks the bottleneck. 6-9.5s: owner moves up, engineers enter and request routes rewire. 11.5-15s: payoff lands, hold at least 2 seconds.

Drawing rules: unfilled contours; seeded fixed geometry; separate tangent-aligned arrowheads with a straight approach; connectors never cross text or objects. Full rules in `../../notes/paper-grid-format.json`.

Preview: `npx hyperframes preview "Short Form/work/paper-grid"` from the repo root.
