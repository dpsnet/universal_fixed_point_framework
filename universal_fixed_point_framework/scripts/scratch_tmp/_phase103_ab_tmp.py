# -*- coding: utf-8 -*-
"""Phase 103j: A/B 判别——线缺失 vs 连续谱增强的分档关系
A（吸收抑制）：连续谱增强=η_comp/RWA 禁连续吸收（与线缺失独立/同源不同物）
B（转移发射）：连续谱增强=线缺失能量 21% 流入（calres ∝ 线缺失，固定比例）
判别：EW 缺失率(B) vs calres(B) 的形状与比例
"""
import json, statistics, math

BASE = r'E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts'

# m83c：518 颗，obs_EW vs koester_EW
with open(BASE + '\\paperX_wd_m83c_koester_ew.json', encoding='utf-8') as f:
    m = json.load(f)
S = []
for s in m['samples']:
    B_t = s.get('B_tesla')
    ob, ko = s.get('obs_EW'), s.get('koester_EW')
    if B_t is None or ob is None or ko is None or ko <= 0:
        continue
    if ob <= 0:
        continue  # 未检测线（与论文筛选一致）
    S.append((B_t / 100.0, 1.0 - ob / ko, s.get('Teff')))  # B_MG, 缺失率
print('m83c 有效（obs_EW>0, koester>0）:', len(S), '/', m['n_samples'])

# gaia_abs：91 颗 calres
with open(BASE + r'\_gaia_abs\paperX_wd_absflux_cal.json', encoding='utf-8') as f:
    g = json.load(f)
rows = g if isinstance(g, list) else g.get('rows', g.get('data', []))
G = []
for r in rows:
    b = r.get('blue_calres'); sb = r.get('snr_blue')
    if b is None or b != b or sb is None or sb < 2:
        continue
    G.append((r.get('B_MG'), b, r.get('red_calres'), r.get('Teff')))
print('gaia_abs 有效（snr>=2）:', len(G))

# B 分档（对齐论文口径：<10 / 10-48 / 48-100 / 100-250）
def bins(X, idx_B, use_teff=False):
    res = {}
    for x in X:
        B = x[idx_B]
        if use_teff and not (10000 <= x[3] <= 20000):
            continue
        if B < 10: k = '<10'
        elif B < 48: k = '10-48'
        elif B < 100: k = '48-100'
        elif B < 250: k = '100-250'
        else: k = '>250'
        res.setdefault(k, []).append(x)
    return res

print()
print('=== 线 EW 缺失率（m83c，全 518 目录）vs 连续谱增强（gaia_abs）——B 分档中位 ===')
print('%-8s | %-28s | %-24s' % ('B 档', '线缺失率(obs/koester)', 'blue_calres'))
b_m83 = bins(S, 0)
b_gaia = bins(G, 0)
for k in ('<10', '10-48', '48-100', '100-250', '>250'):
    ms = b_m83.get(k, [])
    gs = b_gaia.get(k, [])
    if ms:
        miss = statistics.median([x[1] for x in ms])
        print('%-8s | n=%3d 缺失=%.3f (%.1f%%)' % (k, len(ms), miss, miss*100), end='')
    else:
        print('%-8s | n=0' % k, end='')
    if gs:
        print(' | n=%2d blue=%+.4f' % (len(gs), statistics.median([x[2] for x in gs])))
    else:
        print(' | n=0')
    print()

# Teff 10-20kK 子集
print('=== Teff 10-20kK 子集 ===')
b_m83t = bins(S, 0, use_teff=True)
b_gaiat = bins(G, 0, use_teff=True)
for k in ('<10', '10-48', '48-100', '100-250', '>250'):
    ms = b_m83t.get(k, []); gs = b_gaiat.get(k, [])
    if ms:
        miss = statistics.median([x[1] for x in ms])
        print('%-8s | n=%3d 缺失=%.3f' % (k, len(ms), miss), end='')
    else:
        print('%-8s | n=0' % k, end='')
    if gs:
        print(' | n=%2d blue=%+.4f' % (len(gs), statistics.median([x[2] for x in gs])))
    else:
        print(' | n=0')
    print()

# 关键判别量：每档 增强(dex) 对应的"线缺失能量" vs calres
# 线缺失能量（dex）= -log10(1-缺失率)；21% 转移预言：calres ≈ 0.21 * 缺失能量(dex)？或 calres = 0.058（固定）？
print()
print('=== 判别量：转移份额（若 calres=转移）===')
print('（B 假说：calres 应 ∝ 线缺失能量 −log10(1−缺失率)；A 假说：calres 与缺失率无固定比例）')
b_m83t2 = bins(S, 0)
for k in ('<10', '10-48', '48-100', '100-250', '>250'):
    ms = b_m83t2.get(k, []); gs = b_gaia.get(k, [])
    if ms and gs:
        miss = statistics.median([x[1] for x in ms])
        loss_dex = -math.log10(1 - miss) if miss < 1 else float('inf')
        blue = statistics.median([x[2] for x in gs])
        ratio = blue / loss_dex if loss_dex and loss_dex != float('inf') else float('nan')
        print('%-8s | 缺失率 %.3f | 缺失能量 %+.3f dex | blue %+.4f dex | blue/缺失能量=%.3f'
              % (k, miss, loss_dex, blue, ratio))
