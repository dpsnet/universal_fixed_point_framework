# -*- coding: utf-8 -*-
"""Phase 99 M99-2d：试探 LAMOST 光谱 tar 下载端点参数格式"""
import re
import requests

S = requests.Session()
S.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})

def get_csrf():
    r = S.get("https://www.lamost.org/dr11/v2.0/search", timeout=30)
    m = re.search(r'name="csrf_token"\s+value="([^"]+)"', r.text)
    return m.group(1) if m else None

def try_download(csrf, obsid):
    base = "https://www.lamost.org/dr11/v2.0/spectrum/tar"
    variants = [
        (base + "?type=fits", {"obsids": str(obsid), "csrf_token": csrf}),
        (base + "?type=fits", {"obsid": str(obsid), "csrf_token": csrf}),
        (base + "?type=fits.gz", {"obsids": str(obsid), "csrf_token": csrf}),
        (base + "?fits=gz", {"obsids": str(obsid), "csrf_token": csrf}),
        (base, {"obsids": str(obsid), "csrf_token": csrf}),
    ]
    for url, data in variants:
        try:
            r = S.post(url, data=data, timeout=40)
            ct = r.headers.get("Content-Type", "")
            print("POST %s data=%s -> %d ct=%s len=%d head=%s" % (
                url.split("?")[0] + ("?" + url.split("?")[1] if "?" in url else ""),
                list(data.keys()), r.status_code, ct, len(r.content),
                r.content[:60].decode("utf-8", "replace").replace("\n", " ")))
        except Exception as e:
            print("ERR", url, str(e)[:80])

if __name__ == "__main__":
    csrf = get_csrf()
    try_download(csrf, 435606116)
