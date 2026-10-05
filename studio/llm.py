"""Provider-agnostic LLM calls (stdlib only) + ingest with validate/repair loop + fact-check pass + offline mock."""
import copy, json, os, re, subprocess, urllib.request, urllib.error
from . import spec, prompt

DEFAULTS = {'anthropic': 'claude-sonnet-5-5'}


def _post(url, headers, body, timeout=900):
    req = urllib.request.Request(url, json.dumps(body).encode(), {'content-type': 'application/json', **headers})
    try:
        return json.load(urllib.request.urlopen(req, timeout=timeout))
    except urllib.error.HTTPError as e:
        raise SystemExit(f'LLM HTTP {e.code}: {e.read().decode()[:500]}')


def _key(n):
    if not os.environ.get(n): raise SystemExit(f'{n} not set')
    return os.environ[n]


def chat(provider, model, system, messages, max_tokens=16000):
    """messages = [{'role','content'}]. Returns text."""
    model = model or DEFAULTS.get(provider)
    if not model: raise SystemExit(f'--model is required for provider "{provider}"')
    if provider == 'anthropic':
        k = _key('ANTHROPIC_API_KEY')
        r = _post('https://api.anthropic.com/v1/messages', {'x-api-key': k, 'anthropic-version': '2023-06-01'}, {'model': model, 'max_tokens': max_tokens, 'system': system, 'messages': messages})
        return ''.join(b.get('text', '') for b in r['content'])
    base, key = {'openai': ('https://api.openai.com/v1', 'OPENAI_API_KEY'), 'openrouter': ('https://openrouter.ai/api/v1', 'OPENROUTER_API_KEY')}[provider]
    k = _key(key)
    r = _post(base + '/chat/completions', {'authorization': 'Bearer ' + k}, {'model': model, 'messages': [{'role': 'system', 'content': system}] + messages, 'max_tokens': max_tokens})
    return r['choices'][0]['message']['content']


def extract_json(t):
    t = re.sub(r'^```(?:json)?|```$', '', t.strip(), flags=re.M)
    a, b = t.find('{'), t.rfind('}')
    if a < 0 or b < 0: raise ValueError('no JSON object in reply')
    return json.loads(t[a:b + 1])


def read_source(path, max_chars=180000):
    if path.lower().endswith('.pdf'):
        try:
            txt = subprocess.check_output(['pdftotext', '-layout', path, '-'], stderr=subprocess.DEVNULL).decode('utf-8', 'ignore')
        except Exception:
            from pypdf import PdfReader
            txt = '\n'.join((p.extract_text() or '') for p in PdfReader(path).pages)
    else:
        txt = open(path, encoding='utf-8', errors='ignore').read()
    txt = re.sub(r'\n{3,}', '\n\n', txt).strip(); note = None
    if len(txt) > max_chars:
        txt = txt[:max_chars]; note = f'source truncated to {max_chars} characters'
    return txt, note


def example_excerpt():
    p = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'examples', 'mars-orbiter', 'story.json')
    if not os.path.exists(p): return None
    s = json.load(open(p)); s['scenes'] = s['scenes'][2:4]
    s['meta']['notes'] = '(excerpt: scenes 2-3 of a 6-scene demo)'
    return json.dumps(s, ensure_ascii=False, indent=1)


def check(story, root):
    """Static validation + real-browser probe. Returns (errors, warnings)."""
    E, W = spec.validate(story)
    if not E:
        from . import render
        spec.write_build(story, root)
        res, js = render.probe(root)
        for r in res:
            (W if r.get('warn') else E).append(f'cue #{r["i"]}: {r["msg"]}')
        E += [f'page error: {x}' for x in js]
    return E, W


