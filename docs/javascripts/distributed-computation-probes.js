/* Bilingual, dependency-free FSDP and Megatron computation probes; still SVG fallback in Markdown. */
(() => {
  'use strict';
  const mq = matchMedia('(prefers-reduced-motion: reduce)');
  const en = {ranks:'Ranks',size:'Unit MiB',policy:'Reshard after forward',tokens:'Tokens',play:'Play',pause:'Pause',prev:'Previous step',next:'Next step',seek:'Timeline',speed:'Speed',step:'Step',local:'Local shard',remote:'Gathered remote',resident:'Resident parameters',gathers:'All-gathers',width:'Local features',payload:'All-reduce tensor',traffic:'Ring sent/rank',transfer:'All-gather received/rank',round:'Ring round',noteF:'Single FSDP unit; parameters only, excluding gradients, activations, optimizer states and transient buffers. Illustrative MiB, not measured GPU memory.',noteM:'Toy MLP: H=8, expansion=32, 2 bytes/element. Ring estimate 2(N−1)/N × payload per rank; not measured traffic or latency. Forward pass only.'};
  const zh = {ranks:'裝置數',size:'分片單元 MiB',policy:'前向後重新分片',tokens:'Token 數',play:'播放',pause:'暫停',prev:'上一步',next:'下一步',seek:'時間軸',speed:'速度',step:'步驟',local:'本地分片',remote:'暫存遠端分片',resident:'參數駐留量',gathers:'All-gather 次數',width:'本地特徵寬度',payload:'All-reduce 張量',traffic:'每裝置 Ring 已傳送量',transfer:'每裝置 All-gather 接收量',round:'Ring 回合',noteF:'單一 FSDP 單元，只計參數，不含梯度、激活值、最佳化器狀態與暫存緩衝區；MiB 為示意，非實測。',noteM:'示意 MLP：H=8、擴張維度=32、每元素 2 B。Ring 估算為每裝置 2(N−1)/N × 張量大小，非實測流量或延遲；只含前向傳播。'};
  const node=(tag,cls='',value)=>{const e=document.createElement(tag);e.className=cls;if(value!==undefined)e.textContent=value;return e;};
  function range(label,min,max,val,step,fn){const wrap=node('label','dcp-field'),head=node('span','dcp-head',label),out=node('output','',String(val)),input=node('input');input.type='range';Object.assign(input,{min:String(min),max:String(max),step:String(step),value:String(val)});input.setAttribute('aria-label',label);input.addEventListener('input',()=>{out.textContent=input.value;fn(+input.value);});head.append(out);wrap.append(head,input);return {wrap,out};}
  function setup(host,L,total,draw){let step=0,timer=0;const panel=node('div','dcp-panel'),fields=node('div','dcp-fields'),plot=node('div','dcp-plot'),stats=node('div','dcp-stats'),bar=node('div','dcp-controls');
    const button=(label,glyph,fn)=>{const b=node('button','dcp-button',glyph);b.type='button';b.setAttribute('aria-label',label);b.addEventListener('click',fn);return b;};
    const stop=()=>{clearInterval(timer);timer=0;sync();};
    const set=n=>{step=Math.max(0,Math.min(total,n));draw(step,plot,stats);sync();};
    const prev=button(L.prev,'←',()=>{stop();set(step-1);}),play=button(L.play,'▶',()=>{if(mq.matches)return;if(timer){stop();return;}if(step===total)set(0);timer=setInterval(()=>{if(step===total){stop();return;}set(step+1);},900/(+speed.value));sync();}),next=button(L.next,'→',()=>{stop();set(step+1);});
    const seek=node('input','dcp-seek');Object.assign(seek,{type:'range',min:'0',max:String(total),step:'1',value:'0'});seek.setAttribute('aria-label',L.seek);seek.addEventListener('input',()=>{const n=+seek.value;stop();set(n);});
    const status=node('output','dcp-status'),speed=node('select','dcp-speed');speed.setAttribute('aria-label',L.speed);for(const n of [.5,1,2]){const o=node('option','',n+'×');o.value=String(n);if(n===1)o.selected=true;speed.append(o);}speed.addEventListener('change',()=>{if(timer){stop();play.click();}});
    function sync(){play.textContent=timer?'Ⅱ':'▶';play.setAttribute('aria-label',timer?L.pause:L.play);play.disabled=mq.matches;prev.disabled=step===0;next.disabled=step===total;seek.value=String(step);status.textContent=L.step+' '+(step+1)+'/'+(total+1);}
    bar.append(prev,play,next,seek,status,speed);panel.append(fields,plot,stats,bar);host.append(panel);mq.addEventListener('change',stop);document.addEventListener('visibilitychange',()=>{if(document.hidden)stop();});
    return {fields,plot,stats,panel,set,stop};
  }
  function fsdp(host,L){let n=4,size=256,reshard=true;const app=setup(host,L,6,(s,plot,stats)=>{
      const full=s===1||s===2||s===4||s===5||(s===3&&!reshard),value=full?size:size/n;
      const phases=['Shard','All-gather','Forward',reshard?'Reshard':'Retain',reshard?'All-gather':'Reuse','Backward','Reduce-scatter'];
      plot.replaceChildren(node('div','dcp-phase',phases[s]));
      for(const [title,amount] of [['Replicated',size],['FSDP',value]]){const row=node('div','dcp-row'),head=node('div','dcp-head',title),out=node('strong','',amount.toFixed(1)+' MiB'),track=node('div','dcp-track'),local=node('span','dcp-local');head.append(out);local.style.width=(title==='Replicated'?100:100/n)+'%';track.append(local);if(title==='FSDP'&&full){const remote=node('span','dcp-remote');remote.style.width=(100-100/n)+'%';track.append(remote);}row.append(head,track);plot.append(row);}
      const chart=node('div','dcp-chart');for(const [name,policy] of [['Reshard',true],['Retain',false]]){const row=node('div','dcp-chart-row');row.append(node('span','',name));for(let i=0;i<7;i++){const cell=node('span','dcp-mini'+(i===s?' dcp-now':'')+(i>s?' dcp-future':'')),fill=node('i','');fill.style.height=((i===0||i===6||(i===3&&policy)?1/n:1)*100)+'%';cell.append(fill);row.append(cell);}chart.append(row);}plot.append(chart);
      // Each all-gather receives (N-1)/N of this unit per rank.
      // Contrast both policies at the *current* phase, not future totals.
      const bytes=size*(n-1)/n, reshardCount=s===0?0:s<4?1:2, retainCount=s===0?0:1;
      const transfer=node('div','dcp-transfer');
      transfer.append(node('div','dcp-transfer-title','All-gather / rank'));
      for(const [name,count] of [['Reshard',reshardCount],['Retain',retainCount]]){
        const row=node('div','dcp-transfer-row'),track=node('div','dcp-transfer-track'),fill=node('span','dcp-transfer-fill');
        fill.style.width=(50*count)+'%';track.append(fill);
        row.append(node('span','',name),track,node('strong','',(bytes*count).toFixed(1)+' MiB'));transfer.append(row);
      }
      plot.append(transfer);
      stats.replaceChildren(node('span','',L.resident+': '+value.toFixed(1)+' MiB'),node('span','',L.gathers+': '+(reshard?reshardCount:retainCount)),node('span','',L.transfer+': '+(bytes*(reshard?reshardCount:retainCount)).toFixed(1)+' MiB'));
    });
    const ranks=range(L.ranks,2,8,n,1,v=>{n=v;app.set(+app.panel.querySelector('.dcp-seek').value);}),unit=range(L.size,64,512,size,64,v=>{size=v;app.set(+app.panel.querySelector('.dcp-seek').value);});app.fields.append(ranks.wrap,unit.wrap);
    const policy=node('label','dcp-policy'),check=node('input');check.type='checkbox';check.checked=true;check.setAttribute('aria-label',L.policy);policy.append(check,node('span','',L.policy));check.addEventListener('change',()=>{reshard=check.checked;app.set(+app.panel.querySelector('.dcp-seek').value);});app.fields.after(policy);app.panel.append(node('p','dcp-note',L.noteF));app.set(0);
  }
  // Deterministic ring reduce-scatter followed by ring all-gather.
  // Sets track which ranks' contributions have been accumulated for each chunk.
  function ringState(n,round){
    let hold=Array.from({length:n},(_,r)=>Array.from({length:n},()=>new Set([r])));
    for(let step=0;step<Math.min(round,n-1);step++){
      const old=hold.map(row=>row.map(cell=>new Set(cell)));
      for(let r=0;r<n;r++){const c=(r-step+n)%n,dest=(r+1)%n;hold[dest][c]=new Set([...old[dest][c],...old[r][c]]);}
    }
    if(round>n-1){
      hold=Array.from({length:n},(_,r)=>Array.from({length:n},(_,c)=>c===(r+1)%n?new Set(Array.from({length:n},(_,i)=>i)):new Set()));
      for(let step=0;step<round-(n-1);step++){
        const old=hold.map(row=>row.map(cell=>new Set(cell)));
        for(let r=0;r<n;r++){const c=(r+1-step+n)%n;hold[(r+1)%n][c]=new Set(old[r][c]);}
      }
    }
    return hold.map(row=>row.map(cell=>cell.size));
  }
  function megatron(host,L){let n=2,tokens=2,ringRound=0;const app=setup(host,L,5,(s,plot,stats)=>{
      const width=32/n,payload=tokens*8*2,traffic=2*(n-1)/n*payload,phases=['X','Column','GeLU','Row','All-reduce','Y'];
      plot.replaceChildren(node('div','dcp-phase',phases[s]));const scroll=node('div','dcp-scroll'),grid=node('div','dcp-grid');grid.style.gridTemplateColumns='repeat('+n+',minmax(92px,1fr))';grid.style.minWidth=Math.max(600,n*104)+'px';grid.append(node('div','dcp-input','X · '+tokens+' × 8'));
      for(let i=0;i<n;i++){const lane=node('div','dcp-lane');lane.append(node('strong','', 'GPU '+i));for(const [name,count,cls,when] of [['W1',width,'dcp-col',1],['GeLU',width,'dcp-gelu',2],['W2',8,'dcp-part',3]]){const group=node('div','dcp-group');group.append(node('small','',name));const blocks=node('div','dcp-blocks');if(s>=when)for(let j=0;j<count;j++)blocks.append(node('i',cls));group.append(blocks);lane.append(group);}lane.append(node('div',s===5?'dcp-output':'dcp-empty',s===5?'Y · '+tokens+' × 8':''));grid.append(lane);}
      grid.append(node('div',s>=4?'dcp-collective dcp-visible':'dcp-collective',s>=4?'Σ  All-reduce':''));scroll.append(grid);plot.append(scroll);
      const total=2*(n-1),round=s<4?0:s===5?total:Math.min(ringRound,total);
      if(s>=4){
        const state=ringState(n,round),ring=node('div','dcp-ring'),phase=round<=n-1?'Reduce-scatter':'All-gather';
        const sub=round<=n-1?round:round-(n-1);
        ring.append(node('div','dcp-ring-title','Ring · '+phase+' '+sub+'/'+(n-1)));
        const scroller=node('div','dcp-scroll'),matrix=node('div','dcp-ring-grid');
        matrix.style.gridTemplateColumns='56px repeat('+n+',42px)';
        matrix.append(node('span','dcp-ring-head',''));
        for(let c=0;c<n;c++)matrix.append(node('span','dcp-ring-head','C'+c));
        for(let r=0;r<n;r++){
          matrix.append(node('span','dcp-ring-head','GPU '+r));
          for(let c=0;c<n;c++){
            const count=state[r][c],cls=count===n?'dcp-ring-complete':count?'dcp-ring-partial':'dcp-ring-empty';
            matrix.append(node('span','dcp-ring-cell '+cls,count?count+'/'+n:'·'));
          }
        }
        scroller.append(matrix);ring.append(scroller);
        if(s===4){
          const slider=node('input','dcp-ring-seek');
          Object.assign(slider,{type:'range',min:'0',max:String(total),step:'1',value:String(round)});
          slider.setAttribute('aria-label',L.round);
          slider.addEventListener('input',()=>{ringRound=+slider.value;app.set(4);});
          ring.append(slider);
        }
        ring.append(node('div','dcp-ring-foot','Sent/rank: '+(round*payload/n).toFixed(1)+' / '+traffic.toFixed(1)+' B'));
        plot.append(ring);
      }
      stats.replaceChildren(node('span','',L.width+': '+width+'/32'),node('span','',L.payload+': '+payload+' B'),node('span','',L.traffic+': '+(round*payload/n).toFixed(1)+' B'));
    });
    const ranks=range(L.ranks,1,3,1,1,v=>{n=2**v;ranks.out.textContent=String(n);app.set(+app.panel.querySelector('.dcp-seek').value);});ranks.out.textContent='2';const tok=range(L.tokens,1,8,tokens,1,v=>{tokens=v;app.set(+app.panel.querySelector('.dcp-seek').value);});app.fields.append(ranks.wrap,tok.wrap);app.panel.append(node('p','dcp-note',L.noteM));app.set(0);
  }
  function enhance(){for(const host of document.querySelectorAll('.distributed-computation-probe[data-probe]')){if(host.dataset.ready)return;const L=host.dataset.lang==='zh'?zh:en;if(host.dataset.probe==='fsdp')fsdp(host,L);else if(host.dataset.probe==='megatron')megatron(host,L);else continue;host.dataset.ready='yes';const fallback=host.previousElementSibling;if(fallback?.tagName==='P'&&fallback.querySelector('img[src*="-still.svg"]'))fallback.hidden=true;}}
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',enhance);else enhance();if(window.document$?.subscribe)window.document$.subscribe(enhance);
})();
