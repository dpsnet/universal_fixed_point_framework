"""
白矮星光谱分析 v7：温度/质量匹配 + 模型大气效应分离

方法：
1. 从 v6 结果加载 37 颗白矮星的 Balmer 线 EW 测量
2. 按温度（Teff）和质量（Mstar）精确匹配中场与弱场对照
3. 建立弱场 Balmer 线总 EW 的经验关系（EW vs Teff）
4. 对每颗白矮星计算"残差"= 观测 EW / 经验预测 EW
5. 比较中场与弱场的残差分布，分离大气效应与拓扑禁戒
"""

import numpy as np
import json
from scipy.optimize import curve_fit
from scipy.interpolate import interp1d
import warnings
warnings.filterwarnings('ignore')

# Balmer 线
BALMER_LINES = ['Hα', 'Hβ', 'Hγ', 'Hδ', 'Hε', 'Hζ', 'Hη']

def load_results():
    """加载 v6 结果"""
    input_file = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\results\white_dwarf_analysis_v6_results.json"
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    int_results = data['intermediate_results']
    weak_results = data['weak_results']
    
    print(f"加载数据:")
    print(f"  中场白矮星: {len(int_results)} 颗")
    print(f"  弱场白矮星: {len(weak_results)} 颗")
    
    return int_results, weak_results

def extract_params(results):
    """提取每颗白矮星的参数和 EW"""
    extracted = []
    for r in results:
        teff = r.get('Teff')
        mstar = r.get('Mstar')
        b = r.get('B_tesla', 0)
        
        # 总 EW
        total_ew = r.get('total_EW', 0)
        
        # 每条线的 EW
        line_ews = {}
        for line in BALMER_LINES:
            if line in r['balmer_results']:
                lr = r['balmer_results'][line]
                if lr.get('detected', False):
                    line_ews[line] = lr.get('EW', 0)
                else:
                    line_ews[line] = 0.0
            else:
                line_ews[line] = 0.0
        
        extracted.append({
            'name': r['name'],
            'B_tesla': b,
            'Teff': teff,
            'Mstar': mstar,
            'total_EW': total_ew,
            'line_EWs': line_ews,
            'n_detected': r.get('n_detected', 0),
        })
    
    return extracted

