# -*- coding: utf-8 -*-
"""d_H 三候选在已知链的传播核验：m_τ 锚定链（P7-5c：16·dH+ln(16/15)/3，+0.043% 达标）"""
import math, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

LN1615 = math.log(16/15)/3
dH_fw = 2.709532     # 框架观测（P7-5c 达标口径）
dH_65  = 65/24       # 候选 65/24 = 2.7083333
dH_A   = math.sqrt(22/3)  # 候选 A
dH_16259 = 16259/6000     # 高精度候选

m_tau_base = 16*dH_fw + LN1615
for name, d in [("框架观测", dH_fw), ("65/24", dH_65), ("√(22/3)", dH_A), ("16259/6000", dH_16259)]:
    m = 16*d + LN1615
    print(f"{name}: d_H={d:.9f}  m_τ链值={m:.9f}  相对框架基线变化 {(m/m_tau_base-1)*100:+.5f}%")

# α 链：1/α = 24(d_H+3)
print("\n=== α 链传播 ===")
for name, d in [("框架观测", dH_fw), ("65/24", dH_65), ("√(22/3)", dH_A), ("16259/6000", dH_16259)]:
    ainv = 24*(d+3)
    print(f"{name}: 1/α = {ainv:.9f}  (dev vs CODATA 137.035999084: {(ainv-137.035999084)/137.035999084*100:+.6f}%)")

print("\n65/24 = (k_max/N_gen)·(1+1/k_max²) = 8/3·65/64 — A2 双符号族织法 (主结构×(1+修正))")
print("16259 = 2^14−2^7+3 = 2^(2·对合域)−2^对合域+N_gen；131 = 2^7+3（g_p/2 分子）同族")
