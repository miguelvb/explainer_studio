#!/usr/bin/env python3
"""Explainer Studio — PDF / text / script  ->  animated explainer video (assets only, deterministic, re-times to narration).

  python explainer.py ingest report.pdf  -p projects/mycase --minutes 10      # LLM drafts story.json (needs an API key)
  python explainer.py ingest script.txt  -p projects/mycase --mode script     # you already have the narration
  python explainer.py prompt --mode doc > prompt.md                           # the prompt, to use in any chat
  python explainer.py gen      -p examples/film                               # film.py + script.md + scenes/*.py -> story.json (the other commands do it first)
  python explainer.py validate -p projects/mycase                             # static + real-browser checks
  python explainer.py preview  -p projects/mycase --scene 3                   # contact sheet
  python explainer.py all      -p projects/mycase                             # build, tts, rebuild, music, render, mux
  python explainer.py record   -p projects/mycase take1.m4a take2.m4a         # your own voice: clean, reverb, normalise, one file per beat
"""
import argparse, json, os, sys, shutil
from studio import env, spec, llm, prompt, catalog, render, audio, storykit, record as recmod, mark as markmod

HERE = os.path.dirname(os.path.abspath(__file__))


def proj(a): return a.project or '.'
_GEN = set()
def story(a):
    root = proj(a)
    if os.path.exists(os.path.join(root, 'film.py')) and root not in _GEN:     # films built with storykit: story.json is always regenerated first
        _GEN.add(root); storykit.generate(root, log=lambda *x: None)
    return spec.load(os.path.join(root, 'story.json'))
def timings(a):
    p = os.path.join(proj(a), 'audio', 'timings.json')
    return json.load(open(p)) if os.path.exists(p) else None


def do_build(a, use_timings=True):
    st = story(a); T = timings(a) if use_timings else None
    r = spec.write_build(st, proj(a), T, pad=not a.no_pad)
    t = r['total']; print(f'{"real" if T else "estimated"} timings · total {int(t // 60)}:{t % 60:04.1f} · {r["beats"]} beats · {r["cues"]} cues')
    return st


def cmd_validate(a):
    st = story(a); E, W = spec.validate(st, timings(a))
    if not E:
        do_build(a); res, js = render.probe(proj(a))
        for r in res: (W if r.get('warn') else E).append(f'cue #{r["i"]}: {r["msg"]}')
        E += js
    for e in E: print('ERROR  ', e)
    for w in W: print('warning', w)
    if not E and a.blanks:
        b = render.blanks(proj(a))
        if b: print('warning flat/blank frames at:', b[:30])
    print(f'{len(E)} errors, {len(W)} warnings'); sys.exit(1 if E else 0)


def cmd_ingest(a):
    root = proj(a); os.makedirs(root, exist_ok=True)
    st, E, W = llm.ingest(a.source, root, a.provider, a.model, a.mode, a.minutes, a.title, a.audience, a.notes, a.lang, a.repair)
    for e in E: print('ERROR  ', e)
    for w in W[:20]: print('warning', w)
    print(f'wrote {root}/story.json  ({len(st["scenes"])} scenes). Next: validate · preview · tts · all')


def cmd_prompt(a):
    ex = llm.example_excerpt() if not a.no_example else None
    print(prompt.system_prompt(a.mode, ex))
    if a.with_user: print('\n---\n(USER MESSAGE TEMPLATE)\n' + prompt.user_prompt('<paste the document text or script here>', a.minutes))


