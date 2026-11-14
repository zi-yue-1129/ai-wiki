/* Original, deterministic toy calculations for bilingual EWC and NEAT pages. */
(() => {
  'use strict';
  const names = {
    en: { step:'Step',previous:'Previous',next:'Next',play:'Play',pause:'Pause',reset:'Reset',speed:'Speed',
      objective:'Toy calculation, not a trained model', scroll:'Scrollable calculation plot',
      eta:'Learning rate η',stiff:'High stiffness s',low:'Low stiffness s',
      ewcTitle:'Real gradient-descent steps', ewcExplanation:'These curves use discrete gradient descent, not the interpolation shown above. The stationary points do not change with η.',
      near:'High Fisher',far:'Low Fisher', weight:'Weight w',input:'Input x',activation:'Hidden activation',
      neatTitle:'Inspect one add-node mutation',neatExplanation:'Innovation IDs are illustrative. This timeline visualises the successive edits of one atomic mutation, not multiple generations.',
      initial:'Original edge #3 is enabled',disabled:'Old edge #3 is disabled but retained',
      inserted:'A hidden node is inserted',first:'New edge #8 (weight 1) is enabled',
      second:'New edge #9 (weight w) completes the new path',compare:'Compare original and split outputs',
      before:'Original output',after:'Split output',none:'not connected',delta:'Difference',
      accurate:'Identity activation preserves this toy linear function.',caution:'Nonlinear hidden activations need not preserve the original function.' },
    zh: { step:'步驟',previous:'上一步',next:'下一步',play:'播放',pause:'暫停',reset:'重設',speed:'速度',
      objective:'人工計算，並非訓練模型的實測值', scroll:'可水平捲動的計算圖',
      eta:'學習率 η',stiff:'高剛度 s',low:'低剛度 s',
      ewcTitle:'實際梯度下降迭代',ewcExplanation:'曲線來自離散梯度下降，不是上方動畫的插值；學習率 η 不會改變駐點位置。',
      near:'高 Fisher',far:'低 Fisher',weight:'權重 w',input:'輸入 x',activation:'隱藏節點活化函數',
      neatTitle:'檢查一次新增節點突變',neatExplanation:'創新編號均為人工示例。分鏡逐項檢查同一次原子性突變，不代表多個世代。',
      initial:'原始連結 #3 啟用',disabled:'停用 #3，但保留歷史基因',
      inserted:'插入新的隱藏節點',first:'啟用新連結 #8（權重 1）',
      second:'啟用新連結 #9（權重 w），新路徑完成',compare:'比較拆分前後的輸出',
      before:'原始輸出',after:'拆分後輸出',none:'尚未接通',delta:'差值',
      accurate:'使用恆等活化函數時，此人工線性路徑保留原函數。',caution:'非線性隱藏節點通常無法保證保留原函數。' }
  };
  const num = n => Number(n).toFixed(3);
  const esc = n => Math.round(n * 1000) / 1000;
  const coords = (x,y) => `${x.toFixed(1)},${y.toFixed(1)}`;
  function controller(host, max, render, t) {
    const prev=host.querySelector('[data-action=previous]'), next=host.querySelector('[data-action=next]');
    const play=host.querySelector('[data-action=play]'), reset=host.querySelector('[data-action=reset]');
    const seek=host.querySelector('[data-action=seek]'), velocity=host.querySelector('[data-action=speed]');
    let step=0,timer=null;
    const pause=()=>{ if(timer!==null){clearInterval(timer);timer=null;}play.textContent=t.play;play.setAttribute('aria-pressed','false'); };
    function show() { seek.value=String(step); prev.disabled=step===0; next.disabled=step===max; render(step); }
    function advance() { if(step>=max){pause();return;}step++;show(); if(step===max) pause(); }
    function start(){ if(timer!==null)return; if(step===max) step=0; show();timer=setInterval(advance,900/Number(velocity.value));play.textContent=t.pause;play.setAttribute('aria-pressed','true'); }
    prev.addEventListener('click',()=>{pause();step=Math.max(0,step-1);show();});
    next.addEventListener('click',()=>{pause();step=Math.min(max,step+1);show();});
    play.addEventListener('click',()=>timer===null?start():pause());
    reset.addEventListener('click',()=>{pause();step=0;host.querySelectorAll('[data-setting]').forEach(el=>{el.value=el.dataset.default;});show();});
    seek.addEventListener('input',()=>{pause();step=Number(seek.value);show();});
    velocity.addEventListener('change',()=>{if(timer!==null){pause();start();}});
    host.querySelectorAll('[data-setting]').forEach(x=>x.addEventListener('input',show));
    document.addEventListener('visibilitychange',()=>{if(document.hidden)pause();});
    const mq=window.matchMedia?.('(prefers-reduced-motion: reduce)');
    if(mq?.addEventListener)mq.addEventListener('change',e=>{if(e.matches)pause();});
    show();
  }
  const range = (id,text,min,max,step,value) => `<label class="en-lab-setting">${text} <output data-value="${id}">${value}</output><input data-setting="${id}" data-default="${value}" type="range" min="${min}" max="${max}" step="${step}" value="${value}"></label>`;
  function shell(title, settings, t, max, note){return `<section class="en-lab"><h4>${title}</h4><p class="en-lab-note">${note}</p><div class="en-lab-settings">${settings}</div><div class="en-lab-frame" tabindex="0" role="region" aria-label="${t.scroll}"><svg viewBox="0 0 620 260" role="img"></svg></div><output class="en-lab-results" aria-live="polite" aria-atomic="true"></output><div class="en-lab-controls"><button type="button" data-action="previous">${t.previous}</button><button type="button" data-action="play" aria-pressed="false">${t.play}</button><button type="button" data-action="next">${t.next}</button><label>${t.step} <input aria-label="${t.step}" type="range" data-action="seek" min="0" max="${max}" value="0" step="1"></label><label>${t.speed} <select data-action="speed"><option value="0.5">0.5×</option><option value="1" selected>1×</option><option value="2">2×</option></select></label><button type="button" data-action="reset">${t.reset}</button></div><p class="en-lab-disclaimer">${t.objective} · CC BY-SA 4.0</p></section>`;}
  function ewc(host,t){
    host.innerHTML=shell(t.ewcTitle,range('eta',t.eta,.02,.25,.01,.08)+range('high',t.stiff,1,5,.25,4)+range('low',t.low,.05,1.5,.05,.25),t,18,t.ewcExplanation);
    const svg=host.querySelector('svg'),output=host.querySelector('.en-lab-results');
    function render(k){
      const params=id=>{let v=Number(host.querySelector(`[data-setting=${id}]`).value);host.querySelector(`[data-value=${id}]`).textContent=v.toFixed(2);return v;};
      const eta=params('eta'),high=params('high'),low=params('low');
      const theta=(s,n)=>(1-Math.pow(1-eta*(1+s),n))/(1+s);
      const X=n=>52+n*29.2,Y=v=>211-(v+0.2)*155;
      let h=[],l=[];
      for(let i=0;i<=k;i++){h.push(coords(X(i),Y(theta(high,i))));l.push(coords(X(i),Y(theta(low,i))));}
      const grid=[0,.5,1].map(v=>`<path d="M52 ${Y(v)} H582" stroke="#d7e0e7"/><text x="44" y="${Y(v)+4}" text-anchor="end">${v.toFixed(1)}</text>`).join('');
      const ticks=[0,6,12,18].map(i=>`<text x="${X(i)}" y="235" text-anchor="middle">${i}</text>`).join('');
      const path=(a,c)=>`<polyline points="${a.join(' ')}" stroke="${c}" stroke-width="3.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/><circle cx="${X(k)}" cy="${Y(theta(c==='#256d94'?high:low,k))}" r="5.5" fill="${c}" stroke="white" stroke-width="2"/>`;
      svg.innerHTML=`<title>Discrete Fisher-weighted gradient descent, step ${k}</title><rect width="620" height="260" fill="#fff"/><g fill="#455a69" font-size="15" font-family="system-ui,sans-serif"><text x="52" y="18">θ</text>${grid}${ticks}<text x="582" y="252" text-anchor="end">step</text></g><path d="M52 27 V211 H582" stroke="#64798a" stroke-width="1.7" fill="none"/><path d="M52 ${Y(1/(1+high))} H582" stroke="#256d94" stroke-dasharray="3 7" opacity=".45"/><path d="M52 ${Y(1/(1+low))} H582" stroke="#ba713b" stroke-dasharray="3 7" opacity=".45"/>${path(h,'#256d94')}${path(l,'#ba713b')}`;
      output.textContent=`${t.step} ${k}/18 · ${t.near}: θ=${num(theta(high,k))} → θ*=${num(1/(1+high))} · ${t.far}: θ=${num(theta(low,k))} → θ*=${num(1/(1+low))}`;
    }
    controller(host,18,render,t);
  }
  function neat(host,t){
    const activation=`<label class="en-lab-setting">${t.activation}<select data-setting="activation" data-default="identity"><option value="identity">Identity</option><option value="tanh">tanh</option></select></label>`;
    host.innerHTML=shell(t.neatTitle,range('input',t.input,-1,1,.1,.8)+range('weight',t.weight,-2,2,.1,1.4)+activation,t,5,t.neatExplanation);
    const svg=host.querySelector('svg'),output=host.querySelector('.en-lab-results');
    const stages=['initial','disabled','inserted','first','second','compare'];
    function render(k){
      const get=id=>host.querySelector(`[data-setting=${id}]`).value;
      const x=Number(get('input')),w=Number(get('weight')),act=get('activation');
      host.querySelector('[data-value=input]').textContent=x.toFixed(1);host.querySelector('[data-value=weight]').textContent=w.toFixed(1);
      const original=x*w,after=w*(act==='identity'?x:Math.tanh(x));
      const disabled=k>=1, hidden=k>=2,first=k>=3,second=k>=4;
      const line=(x1,y1,x2,y2,c,dash='',label='')=>`<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${c}" stroke-width="5" ${dash?'stroke-dasharray="7 7"':''} stroke-linecap="round"/><text x="${(x1+x2)/2}" y="${(y1+y2)/2-15}" text-anchor="middle" fill="#334b5b" font-size="16">${label}</text>`;
      const circle=(x1,y1,label,active)=>`<circle cx="${x1}" cy="${y1}" r="25" fill="${active?'#d8edf7':'#f0f4f7'}" stroke="#315d76" stroke-width="2"/><text x="${x1}" y="${label==='Hidden'?166:y1+49}" text-anchor="middle" fill="#334b5b" font-size="15">${label}</text>`;
      svg.innerHTML=`<title>NEAT one add-node mutation, edit state ${k}</title><rect width="620" height="260" fill="#fff"/><rect x="19" y="18" width="582" height="224" rx="13" fill="#f7fafd" stroke="#d2e0e8"/><g font-family="system-ui,sans-serif">${line(160,125,460,125,disabled?'#aeb9c0':'#256d94',disabled,'#3')}${hidden&&first?line(172,117,285,72,'#1d8675','', '#8'):''}${hidden&&second?line(334,72,452,117,'#ba713b','', '#9'):''}${circle(135,125,'Input',true)}${circle(485,125,'Output',true)}${hidden?circle(310,63,'Hidden',true):''}<text x="34" y="217" fill="#465c6a" font-size="16">#3 ${disabled?'disabled':'enabled'}</text>${first?'<text x="275" y="217" fill="#1d8675" font-size="16">#8</text>':''}${second?'<text x="385" y="217" fill="#ba713b" font-size="16">#9</text>':''}</g>`;
      let message=`${t.step} ${k}/5 · ${t[stages[k]]} · ${t.before}: ${num(original)} · ${t.after}: ${second?num(after):t.none}`;
      if(second)message+=` · ${t.delta}: ${num(after-original)}. ${act==='identity'?t.accurate:t.caution}`;
      output.textContent=message;
    }
    controller(host,5,render,t);
  }
  function enhance(){
    document.querySelectorAll('[data-ewc-neat-lab]').forEach(host=>{
      if(host.dataset.enReady)return;
      const kind=host.dataset.ewcNeatLab;
      if(kind!=='ewc'&&kind!=='neat')return;
      host.dataset.enReady='true';
      const t=names[host.dataset.locale==='zh-TW'?'zh':'en'];
      if(kind==='ewc')ewc(host,t);else neat(host,t);
    });
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',enhance);else enhance();
  if(window.document$?.subscribe)window.document$.subscribe(enhance);
})();