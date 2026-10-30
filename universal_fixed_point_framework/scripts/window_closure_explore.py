# -*- coding: utf-8 -*-
"""候选 D 数值先证伪：次第闭合模型下 orbitCount 是否自然出现 15（2026-10-23）
pyenv 3.11.8 运行。

orbitCount 按 PeriodicOrbitCount.lean 定义逐字翻译：
  周期点 = 存在 p>0 使 step^[p] x = x；
  轨道   = 周期点"前向可达"等价类（同一循环）；
  orbitCount = 商集大小。

模型矩阵（15 窗口 / 16 组合的次第闭合实现）：
  M1 恒等 id：每窗口自身不动点（基线，orbitCount=15 平凡）
  M2 随机自映射 × 2000 次：一般分布（对照）
  M3 全收敛：i → max(0, i−1)（全合流到 0）
  M4 层合流：窗口按子集尺度 {4,6,4,1} 合流到层代表（单→0/双层→4/三层→10/四层→14）
  M5 子集格删除：非空子集 S → S∖{最小元素}（单元素=不动点）→ 4 个不动点
  M6 分层冻结链：单层冻结到自身、双层→单层代表、三层→双层代表、四层→三层代表
  M7 部分冻结+振荡：14 不动点 + 1 个 2-周期（构造性看是否"自然"）
  M8 阈值收敛：窗口 i → 冻结阈值 k 以下者自身、以上者递减（k 扫描 1..14）
判据：15 是否在**非平凡**模型（非 M1/M7 构造）中自然出现。
"""
import numpy as np
from math import comb

def orbit_count(step, n):
    """按 Lean 定义：周期点集上的可达等价类计数（同一循环 = 一条轨道）"""
    periodic = set()
    for x in range(n):
        seen = set()
        cur = x
        while cur not in seen:
            seen.add(cur)
            cur = step(cur)
        if x in seen:          # x 在其自身轨迹的环上 ⟹ 周期点
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

def scaled_orbit_count(step, n):
    """同定义但按 '同一循环' 去重（等价：用可达性）
    实际上 orbit_count 已实现；此函数保留签名一致性。"""
    return orbit_count(step, n)

print("候选 D 数值先证伪：次第闭合模型 orbitCount 统计")
print("=" * 78)

results = {}

# M1 恒等
step1 = lambda i: i
results["M1 恒等 id"] = orbit_count(step1, 15)

# M2 随机
rng = np.random.default_rng(20261023)
dists = []
for _ in range(2000):
    perm = rng.integers(0, 15, 15)
    dists.append(orbit_count(lambda i, p=perm: int(p[i]), 15))
dists = np.array(dists)
results["M2 随机(2000次)"] = f"min {dists.min()} / med {np.median(dists):.0f} / max {dists.max()} / 含15率 {(dists==15).mean():.3f}"

# M3 全收敛 i→max(0,i-1)
step3 = lambda i: max(0, i - 1)
results["M3 全收敛到0"] = orbit_count(step3, 15)

# M4 层合流（子集尺度 {1,2,3,4} → 层代表 0/4/10/14）
# 窗口 0..3 = 单元素(尺度1)，4..9 = 双元素(2)，10..13 = 三元素(3)，14 = 四元素(4)
layer_rep = {s: r for s, r in [(1, 0), (2, 4), (3, 10), (4, 14)]}
def layer_of(i):
    if i <= 3: return 1
    if i <= 9: return 2
    if i <= 13: return 3
    return 4
step4 = lambda i: layer_rep[layer_of(i)]
results["M4 层合流(层代表不动点)"] = orbit_count(step4, 15)

# M5 子集格删除：S → S∖{最小元素}；单元素 = 不动点
# 编码：非空子集 S ⊆ {0,1,2,3}；编号 i ↔ 位图（0..14 = 1..15 位图-1？）
# 位图 0 为空集（排除）；编号 i 的位图 = i+1
def subset_step(i):
    bm = i + 1           # 位图（1..15）
    # 找最小设置位
    lsb = bm & (-bm)
    if bm == lsb:        # 单元素 = 不动点（冻结）
        return i
    return (bm & ~lsb) - 1  # 删最小位
results["M5 子集格删除(单元素冻结)"] = orbit_count(subset_step, 15)

# M6 分层冻结链：单层冻结自身；双层→单层代表；三层→双层代表；四层→三层代表
# 层代表：单层 0(1), 双层 4(10b=2,3?)，用位图：单层=1,2,4,8；双层=3,5,9,6,10,12；
# 三层=7,11,13,14；四层=15。
# 链：|S|=4 → |S|=3 代表；|S|=3 → |S|=2 代表；|S|=2 → |S|=1 代表；|S|=1 → 自身
def bitcount(bm):
    return bin(bm).count("1")
def rep_for(bm, k):
    """位图 bm 的代表：含 bm 的最小 k 位图（若 bm 有 k 位则自身）"""
    if bitcount(bm) == k:
        return bm
    # 取 bm 的最小 k 位
    bits = [b for b in range(4) if bm & (1 << b)]
    r = 0
    for b in bits[:k]:
        r |= (1 << b)
    return r
def chain_step(bm0):
    bm = bm0 + 1
    k = bitcount(bm)
    if k == 1:
        return bm - 1          # 冻结（不动点）
    # 推进到下一层代表（k-1 位）
    return rep_for(bm, k - 1) - 1
results["M6 分层冻结链(逐层收敛)"] = orbit_count(chain_step, 15)

# M7 部分冻结+振荡：14 不动点 + 1 个 2-周期
def mix_step(i):
    if i == 14:
        return 13             # 14↔13 振荡（2-周期）
    return i                  # 其余不动点
results["M7 14不动+1振荡(构造)"] = orbit_count(mix_step, 15)

# M8 阈值收敛：k 以下自身、以上递减
for k in [1, 3, 5, 7, 9, 11, 13]:
    step8 = lambda i, kk=k: i if i <= kk else i - 1
    results[f"M8 阈值k={k}收敛"] = orbit_count(step8, 15)

for name, val in results.items():
    print(f"{name:<32} → orbitCount = {val}")
