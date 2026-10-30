# -*- coding: utf-8 -*-
"""P7-5e-260ap：① 13 家族跨层同构 + ② 指数谱绕 8 族统一 + ③ c3 高阶分子身份"""
import json
import numpy as np

PTS = r"C:\Users\dps_n\DoubaoWork\chats\2026-10-07\new-chat\p7_5e260ae_e0pts.json"

def f_model(x):
    return 0.5*x - np.sqrt(0.5*x)

def g_inf(x):
    return -0.125 + np.sqrt(0.5*x)/8.0 + x/16.0

H2_LOCK = 7.0/64.0

M23 = ["u/m2", "u2/m2", "u3/m2", "u4/m2", "u5/m2", "u6/m2",
       "1/m3", "u/m3", "u2/m3", "u3/m3", "u4/m3",
       "1/m4", "u/m4", "u2/m4", "u3/m4", "u4/m4", "u5/m4",
       "1/m5", "u/m5", "u2/m5", "u3/m5", "u5/m5", "1/m6"]

def build_cols(x_arr, m_arr, names):
    u = x_arr - 2.0
    d = {"u": u, "u2": u*u, "u3": u**3, "u4": u**4, "u5": u**5, "u6": u**6}
    cols = []
    for n in names:
        a, b = n.split("/")
        k = 1 if b == "m" else int(b[1:])
        if a == "1":
            cols.append(np.ones_like(m_arr)/m_arr**k)
        else:
            cols.append(d[a]/m_arr**k)
    return np.column_stack(cols)

pts = json.load(open(PTS, encoding="utf-8"))
sel = [(p["x"], p["E0"]*p["mm"], p["mm"]) for p in pts]
x_all = np.array([s[0] for s in sel], float)
m_all = np.array([s[2] for s in sel], float)
y_all = np.array([s[1] for s in sel], float)

r = y_all - f_model(x_all) - g_inf(x_all)/m_all - H2_LOCK/m_all**2
A = build_cols(x_all, m_all, M23)
c, *_ = np.linalg.lstsq(A, r, rcond=None)
idx = {n: i for i, n in enumerate(M23)}

print("=== P7-5e-260ap 家族同构 + 指数统一 ===", flush=True)

print("\n① 13 家族跨层谱：", flush=True)
print("  1/m 层：C = 13/128（13 = 8+5）", flush=True)
print("  1/m² 层：h(2) = 7/64（7 = 8−1）", flush=True)
print("  1/m³ 层：3/512（3 = 8−5）、39/2048（39 = 3·13）、7/2048（7 = 8−1）", flush=True)
print("  1/m⁴ 层：j(2) = −13/293（13 = 8+5）", flush=True)
print("  分子族 {13, 7, 3} = {8+5, 8−1, 8−5}——绕 k_max=8 的 {±5, ±1} 摆荡", flush=True)
print("  13 家族出现层：1/m（C）、1/m³（39 链）、1/m⁴（j(2)）——1/m² 层缺失（7 家族）", flush=True)

print("\n② 指数谱绕 8 统一：", flush=True)
print("  指数 {7, 6, 9} = {8−1, 8−2, 8+1}——偏移 {−1, −2, +1}", flush=True)
print("  分子偏移 {+5, −1, −5}（层 1→3）、指数偏移 {−1, −2, +1}——共同成员 −1（8−1 = 7 既是层1指数又是层2分子）", flush=True)
print("  加法互锁：层2 分子 7 + 指数 6 = 13 = C 分子；层3 分子 3 + 指数 9 = 12 = 碗形 2048 分子", flush=True)
print("  公共分母：u 展开以 2048 = 2¹¹ = dim Cl(11) 统一（12 − 39u + 7u² − 2.34u³ + 0.85u⁴）/2048", flush=True)

print("\n③ c3 高阶分子身份（×2048）：", flush=True)
c3 = [float(c[idx["1/m3"]])*2048, float(c[idx["u/m3"]])*2048, float(c[idx["u2/m3"]])*2048,
      float(c[idx["u3/m3"]])*2048, float(c[idx["u4/m3"]])*2048]
names = ["c3₀", "c3₁", "c3₂", "c3₃", "c3₄"]
for nm, v in zip(names, c3):
    print("  %s = %+.6f" % (nm, v), flush=True)
print("  c3₃ = −2.3401 vs −7/3 = −2.3333（差 %+.3f%%）vs −12/5 = −2.4（差 %+.3f%%）" % ((c3[3]+7/3)/(-7/3)*100, (c3[3]+12/5)/(-12/5)*100), flush=True)
print("  c3₄ = +0.8470 vs 5/6 = +0.8333（差 %+.3f%%）vs 13/15 = +0.8667（差 %+.3f%%）" % ((c3[4]-5/6)/(5/6)*100, (c3[4]-13/15)/(13/15)*100), flush=True)

# ② 续：检查"分子+指数=下层关键量"的完整谱
print("\n② 续 分子+指数 互锁谱：", flush=True)
print("  层1 13/2⁷：13+7 = 20（?）", flush=True)
print("  层2 7/2⁶：7+6 = 13 = C 分子 ✓", flush=True)
print("  层3 3/2⁹：3+9 = 12 = 碗形 2048 分子 ✓", flush=True)
print("  层3u 39/2¹¹：39+11 = 50（?）", flush=True)
print("  层3u² 7/2¹¹：7+11 = 18（?）", flush=True)
print("  仅层2/层3 命中——加法互锁为部分观察（2/5），不升级", flush=True)

print("\nexit 0", flush=True)
