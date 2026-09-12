"""(β)-4 预实验：修正 Bianchi 的度规缩并。

步骤：
1. 随机对称正定度量 g（逐点）、ginv = inv(g)、离散 Christoffel：
     Gam^r_{mu n}(x) = 1/2 Σ_l ginv[r,l] ( ∂̃_mu g_{ln} + ∂̃_n g_{mu l} − ∂̃_l g_{n mu} )
2. Riĉ_{sν}(x) = Σ_r naiveCurv(x, r, s, r, ν) 场层级对称性残差测量。
3. 缩并 (β)-3 恒等式（ginv 缩 λ↔r）确认精确为零，再拆解各项
   识别 divRic / ∂̃R 与修正项结构。
"""
import numpy as np

rng = np.random.default_rng(11)

NPT = 8
step = np.array([[rng.integers(0, NPT) for _ in range(NPT)] for _ in range(4)])

# 逐点随机对称正定度量：A A^T + I
g = np.zeros((NPT, 4, 4))
ginv = np.zeros((NPT, 4, 4))
for x in range(NPT):
    A = rng.normal(size=(4, 4))
    g[x] = A @ A.T + np.eye(4)
    ginv[x] = np.linalg.inv(g[x])

def dg(mu, x):
    return g[step[mu, x]] - g[x]

Gam = np.zeros((NPT, 4, 4, 4))
for x in range(NPT):
    for mu in range(4):
        for n in range(4):
            for r in range(4):
                Gam[x, r, mu, n] = 0.5 * sum(
                    ginv[x, r, l] * (dg(mu, x)[l, n] + dg(n, x)[mu, l] - dg(l, x)[n, mu])
                    for l in range(4))

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
    dbl = Gam[step[nu, step[mu, x]], r, lam, s] - Gam[step[mu, step[nu, x]], r, lam, s]
    t1 = sum((Gam[step[mu, x], r, nu, l] - Gam[x, r, nu, l])
             * (Gam[step[mu, x], l, lam, s] - Gam[x, l, lam, s]) for l in range(4))
    t2 = sum((Gam[step[nu, x], r, mu, l] - Gam[x, r, mu, l])
             * (Gam[step[nu, x], l, lam, s] - Gam[x, l, lam, s]) for l in range(4))
    return dbl + t1 - t2

x = 3

# ---- 1. Ricci 对称性残差 ----
Ric = np.zeros((4, 4))
for s in range(4):
    for nu in range(4):
        Ric[s, nu] = sum(naiveCurv(x, r, s, r, nu) for r in range(4))
asym = Ric - Ric.T
print("Ricci 不对称残差 max|Ric-Ric^T| =", np.abs(asym).max())
print("Ricci 尺度 max|Ric| =", np.abs(Ric).max())

# ---- 2. 缩并 (β)-3：ginv 缩 λ↔r ----
# P_{μνs} = Σ_{λ,r} ginv[λ,r] naiveNablaCurv(λ,μ,ν,x,r,s) + cyc
def contractBianchi(lam, mu, nu, s, corr=False):
    def term(a_lam, a_mu, a_nu):
        t = 0.0
        for la in range(4):
            for r in range(4):
                v = naiveNablaCurv(a_lam, a_mu, a_nu, x, r, s)
                if corr:
                    v -= bianchiCorr(a_lam, a_mu, a_nu, x, r, s)
                t += ginv[x, la, r] * v
        return t
    return term(lam, mu, nu) + term(mu, nu, lam) + term(nu, lam, mu)

worst_naive = 0.0
worst_exact = 0.0
for lam in range(4):
    for mu in range(4):
        for nu in range(4):
            for s in range(4):
                if len({lam, mu, nu}) < 3:
                    continue  # 跳过退化指标（循环和由反对称性恒零）
                worst_naive = max(worst_naive, abs(contractBianchi(lam, mu, nu, s, corr=False)))
                worst_exact = max(worst_exact, abs(contractBianchi(lam, mu, nu, s, corr=True)))
print("ginv 缩并循环和（朴素）max =", worst_naive)
print("ginv 缩并循环和（−C 修正）max =", worst_exact)

