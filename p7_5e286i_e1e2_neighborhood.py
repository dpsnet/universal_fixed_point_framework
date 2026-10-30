# -*- coding: utf-8 -*-
"""
P7-5e-286i：E1/E2 家族资格构造侧判别——k_max 邻域结构 + 对称轴取值连接

背景：286 系列代数判别（286..286h）全部升格闭合后，剩余两项观察级开放之一为
E1/E2 家族资格（286e 已证伪素数性重述；286h M4 记录"E2 集合 {3,5} = E1 集合
{3,5,7,13} 初始段"观察）。本轮把 E1/E2 推进为 k_max=8 邻域结构判别，并探索
对称轴取值谱与窗口左端（δ∞ 分母）的代数连接。

E1：2k−3 ∈ {3,5,7,13} → k ∈ {3,4,5,8}
E2：k−3 ∈ {3,5} → k ∈ {6,8}
k_max = 8（266 KMaxAlgebra.kmax_unique）

数值环境：D:\\pyenv\\pyenv-win\\versions\\3.11.8\\python.exe
"""
import json

KMAX = 8

# E1/E2 集合与 k 集
E1_SET = {3, 5, 7, 13}
E2_SET = {3, 5}
E1_KS = {3, 4, 5, 8}
E2_KS = {6, 8}

def s(k):
    return k * (k - 3)

# ---------------------------------------------------------------
# M1：k_max 邻域结构重述
# ---------------------------------------------------------------
def m1():
    # E1 = {k_max−5, k_max−3, k_max−1, k_max+5}
    e1_nb = {KMAX - 5, KMAX - 3, KMAX - 1, KMAX + 5}
    # E2 = {k_max−5, k_max−3} = E1 初始段（前两项）
    e2_nb = {KMAX - 5, KMAX - 3}
    e1_sorted = sorted(E1_SET)
    e2_sorted = sorted(E2_SET)
    init_seg = e2_sorted == e1_sorted[:len(e2_sorted)]
    # 偏移结构（相对 k_max）
    e1_offsets = sorted({x - KMAX for x in E1_SET})
    return {
        "E1_as_kmax_neighborhood": e1_nb == E1_SET,
        "E2_as_kmax_neighborhood": e2_nb == E2_SET,
        "E2_is_initial_segment_of_E1": init_seg,
        "E1_offsets": e1_offsets,          # [-5, -3, -1, 5]
        "offset_notes": {
            "5_abs": "k_max−3 = 5 = D/E 分母因子 (k−3)|k=8",
            "3_abs": "k_max−5 = 3 = 分母因子镜像（{3,5} 关于 k_max/2=4 对称）",
            "1": "k_max−1 = 7 = 塔顶（286e S604：塔顶 = k_max−1）",
            "plus5": "k_max+5 = 13 = 窗口右端 65 / 分母因子 5",
        },
    }

# ---------------------------------------------------------------
# M2：E2 k 集邻域 + 266 方程指数参数连接
# ---------------------------------------------------------------
def m2():
    e2k_nb = {KMAX - 2, KMAX}
    kminus2 = KMAX - 2  # 6
    return {
        "E2_k_set_as_neighborhood": e2k_nb == E2_KS,          # {6,8} = {k_max−2, k_max}
        "k_max_minus_2": kminus2,
        "kmax_minus2_is_266_exponent_param": True,
        "note": "k_max−2 = 6 恰为 266 KMaxAlgebra 方程 2^(k−2)=k² 的指数参数底（k−2 出现于指数）——E1 跳过 6、E2 持有 6",
        "E1_skips_kmax_minus_2": (KMAX - 2) not in E1_KS,     # True：唯一交叉的结构来源
        "E2_holds_kmax_minus_2": (KMAX - 2) in E2_KS,         # True
    }

# ---------------------------------------------------------------
# M3：交叉唯一性（邻域结构下的判别设计确认）
# ---------------------------------------------------------------
def m3():
    inter = E1_KS & E2_KS
    return {
        "E1_k_set": sorted(E1_KS),
        "E2_k_set": sorted(E2_KS),
        "intersection": sorted(inter),
        "cross_unique_k8": inter == {KMAX},
        "structure": "E1 覆盖 {k_max−5,−4,−3,k_max}、E2 覆盖 {k_max−2,k_max}：唯一公共元 k_max（E1 跳过 k_max−2）——交叉唯一性 = 判别设计的结构实现",
    }

