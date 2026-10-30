# -*- coding: utf-8 -*-
"""
chain_audit_147_dh_scan.py — d_H 候选空间重建扫描
观测（框架）d_H = 2.709532（1/α = 24(d_H+3) = 137.028 口径）
精确反推 d_H* = 1/(24α) − 3，α=1/137.035999084 → 2.7098333
目标：重建 ±0.2% 窗口内全部"简单框架表达式"候选，重核 143 段双候选，找 0.01% 级判别路径
"""
from fractions import Fraction as F
import itertools, math, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

T = 2.709532                       # 框架观测口径
T_STAR = 137.035999084/24 - 3      # CODATA 精确反推
print(f"框架观测 d_H = {T:.9f}；CODATA 反推 d_H* = {T_STAR:.9f}（差 {(T_STAR-T)/T*100:.4f}%）")

FR = {2, 3, 4, 5, 7, 8, 16, 25, 49, 64}   # 框架量集
SIG = F(1, 15)

def dev(v): return (v - T) / T * 100

# ---- 候选表达式族（先定规则）----
cands = []

def reg(name, v):
    if abs(dev(v)) < 0.25:
        cands.append((abs(dev(v)), name, v, dev(v)))

# 族1：√(a/b)，a,b ∈ 框架量线性组合
for a in list(FR) + [7+1, 7+2, 7+3, 7+4, 7-1, 7-2, 7+5, 15, 22, 21, 23, 33, 34, 35]:
    for b in FR:
        if a > 0 and b > 0:
            reg(f"√({a}/{b})", math.sqrt(a/b))
# 族2：有理 k/d
for k in FR:
    for d in FR:
        if d: reg(f"{k}/{d}", k/d)
# 族3：k/d 的 (1±σ·j) 修正
for k in FR:
    for d in FR:
        base = k/d
        for j in (1, 2, 3, 4, 5):
            reg(f"{k}/{d}·(1+{j}σ)", base*(1+float(j)*SIG))
            reg(f"{k}/{d}·(1−{j}σ)", base*(1-float(j)*SIG))
            reg(f"{k}/{d}/(1+{j}σ)", base/(1+float(j)*SIG))
            reg(f"{k}/{d}/(1−{j}σ)", base/(1-float(j)*SIG))
# 族4：√(k·d/m) 型
for k in FR:
    for d in FR:
        for m in FR:
            v = k*d/m
            if v > 0: reg(f"√({k}·{d}/{m})", math.sqrt(v))

cands.sort()
print(f"\n=== ±0.25% 窗口命中：{len(cands)} 个 ===")
for err, name, v, d in cands[:30]:
    print(f"  |{d:+.4f}%|  {name} = {v:.9f}")

print("\n=== 双候选重核 ===")
A = math.sqrt(7 + 1/3)
print(f"候选A √(7+1/3) = {A:.9f}  dev(vs框架) = {dev(A):+.4f}%  dev(vs CODATA) = {(A-T_STAR)/T_STAR*100:+.4f}%")
B = 3 * (1 + 1/60)
print(f"候选B (8+1)/3·(1+σ/4) = {B:.9f}  dev(vs框架) = {dev(B):+.4f}%  → 与登记 +0.060% 不符（登记疑笔误）")
# 若登记 +0.060% 准确，候选B ≈ 2.711158
print(f"登记 dev +0.060% 对应的候选值 ≈ {T*(1+0.00060):.9f}")
