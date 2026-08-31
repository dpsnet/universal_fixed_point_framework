"""
调试：尝试多种方法获取白矮星光谱
1. SDSS.get_spectra 直接通过坐标
2. SDSS SQL 查询（简化版）
3. 检查 SDSS 数据版本
"""
from astroquery.sdss import SDSS
from astropy import coordinates as coords
from astropy import units as u
import warnings
warnings.filterwarnings('ignore')

# GD 153 坐标
c = coords.SkyCoord(194.2597, 22.0313, unit=(u.deg, u.deg))

print("方法 1: SDSS.get_spectra 直接通过坐标")
try:
    sp = SDSS.get_spectra(matches=c, radius=10 * u.arcsec)
    if sp is not None and len(sp) > 0:
        print(f"  获取到 {len(sp)} 个光谱")
        for i, s in enumerate(sp):
            print(f"  光谱 {i}: HDUs = {len(s)}")
    else:
        print("  无结果")
except Exception as e:
    print(f"  失败: {e}")

print()
print("方法 2: SDSS SQL 简化查询")
try:
    query = """
    SELECT TOP 5 specObjID, ra, dec, modelMag_g, subClass
    FROM SpecObj
    WHERE specClass = 3 AND modelMag_g < 17
    """
    result = SDSS.query_sql(query)
    if result is not None:
        print(f"  查询到 {len(result)} 条记录")
        print(f"  字段: {result.colnames}")
        print(result)
    else:
        print("  无结果")
except Exception as e:
    print(f"  失败: {e}")

print()
print("方法 3: 检查 SDSS 可用数据版本")
try:
    # 尝试查询 SDSS DR16
    print("  尝试指定 DR16...")
    # astroquery 的 SDSS 可能不支持指定版本
    # 让我们看看默认查询什么
except Exception as e:
    print(f"  失败: {e}")
