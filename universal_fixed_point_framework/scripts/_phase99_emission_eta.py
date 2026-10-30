# -*- coding: utf-8 -*-
"""Phase 99 延伸-4：补测 Hzeta/Heta 发射（发射线集中在蓝端高阶线）"""
import re, glob, os
import numpy as np
from astropy.io import fits

SPEC = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_lamost_spec"
BALMER = {"Hbeta": 4861.3, "Hgamma": 4340.5, "Hdelta": 4101.7,
          "Heps": 3970.1, "Hzeta": 3889.0, "Heta": 3835.4}

# 目标：J233817 的 4 条 + J101712 的 3 条
targets = ["spec-57052-HD101641N252214B01_sp01-149", "spec-57291-EG234156N071501V01_sp15-161",
           "spec-57312-EG234156N071501M01_sp15-172", "spec-57312-EG234156N071501M01_sp16-152",
           "spec-57732-HD101311N212511B01_sp12-228", "spec-57862-HD101311N212511B02_sp12-228"]

def analyze(path):
    hdul = fits.open(path)
    d = hdul[1].data
    wl = np.array(d["WAVELENGTH"]).ravel()
    fl = np.array(d["FLUX"]).ravel()
    iv = np.array(d["IVAR"]).ravel()
    hdul.close()
    good = np.isfinite(fl) & (fl > 0) & (iv > 0)
    fl[~good] = np.nan
    mc = ((wl > 4500) & (wl < 4700)) | ((wl > 5100) & (wl < 5400))
    med = np.nanmedian(fl[mc])
    if not np.isfinite(med) or med <= 0:
        return None
    fl = fl / med
    out = []
    for lab, c in BALMER.items():
        win = (wl > c - 6) & (wl < c + 6)
        basew = ((wl > c - 15) & (wl < c - 6)) | ((wl > c + 6) & (wl < c + 15))
        if win.sum() < 2 or basew.sum() < 4:
            out.append("%s: 无数据" % lab)
            continue
        pk = np.nanmedian(fl[win])
        bg = np.nanmedian(fl[basew])
        if pk > bg * 1.1 and pk > 1.05:
            tag = "EMISSION(%.2f)" % (pk - bg)
        elif pk < bg * 0.95:
            tag = "ABS(%.2f)" % (1 - pk / bg)
        else:
            tag = "flat"
        out.append("%s %.2f/%.2f %s" % (lab, pk, bg, tag))
    return " | ".join(out)

for t in targets:
    p = os.path.join(SPEC, t + ".fits")
    if os.path.exists(p):
        print(t.replace("spec-", ""))
        print("  ", analyze(p))
    else:
        print(t, "不存在")
