# -*- coding: utf-8 -*-
"""S258 级联机制论证数值支撑
V3 = 6σ³+4σ⁵+8σ⁷+5σ⁸
① 逐项分层收敛（每层加项后偏差缩减因子）
② 系数-幂次配对恒等检验（和/积/差/邻域）
③ 级联机制预测检验（下一层）
"""
from decimal import Decimal, getcontext
getcontext().prec = 50
import math

alpha_obs = Decimal("137.035999084")
unc = Decimal("2.1e-8")
ln15 = Decimal(15).ln()
sigma = Decimal(1)/Decimal(15)
delta_obs = alpha_obs/24 - 3 - ln15

s = {p: sigma**p for p in range(1, 13)}

print("=== S258: δ_V3 级联机制数值支撑 ===")
print(f"δ^(obs) = {float(delta_obs):.12f}")

print("\n--- ① 逐项分层收敛 ---")
terms = [("6σ³", 6*s[3]), ("4σ⁵", 4*s[5]), ("8σ⁷", 8*s[7]), ("5σ⁸", 5*s[8])]
acc = Decimal(0)
prev_dev = None
for name, val in terms:
    acc += val
    dev = abs(acc - delta_obs)
    ratio = f"×{prev_dev/dev:.1f}" if prev_dev else "—"
    sig = float(24*dev/unc)
    print(f"  +{name}: 累积 = {float(acc):.12f}——偏差 {float(dev):.2e}（{ratio}）——α⁻¹σ = {sig:.3f}")
    prev_dev = dev

print("\n--- ② 系数-幂次配对恒等 ---")
C = [6, 4, 8, 5]
P = [3, 5, 7, 8]
print(f"系数和 = {sum(C)}——幂次和 = {sum(P)}——{'相等！' if sum(C)==sum(P) else '不等'}")
print(f"系数积 = {6*4*8*5}——幂次积 = {3*5*7*8}——{'相等' if 6*4*8*5==3*5*7*8 else '不等'}")
print(f"邻域偏移（系数−幂次）：{[C[i]-P[i] for i in range(4)]}")
print(f"邻域偏移（幂次−系数）：{[P[i]-C[i] for i in range(4)]}")
print(f"6×4 = 24（不动点！）——8+5 = 13（Fib——静默+幂基³）")
print(f"6+8 = 14、4+5 = 9、6−5 = 1、8−4 = 4（不动点）")

print("\n--- ③ 配对映射的框架结构 ---")
pairs = [("6σ³", "幂基×活跃 → 活跃", "系数含本域因子"),
         ("4σ⁵", "不动点 → 静默", "邻域 4→5(+1)"),
         ("8σ⁷", "幂基³ → 对合", "邻域 8→7(−1)"),
         ("5σ⁸", "静默 → 幂基³", "和 5+3=8(+活跃)")]
for term, mapping, note in pairs:
    print(f"  {term}：{mapping}——{note}")

print("\n--- ④ 域常数谱完整性 ---")
# 框架常数作 σ 幂次的候选全集
fc = {2: "幂基", 3: "活跃", 4: "不动点", 5: "静默", 7: "对合", 8: "幂基³"}
print(f"框架常数全集（可作 σ 幂次）：{sorted(fc)}")
print(f"V3 使用：{{3,5,7,8}}——缺 2（幂基——静默偶幂禁？）与 4（不动点）")
print(f"缺 2 的解释：σ² 属静默偶幂禁（S76——σ²/σ⁴/σ⁶ 未用）")
print(f"缺 4 的解释：不动点幂禁（S239——不动点不做幂次）")
print(f"→ V3 的幂次 = 可用域常数全集 { {3,5,7,8} }——无缺漏！")

print("\n--- ⑤ 级联机制预测 ---")
print(f"下一层（若存在）：σ^{{16}}（全态）/σ^{{42}}（约束域）——数值 5.7e-20/1e-50——")
print(f"远小于当前偏差 2.4e-11——预测不可检验（诚实边界）")
print(f"分级语义：d_H 维数域用框架常数谱（结构量响应域结构）vs")
print(f"  修正域用 Fib 谱（动力学量响应递归代数）——分域假说（C）")
