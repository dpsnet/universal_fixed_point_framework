# -*- coding: utf-8 -*-
"""Phase 104az-131b: structural uniqueness follow-up.
Q1: Restrict k,s to PURE frame constants {2,3,4,5,7,8} (seed-algebra core set).
    Is (k,s)=(8,5) the unique hit for 2*k*s^2*(232/231) ~ kappaL?
Q2: Symmetric-product family S(k)=(k/2-1)(k-1)(3k/2-1), k even.
    Is 231 = S(8) the unique member landing inside the neighborhood band
    [226..236] that achieves |dev|<100ppm for 400(1+1/m)?
Q3: Decompositions of 230/231/232: why 231 not 230/232?
    230 = 2*5*23 (23 prime, no symmetric product form)
    231 = (7-4)*7*(7+4) = S(8) symmetric product
    232 = 8*29 = 8*(7*4+1) (+1-family member but not symmetric product)
"""
import json

KAPPA = 401.73304855
R = 232.0 / 231.0

def dev(v):
    return (v - KAPPA) / KAPPA

out = {}

# Q1: pure frame set
FRAME = [2, 3, 4, 5, 7, 8]
hits = []
for k in FRAME:
    for s in FRAME:
        v = 2.0 * k * s * s * R
        d = dev(v)
        if abs(d) < 1.0e-3:
            hits.append({"k": k, "s": s, "v": round(v, 10), "dev_ppm": round(d * 1e6, 3)})
out["Q1_pure_frame_hits"] = hits
out["Q1_count"] = len(hits)
# also: what k*s^2 = 200 factorizations within FRAME (no R, exact 400 target)
facs = []
for k in FRAME:
    for s in FRAME:
        if k * s * s == 200:
            facs.append({"k": k, "s": s})
out["Q1_ks2_200_exact"] = facs

# Q2: S(k) family vs neighborhood band
band = set(range(226, 237))
sfam = {}
for k in [2, 4, 6, 8, 10, 12, 14, 16]:
    S = (k // 2 - 1) * (k - 1) * (3 * k // 2 - 1)
    sfam[k] = S
out["Q2_S_family"] = sfam
inband = {k: S for k, S in sfam.items() if S in band}
out["Q2_S_family_in_band"] = inband
# dev of each S member as 1/m correction
for k, S in sfam.items():
    if S >= 1:
        v = 400.0 * (1.0 + 1.0 / S)
        out.setdefault("Q2_S_devs", []).append({"k": k, "S": S, "dev_ppm": round(dev(v) * 1e6, 3)})

# Q3: decompositions
def factors(n):
    fs = []
    d = 2
    m = n
    while d * d <= m:
        while m % d == 0:
            fs.append(d)
            m //= d
        d += 1
    if m > 1:
        fs.append(m)
    return fs

out["Q3_230_factors"] = factors(230)
out["Q3_231_factors"] = factors(231)
out["Q3_232_factors"] = factors(232)
out["Q3_232_as_8x29"] = "232 = 8*29 = k_max*(involution_domain*fixed_point+1)"
out["Q3_231_symprod"] = "231 = (7-4)*7*(7+4) = (involution_domain-N_gen)*involution_domain*(involution_domain+N_gen)"
# 230/232 also in S-family? 230: k/2-1|k-1|3k/2-1 products; check membership by solving
sfam_vals = set(sfam.values())
out["Q3_230_in_S_family"] = 230 in sfam_vals
out["Q3_232_in_S_family"] = 232 in sfam_vals

with open(r"C:\Users\dps_n\AppData\Local\DoubaoWork\User Data\Profile 6\.doubaowork\agent_mode\workspace\out_131b.txt", "w", encoding="utf-8") as f:
    f.write(json.dumps(out, indent=1, ensure_ascii=False))
print("written")
