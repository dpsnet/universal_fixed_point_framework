# -*- coding: utf-8 -*-
"""
Phase 102 P7-5e-77：m=-8 通道消失的数值判别——r_max 扩展
================================================================
怀疑：m=-8 离心势 32/r² 把束缚态波函数推向大 r——r_max=60 截断可能误杀
判别：0.225/0.25 au 用 r_max = 80/100/120 重算 m=-8（及全部通道）
  (a) m=-8 恢复束缚 → 9 缺口是 r_max 伪影（负8正1=10 通道其实含被截断的 -8）
  (b) m=-8 仍消失 → 同步收缩是物理的——9 缺口真实
"""
import json, os, time
import numpy as np
from scipy.sparse import diags
from scipy.sparse.linalg import eigsh
import warnings
warnings.filterwarnings('ignore')

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"

def n_bound_m(N_r, r_max, m, B, k=300):
    dr = r_max / N_r
    j = np.arange(N_r)
    r = (j + 0.5) * dr
    off_diag = np.ones(N_r - 1) / (2.0 * dr ** 2)
    diag_main = np.ones(N_r) / dr ** 2
    landau_centrifugal = (m + 0.5 * B * r ** 2) ** 2 / (2.0 * r ** 2)
    coulomb = -1.0 / r
    H = diags([-off_diag, diag_main + landau_centrifugal + coulomb, -off_diag],
              offsets=[-1, 0, 1], shape=(N_r, N_r), format='csr')
    try:
        vals, _ = eigsh(H.astype(np.float64), k=min(k, N_r - 5),
                        which='SA', maxiter=50000, tol=1e-9)
        return int(np.sum(np.real(vals) < 0))
    except Exception:
        return 0

print("="*104)
print("P7-5e-77：m=-8 通道消失的数值判别——r_max 扩展（N_r=1500 固定、dr 随 r_max 变）")
print("="*104)

configs = [
    (0.225, 60), (0.225, 80), (0.225, 100), (0.225, 120),
    (0.25, 60),  (0.25, 80),  (0.25, 100),  (0.25, 120),
    (0.30, 60),  (0.30, 100),
]

results = {}
for B, r_max in configs:
    t0 = time.time()
    N_r = 1500
    Ns = {}
    for m in range(-8, 3):  # 关注负 8 与正侧
        Ns[m] = n_bound_m(N_r, r_max, m, B)
    nonzero = {m: n for m, n in Ns.items() if n > 0}
    neg = {m: n for m, n in Ns.items() if m < 0 and n > 0}
    pos = {m: n for m, n in Ns.items() if m > 0 and n > 0}
    key = "B=%.3f_r=%d" % (B, r_max)
    results[key] = {"n_total": sum(Ns.values()), "n_chan": len(nonzero),
                    "m_min": min(nonzero) if nonzero else None,
                    "m_max": max(nonzero) if nonzero else None,
                    "neg_m": [m for m in neg], "pos_m": [m for m in pos],
                    "N_m": {str(m): v for m, v in Ns.items()}}
    print("  B=%.3f au（%.1f MG）r_max=%d → n_total=%d 通道=%d（负%s 正%s，m_min=%s）[%.0fs]"
          % (B, B*2350, r_max, sum(Ns.values()), len(nonzero),
             str([m for m in neg]), str([m for m in pos]),
             min(nonzero) if nonzero else '-', time.time()-t0), flush=True)

print()
print("【判别】")
print("-"*104)
for B in [0.225, 0.25]:
    r60 = results["B=%.3f_r=%d" % (B, 60)]
    r120 = results["B=%.3f_r=%d" % (B, 120)]
    m8_60 = -8 in r60["N_m"] and r60["N_m"]["-8"] > 0
    m8_120 = -8 in r120["N_m"] and r120["N_m"]["-8"] > 0
    print("  B=%.3f au：r_max=60 时 m=-8 %s；r_max=120 时 m=-8 %s"
          % (B, "存活" if m8_60 else "消失", "存活" if m8_120 else "消失"))
    if not m8_60 and m8_120:
        print("    ★★ m=-8 随 r_max 恢复——9 缺口（负8正0）部分为 r_max 截断伪影！")
    elif not m8_60 and not m8_120:
        print("    ★ m=-8 不随 r_max 恢复——消失是物理的——9 缺口真实")

json.dump(results, open(os.path.join(BASE, "_phase102_p7_5e77_rmax_test.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("JSON 落盘 ✓  exit 0")
