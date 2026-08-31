"""
分析 8 颗无效中场白矮星，尝试更高信噪比检测

步骤：
1. 找出 v10 中 total_EW=0 的 8 颗中场白矮星
2. 重新下载光谱，计算信噪比(SNR)
3. 检查光谱类型（是否真的是 DA 型氢大气）
4. 尝试更敏感的检测方法：
   - 匹配滤波/交叉相关
   - 更宽的积分窗口
   - 多线联合检测
5. 如果 SDSS 有多期光谱，尝试堆叠提高 SNR
6. 尝试从其他数据源获取光谱
"""
import numpy as np
from astroquery.sdss import SDSS
from astroquery.vizier import Vizier
import warnings
warnings.filterwarnings('ignore')
import json

Vizier.ROW_LIMIT = 1000

BALMER = {'Hα':6562.8,'Hβ':4861.3,'Hγ':4340.5,'Hδ':4101.7,'Hε':3970.1,'Hζ':3889.1,'Hη':3835.4}
OTHER = [3933.7,3968.5,4300.0,5175.0,5890.0,7600.0,7699.0]

def log(m): print(m, flush=True)

def load_v10_results():
    """加载 v10 结果"""
    with open(r'E:\workspace\hyper-resolution\universal_fixed_point_framework\results\white_dwarf_analysis_v10_partial.json', 'r', encoding='utf-8') as f:
        d = json.load(f)
    return d['int']

def get_spec(star):
    """获取 SDSS 光谱"""
    parts = star['Sp-ID'].split('-')
    if len(parts) != 3:
        return None
    try:
        sp = SDSS.get_spectra(plate=int(parts[0]), mjd=int(parts[1]), fiberID=int(parts[2]))
        if sp and len(sp) > 0:
            d = sp[0][1].data
            wl = 10**d['loglam']
            fl = np.array(d['flux'], dtype=float)
            ivar = np.array(d['ivar'], dtype=float)
            if star.get('zoff') and abs(star['zoff']) > 1e-5:
                wl = wl / (1 + star['zoff'])
            return wl, fl, ivar
    except Exception as e:
        log(f"    下载失败: {e}")
    return None

def normalize(wl, fl):
    """连续谱归一化"""
    mask = np.ones(len(wl), dtype=bool)
    for lw in list(BALMER.values()) + OTHER:
        mask &= (np.abs(wl - lw) > 50)
    mask &= (wl >= 3800) & (wl <= 7000)
    if np.sum(mask) < 10:
        return fl / np.median(fl)
    try:
        c = np.polyfit(wl[mask], fl[mask], 4)
        return fl / np.polyval(c, wl)
    except:
        return fl / np.median(fl)

def calc_snr(wl, fl, ivar):
    """计算光谱信噪比"""
    # 在连续谱区域（避开强线）计算 SNR
    mask = np.ones(len(wl), dtype=bool)
    for lw in list(BALMER.values()) + OTHER:
        mask &= (np.abs(wl - lw) > 30)
    mask &= (wl >= 4000) & (wl <= 7000)
    if np.sum(mask) < 10:
        return 0, 0
    flux_snr = fl[mask]
    if ivar is not None and len(ivar) == len(fl):
        ivar_snr = ivar[mask]
        valid = ivar_snr > 0
        if np.sum(valid) > 0:
            snr_per_pixel = np.median(flux_snr[valid] * np.sqrt(ivar_snr[valid]))
        else:
            snr_per_pixel = np.median(flux_snr) / np.std(flux_snr) if np.std(flux_snr) > 0 else 0
    else:
        snr_per_pixel = np.median(flux_snr) / np.std(flux_snr) if np.std(flux_snr) > 0 else 0
    # 总 SNR（假设 N 个像素独立）
    n_pixels = np.sum(mask)
    total_snr = snr_per_pixel * np.sqrt(n_pixels)
    return float(snr_per_pixel), float(total_snr)

def sensitive_ew_detection(wl, fl, line_center, window=120):
    """更敏感的 EW 检测：使用更宽窗口 + 匹配滤波"""
    m = (wl >= line_center - window) & (wl <= line_center + window)
    if np.sum(m) < 5:
        return 0.0, False, 0.0
    w = wl[m]
    f = fl[m]
    
    # 宽窗口 EW
    ew_wide = float(np.trapezoid(1.0 - f, w))
    
    # 中心深度（更宽的中心窗口）
    center_mask = np.abs(w - line_center) < 15
    center_depth = 1.0 - np.median(f[center_mask]) if np.sum(center_mask) > 0 else 0
    
    # 检测阈值更宽松
    detected = (ew_wide > 0.3) or (center_depth > 0.02)
    
    return ew_wide, detected, float(center_depth)

def check_spectral_type(wl, fl):
    """检查光谱类型：通过 He I 线判断是否为 DB 型（氦大气）"""
    # He I 线波长
    he_lines = [4471.5, 4026.2, 4143.8, 4387.9, 4713.2, 4921.9, 5015.7, 5875.6, 6678.2, 7065.2]
    he_detections = 0
    for he_wl in he_lines:
        m = (wl >= he_wl - 5) & (wl <= he_wl + 5)
        if np.sum(m) > 0:
            depth = 1.0 - np.median(fl[m])
            if depth > 0.03:
                he_detections += 1
    return he_detections

