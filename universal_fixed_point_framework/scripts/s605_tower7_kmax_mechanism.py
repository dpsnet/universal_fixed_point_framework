# -*- coding: utf-8 -*-
"""
S605 间隔量修正共享塔顶 7 的机制导出（2026-10-30）
识别：7 = k_max − 1（幂次域 [1,8] 半开域长）——S108 系数
      (k_max−1)/(N_gen+k_max−1) = 7/10 已有先例
机制候选：间隔量（轻子间隔 E_e−E_μ）= 幂次域内相邻差——
         差计数 = k_max−1 = 7——修正族共享"域长−1"结构
验证：I_μ 修正 42e^{−6} = 3!×(k_max−1)·e^{−3!}
      I_e 修正 σ^{k_max−1}/3 = σ⁷/3
"""
import math

def check(name, cond):
    if not cond:
        raise AssertionError(f"FAIL: {name}")
    print(f"PASS: {name}")

sigma = 1/15
k_max = 8
N_gen = 3

print("=== ① 7 = k_max − 1 识别 ===")
print(f"k_max = {k_max}——k_max−1 = {k_max-1}——奇数塔最大元 7")
print(f"S108 先例：系数 7/10 = (k_max−1)/(N_gen+k_max−1)")
print(f"  (8-1)/(3+8-1) = {7/10} ✓")
check("7 = k_max-1 (tower top = half-open domain length)", 7 == k_max-1)
check("S108 coefficient 7/10 = (k_max-1)/(N_gen+k_max-1)", (k_max-1)/(N_gen+k_max-1) == 7/10)

print("\n=== ② 间隔 = 域内相邻差——差计数 = k_max−1 ===")
domain = list(range(1, k_max+1))  # 幂次域 [1,8]
pairs = len(domain) - 1           # 相邻对数
print(f"幂次域 [1,{k_max}]：{domain}")
print(f"相邻对数（间隔数）= {pairs} = k_max−1 = 7")
check("interval count in domain = k_max-1", pairs == k_max-1)

print("\n=== ③ I_μ 修正分解 = 3!×(k_max−1)·e^{−3!} ===")
val_mu = 42 * math.exp(-6)
print(f"42 = 3!×7 = {math.factorial(3)}×{k_max-1} = {math.factorial(3)*(k_max-1)}")
check("42 = 3!*(k_max-1)", 42 == math.factorial(3)*(k_max-1))
print(f"e^{{−6}} = e^{{−3!}}——指数 = 活跃阶乘")
check("exp index 6 = 3!", 6 == math.factorial(3))
print(f"42e^{{-6}} = {val_mu:.6e}")

print("\n=== ④ I_e 修正分解 = σ^{{k_max−1}}/3 ===")
val_e = (sigma**(k_max-1))/3
print(f"σ^{{{k_max-1}}}/3 = σ⁷/3 = {val_e:.6e}")
print(f"恒等：σ⁷/3 = 5σ⁸（5 = σ⁻¹/3 = 15/3——S596 衔接）")
check("sigma^7/3 == 5*sigma^8", abs(val_e - 5*sigma**8) < 1e-20)

print("\n=== ⑤ 机制候选综合 ===")
print("间隔量修正族 = 活跃基因子 × (k_max−1) 结构：")
print("  I_μ：3!（活跃阶乘）×（k_max−1）——e 链（e^{−3!}）")
print("  I_e：σ^{k_max−1} ×（活跃基倒数 1/3）——σ 链（静默）")
print("  → 共享 k_max−1 = 7（域内间隔计数）——塔顶 = 域长−1")
print("链分域：I_μ 主项 e 同链修正（e 幂）——I_e 主项 3e 修正 σ 链")
print("  ——S584 判别对：混合链（含 e 窗口项）→ 奇根——σ⁷ 奇根一致")
print("\n诚实边界：'为何间隔用域内相邻差语义'仍属机制推理（非范畴导出）")
print("  ——候选级维持——7 = k_max−1 有 S108 系数先例——较 S604 加强")

print("\nALL PASS")
