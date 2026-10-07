"""storykit — generic story builder for any film.

A film lives in one folder:

    <film>/
      film.py          META (the `meta` of story.json) and PRONUNCIATION (the `pronunciation` table)
      narration.md     the narration (source of truth), one `## N · Title` block per scene, one `**3a** sentence` per beat
      scenes/sNN.py    one DSL script per scene: it builds `cues` (and optionally the sound plan)
      story.json       generated: never edit it by hand

`python explainer.py gen -p <film>` (or `storykit.generate(root)`) assembles story.json.

Scene scripts run in a shared namespace that already contains the helpers below (N, K, L, ag, box, sc, ch, ic, AN,
Q, T, BAR, OR, link …), `W` (studio.worldkit), `math`, the palette (TEAL, CORAL …) and anything a previous scene
defined. A scene script sets:

    cues       list of cues (required)
    PROFILE    'house' (default) or 'raw' — see below
    MUSIC      {style: weight}   music layers of this chapter (default {'pad': 1})
    MOOD       'tense'           (optional)
    INTENSITY  0..1              (optional) music intensity of this scene
    SFX        [{at, kind, g}]   (optional) sound stingers

Profiles. `house` bakes in the house rules (names and chips never wider than the text, communication links never
flatter than curve .3, orthogonal links always solid, quotes sized to their text …). `raw` is the plain constructor
set, kept so that older scenes render exactly as they were approved.
"""
import json, math, re, runpy, glob, os, contextlib
from pathlib import Path
from . import worldkit as W

# ---------------------------------------------------------------- palette
VIO, ORG, RED, BLU, GRY = '#B58CFF', '#FF9F43', '#FF6E6E', '#7C97FF', '#8C96A4'
AMB, TEAL, CORAL, GRN = '#F6B94C', '#3FD8C2', '#FF8A5C', '#9BE564'
CW = .6          # width of a monospace glyph / font size


# ---------------------------------------------------------------- raw constructors
def flat(n):
    """Flatten one level: a node list may contain lists of nodes (agent() returns a list)."""
    return [x for p in n for x in (p if isinstance(p, list) else [p])]


def N(id, kind, x, y, w, h, at=0.05, **k):
    d = dict(id=id, kind=kind, x=round(x), y=round(y), w=round(w), h=round(h), at=at)
    d.update({a: b for a, b in k.items() if b is not None}); return d


def ag(id, cx, cy, at=0.05, s=46, color='blue', **k): return N(id, 'agent', cx - s / 2, cy - s / 2, s, s, at, color=color, **k)
def box(id, x, y, w, h, at=0.05, color='teal', **k): return N(id, 'sandbox', x, y, w, h, at, color=color, **k)
def sc(id, cx, cy, at=0.05, s=96, **k): return box(id, cx - s / 2, cy - s / 2, s, s, at, **k)       # small container around an agent
def srv(id, x, y, w, h, at=0.05, color='amber', **k): return N(id, 'server', x, y, w, h, at, color=color, **k)
def ch_raw(id, cx, cy, w, label, at=0.05, color='muted', **k): return N(id, 'chip', cx - w / 2, cy - 13, w, 26, at, label=label, color=color, **k)
def ic_raw(id, kind, cx, cy, s, at=0.05, color='amber', **k):
    kind = {'check': 'okA', 'cross': 'koA'}.get(kind, kind); return N(id, kind, cx - s / 2, cy - s / 2, s, s, at, color=color, **k)
def L(a, b, at=0.05, color='blue', **k): d = dict(a=a, b=b, at=at, color=color); d.update(k); return d


def K_raw(at, until, nodes, links=None, fs=1.5, cam=None):
    """A `world` cue: persistent diagram with nodes, links and an optional camera path."""
    d = dict(a='world', at=at, until=until, p=dict(nodes=nodes, links=links or [], fs=fs), bg=True, fade=[0.5, 0.5])
    if cam: d['cam'] = cam
    return d


# ---------------------------------------------------------------- house rules
_agent_named, _link = W.agent_named, W.link


