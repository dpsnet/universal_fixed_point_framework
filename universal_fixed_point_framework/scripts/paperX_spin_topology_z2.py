#!/usr/bin/env python3
"""
paperX_spin_topology_z2.py — 自旋拓扑化断言的数值验证（笔记 06_photon_topology 方向 5 §6.5, 2026-08-11）

推进开放问题 ①：旋量 2π 变号（π₁(SO(3)) = Z₂）的数值层——"自旋不是运动，是拓扑结构"。

S1: SU(2) 中 2π 旋转 = -I（旋量变号），4π = +I；SO(3) 中 2π = I（无变号）
S2: 覆盖提升——SO(3) 中 2π 闭环提升到 SU(2) 为开路径（I→-I）、4π 闭环提升为闭环（I→+I）
S3: 双覆盖群性质——Φ(U₁U₂)=Φ(U₁)Φ(U₂)（群同态）、Φ(U)=Φ(-U)（核 Z₂）、每点纤维恰 2 元
S4: 任意轴 2π 旋转旋量均变号（n·σ 参数化，多随机方向）
S5: SU(2) ≅ S³（a²+|b|²=1）——单连通空间参数化（2π 路径可收缩的载体）
S6: Uhlenbeck–Goudsmit 自转模型失败——电子"自转"表面速度 >> c（自旋非运动）
S7: Berry 相位 = -Ω/2——自旋绝热演化的几何/拓扑相位（磁单极通量）

诚实边界：均为标准数学物理事实（旋量双值性、覆盖空间、Berry 相位）的数值复核，
不构成新物理预言；π₁(SO(3))=Z₂ 的严格证明属拓扑学（覆盖空间理论），数值层仅给
出"变号/双覆盖/相位"的一致性证据，形式化证明留待 Lean 层。
"""
import numpy as np

C = 299792458.0  # m/s
HBAR = 1.054571817e-34  # J·s
ME = 9.1093837015e-31  # kg
RE_CLASSIC = 2.8179403262e-15  # m，经典电子半径


def check(name, cond, detail=""):
    status = "PASS" if cond else "FAIL"
    print(f"[{status}] {name}" + (f" — {detail}" if detail else ""))
    return bool(cond)


def su2_rot(n, theta):
    """SU(2) 旋转矩阵：U = cos(θ/2)I - i sin(θ/2)(n·σ)，n 自动归一化"""
    n = np.asarray(n, float)
    n = n / np.linalg.norm(n)
    nx, ny, nz = n
    sx = np.array([[0, 1], [1, 0]], complex)
    sy = np.array([[0, -1j], [1j, 0]], complex)
    sz = np.array([[1, 0], [0, -1]], complex)
    return (np.cos(theta / 2) * np.eye(2, dtype=complex)
            - 1j * np.sin(theta / 2) * (nx * sx + ny * sy + nz * sz))


def so3_from_su2(U):
    """覆盖映射 Φ: SU(2)→SO(3)：共轭作用 X→UXU†（X = x·σ），返回 3x3 旋转矩阵
    R_ij = ½Tr(σ_i U σ_j U†)（i 输出、j 输入）"""
    sx = np.array([[0, 1], [1, 0]], complex)
    sy = np.array([[0, -1j], [1j, 0]], complex)
    sz = np.array([[1, 0], [0, -1]], complex)
    sig = [sx, sy, sz]
    R = np.zeros((3, 3))
    for i in range(3):
        for j in range(3):
            R[i, j] = 0.5 * np.trace(sig[i] @ (U @ sig[j] @ U.conj().T)).real
    return R


