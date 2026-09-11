"""Phase 16B 里程碑(b)预实验：度规缩并与 Einstein 散度的离散真值结构。

背景（sorry_closure_roadmap.md §3.6）：
  开放命题 EinsteinDivergenceFree 的离散真值载体需要"度规缩并"层的构造。
  连续理论中 ∇^μ G_μν = 0 依赖两件事：
    (i)   第二 Bianchi（∂ 项 + Γ 项联合）；
    (ii)  度量相容性 ∇_ρ g_{μν} = 0（用于升降指标穿过协变导数）。
  里程碑(a)已闭合算子层与骨架层 Bianchi；本实验回答缩并层的形式化之前
  必须先决的问题。

实验设计（Z_n^4 周期格点，四方向 step 对易，与 phase16b 同一约定：
  Γ^r_{mn} 下标对称；R^r_{sμν} = ∂̃_μ Γ^r_{νs} − ∂̃_ν Γ^r_{μs} + (Γ∧Γ)；
  Ricci_{σν} = Σ_r R^r_{σrν}）：

  族 P（精确相容族）：g_{μμ}(x) = η_{μμ}·(1+ε sin(2πk x^μ/n))，
    每个对角分量只依赖自身坐标。离散 Christoffel 公式给出 Γ^μ_{μμ}，
    可验证 A_{ρμν} := ∂̃_ρ g_{μν} − Γ^l_{ρμ}g_{lν} − Γ^l_{ρν}g_{μl}
    **逐点精确为零**（ρ=μ 项恒等抵消，ρ≠μ 项两边皆零）。
  族 G（一般光滑族）：g = η + ε·h，h 为低频对称扰动（含非对角），
    离散 Christoffel；A 不再精确为零，测其标度。

回答三个问题：
  Q1  族 P 的 A 是否机器精度为零（验证构造正确）；
  Q2  Einstein 协变散度 E_ν := Σ_μ (∇̃_μ G^·_ν)^μ 与 Bianchi 残差的
      度规缩并 C_ν := Σ ginv·ginv·B5 之间的代数关系：
      A=0 时是否精确恒等？A≠0 时差项是否正比于 A（线性结构）？
  Q3  |E|/|G| 与 |A| 随 n 的标度（连续极限检验）。

结论决定 Lean 形式化目标（沿用数值优先工作流，ENV_GUIDE 模式8）。

运行：python phase16b_metric_contraction.py
"""

import numpy as np

rng = np.random.default_rng(20260912)

ETA = np.diag([-1.0, 1.0, 1.0, 1.0])


# ---------------------------------------------------------------- 基本工具

def ddiff_dir(F, rho):
    """∂̃_ρ F(x) = F(step_ρ x) − F(x)，周期边界（step 自动对易）。"""
    return np.roll(F, -1, axis=-4 + rho) if F.ndim >= 4 and F.shape[-4] == 4 else np.roll(F, -1, axis=rho)


def ddiff(F, rho):
    """∂̃_ρ，方向轴固定为倒数第 4 轴（张量指标之后的格点轴）。"""
    return np.roll(F, -1, axis=F.ndim - 4 + rho)


def smooth_metric(n, eps=0.05, n_modes=3):
    """族 G：g = η + ε·h，h_{μν} 低频对称三角场（含非对角）。"""
    g = np.zeros((4, 4, n, n, n, n))
    g += ETA[:, :, None, None, None, None]
    for _ in range(n_modes):
        kvec = rng.integers(0, 2, size=4)
        if kvec.sum() == 0:
            kvec[0] = 1
        for mu in range(4):
            for nu in range(mu, 4):
                amp = rng.standard_normal() * np.exp(-0.5 * (mu + nu))
                phase = rng.uniform(0, 2 * np.pi)
                grid = np.zeros((n, n, n, n))
                for x0 in range(n):
                    grid[x0] = np.sin(2 * np.pi * np.dot(kvec, [x0, 0, 0, 0]) / n + phase)
                # 显式四坐标网格（低频，n≤32 可直接广播）
                idx = np.indices((n, n, n, n), dtype=float)
                kdotx = sum(kvec[a] * idx[a] for a in range(4))
                grid = np.sin(2 * np.pi * kdotx / n + phase)
                g[mu, nu] += eps * amp * grid
                g[nu, mu] = g[mu, nu]
    return g


def product_metric(n, eps=0.1, k=1):
    """族 P：对角、各分量只依赖自身坐标；离散相容 A ≡ 0（构造上）。"""
    g = np.zeros((4, 4, n, n, n, n))
    idx = np.indices((n, n, n, n), dtype=float)
    for mu in range(4):
        phase = 0.7 * mu + 0.3
        f = 1.0 + eps * np.sin(2 * np.pi * k * idx[mu] / n + phase)
        g[mu, mu] = ETA[mu, mu] * f
    return g


