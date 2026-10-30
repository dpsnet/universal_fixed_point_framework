# -*- coding: utf-8 -*-
"""
P7-5e-174: κ·m 真实结构终判——三提取通道并排拟合（含常数项基）
================================================================
172 判读"κ·m=伪影"基于 w 扫描，但 173b 显示真实 Newton 提取下 κ·m 效应
依然存在（m=512/1024 分别高 1.2e-6/2.5e-6 于无 κ 预言，κ≈2.4e-9）。
w=0.01 的 κ_eff→0 疑为窄窗自身 −2.3e-6 负偏差抵消真实 κ。
174：三组 delta（真实 Newton 17 点 / w=0.01 17 点 / w=0.0265 全链 992 点）
并排拟合【含常数项】的模型族，判别：
  - κ·m 是否在真实 Newton 数据中稳健（真实结构）或随通道消失（伪影）
  - C=13/128、D=103/5000 是否在三通道下命中
"""
import numpy as np, json, re

C13 = -13.0/128.0
Dcan = -103.0/5000.0
inv56 = 1.0/56.0

def fit(delta, ms, model):
    A = np.vstack(model(ms)).T
    c, _, _, _ = np.linalg.lstsq(A, delta, rcond=None)
    resid = delta - A@c
    return c, float(np.sqrt(np.mean(resid**2)))

# --- 数据源 1：真实 Newton（173b 输出）---
ms17 = np.arange(512, 1025, 32, dtype=float)
d_true = np.array([1.765995301e-02, 1.767170983e-02, 1.768216710e-02, 1.769153067e-02,
                   1.769996602e-02, 1.770760647e-02, 1.771455942e-02, 1.772091199e-02,
                   1.772674474e-02, 1.773211527e-02, 1.773707981e-02, 1.774167870e-02,
                   1.774595783e-02, 1.774994393e-02, 1.775367415e-02, 1.775716455e-02,
                   1.776044448e-02])
# --- 数据源 2：w=0.01（173 输出）---
d_w01 = np.array([1.765872461e-02, 1.767040493e-02, 1.768078629e-02, 1.769007381e-02,
                  1.769843245e-02, 1.770599467e-02, 1.771287084e-02, 1.771914887e-02,
                  1.772490352e-02, 1.773020037e-02, 1.773508341e-02, 1.773960555e-02,
                  1.774381469e-02, 1.774771892e-02, 1.775137333e-02, 1.775478385e-02,
                  1.775816508e-02])
# --- 数据源 3：w=0.0265 全链（170 JSON）---
j = json.load(open(r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_phase102_p7_5e170_spectral_m1024.json", encoding='utf-8'))
out = j["out"]
all_m = np.array([-m for m in range(33, 1025)], dtype=float)
all_d = np.array([out[str(m)]["delta"] for m in range(-33, -1025, -1)])
sel3 = (all_m >= 512) & (all_m % 32 == 0)
m3 = all_m[sel3]; d3 = all_d[sel3]
selA = all_m >= 512

models = {
    "1+C/m+D/m²":        lambda m: [np.ones_like(m), 1.0/m, 1.0/m**2],
    "1+C/m+D/m²+κ·m":    lambda m: [np.ones_like(m), 1.0/m, 1.0/m**2, m],
    "1+C/m+D/m²+E/m³+κ·m": lambda m: [np.ones_like(m), 1.0/m, 1.0/m**2, 1.0/m**3, m],
    "1+C/m+D/m²+κ·m+F/m⁴": lambda m: [np.ones_like(m), 1.0/m, 1.0/m**2, m, 1.0/m**4],
}

def report(name, delta, ms):
    print("\n== %s ==" % name)
    for mn, bf in models.items():
        c, rms = fit(delta, ms, bf)
        txt = "  %-26s RMS=%.2e  C=%+.9f（13/128 差 %+.4f pct）  D=%+.6f（103/5000 差 %+.2f pct）" % (
            mn, rms, c[1], (c[1]-C13)/abs(C13)*100, c[2], (c[2]-Dcan)/abs(Dcan)*100)
        if len(c) >= 4 and mn != "1+C/m+D/m²":
            txt += "  κ=%+.3e" % c[3]
        if len(c) >= 5:
            txt += "  末=%+.4f" % c[4]
        print(txt)

report("真实 Newton（17 点）", d_true, ms17)
report("w=0.01（17 点）", d_w01, ms17)
report("w=0.0265（17 点，170 全链抽样）", d3, m3)
report("w=0.0265（全链 992 点）", all_d[selA], all_m[selA])

# 三通道 κ 对比（模型 1+C/m+D/m²+κ·m）
print("\n== κ·m 三通道对比（模型 1+C/m+D/m²+κ·m）==")
for name, delta, ms in [("真实 Newton", d_true, ms17), ("w=0.01", d_w01, ms17), ("w=0.0265(17p)", d3, m3), ("w=0.0265(992p)", all_d[selA], all_m[selA])]:
    c, rms = fit(delta, ms, models["1+C/m+D/m²+κ·m"])
    print("  %-16s C=%+.9f  D=%+.7f  κ=%+.4e  RMS=%.2e" % (name, c[1], c[2], c[3], rms))
print("exit 0", flush=True)
