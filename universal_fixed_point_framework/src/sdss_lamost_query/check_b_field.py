"""检查 B 字段的实际值格式"""
import numpy as np
from astroquery.vizier import Vizier
import warnings
warnings.filterwarnings('ignore')

Vizier.ROW_LIMIT = 1000
result = Vizier.get_catalogs('J/ApJ/944/56')
table = result[0]

print("B 字段前 20 个值:")
for i in range(20):
    val = table['B'][i]
    print(f"  [{i}] type={type(val).__name__}, value={val}, repr={repr(val)}")

print()
print("B 字段统计:")
b_vals = table['B']
print(f"  dtype: {b_vals.dtype}")
print(f"  min: {np.nanmin(b_vals)}")
print(f"  max: {np.nanmax(b_vals)}")
print(f"  mean: {np.nanmean(b_vals)}")
print(f"  非零数: {np.sum(b_vals > 0)}")
print(f"  零数: {np.sum(b_vals == 0)}")
print(f"  NaN数: {np.sum(np.isnan(b_vals))}")

print()
print("e_B 字段前 20 个值:")
for i in range(20):
    val = table['e_B'][i]
    print(f"  [{i}] type={type(val).__name__}, value={val}")

print()
print("sp 字段值分布:")
sp_vals = table['sp']
unique, counts = np.unique(sp_vals, return_counts=True)
for u, c in zip(unique, counts):
    print(f"  {u}: {c}")

print()
print("Teff 字段统计:")
teff_vals = table['Teff']
print(f"  非零数: {np.sum(teff_vals > 0)}")
print(f"  范围: {np.min(teff_vals[teff_vals>0])} - {np.max(teff_vals[teff_vals>0])} K")
