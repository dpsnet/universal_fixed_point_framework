"""
白矮星光谱分析 v3：多数据源尝试

1. VizieR 白矮星目录查询
2. 直接 HTTP 请求 SDSS 光谱
3. 文献数据整理（如果在线获取失败）
"""

import numpy as np
import warnings
warnings.filterwarnings('ignore')

# 尝试 VizieR
print("=" * 70)
print("尝试 1: VizieR 白矮星目录")
print("=" * 70)

try:
    from astroquery.vizier import Vizier
    
    # 查询 McCook & Sion 白矮星目录（VizieR 目录 ID）
    # 这是一个经典的白矮星目录
    Vizier.ROW_LIMIT = 50
    
    # 尝试查询磁场白矮星目录
    # Wickramasinghe & Ferrario 2000 目录
    catalog_list = Vizier.find_catalogs('magnetic white dwarf')
    print(f"找到 {len(catalog_list)} 个相关目录")
    for name, desc in list(catalog_list.items())[:5]:
        print(f"  {name}: {desc.description[:80]}")
    
    print()
    
    # 尝试查询 McCook & Sion 目录（白矮星目录）
    # 目录可能是 VIII/76 或类似
    result = Vizier.query_constraints(catalog='VIII/76', mag='<16')
    if result is not None and len(result) > 0:
        print(f"McCook & Sion 目录: {len(result[0])} 条记录")
        print(f"字段: {result[0].colnames}")
        print(result[0][:5])
    else:
        print("McCook & Sion 目录无结果")
        
except Exception as e:
    print(f"VizieR 查询失败: {e}")
    import traceback
    traceback.print_exc()

print()
print("=" * 70)
print("尝试 2: 直接 HTTP 请求 SDSS SkyServer")
print("=" * 70)

try:
    import requests
    
    # SDSS SkyServer SQL 查询 API
    url = "https://skyserver.sdss.org/dr16/en/tools/search/x_sql.aspx"
    params = {
        'format': 'csv',
        'cmd': "SELECT TOP 10 specObjID, ra, dec, modelMag_g, subClass FROM SpecObj WHERE specClass=3 AND modelMag_g < 16"
    }
    
    print(f"请求 URL: {url}")
    response = requests.get(url, params=params, timeout=30)
    print(f"状态码: {response.status_code}")
    print(f"响应长度: {len(response.text)}")
    print(f"响应前 500 字符:")
    print(response.text[:500])
    
except Exception as e:
    print(f"HTTP 请求失败: {e}")

print()
print("=" * 70)
print("尝试 3: LAMOST 数据")
print("=" * 70)

try:
    import requests
    
    # LAMOST DR8 API
    # 查询白矮星光谱
    url = "http://www.lamost.org/dr8/en/v/search/"
    params = {
        'objname': 'white dwarf',
        'limit': 10,
    }
    
    print(f"请求 LAMOST 搜索 API...")
    # LAMOST 的 API 可能需要不同的接口
    # 让我们尝试直接访问
    print("LAMOST API 可能需要注册，跳过直接查询")
    
except Exception as e:
    print(f"LAMOST 查询失败: {e}")

print()
print("=" * 70)
print("结论")
print("=" * 70)
print("如果以上方法都失败，将使用文献数据整理方案。")
print("文献数据来源：")
print("  - Wickramasinghe & Ferrario (2000) 磁场白矮星目录")
print("  - Putney (1997) 磁场白矮星光谱")
print("  - Landstreet et al. (2015) 磁场白矮星统计")
print("  - SDSS DR7 白矮星目录 (Kleinman et al. 2013)")
