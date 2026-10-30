# -*- coding: utf-8 -*-
"""S256f δ 框架化家族检验（防巧合铁律 S227）
候选：δ = 6σ³ + 4σ⁵ + 14σ⁷ + 13σ⁸
检验1：删项敏感性（哪些项必要）
检验2：系数微扰鲁棒性
检验3：同族复现（Σ C_p·σ^p 框架量组合）——其他已知小量的家族检验
检验4：随机系数命中率（基线——判断 90/6、4、14、13 是否显著优于随机）
"""
from decimal import Decimal, getcontext
getcontext().prec = 50
import random

ln15 = Decimal(15).ln()
delta_target = Decimal(16259)/Decimal(6000) - ln15
s3 = Decimal(1)/Decimal(15)**3
s4 = Decimal(1)/Decimal(15)**4
s5 = Decimal(1)/Decimal(15)**5
s7 = Decimal(1)/Decimal(15)**7
s8 = Decimal(1)/Decimal(15)**8
s6 = Decimal(1)/Decimal(15)**6

def sig_of(delta_pred):
    d = abs(delta_pred - delta_target)
    return float(d)*24/2.1e-8

print("=== S256f: δ 家族检验 ===")
print(f"δ_α 目标 = {float(delta_target):.12f}——需 σ ≤ 1（α⁻¹ 层面）\n")

print("--- 检验1：删项敏感性 ---")
full = 6*s3 + 4*s5 + 14*s7 + 13*s8
print(f"完整 6σ³+4σ⁵+14σ⁷+13σ⁸: σ={sig_of(full):.4f}")
print(f"删 13σ⁸（6σ³+4σ⁵+14σ⁷）: σ={sig_of(6*s3+4*s5+14*s7):.4f}")
print(f"删 14σ⁷（6σ³+4σ⁵+13σ⁸）: σ={sig_of(6*s3+4*s5+13*s8):.4f}")
print(f"删 4σ⁵（6σ³+14σ⁷+13σ⁸）: σ={sig_of(6*s3+14*s7+13*s8):.4f}")
print(f"删 6σ³（4σ⁵+14σ⁷+13σ⁸）: σ={sig_of(4*s5+14*s7+13*s8):.4f}")
print(f"仅 6σ³: σ={sig_of(6*s3):.4f}")

print("\n--- 检验2：系数替代（等值框架量）---")
# 90σ⁴ = 6σ³——其他等值表达
print(f"6σ³+4σ⁵+14σ⁷+13σ⁸: σ={sig_of(6*s3+4*s5+14*s7+13*s8):.4f}")
print(f"90σ⁴+4σ⁵+14σ⁷+13σ⁸: σ={sig_of(90*s4+4*s5+14*s7+13*s8):.4f}（同值）")
print(f"6σ³+4σ⁵+14σ⁷+12σ⁸: σ={sig_of(6*s3+4*s5+14*s7+12*s8):.4f}")
print(f"6σ³+4σ⁵+14σ⁷+15σ⁸: σ={sig_of(6*s3+4*s5+14*s7+15*s8):.4f}")

print("\n--- 检验3：同族复现（框架量系数 × σ 幂——其他小量）---")
# 已知小量：I_μ 残余候选 2σ⁵、S116 σ⁸ 预测、1/675 拟合
known = {
    "2σ⁵（I_μ 残余候选 S173）": 2*s5,
    "σ⁸（S116 预测）": s8,
    "3σ⁵": 3*s5,
    "4σ⁵": 4*s5,
    "6σ³": 6*s3,
}
for name, v in known.items():
    print(f"  {name} = {float(v):.6e}")

print("\n--- 检验4：随机系数基线（防巧合） ---")
# 系数随机 1-20，幂次 3-8 组合——看自然命中率
random.seed(42)
count_lt1 = 0
count_lt3 = 0
N = 20000
for _ in range(N):
    k3 = random.randint(1, 20); k5 = random.randint(1, 20)
    k7 = random.randint(1, 20); k8 = random.randint(1, 20)
    v = k3*s3 + k5*s5 + k7*s7 + k8*s8
    s = sig_of(v)
    if s <= 1: count_lt1 += 1
    if s <= 3: count_lt3 += 1
print(f"随机 4 项组合（系数 1-20、幂 3/5/7/8）：{N} 样本")
print(f"  σ≤1 命中数: {count_lt1}（{count_lt1/N*100:.2f}%）")
print(f"  σ≤3 命中数: {count_lt3}（{count_lt3/N*100:.2f}%）")
print(f"  若命中率极低——框架量组合命中非偶然")

print("\n--- 检验5：系数空间精确度分布（同幂次、系数 1-30） ---")
best = []
for k3 in range(1, 31):
    for k5 in range(1, 31):
        for k7 in range(1, 31):
            v = k3*s3 + k5*s5 + k7*s7
            best.append((sig_of(v), f"{k3}σ³+{k5}σ⁵+{k7}σ⁷"))
best.sort()
print("3 项最优（无 σ⁸）：")
for s, name in best[:5]:
    print(f"  {name}: σ={s:.2f}")
