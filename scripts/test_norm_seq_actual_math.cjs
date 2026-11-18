const assert=require('node:assert/strict');
const {norm,buildStates}=require('../docs/javascripts/norm-seq-labs.js');
for(let shift=-4;shift<=4;shift++)for(let spike=-3;spike<=3;spike++){
 const x=[1,3,5,7,9].map((v,i)=>v+shift+(i===2?spike:0)),r=norm(x),mu=x.reduce((a,b)=>a+b)/5;
 assert.equal(r.mu,mu);assert(Math.abs(r.sd**2-(x.reduce((a,v)=>a+(v-mu)**2,0)/5+1e-5))<1e-13);
 for(let i=0;i<5;i++)assert(Math.abs(r.z[i]-(x[i]-mu)/r.sd)<1e-13);
 if(!spike)for(let i=0;i<5;i++)assert(Math.abs(r.z[i]-norm([1,3,5,7,9]).z[i])<1e-13);
}
const emb={A:[1,.2],B:[.2,.9],C:[-.6,.4],D:[.6,-.8]};
for(const reverse of [true,false]){
 const r=buildStates(reverse);assert.equal(r.states.length,8);assert.deepEqual(r.order,reverse?['D','C','B','A']:['A','B','C','D']);
 let h=[0,0];for(let i=0;i<4;i++){h=h.map((v,j)=>.65*v+emb[r.order[i]][j]);assert.deepEqual(r.states[i+1],h);}
 for(const [i,e] of [[0,[.1,.15]],[1,[.15,-.25]],[2,[-.2,.3]]]){h=h.map((v,j)=>.7*v+e[j]);assert.deepEqual(r.states[i+5],h);}
}
assert.notDeepEqual(buildStates(true).states[4],buildStates(false).states[4]);console.log('PASS actual exported LayerNorm grid and independently reconstructed encoder/decoder recurrence');
