# -*- coding: utf-8 -*-
"""M83c 步骤1：汇总样本 Teff/logg 分布 + 网格点匹配"""
import json, os

base = 'E:/workspace/hyper-resolution/universal_fixed_point_framework'

with open(base + '/results/white_dwarf_analysis_v10_results.json', encoding='utf-8') as f:
    v10 = json.load(f)
with open(base + '/results/white_dwarf_analysis_v11_gap_results.json', encoding='utf-8') as f:
    v11 = json.load(f)

samples = []
# v10
for grp in ['int', 'weak']:
    for r in v10[grp]:
        if r['Teff'] is None or r['log_g'] is None:
            continue
        samples.append({'name': r['name'], 'B_tesla': float(r['B_tesla']),
                        'Teff': float(r['Teff']), 'logg': float(r['log_g']),
                        'obs_EW': float(r['total_EW']), 'src': 'v10_' + grp})
# v11
for r in v11['results']:
    if r['Teff'] is None or r['log_g'] is None:
        continue
    samples.append({'name': r['name'], 'B_tesla': float(r['B_tesla']),
                    'Teff': float(r['Teff']), 'logg': float(r['log_g']),
                    'obs_EW': float(r['total_EW']), 'src': 'v11_gap'})

print(f'总样本: {len(samples)}')
teffs = sorted(s['Teff'] for s in samples)
loggs = sorted(s['logg'] for s in samples)
print(f'Teff: {teffs[0]:.0f} - {teffs[-1]:.0f} K（中位 {teffs[len(teffs)//2]:.0f}）')
print(f'logg: {loggs[0]:.2f} - {loggs[-1]:.2f}（中位 {loggs[len(loggs)//2]:.2f}）')
import numpy as np
B = np.array([s['B_tesla'] for s in samples])
print(f'B: min {B.min():.1f} max {B.max():.1f} T（log10B: {np.log10(B).min():.1f} - {np.log10(B).max():.1f}）')

# Koester 网格步长假设（Teff 250K、logg 0.25）——最近点匹配
def nearest_grid(teff, logg):
    teff_g = round(teff / 250) * 250
    logg_g = round(logg / 0.25) * 0.25
    return teff_g, logg_g

grid_points = set()
for s in samples:
    t, g = nearest_grid(s['Teff'], s['logg'])
    grid_points.add((t, g))
print(f'唯一网格点: {len(grid_points)}')
print(f'Teff 网格范围: {min(t for t, g in grid_points)} - {max(t for t, g in grid_points)}')
print(f'logg 网格范围: {min(g for t, g in grid_points):.2f} - {max(g for t, g in grid_points):.2f}')

# 保存样本 + 网格点
out = {'n_samples': len(samples), 'teff_range': [teffs[0], teffs[-1]], 'logg_range': [loggs[0], loggs[-1]],
       'n_grid_points': len(grid_points), 'grid_points': sorted(grid_points)}
with open(base + '/scripts/paperX_wd_m83c_samples.json', 'w', encoding='utf-8') as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
with open(base + '/scripts/paperX_wd_m83c_sample_list.json', 'w', encoding='utf-8') as f:
    json.dump(samples, f, ensure_ascii=False)
print('\nDONE')
