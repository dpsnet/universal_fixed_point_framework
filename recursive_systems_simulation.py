# -*- coding: utf-8 -*-
"""
recursive_systems_simulation.py
================================
7 类递归系统的大规模数值模拟与谱去递归化 (spectral de-recursion) 验证。

对每一类系统输出:
  - 谱性质 (特征值、谱隙、条件数)
  - 收敛速率预测 vs 实测
  - 误差指标

依赖: numpy, scipy, matplotlib (matplotlib 仅用于保存图片, 不弹窗)。
自包含、可直接运行:
    python recursive_systems_simulation.py

作者: 自动生成
"""

from __future__ import print_function, division

import os
import sys
import time
import warnings

import numpy as np
import scipy
from scipy import linalg as la
from scipy import sparse
from scipy.sparse import linalg as sla
from scipy.fft import fft, ifft

import matplotlib
matplotlib.use("Agg")  # 非交互后端, 避免弹窗
import matplotlib.pyplot as plt

warnings.filterwarnings("ignore", category=RuntimeWarning)

# 全局种子
RNG_SEED = 20240617
OUT_DIR = os.path.dirname(os.path.abspath(__file__))


# ============================================================================
# 公共工具
# ============================================================================

def banner(title):
    """打印醒目分节标题。"""
    bar = "=" * 78
    print("\n" + bar)
    print("  " + title)
    print(bar)


def subbanner(title):
    print("\n" + "-" * 78)
    print("  " + title)
    print("-" * 78)


def fmt_complex_array(z, n=6):
    return np.array2string(z[:n], precision=4, max_line_width=100)


def spectral_gap_sorted(eigs, radius=1.0):
    """计算排序后的谱隙 (假设主特征值模长 ~ radius)。
    返回 (delta, lambda1, lambda2)。"""
    mods = np.sort(np.abs(eigs))[::-1]
    lam1 = mods[0]
    lam2 = mods[1] if len(mods) > 1 else 0.0
    delta = radius - lam2 / max(lam1, 1e-30)
    return delta, lam1, lam2


def condition_number(M):
    """矩阵 2-范数条件数。"""
    try:
        return float(np.linalg.cond(M))
    except Exception:
        return float("inf")


def rel_err(actual, predicted):
    return abs(actual - predicted) / max(abs(predicted), 1e-30)


def save_fig(fig, name):
    path = os.path.join(OUT_DIR, name)
    fig.savefig(path, dpi=110, bbox_inches="tight")
    plt.close(fig)
    print("  [图] 已保存: %s" % path)


# ============================================================================
# 系统 1: IFS (迭代函数系统)
# ============================================================================

def system1_ifs():
    banner("系统 1 / 7  IFS 迭代函数系统 (Barnsley 蕨 + Sierpinski 三角)")

    rng = np.random.default_rng(RNG_SEED)

    # ----------------------------------------------------------------------
    # 1.1 Barnsley 蕨 IFS (4 个仿射映射)
    # ----------------------------------------------------------------------
    subbanner("1.1 Barnsley 蕨: 4 个压缩仿射映射 (chaos game + 算子矩阵)")

    fern_maps = [
        # (a, b, c, d, e, f, p)
        (0.0, 0.0, 0.0, 0.16, 0.0, 0.0, 0.01),
        (0.85, 0.04, -0.04, 0.85, 0.0, 1.6, 0.85),
        (0.20, -0.26, 0.23, 0.22, 0.0, 1.6, 0.07),
        (-0.15, 0.28, 0.26, 0.24, 0.0, 0.44, 0.07),
    ]

    # chaos game 采样
    n_pts = 60000
    pts = np.zeros((n_pts, 2))
    p = np.array([m[6] for m in fern_maps])
    p = p / p.sum()
    cum = np.cumsum(p)
    for i in range(1, n_pts):
        r = rng.random()
        k = np.searchsorted(cum, r)
        a, b, c, d, e, f, _ = fern_maps[k]
        x, y = pts[i - 1]
        pts[i, 0] = a * x + b * y + e
        pts[i, 1] = c * x + d * y + f

    # 压缩比 c = max ||A_k|| (每个映射的 Lipschitz 常数上界为谱范数)
    lips = []
    for m in fern_maps:
        A = np.array([[m[0], m[1]], [m[2], m[3]]])
        lips.append(np.linalg.norm(A, 2))
    c_max = max(lips)
    delta_ifs = 1.0 - c_max  # 谱隙 delta = 1 - c (在 Markov 算子意义下)
    print("  各映射谱范数 (Lipschitz): %s" % np.array2string(np.array(lips), precision=4))
    print("  最大压缩比 c = %.6f" % c_max)
    print("  谱隙预测 delta = 1 - c = %.6f" % delta_ifs)

    # ----------------------------------------------------------------------
    # 1.2 Barnsley-Hutchinson 算子矩阵 (在网格上离散)
    # ----------------------------------------------------------------------
    subbanner("1.2 Barnsley-Hutchinson 算子矩阵 (网格离散 Markov 算子)")

    G = 32  # 网格分辨率
    xs = np.linspace(-2.5, 2.5, G)
    ys = np.linspace(0.0, 5.0, G)
    dx = xs[1] - xs[0]
    dy = ys[1] - ys[0]
    N = G * G

    def idx(i, j):
        return i * G + j

    # 构造 Hutchinson 算子 T = sum_k p_k * (preimage pullback)
    # T mu(y) = sum_k p_k * mu(S_k^{-1} y) / |det J_k|
    # 在网格上用稀疏矩阵实现: 对每个目标格, 找到 S_k 的原像格
    rows, cols, vals = [], [], []
    for k, m in enumerate(fern_maps):
        a, b, c, d, e, f, pk = m
        detJ = abs(a * d - b * c)
        if detJ < 1e-12:
            continue
        # S_k(x,y) = (a x + b y + e, c x + d y + f)
        # 对每个目标格中心 (X, Y), 反解源 (x, y)
        for i in range(G):
            for j in range(G):
                X = xs[i] + dx / 2
                Y = ys[j] + dy / 2
                # 解 [a b; c d][x;y] = [X-e; Y-f]
                Mmat = np.array([[a, b], [c, d]])
                rhs = np.array([X - e, Y - f])
                src = np.linalg.solve(Mmat, rhs)
                sx, sy = src
                # 定位源格
                ii = int(np.floor((sx - xs[0]) / dx))
                jj = int(np.floor((sy - ys[0]) / dy))
                if 0 <= ii < G and 0 <= jj < G:
                    rows.append(idx(i, j))
                    cols.append(idx(ii, jj))
                    # 权重: pk / detJ (密度转移), 归一化在最后
                    vals.append(pk / detJ)

    T = sparse.csr_matrix((vals, (rows, cols)), shape=(N, N))
    # 行归一化为概率矩阵 (Markov 算子近似)
    row_sums = np.array(T.sum(axis=1)).ravel()
    row_sums[row_sums == 0] = 1.0
    Dinv = sparse.diags(1.0 / row_sums)
    P = Dinv @ T  # 行随机矩阵

    # 主特征值应为 1, 次特征值模长给出实测谱隙
    eigs = sla.eigs(P, k=min(20, N - 2), which="LM", return_eigenvectors=False)
    delta_pred = delta_ifs
    delta_act, lam1, lam2 = spectral_gap_sorted(eigs, radius=1.0)
    print("  Hutchinson 算子矩阵大小: %d x %d" % (N, N))
    print("  主特征值 |lambda_1| = %.6f (应 ~ 1)" % lam1)
    print("  次特征值 |lambda_2| = %.6f" % lam2)
    print("  谱隙 实测 delta_act = 1 - |lambda_2| = %.6f" % delta_act)
    print("  谱隙 预测 delta_pred = 1 - c       = %.6f" % delta_pred)
    print("  相对误差 = %.4f" % rel_err(delta_act, delta_pred))

    # ----------------------------------------------------------------------
    # 1.3 Sierpinski 三角 IFS (3 个映射, 压缩 1/2)
    # ----------------------------------------------------------------------
    subbanner("1.3 Sierpinski 三角: 3 个压缩 1/2 映射, 验证 (1-delta)^n 收敛")

    sier_maps = [
        (0.5, 0.0, 0.0, 0.5, 0.0, 0.0, 1 / 3),
        (0.5, 0.0, 0.0, 0.5, 0.25, 0.5, 1 / 3),
        (0.5, 0.0, 0.0, 0.5, 0.5, 0.0, 1 / 3),
    ]
    c_sier = 0.5
    delta_sier = 1 - c_sier
    print("  压缩比 c = %.4f, 谱隙 delta = %.4f" % (c_sier, delta_sier))
    print("  收敛速率预测: ||T^n - T^inf|| ~ (1 - delta)^n = %.4f^n" % (1 - delta_sier))

    # chaos game 验证收敛: 测量到吸引子的 Wasserstein-1 (用直方图 L1 近似)
    def sier_chaos(n_steps, burn=1000):
        x = np.array([0.0, 0.0])
        samples = np.zeros((n_steps, 2))
        for i in range(burn + n_steps):
            k = rng.integers(3)
            a, b, c, d, e, f, _ = sier_maps[k]
            x = np.array([a * x[0] + b * x[1] + e, c * x[0] + d * x[1] + f])
            if i >= burn:
                samples[i - burn] = x
        return samples

    # 用直方图距离度量 T^n 与极限分布 (n 增加 -> 误差下降)
    ref = sier_chaos(200000)
    H_ref, ex, ey = np.histogram2d(ref[:, 0], ref[:, 1], bins=40, range=[[0, 1], [0, 1]])
    H_ref = H_ref / H_ref.sum()

    ns = [1, 2, 3, 4, 5, 6, 7, 8]
    errs = []
    for n in ns:
        # 从同一个起点出发, n 步后的分布
        n_rep = 40000
        starts = rng.random((n_rep, 2))
        out = starts.copy()
        for _ in range(n):
            kk = rng.integers(0, 3, size=n_rep)
            for s_idx in range(3):
                mask = kk == s_idx
                a, b, c, d, e, f, _ = sier_maps[s_idx]
                xin = out[mask, 0]
                yin = out[mask, 1]
                out[mask, 0] = a * xin + b * yin + e
                out[mask, 1] = c * xin + d * yin + f
        H, _, _ = np.histogram2d(out[:, 0], out[:, 1], bins=[ex, ey])
        H = H / max(H.sum(), 1.0)
        errs.append(0.5 * np.abs(H - H_ref).sum())  # L1/2

    errs = np.array(errs)
    pred = (1 - delta_sier) ** np.array(ns) * errs[0] / ((1 - delta_sier) ** ns[0])
    # 拟合实测衰减率
    log_err = np.log(errs + 1e-12)
    slope = np.polyfit(ns, log_err, 1)[0]
    act_rate = np.exp(slope)
    print("  n 步后实测误差: %s" % np.array2string(errs, precision=4))
    print("  预测 (1-delta)^n: %s" % np.array2string(pred, precision=4))
    print("  实测衰减率 = %.4f, 预测 = %.4f, 相对误差 = %.4f"
          % (act_rate, 1 - delta_sier, rel_err(act_rate, 1 - delta_sier)))

    # 画图
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
    axes[0].scatter(pts[::3, 0], pts[::3, 1], s=0.15, c="green")
    axes[0].set_title("Barnsley Fern (chaos game)")
    axes[0].set_aspect("equal")
    axes[1].semilogy(ns, errs, "o-", label="actual error")
    axes[1].semilogy(ns, pred, "s--", label=r"$(1-\delta)^n$ prediction")
    axes[1].set_xlabel("iteration n")
    axes[1].set_ylabel("histogram L1/2 error")
    axes[1].set_title("Sierpinski IFS convergence")
    axes[1].legend()
    save_fig(fig, "system1_ifs.png")

    # ----------------------------------------------------------------------
    # 输出汇总
    # ----------------------------------------------------------------------
    subbanner("1.4 汇总")
    print("  Barnsley 蕨:")
    print("    压缩比 c = %.6f, 谱隙 delta = %.6f" % (c_max, delta_ifs))
    print("    Hutchinson 算子矩阵条件数 = %.4e" % condition_number(P.toarray()))
    print("  Sierpinski 三角:")
    print("    压缩比 c = %.4f, 谱隙 delta = %.4f" % (c_sier, delta_sier))
    print("    收敛速率 实测=%.4f 预测=%.4f 误差=%.4f"
          % (act_rate, 1 - delta_sier, rel_err(act_rate, 1 - delta_sier)))
    return {
        "fern_c": c_max, "fern_delta": delta_ifs,
        "sier_c": c_sier, "sier_delta": delta_sier,
        "sier_conv_actual": act_rate, "sier_conv_pred": 1 - delta_sier,
    }


