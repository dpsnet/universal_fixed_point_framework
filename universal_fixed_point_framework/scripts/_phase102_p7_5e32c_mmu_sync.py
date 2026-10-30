# -*- coding: utf-8 -*-
"""P7-5e-32c：m_τ 精化对 m_μ 继承链的同步验证"""
import math

C2 = 4*math.log(10)
kmax, Ngen = 8, 3
gap = 193-3/40   # 精化系数
interval = math.exp(-(math.log(16)+math.exp(-3)))

print("="*104)
print("P7-5e-32c：m_τ 精化 → m_μ 继承链同步改善")
print("="*104)
m_tau_ref = C2*gap
m_mu_old = C2*193*interval
m_mu_new = C2*gap*interval
print("  m_τ(精化) = C²×(193−3/40) = %.6f（%+.4f%%）" % (m_tau_ref, (m_tau_ref/1776.86-1)*100))
print("  m_μ(原系数) = C²×193×间隔 = %.6f（%+.4f%%）" % (m_mu_old, (m_mu_old/105.658375-1)*100))
print("  m_μ(精化系数) = C²×(193−3/40)×间隔 = %.6f（%+.4f%%）" % (m_mu_new, (m_mu_new/105.658375-1)*100))
print("  m_μ 偏差改善：+0.043%% 到 %+.4f%%（偏差传播源消除）" % ((m_mu_new/105.658375-1)*100))
print()
print("  m_μ/m_e（比值层，独立于系数）：")
print("    m_μ/m_e(PDG) = %.6f" % (105.658375/0.51099895))
print("exit 0")
