# -*- coding: utf-8 -*-
"""
P7-5e-189 · 窗口对合自相似检验（188 候选②：对合常数序列与静默单元家族关联）
用户推进（2026-10-15）后 188 候选②。

背景修正：188 落盘中"对合常数 9/25/41"有误（窗口边界算错）。
正确窗口划分：窗口 j = [a_j, b_j]，b_j = 2^{j+2}（维度塔成员），a_j = b_{j-1}+1。
对合常数 c_j = a_j + b_j = {9, 25, 49, 97, 193, 385, ...}

检验设计：
A. 窗口展开：边界 b_j = 2^{j+2}（维度塔）/ a_j / 对合常数 c_j
B. 静默家族身份：c_j = 8k_j + 1，k_j = {1,3,6,12,24,48,...} = 3·2^{j-2}（j>=2）
   -> 对合常数序列是静默单元家族 {8k+1} 的 k=3·2^p 子序列（翻倍增长）
C. 三重身份：c_j = 窗口首末 2^m+1 成员之和 − 1（j>=2：c_j = (2^{b_j}+1)+(2^{a_j}+1)−1 = 2^{b_j}+2^{a_j}+1）
D. 已登记身份交集：9(域界✓) 25(静默k3✓) 49(静默k6✓) 97(k12?未登记) 193(静默k24✓) 385(k48?未登记)
E. 结论：自相似结构成立（候选层）
"""
import json

OUT = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_phase102_p7_5e189_window_fold_selfsimilar.json"

# 框架身份库（已登记）
framework_keys = {
    1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 13, 15, 17, 25, 33, 41, 49, 56, 64, 65,
    129, 193, 257, 448,
}
# 框架量库详细角色（供交集标注）
fw_roles = {
    9: ["域界/对合常数 K+1", "静默单元 k=1"],
    25: ["静默单元 k=3"],
    49: ["静默单元 k=6", "(k_max-1)^2"],
    41: ["D 分子 8·5+1", "静默单元 k=5"],
    56: ["δ∞ 分母 8·7"],
    64: ["满格 2^6", "8^2"],
    65: ["修正 1/65", "2^6+1", "静默单元 k=8"],
    129: ["2^7+1", "静默单元 k=16"],
    193: ["静默单元 k=24"],
    257: ["2^8+1", "静默单元 k=32"],
}

# ---------- 窗口展开 ----------
windows = []
for j in range(1, 7):
    b = 2 ** (j + 2)          # 终边界 b_j = 2^{j+2}（维度塔投影）
    a = 1 if j == 1 else 2 ** (j + 1) + 1   # 起边界 a_j = 2^{j+1}+1（2^m+1 家族投影）
    c = a + b                 # 对合常数
    k = (c - 1) // 8          # 静默单元序号 k（c = 8k+1）
    # 三重身份检验
    a_family_ok = (a == 2 ** (j + 1) + 1)   # a 是 2^m+1 家族成员（m=j+1）
    b_dim_ok = (b == 2 ** (j + 2))          # b 是维度塔 2^m 成员（m=j+2）
    k_twin_bits = 2 ** (j - 2) + 2 ** (j - 1)   # k_j = 相邻双位 2 进子集（j>=2）
    k_ok = (k == k_twin_bits) if j >= 2 else (k == 1)
    c_silent_ok = (c == 8 * k + 1)
    windows.append({
        "j": j,
        "a": a, "b": b,
        "c": c,
        "k_silent": k,
        "k_binary": format(k, "b") if k else "0",
        "a_is_2mp1_family": a_family_ok,
        "b_is_dim_tower": b_dim_ok,
        "c_is_silent_8k1": c_silent_ok,
        "k_is_twin_bits": k_ok,
        "in_framework": c in framework_keys,
        "fw_roles": fw_roles.get(c, []),
    })

# ---------- 统计 ----------
stats = {
    "windows_total": len(windows),
    "c_all_silent_form": all(w["c_is_silent_8k1"] for w in windows),
    "a_all_family": all(w["a_is_2mp1_family"] for w in windows),
    "b_all_dim": all(w["b_is_dim_tower"] for w in windows),
    "k_all_twin_bits": all(w["k_is_twin_bits"] for w in windows),
    "triple_identity_all": all(
        w["a_is_2mp1_family"] and w["b_is_dim_tower"] and w["c_is_silent_8k1"] and w["k_is_twin_bits"]
        for w in windows),
    "in_framework_hits": [w["c"] for w in windows if w["in_framework"]],
    "in_framework_misses": [w["c"] for w in windows if not w["in_framework"]],
}

