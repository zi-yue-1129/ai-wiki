const assert=require('node:assert/strict');
const {sacMath,dpoMath}=require('../docs/javascripts/sac-dpo-labs.js');
for(const gap of [.25,1,2.5]){let prev=-1;for(let i=0;i<=140;i++){const a=.2+.02*i,{p,H,eq,objective}=sacMath(gap,a);assert(Math.abs(p.reduce((x,y)=>x+y,0)-1)<1e-12);assert(H>=prev-1e-12);prev=H;assert(Math.abs(objective-a*Math.log(Math.exp(2*gap/a)+Math.exp(gap/a)+1))<1e-11);}}
for(const r of [.2,.5,.8])for(const beta of [.2,1,2]){let prev=Infinity;for(let i=0;i<=140;i++){const p=.1+.8*i/140,{margin,logit,loss}=dpoMath(p,r,beta);assert(loss<=prev+1e-12);prev=loss;assert(Math.abs(logit-beta*margin)<1e-12);assert(Math.abs(loss+Math.log(1/(1+Math.exp(-logit))))<1e-12);}}
assert(dpoMath(.1,.8,2).loss>7);assert(Math.abs(dpoMath(.8,.8,2).loss-Math.log(2))<1e-12);
console.log('PASS actual SAC softmax/objective and DPO reference-relative logistic math');
