"""Frame-exact rendering (Playwright + ffmpeg), preview contact sheets and the deep probe."""
import asyncio, json, os, subprocess, time, glob, sys, shutil
from playwright.async_api import async_playwright

CHROMIUM_FALLBACK = os.environ.get('CHROMIUM_PATH', '/opt/pw-browsers/chromium')


async def _launch(p):
    try:
        return await p.chromium.launch()
    except Exception:
        return await p.chromium.launch(executable_path=CHROMIUM_FALLBACK)


def _paths(root):
    b = os.path.join(root, 'build')
    return b, json.load(open(f'{b}/data.json')), 'file://' + os.path.abspath(f'{b}/player/index.html')


SIG = """window.__sig=()=>{const st=document.getElementById('stage');if(st.querySelector('canvas'))return Math.random();
 const s=st.innerHTML;let h1=0xdeadbeef,h2=0x41c6ce57;for(let i=0;i<s.length;i++){const c=s.charCodeAt(i);h1=Math.imul(h1^c,2654435761);h2=Math.imul(h2^c,1597334677)}
 h1=Math.imul(h1^(h1>>>16),2246822507)^Math.imul(h2^(h2>>>13),3266489909);return (h1>>>0)+':'+s.length}"""


async def _page(b, url, D, W):
    H = W * 9 // 16
    pg = await b.new_page(viewport={'width': W, 'height': H})
    errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)))
    await pg.goto(url)
    await pg.evaluate(SIG)
    await pg.evaluate("Promise.all([document.fonts.load('16px \"Press Start 2P\"'),document.fonts.load('16px \"Share Tech Mono\"')]).then(()=>document.fonts.ready)")
    await pg.evaluate(f"document.getElementById('stage').style.transform='scale({W / 1920})'")
    return pg, errs


def _scene_hash(root, D, n, w, fps, limit, preset, crf):
    import hashlib, glob as _g
    S = D['sched']; t0, t1 = S[f'S{n}']['s'], S[f'E{n}']['s']; h = hashlib.sha1()
    h.update(json.dumps([t0, t1, w, fps, limit, preset, crf, D.get('fps'), D.get('bg')], sort_keys=True).encode())
    from .spec import cue_times
    def ov(c):
        try: cs, ce = cue_times(c, S); return ce > t0 - .5 and cs < t1 + .5
        except Exception: return True
    h.update(json.dumps([c for c in D['cues'] if ov(c)], sort_keys=True, default=str).encode())
    for f in sorted(_g.glob(os.path.join(os.path.dirname(__file__), 'player', '*'))):
        if os.path.isfile(f): h.update(open(f, 'rb').read())
    return h.hexdigest()[:16]


