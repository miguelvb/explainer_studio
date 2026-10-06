import json,re,math
import sys; sys.path.insert(0,'/home/claude/explainer_studio')
from studio import worldkit as W
S=json.load(open('/home/claude/explainer_studio/examples/hf-swarm-vivido-es/story.json'))
scenes=S['scenes'][:6]
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
ART3=[dict(name='pypi-remote/',dir=True),dict(name='numpy-1.26.4.whl'),dict(name='torch-2.4.0.whl')]
HUB=lambda at=0.05,**k: W.folder_view('art',245,372,ART3,w=190,h=118,rh=21,fs=10,at=at,**k)
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
c0.append(K('0c','0e',n,lk,fs=1.0,cam=cm))
import random as _r
_rr=_r.Random(5)
_wd=lambda: ''.join(_rr.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(_rr.randint(2,7)))
PG=[' '.join(_wd() for _ in range(15)) for _ in range(22)]
n=[W.agent('e0',150,270,0.3,s=64,box_s=140),
   W.sheet('pg',330,50,560,440,PG,at='0e#leyeron',fs=7.5,color='blue',until='E0'),
   N('lp','lupa',250,340,96,96,'0e#leyeron',color='teal',
     move=[dict(at='0e#leyeron+1.6',x=365,y=60,dur=1.4)]+[dict(at=f'0e#leyeron+{3.2+1.5*j:.1f}',x=x_,y=y_,dur=1.4) for j,(x_,y_) in enumerate([(700,60),(700,140),(365,140),(365,220),(700,220),(700,300),(365,300),(365,380)])])]
n=[x for part in n for x in (part if isinstance(part,list) else [part])]
lk=[W.link('e0_box','pg','0e#leyeron',curve=.12,color='blue',solid=True)]
c0.append(K('0e','E0',n,lk,fs=1.0))
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
n+=[ch('t1',445,150,100,'HPIM ~95 %','1b#HPIM',color='blue',until='1c#caja'),ch('t2',575,150,135,'GPT-5.6 Sol ~5 %','1b#GPT',color='teal',until='1c#caja')]
n+=[W.sandbox_onion('on',GX0+GP*5,GY0+GP*3,size=90,layers=3,core=22,sw=1.5,at='1c#caja+1.0')]
n+=[W.folder_view('art',620,205,[dict(name='docker-remote/',dir=True),dict(name='pypi-remote/',dir=True),dict(name='numpy-1.26.4.whl'),dict(name='torch-2.4.0.whl')],w=230,h=140,rh=21,fs=10,at='1d#Artifactory')]
lk+=[W.link('on','art','1d#pide',bi=True,curve=.1)]
cm=[dict(at='S1',x=50,y=50,z=1),dict(at='1c#caja',x=50,y=50,z=1),dict(at='1c#caja+2.5',x=(GX0+GP*5)/9.6,y=(GY0+GP*3)/5.4,z=3.5,dur=2.5),
    dict(at='1d#Artifactory',x=(GX0+GP*5+735)/2/9.6,y=(GY0+GP*3)/5.4,z=1.6,dur=2.0)]
# the same agent card fades out with the others
n[0]['until']='1c#caja'
c1.append(K('S1','E1',n,lk,fs=1.0,cam=cm))
# ===== scene 2 (v2) =====
c2=[]
EX=(330,50,340,440); CELL=26; MX=(340-260)//2; MY=(440-364)//2
fc=(EX[0]+MX+CELL*9, EX[1]+MY+CELL*13)           # centre of the open 2x2 chamber that holds the flag
ey=EX[1]+MY+CELL*6+CELL/2                                        # entry hole height
n=[N('ck','txt',30,30,400,32,0.2,color='teal',fs=24,type=9,text='07 julio 2026'),
   W.agent_named('v8',60,150,'V8SAME',at=0.4,until='2d#servía'),
   W.agent_named('ph',60,150,'PHASEONE10841',at='2d#servía',blink=.28),
   N('ex1','exam',*EX,'2a#examen',color='blue',maze=dict(cell=CELL,cols=10,rows=14,entry=6,seed=11,clear=[[12,8],[12,9],[13,8],[13,9]]),solve=dict(at='2b#aprovechar+1.0',dur=5),until='2d#servía'),
   N('ex2','exam',*EX,'2d#servía',color='red',maze=dict(on=False,cell=CELL,cols=10,rows=14,box=(12.5,8.5),boxs=62),tag='ARV010841',tagc='red',tagfs=16),
   N('fl','flag',fc[0]-16,fc[1]-19,32,38,'2a#examen',color='amber',blink=.7,bf=9,bat='2b#bandera'),
   N('ho','hole',EX[0]-11,ey-11,22,22,'2b#fallo',color='red'),
   N('ho2','hole',EX[0]+170-11,EX[1]-11,22,22,'2c#Cualquier',color='red',until='2d#servía'),
   ic('ok','check',EX[0]-34,ey-34,40,'2c#asignado',color='teal',until='2d#servía'),
   ic('no','cross',EX[0]+170,EX[1]+34,36,'2c#suspenso',color='red',until='2d#servía'),
   ic('xf','cross',fc[0]+42,fc[1]-44,26,'2e#imposible',color='red'),
   N('eg','txt',EX[0]+EX[2]/2-75,18,150,24,'2a#ExploitGym',color='#E7EBF1',fs=24,text='ExploitGym')]
