# -*- coding: utf-8 -*-
"""Phase 99 M99-2a：LAMOST DR11 官网查询通道验证（Python requests 直连）
验证：GET search 页取 csrf_token -> POST /table/combined/q 按 obsid 查询
"""
import re, json, io, sys
import requests

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_gaia_abs"
S = requests.Session()
S.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})

def get_csrf():
    r = S.get("https://www.lamost.org/dr11/v2.0/search", timeout=30)
    m = re.search(r'name="csrf_token"\s+value="([^"]+)"', r.text)
    if not m:
        m = re.search(r'name="csrf_token"[^>]*value="([^"]+)"', r.text)
    print("GET search:", r.status_code, "len", len(r.text), "csrf:", bool(m))
    return m.group(1) if m else None

def query_obsid(csrf, obsid, cols=None):
    if cols is None:
        cols = ["combined.obsid", "combined.uid", "combined.obsdate", "combined.lmjd",
                "combined.mjd", "combined.planid", "combined.spid", "combined.fiberid",
                "combined.class", "combined.subclass", "combined.z", "combined.ra",
                "combined.dec", "combined.rv", "combined.logg", "combined.teff", "combined.feh",
                "combined.snrg", "combined.snrr"]
    data = {
        "csrf_token": csrf,
        "pos_group": "ra,dec",
        "pos.type": "none",
        "output.fmt": "csv",
        "combined.obsid.constraint": str(obsid),
        "combined.obsid.operation": "==",
        "showcol": cols,  # requests 列表 -> 多值
    }
    r = S.post("https://www.lamost.org/dr11/v2.0/table/combined/q", data=data, timeout=60)
    print("POST obsid=%s:" % obsid, r.status_code, "len", len(r.text))
    print(r.text[:1000])
    return r.text

if __name__ == "__main__":
    csrf = get_csrf()
    if csrf:
        query_obsid(csrf, 604714061)
