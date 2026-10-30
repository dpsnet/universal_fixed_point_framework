# -*- coding: utf-8 -*-
# 104az-225 平方型族跨链全谱扫描（pyenv 3.11.8）
# 目的：判定平方型族 (a^2-b)/(c^2-d) 的命中是"核磁子链 μ_n 专属"还是"跨扇区普遍"
# 目标集：轻子 g 因子、磁矩比、精细结构常数、质子电子质量比（CODATA 记忆值，不确定度保守取宽）
# 附加：44/23 机制动机分解核验（44 = 4×11、23 = 对合域×N_gen+幂基）
import numpy as np
from fractions import Fraction

M = [2, 3, 4, 5, 7, 8, 15, 16, 21, 42, 49, 105]
BD = sorted(set(M + [1]))

# CODATA 记忆值（保守不确定度，3σ 容差从宽）
TARGETS = [
    ("g_e/2",           1.00115965218087, 3e-9),   # 绝对 8.2e-10 → 宽取 1e-9×3
    ("mu_p/mu_mu",      0.4669224,        5e-7),   # 相对 ~3e-7 → 3σ≈4.2e-7，宽取
    ("mu_p/mu_e",       658.210686,       1e-5),   # 不确定度小 → 3σ≈4.5e-7，宽取 1e-5 防记忆偏差
    ("1/alpha",         137.035999084,    1e-5),   # 2.1e-8 相对 → 3σ≈8.6e-6，宽取
    ("m_p/m_e",         1836.15267343,    1e-6),   # 相对 6e-11 → 3σ≈3.3e-7，宽取
]

def scan(target, thresh):
    hits = []
    for a in M:
        for c in M:
            for b in BD:
                for d in BD:
                    n2, d2 = a*a - b, c*c - d
                    if n2 <= 0 or d2 <= 0:
                        continue
                    val = n2/d2
                    if abs(val - target) <= thresh:
                        hits.append((a, b, c, d, n2, d2, val, val-target))
    return hits

print("=== 跨链全谱扫描（3σ 从宽容差）===")
print(f"族规模 = {len(M)**2 * len(BD)**2}\n")
for name, target, th in TARGETS:
    hits = scan(target, th)
    if hits:
        print(f"--- {name} = {target} ±{th:.1e} → 命中 {len(hits)} ---")
        for a, b, c, d, n2, d2, val, diff in sorted(hits, key=lambda x: abs(x[7]))[:5]:
            print(f"    ({a}^2-{b})/({c}^2-{d}) = {n2}/{d2} = {val:.10f}  dev {diff:+.2e}")
    else:
        print(f"--- {name} = {target} ±{th:.1e} → 命中 0 ---")

print("\n=== 44/23 机制动机分解核验 ===")
print("44 = 4×11 ?", 4*11 == 44, "| 4=不动点、11=N_active+k_max（均框架量）")
print("44 = 7²−5 ?", 7*7-5 == 44, "| 7=对合域、5=静默")
print("23 = 7×3+2 ?", 7*3+2 == 23, "| 对合域×N_gen+幂基 = 21+2")
print("23 = 5²−2 ?", 5*5-2 == 23, "| 静默²−幂基")
print("分子分母共用参数族：{7,5,3,2} = 对合域/静默/N_gen/幂基")

print("\n=== 对照：同域有理分数命中密度（框架量族产出的格点） ===")
vals = sorted(set(n2/d2 for a in M for c in M for b in BD for d in BD
                  if (n2 := a*a-b) > 0 and (d2 := c*c-d) > 0))
print(f"族产出的不同有理值数 = {len(vals)}（24336 组合去重后）")
print(f"值域范围 = [{vals[0]:.6f}, {vals[-1]:.6f}]")
