# Content editor template

A short-form video editing system you run from the terminal with an AI agent beside you. You bring a talking-head clip and your own content brain. The system gives you neck-anchored crops, punctuation-timed captions, drawn paper diagrams, a verified colour export and an agent that already knows the rules.

It is HTML, Python and [HyperFrames](https://github.com/heygen-com/hyperframes), not a Premiere or Resolve timeline. Every frame is generated from a few JSON and Python files, so edits are reviewable, repeatable and diffable.

**Use this template:** click "Use this template" on GitHub, clone your copy, then follow the steps below. Full docs are in `docs/`.

## What you get

- **`scripts/editor.mjs`** one entry point: setup, build, preview, check, snapshot, render, transcribe.
- **`Short Form/work/starter/`** a working example video. `edit.json` (cuts and word timings), `camera-plan.json` (one neck anchor, scale only), `graphics.py` (paper diagrams), `build.py` (turns them into the composition).
- **`Short Form/work/brand-kit/`** your palette, type and caption rules in one `brand.json`, plus bundled Inter.
- **`Short Form/content-brain/`** a starter brain with prompts. Fill it in or mount your own as a submodule. See `docs/CONTENT-BRAIN.md`.
- **`Short Form/notes/`** the editing rules: safe zones, paper-grid diagram rules, colour validation.
- **`Misc/`** the HyperFrames authoring, CLI, registry and media skills your agent reads.
- **`docs/EDITS-APP.md`** optional hand-off to Instagram's Edits desktop app over MCP. **`docs/TOPICFINDER.md`** optional idea discovery. Neither is required.

## Setup (macOS, tested)

Prerequisites: Node.js 22+, Python 3.12+, FFmpeg with ffprobe, GitHub CLI.

```sh
brew install node python@3.13 ffmpeg gh
gh repo clone <you>/<your-copy> -- --recurse-submodules
cd <your-copy>
npm ci
PYTHON=/opt/homebrew/bin/python3.13 npm run setup
npm run doctor
```

Other operating systems have not been verified. Windows users need the same tools on PATH.

## Your first video

```sh
npm run new -- my-first-video "My First Video"
# put your prepared 1080x1920 clip at:
#   Short Form/work/my-first-video/composition/assets/media/footage.mp4
npm run transcribe -- "Short Form/work/my-first-video/composition/assets/media/footage.mp4"
# fill in edit.json (cuts + words) and camera-plan.json (neck anchor), see docs/FIRST-VIDEO.md
npm run build && npm run check && npm run preview
```

Open the preview URL (normally `http://localhost:3002`). When it looks right:

```sh
npm run snapshot    # frames at 0, 10, 30, 50, 70, 90 percent, look at them at phone size
npm run render      # Short Form/exports/<video>/<Title>.mp4, 1080x1920, 23.976 fps, sRGB-tagged
```

## Where things are decided

| What to change | File |
| --- | --- |
| Palette, type, caption position and size, camera rule | `Short Form/work/brand-kit/brand.json` |
| Which takes, in what order, which words, which cuts play on paper | `Short Form/work/<video>/edit.json` |
| Crop sizes and the neck anchor | `Short Form/work/<video>/camera-plan.json` |
| Diagram content and animation timing | `Short Form/work/<video>/graphics.py` |
| Caption grouping and layout logic | `Short Form/work/<video>/build.py` |
| An optional grade | `Short Form/work/<video>/color/selected-payload.json` |
| Your voice, stories, beliefs, offer | `Short Form/content-brain/` |
| Which video the npm commands act on | `project.json` (or `npm run use -- <video>`) |

## The rules in one paragraph

Anchor every crop to one stable base-of-neck point, centred horizontally, and only change scale between cuts. Never follow eyes, head or hands. Captions show the words actually spoken, end at punctuation, keep one position and size, and switch from white on footage to ink on paper. Diagrams sit on a paper micro-grid with unfilled outlines, uniform strokes and connectors that never cross text. Keep essential content inside the platform-safe rectangle. Validate colour in a colour-managed player, not from metadata. Details: `docs/EDITING-RULES.md`.

## Sharing media with collaborators

Video, audio and zip files are gitignored. To share prepared clips, zip them, publish the zip as a GitHub release on your copy, and fill in `media-manifest.json`. `npm run download:media` then fetches and checksum-verifies the files for everyone else.

## Licences

HyperFrames (Apache-2.0), GSAP (its standard licence), Inter and Caveat (SIL OFL). See `THIRD_PARTY.md`. Your footage, brain and brand remain yours; this template claims nothing over them.
