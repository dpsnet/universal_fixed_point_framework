# -*- coding: utf-8 -*-
"""n=6 非零判据联合搜索：找最小因子子集使 A≠0 完全刻画。
判据形式：A≠0 ⟺ (因子子集模式 ∈ 特定集合)。
检验：对 k 因子子集，若每个"因子组合键"内 A 全零或全非零 → 判据成立。
搜索 k=2 全组合、k=3 高信息量组合。
"""
import json, os, random, sys
from collections import defaultdict

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from paperX_single_minus_bg_recursion import A_BG
from paperX_degenerate_family_scan import gen_partial_collinear
from paperX_n6_fullbasis import sg_pattern6_full
from paperX_n6_base12 import BASE12

NAMES = ["s1_23","s12_3","s123_4","s56","s23","s1_234","s34","s12",
         "s345_6","s45_6","s45","s61"]

def cache(n=60000, seed=61):
    rng = random.Random(seed)
    data = []
    for _ in range(n):
        omega, zbar, pairs = gen_partial_collinear(6, 0, r1=True, momentum=True, rng=rng)
        full = sg_pattern6_full(omega, zbar)
        base = tuple(full[i] for i in BASE12)
        data.append((base, round(A_BG(6, omega, zbar), 6)))
    return data

if __name__ == "__main__":
    data = cache(60000)
    # 去重 → 574 模式
    pat_a = {}
    for b, a in data:
        pat_a[b] = a
    print(f"模式: {len(pat_a)}  非零: {sum(1 for a in pat_a.values() if abs(a)>1e-9)}")

    # k=2 全组合搜索
    found2 = []
    for i in range(12):
        for j in range(i+1, 12):
            groups = defaultdict(set)
            for b, a in pat_a.items():
                groups[(b[i], b[j])].add(1 if abs(a) > 1e-9 else 0)
            if all(len(v) == 1 for v in groups.values()):
                found2.append((i, j))
    print(f"2 因子判据: {len(found2)} 个组合")
    for i, j in found2[:20]:
        print(f"  ({NAMES[i]},{NAMES[j]})")

    # k=3 搜索：先测"2 因子失败但 3 因子可能成功"的组合
    # 剪枝：只用 2 因子里最接近判据的组合（信息量最高）扩展
    # 信息量度量：组内非零/零混合度（越少混合越好）
    mixed = []
    for i in range(12):
        for j in range(i+1, 12):
            groups = defaultdict(set)
            for b, a in pat_a.items():
                groups[(b[i], b[j])].add(1 if abs(a) > 1e-9 else 0)
            m = sum(1 for v in groups.values() if len(v) > 1)
            mixed.append((m, i, j))
    mixed.sort()
    print("最接近判据的 2 因子组合（混合组数少 → 好）:")
    for m, i, j in mixed[:10]:
        print(f"  {NAMES[i]},{NAMES[j]}: 混合组 {m}")

    # k=3：对 top 15 个 2 因子组合扩展第三因子
    top_pairs = [(i, j) for _, i, j in mixed[:15]]
    found3 = []
    for i, j in top_pairs:
        for k in range(12):
            if k in (i, j):
                continue
            groups = defaultdict(set)
            for b, a in pat_a.items():
                groups[(b[i], b[j], b[k])].add(1 if abs(a) > 1e-9 else 0)
            if all(len(v) == 1 for v in groups.values()):
                found3.append((i, j, k))
    print(f"3 因子判据（top 15 对扩展）: {len(found3)} 个")
    seen = set()
    for t in found3[:30]:
        if t in seen:
            continue
        seen.add(t)
        print(f"  {[NAMES[x] for x in t]}")

    # 无判据时报告最接近的
    res = {
        "patterns": len(pat_a),
        "nonzero": sum(1 for a in pat_a.values() if abs(a) > 1e-9),
        "found2": [[NAMES[i], NAMES[j]] for i, j in found2],
        "found3": [[NAMES[i] for i in t] for t in found3[:30]],
        "best2_mixed": [{"pair": [NAMES[i], NAMES[j]], "mixed_groups": m} for m, i, j in mixed[:10]],
    }
    with open(os.path.join(SCRIPT_DIR, "paperX_n6_joint_criterion_results.json"), "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=2)
    print("DONE")
