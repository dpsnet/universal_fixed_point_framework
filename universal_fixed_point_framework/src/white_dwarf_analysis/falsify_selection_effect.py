"""
选择效应证伪测试（基于 v10 全样本结果）

目标：证明观测到的中场辐射缺失由磁场 B 驱动，而非由与 B 相关的混淆参数驱动。

测试：
  T1a  弱场内 B 梯度平坦性（残差不随 B 平滑漂移）
  T1b  全场（弱+中）残差 vs log10(B) Spearman 相关
  T2   弱场内混淆参数分层（log_g x Teff 四象限），检验质量/温度驱动假设
  T3   中场组内残差 vs log10(B) 相关（B 特异性）
  T5   线系内模式：逐线检测率（高阶线优先缺失签名）
  T6   发射线对照：负 EW 线的出现是否专属中场（同参数弱场对照）
"""

import json
import numpy as np
from scipy import stats

RES = r'E:\workspace\hyper-resolution\universal_fixed_point_framework\results\white_dwarf_analysis_v10_results.json'
LINES = ['Hα','Hβ','Hγ','Hδ','Hε','Hζ','Hη']

with open(RES, 'r', encoding='utf-8') as f:
    d = json.load(f)

int_res = d['int']
weak_res = d['weak']

def eff(rs):
    return [r for r in rs if r.get('resid') is not None and r['total_EW'] > 0]

iv = eff(int_res)
wv = eff(weak_res)
print(f'有效样本: 中场 {len(iv)}/{len(int_res)}, 弱场 {len(wv)}/{len(weak_res)}')
print()

def det_flag(x):
    return str(x).lower() == 'true'

def rstat(vals, label):
    vals = np.array(vals, dtype=float)
    return f'{label}: n={len(vals)}, 均值={np.mean(vals):+.3f} dex, 中值={np.median(vals):+.3f}, 负比例={np.mean(vals<0)*100:.0f}%'

# ============ T1a: 弱场内 B 梯度平坦性 ============
print('='*70)
print('T1a: 弱场内 B 梯度平坦性（选择效应若为平滑参数漂移，残差应随 B 平滑变化）')
print('='*70)
bands = [(0,100),(100,300),(300,1000)]
band_res = []
for lo, hi in bands:
    vals = [r['resid'] for r in wv if lo <= r['B_tesla'] < hi]
    if vals:
        band_res.append(np.array(vals))
        print(f'  B∈[{lo},{hi}) T: {rstat(vals, "残差")}')
# Kruskal-Wallis across bands
if len(band_res) >= 2:
    H, p = stats.kruskal(*band_res)
    print(f'  Kruskal-Wallis(弱场三个B带): H={H:.2f}, p={p:.4f} -> {"带间无差异" if p>0.05 else "带间有差异!"}')
wr_b = np.array([r['resid'] for r in wv])
wb_b = np.array([np.log10(r['B_tesla']) for r in wv])
rho, p_rho = stats.spearmanr(wb_b, wr_b)
print(f'  弱场 Spearman(残差 vs log10 B): rho={rho:+.3f}, p={p_rho:.4f} -> {"残差与B无关(平坦)" if p_rho>0.05 and abs(rho)<0.15 else "残差随B漂移!"}')
print()

# ============ T1b: 全场 B 梯度 ============
print('='*70)
print('T1b: 全场（弱+中）残差 vs log10(B) 相关')
print('='*70)
all_b = np.array([np.log10(r['B_tesla']) for r in iv + wv])
all_r = np.array([r['resid'] for r in iv + wv])
rho, p_rho = stats.spearmanr(all_b, all_r)
print(f'  n={len(all_b)}, Spearman: rho={rho:+.3f}, p={p_rho:.2e}')
# 分带均值
print('  分带残差均值:')
for lo, hi, lab in [(100,1000,'弱场 10^2-10^3 T'),(1000,10000,'缺口 10^3-10^4 T'),(10000,100000,'中场 10^4-10^5 T')]:
    vals = [r['resid'] for r in iv+wv if lo <= r['B_tesla'] < hi]
    if vals:
        print(f'    {lab}: n={len(vals)}, 残差均值={np.mean(vals):+.3f} dex')
print()

# ============ T2: 混淆参数分层 ============
print('='*70)
print('T2: 弱场内混淆参数分层（若质量/温度为驱动，高log_g/高Teff弱场子组应显示同样缺失）')
print('='*70)
lg_w = np.array([r['log_g'] for r in wv])
te_w = np.array([r['Teff'] for r in wv])
lg_med = np.median(lg_w)
te_med = np.median(te_w)
print(f'  弱场 log_g 中值={lg_med:.2f}, Teff 中值={te_med:.0f} K')
for lg_hi in [False, True]:
    for te_hi in [False, True]:
        vals = [r['resid'] for r in wv
                if (r['log_g'] >= lg_med) == lg_hi and (r['Teff'] >= te_med) == te_hi]
        if vals:
            print(f'  log_g{"高" if lg_hi else "低"} x Teff{"高" if te_hi else "低"}: {rstat(vals, "")}')

