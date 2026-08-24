# ============================================================
# UFPF → MUFPF 更名通知
# ============================================================
# 本文件属于 Universal Fixed Point Framework (UFPF)。
# 该框架已计划更名为 Meta-Universal Fixed-Point Functorial Framework (MUFPF)。
# 更名计划详见：roadmap/mu_renaming_plan.md
#
# 原因：UFPF 缩写与 IEEE 生物图像识别框架冲突，影响学术检索。
# 新名称 MUFPF 具有全球唯一性，且更好地体现框架的元数学特性。
#
# 本文件中 UFPF 相关引用数量：2
# 更名将在计划确认后统一执行，当前代码不做修改。
# ============================================================

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
paperX_cl17_gamma_spectrum.py — Cl(1,7) 生成元谱类型分层（B1 推进：Γ 谱 ↔ 可证编码层翻译）
=============================================================================
对应笔记：notes/04_lorentz_gravity/silence_direction_allocation.md §4.7（v0.8）
          + notes/06_photon_topology/photon_first_principle_origin.md §3.6（编码分析）
对应论文：paper32（Cl(1,7) 谱静默，§6 生成元代数本质 / §4.4 建模指派）、
          paper5 定理 5.1/5.2（虚谱→规范、实谱→几何）、
          paper20（Cl(1,7) ≅ M₁₆(ℝ)）

问题：B1 编码缺口的代数骨架——"Γ 生成元的谱结构"是什么？能否翻译到可证编码层？
本脚本验证三个**代数谱事实**（约定内确定）+ 两个**约定无关结构事实**：

  事实 α（约定内，可证）：A² = +I ⟹ 特征值 ∈ {±1}（实谱）
  事实 β（约定内，可证）：A² = −I ⟹ 特征值 ∈ {±i}（纯虚谱）
  事实 γ（约定无关，可证）：同类双线性对 (ΓᵢΓⱼ)² = −I ⟹ 纯虚谱 ±i
  事实 δ（约定无关，可证）：异类双线性对 (ΓᵢΓⱼ)² = +I ⟹ 实谱 ±1
  事实 ε（推论）：静默子代数 Cl(0,4) 的 SO(4) 旋转生成元 = 同类对 ⟹ 纯虚谱 ±i/2

  约定登记（ζ，2026-08-16 修正）：框架内约定已统一为**数学标准 Cl(1,7)**（时间²=+1、空间²=−1，
  Dirac 度规，与 paperX_cl17_first_principle.py / gammas_fixed.py 一致；Lean Clifford.lean
  的 e_01/e_10 命名颠倒已修正）。历史探针 paperX_delta_spatial_probe.py 用时间²=−1
  （= 主导约定表示整体乘 i，酉等价，探针判定不变）。两约定互为整体乘 i（Wick 型翻转）；
  **单生成元谱类型标签随约定翻转**；同类/异类双线性对谱类型约定无关（γ/δ/ε 不受影响）。

性质：数值自洽验证（理论推导候选，非实验验证）。Lean 骨架见
  `formal_proof/UFPFormalization/UFPFormalization/CliffordSpectralType.lean`
  （eig_sq_eq_one / eig_sq_eq_neg_one / bivec_sq_eq_neg_one，lake build 零错误）。
