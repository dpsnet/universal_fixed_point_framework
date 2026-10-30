# -*- coding: utf-8 -*-
"""候选 D 数值先证伪（精简版，纯标准库）：次第闭合模型下 orbitCount 是否出现 15
pyenv 3.11.8 运行。orbitCount 按 PeriodicOrbitCount.lean 定义（周期点可达等价类计数）。"""
import random
from math import comb

def orbit_count(step, n):
    periodic = set()
    for x in range(n):
        seen = set()
        cur = x
        while cur not in seen:
            seen.add(cur)
            cur = step(cur)
        if x in seen:
            periodic.add(x)
    classes = []
    for x in sorted(periodic):
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

print("候选 D 先证伪（精简版）：次第闭合模型 orbitCount")
print("=" * 70)

r = {}
r["M1 恒等 id"] = orbit_count(lambda i: i, 15)
r["M3 全收敛到0"] = orbit_count(lambda i: max(0, i - 1), 15)

# M4 层合流（子集尺度 {1,2,3,4} → 层代表 0/4/10/14）
def layer_of(i):
    if i <= 3: return 1
    if i <= 9: return 2
    if i <= 13: return 3
    return 4
layer_rep = {1: 0, 2: 4, 3: 10, 4: 14}
r["M4 层合流"] = orbit_count(lambda i: layer_rep[layer_of(i)], 15)

# M5 子集格删除：S → S∖{最小元素}；单元素 = 不动点
def subset_step(i):
    bm = i + 1
    lsb = bm & (-bm)
    if bm == lsb:
        return i
    return (bm & ~lsb) - 1
r["M5 子集删除"] = orbit_count(subset_step, 15)

# M6 分层冻结链：|S|=k → 最小 k-1 位代表；|S|=1 冻结
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

# M7 14 不动点 + 1 个 2-周期（构造）
r["M7 14不动+1振荡"] = orbit_count(lambda i: 13 if i == 14 else i, 15)

# M8 阈值收敛
for k in [1, 3, 5, 7, 9, 11, 13]:
    r[f"M8 阈值{k}"] = orbit_count(lambda i, kk=k: i if i <= kk else i - 1, 15)

# M2 随机（小样本 300 次，固定种子）
random.seed(20261023)
dists = []
for _ in range(300):
    perm = [random.randrange(15) for _ in range(15)]
    dists.append(orbit_count(lambda i, p=perm: p[i], 15))
mn, med, mx = min(dists), sorted(dists)[len(dists)//2], max(dists)
c15 = sum(1 for d in dists if d == 15)
r["M2 随机(300次)"] = f"min {mn} / med {med} / max {mx} / =15率 {c15/300:.3f}"

for name, val in r.items():
    print(f"{name:<22} → orbitCount = {val}")
