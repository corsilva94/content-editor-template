# Plugging in your content brain

The editor never guesses who you are. Hooks, captions, diagram labels and scripts all start from the files in `Short Form/content-brain/`. This page is how to make that folder yours.

## What a brain is

A folder of plain Markdown, one fact per file, that an AI reads before writing anything in your name. The minimum that makes the editor useful:

| File | What the editor uses it for |
| --- | --- |
| `06-voice/voice.md` | register, banned phrases, caption style, content boundaries |
| `01-identity/identity.md` | who is speaking, so hooks and diagrams say "you" correctly |
| `03-stories/story-bank.md` | proof and illustrations for diagrams |
| `04-beliefs/beliefs-and-hot-takes.md` | the point a video makes |
| `02-audience/customer.md` | the viewer the caption and hook address |
| `05-offer/offers.md` | the call to action |

The starter ships these files with prompts and `[missing]` markers.

## Three ways to plug yours in

**A. Fill in the starter.** Open the files, answer the prompts in your own words, commit. Start with voice and identity. Ten focused minutes gives the editor enough to work with; you can keep adding.

**B. Mount your own repo as a submodule.** If you already keep a brain (an Obsidian vault, a notes repo), make it the single source for every project:

```sh
git rm -r "Short Form/content-brain"
git submodule add <your-brain-repo-url> "Short Form/content-brain"
git commit -m "Mount my content brain"
```

Then fix two things if your brain nests content under a subfolder such as `20-content-brain/`: the `brain_sources` paths in `Short Form/work/brand-kit/brand.json`, and the content-brain line in `CLAUDE.md`. Collaborators clone with `--recurse-submodules`. Edits to the brain are committed inside the submodule and pushed to its own repo; this repo only records which commit it points at.

**C. Copy files in.** Drop your Markdown into the folder and update the folder's `AGENTS.md` map so an agent can find voice, stories and beliefs by name.

## Rules that keep a brain trustworthy

- **One home per fact.** When a number changes, it changes in one file. Other files link to it.
- **Never invent.** An agent that cannot find a fact writes `[missing]` and asks you. Agents may save your answer into the right file when you say yes.
- **Spoken words win.** Captions in an edit are what you said on camera, not the script. The script is the plan; the footage is the truth.
- **Private stays out of git.** `private/` folders are ignored. Keep passwords, keys and anything you would not want on GitHub out of every file.
- **Write the boundaries down.** Names you never say, family limits, clients under NDA. Put them in `06-voice/voice.md` so every agent respects them.

## How agents use it in this repo

`CLAUDE.md` tells the agent to read `Short Form/content-brain/AGENTS.md` before any voice or content work. That file maps tasks to files. Keep the map current when you add folders.

## Optional: TopicFinder

If you use TopicFinder, its scripts board and inspiration library overlap with `09-ideas-and-scripts/` and a saved-videos folder. The brain stays the source of truth for voice and facts; TopicFinder holds discovery and the team's shared script copies. See `TOPICFINDER.md`. Most people will not have it, and nothing here depends on it.