def invert_metric(g, n):
    """逐点求逆 ginv^{μν}(x)。"""
    ginv = np.zeros_like(g)
    for x0 in range(n):
        for x1 in range(n):
            for x2 in range(n):
                for x3 in range(n):
                    ginv[:, :, x0, x1, x2, x3] = np.linalg.inv(g[:, :, x0, x1, x2, x3])
    return ginv


def christoffel(g, ginv, n):
    """离散 Levi-Civita：Γ^ρ_{μν}(x) = ½ ginv^{ρσ}(∂̃_μ g_{νσ} + ∂̃_ν g_{μσ} − ∂̃_σ g_{μν})。"""
    G = np.zeros((4, 4, 4, n, n, n, n))
    for rho in range(4):
        for mu in range(4):
            for nu in range(4):
                t = np.zeros((n, n, n, n))
                for sigma in range(4):
                    t += ginv[rho, sigma] * (ddiff(g[nu, sigma], mu)
                                             + ddiff(g[mu, sigma], nu)
                                             - ddiff(g[mu, nu], sigma))
                G[rho, mu, nu] = 0.5 * t
    return G


def compatibility_residual(g, G, n):
    """A_{ρμν} = ∂̃_ρ g_{μν} − Γ^l_{ρμ} g_{lν} − Γ^l_{ρν} g_{μl}（度量相容残差）。"""
    A = np.zeros((4, 4, 4, n, n, n, n))
    for rho in range(4):
        for mu in range(4):
            for nu in range(4):
                t1 = sum(G[l, rho, mu] * g[l, nu] for l in range(4))
                t2 = sum(G[l, rho, nu] * g[mu, l] for l in range(4))
                A[rho, mu, nu] = ddiff(g[mu, nu], rho) - t1 - t2
    return A


def riemann_full(G, n):
    """R^r_{sμν}(x) = ∂̃_μ Γ^r_{νs} − ∂̃_ν Γ^r_{μs} + Γ^r_{μl}Γ^l_{νs} − Γ^r_{νl}Γ^l_{μs}。"""
    R = np.zeros((4, 4, 4, 4, n, n, n, n))
    for r in range(4):
        for s in range(4):
            for mu in range(4):
                for nu in range(4):
                    wedge = sum(G[r, mu, l] * G[l, nu, s] - G[r, nu, l] * G[l, mu, s]
                                for l in range(4))
                    R[r, s, mu, nu] = ddiff(G[r, nu, s], mu) - ddiff(G[r, mu, s], nu) + wedge
    return R


def ricci(R, n):
    """Ricci_{σν}(x) = Σ_r R^r_{σrν}(x)。"""
    Ric = np.zeros((4, 4, n, n, n, n))
    for s in range(4):
        for nu in range(4):
            Ric[s, nu] = sum(R[r, s, r, nu] for r in range(4))
    return Ric


def einstein(g, ginv, Ric, n):
    """R = ginv·Ricci；G_{μν} = R_{μν} − ½ g_{μν} R；G^μ_ν = ginv^{μα} G_{αν}。"""
    R = np.zeros((n, n, n, n))
    for s in range(4):
        for nu in range(4):
            R += ginv[s, nu] * Ric[s, nu]
    G_low = np.zeros_like(Ric)
    for mu in range(4):
        for nu in range(4):
            G_low[mu, nu] = Ric[mu, nu] - 0.5 * g[mu, nu] * R
    G_mixed = np.zeros_like(G_low)
    for mu in range(4):
        for nu in range(4):
            G_mixed[mu, nu] = sum(ginv[mu, a] * G_low[a, nu] for a in range(4))
    return R, G_low, G_mixed


def cov_diff_mixed(T, G, n, rho):
    """(∇̃_ρ T)^μ_ ν = ∂̃_ρ T^μ_ ν + Γ^μ_{ρl} T^l_ ν − Γ^l_{ρν} T^μ_ l（(1,1) 张量）。"""
    out = np.zeros_like(T)
    for mu in range(4):
        for nu in range(4):
            t1 = sum(G[mu, rho, l] * T[l, nu] for l in range(4))
            t2 = sum(G[l, rho, nu] * T[mu, l] for l in range(4))
            out[mu, nu] = ddiff(T[mu, nu], rho) + t1 - t2
    return out


def nabla_riemann(G, R, n, lam):
    """(∇̃_λ R)^r_{sμν} = ∂̃_λ R^r_{sμν} + Γ^r_{λl} R^l_{sμν} − Γ^l_{λs} R^r_{lμν}。"""
    out = np.zeros_like(R)
    for r in range(4):
        for s in range(4):
            for mu in range(4):
                for nu in range(4):
                    c1 = sum(G[r, lam, l] * R[l, s, mu, nu] for l in range(4))
                    c2 = sum(G[l, lam, s] * R[r, l, mu, nu] for l in range(4))
                    out[r, s, mu, nu] = ddiff(R[r, s, mu, nu], lam) + c1 - c2
    return out


