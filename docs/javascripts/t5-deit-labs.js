/* Original deterministic teaching labs for T5 and DeiT. No external resources. */
(() => {
  'use strict';
  const messages = {
    en: {
      previous: 'Previous', next: 'Next', play: 'Play', pause: 'Pause', reset: 'Reset', speed: 'Speed', step: 'Step',
      t5title: 'Span corruption lab', deittitle: 'Dual-head distillation lab',
      first: 'First span starts at', second: 'Second span starts at', firstLength: 'First span length', secondLength: 'Second span length',
      stageT5: ['Original tokens', 'Mark the removed spans', 'Construct encoder input', 'Construct decoder target'],
      stagesDeit: ['Student and teacher inputs', 'Two student predictions', 'Separate supervision targets', 'Compute both cross-entropies', 'Average predictions at inference'],
      classProb: 'Class head P(A)', distProb: 'Distillation head P(A)', teacher: 'Teacher hard label',
      t5note: 'Toy 10-token input; the selected removal fraction is illustrative, not the approximately 15% used in T5 pretraining.',
      deitnote: 'Toy binary probabilities and hard labels, not a trained DeiT or a gradient trace. The teacher is fixed and receives no student-loss gradient.',
      noScript: 'Interactive calculation requires JavaScript; the original SVG preview above works without it.'
    },
    zh: {
      previous: '上一步', next: '下一步', play: '播放', pause: '暫停', reset: '重設', speed: '速度', step: '步驟',
      t5title: '跨度破壞互動實驗', deittitle: '雙輸出頭蒸餾互動實驗',
      first: '第一段起始位置', second: '第二段起始位置', firstLength: '第一段長度', secondLength: '第二段長度',
      stageT5: ['原始 Token', '標記移除跨度', '組成編碼器輸入', '組成解碼器目標'],
      stagesDeit: ['學生與教師輸入', '兩個學生預測', '分離的監督目標', '計算兩個交叉熵', '推論時平均輸出機率'],
      classProb: '分類頭 P(A)', distProb: '蒸餾頭 P(A)', teacher: '教師硬標籤',
      t5note: '人工構造的十個 Token 範例；本例移除比例不代表 T5 預訓練常用的約 15%。',
      deitnote: '人工二元機率與硬標籤，並非訓練後的 DeiT 或梯度軌跡；教師固定，不接受學生損失的梯度。',
      noScript: '互動計算需要 JavaScript；上方原始 SVG 預覽不受影響。'
    }
  };
  const esc = s => String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const f = n => Number(n).toFixed(3);
  const rect = (x,y,w,h,fill,stroke='#d7e2eb') => `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="7" fill="${fill}" stroke="${stroke}"/>`;
  const text = (x,y,s,size=15,fill='#28445b',anchor='middle') => `<text x="${x}" y="${y}" font-size="${size}" fill="${fill}" text-anchor="${anchor}" font-family="system-ui,Arial,sans-serif">${esc(s)}</text>`;
  function controls(root, label, min, max, value, step = 1) {
    const id = `${root.id || 'lab'}-${label.replace(/\W/g,'')}`;
    return `<label class="td-field" for="${id}"><span>${esc(label)}</span><input id="${id}" type="range" min="${min}" max="${max}" step="${step}" value="${value}"/><output for="${id}">${value}</output></label>`;
  }
  function tokenLane(items, y, label, active = [], dim = false) {
    const cell = Math.min(57, 665 / Math.max(1, items.length));
    let out = text(64, y+25, label, 15, '#28445b', 'start');
    out += `<g data-lane="${label}">`;
    items.forEach((s,i) => {
      const x = 140+i*cell, marked = active.includes(i);
      out += rect(x,y,cell-6,40,marked?'#ffddbd':dim?'#f0f3f7':'#e3f1f5',marked?'#d97730':'#b9ccd8');
      out += text(x+(cell-6)/2,y+26,s,15,marked?'#8a441e':'#173e56');
    });
    return out+'</g>';
  }
  function t5Draw(s) {
    const tokens = 'ABCDEFGHIJ'.split('');
    const remove = new Set([...Array(s.len1).keys()].map(i=>s.start1+i).concat([...Array(s.len2).keys()].map(i=>s.start2+i)));
    const enc=[],target=['S0'];let idx=0;
    while(idx<tokens.length) {
      if(idx===s.start1) { enc.push('S0');for(let j=0;j<s.len1;j++) target.push(tokens[idx+j]);idx+=s.len1; }
      else if(idx===s.start2) { enc.push('S1');target.push('S1');for(let j=0;j<s.len2;j++)target.push(tokens[idx+j]);idx+=s.len2; }
      else {enc.push(tokens[idx]);idx++;}
    }
    target.push('S2');
    s.encoder=enc;s.target=target;s.masked=remove.size;
    const svg=`<svg viewBox="0 0 760 280" width="760" height="280" role="img" aria-label="${s.zh?'T5 跨度破壞與哨兵 Token 轉換':'T5 span corruption and sentinel transformation'}"><rect width="760" height="280" rx="15" fill="#f8fbfe"/>${tokenLane(tokens,45,'Input',s.stage>=1?[...remove]:[])}${s.stage>=2?tokenLane(enc,115,'Encoder'):text(370,141,'···',20,'#a7bbc7')}${s.stage>=3?tokenLane(target,190,'Target'):text(370,215,'···',20,'#a7bbc7')}${text(740,266,`${remove.size}/10`,13,'#647d91','end')}</svg>`;
    return svg;
  }
  function deitDraw(s) {
    const p=s.p, d=s.d, teacher=s.teacher, ce1=-Math.log(p), ce2=-Math.log(teacher==='A'?d:1-d),total=(ce1+ce2)/2, avg=(p+d)/2;
    s.ce1=ce1;s.ce2=ce2;s.loss=total;s.avg=avg;
    let svg=`<svg viewBox="0 0 760 300" width="760" height="300" role="img" aria-label="${s.zh?'DeiT 分類與蒸餾雙頭、硬標籤與交叉熵':'DeiT class and distillation heads with cross entropy'}"><rect width="760" height="300" rx="15" fill="#f8fbfe"/>`;
    svg+=rect(22,47,145,74,'#e4f1f7')+text(94,79,'Student',17)+text(94,103,'ViT',14);
    svg+=rect(22,169,145,57,'#fff1e1')+text(94,193,'Teacher',16)+text(94,213,teacher,15);
    svg+=`<path d="M168 85H217 M168 196H217" stroke="#7d9bb0" stroke-width="2" stroke-dasharray="5 4"/>`;
    const rows=[{name:'CLS',prob:p,y:55,color:'#169bab',target:'A',ce:ce1},{name:'DIST',prob:d,y:151,color:'#df8a34',target:teacher,ce:ce2}];
    rows.forEach((r,i)=>{
      svg+=rect(222,r.y,498,82,'#fff');svg+=text(256,r.y+28,r.name,15,'#294a5d','start');
      svg+=rect(315,r.y+17,238,18,'#e9eef3');svg+=rect(315,r.y+17,238*r.prob,18,r.color,r.color);
      svg+=text(567,r.y+32,`P(A) ${f(r.prob)}`,13,'#31566b','start');
      if(s.stage>=2)svg+=text(311,r.y+65,`Target ${r.target}`,14,r.color,'start');
      if(s.stage>=3)svg+=text(496,r.y+65,`CE ${f(r.ce)}`,14,'#2a5169','start');
    });
    if(s.stage>=4)svg+=rect(236,247,475,40,'#d9f3e8')+text(475,273,`P(A) ${(100*avg).toFixed(1)}%  ·  Avg heads`,15,'#206d59');
    else if(s.stage>=3)svg+=text(477,273,`L = ${f(total)}`,17,'#28445b');
    svg+='</svg>';return svg;
  }
  function init(root) {
    if(root.dataset.ready==='yes')return;
    root.dataset.ready='yes';
    const isT5=root.dataset.lab==='t5', zh=/zh/i.test(document.documentElement.lang||'')||root.dataset.lang==='zh', m=messages[zh?'zh':'en'];
    const s=isT5?{stage:0,start1:1,len1:2,start2:7,len2:2,zh}:{stage:0,p:0.75,d:0.6,teacher:'B',zh};
    const last=isT5?3:4;
    root.innerHTML=`<div class="td-head"><strong>${esc(isT5?m.t5title:m.deittitle)}</strong></div><div class="td-params">${isT5 ? controls(root,m.first,1,4,2)+controls(root,m.firstLength,1,3,2)+controls(root,m.second,7,9,8)+controls(root,m.secondLength,1,2,2) : controls(root,m.classProb,.05,.95,.75,.05)+controls(root,m.distProb,.05,.95,.6,.05)+`<label class="td-field"><span>${m.teacher}</span><select><option value="A">A</option><option value="B" selected>B</option></select></label>`}</div><div class="td-viewport" role="region" tabindex="0" aria-label="${zh?(isT5?'跨度破壞互動圖，可水平捲動':'蒸餾雙頭互動圖，可水平捲動'):(isT5?'Span corruption diagram, scroll horizontally if needed':'Distillation diagram, scroll horizontally if needed')}"><div class="td-art"></div></div><div class="td-state" aria-live="polite"></div><div class="td-transport"><button data-action="prev" type="button">${m.previous}</button><button data-action="next" type="button">${m.next}</button><button data-action="play" type="button">${m.play}</button><label>${m.step} <input class="td-seek" aria-label="${m.step}" type="range" min="0" max="${last}" step="1" value="0"/></label><label>${m.speed} <select class="td-speed"><option value="2">0.5×</option><option value="1" selected>1×</option><option value="0.5">2×</option></select></label><button data-action="reset" type="button">${m.reset}</button></div><p class="td-note">${isT5?m.t5note:m.deitnote}</p>`;
    const ranges=[...root.querySelectorAll('.td-params input')], out=root.querySelector('.td-state'), seek=root.querySelector('.td-seek');
    let timer=null;
    const stop=()=>{if(timer!==null){clearInterval(timer);timer=null;}root.querySelector('[data-action="play"]').textContent=m.play;};
    const render=()=>{
      root.querySelector('.td-art').innerHTML=isT5?t5Draw(s):deitDraw(s);
      seek.value=s.stage;
      const phase=(isT5?m.stageT5:m.stagesDeit)[s.stage];
      out.textContent=isT5?`${phase} · ${s.masked}/10 (${s.masked*10}%) · Encoder: ${s.encoder.join(' ')} · Target: ${s.target.join(' ')}`:`${phase} · CE(CLS) ${f(s.ce1)} · CE(DIST) ${f(s.ce2)} · L ${f(s.loss)} · P(A) ${f(s.avg)}`;
    };
    if(isT5){ranges.forEach((r,i)=>r.addEventListener('input',()=>{s[['start1','len1','start2','len2'][i]]=Number(r.value)-(i%2===0?1:0); /* position labels 1-based */
      // First span must end before second; positions are zero-based internally.
      s.start1=Math.min(s.start1,3);s.start2=Math.max(6,s.start2);
      r.nextElementSibling.textContent=r.value;stop();render();}));
      s.start1=1;s.start2=7; // Initial positions correspond to the original B-C and H-I example.
    }else{
      ranges.forEach((r,i)=>r.addEventListener('input',()=>{s[i?'d':'p']=Number(r.value);r.nextElementSibling.textContent=r.value;stop();render();}));
      root.querySelector('.td-params select').addEventListener('change',e=>{s.teacher=e.target.value;stop();render();});
    }
    const start=()=>{
      if(timer!==null)clearInterval(timer);
      timer=setInterval(()=>{s.stage=(s.stage+1)%(last+1);render();},700*Number(root.querySelector('.td-speed').value));
      root.querySelector('[data-action="play"]').textContent=m.pause;
    };
    root.querySelector('.td-speed').addEventListener('change',()=>{if(timer!==null)start();});
    root.querySelectorAll('[data-action]').forEach(b=>b.addEventListener('click',()=>{
      const act=b.dataset.action;
      if(act==='play'){if(timer!==null){stop();return;}if(s.stage===last)s.stage=0;
        start();
      }else{stop();if(act==='prev')s.stage=Math.max(0,s.stage-1);if(act==='next')s.stage=Math.min(last,s.stage+1);
        if(act==='reset'){s.stage=0;if(isT5){Object.assign(s,{start1:1,len1:2,start2:7,len2:2});[2,2,8,2].forEach((v,i)=>{ranges[i].value=v;ranges[i].nextElementSibling.textContent=v;});}
          else{Object.assign(s,{p:.75,d:.6,teacher:'B'});ranges[0].value=.75;ranges[1].value=.6;ranges.forEach(r=>r.nextElementSibling.textContent=r.value);root.querySelector('.td-params select').value='B';}}
        render();}
    }));
    seek.addEventListener('input',()=>{stop();s.stage=Number(seek.value);render();});
    document.addEventListener('visibilitychange',()=>{if(document.hidden)stop();});
    render();
  }
  function scan(){document.querySelectorAll('.t5-deit-lab[data-lab]').forEach(init);}
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',scan);else scan();
  if(window.document$?.subscribe)window.document$.subscribe(scan);
})();
