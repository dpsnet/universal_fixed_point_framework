# -*- coding: utf-8 -*-
"""第 61 批数值先证伪：标号 5 与三相塔高（1 / 2 / 无界）的关系。

按 Lean 定义逐字翻译：
  C 相 = 平坦：ker(adLin2 A B) = 0            ⇒ 无层 2 见证 ⇒ 塔高 1
  A 相 = 止步：ker ≠ 0 ∧ ker ∩ range = 0      ⇒ 层 2 有、层 3 无 ⇒ 塔高 2
  B 相 = 可穿：ker ≠ 0 ∧ ker ∩ range ≠ 0      ⇒ 判据层号无关 ⇒ 塔高无界
  标号   = Fintype.card LayerIndex = 5 = nTotal = catOrder + 1
  生成代数计数 = nActive = catOrder - 1 = 3
"""

INF = float("inf")   # 无界：Lean 侧为 "∀ k ≥ 2, LayerWitness jordan3"，不是数值 ∞

HEIGHTS = {"C_flat": 1, "A_stop": 2, "B_traverse": INF}
LABELS = {"card_LayerIndex": 5, "nTotal": 5, "nActive": 3}


def check_A():
    """标签值是否落在塔高集合 {1, 2} 内。"""
    in_set = [k for k, v in LABELS.items() if v in (1, 2)]
    print("A LABELS_IN_HEIGHT_SET", in_set)
    print("A HEIGHT_VALUES", sorted([h for h in HEIGHTS.values() if h != INF]))
    print("A_CARD_FIVE_IN_SET", 5 in (1, 2))
    print("A_ACTIVE_THREE_IN_SET", 3 in (1, 2))
    return in_set == []


def check_B():
    """B = 3 × 5；若把 3 换成任一相塔高，B 不再为 15。"""
    table = [(3, 5, 3 * 5), (2, 5, 2 * 5), (1, 5, 1 * 5)]
    print("B FACTOR_TABLE (first_factor, label, product)", table)
    only_three = [t for t in table if t[2] == 15]
    print("B_ONLY_THREE_GIVES_15", only_three)
    return table[0][2] == 15 and table[1][2] == 10 and table[2][2] == 5


def check_C():
    """无界性：∀ N，存在 k ≥ 2 使 k > N。"""
    ok = True
    witness = []
    for N in range(2, 21):
        ks = [k for k in range(2, N + 4) if k > N]
        if not ks:
            ok = False
        witness.append((N, ks[0] if ks else None))
    print("C NO_NAT_BOUND", ok)
    print("C SAMPLES (N, k):", witness[:6], "...", witness[-2:])
    return ok


def check_D():
    """标号 5 与三相全部共存：5 不等于任何一相塔高。"""
    not_equal = []
    for name, h in HEIGHTS.items():
        if h != 5:
            not_equal.append(name)
    print("D_LABEL_NOT_A_HEIGHT", sorted(not_equal))
    print("D_COEXIST (label, phase) :", [(5, n) for n in sorted(HEIGHTS)])
    return len(not_equal) == 3


def check_E():
    """N = 5 作为上界会被 k = 6 打破。"""
    N = 5
    k = 6
    print("E_FIVE_BREAKS", k > N, "(N,k)=", (N, k))
    return k > N


def check_F():
    """三相判据的 4 格：ker=0 / ker∩range=0 的取值组合，必空一格。"""
    cells = []
    for ker_bot in (True, False):
        for inf_bot in (True, False):
            cells.append((ker_bot, inf_bot))
    excluded = [(True, False)]   # ker = 0 且 ker∩range ≠ 0：自相矛盾
    remain = [c for c in cells if c not in excluded]
    print("F CELLS", len(cells), "EXCLUDED", len(excluded), "REMAIN", len(remain))
    print("F REMAIN_CELLS", remain)
    return len(remain) == 3


def check_G():
    """三个读数互不相等：5 / 1 / 2 / 无界。"""
    print("G READOUTS label=5 C=1 A=2 B=", "unbounded")
    print("G_PAIRS_DISTINCT", len({5, 1, 2}) == 3)
    return len({5, 1, 2}) == 3


def main():
    results = [check_A(), check_B(), check_C(), check_D(), check_E(), check_F(), check_G()]
    print("VERDICT_ALL_OK", all(results))


if __name__ == "__main__":
    main()