def cmd_all(a):
    do_build(a, use_timings=False)
    sc = None
    if a.scene is not None: sc = [a.scene]
    elif a.first is not None or a.last is not None:
        n = len(story(a)['scenes']); f = a.first if a.first is not None else 0; l = a.last if a.last is not None else n - 1
        if not (0 <= f <= l < n): raise SystemExit(f'scene range must satisfy 0 <= from <= to <= {n - 1}')
        sc = list(range(f, l + 1))
    only = None
    if sc is not None:
        import re as _re; only = {b['id'] for b in json.load(open(f'{proj(a)}/build/beats.json')) if _re.fullmatch(r'(\d+)[a-z]', b['id']) and int(b['id'][:-1]) in sc}
    if not a.skip_tts: audio.tts(proj(a), story(a), voice=a.voice, only=only)
    do_build(a)
    import time as _t
    from studio import sound as snd
    D_ = json.load(open(f'{proj(a)}/build/data.json'))
    try: ms, nmiss = snd.estimate_music(proj(a), D_)
    except Exception: ms, nmiss = 0.0, 0
    S_ = D_['sched']; sel_ = (S_[f'E{sc[-1]}']['s'] - S_[f'S{sc[0]}']['s']) if sc else D_['total']
    mux_s = 3 + 0.35 * sel_ / 60
    render.EXTRA['s'] = ms + mux_s
    print(f'  estimación de pasos posteriores al render: música ~{int(ms)} s' + (f' (incluye sintetizar {nmiss} bucles nuevos, solo esta vez)' if nmiss else '') + f' · mux ~{int(mux_s)} s')
    render.render(proj(a), a.w, 30, scenes=sc, workers=a.workers, limit=a.limit, draft=a.draft, force=a.force_render)
    t0 = _t.time(); print('  música…'); audio.music(proj(a)); print(f'  música lista en {int(_t.time() - t0)} s (estimado ~{int(ms)} s)')
    t0 = _t.time(); print('  mux…'); audio.mux(proj(a), burn=a.burn, music_only=a.skip_tts, scenes=sc); print(f'  mux listo en {int(_t.time() - t0)} s (estimado ~{int(mux_s)} s)')


