# Film definition: `meta` of story.json and the pronunciation table.
# Narration lives in script.md and the scenes in scenes/sNN.py (see studio/storykit.py).
META = dict(
    title='Las matemáticas se aceleran: 722 teoremas de una IA', lang='es',
    provider='elevenlabs', el_voice='cristina', el_model='eleven_v4', el_speed=0.95, el_stability=0.5,
    music_style='mix', music_db=-8, sfx_db=-12, duck_ratio=2.5, duck_threshold=0.04, ambience=1.0,
    background='poly', fadein=0.3,
)
PRONUNCIATION = {}
EL_PRONUNCIATION = {'GPT-5.2': 'GPT cinco punto dos', 'GPT-5': 'GPT cinco'}
META['el_pronunciation'] = EL_PRONUNCIATION
