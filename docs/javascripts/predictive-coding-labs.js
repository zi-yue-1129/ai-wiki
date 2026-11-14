/* Original AI Wiki teaching experiments; CC BY-SA 4.0. No external dependencies. */
(() => {
  'use strict';
  const copy = {
    en: {input:'Sensory input x', rate:'Correction step η', left:'Left endpoint a', right:'Right endpoint b',
      prediction:'Prediction', residual:'Residual', state:'Hidden state', energy:'Energy', errors:'Local errors',
      step:'Step', prev:'Previous', next:'Next', play:'Play', pause:'Pause', reset:'Reset', speed:'Speed',
      explanation:'Toy scalar dynamics, not neural recordings or a reproduction of the published model.',
      limit:'The step size controls oscillation and convergence; the dashed line is the fixed target.',
      settled:'Inference only: no synaptic weight update is performed in this laboratory.'},
    zh: {input:'感覺輸入 x', rate:'修正步長 η', left:'左端點 a', right:'右端點 b',
      prediction:'預測', residual:'殘差', state:'隱藏狀態', energy:'能量', errors:'局部誤差',
      step:'步驟', prev:'上一步', next:'下一步', play:'播放', pause:'暫停', reset:'重設', speed:'速度',
      explanation:'人工純量動態示例，不是神經記錄或原論文模型的數值重現。',
      limit:'步長決定是否振盪或收斂；虛線代表固定目標。',
      settled:'僅示範推論：本實驗不執行突觸權重更新。'}
  };
  const fmt = x => (Math.abs(x) < 0.0005 ? 0 : x).toFixed(3);
  const clamp = (x, a, b) => Math.max(a, Math.min(b, x));
  function init(root) {
    if (root.dataset.ready) return;
    root.dataset.ready = '1';
    const settling = root.dataset.lab === 'settling';
    const tr = copy[root.dataset.lang === 'zh' ? 'zh' : 'en'];
    let pos=0, speed=1, timer=null;
    const params = settling
      ? [{id:'a', label:tr.left, min:0,max:1,step:.05,value:.2},
         {id:'b', label:tr.right,min:0,max:1,step:.05,value:.8},
         {id:'eta',label:tr.rate,min:.1,max:.9,step:.05,value:.25}]
      : [{id:'x',label:tr.input,min:.1,max:1,step:.05,value:.85},
         {id:'eta',label:tr.rate,min:.1,max:1.3,step:.05,value:.55}];
    const inputs = params.map(p => `<label class="pc-param"><span>${p.label}: <output data-for="${p.id}">${fmt(p.value)}</output></span><input type="range" data-param="${p.id}" min="${p.min}" max="${p.max}" step="${p.step}" value="${p.value}"></label>`).join('');
    root.innerHTML = `<div class="pc-parameters">${inputs}</div>
      <div class="pc-scroll" role="region" tabindex="0" aria-label="${settling ? (root.dataset.lang === 'zh' ? '隱藏狀態與誤差的動態' : 'State and error dynamics') : (root.dataset.lang === 'zh' ? '預測與殘差的動態' : 'Prediction and residual dynamics')}">
        <svg class="pc-plot" viewBox="0 0 660 252" role="img" aria-label="${settling ? (root.dataset.lang === 'zh' ? '隱藏狀態接近端點平均值' : 'Hidden state approaching midpoint') : (root.dataset.lang === 'zh' ? '預測接近感覺輸入' : 'Prediction approaching input')}"></svg>
      </div><div class="pc-controls">
      <button type="button" data-action="prev">${tr.prev}</button><button type="button" data-action="toggle">${tr.play}</button>
      <button type="button" data-action="next">${tr.next}</button>
      <label class="pc-seek-label">${tr.step} <input aria-label="${tr.step}" type="range" data-seek min="0" max="8" step="1" value="0"></label>
      <label class="pc-speed-label">${tr.speed} <select data-speed aria-label="${tr.speed}"><option value="0.5">0.5×</option><option value="1" selected>1×</option><option value="2">2×</option></select></label>
      <button type="button" data-action="reset">${tr.reset}</button></div>
      <p class="pc-readout" aria-live="polite"></p><p class="pc-note">${tr.explanation} ${settling?tr.settled:tr.limit}</p>`;
    const $ = q => root.querySelector(q);
    const values = () => Object.fromEntries(params.map(p => [p.id, Number($(`[data-param="${p.id}"]`).value)]));
    const sequence = () => {
      const v = values(), target=settling ? (v.a+v.b)/2 : v.x;
      const states = [settling ? v.a : .25];
      for (let k=0;k<8;k++) {
        const z=states[k];
        const delta=settling ? (2*z-v.a-v.b) : (v.x-z);
        states.push(settling ? z-v.eta*delta : z+v.eta*delta);
      }
      return {states,target,v};
    };
    function stop() {if(timer!==null){window.clearInterval(timer);timer=null;} $('[data-action="toggle"]').textContent=tr.play;}
    function plot() {
      const {states,target,v}=sequence(), val=states[pos];
      const all=[...states,target];const lo=Math.min(...all)-.08, hi=Math.max(...all)+.08;
      const X=k=>47+k*70, Y=z=>208-(z-lo)/(hi-lo)*159;
      const points=states.map((s,k)=>`${X(k)},${Y(s).toFixed(2)}`).join(' ');
      const base=`<rect x="0" y="0" width="660" height="252" rx="14" fill="#f7fafc"/><path d="M47 29 V208 H620" fill="none" stroke="#9bb2bf" stroke-width="1.5"/>`;
      const grid=Array.from({length:9},(_,k)=>`<line x1="${X(k)}" x2="${X(k)}" y1="29" y2="208" stroke="#dde7ed"/><text x="${X(k)}" y="226" text-anchor="middle">${k}</text>`).join('');
      const ref=`<line x1="47" x2="607" y1="${Y(target)}" y2="${Y(target)}" stroke="#d18a36" stroke-width="2.2" stroke-dasharray="7 5"/><text x="605" y="${clamp(Y(target)-8,19,204)}" text-anchor="end" fill="#985f13">Target ${fmt(target)}</text>`;
      const current=`<line x1="${X(pos)}" x2="${X(pos)}" y1="29" y2="208" stroke="#a7bbc8" stroke-width="2" stroke-dasharray="4 4"/>`;
      const series=`<polyline points="${points}" fill="none" stroke="#087f8c" stroke-width="3.5" stroke-linejoin="round" stroke-linecap="round"/>`;
      const dots=states.map((s,k)=>`<circle cx="${X(k)}" cy="${Y(s)}" r="${k===pos?7:3.8}" fill="${k===pos?'#e07940':'#087f8c'}" stroke="#fff" stroke-width="1.5"/>`).join('');
      const legend=`<text x="49" y="18" fill="#087f8c">${settling?'State z':'Prediction'}</text><text x="605" y="245" text-anchor="end">Step</text>`;
      $('.pc-plot').innerHTML=`${base}${grid}${ref}${current}${series}${dots}${legend}`;
      $('[data-seek]').value=String(pos);
      for(const p of params) $(`[data-for="${p.id}"]`).textContent=fmt(v[p.id]);
      const measure=settling ? `${tr.state} z=${fmt(val)} · ${tr.errors}: eₐ=${fmt(val-v.a)}, eᵦ=${fmt(val-v.b)} · ${tr.energy} E=${fmt(.5*((val-v.a)**2+(val-v.b)**2))}`
        : `${tr.prediction} p=${fmt(val)} · ${tr.residual} e=x−p=${fmt(v.x-val)}`;
      $('.pc-readout').textContent=`${tr.step} ${pos}/8 · ${measure}`;
    }
    root.querySelectorAll('[data-param]').forEach(el=>el.addEventListener('input',()=>{stop();pos=0;plot();}));
    $('[data-seek]').addEventListener('input',e=>{stop();pos=Number(e.target.value);plot();});
    $('[data-speed]').addEventListener('change',e=>{speed=Number(e.target.value);if(timer!==null){stop();start();}});
    root.querySelectorAll('button[data-action]').forEach(button=>button.addEventListener('click',()=>{
      const a=button.dataset.action;
      if(a==='toggle'){if(timer!==null)stop();else start();return;}
      stop();if(a==='reset'){params.forEach(p=>$(`[data-param="${p.id}"]`).value=p.value);pos=0;speed=1;$('[data-speed]').value='1';}
      if(a==='next')pos=Math.min(8,pos+1);if(a==='prev')pos=Math.max(0,pos-1);plot();
    }));
    function start(){if(timer!==null)return;if(pos===8)pos=0;
      timer=window.setInterval(()=>{pos=Math.min(8,pos+1);plot();if(pos===8)stop();},600/speed);
      $('[data-action="toggle"]').textContent=tr.pause;
    }
    document.addEventListener('visibilitychange',()=>{if(document.hidden)stop();});
    plot();
  }
  const activate=()=>document.querySelectorAll('.pc-lab[data-lab]').forEach(init);
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',activate);
  else activate();
  if(typeof window.document$!=='undefined' && window.document$.subscribe)window.document$.subscribe(activate);
})();