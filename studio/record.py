"""Narration from your own recordings: clean, normalise, a touch of reverb, then cut into one MP3 per beat.

  python explainer.py record -p examples/film toma1.m4a toma2.m4a            # finds the beats it hears (needs faster-whisper)
  python explainer.py record -p examples/film toma.m4a --from 0 --to 2       # without faster-whisper: says which scenes were read

Writes audio/beats/<id>.mp3 and audio/timings.json like `tts`, plus audio/recorded.json (which beats come from a
recording: `tts` and `all` leave them alone) and audio/rec/report.txt (where each beat was cut, to check by ear).
`record --clear` forgets the recorded beats so the next `tts` speaks them again.
"""
import os, re, json, difflib, subprocess, unicodedata

# highpass + spectral denoise + soft gate + gentle compression; reverb and loudness are added per call
CLEAN = 'highpass=f=80,lowpass=f=14000,afftdn=nr=14:nf=-50:tn=1,agate=threshold=0.012:ratio=2:attack=5:release=180,acompressor=threshold=-20dB:ratio=2.5:attack=8:release=120'
SR = 44100


def _ff(*a): subprocess.run(['ffmpeg', '-y', '-hide_banner', '-loglevel', 'error', *a], check=True)
def _norm(w): return re.sub(r'[^a-z0-9ñ]', '', ''.join(c for c in unicodedata.normalize('NFD', w.lower()) if unicodedata.category(c) != 'Mn' or c == '̃'))
def _toks(text): return [t for t in (_norm(w) for w in re.sub(r'\[[^\]]*\]', ' ', text).split()) if t]


def clean(files, out, reverb=0.07, lufs=-18):
    """Every take cleaned and joined (0.6 s of silence between takes), then one loudness pass for the whole thing."""
    d = os.path.dirname(out); parts = []
    for k, f in enumerate(files):
        p = f'{d}/take{k}.wav'; _ff('-i', f, '-af', CLEAN, '-ar', str(SR), '-ac', '1', p); parts.append(p)
    lst = f'{d}/takes.txt'; gap = f'{d}/gap.wav'
    _ff('-f', 'lavfi', '-i', f'anullsrc=r={SR}:cl=mono', '-t', '0.6', gap)
    open(lst, 'w').write(''.join(f"file '{os.path.abspath(x)}'\n" for p in parts for x in ([p] if p == parts[-1] else [p, gap])))
    rv = f',aecho=0.9:0.9:35|70:{reverb:.3f}|{reverb * 0.6:.3f}' if reverb > 0 else ''
    _ff('-f', 'concat', '-safe', '0', '-i', lst, '-af', f'aformat=sample_rates={SR}:channel_layouts=mono{rv},loudnorm=I={lufs}:TP=-1.5:LRA=9', '-ar', str(SR), out)
    return out


def transcribe(wav, model='small', lang='es', log=print):
    """[(word, start, end)] or None when faster-whisper (or its model) is not available."""
    try: from faster_whisper import WhisperModel
    except ImportError: log('faster-whisper no está instalado (pip install faster-whisper): corto por pausas'); return None
    try: m = WhisperModel(model, device='cpu', compute_type='int8')
    except Exception as e: log(f'no se pudo cargar el modelo whisper «{model}» ({str(e)[:80]}): corto por pausas'); return None
    segs, _ = m.transcribe(wav, language=lang, word_timestamps=True, vad_filter=True)
    return [(w.word, w.start, w.end) for s in segs for w in s.words]


def align_words(beats, words):
    """Beat id -> (start, end) from the transcript: match script tokens to heard tokens, keep beats mostly heard."""
    st, own = [], []
    for k, b in enumerate(beats):
        t = _toks(b['text']); st += t; own += [k] * len(t)
    heard, idx = [], []
    for j, (w, _, _) in enumerate(words):
        for t in _toks(w): heard.append(t); idx.append(j)
    hit = {}
    for a, b_, n in difflib.SequenceMatcher(None, st, heard, autojunk=False).get_matching_blocks():
        for i in range(n): hit[a + i] = idx[b_ + i]
    out = {}
    for k, b in enumerate(beats):
        mine = [i for i in range(len(st)) if own[i] == k]
        got = [hit[i] for i in mine if i in hit]
        if mine and len(got) >= max(2, 0.4 * len(mine)):
            out[b['id']] = (words[min(got)][1], words[max(got)][2])
    return out


def pauses(wav, db=-38, dur=0.3):
    """[(start, end)] of the silences in the cleaned recording."""
    r = subprocess.run(['ffmpeg', '-hide_banner', '-i', wav, '-af', f'silencedetect=noise={db}dB:d={dur}', '-f', 'null', '-'], capture_output=True, text=True).stderr
    s = [float(x) for x in re.findall(r'silence_start: ([\d.]+)', r)]; e = [float(x) for x in re.findall(r'silence_end: ([\d.]+)', r)]
    return list(zip(s, e))


