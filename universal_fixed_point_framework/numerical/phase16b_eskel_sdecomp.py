"""E_0 结构分析: 对 D 对称部分 S 的次数分解 + 反对称 D 时是否恒零。
E_0 = -C12*D12*D33 + ... (见 phase16b_eskel_factor.py 输出)。
换元: D_ij = A_ij + S_ij, A 反对称, S 对称, 展开看 E_0 对 S 的次数。
"""
import sympy as sp

C = {}
for i in range(1, 4):
    C[(i, i)] = sp.Integer(0)
for (i, j) in [(1, 2), (1, 3), (2, 3)]:
    C[(i, j)] = sp.Symbol(f'C{i}{j}')
    C[(j, i)] = -C[(i, j)]

# D 用 A(反对称) + S(对称) 参数化
A = {}
S = {}
for i in range(1, 4):
    A[(i, i)] = sp.Integer(0)
    S[(i, i)] = sp.Symbol(f'S{i}{i}')
for (i, j) in [(1, 2), (1, 3), (2, 3)]:
    A[(i, j)] = sp.Symbol(f'A{i}{j}')
    A[(j, i)] = -A[(i, j)]
    S[(i, j)] = sp.Symbol(f'S{i}{j}')
    S[(j, i)] = S[(i, j)]

D = {}
for i in range(1, 4):
    for j in range(1, 4):
        D[(i, j)] = A[(i, j)] + S[(i, j)]

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
G = {(mu, nu): sp.expand(Ric[(mu, nu)] - sp.Rational(1, 2) * eta[mu, nu] * Rsc)
     for mu in range(4) for nu in range(4)}

E0 = sp.Integer(0)
for mu in range(4):
    for a in range(4):
        conn = sp.expand(sum(-Gam(l, mu, a) * G[(l, 0)] - Gam(l, mu, 0) * G[(a, l)]
                             for l in range(4)))
        E0 += eta[mu, a] * conn
E0 = sp.expand(E0)

# 检验 1: D 反对称 (S=0) 时 E_0 = 0?
E0_S0 = sp.expand(E0.subs({S[k]: sp.Integer(0) for k in S}))
print("E_0|_{S=0} =", E0_S0)

# 检验 2: 对 S 的次数分解
def deg_in(poly, syms, d):
    """提取 poly 中 syms 总次数恰好为 d 的部分"""
    poly = sp.Poly(poly, list(syms))
    out = 0
    for monom, coeff in poly.terms():
        if sum(monom) == d:
            out += coeff * sp.prod(s**m for s, m in zip(syms, monom))
    return sp.expand(out)

S_vars = sorted(set(S.values()), key=str)  # 去重: S[(1,2)] 与 S[(2,1)] 同一 symbol
for d in range(4):
    part = deg_in(E0, S_vars, d)
    print(f"E_0 中 S 的次数 {d} 部分: 项数={len(sp.Poly(part, S_vars).terms()) if part != 0 else 0}")
    if d >= 1 and part != 0:
        sp.pprint(sp.factor(part))
        print()

# 检验 3: S 的线性部分系数 (应为 C,A 的二次型)
lin = deg_in(E0, S_vars, 1)
print("\nE_0 对 S 线性部分 =", sp.factor(lin))

# 检验 4: 二次、三次部分是否恒零
q = deg_in(E0, S_vars, 2)
c = deg_in(E0, S_vars, 3)
print("二次部分恒零?", q == 0)
print("三次部分恒零?", c == 0)
