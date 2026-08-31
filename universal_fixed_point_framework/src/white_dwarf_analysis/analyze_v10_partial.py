"""
分析 v10 部分结果（200 弱场 + 20 中场）
"""
import json
import numpy as np

with open(r'E:\workspace\hyper-resolution\universal_fixed_point_framework\results\white_dwarf_analysis_v10_partial.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

print(f"弱场已完成: {d['n_weak_done']}/400")
print(f"中场: {d['n_int']} 颗")
print(f"弱场成功: {d['n_weak']} 颗")
print()

int_res = d['int']
weak_res = d['weak']

def log_g(m):
    if not m or m <= 0: return 8.0
    x = min(m/1.44, 0.99)
    R = 0.012*(m/0.6)**(-1/3)*(1-x**(4/3))**0.5
    g = 6.674e-8*(m*1.989e33)/(R*6.96e10)**2
    return float(np.log10(g))

def theo_ew(teff, lg=8.0):
    t = (teff-15000)/5000
    gf = 1.0+0.15*(lg-8.0)
    coeffs = [[15,3,-2],[12,2.5,-1.5],[8,1.5,-1],[6,1,-0.8],[5,0.8,-0.6],[4,0.6,-0.5],[3,0.5,-0.4]]
    return sum(max(0.1,(c[0]+c[1]*t+c[2]*t**2)*gf) for c in coeffs)

# 计算残差
for res in [int_res, weak_res]:
    for r in res:
        if 'resid' not in r or r.get('resid') is None:
            lg = log_g(r.get('Mstar'))
            r['log_g'] = lg
            if r.get('Teff'):
                r['theo_EW'] = theo_ew(r['Teff'], lg)
                if r['total_EW'] > 0:
                    r['ratio'] = r['total_EW'] / r['theo_EW']
                    r['resid'] = float(np.log10(r['ratio']))
                else:
                    r['ratio'] = 0.0
                    r['resid'] = -3.0

iv = [r for r in int_res if r.get('resid') is not None and r['total_EW'] > 0]
wv = [r for r in weak_res if r.get('resid') is not None and r['total_EW'] > 0]

print(f"有效样本: 中场 {len(iv)}/{len(int_res)}, 弱场 {len(wv)}/{len(weak_res)}")
print()

if iv and wv:
    ir = np.array([r['resid'] for r in iv])
    wr = np.array([r['resid'] for r in wv])
    ie = np.array([r['total_EW'] for r in iv])
    we = np.array([r['total_EW'] for r in wv])

    print("="*60)
    print("v10 部分结果（200 弱场 + 12 中场有效）")
    print("="*60)
    print()
    print(f"总 EW: 中场均值 {np.mean(ie):.1f} Å, 弱场均值 {np.mean(we):.1f} Å")
    print(f"总 EW 比值: {np.mean(ie)/np.mean(we):.3f}")
    print()
    print(f"残差: 中场均值 {np.mean(ir):.3f} dex, 弱场均值 {np.mean(wr):.3f} dex")
    diff = np.mean(ir) - np.mean(wr)
    print(f"残差差异: {diff:.3f} dex")
    print(f"EW 比值: {10**diff:.3f}")
    print(f"辐射强度缺失: {(1-10**diff)*100:.1f}%")
    print()

    try:
        from scipy import stats
        t, p = stats.ttest_ind(ir, wr, equal_var=False)
        print(f"Welch t 检验: t={t:.3f}, p={p:.8f}")
        if p < 0.001:
            print("  -> 极显著 p<0.001!")
        elif p < 0.01:
            print("  -> 非常显著 p<0.01")
        elif p < 0.05:
            print("  -> 显著 p<0.05")
    except Exception as e:
        print(f"t 检验失败: {e}")

    print()
    neg_frac = np.sum(ir < 0) / len(ir)
    print(f"中场残差为负比例: {neg_frac*100:.1f}% ({np.sum(ir<0)}/{len(ir)})")

    idet = np.mean([r['n_detected']/7 for r in iv])
    wdet = np.mean([r['n_detected']/7 for r in wv])
    print(f"检测率: 中场 {idet*100:.1f}%, 弱场 {wdet*100:.1f}%")

    print()
    int_teff = [r['Teff'] for r in iv if r.get('Teff')]
    weak_teff = [r['Teff'] for r in wv if r.get('Teff')]
    print(f"Teff 范围: 中场 {min(int_teff):.0f}-{max(int_teff):.0f} K, 弱场 {min(weak_teff):.0f}-{max(weak_teff):.0f} K")

    print()
    print("="*60)
    print("各版本对比")
    print("="*60)
    print(f"{'版本':<12} {'弱场数':>8} {'中场有效':>10} {'辐射缺失':>10} {'p值':>12}")
    print("-"*58)
    print(f"{'v6':<12} {'17':>8} {'~17':>10} {'65.5%':>10} {'-':>12}")
    print(f"{'v7':<12} {'17':>8} {'~17':>10} {'63.7%':>10} {'0.047':>12}")
    print(f"{'v8':<12} {'17':>8} {'17':>10} {'66.0%':>10} {'0.037':>12}")
    print(f"{'v9b':<12} {'99':>8} {'9':>10} {'52.8%':>10} {'0.014':>12}")
    print(f"{'v10(200)':<12} {str(len(wv)):>8} {str(len(iv)):>10} {f'{(1-10**diff)*100:.1f}%':>10} {f'{p:.6f}':>12}")

    # 保存分析结果
    analysis_out = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\results\v10_partial_analysis.json"
    with open(analysis_out, 'w', encoding='utf-8') as f:
        json.dump({
            'n_weak_done': d['n_weak_done'],
            'n_int_valid': len(iv),
            'n_weak_valid': len(wv),
            'total_ew_ratio': float(np.mean(ie)/np.mean(we)),
            'residual_diff_dex': float(diff),
            'radiation_deficit_percent': float((1-10**diff)*100),
            'p_value': float(p),
            't_statistic': float(t),
            'int_residual_negative_fraction': float(neg_frac),
            'int_detection_rate': float(idet),
            'weak_detection_rate': float(wdet),
        }, f, indent=2, ensure_ascii=False)
    print()
    print(f"分析结果已保存: {analysis_out}")
