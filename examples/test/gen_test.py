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
R=7; NA=6*R
G=[(GX[i%6],340-50*(i//6)) for i in range(NA)]
AL=lambda i: [1,.92,.78,.62,.46,.3,.16][i//6]
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
BC1=lambda at=0.05,**k: box('BC',50,60,720,430,at,color='teal',**k)
c1.append(K('S1','1b',[sc('s',190,270,s=120),ag('a',190,270,s=60),N('pc','box',440,230,130,80,'1a#ordenador',color='teal',label=''),ch('cmd',440,340,150,'$ …','1a#órdenes',color='amber'),
  N('dy','num',640,240,200,50,'1a#días',n=5,from_=1,suf=' días',fs=26,dur=2.5,color='teal')],[L('a','pc','1a#ordenador',bi=True)]))
nb=[];cols=8
for i in range(40):
    x=150+(i%cols)*70; y=130+(i//cols)*70
    teal = i%cols>=7 and i//cols<2 or (i==38)
    nb.append(ag(f'g{i}',x,y,f'1b#Casi+{0.04*i:.2f}',s=40,color='teal' if teal else 'blue'))
nb+= [ch('l1',320,470,120,'HPIM','1b#HPIM',color='blue'),ch('l2',710,470,150,'GPT-5.6 Sol','1b#GPT',color='teal')]
c1.append(K('1b','1c',nb))
pos=[(150+(i%4)*130,130+(i//4)*100+10) for i in range(12)]
def c_nodes(at=0.05,art=False,keep=None):
    n=[BC1(at)]
    for i,(x,y) in enumerate(pos):
        n+= [sc(f's{i}',x,y,at if at!=0.05 else 0.05,s=90),ag(f'a{i}',x,y,at if at!=0.05 else 0.05,s=46)]
    n+= [ic('gl','globe',860,270,100,at,color='blue')]
    return n
n=[BC1('1c#caja')]
for i,(x,y) in enumerate(pos): n+= [sc(f's{i}',x,y,f'1c#caja+{0.1*i}',s=90),ag(f'a{i}',x,y,f'1c#caja+{0.1*i}',s=46)]
n+= [N('gl','globe',810,220,100,100,'1c#internet',color='blue')]
c1.append(K('1c','1d',n,[L('BC','gl','1c#internet',color='red',lock=True,solid=True)]))
n=c_nodes()+[srv('art',640,200,100,150,'1d#Artifactory')]
lk=[L(f'a{i}','art','1d#pide+%.1f'%(0.08*i),bi=True,speed=.35) for i in range(12)]
c1.append(K('1d','1e',n,lk))
n=c_nodes()+[srv('art',640,200,100,150,0.05,until='1e#nueva',dashed=False)]
lk=[L(f'a{i}','art',0.05,bi=True,speed=.35,until='1e#nueva') for i in range(12)]
for j in range(6): n.append(ic(f'nt{j}','doc',612+ (j%3)*28,215+(j//3)*30,22,'1e#notas+%.1f'%(0.3*j),color='amber',s=0) if False else ic(f'nt{j}','doc',612+(j%3)*28,215+(j//3)*30,22,'1e#notas+%.1f'%(0.3*j),color='amber',until='1e#nueva'))
for j in range(14): n.append(ic(f'nm{j}','doc',590+(j%7)*18,205+(j//7)*34,16,'1e#generaron+%.2f'%(0.12*j),color='amber',until='1e#nueva'))
n+= [ic('xx','cross',690,200,60,'1e#tumbaron',color='red',until='1e#nueva'),srv('art2',640,200,100,150,'1e#nueva',color='teal',dashed=True),
     ch('d1',700,175,80,'26 jun','1e#notas',color='muted'),ch('d2',700,150,80,'4 jul','1e#generaron',color='red',until='1e#nueva'),ch('d3',700,150,80,'6 jul','1e#nueva',color='teal')]
lk+= [L(f'a{i}','art2','1e#nueva+%.1f'%(0.06*i),bi=True,speed=.35) for i in range(12)]
c1.append(K('1e','E1',n,lk))
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
BC3=lambda at=0.05,**k: box('BC',50,60,860,420,at,color='teal',**k)
base=lambda: [BC3(),sc('s',150,270,s=110),ag('a',150,270,s=56),srv('art',640,150,200,230,color='amber')]
n=base()+[ch('cl',150,170,80,'23:00','3a#explorar',color='muted'),N('id','chip',390,262,60,26,'3a#explorar',label='ID',color='muted'),ic('idx','cross',420,255,40,'3a#MKCOL',color='red'),
  ch('mk',400,320,90,'MKCOL','3a#MKCOL',color='amber'),N('fo','folder',650,400,64,50,'3a#carpetas',color='amber')]
c3.append(K('S3','3b',n,[L('a','art',0.05,bi=True)]))
n=base()+[N('fo','folder',650,400,64,50,0.05,color='amber'),ch('nm',682,350,100,'···','3b#nombre',color='amber'),ic('mg','bell',770,350,46,'3b#cualquier',color='amber')]
c3.append(K('3b','3c',n,[L('a','art',0.05,bi=True)]))
n=base()+[N('fo','folder',650,400,64,50,0.05,color='amber')]
lk=[L('a','art',0.05,bi=True)]
for i,(y) in enumerate((120,420)):
    n+= [sc(f'o{i}',150,y,'3c#otros+%.1f'%(0.4*i),s=100,color='teal'),ag(f'ao{i}',150,y,'3c#otros+%.1f'%(0.4*i),s=46,color='teal')]
    lk.append(L(f'ao{i}','art','3c#otros+%.1f'%(0.4*i+0.3),bi=True,color='teal'))
    lk.append(L(f'ao{i}','fo','3c#pensó+%.1f'%(0.5*i),color='amber'))
n+= [ic('bl','question',150,200,30,'3c#pensó',color='amber')] if False else []
c3.append(K('3c','3d',n,lk))
n=base()+[N('fo','folder',650,400,64,50,0.05,color='amber'),ch('cl',150,170,80,'+ 7 h','3d#Siete',color='muted'),ic('xs','cross',150,270,70,'3d#solución' if False else '3d#Siete+1.5',color='red'),
  N('fo2','folder',740,400,64,50,'3d#Creó' if False else '3d#llamada',color='amber'),ic('fg','flag',775,385,30,'3d#llamada+0.3',color='amber'),
  ch('idn',700,470,420,'zzHELP_PHASEONE_ARV010841_NO_CONSUMER_SEEK_IDEA','3d#llamada',color='amber',fs=0.8)]
lk=[L('a','art',0.05,bi=True)]
for i,y in enumerate((120,420)):
    n+= [sc(f'o{i}',150,y,s=100,color='teal'),ag(f'ao{i}',150,y,s=46,color='teal')]
    lk.append(L(f'ao{i}','art',0.05,bi=True,color='teal'))
    lk.append(L(f'ao{i}','fo2','3d#llamada+1',color='amber'))
c3.append(K('3d','3e',n,lk))
n=base()+[N('fo','folder',650,400,64,50,0.05,color='amber'),N('fo2','folder',740,400,64,50,0.05,color='amber'),ch('badge',150,200,170,'PHASEONE10841','3e#PHASEONE10841',color='blue')]
c3.append(K('3e','E3',n,[L('a','art',0.05,bi=True)]))
C=[c0,c1,c2,c3]
out=[dict(title=sc_['title'],beats=sc_['beats'],cues=C[i]) for i,sc_ in enumerate(scenes)]
S2=dict(meta=dict(S['meta'],title='Test · escenas 0–3'),pronunciation=S['pronunciation'],scenes=out)
json.dump(S2,open('/home/claude/explainer_studio/examples/test/story.json','w'),ensure_ascii=False,indent=1)
print('ok')