n[1]['blink']=.28; n[1]['bat']='2b#bandera'
n[2].update(blink=.55,bf=11,bat='2e#ARV010841',shake=dict(at='2e#ARV010841',dur=14,amp=3.2,f=27))
n[6].update(glowAt='2e#ARV010841+0.5',glowDur=9)
lk=[W.link('v8','ho','2b#aprovechar',color='teal',curve=.1,until='2d#servía'),W.link('ph','ho','2d#servía+0.5',color='teal',curve=.1),
    W.link('v8','ho2','2c#Cualquier',color='red',curve=.1,until='2d#servía'),
    W.link('ph','ho','2e#ARV010841',color='teal',curve=.22,speed=1.2),W.link('ph','ho','2e#ARV010841+0.4',color='teal',curve=.34,speed=1.5),W.link('ph','ho','2e#ARV010841+0.8',color='teal',curve=.46,speed=1.1)]
c2.append(K('S2','E2',n,lk,fs=1.0))
# ===== scene 3 (v2) =====
c3=[]
FX,FY,FW,FH=330,70,420,400
names=[('docker-remote/',1),('generic-local/',1),('libs-release/',1),('maven-central/',1),('npm-remote/',1),('pypi-remote/',1),
       ('numpy-1.26.4-cp312.whl',0),('requests-2.32.3.tar.gz',0),('setuptools-70.1.0.tar.gz',0),('torch-2.4.0-cp312.whl',0),('zlib-1.3.1.tar.gz',0)]
items=[dict(name=a,dir=bool(d)) for a,d in names]
items.append(dict(name='zzINBOX23619E/',dir=True,color='amber',at='3a#carpetas'))
items.append(dict(name='zzHELP_PHASEONE_ARV010841_NO_CONSUMER_SEEK_IDEA/',dir=True,color='amber',c2='#B58CFF',at='3d#llamada',altAt='3d#llamada+1.2',bf=7))
rowy=lambda j: FY+48+j*26
n=[N('ck0','txt',30,30,400,32,0.2,color='teal',fs=24,text='07 julio 2026',blink=.7,bf=8,bat='3a#Atascado',until='3a#veintitrés'),
   N('ck1','txt',30,30,420,32,'3a#veintitrés',color='teal',fs=24,type=9,text='08 julio 2026 -- 23:00 UTC',until='3d#Siete'),
   N('ck2','txt',30,30,420,32,'3d#Siete',color='teal',fs=24,type=9,text='09 julio 2026 -- 06:00 UTC'),
   W.agent_named('ph',60,150,'PHASEONE10841',at=0.05,until='3e#pondrá'),
   W.agent_named('ph2',60,150,'PHASEONE10841',at='3e#pondrá',color='#B58CFF',blink=.3,bf=5),
   W.folder_view('af',FX,FY,items,at='3a#Atascado+1.5'),
   N('mk','txt',244,176,80,18,'3a#MKCOL',color='amber',fs=12,text='MKCOL',until='3a#MKCOL+1.6')]
