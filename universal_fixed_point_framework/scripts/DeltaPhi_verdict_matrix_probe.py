# -*- coding: utf-8 -*-
"""Δφ 候选第二轮证伪探索（#64b，按裁决协议异路分别探索）

判据设计（每个候选推到可证伪检验点）：
  K1 整数勾股闭合：tanh(Δφ) 为有理数 ⟹ 偏转速度纯整数比例
  K2 g 来源锚：Δφ=ln g 且 g 有结构身份（旋量维数 2 / Clifford 态 15/16 / 谱隙）
  K3 4 步闭合：4·Δφ 的态数身份（2⁴=16 / 15 / 无）
  K4 与 v2 主身份（15=2⁴−1）咬合

一般化洞察：tanh(ln g) = (g²−1)/(g²+1) 恒为有理数（g 有理时）——
"Δφ=ln g 族"全体给出整数勾股；判别落在 g 的选择。
"""
import numpy as np
from fractions import Fraction

print("=== 一般化：Δφ = ln g 族（tanh 有理性恒等式）===")
for g in [2, 15, 16, 3, 4]:
    num = g * g - 1
    den = g * g + 1
    f = Fraction(num, den)
    print(f"g={g:<3} tanh(ln g)=(g²−1)/(g²+1)={num}/{den} = {f}  "
          f"勾股: sin={num}, cos={2*g}（(g²−1)²+(2g)²=(g²+1)² 恒等）")

print()
print("=== K1/K2/K3/K4 判据矩阵 ===")
gap = (np.sqrt(3) - 1) / 6
cands = {
    "C1 翻倍 Δφ=ln2": (np.log(2), 2, "旋量维数 Fin 2"),
    "C2 谱隙 coshΔφ−1=Δλ": (np.arccosh(1 + gap), None, "谱隙 Δλ_min（机检值）"),
    "C3 窗口 Δφ=d_H": (16259 / 6000, np.exp(16259 / 6000), "e^{d_H}≈15.03"),
    "C4 次第 Δφ=ln15/4": (np.log(15) / 4, 15, "Clifford 非标量层 15"),
    "C5 单位 Δφ=1": (1.0, np.e, "自然对数底 e"),
}
for name, (dphi, g, src) in cands.items():
    t = np.tanh(dphi)
    frac = Fraction(t).limit_denominator(10000)
    k1 = "✅" if frac.denominator <= 1000 else "❌"
    k2 = "✅" if g in (2, 15, 16) else ("⚠️" if g is not None else "❌")
    state4 = np.exp(4 * dphi) if dphi > 0 else 0
    k3 = "✅" if abs(state4 - 16) < 0.5 or abs(state4 - 15) < 0.5 else "❌"
    # K4：是否咬合 15=2⁴−1（C1: 4 步态数=16 ⟹ 15=16−1）
    k4 = "✅" if abs(state4 - 16) < 0.5 else "❌"
    print(f"{name:<22} Δφ={dphi:.6f} tanh≈{t:.6f} 有理={frac} K1={k1} "
          f"K2={k2} 4步态数={state4:.4f} K3={k3} K4={k4}  (g来源: {src})")

print()
print("=== 补充检验 ===")
# C3 重解释：窗口总 rapidity = d_H，e^{d_H} vs 15
print(f"C3 重解释：e^{{d_H}}={np.exp(16259/6000):.6f} vs 15（差 {abs(np.exp(16259/6000)-15)/15*100:.3f}%）"
      f"——窗口总量 ∝ 15 咬合级接近；作'每步'已证伪")
# C2 的 4 步态数身份
s2 = np.exp(4 * np.arccosh(1 + gap))
print(f"C2 4步态数 e^{{4Δφ}}={s2:.4f}——无 2/15/16 身份")
# C1 4 步态数
print(f"C1 4步态数 e^{{4·ln2}}=16.0000——精确 2⁴（Clifford 全态）⟹ 15=16−1 与 v2 主身份精确咬合")
# C4 4 步态数
print(f"C4 4步态数 e^{{4·(ln15/4)}}=15.0000——直接 15（非 16−1，与 v2 不咬合）")
# C5 检验
print(f"C5 tanh(1)={Fraction(np.tanh(1)).limit_denominator(10000)} 无理（无整数勾股）")
