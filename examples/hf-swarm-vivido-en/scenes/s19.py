# Scene 19 · Last Warning
MUSIC={'pad': 0.8, 'cinema': 0.2}
INTENSITY=0.12
SFX=[{'at': '19a#This', 'kind': 'heartbeat', 'g': 0.5}, {'at': '19c#late', 'kind': 'poweroff', 'g': 0.7}]
CQ=lambda id,lines,at,y,fs,color,**k: N(id,'ctxt',80,y,800,len(lines)*fs*1.5,at,color=color,lines=lines,fs=fs,**k)
ATT='Ajeya Cotra · METR, researcher and report author'
cues=[K('S19','19b',[CQ('q1',['“This incident feels like it’s more than 50% of the way','to full-blown AI takeover.”'],'19a#This',130,30,'#E7EBF1'),
                    CQ('a1',[ATT],'19a#This+4',360,18,GRY)],[],fs=1.0),
     K('19b','19c',[CQ('q2',['“I continue to expect extremely rapid advances in capabilities,','and think frontier agents will likely be capable of','establishing such a rogue deployment in six months.”'],0.3,130,30,'#E7EBF1'),
                    CQ('a2',['Ajeya Cotra · METR'],2.0,360,18,GRY)],[],fs=1.0),
     K('19c','E19',[CQ('q3',['“I am not sure that we will get such a clear warning shot','before it’s too late.”'],0.3,150,30,'#E7EBF1'),
                    CQ('a3',['Ajeya Cotra · METR'],2.0,360,18,GRY)],[],fs=1.0)]
