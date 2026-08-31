from astroquery.sdss import SDSS
from astropy import coordinates as coords
from astropy import units as u
import warnings
warnings.filterwarnings('ignore')

# 测试 GD 153（标准星，应该在 SDSS 中有光谱）
c = coords.SkyCoord(194.2597, 22.0313, unit=(u.deg, u.deg))

print("查询 SDSS 区域（半径 30 角秒）...")
xid = SDSS.query_region(c, radius=30 * u.arcsec, spectro=True)

if xid is not None:
    print(f"返回 {len(xid)} 条记录")
    print(f"字段名: {xid.colnames}")
    print(xid)
else:
    print("无结果")
    
    # 尝试不指定 spectro
    print()
    print("尝试不指定 spectro...")
    xid2 = SDSS.query_region(c, radius=30 * u.arcsec)
    if xid2 is not None:
        print(f"返回 {len(xid2)} 条记录")
        print(f"字段名: {xid2.colnames}")
        print(xid2)
