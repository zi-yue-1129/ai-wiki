/* Deterministic, original Gibbs teaching models. No random draws or external dependencies. */
(() => {
  'use strict';
  const translations = {
    en: { previous:'Previous',next:'Next',play:'Play',pause:'Pause',reset:'Reset',step:'Step',speed:'Speed',
      rho:'Target correlation ρ', scan:'Update kernel',mixed:'Hybrid refresh',refresh:'Block refresh probability p',start:'Initial state',single:'Single-site Gibbs',block:'Joint block draw',
      note:'Synthetic, fixed innovations and uniform variates; not measured MCMC output or random simulations.',
      gaussian:'Correlated Gaussian: conditional updates and stationary lag autocorrelation',
      discrete:'Two-mode discrete target: single-coordinate trapping versus a joint block draw',
      scroll:'Focus this figure and scroll horizontally to read its full labels.',
      a:'Gaussian sweep',b:'Disconnected target',fixed:'Fixed coordinate',
      reduced:'Reduced-motion is enabled: playback will not start automatically.',
      diagnosticsGaussian:'Theoretical finite-sample effective size of the stationary Gibbs Y mean for 100 full sweeps as target correlation varies.',
      diagnosticsDisconnected:'Exact total variation distance from a point start to the two-mode target after each complete kernel transition.',
      gab:(s)=>`Step ${s.step} of 10; ρ ${s.rho.toFixed(2)}; X ${s.x.toFixed(3)}, Y ${s.y.toFixed(3)}; stationary lag-one correlation ρ² ${(s.rho*s.rho).toFixed(3)}; conditional σ ${Math.sqrt(1-s.rho*s.rho).toFixed(3)}.${s.step ? ` ${s.axis} conditional mean ${s.mean.toFixed(3)}; fixed standard-normal innovation ${s.z.toFixed(2)}.` : ''}`,
      dib:(s)=>`Step ${s.step} of 8; ${s.mode==='single'?'single-site conditional, fixed':'joint block conditional, possibly switching'}; current state (${s.bit},${s.bit}); P(next 00) ${s.p00.toFixed(2)}, P(next 11) ${s.p11.toFixed(2)}; block refresh p=${s.p.toFixed(2)}.`
    },
    zh: { previous:'上一步',next:'下一步',play:'播放',pause:'暫停',reset:'重設',step:'步驟',speed:'速度',
      rho:'目標相關係數 ρ',scan:'更新方式',mixed:'混合更新',refresh:'分塊刷新機率 p',start:'初始狀態',single:'逐座標 Gibbs',block:'聯合分塊抽樣',
      note:'固定的人工常態創新與均勻數值，非實測 MCMC 輸出或真正隨機模擬。',
      gaussian:'相關高斯：條件更新路徑及平穩態的延遲自相關',
      discrete:'雙模態離散目標：逐座標受困與聯合抽樣跨模態',
      scroll:'可聚焦此圖並水平捲動，閱讀完整標籤。',
      a:'高斯掃描',b:'不連通目標',fixed:'固定的座標',
      reduced:'已開啟減少動態效果，不會自動播放。',
      diagnosticsGaussian:'相關高斯 Gibbs 平穩態 Y 平均數在一百輪完整掃描下，理論有限樣本有效樣本數隨相關係數變化的圖。',
      diagnosticsDisconnected:'從單一支援點出發，每次完整更新後與雙模態目標分布之間的精確總變異距離。',
      gab:(s)=>`第 ${s.step}/10 步；ρ=${s.rho.toFixed(2)}；X=${s.x.toFixed(3)}，Y=${s.y.toFixed(3)}；平穩態單輪延遲相關 ρ²=${(s.rho*s.rho).toFixed(3)}；條件標準差 σ=${Math.sqrt(1-s.rho*s.rho).toFixed(3)}。${s.step ? `本步 ${s.axis} 條件平均 ${s.mean.toFixed(3)}；固定標準常態創新 ${s.z.toFixed(2)}。` : ''}`,
      dib:(s)=>`第 ${s.step}/8 步；${s.mode==='single'?'逐座標抽樣受困':'聯合分塊抽樣可跨模態'}；目前為 (${s.bit},${s.bit})；下一步到 (0,0) 的機率 ${s.p00.toFixed(2)}，到 (1,1) 的機率 ${s.p11.toFixed(2)}；分塊刷新 p=${s.p.toFixed(2)}。`
    }
  };
  const esc = s => String(s).replace(/[&<>"']/g, ch => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;','\'':'&#39;'}[ch]));
  const innovations = [0.5,-1,-0.7,0.8,0.2,-0.6,-0.3,0.7,0.9,-0.4];
  const uniforms = [0.8,0.2,0.9,0.1,0.7,0.3,0.6,0.4];
  const refreshUniforms = [0.15,0.85,0.2,0.4,0.05,0.75,0.1,0.6];
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
    const state={step:0,rho:0.8,mode:'single',refresh:0.25,start:0,speed:1,timer:null};
    const opts=(name,options)=>`<label class="gibbs-lab-field">${esc(name)} <select data-field="${name===L.scan?'mode':'start'}">${options.map(([v,label])=>`<option value="${v}">${esc(label)}</option>`).join('')}</select></label>`;
    host.innerHTML=`<div class="gibbs-lab-panel">
      <div class="gibbs-lab-controls"><button type="button" data-action="prev">${L.previous}</button><button type="button" data-action="play">${L.play}</button><button type="button" data-action="next">${L.next}</button>
      <label class="gibbs-lab-field">${L.step} <input aria-label="${L.step}" type="range" data-field="step" min="0" max="${max}" step="1" value="0"><output data-value="step">0/${max}</output></label>
      <label class="gibbs-lab-field">${L.speed} <select data-field="speed"><option value="0.5">0.5×</option><option value="1" selected>1×</option><option value="2">2×</option></select></label>
      <button type="button" data-action="reset">${L.reset}</button></div>
      <div class="gibbs-lab-parameters">${kind==='gaussian'?`<label class="gibbs-lab-field">${L.rho} <input aria-label="${L.rho}" type="range" min="-0.95" max="0.95" step="0.05" value="0.8" data-field="rho"><output data-value="rho">0.80</output></label>`:opts(L.scan,[['single',L.single],['block',L.block],['mix',L.mixed]])+opts(L.start,[[0,'(0,0)'],[1,'(1,1)']])+`<label class="gibbs-lab-field">${L.refresh} <input aria-label="${L.refresh}" type="range" min="0" max="1" step="0.05" value="0.25" data-field="refresh"><output data-value="refresh">0.25</output></label>`}</div>
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
        const px=r=>90+460*(r+.95)/1.9, py=n=>130-82*n/N;
        const curve=Array.from({length:77},(_,i)=>{const r=-.95+1.9*i/76;return `${px(r).toFixed(2)},${py(ess(r)).toFixed(2)}`;}).join(' ');
        const effective=ess(state.rho), mx=px(state.rho), my=py(effective);
        chart.innerHTML=`${box}<text x="23" y="30" font-size="15" font-weight="700" fill="#244259">Stationary mean ESS</text><text x="416" y="30" font-size="12" fill="#4c6275">N = 100 sweeps</text>
          <line x1="90" y1="48" x2="90" y2="130" stroke="#728fa1"/><line x1="90" y1="130" x2="550" y2="130" stroke="#728fa1"/>
          <line x1="90" y1="89" x2="550" y2="89" stroke="#dfe8ee" stroke-dasharray="4 5"/>
          <text x="54" y="53" font-size="12" fill="#506779">100</text><text x="62" y="94" font-size="12" fill="#506779">50</text><text x="69" y="134" font-size="12" fill="#506779">0</text>
          <polyline points="${curve}" fill="none" stroke="#168b88" stroke-width="3" stroke-linecap="round"/>
          <line x1="${mx.toFixed(2)}" y1="${my.toFixed(2)}" x2="${mx.toFixed(2)}" y2="130" stroke="#d59449" stroke-width="1.7" stroke-dasharray="5 4"/>
          <circle data-ess="${effective.toFixed(3)}" cx="${mx.toFixed(2)}" cy="${my.toFixed(2)}" r="6" stroke="#fff" stroke-width="2" fill="#d59449"/>
          <text x="78" y="150" font-size="12" fill="#506779">−0.95</text><text x="316" y="150" font-size="12" fill="#506779">0</text><text x="525" y="150" font-size="12" fill="#506779">+0.95</text>
          <text x="572" y="150" font-size="13" fill="#506779">ρ</text><text x="565" y="70" font-size="13" font-weight="700" fill="#177a77">${effective.toFixed(1)}</text>`;
      } else {
        // Exact P^n on the two supported modes: I for single-site, Pi for joint draw.
        const p=state.mode==='single'?0:state.mode==='block'?1:state.refresh;
        const tv=.5*(1-p)**state.step;
        const px=n=>94+n*55, py=d=>130-154*d;
        const single=Array.from({length:9},(_,n)=>`${px(n)},${py(.5)}`).join(' ');
        const block=Array.from({length:9},(_,n)=>`${px(n)},${py(n===0?.5:0)}`).join(' ');
        const mixed=Array.from({length:9},(_,n)=>`${px(n)},${py(.5*(1-(state.mode==='mix'?state.refresh:.25))**n)}`).join(' ');
        const xx=px(state.step), yy=py(tv);
        chart.innerHTML=`${box}<text x="22" y="29" font-size="15" font-weight="700" fill="#244259">TV distance to target</text>
          <line x1="94" y1="53" x2="94" y2="130" stroke="#728fa1"/><line x1="94" y1="130" x2="534" y2="130" stroke="#728fa1"/>
          <text x="59" y="58" font-size="12" fill="#506779">0.5</text><text x="68" y="134" font-size="12" fill="#506779">0</text>
          <polyline points="${single}" fill="none" stroke="#d59449" stroke-width="3"/>
          <polyline points="${block}" fill="none" stroke="#168b88" stroke-width="3.5" stroke-linejoin="round"/><polyline data-hybrid-curve points="${mixed}" fill="none" stroke="#8e5aaa" stroke-width="3.2" stroke-linejoin="round"/>
          <circle data-tv="${tv.toFixed(3)}" cx="${xx}" cy="${yy}" r="6.5" fill="${state.mode==='single'?'#d59449':state.mode==='block'?'#168b88':'#8e5aaa'}" stroke="#fff" stroke-width="2"/>
          <text x="88" y="151" font-size="12" fill="#506779">0</text><text x="143" y="151" font-size="12" fill="#506779">1</text><text x="527" y="151" font-size="12" fill="#506779">8</text>
          <text x="558" y="151" font-size="12" fill="#506779">step</text>
          <line x1="325" y1="23" x2="344" y2="23" stroke="#d59449" stroke-width="3"/><text x="350" y="27" font-size="11" fill="#506779">Single-site</text>
          <line x1="457" y1="23" x2="476" y2="23" stroke="#168b88" stroke-width="3"/><text x="482" y="27" font-size="11" fill="#506779">Block</text><line x1="545" y1="23" x2="559" y2="23" stroke="#8e5aaa" stroke-width="3"/><text x="566" y="27" font-size="11" fill="#506779">Mix</text>`;
      }
    }
    function gaussian() {
      const s=getStates(state.rho), cur=s[state.step], xx=x=>222+x*57, yy=y=>182-y*57;
      const grid=[-2,-1,0,1,2].map(v=>`<line x1="${xx(v)}" y1="55" x2="${xx(v)}" y2="295" stroke="#e4edf2"/><line x1="83" y1="${yy(v)}" x2="359" y2="${yy(v)}" stroke="#e4edf2"/>`).join('');
      const track=s.slice(0,state.step+1).map(p=>[xx(p.x),yy(p.y)]);
      const contours=[0.7,1.15,1.55].map(c=>`<ellipse cx="222" cy="182" rx="${(57*c*Math.sqrt(1+state.rho)).toFixed(2)}" ry="${(57*c*Math.sqrt(1-state.rho)).toFixed(2)}" transform="rotate(-45 222 182)" fill="none" stroke="#a8cdcb" stroke-width="1.5"/>`).join('');
      const p=state.step? s[state.step-1] : cur;
      // The hollow purple point is E[updated coordinate | fixed coordinate], NOT a sampled state.
      const updatingX=state.step%2===1;
      const mean=state.step ? state.rho*(updatingX?p.y:p.x) : 0;
      const m=updatingX ? {x:mean,y:p.y} : {x:p.x,y:mean};
      const sigma=Math.sqrt(1-state.rho*state.rho);
      const band=state.step ? (updatingX
        ? `<rect data-cond-sigma="${sigma.toFixed(3)}" x="${xx(mean-sigma).toFixed(2)}" y="${(yy(p.y)-10).toFixed(2)}" width="${(114*sigma).toFixed(2)}" height="20" rx="5" fill="#8e5aaa" fill-opacity=".15" stroke="#8e5aaa" stroke-opacity=".5" stroke-width="1.2"/>`
        : `<rect data-cond-sigma="${sigma.toFixed(3)}" x="${(xx(p.x)-10).toFixed(2)}" y="${yy(mean+sigma).toFixed(2)}" width="20" height="${(114*sigma).toFixed(2)}" rx="5" fill="#8e5aaa" fill-opacity=".15" stroke="#8e5aaa" stroke-opacity=".5" stroke-width="1.2"/>`) : '';
      const meanDot=state.step ? `<line x1="${xx(m.x).toFixed(2)}" y1="${yy(m.y).toFixed(2)}" x2="${xx(cur.x).toFixed(2)}" y2="${yy(cur.y).toFixed(2)}" stroke="#8e5aaa" stroke-dasharray="3 4" stroke-width="2"/><circle data-conditional-mean="${mean.toFixed(3)}" cx="${xx(m.x).toFixed(2)}" cy="${yy(m.y).toFixed(2)}" r="6.3" fill="#fff" stroke="#8e5aaa" stroke-width="2.5"/>` : '';
      const fixed=state.step? (state.step%2 ? `<line x1="83" y1="${yy(p.y)}" x2="359" y2="${yy(p.y)}" stroke="#e39b4c" stroke-width="2" stroke-dasharray="5 5"/>` : `<line x1="${xx(p.x)}" y1="55" x2="${xx(p.x)}" y2="295" stroke="#e39b4c" stroke-width="2" stroke-dasharray="5 5"/>`) : '';
      const path=track.length>1?`<polyline points="${poly(track)}" fill="none" stroke="#128f87" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/>`:'';
      const bar=(k)=>{const ac=state.rho**(2*k),x=445,y=115+k*35;return `<text x="416" y="${y+15}" fill="#4c6275" font-size="13">${k}</text><rect x="${x}" y="${y}" width="140" height="17" rx="3" fill="#e9f0f4"/><rect data-acf="${k}" x="${x}" y="${y}" width="${(140*ac).toFixed(2)}" height="17" rx="3" fill="#2283a4"/><text x="590" y="${y+15}" font-size="11" fill="#365166">${ac.toFixed(3)}</text>`};
      svg.innerHTML=`<rect width="640" height="330" rx="16" fill="#f5f9fc"/><rect x="15" y="18" width="376" height="297" rx="12" fill="#fff" stroke="#d9e5ec"/><rect x="402" y="18" width="223" height="297" rx="12" fill="#fff" stroke="#d9e5ec"/>
      <text x="33" y="44" fill="#244259" font-size="16" font-weight="700">Gaussian Gibbs</text><circle cx="335" cy="39" r="5" fill="#fff" stroke="#8e5aaa" stroke-width="2"/><text x="346" y="44" font-size="13" fill="#8e5aaa">μ</text><text x="261" y="44" font-size="11" fill="#8e5aaa">±1σ ${sigma.toFixed(3)}</text><text x="418" y="43" fill="#244259" font-size="16" font-weight="700">Lag ACF</text>
      ${grid}<line x1="83" y1="295" x2="360" y2="295" stroke="#748ea0"/><line x1="83" y1="55" x2="83" y2="295" stroke="#748ea0"/>
      <text x="362" y="311" font-size="13" fill="#60778a">x</text><text x="71" y="65" font-size="13" fill="#60778a">y</text>
      ${contours}${fixed}${path}${band}${meanDot}<circle cx="${xx(cur.x).toFixed(2)}" cy="${yy(cur.y).toFixed(2)}" r="8.5" fill="#128f87" stroke="#fff" stroke-width="3"/>
      <text x="34" y="311" font-size="12" fill="#60778a">${state.step===0?'Start':state.step%2?'X | Y':'Y | X'} · ${state.step}/10</text>
      <text x="418" y="70" font-size="12" fill="#506779">ρ² = ${(state.rho**2).toFixed(3)}</text><text x="418" y="98" font-size="12" fill="#60778a">Full-sweep lag</text>
      ${[1,2,3,4,5].map(bar).join('')}`;
      q('[data-status]').textContent=L.gab({...cur,step:state.step,rho:state.rho,axis:updatingX?'X':'Y',mean,z:state.step?innovations[state.step-1]:0});diagnostic();
    }
    function disconnected() {
      const p=state.mode==='single'?0:state.mode==='block'?1:state.refresh;
      let bit=state.start;
      for(let i=0;i<state.step;i++)if(state.mode==='block'||(state.mode==='mix'&&refreshUniforms[i]<p))bit=uniforms[i]>0.5?1:0;
      const p00=bit===0?1-p/2:p/2, p11=1-p00;
      const pts=[[165,227],[265,227],[165,128],[265,128]], labels=['(0,0)','(1,0)','(0,1)','(1,1)'];
      const node=(index)=>{const viable=index===0||index===3, current=(bit===0&&index===0)||(bit===1&&index===3);const [x,y]=pts[index];return `<circle cx="${x}" cy="${y}" r="29" fill="${viable?(current?'#0a847a':'#e3f2ef'):'#e7ecf0'}" stroke="${current?'#0b665e':'#b6c7d2'}" stroke-width="${current?4:1.5}"/><text x="${x}" y="${y+5}" font-size="14" font-weight="600" text-anchor="middle" fill="${current?'#fff':'#526a7c'}">${labels[index]}</text>`};
      svg.innerHTML=`<rect width="640" height="330" rx="16" fill="#f5f9fc"/><rect x="16" y="18" width="375" height="294" rx="12" fill="#fff" stroke="#d9e5ec"/><rect x="403" y="18" width="222" height="294" rx="12" fill="#fff" stroke="#d9e5ec"/>
      <text x="33" y="44" fill="#244259" font-size="16" font-weight="700">Target support</text><text x="417" y="44" fill="#244259" font-size="16" font-weight="700">Transition</text>
      <line x1="165" y1="227" x2="265" y2="128" stroke="${state.mode==='single'?'#c7d5dc':'#128f87'}" stroke-width="${state.mode==='single'?3:5}" stroke-dasharray="${state.mode==='single'?'3 8':'7 6'}"/>
      ${[1,2,0,3].map(node).join('')}
      <text x="95" y="279" font-size="13" fill="#557187">Support: (0,0), (1,1)</text>
      <text x="420" y="84" font-size="13" fill="#557187">${state.mode==='block'?'Joint block':state.mode==='mix'?'Hybrid':'Single-site'} · from ${bit}</text>
      <text x="419" y="120" font-size="12" fill="#526a7c">→ 00</text><rect x="460" y="105" width="119" height="17" rx="3" fill="#e7eff4"/><rect data-to="00" data-probability="${p00.toFixed(3)}" x="460" y="105" width="${(119*p00).toFixed(2)}" height="17" rx="3" fill="#218a87"/><text x="586" y="119" font-size="12" fill="#365166">${p00.toFixed(2)}</text>
      <text x="419" y="165" font-size="12" fill="#526a7c">→ 11</text><rect x="460" y="150" width="119" height="17" rx="3" fill="#e7eff4"/><rect data-to="11" data-probability="${p11.toFixed(3)}" x="460" y="150" width="${(119*p11).toFixed(2)}" height="17" rx="3" fill="#218a87"/><text x="586" y="164" font-size="12" fill="#365166">${p11.toFixed(2)}</text>
      <text x="420" y="197" font-size="12" fill="#557187">Kernel transition probabilities</text>
      <rect x="422" y="222" width="172" height="27" rx="5" fill="#e7f1f5"/><rect x="422" y="222" width="${172*state.step/max}" height="27" rx="5" fill="#91c7c2"/>
      <text x="420" y="279" font-size="13" fill="#4c6676">Step ${state.step} / ${max}</text>`;
      q('[data-status]').textContent=L.dib({...state,bit,p00,p11,p});diagnostic();
    }
    const render=()=>{q('[data-field="step"]').value=String(state.step);q('[data-value="step"]').textContent=`${state.step}/${max}`;if(kind==='gaussian'){q('[data-value="rho"]').textContent=state.rho.toFixed(2);gaussian()}else{q('[data-value="refresh"]').textContent=state.refresh.toFixed(2);q('[data-field="refresh"]').disabled=state.mode!=='mix';disconnected()}};
    const stop=()=>{if(state.timer!==null)clearInterval(state.timer);state.timer=null;q('[data-action="play"]').textContent=L.play;};
    const play=()=>{if(state.timer!==null){stop();return;}if(state.step===max)state.step=0;q('[data-action="play"]').textContent=L.pause;state.timer=setInterval(()=>{state.step=Math.min(max,state.step+1);render();if(state.step===max)stop();},950/state.speed);render();};
    q('[data-action="play"]').addEventListener('click',play);
    q('[data-action="prev"]').addEventListener('click',()=>{stop();state.step=Math.max(0,state.step-1);render()});
    q('[data-action="next"]').addEventListener('click',()=>{stop();state.step=Math.min(max,state.step+1);render()});
    q('[data-action="reset"]').addEventListener('click',()=>{stop();state.step=0;state.rho=0.8;state.mode='single';state.refresh=.25;state.start=0;state.speed=1;q('[data-field="speed"]').value='1';if(kind==='gaussian')q('[data-field="rho"]').value='0.8';else{q('[data-field="mode"]').value='single';q('[data-field="start"]').value='0';q('[data-field="refresh"]').value='0.25';}render()});
    q('[data-field="step"]').addEventListener('input',e=>{stop();state.step=Number(e.target.value);render()});
    q('[data-field="speed"]').addEventListener('change',e=>{const running=state.timer!==null;stop();state.speed=Number(e.target.value);if(running)play()});
    if(kind==='gaussian')q('[data-field="rho"]').addEventListener('input',e=>{stop();state.rho=Number(e.target.value);render()});
    else{q('[data-field="mode"]').addEventListener('change',e=>{stop();state.mode=e.target.value;render()});q('[data-field="start"]').addEventListener('change',e=>{stop();state.start=Number(e.target.value);render()});q('[data-field="refresh"]').addEventListener('input',e=>{stop();state.refresh=Number(e.target.value);render()})}
    document.addEventListener('visibilitychange',()=>{if(document.hidden)stop()});
    const motion=window.matchMedia('(prefers-reduced-motion: reduce)');motion.addEventListener?.('change',()=>{if(motion.matches)stop()});
    render();
  }
  const enhance=()=>document.querySelectorAll('[data-gibbs-lab]').forEach(init);
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',enhance);else enhance();
  if(window.document$?.subscribe)window.document$.subscribe(enhance);
})();

