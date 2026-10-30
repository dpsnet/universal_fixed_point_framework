# -*- coding: utf-8 -*-
"""
P7-5e-152：C 判别升级——D 连续性判别
δ_1/8(m)·m = u(m) = C + D(m)/m。D(m) = m·(u(m) − C)。
判别：C=13/128 vs 0.1016——哪个使 D(m)（小 m→大 m）连贯单调？
数据：m=1..14 ε·m²（151，C=13/128 假设）；m=128/256 u 高精度（148）。
若 C=13/128：D(m) 应单调趋稳；若 C=0.1016：D 应跳变不连续。
"""
import json, numpy as np

base = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"

def load(fn):
    with open(base + "\\" + fn, "r", encoding="utf-8") as f:
        return json.load(f)

d1 = load("_phase102_p7_5e_fullchain_tridiag.json")

# 高精度 u 值（148）
u_hi = {128: 0.10172153, 256: 0.10164247}
# 小 m δ_1/8（151 原始：invB − (m/2+1/8)）
d18_small = {}
for m in range(1, 15):
    rec = d1["out"].get(str(-m))
    if rec is None: continue
    wins = sorted(rec["dr"].keys(), key=float)
    invB = 1.0/rec["dr"][wins[0]]["Bstar"]
    d18_small[m] = invB - (m/2.0 + 1.0/8.0)

cands = {"13/128": 13.0/128.0, "0.1016": 0.1016}
print("=== P7-5e-152 D 连续性判别 ===", flush=True)
for cname, C in cands.items():
    print("--- C = %s（%.8f）---" % (cname, C), flush=True)
    # 小 m D(m) = m²·(δ_1/8 − C/m)
    print("  小 m D(m)：", flush=True)
    Ds = {}
    for m in sorted(d18_small):
        D = m*m*(d18_small[m] - C/m)
        Ds[m] = D
        print("    m=%2d: D=%.6f" % (m, D), flush=True)
    # 大 m
    for m, u in sorted(u_hi.items()):
        D = m*(u - C)
        Ds[m] = D
        print("    m=%3d: D=%.6f" % (m, D), flush=True)
    # 连贯性指标：相邻 D 差（m=6..14 稳定区 + 14→128→256）
    seq = sorted(Ds.keys())
    jumps = [abs(Ds[seq[i+1]] - Ds[seq[i]]) for i in range(len(seq)-1)]
    print("  相邻差：%s" % [round(j, 5) for j in jumps], flush=True)
    # 尾端趋势：m=8..14 均值 vs m=128/256
    small_tail = np.mean([Ds[m] for m in [8,9,10,11,12,13,14]])
    big = Ds[256]
    print("  小 m 尾（8..14）均值 D=%.5f；D(256)=%.5f；差 %.5f（%.2f%%）" % (
        small_tail, big, abs(small_tail-big), abs(small_tail-big)/small_tail*100), flush=True)
