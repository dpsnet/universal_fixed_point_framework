# -*- coding: utf-8 -*-
"""Phase 99 M99-3b：测批量光谱 tar 下载（逗号分隔 obsid）"""
import re, io, os, tarfile
import requests

S = requests.Session()
S.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})

def get_csrf():
    r = S.get("https://www.lamost.org/dr11/v2.0/search", timeout=30)
    m = re.search(r'name="csrf_token"\s+value="([^"]+)"', r.text)
    return m.group(1) if m else None

if __name__ == "__main__":
    csrf = get_csrf()
    obsids = "435606116,200606145,199806145"
    for fmt in ("fits", "fits.gz"):
        url = "https://www.lamost.org/dr11/v2.0/spectrum/tar?type=%s" % fmt
        r = S.post(url, data={"obsid": obsids, "csrf_token": csrf}, timeout=90)
        ct = r.headers.get("Content-Type", "")
        print("type=%s -> %d ct=%s len=%d" % (fmt, r.status_code, ct, len(r.content)))
        if ct.startswith("application/x-tar") and len(r.content) > 5000:
            tf = tarfile.open(fileobj=io.BytesIO(r.content))
            print("  tar 内文件:", tf.getnames()[:10])
            break
        else:
            print("  ", r.content[:200].decode("utf-8", "replace"))
