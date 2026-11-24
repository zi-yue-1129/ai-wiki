/* Original deterministic stochastic-bandit teaching labs. No third-party runtime. */
(() => {
  'use strict';
  const translations = {
    en: {
      previous: 'Previous', next: 'Next', play: 'Play', pause: 'Pause', reset: 'Reset',
      step: 'Step', speed: 'Speed', rewardFirst: 'Reward on B pull 1', rewardSecond: 'Reward on B pull 2',
      outcome: 'Observed reward for C', success: 'Success (1)', failure: 'Failure (0)',
      mean: 'Mean', bonus: 'Bonus', score: 'UCB score', winner: 'Optimistic winner',
      trials: 'Pulls', observed: 'B observations', time: 'Total pulls',
      greedy: 'Highest observed mean', margin: 'UCB margin', chance: 'P(best)', postMean: 'Posterior means',
      initial: 'Initial posterior', draw: 'First posterior draw',
      update: 'Posterior update', redraw: 'Second posterior draw',
      selected: 'Selected arm', note: 'Illustrative values, not empirical measurements or reproducible random draws.',
      graphA: 'UCB1 mean plus exploration bonus for three arms',
      decompositionGraph: 'Exact UCB B minus A gap split into empirical mean difference, exploration bonus difference and final margin.',
      credibleGraph: 'C Beta posterior 90 percent equal-tailed credible interval with 5th and 95th percentiles and posterior mean.',
      processGraph: 'Stepwise UCB margin and its exact decomposition, or Beta evidence and credible-interval movement.',
      marginGraph: 'Discrete UCB B minus A score margin at three successive pull counts; the larger marker is the selected stage.',
      pseudocountGraph: 'C Beta posterior shape parameters alpha and beta, highlighting the newly added hypothetical observation.',
      graphB: 'Three Beta posterior density curves and constructed samples',
      predictive: 'C next-success probability', uncertainty: 'C posterior variance',
      planeHint: 'Click or tap the decision plane to set both rewards; keyboard users can adjust the two sliders.',
      boundaryLabel: 'Counterfactual UCB1 third-decision reward map', futureChoice: 'Third decision if both B rewards were observed', cutoffLabel: 'Decision changes when r₁ + r₂ exceeds',
      scrollHint: 'Swipe the plot horizontally, or focus it and use arrow keys to inspect all three arms.',
      sample: 'Constructed draws', posterior: 'Beta parameters',
      stage: ['Before pull', 'After B pull 1', 'After B pull 2'],
      ucbStatus: (s) => `After ${s.step} B observation(s), total pulls ${s.t}; optimistic arm ${s.winner}; highest sample mean ${s.greedy}; score margin ${round(s.margin)}.`,
      tsStatus: (s) => `${s.stage}; selected arm ${s.winner}; C posterior ${s.cpost}.`,
    },
    'zh-TW': {
      previous: '上一步', next: '下一步', play: '播放', pause: '暫停', reset: '重設',
      step: '步驟', speed: '播放速度', rewardFirst: 'B 第一次抽取的假設獎勵', rewardSecond: 'B 第二次抽取的假設獎勵',
      outcome: 'C 的假設觀察獎勵', success: '成功（1）', failure: '失敗（0）',
      mean: '平均獎勵', bonus: '探索加分', score: 'UCB 分數', winner: '樂觀選擇',
      trials: '抽取次數', observed: 'B 的新增觀察', time: '總抽取次數',
      greedy: '經驗平均值最高', margin: 'UCB 領先幅度', chance: '成為最佳臂的後驗機率', postMean: '後驗平均值',
      initial: '初始後驗', draw: '第一次後驗抽樣',
      update: '更新後驗', redraw: '第二次後驗抽樣',
      selected: '選擇的臂', note: '所有數值皆為人工教學示意，非實測結果或可重現的隨機抽樣。',
      graphA: '三個臂的 UCB1 經驗平均值與探索加分',
      decompositionGraph: 'UCB B 減 A 的精確分數差，拆成平均獎勵差、探索加分差與淨分數差。',
      credibleGraph: 'C 的 Beta 後驗 90% 等尾可信區間，標出第 5、95 百分位數與後驗平均值。',
      processGraph: 'UCB 決策分數差與分解，或 Beta 證據更新與可信區間變化。',
      marginGraph: '連續三個抽取總數下 UCB B 減 A 的離散分數差，較大標記代表目前步驟。',
      pseudocountGraph: 'C 的 Beta 後驗形狀參數 alpha 與 beta，深色外框標示新增的假設觀察。',
      graphB: '三個 Beta 後驗密度及人工指定的樣本值',
      predictive: 'C 下一次成功的預測機率', uncertainty: 'C 後驗變異數',
      planeHint: '可點選決策平面，同時設定兩次獎勵；鍵盤使用者可操作兩個滑桿。',
      boundaryLabel: 'UCB1 第三次決策的反事實獎勵平面', futureChoice: '假設 B 兩次回饋都已發生，第三次會選擇', cutoffLabel: '決策分界為 r₁ + r₂ 大於',
      scrollHint: '可左右滑動圖表，或聚焦後使用方向鍵查看三個臂。',
      sample: '人工抽樣值', posterior: 'Beta 參數',
      stage: ['抽取之前', 'B 第一次抽取後', 'B 第二次抽取後'],
      ucbStatus: (s) => `B 新增 ${s.step} 次觀察，總抽取次數 ${s.t}；UCB 選擇 ${s.winner}、平均獎勵最高為 ${s.greedy}、分數差 ${round(s.margin)}。`,
      tsStatus: (s) => `${s.stage}；目前選擇 ${s.winner}；C 的後驗為 ${s.cpost}。`,
    },
  };
  const round = n => Number(n).toFixed(3);
  const esc = s => String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const factorial = n => { let x = 1; for (let k=2;k<=n;k++) x*=k; return x; };
  const betaPDF = (x,a,b) => (x <= 0 || x >= 1) ? 0 : (factorial(a+b-1)/(factorial(a-1)*factorial(b-1)))*x**(a-1)*(1-x)**(b-1);
  // For integer Beta parameters, the regularized incomplete beta is a binomial tail.
  const choose = (n,k) => factorial(n)/(factorial(k)*factorial(n-k));
  const betaCDF = (x,a,b) => {
    const n=a+b-1;
    let total=0;
    for(let k=a;k<=n;k++) total+=choose(n,k)*x**k*(1-x)**(n-k);
    return total;
  };
  // Independent posterior draws: P(arm i is best) = ∫ pdf_i(x) ∏_{j!=i} cdf_j(x) dx.
  // Deterministic composite Simpson quadrature, NOT a Monte Carlo observation.
  const probabilityBest = (post,i) => {
    const steps=600, h=1/steps;
    let sum=0;
    for(let k=0;k<=steps;k++){
      const x=k*h;
      let value=betaPDF(x,...post[i]);
      for(let j=0;j<post.length;j++) if(j!==i) value*=betaCDF(x,...post[j]);
      sum+=(k===0||k===steps?1:k%2?4:2)*value;
    }
    return sum*h/3;
  };
  const arms = ['A','B','C'];
  const colors = ['#237eab','#b96b26','#468969'];
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)');
  const ui = (name,id,label,value,max,options) => {
    if (name === 'select') return `<label class="bandit-lab-field">${esc(label)} <select data-role="${id}">${options.map(o=>`<option value="${o[0]}">${esc(o[1])}</option>`).join('')}</select></label>`;
    return `<label class="bandit-lab-field">${esc(label)} <input data-role="${id}" type="range" min="0" max="${max}" step="${name}" value="${value}"><output data-role="${id}-out">${value}</output></label>`;
  };
  function enhance() {
    for (const root of document.querySelectorAll('[data-bandit-lab]')) {
      if (root.dataset.enhanced) continue;
      const kind = root.dataset.banditLab;
      if (kind !== 'ucb' && kind !== 'thompson') continue;
      const tr = translations[root.dataset.lang] || translations.en;
      root.dataset.enhanced = 'true';
      const max = kind==='ucb'?2:3;
      const state = {step:0, reward1:0, reward2:0, outcome:1, speed:1, timer:0};
      root.innerHTML = `
        <div class="bandit-lab-toolbar">
          <button type="button" data-action="previous">${tr.previous}</button>
          <button type="button" data-action="toggle">${tr.play}</button>
          <button type="button" data-action="next">${tr.next}</button>
          <label class="bandit-lab-field">${tr.step} <input data-role="seek" type="range" min="0" max="${max}" step="1" value="0"><output data-role="seek-out">0/${max}</output></label>
          ${ui('select','speed',tr.speed,0,0,[[0.5,'0.5×'],[1,'1×'],[2,'2×']])}
          <button type="button" data-action="reset">${tr.reset}</button>
        </div>
        <div class="bandit-lab-parameters">${kind==='ucb'?ui('0.05','reward1',tr.rewardFirst,0,1)+ui('0.05','reward2',tr.rewardSecond,0,1):ui('select','outcome',tr.outcome,0,0,[[1,tr.success],[0,tr.failure]])}</div>
        <div class="bandit-lab-canvas" tabindex="0" role="region" aria-label="${esc(kind==='ucb'?tr.graphA:tr.graphB)}"><svg viewBox="0 0 720 272" width="720" height="272" role="img" aria-label="${esc(kind==='ucb'?tr.graphA:tr.graphB)}" data-role="svg"></svg></div>
        <p class="bandit-lab-scroll-hint">${esc(tr.scrollHint)}</p>
        ${kind==='ucb'?'<div class="bandit-lab-boundary" data-role="boundary"></div>':''}
        <div class="bandit-lab-legend" data-role="legend"></div>
        ${kind==='thompson'?`<div class="bandit-lab-probabilities" data-role="probabilities" aria-label="${esc(tr.chance)}"></div>`:''}
        <div class="bandit-lab-process" data-role="process" tabindex="0" role="region" aria-label="${esc(tr.processGraph)}"></div>
        <div class="bandit-lab-metrics" data-role="metrics"></div>
        <p class="bandit-lab-note">${tr.note}</p>
        <p class="bandit-lab-live" role="status" aria-live="polite" aria-atomic="true" data-role="status"></p>`;
      const q = selector => root.querySelector(selector);
      const get = id => q(`[data-role="${id}"]`);
      const stop = () => { if(state.timer) window.clearInterval(state.timer);state.timer=0; q('[data-action="toggle"]').textContent=tr.play; };
      // Exact counterfactual third-choice map: with n=(6,4,8) at t=18,
      // A beats C for every r1,r2 in [0,1]; B beats A iff r1+r2 > cutoff.
      // The line is analytical, not a sampled or interpolated heatmap.
      function renderUcbDecisionMap() {
        const scoreA = 0.65 + Math.sqrt(2*Math.log(18)/6);
        const scoreC = 0.60 + Math.sqrt(2*Math.log(18)/8);
        const bonusB = Math.sqrt(2*Math.log(18)/4);
        const cutoff = 4*(Math.max(scoreA,scoreC)-bonusB)-0.9;
        const winner = (0.9+state.reward1+state.reward2)/4+bonusB > Math.max(scoreA,scoreC) ? 'B' : (scoreA>=scoreC?'A':'C');
        const x0=55, y0=27, side=160, bottom=y0+side, xCut=x0+side*cutoff, yCut=bottom-side*cutoff;
        let grid='';
        for(let k=1;k<4;k++){
          const v=side*k/4;
          grid+=`<line x1='${x0+v}' y1='${y0}' x2='${x0+v}' y2='${bottom}' stroke='#fff' opacity='.35'/><line x1='${x0}' y1='${y0+v}' x2='${x0+side}' y2='${y0+v}' stroke='#fff' opacity='.35'/>`;
        }
        const cx=x0+side*state.reward1, cy=bottom-side*state.reward2;
        const svg=`<svg viewBox='0 0 330 228' width='330' height='228' role='img' aria-label='${esc(tr.boundaryLabel)}'>
          <rect width='330' height='228' rx='12' fill='#f8fafc'/>
          <text x='25' y='16' font-size='12' fill='#365166'>r₂</text>
          <rect x='55' y='27' width='160' height='160' fill='#e9b87e'/>
          <polygon points='${x0},${bottom} ${xCut.toFixed(2)},${bottom} ${x0},${yCut.toFixed(2)}' fill='#8ebbd6'/>
          ${grid}<line x1='${xCut.toFixed(2)}' y1='${bottom}' x2='${x0}' y2='${yCut.toFixed(2)}' stroke='#314858' stroke-width='2' stroke-dasharray='5 3'/>
          <rect x='55' y='27' width='160' height='160' fill='none' stroke='#71869b' stroke-width='1'/>
          <circle data-role='reward-marker' cx='${cx.toFixed(1)}' cy='${cy.toFixed(1)}' r='7' fill='#173951' stroke='#fff' stroke-width='2.3'/>
          <text x='55' y='202' font-size='12' fill='#365166'>0</text><text x='211' y='202' font-size='12' text-anchor='end' fill='#365166'>1</text>
          <text x='130' y='217' font-size='13' text-anchor='middle' fill='#365166'>r₁</text>
          <text x='42' y='188' text-anchor='end' font-size='12' fill='#365166'>0</text><text x='42' y='36' text-anchor='end' font-size='12' fill='#365166'>1</text>
          <text x='239' y='44' font-size='13' font-weight='600' fill='#365166'>t = 18</text>
          <rect x='239' y='75' width='12' height='12' rx='2' fill='#8ebbd6'/><text x='258' y='86' font-size='13' fill='#365166'>A</text>
          <rect x='239' y='101' width='12' height='12' rx='2' fill='#e9b87e'/><text x='258' y='112' font-size='13' fill='#365166'>B</text>
        </svg>`;
        get('boundary').innerHTML=`<div class='bandit-lab-boundary-scroll' tabindex='0' role='region' aria-label='${esc(tr.boundaryLabel)}'>${svg}</div><p class='bandit-lab-boundary-note'>${esc(tr.futureChoice)}: <strong>${winner}</strong>. ${esc(tr.cutoffLabel)} ${cutoff.toFixed(3)}.</p><p class='bandit-lab-boundary-hint'>${esc(tr.planeHint)}</p>`;
        // Announce the future (counterfactual) choice when either slider or the
        // plane changes; the current-step UCB choice is a different quantity.
        get('status').textContent += ` ${tr.futureChoice}: ${winner}.`;
      }
      // A pointer click sets both hypothetical rewards. Recreating the SVG on
      // render is intentional: use a click rather than a persistent drag handle.
      // Keyboard-only readers control exactly the same state via both sliders.
      if(kind==='ucb') get('boundary').addEventListener('click',event=>{
        const image=event.target.closest('svg');
        if(!image || !get('boundary').contains(image))return;
        const bounds=image.getBoundingClientRect();
        const x=(event.clientX-bounds.left)*330/bounds.width;
        const y=(event.clientY-bounds.top)*228/bounds.height;
        if(x<55||x>215||y<27||y>187)return;
        const quantise=value=>Math.max(0,Math.min(1,Math.round(value*20)/20));
        stop();state.reward1=quantise((x-55)/160);
        state.reward2=quantise((187-y)/160);
        get('reward1').value=state.reward1.toFixed(2);
        get('reward2').value=state.reward2.toFixed(2);
        render();
      });
      function renderUcbMarginTrace(state, target, tr) {
  // Score gap is an exact discrete UCB1 computation at three successive pull counts.
  const deltas = [0, 1, 2].map(step => {
    const t = 16 + step;
    const a = 0.65 + Math.sqrt(2 * Math.log(t) / 6);
    const b = (0.9 + (step >= 1 ? state.reward1 : 0) + (step >= 2 ? state.reward2 : 0)) / (2 + step) + Math.sqrt(2 * Math.log(t) / (2 + step));
    return b - a;
  });
  const x = [61, 165, 269], top = 28, bottom = 120;
  const y = v => top + (0.65 - v) * (bottom - top);
  const zero = y(0);
  const line = deltas.map((v, i) => `${x[i]},${y(v).toFixed(2)}`).join(' ');
  const labels = deltas.map((v, i) => {
    const cy = y(v), active = i === state.step;
    return `<circle data-margin-step="${i}" data-delta="${v.toFixed(6)}" cx="${x[i]}" cy="${cy.toFixed(2)}" r="${active ? 6.5 : 4.2}" fill="${active ? '#173951' : '#237eab'}" stroke="white" stroke-width="2"/><text x="${x[i]}" y="${Math.max(16, cy + (v >= 0 ? -12 : 18)).toFixed(2)}" text-anchor="middle" font-size="11" font-weight="600" fill="#263d51">${v >= 0 ? '+' : ''}${v.toFixed(3)}</text><text x="${x[i]}" y="145" font-size="11" text-anchor="middle" fill="#506578">${16+i}</text>`;
  }).join('');
  target.innerHTML = `<svg viewBox="0 0 338 156" role="img" aria-label="${esc(tr.marginGraph)}"><rect width="338" height="156" rx="9" fill="#f8fafc"/><text x="12" y="17" font-size="13" font-weight="600" fill="#273e52">B − A</text><text x="299" y="148" font-size="11" fill="#506578">t</text><line x1="38" y1="${zero.toFixed(2)}" x2="294" y2="${zero.toFixed(2)}" stroke="#637b8f" stroke-dasharray="4 4" stroke-width="1.2"/><text x="17" y="${(zero-4).toFixed(2)}" font-size="10" fill="#506578">0</text><polyline points="${line}" fill="none" stroke="#237eab" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>${labels}</svg>`;
}
      function renderThompsonEvidence(state, target, tr, ca, cb) {
  // Alpha and beta include prior pseudo-counts; only the outlined unit is new evidence.
  const extraAlpha = state.step >= 2 && Number(state.outcome) === 1;
  const extraBeta = state.step >= 2 && Number(state.outcome) === 0;
  const blocks = (count, color, cy, extra) => Array.from({length:count},(_,i) => `<rect x="${62+i*31}" y="${cy}" width="24" height="22" rx="4" fill="${color}" ${extra && i === count-1 ? `stroke="#173951" stroke-width="3" data-new-pseudo="${cy===51?'alpha':'beta'}"` : 'stroke="#fff" stroke-width="1"'}/>`).join('');
  target.innerHTML = `<svg viewBox="0 0 338 137" role="img" aria-label="${esc(tr.pseudocountGraph)}" data-alpha="${ca}" data-beta="${cb}"><rect width="338" height="137" rx="9" fill="#f8fafc"/><text x="13" y="22" font-size="13" font-weight="600" fill="#273e52">C · Beta</text><text x="23" y="68" font-size="18" fill="#273e52">α</text><text x="23" y="110" font-size="18" fill="#273e52">β</text>${blocks(ca,'#237eab',51,extraAlpha)}${blocks(cb,'#e6a452',93,extraBeta)}<text x="251" y="68" font-size="14" font-weight="600" fill="#273e52">${ca}</text><text x="251" y="110" font-size="14" font-weight="600" fill="#273e52">${cb}</text></svg>`;
}
function renderUcbDecomposition(state, target, tr) {
  // Exactly decompose the UCB(B)-UCB(A) decision score into empirical and bonus gaps.
  // No observations are added to A or C in this hypothetical two-pull sequence.
  const t = 16 + state.step, n = 2 + state.step;
  const meanGap = (0.9 + (state.step >= 1 ? state.reward1 : 0) + (state.step >= 2 ? state.reward2 : 0)) / n - 0.65;
  const bonusGap = Math.sqrt(2 * Math.log(t) / n) - Math.sqrt(2 * Math.log(t) / 6);
  const netGap = meanGap + bonusGap;
  const px = v => 165.5 + v * 159.4;
  const rows = [
    ['Mean gap', meanGap, '#237eab', 49],
    ['Bonus gap', bonusGap, '#e6a452', 92],
    ['Net gap', netGap, '#173951', 135],
  ];
  const bars = rows.map(([name,value,color,y]) => {
    const edge = px(value), positive = value >= 0;
    return `<text x="12" y="${y-14}" font-size="11" fill="#273e52">${name}</text><rect x="${Math.min(165.5,edge).toFixed(2)}" y="${y-6}" width="${Math.abs(edge-165.5).toFixed(2)}" height="17" rx="2" fill="${color}"/><text x="${(edge+(positive?7:-7)).toFixed(2)}" y="${y+6}" text-anchor="${positive?'start':'end'}" font-size="12" font-weight="600" fill="#263d51">${positive?'+':''}${value.toFixed(3)}</text>`;
  }).join('');
  target.insertAdjacentHTML('beforeend', `<svg viewBox="0 0 338 174" role="img" aria-label="${esc(tr.decompositionGraph)}" data-mean-gap="${meanGap.toFixed(6)}" data-bonus-gap="${bonusGap.toFixed(6)}" data-net-gap="${netGap.toFixed(6)}"><rect width="338" height="174" rx="10" fill="#f8fafc"/><text x="12" y="18" font-size="13" font-weight="600" fill="#273e52">UCB score · B − A</text><line x1="165.5" y1="29" x2="165.5" y2="154" stroke="#637b8f" stroke-width="1.4" stroke-dasharray="4 4"/>${bars}<text x="165.5" y="168" text-anchor="middle" font-size="11" fill="#506578">0</text></svg>`);
}
      function renderThompsonCredible(target,tr,a,b) {
  // Exact integer-Beta CDF inversion by bisection: equal-tailed posterior interval.
  const quantile = p => {
    let lo = 0, hi = 1;
    for(let k=0;k<45;k++) {
      const mid=(lo+hi)/2;
      if(betaCDF(mid,a,b)<p) lo=mid; else hi=mid;
    }
    return (lo+hi)/2;
  };
  const lower=quantile(0.05), upper=quantile(0.95), mean=a/(a+b);
  const px = v => 32 + 273*v;
  target.insertAdjacentHTML('beforeend', `<svg viewBox="0 0 338 160" role="img" aria-label="${esc(tr.credibleGraph)}" data-cred-low="${lower.toFixed(6)}" data-cred-high="${upper.toFixed(6)}" data-cred-mean="${mean.toFixed(6)}"><rect width="338" height="160" rx="10" fill="#f8fafc"/><text x="12" y="21" font-size="13" font-weight="600" fill="#273e52">C · 90% CrI</text><line x1="32" y1="68" x2="305" y2="68" stroke="#a0b0bf" stroke-width="3"/><rect x="${px(lower).toFixed(2)}" y="56" width="${(px(upper)-px(lower)).toFixed(2)}" height="24" rx="4" fill="#b9decb"/><line x1="${px(lower).toFixed(2)}" y1="50" x2="${px(lower).toFixed(2)}" y2="86" stroke="#468969" stroke-width="2"/><line x1="${px(upper).toFixed(2)}" y1="50" x2="${px(upper).toFixed(2)}" y2="86" stroke="#468969" stroke-width="2"/><circle cx="${px(mean).toFixed(2)}" cy="68" r="6" fill="#173951" stroke="white" stroke-width="2"/><text x="${px(mean).toFixed(2)}" y="49" text-anchor="middle" font-size="12" fill="#173951">μ</text><text x="32" y="105" text-anchor="middle" font-size="11" fill="#506578">0</text><text x="168.5" y="105" text-anchor="middle" font-size="11" fill="#506578">0.5</text><text x="305" y="105" text-anchor="middle" font-size="11" fill="#506578">1</text><text x="90" y="139" text-anchor="middle" font-size="12" fill="#263d51">q05 ${lower.toFixed(3)}</text><text x="249" y="139" text-anchor="middle" font-size="12" fill="#263d51">q95 ${upper.toFixed(3)}</text></svg>`);
}
      function ucb() {
        const counts=[6,2+state.step,8], sums=[3.9,0.9+(state.step>=1?state.reward1:0)+(state.step>=2?state.reward2:0),4.8], t=counts.reduce((a,b)=>a+b,0);
        const means=counts.map((n,i)=>sums[i]/n);
        const bonus=counts.map(n=>Math.sqrt(2*Math.log(t)/n));
        const scores=means.map((m,i)=>m+bonus[i]);
        const winner=arms[scores.indexOf(Math.max(...scores))];
        const greedy=arms[means.indexOf(Math.max(...means))];
        const ordered=[...scores].sort((a,b)=>b-a), margin=ordered[0]-ordered[1];
        let svg=`<rect x="0" y="0" width="720" height="272" rx="12" fill="#f8fafc"/><text x="24" y="28" class="bandit-lab-svg-title">UCB1</text><text x="615" y="28" class="bandit-lab-svg-small">t = ${t}</text>`;
        for(let i=0;i<3;i++) {
          const x=119+i*208, scale=76;
          svg+=`<rect x="${x-17}" y="50" width="120" height="173" rx="9" fill="${winner===arms[i]?'#e5f3e9':'#edf2f7'}"/>`;
          svg+=`<line x1="${x}" y1="214" x2="${x+86}" y2="214" stroke="#9babbc"/>`;
          const ymean=means[i]*scale,ybonus=bonus[i]*scale;
          svg+=`<rect x="${x+24}" y="${214-ymean}" width="39" height="${ymean}" fill="${colors[i]}"/><rect x="${x+24}" y="${214-ymean-ybonus}" width="39" height="${ybonus}" fill="#e6a452"/>`;
          svg+=`<text x="${x+44}" y="${214-ymean-ybonus-8}" text-anchor="middle" class="bandit-lab-svg-score">${scores[i].toFixed(2)}</text>`;
          svg+=`<text x="${x+43}" y="238" text-anchor="middle" class="bandit-lab-svg-title">${arms[i]}</text><text x="${x+43}" y="256" text-anchor="middle" class="bandit-lab-svg-small">n=${counts[i]}</text>`;
        }
        get('svg').innerHTML=svg;
        get('legend').innerHTML=`<span><i class="bandit-lab-swatch" style="background:#237eab"></i>${tr.mean} (A/B/C)</span><span><i class="bandit-lab-swatch" style="background:#e6a452"></i>${tr.bonus}</span>`;
        get('metrics').innerHTML=`<span>${tr.time}: <strong>${t}</strong></span><span>${tr.winner}: <strong>${winner}</strong></span><span>${tr.observed}: <strong>${state.step}</strong></span><span>${tr.greedy}: <strong>${greedy}</strong></span><span>${tr.margin}: <strong>${round(margin)}</strong></span><span>${tr.score}: <strong>${scores.map(round).join(' / ')}</strong></span>`;
        renderUcbMarginTrace(state, get('process'), tr);
        renderUcbDecomposition(state, get('process'), tr);
        get('status').textContent=tr.ucbStatus({step:state.step,t,winner,greedy,margin});
        renderUcbDecisionMap();
      }
      function thompson() {
        const posterior=[[3,3],[2,5],[4+(state.step>=2&&state.outcome===1?1:0),3+(state.step>=2&&state.outcome===0?1:0)]];
        const first=[0.47,0.22,0.71], second=[0.57,0.38,0.52];
        const draws=state.step===3?second:first;
        const showDraw=state.step===1 || state.step===3;
        const winner=showDraw?arms[draws.indexOf(Math.max(...draws))]:'—';
        const stages=[tr.initial,tr.draw,tr.update,tr.redraw];
        const chances=arms.map((_,i)=>probabilityBest(posterior,i));
        const means=posterior.map(([a,b])=>a/(a+b));
        const [ca,cb]=posterior[2], nextSuccess=ca/(ca+cb);
        const cVariance=ca*cb/((ca+cb)**2*(ca+cb+1));
        let svg=`<rect x="0" y="0" width="720" height="272" rx="12" fill="#f8fafc"/><text x="24" y="26" class="bandit-lab-svg-title">Thompson</text>`;
        for (let j=0;j<=4;j++) {
          const y=224-j*46;
          svg+=`<line x1="70" y1="${y}" x2="660" y2="${y}" stroke="#d6dfe8" stroke-dasharray="3 4"/>`;
        }
        svg+='<line x1="70" y1="224" x2="660" y2="224" stroke="#91a4b7"/>';
        for (let j=0;j<=5;j++) svg+=`<text x="${70+j*118}" y="243" text-anchor="middle" class="bandit-lab-svg-small">${(j/5).toFixed(1)}</text>`;
        for(let i=0;i<3;i++) {
          let d='';
          for(let j=1;j<160;j++) {
            const x=j/160,den=betaPDF(x,...posterior[i]),sx=70+590*x,sy=224-46*den;
            d+=`${j===1?'M':'L'}${sx.toFixed(2)},${sy.toFixed(2)} `;
          }
          svg+=`<path d="${d}" fill="none" stroke="${colors[i]}" stroke-width="3.4" stroke-linejoin="round"/>`;
          svg+=`<text x="${364+i*94}" y="25" class="bandit-lab-svg-small" style="fill:${colors[i]}">${arms[i]}</text>`;
          // Previously drawn samples belong to the old posterior; never relocate
          // them onto an updated density during the observation-only stage.
          if(showDraw){const x=draws[i],den=betaPDF(x,...posterior[i]);svg+=`<circle cx="${70+x*590}" cy="${224-den*46}" r="7" fill="${colors[i]}" stroke="#fff" stroke-width="2.5"/>`;}
        }
        get('svg').innerHTML=svg;
        get('legend').innerHTML=arms.map((arm,i)=>`<span><i class="bandit-lab-swatch" style="background:${colors[i]}"></i>${arm}</span>`).join('');
        get('probabilities').innerHTML=`<strong class="bandit-lab-prob-title">P(best)</strong>`+arms.map((arm,i)=>`<div class="bandit-lab-prob-row" data-prob="${chances[i].toFixed(6)}"><span>${arm}</span><div class="bandit-lab-prob-track" role="meter" aria-label="${arm} ${esc(tr.chance)}" aria-valuemin="0" aria-valuemax="100" aria-valuenow="${(chances[i]*100).toFixed(1)}"><div class="bandit-lab-prob-fill" style="width:${(chances[i]*100).toFixed(2)}%;background:${colors[i]}"></div></div><output>${(chances[i]*100).toFixed(1)}%</output></div>`).join('');
        get('metrics').innerHTML=`<span>${esc(stages[state.step])}</span><span>${tr.selected}: <strong>${winner}</strong></span><span>${tr.sample}: <strong>${showDraw?draws.map(round).join(' / '):'—'}</strong></span><span>${tr.posterior}: <strong>${posterior.map(p=>`(${p.join(',')})`).join(' / ')}</strong></span><span>${tr.postMean}: <strong>${means.map(round).join(' / ')}</strong></span><span>${tr.predictive}: <strong>${nextSuccess.toFixed(4)}</strong></span><span>${tr.uncertainty}: <strong>${cVariance.toFixed(4)}</strong></span>`;
        renderThompsonEvidence(state, get('process'), tr, ca, cb);
        renderThompsonCredible(get('process'), tr, ca, cb);
        get('status').textContent=tr.tsStatus({stage:stages[state.step],winner,cpost:`Beta(${posterior[2].join(', ')})`});
      }
      function render() {
        get('seek').value=String(state.step);
        get('seek-out').textContent=`${state.step}/${max}`;
        if(kind==='ucb'){get('reward1-out').textContent=Number(state.reward1).toFixed(2);get('reward2-out').textContent=Number(state.reward2).toFixed(2);ucb();} else thompson();
      }
      function go(to){state.step=Math.min(max,Math.max(0,to));render();if(state.step===max)stop();}
      const interval=()=>Math.round(1400/state.speed);
      const play=()=>{if(reduced.matches){stop();return;} if(state.step===max)state.step=0;stop();state.timer=window.setInterval(()=>{if(!root.isConnected||document.hidden){stop();return;}go(state.step+1)},interval());q('[data-action="toggle"]').textContent=tr.pause;render();};
      q('[data-action="previous"]').addEventListener('click',()=>{stop();go(state.step-1);});
      q('[data-action="next"]').addEventListener('click',()=>{stop();go(state.step+1);});
      q('[data-action="reset"]').addEventListener('click',()=>{stop();state.step=0;state.reward1=0;state.reward2=0;state.outcome=1;state.speed=1;get('speed').value='1'; if(kind==='ucb'){get('reward1').value='0';get('reward2').value='0';}else get('outcome').value='1';render();});
      q('[data-action="toggle"]').addEventListener('click',()=>state.timer?stop():play());
      get('seek').addEventListener('input',()=>{stop();go(Number(get('seek').value));});
      get('speed').value='1';
      get('speed').addEventListener('change',()=>{state.speed=Number(get('speed').value);if(state.timer)play();});
      if(kind==='ucb')for(const id of ['reward1','reward2'])get(id).addEventListener('input',()=>{stop();state[id]=Number(get(id).value);render();});
      else get('outcome').addEventListener('change',()=>{stop();state.outcome=Number(get('outcome').value);render();});
      document.addEventListener('visibilitychange',()=>{if(document.hidden)stop();});
      reduced.addEventListener?.('change',e=>{if(e.matches)stop();});
      render();
    }
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',enhance);else enhance();
  if(typeof window.document$!=='undefined' && typeof window.document$.subscribe==='function')window.document$.subscribe(enhance);
})();
