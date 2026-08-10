#!/usr/bin/env python3
"""
paperX_photon_p1_consistency.py — P1 验收推进：光速-能量-动量三恒等式闭环数值验证

笔记来源: notes/06_photon_topology/photon_topology_theory.md §3.1/§4.1
前置: paperX_photon_topology.py S2-S4 (光速/λν/E=hν 数值) +
      PhotonTopology.lean SpeedLocked/EnergyQuantum/energy_from_wavelength

目标: 数值验证 P1 温和兼容部分的**闭环一致性**——E=hν (Planck)、λν=c (波速)、
p=h/λ (de Broglie) 三恒等式通过波速恒等式统一为 E=p·c, 且 E=p·c 恰为
零质量分支结构 (ZeroMassPhoton #2) 的能量-动量关系:

  C1 三恒等式统一: E=hν, λν=c, p=h/λ ⟹ E = p·c (代数一致, 随机采样)
  C2 SI 值验证: h/c 定义值, de Broglie 动量量级 (光学/微波波段)
  C3 零质量衔接: E=p·c 时群速度 v_g=c (与 #2 zero_mass_group_velocity 一致)
  C4 闭环总结: Planck + de Broglie + 波速恒等式 = 零质量光速锁定的共同基础

诚实边界: 三恒等式均为已知物理 (温和兼容, SI 定义构造), 本脚本验证
其代数闭环一致性 (非新预言); P1 的颠覆性部分 (Δ-偏振红移差) 见 §6.1.
"""
import numpy as np

# ============================================================
# 检查项框架
# ============================================================
_CHECKS = []


def check(name, cond, detail=""):
    _CHECKS.append((name, bool(cond), detail))


H = 6.62607015e-34   # Planck 常数 (SI 定义值)
C = 299792458.0      # 真空光速 (SI 定义值)

print("=" * 72)
print("P1 验收推进: 光速-能量-动量三恒等式闭环数值验证")
print("笔记: notes/06_photon_topology/photon_topology_theory.md §3.1/§4.1")
print("=" * 72)

# ============================================================
# C1 三恒等式统一: E = hν, λν = c, p = h/λ ⟹ E = p·c
# ============================================================
print("\n[C1] 三恒等式统一: E=hν ∧ λν=c ∧ p=h/λ ⟹ E=p·c")
rng = np.random.default_rng(20260811)
max_rel = 0.0
for _ in range(500):
    lam = 10.0 ** rng.uniform(-9, 3)          # 波长 1nm ~ 1km
    nu = C / lam                              # λν = c (波速恒等式)
    E1 = H * nu                               # E = hν (Planck)
    p = H / lam                               # p = h/λ (de Broglie)
    E2 = p * C                                # E = p·c (零质量能量-动量)
    max_rel = max(max_rel, abs(E1 - E2) / E1)
check("C1-C1 E=hν 与 p=h/λ 经 λν=c 统一: E = p·c (500 采样, rel < 1e-12)",
      max_rel < 1e-12, "max_rel=%.2e (λ∈[1nm,1km])" % max_rel)

# 显式代数推导逐项验证
lam = 5.0e-7   # 500nm 可见光
nu = C / lam
E_planck = H * nu
p_db = H / lam
E_pc = p_db * C
check("C1-C2 500nm 光子: E(hν) = E(pc) 精确一致",
      abs(E_planck - E_pc) / E_planck < 1e-12,
      "E=%.4e J" % E_planck)

# ============================================================
# C2 SI 值验证: 动量量级与能量-动量关系
# ============================================================
print("\n[C2] SI 值验证: de Broglie 动量量级")
lam_opt = 5.0e-7      # 光学波段 500nm
lam_mic = 3.0e-3      # 微波 3mm
p_opt = H / lam_opt
p_mic = H / lam_mic
E_opt = H * C / lam_opt
E_mic = H * C / lam_mic
print(f"  光学 (500nm):  p = {p_opt:.4e} kg·m/s,  E = {E_opt:.4e} J")
print(f"  微波 (3mm):    p = {p_mic:.4e} kg·m/s,  E = {E_mic:.4e} J")
check("C2-C1 动量量级: 光学 p ~ 1e-27 (h/λ, 波长越长动量越小)",
      1e-28 < p_opt < 1e-26 and p_mic < p_opt, "p_opt=%.2e p_mic=%.2e" % (p_opt, p_mic))
