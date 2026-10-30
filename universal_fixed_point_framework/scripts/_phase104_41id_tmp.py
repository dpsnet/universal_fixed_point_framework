# -*- coding: utf-8 -*-
"""Phase 104az-50：41 MG 框架身份系统搜索——框架内生常数组合命中 41.0/41.02"""
import numpy as np
from itertools import product

# 框架内生常数池
C = {
    "k_max": 8.0, "N_Weyl": 4.0, "N_c": 3.0, "N_gen": 3.0, "N_f": 3.0,
    "N_active": 3.0, "N_total": 5.0, "B": 15.0, "sigma": 1.0/15.0,
    "d_H": np.log(15.0), "d_H_reg": np.log(15.0) + 1.0/675.0,
    "s": np.exp(-1.0), "alpha0_3": 1.0/8.0,
    "dlam": (np.sqrt(3.0)-1.0)/6.0,
    "inv_alpha_EM": 24.0*(np.log(15.0)+3.0),
    "alpha_EM": 1.0/(24.0*(np.log(15.0)+3.0)),
    "E_b_Ryd": 13.576, "C_MG": 2350.5, "C2_MG": 2352.7,
    "pi": np.pi, "e": np.e, "sqrt2": np.sqrt(2.0), "sqrt3": np.sqrt(3.0),
    "sqrt5": np.sqrt(5.0), "ln2": np.log(2.0), "ln3": np.log(3.0), "ln15": np.log(15.0),
}

TARGETS = [41.0, 41.02]

def hits_for(target):
    hits = []
    names = list(C.keys())
    # 二量 a op b
    for a, b in product(names, repeat=2):
        va, vb = C[a], C[b]
        ops = {
            "a+b": va+vb, "a-b": va-vb, "b-a": vb-va, "a*b": va*vb,
            "a/b": va/vb if vb else None, "b/a": vb/va if va else None,
            "a*b/pi": va*vb/np.pi, "a/b*pi": va/vb*np.pi if vb else None,
        }
        # 幂运算（仅小底小指数）
        for pa, pb in [(va, vb), (vb, va)]:
            if pa > 0 and 0 < abs(pb) < 10 and abs(pa) < 5:
                try:
                    vp = pa**pb
                    if np.isfinite(vp) and abs(vp) < 1e4:
                        ops["pow"] = vp
                except Exception:
                    pass
        for opn, v in ops.items():
            if v is None or not np.isfinite(v):
                continue
            for t in TARGETS:
                rel = abs(v - t)/t
                if rel < 0.002:  # 0.2% 内
                    hits.append((rel, "%s(%s,%s)=%.4f" % (opn, a, b, v), v))
    # 三量 a op (b op c) 常见形态：a*b/c, a*(b+c), a*(b-c), a+b*c, a/b*c
    for a, b, c in product(names, repeat=3):
        va, vb, vc = C[a], C[b], C[c]
        combos = {
            "a*b/c": va*vb/vc if vc else None,
            "a*(b+c)": va*(vb+vc),
            "a*(b-c)": va*(vb-vc),
            "a+b*c": va+vb*vc,
            "a+b/c": va+vb/vc if vc else None,
            "(a+b)*c": (va+vb)*vc,
            "(a-b)*c": (va-vb)*vc,
            "a*b+c": va*vb+vc,
            "a/b+c": va/vb+vc if vb else None,
            "a/(b+c)": va/(vb+vc) if (vb+vc) else None,
            "a/b*c": va/vb*vc if vb else None,
            "a*b-c": va*vb-vc,
        }
        for opn, v in combos.items():
            if v is None or not np.isfinite(v) or abs(v) > 1e4:
                continue
            for t in TARGETS:
                rel = abs(v - t)/t
                if rel < 0.0015:  # 0.15% 内
                    hits.append((rel, "%s(%s,%s,%s)=%.4f" % (opn, a, b, c, v), v))
    hits.sort(key=lambda x: x[0])
    return hits

