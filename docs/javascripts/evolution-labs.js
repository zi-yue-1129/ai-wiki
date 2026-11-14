/* Interactive evolutionary algorithm demonstrations. All values are synthetic. */
(() => {
  'use strict';
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)');
  const A = '11011010', B = '00100101';
  const initial = [
    {x: 1, y: 0, fitness: 0.46},
    {x: 4, y: 1, fitness: 0.70},
    {x: 0, y: 3, fitness: 0.55},
  ];
  const words = {
    en: {previous: 'Previous', next: 'Next', play: 'Play', pause: 'Pause', reset: 'Reset',
      speed: 'Speed', step: 'Step', cut: 'Crossover cut', flip: 'Mutation bit',
      rival: 'Challenger fitness', elite: 'Replacement fitness', copy: 'Copied bits',
      child: 'Child', mutated: 'Mutated', coverage: 'Coverage', quality: 'Archive quality sum',
      status: 'Event', no: 'Initial archive', added: 'Insert', rejected: 'Reject', replaced: 'Replace',
      start: 'Start with two parents', inheritA: 'Copy from parent A', inheritB: 'Copy from parent B',
      flipBit: 'Flip a single child bit', accepted: 'Accepted', progress: 'Progress',
      gaHelp: 'Each step copies exactly one bit from the chosen parent. The last step flips one bit.',
      mapHelp: 'Each candidate competes only with the existing elite in its descriptor cell.',
      hypothetical: 'Illustrative values; not an experimental run.'},
    zh: {previous: '上一步', next: '下一步', play: '播放', pause: '暫停', reset: '重設',
      speed: '速度', step: '步驟', cut: '交叉切點', flip: '突變位元',
      rival: '挑戰者適應度', elite: '取代者適應度', copy: '已複製位元',
      child: '子代', mutated: '突變後', coverage: '覆蓋率', quality: '檔案庫品質總和',
      status: '事件', no: '初始檔案庫', added: '插入', rejected: '拒絕', replaced: '取代',
      start: '從兩個親代開始', inheritA: '從親代 A 複製', inheritB: '從親代 B 複製',
      flipBit: '翻轉子代的一個位元', accepted: '接受', progress: '進度',
      gaHelp: '每一步只從指定親代複製一個位元，最後一步翻轉指定的子代位元。',
      mapHelp: '每個候選解只會與描述子對應格內的菁英比較適應度。',
      hypothetical: '所有數值均為人工示意，非演算法實測。'},
  };
  function create(tag, className, textContent) {
    const x = document.createElement(tag);
    if (className) x.className = className;
    if (textContent !== undefined) x.textContent = String(textContent);
    return x;
  }
  function buildSlider(root, label, min, max, step, initialValue, changed) {
    const group = create('label', 'evo-slider');
    const top = create('span', 'evo-slider-head');
    top.append(create('span', '', label));
    const valueLabel = create('output', 'evo-slider-value', initialValue);
    top.append(valueLabel);
    const slider = create('input');
    slider.type = 'range'; slider.min = String(min); slider.max = String(max);
    slider.step = String(step); slider.value = String(initialValue);
    slider.setAttribute('aria-label', label);
    group.append(top, slider);
    root.append(group);
    slider.addEventListener('input', () => {
      valueLabel.textContent = slider.value;
      changed(Number(slider.value));
    });
    return {slider, valueLabel, initialValue};
  }
  function board(root, lang, maxStep, stepChanged) {
    let step = 0, timer = null, intervalMs = 850, speed = 1;
    const bar = create('div', 'evo-timeline');
    const back = create('button', '', lang.previous), next = create('button', '', lang.next);
    const play = create('button', '', lang.play), reset = create('button', '', lang.reset);
    const seek = create('input'); seek.type = 'range'; seek.min = '0';
    seek.max = String(maxStep); seek.value = '0'; seek.step = '1';
    seek.setAttribute('aria-label', lang.progress);
    const speedButton = create('button', '', `${lang.speed}: 1×`);
    const status = create('span', 'evo-step-status');
    status.setAttribute('aria-live', 'polite'); status.setAttribute('role', 'status');
    [back, next, play, reset, speedButton].forEach(button => {button.type = 'button';});
    bar.append(back, play, next, seek, speedButton, reset);
    root.append(bar, status);
    let updated = () => {};
    function halt() { if (timer !== null) {window.clearInterval(timer); timer = null;} play.textContent = lang.play; }
    function setStep(v) {
      step = Math.max(0, Math.min(maxStep, Number(v)));
      seek.value = String(step); back.disabled = step === 0; next.disabled = step === maxStep;
      status.textContent = `${lang.step} ${step}/${maxStep}`;
      updated();
      if (step === maxStep) halt();
    }
    function tick() {if (step >= maxStep) halt(); else setStep(step + 1);}
    function start() {
      halt();
      if (step === maxStep) setStep(0);
      timer = window.setInterval(tick, intervalMs / speed);
      play.textContent = lang.pause;
    }
    back.addEventListener('click', () => {halt(); setStep(step - 1);});
    next.addEventListener('click', () => {halt(); setStep(step + 1);});
    seek.addEventListener('input', () => {halt(); setStep(seek.value);});
    reset.addEventListener('click', () => {halt(); stepChanged(); setStep(0);});
    play.addEventListener('click', () => {if (timer !== null) halt(); else start();});
    speedButton.addEventListener('click', () => {speed = speed === 0.5 ? 1 : speed === 1 ? 2 : 0.5;
      speedButton.textContent = `${lang.speed}: ${speed}×`;
      if (timer !== null) start();});
    document.addEventListener('visibilitychange', () => {if (document.hidden) halt();});
    reduce.addEventListener?.('change', event => {if (event.matches) halt();});
    return {get step() {return step;}, setStep, halt, onUpdate(fn) {updated = fn; setStep(0);}};
  }
  function ga(root, lang) {
    let cut = 4, flip = 7;
    const params = create('div', 'evo-parameters'); root.append(params);
    const stage = create('div', 'evo-canvas'); stage.setAttribute('role', 'group');
    stage.setAttribute('aria-label', 'Genome crossover');
    stage.tabIndex = 0;
    root.append(stage);
    const explanation = create('div','evo-feedback'); root.append(explanation);
    const controls = board(root, lang, 9, () => {});
    const aCut = buildSlider(params, lang.cut, 1, 7, 1, cut, v => {cut = v; controls.halt(); controls.setStep(0);});
    const aFlip = buildSlider(params, lang.flip, 1, 8, 1, flip, v => {flip = v; controls.halt(); controls.setStep(0);});
    function row(label, genome, show, focus, origin) {
      const line = create('div', 'evo-genome-row');
      line.append(create('span', 'evo-row-title', label));
      const bits = create('div', 'evo-bits');
      for (let i = 0; i < 8; i++) {
        const char = (genome[i] === undefined || !show(i)) ? '·' : genome[i];
        const cell = create('span', 'evo-bit ' + (char === '·' ? 'evo-empty' : char === '1' ? 'evo-one' : 'evo-zero'), char);
        if (i === focus) cell.classList.add('evo-focus');
        if (origin && i >= cut) cell.classList.add('evo-from-b');
        bits.append(cell);
      }
      line.append(bits); return line;
    }
    const message = create('p', 'evo-message');
    const numeric = create('p', 'evo-numeric');
    stage.append(message, numeric);
    function render() {
      const n = controls.step, upto = Math.min(n, 8);
      const raw = Array.from({length:8},(_,i)=> i < cut ? A[i] : B[i]).join('');
      const after = raw.slice(0,flip-1) + (raw[flip-1] === '0' ? '1' : '0') + raw.slice(flip);
      const final = n === 9 ? after : raw;
      stage.replaceChildren(
        row('A', A, () => true, n >= 1 && n <= 8 && n-1 < cut ? n-1 : -1),
        row('B', B, () => true, n >= 1 && n <= 8 && n-1 >= cut ? n-1 : -1),
        row('Child', final, i => n === 9 || i < upto, n === 9 ? flip - 1 : n >= 1 ? n - 1 : -1, true)
      );
      const phase = n === 0 ? lang.start : n <= 8 ? `${n <= cut ? lang.inheritA : lang.inheritB} · ${n}/8` : `${lang.flipBit} · ${flip}`;
      message.textContent = phase;
      numeric.textContent = `${lang.copy}: ${upto}/8 · ${lang.mutated}: ${n === 9 ? after : '—'}`;
      explanation.replaceChildren(message, numeric);
      stage.dataset.step = String(n);
      stage.dataset.child = n === 9 ? after : raw;
    }
    controls.onUpdate(render);
    const originalReset = root.querySelector('.evo-timeline button:nth-last-child(1)');
    originalReset.addEventListener('click', () => {
      cut=4; flip=7;
      aCut.slider.value='4';aCut.valueLabel.textContent='4';aFlip.slider.value='7';aFlip.valueLabel.textContent='7';
      render();
    });
  }
  function map(root, lang) {
    let challenger = 0.61, replacement = 0.93;
    const params = create('div', 'evo-parameters'); root.append(params);
    const stage = create('div', 'evo-canvas'); stage.tabIndex=0;
    stage.setAttribute('role','group');stage.setAttribute('aria-label','MAP-Elites archive');root.append(stage);
    const explanation=create('div','evo-feedback');root.append(explanation);
    const controls = board(root, lang, 4, () => {});
    const v1 = buildSlider(params, lang.rival, 0, 1, 0.01, challenger, v => {challenger=v; controls.halt(); controls.setStep(0);});
    const v2 = buildSlider(params, lang.elite, 0, 1, 0.01, replacement, v => {replacement=v; controls.halt(); controls.setStep(0);});
    function compute(n) {
      const store = new Map(initial.map(c => [`${c.x},${c.y}`, {...c}]));
      const events = [
        {x:3,y:1,fitness:0.82}, {x:3,y:1,fitness:challenger},
        {x:3,y:1,fitness:replacement}, {x:2,y:3,fitness:0.75}
      ];
      const history=[];
      for(let i=0;i<n;i++) {
        const c=events[i], id=`${c.x},${c.y}`, old=store.get(id);
        let decision=lang.rejected;
        if(!old){store.set(id,c); decision=lang.added;}
        else if(c.fitness > old.fitness){store.set(id,c);decision=lang.replaced;}
        history.push({decision, c, old});
      }
      return {store, history, events};
    }
    function render() {
      const n=controls.step, {store,history,events}=compute(n);
      const current = n ? events[n-1] : null;
      const cells=create('div','evo-map-cells');
      for(let y=0;y<4;y++) for(let x=0;x<6;x++) {
        const id=`${x},${y}`, val=store.get(id);
        const cell=create('span','evo-niche'+(val?' evo-filled':''),val?val.fitness.toFixed(2):'·');
        cell.title=`(${x},${y}) ${val?val.fitness.toFixed(2):'empty'}`;
        if(val) cell.style.setProperty('--evo-quality',String(val.fitness));
        if(current && current.x===x && current.y===y) cell.classList.add('evo-target');
        cells.append(cell);
      }
      const quality=Array.from(store.values()).reduce((a,b)=>a+b.fitness,0);
      const decision=n?history[n-1].decision:lang.no;
      const note=create('p','evo-message',n?`${decision} · (${current.x}, ${current.y}) · ${current.fitness.toFixed(2)}`:decision);
      const metrics=create('p','evo-numeric',`${lang.coverage}: ${store.size}/24 (${(100*store.size/24).toFixed(1)}%) · ${lang.quality}: ${quality.toFixed(2)}`);
      stage.replaceChildren(cells); explanation.replaceChildren(note,metrics);
      stage.dataset.step=String(n);stage.dataset.coverage=String(store.size);
      stage.dataset.lastDecision=decision;
    }
    controls.onUpdate(render);
    const originalReset=root.querySelector('.evo-timeline button:last-of-type');
    originalReset.addEventListener('click',()=>{
      challenger=0.61;replacement=0.93;
      v1.slider.value='.61';v1.valueLabel.textContent='0.61';
      v2.slider.value='.93';v2.valueLabel.textContent='0.93';render();
    });
  }
  function enhance() {
    document.querySelectorAll('[data-evolution-lab]').forEach(root => {
      if(root.dataset.enhanced==='yes')return;
      root.dataset.enhanced='yes';
      const lang=words[root.dataset.lang==='zh'?'zh':'en'];
      root.classList.add('evo-lab');
      root.replaceChildren(create('p','evo-explanation',root.dataset.evolutionLab==='ga'?lang.gaHelp:lang.mapHelp));
      if(root.dataset.evolutionLab==='ga')ga(root,lang);else map(root,lang);
      root.append(create('p','evo-disclaimer',lang.hypothetical));
    });
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',enhance);
  else enhance();
  if(window.document$ && typeof window.document$.subscribe==='function')window.document$.subscribe(enhance);
})();