def ingest(src, root, provider=None, model=None, mode='doc', minutes=10, title=None, audience=None, notes=None, lang='en', repair=3, log=print):
    from . import env; env.load(root)
    dp, dm = env.llm_defaults(); provider = provider or dp; model = model or (dm if provider == dp else None)
    log(f'llm provider={provider} model={model or DEFAULTS.get(provider)}')
    os.makedirs(root, exist_ok=True)
    text, trunc = read_source(src)
    if trunc: log('warning: ' + trunc)
    open(f'{root}/source.txt', 'w').write(text)
    sysmsg = prompt.system_prompt(mode, example_excerpt())
    msgs = [{'role': 'user', 'content': prompt.user_prompt(text, minutes, title, audience, notes, lang)}]
    data = story = None; E, W = [], []
    for rnd in range(repair + 1):
        if provider == 'mock': data = mock_story(text, minutes, title); raw = json.dumps(data)
        else:
            raw = chat(provider, model, sysmsg, msgs)
            try: data = extract_json(raw)
            except Exception as e:
                msgs += [{'role': 'assistant', 'content': raw}, {'role': 'user', 'content': f'Not valid JSON ({e}). Return only the corrected JSON object.'}]; continue
        data.setdefault('meta', {}).setdefault('minutes', minutes)
        try: story = spec.normalise(copy.deepcopy(data))
        except Exception as e:
            msgs += [{'role': 'assistant', 'content': raw}, {'role': 'user', 'content': f'Structure error: {e}. Return the corrected JSON.'}]; continue
        E, W = check(story, root)
        log(f'round {rnd}: {len(E)} errors, {len(W)} warnings')
        if not E or provider == 'mock': break
        msgs += [{'role': 'assistant', 'content': raw}, {'role': 'user', 'content': 'Fix these problems and return the complete corrected story.json (JSON only):\n- ' + '\n- '.join(E[:40] + W[:15])}]
    if data is None: raise SystemExit('LLM never returned valid JSON')
    json.dump(data, open(f'{root}/story.json', 'w'), indent=1, ensure_ascii=False)
    return story, E, W


def verify(root, provider=None, model=None, source=None, log=print):
    from . import env; env.load(root)
    dp, dm = env.llm_defaults(); provider = provider or dp; model = model or (dm if provider == dp else None)
    if source:
        txt, _ = read_source(source); os.makedirs(root, exist_ok=True); open(f'{root}/source.txt', 'w', encoding='utf-8').write(txt)
    src = open(f'{root}/source.txt', encoding='utf-8').read() if os.path.exists(f'{root}/source.txt') else None
    if not src: raise SystemExit('no source.txt in project: pass --source report.pdf (or run ingest first)')
    st = spec.load(f'{root}/story.json')
    raw = chat(provider, model, prompt.VERIFY, [{'role': 'user', 'content': prompt.verify_prompt(src, st)}], 8000)
    r = extract_json(raw); json.dump(r, open(f'{root}/verify.json', 'w'), indent=1, ensure_ascii=False)
    return r


def mock_story(text, minutes=10, title=None):
    """Offline draft: no LLM. Splits the text into scenes and rotates a few safe assets. Good for testing the pipeline."""
    sents = [s.strip() for s in re.split(r'(?<=[.!?])\s+', re.sub(r'\s+', ' ', text)) if len(s.split()) >= 6][:60]
    per = 3; chunks = [sents[i:i + per] for i in range(0, len(sents), per)][:8] or [['Nothing to narrate here yet.']]
    sc = []
    for n, ch in enumerate(chunks):
        last = len(ch) - 1; ids = [f'{n}{chr(97 + i)}' for i in range(len(ch))]
        cues = [{'a': 'title', 'at': f'S{n}', 'until': f'E{n}', 'p': {'kicker': 'DRAFT', 'title': (title or 'Untitled') if n == 0 else f'Part {n + 1}', 'sub': ch[0][:60]}}] if n == 0 else [
            {'a': ['list', 'quote', 'sequence'][n % 3], 'at': f'S{n}', 'until': f'E{n}',
             'p': ({'title': f'Part {n + 1}', 'items': [c[:60] for c in ch], 'at': 0.5} if n % 3 == 0 else
                   {'cards': [{'text': c, 'kind': 'par', 'at': i * 1.2} for i, c in enumerate(ch)]} if n % 3 == 1 else
                   {'items': [' '.join(c.split()[:4]) for c in ch], 'at': 0.5})}]
        sc.append({'title': f'Part {n + 1}', 'beats': ch, 'cues': cues})
    return {'meta': {'title': title or 'Draft', 'lang': 'en', 'minutes': minutes}, 'scenes': sc}
