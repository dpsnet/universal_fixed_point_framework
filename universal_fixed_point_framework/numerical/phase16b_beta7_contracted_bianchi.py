"""(β)-4 最后一步预实验：Einstein 散度修正的显式形态（端到端装配）。

链条：§26.12（Riemann 散度）ginv 缩并 → Q − T1 + T2 = ginv·(Cc3−K2−K3)；
∇̃^μRiĉ_{μν} = T1 + ConnRic；∇̃^μG_{μν} = ∇̃^μRiĉ_{μν} − ½ ginv^{μa}∇̃_μ(g_{aν}R̂)。
装配目标（★）：
  E_ν = Q_ν + T2_ν + ConnRic_ν − ginv·(Cc3−K2−K3)_ν − ½ B_ν
全部项独立计算，机器精度闭合则显式修正形态确立。
"""
import numpy as np

rng = np.random.default_rng(41)
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
def contractCorr(mu, nu, x, s):
    return sum(bianchiCorr(r, mu, nu, x, r, s) + bianchiCorr(mu, nu, r, x, r, s)
               + bianchiCorr(nu, r, mu, x, r, s) for r in range(4))
def contractConn2(mu, nu, x, s):
    return sum(Gam[x, r, mu, a] * naiveCurv(x, a, s, nu, r)
               for r in range(4) for a in range(4)) \
        + sum(sum(naiveCurv(x, r, a, r, nu) for r in range(4)) * Gam[x, a, mu, s]
              for a in range(4))
def contractConn3(mu, nu, x, s):
    return sum(Gam[x, r, nu, a] * naiveCurv(x, a, s, r, mu)
               for r in range(4) for a in range(4)) \
        - sum(sum(naiveCurv(x, r, a, r, mu) for r in range(4)) * Gam[x, a, nu, s]
              for a in range(4))
def Ric(x, s, nu):
    return sum(naiveCurv(x, r, s, r, nu) for r in range(4))
def nabla02(x, rho, T):
    xs = step[rho, x]
    out = np.zeros((4, 4))
    for sig in range(4):
        for nu in range(4):
            out[sig, nu] = (T[xs, sig, nu] - T[x, sig, nu]
                            + sum(Gam[x, b, rho, sig] * T[xs, b, nu]
                                  + Gam[x, b, rho, nu] * T[xs, sig, b]
                                  - Gam[xs, b, rho, sig] * T[x, b, nu]
                                  - Gam[xs, b, rho, nu] * T[x, sig, b]
                                  for b in range(4)))
    return out

x = 3
Rm = np.zeros((NPT, 4, 4)); Rsc = np.zeros(NPT)
for y in range(NPT):
    Rm[y] = [[Ric(y, s, nu) for nu in range(4)] for s in range(4)]
    Rsc[y] = sum(ginv[y, s, nu] * Rm[y, s, nu] for s in range(4) for nu in range(4))
gR = np.array([g[y] * Rsc[y] for y in range(NPT)])
Gf = np.array([Rm[y] - 0.5 * g[y] * Rsc[y] for y in range(NPT)])

def st(mu): return step[mu, x]

# 各独立项
Q = np.zeros(4); T1 = np.zeros(4); T2 = np.zeros(4); gC = np.zeros(4)
for s_ in range(4):
    for mu in range(4):
        w = ginv[x, s_, mu]
        Q += w * np.array([sum(naiveNablaCurv(r, mu, nu, x, r, s_) for r in range(4))
                           for nu in range(4)])
        T1 += w * np.array([Rm[st(mu), s_, nu] - Rm[x, s_, nu] for nu in range(4)])
        T2 += w * np.array([Rm[st(3) if False else step[nu, x], s_, mu] - Rm[x, s_, mu]
                            for nu in range(4)]) * 0  # 占位
# T2 正确计算：∂̃_ν Riĉ_{sμ} 对 ν 求和输出
T2 = np.zeros(4)
for nu in range(4):
    for s_ in range(4):
        for mu in range(4):
            T2[nu] += ginv[x, s_, mu] * (Rm[step[nu, x], s_, mu] - Rm[x, s_, mu])
for s_ in range(4):
    for mu in range(4):
        gC += ginv[x, s_, mu] * np.array(
            [contractCorr(mu, nu, x, s_) - contractConn2(mu, nu, x, s_)
             - contractConn3(mu, nu, x, s_) for nu in range(4)])
ConnRic = np.zeros(4); A = np.zeros(4); B = np.zeros(4); E = np.zeros(4)
for mu in range(4):
    nR = nabla02(x, mu, Rm)
    ngR = nabla02(x, mu, gR)
    nG = nabla02(x, mu, Gf)
    for a in range(4):
        for nu in range(4):
            ConnRic[nu] += ginv[x, mu, a] * (nR[a, nu] - (Rm[st(mu), a, nu] - Rm[x, a, nu]))
            A[nu] += ginv[x, mu, a] * nR[a, nu]
            B[nu] += ginv[x, mu, a] * ngR[a, nu]
            E[nu] += ginv[x, mu, a] * nG[a, nu]

print("1. 缩并 Riemann 散度（§26.12 的 ginv 缩并）：")
print("   max|Q − T1 + T2 − ginv·(Cc3−K2−K3)| =", np.abs(Q - T1 + T2 - gC).max())
print("2. ∇̃^μRiĉ 分解：max|A − (T1 + ConnRic)| =", np.abs(A - T1 - ConnRic).max())
print("3. 端到端装配（★）：max|E − (Q + T2 + ConnRic − gC − ½B)| =",
      np.abs(E - (Q + T2 + ConnRic - gC - 0.5 * B)).max())
print("4. 曲率散度缺陷：max|Q − ½∂̃_νR̂| =",
      np.abs(Q - 0.5 * np.array([Rsc[step[nu, x]] - Rsc[x] for nu in range(4)])).max())
dR = np.array([Rsc[step[nu, x]] - Rsc[x] for nu in range(4)])
print("   ∂̃_νR̂ 幅值 =", np.abs(dR).max())
print("5. 各项幅值：|Q| =", np.abs(Q).max(), "|T2| =", np.abs(T2).max(),
      "|ConnRic| =", np.abs(ConnRic).max(), "|gC| =", np.abs(gC).max(),
      "|B| =", np.abs(B).max(), "|E| =", np.abs(E).max())
