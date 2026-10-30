# -*- coding: utf-8 -*-
"""Phase 99 延伸-7：论文口径（全局 4 次多项式归一化）重测 LAMOST J233817 Hzeta/Heta
与 SDSS 6161-56238-622（论文发射光谱）同口径对照
"""
import os
import numpy as np
from astropy.io import fits
from astroquery.sdss import SDSS

def poly_norm_ew(wl, fl, c, order=4, core=12.0, clean=30.0):
    """全局多项式（避线区 clean 宽度）归一化 + 积分 EW"""
    mask = np.isfinite(fl) & (fl > 0)
    wl_c, fl_c = wl[mask], fl[mask]
    # 避开所有 Balmer 线（±clean Å）
    bal = [6562.8, 4861.3, 4340.5, 4101.7, 3970.1, 3889.0, 3835.4]
    keep = np.ones(len(wl_c), bool)
    for b in bal:
        keep &= ~((wl_c > b - clean) & (wl_c < b + clean))
    if keep.sum() < 50:
        return None
    p = np.polyfit(wl_c[keep], fl_c[keep], order)
    base = np.polyval(p, wl_c)
    base[base <= 0] = np.nan
    r = fl_c / base - 1.0
    m = (wl_c > c - core) & (wl_c < c + core)
    if m.sum() < 3:
        return None
    ew = np.sum(r[m][:-1] * np.diff(wl_c[m]))
    return ew, np.nanmedian(r[m])

# LAMOST 目标星（J233817 确凿 0″ 匹配）
lp = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_lamost_spec\spec-57052-HD101641N252214B01_sp01-149.fits"
hdul = fits.open(lp)
d = hdul[1].data
wl_l = np.array(d["WAVELENGTH"]).ravel()
fl_l = np.array(d["FLUX"]).ravel()
hdul.close()
print("LAMOST 57052 (J233817, 2016, snrr=10.1) 全局多项式口径:")
for lab, c in (("Hbeta", 4861.3), ("Hdelta", 4101.7), ("Hzeta", 3889.0), ("Heta", 3835.4)):
    r = poly_norm_ew(wl_l, fl_l, c)
    if r:
        ew, peak = r
        print("  %s EW=%.2f A peak=%.3f -> %s" % (lab, ew, peak,
              "EM" if ew < -1 else ("abs" if ew > 0.5 else "flat")), flush=True)

# SDSS 论文光谱（同口径）
print("SDSS 6161-56238-622 (J233817, 2011) 全局多项式口径:")
sp = SDSS.get_spectra(plate=6161, fiberID=622, mjd=56238)[0]
wl_s = 10 ** sp[1].data["loglam"]
fl_s = sp[1].data["flux"]
for lab, c in (("Hbeta", 4861.3), ("Hdelta", 4101.7), ("Hzeta", 3889.0), ("Heta", 3835.4)):
    r = poly_norm_ew(wl_s, fl_s, c)
    if r:
        ew, peak = r
        print("  %s EW=%.2f A peak=%.3f -> %s" % (lab, ew, peak,
              "EM" if ew < -1 else ("abs" if ew > 0.5 else "flat")), flush=True)
