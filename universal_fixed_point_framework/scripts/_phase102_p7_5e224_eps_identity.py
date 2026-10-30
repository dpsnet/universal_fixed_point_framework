# -*- coding: utf-8 -*-
# P7-5e-224: eps = dinf - 1/56 analytic identity search
# 先验登记：eps_true 未知。任务 (a) 判断 eps 是真实常数还是三点拟合对 D 项的范围吸收；
# (b) 在框架常数组合空间搜索 eps 的简单解析候选。
# 判据：相对偏差 <0.1% 强候选；<1% 弱候选；其余开放。
import json, sys, math

sys.set_int_max_str_digits(0)

O56 = 1.0 / 56.0

# eps values from 223 json + refs (all dinf - 1/56)
eps_vals = {
    "shooting_3p":  0.017859482829247056 - O56,
    "shooting_2p_hi": 0.01785946863296317 - O56,
    "spectral_164": 0.017859307919207187 - O56,
    "high_166":     0.01786159799 - O56,
}
print("=== eps values (dinf - 1/56) ===")
for k, v in eps_vals.items():
    print("  %-16s eps=%.9e  (dinf=%.12f)" % (k, v, O56 + v))

# ---- Task A: 223 four delta points vs mirror zero-param model ----
# delta(m) = 1/56 - 13/128/m - 41/2000*(1/m^2 - 1/m^3)  [locked C,D,E mirror]
sh = json.load(open(r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_phase102_p7_5e223_shooting_dinf_closure.json", encoding="utf-8"))
ms = sh["m"]; ds = [sh["out"]["-%d" % m]["delta"] for m in ms]
C = 13.0/128.0; Dc = 41.0/2000.0
res = []
for m, d in zip(ms, ds):
    pred = O56 - C/float(m) - Dc*(1.0/float(m)**2 - 1.0/float(m)**3)
    res.append(d - pred)
print("\n=== Task A: 223 4-point residuals vs mirror model (C=13/128,D=41/2000,E=D) ===")
for m, d, r in zip(ms, ds, res):
    print("  m=%4d  delta=%.12f  mirror_pred=%.12f  resid=%+.3e" % (m, d, d - r, r))
print("  residual sequence sign/magnitude:", ["%+.1e" % r for r in res])
# fit constant eps to these residuals (least squares over 4 points)
eps_fit = sum(res)/len(res)
rms_const = math.sqrt(sum((r - eps_fit)**2 for r in res)/len(res))
# linear-in-m residual trend fit: r = eps + k*(m-320)
import numpy as np
A = np.array([[1.0, m-320.0] for m in ms]); b = np.array(res)
coef, *_ = np.linalg.lstsq(A, b, rcond=None)
pred_trend = A @ coef
rms_trend = math.sqrt(float(np.mean((b - pred_trend)**2)))
print("  constant-eps fit: eps=%.3e  RMS=%.3e" % (eps_fit, rms_const))
print("  linear-trend fit: eps=%.3e k=%.3e  RMS=%.3e  (k!=0 => eps is NOT a pure constant)" % (coef[0], coef[1], rms_trend))
print("  verdict A: k=%.3e ; |k|*range(384)~%.3e vs eps %.3e -> %s" % (
    coef[1], abs(coef[1])*384.0, eps_fit,
    "eps absorbed range effect (D/E high-order), 1/56 exact NOT excluded" if abs(coef[1])*384.0 > 0.5*abs(eps_fit) else "eps approx constant at 4-point resolution"))

# ---- Task B: framework-constant combination search ----
# candidate families: eps = 1/(b*2^a) ; eps = 1/(b*2^a*c) ; eps/dinf ~ 1/N ; telescope 1/(7*2^n)-1/(7*2^(n+1)) = 1/(7*2^(n+1))
base = [3,5,7,8,9,10,13,14,21,25,28,32,41,49,56,57,63,64,65,127,128,129,193,200,600,2000,4096,65536]
cset = [1,3,5,7,8,9,13,41,65]
hits = []
for name, eps in eps_vals.items():
    for b in base:
        for a in range(1, 21):
            cand = 1.0/(float(b) * (2**a))
            rel = (cand - eps)/eps
            if abs(rel) < 0.02:
                hits.append((abs(rel), name, "1/(%d*2^%d)=%.6e" % (b, a, cand), rel))
            for c in cset:
                cand2 = 1.0/(float(b) * (2**a) * float(c))
                rel2 = (cand2 - eps)/eps
                if abs(rel2) < 0.02:
                    hits.append((abs(rel2), name, "1/(%d*2^%d*%d)=%.6e" % (b, a, c, cand2), rel2))
    # eps/dinf ratio
    for N in [2**a for a in range(4, 18)] + [1000, 2000, 4000, 7631, 7671, 427360//56, 427360, 3640]:
        rel3 = ((1.0/N) - eps/O56)/(eps/O56)
        if abs(rel3) < 0.02:
            hits.append((abs(rel3), name, "eps/dinf ~ 1/%d (%.4e)" % (N, 1.0/N), rel3))
    # telescope family
    for n in range(10, 20):
        cand4 = 1.0/(7.0*2**(n+1))
        rel4 = (cand4 - eps)/eps
        if abs(rel4) < 0.02:
            hits.append((abs(rel4), name, "telescope 1/(7*2^%d)=%.6e" % (n+1, cand4), rel4))

hits.sort(key=lambda x: x[0])
print("\n=== Task B: candidate hits (|rel| < 2%) ===")
if not hits:
    print("  (none)")
for h in hits[:40]:
    print("  |rel|=%.2e  %-16s %-28s rel=%+.3e" % (h[0], h[1], h[2], h[3]))

# focused: the two closest families mentioned in analysis
print("\n=== focused candidates ===")
for name, eps in eps_vals.items():
    for label, cand in [("1/(13*2^15)", 1.0/(13*32768)), ("1/(7*2^16)", 1.0/(7*65536)),
                        ("1/(7*2^15)", 1.0/(7*32768)), ("1/(56*2^13)", 1.0/(56*8192)),
                        ("1/(65*2^13)", 1.0/(65*8192)), ("1/(41*2^13)", 1.0/(41*8192)),
                        ("1/(128*2^12)", 1.0/(128*4096)), ("1/(9*2^15)", 1.0/(9*32768)),
                        ("1/(57*2^13)", 1.0/(57*8192)), ("1/(127*2^12)", 1.0/(127*4096))]:
        rel = (cand - eps)/eps
        print("  %-16s %-16s cand=%.6e rel=%+.3e" % (name, label, cand, rel))

# Task C: eps identity relative to locked constants
print("\n=== Task C: eps vs locked constants ===")
for name, eps in eps_vals.items():
    for lab, val in [("C^2/2^?", (13.0/128.0)**2), ("D/2^13", 0.0205/8192.0),
                     ("1/56/2^12", O56/4096.0), ("1/56/2^13", O56/8192.0),
                     ("C*D/2^7", (13.0/128.0)*(41.0/2000.0)/128.0),
                     ("(1/56)*(1/65)/?", O56/65.0/4.0), ("1/(56*65)", O56/65.0)]:
        rel = (val - eps)/eps
        flag = " <1%" if abs(rel) < 0.01 else (" <5%" if abs(rel) < 0.05 else "")
        print("  %-16s %-16s val=%.6e rel=%+.3e %s" % (name, lab, val, rel, flag))

out = {"eps_values": {k: v for k, v in eps_vals.items()},
       "taskA": {"residuals": res, "eps_const_fit": eps_fit, "rms_const": rms_const,
                 "eps_trend": float(coef[0]), "k_trend": float(coef[1]), "rms_trend": rms_trend},
       "hits_top": [{"name": h[1], "expr": h[2], "rel": h[3]} for h in hits[:20]]}
with open(r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_phase102_p7_5e224_eps_identity.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("\nJSON dumped OK (exit 0)")
