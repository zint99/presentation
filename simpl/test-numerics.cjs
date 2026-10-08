const fs=require('fs'),vm=require('vm'),assert=require('assert/strict');
const html=fs.readFileSync(require('path').join(__dirname,'index.html'),'utf8');
const source=html.split('// BEGIN_NUMERICAL_MODEL')[1].split('// END_NUMERICAL_MODEL')[0];
const context={};vm.createContext(context);vm.runInContext(source,context);
const {solveAnchoredPair,b2bEdges}=context;
function near(a,b,eps=1e-10){assert.ok(Math.abs(a-b)<eps,`${a} != ${b}`);}
const noAnchor=solveAnchoredPair(0);near(noAnchor.x1,10/3);near(noAnchor.x2,20/3);
let previous=Infinity;
for(const lambda of [0,.1,1,2,5,10,20,100,1000]){
 const r=solveAnchoredPair(lambda);near(r.x1+r.x2,10);assert.ok(r.residual<1e-9);
 // Symmetry reduces the first equation to (3+lambda)*x1=10+lambda.
 near(r.x1,(10+lambda)/(3+lambda));const distance=Math.abs(r.x1-1)+Math.abs(r.x2-9);assert.ok(distance<previous);previous=distance;
}
for(const pins of [[0,10],[0,2,10],[0,2,7,10],[10,0,7,2],[-4,-1,2,3,9]]){
 const edges=b2bEdges(pins);const weighted=edges.reduce((sum,e)=>sum+e.weight*e.distance**2,0);near(weighted,Math.max(...pins)-Math.min(...pins));assert.equal(edges.length,2*pins.length-3);
}
const stale=b2bEdges([0,2,7,10]).reduce((sum,e)=>sum+e.weight*([0,4,7,10][e.i]-[0,4,7,10][e.j])**2,0);near(stale,65/6);
assert.throws(()=>b2bEdges([1,1]));assert.throws(()=>solveAnchoredPair(-1));
console.log('PASS: exact pair solution, residual, anchor limit, symmetry, B2B identity, stale weights, singular input guards');
