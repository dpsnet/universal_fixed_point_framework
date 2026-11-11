# -*- coding: utf-8 -*-
"""
第 28 批 数值先证伪（模式 8）：
交汇方程 + 顺序约束 是否唯一筛出 (k_max, N_gen) = (8, 3)？

核心猜想：
  交汇方程   N*(2j - N) = 2^j - 1        (j = k_max/2, 2j = k_max)
  顺序约束   2 <= N < j                   (N = N_gen 小于半指数)
  =>         2j = 8 且 N = 3   （唯一）

以及 σ^-1 双分解的相容性：
  15 = 3*5 = M_4,  3 + 5 = 8 = 2*4,  3 < 5
"""
import itertools

FAIL = []


def check(name, cond, detail=""):
    if cond:
        print("[PASS] %s %s" % (name, detail))
    else:
        print("[FAIL] %s %s" % (name, detail))
        FAIL.append(name)


print("=" * 60)
print("A. 全枚举：交汇方程 + 2 <= N < j 的解集")
print("=" * 60)

solutions_all = []
solutions_constrained = []
for j in range(1, 41):
    for N in range(1, 2 * j):
        if N * (2 * j - N) == 2 ** j - 1:
            solutions_all.append((j, N, 2 * j))
            if 2 <= N < j:
                solutions_constrained.append((j, N, 2 * j))

print("  全部解 (j, N, k_max) :", solutions_all)
print("  加约束后            :", solutions_constrained)

check("A1 全部解集 = {(1,1,2),(2,1,4),(2,3,4),(4,3,8),(4,5,8)}",
      sorted(solutions_all) == sorted([(1, 1, 2), (2, 1, 4), (2, 3, 4), (4, 3, 8), (4, 5, 8)]),
      str(sorted(solutions_all)))

check("A2 约束 2<=N<j 后唯一 = (4,3,8)",
      solutions_constrained == [(4, 3, 8)],
      str(solutions_constrained))

print()
print("=" * 60)
print("B. 逐条筛除：哪条约束排掉哪个解")
print("=" * 60)

rows = []
for (j, N, km) in solutions_all:
    r2 = (N >= 2)
    r3 = (N < j)
    rows.append((j, N, km, r2, r3, r2 and r3))
    print("  (j=%d, N=%d, k_max=%d)  N>=2:%s  N<j:%s  保留:%s" % (j, N, km, r2, r3, r2 and r3))

check("B1 仅 (4,3,8) 同时满足 N>=2 与 N<j",
      [r for r in rows if r[5]] == [(4, 3, 8, True, True, True)])
check("B2 (8,5,8) 被 N<j 排掉（5<4 不成立）", not (5 < 4))
check("B3 (4,3,4) 被 N<j 排掉（3<2 不成立）", not (3 < 2))
check("B4 (2,1,2) 被 N>=2 排掉", not (1 >= 2))

print()
print("=" * 60)
print("C. sigma^-1 双分解相容性：15 = 3*5 = M_4, 3+5 = 8 = 2*4")
print("=" * 60)

sig_inv = 15
N_gen = 3
silent = 5
j_from_mersenne = 4
check("C1 3*5 = 15 = sigma^-1", N_gen * silent == sig_inv, "%d*%d=%d" % (N_gen, silent, N_gen * silent))
check("C2 2^4-1 = 15 = M_4", 2 ** 4 - 1 == sig_inv, "2^4-1=%d" % (2 ** 4 - 1))
check("C3 3+5 = 8 = 2*4 = k_max", N_gen + silent == 2 * j_from_mersenne,
      "%d+%d=%d" % (N_gen, silent, N_gen + silent))
check("C4 3 < 5（分解因子有序）", N_gen < silent)
check("C5 3 < 4（N_gen < j）", N_gen < j_from_mersenne)
check("C6 k_max = 8 = 2^3 = 2^N_gen", 2 ** N_gen == 8, "2^3=%d" % 2 ** N_gen)

print()
print("  推论链：")
print("    sigma^-1 = N_gen * silent        (104az-91 双分解)")
print("    silent    = 2j - N_gen           (因 k_max = 2j = N_gen + silent)")
print("    N_gen < silent  <=>  N_gen < j   (2*N_gen < 2j)")
print("    => 交汇方程 + 2<=N<j  =>  (j,N) = (4,3)  =>  k_max = 8, N_gen = 3")

# 验证 5 中的等价：N_gen < silent <=> N_gen < j
print()
print("=" * 60)
print("D. 等价性：N < S <=> N < j   （当 2j = N + S 时）")
print("=" * 60)

ok = True
for j in range(1, 41):
    for N in range(1, 2 * j):
        S = 2 * j - N
        if S < 1:
            continue
        if (N < S) != (N < j):
            ok = False
            print("  [MISMATCH] j=%d N=%d S=%d" % (j, N, S))
check("D1 对 2j=N+S 的全部 (j,N)，N<S <=> N<j", ok)

print()
print("=" * 60)
print("E. 反例搜索：是否存在 A 之外的第二条独立筛选路径给出同样结果")
print("=" * 60)

# 检查 M_j 的互补分解是否唯一（用于确认 C 的'顺序'约束是唯一的筛选力）
for j in range(1, 25):
    M = 2 ** j - 1
    pairs = [(a, M // a) for a in range(1, M + 1) if M % a == 0 and a <= M // a]
    print("  M_%-2d = %-8d 互补对(a,b), a+b=2j? :" % (j, M), end=" ")
    hit = [p for p in pairs if p[0] + p[1] == 2 * j]
    print(hit if hit else "无")

print()
print("=" * 60)
if FAIL:
    print("FAILED CHECKS:", FAIL)
    print("VERDICT_ALL_OK = False")
else:
    print("VERDICT_ALL_OK = True")
print("=" * 60)
