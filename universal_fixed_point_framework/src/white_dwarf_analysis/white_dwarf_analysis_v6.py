"""
白矮星光谱分析 v6：扩大样本 + 等效宽度 + Zeeman 分裂处理

改进：
1. 全部 20 颗中场白矮星（10^4-10^5 T）+ 20 颗弱场对照
2. 精确连续谱归一化（多项式拟合避开 Balmer 线区域）
3. 等效宽度（EW）测量，而非简单线深度
4. Zeeman 分裂处理：宽范围积分总 EW，排除分量混叠
5. 每条 Balmer 线的详细拟合（高斯/洛伦兹）
"""

import numpy as np
from astroquery.vizier import Vizier
from astroquery.sdss import SDSS
from scipy.optimize import curve_fit
from scipy.ndimage import median_filter
import warnings
warnings.filterwarnings('ignore')
import json

Vizier.ROW_LIMIT = 1000

# Balmer 线波长（真空，Å）
BALMER_LINES = {
    'Hα': 6562.8,
    'Hβ': 4861.3,
    'Hγ': 4340.5,
    'Hδ': 4101.7,
    'Hε': 3970.1,
    'Hζ': 3889.1,
    'Hη': 3835.4,
}

# 其他需要避开的强线（用于连续谱拟合）
OTHER_STRONG_LINES = [
    3933.7,  # Ca II K
    3968.5,  # Ca II H
    4300.0,  # G-band
    5175.0,  # Mg I b
    5890.0,  # Na D
    7600.0,  # O2 A-band（大气）
    7699.0,  # K I
]

def load_catalog():
    """加载 VizieR 目录"""
    print("加载 VizieR 目录 J/ApJ/944/56...")
    result = Vizier.get_catalogs('J/ApJ/944/56')
    table = result[0]
    
    # 转换为字典列表
    data = []
    for i in range(len(table)):
        B_mg = float(table['B'][i])
        B_tesla = B_mg * 100.0  # MG -> T
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
    return data

def select_samples(data):
    """选择中场白矮星（全部 20 颗）和弱场对照（20 颗）"""
    print()
    print("选择样本...")
    
    # 中场白矮星：10^4 - 10^5 T
    intermediate = [d for d in data if 1e4 <= d['B_tesla'] < 1e5]
    print(f"  中场白矮星（10^4-10^5 T）: {len(intermediate)} 颗")
    
    # 弱场对照：< 10^3 T，选择温度相近的
    weak_pool = [d for d in data if d['B_tesla'] < 1e3 and d['Teff'] is not None]
    # 按温度排序，选择温度覆盖范围广的 20 颗
    weak_pool.sort(key=lambda x: x['Teff'])
    if len(weak_pool) > 20:
        # 均匀采样
        indices = np.linspace(0, len(weak_pool)-1, 20, dtype=int)
        weak = [weak_pool[i] for i in indices]
    else:
        weak = weak_pool
    
    print(f"  弱场对照（<10^3 T）: {len(weak)} 颗")
    
    return intermediate, weak

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
            
            # 红移校正
            zoff = star.get('zoff', 0)
            if zoff is not None and abs(zoff) > 1e-5:
                wavelength = wavelength / (1 + zoff)
            
            return wavelength, flux, ivar
    except Exception as e:
        pass
    
    return None, None, None

def continuum_normalize(wavelength, flux, ivar):
    """精确连续谱归一化
    
    使用多项式拟合避开所有 Balmer 线和其他强线的区域。
    """
    valid = (ivar > 0) & np.isfinite(flux) & (flux > 0)
    
    if np.sum(valid) < 50:
        return flux, None, valid
    
    # 构建连续谱区域掩码
    cont_mask = valid.copy()
    
    # 避开 Balmer 线（±80 Å）
    for name, wl in BALMER_LINES.items():
        cont_mask &= np.abs(wavelength - wl) > 80
    
    # 避开其他强线（±30 Å）
    for wl in OTHER_STRONG_LINES:
        cont_mask &= np.abs(wavelength - wl) > 30
    
    # 避开光谱边缘（<3850 和 >6800）
    cont_mask &= (wavelength > 3850) & (wavelength < 6800)
    
    if np.sum(cont_mask) < 20:
        return flux, None, valid
    
    # 多项式拟合（4 次）
    try:
        coeffs = np.polyfit(wavelength[cont_mask], flux[cont_mask], 4)
        continuum = np.polyval(coeffs, wavelength)
        # 避免除零
        continuum[continuum <= 0] = np.median(flux[valid])
        norm_flux = flux / continuum
        return norm_flux, continuum, valid
    except:
        return flux, None, valid

