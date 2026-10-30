# -*- coding: utf-8 -*-
"""
Phase 102 P7-6：m_N SU(6) 缺口机制攻坚
==============================================================================
缺口 = m_N(框架 1014.9) − 实验 938.272 = 76.63 MeV
已有候选：κ²Λ/10 = 76.599（−0.038%——/10 = /(N_gen+k_max−1) 加法缺环）
新候选方向：
  · κΛ(1−2σ/3)/5——胶子 dressing 修正量 × 代间静默（5 = k_max−N_gen）
  · √(2/15)·Λ——√(2σ)——2 = k_max/4、15 = 2k_max−1
  · 缺口/Λ = 0.36490 的系统搜索（两参数框架组合）
"""
import math, json

KAPPA = 6/math.pi
LAM = 210.0
SIG = 1/15.0
GAP = 76.63
GAP_L = GAP/LAM

def dev(f, t): return (f/t-1)*100

print("P7-6：m_N SU(6) 缺口机制攻坚")
print("="*78)
print("缺口 = 76.63 MeV（m_N 框架 1014.9 − 实验 938.272）——缺口/Λ = %.5f" % GAP_L)

print("\n[A] 候选对比：")
cands = [
    ("κ²Λ/10（已有——/10 = N_gen+k_max−1）", KAPPA**2*LAM/10),
    ("κΛ(1−2σ/3)/5（新——5 = k_max−N_gen）", KAPPA*LAM*(1-2*SIG/3)/5),
    ("√(2/15)·Λ（新——√(2σ)——2=k_max/4）", math.sqrt(2/15.0)*LAM),
    ("3Δλ_min·Λ（已有——超标准）", 3*((math.sqrt(6)-math.sqrt(2))/math.sqrt(72))*LAM),
]
for name, v in cands:
    print("  %-38s = %8.4f（%+6.4f%%）" % (name, v, dev(v, GAP)))

print("\n[B] 缺口/Λ = 0.36490 系统搜索（框架量两参数组合）：")
DL = (math.sqrt(6)-math.sqrt(2))/math.sqrt(72)  # Δλ_min
frames = {"σ": SIG, "σ²": SIG**2, "σ³": SIG**3, "Δλ_min": DL, "2σ/3": 2*SIG/3,
          "κ/10": KAPPA/10, "κ²/10": KAPPA**2/10, "√(2/15)": math.sqrt(2/15.0),
          "1/ln15": 1/math.log(15), "σ·√(2/3)": SIG*math.sqrt(2/3.0), "√(2σ)": math.sqrt(2*SIG),
          "σ+Δλ_min": SIG+DL, "2Δλ_min/15": 2*DL/15, "Δλ_min·√(2/3)": DL*math.sqrt(2/3.0),
          "κσ": KAPPA*SIG, "κσ²": KAPPA*SIG**2, "κ/15": KAPPA/15, "κ/(2k_max)": KAPPA/16}
hits = []
for name, v in frames.items():
    d = dev(v, GAP_L)
    if abs(d) < 0.15:
        hits.append((abs(d), name, v, d))
hits.sort()
for hd, name, v, d in hits[:12]:
    print("  ★ %-16s = %.6f（%+6.4f%%）" % (name, v, d))
if not hits:
    print("  无 <0.15% 命中——缺口比例无干净两参数组合")

print("\n[C] 判定：")
print("  κΛ(1−2σ/3)/5：组件全身份（κΛ 定理量、2σ/3 已登记 Δ_dress、5 = k_max−N_gen）——但复用修正因子有事后嫌疑")
print("  κ²Λ/10：数值更优（−0.038%%）——/10 = N_gen+k_max−1 加法缺环")
print("  ★ 机制核心未解决：'为什么缺口 = 胶子量的这个比例'——两候选数值近（差 0.06%%）——判别需新证据")

result = {"gap": GAP, "cands": [(n, v, dev(v, GAP)) for n, v in cands], "search_hits": hits[:12]}
with open(r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_phase102_p7_6_mN_gap.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=1)
print("\nexit 0")
