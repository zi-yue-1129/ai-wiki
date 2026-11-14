/* Deterministic, explanatory ViViT and I3D model-mechanism labs. Original CC BY-SA 4.0. */
(() => {
  'use strict';
  const NS = 'http://www.w3.org/2000/svg';
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)');
  const T = 3, P = 4, W = [1, -1, 0.5, 0.5], X = [2, 1, 3, 2];
  const labels = {
    en: { prev:'Previous', next:'Next', play:'Play', pause:'Pause', reset:'Reset',
      step:'Stage', speed:'Speed', frame:'Query frame', patch:'Query patch',
      impulse:'Middle-frame change', spatial:'Spatial', temporal:'Temporal', reach:'Reachable',
      total:'Direct attention pairs', reference:'Unfactorised pairs', selected:'Selected keys',
      sample:'2D response', sum:'Accumulated', final:'Inflated 3D response',
      explainV:'Orange: within a frame. Teal: same spatial position across frames. At the final stage, all tokens can influence a query indirectly through the two operations.',
      explainI:'The same fixed 2D filter is repeated at 1/3 scale at each time position. A change to one pixel of the middle frame breaks the constant-video equality.',
      note:'Synthetic illustration — pair counts are not FLOPs and responses are not measured activations.' },
    zh: { prev:'上一步', next:'下一步', play:'播放', pause:'暫停', reset:'重設',
      step:'階段', speed:'速度', frame:'查詢影格', patch:'查詢區塊',
      impulse:'中間影格擾動', spatial:'空間', temporal:'時間', reach:'間接可達',
      total:'直接注意力配對', reference:'未分解配對', selected:'可關注鍵數',
      sample:'二維響應', sum:'目前累加', final:'膨脹後三維響應',
      explainV:'橘色為同影格空間混合，青綠色為跨影格同位置混合。兩步完成後，所有詞元可以間接影響目前的查詢詞元。',
      explainI:'相同二維濾波器沿時間複製三次，每次縮放為三分之一。中間影格任一像素的擾動會破壞恆定影片的響應相等性。',
      note:'人工示意：配對數不是 FLOPs，響應不是模型量測的激活值。' }
  };
  const fmt = x => (Math.abs(x) < 1e-10 ? 0 : x).toFixed(3);
  const dot = (a,b) => a.reduce((s,x,i)=>s+x*b[i],0);
  const attr = (v) => String(v).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/"/g,'&quot;');
  function setup(node) {
    if(node.dataset.ready==='true') return;
    const kind=node.dataset.lab, lang=(node.dataset.lang==='zh'?'zh':'en'), l=labels[lang];
    if(kind!=='vivit' && kind!=='i3d') return;
    node.dataset.ready='true';
    let stage=0, frame=1, patch=1, delta=0, speed=1, timer=null;
    const max=kind==='vivit'?2:3;
    node.innerHTML=`<div class="val-controls"><button type="button" data-op="prev">${l.prev}</button><button type="button" data-op="play">${l.play}</button><button type="button" data-op="next">${l.next}</button><label>${l.step} <input data-op="seek" type="range" min="0" max="${max}" step="1" value="0"></label><label>${l.speed} <select data-op="speed"><option value="0.5">0.5×</option><option value="1" selected>1×</option><option value="2">2×</option></select></label><button type="button" data-op="reset">${l.reset}</button></div><div class="val-parameters">${kind==='vivit'?`<label>${l.frame} <input data-op="frame" type="range" min="1" max="3" value="2"><output data-out="frame">2</output></label><label>${l.patch} <input data-op="patch" type="range" min="1" max="4" value="2"><output data-out="patch">2</output></label>`:`<label>${l.impulse} <input data-op="delta" type="range" min="-2" max="2" step="0.25" value="0"><output data-out="delta">0.00</output></label>`}</div><div class="val-scroll" tabindex="0" role="region" aria-label="${lang==='zh'?'可水平捲動的教學示意圖':'Horizontally scrollable teaching visual'}"><div data-out="drawing"></div></div><div class="val-readout" data-out="values" role="status" aria-live="polite"></div><p class="val-explain">${kind==='vivit'?l.explainV:l.explainI}</p><p class="val-note">${l.note}</p>`;
    const qs=(a)=>node.querySelector(`[data-op="${a}"]`), out=(a)=>node.querySelector(`[data-out="${a}"]`);
    function stop(){if(timer!==null){window.clearInterval(timer);timer=null;}}
    function drawViViT(){
      const pts=[]; for(let t=0;t<T;t++)for(let p=0;p<P;p++)pts.push({t,p,x:116+t*235+(p%2)*59,y:112+Math.floor(p/2)*64});
      const source=pts[frame*P+patch];
      const keys=pts.filter(q=>stage===0?q.t===frame:stage===1?q.p===patch:true);
      let lines='',cells='';
      for(const q of keys){const c=(q.t===frame?'#e28b46':'#239eaa');if(stage<2){lines+=`<line x1="${source.x+21}" y1="${source.y+18}" x2="${q.x+21}" y2="${q.y+18}" stroke="${c}" stroke-width="2.5" stroke-opacity="0.55"/>`;}}
      for(const q of pts){let hit=keys.includes(q),isQ=q===source;cells+=`<rect x="${q.x}" y="${q.y}" width="42" height="36" rx="7" fill="${isQ?'#f4c66b':hit?((stage===1||stage===2&&q.t!==frame)?'#a0dadd':'#f5d3b9'):'#e9edf3'}" stroke="${isQ?'#bb7324':hit?'#627e91':'#bcc4d0'}" stroke-width="${isQ?3:1}"/><text x="${q.x+21}" y="${q.y+23}" text-anchor="middle" font-size="13" font-weight="600" fill="#233049">${q.p+1}</text>`;}
      const titles=Array.from({length:T},(_,t)=>`<text x="${158+t*235}" y="78" text-anchor="middle" font-size="16" fill="#345">T${t+1}</text>`).join('');
      const stageLabel=['Spatial','Temporal','Reachable'][stage];
      out('drawing').innerHTML=`<svg xmlns="${NS}" viewBox="0 0 760 275" width="760" role="img" aria-label="Factorised video token connectivity at stage ${stage+1}"><rect width="760" height="275" rx="14" fill="#f8fafc"/><text x="24" y="34" font-size="19" font-weight="700" fill="#253c52">ViViT · ${attr(stageLabel)}</text><text x="735" y="34" text-anchor="end" font-size="13" fill="#476071">T=3 · P=4</text>${titles}${lines}${cells}<circle cx="${source.x+21}" cy="${source.y+18}" r="29" fill="none" stroke="#df7840" stroke-width="2.8" stroke-dasharray="5 4"/><text x="380" y="244" text-anchor="middle" font-size="13" fill="#425b6c">${stage===0?'T × P² = 48':stage===1?'P × T² = 36':'48 + 36 = 84'}</text></svg>`;
      out('values').textContent=`${l.step}: ${stage+1}/3 · ${l.selected}: ${keys.length}/${T*P} · ${l.total}: ${stage===0?48:stage===1?36:84} · ${l.reference}: 144`;
    }
    function drawI3D(){
      const responses=Array.from({length:T},(_,t)=>dot(W,X)+(t===1?W[0]*delta:0));
      const part=responses.map(r=>r/3);
      const sum=part.slice(0,stage).reduce((a,b)=>a+b,0);
      let panes='', bars='';
      for(let t=0;t<T;t++){
        const cx=84+t*225;let cells='';
        for(let i=0;i<4;i++){const value=X[i]+(t===1&&i===0?delta:0);cells+=`<rect x="${cx+(i%2)*55}" y="${87+Math.floor(i/2)*49}" width="48" height="43" rx="6" fill="${t===1&&i===0&&delta!==0?'#f8c4a0':'#d4e6f2'}" stroke="#9bb1c5"/><text x="${cx+24+(i%2)*55}" y="${113+Math.floor(i/2)*49}" text-anchor="middle" font-size="13" fill="#264157">${fmt(value)}</text>`;}
        panes+=`<text x="${cx+52}" y="67" text-anchor="middle" font-size="17" fill="#345">T${t+1}</text>${cells}<text x="${cx+52}" y="210" text-anchor="middle" font-size="14" fill="#254a60">${fmt(part[t])}</text>`;
        const start=cx+25; const height=Math.max(2,Math.min(45,Math.abs(part[t])*34)); bars+=`<rect x="${start}" y="${265-height}" width="54" height="${height}" rx="4" fill="${t<stage?'#319da8':'#c7d8e0'}"/>`;
      }
      out('drawing').innerHTML=`<svg xmlns="${NS}" viewBox="0 0 760 306" width="760" role="img" aria-label="Inflated 3D convolution over three time slices"><rect width="760" height="306" rx="14" fill="#f8fafc"/><text x="24" y="33" font-size="18" font-weight="700" fill="#253c52">I3D · W/3</text><text x="735" y="33" font-size="13" fill="#476071" text-anchor="end">W=[1,-1,0.5,0.5]</text>${panes}<line x1="48" y1="265" x2="710" y2="265" stroke="#9ab2c3"/>${bars}<text x="380" y="294" text-anchor="middle" font-size="14" fill="#425b6c">Σ = ${fmt(sum)}</text></svg>`;
      out('values').textContent=`${l.step}: ${stage}/3 · ${l.sample}: ${fmt(dot(W,X))} · ${l.sum}: ${fmt(sum)} · ${l.final}: ${fmt(part.reduce((a,b)=>a+b,0))}`;
    }
    function render(){qs('seek').value=String(stage);qs('play').textContent=timer===null?l.play:l.pause;if(kind==='vivit'){out('frame').textContent=String(frame+1);out('patch').textContent=String(patch+1);drawViViT();}else{out('delta').textContent=delta.toFixed(2);drawI3D();}}
    function advance(){stage=(stage+1)%(max+1);render();}
    function play(){if(timer!==null){stop();render();return;} timer=window.setInterval(advance,1100/speed);render();}
    qs('prev').addEventListener('click',()=>{stop();stage=Math.max(0,stage-1);render()});
    qs('next').addEventListener('click',()=>{stop();stage=Math.min(max,stage+1);render()});
    qs('play').addEventListener('click',play);
    qs('seek').addEventListener('input',e=>{stop();stage=Number(e.target.value);render()});
    qs('speed').addEventListener('change',e=>{speed=Number(e.target.value);if(timer!==null){stop();play()}});
    qs('reset').addEventListener('click',()=>{stop();stage=0;frame=1;patch=1;delta=0;speed=1;qs('speed').value='1';if(kind==='vivit'){qs('frame').value='2';qs('patch').value='2';}else qs('delta').value='0';render()});
    if(kind==='vivit'){qs('frame').addEventListener('input',e=>{frame=Number(e.target.value)-1;render()});qs('patch').addEventListener('input',e=>{patch=Number(e.target.value)-1;render()});}
    else qs('delta').addEventListener('input',e=>{delta=Number(e.target.value);render()});
    document.addEventListener('visibilitychange',()=>{if(document.hidden){stop();render();}});
    reduce.addEventListener?.('change',()=>{if(reduce.matches){stop();render();}});
    render();
  }
  function enhance(){document.querySelectorAll('.video-arch-lab').forEach(setup);}
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',enhance);else enhance();
  window.document$?.subscribe?.(enhance);
})();