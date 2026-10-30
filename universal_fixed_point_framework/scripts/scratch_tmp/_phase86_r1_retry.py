# -*- coding: utf-8 -*-
"""Phase 86 R1 补查：真实未命中的星（str/int 归一化）"""
import json, io, os, time
import numpy as np

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"
OUT = os.path.join(BASE, "_gaia_abs")
with io.open(os.path.join(OUT, "gaia_parallax_phot.json"), "r", encoding="utf-8") as f:
    data = json.load(f)
rows = {int(k): v for k, v in data["rows"].items()}
with io.open(os.path.join(BASE, "paperX_wd_m83e_desi137.json"), "r", encoding="utf-8") as f:
    cat = json.load(f)["samples"]
ids = [int(s["gaia_id"]) for s in cat]
missing = [x for x in ids if x not in rows]
print("真实未命中:", len(missing), missing)

from astroquery.gaia import Gaia
Gaia.TIMEOUT = 60
COLS = "source_id, parallax, parallax_error, phot_g_mean_mag, phot_bp_mean_mag, phot_rp_mean_mag, phot_bp_rp_excess_factor, pmra, pmdec, ruwe"
t0 = time.time()
for i in range(0, len(missing), 60):
    chunk = missing[i:i + 60]
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
        print("chunk fail:", str(e)[:200])
    print("补查 %d/%d，累计 %d，用时 %.0fs" % (i // 60 + 1, (len(missing) - 1) // 60 + 1, len(rows), time.time() - t0))

still = [x for x in ids if x not in rows]
print("最终命中 %d/%d，仍缺 %d" % (len(rows), len(ids), len(still)))
if still:
    print("仍缺:", still)

out = {"n_requested": len(ids), "n_matched": len(rows), "rows": {str(k): v for k, v in rows.items()}}
with io.open(os.path.join(OUT, "gaia_parallax_phot.json"), "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("written:", os.path.join(OUT, "gaia_parallax_phot.json"))
