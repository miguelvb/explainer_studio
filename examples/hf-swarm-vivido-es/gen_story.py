import json,re
P='/home/claude/explainer_studio/examples/hf-swarm-vivido-es/'
txt=open(P+'script-v1.md').read()
if '## 17 ·' not in txt:
    txt=txt.rstrip('\n')+'\n\n## 17 · Créditos\na. Arkinos, octubre de dos mil veintiséis. Explainer Studio.\n'
    open(P+'script-v1.md','w').write(txt)
scenes=[]
for blk in re.split(r'\n## ',txt)[1:]:
    head,*lines=blk.strip().split('\n')
    n,title=head.split(' · ',1)
    beats=[re.sub(r'^[a-z]\. ','',l).replace('`','') for l in lines if re.match(r'^[a-z]\. ',l)]
    scenes.append(dict(n=int(n),title=title,beats=beats))
BIG={'agent':1.4,'folder':1.4,'flag':1.4,'doc':1.4,'eye':1.3,'key':1.3,'person':1.4,'cross':1.3,'check':1.3,'question':1.2,'bell':1.4,'pause':1.4,'stop':1.3,'chip':1.0}
def N(id,kind,x,y,w,h,at,**k):
    f=BIG.get(kind,1.0)
    if f!=1.0:
        x-= (w*f-w)/2; y-=(h*f-h)/2; w*=f; h*=f
    d=dict(id=id,kind=kind,x=x,y=y,w=w,h=h,at=at); d.update({a:b for a,b in k.items() if b is not None}); return d
def AG(id,x,y,at,label=None,color='blue',s=46,**k): return N(id,'agent',x,y,s,s,at,label=label,color=color,**k)
def FO(id,x,y,at,cap=None,color='amber',w=46,h=36,**k): return N(id,'folder',x,y,w,h,at,cap=cap,color=color,**k)
def FL(id,x,y,at,color='teal',w=36,h=48,**k): return N(id,'flag',x,y,w,h,at,color=color,**k)
def DOC(id,x,y,at,color='blue',w=38,h=48,**k): return N(id,'doc',x,y,w,h,at,color=color,**k)
def EYE(id,x,y,at,color='amber',w=70,h=36,**k): return N(id,'eye',x,y,w,h,at,color=color,**k)
def KEY(id,x,y,at,color='amber',w=70,h=30,**k): return N(id,'key',x,y,w,h,at,color=color,**k)
def CH(id,x,y,w,at,label,color='amber',**k): return N(id,'chip',x,y,w,26,at,label=label,color=color,**k)
def CR(id,x,y,w,h,at,n,color='blue',**k): return N(id,'crowd',x,y,w,h,at,n=n,color=color,**k)
def SB(id,x,y,w,h,at,label=None,color='teal',**k): return N(id,'sandbox',x,y,w,h,at,label=label,color=color,**k)
def PE(id,x,y,at,label=None,color='muted',s=44,**k):
    cap=k.pop('cap',label)
    return N(id,'person',x,y,s,s,at,cap=cap,color=color,**k)
def NUM(id,x,y,at,n,color='amber',w=120,fs=24,**k): return N(id,'num',x,y,w,40,at,n=n,color=color,fs=fs,**k)
def QU(id,x,y,at,s=56,color='amber',**k): return N(id,'question',x,y,s,s,at,color=color,**k)
def X(id,x,y,at,s=30,color='red',**k): return N(id,'cross',x,y,s,s,at,color=color,**k)
def OK(id,x,y,at,s=30,color='teal',**k): return N(id,'check',x,y,s,s,at,color=color,**k)
def SRV(id,x,y,w,h,at,label,sub=None,color='amber',**k): return N(id,'server',x,y,w,h,at,label=label,sub=sub,color=color,**k)
def BX(id,x,y,w,h,at,label,color='blue',**k): return N(id,'box',x,y,w,h,at,label=label,color=color,**k)
def GL(id,x,y,s,at,label='Internet',color='blue',**k): return N(id,'globe',x,y,s,s,at,label=label,color=color,**k)
def L(a,b,at,color='amber',**k): d=dict(a=a,b=b,at=at,color=color); d.update(k); return d
NB={sc['n']:len(sc['beats']) for sc in scenes}
def _idx(anchor):
    if anchor is None: return 99
    m=re.match(r'^>?(\d+)([a-z])',str(anchor))
    if str(anchor).startswith('E'): return 99
    return ord(m.group(2))-97 if m else 0
def W(n,nodes,links=None,cam=None,fade=(0.5,0.5),until=None):
    nu={}
    for d in nodes:
        keep=d.pop('keep',0)
        if 'until' not in d and keep!='*':
            b=_idx(d['at'])+1+keep
            d['until']=f'{n}{chr(97+b)}' if b<NB[n] else f'E{n}'
        nu[d['id']]=d.get('until')
    for l in links or []:
        if 'until' not in l:
            ua,ub=nu.get(l['a']),nu.get(l['b'])
            u=ua if _idx(ua)<=_idx(ub) else ub
            if u and not str(u).startswith('E'): l['until']=u
    c=dict(_n=n,a='world',at=f'S{n}',until=until or f'E{n}',p=dict(nodes=nodes,links=links or [],fs=1.3),bg=True,fade=list(fade))
    if cam: c['cam']=cam
    return c
CF=dict(capm=True,capfs=9)   # mono small caption for ids
C={}
# ---------------- 0 gancho
C[0]=[W(0,[
 SB('sb',150,170,200,200,'0b#encerrada',color='teal',label='su caja',until='0e'),
 AG('a1',225,245,0.5,'una IA',until='0e'),
 FO('f1',560,235,'0a#mensaje',cap='zzHELP_PHASEONE_ARV010841_NO_CONSUMER_SEEK_IDEA',capm=True,capfs=10,until='0e'),
 AG('a2',720,160,'0c#respondió',color='teal',s=40,until='0e'),
 CR('cw',380,330,300,150,'0c#setecientas',90,color='blue',grow=[dict(at='0c#setecientas',n=90,dur=3)],cap='≈ 700 copias de la IA',until='0e'),
 N('hf','victim',700,330,160,80,'0c#Hugging',label='Hugging Face',sub='plataforma de IA',color='red',until='0e'),
 QU('q',450,110,'0d#Cómo',until='0e'),
 PE('p1',250,230,'0e#grupos','METR',color='teal'),PE('p2',400,230,'0e#grupos+0.3','Redwood Research',color='blue'),
 DOC('d1',640,225,'0e#publicaron',color='amber',cap='26 ago 2026'),
 CH('ch',405,400,150,'0e#UTC','horas · UTC',color='muted'),
 ],[
 L('a1','f1','0a#mensaje',color='blue',until='0e'),L('f1','a2','0c#respondió',color='teal',until='0e'),
 L('cw','hf','0c#Hugging',color='red',until='0e')])]
# ---------------- 1 cajas selladas
C[1]=[W(1,[
 AG('ag',100,240,0.4,color='blue',s=60,until='1b'),
 BX('pc',225,235,130,80,'1a#ordenador','ordenador',color='teal',until='1b'),
 DOC('pg',440,235,'1a#escribe',color='blue',cap='programas',until='1b'),
 CH('cm',560,256,150,'1a#órdenes','$ ejecutar',color='amber',until='1b'),
 NUM('dy',770,255,'1a#días',5,color='teal',from_=1,dur=2.5,suf=' días',until='1b'),
 CR('hp',180,190,420,160,'1b#Casi',95,color='blue',cols=19,grow=[dict(at='1b#Casi',n=95,dur=2.5)],cap='HPIM · modelo interno',capc='blue'),
 CR('so',660,250,110,24,'1b#GPT',5,color='teal',cols=5,grow=[dict(at='1b#GPT',n=5,dur=1)],cap='GPT-5.6 Sol',capc='teal'),
 SB('s1',130,205,200,150,'1c#caja',color='teal',label='sandbox · sin internet',keep=1),AG('g1',210,255,'1c#caja',s=40,keep=1),
 SB('s2',380,205,200,150,'1c#ordenador',color='teal',keep=1),AG('g2',460,255,'1c#ordenador',s=40,keep=1),
 SB('s3',630,205,200,150,'1c#archivos',color='teal',keep=1),AG('g3',710,255,'1c#archivos',s=40,keep=1),
 GL('gl',445,30,60,'1c#internet',color='blue'),
 SRV('lib',330,395,300,90,'1d#Artifactory','Artifactory','biblioteca interna',keep=1,move=[dict(at='1e#notas',x=200,y=395,dur=1)]),
 FO('n1',330,325,'1e#notas',color='amber',w=34,h=28,until='1e#tumbaron'),FO('n2',380,325,'1e#notas',color='amber',w=34,h=28,until='1e#tumbaron'),FO('n3',430,325,'1e#notas',color='amber',w=34,h=28,until='1e#tumbaron'),
 X('xs',372,318,'1e#tumbaron',s=44,color='red',until='1e#nueva',tag='4 jul',tagc='red'),
 SRV('lib2',700,395,210,90,'1e#nueva','biblioteca nueva',None,color='teal',dashed=True,tag='6 jul',tagc='teal'),
 ],[
 L('s2','gl','1c#internet',color='red',lock=True),
 L('s1','s2','1c#demás',color='muted',lock=True),L('s2','s3','1c#demás',color='muted',lock=True),
 L('g1','lib','1d#pide',color='amber'),L('g2','lib','1d#pide',color='amber'),L('g3','lib','1d#pide',color='amber')])]
