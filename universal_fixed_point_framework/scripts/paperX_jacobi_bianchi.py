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
# 本文件中 UFPF 相关引用数量：0
# 更名将在计划确认后统一执行，当前代码不做修改。
# ============================================================

#!/usr/bin/env python3
"""
paperX_jacobi_bianchi.py — 雅可比恒等式与 Bianchi 代数前提验证（笔记 06_photon_topology §8 曲率层 §8.6, 2026-08-11）

推进 §8.2 第 3 项剩余部分："完整 Bianchi dΩ+[ω,Ω]=0 需外微分幂零 d²=0 与雅可比恒等式"——
d²=0 已闭合（§8.5）；本节验证雅可比恒等式并闭合 Bianchi 的代数前提。

S1: su(2) 基（泡利矩阵）雅可比恒等式 [σ_i,[σ_j,σ_k]]+[σ_j,[σ_k,σ_i]]+[σ_k,[σ_i,σ_j]]=0（全组合）
S2: 随机 su(2) 值矩阵雅可比恒等式（100 组）
S3: 常系数联络的 Bianchi = 雅可比——Ω=ω∧ω（纯对易子），[ω,Ω] 3-形式分量 = 雅可比组合 = 0
S4: 变系数 su(2) 值联络的完整 Bianchi dΩ+[ω,Ω]=0（数值差分，3 维网格残差）
S5: 代数前提总结——d²=0（§8.5）+ 雅可比（本节）⟹ Bianchi（§8.2 第 3 项代数部分闭合）

诚实边界：雅可比恒等式（矩阵结合律推论）与 Bianchi 为标准微分几何事实；
数值验证为实例核对（非新定理）；流形级形式化仍待微分几何库（§8.4）。
"""
import numpy as np

# su(2) 基（泡利矩阵的 i 倍，反厄米）
T1 = np.array([[0, 1], [1, 0]], complex)
T2 = np.array([[0, -1j], [1j, 0]], complex)
T3 = np.array([[1, 0], [0, -1]], complex)
BASIS = [T1, T2, T3]


def check(name, cond, detail=""):
    status = "PASS" if cond else "FAIL"
    print(f"[{status}] {name}" + (f" — {detail}" if detail else ""))
    return bool(cond)


def jacobi(A, B, C):
    """雅可比组合 [A,[B,C]]+[B,[C,A]]+[C,[A,B]]"""
    return (A @ (B @ C - C @ B) - (B @ C - C @ B) @ A
            + B @ (C @ A - A @ C) - (C @ A - A @ C) @ B
            + C @ (A @ B - B @ A) - (A @ B - B @ A) @ C)


