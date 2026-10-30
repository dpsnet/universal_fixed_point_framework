# -*- coding: utf-8 -*-
"""R3a-2：对 23 颗未命中 Gaia ID 逐一单查（排查批量 IN 子句是否被截断/拒绝）"""
import io, json, os

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"
with io.open(os.path.join(BASE, "paperX_wd_m83e_desi137.json"), "r", encoding="utf-8") as f:
    cat = json.load(f)
with io.open(os.path.join(BASE, "paperX_wd_m83e_desi137_coords.json"), "r", encoding="utf-8") as f:
    co = json.load(f)["coords"]

miss = [s for s in cat["samples"] if str(s["gaia_int"]) not in co]
print("重查 %d 颗" % len(miss))

from astroquery.gaia import Gaia
Gaia.MAIN_GAIA_TABLE = "gaiadr3.gaia_source"
found = {}
for s in miss:
    gid = s["gaia_int"]
    q = "SELECT source_id, ra, dec FROM gaiadr3.gaia_source WHERE source_id = %d" % gid
    try:
        job = Gaia.launch_job_async(q, verbose=False)
        tab = job.get_results()
        n = len(tab)
        if n:
            r = tab[0]
            found[str(gid)] = (float(r["ra"]), float(r["dec"]))
            print("FOUND %s (B=%.1f) ra=%.5f dec=%.5f" % (s["gaia_id"], s["B_MG"], float(r["ra"]), float(r["dec"])))
        else:
            print("EMPTY %s (B=%.1f)" % (s["gaia_id"], s["B_MG"]))
    except Exception as e:
        print("ERR %s %s" % (s["gaia_id"], str(e)[:100]))

print("新命中 %d 颗" % len(found))
if found:
    co.update(found)
    with io.open(os.path.join(BASE, "paperX_wd_m83e_desi137_coords.json"), "w", encoding="utf-8") as f:
        json.dump({"n": len(co), "coords": co}, f, ensure_ascii=False)
    print("coords updated ->", len(co))
