"""
下载并分析 3 颗白矮星的蓝端 SDSS 光谱
"""
import numpy as np
from astroquery.sdss import SDSS
import warnings
warnings.filterwarnings('ignore')
import json

BALMER = {'Hα':6562.8,'Hβ':4861.3,'Hγ':4340.5,'Hδ':4101.7,'Hε':3970.1,'Hζ':3889.1,'Hη':3835.4}
OTHER = [3933.7,3968.5,4300.0,5175.0,5890.0,7600.0,7699.0]

TARGETS = [
    {'name': 'J233817.93+083732.6', 'plate': 6161, 'mjd': 56238, 'fiber': 622, 'B_tesla': 1.2e4, 'Teff': 11534, 'Mstar': 0.72},
    {'name': 'J225828.48+280828.8', 'plate': 6293, 'mjd': 56561, 'fiber': 264, 'B_tesla': 1.4e4, 'Teff': 10618, 'Mstar': 1.02},
    {'name': 'J101712.60+233646.6', 'plate': 6458, 'mjd': 56274, 'fiber': 968, 'B_tesla': 1.4e4, 'Teff': 10843, 'Mstar': 1.04},
]

def log(m): print(m, flush=True)

def get_spectrum(plate, mjd, fiber):
    """获取 SDSS 光谱"""
    try:
        sp = SDSS.get_spectra(plate=plate, mjd=mjd, fiberID=fiber)
        if sp and len(sp) > 0:
            d = sp[0][1].data
            wl = 10**d['loglam']
            fl = np.array(d['flux'], dtype=float)
            ivar = np.array(d['ivar'], dtype=float)
            return wl, fl, ivar
    except Exception as e:
        log(f"    下载失败: {e}")
    return None, None, None

def normalize(wl, fl):
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

def measure_ew(wl, fl, center, window=80):
    m = (wl >= center - window) & (wl <= center + window)
    if np.sum(m) < 5:
        return 0.0, False
    w, f = wl[m], fl[m]
    ew = float(np.trapezoid(1.0 - f, w))
    cm = np.abs(w - center) < 5
    depth = 1.0 - np.median(f[cm]) if np.sum(cm) > 0 else 0
    return ew, (ew > 0.5 and depth > 0.03)

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

def main():
    log("="*70)
    log("下载并分析 3 颗白矮星的蓝端 SDSS 光谱")
    log("="*70)
    
    results = []
    
    for target in TARGETS:
        log(f"\n{'='*70}")
        log(f"{target['name']}")
        log(f"  plate={target['plate']}, mjd={target['mjd']}, fiber={target['fiber']}")
        log(f"{'='*70}")
        
        # 下载光谱
        log(f"  下载光谱...")
        wl, fl, ivar = get_spectrum(target['plate'], target['mjd'], target['fiber'])
        
        if wl is not None:
            log(f"    波长范围: {wl.min():.1f}-{wl.max():.1f} Å, 像素数: {len(wl)}")
            
            # 计算 SNR
            mask = np.ones(len(wl), dtype=bool)
            for lw in list(BALMER.values()) + OTHER:
                mask &= (np.abs(wl - lw) > 30)
            mask &= (wl >= 4000) & (wl <= 7000)
            if ivar is not None and len(ivar) == len(fl):
                valid = mask & (ivar > 0)
                if np.sum(valid) > 0:
                    snr = np.median(fl[valid] * np.sqrt(ivar[valid]))
                    log(f"    SNR/像素: {snr:.1f}")
            
            # 归一化
            nf = normalize(wl, fl)
            
            # 测量 Balmer 线
            log(f"  测量 Balmer 线 EW:")
            total_ew = 0.0
            n_detected = 0
            line_results = {}
            for line_name, line_wl in BALMER.items():
                ew, det = measure_ew(wl, nf, line_wl)
                status = "✓" if det else "✗"
                log(f"    {line_name}: EW={ew:.2f} Å, 检测={status}")
                line_results[line_name] = {'EW': ew, 'detected': det}
                if det:
                    total_ew += ew
                    n_detected += 1
            
            log(f"  总 EW={total_ew:.2f} Å, 检测到 {n_detected}/7 条线")
            
            # 计算理论 EW 和残差
            lg = log_g(target['Mstar'])
            tew = theo_ew(target['Teff'], lg)
            ratio = total_ew / tew if total_ew > 0 else 0.0
            resid = np.log10(ratio) if ratio > 0 else -3.0
            
            log(f"  理论 EW={tew:.2f} Å, 观测/理论={ratio:.3f}, 残差={resid:.3f} dex")
            
            results.append({
                'name': target['name'],
                'plate': target['plate'],
                'mjd': target['mjd'],
                'fiber': target['fiber'],
                'B_tesla': target['B_tesla'],
                'Teff': target['Teff'],
                'Mstar': target['Mstar'],
                'log_g': lg,
                'wavelength_min': float(wl.min()),
                'wavelength_max': float(wl.max()),
                'total_EW': total_ew,
                'n_detected': n_detected,
                'theo_EW': tew,
                'obs_theo_ratio': ratio,
                'residual_dex': float(resid),
                'line_results': line_results,
                'status': 'success',
            })
        else:
            log(f"  光谱下载失败")
            results.append({'name': target['name'], 'status': 'failed'})
    
    # 保存结果
    out = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\results\blue_end_sdss_spectra_analysis.json"
    with open(out, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False, default=str)
    
    log(f"\n{'='*70}")
    log(f"结果已保存: {out}")
    log(f"{'='*70}")
    
    # 总结
    log(f"\n总结:")
    for r in results:
        if r.get('status') == 'success':
            log(f"  {r['name']}: 总EW={r['total_EW']:.2f} Å, 检测={r['n_detected']}/7, "
                f"残差={r['residual_dex']:.3f} dex")
        else:
            log(f"  {r['name']}: {r['status']}")
    
    # 与 v10 结果合并的影响
    log(f"\n对 v10 样本的影响:")
    n_success = sum(1 for r in results if r.get('status') == 'success' and r['total_EW'] > 0)
    log(f"  新增有效中场白矮星: {n_success} 颗")
    log(f"  v10 原有有效中场: 13 颗")
    log(f"  合并后有效中场: {13 + n_success} 颗")

if __name__ == "__main__":
    main()
