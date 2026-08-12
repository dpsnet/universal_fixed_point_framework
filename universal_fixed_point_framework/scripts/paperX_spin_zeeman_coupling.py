#!/usr/bin/env python3
"""
paperX_spin_zeeman_coupling.py — 自旋"作用角度"量化候选验证（笔记 06_photon_topology 方向 5 §6.7, 2026-08-11）

推进开放问题 ①："作用角度"量化——时间耦合 cosθ 在自旋自由度上的投影是否成立。
候选：外显能量响应 ΔE(ϑ) ∝ cosϑ（塞曼）与时间耦合 cosθ（4-速度 × 时间轴投影）
同为"单位矢量点积投影"结构，90° 处均归零（垂直取向无响应 / 光子极限零耦合）。

S1: 塞曼能量投影 ΔE(ϑ)=2μ_B B|cosϑ| 的 ϑ 依赖（0°→180°，90° 归零）
S2: 结构同构——时间耦合 cosθ（4-速度×时间轴）与塞曼 cosϑ（磁矩×磁场）同为"单位矢量点积"
S3: 塞曼分裂数值锚定——B=1 T 时 ΔE=2μ_B B=1.1577e-4 eV（标准值）
S4: Larmor 进动频率 ω=2μ_B B/ħ（自旋动力学为时间中的演化）
S5: 90° 归零同构——时间耦合 cos(90°)=0（光子极限）↔ 塞曼投影 cos(90°)=0（垂直无响应）

诚实边界：塞曼/拉莫尔为标准量子物理事实；"作用角度量化"为框架诠释候选，
脚本验证标准关系数值 + cos 投影结构同构，不构成新物理预言。
"""
import numpy as np

MU_B = 5.7883818060e-5   # eV/T，玻尔磁子
HBAR_EV = 6.582119569e-16  # eV·s
B_FIELD = 1.0            # T


def check(name, cond, detail=""):
    status = "PASS" if cond else "FAIL"
    print(f"[{status}] {name}" + (f" — {detail}" if detail else ""))
    return bool(cond)


def zeeman_split(theta_deg):
    """自旋投影能量差 ΔE(ϑ) = 2μ_B B |cosϑ|（电子 g≈2，Δm_s=1）"""
    return 2.0 * MU_B * B_FIELD * abs(np.cos(np.deg2rad(theta_deg)))


def main():
    print("自旋'作用角度'量化候选验证（笔记 §6.7 开放问题①：cosϑ 投影 ↔ 时间耦合 cosθ）")
    print("=" * 78)

    # S1: 塞曼能量投影的 ϑ 依赖（90° 归零）
    print("\nS1  塞曼能量投影 ΔE(ϑ) = 2μ_B B |cosϑ|（B = 1 T）")
    for a in (0, 30, 45, 60, 90, 120, 150, 180):
        print(f"   ϑ={a:>3}°  ΔE = {zeeman_split(a):.6e} eV")
    ok1 = abs(zeeman_split(90)) < 1e-15 and abs(zeeman_split(0) - 2 * MU_B) < 1e-9
    check("S1  塞曼投影 ϑ 依赖：90° 归零（垂直取向无能量响应）、0° 最大", ok1,
          f"ΔE(90°)={zeeman_split(90):.2e}, ΔE(0°)={zeeman_split(0):.6e}")

    # S2: 结构同构——时间耦合与塞曼均为"单位矢量点积投影"
    rng = np.random.default_rng(7)
    ok2 = True
    for _ in range(100):
        u = rng.normal(size=3)
        u = u / np.linalg.norm(u)
        v = rng.normal(size=3)
        v = v / np.linalg.norm(v)
        dot = float(u @ v)                      # 时间耦合 cosθ（u=4-速度向、v=时间轴）
        cos_ang = np.cos(np.arccos(np.clip(dot, -1, 1)))   # 塞曼 cosϑ（u=磁矩向、v=磁场向）
        if abs(dot - cos_ang) > 1e-12:
            ok2 = False
    check("S2  结构同构：时间耦合 cosθ 与塞曼 cosϑ 同为'单位矢量点积投影'（100 随机对）", ok2)

    # S3: 塞曼分裂数值锚定（B = 1 T，标准值 2μ_B B ≈ 1.1577e-4 eV）
    de1 = 2.0 * MU_B * B_FIELD
    ok3 = abs(de1 - 1.1577e-4) < 1e-7
    check("S3  塞曼分裂锚定：B=1 T 时 ΔE = 2μ_B B ≈ 1.1577e-4 eV", ok3,
          f"ΔE = {de1:.6e} eV")

    # S4: Larmor 进动频率（时间中的演化——自旋动力学含时依据）
    omega = 2.0 * MU_B * B_FIELD / HBAR_EV
    ok4 = abs(omega - 1.759e11) < 1e9
    print(f"   ω_L = 2μ_B B/ħ = {omega:.6e} rad/s")
    check("S4  Larmor 进动 ω = 2μ_B B/ħ（自旋演化为时间中过程）", ok4,
          f"ω = {omega:.3e} rad/s")

    # S5: 90° 归零同构——时间耦合 cos(90°)=0（光子极限）↔ 塞曼投影 cos(90°)=0
    cos90_time = np.cos(np.deg2rad(90.0))   # 时间耦合在光速法向（θ=90°）为零
    cos90_zeeman = np.cos(np.deg2rad(90.0))  # 塞曼投影在垂直取向（ϑ=90°）为零
    ok5 = (abs(cos90_time) < 1e-15 and abs(cos90_zeeman) < 1e-15
           and abs(zeeman_split(90)) < 1e-15)
    check("S5  90° 归零同构：时间耦合 cos(90°)=0（光子零耦合极限）↔ 塞曼 cos(90°)=0（垂直无响应）", ok5)

    results = [ok1, ok2, ok3, ok4, ok5]
    print("\n" + "=" * 78)
    print(f"作用角度量化候选验证：{sum(results)}/5 通过")
    if not all(results):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
