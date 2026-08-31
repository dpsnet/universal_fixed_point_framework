"""
选择效应证伪——最终合并汇总（v10弱场+中场 + v11缺口10^3-10^4 T）

输出:
  1. 全场 B-残差梯度（6带 + Kruskal-Wallis + Spearman）
  2. 混淆参数分层（log_g x Teff）——参数路径证伪
  3. 匹配对照（中场 vs 最近邻弱场）——匹配后缺失保持
  4. 逐线EW比值——高阶线抑制/发射模式
  5. 强发射对照
  6. 汇总JSON（供论文引用）
"""

import json
import numpy as np
from scipy import stats

V10 = r'E:\workspace\hyper-resolution\universal_fixed_point_framework\results\white_dwarf_analysis_v10_results.json'
GAP = r'E:\workspace\hyper-resolution\universal_fixed_point_framework\results\white_dwarf_analysis_v11_gap_results.json'
OUT = r'E:\workspace\hyper-resolution\universal_fixed_point_framework\results\selection_effect_falsification.json'
LINES = ['Hα','Hβ','Hγ','Hδ','Hε','Hζ','Hη']

with open(V10, 'r', encoding='utf-8') as f:
    d10 = json.load(f)
with open(GAP, 'r', encoding='utf-8') as f:
    dgap = json.load(f)

all_int = d10['int']
all_weak = d10['weak'] + dgap['results']

def eff(rs):
    return [r for r in rs if r.get('resid') is not None and r['total_EW'] > 0]

iv = eff(all_int)          # 中场 10^4-10^5
wv = eff(all_weak)         # 弱场+缺口（<10^4）
wv_weak = eff(d10['weak'])
wv_gap = eff(dgap['results'])

def det_flag(x):
    return str(x).lower() == 'true'

summary = {}
print(f'有效样本: 中场 {len(iv)}, 弱场(<1e3) {len(wv_weak)}, 缺口(1e3-1e4) {len(wv_gap)}')
print()

# ===== 1. 全场 B-残差梯度 =====
print('='*70)
print('1. 全场 B-残差梯度（6带）')
print('='*70)
bands = [(100,300,'10^2-3x10^2 T'),(300,1000,'3x10^2-10^3 T'),
         (1000,3000,'10^3-3x10^3 T'),(3000,10000,'3x10^3-10^4 T'),
         (10000,30000,'10^4-3x10^4 T'),(30000,100000,'3x10^4-10^5 T')]
band_stat = []
all_r_all = all_int + all_weak
for lo, hi, lab in bands:
    vals = [r['resid'] for r in all_r_all if lo <= r['B_tesla'] < hi and r.get('resid') is not None and r['total_EW'] > 0]
    if vals:
        v = np.array(vals)
        band_stat.append(v)
        print(f'  {lab:<22} n={len(v):>3}  残差均值={np.mean(v):+.3f} dex  中值={np.median(v):+.3f}  负比例={np.mean(v<0)*100:.0f}%')
H, p_kw = stats.kruskal(*band_stat)
print(f'  Kruskal-Wallis(6带): H={H:.2f}, p={p_kw:.2e} -> {"带间显著差异!" if p_kw<0.05 else "带间无差异"}')
all_b = np.array([np.log10(r['B_tesla']) for r in all_r_all if r.get('resid') is not None and r['total_EW']>0])
all_r = np.array([r['resid'] for r in all_r_all if r.get('resid') is not None and r['total_EW']>0])
rho, p_rho = stats.spearmanr(all_b, all_r)
print(f'  全场 Spearman(残差 vs log10 B): n={len(all_b)}, rho={rho:+.3f}, p={p_rho:.2e}')
# 弱场+缺口内部漂移
wl_b = np.array([np.log10(r['B_tesla']) for r in wv])
wl_r = np.array([r['resid'] for r in wv])
rho_w, p_w = stats.spearmanr(wl_b, wl_r)
print(f'  <10^4 T 内部 Spearman: rho={rho_w:+.3f}, p={p_w:.4f}')
# 相邻带间跳跃
for i in range(len(bands)-1):
    pass
