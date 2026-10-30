# -*- coding: utf-8 -*-
"""
P7-5e-168：h(2) = 7/64 判别 → C 解析锁定
================================================================
背景（145/147/148）：C = h(2) - 1/128（147 解析链）；h(2) 数值 ≈ 0.109395（147 三档 4 位收敛）；
若 h(2) = 7/64 = 0.109375 → C = 7/64 - 1/128 = 13/128（148 强候选）——解析闭合缺 h(2) 精确身份。
145：过零位移 1/m² 阶 δ = -1/64 + 2g'(2) - 4h(2)；g'(2) = 3/32。
  → h(2) = (11/64 - δ)/4（11/64 = -1/64 + 6/64）
  → h(2) = 7/64 ⇔ δ = -17/64 = -0.265625；h(2) = 0.109395 ⇔ δ = -0.265705
本步：用 160 全链 480 点（B* 精度 1e-12 饱和 164）提取 δ_ext = lim[(Δx·m + 1/2)·m]，
多窗口 + Richardson 外推，对照两候选。
"""
import json, os
import numpy as np

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"
d160 = json.load(open(os.path.join(BASE, "_phase102_p7_5e160_spectral_m512.json"), encoding="utf-8"))
out = d160["out"]

print("== P7-5e-168：h(2) = 7/64 判别（过零位移 1/m² 阶 δ 提取）==", flush=True)

# s(m) = (Δx·m + 1/2)·m → δ + η/m + O(1/m²)；Δx·m = (B*·m - 2)·m
ms_all = np.arange(33, 513, dtype=float)
s_all = np.array([((out[str(-int(m))]["Bstar"]*m - 2.0)*m + 0.5)*m for m in ms_all])

# ---------- A. s(m) 全链收敛表 ----------
print("\n=== A) s(m) = (Δx·m+1/2)·m 全链（→ δ）===", flush=True)
for m in [64, 128, 192, 256, 320, 384, 448, 512]:
    idx = np.where(ms_all == m)[0][0]
    print("  m=%3d：s = %.6f" % (m, s_all[idx]), flush=True)

# ---------- B. 多窗口 Richardson（消 η/m 残差）----------
print("\n=== B) 窗口 Richardson（两点对消 η/m）===", flush=True)
def s_at(m):
    return ((out[str(-m)]["Bstar"]*m - 2.0)*m + 0.5)*m
for (m1, m2) in [(256, 512), (192, 384), (128, 256), (96, 192), (64, 128)]:
    s1, s2 = s_at(m1), s_at(m2)
    # s = δ + η/m：δ = (s1·m1 - s2·m2)/(m1 - m2)？ s(m) = δ + η/m
    # s1 = δ + η/m1, s2 = δ + η/m2 → δ = (s1/m1 - s2/m2)·m1m2/(m2-m1)
    # 更稳：δ = (s1·m2 - s2·m1)/(m2 - m1)
    d = (s1*m2 - s2*m1)/(m2 - m1)
    print("  (%d,%d)：s1=%.6f s2=%.6f → δ = %.6f（vs -17/64=-0.265625 差 %.4f pct）" %
          (m1, m2, s1, s2, d, (d+0.265625)/0.265625*100), flush=True)

# ---------- C. 全局拟合 s(m) = δ + η/m + ζ/m²（m≥128）----------
print("\n=== C) 三参拟合（m≥128 / m≥256）===", flush=True)
for mmin in [128, 192, 256]:
    idx = ms_all >= mmin
    X = np.vstack([np.ones(idx.sum()), 1.0/ms_all[idx], 1.0/ms_all[idx]**2]).T
    c, _, _, _ = np.linalg.lstsq(X, s_all[idx], rcond=None)
    r = float(np.sqrt(np.mean((X@c - s_all[idx])**2)))
    print("  m≥%3d：δ=%.6f η=%.4f ζ=%.2f RMS=%.1e（vs -17/64 差 %+.4f pct）" %
          (mmin, c[0], c[1], c[2], r, (c[0]+0.265625)/0.265625*100), flush=True)

# ---------- D. h(2) 反推 ----------
print("\n=== D) h(2) = (11/64 - δ)/4 反推 ===", flush=True)
# 最佳 δ 估计（C 通道 m≥256 三参）
idx = ms_all >= 256
X = np.vstack([np.ones(idx.sum()), 1.0/ms_all[idx], 1.0/ms_all[idx]**2]).T
c, _, _, _ = np.linalg.lstsq(X, s_all[idx], rcond=None)
d_best = c[0]
h2_ext = (11.0/64.0 - d_best)/4.0
print("  δ_ext = %.6f → h(2)_ext = %.6f" % (d_best, h2_ext), flush=True)
print("  候选：7/64 = 0.109375（→C=13/128）；数值 0.109395（→C=0.1015825）", flush=True)
print("  h(2)_ext vs 7/64 差 %+.4f pct；vs 0.109395 差 %+.4f pct" %
      ((h2_ext-0.109375)/0.109375*100, (h2_ext-0.109395)/0.109395*100), flush=True)
C_cand1 = 7.0/64.0 - 1.0/128.0
C_cand2 = 0.109395 - 1.0/128.0
print("  对应 C：7/64 路径 → %.8f（13/128=%.8f）；0.109395 路径 → %.8f（0.1016 差 %+.3f pct）" %
      (C_cand1, 13.0/128.0, C_cand2, (C_cand2-0.1016)/0.1016*100), flush=True)

# ---------- 判别 ----------
print("\n=== 判别 ===", flush=True)
dev7 = abs(h2_ext - 7.0/64.0)/ (7.0/64.0)
devnum = abs(h2_ext - 0.109395)/0.109395
if dev7 < 5e-4:
    verdict = "★★ h(2) = 7/64 解析候选升格（偏差 %.2e）→ C = 13/128 解析链闭合（h(2)-1/128）" % dev7
elif devnum < dev7:
    verdict = "★ h(2) ≈ 0.109395 数值维持（偏差 %.2e vs 7/64 %.2e）——13/128 解析闭合未达成" % (devnum, dev7)
else:
    verdict = "★ h(2) 判别未决（偏差 7/64: %.2e / 数值: %.2e）——δ 提取高阶污染限制精度" % (dev7, devnum)
print("  终判：%s" % verdict, flush=True)
print("  诚实边界：δ 提取受 1/m³+ 残差污染（s(m) 展开假设 η/m+ζ/m²）；h(2) 判别分辨率 ~1e-4 级", flush=True)

with open(os.path.join(BASE, "_phase102_p7_5e168_h2_identity.json"), "w", encoding="utf-8") as fo:
    json.dump({"s_chain": {str(m): float(s_at(m)) for m in [64,128,192,256,320,384,448,512]},
               "delta_ext": float(d_best), "h2_ext": float(h2_ext),
               "cand_7_64_dev": float(dev7), "cand_num_dev": float(devnum),
               "verdict": verdict}, fo, indent=1, ensure_ascii=False)
print("JSON 落盘 OK exit 0", flush=True)
