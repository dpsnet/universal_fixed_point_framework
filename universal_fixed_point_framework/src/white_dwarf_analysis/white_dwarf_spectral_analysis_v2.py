"""
白矮星光谱分析 v2：使用 Simbad + SDSS 坐标查询

方法：
1. 从 Simbad 查询已知的 DA 型白矮星（包括磁场白矮星）
2. 通过坐标在 SDSS 中查找光谱
3. 分析 Balmer 线和磁场
"""

import numpy as np
from astroquery.simbad import Simbad
from astroquery.sdss import SDSS
from astropy import coordinates as coords
from astropy import units as u
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

def query_magnetic_white_dwarfs():
    """从 Simbad 查询已知的磁场白矮星
    
    使用 Simbad 的 bibcode 或 otype 查询。
    磁场白矮星的 Simbad 类型通常是 'WhiteDwarf*' 且有磁场测量。
    """
    print("从 Simbad 查询磁场白矮星...")
    
    # 自定义 Simbad 查询，获取磁场信息
    customSimbad = Simbad()
    customSimbad.add_votable_fields('mk', 'fluxdata(B)', 'fluxdata(V)', 'sp', 'z')
    
    # 查询一些已知的磁场白矮星
    # 这些名字来自文献（Wickramasinghe & Ferrario 2000 等）
    known_mwd = [
        'Grw+70 8247',      # B ~ 10^8 T
        'GD 229',            # B ~ 10^7 T
        'PG 1031+234',       # B ~ 10^8 T
        'LB 11146',          # B ~ 10^7 T
        'EUVE J0317-853',    # B ~ 10^8 T
        'PG 0945+245',       # B ~ 10^6 T
        'GD 90',             # B ~ 10^6 T
        'PG 1015+064',       # B ~ 10^6 T
        'LB 11146',          # B ~ 10^7 T
        'G 99-37',           # B ~ 10^7 T
        'PG 1658+441',       # B ~ 10^6 T
        'GD 195',            # B ~ 10^6 T
        'PG 0136+257',       # B ~ 10^6 T
        'LB 253',            # B ~ 10^6 T
        'G 183-22',          # B ~ 10^6 T
        'PG 2359+105',       # B ~ 10^6 T
        'GD 50',             # B ~ 10^6 T
        'PG 1101+263',       # B ~ 10^6 T
        'LB 1497',           # B ~ 10^6 T
    ]
    
    # 也加入一些无磁场的 DA 白矮星作为对照
    known_da = [
        'GD 153',            # 标准星，无磁场
        'G191-B2B',          # 标准星，无磁场
        'GD 191-B2B',        # 标准星，无磁场
        'LB 227',            # DA 白矮星
        'G 62-57',           # DA 白矮星
        'GD 385',            # DA 白矮星
        'PG 1342+445',       # DA 白矮星
        'LB 1334',           # DA 白矮星
        'G 116-B6A',         # DA 白矮星
        'GD 293',            # DA 白矮星
    ]
    
    all_targets = []
    
    print("  查询磁场白矮星...")
    for name in known_mwd:
        try:
            result = customSimbad.query_object(name)
            if result is not None and len(result) > 0:
                ra = result['ra'][0]  # 度
                dec = result['dec'][0]  # 度
                all_targets.append({
                    'name': name,
                    'ra': float(ra),
                    'dec': float(dec),
                    'type': 'magnetic',
                })
                print(f"    {name}: RA={ra:.4f} deg, Dec={dec:.4f} deg")
        except Exception as e:
            print(f"    {name}: 查询失败 - {e}")
    
    print(f"  查询对照 DA 白矮星...")
    for name in known_da:
        try:
            result = customSimbad.query_object(name)
            if result is not None and len(result) > 0:
                ra = result['ra'][0]
                dec = result['dec'][0]
                all_targets.append({
                    'name': name,
                    'ra': float(ra),
                    'dec': float(dec),
                    'type': 'da',
                })
                print(f"    {name}: RA={ra:.4f} deg, Dec={dec:.4f} deg")
        except Exception as e:
            print(f"    {name}: 查询失败 - {e}")
    
    print(f"  共获取 {len(all_targets)} 个目标")
    return all_targets

