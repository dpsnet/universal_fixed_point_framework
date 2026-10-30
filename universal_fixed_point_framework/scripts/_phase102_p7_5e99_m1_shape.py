# -*- coding: utf-8 -*-
"""
Phase 102 P7-5e-99：m=−1 过零动力学形状（斜率/曲率框架身份搜索）
================================================================
P7-5e-92：m=−6 的 E_0(B) B 域线性更优（RMS 1.75e-05）——1/B* 线性是零点定标律
m=−1 是"消失边界态"（独享 65 修正）——过零斜率/曲率是否也有框架身份？
E_0(B) ≈ c1·(B−B*) + c2·(B−B*)²——搜索 c1、c2 框架身份
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

# 框架量
sigma, k_max, N_gen, N_Weyl = 1.0/15.0, 8, 3, 4
alpha0 = N_Weyl / k_max  # 1/2
Np = k_max - N_gen       # 5
C2 = 4.0*np.log(10.0)    # 9.21034
dH = np.log(15.0)        # 2.70805
kl = 6.0/np.pi           # 1.90986
CF = 4.0/3.0

print("="*104)
print("P7-5e-99：m=−1 过零动力学形状（斜率/曲率框架身份搜索）")
print("="*104)

# 高精度网格
N_r, r_max = 6000, 120  # dr=0.02
Bstar_predict = 1.0/(5.0/7.0 + 1.0/65.0)  # 1.370492
Bs = np.linspace(1.28, 1.46, 19)
Es = []
for B in Bs:
    e = e0_m(N_r, r_max, -1, float(B))
    Es.append(e)
    print("  B=%.4f：E_0 = %+.7f" % (B, e), flush=True)

Es = np.array(Es)
# 找过零附近
idx0 = int(np.argmin(np.abs(Es)))
B0 = Bs[idx0]
# 拟合 E ≈ c0 + c1(B−B0) + c2(B−B0)² + c3(B−B0)³
X = Bs - B0
A = np.vstack([np.ones_like(X), X, X**2, X**3]).T
coef, res, rank, sv = np.linalg.lstsq(A, Es, rcond=None)
c0, c1, c2, c3 = coef
print("\n  ★ 过零附近 B0 = %.4f（E_0 = %+.7f）" % (B0, Es[idx0]))
print("  拟合 E ≈ c0 + c1·ΔB + c2·ΔB² + c3·ΔB³")
print("    c0 = %+.8f（应≈0）" % c0)
print("    c1 = %+.8f（斜率）" % c1)
print("    c2 = %+.8f（曲率）" % c2)
print("    c3 = %+.8f" % c3)
print("    RMS = %.3e" % np.sqrt(np.mean((A@coef - Es)**2)))

# 精确过零（线性插值到 E=0）
i = np.where(np.diff(np.sign(Es)) != 0)[0]
if len(i) > 0:
    i = i[0]
    B_cross = Bs[i] - Es[i]*(Bs[i+1]-Bs[i])/(Es[i+1]-Es[i])
    print("\n  线性插值精确过零 B* = %.7f——vs 闭式 1.370492——差 %+.5f%%"
          % (B_cross, (B_cross-Bstar_predict)/Bstar_predict*100))

# 框架身份搜索
print("\n★ c1、c2 框架身份搜索：")
cands = {
    "α₀": alpha0, "α₀²": alpha0**2, "N'": Np, "N'/2": Np/2.0,
    "k_max": k_max, "k_max²": k_max**2, "N_gen": N_gen, "N_gen²": N_gen**2,
    "σ": sigma, "2σ": 2*sigma, "3σ": 3*sigma, "k_max·α₀³": 1.0,
    "C²": C2, "C²/10": C2/10, "dH": dH, "dH/2": dH/2, "κΛ": 6.0/np.pi*16*np.log(10)*(dH+3),
    "1/65": 1.0/65.0, "5/7": 5.0/7.0, "3/40": 3.0/40.0, "1/14": 1.0/14.0,
    "N'_2·13": Np*13.0, "65": 65.0, "40": 40.0, "7": 7.0, "14": 14.0,
}
print("  c1 = %+.8f：" % c1)
hits1 = []
for name, v in cands.items():
    dev = (c1-v)/v*100 if v else 999
    if abs(dev) < 3:
        print("    ~ %s = %.8f（差 %+.4f%%）" % (name, v, dev))
        hits1.append((name, dev))
print("  c2 = %+.8f：" % c2)
hits2 = []
for name, v in cands.items():
    dev = (c2-v)/v*100 if v else 999
    if abs(dev) < 10:
        print("    ~ %s = %.8f（差 %+.4f%%）" % (name, v, dev))
        hits2.append((name, dev))
# 组合候选
print("  组合：")
combo = {"1/(2·c1)": 1.0/(2*c1), "1/c1": 1.0/c1, "1/c2": 1.0/c2 if c2 else 999,
         "2·c1·65": 2*c1*65, "c1·65": c1*65, "c2·65": c2*65 if c2 else 999}
for name, v in combo.items():
    print("    %s = %.6f" % (name, v))

json.dump({"Bstar_cross": float(B_cross) if (isinstance(i, np.ndarray) and len(i) > 0) else None,
           "c1": float(c1), "c2": float(c2), "c3": float(c3),
           "c1_hits": hits1, "c2_hits": hits2},
          open(os.path.join(BASE, "_phase102_p7_5e99_m1_shape.json"), "w", encoding="utf-8"), indent=1)
print("\nJSON 落盘 ✓  exit 0")
