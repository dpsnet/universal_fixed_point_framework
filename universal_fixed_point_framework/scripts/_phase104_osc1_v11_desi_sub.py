# -*- coding: utf-8 -*-
"""同样本核验：DESI 40.9-51 MG 子集——标准缺失 vs 论文 §4.9 DESI 线级观测"""
import json, io
import numpy as np
p = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_gaia_abs\paperX_osc_v10_disk.json"
d = json.load(io.open(p, "r", encoding="utf-8"))
rs = d["results"]
# DESI 40.9-51 MG 子集
sub = [r for r in rs if 40.9 <= r["B_MG"] <= 51.2]
print("DESI 40.9-51.2 MG 子集 n=%d:" % len(sub))
for r in sub:
    print("  B=%.1f i=%.0f: %s | det_syn %s" % (
        r["B_MG"], r["Incl"],
        " ".join("%s %.0f%%" % (nm, r["miss"][nm]) for nm in ("Hβ","Hγ","Hδ")),
        {nm: r["det_syn"][nm] for nm in ("Hβ","Hγ","Hδ")}))
ms = {nm: [r["miss"][nm] for r in sub] for nm in ("Hβ","Hγ","Hδ")}
print("\n标准中位缺失（DESI 40.9-51 MG 子集）:")
for nm in ("Hβ","Hγ","Hδ"):
    print("  %s: %.1f%% (P25 %.1f P75 %.1f)" % (nm, np.median(ms[nm]), np.percentile(ms[nm],25), np.percentile(ms[nm],75)))
print("\n论文 §4.9 DESI 观测缺失（40.9-51 MG 档）: Hβ −45% / Hγ −84% / Hδ −98%")
print("观测序: Hδ(−98) > Hγ(−84) > Hβ(−45) —— 高 n 优先")
print("标准序: Hδ(%.1f) > Hγ(%.1f) > Hβ(%.1f) —— 高 n 优先" % (
    np.median(ms["Hδ"]), np.median(ms["Hγ"]), np.median(ms["Hβ"])))
print("\n=> DESI 序与标准序同向（高 n 优先）——'方向性成立'结论不成立（观测锚不稳定）")