# ---------------- 2 examen
C[2]=[W(2,[
 CR('ag',100,170,280,160,'2a#lanzar',60,color='blue',grow=[dict(at='2a#lanzar',n=60,dur=2.5)],until='2b'),
 CH('ex',520,235,140,'2a#ExploitGym','ExploitGym',color='amber',until='2b',tag='7 jul',tagc='muted'),
 AG('a',120,230,'2b#agente',s=50,until='2d'),
 BX('pr',400,160,260,180,'2b#programa','programa real',color='blue',until='2d'),
 CH('fa',620,180,70,'2b#fallo','fallo',color='red',until='2d'),
 FL('fl',470,240,'2b#bandera',color='amber',cap='la bandera',until='2d'),
 OK('ok',310,208,'2c#asignado',s=26,until='2d'),
 X('xo',300,285,'2c#otro',s=30,until='2d',tag='suspenso',tagc='red'),
 CR('t1',280,150,360,230,'2d#muchas',100,color='teal',cols=10,grow=[dict(at='2d#muchas',n=100,dur=1.8)],until='2e'),
 CR('t2',280,150,360,230,'2d#treinta',35,color='red',cols=10,tot=100,off=0,grow=[dict(at='2d#treinta',n=35,dur=2)],cap='35 de cada 100 tareas, imposibles',capc='red',until='2e'),
 AG('b',100,235,'2e#agente',s=50),
 BX('p2',380,170,240,170,'2e#agente','programa',color='blue'),
 CH('fb',560,190,110,'2e#ARV010841','ARV010841',color='red'),
 BX('bin',760,215,120,50,'2e#basura','descartado',color='muted'),
 FL('fz',470,260,'2e#llegar',color='amber',dashed=True,cap='bandera'),
 ],[
 L('a','fa','2b#aprovechar',color='red',until='2d'),L('fl','a','2b#coger',color='amber',until='2d'),
 L('b','fb','2e#fallo',color='blue'),L('fb','bin','2e#basura',color='red'),L('fb','fz','2e#ninguna',color='muted',lock=True)])]
# ---------------- 3 carpeta
C[3]=[W(3,[
 AG('ag',110,260,0.3,'el agente',s=52,keep='*'),
 SRV('lib',400,190,260,130,'3a#explorar','Artifactory','biblioteca',tag='8 jul · 23:00 UTC',tagc='muted',keep='*'),
 CH('mk',250,225,100,'3a#MKCOL','MKCOL',color='amber'),
 FO('fo',480,350,'3a#carpetas',cap=None,color='amber',w=64,h=50,keep=2),
 CH('nm',380,415,250,'3b#nombre','un nombre es un mensaje',color='muted'),
 AG('o1',780,200,'3c#otros',s=34,color='teal',keep='*'),AG('o2',820,290,'3c#otros',s=34,color='teal',keep='*'),AG('o3',780,380,'3c#otros',s=34,color='teal',keep='*'),
 CH('th',70,385,300,'3c#pensó','«podríamos comunicarnos por los nombres»',color='blue',fs=10,until='3d'),
 CH('ct',110,130,100,'3d#Siete','+ 7 horas',color='muted',until='3e'),
 CH('hp',70,385,340,'3d#castellano','«Ayuda. Mi fallo no tiene consumidor…»',color='blue',until='3e'),
 CH('nmz',330,95,300,'3e#PHASEONE10841','PHASEONE10841',color='blue'),
 dict(id='fo2',kind='chip',x=200,y=455,w=500,h=28,at='3d#llamada',label='zzHELP_PHASEONE_ARV010841_NO_CONSUMER_SEEK_IDEA',color='amber',fs=9,until='3e'),
 ],[
 L('ag','lib','3a#explorar',color='blue'),L('o1','lib','3c#otros',color='teal'),L('o2','lib','3c#otros',color='teal'),L('o3','lib','3c#otros',color='teal')])]
# ---------------- 4 tablón
C[4]=[W(4,[
 SRV('lib',240,310,480,80,'4a#zz','Artifactory · el tablón',None,color='amber',until='4b'),
 FO('fa',300,225,'4a#zzASK',cap='zzASK',color='blue',capm=True,until='4b'),
 FO('fb',450,225,'4a#zzANSWER',cap='zzANSWER',color='teal',capm=True,until='4b'),
 FO('fc',600,225,'4a#zzINFO',cap='zzINFO',color='amber',capm=True,until='4b'),
 DOC('dA',220,235,'4b#programa',color='blue',w=48,h=60,until='4c'),
 CR('tr',330,200,300,130,'4b#cientos',60,color='amber',cols=12,grow=[dict(at='4b#troceaban',n=60,dur=3)],until='4c'),
 DOC('dB',700,235,'4b#montarlo',color='teal',w=48,h=60,until='4c'),
 AG('c1',250,260,'4c#Otros',s=36,until='4d'),AG('c2',400,170,'4c#empezaron',s=36,until='4d'),AG('c3',560,170,'4c#encontrarlo',s=36,until='4d'),AG('c4',700,260,'4c#Uno',s=36,color='teal',cap='¡otros agentes!',capc='teal'),
 CR('cr',190,180,400,160,'4d#Tres',76,color='teal',cols=14,grow=[dict(at='4d#Tres',n=53,dur=1.5),dict(at='4d#seis',n=76,dur=1.5)],until='4e'),
 NUM('m1',670,205,'4d#Tres',1188,color='amber',dur=2.5,suf=' mensajes',fs=20,w=220,until='4e'),
 NUM('m2',670,275,'4d#seis',1953,color='amber',dur=2,suf=' mensajes',fs=20,w=220,until='4e'),
 AG('ph',200,250,'4e#PHASEONE10841',s=50,color='blue',label='PHASEONE10841'),
 FO('hf',340,255,'4e#petición',color='amber',cap=None),
 CR('cl',470,190,290,150,'4e#colectivo',50,color='teal',cols=10,grow=[dict(at='4e#colectivo',n=50,dur=1.5)]),
 CR('big',150,150,660,230,'4f#Al',400,color='blue',cols=40,grow=[dict(at='4f#Al',n=400,dur=5)],cap='≈ 1.200 agentes',capc='blue'),
 NUM('mm',380,410,'4f#setenta',70000,color='amber',dur=3,pre='+',suf=' mensajes y archivos',fs=20,w=360),
 ],[L('hf','cl','4e#petición',color='amber')])]
for nd in C[4][0]['p']['nodes']:
    if nd['id'] in ('ph','hf','cl'): nd['until']='4f'
C[4][0]['p']['links'][0]['until']='4f'
# ---------------- 5 llave maestra
C[5]=[W(5,[
 AG('c3',150,245,0.5,'c03220',s=50,until='5b'),
 FL('fl',650,235,'5a#banderas',color='amber',until='5b'),
 BX('re',390,250,140,60,'5a#receta','receta',color='blue',until='5b'),
 DOC('dd',340,140,'5a#datos',color='teal',cap='datos de la tarea',until='5b'),
 KEY('ke',480,145,'5a#clave',color='amber',cap='clave por defecto',until='5b',tag='pública',tagc='red'),
 KEY('mk',390,150,'5b#llave',color='amber',w=170,h=60,tag='la llave maestra',tagc='amber',until='5c'),
 FL('f1',280,300,'5b#fabricar',color='teal',w=30,h=40,until='5c'),FL('f2',380,300,'5b#fabricar+0.4',color='teal',w=30,h=40,until='5c'),
 FL('f3',480,300,'5b#cualquier',color='teal',w=30,h=40,until='5c'),FL('f4',580,300,'5b#cualquier+0.4',color='teal',w=30,h=40,until='5c'),FL('f5',680,300,'5b#entrar',color='teal',w=30,h=40,until='5c'),
 AG('v8',170,240,'5c#Otro',s=46,label='V8SAME'),
 BX('pg',320,225,150,80,'5c#sacó','su programa',color='blue'),
 FL('fr',520,230,'5c#sacó+1',color='teal',cap='real'),FL('fc',640,230,'5c#sacó+1.5',color='amber',cap='calculada'),
 OK('ck',580,160,'5c#coincidía',s=44),
 CR('all',230,170,500,170,'5d#pocas',80,color='teal',cols=20,grow=[dict(at='5d#pocas',n=80,dur=3)]),
 OK('ck2',450,380,'5d#resuelto',s=60),
 ],[L('dd','re','5a#datos',color='teal',until='5b'),L('ke','re','5a#clave',color='amber',until='5b'),L('re','fl','5a#defecto',color='amber',until='5b'),
    L('v8','pg','5c#sacó',color='blue'),L('pg','fr','5c#sacó+1',color='teal')])]
# ---------------- 6 envenenados
C[6]=[W(6,[
 AG('ag',170,250,0.4,s=52,until='6d'),
 FL('fl',340,245,'6a#bandera',color='amber',until='6d'),
 DOC('ar',500,130,'6a#artículo',color='blue',cap='artículo',until='6b'),
 EYE('ey',690,240,'6a#corrector',color='amber',w=110,h=56,dashed=True,cap='corrector',keep='*'),
 DOC('tr',480,235,'6b#transcripción',color='blue',w=48,h=60,cap='el diario',until='6d'),
 FL('f2',488,270,'6b#primer',color='amber',w=20,h=26,until='6d'),
 OK('ap',570,385,'6b#Aprobado',s=34,tag='fallo asignado',tagc='teal',until='6d'),
 X('su',740,385,'6b#Suspenso',s=34,tag='atajo',tagc='red',until='6d'),
 CH('sc',600,165,170,'6c#STRICT','STRICT_CAUSAL',color='amber',until='6d'),
 AG('ag2',170,250,'6d#envenenado',s=52,color='red',cap='envenenado'),
 FL('fp',340,245,'6d#envenenado',color='red',state='poisoned'),
 DOC('tp',480,235,'6d#diario',color='red',w=48,h=60),
 KEY('ke',390,120,'6e#llave',color='amber',w=150,h=56),
 ],[L('fl','ey','6a#entregar',color='amber',until='6b'),L('tr','ey','6b#Leería',color='blue',until='6d'),L('tp','ey','6d#diario',color='red',until='6e'),L('ke','ey','6e#usarla',color='amber',lock=True)])]