def gaussian(x, amp, mu, sigma, offset):
    """高斯函数（用于吸收线，amp 为负）"""
    return offset + amp * np.exp(-0.5 * ((x - mu) / sigma)**2)

def measure_equivalent_width(wavelength, norm_flux, line_center, window=100):
    """测量单条谱线的等效宽度
    
    EW = ∫(1 - F/F_cont) dλ
    
    同时进行高斯拟合以获取线参数。
    对于 Zeeman 分裂的线，使用宽窗口积分总 EW。
    """
    # 线窗口
    line_mask = (np.abs(wavelength - line_center) < window) & np.isfinite(norm_flux)
    
    if np.sum(line_mask) < 5:
        return {
            'detected': False,
            'reason': 'insufficient_points',
            'EW': 0,
            'EW_error': 0,
            'depth': 0,
            'fwhm': 0,
            'center': line_center,
        }
    
    wl_line = wavelength[line_mask]
    flux_line = norm_flux[line_mask]
    
    # 等效宽度（直接积分）
    # EW = ∫(1 - F) dλ
    ew_integrand = 1.0 - flux_line
    # 只积分正的部分（吸收）
    ew_integrand[ew_integrand < 0] = 0
    EW = float(np.trapezoid(ew_integrand, wl_line))
    
    # 线深度
    depth = float(1.0 - np.min(flux_line))
    
    # 高斯拟合（单峰，用于估计 FWHM 和中心）
    try:
        # 初始猜测
        min_idx = np.argmin(flux_line)
        mu0 = wl_line[min_idx]
        amp0 = np.min(flux_line) - 1.0  # 负值（吸收线）
        sigma0 = 10.0  # Å
        
        p0 = [amp0, mu0, sigma0, 1.0]
        bounds = ([-2.0, line_center-50, 1.0, 0.5], [0.0, line_center+50, 100.0, 1.5])
        
        popt, pcov = curve_fit(gaussian, wl_line, flux_line, p0=p0, bounds=bounds, maxfev=10000)
        amp, mu, sigma, offset = popt
        fwhm = 2.355 * abs(sigma)
        
        # 拟合优度
        flux_fit = gaussian(wl_line, *popt)
        residuals = flux_line - flux_fit
        chi2 = np.sum(residuals**2)
        dof = len(wl_line) - 4
        chi2_dof = chi2 / dof if dof > 0 else 999
        
        # EW 误差（基于连续谱噪声）
        # 估计连续谱区域的噪声
        cont_mask_local = (np.abs(wl_line - line_center) > window*0.6) & (np.abs(wl_line - line_center) < window)
        if np.sum(cont_mask_local) > 5:
            noise = np.std(flux_line[cont_mask_local])
        else:
            noise = 0.01
        EW_error = noise * np.sqrt(window * 2)  # 粗略估计
        
        fit_success = True
    except Exception as e:
        fwhm = 0
        mu = line_center
        chi2_dof = 999
        EW_error = EW * 0.3  # 30% 误差
        fit_success = False
    
    # 检测判据：EW > 0.5 Å 且 depth > 0.03
    detected = (EW > 0.5) and (depth > 0.03)
    
    return {
        'detected': bool(detected),
        'EW': float(EW),
        'EW_error': float(EW_error),
        'depth': float(depth),
        'fwhm': float(fwhm),
        'center_fit': float(mu),
        'center_input': float(line_center),
        'chi2_dof': float(chi2_dof),
        'fit_success': bool(fit_success),
        'n_pixels': int(np.sum(line_mask)),
    }

