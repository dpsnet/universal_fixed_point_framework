# -*- coding: utf-8 -*-
"""
Phase 104az-41 (26.16j-89): "3 通道各 σ" 机制桥梁 -- 0.8 阈值框架身份深化
σ = S_4 = s^{d_H} = 1/15 (静默维数层)
B = 2*k_max-1 = 15 (分支数)
N_total = B/N_active = 5 (总层数 -- B = N_active x N_total)
0.8 = 1-N_active/B = (N_total-1)/N_total = 12/15 = 4/5 -- 全框架量精确
修正 26.16j-82 "4/5 的 5 无身份" -- 5 = N_total 有身份
"""
import json, math, os

k_max = 8
N_active = 3
s = math.e**(-1)
d_H = math.log(15)

# σ 身份: S_4 = s^{d_H}
S4 = s**d_H
S3 = s**N_active

# B 身份
B = 2*k_max - 1

# N_total
N_total = B // N_active

print('=== σ 身份链 ===')
print(f's = e^-1 = {s:.8f}')
print(f'd_H = ln15 = {d_H:.8f}')
print(f'σ = S_4 = s^d_H = e^-ln15 = {S4:.10f}  (期望 1/15 = {1/15:.10f})')
print(f'σ = S_4 与 1/15 残差: {abs(S4-1/15):.2e}')
print(f'S_3 = s^N_active = e^-3 = {S3:.8f}')

print()
print('=== 0.8 框架身份链 ===')
v1 = 1 - N_active/B
v2 = (N_total-1)/N_total
v3 = 1 - N_active*(1/15)
print(f'B = 2*k_max-1 = {B}')
print(f'N_total = B/N_active = {N_total}')
print(f'0.8_a = 1-N_active/B = 1-{N_active}/{B} = {v1:.6f}')
print(f'0.8_b = (N_total-1)/N_total = {N_total-1}/{N_total} = {v2:.6f}')
print(f'0.8_c = 1-N_active*σ = 1-3/15 = {v3:.6f}')
print(f'三者全等: {abs(v1-v2)<1e-12 and abs(v2-v3)<1e-12}')

print()
print('=== 三机制合并对照 (45MG C=3.03) ===')
eta = {'Hα': 0.015, 'Hβ': 0.530, 'Hγ': 0.806, 'Hδ': 0.905, 'Hε': 0.945}
for line, e in eta.items():
    flag = '窗口内 (≥0.8)' if e >= 0.8 else '窗口外 (<0.8)'
    print(f'{line}: η_comp={e:.3f}  {flag}')

print()
print('=== 修正 26.16j-82 ===')
print(f'4/5 = (N_total-1)/N_total -- 5 = N_total (总层数) 有框架身份 (B=N_active×N_total=3×5)')
print(f'原判断 "4/5 的 5 无身份" 修正 -- 5 = N_total')

res = {
    'sigma_identity': f'S_4 = s^d_H = 1/15 (静默维数层, s=e^-1, d_H=ln15)',
    'B_identity': f'2*k_max-1 = {B} (分支数)',
    'N_total_identity': f'B/N_active = {N_total} (总层数)',
    'threshold_0.8': {
        '1-N_active/B': round(v1, 10),
        '(N_total-1)/N_total': round(v2, 10),
        '1-3/15': round(v3, 10),
        'exact': abs(v1-v2) < 1e-12 and abs(v2-v3) < 1e-12
    },
    'correction_26.16j-82': '5 = N_total 有身份 (原"5 无身份"判断修正)',
    'verdict': '0.8 阈值 = 1-N_active/B = (N_total-1)/N_total -- 全框架量精确 -- "3 通道各 σ"机制桥梁: N_active=3 主动机制通道达完全静默 (S_4) 时总静默=N_active/B=3/15'
}
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), '_phase104_08bridge_tmp.json')
with open(out, 'w', encoding='utf-8') as f:
    json.dump(res, f, ensure_ascii=False, indent=2)
print(f'已存盘: {out}')
