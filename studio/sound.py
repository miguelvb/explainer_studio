"""Sound design: music styles (event-based synthesis), room ambience and sound effects driven by the cues.

Everything is synthesised with numpy/scipy, so nothing is downloaded and nothing is licensed.
Styles: pad (the original), pulse, cinema, bells, data.  All follow two curves taken from the story:
  intensity (0-1, per scene `intensity`, default arc)  and  tension (scene `mood: "tense"`).
"""
import json, wave
import numpy as np
from scipy import signal

SR = 44100
STYLES = ('pad', 'pulse', 'cinema', 'bells', 'data')
hz = lambda m: 440.0 * 2 ** ((np.asarray(m, dtype=np.float64) - 69) / 12)


# ------------------------------------------------------------------ curves
def curves(root, D=None):
    D = D or json.load(open(f'{root}/build/data.json')); st = json.load(open(f'{root}/story.json'))
    S = D['sched']; N = len(st['scenes']); total = D['total'] + 2
    ints = [sc.get('intensity') for sc in st['scenes']]
    arc = [.3 + .7 * (1 - abs(i / max(1, N - 1) - .7) / .7) if i / max(1, N - 1) <= .7 else 1 - (i / max(1, N - 1) - .7) / .3 * .6 for i in range(N)]
    ints = [x if x is not None else arc[i] for i, x in enumerate(ints)]
    mood = [1.0 if sc.get('mood') == 'tense' else 0.0 for sc in st['scenes']]
    keys = [(0, ints[0] * .8)] + [(S[f'S{i}']['s'] + 2, ints[i]) for i in range(N)] + [(total, 0)]
    mk = [(0, mood[0])] + [p for i in range(1, N) for p in ((S[f'S{i}']['s'], mood[i - 1]), (S[f'S{i}']['s'] + 3, mood[i]))] + [(total, mood[-1])]
    bounds = [(S[f'S{i}']['s'], ints[i], mood[i]) for i in range(N)]
    return dict(total=total, keys=keys, mk=mk, bounds=bounds, meta=st['meta'])


def make_t(total):
    n = int(total * SR); return n, np.arange(n, dtype=np.float32) / SR


def interp(t, pts): return np.interp(t, [p[0] for p in pts], [p[1] for p in pts]).astype(np.float32)


# ------------------------------------------------------------------ dsp helpers
def lp(x, fc, order=2):
    fc = float(np.clip(fc, 30, SR / 2 - 500)); sos = signal.butter(order, fc, 'low', fs=SR, output='sos'); return signal.sosfilt(sos, x).astype(np.float32)


def hp(x, fc, order=2):
    sos = signal.butter(order, float(fc), 'high', fs=SR, output='sos'); return signal.sosfilt(sos, x).astype(np.float32)


def bp(x, f0, f1, order=2):
    sos = signal.butter(order, [float(f0), float(f1)], 'band', fs=SR, output='sos'); return signal.sosfilt(sos, x).astype(np.float32)


def tt(d): return np.arange(int(d * SR), dtype=np.float32) / SR


def saw(f, d, ph=0.0):
    t = tt(d); return (2 * ((f * t + ph) % 1.0) - 1).astype(np.float32)


def adsr(d, a=.01, dec=.2, s=.0, r=.05):
    n = int(d * SR); t = np.arange(n, dtype=np.float32) / SR
    e = np.where(t < a, t / max(a, 1e-4), s + (1 - s) * np.exp(-(t - a) / max(dec, 1e-4))); rr = np.clip((d - t) / max(r, 1e-4), 0, 1)
    return (e * rr).astype(np.float32)


def bell(f, d=2.5, bright=1.0, dec=1.4):
    t = tt(d); idx = 2.2 * bright * np.exp(-t * 3.0)
    x = np.sin(2 * np.pi * f * t + idx * np.sin(2 * np.pi * f * 3.5 * t)) * np.exp(-t * dec) + .25 * np.sin(2 * np.pi * f * 2.0 * t) * np.exp(-t * dec * 1.8)
    return (x * np.clip(t / .004, 0, 1)).astype(np.float32)


