# -*- coding: utf-8 -*-
"""P7-5e-171b: 尾项形态系统拟合 + 166 协调检验（纯分析 170 数据）。
1) delta 通道模型拟合（m>=512）：线性尾 κ·m / m^{1/2} / ln(m) / 混合 vs 纯幂律基线
2) h(2) 残差 5 点模型判别：a/m + b/m^{1/4} vs a/m + b vs a/m + b·m^q
3) 166 协调：m>=256 纯幂律 5 参拟合的 RMS 与残差形态（线性指纹相关）
"""
import json, numpy as np, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
base = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"

d170 = json.load(open(base + r"\_phase102_p7_5e170_spectral_m1024.json", encoding='utf-8'))
d170b = json.load(open(base + r"\_phase102_p7_5e170b_h2_m1024.json", encoding='utf-8'))
out = d170["out"]
ms = sorted(int(k) for k in out.keys())
mm = np.array([-m for m in ms], dtype=float)
invB = 1.0/np.array([out[str(m)]["Bstar"] for m in ms], dtype=float)
delta = np.array([out[str(m)]["delta"] for m in ms], dtype=float)
inv56 = 1.0/56.0
c13 = 13.0/128.0

print("\n== 1) delta 通道尾项形态拟合（m>=512）==")
def fit_model(ms_, y, basis_fn, names):
    A = np.vstack(basis_fn(ms_)).T
    c, _, _, _ = np.linalg.lstsq(A, y, rcond=None)
    rms = float(np.sqrt(np.mean((A@c - y)**2)))
    return c, rms

ms_ = mm[mm >= 512]
d_ = delta[mm >= 512]
models = {
    "1/56+C/m+κ·m": (lambda m: [1.0/m, m], ["C","κ"]),
    "1/56+C/m+D/m²+κ·m": (lambda m: [1.0/m, 1.0/m**2, m], ["C","D","κ"]),
    "1/56+C/m+D/m²+E/m³+κ·m": (lambda m: [1.0/m, 1.0/m**2, 1.0/m**3, m], ["C","D","E","κ"]),
    "1/56+C/m+D/m²+E/m³+F/m⁴+κ·m": (lambda m: [1.0/m, 1.0/m**2, 1.0/m**3, 1.0/m**4, m], ["C","D","E","F","κ"]),
}
for name, (bf, _) in models.items():
    y_ = d_ - inv56
    c, rms = fit_model(ms_, y_, bf, [])
    print("  %-34s RMS=%.3e  C=%+.12f（13/128 差 %+.4f pct） D=%+.6f κ=%+.3e" % (
        name, rms, c[0], (c[0]+c13)/c13*100, c[1] if len(c)>1 else float('nan'), c[-1]))
# C=13/128 固定：残差 r = delta-(1/56-13/128/m)，尾项形态
r = d_ - (inv56 - c13/ms_)
for name, bf in [("κ·m", lambda m: [m]), ("κ·m+D/m²", lambda m: [m, 1.0/m**2]),
                 ("κ·m+D/m²+E/m³", lambda m: [m, 1.0/m**2, 1.0/m**3])]:
    c, rms = fit_model(ms_, r, bf, [])
    print("  C=13/128 固定残差拟合 %-16s RMS=%.3e  coef=%s（κ=%+.3e）" % (
        name, rms, np.array2string(c, precision=12, suppress_small=False), c[0]))

