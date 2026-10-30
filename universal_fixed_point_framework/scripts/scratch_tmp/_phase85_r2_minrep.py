# -*- coding: utf-8 -*-
"""最小复现：直接调用 measure_continuum 看 D_B/slope"""
import os, sys
import numpy as np

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"
sys.path.insert(0, BASE)
sys.path.insert(0, r"E:\workspace\hyper-resolution\universal_fixed_point_framework\src\white_dwarf_analysis")

# 从 R2 脚本提取函数定义（避免重复 import 歧义）
exec(open(os.path.join(BASE, "_phase85_r2_continuum.py"), encoding="utf-8").read().split("# ---- 1) 观测侧")[0])

gid = "1003378611740398336"
d = np.load(os.path.join(BASE, "_desi_spec", gid + ".npz"), allow_pickle=True)
wl, fl, iv = d["wave"], d["flux"], d["ivar"]
m = measure_continuum(wl, fl, iv)
print("D_B:", m["D_B"])
print("slope:", m["slope"])
print("res:", m["res"])
print("snr:", m["snr_blue"], m["snr_red"])
