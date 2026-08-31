"""
通过 MAST API 下载 LAMOST 光谱
"""
import numpy as np
import warnings
warnings.filterwarnings('ignore')
import json
import os

TARGETS = [
    {'name': 'J233817.93+083732.6', 'ra': 354.5747, 'dec': 8.6257, 'obsid': 355002136},
    {'name': 'J101712.60+233646.6', 'ra': 154.3025, 'dec': 23.6129, 'obsid': 448412228},
]

SPEC_DIR = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\data\lamost_spectra"
os.makedirs(SPEC_DIR, exist_ok=True)

def log(m): print(m, flush=True)

def query_mast_observations(target):
    """通过 MAST 查询观测记录"""
    try:
        from astroquery.mast import Observations
        from astropy import coordinates
        from astropy import units as u
        
        coord = coordinates.SkyCoord(ra=target['ra'], dec=target['dec'], unit=(u.deg, u.deg))
        log(f"    查询 MAST Observations...")
        obs_table = Observations.query_criteria(coordinates=coord, radius=0.01*u.deg)
        if obs_table and len(obs_table) > 0:
            log(f"    找到 {len(obs_table)} 条观测记录")
            for i in range(min(len(obs_table), 5)):
                row = obs_table[i]
                log(f"      {i}: obs_collection={row.get('obs_collection')}, "
                    f"target_name={row.get('target_name')}, "
                    f"filters={row.get('filters')}")
            return obs_table
        else:
            log(f"    无观测记录")
    except Exception as e:
        log(f"    MAST Observations 查询失败: {e}")
    return None

def query_mast_catalog(target):
    """通过 MAST 目录查询"""
    try:
        from astroquery.mast import Catalogs
        from astropy import coordinates
        from astropy import units as u
        
        coord = coordinates.SkyCoord(ra=target['ra'], dec=target['dec'], unit=(u.deg, u.deg))
        log(f"    查询 MAST Catalogs (LAMOST)...")
        # 尝试查询 LAMOST 目录
        catalogs_to_try = ['LAMOST', 'lamost', 'GAIA', 'TIC']
        for cat in catalogs_to_try:
            try:
                result = Catalogs.query_criteria(catalog=cat, coordinates=coord, radius=0.01)
                if result and len(result) > 0:
                    log(f"      {cat}: {len(result)} 条")
                    return result
            except:
                pass
        log(f"    目录查询无结果")
    except Exception as e:
        log(f"    MAST Catalogs 查询失败: {e}")
    return None

def download_mast_products(obs_table, target):
    """下载 MAST 数据产品"""
    if obs_table is None or len(obs_table) == 0:
        return None
    
    try:
        from astroquery.mast import Observations
        
        # 获取数据产品列表
        log(f"    获取数据产品...")
        data_products = Observations.get_product_list(obs_table)
        if data_products and len(data_products) > 0:
            log(f"    找到 {len(data_products)} 个数据产品")
            for i in range(min(len(data_products), 10)):
                row = data_products[i]
                log(f"      {i}: productType={row.get('productType')}, "
                    f"productSubGroupDescription={row.get('productSubGroupDescription')}, "
                    f"productFilename={row.get('productFilename')}")
            
            # 筛选光谱产品
            spec_products = data_products[data_products['productType'] == 'SPECTRUM']
            if len(spec_products) == 0:
                spec_products = data_products  # 如果没有 SPECTRUM 类型，下载所有
            
            log(f"    下载 {len(spec_products)} 个光谱产品...")
            manifest = Observations.download_products(spec_products, download_dir=SPEC_DIR)
            log(f"    下载完成: {len(manifest)} 个文件")
            return manifest
        else:
            log(f"    无数据产品")
    except Exception as e:
        log(f"    MAST 下载失败: {e}")
    return None

def main():
    log("="*70)
    log("通过 MAST API 查询和下载 LAMOST 光谱")
    log("="*70)
    
    all_results = {}
    
    for target in TARGETS:
        log(f"\n{'='*70}")
        log(f"{target['name']}")
        log(f"{'='*70}")
        
        target_results = {}
        
        # 1. 查询 MAST Observations
        obs_table = query_mast_observations(target)
        target_results['observations'] = str(obs_table) if obs_table is not None else None
        
        # 2. 查询 MAST Catalogs
        cat_result = query_mast_catalog(target)
        target_results['catalogs'] = str(cat_result) if cat_result is not None else None
        
        # 3. 下载数据产品
        if obs_table is not None:
            manifest = download_mast_products(obs_table, target)
            target_results['manifest'] = str(manifest) if manifest is not None else None
        
        all_results[target['name']] = target_results
    
    # 保存结果
    out = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\results\mast_lamost_query.json"
    with open(out, 'w', encoding='utf-8') as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False, default=str)
    
    log(f"\n结果已保存: {out}")

if __name__ == "__main__":
    main()
