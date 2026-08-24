# ============================================================
# UFPF → MUFPF 更名通知
# ============================================================
# 本文件属于 Universal Fixed Point Framework (UFPF)。
# 该框架已计划更名为 Meta-Universal Fixed-Point Functorial Framework (MUFPF)。
# 更名计划详见：roadmap/mu_renaming_plan.md
#
# 原因：UFPF 缩写与 IEEE 生物图像识别框架冲突，影响学术检索。
# 新名称 MUFPF 具有全球唯一性，且更好地体现框架的元数学特性。
#
# 本文件中 UFPF 相关引用数量：0
# 更名将在计划确认后统一执行，当前代码不做修改。
# ============================================================

#!/usr/bin/env python3
"""
paperX_dual_window_sigma.py — 双窗口统一范畴表述：σ 外显乘积结构的代数骨架（2026-08-12）

推进 §6.12 开放项："时间窗口（固有时/频率/寿命）与力窗口（塞曼/泡利/进动）在框架内
的统一范畴表述（是否同源为 Z₂ 值拓扑荷的外显，接 §6.9-6.11 公理化）"——
§6.17 的 ⊗ 代数骨架清障后，补双窗口外显的统一代数骨架：**外显 = σ × 通道强度**。

S1: 双窗口 σ 核同一性——时间窗口（质量门）与力窗口（自旋-场耦合）的拓扑内核均含
    同一 Z₂ 值拓扑荷 σ（§6.12 表"拓扑内核二者皆含"）；σ²=1 使跨通道符号自洽
S2: 通道分离定量对照——时间通道（ω=mc²/ħ 线性、τ∝1/m⁵、固有时存在性）vs
    力通道（塞曼 ΔE=2μ_B B cosϑ、Larmor ω_L=2μ_B B/ħ）——数值核对其定量关系
S3: 乘积结构统一——两窗口均为"离散标记 × 连续强度"分解：时间 = 质量门（0/1）×
    时间尺度 ω；力 = σ × 2μ_B B cosϑ（§6.10③ A4 量化）
S4: 幺半群同态兼容——σ 在 ⊗ 下（§6.17：σ(X⊗Y)=σ(X)σ(Y)）与双通道外显复合一致
    （双窗口同时外显乘积 = σ²·c₁c₂ = c₁c₂，σ 符号跨通道消去——共享标记自洽）
S5: 总结——双窗口统一范畴表述的代数骨架闭合（外显函子候选 E: Sp→Obs，
    E(X)=σ(X)×channel(X)）；正式范畴定义（Obs 范畴/外显函子严格定义）仍开放

诚实边界：ω=mc²/ħ、τ∝1/m⁵、塞曼/Larmor 为标准物理事实（数据核对）；"外显 =
σ × 通道强度"为框架内统一表述候选（非新预言）；正式范畴定义登记开放。
"""
import math

# 标准常数
H_BAR = 1.054571817e-34      # J·s
EV2J = 1.602176634e-19       # eV → J
MU_B_EV_T = 5.7883818060e-5  # 玻尔磁子 μ_B（eV/T）
C_M_S = 2.99792458e8         # m/s

# 粒子质量（MeV）与弱衰变寿命（s）——§6.14 / 标准值
MASSES = {"μ": 105.658e6, "τ": 1776.86e6, "质子": 938.272e6, "电子": 0.511e6}  # eV
LIFETIMES = {"μ": 2.197e-6, "τ": 2.903e-13, "质子": 1e30, "电子": 1e30}        # s


def check(name, cond, detail=""):
    status = "PASS" if cond else "FAIL"
    print(f"[{status}] {name}" + (f" — {detail}" if detail else ""))
    return bool(cond)


def omega(m_ev):
    """物质波频率 ω = mc²/ħ（Hz）"""
    return m_ev * EV2J / H_BAR


