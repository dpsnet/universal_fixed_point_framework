# -*- coding: utf-8 -*-
"""数值探索：每步 Δφ 取值候选（衔接层开放项，先证伪/择优）

三层时间分层桥（已机检）：递归 n 步 → rapidity n·Δφ → θ_n = arcsin(tanh(n·Δφ))。
每步 Δφ 的取值是"范畴公设→数值"链的命门之一，候选互斥（异路），按协议分别探索。

候选（异路，互斥取值）：
  C1 翻倍说：Δφ = ln 2（每次递归翻倍）——tanh(ln2)=3/5 ⟹ 3-4-5 勾股、v=0.6c
  C2 谱隙说：Δφ 由谱隙锚定（cosh Δφ − 1 = Δλ_min，谱隙=(√3−1)/6≈0.1220）
  C3 窗口说：Δφ = d_H（静默窗口尺度 w=e^{−d_H}，d_H 判别值 16259/6000≈2.7098）
  C4 次第闭合说：Δφ = (1/4)·ln g = (1/4)·ln 15（g=15 每静默方向平均权重）
  C5 单位说：Δφ = 1（单步单位 rapidity）

判据：
  (i)   可识别结构（勾股整数/谱隙/窗口/15）——偏好简单闭合
  (ii)  与已机检锚相容：谱隙 Δλ_min=(√3−1)/6、静默窗口 e^{−d_H}、g=15
  (iii) d_H 与 ln 15 的接近度（若 d_H=ln15 ⟹ 窗口=1/15 与 g=15 直接咬合）
"""
import numpy as np

d_H = 16259 / 6000
ln15 = np.log(15)
ln16 = np.log(16)
gap = (np.sqrt(3) - 1) / 6

print("=== 锚点核对 ===")
print(f"d_H (判别值)      = {d_H:.10f}")
print(f"ln 15             = {ln15:.10f}")
print(f"ln 16             = {ln16:.10f}")
print(f"Δλ_min (谱隙)     = {gap:.10f}")
print(f"24(d_H+3)         = {24*(d_H+3):.6f}  (路径A α⁻¹ 命中口径)")
print(f"24(ln15+3)        = {24*(ln15+3):.6f}")
print(f"α⁻¹ (CODATA 2018) = {137.035999084:.6f}")
print(f"|d_H−ln15|        = {abs(d_H-ln15):.2e}  相对 {abs(d_H-ln15)/ln15*100:.4f}%")
print()

cands = {
    "C1 翻倍 ln2": np.log(2),
    "C2 谱隙 (coshΔφ−1=Δλ)": np.arccosh(1 + gap),
    "C3 窗口 d_H": d_H,
    "C4 次第闭合 (ln15)/4": ln15 / 4,
    "C5 单位 1": 1.0,
}
print("=== 候选扫描 ===")
print(f"{'候选':<26} {'Δφ':>12} {'cosh Δφ':>12} {'γ=cosh':>12} {'v/c=tanh':>12} {'θ₁(°)':>10} {'sech(红移)':>12}")
for name, dphi in cands.items():
    c = np.cosh(dphi)
    v = np.tanh(dphi)
    th = np.degrees(np.arcsin(v))
    red = 1.0 / c
    print(f"{name:<26} {dphi:12.6f} {c:12.6f} {c:12.6f} {v:12.6f} {th:10.4f} {red:12.6f}")

print()
print("=== 结构判据（可识别闭合）===")
print("C1: tanh(ln2)=3/5 ⟹ 3-4-5 勾股 (sinθ=3/5, cosθ=4/5, γ=5/4) — 纯整数比例")
print(f"C2: coshΔφ−1=Δλ_min={gap:.6f} — 谱隙直接锚定，Δφ={np.arccosh(1+gap):.6f}")
print(f"C3: w=e^{{-d_H}}=1/{np.exp(d_H):.6f} ≈ 1/15? 1/15={1/15:.6f}")
print(f"C4: Δφ=ln15/4, 4步累积=ln15 ⟹ n=4 时 cosh=cosh(ln15)≈{(np.cosh(ln15)):.4f}, 偏转代价 K=m(γ−1)=m(15+1/15)/2−m")
print()
print("=== 判据 (iii)：d_H 与 ln15 ===")
print("d_H=2.709833 vs ln15=2.708050：差 0.18%（非精确相等，但同量级接近）")
print("若 d_H=ln15 精确：24(ln15+3)=136.993 vs α⁻¹=137.036：差 0.03%（更近但非精确命中）")
print("→ d_H=ln15 作为精确链未获支持（判别值 16259/6000 与 ln15 不相等）；")
print("  但'静默窗口 ∝ 1/15'的咬合方向（e^{−d_H}≈1/15）成立级接近，登记观察。")
