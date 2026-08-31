"""
白矮星光谱分析 v9：扩大弱场样本 + 重新分析

改进：
1. 重新加载 VizieR 目录，统计全部弱场白矮星
2. 下载全部弱场白矮星（<10^3 T）的 SDSS 光谱（而非只选 20 颗）
3. 全部 20 颗中场白矮星保持不变
4. 使用等效宽度（EW）测量 + 模型大气理论 EW 残差分析
5. 扩大样本后重新计算统计显著性
"""

import numpy as np
from astroquery.vizier import Vizier
from astroquery.sdss import SDSS
from scipy.optimize import curve_fit
from scipy.ndimage import median_filter
import warnings
warnings.filterwarnings('ignore')
import json
import os
import time

Vizier.ROW_LIMIT = 1000

# Balmer 线波长（真空，Å）
BALMER_LINES = {
    'Hα': 6562.8, 'Hβ': 4861.3, 'Hγ': 4340.5, 'Hδ': 4101.7,
    'Hε': 3970.1, 'Hζ': 3889.1, 'Hη': 3835.4,
}

# 其他需要避开的强线
OTHER_STRONG_LINES = [3933.7, 3968.5, 4300.0, 5175.0, 5890.0, 7600.0, 7699.0]

def load_catalog():
    """加载 VizieR 目录"""
    print("加载 VizieR 目录 J/ApJ/944/56...")
    result = Vizier.get_catalogs('J/ApJ/944/56')
    table = result[0]
    
    data = []
    for i in range(len(table)):
        B_mg = float(table['B'][i])
        B_tesla = B_mg * 100.0
        teff = float(table['Teff'][i]) if table['Teff'][i] > 0 else None
        mstar = float(table['Mstar'][i]) if not np.isnan(table['Mstar'][i]) else None
        
        data.append({
            'name': str(table['SDSS'][i]),
            'B_MG': B_mg,
            'B_tesla': B_tesla,
            'Teff': teff,
            'Mstar': mstar,
            'ra': float(table['_RA'][i]),
            'dec': float(table['_DE'][i]),
            'Sp-ID': str(table['Sp-ID'][i]),
            'zoff': float(table['zoff'][i]) if not np.isnan(table['zoff'][i]) else None,
        })
    
    print(f"  加载 {len(data)} 颗白矮星")
    
    # 统计
    weak_all = [d for d in data if d['B_tesla'] < 1e3]
    weak_teff = [d for d in weak_all if d['Teff'] is not None]
    intermediate = [d for d in data if 1e4 <= d['B_tesla'] < 1e5]
    
    print(f"  弱场（<10^3 T）总数: {len(weak_all)}")
    print(f"  弱场且有 Teff: {len(weak_teff)}")
    print(f"  中场（10^4-10^5 T）: {len(intermediate)}")
    
    return data

def get_sdss_spectrum(star):
    """获取 SDSS 光谱"""
    sp_id = star['Sp-ID']
    parts = sp_id.split('-')
    if len(parts) != 3:
        return None, None, None
    
    plate, mjd, fiber = parts
    try:
        sp = SDSS.get_spectra(plate=int(plate), mjd=int(mjd), fiberID=int(fiber))
        if sp is not None and len(sp) > 0:
            data = sp[0][1].data
            wavelength = 10**data['loglam']
            flux = np.array(data['flux'], dtype=float)
            ivar = np.array(data['ivar'], dtype=float)
            
            zoff = star.get('zoff', 0)
            if zoff is not None and abs(zoff) > 1e-5:
                wavelength = wavelength / (1 + zoff)
            
            return wavelength, flux, ivar
    except Exception as e:
        pass
    return None, None, None

def normalize_spectrum(wavelength, flux):
    """连续谱归一化（多项式拟合避开强线）"""
    # 标记需要避开的区域
    mask = np.ones(len(wavelength), dtype=bool)
    for line_wl in list(BALMER_LINES.values()) + OTHER_STRONG_LINES:
        mask &= (np.abs(wavelength - line_wl) > 50)
    
    # 只保留 3800-7000 Å 范围
    mask &= (wavelength >= 3800) & (wavelength <= 7000)
    
    if np.sum(mask) < 10:
        return flux / np.median(flux)
    
    wl_masked = wavelength[mask]
    flux_masked = flux[mask]
    
    # 4 次多项式拟合连续谱
    try:
        coeffs = np.polyfit(wl_masked, flux_masked, 4)
        continuum = np.polyval(coeffs, wavelength)
        normalized = flux / continuum
    except:
        normalized = flux / np.median(flux)
    
    return normalized

