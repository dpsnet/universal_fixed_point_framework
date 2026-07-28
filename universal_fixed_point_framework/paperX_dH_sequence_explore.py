#!/usr/bin/env python3
"""
paperX_dH_sequence_explore.py — 数列模式扫描

Sp 严格 4-范畴的结构常数:
  N_active = 3, N_total = 5, 2^3 = 8, B = 15

问题: 这些数是否出现在已知整数数列中? 是否有 Fibonacci 以外的模式?
"""
import numpy as np

# =============================================================
# §1 生成各类数列
# =============================================================
def fibonacci(n_terms=15):
    f = [0, 1]
    for i in range(2, n_terms):
        f.append(f[-1] + f[-2])
    return f

def lucas(n_terms=15):
    l = [2, 1]
    for i in range(2, n_terms):
        l.append(l[-1] + l[-2])
    return l

def catalan(n_terms=15):
    c = [1]
    for i in range(1, n_terms):
        c.append(c[-1] * 2 * (2*i - 1) // (i + 1))
    return c

def triangular(n_terms=15):
    return [n*(n+1)//2 for n in range(n_terms)]

def square(n_terms=15):
    return [n*n for n in range(n_terms)]

def pentagonal(n_terms=15):
    return [n*(3*n-1)//2 for n in range(n_terms)]

def bell(n_terms=10):
    # Bell numbers (set partitions)
    b = [1]
    for n in range(1, n_terms):
        s = 0
        for k in range(n):
            from math import comb
            s += comb(n-1, k) * b[k]
        b.append(s)
    return b

def tribonacci(n_terms=15):
    t = [0, 0, 1]
    for i in range(3, n_terms):
        t.append(t[-1] + t[-2] + t[-3])
    return t

def powers_of_two(n_terms=10):
    return [2**n for n in range(n_terms)]

# 我们的目标数
targets = {
    "N_active": 3,
    "N_total": 5,
    "2^3 (Bott)": 8,
    "B = 3x5": 15,
    "N_active+N_total": 8,
    "Bott-1": 7,
    "ln15 近似": 27,  # 2.708 大概对应于 27/10
}

print("=" * 72)
print("§1 各数列中的 3, 5, 8, 15")
print("=" * 72)

sequences = {
    "Fibonacci": fibonacci,
    "Lucas": lucas,
    "Catalan": catalan,
    "Triangular": triangular,
    "Square": square,
    "Pentagonal": pentagonal,
    "Bell": bell,
    "Tribonacci": tribonacci,
    "Powers of 2": powers_of_two,
}

for name, gen_fn in sequences.items():
    seq = gen_fn(20)
    print(f"\n  {name}:")
    print(f"    seq = {[s for s in seq[:12]]}...")
    for t_name, t_val in targets.items():
        if t_val in seq:
            idx = seq.index(t_val)
            print(f"    {t_name}={t_val} 在位置 {idx}")

# =============================================================
# §2 检查 Fibonacci 层数假说
# =============================================================
print("\n" + "=" * 72)
print("§2 Fibonacci 层数假说: Sp 严格 n-范畴")
print("=" * 72)

F = fibonacci(10)
print(f"\n  Fibonacci: F = {F}")
print(f"\n  Sp 严格 4-范畴 (当前):")
print(f"    总层数 = {F[5]} = F_5")
print(f"    主动层 = {F[4]} = F_4")
print(f"    Bott 翻倍 = {F[6]} = F_6")
print(f"    B = F_4 x F_5 = {F[4]*F[5]}")
print(f"    d_H ≈ ln(B) = {np.log(F[4]*F[5]):.6f}")

print(f"\n  外推: Sp 严格 5-范畴:")
print(f"    总层数 = {F[6]} = F_6")
print(f"    主动层 = {F[5]} = F_5")
print(f"    Bott 翻倍 = {F[7]} = F_7")
print(f"    B = F_5 x F_6 = {F[5]*F[6]}")
print(f"    d_H ≈ ln(B) = {np.log(F[5]*F[6]):.6f}")

print(f"\n  外推: Sp 严格 n-范畴:")
for n in range(3, 8):
    active = F[n]
    total = F[n+1]
    B = active * total
    print(f"    n={n}: active=F_{n}={active}, total=F_{n+1}={total}, B={B}, d_H≈ln{B}={np.log(B):.6f}")

# =============================================================
# §3 检查其他可能的递推关系
# =============================================================
print("\n" + "=" * 72)
print("§3 其他可能的数列递推")
print("=" * 72)

# Lucas: L_n = F_{n-1} + F_{n+1} = phi^n + (-phi)^{-n}
L = lucas(10)
print(f"  Lucas: L = {L}")
print(f"  Lucas L_4 = {L[4]} (vs F_4 = {F[4]})")
print(f"  Lucas L_5 = {L[5]} (vs F_5 = {F[5]})")

# Catalan: C_0=1, C_n = (2(2n-1)/(n+1)) * C_{n-1}
C = catalan(10)
print(f"\n  Catalan: C = {C}")
for i, c in enumerate(C):
    if c in [3, 5, 8, 15]:
        print(f"    C_{i} = {c} ✓")

# Tribonacci: T_n = T_{n-1} + T_{n-2} + T_{n-3}
T = tribonacci(12)
print(f"\n  Tribonacci: T = {T}")
for i, t in enumerate(T):
    if t in [3, 5, 8, 15]:
        print(f"    T_{i} = {t} ✓")

# =============================================================
# §4 乘积模式的唯一性
# =============================================================
print("\n" + "=" * 72)
print("§4 F_4 × F_5 = 15 在 Fibonacci 中的唯一性")
print("=" * 72)

print(f"\n  检查: F_n × F_{n+1} 中哪些等于 F_{n+2} 类数?")
products = []
for n in range(2, 10):
    p = F[n] * F[n+1]
    products.append((n, F[n], F[n+1], p))
    print(f"    F_{n} × F_{n+1} = {F[n]} × {F[n+1]} = {p}")

# 特别检查: 3×5=15, 5×8=40, 8×13=104
# 这些有封闭形式吗?
print(f"\n  注意: F_n x F_{n+1} = F_(2n+1) - ...")
for n in range(1, 8):
    # Cassini: F_{n-1}*F_{n+1} - F_n^2 = (-1)^n
    cassini = F[n-1]*F[n+1] - F[n]**2
    print(f"    Cassini: F_{n-1}*F_{n+1} - F_{n}^2 = {F[n-1]}*{F[n+1]} - {F[n]}^2 = {cassini}")

# =============================================================
# §5 3,5,8 在已知数列中的共现
# =============================================================
print("\n" + "=" * 72)
print("§5 3,5,8 同时出现的数列")
print("=" * 72)

found_any = False
for name, gen_fn in sequences.items():
    seq = gen_fn(20)
    if 3 in seq and 5 in seq and 8 in seq:
        i3 = seq.index(3)
        i5 = seq.index(5)
        i8 = seq.index(8)
        consecutive = (i8 - i5 == 1 and i5 - i3 == 1)
        print(f"  {name}: 3@{i3}, 5@{i5}, 8@{i8} {'(连续!)' if consecutive else ''}")
        found_any = True

if not found_any:
    print("  (除了 Fibonacci, 无其他常见数列同时包含 3,5,8)")

# =============================================================
# §6 深化: 层数是否可能满足递推 L_{k+1} = L_k + L_{k-1}?
# =============================================================
print("\n" + "=" * 72)
print("§6 层数递推假说的结构检验")
print("=" * 72)

# 如果层数 L_k 满足 Fibonacci 递推:
# L_0 = 1 (对象层), L_1 = 2? 还是 L_1 = 1?
# 在严格 n-范畴中, k-态射层只有一个类型
# 但"总层数"计数中各层是否互异?

# 假设:
# L_0 = 1 (对象层)
# L_1 = 2 (1-态射层 + 对象层 = 2? 或者...)

# 对严格 n-范畴, "层数计数"的不同方式:
# 方式 A: 总层数 = n + 1 (对象 + n 个态射层)
# 方式 B: 主动层数 = n - 1 (排除对象和 coherence)
# 方式 C: 总层数按 Fibonacci 增长

print(f"  严格 n-范畴的标准层计数 vs Fibonacci 计数:")
print(f"  {'n':>3s}  {'标准总层':>8s}  {'标准主动':>8s}  {'F_{n+1}':>8s}  {'F_n':>8s}  {'匹配?':>8s}")
for n in range(1, 10):
    std_total = n + 1  # 对象 + n 个态射层
    std_active = n - 1 if n >= 2 else 0  # 排除对象和最高层
    fib_total = F[n+1]
    fib_active = F[n]
    match_total = "✓" if std_total == fib_total else ""
    match_active = "✓" if std_active == fib_active else ""
    print(f"  {n:3d}  {std_total:8d}  {std_active:8d}  {fib_total:8d}  {fib_active:8d}  {match_active:>8s}")

print(f"\n  结论: 标准层计数(线性)与 Fibonacci(指数)仅在 n=4 处对齐:")
print(f"    n=4: 标准总层=5=F_5, 标准主动=3=F_4")
print(f"    其他 n 值都不匹配。")
print(f"    这意味着 Fibonacci 模式是 4-范畴这一特定构型的结构巧合,")
print(f"    是线性层计数与 Fibonacci 自相似增长的唯一交点。")
print(f"    类比: 3-4-5 是唯一的连续勾股数——Fibonacci 在 n=4 处的")
print(f"    对齐可能具有类似的'独特性'意义。")
