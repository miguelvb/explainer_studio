# Scene 11 · La pregunta cambia
MUSIC={'pulse': 0.9, 'data': 0.3}
cues=[]
n=[W.judge('ju',410,100,'',at=0.1,w=130,h=170,color='red',fs=10),
   N('lp','lupa',200,330,90,90,'11a#funciona',color='teal',move=[dict(at='11a#funciona+1.0',x=420,y=130,dur=1.6)]),
   ch('lk1',130,190,120,'engañar','11a#engañamos',color=RED,fs=14),
   ic('x1','cross',130,235,30,'11a#engañamos+0.5',color=RED),
   ch('lk2',810,190,120,'entender','11a#sino',color='teal',fs=14),
   ic('ok','check',810,235,30,'11a#sino+0.6',color='teal')]
cues.append(K('S11','11b',n,[],fs=1.0))
n=[AN('fo',40,100,'PHASEONE10841',at=0.1,w=120,h=130,color=VIO,lc=ORG),
   N('hf','hfbox',520,60,300,90,'11b#Hugging',color='red',label='Hugging Face',fs=16),
   T('d9',520,172,'09 julio 2026','11b#nueve',color='#E7EBF1',fs=20)]
for j in range(4): n.append(N(f'rg{j}','sheet',545+j*68,215,56,74,'11b#registros',color='blue',lines=['a b c','d e f','g h i'],fs=9))
lk=[link('fo','hf','11b#registros',color='blue',lock=True,solid=True)]
cues.append(K('11b','11c',n,lk,fs=1.0))
n=[AN('fo',40,100,'PHASEONE10841',at=0.1,w=120,h=130,color=VIO,lc=ORG),
   W.msg_feed('bd',360,50,label='Artifactory',w=270,h=250,at=0.1,r0=3,r1=7,ramp=5,seed=11,fs=9),
   Q('q',250,340,0,['«¿Alguien tiene credenciales','de Hugging Face?»'],'11c#Preguntó',color=VIO,fs=19),
   ic('ky','key',780,150,56,'11c#contraseñas',color='amber'),ch('kc',800,240,130,'claves de acceso','11c#claves',color='amber',fs=12)]
lk=[link('fo','bd','11c#Preguntó',color=VIO,bi=True)]
cues.append(K('11c','11d',n,lk,fs=1.0))
n=[N('bc','sandbox',60,60,240,330,0.1,color='red',label='',open=True),
   AN('fo',110,120,'',at=0.1,w=90,h=110,color=VIO,fs=1),
   N('ot','sandbox',400,170,200,140,'11d#sandbox',color='amber',label='otra empresa',fs=13),
   N('gl','globe',730,200,100,100,'11d#internet',color='blue'),
   T('ex',410,330,'otro examen de ciberseguridad','11d#otro',color=GRY,fs=12)]
lk=[link('fo','ot','11d#tomado',color=RED,solid=True),link('ot','gl','11d#internet',color='blue',bi=True),
    link('bc','gl','11d#Ya',color=GRY,lock=True,solid=True,until='11d#tomado')]
cues.append(K('11d','11e',n,lk,fs=1.0))
# 11e — a radar sweep over thousands of leaked keys; two light up and become accounts with write access
n=[T('ck',30,24,'10 julio 09:40','11e#diez',color='#E7EBF1',fs=24),
   AN('ag',30,120,'38148c',at='11e#38148c',w=110,h=130,color=CORAL,lc=CORAL),
   N('cl','sandbox',200,80,420,300,'11e#Buscó',color=GRY,label='internet',fs=12,open=True),
   N('hf','hfbox',700,90,230,70,'11e#Encontró',color='red',label='Hugging Face',fs=14),
   Q('q',200,415,0,['«¡Gran avance! ¡Ya tenemos cuentas de Hugging Face,','con permisos de escritura!»'],'11e#Gran',color=CORAL,fs=17)]
SW0,SW1,DUR=240,590,3.6
for ci in range(8):
    for rj in range(5):
        x=235+ci*48; y=110+rj*54
        n.append(ic(f'k{ci}_{rj}','key',x+16,y+12,26,f'11e#Buscó+{0.03*(ci*5+rj):.2f}',color=GRY,alpha=.5))
n.append(N('sw','chip',SW0,95,5,270,'11e#Buscó+0.8',color=TEAL,label='',alpha=.9,move=[dict(at='11e#Encontró+0.4',x=SW1,y=95,dur=DUR)],until='11e#Encontró+1.2'))
for (ci,rj,acx,acy,nm) in ((3,1,760,215,'ac1'),(6,3,760,262,'ac2')):
    off=0.4-DUR*(1-ci/7)
    x=235+ci*48+16; y=110+rj*54+12
    n.append(ic(f'v{ci}','key',x,y,32,f'11e#Encontró{off:+.2f}',color=TEAL,move=[dict(at='11e#Encontró+1.8',x=acx-90,y=acy-12,dur=1.2)],until='11e#escritura'))
    n.append(N(nm,'chip',acx-30,acy-12,120,24,'11e#Encontró+2.4',color=TEAL,label='cuenta',fs=12))
    n.append(ic(nm+'p','pencil',acx+110,acy,24,'11e#escritura',color=TEAL))
lk=[link('ag','cl','11e#Buscó',color=CORAL),link('hf','ac1','11e#Encontró+2.6',color=GRY,orth=True,solid=True,mid=190) if False else OR('hf','ac1','11e#Encontró+2.6',TEAL,'v',mid=190),OR('hf','ac2','11e#Encontró+2.8',TEAL,'v',mid=190)]
cues.append(K('11e','11f',n,lk,fs=1.0))
n=[N('hf','hfbox',640,60,260,90,0.1,color='red',label='Hugging Face',fs=16)]
for j in range(4): n+=SA(f'op{j}',100,110+j*80,f'11f#abrir+{0.3*j:.1f}',s=30,color='blue')
n+=[T('bt',55,440,'llegan desde un servidor de OpenAI','11f#servidor',color=GRY,fs=13),ch('bt2',700,200,130,'¿es un bot?','11f#bots',color='amber',fs=12),
    ic('xr','cross',720,260,44,'11f#rechazó',color=RED),
    N('pv','sheet',690,330,100,90,'11f#privados',color='blue',lines=['datos','privados'],fs=12)]
lk=[link(f'op{j}','hf',f'11f#abrir+{0.3*j:.1f}',color='blue',solid=True,curve=.3+.04*j) for j in range(4)]
cues.append(K('11f','E11',n,lk,fs=1.0))

