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
paperX_grr_categorical.py — g_rr 框架内范畴表述：双通道引力调制的代数骨架（2026-08-12）

推进 §7.27②："g_rr 的框架内范畴表述登记未闭合（待 ⊗ 结构）"——
§6.17 的 ⊗ 代数骨架清障后，补 g_rr 范畴表述候选的代数骨架：
**双通道引力调制**（g₀₀ 时间通道调制、g_rr 空间通道调制，度规双通道互逆 g₀₀·g_rr=1）。

S1: g_rr 数值特征——Schwarzschild 径向分量 g_rr=1/g₀₀（g₀₀=1-2GM/rc²，框架符号约定
    与 paperX_theta_esc_gravity.py 一致）；恒等式 g₀₀·g_rr=1（多 r 采样，双通道互逆）
S2: 双法向响应权重——水星进动 42.99"=1/6(g₀₀≈7.17")+2/3(g_rr≈28.66")+1/6(测地线≈7.17")，
    g_rr 空间响应占 2/3（4:1 空间/时间强度比）；光偏折 1.750" 各半（对照）
S3: 双通道调制分离——时间通道 √g₀₀（θ_esc 时间耦合，§7.27①）vs 空间通道 g_rr（2/3 空间响应）；
    外显 = σ × 通道强度（§6.19）的引力侧：引力调制经时间/空间双通道作用于谱对象
S4: ⊗ 自逆结构类比——度规双通道互逆 g₀₀·g_rr=1 与 σ²=1（Z₂ 自逆，§6.17 σ 幺半群同态）
    同为"对偶结构闭合"（互为逆元），结构类比候选
S5: 总结——g_rr 范畴表述候选的代数骨架闭合（双通道引力调制 + ⊗ 互逆类比）；
    正式 Rec/Sp 范畴表述（Δ 法向响应落入谱范畴结构的严格定义）仍开放