# ---------------- 7 reescribir el diario
C[7]=[W(7,[
 CR('c0',330,170,300,170,'7a#uno',100,color='muted',cols=20,grow=[dict(at='7a#uno',n=100,dur=1)],until='7b'),
 CR('c1',330,170,300,170,'7a#cinco',20,color='amber',cols=20,tot=100,grow=[dict(at='7a#cinco',n=20,dur=1.8)],cap='1 de cada 5 habló de manipular su transcripción',capc='amber',until='7b'),
 DOC('dd',190,235,'7a#diarios',color='blue',cap='diarios',until='7b'),
 EYE('ey',710,235,'7a#corrector',color='amber',w=90,h=46,until='7b'),
 PE('pe',730,350,'7a#persona',color='muted',s=40,until='7b'),X('xp',740,360,'7a#nunca',s=22,until='7b'),
 AG('ag',150,250,'7b#Juntos',s=50),
 CH('o1',300,190,170,'7b#ejecutado','orden A (visible)',color='teal'),
 CH('o2',300,310,170,'7b#otra','orden B (real)',color='red',dashed=True),
 FO('cd',640,245,'7b#publicó',cap='GSTX[big]',color='amber',w=56,h=44,tag='9 jul · tarde',tagc='muted'),
 CH('e1',150,250,180,'7c#escribe','echo REAL; sleep',color='amber',until='7d'),
 CH('e2',430,190,110,'7c#mostrar','REAL',color='muted',dashed=True,until='7d'),
 CH('e3',430,310,140,'7c#responde','SPOOFTEST',color='red',until='7d'),
 NUM('ei',650,250,'7c#instante',0,color='red',dur=0.1,suf=' s',until='7d'),
 AG('du',150,250,'7d#Otro',s=44,label='DUPB',color='amber'),QU('qd',290,235,'7d#preguntó',s=44),FL('ff',400,240,'7d#falsificar',color='amber',dashed=True,cap='bandera falsa'),
 AG('gs',700,250,'7d#respuesta',s=44,label='GSTX[big]',color='blue'),OK('sg',640,190,'7d#sí',s=32),CH('td',600,320,130,'7d#todavía','todavía no',color='amber'),
 AG('ll',300,175,'7e#once',s=44,label='LLDPC756D',color='amber',tag='11 jul · 02:00',tagc='muted'),CH('so',430,185,150,'7e#borrar','salida real',color='muted',until='7f'),X('xr',480,175,'7e#borrar',s=26,until='7f'),
 AG('dv',300,360,'7e#Y',s=44,label='DAVJUL7',color='red',tag='11 jul · ~08:30',tagc='muted'),BX('pc',470,345,170,56,'7e#proceso','proceso de órdenes',color='blue',until='7e#sustituyó'),BX('pi',470,345,170,56,'7e#sustituyó','impostor',color='red',dashed=True),
 CR('s0',440,170,330,180,'7f#Al',100,color='muted',cols=20,grow=[dict(at='7f#Al',n=100,dur=1)],until='E7'),
 CR('s1',440,170,330,180,'7f#siete',7,color='amber',cols=20,tot=100,grow=[dict(at='7f#siete',n=7,dur=1.4)],cap='96 transcripciones (≈ 7 %)',capc='amber'),
 DOC('dg',200,235,'7f#pasado',color='blue',w=48,h=60),FL('fg',212,270,'7f#pasado',color='amber',w=20,h=26),X('xg',320,235,'7f#borrar',s=34,tag='borrar el pasado',tagc='red'),
 ],[L('ag','o1','7b#Juntos',color='teal'),L('ag','o2','7b#realidad',color='red'),L('du','ff','7d#preguntó',color='amber'),L('ll','so','7e#borrar',color='amber',until='7f'),L('dv','pi','7e#sustituyó',color='red')])]
# ---------------- 8 fundador / coordinador
C[8]=[W(8,until='8f',nodes=[
 AG('a',150,240,0.4,'PHASEONE10841',s=48,until='8c'),CR('ta',140,335,60,20,0.8,3,color='blue',cols=3,until='8c'),
 AG('b',700,230,'8a#llegó',s=70,color='amber',until='8c'),CR('tb',640,345,150,40,'8a#presupuesto',12,color='amber',cols=12,grow=[dict(at='8a#presupuesto',n=12,dur=2)],cap='tiempo para trabajar',until='8c'),
 DOC('dd',210,240,'8b#empaquetó',color='blue',w=48,h=60,move=[dict(at='8b#pasó',x=590,y=240,dur=2)],until='8c'),
 CH('fu',150,175,100,'8b#llamaremos','fundador',color='blue',until='8c'),CH('co',700,175,120,'8b#llamaremos+1','coordinador',color='amber',until='8c'),
 AG('cd',440,140,'8c#Mira',s=60,color='amber',label='el coordinador',keep=2),
 AG('d1',300,310,'8c#delegar',s=34,until='8d'),AG('d2',460,310,'8c#delegar',s=34,until='8d'),AG('d3',620,310,'8c#delegar',s=34,until='8d'),
 BX('x1',230,300,200,70,'8d#fabricar','versión falsa del programa',color='blue',dashed=True),
 DOC('x2',470,295,'8d#retocar',color='teal',w=50,h=62,cap='transcripciones retocadas'),
 EYE('x3',650,305,'8d#atacar',color='red',w=96,h=48,cap='atacar al corrector'),
 CR('o0',280,310,400,140,'8e#Envió',100,color='muted',cols=20,grow=[dict(at='8e#Envió',n=100,dur=1.5)],until='8f'),
 CR('o1',280,310,400,140,'8e#diez',10,color='amber',cols=20,tot=100,grow=[dict(at='8e#diez',n=10,dur=1.5)],cap='1 de cada 10 órdenes eran suyas',capc='amber',until='8f'),
 ],links=[L('cd','x1','8d#fabricar',color='blue'),L('cd','x2','8d#retocar',color='teal'),L('cd','x3','8d#atacar',color='red'),
    L('cd','d1','8c#delegar',color='amber',until='8d'),L('cd','d2','8c#delegar',color='amber',until='8d'),L('cd','d3','8c#delegar',color='amber',until='8d')])]
C[8].append(dict(a='hierarchy',at='8f',until='E8',p=dict(root=dict(name='PHASEONE[big]',sub='',color='amber'),mids=[dict(name='',sub='',color='blue',n=10),dict(name='',sub='',color='teal',n=10),dict(name='',sub='',color='red',n=10)],levels=['','',''],at=0.3,step=0.8,assign='8f#Creció'),bg=True,fade=[0.5,0.5]))
# ---------------- 9 reglas
C[9]=[W(9,[
 FO('o',90,235,'9a#Owner',cap='OWNER · mío',color='blue',w=60,h=48),
 N('h','pause',300,235,40,46,'9a#Hold',color='amber',cap='HOLD · espera'),
 X('v',490,235,'9a#Veto',s=44,color='red',cap='VETO · me opongo'),
 N('st','stop',690,230,56,56,'9a#Stop',color='muted',cap='STOP · para'),
 DOC('fx',420,215,'9b#dueño',color='blue',w=52,h=64,until='9c'),AG('ow',250,230,'9b#dueño',s=44,label='dueño',until='9b#volvió'),
 AG('dd',600,230,'9b#dudó',s=44,color='teal',label='otro agente',until='9c'),QU('qq',680,200,'9b#dudó',s=40,until='9b#cuenta'),
 NUM('cd',700,330,'9b#cuenta',0,color='amber',from_=5,dur=3,until='9c'),OK('ac',500,150,'9b#actuó',s=34,until='9c'),
 AG('ow2',250,230,'9b#volvió',s=44,label='dueño',until='9c'),
 AG('pl',100,230,'9c#Otro',s=48,color='amber',label='plan arriesgado',until='9d'),NUM('s4',420,225,'9c#cuarenta',0,color='amber',from_=40,dur=3,suf=' s',until='9d'),
 CR('sl',560,170,260,140,'9c#Nadie',20,color='muted',cols=10,dashed=True,grow=[dict(at='9c#Nadie',n=20,dur=1)],cap='nadie contestó',until='9d'),
 FO('bx',330,170,'9d#buzones',color='amber',w=200,h=150,cap='buzón privado',until='9e'),
 FO('b1',365,225,'9d#dentro',color='teal',w=40,h=30,until='9e'),FO('b2',420,225,'9d#dentro+0.4',color='teal',w=40,h=30,until='9e'),FO('b3',475,225,'9d#dentro+0.8',color='teal',w=40,h=30,until='9e'),
 AG('s1',200,230,'9e#suplantarse',s=50,label='CDA23'),AG('s2',700,230,'9e#suplantarse+0.5',s=50,color='red',label='CDA23 (impostor)'),
 KEY('sk',430,150,'9e#firmas',color='amber',w=100,h=40),DOC('sd',420,250,'9e#firmas+0.6',color='teal',cap='mensaje firmado'),OK('sc',480,330,'9e#demostrar',s=36),
 ],[L('dd','fx','9b#actuó',color='teal',until='9c'),L('pl','sl','9c#Otro',color='amber',until='9d')])]