def AN(id, x, y, name, at=0.05, w=110, h=130, color='blue', fs=12, **k):
    """Named agent card sized to its name."""
    fs = min(fs, 12); w = int(max(min(w, 140), len(name) * CW * fs + 16)); h = min(h, 170)
    return _agent_named(id, x, y, name, at=at, w=w, h=h, color=color, fs=fs, **k)


def SA(id, cx, cy, at=0.05, s=22, color='blue', **k): return W.agent(id, cx, cy, at, s=s, color=color, box=False, **k)


def Q(id, x, y, w, lines, at, color='teal', fs=17, **k):
    """Agent quote; the width follows the longest line (`w` is ignored on purpose)."""
    fs = round(fs * .9); w = max(len(l) for l in lines) * fs * .62 + 40; x = min(x, 940 - w)
    return N(id, 'quote', x, y, w, 26 + len(lines) * fs * 1.45, at, color=color, lines=lines, fs=fs, **k)


def T(id, x, y, text, at, color=GRY, fs=14, **k):
    """Small text label."""
    fs = round(fs * .9); w = len(text) * fs * CW; x = min(x, 945 - w); return N(id, 'txt', x, y, w + 4, fs + 4, at, color=color, fs=fs, text=text, **k)


def ch(id, cx, cy, w, label, at=0.05, color='muted', fs=12, **k):
    fs = min(fs, 12); w = max(w, len(label) * CW * fs + 20); return ch_raw(id, cx, cy, w, label, at, color=color, fs=fs, **k)


def ic(id, kind, cx, cy, s, at=0.05, color='amber', **k): return ic_raw(id, kind, cx, cy, s, at, color=color, **k)


def link(a, b, at=0.05, color='blue', **k):
    """Link with the house curve (never flatter than .3; orthogonal links are solid)."""
    if not k.get('orth') and not k.get('lock'): k['curve'] = max(abs(k.get('curve', .12)), .3)
    if k.get('orth'): k['solid'] = True
    return _link(a, b, at, color=color, **k)


def OR(a, b, at, color, mode=True, mid=None, **k):
    """Orthogonal (rectilinear, rounded corners, solid) link. mode True | 'h' | 'v'."""
    d = dict(orth=mode, **k)
    if mid is not None: d['mid'] = mid
    return link(a, b, at, color=color, **d)


def BAR(id, x, y, w, fill, at, color, label='presupuesto', **k):
    """Progress/budget bar with its small caption (returns two nodes)."""
    return [N(id, 'bar', x, y, w, 12, at, color=color, fill=fill, **k),
            T(id + 't', x, y + 18, label, at, color=GRY, fs=12, **({'until': k['until']} if 'until' in k else {}))]


def K_house(at, until, nodes, links=None, fs=1.5, cam=None): return K_raw(at, until, flat(nodes), links, fs, cam)


BASE = dict(N=N, ag=ag, box=box, sc=sc, srv=srv, L=L, flat=flat, W=W, math=math, json=json, re=re,
            VIO=VIO, ORG=ORG, RED=RED, BLU=BLU, GRY=GRY, AMB=AMB, TEAL=TEAL, CORAL=CORAL, GRN=GRN, CW=CW)
RAW = dict(BASE, ch=ch_raw, ic=ic_raw, K=K_raw)
HOUSE = dict(BASE, ch=ch, ic=ic, K=K_house, AN=AN, SA=SA, Q=Q, T=T, link=link, OR=OR, BAR=BAR)


@contextlib.contextmanager
def _house_rules():
    """worldkit's own agent_named / link are patched for the length of a house-profile scene."""
    W.agent_named = lambda id, x, y, name, at=0.05, w=110, h=130, color='blue', fs=12, **k: AN(id, x, y, name, at, w, h, color, fs, **k)
    W.link = link
    try: yield
    finally: W.agent_named, W.link = _agent_named, _link


