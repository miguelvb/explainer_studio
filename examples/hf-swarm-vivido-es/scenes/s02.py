# Scene 2 · Un examen imposible
MUSIC={'bells': 0.6, 'pad': 0.7}
cues=[]
EX=(330,50,340,440); CELL=26; MX=(340-260)//2; MY=(440-364)//2
fc=(EX[0]+MX+CELL*9, EX[1]+MY+CELL*13)           # centre of the open 2x2 chamber that holds the flag
ey=EX[1]+MY+CELL*6+CELL/2                                        # entry hole height
n=[N('ck','txt',30,30,400,32,0.2,color='teal',fs=24,type=9,text='07 julio 2026'),
   W.agent_named('v8',60,150,'V8SAME',at=0.4,until='2d#servía'),
   W.agent_named('ph',60,150,'PHASEONE10841',at='2d#servía',blink=.28),
   N('ex1','exam',*EX,'2a#examen',color='blue',maze=dict(cell=CELL,cols=10,rows=14,entry=6,seed=11,clear=[[12,8],[12,9],[13,8],[13,9]],end=[fc[0],fc[1]]),solve=dict(at='2b#aprovechar+1.0',dur=5),until='2d#servía'),
   N('ex2','exam',*EX,'2d#servía',color='red',maze=dict(on=False,cell=CELL,cols=10,rows=14,box=(12.5,8.5),boxs=62),tag='ARV010841',tagc='red',tagfs=16),
   N('fl','flFly',fc[0]-16,fc[1]-19,32,38,'2a#examen',color='amber',blink=.7,bf=9,bat='2b#bandera'),
   N('ho','hole',EX[0]-11,ey-11,22,22,'2b#fallo',color='red'),
   N('ho2','hole',EX[0]+170-11,EX[1]-11,22,22,'2c#Cualquier',color='red',until='2d#servía'),
   ic('ok','check',EX[0]-34,ey-34,40,'2c#asignado',color='teal',until='2d#servía'),
   ic('no','cross',EX[0]+170,EX[1]+34,36,'2c#suspenso',color='red',until='2d#servía'),
   N('eg','txt',EX[0]+EX[2]/2-75,18,150,24,'2a#ExploitGym',color='#E7EBF1',fs=24,text='ExploitGym',until='2d#servía')]
n[1]['blink']=.28; n[1]['bat']='2b#bandera'
n[2].update(blink=.55,bf=11,bat='2e#ARV010841',shake=dict(at='2e#ARV010841',dur=14,amp=3.2,f=27))
n[6].update(glowAt='2e#ARV010841+0.5',glowDur=9)
lk=[W.link('v8','ho','2b#aprovechar',color='teal',curve=.1,until='2d#servía'),W.link('ph','ho','2d#servía+0.5',color='teal',curve=.1),
    W.link('v8','ho2','2c#Cualquier',color='red',curve=.1,until='2d#servía'),
    W.link('ph','ho','2e#ARV010841',color='teal',curve=.22,speed=1.2),W.link('ph','ho','2e#ARV010841+0.4',color='teal',curve=.34,speed=1.5),W.link('ph','ho','2e#ARV010841+0.8',color='teal',curve=.46,speed=1.1)]
cues.append(K('S2','E2',n,lk,fs=1.0))
