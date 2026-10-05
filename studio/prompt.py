"""Builds the LLM prompts from the asset catalog (so prompt, validator and player can never drift apart)."""
import json, os
from .catalog import ASSETS, COLORS, SEG

STRUCTURE = """\
## Story structure (the arc every film follows)

| # | Scene | Job | Share of runtime |
|---|-------|-----|------------------|
| 0 | Cold open | The hook: the stake, one striking number or image, then a title card. Never start with background. | 5-7 % |
| 1 | The setup | Who/what is involved, in plain words. Only what the viewer needs for scene 2. | 10-12 % |
| 2 | The mechanism | How the system/process normally works. One mental model, built visually. | 10-12 % |
| 3 | The turn | What changed, went wrong or was discovered. The first moment the viewer leans in. | 10-12 % |
| 4 | Escalation | How it grew: scale, speed, repetition. Numbers and timelines. | 10-12 % |
| 5 | The peak | The single most important event or finding, told slowly with the strongest visuals. | 15-18 % |
| 6 | Why it happened | Causes, evidence, quotes, the counter-argument. Say what the source does NOT establish. | 12-15 % |
| 7 | What it means | Consequences, limits, open questions. | 6-8 % |
| 8 | Takeaways | 3 takeaways + source card. End on the sharpest sentence, not a summary of everything. | 5-6 % |

Fewer scenes for shorter films (3 min: scenes 0,1,3,5,8 → 5-6 scenes; 5 min: 7 scenes; 10 min: 9 scenes). Merge, don't skip the hook, the peak, or the takeaways."""

RULES = """\
## Narration rules
- Spoken English for the ear: short sentences, active voice, no parentheses, no abbreviations the narrator cannot say. Spell out numbers the way they are spoken ("three hundred twenty-seven million dollars").
- ~2.45 words per second. A beat (one list item in `beats`) is 12-40 words = one idea = one breath group. Never more than 55 words.
- Open every scene with a sentence that tells the viewer where we are in the story. Define jargon the first time it appears.
- FIDELITY: use only facts, numbers, names and quotations that are in the source. Never make a claim stronger than the source (if it says "likely", say "likely"; if it does not say who/why, do not guess). Put what the source cannot show in scene 6/7 explicitly.
- Quote cards: verbatim only; label paraphrases as paraphrases (`kind: "par"`).

## Visual rules
- Every scene needs full-frame ("stage") cues that cover the scene from `S<n>` to `E<n>` with no gap longer than a second; change the main visual roughly every 12-25 s (1-4 stage cues per scene). Chain cues: `until` of one = `at` of the next, e.g. `{"at":"3a","until":">3b"}` then `{"at":">3b","until":"E3"}`.
- Overlay assets (lower, stamp, note, source, counters with pos top/bottom) sit on top of a stage cue; they need their own `at`/`until` inside that span.
- Vary the assets: do not use the same asset twice in a row; use at least 6 different assets in a 9-scene film. Pick the asset by what the sentence does (see "use" below), not by taste.
- Keep on-screen text short: titles ≤ 28 chars, labels ≤ 40 chars, chip names ≤ 24 chars, list items ≤ 60 chars. The viewer is listening; the screen is a diagram, not a transcript.
- Sync to speech with word anchors: `"at": "3c#thousands"` makes the visual appear exactly when "thousands" is spoken. Use a WORD THAT EXISTS in that beat (whole word, case-insensitive; the first occurrence is used; `_` stands for a space). Times inside `p` are seconds from the cue start, or anchors.
- Numbers on screen must equal numbers in the narration and in the source.
- Colours: blue = neutral/system, teal = good/agent/normal, amber = caution/changed, red = failure/harm, muted = background. In text segments also `plain`."""

