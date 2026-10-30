# -*- coding: utf-8 -*-
"""Phase 103d: 可信样本（剔除 SNR≈0）连续谱基底随 B 单调性量化
回归 blue_calres ~ log10(B) + Spearman 秩相关（纯 Python，无 numpy）
"""
import json, math

P = r'E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_gaia_abs\paperX_wd_absflux_cal.json'
with open(P, encoding='utf-8') as f:
    data = json.load(f)
rows = data['rows']

def clean_rows(rows, min_snr_b=2.0, min_snr_r=2.0):
    """剔除 SNR 无效样本（snr_blue/snr_red 过低或负）"""
    out = []
    for r in rows:
        if r.get('snr_blue') is None or r.get('snr_red') is None:
            continue
        if r['snr_blue'] < min_snr_b or r['snr_red'] < min_snr_r:
            continue
        if 'blue_calres' not in r or r['blue_calres'] is None:
            continue
        v = r['blue_calres']
        if isinstance(v, float) and math.isnan(v):
            continue
        out.append(r)
    return out

def ols(xs, ys):
    """一元 OLS: y = a + b*x；返回 b, a, t_b, r"""
    n = len(xs)
    mx = sum(xs) / n
    my = sum(ys) / n
    sxx = sum((x - mx) ** 2 for x in xs)
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    b = sxy / sxx if sxx > 0 else float('nan')
    a = my - b * mx
    # 残差
    rss = sum((y - (a + b * x)) ** 2 for x, y in zip(xs, ys))
    dof = n - 2
    se_b = math.sqrt(rss / dof / sxx) if dof > 0 and sxx > 0 else float('nan')
    t = b / se_b if se_b and se_b > 0 else float('nan')
    # Pearson r
    syy = sum((y - my) ** 2 for y in ys)
    r = sxy / math.sqrt(sxx * syy) if sxx > 0 and syy > 0 else float('nan')
    return b, a, t, r

def spearman(xs, ys):
    """Spearman 秩相关（处理并列）"""
    def ranks(vals):
        idx = sorted(range(len(vals)), key=lambda i: vals[i])
        rk = [0.0] * len(vals)
        i = 0
        while i < len(idx):
            j = i
            while j + 1 < len(idx) and vals[idx[j + 1]] == vals[idx[i]]:
                j += 1
            avg = (i + j) / 2 + 1
            for k in range(i, j + 1):
                rk[idx[k]] = avg
            i = j + 1
        return rk
    rx, ry = ranks(xs), ranks(ys)
    n = len(xs)
    mx = sum(rx) / n
    my = sum(ry) / n
    sxx = sum((x - mx) ** 2 for x in rx)
    syy = sum((y - my) ** 2 for y in ry)
    sxy = sum((x - mx) * (y - my) for x, y in zip(rx, ry))
    rho = sxy / math.sqrt(sxx * syy) if sxx > 0 and syy > 0 else float('nan')
    # t = rho*sqrt((n-2)/(1-rho^2))
    if abs(rho) >= 1:
        return rho, float('inf')
    t = rho * math.sqrt((n - 2) / (1 - rho * rho))
    return rho, t

print('=== 可信样本定义：snr_blue>=2 且 snr_red>=2（剔除 SNR 无效） ===')
for key, snr_key in [('blue_calres', 'snr_blue'), ('red_calres', 'snr_red'), ('slopeA_calres', 'snr_blue')]:
    rs = clean_rows(rows, 2.0, 2.0)
    xs, ys = [], []
    for r in rs:
        v = r[key]
        if v is None or (isinstance(v, float) and math.isnan(v)):
            continue
        xs.append(math.log10(r['B_MG']))
        ys.append(v)
    b, a, t, pr = ols(xs, ys)
    rho, ts = spearman(xs, ys)
    print('%-14s n=%3d | OLS b=%.4f dex/logB t=%.2f | Pearson r=%.3f | Spearman rho=%.3f t=%.2f'
          % (key, len(xs), b, t, pr, rho, ts))

# 分档中位数（可信样本）
print()
print('=== 可信样本 B 分档中位数 ===')
BINS = [(0, 3), (3, 10), (10, 48), (48, 300)]
BIN_LABELS = ['<3 MG', '3-10', '10-48', '48-300']
rs = clean_rows(rows, 2.0, 2.0)
def median(v):
    sv = sorted(v)
    m = len(sv)
    return sv[m // 2] if m % 2 == 1 else 0.5 * (sv[m // 2 - 1] + sv[m // 2])
for (lo, hi), lab in zip(BINS, BIN_LABELS):
    grp = [r for r in rs if lo <= r['B_MG'] < hi]
    if not grp:
        print('%-8s n=0' % lab)
        continue
    b = median([r['blue_calres'] for r in grp if not (r['blue_calres'] is None or (isinstance(r['blue_calres'], float) and math.isnan(r['blue_calres'])))])
    rd = median([r['red_calres'] for r in grp if not (r['red_calres'] is None or (isinstance(r['red_calres'], float) and math.isnan(r['red_calres'])))])
    print('%-8s n=%2d B[%5.1f-%6.1f] | blue %+.4f | red %+.4f'
          % (lab, len(grp), min(r['B_MG'] for r in grp), max(r['B_MG'] for r in grp), b, rd))

# Teff 10-20kK 子集（排除 Teff 混杂）
print()
print('=== 可信样本 + Teff 10-20kK 子集 ===')
rs2 = [r for r in rs if 10000 <= r['Teff'] < 20000]
for key in ['blue_calres', 'red_calres']:
    xs, ys = [], []
    for r in rs2:
        v = r[key]
        if v is None or (isinstance(v, float) and math.isnan(v)):
            continue
        xs.append(math.log10(r['B_MG']))
        ys.append(v)
    b, a, t, pr = ols(xs, ys)
    rho, ts = spearman(xs, ys)
    print('%-14s n=%3d | OLS b=%.4f dex/logB t=%.2f | Pearson r=%.3f | Spearman rho=%.3f t=%.2f'
          % (key, len(xs), b, t, pr, rho, ts))

# 剔除 50.96/155.79 单颗后中场斜率（检验单调性是否只来自弱场-中场）
print()
print('=== 敏感检查：中场以上样本斜率（B>=10 MG 可信） ===')
rs3 = [r for r in rs if r['B_MG'] >= 10]
for key in ['blue_calres', 'red_calres']:
    xs, ys = [], []
    for r in rs3:
        v = r[key]
        if v is None or (isinstance(v, float) and math.isnan(v)):
            continue
        xs.append(math.log10(r['B_MG']))
        ys.append(v)
    b, a, t, pr = ols(xs, ys)
    rho, ts = spearman(xs, ys)
    print('%-14s n=%3d | OLS b=%.4f dex/logB t=%.2f | Pearson r=%.3f | Spearman rho=%.3f t=%.2f'
          % (key, len(xs), b, t, pr, rho, ts))