def contracted_bianchi(g, ginv, G, R, n):
    """真循环 Bianchi 的两次度规缩并。

    BB^r_{sλμν} = (∇̃_λ R)^r_{sμν} + (∇̃_μ R)^r_{sνλ} + (∇̃_ν R)^r_{sλμ}（λ,μ,ν 两两不同）。
    一次缩并 K_{sμν} = Σ_{λ∉{μ,ν}} Σ_{c,a} ginv^{λc} g_{ca} BB^a_{sλμν}
      （导数方向 λ 与曲率上指标逐点缩并——离散点值骨架缩并）。
    二次缩并 D_ν = Σ_{sμ} ginv^{sμ} K_{sμν}。
    连续极限：K_{sμν} → 2(∇_μ R_{sν} − ∇_ν R_{sμ})，D_ν → 4∇^μ G_{μν}。
    """
    nablaR = [nabla_riemann(G, R, n, lam) for lam in range(4)]
    K = np.zeros((4, 4, 4, n, n, n, n))
    for lam in range(4):
        for mu in range(4):
            for nu in range(4):
                if len({lam, mu, nu}) < 3:
                    continue
                BB = (nablaR[lam][:, :, mu, nu]
                      + nablaR[mu][:, :, nu, lam]
                      + nablaR[nu][:, :, lam, mu])
                # BB^a_{s} 对 (a,s) 在 (lam,mu,nu) 槽位；K 索引按 (s,mu,nu) 存
                for s in range(4):
                    Kl = np.zeros((n, n, n, n))
                    for c in range(4):
                        BB_low = sum(g[c, a] * BB[a, s] for a in range(4))
                        Kl += ginv[lam, c] * BB_low
                    K[s, mu, nu] += Kl
    D = np.zeros((4, n, n, n, n))
    for nu in range(4):
        acc = np.zeros((n, n, n, n))
        for s in range(4):
            for mu in range(4):
                acc += ginv[s, mu] * K[s, mu, nu]
        D[nu] = acc
    return K, D


def einstein_divergence(G_mixed, G, n):
    """E_ν = Σ_μ (∇̃_μ G^·_ν)^μ。"""
    E = np.zeros((4, n, n, n, n))
    for nu in range(4):
        acc = np.zeros((n, n, n, n))
        for mu in range(4):
            dT = cov_diff_mixed(G_mixed, G, n, mu)
            acc += dT[mu, nu]
        E[nu] = acc
    return E


# ---------------------------------------------------------------- 实验主流程

def run_family(name, g, n, eps_desc="", with_D=False):
    ginv = invert_metric(g, n)
    G = christoffel(g, ginv, n)
    A = compatibility_residual(g, G, n)
    R4 = riemann_full(G, n)
    Ric = ricci(R4, n)
    Rsc, G_low, G_mixed = einstein(g, ginv, Ric, n)
    E = einstein_divergence(G_mixed, G, n)
    norms = dict(
        A=np.abs(A).max(),
        E=np.abs(E).max(),
        G=np.abs(G_low).max(),
    )
    print(f"  [{name} n={n:>2} {eps_desc}] |A|={norms['A']:.3e}  "
          f"|E|={norms['E']:.3e}  |G|={norms['G']:.3e}  "
          f"|E|/|G|={norms['E'] / max(norms['G'], 1e-300):.3e}")
    if with_D:
        K, D = contracted_bianchi(g, ginv, G, R4, n)
        alpha = float(np.vdot(E, D) / max(np.vdot(D, D), 1e-300))
        resid = np.abs(E - alpha * D).max()
        norms.update(D=np.abs(D).max(), alpha=alpha, resid=resid)
        print(f"      |D|={norms['D']:.3e}  拟合 α=⟨E,D⟩/⟨D,D⟩={alpha:.4f}  "
              f"|E − αD|={resid:.3e}  (|E|={norms['E']:.3e})")
    return norms


# ---------------------------------------------------------------- 骨架层检验

