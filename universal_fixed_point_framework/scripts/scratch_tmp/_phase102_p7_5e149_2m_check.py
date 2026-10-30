# -*- coding: utf-8 -*-
"""
P7-5e-149 正式：2^m 静默族机制判别
用 tridiag（-1..-14）与 m32（-15..-32）实测 B*（dr 窗口或 Bstar0）：
δ_cl(m) = closed_1B − 1/B*_实测，对比 1/(7·2^m)
判别：残差/1(7·2^m) 的 m 依赖——纯指数（~常数）或修正指数（含 O(1/m)）
"""
import json, numpy as np

base = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"

def load(fn):
    with open(base + "\\" + fn, "r", encoding="utf-8") as f:
        return json.load(f)

d1 = load("_phase102_p7_5e_fullchain_tridiag.json")
d2 = load("_phase102_p7_5e117_m32_scan.json")

def get_bstar(rec):
    """从记录提取实测 1/B*：优先 dr 窗口列表，其次 Bstar0"""
    if "dr" in rec and rec["dr"]:
        for w, win in rec["dr"].items():
            if isinstance(win, dict) and "Bstar" in win:
                return 1.0/win["Bstar"]
            if isinstance(win, (int, float)):
                return 1.0/win
    if "Bstar0" in rec:
        return 1.0/rec["Bstar0"]
    return None

print("=== P7-5e-149 2^m 静默族机制判别 ===", flush=True)
print("m\tcl_1B\tinvB_meas\tdelta_cl\t1/(7·2^m)\tdelta/geom\tlog2", flush=True)
ms_all = list(range(1, 15)) + list(range(15, 33))
for m in ms_all:
    rec = d1["out"].get(str(-m)) or d2["out"].get(str(-m))
    if not rec:
        continue
    cl = rec["closed_1B"]
    invB = get_bstar(rec)
    if invB is None:
        continue
    delta = cl - invB
    geom = 1.0/(7.0*2.0**m)
    ratio = delta/geom if geom != 0 else float('nan')
    # 相对误差（对 1/B*）
    rel = abs(delta)/cl
    print("%d\t%.9f\t%.9f\t%+.3e\t%.3e\t%.4f\t%.2f" % (
        m, cl, invB, delta, geom, ratio, np.log2(abs(delta)) if delta != 0 else -99), flush=True)
