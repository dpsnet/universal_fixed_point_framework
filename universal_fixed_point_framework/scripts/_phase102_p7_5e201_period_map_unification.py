# -*- coding: utf-8 -*-
"""
P7-5e-201 · 周期映射统一与位型连续性判别（200 的检验 DD + EE）
用户推进（2026-10-15）。

检验 DD 设计（Fermat 窗口宽度与周期映射统一）：
DD1. ★ 周期映射族统一：2^{m+2^k}+1 = 2^{2^k}·(2^m+1) - (2^{2^k}-1)
     = b_{2^k-2}·x - (F_k - 2)（缩放 = 窗口终边界 b_{2^k-2}、平移 = Fermat 窗口宽度 F_k-2）
     k=0: 2^{m+1}+1 = 2·(2^m+1) - 1        （平移 1 = F_0-2）
     k=1: 2^{m+2}+1 = 4·(2^m+1) - 3        （平移 3 = F_1-2）
     k=2: 2^{m+4}+1 = 16·(2^m+1) - 15      （平移 15 = F_2-2）
     k=3: 2^{m+8}+1 = 256·(2^m+1) - 255    （平移 255 = F_3-2）——188 的周期映射！
DD2. 缩放因子 2^{2^k} = b_{2^k-2}（b_j = 2^{j+2}：k=3 → b_6=256、k=2 → b_2=16、k=1 → b_0=4）
DD3. 188 映射（k=3）是 Fermat 窗口宽度族的特例——统一成立

检验 EE 设计（合数起边界 k 值位型）：
EE1. 合数起边界 9/33/65/129 静默 k = {1,4,8,16} = 2^{m-3}（m=3,5,6,7）
EE2. 单位位全序列 k = {1,2,4,8,16,32} = 2^{m-3}（m=3..8）——2 进幂连续序列 2^0..2^5
EE3. Fermat 素数位置（m=4,8）k = 2, 32（2 的幂位）
EE4. 65（k=8）与 3265（D(7) 分母 k=408）静默 k 对照
"""
import json

OUT = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_phase102_p7_5e201_period_map_unification.json"

# ---------- DD1：周期映射族统一 ----------
DD1_rows = []
for k in range(0, 4):
    Fk = 2 ** (2 ** k) + 1
    scale = 2 ** (2 ** k)
    shift = 2 ** (2 ** k) - 1  # F_k - 2
    j_b = 2 ** k - 2
    b_j = 2 ** (j_b + 2) if j_b >= 0 else 2 ** (j_b + 2)  # j=-1 -> 2^1 = 2
    # 验证：对 m=1..5，2^{m+2^k}+1 == scale*(2^m+1) - shift
    ok_all = True
    for m in range(1, 6):
        if 2 ** (m + 2 ** k) + 1 != scale * (2 ** m + 1) - shift:
            ok_all = False
    DD1_rows.append({
        "k": k, "F_k": Fk, "scale": scale, "shift": shift,
        "shift_eq_Fk_minus_2": shift == Fk - 2,
        "scale_eq_b": b_j == scale,
        "b_index": j_b, "b_value": b_j,
        "formula": f"2^(m+{2**k})+1 = {scale}·(2^m+1) - {shift}",
        "ok_all_m": ok_all,
    })

# ---------- EE1/EE2/EE3 ----------
EE1_rows = []
for m in range(3, 9):
    fam = 2 ** m + 1
    k_silent = 2 ** (m - 3)
    is_2pow = (m & (m - 1)) == 0
    EE1_rows.append({
        "m": m, "family": fam, "k_silent": k_silent,
        "k_is_2pow": (k_silent & (k_silent - 1)) == 0,
        "m_is_2pow": is_2pow,
    })
EE2 = {
    "unit_k_sequence": [2 ** (m - 3) for m in range(3, 9)],
    "check": "单位位全序列 k = {1,2,4,8,16,32} = 2^{m-3}（m=3..8）——2 进幂连续 2^0..2^5",
}
EE3 = {
    "fermat_positions": [{"m": m, "k": 2 ** (m - 3)} for m in (4, 8)],
    "check": "Fermat 素数位置（m=2 的幂 4,8）k = 2, 32",
}
EE4 = {
    "65_k": 8,
    "D7_3265_k": (3265 - 1) // 8,
    "check": "65 静默 k=8（单位位）；D(7)=3265 分母静默 k=408（非单位位，D(m) k 来自 196 U3: k(m)=m·7·2^(m-4)+2^(m-3)）",
}

