'use strict';
document.documentElement.classList.add('js');
const slides = [...document.querySelectorAll('.slide')];
const $ = id => document.getElementById(id);
let current = 0;
const dialog = $('toc-dialog');
function indexFromHash() {
  const m = location.hash.match(/^#slide-(\d+)$/);
  return m ? Math.max(0, Math.min(slides.length - 1, Number(m[1]) - 1)) : 0;
}
function updateNotes() {
  $('notes-title').textContent = `${current + 1} / ${slides.length} · ${slides[current].querySelector('h1,h2').textContent}`;
  $('note-text').textContent = slides[current].querySelector('template').content.textContent;
}
function show(index, setHash = true) {
  current = Math.max(0, Math.min(slides.length - 1, index));
  slides.forEach((slide, i) => { slide.hidden = i !== current; });
  slides[current].scrollTop = 0;
  $('count').textContent = `${String(current + 1).padStart(2, '0')} / ${slides.length}`;
  $('chapter-label').textContent = slides[current].dataset.chapter;
  $('progress').style.width = `${(current + 1) / slides.length * 100}%`;
  $('previous').disabled = current === 0;
  $('next').disabled = current === slides.length - 1;
  $('slide-status').textContent = `第 ${current + 1} 页：${slides[current].querySelector('h1,h2').textContent}`;
  document.querySelectorAll('#toc button').forEach((button, i) => button.setAttribute('aria-current', String(i === current)));
  if (setHash) history.replaceState(null, '', `#slide-${current + 1}`);
  updateNotes();
}
slides.forEach((slide, i) => {
  const button = document.createElement('button'), small = document.createElement('small');
  small.textContent = `${String(i + 1).padStart(2, '0')} · ${slide.dataset.chapter}`;
  button.append(small, document.createTextNode(slide.querySelector('h1,h2').textContent));
  button.addEventListener('click', () => { dialog.close(); show(i); });
  $('toc').append(button);
});
function overview() {
  dialog.showModal();
  const button = $('toc').children[current];
  button.focus(); button.scrollIntoView({ block: 'nearest' });
}
function notes() { $('notes').hidden = !$('notes').hidden; updateNotes(); }
async function fullscreen() {
  try {
    if (document.fullscreenElement) await document.exitFullscreen();
    else await document.documentElement.requestFullscreen();
  } catch { $('slide-status').textContent = '当前浏览器不支持全屏，请使用浏览器的全屏功能。'; }
}
$('previous').addEventListener('click', () => show(current - 1));
$('next').addEventListener('click', () => show(current + 1));
$('overview').addEventListener('click', overview);
$('close-toc').addEventListener('click', () => dialog.close());
$('show-notes').addEventListener('click', notes);
$('close-notes').addEventListener('click', () => { $('notes').hidden = true; });
$('fullscreen').addEventListener('click', fullscreen);
window.addEventListener('hashchange', () => show(indexFromHash(), false));
document.addEventListener('keydown', event => {
  if (event.ctrlKey || event.metaKey || event.altKey) return;
  if (dialog.open) return;
  if (event.key === 'Escape') { $('notes').hidden = true; return; }
  if (event.target.closest('input,textarea,select,[contenteditable="true"]')) return;
  if (event.target.closest('button,a') && [' ', 'Enter'].includes(event.key)) return;
  const key = event.key.toLowerCase();
  if (['arrowright','arrowdown','pagedown',' '].includes(key)) { event.preventDefault(); show(current + 1); }
  else if (['arrowleft','arrowup','pageup'].includes(key)) { event.preventDefault(); show(current - 1); }
  else if (key === 'home') { event.preventDefault(); show(0); }
  else if (key === 'end') { event.preventDefault(); show(slides.length - 1); }
  else if (key === 'o') overview();
  else if (key === 'n') notes();
  else if (key === 'f') fullscreen();
});
let touch = null;
$('slides').addEventListener('touchstart', event => {
  if (event.target.closest('input,button,a') || event.touches.length !== 1) { touch = null; return; }
  touch = { x: event.touches[0].clientX, y: event.touches[0].clientY };
}, { passive: true });
$('slides').addEventListener('touchend', event => {
  if (!touch) return;
  const dx = event.changedTouches[0].clientX - touch.x, dy = event.changedTouches[0].clientY - touch.y;
  if (Math.abs(dx) > 65 && Math.abs(dy) < 45) show(current + (dx < 0 ? 1 : -1));
  touch = null;
}, { passive: true });

// SVG labs: all values are calculated, never interpolated from an alleged GPL run.
const C = { teal: '#087e83', orange: '#cb613c', ink: '#1d3639', muted: '#627976', line: '#c7d4cd' };
const t = (x, y, value, size = 20, color = C.ink, anchor = 'start') => `<text x="${x}" y="${y}" font-size="${size}" fill="${color}" text-anchor="${anchor}">${value}</text>`;
const r = (x, y, w, h, fill, opacity = 1) => `<rect x="${x}" y="${y}" width="${w}" height="${h}" fill="${fill}" opacity="${opacity}" rx="2"/>`;
const l = (x, y, xx, yy, color = C.line, width = 2, dash = '') => `<line x1="${x}" y1="${y}" x2="${xx}" y2="${yy}" stroke="${color}" stroke-width="${width}" stroke-dasharray="${dash}"/>`;
const point = (x, y, color, radius = 6) => `<circle cx="${x}" cy="${y}" r="${radius}" fill="${color}"/>`;
function arrow(x, y, xx, yy, color) {
  const a = Math.atan2(yy - y, xx - x), len = 9;
  return l(x, y, xx, yy, color, 3) + `<polygon points="${xx},${yy} ${xx-len*Math.cos(a-.45)},${yy-len*Math.sin(a-.45)} ${xx-len*Math.cos(a+.45)},${yy-len*Math.sin(a+.45)}" fill="${color}"/>`;
}
function labSVG(lab, label, body) {
  document.querySelector(`[data-lab="${lab}"]`).innerHTML = `<svg class="visual" viewBox="0 0 680 435" role="img" aria-labelledby="lab-${lab}"><title id="lab-${lab}">${label}</title>${body}${t(340,421,'教学数值实验 · 非完整 GPL 运行',15,C.muted,'middle')}</svg>`;
}
function renderWA() {
  const gamma = Number($('gamma').value), out = GPLMath.wa([0,3,10],gamma), positions=[100,250,600];
  $('gamma-value').textContent = gamma.toFixed(1);
  $('wa-result').textContent = `WA = ${out.value.toFixed(4)}　|　HPWL = 10`;
  let body=t(40,34,`指数权重（γ = ${gamma.toFixed(1)}）`,21)+t(43,62,'青：p−　橙：p+',16,C.muted)+l(60,221,644,221,C.muted);
  positions.forEach((x,i) => {
    body+=r(x-29,205-out.minus[i]*125,25,out.minus[i]*125,C.teal)+r(x+4,205-out.plus[i]*125,25,out.plus[i]*125,C.orange);
    body+=point(x,221,C.ink)+t(x,255,[0,3,10][i],22,C.ink,'middle');
    const force=out.force[i]; body+=point(x,304,C.ink,4);
    if (Math.abs(force)>.001) body+=arrow(x,304,x+force*43,304,C.teal);
    body+=t(x,351,force.toFixed(4),20,C.teal,'middle');
  });
  body+=t(340,389,'下方：各 pin 的负梯度（力）',18,C.muted,'middle');
  labSVG('wa',`γ=${gamma} 时 WA=${out.value.toFixed(4)}，HPWL=10`,body);
}
function renderDensity() {
  const target=Number($('target').value), values=[80,20,65,35], out=GPLMath.density(values,100,target);
  $('target-value').textContent=target.toFixed(2);
  $('density-result').textContent=`超额面积 = ${out.excess.reduce((a,b)=>a+b,0).toFixed(1)}　|　O = ${out.overflow.toFixed(4)}`;
  let body=t(340,33,`每个 bin 容量 = ${out.capacity.toFixed(0)}`,23,C.orange,'middle');
  values.forEach((v,i)=>{
    const x=51+i*153,y=310;
    body+=r(x,65,112,245,'#e2e9df')+r(x,y-v*2.45,112,v*2.45,C.teal);
    if(out.excess[i]>0)body+=r(x,y-v*2.45,112,out.excess[i]*2.45,C.orange);
    body+=l(x-5,y-out.capacity*2.45,x+117,y-out.capacity*2.45,C.orange,3,'5 4');
    body+=t(x+56,344,`占用 ${v}`,19,C.ink,'middle')+t(x+56,375,`超额 ${out.excess[i].toFixed(0)}`,18,C.orange,'middle');
  });
  labSVG('density',`目标密度${target}，overflow ${out.overflow.toFixed(4)}`,body);
}
let steps=0;
function renderOptimizer() {
  const history=GPLMath.optimizer(steps), last=history[history.length-1], cx=325,cy=229,scale=33;
  const coords=v=>[cx+v[0]*scale,cy-v[1]*scale];
  let body=t(40,35,'f = ½(x² + 12y²)',23);
  for(const radius of [50,100,150,220,290])body+=`<ellipse cx="${cx}" cy="${cy}" rx="${radius}" ry="${radius/Math.sqrt(12)}" fill="none" stroke="${C.line}"/>`;
  body+=l(24,cy,653,cy)+l(cx,56,cx,347)+point(cx,cy,C.ink,4)+t(cx-10,cy+25,'最优点',16,C.ink,'end');
  for(const [key,color] of [['gd',C.teal],['nag',C.orange]]) {
    const points=history.map(h=>coords(h[key]));
    body+=`<polyline points="${points.map(p=>p.join(',')).join(' ')}" fill="none" stroke="${color}" stroke-width="3"/>`;
    points.forEach(([x,y])=>body+=point(x,y,color,2.5));
    const [x,y]=coords(last[key]);body+=point(x,y,color,key==='nag'?6:9);
  }
  body+=t(55,373,'青：GD',19,C.teal)+t(260,373,'橙：Nesterov',19,C.orange)+t(615,373,`k = ${steps}`,20,C.ink,'end');
  $('opt-result').innerHTML=`迭代 ${steps} / 40<br>f(GD) = ${last.gdValue.toFixed(6)}<br>f(Nesterov) = ${last.nagValue.toFixed(6)}`;
  $('opt-step').disabled=steps>=40;
  labSVG('optimizer',`第${steps}轮：梯度下降与 Nesterov 的计算轨迹`,body);
}
function renderInflation() {
  const congestion=Number($('congestion').value), out=GPLMath.inflate(congestion), scale=2.3,cx=338,cy=202;
  $('congestion-value').textContent=congestion.toFixed(2);
  $('inflation-result').innerHTML=`理论面积倍率 r = ${out.ratio.toFixed(4)}<br>模型尺寸 = ${out.width} × ${out.height} DBU<br>舍入后实际面积倍率 = ${out.actualRatio.toFixed(4)}`;
  let body=t(340,37,`c = ${congestion.toFixed(2)} · 固定中心比较尺寸`,22,C.ink,'middle');
  body+=r(cx-out.width*scale/2,cy-out.height*scale/2,out.width*scale,out.height*scale,C.orange,.23);
  body+=`<rect x="${cx-out.width*scale/2}" y="${cy-out.height*scale/2}" width="${out.width*scale}" height="${out.height*scale}" fill="none" stroke="${C.orange}" stroke-width="3"/>`;
  body+=r(cx-115,cy-69,230,138,C.teal)+t(cx,cy+7,'100 × 60',24,'white','middle');
  body+=l(cx,55,cx,348,C.muted,1,'5 4')+l(90,cy,585,cy,C.muted,1,'5 4');
  body+=t(340,385,`虚拟面积 +${((out.actualRatio-1)*100).toFixed(1)}%`,26,C.orange,'middle');
  labSVG('inflation',`拥塞${congestion}，虚拟尺寸${out.width}乘${out.height} DBU`,body);
}
$('gamma').addEventListener('input',renderWA);
$('target').addEventListener('input',renderDensity);
$('congestion').addEventListener('input',renderInflation);
$('opt-step').addEventListener('click',()=>{steps=Math.min(40,steps+1);renderOptimizer();});
$('opt-reset').addEventListener('click',()=>{steps=0;renderOptimizer();});
// PDF uses a reproducible, informative baseline, regardless of the last live edits.
function printBaseline() {
  $('gamma').value=2; $('target').value=.6; $('congestion').value=1.2; steps=15;
  renderWA(); renderDensity(); renderInflation(); renderOptimizer();
}
let prePrint=null;
window.addEventListener('beforeprint',()=>{
  prePrint={gamma:$('gamma').value,target:$('target').value,congestion:$('congestion').value,steps};printBaseline();
});
window.addEventListener('afterprint',()=>{
  if(!prePrint)return;
  $('gamma').value=prePrint.gamma;$('target').value=prePrint.target;$('congestion').value=prePrint.congestion;steps=prePrint.steps;
  renderWA();renderDensity();renderInflation();renderOptimizer();prePrint=null;
});
renderWA();renderDensity();renderOptimizer();renderInflation();show(indexFromHash(),false);