def match_by_teff_mass(int_stars, weak_stars, teff_tol=3000, mass_tol=0.3):
    """按温度和质量匹配中场与弱场白矮星
    
    对每颗中场白矮星，在弱场中找到 Teff 差异 < teff_tol 且 
    Mstar 差异 < mass_tol 的最佳匹配。
    """
    print()
    print("=" * 80)
    print("1. 温度/质量精确匹配")
    print("=" * 80)
    print()
    
    matches = []
    used_weak = set()
    
    for i, int_star in enumerate(int_stars):
        if int_star['Teff'] is None:
            continue
        
        best_match = None
        best_dist = float('inf')
        
        for j, weak_star in enumerate(weak_stars):
            if j in used_weak:
                continue
            if weak_star['Teff'] is None:
                continue
            
            teff_diff = abs(int_star['Teff'] - weak_star['Teff'])
            if teff_diff > teff_tol:
                continue
            
            # 质量差异（如果都有质量测量）
            if int_star['Mstar'] is not None and weak_star['Mstar'] is not None:
                mass_diff = abs(int_star['Mstar'] - weak_star['Mstar'])
                if mass_diff > mass_tol:
                    continue
            else:
                mass_diff = 0.5  # 惩罚无质量测量的匹配
            
            # 综合距离（归一化）
            dist = (teff_diff / teff_tol)**2 + (mass_diff / mass_tol)**2
            
            if dist < best_dist:
                best_dist = dist
                best_match = j
        
        if best_match is not None:
            used_weak.add(best_match)
            matches.append({
                'int': int_star,
                'weak': weak_stars[best_match],
                'teff_diff': abs(int_star['Teff'] - weak_stars[best_match]['Teff']),
                'mass_diff': (abs(int_star['Mstar'] - weak_stars[best_match]['Mstar']) 
                              if int_star['Mstar'] is not None and weak_stars[best_match]['Mstar'] is not None else None),
            })
    
    print(f"成功匹配 {len(matches)} 对（温度容差 {teff_tol} K，质量容差 {mass_tol} M_sun）")
    print()
    
    # 打印匹配对
    print(f"  {'中场':<25} {'Teff':>7} {'B(T)':>10} | {'弱场':<25} {'Teff':>7} {'ΔTeff':>7}")
    print("  " + "-" * 95)
    for m in matches:
        int_s = m['int']
        weak_s = m['weak']
        print(f"  {int_s['name']:<25} {int_s['Teff']:>7.0f} {int_s['B_tesla']:>10.2e} | "
              f"{weak_s['name']:<25} {weak_s['Teff']:>7.0f} {m['teff_diff']:>7.0f}")
    
    print()
    
    # 计算匹配对的 EW 比值
    print("匹配对的总 EW 对比:")
    print()
    print(f"  {'中场 EW(Å)':>12} {'弱场 EW(Å)':>12} {'比值':>8} {'log10(比值)':>12}")
    print("  " + "-" * 50)
    
    ratios = []
    for m in matches:
        int_ew = m['int']['total_EW']
        weak_ew = m['weak']['total_EW']
        if weak_ew > 0:
            ratio = int_ew / weak_ew
            ratios.append(ratio)
            print(f"  {int_ew:>12.1f} {weak_ew:>12.1f} {ratio:>8.3f} {np.log10(ratio):>12.3f}")
    
    print()
    if ratios:
        ratios = np.array(ratios)
        print(f"  EW 比值统计:")
        print(f"    均值: {np.mean(ratios):.3f}")
        print(f"    中值: {np.median(ratios):.3f}")
        print(f"    标准差: {np.std(ratios):.3f}")
        print(f"    范围: {np.min(ratios):.3f} - {np.max(ratios):.3f}")
        print(f"    比值 < 1 的比例: {np.sum(ratios < 1)/len(ratios)*100:.1f}%")
        print(f"    比值 < 0.5 的比例: {np.sum(ratios < 0.5)/len(ratios)*100:.1f}%")
        print()
        print(f"  → 匹配对中，中场白矮星总 EW 平均为弱场的 {np.median(ratios)*100:.1f}%")
        print(f"  → 即约 {(1-np.median(ratios))*100:.1f}% 的辐射强度缺失（已匹配温度/质量）")
    
    return matches, ratios

def empirical_ew_relation(weak_stars):
    """建立弱场 Balmer 线总 EW 与 Teff 的经验关系
    
    使用多项式拟合 log(EW) vs Teff。
    """
    print()
    print("=" * 80)
    print("2. 弱场 Balmer 线 EW 经验关系")
    print("=" * 80)
    print()
    
    # 筛选有 Teff 和 EW 测量的弱场白矮星
    valid = [s for s in weak_stars if s['Teff'] is not None and s['total_EW'] > 0]
    
    if len(valid) < 5:
        print("有效样本不足，无法建立经验关系")
        return None
    
    teffs = np.array([s['Teff'] for s in valid])
    ews = np.array([s['total_EW'] for s in valid])
    log_ews = np.log10(ews)
    
    print(f"有效弱场样本: {len(valid)} 颗")
    print(f"Teff 范围: {teffs.min():.0f} - {teffs.max():.0f} K")
    print(f"总 EW 范围: {ews.min():.1f} - {ews.max():.1f} Å")
    print()
    
    # 多项式拟合（2 次）
    def poly2(x, a, b, c):
        return a + b*x + c*x**2
    
    # 归一化 Teff 以提高拟合稳定性
    teff_norm = (teffs - 15000) / 5000
    
    try:
        popt, pcov = curve_fit(poly2, teff_norm, log_ews, maxfev=10000)
        a, b, c = popt
        
        print(f"拟合结果: log10(EW) = {a:.4f} + {b:.4f}*(Teff-15000)/5000 + {c:.4f}*((Teff-15000)/5000)^2")
        
        # 拟合优度
        log_ew_fit = poly2(teff_norm, *popt)
        residuals = log_ews - log_ew_fit
        rms = np.sqrt(np.mean(residuals**2))
        print(f"拟合 RMS: {rms:.3f} dex")
        print()
        
        # 打印每颗的预测和残差
        print(f"  {'名称':<25} {'Teff':>7} {'观测EW':>10} {'预测EW':>10} {'比值':>8} {'残差(dex)':>10}")
        print("  " + "-" * 75)
        for i, s in enumerate(valid):
            tn = (s['Teff'] - 15000) / 5000
            pred_ew = 10**poly2(tn, *popt)
            ratio = s['total_EW'] / pred_ew
            resid = np.log10(ratio)
            print(f"  {s['name']:<25} {s['Teff']:>7.0f} {s['total_EW']:>10.1f} {pred_ew:>10.1f} {ratio:>8.3f} {resid:>10.3f}")
        
        print()
        
        return {
            'popt': popt,
            'rms': rms,
            'n_samples': len(valid),
        }
        
    except Exception as e:
        print(f"拟合失败: {e}")
        return None

