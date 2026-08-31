"""
白矮星光谱分析 v4：使用 VizieR 目录 J/ApJ/944/56
(SDSS magnetic white dwarfs rich in hydrogen, Amorim+ 2023)

这个目录包含了 SDSS 中富氢磁场白矮星的磁场测量和光谱参数。
我们可以直接使用这些已发表的测量数据进行拓扑禁戒特征分析。
"""

import numpy as np
from astroquery.vizier import Vizier
import warnings
warnings.filterwarnings('ignore')
import json

Vizier.ROW_LIMIT = 1000  # 获取所有记录

print("=" * 80)
print("查询 VizieR 目录 J/ApJ/944/56 (SDSS 磁场白矮星)")
print("=" * 80)
print()

# 查询目录
catalog_id = 'J/ApJ/944/56'
try:
    result = Vizier.get_catalogs(catalog_id)
    print(f"目录包含 {len(result)} 个表:")
    for i, table in enumerate(result):
        print(f"  表 {i}: {table.meta.get('name', 'unknown')}, "
              f"{len(table)} 行, {len(table.colnames)} 列")
        print(f"    字段: {table.colnames[:15]}")
        if len(table.colnames) > 15:
            print(f"    ... 还有 {len(table.colnames)-15} 个字段")
    print()
except Exception as e:
    print(f"查询失败: {e}")
    import traceback
    traceback.print_exc()
    result = None

if result is None or len(result) == 0:
    print("无法获取目录数据，退出。")
    exit()

# 获取主表（通常是第一个表）
main_table = result[0]
print(f"主表: {len(main_table)} 颗白矮星")
print()

# 查看前几条记录
print("前 5 条记录:")
print(main_table[:5])
print()

# 分析字段
print("字段分析:")
for col in main_table.colnames:
    dtype = main_table[col].dtype
    n_valid = np.sum(main_table[col].astype(str) != '--')
    print(f"  {col:<20} dtype={str(dtype):<15} 有效值={n_valid}/{len(main_table)}")

print()

# 提取关键数据
# 通常包含：名称、RA、Dec、磁场强度、有效温度、表面重力、Hα 等谱线测量
data = []
for row in main_table:
    record = {}
    for col in main_table.colnames:
        val = row[col]
        # 转换为 Python 原生类型
        if hasattr(val, 'value'):
            val = val.value
        if isinstance(val, (np.floating, np.integer)):
            val = float(val)
        elif isinstance(val, np.ma.core.MaskedConstant):
            val = None
        record[col] = val
    data.append(record)

# 保存原始数据
output_file = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\results\sdss_magnetic_whitedwarfs_raw.json"
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False, default=str)
print(f"原始数据已保存到: {output_file}")
print()

# 尝试识别磁场字段
print("=" * 80)
print("磁场分布分析")
print("=" * 80)
print()

# 查找磁场相关字段
b_fields = [col for col in main_table.colnames 
             if any(kw in col.lower() for kw in ['b', 'field', 'mag', 'bz', 'bmean'])]
print(f"可能的磁场字段: {b_fields}")

# 查找温度和重力字段
teff_fields = [col for col in main_table.colnames if 'teff' in col.lower() or 'temp' in col.lower()]
logg_fields = [col for col in main_table.colnames if 'logg' in col.lower() or 'grav' in col.lower()]
print(f"可能的温度字段: {teff_fields}")
print(f"可能的重力字段: {logg_fields}")

# 查找谱线测量字段
line_fields = [col for col in main_table.colnames 
               if any(kw in col.lower() for kw in ['halpha', 'hbeta', 'hgamma', 'hdelta', 'ew', 'line'])]
print(f"可能的谱线字段: {line_fields}")

print()

# 如果有磁场字段，分析磁场分布
if b_fields:
    b_field = b_fields[0]
    print(f"使用磁场字段: {b_field}")
    
    b_values = []
    for row in main_table:
        val = row[b_field]
        if hasattr(val, 'value'):
            val = val.value
        if isinstance(val, (int, float)) and not np.isnan(val) and val > 0:
            b_values.append(float(val))
    
    b_values = np.array(b_values)
    print(f"有效磁场测量数: {len(b_values)}")
    if len(b_values) > 0:
        print(f"磁场范围: {b_values.min():.2e} - {b_values.max():.2e} T")
        print(f"磁场中值: {np.median(b_values):.2e} T")
        print(f"磁场均值: {np.mean(b_values):.2e} T")
        
        # 按磁场分组
        weak = b_values < 1e4
        intermediate = (b_values >= 1e4) & (b_values < 1e5)
        strong = b_values >= 1e5
        
        print()
        print("磁场分组:")
        print(f"  弱场 (<1e4 T): {np.sum(weak)} 颗 ({np.sum(weak)/len(b_values)*100:.1f}%)")
        print(f"  中场 (1e4-1e5 T): {np.sum(intermediate)} 颗 ({np.sum(intermediate)/len(b_values)*100:.1f}%)")
        print(f"  强场 (>1e5 T): {np.sum(strong)} 颗 ({np.sum(strong)/len(b_values)*100:.1f}%)")

print()
print("=" * 80)
print("分析完成")
print("=" * 80)