# ---------- 结论 ----------
conclusion = {
    "verdict": "DD：★ 周期映射统一——2^{m+2^k}+1 = 2^{2^k}·(2^m+1) − (2^{2^k}−1) = b_{2^k−2}·x − (F_k−2)（k=0..3 全验证）——188 的 k=3 映射（256·x−255）是 Fermat 窗口宽度族的特例：缩放 = 窗口终边界 b_{2^k−2}、平移 = Fermat 窗口宽度 F_k−2。EE：合数起边界静默 k = {1,4,8,16} = 2^{m−3}；单位位全序列 k = {1,2,4,8,16,32} = 2^{m−3}（m=3..8）2 进幂连续；Fermat 素数位置 k = 2,32；65（k=8）与 D(7) 分母（k=408）静默 k 对照",
    "DD": {
        "DD1": "周期映射族统一 k=0..3 全验证（平移 = F_k−2 = Fermat 窗口宽度）",
        "DD2": "缩放 2^{2^k} = b_{2^k−2}（k=3: b_6=256、k=2: b_2=16、k=1: b_0=4）",
        "DD3": "188 映射（k=3）是 Fermat 窗口宽度族特例",
    },
    "EE": {
        "EE1": "合数起边界 k = {1,4,8,16} = 2^{m−3}",
        "EE2": "单位位 k 序列 = 2^{m−3}（m=3..8）2 进幂连续 2^0..2^5",
        "EE3": "Fermat 位置 k = 2, 32（2 的幂位）",
        "EE4": "65 静默 k=8 vs D(7) 分母 k=408",
    },
    "honest_limits": [
        "DD1 的族统一是代数恒等（2^{2^k}·(2^m+1)−(2^{2^k}−1) = 2^{m+2^k}+1），但其'缩放=窗口终边界、平移=Fermat 窗口宽度'的语义指认是候选观察",
        "EE2 的 k 序列 2^{m−3} 是定义恒等（k = (2^m+1−1)/8 = 2^{m−3}）",
        "继承 187-200 候选层",
    ],
    "next_candidates": [
        "检验 FF：周期映射族的'窗口语义'——k=3 映射把窗口 j 送到 j+8（家族 m→m+8），检查 a_j/b_j/c_j 在映射下的行为是否保持位型（窗口平移的框架结构）",
        "检验 GG：F_4 = 65537（m=16）窗口外预言——周期映射 k=4 的平移 65535 = 2^16−1 的框架角色",
        "窗口 2 家族段判据（若框架层扩展）",
    ],
}

result = {
    "title": "P7-5e-201 period-map unification & bit-pattern continuity",
    "date": "2026-10-15",
    "DD1_rows": DD1_rows,
    "EE1_rows": EE1_rows, "EE2": EE2, "EE3": EE3, "EE4": EE4,
    "conclusion": conclusion,
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print("=" * 72)
print("P7-5e-201 period-map unification & bit-pattern continuity")
print("=" * 72)
print("\n[DD1 period-map family unification]")
for r in DD1_rows:
    print(f"  k={r['k']}: {r['formula']}  shift=F_k-2? {r['shift_eq_Fk_minus_2']}  scale=b_{r['b_index']}={r['b_value']}? {r['scale_eq_b']}  all-m ok? {r['ok_all_m']}")
print(f"\n  ★ 统一：2^(m+2^k)+1 = b_{{2^k−2}}·(2^m+1) − (F_k−2)——缩放=窗口终边界、平移=Fermat 窗口宽度")
print(f"\n[EE1 silent k of composite anchors]")
for r in EE1_rows:
    print(f"  m={r['m']}: family={r['family']:<4} k_silent={r['k_silent']:<3} k_is_2pow={r['k_is_2pow']}  m_is_2pow={r['m_is_2pow']}")
print(f"\n[EE2] {EE2['check']}")
print(f"\n[EE3] {EE3['check']}")
print(f"\n[EE4] {EE4['check']}")
print("\n[Conclusion]", conclusion["verdict"])
print("  next:", conclusion["next_candidates"][0])
