const assert=require('node:assert/strict');const {i3dMath,vivitKeys}=require('../docs/javascripts/video-architecture-labs.js');
for(let t=0;t<3;t++)for(let p=0;p<4;p++){
 const spatial=vivitKeys(t,p,0),temporal=vivitKeys(t,p,1),reach=vivitKeys(t,p,2);
 assert.equal(spatial.length,4);assert(spatial.every(([tt])=>tt===t));assert.equal(temporal.length,3);assert(temporal.every(([,pp])=>pp===p));assert.equal(reach.length,12);
 const composed=new Set(temporal.flatMap(([tt,pp])=>vivitKeys(tt,pp,0).map(k=>k.join(','))));assert.equal(composed.size,12);
}
for(let d=-2;d<=2;d+=.25)for(let stage=0;stage<=3;stage++){
 const {responses,part,sum,final}=i3dMath(d,stage);assert.deepEqual(responses,[3.5,3.5+d,3.5]);assert(Math.abs(final-3.5-d/3)<1e-12);assert(Math.abs(sum-part.slice(0,stage).reduce((a,b)=>a+b,0))<1e-12);assert(part.every(x=>x*23<=45));
}
console.log('PASS actual ViViT direct/composed reachability and I3D temporal contributions');
