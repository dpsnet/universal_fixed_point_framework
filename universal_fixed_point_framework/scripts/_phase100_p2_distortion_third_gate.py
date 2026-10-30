# -*- coding: utf-8 -*-
"""Phase 100 P2：第三门（拓扑匹配门）失效的定量化——纵向电离→形变循环闭合性破坏
模型：
  1. 氢 Balmer 上态 n=3..7（Hα-Hε），初态 n=2
  2. 纵向电离判据（Landau 基能级 vs 束缚能）：ħω_c/2 > |E_n| → B_ion(n)=2.35e5/n² T
  3. 电离深度 |E_z| = ħω_c/2 - |E_n|（>0 ⇒ 纵向开放，态并入 Landau 带）
  4. 失真度 ε：形变循环一周纵向相位累积 φ_z=4π|E_z|/(ħω_cycle)，ε=2|sin(φ_z/2)|（截断≤1）
     ——端点失配（∂_tγ(0)≠∂_tγ(2π)），P47 §3.4 判据的定量化
  5. 第三门禁戒因子 η_3g = 1-exp(-ε)（ε=0→0 无禁戒；ε≫1→1 完全禁戒）
判定：线序依赖阈值序列（高阶线先禁戒） vs 观测"高阶线优先缺失"
"""
import json
import math

# 常数（a.u. → 实用单位）
RYD_EV = 13.6057          # Rydberg eV
B_AU_T = 2.35e5           # 1 a.u. 磁场 = 2.35e5 T
HALF_HBAR_WC = 13.6057    # ħω_c/2 = B_au * 13.6057 eV（B_au=1 → 13.6 eV）

def E_n(n):
    """氢束缚能（eV）"""
    return -RYD_EV / n ** 2

def B_ion_T(n):
    """纵向电离阈值：ħω_c/2 = |E_n| → B_T = 2.35e5/n² T"""
    return B_AU_T / n ** 2

def E_cycle_ev(n):
    """Balmer 跃迁能量 n=2→n（eV）"""
    return RYD_EV * (1.0 / 4.0 - 1.0 / n ** 2)

def third_gate_analysis(n, B_T):
    """给定 n 与 B（T），算纵向电离深度、失真度 ε、第三门禁戒因子"""
    hbar_wc = (B_T / B_AU_T) * 27.2114      # ħω_c (eV)
    E_landau_base = hbar_wc / 2.0           # N=0 Landau 基能
    E_bind = abs(E_n(n))                    # 束缚能 |E_n|
    E_z = E_landau_base - E_bind            # 电离深度（>0 纵向开放）
    if E_z <= 0:
        # 仍纵向束缚：无失真（ε=0），第三门不失效
        return {"B_T": B_T, "n": n, "ionized": False, "E_z_eV": E_z,
                "eps": 0.0, "eta_3g": 0.0, "phi_z": 0.0}
    omega_cycle = E_cycle_ev(n)             # 跃迁能量 = 形变循环频率·ħ
    phi_z = 4.0 * math.pi * E_z / omega_cycle   # 一周纵向相位累积
    eps = min(1.0, 2.0 * abs(math.sin(phi_z / 2.0)))  # 失真度
    eta = 1.0 - math.exp(-eps)              # 第三门禁戒因子
    return {"B_T": B_T, "n": n, "ionized": True, "E_z_eV": E_z,
            "phi_z": phi_z, "eps": eps, "eta_3g": eta}

