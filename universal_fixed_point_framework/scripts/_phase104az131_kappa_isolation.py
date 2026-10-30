# -*- coding: utf-8 -*-
"""Phase 104az-131: kappa-Lambda endogenous candidate numerical isolation test.
Target: kappaL = 401.73304855 (identity-A caliber, #455)
Candidate: kappaL = 2*k_max*silence^2*(1+1/231) = 400*232/231 = 401.73160173, dev -0.00036%
Question: is the candidate numerically isolated? (upgrade-review strictness test)

A. Scan 400*(1+1/m) for m in [1, 2000]: which m hit |dev|<0.01% / <0.05%?
B. Scan 2*k*s^2*(1+1/231) for k,s in [1..32]: which (k,s) hit |dev|<0.01% / <0.05%?
C. Neighborhood of 231: 400*(1+1/m) for m in 228..235 (is 231 best-in-window?)
D. Alternative frame combos near 400: k^2*s, k*s^2, k^3 etc with 232/231 factor
E. Without the (1+1/231) correction: is 400 itself rejected (dev -0.431%)?
"""
import json

KAPPA = 401.73304855
R = 232.0 / 231.0

def dev(v):
    return (v - KAPPA) / KAPPA

out = {}

# A. 400(1+1/m)
hitsA = []
for m in range(1, 2001):
    v = 400.0 * (1.0 + 1.0 / m)
    d = dev(v)
    if abs(d) < 5.0e-4:  # 0.05% window
        hitsA.append({"m": m, "v": round(v, 10), "dev_ppm": round(d * 1e6, 3)})
out["A_count_0.05pct"] = len(hitsA)
out["A_first_60"] = hitsA[:60]
# strict 0.01% window
hitsA_strict = [h for h in hitsA if abs(h["dev_ppm"]) < 100.0]
out["A_count_0.01pct"] = len(hitsA_strict)
out["A_strict"] = hitsA_strict

# B. 2*k*s^2*(232/231)
hitsB = []
for k in range(1, 33):
    for s in range(1, 33):
        v = 2.0 * k * s * s * R
        d = dev(v)
        if abs(d) < 5.0e-4:
            hitsB.append({"k": k, "s": s, "v": round(v, 10), "dev_ppm": round(d * 1e6, 3)})
out["B_count_0.05pct"] = len(hitsB)
out["B_all"] = hitsB
hitsB_strict = [h for h in hitsB if abs(h["dev_ppm"]) < 100.0]
out["B_count_0.01pct"] = len(hitsB_strict)
out["B_strict"] = hitsB_strict

# C. 231 neighborhood
hitsC = []
for m in range(226, 237):
    v = 400.0 * (1.0 + 1.0 / m)
    d = dev(v)
    hitsC.append({"m": m, "v": round(v, 10), "dev_ppm": round(d * 1e6, 3)})
out["C_neighborhood"] = hitsC

# D. frame combos near 400 with R factor: k^2*s, k*s^2, k^3, k^2+s^2-based
hitsD = []
for k in range(1, 41):
    for s in range(1, 41):
        for form, v in [("k2s", k * k * s * R), ("ks2", k * s * s * R), ("k3", k * k * k * R), ("k2s2", k * k * s * s * R)]:
            d = dev(v)
            if abs(d) < 5.0e-4:
                hitsD.append({"form": form, "k": k, "s": s, "v": round(v, 10), "dev_ppm": round(d * 1e6, 3)})
out["D_count_0.05pct"] = len(hitsD)
out["D_all"] = hitsD[:80]
hitsD_strict = [h for h in hitsD if abs(h["dev_ppm"]) < 100.0]
out["D_count_0.01pct"] = len(hitsD_strict)
out["D_strict"] = hitsD_strict

# E. uncorrected 400
out["E_uncorrected_400_dev_ppm"] = round(dev(400.0) * 1e6, 3)
# candidate itself
out["E_candidate_dev_ppm"] = round(dev(400.0 * R) * 1e6, 3)

with open(r"C:\Users\dps_n\AppData\Local\DoubaoWork\User Data\Profile 6\.doubaowork\agent_mode\workspace\out_131.txt", "w", encoding="utf-8") as f:
    f.write(json.dumps(out, indent=1, ensure_ascii=False))
print("written")
