const assert=require('node:assert/strict');
const select=require('./concept_motion_fixture_selector.cjs');
const image=src=>({getAttribute:name=>name==='src'?src:null});
const correct=image('https://wiki.example/assets/concept-animations/example-still.svg');
const wrong=image('https://wiki.example/assets/example-still.svg');
const relative=image('../../assets/concept-animations/example-motion.svg');
const selector='img[src*="concept-animations/"]';
assert.deepEqual(select(selector,[wrong,correct,relative,image(null)]),[correct,relative]);
assert.deepEqual(select(selector,[wrong]),[]);
assert.deepEqual(select(selector,[]),[]);
assert.throws(()=>select('img',[correct]),/Review changed production selector/);
console.log('PASS actual selector fixture contract: eligible, excluded, relative, missing src and changed selector');

// Instrument actual helper calls, so a mock that silently returns every image fails.
const requiredPlayers=["test_gqa_player.cjs", "test_diffusion_player.cjs", "test_inference_player.cjs", "test_motor_player.cjs", "test_navigation_player.cjs", "test_reviewed_scroll_player.cjs"];
const helperId=require.resolve('./concept_motion_fixture_selector.cjs');
for(const filename of requiredPlayers){
 let calls=0;require.cache[helperId].exports=(selector,images)=>{calls++;return select(selector,images);};
 try{const id=require.resolve('./'+filename);delete require.cache[id];require(id);assert(calls>0,filename+' bypassed the production selector');}
 finally{require.cache[helperId].exports=select;}
}
