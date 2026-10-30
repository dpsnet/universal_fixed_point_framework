# -*- coding: utf-8 -*-
# P7-5e-225: E = +41/2000 focus discriminant (statistical lock attempt)
# Data: 175 (m=33..1009 step16, 62pt) + 176 (m=17..127 step2, 56pt) merged.
# Models: M0 mirror zero-param (delta=1/56 - C/m - D(1/m^2-1/m^3), C=13/128, D=41/2000);
#         M1 E-free single param (delta=1/56 - C/m - D/m^2 + E/m^3);
#         M2 full-free {C,D,E,F};
# Windows: 中文 pct 字面统一用 "pct" 占位输出避免格式串问题（本脚本无格式串）。
import json, math, random, sys
import numpy as np

sys.set_int_max_str_digits(0)
random.seed(20261016)

d175 = json.load(open(r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_phase102_p7_5e175_delta63.json", encoding="utf-8"))
d176 = json.load(open(r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_phase102_p7_5e176_delta_lowm.json", encoding="utf-8"))
ms = list(d175["m"]) + list(d176["m"])
ds = list(d175["delta"]) + list(d176["delta"])
data = sorted(zip(ms, ds))
# dedupe (m=33..127 appear in both)
seen = {}
for m, d in data:
    if m not in seen:
        seen[m] = d
ms_all = sorted(seen); ds_all = [seen[m] for m in ms_all]
print("merged points: %d, range m=%d..%d" % (len(ms_all), ms_all[0], ms_all[-1]))

O56 = 1.0/56.0
C0 = 13.0/128.0
D0 = 41.0/2000.0

def rms(pred, obs):
    return math.sqrt(float(np.mean((np.array(pred) - np.array(obs))**2)))

def fit_E(ms, ds, C=C0, D=D0):
    # M1: delta = 1/56 - C/m - D/m^2 + E/m^3  ->  solve linear E
    A = np.array([1.0/m**3 for m in ms])
    y = np.array([d - O56 + C/m + D/m**2 for d, m in zip(ds, ms)])
    E_opt = float(np.sum(A*y)/np.sum(A*A))
    pred = [O56 - C/m - D/m**2 + E_opt/m**3 for m in ms]
    return E_opt, rms(pred, ds)

def fit_full(ms, ds):
    # M2: delta = 1/56 - C/m - D/m^2 + E/m^3 + F/m^4, free {C,D,E,F}
    X = np.array([[1.0/m, 1.0/m**2, 1.0/m**3, 1.0/m**4] for m in ms])
    y = np.array([d - O56 for d in ds])
    coef, res, rank, sv = np.linalg.lstsq(X, y, rcond=None)
    pred = O56 + X @ coef
    return -float(coef[0]), float(coef[1]), float(coef[2]), float(coef[3]), rms(pred, ds)

def mirror_rms(ms, ds):
    pred = [O56 - C0/m - D0*(1.0/m**2 - 1.0/m**3) for m in ms]
    return rms(pred, ds)

# windows
windows = {
    "33..96":   [m for m in ms_all if 33 <= m <= 96],
    "33..128":  [m for m in ms_all if 33 <= m <= 128],
    "33..192":  [m for m in ms_all if 33 <= m <= 192],
    "33..256":  [m for m in ms_all if 33 <= m <= 256],
    "33..512":  [m for m in ms_all if 33 <= m <= 512],
    "33..1009": ms_all,
}
print("\n=== E-opt windows (M1: C,D fixed, E free) ===")
res_w = {}
for wname, wms in windows.items():
    wds = [seen[m] for m in wms]
    E_opt, r1 = fit_E(wms, wds)
    r0 = mirror_rms(wms, wds)
    res_w[wname] = {"n": len(wms), "E_opt": E_opt, "rms_mirror": r0, "rms_Efree": r1,
                    "rms_ratio": r0/r1 if r1 > 0 else float("inf"),
                    "E_vs_41o2000_pct": (E_opt - 0.0205)/0.0205*100.0}
    print("  %-10s n=%3d  E_opt=%+.6f  rms_mirror=%.3e  rms_Efree=%.3e  ratio=%.2f  E-vs-41o2000=%+.2f pct"
          % (wname, len(wms), E_opt, r0, r1, r0/r1 if r1>0 else float("inf"), (E_opt-0.0205)/0.0205*100.0))

print("\n=== M2 full-free windows ===")
res_w2 = {}
for wname, wms in windows.items():
    wds = [seen[m] for m in wms]
    C_f, D_f, E_f, F_f, r2 = fit_full(wms, wds)
    res_w2[wname] = {"C": C_f, "D": D_f, "E": E_f, "F": F_f, "rms": r2}
    print("  %-10s n=%3d  C=%+.6f D=%+.6f E=%+.6f F=%+.4f  rms=%.3e"
          % (wname, len(wms), C_f, D_f, E_f, F_f, r2))

# bootstrap on 33..128 (M1)
wms = [m for m in ms_all if 33 <= m <= 128]
wds = [seen[m] for m in wms]
n = len(wms)
Es = []
for _ in range(2000):
    idx = [random.randrange(n) for _ in range(n)]
    sm = [wms[i] for i in idx]; sd = [wds[i] for i in idx]
    E_opt, _ = fit_E(sm, sd)
    Es.append(E_opt)
Es = np.array(Es)
E_mean = float(np.mean(Es)); E_std = float(np.std(Es, ddof=1))
z = (E_mean - 0.0205)/E_std
print("\n=== bootstrap E (33..128, M1, 2000x) ===")
print("  E_mean=%.6f  E_std=%.6f  z-vs-41o2000=%.2f  CI95=[%.5f, %.5f]"
      % (E_mean, E_std, z, np.percentile(Es, 2.5), np.percentile(Es, 97.5)))
print("  P(E>0.0205) = %.4f" % float(np.mean(Es > 0.0205)))

# discriminant power: model difference delta = (1/2000)*(1/m^3) between E=41/2000 vs E=0.0199
# at m=33: (0.0205-0.0199)/33^3 = 6e-4/35937 = 1.67e-8 vs noise ~ rms/sqrt(n)?
print("\n=== discriminant power ===")
for m in [33, 37, 41, 49, 65, 97, 129]:
    dE = 0.0205 - 0.0199
    delta = dE/m**3
    # noise estimate from Efree residual at 33..128
    print("  m=%3d  model-diff=%.2e  vs rms_m1(33..128)=%.1e -> SNR=%.2f"
          % (m, delta, res_w["33..128"]["rms_Efree"], delta/res_w["33..128"]["rms_Efree"]))

out = {"windows_M1": res_w, "windows_M2": res_w2,
       "bootstrap": {"n": n, "mean": E_mean, "std": E_std, "z_vs_41o2000": z,
                     "ci95": [float(np.percentile(Es, 2.5)), float(np.percentile(Es, 97.5))],
                     "p_E_gt_41o2000": float(np.mean(Es > 0.0205))}}
with open(r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_phase102_p7_5e225_E_lock_focus.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("\nJSON dumped OK (exit 0)")
