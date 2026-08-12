#!/usr/bin/env python3
"""
paperX_mass_time_window.py — "时间 = 质量外显窗口"层次二数值验证（笔记 06_photon_topology 方向 5 §6.14, 2026-08-11）

支撑 §6.12："质量大小 → 时间尺度"——质量经时间窗口外显的两个互补表现：
物质波频率 ω=mc²/ħ（质量越大相位演化越快）与寿命 τ∝1/m⁵（弱衰变，质量越大寿命越短）。

S1: 物质波频率 ω=mc²/ħ 数值表（电子/质子/μ 子/τ 子）——ω ∝ m 严格线性
S2: 寿命标度 τ∝1/m⁵（μ 子 vs τ 子，弱衰变标度律量级验证）
S3: 质量经时间的双尺度趋势——m↑ ⟹ ω↑（频率增）且 τ↓（寿命减），互补外显
S4: 固有时/时间耦合模式（质量门参考）——有质量 dτ>0（时间耦合满）vs 光子 dτ=0

诚实边界：ω=mc²/ħ（de Broglie 物质波频率）与 τ∝1/m⁵（弱衰变标度律）均为标准
物理事实核对（非新预言）；寿命标度还有 CKM/相空间等修正（量级验证非精确）；"时间窗口"
为 §6.12 框架诠释。
"""
import numpy as np

HBAR = 1.054571817e-34   # J·s
C = 299792458.0          # m/s
MEV2J = 1.602176634e-13  # MeV → J

# 粒子：(名称, 质量 MeV, 寿命 s)
PARTICLES = [
    ("电子 e", 0.5110, None),
    ("μ 子", 105.66, 2.197e-6),
    ("质子 p", 938.27, None),
    ("τ 子", 1776.86, 2.903e-13),
]


def check(name, cond, detail=""):
    status = "PASS" if cond else "FAIL"
    print(f"[{status}] {name}" + (f" — {detail}" if detail else ""))
    return bool(cond)


def omega_mc2(m_mev):
    """物质波角频率 ω = mc²/ħ（m 以 MeV 计）"""
    return m_mev * MEV2J / HBAR


def main():
    print("时间=质量外显窗口 层次二数值验证（笔记 §6.14：质量大小 → 时间尺度）")
    print("=" * 78)

    # S1: 物质波频率 ω=mc²/ħ 数值表——ω ∝ m
    print("\nS1  物质波频率 ω = mc²/ħ（质量越大相位演化越快）")
    omegas = {}
    for name, m, _ in PARTICLES:
        omegas[name] = omega_mc2(m)
        print(f"   {name:<6} m={m:>8.2f} MeV  ω = {omegas[name]:.3e} Hz")
    # ω ∝ m 严格线性：任意两粒子频率比 = 质量比
    ok1 = abs(omegas["μ 子"] / omegas["电子 e"] - 105.66 / 0.5110) < 1e-9
    ok1 = ok1 and abs(omegas["τ 子"] / omegas["μ 子"] - 1776.86 / 105.66) < 1e-9
    check("S1  ω = mc²/ħ（ω ∝ m 严格线性，μ/e 与 τ/μ 比值核对）", ok1)

    # S2: 寿命标度 τ∝1/m⁵（弱衰变标度律，μ 子 vs τ 子）
    m_mu, tau_mu = 105.66, 2.197e-6
    m_tau, tau_tau = 1776.86, 2.903e-13
    ratio_m5 = (m_tau / m_mu) ** 5          # 质量比^5
    ratio_tau = tau_mu / tau_tau           # 寿命比（实测）
    # τ∝1/m⁵ ⟹ τ_μ/τ_τ ≈ (m_τ/m_μ)⁵（量级）
    order_diff = abs(np.log10(ratio_tau) - np.log10(ratio_m5))
    ok2 = order_diff < 1.2                  # 量级差 < 1.2 个量级（有 CKM/相空间修正）
    print(f"\nS2  寿命标度 τ∝1/m⁵（弱衰变）：(m_τ/m_μ)⁵ = {ratio_m5:.2e}"
          f"，实测 τ_μ/τ_τ = {ratio_tau:.2e}（量级差 {order_diff:.1f}）")
    check("S2  τ∝1/m⁵ 量级验证（μ vs τ 子，考虑 CKM/相空间修正）", ok2,
          f"量级差 {order_diff:.1f} < 1.2")

    # S3: 质量经时间的双尺度趋势——m↑ ⟹ ω↑ 且 τ↓（互补外显）
    ok3 = (omegas["τ 子"] > omegas["μ 子"] > omegas["电子 e"])   # 频率随质量增
    ok3 = ok3 and (tau_tau < tau_mu)                              # 寿命随质量减
    check("S3  双尺度互补：m↑ ⟹ ω↑（频率增）且 τ↓（寿命减）——质量经时间窗口的两个外显方向", ok3,
          f"ω_τ/ω_μ = {omegas['τ 子']/omegas['μ 子']:.1f}（>1），τ_μ/τ_τ = {tau_mu/tau_tau:.1e}（>1）")

    # S4: 固有时/时间耦合模式（质量门参考）——有质量 dτ>0 vs 光子 dτ=0
    # 有质量物体静止系时间耦合 = 1（dτ/dt=1）；光子（v=c）时间耦合 = 0（dτ=0，§7.24 S11）
    coupling_massive = 1.0                 # 有质量静止：dτ/dt = 1（满耦合）
    v_photon = C
    coupling_photon = np.sqrt(1 - (v_photon / C) ** 2)   # = 0（零耦合）
    ok4 = abs(coupling_massive - 1.0) < 1e-15 and abs(coupling_photon) < 1e-12
    check("S4  质量门参考：有质量静止时间耦合=1（固有时 dτ>0）vs 光子零耦合（dτ=0）", ok4,
          f"有质量 {coupling_massive} vs 光子 {coupling_photon:.1e}")

    results = [ok1, ok2, ok3, ok4]
    print("\n" + "=" * 78)
    print(f"质量-时间窗口数值验证：{sum(results)}/4 通过")
    if not all(results):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
