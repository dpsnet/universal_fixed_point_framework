# -*- coding: utf-8 -*-
"""P7-5e-180: E 的 x* 过零位移 δ4 通道判别（方向 ③ 续）
δ4（x* 的 1/m^4 系数）是 E 的线性函数：
  1/B* = n/x* 展开 1/m^3 系数 = -E = -δ4/4 + αγ/4 + β²/8 - 3α²β/8 + α⁴/16
  → E_back = (δ4 + 4·(-αγ/4 - β²/8 + 3α²β/8 - α⁴/16)... 见下
直接从 δ 闭式推导：
  x* = n/(cl-δ), 1/B* = cl-δ = n/2 + 1/8 + C/n + D/n² - E/n³ - F4/n⁴ + ...
  x* 1/n^4 系数 δ4 = -4E + 2D + 8C² - 3C/4 + 1/128（E 为 1/B* 口径，带符号）
  → E_back(1/B*) = -(δ4 - 2D - 8C² + 3C/4 - 1/128)/4
  δ 口径 E_δ = -E_back(1/B*)（1/B* = cl-δ，1/m³ 系数 = -E_δ）
判别目标：δ 口径 E_δ = +41/2000 (0.0205, 镜像结构) vs 178e 最优估计 +0.0199±0.0004
"""
import json, os, sys
import numpy as np

SCRIPTS = os.path.dirname(os.path.abspath(__file__))
OUT_TXT = os.path.join(SCRIPTS, "_phase102_p7_5e180_out.txt")
OUT_JSON = os.path.join(SCRIPTS, "_phase102_p7_5e180_delta4.json")

C = 13.0/128.0          # 锁定
D = 41.0/2000.0         # 锁定（5 通道）
ALPHA = -0.5            # 锁定
BETA = -9.0/32.0        # 锁定
GAMMA_LOCK = 0.089875   # γ_pred(41/2000) = 2C - 4D - 1/32

def load_delta(fn):
    dj = json.load(open(os.path.join(SCRIPTS, fn), encoding="utf-8"))
    return np.array(dj["m"]), np.array(dj["delta"])

m1, d1 = load_delta("_phase102_p7_5e175_delta63.json")
m2, d2 = load_delta("_phase102_p7_5e176_delta_lowm.json")
m = np.concatenate([m1, m2]); dl = np.concatenate([d1, d2])
order = np.argsort(m); m, dl = m[order], dl[order]
uniq = np.unique(m, return_index=True)[1]; m, dl = m[uniq], dl[uniq]
n = m
cl = n/2.0 + 1.0/7.0 + 1.0/(7.0*2.0**n)
x = n / (cl - dl)

def P(s):
    print(s)
    with open(OUT_TXT, "a", encoding="utf-8") as f:
        f.write(s + "\n")

open(OUT_TXT, "w", encoding="utf-8").close()

P("="*90)
P("P7-5e-180: E 的 x* 过零位移 δ4 通道判别")
P(f"数据：{len(m)} 点（m=17..1009）；x* = n/(cl−δ)（175+176 delta 重建）")
P(f"已锁：α=−1/2、β=−9/32、C=13/128、D=41/2000、γ_pred=+0.089875")
P(f"映射：δ4 = -4E + 2D + 8C² − 3C/4 + 1/128 → E_back(1/B*) = -(δ4 − 2D − 8C² + 3C/4 − 1/128)/4；δ 口径 E_δ = -E_back(1/B*)")
P("="*90)

# ---------- 方案 A：固定 γ=γ_pred，双参拟合 {δ4, ε5} ----------
def fit_window(lo, hi, tag, free_gamma=False):
    s = (n>=lo)&(n<hi)
    nn, xx = n[s], x[s]
    if free_gamma:
        # 三参 {γ, δ4, ε5}
        A = np.column_stack([1.0/nn**3, 1.0/nn**4, 1.0/nn**5])
        y = xx - 2.0 - ALPHA/nn - BETA/nn**2
        coef, res, rank, sv = np.linalg.lstsq(A, y, rcond=None)
        gam, d4, e5 = coef
        yf = A@coef
        rms = np.sqrt(np.mean((y-yf)**2))
        P(f"  {tag:10s} N={s.sum():3d}  γ={gam:+.8f}  δ4={d4:+.6f}  ε5={e5:+.4f}  RMS={rms:.2e}")
        return gam, d4
    else:
        # 固定 γ：双参 {δ4, ε5}
        A = np.column_stack([1.0/nn**4, 1.0/nn**5])
        y = xx - 2.0 - ALPHA/nn - BETA/nn**2 - GAMMA_LOCK/nn**3
        coef, res, rank, sv = np.linalg.lstsq(A, y, rcond=None)
        d4, e5 = coef
        yf = A@coef
        rms = np.sqrt(np.mean((y-yf)**2))
        P(f"  {tag:10s} N={s.sum():3d}  γ=固定0.089875  δ4={d4:+.6f}  ε5={e5:+.4f}  RMS={rms:.2e}")
        return GAMMA_LOCK, d4

