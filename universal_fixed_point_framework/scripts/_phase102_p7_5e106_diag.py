# -*- coding: utf-8 -*-
"""P7-5e-106 诊断：m=−5 在 dr=0.0025（N_r=48000）的 eigsh 收敛测试"""
import numpy as np
from scipy.sparse import diags
from scipy.sparse.linalg import eigsh
import warnings, time
warnings.filterwarnings('ignore')

def e0_m(N_r, r_max, m, B, k=12, tol=1e-9, maxiter=50000):
    dr = r_max / N_r
    j = np.arange(N_r)
    r = (j + 0.5) * dr
    off_diag = np.ones(N_r - 1) / (2.0 * dr ** 2)
    diag_main = np.ones(N_r) / dr ** 2
    landau_centrifugal = (m + 0.5 * B * r ** 2) ** 2 / (2.0 * r ** 2)
    coulomb = -1.0 / r
    H = diags([-off_diag, diag_main + landau_centrifugal + coulomb, -off_diag],
              offsets=[-1, 0, 1], shape=(N_r, N_r), format='csr')
    t0 = time.time()
    vals, _ = eigsh(H.astype(np.float64), k=min(k, N_r - 5), which='SA',
                    maxiter=maxiter, tol=tol)
    print("  B=%.4f：E0 = %.10f、耗时 %.1fs" % (B, float(np.real(vals[0])), time.time()-t0), flush=True)
    return float(np.real(vals[0]))

for B in [0.368, 0.378, 0.388]:
    try:
        e0_m(48000, 120.0, -5, B, tol=1e-9, maxiter=50000)
    except Exception as e:
        print("  B=%.4f 失败：%s——尝试 tol=1e-8 maxiter=100000" % (B, e), flush=True)
        try:
            e0_m(48000, 120.0, -5, B, tol=1e-8, maxiter=100000)
        except Exception as e2:
            print("  B=%.4f 再次失败：%s" % (B, e2), flush=True)
