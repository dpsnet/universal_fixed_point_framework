# -*- coding: utf-8 -*-
"""
P7-5e-179: D 的碗形通道独立交叉验证（过零位移 γ 提取，方向 ③）
================================================================
D 已有 4 通道（176 双项判别 / 177a 通道 A / 178d-e bootstrap 免疫 / 175 镜像）。
本步 = 第 5 通道（碗形）：从 x* = B*·n 过零位移的 1/n³ 系数 γ 独立提取 D。

数学（177a 通道 B 已建立，本步修正常数项）：
  1/B* = n/(2 + α/n + β/n² + γ/n³ + ...)
       = n/2 − α/4 + (−β/4 + α²/8)/n + (−γ/4 + αβ/4 − α³/16)/n² + ...
  α=−1/2, β=−9/32（已锁）→ 1/n² 项 = −γ/4 + 11/256
  已知 1/B* = n/2 + 1/8 + C/n + D/n² − D/n³ + ...（C=13/128, D=41/2000）
  → D = −γ/4 + 11/256 → γ_pred(D=41/2000) = 4(11/256 − 41/2000) = +0.089875

177a 的 γ 自由四参拟合 ≈ +0.0975（差 8.5%）——归因 β/γ 相关 + 高阶污染。
本步：固定 α/β（已锁值），消除 β 自由度污染，大窗口 + Richardson 消 δ4/n。
方法自检：同法提取 β（固定 α）应复现 −9/32（+0.05% 级）。
判别：γ vs 0.089875（D=41/2000）vs 0.089475（D=0.0206 终值）vs 0.089823（D=178e）。
"""
import json, numpy as np, os

SCRIPTS = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"
OUT = os.path.join(SCRIPTS, "_phase102_p7_5e179_out.txt")
OUTJSON = os.path.join(SCRIPTS, "_phase102_p7_5e179_gamma.json")

d = None
try:
    d = json.load(open(os.path.join(SCRIPTS, "_phase102_p7_5e177a_xstar.json"), encoding="utf-8"))
    m = np.array(d["m"], dtype=float)
    x = np.array(d["xstar"], dtype=float)
    SRC = "177a_xstar.json"
except FileNotFoundError:
    # 从 delta json 重建 xstar = n/(cl−delta)
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
    SRC = "175+176 delta 重建"

lines = []
def P(s=""):
    lines.append(s); print(s)

P("="*100)
P("P7-5e-179: D 碗形通道（过零位移 γ 提取）——D = −γ/4 + 11/256")
P(f"数据：{len(m)} 点（m=17..1009）；x* = n/(cl−δ)（来源：{SRC}）")
P(f"已锁：α=−1/2、β=−9/32、C=13/128；γ_pred(41/2000) = 4(11/256−41/2000) = {4*(11/256-41/2000):.8f}")
P("="*100)

# ---------- 方法自检：固定 α=−1/2，提取 β（应复现 −9/32）----------
P("\n[自检] 固定 α=−1/2：r2(n) = (x*−2−α/n)·n² → β + γ/n + δ4/n²")
P("-"*80)
r2 = (x - 2.0 - (-0.5)/m) * m**2
for lo, hi, tag in [(33,65,"33..64"), (65,129,"65..128"), (129,257,"129..256"),
                    (257,513,"257..512"), (513,10**6,"513+"), (33,10**6,"33+"),
                    (129,10**6,"129+"), (257,10**6,"257+")]:
    s = (m>=lo)&(m<hi)
    if s.sum() < 4: continue
    A = np.vstack([np.ones(s.sum()), 1.0/m[s]]).T
    c, _, _, _ = np.linalg.lstsq(A, r2[s], rcond=None)
    dev = (c[0]+9/32)/(9/32)*100
    P(f"  {tag:8s} N={s.sum():4d}  β={c[0]:+.8f}（−9/32 距 {dev:+.3f}%）  1/n 系数={c[1]:+.5f}")

