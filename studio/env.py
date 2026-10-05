"""Reads .env files (never overrides variables already set in the shell). Search order, first found wins per variable:
<project>/.env, ./.env, <studio>/.env, ~/.env, ~/video_generator/.env
Recognised keys:
  OPENAI_API_KEY, OPENROUTER_API_KEY, ANTHROPIC_API_KEY
  OPENAI_TTS_MODEL (gpt-4o-mini-tts)  OPENAI_TTS_VOICE (marin)  OPENAI_TTS_SPEED (1.0)  OPENAI_TTS_INSTRUCTIONS
  STUDIO_LLM_PROVIDER (anthropic|openai|openrouter; default: first key found)  STUDIO_LLM_MODEL
  (or per provider: OPENROUTER_TEXT_MODEL / OPENAI_TEXT_MODEL / ANTHROPIC_MODEL)"""
import os, re

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_loaded = set()


def load(root=None):
    cands = [os.path.join(root, '.env')] if root else []
    cands += ['.env', os.path.join(HERE, '.env'), os.path.expanduser('~/.env'), os.path.expanduser('~/video_generator/.env')]
    for p in cands:
        p = os.path.abspath(p)
        if p in _loaded or not os.path.isfile(p): continue
        _loaded.add(p)
        for line in open(p, encoding='utf-8', errors='ignore'):
            m = re.match(r'\s*(?:export\s+)?([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.*?)\s*$', line)
            if not m or line.lstrip().startswith('#'): continue
            v = m.group(2)
            if v[:1] in '"\'' and v.count(v[0]) >= 2: v = v[1:v.index(v[0], 1)]
            else: v = re.sub(r'\s+#.*$', '', v)
            os.environ.setdefault(m.group(1), v)


def llm_defaults():
    """(provider, model) from env; provider auto-detected from available keys."""
    prov = os.environ.get('STUDIO_LLM_PROVIDER')
    if not prov:
        prov = next((p for p, k in (('anthropic', 'ANTHROPIC_API_KEY'), ('openrouter', 'OPENROUTER_API_KEY'), ('openai', 'OPENAI_API_KEY')) if os.environ.get(k)), 'anthropic')
    model = os.environ.get('STUDIO_LLM_MODEL') or os.environ.get({'openrouter': 'OPENROUTER_TEXT_MODEL', 'openai': 'OPENAI_TEXT_MODEL', 'anthropic': 'ANTHROPIC_MODEL'}[prov])
    return prov, model
