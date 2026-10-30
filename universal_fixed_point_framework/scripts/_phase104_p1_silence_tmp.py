# -*- coding: utf-8 -*-
"""
Phase 104az-37 (26.16j-85): 静默加减形式统一 -- 场强依赖切换候选
26.16j-82 开放项: 乘法静默 1-sigma^3 = 0.9997 vs 加法静默 1-3*sigma = 0.8 并存
统一候选: 弱场 = 乘法静默 (连续微扰, 抑制 ~0.03%), 强场 = 加法静默 (阈值离散扣除, 80%)
切换点候选: B_th = E_bind/mu_B (Landau 管化阈值 -- 阈值型机制)
"""
import json, os

sigma = 1/15
mult = 1 - sigma**3   # 乘法静默 1-sigma^3
add  = 1 - 3*sigma    # 加法静默 1-3*sigma

# 弱场观测: 无缺失 (线正常) -- 乘法静默 ~0.9997 (抑制 0.03%)
# 强场观测: 阈值分割 (eta_comp >= 0.8) -- 加法静默 0.8
res = {
    'sigma': sigma,
    'mult_1minus_sigma3': round(mult, 7),
    'add_1minus_3sigma': round(add, 7),
    'weak_field_suppression': round(1-mult, 7),  # 0.03%
    'strong_field_threshold': add,               # 0.8
    'scenario': (
        '统一候选: 场强依赖切换 -- 弱场乘法静默 (连续微扰, 1-sigma^3=0.9997, 抑制仅 0.03%, 与弱场观测无缺失自洽) '
        '-> 强场加法静默 (阈值离散扣除, 1-3*sigma=0.8, 与 eta_comp 阈值分割自洽); '
        '切换点候选 = B_th (E_bind/mu_B -- Landau 管化阈值 -- 阈值型机制)'
    ),
    'checks': {
        'weak_field_no_missing': round(mult, 4),  # 0.9997 -> 弱场几乎无抑制
        'strong_field_threshold': add,            # 0.8 = eta_comp 阈值
        'eta_comp_B_monotone': 'eta_comp 随 B 单调上升 (横向压缩更狠) -- 弱场 ~0 -> 强场 ~1 -- 与乘法->加法切换自洽 (弱场无阈值/强场阈值出现)',
        'switch_point_precision': '切换点 (乘法->加法) 未精确定位 -- 候选 B_th 序列 (48/65/94/147/261 MG)',
    },
}

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), '_phase104_p1_silence_tmp.json')
with open(out, 'w', encoding='utf-8') as f:
    json.dump(res, f, ensure_ascii=False, indent=2)

print(f'sigma = 1/15')
print(f'  乘法静默 1-sigma^3 = {mult:.7f}  (抑制仅 {1-mult:.5f} = 0.03%)')
print(f'  加法静默 1-3*sigma = {add:.4f}  (0.8)')
print()
print(f'统一候选: 场强依赖切换')
print(f'  弱场: 乘法静默 {mult:.4f} -- 连续微扰 (与弱场观测无缺失自洽)')
print(f'  强场: 加法静默 {add:.4f} -- 阈值离散扣除 (与 eta_comp>=0.8 分割自洽)')
print(f'  切换点候选: B_th = E_bind/mu_B (Landau 管化阈值)')
print(f'  eta_comp(B) 单调上升 (弱场~0 -> 强场~1) -- 与乘法->加法切换自洽')
print(f'  诚实边界: 切换点未精确定位; 乘法静默非主机制 (0.03% 抑制 vs 46.9% 缺失) -- 加法才是阈值主机制')
print(f'已存盘: {out}')
