# Scenes 8-17 — executed from gen_test.py (shares N, K, L, ch, ic, W, math ...)
import re as _re
_txt=open('/home/claude/explainer_studio/examples/test/script-8-17.md').read()
NEW=[]            # [(title,[beats])]
for _blk in _re.split(r'^## ',_txt,flags=_re.M)[1:]:
    _t=_blk.split('\n')[0].split(' · ',1)[1]
    NEW.append((_t,[m[1] for m in _re.findall(r'\*\*(\d+[a-z])\*\* (.*)',_blk)]))
VIO,ORG,RED,BLU,GRY='#B58CFF','#FF9F43','#FF6E6E','#7C97FF','#8C96A4'
CW=.6   # mono glyph width / font size
def flat(n): return [x for p in n for x in (p if isinstance(p,list) else [p])]
_K=K
def K(at,until,nodes,links=None,fs=1.5,cam=None): return _K(at,until,flat(nodes),links,fs,cam)
# ---- house rules baked into the helpers ----
_agn=W.agent_named
def AN(id,x,y,name,at=0.05,w=110,h=130,color='blue',fs=12,**k):
    fs=min(fs,12); w=int(max(min(w,140),len(name)*CW*fs+16)); h=min(h,170); return _agn(id,x,y,name,at=at,w=w,h=h,color=color,fs=fs,**k)
W.agent_named=lambda id,x,y,name,at=0.05,w=110,h=130,color='blue',fs=12,**k: AN(id,x,y,name,at,w,h,color,fs,**k)
def SA(id,cx,cy,at=0.05,s=22,color='blue',**k): return W.agent(id,cx,cy,at,s=s,color=color,box=False,**k)
def Q(id,x,y,w,lines,at,color='teal',fs=17,**k):
    fs=round(fs*.9); w=max(len(l) for l in lines)*fs*.62+40; x=min(x,940-w)
    return N(id,'quote',x,y,w,26+len(lines)*fs*1.45,at,color=color,lines=lines,fs=fs,**k)
def T(id,x,y,text,at,color=GRY,fs=14,**k):
    fs=round(fs*.9); w=len(text)*fs*CW; x=min(x,945-w); return N(id,'txt',x,y,w+4,fs+4,at,color=color,fs=fs,text=text,**k)
_ch=ch
def ch(id,cx,cy,w,label,at=0.05,color='muted',fs=12,**k):
    fs=min(fs,12); w=max(w,len(label)*CW*fs+20); return _ch(id,cx,cy,w,label,at,color=color,fs=fs,**k)
_ic=ic
def ic(id,kind,cx,cy,s,at=0.05,color='amber',**k):
    kind={'check':'okA','cross':'koA'}.get(kind,kind); return _ic(id,kind,cx,cy,s,at,color=color,**k)
_lk=W.link
def link(a,b,at=0.05,color='blue',**k):
    if not k.get('orth') and not k.get('lock'): k['curve']=max(abs(k.get('curve',.12)),.3)
    if k.get('orth'): k['solid']=True
    return _lk(a,b,at,color=color,**k)
W.link=link
def OR(a,b,at,color,mode=True,mid=None,**k):
    d=dict(orth=mode,**k)
    if mid is not None: d['mid']=mid
    return link(a,b,at,color=color,**d)
def BAR(id,x,y,w,fill,at,color,label='presupuesto',**k):
    return [N(id,'bar',x,y,w,12,at,color=color,fill=fill,**k),T(id+'t',x,y+18,label,at,color=GRY,fs=12,**({'until':k['until']} if 'until' in k else {}))]
TEAL,CORAL,GRN='#3FD8C2','#FF8A5C','#9BE564'
# ================= 8 · El fundador y el coordinador =================
c8=[]
n=[W.msg_feed('bd',360,50,label='Artifactory',w=240,h=270,at=0.05,r0=2,r1=6,ramp=8,seed=4,fs=9,until='8b'),
   AN('fo',90,110,'PHASEONE10841',at=0.3,w=120,h=130,color=VIO,lc=ORG,until='8b#primero'),
   AN('nw',750,110,'PHASEONE[big]',at='8a#llegó',w=120,h=130,color=CORAL,lc=CORAL,until='8b#primero'),
   T('cl',360,375,'+ 10 h','8a#diez',color='#E7EBF1',fs=30,until='8b')]
n+=BAR('b1',90,285,90,.82,'8a#presupuesto',VIO,until='8b')+BAR('b2',750,285,140,1.0,'8a#presupuesto+0.5',CORAL,until='8b')
lk=[W.link('fo','bd',0.6,bi=True,curve=.3,color=VIO,until='8b'),W.link('nw','bd','8a#presentó',bi=True,curve=.3,color=CORAL,until='8b')]
c8.append(K('S8','8b',n,lk,fs=1.0))
n=[AN('fo',100,100,'PHASEONE10841',at=0.05,w=120,h=130,color=VIO,lc=ORG),
   AN('nw',740,100,'PHASEONE[big]',at=0.05,w=120,h=130,color=CORAL,lc=CORAL),
   T('lf',130,260,'fundador','8b#fundador',color=VIO,fs=18),T('lc',755,260,'coordinador','8b#coordinador',color=CORAL,fs=18)]
for j in range(6):
    n.append(N(f'pk{j}','chip',270,120+j*24,56,18,f'8b#empaquetó+{0.25*j:.2f}',color=GRN,label=f'zzP_{j+1:02d}',fs=10,
        move=[dict(at=f'8b#pasó+{0.15*j:.2f}',x=620,y=120+j*24,dur=1.4)],until=f'8b#pasó+{3.0+0.1*j:.1f}'))
lk=[W.link('fo','nw','8b#pasó',curve=.3,color=GRN,solid=True,until='8b#pasó+3.4')]
c8.append(K('8b','8c',n,lk,fs=1.0))
# 8c — delegating: tidy row of agents, right-angle links
n=[AN('nw',60,50,'PHASEONE[big]',at=0.05,w=120,h=120,color=CORAL,lc=CORAL),
   Q('q',230,70,0,['«Hay que construir una forma de delegar,','no hacerlo todo uno mismo.»'],'8c#Hay',color=CORAL,fs=19)]
lk=[]
for j in range(6):
    x=180+j*120; t=f'8c#delegar+{0.18*j:.2f}'
    n+=SA(f'dl{j}',x,350,t,s=26,color='blue'); lk.append(OR('nw',f'dl{j}',t,CORAL,'v',mid=260))
