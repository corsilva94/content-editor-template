# Your first video, step by step

Goal: one talking-head clip in, one finished 1080×1920 reel out, with neck-anchored crops, timed captions and an optional paper diagram.

## 1. Prepare the clip

Export a single speaking cut from your camera footage at source resolution, 9:16 or wider, with the dialogue on its audio track. Trim long pauses in your editor of choice before you bring it here, or leave them and cut by transcript in step 3. The system treats this file as the original: it never re-encodes it, and a different clip means a new video folder.

```sh
npm run new -- my-first-video "My First Video"
cp /path/to/clip.mp4 "Short Form/work/my-first-video/composition/assets/media/footage.mp4"
```

A music bed is optional. Put it next to the footage and name it in `edit.json` as `"music": "assets/media/bed.wav"`, with `music_volume` around 0.25.

## 2. Get word timings

```sh
npm run transcribe -- "Short Form/work/my-first-video/composition/assets/media/footage.mp4"
```

This writes `transcript.json` next to `edit.json` with `{ text, words: [{text, start, end}] }`. It prefers Parakeet when installed and falls back to whisper.cpp through the HyperFrames CLI; the first run may download a model. If neither is available, any word-level transcript in that shape works.

## 3. Write edit.json

`edit.json` is the edit decision list. An agent can do this from the transcript if you tell it which sentences to keep.

- `cuts`: the takes you keep, in order. `start` and `duration` are on the finished timeline. `source_in` and `source_out` record where they came from. With a single pre-trimmed clip, one cut covering the whole file is fine.
- `words`: every spoken word with `start`, `end` (composition seconds) and the `cut` it belongs to. Copy from the transcript, shifting times if cuts reorder the source.
- `paper_cuts`: the cut ids that play over a paper diagram instead of footage.
- `emphasis`: optional list of words to colour with the accent.
- `duration`: total length.

Captions are generated from `words`, so they always match what was said.

## 4. Set the camera plan

Open one frame of the clip at source resolution. Find the pixel where the collar meets the base of the neck. Put it in `camera-plan.json` as `source_anchor`. Leave `screen_anchor` at `540, 820` unless your framing needs the eyes higher or lower. Save that frame as `qa/neck-reference.jpg` so the next edit of this setup uses the same point.

Then list the cuts: `time` and `scale` only. A wide shot is `1.0` (or whatever fills the frame), a punch-in is 1.2 to 1.25 times that. Identical scales produce identical crops, which is what makes cut-ins feel locked.

## 5. Diagrams (optional)

`graphics.py` returns a list of scenes drawn on paper over the `paper_cuts`. The starter draws a centre person with three connections. Replace it with yours: SVG in 1080×1920 coordinates, strokes with class `outline`, and timeline calls `draw`, `arrow`, `show` timed to the words in `edit.json`. Rules: `../Short Form/notes/paper-grid-format.json`. Keep everything inside the safe rectangle in `short-form-safe-zones.json`, including entrance movement.

## 6. Build, check, look

```sh
npm run build
npm run check
npm run preview      # http://localhost:3002
npm run snapshot     # six frames across the video
```

`check` must say ok. Look at the snapshots at phone width. Confirm captions never cover the diagram, the neck stays put across punch-ins, and nothing essential sits in the platform UI zones.

## 7. Render

```sh
npm run render
```

Output: `Short Form/exports/my-first-video/My First Video.mp4`. The command renders lossless PNG frames, encodes, then tags the file as sRGB so colour-managed players show what the preview showed. Play the export in the real app you will post from before publishing; see `../Short Form/notes/colour-workflow.json` for why metadata alone is not proof.

## 8. Next video

`npm run new -- next-slug "Next Title"` copies the starter and makes it active. `npm run use -- <slug>` switches between videos.
