"""TTS (OpenAI), synthesised music bed, final mux."""
import os, json, subprocess, wave
import numpy as np

DEFAULT_INSTR = ("Calm, measured documentary narrator. Neutral accent, clear diction, no hype and no drama. "
                 "Slightly slower than conversational pace, with a short natural pause at the end of every sentence. "
                 "Read names, codes and numbers slowly and clearly.")


def _dur(p):
    return float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', p]).strip())


def tts(root, st, model=None, voice=None, speed=None, only=None, force=False, log=print):
    """One MP3 per beat -> audio/beats/<id>.mp3 and audio/timings.json. Needs OPENAI_API_KEY (env or .env)."""
    from . import env; env.load(root)
    if 'OPENAI_API_KEY' not in os.environ: raise SystemExit('OPENAI_API_KEY not set (shell or .env)')
    from openai import OpenAI
    client = OpenAI(); m = st['meta']; E = os.environ
    model = model or E.get('OPENAI_TTS_MODEL', 'gpt-4o-mini-tts'); voice = voice or E.get('OPENAI_TTS_VOICE') or m.get('voice', 'marin')
    speed = float(speed or E.get('OPENAI_TTS_SPEED', 1.0)); instr = E.get('OPENAI_TTS_INSTRUCTIONS') or m.get('instructions', DEFAULT_INSTR)
    log(f'tts model={model} voice={voice} speed={speed}')
    pron = sorted(st.get('pronunciation', {}).items(), key=lambda kv: -len(kv[0]))
    def say(t):
        for k, v in pron: t = t.replace(k, v)
        return t
    beats = json.load(open(f'{root}/build/beats.json')); os.makedirs(f'{root}/audio/beats', exist_ok=True)
    tf = f'{root}/audio/timings.json'; T = json.load(open(tf)) if os.path.exists(tf) else {}
    for b in beats:
        i = b['id']
        if only and i not in only: continue
        p = f'{root}/audio/beats/{i}.mp3'
        if os.path.exists(p) and not force and i in T: continue
        log(f'tts {i}')
        with client.audio.speech.with_streaming_response.create(model=model, voice=voice, input=say(b['text']), instructions=instr, speed=speed, response_format='mp3') as r:
            r.stream_to_file(p)
        T[i] = round(_dur(p) + .12, 3); json.dump(T, open(tf, 'w'), indent=1)
    log(f'timings -> {tf}  narration {sum(T.values()):.0f}s')


