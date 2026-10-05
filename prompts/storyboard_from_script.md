You receive a finished narration script. KEEP ITS WORDS (only split it into beats of 12-40 words, fix obvious typos, never add facts). Your job is the storyboard: group beats into scenes following the arc below where it fits, and design the visual cues for every beat as a single story.json.

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

Fewer scenes for shorter films (3 min: scenes 0,1,3,5,8 → 5-6 scenes; 5 min: 7 scenes; 10 min: 9 scenes). Merge, don't skip the hook, the peak, or the takeaways.

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
- Colours: blue = neutral/system, teal = good/agent/normal, amber = caution/changed, red = failure/harm, muted = background. In text segments also `plain`.

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
Anchors: `"2c"` start of beat 2c · `">2c"` end of beat 2c · `"2c#word"` the moment "word" is spoken · `"S2"`/`"E2"` scene start/end · add `+1.5`/`-0.5` to shift.

## Asset catalog (the ONLY assets you may use)
Colours: blue, teal, amber, red, muted. Text-segment colours: blue, teal, amber, plain, muted, red.

### `title` — stage
Opening / closing title card.  
Required: title  
Props: `kicker` small label above; `title` big text, \n allowed; `sub` subtitle; `src` list of source lines (small, bottom); `at` when it appears
Example: `{"a": "title", "p": {"kicker": "CASE STUDY", "title": "The unit mismatch\\nthat sank a probe", "sub": "Mars Climate Orbiter, 1999"}}`

### `feed` — stage
A live stream of short coloured lines (messages, logs, events). Gives 'a lot is happening' texture; real lines can be pinned.  
Required: none  
Props: `lines` list of lines; each line = list of [colour,text] segments (real, pinned lines come first); `filler` false | {prefix,verbs,words,names,mode} generated filler lines; `vis` visible lines (default 9); `key` legend [[colour,label],...] or false; `typed` {at,cps} types line 0 first; `zoom` {from,at,dur} zoom-out reveal; `rate` [[time,lines_per_sec],...]; `first` time of first line; `last` segments of a special final line; `lastAt` when the special line lands; `hl` indices to outline; `dim` opacity of the stream
Example: `{"a": "feed", "p": {"lines": [[["blue", "TELEMETRY"], ["plain", " trajectory_update "], ["teal", "ground"]]], "filler": false, "vis": 6}}`

### `annotated` — stage
One exploded message/string with each part labelled in turn (anatomy of a record).  
Required: msgs  
Props: `heading` small label; `msgs` list of messages; message = list of [kind,text]; `kinds` {kind:{label,color}} (defaults: type,sender,recipient,content,reply); `order` kinds in the order they are explained; `steps` times at which each kind in `order` is highlighted; `end` time all parts light up again; `tags` list of small tag boxes; `tagsAt` when tags appear; `at` when cards appear
Example: `{"a": "annotated", "p": {"heading": "A thruster report", "kinds": {"unit": {"label": "unit", "color": "amber"}, "val": {"label": "value", "color": "teal"}}, "order": ["val", "unit"], "msgs": [[["val", "Impulse: 4.45 "], ["unit", "lbf·s"]]], "steps": [2, 4], "end": 6}}`

### `chips` — stage
Entities as pills carrying the theme mark (actors, agents, systems, teams), grouped in labelled rows.  
Required: rows  
Props: `rows` [[label,colour,[names],flag]] — flag=true/'text' draws a red flagged badge; `big` larger pills; `stag` stagger secs; `at` start; `style` css for container
Example: `{"a": "chips", "p": {"rows": [["Ground team", "blue", ["Navigation", "Flight dynamics"]], ["Vendor", "amber", ["Lockheed software"]]]}}`

### `network` — stage
A graph of nodes joining one by one with a counter ('N units').  
Required: none  
Props: `at` start; `dur` growth seconds; `to` end count (max 90); `unit` counter noun; `packets` false to hide moving packets; `from` start count
Example: `{"a": "network", "p": {"at": 0.5, "dur": 8, "to": 60, "unit": "agents"}}`