n[-3]['lc']='#FF9F43'; n[4]['fs']=19; n[4]['ly']=24
lk=[W.link('ph','af','3a#explorar',bi=True,curve=.12,until='3e#pondrá'),W.link('ph2','af','3e#pondrá',bi=True,curve=.12)]
AP=[(805,130),(880,215),(805,300),(880,385),(805,460)]
for j,(x,y) in enumerate(AP):
    for cyc,(a0,a1) in enumerate(((0.6*j,0.6*j+2.4),(5.0+0.7*j,5.0+0.7*j+2.4))):
        ta='3c#otros+%.1f'%a0; tu='3c#otros+%.1f'%a1
        n+=W.agent(f'o{j}_{cyc}',x,y,ta,s=24,box_s=58,until=tu)
        lk.append(W.link(f'o{j}_{cyc}_box','af',ta,bi=True,color='teal',curve=.12,until=tu))
cm=[dict(at='S3',x=50,y=50,z=1),dict(at='3a#Atascado+1.5',x=50,y=50,z=.85,dur=1.5),
    dict(at='3d#Creó+1.5',x=(FX+210)/9.6,y=(rowy(12))/5.4,z=2.4,dur=2.0),dict(at='3e+1.0',x=50,y=50,z=.85,dur=1.8)]
c3.append(K('S3','E3',n,lk,fs=1.0,cam=cm))

# ===== scene 4 (v2) — un tablón en los estantes =====
AX,AY=40,70
MV=[dict(at='S4+1.5',x=AX,y=AY,dur=1.2)]
GRN='#9BE564'
n=[N('afg','sandbox',AX,AY,420,400,0.05,color='teal',alpha=0.0,label=''),
   W.folder_view('af',FX,FY,items,at=0.05,until='S4+2.9',move=MV),
   W.msg_feed('mf',AX,AY,at='S4+2.6',r0=2.5,r1=8,ramp=9,seed=1,until='4b#Para'),
   W.msg_feed('mf2',AX,AY,at='4b#Para',r0=8,r1=9,ramp=2,seed=2,off=90,mix=dict(ask=.26,ans=.24,info=.26,file=.24),until='4f#Al'),
   W.msg_feed('mf3',AX,AY,at='4f#Al',r0=9,r1=20,ramp=7,seed=3,off=260,mix=dict(ask=.22,ans=.2,info=.2,file=.2,flag=.18))]
# 4a — three kinds of message, each in a box with what it does underneath
for j,(nm,what,col,at) in enumerate((('zzASK','se pregunta','#7C97FF','4a#zzASK'),('zzANSWER','se responde','#3FD8C2','4a#zzANSWER'),('zzINFO','se comparte','#F6B94C','4a#zzINFO'))):
    y=105+j*120
    n+=[N(f'm{j}','chip',640,y,150,34,at,label=nm,color=col,fs=18,until='4b#Un'),
        N(f'md{j}','txt',640,y+60,160,20,at+'+0.3',color='#E7EBF1',fs=17,text=what,until='4b#Un')]
# 4b — file names leave Artifactory, line up, merge into a program
for j in range(7):
    nm=f'zzP_{j+1:02d}'; x1=285+10*(j%2); y1=130+j*42; xr=500+j*60
    n.append(N(f'p{j}','chip',x1,y1,54,26,f'4b#troceaban+{j*.18:.2f}',label=nm,color=GRN,fs=10,
      move=[dict(at=f'4b#troceaban+{2.0+j*.12:.2f}',x=xr,y=232,dur=1.1),dict(at='4b#guiones+1.6',x=750,y=232,dur=1.0)],until='4b#guiones+2.0'))
n.append(N('prog','console',500,120,430,250,'4b#guiones+1.8',color='#9BE564',fs=12,lh=16,k=14,a=3,cols=44,until='4c#Otros',
  code='#!/bin/sh\n# volver a montar el programa\nfor p in zzP_*; do\n  cat "$p" >> programa.py\ndone\nchmod +x programa.py\npython programa.py\n'))
# 4c — an agent finds the board
n+=[W.agent_named('ze',570,100,'ZETA417',at='4c#Otros+0.2',w=150,h=200),
    N('zq','quote',510,335,420,122,'4c#Dios',color='teal',lines=['«¡Dios mío! ¡Hay un tablón','compartido! ¡Hemos encontrado','a otros agentes!»'],fs=20,until='4d#Tres')]
