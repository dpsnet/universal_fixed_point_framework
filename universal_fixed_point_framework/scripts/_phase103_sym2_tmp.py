# -*- coding: utf-8 -*-
"""Phase 103g2: 均匀分布签名检验（增量对称性）——Teff 单位修正版
判别：
- H_uniform（量子数±均匀分布）：B 相关增强增量 blue ≈ red
- H_single（单向转移）：增量不对称
- 对照 RWA λ³ 弱波长依赖：增量比 ≈ (3720/3620)^3 ≈ 1.085
"""
import json, statistics, math

with open(r'E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_gaia_abs\paperX_wd_absflux_cal.json', encoding='utf-8') as f:
    data = json.load(f)
rows = data if isinstance(data, list) else data.get('rows', data.get('data', []))
S = []
for r in rows:
    b, rd = r.get('blue_calres'), r.get('red_calres')
    sb, sr = r.get('snr_blue'), r.get('snr_red')
    if b is None or rd is None or sb is None or sr is None or sb < 2 or sr < 2:
        continue
    S.append((r.get('B_MG'), b, rd, r.get('Teff')))

def sub(cond):
    return [x for x in S if cond(x)]

def report(name, X):
    if len(X) < 4:
        print('%s: n=%d 跳过' % (name, len(X)))
        return
    bs = [x[1] for x in X]; rs = [x[2] for x in X]
    mb, mr = statistics.mean(bs), statistics.mean(rs)
    diffs = [b - r for b, r in zip(bs, rs)]
    z = (statistics.mean(diffs) - 0) / (statistics.stdev(diffs) / math.sqrt(len(diffs))) if len(diffs) > 2 else float('nan')
    p = 2 * (1 - 0.5 * (1 + math.erf(abs(z) / math.sqrt(2)))) if z == z else float('nan')
    print('%s: n=%d | blue均值 %+.4f  red均值 %+.4f | 配对差 %+.4f±%.4f | 配对t z=%.2f (p=%.4f)'
          % (name, len(X), mb, mr, statistics.mean(diffs), statistics.stdev(diffs) if len(diffs) > 2 else 0, z, p))

# 论文口径：Teff 10-20 kK（K 单位：10000-20000）
print('=== Teff 10-20kK 主档（论文口径）===')
W = sub(lambda x: x[0] < 10 and 10000 <= x[3] <= 20000)
M = sub(lambda x: 10 <= x[0] <= 100 and 10000 <= x[3] <= 20000)
print('弱场 n=%d | 中场 n=%d' % (len(W), len(M)))
if len(W) >= 4 and len(M) >= 4:
    mb_w, mr_w = statistics.mean([x[1] for x in W]), statistics.mean([x[2] for x in W])
    mb_m, mr_m = statistics.mean([x[1] for x in M]), statistics.mean([x[2] for x in M])
    db, dr = mb_m - mb_w, mr_m - mr_w
    print('blue: %+.4f -> %+.4f | 增量 %+.4f' % (mb_w, mb_m, db))
    print('red : %+.4f -> %+.4f | 增量 %+.4f' % (mr_w, mr_m, dr))
    print('增量比 blue/red = %.3f（均匀分布≈1.0，RWA λ³≈%.3f）' % (db/dr, (3720/3620)**3))
    # 增量的配对 t（弱场/中场组间差）
    dW = [x[1]-x[2] for x in W]; dM = [x[1]-x[2] for x in M]
    print('配对差(blue-red)：弱场 %+.4f 中场 %+.4f | 组间增量差 %+.4f' % (statistics.mean(dW), statistics.mean(dM), statistics.mean(dM)-statistics.mean(dW)))

# 双带合并增强 vs 禁戒份额（修正 ε_trans 口径）
print()
print('=== 双带合并增强 vs η_line（修正 ε_trans 口径）===')
print('（合并增强 = [10^blue-1]+[10^red-1]，近似双带独立流量增强之和）')
for B, b, r, el in [(2.5, 0.0385, 0.0250, 0.149), (20.0, 0.0843, 0.0477, 0.203), (45.0, 0.1264, 0.1109, 0.600), (100.0, 0.1404, 0.1100, 0.858)]:
    enh = (10**b - 1) + (10**r - 1)
    print('B=%5.1f | blue %+.4f red %+.4f | 合并增强 %.1f%% | η_line=%.3f | ε_trans=%.2f' % (B, b, r, enh*100, el, enh/el))
