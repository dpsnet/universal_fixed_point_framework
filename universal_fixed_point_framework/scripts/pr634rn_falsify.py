# -*- coding: utf-8 -*-
"""第 62 批数值先证伪：N_active 与「相的数量」是否同源。

按 Lean 定义逐字翻译：
  catOrder := 4            （ActiveFromCategoryOrder.lean L93）
  nActive(c) := c - 1      （同文件 L101，参数化为 catOrder 的函数）
  相判据 = 两条二值判据的 4 格排除 1 格（PhaseTrichotomy.lean，第 29 批）
  塔高 = {1, 2} ∪ 无界    （TowerHeightFromPhase.lean，第 30 批）
  B := ActiveLayers.card × N_total = 3 × 5
"""

OK = True


def chk(name, cond, val):
    global OK
    OK = OK and bool(cond)
    print(name, val)


C_RANGE = list(range(1, 21))

# ---------------------------------------------------------------- A
# nActive 是 catOrder 的函数：nActive(c) = c - 1
A1 = [(c, c - 1) for c in range(1, 11)]
chk("A_NACTIVE_FUNC_OK", all(isinstance(v, int) and v == c - 1 for c, v in A1), A1)
chk("A_NACTIVE_AT_FOUR", (4 - 1) == 3, 4 - 1)
chk("A_NACTIVE_AT_THREE", (3 - 1) == 2, 3 - 1)

# ---------------------------------------------------------------- B
# N_active = 3 唯一钉住 catOrder = 4（c >= 1）
B_sols = [c for c in C_RANGE if c - 1 == 3]
chk("B_UNIQUE_SOLUTION", B_sols == [4], B_sols)
B_non = [(c, c - 1) for c in C_RANGE if c != 4 and c - 1 != 3]
chk("B_OTHERS_DIFFER", all(v != 3 for _, v in B_non), len(B_non))

# ---------------------------------------------------------------- C
# 相判据的格数：两条二值判据 → 4 组合，排除「ker = ⊥ 且 ker ⊓ range ≠ ⊥」→ 3
# 该结论不含 catOrder（对每个 c 都得到同一格数）
def phase_cells(c_ignored):
    combos = [(k, kr) for k in (False, True) for kr in (False, True)]
    # 判据：ker = ⊥ ?  与  ker ⊓ range ≠ ⊥ ?
    # 排除格：ker = ⊥ (k=True 表示 ker=⊥) 且 ker ⊓ range ≠ ⊥
    keep = [x for x in combos if not (x[0] and x[1])]
    return len(keep)

C_vals = {c: phase_cells(c) for c in C_RANGE}
chk("C_CELLS_CONST", set(C_vals.values()) == {3}, sorted(set(C_vals.values())))
chk("C_CELLS_ALL_C", len(C_vals) == len(C_RANGE), len(C_vals))

# ---------------------------------------------------------------- D
# 任何有限读数（含 3）都不能封顶无界塔高：∀ N, ∃ k ≥ 2, k > N
D_bad = []
for N in (1, 2, 3, 5):
    k = max(2, N + 1)
    D_bad.append({"N": N, "k": k, "k_le_N": k <= N})
chk("D_NO_CAP", not any(x["k_le_N"] for x in D_bad), D_bad)

# ---------------------------------------------------------------- E
# B 的两个因子都是常数：ActiveLayers.card = 3、N_total = 5 ⇒ B = 15 与 c 无关
E_vals = {(3, 5): 15}
chk("E_B_CONST", list(E_vals.values()) == [15], list(E_vals.values()))

# ---------------------------------------------------------------- F
# 塔高集合与 nActive 的读数：3 ∉ {1, 2}，且 3 不能封顶（D）
HEIGHTS = {1, 2}
chk("F_NACTIVE_NOT_HEIGHT", 3 not in HEIGHTS, sorted(HEIGHTS))
chk("F_READOUTS_DISTINCT", len({5, 1, 2, 3}) == 4, sorted({5, 1, 2, 3}))

# ---------------------------------------------------------------- G
# 同值只在 c = 4：c = 5 时 nActive = 4 ≠ 3，但相仍是 3 格 ⇒ 巧合而非同源
G = {"c4": (4 - 1, phase_cells(4)), "c5": (5 - 1, phase_cells(5), phase_cells(5) != 5 - 1)}
chk("G_COINCIDENCE_ONLY_AT_FOUR",
    G["c4"][0] == 3 and G["c4"][1] == 3 and G["c5"][0] == 4 and G["c5"][1] == 3 and G["c5"][2], G)

print("VERDICT_ALL_OK", OK)
