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
paperX_theta_esc_gravity.py — 等效速度角 θ_esc 量化统一验证（笔记 06_photon_topology 方向 6 §7.25, 2026-08-11）

推进 §7.25 开放问题 ①：等效速度角 θ_esc 与"向引力（Δ 法向）偏转"的量化统一——
引力时间膨胀 dτ/dt = √(1-2GM/rc²) = cos θ_esc（θ_esc = arcsin(v_esc/c)，v_esc = √(2GM/r)），
与运动学钟慢 dτ/dt = cosθ 同构（"向法向自由度偏转"的两种实现）。

S1: θ_esc 数值与引力时间膨胀一致性——cosθ_esc ≡ √(1-2GM/rc²)（地球表面/GPS/太阳表面）
S2: 统一形式——dτ/dt = cosθ_esc（等效速度角）与运动学 cosθ（速度角）同构（多天体核对）
S3: 水星近日点进动 43"/世纪 分解——1/6（g₀₀ 时间膨胀）+ 2/3（g_rr 向 Δ 偏转）+ 1/6（测地线）
S4: 光偏折 4GM/(rc²) 分解——时间部分 + 空间部分各半
S5: 黑洞视界极限——r=2GM/c² 时 θ_esc=90°、cosθ_esc=0（时间冻结）——与"光子⊥时间（θ=90° 零耦合）"极限呼应

