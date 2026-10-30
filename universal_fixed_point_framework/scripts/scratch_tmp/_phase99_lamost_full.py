# -*- coding: utf-8 -*-
"""Phase 99 M99-1b：LAMOST DR11 (V/162) 全量交叉匹配（142 中场 + 99 弱场）
评估命中率 + SNR 分布（snrr 等 5 波段）——判断是否满足 SNR 匹配目标
"""
import json, io, time
import numpy as np
from astroquery.vizier import Vizier
from astropy.coordinates import SkyCoord
import astropy.units as u

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_gaia_abs"

def parse_jname(name):
    ra_s, dec_s = name[1:9], name[9:18]
    ra = float(ra_s[0:2]) + float(ra_s[2:4]) / 60 + float(ra_s[4:]) / 3600
    sign = -1 if dec_s[0] == "-" else 1
    dd = float(dec_s[1:3]) + float(dec_s[3:5]) / 60 + float(dec_s[5:]) / 3600
    return ra * 15.0 if False else ra, sign * dd  # J-name RA 已是度

def query_one(v, s):
    ra, dec = parse_jname(s["name"])
    c = SkyCoord(ra * u.deg, dec * u.deg)
    try:
        r = v.query_region(c, radius=2.0 * u.arcmin, catalog="V/162")
        tbl = r[0]
        best = None
        for row in tbl:
            snrr = float(row["snrr"]) if row["snrr"] is not None and not np.isnan(row["snrr"]) else None
            if best is None or (snrr is not None and (best[1] is None or snrr > best[1])):
                best = (str(row["ObsID"]), snrr, str(row["sp"]))
        return {"name": s["name"], "B_MG": s["B_MG"], "n_hit": len(tbl),
                "obsid": best[0] if best else None,
                "snrr": best[1] if best else None, "sp": best[2] if best else None}
    except Exception:
        return {"name": s["name"], "B_MG": s["B_MG"], "n_hit": 0, "obsid": None,
                "snrr": None, "sp": None}

def main():
    mid = json.load(open(BASE + r"\paperX_wd_linelevel_mid_full_snr.json", encoding="utf-8"))["mid_full"]
    wk = json.load(open(BASE + r"\paperX_wd_linelevel_weak_sdss_snr.json", encoding="utf-8"))["weak_sdss"]
    v = Vizier(row_limit=50, columns=["ObsID", "sp", "snrr", "RAJ2000", "DEJ2000"])
    out = {"mid": [], "weak": []}
    for grp, key in ((mid, "mid"), (wk, "weak")):
        for s in grp:
            r = query_one(v, s)
            out[key].append(r)
            print("  [%s] %s B=%.1f n_hit=%d snrr=%s" % (
                key, r["name"], r["B_MG"], r["n_hit"],
                "%.1f" % r["snrr"] if r["snrr"] is not None else "None"), flush=True)
            time.sleep(0.15)
    json.dump(out, io.open(BASE + r"\paperX_lamost_crossmatch_full.json", "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    for key in ("mid", "weak"):
        grp = out[key]
        nh = sum(1 for r in grp if r["snrr"])
        snrs = [r["snrr"] for r in grp if r["snrr"]]
        print("%s: 命中 %d/%d, snrr 中位=%.1f (P25=%.1f P75=%.1f)" % (
            key, nh, len(grp), np.median(snrs) if snrs else 0,
            np.percentile(snrs, 25) if snrs else 0, np.percentile(snrs, 75) if snrs else 0), flush=True)
    print("written paperX_lamost_crossmatch_full.json")

if __name__ == "__main__":
    main()
