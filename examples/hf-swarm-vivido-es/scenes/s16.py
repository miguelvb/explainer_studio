# Scene 16 · Lo que sabemos y lo que no
MUSIC={'bells': 0.7, 'cinema': 0.3}
cues=[]
n=[W.counter('d6',120,60,6,at='16a#seis',cap='días en OpenAI',w=200,dur=1.8,fs=64),
   W.counter('t13',390,60,1300,at='16a#mil',cap='transcripciones revisadas',w=240,dur=2.4,fs=64),
   W.counter('dl',680,60,400000,at='16a#cuatrocientos',cap='dólares en créditos gratuitos',w=260,dur=2.6,fs=64)]
for i in range(30):
    n.append(N(f'tr{i}','sheet',70+(i%10)*80,230+(i//10)*70,56,50,f'16a#mil+{0.05*i:.2f}',color=BLU,lines=['···'],fs=12))
n+=SA('ai',480,470,'16a#agentes',s=34,color='#3FD8C2')+[N('lp','lupa',500,445,50,50,'16a#agentes+0.3',color='teal'),
   ic('er','question',700,470,40,'16a#errores',color='amber'),T('er2',730,466,'pueden contener errores','16a#errores',color='amber',fs=13)]
cues.append(K('S16','16b',n,[],fs=1.0))
n=[ic('q1','question',200,170,100,'16b#apagaron',color='amber'),T('q1l',130,260,'por qué se apagaron','16b#apagaron',color=GRY,fs=15),
   ic('k1','key',620,160,80,'16b#claves',color='amber'),ic('q2','question',720,150,60,'16b#claves+0.4',color='amber'),
   T('k1l',580,260,'claves de administrador','16b#claves',color=GRY,fs=15),T('k1d',600,300,'13 julio','16b#trece',color=GRY,fs=15)]
cues.append(K('16b','E16',n,[],fs=1.0))
cues[-1]['fade']=[0.5,0.5]   # the last scene before the quotes fades out to the empty stage
