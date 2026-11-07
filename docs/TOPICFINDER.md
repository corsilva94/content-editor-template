# Optional: TopicFinder for ideas and scripts

TopicFinder is a paid service that finds outlier short-form videos in your niche and keeps a scripts board and inspiration library. It exposes an MCP server, so the same agent that edits your videos can also ask what to post. Most people using this template will not have it, and nothing in the pipeline depends on it.

## Where it fits

In front of everything. The brain holds your voice and facts, this repo turns footage into a finished reel, and TopicFinder answers the question before both: which video to make.

1. Browse outliers for your creator (free, no query) or search a topic (paid per search).
2. Pick one idea, write the script in your voice from the brain.
3. Save the idea and script to TopicFinder as the team's shared copy, and the script to `Short Form/content-brain/09-ideas-and-scripts/scripts/`.
4. Shoot, then edit here.

## Setup

```sh
claude mcp add --transport http --scope user topicfinder https://app.topicfinder.ai/mcp
```

Restart the session and run `/mcp`; TopicFinder opens a browser sign-in (standard OAuth, no key to paste). The server asks for three permissions: read discovery, write scripts, save items.

## Keeping the brain in charge

- Voice and facts stay in the brain. TopicFinder's own voice field can hold a summary, but the brain wins.
- TopicFinder's inspiration library has stats and transcripts, so it is the better home for saved reference videos. Point your brain's inspiration file at it instead of copying.
- Scripts marked Ready in TopicFinder get a copy in the brain's scripts folder with the date and a link, so the edit can find the plan.
- Searches with a query cost money. Browse the feed with filters first.