FORMAT = """\
## Output format (story.json) — return ONLY this JSON object, no commentary, no code fences
```
{
 "meta": {"title": "...", "lang": "en", "minutes": 10},
 "pronunciation": {"written form": "how the narrator should say it"},     // only things a TTS would mispronounce
 "scenes": [
  { "title": "Cold open",
    "target": 35,                                  // optional seconds; otherwise derived from meta.minutes
    "intensity": 0.3,                              // optional 0-1 music energy
    "evidence": ["p.3: 'quoted or paraphrased source line'"],   // where each fact comes from (used by the fact-check pass)
    "beats": ["Narration sentence(s) for beat 0a.", "Beat 0b ..."],   // ids are automatic: scene 3 -> 3a, 3b, 3c ...
    "cues": [
      {"a": "title", "at": "S0", "until": ">0a", "p": {"title": "..."}},
      {"a": "counters", "at": "0a#million", "until": "E0", "p": {"items": [...]}, "rect": "full"}
    ] } ] }
```
Cue fields: `a` asset · `at` start anchor · `until` end anchor OR `dur` seconds · `p` props · optional `rect` ("full" default, "top", "bottom", "left", "right" or [left,top,width,height] in %) · `bg` (default true for stage assets) · `fade` [in,out] seconds · `off` seconds offset.
Anchors: `"2c"` start of beat 2c · `">2c"` end of beat 2c · `"2c#word"` the moment "word" is spoken · `"S2"`/`"E2"` scene start/end · add `+1.5`/`-0.5` to shift."""


def catalog_md():
    out = ['## Asset catalog (the ONLY assets you may use)', f'Colours: {", ".join(COLORS)}. Text-segment colours: {", ".join(SEG)}.']
    for k, a in ASSETS.items():
        out.append(f'\n### `{k}` — {a["kind"]}\n{a["use"]}  \nRequired: {", ".join(a.get("required", [])) or "none"}  \nProps: ' + '; '.join(f'`{p}` {d}' for p, d in a['props'].items()))
        out.append('Example: `' + json.dumps({"a": k, "p": a["example"]}, ensure_ascii=False) + '`')
    return '\n'.join(out)


def system_prompt(mode='doc', example=None):
    head = {
     'doc': "You turn a source document into a documentary-style explainer video script with a storyboard, as a single story.json. Adapt, don't copy: choose the 6-12 ideas that carry the story, reorder them into the arc below, and write narration for listening.",
     'script': "You receive a finished narration script. KEEP ITS WORDS (only split it into beats of 12-40 words, fix obvious typos, never add facts). Your job is the storyboard: group beats into scenes following the arc below where it fits, and design the visual cues for every beat as a single story.json."}[mode]
    ex = ''
    if example:
        ex = '\n\n## Worked example (excerpt of a finished story.json)\n```\n' + example.strip() + '\n```'
    return f'{head}\n\n{STRUCTURE}\n\n{RULES}\n\n{FORMAT}\n\n{catalog_md()}{ex}\n'


def user_prompt(text, minutes=None, title=None, audience=None, notes=None, lang='en'):
    p = [f'Target length: {minutes or 10} minutes (≈ {int((minutes or 10) * 60 * 2.2)} spoken words in total). Language: {lang}.']
    if title: p.append(f'Working title: {title}')
    if audience: p.append(f'Audience: {audience}')
    if notes: p.append(f'Extra instructions: {notes}')
    p.append('SOURCE (between the markers):\n<<<SOURCE\n' + text + '\nSOURCE>>>')
    p.append('Return only the story.json object.')
    return '\n\n'.join(p)


VERIFY = """You are a meticulous fact-checker. You get a SOURCE and a video STORY (narration beats and on-screen text). For every beat and every number/name/quote on screen, decide whether the source supports it.
Report only problems, as JSON: {"issues":[{"where":"3c" or "scene 4 cue 2","claim":"...","problem":"unsupported|stronger-than-source|wrong-number|misquote|missing-caveat","source_says":"short quote or 'not in source'","fix":"suggested replacement text"}], "verdict":"pass|fix"}.
Be strict about numbers, causes ('because'), certainty words and who did what. Do not nitpick style. Return only JSON."""


def verify_prompt(source, story):
    rows = []
    for sc in story['scenes']:
        rows.append(f'## Scene {sc["n"]}: {sc.get("title","")}')
        for b in sc['beats']: rows.append(f'{b["id"]}: {b["text"]}')
        for i, c in enumerate(sc.get('cues', [])):
            rows.append(f'cue {i} [{c["a"]}] on-screen: ' + json.dumps(c['p'], ensure_ascii=False)[:600])
    return f'SOURCE:\n<<<\n{source}\n>>>\n\nSTORY:\n' + '\n'.join(rows)
