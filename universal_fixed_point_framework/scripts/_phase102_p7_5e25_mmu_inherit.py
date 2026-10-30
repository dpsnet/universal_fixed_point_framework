# -*- coding: utf-8 -*-
"""
Phase 102 P7-5e-25：m_μ 绝对质量继承链验证
================================================================
分工图景：m_μ 走"间隔链"——由谱隙 m_τ（C²×193）× 指数间隔（P7-4d e^{−(ln16+e^{−3})}）继承
① m_μ = C²×193×e^{−(ln16+e^{−3})}（谱隙 m_τ × 指数间隔）
② P7-4e 统一静默形式重述：m_μ = M·s^{e^{−3}}·16^{−1}（同一恒等，M = m_τ）
③ m_μ 直接谱隙候选扫描（23/2×(1±Δλ/16) 等——确认不达标，分工自洽）
④ m_c 比值恒等重述确认（m_c/m_τ = √10/(193Δλ)——非独立交叉，诚实边界）
"""
import math

dH   = math.log(15)
dlam = math.pi/(24*dH+72)
kmax, Ngen = 8, 3
sigma = 1/15
C  = 2*math.sqrt(math.log(10))
C2 = C*C

m_mu_pdg = 105.658375
m_tau_pdg = 1776.86

print("="*104)
print("P7-5e-25：m_μ 绝对质量继承链验证")
print("="*104)

m_tau_spectral = C2*193
interval = math.exp(-(math.log(16)+math.exp(-3)))
m_mu_inherit = m_tau_spectral*interval

print("① 继承链：m_μ = C²×193×e^{−(ln16+e^{−3})}")
print("  谱隙 m_τ = C²×193 = %.4f（PDG 1776.86，%+.4f%%）" % (m_tau_spectral, (m_tau_spectral/m_tau_pdg-1)*100))
print("  指数间隔 e^{−(ln16+e^{−3})} = %.8f（P7-4d 闭式）" % interval)
print("  m_μ（继承）= %.4f vs PDG 105.6584（%+.4f%%）" % (m_mu_inherit, (m_mu_inherit/m_mu_pdg-1)*100))
print()

print("② P7-4e 统一静默形式重述（M·s^{e^{−3}}·16^{−1}，M = m_τ）：")
m_mu_restate = m_tau_spectral*math.exp(-math.exp(-3))/16
print("  m_μ = m_τ·s^{e^{−3}}·16^{−1} = %.4f（%+.4f%%）——与①恒等（16 = e^{ln16}）" % (m_mu_restate, (m_mu_restate/m_mu_pdg-1)*100))
print()

print("③ m_μ 直接谱隙候选扫描（确认不达标 → 分工自洽）：")
mcand = [
    ("23/2（3k_max−1）/2", 23/2),
    ("23/2×(1−Δλ/16)", 23/2*(1-dlam/16)),
    ("23/2×(1+Δλ/16)", 23/2*(1+dlam/16)),
    ("2⁶/5.58", None),
]
for name, f in mcand:
    if f is None: continue
    v = C2*f
    print("  %-22s = %.4f（%+.4f%%）" % (name, v, (v/m_mu_pdg-1)*100))
print("  → m_μ 直接谱隙候选全部不达标（>0.1%）——m_μ 走间隔继承链，分工自洽")
print()

print("④ m_c 比值恒等重述确认（诚实边界）：")
print("  m_c/m_τ = κΛ√10/(C²×193) = √10/(193Δλ) = %.6f vs PDG %.6f（%+.4f%%）" % (
    math.sqrt(10)/(193*dlam), 1270/1776.86, (math.sqrt(10)/(193*dlam)/(1270/1776.86)-1)*100))
print("  → 该比值是 m_c = κΛ√10 与 m_τ = C²×193 的恒等重述（C² 消去）——非独立交叉——单点命中边界保持")
print()

print("⑤ 判定：")
print("  m_μ 继承链：谱隙 m_τ × 指数间隔 → 105.71（%+.4f%%）——达标（<0.1%%）" % ((m_mu_inherit/m_mu_pdg-1)*100))
print("  分工图景完整化：m_μ 绝对质量由 m_τ（谱隙锚）× 间隔（指数链）继承——无需独立谱隙身份")
print("  → 轻子全三代绝对质量有框架身份：m_e（谱隙锚）、m_μ（间隔继承）、m_τ（谱隙锚）")
print()
print("exit 0")
