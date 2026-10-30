# -*- coding: utf-8 -*-
"""LAMOST 同样本化：B≥41 MG 子集的 B 分布 + 标准缺失（B-only，i=60° 默认，Teff=12000 近似）"""
import json, io, os, sys
import numpy as np
BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"
sys.path.insert(0, BASE)
sys.path.insert(0, r"E:\workspace\hyper-resolution\universal_fixed_point_framework\src\white_dwarf_analysis")
import white_dwarf_analysis_v10 as v10
import _phase104_osc1_v10_tmp as M  # 复用 components()——但注意 v10 的主循环会执行！用 __main__ 保护检查

# 读取 LAMOST 线级
p = os.path.join(BASE, "_gaia_abs", "paperX_lamost_linelevel_raw.json")
d = json.load(io.open(p, "r", encoding="utf-8"))
# 结构探查
def walk(x, path="", depth=0):
    if depth > 2:
        return
    if isinstance(x, dict):
        for k in list(x.keys())[:8]:
            print("  "*(depth+1) + k, type(x[k]).__name__)
            walk(x[k], path+"."+str(k), depth+1)
    elif isinstance(x, list):
        print("  "*(depth+1) + "[%d items]" % len(x))
        if x:
            walk(x[0], path+"[0]", depth+1)
walk(d)
