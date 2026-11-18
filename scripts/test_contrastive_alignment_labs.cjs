const assert=require('node:assert/strict');
const {softmax,simclr,alignment}=require('../docs/javascripts/contrastive-alignment-labs.js');
for(const p of [-1,-.2,.1,.4,.8,1])for(const tau of [1.2,1,.8,.6,.4,.2]){
 const a=simclr(p,tau);assert.ok(Math.abs(a.probs.reduce((x,y)=>x+y,0)-1)<1e-14);
 assert.ok(Math.abs(a.loss+Math.log(a.probs[0]))<1e-14);
 const scores=[p,.4,.1,-.2,-.4];const z=scores.reduce((x,s)=>x+Math.exp(s/tau),0);
 a.probs.forEach((v,i)=>assert.ok(Math.abs(v-Math.exp(scores[i]/tau)/z)<1e-14));
}
assert.ok(simclr(.1,.2).loss>simclr(.1,1).loss);assert.ok(simclr(.8,.2).loss<simclr(.8,1).loss);
const base=[[.65,.2,.1,.05],[.08,.72,.12,.08],[.05,.15,.2,.6]],h=[[.3,.8],[.9,.2],[.2,-.4],[-.7,.5]];
for(let step=0;step<3;step++)for(let source=0;source<4;source++)for(const bias of [-2,0,2]){
 const {p,ctx}=alignment(step,source,bias);const un=base[step].map((v,i)=>v*Math.exp(i===source?bias:0)),z=un.reduce((x,y)=>x+y,0);
 p.forEach((v,i)=>assert.ok(Math.abs(v-un[i]/z)<1e-14));ctx.forEach((v,k)=>assert.ok(Math.abs(v-p.reduce((x,a,i)=>x+a*h[i][k],0))<1e-14));
}
assert.deepEqual(softmax([1000,1000]),[.5,.5]);console.log('PASS actual lab exports: NT-Xent, normalized alignment, context, extreme-score stability');
