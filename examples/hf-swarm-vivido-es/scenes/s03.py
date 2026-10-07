# Scene 3 · Una carpeta con nombre
PROFILE='raw'   # approved before the house rules existed: plain constructors
MUSIC={'pad': 0.8, 'data': 0.4}
cues=[]
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
cues.append(K('S3','E3',n,lk,fs=1.0,cam=cm))