def main():
    env.load()
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest='cmd', required=True)
    def P(name, f, **kw):
        p = sp.add_parser(name, **kw); p.add_argument('-p', '--project'); p.set_defaults(f=f); return p
    p = P('new', lambda a: (os.makedirs(a.project, exist_ok=True), shutil.copy(f'{HERE}/examples/mars-orbiter/story.json', f'{a.project}/story.json'), print('created', a.project, '(a copy of the demo story to edit)'))); 
    p = P('ingest', cmd_ingest); p.add_argument('source'); p.add_argument('--provider', default=None, choices=['anthropic', 'openai', 'openrouter', 'mock'])
    p.add_argument('--model'); p.add_argument('--mode', default='doc', choices=['doc', 'script']); p.add_argument('--minutes', type=float, default=10)
    p.add_argument('--title'); p.add_argument('--audience'); p.add_argument('--notes'); p.add_argument('--lang', default='en'); p.add_argument('--repair', type=int, default=3)
    p = sp.add_parser('prompt'); p.set_defaults(f=cmd_prompt); p.add_argument('--mode', default='doc', choices=['doc', 'script']); p.add_argument('--no-example', action='store_true'); p.add_argument('--with-user', action='store_true'); p.add_argument('--minutes', type=float, default=10)
    p = P('validate', cmd_validate); p.add_argument('--blanks', action='store_true')
    p = P('newfilm', lambda a: (storykit.new_film(proj(a), a.title), print('created', proj(a), '- edit script.md and scenes/, then: gen · validate · preview · all'))); p.add_argument('--title', default='Nueva película')
    P('gen', lambda a: (storykit.generate(proj(a)), print('wrote', os.path.join(proj(a), 'story.json'))))
    p = P('build', lambda a: do_build(a)); p.add_argument('--no-pad', action='store_true'); p.add_argument('--estimate', action='store_true')
    P('script', lambda a: (do_build(a), print('wrote', os.path.join(proj(a), 'script.md'))))
    p = P('preview', lambda a: print(render.preview(proj(a), a.scene, a.step) or 'ok')); p.add_argument('--scene', type=int); p.add_argument('--step', type=float, default=6)
    p = P('voices', lambda a: audio.voices(proj(a), story(a), text=a.text, el_model=a.model, el_voices=a.el.split(',') if a.el else None, openai_voices=a.oa.split(',') if a.oa else None)); p.add_argument('--text'); p.add_argument('--model', help='ElevenLabs model id, e.g. eleven_v4'); p.add_argument('--el', help='comma list of ElevenLabs voices'); p.add_argument('--oa', help='comma list of OpenAI voices')
    p = P('tts', lambda a: audio.tts(proj(a), story(a), voice=a.voice, only=set(a.only.split(',')) if a.only else None, force=a.force)); p.add_argument('--voice'); p.add_argument('--only'); p.add_argument('--force', action='store_true')
    def crec(a):
        if a.clear: return recmod.clear(proj(a))
        if not a.files: raise SystemExit('faltan las grabaciones')
        do_build(a, use_timings=False)
        sc = [a.scene] if a.scene is not None else (list(range(a.first, a.last + 1)) if a.first is not None and a.last is not None else None)
        recmod.record(proj(a), a.files, scenes=sc, model=a.model, reverb=a.reverb, lufs=a.lufs, lang=story(a)['meta'].get('lang', 'es'))
    p = P('record', crec); p.add_argument('files', nargs='*', help='one or more recordings, in reading order'); p.add_argument('--scene', type=int); p.add_argument('--from', dest='first', type=int); p.add_argument('--to', dest='last', type=int)
    p.add_argument('--model', default='small', help='faster-whisper model'); p.add_argument('--reverb', type=float, default=0.07, help='0 = none'); p.add_argument('--lufs', type=float, default=-18); p.add_argument('--clear', action='store_true')
    P('music', lambda a: print(audio.music(proj(a))))
    p = P('render', lambda a: render.render(proj(a), a.w, 30, a.scene, a.workers, a.limit, draft=a.draft)); p.add_argument('--w', type=int, default=1280); p.add_argument('--scene', type=int); p.add_argument('--workers', type=int, default=max(2, (os.cpu_count() or 4) - 2)); p.add_argument('--limit', type=float, default=0); p.add_argument('--draft', action='store_true')
    p = P('mux', lambda a: audio.mux(proj(a), music_only=a.music_only, burn=a.burn)); p.add_argument('--music-only', action='store_true'); p.add_argument('--burn', action='store_true')
    p = P('all', cmd_all); p.add_argument('--scene', type=int, help='only this scene'); p.add_argument('--from', dest='first', type=int, help='first scene of a range'); p.add_argument('--to', dest='last', type=int, help='last scene of a range (inclusive); gives build/final_scenes_A-B.mp4'); p.add_argument('--w', type=int, default=1280); p.add_argument('--workers', type=int, default=max(2, (os.cpu_count() or 4) - 2)); p.add_argument('--limit', type=float, default=0); p.add_argument('--skip-tts', action='store_true'); p.add_argument('--voice'); p.add_argument('--burn', action='store_true'); p.add_argument('--no-pad', action='store_true'); p.add_argument('--draft', action='store_true', help='fast preview render: 854px, 20fps, ultrafast'); p.add_argument('--force-render', action='store_true', help='re-render even unchanged scenes')
    def cv(a):
        r = llm.verify(proj(a), a.provider, a.model, a.source); print(json.dumps(r, indent=1, ensure_ascii=False)); print('saved verify.json')
    p = P('verify', cv); p.add_argument('--provider', default=None, choices=['anthropic', 'openai', 'openrouter']); p.add_argument('--model'); p.add_argument('--source', help='PDF or text the story was made from (cached as source.txt)')
    p = sp.add_parser('mark'); p.set_defaults(f=lambda a: print('wrote', markmod.make(a.logo, a.out))); p.add_argument('logo'); p.add_argument('-o', '--out', default='mark.txt')
    p = sp.add_parser('catalog'); p.set_defaults(f=lambda a: print(prompt.catalog_md()))
    a = ap.parse_args()
    if not hasattr(a, 'no_pad'): a.no_pad = False
    a.f(a)


if __name__ == '__main__': main()
