# -*- coding: utf-8 -*-
"""Phase 86 R1 探测：Gaia DR3 数据源可达性 + 3 颗星试查询"""
import json, io, sys, time
import numpy as np

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"
with io.open(BASE + r"\paperX_wd_m83e_desi137.json", "r", encoding="utf-8") as f:
    cat = json.load(f)["samples"]
ids = [s["gaia_id"] for s in cat[:3]]
print("测试 source_id:", ids)

# 路径 1：astroquery Gaia TAP
try:
    from astroquery.gaia import Gaia
    Gaia.TIMEOUT = 30
    q = "SELECT source_id, parallax, parallax_error, phot_g_mean_mag, phot_bp_mean_mag, phot_rp_mean_mag FROM gaiadr3.gaia_source WHERE source_id IN (%s)" % ",".join(str(i) for i in ids)
    t0 = time.time()
    res = Gaia.launch_job(q).get_results()
    print("[TAP] OK n=%d dt=%.1fs" % (len(res), time.time() - t0))
    print(res)
except Exception as e:
    print("[TAP] FAIL:", type(e).__name__, str(e)[:300])

# 路径 2：Vizier I/355/gaiadr3（web 查询）
try:
    from astroquery.vizier import Vizier
    Vizier.TIMEOUT = 30
    v = Vizier(columns=["source_id", "Plx", "e_Plx", "Gmag", "BPmag", "RPmag", "BPRP", "e_BPRP"], row_limit=10)
    t0 = time.time()
    tbl = v.query_region("", catalog="I/355/gaiadr3", ucd="(POS_EQ_RA_MAIN;POS_EQ_DEC_MAIN)", radius=0.01, cache=False)
    print("[Vizier] query_region 空坐标不可行，改试 TAP")
except Exception as e:
    print("[Vizier] FAIL:", type(e).__name__, str(e)[:300])