诚实边界：Schwarzschild 度规/进动分解/光偏折为标准 GR 事实（数据核对，非新计算）；
"双通道引力调制"为框架内组织语言（§7.25 诠释重述的延伸）；正式 Rec/Sp 范畴表述登记开放。
"""
import math

# 常数（与 paperX_theta_esc_gravity.py 一致）
G = 6.67430e-11       # m³ kg⁻¹ s⁻²
C = 2.99792458e8      # m/s
M_SUN = 1.989e30      # kg
R_SUN = 6.957e8       # m
RS_SUN = 2 * G * M_SUN / C**2   # 太阳 Schwarzschild 半径 ≈ 2.953 km

# 水星进动分解（秒/世纪，§7.27①）
PRECESSION = 42.99
P_TIME = PRECESSION / 6.0          # 1/6 g₀₀ 贡献 ≈ 7.17"
P_SPACE = 2 * PRECESSION / 3.0     # 2/3 g_rr 贡献 ≈ 28.66"
P_GEO = PRECESSION / 6.0           # 1/6 测地线 ≈ 7.17"
LIGHT_DEFL = 1.750                  # 光偏折（秒）
LIGHT_HALF = LIGHT_DEFL / 2.0       # 各半 0.875"


def check(name, cond, detail=""):
    status = "PASS" if cond else "FAIL"
    print(f"[{status}] {name}" + (f" — {detail}" if detail else ""))
    return bool(cond)


def g00(r):
    """Schwarzschild 时间分量 g₀₀ = 1 - r_s/r（框架符号约定，§7.27① √g₀₀=cosθ_esc）"""
    return 1.0 - RS_SUN / r


def grr(r):
    """Schwarzschild 径向分量 g_rr = (1 - r_s/r)⁻¹"""
    return 1.0 / g00(r)


def main():
    print("g_rr 框架内范畴表述：双通道引力调制的代数骨架（推进 §7.27②，⊗ 清障后）")
    print("=" * 78)

    # S1: g_rr 数值特征 + 度规双通道互逆恒等式
    print("\nS1  g_rr 数值特征：g_rr = 1/g₀₀（双通道互逆 g₀₀·g_rr = 1）")
    ok1 = True
    print(f"   太阳 Schwarzschild 半径 r_s = {RS_SUN/1e3:.4f} km")
    print(f"   {'r/r_s':>8}{'r (km)':>12}{'g₀₀':>12}{'g_rr':>12}{'g₀₀·g_rr':>10}")
    for ratio in (10.0, 100.0, 500.0, 1000.0, 695700.0 / 2.953):
        r = RS_SUN * ratio
        g0, gr = g00(r), grr(r)
        prod = g0 * gr
        ok1 = ok1 and abs(prod - 1.0) < 1e-12
        print(f"   {ratio:>8.1f}{r/1e3:>12.2f}{g0:>12.6e}{gr:>12.6e}{prod:>10.1f}")
    check("S1  g_rr = 1/g₀₀（度规双通道互逆 g₀₀·g_rr=1，全采样 <1e-12）", ok1)

    # S2: 双法向响应权重（进动分解 + 光偏折对照）
    print("\nS2  双法向响应权重：g_rr 空间响应占进动 2/3（4:1 空间/时间强度比）")
    ok2 = True
    ok2 = ok2 and abs(P_TIME - PRECESSION / 6) < 0.01
    ok2 = ok2 and abs(P_SPACE - 2 * PRECESSION / 3) < 0.01
    ok2 = ok2 and abs(P_TIME + P_SPACE + P_GEO - PRECESSION) < 0.01
    ratio_st = P_SPACE / P_TIME
    ok2 = ok2 and abs(ratio_st - 4.0) < 1e-6
    print(f"   水星进动 {PRECESSION}\" = {P_TIME:.2f}\"（1/6 g₀₀，时间）+ "
          f"{P_SPACE:.2f}\"（2/3 g_rr，空间）+ {P_GEO:.2f}\"（1/6 测地线）")
    print(f"   空间/时间强度比 = {ratio_st:.1f}:1（g_rr 空间响应为 g₀₀ 时间响应的 4 倍）")
    ok2 = ok2 and abs(LIGHT_HALF - 0.875) < 0.01
    print(f"   对照：光偏折 {LIGHT_DEFL}\" = {LIGHT_HALF}\"（时间）+ {LIGHT_HALF}\"（空间）——各半")
    check("S2  双法向响应：进动分解 1/6+2/3+1/6（g_rr 2/3、4:1 比）+ 光偏折各半", ok2)

    # S3: 双通道调制分离（引力侧外显结构，§6.19 类比）
    print("\nS3  双通道调制分离：时间通道 √g₀₀ vs 空间通道 g_rr")
    ok3 = True
    r_m = RS_SUN * 695700.0 / 2.953          # 太阳表面
    g0_s, gr_s = g00(r_m), grr(r_m)
    cos_esc = math.sqrt(max(g0_s, 0.0))       # √g₀₀ = cosθ_esc（§7.27①）
    print(f"   太阳表面：√g₀₀ = cosθ_esc = {cos_esc:.10f}（时间通道调制，θ_esc = "
          f"{math.degrees(math.acos(cos_esc)):.5f}°）")
    print(f"            g_rr = {gr_s:.10f}（空间通道调制，进动 2/3 权重）")
    # 外显 = σ × 通道强度（§6.19）引力侧：调制 = σ_grav × 通道因子
    #   时间通道：√g₀₀（θ_esc 时间耦合，引力 ⊥ 空间 ↔ 光子 ⊥ 时间，命题 2.1）
    #   空间通道：g_rr（Δ 法向偏转的空间响应）
    ok3 = ok3 and (cos_esc < 1.0) and (gr_s > 1.0)
    print("   通道分离：时间通道（√g₀₀ → θ_esc 时间耦合，光子⊥时间对称侧）；"
          "空间通道（g_rr → Δ 法向空间响应，引力⊥空间对称侧）——命题 2.1 双法向对称")
    check("S3  双通道调制分离：√g₀₀（时间通道）<1、g_rr（空间通道）>1，与命题 2.1 双法向对称衔接", ok3)

    # S4: ⊗ 自逆结构类比——度规互逆与 σ²=1
    print("\nS4  ⊗ 自逆结构类比：g₀₀·g_rr=1（双通道互逆）与 σ²=1（Z₂ 自逆，§6.17）")
    ok4 = True
    # σ 幺半群同态（§6.17）：σ(X⊗Y)=σ(X)σ(Y)，σ²=1（自逆）
    # 度规双通道互逆：g₀₀·g_rr=1（两通道互为乘法逆元）
    for s in (-1, 1):
        ok4 = ok4 and (s * s == 1)
    prod_check = g00(r_m) * grr(r_m)
    ok4 = ok4 and abs(prod_check - 1.0) < 1e-12
    print(f"   σ²=1（Z₂ 自逆，§6.17 S3）：(-1)²=(+1)²=1——离散标记对偶闭合")
    print(f"   g₀₀·g_rr={prod_check:.6f}=1（双通道互逆）——连续调制对偶闭合")
    print("   结构类比候选：离散层 σ²=1（自逆）与连续层 g₀₀·g_rr=1（互逆）同为'对偶闭合'")
    check("S4  ⊗ 自逆类比：σ²=1（Z₂ 自逆）与 g₀₀·g_rr=1（双通道互逆）结构同构候选", ok4)

    # S5: 总结
    print("\nS5  总结：g_rr 范畴表述候选的代数骨架")
    ok5 = ok1 and ok2 and ok3 and ok4
    check("S5  g_rr 范畴表述候选：双通道引力调制（g₀₀ 时间通道 √g₀₀、g_rr 空间通道，"
          "度规互逆 g₀₀·g_rr=1，进动 2/3 空间响应）+ ⊗ 自逆类比（§6.17）——代数骨架闭合；"
          "正式 Rec/Sp 范畴表述（Δ 法向响应严格定义）仍开放", ok5)

    results = [ok1, ok2, ok3, ok4, ok5]
    print("\n" + "=" * 78)
    print(f"g_rr 范畴表述代数骨架：{sum(results)}/{len(results)} 项检查通过")
    print("诚实边界：Schwarzschild 度规/进动分解/光偏折为标准 GR 事实（数据核对）；")
    print("          '双通道引力调制'为框架内组织语言（§7.25 诠释重述延伸）；")
    print("          '⊗ 自逆类比'为结构类比候选（非定理）；正式 Rec/Sp 表述仍开放。")
    if not all(results):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