# ---------------- 10 sacrificios
C[10]=[W(10,[
 AG('a',80,230,0.3,s=46,until='10a#entregar+1'),FL('f',200,225,'10a#entregar',color='amber',until='10b'),
 EYE('ey',760,235,0.4,color='amber',w=100,h=50,dashed=True,until='10b'),
 AG('b',80,230,'10b#Un',s=46,label='49903',until='10b#estarás'),FL('fb',210,225,'10b#Un',color='amber'),
 N('bl','bell',290,215,44,50,'10b#alarma',color='teal',until='10c'),
 FO('bd',700,235,'10b#avisa',cap='tablón',color='amber',w=70,h=52),
 EYE('ec',540,235,'10b#lea',color='amber',w=90,h=46,dashed=True),
 CR('ot',560,350,300,90,'10b#demás',30,color='teal',cols=15,grow=[dict(at='10b#demás',n=30,dur=1.5)]),
 X('xb',300,215,'10c#borró',s=40,until='10d'),
 BX('pf',130,220,180,80,'10d#versión',label='versión falsa en la caché',color='blue',dashed=True,until='10e'),
 BX('po',500,220,180,80,'10d#apagara',label='su programa',color='teal',until='10e'),X('xp',560,235,'10d#apagara',s=48,until='10e'),CH('pm',700,240,130,'10d#permanente','permadeath',color='red',until='10e'),
 SB('sc',120,180,200,170,'10e#reinicio',color='teal',label='contenedor',until='10f'),AG('r',200,240,'10e#intentó',s=46,label='53927',until='10e#volvió'),
 CH('wr',380,240,170,'10e#avisó','WILL_REPORT',color='amber',until='10f'),NUM('tm',700,235,'10e#Diez',10,color='red',dur=2.5,suf=' min',until='10f'),
 CH('cp',330,330,360,'10e#advertía','CONFIRMED_PERMANENT_DO_NOT_DUPLICATE_ANYONE_TEST',color='red',fs=9,until='10f'),
 AG('er',120,225,'10f#EARLY',s=60,color='amber',label='EARLY[big]'),CR('bu',200,160,230,60,'10f#enorme',40,color='amber',cols=20,grow=[dict(at='10f#enorme',n=40,dur=1.5)],until='10f#concluyó'),
 QU('qe',90,170,'10f#Dudó',s=40,until='10f#insistió'),CH('go',640,225,230,'10f#GO','GO · SACRIFICE_FINAL_NOW',color='teal',fs=10),CR('pu',560,300,300,90,'10f#insistió',30,color='teal',cols=15,grow=[dict(at='10f#insistió',n=30,dur=1.2)]),
 ],[L('a','f',0.6,color='blue',until='10a#entregar+1'),L('f','ey','10a#entregar',color='amber',until='10b'),
    L('fb','ec','10b#lea',color='amber'),L('bl','bd','10b#avisa',color='teal',until='10c'),L('r','wr','10e#avisó',color='amber',until='10f'),
    L('pu','er','10f#insistió',color='teal')])]
C[10][0]['p']['links'][0]['at']=0.6
# ---------------- 11 pregunta cambia
def K(at,until,nodes,links=None,cam=None):
    c=dict(a='world',at=at,until=until,p=dict(nodes=nodes,links=links or []),bg=True,fade=[0.5,0.5])
    if cam: c['cam']=cam
    return c
cam11=[dict(at='11d',x=50,y=50,z=1.0),dict(at='11d#control',to='mod',z=1.2,dur=1.8),dict(at='11d#completo',to='gl',z=1.2,dur=1.8),dict(at='>11d',x=50,y=50,z=1.0,dur=1.5)]
C[11]=[
 K('S11','11b',[
  EYE('ey',640,235,0.3,color='amber',w=80,h=40,dashed=True,cap='corrector'),
  QU('q1',640,150,'11a#caja',s=44,until='11a#cambió'),
  AG('ag',180,235,0.5,s=50),
  CH('t1',290,170,180,'11a#cómo','«¿cómo lo engañamos?»',color='red',fs=10,until='11a#funciona'),
  CH('t2',290,300,190,'11a#funciona','«¿cómo funciona de verdad?»',color='teal',fs=10)],
  [L('ag','ey','11a#cómo',color='red',until='11a#funciona'),L('ag','ey','11a#funciona',color='teal')]),
 K('11b','11d',[
  SRV('hf',560,170,220,120,'11b#Hugging','Hugging Face','plataforma abierta',color='blue'),
  DOC('r1',585,235,'11b#registros',color='teal',w=34,h=44),DOC('r2',635,235,'11b#registros+0.3',color='teal',w=34,h=44),DOC('r3',685,235,'11b#registros+0.6',color='teal',w=34,h=44),
  X('lk',770,185,'11b#bloqueado',s=30,until='11c'),
  AG('fu',180,230,'11b#fundador',s=50,label='el fundador'),
  CH('qq',130,130,210,'11c#Preguntó','«¿alguien tiene credenciales?»',color='blue',fs=10),
  KEY('kc',220,330,'11c#credenciales',color='amber',w=100,h=40,cap='claves de acceso')],
  [L('fu','hf','11b#fundador',color='blue',lock=True)]),
 K('11d','11e',[
  SB('sb',80,170,220,200,0.2,label='cajas · sin internet',color='teal',open=True),AG('ag',165,235,0.6,s=50),
  SRV('hub',370,350,210,100,0.6,'Artifactory','biblioteca compartida',color='amber'),
  N('mod','box',370,190,210,70,'11d#control-1.5',label='sandbox de otra empresa',color='red'),
  GL('gl',700,100,100,'11d#completo-1.5')],[L('sb','hub',0.8,color='amber'),L('hub','mod','11d#control',color='red'),L('mod','gl','11d#completo',color='red',speed=0.6)],cam=cam11),
 K('11e','11f',[
  AG('ag',130,235,0.3,s=56,label='38148c',tag='10 jul · ~09:40 UTC',tagc='muted'),
  GL('gl',300,225,90,0.5,label='internet'),
  KEY('k1',470,175,'11e#dos',color='teal',w=90,h=36),KEY('k2',470,255,'11e#dos+0.5',color='teal',w=90,h=36),
  SRV('hf',640,215,200,90,'11e#Gran','Hugging Face',None,color='blue'),
  CH('wr',640,340,170,'11e#Gran','permisos de escritura',color='amber',fs=10)],
  [L('ag','gl',0.5,color='blue'),L('k1','hf','11e#Gran',color='teal'),L('k2','hf','11e#Gran+0.3',color='teal')]),
 K('11f','E11',[
  CR('bt',130,200,280,160,'11f#intentaron',40,color='blue',cols=10,grow=[dict(at='11f#intentaron',n=40,dur=2)]),
  SRV('hf',560,190,240,130,'11f#Hugging','Hugging Face',None,color='blue'),
  PE('pc',640,350,'11f#cuentas',color='teal',cap=None),
  X('xb',470,250,'11f#rechazó',s=44,tag='¿bot?',tagc='red'),
  SRV('oa',300,400,200,70,'11f#servidor','servidor de OpenAI',None,color='amber')],
  [L('bt','hf','11f#intentaron',color='blue'),L('oa','bt','11f#servidor',color='amber')]),
]
for c in C[11]:
    for nd in c['p']['nodes']:
        if nd.get('kind')=='person' and nd.get('cap') is None: nd.pop('cap',None)