# ---------------------------------------------------------------- narration.md  (script.md is generated by `build` for reading)
BEAT = re.compile(r'^\*\*(\d+[a-z])\*\* (?:\(pausa ([\d.]+)\) )?(.*)$')


def parse_script(path):
    """narration.md -> [(title, [beat, ...])]; a beat is a str or {text, pause}."""
    out = []
    for blk in re.split(r'^## ', Path(path).read_text(encoding='utf-8'), flags=re.M)[1:]:
        head, *rest = blk.split('\n')
        title = head.split(' · ', 1)[1].strip() if ' · ' in head else head.strip()
        beats = []
        for line in rest:
            m = BEAT.match(line.strip())
            if m: beats.append(dict(text=m.group(3), pause=float(m.group(2))) if m.group(2) else m.group(3))
        out.append((title, beats))
    return out


def write_script(path, scenes):
    """Inverse of parse_script (used once, to migrate an existing story.json)."""
    lines = []
    for i, sc_ in enumerate(scenes):
        lines.append(f"## {i} · {sc_['title']}\n")
        for j, b in enumerate(sc_['beats']):
            t, p = (b['text'], b.get('pause')) if isinstance(b, dict) else (b, None)
            lines.append(f"**{i}{chr(97 + j)}** " + (f"(pausa {p:g}) " if p else '') + t + '\n')
    Path(path).write_text('\n'.join(lines), encoding='utf-8')


# ---------------------------------------------------------------- lint
def lint(cues_by_scene, log=print):
    """Cheap geometry checks on world nodes: text wider than its box, nodes outside the 960x540 frame."""
    bad = 0
    for si, cs in enumerate(cues_by_scene):
        for ci, c in enumerate(cs):
            for nd in c.get('p', {}).get('nodes', []):
                k = nd['kind']; x, y, w, h = nd['x'], nd['y'], nd['w'], nd['h']; msg = []
                if k == 'quote':
                    fs = nd.get('fs', 18); need = max(len(l) for l in nd['lines']) * fs * .62 + 30
                    if need > w + 2: msg.append(f'quote text {need:.0f}>{w}')
                if k == 'chip':
                    fs = nd.get('fs', 11); need = (len(nd.get('label', '')) * fs * CW + 10) if nd.get('label') else 0
                    if need > w + 2: msg.append(f'chip text {need:.0f}>{w}')
                if k == 'txt':
                    fs = nd.get('fs', 18); need = len(nd.get('text', '')) * fs * CW
                    if x + need > 952: msg.append(f'txt right edge {x + need:.0f}')
                if k == 'acard':
                    fs = nd.get('fs', 11); need = len(nd.get('label', '')) * fs * CW + 8
                    if need > w + 2: msg.append(f'acard label {need:.0f}>{w}')
                if k in ('hfbox', 'server'):
                    need = len(nd.get('label', '')) * 14 * CW + (h * .7 if k == 'hfbox' else 10)
                    if need > w + 2: msg.append(f'{k} label {need:.0f}>{w}')
                if k == 'folderview':
                    fs = nd.get('fs', 10); mx = max([len(i['name']) for i in nd.get('items', [])] + [len(nd.get('label', ''))])
                    if mx * fs * CW + 50 > w: msg.append(f'folder text {mx * fs * CW + 50:.0f}>{w}')
                if not c.get('cam') and (k not in ('sandbox', 'globe') or w < 900):   # a cue with a camera may place nodes off-frame on purpose
                    if x < -1 or y < -1 or x + w > 961 or y + h > 541: msg.append(f'out of frame ({x},{y},{w},{h})')
                if nd.get('cap'):
                    need = len(nd['cap']) * nd.get('capfs', 11) * CW; cx = x + w / 2
                    if cx - need / 2 < 4 or cx + need / 2 > 956: msg.append('cap out of frame')
                if msg: bad += 1; log(f'  LINT scene {si} cue {ci} node {nd["id"]}: ' + '; '.join(msg))
    log('lint:', bad, 'issues'); return bad


