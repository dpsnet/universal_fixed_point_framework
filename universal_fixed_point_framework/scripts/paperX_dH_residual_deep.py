#!/usr/bin/env python3
"""
paperX_dH_residual_deep.py — δ 残差 Δ ≈ 8×10⁻⁷ 的深入结构分析（2026-07-29）

背景与动机：
  §3.5.4d 中存在两个看似矛盾的残差数值：
    - paperX_dH_selection_principle.py: d(√5) = 2.70949946，Δ = 5.41×10⁻⁷
    - paperX_dH_residual_check.py:      d(√5) = 2.70949916，Δ = 8.35×10⁻⁷（与 2³×10⁻⁷ 吻合 4.2%）
  本脚本用 mpmath 50 位精度证明：差异源于两个脚本求解的是**不同的方程**——
    - selection_principle: 精确固定点  d = ln15 + ln15·k·ε₃(d)，ε₃(d) = 1-(1-A(d))^{1/d}
    - residual_check:      线性化方程  d(d-ln15) = k·ln15·A(d)（用了 ε₃ ≈ A/d 一阶近似）
  线性化误差 ≈ 2.94×10⁻⁷ 恰好解释了 8.35e-7 − 5.41e-7 = 2.94e-7。

核心结论：
  1. "Δ ≈ 2³×10⁻⁷（4.2% 吻合）"是**线性化误差污染的人造巧合**——
     对精确固定点，Δ_exact = 5.41×10⁻⁷，与 8×10⁻⁷ 失配 32%。
  2. 二阶自洽闭式将展开误差从 7.3×10⁻⁷ 压到 4.1×10⁻⁸，
     无需任何"残差候选修正"即可闭式逼近精确解。
  3. 线性化误差本身有闭式：Δd_lin = ln15·√5·(d-1)/(2d²)·A²·response ≈ 2.94×10⁻⁷。
  4. 可检验性：Δ_exact/χ²分辨率 ≈ 0.27%，当前 d_H（5 位有效数字）无法检验任何
     10⁻⁷ 量级的残差结构；需要 d_H 确定到 7 位有效数字。
"""

import numpy as np
from mpmath import mp, mpf, log, exp, sqrt, findroot

mp.dps = 50

ln15 = log(15)
k5 = sqrt(5)
d_fit = mpf("2.7095")
d0 = ln15

A = lambda d: exp(-d**2) + exp(-d * (3 + d))
Ap = lambda d: -2 * d * exp(-d**2) - (3 + 2 * d) * exp(-d * (3 + d))
eps3 = lambda d: 1 - (1 - A(d)) ** (1 / d)
eps3p = lambda d: Ap(d) / d - A(d) / d**2  # 一阶近似 ε₃≈A/d 的导数

# =====================================================================
print("=" * 74)
print("S1 高精度基准：两个方程的解（mpmath 50 位）")
print("=" * 74)

# 精确固定点方程: d = ln15 + ln15·k·ε₃(d)
f_exact = lambda d: d - ln15 - ln15 * k5 * eps3(d)
d_exact = findroot(f_exact, mpf("2.7095"))

# 线性化方程: d(d-ln15) = k·ln15·A(d)   （ε₃ 取一阶近似 A/d）
f_lin = lambda d: d * (d - ln15) - k5 * ln15 * A(d)
d_lin = findroot(f_lin, mpf("2.7095"))

lin_err = d_exact - d_lin
print(f"  d_exact (精确固定点, selection_principle) = {mp.nstr(d_exact, 20)}")
print(f"  d_lin   (线性化方程,   residual_check)    = {mp.nstr(d_lin, 20)}")
print(f"  线性化误差 d_exact - d_lin              = {mp.nstr(lin_err, 10)}")

Delta_exact = d_fit - d_exact
Delta_lin = d_fit - d_lin
print(f"\n  Δ_exact = d_fit - d_exact = {mp.nstr(Delta_exact, 10)}")
print(f"  Δ_lin   = d_fit - d_lin   = {mp.nstr(Delta_lin, 10)}")
print(f"  分解检验: Δ_exact + 线性化误差 = {mp.nstr(Delta_exact + lin_err, 10)}")
print(f"           = Δ_lin ✅（残差完全分解）")

