const assert = require('node:assert/strict');
const {wa,density,inflate,optimizer,objective}=require('./numerics.js');
const close=(a,b,tol=1e-8)=>assert.ok(Math.abs(a-b)<=tol,`${a} != ${b}`);
// Independent finite differences check derivative signs and softmax normalization.
for(const xs of [[0,3,10],[-3,-1,2,9],[1,1,1],[10000,10002,10005]]) {
  for(const gamma of [.2,1,2,10]) {
    const result=wa(xs,gamma),h=1e-5;
    xs.forEach((_,i)=>{
      const plus=xs.slice(),minus=xs.slice();plus[i]+=h;minus[i]-=h;
      close(result.gradient[i],(wa(plus,gamma).value-wa(minus,gamma).value)/(2*h),2e-6);
    });
    close(result.gradient.reduce((a,b)=>a+b,0),0,1e-10);
    close(result.plus.reduce((a,b)=>a+b,0),1);
    assert.ok(result.value>=-1e-10 && result.value<=result.hpwl+1e-10);
    const shifted=wa(xs.map(x=>x+100000),gamma);
    close(result.value,shifted.value);result.gradient.forEach((x,i)=>close(x,shifted.gradient[i]));
  }
}
close(wa([0,3,10],.01).value,10);
close(wa([0,0],2).value,0);
assert.throws(()=>wa([0,1],0));
// Four-bin hand calculation and conservation of all excess contributions.
close(density([80,20,65,35],100,.6).overflow,.125);
assert.deepEqual(density([80,20,65,35],100,.6).excess,[20,0,5,0]);
close(density([80,20,65,35],100,.8).overflow,0);
assert.ok(density([80,20,65,35],100,.5).overflow>density([80,20,65,35],100,.6).overflow);
// Threshold continuity, area/edge distinction, integer rounding and cap.
assert.deepEqual(inflate(.7),{ratio:1,width:100,height:60,actualRatio:1});
close(inflate(.95).ratio,1);
close(inflate(1.9).ratio,3);
assert.equal(inflate(1.9).width,173);assert.equal(inflate(1.9).height,104);
close(inflate(1.2).ratio,1.5955678670360112);
// GD has an independent closed form for this diagonal quadratic.
const trace=optimizer(40);
trace.forEach((h,k)=>{
  close(h.gd[0],8*(11/12)**k);
  close(h.gd[1],k===0?4:0);
  close(h.gdValue,objective(h.gd));
  assert.ok(h.nag.every(Number.isFinite));
});
assert.deepEqual(trace[1].gd,trace[1].nag);
assert.ok(trace[15].nagValue<trace[15].gdValue);
assert.ok(trace.some(h=>h.nag[0]<0),'Nesterov demonstration should show an overshoot');
assert.throws(()=>optimizer(41));
console.log('PASS: WA finite differences / translation / limits; density hand calculation; inflation threshold / rounding / cap; optimizer closed-form baseline / overshoot.');
