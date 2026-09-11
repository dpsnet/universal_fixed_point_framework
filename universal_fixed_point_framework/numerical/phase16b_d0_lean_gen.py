"""D₀ = L(C,A)·S + Cub(S) 的 Lean 表达式生成器。

标准原子基底（Lean 端 simp 重写后的剩余原子）：
  C 2 1, C 3 1, C 3 2  (C 反对称, i<j 已重写)
  A 2 1, A 3 1, A 3 2  (A 反对称)
  S 1 1, S 2 2, S 3 3, S 1 2, S 1 3, S 2 3  (S 对称)

输出:
1. 校验: D₀(标准原子) == 线性部分 + 三次部分;
2. Lean 定理 RHS 的 lin/cub 表达式文本(写入 stdout, 供粘贴进 .lean 文件)。
"""
import sympy as sp

c21, c31, c32 = sp.symbols('c21 c31 c32')
a21, a31, a32 = sp.symbols('a21 a31 a32')
s11, s22, s33, s12, s13, s23 = sp.symbols('s11 s22 s33 s12 s13 s23')

C = {(1,2): -c21, (2,1): c21, (1,3): -c31, (3,1): c31,
     (2,3): -c32, (3,2): c32}
A = {(1,2): -a21, (2,1): a21, (1,3): -a31, (3,1): a31,
     (2,3): -a32, (3,2): a32}
S = {(1,1): s11, (2,2): s22, (3,3): s33,
     (1,2): s12, (2,1): s12, (1,3): s13, (3,1): s13, (2,3): s23, (3,2): s23}
for i in (1, 2, 3):
    C[(i, i)] = sp.Integer(0)
    A[(i, i)] = sp.Integer(0)
D = {(i, j): A[(i, j)] + S[(i, j)] for i in (1, 2, 3) for j in (1, 2, 3)}

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
D0 = sp.Integer(0)
for mu in range(4):
    for a in range(4):
        conn = sp.expand(sum(-Gam(l, mu, a) * Eins[(l, 0)]
                             - Gam(l, mu, 0) * Eins[(a, l)] for l in range(4)))
        D0 += eta[mu, a] * conn
D0 = sp.expand(D0)

S_vars = [s11, s22, s33, s12, s13, s23]

def deg_part(poly, d):
    if poly == 0:
        return sp.Integer(0)
    p = sp.Poly(poly, S_vars)
    out = sp.Integer(0)
    for monom, coeff in p.terms():
        if sum(monom) == d:
            out += coeff * sp.prod(v**m for v, m in zip(S_vars, monom))
    return sp.expand(out)

lin = deg_part(D0, 1)
cub = deg_part(D0, 3)
print("D₀ 项数:", len(sp.Add.make_args(D0)))
print("校验 D₀ == lin + cub :", sp.expand(D0 - lin - cub) == 0)
print("lin 项数:", len(sp.Add.make_args(lin)), " cub 项数:", len(sp.Add.make_args(cub)))
print("deg0 为零?", deg_part(D0, 0) == 0, " deg2 为零?", deg_part(D0, 2) == 0)

ATOM = {c21: '(C 2 1)', c31: '(C 3 1)', c32: '(C 3 2)',
        a21: '(A 2 1)', a31: '(A 3 1)', a32: '(A 3 2)',
        s11: 'S 1 1', s22: 'S 2 2', s33: 'S 3 3',
        s12: 'S 1 2', s13: 'S 1 3', s23: 'S 2 3'}

def emit_monom(coeff, powers):
    """powers: list of (var, exp). 返回单项式体(不含符号)。"""
    factors = []
    for v, e in powers:
        if e == 1:
            factors.append(ATOM[v])
        else:
            factors.append(f"{ATOM[v]}^{e}")
    body = ' * '.join(factors) if factors else '1'
    if coeff == 1:
        return body
    if coeff == -1:
        return f"(-{body})"
    return f"{coeff} * {body}"

def emit_poly(poly):
    """把 poly 写成 Lean 表达式: '(t1 + t2 - t3)' 风格。"""
    if poly == 0:
        return "0"
    p = sp.Poly(poly, list(ATOM.keys()))
    pos, neg = [], []
    for monom, coeff in p.terms():
        powers = [(v, m) for v, m in zip(list(ATOM.keys()), monom) if m > 0]
        body = emit_monom(abs(int(coeff)), powers)
        (pos if coeff > 0 else neg).append(body)
    out = ' + '.join(pos) if pos else '0'
    for b in neg:
        out += f" - {b.lstrip('(').rstrip(')')}" if b.startswith('(') and b.endswith(')') and '^' not in b else f" - {b}"
    return out

print("\n----- LIN (Lean) -----")
print(emit_poly(lin))
print("\n----- CUB (Lean) -----")
print(emit_poly(cub))