def main():
    print("自旋拓扑化断言数值验证（笔记方向 5 §6.5 开放问题①：旋量 2π 变号 / π₁(SO(3))=Z₂）")
    print("=" * 78)

    # S1: SU(2) 中 2π 旋转 = -I（旋量变号），4π = +I；SO(3) 中 2π = I
    nz = (0.0, 0.0, 1.0)
    U2 = su2_rot(nz, 2 * np.pi)
    U4 = su2_rot(nz, 4 * np.pi)
    R2 = so3_from_su2(U2)   # SO(3) 中 2π 旋转
    ok1 = (np.allclose(U2, -np.eye(2), atol=1e-12)
           and np.allclose(U4, np.eye(2), atol=1e-12)
           and np.allclose(R2, np.eye(3), atol=1e-12))
    print("\nS1  SU(2) 旋量变号 vs SO(3) 无变号")
    print("   U_z(2π) =\n", np.round(U2, 6))
    print("   U_z(4π) =\n", np.round(U4, 6))
    print(f"   SO(3) R_z(2π) = I? {np.allclose(R2, np.eye(3), atol=1e-12)}")
    check("S1  旋量 2π 变号（U(2π)=-I）而 SO(3) 2π 回自身（R(2π)=I）", ok1,
          "U(2π)=-I, U(4π)=+I, R(2π)=I")

    # S2: 覆盖提升——SO(3) 中 2π 闭环提升为 SU(2) 开路径（I→-I），4π 闭环提升为闭环（I→+I）
    print("\nS2  覆盖提升：SO(3) 闭环路径在 SU(2) 中的端点")
    U_path_2pi = su2_rot(nz, 2 * np.pi)   # 提升到 SU(2) 的端点
    U_path_4pi = su2_rot(nz, 4 * np.pi)
    closed_2pi = np.allclose(U_path_2pi, np.eye(2), atol=1e-12)   # False：开路径
    closed_4pi = np.allclose(U_path_4pi, np.eye(2), atol=1e-12)   # True：闭环
    ok2 = (not closed_2pi) and closed_4pi
    check("S2  SO(3) 的 2π 闭环提升为 SU(2) 开路径（I→-I）、4π 闭环提升为闭环（I→+I）", ok2,
          "2π 提升端点 = -I（非闭），4π 提升端点 = +I（闭）")

    # S3: 双覆盖群性质——群同态 Φ(U1U2)=Φ(U1)Φ(U2)；Φ(U)=Φ(-U)；核 = {±I}；纤维 2 元
    rng = np.random.default_rng(42)
    Ua = su2_rot((0.3, -0.5, 0.8), 1.7)
    Ub = su2_rot((-0.7, 0.2, 0.6), 2.3)
    Ra, Rb = so3_from_su2(Ua), so3_from_su2(Ub)
    R_ab = so3_from_su2(Ua @ Ub)
    hom = np.allclose(R_ab, Ra @ Rb, atol=1e-12)
    ker = np.allclose(so3_from_su2(-Ua), Ra, atol=1e-12)  # Φ(-U)=Φ(U)
    det1 = abs(np.linalg.det(Ra) - 1.0) < 1e-12          # 保向
    ok3 = hom and ker and det1
    check("S3  Φ: SU(2)→SO(3) 群同态 + 核 Z₂（Φ(-U)=Φ(U)）+ 保向 det=1", ok3,
          f"同态 err={np.max(np.abs(R_ab-Ra@Rb)):.1e}, det={np.linalg.det(Ra):.12f}")

    # S4: 任意轴 2π 旋转旋量均变号（多随机方向）
    ok4 = True
    worst4 = 0.0
    for _ in range(20):
        n = rng.normal(size=3)
        n = n / np.linalg.norm(n)
        Un = su2_rot(tuple(n), 2 * np.pi)
        d = np.max(np.abs(Un + np.eye(2)))
        worst4 = max(worst4, d)
        ok4 = ok4 and d < 1e-12
    check("S4  任意轴 2π 旋转旋量均变号（U_n(2π) = -I，20 随机方向）", ok4,
          f"max|U_n(2π)+I| = {worst4:.1e}")

    # S5: SU(2) ≅ S³ 参数化（a²+|b|²=1）——单连通载体
    # U = aI - i(b·σ)：a = Re U00, b_z = -Im U00, b_y = -Re U01, b_x = -Im U10
    ok5 = True
    for _ in range(200):
        n = rng.normal(size=3)
        n = n / np.linalg.norm(n)
        th = rng.uniform(0, 4 * np.pi)
        U = su2_rot(tuple(n), th)
        a = U[0, 0].real
        b_x = -U[1, 0].imag
        b_y = -U[0, 1].real
        b_z = -U[0, 0].imag
        b2 = b_x ** 2 + b_y ** 2 + b_z ** 2
        if abs(a * a + b2 - 1.0) > 1e-12:
            ok5 = False
    check("S5  SU(2) ≅ S³ 参数化（a²+|b|²=1，200 采样）——单连通空间（2π 路径可收缩载体）", ok5)

    # S6: Uhlenbeck–Goudsmit 自转模型失败——表面速度 >> c
    v_surf = HBAR / (2.0 * ME * RE_CLASSIC)
    ok6 = v_surf > C
    print(f"\nS6  Uhlenbeck–Goudsmit 自转速度 v = ħ/(2·m_e·r_e) = {v_surf/C:.2f} c")
    check("S6  电子自转表面速度远超光速（自旋无转动载体，非运动学旋转）", ok6,
          f"v = {v_surf:.3e} m/s = {v_surf/C:.1f}c")

    # S7: Berry 相位 = -Ω/2（自旋绝热演化几何相位）
    # n(φ) = (sinθ0 cosφ, sinθ0 sinφ, cosθ0)，φ: 0→2π 闭合路径
    # |ψ₊⟩ = (cos(θ0/2), sin(θ0/2) e^{iφ})；γ = -Σ Im log⟨ψ₊(φ_k)|ψ₊(φ_{k+1})⟩ = -π(1-cosθ0)
    th0 = np.deg2rad(60.0)
    N = 20000
    phi = np.linspace(0, 2 * np.pi, N, endpoint=False)
    # |ψ₊(φ)⟩ = (cos(θ0/2), sin(θ0/2) e^{iφ})
    psi = np.zeros((2, N), complex)
    psi[0, :] = np.cos(th0 / 2)
    psi[1, :] = np.sin(th0 / 2) * np.exp(1j * phi)
    # 逐段内积 ⟨ψ(φ_k)|ψ(φ_{k+1})⟩（连接 1-形式的离散化）
    inner = np.conj(psi[1, :-1]) * psi[1, 1:] + np.conj(psi[0, :-1]) * psi[0, 1:]
    inner_closed = np.conj(psi[1, -1]) * psi[1, 0] + np.conj(psi[0, -1]) * psi[0, 0]
    inner_all = np.append(inner, inner_closed)
    gamma_num = -np.sum(np.imag(np.log(inner_all)))
    gamma_th = -np.pi * (1 - np.cos(th0))
    ok7 = abs(gamma_num - gamma_th) < 1e-6
    print(f"   θ0=60°: Ω=2π(1-cosθ0)={2*np.pi*(1-np.cos(th0)):.6f}, Berry 相位预测=-Ω/2={gamma_th:.6f}")
    print(f"   数值积累 = {gamma_num:.6f}")
    check("S7  Berry 相位 = -Ω/2（自旋绝热演化的几何/拓扑相位）", ok7,
          f"|γ_num - γ_th| = {abs(gamma_num-gamma_th):.2e}")

    results = [ok1, ok2, ok3, ok4, ok5, ok6, ok7]
    print("\n" + "=" * 78)
    print(f"旋量 Z₂ 拓扑数值验证：{sum(results)}/7 通过")
    if not all(results):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