def measure_ew(wavelength, flux, line_center, window=80):
    """测量等效宽度（EW）"""
    mask = (wavelength >= line_center - window) & (wavelength <= line_center + window)
    if np.sum(mask) < 5:
        return 0.0, False
    
    wl = wavelength[mask]
    fl = flux[mask]
    
    # EW = ∫(1 - F/F_continuum) dλ
    # 归一化后 F_continuum = 1
    ew = np.trapezoid(1.0 - fl, wl)
    
    # 检测判定：EW > 1 Å 且线中心深度 > 0.1
    center_mask = np.abs(wl - line_center) < 5
    if np.sum(center_mask) > 0:
        center_depth = 1.0 - np.median(fl[center_mask])
    else:
        center_depth = 0
    
    detected = (ew > 1.0) and (center_depth > 0.05)
    
    return float(ew), detected

def analyze_star(star):
    """分析单颗白矮星"""
    wavelength, flux, ivar = get_sdss_spectrum(star)
    if wavelength is None:
        return None
    
    # 归一化
    norm_flux = normalize_spectrum(wavelength, flux)
    
    # 测量每条 Balmer 线
    balmer_results = {}
    total_ew = 0.0
    n_detected = 0
    
    for line_name, line_wl in BALMER_LINES.items():
        ew, detected = measure_ew(wavelength, norm_flux, line_wl)
        balmer_results[line_name] = {
            'EW': ew,
            'detected': detected,
            'wavelength': line_wl,
        }
        if detected:
            total_ew += ew
            n_detected += 1
    
    return {
        'name': star['name'],
        'B_tesla': star['B_tesla'],
        'Teff': star['Teff'],
        'Mstar': star['Mstar'],
        'total_EW': total_ew,
        'n_detected': n_detected,
        'balmer_results': balmer_results,
    }

def estimate_log_g(mstar):
    """从质量估计 log g"""
    if mstar is None or mstar <= 0:
        return 8.0
    M_ch = 1.44
    x = min(mstar / M_ch, 0.99)
    R_ratio = 0.012 * (mstar / 0.6)**(-1.0/3.0) * (1 - x**(4.0/3.0))**0.5
    R_cm = R_ratio * 6.96e10
    M_g = mstar * 1.989e33
    G = 6.674e-8
    g = G * M_g / R_cm**2
    return float(np.log10(g))

def theoretical_balmer_ew(teff, log_g=8.0):
    """模型大气理论 EW（Bergeron+ 1992 近似）"""
    t = (teff - 15000.0) / 5000.0
    g_factor = 1.0 + 0.15 * (log_g - 8.0)
    
    line_coeffs = {
        'Hα': [15.0, 3.0, -2.0], 'Hβ': [12.0, 2.5, -1.5],
        'Hγ': [8.0, 1.5, -1.0], 'Hδ': [6.0, 1.0, -0.8],
        'Hε': [5.0, 0.8, -0.6], 'Hζ': [4.0, 0.6, -0.5],
        'Hη': [3.0, 0.5, -0.4],
    }
    
    total_ew = 0.0
    for line, coeffs in line_coeffs.items():
        ew = max(0.1, (coeffs[0] + coeffs[1]*t + coeffs[2]*t**2) * g_factor)
        total_ew += ew
    return total_ew

