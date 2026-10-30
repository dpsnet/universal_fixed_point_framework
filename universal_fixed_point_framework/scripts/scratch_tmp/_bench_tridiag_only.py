# -*- coding: utf-8 -*-
"""纯三对角求解器基准：m=-13, dr=0.005 (N_r=24000)
对比已完成 2 点的 eigsh 值（p114_out.txt 实测）——验证数值一致性与加速倍数。
eigsh 参考值：B=0.14655 -> -0.0010666016；B=0.14788 -> -0.0007317494
"""
import time
import numpy as np
from scipy.linalg import eigvalsh_tridiagonal

N_r, r_max, m = 24000, 120.0, -13
dr = r_max / N_r
j = np.arange(N_r)
r = (j + 0.5) * dr

ref = {0.14655: -0.0010666016, 0.14788: -0.0007317494}
for B, e_ref in ref.items():
    d = np.ones(N_r) / dr**2 + (m + 0.5 * B * r**2)**2 / (2.0 * r**2) - 1.0 / r
    e = -np.ones(N_r - 1) / (2.0 * dr**2)
    t0 = time.time()
    v = eigvalsh_tridiagonal(d, e, select='i', select_range=(0, 0))
    dt = time.time() - t0
    diff = abs(v[0] - e_ref)
    print("B=%.5f: E0_trid = %+.10f  vs eigsh %+.10f  偏差 %.3e  耗时 %.3f s"
          % (B, v[0], e_ref, diff, dt), flush=True)
print("基准完成：eigsh 单点 20-28 min vs 三对角秒级", flush=True)
