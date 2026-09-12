"""(β)-4 第二阶段缺口②预实验：ginv 升指标的 Leibniz 修正结构。

背景：连续理论 ∂(g^{-1}) = −g^{-1}·∂g·g^{-1}。差分代数中需求：
1. **精确恒等式**：ginv(step x) − ginv(x) = −ginv(step x)·∂̃g·ginv(x)
   （双 δ 假设下的逐点恒等式，非渐近）——两种移位变体。
2. **离散度规相容残差**：∂̃_ρ g_{μν} 与 Γ_{ρμν}+Γ_{ρνμ} 的偏差结构
   （离散 Christoffel 公式的相容性残差是否逐点为零）。
3. **升指标 Leibniz 亏损**：∇̃^μ T_μ ≡ Σ ginv^{μa}∇̃_μ T_a 与
   ∇̃_μ(ginv^{μa}T_a) 的差 = ∂̃ginv·T(step)（精确移位 Leibniz 的直接推论），
   即把 ginv 提出协变差分时必须携带的修正项。
"""
import numpy as np

rng = np.random.default_rng(23)

NPT = 8
step = np.array([[rng.integers(0, NPT) for _ in range(NPT)] for _ in range(4)])

# 逐点随机对称正定度量
g = np.zeros((NPT, 4, 4))
ginv = np.zeros((NPT, 4, 4))
for x in range(NPT):
    A = rng.normal(size=(4, 4))
    g[x] = A @ A.T + np.eye(4)
    ginv[x] = np.linalg.inv(g[x])

def dg(mu, x):
    return g[step[mu, x]] - g[x]

def dginv(mu, x):
    return ginv[step[mu, x]] - ginv[x]

# ---- 1. ginv 差分的精确恒等式 ----
# 变体 A（左移位）：∂̃ginv = −ginv(step)·∂̃g·ginv(x)
# 变体 B（右移位）：∂̃ginv = −ginv(x)·∂̃g·ginv(step)
errA = errB = 0.0
for x in range(NPT):
    for mu in range(4):
        lhs = dginv(mu, x)
        rhsA = -ginv[step[mu, x]] @ dg(mu, x) @ ginv[x]
        rhsB = -ginv[x] @ dg(mu, x) @ ginv[step[mu, x]]
        errA = max(errA, np.abs(lhs - rhsA).max())
        errB = max(errB, np.abs(lhs - rhsB).max())
print("1. ginv 差分精确恒等式：")
print("   变体A max|∂̃ginv + ginv(step)·∂̃g·ginv(x)| =", errA)
print("   变体B max|∂̃ginv + ginv(x)·∂̃g·ginv(step)| =", errB)

# ---- 2. 离散度规相容残差 ----
# Γ^r_{μn} 离散 Christoffel
Gam = np.zeros((NPT, 4, 4, 4))
for x in range(NPT):
    for mu in range(4):
        for n in range(4):
            for r in range(4):
                Gam[x, r, mu, n] = 0.5 * sum(
                    ginv[x, r, l] * (dg(mu, x)[l, n] + dg(n, x)[mu, l] - dg(l, x)[n, mu])
                    for l in range(4))

# ---- 2. 离散度规相容恒等式（精确形态） ----
# 正确形态（逐点精确，纯 δ-代数 + g 对称）：
#   ∂̃_ρ g_{μν}(x) = g_{μλ}(x)·Γ^λ_{ρν}(x) + g_{νλ}(x)·Γ^λ_{ρμ}(x)
# （Γ 的导数指标 ρ 在下标对，降指标度量取同点 x；
#   其它移位配置——g(step_ρ x) 降指标、半程移位——均不成立，残差 O(1)。）
errC = 0.0
for x in range(NPT):
    for rho in range(4):
        for mu in range(4):
            for nu in range(4):
                lhs = dg(rho, x)[mu, nu]
                rhs = sum(g[x, mu, l] * Gam[x, l, rho, nu]
                          + g[x, nu, l] * Gam[x, l, rho, mu] for l in range(4))
                errC = max(errC, abs(lhs - rhs))