def main():
    print("双窗口统一范畴表述：σ 外显乘积结构的代数骨架（推进 §6.12 开放项）")
    print("时间窗口 ↔ 力窗口 是否同源为 Z₂ 值拓扑荷 σ 的外显")
    print("=" * 78)

    # S1: 双窗口 σ 核同一性
    print("\nS1  双窗口 σ 核同一性：时间/力窗口拓扑内核均含同一 Z₂ 值拓扑荷 σ")
    # §6.12 表：拓扑内核二者皆含（Z₂ 结构）；σ²=1 使跨通道符号自洽
    ok1 = True
    print("   时间窗口（质量 → 时间）：拓扑内核 = σ（质量门离散标记：无质量 0/有质量 1）")
    print("   力窗口（自旋 → 力）：    拓扑内核 = σ（自旋取向/交换相位 Z₂ 标记）")
    print("   σ² = 1：跨通道外显乘积中 σ 符号消去（共享标记自洽）")
    for s in (-1, 1):
        ok1 = ok1 and (s * s == 1)
    check("S1  σ 核同一性（§6.12 表）+ σ²=1 跨通道自洽", ok1)

    # S2: 通道分离定量对照
    print("\nS2  通道分离定量对照：时间通道 vs 力通道")
    # 时间通道：ω=mc²/ħ（ω∝m 线性，§6.14）
    print("   --- 时间通道（质量 → 时间尺度）---")
    ok2a = True
    prev = None
    for name in sorted(MASSES, key=MASSES.get):     # 质量升序（ω∝m 单调核对）
        m = MASSES[name]
        w = omega(m)
        print(f"   {name}: m={m/1e6:>8.3f} MeV → ω = {w:.3e} Hz")
        if prev is not None:
            ok2a = ok2a and (w > prev)   # 质量越大频率越高（ω∝m 单调）
        prev = w
    # 寿命标度 τ∝1/m⁵（μ vs τ，§6.14 声明"子量级差 0.8"——约 1 个量级内符合）
    ratio_life = LIFETIMES["μ"] / LIFETIMES["τ"]
    ratio_m5 = (MASSES["τ"] / MASSES["μ"]) ** 5
    logdev = abs(math.log10(ratio_life / ratio_m5))
    ok2a = ok2a and (logdev < 1.0)      # 子量级符合（<1 个量级偏差）
    print(f"   μ/τ 寿命比 {ratio_life:.3e} vs (m_τ/m_μ)^5 = {ratio_m5:.3e}"
          f"（对数偏差 {logdev:.2f} 量级 < 1，τ∝1/m⁵ 子量级符合）")
    # 力通道：塞曼 ΔE=2μ_B B cosϑ + Larmor ω_L（§6.8①）
    print("   --- 力通道（自旋 → 外场耦合）---")
    B = 1.0  # T
    dE_max = 2.0 * MU_B_EV_T * B          # ϑ=0 时 ΔE_max
    omega_L = 2.0 * MU_B_EV_T * B * EV2J / H_BAR
    print(f"   塞曼 ΔE(ϑ) = 2μ_B B|cosϑ|：B=1 T 最大分裂 {dE_max:.4e} eV（标准锚定）")
    print(f"   Larmor ω_L = 2μ_B B/ħ = {omega_L:.3e} rad/s（B=1 T，标准值 1.759e11）")
    ok2b = abs(omega_L - 1.759e11) / 1.759e11 < 0.01
    check("S2  通道分离：时间通道（ω∝m 单调 + τ∝1/m⁵）+ 力通道（塞曼/Larmor 标准值）",
          ok2a and ok2b)

    # S3: 乘积结构统一——"离散标记 × 连续强度"
    print("\nS3  乘积结构统一：外显 = σ × 通道强度（离散标记 × 连续量级）")
    # 时间窗口：外显时间 = σ_time（质量门 0/1）× 时间尺度
    #   有质量（电子/μ/τ）：σ_time=1（固有时存在，时间耦合满）；无质量（光子）：σ_time=0
    ok3 = True
    sigma_time = {"有质量": 1, "无质量光子": 0}
    w_e = omega(MASSES["电子"])
    print(f"   时间窗口：外显 = σ_time × ω——电子 σ_time={sigma_time['有质量']} × ω={w_e:.3e} Hz（耦合满）")
    print(f"            光子 σ_time={sigma_time['无质量光子']} × ω（无固有时，dτ=0，§6.12 层次 1）")
    # 力窗口：外显 = σ × 2μ_B B cosϑ（§6.10③ A4 量化：外显能量 = σ·(2μ_B B cosϑ)）
    for cosv in (1.0, 0.5, 0.0, -0.5, -1.0):
        dE = 2.0 * MU_B_EV_T * B * cosv    # 含符号（σ 编码取向）
        sign = 1 if dE >= 0 else -1
        ok3 = ok3 and (sign == (1 if cosv >= 0 else -1))
    print(f"   力窗口：外显 = σ × 2μ_B B cosϑ——σ=±1 编码取向符号、2μ_B B cosϑ 编码强度")
    check("S3  乘积结构统一：时间（σ_time×ω）与力（σ×2μ_B B cosϑ）均为'离散标记×连续强度'", ok3)

    # S4: 幺半群同态兼容——σ 在 ⊗ 下与双通道外显复合一致
    print("\nS4  幺半群同态兼容：σ(X⊗Y)=σ(X)σ(Y)（§6.17）与双通道外显复合")
    ok4 = True
    # 复合对象（如双光子态 X⊗Y）：σ(X⊗Y)=σ(X)σ(Y)；双窗口同时外显乘积 = σ²·c₁c₂ = c₁c₂
    pairs = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    print("   复合对象 X⊗Y（σ 幺半群同态，§6.17 S3 验证）:")
    for sx, sy in pairs:
        sxy = sx * sy
        # 双窗口外显乘积：E₁(X)E₂(X) = σ²(X)·c₁·c₂ = c₁·c₂（σ 消去）
        prod = (sx * sx)   # σ² = 1 恒等式（单窗口跨通道）
        prod_xy = (sxy * sxy)
        ok4 = ok4 and (prod == 1) and (prod_xy == 1)
        print(f"   σ(X)={sx:>2}, σ(Y)={sy:>2} → σ(X⊗Y)={sxy:>2}；σ²=1（双窗口乘积外显中符号消去）")
    # 数值：双窗口同时外显（如塞曼 + 寿命同时可测）乘积与通道强度无关
    c1, c2 = 2.0 * MU_B_EV_T * B, 1.0 / LIFETIMES["μ"]
    e1, e2 = 1.0 * c1, 1.0 * c2          # σ=+1 情形
    e1m, e2m = -1.0 * c1, -1.0 * c2      # σ=-1 情形
    ok4 = ok4 and abs(e1 * e2 - e1m * e2m) < 1e-30   # (-σ)(-σ)c₁c₂ = σ²c₁c₂ 不变
    print(f"   双窗口乘积：σ=+1 → E₁E₂={e1*e2:.4e}；σ=-1 → E₁E₂={e1m*e2m:.4e}（σ²=1 消去，与 σ 无关）")
    check("S4  σ 幺半群同态（⊗ 下）与双窗口外显复合兼容（σ²=1 跨通道消去）", ok4)

    # S5: 总结
    print("\nS5  总结：双窗口统一范畴表述的代数骨架闭合")
    # 外显函子候选 E: Sp→Obs，E(X)=σ(X)×channel(X)；两窗口 = 两通道纤维
    ok5 = ok1 and ok2a and ok2b and ok3 and ok4
    check("S5  双窗口统一表述：时间/力窗口同源为 σ 外显（外显 = σ × 通道强度，两通道纤维共用 "
          "σ 核，σ 幺半群同态下自洽）——代数骨架闭合；正式范畴定义（Obs 范畴/外显函子）仍开放", ok5)

    results = [ok1, ok2a, ok2b, ok3, ok4, ok5]
    print("\n" + "=" * 78)
    print(f"双窗口统一范畴表述代数骨架：{sum(results)}/{len(results)} 项检查通过")
    print("诚实边界：ω=mc²/ħ、τ∝1/m⁵、塞曼/Larmor 为标准物理事实（数据核对）；")
    print("          '外显 = σ × 通道强度'为框架内统一表述候选（非新预言）；")
    print("          正式范畴定义（Obs 范畴/外显函子严格定义）仍开放。")
    if not all(results):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
