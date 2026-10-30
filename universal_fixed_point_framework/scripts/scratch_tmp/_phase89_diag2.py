# -*- coding: utf-8 -*-
"""诊断 2：无场 2D 氢原子基态校验（应 ≈ -2.0）+ 加磁场的基态变化"""
import numpy as np
from scipy.sparse import diags
from scipy.sparse.linalg import eigsh
import warnings
warnings.filterwarnings('ignore')

def ham2d(N_r, r_max, m, B, use_correct_centrifugal=False):
    """B=0 时标准 2D 径向方程：-1/2 u'' + (m^2-1/4)/(2r^2) - 1/r（含 -1/4 修正）
    论文版：(m+B r^2/2)^2/(2r^2) 展开 = m^2/(2r^2) + mB/2 + B^2 r^2/8（缺 -1/8r^2）"""
    dr = r_max / N_r
    j = np.arange(N_r)
    r = (j + 0.5) * dr
    off_diag = np.ones(N_r - 1) / (2.0 * dr ** 2)
    diag_main = np.ones(N_r) / dr ** 2
    if use_correct_centrifugal:
        cent = ((m ** 2 - 0.25) / (2.0 * r ** 2)) + (m * B / 2.0) + (B ** 2 * r ** 2 / 8.0)
    else:
        cent = (m + 0.5 * B * r ** 2) ** 2 / (2.0 * r ** 2)
    coulomb = -1.0 / r
    H_mat = diags([-off_diag, diag_main + cent + coulomb, -off_diag],
                  offsets=[-1, 0, 1], shape=(N_r, N_r), format='csr')
    return H_mat

print("== 无场 B=0, m=0 基态（标准 2D 氢原子应 ≈ -2.0）==")
for N_r, r_max in ((750, 60.0), (1500, 60.0), (3000, 60.0)):
    for cflag, tag in ((False, "论文版(m^2)"), (True, "标准版(m^2-1/4)")):
        H = ham2d(N_r, r_max, 0, 0.0, cflag)
        try:
            vals, _ = eigsh(H.astype(np.float64), k=4, which='SA', maxiter=100000, tol=1e-10)
            print("  N_r=%4d %s: %s" % (N_r, tag, np.round(np.real(vals), 4)))
        except Exception as e:
            print("  N_r=%4d %s: FAIL %s" % (N_r, tag, e))

print("\n== 论文版 vs 标准版基态随 B（m=0, N_r=1500）==")
for B in (0.0, 0.01, 0.05, 0.1, 0.2):
    row = []
    for cflag in (False, True):
        H = ham2d(1500, 60.0, 0, B, cflag)
        try:
            vals, _ = eigsh(H.astype(np.float64), k=2, which='SA', maxiter=100000, tol=1e-10)
            row.append(round(float(np.real(vals)[0]), 4))
        except Exception as e:
            row.append(None)
    print("  B=%.2f: 论文版基态=%s 标准版基态=%s" % (B, row[0], row[1]))
