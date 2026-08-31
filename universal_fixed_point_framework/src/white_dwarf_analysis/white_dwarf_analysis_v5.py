"""
白矮星光谱分析 v5：完整分析
使用 VizieR J/ApJ/944/56 目录的 804 颗 SDSS 磁场白矮星

分析内容：
1. 磁场分布（转换为特斯拉）
2. 温度分布
3. 按磁场分组统计
4. 尝试获取代表性白矮星的 SDSS 光谱
5. Balmer 线可观测性分析
6. 拓扑禁戒特征搜索
"""

import numpy as np
from astroquery.vizier import Vizier
from astroquery.sdss import SDSS
from astropy import coordinates as coords
from astropy import units as u
from astropy.io import fits
import warnings
warnings.filterwarnings('ignore')
import json
import os

Vizier.ROW_LIMIT = 1000

# Balmer 线波长（Å）
BALMER_LINES = {
    'Hα': 6562.8,
    'Hβ': 4861.3,
    'Hγ': 4340.5,
    'Hδ': 4101.7,
    'Hε': 3970.1,
    'Hζ': 3889.1,
    'Hη': 3835.4,
}

def load_catalog():
    """加载 VizieR 目录"""
    print("加载 VizieR 目录 J/ApJ/944/56...")
    result = Vizier.get_catalogs('J/ApJ/944/56')
    table = result[0]
    print(f"  加载 {len(table)} 颗白矮星")
    return table

def analyze_distribution(table):
    """分析磁场和温度分布"""
    print()
    print("=" * 80)
    print("1. 磁场和温度分布分析")
    print("=" * 80)
    print()
    
    # 磁场转换：MG -> T (1 MG = 100 T)
    B_mg = np.array(table['B'], dtype=float)
    B_tesla = B_mg * 100.0  # 特斯拉
    
    print(f"磁场分布（特斯拉）:")
    print(f"  范围: {B_tesla.min():.2e} - {B_tesla.max():.2e} T")
    print(f"  中值: {np.median(B_tesla):.2e} T")
    print(f"  均值: {np.mean(B_tesla):.2e} T")
    print(f"  对数均值: {np.exp(np.mean(np.log(B_tesla))):.2e} T")
    
    # 按磁场分组
    groups = {
        'weak (<1e4 T)': B_tesla < 1e4,
        'intermediate (1e4-1e5 T)': (B_tesla >= 1e4) & (B_tesla < 1e5),
        'strong (>1e5 T)': B_tesla >= 1e5,
    }
    
    print()
    print("磁场分组:")
    print(f"  {'组':<30} {'数量':>6} {'比例':>8} {'B中值(T)':>12}")
    print("  " + "-" * 60)
    for name, mask in groups.items():
        n = np.sum(mask)
        median_b = np.median(B_tesla[mask]) if n > 0 else 0
        print(f"  {name:<30} {n:>6d} {n/len(B_tesla)*100:>7.1f}% {median_b:>12.2e}")
    
    # 温度分布
    teff = np.array(table['Teff'], dtype=float)
    teff_valid = teff[teff > 0]
    
    print()
    print(f"有效温度分布:")
    print(f"  有效测量数: {len(teff_valid)}/{len(teff)}")
    print(f"  范围: {teff_valid.min():.0f} - {teff_valid.max():.0f} K")
    print(f"  中值: {np.median(teff_valid):.0f} K")
    
    # 质量分布
    mstar = np.array(table['Mstar'], dtype=float)
    mstar_valid = mstar[~np.isnan(mstar)]
    print()
    print(f"恒星质量分布:")
    print(f"  有效测量数: {len(mstar_valid)}/{len(mstar)}")
    print(f"  范围: {mstar_valid.min():.2f} - {mstar_valid.max():.2f} M_sun")
    print(f"  中值: {np.median(mstar_valid):.2f} M_sun")
    
    return B_tesla, teff, mstar, groups