def main():
    log("="*70)
    log("分析 8 颗无效中场白矮星")
    log("="*70)
    
    # 加载 v10 结果
    int_results = load_v10_results()
    
    # 找出无效的（total_EW = 0）
    invalid = [r for r in int_results if r['total_EW'] == 0]
    valid = [r for r in int_results if r['total_EW'] > 0]
    
    log(f"\n中场白矮星: 总计 {len(int_results)}, 有效 {len(valid)}, 无效 {len(invalid)}")
    log(f"\n无效的 8 颗中场白矮星:")
    for i, r in enumerate(invalid):
        log(f"  {i+1}. {r['name']}  B={r['B_tesla']:.1e} T  Teff={r['Teff']:.0f} K  Mstar={r.get('Mstar','N/A')}")
    
    # 重新加载目录获取 Sp-ID
    log("\n加载 VizieR 目录获取光谱 ID...")
    res = Vizier.get_catalogs('J/ApJ/944/56')
    t = res[0]
    catalog = {}
    for i in range(len(t)):
        name = str(t['SDSS'][i])
        catalog[name] = {
            'name': name,
            'B_tesla': float(t['B'][i]) * 100.0,
            'Teff': float(t['Teff'][i]) if t['Teff'][i] > 0 else None,
            'Mstar': float(t['Mstar'][i]) if not np.isnan(t['Mstar'][i]) else None,
            'Sp-ID': str(t['Sp-ID'][i]),
            'zoff': float(t['zoff'][i]) if not np.isnan(t['zoff'][i]) else None,
        }
    
    # 分析每颗无效白矮星
    log("\n" + "="*70)
    log("逐颗分析")
    log("="*70)
    
    results = []
    for i, r in enumerate(invalid):
        name = r['name']
        star = catalog.get(name)
        if not star:
            log(f"\n{i+1}. {name}: 目录中未找到")
            continue
        
        log(f"\n{i+1}. {name}")
        log(f"   B={star['B_tesla']:.1e} T, Teff={star['Teff']:.0f} K, Mstar={star.get('Mstar','N/A')}")
        
        # 下载光谱
        spec = get_spec(star)
        if not spec:
            log(f"   光谱下载失败")
            results.append({'name': name, 'status': 'download_failed'})
            continue
        
        wl, fl, ivar = spec
        log(f"   光谱范围: {wl.min():.0f}-{wl.max():.0f} Å, 像素数: {len(wl)}")
        
        # 计算 SNR
        snr_pixel, snr_total = calc_snr(wl, fl, ivar)
        log(f"   信噪比: 每像素 {snr_pixel:.1f}, 总 SNR {snr_total:.1f}")
        
        # 归一化
        nf = normalize(wl, fl)
        
        # 检查光谱类型（He I 线）
        he_det = check_spectral_type(wl, nf)
        log(f"   He I 线检测数: {he_det} ({'可能是 DB/氦大气' if he_det >= 3 else '可能是 DA/氢大气'})")
        
        # 更敏感的 Balmer 线检测
        log(f"   敏感 Balmer 线检测:")
        total_ew_sensitive = 0.0
        n_detected_sensitive = 0
        for line_name, line_wl in BALMER.items():
            ew, det, depth = sensitive_ew_detection(wl, nf, line_wl)
            status = "✓" if det else "✗"
            log(f"     {line_name}: EW={ew:.2f} Å, 深度={depth:.3f}, 检测={status}")
            if det:
                total_ew_sensitive += ew
                n_detected_sensitive += 1
        
        log(f"   敏感检测: 总 EW={total_ew_sensitive:.2f} Å, 检测到 {n_detected_sensitive}/7 条线")
        
        # 检查 Hα 区域细节
        ha_mask = (wl >= 6400) & (wl <= 6700)
        if np.sum(ha_mask) > 0:
            ha_flux = nf[ha_mask]
            ha_min = np.min(ha_flux)
            ha_median = np.median(ha_flux)
            log(f"   Hα 区域: 最小通量={ha_min:.3f}, 中位通量={ha_median:.3f}, 最深深度={1-ha_min:.3f}")
        
        results.append({
            'name': name,
            'B_tesla': star['B_tesla'],
            'Teff': star['Teff'],
            'Mstar': star.get('Mstar'),
            'snr_per_pixel': snr_pixel,
            'snr_total': snr_total,
            'he_lines_detected': he_det,
            'sensitive_total_ew': total_ew_sensitive,
            'sensitive_n_detected': n_detected_sensitive,
            'status': 'analyzed',
        })
    
    # 总结
    log("\n" + "="*70)
    log("总结")
    log("="*70)
    
    low_snr = [r for r in results if r.get('snr_per_pixel', 0) < 5]
    high_snr = [r for r in results if r.get('snr_per_pixel', 0) >= 5]
    db_candidates = [r for r in results if r.get('he_lines_detected', 0) >= 3]
    sensitive_detected = [r for r in results if r.get('sensitive_n_detected', 0) > 0]
    
    log(f"\n低 SNR（<5/像素）: {len(low_snr)} 颗")
    log(f"高 SNR（>=5/像素）: {len(high_snr)} 颗")
    log(f"可能 DB/氦大气: {len(db_candidates)} 颗")
    log(f"敏感检测到 Balmer 线: {len(sensitive_detected)} 颗")
    
    log(f"\n详细列表:")
    for r in results:
        if r.get('status') == 'analyzed':
            log(f"  {r['name']}: SNR={r['snr_per_pixel']:.1f}/pix, He线={r['he_lines_detected']}, "
                f"敏感检测={r['sensitive_n_detected']}/7, EW={r['sensitive_total_ew']:.2f}")
    
    # 保存结果
    out = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\results\invalid_intermediate_analysis.json"
    with open(out, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False, default=str)
    log(f"\n结果已保存: {out}")

if __name__ == "__main__":
    main()