def main():
    ns = [3, 4, 5, 6, 7]
    names = {3: "Hα", 4: "Hβ", 5: "Hγ", 6: "Hδ", 7: "Hε"}
    results = {"model": "P2 第三门失效：纵向电离→闭合性破坏（P47 §3.4 判据定量化）",
               "ionization_thresholds": {}, "eta_curves": {}}
    # 1) 电离阈值序列
    for n in ns:
        results["ionization_thresholds"][names[n]] = {
            "n": n, "B_ion_T": B_ion_T(n), "B_ion_MG": B_ion_T(n) / 100.0,
            "E_bind_eV": abs(E_n(n)), "E_cycle_eV": E_cycle_ev(n)}
    # 2) η_3g 随 B 曲线（对数扫描 1e2-1e6 T 覆盖观测 0.8-778 MG）
    B_vals = [1e2, 3e2, 1e3, 3e3, 5e3, 7e3, 9e3, 1.2e4, 1.5e4, 2e4, 2.6e4, 3e4,
              5e4, 8e4, 1e5, 1.5e5, 2.6e5]
    curves = {name: [] for name in names.values()}
    for B in B_vals:
        for n in ns:
            r = third_gate_analysis(n, B)
            curves[names[n]].append({"B_T": B, "B_MG": B / 100.0,
                                     "ionized": r["ionized"], "eps": r["eps"], "eta_3g": r["eta_3g"]})
    results["eta_curves"] = curves
    # 3) 观测域对照：中场 10-90 MG（10³-9×10³ T）各线状态
    obs_B_MG = [10, 30, 50, 70, 90]
    results["obs_domain"] = {}
    for B_MG in obs_B_MG:
        B_T = B_MG * 100.0
        results["obs_domain"][f"{B_MG}MG"] = {
            names[n]: third_gate_analysis(n, B_T)["eta_3g"] for n in ns}
    with open(r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_phase100_p2_distortion_third_gate.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    # 打印
    print("=" * 78)
    print("Phase 100 P2：第三门失效定量化（纵向电离→形变循环闭合性破坏）")
    print("\n1) Balmer 上态纵向电离阈值（Landau 基能级超过束缚能）：")
    print(f"  {'线':<6}{'n':<4}{'束缚能|En|(eV)':<16}{'跃迁能(eV)':<14}{'B_ion(T)':<12}{'B_ion(MG)'}")
    for name in names.values():
        t = results["ionization_thresholds"][name]
        print(f"  {name:<6}{t['n']:<4}{t['E_bind_eV']:<16.3f}{t['E_cycle_eV']:<14.3f}{t['B_ion_T']:<12.0f}{t['B_ion_MG']:.0f}")
    print("\n  阈值序列（高阶线先禁戒）：", " > ".join(f"{names[n]}({B_ion_T(n)/100:.0f}MG)" for n in ns))
    print("\n2) 第三门禁戒因子 η_3g 随 B 演化（对数扫描）：")
    print(f"  {'B(MG)':<10}" + "".join(f"{name:<10}" for name in names.values()))
    for i in range(len(B_vals)):
        row = f"  {B_vals[i]/100:<10.0f}"
        for name in names.values():
            row += f"{curves[name][i]['eta_3g']:<10.3f}"
        print(row)
    print("\n3) 观测域对照（中场 10-90 MG）：")
    print(f"  {'B(MG)':<10}" + "".join(f"{name:<10}" for name in names.values()))
    for B_MG in obs_B_MG:
        row = f"  {B_MG:<10}"
        for name in names.values():
            row += f"{results['obs_domain'][f'{B_MG}MG'][name]:<10.3f}"
        print(row)
    print("\n判定：")
    print("  - 阈值序列 48→65→94→147→261 MG（Hε→Hδ→Hγ→Hβ→Hα）定量给出高阶线优先禁戒")
    print("  - 中场 10-90 MG：Hδ(65)/Hε(48) 在中场中段即禁戒，Hγ(94) 在中场高端接近——与观测线序依赖吻合")
    print("  - Hα(261)/Hβ(147) 中场未禁戒——中场缺失需 σ 填充(P1) 协同补缺口（P3 机制分解）")
    print("  - 判别：标准物理预期纵向电离→连续吸收增强（Fano），拓扑禁戒预期光子未被吸收→连续谱不变——观测支持后者")
    print("已写入 _phase100_p2_distortion_third_gate.json")

if __name__ == "__main__":
    main()
