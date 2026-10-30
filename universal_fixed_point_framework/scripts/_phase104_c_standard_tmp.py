# -*- coding: utf-8 -*-
"""Phase 104az-55：C 的标准理论身份判别——标准判据（C=1, ℓ_B~r_n）vs 模型 C=3.03 的观测判别"""
import math
from _phase100_p3b_compression import eta_comp

names = {3: "Hα", 4: "Hβ", 5: "Hγ", 6: "Hδ", 7: "Hε"}
obs_thr = {4: 80.0, 5: 41.0, 6: 20.0, 7: 10.0}

def cross_field(n, target, C, lo=1.0, hi=1e6):
    assert eta_comp(n, lo, C) < target < eta_comp(n, hi, C), (n, eta_comp(n, lo, C), eta_comp(n, hi, C))
    for _ in range(60):
        mid = 0.5*(lo+hi)
        if eta_comp(n, mid, C) < target:
            lo = mid
        else:
            hi = mid
    return 0.5*(lo+hi)

print("=== C 的观测判别：标准 C=1（ℓ_B~r_n）vs 模型 C=3.03 vs 观测激活阈值 ===")
print("  标准理论判据：磁场破坏高 n 态当 ℓ_B ~ 轨道尺度（隐含 C=1）——C 不出现（=1 隐藏）")
print("  模型：η_comp = tail(r>C·ℓ_B)，C=3.03（p=0.99 框架身份）\n")
print("  %-4s | %-14s | %-14s | %-12s | %-10s" % ("线", "C=1 交叉(MG)", "C=3.03 交叉(MG)", "观测阈值(MG)", "C=1/观测"))
for n in (4, 5, 6, 7):
    B1 = cross_field(n, 0.8, 1.0)/100.0
    B3 = cross_field(n, 0.8, 3.0349)/100.0
    print("  %-4s | %-14.1f | %-14.1f | %-12.1f | %.1f" % (names[n], B1, B3, obs_thr[n], B1/obs_thr[n]))

print("\n=== C² 标度检验（交叉场强 ∝ C²？）===")
for n in (5,):
    b1 = cross_field(n, 0.8, 1.0)
    b3 = cross_field(n, 0.8, 3.0349)
    print("  Hγ: B(C=1)=%.1f / B(C=3.0349)=%.1f = %.2f（C²=%.2f）" % (b1/100, b3/100, b1/b3, 3.0349**2))

print("\n=== 标准物理里 C 的定位（概念分层）===")
print("  ① 标准部分：Landau 磁长度 ℓ_B=√(ħ/eB) 标准；Landau 基态高斯 |ψ|²∝exp(−ρ²/2ℓ_B²) 标准；")
print("     高斯 p-包含半径 C=√(2·ln(1/(1−p))) 是标准概率论公式（任何高斯过程）")
print("  ② 标准判据的隐含 C=1：标准文献用 ℓ_B ~ r_n（轨道半径）判定高 n 态退束缚——无 C 自由参数")
print("  ③ 模型独有：把 tail(r>C·ℓ_B) 定义为'禁戒率'η_comp（标准理论直接用振子强度/电离速率，")
print("     不用 tail 截断分数）；C 被框架身份锚定（p=0.99=1−(N_c·σ/2)²）——标准理论对 C 无约束")
print("  ④ 判别结论：C=1（标准判据）预言交叉 ~380 MG（Hγ）——比观测 41 MG 高 ~9 倍——")
print("     被四线观测排除；C=3.03（模型）预言 41.6 MG——被四线观测选中——")
print("     **C 值本身不是模型发明的（高斯包含半径通用），但'C=3.03 是观测要求的'是模型判别点**")
