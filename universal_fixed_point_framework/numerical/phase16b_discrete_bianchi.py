"""Phase 16B 预实验：含 ∂̃ 项的离散第二 Bianchi 恒等式检验。

背景（sorry_closure_roadmap.md §3.6）：
  点值代数骨架 second_bianchi_discrete（无 ∂ 项）已机器证明，但 Einstein 散度
  恒假——守恒律载体在 ∂ 项。真值路径：沿 RecObj step 四方向化的有限差分导数
      ∂̃_ρ T(x) := T(step_ρ x) − T(x)
  重建带 ∂ 项的离散第二 Bianchi。

本实验回答形式化之前必须先决的问题：
  在 Z_n^4 周期格点（四方向 step 对易）上，取随机无挠 Γ 场，
  完整曲率 R^r_{sμν}(x) = ∂̃_μ Γ^r_{νs}(x) − ∂̃_ν Γ^r_{μs}(x) + (Γ∧Γ)(x)
  与协变差分 ∇̃_ρ R = ∂̃_ρ R + connAct(Γ, R) 下，
  循环和 Bianchi(x) = Σ_cyc(ρ,μ,ν) ∇̃_ρ R^r_{sμν}(x) 是否逐点恒零？

  若不恒零，分离出修正项（候选：O((∂̃Γ)^2) 型，来自离散 Leibniz 的
  ∂̃(AB) = ∂̃A·B + A·∂̃B + ∂̃A·∂̃B 修正），并检验其量级随格距缩小的标度。

结论决定 Lean 形式化目标：
  (a) 恒零 → 直接形式化恒等式（ring 路径，需 sum4 桥接）；
  (b) 非恒零但修正项有干净结构 → 形式化"主项 + 显式修正"命题；
  (c) 修正项混乱 → 改用算子 Jacobi 路径（协变导数视为场空间自同态，
     第二 Bianchi = [D_ρ,[D_μ,D_ν]] 循环和 = 0，noncomm_ring 恒等式）。

运行：python phase16b_discrete_bianchi.py
"""

import numpy as np

rng = np.random.default_rng(20260911)


def random_torsion_free_gamma(n, scale=1.0):
    """随机无挠 Christoffel 场 Γ^r_{mn}(x)，Γ^r_{mn} = Γ^r_{nm}。

    参数化：对每 r, m<=n 独立高斯采样，再对称补齐。
    返回 shape (4, 4, 4, n, n, n, n)：Γ[r, m, n, x0, x1, x2, x3]。
    """
    G = np.zeros((4, 4, 4, n, n, n, n))
    for r in range(4):
        for m in range(4):
            for nn in range(m, 4):
                G[r, m, nn] = scale * rng.standard_normal((n, n, n, n))
                G[r, nn, m] = G[r, m, nn]
    return G


def ddiff_dir(G, rho, n):
    """∂̃_ρ G(x) = G(step_ρ x) − G(x)，步长 1（周期边界，自动对易）。

    G 为 4 维格点场 (n,n,n,n)，rho ∈ {0,1,2,3} 为方向轴。"""
    return np.roll(G, -1, axis=rho) - G


def riemann_full(G, n):
    """完整离散曲率 R^r_{sμν}(x) = ∂̃_μ Γ^r_{νs} − ∂̃_ν Γ^r_{μs} + (Γ∧Γ)。

    返回 shape (4, 4, 4, 4, n,n,n,n)：R[r, s, mu, nu, x...]。
    """
    # (Γ∧Γ)^r_{sμν} = Σ_l Γ^r_{μl} Γ^l_{νs} − Γ^r_{νl} Γ^l_{μs}
    wedge = np.zeros((4, 4, 4, 4, n, n, n, n))
    for r in range(4):
        for s in range(4):
            for mu in range(4):
                for nu in range(4):
                    t1 = sum(G[r, mu, l] * G[l, nu, s] for l in range(4))
                    t2 = sum(G[r, nu, l] * G[l, mu, s] for l in range(4))
                    wedge[r, s, mu, nu] = t1 - t2
    R = np.zeros_like(wedge)
    for r in range(4):
        for s in range(4):
            for mu in range(4):
                for nu in range(4):
                    d_mu = ddiff_dir(G[r, nu, s], mu, n)
                    d_nu = ddiff_dir(G[r, mu, s], nu, n)
                    R[r, s, mu, nu] = d_mu - d_nu + wedge[r, s, mu, nu]
    return R


def conn_act(G, T, rho, r, s, mu, nu, n):
    """联络作用 (∇̃_ρ T)^r_{sμν} 的联络项 = Σ_l Γ^r_{ρl} T^l_{sμν} − Γ^l_{ρs} T^r_{lμν}。"""
    t1 = sum(G[r, rho, l] * T[l, s, mu, nu] for l in range(4))
    t2 = sum(G[l, rho, s] * T[r, l, mu, nu] for l in range(4))
    return t1 - t2


