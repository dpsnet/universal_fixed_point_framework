# -*- coding: utf-8 -*-
"""S310 δ 度量函数扩展扫描（e/π 通道 + σ-e 混合——2026-10-28）

S302 扫 σ 幂框架量组合、S304 证伪直接候选——本步补齐缺口：
  ① e 幂通道：a/b × e^{−n}（n 小整数）与 e^{−n}·σ^p 混合
  ② π 通道：π/n、2π/n、π/(n·m)、π·σ^p、π·e^{−n}
  ③ 奇异极限偏移身份复核：δ = π/12 − θ_F（闭合点偏移）
判定：δ 不确定度由 σ_θ=1.32e-6 rad 传导（S300）——σ_score=|pred−δ|/σ_θ
  命中需 ≤1σ（1.3e-6）——3σ 内提示
"""
import math, itertools
import numpy as np

sigma = 1/15
e = math.e
pi = math.pi

theta_F_rad = 0.222229627845    # S295 权威
delta_rad = pi/12 - theta_F_rad # = 15°−θ_F 弧度（奇异极限偏移）
sigma_theta = 1.32e-6           # S300 传导不确定度
print("=== S310 δ 度量函数扩展扫描 ===\n")
print(f"δ = π/12 − θ_F = {delta_rad:.12f} rad（奇异极限偏移——静默未满度量）")
print(f"σ_θ = {sigma_theta:.2e} rad——σ_score = |pred−δ|/σ_θ\n")

S = [2, 3, 5, 7, 15, 42, 8, 4, 16, 11, 24]   # 框架常数池
hits = []

def test(name, val):
    if val is None or val <= 0 or not math.isfinite(val):
        return
    sc = abs(val - delta_rad) / sigma_theta
    hits.append((sc, name, val))

# ① e 幂通道
print("① e 幂通道：a/b × e^{−n} 与 e^{−n}·σ^p")
for n in [2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 16, 18, 19, 24]:
    for a in S:
        for b in S:
            test(f"({a}/{b})·e⁻{n}", a/b * e**(-n))
for n in [2, 3, 5, 8]:
    for a in S:
        for p in [1, 2, 3, 5]:
            test(f"{a}·e⁻{n}·σ^{p}", a * e**(-n) * sigma**p)

# ② π 通道
print("② π 通道：π/n、2π/n、π/(n·m)、π·σ^p、π·e^{−n}")
for n in S + [12, 24, 48, 80, 96, 100, 126, 127, 137, 158, 159, 160, 200]:
    test(f"π/{n}", pi/n)
    test(f"2π/{n}", 2*pi/n)
for n in S:
    for m in S:
        test(f"π/({n}·{m})", pi/(n*m))
for p in [1, 2, 3, 4, 5, 7, 8]:
    for a in S:
        test(f"{a}·π·σ^{p}", a*pi*sigma**p)
        test(f"π·σ^{p}", pi*sigma**p)
for n in [2, 4, 8, 16]:
    test(f"π·e⁻{n}", pi*e**(-n))

# ③ 奇异极限偏移身份复核
print("③ 奇异极限偏移身份：δ = π/12 − θ_F")
test("π/12 − 2/9", pi/12 - 2/9)
test("π/12·(1−σ·静默⁻¹?)", None)
# δ 与模流周期：δ = 2π/k？
for k in [158, 159, 160, 161, 162]:
    test(f"2π/{k}", 2*pi/k)
for k in [79, 80, 81]:
    test(f"π/{(k)}·2?", None)

hits.sort()
print(f"\n总候选 {len(hits)} 个——σ_score 排序（前 10）：")
print(f"{'σ_score':<10}{'候选':<24}{'值':<16}{'偏差(rad)'}")
for sc, name, val in hits[:10]:
    print(f"{sc:<10.2f}{name:<24}{val:<16.12g}{abs(val-delta_rad):.2e}")

best = hits[0]
print(f"\n最优：{best[1]} = {best[2]:.12g}——σ_score = {best[0]:.2f}")
print(f"  {'≤1σ 命中' if best[0] <= 1 else '提示(1-3σ)' if best[0] <= 3 else '>3σ 证伪——无精确命中'}")

# ④ δ 的数学身份核对（奇异极限偏移 = 静默未满——S304 已证伪直接候选）
print(f"\n④ 结构性观察：")
print(f"  δ/(π/12) = {delta_rad/(pi/12):.6f}——δ 为奇异角的 {delta_rad/(pi/12)*100:.3f}%")
print(f"  δ/σ = {delta_rad/sigma:.6f}——σ 单位 {delta_rad/sigma:.3f}")
print(f"  δ·15 = {delta_rad*15:.6f}——度口径 15°−θ_F 的弧度 15×")
print(f"  ln(1/δ) = {math.log(1/delta_rad):.6f}——δ 的 surprisal")
