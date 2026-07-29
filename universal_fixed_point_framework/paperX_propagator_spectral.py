#!/usr/bin/env python3
"""
paperX_propagator_spectral.py — A4：等效传播子修正的定量形式（2026-07-29）

回答 §9.4a A4（§5.7f.4）："标准引力子传播子 ~1/k² 在 k ~ M_Pl 附近
将出现由 Δλ_min 决定的偏离"的定量形式。

构造（离散谱塔模型）：
  D(k²) = 1/k² + g_eff · Σ_{n=1}^{8} 1/(k² + λ_n²)   （Planck 单位，λ₈ = 1 = M_Pl）
  g_eff = ‖Δ‖_F² = r_cat·Δλ_min² ≈ 6.01×10⁻⁴（塔模式耦合 = coherence 偏差强度）

谱矩闭式（λ_n² = n(n+1)/72）：
  S₂ = Σ 1/λ_n² = 72·Σ(1/n − 1/(n+1)) = 72·8/9 = **64**（精确闭式）
  S₄ = Σ 1/λ_n⁴ ≈ 1500.31，比值 S₄/S₂ ≈ 23.44

关键结果：
  - 低 k 展开：D(k²) = 1/k² + 64·g_eff·(1 − 23.44·k² + O(k⁴))
    ⇒ 接触项系数 α = −64·g_eff ≈ −0.0385（1/(k²(1+αk²)) 形式）
  - 精确谱和：偏离比 R(k²) = g_eff·k²·S(k²)，高 k 饱和于 8·g_eff ≈ 0.48%
  - 起始标度：k ~ λ₁·M_Pl ≈ 0.17 M_Pl（第一个塔模式）
  - 自相互作用截断（§5.7f.4 原式）：E ~ ‖Δ‖_F·M_Pl ≈ 0.0245 M_Pl
"""

import numpy as np

k_arr = np.arange(1, 9)
lam2 = k_arr * (k_arr + 1) / 72.0   # λ_n²（λ₈ = 1 = M_Pl，Planck 单位）
r_cat = 0.040391
DL = 0.122022
g = r_cat * DL**2

print("=" * 74)
print("S1 谱矩闭式验证")
print("=" * 74)
S2 = np.sum(1 / lam2)
S4 = np.sum(1 / lam2**2)
S2_closed = 72 * 8 / 9
print(f"  S₂ = Σ 1/λ_n² = {S2:.10f}")
print(f"  闭式 72·(1 − 1/9) = {S2_closed:.10f}  一致: {abs(S2-S2_closed) < 1e-12} ✅")
print(f"  S₄ = Σ 1/λ_n⁴ = {S4:.4f}")
print(f"  比值 S₄/S₂ = {S4/S2:.4f}（k² 项的曲率系数）")

print("\n" + "=" * 74)
print("S2 低 k 展开与接触项系数 α")
print("=" * 74)
print(f"  D(k²) = 1/k² + g·(S₂ − S₄·k² + O(k⁴))")
print(f"        = 1/k² + 64·g·(1 − 23.44·k² + ...)")
print(f"  g_eff = r_cat·Δλ_min² = {g:.6e}")
alpha = -64 * g
print(f"  接触项形式 1/(k²(1+αk²/M_Pl²)): α = −64·g_eff = {alpha:.6f} M_Pl²")
print(f"  （α < 0：谱塔修正为**吸引方向增强**，与 A1 的 NLO 恒正一致）")

print("\n" + "=" * 74)
print("S3 精确谱和：偏离比曲线 R(k²) = g·k²·S(k²)")
print("=" * 74)
S = lambda k2: np.sum(1 / (k2 + lam2))
R = lambda k2: g * k2 * S(k2)
print(f"  {'k/M_Pl':>8s}  {'k²':>10s}  {'S(k²)':>10s}  {'R = 偏离比':>12s}  {'低 k 展开':>12s}")
for k in [0.05, 0.1, 0.167, 0.3, 0.5, 1.0, 2.0, 10.0]:
    k2 = k * k
    print(f"  {k:8.3f}  {k2:10.4f}  {S(k2):10.3f}  {R(k2):12.4e}  {64*g*k2:12.4e}")
