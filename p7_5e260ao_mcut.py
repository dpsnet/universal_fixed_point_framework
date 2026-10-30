# -*- coding: utf-8 -*-
"""P7-5e-260ao：① u²/m³=7/2048 档位通道验证——m_cut 扫描 + 分段命中检查
关键问题：7/2048 是低档 m=32 单点驱动，还是低档段共同支持？"""
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

print("=== P7-5e-260ao 档位通道验证 ===", flush=True)

T72 = 7.0/2048.0

def fit_u2(xm, mm, ym):
    rr = ym - f_model(xm) - g_inf(xm)/mm - H2_LOCK/mm**2
    AA = build_cols(xm, mm, M23)
    cc, *_ = np.linalg.lstsq(AA, rr, rcond=None)
    idx = {n: i for i, n in enumerate(M23)}
    return float(cc[idx["u2/m3"]])

print("\n① m_cut 扫描（u²/m³ 系数，窗口 full）：", flush=True)
cuts = [32, 40, 48, 56, 64, 72, 80, 88, 96, 112, 128, 144, 192]
for mc in cuts:
    m_ = m_all >= mc
    v = fit_u2(x_all[m_], m_all[m_], y_all[m_])
    print("  m>=%4d: %+.9f（vs 7/2048 差 %+.3f%%）" % (mc, v, (v-T72)/abs(T72)*100), flush=True)

print("\n② 段内单独拟合：", flush=True)
segs = [("m∈[32,64]", 32, 64), ("m∈[32,96]", 32, 96), ("m∈[64,128]", 64, 128),
        ("m∈[64,256]", 64, 256), ("m∈[96,256]", 96, 256), ("m∈[128,512]", 128, 512)]
for nm, lo, hi in segs:
    m_ = (m_all >= lo) & (m_all <= hi)
    v = fit_u2(x_all[m_], m_all[m_], y_all[m_])
    print("  %-12s (n=%3d): %+.9f（vs 7/2048 差 %+.3f%%）" % (nm, m_.sum(), v, (v-T72)/abs(T72)*100), flush=True)

print("\n③ 去低档检验（低档支持是否单点驱动）：", flush=True)
for excl in [32, 40, 48, 56]:
    m_ = m_all > excl
    v = fit_u2(x_all[m_], m_all[m_], y_all[m_])
    print("  去 m<=%d（m>%d，n=%d）: %+.9f（vs 7/2048 差 %+.3f%%）" % (excl, excl, m_.sum(), v, (v-T72)/abs(T72)*100), flush=True)

print("\nexit 0", flush=True)
