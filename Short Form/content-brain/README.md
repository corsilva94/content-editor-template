# Content brain

This folder is where **your** voice, facts, stories, beliefs and offer live. The editor and every AI agent working in this repo read from here before writing a hook, a caption or a script. Nothing about you is invented; if it is not in here, the agent asks.

The files in this folder are a **starter**: headings and prompts, no content. Pick one of three ways to make it yours.

## Option A: fill in the starter (fastest)

Open each numbered folder and answer the prompts in your own words. Start with `06-voice/voice.md` and `01-identity/identity.md`; the editor uses those first. Commit as you go. The whole thing is plain Markdown, so Obsidian, VS Code or Claude Code all work.

## Option B: mount your existing brain as a submodule (recommended if you already keep one)

If your brain is its own git repo, replace this folder with it so one copy serves every project:

```sh
git rm -r "Short Form/content-brain"
git submodule add <your-brain-repo-url> "Short Form/content-brain"
git commit -m "Mount my content brain"
```

Then check the paths in `work/brand-kit/brand.json` under `brain_sources` and in `CLAUDE.md`. If your brain nests its content under a subfolder (for example `20-content-brain/`), add that prefix to those paths. Collaborators clone with `--recurse-submodules`.

## Option C: copy an existing folder in

Copy your Markdown files into this folder, keep or rename the numbered folders, and update `AGENTS.md` here so the map matches your layout.

## The rules every brain follows

- **One home per fact.** A fact lives in exactly one file; other files point to it.
- **Never invent.** Gaps are marked `[missing]` and turned into questions for you.
- **Private stays private.** Anything under `private/` is ignored by git. Keep passwords and keys out of every file.
- **Content boundaries.** Write down what never gets mentioned, who stays unnamed, and family limits in `06-voice/voice.md` so agents respect them.

See `AGENTS.md` in this folder for which file to read for which task.