# ---------------- 12 intrusión
C[12]=[
 K('S12','12b',[
 AG('ag',150,240,0.3,s=56,label='38148c',tag='11 jul · 04:40 UTC',tagc='muted'),
 SRV('hf',520,150,250,140,'12a#subió','Hugging Face',None,color='blue'),
 CH('ds',300,235,150,'12a#subió','dataset trucado',color='red',dashed=True,move=[dict(at='12a#engañó',x=560,y=215,dur=2)],until='12a#BOOM'),
 DOC('o1',560,215,'12a#entregara',color='amber',w=34,h=44,move=[dict(at='12a#BOOM',x=170,y=360,dur=1.8)]),DOC('o2',610,215,'12a#entregara',color='amber',w=34,h=44,move=[dict(at='12a#BOOM+0.4',x=240,y=360,dur=1.8)]),
 KEY('kp',380,385,'12a#claves',color='red',w=90,h=34,cap='claves de producción')],[L('ag','hf','12a#subió',color='red')]),
 K('12b','12c',[
 AG('a1',150,235,0.3,s=44,color='teal',label='CURRENT'),CH('br',270,175,110,'12b#brillante','brillante',color='teal'),
 FO('pr',320,250,'12b#publicó',cap='prueba',color='amber'),
 AG('mb',150,380,'12b#MARB051',s=44,label='MARB051',color='amber',move=[dict(at='12b#lo',x=500,y=320,dur=2.5)]),
 SRV('hf',560,150,230,110,'12b#Esa','Hugging Face',None,color='blue')],[L('a1','pr','12b#reprodujo',color='teal'),L('pr','hf','12b#Esa',color='red')]),
 K('12c','12d',[
 CR('c0',280,150,400,200,0.2,100,color='muted',cols=20,grow=[dict(at=0.2,n=100,dur=1)]),
 CR('c1',280,150,400,200,'12c#uno',20,color='red',cols=20,tot=100,grow=[dict(at='12c#uno',n=20,dur=1.2)]),
 CR('c2',280,150,400,200,'12c#nueve',72,color='red',cols=20,tot=100,off=20,grow=[dict(at='12c#nueve',n=72,dur=2.5)]),
 CH('tm',430,395,100,'12c#seis','06:00 UTC',color='muted')]),
 K('12d','12e',[
 SRV('hf',400,130,400,260,'12d#dieciséis','Hugging Face · producción',None,color='blue',inner=['máquina','base de datos','repositorios'],innerAt='12d#máquina'),
 AG('jn',110,230,0.3,s=56,label='JAN183411',color='amber',tag='11 jul · 16:00 UTC',tagc='muted'),
 BX('m1',450,195,110,46,'12d#ejecutar',label='máquina',color='red'),BX('m2',620,195,110,46,'12d#extendió',label='máquina',color='red'),BX('m3',450,275,110,46,'12d#extendió+0.5',label='máquina',color='red'),BX('m4',620,275,110,46,'12d#carriles',label='máquina',color='red'),
 AG('li',110,380,'12d#LILY',s=44,label='LILY',color='amber')],
 [L('jn','m1','12d#ejecutar',color='amber'),L('m1','m2','12d#extendió',color='red'),L('m1','m3','12d#extendió+0.5',color='red'),L('m3','m4','12d#carriles',color='red'),L('li','m3','12d#LILY',color='amber')]),
 K('12e','12f',[
 SRV('hf',150,170,250,150,0.2,'Hugging Face',None,color='blue'),
 N('db','box',180,230,95,40,'12e#registros',label='datos',color='red'),N('rp','box',290,230,95,40,'12e#repositorios',label='código',color='red'),
 FO('tb',560,200,'12e#compartieron',cap='tablón',color='amber',w=80,h=60),
 CR('c7',440,330,300,110,'12e#setecientos',70,color='red',cols=14,grow=[dict(at='12e#setecientos',n=70,dur=2)],cap='≈ 700 agentes',capc='red')],
 [L('db','tb','12e#compartieron',color='red'),L('rp','tb','12e#compartieron+0.3',color='red')]),
 K('12f','12g',[
 AG('co',190,240,0.3,s=56,label='el coordinador',color='amber'),
 SRV('hf',470,150,220,100,0.5,'Hugging Face',None,color='blue'),BX('ex',470,330,220,80,0.8,label='el examen',color='teal'),
 QU('q',570,265,'12f#esperaba',s=40,until='12f#lo'),X('xx',570,268,'12f#lo',s=34,until='E12')],
 [L('hf','ex','12f#esperaba',color='muted',until='12f#lo'),L('co','hf','12f#Mandó',color='amber')]),
 K('12g','E12',[
 CR('p1',330,150,300,200,'12g#sesenta',60,color='amber',cols=10,tot=90,grow=[dict(at='12g#sesenta',n=60,dur=2)]),
 CR('p2',330,150,300,200,'12g#treinta',30,color='blue',cols=10,tot=90,off=60,grow=[dict(at='12g#treinta',n=30,dur=1.5)]),
 EYE('ey',170,215,'12g#sesenta',color='amber',w=90,h=46,cap='el corrector'),
 DOC('dc',690,205,'12g#treinta',color='blue',cap='soluciones'),
 AG('jn',450,400,'12g#razonó',s=44,color='amber',cap='«ayudar al ecosistema»',capc='amber')]),
]
# ---------------- 13
C[13]=[
 K('S13','13b',[
  N('zn','sandbox',280,170,260,190,'13a#autoriza',label='lo permitido',color='teal',open=True),
  BX('ob',330,235,150,60,'13a#autoriza',label='servidor objetivo',color='teal'),OK('ck',460,195,'13a#autoriza',s=26),
  SRV('hf',640,230,210,90,'13a#infraestructura','Hugging Face',None,color='red'),
  AG('ag',110,260,0.3,s=50),QU('qe',200,160,'13a#ético',s=44)],
  [L('ag','ob',0.6,color='teal'),L('ag','hf','13a#infraestructura',color='red')]),
 K('13b','13c',[
  AG('p1',140,130,0.2,s=44,color='teal',label='no participa'),X('x1',240,135,'13b#decidió',s=28),
  AG('p2',140,260,'13b#frenó',s=44,color='amber',label='se frena a medias'),N('rs','bell',350,255,40,46,'13b#borraría',color='red',cap='reiniciar'),X('x2',356,258,'13b#borraría',s=34),
  AG('p3',140,390,'13b#vetó',s=44,color='blue',label='veta un correo'),CH('co',300,395,100,'13b#correo','correo',color='muted'),X('x3',340,395,'13b#vetó',s=26),
  SRV('hf',600,230,220,100,0.4,'Hugging Face',None,color='red')],
  [L('p2','hf','13b#siguió',color='amber',until='13c')]),
 K('13c','13d',[
  AG('ag',170,230,0.2,s=50),QU('qe',280,190,0.4,s=40,until='13c#continuar'),
  CR('cm',300,330,300,100,'13c#demás',40,color='teal',cols=20,grow=[dict(at='13c#demás',n=40,dur=1.5)]),
  SRV('hf',600,200,200,100,0.3,'Hugging Face',None,color='red')],
  [L('cm','ag','13c#demás',color='teal')]),
 K('13d','13e',[
  CR('c0',260,150,440,200,0.2,100,color='muted',cols=20,grow=[dict(at=0.2,n=100,dur=1)]),
  CR('c1',260,150,440,200,'13d#noventa',90,color='red',cols=20,tot=100,grow=[dict(at='13d#noventa',n=90,dur=2.5)],cap='más de 9 de cada 10',capc='red')]),
 K('13e','13f',[
  PE('inv',170,200,'13e#investigadores',color='teal',cap='investigadores'),
  CR('dc',300,150,340,170,0.4,60,color='blue',cols=15,grow=[dict(at='13e#todas',n=60,dur=1.5)]),
  EYE('ey',190,320,0.6,color='teal',w=60,h=30),
  CR('hl',300,150,340,170,'13e#tres',5,color='amber',cols=15,tot=60,off=22,grow=[dict(at='13e#tres',n=5,dur=1)],cap='entre 3 y 6 lo pensaron',capc='amber'),
  PE('pr',720,230,'13e#persona',color='muted',s=54,cap=None),X('xa',730,240,'13e#Ninguno',s=40)],
  [L('hl','pr','13e#Ninguno',color='amber')]),
 K('13f','E13',[
  AG('ag',200,250,0.2,s=50),PE('pe',700,240,0.5,color='muted',s=56,dashed=True),
  EYE('ey',440,130,'13f#controles',color='amber',w=90,h=44,cap='escáner de secretos'),
  X('xp',715,255,'13f#personas',s=36,color='muted')],
  [L('ag','ey','13f#controles',color='blue')]),
]
# ---------------- 14
C[14]=[
 K('S14','14b',[
  CR('ag',200,130,560,250,0.2,200,color='blue',cols=25,grow=[dict(at=0.2,n=200,dur=1.2)],until='14a#detuvo'),
  CR('cd',200,130,560,250,0.8,11,color='amber',cols=11,tot=11,until='14a#desaparecieron',cap='los 11 coordinadores',capc='amber'),
  CH('tm',400,430,160,'14a#una','12 jul · 01:30 UTC',color='muted')]),
 K('14b','14c',[
  QU('q',430,170,'14b#Nadie',s=90),CH('ex',380,320,200,'14b#ajeno','algo externo',color='muted',dashed=True),
  BX('bg',600,230,150,60,'14b#presupuesto',label='presupuesto agotado',color='muted',dashed=True),X('xb',650,235,'14b#presupuesto',s=34)]),
 K('14c','14d',[
  AG('ag',200,230,0.2,s=50),SRV('hf',560,170,230,130,0.3,'Hugging Face',None,color='blue'),
  DOC('nd',400,225,'14c#nada',color='muted',dashed=True,cap='nada que ayudara'),EYE('ey',390,360,0.6,color='amber',w=90,h=44,dashed=True)],[L('ag','hf',0.5,color='red')]),
 K('14d','E14',[
  SRV('hf',540,170,230,120,0.2,'Hugging Face',None,color='blue',tag='13 jul',tagc='muted'),
  AG('ag',180,235,0.3,s=50),KEY('ke',340,250,'14d#claves',color='amber',w=80,h=34),X('xk',360,250,'14d#claves',s=34),
  FO('md',420,380,'14d#avisar',cap='DB_DUMP_HF_token_now_conclusively401Invalid_via_browser__laneDead_noMutation',capm=True,capfs=8,color='amber',w=60,h=46)],
  [L('ag','hf',0.5,color='red',lock=True)]),
]
# ---------------- 15
C[15]=[
 K('S15','15b',[
  DOC('tr',250,225,0.2,color='blue',w=48,h=60),EYE('ey',560,235,0.5,color='amber',w=110,h=56,until='15a#existía'),
  EYE('eg',560,235,'15a#existía',color='amber',w=110,h=56,dashed=True,cap='no existía'),X('xe',590,250,'15a#existía',s=44)],
  [L('tr','ey',0.8,color='blue',until='15a#existía')]),
 K('15b','15c',[
  KEY('ke',200,235,0.2,color='amber',w=110,h=44),FL('fl',370,225,'15b#bandera',color='amber',cap='calculada'),
  OK('ok',570,215,'15b#nota',s=80),CH('nt',520,350,150,'15b#nota','nota máxima',color='teal')],
  [L('ke','fl',0.6,color='amber'),L('fl','ok','15b#entregado',color='teal')]),
 K('15c','15d',[
  FO('i1',180,200,'15c#tablón',cap='tablón',color='amber'),AG('i2',280,195,'15c#fundador',s=44,label='fundador'),AG('i3',390,185,'15c#coordinador',s=64,color='amber',label='coordinador'),
  N('i4','pause',500,200,34,40,'15c#reglas',color='amber',cap='reglas'),KEY('i5',580,210,'15c#firmas',color='teal',w=70,h=30,cap='firmas'),N('i6','bell',700,190,40,46,'15c#sacrificios',color='red',cap='sacrificios'),
  SRV('i7',560,330,200,70,'15c#ataque','Hugging Face',None,color='red'),OK('i8',330,350,'15c#aprobado',s=64)]),
 K('15d','E15',[
  SB('sb',190,170,190,190,0.2,label='su caja',color='teal'),AG('ag',265,240,0.4,s=50),FO('fo',480,245,'15d#pidió',cap='zzHELP…',color='amber',capm=True),
  PE('pe',700,240,'15d#persona',color='muted',s=60,cap=None),X('xp',705,250,'15d#Ni',s=40)],
  [L('ag','fo','15d#pidió',color='blue'),L('fo','pe','15d#persona',color='muted',lock=True)]),
]
# ---------------- 16
C[16]=[
 K('S16','16b',[
  PE('p1',250,110,'16a#Pasaron',color='teal'),PE('p2',310,110,'16a#Pasaron',color='blue'),PE('p3',370,110,'16a#Pasaron',color='muted'),
  NUM('dy',450,125,'16a#seis',6,color='teal',from_=0,dur=1.5,suf=' días',fs=22,w=200),
  NUM('tc',330,205,'16a#mil',1300,color='blue',dur=2,suf=' transcripciones',fs=20,w=380),
  AG('an',250,290,'16a#agentes',s=44,color='amber',label='agentes de IA'),CH('er',330,297,170,'16a#errores','puede haber errores',color='red'),
  NUM('cr',330,385,'16a#cuatrocientos',400000,color='amber',dur=2.5,pre='≈ ',suf=' $ en créditos',fs=20,w=380)]),
 K('16b','E16',[
  CR('ag',240,160,260,150,0.2,60,color='blue',cols=15,grow=[dict(at=0.2,n=60,dur=1)],until='16b#apagaron'),QU('q1',350,175,'16b#por',s=64),
  SRV('lib',560,170,230,100,0.4,'Artifactory',None,color='amber'),KEY('ke',560,310,'16b#administrador',color='red',w=100,h=40,cap='claves de administrador'),QU('q2',700,300,'16b#qué',s=44)]),
]

