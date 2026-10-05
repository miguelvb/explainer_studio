"""story.json  ->  normalised story -> schedule -> build/ (data.json, beats.json, captions.srt, player/).
story.json:
{ "meta": {"title","lang","minutes","voice","instructions","mark_label"},
  "pronunciation": {"written":"spoken"},
  "scenes": [ {"title","target"?,"intensity"?, "beats":["narration text",...],
               "cues":[{"a":asset,"at":anchor,"until":anchor|"dur":secs,"p":{...},"rect":"full|top|bottom|left|right|[l,t,w,h]","bg":bool,"fade":[in,out],"off":secs}]} ] }
Beat ids are generated: scene 0 -> 0a,0b,0c ... scene 3 -> 3a ...  Anchors: "3c" start of beat · ">3c" end · "3c#word" when the word is spoken ·
"S3"/"E3" scene start/end · "+1.5"/"-0.5" suffix = offset.   Numbers inside props are seconds from the cue's own start (or anchors)."""
import json, re, os, shutil, string
from .catalog import ASSETS, RECTS, is_overlay

PKG = os.path.dirname(os.path.abspath(__file__))
ANCH = re.compile(r'^(>?)([SE]?\d+[a-z]?)(?:#(.+?))?([+-]\d+(?:\.\d+)?)?$')


def est(text):
    """Estimated spoken duration (s) when no TTS timings exist yet."""
    return len(text.split()) / 2.45 + len(re.findall(r'[.?!]', text)) * 0.35 + len(re.findall(r'[,;:]', text)) * 0.15 + 0.25


def load(path):
    st = json.load(open(path, encoding='utf-8'))
    return normalise(st)


def normalise(st):
    st.setdefault('meta', {}); st.setdefault('pronunciation', {})
    st['meta'].setdefault('title', 'Untitled'); st['meta'].setdefault('lang', 'en')
    for n, sc in enumerate(st['scenes']):
        sc['n'] = n
        beats = []
        for k, b in enumerate(sc.get('beats', [])):
            beats.append({'id': f'{n}{string.ascii_lowercase[k]}', 'text': (b if isinstance(b, str) else b['text']).strip()})
        sc['beats'] = beats
        for c in sc.get('cues', []):
            c.setdefault('p', {})
            r = c.get('rect', 'full')
            c['rect'] = RECTS[r] if isinstance(r, str) and r in RECTS else r
            if 'bg' not in c and c.get('a') in ASSETS:
                c['bg'] = not is_overlay(c['a'], c['p'])
    return st


def schedule(st, timings=None, pad=True, gap=.55, pre=.8, post=1.8):
    timings = timings or {}
    m = st['meta']; gap = m.get('gap', gap); pre = m.get('pre', pre); post = m.get('post', post); tail = m.get('tail', 3.0)   # per-film pacing (seconds)
    scenes = st['scenes']; N = len(scenes)
    nat = []
    for n, sc in enumerate(scenes):
        d = [timings.get(b['id'], est(b['text'])) for b in sc['beats']]
        p0 = .6 if n == 0 else pre; p1 = post + (tail if n == N - 1 else 0)
        nat.append(p0 + sum(d) + gap * max(0, len(d) - 1) + p1)
    tgt = [sc.get('target') for sc in scenes]
    mins = st['meta'].get('minutes')
    if mins:
        fixed = sum(t for t in tgt if t); free = sum(nat[i] for i in range(N) if not tgt[i])
        if free:
            k = max(1.0, (mins * 60 - fixed) / free)
            tgt = [t or nat[i] * k for i, t in enumerate(tgt)]
    sched, order, t = {}, [], 0.0
    for n, sc in enumerate(scenes):
        beats = sc['beats']; d = [timings.get(b['id'], est(b['text'])) for b in beats]
        p0 = .6 if n == 0 else pre; p1 = post + (tail if n == N - 1 else 0); g = gap
        if pad and tgt[n] and nat[n] < tgt[n]:
            sur = tgt[n] - nat[n]
            ga = min(2.2, sur * .7 / max(1, len(d) - 1)) if len(d) > 1 else 0
            used = ga * max(0, len(d) - 1)
            p0 += (sur - used) * .3; p1 += (sur - used) * .7; g += ga
        sched[f'S{n}'] = {'s': round(t, 3), 'e': round(t, 3)}
        t += p0
        for b, dd in zip(beats, d):
            sched[b['id']] = {'s': round(t, 3), 'e': round(t + dd, 3), 'txt': b['text']}
            order.append(b['id']); t += dd + g
        t += p1 - g
        sched[f'E{n}'] = {'s': round(t, 3), 'e': round(t, 3)}
    return sched, order, round(t, 2)