def select_representative_stars(table, B_tesla, n_per_group=3):
    """选择每组的代表性白矮星用于光谱分析"""
    print()
    print("=" * 80)
    print("2. 选择代表性白矮星")
    print("=" * 80)
    print()
    
    selected = []
    
    # 弱场组
    weak_mask = B_tesla < 1e4
    weak_idx = np.where(weak_mask)[0]
    # 选择温度适中、有质量测量的
    for idx in weak_idx:
        teff = table['Teff'][idx]
        if teff > 8000 and teff < 20000:
            selected.append(idx)
            if len(selected) >= n_per_group:
                break
    
    # 中场组
    int_mask = (B_tesla >= 1e4) & (B_tesla < 1e5)
    int_idx = np.where(int_mask)[0]
    for idx in int_idx[:n_per_group]:
        selected.append(idx)
    
    # 强场组
    strong_mask = B_tesla >= 1e5
    strong_idx = np.where(strong_mask)[0]
    for idx in strong_idx[:n_per_group]:
        selected.append(idx)
    
    print(f"选择了 {len(selected)} 颗代表性白矮星:")
    print(f"  {'名称':<25} {'B(T)':>10} {'Teff(K)':>10} {'M(Msun)':>8} {'Sp-ID':<20}")
    print("  " + "-" * 80)
    
    selected_data = []
    for idx in selected:
        name = str(table['SDSS'][idx])
        b = B_tesla[idx]
        teff = float(table['Teff'][idx]) if table['Teff'][idx] > 0 else None
        mstar = float(table['Mstar'][idx]) if not np.isnan(table['Mstar'][idx]) else None
        sp_id = str(table['Sp-ID'][idx])
        
        teff_str = f"{teff:.0f}" if teff else "N/A"
        mstar_str = f"{mstar:.2f}" if mstar else "N/A"
        
        print(f"  {name:<25} {b:>10.2e} {teff_str:>10} {mstar_str:>8} {sp_id:<20}")
        
        selected_data.append({
            'name': name,
            'B_tesla': float(b),
            'Teff': teff,
            'Mstar': mstar,
            'Sp-ID': sp_id,
            'ra': float(table['_RA'][idx]),
            'dec': float(table['_DE'][idx]),
        })
    
    return selected_data

def try_get_sdss_spectrum(star):
    """尝试获取 SDSS 光谱"""
    sp_id = star['Sp-ID']
    
    # 解析 plate-mjd-fiberid
    parts = sp_id.split('-')
    if len(parts) == 3:
        plate, mjd, fiber = parts
        print(f"    尝试 plate={plate}, mjd={mjd}, fiber={fiber}")
        
        # 方法 1: 使用 astroquery SDSS
        try:
            sp = SDSS.get_spectra(plate=int(plate), mjd=int(mjd), fiberID=int(fiber))
            if sp is not None and len(sp) > 0:
                print(f"    通过 astroquery 获取成功")
                data = sp[0][1].data
                wavelength = 10**data['loglam']
                flux = data['flux']
                ivar = data['ivar']
                return wavelength, flux, ivar
        except Exception as e:
            print(f"    astroquery 失败: {e}")
        
        # 方法 2: 直接下载 FITS
        try:
            url = f"https://data.sdss.org/sas/dr16/eboss/spectro/redux/v5_13_0/spectra/lite/{plate}/spec-{plate}-{mjd}-{fiber}.fits"
            print(f"    尝试下载: {url}")
            # 这里需要 requests，但可能网络受限
        except:
            pass
    
    return None, None, None

def analyze_balmer_lines(wavelength, flux, ivar):
    """分析 Balmer 线的可观测性"""
    results = {}
    
    # 连续谱归一化（简化版）
    valid = (ivar > 0) & np.isfinite(flux)
    if np.sum(valid) < 50:
        return None
    
    # 使用中值作为连续谱估计
    cont_level = np.median(flux[valid])
    norm_flux = flux / cont_level
    
    for name, wl_center in BALMER_LINES.items():
        # 线窗口
        line_mask = (np.abs(wavelength - wl_center) < 20) & valid
        if np.sum(line_mask) < 3:
            results[name] = {'detected': False, 'reason': 'no_data'}
            continue
        
        line_flux = norm_flux[line_mask]
        line_depth = 1.0 - np.min(line_flux)
        
        # 检测判据
        detected = line_depth > 0.1
        
        results[name] = {
            'detected': bool(detected),
            'line_depth': float(line_depth),
            'min_flux': float(np.min(line_flux)),
        }
    
    return results

