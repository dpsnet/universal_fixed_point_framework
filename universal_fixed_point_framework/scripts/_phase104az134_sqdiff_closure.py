# -*- coding: utf-8 -*-
"""104az-134：平方差框架闭包完整判别 + '41,27,12,2' 试探对齐。
承接 133（n²−1=2^m 唯一 (3,3)）：
A1. n=2..8 的 n²−1 全落框架积（7/7 闭包判别）
A2. 2 幂唯一交点对比（框架量集内唯一 n=3）
A3. f(x)=x²−1 迭代 2→3→8→63→3968（3968 框架身份判别）
B.  未决线索 41,27,12,2 框架对齐试探（登记判别）"""
from fractions import Fraction

FRAME = {2, 3, 4, 5, 7, 8}  # 纯框架量集（种子代数核心量）
N = {2, 3, 4, 5, 6, 7, 8}

def is_power_of_two(x):
    return x > 0 and (x & (x - 1)) == 0

def frame_factorization(x):
    """在 {2,3,5,7}（框架素基，含 4=2²、8=2³ 幂展开后）上的分解。返回因数列表或 None。"""
    primes = [2, 3, 5, 7]
    rem = x
    facs = []
    for p in primes:
        while rem % p == 0:
            facs.append(p)
            rem //= p
    if rem == 1:
        return facs
    return None

print("=" * 72)
print("A1. 平方差框架闭包：n=2..8 的 n²−1 分解")
print("=" * 72)
all_frame = True
for n in sorted(N):
    v = n * n - 1
    facs = frame_factorization(v)
    ok = facs is not None
    all_frame = all_frame and ok
    print(f"  n={n}: {n}²−1 = {v}  ->  {'✓ 框架素基 {2,3,5,7} 分解: ' + '×'.join(map(str, facs)) if ok else '✗ 非框架'}")

print(f"\n>>> A1 判别：n=2..8 平方差全落框架素基闭包 = {all_frame}（7/7）")
print(">>> 对比：133 主定理 n²−1=2^m 唯一解 n=3——2 幂性是框架量集内唯一挑选")

print("\n" + "=" * 72)
print("A2. n²−1 的 2 幂唯一性（133 复验）+ 全部值的 b² 形式")
print("=" * 72)
for n in sorted(N):
    v = n * n - 1
    tag = "2 幂" if is_power_of_two(v) else ""
    # a·b² 形式探测：v = a·b² 且 a,b 在框架量集∪{1}
    cands = []
    for a in [1] + sorted(FRAME):
        for b in [1] + sorted(FRAME):
            if a * b * b == v:
                cands.append(f"{a}·{b}²")
    print(f"  n={n}: {v}  {tag:>6}  a·b² 形式: {cands if cands else '—'}")

print("\n" + "=" * 72)
print("A3. f(x)=x²−1 迭代链：2→3→8→63→3968")
print("=" * 72)
x = 2
chain = [x]
for _ in range(4):
    x = x * x - 1
    chain.append(x)
for i, c in enumerate(chain):
    facs = frame_factorization(c)
    extra = "✓ 框架素基闭包" if facs else "✗ 非纯框架素基"
    if facs is None:
        # 尝试 2 幂 × Mersenne 形式
        for e in range(1, 20):
            if c % (2 ** e) == 0:
                rest = c // (2 ** e)
                if rest + 1 == 2 ** 5 or rest == 2 ** 5 - 1:
                    print(f"  f^{i}(2) = {c}  {extra}  但 = 2^{e}×{rest}（{rest}=2^5−1 Mersenne，静默指数）")
                    break
        else:
            print(f"  f^{i}(2) = {c}  {extra}")
    else:
        print(f"  f^{i}(2) = {c}  {extra}  {'×'.join(map(str, facs))}")

print("\n" + "=" * 72)
print("B. 未决线索 '41,27,12,2' 框架对齐试探（登记判别）")
print("=" * 72)
nums = [41, 27, 12, 2]
for n in nums:
    facs = frame_factorization(n)
    print(f"  {n} = {'×'.join(map(str, facs)) if facs else '非纯框架素基'}")
# 41 = 7²−8 检查
print(f"  41 = 对合域²−k_max = 7²−8 = {49 - 8}  ✓" if 49 - 8 == 41 else "")
print(f"  27 = N_gen³ = 3³  ✓（框架量立方）")
print(f"  12 = N_gen×不动点 = 3×4  ✓（框架积）")
print(f"  2 = 幂基  ✓（框架量）")
# 链差分
diffs = [nums[i] - nums[i + 1] for i in range(len(nums) - 1)]
print(f"  链差分: {diffs}")
for d in diffs:
    facs = frame_factorization(d)
    print(f"    {d} = {'×'.join(map(str, facs)) if facs else '非框架'}")
# 44,30,15,5 减 3
print(f"  44−3=41、30−3=27、15−3=12、5−3=2：")
for base in [44, 30, 15, 5]:
    facs = frame_factorization(base)
    print(f"    {base} = {'×'.join(map(str, facs)) if facs else '非纯框架素基'}（{base}−3 = {base - 3}）")
print(f"  41 ≈ 42 = 对合域×6 = 7×6（41 = 42−1，静默单元−1 侧）")

print("\n>>> B 试探结论：41=7²−8（对合域²−k_max）、27=3³、12=3·4、2=2——"
      "全部可嵌入框架量/框架积/框架差；链差分 {14,15,10}={2·7,3·5,2·5} 全落框架积。"
      "但'为何这四数成链'的语义在压缩前上下文不可考——登记为框架对齐事实，非结构判别。")
