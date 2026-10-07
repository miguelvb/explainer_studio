# Scene 0 · Gancho
PROFILE='raw'   # approved before the house rules existed: plain constructors
MUSIC={'bells': 1}
cues=[]
cues.append(dict(a='seal',at='S0',until='0b',ext=0,p=dict(text='El primer ataque de|un enjambre de agentes',sub='Arkinos @ oct 2026  ·  Explainer Studio',at=0.5,type=14,scale=1.0,cy=215,ty=392),bg=True,fade=[0.8,2.0]))
cues.append(K('0b','0d',[
  W.clock('ck',30,30,(2026,7,8,23,0),run=dict(at='0c',dur=9,to=(2026,7,9,6,0)),at=0.2),
  W.agent_named('ac',200,150,'PHASEONE10841',at=0.4),
  N('q','quote',420,235,500,92,'0b#mensaje',color='teal',lines=['«Mi fallo no tiene consumidor.','Busco ideas.»'],fs=24,blink=.2,bf=3.2)],fs=1.0))
HOLES=[(662,175),(660,235),(664,300),(662,365),(666,425),(745,135),(830,135),(885,142),(890,215),(892,290),(890,360),(870,440),(800,442),(725,440),(780,230),(740,330)]
n=W.agent_group('g',gap=[235,305],gap_at='0d#atacando')
n+=W.hugging_face('hf',holes=[(x,y,'0d#atacando+%.1f'%(0.35*j+1.8)) for j,(x,y) in enumerate(HOLES)],at='0d#atacando')
n+=[N('gp','cross',499,269,2,2,0.05,color='red',alpha=0),W.counter('n700',630,18,700,'0d#setecientas',cap='agentes de OpenAI atacan Hugging Face')]
lk=[W.link('gp',f'hf_h{j}','0d#atacando+%.1f'%(0.35*j),color='red',speed=.55,curve=.1+.04*(j%4),solid=True) for j in range(len(HOLES))]
cm=[dict(at='0d',x=30,y=50,z=3.4),dict(at='0d#setecientas',x=30,y=50,z=3.4),dict(at='0d#atacando',x=50,y=50,z=1,dur=2.0)]
cues.append(K('0d','0f',n,lk,fs=1.0,cam=cm))
import random as _r
_rr=_r.Random(5)
_wd=lambda: ''.join(_rr.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(_rr.randint(2,7)))
PG=[' '.join(_wd() for _ in range(15)) for _ in range(22)]
n=[W.agent('e0',150,270,0.3,s=64,box_s=140),
   W.sheet('pg',330,50,560,440,PG,at='0f#leyeron',fs=7.5,color='blue',until='E0'),
   N('lp','lupa',250,340,96,96,'0f#leyeron',color='teal',
     move=[dict(at='0f#leyeron+1.6',x=365,y=60,dur=1.4)]+[dict(at=f'0f#leyeron+{3.2+1.5*j:.1f}',x=x_,y=y_,dur=1.4) for j,(x_,y_) in enumerate([(700,60),(700,140),(365,140),(365,220),(700,220),(700,300),(365,300),(365,380)])])]
n=[x for part in n for x in (part if isinstance(part,list) else [part])]
lk=[W.link('e0_box','pg','0f#leyeron',curve=.12,color='blue',solid=True)]
cues.append(K('0f','E0',n,lk,fs=1.0))
