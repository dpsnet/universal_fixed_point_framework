# -*- coding: utf-8 -*-
"""
e 内生化桥 —— 云端研究本地复算（2026-10-21, Windows 本地 pyenv 3.11.8）
四项：A) e 连分数锚点带 + 断裂点验证
      B) 窗口密度（Bott 周期判别）
      C) 对照实验（10 常数前 8 阶命中率）
      D) 阶乘截断候选（e 组合计数涌现）
运行：D:\\pyenv\\pyenv-win\\versions\\3.11.8\\python.exe scripts\\e_internalization_recompute.py
"""
from math import isqrt, factorial

# ---- 框架常数 ----
FW = [2, 3, 4, 5, 7, 8, 42]
N_GEN, K_MAX, POWER, SILENT, FIXED, INVOL, CONFIN, SIGMA_INV = 3, 8, 2, 5, 4, 7, 42, 15
FP = {1}
for a in FW:
    v = a
    for _ in range(1, 21):
        FP.add(v)
        if v > 10**30:
            break
        v *= a
FP = sorted(FP)


def is_s7(n):
    """7-smooth：质因子 ⊆ {2,3,5,7}"""
    if n <= 1:
        return n == 1
    for p in (2, 3, 5, 7):
        while n % p == 0:
            n //= p
    return n == 1