for t in TARGETS:
    hs = hits_for(t)
    print("=== 目标 %.2f 命中（rel<0.15-0.2%%）共 %d ===" % (t, len(hs)))
    seen = set()
    for rel, expr, v in hs[:40]:
        if expr in seen:
            continue
        seen.add(expr)
        print("  %.4f%%  %s" % (rel*100, expr))

# 特别检查：41 = k_max*(N_total + alpha0_3)
print("\n=== 候选 1：k_max*(N_total+alpha0_3) ===")
v = C["k_max"]*(C["N_total"] + C["alpha0_3"])
print("  8*(5+1/8) = %.6f   vs 41.0  rel=%.4f%%" % (v, 100*abs(v-41)/41))

print("\n=== 候选 2：C_MG 标定（41 = C/(180/pi)？外部常数） ===")
v = C["C_MG"]/(180.0/np.pi)
print("  2350.5/(180/pi) = %.4f   vs 41.02  rel=%.4f%%" % (v, 100*abs(v-41.02)/41.02))
print("  (180/pi 为角度制人为常数——不内生，仅登记)")

print("\n=== 候选 3：41 vs B_th 序列（n_eff 搜索） ===")
for n in np.arange(7.0, 8.0, 0.01):
    b = C["C2_MG"]/n**2
    if abs(b - 41.0)/41.0 < 0.002:
        print("  n_eff=%.3f → B=%.2f MG (rel %.3f%%)" % (n, b, 100*abs(b-41)/41))

print("\n=== 候选 4：41 vs 1/alpha_EM / n_eff ===")
print("  1/alpha_EM/41 = %.4f" % (C["inv_alpha_EM"]/41.0))
print("  1/alpha_EM/41.02 = %.4f" % (C["inv_alpha_EM"]/41.02))
print("  alpha_EM*41*1000 = %.3f" % (C["alpha_EM"]*41*1000))

print("\n=== 候选 5：41 vs d_H 组合 ===")
print("  d_H*15 = %.4f  (rel %.3f%%)" % (C["d_H"]*15, 100*abs(C["d_H"]*15-41)/41))
print("  d_H_reg*15 = %.4f  (rel %.3f%%)" % (C["d_H_reg"]*15, 100*abs(C["d_H_reg"]*15-41)/41))
print("  B*d_H_reg = %.4f  (rel %.3f%%)" % (C["B"]*C["d_H_reg"], 100*abs(C["B"]*C["d_H_reg"]-41)/41))
print("  ln15*15 = %.4f  (rel %.3f%%)" % (np.log(15)*15, 100*abs(np.log(15)*15-41)/41))
print("  41/15 = %.6f =? d_H %.6f (rel %.3f%%)" % (41/15, C["d_H"], 100*abs(41/15-C["d_H"])/C["d_H"]))
print("  41/15 = %.6f =? d_H_reg %.6f (rel %.3f%%)" % (41/15, C["d_H_reg"], 100*abs(41/15-C["d_H_reg"])/C["d_H_reg"]))

print("\n=== 候选 6：41 vs N_total/k_max/alpha 组合 ===")
print("  k_max*N_total+1 = %.1f" % (C["k_max"]*C["N_total"]+1))
print("  k_max*N_total+alpha0_3*8 = %.4f" % (C["k_max"]*C["N_total"]+C["alpha0_3"]*8))
print("  B*N_total-k_max = %.1f" % (C["B"]*C["N_total"]-C["k_max"]))
print("  B*N_active+? : 15*3=45, 45-4=%d" % (45-4))
print("  2*k_max*N_total/2+1 : %d" % (8*5/2*2+1))

print("\n=== 候选 7：41 与阈值序列比 ===")
seq = [48.01, 65.35, 94.11, 147.05, 261.41]
for i, b in enumerate(seq):
    print("  B_th(n=%d)=%.2f /41 = %.3f" % (7-i, b, b/41))
