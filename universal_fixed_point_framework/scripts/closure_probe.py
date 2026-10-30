# -*- coding: utf-8 -*-
# 最小探针：单模型 orbitCount 计时（诊断卡点）
import time

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

t0 = time.time()
r1 = orbit_count(lambda i: i, 15)
t1 = time.time()
print(f"M1 id: {r1}  ({(t1-t0)*1000:.1f} ms)")

r2 = orbit_count(lambda i: max(0, i - 1), 15)
t2 = time.time()
print(f"M3 conv: {r2}  ({(t2-t1)*1000:.1f} ms)")

# 子集格
def subset_step(i):
    bm = i + 1
    lsb = bm & (-bm)
    if bm == lsb:
        return i
    return (bm & ~lsb) - 1
r3 = orbit_count(subset_step, 15)
t3 = time.time()
print(f"M5 subset: {r3}  ({(t3-t2)*1000:.1f} ms)")

# 链
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
r4 = orbit_count(chain_step, 15)
t4 = time.time()
print(f"M6 chain: {r4}  ({(t4-t3)*1000:.1f} ms)")

r5 = orbit_count(lambda i: 13 if i == 14 else i, 15)
t5 = time.time()
print(f"M7 mix: {r5}  ({(t5-t4)*1000:.1f} ms)")

import random
random.seed(1)
perm = [random.randrange(15) for _ in range(15)]
r6 = orbit_count(lambda i, p=perm: p[i], 15)
t6 = time.time()
print(f"M2 rand(1): {r6}  ({(t6-t5)*1000:.1f} ms)")
