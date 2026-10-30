# -*- coding: utf-8 -*-
"""
Phase 104az-26 (26.16j-74): 稀释因子 ~20 定量审计
问题: 波长平均 Lp 0.6% (J135141/J100356) = 连续谱峰模型 12.5% x 1/20.8
这 20.8 倍稀释能否由 Balmer 线区覆盖解释? 还是另有来源(缺口窗口窄带/相位/口径)?

审计项:
A. Balmer 线区覆盖 -> 理论稀释上限(线区偏振=0 假设)
B. 缺口窗口窄带候选: 缺口=1 基态 -> 窗口 = 带宽/8 -> 稀释 8 倍
C. 组合候选 + 剩余缺口量化
"""
import json, os

# ---- 参数 ----
win = (4000.0, 6500.0)          # J135141 83-bin 窗口 (Angstrom)
win_width = win[1] - win[0]     # 2500 A
lines = {'Ha': 6562.8, 'Hb': 4861.3, 'Hg': 4340.5, 'Hd': 4101.7, 'He': 3970.1}
model_lp_peak = 12.5            # 连续谱峰模型 (%)
obs_lp_wavg = 0.61              # J135141 0.62 / J100356 0.60 均值 (%)
ratio_needed = model_lp_peak / obs_lp_wavg   # ~20.5

results = {}

# ---- A. 线区覆盖稀释 ----
halfwidths = [10.0, 25.0, 50.0, 100.0]
line_fracs = {}
for hw in halfwidths:
    inwin = 0.0
    details = []
    for name, lc in lines.items():
        lo, hi = lc - hw, lc + hw
        lo_c = max(lo, win[0]); hi_c = min(hi, win[1])
        w = max(0.0, hi_c - lo_c)
        inwin += w
        details.append((name, round(w, 1)))
    frac = inwin / win_width
    line_fracs[hw] = {'inwin_A': round(inwin, 1), 'frac': round(frac, 4),
                      'dil_if_linezero': round(1.0 / (1.0 - frac), 3) if frac < 1 else None,
                      'details': details}
results['A_line_coverage'] = line_fracs

# ---- B. 缺口窗口窄带候选 ----
# 缺口 = 1 基态 (8 基态等分) -> 缺口窗口 = 带宽/8 (基态数占比 -> 带宽占比候选)
dil_8 = 8.0
lp_after_8 = model_lp_peak / dil_8
results['B_gap_window_1of8'] = {
    'dil': dil_8, 'lp_after': round(lp_after_8, 2),
    'note': '缺口窗口=带宽/8 (基态数身份) -> 12.5/8=1.56%, 观测 0.61% 仍差 2.6 倍'
}

# ---- C. 组合候选 ----
# 1/8 缺口窗口 x 线区覆盖(再稀释) 的组合
combos = {}
for hw in [25.0, 50.0]:
    frac = line_fracs[hw]['frac']
    # 缺口窗口=带宽/8, 线区偏振=0 -> 波长平均 = 12.5/8 * (1-frac)
    lp_comb = model_lp_peak / 8.0 * (1.0 - frac)
    combos[f'hw{hw}'] = {'lp': round(lp_comb, 3), 'vs_obs': round(lp_comb / obs_lp_wavg, 3)}
results['C_combined'] = combos

# ---- D. 相位/场结构候选 (PG 1031+234 同星 2 倍差类比) ----
# 12.5 x (1/8 缺口窗口) x (1/2 相位平均) = 0.78% vs 0.61 -- 1.28 倍
lp_full = model_lp_peak / 8.0 * 0.5
results['D_phase_half'] = {'lp': round(lp_full, 3), 'vs_obs': round(lp_full / obs_lp_wavg, 3),
                           'note': '12.5/8 x 1/2(相位平均候选) = 0.78%, 观测 0.61% -- 1.28 倍'}

# ---- E. 关键判定 ----
# 线区覆盖能否解释 20.8 倍?
max_dil_line = max(v['dil_if_linezero'] for v in line_fracs.values() if v['dil_if_linezero'])
results['E_verdict'] = {
    'ratio_needed': round(ratio_needed, 1),
    'max_dil_from_line_coverage': max_dil_line,
    'line_coverage_sufficient': max_dil_line >= ratio_needed,
    'verdict': ('线区覆盖无法解释 20.8 倍稀释(上限 %.1fx) -> 稀释主要来源=缺口窗口窄带(1/8 带宽, 8x)'
                ' + 剩余 2.6x 候选(相位平均/场结构/83-bin 口径)' % max_dil_line)
}

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), '_phase104_p1_dilution_tmp.json')
with open(out, 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print('==== A. Balmer 线区覆盖 -> 理论稀释上限 ====')
for hw, v in line_fracs.items():
    print(f'  半宽 {hw:>5} A: 窗内线区 {v["inwin_A"]:>5.1f} A ({v["frac"]*100:.1f}%), 稀释上限 {v["dil_if_linezero"]}')
print('==== B. 缺口窗口 1/8 带宽候选 ====')
print(f'  稀释 8x -> 12.5/8 = {lp_after_8:.2f}% (观测 0.61% 仍差 {12.5/8/0.61:.1f}x)')
print('==== C. 组合 (1/8 x 线区) ====')
for k, v in combos.items():
    print(f'  {k}: {v["lp"]}% vs 0.61% ({v["vs_obs"]}x)')
print('==== D. 1/8 x 相位平均 1/2 ====')
print(f'  {lp_full}% vs 0.61% ({lp_full/0.61:.2f}x)')
print('==== E. 判定 ====')
print(f'  所需稀释 {ratio_needed:.1f}x vs 线区覆盖最大稀释 {max_dil_line}x')
print(f'  {results["E_verdict"]["verdict"]}')
print(f'已存盘: {out}')
