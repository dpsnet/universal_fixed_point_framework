"""(β) 新阶段最终装配：EinsteinDivergenceFree 显式陈述的数值锁定（beta9）。

beta7 装配：E = Q + T2 + ConnRic − ginv·(Cc3−K2−K3) − ½B（2.8e-14）。
代入 §26.16 contracted_riemann_divergence：ginv·(Cc3−K2−K3) = Q − T1 + T2
  ⟹ Q 与 T2 抵消：
     **E_ν = T1_ν + ConnRic_ν − ½B_ν**                    （抵消形态）
再代入 §26.18 connric_curvature_expand 与 §26.17 metric_term_divergence：
     **E_ν = T1_ν + K_ν − ½(∂̃_νR̂ + 修正_ν)**              （全显式形态）
其中
  T1_ν    = Σ_{sμ} ginv^{sμ}∂̃_μRiĉ_{sν}              （Ricci 方向化散度的 ∂̃ 载体）
  K_ν     = Σ_{μabr} ginv^{μa}[Γ^b_{μa}(x)R̂_{rbrν}(step) + Γ^b_{μν}(x)R̂_{rar b}(step)
            − Γ^b_{μa}(step)R̂_{rbrν}(x) − Γ^b_{μν}(step)R̂_{rar b}(x)]   （K 型四重和）
  修正_ν  = Σ_{μa} ginv^{μa}(∂̃g_{aν}·R̂(step) + 4 项 Γ·g·R̂ 移位修正)

验证目标（seed 43 与 beta8 同构型，x=3）：
  1. E = T1 + ConnRic − ½B                    （抵消形态，vs 直接 E）
  2. E = T1 + K − ½(∂̃R̂ + 修正)                （全显式曲率原语形态）
  3. ∇̃^μRiĉ = T1 + ConnRic                    （方向分裂，定义层校验）
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
Gt = np.array([Rm[y] - 0.5 * g[y] * Rsc[y] for y in range(NPT)])

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
# ---- 直接量：E、∇̃Riĉ、B ----
E = np.zeros(4); divR = np.zeros(4); B = np.zeros(4)
for mu in range(4):
    nG = nabla02(x, mu, Gt)
    nR = nabla02(x, mu, Rm)
    ngR = nabla02(x, mu, gR)
    for a in range(4):
        for nu in range(4):
            E[nu] += ginv[x, mu, a] * nG[a, nu]
            divR[nu] += ginv[x, mu, a] * nR[a, nu]
            B[nu] += ginv[x, mu, a] * ngR[a, nu]

# ---- T1 / ConnRic / K / ∂̃R̂ / 修正 ----
T1 = np.zeros(4); ConnRic = np.zeros(4); K = np.zeros(4)
dR = np.zeros(4); corr = np.zeros(4)
for mu in range(4):
    xs = step[mu, x]
    for nu in range(4):
        dR[nu] += (Rsc[xs] - Rsc[x]) * (1.0 if nu == mu else 0.0)
        for a in range(4):
            w = ginv[x, mu, a]
            T1[nu] += w * (Rm[xs, a, nu] - Rm[x, a, nu])
            ConnRic[nu] += w * sum(
                Gam[x, b, mu, a] * Rm[xs, b, nu] + Gam[x, b, mu, nu] * Rm[xs, a, b]
                - Gam[xs, b, mu, a] * Rm[x, b, nu] - Gam[xs, b, mu, nu] * Rm[x, a, b]
                for b in range(4))
            K[nu] += w * sum(
                Gam[x, b, mu, a] * naiveCurv(xs, r, b, r, nu)
                + Gam[x, b, mu, nu] * naiveCurv(xs, r, a, r, b)
                - Gam[xs, b, mu, a] * naiveCurv(x, r, b, r, nu)
                - Gam[xs, b, mu, nu] * naiveCurv(x, r, a, r, b)
                for b in range(4) for r in range(4))
            corr[nu] += w * ((g[xs, a, nu] - g[x, a, nu]) * Rsc[xs]
                             + sum(Gam[x, b, mu, a] * g[xs, b, nu] * Rsc[xs]
                                   + Gam[x, b, mu, nu] * g[xs, a, b] * Rsc[xs]
                                   - Gam[xs, b, mu, a] * g[x, b, nu] * Rsc[x]
                                   - Gam[xs, b, mu, nu] * g[x, a, b] * Rsc[x]
                                   for b in range(4)))

print("0. 定义层：max|∇̃^μG − (∇̃Riĉ − ½B)| =",
      np.abs(E - (divR - 0.5 * B)).max())
print("1. 抵消形态：max|E − (T1 + ConnRic − ½B)| =",
      np.abs(E - (T1 + ConnRic - 0.5 * B)).max())
print("2. 全显式形态：max|E − (T1 + K − ½(∂̃R̂ + 修正))| =",
      np.abs(E - (T1 + K - 0.5 * (dR + corr))).max())
print("3. 方向分裂：max|∇̃Riĉ − (T1 + ConnRic)| =",
      np.abs(divR - (T1 + ConnRic)).max())
print("   |E| =", np.abs(E).max(), "|T1| =", np.abs(T1).max(),
      "|K| =", np.abs(K).max(), "|修正| =", np.abs(corr).max(),
      "|½∂̃R̂| =", np.abs(0.5 * dR).max())