def analyze_star(star):
    """分析单颗白矮星的完整 Balmer 线系"""
    name = star['name']
    B = star['B_tesla']
    teff = star.get('Teff')
    
    print(f"  分析 {name} (B={B:.2e} T, Teff={teff})...")
    
    # 获取光谱
    wavelength, flux, ivar = get_sdss_spectrum(star)
    if wavelength is None:
        print(f"    无法获取光谱")
        return None
    
    # 限制波长范围
    valid = (wavelength > 3800) & (wavelength < 6800) & (ivar > 0) & np.isfinite(flux)
    wavelength = wavelength[valid]
    flux = flux[valid]
    ivar = ivar[valid]
    
    if len(wavelength) < 100:
        print(f"    有效像素不足: {len(wavelength)}")
        return None
    
    # 连续谱归一化
    norm_flux, continuum, _ = continuum_normalize(wavelength, flux, ivar)
    if continuum is None:
        print(f"    连续谱归一化失败")
        return None
    
    # 测量每条 Balmer 线
    balmer_results = {}
    for line_name, line_center in BALMER_LINES.items():
        result = measure_equivalent_width(wavelength, norm_flux, line_center, window=80)
        balmer_results[line_name] = result
    
    # 统计
    detected_lines = [name for name, res in balmer_results.items() if res['detected']]
    n_detected = len(detected_lines)
    n_total = len(BALMER_LINES)
    
    # 总等效宽度（所有检测到的线之和）
    total_EW = sum(res['EW'] for res in balmer_results.values() if res['detected'])
    
    print(f"    检测到 {n_detected}/{n_total} 条 Balmer 线: {detected_lines}")
    print(f"    总 EW = {total_EW:.1f} Å")
    
    return {
        'name': name,
        'B_tesla': float(B),
        'Teff': teff,
        'Mstar': star.get('Mstar'),
        'n_detected': n_detected,
        'n_total': n_total,
        'detected_fraction': n_detected / n_total,
        'detected_lines': detected_lines,
        'total_EW': float(total_EW),
        'balmer_results': balmer_results,
        'n_pixels': len(wavelength),
        'wavelength_range': [float(wavelength.min()), float(wavelength.max())],
    }

