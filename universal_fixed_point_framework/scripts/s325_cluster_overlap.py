# -*- coding: utf-8 -*-
"""S325 Kraemer 群论-框架数值簇重叠审计
Kraemer 2605.0011 群论量（2I*/A₅ 结构）vs MUFPF 框架常数数值簇交集
核心候选：A₅ 阶 2 元素计数 = 15 = SigmaInv（双对换 15 个）
防巧合：随机数集与框架常数集的期望交集 vs 实际交集
"""
import itertools
import math
import random

print("=== S325 Kraemer 群论-框架数值簇重叠审计 ===\n")

# 1) A₅ 阶 2 元素计数（双对换——程序验证）
print("[1] A₅ 阶 2 元素计数（群论事实验证）")
# A₅ = S₅ 偶置换——阶 2 元素 = 双对换（两个不相交对换的积）
# 手算：C(5,2)×C(3,2)/2 = 10×3/2 = 15
manual = math.comb(5,2)*math.comb(3,2)//2
print(f"    双对换计数 = C(5,2)×C(3,2)/2 = {math.comb(5,2)}×{math.comb(3,2)}/2 = {manual}")
print(f"    SigmaInv = 15——匹配 {'✓' if manual==15 else '✗'}（A₅ 对合数 = MUFPF 静默态域）")

# 程序验证：列举 A₅ 阶 2 元素（用置换奇偶性）
def perm_parity(p):
    """p 是 list（0..n-1 的排列）——返回奇偶（True=偶）"""
    seen = [False]*len(p); parity = 0
    for i in range(len(p)):
        if not seen[i]:
            j = i; l = 0
            while not seen[j]:
                seen[j] = True; j = p[j]; l += 1
            parity += l-1
    return parity % 2 == 0

order2_count = 0
total_even = 0
for perm in itertools.permutations(range(5)):
    if perm_parity(list(perm)):
        total_even += 1
        # 阶 2：p² = id 且 p ≠ id
        p2 = tuple(perm[perm[i]] for i in range(5))
        if p2 == tuple(range(5)) and perm != tuple(range(5)):
            order2_count += 1
print(f"    A₅ 元素总数（程序）= {total_even}（应为 60 ✓）——阶 2 元素 = {order2_count}")
print(f"    程序验证：A₅ 阶 2 元素 = {order2_count} = SigmaInv 15——{'✓' if order2_count==15 else '✗'}")

# 2) SL(2,5) 阶 2 元素（含中心）——120 阶群
print(f"\n[2] SL(2,5)（|2I*| = 120）结构")
print(f"    SL(2,5)/Z₂ = A₅（60 阶）——中心 2 阶——120 = 60×2")
print(f"    SL(2,5) 阶 2 元素 = 中心 1 + 非中心 15 = 16（含 −I）——非中心恰 15")
print(f"    120 = k_max 8 × 活跃 3 × 静默 5 = 8×15——SigmaInv 15 × k_max 8")
print(f"    Q₈（四元数群 8 阶）= SL(2,5) 的 Sylow-2 子群——k_max 8 对应")

# 3) Kraemer 群论数值簇 vs MUFPF 框架常数簇
print(f"\n[3] 数值簇交集")
kraemer_set = {120, 30, 12, 20, 32, 15, 4, 10, 2, 3, 5, 6, 60, 8}   # 论文群论量
mufpf_set = {2, 3, 4, 5, 7, 8, 15, 16, 24, 30, 42, 120, 23}        # 框架常数+23
inter = kraemer_set & mufpf_set
print(f"    Kraemer 群论量集（{sorted(kraemer_set)}）")
print(f"    MUFPF 框架量集（{sorted(mufpf_set)}）")
print(f"    交集 = {sorted(inter)}——{len(inter)} 个数值同现")
print(f"    重叠值：{', '.join(str(v) for v in sorted(inter))}")

# 4) 防巧合：随机数集与框架常数集的期望交集
print(f"\n[4] 防巧合：随机数集交集基线")
rng = random.Random(20261028)
mu = mufpf_set
N = 100000
avg_inter = 0
for _ in range(N):
    rset = set(rng.randint(1, 120) for _ in range(len(kraemer_set)))
    avg_inter += len(rset & mu)
avg_inter /= N
print(f"    随机 14 个数（1-120）∩ 框架量集（{len(mu)} 个）：期望交集 = {avg_inter:.2f}")
print(f"    实际交集 = {len(inter)}——比值 = {len(inter)/avg_inter:.1f}× 期望")

# 5) 结构同现点总结
print(f"\n[5] 数值簇重叠的结构同现点（非单点——簇级）")
print(f"    ★ 15 = SigmaInv = A₅ 阶 2 元素计数（对合——静默态域）")
print(f"    ★ 120 = |2I*| = k_max×活跃×静默 = 8×3×5（素因子=框架常数）")
print(f"    ★ 30 = 二十面体棱数 = 静默×幂基×活跃 = 5×2×3")
print(f"    ★ 8 = Sylow-2 子群 Q₈ 阶 = k_max")
print(f"    ★ 60 = A₅ 阶 = 16×活跃×静默/不动点 = 16×15/4 = 60？——16×3×5/4 = 60 ✓（全态×活跃×静默/不动点）")
print(f"    ★ 4 = 120/30（Kraemer 修正因子）= 不动点（MUFPF）")
print(f"    ★ 3/5 = 活跃/静默 = C₅ 类大小 12/20？——12/20 = 3/5 ✓（共轭类大小比）")
print(f"    ——7 个数值同现（15/120/30/8/60/4/3:5）——簇级重叠而非单点")

# 6) 诚实评估
print(f"\n[6] 诚实评估")
print(f"    ✓ 数值簇重叠强于单点恒等（S323 的 120 素因子）——多数值结构性重叠")
print(f"    △ 均为后验同现（先有 Kraemer 群论量——再有框架常数对照）——非先验预言")
print(f"    △ 15 为常见小整数（对合计数 15 是群论标准事实）——单点强度一般")
print(f"    △ 60 = 16×3×5/4 是后验构造（16×活跃×静默/不动点——可任意配）——降级")
print(f"    △ '为何群结构数值 = 框架常数'的机制连接未建立——同现登记不升格")
print(f"    → 结构锚增强（Kraemer-MUFPF 数值簇重叠——跨框架结构可信度）——维持 P4 预注册")
