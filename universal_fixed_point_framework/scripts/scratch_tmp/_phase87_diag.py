# -*- coding: utf-8 -*-
import io, json, os, sys
import numpy as np
BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"
sys.path.insert(0, BASE)
sys.path.insert(0, r"E:\workspace\hyper-resolution\universal_fixed_point_framework\src\white_dwarf_analysis")
import white_dwarf_analysis_v10 as v10

# 1) fid 表
fp_tbl = os.path.join(BASE, "paperX_wd_m83c_fid_table.json")
print("fid_tbl exists:", os.path.exists(fp_tbl))
with io.open(fp_tbl, "r", encoding="utf-8") as f:
    fid_tbl = json.load(f)
print("fid_tbl keys sample:", list(fid_tbl.keys())[:5], "n=", len(fid_tbl))

grid = {}
for k, v in fid_tbl.items():
    t, g = k.split("_")
    grid[(float(t), float(g))] = int(v)
teffs = sorted(set(t for t, g in grid)); loggs = sorted(set(g for t, g in grid))
print("teffs:", teffs)
print("loggs:", loggs)

# 2) 某中场星
with io.open(os.path.join(BASE, "paperX_wd_m83e_desi137.json"), "r", encoding="utf-8") as f:
    cat = json.load(f)["samples"]
s = [x for x in cat if 10.0 <= x["B_MG"] < 100.0 and 10000 <= x["Teff"] <= 20000][0]
print("star:", s["gaia_int"], "Teff", s["Teff"], "logg", s["logg"], "B", s["B_MG"])

t, g = min(teffs, key=lambda x: abs(x - s["Teff"])), min(loggs, key=lambda x: abs(x - s["logg"]))
fid = grid.get((t, g))
print("nearest:", t, g, "fid:", fid)
fp = os.path.join(BASE, "_koester_spec", "fid%s_%s_%s.dat" % (fid, t, g))
print("model file exists:", os.path.exists(fp))

# 3) 直接拟合该星该线（打印异常）
import scipy.optimize
d = np.load(os.path.join(BASE, "_desi_spec", str(s["gaia_int"]) + ".npz"))
w, f = d["wave"], d["flux"]
good = np.isfinite(f) & (f > 0)
nf = v10.normalize(w[good], f[good])
c = 4861.3
m = (w[good] >= c - 60) & (w[good] <= c + 60)
x, y = w[good][m], 1.0 - nf[m]
print("obs window: n=%d y range %.3f..%.3f" % (len(x), y.min(), y.max()))
i0 = int(np.argmax(y))
print("peak y=%.3f at %.2f" % (y[i0], x[i0]))

# 4) Koester 谱同样流程
wl_a, fl_a = [], []
with io.open(fp, "r", encoding="utf-8", errors="replace") as fh:
    for line in fh:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        p = line.split()
        if len(p) >= 2:
            try:
                wl_a.append(float(p[0])); fl_a.append(float(p[1]))
            except ValueError:
                pass
wl_a, fl_a = np.array(wl_a), np.array(fl_a)
print("model points:", len(wl_a), "range:", wl_a.min(), wl_a.max())
nm = v10.normalize(wl_a, fl_a)
m2 = (wl_a >= c - 60) & (wl_a <= c + 60)
x2, y2 = wl_a[m2], 1.0 - nm[m2]
print("mod window: n=%d y range %.3f..%.3f" % (len(x2), y2.min(), y2.max()))
i02 = int(np.argmax(y2))
print("mod peak y=%.3f at %.2f" % (y2[i02], x2[i02]))
