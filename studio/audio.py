"""TTS (OpenAI), synthesised music bed, final mux."""
import os, json, subprocess, wave
import numpy as np

DEFAULT_INSTR = ("Calm, measured documentary narrator. Neutral accent, clear diction, no hype and no drama. "
                 "Slightly slower than conversational pace, with a short natural pause at the end of every sentence. "
                 "Read names, codes and numbers slowly and clearly.")


def _dur(p):
    return float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', p]).strip())


EL_MODEL = 'eleven_multilingual_v2'
# Spanish male candidates (voice ids from the public ElevenLabs library; availability can change)
EL_CANDIDATES = {'jacobo': 'syjZiIvIUSwKREBfMpKZ', 'carlos': '4FMxnogu8ehUVsRIxx9H', 'jeijo': 'PBaBRSRTvwmnK1PAq9e0',
                 'mateo': 'LcMajEnHqf3tUTha5ppa', 'juancarlos': 'YExhVa4bZONzeingloMX', 'manuel': 'L7pBVwjueW3IPcQt4Ej9',
                 # female
                 'cristina': '2VUqK4PEdMj16L6xTN4J', 'maria': 'GszuzIPs4fVZTjP0EXrv', 'sofia': 'pK5bIn1o1zvVRcDhFUSb',
                 'ligia': 'szJ1F5SgxGkjGanyygoW', 'lourdes': 'SbxCN6LQhBInYaeKjhhW', 'melanie': 'bN1bDXgDIGX5lw0rtY2B'}
OA_CANDIDATES = ['cedar', 'onyx', 'ash', 'echo', 'verse', 'fable', 'marin', 'coral', 'nova', 'shimmer', 'sage']


def _el_say(text, voice, path, model=None, stability=.5, similarity=.75, style=0.0, speed=1.0):
    """ElevenLabs text-to-speech -> mp3. voice = voice id (or a name from EL_CANDIDATES). Key: ELEVENLABS_API_KEY."""
    import urllib.request, urllib.error
    key = os.environ.get('ELEVENLABS_API_KEY') or os.environ.get('XI_API_KEY')
    if not key: raise SystemExit('ELEVENLABS_API_KEY not set (add ELEVENLABS_API_KEY=... to .env)')
    voice = EL_CANDIDATES.get(voice, voice)
    body = json.dumps({'text': text, 'model_id': model or EL_MODEL, 'voice_settings': {'stability': stability, 'similarity_boost': similarity, 'style': style, 'use_speaker_boost': True, 'speed': speed}}).encode()
    rq = urllib.request.Request(f'https://api.elevenlabs.io/v1/text-to-speech/{voice}?output_format=mp3_44100_128', data=body, headers={'xi-api-key': key, 'Content-Type': 'application/json', 'Accept': 'audio/mpeg'})
    try:
        with urllib.request.urlopen(rq, timeout=180) as r: open(path, 'wb').write(r.read())
    except urllib.error.HTTPError as e:
        hint = f"\n  key read from .env: {key[:3]}...{key[-3:]} ({len(key)} chars). Check: no quotes/spaces/duplicate ELEVENLABS_API_KEY line, key not deleted, 'Text to Speech' access enabled for the key." if e.code == 401 else ''
        raise SystemExit(f'ElevenLabs error {e.code}: {e.read().decode()[:300]}{hint}')