# 关键检验: 与中场 log_g 重叠区的弱场星
mid_lg = [r['log_g'] for r in iv]
print(f'  中场 log_g 范围: {min(mid_lg):.2f}-{max(mid_lg):.2f}')
overlap = [r for r in wv if min(mid_lg) <= r['log_g'] <= max(mid_lg)]
if overlap:
    ov_res = [r['resid'] for r in overlap]
    print(f'  弱场中 log_g 落入中场范围({min(mid_lg):.2f}-{max(mid_lg):.2f})的星: n={len(ov_res)}, '
          f'残差均值={np.mean(ov_res):+.3f} dex')
    t2, p2 = stats.ttest_ind(ov_res, [r['resid'] for r in iv], equal_var=False)
    print(f'    vs 中场 Welch t: t={t2:.2f}, p={p2:.4f}')
print()

# ============ T3: 中场组内 B-残差相关 ============
print('='*70)
print('T3: 中场组内残差 vs log10(B)（拓扑禁戒预言 B 特异性增强）')
print('='*70)
mb = np.array([np.log10(r['B_tesla']) for r in iv])
mr = np.array([r['resid'] for r in iv])
rho3, p3 = stats.spearmanr(mb, mr)
slope, intercept, rv, pv, se = stats.linregress(mb, mr)
print(f'  n={len(iv)}')
for r in sorted(iv, key=lambda x: x['B_tesla']):
    print(f'    {r["name"]}: B={r["B_tesla"]:.1e} T, 残差={r["resid"]:+.3f} dex')
print(f'  Spearman: rho={rho3:+.3f}, p={p3:.4f}')
print(f'  线性回归: slope={slope:+.3f} dex/log10T, p={pv:.4f}')
print()

# ============ T5: 线系内模式 ============
print('='*70)
print('T5: 线系内检测率模式（拓扑禁戒预言高阶线优先缺失）')
print('='*70)
print(f'  {"线":<6}{"中场检测率":>12}{"弱场检测率":>12}{"差异":>10}')
for ln in LINES:
    md = [det_flag(r['balmer_results'][ln].get('detected')) for r in iv]
    wd = [det_flag(r['balmer_results'][ln].get('detected')) for r in wv]
    mr_ = np.mean(md)*100
    wr_ = np.mean(wd)*100
    print(f'  {ln:<6}{mr_:>10.1f}%{wr_:>10.1f}%{mr_-wr_:>+9.1f}pp')
# Hα 检测但高阶缺失
cnt = 0
for r in iv:
    ha = det_flag(r['balmer_results']['Hα'].get('detected'))
    he = [det_flag(r['balmer_results'][ln].get('detected')) for ln in ['Hε','Hζ','Hη']]
    if ha and not any(he):
        cnt += 1
print(f'  中场中"Hα检测但Hε/Hζ/Hη全缺"的星: {cnt}/{len(iv)}')
print()

# ============ T6: 发射线对照（强发射判定） ============
print('='*70)
print('T6: 强发射(EW<-5A)对照——强发射现象是否专属中场（B>10^4 T）')
print('='*70)
def strong_emit(r, thr=-5.0):
    return [ln for ln in LINES if r['balmer_results'][ln]['EW'] < thr]
def weak_neg(r):
    return [ln for ln in LINES if r['balmer_results'][ln]['EW'] < -0.5]
mid_se = [(r, strong_emit(r)) for r in iv if strong_emit(r)]
weak_se = [(r, strong_emit(r)) for r in wv if strong_emit(r)]
print(f'  中场有效星中强发射线(EW<-5A): {len(mid_se)}/{len(iv)}')
for r, nls in mid_se:
    print(f'    {r["name"]}: B={r["B_tesla"]:.1e} T, Teff={r["Teff"]:.0f} K, log_g={r["log_g"]:.2f}, 强发射线={nls}')
print(f'  弱场有效星中强发射线(EW<-5A): {len(weak_se)}/{len(wv)}')
all_weak_se = [r for r in weak_res if strong_emit(r)]
print(f'  全部{len(weak_res)}颗弱场(含非有效)中强发射线星: {len(all_weak_se)}')
# 全样本（含中场非有效）强发射
all_mid_se = [r for r in int_res if strong_emit(r)]
print(f'  全部{len(int_res)}颗中场(含非有效)中强发射线星: {len(all_mid_se)}')
# 强发射星参数框内的弱场对照
if mid_se:
    teffs = [r['Teff'] for r, _ in mid_se]
    lgs = [r['log_g'] for r, _ in mid_se]
    print(f'  强发射星参数: Teff∈[{min(teffs):.0f},{max(teffs):.0f}] K, log_g∈[{min(lgs):.2f},{max(lgs):.2f}]')
    box = [r for r in wv if min(teffs)-2000 <= r['Teff'] <= max(teffs)+2000
           and min(lgs)-0.3 <= r['log_g'] <= max(lgs)+0.3]
    box_se = [r for r in box if strong_emit(r)]
    print(f'  同参数框弱场对照: n={len(box)}, 其中强发射线星={len(box_se)} '
          f'({"无强发射特征" if not box_se else "存在强发射特征!"})')
