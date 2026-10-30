# -*- coding: utf-8 -*-
"""R3g：测试 data.desi.lbl.gov HTTP Range 支持（FITS 列按需读取可行性）"""
import requests

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
url = "https://data.desi.lbl.gov/public/dr1/spectro/redux/iron/healpix/main/bright/71/7110/coadd-main-bright-7110.fits"
r = requests.get(url, headers=dict(UA, Range="bytes=0-2047"), timeout=30)
print("status", r.status_code, "content-range:", r.headers.get("Content-Range"), "len", len(r.content))
print("Accept-Ranges:", r.headers.get("Accept-Ranges"))
if r.status_code == 206:
    print("RANGE OK -> 可行：列式按需读取")
else:
    print("RANGE NOT SUPPORTED -> 需全量下载或另寻通道")
