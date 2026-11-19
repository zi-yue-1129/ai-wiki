/* MathJax 3.2.2, matching the site's pinned tex-mml-chtml runtime. Not Chromium. */
const fs = require('node:fs');
const assert = require('node:assert/strict');
const {mathjax} = require('mathjax-full/js/mathjax.js');
const {TeX} = require('mathjax-full/js/input/tex.js');
const {CHTML} = require('mathjax-full/js/output/chtml.js');
require('mathjax-full/js/input/tex/AllPackages.js');
const {liteAdaptor} = require('mathjax-full/js/adaptors/liteAdaptor.js');
const {RegisterHTMLHandler} = require('mathjax-full/js/handlers/html.js');
const {SerializedMmlVisitor} = require('mathjax-full/js/core/MmlTree/SerializedMmlVisitor.js');
assert.equal(require('mathjax-full/package.json').version, '3.2.2');
const adaptor = liteAdaptor(); RegisterHTMLHandler(adaptor);
const result = JSON.parse(fs.readFileSync(0,'utf8')).map(tex => {
  const errors=[];
  const input = new TeX({packages:['base','ams','newcommand','noundefined','require','autoload','configmacros'],
    processEscapes:true,processEnvironments:true,
    formatError:(jax,error)=>{errors.push(error.message);return jax.formatError(error);}});
  const doc = mathjax.document('',{InputJax:input,OutputJax:new CHTML()});
  let mathml='';
  const original=input.compile.bind(input);
  input.compile=math=>{const root=original(math);mathml=new SerializedMmlVisitor().visitTree(root);return root;};
  const node=doc.convert(tex,{display:true});
  return {tex,mathml,chtml:adaptor.outerHTML(node),errors};
});
process.stdout.write(JSON.stringify(result));
