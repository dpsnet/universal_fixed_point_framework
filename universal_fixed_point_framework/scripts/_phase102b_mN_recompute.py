me = 0.51099895
L = 210.219
mud = me*27/4          # 3.44924（新内生）
kappa = 6/3.141592653589793
sigma = 1/15
dress = kappa*L*(1-2*sigma/3)   # kappa*L*43/45
Mud_eff = mud + dress           # 387.094

# 两种 Delta_hf 口径
dh_cand = L*14/15               # Lambda 链候选 196.204
dh_exp = 195.8                  # 实验定标（P7-6b）

print("mud =", mud)
print("Mud_eff =", Mud_eff)
print("dh_cand =", dh_cand, " dh_exp =", dh_exp)

for tag, dh in [("cand", dh_cand), ("exp", dh_exp)]:
    mN_fw = 3*Mud_eff - 3*dh/4
    gap = mN_fw - 938.272
    print("---", tag, "dh =", dh)
    print("  mN_fw =", mN_fw, " gap =", gap, " gap/L =", gap/L)
    c1 = dress/5                 # kappa*L*(1-2sigma/3)/5
    c2 = kappa*kappa*L/10        # kappa^2*L/10
    print("  cand1 kL(1-2s/3)/5 =", c1, " dev =", (c1-gap)/gap*100, "%")
    print("  cand2 k^2L/10 =", c2, " dev =", (c2-gap)/gap*100, "%")
    print("  mN' (cand1) =", mN_fw - c1, " vs 938.272 =", (mN_fw-c1-938.272)/938.272*100, "%")
    print("  mN' (cand2) =", mN_fw - c2, " vs 938.272 =", (mN_fw-c2-938.272)/938.272*100, "%")

# Delta-N 分裂两口径
print("Delta-N via dh_cand =", 1.5*dh_cand, " vs PDG 293.1 =", (1.5*dh_cand-293.1)/293.1*100, "%")
print("Delta-N via dh_exp  =", 1.5*dh_exp, " vs PDG 293.1 =", (1.5*dh_exp-293.1)/293.1*100, "%")

# 新缺口搜索：gap/L = 0.36085 有无干净候选
gap_new = 3*Mud_eff - 3*dh_cand/4 - 938.272
print("gap_new/L =", gap_new/L)
import math
cands = {
    "9/25 (b0/25)": 9/25,
    "4/11": 4/11,
    "kappa/5": kappa/5,
    "sqrt(2/15)": math.sqrt(2/15),
    "kappa^2/10": kappa*kappa/10,
    "2/15*e": 2/15*math.e,
}
for k, v in cands.items():
    print("  ", k, "=", v, " dev =", (v-gap_new/L)/(gap_new/L)*100, "%")