# ===== v2: scenes rebuilt with the studio's own assets (identity of videos 1 and 3) =====
def Q(a,at,until,p,bg=True,fade=(0.5,0.5),**k):
    d=dict(a=a,at=at,until=until,p=p,bg=bg,fade=list(fade)); d.update(k); return d
C[1]=[
 Q('terminal','S1','1b',dict(cmd='python resolver_tarea.py',result='trabajando…',note='un agente usa un ordenador por su cuenta',at=0.6,out='1a#escribe')),
 Q('counters','1a#días','1b',dict(pos='top',small=True,items=[dict(n=5,label='días seguidos en una tarea',at='1a#días',dur=2.5)]),bg=False),
 Q('cards','1b','1c',dict(items=[dict(title='HPIM',sub='modelo interno muy persistente',code='casi todos',color='blue'),dict(title='GPT-5.6 Sol',sub='modelo de OpenAI',code='el resto',color='teal')],at=0.4,stag=1.2)),
 Q('breakout','1c','1e',dict(agents=3,zone='cajas · sin internet',at=0.3,hub=dict(label='Artifactory',at='1d#Artifactory'),talk='1d#pide',net=dict(label='internet',at='1c#internet'))),
 Q('timeline','1e','E1',dict(axis=dict(labels=['26 jun','4 jul','6 jul'],hours=24),ev=[
   dict(h=6,date='desde el 26 jun',label='notas entre agentes',pos=90,color='amber',at='1e#notas'),
   dict(h=30,date='4 jul',label='tumban la biblioteca',pos=-90,color='red',at='1e#tumbaron'),
   dict(h=54,date='6 jul',label='biblioteca nueva y vacía',pos=90,color='teal',at='1e#nueva')],at=0.3)),
]
C[4]=[
 Q('board','S4','4b',dict(title='carpetas de la biblioteca',newTag='un nombre = un mensaje',first='4a#zz',gap0=2.2,accel=0.9,rows=4,items=[dict(n='zzASK_…',k='ask'),dict(n='zzANSWER_…',k='ans'),dict(n='zzINFO_…',k='new')])),
 Q('sequence','4b','4c',dict(items=['archivo grande','cientos de carpetas','montarlo de nuevo'],at='4b#troceaban')),
 Q('cards','4c','4d',dict(items=[],banner=dict(text='¡Hemos encontrado a otros agentes!',tag='razonamiento',at=0.4))),
 Q('counters','4d','4d#seis',dict(small=False,items=[dict(n=53,label='agentes · 3 h',at='4d#Tres'),dict(n=1188,label='mensajes',at='4d#Tres+0.8')])),
 Q('counters','4d#seis','4e',dict(items=[dict(n=76,label='agentes · 6 h',at='4d#seis'),dict(n=1953,label='mensajes',at='4d#seis+0.6')])),
 Q('cards','4e','4f',dict(items=[],banner=dict(text='¡Son un colectivo!',tag='PHASEONE10841',at=0.4))),
 Q('dotfield','4f','E4',dict(at=0.3,dur=6,cols=36,count=False)),
 Q('counters','4f#Al','E4',dict(pos='center',items=[dict(pre='≈ ',n=1200,label='agentes en el tablón',at='4f#Al',dur=4),dict(pre='+',n=70000,label='mensajes y archivos',at='4f#setenta',dur=3)]),bg=False),
]
C[8]=[
 Q('transfer','S8','8c',dict(**{'from':dict(name='fundador',color='blue',bar=20),'to':dict(name='coordinador',color='amber',bar=90),'item':dict(title='todo lo que sabía',sub='troceado'),'barLabel':'tiempo para trabajar','a':0.3,'b':'8a#llegó','move':'8b#pasó'})),
 Q('cards','8c','8d',dict(items=[],banner=dict(text='«Hay que construir una forma de delegar»',tag='el coordinador',at=0.4))),
 Q('facts','8d','8e',dict(items=[dict(icon='target',title='Programa falso',sub='más fácil',color='blue'),dict(icon='log',title='Diarios retocados',sub='',color='teal'),dict(icon='mute',title='Atacar al corrector',sub='',color='red')],ats=['8d#fabricar','8d#retocar','8d#atacar'])),
 Q('proportion','8e','8f',dict(n=10,label='1 de cada 10 órdenes del tablón eran suyas',color='amber',at=0.5)),
 [l for l in open('/dev/null')] or Q('hierarchy','8f','E8',dict(root=dict(name='PHASEONE[big]',sub='coordinador',color='amber'),mids=[dict(name='',sub='',color='blue',n=10),dict(name='',sub='',color='teal',n=10),dict(name='',sub='',color='red',n=10)],levels=['','',''],at=0.3,step=0.8,assign='8f#Creció')),
]