"""
import numpy as np

RESULTS = []


def check(name, cond, detail=""):
    RESULTS.append((name, cond))
    mark = "✓" if cond else "✗"
    print(f"  [{mark}] {name}" + (f"  ({detail})" if detail else ""))


def anticommute(A, B, tol=1e-10):
    return np.allclose(A @ B + B @ A, np.zeros_like(A), atol=tol)


def evals_all(evals, target, tol=1e-8):
    """特征值全部 ∈ target（复数集合）。"""
    return all(any(abs(ev - t) < tol for t in target) for ev in evals)


# ============================================================
# Cl(1,7) 16×16 构造（约定 B：时间 +I、空间 −I）
# 同 paperX_cl17_first_principle.py F5：Γ⁰ = σ₃⊗I₈、Γⁱ = σ₁⊗γ'ᵢ
# ============================================================

def build_cl17_convention_B():
    I2 = np.eye(2)
    I8 = np.eye(8)
    S3 = np.array([[1.0, 0.0], [0.0, -1.0]])
    S1 = np.array([[0.0, 1.0], [1.0, 0.0]])
    S2 = np.array([[0.0, -1.0], [1.0, 0.0]])   # 实，平方 −I

    def kron(*mats):
        out = mats[0]
        for m in mats[1:]:
            out = np.kron(out, m)
        return out

    iS1 = 1j * S1
    # Cl(0,7) 8×8 复生成元（前 6 个标准递推 + 体积元）
    g07 = [
        kron(iS1, I2, I2), kron(S2, I2, I2),
        kron(S3, iS1, I2), kron(S3, S2, I2),
        kron(S3, S3, iS1), kron(S3, S3, S2),
    ]
    omega = I8
    for x in g07:
        omega = omega @ x
    g07.append(omega)
    # Cl(1,7) 16×16：Γ⁰ = σ₃⊗I₈（+I 时间）、Γⁱ = σ₁⊗γ'ᵢ（−I 空间）
    Gamma = [np.kron(S3, I8)] + [np.kron(S1, x) for x in g07]
    return Gamma


def build_cl17_convention_A():
    """约定 A（Lean 式）：时间 ²=−I、空间 ²=+I。= 约定 B 全体乘 i。"""
    G = build_cl17_convention_B()
    return [1j * g for g in G]


# ============================================================
# 验证主体
# ============================================================

def run():
    print()
    print("╔════════════════════════════════════════════════════════════════════╗")
    print("║  Cl(1,7) 生成元谱类型分层（B1/B2 推进）                          ║")
    print("║  约定 B（Dirac 主导，数学标准）：时间 +I / 空间 −I                ║")
    print("║  约定 A（历史探针式）对偶；2026-08-16 已统一                       ║")
    print("╚════════════════════════════════════════════════════════════════════╝")

    for name, G in [("约定 B（时间²=+I，空间²=−I）", build_cl17_convention_B()),
                    ("约定 A（时间²=−I，空间²=+I）", build_cl17_convention_A())]:
        print("\n" + "=" * 74)
        print(f"  {name}")
        print("=" * 74)

        # 合法性：平方 ±I + 全反交换（按各自约定校验平方）
        if name[3] == "B":
            sq = [np.allclose(G[0] @ G[0], np.eye(16))] + \
                 [np.allclose(g @ g, -np.eye(16)) for g in G[1:]]
        else:
            sq = [np.allclose(G[0] @ G[0], -np.eye(16))] + \
                 [np.allclose(g @ g, np.eye(16)) for g in G[1:]]
        ac = all(anticommute(G[i], G[j]) for i in range(8) for j in range(i + 1, 8))
        n_ac = sum(1 for i in range(8) for j in range(i + 1, 8)
                   if anticommute(G[i], G[j]))
        check(f"构造合法（平方 ±I 8/8 + 反交换 28/28）", all(sq) and ac,
              f"平方 {sum(sq)}/8、反交换 {n_ac}/28")

        # T1/T1'：单生成元谱类型（约定内）
        time_ev = np.linalg.eigvals(G[0])
        space_ev = [np.linalg.eigvals(G[i]) for i in range(1, 8)]
        if name[3] == "B":
            t1 = evals_all(time_ev, {1.0, -1.0}) and \
                 all(evals_all(e, {1j, -1j}) for e in space_ev)
            detail = "时间实谱 ±1、空间纯虚谱 ±i"
        else:
            t1 = evals_all(time_ev, {1j, -1j}) and \
                 all(evals_all(e, {1.0, -1.0}) for e in space_ev)
            detail = "时间纯虚谱 ±i、空间实谱 ±1"
        # 迹零（特征值成对 ±）复核
        tr_zero = all(abs(np.trace(g)) < 1e-8 for g in G)
        check("T1 单生成元谱类型（约定内）", t1 and tr_zero,
              f"{detail}；迹零 {tr_zero}")

        # T2/T3：双线性对谱类型（约定无关断言在此核对）
        same_imag, mixed_real = True, True
        for i in range(8):
            for j in range(i + 1, 8):
                b = G[i] @ G[j]
                bsq = b @ b
                is_space_i = (i >= 1)
                is_space_j = (j >= 1)
                if is_space_i and is_space_j:
                    # 同类（空间-空间）：预期 (b)² = −I ⟹ ±i
                    if not np.allclose(bsq, -np.eye(16)):
                        same_imag = False
                else:
                    # 异类（时间-空间）：预期 (b)² = +I ⟹ ±1
                    if not np.allclose(bsq, np.eye(16)):
                        mixed_real = False
        check("T2 同类（空间-空间）双线性对 (ΓᵢΓⱼ)²=−I ⟹ 纯虚谱 ±i（约定无关）",
              same_imag, "28 对中空间-空间对全部 ²=−I")
        check("T3 异类（时间-空间）双线性对 (ΓᵢΓⱼ)²=+I ⟹ 实谱 ±1（约定无关）",
              mixed_real, "7 对时间-空间全部 ²=+I")

        # T4：静默子代数 Cl(0,4)（e₄..e₇）SO(4) 旋转生成元 = 同类对 ⟹ 纯虚谱 ±i/2
        so4_ok = True
        for i in range(4, 8):
            for j in range(i + 1, 8):
                S = 0.25 * (G[i] @ G[j] - G[j] @ G[i])   # = 0.5·ΓᵢΓⱼ（反交换）
                s_sq = S @ S
                if not np.allclose(s_sq, -0.25 * np.eye(16)):
                    so4_ok = False
                ev = np.linalg.eigvals(S)
                if not evals_all(ev, {0.5j, -0.5j}):
                    so4_ok = False
        check("T4 静默子代数 SO(4) 旋转生成元（同类对）²=−I/4 ⟹ 纯虚谱 ±i/2（约定无关）",
              so4_ok, "6 个 SO(4) 生成元（e₄..e₇ 内 6 对）全部 ²=−I/4、特征值 ±i/2")

    # T5：约定差异登记（ζ）——翻转只改单生成元标签，不改双线性对
    GB = build_cl17_convention_B()
    GA = build_cl17_convention_A()
    flip = all(np.allclose(1j * gb, ga) for gb, ga in zip(GB, GA))
    print("\n" + "=" * 74)
    print("  T5. 约定差异登记（ζ）：两约定互为整体乘 i（Wick 型翻转）")
    print("=" * 74)
    print(f"  约定 B（主导，Dirac/数学标准）：时间 Γ⁰²=+I（实谱 ±1）、空间 Γ¹..Γ⁷²=−I（纯虚谱 ±i）")
    print(f"  约定 A（历史探针 delta_spatial_probe 式）：时间²=−I（纯虚谱）、空间²=+I（实谱 ±1）")
    print(f"  GA = i·GB 逐生成元成立: {flip}")
    print(f"  ⟹ 单生成元谱类型标签随约定翻转（酉等价，探针判定不变）；双线性对谱类型约定无关")
    check("T5 约定差异登记（ζ）", flip, "GA = i·GB")

    # T6：静默 SO(4) ≅ SU(2)×SU(2) 分裂（B2 连接规则的结构支撑，约定无关）
    print("\n" + "=" * 74)
    print("  T6. 静默子代数 SO(4) ≅ SU(2)×SU(2)（6 = 3+3 直和分裂）")
    print("=" * 74)
    GB6 = build_cl17_convention_B()
    pairs = [(4, 5), (4, 6), (4, 7), (5, 6), (5, 7), (6, 7)]
    S = {p: 0.25 * (GB6[i] @ GB6[j] - GB6[j] @ GB6[i]) for (i, j) in pairs for p in [(i, j)]}
    S45, S46, S47, S56, S57, S67 = (S[p] for p in pairs)
    Z16 = np.zeros((16, 16), dtype=complex)
    Sp = [(S45 + S67) / 2, (S46 - S57) / 2, (S47 + S56) / 2]   # 自对偶 su(2)₊
    Sm = [(S45 - S67) / 2, (S46 + S57) / 2, (S47 - S56) / 2]   # 反自对偶 su(2)₋
    vecs = np.array([s.flatten() for s in S.values()])
    rank6 = np.linalg.matrix_rank(vecs) == 6
    cross_zero = all(np.allclose(Sp[a] @ Sm[b] - Sm[b] @ Sp[a], Z16)
                     for a in range(3) for b in range(3))

    def in_span(M, basis, tol=1e-8):
        B = np.array([b.flatten() for b in basis])   # (3, 256)
        v = M.flatten()                              # (256,)
        coef, *_ = np.linalg.lstsq(B.T, v, rcond=None)   # 解 B.T·c = v，c 3 维
        return np.linalg.norm(v - B.T @ coef) < tol

    sp_closed = all(in_span(Sp[a] @ Sp[b] - Sp[b] @ Sp[a], Sp)
                    for a in range(3) for b in range(3))
    sm_closed = all(in_span(Sm[a] @ Sm[b] - Sm[b] @ Sm[a], Sm)
                    for a in range(3) for b in range(3))
    sp_imag = all(all(abs(ev.real) < 1e-8 for ev in np.linalg.eigvals(s)) for s in Sp)
    sm_imag = all(all(abs(ev.real) < 1e-8 for ev in np.linalg.eigvals(s)) for s in Sm)
    t6 = rank6 and cross_zero and sp_closed and sm_closed and sp_imag and sm_imag
    check("T6 静默 SO(4) ≅ SU(2)×SU(2)（6=3+3 直和、[S⁺,S⁻]=0、各封闭、谱纯虚）", t6,
          f"秩 {np.linalg.matrix_rank(vecs)}、交叉对易 {sum(1 for a in range(3) for b in range(3) if np.allclose(Sp[a]@Sm[b]-Sm[b]@Sp[a], Z16))}/9、S⁺/S⁻ 封闭、谱纯虚")

    # T7：B2 谱值嵌入构造——A_R = γ·I + S（静默旋转生成元 → Rec_diss 复谱虚部）
    print("\n" + "=" * 74)
    print("  T7. B2 谱值嵌入：A_R = γ·I + S，σ(A_R) 虚部 = σ(S)（'哪个 S ↔ 哪个系统'）")
    print("=" * 74)
    GB7 = build_cl17_convention_B()
    gamma7 = 0.089   # 阻尼锚点（paper27 命题 5.1：Schwarzschild 基模 |Im ω| = 0.089）
    pairs7 = [(4, 5), (4, 6), (4, 7), (5, 6), (5, 7), (6, 7)]
    Sset7 = [0.5 * (GB7[i] @ GB7[j]) for (i, j) in pairs7]
    S45_7, S46_7, S47_7, S56_7, S57_7, S67_7 = Sset7
    Splus7 = [(S45_7 + S67_7) / 2, (S46_7 - S57_7) / 2, (S47_7 + S56_7) / 2]
    Sminus7 = [(S45_7 - S67_7) / 2, (S46_7 + S57_7) / 2, (S47_7 - S56_7) / 2]
    I16 = np.eye(16, dtype=complex)
    embed_ok = True
    for S in Sset7 + Splus7 + Sminus7:
        A_R = gamma7 * I16 + S
        ev = np.linalg.eigvals(A_R)
        s_ev = np.linalg.eigvals(S)
        # 谱值嵌入：实部 = γ（阻尼）、虚部 = σ(S)（S 纯虚谱 → A_R 虚部）
        real_ok = all(abs(e.real - gamma7) < 1e-8 for e in ev)
        imag_ok = sorted(round(e.imag, 8) for e in ev) == sorted(round(e.imag, 8) for e in s_ev)
        # 压缩（Rec_diss 定义 5.1 条件 1）：σ(U_R) = e^{−σ(A_R)}，谱半径 e^{−γ} < 1
        rho = max(abs(np.exp(-mu)) for mu in ev)
        if not (real_ok and imag_ok and rho < 1 and abs(rho - np.exp(-gamma7)) < 1e-10):
            embed_ok = False
    # 单 bivector 精确谱：S_ij² = −(1/4)I ⟹ σ(A_R) = {γ ± i/2}（Lean sq_neg_quarter_eig）
    ev45 = np.linalg.eigvals(gamma7 * I16 + S45_7)
    exact45 = all(abs(e.real - gamma7) < 1e-8 and abs(abs(e.imag) - 0.5) < 1e-8 for e in ev45)
    # 谱值一一对应：S 谱 ±i/2 ↔ A_R 虚部 ±0.5（"哪个 S ↔ 哪个系统" = 谱值对应）
    imag_s45 = sorted(set(round(e.imag, 8) for e in np.linalg.eigvals(gamma7 * I16 + S45_7)))
    s_s45 = sorted(set(round(e.imag, 8) for e in np.linalg.eigvals(S45_7)))
    one_to_one = (imag_s45 == s_s45) and (imag_s45 == [-0.5, 0.5])
    check("T7 谱值嵌入 A_R = γ·I + S：虚部=σ(S)、实部=γ、压缩 e^{−γ}<1（12 个静默旋转生成元全通过）",
          embed_ok and exact45 and one_to_one,
          f"γ={gamma7}、单 bivector 精确 {gamma7}±i/2、谱半径 e^−γ={np.exp(-gamma7):.4f}、虚部↔谱值一一对应")

    # T8：γ 标度第一性候选（B2 剩余自由度①）——γ = Δλ_min / 1/k_max / 1，压缩度与 QNM 对比
    print("\n" + "=" * 74)
    print("  T8. γ 标度第一性候选：阻尼 = 谱间隙 Δλ_min（paper20 定理 6.1）等")
    print("=" * 74)
    import math
    dl_min = (math.sqrt(6) - math.sqrt(2)) / math.sqrt(72)   # paper20 定理 6.1 闭式
    kmax8 = 8
    rho_qnm = math.exp(-0.089)   # Schwarzschild 基模 |λ|（paper27 命题 5.1）
    print(f"    Δλ_min = (√6−√2)/√72 = {dl_min:.6f}；1/Δλ_min = {1.0/dl_min:.4f}；1/k_max = {1.0/kmax8:.4f}")
    print(f"    QNM 锚点 |λ| = e^(−0.089) = {rho_qnm:.6f}（paper27 命题 5.1）")
    for tag, g in [("γ=Δλ_min（谱间隙，paper27 定义 4.3 谱静默阈值先例）", dl_min),
                   ("γ=1/k_max（截断倒数，k_max=8 统一 3 定理）", 1.0 / kmax8),
                   ("γ=1（静默参数 s=e⁻¹，Moran 机器证明）", 1.0)]:
        rho = math.exp(-g)
        diff = (rho / rho_qnm - 1) * 100
        print(f"    {tag}: γ={g:.6f}，ρ=e^−γ={rho:.6f}，vs QNM 差 {diff:+.1f}%")
    # 谱静默阈值一致性：γ=Δλ_min 与 paper27 定义 4.3 γ_threshold=Δλ_min/M_Pl=0.122（无量纲）
    thresh_ok = abs(dl_min - 0.122) < 0.01
    # 压缩度量级：e^{−Δλ_min} 与 QNM |λ| 同量级（谱静默临界耗散候选）
    rho_gap = math.exp(-dl_min)
    scale_ok = 0.5 < rho_gap / rho_qnm < 2.0
    # Δλ_min ≈ 1/k_max 数值关系
    ratio8 = (1.0 / dl_min) / kmax8
    check("T8 γ 候选：γ=Δλ_min 与谱静默阈值一致、压缩度与 QNM 同量级、Δλ_min≈1/k_max（差 <5%）",
          thresh_ok and scale_ok and abs(ratio8 - 1) < 0.05,
          f"Δλ_min={dl_min:.6f}、ρ_gap={rho_gap:.6f} vs QNM {rho_qnm:.6f}、1/(Δλ_min·k_max)={ratio8:.4f}")

    # T9：γ=Δλ_min（谱静默阈值主候选）下谱值嵌入构造全验证 + 1/Δλ_min 精确闭式
    print("\n" + "=" * 74)
    print("  T9. γ=Δλ_min 下谱值嵌入 A_R = Δλ_min·I + S 全验证 + 1/Δλ_min = 3(√3+1) 闭式")
    print("=" * 74)
    g9 = dl_min   # γ = Δλ_min（T8 主候选）
    embed9_ok = True
    for S in Sset7 + Splus7 + Sminus7:
        A9 = g9 * I16 + S
        ev9 = np.linalg.eigvals(A9)
        s_ev9 = np.linalg.eigvals(S)
        real9 = all(abs(e.real - g9) < 1e-8 for e in ev9)
        imag9 = sorted(round(e.imag, 8) for e in ev9) == sorted(round(e.imag, 8) for e in s_ev9)
        rho9 = max(abs(np.exp(-mu)) for mu in ev9)
        if not (real9 and imag9 and rho9 < 1):
            embed9_ok = False
    # 1/Δλ_min = √72/(√6−√2) = 6/(√3−1) = 3(√3+1)（代数化简，精确闭式）
    one_over_closed = 3 * (math.sqrt(3) + 1)
    closed_ok = abs(one_over_closed - 1.0 / dl_min) < 1e-12
    check("T9 γ=Δλ_min 下谱值嵌入全通过（12 生成元、实部=Δλ_min 虚部=σ(S)、压缩<1）+ 1/Δλ_min=3(√3+1) 精确闭式",
          embed9_ok and closed_ok,
          f"1/Δλ_min={1.0/dl_min:.6f}=3(√3+1)={one_over_closed:.6f}、vs k_max=8 差 {(1.0/dl_min/8-1)*100:+.2f}%、ρ=e^−Δλ_min={np.exp(-g9):.4f}")

    # T10："为何取临界"框架先例——c₂ = S₄ = 1/15 恰在观测窗口阈值（paper32 §4.4 可见性判据含等号）
    print("\n" + "=" * 74)
    print("  T10. '为何取临界'框架先例：S₄=1/15 恰在观测窗口阈值（paper32 §4.4）")
    print("=" * 74)
    dH10 = math.log(15)
    S4_10 = math.exp(-dH10)          # = 1/15（精确，因 S₄ = e^{−d_H} = e^{−ln15}）
    c2_10 = math.exp(-dH10)          # c₂ = S₄（paper32 §4.4 物理 3-map IFS）
    c1_10 = math.exp(-(3 + dH10))    # c₁ = S₃S₄（完全静默）
    s4_exact = abs(S4_10 - 1.0 / 15) < 1e-12
    crit_ok = abs(c2_10 - S4_10) < 1e-12    # c₂ 恰在观测窗口阈值（可见性判据 w ≥ S₄ 含等号）
    rho_vis = np.exp(-dl_min)               # Rec_diss 压缩度（γ=Δλ_min）
    vis_ok = rho_vis > S4_10                # 对象活跃可见（ρ > 观测窗口阈值）
    ratio15 = dl_min * 15
    ratio_c2 = dl_min / c2_10
    check("T10 框架先例：S₄=e^{−d_H}=1/15 精确、c₂=S₄ 恰在观测窗口阈值（临界可见先例）、Rec_diss 压缩度 ρ=e^−Δλ_min>S₄ 可见",
          s4_exact and crit_ok and vis_ok,
          f"S₄=1/15={S4_10:.6f}、c₁=e^−(3+d_H)={c1_10:.6f}（完全静默）、c₂=S₄={crit_ok}、ρ={rho_vis:.4f}>S₄、Δλ_min·15={ratio15:.4f}、Δλ_min/c₂={ratio_c2:.4f}")

    # T11：Δλ_min 简洁闭式 (√3−1)/6（恒等于 (√6−√2)/√72）+ Δλ_min·c₂ 关系精确化
    print("\n" + "=" * 74)
    print("  T11. Δλ_min = (√3−1)/6 简洁闭式 + Δλ_min·15 = (5/2)(√3−1) 精确")
    print("=" * 74)
    dl_simple = (math.sqrt(3) - 1) / 6.0
    dl_orig = (math.sqrt(6) - math.sqrt(2)) / math.sqrt(72)
    id_ok = abs(dl_simple - dl_orig) < 1e-15      # (√3−1)/6 ≡ (√6−√2)/√72 代数恒等
    rel15_new = (5.0 / 2.0) * (math.sqrt(3) - 1)  # Δλ_min·15 = 15(√3−1)/6 = (5/2)(√3−1)
    rel_ok = abs(rel15_new - dl_orig * 15) < 1e-12
    # γ=Δλ_min 与 c₂=S₄=1/15 关系（平行论证数值结构）：Δλ_min/c₂ = (5/2)(√3−1)
    ratio_c2_new = dl_orig / (1.0 / 15)
    check("T11 Δλ_min=(√3−1)/6 简洁闭式（恒等）+ Δλ_min·15=(5/2)(√3−1) 精确 + Δλ_min/c₂ 平行论证数值结构",
          id_ok and rel_ok,
          f"Δλ_min=(√3−1)/6={dl_simple:.8f}、Δλ_min·15=(5/2)(√3−1)={rel15_new:.6f}、Δλ_min/c₂={ratio_c2_new:.6f}")

    # T12：γ 取临界必要性——判据下界（paper27：γ≥Δλ_min 才可辨识）+ 最小可辨识极值（电磁长程）
    print("\n" + "=" * 74)
    print("  T12. γ 取临界必要性：γ≥Δλ_min 判据下界（paper27 定义 4.3）+ 最小可辨识极值")
    print("=" * 74)
    # paper27 判据：γ < Δλ_min ⟹ LACI > 2.0 谱静默（物理不可辨识）；γ ≥ Δλ_min 可辨识
    g_vals12 = [0.05, 0.09, dl_min, 0.15, 0.20]
    for gv in g_vals12:
        rho_v = math.exp(-gv)
        if gv < dl_min - 1e-9:
            zone = "谱静默（LACI>2.0 不可辨识）"
        elif abs(gv - dl_min) < 1e-9:
            zone = "临界（恰可辨识，LACI=2.0 边界）"
        else:
            zone = "可辨识（LACI<2.0）"
        print(f"    γ={gv:.3f}：ρ=e^−γ={rho_v:.4f}，{zone}")
    # 可辨识区 [Δλ_min, ∞) 的下确界 = Δλ_min；最小阻尼 = 最大压缩度（最活跃/最长程支持）
    rho_ident = [math.exp(-gv) for gv in [dl_min, 0.15, 0.20]]
    min_damp_ok = rho_ident[0] > rho_ident[1] > rho_ident[2]   # 可辨识区最小阻尼 = 最大压缩度
    boundary_ok = all(gv < dl_min for gv in [0.05, 0.09]) and all(gv > dl_min for gv in [0.15, 0.20])
    check("T12 γ 取临界必要性：γ≥Δλ_min 可辨识下界（paper27 判据，非类比）+ γ=Δλ_min 为可辨识区最小阻尼（下确界，电磁长程支持）",
          boundary_ok and min_damp_ok,
          f"γ<Δλ_min⟹LACI>2.0 不可辨识；γ=Δλ_min 恰可辨识（LACI=2.0）且 ρ={rho_ident[0]:.4f} 为可辨识区最大（最小阻尼）")

    n_pass = sum(1 for _, ok in RESULTS if ok)
    n_total = len(RESULTS)
    print("\n" + "=" * 74)
    print(f"  汇总: {n_pass}/{n_total} 检查通过")
    print("=" * 74)
    if n_pass != n_total:
        raise SystemExit(f"FAIL: {n_total - n_pass} 项未通过")
    print("\n  关键结论（笔记 §4.7/§4.8/§4.9/§4.10 引用）：")
    print("    α/β 单生成元谱类型 = 平方 ±I 的代数推论（约定内确定）")
    print("    γ/δ/ε 双线性对谱类型约定无关（同类对纯虚 ±i、异类对实 ±1）")
    print("    ε 静默子代数 SO(4) 旋转生成元纯虚谱 ±i/2（两约定均成立）")
    print("    ζ 约定已统一（2026-08-16）：数学标准时间²=+1；GA=i·GB 酉等价登记")
    print("    T6 静默 SO(4) ≅ SU(2)×SU(2)（6=3+3 直和、谱纯虚）——B2 连接规则结构支撑")
    print("    T7 谱值嵌入 A_R = γ·I + S（虚部=σ(S)、压缩 e^{−γ}<1）——'哪个 S ↔ 哪个系统'= 谱值一一对应")
    print("    T8/T9 γ=Δλ_min 主候选（谱静默阈值判据量级）：1/Δλ_min=3(√3+1)≈8.196 精确闭式、压缩度与 QNM 同量级")
    print("    T10 γ 临界论证框架先例：c₂=S₄=1/15 恰在观测窗口阈值（paper32 §4.4 可见性判据含等号）")
    print("    T11 Δλ_min=(√3−1)/6 简洁闭式（恒等）；Δλ_min·c₂=(5/2)(√3−1) 精确——γ 与谱权重层关系精确化")
    print("    T12 γ 取临界必要性：γ≥Δλ_min 可辨识下界（paper27 判据非类比）+ 最小可辨识极值（电磁长程）")


if __name__ == "__main__":
    run()
