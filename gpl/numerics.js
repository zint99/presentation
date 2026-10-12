/* Teaching models, independent of OpenROAD. Pure functions shared by UI and tests. */
(function (root, factory) {
  const api = factory();
  if (typeof module === 'object' && module.exports) module.exports = api;
  else root.GPLMath = api;
})(typeof globalThis !== 'undefined' ? globalThis : this, function () {
  'use strict';
  function wa(xs, gamma) {
    if (!xs.length || !(gamma > 0) || !xs.every(Number.isFinite)) throw new RangeError('Invalid WA input');
    // Center first so the derivative stays accurate even after large translations.
    const lo = Math.min(...xs), hi = Math.max(...xs), span = hi - lo;
    const centered = xs.map(x => x - lo);
    const plus = centered.map(x => Math.exp((x - span) / gamma));
    const minus = centered.map(x => Math.exp(-x / gamma));
    const sp = plus.reduce((a, b) => a + b, 0), sm = minus.reduce((a, b) => a + b, 0);
    const p = plus.map(x => x / sp), m = minus.map(x => x / sm);
    const mp = centered.reduce((a, x, i) => a + x * p[i], 0);
    const mm = centered.reduce((a, x, i) => a + x * m[i], 0);
    const gradient = centered.map((x, i) => p[i] * (1 + (x - mp) / gamma) - m[i] * (1 - (x - mm) / gamma));
    return { value: mp - mm, hpwl: span, gradient, force: gradient.map(v => -v), plus: p, minus: m };
  }
  function density(areas, binArea, target) {
    const total = areas.reduce((a, b) => a + b, 0), capacity = binArea * target;
    if (!(total > 0) || !(binArea > 0) || !(target > 0) || areas.some(a => a < 0)) throw new RangeError('Invalid density input');
    const excess = areas.map(a => Math.max(0, a - capacity));
    return { capacity, excess, overflow: excess.reduce((a, b) => a + b, 0) / total };
  }
  function inflate(congestion, width = 100, height = 60) {
    if (!Number.isFinite(congestion) || width <= 0 || height <= 0) throw new RangeError('Invalid inflation input');
    const ratio = congestion < 0.95 ? 1 : Math.min(3, (congestion / 0.95) ** 2);
    const w = Math.round(width * Math.sqrt(ratio)), h = Math.round(height * Math.sqrt(ratio));
    return { ratio, width: w, height: h, actualRatio: w * h / (width * height) };
  }
  function objective(v) { return (v[0] ** 2 + 12 * v[1] ** 2) / 2; }
  function optimizer(steps) {
    if (!Number.isInteger(steps) || steps < 0 || steps > 40) throw new RangeError('Use 0–40 steps');
    let gd = [8, 4], x = [8, 4], y = [8, 4], a = 1;
    const history = [{ gd: gd.slice(), nag: x.slice(), gdValue: objective(gd), nagValue: objective(x) }];
    for (let k = 0; k < steps; k++) {
      gd = [gd[0] - gd[0] / 12, gd[1] - gd[1]];
      const next = [y[0] - y[0] / 12, y[1] - y[1]];
      const an = (1 + Math.sqrt(1 + 4 * a * a)) / 2, beta = (a - 1) / an;
      y = next.map((v, i) => v + beta * (v - x[i])); x = next; a = an;
      history.push({ gd: gd.slice(), nag: x.slice(), gdValue: objective(gd), nagValue: objective(x) });
    }
    return history;
  }
  return { wa, density, inflate, optimizer, objective };
});
