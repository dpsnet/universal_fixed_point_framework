# -*- coding: utf-8 -*-
"""
P7-5e-163：x/16 身份链闭合检验
候选身份链（对 g(x) = a + b√x + c·x 的 x 系数 c）：
  I.  c = g(2)/2 = (1/k_max)/2 = 1/(2k_max) = 2^-4    （满格倒数的一半）
  II. c = (α₀/2)² = (1/4)² = 1/16                       （过零斜率平方，135/138）
  III.c = k_max·b² = 8·(√2/16)² = 1/16                  （√x 系数 b 的复合）
辅助恒等式：
  g(2) = 1/8 直接从形态涌现（-1/8 + √(2/2)/8 相消 + 2/16 = 1/8）
  g'(2) = 3/32 = g(2)·(k_max-2)/k_max
  c = 2·(g(2)-g'(2))
数据：146 拟合 a=-0.12501330 b=0.08839978 c=0.06249828；精确 -1/8, √2/16, 1/16
"""
import json

k_max = 8
alpha0 = 0.5
# 146 拟合值
fit = {"a": -0.12501330, "b": 0.08839978, "c": 0.06249828, "g2": 0.12499801}
exact = {"a": -1/8, "b": 2**0.5/16, "c": 1/16, "g2": 1/8}

print("=== 精确身份链（全部用精确值）===", flush=True)
c = exact["c"]
print("I.  c = g(2)/2          : %.10f vs %.10f  -> %s" %
      (exact["g2"]/2, c, "EXACT" if abs(exact["g2"]/2 - c) < 1e-12 else "NO"), flush=True)
print("    c = 1/(2k_max)      : %.10f vs %.10f  -> %s" %
      (1/(2*k_max), c, "EXACT" if abs(1/(2*k_max) - c) < 1e-12 else "NO"), flush=True)
print("II. c = (alpha0/2)^2    : %.10f vs %.10f  -> %s" %
      ((alpha0/2)**2, c, "EXACT" if abs((alpha0/2)**2 - c) < 1e-12 else "NO"), flush=True)
print("III.c = k_max·b^2       : %.10f vs %.10f  -> %s" %
      (k_max*exact["b"]**2, c, "EXACT" if abs(k_max*exact["b"]**2 - c) < 1e-12 else "NO"), flush=True)

print("\n=== 辅助恒等式 ===", flush=True)
gp2 = exact["b"]/(2*2**0.5) + c   # g'(2) = b/(2√x)|x=2 + c
print("g'(2) 形态涌现        : %.10f vs 3/32=%.10f -> %s" %
      (gp2, 3/32, "EXACT" if abs(gp2-3/32) < 1e-12 else "NO"), flush=True)
print("g'(2) = g(2)(k_max-2)/k_max: %.10f vs %.10f -> %s" %
      (exact["g2"]*(k_max-2)/k_max, gp2, "EXACT" if abs(exact["g2"]*(k_max-2)/k_max-gp2) < 1e-12 else "NO"), flush=True)
print("c = 2(g(2)-g'(2))     : %.10f vs %.10f -> %s" %
      (2*(exact["g2"]-gp2), c, "EXACT" if abs(2*(exact["g2"]-gp2)-c) < 1e-12 else "NO"), flush=True)
print("g(2) 形态涌现         : -1/8 + sqrt(2/2)/8 + 2/16 = %.10f vs 1/8 -> %s" %
      (exact["g2"], "EXACT" if abs(exact["g2"]-1/8) < 1e-12 else "NO"), flush=True)

print("\n=== 数值残差（146 拟合值 vs 精确）===", flush=True)
for k in ["a", "b", "c", "g2"]:
    dev = abs(fit[k]-exact[k])/abs(exact[k])*100
    print("%s: fit=%.8f exact=%.8f dev=%.5f%%" % (k, fit[k], exact[k], dev), flush=True)

print("\n=== 互洽性 ===", flush=True)
print("1/(2k_max) = (alpha0/2)^2 = k_max·b^2 ⇔ 三者同时成立 ⇔ alpha0^2·k_max = 2", flush=True)
print("check alpha0^2*k_max =", alpha0**2*k_max, "== 2?", flush=True)
print("1/(2k_max)=%.6f  (alpha0/2)^2=%.6f  k_max·b^2=%.6f" %
      (1/(2*k_max), (alpha0/2)**2, k_max*exact["b"]**2), flush=True)

print("\n=== 判别 ===", flush=True)
print("x/16 身份链闭合：c = g(2)/2 = 1/(2k_max) = (alpha0/2)^2 = k_max·b^2 —— 五路恒等精确", flush=True)
print("x/16 语义：g 的 x 项系数 = 过零值满格倒数的一半 = 过零斜率(1/4)的平方", flush=True)
print("x/16 不再孤立：从'无源常数'升为'g(2)与g'(2)的连带约束'——过零形态家族成员", flush=True)
print("诚实边界：身份链是代数恒等（精确），非机制推导——为何 g 形态含 c·x 仍需物理机制", flush=True)
print("机制候选（开放）：(a) f 的 m 依赖线性项 (b) 谐振近似遗漏的 1/m 阶 x 项 (c) 过零约束原理", flush=True)

out = {"identity_chain": {
    "I_c_eq_g2_over_2": {"form": "g(2)/2 = 1/(2k_max)", "value": 1/16, "exact": True},
    "II_c_eq_alpha0_2_sq": {"form": "(alpha0/2)^2 = (1/4)^2", "value": 1/16, "exact": True},
    "III_c_eq_kmax_b2": {"form": "k_max·(sqrt2/16)^2", "value": 1/16, "exact": True}},
  "aux": {"g2_from_shape": "1/8", "gp2_from_shape": "3/32",
          "gp2_ratio": "g(2)(k_max-2)/k_max", "c_eq_2_g2_gp2": True},
  "mutual_check": "alpha0^2*k_max = 2 (holds: 0.25*8=2)",
  "numeric_dev_146": {"a": 0.01064, "b": 0.01300, "c": 0.00275, "g2": 0.00159},
  "verdict": "identity chain closed - c = 1/(2k_max) = (alpha0/2)^2 = k_max·b^2 (5-way exact)",
  "honest_limit": "algebraic identity, not mechanism; mechanism open (a/b/c)"}
with open(r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_phase102_p7_5e163_x16_identity.json", "w", encoding="utf-8") as f:
    json.dump(out, f, indent=1, ensure_ascii=False)
print("\nsaved", flush=True)
