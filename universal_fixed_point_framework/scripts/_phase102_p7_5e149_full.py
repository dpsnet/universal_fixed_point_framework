# -*- coding: utf-8 -*-
"""
P7-5e-149b：2^m 静默族完整判别（m=1..32）
δ_cl(m) = closed_1B − 1/B*_实测（dr 窗口最优）
判别：残差相对 1/B* 的量级（0.02% 均匀带？）+ 残差/1(7·2^m) 的 m 依赖（纯指数 or 修正）
"""
import json, numpy as np

base = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"

def load(fn):
    with open(base + "\\" + fn, "r", encoding="utf-8") as f:
        return json.load(f)

d1 = load("_phase102_p7_5e_fullchain_tridiag.json")
d2 = load("_phase102_p7_5e117_m32_scan.json")

def get_invB(rec):
    if "dr" in rec and rec["dr"]:
        wins = sorted(rec["dr"].keys(), key=lambda w: float(w))
        w = wins[0]  # 最窄窗口最优
        win = rec["dr"][w]
        if isinstance(win, dict) and "Bstar" in win:
            return 1.0/win["Bstar"]
        return 1.0/win
    if "Bstar0" in rec:
        return 1.0/rec["Bstar0"]
    return None

print("m\tcl_1B\tinvB_meas\tdelta_cl\trel%%\t1/(7·2^m)\tdelta/geom")
ms = list(range(1, 15)) + list(range(15, 33))
for m in ms:
    rec = d1["out"].get(str(-m))
    if rec is None:
        rec = d2["out"].get(str(-m))
    if rec is None:
        continue
    cl = rec["closed_1B"]
    invB = get_invB(rec)
    if invB is None:
        continue
    delta = cl - invB
    rel = abs(delta)/cl*100
    geom = 1.0/(7.0*2.0**m)
    ratio = delta/geom if geom != 0 else float('nan')
    print("%d\t%.9f\t%.9f\t%+.3e\t%.4f\t%.3e\t%+.4f" % (m, cl, invB, delta, rel, geom, ratio))
