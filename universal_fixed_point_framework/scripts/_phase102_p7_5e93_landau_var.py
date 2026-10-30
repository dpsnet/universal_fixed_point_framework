# -*- coding: utf-8 -*-
"""
Phase 102 P7-5e-93：Landau 基变分推导判别——闭式解析来源
================================================================
一阶 Landau 基（ψ ∝ r^|m| e^{−Br²/8}）：E_0 = B/2 − (√B/2)·Γ(|m|+1/2)/Γ(|m|+1)
  过零 B* = [Γ(|m|+1/2)/Γ(|m|+1)]²——渐近 B* ∝ 1/|m|（方向对）但系数差 2（闭式给 2/|m|）
变分攻：ψ ∝ r^|m| e^{−αr²}（α 自由——Coulomb 压缩波函数）——E(α) 最小化——过零 B*
判别：B_var(m) vs 统一闭式 B*(m) = 1/(|m|/2 + 1/7 + 1/(7·2^|m|))
  ——若 B_var ∝ 2/|m|（系数修正）→ 闭式解析来源 = Landau 变分（获机制身份）
"""
import json, os
import numpy as np
from scipy.special import gamma
from scipy.integrate import quad
import warnings
warnings.filterwarnings('ignore')

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"

def E_var(m, B, alpha):
    """变分能量：ψ = N r^|m| e^{−αr²}——H = T + Coul + Zeeman + Diamag"""
    am = abs(m)
    # 归一化：∫r^{2am+1}e^{−2αr²}dr = (1/2)(2α)^{−(am+1)}Γ(am+1)
    N2 = 2.0 * (2*alpha)**(am+1) / gamma(am+1)
    # 期望积分（权重 r^{2am+1}e^{−2αr²}）
    def exp_r2(p):
        return N2 * gamma(am + 1 + p/2) / (2.0**(am+1+p/2) * alpha**(am+1+p/2)) * 0.5 * 2.0**(am+1+p/2) * alpha**(am+1+p/2) / (2*alpha)**(am+1+p/2) * gamma(am+1) / gamma(am+1)
    # 直接：⟨r^p⟩ = N2·∫r^{2am+1+p}e^{−2αr²}dr = N2·(1/2)(2α)^{−(am+1+p/2)}Γ(am+1+p/2)
    def ex_r(p):
        return N2 * 0.5 * (2*alpha)**(-(am+1+p/2)) * gamma(am+1+p/2)
    # ⟨r²⟩, ⟨1/r⟩, ⟨1/r²⟩
    r2 = ex_r(2); invr = ex_r(-1); invr2 = ex_r(-2)
    # T：2D 径向——T = ⟨−(1/2)(d²/dr² + (1/r)d/dr − m²/r²)⟩
    # ψ = r^am e^{−αr²}: ψ'/ψ = am/r − 2αr
    # −(1/2)ψ''/ψ = −(1/2)[(am/r − 2αr)² + d/dr(am/r − 2αr)]
    #              = −(1/2)[am²/r² − 4α·am + 4α²r² − am/r² − 2α]
    #              = −(1/2)[(am²−am)/r² − 4α·am + 4α²r² − 2α]
    # −(1/2r)ψ'/ψ = −(1/2)(am/r² − 2α)
    # +(1/2)m²/r² (角动量项)
    T = (-0.5*((am*am-am)*invr2 - 4*alpha*am + 4*alpha*alpha*r2 - 2*alpha)
         -0.5*(am*invr2 - 2*alpha)
         +0.5*m*m*invr2)
    Vc = -invr
    Vz = m*B/2.0
    Vd = B*B*r2/8.0
    return T + Vc + Vz + Vd

def e_min(m, B):
    """扫描 α 求 E(α) 最小"""
    best = 1e9; best_a = None
    for a in np.linspace(0.01, 2.0, 200):
        e = E_var(m, B, a)
        if e < best:
            best, best_a = e, a
    return best, best_a

print("="*104)
print("P7-5e-93：Landau 基变分推导判别——闭式解析来源")
print("="*104)

KMAX = 8
def closed(m):
    return 1.0/(abs(m)/2.0 + 1.0/(KMAX-1) + 1.0/((KMAX-1) * 2.0**abs(m)))

quantum = {-11: 0.177487, -10: 0.194733, -9: 0.215692, -8: 0.24168,
           -7: 0.27475, -6: 0.31825, -5: 0.37796, -4: 0.46488,
           -3: 0.60237, -2: 0.84884, -1: 1.3720}

hits = 0; total = 0
for m in sorted(quantum, reverse=True):
    lo, hi = 0.05*closed(m), 3.0*closed(m)
    for _ in range(12):
        mid = 0.5*(lo+hi)
        e, a = e_min(m, mid)
        if e > 0:
            hi = mid
        else:
            lo = mid
    bv = 0.5*(lo+hi)
    q = quantum[m]; total += 1
    diff = (bv - q)/q*100
    hit = abs(diff) < 5.0
    hits += hit
    print("  m=%+d: 变分 B_var=%.5f vs 量子 B*=%.5f——差 %+.2f%% %s"
          % (m, bv, q, diff, "★命中" if hit else "✗"), flush=True)

print()
print("  命中 %d/%d（<5%%）——%s" % (hits, total,
    "Landau 变分 = 闭式机制来源" if hits == total else
    "部分命中（高 |m| 倾向）" if hits >= total*0.6 else "变分亦不足——解析来源仍开放"))

json.dump({"closed": {str(k): closed(k) for k in quantum}},
          open(os.path.join(BASE, "_phase102_p7_5e93_landau_var.json"), "w", encoding="utf-8"), indent=1)
print("JSON 落盘 ✓  exit 0")