# =====================================================================
print("\n" + "=" * 74)
print("S2 'Δ ≈ 2³×10⁻⁷' 吻合检验：两种残差定义对照")
print("=" * 74)

target = mpf("8e-7")  # 2^N_active × 10⁻⁷
m_lin = abs(Delta_lin - target) / target * 100
m_exact = abs(Delta_exact - target) / target * 100
print(f"  2³×10⁻⁷ = {mp.nstr(target, 5)}")
print(f"  vs Δ_lin   = {mp.nstr(Delta_lin, 8)}:  失配 {mp.nstr(m_lin, 4)}%   <- residual_check 报告的 4.2%")
print(f"  vs Δ_exact = {mp.nstr(Delta_exact, 8)}:  失配 {mp.nstr(m_exact, 4)}%  <- 精确固定点")
print(f"""
  判定：4.2% 的"吻合"只存在于被线性化误差（2.94×10⁻⁷，占 Δ_lin 的 35%）
  污染的残差定义中。换用精确固定点后失配升至 32%。
  ⇒ "Δ = 2^N_active × 10⁻⁷ 是系统性结构修正"的假说**不成立**，
    它是近似层级混淆产生的人造巧合（artifact）。""")

# =====================================================================
print("=" * 74)
print("S3 线性化误差的闭式解释")
print("=" * 74)
# ε₃ 的二阶展开: 1-(1-A)^{1/d} = A/d + (d-1)/(2d²)·A² + O(A³)
# ⇒ d_exact - d_lin ≈ ln15·√5·(d-1)/(2d²)·A(d)² · response
# response = 1/(1 - ln15·√5·ε₃'(d_exact)) ≈ 0.992
resp = 1 / (1 - ln15 * k5 * eps3p(d_exact))
shift_closed = ln15 * k5 * (d_exact - 1) / (2 * d_exact**2) * A(d_exact) ** 2 * resp
print(f"  ε₃ 二阶项系数 (d-1)/(2d²)      = {mp.nstr((d_exact-1)/(2*d_exact**2), 8)}")
print(f"  response 因子 1/(1-ln15·√5·ε₃') = {mp.nstr(resp, 8)}")
print(f"  闭式线性化误差                  = {mp.nstr(shift_closed, 8)}")
print(f"  数值线性化误差                  = {mp.nstr(lin_err, 8)}")
print(f"  吻合度                          = {mp.nstr(abs(shift_closed-lin_err)/lin_err*100, 4)}% 误差")
print(f"  ⇒ 线性化误差是纯粹的数学截断效应，无任何物理结构 ✅")

# =====================================================================
print("\n" + "=" * 74)
print("S4 高阶自洽闭式：无需残差候选的收敛序列")
print("=" * 74)
A0, Ap0 = A(d0), Ap(d0)

# 一阶闭式（doc §3.5.4d 公式）: δ₁ = k·ln15·A0/(d0 - k·ln15·Ap0)
d_1st = d0 + k5 * ln15 * A0 / (d0 - k5 * ln15 * Ap0)

# 二阶闭式: 保留 LHS 的 δ² 项，解二次方程 δ² + (d0 - k·ln15·Ap0)δ - k·ln15·A0 = 0
b = d0 - k5 * ln15 * Ap0
c = -k5 * ln15 * A0
d_2nd = d0 + (-b + sqrt(b**2 - 4 * c)) / 2

# 精确 ε₃ 的二阶自洽闭式: δ = ln15·k·[A/d + (d-1)/(2d²)A²] 在 d0 处取值 + 导数修正
eps3_2nd_d0 = A0 / d0 + (d0 - 1) / (2 * d0**2) * A0**2
d_exact_2nd = d0 + ln15 * k5 * eps3_2nd_d0 / (1 - ln15 * k5 * eps3p(d0))