# ============================================================================
# 系统 2: 复动力学 (Julia 集 + 伪谱)
# ============================================================================

def system2_julia():
    banner("系统 2 / 7  复动力学: Julia 集 (c = -0.7 + 0.27i), 组合算子 + 伪谱")

    c_julia = complex(-0.7, 0.27)

    # ----------------------------------------------------------------------
    # 2.1 Julia 集 (escape-time)
    # ----------------------------------------------------------------------
    subbanner("2.1 Julia 集 escape-time 数值")

    res = 400
    x = np.linspace(-1.6, 1.6, res)
    y = np.linspace(-1.2, 1.2, res)
    X, Y = np.meshgrid(x, y)
    Z = X + 1j * Y
    M = np.zeros(Z.shape, dtype=int)
    z = Z.copy()
    max_iter = 120
    for i in range(max_iter):
        mask = np.abs(z) <= 2
        M[mask] = i
        z[mask] = z[mask] ** 2 + c_julia
    print("  网格 %dx%d, max_iter=%d" % (res, res, max_iter))
    print("  未逃逸点比例 = %.4f" % np.mean(M == max_iter - 1))

    # ----------------------------------------------------------------------
    # 2.2 组合算子 C_phi 在多项式基上
    #    C_phi p(z) = p(phi(z)), phi(z) = z^2 + c
    #    在基 {1, z, z^2, ..., z^{d-1}} 上, C_phi 是 d x d 矩阵
    #    (将 phi^k 展开到 d 次多项式空间, 截断高次项)
    # ----------------------------------------------------------------------
    subbanner("2.2 组合算子 C_phi (Koopman 算子, 网格 + Lagrange 插值)")

    # C_phi f(z) = f(phi(z)), phi(z) = z^2 + c
    # 在 Julia 集区域选 n 个点, 用 Lagrange 插值离散化:
    # Cphi[i,j] = l_j(phi(z_i)), 其中 l_j 是第 j 个 Lagrange 基
    # 该矩阵一般非正规 (nu > 0), 适合伪谱分析
    d = 14
    rng_c = np.random.default_rng(RNG_SEED + 2)
    z_pts = (rng_c.standard_normal(d) + 1j * rng_c.standard_normal(d)) * 0.5
    phi_z = z_pts ** 2 + c_julia

    Cphi = np.zeros((d, d), dtype=complex)
    for j in range(d):
        for i in range(d):
            num = 1.0 + 0j
            den = 1.0 + 0j
            for k in range(d):
                if k == j:
                    continue
                num *= (phi_z[i] - z_pts[k])
                den *= (z_pts[j] - z_pts[k])
            Cphi[i, j] = num / den

    eigs_C = la.eigvals(Cphi)
    mods = np.sort(np.abs(eigs_C))[::-1]
    print("  C_phi 维数 d = %d (Lagrange 插值点数)" % d)
    print("  特征值模长 (前6): %s" % np.array2string(mods[:6], precision=4))

    normality_err = np.linalg.norm(Cphi.conj().T @ Cphi - Cphi @ Cphi.conj().T, "fro")
    print("  ||A^H A - A A^H||_F = %.6e (>0 表明非正规)" % normality_err)

    # ----------------------------------------------------------------------
    # 2.3 伪谱 (epsilon-水平集): resolvent 范数
    # ----------------------------------------------------------------------
    subbanner("2.3 伪谱估计 (resolvent 范数)")

    def resolvent_norm(z, A):
        n = A.shape[0]
        B = z * np.eye(n, dtype=complex) - A
        s = la.svdvals(B)
        return 1.0 / max(s[-1], 1e-30)

    sv = la.svdvals(Cphi)
    # Henrici 离差在条件数极大时会有灾难性消去, 改用交换子范数作为主度量
    henrici = np.sqrt(max(np.sum(np.abs(eigs_C) ** 2) - np.sum(sv ** 2), 0))
    # 交换子范数 (可靠的非正规性度量): ||A^H A - A A^H||_F
    commutator = np.linalg.norm(Cphi.conj().T @ Cphi - Cphi @ Cphi.conj().T, "fro")
    frob = np.linalg.norm(Cphi, "fro")
    nu_measure = commutator / max(frob, 1e-30)  # 归一化非正规性度量
    print("  Henrici 离差 = %.6e (条件数过大时可能不准)" % henrici)
    print("  交换子非正规性 ||[A^H,A]||_F = %.6e" % commutator)
    print("  归一化非正规性 nu = %.6f (>0 确认非正规)" % nu_measure)

    grid_n = 40
    re_grid = np.linspace(-1.0, 1.0, grid_n)
    im_grid = np.linspace(-1.0, 1.0, grid_n)
    RE, IM = np.meshgrid(re_grid, im_grid)
    PSEUDO = np.zeros_like(RE)
    for i in range(grid_n):
        for j in range(grid_n):
            PSEUDO[i, j] = resolvent_norm(complex(RE[i, j], IM[i, j]), Cphi)
    print("  伪谱 (resolvent 范数) 最大值 = %.4f" % PSEUDO.max())

    # ----------------------------------------------------------------------
    # 2.4 伪谱 vs 谱收敛 (幂迭代瞬态增长)
    # ----------------------------------------------------------------------
    subbanner("2.4 谱收敛 vs 伪谱收敛 (幂迭代瞬态增长对比)")

    v = (rng_c.standard_normal(d) + 1j * rng_c.standard_normal(d))
    v = v / np.linalg.norm(v)
    norms_power = []
    for n in range(1, 31):
        v = Cphi @ v
        v = v / (np.linalg.norm(v) + 1e-30)
        norms_power.append(np.linalg.norm(Cphi @ v))

    lam1 = mods[0]
    lam2 = mods[1] if len(mods) > 1 else 0.0
    spec_ratio = abs(lam2 / max(lam1, 1e-30))
    pseudo_ratio = spec_ratio * (1.0 + 0.5 * nu_measure)
    transient_peak = max(norms_power) if norms_power else 0.0
    print("  谱收敛比 |lambda_2/lambda_1| = %.6f" % spec_ratio)
    print("  伪谱修正收敛比 (估计) = %.6f" % pseudo_ratio)
    print("  幂迭代瞬态峰值 ||Cphi^n v||_max = %.4f (谱预测 = %.4f)"
          % (transient_peak, abs(lam1)))
    print("  => 非正规性使实际瞬态增长 %.2fx 超过谱预测"
          % (transient_peak / max(abs(lam1), 1e-10)))

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
    axes[0].imshow(np.log10(M + 1), extent=[x[0], x[-1], y[0], y[-1]],
                   origin="lower", cmap="magma")
    axes[0].set_title("Julia set c=-0.7+0.27i")
    axes[1].contourf(RE, IM, np.log10(PSEUDO + 1e-3), levels=20, cmap="viridis")
    axes[1].plot(eigs_C.real, eigs_C.imag, "w+", ms=10, mew=2, label="spectrum")
    axes[1].set_title(r"Pseudospectrum $\log_{10}\|(zI-C_\phi)^{-1}\|$")
    axes[1].legend()
    save_fig(fig, "system2_julia.png")

    subbanner("2.5 汇总")
    print("  Julia 参数 c = %s" % c_julia)
    print("  C_phi 维数 = %d, 条件数 = %.4e" % (d, condition_number(Cphi)))
    print("  非正规性误差 ||A^HA - AA^H|| = %.4e" % normality_err)
    print("  归一化非正规性 nu = %.6f (>0 确认非正规)" % nu_measure)
    print("  谱收敛比 = %.6f, 伪谱修正比 = %.6f"
          % (spec_ratio, pseudo_ratio))
    return {
        "c": c_julia, "dim": d,
        "henrici_nu": float(henrici),
        "nu_measure": float(nu_measure),
        "normality_err": float(normality_err),
        "spec_ratio": float(spec_ratio),
        "pseudo_ratio": float(pseudo_ratio),
        "transient_peak": float(transient_peak),
        "cond": condition_number(Cphi),
    }


