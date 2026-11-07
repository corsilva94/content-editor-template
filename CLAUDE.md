# Content editor — agent instructions

This repository is one creator's short-form editing system built on HyperFrames. Read `project.json` first: it names the active job folder and video.

- Run the root npm commands (`build`, `check`, `preview`, `snapshot`, `render`); they set the working directory. Do not run `hyperframes` by hand unless a command does not cover the task.
- Read `<job>/work/brand-kit/brand.json` and `<job>/notes/BRAND.md` before styling anything. Colour and type values live only in `brand.json`; never duplicate them in instructions.
- Framing rule: one stable base-of-neck anchor, horizontally centred, scale only. No head, eye or hand following, no re-centring at pause trims. The anchor lives in `<job>/work/<video>/camera-plan.json`.
- Captions are the spoken words from `edit.json`, grouped at punctuation, one position and size. Never substitute script text for what was said.
- Load the creator's voice and facts from `<job>/content-brain/AGENTS.md` and the files it points to. Do not invent facts; mark gaps `[missing]` and ask. If the brain is a git submodule, commit brain changes inside it.
- Diagrams follow `<job>/notes/paper-grid-format.json`; placement follows `<job>/notes/short-form-safe-zones.json`; colour validation follows `<job>/notes/colour-workflow.json`.
- Shared skills are in `Misc/` (HyperFrames authoring, CLI, registry, media-use). Optional services mentioned inside them are not installed unless `npm run doctor` or `claude mcp list` says so.
- Keep generated HTML out of hand edits: change `edit.json`, `camera-plan.json`, `graphics.py`, `build.py` or the brand kit, then `npm run build`.
- Save new work under `<job>/inbox`, `work`, `exports` or `notes`. Keep source originals intact; start a new video folder for different footage (`npm run new`).
- Never commit credentials, `.env`, anything under `private/`, media caches, or another person's material.
- Preview, check and snapshot before exporting. `npm run render` applies the sRGB transfer tag the browser capture needs; do not skip it.
- No publishing, posting or pushing to main without explicit authorization. Experiment on a branch.
- Instagram Edits and TopicFinder integrations are optional (`docs/EDITS-APP.md`, `docs/TOPICFINDER.md`). Only use them when their MCP servers are connected in this session.
