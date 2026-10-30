# -*- coding: utf-8 -*-
"""
Phase 104az-32 (26.16j-80): 线序梯度 = 缺口窗口(高阶线带) x B_th 梯度 双链闭合
观测(DESI 4.9): Hβ -45% / Hγ -84% / Hδ -98%   (缺失率 d_obs)
理论禁戒率(45MG, C=3.03): Hβ 0.600 / Hγ 0.835 / Hδ 0.919
电离阈值 B_th: Hβ 147 / Hγ 94 / Hδ 65 MG
缺口窗口: Hε 3970.1 -> Hγ 4340.5, 中心 4155.3 A (26.16j-78)
检验:
  A. 各线到缺口窗口中心的距离 vs 缺失率 -- 单调?
  B. B_th vs 缺失率 -- 单调?
  C. 理论禁戒率 vs 观测缺失率 -- 量级/方向?
"""
import json, os

lines = {
    'Hβ': {'lam': 4861.3, 'd_obs': 0.45, 'forb_th': 0.600, 'Bth': 147.0},
    'Hγ': {'lam': 4340.5, 'd_obs': 0.84, 'forb_th': 0.835, 'Bth': 94.0},
    'Hδ': {'lam': 4101.7, 'd_obs': 0.98, 'forb_th': 0.919, 'Bth': 65.0},
    'Hε': {'lam': 3970.1, 'd_obs': None, 'forb_th': None, 'Bth': 48.0},  # 缺失率未列
}
gap_center = 4155.3   # 缺口窗口中心 (Hε-Hγ 带)
gap_lo, gap_hi = 3970.1, 4340.5

res = {}
for name, d in lines.items():
    dist = abs(d['lam'] - gap_center)
    inwin = gap_lo <= d['lam'] <= gap_hi
    res[name] = {'lam': d['lam'], 'dist_center': round(dist, 1), 'in_gap_win': inwin,
                 'd_obs': d['d_obs'], 'forb_th': d['forb_th'], 'Bth': d['Bth']}

# 排序一致性 (Hβ < Hγ < Hδ 缺失率递增)
order_obs = ['Hβ', 'Hγ', 'Hδ']
d_obs = [res[k]['d_obs'] for k in order_obs]
dist = [res[k]['dist_center'] for k in order_obs]
bth = [res[k]['Bth'] for k in order_obs]
forb = [res[k]['forb_th'] for k in order_obs]

res['order_checks'] = {
    'd_obs_monotone': d_obs[0] < d_obs[1] < d_obs[2],
    'dist_anti_monotone': dist[0] > dist[1] > dist[2],   # 距离越小缺失越大
    'Bth_anti_monotone': bth[0] > bth[1] > bth[2],       # 阈值越低缺失越大
    'forb_th_monotone': forb[0] < forb[1] < forb[2],
}

# 量级对照: 理论禁戒率 vs 观测缺失 (0.600 vs 0.45, 0.835 vs 0.84, 0.919 vs 0.98)
ratios = {k: round(res[k]['forb_th'] / res[k]['d_obs'], 3) for k in order_obs}
res['forb_vs_obs_ratio'] = ratios

# Hε 预测: B_th 48 (最低) + 在缺口窗口蓝端(3970 在段边界 4010.6 外 ~40A)
# -> 预测强禁戒 (>= Hδ 0.98?)
res['Hε_predict'] = {
    'Bth_lowest': True, 'dist_center': res['Hε']['dist_center'],
    'in_gap_win': res['Hε']['in_gap_win'],
    'note': 'Hε B_th=48 MG 最低 + 距窗口中心 185A(Hγ 同级) -> 预测缺失 >= 84% (待观测数据)'
}

res['verdict'] = (
    '双链闭合: 缺失率排序 Hβ<Hγ<Hδ 与 距离窗口中心(706>185>54A) 反单调 且 与 B_th(147>94>65MG) 反单调 -- '
    '缺口窗口位置链 + B_th 梯度链一致; 理论禁戒率(0.600/0.835/0.919) 与观测(0.45/0.84/0.98) '
    'Hγ/Hδ 量级吻合(1.0x/0.94x), Hβ 理论高估(1.33x -- 窗口外线缺失含其他机制/Zeeman 混叠)'
)

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), '_phase104_p1_lineseq_tmp.json')
with open(out, 'w', encoding='utf-8') as f:
    json.dump(res, f, ensure_ascii=False, indent=2)

print('==== 各线对照 ====')
print(f'{"线":<4}{"波长":>8}{"距窗口中心":>10}{"窗口内":>6}{"观测缺失":>8}{"理论禁戒":>8}{"B_th":>7}')
for k in order_obs:
    r = res[k]
    print(f'{k:<4}{r["lam"]:>8.1f}{r["dist_center"]:>10.1f}{str(r["in_gap_win"]):>6}{r["d_obs"]:>8.0%}{r["forb_th"]:>8.3f}{r["Bth"]:>7.0f}')
print(f'Hε 预测: B_th=48(最低), 距中心 {res["Hε"]["dist_center"]}A, 窗口内={res["Hε"]["in_gap_win"]}')
print()
print('==== 排序一致性 ====')
for k, v in res['order_checks'].items():
    print(f'  {k}: {v}')
print()
print('==== 理论 vs 观测 ====')
for k in order_obs:
    print(f'  {k}: 理论/观测 = {res["forb_vs_obs_ratio"][k]}')
print()
print(res['verdict'])
print(f'已存盘: {out}')
