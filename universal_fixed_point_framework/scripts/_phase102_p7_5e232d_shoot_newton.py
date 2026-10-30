# -*- coding: utf-8 -*-
"""
P7-5e-232d：打靶 Newton 纯求根判别（负 m 通道，230c 已验证可复现）
====================================================================
232b（N=1200 谱）已示：Newton 纯求根消除高 m 段线性残差，残差变平坦 ~−2.15e-7≈−ε_w。
本脚本用打靶（DP45 + brentq 1e-12，最高精度通道）做 Newton 细化（负 m，同 230c）：
  若打靶 Newton 版残差也平坦（≈−ε_w 或 ≈0）→ 三次拟合是线性残差来源，
  且 ε（δ∞ 偏移）在纯求根通道消失 → δ∞=1/56 精确候选；
  若打靶 Newton 版仍线性 → 线性残差在真值通道存在（物理/闭式）。
"""
import time, sys, os
import numpy as np
import importlib.util
from scipy.optimize import brentq

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"
sys.path.insert(0, BASE)
spec = importlib.util.spec_from_file_location(
    "p230c", os.path.join(BASE, "_phase102_p7_5e230c_shoot_full_chain.py"))
m230c = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m230c)

C13 = 13.0/128.0
D41 = 41.0/2000.0
E39 = 39.0/2000.0
INV56 = 1.0/56.0
EPS_W = 0.215e-6

def Bstar_shoot_newton(mm, steps=1, h_rel=1e-5):
    """三次拟合根 + 打靶 E0 的 Newton 细化（负 m）"""
    m = -abs(mm)          # 负 m（230c 通道）
    cl = m230c.closed_1B(m)
    r_lo = 0.23*abs(m); r_hi = 3.1*abs(m)
    B, Bs, Es = m230c.Bstar_shooting(m)
    for _ in range(steps):
        h = h_rel*abs(B)
        e_p = m230c.E0_shooting(B+h, m, r_lo, r_hi)
        e_m = m230c.E0_shooting(B-h, m, r_lo, r_hi)
        e_0 = m230c.E0_shooting(B, m, r_lo, r_hi)
        de = (e_p - e_m)/(2.0*h)
        if not np.isfinite(de) or de == 0.0:
            break
        dB = -e_0/de
        B = B + dB
        if abs(dB) < 1e-14*abs(B):
            break
    return B

if __name__ == "__main__":
    t0 = time.time()
    print("== P7-5e-232d：打靶 Newton 纯求根判别（负 m）==", flush=True)
    print("  m     | δ(三次拟合)  | δ(打靶Newton) | Δδ          | r(Newton)   | r(N1200-Newton)", flush=True)
    ms_test = [33, 129, 256, 512, 513, 640, 768, 896, 1024]
    out = {}
    for mm in ms_test:
        cl = m230c.closed_1B(-mm)
        Bc, _, _ = m230c.Bstar_shooting(-mm)
        Bn = Bstar_shoot_newton(mm)
        dc = cl - 1.0/Bc
        dn = cl - 1.0/Bn
        mod = INV56 + EPS_W - C13/mm - D41/mm**2 + E39/mm**3
        rn = dn - mod
        rn1200 = {"33": -2.13e-7, "129": -2.15e-7, "256": -2.15e-7, "512": -2.15e-7,
                  "513": -2.15e-7, "640": -2.11e-7, "768": -2.15e-7, "896": -2.23e-7,
                  "1024": -2.01e-7}.get(str(mm), float('nan'))
        print("  %4d | %.10f | %.10f | %+.2e | %+.2e | %+.2e" %
              (mm, dc, dn, dn-dc, rn, rn1200), flush=True)
        out[str(mm)] = {"delta_cubic": dc, "delta_newton_shoot": dn, "r_newton_shoot": rn}

    print("", flush=True)
    msf = np.array([mm for mm in ms_test if 512 <= mm <= 1024], dtype=float)
    rn_arr = np.array([out[str(mm)]["r_newton_shoot"] for mm in ms_test if 512 <= mm <= 1024])
    X = np.vstack([np.ones_like(msf), msf]).T
    c = np.linalg.lstsq(X, rn_arr, rcond=None)[0]
    rms = float(np.sqrt(np.mean((X@c-rn_arr)**2)))
    print("  打靶 Newton 高 m 段残差线性拟合: %+.3e + %+.3e·m（RMS %.2e）" % (c[0], c[1], rms), flush=True)
    print("  均值 %+.3e（≈ −ε_w=%+.3e？）" % (float(np.mean(rn_arr)), -EPS_W), flush=True)
    json.dump({"base": "shooting Newton pure-root vs cubic-fit (neg-m)", "out": out,
               "runtime_s": time.time()-t0},
              open(os.path.join(BASE, "_phase102_p7_5e232d_shoot_newton.json"), "w",
                   encoding="utf-8"), indent=1, ensure_ascii=False)
    print("JSON 落盘 OK exit 0", flush=True)
