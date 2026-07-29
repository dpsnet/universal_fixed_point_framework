#!/usr/bin/env python3
"""
paperX_gw_observables.py — C1：引力波异常信号的具体定义（2026-07-29）

回答 §9.4a C1：将 A1-A4 的结构结果翻译成可观测量
（信号通道、幅度、现有约束、可行性）。

核心结论（剧透）：**负结果闭合**——框架的引力波异常信号
在所有可达能标下要么被现有多信使约束排除到不可见，
要么位于 Planck 标度不可达区。框架的 GW 扇区在实践中
与 GR 不可区分；其可证伪性落在非 GW 通道
（三组无量纲比率 §5.4b、L_4 ≈ 1470 GeV、QNM 2.03%）。
"""

import numpy as np

c_light = 2.998e8          # m/s
Mpc_m = 3.086e22           # m
M_Pl_GeV = 2.435e18        # GeV
h_GeVs = 4.136e-24         # GeV·s（ℏ）

print("=" * 74)
print("通道 1：双折射到达时间差（A3 + paperX_gw_polarization.py）")
print("=" * 74)
# 关系: δc/c = δ‖Δ‖_F/‖Δ‖_F（弹性介质类比，波速 ∝ √(剪切模量)）
# GW170817/GRB170817A: 1.74 s / 40 Mpc ⇒ |Δv/c| < ~5×10⁻¹⁶
D_m = 40 * Mpc_m
T_travel = D_m / c_light          # 穿越时间 (s)
bound_dvc = 1.74 / T_travel       # GW170817 速度约束
print(f"  GW170817: 40 Mpc, Δt_EM-GW = 1.74 s")
print(f"  速度约束 |δc/c| < {bound_dvc:.1e}")
print(f"\n  框架结构约束（§5.7h/paperX_gw_polarization.py）:")
print(f"    3 层同范畴 ⇒ 各向异性为二阶效应, 估计上界 δ‖Δ‖/‖Δ‖ < 10⁻⁴")
print(f"  ⇒ 若各向异性 δ‖Δ‖/‖Δ‖ ~ 10⁻⁴ 实现为速度差:")
print(f"    Δt = D/c × 10⁻⁴ = {T_travel*1e-4:.2e} s ≈ {T_travel*1e-4/3.15e7:.0f} 年")
print(f"    ——早已被多信使观测排除")
print(f"\n  ★ 判定: 双折射通道被 GW170817 关闭——")
print(f"    框架要求各向异性 η < {bound_dvc:.0e}（比结构估计 10⁻⁴ 严 11 个数量级）,")
print(f"    框架的自然工作点（引力扇区 X.A = Y.A = Z.A = A_GR，§5.7a）")
print(f"    给出 η = 0 精确 ⇒ 双折射恒等于零 ⇒ **观测不可达**")

print("\n" + "=" * 74)
print("通道 2：极化含量（A3）")
print("=" * 74)
print(f"""  框架预测: 恰好 2 个张量模式（Moran 冻结呼吸 + 通量守恒横向性）
  现有检验: GW170814/GW170817 极化分析 —— 与纯张量一致 ✅
  与 GR 的关系: 不可区分（同为 2 模式）
  与其他理论: 排除标量-张量（3 模式）/有质量引力（5 模式）——
              但这与 GR 的排除力相同，非框架独有
  ★ 判定: 通过但与 GR 不可区分——该通道不提供框架特有信号""")

print("\n" + "=" * 74)
print("通道 3：传播子修正的波形效应（A4）")
print("=" * 74)
g_eff = 0.040391 * 0.122022**2
for f_Hz, band in [(100, "LIGO 带"), (1e4, "高频 GW"), (1e16, "暴胀子尺度（原初 GW)")]:
    E_GeV = h_GeVs * f_Hz * 2 * np.pi
    k = E_GeV / M_Pl_GeV
    k2 = k * k
    lam2 = k_arr = np.arange(1, 9) * (np.arange(1, 9) + 1) / 72.0
    S = np.sum(1 / (k2 + lam2))
    R = g_eff * k2 * S
    print(f"  {band:>22s}: f = {f_Hz:.0e} Hz, k = {k:.1e} M_Pl, R = {R:.1e}")