def bianchi_residual(G, n):
    """B(x) = Σ_cyc(ρ,μ,ν) [∂̃_ρ R^r_{sμν} + connAct(Γ, R, ρ)](x)，返回张量 shape (4,4,4,n,n,n,n)。"""
    R = riemann_full(G, n)
    B = np.zeros((4, 4, 4, n, n, n, n))
    for r in range(4):
        for s in range(4):
            acc = np.zeros((n, n, n, n))
            for rho, mu, nu in [(0, 1, 2), (1, 2, 0), (2, 0, 1)]:
                d_rho = ddiff_dir(R[r, s, mu, nu], rho, n)
                conn = conn_act(G, R, rho, r, s, mu, nu, n)
                acc += d_rho + conn
            B[r, s, 0] = acc  # 存入 nu=0 槽位仅作汇总展示
    return B


def build_operators(G, n):
    """把协变差分 D_ρ 建成场空间 V = (Z_n^4 → R^4) 上的矩阵（行优先展平）。

    (D_ρ V)^r(x) = V^r(step_ρ x) − V^r(x) + Σ_l M_ρ[r,l](x) V^l(x)，
    M_ρ[r,l](x) = Γ^r_{ρl}(x)。
    返回 D[4]：shape (4N, 4N)，N = n^4。
    """
    N = n ** 4
    D = np.zeros((4, 4 * N, 4 * N))

    def idx(x, r):
        return 4 * x + r

    # 预展平格点坐标
    for x0 in range(n):
        for x1 in range(n):
            for x2 in range(n):
                for x3 in range(n):
                    x = ((x0 * n + x1) * n + x2) * n + x3
                    for rho in range(4):
                        xs = list((x0, x1, x2, x3))
                        xs[rho] = (xs[rho] + 1) % n
                        sx = ((xs[0] * n + xs[1]) * n + xs[2]) * n + xs[3]
                        for r in range(4):
                            row = idx(x, r)
                            D[rho, row, idx(sx, r)] += 1.0   # 移位项
                            D[rho, row, idx(x, r)] -= 1.0    # −1 项
                            for l in range(4):
                                D[rho, row, idx(x, l)] += G[r, rho, l, x0, x1, x2, x3]
    return D


def operator_jacobi_check(n=3, scale=1.0):
    """验证算子 Jacobi：Σ_cyc [D_ρ,[D_μ,D_ν]] = 0（机器精度）。"""
    G = random_torsion_free_gamma(n, scale)
    D = build_operators(G, n)
    F = [[D[mu] @ D[nu] - D[nu] @ D[mu] for nu in range(4)] for mu in range(4)]
    J = np.zeros_like(D[0])
    for rho, mu, nu in [(0, 1, 2), (1, 2, 0), (2, 0, 1)]:
        J = J + D[rho] @ F[mu][nu] - F[mu][nu] @ D[rho]
    return np.abs(J).max()


def smooth_gamma(n, amp=1.0, k=1):
    """光滑（低频）无挠 Γ 场：Γ^r_{mn}(x) = amp·sin(2πk x^0/n)·δ 型慢变场。"""
    G = np.zeros((4, 4, 4, n, n, n, n))
    for r in range(4):
        for m in range(4):
            for nn in range(m, 4):
                phase = 0.3 * r + 0.5 * m + 0.2 * nn
                for x0 in range(n):
                    val = amp * np.sin(2 * np.pi * k * x0 / n + phase)
                    G[r, m, nn, x0, :, :, :] = val
                    G[r, nn, m, x0, :, :, :] = val
    return G


def continuum_scaling():
    """分量 Bianchi 残差随光滑性/格距细化而消失（连续极限检验）。"""
    print("\n--- 连续极限标度：光滑 Γ 场，分量残差 vs 格距 ---")
    for n in (8, 16, 32):
        G = smooth_gamma(n, amp=1.0, k=1)
        B = bianchi_residual(G, n)
        R = riemann_full(G, n)
        ratio = np.abs(B).max() / np.abs(R).max()
        print(f"  n={n:>2}: |B|_max={np.abs(B).max():.3e}  |R|_max={np.abs(R).max():.3e}  "
              f"|B|/|R|={ratio:.3e}")


def main():
    print("=" * 70)
    print("Phase 16B 预实验：含 ∂̃ 项的离散第二 Bianchi 恒等式检验")
    print("=" * 70)
    for n in (3, 4):
        for scale in (0.5, 1.0):
            G = random_torsion_free_gamma(n, scale)
            B = bianchi_residual(G, n)
            max_abs = np.abs(B).max()
            R = riemann_full(G, n)
            dG = np.stack([ddiff_dir(G, rho, n) for rho in range(4)])
            print(f"\n格点 n={n}, Γ 尺度={scale}:")
            print(f"  |Bianchi|_max（分量式）  = {max_abs:.3e}")
            print(f"  |R|_max                  = {np.abs(R).max():.3e}")
            print(f"  |∂̃Γ|_max                 = {np.abs(dG).max():.3e}")
            print(f"  相对 |∂̃Γ·Γ| 比值        = "
                  f"{max_abs / (np.abs(dG).max() * np.abs(G).max()):.3e}")

    print("\n--- 算子 Jacobi 精确性（随机场，应为机器精度 0）---")
    for n in (3, 4):
        for scale in (0.5, 1.0):
            res = operator_jacobi_check(n, scale)
            print(f"  n={n}, Γ 尺度={scale}: |Σ_cyc[D_ρ,[D_μ,D_ν]]|_max = {res:.3e}")

    continuum_scaling()


if __name__ == "__main__":
    main()
