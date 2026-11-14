/* Original, deterministic S4D / SSD teaching simulations (CC BY-SA 4.0).
 * Built with native controls, no dependencies, network or random numbers.
 */
(() => {
  'use strict';
  const clamp = (x, lo, hi) => Math.max(lo, Math.min(hi, x));
  const fmt = x => (Math.abs(x) < 0.0005 ? 0 : x).toFixed(3);
  const n = (x, fallback) => Number.isFinite(Number(x)) ? Number(x) : fallback;
  const el = (host, selector) => host.querySelector(selector);
  const t = (en, zh, chinese) => chinese ? zh : en;
  const escapeLabel = value => String(value).replace(/[&<>"']/g, '');
  const poly = (values, colour, x, y) => `<polyline points="${values.map((v,i)=>`${x(i)},${y(v)}`).join(' ')}" fill="none" stroke="${colour}" stroke-width="3" stroke-linejoin="round" stroke-linecap="round"/>`;
  const svgHead = `<svg viewBox="0 0 760 340" width="760" height="340" role="img" xmlns="http://www.w3.org/2000/svg">`;

  function s4d(state) {
    const a = Array.from({length:16},(_,i)=>Math.pow(state.decay,i)*Math.cos(state.freq*i));
    const b = Array.from({length:16},(_,i)=>.63*Math.pow(.93,i)*Math.cos(.32*i));
    const sum = a.map((v,i)=>v+b[i]);
    const x = i => (55+i*43.2).toFixed(1);
    const y = v => (170-v*70).toFixed(1);
    const grid=[-1.5,-.75,0,.75,1.5].map(v=>`<line x1="55" x2="704" y1="${y(v)}" y2="${y(v)}" stroke="#dce5ed" stroke-dasharray="3 5"/>`).join('');
    const i = state.step;
    const legend = [['#416dbb','A'],['#159b92','B'],['#e18b3c','K']].map(([c,s],index)=>`<circle cx="${510+index*68}" cy="30" r="5" fill="${c}"/><text x="${522+index*68}" y="34" font-size="14" fill="#314253">${s}</text>`).join('');
    const visual = svgHead+`<rect x="0" y="0" width="760" height="340" rx="12" fill="#f8fafc"/>${grid}<path d="M55 50V290H704" fill="none" stroke="#879bad" stroke-width="1.2"/><text x="15" y="53" font-size="12" fill="#516478">1.5</text><text x="17" y="294" font-size="12" fill="#516478">-1.5</text><text x="51" y="315" font-size="13" fill="#516478">0</text><text x="681" y="315" font-size="13" fill="#516478">15</text><text x="357" y="330" font-size="13" fill="#516478">lag</text>${legend}${poly(a,'#416dbb',x,y)}${poly(b,'#159b92',x,y)}${poly(sum,'#e18b3c',x,y)}<line x1="${x(i)}" x2="${x(i)}" y1="48" y2="291" stroke="#374e63" stroke-dasharray="5 5"/>${[[a[i],'#416dbb'],[b[i],'#159b92'],[sum[i],'#e18b3c']].map(([v,c])=>`<circle cx="${x(i)}" cy="${y(v)}" r="6" fill="${c}" stroke="#fff" stroke-width="2"/>`).join('')}<text x="70" y="38" fill="#314253" font-size="14">ℓ = ${i}</text></svg>`;
    return {visual, stats:[['Mode A',fmt(a[i])],['Mode B',fmt(b[i])],['Kernel',fmt(sum[i])]], equation:`K[${i}] = ${fmt(a[i])} + ${fmt(b[i])} = ${fmt(sum[i])}`,stepMax:15};
  }

  function ssd(state) {
    const x=[1,.7,-.6,state.lastInput], trans=[1,...state.transitions];
    const M=Array.from({length:4},(_,j)=>Array.from({length:4},(_,i)=>{
      if(i>j)return null;
      let p=1;for(let k=i+1;k<=j;k++)p*=trans[k];return p;
    }));
    const h=[];for(let j=0;j<4;j++)h[j]=trans[j]*(j?h[j-1]:0)+x[j];
    const mat=M.map((row,j)=>row.reduce((v,m,i)=>v+(m??0)*x[i],0));
    const error=Math.max(...mat.map((v,i)=>Math.abs(v-h[i])));
    const i=state.step;
    const cells=M.map((row,j)=>row.map((v,k)=>{
      let xx=425+k*72, yy=67+j*61, active=j===i&&v!==null;
      return `<rect x="${xx}" y="${yy}" width="66" height="55" rx="7" fill="${v===null?'#edf1f5':active?'#cae9e2':'#e2eaf4'}" stroke="${active?'#18847a':'#becdd9'}" stroke-width="${active?2:1}"/>${v===null?'':`<text x="${xx+33}" y="${yy+33}" text-anchor="middle" fill="#263d51" font-size="16">${v.toFixed(2)}</text>`}`;
    }).join('')).join('');
    const states=h.map((v,j)=>{
      const xx=65+j*83, yy=190-v*44;
      return `<line x1="${xx}" y1="188" x2="${xx}" y2="${yy}" stroke="${j===i?'#e18b3c':'#52a3a1'}" stroke-width="8" stroke-linecap="round"/><circle cx="${xx}" cy="${yy}" r="${j===i?10:6}" fill="${j===i?'#e18b3c':'#248c89'}"/><text x="${xx}" y="239" text-anchor="middle" fill="#33475b" font-size="13">${j+1}</text><text x="${xx}" y="${Math.min(yy-14,165)}" text-anchor="middle" fill="#33475b" font-size="13">${fmt(v)}</text>`;
    }).join('');
    const visual=svgHead+`<rect width="760" height="340" rx="12" fill="#f8fafc"/><text x="47" y="40" fill="#30475b" font-size="16">Recurrence</text><text x="425" y="40" fill="#30475b" font-size="16">Causal map</text><line x1="385" y1="28" x2="385" y2="298" stroke="#d6e1e9"/>${states}<path d="M42 190H352" stroke="#aabcc9" stroke-width="1.5"/>${cells}<text x="48" y="285" fill="#30475b" font-size="14">h${i+1} = ${fmt(h[i])}</text><text x="425" y="332" fill="#30475b" font-size="14">Mx = ${fmt(mat[i])}</text><text x="54" y="328" fill="#728397" font-size="13">t</text></svg>`;
    return {visual, stats:[['Recurrence',fmt(h[i])],['Matrix',fmt(mat[i])],['Max |difference|',error.toExponential(1)]],equation:`h${i+1} = ${fmt(trans[i])} × ${fmt(i?h[i-1]:0)} + ${fmt(x[i])} = ${fmt(h[i])}`,stepMax:3,error};
  }

  function mount(host) {
    if(host.dataset.ssmReady==='yes')return;
    const kind=host.dataset.ssmLab, chinese=host.dataset.lang==='zh';
    if(!['s4d','ssd'].includes(kind))return;
    host.dataset.ssmReady='yes';
    const name=kind==='s4d'?'S4D kernel':'SSD duality';
    const state=kind==='s4d'?{step:0,decay:.79,freq:.96}:{step:0,transitions:[.8,.7,.9],lastInput:1.1};
    const defaults=JSON.parse(JSON.stringify(state));
    const parameters=kind==='s4d'?
      [['decay',t('Mode A decay','模態 A 衰減係數',chinese),.55,.98,.01],['freq',t('Mode A frequency','模態 A 振盪頻率',chinese),.20,1.45,.01]]:
      [['a2','a₂',.4,1,.01],['a3','a₃',.4,1,.01],['a4','a₄',.4,1,.01],['lastInput',t('Input x₄','輸入 x₄',chinese),-2,2,.1]];
    const sliders=parameters.map(([id,label,min,max,step])=>{
      const value=kind==='s4d'?state[id]:id==='lastInput'?state.lastInput:state.transitions[Number(id.at(-1))-2];
      return `<label class="ssm-lab-field"><span>${escapeLabel(label)} <output data-value="${id}">${value.toFixed(2)}</output></span><input type="range" data-param="${id}" min="${min}" max="${max}" step="${step}" value="${value}"/></label>`;
    }).join('');
    host.innerHTML=`<section class="ssm-lab-card" aria-label="${name}"><div class="ssm-lab-intro"><strong>${name}</strong><span>${t('Deterministic illustrative calculation — not trained model output','確定性的人工示意運算，非訓練模型輸出',chinese)}</span></div><div class="ssm-lab-parameters">${sliders}</div><div class="ssm-lab-viewport" tabindex="0" role="region" aria-label="${t('Interactive figure, scroll horizontally on narrow screens','互動圖表；窄螢幕可水平捲動',chinese)}"><div data-role="figure"></div></div><div class="ssm-lab-metrics" data-role="metrics"></div><p class="ssm-lab-equation" data-role="equation"></p><div class="ssm-lab-controls"><button type="button" data-action="prev">${t('Previous','上一步',chinese)}</button><button type="button" data-action="play">${t('Play','播放',chinese)}</button><button type="button" data-action="next">${t('Next','下一步',chinese)}</button><label class="ssm-lab-timeline">${t('Step','步驟',chinese)} <input data-role="seek" type="range" min="0" max="${kind==='s4d'?15:3}" step="1" value="0"/></label><button type="button" data-action="speed">1×</button><button type="button" data-action="reset">${t('Reset','重設',chinese)}</button></div><p class="ssm-lab-status" role="status" aria-live="polite" data-role="status"></p></section>`;
    let timer=null, speed=1;
    const stop=()=>{if(timer!==null){clearInterval(timer);timer=null;}};
    const setStep=val=>{state.step=clamp(Math.round(val),0,kind==='s4d'?15:3);draw();};
    const draw=()=>{
      const result=kind==='s4d'?s4d(state):ssd(state);
      el(host,'[data-role="figure"]').innerHTML=result.visual;
      el(host,'[data-role="metrics"]').innerHTML=result.stats.map(([label,val])=>`<div><span>${label}</span><strong>${val}</strong></div>`).join('');
      el(host,'[data-role="equation"]').textContent=result.equation;
      el(host,'[data-role="seek"]').value=state.step;
      el(host,'[data-action="play"]').textContent=timer===null?t('Play','播放',chinese):t('Pause','暫停',chinese);
      el(host,'[data-role="status"]').textContent=`${t('Step','步驟',chinese)} ${state.step+1}/${result.stepMax+1} · ${result.equation}`;
    };
    const start=()=>{stop();if(state.step===(kind==='s4d'?15:3))state.step=0;timer=setInterval(()=>{if(state.step===(kind==='s4d'?15:3)){stop();draw();return;}setStep(state.step+1);},900/speed);draw();};
    for(const input of host.querySelectorAll('[data-param]'))input.addEventListener('input',()=>{
      const id=input.dataset.param,value=n(input.value,0);
      if(kind==='s4d')state[id]=value;
      else if(id==='lastInput')state.lastInput=value;
      else state.transitions[Number(id.at(-1))-2]=value;
      el(host,`[data-value="${id}"]`).textContent=value.toFixed(2);draw();
    });
    el(host,'[data-role="seek"]').addEventListener('input',e=>{stop();setStep(n(e.target.value,0));});
    host.querySelectorAll('[data-action]').forEach(button=>button.addEventListener('click',()=>{
      const action=button.dataset.action;
      if(action==='play'){if(timer===null)start();else{stop();draw();}}
      else if(action==='next'||action==='prev'){stop();setStep(state.step+(action==='next'?1:-1));}
      else if(action==='speed'){speed=speed===1?2:speed===2?.5:1;button.textContent=speed+'×';if(timer!==null)start();}
      else if(action==='reset'){stop();Object.assign(state,JSON.parse(JSON.stringify(defaults)));speed=1;el(host,'[data-action="speed"]').textContent='1×';host.querySelectorAll('[data-param]').forEach(input=>{const id=input.dataset.param;const value=kind==='s4d'?state[id]:id==='lastInput'?state.lastInput:state.transitions[Number(id.at(-1))-2];input.value=value;el(host,`[data-value="${id}"]`).textContent=value.toFixed(2);});draw();}
    }));
    document.addEventListener('visibilitychange',()=>{if(document.hidden){stop();draw();}});
    // No autoplay. Reduced-motion users can explicitly step or opt into playback.
    draw();
  }
  const boot=()=>document.querySelectorAll('[data-ssm-lab]').forEach(mount);
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',boot);
  else boot();
  if(document.document$?.subscribe)document.document$.subscribe(boot);
})();