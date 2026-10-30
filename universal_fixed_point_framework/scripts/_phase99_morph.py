# -*- coding: utf-8 -*-
"""Phase 99 延伸-8：LAMOST/SDSS J233817 Hzeta/Heta 原始形态判读（中心凹=吸收 vs 凸=发射）"""
import os
import numpy as np
from astropy.io import fits
from astroquery.sdss import SDSS

def morph(wl, fl, c, half=25):
    """打印线中心 ±half A 每 5A 的中值形态（相对两侧 100-140A 远旁瓣归一）"""
    far = ((wl > c - 140) & (wl < c - 100)) | ((wl > c + 100) & (wl < c + 140))
    fb = np.median(fl[far]) if far.sum() > 5 else np.median(fl)
    r = fl / fb
    bins = []
    for a in range(-half, half + 1, 5):
        m = (wl > c + a - 2.5) & (wl < c + a + 2.5)
        if m.sum() >= 2:
            bins.append((a, np.median(r[m])))
    return bins

lp = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_lamost_spec\spec-57052-HD101641N252214B01_sp01-149.fits"
hdul = fits.open(lp)
d = hdul[1].data
wl_l = np.array(d["WAVELENGTH"]).ravel()
fl_l = np.array(d["FLUX"]).ravel()
hdul.close()

sp = SDSS.get_spectra(plate=6161, fiberID=622, mjd=56238)[0]
wl_s = 10 ** sp[1].data["loglam"]
fl_s = sp[1].data["flux"]

for lab, c in (("Hzeta", 3889.0), ("Heta", 3835.4)):
    print("== %s (%.0f A) ==" % (lab, c))
    print("  LAMOST 57052 (2016):", " ".join("%+d:%.3f" % (a, v) for a, v in morph(wl_l, fl_l, c)))
    print("  SDSS 6161 (2011)   :", " ".join("%+d:%.3f" % (a, v) for a, v in morph(wl_s, fl_s, c)))
