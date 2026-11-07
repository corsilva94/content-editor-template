# Brand and editing direction

Visual settings live in `work/brand-kit/brand.json`. This page explains how they are applied; it never repeats the values.

## Source of truth

- Colours, type weights, caption geometry, camera rule: `work/brand-kit/brand.json`.
- Reusable CSS classes and bundled Inter: `work/brand-kit/brand.css` (stage into a hand-built composition with `work/brand-kit/stage.py`). The starter `build.py` reads `brand.json` directly and needs no staging.
- Voice and facts: `content-brain/` (see its `AGENTS.md`).

## Application

- Hook weight for titles, caption weight for spoken captions, body weight for supporting copy.
- Paper-white text over footage, accent colour for sparing emphasis, ink colour over paper panels. Keep the brand family for emphasis; no automatic substitutions.
- Sentence case, proper names kept, legible at phone size. Measure text with the brand font, not a stand-in.
- Captions in one lower position and one size across footage and diagram scenes, text only.
- Straight cuts or simple fades, natural skin colour. No neon, heavy grade, caption rotation or music carried over from another creator's look.

## Reviews before export

- `notes/short-form-safe-zones.json` for placement, with the overlay in `exports/short-form-guides/`.
- `notes/paper-grid-format.json` for diagram drawing and connector clearance.
- `notes/colour-workflow.json` for grade validation.
- Snapshots at phone width, every cut checked for a stable neck anchor.

## Keeping a record

When a direction changes, add a dated section below with what changed and why, and update `brand.json` in the same commit. Earlier sections stay as history.

## Direction log

- *(date)* Template defaults adopted. Replace with your own first decision.
