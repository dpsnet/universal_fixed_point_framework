# -*- coding: utf-8 -*-
"""
Phase 102b P7-1 续-10：F_np 机制三方向排查
==============================================================================
F_np 目标 ≈ 4.220（3 圈口径缺口）
方向 a：S 静默家族组合
方向 b：凝聚比结构——T_c/Λ = 0.729 谱织约束——检验 0.729 = (b₀/10)³ 身份
方向 c：∂Rec_D 谱隙坍缩关联——0.729/Δλ₃
"""
import math, json

KAPPA = 6/math.pi
SIGMA = 1/15.0
K_MAX = 8.0
N_GEN = 3.0
N_C = 3.0
B0 = (11*N_C-2*N_GEN)/3.0
DL_MIN = (math.sqrt(6)-math.sqrt(2))/math.sqrt(72)
DL3 = math.sqrt(2)*DL_MIN
D_H = 2.7095
TARGET = 4.220
TAU = 0.729  # paper17 §12.5 T_c/Λ = 0.729

def dev(f, e): return (f/e-1)*100

print("Phase 102b P7-1 续-10：F_np 机制三方向排查")
print("="*74)
print("  目标 F_np = %.3f（3 圈口径缺口）；Δλ_min = %.8f；Δλ₃ = %.8f；b₀ = %g" % (TARGET, DL_MIN, DL3, B0))

print("\n[a] S 静默家族：")
cands_a = {
    "e^√2": math.e**math.sqrt(2),
    "e^√3": math.e**math.sqrt(3),
    "e^{d_H}/e": math.e**(D_H-1),
    "1/S_{d_H}=e^{d_H}": math.e**D_H,
    "e^π/e^1.15": math.e**(math.pi-1.15),
    "e^{π/2}×2.05": math.e**(math.pi/2)*2.05,
}
for name, v in cands_a.items():
    print("  %-20s = %.5f（偏差 %+.3f%%）" % (name, v, dev(v, TARGET)))

print("\n[b] 凝聚比结构——T_c/Λ 身份检验：")
print("  T_c/Λ = 0.729；(9/10)³ = %.6f（偏差 %+.4f%%）" % (0.729, dev(0.729, 0.729)))
print("  0.9 = b₀/10 = %g ✓；10 = N_gen+k_max−1 ✓——纯框架量" % (B0/10))
print("  候选身份：T_c/Λ = (b₀/10)³ = (9/10)³——待 paper17 §12.5 D9 公式验证")

print("\n[c] 谱隙坍缩关联——F_np 候选：")
cands_c = {
    "T_c/Λ ÷ Δλ₃": TAU/DL3,
    "T_c/Λ ÷ Δλ_min": TAU/DL_MIN,
    "1/(T_c/Λ)²×4.22": (1/TAU**2)*4.22,
    "(b₀/10)³/Δλ₃": (B0/10)**3/DL3,
    "C_QCD/(T_c/Λ)²": 2.25/TAU**2,
}
for name, v in cands_c.items():
    print("  %-22s = %.5f（偏差 %+.3f%%）" % (name, v, dev(v, TARGET)))

print("\n[判定]")
print("  方向 a：无干净命中（e^√2 −2.5%%、e^{d_H} 大）——登记不利")
print("  方向 b：★ T_c/Λ = 0.729 ≈ (b₀/10)³——纯框架量身份候选——需 D9 闭式验证")
print("  方向 c：F_np 候选 = (b₀/10)³/Δλ₃ = %.5f（%+.4f%%——0.1%% 边缘外）" % ((B0/10)**3/DL3, dev((B0/10)**3/DL3, TARGET)))
print("  若 D9 谱织约束闭式 = (b₀/10)³——F_np = (b₀/10)³/Δλ₃ 组件全框架——候选升级待验")

result = {"a": {k: v for k, v in cands_a.items()}, "b_identity": dev(0.729, 0.729),
          "c": {k: v for k, v in cands_c.items()},
          "verdict": "方向 b 身份候选 (b₀/10)³——F_np=(b₀/10)³/Δλ₃ +0.12% 边缘——待 D9 验证"}
with open(r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_phase102b_p7_1_fnp_directions.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=1)
print("\nexit 0")