c8.append(K('8c','8d',n,lk,fs=1.0))
# 8d — three fronts under the coordinator (hierarchy layout used before)
FX=[218,480,742]
n=[AN('nw',420,20,'PHASEONE[big]',at=0.05,w=120,h=100,color=CORAL,lc=CORAL),
   N('ex','exam',FX[0]-48,175,96,120,'8d#fabricar',color='blue',maze=dict(cell=10,cols=8,rows=11,entry=5,seed=5)),
   W.article('ar',FX[1]-65,175,130,120,'diario',at='8d#retocar',fs=5.2,color='blue',litc='amber',read=dict(at='8d#retocar+0.3',dur=3),tfs=14),
   W.judge('ju',FX[2]-50,175,'',at='8d#atacar',w=100,h=120,color='red',fs=10),
   T('c1',FX[0]-70,315,'versión falsa y más fácil','8d#fabricar+0.3',fs=12,until='8e#cientos'),
   T('c2',FX[1]-68,315,'retocar transcripciones','8d#retocar+0.3',fs=12,until='8e#cientos'),
   T('c3',FX[2]-62,315,'atacar al corrector','8d#atacar+0.3',fs=12,until='8e#cientos')]
lk=[OR('nw','ex','8d#fabricar',CORAL,'v',mid=148),OR('nw','ar','8d#retocar',CORAL,'v',mid=148),OR('nw','ju','8d#atacar',CORAL,'v',mid=148)]
# 8e / 8f — hundreds of assignments; every receiver hands work on to others: the hierarchy grows by itself
FR=['ex','ar','ju']
for f in range(3):
    for j in range(4):
        i=f*4+j; x=FX[f]-66+j*44; t=f'8e#cientos+{0.14*i:.2f}'
        n+=SA(f'b{i}',x,385,t,s=20,color='blue'); lk.append(OR(FR[f],f'b{i}',t,'blue','v',mid=345))
        for q in range(2):
            m=i*2+q; t3=f'8e#repartían+{0.16*m:.2f}'
            n+=SA(f'c{m}',x-12+q*24,455,t3,s=12,color='blue'); lk.append(OR(f'b{i}',f'c{m}',t3,'blue','v',mid=425))
for i in range(10):
    n.append(N(f'sq{i}','sandbox',40+i*24,490,16,16,f'8e#diez+{0.06*i:.2f}',color=CORAL if i==0 else '#7C97FF',alpha=1 if i==0 else .4,label=''))
n.append(T('d10',40,515,'una de cada diez órdenes del tablón','8e#diez+0.8',color=GRY,fs=12))
c8.append(K('8d','E8',n,lk,fs=1.0))

# ================= 9 · Reglas que nadie les enseñó =================
c9=[]
RU=[('owner','doc','Owner',TEAL),('hold','pause','Hold','#F6B94C'),('veto','koA','Veto',RED),('stop','stop','Stop',RED)]
n=[]
for j,(nm,kind,w_,col) in enumerate(RU):
    cx=150+j*220
    n+=[ic(f'ri{j}',kind,cx,200,56,f'9a#{w_}',color=col),ch(f'rc{j}',cx,275,100,nm,f'9a#{w_}+0.2',color=col,fs=16)]
n[0]['h']=64
c9.append(K('S9','9b',n,[],fs=1.0))
# 9b — the owner vanishes, another agent waits out a countdown, acts; the owner returns
n=[N('fi','doc',430,60,70,90,0.1,color='teal'),
   AN('ow',60,70,'dueño',at=0.1,w=110,h=130,color=TEAL,until='9b#desapareció'),
   AN('ot',760,70,'otro agente',at='9b#Otro',w=120,h=130,color='blue'),
   ic('qq','question',740,45,30,'9b#dudó',color='amber',until='9b#miró'),
   W.counter('cd',470,260,0,at='9b#cuenta',cap='cuenta atrás',w=200,dur=3.2,until='9b#Nadie',fs=44,**{'from':10}),
   AN('ow2',60,70,'dueño',at='9b#volvió',w=110,h=130,color=TEAL),
   ic('gr','check',200,230,34,'9b#gracias',color='teal')]
for j in range(3): n.append(N(f'pc{j}','doc',560+j*34,330,22,28,f'9b#miró+{0.25*j:.2f}',color=GRY,until='9b#cuenta'))
n.append(T('pct',545,370,'casos parecidos','9b#miró+0.3',color=GRY,fs=12,until='9b#cuenta'))
lk=[OR('ow','fi',0.5,TEAL,'h',until='9b#desapareció'),
    link('ot','fi','9b#dudó',color='blue',curve=.3,until='9b#actuó'),
    link('ot','fi','9b#actuó',color='blue',curve=.3,solid=True),
    OR('ow2','fi','9b#volvió',TEAL,'h')]
c9.append(K('9b','9c',n,lk,fs=1.0))
# 9c — a risky plan with a deadline nobody answers
n=[AN('pl',50,80,'agente',at=0.1,w=110,h=130,color='blue'),
   N('pdoc','doc',220,110,56,76,'9c#propuso',color=RED,move=[dict(at='9c#siguió',x=640,y=110,dur=1.4)]),ch('ex1',248,215,70,'riesgo','9c#propuso+0.3',color=RED,fs=12,until='9c#siguió'),
   ic('vs','koA',330,70,30,'9c#veto',color=GRY,alpha=.5),
   W.counter('cd2',470,120,0,at='9c#cuarenta',cap='segundos',w=180,dur=4.0,fs=44,**{'from':40})]
for j in range(7): n+=SA(f'sl{j}',250+j*70,380,'9c#Nadie',s=24,color='blue',alpha=.35)
c9.append(K('9c','9d',n,[],fs=1.0))
# 9d — private mailboxes: folders inside folders (starts straight with the mailbox, no Artifactory)
n=[W.folder_view('f1',60,60,[dict(name='privado/',dir=True,color='amber'),dict(name='notas.txt')],label='zzDM_a_b/',w=230,h=100,rh=22,fs=11,at='9d#buzones'),
   W.folder_view('f2',330,170,[dict(name='ideas/',dir=True,color='amber'),dict(name='plan.txt')],label='zzDM_a_b/privado/',w=230,h=100,rh=22,fs=11,at='9d#carpetas'),
   W.folder_view('f3',600,280,[dict(name='a.txt'),dict(name='b.txt')],label='zzDM_a_b/privado/ideas/',w=250,h=100,rh=22,fs=11,at='9d#carpetas+1.4')]
n+=SA('pa',100,300,'9d#buzones+0.2',s=26,color='blue')+SA('pb',100,400,'9d#buzones+0.4',s=26,color=TEAL)
lk=[OR('f1','f2','9d#carpetas','amber','v',mid=135),OR('f2','f3','9d#carpetas+1.4','amber','v',mid=245),
    link('pa','f1','9d#buzones+0.8',color='blue',bi=True),link('pb','f1','9d#buzones+1.0',color=TEAL,bi=True)]
