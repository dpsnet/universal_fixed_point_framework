# -*- coding: utf-8 -*-
"""反向翻译精确化先证伪：orbitCount=15 的完整解集。

模型：silenceRec15_layered S，Fin 15 四层 {0..3}/{4..9}/{10..13}/{14}。
layeredStep 层内循环：3->0, 9->4, 13->10, 14->14（层4=1-周期，天然不动点）。
silentStep S x = x if x in S else layeredStep x。
orbitCount = 周期点循环类数（periodicPoint 逐字对齐 Lean：∃p>0, step^[p] x = x）。

待验证命题 P：
  orbitCount(silenceRec15_layered S) = 15  ⟺  S = univ ∨ S = univ − {14}
即"15 的实现 = 全静默（univ）或 除 14 外全静默（14 天然不动无需静默）"。

辅助口径：S.card + fullActiveCount S = 15 的解集应同样为 {univ, univ−{14}}。

穷举 2^15 = 32768 全枚举。
"""
from itertools import product

N = 15
UNIV = frozenset(range(N))

def layered_step(x):
    if x <= 3:
        return (x + 1) % 4          # 层1: 0->1->2->3->0
    if x <= 9:
        return 4 + (x - 4 + 1) % 6  # 层2: 4..9 循环
    if x <= 13:
        return 10 + (x - 10 + 1) % 4 # 层3: 10..13 循环
    return 14                        # 层4: 14->14（1-周期，天然不动点）

def silent_step(S, x):
    return x if x in S else layered_step(x)

def is_periodic(S, x):
    # 逐字对齐 Lean periodicPoint：∃p>0, step^[p] x = x
    cur = x
    seen = set()
    while cur not in seen:
        seen.add(cur)
        cur = silent_step(S, cur)
    return cur == x  # 撞回自身（含 p=1 不动点）

def orbit_count(S):
    reps = set()
    for x in range(N):
        if is_periodic(S, x):
            # 沿正向可达类（frozenset 不可用于周期点检测的等价类，用最小可达集）
            cyc = []
            cur = x
            cseen = set()
            while cur not in cseen:
                cseen.add(cur)
                cyc.append(cur)
                cur = silent_step(S, cur)
            reps.add(frozenset(cyc[-1:]) if cur in cyc[-1:] else frozenset())
    # 用"每个周期点的轨道循环"求代表：取循环的 frozenset
    cycles = set()
    for x in range(N):
        if is_periodic(S, x):
            cur = x
            cseen = set()
            chain = []
            while cur not in cseen:
                cseen.add(cur)
                chain.append(cur)
                cur = silent_step(S, cur)
            if cur in chain:  # 有循环
                cyc = frozenset(chain[chain.index(cur):])
            else:
                cyc = frozenset()
            cycles.add(cyc)
    return len(cycles)

def layers():
    return [frozenset(range(4)), frozenset(range(4, 10)), frozenset(range(10, 14)), frozenset([14])]

def full_active_count(S):
    return sum(1 for L in layers() if not (L & S))

def main():
    sol_count15 = []       # orbitCount == 15 的解
    sol_formula15 = []     # card + fullActive = 15 的解
    formula_mismatch = 0   # orbitCount 与公式不符的计数（v3 应零）
    formula_total = 0
    checked = 0
    for bits in product([0, 1], repeat=N):
        S = frozenset(x for x in range(N) if bits[x])
        oc = orbit_count(S)
        formula = len(S) + full_active_count(S)
        if formula != oc:
            formula_mismatch += 1
        formula_total += 1
        if oc == 15:
            sol_count15.append(S)
        if formula == 15:
            sol_formula15.append(S)
        checked += 1

    univ = UNIV
    univ_minus_14 = UNIV - frozenset([14])
    expect = {univ, univ_minus_14}

    print("=== 反向翻译精确化先证伪 ===")
    print(f"穷举配置数: {checked}")
    print(f"公式 orbitCount = card S + fullActiveCount S 违例数: {formula_mismatch}/{formula_total}")
    print()
    print("orbitCount=15 解数:", len(sol_count15))
    for s in sorted(sol_count15, key=lambda s: (len(s), sorted(s))):
        print("  ", "S.card=%d" % len(s), "fullActive=%d" % full_active_count(s),
              "S=", sorted(s))
    ok_count = set(sol_count15) == expect
    print("orbitCount=15 ⟺ {univ, univ-{14}} ?", ok_count)
    print()
    print("card+fullActive=15 解数:", len(sol_formula15))
    ok_formula = set(sol_formula15) == expect
    print("card+fullActive=15 ⟺ {univ, univ-{14}} ?", ok_formula)
    # 补充：检查 S=univ-{14} 的 orbitCount 与是否恒等
    for name, S in [("univ", univ), ("univ-{14}", univ_minus_14),
                    ("univ-{13}", UNIV - frozenset([13]))]:
        print(name, "orbitCount=", orbit_count(S), "card=", len(S),
              "fullActive=", full_active_count(S))
    print()
    print("PASS" if (ok_count and ok_formula and formula_mismatch == 0) else "FAIL")

if __name__ == "__main__":
    main()