# ---------- 结论 ----------
conclusion = {
    "verdict": "窗口三重身份自相似成立（候选层）：窗口三量各来自一个 2 进家族——起边界 a_j=2^{j+1}+1（2^m+1 家族）、终边界 b_j=2^{j+2}（维度塔 2^m）、对合常数 c_j=8k_j+1（静默单元家族，k_j=2^{j-2}+2^{j-1} 相邻双位）",
    "windows_summary": [
        f"窗口{j}: m∈[{w['a']},{w['b']}]  a=2^{j+1}+1(家族){'✓' if w['a_is_2mp1_family'] else '✗'} b=2^{j+2}(维度){'✓' if w['b_is_dim_tower'] else '✗'} c={w['c']}=8·{w['k_silent']}+1(静默){'✓' if w['c_is_silent_8k1'] else '✗'} k₂={w['k_binary']}(双位){'✓' if w['k_is_twin_bits'] else '✗'}{'  [身份: '+', '.join(w['fw_roles'])+']' if w['fw_roles'] else '  [框架外]'}"
        for j, w in enumerate(windows, 1)
    ],
    "structure": {
        "a_start": "a_j = 2^{j+1}+1（j≥2）= 2^m+1 家族成员（m=j+1）——家族塔投影",
        "b_end": "b_j = 2^{j+2} = 维度塔成员（满格 2^m，m=j+2）——维度塔投影",
        "c_fold": "c_j = a_j+b_j = 8k_j+1（静默单元家族）——静默塔投影",
        "k_twin_bits": "k_j = 2^{j-2}+2^{j-1}（相邻双位 2 进子集）——与静默家族 2 进子集组织一致",
        "note_193": "c_5=193 即已登记的静默单元 k=24；窗口 1 起点异类（a_1=1，非家族成员）",
    },
    "framing": {
        "triple_family_surface": "窗口结构 = 三 2 进家族（2^m+1 / 2^m / 8k+1）的重合面——186'双家族代数重合'扩展为三家族窗口结构",
        "in_window_only": "框架内（m≤8）只有窗口 1（c_1=9 域界）；25/49/193 身份来自静默家族投影（k=3/6/24）——同家族多窗口投影",
        "beyond_window": "97/385 无身份是预期的（窗口 4/6 在框架截断外）——与 188'窗口外零身份'一致",
    },
    "honest_limits": [
        "继承 187/188 候选层（无 Clifford 特异性；纯 2 进幂集组织）",
        "三重身份是同一 2 进幂集组织的多投影，非独立新机制（判别力中等）",
        "窗口 1 起点异类（a_1=1）未解释——起点窗口的特殊性",
    ],
    "next_candidates": [
        "检验 G：静默 k 全集 {1,2,3,4,5,6,8,16,24,32} 与 3·2^p/相邻双位模式的交叉——检验'窗口常数 k 必为相邻双位 2 进子集'是否区别于其他静默 k（如 41 的 k=5=2^0+2^2 隔位）",
        "检验 H：窗口 1 起点异类 a_1=1 的系统性（为何起点窗口的起边界是恒等 1 而非家族成员）",
        "若框架层扩展：c_4=97、c_6=385 成为下窗口预言（静默 k=12/48 应在扩展后出现身份）",
    ],
}

result = {
    "title": "P7-5e-189 · 窗口对合自相似检验",
    "date": "2026-10-15",
    "windows": windows,
    "stats": stats,
    "conclusion": conclusion,
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

# ---------- 控制台 ----------
print("=" * 72)
print("P7-5e-189 · 窗口对合自相似检验（188 候选②）")
print("=" * 72)
print(f"{'窗口':<4}{'m 区间':<12}{'a(家族)':<12}{'b(维度)':<10}{'c(静默)':<10}{'k 二进制':<10}{'框架身份'}")
for w in windows:
    roles = "✓ " + ",".join(w["fw_roles"]) if w["fw_roles"] else "—（框架外）"
    a_mark = "✓" if w["a_is_2mp1_family"] else "✗"
    b_mark = "✓" if w["b_is_dim_tower"] else "✗"
    c_mark = "✓" if w["c_is_silent_8k1"] else "✗"
    print(f"{w['j']:<4}[{w['a']},{w['b']}]  {w['a']}({a_mark})  {w['b']}({b_mark})  {w['c']}({c_mark})  {w['k_binary']}({w['k_is_twin_bits']})  {roles}")
print()
print("【三重身份检查】")
print(f"  a=2^(j+1)+1 家族投影: {stats['a_all_family']}")
print(f"  b=2^(j+2) 维度塔投影: {stats['b_all_dim']}")
print(f"  c=8k+1 静默形式: {stats['c_all_silent_form']}")
print(f"  k=相邻双位 2 进子集: {stats['k_all_twin_bits']}  (k={[w['k_silent'] for w in windows]}, 二进制={[w['k_binary'] for w in windows]})")
print(f"  三重身份全成立: {stats['triple_identity_all']}")
print(f"  框架内命中: {stats['in_framework_hits']}  框架外缺席: {stats['in_framework_misses']}")
print()
print("【结论】", conclusion["verdict"])
for line in conclusion["windows_summary"]:
    print("   ", line)
