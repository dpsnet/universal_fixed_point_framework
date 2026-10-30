# -*- coding: utf-8 -*-
"""轻子间隔统一判别（2026-10-25）：I_μ = ln16+e^{−3} vs I_e = 3e−σ³(1+α_v)

口径（P7-4d / P7-5v，note_phase102:218-233/2827-2842）：
  I_μ = ln16 + e^{−3}（主项 ln16 = 4ln2 旋量对偶、修正 e^{−3} 对象静默 S_3）
  I_e = 3e − σ³(1+α_v)（主项 3e = N_gen·e 自然静默、修正 σ³(1+α_v) 弱电放大）
  σ = 1/15（静默基倒数）、σ³ = 1/3375、α_v = 16/15+√(2/N_c)（P7-5j 框架）
  (1+α_v) = 2σ³+σ⁴+σ³√(C_F/2) 三层分解（P7-5v 登记）

目标：判别 I_e、I_μ、I_e−I_μ、I_e/I_μ 的框架组合身份（≤0.01% 达标线）。
勘误登记：先前错误计算把 σ³ 误用为 0.005346（正确 1/3375 = 0.0002963），
'16/3−1/160 锁定级'为错误产物——本脚本用正确口径。
"""
import math
from itertools import product

# ---- 框架常数库 ----
N_gen, k_max = 3, 8
e = math.e
ln2, ln15, ln16 = math.log(2), math.log(15), math.log(16)
sigma = 1/15
s3 = sigma**3                      # 1/3375
alpha_v = 16/15 + math.sqrt(2/N_gen)   # P7-5j
Cf2 = 2/3                          # C_F/2
dH = 16259/6000                    # d_H 生成链闭式
dlmin = math.sqrt(3) - 1
dl3 = math.sqrt(2)*dlmin

I_mu = ln16 + e**(-3)
I_e  = 3*e - s3*(1+alpha_v)
# 三层分解校验
decomp = 2*s3 + sigma**4 + s3*math.sqrt(Cf2)
print(f"I_μ = ln16 + e^(−3) = {I_mu:.10f}")
print(f"I_e = 3e − σ³(1+α_v) = {I_e:.10f}  （三层分解 {decomp:.10f} 校验差 {abs((1+alpha_v)*s3-decomp):.2e}）")
print(f"I_e − I_μ = {I_e-I_mu:.10f}   I_e/I_μ = {I_e/I_mu:.10f}")
print()

# ---- 目标量 ----
targets = {
    "I_mu":  I_mu,
    "I_e":   I_e,
    "Ie-Im": I_e - I_mu,
    "Ie/Im": I_e / I_mu,
}

# ---- 候选生成：a×ln(b) / a×e^k / 有理组合 ----
ints = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,27,28,30,
        31,32,35,40,42,44,45,48,49,54,56,60,63,64,70,84,100,105,125,128,160,193,210,
        253,320,3375,675,729,1000]
logs = {"ln2": ln2, "ln15": ln15, "ln16": ln16, "ln3": math.log(3), "ln5": math.log(5),
        "ln7": math.log(7), "ln10": math.log(10), "ln(e)": 1.0}
exps = {"e": e, "e^-1": e**(-1), "e^-2": e**(-2), "e^-3": e**(-3), "e^-16": e**(-16)}
fracs = {"N_gen":3.0, "k_max":8.0, "σ": sigma, "σ²": sigma**2, "σ³": s3,
         "Δλ_min": dlmin, "Δλ³": dlmin**3, "√(C_F/2)": math.sqrt(Cf2),
         "α_v": alpha_v, "d_H": dH, "16/15": 16/15, "15/16": 15/16}

# 组合候选：a×lnb、a×e^k、a×frac、纯有理 a/b、组合差/和
cands = {}
for a in ints:
    for name, lv in logs.items():
        cands[f"{a}×{name}"] = a*lv
    for name, ev in exps.items():
        cands[f"{a}×{name}"] = a*ev
    for name, fv in fracs.items():
        cands[f"{a}×{name}"] = a*fv
    for b in ints:
        if b != 0:
            cands[f"{a}/{b}"] = a/b
            cands[f"{a}+{b}"] = a+b
# 两量组合（仅记录命中的）
print("=== 单量/组合命中（|相对差| ≤ 0.05%） ===")
for tname, tval in targets.items():
    hits = []
    for cname, cval in cands.items():
        if cval == 0:
            continue
        rel = (cval - tval)/tval
        if abs(rel) <= 5e-4:
            hits.append((cname, cval, rel))
    hits.sort(key=lambda x: abs(x[2]))
    print(f"\n[{tname}] = {tval:.10f}：{len(hits)} 命中")
    for cname, cval, rel in hits[:12]:
        print(f"   {cname:16s} = {cval:.10f}  差 {rel*100:+.4f}%")

# ---- 双量组合（Ie−Im 目标） ----
print("\n=== Ie−Im = 5.3316151 双量组合（差/和/积商，≤0.05%） ===")
tval = targets["Ie-Im"]
hits = []
for (n1, v1), (n2, v2) in product(cands.items(), repeat=2):
    if n1 == n2:
        continue
    for op, f in (("+", v1+v2), ("−", v1-v2)):
        if f != 0:
            rel = (f - tval)/tval
            if abs(rel) <= 5e-4:
                hits.append((f"{v1:.6f} {op} {v2:.6f} [{n1} {op} {n2}]", f, rel))
hits.sort(key=lambda x: abs(x[2]))
print(f"{len(hits)} 命中")
for cname, cval, rel in hits[:10]:
    print(f"   {cname} = {cval:.10f}  差 {rel*100:+.4f}%")

# ---- 通道差判别：3e vs 4ln2 ----
print("\n=== 通道差判别 ===")
diff_3e_4ln2 = 3*e - 4*ln2
print(f"3e − 4ln2 = {diff_3e_4ln2:.10f}（主项通道差）")
print(f"  ≈ 2π − 9/10 = {2*math.pi-0.9:.10f}（差 {(2*math.pi-0.9-diff_3e_4ln2)/diff_3e_4ln2*100:+.4f}%）")
print(f"  ≈ 5.38140 目标组合……I_e−ln16 = {I_e-ln16:.10f}")
print(f"  ≈ 16/3+1/15−σ? = {16/3+1/15-sigma:.6f}")
print(f"  16/3 vs Ie−Im 差 {(16/3-tval)/tval*100:+.4f}%（登记候选 0.032%）")
print(f"  ln16+e^{{-3}} 主项修正比 {ln16/e**(-3):.4f}（>55 主导+修正 阈值）")