def put(buf, t0, x, g=1.0, pan=.5):
    i = int(t0 * SR)
    if i >= buf.shape[1] or i + len(x) <= 0: return
    a = max(0, -i); e = min(len(x), buf.shape[1] - i); gl = np.cos(pan * np.pi / 2) * g * 1.41; gr = np.sin(pan * np.pi / 2) * g * 1.41
    buf[0, i + a:i + e] += x[a:e] * gl; buf[1, i + a:i + e] += x[a:e] * gr


def reverb(buf, sec=3.0, wet=.35, seed=3, damp=3500):
    rng = np.random.default_rng(seed); n = int(sec * SR); t = np.arange(n) / SR
    ir = [lp((rng.standard_normal(n) * np.exp(-t * (6.9 / sec))).astype(np.float32), damp) for _ in range(2)]
    out = np.stack([signal.oaconvolve(buf[c], ir[c], mode='full')[:buf.shape[1]] for c in range(2)]).astype(np.float32)
    out *= wet / (np.abs(out).max() + 1e-9) * np.abs(buf).max() * 1.2; return buf * (1 - wet * .4) + out


# ------------------------------------------------------------------ progression
CH = [[38, 45, 50, 53, 57], [34, 41, 46, 50, 53], [31, 38, 43, 46, 50], [33, 40, 45, 49, 52]]   # Dm  Bb  Gm  A


