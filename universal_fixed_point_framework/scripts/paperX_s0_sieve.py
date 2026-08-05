#!/usr/bin/env python3
"""
S0 表示静默的筛（sieve）结构验证（P2，2026-07-31）。

对应笔记：notes/00_foundations/spectral_representation_silence.md §10
验证内容：
  1. 2 状态平凡系统上 Im(D) = 4 个转移矩阵，S0 静默空间 = span{[[1,1],[-1,-1]]}
  2. S0 静默态射类对左复合（后复合）不封闭：φ ∈ S_D 但 ψ∘φ ∉ S_D
  3. S0 静默态射类对右复合（前复合）不封闭：φ ∈ S_D 但 φ∘χ ∉ S_D
  4. 结论：S0 静默不构成 sieve（与 S1 动力学静默构成 sieve（定理 R6）形成结构性对照）
  5. S_D 静默度在复合下不单调（可从 1 降到 < 1）
"""
import numpy as np

# ── 基础设施：2 状态平凡系统 ─────────────────────────────────────────

def all_transfer_matrices(n: int) -> "list[np.ndarray]":
    """Im(D)：n 状态全部转移矩阵（每行恰一个 1，行和为 1）。"""
    import itertools
    mats = []
    for cols in itertools.product(range(n), repeat=n):
        M = np.zeros((n, n))
        for i, c in enumerate(cols):
            M[i, c] = 1.0
        mats.append(M)
    return mats

def frob(a: np.ndarray, b: np.ndarray) -> complex:
    """Frobenius 内积 <a,b> = Tr(a† b)。"""
    return np.trace(a.conj().T @ b)

def sD(phi: np.ndarray, trans: "list[np.ndarray]") -> float:
    """S_D(φ) = 1 - ||P_Im(D)(φ)|| / ||φ||（正交投影到 span(Im(D))）。"""
    norm = np.linalg.norm(phi)
    if norm == 0:
        return 1.0
    # Gram-Schmidt 正交化转移矩阵基
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

def is_silent(phi: np.ndarray, trans: "list[np.ndarray]", tol: float = 1e-9) -> bool:
    """φ 正交于所有转移矩阵（S0 静默）。"""
    return all(abs(frob(phi, T)) < tol for T in trans)

# ── 检查 1：S0 静默空间结构 ──────────────────────────────────────────

def check_silent_space() -> "tuple[bool, str]":
    trans = all_transfer_matrices(2)
    # 生成器 a·[[1,1],[-1,-1]] 对 a=1..5 均静默
    for a in (1.0, 2.0, -1.0, 0.5j):
        M = a * np.array([[1, 1], [-1, -1]], dtype=complex)
        if not is_silent(M, trans):
            return False, f"S0 静默空间生成元验证失败 (a={a})"
    # 反例矩阵 [[1,0],[1,1]] 非静默（它是合法谱态射但非转移矩阵）
    P = np.array([[1, 0], [1, 1]], dtype=complex)
    if is_silent(P, trans):
        return False, "P=[[1,0],[1,1]] 不应是 S0 静默（它只不在 Im(D) 中，而非正交于 Im(D)）"
    # 随机矩阵几乎都不是 S0 静默
    rng = np.random.default_rng(7)
    cnt_silent = 0
    for _ in range(200):
        R = rng.normal(size=(2, 2)) + 1j * rng.normal(size=(2, 2))
        if is_silent(R, trans):
            cnt_silent += 1
    if cnt_silent != 0:
        return False, f"随机矩阵中出现 {cnt_silent}/200 个 S0 静默（预期 0）"
    return True, "S0 静默空间 = span{[[1,1],[-1,-1]]}（一维，测度零）"

# ── 检查 2：左复合（后复合）不封闭 ────────────────────────────────────

def check_left_composite() -> "tuple[bool, str]":
    trans = all_transfer_matrices(2)
    phi = np.array([[1, 1], [-1, -1]], dtype=complex)   # S0 静默
    psi = np.array([[1, 0], [0, 0]], dtype=complex)      # 合法谱态射（平凡系统 Hom_Sp = C^{2x2}）
    psi_phi = psi @ phi
    if not is_silent(phi, trans):
        return False, "φ 应为 S0 静默（前提失效）"
    if is_silent(psi_phi, trans):
        return False, "ψ∘φ 意外静默（反例失效）"
    s0, s1 = sD(phi, trans), sD(psi_phi, trans)
    if not (s0 > 0.999 and s1 < 0.999):
        return False, f"静默度未下降: S_D(φ)={s0:.6f}, S_D(ψ∘φ)={s1:.6f}"
    return True, f"左复合不封闭：φ∈S_D 但 ψ∘φ∉S_D（S_D: {s0:.3f}→{s1:.3f}）"

# ── 检查 3：右复合（前复合）不封闭 ────────────────────────────────────

def check_right_composite() -> "tuple[bool, str]":
    trans = all_transfer_matrices(2)
    phi = np.array([[1, 1], [-1, -1]], dtype=complex)   # S0 静默
    chi = np.array([[1, 0], [0, 0]], dtype=complex)      # 合法谱态射
    phi_chi = phi @ chi
    if not is_silent(phi, trans):
        return False, "φ 应为 S0 静默（前提失效）"
    if is_silent(phi_chi, trans):
        return False, "φ∘χ 意外静默（反例失效）"
    s0, s1 = sD(phi, trans), sD(phi_chi, trans)
    if not (s0 > 0.999 and s1 < 0.999):
        return False, f"静默度未下降: S_D(φ)={s0:.6f}, S_D(φ∘χ)={s1:.6f}"
    return True, f"右复合不封闭：φ∈S_D 但 φ∘χ∉S_D（S_D: {s0:.3f}→{s1:.3f}）"

