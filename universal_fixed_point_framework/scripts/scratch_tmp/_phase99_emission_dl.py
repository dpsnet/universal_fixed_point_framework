# -*- coding: utf-8 -*-
"""Phase 99 延伸-3：下载 3 颗发射线星的 LAMOST 光谱并检测 Balmer 发射"""
import re, io, os, tarfile, gzip
import numpy as np
import requests
from astropy.io import fits

SPEC = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_lamost_spec"
os.makedirs(SPEC, exist_ok=True)
S = requests.Session()
S.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})

OBSIDS = ["355002136", "371716152", "361515161", "371715172",
          "307601149", "491912228", "563812228"]

r = S.get("https://www.lamost.org/dr11/v2.0/search", timeout=30)
m = re.search(r'name="csrf_token"\s+value="([^"]+)"', r.text)
csrf = m.group(1) if m else None

# 分批下载
for i in range(0, len(OBSIDS), 5):
    chunk = OBSIDS[i:i + 5]
    r2 = S.post("https://www.lamost.org/dr11/v2.0/spectrum/tar?type=fits",
                data={"obsid": ",".join(chunk), "csrf_token": csrf}, timeout=120)
    print("batch", chunk, "->", r2.status_code, r2.headers.get("Content-Type", ""), len(r2.content))
    if r2.headers.get("Content-Type", "").startswith("application/x-tar"):
        tf = tarfile.open(fileobj=io.BytesIO(r2.content))
        for nm in tf.getnames():
            if nm.endswith(".fits.gz"):
                base = os.path.basename(nm).replace(".fits.gz", "")
                data = tf.extractfile(nm).read()
                raw = gzip.decompress(data)
                with open(os.path.join(SPEC, base + ".fits"), "wb") as fh:
                    fh.write(raw)
                print("  saved", base + ".fits")

# 检测 Balmer 发射：Hbeta/Hgamma/Hdelta 线上方凸起（中值>1.15 且>基线）
print("\n== Balmer 发射检测（凸起 >1.15 为发射特征）==")
BALMER = {"Hbeta": 4861.3, "Hgamma": 4340.5, "Hdelta": 4101.7}
import glob
for f in sorted(glob.glob(os.path.join(SPEC, "*.fits"))):
    base = os.path.basename(f).replace(".fits", "")
    mj = re.search(r"spec-(\d+)-(.*)_sp(\d+)-(\d+)", base)
    if not mj:
        continue
    try:
        hdul = fits.open(f)
        d = hdul[1].data
        wl = np.array(d["WAVELENGTH"]).ravel()
        fl = np.array(d["FLUX"]).ravel()
        hdul.close()
        good = np.isfinite(fl) & (fl > 0)
        fl[~good] = np.nan
        mc = ((wl > 4500) & (wl < 4700)) | ((wl > 5100) & (wl < 5400))
        med = np.nanmedian(fl[mc])
        if not np.isfinite(med) or med <= 0:
            continue
        fl = fl / med
        feats = []
        for lab, c in BALMER.items():
            win = (wl > c - 6) & (wl < c + 6)
            basew = ((wl > c - 15) & (wl < c - 6)) | ((wl > c + 6) & (wl < c + 15))
            if win.sum() > 2 and basew.sum() > 4:
                pk = np.nanmedian(fl[win])
                bg = np.nanmedian(fl[basew])
                feats.append("%s pk=%.2f bg=%.2f %s" % (lab, pk, bg, "EMISSION" if pk > 1.15 and pk > bg else ("ABS" if pk < 0.95 else "flat")))
        if feats:
            print(base, " | ".join(feats))
    except Exception as e:
        print(base, "ERR", str(e)[:60])
