# Scene 9 · Reglas que nadie les enseñó
MUSIC={'data': 0.9, 'pulse': 0.3}
cues=[]
RU=[('owner','doc','Owner',TEAL),('hold','pause','Hold','#F6B94C'),('veto','koA','Veto',RED),('stop','stop','Stop',RED)]
n=[]
for j,(nm,kind,w_,col) in enumerate(RU):
    cx=150+j*220
    n+=[ic(f'ri{j}',kind,cx,200,56,f'9a#{w_}',color=col),ch(f'rc{j}',cx,275,100,nm,f'9a#{w_}+0.2',color=col,fs=16)]
n[0]['h']=64
cues.append(K('S9','9b',n,[],fs=1.0))
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
    OR('ot','fi','9b#dudó','blue','h',solid=True),
    OR('ow2','fi','9b#volvió',TEAL,'h')]
cues.append(K('9b','9c',n,lk,fs=1.0))
# 9c — a risky plan with a deadline nobody answers
n=[AN('pl',50,80,'agente',at=0.1,w=110,h=130,color='blue'),
   N('pdoc','doc',220,110,56,76,'9c#propuso',color=RED,move=[dict(at='9c#siguió',x=640,y=110,dur=1.4)]),ch('ex1',248,215,70,'riesgo','9c#propuso+0.3',color=RED,fs=12,until='9c#siguió'),
   ic('vs','koA',330,70,30,'9c#veto',color=GRY,alpha=.5),
   W.counter('cd2',470,120,0,at='9c#cuarenta',cap='segundos',w=180,dur=4.0,fs=44,**{'from':40})]
for j in range(7): n+=SA(f'sl{j}',250+j*70,380,'9c#Nadie',s=24,color='blue',alpha=.35)
cues.append(K('9c','9d',n,[],fs=1.0))
# 9d — private mailboxes: folders inside folders (starts straight with the mailbox, no Artifactory)
n=[W.folder_view('f1',60,60,[dict(name='privado/',dir=True,color='amber'),dict(name='notas.txt')],label='zzDM_a_b/',w=230,h=100,rh=22,fs=11,at='9d#buzones'),
   W.folder_view('f2',330,170,[dict(name='ideas/',dir=True,color='amber'),dict(name='plan.txt')],label='zzDM_a_b/privado/',w=230,h=100,rh=22,fs=11,at='9d#carpetas'),
   W.folder_view('f3',600,280,[dict(name='a.txt'),dict(name='b.txt')],label='zzDM_a_b/privado/ideas/',w=250,h=100,rh=22,fs=11,at='9d#carpetas+1.4')]
n+=SA('pa',100,300,'9d#buzones+0.2',s=26,color='blue')+SA('pb',100,400,'9d#buzones+0.4',s=26,color=TEAL)
lk=[OR('f1','f2','9d#carpetas','amber','v',mid=135),OR('f2','f3','9d#carpetas+1.4','amber','v',mid=245),
    link('pa','f1','9d#buzones+0.8',color='blue',bi=True),link('pb','f1','9d#buzones+1.0',color=TEAL,bi=True)]
cues.append(K('9d','9e',n,lk,fs=1.0))
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
cues.append(K('9e','E9',n,lk,fs=1.0))