R_sat = 8 * g
print(f"\n  高 k 饱和值: R → 8·g_eff = {R_sat:.4e}（{R_sat*100:.2f}%）")
print(f"  ⇒ 传播子偏离**有界**：任何能标下不超过 {R_sat*100:.2f}%")
print(f"  起始标度（R ≈ 0.1%）: k ≈ λ₁·M_Pl = {np.sqrt(lam2[0]):.3f} M_Pl（第一个塔模式）")
print(f"  注: 低 k 展开在 k² > λ₁² = {lam2[0]:.4f} 后失效——")
print(f"      '1% 偏离'的朴素展开估计不适用，精确饱和值为 {R_sat*100:.2f}%")

print("\n" + "=" * 74)
print("S4 修正幅度上限的来源分析")
print("=" * 74)
print(f"""  偏离上限 = 8·g_eff = 8·r_cat·Δλ_min² = {R_sat:.4e}
  物理解读: 引力子传播子的谱塔修正在所有能标下 ≤ {R_sat*100:.2f}%。
  失效模式是**小幅单调饱和**而非截断发散——
  §5.7f.4 的"等效传播子在 k ~ M_Pl 处偏离"定量化为:
    起始 k ~ {np.sqrt(lam2[0]):.2f} M_Pl，饱和 {R_sat*100:.2f}%（k ≫ M_Pl）。""")

print("\n" + "=" * 74)
print("S5 自相互作用截断（§5.7f.4 第 2 条）")
print("=" * 74)
DeltaF = np.sqrt(g)
print(f"  ‖Δ‖_F = √(r_cat)·Δλ_min = {DeltaF:.6f}")
print(f"  §5.7f.4: 引力子自相互作用在 E ~ ‖Δ‖_F·M_Pl 处偏离微扰展开")
print(f"  ⇒ E_cutoff ≈ {DeltaF:.4f} M_Pl ≈ M_Pl / {1/DeltaF:.0f}")
print(f"  锐利预测: 引力 EFT 的自耦合微扰展开在 ~{DeltaF:.2f} M_Pl")
print(f"  （远低于 M_Pl）开始失效——比传播子通道（0.17 M_Pl 起始）更早")

print("\n" + "=" * 74)
print("S6 结论与诚实标注")
print("=" * 74)
print(f"""
  A4 判定（模型化级别闭合）:

  定量形式（Planck 单位）:
    D(k²) = 1/k² + g_eff·Σₙ 1/(k² + λ_n²),  g_eff = r_cat·Δλ_min² = {g:.2e}
    低 k: D(k²) ≈ 1/(k²(1 + αk²/M_Pl²)),  α = −64·g_eff = {alpha:.4f}

  硬结构数（范畴结构直接给出，无建模自由度）:
    S₂ = Σ 1/λ_n² = 64（精确闭式 72·8/9）
    S₄/S₂ = 23.44（k² 曲率系数）

  可证伪定量预测:
    传播子通道: 偏离起始 k ~ 0.17 M_Pl，饱和 {R_sat*100:.2f}%（有界）
    自耦合通道: EFT 失效 E ~ {DeltaF:.4f} M_Pl（锐利，远早于 M_Pl）

  诚实标注（模型化级别）:
  - g_eff = r_cat·Δλ_min²（塔耦合 = coherence 偏差强度）是建模指派;
    权重 w_n = 1（每特征值简并度 1）是基线选择;
  - 动量空间表述预设涌现时空 Fourier 变换（B1④/B2 依赖）——
    与 paper18"正比于"同级，非第一性推导;
  - 硬数（64、23.44、饱和上限 8·g_eff）不依赖上述指派，
    改变权重只改 g_eff 的有效值，不改谱矩闭式。
""")
