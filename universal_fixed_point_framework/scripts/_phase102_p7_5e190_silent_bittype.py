# -*- coding: utf-8 -*-
"""
P7-5e-190 · 静默 k 位型分类 + 窗口异类 + 下窗口预言（189 的 ①②③ 合并判别）
用户推进（2026-10-15）："1 2 3"

检验设计：
G. 静默 k 的 2 进位型分类——已登记静默单元 k 全集按二进制位型分类
   （单位位 2^p / 相邻双位 2^p+2^{p+1} / 隔位双位 2^p+2^{p+2} / 其他）
   → 位型→身份族映射（单位位→2^m+1 家族（186 重合面）；相邻双位→窗口对合常数（189）；隔位→D 分子 41）
   → 判别：窗口常数 k 是否全部相邻双位；相邻双位静默单元是否=窗口常数（同一性）
H. 窗口 1 起点异类 a₁=1：替代公式值 a₁=5（=2²+1）→ 对合常数 13（C 分子身份！）vs 实际 9（域界）——判别为何取 1
3. 下窗口预言登记：c₄=97（k=12）、c₆=385（k=48）——静默 k 相邻双位、框架外、预言若扩展应获身份
"""
import json

OUT = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_phase102_p7_5e190_silent_bittype.json"

# ---------- 已登记静默单元全集（8k+1，含身份） ----------
# 框架内（m<=8 谱上出现）+ 窗口常数（189）
silent_units = {
    9:   {"k": 1,  "roles": ["域界/对合常数 K+1", "2^3+1", "静默 k=1"], "window_const": True},
    17:  {"k": 2,  "roles": ["尖端沉默位点", "2^4+1", "静默 k=2"], "window_const": False},
    25:  {"k": 3,  "roles": ["静默 k=3"], "window_const": True},
    33:  {"k": 4,  "roles": ["尖端沉默位点", "2^5+1", "静默 k=4"], "window_const": False},
    41:  {"k": 5,  "roles": ["D 分子 8·5+1", "静默 k=5"], "window_const": False},
    49:  {"k": 6,  "roles": ["静默 k=6", "(k_max-1)^2"], "window_const": True},
    65:  {"k": 8,  "roles": ["修正 1/65", "2^6+1", "静默 k=8"], "window_const": False},
    81:  {"k": 10, "roles": ["D_9 超对合域（m=-9，P7-5e-110）", "9^2", "静默 k=10"], "window_const": False},
    97:  {"k": 12, "roles": ["窗口 4 对合常数（189，框架外预言）"], "window_const": True},
    129: {"k": 16, "roles": ["2^7+1 闭式编号", "静默 k=16"], "window_const": False},
    193: {"k": 24, "roles": ["静默 k=24"], "window_const": True},
    257: {"k": 32, "roles": ["2^8+1", "静默 k=32"], "window_const": False},
    385: {"k": 48, "roles": ["窗口 6 对合常数（189，框架外预言）"], "window_const": True},
}

# ---------- 位型分类 ----------
def bittype(k):
    """k 的 2 进位型：单位位 / 相邻双位 / 隔位双位 / 其他"""
    bits = [i for i in range(k.bit_length()) if (k >> i) & 1]
    n = len(bits)
    if n == 1:
        return "unit_bit(2^p)"
    if n == 2:
        gap = bits[1] - bits[0]
        if gap == 1:
            return "adjacent_bits(2^p+2^{p+1})"
        if gap == 2:
            return "gap_bit(2^p+2^{p+2})"
        return f"other_2bit(gap={gap})"
    return f"multi({n}bits)"

classified = []
for v, info in sorted(silent_units.items()):
    k = info["k"]
    t = bittype(k)
    info["bittype"] = t
    info["binary"] = format(k, "b")
    info["value"] = v
    classified.append(info)

# ---------- G：位型 → 身份族映射 ----------
family_map = {}
for info in classified:
    t = info["bittype"]
    family_map.setdefault(t, []).append(info)