def main():
    print("雅可比恒等式与 Bianchi 代数前提验证（笔记 §8.2 第 3 项剩余部分）")
    print("=" * 78)

    # S1: su(2) 基雅可比恒等式（全组合）
    ok1 = True
    worst1 = 0.0
    for i in range(3):
        for j in range(3):
            for k in range(3):
                r = jacobi(BASIS[i], BASIS[j], BASIS[k])
                worst1 = max(worst1, np.max(np.abs(r)))
                if np.max(np.abs(r)) > 1e-10:
                    ok1 = False
    check("S1  su(2) 基雅可比恒等式（[σ_i,[σ_j,σ_k]]+cyc=0，3³ 组合）", ok1,
          f"max 残差 = {worst1:.2e}")

    # S2: 随机 su(2) 值矩阵雅可比（100 组）
    rng = np.random.default_rng(3)
    ok2 = True
    worst2 = 0.0
    for _ in range(100):
        # 随机 su(2) 元素：a·T1+b·T2+c·T3（a,b,c 实数）
        def rand_su2():
            return (rng.normal() * T1 + rng.normal() * T2
                    + rng.normal() * T3)
        A, B, C = rand_su2(), rand_su2(), rand_su2()
        r = jacobi(A, B, C)
        worst2 = max(worst2, np.max(np.abs(r)))
        if np.max(np.abs(r)) > 1e-10:
            ok2 = False
    check("S2  随机 su(2) 值矩阵雅可比恒等式（100 组）", ok2,
          f"max 残差 = {worst2:.2e}")

    # S3: 常系数联络的 Bianchi = 雅可比
    # ω 常系数：dω=0、Ω=ω∧ω（纯对易子）、dΩ=0、[ω,Ω] 3-形式分量 = 雅可比组合 = 0
    A, B, C = np.eye(2) * 0 + 0.7 * T1 + 0.3 * T2, 0.5 * T2 + 0.4 * T3, 0.6 * T3 + 0.2 * T1
    # Ω_yz = [B,C]、Ω_zx = [C,A]、Ω_xy = [A,B]（常系数，∂ 全零）
    O_yz = B @ C - C @ B
    O_zx = C @ A - A @ C
    O_xy = A @ B - B @ A
    # [ω,Ω] 3-形式分量 = [A,O_yz]+[B,O_zx]+[C,O_xy] = 雅可比(A,B,C)
    commutator3 = (A @ O_yz - O_yz @ A) + (B @ O_zx - O_zx @ B) + (C @ O_xy - O_xy @ C)
    jac = jacobi(A, B, C)
    ok3 = np.max(np.abs(commutator3)) < 1e-10 and np.max(np.abs(commutator3 - jac)) < 1e-10
    check("S3  常系数联络 Bianchi = 雅可比恒等式（[ω,Ω] 3-形式分量 ≡ 雅可比组合 = 0）", ok3,
          f"max 残差 = {np.max(np.abs(commutator3)):.2e}")

    # S4: 变系数 su(2) 值联络的完整 Bianchi dΩ+[ω,Ω]=0（数值差分，3 维网格）
    def field(x, y, z):
        """su(2) 值 1-形式分量 A,B,C（多项式系数）"""
        A = (x * x) * T1 + (x * y) * T2
        B = (y * y) * T2 + z * T3
        C = z * T1 + (x * z) * T3
        return A, B, C

    def d(f, x, y, z, axis, h=1e-3):
        """中心差分偏导 ∂_axis f（f 返回矩阵）"""
        pt = [x, y, z]
        ptp, ptm = list(pt), list(pt)
        ptp[axis] += h
        ptm[axis] -= h
        return (f(*ptp) - f(*ptm)) / (2 * h)

    worst4 = 0.0
    # Ω 分量的位置函数（任意点 (a,b,c) 处计算）
    def Omega_yz(a, b, c):
        Aa, Bb, Cc = field(a, b, c)
        return (d(lambda u, v, w: field(u, v, w)[2], a, b, c, 1)
                - d(lambda u, v, w: field(u, v, w)[1], a, b, c, 2)
                + (Bb @ Cc - Cc @ Bb))

    def Omega_zx(a, b, c):
        Aa, Bb, Cc = field(a, b, c)
        return (d(lambda u, v, w: field(u, v, w)[0], a, b, c, 2)
                - d(lambda u, v, w: field(u, v, w)[2], a, b, c, 0)
                + (Cc @ Aa - Aa @ Cc))

    def Omega_xy(a, b, c):
        Aa, Bb, Cc = field(a, b, c)
        return (d(lambda u, v, w: field(u, v, w)[1], a, b, c, 0)
                - d(lambda u, v, w: field(u, v, w)[0], a, b, c, 1)
                + (Aa @ Bb - Bb @ Aa))

    for x in (0.3, 0.7):
        for y in (0.4, 0.8):
            for z in (0.5, 0.9):
                A, B, C = field(x, y, z)
                O_yz, O_zx, O_xy = Omega_yz(x, y, z), Omega_zx(x, y, z), Omega_xy(x, y, z)
                # dΩ 的 3-形式分量：∂_x Ω_yz + ∂_y Ω_zx + ∂_z Ω_xy
                dO = d(Omega_yz, x, y, z, 0) \
                     + d(Omega_zx, x, y, z, 1) \
                     + d(Omega_xy, x, y, z, 2)
                # [ω,Ω] 3-形式分量：[A,Ω_yz]+[B,Ω_zx]+[C,Ω_xy]
                comm = (A @ O_yz - O_yz @ A) + (B @ O_zx - O_zx @ B) + (C @ O_xy - O_xy @ C)
                res = dO + comm
                worst4 = max(worst4, np.max(np.abs(res)))
    ok4 = worst4 < 1e-6
    check("S4  变系数 su(2) 值联络完整 Bianchi dΩ+[ω,Ω]=0（3 维网格数值差分）", ok4,
          f"max 残差 = {worst4:.2e}")

    # S5: 代数前提总结——d²=0（§8.5）+ 雅可比（本节）⟹ Bianchi（§8.2 第 3 项代数部分闭合）
    ok5 = ok1 and ok2 and ok3 and ok4
    check("S5  Bianchi 代数前提闭合：d²=0（§8.5 已验证）+ 雅可比恒等式（S1-S2）⟹ 完整 Bianchi（S3-S4）", ok5)

    results = [ok1, ok2, ok3, ok4, ok5]
    print("\n" + "=" * 78)
    print(f"雅可比/Bianchi 代数前提验证：{sum(results)}/5 通过")
    if not all(results):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
