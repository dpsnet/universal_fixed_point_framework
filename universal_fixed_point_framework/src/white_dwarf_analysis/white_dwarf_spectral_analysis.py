"""
白矮星光谱实际数据分析：寻找拓扑禁戒特征

目标：
1. 从 SDSS 获取 DA 型白矮星（氢大气）光谱
2. 识别氢 Balmer 线系，测量每条线的强度
3. 从 Zeeman 展宽估计磁场
4. 按磁场分组，统计可观测 Balmer 线数
5. 寻找"缺失线"：理论预测存在但观测中缺失或显著减弱的谱线

氢 Balmer 线波长（真空，Å）：
Hα = 6562.8
Hβ = 4861.3
Hγ = 4340.5
Hδ = 4101.7
Hε = 3970.1
Hζ = 3889.1
Hη = 3835.4
Hθ = 3797.9
Hι = 3770.6
Hκ = 3750.1
...（Balmer 系限 3646 Å）
"""

import numpy as np
from astroquery.sdss import SDSS
from astropy import coordinates as coords
from astropy import units as u
from astropy.io import fits
import warnings
warnings.filterwarnings('ignore')

# Balmer 线波长（Å）
BALMER_LINES = {
    'Hα': 6562.8,
    'Hβ': 4861.3,
    'Hγ': 4340.5,
    'Hδ': 4101.7,
    'Hε': 3970.1,
    'Hζ': 3889.1,
    'Hη': 3835.4,
    'Hθ': 3797.9,
    'Hι': 3770.6,
    'Hκ': 3750.1,
}

def query_white_dwarfs(n_max=50):
    """查询 SDSS 中的 DA 型白矮星
    
    使用 SDSS 光谱分类查询白矮星。
    返回包含坐标、星等、光谱信息的列表。
    """
    print("查询 SDSS 白矮星样本...")
    
    # 使用 SQL 查询 SDSS 中的白矮星
    # specClass = 3 表示白矮星，subClass 包含 'DA' 表示氢大气
    query = """
    SELECT TOP {n} 
        s.specObjID, s.ra, s.dec, s.specClass, s.subClass,
        s.modelMag_u, s.modelMag_g, s.modelMag_r,
        s.modelMag_i, s.modelMag_z,
        s.z, s.zErr,
        p.plate, p.mjd, p.fiberID
    FROM SpecObj s
    JOIN PlateX p ON s.plate = p.plate
    WHERE s.specClass = 3 
        AND s.subClass LIKE '%DA%'
        AND s.modelMag_g BETWEEN 12 AND 19
        AND s.z BETWEEN -0.001 AND 0.01
    ORDER BY s.modelMag_g
    """.format(n=n_max)
    
    try:
        results = SDSS.query_sql(query)
        print(f"  查询到 {len(results)} 颗 DA 型白矮星")
        return results
    except Exception as e:
        print(f"  SQL 查询失败: {e}")
        print("  尝试备用查询方法...")
        return None

def get_spectrum(specObjID):
    """获取单个天体的 SDSS 光谱
    
    返回：
        wavelength: 波长数组（Å）
        flux: 流量数组
        ivar: 逆方差数组
    """
    try:
        sp = SDSS.get_spectra(specObjID=specObjID)
        if sp is None or len(sp) == 0:
            return None, None, None
        
        # SDSS 光谱在第一个 HDU 的 data 中
        # coadded 光谱在 sp[0] 中
        hdu = sp[0]
        data = hdu[1].data
        
        # SDSS 光谱的波长是 log10(wavelength)，需要转换
        loglam = data['loglam']
        wavelength = 10**loglam  # Å
        flux = data['flux']  # 10^-17 erg/s/cm²/Å
        ivar = data['ivar']  # 逆方差
        
        return wavelength, flux, ivar
    except Exception as e:
        print(f"    获取光谱失败: {e}")
        return None, None, None