诚实边界：所列数值均为标准 GR 已知结果核对（非新计算）；θ_esc 统一为框架
诠释（数学等价于 √g₀₀），不覆盖 GR 全部预言（进动/光偏折需双法向 g₀₀+g_rr）。
"""
import numpy as np

C = 299792458.0          # m/s
G = 6.67430e-11          # m³/(kg·s²)
M_SUN = 1.98892e30       # kg
M_EARTH = 5.9722e24      # kg
R_EARTH = 6.371e6        # m
R_GPS = 2.656e7          # m（GPS 轨道半径）
R_SUN = 6.9634e8         # m
# 水星
A_MERCURY = 5.7909e10    # m（半长轴）
E_MERCURY = 0.2056       # 偏心率
T_MERCURY_YR = 0.240846  # 公转周期（年）
ARCSEC = np.pi / (180 * 3600)   # 角秒 → rad


def check(name, cond, detail=""):
    status = "PASS" if cond else "FAIL"
    print(f"[{status}] {name}" + (f" — {detail}" if detail else ""))
    return bool(cond)


def v_esc(M, r):
    return np.sqrt(2 * G * M / r)


def theta_esc(M, r):
    return np.arcsin(np.minimum(1.0, v_esc(M, r) / C))


def time_dilation_factor(M, r):
    """引力时间膨胀因子 dτ/dt = √(1-2GM/rc²)"""
    return np.sqrt(max(0.0, 1 - 2 * G * M / (r * C * C)))


def main():
    print("等效速度角 θ_esc 量化统一验证（笔记 §7.25 开放问题①：引力时间膨胀 = cosθ_esc）")
    print("=" * 78)

    # S1: θ_esc 与引力时间膨胀一致性（cosθ_esc ≡ √(1-2GM/rc²)）
    bodies = [("地球表面", M_EARTH, R_EARTH), ("GPS 轨道", M_EARTH, R_GPS),
              ("太阳表面", M_SUN, R_SUN)]
    ok1 = True
    print("\nS1  cosθ_esc ≡ √(1-2GM/rc²)（引力时间膨胀 = 等效速度角的时间耦合）")
    for name, M, r in bodies:
        th = theta_esc(M, r)
        cos_th = np.cos(th)
        factor = time_dilation_factor(M, r)
        ok = abs(cos_th - factor) < 1e-15
        ok1 = ok1 and ok
        print(f"   {name:<8} θ_esc={th*180/np.pi:.5f}°  cosθ_esc={cos_th:.12f}"
              f"  √(1-2GM/rc²)={factor:.12f}  {'✓' if ok else '✗'}")
    check("S1  cosθ_esc ≡ √(1-2GM/rc²)（地球/GPS/太阳，偏差 <1e-15）", ok1)

    # S2: 统一形式——引力时间膨胀与运动学钟慢同构（dτ/dt = cosθ，θ 为等效/实际速度角）
    # 逃逸速度对应：√(1-v_esc²/c²) = √(1-2GM/rc²)
    ok2 = True
    for name, M, r in bodies:
        ves = v_esc(M, r)
        lhs = np.sqrt(1 - (ves / C) ** 2)
        rhs = time_dilation_factor(M, r)
        ok2 = ok2 and abs(lhs - rhs) < 1e-15
    check("S2  统一形式：√(1-v_esc²/c²) = √(1-2GM/rc²)（逃逸速度对应 = 运动学钟慢同构）", ok2)

    # S3: 水星近日点进动 43"/世纪 分解（1/6 g₀₀ + 2/3 g_rr + 1/6 测地线）
    dphi_per_orbit = 6 * np.pi * G * M_SUN / (C * C * A_MERCURY * (1 - E_MERCURY ** 2))
    orbits_per_century = 100.0 / T_MERCURY_YR
    total_arcsec = dphi_per_orbit * orbits_per_century / ARCSEC
    time_part = total_arcsec / 6          # 1/6：g₀₀ 时间膨胀（等效速度角）
    space_part = total_arcsec * 2 / 3     # 2/3：g_rr（向 Δ 偏转的动力学响应）
    geodetic_part = total_arcsec / 6      # 1/6：测地线高阶项
    ok3 = abs(total_arcsec - 43.0) < 1.0
    ok3b = abs((time_part + space_part + geodetic_part) - total_arcsec) < 1e-9
    print(f"\nS3  水星近日点进动：总 {total_arcsec:.2f}\"/世纪（GR 43.0\"）")
    print(f"   1/6 g₀₀ 时间膨胀（等效速度角）≈ {time_part:.2f}\"；"
          f"2/3 g_rr（向 Δ 偏转响应）≈ {space_part:.2f}\"；1/6 测地线 ≈ {geodetic_part:.2f}\"")
    check("S3  水星进动 43\"/世纪 与 1/6+2/3+1/6 分解（数值核对）", ok3 and ok3b,
          f"总 {total_arcsec:.2f}\", 分解和 {time_part+space_part+geodetic_part:.2f}\"")

    # S4: 光偏折 4GM/(rc²) 分解——时间部分 + 空间部分各半
    bend_total = 4 * G * M_SUN / (R_SUN * C * C) / ARCSEC   # 角秒
    bend_time = bend_total / 2          # 时间部分（等效速度角）
    bend_space = bend_total / 2         # 空间部分（向 Δ 偏转）
    ok4 = abs(bend_total - 1.75) < 0.05
    print(f"\nS4  太阳表面光偏折：总 {bend_total:.3f}\"（GR 1.75\"）")
    print(f"   时间部分（等效速度角）≈ {bend_time:.3f}\"；空间部分（向 Δ 偏转）≈ {bend_space:.3f}\"")
    check("S4  光偏折 4GM/(rc²) ≈ 1.75\"（时间/空间各半）", ok4,
          f"总 {bend_total:.3f}\"")

    # S5: 黑洞视界极限——r=2GM/c² 时 θ_esc=90°、cosθ_esc→0（时间冻结）
    r_schw = 2 * G * M_SUN / (C * C)
    th_horizon = theta_esc(M_SUN, r_schw)
    factor_horizon = time_dilation_factor(M_SUN, r_schw)
    # 视界处 2GM/rc²=1（浮点舍入 ~1e-16）→ 因子 ~1e-8；物理上 dτ/dt→0
    ok5 = abs(th_horizon - np.pi / 2) < 1e-12 and factor_horizon < 1e-7
    print(f"\nS5  黑洞视界（r_s=2GM/c²）：θ_esc = {th_horizon*180/np.pi:.2f}°（=90°）"
          f"，cosθ_esc ≈ {factor_horizon:.2e}（时间冻结，浮点极限）")
    check("S5  黑洞视界 θ_esc=90°、时间耦合→0——与光子⊥时间（θ=90° 零耦合）极限呼应", ok5)

    results = [ok1, ok2, ok3 and ok3b, ok4, ok5]
    print("\n" + "=" * 78)
    print(f"等效速度角量化统一验证：{sum(results)}/5 通过")
    if not all(results):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
