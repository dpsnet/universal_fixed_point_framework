# -*- coding: utf-8 -*-
"""Phase 86 R1：Gaia DR3 视差/测光批量获取（137 颗 DESI 星）-> scripts/_gaia_abs/gaia_parallax_phot.json"""
import json, io, os, time
import numpy as np

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"
OUT = os.path.join(BASE, "_gaia_abs")
os.makedirs(OUT, exist_ok=True)

with io.open(os.path.join(BASE, "paperX_wd_m83e_desi137.json"), "r", encoding="utf-8") as f:
    cat = json.load(f)["samples"]
ids = [s["gaia_id"] for s in cat]
print("总星数:", len(ids))

from astroquery.gaia import Gaia
Gaia.TIMEOUT = 60

COLS = "source_id, parallax, parallax_error, phot_g_mean_mag, phot_bp_mean_mag, phot_rp_mean_mag, phot_bp_rp_excess_factor, pmra, pmdec, ruwe"

rows = {}
missing = []
t0 = time.time()
for i in range(0, len(ids), 60):
    chunk = ids[i:i + 60]
    q = "SELECT %s FROM gaiadr3.gaia_source WHERE source_id IN (%s)" % (COLS, ",".join(str(x) for x in chunk))
    try:
        res = Gaia.launch_job(q).get_results()
        for r in res:
            sid = int(r["source_id"])
            rows[sid] = {
                "parallax": float(r["parallax"]) if r["parallax"] is not None else None,
                "parallax_error": float(r["parallax_error"]) if r["parallax_error"] is not None else None,
                "g_mag": float(r["phot_g_mean_mag"]) if r["phot_g_mean_mag"] is not None else None,
                "bp_mag": float(r["phot_bp_mean_mag"]) if r["phot_bp_mean_mag"] is not None else None,
                "rp_mag": float(r["phot_rp_mean_mag"]) if r["phot_rp_mean_mag"] is not None else None,
                "bp_rp_excess": float(r["phot_bp_rp_excess_factor"]) if r["phot_bp_rp_excess_factor"] is not None else None,
                "ruwe": float(r["ruwe"]) if r["ruwe"] is not None else None,
            }
    except Exception as e:
        print("chunk %d fail: %s" % (i, str(e)[:200]))
        for x in chunk:
            missing.append(x)
    print("批 %d/%d 完成，已取 %d，用时 %.0fs" % (i // 60 + 1, (len(ids) - 1) // 60 + 1, len(rows), time.time() - t0))

not_found = [x for x in ids if x not in rows]
print("命中 %d/%d，未命中 %d" % (len(rows), len(ids), len(not_found)))
if not_found:
    print("未命中:", not_found[:10])

# 视差质量统计
pars = [v["parallax"] for v in rows.values() if v["parallax"]]
perr = [v["parallax_error"] for v in rows.values() if v["parallax_error"]]
if pars:
    print("视差 med=%.3f mas (%.0f pc)，parallax_error med=%.3f mas" % (
        float(np.median(pars)), 1000.0 / float(np.median(pars)), float(np.median(perr))))
    snr = [p / e for p, e in zip(pars, perr) if e and e > 0]
    print("S/N>10 占比: %.1f%%" % (100.0 * sum(1 for s in snr if s > 10) / len(snr)))

out = {"n_requested": len(ids), "n_matched": len(rows), "rows": {str(k): v for k, v in rows.items()}}
with io.open(os.path.join(OUT, "gaia_parallax_phot.json"), "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("written:", os.path.join(OUT, "gaia_parallax_phot.json"))
