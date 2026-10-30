# -*- coding: utf-8 -*-
"""Phase 99 M99-3a：修正坐标（×15 + 正确切片）后全量交叉匹配
对 142 中场 + 99 弱场，cone 120 arcsec 查询 LAMOST DR11
输出 paperX_lamost_crossmatch_fixed.json
"""
import json, io, time, re
import numpy as np
import requests

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_gaia_abs"
S = requests.Session()
S.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})

def parse_jname(name):
    ra_s = name[1:10]
    dec_s = name[10:19]
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

COLS = ["combined.obsid", "combined.obsdate", "combined.planid", "combined.spid",
        "combined.fiberid", "combined.class", "combined.z", "combined.ra", "combined.dec",
        "combined.snrg", "combined.snrr"]

def query_cone(csrf, ra, dec, radius=120):
    data = {
        "csrf_token": csrf, "pos_group": "ra,dec", "pos.type": "cone",
        "pos.racenter": "%.7f" % ra, "pos.deccenter": "%.7f" % dec,
        "pos.radius": str(radius), "output.fmt": "csv", "showcol": COLS,
    }
    try:
        r = S.post("https://www.lamost.org/dr11/v2.0/table/combined/q", data=data, timeout=45)
        txt = r.text
        if r.status_code != 200:
            return None
        lines = [l for l in txt.strip().splitlines() if l.strip()]
        if len(lines) < 2:
            return None
        hdr = [h.strip() for h in lines[0].replace("\ufeff", "").split(",")]
        rows = []
        for ln in lines[1:]:
            vals = ln.split(",")
            rows.append(dict(zip(hdr, vals)))
        return rows
    except Exception as e:
        return None

def main():
    mid = json.load(open(BASE + r"\paperX_wd_linelevel_mid_full_snr.json", encoding="utf-8"))["mid_full"]
    wk = json.load(open(BASE + r"\paperX_wd_linelevel_weak_sdss_snr.json", encoding="utf-8"))["weak_sdss"]
    csrf = get_csrf()
    out = {"mid": [], "weak": []}
    for grp, key in ((mid, "mid"), (wk, "weak")):
        for s in grp:
            ra, dec = parse_jname(s["name"])
            rows = query_cone(csrf, ra, dec, 120)
            rec = {"name": s["name"], "B_MG": s["B_MG"], "ra": ra, "dec": dec, "lamost": rows}
            out[key].append(rec)
            if rows:
                r0 = rows[0]
                print("[%s] %s B=%.1f -> LAMOST %d 条 snrr=%.1f class=%s dist0=%s" % (
                    key, s["name"], s["B_MG"], len(rows),
                    float(r0.get("snrr", 0) or 0), r0.get("class", "?"), r0.get("dist_arcsec", "?")), flush=True)
            else:
                print("[%s] %s B=%.1f -> 无命中" % (key, s["name"], s["B_MG"]), flush=True)
            time.sleep(0.15)
    json.dump(out, io.open(BASE + r"\paperX_lamost_crossmatch_fixed.json", "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    for key in ("mid", "weak"):
        grp = out[key]
        hit = [g for g in grp if g["lamost"]]
        snrs = [float(g["lamost"][0]["snrr"]) for g in hit if g["lamost"][0].get("snrr")]
        print("%s: 命中 %d/%d, snrr 中位 %.1f (P25 %.1f P75 %.1f)" % (
            key, len(hit), len(grp), np.median(snrs) if snrs else 0,
            np.percentile(snrs, 25) if snrs else 0, np.percentile(snrs, 75) if snrs else 0), flush=True)
    print("written paperX_lamost_crossmatch_fixed.json")

if __name__ == "__main__":
    main()
