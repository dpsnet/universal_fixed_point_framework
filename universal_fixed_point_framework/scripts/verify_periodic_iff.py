# -*- coding: utf-8 -*-
# verify_periodic_iff.py — 数值先证伪 periodicPoint_iff：
#   periodicPoint(S,x) ↔ x∈S ∨ ∃L∈layers, x∈L ∧ L∩S=∅
import itertools

N = 15
layer1 = {0, 1, 2, 3}
layer2 = {4, 5, 6, 7, 8, 9}
layer3 = {10, 11, 12, 13}
layer4 = {14}
layers = [layer1, layer2, layer3, layer4]


def layered_step(x):
    if x in layer1:
        return 0 if x == 3 else x + 1
    if x in layer2:
        return 4 if x == 9 else x + 1
    if x in layer3:
        return 10 if x == 13 else x + 1
    return 14


def silent_step(S, x):
    return x if x in S else layered_step(x)


def periodic_point(S, x):
    # 存在 p>0, step^p x = x（周期 ≤ N 有界，枚举 1..N+1）
    cur = x
    for p in range(1, N + 2):
        cur = silent_step(S, cur)
        if cur == x:
            return True
    return False


def rhs(S, x):
    if x in S:
        return True
    return any(x in L and not (L & S) for L in layers)


def main():
    bad = 0
    for S_mask in range(1 << N):
        S = {i for i in range(N) if (S_mask >> i) & 1}
        for x in range(N):
            a = periodic_point(S, x)
            b = rhs(S, x)
            if a != b:
                bad += 1
                if bad <= 10:
                    print("MISMATCH S=", sorted(S), "x=", x, "periodic=", a, "rhs=", b)
    print("checked all 2^15 * 15 =", (1 << N) * N, "pairs; mismatches =", bad)
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
