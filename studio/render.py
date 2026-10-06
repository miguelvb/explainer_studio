"""Frame-exact rendering (Playwright + ffmpeg), preview contact sheets and the deep probe."""
import asyncio, json, os, subprocess, time, glob
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


async def _page(b, url, D, W):
    H = W * 9 // 16
    pg = await b.new_page(viewport={'width': W, 'height': H})
    errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)))
    await pg.goto(url)
    await pg.evaluate(f"document.getElementById('stage').style.transform='scale({W / 1920})'")
    return pg, errs


def _scene_hash(root, D, n, w, fps, limit, preset, crf):
    import hashlib, glob as _g
    S = D['sched']; t0, t1 = S[f'S{n}']['s'], S[f'E{n}']['s']; h = hashlib.sha1()
    h.update(json.dumps([t0, t1, w, fps, limit, preset, crf, D.get('fps')], sort_keys=True).encode())
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

    async def one(br, n):
        t0, t1 = S[f'S{n}']['s'], S[f'E{n}']['s']
        f0, f1 = round(t0 * fps), round(t1 * fps)
        if limit: f1 = min(f1, f0 + int(limit * fps))
        out = f'{b}/video/scene_{n}.mp4'; hf = out + '.hash'; hh = _scene_hash(root, D, n, w, fps, limit, preset, crf)
        if not force and os.path.exists(out) and os.path.exists(hf) and open(hf).read() == hh: return n, -1
        pg, errs = await _page(br, url, D, w)
        await pg.evaluate('(d)=>setup(d.sched,d.cues)', D)
        ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', str(fps), '-c:v', 'mjpeg', '-i', '-',
                               '-c:v', 'libx264', '-preset', preset, '-crf', str(crf), '-pix_fmt', 'yuv420p', out], stdin=subprocess.PIPE)
        for f in range(f0, f1):
            await pg.evaluate(f'frame({f / fps})')
            ff.stdin.write(await pg.screenshot(type='jpeg', quality=94))
        ff.stdin.close(); ff.wait(); await pg.close(); open(hf, 'w').write(hh)
        return n, f1 - f0

    async def main():
        scenes_ = list(scenes) if scenes is not None else ([scene] if scene is not None else list(range(N))); t = time.time(); sem = asyncio.Semaphore(workers)
        async with async_playwright() as p:
            br = await _launch(p)
            async def go(n):
                async with sem:
                    r = await one(br, n); log(f'scene {r[0]} unchanged, reused' if r[1] < 0 else f'scene {r[0]} done: {r[1]} frames, {time.time() - t:.0f}s'); return r
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
            await pg.evaluate('(d)=>setup(d.sched,d.cues)', D)
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


PROBE = """(a)=>{const out=[];const [sched,cues,total]=a;
 for(let i=0;i<cues.length;i++){const c=cues[i];
  try{setup(sched,[c]);const q=window.CUES[0];const ts=[];for(let t=q.start+.05;t<q.end;t+=Math.max(.5,(q.end-q.start)/14))ts.push(t);ts.push(q.end-.05,q.end+1);
   window.__fit=[];for(const t of ts)frame(t);const seen=new Set();for(const f of window.__fit){const k=f.id+f.t;if(seen.has(k))continue;seen.add(k);out.push({i,msg:'text '+f.how+' to fit its container: "'+f.t+'" (node '+f.id+')',warn:f.how!=='hidden'})}
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
            await pg.evaluate('(d)=>setup(d.sched,d.cues)', D)
            t = 0.5
            while t < D['total'] - .3:
                await pg.evaluate(f'frame({t})')
                im = Image.open(io.BytesIO(await pg.screenshot(type='png'))).convert('L')
                if ImageStat.Stat(im).stddev[0] < thresh: out.append(round(t, 1))
                t += step
            await br.close()
        return out
    return asyncio.run(main())
