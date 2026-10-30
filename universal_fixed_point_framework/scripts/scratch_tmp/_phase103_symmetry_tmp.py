# -*- coding: utf-8 -*-
"""Phase 103g: 均匀分布签名检验——blue/red 连续谱增强对称性
H_uniform（量子数±均匀分布）：blue 增量 ≈ red 增量（对称）
H_single（单向转移）：blue >> red 或 red >> blue（不对称）
对照：RWA 弱波长依赖预测 blue/red ≈ (λ_red/λ_blue)^3 附近（~1.09，弱不对称）
"""
import json, statistics

with open(r'E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_gaia_abs\paperX_wd_absflux_cal.json', encoding='utf-8') as f:
    data = json.load(f)

rows = data if isinstance(data, list) else data.get('rows', data.get('data', []))
print('total rows:', len(rows))

def g(r, k):
    v = r.get(k)
    return v if v is not None else float('nan')

# 有效样本（blue+red calres 均有效，SNR>=2）
S = []
for r in rows:
    b, rd, sb, sr = g(r, 'blue_calres'), g(r, 'red_calres'), g(r, 'snr_blue'), g(r, 'snr_red')
    if b != b or rd != rd:
        continue
    if sb != sb or sr != sr or sb < 2 or sr < 2:
        continue
    S.append((g(r, 'B_MG'), b, rd, sb, sr, g(r, 'Teff')))
print('有效样本（snr>=2）:', len(S))

def sub(cond):
    return [x for x in S if cond(x)]

# 1) 全场：blue vs red 配对差（Wilcoxon 近似 z）
import math
def wilcoxon_signed( diffs ):
    ds = [d for d in diffs if abs(d) > 1e-12]
    n = len(ds)
    ranks = {}
    sd = sorted(ds, key=abs)
    i = 0
    while i < n:
        j = i
        while j + 1 < n and abs(sd[j+1] - sd[i]) < 1e-12:
            j += 1
        r = (i + j) / 2 + 1
        for k in range(i, j+1):
            ranks[id(sd[k])] = r
        i = j + 1
    # 用值做 key（float 可能重复，改用 index 映射）
    idx = {id(v): k for k, v in enumerate(sd)}
    Wpos = sum(ranks[id(v)] for v in ds if v > 0)
    # 重新精确做：按位置
    pos_ranks = []
    for k, v in enumerate(sd):
        r = ranks[id(v)]
        if v > 0:
            pos_ranks.append(r)
    Wpos = sum(pos_ranks)
    mu = n * (n + 1) / 4
    sigma = math.sqrt(n * (n + 1) * (2 * n + 1) / 24)
    z = (Wpos - mu) / sigma if sigma > 0 else 0
    return n, Wpos, z

def report(name, X):
    if len(X) < 4:
        print(name, 'n<4 跳过')
        return
    bs = [x[1] for x in X]; rs = [x[2] for x in X]
    mb, mr = statistics.median(bs), statistics.median(rs)
    diffs = [b - r for b, r in zip(bs, rs)]
    n, W, z = wilcoxon_signed(diffs)
    ratio = mb / mr if mr != 0 else float('nan')
    print('%s: n=%d | blue中位 %+.4f  red中位 %+.4f | blue/red=%.3f | 配对差中位 %+.4f | Wilcoxon z=%.2f (p≈%.3f)'
          % (name, len(X), mb, mr, ratio, statistics.median(diffs), z, 2*(1-0.5*(1+math.erf(abs(z)/math.sqrt(2)))) if z==z else float('nan')))

report('全场 snr>=2', S)
report('中场 10-100 MG', sub(lambda x: 10 <= x[0] <= 100))
report('中场 10-48 MG', sub(lambda x: 10 <= x[0] < 48))
report('弱场 <10 MG', sub(lambda x: x[0] < 10))
report('Teff 10-20kK 全场', sub(lambda x: 10 <= x[5] <= 20))
report('Teff 10-20kK 中场', sub(lambda x: 10 <= x[5] <= 20 and 10 <= x[0] <= 100))

# 2) 增量（中场-弱场）对称性：用分档中位差（论文口径）
print()
print('=== 论文口径：弱场(<10) vs 中场(10-100) mean 增量（Teff 10-20kK） ===')
W = sub(lambda x: x[0] < 10 and 10 <= x[5] <= 20)
M = sub(lambda x: 10 <= x[0] <= 100 and 10 <= x[5] <= 20)
for nm, key in [('blue_calres', 1), ('red_calres', 2)]:
    pass
mb_w = statistics.mean([x[1] for x in W]); mr_w = statistics.mean([x[2] for x in W])
mb_m = statistics.mean([x[1] for x in M]); mr_m = statistics.mean([x[2] for x in M])
print('blue: 弱场 %+.4f -> 中场 %+.4f | 增量 %+.4f' % (mb_w, mb_m, mb_m - mb_w))
print('red : 弱场 %+.4f -> 中场 %+.4f | 增量 %+.4f' % (mr_w, mr_m, mr_m - mr_w))
db, dr = mb_m - mb_w, mr_m - mr_w
print('增量比 blue/red = %.3f（均匀分布预测≈1.0，RWA λ³ 预测≈%.3f）' % (db/dr, (3720/3620)**3))
