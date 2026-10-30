# -*- coding: utf-8 -*-
"""
P7-5e-118：m=−33..−128 大规模外推（双曲渐近持续/变换判别）
================================================================
先验（计算前登记，117b 双曲模型）：δ(m) = 0.017895 − 0.103317/m（13..32 拟合）
  δ_pred(33)=0.014764  δ_pred(64)=0.016281  δ_pred(96)=0.016819  δ_pred(128)=0.017088
判据：|偏差| < 1% → 双曲持续；1–5% → 弱变换（1/m² 等高阶项）；>5% → 形态变换。
r_max 规则（118 校验）：r_max = max(120, 4|m|)——m=128 时 512 与 1024/1536 差 ~1e-11。
"""
import time, json, os
import numpy as np
from scipy.linalg import eigvalsh_tridiagonal

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"
w = 0.0265
drs = [0.02, 0.01]   # 118c 收敛诊断：dr≤0.005（N_r≥102400）dstemr 噪声 ~5e-7 污染 Richardson → 只用干净档
D_INF, C_HYP = 0.017895, 0.103317   # 117b 双曲拟合（m≥15 两参数）

def closed_1B(m):
    return abs(m)/2.0 + 1.0/7.0 + 1.0/(7.0*2.0**abs(m))

def solve(N_r, r_max, B, m):
    dr = r_max / N_r
    j = np.arange(N_r)
    r = (j + 0.5) * dr
    d = np.ones(N_r) / dr**2 + (m + 0.5 * B * r**2)**2 / (2.0 * r**2) - 1.0 / r
    e = -np.ones(N_r - 1) / (2.0 * dr**2)
    return float(eigvalsh_tridiagonal(d, e, select='i', select_range=(0, 0))[0])

def Bstar_3dr(m, r_max):
    cl = closed_1B(m); Bc = 1.0/cl
    Bs = np.linspace(Bc*(1-w), Bc*(1+w), 7)
    res = {}
    for dr in drs:
        N_r = int(round(r_max / dr))
        Es = np.array([solve(N_r, r_max, float(B), m) for B in Bs])
        B0 = float(Bs[3]); X = Bs - B0
        A = np.vstack([np.ones_like(X), X, X**2, X**3]).T
        coef, _, _, _ = np.linalg.lstsq(A, Es, rcond=None)
        c0, c1, c2, c3 = coef
        x = -c0/c1
        for _ in range(6):
            x = x - (c0+c1*x+c2*x**2+c3*x**3)/(c1+2*c2*x+3*c3*x**2)
        res[dr] = {"Bstar": float(B0 + x),
                   "rms": float(np.sqrt(np.mean((A@coef-Es)**2)))}
    R2 = (4*res[0.01]["Bstar"] - res[0.02]["Bstar"])/3.0   # 干净档 Richardson 二阶（118c 诊断确认）
    return R2, abs(1.0/R2 - cl), res

print("P7-5e-118：m=−33..−128 批量外推（r_max=4|m|，三档×7点）", flush=True)
print("先验（双曲 δ=%.6f−%.6f/m）：δ_pred(33)=%.6f  (64)=%.6f  (96)=%.6f  (128)=%.6f"
      % (D_INF, C_HYP, D_INF-C_HYP/33, D_INF-C_HYP/64, D_INF-C_HYP/96, D_INF-C_HYP/128), flush=True)

out = {}
t0 = time.time()
for m in range(-33, -129, -1):
    r_max = max(120.0, 4.0*abs(m))
    cl = closed_1B(m)
    B0v, delta, res = Bstar_3dr(m, r_max)
    pred = D_INF - C_HYP/abs(m)
    dev = (delta-pred)/pred*100
    out[m] = {"closed_1B": cl, "Bstar0": float(B0v), "delta": float(delta),
              "pred_hyper": pred, "dev_pct": dev, "r_max": r_max, "res": res}
    tag = "★持续" if abs(dev) < 1.0 else ("弱变换" if abs(dev) < 5.0 else "★★变换")
    print("m=%4d  r_max=%.0f  1/B*=%.6f  δ=%.7f  双曲预测=%.6f  偏差=%+.2f pct  %s"
          % (m, r_max, cl+delta, delta, pred, dev, tag), flush=True)
dt = time.time()-t0

# 精化：33..128 两参数/三参数拟合
print("", flush=True)
print("== 双曲精化（33..128，%d 点，总耗时 %.0f s）==" % (128-32, dt), flush=True)
ms = np.arange(33, 129, dtype=float)
ds = np.array([out[m]["delta"] for m in range(-33, -129, -1)])
X2 = np.vstack([np.ones(len(ms)), 1.0/ms]).T
c2f, _, _, _ = np.linalg.lstsq(X2, ds, rcond=None)
rms2 = float(np.sqrt(np.mean((X2@c2f-ds)**2)))
print("  两参数（m≥33）：δ∞=%.6f  C=%.6f  RMS=%.2e" % (c2f[0], c2f[1], rms2), flush=True)
X3 = np.vstack([np.ones(len(ms)), 1.0/ms, 1.0/ms**2]).T
c3f, _, _, _ = np.linalg.lstsq(X3, ds, rcond=None)
rms3 = float(np.sqrt(np.mean((X3@c3f-ds)**2)))
print("  三参数（m≥33）：δ∞=%.6f  C=%.6f  D=%.6f  RMS=%.2e" % (c3f[0], c3f[1], c3f[2], rms3), flush=True)
print("  δ∞ vs 1/56=%.8f：两参 %+.3f pct、三参 %+.3f pct" % (
    1/56.0, (c2f[0]-1/56.0)/(1/56.0)*100, (c3f[0]-1/56.0)/(1/56.0)*100), flush=True)
print("  全局（13..128）：δ∞ vs 1/56 联合检验——两参 δ∞=%.6f（%+.3f pct）" % (
    c2f[0], (c2f[0]-1/56.0)/(1/56.0)*100), flush=True)

# 判别汇总
devs = np.array([abs(out[m]["dev_pct"]) for m in range(-33, -129, -1)])
n_ok = int(np.sum(devs < 1.0))
print("", flush=True)
print("判别：偏差<1%% 点数 = %d/96——%s" % (n_ok,
    "★★★ 双曲渐近持续至 m=128（形态稳定，无变换）" if n_ok >= 92 else
    ("弱变换（部分点超 1%%——1/m² 项候选）" if n_ok >= 70 else "★★ 形态变换（双曲在更大 m 失效）")), flush=True)

json.dump({"D_INF": D_INF, "C_HYP": C_HYP, "out": {str(k): v for k, v in out.items()},
           "fit_2p": {"d_inf": float(c2f[0]), "C": float(c2f[1]), "rms": rms2},
           "fit_3p": {"d_inf": float(c3f[0]), "C": float(c3f[1]), "D": float(c3f[2]), "rms": rms3},
           "runtime_s": dt, "n_ok_1pct": n_ok},
          open(os.path.join(BASE, "_phase102_p7_5e118_m128_scan.json"), "w", encoding="utf-8"),
          indent=1, ensure_ascii=False)
print("", flush=True)
print("JSON 落盘 OK exit 0", flush=True)
