#!/usr/bin/env node
'use strict';
// Unit checks for the deterministic interaction state. Rendered QA is separate.
const assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm');
const source=fs.readFileSync('docs/javascripts/self-supervised-labs.js','utf8');
function setup(kind,locale) {
  const map={};
  function element(name) {
    return {name,value:'',textContent:'',disabled:false,events:{},
      setAttribute(k,v){this[k]=v},
      addEventListener(k,v){this.events[k]=v}};
  }
  const host={dataset:{selfSupervisedLab:kind,locale},classList:{add(){}},
    set innerHTML(value){this.html=value; for(const key of ['play','prev','next','seek','speed'])map['[data-act="'+key+'"]']=element(key);
      map['.ssl-figure']=element('figure');map['.ssl-explain']=element('explain');map['.ssl-compute']=element('compute');
      map['[data-act="speed"]'].value='1';},
    querySelector(selector){return map[selector]}};
  const document={readyState:'complete',querySelectorAll(){return [host]}};
  const intervals=[];
  vm.runInNewContext(source,{document,window:{},setInterval(fn,ms){intervals.push({fn,ms});return intervals.length},
    clearInterval(){}},{filename:'self-supervised-labs.js'});
  return {host,map,intervals,control:name=>map['[data-act="'+name+'"]']};
}
for(const kind of ['moco','byol'])for(const locale of ['en','zh-TW']) {
  const h=setup(kind,locale),next=h.control('next'),prev=h.control('prev'),seek=h.control('seek');
  const output=()=>h.map['.ssl-compute'].textContent;
  assert.match(output(),/0\.700/);
  assert.match(output(),/0\.300/);
  assert.match(h.map['.ssl-figure'].innerHTML,/<svg/);
  next.events.click();assert.equal(seek.value,'1');
  prev.events.click();assert.equal(seek.value,'0');
  seek.value='3';seek.events.input();assert.match(output(),/0\.850/);
  if(kind==='moco')assert.match(output(),/0\.355/);
  else assert.match(output(),/0\.300/);
  seek.value='4';seek.events.input();assert.match(output(),/0\.355/);
  if(kind==='moco')assert.match(output(),/FIFO \[B C D E F G\]/);
  else assert.match(output(),/Target gradient = 0/);
  seek.value='14';seek.events.input();assert.equal(next.disabled,true);
  const play=h.control('play');play.events.click();assert.equal(seek.value,'0');
  assert.equal(h.intervals[0].ms,1250);
  play.events.click();assert.match(play.textContent,/Play|播放/);
  if(locale==='zh-TW')assert.match(h.map['.ssl-explain'].textContent,/回合/);
}
console.log('PASS: 4 bilingual MoCo/BYOL DOM simulations; deterministic FIFO, SGD, EMA, seek and playback');
