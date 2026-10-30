# -*- coding: utf-8 -*-
"""
Phase 104az-45 数值先证伪 (模式 8, Lean 固化前置):
SilenceObservabilityBoundary -- 可观测性边界定理的数值真值检验
rho(s) = B*e^-s (分支收缩积 -- B=15 分支 x 收缩率 e^-s)
1. rho(d_H) = 1 (Moran 临界 -- Bowen=Moran 方程 B*r^dH=1)
2. 收敛域: rho(s)<1 <-> s>d_H (可观测)
3. 发散域: rho(s)>1 <-> s<d_H (不可观测)
4. 临界唯一: rho(s)=1 <-> s=d_H
5. 随机样本: 单调过渡验证
"""
import json, math, os, random

random.seed(7)
B = 15
d_H = math.log(15)
res = {'checks': []}

# 1. rho(d_H)=1
rho = lambda s: B * math.exp(-s)
r1 = abs(rho(d_H) - 1)
res['checks'].append({'name': 'rho(d_H)=1 (Moran 临界)', 'value': rho(d_H), 'residual': r1})

# 2-4. 域分割
samples = []
for i in range(20):
    s = d_H + random.uniform(-3, 3)
    r = rho(s)
    if s > d_H + 1e-9:
        pred = r < 1
    elif s < d_H - 1e-9:
        pred = r > 1
    else:
        pred = abs(r - 1) < 1e-9
    samples.append({'s': round(s, 4), 'rho': round(r, 4), 'domain': '收敛(可观测)' if r < 1 else ('临界' if abs(r-1)<1e-9 else '发散(不可观测)'), 'ok': pred})
res['checks'].append({'name': 'domain_split_20_samples', 'samples': samples, 'all_ok': all(x['ok'] for x in samples)})

# 5. 临界唯一性: 解 rho(s)=1/2 -> s=log(30)... 解 rho(s)=1 的数值根
def bisect_root(f, lo, hi, tol=1e-12):
    # f 递减 (15e^-s-1): f(mid)>0 根在右侧 -> lo=mid
    for _ in range(100):
        mid = (lo+hi)/2
        if f(mid) > 0:
            lo = mid
        else:
            hi = mid
    return (lo+hi)/2
root = bisect_root(lambda s: rho(s) - 1, -1, 6)
res['checks'].append({'name': 'unique_root_rho=1', 'root': root, 'd_H': d_H, 'residual': abs(root-d_H)})

ok = r1 < 1e-8 and all(x['ok'] for x in samples) and abs(root-d_H) < 1e-8
res['verdict'] = f'rho(d_H)=1 残差 {r1:.2e}, 20 样本域分割全对, 临界根唯一 (残差 {abs(root-d_H):.2e}) -- 可投入 Lean 固化' if ok else 'FAIL'
print(json.dumps(res, ensure_ascii=False, indent=2))
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), '_phase104_obsboundary_leanpre_tmp.json')
with open(out, 'w', encoding='utf-8') as f:
    json.dump(res, f, ensure_ascii=False, indent=2)
print(f'已存盘: {out}')
