# -*- coding: utf-8 -*-
"""最小复现 2：观测+理论全链路"""
import os, sys, re
import numpy as np

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"
sys.path.insert(0, BASE)
sys.path.insert(0, r"E:\workspace\hyper-resolution\universal_fixed_point_framework\src\white_dwarf_analysis")
exec(open(os.path.join(BASE, "_phase85_r2_continuum.py"), encoding="utf-8").read().split("# ---- 1) 观测侧")[0])

def load_koester(teff, logg):
    best = None
    for fn in os.listdir(os.path.join(BASE, "_koester_spec")):
        mm = re.match(r"fid\d+_([\d.]+)_([\d.]+)\.dat", fn)
        if not mm:
            continue
        t, g = float(mm.group(1)), float(mm.group(2))
        score = (t - teff) ** 2 + (g - logg) ** 2
        if best is None or score < best[0]:
            best = (score, os.path.join(BASE, "_koester_spec", fn))
    arr = np.loadtxt(best[1])
    return arr[:, 0], arr[:, 1]

wl_k, fl_k = load_koester(10059.0, 8.0)
print("Koester 谱: %d 点, %.0f-%.0f Å" % (len(wl_k), wl_k.min(), wl_k.max()))
tm = measure_continuum(wl_k, fl_k)
print("theo D_B:", tm["D_B"], " slope:", tm["slope"], " res:", tm["res"])