# ---- 3. 拆解：P_{μνs} 各项识别 ----
# naiveNablaCurv = ∂̃_λ R̂ + [Γ_λ, R̂]。缩并 ginv：
# Σ ginv[λ,r] ∂̃_λ R̂^r_{sμν} = ∂̃_λ(Σ ginv[λ,r] R̂^r_{sμν}) − Σ ∂̃_λ ginv[λ,r] R̂^r_{sμν}
# ∂̃ginv = −ginv ∂̃g ginv（矩阵恒等式），离散 Christoffel 下 ∂̃g 由 Γ 表示（相容条件）。
# ---- 3. 第一阶段：裸迹缩并 (β)-3（λ=r 求和，无度量）----
# 恒等式：Σ_r [N(r,μ,ν)^r_s + N(μ,ν,r)^r_s + N(ν,r,μ)^r_s
#           − C(r,μ,ν)^r_s − C(μ,ν,r)^r_s − C(ν,r,μ)^r_s] = 0（精确）
def Ricci(s, nu, y):
    return sum(naiveCurv(y, r, s, r, nu) for r in range(4))

worst = 0.0
for mu in range(4):
    for nu in range(4):
        for s in range(4):
            K = 0.0
            for r in range(4):
                K += naiveNablaCurv(r, mu, nu, x, r, s) \
                    + naiveNablaCurv(mu, nu, r, x, r, s) \
                    + naiveNablaCurv(nu, r, mu, x, r, s) \
                    - bianchiCorr(r, mu, nu, x, r, s) \
                    - bianchiCorr(mu, nu, r, x, r, s) \
                    - bianchiCorr(nu, r, mu, x, r, s)
            worst = max(worst, abs(K))
print("裸迹缩并（−C）max =", worst)

# ---- 4. Riemann 散度 = Ricci 差（修正版）----
# 定义 Q_{μνs} = Σ_r N(r,μ,ν)^r_s − ∂̃_μ Ric_{sν} + ∂̃_ν Ric_{sμ}
# 连续恒等式 Q = 联络修正 + 缩并 C；数值定位修正的精确形态。
def dRic(mu, s, nu, y):
    return Ricci(s, nu, step[mu, y]) - Ricci(s, nu, y)

def Q(mu, nu, s):
    p1 = sum(naiveNablaCurv(r, mu, nu, x, r, s) for r in range(4))
    return p1 - dRic(mu, s, nu, x) + dRic(nu, s, mu, x)

# 联络修正候选：P2 = Σ_r ∇̃_μ R̂^r_{sνr} = −∂̃_μ Ric_{sν}
#   + Σ_{r,a} Γ^r_{μa} R̂^a_{sνr} − Σ_a Ric_{aν} Γ^a_{μs}
# P3 = Σ_r ∇̃_ν R̂^r_{srμ} = +∂̃_ν Ric_{sμ}
#   − Σ_{r,a} Γ^r_{νa} R̂^a_{srμ} + Σ_a Ric_{aμ} Γ^a_{νs}
def connCorr2(mu, nu, s):
    # P2 = −∂̃_μ Ric_{sν} + Σ_{r,a} Γ^r_{μa} R̂^a_{sνr} + Σ_a Ric_{aν} Γ^a_{μs}
    t1 = sum(Gam[x, r, mu, a] * naiveCurv(x, a, s, nu, r) for r in range(4) for a in range(4))
    t2 = sum(Ricci(a, nu, x) * Gam[x, a, mu, s] for a in range(4))
    return t1 + t2

def connCorr3(mu, nu, s):
    # P3 = +∂̃_ν Ric_{sμ} + Σ_{r,a} Γ^r_{νa} R̂^a_{srμ} − Σ_a Ric_{aμ} Γ^a_{νs}
    t1 = sum(Gam[x, r, nu, a] * naiveCurv(x, a, s, r, mu) for r in range(4) for a in range(4))
    t2 = sum(Ricci(a, mu, x) * Gam[x, a, nu, s] for a in range(4))
    return t1 - t2

# 恒等式检验：Q = connCorr2 + connCorr3 + 缩并 C（三项循环）
worstQ = 0.0
qscale = 0.0
for mu in range(4):
    for nu in range(4):
        for s in range(4):
            # C 缩并三项：C(r,μ,ν)、C(μ,ν,r)、C(ν,r,μ) 各对 r 求和
            cc3 = sum(bianchiCorr(r, mu, nu, x, r, s) for r in range(4)) \
                + sum(bianchiCorr(mu, nu, r, x, r, s) for r in range(4)) \
                + sum(bianchiCorr(nu, r, mu, x, r, s) for r in range(4))
            lhs = Q(mu, nu, s)
            rhs = cc3 - connCorr2(mu, nu, s) - connCorr3(mu, nu, s)
            worstQ = max(worstQ, abs(lhs - rhs))
            qscale = max(qscale, abs(lhs))