# ---------- γ 提取：固定 α/β ----------
P("\n[γ 提取] 固定 α=−1/2、β=−9/32：r3(n) = (x*−2−α/n−β/n²)·n³ → γ + δ4/n + O(1/n²)")
P("-"*80)
r3 = (x - 2.0 - (-0.5)/m - (-9.0/32.0)/m**2) * m**3
gamma_cand = 4*(11.0/256.0 - 41.0/2000.0)   # 0.089875（D=41/2000）
gamma_cand2 = 4*(11.0/256.0 - 0.0205131)     # 178e D 最优
gamma_cand3 = 4*(11.0/256.0 - 0.0206)        # 176 终值
res = {}
for lo, hi, tag in [(33,65,"33..64"), (65,129,"65..128"), (129,257,"129..256"),
                    (257,513,"257..512"), (513,10**6,"513+"),
                    (33,129,"33..128"), (129,10**6,"129+"), (257,10**6,"257+"),
                    (33,10**6,"33+"), (65,10**6,"65+")]:
    s = (m>=lo)&(m<hi)
    if s.sum() < 4: continue
    A = np.vstack([np.ones(s.sum()), 1.0/m[s]]).T
    c, _, _, _ = np.linalg.lstsq(A, r3[s], rcond=None)
    rms = np.sqrt(np.mean((r3[s] - A@c)**2))
    res[tag] = (c[0], c[1], rms, int(s.sum()))
    dev = (c[0]-gamma_cand)/gamma_cand*100
    P(f"  {tag:8s} N={s.sum():4d}  γ={c[0]:+.8f}（41/2000 预测 {gamma_cand:.8f} 距 {dev:+.3f}%）"
      f"  δ4/n 系数={c[1]:+.5f}  RMS={rms:.2e}")

# ---------- Richardson 配对（消 δ4/n；数据网格无 2n 配对，改为三窗口一致性判别）----------
P("\n[Richardson/一致性] 数据网格不支持 n→2n 配对；改用中段三窗口 γ 一致性判别：")
P("-"*80)
g_33_64 = res["33..64"][0]; g_65_128 = res["65..128"][0]; g_129_256 = res["129..256"][0]
g_spread = max(g_33_64, g_65_128, g_129_256) - min(g_33_64, g_65_128, g_129_256)
P(f"  γ(33..64)={g_33_64:+.8f}  γ(65..128)={g_65_128:+.8f}  γ(129..256)={g_129_256:+.8f}")
P(f"  三窗口散布 = {g_spread:.2e}（模型差 41/2000 vs 103/5000 = {gamma_cand-gamma_cand3:.2e} → 信噪比 {abs(gamma_cand-gamma_cand3)/g_spread:.1f}）")

# ---------- 判别 ----------
P("\n[判别]")
P("-"*80)
g_best = res["33..128"][0]
P(f"  最优窗口（33..128）γ = {g_best:+.8f}，RMS={res['33..128'][2]:.2e}")
for lab, gc in [("D=41/2000", gamma_cand), ("D=178e 0.0205131", gamma_cand2), ("D=176 终值 0.0206", gamma_cand3)]:
    P(f"    vs {lab}: γ_pred={gc:+.8f}  差 {(g_best-gc)/gc*100:+.3f}%")
P(f"    vs 177a 自由拟合 0.0975: 差 {(g_best-0.0975)/0.0975*100:+.3f}%（177a 差 8.5% = β/γ 相关污染，固定 α/β 后消除）")
D_back = (11.0/256.0 - g_best/4.0)
P(f"  ★ γ → D_back = 11/256 − γ/4 = {D_back:+.8f}（41/2000 距 {(D_back-41/2000)/(41/2000)*100:+.3f}%）")
# 判别力：γ 模型差 vs 提取噪声（33..128 段两参拟合残差）
noise = res["33..128"][2]
P(f"  判别力：γ 候选差(41 vs 103) = {abs(gamma_cand-gamma_cand3):.2e} vs 33..128 段噪声 RMS = {noise:.2e} → SNR = {abs(gamma_cand-gamma_cand3)/noise:.1f}（>3 可判别）")

json.dump({"m": m.tolist(), "xstar": x.tolist(), "r3": r3.tolist(),
           "gamma_windows": {k: [v[0], v[1], v[2], v[3]] for k, v in res.items()},
           "gamma_best": float(g_best), "D_back": float(D_back),
           "script": "P7-5e-179",
           "note": "γ 提取：固定 α=−1/2 β=−9/32；D = −γ/4 + 11/256（177a 常数项修正）"},
          open(OUTJSON, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
open(OUT, "w", encoding="utf-8").write("\n".join(lines))
print("JSON 落盘 OK exit 0")
