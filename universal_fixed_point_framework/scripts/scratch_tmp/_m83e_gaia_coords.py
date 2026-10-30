# -*- coding: utf-8 -*-
"""R3a：DESI 137 颗 Gaia DR3 source_id → RA/DEC（Gaia TAP 查询）→ 保存坐标"""
import io, json, os, sys

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"
with io.open(os.path.join(BASE, "paperX_wd_m83e_desi137.json"), "r", encoding="utf-8") as f:
    cat = json.load(f)

ids = [int(s["gaia_int"]) for s in cat["samples"] if s.get("gaia_int") is not None]
print("查询 %d 颗 Gaia ID" % len(ids))

from astroquery.gaia import Gaia
Gaia.MAIN_GAIA_TABLE = "gaiadr3.gaia_source"
chunk = 60
coords = {}
for i in range(0, len(ids), chunk):
    c = ids[i:i+chunk]
    idlist = ",".join(str(x) for x in c)
    q = "SELECT source_id, ra, dec FROM gaiadr3.gaia_source WHERE source_id IN (%s)" % idlist
    try:
        job = Gaia.launch_job_async(q, verbose=False)
        tab = job.get_results()
        for r in tab:
            coords[str(int(r["source_id"]))] = (float(r["ra"]), float(r["dec"]))
    except Exception as e:
        print("chunk %d FAIL %s" % (i, str(e)[:150]))
    print("progress %d/%d -> %d" % (i + len(c), len(ids), len(coords)))

print("命中 %d 颗" % len(coords))
out = {"n": len(coords), "coords": coords}
with io.open(os.path.join(BASE, "paperX_wd_m83e_desi137_coords.json"), "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False)
print("saved coords json")
