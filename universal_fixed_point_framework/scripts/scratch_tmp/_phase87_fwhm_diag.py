# -*- coding: utf-8 -*-
"""FWHM 诊断：3 颗星 Hβ 扫描细节"""
import io, json, os, sys
import numpy as np
BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"
sys.path.insert(0, BASE)
sys.path.insert(0, r"E:\workspace\hyper-resolution\universal_fixed_point_framework\src\white_dwarf_analysis")
import white_dwarf_analysis_v10 as v10

with io.open(os.path.join(BASE, "paperX_wd_m83e_desi137.json"), "r", encoding="utf-8") as f:
    cat = json.load(f)["samples"]
with io.open(os.path.join(BASE, "_m83e_desi_ew.json"), "r", encoding="utf-8") as f:
    ew0 = json.load(f)
pick = None
for s in cat:
    gid = str(s["gaia_int"])
    if gid not in ew0 or not ew0[gid].get("ok"):
        continue
    if not (8000 <= s["Teff"] <= 25000):
        continue
    if s["B_MG"] < 10 and pick is None:
        pick = s
        break
for s in (pick,):
    gid = str(s["gaia_int"])
    d = np.load(os.path.join(BASE, "_desi_spec", gid + ".npz"))
    wave, flux = d["wave"], d["flux"]
    good = np.isfinite(flux) & (flux > 0)
    w, f = wave[good], flux[good]
    nf = v10.normalize(w, f)
    c = 4861.3
    m = (w >= c - 60) & (w <= c + 60)
    x, y = w[m], 1.0 - nf[m]
    core = np.abs(x - c) < 12.0
    wing = ~core
    bb = np.polyfit(x[wing], y[wing], 2)
    yb = y - np.polyval(bb, x)
    cm = np.abs(x - c) < 5.0
    d_meas = float(np.median(y[cm]))
    wb = (np.abs(x - c) >= 15.0) & (np.abs(x - c) <= 22.0)
    bg = np.median(y[wb])
    hm = bg + d_meas / 2.0
    print("gid=%s B=%.1f Teff=%d d_meas=%.3f bg=%.3f hm=%.3f" % (gid, s["B_MG"], s["Teff"], d_meas, bg, hm))
    print(" y center(±5A) median=%.3f  y min=%.3f max=%.3f" % (np.median(y[cm]), y.min(), y.max()))
    cent = int(np.argmin(np.abs(x - c)))
    print(" y[cent]=%.3f  y[cent-10]=%.3f y[cent+10]=%.3f" % (y[cent], y[cent-10], y[cent+10]))
    print(" n>=hm: %d / %d" % ((y >= hm).sum(), len(y)))
    print(" y 头部10个:", np.round(y[:10], 3))
    print(" y 尾部10个:", np.round(y[-10:], 3))
