#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
dynamic_rg_stepwise_resolution.py — Paper LVII §8.7#5 动力学逐步重解 与 §8.7#5 材料 c 截线的动力学落地

[A] 项① 动力学逐步重解（把 §8.6g 的"逆流代数闭合"升级为实际逐步积分）
    β 形式 ODE：  d ln r / d ln c = β(r) := 1/ζ(r),  ζ(r) = (1+(3/2)√3√r)/(1+√3√r)
    已知（§8.6g）流族 ρ(c)=f⁻¹(c) 是此 ODE 的水平簇解（轨迹即 c=f(r)）。
    本脚本**实际逐步积分**该 ODE（Euler + RK4，中心/前向步进），验证：
      (1) 从普适点 (c₀,r*) 积分去复现整条流族 ρ(c)——逐步重解＝解析流族；
      (2) 逐步积分收敛回 r*（动态固定点在物理截线 c=c₀ 被"逐步重解"得到）；
      (3) 逐步步长 h→0 时数值解一致收敛到解析 r*（收敛阶：Euler O(h)、RK4 O(h⁴)）。
    诚实边界：本脚本证明"流族是自身动力学逐点重解所得"，即把§8.6g 代数闭合
    升级为**实际动力学求解**；"EM 中间级由独立谱流方程涌现"仍开放（§8.7#5 核心）。

[B] 项③ 材料 c 截线的动力学落地
    把 §8.6f/g 的运行反常维度 ζ、β 通量沿流诊断应用到五个 BCS 材料点
    r_mat = r*·a_exp/a_BCS，检验强耦合偏移 |c_mat-c₀| 与 β(r_mat)、ζ(r_mat) 的关联，
    即"强耦合修正是否在流族的运行尺度变化中被 ζ 重新吸收"。
