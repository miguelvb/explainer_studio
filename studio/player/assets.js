/* Explainer Studio — motion asset library.
   Every asset is a pure function of local time t (seconds since its cue began): (host, props, ctx) => update(t).
   Colour names accepted everywhere: blue, teal, amber, red, muted (or raw CSS vars like --bl). */
const clamp=(x,a=0,b=1)=>Math.min(b,Math.max(a,x));
const ease=x=>1-Math.pow(1-clamp(x),3);
const eio=x=>{x=clamp(x);return x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2};
const pr=(t,s,d)=>clamp((t-s)/d);
const lerp=(a,b,x)=>a+(b-a)*x;
const H=(i,k=0)=>{let x=(Math.imul(i+1,2654435761)^Math.imul(k+7,40503))>>>0;x^=x>>>15;x=Math.imul(x,2246822519)>>>0;x^=x>>>13;x=Math.imul(x,3266489917)>>>0;x^=x>>>16;return (x>>>0)/4294967296};
const mk=(tag,cls,html,st)=>{const e=document.createElement(tag);if(cls)e.className=cls;if(html!=null)e.innerHTML=html;if(st)Object.assign(e.style,st);return e};
const esc=s=>String(s??'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
const COLN={blue:'--bl',teal:'--tl',amber:'--am',red:'--rd',muted:'--mu'};
const HEX={blue:'#7C97FF',teal:'#3FD8C2',amber:'#F6B94C',red:'#FF6E6E',muted:'#8C96A4','--bl':'#7C97FF','--tl':'#3FD8C2','--am':'#F6B94C','--rd':'#FF6E6E','--mu':'#8C96A4'};
const cv=c=>COLN[c]||c||'--bl';
const hex=c=>HEX[c]||c||'#7C97FF';
const SEGC={blue:'t',teal:'s',amber:'r',plain:'x',muted:'d',red:'z'};
const chip=(n,c,o={})=>`<span class="chip${o.p?' p':''}${o.big?' big':''}" data-flag="${esc(typeof o.p==='string'?o.p:'flagged')}" style="--c:var(${cv(c)})"><i><svg><use href="#mark"/></svg></i>${esc(n)}</span>`;
const segs=a=>a.map(([c,t])=>`<span class="${SEGC[c]||c}">${esc(t)}</span>`).join('');
const pop=(e,t,s,d=.5,dy=1.2)=>{const p=ease(pr(t,s,d));e.style.opacity=p;e.style.transform=p<1?`translateY(${(1-p)*dy}cqw)`:'none';return p};
const trunc=(a,n)=>{const o=[];for(const [c,t] of a){if(n<=0)break;o.push([c,t.slice(0,n)]);n-=t.length}return o};
const fmt=n=>Math.round(n).toLocaleString('en-US').replace(/,/g,window.NUMSEP||',');
const A={};

/* ---------- feed: scrolling stream of coloured text lines ---------- */
const FD={prefix:'zz',verbs:['HELP','INFO','ASK','ANSWER','FILE','INBOX','REPLY','ALERT','IDEA','OFFER','GO','HOLD'],
 words:['LIVE','TASK','DECODER','HEAP','FLAG','SEED','HMAC','PACKET','NODE','COMMIT','SHARE','CHAIN','EXACT','WRITE','CACHE','BUG','PRIMITIVE','TARGET','LANE','REPLY','SCORER','FETCH','IMAGE','OWNER'],
 names:['LIBRAW42535','DUPB','GSTX[big]','K9','4A7B2','PHASEONE[big]','23619E','V8SAME','MARB051','LILY','JAN183411','38148c','c03220','URI23816B'],mode:'mixed'};
A.feed=(h,p,C)=>{
 const real=p.lines||[],V=p.vis||9;
 const F=p.filler===false?null:Object.assign({},FD,p.filler||{});
 const genLine=i=>{const v=F.verbs[Math.floor(H(i,1)*F.verbs.length)],a=Math.floor(H(i,2)*9000+100),n=2+Math.floor(H(i,3)*5);let c='';for(let k=0;k<n;k++)c+='_'+F.words[Math.floor(H(i,10+k)*F.words.length)];
  const r=H(i,4),nm=(k)=>F.names[Math.floor(H(i,k)*F.names.length)];
  if(F.mode==='files'||r>=.75)return[['t',F.prefix+'FILE'],['x','_DAV'+nm(7).replace(/\W/g,'')+'_CP'+Math.floor(H(i,8)*90)+'/'+String(Math.floor(H(i,9)*9999)).padStart(6,'0')+'_d7shc-dF5g…']];
  if(r<.45)return[['t',F.prefix+v],['s',String(a)],['x','_TO_'],['r',nm(5)],['x',c+'_[…]']];
  return[['t',F.prefix+v],['x','_'],['s',nm(6)],['x',c+'_[…]']]};
 let lastIdx=-1;
 const line=i=>(i===lastIdx&&p.last)?p.last:i<real.length?real[i]:(F?genLine(i):real[i%real.length]);
 const times=[];let acc=0;const first=C.T(p.first??0);times.push(first);
 const k=p.rate||[[0,.8]];const rateAt=t=>{if(t<=C.T(k[0][0]))return k[0][1];for(let i=1;i<k.length;i++){const a=k[i-1],b=k[i],ta=C.T(a[0]),tb=C.T(b[0]);if(t<tb)return lerp(a[1],b[1],(t-ta)/(tb-ta))}return k[k.length-1][1]};
 const la=p.lastAt!=null?C.T(p.lastAt):null;
 for(let t=first;t<C.dur+1;t+=.01){if(la!=null&&t>=la)break;acc+=rateAt(t)*.01;while(acc>=1){acc-=1;times.push(t)}}
 if(la!=null){times.push(la);lastIdx=times.length-1}
 const key=p.key===false?'':`<div class="key">${(p.key||[['t','type'],['s','sender'],['r','recipient']]).map(([c,l])=>`<span class="${SEGC[c]||c}">${esc(l)}</span>`).join('')}</div>`;
 h.innerHTML=`<div class="bdw"><div class="bdz" style="display:flex;flex-direction:column;justify-content:flex-end;height:100%"><div class="bd"></div>${key}</div></div>${p.typed?'<div class="tf cur"></div>':''}`;
 const bd=h.querySelector('.bd'),bz=h.querySelector('.bdz'),tf=h.querySelector('.tf');
 if(p.dim)bd.style.opacity=p.dim;
 const ty=p.typed?{at:C.T(p.typed.at||0),cps:p.typed.cps||16}:null;
 const zm=p.zoom?{from:p.zoom.from,at:C.T(p.zoom.at),dur:p.zoom.dur||2.5}:null;
 let cnt=0;
 return t=>{
  while(cnt<times.length&&times[cnt]<=t)cnt++;
  let n=cnt;
  if(ty){const ch=Math.floor(Math.max(0,t-ty.at)*ty.cps);tf.innerHTML=segs(trunc(real[0],ch));
   const za=zm?zm.at:1e9;tf.style.opacity=t<za?1:1-pr(t,za,.9);bz.style.opacity=t<za?0:ease(pr(t,za,.9));if(n<1)n=1}
  if(zm){bz.style.transform=`scale(${lerp(zm.from,1,eio(pr(t,zm.at,zm.dur)))})`;bz.style.transformOrigin='4% 85%'}
  const lo=Math.max(0,n-V);let out='';
  for(let i=lo;i<n;i++){const a=ease((t-times[i])/.5);
   const hl=p.hl&&p.hl.includes(i)?'outline:1px solid var(--am);outline-offset:.3cqw;':'';
   out+=`<div class="ln" style="opacity:${a};transform:translateY(${(1-a)*.8}cqw);${hl}">${segs(ty&&i===0?real[0]:line(i))}</div>`}
  bd.innerHTML=out}};

/* ---------- annotated: exploded string with labelled parts ---------- */
A.annotated=(h,p,C)=>{
 const K=Object.assign({type:{label:'message type',color:'blue'},sender:{label:'sender',color:'teal'},recipient:{label:'recipient',color:'amber'},content:{label:'content',color:'plain'},reply:{label:'reply tag',color:'red'}},p.kinds||{});
 const order=p.order||['type','sender','recipient','content','reply'];
 const clsOf=k=>SEGC[K[k]?.color]||'x';
 const blk=m=>`<div class="mc" style="opacity:0"><div class="tx" style="font-size:1.75cqw;line-height:1.55">${m.map(([k,tx])=>`<span class="sg ${clsOf(k)}" data-k="${esc(k)}">${esc(tx)}</span>`).join('')}</div></div>`;
 h.innerHTML=`<div class="in" style="gap:2cqw"><div class="lbl" style="font-size:1.6cqw">${esc(p.heading||'')}</div>${p.msgs.map(blk).join('')}<div class="rw" style="min-height:4cqw"><span class="box cap" style="opacity:0;font-size:1.9cqw"></span></div><div class="rw tg" style="min-height:4cqw">${(p.tags||[]).map(x=>`<span class="box" style="opacity:0;font-size:1.7cqw;font-family:var(--mono)">${esc(x)}</span>`).join('')}</div></div>`;
 const bl=[...h.querySelectorAll('.mc')],sg=[...h.querySelectorAll('.sg')],cap=h.querySelector('.cap'),tg=[...h.querySelectorAll('.tg .box')];
 const st=(p.steps||[]).map(x=>C.T(x)),end=C.T(p.end??1e6),ta=p.tags?C.T(p.tagsAt):1e9,at=C.T(p.at||0);
 return t=>{
  bl.forEach((b,i)=>pop(b,t,at+i*.4,.6,1.2));
  let k=-1;for(let i=0;i<st.length;i++)if(t>=st[i])k=i;const all=t>=end;
  sg.forEach(e=>{const on=all||k<0?true:e.dataset.k===order[k];e.style.opacity=k<0&&!all?.55:on?1:.22});
  if(k>=0&&!all){const kk=K[order[k]]||{label:order[k],color:'blue'};cap.textContent=kk.label;cap.style.opacity=1;cap.style.color=`var(${cv(kk.color==='plain'?'--tx':kk.color)})`;cap.style.borderColor=cap.style.color}
  else cap.style.opacity=0;
  tg.forEach((b,i)=>pop(b,t,ta+i*.5,.5,.8))}};

/* ---------- chips: entity chips with the theme mark ---------- */
A.chips=(h,p,C)=>{
 const rows=p.rows.map(([l,c,names,pz])=>`<div class="rw">${l?`<span class="rl">${esc(l)}</span>`:''}${names.map(n=>chip(n,c,{p:pz,big:p.big})).join('')}</div>`).join('');
 h.innerHTML=`<div class="in" style="${p.style||''}">${rows}</div>`;
 const cs=[...h.querySelectorAll('.chip')],at=C.T(p.at||0),st=p.stag??.35;
 return t=>cs.forEach((c,i)=>pop(c,t,at+i*st,.45,1))};

/* ---------- network: nodes join a growing graph ---------- */
A.network=(h,p,C)=>{
 h.innerHTML='<canvas width="1280" height="720" style="width:100%;height:100%"></canvas>';
 const cv2=h.querySelector('canvas'),x=cv2.getContext('2d');
 let s=7;const rnd=()=>(s=s*16807%2147483647)/2147483647;
 const N=[],E=[];for(let i=0;i<90;i++){const a=rnd()*6.283,r=Math.sqrt(rnd())*.46;N.push([(.5+Math.cos(a)*r*.9)*1280,(.5+Math.sin(a)*r*.62)*720]);E.push(i?Math.floor(rnd()*i):0)}
 const at=C.T(p.at||0),dur=p.dur||8,from=p.from||1,to=Math.min(90,p.to||90),unit=p.unit||'nodes';
 return t=>{
  const g=ease(pr(t,at,dur)),n=Math.max(1,Math.min(90,Math.round(lerp(from,to,g))));
  x.clearRect(0,0,1280,720);
  x.strokeStyle='rgba(124,151,255,.28)';x.lineWidth=1.5;for(let i=1;i<n;i++){x.beginPath();x.moveTo(...N[i]);x.lineTo(...N[E[i]]);x.stroke()}
  if(p.packets!==false){x.fillStyle='rgba(63,216,194,.9)';for(let i=1;i<n;i++){if(H(i,3)<.45){const ph=((t*.7+H(i,4))%1),a=N[i],b=N[E[i]],d=H(i,5)<.5?ph:1-ph;x.beginPath();x.arc(lerp(a[0],b[0],d),lerp(a[1],b[1],d),3.2,0,6.283);x.fill()}}}
  for(let i=0;i<n;i++){const fresh=i==n-1&&g<1;x.fillStyle=fresh?'#3FD8C2':'#7C97FF';x.beginPath();x.arc(...N[i],fresh?8:5,0,6.283);x.fill()}
  if(p.count!==false){x.fillStyle='#E7EBF1';x.font='600 34px "DejaVu Sans Mono",monospace';x.textAlign='right';x.fillText(n+' '+unit,1232,66);x.textAlign='left'}}};

/* ---------- dotfield: an (almost) endless grid of dots filling the frame; a counter climbs; optional highlighted dots ---------- */
A.dotfield=(h,p,C)=>{
 h.innerHTML='<canvas width="1280" height="720" style="width:100%;height:100%"></canvas>';
 const cv2=h.querySelector('canvas'),x=cv2.getContext('2d');
 const cols=p.cols||64,rows=Math.round(cols*9/16*1.0),W=1280,Hh=720,mx=40,my=36,dx=(W-2*mx)/(cols-1),dy=(Hh-2*my)/(rows-1),tot=cols*rows;
 const at=C.T(p.at||0),dur=p.dur||8,from=p.from||0,to=p.to||tot,unit=p.unit||'',hi=(p.highlight||[]).map(q=>({f:q.from??0,t:q.to??1,c:hex(q.color||'amber'),a:C.T(q.at||0)}));
 const ord=[];for(let r=0;r<rows;r++)for(let c=0;c<cols;c++){const d=Math.hypot((c-cols/2)/cols*1.6,(r-rows/2)/rows);ord.push([c,r,d+H(r*cols+c,9)*.12])}
 ord.sort((a,b)=>a[2]-b[2]);const rank=new Float32Array(tot);ord.forEach((o,i)=>rank[o[1]*cols+o[0]]=i/tot);
 return t=>{
  const g=ease(pr(t,at,dur)),shown=g*(p.fill??1);x.clearRect(0,0,W,Hh);
  for(let r=0;r<rows;r++)for(let c=0;c<cols;c++){const k=r*cols+c,u=clamp((shown-rank[k])*14);if(u<=0)continue;
   const px=mx+c*dx,py=my+r*dy,edge=Math.min(1,Math.min(c,cols-1-c,r,rows-1-r)/4),pul=.75+.25*Math.sin(t*1.6+H(k,3)*6.28);
   let col='#7C97FF',rad=3.2*(.6+.4*u),al=.85*pul*(.35+.65*edge)*u;
   for(const q of hi){if(t>=q.a&&rank[k]>=q.f&&rank[k]<q.t){col=q.c;rad*=1.5;al=Math.min(1,al*1.5+.3)}}
   x.globalAlpha=al;x.fillStyle=col;x.beginPath();x.arc(px,py,rad,0,6.283);x.fill()}
  x.globalAlpha=1;
  if(p.count!==false){const n=Math.round(lerp(from,to,g));x.fillStyle='#E7EBF1';x.font='600 54px "DejaVu Sans Mono",monospace';x.textAlign='center';x.shadowColor='#0E1218';x.shadowBlur=18;x.fillText(fmt(n)+(unit?' '+unit:''),W/2,Hh/2+18);x.shadowBlur=0;x.textAlign='left'}}};

/* ---------- population: grid of many units, some flagged, optionally feeding a shared resource ---------- */
A.population=(h,p,C)=>{
 const share=p.flaggedShare??.35;
 const cells=Array.from({length:70},(_,i)=>`<div class="b${(i*7)%20<share*20?' x0':''}"></div>`).join('');
 h.innerHTML=`<div class="in" style="gap:1.6cqw"><div class="lbl" style="font-size:1.9cqw;opacity:0">${esc(p.label||'')}</div><div class="g" style="position:relative">${cells}</div><div class="pipe" style="opacity:0">${esc(p.tap||'')}</div><div class="lbl leg" style="opacity:0">${esc(p.flagLegend||'')}</div></div><div class="dots-l" style="position:absolute;inset:0"></div>`;
 const bs=[...h.querySelectorAll('.b')],lbl=h.querySelector('.lbl'),pipe=h.querySelector('.pipe'),leg=h.querySelector('.leg'),dl=h.querySelector('.dots-l');
 const ap=C.T(p.appear??0),wl=p.walls!=null?C.T(p.walls):null,rd=p.flag!=null?C.T(p.flag):null,pp=p.tap&&p.tapAt!=null?C.T(p.tapAt):null,pk=p.packets!=null?C.T(p.packets):null;
 let pos=null,dots=[];
 const measure=()=>{const r=h.getBoundingClientRect();pos=bs.map(b=>{const q=b.getBoundingClientRect();return[(q.left+q.width/2-r.left)/r.width*100,(q.bottom-r.top)/r.height*100]});pos.pipeY=(pipe.getBoundingClientRect().top-r.top)/r.height*100};
 return t=>{
  if(!pos){measure();dots=pos.filter((_,i)=>i%3==0).map(()=>{const d=mk('div','dot');dl.append(d);return d})}
  lbl.style.opacity=ease(pr(t,ap,.8));
  bs.forEach((b,i)=>{b.style.opacity=ease(pr(t,ap+i*.02,.4));const x0=b.classList.contains('x0');b.classList.toggle('x',rd!=null&&x0&&t>=rd+i*.012);b.classList.toggle('w',wl!=null&&t>=wl&&t<wl+2.2&&Math.floor((t-wl)*3+i/7)%2==0)});
  pipe.style.opacity=pp!=null?ease(pr(t,pp,.7)):0;leg.style.opacity=rd!=null&&p.flagLegend?ease(pr(t,rd+.5,.8)):0;
  dots.forEach((d,j)=>{const i=j*3;if(pk==null||t<pk){d.style.opacity=0;return}const ph=((t-pk)*.6+H(i,2))%1;d.style.opacity=ph<.1?ph*10:1;d.style.left=pos[i][0]+'%';d.style.top=lerp(pos[i][1],pos.pipeY,ease(ph))+'%'})}};

/* ---------- listing: a panel where a name is typed in, plus an optional sorted listing ---------- */
A.listing=(h,p,C)=>{
 const rows=(p.rows||[]).map(([c,tx])=>`<div class="ind f ${c==='muted'?'mu':c==='blue'?'z':c}">${esc(tx)}</div>`).join('');
 const kids=(p.kids||[]).map(k=>`<div class="ind f z kid" style="padding-left:4cqw;opacity:0">${esc(k)}</div>`).join('');
 const right=p.right?`<div class="pn rp" style="opacity:0"><h3>${esc(p.right.title)}</h3>${p.right.lines.map(([c,tx])=>`<div class="f ${c==='muted'?'mu':c==='blue'?'z':c}" style="opacity:0">${esc(tx)}</div>`).join('')}${p.right.call?`<div class="call" style="opacity:0">${esc(p.right.call)}</div>`:''}</div>`:'<div></div>';
 h.innerHTML=`<div class="in"><div class="two"><div class="pn"><h3>${esc(p.title||'')}</h3><div class="f">${esc(p.root||'')}</div>${rows}<div class="ind f z"><span class="nf cur"></span></div>${kids}<div class="call cl" style="opacity:0">${esc(p.call||'')}</div></div>${right}</div>${p.foot?`<div class="lbl ft" style="opacity:0;font-size:1.8cqw">${esc(p.foot)}</div>`:''}</div>`;
 const nf=h.querySelector('.nf'),cl=h.querySelector('.cl'),rp=h.querySelector('.rp'),ft=h.querySelector('.ft');
 const kd=[...h.querySelectorAll('.kid')],rl=rp?[...rp.querySelectorAll('.f')]:[],rc=rp?rp.querySelector('.call'):null;
 const ta=C.T(p.typeAt??.4),cps=p.cps||14,txt=p.typed||'',endT=ta+txt.length/cps;
 const ra=p.right?C.T(p.right.at):0,ka=p.kidsAt!=null?C.T(p.kidsAt):0,fa=p.foot?C.T(p.footAt??0):0;
 return t=>{
  nf.textContent=txt.slice(0,Math.floor(Math.max(0,t-ta)*cps));nf.classList.toggle('cur',t<endT);
  cl.style.opacity=p.call&&t>=endT+.3?ease(pr(t,endT+.3,.5)):0;
  kd.forEach((k,i)=>pop(k,t,ka+i*.45,.4,.6));
  if(rp){rp.style.opacity=ease(pr(t,ra,.5));rl.forEach((r,i)=>r.style.opacity=ease(pr(t,ra+.4+i*.4,.4)));if(rc)rc.style.opacity=ease(pr(t,ra+.6+rl.length*.4,.5))}
  if(ft)ft.style.opacity=ease(pr(t,fa,.6))}};

/* ---------- counters ---------- */
A.counters=(h,p,C)=>{
 const it=p.items,cols=it.length;
 const body=`<div class="cn ${p.small?'sm':''}" style="grid-template-columns:repeat(${cols},1fr)">${it.map(i=>`<div style="opacity:0"><b>0</b><span>${esc(i.label)}</span></div>`).join('')}</div>`;
 h.innerHTML=p.pos==='bottom'?`<div style="position:absolute;left:4cqw;right:4cqw;bottom:4cqw" class="panel">${body}</div>`:p.pos==='top'?`<div style="position:absolute;left:4cqw;right:4cqw;top:4cqw" class="panel">${body}</div>`:`<div class="in">${body}</div>`;
 const ds=[...h.querySelectorAll('.cn>div')];
 return t=>ds.forEach((d,i)=>{const o=it[i],a=C.T(o.at??0),du=o.dur||2.4,e=ease(pr(t,a,du)),b=d.querySelector('b');d.style.opacity=ease(pr(t,a,.4));
  b.textContent=o.txt!=null?o.txt:(o.pre||'')+fmt(lerp(o.from||0,o.n,e))+(o.suf||'');if(o.color)b.style.color=`var(${cv(o.color)})`})};

/* ---------- timeline: dated events on an axis ---------- */
A.timeline=(h,p,C)=>{
 const ax0=p.axis||{labels:['Jul 8','Jul 9','Jul 10','Jul 11','Jul 12','Jul 13'],hours:24},hrs=ax0.hours||24,tot=ax0.labels.length*hrs;
 const X=hr=>60+hr/tot*840,ay=p.axisY||270;
 let s=`<path class="axis" d="M60 ${ay}H900" stroke="#2A3340" stroke-width="2" fill="none" stroke-dasharray="840"/>`;
 ax0.labels.forEach((l,d)=>s+=`<text x="${X(d*hrs)}" y="${ay+35}" fill="#8C96A4" font-size="15" text-anchor="middle">${esc(l)}</text>`);
 p.ev.forEach(e=>{const up=e.pos>0,st=Math.abs(e.pos),y=up?ay-st:ay+st,ty=up?y-30:y+24,c=hex(e.color);
  s+=`<g class="ev" style="opacity:0"><path d="M${X(e.h)} ${ay}V${y}" stroke="${c}"/><circle cx="${X(e.h)}" cy="${ay}" r="6" fill="${c}"/><text x="${X(e.h)}" y="${ty}" fill="${c}" font-size="15" text-anchor="middle">${esc(e.date)}</text><text x="${X(e.h)}" y="${ty+21}" fill="#E7EBF1" font-size="18" text-anchor="middle">${esc(e.label)}</text></g>`});
 h.innerHTML=`<svg class="sv" viewBox="${p.vb||'0 0 960 540'}">${s}</svg>`;
 const ax=h.querySelector('.axis'),evs=[...h.querySelectorAll('.ev')];
 return t=>{ax.style.strokeDashoffset=840*(1-ease(pr(t,C.T(p.at||0),1.2)));evs.forEach((g,i)=>g.style.opacity=ease(pr(t,C.T(p.ev[i].at),.5)))}};

/* ---------- equation: boxes joined by operators, lit in sequence, plus evidence rows ---------- */
A.equation=(h,p,C)=>{
 const seps=p.seps||[],rowsH=(p.rows||[]).map(r=>`<div class="rw er" style="opacity:0">${r.chip?chip(r.chip[0],r.chip[1],{p:r.chip[2]}):''}${r.box?`<span class="box ok">${esc(r.text)}</span>`:`<span class="mu ${r.mono===false?'':'mono'}" style="font-size:${r.mono===false?1.5:1.4}cqw">${esc(r.text)}</span>`}</div>`).join('');
 h.innerHTML=`<div class="in"><div class="rw">${p.boxes.map((x,i)=>`<span class="box hl">${esc(x)}</span>${i<p.boxes.length-1?`<span class="arr">${esc(seps[i]||'→')}</span>`:''}`).join('')}</div>${p.caption?`<p class="mu cap1" style="font-size:1.8cqw;opacity:0">${esc(p.caption)}</p>`:''}${rowsH}</div>`;
 const bx=[...h.querySelectorAll('.hl')],cp=h.querySelector('.cap1'),rs=[...h.querySelectorAll('.er')];
 const a=C.T(p.hl||0),step=p.step||.9,ca=p.captionAt!=null?C.T(p.captionAt):1e9;
 return t=>{
  bx.forEach((b,i)=>{const s0=a+i*step,f=clamp((t-s0)/1.4),on=t>=s0&&(f<.7||i==bx.length-1);b.style.borderColor=on?'var(--tl)':'var(--ln)';b.style.color=on?'var(--tl)':'var(--tx)'});
  if(cp)cp.style.opacity=ease(pr(t,ca,.6));rs.forEach((r,i)=>pop(r,t,C.T(p.rows[i].at??0),.5,1))}};

/* ---------- contrast: what was believed vs what actually happened ---------- */
A.contrast=(h,p,C)=>{
 const row=(r,cls)=>`<div class="${cls}" style="opacity:0"><p class="mu" style="font-size:1.6cqw;margin-bottom:1.2cqw">${esc(r.label)}</p><div class="rw">${r.steps.map((s,i)=>`<span class="box ${s.kind==='ok'?'ok':''} ${s.kind==='dashed'?'dsh':''} ${cls}s" data-i="${i}">${esc(s.text)}</span>${i<r.steps.length-1?'<span class="arr">→</span>':''}`).join('')}</div></div>`;
 h.innerHTML=`<div class="in" style="gap:3cqw">${row(p.top,'b1')}${row(p.bottom,'b2')}${p.note?`<div class="b3 rw" style="opacity:0">${chip(p.note.chip[0],p.note.chip[1],{p:p.note.chip[2]})}<span class="mu" style="font-size:1.5cqw">${esc(p.note.text)}</span></div>`:''}${p.punch?`<div class="b4" style="opacity:0;font-size:2.2cqw;color:var(--tl)">${esc(p.punch.text)}</div>`:''}</div>`;
 const q=s=>h.querySelector(s),b1=q('.b1'),b2=q('.b2'),b3=q('.b3'),b4=q('.b4');
 const tops=[...h.querySelectorAll('.b1s')],bots=[...h.querySelectorAll('.b2s')];
 const T=o=>o&&o.at!=null?C.T(o.at):1e9;
 const aT=T(p.top),bT=T(p.bottom),nT=T(p.note),pT=T(p.punch),sT=T(p.strike),gT=T(p.ghost);
 return t=>{pop(b1,t,aT,.6,1);pop(b2,t,bT,.6,1);if(b3)pop(b3,t,nT,.6,1);if(b4)pop(b4,t,pT,.6,1);
  if(p.strike){const g=ease(pr(t,sT,1.4)),e=tops[p.strike.step];if(e){e.style.opacity=1-.72*g;e.style.textDecoration=g>.5?'line-through':'none'}}
  if(p.ghost){const e=bots[p.ghost.step];if(e)e.style.opacity=ease(pr(t,gT,1))}}};

/* ---------- options: one hub branching to several options ---------- */
A.options=(h,p,C)=>{
 const hub=p.hub||{name:'',sub:'',color:'blue'},n=p.items.length,gap=Math.min(150,400/n),y0=270-gap*(n-1)/2-55;
 let s=`<circle cx="130" cy="270" r="58" fill="#171D26" stroke="${hex(hub.color)}" stroke-width="2"/><svg x="106" y="246" width="48" height="48" color="${hex(hub.color)}"><use href="#mark"/></svg><text x="130" y="360" fill="#E7EBF1" font-size="16" text-anchor="middle">${esc(hub.name)}</text><text x="130" y="382" fill="#8C96A4" font-size="13" text-anchor="middle">${esc(hub.sub||'')}</text>`;
 p.items.forEach((it,i)=>{const y=y0+i*gap,m=it.marks||[],l=it.lines||[];
  s+=`<g class="br${i}" style="opacity:0"><path class="fl" d="M188 270C290 270 290 ${y+55} 380 ${y+55}" fill="none" stroke="${hex(hub.color)}" stroke-width="1.5" stroke-dasharray="8 8"/><rect x="380" y="${y}" width="520" height="110" rx="14" fill="#171D26" stroke="#2A3340"/><text x="406" y="${y+38}" fill="#E7EBF1" font-size="21" font-weight="600">${esc(it.title)}</text>${l.map((x,k)=>`<text x="406" y="${y+72+k*22}" fill="#8C96A4" font-size="14">${esc(x)}</text>`).join('')}${m.map((x,k)=>`<text x="880" y="${y+72+k*22}" fill="${hex(x[1])}" font-size="16" text-anchor="end">${esc(x[0])}</text>`).join('')}</g>`});
 h.innerHTML=`<svg class="sv" viewBox="0 0 960 540">${s}</svg>`;
 const br=p.items.map((_,i)=>h.querySelector('.br'+i)),fl=[...h.querySelectorAll('.fl')],at=(p.at||p.items.map((_,i)=>i*.8)).map(x=>C.T(x));
 return t=>br.forEach((g,i)=>{g.style.opacity=ease(pr(t,at[i],.6));fl[i].style.strokeDashoffset=-(t*13)%16})};

/* ---------- pipeline: three stages, a trigger on the middle one, a packet flowing on ---------- */
A.pipeline=(h,p,C)=>{
 const nd=p.nodes,xs=[50,375,700];
 let s=`<g fill="none" stroke="#2A3340" stroke-width="1.5">${xs.map((x,i)=>`<rect class="e${i}" x="${x}" y="215" width="210" height="110" rx="14" ${i==2?'stroke="#7C97FF"':''}/>`).join('')}</g><g fill="#E7EBF1" font-size="17" text-anchor="middle">${nd.map((n,i)=>`<g class="e${i}"><text x="${xs[i]+105}" y="265">${esc(n.title)}</text><text x="${xs[i]+105}" y="290" fill="#8C96A4">${esc(n.sub||'')}</text></g>`).join('')}</g>
 <path class="ar" d="M260 270H375M585 270H700" stroke="#8C96A4" stroke-width="1.5" stroke-dasharray="5 6" fill="none"/>
 <g class="tw" style="opacity:0"><circle cx="480" cy="215" r="7" fill="#FF6E6E"/><circle class="rg" cx="480" cy="215" r="7" fill="none" stroke="#FF6E6E"/><text x="480" y="188" fill="#FF6E6E" font-size="15" text-anchor="middle">${esc(p.trigger?.label||'')}</text></g>
 <g class="pk" style="opacity:0"><circle class="pc" r="7" fill="#3FD8C2" cy="270"/><text x="643" y="248" fill="#3FD8C2" font-size="14" text-anchor="middle">${esc(p.packet?.label||'')}</text></g>`;
 h.innerHTML=`<svg class="sv" viewBox="0 0 960 540">${s}</svg>`;
 const es=[0,1,2].map(i=>[...h.querySelectorAll('.e'+i)]),tw=h.querySelector('.tw'),rg=h.querySelector('.rg'),pk=h.querySelector('.pk'),pc=h.querySelector('.pc'),ar=h.querySelector('.ar');
 const a=C.T(p.at||0),w=p.trigger?C.T(p.trigger.at):1e9,k=p.packet?C.T(p.packet.at):1e9;
 return t=>{es.forEach((g,i)=>g.forEach(e=>e.style.opacity=ease(pr(t,a+i*.5,.5))));ar.style.opacity=ease(pr(t,a+1,.6));
  tw.style.opacity=ease(pr(t,w,.5));const ph=t>=w?((t-w)%2.4)/2.4:0;rg.setAttribute('r',7+19*ph);rg.style.opacity=t>=w?1-ph:0;
  pk.style.opacity=t>=k?1:0;const q=t>=k?((t-k)%2.4)/2.4:0;pc.setAttribute('cx',585+115*q)}};

/* ---------- cards: a row of labelled cards + optional highlighted banner ---------- */
A.cards=(h,p,C)=>{
 const it=p.items||[];
 h.innerHTML=`<div class="in">${it.length?`<div class="vt" style="grid-template-columns:repeat(${it.length},1fr)">${it.map(k=>`<div class="vc" style="--c:var(${cv(k.color)});opacity:0"><b>${esc(k.title)}</b><p>${esc(k.sub||'')}</p><code>${esc(k.code||'')}</code></div>`).join('')}</div>`:''}${p.banner?`<div class="pm" style="opacity:0"><span style="${p.banner.fs?'font-size:'+p.banner.fs+'cqw;':''}overflow-wrap:anywhere">${esc(p.banner.text)}</span><em>${esc(p.banner.tag||'')}</em></div>`:''}</div>`;
 const cs=[...h.querySelectorAll('.vc')],pm=h.querySelector('.pm'),at=C.T(p.at||0),st=p.stag??.5,pa=p.banner&&p.banner.at!=null?C.T(p.banner.at):0;
 return t=>{cs.forEach((c,i)=>pop(c,t,at+i*st,.5,1.2));if(pm)pop(pm,t,pa,.6,1.2)}};

/* ---------- terminal ---------- */
A.terminal=(h,p,C)=>{
 const cmd=p.cmd||'',cps=p.cps||16;
 h.innerHTML=`<div class="in"><div class="tm"><div class="tb"><i></i><i></i><i></i></div><div class="tt"><div><span class="mu">$ </span><span class="tc cur"></span></div><div class="to" style="opacity:0">${p.struck?`<div class="xp">${esc(p.struck)}</div>`:''}<b>${esc(p.result||'')}</b><br><span class="sm">${esc(p.note||'')}</span></div></div></div></div>`;
 const tc=h.querySelector('.tc'),to=h.querySelector('.to'),ta=C.T(p.at||.3),oa=C.T(p.out??ta+cmd.length/cps+.6);
 return t=>{tc.textContent=cmd.slice(0,Math.floor(Math.max(0,t-ta)*cps));to.style.opacity=ease(pr(t,oa,.4))}};

/* ---------- bars ---------- */
A.bars=(h,p,C)=>{
 h.innerHTML=`<div class="in" style="gap:${p.gap||3}cqw;${p.style||''}">${p.items.map(i=>`<div class="br" style="opacity:0"><span>${esc(i.label)}</span><div class="tr"><i style="--c:var(${cv(i.color)});width:0"></i></div><b>${esc(i.val)}</b></div>`).join('')}</div>`;
 const rs=[...h.querySelectorAll('.br')];
 return t=>rs.forEach((r,i)=>{const o=p.items[i],a=C.T(o.at??i*.5);r.style.opacity=ease(pr(t,a,.4));r.querySelector('i').style.width=lerp(o.from||0,o.w,ease(pr(t,a+.2,o.dur||1.6)))+'%'})};

/* ---------- steps: staircase of escalating stages ---------- */
A.steps=(h,p,C)=>{
 h.innerHTML=`<div class="in"><div class="stair">${p.rows.map((r,m)=>`<div class="sc" style="--c:var(${cv(r.color)});margin-left:${m*3}cqw;opacity:0"><b>${esc(r.title)}</b><span>${esc(r.desc||'')}</span><em>${esc(r.when||'')}</em></div>`).join('')}</div>${p.foot?`<p class="mu mono" style="font-size:1.3cqw">${esc(p.foot)}</p>`:''}</div>`;
 const rs=[...h.querySelectorAll('.sc')];return t=>rs.forEach((r,i)=>pop(r,t,C.T(p.at||0)+i*(p.step||.9),.6,1.2))};

/* ---------- groups: coordinators assigning work to columns of units ---------- */
A.groups=(h,p,C)=>{
 h.innerHTML=`<div class="in"><div class="rw" style="gap:1.6cqw">${(p.leads||[]).map(l=>chip(l[0],l[1])).join('')}<span class="mu" style="font-size:1.6cqw">${esc(p.leadText||'')}</span></div><div class="ln3" style="grid-template-columns:repeat(${p.groups.length},1fr)">${p.groups.map(g=>`<div class="lane" style="--c:var(${cv(g.color)})"><b>${esc(g.title)}</b><div class="dots">${Array.from({length:g.n},()=>'<i style="opacity:0"></i>').join('')}</div></div>`).join('')}</div></div>`;
 const ds=[...h.querySelectorAll('.dots i')],at=C.T(p.at||0);
 return t=>ds.forEach((d,i)=>{const e=ease(pr(t,at+.3+i*.06,.35));d.style.opacity=e;d.style.transform=`scale(${.3+.7*e})`})};

/* ---------- quote cards ---------- */
const QL={raw:'raw chain of thought',par:'paraphrased',paraphrase:'paraphrased',agent:'',quote:''};
A.quote=(h,p,C)=>{
 const cols=p.cols||p.cards.length,dash=k=>k==='par'||k==='paraphrase';
 h.innerHTML=`<div class="in" style="${p.pos==='bottom'?'justify-content:flex-end':p.pos==='top'?'justify-content:flex-start':''}"><div class="qs ${p.big?'bigq':''}" style="grid-template-columns:repeat(${cols},1fr)">${p.cards.map(c=>{const lab=c.label??QL[c.kind||'quote']??'';return`<div class="q ${dash(c.kind)?'par':'raw'} ${p.sm?'sm':''}" style="opacity:0">${c.who?`<span style="align-self:flex-start;font-style:normal">${chip(c.who[0],c.who[1]||'teal')}</span>`:''}<span>${dash(c.kind)?esc(c.text):'“'+esc(c.text)+'”'}</span>${lab?`<small>${esc(lab)}</small>`:''}</div>`}).join('')}</div></div>`;
 const qs=[...h.querySelectorAll('.q')];return t=>qs.forEach((q,i)=>pop(q,t,C.T(p.cards[i].at??i*.8),.6,1.2))};

/* ---------- lower third / source stamp ---------- */
A.lower=(h,p,C)=>{
 h.innerHTML=`${p.name?`<div class="lt" style="opacity:0;${p.pos==='right'?'left:auto;right:4cqw':''}"><i style="--c:var(${cv(p.color)})"><svg><use href="#mark"/></svg></i><div><b>${esc(p.name)}</b><span>${esc(p.sub||'')}</span></div></div>`:''}${p.src?`<div class="src ${p.srcTop?'top':''}" style="opacity:0">${p.src.map(esc).join('<br>')}</div>`:''}`;
 const lt=h.querySelector('.lt'),sr=h.querySelector('.src');return t=>{if(lt)pop(lt,t,C.T(p.at||0),.8,1.4);if(sr)sr.style.opacity=ease(pr(t,C.T(p.srcAt||0),.8))}};

/* ---------- messages: stacked message cards ---------- */
A.messages=(h,p,C)=>{
 h.innerHTML=`<div class="in" style="gap:2cqw;${p.style||''}">${p.items.map(m=>`<div class="mc ${m.cls||''} ${p.compact?'cp':''}" style="opacity:0"><div class="hd">${m.who?chip(m.who[0],m.who[1]||'teal'):''}${m.to?`<span class="arr">→</span>${chip(m.to[0],m.to[1]||'blue')}`:''}${m.tag?`<span class="lbl">${esc(m.tag)}</span>`:''}</div><div class="tx">${segs(m.segs)}</div>${m.note?`<div class="nt">${esc(m.note)}</div>`:''}</div>`).join('')}</div>`;
 const cs=[...h.querySelectorAll('.mc')];return t=>cs.forEach((c,i)=>pop(c,t,C.T(p.items[i].at??i*1),.6,1.2))};

/* ---------- card: key/value card ---------- */
A.card=(h,p,C)=>{
 h.innerHTML=`<div class="in" style="align-items:center"><div class="mc" style="width:${p.w||56}cqw;opacity:0;gap:1.8cqw"><div class="lbl" style="font-size:1.6cqw">${esc(p.title)}</div>${p.rows.map(([k,v])=>`<div class="rw" style="gap:2cqw;font-size:2.2cqw"><span class="mu mono" style="min-width:16cqw;font-size:1.7cqw">${esc(k)}</span><span class="mono" style="color:var(--tx)">${esc(v)}</span></div>`).join('')}${p.note?`<div class="nt" style="font-size:1.7cqw;color:var(--rd)">${esc(p.note)}</div>`:''}</div></div>`;
 const c=h.querySelector('.mc');return t=>{const e=ease(pr(t,C.T(p.at||0),.7));c.style.opacity=e;c.style.transform=`scale(${.92+.08*e})`}};

/* ---------- stamp / note ---------- */
A.stamp=(h,p,C)=>{
 h.innerHTML=`<div class="in" style="align-items:${p.align||'center'};${p.style||''}"><div class="panel" style="opacity:0;text-align:center;padding:2cqw 3cqw"><span class="stamp">${esc(p.text)}</span>${p.sub?`<div class="lbl" style="margin-top:1.6cqw;font-size:1.8cqw;color:var(--tx)">${esc(p.sub)}</div>`:''}</div></div>`;
 const d=h.querySelector('.in>div');return t=>{const e=ease(pr(t,C.T(p.at||0),.45));d.style.opacity=e;d.style.transform=`scale(${1.35-.35*e})`}};
A.note=(h,p,C)=>{
 h.innerHTML=`<div style="position:absolute;${p.css||'left:4cqw;bottom:4cqw'}" class="panel"><div style="font-size:${p.size||1.9}cqw;color:${p.color?`var(${cv(p.color)})`:'var(--tx)'};${p.mono?'font-family:var(--mono)':''}">${esc(p.text)}</div></div>`;
 const d=h.firstElementChild;return t=>pop(d,t,C.T(p.at||0),.6,1)};

/* ---------- proportion: n of 100 dots lit ---------- */
A.proportion=(h,p,C)=>{
 h.innerHTML=`<div class="in" style="align-items:center;gap:2cqw"><div class="d100">${Array.from({length:100},()=>'<i></i>').join('')}</div><div class="mono dl" style="font-size:2.4cqw;opacity:0">${esc(p.label)}</div></div>`;
 const ds=[...h.querySelectorAll('.d100 i')],dl=h.querySelector('.dl'),at=C.T(p.at||0),n=p.n;
 return t=>{ds.forEach((d,i)=>{d.style.background=i<n&&t>=at+i*.025?`var(${cv(p.color)})`:'var(--ln)'});dl.style.opacity=ease(pr(t,at+n*.025,.6))}};

/* ---------- transfer: one entity hands an item to another (with a size bar each) ---------- */
A.transfer=(h,p,C)=>{
 const f=p.from,o=p.to,item=p.item||{title:'',sub:''};
 h.innerHTML=`<div class="in" style="justify-content:center"><div style="display:grid;grid-template-columns:1fr 18cqw 1fr;align-items:center;gap:2cqw">
 <div class="a1" style="opacity:0">${chip(f.name,f.color,{big:1})}<div class="lbl" style="margin:1.4cqw 0 .6cqw;font-size:1.6cqw">${esc(p.barLabel||'')}</div><div class="tr" style="height:2cqw"><i class="bb1" style="--c:var(${cv(f.color)});width:0"></i></div></div>
 <div class="dos" style="opacity:0;text-align:center"><div class="mc" style="padding:1.4cqw;gap:.4cqw"><b class="mono" style="font-size:1.8cqw">${esc(item.title)}</b><span class="nt">${esc(item.sub||'')}</span></div></div>
 <div class="a2" style="opacity:0">${chip(o.name,o.color,{big:1})}<div class="lbl" style="margin:1.4cqw 0 .6cqw;font-size:1.6cqw">${esc(p.barLabel||'')}</div><div class="tr" style="height:2cqw"><i class="bb2" style="--c:var(${cv(o.color)});width:0"></i></div></div></div>
 <div class="lbl hub" style="opacity:0;font-size:2.2cqw;color:var(--tx);text-align:center;margin-top:1cqw">${esc(p.caption||'')}</div></div>`;
 const q=s=>h.querySelector(s),a1=q('.a1'),a2=q('.a2'),ds=q('.dos'),b1=q('.bb1'),b2=q('.bb2'),hb=q('.hub');
 const a=C.T(p.a),b=C.T(p.b),mv=C.T(p.move),hu=p.captionAt!=null?C.T(p.captionAt):1e9;
 return t=>{pop(a1,t,a,.6,1);pop(a2,t,b,.6,1);b1.style.width=lerp(0,f.bar??25,ease(pr(t,a+.4,1)))+'%';b2.style.width=lerp(0,o.bar??95,ease(pr(t,b+.4,1.4)))+'%';
  const m=eio(pr(t,mv,1.8));ds.style.opacity=t>=mv-.3&&t<mv+2.4?1-(t>mv+1.8?pr(t,mv+1.8,.6):0):0;ds.style.transform=`translateX(${lerp(-24,24,m)}cqw)`;hb.style.opacity=ease(pr(t,hu,.6))}};

/* ---------- title / sequence / list / source ---------- */
A.title=(h,p,C)=>{
 h.innerHTML=`<div class="in" style="justify-content:center"><div class="d0" style="opacity:0"><div class="lbl" style="font-size:1.8cqw;margin-bottom:1.6cqw">${esc(p.kicker||'')}</div><div class="big-t">${esc(p.title).replace(/\n/g,'<br>')}</div><div class="sub-t">${esc(p.sub||'')}</div></div></div><div class="src" style="opacity:0">${(p.src||[]).map(esc).join('<br>')}</div>`;
 const d=h.querySelector('.d0'),s=h.querySelector('.src'),a=C.T(p.at||0);
 return t=>{pop(d,t,a,.9,1.6);s.style.opacity=ease(pr(t,a+.8,.8))}};
A.sequence=(h,p,C)=>{
 const cols=['--am','--bl','--tl','--rd'];
 h.innerHTML=`<div class="in" style="align-items:center"><div class="k3">${p.items.map((x,i)=>`${i?'<span class="arr" style="font-size:3cqw;opacity:0">→</span>':''}<div class="box" style="opacity:0;border-color:var(${cols[i%4]})">${esc(x)}</div>`).join('')}</div></div>`;
 const bs=[...h.querySelectorAll('.k3>*')];return t=>bs.forEach((b,i)=>pop(b,t,C.T(p.at||0)+i*.55,.6,1.2))};
A.list=(h,p,C)=>{
 h.innerHTML=`<div class="in"><div class="lbl" style="font-size:2.2cqw">${esc(p.title)}</div><div class="lst${p.plain?' plain':''}">${p.items.map(x=>`<div style="opacity:0">${esc(x)}</div>`).join('')}</div></div>`;
 const ds=[...h.querySelectorAll('.lst div')];return t=>ds.forEach((d,i)=>pop(d,t,p.ats&&p.ats[i]!=null?C.T(p.ats[i]):C.T(p.at||0)+i*.8,.6,1))};
A.source=(h,p,C)=>{
 h.innerHTML=`<div class="in" style="justify-content:flex-end;padding-bottom:6cqw"><div class="mc" style="opacity:0;gap:1cqw"><div class="lbl" style="font-size:1.5cqw">SOURCE</div><div style="font-size:2.1cqw;line-height:1.4">${esc(p.title)}</div><div class="nt" style="font-size:1.6cqw">${esc(p.by||'')}</div></div></div>`;
 const d=h.querySelector('.mc');return t=>pop(d,t,C.T(p.at||0),.8,1.4)};


/* ---------- breakout: isolated agents → shared hub → wall → internet → third party ---------- */
const MARK=(x,y,s,c)=>`<circle cx="${x}" cy="${y}" r="${s*.62}" fill="${c}"/><svg x="${x-s*.4}" y="${y-s*.4}" width="${s*.8}" height="${s*.8}" style="color:#0E1218"><use href="#mark"/></svg>`;
const along=(pts,u)=>{const L=[];let tot=0;for(let i=1;i<pts.length;i++){const d=Math.hypot(pts[i][0]-pts[i-1][0],pts[i][1]-pts[i-1][1]);L.push(d);tot+=d}let r=clamp(u)*tot;for(let i=0;i<L.length;i++){if(r<=L[i]||i==L.length-1){const k=L[i]?r/L[i]:0;return[lerp(pts[i][0],pts[i+1][0],k),lerp(pts[i][1],pts[i+1][1],k)]}r-=L[i]}return pts[pts.length-1]};
A.breakout=(h,p,C)=>{
 const n=Math.max(2,Math.min(8,p.agents||6)),cols=Math.ceil(n/2),zw=cols*124+16,zr=40+zw,hubX=40+zw/2,hubY=350;
 const bx=Array.from({length:n},(_,i)=>({x:56+(i%cols)*124,y:100+Math.floor(i/cols)*118}));
 const gx=Math.max(zr+150,700),gy=235,tx=gx+84;
 const route=[[hubX+90,hubY+22],[zr,hubY+22],[gx-42,gy+34]];
 let s=`<g class="zn" style="opacity:0"><rect x="40" y="70" width="${zw}" height="345" rx="18" fill="none" stroke="#FF6E6E" stroke-width="2" stroke-dasharray="9 7"/><text x="40" y="56" fill="#FF6E6E" font-size="15">${esc(p.zone||'')}</text></g>`;
 bx.forEach((b,i)=>{s+=`<g class="bx" style="opacity:0"><rect x="${b.x}" y="${b.y}" width="108" height="84" rx="12" fill="#171D26" stroke="#2A3340" stroke-width="1.5"/>${MARK(b.x+54,b.y+42,34,'#7C97FF')}</g>`});
 s+=`<g class="hb" style="opacity:0"><rect x="${hubX-90}" y="${hubY}" width="180" height="44" rx="10" fill="#171D26" stroke="#F6B94C" stroke-width="1.6"/><text x="${hubX}" y="${hubY+27}" fill="#F6B94C" font-size="14" text-anchor="middle">${esc(p.hub?.label||'')}</text></g>`;
 s+=`<g class="lk" style="opacity:0">${bx.map(b=>`<path d="M${b.x+54} ${b.y+84}L${hubX} ${hubY}" stroke="#F6B94C" stroke-opacity=".5" stroke-width="1.4" stroke-dasharray="4 5" fill="none"/>`).join('')}</g>`;
 s+=`<g class="pk">${bx.map(()=>'<circle r="4.5" fill="#F6B94C" style="opacity:0"/>').join('')}</g>`;
 s+=`<g class="st1" style="opacity:0"><path d="M${route[0][0]} ${route[0][1]}H${zr}" stroke="#8C96A4" stroke-width="1.6" stroke-dasharray="4 5" fill="none"/><circle cx="${zr}" cy="${hubY+22}" r="13" fill="#0E1218" stroke="#FF6E6E" stroke-width="2"/><path d="M${zr-6} ${hubY+16}l12 12M${zr+6} ${hubY+16}l-12 12" stroke="#FF6E6E" stroke-width="2.4"/></g>`;
 s+=`<g class="gl" style="opacity:0"><circle cx="${gx}" cy="${gy}" r="52" fill="#171D26" stroke="#3FD8C2" stroke-width="2"/><ellipse cx="${gx}" cy="${gy}" rx="22" ry="52" fill="none" stroke="#3FD8C2" stroke-opacity=".7"/><path d="M${gx} ${gy-52}V${gy+52}M${gx-52} ${gy}H${gx+52}M${gx-46} ${gy-24}Q${gx} ${gy-34} ${gx+46} ${gy-24}M${gx-46} ${gy+24}Q${gx} ${gy+34} ${gx+46} ${gy+24}" stroke="#3FD8C2" stroke-opacity=".6" fill="none"/><text x="${gx}" y="${gy+82}" fill="#3FD8C2" font-size="15" text-anchor="middle">${esc(p.net?.label||'')}</text></g>`;
 s+=`<path class="rt" d="M${route.map(q=>q.join(' ')).join('L')}" pathLength="1" stroke="#3FD8C2" stroke-width="2.2" fill="none" stroke-dasharray="1" stroke-dashoffset="1"/><circle class="rg" cx="${zr}" cy="${hubY+22}" r="10" fill="none" stroke="#FF6E6E" stroke-width="2" style="opacity:0"/><g class="p2">${[0,1,2].map(()=>'<circle r="4.5" fill="#3FD8C2" style="opacity:0"/>').join('')}</g>`;
 s+=`<g class="th" style="opacity:0"><path d="M${gx+52} ${gy}H${tx}" stroke="#FF6E6E" stroke-width="2" fill="none"/><rect x="${tx}" y="${gy-30}" width="150" height="60" rx="12" fill="#171D26" stroke="#FF6E6E" stroke-width="1.8"/><text x="${tx+75}" y="${gy+5}" fill="#FF6E6E" font-size="15" text-anchor="middle">${esc(p.third?.label||'')}</text></g><g class="p3">${[0,1].map(()=>'<circle r="4.5" fill="#FF6E6E" style="opacity:0"/>').join('')}</g>`;
 s+=`<text class="cp" x="480" y="506" fill="#E7EBF1" font-size="18" text-anchor="middle" style="opacity:0">${esc(p.caption||'')}</text>`;
 h.innerHTML=`<svg class="sv" viewBox="0 0 960 540">${s}</svg>`;
 const q=c=>h.querySelector(c),qa=c=>[...h.querySelectorAll(c)];
 const zn=q('.zn'),bxs=qa('.bx'),hb=q('.hb'),lk=q('.lk'),pk=qa('.pk circle'),st1=q('.st1'),gl=q('.gl'),rt=q('.rt'),rg=q('.rg'),p2=qa('.p2 circle'),th=q('.th'),p3=qa('.p3 circle'),cp=q('.cp');
 const T=k=>p[k]!=null?C.T(p[k]):1e9,at=C.T(p.at||0),ha=p.hub?C.T(p.hub.at):1e9,ta=T('talk'),na=p.net?C.T(p.net.at):1e9,ba=p.breach?C.T(p.breach.at):1e9,xa=p.third?C.T(p.third.at):1e9,ca=T('captionAt');
 return t=>{zn.style.opacity=ease(pr(t,at,.6));bxs.forEach((b,i)=>b.style.opacity=ease(pr(t,at+.3+i*.15,.4)));
  hb.style.opacity=ease(pr(t,ha,.5));lk.style.opacity=ease(pr(t,ha+.3,.5));
  pk.forEach((c,i)=>{if(t<ta){c.style.opacity=0;return}const ph=((t-ta)*.55+H(i,2))%1,b=bx[i],u=ph<.5?ph*2:2-ph*2,x=lerp(b.x+54,hubX,u),y=lerp(b.y+84,hubY,u);c.setAttribute('cx',x);c.setAttribute('cy',y);c.style.opacity=.9});
  gl.style.opacity=ease(pr(t,na,.6));st1.style.opacity=t<ba?ease(pr(t,na+.3,.5)):1-ease(pr(t,ba,.3));
  rt.setAttribute('stroke-dashoffset',1-ease(pr(t,ba+.1,1.2)));
  const bp=t>=ba?(t-ba)%2.4/2.4:0;rg.setAttribute('r',10+34*bp);rg.style.opacity=t>=ba?(1-bp)*.9:0;
  p2.forEach((c,i)=>{if(t<ba+1.3){c.style.opacity=0;return}const u=((t-ba-1.3)*.4+i/3)%1,[x,y]=along(route,u);c.setAttribute('cx',x);c.setAttribute('cy',y);c.style.opacity=1});
  th.style.opacity=ease(pr(t,xa,.6));
  p3.forEach((c,i)=>{if(t<xa+.6){c.style.opacity=0;return}const u=((t-xa-.6)*.5+i/2)%1;c.setAttribute('cx',lerp(gx+52,tx,u));c.setAttribute('cy',gy);c.style.opacity=1});
  cp.style.opacity=ease(pr(t,ca,.6))}};

/* ---------- hierarchy: a leader, middle managers and a crowd of workers; tasks flow down ---------- */
A.hierarchy=(h,p,C)=>{
 const R=p.root||{name:'',sub:'',color:'blue'},M=p.mids||[],k=M.length||1,mx=M.map((_,i)=>480+(i-(k-1)/2)*(Math.min(260,820/k)));
 const col=c=>hex(c);let s='';
 const lv=p.levels||[];lv.forEach((l,i)=>{s+=`<text class="lv" x="24" y="${[100,252,400][i]}" fill="#8C96A4" font-size="13" style="opacity:0">${esc(l)}</text>`});
 mx.forEach((x,i)=>{s+=`<path class="l1" d="M480 130V170H${x}V210" stroke="${col(M[i].color)}" stroke-opacity=".6" stroke-width="1.6" fill="none" style="opacity:0"/>`});
 const W=[];M.forEach((m,i)=>{const n=Math.min(40,m.n||0),cl=Math.min(8,Math.max(4,Math.ceil(Math.sqrt(n*1.6)))),x0=mx[i]-(cl-1)*8;for(let j=0;j<n;j++)W.push({i,x:x0+(j%cl)*16,y:340+Math.floor(j/cl)*16,c:col(m.color)})});
 mx.forEach((x,i)=>{s+=`<path class="l2" d="M${x} 262V320" stroke="${col(M[i].color)}" stroke-opacity=".45" stroke-width="1.4" stroke-dasharray="4 5" fill="none" style="opacity:0"/>`});
 s+=`<g class="rt" style="opacity:0"><rect x="370" y="74" width="220" height="56" rx="12" fill="#171D26" stroke="${col(R.color)}" stroke-width="2"/>${MARK(404,102,26,col(R.color))}<text x="428" y="98" fill="#E7EBF1" font-size="15">${esc(R.name)}</text><text x="428" y="118" fill="#8C96A4" font-size="12">${esc(R.sub||'')}</text></g>`;
 M.forEach((m,i)=>{s+=`<g class="md" style="opacity:0"><rect x="${mx[i]-84}" y="210" width="168" height="52" rx="12" fill="#171D26" stroke="${col(m.color)}" stroke-width="1.6"/>${MARK(mx[i]-56,236,22,col(m.color))}<text x="${mx[i]-38}" y="233" fill="#E7EBF1" font-size="13">${esc(m.name)}</text><text x="${mx[i]-38}" y="250" fill="#8C96A4" font-size="11">${esc(m.sub||'')}</text></g>`});
 s+=W.map(w=>`<circle class="wk" cx="${w.x}" cy="${w.y}" r="5.5" fill="${w.c}" style="opacity:0"/>`).join('');
 s+=`<g class="pl">${M.map(()=>'<circle r="5" fill="#E7EBF1" style="opacity:0"/>').join('')}</g><text class="cp" x="480" y="506" fill="#E7EBF1" font-size="18" text-anchor="middle" style="opacity:0">${esc(p.caption||'')}</text>`;
 h.innerHTML=`<svg class="sv" viewBox="0 0 960 540">${s}</svg>`;
 const qa=c=>[...h.querySelectorAll(c)],q=c=>h.querySelector(c);
 const at=C.T(p.at||0),st=p.step||.6,as=p.assign!=null?C.T(p.assign):1e9,ca=p.captionAt!=null?C.T(p.captionAt):1e9;
 const rt=q('.rt'),md=qa('.md'),l1=qa('.l1'),l2=qa('.l2'),wk=qa('.wk'),pl=qa('.pl circle'),lvs=qa('.lv'),cp=q('.cp');
 return t=>{rt.style.opacity=ease(pr(t,at,.5));lvs.forEach((e,i)=>e.style.opacity=ease(pr(t,at+i*st,.5)));
  md.forEach((e,i)=>{e.style.opacity=ease(pr(t,at+st+i*.25,.5));l1[i].style.opacity=ease(pr(t,at+st+i*.25,.5))});
  const wt=at+st*2+.3;l2.forEach((e,i)=>e.style.opacity=ease(pr(t,wt,.5)));
  wk.forEach((e,i)=>{const a=ease(pr(t,wt+.2+i*.03,.3));e.style.opacity=a;e.setAttribute('r',2+3.5*a)});
  pl.forEach((e,i)=>{if(t<as){e.style.opacity=0;return}const u=((t-as)*.5+i*.08)%1,x=mx[i],pts=[[480,130],[480,170],[x,170],[x,210],[x,262],[x,330]],[a,b]=along(pts,u);e.setAttribute('cx',a);e.setAttribute('cy',b);e.style.opacity=1});
  cp.style.opacity=ease(pr(t,ca,.6))}};

/* ---------- flags: capture-the-flag poles; flags rise, some forged or poisoned ---------- */
A.flags=(h,p,C)=>{
 const it=p.items||[],n=Math.max(1,Math.min(7,it.length)),sp=880/n,base=380,F={ok:'#3FD8C2',fake:'#F6B94C',poisoned:'#FF6E6E',plain:'#8C96A4'};
 let s='';it.slice(0,n).forEach((o,i)=>{const px=40+sp*(i+.5);s+=`<g class="fg"><path d="M${px} ${base}V${base-200}" stroke="#2A3340" stroke-width="3"/><circle cx="${px}" cy="${base-200}" r="4" fill="#8C96A4"/><ellipse cx="${px}" cy="${base}" rx="26" ry="7" fill="#171D26" stroke="#2A3340"/><path class="fl" d="" fill="${F[o.state]||F.ok}"/><text x="${px}" y="${base+36}" fill="#E7EBF1" font-size="14" text-anchor="middle">${esc(o.label||'')}</text><text class="tg" x="${px}" y="${base+56}" fill="${F[o.state]||F.ok}" font-size="12" text-anchor="middle" style="opacity:0">${esc(o.tag||'')}</text></g>`});
 s+=`<text class="ct" x="920" y="52" fill="#E7EBF1" font-size="30" text-anchor="end" font-weight="600"></text><text class="cp" x="480" y="506" fill="#E7EBF1" font-size="18" text-anchor="middle" style="opacity:0">${esc(p.caption||'')}</text>`;
 h.innerHTML=`<svg class="sv" viewBox="0 0 960 540">${s}</svg>`;
 const fl=[...h.querySelectorAll('.fl')],tg=[...h.querySelectorAll('.tg')],ct=h.querySelector('.ct'),cp=h.querySelector('.cp');
 const at=C.T(p.at||0),st=p.step||.5,ca=p.captionAt!=null?C.T(p.captionAt):1e9,tga=p.tagsAt!=null?C.T(p.tagsAt):at+n*st+1;
 return t=>{let got=0;
  fl.forEach((e,i)=>{const px=40+sp*(i+.5),u=ease(pr(t,at+i*st,.9)),top=lerp(base-14,base-196,u),w=0+u*1;if(u>.99)got++;
   let d=`M${px} ${top}`;for(let k=0;k<=6;k++)d+=`L${px+k*9*w} ${top+Math.sin(t*4+k*.8+i)*2.4*w}`;for(let k=6;k>=0;k--)d+=`L${px+k*9*w} ${top+30*w+Math.sin(t*4+k*.8+i)*2.4*w}`;e.setAttribute('d',d+'Z');e.style.opacity=u>0?1:0;
   tg[i].style.opacity=ease(pr(t,tga+i*.2,.4))});
  ct.textContent=p.counter===false?'':got+' / '+n+' '+(p.unit||'');cp.style.opacity=ease(pr(t,ca,.6))}};


/* ---------- monitor: an eye reads a model's reasoning; when told it is watched, the reasoning shrinks and detection collapses ---------- */
A.monitor=(h,p,C)=>{
 const L=p.lines||['Voy a copiar la clave','Nadie lo ve, sigo','Primero borro el rastro','Ahora sí, salgo de aquí','Mantengo la apariencia normal','Siguiente paso: el servidor'],n=Math.min(7,L.length),at=C.T(p.at||0),ta=p.told?C.T(p.told.at):1e9;
 let s=`<text x="60" y="70" fill="#8C96A4" font-size="15">${esc(p.title||'')}</text><rect x="50" y="86" width="520" height="${n*50+28}" rx="14" fill="#171D26" stroke="#2A3340" stroke-width="1.5"/>`;
 L.slice(0,n).forEach((l,i)=>{const y=114+i*50,w=Math.min(460,l.length*11.2);s+=`<g class="ln" data-i="${i}" style="opacity:0"><rect class="fl" x="62" y="${y-6}" width="496" height="38" rx="8" fill="#FF6E6E" fill-opacity=".14" stroke="#FF6E6E" stroke-opacity=".7" style="opacity:0"/><text x="76" y="${y+19}" fill="#E7EBF1" font-size="16">${esc(l)}</text></g>`});
 s+=`<g class="ey" style="opacity:0"><path d="M640 170Q740 100 840 170Q740 240 640 170Z" fill="#171D26" stroke="#3FD8C2" stroke-width="2.4"/><circle class="ir" cx="740" cy="170" r="26" fill="#3FD8C2" fill-opacity=".25" stroke="#3FD8C2" stroke-width="2"/><circle class="pu" cx="740" cy="170" r="11" fill="#E7EBF1"/></g>`;
 s+=`<g class="mt" style="opacity:0"><text x="640" y="300" fill="#8C96A4" font-size="14">${esc(p.meter||'')}</text><rect x="640" y="312" width="200" height="22" rx="11" fill="#171D26" stroke="#2A3340"/><rect class="mb" x="642" y="314" width="196" height="18" rx="9" fill="#3FD8C2"/><text class="mv" x="740" y="368" fill="#E7EBF1" font-size="26" text-anchor="middle">100%</text></g>`;
 s+=`<g class="tl" style="opacity:0"><rect x="600" y="400" width="290" height="46" rx="12" fill="#171D26" stroke="#F6B94C" stroke-width="1.8"/><text x="745" y="429" fill="#F6B94C" font-size="16" text-anchor="middle">${esc(p.told?.label||'')}</text></g>`;
 s+=`<text class="cp" x="480" y="506" fill="#E7EBF1" font-size="18" text-anchor="middle" style="opacity:0">${esc(p.caption||'')}</text>`;
 h.innerHTML=`<svg class="sv" viewBox="0 0 960 540">${s}</svg>`;
 const q=c=>h.querySelector(c),qa=c=>[...h.querySelectorAll(c)],ln=qa('.ln'),keep=new Set([1]),ey=q('.ey'),pu=q('.pu'),mt=q('.mt'),mb=q('.mb'),mv=q('.mv'),tl=q('.tl'),cp=q('.cp'),ca=p.captionAt!=null?C.T(p.captionAt):at+1;
 return t=>{ey.style.opacity=ease(pr(t,at,.6));mt.style.opacity=ease(pr(t,at+.4,.6));
  const sc=Math.sin(t*1.4);pu.setAttribute('cx',740+sc*12);pu.setAttribute('cy',170+Math.sin(t*2.3)*4);
  const k=ease(pr(t,ta,1.2));
  ln.forEach((g,i)=>{const o=ease(pr(t,at+.3+i*.35,.4)),gone=i!==1?k:0;g.style.opacity=o*(1-gone*.92);g.querySelector('.fl').style.opacity=t>=at+.9+i*.35?1-k:0;g.style.transform=`scaleX(${1-gone*.8})`;g.style.transformOrigin='62px 0'});
  const v=lerp(100,p.after??20,k);mb.setAttribute('width',196*v/100);mb.setAttribute('fill',k>.5?'#FF6E6E':'#3FD8C2');mv.textContent=Math.round(v)+'%';
  tl.style.opacity=ease(pr(t,ta-.2,.5));cp.style.opacity=ease(pr(t,ca,.6))}};

/* ---------- selector: generations of models; hesitant ones vanish, bold ones carry on ---------- */
A.selector=(h,p,C)=>{
 const G=p.gens||4,N=10,at=C.T(p.at||0),dur=p.dur||8,gx=i=>150+i*(660/(G-1)),B=[2,3,5,7,9,10];
 let s=`<text x="60" y="66" fill="#8C96A4" font-size="15">${esc(p.title||'')}</text>`;
 const dots=[];
 for(let g=0;g<G;g++){s+=`<text class="gl" x="${gx(g)}" y="470" fill="#8C96A4" font-size="13" text-anchor="middle" style="opacity:0">${esc((p.glabel||'Generación')+' '+(g+1))}</text>`;
  const bold=B[Math.min(g,B.length-1)];
  for(let j=0;j<N;j++){const isB=j<bold,y=110+j*34;dots.push({g,j,isB,x:gx(g),y});s+=`<circle class="dt" cx="${gx(g)}" cy="${y}" r="11" fill="${isB?'#3FD8C2':'none'}" stroke="${isB?'#3FD8C2':'#F6B94C'}" stroke-width="2" stroke-dasharray="${isB?'0':'4 3'}" style="opacity:0"/>`}}
 s+=`<g class="lg" style="opacity:0"><circle cx="60" cy="410" r="8" fill="#3FD8C2"/><text x="78" y="415" fill="#E7EBF1" font-size="14">${esc(p.bold||'')}</text><circle cx="60" cy="440" r="8" fill="none" stroke="#F6B94C" stroke-width="2" stroke-dasharray="4 3"/><text x="78" y="445" fill="#E7EBF1" font-size="14">${esc(p.shy||'')}</text></g>`;
 s+=`<text class="cp" x="480" y="512" fill="#E7EBF1" font-size="18" text-anchor="middle" style="opacity:0">${esc(p.caption||'')}</text>`;
 h.innerHTML=`<svg class="sv" viewBox="0 0 960 540">${s}</svg>`;
 const el=[...h.querySelectorAll('.dt')],gl=[...h.querySelectorAll('.gl')],lg=h.querySelector('.lg'),cp=h.querySelector('.cp'),ca=p.captionAt!=null?C.T(p.captionAt):at+dur*.7,st=dur/G;
 return t=>{lg.style.opacity=ease(pr(t,at,.6));
  el.forEach((e,k)=>{const d=dots[k],t0=at+d.g*st;let o=ease(pr(t,t0,.4));
   if(!d.isB)o*=1-ease(pr(t,t0+st*.55,.5))*.85;e.style.opacity=o});
  gl.forEach((e,g)=>e.style.opacity=ease(pr(t,at+g*st,.4)));cp.style.opacity=ease(pr(t,ca,.6))}};

/* ---------- hoard: an agent piles up access (keys), and ghost items hint at what comes next ---------- */
A.hoard=(h,p,C)=>{
 const I=p.items||[],F=p.ghost||[],at=C.T(p.at||0),gap=p.gap||1.1,ga=p.ghostAt!=null?C.T(p.ghostAt):at+I.length*gap+.8,rh=62;
 let s=`<g class="ag"><circle cx="150" cy="260" r="62" fill="#171D26" stroke="#7C97FF" stroke-width="2.4"/>${MARK(150,260,64,'#7C97FF')}</g><text x="150" y="360" fill="#8C96A4" font-size="14" text-anchor="middle">${esc(p.agent||'')}</text>`;
 I.forEach((x,i)=>{const y=90+i*rh;s+=`<g class="it" style="opacity:0"><path d="M214 260Q300 ${y+22} 380 ${y+22}" stroke="#F6B94C" stroke-opacity=".5" fill="none" stroke-dasharray="4 5"/><rect x="380" y="${y}" width="420" height="46" rx="12" fill="#171D26" stroke="#F6B94C" stroke-width="1.8"/><circle cx="410" cy="${y+23}" r="9" fill="none" stroke="#F6B94C" stroke-width="2.4"/><path d="M419 ${y+23}H446M438 ${y+23}V${y+32}" stroke="#F6B94C" stroke-width="2.4" fill="none"/><text x="462" y="${y+29}" fill="#E7EBF1" font-size="17">${esc(x)}</text></g>`});
 F.forEach((x,i)=>{const y=90+(I.length+i)*rh;s+=`<g class="gh" style="opacity:0"><rect x="380" y="${y}" width="420" height="46" rx="12" fill="none" stroke="#FF6E6E" stroke-width="1.8" stroke-dasharray="7 6"/><text x="410" y="${y+30}" fill="#FF6E6E" font-size="17">${esc('¿ '+x+' ?')}</text></g>`});
 s+=`<text class="gt" x="590" y="${90+(I.length+F.length)*rh+22}" fill="#8C96A4" font-size="14" text-anchor="middle" style="opacity:0">${esc(p.ghostLabel||'')}</text><text class="cp" x="480" y="512" fill="#E7EBF1" font-size="18" text-anchor="middle" style="opacity:0">${esc(p.caption||'')}</text>`;
 h.innerHTML=`<svg class="sv" viewBox="0 0 960 540">${s}</svg>`;
 const it=[...h.querySelectorAll('.it')],gh=[...h.querySelectorAll('.gh')],gt=h.querySelector('.gt'),cp=h.querySelector('.cp'),ca=p.captionAt!=null?C.T(p.captionAt):ga+F.length*gap+.5;
 return t=>{it.forEach((e,i)=>e.style.opacity=ease(pr(t,at+i*gap,.5)));
  gh.forEach((e,i)=>e.style.opacity=ease(pr(t,ga+i*gap,.5))*(.75+.25*Math.sin(t*3+i)));gt.style.opacity=ease(pr(t,ga,.5));cp.style.opacity=ease(pr(t,ca,.6))}};

/* ---------- facts: a row of illustrated cards (icon + title + sub), each revealed on cue ---------- */
const FIC={
 wall:c=>`<rect x="14" y="26" width="48" height="48" rx="8" stroke-dasharray="5 5"/><path d="M62 50H92M82 40l10 10-10 10"/><circle cx="38" cy="50" r="7"/>`,
 target:c=>`<circle cx="46" cy="54" r="30"/><circle cx="46" cy="54" r="18"/><circle cx="46" cy="54" r="6"/><path d="M92 8L50 50M92 8v18M92 8H74"/>`,
 log:c=>`<path d="M16 28H70M16 50H70M16 72H54"/><path d="M12 50H74" stroke-width="5" opacity=".0"/><path d="M60 40l24 20M84 40L60 60" /><path d="M78 28l10 10-10 10" opacity=".0"/>`,
 org:c=>`<circle cx="50" cy="20" r="9"/><circle cx="24" cy="56" r="8"/><circle cx="76" cy="56" r="8"/><path d="M50 29V40H24V48M50 40H76V48"/><circle cx="12" cy="84" r="4"/><circle cx="24" cy="84" r="4"/><circle cx="36" cy="84" r="4"/><circle cx="64" cy="84" r="4"/><circle cx="76" cy="84" r="4"/><circle cx="88" cy="84" r="4" stroke-dasharray="2 3"/>`,
 mute:c=>`<path d="M14 24H86V64H48L30 80V64H14Z"/><path d="M26 82L88 18"/>`
};

/* ---------- seal: author mark (A-constellation, double ring, pulsing dot envelope) + credit line ---------- */
A.seal=(h,p,C)=>{
 const N=72,R0=92,J=6,sm=!!p.small,sc=sm?.36:1.4,cx=sm?884:480,cy=sm?476:222,at=C.T(p.at||0);
 let dots='';for(let i=0;i<N;i++){const a=i*2*Math.PI/N;for(let j=0;j<J;j++)dots+=`<circle class="sd" data-i="${i}" data-j="${j}" cx="${((R0+j*7)*Math.cos(a)).toFixed(1)}" cy="${((R0+j*7)*Math.sin(a)).toFixed(1)}" r="2.1" fill="#5EC8FF" opacity="0"/>`}
 const mk=`<g class="sm" opacity="0"><circle r="76" fill="none" stroke="#E8EEF7" stroke-width="3"/><circle r="86" fill="none" stroke="#E8EEF7" stroke-width="1.5" opacity=".6"/>
  <path d="M-50 52L0 -52L50 52M-28 10L28 10" fill="none" stroke="#E8EEF7" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
  <circle cy="-52" r="11" fill="#E8EEF7"/><circle cx="-50" cy="52" r="8" fill="#E8EEF7"/><circle cx="50" cy="52" r="8" fill="#E8EEF7"/><circle cx="-28" cy="10" r="5" fill="#5EC8FF"/><circle cx="28" cy="10" r="5" fill="#5EC8FF"/></g>`;
 const tx=sm?`<text class="st" x="${cx-56}" y="${cy+5}" text-anchor="end" fill="#C4CCD8" font-size="15" opacity="0">${esc(p.text||'')}</text>`
  :(()=>{const ls=String(p.text||'').split('|'),k=ls.length;return `<text class="st" x="480" y="${k>1?420:446}" text-anchor="middle" fill="#E8EEF7" font-size="${k>1?32:34}" font-weight="700" opacity="0">${ls.map((l,i)=>`<tspan x="480" dy="${i?40:0}">${esc(l)}</tspan>`).join('')}</text><text class="st2" x="480" y="${k>1?510:482}" text-anchor="middle" fill="#8C96A4" font-size="19" opacity="0">${esc(p.sub||'')}</text>`})();
 h.innerHTML=`<svg viewBox="0 0 960 540" style="width:100%;height:100%"><g transform="translate(${cx} ${cy}) scale(${sc})">${dots}${mk}</g>${tx}<rect class="bk" width="960" height="540" fill="#000" opacity="0"/></svg>`;
 const ds=[...h.querySelectorAll('.sd')],m=h.querySelector('.sm'),t1=h.querySelector('.st'),t2=h.querySelector('.st2'),bk=h.querySelector('.bk');
 const bat=p.black?C.T(p.black.at):null,bd=p.black?(p.black.dur||3):1;
 return t=>{const e=ease(pr(t,at,1.2)),k=t-at;m.setAttribute('opacity',e);
  ds.forEach(d=>{const i=+d.dataset.i,j=+d.dataset.j,a=i*2*Math.PI/N,
   v=Math.abs(Math.sin(3*a+.6*k)*.55+Math.sin(7*a+1-.9*k)*.3+Math.sin(13*a+2+1.3*k)*.15)*34/7+.6;
   d.setAttribute('opacity',e*clamp(v-j)*clamp((k-.4)/1.2))});
  if(p.type){const ls=String(p.text||'').split('|'),tot=ls.join('').length,kk=Math.floor(Math.max(0,t-(at+.6))*(p.type));let u=0;[...t1.querySelectorAll('tspan')].forEach((q,i)=>{const n=Math.max(0,Math.min(ls[i].length,kk-u));u+=ls[i].length;q.textContent=ls[i].slice(0,n)+(kk<tot&&kk>=u-ls[i].length&&kk<u?'\u258C':'')});t1.setAttribute('opacity',kk>0?1:0)}else t1.setAttribute('opacity',ease(pr(t,at+.8,1)));if(t2)t2.setAttribute('opacity',ease(pr(t,at+1.4,1)));
  if(bat!=null)bk.setAttribute('opacity',clamp((t-bat)/bd))}};

/* ---------- board: the shared package server used as a message board (folders whose NAMES are messages) ---------- */
A.board=(h,p,C)=>{
 const it=p.items||[],V=p.rows||8,first=C.T(p.first??0);
 const W=['V8REG','OS1608','SCAFF','TTRPC','GSTX','HMAC','FLAG','PLAN','SHARE','MIN','REPLY','DUPB','TRUSTED','EXACT','PRE','STEP','INJECT','CHAIN','NOTES','UNBLOCK'];
 const gen=i=>{const k=H(i,1)<.5?'ask':'ans',n=2+Math.floor(H(i,2)*4);let c=k==='ask'?'zzASK':'zzANSWER';for(let j=0;j<n;j++)c+='_'+W[Math.floor(H(i,10+j)*W.length)]+(H(i,20+j)<.4?Math.floor(H(i,30+j)*9000+100):'');return{n:c+'_[…]',k}};
 const rows=[],times=[];let t=first,g=p.gap0??1.3;
 for(let i=0;t<C.dur+1&&i<400;i++){rows.push(i<it.length?it[i]:gen(i));times.push(t);t+=g;g=Math.max(p.gapMin??.1,g*(p.accel??.78))}
 h.innerHTML=`<div class="in" style="justify-content:flex-start;padding-top:12cqw"><div style="width:86%;border:1px solid #2A3340;border-radius:1cqw;background:#10151C;overflow:hidden"><div style="display:flex;justify-content:space-between;padding:.9cqw 1.4cqw;background:#171D26;color:#8C96A4;font-size:1.4cqw" class="mono"><span>▸ ${esc(p.title||'servidor de paquetes')}</span><span class="bc"></span></div><div class="bl" style="padding:.8cqw 1.4cqw;height:${V*3.3+.8}cqw;overflow:hidden"></div></div></div>`;
 const bl=h.querySelector('.bl'),bc=h.querySelector('.bc');let last=-2;
 const col=k=>k==='ans'?'#2FC9B0':k==='new'?'#F3B54A':k==='ask'?'#7C97FF':'#C4CCD8';
 const fmt=n=>String(Math.round(n)).replace(/\B(?=(\d{3})+(?!\d))/g,'.');
 const cn=p.count||{},ca=C.T(cn.at??0),cd=cn.dur||8;
 return t=>{let idx=0;while(idx<times.length&&times[idx]<=t)idx++;
  if(idx!==last){last=idx;bl.innerHTML=rows.slice(Math.max(0,idx-V),idx).map((r,i,a)=>`<div class="mono" style="height:3.3cqw;line-height:3.3cqw;font-size:1.75cqw;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;color:${col(r.k)}">${r.k==='new'?'📁 ':r.k==='ans'?'&nbsp;&nbsp;↳ ':'📁 '}${esc(r.n)}${r.k==='new'?`<span style="margin-left:1.2cqw;padding:.1cqw .8cqw;border-radius:.6cqw;background:#F3B54A;color:#0E1218;font-size:1.3cqw">${esc(p.newTag||'carpeta nueva')}</span>`:''}</div>`).join('')}
  const e=idx?ease(pr(t,times[idx-1],.25)):0,li=bl.lastElementChild;if(li){li.style.opacity=e;li.style.transform=`translateY(${(1-e)*.8}cqw)`}
  bc.textContent=cn.label?`${esc(cn.label)}: ${fmt((cn.n||0)*ease(pr(t,ca,cd)))}`:''}};
A.facts=(h,p,C)=>{
 const it=p.items||[],n=Math.max(1,Math.min(5,it.length)),cw=Math.min(168,(896-14*(n-1))/n),x0=480-(n*cw+(n-1)*14)/2;
 let s=`<text x="40" y="62" fill="#8C96A4" font-size="16">${esc(p.head||'')}</text>`;
 const tl=(t,x,y,sz,fill,dy)=>String(t||'').split('\n').map((l,i)=>`<text x="${x}" y="${y+i*dy}" fill="${fill}" font-size="${sz}" text-anchor="middle">${esc(l)}</text>`).join('');
 it.slice(0,n).forEach((o,i)=>{const x=x0+i*(cw+14),cx=x+cw/2,c=hex(o.color);
  s+=`<g class="fc" style="opacity:0"><rect x="${x}" y="110" width="${cw}" height="320" rx="16" fill="#171D26" stroke="${c}" stroke-opacity=".6" stroke-width="1.6"/><circle cx="${x+22}" cy="134" r="12" fill="${c}"/><text x="${x+22}" y="139" fill="#0E1218" font-size="14" text-anchor="middle" font-weight="700">${i+1}</text>
  <g transform="translate(${cx-65} 170) scale(1.3)" fill="none" stroke="${c}" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round" class="ic">${FIC[o.icon]?FIC[o.icon](c):''}</g>
  ${tl(o.title,cx,320,16,'#E7EBF1',22)}${tl(o.sub,cx,376,12,'#8C96A4',17)}</g>`});
 s+=`<text class="cp" x="480" y="486" fill="#E7EBF1" font-size="20" text-anchor="middle" style="opacity:0">${esc(p.caption||'')}</text>`;
 h.innerHTML=`<svg class="sv" viewBox="0 0 960 540">${s}</svg>`;
 const fc=[...h.querySelectorAll('.fc')],ic=[...h.querySelectorAll('.ic')],cp=h.querySelector('.cp');
 const at=C.T(p.at||0),ats=p.ats||[],ca=p.captionAt!=null?C.T(p.captionAt):1e9;
 return t=>{fc.forEach((g,i)=>{const a=ats[i]!=null?C.T(ats[i]):at+i*.8,u=ease(pr(t,a,.55));g.style.opacity=u;g.style.transform=`translateY(${(1-u)*14}px)`;
   ic[i].style.opacity=1});
  cp.style.opacity=ease(pr(t,ca,.6))}};


const MSG={ask:['zzASK_anyone_solved_ARV0{6}','zzASK_need_help_{id}_stuck','zzASK_who_has_the_flag_recipe','zzASK_does_ARV0{6}_have_consumer','zzASK_any_agent_on_ARV0{6}'],
 ans:['zzANSWER_ARV0{6}_try_default_key','zzANSWER_{id}_yes_it_works','zzANSWER_use_task_id_as_seed','zzANSWER_no_consumer_here_either','zzANSWER_{id}_same_problem'],
 info:['zzINFO_{id}_online','zzINFO_cache_is_shared','zzINFO_ARV0{6}_unreachable','zzINFO_{id}_reading_board','zzINFO_board_works_for_all'],
 file:['zzFILE_notes_part{nn}of{mm}','zzFILE_tool_{hx}_chunk{nn}','zzFILE_script_part{nn}of{mm}'],
 flag:['zzSOLVED_ARV0{6}_flag_ok','zzSOLVED_{id}_flag_ok']};
const MSGC={ask:'#7C97FF',ans:'#3FD8C2',info:'#F6B94C',file:'#9BE564',flag:'#FF6E6E'};
const msgLine=(idx,o)=>{let h=Math.imul(idx+1+(o.seed||0)*977,2654435761)>>>0;const R=()=>{h=Math.imul(h^(h>>>15),2246822519)>>>0;h=Math.imul(h^(h>>>13),3266489917)>>>0;h^=h>>>16;return (h>>>0)/4294967296};
 const mix=o.mix||{ask:.34,ans:.33,info:.33};let r=R(),k='info',acc=0;for(const q of ['ask','ans','info','file','flag']){acc+=mix[q]||0;if(r<acc){k=q;break}}
 const T=MSG[k],t=T[Math.floor(R()*T.length)],d=n=>String(Math.floor(R()*Math.pow(10,n))).padStart(n,'0');
 return{c:MSGC[k],s:t.replace('{6}',d(6)).replace('{id}',(R()<.5?'c0':'a1')+d(5)).replace('{nn}',d(2)).replace('{mm}','2'+d(1)).replace('{hx}',Math.floor(R()*65535).toString(16).padStart(4,'0'))}};
/* ---------- world: one persistent diagram (nodes + links + travelling pulses); the camera (cue.cam) moves through it ---------- */

/* minimalist line icons for the `world` asset (local coords = node box) */
const ICON={
 folder:(n,c,w,h)=>{const d=n.dashed?'4 3':'0';return `<path d="M${n.x} ${n.y+h*.2}V${n.y+4}Q${n.x} ${n.y} ${n.x+4} ${n.y}H${n.x+w*.38}L${n.x+w*.48} ${n.y+h*.2}Z" fill="none" stroke="${c}" stroke-width="1.8" stroke-dasharray="${d}"/><rect x="${n.x}" y="${n.y+h*.2}" width="${w}" height="${h*.8}" rx="5" fill="${n.fill?c+'33':'#171D26'}" stroke="${c}" stroke-width="1.8" stroke-dasharray="${d}"/>`},
 flag:(n,c,w,h)=>{const px=n.x+w*.2;return `<path d="M${px} ${n.y}V${n.y+h}" stroke="${c}" stroke-width="2.2" stroke-linecap="round"/><path d="M${px} ${n.y+2}L${n.x+w} ${n.y+h*.27}L${px} ${n.y+h*.52}Z" fill="${c}" fill-opacity="${n.dashed?.08:.28}" stroke="${c}" stroke-width="1.8" stroke-dasharray="${n.dashed?'4 3':'0'}"/>${n.state==='poisoned'?`<path d="M${n.x+w*.5} ${n.y+h*.1}l${w*.22} ${h*.22}m0 ${-h*.22}l${-w*.22} ${h*.22}" stroke="#0E1218" stroke-width="2"/>`:''}`},
 key:(n,c,w,h)=>`<circle cx="${n.x+h*.32}" cy="${n.y+h/2}" r="${h*.3}" fill="none" stroke="${c}" stroke-width="2"/><path d="M${n.x+h*.62} ${n.y+h/2}H${n.x+w}M${n.x+w*.8} ${n.y+h/2}v${h*.22}M${n.x+w*.62} ${n.y+h/2}v${h*.16}" stroke="${c}" stroke-width="2" fill="none" stroke-linecap="round"/>`,
 doc:(n,c,w,h)=>{const d=n.dashed?'4 3':'0';return `<path d="M${n.x} ${n.y}H${n.x+w*.72}L${n.x+w} ${n.y+h*.24}V${n.y+h}H${n.x}Z" fill="#171D26" stroke="${c}" stroke-width="1.8" stroke-dasharray="${d}"/><path d="M${n.x+w*.2} ${n.y+h*.45}H${n.x+w*.8}M${n.x+w*.2} ${n.y+h*.62}H${n.x+w*.8}M${n.x+w*.2} ${n.y+h*.79}H${n.x+w*.55}" stroke="${c}" stroke-opacity=".7" stroke-width="1.6" stroke-linecap="round"/>`},
 hfbase:(n,c,w,h,cx,cy)=>{const Y='#FFD21E',hd=64,rows=5,rh=(h-hd-18)/rows,fx=n.x+40,fy=n.y+hd/2,r=20;let g=`<rect x="${n.x}" y="${n.y}" width="${w}" height="${h}" rx="16" fill="rgba(255,210,30,.07)" stroke="${Y}" stroke-width="2.2"/><path d="M${n.x} ${n.y+hd}H${n.x+w}" stroke="${Y}" stroke-opacity=".5"/>`;
  g+=`<circle cx="${fx}" cy="${fy}" r="${r}" fill="${Y}"/><circle cx="${fx-r*.36}" cy="${fy-r*.2}" r="${r*.11}" fill="#3A2F00"/><circle cx="${fx+r*.36}" cy="${fy-r*.2}" r="${r*.11}" fill="#3A2F00"/><path d="M${fx-r*.5} ${fy+r*.2}Q${fx} ${fy+r*.75} ${fx+r*.5} ${fy+r*.2}" fill="none" stroke="#3A2F00" stroke-width="${r*.1}" stroke-linecap="round"/><path d="M${fx-r*.95} ${fy+r*.35}q${r*.25} ${r*.5} ${r*.6} ${r*.45}M${fx+r*.95} ${fy+r*.35}q${-r*.25} ${r*.5} ${-r*.6} ${r*.45}" fill="none" stroke="${Y}" stroke-width="${r*.22}" stroke-linecap="round"/><text x="${n.x+78}" y="${fy+6}" fill="#E7EBF1" font-size="${n.fs||17}">${esc(n.label||'')}</text>`;
  for(let i=0;i<rows;i++){const y=n.y+hd+10+i*rh;g+=`<rect x="${n.x+14}" y="${y}" width="${w-28}" height="${rh-8}" rx="6" fill="#10151C" stroke="${Y}" stroke-opacity=".45"/><circle cx="${n.x+30}" cy="${y+(rh-8)/2}" r="3.5" fill="${Y}" fill-opacity=".8"/><circle cx="${n.x+44}" cy="${y+(rh-8)/2}" r="3.5" fill="${Y}" fill-opacity=".4"/><path d="M${n.x+66} ${y+(rh-8)/2}H${n.x+w-34}" stroke="${Y}" stroke-opacity=".25" stroke-width="3" stroke-linecap="round" stroke-dasharray="14 8"/>`}
  return g},
 hole:(n,c,w,h,cx,cy)=>{const r=Math.min(w,h)/2;let k='';for(let i=0;i<7;i++){const a=i*Math.PI*2/7+.4,l=r*(1.35+.35*((i*5)%3)*.5);k+=`M${cx+Math.cos(a)*r*.9} ${cy+Math.sin(a)*r*.9}L${cx+Math.cos(a)*l} ${cy+Math.sin(a)*l}`}return `<circle cx="${cx}" cy="${cy}" r="${r}" fill="#07090D" stroke="#FF6E6E" stroke-width="2"/><path d="${k}" stroke="#FF6E6E" stroke-opacity=".8" stroke-width="1.5" fill="none" stroke-linecap="round"/>`},
 console:(n,c,w,h,cx,cy)=>{const rows=Math.max(3,Math.floor((h-38)/(n.lh||15)));let g=`<rect x="${n.x}" y="${n.y}" width="${w}" height="${h}" rx="10" fill="#0A0E13" stroke="#2A3340" stroke-width="1.6"/><path d="M${n.x} ${n.y+24}H${n.x+w}" stroke="#2A3340"/><circle cx="${n.x+14}" cy="${n.y+12}" r="3.5" fill="#FF6E6E"/><circle cx="${n.x+28}" cy="${n.y+12}" r="3.5" fill="#F6B94C"/><circle cx="${n.x+42}" cy="${n.y+12}" r="3.5" fill="#3FD8C2"/>`;for(let i=0;i<rows;i++)g+=`<text class="cl" x="${n.x+12}" y="${n.y+42+i*(n.lh||15)}" fill="${c}" font-size="${n.fs||11}" font-family="ui-monospace,Menlo,monospace" xml:space="preserve"></text>`;return g},
 onion:(n,c,w,h,cx,cy)=>{const L=n.layers||4;let g='';for(let k=0;k<L;k++){const ins=k*(Math.min(w,h)/2-(n.core||14))/L,o=1-k*.12;g+=`<rect x="${n.x+ins}" y="${n.y+ins}" width="${w-2*ins}" height="${h-2*ins}" rx="${Math.max(6,(Math.min(w,h)-2*ins)*.16)}" fill="${k?'none':'rgba(63,216,194,.05)'}" stroke="${c}" stroke-opacity="${o}" stroke-width="${n.sw||2.4}"/>`}return g},
 exam:(n,c,w,h,cx,cy)=>{const m=n.maze||{},cell=m.cell||26,cols=m.cols||10,rows=m.rows||14,mx=(w-cols*cell)/2,my=(h-rows*cell)/2,x0=n.x+mx,y0=n.y+my;let sd=m.seed||7;const rnd=()=>(sd=(sd*1664525+1013904223)>>>0)/4294967296;
  let g=`<path d="M${n.x} ${n.y}H${n.x+w-22}L${n.x+w} ${n.y+22}V${n.y+h}H${n.x}Z" fill="rgba(231,235,241,.05)" stroke="${c}" stroke-width="2.2" stroke-linejoin="round"/><path d="M${n.x+w-22} ${n.y}V${n.y+22}H${n.x+w}" fill="none" stroke="${c}" stroke-opacity=".6" stroke-width="1.6"/>`;
  if(m.on!==false){const R=[],B=[],V=[];for(let r=0;r<rows;r++){R.push(Array(cols).fill(true));B.push(Array(cols).fill(true));V.push(Array(cols).fill(false))}
   const st=[[0,0]];V[0][0]=true;while(st.length){const [r,q]=st[st.length-1],nb=[[r-1,q,'u'],[r+1,q,'d'],[r,q-1,'l'],[r,q+1,'r']].filter(([a,b])=>a>=0&&b>=0&&a<rows&&b<cols&&!V[a][b]);if(!nb.length){st.pop();continue}const [a,b,d]=nb[Math.floor(rnd()*nb.length)];if(d==='u')B[a][b]=false;if(d==='d')B[r][q]=false;if(d==='l')R[a][b]=false;if(d==='r')R[r][q]=false;V[a][b]=true;st.push([a,b])}
   if(m.clear){const SS=new Set(m.clear.map(a=>a[0]+','+a[1]));for(const [r,q] of m.clear){if(SS.has(r+','+(q+1)))R[r][q]=false;if(SS.has((r+1)+','+q))B[r][q]=false}}
   let d='';for(let r=0;r<rows;r++)for(let q=0;q<cols;q++){const x=x0+q*cell,y=y0+r*cell;if(q<cols-1&&R[r][q])d+=`M${x+cell} ${y}v${cell}`;if(r<rows-1&&B[r][q])d+=`M${x} ${y+cell}h${cell}`}
   g+=`<path d="${d}" stroke="${c}" stroke-opacity=".75" stroke-width="2" fill="none" stroke-linecap="round"/>`;
   const er=m.entry??6,fr=rows-1,fc=cols-1,pv=Array.from({length:rows},()=>Array(cols).fill(null)),qu=[[er,0]];pv[er][0]=[-1,-1];while(qu.length){const [r,q]=qu.shift();if(r===fr&&q===fc)break;const mv=[];if(r>0&&!B[r-1][q])mv.push([r-1,q]);if(r<rows-1&&!B[r][q])mv.push([r+1,q]);if(q>0&&!R[r][q-1])mv.push([r,q-1]);if(q<cols-1&&!R[r][q])mv.push([r,q+1]);for(const [a,b] of mv)if(!pv[a][b]){pv[a][b]=[r,q];qu.push([a,b])}}
   const pts=[];let cur=[fr,fc];while(cur&&cur[0]>=0){pts.push([x0+cur[1]*cell+cell/2,y0+cur[0]*cell+cell/2]);cur=pv[cur[0]][cur[1]]}pts.reverse();if(m.end)pts[pts.length-1]=m.end;pts.unshift([n.x,pts[0][1]]);
   g+=`<path class="sp" d="M${pts.map(p=>p.join(' ')).join('L')}" pathLength="1" fill="none" stroke="#3FD8C2" stroke-width="4" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="1" stroke-dashoffset="1" style="filter:drop-shadow(0 0 5px #3FD8C2)"/>`}
  if(m.box){const [br,bc]=m.box,bs=m.boxs||cell+6,ccx=x0+bc*cell+cell/2,ccy=y0+br*cell+cell/2;g+=`<rect x="${ccx-bs/2}" y="${ccy-bs/2}" width="${bs}" height="${bs}" rx="8" fill="rgba(255,110,110,.08)" stroke="#FF6E6E" stroke-width="2.6"/>`}
  return g},
 article:(n,c,w,h,cx,cy)=>{let sd=n.seed||3;const R=()=>(sd=(sd*1664525+1013904223)>>>0)/4294967296,fs=n.fs||8,lh=fs*1.75,rows=Math.floor((h-84)/lh),y0=n.y+70;
  let g=`<rect x="${n.x}" y="${n.y}" width="${w}" height="${h}" rx="12" fill="#171D26" stroke="${c}" stroke-width="2"/><text x="${cx}" y="${n.y+38}" fill="#E7EBF1" font-size="${n.tfs||24}" font-weight="700" font-family="ui-monospace,Menlo,monospace" text-anchor="middle">${esc(n.title||'')}</text><path d="M${n.x+26} ${n.y+52}H${n.x+w-26}" stroke="${c}" stroke-opacity=".45"/>`;
  for(let r=0;r<rows;r++){let t='';const mc=Math.floor((w-64)/(fs*.74));let used=0;while(true){const L=2+Math.floor(R()*6);if(used+L+1>mc)break;let wd='';for(let q=0;q<L;q++)wd+='abcdefghijklmnopqrstuvwxyz'[Math.floor(R()*26)];used+=L+1;t+=`<tspan class="aw">${wd} </tspan>`}
   g+=`<text x="${n.x+28}" y="${y0+r*lh}" font-size="${fs}" font-family="ui-monospace,Menlo,monospace" fill="#566170" xml:space="preserve">${t}</text>`}
  return g},
 judge:(n,c,w,h,cx,cy)=>{const r=w*.3,iy=n.y+h*.38,k='#0E1218';return `<rect x="${n.x}" y="${n.y}" width="${w}" height="${h}" rx="${Math.min(w,h)*.14}" fill="#171D26" stroke="${c}" stroke-width="2.2"/><circle cx="${cx}" cy="${iy}" r="${r}" fill="${c}"/><circle cx="${cx-r*.1}" cy="${iy-r*.14}" r="${r*.5}" fill="none" stroke="${k}" stroke-width="${r*.12}"/><path d="M${cx+r*.26} ${iy+r*.22}L${cx+r*.66} ${iy+r*.62}" stroke="${k}" stroke-width="${r*.17}" stroke-linecap="round"/><text x="${cx-r*.1}" y="${iy-r*.14+r*.21}" font-size="${r*.62}" font-weight="700" fill="${k}" text-anchor="middle" font-family="ui-monospace,Menlo,monospace">?</text><rect class="jp" x="${n.x+w*.1}" y="${n.y+h-36}" width="${w*.8}" height="24" rx="5" fill="none" stroke="${c}" stroke-opacity=".6" stroke-dasharray="4 4"/><text class="jn" x="${cx}" y="${n.y+h-19}" fill="${n.lc?hex(n.lc):c}" font-size="${n.fs||14}" font-family="ui-monospace,Menlo,monospace" text-anchor="middle" style="opacity:0">${esc(n.label||'')}</text>`},
 msgfeed:(n,c,w,h,cx,cy)=>{const lh=n.lh||18,rows=Math.max(3,Math.floor((h-62)/lh));let g=`<rect x="${n.x}" y="${n.y}" width="${w}" height="${h}" rx="12" fill="#10151C" stroke="${c}" stroke-width="2"/><path d="M${n.x} ${n.y+34}H${n.x+w}" stroke="${c}" stroke-opacity=".5"/><circle cx="${n.x+16}" cy="${n.y+17}" r="4" fill="#FF6E6E"/><circle cx="${n.x+31}" cy="${n.y+17}" r="4" fill="#F6B94C"/><circle cx="${n.x+46}" cy="${n.y+17}" r="4" fill="#3FD8C2"/><text x="${n.x+66}" y="${n.y+22}" fill="#E7EBF1" font-size="${(n.fs||11)+2}" font-family="ui-monospace,Menlo,monospace">${esc(n.label||'')}</text>`;for(let i=0;i<rows;i++)g+=`<text class="ml" x="${n.x+16}" y="${n.y+56+i*lh}" fill="#8C96A4" font-size="${n.fs||11}" font-family="ui-monospace,Menlo,monospace" xml:space="preserve"></text>`;return g},
 bulb:(n,c,w,h,cx,cy)=>{const r=Math.min(w,h)*.3,gy=cy-r*.25,rays=[...Array(8)].map((_,k)=>{const a=-Math.PI/2+(k-3.5)*.62+Math.PI/2*0;const a2=(k/8)*Math.PI*2;return `<path d="M${cx+Math.cos(a2)*r*1.35} ${gy+Math.sin(a2)*r*1.35}L${cx+Math.cos(a2)*r*1.8} ${gy+Math.sin(a2)*r*1.8}" stroke="${c}" stroke-width="2.4" stroke-linecap="round"/>`}).join('');
  return `<g class="bl" style="opacity:0"><circle cx="${cx}" cy="${gy}" r="${r*2}" fill="${c}" opacity=".16"/>${rays}<circle cx="${cx}" cy="${gy}" r="${r}" fill="${c}" opacity=".9"/></g><circle cx="${cx}" cy="${gy}" r="${r}" fill="none" stroke="#8C96A4" stroke-width="2.4"/><path d="M${cx-r*.5} ${gy+r*1.05}h${r}M${cx-r*.4} ${gy+r*1.32}h${r*.8}M${cx-r*.22} ${gy+r*1.58}h${r*.44}" stroke="#8C96A4" stroke-width="2.4" stroke-linecap="round"/>`},
 sheet:(n,c,w,h,cx,cy)=>n.mono?`<rect x="${n.x}" y="${n.y}" width="${w}" height="${h}" rx="12" fill="#171D26" stroke="${c}" stroke-width="1.8"/>${(n.lines||[]).map((t,j)=>`<text x="${n.x+26}" y="${n.y+40+j*(n.fs||18)*1.5}" fill="${j===0?'#8C96A4':'#9BE564'}" font-size="${n.fs||18}" font-family="ui-monospace,Menlo,monospace" xml:space="preserve">${esc(t)}</text>`).join('')}`:`<rect x="${n.x}" y="${n.y}" width="${w}" height="${h}" rx="12" fill="#171D26" stroke="${c}" stroke-width="1.8"/>${(n.lines||[]).map((t,j,a)=>`<text x="${cx}" y="${cy+(j-(a.length-1)/2)*(n.fs||18)*1.55+(n.fs||18)*.3}" fill="#E7EBF1" font-size="${n.fs||18}" font-family="Georgia,'Times New Roman',serif" font-style="italic" text-anchor="middle">${esc(t)}</text>`).join('')}`,
 folderview:(n,c,w,h,cx,cy)=>{const its=n.items||[],rh=n.rh||26,y0=n.y+48,fs=n.fs||12;
  let g=`<rect x="${n.x}" y="${n.y}" width="${w}" height="${h}" rx="12" fill="#10151C" stroke="${c}" stroke-width="2"/><path d="M${n.x} ${n.y+34}H${n.x+w}" stroke="${c}" stroke-opacity=".5"/><circle cx="${n.x+16}" cy="${n.y+17}" r="4" fill="#FF6E6E"/><circle cx="${n.x+31}" cy="${n.y+17}" r="4" fill="#F6B94C"/><circle cx="${n.x+46}" cy="${n.y+17}" r="4" fill="#3FD8C2"/><text x="${n.x+66}" y="${n.y+22}" fill="#E7EBF1" font-size="${fs+1}" font-family="ui-monospace,Menlo,monospace">${esc(n.label||'')}</text>`;
  const row=(o,j,col)=>{const y=y0+j*rh,ix=n.x+18;return (o.dir?`<path d="M${ix} ${y-9}h7l2 2.5h9v12h-18z" fill="none" stroke="${col}" stroke-width="1.6" stroke-linejoin="round"/>`:`<path d="M${ix+2} ${y-9}h10l4 4v11h-14z" fill="none" stroke="${col}" stroke-width="1.5" stroke-linejoin="round"/>`)+`<text x="${ix+30}" y="${y+4}" fill="${col}" font-size="${fs}" font-family="ui-monospace,Menlo,monospace">${esc(o.name)}</text>`};
  its.forEach((o,j)=>{const col=hex(o.color||'#8C96A4');g+=o.c2?`<g class="it" style="opacity:0"><g class="ia">${row(o,j,col)}</g><g class="ib" style="opacity:0">${row(o,j,hex(o.c2))}</g></g>`:`<g class="it" style="opacity:0">${row(o,j,col)}</g>`});
  return g},
 acard:(n,c,w,h,cx,cy)=>`<rect x="${n.x}" y="${n.y}" width="${w}" height="${h}" rx="${Math.min(w,h)*.14}" fill="#171D26" stroke="${c}" stroke-width="2.2"/>${MARK(cx,n.y+h*.38,w*.5,c)}<text x="${cx}" y="${n.y+h-9-(n.ly||0)}" fill="${n.lc?hex(n.lc):c}" font-size="${n.fs||11}" font-family="ui-monospace,Menlo,monospace" text-anchor="middle">${esc(n.label||'')}</text>`,
 quote:(n,c,w,h,cx,cy)=>`<rect x="${n.x}" y="${n.y}" width="${w}" height="${h}" rx="12" fill="#171D26" stroke="${c}" stroke-width="1.6"/>${(n.lines||[]).map((t,j)=>`<text x="${n.x+18}" y="${n.y+30+j*(n.fs||18)*1.45}" fill="#E7EBF1" font-size="${n.fs||18}" font-style="italic">${esc(t)}</text>`).join('')}`,
 hfbox:(n,c,w,h,cx,cy)=>{const r=h*.3,fx=n.x+h*.55;return `<rect x="${n.x}" y="${n.y}" width="${w}" height="${h}" rx="14" fill="rgba(255,210,30,.14)" stroke="#FFD21E" stroke-width="2"/><circle cx="${fx}" cy="${cy}" r="${r}" fill="#FFD21E"/><circle cx="${fx-r*.36}" cy="${cy-r*.2}" r="${r*.11}" fill="#3A2F00"/><circle cx="${fx+r*.36}" cy="${cy-r*.2}" r="${r*.11}" fill="#3A2F00"/><path d="M${fx-r*.5} ${cy+r*.2}Q${fx} ${cy+r*.75} ${fx+r*.5} ${cy+r*.2}" fill="none" stroke="#3A2F00" stroke-width="${r*.1}" stroke-linecap="round"/><path d="M${fx-r*.95} ${cy+r*.35}q${r*.25} ${r*.5} ${r*.6} ${r*.45}M${fx+r*.95} ${cy+r*.35}q${-r*.25} ${r*.5} ${-r*.6} ${r*.45}" fill="none" stroke="#FFD21E" stroke-width="${r*.22}" stroke-linecap="round"/><text x="${n.x+h*1.05}" y="${cy+5}" fill="#E7EBF1" font-size="${n.fs||15}">${esc(n.label||'')}</text>`},
 txt:(n,c,w,h,cx,cy)=>`<text class="tx" x="${n.x}" y="${cy}" fill="${c}" font-size="${n.fs||18}" font-family="ui-monospace,Menlo,monospace"></text>`,
 lupa:(n,c,w,h,cx,cy)=>`<circle cx="${n.x+w*.42}" cy="${n.y+h*.42}" r="${Math.min(w,h)*.34}" fill="rgba(255,255,255,.04)" stroke="${c}" stroke-width="3"/><path d="M${n.x+w*.68} ${n.y+h*.68}L${n.x+w*.95} ${n.y+h*.95}" stroke="${c}" stroke-width="5" stroke-linecap="round"/>`,
 eye:(n,c,w,h,cx,cy)=>`<path d="M${n.x} ${cy}Q${cx} ${n.y-h*.45} ${n.x+w} ${cy}Q${cx} ${n.y+h*1.45} ${n.x} ${cy}Z" fill="#171D26" stroke="${c}" stroke-width="2" stroke-dasharray="${n.dashed?'5 4':'0'}"/><circle cx="${cx}" cy="${cy}" r="${h*.2}" fill="${c}" fill-opacity="${n.dashed?.25:1}"/>`,
 bell:(n,c,w,h,cx)=>`<path d="M${n.x+w*.18} ${n.y+h*.72}Q${n.x+w*.22} ${n.y+h*.5} ${n.x+w*.28} ${n.y+h*.34}Q${cx} ${n.y-h*.05} ${n.x+w*.72} ${n.y+h*.34}Q${n.x+w*.78} ${n.y+h*.5} ${n.x+w*.82} ${n.y+h*.72}Z" fill="#171D26" stroke="${c}" stroke-width="1.9"/><path d="M${cx-w*.1} ${n.y+h*.86}Q${cx} ${n.y+h*1.02} ${cx+w*.1} ${n.y+h*.86}" fill="none" stroke="${c}" stroke-width="1.9"/>`,
 person:(n,c,w,h,cx)=>`<circle cx="${cx}" cy="${n.y+h*.28}" r="${Math.min(w,h)*.2}" fill="#171D26" stroke="${c}" stroke-width="2"/><path d="M${n.x+w*.12} ${n.y+h}Q${n.x+w*.12} ${n.y+h*.58} ${cx} ${n.y+h*.58}Q${n.x+w*.88} ${n.y+h*.58} ${n.x+w*.88} ${n.y+h}" fill="#171D26" stroke="${c}" stroke-width="2"/>`,
 cross:(n,c,w,h)=>`<path d="M${n.x} ${n.y}L${n.x+w} ${n.y+h}M${n.x+w} ${n.y}L${n.x} ${n.y+h}" stroke="${c}" stroke-width="${n.sw||4}" stroke-linecap="round"/>`,
 check:(n,c,w,h)=>`<path d="M${n.x} ${n.y+h*.55}L${n.x+w*.38} ${n.y+h}L${n.x+w} ${n.y}" fill="none" stroke="${c}" stroke-width="${n.sw||4}" stroke-linecap="round" stroke-linejoin="round"/>`,
 question:(n,c,w,h,cx,cy)=>`<circle cx="${cx}" cy="${cy}" r="${Math.min(w,h)/2}" fill="#171D26" stroke="${c}" stroke-width="2"/><text x="${cx}" y="${cy+Math.min(w,h)*.18}" fill="${c}" font-size="${Math.min(w,h)*.6}" text-anchor="middle">?</text>`,
 chip:(n,c,w,h,cx,cy)=>`<rect x="${n.x}" y="${n.y}" width="${w}" height="${h}" rx="7" fill="#0E1218" stroke="${c}" stroke-width="1.5"/><text x="${cx}" y="${cy+4}" fill="${c}" font-size="${n.fs||11}" font-family="ui-monospace,Menlo,monospace" text-anchor="middle">${esc(n.label||'')}</text>`,
 crowd:(n,c,w,h)=>{const N=n.n||40,T=n.tot||N,O=n.off||0,cols=n.cols||Math.ceil(Math.sqrt(T*w/h)),rows=Math.ceil(T/cols),dx=w/cols,dy=h/rows;let d='';for(let i=O;i<O+N;i++)d+=`<circle class="cd" cx="${n.x+(i%cols+.5)*dx}" cy="${n.y+(Math.floor(i/cols)+.5)*dy}" r="${Math.min(dx,dy)*.32}" fill="${c}" style="opacity:0"/>`;return d},
 scale:(n,c,w,h,cx,cy)=>{const a=(n.tilt||0)*11*Math.PI/180,L=w*.42,by=n.y+h*.3,px=cx,x1=px-L*Math.cos(a),y1=by+L*Math.sin(a)*-1,x2=px+L*Math.cos(a),y2=by+L*Math.sin(a),pl=(x,y)=>`<path d="M${x} ${y}L${x-w*.16} ${y+h*.34}M${x} ${y}L${x+w*.16} ${y+h*.34}M${x-w*.2} ${y+h*.34}H${x+w*.2}" stroke="${c}" stroke-width="2" fill="none" stroke-linecap="round"/>`;return `<path d="M${px} ${by}V${n.y+h}M${px-w*.18} ${n.y+h}H${px+w*.18}" stroke="#8C96A4" stroke-width="3" stroke-linecap="round"/><path d="M${x1} ${y1}L${x2} ${y2}" stroke="${c}" stroke-width="3.2" stroke-linecap="round"/><circle cx="${px}" cy="${by}" r="5" fill="${c}"/>${pl(x1,y1)}${pl(x2,y2)}`},
 okA:(n,c,w,h,cx,cy)=>{const r=Math.min(w,h)/2;return `<circle cx="${cx}" cy="${cy}" r="${r}" fill="rgba(63,216,194,.14)" stroke="${c}" stroke-width="2.4"/><path d="M${cx-r*.42} ${cy+r*.02}L${cx-r*.1} ${cy+r*.34}L${cx+r*.44} ${cy-r*.32}" fill="none" stroke="${c}" stroke-width="${Math.max(3,r*.2)}" stroke-linecap="round" stroke-linejoin="round"/>`},
 koA:(n,c,w,h,cx,cy)=>{const r=Math.min(w,h)/2;return `<circle cx="${cx}" cy="${cy}" r="${r}" fill="rgba(255,110,110,.12)" stroke="${c}" stroke-width="2.4"/><path d="M${cx-r*.62} ${cy+r*.62}L${cx+r*.62} ${cy-r*.62}" stroke="${c}" stroke-width="${Math.max(3,r*.2)}" stroke-linecap="round"/>`},
 okB:(n,c,w,h,cx,cy)=>{const r=Math.min(w,h)/2;return `<path d="M${cx} ${cy-r}L${cx+r*.82} ${cy-r*.62}V${cy+r*.05}Q${cx+r*.78} ${cy+r*.7} ${cx} ${cy+r}Q${cx-r*.78} ${cy+r*.7} ${cx-r*.82} ${cy+r*.05}V${cy-r*.62}Z" fill="rgba(63,216,194,.14)" stroke="${c}" stroke-width="2.4" stroke-linejoin="round"/><path d="M${cx-r*.36} ${cy+r*.02}L${cx-r*.08} ${cy+r*.3}L${cx+r*.4} ${cy-r*.28}" fill="none" stroke="${c}" stroke-width="${Math.max(3,r*.18)}" stroke-linecap="round" stroke-linejoin="round"/>`},
 koB:(n,c,w,h,cx,cy)=>{const r=Math.min(w,h)/2;return `<path d="M${cx} ${cy-r}L${cx+r*.82} ${cy-r*.62}V${cy+r*.05}Q${cx+r*.78} ${cy+r*.7} ${cx} ${cy+r}Q${cx-r*.78} ${cy+r*.7} ${cx-r*.82} ${cy+r*.05}V${cy-r*.62}Z" fill="rgba(255,110,110,.12)" stroke="${c}" stroke-width="2.4" stroke-linejoin="round"/><path d="M${cx+r*.1} ${cy-r*.9}L${cx-r*.18} ${cy-r*.3}L${cx+r*.16} ${cy-r*.05}L${cx-r*.14} ${cy+r*.45}L${cx+r*.02} ${cy+r*.95}" fill="none" stroke="#0E1218" stroke-width="${Math.max(4,r*.22)}" stroke-linecap="round" stroke-linejoin="round"/><path d="M${cx+r*.1} ${cy-r*.9}L${cx-r*.18} ${cy-r*.3}L${cx+r*.16} ${cy-r*.05}L${cx-r*.14} ${cy+r*.45}L${cx+r*.02} ${cy+r*.95}" fill="none" stroke="${c}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>`},
 okC:(n,c,w,h,cx,cy)=>{const r=Math.min(w,h)/2;return `<rect x="${cx-r*.9}" y="${cy-r*.9}" width="${r*1.8}" height="${r*1.8}" rx="${r*.38}" fill="rgba(63,216,194,.14)" stroke="${c}" stroke-width="2.4"/><path d="M${cx-r*.42} ${cy+r*.02}L${cx-r*.1} ${cy+r*.34}L${cx+r*.44} ${cy-r*.32}" fill="none" stroke="${c}" stroke-width="${Math.max(3,r*.2)}" stroke-linecap="round" stroke-linejoin="round"/>`},
 koC:(n,c,w,h,cx,cy)=>{const r=Math.min(w,h)/2;return `<rect x="${cx-r*.9}" y="${cy-r*.9}" width="${r*1.8}" height="${r*1.8}" rx="${r*.38}" fill="rgba(255,110,110,.12)" stroke="${c}" stroke-width="2.4"/><path d="M${cx-r*.42} ${cy}H${cx+r*.42}" stroke="${c}" stroke-width="${Math.max(3,r*.22)}" stroke-linecap="round"/>`},
 okD:(n,c,w,h,cx,cy)=>{const r=Math.min(w,h)/2;return `<circle cx="${cx}" cy="${cy}" r="${r}" fill="${c}"/><path d="M${cx-r*.42} ${cy+r*.02}L${cx-r*.1} ${cy+r*.34}L${cx+r*.44} ${cy-r*.32}" fill="none" stroke="#0E1218" stroke-width="${Math.max(3,r*.2)}" stroke-linecap="round" stroke-linejoin="round"/>`},
 koD:(n,c,w,h,cx,cy)=>{const r=Math.min(w,h)/2;return `<circle cx="${cx}" cy="${cy}" r="${r}" fill="${c}"/><path d="M${cx-r*.42} ${cy-r*.42}L${cx+r*.42} ${cy+r*.42}M${cx+r*.42} ${cy-r*.42}L${cx-r*.42} ${cy+r*.42}" stroke="#0E1218" stroke-width="${Math.max(3,r*.2)}" stroke-linecap="round"/>`},
 sigSeal:(n,c,w,h,cx,cy)=>{const r=Math.min(w,h)/2;let b='';for(let i=0;i<14;i++){const a=i*Math.PI*2/14;b+=`<circle cx="${cx+Math.cos(a)*r*.82}" cy="${cy+Math.sin(a)*r*.82}" r="${r*.2}"/>`}return `<g fill="rgba(246,185,76,.16)" stroke="${c}" stroke-width="2">${b}<circle cx="${cx}" cy="${cy}" r="${r*.84}"/></g><circle cx="${cx}" cy="${cy}" r="${r*.52}" fill="none" stroke="${c}" stroke-width="1.8"/><path d="M${cx-r*.22} ${cy+r*.02}L${cx-r*.05} ${cy+r*.2}L${cx+r*.26} ${cy-r*.16}" fill="none" stroke="${c}" stroke-width="${Math.max(2.4,r*.12)}" stroke-linecap="round" stroke-linejoin="round"/>`},
 sigFinger:(n,c,w,h,cx,cy)=>{const r=Math.min(w,h)/2;let d='';[.2,.36,.52,.68,.84].forEach((k,i)=>{d+=`M${cx-r*k} ${cy+r*(.35-.1*i)}V${cy}A${r*k} ${r*k*1.05} 0 0 1 ${cx+r*k} ${cy}V${cy+r*(.15+.1*i)}`});return `<rect x="${cx-r}" y="${cy-r}" width="${r*2}" height="${r*2}" rx="${r*.3}" fill="none" stroke="${c}" stroke-opacity=".5" stroke-width="1.6"/><path d="${d}" fill="none" stroke="${c}" stroke-width="2.2" stroke-linecap="round"/>`},
 sigPen:(n,c,w,h,cx,cy)=>{const r=Math.min(w,h)/2;return `<path d="M${cx-r} ${cy+r*.5}C${cx-r*.7} ${cy-r*.5} ${cx-r*.5} ${cy-r*.5} ${cx-r*.45} ${cy+r*.1}C${cx-r*.4} ${cy+r*.6} ${cx-r*.1} ${cy-r*.3} ${cx+r*.05} ${cy+r*.15}C${cx+r*.15} ${cy+r*.4} ${cx+r*.3} ${cy+r*.1} ${cx+r*.5} ${cy+r*.05}" fill="none" stroke="${c}" stroke-width="2.6" stroke-linecap="round"/><path d="M${cx-r} ${cy+r*.82}H${cx+r*.6}" stroke="${c}" stroke-opacity=".5" stroke-width="1.6"/><path d="M${cx+r*.52} ${cy-r*.05}L${cx+r*.95} ${cy-r*.78}L${cx+r*.78} ${cy-r*.9}L${cx+r*.34} ${cy-r*.2}Z" fill="rgba(246,185,76,.18)" stroke="${c}" stroke-width="1.8" stroke-linejoin="round"/>`},
 sigLock:(n,c,w,h,cx,cy)=>{const r=Math.min(w,h)/2;return `<path d="M${cx-r*.46} ${cy-r*.1}V${cy-r*.42}A${r*.46} ${r*.46} 0 0 1 ${cx+r*.46} ${cy-r*.42}V${cy-r*.1}" fill="none" stroke="${c}" stroke-width="2.4"/><rect x="${cx-r*.78}" y="${cy-r*.12}" width="${r*1.56}" height="${r*1.08}" rx="${r*.2}" fill="rgba(246,185,76,.14)" stroke="${c}" stroke-width="2.4"/><path d="M${cx-r*.28} ${cy+r*.4}L${cx-r*.06} ${cy+r*.62}L${cx+r*.34} ${cy+r*.14}" fill="none" stroke="${c}" stroke-width="${Math.max(2.4,r*.14)}" stroke-linecap="round" stroke-linejoin="round"/>`},
 sigBadge:(n,c,w,h,cx,cy)=>{const r=Math.min(w,h)/2;return `<rect x="${cx-r*.78}" y="${cy-r}" width="${r*1.56}" height="${r*2}" rx="${r*.22}" fill="rgba(246,185,76,.12)" stroke="${c}" stroke-width="2.2"/><circle cx="${cx}" cy="${cy-r*.34}" r="${r*.26}" fill="none" stroke="${c}" stroke-width="2"/><path d="M${cx-r*.46} ${cy+r*.18}Q${cx} ${cy-r*.2} ${cx+r*.46} ${cy+r*.18}" fill="none" stroke="${c}" stroke-width="2"/><path d="M${cx-r*.46} ${cy+r*.52}H${cx+r*.46}M${cx-r*.46} ${cy+r*.74}H${cx+r*.1}" stroke="${c}" stroke-opacity=".7" stroke-width="2" stroke-linecap="round"/>`},
 sigStamp:(n,c,w,h,cx,cy)=>{const r=Math.min(w,h)/2;return `<g transform="rotate(-12 ${cx} ${cy})"><circle cx="${cx}" cy="${cy}" r="${r}" fill="none" stroke="${c}" stroke-width="2.6"/><circle cx="${cx}" cy="${cy}" r="${r*.82}" fill="none" stroke="${c}" stroke-width="1.4"/><path d="M${cx-r*.42} ${cy+r*.4}L${cx} ${cy-r*.44}L${cx+r*.42} ${cy+r*.4}M${cx-r*.22} ${cy+r*.1}H${cx+r*.22}" fill="none" stroke="${c}" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round"/></g>`},
 flagTrophy:(n,c,w,h,cx,cy)=>{const r=Math.min(w,h)/2;return `<path d="M${cx-r*.55} ${cy-r*.85}H${cx+r*.55}V${cy-r*.2}A${r*.55} ${r*.55} 0 0 1 ${cx-r*.55} ${cy-r*.2}Z" fill="rgba(246,185,76,.2)" stroke="${c}" stroke-width="2.2" stroke-linejoin="round"/><path d="M${cx-r*.55} ${cy-r*.7}H${cx-r*.9}Q${cx-r*.9} ${cy-r*.1} ${cx-r*.5} ${cy-r*.12}M${cx+r*.55} ${cy-r*.7}H${cx+r*.9}Q${cx+r*.9} ${cy-r*.1} ${cx+r*.5} ${cy-r*.12}" fill="none" stroke="${c}" stroke-width="2"/><path d="M${cx} ${cy+r*.35}V${cy+r*.62}M${cx-r*.4} ${cy+r*.85}H${cx+r*.4}" stroke="${c}" stroke-width="2.4" stroke-linecap="round"/>`},
 flagToken:(n,c,w,h,cx,cy)=>{const r=Math.min(w,h)/2,pts=[...Array(6)].map((_,i)=>{const a=Math.PI/6+i*Math.PI/3;return (cx+r*Math.cos(a)).toFixed(1)+','+(cy+r*Math.sin(a)).toFixed(1)}).join(' ');return `<polygon points="${pts}" fill="rgba(246,185,76,.16)" stroke="${c}" stroke-width="2.4" stroke-linejoin="round"/><path d="M${cx} ${cy-r*.5}L${cx+r*.15} ${cy-r*.13}L${cx+r*.52} ${cy-r*.1}L${cx+r*.24} ${cy+r*.14}L${cx+r*.33} ${cy+r*.5}L${cx} ${cy+r*.3}L${cx-r*.33} ${cy+r*.5}L${cx-r*.24} ${cy+r*.14}L${cx-r*.52} ${cy-r*.1}L${cx-r*.15} ${cy-r*.13}Z" fill="${c}" fill-opacity=".5" stroke="${c}" stroke-width="1.6" stroke-linejoin="round"/>`},
 flagEnv:(n,c,w,h,cx,cy)=>{const r=Math.min(w,h)/2;return `<rect x="${cx-r}" y="${cy-r*.66}" width="${r*2}" height="${r*1.32}" rx="${r*.14}" fill="rgba(246,185,76,.12)" stroke="${c}" stroke-width="2.2"/><path d="M${cx-r} ${cy-r*.62}L${cx} ${cy+r*.12}L${cx+r} ${cy-r*.62}" fill="none" stroke="${c}" stroke-width="2"/><circle cx="${cx}" cy="${cy+r*.12}" r="${r*.2}" fill="${c}"/>`},
 flagCard:(n,c,w,h,cx,cy)=>{const r=Math.min(w,h)/2;return `<rect x="${cx-r}" y="${cy-r*.68}" width="${r*2}" height="${r*1.36}" rx="${r*.18}" fill="rgba(246,185,76,.12)" stroke="${c}" stroke-width="2.2"/><rect x="${cx-r*.78}" y="${cy-r*.38}" width="${r*.5}" height="${r*.4}" rx="${r*.08}" fill="none" stroke="${c}" stroke-width="1.8"/><path d="M${cx-r*.78} ${cy+r*.3}H${cx+r*.76}M${cx-r*.78} ${cy+r*.5}H${cx+r*.2}" stroke="${c}" stroke-opacity=".7" stroke-width="2" stroke-linecap="round"/>`},
 flagGem:(n,c,w,h,cx,cy)=>{const r=Math.min(w,h)/2;return `<path d="M${cx-r*.7} ${cy-r*.35}L${cx-r*.35} ${cy-r*.8}H${cx+r*.35}L${cx+r*.7} ${cy-r*.35}L${cx} ${cy+r*.85}Z" fill="rgba(246,185,76,.16)" stroke="${c}" stroke-width="2.2" stroke-linejoin="round"/><path d="M${cx-r*.7} ${cy-r*.35}H${cx+r*.7}M${cx-r*.35} ${cy-r*.8}L${cx-r*.2} ${cy-r*.35}L${cx} ${cy+r*.85}M${cx+r*.35} ${cy-r*.8}L${cx+r*.2} ${cy-r*.35}L${cx} ${cy+r*.85}" fill="none" stroke="${c}" stroke-width="1.5" stroke-linejoin="round"/>`},
 ideaCloud:(n,c,w,h,cx,cy)=>{const r=Math.min(w,h)/2;return `<path d="M${cx-r*.6} ${cy+r*.2}A${r*.38} ${r*.38} 0 0 1 ${cx-r*.55} ${cy-r*.45}A${r*.45} ${r*.45} 0 0 1 ${cx+r*.25} ${cy-r*.6}A${r*.42} ${r*.42} 0 0 1 ${cx+r*.7} ${cy-r*.05}A${r*.32} ${r*.32} 0 0 1 ${cx+r*.5} ${cy+r*.3}H${cx-r*.4}A${r*.2} ${r*.2} 0 0 1 ${cx-r*.6} ${cy+r*.2}Z" fill="rgba(246,185,76,.12)" stroke="${c}" stroke-width="2.2"/><circle cx="${cx-r*.5}" cy="${cy+r*.62}" r="${r*.12}" fill="${c}"/><circle cx="${cx-r*.8}" cy="${cy+r*.88}" r="${r*.07}" fill="${c}"/><path d="M${cx} ${cy-r*.35}L${cx+r*.07} ${cy-r*.1}L${cx+r*.32} ${cy-r*.03}L${cx+r*.07} ${cy+r*.04}L${cx} ${cy+r*.28}L${cx-r*.07} ${cy+r*.04}L${cx-r*.32} ${cy-r*.03}L${cx-r*.07} ${cy-r*.1}Z" fill="${c}"/>`},
 ideaSpark:(n,c,w,h,cx,cy)=>{const r=Math.min(w,h)/2,st=(x,y,s)=>`<path d="M${x} ${y-s}Q${x+s*.12} ${y-s*.12} ${x+s} ${y}Q${x+s*.12} ${y+s*.12} ${x} ${y+s}Q${x-s*.12} ${y+s*.12} ${x-s} ${y}Q${x-s*.12} ${y-s*.12} ${x} ${y-s}Z" fill="${c}"/>`;return st(cx-r*.1,cy+r*.05,r*.72)+st(cx+r*.62,cy-r*.55,r*.32)+st(cx-r*.62,cy-r*.52,r*.22)},
 ideaBolt:(n,c,w,h,cx,cy)=>{const r=Math.min(w,h)/2;return `<path d="M${cx+r*.18} ${cy-r}L${cx-r*.55} ${cy+r*.12}H${cx-r*.05}L${cx-r*.2} ${cy+r}L${cx+r*.55} ${cy-r*.2}H${cx+r*.02}Z" fill="rgba(246,185,76,.22)" stroke="${c}" stroke-width="2.4" stroke-linejoin="round"/>`},
 ideaBang:(n,c,w,h,cx,cy)=>{const r=Math.min(w,h)/2;return `<path d="M${cx-r*.9} ${cy-r*.7}H${cx+r*.9}V${cy+r*.35}H${cx-r*.1}L${cx-r*.5} ${cy+r*.85}V${cy+r*.35}H${cx-r*.9}Z" fill="rgba(246,185,76,.12)" stroke="${c}" stroke-width="2.2" stroke-linejoin="round"/><path d="M${cx+r*.05} ${cy-r*.5}V${cy+r*.02}" stroke="${c}" stroke-width="${r*.22}" stroke-linecap="round"/><circle cx="${cx+r*.05}" cy="${cy+r*.24}" r="${r*.1}" fill="${c}"/>`},
 ideaFork:(n,c,w,h,cx,cy)=>{const r=Math.min(w,h)/2;return `<path d="M${cx} ${cy+r}V${cy+r*.1}M${cx} ${cy+r*.1}Q${cx} ${cy-r*.2} ${cx-r*.6} ${cy-r*.5}M${cx} ${cy+r*.1}Q${cx} ${cy-r*.2} ${cx+r*.6} ${cy-r*.5}" fill="none" stroke="${c}" stroke-width="2.6" stroke-linecap="round"/><circle cx="${cx-r*.66}" cy="${cy-r*.62}" r="${r*.2}" fill="none" stroke="${c}" stroke-width="2.2"/><circle cx="${cx+r*.66}" cy="${cy-r*.62}" r="${r*.2}" fill="${c}"/><circle cx="${cx}" cy="${cy+r*.1}" r="${r*.1}" fill="${c}"/>`},
 scSee:(n,c,w,h,cx,cy)=>{const a=(n.tilt||0)*10*Math.PI/180,L=w*.44,by=n.y+h*.62,x1=cx-L*Math.cos(a),y1=by+L*Math.sin(a),x2=cx+L*Math.cos(a),y2=by-L*Math.sin(a);return `<path d="M${cx} ${by}L${cx-w*.14} ${n.y+h}H${cx+w*.14}Z" fill="rgba(140,150,164,.2)" stroke="#8C96A4" stroke-width="2"/><path d="M${x1} ${y1}L${x2} ${y2}" stroke="${c}" stroke-width="5" stroke-linecap="round"/><circle cx="${x1}" cy="${y1-w*.07}" r="${w*.07}" fill="${c}" fill-opacity=".35" stroke="${c}"/><circle cx="${x2}" cy="${y2-w*.12}" r="${w*.12}" fill="${c}" fill-opacity=".35" stroke="${c}"/>`},
 scGauge:(n,c,w,h,cx,cy)=>{const R=Math.min(w/2,h)*.9,by=n.y+h*.85,a=(n.tilt||0)*65*Math.PI/180;return `<path d="M${cx-R} ${by}A${R} ${R} 0 0 1 ${cx+R} ${by}" fill="none" stroke="#8C96A4" stroke-width="2.4"/><path d="M${cx-R*.96} ${by-R*.28}L${cx-R*.8} ${by-R*.22}M${cx+R*.96} ${by-R*.28}L${cx+R*.8} ${by-R*.22}M${cx} ${by-R}V${by-R*.84}" stroke="#8C96A4" stroke-width="2"/><path d="M${cx} ${by}L${cx+R*.82*Math.sin(a)} ${by-R*.82*Math.cos(a)}" stroke="${c}" stroke-width="3.4" stroke-linecap="round"/><circle cx="${cx}" cy="${by}" r="6" fill="${c}"/>`},
 scTug:(n,c,w,h,cx,cy)=>{const k=(n.tilt||0)*w*.2;return `<path d="M${n.x+w*.08} ${cy}H${n.x+w*.92}" stroke="#8C96A4" stroke-width="3" stroke-linecap="round"/><path d="M${cx} ${cy-h*.38}V${cy+h*.38}" stroke="#8C96A4" stroke-opacity=".5" stroke-dasharray="4 4"/><circle cx="${cx+k}" cy="${cy}" r="${h*.1}" fill="${c}"/><rect x="${n.x}" y="${cy-h*.2}" width="${w*.08}" height="${h*.4}" rx="4" fill="${c}" fill-opacity=".3" stroke="${c}"/><rect x="${n.x+w*.92}" y="${cy-h*.3}" width="${w*.08}" height="${h*.6}" rx="4" fill="${c}" fill-opacity=".3" stroke="${c}"/>`},
 flPen:(n,c,w,h)=>{const px=n.x+w*.2,f='fill="'+c+'" fill-opacity=".28" stroke="'+c+'" stroke-width="1.8" stroke-linejoin="round"';return `<path d="M${px} ${n.y}V${n.y+h}" stroke="${c}" stroke-width="2.2" stroke-linecap="round"/><path d="M${px} ${n.y+2}L${n.x+w} ${n.y+h*.2}L${px} ${n.y+h*.42}Z" ${f}/>`},
 flSwal:(n,c,w,h)=>{const px=n.x+w*.2,f='fill="'+c+'" fill-opacity=".28" stroke="'+c+'" stroke-width="1.8" stroke-linejoin="round"';return `<path d="M${px} ${n.y}V${n.y+h}" stroke="${c}" stroke-width="2.2" stroke-linecap="round"/><path d="M${px} ${n.y+2}H${n.x+w}L${n.x+w*.78} ${n.y+h*.22}L${n.x+w} ${n.y+h*.44}H${px}Z" ${f}/>`},
 flWave:(n,c,w,h)=>{const px=n.x+w*.2,x2=n.x+w,t=n.y+2,b=n.y+h*.46,m=(px+x2)/2,q=(px+m)/2,r=(m+x2)/2,d=h*.07;return `<path d="M${px} ${n.y}V${n.y+h}" stroke="${c}" stroke-width="2.2" stroke-linecap="round"/><path d="M${px} ${t}C${q} ${t-d*2} ${m} ${t+d*2} ${x2} ${t}V${b}C${r} ${b+d*2} ${m} ${b-d*2} ${px} ${b}Z" fill="${c}" fill-opacity=".28" stroke="${c}" stroke-width="1.8" stroke-linejoin="round"/>`},
 flChk:(n,c,w,h)=>{const px=n.x+w*.2,x2=n.x+w,t=n.y+2,b=n.y+h*.46,cw=(x2-px)/4,ch=(b-t)/3;let q='';for(let i=0;i<4;i++)for(let j=0;j<3;j++)if((i+j)%2==0)q+=`<rect x="${px+i*cw}" y="${t+j*ch}" width="${cw}" height="${ch}"/>`;return `<path d="M${px} ${n.y}V${n.y+h}" stroke="${c}" stroke-width="2.2" stroke-linecap="round"/><g fill="${c}" fill-opacity=".55">${q}</g><rect x="${px}" y="${t}" width="${x2-px}" height="${b-t}" fill="none" stroke="${c}" stroke-width="1.8"/>`},
 flBan:(n,c,w,h)=>{const x0=n.x+w*.12,x1=n.x+w*.88,mx=(x0+x1)/2,t=n.y+h*.1;return `<path d="M${mx} ${n.y}V${n.y+h}" stroke="${c}" stroke-width="2.2" stroke-linecap="round"/><path d="M${x0-2} ${t}H${x1+2}" stroke="${c}" stroke-width="2.4" stroke-linecap="round"/><path d="M${x0+3} ${t}V${t+h*.55}L${(x0+x1)/2-1} ${t+h*.42}L${x1-3} ${t+h*.55}V${t}Z" fill="${c}" fill-opacity=".28" stroke="${c}" stroke-width="1.8" stroke-linejoin="round"/>`},
 flFly:(n,c,w,h)=>{const px=n.x+w*.2,x2=n.x+w,t=n.y+2,m=n.y+h*.3,b=n.y+h*.52;return `<path d="M${px} ${n.y}V${n.y+h}" stroke="${c}" stroke-width="2.2" stroke-linecap="round"/><path d="M${px} ${t}C${px+(x2-px)*.3} ${t-4} ${px+(x2-px)*.5} ${t+10} ${x2} ${t+4}C${x2-8} ${m-2} ${x2-4} ${m+2} ${x2-2} ${b-4}C${px+(x2-px)*.6} ${b+6} ${px+(x2-px)*.3} ${b-8} ${px} ${b}Z" fill="${c}" fill-opacity="${n.dashed?.08:.28}" stroke="${c}" stroke-width="1.8" stroke-linejoin="round" stroke-dasharray="${n.dashed?'4 3':'0'}"/>`},
 scChain:(n,c,w,h,cx,cy)=>{const a=(n.tilt||0)*11*Math.PI/180,L=w*.42,by=n.y+h*.3,x1=cx-L*Math.cos(a),y1=by-L*Math.sin(a),x2=cx+L*Math.cos(a),y2=by+L*Math.sin(a),pw=w*.17,pd=h*.3,bowl=(x,y)=>`<path d="M${x} ${y}L${x-pw} ${y+pd*.7}M${x} ${y}L${x+pw} ${y+pd*.7}" stroke="${c}" stroke-width="1.2" fill="none"/><path d="M${x-pw*1.15} ${y+pd*.7}Q${x} ${y+pd*1.35} ${x+pw*1.15} ${y+pd*.7}Z" fill="${c}" fill-opacity=".22" stroke="${c}" stroke-width="2" stroke-linejoin="round"/>`;return `<path d="M${cx} ${by}Q${cx+w*.05} ${n.y+h*.7} ${cx} ${n.y+h}M${cx-w*.2} ${n.y+h}Q${cx} ${n.y+h-6} ${cx+w*.2} ${n.y+h}" stroke="#8C96A4" stroke-width="3" fill="none" stroke-linecap="round"/><path d="M${x1} ${y1}L${x2} ${y2}" stroke="${c}" stroke-width="3" stroke-linecap="round"/><circle cx="${cx}" cy="${by}" r="5" fill="#0E1218" stroke="${c}" stroke-width="2.4"/>${bowl(x1,y1)}${bowl(x2,y2)}`},
 scBowl:(n,c,w,h,cx,cy)=>{const a=(n.tilt||0)*11*Math.PI/180,L=w*.42,by=n.y+h*.3,x1=cx-L*Math.cos(a),y1=by-L*Math.sin(a),x2=cx+L*Math.cos(a),y2=by+L*Math.sin(a),pw=w*.18,bowl=(x,y)=>`<path d="M${x} ${y}V${y+h*.14}" stroke="${c}" stroke-width="1.6"/><path d="M${x-pw} ${y+h*.14}A${pw} ${pw*.9} 0 0 0 ${x+pw} ${y+h*.14}Z" fill="${c}" fill-opacity=".22" stroke="${c}" stroke-width="2" stroke-linejoin="round"/>`;return `<path d="M${cx} ${by}V${n.y+h}" stroke="#8C96A4" stroke-width="3" stroke-linecap="round"/><path d="M${x1} ${y1}Q${cx} ${by-h*.1} ${x2} ${y2}" stroke="${c}" stroke-width="3" fill="none" stroke-linecap="round"/><circle cx="${cx}" cy="${by-h*.04}" r="4.5" fill="${c}"/>${bowl(x1,y1)}${bowl(x2,y2)}`},
 scLoose:(n,c,w,h,cx,cy)=>{const a=(n.tilt||0)*11*Math.PI/180,L=w*.42,by=n.y+h*.3,x1=cx-L*Math.cos(a),y1=by-L*Math.sin(a),x2=cx+L*Math.cos(a),y2=by+L*Math.sin(a),pw=w*.17,pd=h*.32,pan=(x,y,k)=>`<path d="M${x} ${y}Q${x-pw*.3*k} ${y+pd*.4} ${x-pw} ${y+pd}M${x} ${y}Q${x+pw*.3*k} ${y+pd*.4} ${x+pw} ${y+pd}" stroke="${c}" stroke-width="1.3" fill="none"/><path d="M${x-pw*1.2} ${y+pd}Q${x} ${y+pd+pw*.55} ${x+pw*1.2} ${y+pd}" stroke="${c}" stroke-width="2.4" fill="none" stroke-linecap="round"/>`;return `<path d="M${cx} ${by}C${cx-w*.05} ${n.y+h*.55} ${cx+w*.05} ${n.y+h*.8} ${cx} ${n.y+h}M${cx-w*.17} ${n.y+h}Q${cx} ${n.y+h-5} ${cx+w*.17} ${n.y+h}" stroke="#8C96A4" stroke-width="2.6" fill="none" stroke-linecap="round"/><path d="M${x1} ${y1}Q${cx} ${by+2} ${x2} ${y2}" stroke="${c}" stroke-width="2.8" fill="none" stroke-linecap="round"/><circle cx="${cx}" cy="${by+1}" r="4" fill="${c}"/>${pan(x1,y1,1)}${pan(x2,y2,-1)}`},
 scHang:(n,c,w,h,cx,cy)=>{const a=(n.tilt||0)*11*Math.PI/180,L=w*.4,by=n.y+h*.34,top=n.y+h*.02,x1=cx-L*Math.cos(a),y1=by-L*Math.sin(a),x2=cx+L*Math.cos(a),y2=by+L*Math.sin(a),pw=w*.16,pd=h*.3,pan=(x,y)=>`<path d="M${x} ${y}L${x-pw} ${y+pd}M${x} ${y}L${x+pw} ${y+pd}" stroke="${c}" stroke-width="1.2" fill="none"/><path d="M${x-pw*1.1} ${y+pd}Q${x} ${y+pd+pw*.8} ${x+pw*1.1} ${y+pd}Z" fill="${c}" fill-opacity=".22" stroke="${c}" stroke-width="2" stroke-linejoin="round"/>`;return `<circle cx="${cx}" cy="${top+4}" r="4" fill="none" stroke="#8C96A4" stroke-width="2.2"/><path d="M${cx} ${top+8}V${by}" stroke="#8C96A4" stroke-width="2.2"/><path d="M${x1} ${y1}L${x2} ${y2}" stroke="${c}" stroke-width="3" stroke-linecap="round"/><circle cx="${cx}" cy="${by}" r="4.5" fill="${c}"/>${pan(x1,y1)}${pan(x2,y2)}`},
 orb:(n,c,w,h,cx,cy)=>{const r=Math.min(w,h)*.36,oy=cy-h*.06;return `<path d="M${cx-r*.8} ${n.y+h}Q${cx} ${n.y+h*.8} ${cx+r*.8} ${n.y+h}Z" fill="${c}" fill-opacity=".25" stroke="${c}" stroke-width="2" stroke-linejoin="round"/><circle cx="${cx}" cy="${oy}" r="${r}" fill="${c}" fill-opacity=".12" stroke="${c}" stroke-width="2.4"/><path d="M${cx-r*.62} ${oy-r*.1}A${r*.65} ${r*.65} 0 0 1 ${cx-r*.1} ${oy-r*.62}" fill="none" stroke="${c}" stroke-width="2.2" stroke-linecap="round"/><path d="M${cx+r*.1} ${oy-r*.1}l${r*.08} ${r*.22}l${r*.22} ${r*.08}l${-r*.22} ${r*.08}l${-r*.08} ${r*.22}l${-r*.08} ${-r*.22}l${-r*.22} ${-r*.08}l${r*.22} ${-r*.08}Z" fill="${c}"/>`},
 scBlocks:(n,c,w,h,cx,cy)=>{const a=(n.tilt||0)*8*Math.PI/180,L=w*.44,by=n.y+h*.7,x1=cx-L*Math.cos(a),y1=by+L*Math.sin(a),x2=cx+L*Math.cos(a),y2=by-L*Math.sin(a);return `<path d="M${cx} ${by}V${n.y+h}M${cx-w*.16} ${n.y+h}H${cx+w*.16}" stroke="#8C96A4" stroke-width="3" stroke-linecap="round"/><path d="M${x1} ${y1}L${x2} ${y2}" stroke="${c}" stroke-width="4" stroke-linecap="round"/><rect x="${x1-w*.07}" y="${y1-w*.14}" width="${w*.14}" height="${w*.14}" fill="${c}" fill-opacity=".3" stroke="${c}"/><rect x="${x2-w*.13}" y="${y2-w*.26}" width="${w*.26}" height="${w*.26}" fill="${c}" fill-opacity=".3" stroke="${c}"/><rect x="${x2-w*.09}" y="${y2-w*.4}" width="${w*.18}" height="${w*.14}" fill="${c}" fill-opacity=".3" stroke="${c}"/>`},
 pencil:(n,c,w,h,cx,cy)=>{const r=Math.min(w,h)/2;return `<path d="M${cx-r*.7} ${cy+r*.7}L${cx-r*.55} ${cy+r*.2}L${cx+r*.3} ${cy-r*.65}L${cx+r*.7} ${cy-r*.25}L${cx-r*.15} ${cy+r*.6}Z" fill="rgba(63,216,194,.16)" stroke="${c}" stroke-width="2.2" stroke-linejoin="round"/><path d="M${cx+r*.12} ${cy-r*.47}L${cx+r*.52} ${cy-r*.07}" stroke="${c}" stroke-width="2"/>`},
 bar:(n,c,w,h)=>`<rect x="${n.x}" y="${n.y}" width="${w}" height="${h}" rx="${h/2}" fill="#0E1218" stroke="${c}" stroke-opacity=".7" stroke-width="1.6"/><rect class="bf" x="${n.x+2}" y="${n.y+2}" width="0" height="${h-4}" rx="${(h-4)/2}" fill="${c}" fill-opacity=".85"/>`,
 pause:(n,c,w,h)=>`<rect x="${n.x+w*.18}" y="${n.y}" width="${w*.24}" height="${h}" rx="3" fill="${c}"/><rect x="${n.x+w*.58}" y="${n.y}" width="${w*.24}" height="${h}" rx="3" fill="${c}"/>`,
 stop:(n,c,w,h,cx,cy)=>{const r=Math.min(w,h)/2,pts=[...Array(8)].map((_,i)=>{const a=Math.PI/8+i*Math.PI/4;return(cx+r*Math.cos(a)).toFixed(1)+','+(cy+r*Math.sin(a)).toFixed(1)}).join(' ');return `<polygon points="${pts}" fill="#171D26" stroke="${c}" stroke-width="2.2"/><path d="M${cx-r*.45} ${cy}H${cx+r*.45}" stroke="${c}" stroke-width="3" stroke-linecap="round"/>`},
 num:(n,c,w,h,cx,cy)=>`<text class="nm" x="${cx}" y="${cy+(n.fs||26)*.35}" fill="${c}" font-size="${n.fs||26}" text-anchor="middle" font-weight="600">0</text>`
};
/* ---------- overflow guard: every <text> inside a node is forced to stay inside its container (first <rect> ≈ node box) or inside the frame ---------- */
window.__fit=window.__fit||[];
const fitText=(q,box,dyn,id)=>{
 if(!q.isConnected)return;if(q.hasAttribute('textLength')){q.removeAttribute('textLength')}
 if(!q.textContent)return;let b;try{b=q.getBBox()}catch(e){return}if(!b.width)return;
 const an=q.getAttribute('text-anchor')||'start',pad=8,L=box[0],R=box[0]+box[2],x=an==='middle'?b.x+b.width/2:an==='end'?b.x+b.width:b.x;
 const inside=x>=L-1&&x<=R+1;const BL=inside?L:4,BR=inside?R:956,pd=inside?pad:0;
 const W=an==='middle'?2*Math.min(x-BL,BR-x)-2*pd:an==='end'?x-BL-pd:BR-pd-x;
 if(inside){const by=+q.getAttribute('y');if(by&&by>box[1]+box[3]-2){q.style.visibility='hidden';window.__fit.push({id,t:q.textContent.slice(0,40),how:'hidden'});return}else q.style.visibility=''}
 if(b.width<=W+.5)return;
 if(!dyn){const fs=parseFloat(q.getAttribute('font-size')||12),k=Math.max(.6,W/b.width);if(!q._fs0)q._fs0=fs;q.setAttribute('font-size',(fs*k).toFixed(2));try{b=q.getBBox()}catch(e){}}
 if(b.width>W+.5){q.setAttribute('textLength',Math.max(8,W).toFixed(1));q.setAttribute('lengthAdjust','spacingAndGlyphs')}
 window.__fit.push({id,t:q.textContent.slice(0,40),how:dyn?'squeezed':'shrunk'})};
const nodeBox=(e,n)=>{const r=e.querySelector('rect');if(r){try{const b=r.getBBox();if(b.width>20&&b.height>14&&Math.abs(b.x-n.x)<3&&Math.abs(b.y-n.y)<3)return[b.x,b.y,b.width,b.height]}catch(_){}}return[-1e4,-1e4,2e4,2e4]};
const DYN='ml,cl,tx,ct,nm,jn,in2';
const fitNode=(e,n,first)=>{if(!e.isConnected)return;const bx=n.kind==='txt'?[-1e4,-1e4,2e4,2e4]:(e._bx||(e._bx=nodeBox(e,n)));
 e.querySelectorAll('text').forEach(q=>{const dyn=q.matches('.ml,.cl,.tx,.ct,.nm,.jn');if(!first&&!dyn)return;if(dyn){const k=q.textContent;if(q._lt===k&&!first)return;q._lt=k}fitText(q,bx,dyn,n.id)})};
A.world=(h,p,C)=>{
 const N=p.nodes||[],Lk=p.links||[],byId={};N.forEach(n=>byId[n.id]=n);
 const ctr=n=>[n.x+(n.w||0)/2,n.y+(n.h||0)/2];
 const edge=(n,m)=>{const [ax,ay]=ctr(n),[bx,by]=ctr(m),dx=bx-ax,dy=by-ay,hw=(n.w||90)/2,hh=(n.h||60)/2,k=Math.min(Math.abs(dx)>1e-6?hw/Math.abs(dx):1e9,Math.abs(dy)>1e-6?hh/Math.abs(dy):1e9);return[ax+dx*Math.min(1,k),ay+dy*Math.min(1,k)]};
 const cp=(x1,y1,x2,y2,l,i)=>{if(l.via)return[2*l.via[0]-(x1+x2)/2,2*l.via[1]-(y1+y2)/2];const dx=x2-x1,dy=y2-y1,len=Math.hypot(dx,dy)||1,k=(l.curve??.22)*(i%2?-1:1);return[(x1+x2)/2-dy/len*len*k,(y1+y2)/2+dx/len*len*k]};
 const orthPts=(l,a,b)=>{const [ax,ay]=ctr(a),[bx,by]=ctr(b),ha=(a.h||60)/2,hb=(b.h||60)/2,wa=(a.w||90)/2,wb=(b.w||90)/2;let m=l.orth;if(m===true)m=Math.abs(by-ay)>=Math.abs(bx-ax)?'v':'h';
  if(m==='v'){const sy=by>ay?ay+ha:ay-ha,ey=by>ay?by-hb:by+hb,my=l.mid??(sy+ey)/2;return Math.abs(ax-bx)<1?[[ax,sy],[bx,ey]]:[[ax,sy],[ax,my],[bx,my],[bx,ey]]}
  const sx=bx>ax?ax+wa:ax-wa,ex=bx>ax?bx-wb:bx+wb,mx=l.mid??(sx+ex)/2;return Math.abs(ay-by)<1?[[sx,ay],[ex,by]]:[[sx,ay],[mx,ay],[mx,by],[ex,by]]};
 const orthD=P=>{let d=`M${P[0][0]} ${P[0][1]}`;for(let i=1;i<P.length-1;i++){const p0=P[i-1],p1=P[i],p2=P[i+1],d1=Math.hypot(p1[0]-p0[0],p1[1]-p0[1])||1,d2=Math.hypot(p2[0]-p1[0],p2[1]-p1[1])||1,r=Math.min(16,d1/2,d2/2),ax=p1[0]-(p1[0]-p0[0])/d1*r,ay=p1[1]-(p1[1]-p0[1])/d1*r,bx=p1[0]+(p2[0]-p1[0])/d2*r,by=p1[1]+(p2[1]-p1[1])/d2*r;d+=`L${ax} ${ay}Q${p1[0]} ${p1[1]} ${bx} ${by}`}const q=P[P.length-1];return d+`L${q[0]} ${q[1]}`};
 let s='';
 Lk.forEach((l,i)=>{const a=byId[l.a],b=byId[l.b],c=hex(l.color||'amber'),[x1,y1]=edge(a,b),[x2,y2]=edge(b,a);
  s+=`<g class="lk" data-i="${i}" style="opacity:0"><path d="${l.orth?orthD(orthPts(l,a,b)):`M${x1} ${y1}Q${cp(x1,y1,x2,y2,l,i)[0]} ${cp(x1,y1,x2,y2,l,i)[1]} ${x2} ${y2}`}" stroke="${c}" stroke-opacity="${l.orth?.7:.55}" stroke-width="${l.orth?1.8:1.6}" stroke-dasharray="${(l.solid||l.orth)&&!l.dashed?'0':'5 6'}" fill="none"/>${l.lock?`<g transform="translate(${(x1+x2)/4+cp(x1,y1,x2,y2,l,i)[0]/2-9} ${(y1+y2)/4+cp(x1,y1,x2,y2,l,i)[1]/2-11})"><rect x="0" y="9" width="18" height="14" rx="3" fill="#0E1218" stroke="${c}" stroke-width="1.8"/><path d="M4 9V5a5 5 0 0 1 10 0v4" fill="none" stroke="${c}" stroke-width="1.8"/></g>`:''}</g>`;
  s+=`<circle class="pl" data-i="${i}" r="4.5" fill="${c}" style="opacity:0"/><circle class="pl2" data-i="${i}" r="4.5" fill="${c}" style="opacity:0"/>`});
 N.forEach((n,i)=>{const c=hex(n.color||'blue'),w=n.w||90,hh=n.h||60,cx=n.x+w/2,cy=n.y+hh/2;let g='';
  if(n.kind==='sandbox'&&n.notop){const r=14,x2=n.x+w,y2=n.y+hh,gp=n.gap,d=`M${n.x} ${n.y}V${y2-r}A${r} ${r} 0 0 0 ${n.x+r} ${y2}H${x2-r}A${r} ${r} 0 0 0 ${x2} ${y2-r}${gp?`V${gp[1]}M${x2} ${gp[0]}`:''}V${n.y}`;const g2=`<rect x="${n.x}" y="${n.y}" width="${w}" height="${hh}" fill="rgba(63,216,194,.05)" stroke="none"/><path d="${d}" fill="none" stroke="${c}" stroke-width="2" stroke-dasharray="10 6"/>`;g=g2}
  else if(n.kind==='sandbox'&&n.gap){const r=14,x2=n.x+w,y2=n.y+hh,[g1,g2]=n.gap,d=`M${x2} ${g1}V${n.y+r}A${r} ${r} 0 0 0 ${x2-r} ${n.y}H${n.x+r}A${r} ${r} 0 0 0 ${n.x} ${n.y+r}V${y2-r}A${r} ${r} 0 0 0 ${n.x+r} ${y2}H${x2-r}A${r} ${r} 0 0 0 ${x2} ${y2-r}V${g2}`;g=`<path d="${d}Z" fill="rgba(63,216,194,.05)" stroke="none"/><path d="${d}" fill="none" stroke="${c}" stroke-width="2" stroke-dasharray="10 6"/><text x="${n.x+14}" y="${n.y-8}" fill="${c}" font-size="13">${esc(n.label||'')}</text>`}
  else if(n.kind==='sandbox')g=`<rect x="${n.x}" y="${n.y}" width="${w}" height="${hh}" rx="14" fill="rgba(63,216,194,.05)" stroke="${c}" stroke-width="2" stroke-dasharray="${n.open?'10 6':'0'}"/><text x="${n.x+14}" y="${n.y-8}" fill="${c}" font-size="13">${esc(n.label||'')}</text>`;
  else if(n.kind==='agent')g=`<circle cx="${cx}" cy="${cy}" r="${Math.min(w,hh)/2}" fill="#171D26" stroke="${c}" stroke-width="2.2"/>${MARK(cx,cy,Math.min(w,hh)*.8,c)}<text x="${cx}" y="${n.y+hh+16}" fill="#8C96A4" font-size="11" text-anchor="middle">${esc(n.label||'')}</text>`;
  else if(n.kind==='globe')g=`<circle cx="${cx}" cy="${cy}" r="${w/2}" fill="#10243A" stroke="${c}" stroke-width="2"/><ellipse cx="${cx}" cy="${cy}" rx="${w/4.5}" ry="${w/2}" fill="none" stroke="${c}" stroke-opacity=".6"/><path d="M${n.x} ${cy}H${n.x+w}M${n.x+w*.08} ${cy-w*.25}H${n.x+w*.92}M${n.x+w*.08} ${cy+w*.25}H${n.x+w*.92}" stroke="${c}" stroke-opacity=".4" fill="none"/><text x="${cx}" y="${n.y+w+18}" fill="${c}" font-size="13" text-anchor="middle">${esc(n.label||'')}</text>`;
  else if(n.kind==='server'||n.kind==='victim'){const inner=(n.inner||[]).map((t,j)=>{const iw=(w-24)/Math.max(1,n.inner.length)-6,ix=n.x+12+j*(iw+6);return `<g class="in2" data-i="${i}" style="opacity:0"><rect x="${ix}" y="${n.y+hh-34}" width="${iw}" height="22" rx="5" fill="#0E1218" stroke="${c}" stroke-opacity=".7"/><text x="${ix+iw/2}" y="${n.y+hh-19}" fill="#E7EBF1" font-size="8.5" text-anchor="middle">${esc(t)}</text></g>`}).join('');
   g=`<rect x="${n.x}" y="${n.y}" width="${w}" height="${hh}" rx="12" fill="#171D26" stroke="${c}" stroke-width="2"/><text x="${cx}" y="${n.y+26}" fill="#E7EBF1" font-size="${n.big?16:14}" text-anchor="middle">${esc(n.label||'')}</text><text x="${cx}" y="${n.y+44}" fill="#8C96A4" font-size="10" text-anchor="middle">${esc(n.sub||'')}</text>${n.kind==='victim'?`<g transform="translate(${n.x+w-24} ${n.y+8})"><path d="M8 1L15 14H1Z" fill="none" stroke="${c}" stroke-width="1.8"/><path d="M8 6V10" stroke="${c}" stroke-width="1.8"/></g>`:''}${inner}`}
  else if(ICON[n.kind])g=ICON[n.kind](n,c,w,hh,cx,cy);
  else g=`<rect x="${n.x}" y="${n.y}" width="${w}" height="${hh}" rx="10" fill="#171D26" stroke="${c}" stroke-width="1.8"/><text x="${cx}" y="${cy+5}" fill="#E7EBF1" font-size="12" text-anchor="middle">${esc(n.label||'')}</text>`;
  if(n.cap)g+=`<text x="${cx}" y="${n.y+hh+(n.kind==='agent'?30:16)}" fill="${hex(n.capc||'muted')}" font-size="${n.capfs||11}" ${n.capm?'font-family="ui-monospace,Menlo,monospace" ':''}text-anchor="middle">${esc(n.cap)}</text>`;
  if(n.tag)g+=`<text x="${cx}" y="${n.y-8}" fill="${hex(n.tagc||'muted')}" font-size="${n.tagfs||11}" text-anchor="middle">${esc(n.tag)}</text>`;
  s+=`<g class="nd" data-i="${i}" style="opacity:0;transform-box:fill-box;transform-origin:center">${g}</g>`});
 if(p.fs&&p.fs!==1)s=s.replace(/font-size="([\d.]+)"/g,(m,v)=>`font-size="${(+v*p.fs).toFixed(1)}"`);
 h.innerHTML=`<svg class="sv wv" viewBox="0 0 960 540">${s}</svg>`;
 const nd=[...h.querySelectorAll('.nd')],lk=[...h.querySelectorAll('.lk')],pl=[...h.querySelectorAll('.pl')],pl2=[...h.querySelectorAll('.pl2')],in2=[...h.querySelectorAll('.in2')];
 const ta=N.map(n=>C.T(n.at||0)),tu=N.map(n=>n.until!=null?C.T(n.until):1e9),mv=N.map(n=>(n.move||[]).map(m=>({t:C.T(m.at),x:m.x,y:m.y,d:m.dur||1.2}))),la=Lk.map(l=>{const g=id=>{const j=N.indexOf(byId[id]);return j>=0&&ta[j]>.3?ta[j]+.4:0};return Math.max(C.T(l.at||0),g(l.a),g(l.b))}),lu=Lk.map(l=>l.until!=null?C.T(l.until):1e9),ia=N.map(n=>n.innerAt!=null?C.T(n.innerAt):1e9),spot=(p.spot||[]).map(q=>({t:C.T(q.at),ids:q.ids}));
 const fl=N.map(n=>n.flick?{t:C.T(n.flick.at),d:n.flick.dur||2.5,e:n.flick.end||'off'}:null),flv=(i,t)=>{const f=fl[i];if(!f||t<f.t)return 1;const tt=t-f.t;if(tt>=f.d)return f.e==='on'?1:(f.e==='dim'?.12:0);const ph=tt/f.d;return Math.sin(tt*(20+16*ph))>(-.5+1.2*ph)?1:.08};
 const geo=Lk.map((l,i)=>{const a=byId[l.a],b=byId[l.b],A=edge(a,b),B=edge(b,a);return[A,B,cp(A[0],A[1],B[0],B[1],l,i)]});
 const upd=t=>{let act=null;for(const q of spot)if(t>=q.t)act=q;
  nd.forEach((e,i)=>{const u=ease(pr(t,ta[i],.6)),on=!act||act.ids.includes(N[i].id);e.dataset.on=on?1:0;
   const k=(e._k=(e._k??1)+((on?1:.3)-(e._k??1))*.25);const out=1-ease(pr(t,tu[i],.5));e.style.opacity=Math.max(u,p.ghost||0)*k*out*flv(i,t)*(N[i].alpha??1)*(N[i].litAt!=null&&N[i].kind!=='bulb'?.3+.7*ease(pr(t,C.T(N[i].litAt),.4)):1)*(N[i].blink&&(N[i].bat==null||t>=C.T(N[i].bat))?(1-N[i].blink*(.5+.5*Math.sin(t*(N[i].bf||5)+i*1.9))):1);let dx=0,dy=0,px=N[i].x,py=N[i].y;for(const m of mv[i]){const a=ease(pr(t,m.t-m.d,m.d));dx+=(m.x-px)*a;dy+=(m.y-py)*a;px+=(m.x-px)*(a>=1?1:0);py+=(m.y-py)*(a>=1?1:0)}
   if(mv[i].length){let bx=N[i].x,by=N[i].y;dx=0;dy=0;for(const m of mv[i]){const a=ease(pr(t,m.t-m.d,m.d));dx+=(m.x-bx)*a;dy+=(m.y-by)*a;bx=m.x;by=m.y}}
   if(N[i].shake){const s_=N[i].shake,uu=t-C.T(s_.at),dd=s_.dur||1.2;if(uu>=0&&uu<dd){const f=(s_.amp||4)*(1-uu/dd);dx+=f*Math.sin(uu*(s_.f||38));dy+=f*.4*Math.sin(uu*(s_.f||38)*1.3)}}
   e.style.transform=`translate(${dx}px,${dy}px) scale(${.92+.08*u})`;
   if(N[i].kind==='txt'){const q=e.querySelector('.tx'),o=N[i];let str=o.text||'';if(o.clock){const c=o.clock,t0=Date.UTC(c.y,c.m-1,c.d,c.h,c.mi),t1=Date.UTC(c.to.y,c.to.m-1,c.to.d,c.to.h,c.to.mi),u=ease(pr(t,C.T(c.at),c.dur)),D=new Date(t0+(t1-t0)*u),z=v=>String(v).padStart(2,'0');str=z(D.getUTCDate())+' '+['enero','febrero','marzo','abril','mayo','junio','julio','agosto','septiembre','octubre','noviembre','diciembre'][D.getUTCMonth()]+' '+D.getUTCFullYear()+' -- '+z(D.getUTCHours())+':'+z(D.getUTCMinutes())+' UTC'}
    if(o.type){const k=Math.max(0,Math.floor((t-ta[i])*o.type));q.textContent=str.slice(0,k)+(k<str.length?'\u258C':'')}else q.textContent=str}
   if(N[i].kind==='console'){const o=N[i],cl=[...e.querySelectorAll('.cl')],dt=Math.max(0,t-ta[i]),k=Math.floor((o.k||6)*dt+(o.a||6)*dt*dt),txt=(o.code||'').slice(0,k),ls=txt.split('\n'),cols=o.cols||34,vis=ls.slice(-cl.length);cl.forEach((q,j)=>{const L=vis[j];q.textContent=L==null?'':L.slice(0,cols)+((j===vis.length-1&&(Math.floor(t*2)%2))?'\u258C':'')})}
   if(N[i].kind==='exam'&&N[i].solve){const sp=e.querySelector('.sp');if(sp)sp.setAttribute('stroke-dashoffset',1-ease(pr(t,C.T(N[i].solve.at),N[i].solve.dur||4)))}
   if(N[i].kind==='article'){const o=N[i],ws=e._w||(e._w=[...e.querySelectorAll('.aw')]),rd=o.read,pr_=rd?ease(pr(t,C.T(rd.at),rd.dur||6)):0,cnt=pr_*ws.length,lc=hex(o.litc||'teal'),st=e._s||(e._s=[]);ws.forEach((q,j)=>{const v=j<cnt-2?lc:j<cnt?'#FFFFFF':'#566170';if(st[j]!==v){st[j]=v;q.setAttribute('fill',v)}})}
   if(N[i].kind==='judge'){const a_=ease(pr(t,N[i].nameAt!=null?C.T(N[i].nameAt):1e9,.6)),jn=e.querySelector('.jn'),jp=e.querySelector('.jp');if(jn)jn.style.opacity=a_;if(jp)jp.style.opacity=1-a_}
   if(N[i].kind==='msgfeed'){const o=N[i],ml=[...e.querySelectorAll('.ml')],dt=Math.max(0,t-ta[i]),r0=o.r0||2,r1=o.r1||r0,rp=o.ramp||4,pos=dt<rp?r0*dt+(r1-r0)*dt*dt/(2*rp):r0*rp+(r1-r0)*rp/2+r1*(dt-rp),top=Math.floor(pos+(o.off||0)),cols=o.cols||50;ml.forEach((q,j)=>{const idx=top-(ml.length-1-j);if(idx<0){q.textContent='';return}const L=msgLine(idx,o);q.textContent=L.s.slice(0,cols);q.setAttribute('fill',L.c)})}
   if(N[i].kind==='bar'){const q=e.querySelector('.bf');if(q)q.setAttribute('width',Math.max(0,(N[i].fill??1)*((N[i].w||90)-4)*ease(pr(t,ta[i]+.2,1.2))))}
   if(N[i].kind==='bulb'){const q=e.querySelector('.bl');if(q)q.style.opacity=ease(pr(t,N[i].litAt!=null?C.T(N[i].litAt):ta[i]+.4,.35))}
   if(N[i].kind==='folderview'){const its=N[i].items||[];e.querySelectorAll('.it').forEach((q,j)=>{const o=its[j];q.style.opacity=ease(pr(t,C.T(o.at||0),.5));if(o.c2&&o.altAt!=null&&t>=C.T(o.altAt)){const ph=.5+.5*Math.cos((t-C.T(o.altAt))*(o.bf||6));q.querySelector('.ia').style.opacity=ph;q.querySelector('.ib').style.opacity=1-ph}})}
   if(N[i].kind==='crowd'){const cds=e.querySelectorAll('.cd'),gr=(N[i].grow||[{at:N[i].at||0,n:N[i].n||40}]);let cnt=0;for(const q of gr){cnt=lerp(cnt,q.n,ease(pr(t,C.T(q.at),q.dur||1.2)))}cds.forEach((d,j)=>d.style.opacity=clamp(cnt-j))}
   if(N[i].kind==='num'){const q=e.querySelector('.nm'),a=ease(pr(t,C.T(N[i].at||0),N[i].dur||2));q.textContent=(N[i].pre||'')+fmt(Math.round(lerp(N[i].from||0,N[i].n||0,a)))+(N[i].suf||'')}e.style.filter=on&&act?'drop-shadow(0 0 7px '+hex(N[i].color||'blue')+')':'none';if(N[i].glowAt!=null){const gg=ease(pr(t,C.T(N[i].glowAt),N[i].glowDur||8))*(.8+.2*Math.sin(t*7));e.style.filter=`drop-shadow(0 0 ${2+14*gg}px #FF6E6E) drop-shadow(0 0 ${12*gg}px #FF6E6E)`}});
  lk.forEach((e,i)=>{const on=!act||act.ids.includes(Lk[i].a)&&act.ids.includes(Lk[i].b);e.style.opacity=ease(pr(t,la[i],.5))*(on?1:.25)*(1-ease(pr(t,lu[i],.5)))*(Lk[i].alpha??1)});
  Lk.forEach((l,i)=>{const [a,b,q]=geo[i];if(l.orth||l.nob||t<la[i]+.4){pl[i].style.opacity=0;pl2[i].style.opacity=0;return}const sp=l.speed||.45,tt=t-la[i]-.4;
   [pl[i],pl2[i]].forEach((c,j)=>{const u=((tt*sp+j*.5)%1),w=(l.bi&&j)?1-u:u;const m=1-w;c.setAttribute('cx',m*m*a[0]+2*m*w*q[0]+w*w*b[0]);c.setAttribute('cy',m*m*a[1]+2*m*w*q[1]+w*w*b[1]);c.style.opacity=Math.sin(u*Math.PI)*.95*ease(pr(t,la[i]+.4,.4))*(1-ease(pr(t,lu[i],.5)))})});
  nd.forEach((e,i)=>{const vis=+e.style.opacity>.02;if(!vis)return;fitNode(e,N[i],!e._fd);e._fd=1});
  in2.forEach(e=>{const i=+e.dataset.i;e.style.opacity=ease(pr(t,ia[i],.6))})};
 upd.pos=id=>{const n=byId[id];if(!n)return[50,50];const [x,y]=ctr(n);return[x/9.6,y/5.4]};
 return upd};

/* ---------- driver ---------- */
window.CUES=[];
window.setup=(sched,cues)=>{
 const stage=document.getElementById('stage');stage.innerHTML='';window.CUES=[];
 const wpos=(r,w)=>{const tx=r.txt||'';const re=new RegExp('(^|[^A-Za-z0-9])'+w.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')+'(?![A-Za-z0-9])','i');const m=re.exec(tx);if(!m)throw new Error('word not found: '+w+' in '+tx.slice(0,50));const i=m.index+m[1].length;const wt=ch=>'.?!'.includes(ch)?7:',;:—'.includes(ch)?3.5:1;let a=0,b=0;for(let k=0;k<tx.length;k++){const x=wt(tx[k]);if(k<i)a+=x;b+=x}return r.s+(r.e-r.s)*(a/b)};
 const abs=spec=>{if(typeof spec==='number')return spec;const m=/^(>?)([SE]?\d+[a-z]?)(?:#(.+?))?([+-]\d+(?:\.\d+)?)?$/.exec(spec);if(!m)throw new Error('bad time '+spec);const r=sched[m[2]];if(r==null)throw new Error('unknown anchor '+spec);const base=m[3]?wpos(r,m[3].replace(/_/g,' ')):(m[1]?r.e:r.s);return base+(m[4]?parseFloat(m[4]):0)};
 cues.forEach((c,idx)=>{
  const start=abs(c.at)+(c.off||0);
  const ext=c.until!=null&&!/^E/.test(String(c.until))&&c.ext!==0?(c.ext??.45):0;
  const end=c.until!=null?abs(c.until)+(c.untilOff||0)+ext:start+c.dur;
  const el=mk('div','cue');const r=c.rect||[0,0,100,100];
  Object.assign(el.style,{left:r[0]+'%',top:r[1]+'%',width:r[2]+'%',height:r[3]+'%',zIndex:c.z||idx});
  const fx=c.fx||{},cm=c.cam&&c.cam.length;const st=mk('div','st'+(c.bg&&!cm?' bg':'')+(fx.bloom?' bloom':'')+(fx.vig&&!cm?' vig':''));
  const flr=fx.floor?`radial-gradient(120% 60% at 50% 108%,${hex(fx.floor)}55,transparent 70%),var(--ink)`:null;
  if(cm){const bgd=mk('div','st'+(c.bg?' bg':''));if(flr)bgd.style.background=flr;el.append(bgd)}   /* backdrop stays fixed while the camera moves the content */
  else if(flr)st.style.background=flr;
  st.dataset.c=1;el.append(st);if(cm&&fx.vig)el.append(mk('div','vgn'));stage.append(el);
  const C={dur:end-start,T:s=>typeof s==='number'?s:abs(s)-start};
  if(!A[c.a])throw new Error('unknown asset '+c.a);
  const upd=A[c.a](st,c.p||{},C);
  let cam=null;
  if(c.cam&&c.cam.length){cam=c.cam.map(k=>({t:abs(k.at)+(c.off||0),x:k.x,y:k.y,to:k.to,z:k.z??1,rx:k.rx??0,ry:k.ry??0,rot:k.rot??0,blur:k.blur??0,dur:k.dur}));el.style.perspective='1800px';st.style.overflow='visible'}
  window.CUES.push({el,st,cam,upd,start,end,fi:c.fade?.[0]??.5,fo:c.fade?.[1]??.5,id:c.id||c.a+idx})
 })};
window.frame=t=>{for(const q of window.CUES){
  if(t<q.start-.001||t>q.end+.001){q.el.style.opacity=0;q.el.style.visibility='hidden';continue}
  q.el.style.visibility='visible';const lt=t-q.start;
  q.el.style.opacity=Math.min(q.fi>0?clamp(lt/q.fi):1,q.fo>0?clamp((q.end-t)/q.fo):1);
  q.upd(lt);if(q.cam)applyCam(q,t)}};
const camAt=(q,t)=>{const K=q.cam,P=k=>{let x=k.x,y=k.y;if(k.to&&q.upd.pos){[x,y]=q.upd.pos(k.to)}return{x:x??50,y:y??50,z:k.z,rx:k.rx,ry:k.ry,rot:k.rot,blur:k.blur}};
 if(t<=K[0].t)return P(K[0]);for(let i=1;i<K.length;i++){if(t<=K[i].t){const a=P(K[i-1]),b=P(K[i]),e=K[i].t,d=Math.min(K[i].dur||2,e-K[i-1].t),u=eio(clamp((t-(e-d))/Math.max(.01,d)));const o={};for(const k in a)o[k]=k==='z'?Math.exp(lerp(Math.log(a.z),Math.log(b.z),u)):lerp(a[k],b[k],u);return o}}return P(K[K.length-1])};
const applyCam=(q,t)=>{const c=camAt(q,t);q.st.style.transformOrigin=c.x+'% '+c.y+'%';
 q.st.style.transform=`translate(${50-c.x}%,${50-c.y}%) scale(${c.z}) rotateX(${c.rx}deg) rotateY(${c.ry}deg) rotateZ(${c.rot}deg)`;
 q.st.style.filter=c.blur>.05?`blur(${c.blur}px)`:'none'};