print("Riemann 散度恒等式残差 max|Q − connCorr − C缩并| =", worstQ)
print("Q 量级 max|Q| =", qscale)


# ---- 5. key 恒等式复核：Lean key 两侧之差 ----
def LHS_lean(mu, nu, s):
    p1 = sum(naiveNablaCurv(r, mu, nu, x, r, s) for r in range(4))
    return p1 - (Ricci(s, nu, step[mu, x]) - Ricci(s, nu, x)) \
        + (Ricci(s, mu, step[nu, x]) - Ricci(s, mu, x))

def cc3_py(mu, nu, s):
    return sum(bianchiCorr(r, mu, nu, x, r, s) for r in range(4)) \
        + sum(bianchiCorr(mu, nu, r, x, r, s) for r in range(4)) \
        + sum(bianchiCorr(nu, r, mu, x, r, s) for r in range(4))

def RHS_lean(mu, nu, s):
    return cc3_py(mu, nu, s) - connCorr2(mu, nu, s) - connCorr3(mu, nu, s)

def cyclicNC(r, mu, nu, s):
    return (naiveNablaCurv(r, mu, nu, x, r, s) - bianchiCorr(r, mu, nu, x, r, s)
            + naiveNablaCurv(mu, nu, r, x, r, s) - bianchiCorr(mu, nu, r, x, r, s)
            + naiveNablaCurv(nu, r, mu, x, r, s) - bianchiCorr(nu, r, mu, x, r, s))

worst_key = 0.0
worst_goal = 0.0
for mu in range(4):
    for nu in range(4):
        for s in range(4):
            key_res = (LHS_lean(mu, nu, s) - RHS_lean(mu, nu, s)) \
                - sum(cyclicNC(r, mu, nu, s) for r in range(4))
            worst_key = max(worst_key, abs(key_res))
            worst_goal = max(worst_goal, abs(LHS_lean(mu, nu, s) - RHS_lean(mu, nu, s)))
print("key 恒等式残差 max =", worst_key)
print("目标恒等式残差 max|LHS−RHS| =", worst_goal)

# ---- 6. P2/P3 分片验证 ----
w2 = w3 = 0.0
for mu in range(4):
    for nu in range(4):
        for s in range(4):
            P2 = sum(naiveNablaCurv(mu, nu, r, x, r, s) for r in range(4))
            P3 = sum(naiveNablaCurv(nu, r, mu, x, r, s) for r in range(4))
            w2 = max(w2, abs(P2 - (-(Ricci(s, nu, step[mu, x]) - Ricci(s, nu, x)) + connCorr2(mu, nu, s))))
            w3 = max(w3, abs(P3 - ((Ricci(s, mu, step[nu, x]) - Ricci(s, mu, x)) + connCorr3(mu, nu, s))))
print("P2 分解残差 max =", w2)
print("P3 分解残差 max =", w3)

# ---- 7. Ricci 对称性修正形态：pair-swap 残差恒等式 ----
# 经典推导（仅用 pair swap 与 ginv·g=δ，无场方程）：
#   A_{σν} := Ric_{σν} − Ric_{νσ} = g^{ab}(R_{bσaν} − R_{bνaσ})
#   pair swap: R_{bσaν} = R_{aνbσ} + PS_{bσaν}（PS := R4 − swap）
#   ⟹ 2A = g^{ab}(PS_{bσaν} − PS_{bνaσ})
R4 = np.zeros((4, 4, 4, 4))
for a in range(4):
    for b in range(4):
        for c in range(4):
            for d in range(4):
                R4[a, b, c, d] = sum(g[x, a, r] * naiveCurv(x, r, b, c, d) for r in range(4))

def PS(a, b, c, d):
    return R4[a, b, c, d] - R4[c, d, a, b]

worst_id = 0.0
ps_scale = 0.0
for sig in range(4):
    for nu in range(4):
        A = Ric[sig, nu] - Ric[nu, sig]
        rhs = 0.5 * sum(ginv[x, a, b] * (PS(b, sig, a, nu) - PS(b, nu, a, sig))
                        for a in range(4) for b in range(4))
        worst_id = max(worst_id, abs(A - rhs))
        ps_scale = max(ps_scale, max(abs(PS(sig, a, nu, b))
                       for a in range(4) for b in range(4)))
print("pair-swap 残差恒等式 max|A − rhs| =", worst_id)
print("PS 量级 max|PS| =", ps_scale, " A 量级 max|A| =", np.abs(Ric - Ric.T).max())
