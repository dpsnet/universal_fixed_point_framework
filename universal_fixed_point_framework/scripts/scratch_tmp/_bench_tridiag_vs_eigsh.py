# -*- coding: utf-8 -*-
"""基准测试：eigsh（通用稀疏 Arnoldi） vs eigvalsh_tridiagonal（三对角专用）
同点 m=-13, dr=0.005 (N_r=24000), B=0.14921 —— 对比 E0 值与耗时。
用途：判断 m=-13 剩余 5 点能否换用三对角专用求解器加速。
"""
import time
import numpy as np
from scipy.linalg import eigvalsh_tridiagonal
from scipy.sparse import diags
from scipy.sparse.linalg import eigsh

N_r, r_max, m, B = 24000, 120.0, -13, 0.14921
dr = r_max / N_r
j = np.arange(N_r)
r = (j + 0.5) * dr
d = np.ones(N_r) / dr**2 + (m + 0.5 * B * r**2)**2 / (2.0 * r**2) - 1.0 / r
e = -np.ones(N_r - 1) / (2.0 * dr**2)

# --- eigsh（现用方法，含降级链）---
t0 = time.time()
E0_eigsh = None
for tol, maxiter in [(1e-9, 50000), (1e-8, 100000), (1e-7, 150000)]:
    try:
        vals, _ = eigsh(diags([e, d, e], offsets=[-1, 0, 1], format='csr').astype(np.float64),
                        k=min(12, N_r - 5), which='SA', maxiter=maxiter, tol=tol)
        E0_eigsh = float(np.real(vals[0]))
        break
    except Exception:
        continue
t1 = time.time()
print("eigsh:      E0 = %+.10f   耗时 %.2f s" % (E0_eigsh, t1 - t0), flush=True)

# --- eigvalsh_tridiagonal（三对角专用，只求最小特征值）---
t0 = time.time()
v = eigvalsh_tridiagonal(d, e, select='i', select_range=(0, 0))
t1 = time.time()
print("tridiag:    E0 = %+.10f   耗时 %.3f s" % (v[0], t1 - t0), flush=True)

if E0_eigsh is not None:
    diff = abs(E0_eigsh - v[0])
    print("偏差 |E0_eigsh - E0_trid| = %.3e（相对 %.3e）" % (diff, diff / abs(E0_eigsh)), flush=True)
