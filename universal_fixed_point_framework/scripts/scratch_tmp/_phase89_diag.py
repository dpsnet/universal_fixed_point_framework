# -*- coding: utf-8 -*-
"""M89-1 诊断：m=0 分波最低态（2D 库仑基态应 ≈ -2）+ 各分波束缚态计数"""
import numpy as np
from scipy.sparse import diags
from scipy.sparse.linalg import eigsh
import warnings
warnings.filterwarnings('ignore')

def hamiltonian_2d_hydrogen(N_r, r_max, m, B):
    dr = r_max / N_r
    j = np.arange(N_r)
    r = (j + 0.5) * dr
    off_diag = np.ones(N_r - 1) / (2.0 * dr ** 2)
    diag_main = np.ones(N_r) / dr ** 2
    landau_centrifugal = (m + 0.5 * B * r ** 2) ** 2 / (2.0 * r ** 2)
    coulomb = -1.0 / r
    H_mat = diags([-off_diag, diag_main + landau_centrifugal + coulomb, -off_diag],
                  offsets=[-1, 0, 1], shape=(N_r, N_r), format='csr')
    return H_mat, r

# 1) m=0, B=0 无场：基态应 ≈ -2（2D 库仑）
for N_r, r_max in ((1500, 60.0), (3000, 60.0), (1500, 80.0)):
    H, r = hamiltonian_2d_hydrogen(N_r, r_max, 0, 0.0)
    vals, _ = eigsh(H.astype(np.float64), k=8, which='SA', maxiter=50000, tol=1e-9)
    print("N_r=%d r_max=%.0f m=0 B=0 最低8态: %s" % (N_r, r_max, np.round(np.real(vals), 4)))

# 2) m=0..8 分波束缚态数（B=0.01, 0.2）——看哪些分波贡献
for B in (0.01, 0.2):
    print("\nB=%.3f 各分波束缚态数（N_r=1500, r_max=60）:" % B)
    tot = 0
    for m in range(-8, 9):
        H, r = hamiltonian_2d_hydrogen(1500, 60.0, m, B)
        try:
            vals, _ = eigsh(H.astype(np.float64), k=200, which='SA', maxiter=50000, tol=1e-9)
            vals = np.real(vals)
            nb = int(np.sum(vals < 0))
            emin = float(vals.min()) if len(vals) else None
            print("  m=%+3d: 束缚态=%3d E_min=%.4f" % (m, nb, emin))
            tot += nb
        except Exception as e:
            print("  m=%+3d: FAIL %s" % (m, e))
    print("  总束缚态 = %d" % tot)