def get_sdss_spectrum(ra_deg, dec_deg, radius=5.0):
    """通过坐标在 SDSS 中查找并获取光谱
    
    参数：
        ra_deg, dec_deg: 坐标（度）
        radius: 搜索半径（角秒）
    """
    try:
        c = coords.SkyCoord(ra_deg, dec_deg, unit=(u.deg, u.deg))
        
        # 在 SDSS 中查找光谱
        xid = SDSS.query_region(c, radius=radius * u.arcsec, spectro=True)
        
        if xid is None or len(xid) == 0:
            return None, None, None, None
        
        # 取第一个匹配
        specObjID = int(xid['specObjID'][0])
        
        # 获取光谱
        sp = SDSS.get_spectra(specObjID=specObjID)
        if sp is None or len(sp) == 0:
            return None, None, None, None
        
        hdu = sp[0]
        data = hdu[1].data
        
        loglam = data['loglam']
        wavelength = 10**loglam
        flux = data['flux']
        ivar = data['ivar']
        
        return wavelength, flux, ivar, specObjID
        
    except Exception as e:
        print(f"    SDSS 查询失败: {e}")
        return None, None, None, None

def normalize_spectrum(wavelength, flux, ivar):
    """连续谱归一化"""
    cont_mask = np.ones(len(wavelength), dtype=bool)
    
    for name, wl in BALMER_LINES.items():
        mask = np.abs(wavelength - wl) < 50
        cont_mask &= ~mask
    
    for wl in [3933, 3968, 4300, 5175, 5890, 7699, 7600]:
        mask = np.abs(wavelength - wl) < 20
        cont_mask &= ~mask
    
    valid = cont_mask & (ivar > 0) & np.isfinite(flux)
    
    if np.sum(valid) < 10:
        return flux, None
    
    try:
        coeffs = np.polyfit(wavelength[valid], flux[valid], 3)
        continuum = np.polyval(coeffs, wavelength)
        normalized_flux = flux / continuum
        return normalized_flux, continuum
    except:
        return flux, None

def measure_balmer_lines(wavelength, flux, ivar):
    """测量 Balmer 线"""
    results = {}
    
    for name, wl_center in BALMER_LINES.items():
        line_mask = np.abs(wavelength - wl_center) < 15
        cont_mask = (np.abs(wavelength - wl_center) > 30) & (np.abs(wavelength - wl_center) < 60)
        
        if np.sum(line_mask) < 3 or np.sum(cont_mask) < 5:
            results[name] = {'detected': False, 'reason': 'insufficient_points'}
            continue
        
        cont_level = np.median(flux[cont_mask])
        if cont_level <= 0 or not np.isfinite(cont_level):
            results[name] = {'detected': False, 'reason': 'bad_continuum'}
            continue
        
        line_flux = flux[line_mask]
        line_depth = 1.0 - np.min(line_flux) / cont_level
        
        normalized_line = 1.0 - line_flux / cont_level
        ew = float(np.trapezoid(normalized_line, wavelength[line_mask]))
        
        line_ivar = ivar[line_mask]
        snr = float(np.mean(line_flux) * np.sqrt(np.mean(line_ivar))) if np.sum(line_ivar) > 0 else 0
        
        detected = (line_depth > 0.05) and (ew > 0.5) and (snr > 3)
        
        results[name] = {
            'detected': bool(detected),
            'line_depth': float(line_depth),
            'equivalent_width': ew,
            'snr': snr,
        }
    
    return results

def estimate_magnetic_field(wavelength, flux, ivar):
    """从 Hβ Zeeman 展宽估计磁场"""
    wl_center = BALMER_LINES['Hβ']
    line_mask = np.abs(wavelength - wl_center) < 30
    
    if np.sum(line_mask) < 5:
        return None
    
    line_flux = flux[line_mask]
    cont_mask = (np.abs(wavelength - wl_center) > 40) & (np.abs(wavelength - wl_center) < 80)
    
    if np.sum(cont_mask) < 5:
        return None
    
    cont_level = np.median(flux[cont_mask])
    if cont_level <= 0:
        return None
    
    norm_flux = line_flux / cont_level
    half_max = 0.5 * (1 + np.min(norm_flux))
    
    above_half = norm_flux < half_max
    if np.sum(above_half) < 2:
        return None
    
    wl_line = wavelength[line_mask]
    fwhm_indices = np.where(above_half)[0]
    fwhm = float(wl_line[fwhm_indices[-1]] - wl_line[fwhm_indices[0]])
    
    intrinsic_fwhm = 20.0  # Å，无磁场白矮星的典型 Hβ FWHM
    
    if fwhm > intrinsic_fwhm:
        broadened = np.sqrt(fwhm**2 - intrinsic_fwhm**2)
    else:
        broadened = 0
    
    if broadened > 0:
        B_tesla = broadened / (4.67e-13 * wl_center**2)
    else:
        B_tesla = 0
    
    return float(B_tesla)