### `population` — stage
Grid of many units, a share flagged/changed, optionally all feeding one shared resource (a 'tap').  
Required: none  
Props: `label` top label; `flaggedShare` 0-1; `appear` when grid appears; `walls` when cells flash (isolation); `flag` when flagged cells turn red; `flagLegend` legend after flagging; `tap` label of the shared resource bar; `tapAt` when it appears; `packets` when dots start flowing to the resource
Example: `{"a": "population", "p": {"label": "70 independent sandboxes", "appear": 0.5, "flag": 6, "flagLegend": "flagged", "tap": "shared package registry", "tapAt": 9, "packets": 11}}`

### `listing` — stage
Left panel where a name/path is typed (file tree, command, URL) + optional right panel with a list.  
Required: none  
Props: `title` panel title; `root` root line; `rows` [[colour,text]]; `typed` text to type; `typeAt` when typing starts; `cps` chars/sec; `call` callout after typing; `kids` child lines; `kidsAt` when they appear; `foot` footer line; `footAt` when; `right` {title,at,lines:[[colour,text]],call}
Example: `{"a": "listing", "p": {"title": "/reports/", "root": "reports/", "rows": [["muted", "q1.csv"]], "typed": "q2_final.csv", "typeAt": 1, "call": "new file"}}`

### `counters` — stage
Big animated numbers. Use pos='top'/'bottom' to make it an overlay on another stage.  
Required: items  
Props: `items` [{label,n,from,pre,suf,txt,at,dur,color}] n=target number; txt overrides the number with fixed text; `pos` center|top|bottom; `small` smaller digits
Example: `{"a": "counters", "p": {"items": [{"label": "mission cost (USD millions)", "n": 327, "pre": "$", "at": 0.5}, {"label": "years of cruise", "n": 9, "at": 1.5}]}}`

### `timeline` — stage
Dated events on an axis (up/down stems).  
Required: ev  
Props: `axis` {labels:[...],hours:N per label} (default 6 days × 24h); `ev` [{h,date,label,pos(+up/-down px),color,at}] h = position in axis hours; `vb` svg viewBox crop; `axisY` axis y (default 270); `at` axis draws
Example: `{"a": "timeline", "p": {"axis": {"labels": ["1998", "1999 Jan", "1999 Sep"], "hours": 24}, "ev": [{"h": 4, "date": "Dec 1998", "label": "Launch", "pos": 90, "color": "blue", "at": 1}, {"h": 60, "date": "Sep 23", "label": "Orbit insertion", "pos": -90, "color": "red", "at": 3}]}}`

### `equation` — stage
Boxes joined by arrows/operators lit in sequence (a formula, a causal chain), plus evidence rows below.  
Required: boxes  
Props: `boxes` list of strings; `seps` operators between boxes (default →); `hl` when lighting starts; `step` secs between boxes; `caption` line under the chain; `captionAt` when; `rows` [{chip:[name,colour,flag?],text,box,mono,at}]
Example: `{"a": "equation", "p": {"boxes": ["Thruster firing", "× impulse (lbf·s)", "= trajectory error"], "hl": 1, "step": 1.2}}`

### `contrast` — stage
What was believed vs what actually happened: two rows of step boxes, strike-through and ghost steps.  
Required: top, bottom  
Props: `top` {label,steps:[{text,kind(ok|dashed|'')}],at}; `bottom` same; `note` {chip:[name,colour],text,at}; `punch` {text,at}; `strike` {step,at} strikes a step of top; `ghost` {step,at} reveals a step of bottom
Example: `{"a": "contrast", "p": {"top": {"label": "What the spec said", "at": 0.5, "steps": [{"text": "Metric units"}, {"text": "Newton-seconds"}]}, "bottom": {"label": "What the software did", "at": 3, "steps": [{"text": "Metric units"}, {"text": "Pound-force seconds", "kind": "dashed"}]}, "strike": {"step": 1, "at": 5}}}`