P("\n[方案 A] 固定 γ=γ_pred=0.089875，双参 {δ4, ε5}（r4=(x*−2−α/n−β/n²−γ/n³)·n⁴ = δ4 + ε5/n）")
P("-"*90)
resA = {}
for lo, hi, tag in [(33,65,"33..64"), (65,129,"65..128"), (129,257,"129..256"),
                    (33,129,"33..128"), (33,257,"33..256"), (33,513,"33..512")]:
    g, d4 = fit_window(lo, hi, tag, free_gamma=False)
    resA[tag] = d4
    E_1B = -(d4 - 2*D - 8*C**2 + 3*C/4 - 1.0/128.0)/4.0   # 1/B* 口径
    E_d = -E_1B                                            # δ 口径
    P(f"      → E_back(δ口径) = {E_d:+.8f}（41/2000={41/2000:.8f} 差 {(E_d-41/2000)/(41/2000)*100:+.2f}%；178e 0.0199 差 {(E_d-0.0199)/0.0199*100:+.2f}%）")

P("\n[方案 B] 自由 γ（三参 {γ, δ4, ε5}——γ 窗口一致性检查 + δ4 去耦合）")
P("-"*90)
resB = {}
for lo, hi, tag in [(33,65,"33..64"), (65,129,"65..128"), (129,257,"129..256"),
                    (33,129,"33..128"), (33,257,"33..256"), (33,513,"33..512")]:
    g, d4 = fit_window(lo, hi, tag, free_gamma=True)
    resB[tag] = d4
    E_1B = -(d4 - 2*D - 8*C**2 + 3*C/4 - 1.0/128.0)/4.0   # 1/B* 口径
    E_d = -E_1B                                            # δ 口径
    P(f"      → E_back(δ口径) = {E_d:+.8f}（41/2000 差 {(E_d-41/2000)/(41/2000)*100:+.2f}%；178e 0.0199 差 {(E_d-0.0199)/0.0199*100:+.2f}%）")

# ---------- 判别 ----------
P("\n[判别]")
P("-"*90)
d4_bestA = resA["33..128"]
d4_bestB = resB["33..128"]
E_A = -(d4_bestA - 2*D - 8*C**2 + 3*C/4 - 1.0/128.0)/4.0   # 1/B* 口径
E_B = -(d4_bestB - 2*D - 8*C**2 + 3*C/4 - 1.0/128.0)/4.0
E_A_d, E_B_d = -E_A, -E_B   # δ 口径
d4s = list(resA.values())
spread = max(d4s)-min(d4s)
dE = spread/4.0
P(f"  方案 A 最优窗口(33..128) δ4={d4_bestA:+.6f} → E_back(δ口径) = {E_A_d:+.6f}")
P(f"  方案 B 最优窗口(33..128) δ4={d4_bestB:+.6f} → E_back(δ口径) = {E_B_d:+.6f}")
P(f"  δ4 窗口散布 = {spread:.2e} → E 不确定度 ≈ ±{dE:.2e}（ΔE_候选 = 41/2000−0.0199 = {41/2000-0.0199:.2e}）")
if dE < abs(41/2000-0.0199):
    P(f"  ★ 分辨率足够：E 不确定度 < 候选差 → δ4 通道可判别")
else:
    P(f"  ✗ 分辨率不足：E 不确定度 > 候选差 → δ4 通道不可判别（与 177c 同病）")
P(f"  判别结论：E_back(δ口径) ≈ {E_B_d:+.4f}（方案 B 自由 γ 去耦合）vs 41/2000=+0.0205 vs 178e=+0.0199±0.0004")
P(f"  注：δ4 公式不含 γ（δ4 = -4E+2D+8C²−3C/4+1/128）→ δ4 通道对 γ 免疫；方案 A/B 差来自 γ 固定误差经 ε5 传导")

json.dump({"resA": resA, "resB": resB, "E_A_1B": E_A, "E_B_1B": E_B,
           "E_A_delta": E_A_d, "E_B_delta": E_B_d,
           "d4_spread": spread, "dE": dE},
          open(OUT_JSON, "w", encoding="utf-8"), indent=1)
P(f"\nJSON 落盘 OK")
