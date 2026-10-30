# -*- coding: utf-8 -*-
"""
P7-5e-115 预备：二次段五点形态精化（失调身份框架化第一步）
============================================================
目标：把 114 的"末点衰减登记"升级为定量形态——三阶差分揭示三次项；
      二次+三次拟合 vs 纯二次拟合残差对比；线性段斜率精化；均匀带登记。
数据：全链权威 JSON（tridiag，δ(1/B) 高精度）。
"""
import json, os
import numpy as np

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"
fc = json.load(open(os.path.join(BASE, "_phase102_p7_5e_fullchain_tridiag.json"), encoding="utf-8"))
deltas = {int(k): v for k, v in fc["deltas"].items()}
print("全链 δ(1/B)（m=−1..−13）：", flush=True)
for m in sorted(deltas, reverse=True):
    print("  m=%+d  δ=%.9f" % (m, deltas[m]), flush=True)

# ---------- 二次段 m=9..13（|m| 升序）----------
mm = np.arange(9, 14, dtype=float)                      # |m| = 9..13
dd = np.array([deltas[-m] for m in range(9, 14)])       # δ(9..13)
d1 = dd[1:] - dd[:-1]                                   # 一阶差分（10..13）
d2 = d1[1:] - d1[:-1]                                   # 二阶差分（11..13）
d3 = d2[1:] - d2[:-1]                                   # 三阶差分（12..13）
print("", flush=True)
print("== 二次段差分（|m|=9..13）==", flush=True)
print("  δ      = %s" % ["%.6f" % x for x in dd], flush=True)
print("  d1     = %s" % ["%+.6f" % x for x in d1], flush=True)
print("  d2     = %s" % ["%+.6f" % x for x in d2], flush=True)
print("  d3     = %s" % ["%+.6f" % x for x in d3], flush=True)
print("  d3 判定：%s" % ("三点恒定（纯三次）" if max(d3)-min(d3) < 3e-6 else "三点非恒定（更高阶/噪声）"), flush=True)

# 二次拟合 vs 二次+三次拟合（五点最小二乘）
A2 = np.vstack([np.ones(5), mm, mm**2]).T
A3 = np.vstack([np.ones(5), mm, mm**2, mm**3]).T
c2, res2, _, _ = np.linalg.lstsq(A2, dd, rcond=None)
c3, res3, _, _ = np.linalg.lstsq(A3, dd, rcond=None)
pred2, pred3 = A2@c2, A3@c3
rms2 = float(np.sqrt(np.mean((pred2-dd)**2)))
rms3 = float(np.sqrt(np.mean((pred3-dd)**2)))
print("", flush=True)
print("== 形态拟合（|m|=9..13 五点）==", flush=True)
print("  纯二次：δ = %.6f + %.6f·m + %.7f·m²   RMS=%.2e" % (c2[0], c2[1], c2[2], rms2), flush=True)
print("  二次+三次：δ = %.6f + %.6f·m + %.7f·m² + %.2e·m³   RMS=%.2e" % (c3[0], c3[1], c3[2], c3[3], rms3), flush=True)
print("  残差对比：三次项改善 %.1f 倍" % (rms2/rms3 if rms3 > 0 else float('inf')), flush=True)
print("  三次项系数 e = %.3e" % c3[3], flush=True)
print("  e·10⁶ = %.2f（3=N_gen 候选：e ≈ N_gen/10⁶——后验候选，需 m=−14 确认）" % (c3[3]*1e6), flush=True)

# 分点残差
print("  五点残差（纯二次）：%s" % ["%+.1e" % x for x in (dd-pred2)], flush=True)
print("  五点残差（二次+三次）：%s" % ["%+.1e" % x for x in (dd-pred3)], flush=True)

# ---------- 线性段 m=5..8 斜率精化 ----------
ml = np.arange(5, 9, dtype=float)
dl = np.array([deltas[-m] for m in range(5, 9)])
A1 = np.vstack([np.ones(4), ml]).T
cl, _, _, _ = np.linalg.lstsq(A1, dl, rcond=None)
kappa_1400 = (6.0/np.pi)/1400.0
print("", flush=True)
print("== 线性段斜率精化（|m|=5..8）==", flush=True)
print("  四点最小二乘：δ = %.6f + %.6f·m（斜率 s=%.6f）" % (cl[0], cl[1], cl[1]), flush=True)
print("  s vs κ/1400 = %.6f——偏差 %+.3f pct" % (kappa_1400, (cl[1]-kappa_1400)/kappa_1400*100), flush=True)
print("  候选：1/735 = %.6f（偏差 %+.3f pct——735=7²·15——后验候选）" % (1/735.0, (cl[1]-1/735.0)/(1/735.0)*100), flush=True)

# ---------- 均匀带 m=2..4 ----------
du = np.array([deltas[-m] for m in range(2, 5)])
print("", flush=True)
print("== 均匀带登记（|m|=2..4）==", flush=True)
print("  δ = %s" % ["%.3e" % x for x in du], flush=True)
print("  比值 = %s（无干净身份——登记维持开放）" % ["%.3f" % (du[i]/du[0]) for i in range(1, 3)], flush=True)

print("", flush=True)
print("exit 0", flush=True)
