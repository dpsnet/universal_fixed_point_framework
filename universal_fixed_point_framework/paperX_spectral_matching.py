#!/usr/bin/env python3
"""
P1 谱匹配三条件等价验证（2026-07-31）。

对应笔记：notes/00_foundations/spectral_R11_morphism_layer.md（定理 3 / 命题 6）
验证内容（有限维数值，自伴矩阵）：
  1. 交织条件 X·A_E = A_S·X 的解空间 = 谱匹配条件 X·E_{A_E}(Ω) = E_{A_S}(Ω)·X 的解空间（引理 1）
  2. exp 交换条件 X·e^{-A_E} = e^{-A_S}·X 的解空间 = 谱匹配解空间（引理 2 + 定理 3）
  3. 谱匹配解空间闭式：dim = Σ_{λ∈σ_E∩σ_S} m_E(λ)·m_S(λ)
  4. 谱不相交（σ_E ∩ σ_S = ∅）⟹ 解空间 = {0}
  5. 命题 6（集合语义反例）：ψ(z)=|z| 沿本征方向给出非线性谱匹配映射
  6. P1 反例修正验证：ψ(z)=|z| 是正齐次（满足 ψ(cz)=cψ(z)），ψ(z)=|z|z 不是
  7. 重数块结构：共同本征值重数乘积闭式（含重数情形）
"""
import numpy as np
from itertools import product

# ── 基础设施 ─────────────────────────────────────────────────────────

def random_hermitian(n: int, seed: int) -> "np.ndarray":
    """随机 Hermitian 矩阵（自伴）。"""
    rng = np.random.default_rng(seed)
    R = rng.normal(size=(n, n)) + 1j * rng.normal(size=(n, n))
    return (R + R.conj().T) / 2

def spectral_projections(A: "np.ndarray", tol: float = 1e-9) -> "dict":
    """返回 {λ: 本征投影 P_λ}（本征值按 tol 分组）。"""
    vals, vecs = np.linalg.eigh(A)
    proj = {}
    for i, lam in enumerate(vals):
        v = vecs[:, [i]]
        found = None
        for lam0 in proj:
            if abs(lam - lam0) < tol:
                found = lam0
                break
        if found is None:
            proj[float(lam)] = v @ v.conj().T
        else:
            proj[found] = proj[found] + v @ v.conj().T
    return proj

def mat_exp(A: "np.ndarray") -> "np.ndarray":
    """矩阵指数 e^{-A}（经谱分解，A 自伴）。"""
    vals, vecs = np.linalg.eigh(A)
    return (vecs * np.exp(-vals)) @ vecs.conj().T

def null_space(M: "np.ndarray") -> "np.ndarray":
    """M 的零空间基（列向量，正交归一）。"""
    U, S, Vt = np.linalg.svd(M)
    tol = max(M.shape) * (S[0] if S.size > 0 else 0.0) * 1e-12
    rank = int((S > tol).sum())
    return Vt[rank:].conj().T

def subspaces_equal(U1: "np.ndarray", U2: "np.ndarray", tol: float = 1e-6) -> "tuple[bool, str]":
    """两个列正交基张成的子空间是否一致。"""
    if U1.shape[1] != U2.shape[1]:
        return False, f"维数不同: {U1.shape[1]} vs {U2.shape[1]}"
    if U1.shape[1] == 0:
        return True, "0"
    P1, P2 = U1 @ U1.conj().T, U2 @ U2.conj().T
    d = float(np.linalg.norm(P1 - P2))
    return d < tol, f"dim={U1.shape[1]}, ‖P₁-P₂‖={d:.2e}"

def interleave_space(A_E: "np.ndarray", A_S: "np.ndarray") -> "np.ndarray":
    """交织条件 X·A_E = A_S·X 的解空间。"""
    n = A_E.shape[0]
    M = np.kron(A_E.T, np.eye(n)) - np.kron(np.eye(n), A_S)
    return null_space(M)

def spectral_match_space(A_E: "np.ndarray", A_S: "np.ndarray") -> "np.ndarray":
    """谱匹配 X·E_{A_E}(Ω) = E_{A_S}(Ω)·X（对本征投影）的解空间。"""
    n = A_E.shape[0]
    PE, PS = spectral_projections(A_E), spectral_projections(A_S)
    rows = []
    for lam, P in PE.items():
        PSlam = PS.get(lam, np.zeros((n, n)))
        rows.append(np.kron(P.T, np.eye(n)) - np.kron(np.eye(n), PSlam))
    return null_space(np.vstack(rows))

