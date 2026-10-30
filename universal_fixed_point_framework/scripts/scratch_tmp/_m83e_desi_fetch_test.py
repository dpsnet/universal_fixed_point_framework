# -*- coding: utf-8 -*-
"""R3e：测试下载 DESI coadd 光谱并核对 TARGETID（7110 bright）"""
import os, requests, io, sys

CACHE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_desi_spec"
os.makedirs(CACHE, exist_ok=True)
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

hp = 7110
prog = "bright"
url = ("https://data.desi.lbl.gov/public/dr1/spectro/redux/iron/healpix/main/%s/%d/%d/coadd-main-%s-%d.fits"
       % (prog, hp // 100, hp, prog, hp))
dest = os.path.join(CACHE, "coadd-main-%s-%d.fits" % (prog, hp))
if not os.path.exists(dest):
    r = requests.get(url, headers=UA, timeout=120)
    print("GET", url, "->", r.status_code, "len", len(r.content))
    if r.status_code == 200:
        with open(dest, "wb") as f:
            f.write(r.content)
        print("saved", dest, len(r.content) / 1e6, "MB")
    else:
        sys.exit(1)
else:
    print("cached", dest)

from astropy.io import fits
hdul = fits.open(dest)
print("HDUs:", [h.name for h in hdul])
hdr0 = hdul[0].header
for k in ["SURVEY", "PROGRAM", "TARGETID"]:
    pass
# coadd HDU 1: 表，列 TARGETID/TARGET_RA/TARGET_DEC/FLUX/WAVELENGTH/IVAR
t = hdul[1].data
cols = t.columns.names if hasattr(t, "columns") else list(t.dtype.names)
print("HDU1 cols:", cols)
print("rows:", len(t))
tid = t["TARGETID"][:8] if "TARGETID" in t.dtype.names else None
print("sample TARGETID:", tid)
# 查找 DESI 39632934751175691
target = 39632934751175691
if "TARGETID" in t.dtype.names:
    import numpy as np
    idx = np.where(t["TARGETID"] == target)[0]
    print("target found rows:", len(idx))
    if len(idx):
        r0 = t[idx[0]]
        print("RA/DEC:", r0["TARGET_RA"], r0["TARGET_DEC"])
