# -*- coding: utf-8 -*-
"""S256b α⁻¹ 修正项攻坚：0.035999084 的框架量组合
α⁻¹ = 137.035999084——整数层 137 = 2³(2⁴+1)+1 = 136+1（机制）
修正 0.035999084 需要含无理数（ln15/ln2/e/σ 幂/√）的框架表达式
目标：|预测−0.035999084| ≤ 1σ = 2.1e-8
"""
import math
from itertools import product

target = 0.035999084
unc = 2.1e-8
ln15 = math.log(15)
ln2 = math.log(2)
ln1615 = math.log(16/15)
ln17 = math.log(17)
sigma = 1/15
e = math.e
print("=== S256b: α⁻¹ 修正项 0.035999084 扫描 ===\n")
print(f"目标 = {target:.9f}——需 |预测−目标| ≤ {unc:.1e}（≤1σ）")

# 候选池：ln 族、σ 幂、e 幂、√ 组合、框架常数分数
base_pool = [
    ("σ", sigma), ("σ²", sigma**2), ("σ³", sigma**3), ("σ⁴", sigma**4),
    ("σ⁵", sigma**5), ("2σ³", 2*sigma**3), ("3σ³", 3*sigma**3),
    ("4σ³", 4*sigma**3), ("6σ³", 6*sigma**3),
    ("σ/15", sigma/15), ("σ²/15", sigma**2/15), ("σ³/15", sigma**3/15),
    ("1/27", 1/27), ("1/28", 1/28), ("1/29", 1/29),
    ("1/2.7", 1/2.7), ("1/27.78", 1/27.78),
    ("ln(16/15)", ln1615), ("ln(16/15)/2", ln1615/2),
    ("ln(16/15)×9/16", ln1615*9/16), ("ln(16/15)×8/15", ln1615*8/15),
    ("ln(16/15)×7/15", ln1615*7/15), ("ln(16/15)×5/9", ln1615*5/9),
    ("ln2/15", ln2/15), ("ln2/16", ln2/16), ("ln2/19", ln2/19),
    ("ln2×σ²", ln2*sigma**2), ("ln2×σ³", ln2*sigma**3),
    ("ln15/75", ln15/75), ("ln15/75.24", ln15/75.24), ("ln15/76", ln15/76),
    ("e^-6/0.07", math.exp(-6)/0.07), ("e^-6×14", 14*math.exp(-6)),
    ("e^-5/18", math.exp(-5)/18), ("e^-4/25", math.exp(-4)/25),
    ("σ×ln(16/15)×8", sigma*ln1615*8),
    ("σ⁴×1823", sigma**4*1823), ("σ⁴×1822", sigma**4*1822),
    ("σ⁴×1810", sigma**4*1810), ("σ⁴×1820", sigma**4*1820),
    ("σ⁴×1825", sigma**4*1825),
    ("√(2/3)/22", math.sqrt(2/3)/22), ("√(2/3)/22.7", math.sqrt(2/3)/22.7),
    ("√(2/3)/23", math.sqrt(2/3)/23),
    ("ln(17)/76", ln17/76), ("ln(17)/76.1", ln17/76.1),
    ("ln(17)/77", ln17/77), ("ln15/ln2/42", ln15/ln2/42),
    ("ln15×σ/45", ln15*sigma/45), ("ln15×σ²/2", ln15*sigma**2/2),
    ("ln15×2σ³×10/9", ln15*2*sigma**3*10/9),
    ("ln15×2σ³", ln15*2*sigma**3),
]

print("\n=== 单参数命中（top 10） ===")
res = []
for (n, v) in base_pool:
    d = abs(v - target)
    res.append((d, v, n))
res.sort()
for d, v, n in res[:10]:
    print(f"  {n} = {v:.9f}  偏差 {d:.2e}  σ={d/unc:.1f}")

print("\n=== 双参数（k·A ± m·B——k,m∈整数 1-20） top 8 ===")
res = []
for (n1, v1), (n2, v2) in product(base_pool, repeat=2):
    for k in range(1, 13):
        for m in range(1, 13):
            for s in (+1, -1):
                v = k*v1 + s*m*v2
                d = abs(v - target)
                res.append((d, v, f"{k}×({n1}){'±' if s>0 else '−'}{m}×({n2})"))
res.sort()
for d, v, s in res[:8]:
    print(f"  {s} = {v:.9f}  偏差 {d:.2e}  σ={d/unc:.1f}")

print("\n=== 判定 ===")
print("若 top 命中 σ ≤ 1——修正项闭环——α⁻¹ = 136+1+修正 全框架")