# 中场 vs 邻近缺口带(3e3-1e4)差异
g3 = np.array([r['resid'] for r in all_r_all if 3e3 <= r['B_tesla'] < 1e4 and r.get('resid') is not None and r['total_EW']>0])
m_all = np.array([r['resid'] for r in iv])
if len(g3)>0:
    t3, p3 = stats.ttest_ind(m_all, g3, equal_var=False)
    print(f'  中场(10^4-10^5) vs 缺口(3e3-10^4): {len(m_all)} vs {len(g3)}, t={t3:.2f}, p={p3:.4f}')
summary['gradient'] = {
    'bands': [{'label': lab, 'n': len(v), 'mean_resid': round(float(np.mean(v)),3),
               'median_resid': round(float(np.median(v)),3), 'neg_frac': round(float(np.mean(v<0)),3)}
              for (lo,hi,lab), v in zip(bands, band_stat)],
    'kruskal_p': float(p_kw),
    'spearman_full': {'rho': round(float(rho),3), 'p': float(p_rho)},
    'spearman_sub1e4': {'rho': round(float(rho_w),3), 'p': float(p_w)},
}
print()

# ===== 2. 混淆参数分层 =====
print('='*70)
print('2. 混淆参数分层（<10^4 T 组内 log_g x Teff 四象限）')
print('='*70)
lg_w = np.array([r['log_g'] for r in wv])
te_w = np.array([r['Teff'] for r in wv if r['Teff']])
lg_med = np.median(lg_w); te_med = np.median(te_w)
print(f'  中值: log_g={lg_med:.2f}, Teff={te_med:.0f} K')
quad = {}
for lg_hi in [False, True]:
    for te_hi in [False, True]:
        vals = [r['resid'] for r in wv if (r['log_g'] >= lg_med) == lg_hi and (r['Teff'] >= te_med) == te_hi]
        if vals:
            v = np.array(vals)
            quad[f'lg{"H" if lg_hi else "L"}-te{"H" if te_hi else "L"}'] = {
                'n': len(v), 'mean_resid': round(float(np.mean(v)),3)}
            print(f'  log_g{"高" if lg_hi else "低"} x Teff{"高" if te_hi else "低"}: n={len(v):>3}, 残差均值={np.mean(v):+.3f} dex, 负比例={np.mean(v<0)*100:.0f}%')
# 与中场同log_g区间的<1e4星
mid_lg = [r['log_g'] for r in iv]
ov = [r for r in wv if min(mid_lg) <= r['log_g'] <= max(mid_lg)]
ov_r = np.array([r['resid'] for r in ov])
mr = np.array([r['resid'] for r in iv])
if len(ov)>0:
    t_ov, p_ov = stats.ttest_ind(mr, ov_r, equal_var=False)
    print(f'  <10^4 T 中 log_g 落入中场范围({min(mid_lg):.2f}-{max(mid_lg):.2f})的星: n={len(ov)}, 残差均值={np.mean(ov_r):+.3f} dex')
    print(f'    vs 中场: t={t_ov:.2f}, p={p_ov:.4f} -> {"差异仍显著(参数路径证伪)" if p_ov<0.05 else "差异不显著"}')
    summary['confounder'] = {'quadrants': quad, 'overlap_n': len(ov),
                             'overlap_mean_resid': round(float(np.mean(ov_r)),3),
                             'mid_mean_resid': round(float(np.mean(mr)),3),
                             'overlap_vs_mid_p': float(p_ov)}
print()

# ===== 3. 匹配对照 =====
print('='*70)
print('3. 匹配对照（每颗中场星按 Teff+log_g 最近邻匹配弱场星）')
print('='*70)
matched_diff = []
for r in iv:
    ww = min(wv, key=lambda w: ((np.log10(w['Teff'])-np.log10(r['Teff']))/0.1)**2
              + ((w['log_g']-r['log_g'])/0.5)**2)
    matched_diff.append(r['resid'] - ww['resid'])
