# -*- coding: utf-8 -*-
"""M83c：样本 Teff/logg 分布（确定检索范围）"""
import json, os

base = 'E:/workspace/hyper-resolution/universal_fixed_point_framework'
with open(base + '/results/white_dwarf_analysis_v10_results.json', encoding='utf-8') as f:
    v10 = json.load(f)
with open(base + '/results/white_dwarf_analysis_v11_gap_results.json', encoding='utf-8') as f:
    v11 = json.load(f)

def collect(d, key):
    out = []
    if isinstance(d, dict) and 'results' in d:
        d = d['results']
    if isinstance(d, dict):
        for v in d.values():
            if isinstance(v, list):
                for r in v:
                    if isinstance(r, dict) and key in r:
                        out.append(r)
            elif isinstance(v, dict) and key in v:
                out.append(v)
    elif isinstance(d, list):
        for r in d:
            if isinstance(r, dict) and key in r:
                out.append(r)
    return out

# v10 结构探测
print('v10 keys:', list(v10.keys())[:10])
print('v11 keys:', list(v11.keys())[:10])
# 探测一条记录
def first_rec(d):
    if isinstance(d, dict):
        for v in d.values():
            if isinstance(v, list) and v:
                return v[0]
            if isinstance(v, dict):
                r = first_rec(v)
                if r: return r
    return None
r = first_rec(v10)
print('v10 样例:', {k: str(v)[:60] for k, v in r.items()} if r else None)
