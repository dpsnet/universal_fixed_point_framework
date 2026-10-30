# -*- coding: utf-8 -*-
"""
Phase 104az-70: 机制论证 — F_np 三组件谱语言重写 + 谱织同构重审
核心问题：F_np = (b0/10)^3 * (1-delta)/dl3 的机制来源
候选：(b0/10)^3 = Ngen^6/10^3 = 729/1000 与 D9 谱织约束 a = Tc/Lambda = 0.72915 的 0.02% 同构
      —— 104az-67 给 (b0/10)^3 代数身份后，此同构是否仍"登记不立"？是否升格候选？
另检：F_np 三组件全部为框架量纯代数组合的结构事实
"""
import math

# --- 框架常数 ---
Nc = 3
Nf = 3
Ngen = 3
kmax = 8
sigma = 1/15
CF = (Nc**2 - 1)/(2*Nc)
delta = sigma**2 * CF / 4          # 1/675
dlmin = (math.sqrt(3) - 1) / 6
dl3 = math.sqrt(2) * dlmin
b0 = (11*Nc - 2*Nf) / 3            # 9
ten = Ngen + kmax - 1              # 10

# --- F_np 三组件 ---
base = (b0/10)**3                  # 729/1000
corr = 1 - delta                   # 674/675
inv_dl3 = 1/dl3
F_np = base * corr * inv_dl3
print(f"F_np = {F_np:.9f}  (登记 4.218700, 目标 4.220, dev {(F_np/4.220-1)*100:+.4f}%)")
print(f"  base  = {base:.9f} = (Ngen^2/10)^3 = 729/1000")
print(f"  corr  = {corr:.9f} = 674/675 = 1 - sigma^2*CF/4")
print(f"  invdl3= {inv_dl3:.9f} = 1/(sqrt2*dlmin) = Ngen!/(sqrt2*(sqrt3-1))")

# --- 机制候选 1：谱织同构重审 ---
# D9 谱织约束 a = Tc/Lambda = (62/(36*pi*sqrt2))^(1/3)
d_eff = 62/3                       # 3*d_eff = 62
a = (62/(36*math.pi*math.sqrt(2)))**(1/3)
print(f"\n[谱织同构] a = Tc/Lambda = {a:.9f}")
print(f"  base = (b0/10)^3 = {base:.9f}")
print(f"  dev a vs base = {(a/base-1)*100:+.5f}%")
print(f"  a^3 = {a**3:.9f}  vs 62/(36*pi*sqrt2) = {62/(36*math.pi*math.sqrt(2)):.9f}")
print(f"  判别: 0.02% 同构 → {'候选级(不立)' if abs(a/base-1)*100 > 0.005 else '强候选'}")
print(f"  注: (b0/10)^3 = (Ngen^2/10)^3 有代数身份——'0.729'从数值巧合升级为结构量")

# --- 机制候选 2：F_np 用谱织 a 代 base 的偏差 ---
F_np_a = a * corr * inv_dl3
print(f"\n[谱织替换] F_np(a) = a*(1-delta)/dl3 = {F_np_a:.9f}")
print(f"  dev vs F_np = {(F_np_a/F_np-1)*100:+.5f}%")
print(f"  dev vs 4.220 = {(F_np_a/4.220-1)*100:+.5f}%")

# --- 机制候选 3：三组件代数闭式（全框架量——结构事实） ---
print(f"\n[结构事实] F_np 全组件框架量表达:")
print(f"  (Ngen^2/(Ngen+kmax-1))^3 = {(Ngen**2/ten)**3:.9f} == base? {abs((Ngen**2/ten)**3 - base) < 1e-12}")
print(f"  (1 - sigma^2/Nc) = {1 - sigma**2/Nc:.9f} == corr? {abs(1-sigma**2/Nc - corr) < 1e-12}")
print(f"  1/(sqrt2*dlmin) = {1/(math.sqrt(2)*dlmin):.9f} == inv_dl3? {abs(1/(math.sqrt(2)*dlmin) - inv_dl3) < 1e-12}")
print(f"  结论: 三组件全部 = Ngen/kmax/sigma/Nc/dlmin 纯代数组合——F_np 不含任何外部量")

# --- 机制候选 4：分子家族 Ngen 幂 —— 6 = 3*2 = Ngen*N_active? ---
print(f"\n[分子家族] Ngen^6 = Ngen^(2*N_active) = 3^6? {Ngen**6 == 729}")
print(f"  6 = 2*3 = 2*Ngen (N_active=3=Ngen) —— Ngen 幂 = 2*Ngen = 6")
print(f"  10^3 = (Ngen+kmax-1)^3——分母 10 = 代间静默和")
print(f"  幂差 4 = kmax/2 (Λ缺口 Ngen^6 vs mN缺口 Ngen^2)")

# --- 机制候选 5：1/56 = 1/(8*7) 静默家族连接（历史 1/56 锁定量） ---
print(f"\n[谱隙分母] dl3 = sqrt2*dlmin = {dl3:.9f}")
print(f"  dl3 vs 1/56 = {1/56:.9f} (历史 δ∞ 锁定量)")
print(f"  dl3/(1/56) = {dl3/(1/56):.6f} —— 无简单比值（谱隙分母非静默量）")
print(f"  谱隙语义: paper17 §12.1 禁闭 = 谱间隙坍缩——非微扰因子分母=谱隙尺度")

# --- 判别总结 ---
print(f"\n=== 机制论证结论 ===")
print(f"1. F_np 三组件全框架量（结构事实，104az-67/68 代数身份 Lean 固化）")
print(f"2. base=(b0/10)^3 与谱织 a=Tc/Lambda 0.02% 同构——候选级")
print(f"   (b0/10)^3 = (Ngen^2/10)^3 是代数身份——'0.729' 从巧合升格为结构量——但 a 的公式 62/(36pi√2) 与 729/1000 无代数联系——同构仍候选")
print(f"3. 为什么是 织×修/隙 而非其他组合——诠释层开放（M1-M3 登记延续）")