print("\n== 2) h(2) 残差 5 点模型判别 ==")
h2m = d170b["h2_m"]
ms_h = np.array(sorted(int(k) for k in h2m.keys()), dtype=float)
dres = np.array([h2m[str(int(m))] for m in ms_h], dtype=float) - 7.0/64.0
for name, bf in [
    ("a/m", lambda m: [1.0/m]),
    ("a/m+b", lambda m: [1.0/m, np.ones_like(m)]),
    ("a/m+b/m^1/4", lambda m: [1.0/m, 1.0/m**0.25]),
    ("a/m+b·ln(m)/m", lambda m: [1.0/m, np.log(m)/m]),
    ("a/m+b·m^q(q 自由)", None),
]:
    if bf is None:
        # 非线性：网格搜 q
        best = None
        for q in np.arange(-1.0, 1.01, 0.05):
            A = np.vstack([1.0/ms_h, ms_h**q]).T
            c, _, _, _ = np.linalg.lstsq(A, dres, rcond=None)
            rms = float(np.sqrt(np.mean((A@c - dres)**2)))
            if best is None or rms < best[1]:
                best = (c, rms, q)
        c, rms, q = best
        print("  %-28s RMS=%.2e  q=%.2f  coef=%s" % (name, rms, q, np.array2string(c, precision=6, suppress_small=True)))
        continue
    A = np.vstack(bf(ms_h)).T
    c, _, _, _ = np.linalg.lstsq(A, dres, rcond=None)
    rms = float(np.sqrt(np.mean((A@c - dres)**2)))
    print("  %-28s RMS=%.2e  coef=%s" % (name, rms, np.array2string(c, precision=6, suppress_small=True)))
# 尾段 3 点（512,1024 只有 2 点，用 256,512,1024）q 判别
ms_h3 = np.array([256, 512, 1024], dtype=float)
d3 = np.array([h2m[str(int(m))] for m in ms_h3], dtype=float) - 7.0/64.0
q3 = np.log(d3[2]/d3[1])/np.log(ms_h3[2]/ms_h3[1])
q32 = np.log(d3[1]/d3[0])/np.log(ms_h3[1]/ms_h3[0])
print("  256→512 斜率 %.3f；512→1024 斜率 %.3f" % (q32, q3))

print("\n== 3) 166 协调：m>=256 全链（含常数项基，与 166 一致）5 参拟合的 RMS 与残差线性指纹 ==")
for lo in [256, 384, 512, 640, 768]:
    sel = mm >= lo
    ms_ = mm[sel]; d_ = delta[sel]
    A = np.vstack([1.0/ms_**j for j in range(5)]).T   # j=0..4 含常数（166 口径）
    c, _, _, _ = np.linalg.lstsq(A, d_, rcond=None)
    resid = d_ - A@c
    rms = float(np.sqrt(np.mean(resid**2)))
    rho = np.corrcoef(resid, ms_)[0,1]
    print("  m>=%4d（%4d 点）5 参（含常数）RMS=%.3e  δ∞=%+.10f（abs_dev %.2e） 残差-线性 ρ=%.2f  max|r|=%.2e" % (
        lo, sel.sum(), rms, c[0]-inv56, abs(c[0]-inv56), rho, np.max(np.abs(resid))))
# 166 精确复现：d160 数据 m>=256 5 参
d160 = json.load(open(base + r"\_phase102_p7_5e160_spectral_m512.json", encoding='utf-8'))
out160 = d160["out"]
ms160 = np.arange(33, 513, dtype=float)
ds160 = np.array([out160[str(m)]["delta"] for m in range(-33, -513, -1)])
idx = ms160 >= 256
X = np.vstack([1.0/ms160[idx]**j for j in range(5)]).T
cc, _, _, _ = np.linalg.lstsq(X, ds160[idx], rcond=None)
rr = float(np.sqrt(np.mean((X@cc - ds160[idx])**2)))
print("  166 精确复现（d160，m>=256，5 参含常数）：δ∞=%+.10f（abs_dev %.2e） RMS=%.3e" % (
    cc[0]-inv56, abs(cc[0]-inv56), rr))
# 检验尾项在 256..512 的显著性：r(256..512) 形态
r_all = delta - (inv56 - c13/mm)
for mq in [256, 320, 384, 448, 512, 640, 768, 896, 1024]:
    idx = np.where(mm == mq)[0]
    if len(idx):
        print("  r(m=%4d) = %+.3e" % (mq, r_all[idx[0]]))
print("\n完成。")
