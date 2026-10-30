# -*- coding: utf-8 -*-
"""Phase 99 M99-2b：修正坐标解析（×15）后 cone 查询验证
J121635.36-002656.3 -> RA=184.1473° Dec=-0.44897°
"""
import re
import requests

S = requests.Session()
S.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})

def parse_jname(name):
    """JHHMMSS.ss±DDMMSS.s -> (ra_deg, dec_deg)  固定格式：J + RA(9) + DEC(9)"""
    ra_s = name[1:10]    # "HHMMSS.ss"
    dec_s = name[10:19]  # "±DDMMSS.s"
    hh, mm, ss = int(ra_s[0:2]), int(ra_s[2:4]), float(ra_s[4:])
    ra = (hh + mm / 60 + ss / 3600) * 15.0
    sign = -1 if dec_s[0] == "-" else 1
    dd, dm, ds = int(dec_s[1:3]), int(dec_s[3:5]), float(dec_s[5:])
    dec = sign * (dd + dm / 60 + ds / 3600)
    return ra, dec

def get_csrf():
    r = S.get("https://www.lamost.org/dr11/v2.0/search", timeout=30)
    m = re.search(r'name="csrf_token"\s+value="([^"]+)"', r.text)
    return m.group(1) if m else None

def query_cone(csrf, ra, dec, radius_arcsec=120, pos_group="ra,dec", cols=None):
    if cols is None:
        cols = ["combined.obsid", "combined.uid", "combined.obsdate", "combined.planid",
                "combined.spid", "combined.fiberid", "combined.class", "combined.subclass",
                "combined.z", "combined.ra", "combined.dec", "combined.snrg", "combined.snrr"]
    data = {
        "csrf_token": csrf, "pos_group": pos_group, "pos.type": "cone",
        "pos.racenter": str(ra), "pos.deccenter": str(dec), "pos.radius": str(radius_arcsec),
        "output.fmt": "csv", "showcol": cols,
    }
    r = S.post("https://www.lamost.org/dr11/v2.0/table/combined/q", data=data, timeout=60)
    return r

if __name__ == "__main__":
    csrf = get_csrf()
    ra, dec = parse_jname("J121635.36-002656.3")
    print("parsed RA=%.4f Dec=%.6f" % (ra, dec))
    for pg in ("ra,dec", "ra_obs,dec_obs"):
        r = query_cone(csrf, ra, dec, 120, pg)
        print("--- pos_group=%s status=%d len=%d ---" % (pg, r.status_code, len(r.text)))
        print(r.text[:600])
