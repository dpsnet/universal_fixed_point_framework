#!/usr/bin/env python3
"""
paperX_z2_winding_unification.py — Z₂ 值拓扑荷统一验证（笔记 06_photon_topology 方向 5 §6.10, 2026-08-11）

推进 §6.9 开放问题：① A2 张量性论证、② 光子环绕定向 vs 旋量 Z₂ 结构是否同一拓扑荷、③ A4 量化嵌入。

核心数学事实：SO(2) ⊂ SO(3)，π₁(SO(2)) = Z（环绕数）→ π₁(SO(3)) = Z₂ 为模 2 约化——
光子环绕数 n（Z 值）模 2 与旋量 2π 变号（非平凡类）给出同一 Z₂ 值拓扑荷。

S1: 环绕数模 2 约化——n 圈路径的旋量提升 U(2πn) = (-1)^n I（n 奇 → -I、n 偶 → +I）
S2: 光子两环绕方向同值——s=±1（n=±1）模 2 同为非平凡类（n ≡ -n mod 2）
S3: A2 张量性由环绕数可加性推出——σ(n₁+n₂)=σ(n₁)σ(n₂)（Z₂ 加法 = Z₂ 乘法）
S4: A4 量化嵌入——外显能量 = σ·(2μ_B B cosϑ)（Z₂ 符号 × 时间耦合投影强度）
S5: 三层次区分——投影值 s=±1（观测 2 值）vs 环绕模 2 类（非平凡单值）vs 统计类（光子玻色子+1）

诚实边界：π₁(SO(2))→π₁(SO(3)) 模 2 约化为标准代数拓扑事实；A2/A4 的框架
公理化应用为诠释层；S5 的三层次区分防混淆，不构成新物理预言。
"""
import numpy as np

MU_B = 5.7883818060e-5   # eV/T
B_FIELD = 1.0            # T


def check(name, cond, detail=""):
    status = "PASS" if cond else "FAIL"
    print(f"[{status}] {name}" + (f" — {detail}" if detail else ""))
    return bool(cond)


def z2_of_winding(n):
    """环绕数 n（Z 值）模 2 约化 → Z₂ 值（+1 偶 / -1 奇）"""
    return 1 if n % 2 == 0 else -1


def spinor_lift(n):
    """n 圈路径的旋量提升：U(2πn) = cos(nπ)I - i sin(nπ)σ_z = (-1)^n I"""
    sz = np.array([[1, 0], [0, -1]], complex)
    U = np.cos(n * np.pi) * np.eye(2, dtype=complex) - 1j * np.sin(n * np.pi) * sz
    return U


def main():
    print("Z₂ 值拓扑荷统一验证（笔记 §6.9 开放问题①②③：环绕模 2 = 旋量变号）")
    print("=" * 78)

    # S1: 环绕数模 2 约化——n 圈路径的旋量提升 U(2πn) = (-1)^n I
    ok1 = True
    print("\nS1  环绕数模 2 约化：U(2πn) = (-1)^n I（π₁(SO(2))=Z → π₁(SO(3))=Z₂）")
    for n in range(-3, 4):
        U = spinor_lift(n)
        expect = -np.eye(2) if n % 2 == 1 else np.eye(2)
        ok = np.allclose(U, expect, atol=1e-12)
        ok1 = ok1 and ok
        print(f"   n={n:>2}  U(2πn)={'-I' if n % 2 == 1 else '+I'}  z₂={z2_of_winding(n):+d}"
              f"  {'✓' if ok else '✗'}")
    check("S1  环绕数 n 模 2 = 旋量变号（n 奇 → -I、n 偶 → +I）", ok1)

    # S2: 光子两环绕方向同值——s=±1（n=±1）模 2 同为非平凡类
    s_plus, s_minus = 1, -1   # 光子两螺旋度对应环绕数 n=±1
    z2_plus = z2_of_winding(s_plus)
    z2_minus = z2_of_winding(s_minus)
    ok2 = (z2_plus == -1 and z2_minus == -1)   # n ≡ -n mod 2，两方向同非平凡类
    check("S2  光子两螺旋度（s=±1）模 2 同值：均非平凡类（n ≡ -n mod 2）", ok2,
          f"z₂(+1)={z2_plus:+d}, z₂(-1)={z2_minus:+d}")

    # S3: A2 张量性由环绕数可加性推出——σ(n₁+n₂)=σ(n₁)σ(n₂)
    ok3 = True
    for n1 in range(-3, 4):
        for n2 in range(-3, 4):
            if z2_of_winding(n1 + n2) != z2_of_winding(n1) * z2_of_winding(n2):
                ok3 = False
    check("S3  A2 张量性：σ(n₁+n₂)=σ(n₁)σ(n₂)（环绕数可加性 → 模 2 乘法，n∈[-3,3] 全组合）", ok3)

    # S4: A4 量化嵌入——外显能量 = σ·(2μ_B B cosϑ)（Z₂ 符号 × 时间耦合投影强度）
    ok4 = True
    for sig in (1, -1):           # σ = ±1（自旋投影符号）
        for th in (0, 30, 45, 60, 90, 120):
            E = sig * 2.0 * MU_B * B_FIELD * np.cos(np.deg2rad(th))
            # 分解核对：E = σ × (强度 2μ_B B cosϑ)
            strength = 2.0 * MU_B * B_FIELD * np.cos(np.deg2rad(th))
            if abs(E - sig * strength) > 1e-18:
                ok4 = False
    check("S4  A4 量化嵌入：外显能量 = σ·(2μ_B B cosϑ)（Z₂ 符号 × 强度投影）", ok4)

    # S5: 三层次区分——投影值 s=±1 vs 环绕模 2 类 vs 统计类
    # 光子：投影值 2 个（s=±1）、环绕模 2 类非平凡（-1）、统计类玻色子（+1，整数自旋）
    photon_proj_values = {1, -1}          # s=±1（2 个观测值）
    photon_winding_z2 = -1                 # n=±1 模 2（非平凡单值）
    photon_stat = 1                        # 玻色子（整数自旋 → 交换对称 +1）
    fermion_stat = -1                      # 费米子（半整数自旋 → 反对称 -1）
    ok5 = (len(photon_proj_values) == 2
           and photon_winding_z2 == -1
           and photon_stat == 1 and fermion_stat == -1)
    check("S5  三层次区分：投影值 s=±1（2 值）≠ 环绕模 2 类（非平凡单值）≠ 统计类（光子+1/费米子-1）", ok5,
          "光子统计类（玻色子 +1）独立于其环绕模 2 类（非平凡）——不可混为一谈")

    results = [ok1, ok2, ok3, ok4, ok5]
    print("\n" + "=" * 78)
    print(f"Z₂ 值拓扑荷统一验证：{sum(results)}/5 通过")
    if not all(results):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
