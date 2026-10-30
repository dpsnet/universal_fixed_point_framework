# -*- coding: utf-8 -*-
"""
Phase 102 P7-5e-30：m_τ/m_e 双链汇合偏差诊断
================================================================
谱隙链 vs 指数链（P7-5v）对 m_e/m_τ 的预言偏差 0.05%——来源诊断：
- 谱隙链：m_e/m_τ = (1−Δλ_EM/16)/(193×18)
- 指数链：m_e/m_τ = e^{−(3e−σ³(1+α_v))}
诊断偏差来自哪条链、是否需要第二修正项
"""
import math

dH   = math.log(15)
dlam_EM = math.pi/(24*dH+72)
C2 = 4*math.log(10)
sigma = 1/15
alpha_v = 1+sigma+math.sqrt(4/3/2)   # 1+σ+√(C_F/2)

m_e = 0.51099895
m_tau = 1776.86

print("="*104)
print("P7-5e-30：m_τ/m_e 双链汇合偏差诊断")
print("="*104)
print("  PDG：m_τ/m_e = %.6f" % (m_tau/m_e))
print("  Δλ_EM/16 = %.8f" % (dlam_EM/16))
print()

print("① 谱隙链（P7-5e-20 形式）：")
me_tau_spec = (1-dlam_EM/16)/(193*18)
tau_me_spec = 1/me_tau_spec
print("  m_e/m_τ = (1−Δλ/16)/(193×18) = %.10f" % me_tau_spec)
print("  m_τ/m_e = %.6f（%+.4f%% vs PDG）" % (tau_me_spec, (tau_me_spec/(m_tau/m_e)-1)*100))
print()

print("② 指数链（P7-5v 形式）：")
exp_arg = 3*math.e - sigma**3*(1+alpha_v)
me_tau_exp = math.exp(-exp_arg)
tau_me_exp = 1/me_tau_exp
print("  m_e/m_τ = e^{−(3e−σ³(1+α_v))} = e^{−%.10f} = %.10f" % (exp_arg, me_tau_exp))
print("  m_τ/m_e = %.6f（%+.4f%% vs PDG）" % (tau_me_exp, (tau_me_exp/(m_tau/m_e)-1)*100))
print()

print("③ 双链汇合：")
print("  谱隙链 vs 指数链 m_e/m_τ：")
print("    谱隙 %.10f vs 指数 %.10f——差 %+.4f%%" % (me_tau_spec, me_tau_exp, (me_tau_spec/me_tau_exp-1)*100))
print("  m_τ/m_e：谱隙 %.6f vs 指数 %.6f——差 %+.4f%%" % (tau_me_spec, tau_me_exp, (tau_me_spec/tau_me_exp-1)*100))
print()

print("④ 偏差来源诊断：")
print("  谱隙链偏差（vs PDG）：%+.4f%%" % ((tau_me_spec/(m_tau/m_e)-1)*100))
print("  指数链偏差（vs PDG）：%+.4f%%" % ((tau_me_exp/(m_tau/m_e)-1)*100))
print("  双链间偏差：%+.4f%%" % ((tau_me_spec/tau_me_exp-1)*100))
print()

print("⑤ 诊断：若双链应精确一致（同一物理量同一框架）——偏差揭示结构不精确：")
print("  候选 1：谱隙链一阶修正 (1−Δλ/16) 需二阶项 Δλ²·k？——量级 ~5e-7 太小，不解释 0.05%")
print("  候选 2：指数链参数（α_v 或 σ³ 系数）有微调空间——需框架身份支持")
print("  候选 3：两条链的'基准'不同（谱隙链以 m_e 绝对锚、指数链以 m_τ 绝对锚）——")
print("        谱隙链 m_e = C²(1−Δλ/16)/18 自身偏差 −0.0092%——链上误差传播")
print()
print("exit 0")
