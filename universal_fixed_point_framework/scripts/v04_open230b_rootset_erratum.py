# -*- coding: utf-8 -*-
# 104az-230 勘误重算：√3 自根集移除（143 已关闭 = √N_gen，非独立公设）
roots = [
    ("N_gen = 3",                     "结构常数",  "公设",       1),
    ("幂基 = 2",                      "结构常数",  "公设",       1),
    ("E0：对数-指数对 (ln, e)",        "超越函数对", "公设",       2),
    ("d_H（BranchCounting 条件定理零阶锚）", "自由参数", "结构性",  1),
    ("量纲锚 ħ, c, e",                "量纲锚",     "§6 承认",    3),
    ("B₀ = 2352.7 MG（观测锚）",       "观测锚",     "§6",        1),
]
n_sym = 0
n_anchor = 0
print("=== 根集清点（勘误后：√3 移除）===")
for name, cat, status, n in roots:
    print(f"  {name:<46}{cat:<8}{status:<10}{n}")
    n_sym += n
    if cat in ("量纲锚", "观测锚", "自由参数"):
        n_anchor += n
print(f"\n根集条目数 |R| = {len(roots)}")
print(f"根集符号数 = {n_sym}")
print(f"锚/自由参数 = {n_anchor} 符号 → 锚占比 = {n_anchor/n_sym*100:.1f}%")
print(f"“纯内生”可检验量 = 1 − 锚占比 = {100 - n_anchor/n_sym*100:.1f}%")
print("\n√3 勘误：104az-143 已关闭 —— √3 = √(k_max−静默) = √(8−5) = √N_gen（根集成员函数，非独立公设）")
print("  原 230 初版误列'⬜部分待溯源'，本条勘误自根集移除；根集块 L24 同步修正")
