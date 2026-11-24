const assert=require('node:assert/strict');
const {compute}=require('../docs/javascripts/predictive-coding-labs.js');
for(const settling of [false,true]) for(const a of [0,.2,.8,1])for(const b of [0,.3,.8,1])for(const eta of [.1,.25,.5,.9,1.3]){
 if(settling&&eta>=1)continue;
 const v={a,b,x:b,eta}, {states,target}=compute(settling,v),q=1-(settling?2:1)*eta;
 states.forEach((z,k)=>{assert(Math.abs(z-(target+(states[0]-target)*q**k))<1e-12);if(k)assert(Math.abs(z-target)<=Math.abs(states[k-1]-target)+1e-12);});
 if(settling){const E=z=>.5*((z-a)**2+(z-b)**2);states.forEach((z,k)=>{if(k)assert(E(z)<=E(states[k-1])+1e-12)});}
}
assert(Math.abs(compute(false,{x:.85,eta:.55}).states[1]-.58)<1e-12);
assert(Math.abs(compute(true,{a:.2,b:.8,eta:.25}).states[1]-.35)<1e-12);
console.log('PASS actual predictive-coding lab exports: closed-form trajectories, contraction, overshoot and energy');