print(f"  （高 k 饱和上限 = 8·g_eff = {8*g_eff:.2e} = 0.48%）")
print(f"\n  ★ 判定: LIGO 带修正 ~10⁻⁸¹——绝对不可达;")
print(f"    即使原初 GW（k ~ M_Pl）也只有 ≤0.48% 的传播修正,")
print(f"    低于可预见的 CMB B 模/脉冲星计时阵探测能力")

print("\n" + "=" * 74)
print("通道 4：EFT 自耦合截断（A4）")
print("=" * 74)
E_cut = np.sqrt(g_eff)
print(f"  E_cutoff = ‖Δ‖_F·M_Pl = {E_cut:.4f} M_Pl = {E_cut*M_Pl_GeV:.2e} GeV")
print(f"  对比: LHC 质心能量 ~10⁴ GeV, LIGO 相关强场曲率标度 ≪ 10¹⁰ GeV")
print(f"  ★ 判定: 锐利的理论陈述（EFT 适用范围上界）,")
print(f"    但高出任何可及实验标度 ~{E_cut*M_Pl_GeV/1e4:.0e} 倍——无观测通道")

print("\n" + "=" * 74)
print("通道 5/6：既有结果与退相干")
print("=" * 74)
print(f"""  通道 5（QNM ringdown）: Kerr QNM 谱偏差 2.03%（paper5 §4.1）
    ——已有结果, 与 GR 一致 ✅
  通道 6（引力-量子退相干）: ‖[A_GR, A_SM]‖/... ~ 10⁻²¹（paper5 §4.4）
    ——Planck 标度抑制, 不可达""")

print("\n" + "=" * 74)
print("C1 总结：观测信号字典")
print("=" * 74)
print(f"""  {'通道':<18s}  {'幅度':<12s}  {'现有约束/状态':<22s}  {'判定':<14s}
  {'1 双折射 Δt':<18s}  {'η=0(工作点)':<12s}  {'GW170817: η<5×10⁻¹⁶':<22s}  {'关闭':<14s}
  {'2 极化含量':<18s}  {'2 张量模式':<12s}  {'LIGO 极化检验一致':<22s}  {'同 GR':<14s}
  {'3 传播子修正':<18s}  {'≤0.48%':<12s}  {'LIGO 带 ~10⁻⁸¹':<22s}  {'不可达':<14s}
  {'4 EFT 截断':<18s}  {'0.0245 M_Pl':<12s}  {'超 LHC 标度 6×10¹²':<22s}  {'理论陈述':<14s}
  {'5 QNM':<18s}  {'2.03%':<12s}  {'ringdown 一致':<22s}  {'同 GR':<14s}
  {'6 退相干':<18s}  {'~10⁻²¹':<12s}  {'—':<22s}  {'不可达':<14s}

  ★ C1 最终判定（负结果闭合）:
    §5.7e/f 设想的"引力波异常信号"经定量化后**不存在近中期
    观测通道**——框架的 GW 扇区在一切可达能标下与 GR 不可区分。
    框架的可证伪性落在非 GW 通道:
    - 三组无量纲比率（§5.4b: ε、M_Pl/M_SM、α_Gravity/α_SU(2)）
    - L_4 ≈ 1470 GeV（HL-LHC/FCC-hh）
    - Kerr QNM 2.03%（已一致）
    - 质子寿命 τ_p ~ 10³⁴⁻³⁶ 年（Hyper-K、DUNE）
    
  诚实价值: 该负结果排除了一个此前被寄予希望的证伪通道,
  使框架的可证伪资源地图完整化——
  "引力波异常"不再是未决问题, 而是已量化的关闭通道。
""")
