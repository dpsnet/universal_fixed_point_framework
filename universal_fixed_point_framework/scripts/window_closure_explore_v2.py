# -*- coding: utf-8 -*-
"""候选 D 数值先证伪（v2，修复 orbitCount 周期点判定）：次第闭合模型下 orbitCount 是否出现 15
pyenv 3.11.8 运行。

修复：周期点判定与 Lean periodicPoint 定义一致（∃p>0, step^[p] x = x —— 真周期点，
非"被访问过"；预周期点（进入环但不回自身）必须排除——v1 的 `x in seen` 误判导致
收集环死循环。这是先证伪的重要发现：数值实现必须逐字对齐 Lean 定义。
"""
import random

def orbit_count(step, n):
    """按 PeriodicOrbitCount.lean：周期点 = ∃p>0, step^[p] x = x；
    轨道 = 周期点可达等价类（同一循环）；orbitCount = 商集大小。"""
    periodic = set()
    for x in range(n):
        cur = step(x)
        for _ in range(n):          # 有限状态：n 步内必回（若周期 p ≤ n）
            if cur == x:
                periodic.add(x)
                break
            cur = step(cur)
    classes = []
    for x in sorted(periodic):      # 真周期点：从 x 出发必回 x（收集环安全）
        cyc = set()
        cur = x
        while True:
            cyc.add(cur)
            cur = step(cur)
            if cur == x:
                break
        if not any(cyc == c for c in classes):
            classes.append(cyc)
    return len(classes)

def check_fixed(step, n):
    """对照：不动点数（辅助判读）"""
    return sum(1 for i in range(n) if step(i) == i)

print("候选 D 先证伪（v2 修复版）：次第闭合模型 orbitCount")
print("=" * 70)

r = {}
r["M1 恒等 id"] = orbit_count(lambda i: i, 15)
r["M3 全收敛到0"] = orbit_count(lambda i: max(0, i - 1), 15)

def layer_of(i):
    if i <= 3: return 1
    if i <= 9: return 2
    if i <= 13: return 3
    return 4
layer_rep = {1: 0, 2: 4, 3: 10, 4: 14}
r["M4 层合流"] = orbit_count(lambda i: layer_rep[layer_of(i)], 15)

def subset_step(i):
    bm = i + 1
    lsb = bm & (-bm)
    if bm == lsb:
        return i
    return (bm & ~lsb) - 1
r["M5 子集删除(单元素冻结)"] = orbit_count(subset_step, 15)

def bitcount(bm):
    return bin(bm).count("1")
def rep_for(bm, k):
    bits = [b for b in range(4) if bm & (1 << b)]
    rr = 0
    for b in bits[:k]:
        rr |= (1 << b)
    return rr
def chain_step(i0):
    bm = i0 + 1
    k = bitcount(bm)
    if k == 1:
        return bm - 1
    return rep_for(bm, k - 1) - 1
r["M6 分层冻结链"] = orbit_count(chain_step, 15)

# M7：14 个不动点 + 1 个预周期点（14→13 单向，非振荡——审阅修正：真 2-环模型下
# orbitCount 同为 14，数值结论不变；标注须与实现一致）
r["M7 14不动+1预周期(14→13)"] = orbit_count(lambda i: 13 if i == 14 else i, 15)

for k in [1, 3, 5, 7, 9, 11, 13]:
    r[f"M8 阈值{k}"] = orbit_count(lambda i, kk=k: i if i <= kk else i - 1, 15)

random.seed(20261023)
dists = []
for _ in range(300):
    perm = [random.randrange(15) for _ in range(15)]
    dists.append(orbit_count(lambda i, p=perm: p[i], 15))
mn, med, mx = min(dists), sorted(dists)[len(dists)//2], max(dists)
c15 = sum(1 for d in dists if d == 15)
r["M2 随机(300次)"] = f"min {mn} / med {med} / max {mx} / =15率 {c15/300:.3f}"

# M9：不动点混合周期的一般扫描（15 元集上固定 k 个不动点 + 其余随机，k=1..14）
print("-" * 70)
print("M9 扫描：固定 k 个不动点 + 其余随机（各 100 次）")
for k in [1, 4, 7, 10, 14]:
    dd = []
    for _ in range(100):
        perm = [random.randrange(15) for _ in range(15)]
        for i in range(k):
            perm[i] = i
        dd.append(orbit_count(lambda i, p=perm: p[i], 15))
    print(f"   k={k} 不动点: min {min(dd)} / med {sorted(dd)[50]} / max {max(dd)} / =15率 {sum(1 for d in dd if d==15)/100:.3f}")

for name, val in r.items():
    print(f"{name:<28} → orbitCount = {val}")