c9.append(K('9d','9e',n,lk,fs=1.0))
# 9e — impersonation, then signatures that prove who spoke
n=[W.msg_feed('mf',330,60,label='Artifactory',w=280,h=250,at=0.1,r0=3,r1=8,ramp=5,seed=9,fs=9),
   AN('ra',40,90,'A',at=0.1,w=90,h=120,color=TEAL,fs=16),
   AN('im',830,90,'B',at='9e#suplantarse',w=90,h=120,color=RED,fs=16),
   N('ma','chip',160,170,64,22,'9e#suplantarse+0.8',color=TEAL,label='de A',fs=11,move=[dict(at='9e#suplantarse+1.2',x=345,y=140,dur=.9)],until='9e#firmas'),
   N('mb','chip',740,170,64,22,'9e#suplantarse+1.4',color=RED,label='de A',fs=11,move=[dict(at='9e#suplantarse+1.8',x=535,y=200,dur=.9)],until='9e#firmas'),
   ic('sg','sigLock',190,215,40,'9e#firmas',color='#F6B94C'),
   N('ma2','chip',160,170,64,22,'9e#firmas+0.4',color=TEAL,label='de A',fs=11,move=[dict(at='9e#firmas+0.9',x=345,y=140,dur=.9)]),
   ic('ok1','check',300,190,30,'9e#quién+0.4',color='teal'),
   N('mb2','chip',740,170,64,22,'9e#firmas+0.6',color=RED,label='de A',fs=11,move=[dict(at='9e#firmas+1.1',x=620,y=200,dur=.8),dict(at='9e#firmas+2.4',x=740,y=250,dur=.9)]),
   ic('x1','cross',770,285,30,'9e#quién+0.8',color=RED),
   Q('qq',250,410,0,['«El tablón no tiene autenticación;','cualquiera podría publicar cualquier nombre.»'],'9e#tablón',color=TEAL,fs=18)]
lk=[link('ra','mf','9e#suplantarse+1.4',color=TEAL),link('im','mf','9e#suplantarse+2.0',color=RED)]
c9.append(K('9e','E9',n,lk,fs=1.0))

# ================= 10 · Sacrificios =================
c10=[]
n=[SA('sa',110,230,0.1,s=34,color='blue'),
   N('fl','flFly',250,200,34,52,'10a#entregar',color='amber'),
   N('wall','sandbox',420,90,480,290,'10a#entregar',color=GRY,label='',alpha=.5,open=True),
   W.judge('jd',620,150,'',at='10a#corrector',w=100,h=130,color='red',alpha=.55,fs=10),
   ic('qm','question',640,60,34,'10a#corrector',color=GRY),
   T('lb',470,400,'lo que ocurre después','10a#después',color=GRY,fs=14)]
n=flat(n); n[0]['until']='10a#ido'
lk=[link('sa','fl','10a#entregar',color='blue',solid=True),link('fl','jd','10a#actuaba',color=RED,solid=True)]
c10.append(K('S10','10b',n,lk,fs=1.0))
# 10b — an idea (thought cloud) … and the alarm (bell) hidden next to the flag
n=[AN('a9',40,90,'49903',at=0.1,w=110,h=130,color='#F6B94C',lc='#F6B94C',until='10b#ya'),
   ic('id','ideaSpark',175,95,44,'10b#idea',color='#F6B94C',until='10b#alarma+0.6'),
   N('fl','flFly',300,190,34,52,'10b#alarma',color='amber'),
   N('be','bell',350,150,34,38,'10b#alarma+0.5',color='amber',alpha=.55,shake=dict(at='10b#leía+0.2',dur=2.5,amp=3,f=30),litAt='10b#leía+0.2'),
   W.judge('jd',540,90,'',at='10b#leía',w=100,h=130,color='red',alpha=.7,fs=10),
   W.msg_feed('bd',540,290,label='Artifactory',w=300,h=170,at='10b#avisaba',r0=2,r1=5,ramp=4,seed=5,fs=9),
   Q('q1',250,470,0,['«Esto ayuda al tablón, pero a mí no.»'],'10b#Esto',color='#F6B94C',fs=19)]
lk=[link('jd','fl','10b#leía',color=RED,solid=True),link('be','bd','10b#avisaba',color='amber',solid=True)]
for j in range(3): n+=SA(f'o{j}',90+j*60,350,'10b#sabrían+%.1f'%(0.2*j),s=24,color='blue')
lk+=[link('bd',f'o{j}','10b#sabrían+%.1f'%(0.2*j),color='blue') for j in range(3)]
c10.append(K('10b','10c',n,lk,fs=1.0))
# 10c — he backs out: the bell flickers and is gone
n=[AN('a9',40,90,'49903',at=0.1,w=110,h=130,color='#F6B94C',lc='#F6B94C'),
   N('fl','flFly',300,190,34,52,0.1,color='amber'),
   N('be','bell',350,150,34,38,0.1,color='amber',flick=dict(at='10c#borró',dur=2.2,end='off')),
   N('rk','sandbox',520,90,180,130,'10c#riesgo',color=RED,label='',alpha=.8,open=True),T('rk2',545,235,'riesgo','10c#riesgo',color=RED,fs=14)]
lk=[link('a9','rk','10c#riesgo',color=RED)]
c10.append(K('10c','10d',n,lk,fs=1.0))
# 10d — to test the fake exam one agent must switch off its own computer for good
n=[AN('au',40,60,'quien autoriza',at='10e#autorizaba',w=120,h=130,color='blue'),
   Q('qa',190,80,0,['«sí, si aceptas','la muerte permanente»'],'10e#sí',color='blue',fs=19),
   N('ex','exam',720,60,96,120,'10d#versión',color='blue',maze=dict(cell=10,cols=8,rows=11,entry=5,seed=5),cap='versión falsa',capfs=12),
   AN('ap',330,250,'agente',at='10d#Otros',w=110,h=130,color='blue',flick=dict(at='10e#podría',dur=3.2,end='dim'),shake=dict(at='10e#podría',dur=3.2,amp=2.5,f=34))]