def normalize_spectrum(wavelength, flux, ivar):
    """连续谱归一化
    
    使用多项式拟合连续谱，然后除以连续谱。
    """
    # 选择连续谱窗口（避开 Balmer 线和其他强线）
    # 使用 3500-4000 Å 和 5000-6000 Å 作为连续谱窗口
    cont_mask = np.ones(len(wavelength), dtype=bool)
    
    # 屏蔽 Balmer 线附近
    for name, wl in BALMER_LINES.items():
        mask = np.abs(wavelength - wl) < 50  # ±50 Å
        cont_mask &= ~mask
    
    # 屏蔽其他可能的强线（Ca H&K, G-band 等）
    for wl in [3933, 3968, 4300, 5175, 5890]:
        mask = np.abs(wavelength - wl) < 20
        cont_mask &= ~mask
    
    # 只保留有效流量点
    valid = cont_mask & (ivar > 0) & np.isfinite(flux)
    
    if np.sum(valid) < 10:
        return flux, None
    
    # 多项式拟合连续谱（3 次多项式）
    try:
        coeffs = np.polyfit(wavelength[valid], flux[valid], 3)
        continuum = np.polyval(coeffs, wavelength)
        normalized_flux = flux / continuum
        return normalized_flux, continuum
    except Exception as e:
        print(f"    连续谱拟合失败: {e}")
        return flux, None

def measure_balmer_lines(wavelength, flux, ivar):
    """测量 Balmer 线的等效宽度和深度
    
    返回：
        results: dict，包含每条线的测量结果
    """
    results = {}
    
    for name, wl_center in BALMER_LINES.items():
        # 线窗口（±15 Å）
        line_mask = np.abs(wavelength - wl_center) < 15
        # 连续谱窗口（±30 到 ±50 Å）
        cont_mask = (np.abs(wavelength - wl_center) > 30) & (np.abs(wavelength - wl_center) < 60)
        
        if np.sum(line_mask) < 3 or np.sum(cont_mask) < 5:
            results[name] = {
                'detected': False,
                'reason': 'insufficient_points',
                'center': wl_center,
            }
            continue
        
        # 连续谱水平
        cont_level = np.median(flux[cont_mask])
        
        if cont_level <= 0 or not np.isfinite(cont_level):
            results[name] = {
                'detected': False,
                'reason': 'bad_continuum',
                'center': wl_center,
            }
            continue
        
        # 线深度（相对于连续谱）
        line_flux = flux[line_mask]
        line_depth = 1.0 - np.min(line_flux) / cont_level
        
        # 等效宽度（假设归一化后连续谱=1）
        # EW = ∫(1 - F/F_cont) dλ
        normalized_line = 1.0 - line_flux / cont_level
        ew = np.trapezoid(normalized_line, wavelength[line_mask])
        
        # 信噪比
        line_ivar = ivar[line_mask]
        if np.sum(line_ivar) > 0:
            snr = np.mean(line_flux) * np.sqrt(np.mean(line_ivar))
        else:
            snr = 0
        
        # 检测判据：线深度 > 0.05 且 EW > 0.5 Å 且 SNR > 3
        detected = (line_depth > 0.05) and (ew > 0.5) and (snr > 3)
        
        results[name] = {
            'detected': bool(detected),
            'center': float(wl_center),
            'line_depth': float(line_depth),
            'equivalent_width': float(ew),
            'snr': float(snr),
            'cont_level': float(cont_level),
        }
    
    return results

def estimate_magnetic_field(wavelength, flux, ivar):
    """从 Balmer 线的 Zeeman 展宽估计磁场
    
    对于弱磁场（B < 10^6 T），Zeeman 分裂小于线宽，
    表现为线的展宽。可以通过比较 Hβ 和 Hα 的宽度来估计磁场。
    
    简化方法：使用 Hβ 线的半高全宽（FWHM）估计磁场。
    无磁场白矮星的 Hβ FWHM 主要由压力展宽决定（~10-50 Å）。
    磁场导致的额外展宽：Δλ_B ≈ 4.67e-13 * λ² * B（Å）
    """
    # 测量 Hβ 的 FWHM
    wl_center = BALMER_LINES['Hβ']
    line_mask = np.abs(wavelength - wl_center) < 30
    
    if np.sum(line_mask) < 5:
        return None, 'insufficient_points'
    
    line_flux = flux[line_mask]
    cont_mask = (np.abs(wavelength - wl_center) > 40) & (np.abs(wavelength - wl_center) < 80)
    
    if np.sum(cont_mask) < 5:
        return None, 'no_continuum'
    
    cont_level = np.median(flux[cont_mask])
    if cont_level <= 0:
        return None, 'bad_continuum'
    
    # 归一化
    norm_flux = line_flux / cont_level
    half_max = 0.5 * (1 + np.min(norm_flux))
    
    # 找半高点
    above_half = norm_flux < half_max
    if np.sum(above_half) < 2:
        return None, 'no_half_max'
    
    wl_line = wavelength[line_mask]
    fwhm_indices = np.where(above_half)[0]
    fwhm = wl_line[fwhm_indices[-1]] - wl_line[fwhm_indices[0]]
    
    # 无磁场白矮星的典型 Hβ FWHM（~20 Å，对于 g~16 的 DA 白矮星）
    # 这是一个粗略的估计，实际值取决于表面重力和温度
    intrinsic_fwhm = 20.0  # Å
    
    # 磁场导致的额外展宽（ quadrature 求和）
    if fwhm > intrinsic_fwhm:
        broadened_fwhm = np.sqrt(fwhm**2 - intrinsic_fwhm**2)
    else:
        broadened_fwhm = 0
    
    # Zeeman 展宽公式：Δλ = 4.67e-13 * λ² * B
    # B = Δλ / (4.67e-13 * λ²)
    if broadened_fwhm > 0:
        B_tesla = broadened_fwhm / (4.67e-13 * wl_center**2)
    else:
        B_tesla = 0
    
    return float(B_tesla), 'estimated'