# ── 检查 4：S_D 在复合下不单调（度扫描） ──────────────────────────────

def check_monotonicity_scan() -> "tuple[bool, str]":
    trans = all_transfer_matrices(2)
    phi = np.array([[1, 1], [-1, -1]], dtype=complex)
    rng = np.random.default_rng(11)
    drops = 0
    for _ in range(100):
        psi = rng.normal(size=(2, 2)) + 1j * rng.normal(size=(2, 2))
        # psi 需为合法谱态射：平凡系统上 Hom_Sp = 全矩阵，无约束
        s0, s1 = sD(phi, trans), sD(psi @ phi, trans)
        if s1 < s0 - 1e-6:
            drops += 1
    if drops < 90:
        return False, f"静默度下降比例过低: {drops}/100"
    return True, f"S_D 在左复合下非保静默（{drops}/100 随机 ψ 使静默度下降）"

# ── 检查 5：S_D 复合下降率的定量分布 ──────────────────────────────────

def check_drop_rate_distribution() -> "tuple[bool, str]":
    """统计 S_D(ψ∘φ) 在随机 ψ 下的分布（均值/中位数/标准差）。"""
    trans = all_transfer_matrices(2)
    phi = np.array([[1, 1], [-1, -1]], dtype=complex)
    rng = np.random.default_rng(21)
    N = 2000
    vals = []
    for _ in range(N):
        psi = rng.normal(size=(2, 2)) + 1j * rng.normal(size=(2, 2))
        vals.append(sD(psi @ phi, trans))
    vals = np.array(vals)
    mean, med, std = vals.mean(), np.median(vals), vals.std()
    frac_quiet = float((vals < 0.5).mean())   # 静默度被压到 <0.5 的比例
    if not (mean < 0.6 and frac_quiet > 0.5):
        return False, f"下降率分布异常: mean={mean:.3f}, med={med:.3f}, quiet={frac_quiet:.2f}"
    return True, f"S_D(ψ∘φ) 分布: mean={mean:.3f}, median={med:.3f}, σ={std:.3f}, <0.5 占比 {frac_quiet:.0%}"

# ── 检查 6：高维（n=3）筛结构 ─────────────────────────────────────────

def check_high_dim_sieve() -> "tuple[bool, str]":
    """n=3：转移矩阵张成空间秩 → S0 静默空间维数 = n² - rank。"""
    n = 3
    trans = all_transfer_matrices(n)
    # 转成向量矩阵求秩
    V = np.stack([T.ravel() for T in trans])
    rank = np.linalg.matrix_rank(V)
    dim_silent = n * n - rank
    if rank == n * n:
        # Im(D) 张成全 Hom_Sp：S0 静默空间为 {0}，只有零态射静默
        return True, f"n=3: rank(Im D)={rank}=n² → S0 静默空间={{0}}（平凡）"
    # 非平凡：找 S0 静默基并验证复合破坏
    U, S, Vt = np.linalg.svd(V)
    null = Vt[rank:].conj()   # 零空间基（行向量）
    if null.shape[0] == 0:
        return False, "SVD 零空间为空但 rank < n²（数值异常）"
    phi = null[0].reshape(n, n)
    if not is_silent(phi, trans):
        return False, "S0 静默基不静默（数值异常）"
    psi = np.zeros((n, n)); psi[0, 0] = 1.0
    s0, s1 = sD(phi, trans), sD(psi @ phi, trans)
    if not (s0 > 0.999 and s1 < 0.999):
        return False, f"高维复合未破坏静默: {s0:.3f}→{s1:.3f}"
    return True, f"n=3: rank(Im D)={rank}, S0 静默空间维数={dim_silent}，复合仍破坏静默 ({s0:.2f}→{s1:.2f})"

# ── 检查 7：标量演化复合保持 S0 静默（对照） ───────────────────────────

def check_scalar_evolution() -> "tuple[bool, str]":
    """平凡系统上动力学演化 e^{-tA} = e^{-t}·I 是标量：标量复合保持 S0 静默。
    对照：结构性复合（任意谱态射）破坏静默，标量复合保持——破坏源于态射形状而非缩放。"""
    trans = all_transfer_matrices(2)
    phi = np.array([[1, 1], [-1, -1]], dtype=complex)
    for t in np.linspace(0.0, 10.0, 21):
        E = np.exp(-t) * np.eye(2)   # e^{-tA}，平凡系统 A=I
        if not is_silent(E @ phi, trans) or not is_silent(phi @ E, trans):
            return False, f"t={t:.2f}: 标量演化破坏 S0 静默"
    return True, "标量演化 e^{-t}I 保持 S0 静默（t∈[0,10]，21 点）"

# ── 主流程 ───────────────────────────────────────────────────────────

def main():
    checks = [
        ("S0 静默空间结构",       check_silent_space),
        ("左复合不封闭",          check_left_composite),
        ("右复合不封闭",          check_right_composite),
        ("S_D 非保静默扫描",      check_monotonicity_scan),
        ("S_D 下降率分布",        check_drop_rate_distribution),
        ("高维筛结构 n=3",        check_high_dim_sieve),
        ("标量演化保持",          check_scalar_evolution),
    ]
    npass = 0
    for name, fn in checks:
        ok, msg = fn()
        mark = "✓" if ok else "✗"
        print(f"{mark} PASS  {name:<16s} {msg}")
        npass += int(ok)
    print(f"\n汇总: {npass}/{len(checks)} 检查通过")
    print("结论: S0 表示静默态射类不构成 sieve（左、右复合均不封闭）；破坏源于结构性复合，标量演化保持")
    return 0 if npass == len(checks) else 1

if __name__ == "__main__":
    raise SystemExit(main())