def chord_at(t, L):
    return CH[int(t // L) % 4]


# ------------------------------------------------------------------ styles
def style_pulse(cv, n, t, rng):
    total = cv['total']; inten = interp(t, cv['keys']); ten = interp(t, cv['mk']); buf = np.zeros((2, n), np.float32)
    bpm = 96; beat = 60 / bpm; L = beat * 8
    pat = [0, 2, 3, 2, 1, 2, 4, 2]
    k = 0; ti = 0.0
    while ti < total - 1:
        ii = float(inten[min(n - 1, int(ti * SR))]); te = float(ten[min(n - 1, int(ti * SR))]); ch = chord_at(ti, L)
        # pad swell per bar
        if abs(ti % L) < beat / 2:
            for nt in ch[:4]:
                d = L + 1; x = sum(saw(float(hz(nt)) * (1 + dt), d, rng.random()) for dt in (-.004, .004)) / 2
                put(buf, ti - .3, lp(x, 600 + 1400 * ii) * adsr(d, 1.8, 3, .8, 2.5), .05 * (.4 + .6 * ii), rng.random() * .6 + .2)
        # bass on each beat (pumping)
        if k % 2 == 0:
            f = float(hz(ch[0])); x = lp(saw(f, beat * 1.6), 300 + 600 * ii)
            put(buf, ti, x * adsr(beat * 1.6, .005, .35, .05, .1), .16 * (.35 + .65 * ii), .5)
        # soft kick above intensity .55
        if k % 4 == 0 and ii > .55:
            tk = tt(.35); kick = np.sin(2 * np.pi * (48 + 90 * np.exp(-tk * 30)) * tk) * np.exp(-tk * 9)
            put(buf, ti, kick.astype(np.float32), .22 * (ii - .4), .5)
        # arpeggio, eighth notes
        if ii > .2 and (k % 1 == 0):
            nt = ch[1 + pat[k % 8] % 4] + 12 * (1 if (k // 8) % 2 else 0) + (1 if te > .5 and k % 8 == 5 else 0)
            f = float(hz(nt)); d = beat * .9
            x = lp(saw(f, d, rng.random()), 700 + 4200 * ii * (1 - .4 * te)) * adsr(d, .004, .13, .0, .05)
            put(buf, ti, x, .1 * (.25 + .75 * ii), .25 + .5 * ((k % 4) / 3))
        ti += beat / 2; k += 1
    return reverb(buf, 2.4, .28)


def style_cinema(cv, n, t, rng):
    total = cv['total']; inten = interp(t, cv['keys']); ten = interp(t, cv['mk']); buf = np.zeros((2, n), np.float32); L = 16.0
    # continuous low drone
    drone = np.zeros(n, np.float32)
    for m, a in ((26, .5), (38, .3), (45, .16)):
        drone += np.sin(2 * np.pi * float(hz(m)) * t + rng.random() * 6) * a
    drone *= (.6 + .4 * np.sin(2 * np.pi * .05 * t)) * (.35 + .65 * inten) * .22
    buf[0] += drone; buf[1] += drone * .96
    ti = 0.0
    while ti < total - 2:
        ii = float(inten[min(n - 1, int(ti * SR))]); te = float(ten[min(n - 1, int(ti * SR))]); ch = chord_at(ti, L)
        for j, nt in enumerate(ch[1:]):
            d = L + 4; x = sum(saw(float(hz(nt + 12 * (j % 2))) * (1 + dt), d, rng.random()) for dt in (-.006, 0, .006)) / 3
            x = lp(x, 450 + 1800 * ii) * adsr(d, 5.0, 5, .85, 5.0)
            if te > .3: x = x * (1 - .35 * te) + .35 * te * lp(saw(float(hz(nt + 1)), d, rng.random()), 800) * adsr(d, 5, 5, .85, 5)
            put(buf, ti - 2, x, .07 * (.3 + .7 * ii), .25 + .5 * ((j * .37) % 1))
        ti += L
    # hits and risers at scene boundaries
    prev = .3
    for (ts, ii, mo) in cv['bounds']:
        if ts > 4 and (ii - prev > .12 or mo > 0):
            tb = tt(3.5); boom = (np.sin(2 * np.pi * (34 + 40 * np.exp(-tb * 5)) * tb) * np.exp(-tb * 1.1)).astype(np.float32)
            put(buf, ts - .05, boom, .35 * (.4 + .6 * ii), .5)
            rs = tt(5.0); sweep = lp(rng.standard_normal(len(rs)).astype(np.float32), 400) ; sweep = bp(rng.standard_normal(len(rs)).astype(np.float32), 300, 2500) * (rs / 5.0) ** 3
            put(buf, ts - 5.0, sweep, .22 * ii, .5)
        prev = ii
    # tension: tremolo cluster
    ten_c = (np.sin(2 * np.pi * float(hz(62)) * t) + np.sin(2 * np.pi * float(hz(63)) * t + 1)) * (.55 + .45 * np.sin(2 * np.pi * 5.5 * t)) * ten * .03
    buf[0] += ten_c; buf[1] += ten_c * .9
    hb = (t * 54 / 60) % 1.0; thump = (np.sin(2 * np.pi * 44 * t) * (np.exp(-hb * 14) + .5 * np.exp(-np.clip(hb - .3, 0, 9) * 16) * (hb > .3))) * ten * .3
    buf[0] += thump; buf[1] += thump
    return reverb(buf, 4.0, .4)


def style_bells(cv, n, t, rng):
    total = cv['total']; inten = interp(t, cv['keys']); ten = interp(t, cv['mk']); buf = np.zeros((2, n), np.float32); L = 24.0
    scale = [50, 53, 55, 57, 60, 62, 65, 67, 69, 72, 74, 77]   # D minor-ish pentatonic
    ti = 1.0
    while ti < total - 3:
        ii = float(inten[min(n - 1, int(ti * SR))]); te = float(ten[min(n - 1, int(ti * SR))]); ch = chord_at(ti, L)
        if abs(ti % L) < .5 or ti < 1.5:
            pass
        nt = int(rng.choice(ch[1:] + [ch[2] + 12, ch[3] + 12, ch[4] + 12]))
        if te > .5 and rng.random() < .35: nt -= 12 if nt > 60 else 0
        b = bell(float(hz(nt)), 4.0, .5 + .8 * ii, 1.1 + .6 * te)
        put(buf, ti, b, .16 * (.35 + .65 * ii), rng.random()); ti += rng.uniform(1.2, 4.8) * (1.5 - .9 * ii) * (1 + .5 * te)
    # pad
    ti = 0.0
    while ti < total:
        ch = chord_at(ti, L)
        for j, nt in enumerate(ch[:4]):
            d = L + 4; x = lp(sum(saw(float(hz(nt)) * (1 + dt), d, rng.random()) for dt in (-.005, .005)) / 2, 500 + 700 * float(inten[min(n - 1, int(ti * SR))])) * adsr(d, 6, 5, .8, 6)
            put(buf, ti - 2, x, .04, .3 + .4 * (j % 2))
        ti += L
    return reverb(buf, 5.0, .55, damp=5000)


def style_data(cv, n, t, rng):
    total = cv['total']; inten = interp(t, cv['keys']); ten = interp(t, cv['mk']); buf = np.zeros((2, n), np.float32)
    bpm = 108; step = 60 / bpm / 4; L = step * 32; k = 0; ti = 0.0
    scale = [62, 65, 67, 69, 72, 74, 77, 79]
    while ti < total - 1:
        ii = float(inten[min(n - 1, int(ti * SR))]); te = float(ten[min(n - 1, int(ti * SR))]); ch = chord_at(ti, L)
        if k % 16 == 0:   # sub bass note
            d = step * 14; x = lp(saw(float(hz(ch[0])), d), 220 + 500 * ii) * adsr(d, .01, .8, .5, .3); put(buf, ti, x, .17 * (.4 + .6 * ii), .5)
        if rng.random() < .15 + .6 * ii:     # hat / tick
            d = .05; x = hp(rng.standard_normal(int(d * SR)).astype(np.float32), 6000) * adsr(d, .001, .015, 0, .01); put(buf, ti, x, .05 * (.3 + .7 * ii) * (1.4 if k % 4 == 2 else .8), rng.random())
        if rng.random() < .12 + .35 * ii:    # digital blip
            nt = scale[int(rng.integers(len(scale)))] + (1 if te > .5 and rng.random() < .3 else 0); d = .09
            x = np.sign(np.sin(2 * np.pi * float(hz(nt)) * tt(d))) * .5 * adsr(d, .001, .04, 0, .02); put(buf, ti, lp(x, 3500), .05 * (.4 + .6 * ii), rng.random())
        if k % 32 == 0:   # soft pad stab
            for nt in ch[1:4]:
                d = L; x = lp(saw(float(hz(nt)), d, rng.random()), 900) * adsr(d, 2, 3, .6, 2); put(buf, ti, x, .035, rng.random())
        if ii > .5 and k % 8 == 0:
            tk = tt(.3); kick = np.sin(2 * np.pi * (46 + 80 * np.exp(-tk * 28)) * tk) * np.exp(-tk * 10); put(buf, ti, kick.astype(np.float32), .2 * (ii - .3), .5)
        ti += step; k += 1
    return reverb(buf, 1.8, .22)


def style_pad(cv, n, t, rng):
    """The original music bed (kept as it was; see audio.music for the legacy implementation)."""
    return None


# ------------------------------------------------------------------ ambience
def ambience(cv, n, t, rng, level=1.0):
    inten = interp(t, cv['keys']); ten = interp(t, cv['mk'])
    nz = rng.standard_normal(n).astype(np.float32); room = lp(nz, 500) * .35
    hum = (np.sin(2 * np.pi * 50 * t) * .5 + np.sin(2 * np.pi * 100 * t + 1) * .35 + np.sin(2 * np.pi * 150 * t + 2) * .15) * (.8 + .2 * np.sin(2 * np.pi * .07 * t))
    air = bp(rng.standard_normal(n).astype(np.float32), 1800, 5200) * (.25 + .5 * ten) * (.5 + .5 * np.sin(2 * np.pi * .04 * t + 1.1) ** 2)
    base = (room + hum * .18 + air * .25) * (.5 + .5 * inten + .4 * ten) * .05 * level
    out = np.stack([base, np.roll(base, 530)]).astype(np.float32)   # tiny inter-channel delay for width
    return out


# ------------------------------------------------------------------ sfx
def sfx_sound(kind, rng):
    """Short synthesised effect (mono float32) for a named kind."""
    if kind == 'pop':
        t = tt(.12); return (np.sin(2 * np.pi * (380 + 260 * np.exp(-t * 40)) * t) * np.exp(-t * 32)).astype(np.float32) * .5
    if kind == 'zip':
        d = .3; x = bp(rng.standard_normal(int(d * SR)).astype(np.float32), 1200, 4800) * np.sin(np.pi * tt(d) / d) ** 2; return x * .5
    if kind == 'chime':
        return _mix_at([(0, bell(float(hz(81)), 1.2, .7, 3.2)), (.12, bell(float(hz(88)), 1.6, .7, 2.8))])
    if kind == 'flag':
        return _mix_at([(0, bell(float(hz(84)), 1.8, .8, 2.2)), (.09, bell(float(hz(91)), 1.5, .6, 2.4))])
    if kind == 'thud':
        t = tt(.7); return (np.sin(2 * np.pi * (60 + 80 * np.exp(-t * 25)) * t) * np.exp(-t * 7)).astype(np.float32) + lp(rng.standard_normal(len(t)).astype(np.float32), 300) * np.exp(-t * 18) * .4
    if kind == 'deny':
        t = tt(.5); return (np.sin(2 * np.pi * 170 * t) * np.exp(-t * 7) * .7 + np.sin(2 * np.pi * 120 * t) * np.exp(-t * 5)).astype(np.float32) * .8
    if kind == 'spark':
        return _mix_at([(i * .07, bell(float(hz(93 + [0, 4, 7, 12][i])), .9, 1.0, 4.0)) for i in range(4)])
    if kind == 'key':
        return _mix_at([(i * .05, bell(float(hz(96 + [0, 4, 7][i])), .7, 1.4, 6.0)) for i in range(3)])
    if kind == 'power':
        d = 1.6; t = tt(d); f = 520 * np.exp(-t * 2.0) + 30; ph = 2 * np.pi * np.cumsum(f) / SR
        fl = (np.sin(t * (30 + 24 * t / d)) > -.4 + t / d).astype(np.float32) * .8 + .2
        return (np.sin(ph) * np.exp(-t * 1.4) * fl).astype(np.float32) * .8
    if kind == 'whoosh':
        d = 1.1; t = tt(d); x = bp(rng.standard_normal(len(t)).astype(np.float32), 200, 3200) * np.sin(np.pi * t / d) ** 2; return x * .55
    if kind == 'burst':
        return _mix_at([(i * .045, sfx_sound('pop', rng) * (.5 + .5 * rng.random())) for i in range(7)])
    if kind == 'lock':
        t = tt(.3); click = hp(rng.standard_normal(len(t)).astype(np.float32), 2500) * np.exp(-t * 90) * .8; return click + (np.sin(2 * np.pi * 140 * t) * np.exp(-t * 18)).astype(np.float32) * .7
    if kind == 'swell':
        d = 2.4; t = tt(d); return lp(rng.standard_normal(len(t)).astype(np.float32), 900) * (t / d) ** 2 * .9 * np.clip((d - t) / .5, 0, 1)
    if kind == 'bell':
        return bell(float(hz(76)), 3.5, .6, 1.0)
    if kind == 'rise':
        d = 4.0; t = tt(d); x = bp(rng.standard_normal(len(t)).astype(np.float32), 400, 4000) * (t / d) ** 2; return x * .7
    if kind == 'hole':
        t = tt(.35); return (np.sin(2 * np.pi * (160 - 80 * t / .35) * t) * np.exp(-t * 9)).astype(np.float32) * .8
    t = tt(.1); return np.zeros(len(t), np.float32)


def _mix_at(parts):
    L = max(int(a * SR) + len(x) for a, x in parts); out = np.zeros(L, np.float32)
    for a, x in parts: out[int(a * SR):int(a * SR) + len(x)] += x
    return out


KIND_SFX = {   # world node kind -> (sfx, gain)
    'acard': ('pop', .5), 'agent': ('pop', .3), 'koA': ('deny', .6), 'cross': ('deny', .6), 'okA': ('chime', .55), 'check': ('chime', .55),
    'flFly': ('flag', .5), 'flag': ('flag', .5), 'ideaSpark': ('spark', .5), 'bulb': ('spark', .5), 'key': ('key', .45), 'sigLock': ('lock', .6),
    'hole': ('hole', .5), 'bell': ('bell', .45), 'crowd': ('swell', .5), 'msgfeed': ('burst', .4), 'scHang': ('thud', .5), 'person': ('pop', .35),
    'orb': ('spark', .4), 'flagTrophy': ('flag', .5),
}


def sfx_events(root, D):
    from .spec import resolve, cue_times
    S = D['sched']; ev = []
    for i in range(len(D['scenes'])) if isinstance(D['scenes'], list) else range(D['scenes']):
        if f'S{i}' in S and i > 0: ev.append((S[f'S{i}']['s'] - .15, 'whoosh', .35, .5))
    for c in D.get('cues', []):
        try: cs, ce = cue_times(c, S)
        except Exception: continue
        if c.get('a') == 'seal': ev.append((cs + .2, 'rise', .45, .5)); continue
        if c.get('a') != 'world': continue
        T = lambda v: (cs + float(v)) if isinstance(v, (int, float)) else resolve(v, S)
        for nd in c.get('p', {}).get('nodes', []):
            k = nd.get('kind'); ta = T(nd.get('at', 0))
            if nd.get('flick'): ev.append((T(nd['flick']['at']), 'power', .5, (nd.get('x', 480) + (nd.get('w', 0) or 0) / 2) / 960)); continue
            if k in KIND_SFX and (nd.get('alpha', 1) or 1) > .2 and ta > cs - .01:
                s_, g = KIND_SFX[k]; ev.append((ta + .05, s_, g, (nd.get('x', 480) + (nd.get('w', 0) or 0) / 2) / 960))
    ev.sort()
    out = []; last = {}
    for t_, s_, g, p in ev:        # thin out dense bursts so the film does not rattle
        gap = {'pop': .35, 'swell': 3, 'whoosh': 1}.get(s_, .12)
        if t_ - last.get(s_, -9) < gap: continue
        last[s_] = t_; out.append((t_, s_, g, min(.95, max(.05, p))))
    return out


def render_sfx(root, D, t0=0.0, tot=None, out=None, level=1.0):
    tot = tot or D['total']; n = int((tot + 3) * SR); buf = np.zeros((2, n), np.float32); rng = np.random.default_rng(11); cache = {}
    for t_, s_, g, p in sfx_events(root, D):
        if not (t0 - 1 <= t_ < t0 + tot): continue
        cache.setdefault(s_, sfx_sound(s_, rng)); put(buf, t_ - t0, cache[s_], g * level, p)
    buf = reverb(buf, 1.6, .22) if buf.any() else buf
    out = out or f'{root}/build/sfx.wav'; write_wav(out, buf[:, :int(tot * SR)]); return out


# ------------------------------------------------------------------ output
def write_wav(path, buf, peak=.7):
    m = float(np.abs(buf).max()) or 1.0; x = (buf / m * peak) if peak else buf
    with wave.open(path, 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(x.T, -1, 1) * 32767).astype('<i2').tobytes())
    return path


def render_style(style, cv, seed=7, ambience_level=1.0):
    n, t = make_t(cv['total']); rng = np.random.default_rng(seed)
    fn = dict(pulse=style_pulse, cinema=style_cinema, bells=style_bells, data=style_data)[style]
    buf = fn(cv, n, t, rng)
    if ambience_level: buf = buf + ambience(cv, n, t, np.random.default_rng(seed + 1), ambience_level) * float(np.abs(buf).max()) * 6
    fi = max(.05, float(cv['meta'].get('fadein', 4))); fo = float(cv['meta'].get('fadeout', 4))
    buf *= (np.clip(t / fi, 0, 1) * np.clip((cv['total'] - 2 - t) / fo, 0, 1))[None]
    return buf


def demo_curves(total=48.0):
    keys = [(0, .25), (8, .35), (16, .6), (26, .95), (36, .6), (total, 0)]; mk = [(0, 0), (14, 0), (17, 1), (30, 1), (34, 0), (total, 0)]
    return dict(total=total, keys=keys, mk=mk, bounds=[(0, .25, 0), (16, .6, 1), (30, .9, 1), (36, .6, 0)], meta=dict(fadein=2, fadeout=4))


def demos(outdir, total=48.0):
    import os; os.makedirs(outdir, exist_ok=True); cv = demo_curves(total); res = []
    for s in ('pulse', 'cinema', 'bells', 'data'):
        res.append(write_wav(f'{outdir}/music_{s}.wav', render_style(s, cv)))
    return res


def sfx_sampler(path):
    rng = np.random.default_rng(5); kinds = ['whoosh', 'pop', 'zip', 'chime', 'flag', 'spark', 'key', 'lock', 'deny', 'thud', 'hole', 'burst', 'power', 'bell', 'swell', 'rise']
    buf = np.zeros((2, int((len(kinds) * 2.2 + 3) * SR)), np.float32)
    for i, k in enumerate(kinds): put(buf, 1 + i * 2.2, sfx_sound(k, rng), 1.0, .5)
    return write_wav(path, reverb(buf, 1.6, .22))
