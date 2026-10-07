# Scene 8 · Créditos
MUSIC = {'bells': 1.0, 'pad': 0.6}
INTENSITY = 0.2
# the seal's own `links` property takes plain strings that the engine's link classifier cannot read, so the sources go in a small world cue (Share Tech Mono) over the seal
cues = [dict(a='seal', at='S8', until='E8', p=dict(text='Arkinos @ oct 2026', sub='Explainer Studio', scale=1.0, cy=150, ty=330, at=1.2,
             black=dict(at='8a#Explainer+9', dur=6)), bg=True, fade=[1.4, 0]),
        dict(a='world', at='8a#Explainer', until='8a#Explainer+10', p=dict(fs=1.0, links=[], nodes=[
            N('src', 'ctxt', 80, 392, 800, 110, 0.2, color='#5EC8FF', fs=16,
              lines=['Fuentes', 'openai.com/index/sharing-ai-progress-in-mathematics', 'github.com/openai/math', 'Quanta Magazine  ·  Nature'])]),
             bg=False, fade=[1.0, 2.5])]