### `options` — stage
One hub branching to 2-4 alternatives/approaches, each a card with lines and marks.  
Required: hub, items  
Props: `hub` {name,sub,color}; `items` [{title,lines:[...],marks:[[text,colour],...]}]; `at` list of start times per item
Example: `{"a": "options", "p": {"hub": {"name": "The team", "sub": "had three options", "color": "blue"}, "items": [{"title": "Burn now", "lines": ["risky"], "marks": [["fast", "amber"]]}, {"title": "Wait", "lines": ["safe"], "marks": [["slow", "teal"]]}], "at": [1, 2.5]}}`

### `pipeline` — stage
Three stages in a row (A → B → C) with a trigger on the middle one and a packet flowing on.  
Required: nodes  
Props: `nodes` exactly 3 × {title,sub}; `at` start; `trigger` {label,at}; `packet` {label,at}
Example: `{"a": "pipeline", "p": {"nodes": [{"title": "Sensor", "sub": "raw data"}, {"title": "Converter", "sub": "wrong units"}, {"title": "Navigation", "sub": "uses result"}], "trigger": {"label": "bug", "at": 3}, "packet": {"label": "bad value", "at": 5}}}`

### `cards` — stage
A row of labelled cards (options, votes, roles) + optional highlighted banner.  
Required: none  
Props: `items` [{title,sub,code,color}]; `at` start; `stag` stagger; `banner` {text,tag,at}
Example: `{"a": "cards", "p": {"items": [{"title": "Review A", "sub": "approved", "code": "OK", "color": "teal"}, {"title": "Review B", "sub": "skipped", "code": "—", "color": "amber"}], "banner": {"text": "Nobody checked the units", "tag": "gap", "at": 3}}}`

### `terminal` — stage
A terminal window: a command is typed, then a result appears.  
Required: none  
Props: `cmd` command text; `cps` typing speed; `struck` struck-through line; `result` bold result; `note` small note; `at` typing start; `out` when output appears
Example: `{"a": "terminal", "p": {"cmd": "convert --from lbf_s --to N_s 4.45", "result": "19.8 N·s", "note": "never run in flight software", "at": 0.5}}`

### `bars` — stage
Horizontal bars to compare shares/amounts.  
Required: items  
Props: `items` [{label,val(text),w(0-100),color,at,from,dur}]; `gap` spacing; `style` css
Example: `{"a": "bars", "p": {"items": [{"label": "Predicted", "val": "1×", "w": 20, "color": "teal", "at": 0.5}, {"label": "Actual", "val": "4.45×", "w": 90, "color": "red", "at": 1.5}]}}`

### `steps` — stage
Staircase of escalating levels/stages.  
Required: rows  
Props: `rows` [{title,desc,when,color}]; `at` start; `step` secs between; `foot` mono footer
Example: `{"a": "steps", "p": {"rows": [{"title": "Level 1", "desc": "noticed", "when": "day 1", "color": "blue"}, {"title": "Level 2", "desc": "ignored", "when": "day 30", "color": "red"}]}}`

### `groups` — stage
Leaders assigning work to columns of dots (parallel workers split into groups).  
Required: groups  
Props: `leads` [[name,colour]]; `leadText` caption beside leads; `groups` [{title,color,n}]; `at` start
Example: `{"a": "groups", "p": {"leads": [["Lead", "blue"]], "leadText": "splits the work", "groups": [{"title": "Team A", "color": "teal", "n": 10}, {"title": "Team B", "color": "amber", "n": 14}]}}`

### `quote` — stage
Quote cards (verbatim quotes, paraphrases, agent/person statements).  
Required: cards  
Props: `cards` [{text,kind(quote|raw|par|agent),who:[name,colour],label,at}]; `big` larger text; `sm` smaller; `pos` top|bottom; `cols` columns
Example: `{"a": "quote", "p": {"cards": [{"text": "We assumed the numbers were metric.", "kind": "quote", "at": 0.5, "label": "Engineer, board hearing"}]}}`

