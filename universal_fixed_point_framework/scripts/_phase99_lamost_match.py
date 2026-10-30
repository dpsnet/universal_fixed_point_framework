# -*- coding: utf-8 -*-
"""Phase 99 M99-1：LAMOST DR11 (V/162) 交叉匹配试点
20 颗中场星 cone search（radius=2'），评估命中率与 SNR 分布
"""
import json, io, sys, time
import numpy as np
from astroquery.vizier import Vizier
from astropy.coordinates import SkyCoord
import astropy.units as u

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_gaia_abs"
mid = json.load(open(BASE + r"\paperX_wd_linelevel_mid_full_snr.json", encoding="utf-8"))["mid_full"]

# 取 20 颗（覆盖 10-100 MG 域）
sample = mid[::7][:20] + mid[1::7][:2] if len(mid) > 20 else mid[:20]
sample = sample[:20]
print("试点 %d 颗中场星（B %.0f-%.0f MG）" % (len(sample), min(s["B_MG"] for s in sample), max(s["B_MG"] for s in sample)), flush=True)

v = Vizier(row_limit=1, columns=["*"])
hits = []
for s in sample:
    # 从 J 名称解析坐标（JHHMMSS.ss+DDMMSS.s）
    name = s["name"]
    ra_s, dec_s = name[1:9], name[9:18]
    ra = float(ra_s[0:2]) + float(ra_s[2:4]) / 60 + float(ra_s[4:]) / 3600
    sign = -1 if dec_s[0] == "-" else 1
    dd = float(dec_s[1:3]) + float(dec_s[3:5]) / 60 + float(dec_s[5:]) / 3600
    dec = sign * dd
    c = SkyCoord(ra * u.deg, dec * u.deg)
    try:
        tbl = v.query_region(c, radius=2.0 * u.arcmin, catalog="V/162")[0]
        n_hit = len(tbl)
        snrs = []
        names = []
        if n_hit > 0:
            for row in tbl:
                snr = None
                for col in ("SNR", "s2n", "SNr"):
                    if col in row.colnames:
                        try:
                            snr = float(row[col])
                        except Exception:
                            snr = None
                        break
                if snr is not None:
                    snrs.append(snr)
                names.append(str(row[0]) if len(row) > 0 else "?")
        hits.append({"name": s["name"], "B_MG": s["B_MG"], "n_hit": n_hit,
                     "snr_max": max(snrs) if snrs else None, "ids": names[:3]})
        print("  %s B=%.0f MG -> LAMOST 命中 %d (SNRmax=%s)" % (
            s["name"], s["B_MG"], n_hit,
            ("%.1f" % max(snrs)) if snrs else "None"), flush=True)
    except Exception as e:
        print("  %s ERR %s" % (s["name"], str(e)[:60]), flush=True)
    time.sleep(0.3)

nh = sum(1 for h in hits if h["n_hit"] > 0)
print("命中率: %d/%d (%.0f%%)" % (nh, len(hits), 100.0 * nh / len(hits)), flush=True)
snrs = [h["snr_max"] for h in hits if h["snr_max"]]
print("命中星 SNRmax 中位=%.1f" % (np.median(snrs) if snrs else 0), flush=True)
json.dump(hits, io.open(BASE + r"\paperX_lamost_crossmatch_pilot.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print("written paperX_lamost_crossmatch_pilot.json")
