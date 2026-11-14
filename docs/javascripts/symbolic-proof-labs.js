/* Deterministic, bilingual, accessible teaching simulations.
 * No dependencies, storage, network requests, or inline event handlers.
 * These labs enhance (never replace) GitHub-compatible static SVG figures.
 */
(() => {
  'use strict';
  const media = window.matchMedia('(prefers-reduced-motion: reduce)');
  const translations = {
    en: {
      idaTitle: 'IDA*: inspect every DFS decision',
      resTitle: 'Resolution: eliminate complementary literals',
      previous: 'Previous', next: 'Next', play: 'Play', pause: 'Pause', reset: 'Reset',
      timeline: 'Step', speed: 'Speed', bound: 'f-bound', iteration: 'Iteration',
      visits: 'Examined', repeat: 'Revisits', stack: 'Current path',
      threshold: 'Next cutoff', decision: 'Decision',
      expand: 'Expand: within the bound', cutoff: 'Cut off: f exceeds the bound',
      goal: 'Goal reached', nextBound: 'Raise the bound to the minimum cutoff',
      start: 'Begin a depth-first iteration', path: 'Path',
      idaIntro: 'The same nodes are examined again when the bound rises. Cut-off nodes are tested, not expanded.',
      resIntro: 'Select each inference to inspect the complementary pair and its resolvent. The empty clause proves the initial clauses inconsistent.',
      premises: 'Parent clauses', pivot: 'Eliminated pivot', resolvent: 'Resolvent',
      noResult: 'No derived clause yet', result: 'Empty clause: contradiction',
      proof: 'Proof progress', initial: 'Initial clauses only',
      explanation: 'The complementary literals cancel; the remaining literals form the resolvent.',
      completed: 'All three resolution inferences complete',
      status: 'Current simulation state'
    },
    zh: {
      idaTitle: 'IDA*：逐步檢視 DFS 決策',
      resTitle: '歸結：消去互補文字',
      previous: '上一步', next: '下一步', play: '播放', pause: '暫停', reset: '重設',
      timeline: '步驟', speed: '速度', bound: 'f 上界', iteration: '迭代輪次',
      visits: '檢查次數', repeat: '重訪次數', stack: '目前路徑',
      threshold: '下次截斷值', decision: '目前決策',
      expand: '展開：未超過上界', cutoff: '截斷：f 超過上界',
      goal: '找到目標', nextBound: '將上界提高至最小截斷值',
      start: '開始新一輪深度優先搜尋', path: '路徑',
      idaIntro: '上界提高後，同一批節點會再次被檢查。被截斷節點僅進行門檻檢查，不會展開子節點。',
      resIntro: '逐步檢視互補文字及產生的歸結子句。推導出空子句即代表初始子句合取不可滿足。',
      premises: '父子句', pivot: '消去文字', resolvent: '歸結子句',
      noResult: '尚未推導子句', result: '空子句：產生矛盾',
      proof: '證明進度', initial: '尚未進行歸結',
      explanation: '消去兩個互補文字，並合併剩餘文字，得到新的子句。',
      completed: '已完成三次歸結',
      status: '目前模擬狀態'
    }
  };
  const nodes = [
    {id:'S', f:4, x:80, y:126, children:['A','B']},
    {id:'A', f:6, x:240, y:71, children:['C','D']},
    {id:'B', f:8, x:240, y:213, children:['E']},
    {id:'C', f:7, x:407, y:49, children:['G']},
    {id:'D', f:10, x:407, y:148, children:[]},
    {id:'E', f:9, x:407, y:251, children:[]},
    {id:'G', f:8, x:569, y:49, children:[]}
  ];
  const byId = Object.fromEntries(nodes.map(n => [n.id,n]));
  const bounds = [4,6,7,8];

  function buildIdaSteps() {
    const steps=[];
    let examined=0, revisits=0;
    const seen=new Set();
    for (let iteration=0; iteration<bounds.length; iteration++) {
      const bound=bounds[iteration];
      let smallestCutoff=Infinity;
      let found=false;
      steps.push({kind:'start',iteration,bound,node:null,path:[],examined,revisits,smallestCutoff:null});
      function walk(id,path) {
        if(found) return;
        const n=byId[id];
        examined++;
        if(seen.has(id)) revisits++; else seen.add(id);
        const currentPath=[...path,id];
        const kind=n.f>bound?'cutoff':id==='G'?'goal':'expand';
        if(kind==='cutoff') smallestCutoff=Math.min(smallestCutoff,n.f);
        if(kind==='goal') found=true;
        steps.push({kind,iteration,bound,node:id,path:currentPath,examined,revisits,
          smallestCutoff:Number.isFinite(smallestCutoff)?smallestCutoff:null});
        if(kind==='expand') for(const child of n.children) walk(child,currentPath);
      }
      walk('S',[]);
      if(found) break;
      if(iteration<bounds.length-1) {
        if(smallestCutoff!==bounds[iteration+1]) throw new Error('IDA* next threshold mismatch');
        steps.push({kind:'nextBound',iteration,bound,node:null,path:[],examined,revisits,smallestCutoff});
      }
    }
    if(steps[steps.length-1].kind!=='goal' || steps[steps.length-1].path.join('')!=='SACG') {
      throw new Error('IDA* goal path mismatch');
    }
    return steps;
  }
  const idaSteps=buildIdaSteps();

  const original = [['P','Q'],['¬P','R'],['¬Q'],['¬R']];
  const proof = [
    {left:original[0],right:original[1],pivot:'P'},
    {left:['Q','R'],right:original[2],pivot:'Q'},
    {left:['R'],right:original[3],pivot:'R'}
  ];
  function resolve(left,right,pivot) {
    const a=left.includes(pivot), b=right.includes('¬'+pivot);
    const c=left.includes('¬'+pivot), d=right.includes(pivot);
    if(!((a&&b)||(c&&d))) throw new Error('Not a complementary pair');
    return [...new Set([...left,...right].filter(x=>x!==pivot && x!=='¬'+pivot))];
  }
  const proofResults=proof.map(p=>resolve(p.left,p.right,p.pivot));
  if(JSON.stringify(proofResults)!==JSON.stringify([['Q','R'],['R'],[]])) throw new Error('Invalid resolution proof');

  const formatClause = xs => xs.length ? xs.join(' ∨ ') : '□';
  const h = (tag,cls,txt) => {
    const el=document.createElement(tag);
    if(cls) el.className=cls;
    if(txt!==undefined) el.textContent=txt;
    return el;
  };

  function controls(root,total,language,render) {
    const t=translations[language];
    let index=0, speed=1, timer=null;
    const nav=h('div','sp-lab-controls');
    const back=h('button','sp-lab-btn',t.previous);
    const toggle=h('button','sp-lab-btn sp-lab-primary',t.play);
    const forward=h('button','sp-lab-btn',t.next);
    const reset=h('button','sp-lab-btn',t.reset);
    [back,toggle,forward,reset].forEach(b=>{b.type='button';nav.append(b);});
    const line=h('label','sp-lab-label');line.append(document.createTextNode(t.timeline+' '));
    const seek=h('input','sp-lab-seek');seek.type='range';seek.min='0';seek.max=String(total-1);seek.step='1';seek.value='0';
    seek.setAttribute('aria-label',t.timeline);line.append(seek);
    const counter=h('output','sp-lab-counter');line.append(counter);nav.append(line);
    const speedWrap=h('label','sp-lab-label',t.speed+' ');
    const select=h('select','sp-lab-select');select.setAttribute('aria-label',t.speed);
    for(const s of [0.5,1,2]) {const o=h('option',null,`${s}×`);o.value=String(s);if(s===1)o.selected=true;select.append(o);}
    speedWrap.append(select);nav.append(speedWrap);root.append(nav);
    function stop(){if(timer!==null){window.clearInterval(timer);timer=null;}toggle.textContent=t.play;}
    function draw(){seek.value=String(index);counter.textContent=`${index+1} / ${total}`;back.disabled=index===0;forward.disabled=index===total-1;
      render(index); if(index===total-1) stop();}
    function tick(){if(!root.isConnected || index+1>=total)stop();else{index++;draw();}}
    function play(){if(timer!==null){stop();return;}
      if(index>=total-1)index=0;
      toggle.textContent=t.pause;draw();timer=window.setInterval(tick,Math.round(1000/speed));}
    back.addEventListener('click',()=>{stop();index=Math.max(0,index-1);draw();});
    forward.addEventListener('click',()=>{stop();index=Math.min(total-1,index+1);draw();});
    reset.addEventListener('click',()=>{stop();index=0;draw();});
    toggle.addEventListener('click',play);
    seek.addEventListener('input',()=>{stop();index=Number(seek.value);draw();});
    select.addEventListener('change',()=>{const wasPlaying=timer!==null;stop();speed=Number(select.value);if(wasPlaying)play();});
    const onHidden=()=>{if(document.hidden||!root.isConnected)stop();};
    document.addEventListener('visibilitychange',onHidden);
    media.addEventListener?.('change',e=>{if(e.matches)stop();});
    draw();
    return {stop};
  }

  function setupIda(root,language){
    const t=translations[language];
    const figure=h('div','sp-lab-figure sp-ida-canvas');figure.tabIndex=0;figure.setAttribute('role','region');figure.setAttribute('aria-label',language==='zh'?'可水平捲動的搜尋樹':'Scrollable search tree');root.append(figure);
    const detail=h('div','sp-lab-metrics');root.append(detail);
    const live=h('p','sp-lab-live');live.setAttribute('role','status');live.setAttribute('aria-live','polite');root.append(live);
    const graph=nodes.map(n=>`<g class="sp-node" data-node="${n.id}" transform="translate(${n.x} ${n.y})"><circle r="24"/><text class="sp-node-id" text-anchor="middle" y="5">${n.id}</text><text class="sp-node-score" text-anchor="middle" y="42">f=${n.f}</text></g>`).join('');
    const edges=nodes.flatMap(n=>n.children.map(id=>{
      const target=byId[id];return `<line class="sp-ida-edge" x1="${n.x}" y1="${n.y}" x2="${target.x}" y2="${target.y}"/>`;
    })).join('');
    figure.innerHTML=`<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 680 305" role="img" aria-label="IDA star search tree"><title>IDA* toy search tree</title><g>${edges}</g><g>${graph}</g></svg>`;
    const bound=h('div','sp-lab-metric');const iteration=h('div','sp-lab-metric');const visits=h('div','sp-lab-metric');
    const revisit=h('div','sp-lab-metric');const cutoff=h('div','sp-lab-metric');const stack=h('div','sp-lab-metric sp-lab-wide');
    [bound,iteration,visits,revisit,cutoff,stack].forEach(x=>detail.append(x));
    controls(root,idaSteps.length,language,i=>{
      const s=idaSteps[i];
      for(const n of figure.querySelectorAll('.sp-node')){
        const id=n.getAttribute('data-node');
        n.classList.toggle('sp-on-path',s.path.includes(id));
        n.classList.toggle('sp-current',id===s.node);
        n.classList.toggle('sp-cut',id===s.node && s.kind==='cutoff');
        n.classList.toggle('sp-found',id===s.node && s.kind==='goal');
      }
      bound.innerHTML=`<small>${t.bound}</small><strong>${s.bound}</strong>`;
      iteration.innerHTML=`<small>${t.iteration}</small><strong>${s.iteration+1} / ${bounds.length}</strong>`;
      visits.innerHTML=`<small>${t.visits}</small><strong>${s.examined}</strong>`;
      revisit.innerHTML=`<small>${t.repeat}</small><strong>${s.revisits}</strong>`;
      cutoff.innerHTML=`<small>${t.threshold}</small><strong>${s.smallestCutoff??'—'}</strong>`;
      stack.innerHTML=`<small>${t.stack}</small><strong>${s.path.join(' → ')||'—'}</strong>`;
      const decision=s.node ? `${s.node} · f=${byId[s.node].f}` : `f≤${s.bound}`;
      live.textContent=`${t.decision}: ${t[s.kind]} · ${decision}.`;
    });
  }
  function proofChip(clause,pivot){
    const chip=h('div','sp-clause');
    if(!clause.length){chip.textContent='□';chip.classList.add('sp-clause-empty');return chip;}
    clause.forEach((lit,i)=>{
      if(i)chip.append(document.createTextNode(' ∨ '));
      const span=h('span',lit===pivot || lit==='¬'+pivot?'sp-pivot':'',lit);chip.append(span);
    });return chip;
  }
  function setupResolution(root,language){
    const t=translations[language];
    const figure=h('div','sp-lab-figure sp-resolution-canvas');root.append(figure);
    const progress=h('div','sp-proof-progress');root.append(progress);
    const live=h('p','sp-lab-live');live.setAttribute('role','status');live.setAttribute('aria-live','polite');root.append(live);
    controls(root,4,language,i=>{
      figure.replaceChildren();
      const labels=h('div','sp-res-labels');
      [t.premises,t.pivot,t.resolvent].forEach(s=>labels.append(h('span',null,s)));
      figure.append(labels);
      const main=h('div','sp-res-row');figure.append(main);
      if(i===0){
        const init=h('div','sp-init-clauses');
        original.forEach(c=>init.append(proofChip(c,'')));
        main.append(init);main.append(h('div','sp-res-arrow','→'));
        main.append(h('div','sp-res-outcome',t.noResult));
        live.textContent=t.initial;
      }else{
        const p=proof[i-1];const left=h('div','sp-res-parents');
        left.append(proofChip(p.left,p.pivot));left.append(proofChip(p.right,p.pivot));
        main.append(left);
        const pivot=h('div','sp-res-pivot',p.pivot+' / ¬'+p.pivot);main.append(pivot);
        const final=proofResults[i-1];main.append(proofChip(final,''));
        live.textContent=i===3?t.completed:`${t.explanation} ${formatClause(final)}.`;
      }
      progress.replaceChildren();
      proof.forEach((p,j)=>{
        const row=h('div','sp-proof-step'+(j<i?' sp-proof-done':'')+(j===i-1?' sp-proof-now':''));
        row.append(h('span','sp-proof-badge',String(j+1)));
        row.append(h('span','sp-proof-equation',`${formatClause(p.left)}  +  ${formatClause(p.right)}  ⇒  ${formatClause(proofResults[j])}`));
        progress.append(row);
      });
    });
  }
  function enhance(root=document){
    for(const box of root.querySelectorAll('[data-aiwiki-lab]')){
      if(box.dataset.enhanced==='yes')continue;
      const which=box.dataset.aiwikiLab;
      if(which!=='ida'&&which!=='resolution')continue;
      const language=box.dataset.lang==='zh-TW'?'zh':'en';
      const t=translations[language];
      const outer=h('section','sp-lab');
      const title=h('h4','sp-lab-title',which==='ida'?t.idaTitle:t.resTitle);
      const intro=h('p','sp-lab-intro',which==='ida'?t.idaIntro:t.resIntro);
      outer.append(title,intro);
      if(which==='ida')setupIda(outer,language);else setupResolution(outer,language);
      box.replaceChildren(outer);box.dataset.enhanced='yes';
    }
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',()=>enhance());
  else enhance();
  if(window.document$?.subscribe)window.document$.subscribe(()=>enhance());
})();