"""
import mpmath as mp

mp.mp.dps = 60
eps = mp.mpf('1e-45')
sqrt3 = mp.sqrt(3)
a_BCS = mp.mpf(1) / mp.mpf('1.764')
c0 = a_BCS ** 3 * (4 * mp.pi)


def f(r):
    return (1 + sqrt3 * mp.sqrt(r)) * r


def zeta(r):
    s = sqrt3 * mp.sqrt(r)
    return (1 + (mp.mpf(3) / 2) * s) / (1 + s)


def beta_of(r):           # β = 1/ζ
    return 1 / zeta(r)


def rho(c):
    r = c
    for _ in range(200):
        nr = r - (f(r) - c) / (1 + sqrt3 * (mp.mpf(3) / 2) * mp.sqrt(r))
        if mp.almosteq(nr, r, rel_eps=mp.mpf('1e-55')):
            return nr
        r = nr
    raise RuntimeError("Newton")


r_star = rho(c0)

print("=" * 80)
print("谱流族：c₀=%.6f  r*=%.10f  1/r*=%.10f" % (float(c0), float(r_star), float(1 / r_star)))
print("β-ODE：d ln r/d ln c = β(r)=1/ζ(r) ∈ (2/3,1)，ζ(r)∈(1,3/2)")
print("=" * 80)

# ================================================================
# [A] 项① 逐步积分 β-ODE 复现流族 / 收敛回 r*
# ================================================================
logc0 = mp.log(c0)
# 目标复现区间 ln c ∈ [ln(0.2), ln(3)]
ln_c_lo, ln_c_hi = mp.log(mp.mpf('0.2')), mp.log(mp.mpf('3'))

def euler_step(lr, dlc):
    return lr + dlc * beta_of(mp.e ** lr)

def rk4_step(lr, dlc):
    b1 = beta_of(mp.e ** lr)
    k2_lr = lr + dlc / 2 * b1
    b2 = beta_of(mp.e ** k2_lr)
    k3_lr = lr + dlc / 2 * b2
    b3 = beta_of(mp.e ** k3_lr)
    k4_lr = lr + dlc * b3
    b4 = beta_of(mp.e ** k4_lr)
    return lr + dlc / 6 * (b1 + 2 * b2 + 2 * b3 + b4)

def integrate(from_lc, to_lc, n, sch):
    h = (to_lc - from_lc) / n
    lr = mp.log(rho(mp.e ** from_lc))
    # 误差用 ln r 绝对误差（ODE 变量是 ln r；log 空间相对误差在 ρ=1 处畸变）
    max_err = mp.mpf('0')
    for i in range(n):
        lr = sch(lr, h)
        c = mp.e ** (from_lc + (i + 1) * h)
        expect = mp.log(rho(c))
        err = abs(lr - expect)
        max_err = max(max_err, err)
    return max_err

print("\n[A] 项① 逐步积分 β-ODE 复现流族 / 收敛回 r*")
print("-" * 80)
print(f"{'方法':<6}{'步数N':>7}{'ln c区间':>16}{'max |Δ ln r|':>16}")
for sch, name in ((euler_step, 'Euler'), (rk4_step, 'RK4')):
    for N in (20, 200, 2000):
        err = integrate(ln_c_lo, ln_c_hi, N, sch)
        print(f"{name:<6}{N:>7}{'[%.2f,%.2f]' % (float(ln_c_lo), float(ln_c_hi)):>16}{float(err):>16.3e}")

# 收敛到 r*：从 c₀ 附近逐步积分回到并越过 c₀，检查 r* 处
def reach_r_star(N):
    h = (logc0 - ln_c_lo) / N
    lr = mp.log(rho(mp.e ** ln_c_lo))
    for i in range(N):
        lr = rk4_step(lr, h)
    return mp.e ** lr
for N in (20, 200, 2000, 20000):
    r_end = reach_r_star(N)
    rel = abs(r_end - r_star) / r_star
    print(f"  RK4 从 ln c=ln(0.2) 逐步积分 {N} 步到 c₀：r_step={float(r_end):.8f}  对 r* 相对误差={float(rel):.2e}")

print("-" * 80)
print("解读：Euler O(h)、RK4 O(h⁴)；逐步积分精确复现解析流族并以收紧步长收敛回 r*。")
print("     ⇒ 流族是β-ODE的动态解，r* 在物理截线 c=c₀ 处被『逐步重解』（动态）取得。")

# ================================================================
# [B] 项③ 材料 c 截线的动力学落地（ζ/β 沿流诊断）
# ================================================================
materials = [("Pb", mp.mpf('0.415')), ("Al", mp.mpf('0.576')),
             ("Sn", mp.mpf('0.542')), ("Nb", mp.mpf('0.519')), ("Hg", mp.mpf('0.438'))]
print("\n[B] 项③ 材料 c 截线 + 运行反常维度诊断 (§8.6f/g 沿流落地)")
print("-" * 88)
print(f"{'材料':<4}{'a_exp':>7}{'Δa%':>7}{'r_mat':>9}{'c_mat':>9}{'c/c0':>8}"
      f"{'ζ(r_mat)':>9}{'β(r_mat)':>9}{'|Δc|/ζ':>10}")
print("-" * 88)
rows = []
for name, a_exp in materials:
    r_mat = r_star * a_exp / a_BCS
    c_mat = f(r_mat)
    ratio = c_mat / c0
    dev_a = float((a_exp / a_BCS - 1) * 100)
    z = zeta(r_mat)
    b = beta_of(r_mat)
    dcoff = abs(float(ratio) - 1) * 100
    rows.append((name, float(a_exp), dev_a, float(r_mat), float(c_mat), float(ratio), float(z), float(b), dcoff, z, b))
    print(f"{name:<4}{rows[-1][1]:>7.4f}{dev_a:>7.2f}{rows[-1][3]:>9.5f}{rows[-1][4]:>9.5f}"
          f"{rows[-1][5]:>8.4f}{float(z):>9.5f}{float(b):>9.5f}{dcoff/float(z):>10.3f}")

print("-" * 88)
z_vals = [r[9] for r in rows]
off_vals = [r[8] for r in rows]       # |Δc| 百分比
b_vals = [r[6] for r in rows]
print("观测：材料的 ζ(r_mat) 沿谱流族随 r_mat 单调增大（与 a_exp 同向：Al ζ=1.310 > Sn > Nb")
print("      > Hg > Pb ζ=1.290），严格复现 §8.6f/g 的 `anom_dim_strictMono`（流上 ζ 严格上升）；")
print("      β(r_mat)=1/ζ 随 a_exp 单调减小。五个 c_mat 互异且被独立能量锚 a_exp 单射选定。")
print("      强耦合材料（Pb/Hg）的 r_mat 落到 r* 下方、c 截线偏移 |Δc| 最大（-33%/-29%），")
print("      落在流族运行尺度 ζ 较低（更近清洁隙极限 1）的一端——强耦合修正即材料在")
print("      谱流族上相对弱耦合普适点 c₀ 的下移，运行尺度诊断 ζ/β 逐材料成立。ALL DONE")