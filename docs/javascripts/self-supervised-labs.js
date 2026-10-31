// Interactive deterministic MoCo / BYOL teaching labs, original CC BY-SA 4.0.
// The scalar parameters and six-slot queue are schematic, not training results.
(() => {
  'use strict';
  const online = [0.70, 0.85, 0.78, 0.91];
  const targets = momentum => {
    const values = [0.30];
    for (let i=1;i<online.length;i++) values.push(momentum*values[i-1]+(1-momentum)*online[i]);
    return values;
  };
  const stages = {
    moco: ['Encode key','Contrast','Query SGD','Key EMA','FIFO enqueue'],
    byol: ['Two views','Predict','Stop-gradient','Online SGD','Target EMA']
  };
  const explanations = {
    moco: {
      en: ['Encode the positive key with the pre-update key encoder; negatives are in the old queue.','Compare the query with its positive key and queued negatives before enqueueing.','Gradient descent updates only the query encoder.','Update the key encoder by EMA of the updated query parameters.','Enqueue the new key and evict the oldest negative after the loss.'],
      zh: ['用更新前的鍵編碼器建立正樣本鍵；負樣本來自原本的佇列。','查詢與正樣本及舊佇列負樣本比較，尚未將新鍵入列。','只有查詢編碼器透過梯度下降更新。','使用更新後的查詢參數，以 EMA 更新鍵編碼器。','完成損失計算後才加入新鍵，並淘汰最舊的負樣本。']
    },
    byol: {
      en: ['Process two augmentations with separate online and target branches.','The online predictor matches the target representation.','Stop-gradient blocks gradients into the target; there is no negative-key queue.','Only the online network and predictor receive loss gradients.','EMA follows the updated online parameters, without target backpropagation.'],
      zh: ['兩種影像增強視角分別送入線上與目標分支。','線上預測器嘗試對齊目標網路的表徵。','停止梯度阻止損失梯度回傳至目標網路；沒有負樣本佇列。','只有線上網路與預測器接收損失梯度。','以更新後的線上參數執行 EMA，而非對目標網路反向傳播。']
    }
  };

  // An independent toy loss inspector: fixed similarities are NOT inferred from
  // the schematic scalar EMA weights or FIFO letters. No gradients are simulated.
  const toyNegatives = [-0.20, -0.10, 0.00, 0.10, 0.20, 0.05];
  function lossSnapshot(kind, value) {
    if (kind === 'moco') {
      const tau = Math.min(1, Math.max(0.1, value));
      const logits = [0.70, ...toyNegatives].map(v => v / tau);
      const offset = Math.max(...logits);
      const exponentials = logits.map(v => Math.exp(v - offset));
      const denominator = exponentials.reduce((a, b) => a + b, 0);
      const positive = exponentials[0] / denominator;
      return {tau, positive, loss: -Math.log(positive)};
    }
    const cosine = Math.min(1, Math.max(-1, value));
    return {cosine, loss: 2 - 2 * cosine};
  }
  function lossGraphic(kind, result, zh) {
    if (kind === 'moco') {
      const pct = (100 * result.positive).toFixed(1);
      return '<div class="ssl-loss-bars" role="img" aria-label="' +
        (zh ? '正樣本機率 ' + pct + '%，其餘為負樣本' : 'Positive-key probability ' + pct + '%, remainder is negatives') + '">' +
        '<span class="ssl-loss-positive" style="width:' + pct + '%"></span>' +
        '<span class="ssl-loss-negative" style="width:' + (100 - result.positive * 100).toFixed(1) + '%"></span></div>';
    }
    const angle = Math.acos(result.cosine);
    const x = (110 + 70 * Math.cos(angle)).toFixed(2);
    const y = (120 - 70 * Math.sin(angle)).toFixed(2);
    return '<svg class="ssl-loss-vectors" viewBox="0 0 250 140" role="img" aria-label="' +
      (zh ? '兩個單位向量夾角的示意圖' : 'Angle between two unit vectors') + '">' +
      '<path d="M110 120 H180" stroke="#399a80" stroke-width="4" stroke-linecap="round"/>' +
      '<path d="M110 120 L' + x + ' ' + y + '" stroke="#3a7fa9" stroke-width="4" stroke-linecap="round"/>' +
      '<circle cx="110" cy="120" r="4" fill="#20384b"/>' +
      '<path d="M8 15 H25" stroke="#3a7fa9" stroke-width="3"/>' +
      '<text x="31" y="19" class="ssl-vector-label">Online</text>' +
      '<path d="M120 15 H137" stroke="#399a80" stroke-width="3"/>' +
      '<text x="143" y="19" class="ssl-vector-label">Target</text></svg>';
  }
  const fmt = x => (Math.round((x + Number.EPSILON)*1000)/1000).toFixed(3);
  function calculate(kind, index, momentum) {
    const target=targets(momentum);
    const turn=Math.floor(index/5), phase=index%5;
    const onlineAt=turn+(phase >= (kind==='moco'?2:3)?1:0);
    const targetAt=turn+(phase >= (kind==='moco'?3:4)?1:0);
    const removed=turn+(kind==='moco'&&phase===4?1:0);
    return {turn,phase,q:online[onlineAt],k:target[targetAt],
      target, queue:['A','B','C','D','E','F','G','H','I'].slice(removed,removed+6)};
  }
  function diagram(kind,s,momentum) {
    const m=kind==='moco', qx=112+s.q*380, kx=112+s.k*380;
    const emphasis=['#196b96','#087f83','#c06647','#8c62a7','#15856d'][s.phase];
    const paths=m?[[130,100,470,100],[305,105,305,156],[460,166,460,110],[330,160,330,115],[488,180,575,180]]
                 :[[135,100,480,100],[450,100,305,165],[350,170,350,170],[460,155,460,95],[190,220,455,220]];
    const a=paths[s.phase];
    let queue='';
    if(m){
      queue='<text x="22" y="188" class="ssl-small">FIFO negatives · oldest → newest</text>';
      s.queue.forEach((item,i)=>{
        queue+='<rect x="'+(22+98*i)+'" y="193" width="82" height="37" rx="7" fill="'+(i===5&&s.phase===4?'#c6eee0':'#e9eff4')+'" stroke="#9eb3c0"/>';
        queue+='<text x="'+(63+98*i)+'" y="218" class="ssl-token">'+item+'</text>';
      });
    } else {
      queue='<text x="22" y="194" class="ssl-small">No negatives · target gradient = 0</text><path d="M350 183 H405" stroke="#b55d65" stroke-width="3" stroke-dasharray="6 5"/><text x="414" y="187" class="ssl-small">Stop-grad</text>';
    }
    return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 260" role="img" aria-label="'+(m?'MoCo: query, momentum key, FIFO negatives':'BYOL: online, stop-gradient, EMA target')+'">'+
      '<rect x="1" y="1" width="638" height="258" rx="12" fill="#f8fbfd" stroke="#b9cbd6"/>'+
      '<text x="22" y="28" class="ssl-title">'+(m?'MoCo · Queue + Momentum':'BYOL · Online + Target')+'</text>'+
      '<path d="M24 44 H616" stroke="#cad9e2"/>'+
      '<text x="24" y="75" class="ssl-small">'+(m?'Query encoder (SGD)':'Online encoder + predictor')+'</text>'+
      '<text x="24" y="133" class="ssl-small">'+(m?'Key encoder (EMA)':'Target encoder (EMA)')+'</text>'+
      '<rect x="111" y="83" width="385" height="15" rx="7" fill="#dfecf3"/>'+
      '<rect x="111" y="141" width="385" height="15" rx="7" fill="#e4f3eb"/>'+
      '<rect x="111" y="83" width="'+(qx-111)+'" height="15" rx="7" fill="#3a7fa9"/>'+
      '<rect x="111" y="141" width="'+(kx-111)+'" height="15" rx="7" fill="#399a80"/>'+
      '<circle cx="'+qx+'" cy="90" r="10" fill="#1e5d86" stroke="white" stroke-width="2"/>'+
      '<circle cx="'+kx+'" cy="148" r="10" fill="#187d6a" stroke="white" stroke-width="2"/>'+
      '<text x="530" y="94" class="ssl-number">'+fmt(s.q)+'</text>'+
      '<text x="530" y="152" class="ssl-number">'+fmt(s.k)+'</text>'+
      '<path d="M607 65 V158" stroke="'+emphasis+'" stroke-width="4" stroke-linecap="round"/>'+
      queue+
      '<circle class="ssl-packet" cx="'+a[0]+'" cy="'+a[1]+'" data-x0="'+a[0]+'" data-y0="'+a[1]+'" data-x1="'+a[2]+'" data-y1="'+a[3]+'" r="7" fill="'+emphasis+'" aria-hidden="true"/>'+
      '<text x="22" y="247" class="ssl-small">Toy weights · m = '+momentum.toFixed(2)+' · Not measurements</text></svg>';
  }
  function enhance() {
    document.querySelectorAll('[data-self-supervised-lab]').forEach(host=>{
      if(host.dataset.labReady) return;
      const kind=host.dataset.selfSupervisedLab;
      if(!stages[kind]) return;
      host.dataset.labReady='yes';
      const zh=host.dataset.locale==='zh-TW';
      const lossTitle=kind==='moco'?(zh?'溫度 τ':'Temperature τ'):(zh?'餘弦相似度':'Cosine similarity');
      const lossDefault=kind==='moco'?'0.20':'0.50';
      const lossMin=kind==='moco'?'0.10':'-1.00';
      const words=zh?['播放','暫停','上一步','下一步','進度','速度','動量 m']:['Play','Pause','Previous','Next','Timeline','Speed','Momentum m'];
      host.classList.add('ssl-lab');
      host.innerHTML='<div class="ssl-figure"></div><div class="ssl-toolbar">'+
        '<button type="button" data-act="play"></button><button type="button" data-act="prev"></button><button type="button" data-act="next"></button>'+
        '<label>'+words[4]+' <input type="range" min="0" max="14" step="1" value="0" aria-label="'+words[4]+'" data-act="seek"></label>'+
        '<label>'+words[5]+' <select aria-label="'+words[5]+'" data-act="speed"><option value=".5">0.5×</option><option value="1" selected>1×</option><option value="2">2×</option></select></label>'+
        '<label class="ssl-momentum">'+words[6]+' <input type="range" min="0.50" max="0.99" step="0.01" value="0.90" aria-label="'+words[6]+'" data-act="momentum"><output data-momentum-output>0.90</output></label></div>'+
        '<div class="ssl-explain" aria-live="polite" aria-atomic="true"></div><div class="ssl-compute" aria-live="off"></div>'+
        '<div class="ssl-loss"><label>'+lossTitle+' <input type="range" data-act="loss" min="'+lossMin+'" max="1.00" step="0.05" value="'+lossDefault+'" aria-label="'+lossTitle+'"></label><output class="ssl-loss-value"></output><div class="ssl-loss-visual"></div><p class="ssl-loss-note"></p></div>';
      const find = name => host.querySelector('[data-act="'+name+'"]');
      const figure=host.querySelector('.ssl-figure'),note=host.querySelector('.ssl-explain'),calc=host.querySelector('.ssl-compute');
      const play=find('play'),prev=find('prev'),next=find('next'),seek=find('seek'),speed=find('speed');
      const momentumInput=find('momentum'), momentumOutput=host.querySelector('[data-momentum-output]');
      const lossInput=find('loss'),lossValue=host.querySelector('.ssl-loss-value');
      const lossVisual=host.querySelector('.ssl-loss-visual'),lossNote=host.querySelector('.ssl-loss-note');
      const renderLoss=()=>{
        const value=Number(lossInput.value),result=lossSnapshot(kind,value);
        lossInput.setAttribute('aria-valuetext',value.toFixed(2));
        lossValue.textContent=kind==='moco'
          ? 'P(+) = '+result.positive.toFixed(3)+' · InfoNCE = '+result.loss.toFixed(3)
          : 'cos = '+result.cosine.toFixed(2)+' · L = 2 − 2cos = '+result.loss.toFixed(3);
        lossVisual.innerHTML=lossGraphic(kind,result,zh);
        lossNote.textContent=kind==='moco'
          ? (zh?'固定示意相似度：正樣本 0.70，六個負樣本介於 −0.20 至 0.20。調整 τ 觀察 Softmax 與 InfoNCE；與上方 EMA 權重無關。':'Fixed toy similarities: positive 0.70 and six negatives from −0.20 to 0.20. Vary τ to inspect softmax and InfoNCE; independent of EMA weights above.')
          : (zh?'兩個單位向量的平方距離；調整 cos 觀察損失。這不是上方 EMA 權重的相似度，也不是實測表徵。':'Squared distance between unit vectors. Vary cos to inspect the loss; this is not the cosine of the EMA weights above or a measured representation.');
      };
      lossInput.addEventListener('input',renderLoss);
      // The particle follows the current operation ONCE. Its position is a pure
      // function of elapsed time, so Pause freezes it and seek/step is deterministic.
      const STEP_MS=1250;
      let frame=0,running=false,raf=0,last=null,elapsed=0;
      const movePacket=()=>{
        const packet=figure.querySelector?.('.ssl-packet');
        if(!packet) return; // The lightweight Node DOM mock has no SVG tree.
        const t=Math.min(1,Math.max(0,elapsed/STEP_MS));
        const ease=t*t*(3-2*t);
        for(const axis of ['x','y']){
          const from=Number(packet.getAttribute('data-'+axis+'0'));
          const to=Number(packet.getAttribute('data-'+axis+'1'));
          packet.setAttribute(axis==='x'?'cx':'cy',String(from+(to-from)*ease));
        }
      };
      const updatePlay=()=>{play.textContent=(running?'Ⅱ '+words[1]:'▶ '+words[0]);};
      const stop=()=>{
        running=false;last=null;cancelAnimationFrame(raf);raf=0;updatePlay();
      };
      const render=()=>{
        const momentum=Number(momentumInput.value);
        const s=calculate(kind,frame,momentum);
        momentumOutput.textContent=momentum.toFixed(2);
        momentumInput.setAttribute('aria-valuetext',momentum.toFixed(2));
        figure.innerHTML=diagram(kind,s,momentum);
        const label=zh ? (kind==='moco'?['產生鍵','對比','查詢 SGD','動量 EMA','佇列入列']:['增強視角','預測','停止梯度','線上 SGD','目標 EMA'])[s.phase] : stages[kind][s.phase];
        note.textContent=(zh?'回合 ':'Iteration ')+(s.turn+1)+'/3 · '+label+' — '+explanations[kind][zh?'zh':'en'][s.phase];
        // The numerical trace must not reveal future SGD/EMA results before
        // their operations. Other charts already obey this causal boundary.
        const emaComplete=s.phase >= (kind==='moco'?3:4);
        const emaReadout=emaComplete
          ? (zh?'已執行 EMA':'EMA applied')+': '+momentum.toFixed(2)+'×'+fmt(s.target[s.turn])+' + '+(1-momentum).toFixed(2)+'×'+fmt(online[s.turn+1])+' = '+fmt(s.k)
          : (zh?'待執行 EMA（未來結果隱藏）':'EMA pending (future result hidden)');
        calc.textContent=(zh?'線上／查詢參數':'Online / query weight')+' = '+fmt(s.q)+' · '+(zh?'目標／鍵參數':'Target / key weight')+' = '+fmt(s.k)+
          ' · '+emaReadout+
          ' · |Δ|='+fmt(Math.abs(s.q-s.k))+
          (kind==='moco'?' · FIFO ['+s.queue.join(' ')+']':(zh?' · 目標梯度 = 0':' · Target gradient = 0'));
        movePacket();updatePlay();
        prev.textContent='← '+words[2];next.textContent=words[3]+' →';
        prev.disabled=frame===0;next.disabled=frame===14;seek.value=String(frame);
        seek.setAttribute('aria-valuetext',(frame+1)+'/15');
      };
      const show=n=>{frame=Math.max(0,Math.min(14,n));elapsed=0;render();};
      const tick=now=>{
        if(!running)return;
        if(last!==null)elapsed+=Math.min(250,Math.max(0,now-last))*Number(speed.value);
        last=now;
        if(elapsed>=STEP_MS){
          if(frame===14){elapsed=STEP_MS;movePacket();stop();return;}
          elapsed-=STEP_MS;frame++;render();
        }else movePacket();
        raf=requestAnimationFrame(tick);
      };
      const start=()=>{
        if(frame===14){frame=0;elapsed=0;render();}
        running=true;last=null;updatePlay();raf=requestAnimationFrame(tick);
      };
      play.addEventListener('click',()=>{if(running)stop();else start();});
      prev.addEventListener('click',()=>{stop();show(frame-1);});
      next.addEventListener('click',()=>{stop();show(frame+1);});
      seek.addEventListener('input',()=>{stop();show(Number(seek.value));});
      // Speed applies to the current interpolation without resetting its state.
      speed.addEventListener('change',()=>{});
      // The what-if slider recomputes all three EMA steps, without changing SGD or FIFO.
      momentumInput.addEventListener('input',()=>{stop();render();});
      document.addEventListener?.('visibilitychange',()=>{if(document.hidden&&running)stop();});
      render();renderLoss();
    });
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',enhance);
  else enhance();
  if(window.document$ && typeof window.document$.subscribe==='function')window.document$.subscribe(enhance);
})();
