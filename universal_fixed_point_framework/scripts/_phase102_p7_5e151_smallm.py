# -*- coding: utf-8 -*-
"""
P7-5e-151：小 m 区真实结构——2^m 机制核心判别
δ_1/8(m) = 1/B* − (|m|/2 + 1/8) 全序列（小 m 区真实偏离双曲的结构）
P1 δ_1/8(m) 与 C/m 的差：ε(m) = δ_1/8(m) − C/m（C=13/128）
P2 ε(m) 候选形式：1/(7·2^m)？(1/56)·2^{-m}？C·2^{-m}？c/m²？
P3 m=5 跳跃确认：dr 窗口一致性 + rms（排除数据伪影）
P4 闭式 1/(7·2^m) 项在小 m 的补偿精确性：δ_cl vs [1/56 + 1/(7·2^m) − C/m]
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
        out = {}
        for w in wins:
            win = rec["dr"][w]
            out[w] = (1.0/win["Bstar"], win.get("rms", None))
        return out
    return None

C = 13.0/128.0
print("m\twin0_invB\tδ_1/8\tε=δ_1/8−C/m\t1/(7·2^m)\tε/geom\tε·m²\tε·m·2^m", flush=True)
ms = list(range(1, 15))
for m in ms:
    rec = d1["out"].get(str(-m))
    if rec is None:
        continue
    cl = rec["closed_1B"]
    wins = get_invB(rec)
    if not wins:
        continue
    # 多窗口对比（m=5 跳跃确认）
    invBs = {w: v[0] for w, v in wins.items()}
    invB = invBs[sorted(invBs.keys(), key=float)[0]]
    d18 = invB - (abs(m)/2.0 + 1.0/8.0)
    eps = d18 - C/abs(m)
    geom = 1.0/(7.0*2.0**m)
    # 闭式残差
    delta_cl = cl - invB
    pred = 1.0/56.0 + geom - C/abs(m)
    ratio_pred = delta_cl/pred if pred != 0 else float('nan')
    print("%d\t%.9f\t%.6f\t%+.3e\t%.3e\t%+.4f\t%.4f\t%.4f\tdelta_cl=%.3e pred=%.3e r=%.3f" % (
        m, invB, d18, eps, geom, eps/geom if geom else 0, eps*m*m,
        eps*m*2.0**m, delta_cl, pred, ratio_pred), flush=True)
    if len(invBs) > 1:
        print("   窗口差异：%s" % {k: round(v, 9) for k, v in invBs.items()}, flush=True)
