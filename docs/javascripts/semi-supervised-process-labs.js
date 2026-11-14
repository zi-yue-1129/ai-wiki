/* Original CC BY-SA 4.0 — deterministic FixMatch and Mean Teacher arithmetic. */
(() => {
  'use strict';
  const N='http://www.w3.org/2000/svg',fmt=n=>Number(n).toFixed(3),
  str={en:{prev:'Previous',next:'Next',play:'Play',pause:'Pause',reset:'Reset',seek:'Step',speed:'Speed',weak:'Weak-view confidence',gate:'Threshold',strong:'Strong-view target P',alpha:'EMA coefficient',student:'Student',teacher:'Teacher',loss:'Unsupervised CE',stages:['Weak view','Confidence gate','Strong view','Loss'],noteF:'Synthetic inputs; not model outputs or augmentations.',noteT:'Synthetic scalar weights; the teacher never receives gradients.'},
  zh:{prev:'上一步',next:'下一步',play:'播放',pause:'暫停',reset:'重設',seek:'步驟',speed:'速度',weak:'弱視角信心',gate:'門檻',strong:'強視角目標類別機率',alpha:'EMA 係數',student:'學生',teacher:'教師',loss:'無監督交叉熵',stages:['弱視角','信心門檻','強視角','損失'],noteF:'人工機率，並非模型輸出或影像增強結果。',noteT:'人工純量權重；教師不接受梯度。'}};
  function html(tag,parent,attrs={},content){const e=document.createElement(tag);Object.entries(attrs).forEach(([k,v])=>e.setAttribute(k,v));if(content!==undefined)e.textContent=content;parent.append(e);return e;}
  function svg(tag,parent,attrs={},content){const e=document.createElementNS(N,tag);Object.entries(attrs).forEach(([k,v])=>e.setAttribute(k,v));if(content!==undefined)e.textContent=content;parent.append(e);return e;}
  const defaults={weak:.97,gate:.95,strong:.62,alpha:.75},student=[.15,.85,.35,.95,.50,.72];
  function init(host){
    if(host.dataset.ready)return;
    const fix=host.dataset.kind==='fixmatch',L=str[host.dataset.lang==='zh'?'zh':'en'],last=fix?3:5,state={t:0,playing:false,speed:1,timer:null,values:{...defaults}};
    const root=document.createElement('div'),inputs=html('div',root,{class:'semi-inputs'}),bar=html('div',root,{class:'semi-bar'}),viewport=html('div',root,{class:'semi-viewport',tabindex:'0',role:'group','aria-label':'Scrollable teaching diagram'}),figure=svg('svg',viewport,{viewBox:'0 0 640 300',width:'640',height:'300',role:'img','aria-label':fix?'FixMatch confidence gate calculation':'Mean Teacher EMA trajectory'}),read=html('div',root,{class:'semi-read',role:'status','aria-live':'polite'}),note=html('p',root,{class:'semi-note'},fix?L.noteF:L.noteT);
    const params=fix?[['weak',.5,.99,L.weak],['gate',.6,.99,L.gate],['strong',.1,.99,L.strong]]:[['alpha',.5,.99,L.alpha]];
    const controls={};
    for(const [key,min,max,label] of params){
      const field=html('label',inputs,{},label),out=html('output',field,{},fmt(state.values[key])),input=html('input',field,{type:'range',min:String(min),max:String(max),step:'.01',value:String(state.values[key]),'aria-label':label});
      controls[key]={input,out};input.addEventListener('input',()=>{stop();state.values[key]=+input.value;out.textContent=fmt(state.values[key]);draw();});
    }
    const buttons={};for(const [key,label] of [['prev',L.prev],['next',L.next],['play',L.play],['reset',L.reset]])buttons[key]=html('button',bar,{type:'button','data-act':key},label);
    const seekBox=html('label',bar,{},L.seek),seek=html('input',seekBox,{type:'range',min:'0',max:String(last),step:'1',value:'0','data-act':'seek','aria-label':L.seek});
    const speedBox=html('label',bar,{},L.speed),speed=html('select',speedBox,{'data-act':'speed','aria-label':L.speed});
    for(const value of [.5,1,2])html('option',speed,{value:String(value)},value+'×');speed.value='1';
    function stop(){if(state.timer!==null)clearInterval(state.timer);state.timer=null;state.playing=false;buttons.play.textContent=L.play;buttons.play.setAttribute('aria-pressed','false');}
    function go(t){state.t=Math.max(0,Math.min(last,t));draw();if(state.t===last)stop();}
    function play(){if(state.t===last)go(0);state.playing=true;buttons.play.textContent=L.pause;buttons.play.setAttribute('aria-pressed','true');state.timer=setInterval(()=>go(state.t+1),850/state.speed);}
    buttons.prev.addEventListener('click',()=>{stop();go(state.t-1);});
    buttons.next.addEventListener('click',()=>{stop();go(state.t+1);});
    buttons.play.addEventListener('click',()=>state.playing?stop():play());
    buttons.reset.addEventListener('click',()=>{stop();for(const [key] of params){state.values[key]=defaults[key];controls[key].input.value=String(defaults[key]);controls[key].out.textContent=fmt(defaults[key]);}state.speed=1;speed.value='1';go(0);});
    seek.addEventListener('input',()=>{stop();go(+seek.value);});
    speed.addEventListener('change',()=>{state.speed=+speed.value;if(state.playing){stop();play();}});
    document.addEventListener('visibilitychange',()=>{if(document.hidden)stop();});
    function rect(x,y,w,h,fill,stroke='#cedce4'){svg('rect',figure,{x,y,width:w,height:h,rx:10,fill,stroke,'stroke-width':1.5});}
    function text(x,y,value,color='#243e52',size=16){svg('text',figure,{x,y,'font-family':'system-ui,Arial,sans-serif','font-size':size,'font-weight':600,fill:color,'text-anchor':'middle'},String(value));}
    function line(path,color='#d4e2ec',dashed=false){svg('path',figure,{d:path,fill:'none',stroke:color,'stroke-width':3,...(dashed?{'stroke-dasharray':'5 6'}:{})});}
    function drawFix(){
      const {weak,gate,strong}=state.values,pass=weak>=gate,ce=pass?-Math.log(strong):0,t=state.t;
      for(let j=0;j<4;j++){
        const x=89+j*154,active=t>=j,valid=j<2||pass,color=active?(valid?'#0b8a82':'#ba6569'):'#849baa';
        rect(x-63,65,126,91,active?(valid?'#e9f7f3':'#faeeee'):'#f0f5f8',active?color:'#d7e3e9');
        text(x,99,['Weak','Gate','Strong','Loss'][j]);
        text(x,132,j===0?fmt(weak):j===1?fmt(gate):j===2?(t>=2?fmt(strong):'—'):(t>=3?fmt(ce):'—'),color,18);
        if(j<3)line('M'+(x+64)+' 111 H'+(x+87),active?color:'#a1b4c2',!active);
      }
      rect(52,181,536,52,'#f4f8fa');rect(84,204,464,12,'#d9e5ea');rect(84,204,464*weak,12,'#2867a7','#2867a7');
      line('M'+(84+464*gate)+' 190 V228','#cf8a29');
      text(320,263,t<1?'WAIT':(pass?'PASS':'SKIP'),pass?'#0b8a82':'#ba6569',19);
      read.textContent=L.stages[t]+' · '+L.weak+' = '+fmt(weak)+' · τ = '+fmt(gate)+' · '+L.loss+' = '+(t<3?'—':fmt(ce));
    }
    function drawTeacher(){
      const a=state.values.alpha,t=state.t,teacher=[student[0]];for(let i=1;i<student.length;i++)teacher.push(a*teacher[i-1]+(1-a)*student[i]);
      const X=i=>72+98*i,Y=v=>247-176*v;
      rect(38,32,567,244,'#f7f9fc');
      for(const v of [0,.5,1]){line('M68 '+Y(v)+' H570');text(50,Y(v)+4,v.toFixed(1),'#839aa9',12);}
      for(const [values,color] of [[student,'#2869aa'],[teacher,'#d08a27']]){
        svg('polyline',figure,{points:values.slice(0,t+1).map((v,i)=>X(i)+','+Y(v)).join(' '),fill:'none',stroke:color,'stroke-width':3.5,'stroke-linecap':'round'});
        for(let i=0;i<=t;i++)svg('circle',figure,{cx:X(i),cy:Y(values[i]),r:i===t?7:4,fill:color,stroke:'white','stroke-width':2});
      }
      for(let i=0;i<6;i++)text(X(i),270,i,'#869eae',13);
      text(138,20,'Student','#2869aa',15);text(292,20,'Teacher (EMA)','#d08a27',15);
      line('M'+X(t)+' 36 V249','#0b8a82',true);
      read.textContent=L.seek+' '+t+'/5 · '+L.student+' = '+fmt(student[t])+' · '+L.teacher+' = '+fmt(teacher[t])+' · |Δ| = '+fmt(Math.abs(student[t]-teacher[t]))+(t?' · '+fmt(a)+' × '+fmt(teacher[t-1])+' + '+fmt(1-a)+' × '+fmt(student[t]):'');
    }
    function draw(){figure.replaceChildren();seek.value=String(state.t);buttons.prev.disabled=state.t===0;buttons.next.disabled=state.t===last;if(fix)drawFix();else drawTeacher();}
    host.replaceChildren(root);host.dataset.ready='1';buttons.play.setAttribute('aria-pressed','false');draw();
  }
  function boot(){document.querySelectorAll('.semi-process-lab[data-kind]:not([data-ready])').forEach(init);}
  if(typeof document$!=='undefined'&&document$&&document$.subscribe)document$.subscribe(boot);
  else if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',boot);
  else boot();
})();