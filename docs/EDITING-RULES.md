# Editing rules

These are the decisions the system encodes. Change them in `brand.json` and the notes files, not in generated HTML.

## Framing: the neck anchor

Pick one stable point at the base of the neck in the source clip. Pin it to one screen point. Between cuts only the scale changes, so a punch-in zooms around that point and a punch-out returns to exactly the same crop as before. Never track eyes, the head or hands, and never nudge the frame at a pause trim: natural movement stays inside the frame, the frame stays still. When the camera or seating changes, choose a new anchor and save the reference frame.

Why: moving the crop to chase a face creates small sideways jumps at every cut that viewers feel as instability. A fixed anchor reads as a locked camera with deliberate cut-ins.

Punch-ins of 20 to 25 percent read as intentional. Check stationary background position across cuts, not only eye position.

## Captions

- The words actually spoken, from the transcript. Never the script.
- One caption ends at a comma, period, colon, semicolon, question or exclamation mark; the next word starts a new caption.
- One position and one size everywhere. Two lines maximum, balanced.
- White with a thin dark glyph edge over footage; ink colour over paper. No background panel, no rotation, no bounce.
- Sentence case, proper names kept.
- Appear at the word's onset; end at the next caption's start or shortly after the last word.

## Paper diagrams

- Paper background with a 48px micro-grid, white 8px edge fading in over 72px. No major grid.
- Unfilled outlines, uniform 4px stroke, precise circles and rectangles. Hand-drawn variation only in arrows and annotations.
- Arrows: separate shaft and head, straight final 20px, head aligned to the shaft, wings on opposite sides, never crossing.
- Connectors never pass through or behind text or objects; they stop with clearance outside the target.
- Labels at least 33px on the 1080px canvas; handwritten annotations at least 38px.
- Centre the main group on the frame, then raise diagram stages enough to clear captions.
- Check routes during animation, not only at rest.

## Placement and safe zones

Keep essential content inside x 120 to 900 and y 290 to 1210 on the 1080×1920 canvas, including movement. The right rail, top and bottom third hold platform UI. Review with the overlay in `Short Form/exports/short-form-guides/` and never bake it into an export. Test at 360px wide. Verify the first real post in the target app; UI changes.

## Motion and effects

Straight cuts or simple fades. No neon, glow, shake or caption animation. Diagrams draw in over roughly half a second; nodes fade in over 0.18 s.

## Colour

Do not approve a grade from metadata or a thumbnail. Compare the preview frame against the exported frame in a colour-managed player. Browser renders are sRGB-coded; `npm run render` tags the H.264 stream and MP4 container to match. A grade measured on one shoot does not transfer to the next.

## Audio

Dialogue clear, music bed well under it (the starter default is 25 percent). The check reports unreadable or missing audio.

## Before export

`npm run check` ok, snapshots reviewed at phone size, safe zones confirmed, captions clear of diagrams, neck anchor stable across every cut.
