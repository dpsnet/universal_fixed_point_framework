# -*- coding: utf-8 -*-
"""Phase 103b: §4.8 带结构 B 分档判别检验（calres 字段）
判别：RWA（宽带平滑增强） vs 转移假说（B_ion 阈值阶梯/窗口结构）
口径：与 _phase86_r3_conservation.py 一致（blue_calres 等 k_g 校准后残差）
"""
import json, math

P = r'E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_gaia_abs\paperX_wd_absflux_cal.json'

with open(P, encoding='utf-8') as f:
    data = json.load(f)
rows = data['rows']

# 字段确认
print('字段样例 keys:', sorted(rows[0].keys()))
KEYS = ['blue_calres', 'red_calres', 'slopeA_calres', 'slopeB_calres']

def clean(rows, cond, key):
    out = []
    for r in rows:
        if cond(r) and key in r and r[key] is not None:
            v = r[key]
            if isinstance(v, float) and math.isnan(v):
                continue
            out.append(v)
    return out

def mean(v):
    return sum(v) / len(v) if v else None

def median(v):
    sv = sorted(v)
    m = len(sv)
    if m == 0:
        return None
    if m % 2 == 1:
        return sv[m // 2]
    return 0.5 * (sv[m // 2 - 1] + sv[m // 2])

# ---- 1) 复现论文口径（10-20kK 主档，mean 差，Welch t + bootstrap CI）----
print()
print('=== 1) 复现论文口径：10-20kK 主档 弱场(<10) vs 中场(10-100)，mean 差 ===')
for key in KEYS:
    w = clean(rows, lambda r: r['B_MG'] < 10 and 10000 <= r['Teff'] < 20000, key)
    m = clean(rows, lambda r: 10 <= r['B_MG'] < 100 and 10000 <= r['Teff'] < 20000, key)
    if not w or not m:
        print('%-14s n_w=%d n_m=%d (跳过)' % (key, len(w), len(m)))
        continue
    dw, dm = mean(w), mean(m)
    d = dm - dw
    # Welch t
    import math as _m
    vw = sum((x - dw) ** 2 for x in w) / (len(w) - 1)
    vm = sum((x - dm) ** 2 for x in m) / (len(m) - 1)
    se = _m.sqrt(vw / len(w) + vm / len(m))
    t = d / se if se > 0 else float('inf')
    print('%-14s 弱场 n=%2d mean %+.4f | 中场 n=%2d mean %+.4f | 差 %+.4f | t=%.2f'
          % (key, len(w), dw, len(m), dm, d, t))

# ---- 2) B 分档（calres 中位数）----
print()
print('=== 2) B 分档：四带 calres 中位数（全 91 颗） ===')
BINS = [(0, 10), (10, 48), (48, 100), (100, 250), (250, 1e9)]
BIN_LABELS = ['<10 MG', '10-48', '48-100', '100-250', '>250 MG']
print('%-8s %5s | %8s %8s %8s %8s' % ('bin', 'n', 'blue', 'red', 'slopeA', 'slopeB'))
for (lo, hi), lab in zip(BINS, BIN_LABELS):
    grp = [r for r in rows if lo <= r['B_MG'] < hi]
    if not grp:
        print('%-8s %5d | %8s %8s %8s %8s' % (lab, 0, '-', '-', '-', '-'))
        continue
    vals = [median(clean(grp, lambda r: True, k)) for k in KEYS]
    print('%-8s %5d | %8s %8s %8s %8s'
          % (lab, len(grp), *['%.4f' % v if v is not None else '-' for v in vals]))

# ---- 3) B_ion 阈值邻域（转移假说检验）----
print()
print('=== 3) B_ion 阈值邻域：blue/red calres 中位数（半档-1.5档） ===')
for thr in [48, 65, 94, 147]:
    lo_grp = [r for r in rows if thr * 0.5 <= r['B_MG'] < thr]
    hi_grp = [r for r in rows if thr <= r['B_MG'] < thr * 1.5]
    def agg(g, key):
        v = median([r[key] for r in g if key in r and r[key] is not None])
        return ('%.4f' % v) if v is not None else '-'
    print('thr %3d | below[%4.0f-%3.0f] n=%2d blue=%s red=%s | above[%3.0f-%4.0f] n=%2d blue=%s red=%s'
          % (thr, thr * 0.5, thr, len(lo_grp), agg(lo_grp, 'blue_calres'), agg(lo_grp, 'red_calres'),
             thr, thr * 1.5, len(hi_grp), agg(hi_grp, 'blue_calres'), agg(hi_grp, 'red_calres')))

# ---- 4) 排序趋势（RWA 单调 vs 转移阶梯）----
print()
print('=== 4) 按 B 排序 10 颗一组（calres 中位数） ===')
srt = sorted(rows, key=lambda r: r['B_MG'])
for i in range(0, len(srt), 10):
    grp = srt[i:i + 10]
    def med(key):
        v = median([r[key] for r in grp if key in r and r[key] is not None])
        return ('%+.4f' % v) if v is not None else '-'
    print('B[%6.2f-%6.2f] n=%2d | blue %s | red %s | slopeA %s'
          % (grp[0]['B_MG'], grp[-1]['B_MG'], len(grp), med('blue_calres'), med('red_calres'), med('slopeA_calres')))

# ---- 5) Teff 10-20kK 内 B 分档（排除 Teff 混杂）----
print()
print('=== 5) Teff 10-20kK 内 B 分档（calres 中位数） ===')
for (lo, hi), lab in zip(BINS, BIN_LABELS):
    grp = [r for r in rows if lo <= r['B_MG'] < hi and 10000 <= r['Teff'] < 20000]
    if not grp:
        print('%-8s n=0' % lab)
        continue
    def med(key):
        v = median([r[key] for r in grp if key in r and r[key] is not None])
        return ('%+.4f' % v) if v is not None else '-'
    print('%-8s n=%2d B[%5.1f-%5.1f] | blue %s | red %s | slopeA %s'
          % (lab, len(grp), min(r['B_MG'] for r in grp), max(r['B_MG'] for r in grp),
             med('blue_calres'), med('red_calres'), med('slopeA_calres')))
