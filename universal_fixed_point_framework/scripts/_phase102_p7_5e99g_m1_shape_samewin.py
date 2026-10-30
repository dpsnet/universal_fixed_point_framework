# -*- coding: utf-8 -*-
"""
Phase 102 P7-5e-99g：m=−1 过零形状同窗口 dr 定案
================================================================
固定 B 采样点（同一物理窗口），只变网格 dr——纯网格收敛判别
B = [1.34, 1.40] 步长 0.01（7 点，过零 1.3705 居中 ±0.03）
dr ∈ {0.02, 0.01, 0.005, 0.0025}
判别：c1(0) vs 15/49 = 0.3061224；c2(0) vs (9−1/65)/200 = 0.044923077
"""
import json, os
import numpy as np
from scipy.sparse import diags
from scipy.sparse.linalg import eigsh
import warnings
warnings.filterwarnings('ignore')

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"

def e0_m(N_r, r_max, m, B, k=12):
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
print("P7-5e-99g：m=−1 同窗口 dr 定案（B=[1.34,1.40] 7 点）")
print("="*104)

Bs = np.linspace(1.34, 1.40, 7)
results = {}
for N_r, label in [(6000, "dr=0.02"), (12000, "dr=0.01"), (24000, "dr=0.005"), (48000, "dr=0.0025")]:
    Es = np.array([e0_m(N_r, 120, -1, float(B)) for B in Bs])
    idx0 = int(np.argmin(np.abs(Es)))
    B0 = Bs[idx0]
    X = Bs - B0
    A = np.vstack([np.ones_like(X), X, X**2, X**3]).T
    coef, _, _, _ = np.linalg.lstsq(A, Es, rcond=None)
    c0, c1, c2, c3 = coef
    # 三阶 Newton 反解 B*
    i_arr = np.where(np.diff(np.sign(Es)) != 0)[0]
    B_cross = None
    if len(i_arr) > 0:
        i0 = int(i_arr[0])
        Bn = Bs[i0] - Es[i0]*(Bs[i0+1]-Bs[i0])/(Es[i0+1]-Es[i0])
        for _ in range(5):
            x = Bn - B0
            e = c0 + c1*x + c2*x**2 + c3*x**3
            de = c1 + 2*c2*x + 3*c3*x**2
            Bn = Bn - e/de
        B_cross = Bn
    results[label] = {"c1": float(c1), "c2": float(c2), "c3": float(c3), "Bstar": B_cross}
    print("  %s：c1 = %+.8f、c2 = %+.8f、c3 = %+.8f、B* = %.7f、RMS = %.3e"
          % (label, c1, c2, c3, B_cross, np.sqrt(np.mean((A@coef-Es)**2))), flush=True)

# Richardson 二阶外推（c(dr) = c(0) + a·dr²）用最后两个 dr
def rich(c_hi, c_lo, dr_hi, dr_lo):
    # c(dr_lo) = c0 + a dr_lo^2 ; c(dr_hi) = c0 + a dr_hi^2
    a = (c_lo - c_hi) / (dr_lo**2 - dr_hi**2)
    return c_lo - a * dr_lo**2

c1_005, c1_0025 = results["dr=0.005"]["c1"], results["dr=0.0025"]["c1"]
c2_005, c2_0025 = results["dr=0.005"]["c2"], results["dr=0.0025"]["c2"]
c1_0 = rich(results["dr=0.01"]["c1"], c1_005, 0.01, 0.005)
c2_0 = rich(results["dr=0.01"]["c2"], c2_005, 0.01, 0.005)
c1_0b = rich(c1_005, c1_0025, 0.005, 0.0025)
c2_0b = rich(c2_005, c2_0025, 0.005, 0.0025)
B_0 = rich(results["dr=0.01"]["Bstar"], results["dr=0.005"]["Bstar"], 0.01, 0.005)
B_0b = rich(results["dr=0.005"]["Bstar"], results["dr=0.0025"]["Bstar"], 0.005, 0.0025)

print("\n★ Richardson 外推（二阶，dr→0）：")
print("  c1(0) = %.8f（用 0.01/0.005）——%.8f（用 0.005/0.0025）" % (c1_0, c1_0b))
print("  c2(0) = %.8f（用 0.01/0.005）——%.8f（用 0.005/0.0025）" % (c2_0, c2_0b))
print("  B*(0) = %.8f（用 0.01/0.005）——%.8f（用 0.005/0.0025）" % (B_0, B_0b))

print("\n★ 定案判别：")
print("  c1(0) 平均 = %.8f——vs 15/49 = 0.306122449：差 %+.6f%%" % ((c1_0+c1_0b)/2, ((c1_0+c1_0b)/2-15.0/49.0)/(15.0/49.0)*100))
print("  c2(0) 平均 = %.8f——vs (9−1/65)/200 = 0.044923077：差 %+.6f%%" % ((c2_0+c2_0b)/2, ((c2_0+c2_0b)/2-(9-1.0/65.0)/200.0)/((9-1.0/65.0)/200.0)*100))
print("  c2(0) 平均 = %.8f——vs 9/200 = 0.045：差 %+.6f%%" % ((c2_0+c2_0b)/2, ((c2_0+c2_0b)/2-0.045)/0.045*100))
print("  B*(0) 平均 = %.8f——vs 闭式 1.3704922：差 %+.6f%%" % ((B_0+B_0b)/2, ((B_0+B_0b)/2-1.3704922)/1.3704922*100))
print("  c3 序列：", "、".join("%.8f" % results[k]["c3"] for k in ["dr=0.02","dr=0.01","dr=0.005","dr=0.0025"]))

json.dump(results, open(os.path.join(BASE, "_phase102_p7_5e99g_m1_shape_samewin.json"), "w", encoding="utf-8"), indent=1)
print("\nJSON 落盘 ✓  exit 0")
