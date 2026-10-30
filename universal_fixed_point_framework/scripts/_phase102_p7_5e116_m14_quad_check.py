# -*- coding: utf-8 -*-
"""
P7-5e-116：m=−14 四阶差分确认（三次多项式形态的严格判别，用户指令：立即计算）
=============================================================================
任务：115 判别"二次段 = 三次多项式"的严格确认需 m=−14 四阶差分。
  若三阶差分继续恒定（d3(14)=+2.0e-5）→ 四阶差分 ≈ 0 → 三次多项式确认；
  若 d3(14) 偏离 → 四次项/更高阶存在。
先验（三次外推）：d1(14)_pred = d1(13)+d2(13)+d3(13) = 0.000652−0.000106+0.000020 = 0.000566
                → δ_pred(14) = δ(13)+0.000566 = 0.010516
判据：|d4(14)| = |d3(14)−d3(13)| < 3e-6 → 三次确认；否则更高阶。
"""
import time, json, os
import numpy as np
from scipy.linalg import eigvalsh_tridiagonal

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"
m = -14
closed = 14.0/2.0 + 1.0/7.0 + 1.0/(7.0*2.0**14)   # 7 + 1/7 + 1/114688
Bstar_closed = 1.0/closed
w = 0.0265
Bs = np.linspace(Bstar_closed*(1-w), Bstar_closed*(1+w), 7)
r_max = 120.0

def solve(N_r, B):
    dr = r_max / N_r
    j = np.arange(N_r)
    r = (j + 0.5) * dr
    d = np.ones(N_r) / dr**2 + (m + 0.5 * B * r**2)**2 / (2.0 * r**2) - 1.0 / r
    e = -np.ones(N_r - 1) / (2.0 * dr**2)
    return float(eigvalsh_tridiagonal(d, e, select='i', select_range=(0, 0))[0])

print("P7-5e-116：m=-14 三档全量（tridiag）+ 四阶差分确认", flush=True)
print("闭式 1/B* = %.10f、B*_closed = %.8f、窗口 ±2.65%% 7 点" % (closed, Bstar_closed), flush=True)

results = {}
for dr in [0.02, 0.01, 0.005]:
    N_r = int(round(r_max / dr))
    Es = np.array([solve(N_r, float(B)) for B in Bs])
    B0 = float(Bs[len(Bs)//2])
    X = Bs - B0
    A = np.vstack([np.ones_like(X), X, X**2, X**3]).T
    coef, _, _, _ = np.linalg.lstsq(A, Es, rcond=None)
    c0, c1, c2, c3 = coef
    x = -c0/c1
    for _ in range(6):
        e = c0 + c1*x + c2*x**2 + c3*x**3
        de = c1 + 2*c2*x + 3*c3*x**2
        x = x - e/de
    Bcross = B0 + x
    rms = float(np.sqrt(np.mean((A@coef-Es)**2)))
    results[dr] = {"Bstar": float(Bcross), "c1": float(c1), "c2": float(c2), "c3": float(c3), "rms": rms}
    print("dr=%.4f：c1=%+.9f c2=%+.9f c3=%+.9f  B*=%.8f  RMS=%.2e"
          % (dr, c1, c2, c3, Bcross, rms), flush=True)

B002, B001, B0005 = results[0.02]["Bstar"], results[0.01]["Bstar"], results[0.005]["Bstar"]
R2 = (4*B0005 - B001)/3.0
delta = abs(1.0/R2 - closed)
print("", flush=True)
print("Richardson 二阶（0.01/0.005）：B*(0) = %.8f   1/B* = %.8f   δ(14) = %.9f"
      % (R2, 1.0/R2, delta), flush=True)

# ---- 差分判别（读全链权威 δ 精确值 + 新 δ(14)）----
fc = json.load(open(os.path.join(BASE, "_phase102_p7_5e_fullchain_tridiag.json"), encoding="utf-8"))
deltas = {int(k): v for k, v in fc["deltas"].items()}
deltas[-14] = delta
for mm in [-9, -10, -11, -12, -13, -14]:
    print("  m=%+d  δ=%.9f" % (mm, deltas[mm]), flush=True)

d1_14 = deltas[-14] - deltas[-13]                       # 一阶差分 m=14
d1_13 = deltas[-13] - deltas[-12]
d2_14 = d1_14 - d1_13                                   # 二阶差分 m=14
d2_13 = deltas[-12] - 2*deltas[-13] + deltas[-14]       # 用前向一致性：d2(13)=d1(13)-d1(12)
d1_12 = deltas[-12] - deltas[-11]
d2_13_f = d1_13 - d1_12
d3_14 = d2_14 - d2_13_f                                 # 三阶差分 m=14
d3_13 = d2_13_f - (d1_12 - (deltas[-11]-deltas[-10]))   # 三阶差分 m=13
d4 = d3_14 - d3_13                                      # 四阶差分 m=14
print("", flush=True)
print("== 差分（前向定义）==", flush=True)
print("  d1(13)=%+.9f  d1(14)=%+.9f" % (d1_13, d1_14), flush=True)
print("  d2(13)=%+.9f  d2(14)=%+.9f" % (d2_13_f, d2_14), flush=True)
print("  d3(13)=%+.9f  d3(14)=%+.9f" % (d3_13, d3_14), flush=True)
print("  d4(14)=%+.9f" % d4, flush=True)
if abs(d4) < 3e-6:
    verdict = "★ 三次多项式确认（四阶差分≈0——三阶差分继续恒定）"
elif abs(d4) < 1.5e-5:
    verdict = "弱四次项（d4 同量级但显著）——近似三次+小四次"
else:
    verdict = "更高阶（四阶差分显著）——三次不够"
print("  判据 |d4|<3e-6 → %s" % verdict, flush=True)

# 先验对照：三次外推 δ_pred(14)
d1_14_pred = d1_13 + d2_13_f + d3_13
delta_pred = deltas[-13] + d1_14_pred
print("", flush=True)
print("== 三次外推先验对照 ==", flush=True)
print("  预测 d1(14)=%+.6f → δ_pred(14)=%.6f；实测 δ(14)=%.6f——偏差 %+.3f pct"
      % (d1_14_pred, delta_pred, delta, (delta-delta_pred)/delta_pred*100), flush=True)

json.dump({"Bstar_closed": Bstar_closed, "results": results,
           "R2_01_005": float(R2), "delta_14": float(delta),
           "d1_14": float(d1_14), "d2_14": float(d2_14), "d3_14": float(d3_14),
           "d4_14": float(d4), "verdict": verdict,
           "delta_pred_cubic": float(delta_pred)},
          open(os.path.join(BASE, "_phase102_p7_5e116_m14_3dr_tridiag.json"), "w", encoding="utf-8"), indent=1)
print("", flush=True)
print("JSON 落盘 OK exit 0", flush=True)
