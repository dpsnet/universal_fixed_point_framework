"""散度 4 分量 D_nu 在 12 维恰单零指标族内的符号结构 (修正版)。

族: Γ^i_{0j}=C_ij, Γ^i_{j0}=D_ij, Γ^0_{ij}=D_ji, η=Minkowski。
D_nu = Σ_{μ,a} η^{μa} ∇̃_μ G_{aν},  ∇̃_μ G_{aν} = Σ_l(-Γ^l_{μa}G_{lν} - Γ^l_{μν}G_{al})。

对 D = A + S (A 反对称, S 对称) 分解每个 D_nu:
  - S=0 (omega 型) 时是否恒零;
  - 对 S 的次数 (0..3 次部分哪些非零)。
"""
import sympy as sp

C = {}
for i in range(1, 4):
    C[(i, i)] = sp.Integer(0)
for (i, j) in [(1, 2), (1, 3), (2, 3)]:
    C[(i, j)] = sp.Symbol(f'C{i}{j}')
    C[(j, i)] = -C[(i, j)]

A, S = {}, {}
for i in range(1, 4):
    A[(i, i)] = sp.Integer(0)
    S[(i, i)] = sp.Symbol(f'S{i}{i}')
for (i, j) in [(1, 2), (1, 3), (2, 3)]:
    A[(i, j)] = sp.Symbol(f'A{i}{j}')
    A[(j, i)] = -A[(i, j)]
    S[(i, j)] = sp.Symbol(f'S{i}{j}')
    S[(j, i)] = S[(i, j)]

D = {(i, j): A[(i, j)] + S[(i, j)] for i in range(1, 4) for j in range(1, 4)}


def Gam(r, m, n):
    if r >= 1 and m == 0 and n >= 1:
        return C[(r, n)]
    if r >= 1 and n == 0 and m >= 1:
        return D[(r, m)]
    if r == 0 and m >= 1 and n >= 1:
        return D[(n, m)]
    return sp.Integer(0)


eta = sp.diag(-1, 1, 1, 1)

R = {}
for r in range(4):
    for s in range(4):
        for mu in range(4):
            for nu in range(4):
                R[(r, s, mu, nu)] = sp.expand(
                    sum(Gam(r, mu, l) * Gam(l, nu, s) - Gam(r, nu, l) * Gam(l, mu, s)
                        for l in range(4)))
Ric = {(s, nu): sp.expand(sum(R[(r, s, r, nu)] for r in range(4)))
       for s in range(4) for nu in range(4)}
Rsc = sp.expand(sum(eta[s, nu] * Ric[(s, nu)] for s in range(4) for nu in range(4)))
Eins = {(mu, nu): sp.expand(Ric[(mu, nu)] - sp.Rational(1, 2) * eta[mu, nu] * Rsc)
        for mu in range(4) for nu in range(4)}


def div(nu):
    out = sp.Integer(0)
    for mu in range(4):
        for a in range(4):
            conn = sp.expand(sum(-Gam(l, mu, a) * Eins[(l, nu)]
                                 - Gam(l, mu, nu) * Eins[(a, l)] for l in range(4)))
            out += eta[mu, a] * conn
    return sp.expand(out)


S_vars = sorted(set(S.values()), key=str)


def deg_in(poly, d):
    if poly == 0:
        return sp.Integer(0)
    p = sp.Poly(poly, S_vars)
    out = sp.Integer(0)
    for monom, coeff in p.terms():
        if sum(monom) == d:
            out += coeff * sp.prod(s**m for s, m in zip(S_vars, monom))
    return sp.expand(out)


S0 = {s: sp.Integer(0) for s in S_vars}
for nu in range(4):
    Dn = div(nu)
    n_terms = len(sp.Add.make_args(Dn))
    at_omega = sp.simplify(Dn.subs(S0)) == 0
    degs = []
    for d in range(4):
        part = deg_in(Dn, d)
        degs.append(0 if part == 0 else len(sp.Poly(part, S_vars).terms()))
    print(f"D_{nu}: 总项数={n_terms:3d}  S=0 时恒零: {at_omega}  "
          f"S 次数分布(0..3 次项数)={degs}")