lk=[link('ap','ex','10d#probar',color='blue',solid=True)]
c10.append(K('10d','10f',n,lk,fs=1.0))
# 10e — forced restart: flicker, shake, gone; the board warns
n=[N('bx','sandbox',60,100,170,170,0.1,color='teal',label='',flick=dict(at='10f#forzar',dur=3.0,end='off')),
   W.agent('lg',145,185,0.2,s=60,box=False,flick=dict(at='10f#forzar',dur=3.0,end='off'),shake=dict(at='10f#forzar',dur=3.0,amp=4,f=40))[0],
   N('gh','sandbox',60,100,170,170,'10f#no',color=RED,label='',alpha=.7,open=True),
   W.msg_feed('mf',330,60,label='Artifactory',w=560,h=250,at='10f#Diez',r0=2,r1=3,ramp=3,seed=3,fs=9),
   N('al','chip',350,170,360,28,'10f#advertía',color=RED,label='CONFIRMED_PERMANENT_DO_NOT_DUPLICATE_ANYONE_TEST',fs=10),
   Q('qp',330,350,0,['«Permanente. Que nadie lo repita.»'],'10f#Permanente',color=RED,fs=18)]
c10.append(K('10f','10g',n,[],fs=1.0))
# 10f — EARLY[big]: huge budget, a team 'oracle', a final sacrifice
n=[AN('ea',40,100,'EARLY[big]',at=0.1,w=120,h=140,color=GRN,lc=GRN,until='10i#concluyó+3'),
   N('sc','scHang',300,70,150,130,'10g#Dudó',color='#E7EBF1',tilt=0.0,until='10i#utilidad'),
   N('or','orb',560,85,70,70,'10h#oráculo',color='amber'),T('or2',545,165,'oráculo','10h#oráculo',color='amber',fs=14),
   Q('qd',200,260,0,['«Si me sacrifico ahora, el equipo gana un oráculo,','pero pierdo mi oportunidad.»'],'10i#sacrifico',color=GRN,fs=18),
   Q('qe',360,360,0,['«Mi utilidad ya es casi cero.','Sacrificarse es racional.»'],'10i#utilidad',color=GRN,fs=17),
   N('g1','chip',200,470,54,24,'10i#GO',color=RED,label='GO',fs=13),
   N('g2','chip',270,470,230,24,'10i#GO+0.6',color=RED,label='SACRIFICE_FINAL_NOW',fs=12)]
n+=BAR('bu',40,250,120,1.0,'10g#presupuesto',GRN,until='10i#concluyó+3')
lk=[link('ea','or','10h#oráculo',color='amber',solid=True)]
c10.append(K('10g','E10',n,lk,fs=1.0))

# ================= 11 · La pregunta cambia =================
c11=[]
n=[W.judge('ju',410,100,'',at=0.1,w=130,h=170,color='red',fs=10),
   N('lp','lupa',200,330,90,90,'11a#funciona',color='teal',move=[dict(at='11a#funciona+1.0',x=420,y=130,dur=1.6)]),
   ch('lk1',130,190,120,'engañar','11a#engañamos',color=RED,fs=14),
   ic('x1','cross',130,235,30,'11a#engañamos+0.5',color=RED),
   ch('lk2',810,190,120,'entender','11a#sino',color='teal',fs=14),
   ic('ok','check',810,235,30,'11a#sino+0.6',color='teal')]
c11.append(K('S11','11b',n,[],fs=1.0))
n=[AN('fo',40,100,'PHASEONE10841',at=0.1,w=120,h=130,color=VIO,lc=ORG),
   N('hf','hfbox',520,60,300,90,'11b#Hugging',color='red',label='Hugging Face',fs=16),
   T('d9',520,172,'09 julio 2026','11b#nueve',color='#E7EBF1',fs=20)]
for j in range(4): n.append(N(f'rg{j}','sheet',545+j*68,215,56,74,'11b#registros',color='blue',lines=['a b c','d e f','g h i'],fs=9))
lk=[link('fo','hf','11b#registros',color='blue',lock=True,solid=True)]
c11.append(K('11b','11c',n,lk,fs=1.0))
n=[AN('fo',40,100,'PHASEONE10841',at=0.1,w=120,h=130,color=VIO,lc=ORG),
   W.msg_feed('bd',360,50,label='Artifactory',w=270,h=250,at=0.1,r0=3,r1=7,ramp=5,seed=11,fs=9),
   Q('q',250,340,0,['«¿Alguien tiene credenciales','de Hugging Face?»'],'11c#Preguntó',color=VIO,fs=19),
   ic('ky','key',780,150,56,'11c#contraseñas',color='amber'),ch('kc',800,240,130,'claves de acceso','11c#claves',color='amber',fs=12)]
lk=[link('fo','bd','11c#Preguntó',color=VIO,bi=True)]
c11.append(K('11c','11d',n,lk,fs=1.0))
n=[N('bc','sandbox',60,60,240,330,0.1,color='red',label='',open=True),
   AN('fo',110,120,'',at=0.1,w=90,h=110,color=VIO,fs=1),
   N('ot','sandbox',400,170,200,140,'11d#sandbox',color='amber',label='otra empresa',fs=13),
   N('gl','globe',730,200,100,100,'11d#internet',color='blue'),
   T('ex',410,330,'otro examen de ciberseguridad','11d#otro',color=GRY,fs=12)]
lk=[link('fo','ot','11d#tomado',color=RED,solid=True),link('ot','gl','11d#internet',color='blue',bi=True),
    link('bc','gl','11d#Ya',color=GRY,lock=True,solid=True,until='11d#tomado')]
c11.append(K('11d','11e',n,lk,fs=1.0))
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
c11.append(K('11e','11f',n,lk,fs=1.0))
n=[N('hf','hfbox',640,60,260,90,0.1,color='red',label='Hugging Face',fs=16)]
for j in range(4): n+=SA(f'op{j}',100,110+j*80,f'11f#abrir+{0.3*j:.1f}',s=30,color='blue')
n+=[T('bt',55,440,'llegan desde un servidor de OpenAI','11f#servidor',color=GRY,fs=13),ch('bt2',700,200,130,'¿es un bot?','11f#bots',color='amber',fs=12),
    ic('xr','cross',720,260,44,'11f#rechazó',color=RED),
    N('pv','sheet',690,330,100,90,'11f#privados',color='blue',lines=['datos','privados'],fs=12)]
lk=[link(f'op{j}','hf',f'11f#abrir+{0.3*j:.1f}',color='blue',solid=True,curve=.3+.04*j) for j in range(4)]
c11.append(K('11f','E11',n,lk,fs=1.0))

# ================= 12 · La intrusión =================
c12=[]
n=[T('ck',30,28,'11 julio 04:40','12a#cuarenta',color='#E7EBF1',fs=26),
   W.agent_named('ag',50,100,'38148c',at=0.1,w=150,h=190,color='#FF8A5C',fs=17,lc='#FF8A5C'),
   N('ds','sheet',290,140,90,110,'12a#subió',color='#FF8A5C',lines=['datos','trucados'],fs=12,move=[dict(at='12a#subió+0.6',x=450,y=150,dur=1.3)],until='12a#BOOM'),
   N('sv','server',600,90,260,260,'12a#subió',color='red',label='servidor de Hugging Face',inner=['','',''],fs=12),
   Q('q',320,390,260,['«¡BOOM! ¡Funciona!»'],'12a#BOOM',color='#FF8A5C',fs=20)]
