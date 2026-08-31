"""
查看 LAMOST 记录详情并尝试下载光谱
"""
import json
import numpy as np
from astroquery.vizier import Vizier
from astropy import coordinates
from astropy import units as u
import warnings
warnings.filterwarnings('ignore')

Vizier.ROW_LIMIT = 5000

TARGETS = [
    {'name': 'J233817.93+083732.6', 'ra': 354.5747, 'dec': 8.6257},
    {'name': 'J101712.60+233646.6', 'ra': 154.3025, 'dec': 23.6129},
]

def log(m): print(m, flush=True)

for target in TARGETS:
    log(f"\n{'='*70}")
    log(f"{target['name']}")
    log(f"{'='*70}")
    
    coord = coordinates.SkyCoord(ra=target['ra'], dec=target['dec'], unit=(u.deg, u.deg))
    
    # 查询 V/156 (LAMOST DR7)
    for cat in ['V/156', 'V/153']:
        log(f"\n  目录 {cat}:")
        try:
            result = Vizier.query_region(coord, radius=10*u.arcsec, catalog=cat)
            if result and len(result) > 0:
                for table_name in result.keys():
                    table = result[table_name]
                    log(f"    表 {table_name}: {len(table)} 条")
                    if len(table) > 0:
                        # 打印所有列名
                        log(f"    列: {list(table.colnames)}")
                        # 打印第一条记录的所有字段
                        row = table[0]
                        for col in table.colnames:
                            val = row[col]
                            log(f"      {col}: {val}")
            else:
                log(f"    无结果")
        except Exception as e:
            log(f"    查询失败: {e}")