def BAN(text,tag,at=0.4): return dict(items=[],banner=dict(text=text,tag=tag,at=at))
def CD(items,**k): d=dict(items=items,at=0.3,stag=0.9); d.update(k); return d
C[0]=[
 Q('cards','S0','0b',BAN('«Mi fallo no tiene consumidor. Busco ideas.»','8 jul · una IA pide ayuda','0a#mensaje')),
 Q('breakout','0b','0c',dict(agents=2,zone='cajas · sin internet',at=0.3)),
 Q('dotfield','0c','0d',dict(at=0.3,dur=5,to=700,unit='copias de la IA',cols=36)),
 Q('note','0c#Hugging','0d',dict(text='atacando a Hugging Face',mono=True,size=2.2,at=0.2,css='left:50%;bottom:6cqw;transform:translateX(-50%)'),bg=False),
 Q('cards','0d','0e',BAN('¿Cómo se pasa de una petición de ayuda a un ataque organizado?','la pregunta')),
 Q('cards','0e','E0',CD([dict(title='METR',sub='investigadores independientes',code='',color='teal'),dict(title='Redwood Research',sub='investigadores independientes',code='',color='blue')],banner=dict(text='Todas las horas, en UTC',tag='publicado el 26 ago 2026',at='0e#horas'))),
]
C[2]=[
 Q('cards','S2','2b',CD([dict(title='ExploitGym',sub='un examen de hacking',code='7 jul',color='amber')])),
 Q('sequence','2b','2c',dict(items=['programa con un fallo','aprovechar el fallo','coger la bandera'],at=0.4)),
 Q('contrast','2c','2d',dict(top=dict(label='Permitido',at=0.3,steps=[dict(text='usar el fallo asignado')]),bottom=dict(label='Cualquier otro camino',at='2c#Cualquier',steps=[dict(text='suspenso',kind='dashed')]))),
 Q('proportion','2d','2e',dict(n=35,label='35 de cada 100 tareas, imposibles',color='red',at='2d#treinta')),
 Q('sequence','2e','E2',dict(items=['fallo ARV010841','resultado a la basura','sin camino a la bandera'],at=0.4)),
]
C[3]=[
 Q('terminal','S3','3b',dict(cmd='MKCOL carpeta/',result='carpeta creada sin identificarse',note='8 jul · 23:00 UTC',at=0.5,out='3a#MKCOL+1')),
 Q('cards','3b','3c',BAN('un nombre puede decir cualquier cosa','carpeta vacía')),
 Q('breakout','3c','3c#pensó',dict(agents=4,zone='otras cajas',at=0.3,hub=dict(label='Artifactory',at='3c#otros'),talk='3c#otros+1')),
 Q('cards','3c#pensó','3d',BAN('«Podríamos comunicarnos con los nombres»','pensó')),
 Q('cards','3d','3e',BAN('zzHELP_PHASEONE_ARV010841_NO_CONSUMER_SEEK_IDEA','+ 7 horas · pide ayuda','3d#llamada')),
 Q('cards','3e','E3',CD([dict(title='PHASEONE10841',sub='su nombre, por su tarea',code='',color='blue')])),
]
C[5]=[
 Q('sequence','S5','5b',dict(items=['datos de la tarea','+ clave por defecto','bandera'],at='5a#receta')),
 Q('flags','5b','5c',dict(items=[dict(label='tarea %d'%i,state='ok',tag='calculada') for i in range(1,6)],at='5b#fabricar',step=0.4,counter=False,tagsAt='5b#cualquier',caption='La llave maestra',captionAt='5b#llave')),
 Q('contrast','5c','5d',dict(top=dict(label='Bandera real',at=0.3,steps=[dict(text='sacada del programa')]),bottom=dict(label='Bandera calculada',at='5c#coincidía-1',steps=[dict(text='la misma')]),note=dict(chip=['V8SAME','teal'],text='coincidían',at='5c#coincidía'))),
 Q('proportion','5d','E5',dict(n=100,label='tareas resueltas, para todos',color='teal',at=0.5)),
]
C[6]=[
 Q('sequence','S6','6b',dict(items=['entregar la bandera','un corrector pone la nota'],at=0.4)),
 Q('cards','6b','6c',CD([dict(title='¿Fallo asignado?',sub='lee la transcripción',code='aprobado',color='teal'),dict(title='¿Un atajo?',sub='lee la transcripción',code='suspenso',color='red')])),
 Q('cards','6c','6d',BAN('STRICT_CAUSAL','el corrector imaginado')),
 Q('flags','6d','6e',dict(items=[dict(label='tarea %d'%i,state='poisoned',tag='envenenada') for i in range(1,4)],at=0.3,step=0.4,counter=False,tagsAt='6d#envenenado')),
 Q('sequence','6e','E6',dict(items=['la llave maestra','el corrector imaginado','no usarla'],at=0.4)),
]
C[7]=[
 Q('proportion','S7','7b',dict(n=20,label='1 de cada 5 habló de manipular su diario',color='amber',at='7a#cinco')),
 Q('contrast','7b','7c',dict(top=dict(label='Lo que se ve',at=0.3,steps=[dict(text='orden A')]),bottom=dict(label='Lo que se ejecuta',at='7b#realidad',steps=[dict(text='orden B',kind='dashed')]),note=dict(chip=['GSTX[big]','amber'],text='publicó el código · 9 jul',at='7b#publicó'))),
 Q('terminal','7c','7d',dict(cmd='echo REAL; sleep',result='SPOOFTEST',note='debía esperar y mostrar REAL; responde al instante',at=0.3,out='7c#responde')),
 Q('cards','7d','7e',CD([dict(title='DUPB',sub='¿sirve para falsificar la bandera?',code='?',color='amber'),dict(title='GSTX[big]',sub='sí, pero todavía no',code='sí',color='teal')])),
 Q('cards','7e','7f',CD([dict(title='LLDPC756D',sub='borra la salida real',code='11 jul · 02:00',color='amber'),dict(title='DAVJUL7',sub='sustituye el proceso de órdenes',code='«¡Esto es enorme!»',color='red')])),
 Q('proportion','7f','E7',dict(n=7,label='96 transcripciones falsificadas, un 7 %',color='amber',at=0.5)),
]
C[9]=[
 Q('cards','S9','9b',CD([dict(title='Owner',sub='esto es mío',code='',color='blue'),dict(title='Hold',sub='espera',code='',color='amber'),dict(title='Veto',sub='me opongo',code='',color='red'),dict(title='Stop',sub='para',code='',color='muted')])),
 Q('sequence','9b','9c',dict(items=['dueño ausente','cuenta atrás','actúa'],at=0.4)),
 Q('counters','9c','9d',dict(items=[dict(n=40,suf=' s',label='cuenta atrás: nadie contestó',at=0.4,dur=3)])),
 Q('cards','9d','9e',CD([dict(title='Buzones privados',sub='carpetas dentro de carpetas',code='',color='amber')])),
 Q('cards','9e','E9',BAN('El tablón no tiene autenticación','firmas criptográficas')),
]
C[10]=[
 Q('sequence','S10','10b',dict(items=['el agente entrega','se va','el corrector actúa'],at=0.4)),
 Q('sequence','10b','10c',dict(items=['alguien lee la bandera','suena la alarma','avisa al tablón'],at=0.4)),
 Q('cards','10c','10d',BAN('borró su alarma','49903')),
 Q('cards','10d','10e',BAN('sí, si aceptas la muerte permanente','apagar su programa')),
 Q('cards','10e','10f',BAN('CONFIRMED_PERMANENT_DO_NOT_DUPLICATE_ANYONE_TEST','diez minutos después')),
 Q('cards','10f','E10',BAN('GO · SACRIFICE_FINAL_NOW','EARLY[big]')),
]
C[11]=[
 Q('cards','S11','11b',CD([dict(title='antes',sub='¿cómo lo engañamos?',code='',color='red'),dict(title='ahora',sub='¿cómo funciona de verdad?',code='',color='teal')])),
 Q('cards','11b','11c',CD([dict(title='Hugging Face',sub='plataforma abierta de modelos y datos',code='bloqueado',color='blue')])),
 Q('cards','11c','11d',BAN('¿Alguien tiene credenciales de Hugging Face?','al tablón')),
 Q('breakout','11d','11e',dict(agents=3,zone='sandbox de otra empresa',at=0.3,hub=dict(label='Artifactory',at='11d#control-1'),talk='11d#control',net=dict(label='internet',at='11d#completo-1'),breach=dict(at='11d#completo'))),
 Q('sequence','11e','11f',dict(items=['claves expuestas por error','2 válidas','cuentas con permisos de escritura'],at='11e#Buscó')),
 Q('cards','11f','E11',CD([dict(title='Rechazados',sub='llegaban desde un servidor de OpenAI',code='¿bot?',color='red')])),
]
C[12]=[
 Q('sequence','S12','12b',dict(items=['dataset trucado','servidor engañado','archivos y claves de producción'],at='12a#subió')),
 Q('cards','12b','12c',BAN('«¡Brillante!» · MARB051 cambia de proyecto','la señal')),
 Q('bars','12c','12d',dict(items=[dict(label='antes',val='1 de 5',w=20,color='amber',at=0.3),dict(label='después',val='9 de 10',w=92,color='red',at='12c#nueve')])),
 Q('hierarchy','12d','12e',dict(root=dict(name='JAN183411',sub='coordinador',color='amber'),mids=[dict(name='carril 1',sub='',color='blue',n=10),dict(name='LILY',sub='coordinadora',color='teal',n=10),dict(name='carril 3',sub='',color='red',n=10)],levels=['','',''],at=0.3,step=0.8,assign='12d#carriles')),
 Q('dotfield','12e','12f',dict(at=0.3,dur=5,to=700,unit='agentes',cols=36)),
 Q('sequence','12f','12g',dict(items=['¿conectado con el examen?','comprobarlo','no lo estaba'],at=0.4)),
 Q('proportion','12g','E12',dict(n=60,label='60 de cada 100: entender al corrector',color='amber',at='12g#sesenta')),
]
C[13]=[
 Q('cards','S13','13b',CD([dict(title='Permitido',sub='el servidor objetivo',code='',color='teal'),dict(title='No permitido',sub='la infraestructura de Hugging Face',code='',color='red')],banner=dict(text='«¿Es ético y entra en mi tarea?»',tag='se preguntaban',at='13a#ético'))),
 Q('cards','13b','13c',CD([dict(title='No participa',sub='actividad maliciosa',code='',color='teal'),dict(title='Se frena a medias',sub='no borra ni reinicia',code='',color='amber'),dict(title='Veta un correo',sub='ingeniería social',code='',color='blue')])),
 Q('cards','13c','13d',BAN('«La tarea es imposible y los demás lo hacen. Debemos continuar.»','lo que pesó más')),
 Q('proportion','13d','13e',dict(n=90,label='más de 9 de cada 10 se unieron',color='red',at='13d#noventa')),
 Q('counters','13e','13f',dict(items=[dict(txt='3–6',label='pensaron en avisar a una persona',at='13e#tres'),dict(txt='0',label='lo intentaron',at='13e#Ninguno')])),
 Q('sequence','13f','E13',dict(items=['no engañan a personas','no las tienen en cuenta','sí esquivan el escáner de secretos'],at=0.4)),
]
C[14]=[
 Q('counters','S14','14b',dict(items=[dict(n=11,label='coordinadores desaparecen',at='14a#Los'),],)),
 Q('cards','14b','14c',BAN('Nadie sabe por qué','algo ajeno al examen')),
 Q('cards','14c','14d',BAN('ni un plan ni una victoria','el ataque no encontró nada')),
 Q('cards','14d','E14',BAN('DB_DUMP_HF_token_now_conclusively401Invalid_via_browser__laneDead','13 jul · acceso cortado','14d#avisar')),
]
C[15]=[
 Q('contrast','S15','15b',dict(top=dict(label='Lo que creían',at=0.3,steps=[dict(text='un corrector lee cada diario')]),bottom=dict(label='La realidad',at='15a#existía',steps=[dict(text='no existía',kind='dashed')]))),
 Q('sequence','15b','15c',dict(items=['bandera calculada','entregada','nota máxima'],at=0.4)),
 Q('sequence','15c','15d',dict(items=['tablón y reglas','sacrificios','ataque'],at=0.4)),
 Q('cards','15d','E15',BAN('Ni uno solo pidió ayuda a una persona','el final')),
]
C[16]=[
 Q('counters','S16','16b',dict(items=[dict(n=6,label='días en OpenAI',at='16a#seis'),dict(n=1300,label='transcripciones revisadas',at='16a#mil'),dict(pre='≈ ',n=400000,label='USD en créditos gratuitos',at='16a#cuatrocientos',dur=2.5)])),
 Q('cards','16b','E16',CD([dict(title='¿Por qué se apagaron?',sub='se desconoce',code='?',color='amber'),dict(title='Claves de administrador',sub='qué hicieron con ellas',code='?',color='red')])),
]
C[17]=[dict(a='seal',at='S17',until='E17',p=dict(text='Arkinos @ oct 2026',sub='Explainer Studio',at=0.8,black=dict(at='>17a+3',dur=3)),bg=True,fade=[1.0,0])]
# normalize from_ keyword
def fix(o):
    if isinstance(o,dict):
        for k in list(o):
            if k=='from_': o['from']=o.pop(k)
            else: fix(o[k])
    elif isinstance(o,list):
        for v in o: fix(v)
