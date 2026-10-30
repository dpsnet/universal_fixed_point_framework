# -*- coding: utf-8 -*-
"""
Phase 102 P7-5e-92：E_0(B) 过零形状判别——1/B 域线性的物理来源
================================================================
统一闭式 1/B* = |m|/2 + 1/7 + 1/(7·2^|m|)——1/B* 线性结构的机制判别：
  若 E_0 ∝ (1/B − 1/B*)（1/B 域线性）→ 过零闭式的线性是"1/B 域结构"的内生结果
  若 E_0 ∝ (B − B*)（B 域线性）→ 1/B* 线性为巧合/高阶近似
测：m=-6（最精确点 0.02%）在 B*≈0.318 附近的 E_0(B) 曲线——两种域回归比较残差
"""
import json, os
import numpy as np
from scipy.sparse import diags
from scipy.sparse.linalg import eigsh
import warnings
warnings.filterwarnings('ignore')

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"

def e0_m(N_r, r_max, m, B, k=20):
    dr = r_max / N_r
    j = np.arange(N_r)
    r = (j + 0.5) * dr
    off_diag = np.ones(N_r - 1) / (2.0 * dr ** 2)
    diag_main = np.ones(N_r) / dr ** 2
    landau_centrifugal = (m + 0.5 * B * r ** 2) ** 2 / (2.0 * r ** 2)
    coulomb = -1.0 / r
    H = diags([-off_diag, diag_main + landau_centrifugal + coulomb, -off_diag],
              offsets=[-1, 0, 1], shape=(N_r, N_r), format='csr')
    try:
        vals, _ = eigsh(H.astype(np.float64), k=min(k, N_r - 5),
                        which='SA', maxiter=50000, tol=1e-9)
        return float(np.real(vals[0]))
    except Exception:
        return None

print("="*104)
print("P7-5e-92：E_0(B) 过零形状判别——m=-6（B*≈0.318）")
print("="*104)

m = -6
Bstar = 0.31825
Bs = [0.30, 0.305, 0.31, 0.315, 0.31825, 0.322, 0.328, 0.335, 0.345]
E = []
for B in Bs:
    e = e0_m(1500, 80, m, B)
    E.append(e)
    print("  B=%.5f: E_0 = %+.6f" % (B, e), flush=True)

# 两种域回归（过零附近 5 点 0.305-0.335）
idx = [1, 2, 3, 4, 5, 6, 7]  # 0.305..0.335
Bs_r, Es_r = np.array(Bs)[idx], np.array(E)[idx]
# 线性回归 y = a*x + b 残差（残差平方和 / 点数）
def linfit(x, y):
    A = np.vstack([x, np.ones_like(x)]).T
    coef, res, _, _ = np.linalg.lstsq(A, y, rcond=None)
    pred = A @ coef
    rms = np.sqrt(np.mean((y - pred)**2))
    return coef, rms

cB, rmsB = linfit(Bs_r, Es_r)
cI, rmsI = linfit(1.0/Bs_r, Es_r)
print()
print("B 域线性回归 E = a·B+b：a=%+.4f——RMS 残差 %.2e" % (cB[0], rmsB))
print("1/B 域线性回归 E = a·(1/B)+b：a=%+.4f——RMS 残差 %.2e" % (cI[0], rmsI))
print("判别：%s" % ("1/B 域线性更优（过零闭式线性 = 1/B 域结构内生）" if rmsI < rmsB*0.5 else
      "B 域线性相当（1/B* 线性为近似/巧合）" if rmsB <= rmsI else "1/B 域线性略优（倾向内生）"))

json.dump({"m": m, "Bs": Bs, "E": E, "rms_B_domain": rmsB, "rms_1B_domain": rmsI},
          open(os.path.join(BASE, "_phase102_p7_5e92_E0_shape.json"), "w", encoding="utf-8"), indent=1)
print("JSON 落盘 ✓  exit 0")
