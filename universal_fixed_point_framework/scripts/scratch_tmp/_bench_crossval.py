# -*- coding: utf-8 -*-
"""求解器正确性交叉验证：同一离散矩阵，eigsh vs tridiag
关键判别：同一 dr（同一矩阵）下两求解器应一致到机器精度；5e-7 偏差必有一方未解准。
测试点：m=-13
  A) N=6000  (dr=0.02)  eigsh vs tridiag —— 小矩阵 eigsh 应准
  B) N=24000 (dr=0.005) eigsh vs tridiag —— 大矩阵偏差源
  C) tridiag N=24000 vs N=48000 (dr=0.0025) —— tridiag 自身收敛 + 网格收敛
"""
import time
import numpy as np
from scipy.linalg import eigvalsh_tridiagonal
from scipy.sparse import diags
from scipy.sparse.linalg import eigsh

m, r_max, B = -13, 120.0, 0.14921

def build(N_r):
    dr = r_max / N_r
    j = np.arange(N_r)
    r = (j + 0.5) * dr
    d = np.ones(N_r) / dr**2 + (m + 0.5 * B * r**2)**2 / (2.0 * r**2) - 1.0 / r
    e = -np.ones(N_r - 1) / (2.0 * dr**2)
    return d, e, dr

def eigsh_e0(d, e, N_r):
    t0 = time.time()
    A = diags([e, d, e], offsets=[-1, 0, 1], format='csr').astype(np.float64)
    for tol, maxiter in [(1e-9, 50000), (1e-8, 100000), (1e-7, 150000)]:
        try:
            vals, _ = eigsh(A, k=min(12, N_r - 5), which='SA', maxiter=maxiter, tol=tol)
            return float(np.real(vals[0])), time.time() - t0
        except Exception:
            continue
    raise RuntimeError("eigsh fail")

# A) 小矩阵
d, e, dr = build(6000)
v = eigvalsh_tridiagonal(d, e, select='i', select_range=(0, 0))[0]
eg, tg = eigsh_e0(d, e, 6000)
print("A) N=6000  (dr=0.02):  tridiag %+.10f  eigsh %+.10f  偏差 %.3e  (eigsh %.1fs)"
      % (v, eg, abs(eg - v), tg), flush=True)

# B) 大矩阵（与已跑基准一致）
d, e, dr = build(24000)
v = eigvalsh_tridiagonal(d, e, select='i', select_range=(0, 0))[0]
print("B) N=24000 (dr=0.005): tridiag %+.10f（参考 eigsh -0.0010666016，偏差 5.0e-7）" % v, flush=True)

# C) tridiag 自收敛（dr=0.0025, N=48000）
d, e, dr = build(48000)
v2 = eigvalsh_tridiagonal(d, e, select='i', select_range=(0, 0))[0]
print("C) tridiag: N=48000 (dr=0.0025) %+.10f  vs N=24000 (dr=0.005) %+.10f  网格漂移 %.3e"
      % (v2, v, abs(v2 - v)), flush=True)
print("判别：若 A 两求解器一致(<=1e-11)而 B 差 5e-7 → eigsh 在大矩阵未解准，tridiag 为权威", flush=True)
