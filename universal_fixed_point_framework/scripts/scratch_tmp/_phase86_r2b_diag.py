# -*- coding: utf-8 -*-
"""诊断：nan 分布"""
import json, io, numpy as np

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_gaia_abs"
with io.open(BASE + r"\paperX_wd_absflux.json", "r", encoding="utf-8") as f:
    data = json.load(f)
rows = data["rows"]
print("n=", len(rows))
for key in ["blue_res", "red_res", "slopeA_res", "slopeB_res", "jump_res"]:
    nn = sum(1 for r in rows if r.get(key) is not None and np.isnan(r[key]))
    print(key, "nan:", nn, "/", len(rows))

# 看前 3 颗弱场星详情
wk = [r for r in rows if r["B_MG"] < 10]
for r in wk[:3]:
    print("gid=%d B=%.1f Teff=%.0f par=%s perr=%s d_pc=%s" % (
        r["gaia_int"], r["B_MG"], r["Teff"], r.get("parallax"), r.get("parallax_error"), r.get("d_pc")))
    for key in ["blue_obs", "blue_mod", "blue_res", "slopeA_mod", "slopeB_mod"]:
        print("  ", key, r.get(key))
