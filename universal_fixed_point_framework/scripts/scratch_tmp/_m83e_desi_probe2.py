# -*- coding: utf-8 -*-
"""R3d：探测 DESI healpix 目录（bright/dark），确认光谱文件名"""
import requests

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
for prog in ["bright", "dark"]:
    url = "https://data.desi.lbl.gov/public/dr1/spectro/redux/iron/healpix/main/%s/71/7110/" % prog
    try:
        r = requests.get(url, headers=UA, timeout=30)
        print(url, "->", r.status_code, "len", len(r.content))
        if r.status_code == 200:
            # 提取文件名链接
            import re
            names = re.findall(r'href="([^"]+)"', r.text)
            fits = [n for n in names if n.endswith(".fits")][:12]
            print("  fits:", fits)
    except Exception as e:
        print(url, "ERR", str(e)[:100])