def resolve(spec, sched):
    """Python twin of the player's anchor resolver. Returns seconds or raises ValueError."""
    if isinstance(spec, (int, float)): return float(spec)
    m = ANCH.match(str(spec))
    if not m: raise ValueError(f'bad anchor "{spec}" (use e.g. "3c", ">3c", "3c#word", "S3", "E3", with optional +1.5)')
    r = sched.get(m.group(2))
    if r is None: raise ValueError(f'anchor "{spec}" points to unknown beat/scene "{m.group(2)}"')
    if m.group(3):
        w = m.group(3).replace('_', ' ')
        tx = r.get('txt', '')
        mm = re.search(r'(^|[^A-Za-z0-9])' + re.escape(w) + r'(?![A-Za-z0-9])', tx, re.I)
        if not mm: raise ValueError(f'word "{w}" not found in beat {m.group(2)}: "{tx[:60]}…"')
        i = mm.start() + len(mm.group(1))
        wt = lambda ch: 7 if ch in '.?!' else 3.5 if ch in ',;:—' else 1
        a = sum(wt(c) for c in tx[:i]); b = sum(wt(c) for c in tx)
        base = r['s'] + (r['e'] - r['s']) * a / b
    else:
        base = r['e'] if m.group(1) else r['s']
    return base + (float(m.group(4)) if m.group(4) else 0)


def cue_times(c, sched):
    start = resolve(c['at'], sched) + c.get('off', 0)
    if c.get('until') is not None:
        ext = 0 if str(c['until']).startswith('E') or c.get('ext') == 0 else c.get('ext', .45)
        end = resolve(c['until'], sched) + c.get('untilOff', 0) + ext
    else:
        end = start + c['dur']
    return start, end


def validate(st, timings=None):
    """Static checks. Returns (errors, warnings) as lists of strings."""
    E, W = [], []
    if not st.get('scenes'): return ['story has no scenes'], W
    sched, order, total = schedule(st, timings, pad=True)
    for sc in st['scenes']:
        n = sc['n']; tag = f'scene {n}'
        if not sc['beats']: E.append(f'{tag}: no beats'); continue
        if len(sc['beats']) > 26: E.append(f'{tag}: more than 26 beats')
        for b in sc['beats']:
            w = len(b['text'].split())
            if w < 4: W.append(f'{b["id"]}: very short beat ({w} words)')
            if w > 55: W.append(f'{b["id"]}: long beat ({w} words) — split it so visuals can change')
        cues = sc.get('cues', [])
        if not cues: E.append(f'{tag}: no cues (nothing to show)')
        spans = []
        for i, c in enumerate(cues):
            ct = f'{tag} cue {i} ({c.get("a")})'
            a = c.get('a')
            if a not in ASSETS: E.append(f'{ct}: unknown asset "{a}". Available: {", ".join(ASSETS)}'); continue
            cat = ASSETS[a]
            for r in cat.get('required', []):
                if r not in c['p']: E.append(f'{ct}: missing required prop "{r}"')
            for k in c['p']:
                if k not in cat['props']: W.append(f'{ct}: unknown prop "{k}" (known: {", ".join(cat["props"])})')
            if 'at' not in c: E.append(f'{ct}: missing "at"'); continue
            if 'until' not in c and 'dur' not in c: E.append(f'{ct}: needs "until" or "dur"'); continue
            try:
                s, e = cue_times(c, sched)
            except ValueError as x:
                E.append(f'{ct}: {x}'); continue
            if e <= s + .3: E.append(f'{ct}: ends before it starts / shorter than 0.3 s (at={c["at"]}, until={c.get("until")})')
            if not is_overlay(a, c['p']) and c.get('rect') == RECTS['full']: spans.append((s, e))
            _check_props(c['p'], sched, ct, E)
        # coverage: sample the scene; the union of active stage cues must cover (almost) the whole frame
        S, Eend = sched[f'S{n}']['s'], sched[f'E{n}']['s']
        stage = []
        for c in cues:
            if c.get('a') in ASSETS and not is_overlay(c['a'], c['p']) and 'at' in c and ('until' in c or 'dur' in c):
                try: s0, e0 = cue_times(c, sched)
                except ValueError: continue
                stage.append((s0, e0, c.get('rect') or RECTS['full']))
        def cov(t):
            g = set()
            for s0, e0, r in stage:
                if s0 - .01 <= t <= e0 + .01:
                    for i in range(10):
                        for j in range(10):
                            x, y = i * 10 + 5, j * 10 + 5
                            if r[0] <= x <= r[0] + r[2] and r[1] <= y <= r[1] + r[3]: g.add((i, j))
            return len(g)
        bad, t = [], S + .6
        while t < Eend - .6:
            if cov(t) < 85: bad.append(t)
            t += .5
        if bad:
            runs, st0, prev = [], bad[0], bad[0]
            for x in bad[1:]:
                if x - prev > .6: runs.append((st0, prev)); st0 = x
                prev = x
            runs.append((st0, prev))
            for g0, g1 in runs:
                if g1 - g0 >= .9: W.append(f'{tag}: frame not covered by a stage visual {g0 - S:.1f}s–{g1 - S:.1f}s into the scene — extend a cue or add one')
    return E, W