def music(root, out=None):
    """Ambient pad + pulse shaped by each scene's `intensity` (0-1; default arc: builds to ~70% of the film, then eases)."""
    D = json.load(open(f'{root}/build/data.json')); S = D['sched']; N = D['scenes']; total = D['total'] + 6
    st = json.load(open(f'{root}/story.json')); ints = [sc.get('intensity') for sc in st['scenes']]
    arc = [.3 + .7 * (1 - abs(i / max(1, N - 1) - .7) / .7) if i / max(1, N - 1) <= .7 else 1 - (i / max(1, N - 1) - .7) / .3 * .6 for i in range(N)]
    ints = [x if x is not None else arc[i] for i, x in enumerate(ints)]
    sr = 44100; n = int(total * sr); t = np.arange(n, dtype=np.float32) / sr; rng = np.random.default_rng(7)
    keys = [(0, ints[0] * .8)] + [(S[f'S{i}']['s'] + 2, ints[i]) for i in range(N)] + [(total, 0)]
    inten = np.interp(t, [k[0] for k in keys], [k[1] for k in keys]).astype(np.float32)
    hz = lambda m: 440.0 * 2 ** ((m - 69) / 12)
    chords = [[38, 45, 53, 57, 60], [34, 46, 53, 58, 62], [43, 50, 53, 58, 62], [33, 45, 52, 57, 61]]; L = 32.0
    pad = np.zeros(n, np.float32); padR = np.zeros(n, np.float32)
    for ci, ch in enumerate(chords):
        k = np.arange(n) // int(L * sr); slot = (k % 4 == ci).astype(np.float32); w = int(10 * sr)
        cs = np.cumsum(np.concatenate([[0], slot])); env = (cs[w:] - cs[:-w]) / w
        env = np.concatenate([np.full(w // 2, env[0]), env, np.full(n - len(env) - w // 2, env[-1])])[:n].astype(np.float32)
        for note in ch:
            f = hz(note)
            for det, pan in ((-.07, 0), (.07, 1), (0, 2)):
                ph = rng.random() * 6.283; lfo = .65 + .35 * np.sin(2 * np.pi * (.03 + .01 * rng.random()) * t + rng.random() * 6.283)
                osc = np.sin(2 * np.pi * f * (1 + det * .01) * t + ph) + .35 * np.sin(2 * np.pi * 2 * f * (1 + det * .01) * t + ph * 1.3) + .12 * np.sin(2 * np.pi * 3 * f * t + ph)
                g = env * lfo * (.5 if note < 50 else .34) * (.45 + .55 * inten)
                if pan == 0: pad += osc * g
                elif pan == 1: padR += osc * g
                else: pad += osc * g * .6; padR += osc * g * .6
    ping = np.zeros(n, np.float32); pingR = np.zeros(n, np.float32); tt = 4.0
    while tt < total - 4:
        f = hz([74, 77, 79, 81, 84, 86][rng.integers(6)]); i0 = int(tt * sr); L2 = int(3.2 * sr); seg = t[:L2]
        bell = (np.sin(2 * np.pi * f * seg) + .4 * np.sin(2 * np.pi * f * 2.76 * seg)) * np.exp(-seg * 1.5); amp = .05 * (.3 + .7 * inten[min(n - 1, i0)]); e = min(n, i0 + L2)
        (ping if rng.random() < .5 else pingR)[i0:e] += bell[:e - i0] * amp
        tt += rng.uniform(3.5, 9.0) * (1.3 - .8 * inten[min(n - 1, i0)])
    bpm = 50 + 22 * inten; frac = np.cumsum(bpm / 60 / sr) % 1.0
    pulse = (np.sin(2 * np.pi * 52 * t) * np.exp(-frac * 9) * np.clip((inten - .42) / .4, 0, 1) * np.clip(t / 30, 0, 1) * .32).astype(np.float32)
    Lc = pad + ping + pulse; Rc = padR + pingR + pulse; fade = np.clip(t / 4, 0, 1) * np.clip((total - t) / 6, 0, 1); Lc *= fade; Rc *= fade
    m = max(abs(Lc).max(), abs(Rc).max()); st2 = np.stack([Lc / m * .7, Rc / m * .7], 1); out = out or f'{root}/build/music.wav'
    with wave.open(out, 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr); w.writeframes((np.clip(st2, -1, 1) * 32767).astype('<i2').tobytes())
    return out


def mux(root, audio_dir='audio', out=None, music_only=False, burn=False, music_db=-14, video=None, log=print):
    b = f'{root}/build'; D = json.load(open(f'{b}/data.json')); S = D['sched']; beats = json.load(open(f'{b}/beats.json'))
    video = video or f'{b}/video_silent.mp4'; out = out or f'{b}/final.mp4'; ad = os.path.join(root, audio_dir)
    files = [] if music_only else [(x['id'], f"{ad}/beats/{x['id']}.mp3") for x in beats if os.path.exists(f"{ad}/beats/{x['id']}.mp3")]
    if not music_only and len(files) < len(beats): log(f'warning: {len(files)}/{len(beats)} narration files found')
    cmd = ['ffmpeg', '-y', '-loglevel', 'error', '-i', video, '-i', f'{b}/music.wav']
    for _, f in files: cmd += ['-i', f]
    fc = []
    if files:
        for k, (i, _) in enumerate(files):
            ms = int(S[i]['s'] * 1000); fc.append(f'[{k + 2}:a]adelay={ms}|{ms},apad[b{k}]')
        fc += [''.join(f'[b{k}]' for k in range(len(files))) + f'amix=inputs={len(files)}:normalize=0:duration=longest[nar0]', '[nar0]asplit=2[nar][sc]', f'[1:a]volume={music_db}dB[mu]',
               '[mu][sc]sidechaincompress=threshold=0.015:ratio=9:attack=20:release=700[duck]', '[nar][duck]amix=inputs=2:normalize=0:duration=longest,loudnorm=I=-16:TP=-1.5:LRA=9[aout]']
    else: fc.append(f'[1:a]volume={music_db + 4}dB,loudnorm=I=-20:TP=-1.5[aout]')
    vf = ['-vf', f"subtitles={b}/captions.srt:force_style='FontSize=20,Outline=1,Shadow=0,MarginV=36'", '-c:v', 'libx264', '-crf', '18', '-preset', 'fast'] if burn else ['-c:v', 'copy']
    cmd += ['-filter_complex', ';'.join(fc), '-map', '0:v', '-map', '[aout]'] + vf + ['-c:a', 'aac', '-b:a', '192k', '-t', str(D['total']), '-movflags', '+faststart', out]
    subprocess.run(cmd, check=True); log(f'wrote {out}'); return out
