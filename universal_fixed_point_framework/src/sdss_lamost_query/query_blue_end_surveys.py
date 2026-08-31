"""
查询其他蓝端光谱巡天补充 3 颗缺蓝端白矮星

目标：
1. J233817.93+083732.6 (RA=354.5747, Dec=8.6257)
2. J225828.48+280828.8 (RA=344.6187, Dec=28.1413)
3. J101712.60+233646.6 (RA=154.3025, Dec=23.6129)

查询巡天：
- SDSS 多期光谱（检查是否有其他观测包含蓝端）
- GALAH DR3 (V/162)
- Gaia-ESO (J/A+A/666/A120)
- WEAVE (如果有公开数据)
- Pristine (如果有公开数据)
- RAVE (红端，可能不适合，但查询一下)
- 4MOST (可能还没有公开数据)
"""
import numpy as np
from astroquery.vizier import Vizier
from astroquery.sdss import SDSS
from astropy import coordinates
from astropy import units as u
import warnings
warnings.filterwarnings('ignore')
import json
import time

Vizier.ROW_LIMIT = 5000

TARGETS = [
    {'name': 'J233817.93+083732.6', 'ra': 354.5747, 'dec': 8.6257, 'sdss_spid': None},
    {'name': 'J225828.48+280828.8', 'ra': 344.6187, 'dec': 28.1413, 'sdss_spid': None},
    {'name': 'J101712.60+233646.6', 'ra': 154.3025, 'dec': 23.6129, 'sdss_spid': None},
]

# 先从 Amorim+ 2023 目录获取 SDSS Sp-ID
def load_sdss_spids():
    log("加载 Amorim+ 2023 目录获取 Sp-ID...")
    res = Vizier.get_catalogs('J/ApJ/944/56')
    t = res[0]
    spid_map = {}
    for i in range(len(t)):
        name = str(t['SDSS'][i])
        spid = str(t['Sp-ID'][i])
        spid_map[name] = spid
    for target in TARGETS:
        target['sdss_spid'] = spid_map.get(target['name'])
        log(f"  {target['name']}: Sp-ID={target['sdss_spid']}")

def log(m): print(m, flush=True)

def query_sdss_multiple(target):
    """查询 SDSS 多期光谱"""
    log(f"\n  查询 SDSS 多期光谱...")
    try:
        coord = coordinates.SkyCoord(ra=target['ra'], dec=target['dec'], unit=(u.deg, u.deg))
        # 查询 SDSS 光谱
        xid = SDSS.query_region(coord, spectro=True, radius=5*u.arcsec)
        if xid and len(xid) > 0:
            log(f"    找到 {len(xid)} 条 SDSS 光谱记录")
            spectra_info = []
            for i in range(len(xid)):
                row = xid[i]
                plate = row.get('plate')
                mjd = row.get('mjd')
                fiber = row.get('fiberID')
                z = row.get('z')
                spec_class = row.get('class')
                sub_class = row.get('subClass')
                log(f"      {i}: plate={plate}, mjd={mjd}, fiber={fiber}, z={z}, class={spec_class}, sub={sub_class}")
                spectra_info.append({
                    'plate': str(plate),
                    'mjd': str(mjd),
                    'fiber': str(fiber),
                    'z': str(z),
                    'class': str(spec_class),
                    'subClass': str(sub_class),
                })
            
            # 尝试下载每条光谱并检查波长覆盖
            log(f"    下载并检查波长覆盖...")
            for i, info in enumerate(spectra_info):
                try:
                    sp = SDSS.get_spectra(plate=int(info['plate']), mjd=int(info['mjd']), fiberID=int(info['fiber']))
                    if sp and len(sp) > 0:
                        d = sp[0][1].data
                        wl = 10**d['loglam']
                        log(f"      光谱 {i}: 波长 {wl.min():.0f}-{wl.max():.0f} Å, 像素 {len(wl)}")
                        info['wavelength_min'] = float(wl.min())
                        info['wavelength_max'] = float(wl.max())
                        info['has_blue_end'] = bool(wl.min() < 4500)
                except Exception as e:
                    log(f"      光谱 {i} 下载失败: {e}")
            
            return spectra_info
        else:
            log(f"    无 SDSS 光谱")
    except Exception as e:
        log(f"    SDSS 查询失败: {e}")
    return None