def skeleton_check(Gam, ginv, g, tag):
    """常值场骨架层 Einstein 协变散度（∂̃=0，联络项 + 度规缩并）。"""
    R = np.zeros((4, 4, 4, 4))
    for r in range(4):
        for s in range(4):
            for mu in range(4):
                for nu in range(4):
                    R[r, s, mu, nu] = sum(Gam[r, mu, l] * Gam[l, nu, s]
                                          - Gam[r, nu, l] * Gam[l, mu, s] for l in range(4))
    Ric = np.zeros((4, 4))
    for s in range(4):
        for nu in range(4):
            Ric[s, nu] = sum(R[r, s, r, nu] for r in range(4))
    Rsc = sum(ginv[s, nu] * Ric[s, nu] for s in range(4) for nu in range(4))
    G_low = np.zeros((4, 4))
    for mu in range(4):
        for nu in range(4):
            G_low[mu, nu] = Ric[mu, nu] - 0.5 * g[mu, nu] * Rsc
    E = np.zeros(4)
    for nu in range(4):
        acc = 0.0
        for mu in range(4):
            for a in range(4):
                conn = sum(-Gam[l, mu, a] * G_low[l, nu] - Gam[l, mu, nu] * G_low[a, l]
                           for l in range(4))
                acc += ginv[mu, a] * conn
        E[nu] = acc
    # 相容残差（常值：A = −Γ^l_{ρμ} g_{lν} − Γ^l_{ρν} g_{μl}）
    A = np.zeros((4, 4, 4))
    for rho in range(4):
        for mu in range(4):
            for nu in range(4):
                A[rho, mu, nu] = (-sum(Gam[l, rho, mu] * g[l, nu] for l in range(4))
                                  - sum(Gam[l, rho, nu] * g[mu, l] for l in range(4)))
    print(f"  [{tag}] |A|={np.abs(A).max():.3e}  |E_skel|={np.abs(E).max():.3e}")


def skeleton_layer():
    """定理 B 数值检验：常值 + 度规相容 ⟹ 骨架 Einstein 散度恒零；
    非相容对照组应为非零（证假设不可去）。"""
    print("\n--- 定理 B 骨架层检验（常值场，单点即全域）---")
    eta = ETA.copy()
    etainv = ETA.copy()
    # 相容组：Γ^i_{0j} = Γ^i_{j0} = ω_{ij}（无挠），Γ^0_{ij} = −ω_{ij}，
    # ω 反对称——手算验证 A ≡ 0（含 A_{i0j} 与 A_{0ij} 两组槽位）
    for w in (np.array([[0, 0.7, -0.4], [-0.7, 0, 0.9], [0.4, -0.9, 0]]),
              np.array([[0, 1.2, 0.3], [-1.2, 0, -0.8], [-0.3, 0.8, 0]])):
        Gam = np.zeros((4, 4, 4))
        for i in range(1, 4):
            for j in range(1, 4):
                Gam[i, 0, j] = w[i - 1, j - 1]
                Gam[i, j, 0] = w[i - 1, j - 1]  # 无挠：Γ^i_{j0} = Γ^i_{0j}
                Gam[0, i, j] = -w[i - 1, j - 1]
        skeleton_check(Gam, etainv, eta, "相容(ω-联络,无挠)")
    # 对照组：随机无挠常值 Γ（一般不相容）
    for trial in range(3):
        Gam = np.zeros((4, 4, 4))
        for r in range(4):
            for m in range(4):
                for nn in range(m, 4):
                    Gam[r, m, nn] = rng.standard_normal()
                    Gam[r, nn, m] = Gam[r, m, nn]
        skeleton_check(Gam, etainv, eta, f"非相容对照{trial + 1}")


def main():
    print("=" * 72)
    print("Phase 16B 里程碑(b)预实验：度规缩并与 Einstein 散度离散真值结构")
    print("=" * 72)

    print("\n--- Q1 度量相容残差：族 P 与族 G 的 A 量级 ---")
    for n in (4, 6):
        g = product_metric(n, eps=0.1, k=1)
        run_family("P(精确相容)", g, n, "eps=0.1")
    for n in (4, 6):
        g = smooth_metric(n, eps=0.05, n_modes=3)
        run_family("G(一般光滑)", g, n, "eps=0.05")

    print("\n--- Q2 恒等式检验：E ?= α·缩并(Bianchi)（n=6，族 P/G）---")
    for name, g in [("P", product_metric(6, eps=0.1, k=1)),
                    ("G", smooth_metric(6, eps=0.05, n_modes=3))]:
        run_family(name, g, 6, with_D=True)

    print("\n--- Q3 连续极限标度 ---")
    print("  族 P（E 与 A）：")
    prev = None
    for n in (8, 16, 32):
        g = product_metric(n, eps=0.1, k=1)
        nm = run_family("P", g, n)
        ratio = nm['E'] / max(nm['G'], 1e-300)
        if prev is not None:
            print(f"      |E|/|G| 减半因子 {prev / ratio:.2f}（2 ⇒ O(a)，4 ⇒ O(a²)）")
        prev = ratio
    print("  族 G（E 与 A）：")
    prev = None
    for n in (8, 16, 32):
        g = smooth_metric(n, eps=0.05, n_modes=3)
        nm = run_family("G", g, n)
        ratio = nm['E'] / max(nm['G'], 1e-300)
        prev = ratio

    skeleton_layer()


if __name__ == "__main__":
    main()
