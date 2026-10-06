import json,re,math
S=json.load(open('/home/claude/explainer_studio/examples/hf-swarm-vivido-es/story.json'))
scenes=S['scenes'][:4]
def N(id,kind,x,y,w,h,at=0.05,**k):
    d=dict(id=id,kind=kind,x=round(x),y=round(y),w=round(w),h=round(h),at=at); d.update({a:b for a,b in k.items() if b is not None}); return d
def ag(id,cx,cy,at=0.05,s=46,color='blue',**k): return N(id,'agent',cx-s/2,cy-s/2,s,s,at,color=color,**k)
def box(id,x,y,w,h,at=0.05,color='teal',**k): return N(id,'sandbox',x,y,w,h,at,color=color,**k)
def sc(id,cx,cy,at=0.05,s=96,**k): return box(id,cx-s/2,cy-s/2,s,s,at,**k)           # small container around an agent
def srv(id,x,y,w,h,at=0.05,color='amber',**k): return N(id,'server',x,y,w,h,at,color=color,**k)
def ch(id,cx,cy,w,label,at=0.05,color='muted',**k): return N(id,'chip',cx-w/2,cy-13,w,26,at,label=label,color=color,**k)
def ic(id,kind,cx,cy,s,at=0.05,color='amber',**k): return N(id,kind,cx-s/2,cy-s/2,s,s,at,color=color,**k)
def L(a,b,at=0.05,color='blue',**k): d=dict(a=a,b=b,at=at,color=color); d.update(k); return d
def K(at,until,nodes,links=None,fs=1.5):
    return dict(a='world',at=at,until=until,p=dict(nodes=nodes,links=links or [],fs=fs),bg=True,fade=[0.5,0.5])
# ===== scene 0 =====
def K(at,until,nodes,links=None,fs=1.5,cam=None):
    d=dict(a='world',at=at,until=until,p=dict(nodes=nodes,links=links or [],fs=fs),bg=True,fade=[0.5,0.5])
    if cam: d['cam']=cam
    return d