def _chain(spans, a, b):
    cur = a
    for s, e in sorted(spans):
        if s <= cur + .6: cur = max(cur, e)
    return cur >= b - .2


def _check_props(p, sched, ct, E):
    """Any string value that looks like an anchor (digit+letter / S1 / E1 / >1a) must resolve."""
    def walk(v, path):
        if isinstance(v, dict):
            for k, x in v.items(): walk(x, f'{path}.{k}')
        elif isinstance(v, list):
            for i, x in enumerate(v): walk(x, f'{path}[{i}]')
        elif isinstance(v, str) and re.match(r'^(>?\d+[a-z](#.+)?|[SE]\d+)([+-]\d+(\.\d+)?)?$', v) and re.search(r'(at|At|steps|end|out|appear|walls|flag|packets|hl|move|a|b)\b', path):
            try: resolve(v, sched)
            except ValueError as x: E.append(f'{ct}: prop {path}: {x}')
    walk(p, 'p')


def write_build(st, root, timings=None, pad=True, **kw):
    """Write build/data.json etc. + the player. Returns summary dict."""
    b = os.path.join(root, 'build'); os.makedirs(b, exist_ok=True)
    sched, order, total = schedule(st, timings, pad, **kw)
    cues = []
    for sc in st['scenes']:
        for c in sc.get('cues', []):
            q = {k: v for k, v in c.items() if k in ('a', 'at', 'until', 'dur', 'off', 'untilOff', 'ext', 'rect', 'bg', 'fade', 'z', 'id', 'p')}
            cues.append(q)
    json.dump({'sched': sched, 'cues': cues, 'total': total, 'fps': 30, 'scenes': len(st['scenes'])}, open(f'{b}/data.json', 'w'), ensure_ascii=False)
    json.dump([{'id': i, 'text': sched[i]['txt'], 'start': sched[i]['s']} for i in order], open(f'{b}/beats.json', 'w'), ensure_ascii=False, indent=1)
    _srt(sched, order, f'{b}/captions.srt')
    # player
    pdir = f'{b}/player'; os.makedirs(pdir, exist_ok=True)
    for f in ('assets.js', 'style.css'): shutil.copy(f'{PKG}/player/{f}', f'{pdir}/{f}')
    mark = st['meta'].get('mark')
    mp = os.path.join(root, mark) if mark and os.path.exists(os.path.join(root, mark)) else f'{PKG}/default_mark.txt'
    head, d = open(mp).read().split('\n', 1); W, H = head.split()
    lang = st['meta'].get('lang', 'en')[:2]; numsep = st['meta'].get('numsep') or ('.' if lang in ('es', 'de', 'it', 'pt') else ',')
    html = f'''<!doctype html><html><head><meta charset="utf-8"><title>{st["meta"]["title"]}</title><link rel="stylesheet" href="style.css"></head>
<body style="margin:0;background:#0E1218"><svg width="0" height="0" style="position:absolute"><symbol id="mark" viewBox="0 0 {W} {H}"><path fill="currentColor" fill-rule="evenodd" d="{d.strip()}"/></symbol></svg>
<div id="stage"></div><script>window.NUMSEP="{numsep}"</script><script src="assets.js"></script></body></html>'''
    open(f'{pdir}/index.html', 'w').write(html)
    return dict(total=total, beats=len(order), cues=len(cues), sched=sched)


def _ts(x):
    h, m, s = int(x // 3600), int(x % 3600 // 60), x % 60
    return f'{h:02d}:{m:02d}:{s:06.3f}'.replace('.', ',')


def _srt(sched, order, path):
    with open(path, 'w', encoding='utf-8') as f:
        k = 1
        for i in order:
            b = sched[i]
            parts = re.split(r'(?<=[.?!”])\s+', b['txt']); lines, cur = [], ''
            for p in parts:
                if cur and len(cur) + len(p) > 84: lines.append(cur); cur = p
                else: cur = (cur + ' ' + p).strip()
            if cur: lines.append(cur)
            tot = sum(len(x) for x in lines); acc = 0
            for x in lines:
                s0 = b['s'] + (b['e'] - b['s']) * acc / tot; acc += len(x); s1 = b['s'] + (b['e'] - b['s']) * acc / tot
                f.write(f'{k}\n{_ts(s0)} --> {_ts(min(s1, b["e"]))}\n{x}\n\n'); k += 1
