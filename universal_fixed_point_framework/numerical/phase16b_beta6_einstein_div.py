"""(β)-4 缺口③预实验：Einstein 张量构造与散度修正结构。

目标：
1. 构造 G_{μν} = Riĉ_{μν} − ½ g_{μν}R̂，R̂ = ginv^{σν}Riĉ_{σν}；
2. 计算 E_ν = ∇̃^μ G_{μν}（(β)-链 ∇̃ 约定），确认场层级不恒零并测幅值；
3. **PS 载体检验**：用对称化 Ricci 构造 G^sym，若 |E^sym| << |E|
   则确证散度亏损的主载体是 Ricci 不对称（§26.13 的 PS）；
4. 迹恒等式：ginv^{μν}G_{μν} = −R̂（4 维 δ-代数，应为机器精度）。
"""
import numpy as np

rng = np.random.default_rng(37)

NPT = 8
step = np.array([[rng.integers(0, NPT) for _ in range(NPT)] for _ in range(4)])

g = np.zeros((NPT, 4, 4)); ginv = np.zeros((NPT, 4, 4))
for x in range(NPT):
    A = rng.normal(size=(4, 4))
    g[x] = A @ A.T + np.eye(4); ginv[x] = np.linalg.inv(g[x])

def dg(mu, x): return g[step[mu, x]] - g[x]

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

def Ric(x, s, nu):
    return sum(naiveCurv(x, r, s, r, nu) for r in range(4))

def scalarR(x):
    return sum(ginv[x, s, nu] * Ric(x, s, nu) for s in range(4) for nu in range(4))

def nabla02(x, rho, T):
    """(β)-链约定下 (0,2) 张量 T_{σν} 的协变差分 (∇̃_ρ T)_{σν}。
    T: (NPT,4,4) 场。约定（与 covector 情形一致）：
    ∂̃_ρ T_{σν} + Γ^b_{ρσ}(x)T_{bν}(step) + Γ^b_{ρν}(x)T_{σb}(step)
               − Γ^b_{ρσ}(step)T_{bν}(x) − Γ^b_{ρν}(step)T_{σb}(x)"""
    xs = step[rho, x]
    out = np.zeros((4, 4))
    for sig in range(4):
        for nu in range(4):
            d = T[xs, sig, nu] - T[x, sig, nu]
            c = sum(Gam[x, b, rho, sig] * T[xs, b, nu]
                    + Gam[x, b, rho, nu] * T[xs, sig, b]
                    - Gam[xs, b, rho, sig] * T[x, b, nu]
                    - Gam[xs, b, rho, nu] * T[x, sig, b] for b in range(4))
            out[sig, nu] = d + c
    return out

def Gfield(sym=False):
    Gf = np.zeros((NPT, 4, 4))
    for x in range(NPT):
        Rm = np.array([[Ric(x, s, nu) for nu in range(4)] for s in range(4)])
        if sym:
            Rm = 0.5 * (Rm + Rm.T)
        Gf[x] = Rm - 0.5 * g[x] * scalarR_with(x, Rm)
    return Gf

def scalarR_with(x, Rm):
    return sum(ginv[x, s, nu] * Rm[s, nu] for s in range(4) for nu in range(4))

def divG(x, Gf):
    """E_ν = Σ_{μ,a} ginv^{μa}(x)·(∇̃_μ G)_{aν}(x)"""
    out = np.zeros(4)
    for mu in range(4):
        nG = nabla02(x, mu, Gf)
        for a in range(4):
            for nu in range(4):
                out[nu] += ginv[x, mu, a] * nG[a, nu]
    return out

x = 3
Gf = Gfield(sym=False)
Gsym = Gfield(sym=True)

E = divG(x, Gf)
Es = divG(x, Gsym)
amp_E = np.abs(E).max(); amp_Es = np.abs(Es).max()
scale = max(abs(scalarR(x)), 1e-30)
print("1. E_ν = ∇̃^μG_{μν} 场层级残差：")
print("   max|E| =", amp_E, " max|E^sym| =", amp_Es,
      " 比值 |E^sym|/|E| =", amp_Es / amp_E)
print("   |R̂| 尺度 =", scale, " |E|/|R̂| =", amp_E / scale)

# 2. 逐项分解：E = ∇̃^μRiĉ_{μν} − ½ ginv^{μa}∇̃_μ(g_{aν}R̂)
Rf = np.zeros((NPT, 4, 4))
gR = np.zeros((NPT, 4, 4))
for y in range(NPT):
    Rf[y] = [[Ric(y, s, nu) for nu in range(4)] for s in range(4)]
    gR[y] = g[y] * scalarR(y)
A = np.zeros(4); B = np.zeros(4)
for mu in range(4):
    nR = nabla02(x, mu, Rf)
    ngR = nabla02(x, mu, gR)
    for a in range(4):
        for nu in range(4):
            A[nu] += ginv[x, mu, a] * nR[a, nu]
            B[nu] += ginv[x, mu, a] * ngR[a, nu]
print("2. 线性分解 max|E − (A − ½B)| =", np.abs(E - (A - 0.5 * B)).max())

# 3. 迹恒等式：ginv^{μν}G_{μν} = −R̂
trG = sum(ginv[x, mu, nu] * Gf[x, mu, nu] for mu in range(4) for nu in range(4))
print("3. 迹恒等式 |ginv·G + R̂| =", abs(trG + scalarR(x)))

