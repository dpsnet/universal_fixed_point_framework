# -*- coding: utf-8 -*-
import io, json, os, sys
import numpy as np
from scipy.optimize import curve_fit
BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"
sys.path.insert(0, BASE)
sys.path.insert(0, r"E:\workspace\hyper-resolution\universal_fixed_point_framework\src\white_dwarf_analysis")
import white_dwarf_analysis_v10 as v10

def gauss(x, d, x0, s):
    return d * np.exp(-(x - x0) ** 2 / (2 * s ** 2))

d = np.load(os.path.join(BASE, "_desi_spec", "1003378611740398336.npz"))
w, f = d["wave"], d["flux"]
good = np.isfinite(f) & (f > 0)
nf = v10.normalize(w[good], f[good])

c = 4861.3
hw = 60.0
m = (w[good] >= c - hw) & (w[good] <= c + hw)
x, y = w[good][m], 1.0 - nf[m]
core = np.abs(x - c) < 12.0
wing = ~core
print("wing n=%d" % wing.sum())
bb = np.polyfit(x[wing], y[wing], 1)
yb = y - np.polyval(bb, x)
i0 = int(np.argmax(yb))
d0 = max(yb[i0], 0.02)
x00 = x[i0]
s0 = max(np.std(x[yb > 0.3 * d0]) if np.sum(yb > 0.3 * d0) > 2 else 1.0, 0.3)
print("i0=%d yb_peak=%.3f at x=%.2f  s0=%.3f" % (i0, yb[i0], x00, s0))
print("yb range: %.4f..%.4f" % (yb.min(), yb.max()))
try:
    p, cov = curve_fit(gauss, x, yb, p0=[d0, x00, s0],
                       bounds=([0.0, c - 3.0, 0.05], [2.0, c + 3.0, 8.0]), maxfev=4000)
    print("fit OK:", p)
except Exception as e:
    print("fit FAIL:", type(e).__name__, repr(e)[:200])