def analyze_white_dwarf(row):
    """分析单颗白矮星的光谱"""
    specObjID = int(row['specObjID'])
    ra = float(row['ra'])
    dec = float(row['dec'])
    subClass = str(row['subClass'])
    g_mag = float(row['modelMag_g'])
    
    print(f"  分析 specObjID={specObjID} (RA={ra:.3f}, Dec={dec:.3f}, g={g_mag:.2f}, {subClass})...")
    
    # 获取光谱
    wavelength, flux, ivar = get_spectrum(specObjID)
    if wavelength is None:
        return None
    
    # 限制波长范围（SDSS 光谱 3800-9200 Å）
    valid = (wavelength > 3700) & (wavelength < 7000) & (ivar > 0) & np.isfinite(flux)
    wavelength = wavelength[valid]
    flux = flux[valid]
    ivar = ivar[valid]
    
    if len(wavelength) < 100:
        print(f"    有效波长点不足: {len(wavelength)}")
        return None
    
    # 连续谱归一化
    norm_flux, continuum = normalize_spectrum(wavelength, flux, ivar)
    
    # 测量 Balmer 线
    balmer_results = measure_balmer_lines(wavelength, norm_flux, ivar)
    
    # 统计检测到的线数
    detected_lines = [name for name, res in balmer_results.items() if res.get('detected', False)]
    n_detected = len(detected_lines)
    n_total = len(BALMER_LINES)
    
    # 估计磁场
    B_tesla, B_method = estimate_magnetic_field(wavelength, norm_flux, ivar)
    
    result = {
        'specObjID': specObjID,
        'ra': ra,
        'dec': dec,
        'subClass': subClass,
        'g_mag': g_mag,
        'z': float(row['z']),
        'n_detected': n_detected,
        'n_total': n_total,
        'detected_fraction': n_detected / n_total,
        'detected_lines': detected_lines,
        'balmer_results': {k: {kk: vv for kk, vv in v.items() if kk != 'detected'} 
                           for k, v in balmer_results.items()},
        'B_tesla': B_tesla,
        'B_method': B_method,
        'wavelength_range': [float(wavelength.min()), float(wavelength.max())],
        'n_pixels': len(wavelength),
    }
    
    print(f"    检测到 {n_detected}/{n_total} 条 Balmer 线: {detected_lines}")
    print(f"    估计磁场 B = {B_tesla:.2e} T ({B_method})")
    
    return result

