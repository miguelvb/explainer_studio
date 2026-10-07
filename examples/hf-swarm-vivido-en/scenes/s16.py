# Scene 16 · What We Know and What We Don't
MUSIC={'bells': 0.7, 'cinema': 0.3}
cues=[]
n=[W.counter('d6',120,60,6,at='16a#six',cap='days at OpenAI',w=200,dur=1.8,fs=64),
   W.counter('t13',390,60,1300,at='16a#thirteen',cap='transcripts reviewed',w=240,dur=2.4,fs=64),
   W.counter('dl',680,60,400000,at='16a#four',cap='dollars in free credits',w=260,dur=2.6,fs=64)]
for i in range(30):
    n.append(N(f'tr{i}','sheet',70+(i%10)*80,230+(i//10)*70,56,50,f'16a#thirteen+{0.05*i:.2f}',color=BLU,lines=['···'],fs=12))
n+=SA('ai',480,470,'16a#agents',s=34,color='#3FD8C2')+[N('lp','lupa',500,445,50,50,'16a#agents+0.3',color='teal'),
   ic('er','question',700,470,40,'16a#errors',color='amber'),T('er2',730,466,'may contain errors','16a#errors',color='amber',fs=13)]
cues.append(K('S16','16b',n,[],fs=1.0))
n=[ic('q1','question',200,170,100,'16b#shut',color='amber'),T('q1l',130,260,'why they shut down','16b#shut',color=GRY,fs=15),
   ic('k1','key',620,160,80,'16b#credentials',color='amber'),ic('q2','question',720,150,60,'16b#credentials+0.4',color='amber'),
   T('k1l',580,260,'administrator credentials','16b#credentials',color=GRY,fs=15),T('k1d',600,300,'July 13','16b#July',color=GRY,fs=15)]
cues.append(K('16b','E16',n,[],fs=1.0))
cues[-1]['fade']=[0.5,0.5]   # the last scene before the quotes fades out to the empty stage
