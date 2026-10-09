# Film definition: `meta` of story.json and the pronunciation table.
# Narration lives in script.md and the scenes in scenes/sNN.py (see studio/storykit.py).
META = dict(
    title='¿Hay alguien ahí dentro?', lang='es',
    provider='elevenlabs', el_voice='cristina', el_model='eleven_v4', el_speed=0.95, el_stability=0.5,
    music_style='mix', music_db=-8, sfx_db=-12, duck_ratio=2.5, duck_threshold=0.04, ambience=1.0,
    background='grid4', bg_speed=3, fadein=0.3,
)
PRONUNCIATION = {}
# English names said in English (untested: try them with `voices` before the full TTS run)
EL_PRONUNCIATION = {'Anthropic': 'Anzrópic', 'Claude': 'Clod', 'Chalmers': 'Chálmers', 'Berkeley': 'Bérkli',
                    'Othello': 'Otelo', 'Hofstadter': 'Jófstater', 'Severance': 'Séverans', 'Locke': 'Lok',
                    'Jankis': 'Yánkis', 'Seth': 'Sez', 'embedding': 'embéding', 'J-space': 'yei espeis'}
META['el_pronunciation'] = EL_PRONUNCIATION

# Sammy (the AI that writes the e-mail and the blog entry) speaks with his own male voice: set SAMMY_VOICE once chosen
# (try candidates with: python explainer.py voices -p examples/ia-consciencia-es --model eleven_v4 --el jacobo,carlos,mateo --text "<first sentence>")
SAMMY_VOICE = 'jacobo'
SAMMY_BEATS = [f'1{c}' for c in 'hijklmnopq'] + ['8l', '8m', '8n']
if SAMMY_VOICE: META['el_voice_by_beat'] = {b: SAMMY_VOICE for b in SAMMY_BEATS}