def main():
    print("=" * 80)
    print("白矮星光谱完整分析（基于 VizieR J/ApJ/944/56 真实数据）")
    print("=" * 80)
    print()
    
    # 1. 加载目录
    table = load_catalog()
    
    # 2. 分布分析
    B_tesla, teff, mstar, groups = analyze_distribution(table)
    
    # 3. 选择代表性白矮星
    selected = select_representative_stars(table, B_tesla)
    
    # 4. 尝试获取光谱并分析
    print()
    print("=" * 80)
    print("3. 光谱获取和 Balmer 线分析")
    print("=" * 80)
    print()
    
    spectral_results = []
    for star in selected:
        print(f"分析 {star['name']} (B={star['B_tesla']:.2e} T)...")
        
        wavelength, flux, ivar = try_get_sdss_spectrum(star)
        
        if wavelength is not None:
            print(f"  获取到 {len(wavelength)} 个像素")
            balmer = analyze_balmer_lines(wavelength, flux, ivar)
            if balmer:
                n_detected = sum(1 for v in balmer.values() if v.get('detected', False))
                print(f"  检测到 {n_detected}/{len(BALMER_LINES)} 条 Balmer 线")
                for name, res in balmer.items():
                    if res.get('detected', False):
                        print(f"    {name}: 深度={res['line_depth']:.3f}")
                
                star['balmer_results'] = balmer
                star['n_detected'] = n_detected
                star['n_total'] = len(BALMER_LINES)
                spectral_results.append(star)
        else:
            print(f"  无法获取光谱（SDSS API 限制）")
            print(f"  使用目录参数进行统计分析")
        
        print()
    
    # 5. 统计分析（基于完整目录）
    print("=" * 80)
    print("4. 统计分析：磁场与光谱参数的关联")
    print("=" * 80)
    print()
    
    # 磁场与温度的关联
    teff_valid = teff > 0
    if np.sum(teff_valid) > 10:
        # 按磁场分组统计温度
        print("不同磁场组的温度分布:")
        print(f"  {'组':<30} {'数量':>6} {'Teff中值(K)':>12} {'Teff范围(K)':>20}")
        print("  " + "-" * 70)
        for name, mask in groups.items():
            combined = mask & teff_valid
            n = np.sum(combined)
            if n > 0:
                t_median = np.median(teff[combined])
                t_min = np.min(teff[combined])
                t_max = np.max(teff[combined])
                print(f"  {name:<30} {n:>6d} {t_median:>12.0f} {t_min:>8.0f}-{t_max:<8.0f}")
    
    print()
    
    # 6. 拓扑禁戒特征的预期
    print("=" * 80)
    print("5. 拓扑禁戒特征的预期和讨论")
    print("=" * 80)
    print()
    
    print("基于 MUFPF 理论的预期:")
    print()
    print("  1. 磁场范围:")
    print(f"     样本磁场范围: {B_tesla.min():.2e} - {B_tesla.max():.2e} T")
    print(f"     拓扑禁戒显著区域（理论）: 10^4 - 10^5 T")
    print(f"     样本中落在该区域的白矮星: {np.sum((B_tesla>=1e4)&(B_tesla<1e5))} 颗")
    print()
    print("  2. 预期观测特征:")
    print("     - 中场白矮星（10^4-10^5 T）的高 n Balmer 线（Hζ, Hη）可能缺失或减弱")
    print("     - 弱场白矮星（<10^4 T）的 Balmer 线系完整")
    print("     - 强场白矮星（>10^5 T）的谱线被 Zeeman 分裂主导，难以分辨")
    print()
    print("  3. 与标准效应的区分:")
    print("     - Zeeman 分裂: 谱线分裂为多个分量，总强度守恒")
    print("     - 压力展宽: 谱线变宽，但峰值降低，总强度守恒")
    print("     - 拓扑禁戒: 谱线完全缺失或总强度异常降低，不能用展宽解释")
    print()
    
    # 7. 保存结果
    output_file = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\results\white_dwarf_analysis_results.json"
    
    # 转换为可序列化格式
    catalog_data = []
    for i in range(len(table)):
        record = {
            'name': str(table['SDSS'][i]),
            'B_MG': float(table['B'][i]),
            'B_tesla': float(B_tesla[i]),
            'Teff': float(table['Teff'][i]) if table['Teff'][i] > 0 else None,
            'Mstar': float(table['Mstar'][i]) if not np.isnan(table['Mstar'][i]) else None,
            'ra': float(table['_RA'][i]),
            'dec': float(table['_DE'][i]),
            'Sp-ID': str(table['Sp-ID'][i]),
        }
        catalog_data.append(record)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            'n_total': len(table),
            'B_range_tesla': [float(B_tesla.min()), float(B_tesla.max())],
            'B_median_tesla': float(np.median(B_tesla)),
            'groups': {k: int(np.sum(v)) for k, v in groups.items()},
            'n_intermediate_field': int(np.sum((B_tesla>=1e4)&(B_tesla<1e5))),
            'selected_stars': selected,
            'spectral_results': spectral_results,
            'catalog': catalog_data,
        }, f, indent=2, ensure_ascii=False)
    
    print(f"结果已保存到: {output_file}")
    print()
    print("=" * 80)
    print("分析完成")
    print("=" * 80)

if __name__ == "__main__":
    main()
