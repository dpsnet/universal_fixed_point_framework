# -*- coding: utf-8 -*-
"""Phase 86 R2a：绝对标定链单星验证
1) DESI npz flux 单位与量级（是否 1e-17 erg/cm2/s/A 或绝对）
2) Gaia G 波段交叉校准因子
3) Koester 表面流量 x (R/d)^2 模型绝对流量 vs 观测
"""
import json, io, os, re
import numpy as np

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"
GAI = os.path.join(BASE, "_gaia_abs", "gaia_parallax_phot.json")

with io.open(GAI, "r", encoding="utf-8") as f:
    gai = json.load(f)["rows"]
with io.open(os.path.join(BASE, "paperX_wd_m83e_desi137.json"), "r", encoding="utf-8") as f:
    cat = {str(s["gaia_int"]): s for s in json.load(f)["samples"]}

# 选一颗命中星
gid = "1003378611740398336"  # B=3.56 Teff=10059 logg=8
print("星:", gid, "Gaia:", gai.get(gid))
s = cat[gid]
print("目录: B_MG=%.2f Teff=%.0f Mass=%.2f" % (s["B_MG"], s["Teff"], s["Mass"]))

d = np.load(os.path.join(BASE, "_desi_spec", gid + ".npz"), allow_pickle=True)
wl, fl, iv = d["wave"], d["flux"], d["ivar"]
print("DESI flux: min=%.3g max=%.3g median=%.3g (波段 3600-5800)" % (fl.min(), fl.max(), np.median(fl)))
print("  量级判断: 若 ~1e-17 量级为 1e-17 erg/cm2/s/A 单位")

# Gaia G 波段交叉：DESI flux 经 Gaia 响应卷积 vs Gaia G 测光
# 简化：用 4500-5500 Å DESI 平均流量 x 带宽估算 vs G 星等对应的通量密度
gmag = gai[gid]["g_mag"]
par = gai[gid]["parallax"]  # mas
d_pc = 1000.0 / par
print("距离: %.0f pc" % d_pc)

# 绝对流量密度：F_nu 与 mag 关系: F_nu = 10^(-0.4*(m + 48.60)) erg/cm2/s/Hz (Vega 零点)
# G 波段 ~ 5400 Å；F_lambda = F_nu * c/lambda^2
c = 2.998e18  # A/s
lam_g = 5400.0
fnu = 10 ** (-0.4 * (gmag + 48.60))
flam_g = fnu * c / lam_g ** 2
print("Gaia G -> F_lambda(5400A) = %.3g erg/cm2/s/A" % flam_g)

# DESI 在 5300-5500 平均
m = (wl >= 5300) & (wl <= 5500)
f_desi = np.median(fl[m])
print("DESI median(5300-5500) = %.3g -> 校准因子(FluxGaia/FluxDesi) = %.3f" % (f_desi, flam_g / f_desi))

# 模型绝对流量: F_surf x (R/d)^2
# 质量-半径: 0.6 Msun -> R=0.012 R_sun x (m/0.6)^(-1/3)（v10 log_g 同口径）
msun, rsun = 1.989e33, 6.96e10  # g, cm
m_s = s["Mass"]
x = min(m_s / 1.44, 0.99)
R_cm = 0.012 * (m_s / 0.6) ** (-1 / 3) * (1 - x ** (4 / 3)) ** 0.5 * rsun
d_cm = d_pc * 3.086e18
scale = (R_cm / d_cm) ** 2
print("R=%.3g cm, d=%.3g cm, (R/d)^2=%.3g" % (R_cm, d_cm, scale))

# 找 Koester 最近网格
def load_koester(teff, logg):
    best = None
    for fn in os.listdir(os.path.join(BASE, "_koester_spec")):
        mm = re.match(r"fid\d+_([\d.]+)_([\d.]+)\.dat", fn)
        if not mm:
            continue
        t, g = float(mm.group(1)), float(mm.group(2))
        score = (t - teff) ** 2 + (g - logg) ** 2
        if best is None or score < best[0]:
            best = (score, os.path.join(BASE, "_koester_spec", fn))
    arr = np.loadtxt(best[1])
    return arr[:, 0], arr[:, 1]

wlk, fk = load_koester(s["Teff"], s["logg"])
mk = (wlk >= 5300) & (wlk <= 5500)
f_model = np.median(fk[mk]) * scale
print("模型 F(5400A) x (R/d)^2 = %.3g  vs 观测 DESI %.3g / Gaia标定 %.3g" % (f_model, f_desi, f_desi * (flam_g / f_desi)))
