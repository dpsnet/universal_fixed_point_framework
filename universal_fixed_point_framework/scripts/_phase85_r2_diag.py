# -*- coding: utf-8 -*-
"""R2 诊断：D_B/slope 残差为何为空 + res_b1 离群检查"""
import os, sys, json, io
import numpy as np

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"
sys.path.insert(0, r"E:\workspace\hyper-resolution\universal_fixed_point_framework\src\white_dwarf_analysis")
from white_dwarf_analysis_v10 import normalize, BALMER

with io.open(os.path.join(BASE, "paperX_wd_continuum.json"), "r", encoding="utf-8") as f:
    data = json.load(f)

rows = data["rows"]
print("n_rows:", len(rows))
for key in ["D_B_res", "slope_res"]:
    n = sum(1 for r in rows if r.get(key) is not None)
    print(key, "非空:", n)

# 检查前 3 行详情
for r in rows[:3]:
    print({k: (round(v, 4) if isinstance(v, float) else v) for k, v in r.items() if v is not None and k not in ("gaia_int",)})

# res_b1 离群
v = [(r["gaia_int"], r["B_MG"], r.get("res_b1_diff")) for r in rows if r.get("res_b1_diff") is not None]
v.sort(key=lambda x: -abs(x[2]))
print("res_b1 离群 top5:")
for g, b, d in v[:5]:
    print("  gid=%d B=%.1f res_b1=%.3f" % (g, b, d))

# 逐带统计 D_B_obs 分布（确认测量本身有效）
db = [(r["gaia_int"], r.get("D_B_obs"), r.get("D_B_theo"), r.get("slope_obs"), r.get("slope_theo")) for r in rows]
dbv = [x for x in db if x[1] is not None and x[3] is not None]
print("D_B_obs 有效:", sum(1 for x in db if x[1] is not None), "/", len(db))
print("slope_obs 有效:", sum(1 for x in db if x[3] is not None), "/", len(db))
