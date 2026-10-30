# -*- coding: utf-8 -*-
"""104az-210 扫描：1124315 分解 → 框架量组合 + 邻域结构 + 交叉锁定素材
规则：v0.4 判据下为"探索性扫描"，全部结果以观察/候选级登记，不升格。
目标：1124315 = 5 × 224863；邻域 224861（用户分解2）、224903（用户分解1）。
"""
import math
from fractions import Fraction

# ---- 框架量集 ----
# M12 主结构 + 扩展素域 {11,13,29}（104az-202）
F = sorted(set([2, 3, 4, 5, 7, 8, 11, 13, 15, 16, 21, 29, 42, 49, 105]))
F_NAME = {2:"幂基−N_gen", 3:"N_gen", 4:"不动点", 5:"幂基/静默(迭代)", 7:"对合域/静默(态并存)",
          8:"k_max", 11:"素域", 13:"素域", 15:"N_gen×幂基", 16:"不动点²", 21:"N_gen×对合域",
          29:"素域", 42:"禁闭域", 49:"对合域²", 105:"N_gen×幂基×对合域"}

def factorize(n):
    """试除法素因子分解（n<1e6 足够）"""
    fac = []
    m = n
    d = 2
    while d * d <= m:
        while m % d == 0:
            fac.append(d)
            m //= d
        d += 1 if d == 2 else 2
    if m > 1:
        fac.append(m)
    return fac

def is_prime(n):
    if n < 2:
        return False
    if n < 4:
        return True
    if n % 2 == 0:
        return False
    d = 3
    while d * d <= n:
        if n % d == 0:
            return False
        d += 2
    return True

print("===== ① 素因子核验 =====", flush=True)
N = 1124315
facN = factorize(N)
print("1124315 = %s" % " × ".join(map(str, facN)), flush=True)
p = N // 5
print("224863 素性：%s（is_prime）" % is_prime(p), flush=True)
print("224861 素性：%s；224903 素性：%s" % (is_prime(224861), is_prime(224903)), flush=True)

print("\n===== ② 用户两次尝试的邻域结构 =====", flush=True)
a1 = 7*19*19*89
a2 = 7*7*13*353
print("用户分解1 5·7·19²·89 = 5×%d = %d（vs 1124315 差 %+d）" % (a1, 5*a1, 5*a1 - N), flush=True)
print("用户分解2 5·7²·13·353 = 5×%d = %d（vs 1124315 差 %+d）" % (a2, 5*a2, 5*a2 - N), flush=True)
print("224861 = %s" % " × ".join(map(str, factorize(224861))), flush=True)
print("224903 = %s" % " × ".join(map(str, factorize(224903))), flush=True)
print("邻域差：224863−224861 = %d（= 幂基−N_gen = 5−3）" % (224863-224861), flush=True)
print("        224903−224863 = %d（= 幂基×k_max = 5×8）" % (224903-224863), flush=True)
print("        224903−224861 = %d（= 禁闭域 42 = 2+40）" % (224903-224861), flush=True)

print("\n===== ③ 224863 的框架量组合 A×B±C 精确表示（A,B,C ∈ F15）=====", flush=True)
hits = []
for A in F:
    for B in F:
        ab = A * B
        for C in F:
            if ab - C == 224863:
                hits.append((A, B, C, "-"))
            if ab + C == 224863:
                hits.append((A, B, C, "+"))
print("命中数：%d" % len(hits), flush=True)
for A, B, C, s in hits[:40]:
    print("  224863 = %d×%d %s %d  →  %s×%s %s %s" % (
        A, B, s, C, F_NAME.get(A, str(A)), F_NAME.get(B, str(B)), s, F_NAME.get(C, str(C))), flush=True)

print("\n===== ④ 224863 的幂±修正表示（A^k ± C 与 A² ± B，A,B,C ∈ F15）=====", flush=True)
pow_hits = []
for A in F:
    for k in range(2, 5):
        ak = A ** k
        if ak > 224863 + 5000:
            continue
        for C in F:
            if ak - C == 224863:
                pow_hits.append((A, k, C, "-"))
            if ak + C == 224863:
                pow_hits.append((A, k, C, "+"))
print("命中数：%d" % len(pow_hits), flush=True)
for A, k, C, s in pow_hits[:20]:
    print("  224863 = %d^%d %s %d" % (A, k, s, C), flush=True)

print("\n===== ⑤ 已登记因子身份对照（交叉锁定素材）=====", flush=True)
idents = {
    353: "幂基×N_gen²×k_max − 对合域 = 5·9·8−7（104az-155，禁闭域 42 家族/DS 禁闭质量弱实例）",
    19:  "静默(5)×不动点 − 1 = 5·4−1（104az-181，g 收缩因子语境）",
    89:  "对合域² + 幂基×k_max = 49+40（新标注，待核）",
    13:  "扩展素域成员（104az-202）",
    7:   "对合域/静默(7)（104az-188/190）",
    49:  "对合域²",
    5:   "幂基/静默(5)（104az-191）",
}
for fac in sorted(set(factorize(224861) + factorize(224903) + [5, 224863])):
    if fac in idents:
        print("  %d：%s" % (fac, idents[fac]), flush=True)
    elif is_prime(fac):
        print("  %d：素数（无已登记框架身份）" % fac, flush=True)
    else:
        print("  %d：合数（%s）" % (fac, " × ".join(map(str, factorize(fac)))), flush=True)
