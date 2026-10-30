# -*- coding: utf-8 -*-
"""
Phase 102 P7-5u-verify：e^{−3e} 精确化候选验证
==============================================================================
候选：① 3e−σ/78（= 3e−1/1170——指数命中 0.00001% 级——但 78 身份待查）
      ② 3e−σ³（全框架量——σ³ = (1/15)³——质量偏差改善？）
"""
import math, json

M_TAU = 1776.86
M_E = 0.5109989
R_TARGET = M_E/M_TAU
X_TARGET = -math.log(R_TARGET)
E = math.e
SIG3 = (1/15.0)**3

def dev(f, t): return (f/t-1)*100

print("P7-5u-verify：e^{−3e} 精确化候选验证")
print("="*74)
print("目标：x_target = %.6f（m_e/m_τ = %.7e）" % (X_TARGET, R_TARGET))

cands = [
    ("3e（P7-4b 原候选）", 3*E, "e 域基础"),
    ("3e−σ/78（=3e−1/1170）", 3*E-SIG3*15/78.0 if False else 3*E-1/1170.0, "78 无身份——待查"),
    ("3e−σ³", 3*E-SIG3, "σ³ = (1/15)³ 全框架"),
]
for name, x, note in cands:
    r = math.exp(-x)
    print("\n[%s]" % name)
    print("  x = %.6f（vs 目标 %+.4f%% 指数）——%s" % (x, dev(x, X_TARGET), note))
    print("  m_e/m_τ = %.7e（vs 实验 %.7e——质量 %+.4f%%）" % (r, R_TARGET, dev(r, R_TARGET)))
    me = r*M_TAU
    print("  m_e = %.5f MeV（vs 实验 %.7f——%+.4f%%）" % (me, M_E, dev(me, M_E)))

# 78 身份搜索
print("\n[78 身份搜索]")
print("  78 = 2×3×13——13 不在对偶网络（16/15/8/3/7/4/5）")
print("  78 = 15×5+3 = (2k_max−1)(k_max−N_gen)+N_gen——绕但全框架量")
print("  78 = 6×(8+5) = (k_max/4·N_gen)(k_max+k_max−N_gen)——更绕")
print("  ★ 诚实：78 无干净框架身份——3e−σ/78 数值命中但身份缺失——不立候选（P7-1 4.22 同类）")

print("\n[判定]")
print("  ★ 3e−σ³：质量 %+.4f%%（优 P7-4b −0.0854%%）——全框架量——候选级登记（非 0.01%% 级达标）" % dev(math.exp(-(3*E-SIG3))*M_TAU, M_E))
print("  ★ e^{−3e} 维持 −0.085%% 候选——域间张力维持——统一钥匙未找到")
print("  ★ 3e−σ³ 的机制：为何 σ³ 从 3e 减？——σ³ = S_4 立方——'静默立方的代静默修正'——机制开放")

result = {"cands": [(n, x, dev(x, X_TARGET)) for n, x, _ in cands]}
with open(r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_phase102_p7_5u_verify.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=1)
print("\nexit 0")