def query_vizier_catalog(target, catalog, catalog_name):
    """通过 VizieR 查询指定目录"""
    log(f"\n  查询 {catalog_name} ({catalog})...")
    try:
        coord = coordinates.SkyCoord(ra=target['ra'], dec=target['dec'], unit=(u.deg, u.deg))
        result = Vizier.query_region(coord, radius=10*u.arcsec, catalog=catalog)
        if result and len(result) > 0:
            for table_name in result.keys():
                table = result[table_name]
                if len(table) > 0:
                    log(f"    {table_name}: {len(table)} 条记录")
                    # 打印列名
                    log(f"    列: {list(table.colnames)[:20]}")
                    # 打印第一条记录
                    row = table[0]
                    for col in table.colnames[:15]:
                        val = row[col]
                        log(f"      {col}: {val}")
                    return table
        else:
            log(f"    无结果")
    except Exception as e:
        log(f"    查询失败: {e}")
    return None

def main():
    log("="*70)
    log("查询其他蓝端光谱巡天补充 3 颗缺蓝端白矮星")
    log("="*70)
    
    # 加载 SDSS Sp-ID
    load_sdss_spids()
    
    all_results = {}
    
    for target in TARGETS:
        log(f"\n{'='*70}")
        log(f"{target['name']}")
        log(f"  RA={target['ra']:.4f}, Dec={target['dec']:.4f}")
        log(f"{'='*70}")
        
        target_results = {}
        
        # 1. SDSS 多期光谱
        sdss_spectra = query_sdss_multiple(target)
        target_results['sdss_multiple'] = sdss_spectra
        
        # 2. GALAH DR3
        galah = query_vizier_catalog(target, 'V/162', 'GALAH DR3')
        target_results['galah_dr3'] = str(galah) if galah is not None else None
        
        # 3. Gaia-ESO
        gaia_eso = query_vizier_catalog(target, 'J/A+A/666/A120', 'Gaia-ESO')
        target_results['gaia_eso'] = str(gaia_eso) if gaia_eso is not None else None
        
        # 4. RAVE DR6
        rave = query_vizier_catalog(target, 'V/150', 'RAVE DR6')
        target_results['rave_dr6'] = str(rave) if rave is not None else None
        
        # 5. LAMOST DR7 (已查询，但再确认)
        lamost = query_vizier_catalog(target, 'V/156', 'LAMOST DR7')
        target_results['lamost_dr7'] = str(lamost) if lamost is not None else None
        
        all_results[target['name']] = target_results
        
        time.sleep(1)
    
    # 保存结果
    out = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\results\blue_end_surveys_query.json"
    with open(out, 'w', encoding='utf-8') as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False, default=str)
    
    log(f"\n{'='*70}")
    log(f"结果已保存: {out}")
    log(f"{'='*70}")
    
    # 总结
    log(f"\n总结:")
    for name, res in all_results.items():
        sdss = res.get('sdss_multiple')
        has_blue = False
        if sdss:
            for s in sdss:
                if s.get('has_blue_end'):
                    has_blue = True
                    break
        log(f"  {name}: SDSS多期={len(sdss) if sdss else 0}条(含蓝端={'是' if has_blue else '否'}), "
            f"GALAH={'有' if res.get('galah_dr3') else '无'}, "
            f"Gaia-ESO={'有' if res.get('gaia_eso') else '无'}, "
            f"RAVE={'有' if res.get('rave_dr6') else '无'}, "
            f"LAMOST={'有' if res.get('lamost_dr7') else '无'}")

if __name__ == "__main__":
    main()