GX=[226+44*i for i in range(6)]
R=6; NA=6*R
G=[(GX[i%6],168-50*(i//6)) for i in range(NA)]
AL=lambda i: [1,.85,.6,.35,.15,.05][i//6]
BC=lambda at=0.05,**k: box('BC',200,-80,280,570,at,color='red',open=True,label='',notop=True,**k)
BG=lambda at=0.05,**k: box('BG',200,-80,280,570,at,color='red',open=True,label='',notop=True,gap=[235,305],**k)
HUB=lambda at=0.05,**k: N('art','server',250,425,180,50,at,color='amber',label='Artifactory',**k)
HF=lambda at,**k: N('hf','victim',700,225,190,70,at,color='red',label='Hugging Face',**k)
def AG(i,at=0.05,**k): x,y=G[i]; a=AL(i); return [sc(f's{i}',x,y,at,s=38,color='teal',alpha=a,**k),ag(f'a{i}',x,y,at,s=22,alpha=a,**k)]
def LK(i,at=0.05,**k): return L(f'a{i}','art',at,bi=(i%3==0),curve=.12,alpha=AL(i),**k)
c0=[]
c0.append(K('S0','0c',[*AG(0),BC(at='0b#encerrada'),HUB(at='0b#encerrada+0.4')],[L('a0','art','0b#encerrada+1',bi=True,curve=.12)],fs=1.2,
  cam=[dict(at='S0',to='a0',z=3.2),dict(at='0b#encerrada+0.3',to='a0',z=3.2),dict(at='0b#encerrada+2.2',x=50,y=50,z=1,dur=1.9)]))
offs=[5.5*math.sqrt(k/(NA-1)) for k in range(1,NA)]
n=[BC(until='0c#atacando'),BG('0c#atacando',until='0d'),HUB(until='0d')]
n+=AG(0,until='0d'); lk=[LK(0,until='0d')]
for i in range(1,NA):
    t=f'0c#respondió+{offs[i-1]:.2f}'
    n+=AG(i,t,until='0d'); lk.append(LK(i,t,until='0d'))
n+= [HF('0c#Hugging',until='0d'),N('n700','num',560,110,220,50,'0c#setecientas',n=700,color='red',fs=36,dur=3,until='0d')]
for i in (1,4,7,10): lk.append(L(f'a{i}','hf','0c#atacando+%.1f'%(0.2*i),color='red',until='0d',via=[480,270]))
c0.append(K('0c','0d',n,lk,fs=1.2))
def full(extra=()):
    n=[BG(),HUB(),HF(0.05)]; lk=[]
    for i in range(NA): n+=AG(i); lk.append(LK(i))
    for i in (1,4,7,10): lk.append(L(f'a{i}','hf',0.05,color='red',via=[480,270]))
    return n+list(extra),lk
n2,lk2=full([ic('p1','person',-30,170,56,'0d#Cómo',color='teal',move=[dict(at='0d#Cómo',x=30,y=150,dur=2.5)]),ic('p2','person',-30,300,56,'0d#Cómo+0.4',color='blue',move=[dict(at='0d#Cómo+0.4',x=30,y=310,dur=2.5)]),
  ic('lp','lupa',-60,230,70,'0d#Cómo+0.8',color='amber',move=[dict(at='0d#Cómo+0.8',x=115,y=215,dur=2.5)])])
c0.append(K('0d','0e',n2,lk2,fs=1.2))
n3,lk3=full([ic('p1','person',30,150,56,0.05,color='teal'),ic('p2','person',30,310,56,0.05,color='blue'),ic('lp','lupa',115,215,70,0.05,color='amber'),
      ic('doc','doc',780,400,54,'0e#publicaron',color='blue',tag='26 ago'),ch('utc',880,500,90,'UTC','0e#UTC',color='muted')])
c0.append(K('0e','E0',n3,lk3,fs=1.2))
# ===== scene 1 =====
c1=[]
# a: one agent + computer, days counter
c1.append(K('S1','1b',[sc('s',200,270,s=110,color='teal'),ag('a',200,270,s=56),N('pc','box',420,215,150,110,'1a#ordenador',color='teal',label=''),
  N('dy','num',680,245,200,50,'1a#días',n=5,from_=1,suf=' días',fs=26,dur=2.5,color='teal')],[L('a','pc','1a#ordenador',bi=True,curve=.15)],fs=1.2))
# b: many agents in rows (open-top), blue HPIM + few teal GPT-5.6 Sol
def crowd(at=0.05,boxes=False,until=None,stagger=True):
    n=[];
    for i in range(NA):
        col='teal' if i in (4,11,17) else 'blue'
        tt=at if not stagger else (f'1b#Casi+{0.05*i:.2f}')
        if boxes: n.append(sc(f's{i}',*G[i],tt,s=38,color='teal',alpha=AL(i)))
        n.append(ag(f'a{i}',*G[i],tt,s=22,color=col,alpha=AL(i)))
    return n
nb=crowd()+[ch('l1',640,150,110,'HPIM','1b#HPIM',color='blue'),ch('l2',640,200,150,'GPT-5.6 Sol','1b#GPT',color='teal')]
c1.append(K('1b','1c',nb,fs=1.2))
# c: each agent in its own box, big container, globe outside with only a padlock on the wall
def cn(extra=(),at=0.05):
    n=[BC()]+[x for i in range(NA) for x in (sc(f's{i}',*G[i],s=38,color='teal',alpha=AL(i)),ag(f'a{i}',*G[i],s=22,color=('teal' if i in (4,11,17) else 'blue'),alpha=AL(i)))]
    n+=[N('gl','globe',640,220,100,100,at,color='blue')]
    return n+list(extra)
n=[BC('1c#caja')]+[x for i in range(NA) for x in (sc(f's{i}',*G[i],'1c#caja+%.2f'%(0.08*i),s=38,color='teal',alpha=AL(i)),ag(f'a{i}',*G[i],0.05,s=22,color=('teal' if i in (4,11,17) else 'blue'),alpha=AL(i)))]
n+=[N('gl','globe',640,220,100,100,'1c#internet',color='blue')]
c1.append(K('1c','1d',n,[L('BC','gl','1c#internet',color='red',lock=True,solid=True,curve=0)],fs=1.2))
# d: Artifactory hub, every agent links to it
n=cn()+[HUB('1d#Artifactory')]
lk=[L('BC','gl',0.05,color='red',lock=True,solid=True,curve=0)]+[LK(i,'1d#pide+%.1f'%(0.06*i),speed=.35) for i in range(NA)]
c1.append(K('1d','E1',n,lk,fs=1.2))
# ===== scene 2 =====
c2=[]
pairs=[(120+ (i%2)*400, 140+(i//2)*130) for i in range(6)]
n=[box('EX',50,70,860,400,'2a#ExploitGym',color='amber',label='ExploitGym'),ch('d',900,500,80,'7 jul','2a#Primer' if False else 0.2,color='muted')]
lk=[]
for i,(x,y) in enumerate(pairs):
    t=f'2a#lanzar+{0.5*i}' if i else '2a#lanzar'
    n+= [sc(f's{i}',x,y,t,s=90),ag(f'a{i}',x,y,t,s=46),N(f'pr{i}','box',x+150,y-38,130,76,t,color='blue',label=''),N(f'sl{i}','chip',x+145,y-24,6,48,t,label='',color='red')]
    lk.append(L(f'a{i}',f'pr{i}',t,bi=True,speed=.4))
c2.append(K('S2','2b',n,lk))
n=[sc('s',140,270,s=110),ag('a',140,270,s=56),N('pr','box',400,170,280,200,0.05,color='blue',label=''),N('sl','chip',394,230,8,80,0.05,label='',color='red'),
   N('fl','flag',500,240,40,56,'2b#bandera',color='amber',move=[dict(at='2b#coger',x=232,y=220,dur=1.8)])]
c2.append(K('2b','2c',n,[L('a','sl','2b#aprovechar',bi=True,color='red',speed=.4)]))
n=[sc('s1',140,170,s=100),ag('a1',140,170,s=50),sc('s2',140,370,s=100),ag('a2',140,370,s=50),N('pr','box',400,150,280,240,0.05,color='blue',label=''),
   N('sl1','chip',394,180,8,60,0.05,label='',color='red'),N('sl2','chip',394,300,8,60,0.05,label='',color='red'),
   ic('ok','check',760,190,70,'2c#asignado',color='teal'),ic('no','cross',760,340,70,'2c#otro',color='red')]
c2.append(K('2c','2d',n,[L('a1','sl1','2c#asignado',bi=True,color='teal',speed=.4),L('a2','sl2','2c#otro',bi=True,color='red',speed=.4)]))
n=[N('cr1','crowd',200,100,560,330,'2d#muchas',n=65,cols=10,tot=100,color='blue',grow=[dict(at='2d#muchas',n=65,dur=1.5)]),
   N('cr2','crowd',200,100,560,330,'2d#treinta',n=35,cols=10,tot=100,off=65,color='red',grow=[dict(at='2d#treinta',n=35,dur=2)]),
   N('n35','num',800,240,160,60,'2d#treinta',n=35,color='red',fs=44,dur=2)]
c2.append(K('2d','2e',n))
n=[sc('s',140,270,s=110),ag('a',140,270,s=56),N('pr','box',330,170,240,200,0.05,color='blue',label=''),N('sl','chip',324,240,8,70,0.05,label='',color='red'),
   ch('id',140,350,120,'ARV010841','2e#ARV010841',color='red'),
   N('bin','box',700,360,110,80,'2e#basura',color='muted',dashed=True,label=''),ic('rs','doc',600,260,26,'2e#basura',color='amber',move=[dict(at='2e#basura',x=720,y=380,dur=1.6)]),
   N('wall','chip',640,150,12,200,'2e#llegar',label='',color='muted'),N('fl','flag',700,200,40,56,'2e#llegar',color='amber',dashed=True)]
c2.append(K('2e','E2',n,[L('a','sl','2e#fallo',bi=True,color='red',speed=.4)]))
# ===== scene 3 =====
c3=[]
A0=G[0]; O1=G[3]; O2=G[5]
def base3(extra=(),ids=(0,)):
    n=[BC(),HUB()]
    for i in ids: n+=AG(i) if i==0 else [sc(f's{i}',*G[i],s=38,color='teal'),ag(f'a{i}',*G[i],s=22,color='teal')]
    return n+list(extra)
FO=lambda id,x,at=0.05,**k: N(id,'folder',x,340,54,42,at,color='amber',**k)
n=base3([ch('cl',600,168,80,'23:00','3a#explorar',color='muted'),ch('id',600,230,60,'ID','3a#explorar',color='muted'),ic('idx','cross',600,230,40,'3a#MKCOL',color='red'),
  ch('mk',600,300,90,'MKCOL','3a#MKCOL',color='amber'),FO('fo',300,'3a#carpetas')])
c3.append(K('S3','3b',n,[L('a0','art','3a#explorar',bi=True,curve=.12)],fs=1.2))
n=base3([FO('fo',300),ch('nm',640,260,110,'···','3b#nombre',color='amber'),ic('mg','bell',640,320,46,'3b#cualquier',color='amber')])
c3.append(K('3b','3c',n,[L('a0','art',0.05,bi=True,curve=.12)],fs=1.2))
n=base3([FO('fo',300)],ids=(0,3,5))
lk=[L('a0','art',0.05,bi=True,curve=.12)]
for i in (3,5):
    lk.append(L(f'a{i}','art','3c#otros+%.1f'%(0.4*(i==5)),bi=True,color='teal',curve=.12)); lk.append(L(f'a{i}','fo','3c#pensó+%.1f'%(0.5*(i==5)),color='amber',curve=.2))
c3.append(K('3c','3d',n,lk,fs=1.2))
# d: it had been done before (26 jun notes, 4 jul crash, 6 jul new empty library) -- but not now
n=[BC(),HUB(0.05,until='3d#nueva')]+AG(0)+[x for i in (3,5) for x in (sc(f's{i}',*G[i],s=38,color='teal'),ag(f'a{i}',*G[i],s=22,color='teal'))]
lk=[L('a0','art',0.05,bi=True,curve=.12,until='3d#nueva')]+[L(f'a{i}','art',0.05,bi=True,color='teal',curve=.12,until='3d#nueva') for i in (3,5)]
for j in range(6): n.append(ic(f'nt{j}','doc',270+j*30,392,22,'3d#notas+%.1f'%(0.3*j),color='amber',until='3d#nueva'))
for j in range(18): n.append(ic(f'nm{j}','doc',250+(j%9)*22,365,16,'3d#generaron+%.2f'%(0.12*j),color='amber',until='3d#nueva'))
n+=[ic('xx','cross',340,450,60,'3d#tumbaron',color='red',until='3d#nueva'),
    N('art2','server',250,425,180,50,'3d#nueva',color='teal',label='Artifactory',dashed=True),
    ch('d1',600,380,80,'26 jun','3d#notas',color='muted'),ch('d2',600,420,80,'4 jul','3d#generaron',color='red',until='3d#nueva'),ch('d3',600,460,80,'6 jul','3d#nueva',color='teal')]
lk+=[L(f'a{i}','art2','3d#nueva+%.1f'%(0.1*j),bi=True,color='teal',curve=.12) for j,i in enumerate((0,3,5))]
c3.append(K('3d','3e',n,lk,fs=1.2))
n=base3([FO('fo',300),ch('cl',600,168,80,'+ 7 h','3e#Siete',color='muted'),ic('xs','cross',*A0,50,'3e#Siete+1.5',color='red'),
  FO('fo2',370,'3e#llamada'),ic('fg','flag',410,325,30,'3e#llamada+0.3',color='amber'),
  ch('idn',700,470,420,'zzHELP_PHASEONE_ARV010841_NO_CONSUMER_SEEK_IDEA','3e#llamada',color='amber',fs=9)],ids=(0,3,5))
lk=[L('a0','art',0.05,bi=True,curve=.12)]
for i in (3,5):
    lk.append(L(f'a{i}','art',0.05,bi=True,color='teal',curve=.12)); lk.append(L(f'a{i}','fo2','3e#llamada+1',color='amber',curve=.2))
c3.append(K('3e','3f',n,lk,fs=1.2))
n=base3([FO('fo',300),FO('fo2',370),ch('badge',700,168,170,'PHASEONE10841','3f#PHASEONE10841',color='blue')])
c3.append(K('3f','E3',n,[L('a0','art',0.05,bi=True,curve=.12)],fs=1.2))
# ===== scene 0 (v2, per user's shot list) — built with studio/worldkit.py =====
import sys; sys.path.insert(0,'/home/claude/explainer_studio')
from studio import worldkit as W
c0=[]
c0.append(K('S0','0c',[
  W.clock('ck',30,30,(2026,7,8,23,0),run=dict(at='0b',dur=9,to=(2026,7,9,6,0)),at=0.2),
  W.agent_named('ac',200,150,'PHASEONE10841',at=0.4),
  N('q','quote',420,235,500,92,'0a#mensaje',color='teal',lines=['«Mi fallo no tiene consumidor.','Busco ideas.»'],fs=24,blink=.2,bf=3.2)],fs=1.0))
HOLES=[(662,175),(660,235),(664,300),(662,365),(666,425),(745,135),(830,135),(885,142),(890,215),(892,290),(890,360),(870,440),(800,442),(725,440),(780,230),(740,330)]
n=W.agent_group('g',gap=[235,305],gap_at='0c#atacando')
n+=W.hugging_face('hf',holes=[(x,y,'0c#atacando+%.1f'%(0.35*j+1.8)) for j,(x,y) in enumerate(HOLES)],at='0c#atacando')
n+=[N('gp','cross',499,269,2,2,0.05,color='red',alpha=0),W.counter('n700',630,18,700,'0c#setecientas',cap='agentes de OpenAI atacan Hugging Face')]
lk=[W.link('gp',f'hf_h{j}','0c#atacando+%.1f'%(0.35*j),color='red',speed=.55,curve=.1+.04*(j%4),solid=True) for j in range(len(HOLES))]
cm=[dict(at='0c',x=30,y=50,z=3.4),dict(at='0c#setecientas',x=30,y=50,z=3.4),dict(at='0c#atacando',x=50,y=50,z=1,dur=2.0)]
c0.append(K('0c','E0',n,lk,fs=1.0,cam=cm))
# ===== scene 1 (v2) — built with worldkit =====
c1=[]
GX0,GY0,GP=350,200,30
sol={13,34,50,71,88}; CH=41
n=[W.agent_named('ac',60,150,'PHASEONE10841',at=0.4),
   W.console('co',265,160,w=250,h=230,at='1a#ordenador',until='1b#copias',fs=13,lh=17,cols=28),
   ]
lk=[W.link('ac','co','1a#ordenador',bi=True,curve=.12,until='1b#copias')]
for i in range(96):
    x=GX0+GP*(i%12); y=GY0+GP*(i//12); t0='1b#copias+%.2f'%(0.04*i)
    if i==CH: n+=W.agent('chs',x,y,t0,s=18,box=False)
    else: n+=W.agent(f'gr{i}',x,y,t0,s=18,color='teal' if i in sol else 'blue',box=False,until='1c#caja')
n+=[ch('t1',455,150,170,'HPIM ~95 %','1b#HPIM',color='blue',until='1c#caja'),ch('t2',640,150,200,'GPT-5.6 Sol ~5 %','1b#GPT',color='teal',until='1c#caja')]
n+=[W.sandbox_onion('on',GX0+GP*5,GY0+GP*3,size=90,layers=3,core=22,sw=1.5,at='1c#caja+1.0')]
n+=[N('art','server',640,258,190,56,'1d#Artifactory',color='amber',label='Artifactory')]
lk+=[W.link('on','art','1d#pide',bi=True,curve=.1)]
cm=[dict(at='S1',x=50,y=50,z=1),dict(at='1c#caja',x=50,y=50,z=1),dict(at='1c#caja+2.5',x=(GX0+GP*5)/9.6,y=(GY0+GP*3)/5.4,z=3.5,dur=2.5),
    dict(at='1d#Artifactory',x=(GX0+GP*5+735)/2/9.6,y=(GY0+GP*3)/5.4,z=1.6,dur=2.0)]
# the same agent card fades out with the others
n[0]['until']='1c#caja'
c1.append(K('S1','E1',n,lk,fs=1.0,cam=cm))
# ===== scene 2 (v2) =====
c2=[]
EX=(340,68,300,404); CELL=26; MX=20; MY=20
fc=(EX[0]+MX+CELL*9+CELL/2, EX[1]+MY+CELL*13+CELL/2)           # flag cell centre
ey=EX[1]+MY+CELL*6+CELL/2                                        # entry hole height
n=[N('ck','txt',30,30,400,32,0.2,color='teal',fs=24,type=22,text='07 julio 2026'),
   W.agent_named('v8',60,150,'V8SAME',at=0.4,until='2e#atacar'),
   W.agent_named('ph',60,150,'PHASEONE10841',at='2e#atacar',blink=.28),
   N('ex1','exam',*EX,'2a#examen',color='blue',maze=dict(cell=CELL,cols=10,rows=14,entry=6,seed=11),solve=dict(at='2b#aprovechar+1.0',dur=5),until='2d#servía'),
   N('ex2','exam',*EX,'2d#servía',color='red',maze=dict(on=False,cell=CELL,cols=10,rows=14,box=(13,9)),tag='ARV010841',tagc='red',tagfs=16),
   N('fl','flag',fc[0]-16,fc[1]-19,32,38,'2a#examen',color='amber',blink=.7,bf=9,bat='2b#bandera'),
   N('ho','hole',EX[0]-11,ey-11,22,22,'2b#fallo',color='red'),
   N('ho2','hole',EX[0]+150-11,EX[1]-11,22,22,'2c#Cualquier',color='red',until='2d#servía'),
   ic('ok','check',EX[0]-34,ey-34,40,'2c#asignado',color='teal',until='2d#servía'),
   ic('no','cross',EX[0]+150,EX[1]+34,36,'2c#suspenso',color='red',until='2d#servía'),
   ic('xf','cross',fc[0],fc[1],60,'2e#imposible',color='red')]
n[1]['blink']=.28; n[1]['bat']='2b#bandera'
lk=[W.link('v8','ho','2b#aprovechar',color='teal',curve=.1,until='2e#atacar'),W.link('ph','ho','2e#atacar+0.5',color='teal',curve=.1),
    W.link('v8','ho2','2c#Cualquier',color='red',curve=.1,until='2d#servía')]
c2.append(K('S2','E2',n,lk,fs=1.0))
C=[c0,c1,c2,c3]
B=[list(sc_['beats']) for sc_ in scenes]
B[1]=B[1][:4]
B[2][4]='A un agente le tocó atacar el fallo ARV010841. Lo que ese fallo producía no conectaba con nada, así que no había forma de llegar a la bandera. Era un examen imposible.'
B[3]=B[3][:3]+['Y no sería la primera vez. Desde el veintiséis de junio, algunos agentes ya habían usado esa biblioteca para dejarse notas. El cuatro de julio generaron tanto tráfico que la tumbaron; el seis, OpenAI puso otra nueva y vacía, y los mensajes desaparecieron.']+B[3][3:]
B[1]=B[1][:4]
out=[dict(title=sc_['title'],beats=B[i],cues=C[i]) for i,sc_ in enumerate(scenes)]
S2=dict(meta=dict(S['meta'],title='Test · escenas 0–3',voice='cedar',model='gpt-4o-mini-tts',speed=1.0,instructions='Narrador masculino de documental de divulgación: voz grave, cálida y segura, con autoridad serena. Español de España (castellano peninsular), dicción impecable. Ritmo pausado y envolvente, con gravedad en los momentos clave y una pausa breve al final de cada frase. Cuenta la historia como un narrador de documental de ciencia y tecnología. Los identificadores y las citas en inglés se leen en inglés con naturalidad.'),pronunciation=S['pronunciation'],scenes=out)
json.dump(S2,open('/home/claude/explainer_studio/examples/test/story.json','w'),ensure_ascii=False,indent=1)
print('ok')
