# -*- coding: utf-8 -*-
"""chain_audit_192b_generator_scan.py — 104az-193 判别前置：{1,3,5,7} 子集闭包生成集唯一性扫描

口径（严格、可复核）：
- 候选集合：所有 4 元子集 S ⊂ [1,16]（C(16,4) = 1820 个），元素互异。
- 框架量表 FW = 104az 登记中明确出现的框架量整数（保守，不扩张到乘法闭包——
  扩张会让"任何积 = 两框架量乘积"平凡化，失去判别力）。
- 和闭包：15 个非空子集和 ∈ FW_SUM（值 ≤ 64 的框架量 + 大框架量）。
- 积闭包：15 个非空子集积 ∈ FW。
- 联合闭包 = 和闭包 ∧ 积闭包。
- 输出：联合闭包集合全集 + 各候选未命中明细 + {1,3,5,7} 判定。
"""
import io, sys, itertools
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

# 框架量表（来源：RESEARCH_STATE 104az 登记明确身份值）
FW = {
    # 基础框架常数
    1, 2, 3, 4, 5, 7, 8, 9, 15, 16, 21, 31, 35, 42,
    56, 60, 61, 63, 64, 65, 105, 125, 210, 253, 320, 675, 729, 1000,
    # 104az-192 组合恒等（幂基×N_gen 等）：6,10,11,12,13,14
    6, 10, 11, 12, 13, 14,
}
FW_SUM = {v for v in FW if v <= 64} | {105, 125, 210, 253, 320, 675, 729}

def subsets(s):
    n = len(s)
    for r in range(1, n + 1):
        for c in itertools.combinations(s, r):
            yield c

def sums_and_prods(s):
    ss, pp = [], []
    for c in subsets(s):
        sm = sum(c)
        pr = 1
        for x in c:
            pr *= x
        ss.append(sm)
        pp.append(pr)
    return ss, pp

results = []      # (集合, 和未命中, 积未命中)
joint_closed = [] # 联合闭包
sum_closed_only = []
for s in itertools.combinations(range(1, 17), 4):
    ss, pp = sums_and_prods(s)
    bad_s = sorted({v for v in ss if v not in FW_SUM})
    bad_p = sorted({v for v in pp if v not in FW})
    sum_ok = len(bad_s) == 0
    prod_ok = len(bad_p) == 0
    if sum_ok and prod_ok:
        joint_closed.append(s)
    elif sum_ok:
        sum_closed_only.append(s)
    results.append((s, bad_s, bad_p))

print("=== 104az-193 生成集唯一性扫描（4 元子集 ⊂ [1,16]，C(16,4) = 1820）===")
print(f"\nFW 表大小 = {len(FW)}：{sorted(FW)}")
print(f"FW_SUM = {sorted(FW_SUM)}")

print(f"\n[1] 联合闭包（和∧积全部落框架量）集合数 = {len(joint_closed)}")
for s in joint_closed:
    ss, pp = sums_and_prods(s)
    print(f"    {s}  和谱={sorted(set(ss))}  积谱={sorted(set(pp))}")

print(f"\n[2] 仅和闭包（积有未命中）集合数 = {len(sum_closed_only)}")
for s in sum_closed_only[:20]:
    ss, pp = sums_and_prods(s)
    bad_p = sorted({v for v in pp if v not in FW})
    print(f"    {s}  积未命中={bad_p}")

target = (1, 3, 5, 7)
print(f"\n[3] 目标 {target} 判定：")
if target in joint_closed:
    print("    在联合闭包集合中 ✓")
else:
    print("    ⚠ 不在联合闭包集合中（口径问题？）")
    for s, b1, b2 in results:
        if set(s) == set(target):
            print(f"    未命中：和={b1} 积={b2}")

# 按未命中数排序的最接近闭包集合（前 15）
ranked = sorted(results, key=lambda r: len(r[1]) + len(r[2]))
print(f"\n[4] 最接近闭包的前 15 候选（未命中数升序）：")
for s, b1, b2 in ranked[:15]:
    print(f"    {s}  和未命中 {len(b1)} 个 {b1}；积未命中 {len(b2)} 个 {b2}")

print("\n=== 扫描完成 ===")
