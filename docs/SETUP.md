# Setup

Tested on macOS (Apple silicon). The tools are cross-platform, but other systems have not been verified.

## Tools

| Tool | Why | macOS install |
| --- | --- | --- |
| Node.js 22+ | runs HyperFrames and the npm commands | `brew install node` |
| Python 3.12+ | builds compositions, measures caption widths | `brew install python@3.13` |
| FFmpeg with ffprobe | reads audio, encodes and tags the export | `brew install ffmpeg` |
| GitHub CLI | cloning, optional media release download | `brew install gh` then `gh auth login` |
| Claude Code (or another agent that reads CLAUDE.md) | the editing partner | see claude.com/claude-code |

macOS ships Python 3.9, which is too old. Point setup at the Homebrew one:

```sh
PYTHON=/opt/homebrew/bin/python3.13 npm run setup
```

## Install

```sh
gh repo clone <you>/<your-copy> -- --recurse-submodules
cd <your-copy>
npm ci
PYTHON=/opt/homebrew/bin/python3.13 npm run setup
npm run doctor
```

`doctor` prints the Python, FFmpeg and HyperFrames versions, the active video, whether its footage is in place and whether the Python tools are ready.

## Optional

- **Transcription:** `npm run transcribe` prefers Parakeet (`npx hyperframes models install parakeet`) and falls back to whisper.cpp, which the HyperFrames CLI fetches on first use.
- **Instagram Edits hand-off:** `EDITS-APP.md`.
- **TopicFinder:** `TOPICFINDER.md`.
- **HeyGen sign-in** for the media-use skill's music and asset catalogs: `npx hyperframes auth login`. Not needed for the core pipeline.

## Files git ignores

Video, audio and zip files, `node_modules`, `.venv`, `.hyperframes` caches, `.downloads`, `.env*`, `private/` folders, `.mcp.json`. Share media through a release (see README) rather than committing it.

## Agent setup

Open the repo in Claude Code. `CLAUDE.md` at the root and in `Short Form/` carry the rules; `Misc/` holds the HyperFrames skills. Nothing else to configure.
