# -*- coding: utf-8 -*-
"""d_H = 16259/6000 全框架量生成链验证（2026-10-25）

候选生成链（104az-149 分母未分解，本轮补全）：
  d_H^(obs) = 16259/6000 = [2^7·(2^7−1) + 3] / [2⁴·3·5³]
组件框架身份：
  2 = 幂基、7 = 对合域（104az-188）、2^7−1 = 127 = M_7（Mersenne 素数，
  对合域 7 为 Mersenne 指数）、3 = N_gen（活跃代）、2⁴ = 16 = Cℓ(3,1) 全态、
  5 = 静默、5³ = 静默³
隐藏恒等：2^7 − 5³ = 128 − 125 = 3 = N_gen（翻倍塔 7 层 vs 静默立方之差 = 活跃代）
  ⟹ 5³ = 2^7 − N_gen ⟹ 分母 6000 = 2⁴·N_gen·(2^7−N_gen) 全框架量

模式 8 先证伪：整数/有理恒等逐项验证 + 全量样本核对。
"""
import numpy as np
from fractions import Fraction

print("=== 组件恒等验证 ===")
print(f"2^7 = {2**7}")
print(f"5³  = {5**3}")
print(f"2^7 − 5³ = {2**7 - 5**3} = N_gen = 3 ✓")
print(f"2^7 − 1 = {2**7-1} = 127 = M_7（Mersenne 素数，指数 7 = 对合域）✓")
print(f"2^7·(2^7−1) + 3 = {2**7*(2**7-1)+3} = 16259 ✓")
print(f"2⁴·3·5³ = {2**4*3*5**3} = 6000 ✓")
print()

print("=== 恒等式主验证 ===")
lhs = Fraction(16259, 6000)
rhs = Fraction(2**7*(2**7-1)+3, 2**4*3*5**3)
print(f"16259/6000 = {lhs}")
print(f"[2^7·(2^7−1)+3]/(2⁴·3·5³) = {rhs}")
print(f"相等：{lhs == rhs}（精确有理恒等）")
print()

print("=== 模式 8 全量样本核对（恒等式两侧重算，含分母等价形式） ===")
samples = 0
for n in range(-50, 51):
    for gen in [2, 3, 4]:  # 检查 2^n − 5³ = gen 的变体不混淆（仅 n=7, gen=3 成立）
        if 2**n - 5**3 == gen:
            samples += 1
            print(f"  2^{n} − 5³ = {gen}（恒等成立样本 {samples}）")
print(f"2^n − 5³ = gen 恒等检查：n∈[−50,50] × gen∈{{2,3,4}} 共 {samples} 个成立样本"
      f"（应恰为 (7,3) 1 个）")
print()

# 数值参照：d_H 与 ln15 的 δ 关系（超验数身份）
dH = 16259/6000
ln15 = np.log(15)
delta = dH - ln15
print(f"=== δ 参照（超验身份） ===")
print(f"d_H = {dH:.9f}；ln15 = {ln15:.9f}")
print(f"δ = d_H − ln15 = {delta:.9f}（超验数——d_H 有理、ln15 超验，δ 无精确有理身份）")
print(f"δ 层放大镜：E 口径 ppm 级差 → δ 层 0.1% 级差（deltaP7_identity_probe 已证）")
print()
print("结论：d_H^(obs) = 16259/6000 获全框架量闭式生成链候选——")
print("  [M_7·2^7 + N_gen] / [全态·N_gen·静默³]，含隐藏恒等 2^7−5³=N_gen、")
print("  M_7=127（Mersenne 素数、对合域 7 作指数）——从'自由参数'推进为'框架量闭式'；")
print("  诚实边界：后验分解（先有数值再找框架身份），生成链语义为候选级，")
print("  Lean 形式化建议：AlphaChain 加 dH 分解恒等定理（ℚ 精确恒等）。")
