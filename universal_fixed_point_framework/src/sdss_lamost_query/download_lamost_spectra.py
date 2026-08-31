"""
下载 LAMOST 光谱并测量 Balmer 线 EW
"""
import numpy as np
import warnings
warnings.filterwarnings('ignore')
import json
import urllib.request
import os

BALMER = {'Hα':6562.8,'Hβ':4861.3,'Hγ':4340.5,'Hδ':4101.7,'Hε':3970.1,'Hζ':3889.1,'Hη':3835.4}
OTHER = [3933.7,3968.5,4300.0,5175.0,5890.0,7600.0,7699.0]

TARGETS = [
    {'name': 'J233817.93+083732.6', 'obsid': 355002136, 'B_tesla': 1.2e4, 'Teff': 11534},
    {'name': 'J101712.60+233646.6', 'obsid': 448412228, 'B_tesla': 1.4e4, 'Teff': 10843},
]

SPEC_DIR = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\data\lamost_spectra"
os.makedirs(SPEC_DIR, exist_ok=True)

def log(m): print(m, flush=True)

def download_lamost_spectrum(obsid):
    """尝试多种 URL 格式下载 LAMOST 光谱"""
    urls_to_try = [
        f"http://dr7.lamost.org/v2.0/spectrum/fits?obsid={obsid}",
        f"http://www.lamost.org/lamost/dr7/spectrum/fits/{obsid}.fits",
        f"http://dr7.lamost.org/v2.0/spectrum?obsid={obsid}",
        f"https://dr7.lamost.org/v2.0/spectrum/fits?obsid={obsid}",
    ]
    
    for url in urls_to_try:
        try:
            log(f"    尝试: {url}")
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            response = urllib.request.urlopen(req, timeout=30)
            data = response.read()
            if len(data) > 1000:
                filepath = os.path.join(SPEC_DIR, f"lamost_{obsid}.fits")
                with open(filepath, 'wb') as f:
                    f.write(data)
                log(f"    成功! 大小: {len(data)} 字节, 保存到: {filepath}")
                return filepath
            else:
                log(f"    返回数据太小: {len(data)} 字节")
        except Exception as e:
            log(f"    失败: {e}")
    return None

def read_lamost_fits(filepath):
    """读取 LAMOST FITS 光谱"""
    try:
        from astropy.io import fits
        with fits.open(filepath) as hdul:
            # LAMOST 光谱通常在第 1 个 HDU
            # 波长可能在 loglam 或 wavelength 列
            # 通量在 flux 列
            data = hdul[0].data
            header = hdul[0].header
            
            # 尝试不同的数据结构
            if data is not None and hasattr(data, 'names') and data.names:
                log(f"      列名: {data.names}")
                if 'wavelength' in data.names:
                    wl = np.array(data['wavelength'], dtype=float)
                elif 'loglam' in data.names:
                    wl = 10**np.array(data['loglam'], dtype=float)
                else:
                    # 尝试从 header 获取波长信息
                    if 'CRVAL1' in header:
                        crval = header['CRVAL1']
                        cdelt = header.get('CDELT1', header.get('CD1_1', 1))
                        naxis = header.get('NAXIS1', len(data))
                        wl = crval + cdelt * np.arange(naxis)
                    else:
                        wl = None
                
                if 'flux' in data.names:
                    fl = np.array(data['flux'], dtype=float)
                elif 'FLUX' in data.names:
                    fl = np.array(data['FLUX'], dtype=float)
                else:
                    fl = None
                
                if wl is not None and fl is not None:
                    log(f"      波长范围: {wl.min():.1f}-{wl.max():.1f} Å, 像素数: {len(wl)}")
                    return wl, fl
            else:
                # 尝试 1D 数组
                if isinstance(data, np.ndarray) and data.ndim == 1:
                    fl = np.array(data, dtype=float)
                    if 'CRVAL1' in header:
                        crval = header['CRVAL1']
                        cdelt = header.get('CDELT1', header.get('CD1_1', 1))
                        wl = crval + cdelt * np.arange(len(fl))
                        log(f"      波长范围: {wl.min():.1f}-{wl.max():.1f} Å")
                        return wl, fl
    except Exception as e:
        log(f"      读取失败: {e}")
    return None, None

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

def main():
    log("="*70)
    log("下载并分析 LAMOST 光谱")
    log("="*70)
    
    results = []
    
    for target in TARGETS:
        log(f"\n{'='*70}")
        log(f"{target['name']} (ObsID={target['obsid']})")
        log(f"{'='*70}")
        
        # 下载光谱
        filepath = download_lamost_spectrum(target['obsid'])
        
        if filepath:
            # 读取光谱
            log(f"  读取光谱...")
            wl, fl = read_lamost_fits(filepath)
            
            if wl is not None and fl is not None:
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
                
                results.append({
                    'name': target['name'],
                    'obsid': target['obsid'],
                    'B_tesla': target['B_tesla'],
                    'Teff': target['Teff'],
                    'spectrum_file': filepath,
                    'wavelength_range': [float(wl.min()), float(wl.max())],
                    'total_EW': total_ew,
                    'n_detected': n_detected,
                    'line_results': line_results,
                    'status': 'success',
                })
            else:
                log(f"  光谱读取失败")
                results.append({'name': target['name'], 'status': 'read_failed'})
        else:
            log(f"  光谱下载失败")
            results.append({'name': target['name'], 'status': 'download_failed'})
    
    # 保存结果
    out = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\results\lamost_spectrum_analysis.json"
    with open(out, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False, default=str)
    
    log(f"\n{'='*70}")
    log(f"结果已保存: {out}")
    log(f"{'='*70}")
    
    # 总结
    log(f"\n总结:")
    for r in results:
        if r.get('status') == 'success':
            log(f"  {r['name']}: 总EW={r['total_EW']:.2f} Å, 检测={r['n_detected']}/7")
        else:
            log(f"  {r['name']}: {r['status']}")

if __name__ == "__main__":
    main()