def main():
    print("=" * 90)
    print("白矮星光谱分析 v2：Simbad + SDSS 坐标查询")
    print("=" * 90)
    print()
    
    # 步骤 1：查询目标
    targets = query_magnetic_white_dwarfs()
    
    if len(targets) == 0:
        print("没有获取到目标，退出。")
        return
    
    print()
    
    # 步骤 2：逐颗获取 SDSS 光谱并分析
    all_results = []
    
    for i, target in enumerate(targets):
        name = target['name']
        ra_deg = target['ra']
        dec_deg = target['dec']
        wd_type = target['type']
        
        print(f"[{i+1}/{len(targets)}] {name} ({wd_type})")
        print(f"  坐标: RA={ra_deg:.4f} deg, Dec={dec_deg:.4f} deg")
        
        # 获取 SDSS 光谱
        wavelength, flux, ivar, specObjID = get_sdss_spectrum(ra_deg, dec_deg)
        
        if wavelength is None:
            print(f"  SDSS 中无光谱，跳过")
            print()
            continue
        
        print(f"  SDSS specObjID={specObjID}, 像素数={len(wavelength)}")
        
        # 限制波长范围
        valid = (wavelength > 3700) & (wavelength < 7000) & (ivar > 0) & np.isfinite(flux)
        wavelength = wavelength[valid]
        flux = flux[valid]
        ivar = ivar[valid]
        
        if len(wavelength) < 100:
            print(f"  有效像素不足: {len(wavelength)}")
            print()
            continue
        
        # 归一化
        norm_flux, continuum = normalize_spectrum(wavelength, flux, ivar)
        
        # 测量 Balmer 线
        balmer_results = measure_balmer_lines(wavelength, norm_flux, ivar)
        detected_lines = [name for name, res in balmer_results.items() if res.get('detected', False)]
        n_detected = len(detected_lines)
        n_total = len(BALMER_LINES)
        
        # 估计磁场
        B_tesla = estimate_magnetic_field(wavelength, norm_flux, ivar)
        
        result = {
            'name': name,
            'type': wd_type,
            'ra_deg': ra_deg,
            'dec_deg': dec_deg,
            'specObjID': specObjID,
            'n_detected': n_detected,
            'n_total': n_total,
            'detected_fraction': n_detected / n_total,
            'detected_lines': detected_lines,
            'B_tesla_estimated': B_tesla,
            'n_pixels': len(wavelength),
        }
        
        all_results.append(result)
        
        print(f"  检测到 {n_detected}/{n_total} 条 Balmer 线: {detected_lines}")
        if B_tesla is not None:
            print(f"  估计磁场 B = {B_tesla:.2e} T")
        print()
    
    print("=" * 90)
    print("汇总分析")
    print("=" * 90)
    print()
    
    if len(all_results) == 0:
        print("没有成功分析的白矮星。")
        return
    
    # 按类型和磁场分组
    magnetic_results = [r for r in all_results if r['type'] == 'magnetic']
    da_results = [r for r in all_results if r['type'] == 'da']
    
    print(f"总分析数: {len(all_results)}")
    print(f"  磁场白矮星: {len(magnetic_results)}")
    print(f"  对照 DA 白矮星: {len(da_results)}")
    print()
    
    # 平均检测率
    if magnetic_results:
        mag_mean_frac = np.mean([r['detected_fraction'] for r in magnetic_results])
        print(f"磁场白矮星平均 Balmer 线检测率: {mag_mean_frac:.3f}")
    
    if da_results:
        da_mean_frac = np.mean([r['detected_fraction'] for r in da_results])
        print(f"对照 DA 白矮星平均 Balmer 线检测率: {da_mean_frac:.3f}")
    
    if magnetic_results and da_results:
        diff = da_mean_frac - mag_mean_frac
        print(f"差异: {diff:.3f} ({diff*100:.1f}%)")
        print(f"  （正值表示磁场白矮星检测率更低，可能存在拓扑禁戒）")
    
    print()
    
    # 详细列表
    print("详细结果：")
    print()
    print(f"{'名称':<20} {'类型':<10} {'检测数':>6} {'检测率':>8} {'估计B(T)':>12}")
    print("-" * 60)
    for r in all_results:
        B_str = f"{r['B_tesla_estimated']:.2e}" if r['B_tesla_estimated'] is not None else "N/A"
        print(f"{r['name']:<20} {r['type']:<10} {r['n_detected']:>3d}/{r['n_total']:<2d} "
              f"{r['detected_fraction']:>8.3f} {B_str:>12}")
    
    print()
    
    # 保存结果
    import json
    output_file = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\results\white_dwarf_spectral_analysis_v2.json"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            'n_analyzed': len(all_results),
            'n_magnetic': len(magnetic_results),
            'n_da': len(da_results),
            'magnetic_mean_detection_fraction': float(mag_mean_frac) if magnetic_results else None,
            'da_mean_detection_fraction': float(da_mean_frac) if da_results else None,
            'results': all_results,
        }, f, indent=2, ensure_ascii=False)
    
    print(f"结果已保存到: {output_file}")

if __name__ == "__main__":
    main()