def align_pauses(beats, wav, total):
    """Without a transcript: the n-1 cuts go to the pauses nearest to where the word counts say each beat ends."""
    P = pauses(wav); P = [p for p in P if p[1] - p[0] >= 0.3]
    t0 = P[0][1] if P and P[0][0] < 0.05 else 0.0; t1 = P[-1][0] if P and P[-1][1] > total - 0.05 else total
    inner = [p for p in P if t0 < p[0] and p[1] < t1]
    n = [len(_toks(b['text'])) for b in beats]; N = sum(n) or 1
    cuts, prev, acc = [], t0, 0
    for k in range(len(beats) - 1):
        acc += n[k]; want = t0 + (t1 - t0) * acc / N
        cand = [p for p in inner if p[0] > prev + 0.5]
        if not cand: break
        # nearest pause, longer pauses win ties (a beat usually ends on a breath)
        p = min(cand, key=lambda p: abs((p[0] + p[1]) / 2 - want) - 1.5 * (p[1] - p[0]))
        cuts.append(p); prev = p[1]
    out, s = {}, t0
    for k, b in enumerate(beats):
        e = cuts[k][0] if k < len(cuts) else t1
        out[b['id']] = (s, e)
        if k < len(cuts): s = cuts[k][1]
    return out


def record(root, files, scenes=None, model='small', reverb=0.07, lufs=-18, lang='es', log=print):
    from .audio import _dur
    beats = json.load(open(f'{root}/build/beats.json'))
    if scenes is not None: beats = [b for b in beats if re.fullmatch(r'(\d+)[a-z]+', b['id']) and int(re.match(r'\d+', b['id']).group()) in scenes]
    rd = f'{root}/audio/rec'; os.makedirs(rd, exist_ok=True); os.makedirs(f'{root}/audio/beats', exist_ok=True)
    wav = clean(files, f'{rd}/clean.wav', reverb=reverb, lufs=lufs); total = _dur(wav)
    log(f'grabación limpia: {total:.1f} s -> {wav}')
    words = transcribe(wav, model=model, lang=lang, log=log)
    if words: span = align_words(beats, words); mode = 'whisper'
    else:
        if scenes is None: raise SystemExit('sin faster-whisper hay que decir qué escenas se leen: --from N --to M (o --scene N)')
        span = align_pauses(beats, wav, total); mode = 'pausas'
    ids = [b['id'] for b in beats if b['id'] in span]
    if not ids: raise SystemExit('no he reconocido ningún beat del guion en la grabación')
    tf = f'{root}/audio/timings.json'; T = json.load(open(tf)) if os.path.exists(tf) else {}
    rf = f'{root}/audio/recorded.json'; R = json.load(open(rf)) if os.path.exists(rf) else {}
    rep = []
    for k, i in enumerate(ids):
        s, e = span[i]
        # cut halfway into the pauses around the beat, at most 0.25 s before and 0.4 s after the voice
        lo = span[ids[k - 1]][1] if k else 0.0; hi = span[ids[k + 1]][0] if k + 1 < len(ids) else total
        a = max(lo + (s - lo) / 2, s - 0.25, 0.0); z = min(e + (hi - e) / 2, e + 0.4, total)
        p = f'{root}/audio/beats/{i}.mp3'
        _ff('-ss', f'{a:.3f}', '-to', f'{z:.3f}', '-i', wav, '-af', f'afade=t=in:d=0.02,areverse,afade=t=in:d=0.06,areverse', '-c:a', 'libmp3lame', '-q:a', '2', p)
        T[i] = round(_dur(p) + .12, 3); R[i] = dict(mode=mode, start=round(a, 2), end=round(z, 2), files=[os.path.basename(f) for f in files])
        rep.append(f'{i:>4}  {a:7.2f}–{z:7.2f}  ({z - a:5.2f} s)')
    json.dump(T, open(tf, 'w'), indent=1); json.dump(R, open(rf, 'w'), indent=1)
    hf = f'{root}/audio/hashes.json'   # drop the TTS fingerprints, so after `record --clear` these beats are spoken again
    if os.path.exists(hf): H = json.load(open(hf)); [H.pop(i, None) for i in ids]; json.dump(H, open(hf, 'w'), indent=1)
    miss = [b['id'] for b in beats if b['id'] not in span]
    open(f'{rd}/report.txt', 'w').write(f'modo: {mode}\n' + '\n'.join(rep) + (f'\nsin encontrar: {", ".join(miss)}\n' if miss else '\n'))
    log(f'{len(ids)} beats grabados ({mode}): {ids[0]}…{ids[-1]}' + (f' · sin encontrar: {", ".join(miss)}' if miss else '') + f' · revisa {rd}/report.txt')
    return ids


def clear(root, log=print):
    rf = f'{root}/audio/recorded.json'
    if os.path.exists(rf): os.remove(rf); log('olvidados los beats grabados: el próximo tts los vuelve a generar')
