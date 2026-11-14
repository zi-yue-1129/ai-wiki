/* Original deterministic stochastic-bandit teaching labs. No third-party runtime. */
(() => {
  'use strict';
  const translations = {
    en: {
      previous: 'Previous', next: 'Next', play: 'Play', pause: 'Pause', reset: 'Reset',
      step: 'Step', speed: 'Speed', reward: 'Reward on each B pull',
      outcome: 'Observed reward for C', success: 'Success (1)', failure: 'Failure (0)',
      mean: 'Mean', bonus: 'Bonus', score: 'UCB score', winner: 'Optimistic winner',
      trials: 'Pulls', observed: 'B observations', time: 'Total pulls',
      initial: 'Initial posterior', draw: 'First posterior draw',
      update: 'Posterior update', redraw: 'Second posterior draw',
      selected: 'Selected arm', note: 'Illustrative values, not empirical measurements or reproducible random draws.',
      graphA: 'UCB1 mean plus exploration bonus for three arms',
      graphB: 'Three Beta posterior density curves and constructed samples',
      sample: 'Constructed draws', posterior: 'Beta parameters',
      stage: ['Before pull', 'After B pull 1', 'After B pull 2'],
      ucbStatus: (s) => `After ${s.step} B observation(s), total pulls ${s.t}; optimistic arm ${s.winner}.`,
      tsStatus: (s) => `${s.stage}; selected arm ${s.winner}; C posterior ${s.cpost}.`,
    },
    'zh-TW': {
      previous: '上一步', next: '下一步', play: '播放', pause: '暫停', reset: '重設',
      step: '步驟', speed: '播放速度', reward: 'B 每次抽取的假設獎勵',
      outcome: 'C 的假設觀察獎勵', success: '成功（1）', failure: '失敗（0）',
      mean: '平均獎勵', bonus: '探索加分', score: 'UCB 分數', winner: '樂觀選擇',
      trials: '抽取次數', observed: 'B 的新增觀察', time: '總抽取次數',
      initial: '初始後驗', draw: '第一次後驗抽樣',
      update: '更新後驗', redraw: '第二次後驗抽樣',
      selected: '選擇的臂', note: '所有數值皆為人工教學示意，非實測結果或可重現的隨機抽樣。',
      graphA: '三個臂的 UCB1 經驗平均值與探索加分',
      graphB: '三個 Beta 後驗密度及人工指定的樣本值',
      sample: '人工抽樣值', posterior: 'Beta 參數',
      stage: ['抽取之前', 'B 第一次抽取後', 'B 第二次抽取後'],
      ucbStatus: (s) => `B 新增 ${s.step} 次觀察，總抽取次數 ${s.t}；當前最高 UCB 為 ${s.winner}。`,
      tsStatus: (s) => `${s.stage}；目前選擇 ${s.winner}；C 的後驗為 ${s.cpost}。`,
    },
  };
  const round = n => Number(n).toFixed(3);
  const esc = s => String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const factorial = n => { let x = 1; for (let k=2;k<=n;k++) x*=k; return x; };
  const betaPDF = (x,a,b) => (x <= 0 || x >= 1) ? 0 : (factorial(a+b-1)/(factorial(a-1)*factorial(b-1)))*x**(a-1)*(1-x)**(b-1);
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
      const state = {step:0, reward:0, outcome:1, speed:1, timer:0};
      root.innerHTML = `
        <div class="bandit-lab-toolbar">
          <button type="button" data-action="previous">${tr.previous}</button>
          <button type="button" data-action="toggle">${tr.play}</button>
          <button type="button" data-action="next">${tr.next}</button>
          <label class="bandit-lab-field">${tr.step} <input data-role="seek" type="range" min="0" max="${max}" step="1" value="0"><output data-role="seek-out">0/${max}</output></label>
          ${ui('select','speed',tr.speed,0,0,[[0.5,'0.5×'],[1,'1×'],[2,'2×']])}
          <button type="button" data-action="reset">${tr.reset}</button>
        </div>
        <div class="bandit-lab-parameters">${kind==='ucb'?ui('0.25','reward',tr.reward,0,1):ui('select','outcome',tr.outcome,0,0,[[1,tr.success],[0,tr.failure]])}</div>
        <div class="bandit-lab-canvas" tabindex="0" role="region" aria-label="${esc(kind==='ucb'?tr.graphA:tr.graphB)}"><svg viewBox="0 0 720 272" width="720" height="272" role="img" aria-label="${esc(kind==='ucb'?tr.graphA:tr.graphB)}" data-role="svg"></svg></div>
        <div class="bandit-lab-legend" data-role="legend"></div>
        <div class="bandit-lab-metrics" data-role="metrics"></div>
        <p class="bandit-lab-note">${tr.note}</p>
        <p class="bandit-lab-live" role="status" aria-live="polite" aria-atomic="true" data-role="status"></p>`;
      const q = selector => root.querySelector(selector);
      const get = id => q(`[data-role="${id}"]`);
      const stop = () => { if(state.timer) window.clearInterval(state.timer);state.timer=0; q('[data-action="toggle"]').textContent=tr.play; };
      function ucb() {
        const counts=[6,2+state.step,8], sums=[3.9,0.9+state.reward*state.step,4.8], t=counts.reduce((a,b)=>a+b,0);
        const means=counts.map((n,i)=>sums[i]/n);
        const bonus=counts.map(n=>Math.sqrt(2*Math.log(t)/n));
        const scores=means.map((m,i)=>m+bonus[i]);
        const winner=arms[scores.indexOf(Math.max(...scores))];
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
        get('metrics').innerHTML=`<span>${tr.time}: <strong>${t}</strong></span><span>${tr.winner}: <strong>${winner}</strong></span><span>${tr.observed}: <strong>${state.step}</strong></span><span>${tr.score}: <strong>${scores.map(round).join(' / ')}</strong></span>`;
        get('status').textContent=tr.ucbStatus({step:state.step,t,winner});
      }
      function thompson() {
        const posterior=[[3,3],[2,5],[4+(state.step>=2&&state.outcome===1?1:0),3+(state.step>=2&&state.outcome===0?1:0)]];
        const first=[0.47,0.22,0.71], second=[0.57,0.38,0.52];
        const draws=state.step===3?second:first;
        const winner=state.step===0?'—':arms[draws.indexOf(Math.max(...draws))];
        const stages=[tr.initial,tr.draw,tr.update,tr.redraw];
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
          if(state.step>0){const x=draws[i],den=betaPDF(x,...posterior[i]);svg+=`<circle cx="${70+x*590}" cy="${224-den*46}" r="7" fill="${colors[i]}" stroke="#fff" stroke-width="2.5"/>`;}
        }
        get('svg').innerHTML=svg;
        get('legend').innerHTML=arms.map((arm,i)=>`<span><i class="bandit-lab-swatch" style="background:${colors[i]}"></i>${arm}</span>`).join('');
        get('metrics').innerHTML=`<span>${esc(stages[state.step])}</span><span>${tr.selected}: <strong>${winner}</strong></span><span>${tr.sample}: <strong>${state.step>0?draws.map(round).join(' / '):'—'}</strong></span><span>${tr.posterior}: <strong>${posterior.map(p=>`(${p.join(',')})`).join(' / ')}</strong></span>`;
        get('status').textContent=tr.tsStatus({stage:stages[state.step],winner,cpost:`Beta(${posterior[2].join(', ')})`});
      }
      function render() {
        get('seek').value=String(state.step);
        get('seek-out').textContent=`${state.step}/${max}`;
        if(kind==='ucb'){get('reward-out').textContent=Number(state.reward).toFixed(2);ucb();} else thompson();
      }
      function go(to){state.step=Math.min(max,Math.max(0,to));render();if(state.step===max)stop();}
      const interval=()=>Math.round(1400/state.speed);
      const play=()=>{if(reduced.matches){stop();return;} if(state.step===max)state.step=0;stop();state.timer=window.setInterval(()=>go(state.step+1),interval());q('[data-action="toggle"]').textContent=tr.pause;render();};
      q('[data-action="previous"]').addEventListener('click',()=>{stop();go(state.step-1);});
      q('[data-action="next"]').addEventListener('click',()=>{stop();go(state.step+1);});
      q('[data-action="reset"]').addEventListener('click',()=>{stop();state.step=0;state.reward=0;state.outcome=1;state.speed=1;get('speed').value='1'; if(kind==='ucb')get('reward').value='0';else get('outcome').value='1';render();});
      q('[data-action="toggle"]').addEventListener('click',()=>state.timer?stop():play());
      get('seek').addEventListener('input',()=>{stop();go(Number(get('seek').value));});
      get('speed').value='1';
      get('speed').addEventListener('change',()=>{state.speed=Number(get('speed').value);if(state.timer)play();});
      if(kind==='ucb')get('reward').addEventListener('input',()=>{state.reward=Number(get('reward').value);render();});
      else get('outcome').addEventListener('change',()=>{state.outcome=Number(get('outcome').value);render();});
      document.addEventListener('visibilitychange',()=>{if(document.hidden)stop();});
      reduced.addEventListener?.('change',e=>{if(e.matches)stop();});
      render();
    }
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',enhance);else enhance();
  if(typeof window.document$!=='undefined' && typeof window.document$.subscribe==='function')window.document$.subscribe(enhance);
})();
