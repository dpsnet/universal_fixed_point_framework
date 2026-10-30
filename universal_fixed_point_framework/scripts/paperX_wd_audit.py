# -*- coding: utf-8 -*-
"""P83 方法学审计：样本构成 + 口径一致性 + 选择性风险盘点"""
import json, numpy as np

base = 'E:/workspace/hyper-resolution/universal_fixed_point_framework'

# 1) 样本构成
with open(base + '/scripts/paperX_wd_m83c_sample_list.json', encoding='utf-8') as f:
    samples = json.load(f)
with open(base + '/scripts/paperX_wd_m83c_koester_ew.json', encoding='utf-8') as f:
    ko = json.load(f)
ko_s = ko['samples']
by_src = {}
for s in samples:
    by_src.setdefault(s['src'], []).append(s)
print('=== 样本构成（按来源）===')
for k, v in by_src.items():
    B = np.array([x['B_tesla'] for x in v])
    print(f'{k}: n={len(v)}  B: {B.min():.0f}-{B.max():.0f} T (log10B {np.log10(B).min():.1f}-{np.log10(B).max():.1f})')

# 2) 检测线筛选（有效残差 236 的构成）
S2 = [s for s in ko_s if s.get('koester_EW')]
det = [s for s in S2 if s.get('obs_EW', 0) > 0]
print(f'\n=== 筛选链 ===')
print(f'518 总样本 -> 有 Koester EW {len(S2)} -> obs_EW>0（检测到线）{len(det)} -> 残差有效（log10 可算）{sum(1 for s in det if s.get("koester_EW", 0) > 0)}')
no_det = [s for s in S2 if s.get('obs_EW', 0) <= 0]
print(f'未检测线样本: {len(no_det)}/{len(S2)}——B 分布: {[round(x["B_tesla"]) for x in no_det[:10]]}')
# 未检测样本的 B 分布 vs 检测样本
if no_det:
    Bn = np.array([x['B_tesla'] for x in no_det])
    Bd = np.array([x['B_tesla'] for x in det])
    print(f'未检测 B: log10 中位 {np.median(np.log10(Bn)):.2f}（范围 {np.log10(Bn).min():.1f}-{np.log10(Bn).max():.1f}）')
    print(f'已检测 B: log10 中位 {np.median(np.log10(Bd)):.2f}（范围 {np.log10(Bd).min():.1f}-{np.log10(Bd).max():.1f}）')

# 3) 口径：M83a 残差定义 vs M83c（从数据看）
# M83a 的 resid 字段在 v10 结果里——比对
with open(base + '/results/white_dwarf_analysis_v10_results.json', encoding='utf-8') as f:
    v10 = json.load(f)
r0 = v10['weak'][0]
print(f'\n=== 口径核对 ===')
print(f'v10 weak 样例: total_EW={r0["total_EW"]}, theo_EW={r0["theo_EW"]}, resid={r0["resid"]}, ratio={r0["ratio"]}')
# resid 定义推导
try:
    resid_calc = (float(r0['total_EW']) - float(r0['theo_EW'])) / float(r0['theo_EW'])
    print(f'残差候选定义 (obs-theo)/theo = {resid_calc:.4f} vs 存储 {r0["resid"]}')
except Exception as e:
    print('resid 计算失败', e)

# 4) Zeeman 排除检查——v10 有 Zeeman 诊断字段吗？
print(f'\nv10 记录字段: {list(r0.keys())}')
print(f'M83c 样本字段: {list(ko_s[0].keys())}')
