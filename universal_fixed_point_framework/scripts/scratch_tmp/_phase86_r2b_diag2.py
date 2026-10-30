# -*- coding: utf-8 -*-
"""诊断：nan 星详情 + 修复汇总"""
import json, io, numpy as np

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_gaia_abs"
with io.open(BASE + r"\paperX_wd_absflux.json", "r", encoding="utf-8") as f:
    data = json.load(f)
rows = data["rows"]
for key in ["blue_res", "red_res", "slopeA_res", "slopeB_res"]:
    for r in rows:
        v = r.get(key)
        if v is not None and (isinstance(v, float) and np.isnan(v)):
            print("nan star:", r["gaia_int"], key, "B=", r["B_MG"], "par=", r.get("parallax"),
                  "d=", r.get("d_pc"), "blue_obs=", r.get("blue_obs"), "blue_mod=", r.get("blue_mod"),
                  "slopeB_mod=", r.get("slopeB_mod"), "koester=", r.get("koester"))

# 修复汇总：过滤 nan
def grp(rows, cond, key):
    vs = []
    for r in rows:
        if cond(r):
            v = r.get(key)
            if v is not None and not (isinstance(v, float) and np.isnan(v)):
                vs.append(v)
    return (len(vs), float(np.mean(vs)), float(np.std(vs))) if vs else (0, None, None)

print("\n--- 修复后汇总 ---")
for key in ["blue_res", "red_res", "slopeA_res", "slopeB_res", "jump_res"]:
    for nm, cond in [("弱场<10MG", lambda r: r["B_MG"] < 10),
                     ("中场10-100", lambda r: 10 <= r["B_MG"] < 100),
                     ("强场>100", lambda r: r["B_MG"] >= 100)]:
        n, mu, sd = grp(rows, cond, key)
        if n:
            print("%-10s %-12s n=%3d mean=%+.4f sd=%.4f" % (key, nm, n, mu, sd))
