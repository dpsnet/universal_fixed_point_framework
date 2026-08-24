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
S0 表示静默剩余项解析推进（2026-07-31）。

对应笔记：notes/00_foundations/spectral_representation_silence.md §10.4（遗留 1/3）
验证内容：
  1. 遗留 3：S0 静默空间维数闭式 dim S_D = n² - rank(Im D) = n-1
     （Im(D) 张成 = 行和相等矩阵空间；n=2→1, n=3→2，一般 n→n-1）
  2. 遗留 1：S_D 下降率解析刻画——平凡 2 态系统左复合 M=ψ·φ（φ=[[1,1],[-1,-1]]）
     解析分布 S_D = 1-|cos θ|（θ~U(0,2π)），中位数 1-√2/2≈0.293，均值 1-2/π≈0.363
  3. 遗留 2 预备：非平凡谱对象（step=swap, A=[[0,1],[1,0]]）Hom_Sp 与 S0 静默结构
"""
import numpy as np
from itertools import product

# ── 基础设施 ─────────────────────────────────────────────────────────

def all_transfer_matrices(n: int) -> "list[np.ndarray]":
    """Im(D)：n 状态全部转移矩阵（每行恰一个 1）。"""
    mats = []
    for cols in product(range(n), repeat=n):
        M = np.zeros((n, n))
        for i, c in enumerate(cols):
            M[i, c] = 1.0
        mats.append(M)
    return mats

def span_rank(mats: "list[np.ndarray]") -> int:
    """矩阵集合张成空间秩。"""
    V = np.stack([M.ravel() for M in mats])
    return np.linalg.matrix_rank(V)

def frob(a: np.ndarray, b: np.ndarray) -> complex:
    return np.trace(a.conj().T @ b)

def sD(phi: np.ndarray, trans: "list[np.ndarray]") -> float:
    """S_D(φ) = 1 - ||P_Im(D)(φ)|| / ||φ||。"""
    norm = np.linalg.norm(phi)
    if norm == 0:
        return 1.0
    basis = []
    for T in trans:
        v = T.copy()
        for b in basis:
            v = v - frob(b, v) * b / (frob(b, b) + 1e-300)
        if np.linalg.norm(v) > 1e-12:
            basis.append(v)
    proj = np.zeros_like(phi)
    for b in basis:
        proj = proj + (frob(b, phi) / (frob(b, b) + 1e-300)) * b
    return float(1 - np.linalg.norm(proj) / norm)

# ── 检查 1：闭式 dim S_D = n - 1（遗留 3） ───────────────────────────

def check_dim_formula() -> "tuple[bool, str]":
    for n in range(2, 8):
        trans = all_transfer_matrices(n)
        rank = span_rank(trans)
        dim_silent = n * n - rank
        if rank != n * n - (n - 1):
            return False, f"n={n}: rank(Im D)={rank} ≠ n²-(n-1)={n*n-(n-1)}"
        if dim_silent != n - 1:
            return False, f"n={n}: dim S_D={dim_silent} ≠ n-1={n-1}"
    return True, "n=2..7：rank(Im D)=n²-(n-1)，dim S_D=n-1（闭式 ✓）"

def check_rowsum_structure() -> "tuple[bool, str]":
    """Im(D) 张成 = 行和相等矩阵空间（理论依据：转移矩阵每行行和=1）。"""
    n = 3
    trans = all_transfer_matrices(n)
    # 行和相等矩阵空间的基：{E_ij - E_i0} ∪ {J}
    basis = []
    for i in range(n):
        for j in range(1, n):
            B = np.zeros((n, n))
            B[i, j] = 1.0
            B[i, 0] = -1.0
            basis.append(B)
    basis.append(np.ones((n, n)))
    rank_rs = span_rank(basis)
    rank_im = span_rank(trans)
    if rank_rs != rank_im:
        return False, f"行和相等空间秩 {rank_rs} ≠ rank(Im D) {rank_im}"
    # E_ij - E_i0 的每个元素是转移矩阵差（构造性）：T(σ(i)=j)-T'(σ(i)=0)
    return True, f"n=3：Im(D) 张成 = 行和相等空间（秩 {rank_im}，含 {len(basis)} 个构造基）"

# ── 检查 2：遗留 1 解析分布（1-√U） ─────────────────────────────────

def check_analytic_distribution() -> "tuple[bool, str]":
    """平凡 2 态系统：φ=[[1,1],[-1,-1]]，ψ 标准复高斯，M=ψφ。
    解析：M=[[u,u],[v,v]]（u=ψ₀₀-ψ₀₁ 复高斯），P(M)=[[w,w],[w,w]]，w=(u+v)/2。
    S_D = 1 - |u+v|/√(2(|u|²+|v|²)) = 1-√(X/(X+Y)) = 1-√U（X,Y 独立指数，U~U(0,1)）。
    中位数 1-√(1/2)≈0.2929，均值 1/3≈0.3333，σ=√(1/18)≈0.2357。"""
    trans = all_transfer_matrices(2)
    phi = np.array([[1, 1], [-1, -1]], dtype=complex)
    rng = np.random.default_rng(5)
    N = 20000
    vals = []
    for _ in range(N):
        psi = rng.normal(size=(2, 2)) + 1j * rng.normal(size=(2, 2))
        vals.append(sD(psi @ phi, trans))
    vals = np.array(vals)
    med_n, mean_n, std_n = np.median(vals), vals.mean(), vals.std()
    med_a, mean_a, std_a = 1 - np.sqrt(0.5), 1 / 3, np.sqrt(1 / 18)
    if abs(med_n - med_a) > 2e-3 or abs(mean_n - mean_a) > 2e-3 or abs(std_n - std_a) > 2e-3:
        return False, (f"矩不匹配: 数值 med={med_n:.4f}/mean={mean_n:.4f}/σ={std_n:.4f} "
                       f"vs 解析 med={med_a:.4f}/mean={mean_a:.4f}/σ={std_a:.4f}")
    return True, (f"S_D=1-√U 解析成立：中位数 {med_n:.4f}≈1-√(1/2)={med_a:.4f}，"
                  f"均值 {mean_n:.4f}≈1/3={mean_a:.4f}，σ={std_n:.4f}≈√(1/18)={std_a:.4f}")

# ── 检查 3：1-√U 直接采样对照 ────────────────────────────────────────

def check_uniform_identity() -> "tuple[bool, str]":
    """直接采样 U~U(0,1)：1-√U 的分位数与数值 S_D 分布一致（分布恒等检验）。"""
    rng = np.random.default_rng(9)
    N = 20000
    analytic = 1 - np.sqrt(rng.uniform(0, 1, N))
    trans = all_transfer_matrices(2)
    phi = np.array([[1, 1], [-1, -1]], dtype=complex)
    numeric = []
    for _ in range(N):
        psi = rng.normal(size=(2, 2)) + 1j * rng.normal(size=(2, 2))
        numeric.append(sD(psi @ phi, trans))
    numeric = np.array(numeric)
    # 分位数对照（0.1..0.9；解析 q 分位 = 1-√(1-p)，容差含采样波动）
    for p in (0.1, 0.25, 0.5, 0.75, 0.9):
        q_a = 1 - np.sqrt(1 - p)
        if abs(np.quantile(numeric, p) - q_a) > 6e-3:
            return False, f"分位数 {p} 不匹配: 数值 {np.quantile(numeric,p):.4f} vs 解析 {q_a:.4f}"
    return True, "S_D(ψφ) 与 1-√U 分位数一致（0.1/0.25/0.5/0.75/0.9）——分布恒等"

# ── 检查 4：遗留 2——非平凡动力学演化下的 S0 静默 ─────────────────────

def check_nontrivial_evolution() -> "tuple[bool, str]":
    """S0 静默态射 φ=[[1,1],[-1,-1]] 经非平凡动力学 e^{-tA}（A=diag(1,2) 非标量）左复合。
    解析：M=e^{-tA}·φ=[[x,x],[-y,-y]]（x=e^{-t},y=e^{-2t}），投影到行和相等空间得
    N=[[(x-y)/2]*4]，故 S_D(t) = 1 - |x-y|/√(2(x²+y²))。
    t=0：S_D=1（φ 静默）；t→∞：S_D→1-1/√2≈0.293（极限）——非平凡动力学破坏静默。"""
    trans = all_transfer_matrices(2)
    phi = np.array([[1, 1], [-1, -1]], dtype=complex)
    if sD(phi, trans) < 1 - 1e-9:
        return False, "φ 应为 S0 静默（S_D≈1）"
    A = np.diag([1.0, 2.0])
    for t in (0.0, 0.5, 1.0, 2.0, 5.0):
        E = np.diag([np.exp(-1.0 * t), np.exp(-2.0 * t)])
        M = E @ phi
        sd = sD(M, trans)
        x, y = np.exp(-t), np.exp(-2 * t)
        pred = 1 - abs(x - y) / np.sqrt(2 * (x * x + y * y))
        if abs(sd - pred) > 1e-9:
            return False, f"t={t}: 数值 S_D={sd:.6f} vs 解析 {pred:.6f}"
    return True, ("e^{-tA}·φ 演化：S_D(t)=1-|e^{-t}-e^{-2t}|/√(2(e^{-2t}+e^{-4t})) 解析吻合"
                  "（t=0,0.5,1,2,5）；t=0 静默→极限 1-1/√2≈0.293——非平凡动力学破坏 S0 静默")

# ── 检查 5：swap 系统 Hom_Sp 被 Im(D) 覆盖（S0 静默={0}） ────────────

def check_swap_system_silence() -> "tuple[bool, str]":
    """swap 系统（A=[[0,1],[1,0]]）：Hom_Sp=span{I,A}，且 I=transferMatrix(id)、
    A=transferMatrix(swap) 均在 Im(D) 中 ⟹ 覆盖 Hom_Sp，Hom_Sp 中无全局 S0 静默。"""
    A = np.array([[0, 1], [1, 0]], dtype=complex)
    trans = all_transfer_matrices(2)
    hom_span = span_rank([np.eye(2), A])
    im_inter_rank = span_rank([T for T in trans if np.linalg.norm(T @ A - A @ T) < 1e-12])
    # 非零 Hom_Sp 元是否都存在非零 Im(D) 分量（非全局静默）
    for a, b in ((1.0, 0.0), (0.0, 1.0), (1.0, 1.0)):
        M = np.array([[a, b], [b, a]], dtype=complex)
        if sD(M, trans) > 1e-6:
            return False, f"swap 系统 Hom_Sp 元 {M} 非静默（S_D={sD(M,trans):.4f}）"
    if not (hom_span == 2 and im_inter_rank == 2):
        return False, f"swap 系统: Hom_Sp 秩 {hom_span}，Im(D)∩Hom_Sp 秩 {im_inter_rank}"
    return True, "swap 系统：Hom_Sp=span{I,A}⊆Im(D)，S0 静默={0}（结构依赖：静默需 Hom_Sp 未被 Im(D) 覆盖）"

# ── 主流程 ───────────────────────────────────────────────────────────

def main():
    checks = [
        ("闭式 dim=n-1",        check_dim_formula),
        ("行和相等结构",         check_rowsum_structure),
        ("解析分布矩匹配",        check_analytic_distribution),
        ("1-√U 分布恒等",        check_uniform_identity),
        ("非平凡演化（遗留 2）",   check_nontrivial_evolution),
        ("swap 系统静默={0}",     check_swap_system_silence),
    ]
    npass = 0
    for name, fn in checks:
        ok, msg = fn()
        mark = "✓" if ok else "✗"
        print(f"{mark} PASS  {name:<14s} {msg}")
        npass += int(ok)
    print(f"\n结果: {npass}/{len(checks)} 项通过")
    return 0 if npass == len(checks) else 1

if __name__ == "__main__":
    import sys
    sys.exit(main())
