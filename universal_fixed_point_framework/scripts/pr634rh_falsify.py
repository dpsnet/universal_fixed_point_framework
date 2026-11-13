# -*- coding: utf-8 -*-
"""PR-634 第 56 批 模式 8 数值先证伪
命题：B = N_active * N_total = (c-1)*(c+1) = c^2 - 1 与 Mersenne M_c = 2^c - 1
在框架域 c >= 3 内是否唯一同值于 c = 4。
"""

# --- A: (c-1)*(c+1) 与 2^c - 1 的相等点（全域，c >= 0）---
A_HITS = []
A_FAILS = []
for c in range(0, 41):
    lhs = (c - 1) * (c + 1)
    rhs = 2 ** c - 1
    if lhs == rhs:
        A_HITS.append(c)
    else:
        A_FAILS.append((c, lhs, rhs))
print("A_HITS", A_HITS)
print("A_COUNT_HITS", len(A_HITS))
print("A_COUNT_FAILS", len(A_FAILS))

# --- B: 限制 c >= 3 ---
B_HITS = [c for c in A_HITS if c >= 3]
print("B_HITS", B_HITS)
print("B_PIN_UNIQUE", B_HITS == [4])

# --- C: 由 B = 15 反解 c（N_active = c-1, N_total = c+1, B = 15）---
C_SOL = [c for c in range(0, 41) if (c - 1) * (c + 1) == 15]
C_SOL_GE3 = [c for c in C_SOL if c >= 3]
print("C_SOL", C_SOL)
print("C_SOL_GE3", C_SOL_GE3)
print("C_UNIQUE_GE3", C_SOL_GE3 == [4])

# --- D: 偏离表 ---
print("D_TABLE (c, (c-1)(c+1), 2^c-1, diff)")
for c in [2, 3, 4, 5, 6, 8, 10]:
    lhs = (c - 1) * (c + 1)
    rhs = 2 ** c - 1
    print("D %d LHS %d MER %d DIFF %+d" % (c, lhs, rhs, lhs - rhs))

# --- E: c^2 - 1 与 (c-1)(c+1) 恒等式全称检验（c 1..40）---
E_FAILS = []
for c in range(1, 41):
    a = (c - 1) * (c + 1)
    b = c * c - 1
    if a != b:
        E_FAILS.append(c)
print("E_IDENTITY_FAILS", E_FAILS)
print("E_IDENTITY_OK", len(E_FAILS) == 0)

# --- F: c=1 边界（c-1 = 0，Nat 截断风险）---
print("F_C1", (1 - 1) * (1 + 1), 1 * 1 - 1)
print("F_C0", (0 - 1) * (0 + 1), 0 * 0 - 1)

VERDICT_A = len(A_FAILS) == 39
VERDICT_B = B_HITS == [4]
VERDICT_C = C_SOL_GE3 == [4]
VERDICT_E = len(E_FAILS) == 0
print("VERDICT_A", VERDICT_A)
print("VERDICT_B", VERDICT_B)
print("VERDICT_C", VERDICT_C)
print("VERDICT_E", VERDICT_E)
print("VERDICT_ALL_OK", VERDICT_A and VERDICT_B and VERDICT_C and VERDICT_E)
