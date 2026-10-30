# -*- coding: utf-8 -*-
"""Phase 104az-47c：DESI mid_full 内部按 B 分档——B_0.8 切换点同口径验证"""
import json
import numpy as np

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_gaia_abs"
midf = json.load(open(BASE + r"\paperX_wd_linelevel_mid_full_snr.json", encoding="utf-8"))["mid_full"]
mid = [r for r in midf if r.get("B_MG") is not None]
print("DESI mid_full n=%d, B 范围 %.1f–%.1f MG, 中位 %.1f" %
      (len(mid), min(r["B_MG"] for r in mid), max(r["B_MG"] for r in mid),
       np.median([r["B_MG"] for r in mid])))

# B_0.8 切换点（×2 递推候选）
sw = {"Hbeta": 80.0, "Hgamma": 41.0, "Hdelta": 20.0, "Heps": 10.0}
print("\n=== 跨激活阈值 B 分档（同仪器同口径） ===")
for lab, b0 in sw.items():
    below = [r["lines"][lab]["d_pure"] for r in mid
             if r.get("lines", {}).get(lab) and r["B_MG"] < b0
             and np.isfinite(r["lines"][lab].get("d_pure")) and r["lines"][lab]["d_pure"] >= 0]
    above = [r["lines"][lab]["d_pure"] for r in mid
             if r.get("lines", {}).get(lab) and r["B_MG"] >= b0
             and np.isfinite(r["lines"][lab].get("d_pure")) and r["lines"][lab]["d_pure"] >= 0]
    if below and above:
        mb, ma = np.median(below), np.median(above)
        print("  %-7s 阈值=%4.0f MG  B<阈 n=%2d 中位=%.4f | B≥阈 n=%2d 中位=%.4f | 跳变=%.0f%%" %
              (lab, b0, len(below), mb, len(above), ma, 100.0 * (1.0 - ma / mb)))
    elif below:
        print("  %-7s 阈值=%4.0f MG  B<阈 n=%2d 中位=%.4f | B≥阈 n= 0（无样本）" %
              (lab, b0, len(below), np.median(below)))
    else:
        print("  %-7s 阈值=%4.0f MG  B<阈 n= 0 | B≥阈 n=%2d 中位=%.4f" %
              (lab, b0, len(above), np.median(above)))

# 更细 B 分档（Hgamma 重点）
print("\n=== Hgamma 细 B 分档（DESI mid_full） ===")
for lo, hi in [(10, 20), (20, 41), (41, 60), (60, 1000)]:
    sub = [r["lines"]["Hgamma"]["d_pure"] for r in mid
           if lo <= r["B_MG"] < hi and r.get("lines", {}).get("Hgamma")
           and np.isfinite(r["lines"]["Hgamma"].get("d_pure")) and r["lines"]["Hgamma"]["d_pure"] >= 0]
    if sub:
        print("    B[%2d,%3d) n=%2d  d_pure中位=%.4f" % (lo, hi, len(sub), np.median(sub)))
    else:
        print("    B[%2d,%3d) n= 0" % (lo, hi))

print("\n=== Hbeta 细 B 分档 ===")
for lo, hi in [(10, 40), (40, 80), (80, 1000)]:
    sub = [r["lines"]["Hbeta"]["d_pure"] for r in mid
           if lo <= r["B_MG"] < hi and r.get("lines", {}).get("Hbeta")
           and np.isfinite(r["lines"]["Hbeta"].get("d_pure")) and r["lines"]["Hbeta"]["d_pure"] >= 0]
    if sub:
        print("    B[%2d,%3d) n=%2d  d_pure中位=%.4f" % (lo, hi, len(sub), np.median(sub)))
    else:
        print("    B[%2d,%3d) n= 0" % (lo, hi))

# 无线率 vs B 档（Hgamma：缺口线是否在激活后消失）
print("\n=== Hgamma 无线率 vs B 档（线消失证据） ===")
for lo, hi in [(10, 41), (41, 1000)]:
    n_tot = sum(1 for r in mid if lo <= r["B_MG"] < hi)
    n_ok = sum(1 for r in mid if lo <= r["B_MG"] < hi and r.get("lines", {}).get("Hgamma")
               and np.isfinite(r["lines"]["Hgamma"].get("d_pure")))
    print("    B[%2d,%4d) 星=%2d  有线=%2d (%.0f%%)  无线率 %.0f%%" %
          (lo, hi, n_tot, n_ok, 100.0 * n_ok / n_tot, 100.0 * (n_tot - n_ok) / n_tot))