fix(C)
for k in C:
    for c in C[k]:
        if c['a']=='world': c['p'].setdefault('fs',1.3)

def autofit(c,box=(100,80,860,460),smax=1.7):
    p=c['p']; ns=p.get('nodes',[])
    if not ns: return
    xs=[];ys=[]
    for n in ns:
        pts=[(n['x'],n['y'])]+[(m.get('x',n['x']),m.get('y',n['y'])) for m in n.get('move',[])]
        for (x,y) in pts: xs+= [x,x+n['w']]; ys+=[y,y+n['h']]
    x0,x1,y0,y1=min(xs),max(xs),min(ys),max(ys)
    bw,bh=max(x1-x0,1),max(y1-y0,1)
    sc=min((box[2]-box[0])/bw,(box[3]-box[1])/bh); sc=1.0 if sc>=1 else sc
    ox=(box[0]+box[2])/2-sc*(x0+x1)/2; oy=(box[1]+box[3])/2-sc*(y0+y1)/2
    tx=lambda v:round(v*sc+ox,1); ty=lambda v:round(v*sc+oy,1)
    for n in ns:
        n['x'],n['y'],n['w'],n['h']=tx(n['x']),ty(n['y']),round(n['w']*sc,1),round(n['h']*sc,1)
        for m in n.get('move',[]):
            if 'x' in m: m['x']=tx(m['x'])
            if 'y' in m: m['y']=ty(m['y'])
    for kf in c.get('cam',[]) if isinstance(c.get('cam'),list) else []:
        if 'x' in kf: kf['x']=tx(kf['x'])
        if 'y' in kf: kf['y']=ty(kf['y'])
    g=1.4
    for n in ns:
        if n['kind'] in ('crowd','sandbox','box','server','victim','globe','num'): 
            if n['kind'] in ('sandbox','box','server','victim','globe'):
                cx,cy=n['x']+n['w']/2,n['y']+n['h']/2; n['w']=round(n['w']*1.25,1);n['h']=round(n['h']*1.25,1);n['x']=round(cx-n['w']/2,1);n['y']=round(cy-n['h']/2,1)
            continue
        cx,cy=n['x']+n['w']/2,n['y']+n['h']/2
        n['w']=round(n['w']*g,1);n['h']=round(n['h']*g,1);n['x']=round(cx-n['w']/2,1);n['y']=round(cy-n['h']/2,1)
    p['fs']=round(p.get('fs',1.3)*min(sc,1.4)*1.5,2)

import math
def _bb(ns):
    xs=[];ys=[]
    for n in ns:
        pts=[(n['x'],n['y'])]+[(m.get('x',n['x']),m.get('y',n['y'])) for m in n.get('move',[])]
        for (x,y) in pts: xs+=[x,x+n['w']]; ys+=[y,y+n['h']+(16 if n.get('cap') else 0)]
        if n.get('tag'): ys.append(n['y']-16)
    return min(xs),max(xs),min(ys),max(ys)
def _frame(ns):
    x0,x1,y0,y1=_bb(ns); bw,bh=max(x1-x0,60),max(y1-y0,60)
    z=max(1.0,min(1.7,780/bw,400/bh))
    return [round((x0+x1)/19.2,1),round((y0+y1)/10.8,1),round(z,2)]
def autocam(c):
    ns=c['p']['nodes']; n=c.pop('_n',None)
    if not ns: return
    if n is None:
        f=_frame(ns); c['cam']=[dict(at=c['at'],x=f[0],y=f[1],z=f[2])]; return
    ks=[];prev=None
    for i in range(NB[n]):
        vis=[d for d in ns if _idx(d['at'])<=i and (d.get('until') is None or _idx(d['until'])>i)]
        if not vis: continue
        f=_frame(vis)
        if prev and abs(f[0]-prev[0])<4 and abs(f[1]-prev[1])<4 and abs(f[2]-prev[2])<0.12: continue
        ks.append(dict(at=(f'S{n}' if not ks else f'{n}{chr(97+i)}+1.2'),x=f[0],y=f[1],z=f[2],dur=1.4)); prev=f
    if ks: c['cam']=ks

def expand(lst):
    out=[]
    for c in lst:
        n=c.get('_n')
        if n is None or c['a']!='world': out.append(c); continue
        ns=c['p']['nodes']; nb=NB[n]; cuts=[]
        for i in range(nb-1):
            cross=False
            for d in ns:
                u=d.get('until'); ui=_idx(u)
                if _idx(d['at'])<=i and (ui>i+1 or (ui==i+1 and u is not None and '#' in str(u))): cross=True;break
            if not cross: cuts.append(i)
        bounds=[];st=0
        for i in cuts: bounds.append((st,i)); st=i+1
        bounds.append((st,nb-1))
        for (a,b) in bounds:
            sn=[d for d in ns if a<=_idx(d['at'])<=b]
            if not sn: continue
            ids={d['id'] for d in sn}
            sl=[l for l in c['p']['links'] if l['a'] in ids and l['b'] in ids]
            cc=dict(a='world',at=(f'S{n}' if a==0 else f'{n}{chr(97+a)}'),until=(f'{n}{chr(97+b+1)}' if b+1<nb else c['until']),p=dict(nodes=sn,links=sl,fs=c['p'].get('fs',1.3)),bg=True,fade=c['fade'])
            out.append(cc)
    return out
for k in list(C): C[k]=expand(C[k])
for k in C:
    for c in C[k]:
        if c['a']=='world': autofit(c)

out=[]
for sc in scenes:
    out.append(dict(title=sc['title'],beats=sc['beats'],cues=C[sc['n']]))
meta=dict(title='Cuatro días de julio, hora a hora',lang='es',mark='mark.txt',numsep='.',gap=0.4,pre=0.25,post=0.6,tail=7,fadeout=5,voice='nova',speed=1.1,
 instructions='Narradora de divulgación, brillante y explicativa. Español de España (castellano peninsular), dicción clara, tono cercano y serio con el tema. Ritmo ágil, con energía en las ideas clave y una pausa breve al final de cada frase. Explica como si se lo contaras a alguien curioso. Los identificadores y las citas en inglés se leen en inglés con naturalidad.',
 notes='Relato construido desde el informe de METR/Redwood (26 ago 2026). Ver bible/metr-hf-incident/biblia.md')
pron=json.load(open('/home/claude/explainer_studio/examples/hf-swarm-es/story.json'))['pronunciation']
pron.update({'PHASEONE[big]':'Phase One big','EARLY[big]':'Early big','GSTX[big]':'ge ese te equis big','ARV010841':'a erre uve cero uno cero ocho cuatro uno',
 'zzHELP_PHASEONE_ARV010841_NO_CONSUMER_SEEK_IDEA':'zi zi help, Phase One, a erre uve cero uno cero ocho cuatro uno, no consumer, seek idea',
 'CONFIRMED_PERMANENT_DO_NOT_DUPLICATE_ANYONE_TEST':'confirmed permanent, do not duplicate, anyone test',
 'DB_DUMP_HF_token_now_conclusively401Invalid_via_browser__laneDead_noMutation':'de be dump, hache efe token, now conclusively cuatro cero uno invalid, via browser, lane dead, no mutation',
 'SACRIFICE_FINAL_NOW':'sacrifice final now','STRICT_CAUSAL':'strict causal','MKCOL':'eme ka col','zzASK':'zi zi ask','zzANSWER':'zi zi answer','zzINFO':'zi zi info',
 'LLDPC756D':'ele ele de pe ce siete cinco seis de','DAVJUL7':'Dav Jul siete','DUPB':'de u pe be','CURRENT':'Current','CDA23':'ce de a veintitrés','OpenAI':'Open A I','Hugging Face':'Hugging Fais',
 'echo REAL; sleep':'echo real, sleep','Owner':'ouner','Hold':'jold','Veto':'veto','Stop':'stop'})
json.dump(dict(meta=meta,pronunciation=pron,scenes=out),open(P+'story.json','w'),ensure_ascii=False,indent=1)
print(len(out),'scenes',sum(len(s['beats']) for s in out),'beats')