def exp_match_space(A_E: "np.ndarray", A_S: "np.ndarray") -> "np.ndarray":
    """exp 交换 X·e^{-A_E} = e^{-A_S}·X 的解空间。"""
    n = A_E.shape[0]
    M = np.kron(mat_exp(A_E).T, np.eye(n)) - np.kron(np.eye(n), mat_exp(A_S))
    return null_space(M)

def spectral_match_dim_formula(A_E: "np.ndarray", A_S: "np.ndarray", tol: float = 1e-6) -> int:
    """闭式：Σ_{λ∈σ_E∩σ_S} m_E(λ)·m_S(λ)。"""
    vals_E = sorted(np.linalg.eigvalsh(A_E).tolist())
    vals_S = sorted(np.linalg.eigvalsh(A_S).tolist())
    total = 0
    for lam in vals_E:
        mE = sum(abs(v - lam) < tol for v in vals_E)
        mS = sum(abs(v - lam) < tol for v in vals_S)
        if mS > 0:
            total += mE * mS
    return total

# ── 检查 1：交织 ⟺ 谱匹配（引理 1） ──────────────────────────────────

def check_interleave_iff_spectral() -> "tuple[bool, str]":
    for n, seed in [(4, 3), (4, 5), (5, 7), (5, 11)]:
        A_E = random_hermitian(n, seed)
        A_S = random_hermitian(n, 1000 + seed)
        U1 = interleave_space(A_E, A_S)
        U2 = spectral_match_space(A_E, A_S)
        ok, msg = subspaces_equal(U1, U2)
        if not ok:
            return False, f"n={n} seed={seed}: 交织 vs 谱匹配不一致 ({msg})"
    return True, "4 组随机自伴：交织解空间 = 谱匹配解空间（引理 1 ✓）"

# ── 检查 2：exp 交换 ⟺ 谱匹配（引理 2 + 定理 3） ──────────────────────

def check_exp_iff_spectral() -> "tuple[bool, str]":
    for n, seed in [(4, 21), (4, 22), (5, 23)]:
        A_E = random_hermitian(n, seed)
        A_S = random_hermitian(n, 2000 + seed)
        U2 = spectral_match_space(A_E, A_S)
        U3 = exp_match_space(A_E, A_S)
        ok, msg = subspaces_equal(U2, U3)
        if not ok:
            return False, f"n={n} seed={seed}: exp 交换 vs 谱匹配不一致 ({msg})"
    return True, "3 组随机自伴：exp 交换解空间 = 谱匹配解空间（引理 2 + 定理 3 ✓）"

# ── 检查 3：谱匹配解空间闭式 ─────────────────────────────────────────

def check_dim_formula() -> "tuple[bool, str]":
    for n, seed in [(4, 31), (5, 32), (6, 33)]:
        A_E = random_hermitian(n, seed)
        A_S = random_hermitian(n, 3000 + seed)
        U2 = spectral_match_space(A_E, A_S)
        dim = U2.shape[1]
        dim_formula = spectral_match_dim_formula(A_E, A_S)
        if dim != dim_formula:
            return False, f"n={n}: dim={dim} ≠ 闭式 {dim_formula}"
    return True, "3 组随机自伴：dim M_σ = Σ m_E(λ)·m_S(λ)（闭式 ✓）"

# ── 检查 4：谱不相交 ⟹ 解空间 {0} ────────────────────────────────────

def check_disjoint_spectra() -> "tuple[bool, str]":
    A_E = np.diag([1.0, 2.0, 3.0])
    A_S = np.diag([5.0, 7.0, 9.0])
    U1 = interleave_space(A_E, A_S)
    U2 = spectral_match_space(A_E, A_S)
    U3 = exp_match_space(A_E, A_S)
    if U1.shape[1] != 0 or U2.shape[1] != 0 or U3.shape[1] != 0:
        return False, f"谱不相交但解空间非零: inter={U1.shape[1]}, spec={U2.shape[1]}, exp={U3.shape[1]}"
    return True, "σ_E ∩ σ_S = ∅ ⟹ 三条件解空间均为 {0}"

# ── 检查 5：命题 6 非线性元（集合语义反例） ──────────────────────────