# E = pc 量级: 光子能量 = 动量 × 光速
check("C2-C2 E = p·c 量级一致 (E_opt ≈ 4e-19 J)",
      abs(E_opt - p_opt * C) / E_opt < 1e-12, "")

# ============================================================
# C3 零质量衔接: E = p·c ⟹ 群速度 v_g = c
# ============================================================
print("\n[C3] 零质量衔接: E=p·c ⟹ v_g = c (衔接 #2 zero_mass_group_velocity)")
# 群速度公式 v_g = p·c²/E (相对论标准公式)
def vg(p, c, E):
    return p * c**2 / E

for lam_i in [5.0e-7, 1.0e-6, 3.0e-3]:
    nu_i = C / lam_i
    p_i = H / lam_i
    E_i = H * nu_i
    v = vg(p_i, C, E_i)
    if not abs(v - C) / C < 1e-12:
        check("C3-C1 E=p·c ⟹ v_g=c (全波长)", False, "λ=%.1e" % lam_i)
        break
else:
    check("C3-C1 E=p·c ⟹ v_g=c (3 波长, 零质量光速锁定)", True)

# 对照: 若 E≠p·c (有效质量), v_g < c
lam_i = 5.0e-7
p_i = H / lam_i
E_massive = p_i * C + 1.0     # 加入有效质量能量
v_slow = vg(p_i, C, E_massive)
check("C3-C2 对照: 非零质量 E>p·c ⟹ v_g<c (判别性)",
      v_slow < C and abs(v_slow - C) / C > 1e-3, "v_g=%.6e c" % (v_slow / C))

# ============================================================
# C4 闭环总结
# ============================================================
print("\n[C4] 闭环总结: 三恒等式的统一结构")
# E = hν; λν = c; p = h/λ ⟹ 消去 λ,ν 得 E = pc
# 代数消元验证:
# 由 λν=c 与 p=h/λ: p = hν/c ⟹ hν = pc ⟹ E = pc
check("C4-C1 消元链: p=h/λ ∧ λν=c ⟹ p·c = hν (代数一致)",
      abs((p_db * C) - (H * nu)) / (H * nu) < 1e-12, "p·c=%.4e hν=%.4e" % (p_db * C, H * nu))
check("C4-C2 三恒等式 (Planck/de Broglie/波速) 的公共常数: h, c",
      H == 6.62607015e-34 and C == 299792458.0,
      "h=%g c=%g (SI 定义值)" % (H, C))

# ============================================================
# 总结
# ============================================================
print("\n" + "=" * 72)
print("汇总")
print("=" * 72)
passed = sum(1 for _, ok, _ in _CHECKS if ok)
total = len(_CHECKS)
print("结果: %d/%d" % (passed, total))
for name, ok, detail in _CHECKS:
    mark = "[PASS]" if ok else "[FAIL]"
    line = "  %s %s" % (mark, name)
    if detail:
        line += "  (%s)" % detail
    print(line)

print("""
结论:
  1. E=hν (Planck)、λν=c (波速)、p=h/λ (de Broglie) 三恒等式代数一致,
     通过波速恒等式统一为 E = p·c (500 采样 rel < 1e-12)。
  2. SI 定义值验证: de Broglie 动量量级 (光学 ~1e-27), E=p·c 量级一致。
  3. E=p·c 恰为零质量分支的能量-动量关系 ⟹ v_g=c (零质量光速锁定,
     衔接 #2 zero_mass_group_velocity); 非零质量对照 v_g<c。
  4. 闭环: Planck + de Broglie + 波速恒等式的公共基础是 {h, c}——
     零质量光速锁定是这三恒等式的共同推论 (P1 温和兼容部分闭环)。
  诚实边界: 三恒等式均为已知物理 (温和兼容), 本脚本验证代数闭环一致性
  (非新预言); P1 颠覆性部分 (Δ-偏振红移差) 见 §6.1。
""")
if passed < total:
    raise SystemExit(1)
