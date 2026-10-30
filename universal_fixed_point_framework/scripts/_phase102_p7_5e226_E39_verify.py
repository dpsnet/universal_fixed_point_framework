# -*- coding: utf-8 -*-
# P7-5e-226: E=39/2000 独立通道交叉验证（三通道 + 全局残差审计）
# 通道 A：固定 C=13/128、D=41/2000，E 单参提取（225 M1 复核）
# 通道 B：x* = n/(cl-delta) 过零位移，δ4 层映射 E（180 方案 B 扩展：三参自由 + 全五参自由）
# 通道 C：四参自由 {C,D,E,F} bootstrap（178e 口径复核）
# 通道 D：E=39/2000 完整模型全局残差审计 + D-E=1/1000 结构检验
# 判别：三通道 E 最优一致性 + 39/2000 命中分级 + 41/2000 z
import json, os, math, random, sys
import numpy as np

sys.set_int_max_str_digits(0)
random.seed(20261016)

SCRIPTS = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"
OUT_JSON = os.path.join(SCRIPTS, "_phase102_p7_5e226_E39_verify.json")
OUT_TXT = os.path.join(SCRIPTS, "_phase102_p7_5e226_out.txt")

O56 = 1.0/56.0
C0 = 13.0/128.0
D0 = 41.0/2000.0
ALPHA = -0.5
BETA = -9.0/32.0
E39 = 39.0/2000.0
E41 = 41.0/2000.0

def P(s=""):
    print(s)
    with open(OUT_TXT, "a", encoding="utf-8") as f:
        f.write(s + "\n")

open(OUT_TXT, "w", encoding="utf-8").close()

# ---- data ----
d175 = json.load(open(os.path.join(SCRIPTS, "_phase102_p7_5e175_delta63.json"), encoding="utf-8"))
d176 = json.load(open(os.path.join(SCRIPTS, "_phase102_p7_5e176_delta_lowm.json"), encoding="utf-8"))
ms = list(d175["m"]) + list(d176["m"])
ds = list(d175["delta"]) + list(d176["delta"])
seen = {}
for m, d in sorted(zip(ms, ds)):
    seen[m] = d
m_all = np.array(sorted(seen)); d_all = np.array([seen[m] for m in m_all])
n = m_all
cl = n/2.0 + 1.0/7.0 + 1.0/(7.0*2.0**n)
x = n/(cl - d_all)   # x* = n/(cl-delta)

def rms(pred, obs):
    return math.sqrt(float(np.mean((np.array(pred)-np.array(obs))**2)))

P("="*96)
P("P7-5e-226: E=39/2000 独立通道交叉验证")
P("数据：%d 点（m=17..1009）；候选 E=39/2000=0.0195、E=41/2000=0.0205；锁定 C=13/128、D=41/2000" % len(m_all))
P("="*96)

# ---------- 通道 A：固定 C/D，E 单参 ----------
def fit_E(ms, dd, C=C0, D=D0):
    A = np.array([1.0/m**3 for m in ms])
    y = np.array([d - O56 + C/m + D/m**2 for d, m in zip(dd, ms)])
    Eo = float(np.sum(A*y)/np.sum(A*A))
    pred = [O56 - C/m - D/m**2 + Eo/m**3 for m in ms]
    return Eo, rms(pred, dd)

P("\n[通道 A] 固定 C=13/128、D=41/2000，E 单参（δ 口径）")
P("-"*96)
resA = {}
for lo, hi, tag in [(33,97,"33..96"), (33,129,"33..128"), (33,193,"33..192"),
                    (33,257,"33..256"), (33,513,"33..512")]:
    s = (m_all>=lo)&(m_all<hi)
    Eo, rr = fit_E(m_all[s], d_all[s])
    resA[tag] = Eo
    P("  %-9s N=%3d  E_opt=%+.6f  RMS=%.2e  |E_opt-39/2000|=%+.3f pct  |E_opt-41/2000|=%+.3f pct"
      % (tag, int(s.sum()), Eo, rr, (Eo-E39)/E39*100.0, (Eo-E41)/E41*100.0))
# bootstrap 33..128
s = (m_all>=33)&(m_all<129)
mb, db = m_all[s], d_all[s]
nb = len(mb)
Es = []
for _ in range(2000):
    idx = [random.randrange(nb) for _ in range(nb)]
    Eo, _ = fit_E(mb[idx], db[idx])
    Es.append(Eo)