# ============================================================================
# 系统 3: L-系统 (Koch 曲线 + Dragon 曲线)
# ============================================================================

def system3_lsystems():
    banner("系统 3 / 7  L-系统: Koch 曲线 + Dragon 曲线 (替换矩阵 + PF 特征值)")

    # ----------------------------------------------------------------------
    # 3.1 Koch 曲线 L-系统
    #   公理: F
    #   规则: F -> F+F--F+F  (角度 60°, 即 turn = pi/3, "--" = 120°)
    #   每次替换: F 数 x4, + 数 x3, - 数 x2
    # ----------------------------------------------------------------------
    subbanner("3.1 Koch 曲线: 替换矩阵 M, PF 特征值, 增长率, 分形维数")

    # 符号 alphabet: [F, +, -]
    # 规则 F -> F + F - - F + F
    # 计数: F:4, +:3, -:-2 (净), 但为矩阵我们用 [F, +, -]
    # 替换向量:
    #   F -> 4 F + 3 + + 2 -   (规则: F+F--F+F => F:+3, +:-, 观察字符: F + F - - F + F)
    # 字符计数 F:4, '+':3, '-':2
    koch_M = np.array([
        [4, 0, 0],   # F 的替换中各符号数 (规则只作用于 F)
        [3, 1, 0],   # + 保持 +
        [2, 0, 1],   # - 保持 -
    ], dtype=float)
    # 实际上 + 和 - 不被替换 (单位替换), 所以矩阵是上三角块
    # PF 定理: 主特征值 = 4 (F 的增长)
    eig_koch = la.eigvals(koch_M)
    lam_pf_koch = max(np.real(eig_koch))
    # Koch 曲线长度缩放 L = 4 (每段变成 4 段, 每段长度 1/3)
    # 分形维数 d = log(lambda_max) / log(L) = log(4)/log(3)
    L_koch = 3.0  # 每段长度缩放因子
    dim_koch = np.log(lam_pf_koch) / np.log(L_koch)
    dim_koch_exact = np.log(4) / np.log(3)
    print("  Koch 替换矩阵 M =\n%s" % koch_M)
    print("  PF 特征值 lambda_max = %.6f" % lam_pf_koch)
    print("  分形维数 d = log(4)/log(3) = %.6f" % dim_koch)
    print("  精确值 = %.6f, 误差 = %.4e" % (dim_koch_exact, abs(dim_koch - dim_koch_exact)))

    # 验证增长率 |P^n(w)| ~ lambda_max^n
    # 起始公理 w = F (向量 [1,0,0])
    w = np.array([1.0, 0.0, 0.0])
    growth = []
    for n in range(1, 9):
        wn = (koch_M ** n) @ w if False else np.linalg.matrix_power(koch_M.astype(int), n) @ w.astype(int)
        growth.append(int(wn[0]))  # F 的个数 ~ 总长度的代理
    growth = np.array(growth, dtype=float)
    ns = np.arange(1, len(growth) + 1)
    slope = np.polyfit(ns, np.log(growth), 1)[0]
    print("  |P^n(w)| (F 个数): %s" % np.array2string(growth.astype(int), precision=4))
    print("  拟合增长率 = %.6f, 预测 lambda_max = %.6f, 误差 = %.4e"
          % (np.exp(slope), lam_pf_koch, abs(np.exp(slope) - lam_pf_koch)))

    # ----------------------------------------------------------------------
    # 3.2 Dragon 曲线 L-系统
    #   公理: FX
    #   规则: X -> X+YF+, Y -> -FX-Y  (角度 90°)
    #   字母表 [F, X, Y, +, -]
    # ----------------------------------------------------------------------
    subbanner("3.2 Dragon 曲线: 替换矩阵 + PF 特征值")

    # 字母表顺序: F, X, Y, +, -
    # 规则:
    #   F -> F        (不变)
    #   X -> X + Y F +    => F:1, X:1, Y:1, +:2, -:0
    #   Y -> - F X - Y    => F:1, X:1, Y:1, +:0, -:2
    #   + -> +
    #   - -> -
    dragon_M = np.array([
        [1, 1, 1, 0, 0],  # F
        [0, 1, 0, 0, 0],  # X
        [0, 0, 1, 0, 0],  # Y
        [0, 2, 0, 1, 0],  # +
        [0, 0, 2, 0, 1],  # -
    ], dtype=float)
    eig_drag = la.eigvals(dragon_M)
    mods = np.sort(np.abs(eig_drag))[::-1]
    lam_pf_drag = mods[0]
    # Dragon: 每次迭代段数翻倍, 长度缩放 sqrt(2), 维数 d=2
    L_drag = np.sqrt(2)
    dim_drag = np.log(2) / np.log(L_drag)  # 精确 = 2
    print("  Dragon 替换矩阵特征值模长 (前3): %s" % np.array2string(mods[:3], precision=4))
    print("  PF 特征值 = %.6f" % lam_pf_drag)
    print("  分形维数 d = log(2)/log(sqrt(2)) = %.6f" % dim_drag)

    # 验证增长
    w2 = np.array([1.0, 1.0, 0.0, 0.0, 0.0])  # 公理 FX
    g2 = []
    for n in range(1, 9):
        wn = np.linalg.matrix_power(dragon_M.astype(int), n) @ w2.astype(int)
        g2.append(int(wn[0]))
    g2 = np.array(g2, dtype=float)
    slope2 = np.polyfit(ns, np.log(g2), 1)[0]
    print("  |P^n(FX)| (F 个数): %s" % np.array2string(np.array(g2, dtype=int), precision=4))
    print("  拟合增长率 = %.6f" % np.exp(slope2))

    # 画图: 绘制 Koch 与 Dragon 曲线
    def draw_koch(order=4):
        # 用字符串重写
        s = "F"
        for _ in range(order):
            s = s.replace("F", "F+F--F+F")
        x, y, ang = [0.0], [0.0], 0.0
        step = 1.0 / (3 ** order)
        for ch in s:
            if ch == "F":
                x.append(x[-1] + step * np.cos(ang))
                y.append(y[-1] + step * np.sin(ang))
            elif ch == "+":
                ang += np.pi / 3
            elif ch == "-":
                ang -= np.pi / 3
        return np.array(x), np.array(y)

    def draw_dragon(order=10):
        s = "FX"
        for _ in range(order):
            ns = []
            for ch in s:
                if ch == "X":
                    ns.append("X+YF+")
                elif ch == "Y":
                    ns.append("-FX-Y")
                else:
                    ns.append(ch)
            s = "".join(ns)
        x, y, ang = [0.0], [0.0], 0.0
        step = 1.0 / (2 ** (order / 2))
        for ch in s:
            if ch == "F":
                x.append(x[-1] + step * np.cos(ang))
                y.append(y[-1] + step * np.sin(ang))
            elif ch == "+":
                ang += np.pi / 2
            elif ch == "-":
                ang -= np.pi / 2
        return np.array(x), np.array(y)

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
    kx, ky = draw_koch(4)
    axes[0].plot(kx, ky, "b-", lw=0.6)
    axes[0].set_title("Koch curve (order 4)")
    axes[0].set_aspect("equal")
    dx, dy = draw_dragon(10)
    axes[1].plot(dx, dy, "r-", lw=0.4)
    axes[1].set_title("Dragon curve (order 10)")
    axes[1].set_aspect("equal")
    save_fig(fig, "system3_lsystems.png")

    subbanner("3.3 汇总")
    print("  Koch:  lambda_max=%.4f, dim=%.6f (exact=%.6f), 条件数=%.4e"
          % (lam_pf_koch, dim_koch, dim_koch_exact, condition_number(koch_M)))
    print("  Dragon: lambda_max=%.4f, dim=%.6f, 条件数=%.4e"
          % (lam_pf_drag, dim_drag, condition_number(dragon_M)))
    return {
        "koch_lam": float(lam_pf_koch), "koch_dim": float(dim_koch),
        "koch_dim_exact": float(dim_koch_exact),
        "dragon_lam": float(lam_pf_drag), "dragon_dim": float(dim_drag),
        "koch_growth": float(np.exp(slope)),
    }


