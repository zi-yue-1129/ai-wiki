/* Deterministic, original Gibbs teaching models. No random draws or external dependencies. */
(() => {
  'use strict';
  const translations = {
    en: { previous:'Previous',next:'Next',play:'Play',pause:'Pause',reset:'Reset',step:'Step',speed:'Speed',
      rho:'Target correlation ρ', scan:'Update kernel',start:'Initial state',single:'Single-site Gibbs',block:'Joint block draw',
      note:'Synthetic, fixed innovations and uniform variates; not measured MCMC output or random simulations.',
      gaussian:'Correlated Gaussian: conditional updates and stationary lag autocorrelation',
      discrete:'Two-mode discrete target: single-coordinate trapping versus a joint block draw',
      scroll:'Focus this figure and scroll horizontally to read its full labels.',
      a:'Gaussian sweep',b:'Disconnected target',fixed:'Fixed coordinate',
      reduced:'Reduced-motion is enabled: playback will not start automatically.',
      diagnosticsGaussian:'Theoretical finite-sample effective size of the stationary Gibbs Y mean for 100 full sweeps as target correlation varies.',
      diagnosticsDisconnected:'Exact total variation distance from a point start to the two-mode target after each complete kernel transition.',
      gab:(s)=>`Step ${s.step} of 10; ρ ${s.rho.toFixed(2)}; X ${s.x.toFixed(3)}, Y ${s.y.toFixed(3)}; stationary lag-one correlation ρ² ${(s.rho*s.rho).toFixed(3)}.`,
      dib:(s)=>`Step ${s.step} of 8; ${s.mode==='single'?'single-site conditional, fixed':'joint block conditional, possibly switching'}; current state (${s.bit},${s.bit}).`
    },
    zh: { previous:'上一步',next:'下一步',play:'播放',pause:'暫停',reset:'重設',step:'步驟',speed:'速度',
      rho:'目標相關係數 ρ',scan:'更新方式',start:'初始狀態',single:'逐座標 Gibbs',block:'聯合分塊抽樣',
      note:'固定的人工常態創新與均勻數值，非實測 MCMC 輸出或真正隨機模擬。',
      gaussian:'相關高斯：條件更新路徑及平穩態的延遲自相關',
      discrete:'雙模態離散目標：逐座標受困與聯合抽樣跨模態',
      scroll:'可聚焦此圖並水平捲動，閱讀完整標籤。',
      a:'高斯掃描',b:'不連通目標',fixed:'固定的座標',
      reduced:'已開啟減少動態效果，不會自動播放。',
      diagnosticsGaussian:'相關高斯 Gibbs 平穩態 Y 平均數在一百輪完整掃描下，理論有限樣本有效樣本數隨相關係數變化的圖。',
      diagnosticsDisconnected:'從單一支援點出發，每次完整更新後與雙模態目標分布之間的精確總變異距離。',
      gab:(s)=>`第 ${s.step}/10 步；ρ=${s.rho.toFixed(2)}；X=${s.x.toFixed(3)}，Y=${s.y.toFixed(3)}；平穩態單輪延遲相關 ρ²=${(s.rho*s.rho).toFixed(3)}。`,
      dib:(s)=>`第 ${s.step}/8 步；${s.mode==='single'?'逐座標抽樣受困':'聯合分塊抽樣可跨模態'}；目前為 (${s.bit},${s.bit})。`
    }
  };
  const esc = s => String(s).replace(/[&<>"']/g, ch => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;','\'':'&#39;'}[ch]));
  const innovations = [0.5,-1,-0.7,0.8,0.2,-0.6,-0.3,0.7,0.9,-0.4];
  const uniforms = [0.8,0.2,0.9,0.1,0.7,0.3,0.6,0.4];
  const getStates = rho => {
    const arr = [{x:0,y:1}]; const sigma = Math.sqrt(1-rho*rho);
    for(let i=0;i<10;i++) {
      const p=arr[arr.length-1];
      arr.push(i%2===0 ? {x:rho*p.y+sigma*innovations[i],y:p.y} : {x:p.x,y:rho*p.x+sigma*innovations[i]});
    }
    return arr;
  };
  function init(host) {
    if(host.dataset.gibbsReady)return;
    const kind=host.dataset.gibbsLab;
    if(kind!=='gaussian'&&kind!=='disconnected')return;
    host.dataset.gibbsReady='true';
    const L=translations[host.dataset.lang==='zh-TW'?'zh':'en'];
    const max=kind==='gaussian'?10:8;
    const state={step:0,rho:0.8,mode:'single',start:0,speed:1,timer:null};
    const opts=(name,options)=>`<label class="gibbs-lab-field">${esc(name)} <select data-field="${name===L.scan?'mode':'start'}">${options.map(([v,label])=>`<option value="${v}">${esc(label)}</option>`).join('')}</select></label>`;
    host.innerHTML=`<div class="gibbs-lab-panel">
      <div class="gibbs-lab-controls"><button type="button" data-action="prev">${L.previous}</button><button type="button" data-action="play">${L.play}</button><button type="button" data-action="next">${L.next}</button>
      <label class="gibbs-lab-field">${L.step} <input aria-label="${L.step}" type="range" data-field="step" min="0" max="${max}" step="1" value="0"><output data-value="step">0/${max}</output></label>
      <label class="gibbs-lab-field">${L.speed} <select data-field="speed"><option value="0.5">0.5×</option><option value="1" selected>1×</option><option value="2">2×</option></select></label>
      <button type="button" data-action="reset">${L.reset}</button></div>
      <div class="gibbs-lab-parameters">${kind==='gaussian'?`<label class="gibbs-lab-field">${L.rho} <input aria-label="${L.rho}" type="range" min="0" max="0.95" step="0.05" value="0.8" data-field="rho"><output data-value="rho">0.80</output></label>`:opts(L.scan,[['single',L.single],['block',L.block]])+opts(L.start,[[0,'(0,0)'],[1,'(1,1)']])}</div>
      <div class="gibbs-lab-scroll" tabindex="0" role="region" aria-label="${esc(kind==='gaussian'?L.gaussian:L.discrete)}"><svg data-graphic="main" role="img" width="640" height="330" viewBox="0 0 640 330" aria-label="${esc(kind==='gaussian'?L.gaussian:L.discrete)}"></svg></div>
      <div class="gibbs-lab-scroll gibbs-lab-diagnostic" tabindex="0" role="region" aria-label="${esc(kind==='gaussian'?L.diagnosticsGaussian:L.diagnosticsDisconnected)}"><svg data-graphic="diagnostic" width="640" height="170" viewBox="0 0 640 170" role="img" aria-label="${esc(kind==='gaussian'?L.diagnosticsGaussian:L.diagnosticsDisconnected)}"></svg></div>
      <p class="gibbs-lab-hint">${L.scroll}</p><p class="gibbs-lab-status" role="status" aria-live="polite" data-status></p><p class="gibbs-lab-note">${L.note}</p>
    </div>`;
    const q=s=>host.querySelector(s);
    const svg=q('svg[data-graphic="main"]');
    const poly=coords=>coords.map(p=>`${p[0].toFixed(1)},${p[1].toFixed(1)}`).join(' ');
    // Diagnostics are *analytic properties of the transition kernel*, never sample estimates.
    function diagnostic() {
      const chart=q('svg[data-graphic="diagnostic"]');
      const box='<rect width="640" height="170" rx="12" fill="#f5f9fc"/><rect x="9" y="8" width="622" height="153" rx="10" fill="#fff" stroke="#d9e5ec"/>';
      if(kind==='gaussian') {
        // Exact stationary variance-equivalent ESS for the sample mean of N=100
        // full-sweep Y values: Corr(Y_t,Y_{t+k}) = rho^(2k).
        const N=100, ess=r=>{
          let inflation=1;
          for(let k=1;k<N;k++)inflation+=2*(1-k/N)*r**(2*k);
          return N/inflation;
        };
        const px=r=>90+460*r/.95, py=n=>130-82*n/N;
        const curve=Array.from({length:39},(_,i)=>{const r=.95*i/38;return `${px(r).toFixed(2)},${py(ess(r)).toFixed(2)}`;}).join(' ');
        const effective=ess(state.rho), mx=px(state.rho), my=py(effective);
        chart.innerHTML=`${box}<text x="23" y="30" font-size="15" font-weight="700" fill="#244259">Stationary mean ESS</text><text x="416" y="30" font-size="12" fill="#4c6275">N = 100 sweeps</text>
          <line x1="90" y1="48" x2="90" y2="130" stroke="#728fa1"/><line x1="90" y1="130" x2="550" y2="130" stroke="#728fa1"/>
          <line x1="90" y1="89" x2="550" y2="89" stroke="#dfe8ee" stroke-dasharray="4 5"/>
          <text x="54" y="53" font-size="12" fill="#506779">100</text><text x="62" y="94" font-size="12" fill="#506779">50</text><text x="69" y="134" font-size="12" fill="#506779">0</text>
          <polyline points="${curve}" fill="none" stroke="#168b88" stroke-width="3" stroke-linecap="round"/>
          <line x1="${mx.toFixed(2)}" y1="${my.toFixed(2)}" x2="${mx.toFixed(2)}" y2="130" stroke="#d59449" stroke-width="1.7" stroke-dasharray="5 4"/>
          <circle data-ess="${effective.toFixed(3)}" cx="${mx.toFixed(2)}" cy="${my.toFixed(2)}" r="6" stroke="#fff" stroke-width="2" fill="#d59449"/>
          <text x="90" y="150" font-size="12" fill="#506779">0</text><text x="317" y="150" font-size="12" fill="#506779">0.5</text><text x="529" y="150" font-size="12" fill="#506779">0.95</text>
          <text x="572" y="150" font-size="13" fill="#506779">ρ</text><text x="565" y="70" font-size="13" font-weight="700" fill="#177a77">${effective.toFixed(1)}</text>`;
      } else {
        // Exact P^n on the two supported modes: I for single-site, Pi for joint draw.
        const tv=state.mode==='single'||state.step===0?.5:0;
        const px=n=>94+n*55, py=d=>130-154*d;
        const single=Array.from({length:9},(_,n)=>`${px(n)},${py(.5)}`).join(' ');
        const block=Array.from({length:9},(_,n)=>`${px(n)},${py(n===0?.5:0)}`).join(' ');
        const xx=px(state.step), yy=py(tv);
        chart.innerHTML=`${box}<text x="22" y="29" font-size="15" font-weight="700" fill="#244259">TV distance to target</text>
          <line x1="94" y1="53" x2="94" y2="130" stroke="#728fa1"/><line x1="94" y1="130" x2="534" y2="130" stroke="#728fa1"/>
          <text x="59" y="58" font-size="12" fill="#506779">0.5</text><text x="68" y="134" font-size="12" fill="#506779">0</text>
          <polyline points="${single}" fill="none" stroke="#d59449" stroke-width="3"/>
          <polyline points="${block}" fill="none" stroke="#168b88" stroke-width="3.5" stroke-linejoin="round"/>
          <circle data-tv="${tv.toFixed(3)}" cx="${xx}" cy="${yy}" r="6.5" fill="${state.mode==='single'?'#d59449':'#168b88'}" stroke="#fff" stroke-width="2"/>
          <text x="88" y="151" font-size="12" fill="#506779">0</text><text x="143" y="151" font-size="12" fill="#506779">1</text><text x="527" y="151" font-size="12" fill="#506779">8</text>
          <text x="558" y="151" font-size="12" fill="#506779">step</text>
          <line x1="325" y1="23" x2="344" y2="23" stroke="#d59449" stroke-width="3"/><text x="350" y="27" font-size="11" fill="#506779">Single-site</text>
          <line x1="457" y1="23" x2="476" y2="23" stroke="#168b88" stroke-width="3"/><text x="482" y="27" font-size="11" fill="#506779">Block</text>`;
      }
    }
    function gaussian() {
      const s=getStates(state.rho), cur=s[state.step], xx=x=>222+x*57, yy=y=>182-y*57;
      const grid=[-2,-1,0,1,2].map(v=>`<line x1="${xx(v)}" y1="55" x2="${xx(v)}" y2="295" stroke="#e4edf2"/><line x1="83" y1="${yy(v)}" x2="359" y2="${yy(v)}" stroke="#e4edf2"/>`).join('');
      const track=s.slice(0,state.step+1).map(p=>[xx(p.x),yy(p.y)]);
      const contours=[0.7,1.15,1.55].map(c=>`<ellipse cx="222" cy="182" rx="${(57*c*Math.sqrt(1+state.rho)).toFixed(2)}" ry="${(57*c*Math.sqrt(1-state.rho)).toFixed(2)}" transform="rotate(-45 222 182)" fill="none" stroke="#a8cdcb" stroke-width="1.5"/>`).join('');
      const p=state.step? s[state.step-1] : cur;
      const fixed=state.step? (state.step%2 ? `<line x1="83" y1="${yy(p.y)}" x2="359" y2="${yy(p.y)}" stroke="#e39b4c" stroke-width="2" stroke-dasharray="5 5"/>` : `<line x1="${xx(p.x)}" y1="55" x2="${xx(p.x)}" y2="295" stroke="#e39b4c" stroke-width="2" stroke-dasharray="5 5"/>`) : '';
      const path=track.length>1?`<polyline points="${poly(track)}" fill="none" stroke="#128f87" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/>`:'';
      const bar=(k)=>{const ac=state.rho**(2*k),x=445,y=115+k*35;return `<text x="416" y="${y+15}" fill="#4c6275" font-size="13">${k}</text><rect x="${x}" y="${y}" width="140" height="17" rx="3" fill="#e9f0f4"/><rect data-acf="${k}" x="${x}" y="${y}" width="${(140*ac).toFixed(2)}" height="17" rx="3" fill="#2283a4"/><text x="590" y="${y+15}" font-size="11" fill="#365166">${ac.toFixed(3)}</text>`};
      svg.innerHTML=`<rect width="640" height="330" rx="16" fill="#f5f9fc"/><rect x="15" y="18" width="376" height="297" rx="12" fill="#fff" stroke="#d9e5ec"/><rect x="402" y="18" width="223" height="297" rx="12" fill="#fff" stroke="#d9e5ec"/>
      <text x="33" y="44" fill="#244259" font-size="16" font-weight="700">Gaussian Gibbs</text><text x="418" y="43" fill="#244259" font-size="16" font-weight="700">Lag ACF</text>
      ${grid}<line x1="83" y1="295" x2="360" y2="295" stroke="#748ea0"/><line x1="83" y1="55" x2="83" y2="295" stroke="#748ea0"/>
      <text x="362" y="311" font-size="13" fill="#60778a">x</text><text x="71" y="65" font-size="13" fill="#60778a">y</text>
      ${contours}${fixed}${path}<circle cx="${xx(cur.x).toFixed(2)}" cy="${yy(cur.y).toFixed(2)}" r="8.5" fill="#128f87" stroke="#fff" stroke-width="3"/>
      <text x="34" y="311" font-size="12" fill="#60778a">${state.step%2?'X | Y':'Y | X'} · ${state.step}/10</text>
      <text x="418" y="70" font-size="12" fill="#506779">ρ² = ${(state.rho**2).toFixed(3)}</text><text x="418" y="98" font-size="12" fill="#60778a">Full-sweep lag</text>
      ${[1,2,3,4,5].map(bar).join('')}`;
      q('[data-status]').textContent=L.gab({...cur,step:state.step,rho:state.rho});diagnostic();
    }
    function disconnected() {
      const bit=state.mode==='single'?state.start:(state.step===0?state.start:uniforms[state.step-1]>0.5?1:0);
      const pts=[[165,227],[265,227],[165,128],[265,128]], labels=['(0,0)','(1,0)','(0,1)','(1,1)'];
      const node=(index)=>{const viable=index===0||index===3, current=(bit===0&&index===0)||(bit===1&&index===3);const [x,y]=pts[index];return `<circle cx="${x}" cy="${y}" r="29" fill="${viable?(current?'#0a847a':'#e3f2ef'):'#e7ecf0'}" stroke="${current?'#0b665e':'#b6c7d2'}" stroke-width="${current?4:1.5}"/><text x="${x}" y="${y+5}" font-size="14" font-weight="600" text-anchor="middle" fill="${current?'#fff':'#526a7c'}">${labels[index]}</text>`};
      svg.innerHTML=`<rect width="640" height="330" rx="16" fill="#f5f9fc"/><rect x="16" y="18" width="375" height="294" rx="12" fill="#fff" stroke="#d9e5ec"/><rect x="403" y="18" width="222" height="294" rx="12" fill="#fff" stroke="#d9e5ec"/>
      <text x="33" y="44" fill="#244259" font-size="16" font-weight="700">Target support</text><text x="417" y="44" fill="#244259" font-size="16" font-weight="700">Transition</text>
      <line x1="165" y1="227" x2="265" y2="128" stroke="${state.mode==='block'?'#128f87':'#c7d5dc'}" stroke-width="${state.mode==='block'?5:3}" stroke-dasharray="${state.mode==='block'?'7 6':'3 8'}"/>
      ${[1,2,0,3].map(node).join('')}
      <text x="95" y="279" font-size="13" fill="#557187">Support: (0,0), (1,1)</text>
      <text x="420" y="83" font-size="13" fill="#557187">${state.mode==='block'?'Joint block':'Single-site'}</text>
      <text x="420" y="121" font-size="27" font-weight="700" fill="#0c8177">${state.mode==='block'?'0.5 / 0.5':'P(stay)=1'}</text>
      <text x="420" y="172" font-size="13" fill="#557187">${state.mode==='block'?'Both modes reachable':'Cannot leave mode'}</text>
      <rect x="422" y="207" width="172" height="28" rx="5" fill="#e7f1f5"/><rect x="422" y="207" width="${172*state.step/max}" height="28" rx="5" fill="#91c7c2"/>
      <text x="420" y="265" font-size="13" fill="#4c6676">Step ${state.step} / ${max}</text>`;
      q('[data-status]').textContent=L.dib({...state,bit});diagnostic();
    }
    const render=()=>{q('[data-field="step"]').value=String(state.step);q('[data-value="step"]').textContent=`${state.step}/${max}`;if(kind==='gaussian'){q('[data-value="rho"]').textContent=state.rho.toFixed(2);gaussian()}else disconnected()};
    const stop=()=>{if(state.timer!==null)clearInterval(state.timer);state.timer=null;q('[data-action="play"]').textContent=L.play;};
    const play=()=>{if(state.timer!==null){stop();return;}if(state.step===max)state.step=0;q('[data-action="play"]').textContent=L.pause;state.timer=setInterval(()=>{state.step=Math.min(max,state.step+1);render();if(state.step===max)stop();},950/state.speed);render();};
    q('[data-action="play"]').addEventListener('click',play);
    q('[data-action="prev"]').addEventListener('click',()=>{stop();state.step=Math.max(0,state.step-1);render()});
    q('[data-action="next"]').addEventListener('click',()=>{stop();state.step=Math.min(max,state.step+1);render()});
    q('[data-action="reset"]').addEventListener('click',()=>{stop();state.step=0;state.rho=0.8;state.mode='single';state.start=0;state.speed=1;q('[data-field="speed"]').value='1';if(kind==='gaussian')q('[data-field="rho"]').value='0.8';else{q('[data-field="mode"]').value='single';q('[data-field="start"]').value='0';}render()});
    q('[data-field="step"]').addEventListener('input',e=>{stop();state.step=Number(e.target.value);render()});
    q('[data-field="speed"]').addEventListener('change',e=>{const running=state.timer!==null;stop();state.speed=Number(e.target.value);if(running)play()});
    if(kind==='gaussian')q('[data-field="rho"]').addEventListener('input',e=>{stop();state.rho=Number(e.target.value);render()});
    else{q('[data-field="mode"]').addEventListener('change',e=>{stop();state.mode=e.target.value;render()});q('[data-field="start"]').addEventListener('change',e=>{stop();state.start=Number(e.target.value);render()})}
    document.addEventListener('visibilitychange',()=>{if(document.hidden)stop()});
    const motion=window.matchMedia('(prefers-reduced-motion: reduce)');motion.addEventListener?.('change',()=>{if(motion.matches)stop()});
    render();
  }
  const enhance=()=>document.querySelectorAll('[data-gibbs-lab]').forEach(init);
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',enhance);else enhance();
  if(window.document$?.subscribe)window.document$.subscribe(enhance);
})();