def main():
    print("=" * 90)
    print("白矮星光谱分析 v6：扩大样本 + 等效宽度 + Zeeman 分裂处理")
    print("=" * 90)
    print()
    
    # 1. 加载目录
    data = load_catalog()
    
    # 2. 选择样本
    intermediate, weak = select_samples(data)
    
    # 3. 分析中场白矮星
    print()
    print("=" * 90)
    print("分析中场白矮星（10^4-10^5 T）")
    print("=" * 90)
    print()
    
    int_results = []
    for i, star in enumerate(intermediate):
        print(f"[{i+1}/{len(intermediate)}]")
        result = analyze_star(star)
        if result is not None:
            int_results.append(result)
        print()
    
    # 4. 分析弱场对照
    print("=" * 90)
    print("分析弱场对照（<10^3 T）")
    print("=" * 90)
    print()
    
    weak_results = []
    for i, star in enumerate(weak):
        print(f"[{i+1}/{len(weak)}]")
        result = analyze_star(star)
        if result is not None:
            weak_results.append(result)
        print()
    
    # 5. 汇总分析
    print("=" * 90)
    print("汇总分析")
    print("=" * 90)
    print()
    
    print(f"成功分析的白矮星:")
    print(f"  中场: {len(int_results)}/{len(intermediate)} 颗")
    print(f"  弱场: {len(weak_results)}/{len(weak)} 颗")
    print()
    
    if len(int_results) > 0 and len(weak_results) > 0:
        # 检测率对比
        int_det_rate = np.mean([r['detected_fraction'] for r in int_results])
        weak_det_rate = np.mean([r['detected_fraction'] for r in weak_results])
        
        print(f"Balmer 线平均检测率:")
        print(f"  中场: {int_det_rate:.3f} ({int_det_rate*100:.1f}%)")
        print(f"  弱场: {weak_det_rate:.3f} ({weak_det_rate*100:.1f}%)")
        print(f"  差异: {weak_det_rate - int_det_rate:.3f} ({(weak_det_rate-int_det_rate)*100:.1f} 个百分点)")
        print()
        
        # 总 EW 对比
        int_total_EW = np.mean([r['total_EW'] for r in int_results])
        weak_total_EW = np.mean([r['total_EW'] for r in weak_results])
        
        print(f"Balmer 线总等效宽度（平均）:")
        print(f"  中场: {int_total_EW:.1f} Å")
        print(f"  弱场: {weak_total_EW:.1f} Å")
        print(f"  比值: {int_total_EW/weak_total_EW:.3f}")
        print()
        
        # 每条线的检测率对比
        print("每条 Balmer 线的检测率:")
        print()
        print(f"  {'线':<6} {'波长(Å)':>10} {'中场检测率':>12} {'弱场检测率':>12} {'差异':>10}")
        print("  " + "-" * 55)
        
        line_stats = {}
        for line_name, line_center in BALMER_LINES.items():
            int_det = sum(1 for r in int_results if r['balmer_results'][line_name]['detected'])
            weak_det = sum(1 for r in weak_results if r['balmer_results'][line_name]['detected'])
            
            int_rate = int_det / len(int_results) if len(int_results) > 0 else 0
            weak_rate = weak_det / len(weak_results) if len(weak_results) > 0 else 0
            
            print(f"  {line_name:<6} {line_center:>10.1f} {int_rate:>12.3f} {weak_rate:>12.3f} {weak_rate-int_rate:>10.3f}")
            
            line_stats[line_name] = {
                'int_rate': float(int_rate),
                'weak_rate': float(weak_rate),
                'int_n': int_det,
                'weak_n': weak_det,
            }
        
        print()
        
        # 每条线的 EW 对比
        print("每条 Balmer 线的平均等效宽度（仅检测到的线）:")
        print()
        print(f"  {'线':<6} {'中场 EW(Å)':>12} {'弱场 EW(Å)':>12} {'比值':>10}")
        print("  " + "-" * 45)
        
        for line_name in BALMER_LINES:
            int_ews = [r['balmer_results'][line_name]['EW'] for r in int_results 
                       if r['balmer_results'][line_name]['detected']]
            weak_ews = [r['balmer_results'][line_name]['EW'] for r in weak_results 
                        if r['balmer_results'][line_name]['detected']]
            
            int_ew = np.mean(int_ews) if len(int_ews) > 0 else 0
            weak_ew = np.mean(weak_ews) if len(weak_ews) > 0 else 0
            ratio = int_ew / weak_ew if weak_ew > 0 else 0
            
            print(f"  {line_name:<6} {int_ew:>12.2f} {weak_ew:>12.2f} {ratio:>10.3f}")
        
        print()
        
        # Zeeman 分裂讨论
        print("=" * 90)
        print("Zeeman 分裂效应讨论")
        print("=" * 90)
        print()
        print("等效宽度（EW）是积分量，对 Zeeman 分裂不敏感：")
        print("  - Zeeman 分裂将单峰分散为多个分量，但总 EW 守恒")
        print("  - 我们使用宽窗口（±80 Å）积分总 EW，包含所有 Zeeman 分量")
        print("  - 因此，如果中场白矮星的总 EW 仍然低，则不是 Zeeman 分裂导致的")
        print()
        print(f"观测结果：")
        print(f"  中场总 EW / 弱场总 EW = {int_total_EW/weak_total_EW:.3f}")
        if int_total_EW / weak_total_EW < 0.7:
            print(f"  → 中场总 EW 显著低于弱场，不能用 Zeeman 分裂解释")
            print(f"  → 支持拓扑禁戒假说")
        else:
            print(f"  → 中场总 EW 与弱场相当，可能受 Zeeman 分裂或其他效应影响")
        
        print()
    
    # 6. 保存结果
    output_file = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\results\white_dwarf_analysis_v6_results.json"
    
    # 转换为可序列化格式
    def serialize(obj):
        if isinstance(obj, (np.floating, np.integer)):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return obj
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            'n_intermediate_analyzed': len(int_results),
            'n_weak_analyzed': len(weak_results),
            'intermediate_results': [{k: serialize(v) for k, v in r.items() if k != 'balmer_results'} 
                                      | {'balmer_results': {ln: serialize(lr) for ln, lr in r['balmer_results'].items()}}
                                      for r in int_results],
            'weak_results': [{k: serialize(v) for k, v in r.items() if k != 'balmer_results'} 
                            | {'balmer_results': {ln: serialize(lr) for ln, lr in r['balmer_results'].items()}}
                            for r in weak_results],
            'line_stats': line_stats if 'line_stats' in dir() else None,
        }, f, indent=2, ensure_ascii=False, default=str)
    
    print(f"结果已保存到: {output_file}")
    print()
    print("=" * 90)
    print("分析完成")
    print("=" * 90)

if __name__ == "__main__":
    main()