def compute_residuals(stars, relation):
    """计算每颗白矮星的 EW 残差（观测/预测）"""
    if relation is None:
        return []
    
    popt = relation['popt']
    residuals = []
    
    for s in stars:
        if s['Teff'] is None or s['total_EW'] <= 0:
            continue
        
        tn = (s['Teff'] - 15000) / 5000
        pred_ew = 10**(popt[0] + popt[1]*tn + popt[2]*tn**2)
        ratio = s['total_EW'] / pred_ew
        resid = np.log10(ratio)
        
        residuals.append({
            'name': s['name'],
            'Teff': s['Teff'],
            'B_tesla': s['B_tesla'],
            'obs_EW': s['total_EW'],
            'pred_EW': pred_ew,
            'ratio': ratio,
            'residual_dex': resid,
        })
    
    return residuals

def compare_residuals(int_residuals, weak_residuals, relation_rms):
    """比较中场与弱场的残差分布"""
    print()
    print("=" * 80)
    print("3. 残差分析：分离大气效应与拓扑禁戒")
    print("=" * 80)
    print()
    
    print(f"弱场经验关系 RMS: {relation_rms:.3f} dex")
    print(f"  （这是大气效应、测量误差、样本异质性的总散度）")
    print()
    
    if len(int_residuals) == 0 or len(weak_residuals) == 0:
        print("残差样本不足")
        return
    
    int_res = np.array([r['residual_dex'] for r in int_residuals])
    weak_res = np.array([r['residual_dex'] for r in weak_residuals])
    int_ratio = np.array([r['ratio'] for r in int_residuals])
    weak_ratio = np.array([r['ratio'] for r in weak_residuals])
    
    print(f"残差统计（log10(观测/预测)）:")
    print()
    print(f"  {'组别':<15} {'数量':>6} {'均值(dex)':>10} {'中值(dex)':>10} {'标准差':>8} {'均值比值':>10}")
    print("  " + "-" * 65)
    print(f"  {'弱场':<15} {len(weak_res):>6} {np.mean(weak_res):>10.3f} {np.median(weak_res):>10.3f} {np.std(weak_res):>8.3f} {np.mean(weak_ratio):>10.3f}")
    print(f"  {'中场':<15} {len(int_res):>6} {np.mean(int_res):>10.3f} {np.median(int_res):>10.3f} {np.std(int_res):>8.3f} {np.mean(int_ratio):>10.3f}")
    
    print()
    
    # 中场残差与弱场的差异
    mean_diff = np.mean(int_res) - np.mean(weak_res)
    median_diff = np.median(int_res) - np.median(weak_res)
    
    print(f"中场 - 弱场 残差差异:")
    print(f"  均值差异: {mean_diff:.3f} dex")
    print(f"  中值差异: {median_diff:.3f} dex")
    print(f"  对应 EW 比值差异: {10**mean_diff:.3f}")
    print()
    
    # 显著性检验（简单的 t 检验）
    from scipy import stats
    t_stat, p_value = stats.ttest_ind(int_res, weak_res, equal_var=False)
    print(f"Welch t 检验:")
    print(f"  t = {t_stat:.3f}")
    print(f"  p = {p_value:.4f}")
    if p_value < 0.05:
        print(f"  → 中场与弱场残差差异显著（p < 0.05）")
    else:
        print(f"  → 中场与弱场残差差异不显著（p >= 0.05）")
    print()
    
    # 扣除大气效应后的拓扑禁戒估计
    # 弱场残差均值代表大气效应的系统偏差（应为 ~0）
    # 中场残差均值扣除弱场均值后，剩余部分为拓扑禁戒
    topo_effect_dex = np.mean(int_res) - np.mean(weak_res)
    topo_effect_ratio = 10**topo_effect_dex
    
    print(f"拓扑禁戒效应估计（扣除大气效应后）:")
    print(f"  中场残差均值: {np.mean(int_res):.3f} dex")
    print(f"  弱场残差均值: {np.mean(weak_res):.3f} dex（大气效应基准）")
    print(f"  扣除大气后: {topo_effect_dex:.3f} dex")
    print(f"  对应 EW 比值: {topo_effect_ratio:.3f}")
    print(f"  即: 约 {(1-topo_effect_ratio)*100:.1f}% 的辐射强度缺失可归因于拓扑禁戒")
    print()
    
    # 详细列表
    print("中场白矮星残差详细列表:")
    print()
    print(f"  {'名称':<25} {'Teff':>7} {'B(T)':>10} {'观测EW':>10} {'预测EW':>10} {'比值':>8} {'残差':>8}")
    print("  " + "-" * 85)
    for r in int_residuals:
        print(f"  {r['name']:<25} {r['Teff']:>7.0f} {r['B_tesla']:>10.2e} "
              f"{r['obs_EW']:>10.1f} {r['pred_EW']:>10.1f} {r['ratio']:>8.3f} {r['residual_dex']:>8.3f}")
    
    print()

