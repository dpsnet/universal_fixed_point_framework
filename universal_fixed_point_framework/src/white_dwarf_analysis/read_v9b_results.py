import json
import numpy as np

with open(r'E:\workspace\hyper-resolution\universal_fixed_point_framework\results\white_dwarf_analysis_v9b_results.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

print(f'中场: {d["n_int"]} 颗')
print(f'弱场: {d["n_weak"]} 颗')
print()

int_res = d['int']
weak_res = d['weak']
iv = [r for r in int_res if r.get('resid') is not None and r['total_EW'] > 0]
wv = [r for r in weak_res if r.get('resid') is not None and r['total_EW'] > 0]
print(f'有效: 中场 {len(iv)}/{len(int_res)}, 弱场 {len(wv)}/{len(weak_res)}')
print()

ir = np.array([r['resid'] for r in iv])
wr = np.array([r['resid'] for r in wv])
ie = np.array([r['total_EW'] for r in iv])
we = np.array([r['total_EW'] for r in wv])

print(f'总EW: 中场均值 {np.mean(ie):.1f} A, 弱场均值 {np.mean(we):.1f} A')
print(f'总EW比值: {np.mean(ie)/np.mean(we):.3f}')
print()
print(f'残差: 中场均值 {np.mean(ir):.3f} dex, 弱场均值 {np.mean(wr):.3f} dex')
diff = np.mean(ir) - np.mean(wr)
print(f'残差差异: {diff:.3f} dex')
print(f'EW比值: {10**diff:.3f}')
print(f'辐射强度缺失: {(1-10**diff)*100:.1f}%')
print()

try:
    from scipy import stats
    t, p = stats.ttest_ind(ir, wr, equal_var=False)
    print(f'Welch t检验: t={t:.3f}, p={p:.6f}')
    if p < 0.001:
        print('  -> 极显著 p<0.001')
    elif p < 0.01:
        print('  -> 非常显著 p<0.01')
    elif p < 0.05:
        print('  -> 显著 p<0.05')
except Exception as e:
    print(f't检验失败: {e}')

print()
idet = np.mean([r['n_detected']/7 for r in iv])
wdet = np.mean([r['n_detected']/7 for r in wv])
print(f'检测率: 中场 {idet*100:.1f}%, 弱场 {wdet*100:.1f}%')

print()
int_teff = [r['Teff'] for r in iv if r['Teff']]
weak_teff = [r['Teff'] for r in wv if r['Teff']]
print(f'Teff范围: 中场 {min(int_teff):.0f}-{max(int_teff):.0f} K, 弱场 {min(weak_teff):.0f}-{max(weak_teff):.0f} K')

# 中场残差为负的比例
neg_frac = np.sum(ir < 0) / len(ir)
print(f'中场残差为负的比例: {neg_frac*100:.1f}%')
