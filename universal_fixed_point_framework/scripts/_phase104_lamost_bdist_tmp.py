# -*- coding: utf-8 -*-
"""Phase 104az-46b：LAMOST 中场 B 分布 vs 缺口激活阈值（B_0.8 切换）"""
import json, collections
import numpy as np

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_gaia_abs"
d = json.load(open(BASE + r"\paperX_lamost_linelevel_raw.json", encoding="utf-8"))

mid = [r for r in d if r.get("grp") == "mid" and r.get("B_MG") is not None]
weak = [r for r in d if r.get("grp") == "weak" and r.get("B_MG") is not None]

def stats(v, name):
    v = np.array(sorted(v), dtype=float)
    print("  %-6s n=%3d  中位=%7.2f  均值=%7.2f  min=%6.1f  max=%7.1f  p25=%6.1f  p75=%6.1f" %
          (name, len(v), np.median(v), np.mean(v), v.min(), v.max(),
           np.percentile(v, 25), np.percentile(v, 75)))

print("=== LAMOST 样本 B 分布（MG） ===")
stats([r["B_MG"] for r in mid], "mid")
stats([r["B_MG"] for r in weak], "weak")

# 缺口激活阈值：B_0.8 切换点（η_comp=0.8 交叉）
# Hε 10 / Hδ 20 / Hγ 41 / Hβ 80 MG（×2 递推候选，26.16j-92/86）
sw = {"Hbeta": 80.0, "Hgamma": 41.0, "Hdelta": 20.0, "Heps": 10.0, "Hzeta": 8.0}
print("\n=== mid 星在各线激活阈值之上的比例（B >= B_0.8） ===")
for lab, b0 in sw.items():
    n_above = sum(1 for r in mid if r["B_MG"] >= b0)
    print("  %-7s B_0.8=%5.1f MG   mid 星 ≥阈值: %2d/%2d (%.0f%%)" %
          (lab, b0, n_above, len(mid), 100.0 * n_above / len(mid)))

print("\n=== 参照：DESI 中场样本 B 范围（§4.9：含强中场 40.9–51.0 MG） ===")
print("  DESI 中场 B≈41–51 MG → Hγ(41)激活、Hβ(80)未激活 → 差异主要由 Hγ/Hδ 贡献")
print("  LAMOST mid B 若主要 <41 MG → Hγ 未激活 → 差异消失符合 0.8 切换预言（非证伪）")

# 逐 B 档缺失率（LAMOST mid，Hbeta/Hgamma 有效星）——看 B 高端的趋势
print("\n=== LAMOST mid 星按 B 分档的线深（Hbeta/Hgamma/Hdelta） ===")
bins = [(0, 10), (10, 20), (20, 41), (41, 80), (80, 1000)]
for lab in ("Hbeta", "Hgamma", "Hdelta"):
    print("  --- %s ---" % lab)
    for lo, hi in bins:
        sub = [r for r in mid if lo <= r["B_MG"] < hi and r.get("lines", {}).get(lab)
               and np.isfinite(r["lines"][lab].get("d_pure")) and r["lines"][lab]["d_pure"] >= 0]
        if sub:
            v = [r["lines"][lab]["d_pure"] for r in sub]
            print("    B[%3d,%3d) MG  n=%2d  d_pure中位=%.4f" % (lo, hi, len(v), np.median(v)))
        else:
            print("    B[%3d,%3d) MG  n= 0" % (lo, hi))
