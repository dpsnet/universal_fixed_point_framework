# -*- coding: utf-8 -*-
"""
长7段多井 S1~TOC 线性回归 Bootstrap 置信区间（按井分组）
对应评审建议第 3 点：小样本标定核心 S1 线性公式须补自助回归 CI
数据：
  scripts/data/rockeval_chang7/chang7_rockeval.csv        CY 井（10 样品，零阈值型）
  scripts/data/rockeval_chang7_f75/chang7_f75_rockeval.csv  F75 井（23 样品，Chen 2021）
  scripts/data/rockeval_chang7_n228/chang7_n228_rockeval.csv N228 井（9 样品，崔德艺 2023）
Zhou 2024 表 3 无 TOC 列，不进入 S1-TOC 标定（仅成熟度/窗形支持）。
"""
import csv
import random

random.seed(42)

SOURCES = [
    ("CY井(零阈值)", r'e:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\data\rockeval_chang7\chang7_rockeval.csv'),
    ("F75井", r'e:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\data\rockeval_chang7_f75\chang7_f75_rockeval.csv'),
    ("N228井", r'e:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\data\rockeval_chang7_n228\chang7_n228_rockeval.csv'),
    ("Zhou2024中央区", r'e:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\data\rockeval_chang7_zhou\zhou2024_tbl3.csv'),
    ("Fan2023陇东", r'e:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\data\rockeval_chang7_fan2023\chang7_fan2023_rockeval.csv'),
]


def ols(xs, ys):
    mx = sum(xs) / len(xs)
    my = sum(ys) / len(ys)
    num = sum((xi - mx) * (yi - my) for xi, yi in zip(xs, ys))
    den = sum((xi - mx) ** 2 for xi in xs)
    a = num / den
    b = my - a * mx
    ss_tot = sum((yi - my) ** 2 for yi in ys)
    ss_res = sum((yi - (a * xi + b)) ** 2 for xi, yi in zip(xs, ys))
    r2 = 1 - ss_res / ss_tot
    return a, b, r2


def pct(vals, q):
    s = sorted(vals)
    k = (len(s) - 1) * q
    lo = int(k)
    hi = min(lo + 1, len(s) - 1)
    return s[lo] + (s[hi] - s[lo]) * (k - lo)


def read_ts(path):
    rows = []
    with open(path, encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(r for r in reader if r and not r[0].lstrip().startswith('#'))
        i_t, i_s = header.index('TOC_wt'), header.index('S1_mgg')
        for r in reader:
            if not r or r[0].lstrip().startswith('#'):
                continue
            rows.append((float(r[i_t]), float(r[i_s])))
    return rows


for name, path in SOURCES:
    rows = read_ts(path)
    x = [p[0] for p in rows]
    y = [p[1] for p in rows]
    n = len(x)

    a0, b0, r2_0 = ols(x, y)
    print(f'=== {name}（n={n}） ===')
    print(f'OLS: S1 = {a0:.4f}·TOC + {b0:.4f}  (R² = {r2_0:.4f})')
    if a0 != 0:
        print(f'TOC* = -b/a = {-b0 / a0:.4f}')

    B = 10000
    boot_a, boot_b, boot_toc, boot_r2 = [], [], [], []
    for _ in range(B):
        idx = [random.randrange(n) for _ in range(n)]
        xs = [x[i] for i in idx]
        ys = [y[i] for i in idx]
        try:
            a, b, r2 = ols(xs, ys)
        except ZeroDivisionError:
            continue
        boot_a.append(a)
        boot_b.append(b)
        if a != 0:
            boot_toc.append(-b / a)
        boot_r2.append(r2)

    for label, vals in [('斜率 a', boot_a), ('截距 b', boot_b), ('TOC* (wt%)', boot_toc), ('R²', boot_r2)]:
        print(f'{label}: 中位 {pct(vals, .5):.4f} | 95% CI [{pct(vals, .025):.4f}, {pct(vals, .975):.4f}]')
    print()
