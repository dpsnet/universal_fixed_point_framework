# -*- coding: utf-8 -*-
"""Phase 99 M99-2f：解析 LAMOST FITS，验证 Balmer 形态（DA vs 普通恒星）"""
import os
import numpy as np

FITS = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_lamost_spec\spec-57454-HD120800N003716B02_sp06-116.fits"

from astropy.io import fits
hdul = fits.open(FITS)
print("HDUs:", len(hdul))
for i, h in enumerate(hdul):
    print("HDU%d" % i, h.name, h.header.get("NAXIS"), h.header.get("NAXIS1"), h.header.get("NAXIS2"))
h0 = hdul[0].header
for k in ("OBSTIME", "EXPTIME", "SNR", "OBSDATE", "OBJECT", "RA", "DEC"):
    if k in h0:
        print(k, "=", h0[k])

# 尝试读波长与流量
wl = None
fl = None
try:
    d = hdul[1].data  # 扩展
    cols = d.columns.names if hasattr(d, "columns") else None
    print("HDU1 cols:", cols)
    wl = np.array(d["WAVELENGTH"]).ravel()
    fl = np.array(d["FLUX"]).ravel()
except Exception as e:
    print("HDU1 err", e)
if wl is None:
    # HDU0 有 wavelength 头
    try:
        wl = np.array(hdul[0].data["WAVELENGTH"])
        fl = np.array(hdul[0].data["FLUX"])
    except Exception as e:
        print("HDU0 data err", e)
if wl is None:
    # loglam 头
    try:
        if "COEFF0" in h0:
            wl = 10 ** (h0["COEFF0"] + np.arange(h0["NAXIS1"]) * h0.get("COEFF1", 1e-4))
        fl = np.array(hdul[0].data)
    except Exception as e:
        print("loglam err", e)

if wl is not None and fl is not None:
    print("wl len", len(wl), "range %.0f-%.0f" % (wl[0], wl[-1]), "flux len", len(fl))
    # 归一化 + Balmer 区粗看（中值）
    f = np.array(fl, dtype=float)
    f = f / np.nanmedian(f[np.isfinite(f) & (f > 0)])
    for lab, c in (("Hbeta", 4861.3), ("Hgamma", 4340.5), ("Hdelta", 4101.7), ("Heps", 3970.1), ("Hzeta", 3889.0)):
        m = (wl > c - 15) & (wl < c + 15)
        if m.sum() > 3:
            print("%s %.1fA: 中值 %.3f 最小 %.3f" % (lab, c, np.median(f[m]), np.min(f[m])))
    # 连续谱窗（4500-4700, 5000-5200 之间）
    mcont = ((wl > 4500) & (wl < 4700)) | ((wl > 5000) & (wl < 5200))
    print("连续谱中值 %.3f" % np.median(f[mcont]))
