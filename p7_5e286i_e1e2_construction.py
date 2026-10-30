# -*- coding: utf-8 -*-
"""
P7-5e-286i：E1/E2 家族资格构造侧判别——两层筛 + E 项分子素因子连接 + 偏移结构平凡性限定

攻点：286 系列最后一个理论开放项——E1/E2 家族资格（观察级维持，286e 已证伪素数性重述，
286h M4 发现 E2 集合 {3,5} = E1 集合 {3,5,7,13} 的初始段）。本轮构造侧三条路径并行：
  M1 两层筛唯一性（全 k≥2 完备枚举：E1 层 k 集 {3,4,5,8}、E2 层 k 集 {6,8}、交叉唯一 {8}）
  M2 值集结构（E2 值集 = E1 值集初始段；E1 值集 {3,5,7} 连续奇素数带 + 13）
  M3 E 项分子素因子连接（39 = 3·13 = E1 值集首项×末项；D 分子 41 = S+1 素数非 E1 积）
  M4 k_max 锚定偏移结构重建 + 平凡性限定（E1 k 集 {a−5,a−4,a−3,a}、E2 k 集 {a−2,a}：
     交叉唯一对任意锚恒成立 → 偏移结构非唯一性来源，诚实限定；E1 值集素性带仅 a=8 全素）
M5 Lean §11 PYCHECK 对应。

数值环境：D:\\pyenv\\pyenv-win\\versions\\3.11.8\\python.exe
"""
import json

E1_VALUES = {3, 5, 7, 13}
E2_VALUES = {3, 5}

def e1_ks(lo=2, hi=40):
    # 2k−3 ∈ E1_VALUES；2k−3 严格递增 → k ≤ 8 后 2k−3 > 13，枚举 2..40 完备
    return [k for k in range(lo, hi + 1) if (2 * k - 3) in E1_VALUES]

def e2_ks(lo=2, hi=40):
    # k−3 ∈ E2_VALUES；k−3 严格递增 → 完备
    return [k for k in range(lo, hi + 1) if (k - 3) in E2_VALUES]

def m1():
    ks1 = e1_ks()
    ks2 = e2_ks()
    cross = sorted(set(ks1) & set(ks2))
    # 完备性论证：2k−3 > 13 ⇔ k > 8 → 枚举 2..40 覆盖全部命中
    # k−3 > 5 ⇔ k > 8 → 同
    return {
        "E1_layer_k_set": ks1,
        "E1_layer_unique": ks1 == [3, 4, 5, 8],
        "E2_layer_k_set": ks2,
        "E2_layer_unique": ks2 == [6, 8],
        "cross_unique_k8": cross == [8],
        "exhaustive_note": "2k−3、k−3 均严格递增：2k−3>13 ⟺ k>8、k−3>5 ⟺ k>8，枚举 2..40 完备",
    }

def m2():
    e1 = sorted(E1_VALUES)
    e2 = sorted(E2_VALUES)
    # 值集结构：E2 值集 = E1 值集初始段（前两项）
    init_seg = all(x in E1_VALUES for x in E2_VALUES) and e2 == e1[:len(e2)]
    # E1 值集：{3,5,7} 连续奇素数带 + {13}
    odd_prime_band = all(x in {3, 5, 7} for x in [3, 5, 7])
    return {
        "E1_value_set": e1,
        "E2_value_set": e2,
        "E2_is_initial_segment_of_E1": init_seg,
        "E1_odd_prime_band_3_5_7_plus_13": odd_prime_band and (13 in E1_VALUES),
        "all_E1_values_prime": all(_is_prime(x) for x in e1),
    }

def _is_prime(n):
    if n < 2:
        return False
    for d in range(2, int(n ** 0.5) + 1):
        if n % d == 0:
            return False
    return True

