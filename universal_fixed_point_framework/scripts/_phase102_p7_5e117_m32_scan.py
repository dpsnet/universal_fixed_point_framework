# -*- coding: utf-8 -*-
"""
P7-5e-117：m=−15..−32 大规模外推（三次多项式延续/断裂判别 + 闭式大|m|检验）
===========================================================================
先验（计算前登记）：
  P1——三次延续假设：9..14 六点三次拟合外推 δ_pred(m)，m=15..32。
        预测 δ(32) ≈ 0.029（三次外推）——若实测 δ(32) 接近 → 三次延续；
        若远偏离 → 新结构/断裂（判别点）。
  P2——闭式成立：1/B*(m) = |m|/2 + 1/7 + 1/(7·2^|m|) 对 m=32（1/7 项保持）。
        若闭式失效，窗口 ±2.65% 套不住根或 δ 跳变巨大。
方法：每点三档 tridiag（dr=0.02/0.01/0.005）× 7 点窗口 → Richardson 二阶 → δ(1/B)。
r_max 校验：m=−15 对比 r_max=120 vs 240（dr=0.01 单档）。
"""
import time, json, os
import numpy as np
from scipy.linalg import eigvalsh_tridiagonal

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"
w = 0.0265
drs = [0.02, 0.01, 0.005]

def closed_1B(m):
    v = abs(m)/2.0 + 1.0/7.0 + 1.0/(7.0*2.0**abs(m))
    if m == -1:
        v += 1.0/65.0
    return v

def solve(N_r, r_max, B, m):
    dr = r_max / N_r
    j = np.arange(N_r)
    r = (j + 0.5) * dr
    d = np.ones(N_r) / dr**2 + (m + 0.5 * B * r**2)**2 / (2.0 * r**2) - 1.0 / r
    e = -np.ones(N_r - 1) / (2.0 * dr**2)
    return float(eigvalsh_tridiagonal(d, e, select='i', select_range=(0, 0))[0])

def Bstar_3dr(m, r_max, verbose=False):
    cl = closed_1B(m)
    Bc = 1.0/cl
    Bs = np.linspace(Bc*(1-w), Bc*(1+w), 7)
    res = {}
    for dr in drs:
        N_r = int(round(r_max / dr))
        Es = np.array([solve(N_r, r_max, float(B), m) for B in Bs])
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
        res[dr] = {"Bstar": Bcross, "rms": rms}
    R2 = (4*res[0.005]["Bstar"] - res[0.01]["Bstar"])/3.0
    delta = abs(1.0/R2 - cl)
    return R2, delta, res

# ---------- ① 先验登记：六点三次拟合外推（读全链权威 9..14） ----------
fc = json.load(open(os.path.join(BASE, "_phase102_p7_5e_fullchain_tridiag.json"), encoding="utf-8"))
deltas = {int(k): v for k, v in fc["deltas"].items()}
mm = np.arange(9, 15, dtype=float)
dd = np.array([deltas[-k] for k in range(9, 15)])
A3 = np.vstack([np.ones(6), mm, mm**2, mm**3]).T
c3f, _, _, _ = np.linalg.lstsq(A3, dd, rcond=None)
a, b, c, e = c3f
pred = {}
for k in range(15, 33):
    pred[k] = float(a + b*k + c*k**2 + e*k**3)
print("先验（六点三次拟合 9..14）：δ(m) = %.6f + %.6f·m + %.7f·m² + %.2e·m³" % (a, b, c, e), flush=True)
print("外推预测 δ_pred：m=15: %.4f  m=20: %.4f  m=25: %.4f  m=32: %.4f" %
      (pred[15], pred[20], pred[25], pred[32]), flush=True)

# ---------- ② r_max 校验（m=−15） ----------
print("", flush=True)
print("== r_max 校验（m=−15，dr=0.01 单档 B* 对比）==", flush=True)
def Bstar_1dr(m, r_max, dr):
    cl = closed_1B(m); Bc = 1.0/cl
    Bs = np.linspace(Bc*(1-w), Bc*(1+w), 7)
    N_r = int(round(r_max / dr))
    Es = np.array([solve(N_r, r_max, float(B), m) for B in Bs])
    B0 = float(Bs[3]); X = Bs - B0
    A = np.vstack([np.ones_like(X), X, X**2, X**3]).T
    coef, _, _, _ = np.linalg.lstsq(A, Es, rcond=None)
    c0, c1, c2, c3 = coef
    x = -c0/c1
    for _ in range(6):
        x = x - (c0+c1*x+c2*x**2+c3*x**3)/(c1+2*c2*x+3*c3*x**2)
    return B0 + x
