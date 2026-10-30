# -*- coding: utf-8 -*-
"""R1-fix4：用 PDF 精确版重建 desi137 目录 + Gaia TAP 重查全部坐标"""
import fitz, io, json, os, re

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"
with io.open(os.path.join(BASE, "_m83e_pdf_table1.json"), "r", encoding="utf-8") as f:
    tbl = json.load(f)["rows"]

samples = []
for r in tbl:
    gaia_id = r[0]
    samples.append({
        "gaia_id": gaia_id,
        "gaia_int": int(gaia_id),
        "desi_name": r[1],
        "Teff": float(r[2]),
        "Mass": float(r[3]),
        "B_MG": float(r[4]),
        "zoffset": None if r[5] == "NA" else float(r[5]),
        "Incl": None if r[6] == "NA" else float(r[6]),
        "tau_Gyr": float(r[7]),
        "G_mag": float(r[8]),
        "logg": 8.0,
        "src": "desi137_pdf",
    })
print("samples:", len(samples))
# B 分档统计
b = [s["B_MG"] for s in samples]
print("B<10:", sum(1 for x in b if x < 10), "10-100:", sum(1 for x in b if 10 <= x < 100), ">=100:", sum(1 for x in b if x >= 100))

with io.open(os.path.join(BASE, "paperX_wd_m83e_desi137.json"), "w", encoding="utf-8") as f:
    json.dump({"samples": samples, "note": "PDF 精确版（修正 WebFetch 转录错位）"}, f, ensure_ascii=False)
print("saved desi137 v2")

# Gaia TAP 重查全部坐标
from astroquery.gaia import Gaia
Gaia.MAIN_GAIA_TABLE = "gaiadr3.gaia_source"
ids = [s["gaia_int"] for s in samples]
coords = {}
for i in range(0, len(ids), 50):
    c = ids[i:i+50]
    idlist = ",".join(str(x) for x in c)
    q = "SELECT source_id, ra, dec FROM gaiadr3.gaia_source WHERE source_id IN (%s)" % idlist
    try:
        job = Gaia.launch_job_async(q, verbose=False)
        for r in job.get_results():
            coords[str(int(r["source_id"]))] = (float(r["ra"]), float(r["dec"]))
    except Exception as e:
        print("chunk fail", str(e)[:100])
    print("progress", len(coords), "/", len(ids))
print("hit:", len(coords))
with io.open(os.path.join(BASE, "paperX_wd_m83e_desi137_coords.json"), "w", encoding="utf-8") as f:
    json.dump({"n": len(coords), "coords": coords}, f, ensure_ascii=False)
print("saved coords v2")
