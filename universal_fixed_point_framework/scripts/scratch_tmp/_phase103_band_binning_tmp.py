# -*- coding: utf-8 -*-
"""Phase 103: §4.8 带结构 B 分档判别检验（临时分析脚本）
判别：RWA（宽带平滑增强） vs 转移假说（B_ion 阈值处阶梯/窗口结构）
数据：scripts/_gaia_abs/paperX_wd_absflux_cal.json（91 颗，k_g 校准版）
"""
import json

P = r'E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_gaia_abs\paperX_wd_absflux_cal.json'

with open(P, encoding='utf-8') as f:
    data = json.load(f)
rows = data['rows']

Bs = sorted(r['B_MG'] for r in rows)
print('n =', len(rows))
print('B min/max =', round(Bs[0], 4), '/', round(Bs[-1], 2))

def pct(q):
    return Bs[int(q * (len(Bs) - 1))]

print('B p25/p50/p75 =', round(pct(0.25), 2), round(pct(0.5), 2), round(pct(0.75), 2))
print('B<1MG:', sum(1 for b in Bs if b < 1))
print('1-10MG:', sum(1 for b in Bs if 1 <= b < 10))
print('10-48MG:', sum(1 for b in Bs if 10 <= b < 48))
print('48-100MG:', sum(1 for b in Bs if 48 <= b < 100))
print('>100MG:', sum(1 for b in Bs if b >= 100))
print('Teff range:', min(r['Teff'] for r in rows), '/', max(r['Teff'] for r in rows))
print('snr_blue range:', round(min(r['snr_blue'] for r in rows), 2), '/', round(max(r['snr_blue'] for r in rows), 2))

# ---- B 分档聚合（全 91 颗） ----
# 档位：<1, 1-10, 10-48, 48-100, 100-250, >250 MG（B_ion 序列 48/65/94/147/261 MG 附近）
BINS = [(0, 1), (1, 10), (10, 48), (48, 100), (100, 250), (250, 1e9)]
BIN_LABELS = ['<1 MG', '1-10', '10-48', '48-100', '100-250', '>250 MG']

def median(vals):
    sv = sorted(vals)
    m = len(sv)
    if m == 0:
        return None
    if m % 2 == 1:
        return sv[m // 2]
    return 0.5 * (sv[m // 2 - 1] + sv[m // 2])

print()
print('=== B 分档：三带残差中位数（log10 obs/mod） ===')
print('%-8s %5s | %8s %8s %8s %8s' % ('bin', 'n', 'blue', 'red', 'slopeA', 'slopeB'))
for (lo, hi), lab in zip(BINS, BIN_LABELS):
    grp = [r for r in rows if lo <= r['B_MG'] < hi]
    if not grp:
        print('%-8s %5s | %8s %8s %8s %8s' % (lab, 0, '-', '-', '-', '-'))
        continue
    b = median([r['blue_res'] for r in grp])
    rd = median([r['red_res'] for r in grp])
    sa = median([r['slopeA_res'] for r in grp])
    sb = median([r.get('slopeB_res', 0) for r in grp])
    print('%-8s %5d | %8.4f %8.4f %8.4f %8.4f' % (lab, len(grp), b, rd, sa, sb))

# ---- 中场 vs 弱场（论文口径：10-20kK 主档） ----
print()
print('=== Teff 10-20kK 主档：弱场(<10MG) vs 中场(10-100MG) ===')
for lab, cond in [('weak <10MG', lambda r: r['Teff'] >= 10000 and r['Teff'] <= 20000 and r['B_MG'] < 10),
                  ('mid 10-100', lambda r: r['Teff'] >= 10000 and r['Teff'] <= 20000 and 10 <= r['B_MG'] < 100),
                  ('strong >100', lambda r: r['Teff'] >= 10000 and r['Teff'] <= 20000 and r['B_MG'] >= 100)]:
    grp = [r for r in rows if cond(r)]
    if not grp:
        print('%-12s n=0' % lab)
        continue
    b = median([r['blue_res'] for r in grp])
    rd = median([r['red_res'] for r in grp])
    sa = median([r['slopeA_res'] for r in grp])
    sb = median([r.get('slopeB_res', 0) for r in grp])
    print('%-12s n=%3d | blue %+.4f | red %+.4f | slopeA %+.4f | slopeB %+.4f'
          % (lab, len(grp), b, rd, sa, sb))
    print('          B range:', round(min(r['B_MG'] for r in grp), 2), '-', round(max(r['B_MG'] for r in grp), 2))

# ---- 逐阈值检查（转移假说：B_ion 序列处应有窗口边缘结构） ----
print()
print('=== 阈值邻域检查（B_ion: Heps 48 / Hd 65 / Hg 94 / Hb 147 / Ha 261 MG） ===')
for thr in [48, 65, 94, 147, 261]:
    lo_grp = [r for r in rows if thr * 0.5 <= r['B_MG'] < thr]
    hi_grp = [r for r in rows if thr <= r['B_MG'] < thr * 1.5]
    def agg(g, key):
        v = median([r[key] for r in g])
        return ('%.4f' % v) if v is not None else '-'
    print('thr %3d MG | below[%4.0f-%3.0f] n=%2d blue=%s red=%s | above[%3.0f-%4.0f] n=%2d blue=%s red=%s'
          % (thr, thr * 0.5, thr, len(lo_grp), agg(lo_grp, 'blue_res'), agg(lo_grp, 'red_res'),
             thr, thr * 1.5, len(hi_grp), agg(hi_grp, 'blue_res'), agg(hi_grp, 'red_res')))

# ---- Spearman 式单调性粗检（排序后看趋势） ----
print()
print('=== 按 B 排序的三带残差（每 10 颗一组，中位数） ===')
sorted_rows = sorted(rows, key=lambda r: r['B_MG'])
for i in range(0, len(sorted_rows), 10):
    grp = sorted_rows[i:i + 10]
    b = median([r['blue_res'] for r in grp])
    rd = median([r['red_res'] for r in grp])
    sa = median([r['slopeA_res'] for r in grp])
    print('B[%6.2f-%6.2f] n=%2d | blue %+.4f | red %+.4f | slopeA %+.4f'
          % (grp[0]['B_MG'], grp[-1]['B_MG'], len(grp), b, rd, sa))