def render(root, w=1280, fps=30, scene=None, workers=2, limit=0, scenes=None, draft=False, force=False, log=print):
    """draft=True: smaller, 20 fps, ultrafast encode. Unchanged scenes (same cues/player/size) are reused unless force."""
    b, D, url = _paths(root); S = D['sched']; N = D['scenes']
    if draft: w, fps = min(w, 854), 20
    preset, crf = ('ultrafast', 26) if draft else ('fast', 17)
    os.makedirs(f'{b}/video', exist_ok=True)

    PR = dict(total=0, done=0, scenes=0, sdone=0, active=set(), t=time.time(), last=0.0)

    def _fr(n):
        f0, f1 = round(S[f'S{n}']['s'] * fps), round(S[f'E{n}']['s'] * fps)
        return f0, (min(f1, f0 + int(limit * fps)) if limit else f1)

    def _fmt(x): x = int(max(0, x)); return f'{x // 3600}:{x % 3600 // 60:02d}:{x % 60:02d}' if x >= 3600 else f'{x // 60}:{x % 60:02d}'

    def _progress(force=False):
        now = time.time()
        if not force and now - PR['last'] < (2 if sys.stdout.isatty() else 20): return
        PR['last'] = now; el = now - PR['t']; d, T = PR['done'], max(1, PR['total']); rate = d / el if el > 1 else 0
        eta = (T - d) / rate if rate else 0
        msg = f"  progreso {100 * d / T:5.1f}%  escenas {PR['sdone']}/{PR['scenes']}  frames {d}/{T}  transcurrido {_fmt(el)}  falta ~{_fmt(eta) if rate else '?'}  total est. ~{_fmt(el + eta + EXTRA['s']) if rate else '?'} (con música+mux ~{_fmt(EXTRA['s'])})  {rate:.1f} fps  en curso: {','.join(str(a) for a in sorted(PR['active']))}"
        if sys.stdout.isatty(): sys.stdout.write('\r' + msg[:shutil.get_terminal_size((160, 20)).columns - 1].ljust(shutil.get_terminal_size((160, 20)).columns - 1)); sys.stdout.flush()
        else: log(msg)

    async def one(br, n):
        f0, f1 = _fr(n)
        out = f'{b}/video/scene_{n}.mp4'; hf = out + '.hash'; hh = _scene_hash(root, D, n, w, fps, limit, preset, crf)
        if not force and os.path.exists(out) and os.path.exists(hf) and open(hf).read() == hh: return n, -1
        PR['active'].add(n)
        pg, errs = await _page(br, url, D, w)
        await pg.evaluate('(d)=>{window.BGCFG=d.bg;setup(d.sched,d.cues)}', D)
        ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', str(fps), '-c:v', 'mjpeg', '-i', '-',
                               '-c:v', 'libx264', '-preset', preset, '-crf', str(crf), '-pix_fmt', 'yuv420p', out], stdin=subprocess.PIPE)
        last, img, reused = None, b'', 0
        for f in range(f0, f1):
            sig = await pg.evaluate(f'(()=>{{frame({f / fps});return window.__sig()}})()')   # one round trip: draw + state signature
            if sig != last or not img or os.environ.get('NODEDUP'): img = await pg.screenshot(type='jpeg', quality=94); last = sig
            else: reused += 1                                                              # identical DOM state -> identical picture: skip the screenshot
            ff.stdin.write(img); PR['done'] += 1; _progress()
        ff.stdin.close(); ff.wait(); await pg.close(); open(hf, 'w').write(hh); PR['active'].discard(n); PR['sdone'] += 1
        None
        return n, f1 - f0

    async def main():
        scenes_ = list(scenes) if scenes is not None else ([scene] if scene is not None else list(range(N))); t = time.time(); sem = asyncio.Semaphore(workers)
        todo = [n for n in scenes_ if force or not (os.path.exists(f'{b}/video/scene_{n}.mp4') and os.path.exists(f'{b}/video/scene_{n}.mp4.hash') and open(f'{b}/video/scene_{n}.mp4.hash').read() == _scene_hash(root, D, n, w, fps, limit, preset, crf))]
        PR.update(total=sum(_fr(n)[1] - _fr(n)[0] for n in todo), scenes=len(todo), t=time.time()); log(f'  a renderizar: {len(todo)} escenas, {PR["total"]} frames ({w}px, {fps} fps, {workers} workers); el resto se reutiliza')
        async with async_playwright() as p:
            br = await _launch(p)
            async def go(n):
                async with sem:
                    r = await one(br, n)
                    if sys.stdout.isatty(): sys.stdout.write('\r' + ' ' * (shutil.get_terminal_size((160, 20)).columns - 1) + '\r')
                    log(f'scene {r[0]} unchanged, reused' if r[1] < 0 else f'scene {r[0]} done: {r[1]} frames, {_fmt(time.time() - t)}'); _progress(True); return r
            await asyncio.gather(*[go(n) for n in scenes_]); await br.close()
    asyncio.run(main())
    if scenes is not None:
        with open(f'{b}/video/list_range.txt', 'w') as f:
            for n in scenes: f.write(f"file 'scene_{n}.mp4'\n")
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', f'{b}/video/list_range.txt', '-c', 'copy', f'{b}/video_range.mp4'], check=True)
        log(f'wrote {b}/video_range.mp4')
    elif scene is None:
        with open(f'{b}/video/list.txt', 'w') as f:
            for n in range(N): f.write(f"file 'scene_{n}.mp4'\n")
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', f'{b}/video/list.txt', '-c', 'copy', f'{b}/video_silent.mp4'], check=True)
        log(f'wrote {b}/video_silent.mp4')


