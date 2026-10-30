/* Deterministic, bilingual GPipe/ZeRO teaching explorations. No external dependencies.
 * GitHub retains the chapter's original SVG fallback when scripts are unavailable.
 */
(() => {
  'use strict';
  const motion = window.matchMedia('(prefers-reduced-motion: reduce)');
  const labels = {
    en: {stages:'Stages', batches:'Micro-batches', play:'Play', pause:'Pause', prev:'Previous step', next:'Next step', reset:'Reset', speed:'Speed', slot:'Slot', idle:'Idle slots', active:'Completed operations', schematic:'Illustrative equal-duration slots; not measured GPU utilisation.', ranks:'Ranks', stage:'ZeRO stage', baseline:'Replicated', current:'Per rank', saved:'Model-state saving', memory:'Bytes per parameter per rank', caveat:'Model state only; excludes activations and temporary buffers.', live:'Current step'},
    zh: {stages:'管線階段', batches:'微批次', play:'播放', pause:'暫停', prev:'上一步', next:'下一步', reset:'重設', speed:'速度', slot:'時槽', idle:'閒置比例', active:'已完成運算', schematic:'等長時槽的教學示意，非實測 GPU 使用率。', ranks:'裝置數', stage:'ZeRO 階段', baseline:'未分片', current:'每裝置', saved:'模型狀態節省', memory:'每裝置、每參數位元組', caveat:'僅模型狀態，不含激活值與暫時緩衝區。', live:'目前步驟'}
  };
  const create = (tag, className, text) => {
    const node = document.createElement(tag);
    if (className) node.className = className;
    if (text !== undefined) node.textContent = text;
    return node;
  };
  const clamp = (n, a, b) => Math.max(a, Math.min(b, n));
  function slider(label, min, max, value, onChange) {
    const wrap = create('label', 'dex-field');
    const head = create('span', 'dex-field-head');
    const title = create('span', '', label), out = create('output', 'dex-field-value', String(value));
    head.append(title, out);
    const input = create('input'); input.type = 'range';
    input.min = String(min); input.max = String(max); input.value = String(value);
    input.setAttribute('aria-label', label);
    input.addEventListener('input', () => { out.textContent = input.value; onChange(Number(input.value)); });
    wrap.append(head, input);
    return {wrap, input, out};
  }
  function button(label, text, handler) {
    const b = create('button', 'dex-button', text);
    b.type = 'button'; b.setAttribute('aria-label', label); b.addEventListener('click', handler);
    return b;
  }
  function initGpipe(host, L) {
    let k = 3, m = 4, step = 0, playing = false, raf = 0, previous = 0, fraction = 0;
    const panel = create('div', 'dex-panel');
    const fields = create('div', 'dex-fields');
    const plot = create('div', 'dex-plot');
    const grid = create('div', 'dex-schedule');
    const stats = create('div', 'dex-stats');
    const controls = create('div', 'dex-controls');
    const status = create('output', 'dex-time'); status.setAttribute('aria-live', 'off');
    const help = create('p', 'dex-note', L.schematic);
    const stageField = slider(L.stages, 2, 6, k, v => { k=v; stop(); step=0; render(); });
    const batchField = slider(L.batches, 1, 12, m, v => { m=v; stop(); step=0; render(); });
    fields.append(stageField.wrap, batchField.wrap);
    const back = button(L.prev, '←', () => {stop(); step=clamp(step-1,0,total());render();});
    const play = button(L.play, '▶', () => {
      if (motion.matches) return;
      if (playing) stop(); else {if(step>=total()){step=0;render();} playing=true;previous=0;fraction=0;raf=requestAnimationFrame(tick);}
      renderControls();
    });
    const next = button(L.next, '→', () => {stop();step=clamp(step+1,0,total());render();});
    const reset = button(L.reset, '↺', () => {stop();step=0;render();});
    const rate = create('select', 'dex-rate'); rate.setAttribute('aria-label', L.speed);
    for(const value of [0.5,1,2]) {const opt=create('option','',value+'×');opt.value=String(value);if(value===1)opt.selected=true;rate.append(opt);}
    controls.append(back,play,next,reset,status,rate);
    plot.append(grid); panel.append(fields,plot,stats,controls,help);host.append(panel);
    function total(){return 2*(k+m-1);}
    function stop(){playing=false;cancelAnimationFrame(raf);raf=0;previous=0;fraction=0;renderControls();}
    function tick(now){
      if(!playing) return;
      if(previous) fraction+=(now-previous)/650*Number(rate.value);
      previous=now;
      if(fraction>=1){const advances=Math.floor(fraction);fraction-=advances;step=clamp(step+advances,0,total());render();}
      if(step>=total()){stop();return;}
      raf=requestAnimationFrame(tick);
    }
    function renderControls(){play.textContent=playing?'Ⅱ':'▶';play.setAttribute('aria-label',playing?L.pause:L.play);play.disabled=motion.matches;back.disabled=step===0;next.disabled=step===total();status.textContent=L.slot+' '+step+' / '+total();}
    function render(){
      const t=total(), f=k+m-1;
      grid.replaceChildren();grid.style.gridTemplateColumns='52px repeat('+t+', 34px)';
      grid.append(create('span','dex-grid-label','GPU'));
      for(let s=0;s<t;s++)grid.append(create('span','dex-tick'+(s===step?' dex-now':''),String(s+1)));
      for(let row=0;row<k;row++){
        grid.append(create('span','dex-grid-label','S'+(row+1)));
        for(let s=0;s<t;s++){
          let kind='idle', index='';
          if(s<f){const b=s-row;if(b>=0&&b<m){kind='forward';index=b+1;}}
          else {const b=m-1-(s-f-(k-1-row));if(b>=0&&b<m){kind='backward';index=b+1;}}
          const cell=create('span','dex-cell dex-'+kind+(s<step?' dex-done':' dex-future')+(s===step?' dex-now':''),kind==='idle'?'':(kind==='forward'?'F':'B')+index);
          cell.title=kind==='idle'?'Idle':kind+' micro-batch '+index;
          grid.append(cell);
        }
      }
      const bubble=(k-1)/(m+k-1);
      const finished=[...grid.querySelectorAll('.dex-cell.dex-done:not(.dex-idle)')].length;
      stats.replaceChildren(create('span','',L.idle+': '+(bubble*100).toFixed(1)+'%'),create('span','',L.active+': '+finished+' / '+(2*k*m)));
      renderControls();
    }
    const onReduce=()=>{if(motion.matches)stop();renderControls();};motion.addEventListener('change',onReduce);
    const cleanup=new MutationObserver(()=>{if(host.isConnected)return;stop();cleanup.disconnect();motion.removeEventListener('change',onReduce);});cleanup.observe(document.body,{childList:true,subtree:true});
    render();
  }
  function initZero(host,L){
    let ranks=2, stage=0, playing=false, timer=0;
    const panel=create('div','dex-panel');
    const fields=create('div','dex-fields');
    const rankField=slider(L.ranks,2,16,ranks,v=>{ranks=v;render();});
    const stageField=slider(L.stage,0,3,stage,v=>{stop();stage=v;render();});
    fields.append(rankField.wrap,stageField.wrap);
    const plot=create('div','dex-memory');
    const legend=create('div','dex-legend');
    for(const [name,cls] of [['P','dex-p'],['G','dex-g'],['O','dex-o']]){const item=create('span','dex-legend-item');item.append(create('i',cls),document.createTextNode(name));legend.append(item);}
    const stats=create('div','dex-stats');
    const controls=create('div','dex-controls');
    const back=button(L.prev,'←',()=>{stop();stage=clamp(stage-1,0,3);sync();});
    const play=button(L.play,'▶',()=>{if(motion.matches)return;if(playing)stop();else {if(stage===3){stage=0;sync();}playing=true;tick();}renderControls();});
    const next=button(L.next,'→',()=>{stop();stage=clamp(stage+1,0,3);sync();});
    const reset=button(L.reset,'↺',()=>{stop();stage=0;sync();});
    const status=create('output','dex-time');status.setAttribute('aria-live','off');
    controls.append(back,play,next,reset,status);
    panel.append(fields,plot,legend,stats,controls,create('p','dex-note',L.caveat));host.append(panel);
    function stop(){playing=false;clearTimeout(timer);timer=0;renderControls();}
    function tick(){if(!playing)return;timer=setTimeout(()=>{stage++;sync();if(stage===3)stop();else tick();},1100);}
    function sync(){stageField.input.value=String(stage);stageField.out.textContent=String(stage);render();}
    function renderControls(){play.textContent=playing?'Ⅱ':'▶';play.setAttribute('aria-label',playing?L.pause:L.play);play.disabled=motion.matches;back.disabled=stage===0;next.disabled=stage===3;status.textContent=(stage===0?'DP':'S'+stage)+' · N='+ranks;}
    function makeBar(title,parts){
      const line=create('div','dex-memory-row');
      const head=create('div','dex-memory-head');head.append(create('span','',title),create('strong','',parts.reduce((a,b)=>a+b,0).toFixed(2)+' B'));
      const track=create('div','dex-memory-track');track.setAttribute('role','img');track.setAttribute('aria-label',title+' '+parts.map((n,i)=>['P','G','O'][i]+' '+n.toFixed(2)+' bytes').join(', '));
      parts.forEach((n,i)=>{const part=create('span',['dex-p','dex-g','dex-o'][i]);part.style.width=(n/16*100)+'%';track.append(part);});
      line.append(head,track);return line;
    }
    function render(){
      const p=stage>=3?2/ranks:2, g=stage>=2?2/ranks:2, o=stage>=1?12/ranks:12;
      const total=p+g+o;
      plot.replaceChildren(makeBar(L.baseline,[2,2,12]),makeBar(L.current,[p,g,o]));
      stats.replaceChildren(create('span','',L.memory+': '+total.toFixed(2)+' B'),create('span','',L.saved+': '+((1-total/16)*100).toFixed(1)+'%'));
      renderControls();
    }
    const onReduce=()=>{if(motion.matches)stop();renderControls();};motion.addEventListener('change',onReduce);
    const cleanup=new MutationObserver(()=>{if(host.isConnected)return;stop();cleanup.disconnect();motion.removeEventListener('change',onReduce);});cleanup.observe(document.body,{childList:true,subtree:true});
    render();
  }
  function enhance(){
    for(const host of document.querySelectorAll('.distributed-explorer[data-explorer]')){
      if(host.dataset.ready==='yes')continue;
      const lang=host.dataset.lang==='zh'?'zh':'en', L=labels[lang];
      if(host.dataset.explorer==='gpipe')initGpipe(host,L);
      else if(host.dataset.explorer==='zero')initZero(host,L);
      else continue;
      host.dataset.ready='yes';
      const fallback = host.previousElementSibling;
      if (fallback?.tagName === 'P' && fallback.querySelector('img[src*="-still.svg"]')) fallback.hidden = true;
    }
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',enhance);else enhance();
  if(window.document$?.subscribe)window.document$.subscribe(enhance);
})();
