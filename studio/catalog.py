"""Asset catalog: the single source of truth for validation AND for the LLM prompt.
kind  : 'stage'   = full-frame visual (gets an opaque background by default)
        'overlay' = drawn on top of a stage (transparent)
props : name -> one-line doc.  Times inside props are seconds from the cue start OR anchors ("3c#word").
"""
COLORS = ["blue", "teal", "amber", "red", "muted"]
SEG = ["blue", "teal", "amber", "plain", "muted", "red"]   # colours of text segments [colour, text]

ASSETS = {
 "title": dict(kind="stage", use="Opening / closing title card.", required=["title"],
   props=dict(kicker="small label above", title="big text, \\n allowed", sub="subtitle", src="list of source lines (small, bottom)", at="when it appears"),
   example=dict(kicker="CASE STUDY", title="The unit mismatch\\nthat sank a probe", sub="Mars Climate Orbiter, 1999")),
 "feed": dict(kind="stage", use="A live stream of short coloured lines (messages, logs, events). Gives 'a lot is happening' texture; real lines can be pinned.",
   props=dict(lines="list of lines; each line = list of [colour,text] segments (real, pinned lines come first)", filler="false | {prefix,verbs,words,names,mode} generated filler lines", vis="visible lines (default 9)",
              key="legend [[colour,label],...] or false", typed="{at,cps} types line 0 first", zoom="{from,at,dur} zoom-out reveal", rate="[[time,lines_per_sec],...]",
              first="time of first line", last="segments of a special final line", lastAt="when the special line lands", hl="indices to outline", dim="opacity of the stream"),
   example=dict(lines=[[["blue", "TELEMETRY"], ["plain", " trajectory_update "], ["teal", "ground"]]], filler=False, vis=6)),
 "annotated": dict(kind="stage", use="One exploded message/string with each part labelled in turn (anatomy of a record).", required=["msgs"],
   props=dict(heading="small label", msgs="list of messages; message = list of [kind,text]", kinds="{kind:{label,color}} (defaults: type,sender,recipient,content,reply)", order="kinds in the order they are explained",
              steps="times at which each kind in `order` is highlighted", end="time all parts light up again", tags="list of small tag boxes", tagsAt="when tags appear", at="when cards appear"),
   example=dict(heading="A thruster report", kinds={"unit": {"label": "unit", "color": "amber"}, "val": {"label": "value", "color": "teal"}}, order=["val", "unit"],
                msgs=[[["val", "Impulse: 4.45 "], ["unit", "lbf·s"]]], steps=[2, 4], end=6)),
 "chips": dict(kind="stage", use="Entities as pills carrying the theme mark (actors, agents, systems, teams), grouped in labelled rows.", required=["rows"],
   props=dict(rows="[[label,colour,[names],flag]] — flag=true/'text' draws a red flagged badge", big="larger pills", stag="stagger secs", at="start", style="css for container"),
   example=dict(rows=[["Ground team", "blue", ["Navigation", "Flight dynamics"]], ["Vendor", "amber", ["Lockheed software"]]])),
 "network": dict(kind="stage", use="A graph of nodes joining one by one with a counter ('N units').", props=dict(at="start", dur="growth seconds", from_="start count", to="end count (max 90)", unit="counter noun", packets="false to hide moving packets"),
   example=dict(at=0.5, dur=8, to=60, unit="agents")),
 "population": dict(kind="stage", use="Grid of many units, a share flagged/changed, optionally all feeding one shared resource (a 'tap').",
   props=dict(label="top label", flaggedShare="0-1", appear="when grid appears", walls="when cells flash (isolation)", flag="when flagged cells turn red", flagLegend="legend after flagging", tap="label of the shared resource bar", tapAt="when it appears", packets="when dots start flowing to the resource"),
   example=dict(label="70 independent sandboxes", appear=0.5, flag=6, flagLegend="flagged", tap="shared package registry", tapAt=9, packets=11)),
 "listing": dict(kind="stage", use="Left panel where a name/path is typed (file tree, command, URL) + optional right panel with a list.", props=dict(title="panel title", root="root line", rows="[[colour,text]]", typed="text to type", typeAt="when typing starts", cps="chars/sec", call="callout after typing", kids="child lines", kidsAt="when they appear", foot="footer line", footAt="when", right="{title,at,lines:[[colour,text]],call}"),
   example=dict(title="/reports/", root="reports/", rows=[["muted", "q1.csv"]], typed="q2_final.csv", typeAt=1, call="new file")),
 "counters": dict(kind="stage", use="Big animated numbers. Use pos='top'/'bottom' to make it an overlay on another stage.", required=["items"],
   props=dict(items="[{label,n,from,pre,suf,txt,at,dur,color}] n=target number; txt overrides the number with fixed text", pos="center|top|bottom", small="smaller digits"),
   example=dict(items=[{"label": "mission cost (USD millions)", "n": 327, "pre": "$", "at": 0.5}, {"label": "years of cruise", "n": 9, "at": 1.5}])),
 "timeline": dict(kind="stage", use="Dated events on an axis (up/down stems).", required=["ev"],
   props=dict(axis="{labels:[...],hours:N per label} (default 6 days × 24h)", ev="[{h,date,label,pos(+up/-down px),color,at}] h = position in axis hours", vb="svg viewBox crop", axisY="axis y (default 270)", at="axis draws"),
   example=dict(axis={"labels": ["1998", "1999 Jan", "1999 Sep"], "hours": 24}, ev=[{"h": 4, "date": "Dec 1998", "label": "Launch", "pos": 90, "color": "blue", "at": 1}, {"h": 60, "date": "Sep 23", "label": "Orbit insertion", "pos": -90, "color": "red", "at": 3}])),
 "equation": dict(kind="stage", use="Boxes joined by arrows/operators lit in sequence (a formula, a causal chain), plus evidence rows below.", required=["boxes"],
   props=dict(boxes="list of strings", seps="operators between boxes (default →)", hl="when lighting starts", step="secs between boxes", caption="line under the chain", captionAt="when", rows="[{chip:[name,colour,flag?],text,box,mono,at}]"),
   example=dict(boxes=["Thruster firing", "× impulse (lbf·s)", "= trajectory error"], hl=1, step=1.2)),
 "contrast": dict(kind="stage", use="What was believed vs what actually happened: two rows of step boxes, strike-through and ghost steps.", required=["top", "bottom"],
   props=dict(top="{label,steps:[{text,kind(ok|dashed|'')}],at}", bottom="same", note="{chip:[name,colour],text,at}", punch="{text,at}", strike="{step,at} strikes a step of top", ghost="{step,at} reveals a step of bottom"),
   example=dict(top={"label": "What the spec said", "at": 0.5, "steps": [{"text": "Metric units"}, {"text": "Newton-seconds"}]}, bottom={"label": "What the software did", "at": 3, "steps": [{"text": "Metric units"}, {"text": "Pound-force seconds", "kind": "dashed"}]}, strike={"step": 1, "at": 5})),
 "options": dict(kind="stage", use="One hub branching to 2-4 alternatives/approaches, each a card with lines and marks.", required=["hub", "items"],
   props=dict(hub="{name,sub,color}", items="[{title,lines:[...],marks:[[text,colour],...]}]", at="list of start times per item"),
   example=dict(hub={"name": "The team", "sub": "had three options", "color": "blue"}, items=[{"title": "Burn now", "lines": ["risky"], "marks": [["fast", "amber"]]}, {"title": "Wait", "lines": ["safe"], "marks": [["slow", "teal"]]}], at=[1, 2.5])),
 "pipeline": dict(kind="stage", use="Three stages in a row (A → B → C) with a trigger on the middle one and a packet flowing on.", required=["nodes"],
   props=dict(nodes="exactly 3 × {title,sub}", at="start", trigger="{label,at}", packet="{label,at}"),
   example=dict(nodes=[{"title": "Sensor", "sub": "raw data"}, {"title": "Converter", "sub": "wrong units"}, {"title": "Navigation", "sub": "uses result"}], trigger={"label": "bug", "at": 3}, packet={"label": "bad value", "at": 5})),
 "cards": dict(kind="stage", use="A row of labelled cards (options, votes, roles) + optional highlighted banner.", props=dict(items="[{title,sub,code,color}]", at="start", stag="stagger", banner="{text,tag,at}"),
   example=dict(items=[{"title": "Review A", "sub": "approved", "code": "OK", "color": "teal"}, {"title": "Review B", "sub": "skipped", "code": "—", "color": "amber"}], banner={"text": "Nobody checked the units", "tag": "gap", "at": 3})),
 "terminal": dict(kind="stage", use="A terminal window: a command is typed, then a result appears.", props=dict(cmd="command text", cps="typing speed", struck="struck-through line", result="bold result", note="small note", at="typing start", out="when output appears"),
   example=dict(cmd="convert --from lbf_s --to N_s 4.45", result="19.8 N·s", note="never run in flight software", at=0.5)),
 "bars": dict(kind="stage", use="Horizontal bars to compare shares/amounts.", required=["items"], props=dict(items="[{label,val(text),w(0-100),color,at,from,dur}]", gap="spacing", style="css"),
   example=dict(items=[{"label": "Predicted", "val": "1×", "w": 20, "color": "teal", "at": 0.5}, {"label": "Actual", "val": "4.45×", "w": 90, "color": "red", "at": 1.5}])),
 "steps": dict(kind="stage", use="Staircase of escalating levels/stages.", required=["rows"], props=dict(rows="[{title,desc,when,color}]", at="start", step="secs between", foot="mono footer"),
   example=dict(rows=[{"title": "Level 1", "desc": "noticed", "when": "day 1", "color": "blue"}, {"title": "Level 2", "desc": "ignored", "when": "day 30", "color": "red"}])),
 "groups": dict(kind="stage", use="Leaders assigning work to columns of dots (parallel workers split into groups).", required=["groups"], props=dict(leads="[[name,colour]]", leadText="caption beside leads", groups="[{title,color,n}]", at="start"),
   example=dict(leads=[["Lead", "blue"]], leadText="splits the work", groups=[{"title": "Team A", "color": "teal", "n": 10}, {"title": "Team B", "color": "amber", "n": 14}])),
 "quote": dict(kind="stage", use="Quote cards (verbatim quotes, paraphrases, agent/person statements).", required=["cards"], props=dict(cards="[{text,kind(quote|raw|par|agent),who:[name,colour],label,at}]", big="larger text", sm="smaller", pos="top|bottom", cols="columns"),
   example=dict(cards=[{"text": "We assumed the numbers were metric.", "kind": "quote", "at": 0.5, "label": "Engineer, board hearing"}])),
 "messages": dict(kind="stage", use="Stacked message cards (emails, chat, log entries) with sender → recipient and coloured segments.", required=["items"],
   props=dict(items="[{who:[name,colour],to:[name,colour],tag,segs:[[colour,text]],note,at}]", compact="tighter cards", style="css"),
   example=dict(items=[{"who": ["Navigator", "teal"], "to": ["Flight lead", "blue"], "segs": [["plain", "Trajectory looks off by 170 km."]], "at": 0.5}])),
 "card": dict(kind="stage", use="One key/value card (record, ID card, config).", required=["title", "rows"], props=dict(title="label", rows="[[key,value],...]", note="red note", w="width in cqw", at="start"),
   example=dict(title="Burn log", rows=[["unit", "lbf·s"], ["expected", "N·s"]], note="mismatch")),
 "proportion": dict(kind="stage", use="N of 100 dots lit: 'x out of 100'.", required=["n", "label"], props=dict(n="0-100", label="caption", color="colour", at="start"), example=dict(n=41, label="41 of 100 reviews were skipped", color="amber")),
 "transfer": dict(kind="stage", use="One entity hands an item to another (with a size bar each).", required=["from", "to", "a", "b", "move"],
   props=dict(**{"from": "{name,color,bar%}", "to": "{name,color,bar%}", "item": "{title,sub}", "barLabel": "label over bars", "caption": "caption", "a": "when `from` appears", "b": "when `to` appears", "move": "when item moves", "captionAt": "when caption"}),
   example={"from": {"name": "Team A", "color": "blue", "bar": 25}, "to": {"name": "Team B", "color": "teal", "bar": 95}, "item": {"title": "spec.pdf", "sub": "v2"}, "barLabel": "knowledge of change", "a": 0.5, "b": 1.5, "move": 3, "caption": "The change never reached B", "captionAt": 5}),
 "sequence": dict(kind="stage", use="2-4 boxes joined by arrows: a short process or verdict chain.", required=["items"], props=dict(items="list of strings", at="start"), example=dict(items=["Assume", "Skip the check", "Fail"], at=0.5)),
 "list": dict(kind="stage", use="Titled bullet list revealed one by one (takeaways).", required=["title", "items"], props=dict(title="heading", items="list of strings", at="start"), example=dict(title="Takeaways", items=["Check units at every interface", "Test with real data"], at=0.5)),
 "source": dict(kind="overlay", use="Small source/citation card bottom-centre.", required=["title"], props=dict(title="what the source is", by="author / date", at="appear"), example=dict(title="Mishap Investigation Board report", by="NASA, Nov 1999", at=0.5)),
 "lower": dict(kind="overlay", use="Lower-third name tag (name + role) and/or a small source stamp line.", props=dict(name="name", sub="role", color="colour", pos="left|right", at="appear", src="list of small source lines", srcTop="put src at top", srcAt="when src appears"),
   example=dict(name="Mars Climate Orbiter", sub="NASA / JPL, 1998", color="blue", at=0.5)),
 "stamp": dict(kind="overlay", use="Big verdict stamp (CONFIRMED / FAILED / FALSE) with optional sub-line.", required=["text"], props=dict(text="stamp word(s)", sub="sub-line", align="center|flex-start|flex-end", style="css", at="appear"), example=dict(text="LOST", sub="orbit insertion, Sep 23 1999", at=0.5)),
 "note": dict(kind="overlay", use="Small annotation panel anywhere on screen.", required=["text"], props=dict(text="plain text", css="position css, default 'left:4cqw;bottom:4cqw'", size="cqw font size", color="colour", mono="monospace", at="appear"), example=dict(text="1 lbf·s = 4.448 N·s", mono=True, at=0.5)),
}
# 'from_' is written 'from' in JSON (python keyword workaround)
ASSETS["network"]["props"]["from"] = ASSETS["network"]["props"].pop("from_")

RECTS = {"full": [0, 0, 100, 100], "top": [0, 0, 100, 50], "bottom": [0, 50, 100, 50], "left": [0, 0, 50, 100], "right": [50, 0, 50, 100]}


def is_overlay(asset, props):
    k = ASSETS[asset]["kind"]
    if asset == "counters" and (props or {}).get("pos") in ("top", "bottom"):
        return True
    if asset == "quote" and (props or {}).get("pos") in ("top", "bottom"):
        return False
    return k == "overlay"