# 4. 对称化后迹不变性
trGs = sum(ginv[x, mu, nu] * Gsym[x, mu, nu] for mu in range(4) for nu in range(4))
print("   对称化迹 |ginv·G^sym + R̂^sym| =", abs(trGs + scalarR_with(x, 0.5 * (Rf[x] + Rf[x].T))))

# 4. ginv-Leibniz 精确份额：E = Σ_μ ∂̃_μ H^{(μ)} − Σ∂̃ginv·G(step) + Σ ginv·conn(G)，
#    方向指标化标量场 H^{(μ)}_ν(y) := Σ_a ginv[y,μ,a]G[y,a,ν]
#    （关键：收缩指标 μ 与求导方向 μ 绑定，不能先对 μ 全求和再造标量场）
def dginv(mu, x): return ginv[step[mu, x]] - ginv[x]
def connG(x, mu, Gf):
    """(∇̃_μ G − ∂̃_μ G)_{aν}：联络部分"""
    xs = step[mu, x]
    out = np.zeros((4, 4))
    for a in range(4):
        for nu in range(4):
            out[a, nu] = sum(Gam[x, b, mu, a] * Gf[xs, b, nu]
                             + Gam[x, b, mu, nu] * Gf[xs, a, b]
                             - Gam[xs, b, mu, a] * Gf[x, b, nu]
                             - Gam[xs, b, mu, nu] * Gf[x, a, b] for b in range(4))
    return out

Hmu = lambda y, mu, nu: sum(ginv[y, mu, a] * Gf[y, a, nu] for a in range(4))
xs_cache = {mu: step[mu, x] for mu in range(4)}
dH = np.array([sum(Hmu(xs_cache[mu], mu, nu) - Hmu(x, mu, nu)
                   for mu in range(4)) for nu in range(4)])
ginvShift = np.zeros(4); ginvConn = np.zeros(4)
for mu in range(4):
    xs = xs_cache[mu]
    cG = connG(x, mu, Gf)
    for a in range(4):
        for nu in range(4):
            ginvShift[nu] += dginv(mu, x)[mu, a] * Gf[xs, a, nu]
            ginvConn[nu] += ginv[x, mu, a] * cG[a, nu]
print("4. ginv-Leibniz 精确份额 max|E − (Σ∂̃H − Σ∂̃ginv·G(step) + Σginv·connG)| =",
      np.abs(E - (dH - ginvShift + ginvConn)).max())

# ∂̃ 幅度标定：残差随度量扰动 ε 的阶
print("5. 扰动标定：", end=" ")
for eps in [1.0, 0.1, 0.01]:
    g2 = np.zeros((NPT, 4, 4)); ginv2 = np.zeros((NPT, 4, 4))
    for y in range(NPT):
        g2[y] = np.eye(4) + eps * (g[y] - np.eye(4))
        ginv2[y] = np.linalg.inv(g2[y])
    # 重算 Christoffel/Ricci/G/散度
    Gm2 = np.zeros((NPT, 4, 4, 4))
    for y in range(NPT):
        for mu in range(4):
            for n in range(4):
                for r in range(4):
                    Gm2[y, r, mu, n] = 0.5 * sum(
                        ginv2[y, r, l] * (g2[step[mu, y], l, n] - g2[y, l, n]
                                          + g2[step[n, y], mu, l] - g2[y, mu, l]
                                          - g2[step[l, y], n, mu] + g2[y, n, mu])
                        for l in range(4))
    def curv2(y, r, s, mu, nu):
        return (Gm2[step[mu, y], r, nu, s] - Gm2[y, r, nu, s]) \
            - (Gm2[step[nu, y], r, mu, s] - Gm2[y, r, mu, s]) \
            + sum(Gm2[y, r, mu, l] * Gm2[y, l, nu, s]
                  - Gm2[y, r, nu, l] * Gm2[y, l, mu, s] for l in range(4))
    Rm2 = np.zeros((NPT, 4, 4))
    for y in range(NPT):
        Rm2[y] = [[sum(curv2(y, r, s, r, nu) for r in range(4)) for nu in range(4)]
                  for s in range(4)]
    Rsc2 = np.array([sum(ginv2[y, s, nu] * Rm2[y, s, nu]
                         for s in range(4) for nu in range(4)) for y in range(NPT)])
    Gf2 = np.array([Rm2[y] - 0.5 * g2[y] * Rsc2[y] for y in range(NPT)])
    def nb2(y, rho, T):
        xs = step[rho, y]
        out = np.zeros((4, 4))
        for sig in range(4):
            for nu in range(4):
                out[sig, nu] = (T[xs, sig, nu] - T[y, sig, nu]
                                + sum(Gm2[y, b, rho, sig] * T[xs, b, nu]
                                      + Gm2[y, b, rho, nu] * T[xs, sig, b]
                                      - Gm2[xs, b, rho, sig] * T[y, b, nu]
                                      - Gm2[xs, b, rho, nu] * T[y, sig, b]
                                      for b in range(4)))
        return out
    E2 = np.zeros(4)
    for mu in range(4):
        nG = nb2(x, mu, Gf2)
        for a in range(4):
            for nu in range(4):
                E2[nu] += ginv2[x, mu, a] * nG[a, nu]
    print(f"ε={eps}: max|E|={np.abs(E2).max():.3e}", end="  ")
print()