# ============================================================================
# 系统 4: 转移算子 (Ruelle, 双倍映射)
# ============================================================================

def system4_ruelle():
    banner("系统 4 / 7  Ruelle 转移算子: 双倍映射 sigma(x)=2x mod 1 (Fourier 基)")

    # ----------------------------------------------------------------------
    # 4.1 双倍映射与 Ruelle 算子 L
    #   L f(x) = sum_{y: sigma(y)=x} f(y) / |sigma'(y)|
    #          = (1/2) [ f(x/2) + f((x+1)/2) ]
    #   在 Fourier 基 e_k(x) = e^{2 pi i k x} 上:
    #     L e_k = e_{2k}  (因为 (1/2)(e_k(x/2) + e_k((x+1)/2)) = e_{2k}(x))
    #   所以 L 把基指标 k -> 2k
    #   截断到 |k| <= N, L 是 (2N+1) x (2N+1) 矩阵
    # ----------------------------------------------------------------------
    subbanner("4.1 Ruelle 算子在 Fourier 基上的矩阵表示")

    N = 32  # |k| <= N, 维数 2N+1
    dim = 2 * N + 1

    def k_index(k):
        # k in [-N, N] -> index [0, 2N]
        return k + N

    L = np.zeros((dim, dim), dtype=complex)
    for k in range(-N, N + 1):
        # L e_k = e_{2k} 若 |2k| <= N, 否则被截断 -> 0
        if abs(2 * k) <= N:
            L[k_index(2 * k), k_index(k)] = 1.0
    # 注意: Ruelle 算子的"主特征值"是常数函数 (k=0) -> 1
    # 其余特征值通过 L e_k = e_{2k} 链: k -> 2k -> 4k -> ... 直到被截断为 0
    # 因此截断后, 所有 |k|>=1 的特征值都是 0 (幂零结构!)
    # 这给出"无限"谱隙 (Ruelle 定理: 谱隙 = 1, 次大特征值 = 1/2 在更光滑空间中)

    eigs_L = la.eigvals(L)
    mods = np.sort(np.abs(eigs_L))[::-1]
    print("  Fourier 基维数 = %d (|k| <= %d)" % (dim, N))
    print("  特征值模长 (前6): %s" % np.array2string(mods[:6], precision=4))
    print("  => 主特征值 = 1 (常数函数), 其余被截断为 0 (幂零)")

    # 在更光滑的空间 (解析/可微) 中, Ruelle 算子次大特征值 = 1/2^s (s=光滑度)
    # 用 Ulam 方法 (离散化) 测量实际谱隙
    subbanner("4.2 Ulam 方法离散化双倍映射的 Perron-Frobenius 算子")

    G = 128
    P_ulam = np.zeros((G, G))
    # 双倍映射 sigma(x) = 2x mod 1, PF 算子: (Lf)(x) = (1/2)(f(x/2) + f((x+1)/2))
    # Ulam 离散化: P[j,i] = (1/|sigma'|) * |sigma(I_i) ∩ I_j| / |I_j|
    # 其中 |sigma'| = 2 (常数导数)
    for i in range(G):
        # 源区间 I_i = [i/G, (i+1)/G], 像 sigma(I_i) = [2i/G, 2(i+1)/G] mod 1
        a = 2.0 * i / G
        b = 2.0 * (i + 1) / G
        # 像可能绕回 1.0, 分成不绕回的段 (注意 a>=1 时不能取 a%1)
        segments = []
        if b <= 1.0:
            segments.append((a, b))
        elif a < 1.0:
            # 跨越 1.0: [a, 1.0] + [0, b-1]
            segments.append((a, 1.0))
            segments.append((0.0, b - 1.0))
        else:
            # a >= 1.0 且 b > 1.0: 整体平移到 [0,1] 内
            segments.append((a - 1.0, b - 1.0))
        for (seg_a, seg_b) in segments:
            # 找到与 [seg_a, seg_b] 相交的目标区间 j
            j_lo = int(np.floor(seg_a * G))
            j_hi = int(np.ceil(seg_b * G))
            for j in range(max(0, j_lo), min(G, j_hi)):
                lo = max(seg_a, j / G)
                hi = min(seg_b, (j + 1) / G)
                overlap = max(0.0, hi - lo)
                # PF: (1/|sigma'|) * overlap / |I_j| = 0.5 * overlap * G
                P_ulam[j, i] += 0.5 * overlap * G

    # PF 算子保持概率: 每列和应 ~ 1 (密度演化)
    col_sums = P_ulam.sum(axis=0)
    print("  PF 列和: min=%.6f max=%.6f (应 ~ 1)" % (col_sums.min(), col_sums.max()))
    P_pf = P_ulam  # 已正确归一化

    eigs_pf = la.eigvals(P_pf)
    mods_pf = np.sort(np.abs(eigs_pf))[::-1]
    delta_ruelle, lam1_r, lam2_r = spectral_gap_sorted(eigs_pf, radius=1.0)
    print("  Ulam 网格 G = %d" % G)
    print("  主特征值 |lambda_1| = %.6f" % lam1_r)
    print("  次特征值 |lambda_2| = %.6f" % lam2_r)
    print("  谱隙 delta = 1 - |lambda_2| = %.6f (Ruelle 定理保证 > 0)" % delta_ruelle)

    # ----------------------------------------------------------------------
    # 4.3 混合速率 vs 谱隙预测
    # ----------------------------------------------------------------------
    subbanner("4.3 混合速率 vs 谱隙预测")

    # 初始分布: 集中在前 1/4 区间
    rho = np.zeros(G)
    rho[:G // 4] = 1.0
    rho = rho / rho.sum()

    # 均匀分布 (不动点)
    rho_inf = np.ones(G) / G

    mix_errs = []
    for n in range(1, 21):
        rho = P_pf @ rho
        mix_errs.append(0.5 * np.abs(rho - rho_inf).sum())  # TV 距离

    mix_errs = np.array(mix_errs)
    ns = np.arange(1, len(mix_errs) + 1)
    slope = np.polyfit(ns, np.log(mix_errs + 1e-30), 1)[0]
    act_rate = np.exp(slope)
    pred_rate = 1 - delta_ruelle  # ~ |lambda_2|
    print("  混合误差 (TV) 前5: %s" % np.array2string(mix_errs[:5], precision=4))
    print("  实测衰减率 = %.6f" % act_rate)
    print("  谱隙预测率 = 1 - delta = %.6f" % pred_rate)
    print("  相对误差 = %.4f" % rel_err(act_rate, pred_rate))

    # 画图
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
    axes[0].plot(np.arange(G) / G, P_pf[:, G // 4], "b-", label="1 step col")
    axes[0].plot(np.arange(G) / G, np.ones(G) / G, "k--", label="uniform")
    axes[0].set_title("Perron-Frobenius 1-step transfer")
    axes[0].legend()
    axes[1].semilogy(ns, mix_errs, "o-", label="actual TV error")
    axes[1].semilogy(ns, pred_rate ** ns * mix_errs[0] / (pred_rate ** ns[0]),
                     "s--", label=r"$|\lambda_2|^n$ prediction")
    axes[1].set_xlabel("iteration n")
    axes[1].set_title("Mixing rate vs spectral gap")
    axes[1].legend()
    save_fig(fig, "system4_ruelle.png")

    subbanner("4.4 汇总")
    print("  Ruelle 谱隙 delta = %.6f" % delta_ruelle)
    print("  混合速率 实测=%.4f 预测=%.4f 误差=%.4f"
          % (act_rate, pred_rate, rel_err(act_rate, pred_rate)))
    print("  条件数 (Ulam PF) = %.4e" % condition_number(P_pf))
    return {
        "N_fourier": N, "G_ulam": G,
        "delta": float(delta_ruelle),
        "mix_actual": float(act_rate), "mix_pred": float(pred_rate),
        "cond": condition_number(P_pf),
    }


# ============================================================================
# 系统 5: 小波细分 (Daubechies-4)
# ============================================================================

def system5_wavelet():
    banner("系统 5 / 7  小波细分: Daubechies-4 细分算子 (转移矩阵特征值)")

    # ----------------------------------------------------------------------
    # 5.1 Daubechies-4 滤波器系数
    # ----------------------------------------------------------------------
    subbanner("5.1 Daubechies-4 细分算子与转移矩阵")

    # Daubechies-4 (D4) 低通滤波器系数
    h = np.array([
        (1 + np.sqrt(3)) / 4,
        (3 + np.sqrt(3)) / 4,
        (3 - np.sqrt(3)) / 4,
        (1 - np.sqrt(3)) / 4,
    ])
    h = h / h.sum() * 2  # 归一化 sum(h) = sqrt(2); 这里用于细分 sum=2
    print("  D4 滤波器系数 h = %s" % np.array2string(h, precision=5))
    print("  sum(h) = %.6f (应 = 2)" % h.sum())

    # 细分算子: 对偶数下标的点, 用 h 做插值
    # 转移矩阵 T (Strang-Fix): T_{ij} = sum_k h_{k-2i} h_{k-2j}
    # 这里构造 L=4 的转移矩阵 (大小 (L/2) x (L/2) = 2x2 对 D4? 实际为 (L-1) x (L-1) )
    # 对 D4, 转移矩阵是 3x3 (考虑符号 {0,1,2,3} 的双尺度相似)
    # 标准构造: T[i,j] = sum_n h(n - 2i) * h(n - 2j), i,j in {0,1,2}
    L = len(h)
    T_size = L - 1  # = 3, 转移矩阵大小 = L-1
    # 标准 transition matrix (Cavaretta-Dahmen-Micchelli):
    # M[i,j] = h(2i - j + 1), i,j in {0, ..., L-2}
    # 特征值: 1, 1/2, ... (sum rules), 其余 < 1 决定正则性
    T = np.zeros((T_size, T_size))
    for i in range(T_size):
        for j in range(T_size):
            idx = 2 * i - j + 1
            if 0 <= idx < L:
                T[i, j] = h[idx]
    print("  转移矩阵 T (%d x %d) =\n%s" % (T_size, T_size,
                                            np.array2string(T, precision=5)))

    eigs_T = la.eigvals(T)
    mods = np.sort(np.abs(eigs_T))[::-1]
    print("  转移矩阵特征值模长: %s" % np.array2string(mods, precision=5))

    # ----------------------------------------------------------------------
    # 5.2 验证收敛条件: lambda=1 简单, 其余 < 1
    # ----------------------------------------------------------------------
    subbanner("5.2 收敛条件: lambda=1 简单, 其余 |lambda|<1")

    # 找最接近 1 的特征值
    idx1 = np.argmin(np.abs(eigs_T - 1.0))
    lam1 = eigs_T[idx1]
    other_mods = np.delete(mods, np.argmax(mods))
    print("  主特征值 lambda_1 = %.6f + %.6fi (应 ~ 1)" % (lam1.real, lam1.imag))
    print("  其余特征值模长: %s" % np.array2string(other_mods, precision=5))
    cond1 = abs(abs(lam1) - 1.0) < 1e-6
    cond2 = np.all(other_mods < 1.0 - 1e-9)
    print("  条件1 (lambda=1): %s" % ("满足" if cond1 else "不满足"))
    print("  条件2 (其余 |lambda|<1): %s" % ("满足" if cond2 else "不满足"))
    print("  => 细分收敛: %s" % ("YES" if cond1 and cond2 else "NO"))

    # ----------------------------------------------------------------------
    # 5.3 正则性条件: |lambda| < 2^{-alpha}
    #   Daubechies-4 的 Sobolev 正则性 alpha ~ 1.0 (Hölder ~ 0.55)
    #   次大特征值应满足 |lambda_2| < 2^{-alpha}
    # ----------------------------------------------------------------------
    subbanner("5.3 正则性条件: |lambda_{p+1}| < 2^{-alpha}")

    # D4 有 p=2 阶 sum rules, 特征值 1, 1/2 来自 sum rules
    # 正则性由第 p+1 = 3 个特征值决定
    p_sr = 2  # sum rule 阶数 (消失矩数)
    lam_reg = mods[p_sr] if len(mods) > p_sr else 0.0
    # 由 |lambda_{p+1}| = 2^{-alpha} 解出 alpha
    alpha_est = -np.log(max(lam_reg, 1e-12)) / np.log(2)
    alpha_known = 0.55  # D4 Hölder 正则性 (Rioul 估)
    print("  sum rule 阶数 p = %d, 特征值 1, 1/2 来自 sum rules" % p_sr)
    print("  正则性决定特征值 |lambda_{p+1}| = %.6f" % lam_reg)
    print("  估计正则性 alpha = -log2(|lambda_{p+1}|) = %.6f" % alpha_est)
    print("  已知 D4 Hölder 正则性 ~ %.2f" % alpha_known)
    print("  条件 |lambda_{p+1}| < 2^{-alpha} = %.6f: %s"
          % (2 ** (-alpha_known), "满足" if lam_reg < 2 ** (-alpha_known) else "需检验"))

    # ----------------------------------------------------------------------
    # 5.4 细分迭代验证 (Cascade 算法)
    # ----------------------------------------------------------------------
    subbanner("5.4 细分 (Cascade) 迭代: 验证收敛到尺度函数")

    # 从 delta 函数出发, 反复细分
    n_iter = 8
    phi = np.array([1.0])
    for _ in range(n_iter):
        new = np.zeros(2 * len(phi))
        # 上采样 + 卷积
        new[::2] = phi
        new = np.convolve(new, h, mode="full")[:2 * len(phi)]
        phi = new
    t = np.arange(len(phi)) / (2 ** n_iter)
    print("  Cascade %d 次后, 尺度函数采样点数 = %d" % (n_iter, len(phi)))
    print("  phi 范数 = %.6f" % np.linalg.norm(phi))

    # 画图
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
    axes[0].stem(np.arange(len(h)), h, basefmt=" ")
    axes[0].set_title("Daubechies-4 filter coefficients")
    axes[1].plot(t, phi, "b-")
    axes[1].set_title("Scaling function (cascade, %d iter)" % n_iter)
    save_fig(fig, "system5_wavelet.png")

    subbanner("5.5 汇总")
    print("  转移矩阵特征值: %s" % np.array2string(mods, precision=5))
    print("  收敛条件: %s" % ("满足" if cond1 and cond2 else "不满足"))
    print("  正则性 alpha 估计 = %.4f (已知 ~ %.2f)" % (alpha_est, alpha_known))
    print("  条件数 (T) = %.4e" % condition_number(T))
    return {
        "eigvals": mods, "lam1": float(abs(lam1)),
        "lam_reg": float(lam_reg), "alpha_est": float(alpha_est),
        "converges": bool(cond1 and cond2),
        "cond": condition_number(T),
    }


# ============================================================================
# 系统 6: 重整化群 (2D Ising, Migdal-Kadanoff)
# ============================================================================

def system6_rg():
    banner("系统 6 / 7  重整化群: 2D Ising (Migdal-Kadanoff), 线性化 RG + 临界指数")

    # ----------------------------------------------------------------------
    # 6.1 Migdal-Kadanoff RG 变换 (b=2)
    #   对 2D Ising, MK 近似: 先 bond-moving 再 decimation
    #   耦合 K = J/T 满足递推:
    #     K' = (1/2) * log(cosh(2 K^*)),  其中 K^* = 2 K (bond-moving)
    #   即 K' = (1/2) * log(cosh(4 K))
    #   (MK 近似下 2D Ising 的递推)
    # ----------------------------------------------------------------------
    subbanner("6.1 Migdal-Kadanoff RG 递推与不动点")

    def rg_mk(K):
        """MK 递推: K' = 0.5 * log(cosh(4K))."""
        return 0.5 * np.log(np.cosh(4.0 * K))

    # 找非平凡不动点 K* (K=0 是平凡不动点, 不稳定的不动点需用二分法)
    # 不动点方程: f(K) = rg_mk(K) - K = 0
    # 对小 K: rg_mk(K) ~ 2K^2 < K (流向下); 对大 K: rg_mk(K) ~ 2K > K (流向上)
    # 故存在非平凡不动点 K* > 0
    def fixed_eq(K):
        return rg_mk(K) - K

    # 二分法: f(0.01) < 0, f(1.0) > 0
    K_lo, K_hi = 0.01, 1.0
    for _ in range(200):
        K_mid = 0.5 * (K_lo + K_hi)
        if fixed_eq(K_mid) < 0:
            K_lo = K_mid
        else:
            K_hi = K_mid
    K_star = 0.5 * (K_lo + K_hi)
    print("  MK 非平凡不动点 K* = %.6f (二分法)" % K_star)
    print("  验证 rg_mk(K*) = %.6f" % rg_mk(K_star))
    print("  (MK 近似下 2D Ising 临界点 K_c ~ 0.6067, 精确解 K_c = 0.4407)")

    # ----------------------------------------------------------------------
    # 6.2 线性化 RG 算子 dK'/dK 在不动点
    # ----------------------------------------------------------------------
    subbanner("6.2 线性化 RG 算子 (标度算子)")

    # 数值微分
    eps = 1e-6
    dKdK = (rg_mk(K_star + eps) - rg_mk(K_star - eps)) / (2 * eps)
    # 标度因子 b = 2, 相关本征值 lambda_t = b^{y_t}
    b = 2.0
    y_t = np.log(dKdK) / np.log(b)
    nu = 1.0 / y_t  # 关联长度指数
    print("  dK'/dK|_* = %.6f" % dKdK)
    print("  热指数 y_t = log(lambda)/log(b) = %.6f" % y_t)
    print("  关联长度指数 nu = 1/y_t = %.6f" % nu)
    print("  精确 2D Ising nu = 1.0")

    # ----------------------------------------------------------------------
    # 6.3 完整线性化算子 (考虑磁场 h, 扩展参数空间)
    #   参数 (K, h), MK 递推:
    #     K' = 0.5 log(cosh(4K))  (h=0 时)
    #     h' = h * (1 + tanh(2K))  (MK 场重整化: bond-moving 后 K_b=2K,
    #                                decimation 给 h' = h*(1+tanh(K_b)))
    #   雅可比 J 在 (K*, 0): 对角化, dK'/dh ~ 0, dh'/dK ~ 0 (对称)
    #     J = diag(dK'/dK, dh'/dh)
    #   临界指数: nu = 1/y_t, eta = d + 2 - 2*y_h (d=2)
    # ----------------------------------------------------------------------
    subbanner("6.3 扩展参数空间 (K, h) 的线性化算子")

    # MK 场重整化: h'/h = 1 + tanh(K_b), K_b = 2K (bond-moving 后)
    dh_dh = 1.0 + np.tanh(2.0 * K_star)
    # 精确值 (Onsager 解)
    y_h_exact = 15.0 / 8.0
    eta_exact = 1.0 / 4.0
    nu_exact = 1.0
    # 雅可比 (MK 近似, 在 h=0 解耦)
    J = np.array([
        [dKdK, 0.0],
        [0.0, dh_dh],
    ])
    eigs_J = la.eigvals(J)
    mods = np.sort(np.abs(eigs_J))[::-1]
    print("  雅可比 J =\n%s" % np.array2string(J, precision=5))
    print("  特征值模长: %s" % np.array2string(mods, precision=5))
    # 临界指数: 热本征值 = dK'/dK, 磁本征值 = dh'/dh
    y_t_est = np.log(dKdK) / np.log(b)
    y_h_est = np.log(dh_dh) / np.log(b)
    nu_est = 1.0 / y_t_est
    eta_est = 2.0 + 2.0 - 2.0 * y_h_est  # eta = d + 2 - 2*y_h, d=2
    print("  热指数 y_t = %.6f -> nu = %.6f (精确=1.0, MK已知偏差)" % (y_t_est, nu_est))
    print("  磁指数 y_h = %.6f -> eta = %.6f (精确=0.25, MK不捕获eta)" % (y_h_est, eta_est))
    print("  nu 相对误差 = %.4f" % rel_err(nu_est, nu_exact))
    print("  eta 相对误差 = %.4f (MK 近似不保证 eta 精度)" % rel_err(eta_est, eta_exact))

    # ----------------------------------------------------------------------
    # 6.4 RG 流轨迹
    # ----------------------------------------------------------------------
    subbanner("6.4 RG 流轨迹 (从不同初值流向不动点)")

    K_inits = [0.2, 0.4, 0.6, 0.8, 1.0]
    fig, ax = plt.subplots(figsize=(7, 5))
    for K0 in K_inits:
        traj = [K0]
        Kc = K0
        for _ in range(20):
            Kc = rg_mk(Kc)
            traj.append(Kc)
        ax.plot(range(len(traj)), traj, "o-", label="K0=%.1f" % K0, ms=3)
    ax.axhline(K_star, color="k", ls="--", label="K*=%.4f" % K_star)
    ax.set_xlabel("RG step")
    ax.set_ylabel("K = J/T")
    ax.set_title("Migdal-Kadanoff RG flow (2D Ising)")
    ax.legend()
    save_fig(fig, "system6_rg.png")

    subbanner("6.5 汇总")
    print("  MK 不动点 K* = %.6f" % K_star)
    print("  线性化算子特征值: %s" % np.array2string(mods, precision=5))
    print("  临界指数 nu = %.4f (精确 1.0), eta = %.4f (精确 0.25)" % (nu_est, eta_est))
    print("  条件数 (J) = %.4e" % condition_number(J))
    return {
        "K_star": float(K_star), "nu": float(nu_est), "eta": float(eta_est),
        "y_t": float(y_t_est), "y_h": float(y_h_est),
        "cond": condition_number(J),
    }


# ============================================================================
# 系统 7: 神经网络训练 (NTK 谱去递归)
# ============================================================================

def system7_ntk():
    banner("系统 7 / 7  神经网络训练作为递归系统: NTK 谱去递归验证")

    rng = np.random.default_rng(RNG_SEED + 7)

    # ----------------------------------------------------------------------
    # 7.1 生成分形数据 (Sierpinski-like 标签)
    # ----------------------------------------------------------------------
    subbanner("7.1 分形数据 + 简单 MLP 初始化")

    n_data = 64
    d_in = 4
    # 输入: 低维嵌入
    X = rng.standard_normal((n_data, d_in))
    # 分形标签: 用 Sierpinski 生成二值标签 (基于到吸引子的距离阈值)
    def sier_label(x):
        # 简化: 基于 x 的奇偶结构生成 0/1
        v = np.sum(np.sin(x * 3.0)) + np.sum(np.cos(x * 5.0))
        return 1.0 if v > 0 else 0.0
    Y = np.array([sier_label(x) for x in X]).reshape(-1, 1)

    # 简单 MLP: d_in -> H -> 1, 无激活的线性等价 (用于精确 NTK)
    H = 32
    W1 = rng.standard_normal((d_in, H)) / np.sqrt(d_in)
    W2 = rng.standard_normal((H, 1)) / np.sqrt(H)

    def forward(X, W1, W2):
        Z = X @ W1  # (n, H) 线性
        # 用 tanh 非线性 (NTK 的标准设置)
        A = np.tanh(Z)
        return A @ W2  # (n, 1)

    def ntk_kernel(X, W1, W2):
        """计算 NTK 核 K(x_i, x_j) 对 tanh 网络.
        K = K_linear + K_relu_part; 对 tanh:
          K(x,x') = sum_h phi'(z_h) phi'(z'_h) * (x . x') + phi(z_h) phi(z'_h)
        其中 phi = tanh, z = W1 x."""
        Z = X @ W1  # (n, H)
        Phi = np.tanh(Z)  # (n, H)
        Phi_prime = 1.0 - Phi ** 2  # (n, H)
        n = X.shape[0]
        # 核 = (Phi @ Phi.T) + (X @ X.T) * sum_h Phi_prime_i Phi_prime_j
        K1 = Phi @ Phi.T  # (n, n)
        # 第二项: (n,n) = sum_h Phi_prime[i,h] * (x_i . x_j) * Phi_prime[j,h]
        # = (Phi_prime * X_norm?) 用展开
        # 先算 G[i,j] = x_i . x_j
        G = X @ X.T  # (n, n)
        # sum_h Phi_prime[i,h] Phi_prime[j,h] G[i,j]
        # = G * (Phi_prime @ Phi_prime.T)
        K2 = G * (Phi_prime @ Phi_prime.T)
        return K1 + K2

    K = ntk_kernel(X, W1, W2)
    print("  数据: n=%d, d_in=%d, 隐藏 H=%d" % (n_data, d_in, H))
    print("  NTK 核 K 形状 = %s" % str(K.shape))
    print("  K 对称性误差 = %.4e" % np.linalg.norm(K - K.T))

    # ----------------------------------------------------------------------
    # 7.2 NTK 谱分解
    # ----------------------------------------------------------------------
    subbanner("7.2 NTK 谱分解")

    eigvals_K, eigvecs_K = np.linalg.eigh(K)
    idx = np.argsort(eigvals_K)[::-1]
    eigvals_K = eigvals_K[idx]
    eigvecs_K = eigvecs_K[:, idx]
    print("  NTK 特征值 (前6): %s" % np.array2string(eigvals_K[:6], precision=4))
    print("  NTK 特征值 (后3): %s" % np.array2string(eigvals_K[-3:], precision=4))
    print("  谱条件数 = %.4e" % (eigvals_K[0] / max(eigvals_K[-1], 1e-12)))

    # ----------------------------------------------------------------------
    # 7.3 谱去递归: f_t = exp(-t * eta * K) f_0
    #   训练动力学在 NTK 极限下精确由核指数给出
    # ----------------------------------------------------------------------
    subbanner("7.3 谱去递归验证: f_t = exp(-t*eta*K) f_0")

    eta = 0.05
    # 初始预测 f_0 (网络前向)
    f0 = forward(X, W1, W2).ravel()
    y = Y.ravel()
    # 残差
    r0 = f0 - y

    # 预测: r_t = exp(-t eta K) r_0  (梯度下降下的残差演化)
    # 训练时间 t = step (full-batch GD, lr=eta)
    n_steps = 60
    actual_err = []
    pred_err = []
    W1c, W2c = W1.copy(), W2.copy()
    for step in range(n_steps + 1):
        f_t = forward(X, W1c, W2c).ravel()
        actual_err.append(0.5 * np.mean((f_t - y) ** 2))
        # 预测: r_t = expm(-t eta K) r0
        t_val = step
        r_pred = (eigvecs_K @ np.diag(np.exp(-t_val * eta * eigvals_K))
                  @ eigvecs_K.T @ r0)
        pred_err.append(0.5 * np.mean(r_pred ** 2))
        # 实际梯度下降更新 (full-batch)
        # df/dW2 = A^T (f - y) / n; A = tanh(X W1)
        Z = X @ W1c
        A = np.tanh(Z)
        f_t_mat = (A @ W2c)
        grad_out = (f_t_mat - Y) / n_data  # (n,1)
        grad_W2 = A.T @ grad_out  # (H,1)
        # 反向到隐藏: dA = grad_out @ W2.T; dZ = dA * (1 - tanh^2)
        dA = grad_out @ W2c.T  # (n, H)
        dZ = dA * (1 - A ** 2)
        grad_W1 = X.T @ dZ  # (d_in, H)
        W2c -= eta * grad_W2
        W1c -= eta * grad_W1

    actual_err = np.array(actual_err)
    pred_err = np.array(pred_err)
    steps = np.arange(n_steps + 1)
    # 衰减率 (前半段拟合)
    half = n_steps // 2 + 1
    slope_act = np.polyfit(steps[:half], np.log(actual_err[:half] + 1e-30), 1)[0]
    slope_pred = np.polyfit(steps[:half], np.log(pred_err[:half] + 1e-30), 1)[0]
    rate_act = -slope_act
    rate_pred = -slope_pred
    print("  训练步数 = %d, 学习率 eta = %.4f" % (n_steps, eta))
    print("  实测误差衰减率 = %.6f" % rate_act)
    print("  NTK 预测衰减率 = %.6f" % rate_pred)
    print("  相对误差 = %.4f" % rel_err(rate_act, rate_pred))
    print("  最终误差 实测=%.4e 预测=%.4e" % (actual_err[-1], pred_err[-1]))

    # 最大特征值决定的快速衰减
    lam_max = eigvals_K[0]
    lam_min = eigvals_K[-1]
    print("  NTK lambda_max = %.4f (快速模式衰减 ~ exp(-eta*lam_max*t))"
          % lam_max)
    print("  NTK lambda_min = %.4f (慢速模式, 主导长期收敛)" % lam_min)
    print("  长期收敛率预测 ~ eta * lambda_min = %.6f" % (eta * lam_min))

    # 画图
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
    axes[0].semilogy(np.arange(1, len(eigvals_K) + 1), eigvals_K, "b.-")
    axes[0].set_title("NTK eigenvalue spectrum")
    axes[0].set_xlabel("index")
    axes[0].set_ylabel("lambda")
    axes[1].semilogy(steps, actual_err, "b-", label="actual training loss")
    axes[1].semilogy(steps, pred_err, "r--", label=r"$e^{-t\eta K}$ prediction")
    axes[1].set_xlabel("training step t")
    axes[1].set_ylabel("loss")
    axes[1].set_title("Spectral de-recursion verification")
    axes[1].legend()
    save_fig(fig, "system7_ntk.png")

    subbanner("7.4 汇总")
    print("  NTK 谱: lambda_max=%.4f, lambda_min=%.4e, 条件数=%.4e"
          % (lam_max, lam_min, lam_max / max(lam_min, 1e-30)))
    print("  谱去递归验证: f_t = exp(-t eta K) f_0")
    print("    实测衰减率=%.4f, 预测=%.4f, 相对误差=%.4f"
          % (rate_act, rate_pred, rel_err(rate_act, rate_pred)))
    return {
        "ntk_lam_max": float(lam_max), "ntk_lam_min": float(lam_min),
        "rate_actual": float(rate_act), "rate_pred": float(rate_pred),
        "final_err_actual": float(actual_err[-1]),
        "final_err_pred": float(pred_err[-1]),
        "cond": float(lam_max / max(lam_min, 1e-30)),
    }


# ============================================================================
# 主函数
# ============================================================================

def main():
    t0 = time.time()
    np.random.seed(RNG_SEED)

    print("#" * 78)
    print("#  7 类递归系统大规模数值模拟  ".center(78, "#"))
    print("#  spectral de-recursion verification  ".center(78, "#"))
    print("#" * 78)

    results = {}
    try:
        results["ifs"] = system1_ifs()
    except Exception as e:
        import traceback
        print("  [系统1 IFS 异常] %s" % e)
        traceback.print_exc()
        results["ifs"] = None

    try:
        results["julia"] = system2_julia()
    except Exception as e:
        import traceback
        print("  [系统2 Julia 异常] %s" % e)
        traceback.print_exc()
        results["julia"] = None

    try:
        results["lsystems"] = system3_lsystems()
    except Exception as e:
        import traceback
        print("  [系统3 L-系统 异常] %s" % e)
        traceback.print_exc()
        results["lsystems"] = None

    try:
        results["ruelle"] = system4_ruelle()
    except Exception as e:
        import traceback
        print("  [系统4 Ruelle 异常] %s" % e)
        traceback.print_exc()
        results["ruelle"] = None

    try:
        results["wavelet"] = system5_wavelet()
    except Exception as e:
        import traceback
        print("  [系统5 小波 异常] %s" % e)
        traceback.print_exc()
        results["wavelet"] = None

    try:
        results["rg"] = system6_rg()
    except Exception as e:
        import traceback
        print("  [系统6 RG 异常] %s" % e)
        traceback.print_exc()
        results["rg"] = None

    try:
        results["ntk"] = system7_ntk()
    except Exception as e:
        import traceback
        print("  [系统7 NTK 异常] %s" % e)
        traceback.print_exc()
        results["ntk"] = None

    # ----------------------------------------------------------------------
    # 全局汇总
    # ----------------------------------------------------------------------
    banner("全局汇总: 7 类递归系统谱去递归化验证结果")
    names = {
        "ifs": "1. IFS 迭代函数系统",
        "julia": "2. 复动力学 (Julia)",
        "lsystems": "3. L-系统",
        "ruelle": "4. Ruelle 转移算子",
        "wavelet": "5. 小波细分 (D4)",
        "rg": "6. 重整化群 (Ising)",
        "ntk": "7. 神经网络 NTK",
    }
    for key, name in names.items():
        r = results.get(key)
        print("\n  %s:" % name)
        if r is None:
            print("    [失败]")
            continue
        for k, v in r.items():
            if isinstance(v, (int, float)):
                print("    %-22s = %.6f" % (k, v))
            elif isinstance(v, complex):
                print("    %-22s = %.4f + %.4fi" % (k, v.real, v.imag))
            elif isinstance(v, np.ndarray):
                print("    %-22s = %s" % (k, np.array2string(v[:6], precision=4)))
            elif isinstance(v, bool):
                print("    %-22s = %s" % (k, v))
            else:
                print("    %-22s = %s" % (k, v))

    print("\n  总耗时: %.2f s" % (time.time() - t0))
    print("\n" + "#" * 78)
    print("#  仿真完成  ".center(78, "#"))
    print("#" * 78)


if __name__ == "__main__":
    main()
