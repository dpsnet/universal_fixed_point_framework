# -*- coding: utf-8 -*-
"""v1.3 修订后审计：σ_score 六通道复算 + 摘要/正文指标一致性 + 残留 token 扫描。"""
import io, math, re

P = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\paper\paper_SM_endogenous_derivation.md"
txt = io.open(P, encoding="utf-8", newline="").read()
lines = txt.split("\n")

# ---------- 1. 框架值与六通道 σ_score 复算 ----------
s = 1.0 / 15.0
dstar = 6 * s ** 3 + 4 * s ** 5 + 8 * s ** 7 + 5 * s ** 8
alpha_fw = 72 + 24 * math.log(15) + 24 * dstar
print("σ = 1/15 = %.17g" % s)
print("δ* = %.17g" % dstar)
print("α⁻¹_fw = %.15f  (论文 137.035999083426)" % alpha_fw)
print("Δ(理论值-论文值) = %.3e" % (alpha_fw - 137.035999083426))

CH = [("Cs 反冲", 137.035999046, 2.7e-8, -1.39),
      ("Rb-2011", 137.035999037, 9.1e-8, -0.51),
      ("Rb-2020", 137.035999206, 1.1e-8, +11.14),
      ("a_e g-2", 137.035999152, 3.4e-8, +2.02),
      ("CODATA 2018", 137.035999084, 2.1e-8, +0.03),
      ("CODATA 2022", 137.035999177, 2.1e-8, +4.46)]
print("\n%-12s %10s %10s %12s" % ("channel", "论文σ", "复算σ", "diff"))
for name, exp, u, claimed in CH:
    ss = (exp - alpha_fw) / u
    print("%-12s %+10.2f %+10.4f %12.2e" % (name, claimed, ss, ss - claimed))

# ---------- 2. sin²θ_W / 比值 ----------
r = 1286.0 / 1459.0
sin2 = 1.0 - r ** 2
print("\nm_W/m_Z = 1286/1459 = %.9f" % r)
print("sin²θ_W = 1-r² = %.9f" % sin2)
r_exp = 80.3692 / 91.1880
print("实验比值 80.3692/91.1880 = %.9f  偏差 %.5f%%" % (r_exp, (r - r_exp) / r_exp * 100))

# ---------- 3. 残留 token 扫描 ----------
print("\n=== 残留扫描（每处给行号+上下文）")
TOK = ["−4.5σ", "4.5σ_score", "−4.5", "0.0005%", "Fibonacci {3, 5, 7, 8}",
       "1.1×10⁻¹⁰", "9.1×10⁻¹⁰", "n=4 有整数根", "v1.2 — 2026-11-11",
       "2026-11-11", "codata2026_frozen", "纯时空代数基准", "纯签名域"]
for t in TOK:
    hits = [(i + 1, l) for i, l in enumerate(lines) if t in l]
    if hits:
        print("\n[%s] %d 处" % (t, len(hits)))
        for ln, l in hits[:6]:
            print("  L%-5d %s" % (ln, l.strip()[:150]))

# ---------- 4. 关键指标一致性 ----------
print("\n=== 关键指标一致性")
for pat, want in [("N_active=3", "摘要/§5.5 指标"),
                  ("+4.46σ_score", "CODATA 2022 口径"),
                  ("0.8813572", "实验比值"),
                  ("0.881425634", "框架比值")]:
    print("%-14s 出现 %d 次" % (pat, txt.count(pat)))

print("\n=== 版本行 & §9.1b 引用")
for i, l in enumerate(lines):
    if "**版本**" in l or "**仓库**" in l or "9.1b" in l:
        print("L%-5d %s" % (i + 1, l.strip()[:120]))