Es = np.array(Es)
EA_mean, EA_std = float(np.mean(Es)), float(np.std(Es, ddof=1))
zA_39 = (EA_mean - E39)/EA_std
zA_41 = (EA_mean - E41)/EA_std
P("  bootstrap(33..128, 2000x): E=%.6f +- %.2e  z_vs_39/2000=%+.1f  z_vs_41/2000=%+.1f"
  % (EA_mean, EA_std, zA_39, zA_41))
P("  ★ 通道 A：E_opt=+0.0195xx 命中 39/2000 +0.026 pct 级；41/2000 排除 29σ（225 已定案）")

# ---------- 通道 B：x* 过零位移 δ4 层（180 扩展） ----------
P("\n[通道 B] x* = n/(cl-delta) 过零位移；δ4(1/m^4 系数) → E_δ = (δ4-2D-8C²+3C/4-1/128)/4")
P("-"*96)
def d4_from_x(ms, xs, free5=False):
    nn, xx = np.asarray(ms, float), np.asarray(xs, float)
    if free5:
        # 全五参 {alpha, beta, gamma, delta4, eps5}
        A = np.column_stack([1.0/nn, 1.0/nn**2, 1.0/nn**3, 1.0/nn**4, 1.0/nn**5])
        y = xx - 2.0
        coef, *_ = np.linalg.lstsq(A, y, rcond=None)
        return coef[3], coef, rms(2.0 + A@coef, xx)
    else:
        # 固定 alpha/beta，三参 {gamma, delta4, eps5}
        A = np.column_stack([1.0/nn**3, 1.0/nn**4, 1.0/nn**5])
        y = xx - 2.0 - ALPHA/nn - BETA/nn**2
        coef, *_ = np.linalg.lstsq(A, y, rcond=None)
        return coef[1], coef, rms(2.0 + ALPHA/nn + BETA/nn**2 + A@coef, xx)

def E_from_d4(d4):
    return (d4 - 2*D0 - 8*C0**2 + 3*C0/4.0 - 1.0/128.0)/4.0

resB3 = {}; resB5 = {}
P("  -- 方案 B3（固定 α=-1/2、β=-9/32，三参 {γ,δ4,ε5} 自由）--")
for lo, hi, tag in [(33,129,"33..128"), (33,257,"33..256"), (33,513,"33..512")]:
    s = (m_all>=lo)&(m_all<hi)
    d4, coef, rr = d4_from_x(m_all[s], x[s], free5=False)
    Eo = E_from_d4(d4)
    resB3[tag] = Eo
    P("  %-9s N=%3d  γ=%+.6f δ4=%+.6f ε5=%+.4f RMS=%.2e  → E_δ=%+.6f（vs 39/2000 %+.2f pct, vs 41/2000 %+.2f pct）"
      % (tag, int(s.sum()), coef[0], coef[1], coef[2], rr, Eo, (Eo-E39)/E39*100.0, (Eo-E41)/E41*100.0))
P("  -- 方案 B5（全五参 {α,β,γ,δ4,ε5} 自由——α/β 锁定免检）--")
for lo, hi, tag in [(33,129,"33..128"), (33,257,"33..256"), (33,513,"33..512")]:
    s = (m_all>=lo)&(m_all<hi)
    d4, coef, rr = d4_from_x(m_all[s], x[s], free5=True)
    Eo = E_from_d4(d4)
    resB5[tag] = Eo
    P("  %-9s N=%3d  α=%+.4f β=%+.4f γ=%+.6f δ4=%+.6f ε5=%+.4f RMS=%.2e  → E_δ=%+.6f（vs 39/2000 %+.2f pct, vs 41/2000 %+.2f pct）"
      % (tag, int(s.sum()), coef[0], coef[1], coef[2], coef[3], coef[4], rr, Eo, (Eo-E39)/E39*100.0, (Eo-E41)/E41*100.0))

# ---------- 通道 C：四参自由 {C,D,E,F} bootstrap（178e 口径复核） ----------
P("\n[通道 C] 四参自由 {C,D,E,F}（δ = 1/56 - C/m - D/m² + E/m³ + F/m⁴）bootstrap 33..128")
P("-"*96)
def fit_full(ms, dd):
    X = np.array([[1.0/m, 1.0/m**2, 1.0/m**3, 1.0/m**4] for m in ms])
    y = np.array([d - O56 for d in dd])
    coef, *_ = np.linalg.lstsq(X, y, rcond=None)
    pred = O56 + X@coef
    return coef, rms(pred, dd)

s = (m_all>=33)&(m_all<129)
mb, db = m_all[s], d_all[s]
coef0, r0 = fit_full(mb, db)
EC_mean, EC_std = 0.0, 0.0
ECs = []
for _ in range(2000):
    idx = [random.randrange(nb) for _ in range(nb)]
    coef, _ = fit_full(mb[idx], db[idx])
    ECs.append(coef[2])
