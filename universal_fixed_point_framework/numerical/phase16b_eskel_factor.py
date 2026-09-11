"""符号因式分解: 恰单零指标 12 维相容子族内 E_skel 的多项式结构。

Γ^i_{0j}=C_ij, Γ^i_{j0}=D_ij, Γ^0_{ij}=D_ji (i,j>=1), 其余=0。
相容约束: C 反对称, F=D^T (自动)。
E_ν = Σ_{μa} ginv^{μa} Σ_l (−Γ^l_{μa} G_{lν} − Γ^l_{μν} G_{al}),
G = Ric − ½ g R̂, Ric_{σν} = Σ_r R^r_{σrν}, R^r_{sμν} = Σ_l(Γ^r_{μl}Γ^l_{νs} − Γ^r_{νl}Γ^l_{μs})。
η = diag(-1,1,1,1)。
"""
import sympy as sp

# 12 个符号: C_ij (i<j, 3个), D_ij (9个)
C = {}
for i in range(1, 4):
    C[(i, i)] = sp.Integer(0)
for a, (i, j) in enumerate([(1, 2), (1, 3), (2, 3)]):
    C[(i, j)] = sp.Symbol(f'C{i}{j}')
    C[(j, i)] = -C[(i, j)]
D = {}
for i in range(1, 4):
    for j in range(1, 4):
        D[(i, j)] = sp.Symbol(f'D{i}{j}')

def Gam(r, m, n):
    if r >= 1 and m == 0 and n >= 1:
        return C[(r, n)]
    if r >= 1 and n == 0 and m >= 1:
        return D[(r, m)]
    if r == 0 and m >= 1 and n >= 1:
        return D[(n, m)]
    return sp.Integer(0)

eta = sp.diag(-1, 1, 1, 1)
etainv = eta

# Riemann
R = {}
for r in range(4):
    for s in range(4):
        for mu in range(4):
            for nu in range(4):
                R[(r, s, mu, nu)] = sp.expand(
                    sum(Gam(r, mu, l) * Gam(l, nu, s) - Gam(r, nu, l) * Gam(l, mu, s)
                        for l in range(4)))

# Ricci
Ric = {}
for s in range(4):
    for nu in range(4):
        Ric[(s, nu)] = sp.expand(sum(R[(r, s, r, nu)] for r in range(4)))

Rsc = sp.expand(sum(etainv[s, nu] * Ric[(s, nu)] for s in range(4) for nu in range(4)))

G = {}
for mu in range(4):
    for nu in range(4):
        G[(mu, nu)] = sp.expand(Ric[(mu, nu)] - sp.Rational(1, 2) * eta[mu, nu] * Rsc)

print("Rsc =", Rsc)
print("Ric[0,0] =", Ric[(0, 0)])

# E_nu
E = []
for nu in range(4):
    e = sp.Integer(0)
    for mu in range(4):
        for a in range(4):
            conn = sp.expand(sum(-Gam(l, mu, a) * G[(l, nu)] - Gam(l, mu, nu) * G[(a, l)]
                                 for l in range(4)))
            e += etainv[mu, a] * conn
    E.append(sp.expand(e))

for nu in range(4):
    print(f"\nE_{nu} =", E[nu])
    f = sp.factor(E[nu])
    print(f"  factor:", f)

# 用 torsion 变量重写: T^i_{0j} = C_ij - D_ij, T^0_{ij} = D_ji - D_ij
print("\n--- 换元为挠率 ---")
T0 = {}  # T^i_{0j} = C_ij - D_ij
for i in range(1, 4):
    for j in range(1, 4):
        T0[(i, j)] = sp.Symbol(f'T{i}{j}')
T1 = {}  # T^0_{ij} = D_ji - D_ij
for i in range(1, 4):
    for j in range(1, 4):
        T1[(i, j)] = sp.Symbol(f'U{i}{j}')

# 哑元代换: C = T0 + D 的对称部分处理——直接从 (C,D) 解出用 T 表示
# T^i_{0j} = C_ij - D_ij (9 方程), T^0_{ij} = D_ji - D_ij (9, 但反对称只有 3 独立)
# 独立: sym(T0) = -sym(D) (3), antisym(T0) = C - antisym(D) (3), T1 = -2 antisym(D) (3)
subs = {}
for i in range(1, 4):
    for j in range(1, 4):
        # 解: antisym(D)_ij = -U_ij/2, sym(D)_ij = -sym(T)_ij
        aD = -T1[(i, j)] / 2 if i != j else sp.Integer(0)
        sD = -(T0[(i, j)] + T0[(j, i)]) / 2
        Dij = sp.expand(aD + sD)
        subs[D[(i, j)]] = Dij
        subs[C[(i, j)]] = sp.expand(T0[(i, j)] + Dij)  # C = T0 + D

for nu in range(4):
    eT = sp.expand(E[nu].subs(subs))
    print(f"\nE_{nu}(T) =", eT)