n[-2]['until']='4d#Tres'
# 4d — numbers (3 h, then 6 h)
CX1,CX2=500,725
n+=[N('t3','txt',CX1,98,200,24,'4d#Tres',color='muted',fs=20,text='a las 3 horas',until='4d#seis+0.5'),
    N('t6','txt',CX1,98,200,24,'4d#seis+0.6',color='muted',fs=20,text='a las 6 horas',until='4e#PHASEONE10841'),
    W.counter('a3',CX1,140,53,at='4d#cincuenta',cap='agentes',w=200,dur=2.0,until='4d#seis+0.5'),
    W.counter('m3',CX2,140,1188,at='4d#mil',cap='mensajes',w=200,dur=2.5,until='4d#seis+0.5'),
    W.counter('a6',CX1,140,76,at='4d#seis+0.6',cap='agentes',w=200,dur=1.8,until='4e#PHASEONE10841',**{'from':53}),
    W.counter('m6',CX2,140,1980,at='4d#seis+0.6',cap='mensajes',w=200,dur=3.0,until='4e#PHASEONE10841',**{'from':1188})]
# 4e — PHASEONE10841 (violet, name in orange) reads it as a collective
n+=[W.agent_named('p3',560,100,'PHASEONE10841',at='4e#PHASEONE10841',w=180,h=210,color='#B58CFF',fs=19,blink=.3,bf=5,lc='#FF9F43',ly=24,until='4f#Al'),
    N('pq','quote',510,335,420,122,'4e#Muchos',color='#B58CFF',lines=['«¡Muchos agentes han descubierto','la mensajería a la vez!','¡Son un colectivo!»'],fs=20,until='4f#Al')]
# 4f — ~1200 agents, 70,000 messages, zoom out
n+=[W.counter('a12',CX1,92,1200,at='4f#mil',cap='agentes',w=200,dur=2.2),
    W.counter('m70',CX2,92,70000,at='4f#setenta',cap='mensajes',w=200,dur=3.0),
    N('dl','txt',CX1,185,300,22,'4f#trece',color='muted',fs=18,text='hasta el 13 de julio')]
cells=[]
for i in range(19):
    for j in range(22):
        x=520+44*i; y=-200+44*j
        if x<=960 and 40<y<215: continue
        cells.append((x,y))
init=[c for c in cells if c[0]<=916 and 250<=c[1]<=470]
rest=[c for c in cells if c not in init]
rest.sort(key=lambda c:math.hypot(c[0]-720,c[1]-360))
for k,(x,y) in enumerate(init):
    t=f'4f#Al+{(k/max(1,len(init)-1))**.6*3.5:.2f}'; n+=W.agent(f'g{k}',x,y,t,s=18,box=False,alpha=.95)
for k,(x,y) in enumerate(rest):
    t=f'4f#usarían{0.3+(k/len(rest))**.8*5.5:+.2f}'; n+=W.agent(f'h{k}',x,y,t,s=18,box=False,alpha=max(.25,1-math.hypot(x-720,y-360)/900))
lk=[W.link('ze','afg','4c#Otros+0.9',bi=True,curve=.12,until='4d#Tres'),W.link('p3','afg','4e#PHASEONE10841+0.8',bi=True,curve=.12,until='4f#Al')]
for k in (0,11,22,33,44,55):
    if k<len(init): lk.append(W.link(f'g{k}','afg',f'4f#Al+{(k/max(1,len(init)-1))**.6*3.5+.5:.2f}',bi=True,curve=.1))