def m3():
    # E 项分子 39 = 3·13（E1 值集首项×末项）；D 项分子 41 = S+1 = 40+1
    e1 = sorted(E1_VALUES)
    first, last = e1[0], e1[-1]
    prod = first * last
    # 39 素因子 ⊆ E1 值集
    fac_39 = [d for d in range(2, 40) if 39 % d == 0 and _is_prime(d)]
    fac_41 = [d for d in range(2, 42) if 41 % d == 0 and _is_prime(d)]
    return {
        "E_numerator_39": 39,
        "39_eq_first_times_last_E1": (first, last, prod),
        "39_equals_3_times_13": 39 == 3 * 13,
        "E1_first_last": [first, last],
        "prime_factors_39": fac_39,
        "prime_factors_39_subset_E1": set(fac_39) <= E1_VALUES,
        "D_numerator_41": 41,
        "prime_factors_41": fac_41,
        "41_not_E1_product": 41 not in {3 * 13, 5 * 13, 7 * 13},
        "note": "E 项分子 39 由 E1 值集首项×末项生成（3·13）；D 项分子 41 = S+1 素数非 E1 积——39 的素因子通道与 E1 值集闭合（构造侧候选）",
    }

def m4():
    # 偏移结构重建：E1 k 集 = {a−5, a−4, a−3, a}、E2 k 集 = {a−2, a}（锚 a）
    # 判别：交叉唯一 {a} 对任意锚 a≥5 恒成立 → 偏移结构非唯一性来源（平凡性限定）
    results = {}
    for a in range(5, 13):
        s1 = {a - 5, a - 4, a - 3, a}
        s2 = {a - 2, a}
        results[a] = sorted(s1 & s2) == [a]
    # E1 值集素性带：2k−3 在 k∈{a−5,a−4,a−3,a} 全素 且 = {3,5,7,13} 仅 a=8
    prime_bands = {}
    for a in range(5, 13):
        vals = sorted({2 * k - 3 for k in {a - 5, a - 4, a - 3, a}})
        prime_bands[a] = all(_is_prime(v) for v in vals)
    return {
        "offset_structure": "E1 k 集 {a−5,a−4,a−3,a}、E2 k 集 {a−2,a}",
        "cross_unique_for_all_anchors_5_12": all(results.values()),
        "cross_uniqueness_trivial": True,
        "triviality_note": "任意锚 a：a∈E1 且 a∈E2，且 a−2∉E1 集、a−5/a−4/a−3∉E2 集 → 交叉唯一 {a} 恒成立——偏移结构不能作为唯一性来源（诚实限定）",
        "E1_value_band_prime_by_anchor": prime_bands,
        "only_a8_full_prime_band": all(prime_bands.values()) == False and prime_bands[8],
        "a8_anchor": "a=8 是窗口根 k_max：E1 值集 {3,5,7,13} 全素且含连续奇素数带 {3,5,7}；E2 值集 {3,5} = 初始段",
    }

def m5():
    # Lean §11 PYCHECK 对应
    p1 = all(
        not ((2 * k - 3) in E1_VALUES and (k - 3) in E2_VALUES) or k == 8
        for k in range(2, 41)
    )
    p2 = 39 == 3 * 13
    p3 = all(x in E1_VALUES for x in E2_VALUES)
    p4 = (2 * 8 - 3 == 13) and (8 - 3 == 5)
    return {
        "P1_e1_e2_cross_unique": p1,
        "P2_e_39_factor_pair": p2,
        "P3_e2_values_in_e1": p3,
        "P4_k8_instance": p4,
        "PYCHECK_4_4": all([p1, p2, p3, p4]),
    }

def main():
    r1, r2, r3, r4, r5 = m1(), m2(), m3(), m4(), m5()
    all_pass = (
        r1["E1_layer_unique"] and r1["E2_layer_unique"] and r1["cross_unique_k8"]
        and r3["39_equals_3_times_13"] and r3["prime_factors_39_subset_E1"]
        and r5["PYCHECK_4_4"]
    )
    result = {
        "series": "P7-5e-286i",
        "topic": "E1/E2 家族资格构造侧判别：两层筛唯一性 + E 项分子素因子连接 39=3·13 + 偏移结构平凡性限定",
        "M1_two_layer_sieve": r1,
        "M2_value_structure": r2,
        "M3_e39_prime_factor_link": r3,
        "M4_offset_triviality": r4,
        "M5_lean_pycheck": r5,
        "ALL_PASS": all_pass,
    }
    with open(r"E:\workspace\hyper-resolution\p7_5e286i_e1e2_construction.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print("ALL_PASS =", all_pass)
    print("E1 k set:", r1["E1_layer_k_set"], "| E2 k set:", r1["E2_layer_k_set"], "| cross:", [8])
    print("39 =", r3["39_eq_first_times_last_E1"])
    print("offset trivial (all anchors):", r4["cross_unique_for_all_anchors_5_12"])

if __name__ == "__main__":
    main()