# 身份族判定：2^m+1 家族（unit_bit）/ 窗口常数 / 对合域常数
family_assign = {}
for t, infos in family_map.items():
    fams = set()
    for info in infos:
        v = info["value"]
        roles = info["roles"]
        if info["bittype"] == "unit_bit(2^p)":
            fams.add("2^m+1 家族（186 重合面）")
        if info["window_const"]:
            fams.add("窗口对合常数（189）")
        if any("D 分子" in r or "D_" in r or "对合域" in r for r in roles):
            fams.add("对合域常数（41 D 分子 / 81 D_9 超对合域）")
    family_assign[t] = sorted(fams)

# 判别 G1：窗口常数 k——c_1=9(k=1 单位位，根窗口异类)、c_{j>=2} 全部相邻双位
window_consts = [i for i in classified if i["window_const"]]
g1 = all(
    (i["value"] == 9 and i["bittype"] == "unit_bit(2^p)") or
    (i["value"] != 9 and i["bittype"] == "adjacent_bits(2^p+2^{p+1})")
    for i in window_consts
)
# 判别 G2：相邻双位静默单元 全部 = 窗口常数（同一性，非仅判别）
adjacent_units = [i for i in classified if i["bittype"] == "adjacent_bits(2^p+2^{p+1})"]
g2 = all(i["window_const"] for i in adjacent_units)
# 判别 G3：单位位静默单元 全部 = 2^m+1 家族（m=p+3；9 兼窗口 1 常数）
unit_units = [i for i in classified if i["bittype"] == "unit_bit(2^p)"]
g3 = all(i["value"] == 2 ** (int(i["k"]).bit_length() - 1 + 3) + 1 for i in unit_units)
# 判别 G4：隔位双位静默单元 全部 = 对合域常数（41 D 分子 / 81 D_9 超对合域）
gap_units = [i for i in classified if i["bittype"] == "gap_bit(2^p+2^{p+2})"]
g4 = all(any("对合域" in r or "D_" in r or "D 分子" in r for r in i["roles"]) for i in gap_units)

# ---------- H：窗口 1 异类 ----------
# 实际：a1=1 -> c1=9（域界）；公式值 a1'=2^{1+1}+1=5 -> c1'=13（C 分子 13/128！）
h_analysis = {
    "actual_a1": 1,
    "actual_c1": 9,
    "actual_c1_roles": ["域界/对合常数 K+1", "静默 k=1"],
    "formula_a1": 5,
    "formula_c1": 13,
    "formula_c1_roles": ["C 分子 2^2+3^2", "13/128"],
    "question": "窗口 1 起边界为何取恒等 1（→域界 9）而非公式值 5（→C 分子 13）？",
    "candidates": [
        "窗口 1 需覆盖 m=1,2（截距分子 3,5，非静默家族），从恒等 1 开始才能包含非静默段——窗口 1 是'根窗口'，含 m<=2 的非家族成员",
        "9=域界（K+1）为 183 对合 K=8 的直接 +1，优先级高于 C 分子（系数分子层）",
        "a1=1 与 α0^3=1/8 静默修正底/δ∞ 恒等式 1/7−1/8 的 1 呼应（恒等起点语义）",
        "若取 5：窗口 1 变为 [5,8] 仅 4 层，丢失 m=1..4 通道——与 k_max=8 通道数锁定冲突",
    ],
    "tentative": "根窗口解释（窗口 1 含非静默段 m<=2，需恒等起点）——候选层",
}

# ---------- 3：下窗口预言 ----------
predictions = [
    {"value": 97,  "k": 12, "window": 4,  "bittype": bittype(12), "status": "框架外预言（静默 k=12 相邻双位，窗口常数）"},
    {"value": 385, "k": 48, "window": 6,  "bittype": bittype(48), "status": "框架外预言（静默 k=48 相邻双位，窗口常数）"},
    {"value": 161, "k": 20, "window": "-", "bittype": bittype(20), "status": "新预言（静默 k=20 隔位双位 10100₂——若更高对合域出现应获身份）"},
    {"value": 321, "k": 40, "window": "-", "bittype": bittype(40), "status": "新预言（静默 k=40 隔位双位 101000₂——若更高对合域出现应获身份）"},
]

