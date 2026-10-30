# -*- coding: utf-8 -*-
"""R3a-v3：Gaia TAP 坐标重查（小 chunk 20 + 每 chunk 重试 3 次 + 5s 退避）
查询全部 137 颗（PDF 精确版 ID），覆盖 coords.json"""
import io, json, os, time

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"
with io.open(os.path.join(BASE, "paperX_wd_m83e_desi137.json"), "r", encoding="utf-8") as f:
    cat = json.load(f)
ids = [s["gaia_int"] for s in cat["samples"]]

from astroquery.gaia import Gaia
Gaia.MAIN_GAIA_TABLE = "gaiadr3.gaia_source"

coords = {}
CH = 20
for i in range(0, len(ids), CH):
    c = ids[i:i+CH]
    idlist = ",".join(str(x) for x in c)
    got = False
    for attempt in range(4):
        try:
            q = "SELECT source_id, ra, dec FROM gaiadr3.gaia_source WHERE source_id IN (%s)" % idlist
            job = Gaia.launch_job_async(q, verbose=False)
            for r in job.get_results():
                coords[str(int(r["source_id"]))] = (float(r["ra"]), float(r["dec"]))
            got = True
            break
        except Exception as e:
            print("chunk %d attempt %d fail: %s" % (i // CH, attempt, str(e)[:80]), flush=True)
            time.sleep(5 * (attempt + 1))
    print("chunk %d -> %d total" % (i // CH, len(coords)), flush=True)
    time.sleep(2)

print("hit:", len(coords), "/", len(ids))
with io.open(os.path.join(BASE, "paperX_wd_m83e_desi137_coords.json"), "w", encoding="utf-8") as f:
    json.dump({"n": len(coords), "coords": coords}, f, ensure_ascii=False)
print("saved coords v3")