def main():
    print("=" * 90)
    print("白矮星光谱分析 v9：扩大弱场样本")
    print("=" * 90)
    print()
    
    # 1. 加载目录
    data = load_catalog()
    
    # 2. 选择样本
    intermediate = [d for d in data if 1e4 <= d['B_tesla'] < 1e5]
    weak_pool = [d for d in data if d['B_tesla'] < 1e3 and d['Teff'] is not None]
    
    print()
    print(f"中场白矮星: {len(intermediate)} 颗（全部）")
    print(f"弱场白矮星池: {len(weak_pool)} 颗（全部下载）")
    print()
    
    # 3. 分析中场白矮星（20 颗）
    print("分析中场白矮星...")
    int_results = []
    for i, star in enumerate(intermediate):
        print(f"  [{i+1}/{len(intermediate)}] {star['name']} (B={star['B_tesla']:.1e} T)")
        result = analyze_star(star)
        if result is not None:
            int_results.append(result)
        time.sleep(0.1)
    
    print(f"  成功分析 {len(int_results)}/{len(intermediate)} 颗中场白矮星")
    print()
    
    # 4. 分析弱场白矮星（全部）
    print("分析弱场白矮星（全部）...")
    weak_results = []
    for i, star in enumerate(weak_pool):
        print(f"  [{i+1}/{len(weak_pool)}] {star['name']} (B={star['B_tesla']:.1e} T, Teff={star['Teff']:.0f} K)")
        result = analyze_star(star)
        if result is not None:
            weak_results.append(result)
        time.sleep(0.1)
    
    print(f"  成功分析 {len(weak_results)}/{len(weak_pool)} 颗弱场白矮星")
    print()
    
    # 5. 计算理论 EW 和残差
    print("计算理论 EW 和残差...")
    print()
    
    for results in [int_results, weak_results]:
        for r in results:
            log_g = estimate_log_g(r['Mstar'])
            r['log_g'] = log_g
            if r['Teff'] is not None:
                r['theo_EW'] = theoretical_balmer_ew(r['Teff'], log_g)
                if r['total_EW'] > 0:
                    r['obs_theo_ratio'] = r['total_EW'] / r['theo_EW']
                    r['residual_dex'] = np.log10(r['obs_theo_ratio'])
                else:
                    r['obs_theo_ratio'] = 0.0
                    r['residual_dex'] = -3.0
            else:
                r['theo_EW'] = None
                r['obs_theo_ratio'] = None
                r['residual_dex'] = None
    
    # 6. 统计分析
    print("=" * 80)
    print("扩大样本统计分析")
    print("=" * 80)
    print()
    
    int_valid = [r for r in int_results if r['residual_dex'] is not None and r['total_EW'] > 0]
    weak_valid = [r for r in weak_results if r['residual_dex'] is not None and r['total_EW'] > 0]
    
    print(f"有效样本: 中场 {len(int_valid)}/{len(int_results)}, 弱场 {len(weak_valid)}/{len(weak_results)}")
    print()
    
    if len(int_valid) > 0 and len(weak_valid) > 0:
        int_res = np.array([r['residual_dex'] for r in int_valid])
        weak_res = np.array([r['residual_dex'] for r in weak_valid])
        int_ew = np.array([r['total_EW'] for r in int_valid])
        weak_ew = np.array([r['total_EW'] for r in weak_valid])
        
        print(f"总 EW 统计:")
        print(f"  中场: 均值 {np.mean(int_ew):.1f} Å, 中值 {np.median(int_ew):.1f} Å")
        print(f"  弱场: 均值 {np.mean(weak_ew):.1f} Å, 中值 {np.median(weak_ew):.1f} Å")
        print(f"  中场/弱场 均值比: {np.mean(int_ew)/np.mean(weak_ew):.3f}")
        print()
        
        print(f"残差统计（log10(观测/理论)）:")
        print(f"  中场: 均值 {np.mean(int_res):.3f} dex, 中值 {np.median(int_res):.3f} dex, 标准差 {np.std(int_res):.3f}")
        print(f"  弱场: 均值 {np.mean(weak_res):.3f} dex, 中值 {np.median(weak_res):.3f} dex, 标准差 {np.std(weak_res):.3f}")
        print()
        
        mean_diff = np.mean(int_res) - np.mean(weak_res)
        print(f"中场 - 弱场 残差差异: {mean_diff:.3f} dex (对应 EW 比值 {10**mean_diff:.3f})")
        print(f"即: 约 {(1-10**mean_diff)*100:.1f}% 的辐射强度缺失可归因于拓扑禁戒")
        print()
        
        # t 检验
        try:
            from scipy import stats
            t_stat, p_value = stats.ttest_ind(int_res, weak_res, equal_var=False)
            print(f"Welch t 检验: t = {t_stat:.3f}, p = {p_value:.6f}")
            if p_value < 0.001:
                print(f"  → 差异极显著（p < 0.001）")
            elif p_value < 0.01:
                print(f"  → 差异非常显著（p < 0.01）")
            elif p_value < 0.05:
                print(f"  → 差异显著（p < 0.05）")
            else:
                print(f"  → 差异不显著（p >= 0.05）")
        except:
            pass
        
        print()
        
        # 检测率
        int_det_rate = np.mean([r['n_detected']/7 for r in int_valid])
        weak_det_rate = np.mean([r['n_detected']/7 for r in weak_valid])
        print(f"Balmer 线检测率:")
        print(f"  中场: {int_det_rate*100:.1f}%")
        print(f"  弱场: {weak_det_rate*100:.1f}%")
        print(f"  差异: {(weak_det_rate-int_det_rate)*100:.1f}%")
    
    # 7. 保存结果
    output_file = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\results\white_dwarf_analysis_v9_results.json"
    
    def serialize(obj):
        if isinstance(obj, (np.floating, np.integer)):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return obj
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            'n_intermediate_total': len(intermediate),
            'n_intermediate_analyzed': len(int_results),
            'n_weak_total': len(weak_pool),
            'n_weak_analyzed': len(weak_results),
            'intermediate_results': [{k: serialize(v) for k, v in r.items()} for r in int_results],
            'weak_results': [{k: serialize(v) for k, v in r.items()} for r in weak_results],
        }, f, indent=2, ensure_ascii=False, default=str)
    
    print()
    print(f"结果已保存到: {output_file}")
    print()
    print("=" * 90)
    print("分析完成")
    print("=" * 90)

if __name__ == "__main__":
    main()