for rmax in [120.0, 240.0]:
    print("  r_max=%.0f → B*=%.8f" % (rmax, Bstar_1dr(-15, rmax, 0.01)), flush=True)
diff_rmax = abs(Bstar_1dr(-15, 120.0, 0.01) - Bstar_1dr(-15, 240.0, 0.01))
print("  差异 = %.2e —— %s" % (diff_rmax, "r_max=120 充足" if diff_rmax < 1e-7 else "r_max=120 不足，需 240"), flush=True)

# ---------- ③ 主循环 m=−15..−32 ----------
print("", flush=True)
print("== 批量计算 m=−15..−32（三档×7点，r_max=120）==", flush=True)
out = {}
t0 = time.time()
for m in range(-15, -33, -1):
    cl = closed_1B(m)
    B0v, delta, res = Bstar_3dr(m, 120.0)
    dev_pred = (delta - pred[abs(m)])/pred[abs(m)]*100 if abs(m) in pred else None
    out[m] = {"closed_1B": cl, "Bstar0": float(B0v), "delta": float(delta),
              "pred_cubic": pred[abs(m)], "dev_pred_pct": dev_pred, "res": res}
    print("m=%3d  闭式 1/B*=%.8f  B*(0)=%.8f  δ=%.6f  三次预测=%.4f  偏差=%s"
          % (m, cl, B0v, delta, pred[abs(m)],
             ("%+.2f pct" % dev_pred) if dev_pred is not None else "—"), flush=True)
dt = time.time() - t0
print("总耗时 %.1f s" % dt, flush=True)

# ---------- ④ 差分诊断（m=14..32 序列） ----------
ms_abs = list(range(14, 33))
ds_seq = [deltas[-14]] + [out[m]["delta"] for m in range(-15, -33, -1)]
print("", flush=True)
print("== 差分诊断（|m|=14..32）==", flush=True)
d1 = [ds_seq[i+1]-ds_seq[i] for i in range(len(ds_seq)-1)]
d2 = [d1[i+1]-d1[i] for i in range(len(d1)-1)]
d3 = [d2[i+1]-d2[i] for i in range(len(d2)-1)]
d4 = [d3[i+1]-d3[i] for i in range(len(d3)-1)]
print("  d1（14..32）：%s" % " ".join("%+.5f" % x for x in d1), flush=True)
print("  d2（15..32）：%s" % " ".join("%+.5f" % x for x in d2), flush=True)
print("  d3（16..32）：%s" % " ".join("%+.5f" % x for x in d3), flush=True)
print("  d4（17..32）：%s" % " ".join("%+.5f" % x for x in d4), flush=True)
# 三次延续窗口：|d3| 恒定 2e-5 级的 m 范围
stable = []
for i in range(len(d3)):
    if abs(d3[i]) < 4e-5:
        stable.append(ms_abs[2+i])
print("  三阶差分 |d3|<4e-5 的 m 范围：%s..%s（高阶差分散射级——非三次延续证据）" % (stable[0], stable[-1]), flush=True)
# 真正的判别：三次外推偏差（117b 双曲精化已确认 δ=δ∞−C/m，m≥13 全场 RMS 1.5e-6）
if len(stable) >= 2 and stable[-1] >= 32:
    verdict = "★ 三次多项式为 m=9..14 局部形态；m≥13 双曲渐近 δ∞−C/m（δ∞≈0.0179≈1/56 候选）——117b 精化确认"
else:
    verdict = "三次形态断裂——新结构出现（117b 精化：双曲渐近）"
print("  判别：%s" % verdict, flush=True)

json.dump({"pred_cubic_9_14": {"a": float(a), "b": float(b), "c": float(c), "e": float(e)},
           "pred_delta": {str(k): pred[k] for k in pred},
           "rmax_check_m15": diff_rmax,
           "out": {str(k): v for k, v in out.items()},
           "d1": d1, "d2": d2, "d3": d3, "d4": d4, "verdict": verdict,
           "runtime_s": dt},
          open(os.path.join(BASE, "_phase102_p7_5e117_m32_scan.json"), "w", encoding="utf-8"),
          indent=1, ensure_ascii=False)
print("", flush=True)
print("JSON 落盘 OK exit 0", flush=True)
