"""E 骨架 Einstein 散度在全相容空间上的数值结构分析 (修正版)。

对象: 常值 Minkowski 度规 eta=diag(-1,1,1,1) 上的常值相容联络
(lowered Γ_{abc} 对 (a,c) 反对称, 48 实参数), 升指标得 Γ^a_{bc}。

Einstein 散度的骨架 (无 ∂) 形态, 4 个分量:
  D_ν = Σ_{μ,a} η^{μa} ∇̃_μ G_{aν},
  ∇̃_μ G_{aν} = Σ_l ( -Γ^l_{μa} G_{lν} - Γ^l_{μν} G_{al} ),
  G_{μν} = Ric_{μν} - (1/2) η_{μν} R,  黎曼量由 Γ 按常度规公式计算。

检验:
1. 全空间随机采样: D 的 4 个分量是否恒零?
2. D 对联络的齐次次数 (期望纯 3 次)。
3. omega 型联络 (12 维恰单零指标族, D 反对称) 上 D 是否恒为零。
4. omega 点附近沿对称 S 方向的响应展开 (常数/线性/二次/三次项大小)。
"""
import numpy as np

rng = np.random.default_rng(20260911)
eta = np.diag([-1.0, 1.0, 1.0, 1.0])


def raise_first(G):
    return np.einsum('ad,dbc->abc', eta, G)  # Γ^a_{bc} = η^{ad} Γ_{dbc}


def divergence(G_lo):
    """lowered Γ[a,b,c] (antisym in a,c) -> D_ν (4 分量 Einstein 散度骨架)"""
    G = raise_first(G_lo)
    R = np.einsum('rml,lns->rsmn', G, G) - np.einsum('rnl,lms->rsmn', G, G)
    Ric = np.einsum('rsrn->sn', R)                      # Ric_{s n}
    Rsc = np.einsum('sn,sn->', Ric, eta)                # η^{sn} Ric_{sn}
    Eins = Ric - 0.5 * eta * Rsc                        # G_{sn}
    # ∇̃_μ G_{aν}: conn[mu,a,nu]
    conn = np.einsum('lma,lv->mav', -G, Eins) \
        + np.einsum('lmv,al->mav', -G, Eins)
    return np.einsum('ma,mav->v', eta, conn)            # D_ν = η^{μa} ∇̃_μ G_{aν}


def random_lowered():
    G = np.zeros((4, 4, 4))
    for a in range(4):
        for c in range(a + 1, 4):
            for b in range(4):
                G[a, b, c] = rng.standard_normal()
                G[c, b, a] = -G[a, b, c]
    return G


def omega_lowered(C, D):
    """12 维恰单零指标族 (上指标): Γ^i_{0j}=C_ij, Γ^i_{j0}=D_ij, Γ^0_{ij}=D_ji,
    C,D 反对称; 转 lowered: Γ_{i0j}=C_ij, Γ_{ij0}=D_ij, Γ_{0ij}=-D_ji。"""
    G = np.zeros((4, 4, 4))
    for i in range(1, 4):
        for j in range(1, 4):
            G[i, 0, j] = C[i, j]
            G[i, j, 0] = D[i, j]
            G[0, i, j] = -D[j, i]
    return G


print("=== 检验 1: 全空间随机采样下 D 的分量结构 ===")
n = 2000
maxv = np.zeros(4)
for _ in range(n):
    Dv = divergence(random_lowered())
    maxv = np.maximum(maxv, np.abs(Dv))
for v in range(4):
    print(f"  max|D_{v}| = {maxv[v]:.4f}   {'<- 恒零' if maxv[v] < 1e-9 else ''}")

print("\n=== 检验 2: D 对联络的齐次次数 ===")
G0 = random_lowered()
Ts = np.array([1.0, 2.0, 3.0, 4.0])
vals = np.array([divergence(t * G0) for t in Ts])
V = np.stack([Ts, Ts**2, Ts**3], axis=1)
coef, *_ = np.linalg.lstsq(V, vals, rcond=None)
for d in range(3):
    print(f"  |D 的 {d+1} 次项| max = {np.abs(coef[d]).max():.3e}")

print("\n=== 检验 3: omega 型联络上 D 是否恒为零 ===")
bad = 0
maxbad = 0.0
for _ in range(2000):
    C = np.zeros((4, 4))
    D = np.zeros((4, 4))
    for (i, j) in [(1, 2), (1, 3), (2, 3)]:
        C[i, j] = rng.standard_normal()
        C[j, i] = -C[i, j]
        D[i, j] = rng.standard_normal()
        D[j, i] = -D[i, j]
    Dv = divergence(omega_lowered(C, D))
    m = np.abs(Dv).max()
    maxbad = max(maxbad, m)
    if m > 1e-9:
        bad += 1
print(f"  |D|>1e-9 样本: {bad}/2000,  max|D| = {maxbad:.3e}")

print("\n=== 检验 4: omega 点沿对称 S 扰动的响应展开 ===")
C = np.zeros((4, 4))
D = np.zeros((4, 4))
for (i, j) in [(1, 2), (1, 3), (2, 3)]:
    C[i, j] = rng.standard_normal()
    C[j, i] = -C[i, j]
    D[i, j] = rng.standard_normal()
    D[j, i] = -D[i, j]
Gom = omega_lowered(C, D)
S = np.zeros((4, 4))
for i in range(1, 4):
    for j in range(1, 4):
        S[i, j] = rng.standard_normal()
S = 0.5 * (S + S.T)
Gt = np.zeros((4, 4, 4))
for i in range(1, 4):
    for j in range(1, 4):
        Gt[i, j, 0] = S[i, j]
        Gt[0, i, j] = -S[j, i]
vals = np.array([divergence(Gom + t * Gt) for t in Ts])
V1 = np.stack([np.ones_like(Ts), Ts, Ts**2, Ts**3], axis=1)
coef, *_ = np.linalg.lstsq(V1, vals, rcond=None)
names = ['c0 (omega 点处)', 'c1 (线性)', 'c2 (二次)', 'c3 (三次)']
for k, nm in enumerate(names):
    print(f"  |{nm}| max = {np.abs(coef[k]).max():.4f}")
