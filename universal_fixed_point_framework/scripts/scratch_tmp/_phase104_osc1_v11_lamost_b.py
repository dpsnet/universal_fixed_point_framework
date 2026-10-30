# -*- coding: utf-8 -*-
"""LAMOST B≥41 MG 子集核验：B 分布 + 观测缺失（41MG 档）"""
import json, io
import numpy as np
base = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_gaia_abs"
with io.open(base + r"\paperX_lamost_linelevel_raw.json", "r", encoding="utf-8") as f:
    data = json.load(f)
recs = data if isinstance(data, list) else data.get("mid", [])
print("LAMOST mid n=%d" % len(recs))
print("样例字段:", list(recs[0].keys()))
Bs = [r["B_MG"] for r in recs if r.get("B_MG") is not None]
print("有 B 星 n=%d" % len(Bs))
Bs_sorted = sorted(Bs)
print("B 分布：min %.1f / p25 %.1f / 中位 %.1f / p75 %.1f / max %.1f" % (
    Bs_sorted[0], Bs_sorted[len(Bs_sorted)//4], Bs_sorted[len(Bs_sorted)//2],
    Bs_sorted[3*len(Bs_sorted)//4], Bs_sorted[-1]))
ge41 = [r for r in recs if r.get("B_MG") is not None and r["B_MG"] >= 41]
print("\nB≥41 MG 子集 n=%d" % len(ge41))
for r in ge41:
    L = r["lines"]
    dd = {k: (v.get("d_pure") if isinstance(v, dict) else None) for k, v in L.items()}
    print("  B=%.1f %s | d_pure %s" % (r["B_MG"], r.get("name",""), {k: (round(v,3) if v is not None else None) for k,v in dd.items()}))
# 41MG 档观测缺失（论文行 1268）
print("\n论文 41MG 档观测缺失：Hγ −41% / Hβ −27% / Hδ −12% / Hε −2%（LAMOST B≥41 vs B<41）")