md = np.array(matched_diff)
t_m, p_m = stats.ttest_1samp(md, 0)
binom_p = stats.binomtest(np.sum(md<0), len(md), 0.5).pvalue
print(f'  匹配后残差差异: 均值={np.mean(md):+.3f} dex (EW比值 {10**np.mean(md):.3f})')
print(f'  负差异: {np.sum(md<0)}/{len(md)} ({np.mean(md<0)*100:.0f}%)')
print(f'  单样本t检验: t={t_m:.2f}, p={p_m:.4f}')
print(f'  符号检验: p={binom_p:.4f}')
summary['matched'] = {'mean_diff': round(float(np.mean(md)),3),
                      'ew_ratio': round(float(10**np.mean(md)),3),
                      'neg_frac': round(float(np.mean(md<0)),3),
                      'ttest_p': float(p_m), 'sign_p': float(binom_p)}
print()

# ===== 4. 逐线EW比值 =====
print('='*70)
print('4. 逐线平均EW比值（中场/弱场）——高阶线抑制模式')
print('='*70)
print(f'  {"线":<6}{"中场均值EW":>10}{"弱场均值EW":>10}{"比值":>8}')
perline = {}
for ln in LINES:
    m_ew = np.array([r['balmer_results'][ln]['EW'] for r in iv])
    w_ew = np.array([r['balmer_results'][ln]['EW'] for r in wv_weak])
    mm, wm = np.mean(m_ew), np.mean(w_ew)
    ratio = mm/wm if wm > 0 else None
    print(f'  {ln:<6}{mm:>9.1f}A{wm:>9.1f}A{ratio if ratio is None else round(ratio,2):>9}')
    perline[ln] = {'mid_mean': round(float(mm),2), 'weak_mean': round(float(wm),2),
                   'ratio': round(float(ratio),2) if ratio else None}
summary['perline'] = perline
print()

# ===== 5. 强发射对照（EW<-10A, 排除极端伪影>100A） =====
print('='*70)
print('5. 强发射对照（EW<-10A）')
print('='*70)
def strong_emit(r, thr=-10.0):
    return [ln for ln in LINES if r['balmer_results'][ln]['EW'] < thr]
mid_se = [r for r in all_int if strong_emit(r)]
weak_se = [r for r in all_weak if strong_emit(r)]
print(f'  中场({len(all_int)}颗含非有效): 强发射星 {len(mid_se)} ({len(mid_se)/len(all_int)*100:.0f}%)')
print(f'  <10^4 T({len(all_weak)}颗含非有效): 强发射星 {len(weak_se)} ({len(weak_se)/len(all_weak)*100:.0f}%)')
# 高阶线(He,Hζ,Hη)强发射
def high_order_strong(r, thr=-10.0):
    return [ln for ln in ['Hε','Hζ','Hη'] if r['balmer_results'][ln]['EW'] < thr]
mh = [r for r in all_int if high_order_strong(r)]
wh = [r for r in all_weak if high_order_strong(r)]
print(f'  高阶线(Hε/Hζ/Hη)强发射星: 中场 {len(mh)}/{len(all_int)} ({len(mh)/len(all_int)*100:.0f}%), <10^4 T {len(wh)}/{len(all_weak)} ({len(wh)/len(all_weak)*100:.0f}%)')
summary['emission'] = {'mid_strong_any': len(mid_se), 'weak_strong_any': len(weak_se),
                       'mid_high_order': len(mh), 'weak_high_order': len(wh),
                       'n_mid': len(all_int), 'n_weak': len(all_weak)}
print()

print('='*70)
print('汇总JSON已保存:', OUT)
print('='*70)
with open(OUT, 'w', encoding='utf-8') as f:
    json.dump(summary, f, indent=2, ensure_ascii=False)
