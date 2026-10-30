# -*- coding: utf-8 -*-
"""R3b：114 颗命中星 → DESI healpix（nside=64 nested）→ 探测光谱文件"""
import io, json, os
import numpy as np
import astropy.units as u
from astropy_healpix import HEALPix

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"
with io.open(os.path.join(BASE, "paperX_wd_m83e_desi137_coords.json"), "r", encoding="utf-8") as f:
    co = json.load(f)["coords"]

hp = HEALPix(nside=64, order="nested")
out = {}
for k, (ra, dec) in co.items():
    ipix = hp.lonlat_to_healpix(u.Quantity(float(ra), u.deg), u.Quantity(float(dec), u.deg))
    out[k] = int(ipix)
print("healpix computed for", len(out), "stars; unique hp:", len(set(out.values())))
with io.open(os.path.join(BASE, "paperX_wd_m83e_desi137_hp.json"), "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False)
# 打印前几个 hp 供探测
from collections import Counter
cnt = Counter(out.values())
print("top hp:", cnt.most_common(8))
