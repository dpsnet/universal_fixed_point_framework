"""(β) 新阶段预实验：度规项 B 的 δ 展开与 ConnRic 的曲率迹展开。

B_ν = Σ_{μa} ginv^{μa}∇̃_μ(g_{aν}R̂) 展开：
  ∂̃(gR̂) 部分：∂̃_μ g_{aν}·R̂(step) + g_{aν}·∂̃_μR̂
  conn(gR̂) 部分：Σ_b[Γ^b_{μa}(x)g_{bν}(step)R̂(step) + Γ^b_{μν}(x)g_{ab}(step)R̂(step)
                    − Γ^b_{μa}(step)g_{bν}(x)R̂(x) − Γ^b_{μν}(step)g_{ab}(x)R̂(x)]
  δ 缩并：Σ_a ginv^{μa}g_{aν} = δ^μ_ν（hctr，无需对称）
  ⟹ B_ν = ∂̃_νR̂ + 度规相容型修正（5 项显式）

ConnRic_ν = Σ_{μa} ginv^{μa}(conn_μ Riĉ)_{aν} 展开为 ginv·Γ·naiveCurv 四重和（K 型）。
"""
import numpy as np

rng = np.random.default_rng(43)
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

Rm = np.zeros((NPT, 4, 4)); Rsc = np.zeros(NPT)
for y in range(NPT):
    Rm[y] = [[Ric(y, s, nu) for nu in range(4)] for s in range(4)]
    Rsc[y] = sum(ginv[y, s, nu] * Rm[y, s, nu] for s in range(4) for nu in range(4))
gR = np.array([g[y] * Rsc[y] for y in range(NPT)])

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
# ---- B 直接值 ----
B = np.zeros(4)
for mu in range(4):
    ngR = nabla02(x, mu, gR)
    for a in range(4):
        for nu in range(4):
            B[nu] += ginv[x, mu, a] * ngR[a, nu]

# ---- B 的 δ 展开 ----
dR = np.zeros(4)       # ∂̃_ν R̂
corr = np.zeros(4)     # 度规相容型修正（5 项）
for mu in range(4):
    xs = step[mu, x]
    for nu in range(4):
        dR[nu] += (Rsc[xs] - Rsc[x]) * (1.0 if nu == mu else 0.0)
        for a in range(4):
            w = ginv[x, mu, a]
            corr[nu] += w * ((g[xs, a, nu] - g[x, a, nu]) * Rsc[xs]
                             + sum(Gam[x, b, mu, a] * g[xs, b, nu] * Rsc[xs]
                                   + Gam[x, b, mu, nu] * g[xs, a, b] * Rsc[xs]
                                   - Gam[xs, b, mu, a] * g[x, b, nu] * Rsc[x]
                                   - Gam[xs, b, mu, nu] * g[x, a, b] * Rsc[x]
                                   for b in range(4)))
print("1. B 的 δ 展开：max|B − (∂̃_νR̂ + 修正)| =", np.abs(B - (dR + corr)).max())
print("   |∂̃R̂| =", np.abs(dR).max(), "|修正| =", np.abs(corr).max(), "|B| =", np.abs(B).max())

# ---- 修正项的度规相容化简：∂̃_μ g_{aν} = g_{aλ}Γ^λ_{μν} + g_{νλ}Γ^λ_{μa} ----
corr2 = np.zeros(4)
for mu in range(4):
    xs = step[mu, x]
    for nu in range(4):
        for a in range(4):
            w = ginv[x, mu, a]
            dgm = sum(g[x, a, l] * Gam[x, l, mu, nu] + g[x, nu, l] * Gam[x, l, mu, a]
                      for l in range(4))
            corr2[nu] += w * (dgm * Rsc[xs]
                              + sum(Gam[x, b, mu, a] * g[xs, b, nu] * Rsc[xs]
                                    + Gam[x, b, mu, nu] * g[xs, a, b] * Rsc[xs]
                                    - Gam[xs, b, mu, a] * g[x, b, nu] * Rsc[x]
                                    - Gam[xs, b, mu, nu] * g[x, a, b] * Rsc[x]
                                    for b in range(4)))
print("2. 相容代换后修正：max|修正 − 相容形| =", np.abs(corr - corr2).max())

# ---- ConnRic 的曲率迹展开 ----
ConnRic = np.zeros(4)
K = np.zeros(4)  # ginv·Γ·naiveCurv 四重和
for mu in range(4):
    xs = step[mu, x]
    for a in range(4):
        w = ginv[x, mu, a]
        for nu in range(4):
            ConnRic[nu] += w * (
                sum(Gam[x, b, mu, a] * Rm[xs, b, nu]
                    + Gam[x, b, mu, nu] * Rm[xs, a, b]
                    - Gam[xs, b, mu, a] * Rm[x, b, nu]
                    - Gam[xs, b, mu, nu] * Rm[x, a, b] for b in range(4)))
            K[nu] += w * sum(
                Gam[x, b, mu, a] * naiveCurv(xs, r, b, r, nu)
                + Gam[x, b, mu, nu] * naiveCurv(xs, r, a, r, b)
                - Gam[xs, b, mu, a] * naiveCurv(x, r, b, r, nu)
                - Gam[xs, b, mu, nu] * naiveCurv(x, r, a, r, b)
                for b in range(4) for r in range(4))
print("3. ConnRic 曲率迹展开：max|ConnRic − K| =", np.abs(ConnRic - K).max())
print("   |ConnRic| =", np.abs(ConnRic).max(), "|K| =", np.abs(K).max())
