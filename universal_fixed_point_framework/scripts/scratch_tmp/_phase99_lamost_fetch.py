# -*- coding: utf-8 -*-
"""Phase 99 M99-2e：下载 LAMOST 光谱 tar 并解析 FITS，验证是否为磁场白矮星"""
import re, io, os, tarfile, json
import requests
import numpy as np

S = requests.Session()
S.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
CACHE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_lamost_spec"

def get_csrf():
    r = S.get("https://www.lamost.org/dr11/v2.0/search", timeout=30)
    m = re.search(r'name="csrf_token"\s+value="([^"]+)"', r.text)
    return m.group(1) if m else None

def download_tar(csrf, obsid):
    url = "https://www.lamost.org/dr11/v2.0/spectrum/tar?type=fits"
    r = S.post(url, data={"obsid": str(obsid), "csrf_token": csrf}, timeout=90)
    print("obsid=%s -> %d ct=%s len=%d" % (obsid, r.status_code, r.headers.get("Content-Type", ""), len(r.content)))
    if r.headers.get("Content-Type", "").startswith("application/x-tar"):
        return r.content
    print(r.content[:300].decode("utf-8", "replace"))
    return None

if __name__ == "__main__":
    os.makedirs(CACHE, exist_ok=True)
    csrf = get_csrf()
    tar_bytes = download_tar(csrf, 435606116)
    if tar_bytes:
        tf = tarfile.open(fileobj=io.BytesIO(tar_bytes))
        names = tf.getnames()
        print("tar files:", names)
        for nm in names:
            if nm.endswith((".fits", ".fits.gz")):
                f = tf.extractfile(nm)
                data = f.read()
                out = os.path.join(CACHE, os.path.basename(nm).replace(".gz", ""))
                with open(out, "wb") as fh:
                    fh.write(data)
                print("extracted", out, len(data), "bytes")
