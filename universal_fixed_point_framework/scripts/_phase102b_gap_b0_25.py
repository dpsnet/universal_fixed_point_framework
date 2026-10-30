me = 0.51099895
L = 210.219
mud = me*27/4
kappa = 6/3.141592653589793
sigma = 1/15
dress = kappa*L*(1-2*sigma/3)
Mud_eff = mud + dress

# 新组合：Delta_hf = L*14/15（Lambda 链候选）+ 缺口 = L*b0/25
b0 = 9           # (11*3 - 2*3)/3
dh = L*14/15
gap_new = L*b0/25

mN_fw = 3*Mud_eff - 3*dh/4
mN = mN_fw - gap_new
print("dh =", dh, " gap =", gap_new, " gap/L =", gap_new/L)
print("mN_fw =", mN_fw, " mN =", mN, " vs 938.272 =", (mN-938.272)/938.272*100, "%")
print("gap target (cand dh) =", mN_fw-938.272, " dev of b0L/25 =", (gap_new-(mN_fw-938.272))/(mN_fw-938.272)*100, "%")

# m_Delta = m_N + 3/2*Delta_hf
mD = mN + 1.5*dh
print("mDelta =", mD, " vs PDG 1232.0 =", (mD-1232.0)/1232.0*100, "%")
print("重子和 =", mN+mD, " vs 2170.25 =", (mN+mD-2170.25)/2170.25*100, "%")

# m_H = m_N + m_e - E_b（E_b = 13.6 eV 可忽略）
mH = mN + me - 0.0000136
print("mH =", mH, " vs 938.783 =", (mH-938.783)/938.783*100, "%")

# m_p/m_n 检查（P7-3 Delta_m_pn = 1.293）
mp = mN - 1.293
mn = mN
print("mp =", mp, " mn =", mn, " (p+n)/2 vs PDG 938.919 =", (mN-938.919)/938.919*100, "%")

# m_rho 一致性（无缺口）
print("m_rho =", 2*Mud_eff, " vs 775.3 =", (2*Mud_eff-775.3)/775.3*100, "%")

# 旧候选对比（Δ_hf 候选口径）
c1 = dress/5
c2 = kappa*kappa*L/10
print("旧候选 dev: kL(1-2s/3)/5 =", (c1-(mN_fw-938.272))/(mN_fw-938.272)*100, "%  k^2L/10 =", (c2-(mN_fw-938.272))/(mN_fw-938.272)*100, "%")
