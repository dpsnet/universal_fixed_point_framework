# -*- coding: utf-8 -*-
# 主定理先证伪：orbitCount(S) = card S + fullActiveCount(S)
# 分层静默模型：layer1={0..3}, layer2={4..9}, layer3={10..13}, layer4={14}
# silentStep: x in S -> x (不动)；否则沿层内循环后继
# orbitCount 用真实轨道模拟（每点轨迹直至首次重复，计数不同循环类）
# 2^15 全枚举。
import itertools

N = 15
layered_next = {0:1, 1:2, 2:3, 3:0, 4:5, 5:6, 6:7, 7:8, 8:9, 9:4,
                10:11, 11:12, 12:13, 13:10, 14:14}

def step(S, x):
    if x in S:
        return x
    return layered_next[x]

def orbit_count(S):
    # 周期点：存在 p>=1 使 step^p(x)=x
    per = [False] * N
    for x in range(N):
        p = step(S, x)
        for _ in range(N):
            if p == x:
                per[x] = True
                break
            p = step(S, p)
    # 每个周期点循环类以最小元素为代表
    count = 0
    for x in range(N):
        if not per[x]:
            continue
        orb = set()
        p = x
        for _ in range(N):
            orb.add(p)
            p = step(S, p)
            if p == x:
                break
        if x == min(orb):
            count += 1
    return count

def full_active_count(S):
    layers = [frozenset(range(0, 4)), frozenset(range(4, 10)),
              frozenset(range(10, 14)), frozenset([14])]
    return sum(1 for L in layers if not (set(L) & set(S)))

violations = 0
checked = 0
for bits in range(1 << N):
    S = {i for i in range(N) if (bits >> i) & 1}
    oc = orbit_count(S)
    lhs = oc
    rhs = len(S) + full_active_count(S)
    checked += 1
    if lhs != rhs:
        violations += 1
        if violations <= 5:
            print(f"VIOLATION S={sorted(S)} orbitCount={lhs} card+fullActive={rhs}")
print(f"checked={checked} violations={violations}")
print("PASS" if violations == 0 else "FAIL")
