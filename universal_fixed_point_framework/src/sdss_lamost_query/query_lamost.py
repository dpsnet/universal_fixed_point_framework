"""
查询 LAMOST 光谱补充 3 颗缺蓝端白矮星

目标：
1. J233817.93+083732.6 (RA=354.5747, Dec=8.6257)
2. J225828.48+280828.8 (RA=344.6187, Dec=28.1413)
3. J101712.60+233646.6 (RA=154.3025, Dec=23.6129)

方法：
1. 通过 VizieR 查询 LAMOST DR7/DR8 光谱目录
2. 通过 LAMOST 官方 API 查询
3. 通过 MAST 查询
4. 下载光谱并测量 Balmer 线 EW
"""
import numpy as np
from astroquery.vizier import Vizier
from astropy import coordinates
from astropy import units as u
import warnings
warnings.filterwarnings('ignore')
import json
import time

Vizier.ROW_LIMIT = 5000

# 3 颗目标白矮星
TARGETS = [
    {'name': 'J233817.93+083732.6', 'ra': 354.5747, 'dec': 8.6257, 'B_tesla': 1.2e4, 'Teff': 11534},
    {'name': 'J225828.48+280828.8', 'ra': 344.6187, 'dec': 28.1413, 'B_tesla': 1.4e4, 'Teff': 10618},
    {'name': 'J101712.60+233646.6', 'ra': 154.3025, 'dec': 23.6129, 'B_tesla': 1.4e4, 'Teff': 10843},
]

BALMER = {'Hα':6562.8,'Hβ':4861.3,'Hγ':4340.5,'Hδ':4101.7,'Hε':3970.1,'Hζ':3889.1,'Hη':3835.4}
OTHER = [3933.7,3968.5,4300.0,5175.0,5890.0,7600.0,7699.0]

def log(m): print(m, flush=True)

def query_vizier_lamost(target):
    """通过 VizieR 查询 LAMOST 光谱"""
    log(f"\n  查询 VizieR LAMOST 目录...")
    try:
        coord = coordinates.SkyCoord(ra=target['ra'], dec=target['dec'], unit=(u.deg, u.deg))
        
        # 尝试多个 LAMOST 目录
        catalogs_to_try = [
            'V/156',   # LAMOST DR7 恒星参数
            'V/153',   # LAMOST DR6
            'II/364',  # LAMOST DR5
            'J/ApJS/257/15',  # LAMOST DR8 白矮星
            'J/ApJS/254/23',  # LAMOST DR7 白矮星
        ]
        
        results = []
        for cat in catalogs_to_try:
            try:
                log(f"    尝试目录 {cat}...")
                result = Vizier.query_region(coord, radius=5*u.arcsec, catalog=cat)
                if result and len(result) > 0:
                    for table_name in result.keys():
                        table = result[table_name]
                        if len(table) > 0:
                            log(f"      {table_name}: {len(table)} 条记录")
                            for i in range(min(len(table), 3)):
                                row = table[i]
                                results.append({
                                    'catalog': cat,
                                    'table': table_name,
                                    'row': {col: str(row[col]) for col in table.colnames},
                                })
            except Exception as e:
                log(f"      失败: {e}")
        
        return results
    except Exception as e:
        log(f"    VizieR 查询失败: {e}")
        return []

def query_lamost_api(target):
    """通过 LAMOST 官方 API 查询光谱"""
    log(f"\n  查询 LAMOST 官方 API...")
    try:
        import urllib.request
        import urllib.parse
        
        # LAMOST DR8 API
        params = urllib.parse.urlencode({
            'ra': target['ra'],
            'dec': target['dec'],
            'radius': 5,  # 角秒
            'output.format': 'json',
        })
        url = f"http://www.lamost.org/lamost/dr8/query?{params}"
        log(f"    URL: {url}")
        
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        response = urllib.request.urlopen(req, timeout=30)
        data = json.loads(response.read().decode('utf-8'))
        log(f"    返回记录数: {len(data.get('data', []))}")
        return data
    except Exception as e:
        log(f"    LAMOST API 失败: {e}")
        return None

def query_mast(target):
    """通过 MAST 查询 LAMOST 光谱"""
    log(f"\n  查询 MAST...")
    try:
        from astroquery.mast import Mast
        coord = coordinates.SkyCoord(ra=target['ra'], dec=target['dec'], unit=(u.deg, u.deg))
        result = Mast.query_region(coord, radius=5*u.arcsec)
        if result and len(result) > 0:
            log(f"    MAST 返回 {len(result)} 条记录")
            # 筛选 LAMOST
            lamost_rows = []
            for i in range(len(result)):
                row = result[i]
                if 'lamost' in str(row).lower() or 'LAMOST' in str(row):
                    lamost_rows.append(row)
            log(f"    其中 LAMOST: {len(lamost_rows)} 条")
            return result
        else:
            log(f"    MAST 无结果")
    except Exception as e:
        log(f"    MAST 查询失败: {e}")
    return None

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
    log("查询 LAMOST 补充 3 颗缺蓝端白矮星光谱")
    log("="*70)
    
    all_results = {}
    
    for target in TARGETS:
        log(f"\n{'='*70}")
        log(f"目标: {target['name']}")
        log(f"  RA={target['ra']:.4f}, Dec={target['dec']:.4f}")
        log(f"  B={target['B_tesla']:.1e} T, Teff={target['Teff']:.0f} K")
        log(f"{'='*70}")
        
        target_results = {}
        
        # 1. VizieR 查询
        vizier_results = query_vizier_lamost(target)
        target_results['vizier'] = vizier_results
        
        # 2. LAMOST API
        api_results = query_lamost_api(target)
        target_results['lamost_api'] = api_results
        
        # 3. MAST
        mast_results = query_mast(target)
        target_results['mast'] = str(mast_results) if mast_results is not None else None
        
        all_results[target['name']] = target_results
        
        time.sleep(1)
    
    # 保存结果
    out = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\results\lamost_query_results.json"
    with open(out, 'w', encoding='utf-8') as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False, default=str)
    
    log(f"\n{'='*70}")
    log(f"查询结果已保存: {out}")
    log(f"{'='*70}")
    
    # 总结
    log(f"\n总结:")
    for name, res in all_results.items():
        n_vizier = len(res.get('vizier', []))
        has_api = res.get('lamost_api') is not None
        has_mast = res.get('mast') is not None
        log(f"  {name}: VizieR={n_vizier}条, API={'有' if has_api else '无'}, MAST={'有' if has_mast else '无'}")

if __name__ == "__main__":
    main()
