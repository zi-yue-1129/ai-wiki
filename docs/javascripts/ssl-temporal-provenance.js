/* CC BY-SA 4.0 — deterministic teaching views of MoCo queue lifetime and
 * BYOL EMA source attribution. Values are schematic, never measured features.
 * The existing lab owns all controls; these views never start their own timer.
 */
(() => {
  'use strict';
  const initial = ['A','B','C','D','E','F'];
  const arrivals = ['G','H','I'];
  const clamp = (x,lo,hi,otherwise) => Number.isFinite(x) ? Math.max(lo,Math.min(hi,x)) : otherwise;
  const pct = x => (100*x).toFixed(1)+'%';
  const ageColors = ['#1c7c80','#39999b','#68b3b0','#9acbc4','#c3ddd7','#e2eeea'];
  const sources = [
    {name:'T0',color:'#4c648a'},
    {name:'Q1',color:'#2b91a1'},
    {name:'Q2',color:'#d49b49'},
    {name:'Q3',color:'#a77ab0'}
  ];
  const svgStart = label => `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 270" role="img" aria-label="${label}"><rect x="1" y="1" width="638" height="268" rx="12" fill="#f8fbfd" stroke="#b6cbd5"/>`;
  function queueState(step) {
    return [...initial,...arrivals].slice(step,step+6);
  }
  function queueGraphic(step) {
    let svg=svgStart('MoCo FIFO: active negative-key dictionary before and after three enqueues');
    svg+=`<text x="22" y="30" class="ssl-temporal-title">FIFO window</text><text x="618" y="30" text-anchor="end" class="ssl-temporal-small">oldest → newest</text>`;
    for(let row=0;row<4;row++) {
      const active=row===step, y=49+row*49;
      if(active) svg+=`<rect x="12" y="${y-5}" width="616" height="46" rx="9" fill="#e6f2f4" stroke="#17808a" stroke-width="2"/>`;
      svg+=`<text x="22" y="${y+23}" class="ssl-temporal-row">${row}</text>`;
      const keys=queueState(row);
      for(let i=0;i<6;i++){
        const x=68+i*92, age=5-i;
        svg+=`<rect x="${x}" y="${y}" width="77" height="34" rx="7" fill="${ageColors[age]}" stroke="#829ba6" stroke-width=".8"/>`;
        svg+=`<text x="${x+38.5}" y="${y+23}" text-anchor="middle" class="ssl-temporal-token">${keys[i]}</text>`;
      }
    }
    svg+=`<path d="M69 248 H606" stroke="#b5c9d0" stroke-width="2"/><path d="M599 242 L607 248 L599 254" fill="none" stroke="#b5c9d0" stroke-width="2"/><text x="22" y="252" class="ssl-temporal-small">FIFO</text></svg>`;
    return svg;
  }
  function coefficients(m,step) {
    const out=[m**step];
    for(let i=1;i<=3;i++)out.push(i<=step ? (1-m)*m**(step-i) : 0);
    return out;
  }
  function historyGraphic(m,step) {
    let svg=svgStart('BYOL EMA: coefficients of initial target and successive online weights');
    svg+=`<text x="22" y="30" class="ssl-temporal-title">EMA source weights</text><text x="618" y="30" text-anchor="end" class="ssl-temporal-small">Σ weights = 1</text>`;
    for(let row=0;row<4;row++) {
      const active=row===step, y=52+row*46;
      if(active)svg+=`<rect x="12" y="${y-5}" width="616" height="43" rx="9" fill="#e6f2f4" stroke="#17808a" stroke-width="2"/>`;
      svg+=`<text x="23" y="${y+23}" class="ssl-temporal-row">${row}</text>`;
      let x=67;
      const values=coefficients(m,row);
      values.forEach((v,i)=>{
        if(v<=0) return;
        const w=536*v;
        svg+=`<rect x="${x.toFixed(3)}" y="${y}" width="${w.toFixed(3)}" height="31" fill="${sources[i].color}"/>`;
        if(w>48) svg+=`<text x="${(x+w/2).toFixed(2)}" y="${y+21}" text-anchor="middle" class="ssl-temporal-pct">${pct(v)}</text>`;
        x+=w;
      });
      svg+=`<rect x="67" y="${y}" width="536" height="31" rx="2" fill="none" stroke="#7797a6" stroke-width="1"/>`;
    }
    sources.forEach((s,i)=>{
      const x=68+i*132;
      svg+=`<rect x="${x}" y="246" width="13" height="13" rx="2" fill="${s.color}"/><text x="${x+19}" y="257" class="ssl-temporal-small">${s.name}</text>`;
    });
    svg+='</svg>';
    return svg;
  }
  function render(host, kind, zh, chart, readout) {
    const seek=host.querySelector('[data-act="seek"]');
    const momentum=host.querySelector('[data-act="momentum"]');
    if(!seek||!momentum) return;
    const frame=Math.round(clamp(Number(seek.value),0,14,0));
    const m=clamp(Number(momentum.value),0.5,0.99,0.9);
    const turn=Math.floor(frame/5), phase=frame%5;
    if(kind==='moco') {
      // Current loss uses the PRE-enqueue dictionary. Only the fifth phase
      // advances the FIFO window; the newly encoded positive key is not a
      // negative for its own current contrastive objective.
      const step=turn+(phase===4?1:0);
      chart.innerHTML=queueGraphic(step);
      const queue=queueState(step).join(' ');
      readout.textContent=zh
        ? `已完成入列 ${step}/3 次 · 目前負樣本 [${queue}] · ${phase===4?'本輪新鍵已入列':'本輪新鍵尚未入列'}`
        : `${step}/3 enqueues complete · negatives [${queue}] · ${phase===4?'new key enqueued':'new key not yet enqueued'}`;
    } else {
      // Target EMA is a discrete operation AFTER online SGD, not a loss
      // gradient. T_t=m^t*T_0+(1-m)*sum_{i=1}^t m^(t-i)*Q_i.
      const step=turn+(phase===4?1:0);
      const c=coefficients(m,step);
      chart.innerHTML=historyGraphic(m,step);
      readout.textContent=zh
        ? `EMA 已更新 ${step}/3 次 · 初始目標貢獻 ${pct(c[0])} · 線上歷史貢獻 ${pct(1-c[0])} · 係數和 100%`
        : `${step}/3 EMA updates · initial target ${pct(c[0])} · online history ${pct(1-c[0])} · coefficient sum 100%`;
    }
  }
  function enhance(){
    document.querySelectorAll('[data-self-supervised-lab]').forEach(host=>{
      if(host.dataset.temporalProvenanceReady) return;
      const kind=host.dataset.selfSupervisedLab;
      if(kind!=='moco'&&kind!=='byol')return;
      const compute=host.querySelector('.ssl-compute');
      const seek=host.querySelector('[data-act="seek"]');
      const momentum=host.querySelector('[data-act="momentum"]');
      if(!compute||!seek||!momentum)return;
      host.dataset.temporalProvenanceReady='yes';
      const zh=host.dataset.locale==='zh-TW';
      const section=document.createElement('section');
      section.className='ssl-temporal-provenance';
      const heading=document.createElement('div');heading.className='ssl-temporal-heading';
      heading.textContent=kind==='moco'
        ?(zh?'負樣本佇列的時間窗口':'Negative dictionary across time')
        :(zh?'EMA 歷史參數來源':'EMA historical contributions');
      const chart=document.createElement('div');chart.className='ssl-temporal-chart';
      const readout=document.createElement('output');readout.className='ssl-temporal-readout';
      readout.setAttribute('aria-live','off');
      const note=document.createElement('p');note.className='ssl-temporal-note';
      note.textContent=kind==='moco'
        ?(zh?'每一列是初始狀態或一次入列後的六格 FIFO 快照；反白列與主播放器同步。最左側是最舊的鍵。字母及位置只代表示意的佇列年齡，不能推算實際嵌入漂移或負樣本難度。'
          :'Rows show the initial six-slot FIFO and the snapshots after each enqueue; the highlighted row follows playback. Oldest keys are on the left. Letters and positions indicate illustrative queue age, not measured embedding drift or negative hardness.')
        :(zh?'每一列將目標權重拆成初始目標 T0 與歷次線上權重 Q1–Q3 的 EMA 係數。反白列只在 EMA 步驟後前進；調整動量會重新分配貢獻。這不是模型實測權重或梯度。'
          :'Each row decomposes the target into its initial weight T0 and online snapshots Q1–Q3. The highlighted row advances only after EMA; momentum redistributes contributions. These are not measured weights or gradients.');
      section.append(heading,chart,readout,note);
      compute.after(section);
      const update=()=>render(host,kind,zh,chart,readout);
      seek.addEventListener('input',update);
      momentum.addEventListener('input',update);
      // The main player mutates its computation text during autoplay; native
      // input events are not fired when it changes the seek value in code.
      new MutationObserver(update).observe(compute,{childList:true,characterData:true,subtree:true});
      update();
    });
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',enhance);
  else enhance();
  if(window.document$&&typeof window.document$.subscribe==='function')window.document$.subscribe(enhance);
})();
