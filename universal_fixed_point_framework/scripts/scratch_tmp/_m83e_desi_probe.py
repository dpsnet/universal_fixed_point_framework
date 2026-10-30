# -*- coding: utf-8 -*-
"""R3c：探测 DESI 光谱目录结构（requests 直连）"""
import requests, sys

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) research"}
for url in [
    "https://data.desi.lbl.gov/public/dr1/spectra/healpix/main/coadd/7110/",
    "https://data.desi.lbl.gov/public/dr1/spectra/healpix/main/coadd/7110/coadd-7110-20210501.fits",
]:
    try:
        r = requests.get(url, headers=UA, timeout=30)
        print(url, "->", r.status_code, "len", len(r.content))
        if r.status_code == 200 and len(r.content) < 100000:
            print(r.text[:500])
    except Exception as e:
        print(url, "ERR", str(e)[:120])