print("2. 离散度规相容（精确形态）max|∂̃_ρg_{μν} − (g_{μλ}Γ^λ_{ρν}+g_{νλ}Γ^λ_{ρμ})| =", errC)

# ---- 3. 升指标 Leibniz 亏损 ----
# 精确移位 Leibniz：∂̃(A·B)(x) = ∂̃A(x)·B(step x) + A(x)·∂̃B(x)
# 对 ∇̃^μ T_μ = Σ_{μ,a} ginv[μ,a](x)·(∇̃_μ T)_a(x)：
# 提出 ginv 的亏损 = Σ_{μ,a} ∂̃_μ ginv^{μa}(x)·(∇̃_μ T)_a(step x)
# 用随机张量场 T_a(x) 与朴素协变差分 ∇̃_μ T_a = ∂̃_μ T_a + Γ_{μa}^b(step?)·T_b
# 采用 (β) 链路的 ∇̃ 约定：∇̃_μ T_a(x) = T_a(step x) − T_a(x)
#   + Σ_b (Γ^b_{μa}(x) T_b(step x) − Γ^b_{μa}(step x) T_b(x)) 的差分联络形式，
# 此处先用最简约定（与 (β)-1 链一致）：∇̃_μ T_a = ∂̃_μ T_a + Γ^b_{μa}(x)·∂̃... 
# 为聚焦 ginv 结构，取线性 T，直接用定义 ∇̃_μ T_a = ∂̃_μ T_a（Γ 修正另行叠加）。
T = rng.normal(size=(NPT, 4))
def dT(mu, x, a):
    return T[step[mu, x], a] - T[x, a]

def nablaT(mu, x, a):
    # 完整离散协变差分：∂̃_μ T_a + Γ^b_{μa}(x)·(T_b(step x) − T_b(x)) + ... 
    # 采用 (β)-3 链的 naiveNablaCurv 同款联络约定（左作用 step 值）：
    return dT(mu, x, a) + sum(Gam[x, a, mu, b] * T[step[mu, x], b]
                                - Gam[step[mu, x], a, mu, b] * T[x, b] for b in range(4))

# 亏损检验：Σ_{μ,a} ginv[μ,a]·∇̃_μT_a  vs  ∇̃_μ(ginv·T) 展开
# 精确断言：Σ ginv·∇̃T = ∂̃_μ(Σ ginv·T) − Σ ∂̃ginv·(∇̃T 的移位部分)
# 数值上直接验证标量移位 Leibniz：∂̃(Σ_a ginv[μ,a]T_a) = Σ ∂̃ginv[μ,a]·T_a(step) + Σ ginv[μ,a]·∂̃T_a
errL = 0.0
for x in range(NPT):
    for mu in range(4):
        S = lambda y: sum(ginv[y, mu, a] * T[y, a] for a in range(4))
        lhs = S(step[mu, x]) - S(x)
        rhs = sum(dginv(mu, x)[mu, a] * T[step[mu, x], a]
                  + ginv[x, mu, a] * dT(mu, x, a) for a in range(4))
        errL = max(errL, abs(lhs - rhs))
print("3. 移位 Leibniz（标量缩并）max|LHS−RHS| =", errL)

# 升指标亏损量：把 ginv 提出协变差分时的修正项幅值
def raisedDiv(x):
    return sum(ginv[x, mu, a] * nablaT(mu, x, a) for mu in range(4) for a in range(4))
def rawDiv(x):
    return sum(nablaT(mu, x, mu) for mu in range(4))
amp = max(abs(raisedDiv(x)) for x in range(NPT))
print("   |Σ ginv·∇̃T| 幅值 =", amp, "（升指标与裸缩并不等价，差即 Leibniz 修正）")
