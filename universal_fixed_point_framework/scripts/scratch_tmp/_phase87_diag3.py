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

# 1003378611740398336: Hβ EW=22.8 强线
d = np.load(os.path.join(BASE, "_desi_spec", "1003378611740398336.npz"))
w, f = d["wave"], d["flux"]
good = np.isfinite(f) & (f > 0)
print("wave range:", w[good].min(), w[good].max(), "n:", good.sum())
nf = v10.normalize(w[good], f[good])

c = 4861.3
m = (w[good] >= c - 60) & (w[good] <= c + 60)
x, y = w[good][m], 1.0 - nf[m]
print("window n=%d y range %.4f..%.4f  median(1-nf)=%.4f" % (len(x), y.min(), y.max(), np.median(y)))
i0 = int(np.argmax(y))
print("peak y=%.3f at x=%.2f" % (y[i0], x[i0]))

try:
    p, _ = curve_fit(gauss, x, y, p0=[y[i0], x[i0], 1.0],
                     bounds=([0.0, c - 2.0, 0.05], [2.0, c + 2.0, 8.0]), maxfev=4000)
    print("fit OK: d=%.3f x0=%.3f sig=%.3f" % tuple(p))
except Exception as e:
    print("fit FAIL:", repr(e))
    # 打印初值附近样本
    print("x[i0-3:i0+4]=", x[i0-3:i0+4], "y[i0-3:i0+4]=", y[i0-3:i0+4])

# 检查 npz 键
print("npz keys:", list(d.keys()))
print("flux sample:", f[good][:3])