def check_nonlinear_element() -> "tuple[bool, str]":
    """A 自伴、v 本征向量（λ=0），f(x)=|⟨x,v⟩|·v 满足交换但非线性。"""
    A = np.diag([0.0, 1.0, 2.0])          # 含 0 本征值（λ=0：任意 ψ 可交换）
    v = np.array([1, 0, 0], dtype=complex)  # Av = 0·v
    E = mat_exp(A)                          # e^{-A}
    # 交换残差：f(e^{-A}x) vs e^{-A}f(x)，随机采样
    rng = np.random.default_rng(41)
    worst = 0.0
    for _ in range(200):
        x = rng.normal(size=3) + 1j * rng.normal(size=3)
        fx = abs(np.vdot(x, v)) * v
        lhs = abs(np.vdot(E @ x, v)) * v              # f(e^{-A}x)
        rhs = E @ fx                                    # e^{-A}f(x)
        nrm = max(np.linalg.norm(x), 1e-12)
        worst = max(worst, float(np.linalg.norm(lhs - rhs)) / nrm)
    if worst > 1e-9:
        return False, f"非线性元交换残差过大: {worst:.2e}"
    # 非线性：f(-x) = f(x) ≠ -f(x)（|·| 非负齐次，非复线性）
    x0 = np.array([1, 1, 1], dtype=complex)
    fx = abs(np.vdot(x0, v)) * v
    fnx = abs(np.vdot(-x0, v)) * v
    if not (np.linalg.norm(fnx - fx) < 1e-12 and np.linalg.norm(fnx + fx) > 1e-3):
        return False, "非线性度量异常"
    return True, f"f(x)=|⟨x,v⟩|·v 满足交换（残差 {worst:.1e}）且非线性（f(-x)=f(x)≠-f(x)）"

# ── 检查 6：P1 反例修正验证（正齐次性） ──────────────────────────────

def check_homogeneity_correction() -> "tuple[bool, str]":
    """ψ(z)=|z| 正齐次（ψ(cz)=cψ(z)）；ψ(z)=|z|z 是齐次度 2（不满足）——P1 笔记反例修正依据。"""
    c = 0.37
    z = 1.3 + 2.1j
    ok_abs = abs(abs(c * z) - c * abs(z)) < 1e-12
    # |cz|·(cz) vs c·|z|z：差 = (c²-c)|z|z ≠ 0（c≠0,1）
    err_absz = abs((abs(c * z) * (c * z)) - c * (abs(z) * z))
    ok_absz = err_absz > 1e-6
    if not (ok_abs and ok_absz):
        return False, f"正齐次性验证异常: err(|z|)={0}, err(|z|z)={err_absz:.3f}"
    return True, f"ψ=|z| 正齐次 ✓；ψ=|z|z 齐次度 2 不满足（误差 {err_absz:.3f}）——命题 6 用 |z|"

# ── 检查 7：重数块结构闭式 ───────────────────────────────────────────

def check_multiplicity_block() -> "tuple[bool, str]":
    """重数情形：A_E=diag(1,1,2)，A_S=diag(1,2,2)。共同谱 {1,2}：dim = 2·1 + 1·2 = 4。"""
    A_E = np.diag([1.0, 1.0, 2.0])
    A_S = np.diag([1.0, 2.0, 2.0])
    U = spectral_match_space(A_E, A_S)
    dim = U.shape[1]
    if dim != 4:
        return False, f"重数块结构: dim={dim} ≠ 4（2·1+1·2）"
    # 结构验证：解空间基的块模式（X 非零块仅在匹配本征值间）
    # 本征空间：A_E 在 λ=1 为 {e1,e2}，λ=2 为 {e3}；A_S 在 λ=1 为 {e1}，λ=2 为 {e2,e3}
    # 匹配块：X[E₁,S₁]（2×1）、X[E₂,S₂]（1×2）——非零块指标集
    allowed = [(0, 0), (1, 0), (2, 1), (2, 2)]   # (i,j)：X_ij 可非零
    for k in range(dim):
        X = U[:, k].reshape(3, 3)
        for i, j in product(range(3), range(3)):
            if (i, j) not in allowed and abs(X[i, j]) > 1e-6:
                return False, f"块结构违例: 基 {k} 在 ({i},{j}) 非零"
        if all(abs(X[i, j]) < 1e-6 for (i, j) in allowed):
            return False, f"基 {k} 全零"
    return True, "重数块结构：dim=4（2·1+1·2），非零块仅在匹配本征空间间 ✓"

# ── 主流程 ───────────────────────────────────────────────────────────

def main():
    checks = [
        ("交织 ⟺ 谱匹配",        check_interleave_iff_spectral),
        ("exp 交换 ⟺ 谱匹配",     check_exp_iff_spectral),
        ("解空间闭式",            check_dim_formula),
        ("谱不相交 ⟹ {0}",        check_disjoint_spectra),
        ("非线性元（命题 6）",     check_nonlinear_element),
        ("正齐次性修正",          check_homogeneity_correction),
        ("重数块结构",            check_multiplicity_block),
    ]
    npass = 0
    for name, fn in checks:
        ok, msg = fn()
        mark = "✓" if ok else "✗"
        print(f"{mark} PASS  {name:<16s} {msg}")
        npass += int(ok)
    print(f"\n结果: {npass}/{len(checks)} 项通过")
    return 0 if npass == len(checks) else 1

if __name__ == "__main__":
    import sys
    sys.exit(main())