def voices(root, st, text=None, openai_voices=None, el_voices=None, el_model=None, log=print):
    """Same sentence in several voices -> <project>/audio/voices/*.mp3, to choose by ear. Skips providers without a key."""
    from . import env; env.load(root)
    beats = json.load(open(f'{root}/build/beats.json')); text = text or beats[0]['text']
    raw = text
    def prep(el):
        pr = sorted({**st.get('pronunciation', {}), **(st['meta'].get('el_pronunciation', {}) if el else {})}.items(), key=lambda kv: -len(kv[0])); t = raw
        for k, v in pr: t = t.replace(k, v)
        return t
    text = prep(False); text_el = prep(True)
    out = f'{root}/audio/voices'; os.makedirs(out, exist_ok=True); m = st['meta']; made = []
    log(f'sample text ({len(text)} chars): {text[:90]}...')
    if 'OPENAI_API_KEY' in os.environ:
        from openai import OpenAI
        c = OpenAI(); instr = m.get('instructions') or os.environ.get('OPENAI_TTS_INSTRUCTIONS') or DEFAULT_INSTR
        for v in openai_voices or OA_CANDIDATES:
            p = f'{out}/openai_{v}.mp3'; log(f'openai {v}')
            with c.audio.speech.with_streaming_response.create(model='gpt-4o-mini-tts', voice=v, input=text, instructions=instr, response_format='mp3') as r: r.stream_to_file(p)
            made.append(p)
    else: log('OPENAI_API_KEY not set: skipping OpenAI voices')
    if os.environ.get('ELEVENLABS_API_KEY') or os.environ.get('XI_API_KEY'):
        for v in el_voices or list(EL_CANDIDATES):
            tag = '' if not el_model else '_' + el_model.replace('eleven_', ''); p = f'{out}/eleven_{v}{tag}.mp3'; log(f'elevenlabs {v} {el_model or EL_MODEL}'); _el_say(text_el, v, p, model=el_model); made.append(p)
    else: log('ELEVENLABS_API_KEY not set: skipping ElevenLabs voices')
    log(f'{len(made)} samples in {out}'); return made


def tts(root, st, model=None, voice=None, speed=None, only=None, force=False, log=print):
    """One MP3 per beat -> audio/beats/<id>.mp3 and audio/timings.json. Needs OPENAI_API_KEY (env or .env)."""
    from . import env; env.load(root)
    m0 = st['meta']; prov = (m0.get('provider') or os.environ.get('TTS_PROVIDER') or 'openai').lower(); el = prov.startswith('eleven')
    if not el and 'OPENAI_API_KEY' not in os.environ: raise SystemExit('OPENAI_API_KEY not set. .env files read: ' + (', '.join(env.FOUND) or 'none found') + '. The line must look like OPENAI_API_KEY=sk-...')
    client = None
    if not el: from openai import OpenAI; client = OpenAI()
    m = st['meta']; E = os.environ
    model = model or m.get('model') or E.get('OPENAI_TTS_MODEL', 'gpt-4o-mini-tts'); voice = voice or m.get('voice') or E.get('OPENAI_TTS_VOICE') or 'marin'
    speed = float(speed or m.get('speed') or E.get('OPENAI_TTS_SPEED', 1.0)); instr = m.get('instructions') or E.get('OPENAI_TTS_INSTRUCTIONS') or DEFAULT_INSTR
    if el: model = m.get('el_model') or E.get('ELEVENLABS_MODEL', EL_MODEL); voice = m.get('el_voice') or E.get('ELEVENLABS_VOICE') or 'jacobo'; speed = float(m.get('el_speed') or speed); instr = f"el|{m.get('el_stability', .5)}|{m.get('el_style', 0)}"
    log(f'tts[{prov}] model={model} voice={voice} speed={speed}')
    pron = sorted({**st.get('pronunciation', {}), **(m.get('el_pronunciation', {}) if el else {})}.items(), key=lambda kv: -len(kv[0]))
    def say(t):
        for k, v in pron: t = t.replace(k, v)
        return t
    beats = json.load(open(f'{root}/build/beats.json')); os.makedirs(f'{root}/audio/beats', exist_ok=True)
    tf = f'{root}/audio/timings.json'; T = json.load(open(tf)) if os.path.exists(tf) else {}
    hf = f'{root}/audio/hashes.json'; Hh = json.load(open(hf)) if os.path.exists(hf) else {}   # text+voice fingerprint per beat: edited beats or a new voice re-speak themselves
    import hashlib
    for b in beats:
        i = b['id']
        if only and i not in only: continue
        p = f'{root}/audio/beats/{i}.mp3'
        hh = hashlib.sha1('|'.join([say(b['text']), model, voice, str(speed), instr]).encode()).hexdigest()[:12]
        if os.path.exists(p) and not force and i in T and Hh.get(i) == hh: continue
        log(f'tts {i}')
        if el: _el_say(say(b['text']), voice, p, model=model, speed=min(1.2, max(.7, speed)), stability=float(m.get('el_stability', .5)), style=float(m.get('el_style', 0)))
        else:
            with client.audio.speech.with_streaming_response.create(model=model, voice=voice, input=say(b['text']), instructions=instr, speed=speed, response_format='mp3') as r:
                r.stream_to_file(p)
        T[i] = round(_dur(p) + .12, 3); json.dump(T, open(tf, 'w'), indent=1); Hh[i] = hh; json.dump(Hh, open(hf, 'w'), indent=1)
    log(f'timings -> {tf}  narration {sum(T.values()):.0f}s')


