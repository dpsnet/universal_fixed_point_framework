# -*- coding: utf-8 -*-
"""104az-137：平方差闭包结构定理判别（135 谱升级）。
判别 1：闭包 ⟺ (n−1)、(n+1) 均 7-平滑（等价判别，n≤512 全验证）。
判别 2：7-平滑偶数连续段结构——22 是第一个非 7-平滑偶数（11 是第一个 >7 质数）
        ——解释 [2,9] 连续段与奇数 3..19 段的来源。
判别 3：新成员身份（n=71 → 5040=7!、+1 家族扩展）。"""
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

N_MAX = 512
print("=" * 78)
print("平方差闭包结构定理判别（104az-137，n≤512）")
print("=" * 78)

# ① 等价判别：闭包 ⟺ (n−1),(n+1) 均 7-平滑
equiv_fail = []
closure_ns = []
for n in range(2, N_MAX + 1):
    ok = is_smooth(n * n - 1)
    ok2 = is_smooth(n - 1) and is_smooth(n + 1)
    if ok != ok2:
        equiv_fail.append((n, ok, ok2))
    if ok:
        closure_ns.append(n)
print(f"① 等价判别（n=2..{N_MAX}）：闭包 ⟺ (n−1),(n+1) 均 7-平滑 —— 反例数 = {len(equiv_fail)}")
if equiv_fail:
    for e in equiv_fail[:10]:
        print(f"   反例: n={e[0]} closure={e[1]} pair={e[2]}")
else:
    print("   ✓ 全一致（等价判别成立）")

# ② 闭包 n 序列
print(f"\n② 闭包 n（n=2..{N_MAX}）：")
print(f"   {closure_ns}")
# 连续段
segs = []
start = None
prev = None
for n in closure_ns:
    if start is None:
        start = n; prev = n
    elif n == prev + 1:
        prev = n
    else:
        segs.append((start, prev))
        start = n; prev = n
if start is not None:
    segs.append((start, prev))
print(f"   连续段：{segs}")
print(f"   最长连续段 = {max(segs, key=lambda s: s[1]-s[0])}")

# ③ 7-平滑偶数序列与断裂
print(f"\n③ 7-平滑偶数（2..512）：")
smooth_evens = [e for e in range(2, N_MAX + 1, 2) if is_smooth(e)]
print(f"   {smooth_evens[:60]}{'...' if len(smooth_evens) > 60 else ''}（共 {len(smooth_evens)} 个）")
nonsmooth_evens = [e for e in range(2, 200, 2) if not is_smooth(e)]
print(f"   首个非 7-平滑偶数：{nonsmooth_evens[0]} = {nonsmooth_evens[0]} = 2×11（11 = 第一个 >7 的质数）")
print(f"   前 10 个非 7-平滑偶数：{nonsmooth_evens[:10]}")

# ④ 新成员身份：n=71
print(f"\n④ 新成员身份：")
print(f"   n=71: 71²−1 = 5040 = {factors(5040)}")
print(f"   5040 = 7! = 对合域！= 2⁴·3²·5·7 ✓ 全框架（5040 为 Plato 理想城邦人口数）")
print(f"   n=71 = 2·5·7+1 = 幂基×静默×对合域+1（框架三积 +1 家族新成员）")
# 其他新成员
new_members = [n for n in closure_ns if n > 64]
print(f"   n>64 闭包新成员：{new_members}")
for n in new_members:
    v = n * n - 1
    print(f"     n={n}: {n}²−1={v} = {factors(v)}")

# ⑤ +1/−1 家族扩展（闭包 n 的 n−1 或 n+1 为框架积）
print(f"\n⑤ 闭包 n 的 ±1 家族（n−1 或 n+1 为纯框架积/幂）：")
for n in closure_ns:
    if n > 64:
        print(f"   n={n}: n−1={n-1} ({factors(n-1)}) n+1={n+1} ({factors(n+1)})")

print("\n" + "=" * 78)
print("判别结论：闭包 ⟺ 相邻对 7-平滑（等价判别成立）；22=2·11 是第一个")
print("非 7-平滑偶数 ⟹ [2,9] 段与奇数 3..19 段由 '11 是第一个 >7 质数' 驱动；")
print("n=71 → 5040=7! 新发现（对合域阶乘，全框架）。")
print("=" * 78)
