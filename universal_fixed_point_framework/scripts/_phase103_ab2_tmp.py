# -*- coding: utf-8 -*-
"""Phase 103j2: A/B 判别 v2——线缺失（dex 口径）vs 连续谱增强（dex）
论文口径：EW 缺失 = log10(obs_EW/koester_EW) dex（中位 −0.275 ≈ 46.9%）
对比 calres（dex）。B 假说：calres ≈ 0.21×|缺失|（固定比例）；A 假说：形状/比例独立
"""
import json, statistics, math

BASE = r'E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts'
with open(BASE + '\\paperX_wd_m83c_koester_ew.json', encoding='utf-8') as f:
    m = json.load(f)
S = []
for s in m['samples']:
    B_t, ob, ko = s.get('B_tesla'), s.get('obs_EW'), s.get('koester_EW')
    if B_t is None or ob is None or ko is None or ko <= 0 or ob <= 0:
        continue
    S.append((B_t / 100.0, math.log10(ob / ko), s.get('Teff')))  # B_MG, 缺失dex, Teff
print('m83c 有效:', len(S))

with open(BASE + r'\_gaia_abs\paperX_wd_absflux_cal.json', encoding='utf-8') as f:
    g = json.load(f)
rows = g if isinstance(g, list) else g.get('rows', g.get('data', []))
G = []
for r in rows:
    b, sb = r.get('blue_calres'), r.get('snr_blue')
    if b is None or b != b or sb is None or sb < 2:
        continue
    G.append((r.get('B_MG'), b, r.get('red_calres'), r.get('Teff')))
print('gaia_abs 有效:', len(G))

def bins(X, iB, iTeff):
    res = {}
    for x in X:
        B = x[iB]
        if not (10000 <= x[iTeff] <= 20000):
            continue
        if B < 10: k = '<10'
        elif B < 48: k = '10-48'
        elif B < 100: k = '48-100'
        else: k = '>100'
        res.setdefault(k, []).append(x)
    return res

print()
print('=== Teff 10-20kK 子集：线缺失(dex) vs blue_calres(dex)——B 分档中位 ===')
bS = bins(S, 0, 2); bG = bins(G, 0, 3)
print('%-8s | %-26s | %-22s | %s' % ('B 档', '线缺失 dex (m83c)', 'blue_calres', 'red_calres'))
for k in ('<10', '10-48', '48-100', '>100'):
    ms = bS.get(k, []); gs = bG.get(k, [])
    miss = statistics.median([x[1] for x in ms]) if ms else float('nan')
    blue = statistics.median([x[1] for x in gs]) if gs else float('nan')
    red = statistics.median([x[2] for x in gs]) if gs else float('nan')
    print('%-8s | n=%3d 缺失=%+.3f | n=%2d blue=%+.4f | red=%+.4f'
          % (k, len(ms), miss, len(gs), blue, red))

print()
print('=== 判别量 ===')
print('B 假说（转移）：blue_calres ≈ 0.21 × |线缺失 dex|（固定转移份额）')
print('A 假说（独立抑制）：blue_calres 与线缺失形状/比例独立')
prev = None
for k in ('<10', '10-48', '48-100', '>100'):
    ms = bS.get(k, []); gs = bG.get(k, [])
    if not ms or not gs:
        continue
    miss = statistics.median([x[1] for x in ms])
    blue = statistics.median([x[1] for x in gs])
    ratio = blue / abs(miss) if miss else float('nan')
    print('%-8s | |缺失|=%+.3f | blue=%+.4f | blue/|缺失|=%.3f' % (k, abs(miss), blue, ratio))