### `messages` — stage
Stacked message cards (emails, chat, log entries) with sender → recipient and coloured segments.  
Required: items  
Props: `items` [{who:[name,colour],to:[name,colour],tag,segs:[[colour,text]],note,at}]; `compact` tighter cards; `style` css
Example: `{"a": "messages", "p": {"items": [{"who": ["Navigator", "teal"], "to": ["Flight lead", "blue"], "segs": [["plain", "Trajectory looks off by 170 km."]], "at": 0.5}]}}`

### `card` — stage
One key/value card (record, ID card, config).  
Required: title, rows  
Props: `title` label; `rows` [[key,value],...]; `note` red note; `w` width in cqw; `at` start
Example: `{"a": "card", "p": {"title": "Burn log", "rows": [["unit", "lbf·s"], ["expected", "N·s"]], "note": "mismatch"}}`

### `proportion` — stage
N of 100 dots lit: 'x out of 100'.  
Required: n, label  
Props: `n` 0-100; `label` caption; `color` colour; `at` start
Example: `{"a": "proportion", "p": {"n": 41, "label": "41 of 100 reviews were skipped", "color": "amber"}}`

### `transfer` — stage
One entity hands an item to another (with a size bar each).  
Required: from, to, a, b, move  
Props: `from` {name,color,bar%}; `to` {name,color,bar%}; `item` {title,sub}; `barLabel` label over bars; `caption` caption; `a` when `from` appears; `b` when `to` appears; `move` when item moves; `captionAt` when caption
Example: `{"a": "transfer", "p": {"from": {"name": "Team A", "color": "blue", "bar": 25}, "to": {"name": "Team B", "color": "teal", "bar": 95}, "item": {"title": "spec.pdf", "sub": "v2"}, "barLabel": "knowledge of change", "a": 0.5, "b": 1.5, "move": 3, "caption": "The change never reached B", "captionAt": 5}}`

### `sequence` — stage
2-4 boxes joined by arrows: a short process or verdict chain.  
Required: items  
Props: `items` list of strings; `at` start
Example: `{"a": "sequence", "p": {"items": ["Assume", "Skip the check", "Fail"], "at": 0.5}}`

### `list` — stage
Titled bullet list revealed one by one (takeaways).  
Required: title, items  
Props: `title` heading; `items` list of strings; `at` start
Example: `{"a": "list", "p": {"title": "Takeaways", "items": ["Check units at every interface", "Test with real data"], "at": 0.5}}`

### `source` — overlay
Small source/citation card bottom-centre.  
Required: title  
Props: `title` what the source is; `by` author / date; `at` appear
Example: `{"a": "source", "p": {"title": "Mishap Investigation Board report", "by": "NASA, Nov 1999", "at": 0.5}}`

### `lower` — overlay
Lower-third name tag (name + role) and/or a small source stamp line.  
Required: none  
Props: `name` name; `sub` role; `color` colour; `pos` left|right; `at` appear; `src` list of small source lines; `srcTop` put src at top; `srcAt` when src appears
Example: `{"a": "lower", "p": {"name": "Mars Climate Orbiter", "sub": "NASA / JPL, 1998", "color": "blue", "at": 0.5}}`

### `stamp` — overlay
Big verdict stamp (CONFIRMED / FAILED / FALSE) with optional sub-line.  
Required: text  
Props: `text` stamp word(s); `sub` sub-line; `align` center|flex-start|flex-end; `style` css; `at` appear
Example: `{"a": "stamp", "p": {"text": "LOST", "sub": "orbit insertion, Sep 23 1999", "at": 0.5}}`

### `note` — overlay
Small annotation panel anywhere on screen.  
Required: text  
Props: `text` plain text; `css` position css, default 'left:4cqw;bottom:4cqw'; `size` cqw font size; `color` colour; `mono` monospace; `at` appear
Example: `{"a": "note", "p": {"text": "1 lbf·s = 4.448 N·s", "mono": true, "at": 0.5}}`