def music(root, out=None, style=None, ambience=None):
    """Music bed. meta.music_style: pad (default) | pulse | cinema | bells | data. Shaped by each scene's `intensity` (0-1) and `mood: tense`."""
    _m = json.load(open(f'{root}/story.json'))['meta']; _style = style or _m.get('music_style', 'pad')
    if ambience is not None: _m = dict(_m, ambience=ambience)
    if _style == 'mix':
        from . import sound
        return sound.render_mix(root, out=out or f'{root}/build/music.wav')
    if _style != 'pad':
        from . import sound
        D = json.load(open(f'{root}/build/data.json')); cv = sound.curves(root, D)
        buf = sound.render_style(_style, cv, ambience_level=float(_m.get('ambience', 1.0)))
        return sound.write_wav(out or f'{root}/build/music.wav', buf)
    D = json.load(open(f'{root}/build/data.json')); S = D['sched']; N = D['scenes']; total = D['total'] + 2; fo = float(json.load(open(f'{root}/story.json'))['meta'].get('fadeout', 4))
    st = json.load(open(f'{root}/story.json')); ints = [sc.get('intensity') for sc in st['scenes']]
    arc = [.3 + .7 * (1 - abs(i / max(1, N - 1) - .7) / .7) if i / max(1, N - 1) <= .7 else 1 - (i / max(1, N - 1) - .7) / .3 * .6 for i in range(N)]
    ints = [x if x is not None else arc[i] for i, x in enumerate(ints)]
    sr = 44100; n = int(total * sr); t = np.arange(n, dtype=np.float32) / sr; rng = np.random.default_rng(7)
    keys = [(0, ints[0] * .8)] + [(S[f'S{i}']['s'] + 2, ints[i]) for i in range(N)] + [(total, 0)]
    inten = np.interp(t, [k[0] for k in keys], [k[1] for k in keys]).astype(np.float32)
    hz = lambda m: 440.0 * 2 ** ((m - 69) / 12)
    chords = [[38, 45, 53, 57, 60], [34, 46, 53, 58, 62], [43, 50, 53, 58, 62], [33, 45, 52, 57, 61]]; L = 32.0
    pad = np.zeros(n, np.float32); padR = np.zeros(n, np.float32)
    # oscillator parameters are drawn up-front (same rng order as always), then the pad is synthesised in 60 s blocks: flat memory for hour-long films
    prm = [[(note, det, pan, rng.random() * 6.283, .03 + .01 * rng.random(), rng.random() * 6.283) for note in ch for det, pan in ((-.07, 0), (.07, 1), (0, 2))] for ch in chords]
    Ls = int(L * sr); w = int(10 * sr); nc = n - w + 1; BL = sr * 60
    for b0 in range(0, n, BL):
        b1 = min(n, b0 + BL); ts = np.arange(b0, b1) / sr; ins = inten[b0:b1]
        j = np.clip(np.arange(b0, b1) - w // 2, 0, nc - 1); j0 = int(j[0]); j1 = int(j[-1]) + w
        gi = np.arange(j0, j1) // Ls % 4
        for ci in range(4):
            cs = np.concatenate([[0], np.cumsum((gi == ci).astype(np.float32))]); es = ((cs[j - j0 + w] - cs[j - j0]) / w).astype(np.float32)
            if es.max() <= 1e-6: continue
            for note, det, pan, ph, lf, lp_ in prm[ci]:
                f = hz(note); lfo = .65 + .35 * np.sin(2 * np.pi * lf * ts + lp_)
                osc = np.sin(2 * np.pi * f * (1 + det * .01) * ts + ph) + .35 * np.sin(2 * np.pi * 2 * f * (1 + det * .01) * ts + ph * 1.3) + .12 * np.sin(2 * np.pi * 3 * f * ts + ph)
                g = es * lfo * (.5 if note < 50 else .34) * (.45 + .55 * ins)
                o = (osc * g).astype(np.float32)
                if pan == 0: pad[b0:b1] += o
                elif pan == 1: padR[b0:b1] += o
                else: pad[b0:b1] += o * .6; padR[b0:b1] += o * .6
    ping = np.zeros(n, np.float32); pingR = np.zeros(n, np.float32); tt = 4.0
    while tt < total - 4:
        f = hz([74, 77, 79, 81, 84, 86][rng.integers(6)]); i0 = int(tt * sr); L2 = int(3.2 * sr); seg = t[:L2]
        bell = (np.sin(2 * np.pi * f * seg) + .4 * np.sin(2 * np.pi * f * 2.76 * seg)) * np.exp(-seg * 1.5); amp = .05 * (.3 + .7 * inten[min(n - 1, i0)]); e = min(n, i0 + L2)
        (ping if rng.random() < .5 else pingR)[i0:e] += bell[:e - i0] * amp
        tt += rng.uniform(3.5, 9.0) * (1.3 - .8 * inten[min(n - 1, i0)])
    # pulse / tense layer / fades are computed per 60 s block (float64 time) so long films stay within memory
    mood = [1.0 if sc.get('mood') == 'tense' else 0.0 for sc in st['scenes']]
    mk = [(0, mood[0])] + [p for i in range(1, N) for p in ((S[f'S{i}']['s'], mood[i - 1]), (S[f'S{i}']['s'] + 3, mood[i]))] + [(total, mood[-1])]
    mkt = [k[0] for k in mk]; mkv = [k[1] for k in mk]; anyten = max(mkv) > 0
    fi = max(.05, float(json.load(open(f'{root}/story.json'))['meta'].get('fadein', 4))); ph0 = 0.0
    for b0 in range(0, n, BL):
        b1 = min(n, b0 + BL); tb = np.arange(b0, b1) / sr; ib = inten[b0:b1].astype(np.float64)
        fr = ph0 + np.cumsum((50 + 22 * ib) / 60 / sr); ph0 = float(fr[-1]); fr = fr % 1.0
        pulse = np.sin(2 * np.pi * 52 * tb) * np.exp(-fr * 9) * np.clip((ib - .42) / .4, 0, 1) * np.clip(tb / 30, 0, 1) * .32
        P = pad[b0:b1].astype(np.float64); PR = padR[b0:b1].astype(np.float64); G = ping[b0:b1].astype(np.float64); GR = pingR[b0:b1].astype(np.float64)
        if anyten:
            ten = np.interp(tb, mkt, mkv); trem = .75 + .25 * np.sin(2 * np.pi * .13 * tb)
            drone = sum(np.sin(2 * np.pi * hz(m_) * tb + ph) * a_ for m_, ph, a_ in ((38, 0, .5), (44, 1.3, .36), (39, 2.1, .22), (50, .7, .16))) * trem * ten * .26
            beat = (tb * 56 / 60) % 1.0
            thump = (np.sin(2 * np.pi * 46 * tb) * (np.exp(-beat * 16) + .55 * np.exp(-np.clip(beat - .3, 0, 9) * 18) * (beat > .3))) * ten * .34
            hi = (np.sin(2 * np.pi * hz(74) * tb) + np.sin(2 * np.pi * hz(75) * tb + 1)) * (.5 + .5 * np.sin(2 * np.pi * .07 * tb)) * ten * .018
            P = P * (1 - .45 * ten) + drone + hi; PR = PR * (1 - .45 * ten) + drone * .92 + hi; G = G * (1 - .85 * ten); GR = GR * (1 - .85 * ten); pulse = pulse * (1 - ten) + thump
        fade = np.clip(tb / fi, 0, 1) * np.clip((D['total'] - tb) / fo, 0, 1)
        pad[b0:b1] = ((P + G + pulse) * fade).astype(np.float32); padR[b0:b1] = ((PR + GR + pulse) * fade).astype(np.float32)
    Lc, Rc = pad, padR; del ping, pingR
    if float(_m.get('ambience', 1.0)) > 0:
        from . import sound
        _a = sound.ambience(sound.curves(root, D), n, t, np.random.default_rng(8), float(_m.get('ambience', 1.0))) * float(max(abs(Lc).max(), abs(Rc).max())) * 6; Lc = Lc + _a[0]; Rc = Rc + _a[1]
    m = float(max(abs(Lc).max(), abs(Rc).max())); out = out or f'{root}/build/music.wav'
    with wave.open(out, 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr)
        for b0 in range(0, n, BL):
            x = np.stack([Lc[b0:b0 + BL], Rc[b0:b0 + BL]], 1) / m * .7; w.writeframes((np.clip(x, -1, 1) * 32767).astype('<i2').tobytes())
    return out



def typing_events(root, D, t0, tot):
    """(time, char) for every character of a typed `txt` world node, so the keys can be heard."""
    from .spec import resolve, cue_times
    S = D['sched']; ev = []
    for c in D.get('cues', []):
        if c.get('a') != 'world': continue
        try: cs, ce = cue_times(c, S)
        except Exception: continue
        for n in c.get('p', {}).get('nodes', []):
            if n.get('kind') != 'txt' or not n.get('type') or n.get('silent'): continue
            T = lambda v: (cs + float(v)) if isinstance(v, (int, float)) else resolve(v, S)
            ta = T(n.get('at', 0)); te = T(n['until']) + .45 if n.get('until') is not None else ce
            txt = n.get('text', '')
            for k, ch in enumerate(txt):
                tt = ta + (k + 1) / n['type']
                if tt < te and t0 <= tt < t0 + tot: ev.append((tt - t0, ch))
    return ev


def typing_wav(ev, tot, path, sr=44100):
    """soft, muted keystrokes: short low-passed thud with a gentle attack (no sharp click or hiss)."""
    rng = np.random.default_rng(7); y = np.zeros(int((tot + 1) * sr), dtype=np.float32)
    def lp(x, fc):  # one-pole low-pass
        a = np.exp(-2 * np.pi * fc / sr); o = np.empty_like(x); z = 0.0
        for k in range(len(x)): z = (1 - a) * x[k] + a * z; o[k] = z
        return o
    for t, ch in ev:
        i = int(t * sr); L = int(.045 * sr); x = np.arange(L) / sr
        f = rng.uniform(110, 150) * (.8 if ch == ' ' else 1)
        body = np.sin(2 * np.pi * f * x) * np.exp(-x * 75)                       # soft low thud
        tick = lp(rng.standard_normal(L), 1800) * np.exp(-x * 160) * .35         # muffled tick, no hiss
        w = (body + tick) * np.minimum(1, x / .003) * (1.0 if ch != ' ' else 1.15) * rng.uniform(.75, 1.0)
        y[i:i + L] += w.astype(np.float32)
    y = np.clip(y * .6, -1, 1); import wave
    with wave.open(path, 'wb') as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes((y * 32767).astype('<i2').tobytes())
    return path


def mux(root, audio_dir='audio', out=None, music_only=False, burn=False, music_db=None, video=None, scenes=None, log=print):
    b = f'{root}/build'; D = json.load(open(f'{b}/data.json')); S = D['sched']; beats = json.load(open(f'{b}/beats.json'))
    t0, tot = 0.0, D['total']
    if scenes is not None: t0, tot = S[f'S{scenes[0]}']['s'], S[f'E{scenes[-1]}']['s'] - S[f'S{scenes[0]}']['s']; beats = [x for x in beats if t0 - .01 <= S[x['id']]['s'] < t0 + tot]
    video = video or (f'{b}/video_range.mp4' if scenes is not None else f'{b}/video_silent.mp4'); out = out or (f'{b}/final_scenes_{scenes[0]}-{scenes[-1]}.mp4' if scenes is not None else f'{b}/final.mp4'); ad = os.path.join(root, audio_dir)
    files = [] if music_only else [(x['id'], f"{ad}/beats/{x['id']}.mp3") for x in beats if os.path.exists(f"{ad}/beats/{x['id']}.mp3")]
    if not music_only and len(files) < len(beats): log(f'warning: {len(files)}/{len(beats)} narration files found')
    cmd = ['ffmpeg', '-y', '-loglevel', 'error', '-i', video, '-ss', f'{t0:.2f}', '-i', f'{b}/music.wav']
    for _, f in files: cmd += ['-i', f]
    try: _meta = json.load(open(f'{root}/story.json'))['meta']
    except Exception: _meta = {}
    if music_db is None: music_db = float(_meta.get('music_db', -9))
    sfx_db = float(_meta.get('sfx_db', -14)); sfx_i = None
    ev = typing_events(root, D, t0, tot) if _meta.get('typing_sound') else []; tk = None
    if ev and files: tk = 2 + len(files); cmd += ['-i', typing_wav(ev, tot, f'{b}/typing.wav')]; log(f'typing sounds: {len(ev)} keys')
    n_in = 2 + len(files) + (1 if tk else 0)
    if _meta.get('sfx', True):
        from . import sound
        try: cmd += ['-i', sound.render_sfx(root, D, t0, tot, f'{b}/sfx.wav')]; sfx_i = n_in
        except Exception as e: log(f'warning: sfx skipped ({e})')
    fc = []
    if files:
        for k, (i, _) in enumerate(files):
            ms = int((S[i]['s'] - t0) * 1000); fc.append(f'[{k + 2}:a]adelay={ms}|{ms},apad[b{k}]')
        if tk: fc.append(f'[{tk}:a]volume=-20dB[ty]')
        fc += [''.join(f'[b{k}]' for k in range(len(files))) + (f'[ty]' if tk else '') + f'amix=inputs={len(files) + (1 if tk else 0)}:normalize=0:duration=longest[nar0]', '[nar0]asplit=2[nar][sc]', f'[1:a]volume={music_db}dB[mu]',
               f"[mu][sc]sidechaincompress=threshold={_meta.get('duck_threshold', .04)}:ratio={_meta.get('duck_ratio', 2.5)}:attack=40:release=900[duck]"] + ([f'[{sfx_i}:a]volume={sfx_db}dB[sfx]', '[nar][duck][sfx]amix=inputs=3:normalize=0:duration=longest,loudnorm=I=-16:TP=-1.5:LRA=11[aout0]'] if sfx_i is not None else ['[nar][duck]amix=inputs=2:normalize=0:duration=longest,loudnorm=I=-16:TP=-1.5:LRA=11[aout0]'])
    else: fc.append(f'[1:a]volume={music_db + 4}dB,loudnorm=I=-20:TP=-1.5[aout0]')
    fo = float(json.load(open(f'{root}/story.json'))['meta'].get('fadeout', 4))   # fade to silence at the very end
    fc.append(f"[aout0]afade=t=out:st={max(0, tot - fo):.2f}:d={fo}[aout]")
    vf = ['-vf', f"subtitles={b}/captions.srt:force_style='FontSize=20,Outline=1,Shadow=0,MarginV=36'", '-c:v', 'libx264', '-crf', '18', '-preset', 'fast'] if burn else ['-c:v', 'copy']
    cmd += ['-filter_complex', ';'.join(fc), '-map', '0:v', '-map', '[aout]'] + vf + ['-c:a', 'aac', '-b:a', '192k', '-t', str(tot), '-movflags', '+faststart', out]
    subprocess.run(cmd, check=True); log(f'wrote {out}'); return out
