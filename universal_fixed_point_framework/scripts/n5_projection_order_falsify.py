# -*- coding: utf-8 -*-
"""先证伪：投影序事实 sgn(bk{1,2}{3})=1（模式 A 序假设下）。

按 Lean 定义逐字翻译：
  br i j = w i * w j * (z i - z j)
  bk A B = sum_{i in A} sum_{j in B} br i j
模式 A 投影序（0-based）：z3 < z4 < z1 < z0 < z2
  （即 1-based z̄4 < z̄5 < z̄2 < z̄1 < z̄3）
R1：w1 < 0，w2..w5 > 0（bk{1,2}{3} 只用 w1,w2,w3，均 >0 即可）。
目标：恒 sgn(bk{1,2}{3}) = +1。
"""
import random
import math

def sgn(x):
    if x > 0:
        return 1
    elif x < 0:
        return -1
    else:
        return 0

def br(w, z, i, j):
    return w[i] * w[j] * (z[i] - z[j])

def bk(w, z, A, B):
    return sum(br(w, z, i, j) for i in A for j in B)

def gen_modeA(rng):
    # 投影序（0-based）：z3 < z4 < z1 < z0 < z2，随机间距
    gaps = [rng.uniform(0.1, 3.0) for _ in range(4)]
    z = [0.0] * 5
    z[3] = 0.0
    z[4] = z[3] + gaps[0]
    z[1] = z[4] + gaps[1]
    z[0] = z[1] + gaps[2]
    z[2] = z[0] + gaps[3]
    # R1：w1<0，w2..w5>0
    w = [0.0] * 5
    w[0] = -rng.uniform(0.1, 3.0)
    for i in range(1, 5):
        w[i] = rng.uniform(0.1, 3.0)
    return w, z

def main():
    rng = random.Random(20261001)
    worst = 0
    n = 200000
    viol = 0
    for _ in range(n):
        w, z = gen_modeA(rng)
        v = bk(w, z, {1, 2}, {3})
        s = sgn(v)
        if s != 1:
            viol += 1
            worst = max(worst, abs(v))
    print(f"模式 A：{n} 样本，违反 {viol}，最差偏离 {worst:.3g}")
    assert viol == 0

if __name__ == "__main__":
    main()