def main():
    print("=" * 90)
    print("白矮星光谱分析 v7：温度/质量匹配 + 大气效应分离")
    print("=" * 90)
    print()
    
    # 1. 加载数据
    int_results, weak_results = load_results()
    int_stars = extract_params(int_results)
    weak_stars = extract_params(weak_results)
    
    # 2. 温度/质量匹配
    matches, match_ratios = match_by_teff_mass(int_stars, weak_stars)
    
    # 3. 建立弱场经验关系
    relation = empirical_ew_relation(weak_stars)
    
    # 4. 计算残差
    int_residuals = compute_residuals(int_stars, relation)
    weak_residuals = compute_residuals(weak_stars, relation)
    
    # 5. 比较残差
    compare_residuals(int_residuals, weak_residuals, relation['rms'] if relation else 0.3)
    
    # 6. 保存结果
    output_file = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\results\white_dwarf_analysis_v7_results.json"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            'n_matched_pairs': len(matches),
            'match_ratios': [float(r) for r in match_ratios],
            'match_ratio_median': float(np.median(match_ratios)) if len(match_ratios) > 0 else None,
            'empirical_relation': {
                'popt': [float(p) for p in relation['popt']] if relation else None,
                'rms': float(relation['rms']) if relation else None,
                'n_samples': relation['n_samples'] if relation else 0,
            },
            'intermediate_residuals': int_residuals,
            'weak_residuals': weak_residuals,
            'residual_mean_diff': float(np.mean([r['residual_dex'] for r in int_residuals]) - 
                                         np.mean([r['residual_dex'] for r in weak_residuals])) if int_residuals and weak_residuals else None,
        }, f, indent=2, ensure_ascii=False, default=str)
    
    print(f"结果已保存到: {output_file}")
    print()
    print("=" * 90)
    print("分析完成")
    print("=" * 90)

if __name__ == "__main__":
    main()
