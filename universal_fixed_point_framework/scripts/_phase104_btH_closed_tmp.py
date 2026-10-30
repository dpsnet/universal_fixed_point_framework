# -*- coding: utf-8 -*-
"""
Phase 104az-39 (26.16j-87): B_th 全框架闭式正式登记 -- m_e^2(4*pi*alpha)^(3/2)/n^2
谱定口径 (104m 最优): m_e -0.0081%, alpha 1/137.028 (-0.0058%)
B_th(n) = B_AU/n^2 -- 对照 48.01/65.35/94.11/147.05/261.41 MG
附: B_0.8 x2 递推的框架身份尝试 (26.16j-86 发现)
"""
import json, os, math

# ---- 框架量 ----
alpha_exp = 1/137.036
alpha_int = 1/137.028          # P7-5l (1/alpha = 24(d_H+3))
m_e_exp = 0.51099895           # MeV (PDG)
m_e_int = 0.51096              # 谱定口径 (-0.0081%)
B_AU_exp_T = 2350.5e3          # 实验 B_AU (Tesla) = Ryd/mu_B * 1e4? -- 2350.5 MG = 2.3505e5 T

# 无量纲比值法 (104m v2)
R = (m_e_int/m_e_exp)**2 * (alpha_int/alpha_exp)**1.5
dev = (R-1)*100
dm_e = (m_e_int/m_e_exp - 1)*100
da = (alpha_int/alpha_exp - 1)*100

names = {7:'Hε', 6:'Hδ', 5:'Hγ', 4:'Hβ', 3:'Hα'}
obs = {7:48.01, 6:65.35, 5:94.11, 4:147.05, 3:261.41}  # MG (观测/Phase100)

res = {'model': 'B_th(n) = m_e^2(4*pi*alpha)^(3/2)/n^2 (自然单位, 谱定口径)',
       'dm_e_pct': round(dm_e,4), 'dalpha_pct': round(da,4),
       'R': round(R,7), 'dev_pct': round(dev,4),
       'expected': round(2*dm_e + 1.5*da, 4)}

print('=== B_th 全框架闭式 (谱定口径, 26.16j-87) ===')
print(f'dm_e = {dm_e:+.4f}%  dalpha = {da:+.4f}%')
print(f'R = (m_e_int/m_e_exp)^2 (alpha_int/alpha_exp)^1.5 = {R:.7f}  -> 偏差 {dev:+.4f}%')
print(f'理论预期 2*dm_e + 1.5*da = {res["expected"]:+.4f}%')
print()
print('阈值序列对照 (MG):')
res['sequence'] = {}
print(f'{"线":<6}{"n":<4}{"B_th^内生":<14}{"B_th^观测":<14}{"偏差%":<10}')
for n in (7,6,5,4,3):
    b_int = 2350.5/n**2 * R
    b_obs = obs[n]
    d = (b_int/b_obs - 1)*100
    res['sequence'][names[n]] = {'n': n, 'B_endog_MG': round(b_int,2), 'B_obs_MG': b_obs, 'dev_pct': round(d,3)}
    print(f'{names[n]:<6}{n:<4}{b_int:<14.2f}{b_obs:<14.2f}{d:<+10.3f}')

# ---- B_0.8 x2 递推框架身份尝试 ----
print()
print('=== B_0.8 x2 递推框架身份尝试 (26.16j-86 发现) ===')
B08 = {7:10.0, 6:20.0, 5:41.0, 4:80.0}
res['B08_ratio_to_Bth'] = {}
for n in (7,6,5,4):
    r = B08[n]/obs[n]
    res['B08_ratio_to_Bth'][names[n]] = round(r,4)
    print(f'{names[n]} (n={n}): B_0.8={B08[n]:.0f} MG, B_th={obs[n]:.2f}, 比值={r:.4f}')

# 尝试: B_0.8 = B_th * f(n)?  f 序列: 0.208/0.306/0.436/0.544
# 候选: f(n) = (n-3)/n?  n=7: 4/7=0.571 no; f(n) = 2^(7-n)*10/2350.5*n^2?
res['B08_attempt'] = {
    'x2_recurrence': 'B_0.8(n+1) ≈ 2×B_0.8(n) (10→20→41→80 -- Hγ 差 2.5%)',
    'base_10MG_identity': '10 MG 无框架身份 (候选: 2×(k_max-N_gen)? 5 无身份 -- 不强凑)',
    'ratio_to_Bth': res['B08_ratio_to_Bth'],
    'verdict': '×2 递推为数值发现候选 -- 2=螺旋数 (Paper 44) 有框架身份但递推本身未从框架推导 -- 登记数值发现'
}

res['verdict'] = (
    f'B_th(n) = m_e^2(4π α)^(3/2)/n² 全框架闭式确认 (谱定口径偏差 {dev:+.4f}% -- 104m 维持); '
    f'公式结构来源: 1/n² 已转正 (Phase 102b 2b w=n), g=2 已内生 (2c-E), '
    f'(4πα)^(3/2) 的 3/2 幂 = e³/ħ³ (μ_B 组合) 仍外部 -- 最后外部环; '
    f'B_0.8 ×2 递推 = 数值发现 (2=螺旋数有身份, 10 MG 基数无身份)'
)

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), '_phase104_btH_closed_tmp.json')
with open(out, 'w', encoding='utf-8') as f:
    json.dump(res, f, ensure_ascii=False, indent=2)
print()
print(res['verdict'])
print(f'已存盘: {out}')
