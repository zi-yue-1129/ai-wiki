/* SAC / DPO quantitative teaching laboratories. Original CC BY-SA 4.0.
 * No network calls or user-provided HTML. Pages keep their SVG fallback without JS.
 */
(() => {
  'use strict';
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)');
  const P = {
    en: {play:'Play',pause:'Pause',previous:'Previous',next:'Next',reset:'Reset',speed:'Speed',alpha:'Temperature α',gap:'Q gap',pref:'Preferred policy probability',reference:'Reference preferred probability',beta:'DPO β',posterior:'Computed values',weight:'Probability',entropy:'Entropy',expected:'Expected Q',soft:'Soft objective',margin:'Reference-relative margin',loss:'DPO loss',referenceLabel:'Reference',policyLabel:'Policy',preferred:'Preferred',rejected:'Rejected',value:'Value',illustration:'Illustrative analytical values, not model measurements.',scroll:'Scroll to inspect the full illustration',progress:'Playback progress'},
    zh: {play:'播放',pause:'暫停',previous:'上一步',next:'下一步',reset:'重設',speed:'速度',alpha:'溫度 α',gap:'Q 值間距',pref:'偏好回應的策略機率',reference:'偏好回應的參考機率',beta:'DPO β',posterior:'即時計算結果',weight:'機率',entropy:'熵',expected:'期望 Q',soft:'軟目標',margin:'相對參考模型差距',loss:'DPO 損失',referenceLabel:'參考模型',policyLabel:'目前策略',preferred:'偏好',rejected:'拒絕',value:'數值',illustration:'數值為解析式人工示例，並非模型實測。',scroll:'可水平捲動觀看完整圖面',progress:'播放進度'}
  };
  const svg = (s) => `<svg viewBox="0 0 720 272" role="img" aria-label="${s}" xmlns="http://www.w3.org/2000/svg"></svg>`;
  const clamp = (x,lo,hi) => Math.max(lo,Math.min(hi,x));
  const round = (v,n=3) => Number(v).toFixed(n);
  const scale = (x,a,b) => a + x*(b-a);
  const NS='http://www.w3.org/2000/svg';
  function el(name,attrs={},text='') { const e=document.createElementNS(NS,name); for(const [k,v] of Object.entries(attrs))e.setAttribute(k,String(v));if(text)e.textContent=text;return e; }
  function line(plot,x1,y1,x2,y2,cls){plot.append(el('line',{x1,y1,x2,y2,class:cls}));}
  function txt(plot,x,y,str,cls,anchor='start'){plot.append(el('text',{x,y,class:cls,'text-anchor':anchor},String(str)));}
  function init(root) {
    if(root.dataset.sacDpoReady === '1')return;
    root.dataset.sacDpoReady='1';
    const kind=root.dataset.sacDpoLab;
    if(kind!=='sac' && kind!=='dpo') return;
    const t=P[root.dataset.lang==='zh-TW'?'zh':'en'];
    const initial=kind==='sac'?{alpha:2,gap:1}:{pref:0.5,reference:0.5,beta:1};
    const state={...initial};
    const spec=kind==='sac'?
      [['alpha',0.2,3,0.1,t.alpha],['gap',0.25,2.5,0.25,t.gap]]:
      [['pref',0.1,0.9,0.02,t.pref],['reference',0.2,0.8,0.05,t.reference],['beta',0.2,2,0.1,t.beta]];
    root.innerHTML=`<div class="sd-head"><span class="sd-name">${kind==='sac'?'SAC · Soft policy':'DPO · Preference margin'}</span><span class="sd-flag">ANALYTICAL DEMO</span></div><div class="sd-params"></div><div class="sd-scroll" role="region" tabindex="0" aria-label="${t.scroll}">${svg(kind==='sac'?'Softmax policy probabilities and analytical entropy':'Reference versus policy probabilities and DPO logistic loss')}</div><div class="sd-readouts" role="status" aria-live="polite" aria-atomic="true"></div><div class="sd-controls"><button type="button" data-act="previous">◀ ${t.previous}</button><button type="button" data-act="play">▶ ${t.play}</button><button type="button" data-act="next">${t.next} ▶</button><label class="sd-seeklabel">${t.progress}<input type="range" data-act="seek" min="0" max="20" step="1" value="0"/></label><label class="sd-speedlabel">${t.speed}<select data-act="speed"><option value="0.5">0.5×</option><option value="1" selected>1×</option><option value="2">2×</option></select></label><button type="button" data-act="reset">↺ ${t.reset}</button></div><p class="sd-note">${t.illustration}</p>`;
    const params=root.querySelector('.sd-params'),plot=root.querySelector('svg'),read=root.querySelector('.sd-readouts');
    for(const [key,min,max,step,label] of spec){
      const holder=document.createElement('label');holder.className='sd-param';
      const title=document.createElement('span');title.textContent=label;
      const val=document.createElement('output');val.dataset.for=key;
      const slider=document.createElement('input');slider.type='range';slider.min=min;slider.max=max;slider.step=step;slider.value=state[key];slider.dataset.param=key;
      holder.append(title,val,slider);params.append(holder);
      slider.addEventListener('input',()=>{state[key]=Number(slider.value);stop();render();});
    }
    const play=root.querySelector('[data-act="play"]'),seek=root.querySelector('[data-act="seek"]'),speed=root.querySelector('[data-act="speed"]');
    let interval=null,position=kind==='sac'?7:10;
    seek.value=position;
    play.disabled=reduced.matches;
    const key=kind==='sac'?'alpha':'pref';
    const setPosition=(idx)=>{
      position=clamp(idx,0,20);
      state[key]=kind==='sac' ? +(3-position*0.14).toFixed(2) : +(0.1+position*0.04).toFixed(2);
      root.querySelector(`[data-param="${key}"]`).value=state[key];
      seek.value=position;render();
    };
    function stop(){if(interval!==null){window.clearInterval(interval);interval=null;}play.textContent=`▶ ${t.play}`;play.setAttribute('aria-pressed','false');}
    function advance(){if(position===20)position=-1;setPosition(position+1);}
    function start(){if(reduced.matches)return;stop();interval=window.setInterval(()=>{if(!root.isConnected || document.hidden){stop();return;}advance();},700/Number(speed.value));play.textContent=`Ⅱ ${t.pause}`;play.setAttribute('aria-pressed','true');}
    function redrawAxes(){plot.replaceChildren();plot.append(el('rect',{x:0,y:0,width:720,height:272,rx:12,class:'sd-canvas'}));}
    function renderSac(){
      const q=[2*state.gap,state.gap,0],a=state.alpha;
      const x=q.map(v=>Math.exp((v-q[0])/a)),z=x.reduce((s,v)=>s+v,0),p=x.map(v=>v/z);
      const H=-p.reduce((s,v)=>s+v*Math.log(v),0), eq=p.reduce((s,v,i)=>s+v*q[i],0);
      const objective=eq+a*H;
      redrawAxes();
      txt(plot,24,28,'π(a | s)', 'sd-title');txt(plot,425,28,'H(π) / α','sd-title');
      for(let i=0;i<3;i++){
        const y=67+i*62,w=p[i]*245;
        plot.append(el('rect',{x:85,y:y-23,width:245,height:29,rx:6,class:'sd-track'}));
        plot.append(el('rect',{x:85,y:y-23,width:w,height:29,rx:6,class:`sd-bar sd-action-${i}`}));
        txt(plot,24,y-2,`A${i+1}`,'sd-axis');txt(plot,342,y-3,round(p[i]),'sd-number');
        txt(plot,85,y+23,`Q${i+1} = ${round(q[i],2)}`,'sd-small');
      }
      const xx=440,yy=222,W=240,Hh=164;
      line(plot,xx,yy,xx+W,yy,'sd-grid');line(plot,xx,yy-Hh,xx,yy,'sd-grid');
      for(let i=0;i<=2;i++){const v=i*.5; const yy2=yy-v/1.15*Hh;line(plot,xx,yy2,xx+W,yy2,'sd-grid-light');txt(plot,xx-8,yy2+3,String(v.toFixed(1)),'sd-small','end');}
      let d='';for(let k=0;k<=80;k++){const aa=0.2+(2.8*k/80), v=q.map(e=>Math.exp((e-q[0])/aa)),s=v.reduce((u,x)=>u+x,0),h=-v.reduce((u,e)=>{let pp=e/s;return u+pp*Math.log(pp);},0);const px=xx+W*k/80,py=yy-h/1.15*Hh;d+=`${k?'L':'M'}${px.toFixed(2)},${py.toFixed(2)} `;}
      plot.append(el('path',{d,class:'sd-curve'}));
      const px=xx+W*(a-0.2)/2.8,py=yy-H/1.15*Hh;
      line(plot,px,py,px,yy,'sd-dash');plot.append(el('circle',{cx:px,cy:py,r:6,class:'sd-dot'}));
      txt(plot,xx+W/2,252,'α','sd-axis','middle');
      txt(plot,xx,238,'0.2','sd-small');txt(plot,xx+W,238,'3.0','sd-small','end');
      read.innerHTML=`<span><small>${t.entropy} H (nats)</small><strong data-value="entropy">${round(H)}</strong></span><span><small>${t.expected}</small><strong data-value="expected">${round(eq)}</strong></span><span><small>${t.soft} E[Q]+αH</small><strong data-value="soft">${round(objective)}</strong></span>`;
    }
    function renderDpo(){
      const p=state.pref,r=state.reference,beta=state.beta;
      const margin=Math.log(p/(1-p))-Math.log(r/(1-r)),logit=beta*margin;
      const loss=Math.log1p(Math.exp(-logit));
      redrawAxes();
      txt(plot,24,28,'P(y | x)','sd-title');txt(plot,423,28,'−log σ(βΔ)','sd-title');
      const rows=[[r,1-r,'Ref'],[p,1-p,'π']];
      rows.forEach(([w,l,name],i)=>{
        const y=85+i*89;txt(plot,24,y-20,name,'sd-axis');
        plot.append(el('rect',{x:89,y:y-40,width:265,height:32,rx:6,class:'sd-track'}));
        plot.append(el('rect',{x:89,y:y-40,width:265*w,height:32,rx:6,class:'sd-bar sd-action-0'}));
        plot.append(el('rect',{x:89+265*w,y:y-40,width:265*l,height:32,rx:6,class:'sd-bar sd-action-2'}));
        txt(plot,89,y+11,`Win ${round(w)}  ·  Lose ${round(l)}`,'sd-small');
      });
      const xx=440, yy=226,W=241,Hh=168;
      line(plot,xx,yy,xx+W,yy,'sd-grid');line(plot,xx,yy-Hh,xx,yy,'sd-grid');
      let d='';for(let k=0;k<=100;k++){
        const pp=0.1+0.8*k/100,m=Math.log(pp/(1-pp))-Math.log(r/(1-r));
        const v=Math.log1p(Math.exp(-beta*m));
        const px=xx+W*k/100,py=yy-clamp(v/4,0,1)*Hh;
        d+=`${k?'L':'M'}${px.toFixed(1)},${py.toFixed(1)} `;
      }
      plot.append(el('path',{d,class:'sd-curve'}));
      const px=xx+W*(p-0.1)/0.8,py=yy-clamp(loss/4,0,1)*Hh;
      line(plot,px,py,px,yy,'sd-dash');plot.append(el('circle',{cx:px,cy:py,r:6,class:'sd-dot'}));
      txt(plot,xx+W/2,254,'π(Win)','sd-axis','middle');txt(plot,xx,241,'0.1','sd-small');txt(plot,xx+W,241,'0.9','sd-small','end');
      txt(plot,xx-7,yy-168+4,'4.0','sd-small','end');
      read.innerHTML=`<span><small>${t.margin} Δ</small><strong data-value="margin">${round(margin)}</strong></span><span><small>βΔ</small><strong data-value="betaMargin">${round(logit)}</strong></span><span><small>${t.loss} (nats)</small><strong data-value="loss">${round(loss)}</strong></span>`;
    }
    function render(){for(const [k] of spec)root.querySelector(`[data-for="${k}"]`).textContent=round(state[k],2);kind==='sac'?renderSac():renderDpo();}
    root.querySelector('[data-act="previous"]').addEventListener('click',()=>{stop();setPosition(position-1);});
    root.querySelector('[data-act="next"]').addEventListener('click',()=>{stop();setPosition(position+1);});
    play.addEventListener('click',()=>{if(interval!==null)stop();else start();});
    seek.addEventListener('input',()=>{stop();setPosition(Number(seek.value));});
    speed.addEventListener('change',()=>{if(interval!==null)start();});
    root.querySelector('[data-act="reset"]').addEventListener('click',()=>{stop();Object.assign(state,initial);position=kind==='sac'?7:10;seek.value=position;for(const [k] of spec)root.querySelector(`[data-param="${k}"]`).value=state[k];render();});
    document.addEventListener('visibilitychange',()=>{if(document.hidden)stop();});
    reduced.addEventListener?.('change',e=>{if(e.matches)stop();play.disabled=e.matches;});
    render();
  }
  const enhance=()=>document.querySelectorAll('[data-sac-dpo-lab]').forEach(init);
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',enhance);else enhance();
  if(window.document$?.subscribe) window.document$.subscribe(enhance);
})();