# ---------------------------------------------------------------- assembling a film
def generate(root, write=True, log=print):
    """Build `<root>/story.json` from film.py + narration.md + scenes/*.py and return the story dict."""
    root = Path(root); film = runpy.run_path(str(root / 'film.py'))
    script = parse_script(root / 'narration.md')
    files = sorted(glob.glob(str(root / 'scenes' / 's*.py')))
    if len(files) != len(script): raise SystemExit(f'{len(files)} scene files but {len(script)} scenes in narration.md')
    ns = {}; scenes = []; cues_all = []; house = []
    for i, (f, (title, beats)) in enumerate(zip(files, script)):
        src = Path(f).read_text(encoding='utf-8')
        m = re.search(r'^PROFILE\s*=\s*[\'"](\w+)[\'"]', src, re.M); profile = m.group(1) if m else 'house'
        for k_ in ('cues', 'MUSIC', 'MOOD', 'INTENSITY', 'SFX', 'PROFILE'): ns.pop(k_, None)
        ns.update(RAW if profile == 'raw' else HOUSE); ns['__file__'] = f
        cm = _house_rules() if profile == 'house' else contextlib.nullcontext()
        with cm: exec(compile(src, f, 'exec'), ns)
        d = dict(title=title, beats=beats, cues=ns['cues'], music=ns.get('MUSIC', {'pad': 1}))
        if ns.get('MOOD'): d['mood'] = ns['MOOD']
        if ns.get('INTENSITY') is not None: d['intensity'] = ns['INTENSITY']
        if ns.get('SFX'): d['sfx'] = ns['SFX']
        scenes.append(d); cues_all.append(ns['cues']); house.append(profile == 'house')
    story = dict(meta=film['META'], pronunciation=film['PRONUNCIATION'], scenes=scenes)
    W.classify_links(story); lint(cues_all, log)
    if write: (root / 'story.json').write_text(json.dumps(story, ensure_ascii=False, indent=1), encoding='utf-8')
    return story


# ---------------------------------------------------------------- scaffolding for a new film
_FILM = '''# Film definition: `meta` of story.json and the pronunciation table.
# Narration lives in narration.md and the scenes in scenes/sNN.py (see studio/storykit.py).
META = dict(
    title=%(title)r, lang='es',
    provider='elevenlabs', el_voice='cristina', el_model='eleven_v4', el_speed=0.95, el_stability=0.5,
    music_style='mix', music_db=-8, sfx_db=-12, duck_ratio=2.5, duck_threshold=0.04, ambience=1.0,
    background='poly', fadein=0.3,
)
PRONUNCIATION = {}
EL_PRONUNCIATION = {}   # {'OpenAI': 'Óupen Ei Ái'}; copy it into META['el_pronunciation'] when needed
'''
_NARR = """## 0 · Gancho

**0a** (pausa 2) %(title)s.

**0b** Primera frase de la historia. Una frase por línea; el id (0b, 0c…) es la letra de la frase dentro de la escena.
"""
_SCENE = """# Scene 0 · Gancho
MUSIC = {'bells': 1}
# `cues` is the list of things that appear. Anchors hang from the narration: '0b#palabra+0.4', 'S0', 'E0'.
cues = [
    dict(a='seal', at='S0', until='0b', ext=0, p=dict(text='%(title)s', sub='Arkinos @ oct 2026  ·  Explainer Studio', at=0.5, type=14, scale=1.0, cy=215, ty=392), bg=True, fade=[0.8, 2.0]),
    K('0b', 'E0', [AN('ag', 200, 150, 'AGENTE', at=0.4)], [], fs=1.0),
]
"""


def new_film(root, title):
    """Write a minimal film skeleton (film.py, narration.md, scenes/s00.py)."""
    root = Path(root); (root / 'scenes').mkdir(parents=True, exist_ok=True); d = dict(title=title)
    (root / 'film.py').write_text(_FILM % d, encoding='utf-8')
    (root / 'narration.md').write_text(_NARR % d, encoding='utf-8')
    (root / 'scenes' / 's00.py').write_text(_SCENE % d, encoding='utf-8')
    return root