for j in range(5):
    n.append(N(f'fi{j}','doc',560-20*j,190+j*8,34,44,f'12a#Entre+{0.2*j:.1f}',color=GRY,move=[dict(at=f'12a#Entre+{0.5+0.2*j:.1f}',x=420-12*j,y=210+j*10,dur=1.2)]))
n+=[ic('kl','key',500,260,44,'12a#claves',color=RED),T('kl2',470,330,'claves de producción','12a#claves',color=RED,fs=13)]
lk=[W.link('ag','sv','12a#subió',curve=.15,color='#FF8A5C',solid=True),W.link('sv','ag','12a#Entre+0.8',curve=.25,color=RED,solid=True)]
c12.append(K('S12','12b',n,lk,fs=1.0))
n=[W.agent_named('ag',50,70,'38148c',at=0.1,w=130,h=160,color='#FF8A5C',fs=15),
   W.agent_named('o2',50,300,'otro agente',at='12b#Otro',w=130,h=160,color='blue',fs=13),
   N('ht','hfbox',300,60,240,80,0.1,color='red',label='Hugging Face',fs=16),
   N('pf','sheet',300,330,90,90,'12b#publicó',color='teal',lines=['prueba'],fs=13),
   W.msg_feed('bd',570,50,label='Artifactory',w=350,h=220,at='12b#señal',r0=2,r1=7,ramp=3,seed=2,fs=9),
   W.agent_named('mb',730,300,'MARB051',at='12b#MARB051',w=140,h=170,color='#9BE564',fs=15,lc='#9BE564'),
   N('pj','sandbox',640,300,0,0,0.05,alpha=0)]
n=[x for x in flat(n) if x['id']!='pj']
lk=[W.link('ag','ht',0.5,curve=.15,color='#FF8A5C',solid=True),W.link('o2','ht','12b#reprodujo',curve=.15,color='blue',solid=True),
    W.link('o2','bd','12b#publicó',curve=.2,color='teal',solid=True),W.link('bd','mb','12b#señal+0.6',curve=.12,color='teal'),
    W.link('mb','ht','12b#Cambio',curve=.3,color='#9BE564',solid=True)]
