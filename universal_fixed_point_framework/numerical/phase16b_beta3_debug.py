"""(β)-3 调试：修正张量 Bianchi 恒等式的数值对照。

精确复现 Lean §26.11 定义（naiveCurv / naiveNablaCurv / bianchiCorr），
在抽象 FrameRecObj（随机 step 函数，无对易假设）上验证：
  Σ_s [Σ_cyc(lam,mu,nu) (∇̃ R̂ − C)]^r_s * v^s = 算子 Jacobi 恒等式左端 = 0。
若残差非零，打印残差单项式结构定位偏差。
"""
import numpy as np

rng = np.random.default_rng(7)

NPT = 8
step = np.array([[rng.integers(0, NPT) for _ in range(NPT)] for _ in range(4)])
# Gamma[point][r][m][n]
Gam = rng.normal(size=(NPT, 4, 4, 4))

def D(F, rho, V, x):
    """(D_rho V)(x) = V(step_rho x) − V(x) + Gam[x]·V(x)（对向量场 V: pt->4）。"""
    out = V[step[rho, x]] - V[x]
    out = out + np.einsum('rl,l->r', Gam[x, :, rho, :], V[x])
    return out

def F(F_, mu, nu, V, x):
    """curvatureOp 分量展开（无假设形态）。"""
    dbl = V[step[nu, step[mu, x]]] - V[step[mu, step[nu, x]]]
    t1 = np.einsum('rl,l->r', Gam[step[mu, x], :, nu, :] - Gam[x, :, nu, :], V[step[mu, x]])
    t2 = np.einsum('rl,l->r', Gam[step[nu, x], :, mu, :] - Gam[x, :, mu, :], V[step[nu, x]])
    wedge = np.einsum('rm,ml->rl', Gam[x, :, mu, :], Gam[x, :, nu, :]) \
        - np.einsum('rm,ml->rl', Gam[x, :, nu, :], Gam[x, :, mu, :])
    return dbl + t1 - t2 + wedge @ V[x]

def naiveCurv(x, r, s, mu, nu):
    return (Gam[step[mu, x], r, nu, s] - Gam[x, r, nu, s]) \
        - (Gam[step[nu, x], r, mu, s] - Gam[x, r, mu, s]) \
        + sum(Gam[x, r, mu, l] * Gam[x, l, nu, s] - Gam[x, r, nu, l] * Gam[x, l, mu, s]
              for l in range(4))

def naiveNablaCurv(lam, mu, nu, x, r, s):
    d = naiveCurv(step[lam, x], r, s, mu, nu) - naiveCurv(x, r, s, mu, nu)
    t1 = sum(Gam[x, r, lam, a] * naiveCurv(x, a, s, mu, nu) for a in range(4))
    t2 = sum(naiveCurv(x, r, a, mu, nu) * Gam[x, a, lam, s] for a in range(4))
    return d + t1 - t2

def bianchiCorr(lam, mu, nu, x, r, s):
    # 修正项 C = 双移位差 + ∂̃_μΓ_ν · ∂̃_μΓ_lam − ∂̃_νΓ_μ · ∂̃_νΓ_lam
    # （R̂Γ_λv 项精确抵消后的纯二阶差分形态，与 Lean §26.11 一致）
    dbl = Gam[step[nu, step[mu, x]], r, lam, s] - Gam[step[mu, step[nu, x]], r, lam, s]
    t1 = sum((Gam[step[mu, x], r, nu, l] - Gam[x, r, nu, l])
             * (Gam[step[mu, x], l, lam, s] - Gam[x, l, lam, s])
             for l in range(4))
    t2 = sum((Gam[step[nu, x], r, mu, l] - Gam[x, r, mu, l])
             * (Gam[step[nu, x], l, lam, s] - Gam[x, l, lam, s])
             for l in range(4))
    return dbl + t1 - t2

v = rng.normal(size=4)
x = 3
worst = 0.0
for lam in range(4):
    for mu in range(4):
        for nu in range(4):
            # LHS：Σ_s tensor^r_s v^s
            lhs = np.zeros(4)
            for r in range(4):
                for s in range(4):
                    lhs[r] += (naiveNablaCurv(lam, mu, nu, x, r, s) - bianchiCorr(lam, mu, nu, x, r, s)
                               + naiveNablaCurv(mu, nu, lam, x, r, s) - bianchiCorr(mu, nu, lam, x, r, s)
                               + naiveNablaCurv(nu, lam, mu, x, r, s) - bianchiCorr(nu, lam, mu, x, r, s)) * v[s]
            # RHS：算子 Jacobi 左端作用于常值场 v
            V = np.tile(v, (NPT, 1))
            W1 = np.array([F(None, mu, nu, V, y) for y in range(NPT)])
            W2 = np.array([F(None, nu, lam, V, y) for y in range(NPT)])
            W3 = np.array([F(None, lam, mu, V, y) for y in range(NPT)])
            U1 = np.array([D(None, lam, V, y) for y in range(NPT)])
            U2 = np.array([D(None, mu, V, y) for y in range(NPT)])
            U3 = np.array([D(None, nu, V, y) for y in range(NPT)])
            rhs = (D(None, lam, W1, x) - F(None, mu, nu, U1, x)
                   + D(None, mu, W2, x) - F(None, nu, lam, U2, x)
                   + D(None, nu, W3, x) - F(None, lam, mu, U3, x))
            resid = np.max(np.abs(lhs - rhs))
            worst = max(worst, resid)
            if resid > 1e-9:
                print(f'({lam},{mu},{nu}) resid={resid:.3e}')
                print('  lhs-rhs =', np.round(lhs - rhs, 6))
print('worst |LHS - RHS| =', worst)
