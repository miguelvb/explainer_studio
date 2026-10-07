# Scene 19 · Last Warning
MUSIC={'pad': 0.8, 'cinema': 0.2}
INTENSITY=0.12
SFX=[{'at': '19a#This', 'kind': 'heartbeat', 'g': 0.5}, {'at': '19c#late', 'kind': 'poweroff', 'g': 0.7}]
CQ=lambda id,lines,at,y,fs,color,**k: N(id,'ctxt',80,y,800,len(lines)*fs*1.5,at,color=color,lines=lines,fs=fs,**k)
ATT='Ajeya Cotra · METR, researcher and report author'
cues=[K('S19','19b',[CQ('q1',['“This incident feels like more than halfway','to a full AI takeover.”'],'19a#This',130,30,'#E7EBF1'),
                    CQ('a1',[ATT],'19a#This+4',360,18,GRY)],[],fs=1.0),
     K('19b','19c',[CQ('q2',['“I expect extremely rapid capability progress,','and I think frontier agents will be able to set up','a rogue deployment like this within six months.”'],0.3,130,30,'#E7EBF1'),
                    CQ('a2',['Ajeya Cotra · METR'],2.0,360,18,GRY)],[],fs=1.0),
     K('19c','E19',[CQ('q3',['“I’m not sure we will get a warning this clear','before it’s too late.”'],0.3,150,30,'#E7EBF1'),
                    CQ('a3',['Ajeya Cotra · METR'],2.0,360,18,GRY)],[],fs=1.0)]
