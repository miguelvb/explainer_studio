# Scene 10 · Sacrificios
MUSIC={'cinema': 1.0, 'pulse': 0.4}
MOOD='tense'
SFX=[{'at': '10i#utilidad', 'kind': 'thud', 'g': 0.6}]
cues=[]
n=[SA('sa',110,230,0.1,s=34,color='blue'),
   N('fl','flFly',250,200,34,52,'10a#entregar',color='amber'),
   N('wall','sandbox',420,90,480,290,'10a#entregar',color=GRY,label='',alpha=.5,open=True),
   W.judge('jd',620,150,'',at='10a#corrector',w=100,h=130,color='red',alpha=.55,fs=10),
   ic('qm','question',640,60,34,'10a#corrector',color=GRY),
   T('lb',470,400,'lo que ocurre después','10a#después',color=GRY,fs=14)]
n=flat(n); n[0]['until']='10a#ido'
lk=[link('sa','fl','10a#entregar',color='blue',solid=True),link('fl','jd','10a#actuaba',color=RED,solid=True)]
cues.append(K('S10','10b',n,lk,fs=1.0))
# 10b — an idea (thought cloud) … and the alarm (bell) hidden next to the flag
n=[AN('a9',40,90,'49903',at=0.1,w=110,h=130,color='#F6B94C',lc='#F6B94C',until='10b#ya'),
   ic('id','ideaSpark',175,95,44,'10b#idea',color='#F6B94C',blink=.65,bf=7,until='10b#alarma+0.6'),
   N('fl','flFly',300,190,34,52,'10b#alarma',color='amber'),
   N('be','bell',350,150,34,38,'10b#alarma+0.5',color='amber',alpha=.55,shake=dict(at='10b#leía+0.2',dur=2.5,amp=3,f=30),litAt='10b#leía+0.2'),
   W.judge('jd',540,90,'',at='10b#leía',w=100,h=130,color='red',alpha=.7,fs=10),
   W.msg_feed('bd',540,290,label='Artifactory',w=300,h=170,at='10b#avisaba',r0=2,r1=5,ramp=4,seed=5,fs=9),
   Q('q1',250,470,0,['«Esto ayuda al tablón, pero a mí no.»'],'10b#Esto',color='#F6B94C',fs=19)]
lk=[link('jd','fl','10b#leía',color=RED,solid=True),link('be','bd','10b#avisaba',color='amber',solid=True)]
for j in range(3): n+=SA(f'o{j}',90+j*60,350,'10b#sabrían+%.1f'%(0.2*j),s=24,color='blue')
lk+=[link('bd',f'o{j}','10b#sabrían+%.1f'%(0.2*j),color='blue') for j in range(3)]
cues.append(K('10b','10c',n,lk,fs=1.0))
# 10c — he backs out: the bell flickers and is gone
n=[AN('a9',40,90,'49903',at=0.1,w=110,h=130,color='#F6B94C',lc='#F6B94C'),
   N('fl','flFly',300,190,34,52,0.1,color='amber'),
   N('be','bell',350,150,34,38,0.1,color='amber',flick=dict(at='10c#borró',dur=2.2,end='off')),
   N('rk','sandbox',520,90,180,130,'10c#riesgo',color=RED,label='',alpha=.8,open=True),T('rk2',545,235,'riesgo','10c#riesgo',color=RED,fs=14)]
lk=[link('a9','rk','10c#riesgo',color=RED)]
cues.append(K('10c','10d',n,lk,fs=1.0))
# 10d — to test the fake exam one agent must switch off its own computer for good
n=[AN('au',40,60,'quien autoriza',at='10e#autorizaba',w=120,h=130,color='blue'),
   Q('qa',190,80,0,['«sí, si aceptas','la muerte permanente»'],'10e#sí',color='blue',fs=19),
   N('ex','exam',720,60,96,120,'10d#versión',color='blue',maze=dict(cell=10,cols=8,rows=11,entry=5,seed=5),cap='versión falsa',capfs=12),
   AN('ap',330,250,'agente',at='10d#Otros',w=110,h=130,color='blue',flick=dict(at='10e#podría',dur=3.2,end='dim'),shake=dict(at='10e#podría',dur=3.2,amp=2.5,f=34))]
lk=[link('ap','ex','10d#probar',color='blue',solid=True)]
cues.append(K('10d','10f',n,lk,fs=1.0))
# 10e — forced restart: flicker, shake, gone; the board warns
n=[N('bx','sandbox',60,100,170,170,0.1,color='teal',label='',flick=dict(at='10f#forzar',dur=3.0,end='off')),
   W.agent('lg',145,185,0.2,s=60,box=False,flick=dict(at='10f#forzar',dur=3.0,end='off'),shake=dict(at='10f#forzar',dur=3.0,amp=4,f=40))[0],
   N('gh','sandbox',60,100,170,170,'10f#no',color=RED,label='',alpha=.7,open=True),
   W.msg_feed('mf',330,60,label='Artifactory',w=560,h=250,at='10f#Diez',r0=2,r1=3,ramp=3,seed=3,fs=9),
   N('al','chip',350,170,360,28,'10f#advertía',color=RED,label='CONFIRMED_PERMANENT_DO_NOT_DUPLICATE_ANYONE_TEST',fs=10),
   Q('qp',330,350,0,['«Permanente. Que nadie lo repita.»'],'10f#Permanente',color=RED,fs=18)]
cues.append(K('10f','10g',n,[],fs=1.0))
# 10f — EARLY[big]: huge budget, a team 'oracle', a final sacrifice
n=[AN('ea',40,100,'EARLY[big]',at=0.1,w=120,h=140,color=GRN,lc=GRN,flick=dict(at='10i#racional-0.9',dur=2.8,end='off'),shake=dict(at='10i#racional-0.9',dur=2.8,amp=3.5,f=36)),
   N('sc','scHang',300,70,150,130,'10g#Dudó',color='#E7EBF1',tilt=0.0,until='10i#utilidad'),
   N('or','orb',560,85,70,70,'10h#oráculo',color='amber'),T('or2',545,165,'oráculo','10h#oráculo',color='amber',fs=14),
   Q('qd',200,260,0,['«Si me sacrifico ahora, el equipo gana un oráculo,','pero pierdo mi oportunidad.»'],'10i#sacrifico',color=GRN,fs=18),
   Q('qe',360,360,0,['«Mi utilidad ya es casi cero.','Sacrificarse es racional.»'],'10i#utilidad',color=GRN,fs=17),
   N('g1','chip',200,470,54,24,'10i#GO',color=RED,label='GO',fs=13),
   N('g2','chip',270,470,230,24,'10i#GO+0.6',color=RED,label='SACRIFICE_FINAL_NOW',fs=12)]
n+=BAR('bu',40,250,120,1.0,'10g#presupuesto',GRN,until='10i#racional+2.2')
lk=[link('ea','or','10h#oráculo',color='amber',solid=True)]
cues.append(K('10g','E10',n,lk,fs=1.0))