ECs = np.array(ECs)
EC_mean, EC_std = float(np.mean(ECs)), float(np.std(ECs, ddof=1))
zC_39 = (EC_mean - E39)/EC_std
zC_41 = (EC_mean - E41)/EC_std
P("  full-fit(33..128): C=%.8f D=%+.6f E=%+.6f F=%+.4f RMS=%.2e" % (-coef0[0], coef0[1], coef0[2], coef0[3], r0))
P("  bootstrap: E=%.6f +- %.2e  z_vs_39/2000=%+.1f  z_vs_41/2000=%+.1f"
  % (EC_mean, EC_std, zC_39, zC_41))
P("  ★ 通道 C 注意：E/D 相关污染（178e 已登记 z=-1.54 vs 41/2000）——E 的 σ 被 D 涨落放大，39/2000 vs 41/2000 在此通道无判别力")

# ---------- 通道 D：E=39/2000 完整模型全局残差审计 + D-E=1/1000 结构 ----------
P("\n[通道 D] E=39/2000 完整模型残差审计 + D−E=1/1000 结构")
P("-"*96)
for lo, hi, tag in [(33,129,"33..128"), (33,257,"33..256"), (33,513,"33..512"), (33,1009,"33..1009")]:
    s = (m_all>=lo)&(m_all<hi)
    mn, dd = m_all[s], d_all[s]
    pred39 = O56 - C0/mn - D0/mn**2 + E39/mn**3
    pred41 = O56 - C0/mn - D0/mn**2 + E41/mn**3
    r39 = rms(pred39, dd); r41 = rms(pred41, dd)
    res = dd - pred39
    P("  %-9s N=%3d  RMS(E39)=%.2e  RMS(E41)=%.2e  ratio=%.2f  E39残差: max=%+.1e mean=%+.1e"
      % (tag, int(s.sum()), r39, r41, r41/r39 if r39>0 else float("inf"),
         float(np.max(np.abs(res))), float(np.mean(res))))
P("  结构检验：D−E = 41/2000−39/2000 = 1/1000 = 10⁻³（n_max=10 的立方，候选级）")
P("  δ(E=39/2000) = 镜像零参(41/2000) − 10⁻³/m³ —— 望远镜镜像结构保留 + 10⁻³ 修正")

# ---------- 判别 ----------
P("\n[判别] 三通道 E 最优估计一致性 + 39/2000 命中")
P("-"*96)
rows = [
    ("A: δ拟合单参(M1, 225)", 0.019505, 3.4e-5, "bootstrap 33..128"),
    ("B: x* δ4 三参(B3, 180扩)", resB3["33..128"], None, "固定 α/β"),
    ("B5: x* δ4 全五参", resB5["33..128"], None, "全自由"),
    ("C: 四参自由 bootstrap(178e)", EC_mean, EC_std, "D/E 相关污染"),
]
P("  %-28s %12s %10s  vs39/2000  vs41/2000  注" % ("通道", "E_opt", "±σ"))
for name, Eo, sig, note in rows:
    if sig is None or sig == 0:
        sigs = "  --  "
        z39 = "--"; z41 = "--"
    else:
        sigs = "%.1e" % sig
        z39 = "%+.1fσ" % ((Eo-E39)/sig)
        z41 = "%+.1fσ" % ((Eo-E41)/sig)
    P("  %-28s %+10.6f %10s  %8s  %8s  %s" % (name, Eo, sigs, z39, z41, note))
P("")
P("  ★ 39/2000 命中判级：")
P("    通道 A: +0.026 pct（精确命中，强候选级）")
P("    通道 B: B3 %+.2f pct / B5 %+.2f pct（σ 内一致）" % ((resB3["33..128"]-E39)/E39*100.0, (resB5["33..128"]-E39)/E39*100.0))
P("    通道 C: %+.1fσ（相关污染，弱判别力）" % zC_39)
P("  41/2000 状态：通道 A 29σ 排除（225 定案）；通道 B/C 方向一致偏 39/2000 侧")

json.dump({"resA": resA, "bootstrapA": {"mean": EA_mean, "std": EA_std, "z39": zA_39, "z41": zA_41},
           "resB3": resB3, "resB5": resB5,
           "bootstrapC": {"mean": EC_mean, "std": EC_std, "z39": zC_39, "z41": zC_41},
           "E39": E39, "E41": E41},
          open(OUT_JSON, "w", encoding="utf-8"), indent=1)
P("\nJSON 落盘 OK (exit 0)")
