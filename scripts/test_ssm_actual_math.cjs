const assert=require('node:assert/strict');const {s4d,ssd}=require('../docs/javascripts/ssm-duality-labs.js');
for(const decay of [.55,.79,.98])for(const freq of [.2,.96,1.45])for(let step=0;step<16;step++){
 const r=s4d({decay,freq,step});assert.equal(r.sum[step],decay**step*Math.cos(freq*step)+.63*.93**step*Math.cos(.32*step));assert.equal(r.sum[0],1.63);
}
for(const a2 of [.4,.8,1])for(const a3 of [.4,.7,1])for(const a4 of [.4,.9,1])for(const lastInput of [-2,1.1,2])for(let step=0;step<4;step++){
 const r=ssd({transitions:[a2,a3,a4],lastInput,step});assert(r.error<1e-14);assert(Math.abs(r.h[3]-(a4*(a3*(a2+.7)-.6)+lastInput))<1e-14);for(let j=0;j<4;j++){assert.equal(r.M[j][j],1);for(let i=j+1;i<4;i++)assert.equal(r.M[j][i],null);}assert(r.h.every(v=>190-v*44>40&&190-v*44+20<340));
}
console.log('PASS actual S4D kernel and independent SSD recurrence/matrix exports');
