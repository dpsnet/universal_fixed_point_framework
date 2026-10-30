# -*- coding: utf-8 -*-
"""104az-218：跨谱线复合结构唯一性检验
模板：κΛ × (谱线相对频率 f_L) × (框架因子 x) = 16（预言 C，κΛ = 92800/231）。
对氢谱线族 f_L = 1/m²−1/n²，反解 x = 16/(κΛ·f_L) = (231/5800)·m²n²/(n²−m²)。
判定：x 的素因子 ⊆ 扩展素域 {2,3,5,7,11,13,29}（框架量定义）→ "干净"。
若仅 Hγ 一条干净 → 谱线族内宿主唯一性获证；若多条 → 模板不唯一（乱套风险，宿主放弃）。
"""
from fractions import Fraction
from math import gcd

PRIMES = [2, 3, 5, 7, 11, 13, 29]
F16 = Fraction(16, 1)
KAPPA = Fraction(92800, 231)   # κΛ 内生化闭式

def factorize(n):
    """返回素因子集合（正整数）。"""
    fs = set()
    d = 2
    while d * d <= n:
        while n % d == 0:
            fs.add(d)
            n //= d
        d += 1 if d == 2 else 2
        if d > 3 and d % 3 == 0:
            d += 2
    if n > 1:
        fs.add(n)
    return fs

def is_clean(x):
    """素因子 ⊆ 扩展素域。"""
    num, den = x.numerator, x.denominator
    fn, fd = factorize(num), factorize(den)
    return fn.issubset(PRIMES) and fd.issubset(PRIMES), fn, fd

print("κΛ = %s = %s" % (KAPPA, float(KAPPA)), flush=True)
print("模板：κΛ × f_L × x = 16 → x = 16/(κΛ·f_L) = (231/5800)·m²n²/(n²−m²)", flush=True)
print("扩展素域：{2,3,5,7,11,13,29}（框架量 = 素因子子集）", flush=True)
print("", flush=True)

clean_lines = []
for m in range(1, 21):
    for n in range(m + 1, 41):
        f = Fraction(1, m*m) - Fraction(1, n*n)
        x = F16 / (KAPPA * f)
        clean, fn, fd = is_clean(x)
        line = "H(%d→%d)" % (n, m)
        if clean:
            clean_lines.append((m, n, f, x))
            print("✓ 干净：%s  f=%s（%.6f）  x=%s（分子素 %s / 分母素 %s）" % (
                line, f, float(f), x, sorted(fn), sorted(fd)), flush=True)

print("", flush=True)
print("===== 判定 =====", flush=True)
print("氢谱线族（m<20, n≤40）中反解因子 x 为干净框架量的谱线数 = %d" % len(clean_lines), flush=True)
if len(clean_lines) == 1:
    m, n, f, x = clean_lines[0]
    print("唯一性成立：仅 %d→%d 跃迁（f = %s = 21/100，Hγ）——模板在谱线族内唯一干净实例" % (n, m, f), flush=True)
elif len(clean_lines) > 1:
    print("唯一性不成立：多条干净谱线 → 模板不唯一（乱套风险），预言 C 宿主定位在代数侧放弃", flush=True)
else:
    print("零干净谱线（Hγ 自身反解竟不干净？检查素域定义）", flush=True)

# 对照：把 x 的限制放宽到 <0.01% 级的近框架量（排除严格素因子子集，看 Hγ 是否仍特殊）
print("", flush=True)
print("===== 近框架量对照（x ≈ 素域组合，dev ≤ 0.01%）=====", flush=True)
near = []
for m in range(1, 21):
    for n in range(m + 1, 41):
        f = Fraction(1, m*m) - Fraction(1, n*n)
        x = F16 / (KAPPA * f)
        xf = float(x)
        # 素域组合候选：小整数比（分子分母 ≤ 1000，素因子 ⊆ 素域）
        for nd in range(1, 1001):
            for dd in range(1, 1001):
                if gcd(nd, dd) != 1:
                    continue
                c = Fraction(nd, dd)
                clean, fn, fd = is_clean(c)
                if not clean:
                    continue
                dev = abs(float(c) / xf - 1.0)
                if dev <= 1e-4:
                    near.append((m, n, x, c, dev))
                    break
            else:
                continue
            break
near.sort(key=lambda t: t[4])
for m, n, x, c, dev in near[:15]:
    print("H(%d→%d)：x=%s（%.6f）≈ 干净候选 %s（dev %+.2e）" % (n, m, x, float(x), c, dev), flush=True)
