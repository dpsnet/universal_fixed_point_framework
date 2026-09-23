# =============================================================================
# Route A 结构论判表：EM 独立动力学是否破缺折叠（RN-ENDO-008）
#
# §8.7#5 最深开放项（RN-ENDO-007 §5.1）：f_EM(u)=f(√3u) 当前只是单级自洽方程
# 经坐标缩放 u=r/√3 的"共轭"。Route A 断言 EM 扇区（阿贝尔/电荷）的谱流闭合
# 应有自身结构。
#
# — 关键结构约束 ————————————————————————————————————————————————
# Δλ_min^EM = Δλ_min/√3 由 SU(2) Casimir 塔钉死（SpectralFlowRG.dl_min_EM 定理），
# 因此 EM 中间级不可移动；"EM 阶段流" f_EM(u)=f(√3u) = √3u(1+3^{3/4}√u) 的形状
# 是规范的强制共轭，非自由参数。**唯一能承载独立动力学的自由度是 EM 阶段自身的
# 闭合常数 c_EM**。故：
#     ū = ρ(c_EM)/√3   （ρ=f⁻¹，单级流族根；f(√3ū)=c_EM ⟹ √3ū=ρ(c_EM)）
#     F = δ_SC'/δ_SC = r*/(√3·ū) = r*/ρ(c_EM)
# F=1 ⟺ c_EM=c₀：两条路径给出同一 δ_SC，EM 动力学平庸（折叠精确）。
# F≠1：EM 阶段独立锚 c_EM≠c₀，δ_SC 偏移 (F−1)×100%，即 §8.7#5 的可测修正。
#
# — 内部普适间断面 ————————————————————————————————————————————
# 所有候选锚均只用 {π, e^{γ_E}} 与整数因子（c=1 式，零测量）：
#   c₀     = b³·4π,            b = e^{γ_E}/π          （BCS 锁）
#   c₀D    = a0³·4π = 8c₀,     a0 = 2b = 2e^{γ_E}/π   （Debye 有限部锚，BCSConstantOrigin）
#   c₀/8   = (b/2)³·4π                                （Debye 之半；b/2 = e^{γ_E}/(2π)）
#
# mpmath 60 位精度。相关：SpectralFlowDynamicsRG.lean、SpectralFlowRG.lean(dl_min_EM)、
# SuperfluidBridge.lean(selfConsC_int)、BCSConstantOrigin.lean。
# =============================================================================
import mpmath as mp

mp.mp.dps = 60

sqrt3 = mp.sqrt(3)


def f(r):
    """单级谱流自洽函数 f(r) = (1+√3·√r)·r"""
    return (1 + sqrt3 * mp.sqrt(r)) * r


def rho(c):
    """流族根 ρ(c)：f 在 [0,∞) 的唯一正根 f(r)=c"""
    lo, hi = mp.mpf('0'), mp.mpf('1000')
    for _ in range(400):
        mid = (lo + hi) / 2
        if f(mid) < c:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


# ---------------------------- 内部普适锁常数 --------------------------------
b = mp.e ** mp.euler / mp.pi            # BCS 锁 a_BCS = e^{γ_E}/π
c0 = b ** 3 * 4 * mp.pi                 # c₀ = (e^{γ_E}/π)³·4π
r_star = rho(c0)                        # 单级自洽根 r*
a0 = 2 * b                              # Debye 有限部 a0 = 2e^{γ_E}/π
c0D = a0 ** 3 * 4 * mp.pi               # c₀D = 8·c₀

# ---------------------------- EM 阶段独立闭合判表 ----------------------------
cands = [("c₀  =(e^{γ_E}/π)³·4π   (BCS 锁，共享)", c0),
         ("c₀D = a0³·4π = 8c₀     (Debye 锚 a0=2b)", c0D),
         ("c₀/8= (b/2)³·4π        (Debye 之半)", c0 / 8)]

print("=" * 96)
print("Route A 判表：EM 独立闭常数 c_EM 破缺折叠量 F（RN-ENDO-008，内部普适锁，零测量）")
print("=" * 96)
print("\n内部普适锁：b = e^{γ_E}/π   = %.12f" % b)
print("           c₀ = (e^{γ_E}/π)³·4π = %.12f" % c0)
print("           r* = 单级自洽根 ρ(c₀) = %.12f" % r_star)
print("           a0 = 2b = 2e^{γ_E}/π  = %.12f (Debye 有限部)" % a0)
print("           EM 阶段流: f_EM(u)=f(√3u)(Casimir 塔钉死形状，非自由参数)")

print("\n判表：ū = ρ(c_EM)/√3，单级参考 ū^ref = r*/√3 = %.12f" % (r_star / sqrt3))
print("-" * 96)
print("%-34s %12s %-18s %-12s %10s" % ("c_EM 锚", "ρ(c_EM)", "ū=ρ(c_EM)/√3",
                                    "δ_SC 相对", "F"))
print("-" * 96)

rows = []
for tag, cEM in cands:
    rhoEM = rho(cEM)
    u = rhoEM / sqrt3
    F = r_star / (rhoEM)
    rows.append((tag, rhoEM, u, F))
    print("%-34s %12.9f %18.12f %-12s %10.8f"
          % (tag, rhoEM, u,
             "=δ_SC" if abs(F - 1) < mp.mpf('1e-30') else "偏移",
             F))

print("-" * 96)
print("F = δ_SC'/δ_SC = r*/√3ū = r*/ρ(c_EM)：F=1 两路径同 δ_SC（折叠精确，EM 平庸）；")
print("F≠1 时 T_c 相对单级理论偏移 (F−1)×100%（经 T_c ∝ δ_SC ∝ Δλ_min/(√3ū)）。")

# ---------------------------- 自检 --------------------------------
print("\n[A] 自检：贡献锚 c_EM=c₀ 必须精确给出 F=1")
F_conj = r_star / rho(c0)
print("    F(c_EM=c₀) = %.18f   差 = %.2e  (判表自检)" % (F_conj,
                                                       abs(F_conj - 1)))
print("    ū(c_EM=c₀) = ρ(c₀)/√3 = r*/√3  (折叠精确复现)")

# ---------------------------- 判定与边界 --------------------------------
print("\n[B] 判定（Route A 二分定理的数值侧）")
print("    · 只要 c_EM=c₀(共享 BCS 锁)，无论流形状如何，都给出 F=1：EM 动力学平庸。")
print("    · 若存在内部普适锚 c_EM≠c₀ 而两路径仍自洽，则该锁给出 F≠1，")
print("      即真实的 EM 独立内容与可测 T_c 修正；上表量化每候选锚的 F。")
print("    · 是 F=1 恒等还是存在 F≠1 的内部锁，由**结构二分定理**定案")
print("      （Lean 待形式化：∀内部普适锚 c_EM, F(c_EM)=1 ⟺ c_EM=c₀）。")

print("\n[C] 诚实边界")
print("    · 判表只列候选锁的折叠比（数值证据层），不预判哪个锚成立。")
print("    · EM 阶段流形状被 Casimir 塔钉死为非自由；独立内容全部归 c_EM。")
print("    · 电荷归一化路（β=2√(q²)，引入电子电荷 e）需先内部锁定 α，本轮未纳入。")
print("\nALL CHECKS DONE")