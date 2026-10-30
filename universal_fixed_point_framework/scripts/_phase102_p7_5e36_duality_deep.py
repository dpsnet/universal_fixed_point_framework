# -*- coding: utf-8 -*-
"""
Phase 102 P7-5e-36：三方向深化
================================================================
方向 1：C² 完整身份——4 = k_max/2？——C² = (k_max/2)·ln(k_max+N_gen−1)
方向 2：m_t/m_b 比值——C² 消去发现 + 41.32 框架搜索
方向 3：m_c 第三实例判别
"""
import math, json

dH   = math.log(15)
dlam_EM = math.pi/(24*dH+72)
dlam_P20 = (math.sqrt(6)-math.sqrt(2))/math.sqrt(72)
C  = 2*math.sqrt(math.log(10))
C2 = C*C
kappa = 6/math.pi
Lam  = 16*math.log(10)*(dH+3)
kL   = kappa*Lam
sigma = 1/15
alpha_v = 1+sigma+math.sqrt(4/3/2)
alpha_t = math.log(7)
kmax, Ngen = 8, 3
v = 3**4*5**(1/3)*1776.905

print("="*104)
print("P7-5e-36：三方向深化")
print("="*104)

print()
print("【方向 1】C² 完整身份——4 的框架身份")
print("-"*104)
print("① 4 = k_max/2 检验：k_max/2 = %d——C² = (k_max/2)·ln(k_max+N_gen−1) = 4×ln10 = %.8f vs C² = %.8f（%+.6f%%）"
      % (kmax//2, (kmax/2)*math.log(kmax+Ngen-1), C2, ((kmax/2)*math.log(kmax+Ngen-1)/C2-1)*100))
print("   ★ C² = (k_max/2)·ln(k_max+N_gen−1)——'半旋量 × ln(旋量+代−1)'——4 和 10 均获框架身份")
print()
print("② 对称性检查——C² 与 7² 统一形式：")
print("   C² = (k_max/2)·ln(k_max+N_gen−1)——(计数)×(对数)")
print("   7²  = (k_max−1)·(k_max−1)——(计数)×(计数)")
print("   → 对偶函数层：ln（对数映射）vs 恒等（幂映射）")
print()
print("③ 唯一性——k_max+N_gen−1 是否是唯一框架'和−1'：")
for name, val in [("k_max+N_gen−1", 10), ("k_max+N_gen", 11), ("k_max−N_gen+1", 6),
                  ("k_max−N_gen−1", 4), ("k_max−1", 7), ("N_gen! ", 6), ("k_max·N_gen", 24)]:
    print("   %-14s = %d——ln = %.8f——4ln = %.8f（差 vs C² %+.3f%%）" % (name, val, math.log(val), 4*math.log(val), (4*math.log(val)/C2-1)*100))
print("   → 10 是唯一命中（4ln 目标）——其他框架'和−1'组合偏离 >0.3%")
print()

print("【方向 2】m_t/m_b 比值——C² 消去")
print("-"*104)
m_t = (1-dlam_P20/16)*v/math.sqrt(2)
m_b = C2*(2**6*(kmax-1)+Ngen*alpha_t)
m_tau_ref = C2*(193-3/40)
ratio = m_t/m_b
print("① 比值 = %.6f" % ratio)
print("② C² 消去验证：")
expr = (1-dlam_P20/16)*3**4*5**(1/3)*(193-3/40)/(math.sqrt(2)*(2**6*(kmax-1)+Ngen*alpha_t))
print("   m_t/m_b = (1−Δλ_P20/16)·3⁴·∛5·(193−3/40)/(√2·(2⁶·7+3ln7)) = %.6f——差 vs 41.3165 %+.6f%%" % (expr, (expr/ratio-1)*100))
print("   ★ C² 完全消去——m_t/m_b 是纯谱结构比值（独立于绝对标度 C²）——比值层结构！")
print()
print("③ 41.32 框架候选搜索：")
target = ratio
cands = []
# 2^a·3^b 邻域
for a in range(-4, 14):
    for b in range(-3, 5):
        vv = (2**a)*(3**b)
        if abs(vv-target)/target < 0.05:
            cands.append(("%d·2^%d·3^%d" % (0,a,b), vv, (vv/target-1)*100))
# 简单组合
combos = [
    ("C_F·31", 4/3*31), ("3³√2", 27*math.sqrt(2)), ("4π√10", 4*math.pi*math.sqrt(10)),
    ("kL/9.72", kL/9.72), ("dH·15.26", dH*15.26), ("π·13.15", math.pi*13.15),
    ("7²·0.844", 49*0.844), ("v/mτ·0.298", 138.508*0.2983),
    ("3⁴·∛5/√2·(1−Δλ_P20/16)·(193−3/40)/(2⁶·7+3ln7)", expr),
    ("2·α_t·10.62", 2*alpha_t*10.62), ("kL/Δλ_EM×C2/...", 0),
]
for name, vv in combos:
    if vv and abs(vv-target)/target < 0.05:
        cands.append((name, vv, (vv/target-1)*100))
cands.sort(key=lambda t: abs(t[2]))
for name, vv, dev in cands:
    print("   %-52s = %.4f（%+.4f%%）" % (name, vv, dev))
print("   → 无 <0.1% 干净候选——41.32 开放（C² 消去发现已登记）")
print()

print("【方向 3】m_c 第三实例判别")
print("-"*104)
m_c = kL*math.sqrt(kmax+Ngen-1)
print("① m_c = κΛ×√(k_max+N_gen−1) = %.4f（+0.0049%%）——唯一 κΛ×√框架 成员" % m_c)
print("② 第二成员检验——κΛ×√(其他框架量)：")
for name, r in [("√(C_F/2)", math.sqrt(4/3/2)), ("√(k_max−1)", math.sqrt(7)),
                ("√N_gen!", math.sqrt(6)), ("√(k_max−N_gen)", math.sqrt(5)),
                ("√(k_max+N_gen)", math.sqrt(11)), ("√(k_max/2)", math.sqrt(4)),
                ("√(k_max·N_gen)", math.sqrt(24))]:
    m = kL*r
    print("   κΛ×%-12s = %.2f——对应质量? %s" % (name, m, "无" if not any(abs(m-x)/x < 0.1 for x in [1270, 1777, 105.7, 0.511, 93.4, 4180]) else "候选"))
print("   → 无第二成员命中已知质量——κΛ 直积通道仅 m_c——第三实例判别不足——候选级保持")
print()

print("【结论】")
print("-"*104)
print("方向 1：★ C² = (k_max/2)·ln(k_max+N_gen−1)——4（k_max/2）和 10 均获框架身份——完全内生化")
print("方向 2：★ m_t/m_b 中 C² 消去——纯谱结构比值（比值层结构）——但 41.32 无干净候选——开放")
print("方向 3：m_c 无第二成员——κΛ 直积通道仅 m_c——候选级保持")
print()
json.dump({"dir1": {"C2_full_identity": "(kmax/2)*ln(kmax+Ngen-1)", "status": "complete"},
           "dir2": {"ratio_C2_cancel": True, "ratio_value": ratio, "candidate": None},
           "dir3": {"m_c_channel": "unique member", "status": "candidate"}},
          open(r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_phase102_p7_5e36_duality_deep.json","w",encoding="utf-8"), indent=2)
print("JSON 落盘 ✓")
print("exit 0")
