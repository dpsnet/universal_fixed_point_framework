# -*- coding: utf-8 -*-
"""Phase 104az-51：41 MG 单位标定链搜索——f=41/2352.7 的框架组合 + 独立量纲候选"""
import numpy as np
from itertools import product

C = {
    "k_max": 8.0, "N_Weyl": 4.0, "N_c": 3.0, "N_gen": 3.0, "N_f": 3.0,
    "N_active": 3.0, "N_total": 5.0, "B": 15.0, "sigma": 1.0/15.0,
    "d_H": np.log(15.0), "d_H_reg": np.log(15.0) + 1.0/675.0,
    "s": np.exp(-1.0), "alpha0_3": 1.0/8.0,
    "dlam": (np.sqrt(3.0)-1.0)/6.0,
    "inv_alpha_EM": 24.0*(np.log(15.0)+3.0),
    "alpha_EM": 1.0/(24.0*(np.log(15.0)+3.0)),
    "C_MG": 2350.5, "C2_MG": 2352.7, "E_b": 13.576,
    "pi": np.pi, "e": np.e, "sqrt2": np.sqrt(2.0), "sqrt3": np.sqrt(3.0),
    "sqrt5": np.sqrt(5.0), "ln2": np.log(2.0), "ln3": np.log(3.0), "ln15": np.log(15.0),
}

T_C = 2352.7   # B_th x n^2 谱定（MG）
T41 = 41.0

def search(target, tol):
    hits = []
    names = list(C.keys())
    for a, b in product(names, repeat=2):
        va, vb = C[a], C[b]
        ops = {
            "a+b": va+vb, "a-b": va-vb, "b-a": vb-va, "a*b": va*vb,
            "a/b": va/vb if vb else None, "b/a": vb/va if va else None,
            "a*b/pi": va*vb/np.pi, "a/b*pi": va/vb*np.pi if vb else None,
            "a*b*d": None,  # placeholder
        }
        for opn, v in ops.items():
            if v is None or not np.isfinite(v) or abs(v) > 1e5:
                continue
            rel = abs(v - target)/target
            if rel < tol:
                hits.append((rel, "%s(%s,%s)=%.5f" % (opn, a, b, v)))
    for a, b, c in product(names, repeat=3):
        va, vb, vc = C[a], C[b], C[c]
        combos = {
            "a*b/c": va*vb/vc if vc else None,
            "a*(b+c)": va*(vb+vc), "a*(b-c)": va*(vb-vc),
            "a+b*c": va+vb*vc, "a+b/c": va+vb/vc if vc else None,
            "(a+b)*c": (va+vb)*vc, "(a-b)*c": (va-vb)*vc,
            "a*b+c": va*vb+vc, "a/b+c": va/vb+vc if vb else None,
            "a/(b+c)": va/(vb+vc) if (vb+vc) else None,
            "a/b*c": va/vb*vc if vb else None, "a*b-c": va*vb-vc,
        }
        for opn, v in combos.items():
            if v is None or not np.isfinite(v) or abs(v) > 1e5:
                continue
            rel = abs(v - target)/target
            if rel < tol:
                hits.append((rel, "%s(%s,%s,%s)=%.5f" % (opn, a, b, c, v)))
    hits.sort(key=lambda x: x[0])
    return hits

print("=== 目标 A：f = 41/2352.7 = %.7f 的框架组合（rel<0.1%%） ===" % (T41/T_C))
f = T41/T_C
hs = search(f, 0.001)
for rel, expr, in hs[:25]:
    print("  %.4f%%  %s" % (rel*100, expr))

print("\n=== 目标 B：41 = C_MG×组合（直接形式，rel<0.1%%） ===")
names = list(C.keys())
for a in names:
    va = C[a]
    if va == 0:
        continue
    # 41/C 与 1/va 比较
    r = T41/T_C
    for b in names:
        vb = C[b]
        cands = {"r/va": r/va, "r*va": r*va, "r+va": r+va, "r-va": r-va, "va-r": va-r,
                 "(r*va)^.5": np.sqrt(abs(r*va)), "(r/va)^.5": np.sqrt(abs(r/va))}
        for opn, v in cands.items():
            if not np.isfinite(v) or abs(v) > 100:
                continue
            rel = abs(v-1.0)
            if rel < 0.001:
                print("  %.4f%%  41 = C_MG×%s  (%.6f)" % (rel*100, opn, v))

print("\n=== 目标 C：独立量纲链——41 MG 的 ħω_c/E_b 关系 ===")
muB = 9.274009994e-24  # J/T
eJ = 1.602176634e-19
hw = 41e6*muB/eJ*1000  # meV
print("  hbar*omega_c(41 MG) = %.4f meV" % hw)
print("  E_b/hw = %.2f  (E_b=13.576 eV 框架 Ryd)" % (13576.0/hw))
print("  hw/E_b = %.6f" % (hw/13576.0))
print("  hw/E_b vs sigma^2=%.6f (1/225): ratio=%.4f" % (1.0/225.0, (hw/13576.0)/(1.0/225.0)))
print("  hw/E_b vs alpha_EM=%.6f: ratio=%.4f" % (1.0/137.028, (hw/13576.0)/(1.0/137.028)))
print("  hw/E_b vs alpha0_3*sigma=%.6f: ratio=%.4f" % ((1.0/8.0)/15.0, (hw/13576.0)/((1.0/8.0)/15.0)))
print("  hw/E_b vs 3sigma*alpha0_3=%.6f: ratio=%.4f" % (3.0/15.0/8.0, (hw/13576.0)/(3.0/15.0/8.0)))

print("\n=== 目标 D：41 = B_th(n_eff) 的 n_eff 框架身份 ===")
neff2 = T_C/T41
neff = np.sqrt(neff2)
print("  n_eff^2 = %.4f, n_eff = %.4f" % (neff2, neff))
print("  n_eff^2 候选：k_max(N_total+alpha0_3)*7/5 = %.4f (rel %.3f%%)" %
      (8*(5+1.0/8)*7.0/5.0, 100*abs(8*(5+1.0/8)*7.0/5.0-neff2)/neff2))
print("  n_eff^2 候选：N_total*k_max*7/5+? = %.4f" % (5*8*7.0/5.0))
print("  n_eff^2 候选：B*d_H*s^2*? = %.4f" % (15*np.log(15)*np.exp(-2)))
print("  n_eff 候选：sqrt(57.38)=7.573 — vs k_max*15/16=%.3f vs 15*3sigma/1=%.2f" % (8*15.0/16, 15*0.2))
print("  n_eff vs d_H*e = %.3f (rel %.2f%%)" % (np.log(15)*np.e, 100*abs(np.log(15)*np.e-7.573)/7.573))
print("  n_eff vs k_max*15/(N_total+?) ...")
