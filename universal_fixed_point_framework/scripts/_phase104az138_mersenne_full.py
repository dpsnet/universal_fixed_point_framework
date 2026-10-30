# -*- coding: utf-8 -*-
"""104az-138：Mersenne 闭包家族完整判别（137 扩展）。
判别：n=2^p−1 的平方差闭包性 vs 指数 p 的完整谱。
闭包条件：(2^p−1)²−1 = 2^(p+1)·(2^(p−1)−1) ⟺ 2^(p−1)−1 为 7-平滑。
预期：p∈{2,3,4,5,7}（框架量集）时 2^(p−1)−1 ∈ {1,3,7,15,63} 全框架；p=6/8 断裂。"""
FRAME = [2, 3, 5, 7]

def is_smooth(x):
    if x <= 0:
        return False
    for p in FRAME:
        while x % p == 0:
            x //= p
    return x == 1

def factors(x):
    facs = []
    d = 2
    t = x
    while d * d <= t:
        while t % d == 0:
            facs.append(d)
            t //= d
        d += 1
    if t > 1:
        facs.append(t)
    return facs

print("=" * 78)
print("Mersenne 闭包家族完整判别（104az-138，n=2^p−1，p=1..30）")
print("=" * 78)

print("\n① 闭包性全谱：")
closure_ps = []
break_ps = []
for p in range(1, 31):
    n = 2 ** p - 1
    ok = is_smooth(n * n - 1)
    m = 2 ** (p - 1) - 1   # p>=1
    tag = "闭包 ✓" if ok else "断裂 ✗"
    print(f"   p={p:2d}: n=2^{p}-1={n:6d}  2^(p-1)-1={m:6d} ({factors(m) if m > 0 else []})  {tag}")
    if ok:
        closure_ps.append(p)
    else:
        break_ps.append(p)

print(f"\n② 闭包 p 集：{closure_ps}")
print(f"   断裂 p 集（前 10）：{break_ps[:10]}")
print(f"   框架量集 {2, 3, 4, 5, 7} ⊆ 闭包 p 集？ {set(closure_ps) >= {2,3,4,5,7}}")

print("\n③ 完整闭包成员：")
for p in closure_ps:
    n = 2 ** p - 1
    print(f"   n=2^{p}-1={n}: {n}^2-1 = 2^{p+1}*(2^{p-1}-1) = {2**(p+1)}*{2**(p-1)-1} = {n*n-1} ({factors(n*n-1)})")

print("\n④ 判别结论：")
print(f"   n=2^p−1 闭包 ⟺ 2^(p−1)−1 为 7-平滑（等价判别同 137）")
print(f"   闭包 p = {closure_ps} —— 含框架量集 {{2,3,4,5,7}} 全部 5 成员（5/5）")
print(f"   p=6 断裂：2⁵−1=31（31=2⁵−1 自身是 Mersenne，非框架素基）")
print(f"   p=8 断裂：2⁷−1=127（127=2⁷−1 自身是 Mersenne，非框架素基）")
print(f"   二次 Mersenne 链：2^(p−1)−1 ∈ {{1,3,7,15,63}} = {{2^k−1: k∈{{1,2,3,4,6}}}} 全框架")
print("=" * 78)