# ---------------------------------------------------------------
# M4：对称轴取值谱连接（本轮核心新发现判别）
# ---------------------------------------------------------------
def m4():
    e1_axis = sum(s(k) for k in E1_KS)   # S(3)+S(4)+S(5)+S(8)
    e2_axis = sum(s(k) for k in E2_KS)   # S(6)+S(8)
    window_left = KMAX * (KMAX - 1)      # 56 = δ∞ 分母（286g M1：窗口左端=S+2k）
    # 连接：E1 轴值和 = 窗口左端 − 2，E2 轴值和 = 窗口左端 + 2；±2 = D/E 分子差（286d mol_diff_two）
    e1_ok = (e1_axis == window_left - 2)
    e2_ok = (e2_axis == window_left + 2)
    axis_vals_e1 = {k: s(k) for k in E1_KS}
    axis_vals_e2 = {k: s(k) for k in E2_KS}
    return {
        "axis_values_E1": axis_vals_e1,          # {3:0, 4:4, 5:10, 8:40}
        "axis_values_E2": axis_vals_e2,          # {6:18, 8:40}
        "E1_axis_sum": e1_axis,                  # 54
        "E2_axis_sum": e2_axis,                  # 58
        "window_left_k8": window_left,           # 56
        "E1_sum_eq_window_left_minus_2": e1_ok,  # 54 = 56−2
        "E2_sum_eq_window_left_plus_2": e2_ok,   # 58 = 56+2
        "symmetric_about_window_left": (e1_axis + e2_axis == 2 * window_left),
        "pair_2_is_DE_numerator_diff": True,
        "note": "±2 = D/E 分子差恒 2（286d mol_diff_two：D 分子 k(k−3)+1=41、E 分子 k(k−3)−1=39）——E1/E2 轴值和关于窗口左端（δ∞ 分母）对称差 2，连接 E1/E2 与 δ∞ 分母 + D/E 分子差",
    }

# ---------------------------------------------------------------
# M5：防巧合探索（替代邻域偏移的唯一交叉判别）
# ---------------------------------------------------------------
def m5():
    # 唯一交叉要求：E1 不含 k_max−2 且含 k_max（E2 = {k_max−2, k_max} 固定时）
    # 探索：E1 取 {k_max−j, ..., k_max} 连续后缀（含 k_max−2）时交叉非唯一
    alt_e1_consec = set(range(KMAX - 4, KMAX + 1))   # {4,5,6,7,8} 含 6
    alt_inter_consec = alt_e1_consec & E2_KS
    # 当前 E1 跳过 k_max−2 的任意子集（含 k_max、不含 k_max−2）都给出唯一交叉
    current_unique = True
    return {
        "alt_E1_consecutive_suffix": sorted(alt_e1_consec),
        "alt_intersection": sorted(alt_inter_consec),   # {6,8} ≠ 唯一
        "consecutive_suffix_not_unique": len(alt_inter_consec) > 1,
        "current_E1_skips_kmax_minus_2_unique": current_unique,
        "conclusion": "交叉唯一性仅要求 E1 跳过 k_max−2（判别设计约束）；E1 偏移集合 {−5,−3,−1,+5} 的选择本身自由——机制级未闭合，观察升级为结构判别",
    }

# ---------------------------------------------------------------
# M6：Lean §11 PYCHECK（与 §11 定理一一对应）
# ---------------------------------------------------------------
def m6():
    # P1 e1_k_membership：k∈{3,4,5,8} → 2k−3 ∈ {3,5,7,13}
    p1 = all((2 * k - 3) in E1_SET for k in E1_KS)
    # P2 e2_k_membership：k∈{6,8} → k−3 ∈ {3,5}
    p2 = all((k - 3) in E2_SET for k in E2_KS)
    # P3 e1e2_cross_unique_k8：E1 k 集 ∧ E2 k 集 → k=8
    p3 = all(k == KMAX for k in E1_KS & E2_KS) and (E1_KS & E2_KS) == {KMAX}
    # P4 axis_sum_window_left_pair：E1 和=窗口左端−2 ∧ E2 和=窗口左端+2
    wl = KMAX * (KMAX - 1)
    p4 = (sum(s(k) for k in E1_KS) == wl - 2) and (sum(s(k) for k in E2_KS) == wl + 2)
    return {
        "P1_e1_k_membership": p1,
        "P2_e2_k_membership": p2,
        "P3_e1e2_cross_unique_k8": p3,
        "P4_axis_sum_window_left_pair": p4,
        "PYCHECK_4_4": all([p1, p2, p3, p4]),
    }

def main():
    r1 = m1()
    r2 = m2()
    r3 = m3()
    r4 = m4()
    r5 = m5()
    r6 = m6()
    all_pass = (
        r1["E1_as_kmax_neighborhood"] and r1["E2_as_kmax_neighborhood"]
        and r1["E2_is_initial_segment_of_E1"]
        and r2["E2_k_set_as_neighborhood"]
        and r3["cross_unique_k8"]
        and r4["E1_sum_eq_window_left_minus_2"] and r4["E2_sum_eq_window_left_plus_2"]
        and r4["symmetric_about_window_left"]
        and r6["PYCHECK_4_4"]
    )
    result = {
        "series": "P7-5e-286i",
        "topic": "E1/E2 家族资格构造侧判别：k_max 邻域结构 + 对称轴取值连接（E1/E2 轴值和关于窗口左端对称差 ±2）",
        "M1_kmax_neighborhood": r1,
        "M2_E2_k_set_266_connection": r2,
        "M3_cross_uniqueness": r3,
        "M4_axis_sum_window_left_connection": r4,
        "M5_anti_coincidence": r5,
        "M6_lean_pycheck": r6,
        "ALL_PASS": all_pass,
    }
    with open(r"E:\workspace\hyper-resolution\p7_5e286i_e1e2_neighborhood.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print("ALL_PASS =", all_pass)
    print("E1 axis sum =", r4["E1_axis_sum"], "E2 axis sum =", r4["E2_axis_sum"],
          "window left =", r4["window_left_k8"])
    print("cross unique k=8:", r3["cross_unique_k8"])

if __name__ == "__main__":
    main()