def preview(root, scene=None, step=6.0, w=640, times=None, log=print):
    """Screenshots every `step` seconds (or at `times`) + a contact sheet build/preview/sheet.png (needs Pillow)."""
    b, D, url = _paths(root); S = D['sched']; os.makedirs(f'{b}/preview', exist_ok=True)
    for f in glob.glob(f'{b}/preview/*.png'): os.remove(f)
    if times is None:
        sc = [scene] if scene is not None else range(D['scenes']); times = []
        for n in sc:
            t = S[f'S{n}']['s'] + .5
            while t < S[f'E{n}']['s'] - .2: times.append(round(t, 2)); t += step
    async def main():
        async with async_playwright() as p:
            br = await _launch(p); pg, errs = await _page(br, url, D, w)
            await pg.evaluate('(d)=>{window.BGCFG=d.bg;setup(d.sched,d.cues)}', D)
            for t in times:
                await pg.evaluate(f'frame({t})'); await pg.screenshot(path=f'{b}/preview/{t:08.2f}.png')
            await br.close(); return errs
    errs = asyncio.run(main())
    try:
        from PIL import Image, ImageDraw
        fs = sorted(glob.glob(f'{b}/preview/0*.png')); cols = 4; tw = 480; th = tw * 9 // 16
        rows = (len(fs) + cols - 1) // cols; sh = Image.new('RGB', (cols * tw, rows * (th + 18)), '#000')
        d = ImageDraw.Draw(sh)
        for i, f in enumerate(fs):
            im = Image.open(f).resize((tw, th)); x, y = i % cols * tw, i // cols * (th + 18)
            sh.paste(im, (x, y + 18)); d.text((x + 4, y + 3), f'{float(os.path.basename(f)[:-4]):.1f}s', fill='#9fb')
        sh.save(f'{b}/preview/sheet.png'); log(f'{len(fs)} frames -> {b}/preview/sheet.png')
    except ImportError:
        log(f'{len(times)} frames in {b}/preview/ (install Pillow for a contact sheet)')
    return errs


EXTRA = {'s': 0.0}      # seconds of work after the frames (music + mux), added to the estimates; set by explainer.py all


PROBE = """(a)=>{const out=[];const [sched,cues,total]=a;
 for(let i=0;i<cues.length;i++){const c=cues[i];
  try{setup(sched,[c]);const q=window.CUES[0];const ts=[];for(let t=q.start+.05;t<q.end;t+=Math.max(.5,(q.end-q.start)/14))ts.push(t);ts.push(q.end-.05,q.end+1);
   window.__fit=[];window.__lk=[];for(const t of ts)frame(t);const seen=new Set();for(const f of window.__fit){const k=f.id+f.t;if(seen.has(k))continue;seen.add(k);out.push({i,msg:'text '+f.how+' to fit its container: "'+f.t+'" (node '+f.id+')',warn:f.how!=='hidden'})}const sk=new Set();for(const f of (window.__lk||[])){const k=f.a+f.b;if(sk.has(k))continue;sk.add(k);out.push({i,msg:'link '+f.a+' -> '+f.b+' still crosses another node (no clear route found)',warn:true})}
   const st=document.querySelector('#stage .st[data-c]');
   if(st&&!st.textContent.trim()&&!st.querySelector('svg,canvas,i'))out.push({i,msg:'rendered nothing'});
   const el=document.querySelector('#stage .st');
   if(el){const r=el.scrollWidth>el.clientWidth+2||el.scrollHeight>el.clientHeight+2; if(r)out.push({i,msg:'content overflows its frame (too much text/items for this rect)',warn:true})}
  }catch(e){out.push({i,msg:String(e&&e.message||e)})}}
 return out}"""


def probe(root):
    """Instantiate every cue in a real browser at start/mid/end and report JS errors, empty output and overflow."""
    b, D, url = _paths(root)
    async def main():
        async with async_playwright() as p:
            br = await _launch(p); pg, errs = await _page(br, url, D, 1280)
            r = await pg.evaluate(PROBE, [D['sched'], D['cues'], D['total']])
            await br.close(); return r, errs
    return asyncio.run(main())


def blanks(root, step=1.0, thresh=2.0):
    """Frames sampled every `step` s; returns times where the picture is (almost) a flat colour = dead air."""
    from PIL import Image, ImageStat
    import io
    b, D, url = _paths(root); S = D['sched']
    async def main():
        out = []
        async with async_playwright() as p:
            br = await _launch(p); pg, _ = await _page(br, url, D, 320)
            await pg.evaluate('(d)=>{window.BGCFG=d.bg;setup(d.sched,d.cues)}', D)
            t = 0.5
            while t < D['total'] - .3:
                await pg.evaluate(f'frame({t})')
                im = Image.open(io.BytesIO(await pg.screenshot(type='png'))).convert('L')
                if ImageStat.Stat(im).stddev[0] < thresh: out.append(round(t, 1))
                t += step
            await br.close()
        return out
    return asyncio.run(main())