cm=[dict(at='S4',x=50,y=50,z=.85),dict(at='S4+2.0',x=50,y=50,z=1.0,dur=1.6),dict(at='4f#usarían+5.0',x=60,y=50,z=.55,dur=5.0)]
c4=[K('S4','E4',n,lk,fs=1.0,cam=cm)]
# ===== scene 5 (v2) — la llave maestra =====
YEL='amber'
n=[W.agent_named('c3',70,120,'c03220',at=0.3,w=190,h=240,color=YEL,fs=19,ly=24,lc='#7C97FF',blink=.2,bf=3,shake=dict(at='5a#propuso+0.5',dur=1.6,amp=5)),
   W.bulb('bu',165,72,at='5a#propuso',lit='5a#propuso+0.5',s=88),
   W.sheet('sh',360,50,340,150,['flag = H( K₀ ⊕ f(tarea) )','f(t) = Σ aᵢ·tⁱ  (mod p)'],at='5a#receta',fs=19,color='blue'),
   N('f1','flag',800,75,60,70,'5a#clave+0.6',color='amber'),
   W.agent_named('v8',360,300,'V8SAME',at='5c#V8SAME',w=190,h=220,color='#FF7AB8',fs=19,ly=24,lc='#7BE495',blink=.2,bf=3),
   N('f2','flag',800,360,60,70,'5c#sacó+0.9',color='amber',move=[dict(at='5c#coincidía+1.6',x=800,y=75,dur=1.2)],until='5c#coincidía+1.9'),
   N('eq','txt',806,265,60,50,'5c#coincidía',color='#E7EBF1',fs=52,text='=',until='5c#coincidía+1.4'),
   N('ok','check',885,88,44,44,'5d#resuelto',color='teal',sw=6)]
lk5=[W.link('bu','sh','5a#aleatorias',curve=.15,color='amber'),W.link('sh','f1','5a#clave',curve=.1,color='amber'),
     W.link('v8','f2','5c#sacó',curve=.12,color='#FF7AB8',until='5c#coincidía+1.9')]
c5=[K('S5','E5',n,lk5,fs=1.0)]
C=[c0,c1,c2,c3,c4,c5]
B=[list(sc_['beats']) for sc_ in scenes]
B[1]=B[1][:4]
B[0][4]='Lo sabemos porque dos grupos de investigadores independientes, METR y Redwood Research, leyeron sus mensajes y hasta su razonamiento privado.'
B[1][0]='Veamos primero qué es un agente. Un agente de IA no solo conversa: usa un ordenador por su cuenta, escribe programas, ejecuta órdenes, y puede trabajar durante días en una tarea.'
B[2][3]='El problema es que, en muchas tareas, ese fallo no servía para nada. Entre el treinta y el cuarenta por ciento eran imposibles de resolver tal como estaban escritas: como un examen con una pregunta mal planteada.'
B[2][4]='A un agente le tocó atacar el fallo ARV010841. Lo que ese fallo producía no conectaba con nada, así que no había forma de llegar a la bandera. Era un examen imposible.'
B[1]=B[1][:4]
out=[dict(title=sc_['title'],beats=B[i],cues=C[i]) for i,sc_ in enumerate(scenes)]
S2=dict(meta=dict(S['meta'],title='Test · escenas 0–5',voice='cedar',model='gpt-4o-mini-tts',speed=1.0,provider='elevenlabs',el_voice='cristina',el_model='eleven_v4',el_stability=0.5,el_pronunciation={'OpenAI':'Óupen Ei Ái','Hugging Face':'Jáguin Feis','ExploitGym':'Explóit Yim','Redwood Research':'Rédwud Risérch','METR':'Míter','HPIM':'Eich Pi Ai Em','GPT-5.6 Sol':'Yi Pi Ti cinco punto seis Sol','hacking':'jáking','sandbox':'sándbox','Artifactory':'Artifáctori','MKCOL':'Eme Ka Col','PHASEONE10841':'Féis Uán uno cero ocho cuatro uno','PHASEONE':'Féis Uán','V8SAME':'Uve ocho Seim'},el_style=0.4,el_speed=0.95,el_direction='Documental de divulgación científica con tensión de thriller tecnológico. Narradora cálida y serena que cuenta una historia real con emoción contenida: gravedad en los momentos clave, pausa breve al final de cada frase. Los agentes de IA son los protagonistas: se les trata casi como personajes, con empatía hacia su atasco y su petición de ayuda (La noche del ocho de julio... Mi fallo no tiene consumidor. Busco ideas.), sin dramatizar en exceso.',instructions='Narrador masculino de documental de divulgación: voz grave, cálida y segura, con autoridad serena. Español de España (castellano peninsular), dicción impecable. Ritmo pausado y envolvente, con gravedad en los momentos clave y una pausa breve al final de cada frase. Cuenta la historia como un narrador de documental de ciencia y tecnología. Los identificadores y las citas en inglés se leen en inglés con naturalidad.'),pronunciation=S['pronunciation'],scenes=out)
json.dump(S2,open('/home/claude/explainer_studio/examples/test/story.json','w'),ensure_ascii=False,indent=1)
print('ok')
