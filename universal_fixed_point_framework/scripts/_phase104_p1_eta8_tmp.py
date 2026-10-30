# -*- coding: utf-8 -*-
"""
Phase 104az-34 (26.16j-82): eta_comp >= 0.8 阈值的框架身份候选
候选: 0.8 = 1 - N_active*sigma = 1 - 3*(1/15) = 1 - 0.2 = 0.8 (精确)
  sigma = 1/15 (静默族基元), N_active = 3 (统一 3 定理: 质量/力/谱)
对照: eta_comp 数值 (45MG, C=3.03): Halpha 0.015 / Hbeta 0.530 / Hgamma 0.806 / Hdelta 0.905 / Heps 0.945
检验: 阈值 0.8 的分割 (Hgamma/Hdelta/Heps >= 0.8) 与缺口窗口 (3970-4340 A) 重合
     eta_comp 数值与 0.8 的偏差 (Hgamma 0.806 vs 0.8 = 0.75%)
其他候选恒等: 4/5 (N_Weyl/5?), 1-sigma*3, 1-1/5, 0.8 vs 缺口 1/8=0.125 的关系
"""
import json, os

sigma = 1/15.0
N_active = 3
N_weyl = 4
k_max = 8

cands = {
    '1 - N_active*sigma': 1 - N_active*sigma,
    '1 - 3/15 (展开)': 1 - 3/15.0,
    '4/5 = N_weyl/(N_weyl+1)': N_weyl/(N_weyl+1.0),
    '1 - 1/5': 1 - 1/5.0,
    '1 - 2/10': 1 - 2/10.0,
}

eta_comp = {'Hα': 0.015, 'Hβ': 0.530, 'Hγ': 0.806, 'Hδ': 0.905, 'Hε': 0.945}
threshold = 0.8

res = {'sigma': sigma, 'N_active': N_active, 'threshold_target': threshold,
       'candidates': {k: round(v, 6) for k, v in cands.items()},
       'eta_comp': eta_comp}

# 阈值分割
res['segmentation'] = {}
for k, v in eta_comp.items():
    res['segmentation'][k] = {'eta_comp': v, 'ge_0.8': v >= threshold,
                              'gap_win_3970_4340': k in ('Hγ','Hδ','Hε')}

# 偏差: Hgamma 0.806 vs 0.8
res['deviations'] = {
    'Hγ_vs_0.8': round(eta_comp['Hγ']/threshold - 1, 4),
    'Hδ_vs_0.8': round(eta_comp['Hδ']/threshold - 1, 4),
    'Hε_vs_0.8': round(eta_comp['Hε']/threshold - 1, 4),
}

# 0.8 与缺口 1/8 关系
res['gap_relation'] = {
    '0.8+1/8': 0.8 + 0.125,
    'eta_comp_Hδ_vs_sum': round(eta_comp['Hδ']/(0.8+0.125), 4),
    'note': '0.8+0.125=0.925 vs eta_comp(Hδ)=0.905 -- 差 2.2% -- 弱候选(不强凑)'
}

# 静默形式并存: 乘法 1-sigma^N vs 加法 1-N*sigma
res['silence_forms'] = {
    'mult_1-sigma^3': 1 - sigma**3,
    'add_1-3sigma': 1 - 3*sigma,
    'note': '乘法静默(1-sigma^N, ~0.9997) vs 加法静默(1-3sigma, 0.8) -- 两种形式并存 -- 统一开放'
}

res['verdict'] = (
    '0.8 = 1 - N_active*sigma = 1 - 3*(1/15) = 0.8 精确命中 -- 框架身份候选成立(数值级); '
    'Hγ 0.806 偏差 +0.75% (eta_comp 数值依赖 C=3.03 定标); '
    '阈值分割: eta_comp>=0.8 线 (Hγ 0.806/Hδ 0.905/Hε 0.945) 与缺口窗口 (3970-4340A) 精确重合; '
    '静默加减形式并存开放 (1-sigma^3 vs 1-3sigma)'
)

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), '_phase104_p1_eta8_tmp.json')
with open(out, 'w', encoding='utf-8') as f:
    json.dump(res, f, ensure_ascii=False, indent=2)

print('==== 框架恒等候选 ====')
for k, v in cands.items():
    print(f'  {k:<28} = {v:.6f}')
print(f'\n==== 阈值分割 (eta_comp >= 0.8) ====')
for k, v in eta_comp.items():
    win = '缺口窗口内' if k in ('Hγ','Hδ','Hε') else '窗口外'
    print(f'  {k}: eta_comp={v:.3f} {">=0.8" if v>=0.8 else "<0.8"}  [{win}]')
print(f'\n==== 偏差 ====')
for k, v in res['deviations'].items():
    print(f'  {k}: {v:+.2%}')
print(f'\n==== 0.8 vs 缺口 1/8 ====')
print(f'  0.8+1/8 = {res["gap_relation"]["0.8+1/8"]} vs eta_comp(Hδ) {eta_comp["Hδ"]} -- {res["gap_relation"]["eta_comp_Hδ_vs_sum"]}')
print(f'\n==== 静默形式并存 ====')
print(f'  乘法 1-sigma^3 = {res["silence_forms"]["mult_1-sigma^3"]:.6f}')
print(f'  加法 1-3sigma  = {res["silence_forms"]["add_1-3sigma"]:.6f}')
print(f'\n{res["verdict"]}')
print(f'已存盘: {out}')