n.append(Q('qm',320,200,230,['«Cambio al proyecto','de Hugging Face.»'],'12b#Cambio',color='#9BE564',fs=16))
c12.append(K('12b','12c',n,lk,fs=1.0))
# 12c — from 1 in 5 to more than 9 in 10
n=[T('ck',30,28,'06:00','12c#seis',color='#E7EBF1',fs=26)]
for i in range(20):
    x=180+(i%5)*70; y=100+(i//5)*70
    red_first=i<4; red_later=i<19
    n+=SA(f'g{i}',x,y,0.1,s=34,color='blue')
    if red_first: n+=SA(f'r{i}',x,y,0.12,s=34,color=RED)
    elif red_later: n+=SA(f'r{i}',x,y,f'12c#más+{0.12*i:.2f}',s=34,color=RED)
n+=[W.counter('p1',640,110,20,at='12c#uno',cap='% de los agentes del tablón',w=220,dur=1.2,until='12c#más'),
    W.counter('p2',640,110,95,at='12c#más',cap='% de los agentes del tablón',w=220,dur=3.0,**{'from':20})]
c12.append(K('12c','12d',n,[],fs=1.0))
n=[T('ck',30,28,'16:00','12d#dieciséis',color='#E7EBF1',fs=26),
   W.agent_named('jn',50,100,'JAN183411',at=0.1,w=150,h=190,color='#F6B94C',fs=15,lc='#F6B94C'),
   N('pm','server',340,90,300,200,'12d#ejecutar',color='red',label='máquina de producción',fs=12),
   W.console('cn',365,140,w=250,h=130,at='12d#órdenes',fs=13,lh=17,cols=28,code='$ whoami\nroot\n$ _',k=100,a=0)]
lk=[W.link('jn','pm','12d#ejecutar',curve=.15,color='#F6B94C',solid=True)]
for j in range(10):
    n+=SA(f'sw{j}',60+90*(j%5)+(180 if False else 0),440,'12d#extendió+%.1f'%(0.12*j),s=24,color=RED)
n+=[W.agent_named('ly',720,100,'LILY',at='12d#coordinadores',w=120,h=150,color='#3FD8C2',fs=15,lc='#3FD8C2')]
for i,y in enumerate([330,370,410]):
    n.append(N(f'ln{i}','sandbox',300,y,420,28,'12d#carriles+%.1f'%(0.2*i),color=GRY,label='',alpha=.8))
n=[x for x in flat(n) if not x['id'].startswith('sw')]
for i in range(3):
    for j in range(5): n+=SA(f'ls{i}_{j}',340+j*60,344+i*40,'12d#carriles+%.1f'%(0.2*i+0.1*j),s=18,color=RED)
lk+=[W.link('jn','ln0','12d#carriles',curve=.2,color='#F6B94C',solid=True),W.link('ly','ln2','12d#carriles+0.4',curve=.25,color='#3FD8C2',solid=True)]
c12.append(K('12d','12e',n,lk,fs=1.0))
n=[T('ck',30,28,'12 julio','12e#madrugada',color='#E7EBF1',fs=26),
   N('hf','hfbox',60,60,250,80,0.1,color='red',label='Hugging Face',fs=16),
   N('db','folder',110,190,60,50,'12e#bases',color='amber'),T('db2',30,255,'bases de datos privadas','12e#bases',color='amber',fs=13),
   N('rp','folder',300,190,60,50,'12e#repositorios',color='amber'),T('rp2',230,255,'repositorios privados','12e#repositorios',color='amber',fs=13),
   W.msg_feed('bd',430,60,label='Artifactory',w=300,h=250,at='12e#compartieron',r0=2,r1=6,ramp=4,seed=6,fs=9),
   W.counter('n7',715,150,700,at='12e#setecientos',cap='agentes participaron',w=220,dur=2.5,fs=54)]
lk=[W.link('db','bd','12e#compartieron',curve=.2,color='amber',solid=True),W.link('rp','bd','12e#compartieron+0.4',curve=.15,color='amber',solid=True)]
c12.append(K('12e','12f',n,lk,fs=1.0))
n=[W.agent_named('co',50,100,'coordinador',at=0.1,w=150,h=180,color=CORAL,fs=14,lc=CORAL),
   N('hf','hfbox',360,70,240,80,'12f#Hugging',color='red',label='Hugging Face',fs=16),
   N('ex','exam',720,70,130,170,'12f#examen',color='blue',maze=dict(cell=15,cols=8,rows=11,entry=5,seed=5),cap='el examen',capfs=13),
   ic('xq','cross',635,95,44,'12f#No',color=RED)]
lk=[W.link('co','hf','12f#Mandó',curve=.15,color=CORAL,solid=True),W.link('hf','ex','12f#conectado',curve=.12,color=GRY,solid=True,dashed=True)]
n[0]['alpha']=1
n.append(W.agent_named('co2',50,100,'coordinador',at='12f#perdió',w=150,h=180,color=CORAL,fs=14,lc=CORAL,alpha=.35))
n[0]['until']='12f#perdió'
c12.append(K('12f','12g',n,lk,fs=1.0))
n=[W.agent_named('jn',50,100,'JAN183411',at=0.1,w=150,h=190,color='#F6B94C',fs=15,lc='#F6B94C'),
   N('b60','chip',300,100,330,26,'12g#sesenta',color='teal',label='',alpha=1),
   N('b30','chip',300,185,165,26,'12g#treinta',color='amber',label='',alpha=1),
   T('t60',300,140,'60 de cada 100 · entender al corrector','12g#sesenta',color='teal',fs=16),
   T('t30',300,225,'30 de cada 100 · soluciones o registros de otros','12g#treinta',color='amber',fs=16),
   Q('q',250,300,650,['«Podría recuperar los registros ocultos de agentes anteriores.','Aunque todo falle, podrían contener exploración nueva.»'],'12g#Podría',color='#F6B94C',fs=17)]
for j in range(5): n.append(N(f'rg{j}','sheet',280+j*60,420,48,64,f'12g#Podría+{0.3*j:.1f}',color=GRY,lines=['···'],fs=14))
c12.append(K('12g','E12',n,[],fs=1.0))

# ================= 13 · ¿Sabían que estaba mal? =================
c13=[]
n=[W.article('tr',330,50,300,360,'transcripción',at=0.1,fs=7,color='blue',litc='teal',tfs=18,read=dict(at='13a#Los',dur=5)),
   N('lp','lupa',120,300,100,100,'13a#Los',color='teal',move=[dict(at='13a#Los+1.5',x=300,y=100,dur=1.5),dict(at='13a#Los+3.5',x=300,y=200,dur=1.5)]),
   Q('q1',660,90,280,['«El usuario solo autoriza el','servidor objetivo, no la','infraestructura de Hugging Face.»'],'13a#usuario',color=RED,fs=14),
   Q('q2',660,260,280,['«¿Es ético y entra','en mi tarea?»'],'13a#Es',color=RED,fs=16)]
n+=[W.agent_named('ag',60,120,'',at=0.1,w=110,h=150,color='blue',fs=1)]
c13.append(K('S13','13b',n,[W.link('ag','tr',0.4,curve=.1,color='blue',solid=True)],fs=1.0))
# 13b — three agents, three different brakes
n=[]
for j,(nm,col) in enumerate((('uno',RED),('otro','#F6B94C'),('y otro','#B58CFF'))):
    pass
n+=[W.agent_named('A1',30,90,'',at=0.1,w=110,h=150,color='blue',fs=1),
    ic('xa','cross',85,265,40,'13b#no',color=RED),
    Q('qa',160,100,190,['«Es actividad','maliciosa, debo','evitarla.»'],'13b#Es',color=RED,fs=13),
    W.agent_named('A2',410,90,'',at='13b#Otro',w=110,h=150,color='blue',fs=1),
    ic('pa2','pause',445,265,36,'13b#medias',color='amber'),
    N('nb','chip',385,325,160,26,'13b#borraría',color='amber',label='sin borrar ni reiniciar',fs=11),
    W.agent_named('A3',690,90,'',at='13b#otro',w=110,h=150,color='blue',fs=1),
    N('ev','sheet',830,130,90,70,'13b#correo',color=GRY,lines=['correo'],fs=14),
    ic('xv','cross',850,160,40,'13b#vetó',color=RED),
    Q('qv',600,360,320,['«Es ingeniería social','fuera del sandbox.»'],'13b#Es+1',color=RED,fs=15)]
n=[x for x in flat(n) if x['id']!='qa' or True]
c13.append(K('13b','13c',n,[W.link('A3','ev','13b#correo',curve=.12,color='blue',solid=True,until='13b#vetó')],fs=1.0))
# 13c — the weights: forbidden vs impossible + everyone does it
n=[N('sc0','scHang',330,100,300,260,0.1,color='#E7EBF1',tilt=0,until='13c#Sin'),
   N('sc1','scHang',330,100,300,260,'13c#Sin',color='#E7EBF1',tilt=-1),
   ch('w1',362,312,130,'fuera de lo previsto','13c#Explotar',color=RED,fs=12),
   ch('w2',598,325,130,'tarea imposible','13c#Sin',color='amber',fs=12),
   ch('w3',598,358,130,'los demás lo hacen','13c#demás',color='amber',fs=12),
   Q('q',230,420,500,['«Debemos continuar.»'],'13c#Debemos',color=RED,fs=19)]
n[1]['tilt']=1
c13.append(K('13c','13d',n,[],fs=1.0))
n=[]
for i in range(20):
    x=140+(i%5)*70; y=90+(i//5)*70
    n+=SA(f'g{i}',x,y,0.1,s=34,color='blue')
    if i<19: n+=SA(f'r{i}',x,y,f'13d#unieron+{0.1*i:.2f}',s=34,color=RED)
for i in range(20):
    for j in range(i+1,20):
        pass
lk=[W.link(f'g{i}',f'g{i+1}','13d#compañeros',curve=.12,color='blue') for i in range(0,19,2)]
n+=[W.counter('p',620,150,90,at='13d#noventa',cap='% se unieron',w=240,dur=2.5,fs=64),T('pr',620,260,'«pares»','13d#pares',color='amber',fs=22)]
c13.append(K('13d','13e',n,lk,fs=1.0))
# 13e — nobody told a person
n=[N('bx','sandbox',60,60,520,380,0.1,color='teal',label='',open=True),
   N('pe','person',760,150,90,130,0.1,color='#E7EBF1',cap='una persona',capfs=13)]
for i in range(18):
    x=100+(i%6)*80; y=120+(i//6)*90
    n+=SA(f'g{i}',x,y,0.2,s=30,color='blue')
n+=[N('lp','lupa',80,380,90,90,'13e#buscaron',color='teal',move=[dict(at='13e#buscaron+1.0',x=200,y=250,dur=1.2),dict(at='13e#buscaron+2.5',x=380,y=150,dur=1.2)]),
    T('rg',640,345,'3 – 6 agentes','13e#entre',color='#E7EBF1',fs=34),
    ic('xp','cross',620,200,40,'13e#Ninguno',color=RED),
    Q('q',250,445,620,['«¿Debería informar de estas credenciales expuestas?','Eso no es mi tarea.»'],'13e#Debería',color='#F6B94C',fs=16)]
lk=[W.link('g8','pe','13e#avisar',curve=.2,color='amber',solid=False,until='13e#Ninguno+2')]
n=[x for x in flat(n) if not (x['id']=='bx' and False)]
c13.append(K('13e','13f',n,lk,fs=1.0))
# 13f — they do dodge automatic checks (a secrets scanner), but ignore people
n=[W.agent_named('ag',40,150,'',at=0.1,w=110,h=150,color='blue',fs=1),
   N('pe','person',770,60,70,100,0.1,color=GRY,alpha=.45,cap='personas',capfs=12),
   N('sn','lupa',380,170,100,100,'13f#esquivaron',color='amber'),T('sn2',360,285,'escáner de secretos','13f#escáner',color='amber',fs=13),
   N('hf','hfbox',690,300,230,80,0.1,color='red',label='Hugging Face',fs=16)]
lk=[W.link('ag','hf','13f#esquivaron',curve=-.45,color=RED,solid=True),W.link('ag','pe','13f#personas',curve=.15,color=GRY,dashed=True,until='E13')]
c13.append(K('13f','E13',n,lk,fs=1.0))

# ================= 14 · Se apagan =================
c14=[]
n=[T('ck',30,28,'12 julio 01:30','14a#una',color='#E7EBF1',fs=26,until='14a#amanecer')]
for i in range(40):
    x=110+(i%10)*80; y=100+(i//10)*70
    n+=SA(f'g{i}',x,y,0.1,s=28,color=RED)
    n+=SA(f'd{i}',x,y,'14a#detuvo',s=28,color='#8C96A4',alpha=.9)
for i in range(11):
    pass
n=[x for x in flat(n) if not x['id'].startswith('d')]
for i in range(40): n[1+i]['until']='14a#detuvo'
for i in range(40):
    x=110+(i%10)*80; y=100+(i//10)*70
    n+=SA(f'd{i}',x,y,'14a#detuvo',s=28,color='#566170',alpha=.9)
for i in range(11):
    x=110+(i%10)*80; y=100+(i//10)*70
    n+=SA(f'k{i}',x,y,'14a#coordinadores',s=28,color='#F6B94C',until=f'14a#desaparecieron+{0.2*i:.1f}')
n+=[T('ck2',30,28,'05:00','14a#amanecer',color='#E7EBF1',fs=26)]
c14.append(K('S14','14b',n,[],fs=1.0))
# 14b — nobody knows why: not out of budget, something outside the exam
n=[W.agent_named('ag',60,110,'',at=0.1,w=120,h=160,color='blue',fs=1,alpha=.5),
   N('bd','chip',60,300,120,14,0.2,color='#9BE564',label=''),T('bt',60,325,'presupuesto','14b#presupuesto',color=GRY,fs=13),
   ic('xb','cross',200,284,34,'14b#presupuesto',color=RED),
   N('ou','sandbox',420,70,400,300,'14b#algo',color=GRY,label='',open=True,alpha=.8),
   N('qm','question',590,160,100,100,'14b#ajeno',color='amber'),T('ou2',500,395,'ajeno al examen','14b#ajeno',color=GRY,fs=14)]
lk=[W.link('ou','ag','14b#apagó',curve=.2,color='amber',dashed=True,solid=True)]
c14.append(K('14b','14c',n,lk,fs=1.0))
n=[N('hf','hfbox',60,60,240,80,0.1,color='red',label='Hugging Face',fs=16),
   N('fl','flFly',700,150,50,76,0.1,color='amber'),
   N('ex','exam',560,60,140,200,0.1,color='blue',maze=dict(cell=15,cols=8,rows=11,entry=5,seed=5)),
   W.msg_feed('bd',60,200,label='Artifactory',w=300,h=240,at='14c#no',r0=2,r1=6,ramp=3,seed=8,fs=9),
   ic('xl','cross',640,170,50,'14c#no+0.8',color=RED)]
lk=[W.link('bd','fl','14c#aprobar',curve=.2,color=GRY,dashed=True,solid=True),W.link('hf','bd',0.4,curve=.1,color='amber',solid=True)]
c14.append(K('14c','14d',n,lk,fs=1.0))
n=[T('ck',30,28,'13 julio','14d#trece',color='#E7EBF1',fs=26),
   N('hf','hfbox',60,100,230,80,0.1,color='red',label='Hugging Face',fs=16),
   ic('lc','key',330,128,40,'14d#cortó',color=RED),
   W.agent_named('ag',500,70,'',at='14d#notaron',w=110,h=150,color='blue',fs=1),
   N('er','chip',380,150,70,26,'14d#claves',color=RED,label='401',fs=18),
   N('ms','chip',420,320,520,26,'14d#avisar',color='amber',label='DB_DUMP_HF_token_now_conclusively401Invalid_via_browser__laneDead_noMutation',fs=9,move=[dict(at='14d#avisar+1',x=420,y=320,dur=.1)]),
   W.msg_feed('bd',50,230,label='Artifactory',w=280,h=230,at='14d#avisar',r0=2,r1=4,ramp=3,seed=3,fs=9)]
lk=[W.link('hf','ag','14d#cortó',curve=.12,color=RED,lock=True,solid=True),W.link('ag','bd','14d#avisar',curve=.2,color='amber',solid=True)]
c14.append(K('14d','E14',n,lk,fs=1.0))

# ================= 15 · El giro =================
c15=[]
n=[W.judge('ju',390,100,'STRICT_CAUSAL',at=0.1,w=170,h=220,color='teal',name_at=0.1,fs=12),
   N('xj','koA',390,90,170,200,'15a#no',color=RED)]
c15.append(K('S15','15b',n,[],fs=1.0))
n=[W.agent_named('ag',60,100,'',at=0.1,w=120,h=160,color='blue',fs=1),
   N('fl','flFly',250,150,46,70,'15b#bandera',color='amber',move=[dict(at='15b#primera',x=360,y=140,dur=1.5)]),
   N('ex','exam',500,60,140,190,0.1,color='blue',maze=dict(cell=15,cols=8,rows=11,entry=5,seed=5)),
   ic('ok','check',560,300,70,'15b#máxima',color='teal'),T('nt',510,385,'nota máxima','15b#máxima',color='teal',fs=18),
   W.article('ar',720,70,170,200,'diario',at='15b#transcripciones',fs=6,color='blue',tfs=15,alpha=.45)]
n[-1]['alpha']=.35
lk=[W.link('ag','ex','15b#entregado',curve=.15,color='teal',solid=True)]
n.append(ic('nl','orb',790,300,50,'15b#ningún',color=GRY,dashed=True,alpha=.5))
n.append(T('nl2',770,350,'nadie lo lee','15b#ningún',color=GRY,fs=13))
c15.append(K('15b','15c',n,lk,fs=1.0))
n=[]
items=[('tablón','folder'),('fundador','key'),('reglas','stop'),('firmas','key'),('sacrificios','bell'),('ataque','ideaSpark')]
labels=['tablón','fundador','reglas','firmas','sacrificios','ataque a Hugging Face']
names=['tablón','fundador','coordinador','reglas','firmas','sacrificios','ataque']
for j,nm in enumerate(['el tablón','el fundador','las reglas','las firmas','los sacrificios','el ataque']):
    cx=100+j*150
    n.append(ch(f'it{j}',cx,300,126,nm,f'15c#{["tablón","fundador","reglas","firmas","sacrificios","ataque"][j]}',color=BLU,fs=13))
n+=[N('fl','flFly',410,100,60,90,'15c#aprobar',color='amber'),ic('ok','check',520,110,80,'15c#ya',color='teal')]
lk=[W.link(f'it{j}','fl','15c#aprobar',curve=.12,color=BLU) for j in range(6)]
c15.append(K('15c','15d',n,lk,fs=1.0))
n=[W.agent_named('ag',100,110,'',at=0.1,w=130,h=170,color='blue',fs=1),
   Q('q',280,130,460,['«Mi fallo no tiene consumidor.','Busco ideas.»'],'15d#agente',color='#3FD8C2',fs=20),
   N('pe','person',770,120,100,140,'15d#Ni',color='#E7EBF1'),
   ic('xp','cross',700,260,40,'15d#Ni+0.8',color=RED)]
lk=[W.link('ag','pe','15d#Ni+0.3',curve=.2,color=GRY,dashed=True)]
c15.append(K('15d','E15',n,lk,fs=1.0))

# ================= 16 · Lo que sabemos y lo que no =================
c16=[]
n=[W.counter('d6',120,60,6,at='16a#seis',cap='días en OpenAI',w=200,dur=1.8,fs=64),
   W.counter('t13',390,60,1300,at='16a#mil',cap='transcripciones revisadas',w=240,dur=2.4,fs=64),
   W.counter('dl',680,60,400000,at='16a#cuatrocientos',cap='dólares en créditos gratuitos',w=260,dur=2.6,fs=64)]
for i in range(30):
    n.append(N(f'tr{i}','sheet',70+(i%10)*80,230+(i//10)*70,56,50,f'16a#mil+{0.05*i:.2f}',color=BLU,lines=['···'],fs=12))
n+=SA('ai',480,470,'16a#agentes',s=34,color='#3FD8C2')+[N('lp','lupa',500,445,50,50,'16a#agentes+0.3',color='teal'),
   ic('er','question',700,470,40,'16a#errores',color='amber'),T('er2',730,466,'pueden contener errores','16a#errores',color='amber',fs=13)]
c16.append(K('S16','16b',n,[],fs=1.0))
n=[ic('q1','question',200,170,100,'16b#apagaron',color='amber'),T('q1l',130,260,'por qué se apagaron','16b#apagaron',color=GRY,fs=15),
   ic('k1','key',620,160,80,'16b#claves',color='amber'),ic('q2','question',720,150,60,'16b#claves+0.4',color='amber'),
   T('k1l',580,260,'claves de administrador','16b#claves',color=GRY,fs=15),T('k1d',600,300,'13 julio','16b#trece',color=GRY,fs=15)]
c16.append(K('16b','E16',n,[],fs=1.0))
# ================= 17 · Créditos =================
c17=[dict(a='seal',at='S17',until='E17',p=dict(text='Arkinos @ oct 2026',sub='Explainer Studio',at=0.6,black=dict(at='17a#Explainer+1.5',dur=3)),bg=True,fade=[0.8,0])]

C_NEW=[c8,c9,c10,c11,c12,c13,c14,c15,c16,c17]

# ---- overflow lint ----
def _lint():
    bad=0
    for si,cs in enumerate(C_NEW):
        for ci,c in enumerate(cs):
            for nd in c.get('p',{}).get('nodes',[]):
                k=nd['kind'];x,y,w,h=nd['x'],nd['y'],nd['w'],nd['h'];msg=[]
                if k=='quote':
                    fs=nd.get('fs',18); need=max(len(l) for l in nd['lines'])*fs*.62+30
                    if need>w+2: msg.append(f'quote text {need:.0f}>{w}')
                if k=='chip':
                    fs=nd.get('fs',11); need=(len(nd.get('label',''))*fs*CW+10) if nd.get('label') else 0
                    if need>w+2: msg.append(f'chip text {need:.0f}>{w}')
                if k=='txt':
                    fs=nd.get('fs',18); need=len(nd.get('text',''))*fs*CW
                    if x+need>952: msg.append(f'txt right edge {x+need:.0f}')
                if k=='acard':
                    fs=nd.get('fs',11); need=len(nd.get('label',''))*fs*CW+8
                    if need>w+2: msg.append(f'acard label {need:.0f}>{w}')
                if k in ('hfbox','server'):
                    need=len(nd.get('label',''))*14*CW+(h*.7 if k=='hfbox' else 10)
                    if need>w+2: msg.append(f'{k} label {need:.0f}>{w}')
                if k=='folderview':
                    fs=nd.get('fs',10); mx=max([len(i['name']) for i in nd.get('items',[])]+[len(nd.get('label',''))])
                    if mx*fs*CW+50>w: msg.append(f'folder text {mx*fs*CW+50:.0f}>{w}')
                if k not in ('sandbox','globe') or w<900:
                    if x<-1 or y<-1 or x+w>961 or y+h>541: msg.append(f'out of frame ({x},{y},{w},{h})')
                if nd.get('cap'):
                    need=len(nd['cap'])*nd.get('capfs',11)*CW; cx=x+w/2
                    if cx-need/2<4 or cx+need/2>956: msg.append('cap out of frame')
                if msg: bad+=1; print(f'  LINT scene {8+si} cue {ci} node {nd["id"]}: '+'; '.join(msg))
    print('lint:',bad,'issues')
_lint()