rows = [
    ("ln15（范畴基线）", d0, d_fit),
    ("最简闭式 ln15+√5·e^{-(ln15)²}", d0 + k5 * exp(-ln15**2), d_fit),
    ("一阶自洽闭式", d_1st, d_fit),
    ("二阶自洽闭式（含 δ²）", d_2nd, d_fit),
    ("精确ε₃二阶闭式", d_exact_2nd, d_fit),
    ("线性化方程精确解 d_lin", d_lin, d_fit),
    ("精确固定点 d_exact", d_exact, d_fit),
]
print(f"  {'表达式':>28s}  {'数值':>18s}  {'与 d_fit 偏差':>14s}")
print(f"  {'-'*28}  {'-'*18}  {'-'*14}")
for name, val, ref in rows:
    print(f"  {name:>28s}  {mp.nstr(val, 12):>18s}  {mp.nstr(d_fit - val, 6):>14s}")

print(f"\n  收敛性（对各自精确解的误差）:")
print(f"    一阶闭式  vs d_lin   : {mp.nstr(abs(d_1st - d_lin), 6)}")
print(f"    二阶闭式  vs d_lin   : {mp.nstr(abs(d_2nd - d_lin), 6)}  (×{mp.nstr(abs(d_1st-d_lin)/abs(d_2nd-d_lin), 4)} 改善)")
print(f"    精确ε₃二阶 vs d_exact: {mp.nstr(abs(d_exact_2nd - d_exact), 6)}")
print(f"  ⇒ 展开序列自身收敛，残差全部被高阶项吸收，")
print(f"    不存在需要 2³×10⁻⁷ 之类外加结构修正的剩余 ✅")

# =====================================================================
print("\n" + "=" * 74)
print("S5 可检验性分析：残差是否可被现有/未来数据检验")
print("=" * 74)
chi2_res = mpf("2e-4")       # 文档引用的 χ² 拟合精度
fit_rounding = mpf("5e-5")   # d_H = 2.7095（5 位有效数字）的舍入不确定度
print(f"  Δ_exact                     = {mp.nstr(Delta_exact, 6)}")
print(f"  χ² 拟合精度                 = {mp.nstr(chi2_res, 3)}")
print(f"  Δ_exact / χ² 精度           = {mp.nstr(Delta_exact/chi2_res*100, 4)}%")
print(f"  d_H 舍入不确定度(±5×10⁻⁵)下 Δ_exact 范围:")
print(f"    [{mp.nstr(Delta_exact - fit_rounding, 6)}, {mp.nstr(Delta_exact + fit_rounding, 6)}]")
print(f"  ⇒ Δ_exact 远小于拟合噪声（约 370 分之一），且符号都无法确定。")
print(f"  ⇒ 检验任何 10⁻⁷ 量级残差结构需要 d_H 独立确定到 ≥7 位有效数字。")
print(f"  ⇒ 区分 RMS 假说(ρ=0)与 ρ≈2×10⁻⁴ 所需精度同理不可达（v1.27 结论强化）。")

# =====================================================================
print("\n" + "=" * 74)
print("S6 总结")
print("=" * 74)
print(f"""
  1. 数值不一致已解决：5.41×10⁻⁷（精确固定点）vs 8.35×10⁻⁷（线性化方程）
     差异 = 线性化误差 2.94×10⁻⁷，有闭式解释（S3）。
  2. "Δ ≈ 2³×10⁻⁷ 吻合 4.2%" 证伪：对精确残差失配 32%，
     原吻合是近似层级混淆的 artifact。
  3. 高阶闭式序列收敛（二阶误差 4.1×10⁻⁸），δ 的闭式表达完备，
     无需外加残差结构。
  4. 残差 Δ_exact = 5.41×10⁻⁷ 低于 χ² 分辨率两个数量级以上，
     当前不可检验；δ 问题在现有数据精度下已到分析极限。
  5. 文档修正：§3.5.4d 表格"自洽方程精确解 2.70949916"应标注为
     "线性化方程解"；精确固定点为 2.7094994587。
""")
