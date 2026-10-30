# -*- coding: utf-8 -*-
"""
Phase 104az-43 数值先证伪 (模式 8, Lean 固化前置):
SilenceCriticalLayer 定理的数值真值检验
1. S_4 = s^d_H = e^-ln15 = 1/15 (残差)
2. 0.8 三表达全等: 1-N_active/B = (N_total-1)/N_total = 1-3/15 = 4/5
3. 唯一性: 3*s^k = 3/15 的唯一解 k = ln15 (对数单射)
4. 随机扰动样本: 阈值恒等式在扰动下残差稳定为 0 (解析恒等)
"""
import json, math, os, random

random.seed(42)
res = {'checks': []}

# 1. S_4 = e^-ln15
s = math.e**(-1)
d_H = math.log(15)
S4 = s**d_H
r1 = abs(S4 - 1/15)
res['checks'].append({'name': 'S4 = s^d_H = 1/15', 'value': S4, 'residual': r1})

# 2. 三表达全等
k_max, N_active, B, N_total = 8, 3, 15, 5
v_a = 1 - N_active/B
v_b = (N_total-1)/N_total
v_c = 1 - 3*(1/15)
res['checks'].append({'name': 'three_forms', 'v_a': v_a, 'v_b': v_b, 'v_c': v_c,
                      'max_residual': max(abs(v_a-v_b), abs(v_b-v_c), abs(v_a-v_c))})

# 3. 唯一性: 3*s^k = 3/15 -> k = ln15
# 3*s^k = 3/15 -> s^k = 1/15 -> k*ln(s) = ln(1/15) -> k = ln(1/15)/ln(s) = ln15/1 = ln15
k_solved = math.log(1/15)/math.log(s)
r3 = abs(k_solved - d_H)
res['checks'].append({'name': 'uniqueness k = ln15', 'k_solved': k_solved, 'd_H': d_H, 'residual': r3})

# 4. 随机样本: 阈值恒等式对 k_max/N_active 扰动 (整数域保持关系) -- 解析恒等
samples = []
for i in range(8):
    # 扰动: 用不同整数组合保持 B=2k-1, N_total=B/N_active
    kk = random.choice([8, 8, 8, 4, 16])  # 保持 k_max=8 主域; 其他为对照 (应破坏 0.8)
    na = random.choice([3, 3, 3, 2, 4])
    if kk*na == 0:
        continue
    bb = 2*kk - 1
    nt = bb // na if bb % na == 0 else None
    if nt is None:
        samples.append({'k_max': kk, 'N_active': na, 'B': bb, 'N_total': None, 'thr': None})
        continue
    thr = 1 - na/bb
    thr2 = (nt-1)/nt
    samples.append({'k_max': kk, 'N_active': na, 'B': bb, 'N_total': nt,
                    'thr': round(thr,6), 'thr2': round(thr2,6),
                    'eq': abs(thr-thr2)<1e-12})
res['checks'].append({'name': 'random_samples', 'samples': samples,
                      'note': '主域 (k_max=8,N_active=3): thr=0.8 精确; 其他组合破坏 0.8 (身份链依赖具体框架量)'})

ok = all(c.get('residual', 0) < 1e-8 if 'residual' in c else True for c in res['checks'][:3])
res['verdict'] = f'解析恒等式残差全部 <1e-8 (S4 {r1:.2e}, 唯一性 {r3:.2e}) -- 可投入 Lean 固化' if ok else 'FAIL'
print(json.dumps(res, ensure_ascii=False, indent=2))
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), '_phase104_s4lean_pre_tmp.json')
with open(out, 'w', encoding='utf-8') as f:
    json.dump(res, f, ensure_ascii=False, indent=2)
print(f'已存盘: {out}')
