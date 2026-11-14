"""PR-634 第 60 批：`N_total = catOrder + 1` / `N_active = catOrder − 1` 那一对边界 `±1`（模式 8）

库内四处 `N_total`：
  CategoryOrder.nTotal      := catOrder + 1        （函数，L96）
  CatOrderSpacetime.nTotalOf:= catOrderOf d + 1    （函数，L105）
  BranchCounting.N_total    := 5                   （裸常量，L86）
  DHStructural.N_total      := 5                   （裸常量，L109）
并有 nActive := catOrder − 1（L101）。

检验目标：
  A 「去两层」是不是恒等式：c − 1 = (c + 1) − 2 对所有 c 成立
  B ±1 对称：c+1 与 c−1 之和 = 2c（c ≥ 1）
  C 括号平方：(c − 1)(c + 1) + 1 = c²（c ≥ 1）⇒ B 完全由 c 决定
  D ±1 各自变动对 B 的敏感性
  E 函数口径 vs 裸常量口径：只在 c = 4 重合
  F B(c) 与 2^c − 1 的重合集（第 56 批结论对照）
"""

def nTotal_func(c): return c + 1
def nActive_func(c): return c - 1
N_TOTAL_LITERAL = 5          # BranchCounting.N_total / DHStructural.N_total
N_ACTIVE_LITERAL = 3         # DHStructural.N_active

print("A SUB_IS_ADD_SUB_TWO", all((c - 1) == (c + 1) - 2 for c in range(0, 25)))
print("A_AT_CATORDER", 4 - 1, (4 + 1) - 2)

print("B SYMMETRIC_SUM", all(((c + 1) + (c - 1) == 2 * c) for c in range(1, 25)))

print("C BRACKETED_SQUARE", all((c - 1) * (c + 1) + 1 == c * c for c in range(1, 25)))

rowsD = []
for top in (0, 1, 2):
    for bot in (0, 1, 2):
        c = 4
        nt = c + top
        na = c - bot
        rowsD.append((top, bot, nt, na, na * nt))
print("D OFFSET_TABLE (top,bot,N_total,N_active,B):", rowsD)
print("D_BASELINE_15", [r for r in rowsD if r[0] == 1 and r[1] == 1][0][4] == 15)

rowsE = [(c, nTotal_func(c), N_TOTAL_LITERAL, nActive_func(c), N_ACTIVE_LITERAL) for c in range(1, 10)]
print("E FUNCTION_VS_LITERAL (c, c+1, 5, c-1, 3):", rowsE)
agree_t = [c for c, a, b, _, _ in rowsE if a == b]
agree_a = [c for c, _, _, a, b in rowsE if a == b]
print("E_AGREE_ON_NTOTAL", agree_t, "E_AGREE_ON_NACTIVE", agree_a)

print("F B_VS_MERSENNE (c, (c-1)(c+1), 2^c-1):",
      [(c, (c - 1) * (c + 1), 2 ** c - 1) for c in range(2, 11)])
print("F_COINCIDE", [c for c in range(2, 11) if (c - 1) * (c + 1) == 2 ** c - 1])
print("F_COINCIDE_GE3", [c for c in range(3, 11) if (c - 1) * (c + 1) == 2 ** c - 1])

print("G_LITERAL_B", N_ACTIVE_LITERAL * N_TOTAL_LITERAL)

ok = (all((c - 1) == (c + 1) - 2 for c in range(0, 25))
      and all(((c + 1) + (c - 1) == 2 * c) for c in range(1, 25))
      and all((c - 1) * (c + 1) + 1 == c * c for c in range(1, 25))
      and [r for r in rowsD if r[0] == 1 and r[1] == 1][0][4] == 15
      and agree_t == [4] and agree_a == [4]
      and [c for c in range(3, 11) if (c - 1) * (c + 1) == 2 ** c - 1] == [4]
      and N_ACTIVE_LITERAL * N_TOTAL_LITERAL == 15)
print("VERDICT_ALL_OK", ok)
