# -*- coding: utf-8 -*-
"""Phase 99 M99-2c：找 LAMOST 光谱 FITS 下载 URL（html 输出格式含链接）"""
import re
import requests

S = requests.Session()
S.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})

def get_csrf():
    r = S.get("https://www.lamost.org/dr11/v2.0/search", timeout=30)
    m = re.search(r'name="csrf_token"\s+value="([^"]+)"', r.text)
    return m.group(1) if m else None

def query_html(csrf, obsid):
    data = {
        "csrf_token": csrf, "pos_group": "ra,dec", "pos.type": "none",
        "output.fmt": "html",
        "combined.obsid.constraint": str(obsid), "combined.obsid.operation": "==",
        "showcol": ["combined.obsid", "combined.uid", "combined.obsdate", "combined.planid",
                    "combined.spid", "combined.fiberid", "combined.snrg", "combined.snrr"],
    }
    r = S.post("https://www.lamost.org/dr11/v2.0/table/combined/q", data=data, timeout=60)
    print("status", r.status_code, "len", len(r.text))
    return r.text

if __name__ == "__main__":
    csrf = get_csrf()
    html = query_html(csrf, 435606116)
    # 找链接/下载相关
    links = re.findall(r'href="([^"]+)"', html)
    print("LINKS:", links[:30])
    for pat in ("fits", "spectrum", "download", "tar"):
        for m in re.finditer(pat, html):
            s = max(0, m.start() - 120)
            print("...", html[s:m.start() + 150].replace("\n", " "))
            break
