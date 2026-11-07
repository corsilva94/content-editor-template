# Optional: hand off to Instagram Edits (macOS)

Instagram's Edits desktop app for macOS (released November 2026) exposes its editing tools over MCP, so an agent in this repo can open the finished render in Edits, apply captions, transitions or filters from Edits' catalogs, and leave you a project to finish and post by hand. This is optional. The pipeline here produces a complete reel without it.

## When it helps

- You want Edits' native caption styles, transitions or music on top of the finished cut.
- You post from Edits and want the project waiting there instead of importing by hand.
- You want a rough cut assembled in Edits from a raw clip while this repo handles the polished version.

What Edits cannot reproduce: the neck-anchored camera plan, the paper diagrams and the validated colour tag. Keep those here and hand off the rendered MP4.

## Setup

1. Install Edits for Mac and sign in.
2. In Edits settings, enable **MCP**. The app shows a local URL (`http://127.0.0.1:19501/mcp`) and a bearer token.
3. Register it with Claude Code at user scope so every project can use it. Paste your own token:

```sh
claude mcp add --transport http --scope user edits http://127.0.0.1:19501/mcp \
  --header "Authorization: Bearer <your-token-from-edits-settings>"
```

4. Restart the Claude Code session. `claude mcp list` should show the server connected while Edits is running.

Never commit the token. `.mcp.json.example` at the repo root shows the shape if you prefer a project-level config; copy it to `.mcp.json` only on your own machine (it is gitignored).

## What the server offers

The tool set follows the app's current screen.

- **Home:** list, open, create, rename, duplicate, delete, pin and favourite projects; import media; export or import a project as a `.mcomp` archive; inspect catalogs.
- **Catalogs (observed November 2026):** 51 transitions, 148 video effects, 77 filters, 16 LUTs, 77 text animations, 34 text presets, 39 caption styles, 380 fonts, 8 speed curves, 5 emphasis styles, 5 mask shapes. `getCapabilities` returns the conventions: time in seconds, canvas positions normalised 0 to 1 with origin top-left, colours as hex, rotation in degrees clockwise.
- **Editor (once a project is open):** add media and text, split clips, beat markers, apply filter, LUT, effect, transition, caption style, text animation, speed curve and mask; preview renders and frames.
- **Fallback:** tap, drag and keystroke tools for anything without a dedicated call.

## A first experiment

Ask the agent, with Edits open on the home screen:

> Create a new Edits project, import `Short Form/exports/<video>/<Title>.mp4`, apply a caption style from the catalog, and preview it. Do not post.

The agent should call `newProject`, `addMedia` with the file path, `listCaptionStyles`, `setCaptionStyle`, then `previewVideoStatus`. Review in Edits and finish by hand.

## Boundaries

- Posting stays manual. The system never publishes.
- Projects in Edits do not sync with the JSON sources here. Treat an Edits project as a derivative of a specific render.
- Mac only, and the app updates weekly; tool names may change. Re-run `getCapabilities` when something looks different.