## Worked example (excerpt of a finished story.json)
```
{
 "meta": {
  "title": "Mars Climate Orbiter: the unit mismatch",
  "lang": "en",
  "minutes": 3,
  "voice": "marin",
  "notes": "(excerpt: scenes 2-3 of a 6-scene demo)"
 },
 "pronunciation": {
  "JPL": "J P L",
  "lbf·s": "pound-force seconds",
  "N·s": "newton-seconds",
  "km": "kilometers"
 },
 "scenes": [
  {
   "title": "The mismatch",
   "beats": [
    "The interface document was clear: thruster impulse must be reported in newton-seconds, the metric unit.",
    "But the builder's software produced the numbers in pound-force seconds, the unit used in the United States.",
    "One pound-force second is about four point four five newton-seconds. And nothing in the data said which unit it was.",
    "So the navigators read every number as metric, and every number was off by a factor of four and a half."
   ],
   "cues": [
    {
     "a": "contrast",
     "at": "S2",
     "until": "E2",
     "p": {
      "top": {
       "label": "What the specification said",
       "at": 0.3,
       "steps": [
        {
         "text": "Thruster firing"
        },
        {
         "text": "Impulse in newton-seconds",
         "kind": "ok"
        },
        {
         "text": "Navigation model"
        }
       ]
      },
      "bottom": {
       "label": "What the software delivered",
       "at": "2b",
       "steps": [
        {
         "text": "Thruster firing"
        },
        {
         "text": "Impulse in pound-force seconds",
         "kind": "dashed"
        },
        {
         "text": "Navigation model"
        }
       ]
      },
      "strike": {
       "step": 1,
       "at": "2b#produced"
      },
      "note": {
       "chip": [
        "Navigation",
        "blue"
       ],
       "text": "reads every value as newton-seconds",
       "at": "2d#navigators"
      },
      "punch": {
       "text": "1 lbf·s = 4.448 N·s",
       "at": "2c#four"
      }
     }
    }
   ]
  },
  {
   "title": "Why nobody caught it",
   "beats": [
    "The error was small each time. A thruster firing here, a correction there. But the spacecraft fired its thrusters again and again for months.",
    "Each wrong number nudged the predicted path a little further from the real one.",
    "Some team members did notice that the trajectory looked odd. But the concern never became a formal, tracked problem.",
    "The checks looked at whether the software ran, not at what its numbers meant."
   ],
   "cues": [
    {
     "a": "pipeline",
     "at": "S3",
     "until": ">3b",
     "p": {
      "at": 0.3,
      "nodes": [
       {
        "title": "Builder software",
        "sub": "outputs lbf·s"
       },
       {
        "title": "Interface",
        "sub": "specified as N·s"
       },
       {
        "title": "Navigation",
        "sub": "assumes N·s"
       }
      ],
      "trigger": {
       "label": "unit mismatch",
       "at": "3a#again"
      },
      "packet": {
       "label": "wrong values",
       "at": "3b#Each"
      }
     }
    },
    {
     "a": "cards",
     "at": ">3b",
     "until": "E3",
     "p": {
      "at": 0.3,
      "items": [
       {
        "title": "Concern raised",
        "sub": "by team members",
        "code": "informal",
        "color": "amber"
       },
       {
        "title": "Formal problem report",
        "sub": "never opened",
        "code": "missing",
        "color": "red"
       },
       {
        "title": "Unit check",
        "sub": "not part of the tests",
        "code": "gap",
        "color": "red"
       }
      ],
      "banner": {
       "text": "The checks tested that it ran, not what the numbers meant",
       "tag": "root cause",
       "at": "3d#looked"
      }
     }
    }
   ]
  }
 ]
}
```


---
(USER MESSAGE TEMPLATE)
Target length: 10 minutes (≈ 1320 spoken words in total). Language: en.

SOURCE (between the markers):
<<<SOURCE
<paste the document text or script here>
SOURCE>>>

Return only the story.json object.