def main():
    print("=" * 90)
    print("白矮星光谱实际数据分析：寻找拓扑禁戒特征")
    print("=" * 90)
    print()
    
    # 步骤 1：查询白矮星样本
    sample = query_white_dwarfs(n_max=30)
    
    if sample is None or len(sample) == 0:
        print("无法获取白矮星样本，退出。")
        return
    
    print()
    
    # 步骤 2：逐颗分析
    all_results = []
    for i, row in enumerate(sample):
        print(f"[{i+1}/{len(sample)}]")
        result = analyze_white_dwarf(row)
        if result is not None:
            all_results.append(result)
        print()
    
    print("=" * 90)
    print("汇总分析")
    print("=" * 90)
    print()
    
    if len(all_results) == 0:
        print("没有成功分析的白矮星。")
        return
    
    # 按磁场分组
    B_values = np.array([r['B_tesla'] for r in all_results if r['B_tesla'] is not None])
    valid_results = [r for r in all_results if r['B_tesla'] is not None]
    
    if len(B_values) == 0:
        print("没有有效的磁场估计。")
        return
    
    # 分组：弱场 (<10^4 T), 中场 (10^4-10^5 T), 强场 (>10^5 T)
    groups = {
        'weak (<1e4 T)': [],
        'intermediate (1e4-1e5 T)': [],
        'strong (>1e5 T)': [],
    }
    
    for r in valid_results:
        B = r['B_tesla']
        if B < 1e4:
            groups['weak (<1e4 T)'].append(r)
        elif B < 1e5:
            groups['intermediate (1e4-1e5 T)'].append(r)
        else:
            groups['strong (>1e5 T)'].append(r)
    
    print(f"总样本数: {len(valid_results)}")
    print()
    print(f"{'组':<30} {'数量':>6} {'平均检测率':>12} {'平均磁场(T)':>14}")
    print("-" * 70)
    
    for group_name, group_results in groups.items():
        if len(group_results) == 0:
            print(f"{group_name:<30} {0:>6} {'N/A':>12} {'N/A':>14}")
            continue
        
        mean_fraction = np.mean([r['detected_fraction'] for r in group_results])
        mean_B = np.mean([r['B_tesla'] for r in group_results])
        print(f"{group_name:<30} {len(group_results):>6} {mean_fraction:>12.3f} {mean_B:>14.2e}")
    
    print()
    
    # 按 Balmer 线统计各组的检测率
    print("各 Balmer 线在不同磁场组中的检测率：")
    print()
    print(f"{'线':<8} {'波长(Å)':>10} {'弱场':>8} {'中场':>8} {'强场':>8}")
    print("-" * 50)
    
    for line_name, line_wl in BALMER_LINES.items():
        rates = []
        for group_name in ['weak (<1e4 T)', 'intermediate (1e4-1e5 T)', 'strong (>1e5 T)']:
            group = groups[group_name]
            if len(group) == 0:
                rates.append('N/A')
            else:
                n_det = sum(1 for r in group if line_name in r['detected_lines'])
                rates.append(f"{n_det/len(group):.2f}")
        print(f"{line_name:<8} {line_wl:>10.1f} {rates[0]:>8} {rates[1]:>8} {rates[2]:>8}")
    
    print()
    
    # 寻找"缺失线"模式
    print("缺失线分析（理论预测存在但观测中缺失的谱线）：")
    print()
    
    # 对于每颗白矮星，找出缺失的 Balmer 线
    missing_patterns = {}
    for r in valid_results:
        missing = [name for name in BALMER_LINES if name not in r['detected_lines']]
        if missing:
            pattern = tuple(missing)
            if pattern not in missing_patterns:
                missing_patterns[pattern] = []
            missing_patterns[pattern].append(r['B_tesla'])
    
    # 按出现频率排序
    sorted_patterns = sorted(missing_patterns.items(), key=lambda x: len(x[1]), reverse=True)
    
    print(f"{'缺失线模式':<40} {'出现次数':>8} {'平均磁场(T)':>14}")
    print("-" * 70)
    for pattern, B_list in sorted_patterns[:10]:
        pattern_str = ', '.join(pattern)
        mean_B = np.mean(B_list)
        print(f"{pattern_str:<40} {len(B_list):>8} {mean_B:>14.2e}")
    
    print()
    
    # 保存结果
    import json
    output_file = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\results\white_dwarf_spectral_analysis.json"
    
    # 转换为可序列化格式
    serializable_results = []
    for r in all_results:
        sr = {k: v for k, v in r.items() if k != 'balmer_results'}
        sr['balmer_results'] = {k: {kk: (float(vv) if isinstance(vv, (np.floating, np.integer)) else vv) 
                                      for kk, vv in v.items()} 
                                 for k, v in r['balmer_results'].items()}
        serializable_results.append(sr)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            'n_analyzed': len(all_results),
            'n_valid_B': len(valid_results),
            'groups': {k: len(v) for k, v in groups.items()},
            'results': serializable_results,
        }, f, indent=2, ensure_ascii=False)
    
    print(f"结果已保存到: {output_file}")

if __name__ == "__main__":
    main()
