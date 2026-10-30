# -*- coding: utf-8 -*-
"""P7-5e 全链 tridiag 重算验证（m=−1..−14）
用三对角专用求解器（scipy.linalg.eigvalsh_tridiagonal，LAPACK 直接法）统一重算全部历史点：
三档 dr={0.02,0.01,0.005} × 7 点窗口 ±2.65% → 三次拟合 B*(dr) → Richardson 二阶 → δ(1/B)
与历史定案（判别脚本硬编码，eigsh 版）逐点对比。
判别：① 全链复现（偏差<容差）② 分层结构保持（均匀带/线性段/二次段）。
"""
import time, json, os
import numpy as np
from scipy.linalg import eigvalsh_tridiagonal

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"

# 历史定案 δ(1/B)（1/B 域失调，判别脚本 _phase102_p7_5e113_discern.py 硬编码 + m=-13 新增）
hist_delta = {
    -1: 0.0, -2: 0.000197, -3: 0.000349, -4: 0.000438, -5: 0.001354,
    -6: 0.002685, -7: 0.004106, -8: 0.005439, -9: 0.006626,
    -10: 0.007656, -11: 0.008540, -12: 0.009298, -13: 0.009950}
# m=-14 为新判别点（P7-5e-116 首次登记，无历史）——走"新点"分支
new_points = {-14}

r_max = 120.0
w = 0.0265
drs = [0.02, 0.01, 0.005]

def closed_1B(m):
    v = abs(m)/2.0 + 1.0/7.0 + 1.0/(7.0*2.0**abs(m))
    if m == -1:
        v += 1.0/65.0
    return v

def solve(N_r, B, m):
    dr = r_max / N_r
    j = np.arange(N_r)
    r = (j + 0.5) * dr
    d = np.ones(N_r) / dr**2 + (m + 0.5 * B * r**2)**2 / (2.0 * r**2) - 1.0 / r
    e = -np.ones(N_r - 1) / (2.0 * dr**2)
    return float(eigvalsh_tridiagonal(d, e, select='i', select_range=(0, 0))[0])

def Bstar_fit(Bs, Es):
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
    return Bcross, (c0, c1, c2, c3), rms

print("P7-5e 全链 tridiag 重算验证（m=−1..−14，三档×7点，窗口 ±2.65%）", flush=True)
t_start = time.time()
out = {}
for m in range(-1, -15, -1):
    cl = closed_1B(m)
    Bc = 1.0/cl
    Bs = np.linspace(Bc*(1-w), Bc*(1+w), 7)
    res_dr = {}
    for dr in drs:
        N_r = int(round(r_max / dr))
        Es = np.array([solve(N_r, float(B), m) for B in Bs])
        Bcross, (c0, c1, c2, c3), rms = Bstar_fit(Bs, Es)
        res_dr[dr] = {"Bstar": Bcross, "c1": float(c1), "c2": float(c2),
                      "c3": float(c3), "rms": rms}
    B002, B001, B0005 = res_dr[0.02]["Bstar"], res_dr[0.01]["Bstar"], res_dr[0.005]["Bstar"]
    R2 = (4*B0005 - B001)/3.0
    invB0 = 1.0/R2
    delta = abs(invB0 - cl)
    hist = hist_delta.get(m, 0.0)
    if m in new_points:
        dev_txt = "新点首次登记（P7-5e-116）"
    elif abs(hist) < 1e-12:
        dev = None if delta < 2e-6 else (delta/hist if hist else float('inf'))
        dev_txt = "δ≈0（65 修正精确点）——新 δ=%.2e %s" % (delta, "OK" if delta < 2e-6 else "!! 偏离")
    else:
        dev = (delta - hist)/hist*100
        dev_txt = "%+.3f pct" % dev
    out[m] = {"closed_1B": cl, "Bc": Bc, "dr": res_dr, "R2": float(R2),
              "invB0": float(invB0), "delta": float(delta),
              "hist_delta": hist, "dev_pct": None if m in new_points else dev}
    print("m=%3d  闭式 1/B*=% .8f  B*(0)=%.8f  1/B*(0)=% .8f  δ=% .6f  历史=%s  → %s"
          % (m, cl, R2, invB0, delta, ("%.6f" % hist) if hist else "0.0(65精确)", dev_txt), flush=True)

# ---- 分层结构判别（重算后）----
print("", flush=True)
print("【分层结构判别（重算值）】", flush=True)
ms = list(range(-1, -15, -1))
ds = [out[m]["delta"] for m in ms]
# 均匀带 m=-2..-4
band = ds[1:4]
print("均匀带 m=−2..−4：δ = %s——%s" % (["%.3e" % x for x in band],
    "OK（<5e-4，非零小失调）" if all(x < 5e-4 for x in band) else "偏离"), flush=True)
# 线性段 m=-5..-8
lin = ds[4:8]
d1_lin = [lin[i+1]-lin[i] for i in range(3)]
slope = sum(d1_lin)/3.0
k_ref = (6.0/np.pi)/1400.0
print("线性段 m=−5..−8：δ = %s——差分 %s——斜率 %.6f vs κ/1400=%.6f（%+.2f pct）" % (
    ["%.6f" % x for x in lin], ["%+.6f" % x for x in d1_lin], slope, k_ref,
    (slope-k_ref)/k_ref*100), flush=True)
# 曲率段 m=-9..-14（P7-5e-115/116：三次多项式形态）
quad = ds[8:14]
d1_q = [quad[i+1]-quad[i] for i in range(5)]
d2_q = [d1_q[i+1]-d1_q[i] for i in range(4)]
d3_q = [d2_q[i+1]-d2_q[i] for i in range(3)]
mean_d2 = sum(d2_q)/4.0
devs = [abs(x-mean_d2)/abs(mean_d2)*100 for x in d2_q]
print("曲率段 m=−9..−14：δ = %s" % ["%.6f" % x for x in quad], flush=True)
print("  一阶差分 %s" % ["%+.6f" % x for x in d1_q], flush=True)
print("  二阶差分 %s——均值 %.3e，各点偏差 %s pct" % (
    ["%+.6f" % x for x in d2_q], mean_d2,
    ["%.1f" % x for x in devs]), flush=True)
print("  三阶差分 %s——三次判别：%s" % (
    ["%+.6f" % x for x in d3_q],
    "★ 恒定（三次多项式确认）" if max(d3_q)-min(d3_q) < 1e-5 else "非恒定（更高阶）"), flush=True)

json.dump({"out": {str(k): v for k, v in out.items()},
           "deltas": {str(k): float(v) for k, v in zip(ms, ds)}},
          open(os.path.join(BASE, "_phase102_p7_5e_fullchain_tridiag.json"), "w", encoding="utf-8"),
          indent=1, ensure_ascii=False)
print("", flush=True)
print("全链耗时 %.1f s——JSON 落盘 OK exit 0" % (time.time()-t_start), flush=True)