print()

# ============ T5b: 逐线EW比值（高阶线抑制模式） ============
print('='*70)
print('T5b: 逐线平均EW与检测率——高阶线优先抑制检验')
print('='*70)
print(f'  {"线":<6}{"中场均值EW":>10}{"弱场均值EW":>10}{"比值":>8}{"中场检测率":>10}{"弱场检测率":>10}')
for ln in LINES:
    m_ew = [r['balmer_results'][ln]['EW'] for r in iv]
    w_ew = [r['balmer_results'][ln]['EW'] for r in wv]
    md = [det_flag(r['balmer_results'][ln].get('detected')) for r in iv]
    wd = [det_flag(r['balmer_results'][ln].get('detected')) for r in wv]
    mm = np.mean(m_ew); wm = np.mean(w_ew)
    ratio = mm/wm if wm > 0 else float('nan')
    print(f'  {ln:<6}{mm:>9.1f}A{wm:>9.1f}A{ratio:>8.2f}{np.mean(md)*100:>9.1f}%{np.mean(wd)*100:>9.1f}%')
# 检测到正EW的线平均
def pos_ew_ratio(r):
    pos = [r['balmer_results'][ln]['EW'] for ln in LINES if r['balmer_results'][ln]['EW'] > 0]
    return np.mean(pos) if pos else 0.0
m_pos = np.mean([pos_ew_ratio(r) for r in iv])
w_pos = np.mean([pos_ew_ratio(r) for r in wv])
print(f'  正EW线均值: 中场 {m_pos:.1f} A, 弱场 {w_pos:.1f} A, 比值 {m_pos/w_pos:.2f}')
print()

# ============ T2b: 匹配对照检验（逐星最近邻匹配） ============
print('='*70)
print('T2b: 匹配对照——每颗中场星按Teff+log_g最近邻匹配弱场星')
print('='*70)
matched_diff = []
for r in iv:
    # 在弱场中找 Teff、log_g 最近邻（排除自身组别偏差，归一化距离）
    def dist(w):
        return ((np.log10(w['Teff']) - np.log10(r['Teff']))/0.1)**2 + ((w['log_g']-r['log_g'])/0.5)**2
    ww = min(wv, key=dist)
    matched_diff.append(r['resid'] - ww['resid'])
    print(f'    {r["name"]}: 残差={r["resid"]:+.3f} vs 匹配弱场 {ww["name"][:12]}(Teff={ww["Teff"]:.0f},lg={ww["log_g"]:.2f}) 残差={ww["resid"]:+.3f} -> 差={r["resid"]-ww["resid"]:+.3f}')
md = np.array(matched_diff)
print(f'  匹配后残差差异: 均值={np.mean(md):+.3f} dex (对应EW比值 {10**np.mean(md):.3f})')
print(f'  负差异比例: {np.mean(md<0)*100:.0f}% ({np.sum(md<0)}/{len(md)})')
t_m, p_m = stats.ttest_1samp(md, 0)
print(f'  单样本t检验(差异=0): t={t_m:.2f}, p={p_m:.4f}')
# 符号检验
binom_p = stats.binomtest(np.sum(md<0), len(md), 0.5).pvalue
print(f'  符号检验: p={binom_p:.4f}')
print()

# ============ 汇总 ============
print('='*70)
print('证伪测试汇总')
print('='*70)
print(f'T1a 弱场内B梯度: 带间 p={p:.4f}, 组内Spearman rho={rho:+.3f} (p={p_rho:.4f})')
print(f'T1b 全场B相关:  Spearman rho={rho:+.3f} (p={p_rho:.2e})')
print(f'T3  中场B相关:   Spearman rho={rho3:+.3f} (p={p3:.4f}), 回归slope={slope:+.3f} dex/log10T (p={pv:.4f})')
print(f'T2b 匹配对照:    匹配后残差差异={np.mean(md):+.3f} dex, t={t_m:.2f}, p={p_m:.4f}, 负差异{np.sum(md<0)}/{len(md)}')
print(f'T6  强发射对照:  中场强发射(EW<-5A) {len(mid_se)}/{len(iv)}, 弱场 {len(weak_se)}/{len(wv)}')
