# Explainer Studio

PDF / text / script → animated explainer video. Everything on screen is one of 39 deterministic motion assets (`studio/player/assets.js`); no stock images or AI clips. Each asset is a pure function of time, so frames render exactly and **the whole film re-times itself when the real narration is generated**.

```
source.pdf ──ingest (LLM)──► story.json ──validate──► build/ (schedule, captions, player)
                                  │                      │
                  tts (OpenAI) ───┴─ timings ─► build ─► render ─► video_silent.mp4 ─► mux (+ music, ducking) ─► final.mp4
```

## Configuration (.env)
Copy `.env.example` to `.env` in the same folder as `explainer.py` (that is the only place it is read; shell variables win). `OPENAI_TTS_MODEL`, `OPENAI_TTS_VOICE`, `OPENAI_TTS_SPEED`, `OPENAI_TTS_INSTRUCTIONS` configure narration; `STUDIO_LLM_PROVIDER` / `STUDIO_LLM_MODEL` the script step (provider is auto-detected from whichever API key is present). Precedence: command line > story.json `meta` (`voice`, `model`, `speed`, `instructions`) > .env > defaults, so one film can use its own voice while `.env` stays your global default. Other keys in the file (e.g. `OPENROUTER_IMAGE_MODEL`) are ignored.

Pacing: `meta.pre` (silence before a scene's first line, default 0.8 s), `meta.post` (after its last line, 1.8 s) and `meta.gap` (between lines, 0.55 s) set the silences; lower them for a snappier film.

## Quick start
```bash
pip install playwright numpy Pillow && playwright install chromium     # openai only for tts
python explainer.py ingest report.pdf -p projects/case --minutes 10     # needs ANTHROPIC_API_KEY (or --provider openai|openrouter --model ...)
python explainer.py validate -p projects/case --blanks                  # static checks + every cue run in a real browser
python explainer.py preview  -p projects/case                           # contact sheet: projects/case/build/preview/sheet.png
python explainer.py verify   -p projects/case                           # 2nd LLM pass: fact-check story against the source
python explainer.py all      -p projects/case                           # build → tts → re-time → music → render → mux  (OPENAI_API_KEY)
```
Without keys: `--provider mock` makes a rough offline draft; `all --skip-tts` renders with the estimated timing and a music bed.
Already have a script? `ingest script.txt --mode script` keeps your words and only designs the visuals.
No API at all? `python explainer.py prompt --mode doc` prints the full prompt; paste it plus your document into any Claude chat, save the JSON reply as `projects/case/story.json`. (Also in `prompts/`.)

## Examples
- `examples/hf-incident` — the 10-minute OpenAI / Hugging Face agent incident film (METR / Redwood report, Aug 2026), 9 scenes, 57 beats, 68 cues. Narration was fact-checked against the report; run `python explainer.py verify -p examples/hf-incident --source report.pdf` for a second, automated check.
- `examples/hf-incident-es` — the same film in Spanish (Spain accent, ~11 min). Agent quotes stay in English with Spanish labels. Shows how to localise a story: `meta.lang`, `meta.numsep` (thousands separator, `.` for es/de/it/pt), Spanish TTS `instructions` and a `pronunciation` table.
- `examples/hf-swarm-es` — second film (Spanish, ~8 min): the same incident told from Rob Wiblin's analysis plus the METR and OpenAI reports, with source cards at start and end and a closing scene on later incidents. Uses the new `breakout` (isolated agents → shared hub → wall → internet → third party), `hierarchy` (leader / managers / workers) and `flags` (capture-the-flag poles: real, forged, poisoned) assets.
- `examples/hf-rob-es` — third film (Spanish, ~11 min, female voice test): how AI models learn to dodge oversight, from the same Rob Wiblin source. New assets `monitor`, `selector`, `hoard`.
- `examples/mars-orbiter` — 3-minute demo written from general knowledge (verify before publishing).

## story.json
See `prompts/script_from_doc.md` (generated from `studio/catalog.py`, so it is always in sync). In short: scenes → `beats` (narration, ids auto: `3a`,`3b`…) and `cues` (`a` asset, `at`/`until` anchors, `p` props). Anchors: `"3c"` beat start · `">3c"` beat end · `"3c#word"` the moment a word is spoken · `S3`/`E3` scene bounds · `+1.5` offset. Because cues hang off words and beats, changing the narration or voice never breaks sync.

## Commands
`new · ingest · prompt · catalog · validate · build · preview · tts · music · render · mux · all · verify · mark`.
`mark logo.png` vectorises your logo into the glyph used in actor chips (`meta.mark = "mark.txt"` in story.json).
Project folders hold `story.json`, optional `mark.txt`, `source.txt`, `audio/`, `build/`.

## Add a new asset
1. `A.myasset=(host,props,C)=>{ …build DOM…; return t=>{ …update for local time t… } }` in `assets.js` (`C.T(x)` converts an anchor/number to seconds from cue start).
2. Describe it in `catalog.py` (kind, use, props, example). Validator and LLM prompt pick it up automatically.

## Limits
- Colours/fonts are fixed (dark theme); only the mark is themeable.
- 26 beats per scene max; asset layouts are tuned for full 16:9 frames (use `rect` presets sparingly).
- The LLM step can still misread a source — always run `verify` and skim the contact sheet.
- `examples/mars-orbiter` is a demo written from general knowledge, not from a supplied document — check it before publishing.

## Script

Every build (`build`, `validate`, `all`, or `python explainer.py script -p <project>`) writes `script.md` next to `story.json`: the voice-over, scene by scene, with beat ids.

## Cinematic camera (cue-level `cam` + `fx`)
Any cue can carry `cam`: keyframes `{at, x,y | to:<node id>, z (zoom), rx, ry, rot (tilt, deg), blur, dur}` interpolated with easing (anchors work as in `at`). `fx`: `{floor:<colour>, bloom:true, vig:true}` adds a lit floor, glow on strokes and a vignette. The `world` asset is a persistent diagram whose nodes the camera can fly to by id (`to:"hub"`). See `examples/cinematic-demo`.