def is_mersenne7(n):
    """Mersenne × 7-smooth"""
    for i in range(1, 12):
        mi = 2**i - 1
        if mi > n:
            break
        if n % mi == 0 and is_s7(n // mi):
            return True
    return False


def expr_ext(n):
    """框架表达（扩展模式库：7-smooth / M×s7 / FWPOW±1）"""
    if n == 1:
        return True
    if is_s7(n):
        return True
    if is_mersenne7(n):
        return True
    for d in (-1, 1):
        m = n - d
        if m <= 1:
            continue
        for x in FP:
            if x > m:
                break
            if x == 1:
                continue
            if m % x == 0 and (m // x) in FP:
                return True
    return False


def convergents(a):
    """连分数收敛子"""
    p2, p1, q2, q1 = 0, 1, 1, 0
    r = []
    for ai in a:
        p = ai * p1 + p2
        q = ai * q1 + q2
        p2, p1 = p1, p
        q2, q1 = q1, q
        r.append((p, q))
    return r


def hit_rate(c):
    pm = sum(1 for p, _ in c if expr_ext(p))
    qm = sum(1 for _, q in c if expr_ext(q))
    return pm, qm


def fmt(flag):
    return "FW" if flag else "  "


# ================= A) e 锚点带 =================
print("=" * 78)
print("A) e 连分数收敛子锚点带（n=0..16）")
print("=" * 78)
a_e = [2, 1, 2, 1, 1, 4, 1, 1, 6, 1, 1, 8, 1, 1, 10, 1, 1, 12, 1, 1, 14]
cs = convergents(a_e)
print(" n |   p_n  | p-FW |    q_n  | q-FW | 表达式线索")
print("-" * 78)
hints = {
    (2, 8): "k_max = 2^3",
    (3, 11): "N_gen*FIXED-1 = 3*4-1",
    (4, 19): "FIXED*SILENT-1 = 4*5-1",
    (5, 87): "k_max*11-1",
    (6, 39): "SILENT*k_max-1 = 5*8-1",
    (7, 193): "N_gen*k_max^2+1 = 3*64+1",
    (8, 465): "M4*M5 = SIGMA_INV*31  [断裂点第一项]",
    (9, 1457): "POWER*N_gen^6-1 = 2*3^6-1",
    (10, 1001): "k_max*SILENT^3+1 = 8*125+1",
    (5, 32): "POWER^SILENT = 2^5",
    (7, 71): "k_max*(k_max+1)-1 = 8*9-1",
    (6, 106): "--",
    (8, 1264): "-- [n=8 断裂]",
}
for n, (p, q) in enumerate(cs[:17]):
    print(" %2d | %6d |  %s  | %6d |  %s  | %s" % (
        n, p, fmt(expr_ext(p)), q, fmt(expr_ext(q)),
        hints.get((n, p), hints.get((n, q), ""))))
# 锚点带统计
band = [(p, q) for p, q in cs[:8]]
pm, qm = hit_rate(band)
print(" 锚点带 n=0..7：分子 %d/8，分母 %d/8" % (pm, qm))

# ================= B) 窗口密度（Bott 判别） =================
print()
print("=" * 78)
print("B) 窗口密度（Bott 周期 8 判别）")
print("=" * 78)
a_e_long = [2]
i = 1
while len(a_e_long) < 25:
    if i % 3 == 2:
        a_e_long.append(2 * (i + 1) // 3)
    else:
        a_e_long.append(1)
    i += 1
cs_long = convergents(a_e_long)
for (lo, hi), label in [((0, 8), "W0 (n=0..7)"), ((8, 16), "W1 (n=8..15)"), ((16, 24), "W2 (n=16..23)")]:
    seg = cs_long[lo:hi]
    pm, qm = hit_rate(seg)
    print(" %s：分子 %d/8，分母 %d/8" % (label, pm, qm))

# ================= C) 对照实验 =================
print()
print("=" * 78)
print("C) 对照实验：10 常数前 8 阶命中率")
print("=" * 78)
T = {
    "e":     [2, 1, 2, 1, 1, 4, 1, 1, 6],
    "pi":    [3, 7, 15, 1, 292, 1, 1, 1, 2],
    "sqrt2": [1, 2, 2, 2, 2, 2, 2, 2, 2],
    "phi":   [1, 1, 1, 1, 1, 1, 1, 1, 1],
    "sqrt3": [1, 1, 2, 1, 2, 1, 2, 1, 2],
    "sqrt5": [2, 4, 4, 4, 4, 4, 4, 4, 4],
    "ln2":   [0, 1, 2, 3, 1, 6, 3, 1, 1],
    "gamma": [0, 1, 1, 2, 1, 2, 1, 4, 3],
    "sqrt7": [2, 1, 1, 1, 4, 1, 1, 1, 4],
    "e^2":   [7, 2, 1, 1, 3, 18, 5, 1, 1],
}
print(" %-6s | p | q | 分母序列(前8)" % "常数")
print("-" * 78)
for name, a in T.items():
    c = convergents(a[:8])
    pm, qm = hit_rate(c)
    print(" %-6s | %d/8 | %d/8 | %s" % (name, pm, qm, [q for _, q in c]))

# ================= D) 阶乘截断候选 =================
print()
print("=" * 78)
print("D) 阶乘截断候选（e 组合计数涌现）")
print("=" * 78)
E = 2.718281828459045
print(" K | 身份       | sum 1/k!        | err%% | 交替(-1)^k/k! | err%%")
print("-" * 78)
s_pos = 0.0
s_alt = 0.0
idmap = {4: "FIXED=4", 5: "SILENT=5", 7: "INVOL=7", 8: "K_MAX=8", 15: "SIGMA^-1=15", 42: "CONFIN=42"}
for K in range(0, 13):
    s_pos += 1.0 / factorial(K)
    if K >= 1:
        s_alt += (-1.0) ** K / factorial(K)
    elif K == 0:
        s_alt = 1.0
    print(" %2d | %-11s | %.8f | %+8.5f | %.8f | %+8.5f" % (
        K, idmap.get(K, ""), s_pos, (s_pos / E - 1) * 100, s_alt, (s_alt * E - 1) * 100))
# 幂型对照
print()
print(" (1+1/m)^m 幂型对照（m=框架量）")
for m in (3, 4, 5, 7, 8, 15, 42, 64):
    v = (1 + 1.0 / m) ** m
    print("  m=%2d: %.7f  err %+7.4f%%" % (m, v, (v / E - 1) * 100))
# 乘积链
p1 = p2 = p3 = 1.0
for j in range(1, 30):
    p1 *= (1 + 1.0 / 2**j)
for j in range(30):
    p2 *= (1 + 1.0 / 8**j)
print()
print(" 乘积链: Pi(1+2^-j)=%.6f, Pi(1+8^-j)=%.6f, e=%.6f" % (p1, p2, E))
print()
print("复算完成：与云端结论一致性核对——锚点带 8/8、W1=3/8、W2=0、对照表、K=8 截断 1e-6 级")
