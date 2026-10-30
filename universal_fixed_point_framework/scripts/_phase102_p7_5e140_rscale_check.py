# -*- coding: utf-8 -*-
"""
P7-5e-140：r(c) 多列标度判别——C(m) 形式判别（139 延伸）
================================================================
139 的 C₁/C₀ = 0.043（c=7）vs 0.091（c=8）不一致——补 c=9,10,12 列判别：
  P1 r(c) 序列（乘数 2,3,4 等差步长 c）
  P2 C₁/C₀ = 2(r−2)·c 是否常数（C(m)=C₀+C₁/m 检验）
  P3 1/c 标度：r−2 ∝ 1/c？（C₁/m 修正预言）
  P4 高阶备选：r−2 ∝ 1/c²？（E/m³ 型修正预言，但方向反）
"""
import json, os
import numpy as np

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"
fa = json.load(open(os.path.join(BASE, "_phase102_p7_5e_fullchain_tridiag.json"), encoding="utf-8"))
fb = json.load(open(os.path.join(BASE, "_phase102_p7_5e117_m32_scan.json"), encoding="utf-8"))
fc = json.load(open(os.path.join(BASE, "_phase102_p7_5e124_spectral_m256.json"), encoding="utf-8"))

B = {}
for k, v in fa["out"].items():
    B[-int(k)] = v["R2"]
for k, v in fb["out"].items():
    B[-int(k)] = v["Bstar0"]
for k, v in fc["out"].items():
    B[-int(k)] = v["Bstar"]

def closed(m):
    cl = abs(m)/2.0 + 1.0/7.0 + 1.0/(7.0*2.0**abs(m))
    if abs(m) == 1:
        cl += 1.0/65.0
    return cl

C_FIX = 0.1016

def Deff(m):
    return (closed(m) - 1.0/B[m]) - C_FIX/m

print("=== P7-5e-140 r(c) 多列标度判别 ===", flush=True)
print("--- P1 r(c) 序列（乘数等差 2→3→4，步长 c）---", flush=True)
cols = [7, 8, 9, 10, 12, 14]
res = []
for c in cols:
    m2, m3, m4 = 2*c, 3*c, 4*c
    if m4 not in B:
        continue
    d2, d3, d4 = Deff(m2), Deff(m3), Deff(m4)
    D1a = d3 - d2
    D1b = d4 - d3
    r = D1a/D1b
    res.append((c, r, m2, m3, m4))
    print("  c=%2d（m=%d/%d/%d）：Δ_eff=%.6f/%.6f/%.6f——r=%.4f、r−2=%+.5f" % (
        c, m2, m3, m4, d2, d3, d4, r, r-2.0), flush=True)

print("--- P2/P3 标度检验 ---", flush=True)
print("  假设 C(m)=C₀+C₁/m → C₁/C₀=2(r−2)c 应常数；r−2 ∝ 1/c", flush=True)
C1C0 = [(c, 2.0*(r-2.0)*c, r-2.0) for c, r, _, _, _ in res]
for c, k, e in C1C0:
    print("  c=%2d：C₁/C₀=%.4f、r−2=%+.5f、c·(r−2)=%+.5f、c²·(r−2)=%+.4f" % (
        c, k, e, c*e, c*c*e), flush=True)
# 检验 1/c 还是 1/c²
import itertools
cs = [c for c, _, _ in C1C0]
es = [e for _, _, e in C1C0]
print("  r−2 vs 1/c 线性拟合 R²：", flush=True)
x1 = np.array([1.0/c for c in cs]); y = np.array(es)
k1, b1 = np.polyfit(x1, y, 1)
r2_1 = 1.0 - np.sum((y - (k1*x1+b1))**2)/np.sum((y-np.mean(y))**2)
print("    y = %.5f·(1/c) %+.5f——R²=%.4f" % (k1, b1, r2_1), flush=True)
x2 = np.array([1.0/(c*c) for c in cs])
k2, b2 = np.polyfit(x2, y, 1)
r2_2 = 1.0 - np.sum((y - (k2*x2+b2))**2)/np.sum((y-np.mean(y))**2)
print("    y = %.5f·(1/c²) %+.5f——R²=%.4f" % (k2, b2, r2_2), flush=True)
print("exit 0", flush=True)
