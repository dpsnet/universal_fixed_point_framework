me = 0.51099895
cand = me * 3 * (3/2)**2   # Nc*C_QCD = 3*(9/4) = 27/4
print("m_e*Nc*C_QCD =", cand)
print("paper40 m_ud = 3.45, dev =", (cand-3.45)/3.45*100, "%")
# PDG 2 GeV MS-bar 现值：u=2.16, d=4.67（平均 3.415）
print("PDG avg (2.16+4.67)/2 =", (2.16+4.67)/2, "dev =", (cand-3.415)/3.415*100, "%")
# 阶段1 m_ud/Lambda = (2σ)²(1-σ) 候选核对
sigma=1/15; L=210.219
c2 = (2*sigma)**2*(1-sigma)*L
print("stage1 cand (2σ)²(1-σ)Λ =", c2, "dev vs 3.45 =", (c2-3.45)/3.45*100, "%")