# ---------- 结论 ----------
conclusion = {
    "verdict": "静默 k 位型→身份族分派规则成立（候选机制，3 位型 3 身份族）：单位位 k→2^m+1 家族（m=p+3，186 重合面，9 兼窗口 1 常数）、相邻双位 k→窗口对合常数（c_2..c_6，189）、隔位双位 k→对合域常数（41 D 分子 + 81 D_9 超对合域——新发现双例）",
    "G": {
        "classification": {t: [i["value"] for i in infos] for t, infos in family_map.items()},
        "family_assign": family_assign,
        "G1_window_const_k": "c_1=9 单位位（根窗口异类）；c_{j>=2} 全部相邻双位 ✓",
        "G2_adjacent_all_window_const": g2,
        "G3_unit_all_2mp1_family": g3,
        "G4_gap_all_fold_domain": g4,
        "note": "位型→身份是'分派规则'而非判别：相邻双位静默单元与窗口常数是同一对象（25/49/193 双投影重合）；隔位双位 2 例（41/81）均带对合域语义——新规律（候选）",
    },
    "H": h_analysis,
    "predictions": predictions,
    "honest_limits": [
        "位型分类 n=13 小样本；隔位型仅 2 例（41/81），'隔位→对合域'为候选规律",
        "单位位静默单元=2^m+1 家族是 186 已证重合的再表述（m>=3）；m=1,2（3,5）非静默（分数 k）",
        "窗口 1 根窗口解释为候选，无独立证据区分四个候选解释",
        "继承 187/188/189 候选层（纯 2 进幂集组织，无 Clifford 特异性）",
    ],
    "next_candidates": [
        "检验 J：分数 k 静默（m=1,2 的 3,5）的位型语义——3=2^0+2^1（相邻双位！）、5=2^0+2^2（隔位！）——截距分子 3/5 是否即'窗口外'的相邻/隔位位型（与窗口常数/D 分子同型但分数化）",
        "检验 K：隔位位型预言 161/321（k=20/40）与 D 族高阶结构（D_9=81 之后）的关联",
        "若框架层扩展：97/385 成为静默 k=12/48 的身份判据",
    ],
}

result = {
    "title": "P7-5e-190 · 静默 k 位型分类 + 窗口异类 + 下窗口预言",
    "date": "2026-10-15",
    "classified": classified,
    "family_assign": family_assign,
    "G_results": {"G1": g1, "G2": g2, "G3": g3, "G4": g4},
    "H": h_analysis,
    "predictions": predictions,
    "conclusion": conclusion,
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

# ---------- 控制台 ----------
print("=" * 72)
print("P7-5e-190 · 静默 k 位型分类 + 窗口异类 + 下窗口预言")
print("=" * 72)
print(f"\n【位型分类】({len(classified)} 个静默单元)")
print(f"{'值':<6}{'k':<5}{'二进制':<10}{'位型':<30}{'身份族'}")
for info in classified:
    fam = family_assign[info["bittype"]]
    print(f"{info['value']:<6}{info['k']:<5}{info['binary']:<10}{info['bittype']:<30}{'; '.join(fam)}")
print()
print("【G 判别】")
print(f"  G1 窗口常数 k（c1=9 单位位根窗口；c_{'{j>=2}'} 全部相邻双位）: {g1}")
print(f"  G2 相邻双位静默单元全部=窗口常数: {g2}  (相邻双位单元: {[i['value'] for i in adjacent_units]})")
print(f"  G3 单位位静默单元全部=2^m+1 家族(m=p+3): {g3}  (单位位单元: {[i['value'] for i in unit_units]})")
print(f"  G4 隔位双位静默单元全部=对合域常数: {g4}  (隔位单元: {[i['value'] for i in gap_units]})")
print(f"  位型→身份族映射:")
for t, fams in family_assign.items():
    print(f"    {t:<30} -> {fams}")
print()
print("【H 窗口 1 异类】")
print(f"  实际 a1=1 -> c1=9（域界/静默 k=1）")
print(f"  公式值 a1=5 -> c1=13（C 分子 13/128！）")
print(f"  候选解释: {h_analysis['candidates'][0]}")
print()
print("【下窗口预言】")
for p in predictions:
    print(f"  {p['value']} (k={p['k']}, {p['bittype']}) — {p['status']}")
print()
print("【结论】", conclusion["verdict"])
print("  位型→身份:", conclusion["G"]["family_assign"])
print("  下一步候选:", conclusion["next_candidates"][0])
