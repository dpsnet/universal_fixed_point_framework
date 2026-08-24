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
paperX_closure_winding.py — 闭合结构方向转变：环绕闭环数值验证（笔记 06_photon_topology 方向 4 §5.5, 2026-08-11）

推进方向 4（命题 2.6 闭合结构方向转变）的定量内容——行波"环绕轴闭合"的数值实现
（图 4 的定量版本）：电磁形变在法向平面内绕传播轴 k 闭环，直线传播 = 环绕闭环的宏观投影。

S1: 圆偏振基矢 ε± 的环绕——Im(ε±*×ε±)·k̂ = ±1（螺旋度定量，拓扑表述 2.5.1）
S2: 相位环绕轨迹——E(t) 在法向平面的圆轨迹（|E|² 恒定，模守恒）
S3: 线偏振 = ε± 等权叠加——无净环绕（Im = 0，非 s=0 本征态）
S4: 直线传播 = 环绕投影——螺旋线在轴向投影为直线（宏观直线运动）
S5: 与拓扑表述 2.5.1 一致（螺旋度 = 手性，环绕定向 = 螺旋度）

诚实边界：圆偏振/横波性为标准电动力学事实（数据核对，非新预言）；
"环绕闭环"为法向平面内场形变周期循环的投影语义（非实体螺旋运动，§5.4）。
"""
import numpy as np

OMEGA = 2.0          # 角频率（任意单位）


def check(name, cond, detail=""):
    status = "PASS" if cond else "FAIL"
    print(f"[{status}] {name}" + (f" — {detail}" if detail else ""))
    return bool(cond)


def im_cross_dot(eps, k):
    """Im(ε*×ε)·k̂——螺旋度/环绕定向"""
    return float(np.imag(np.dot(np.cross(np.conj(eps), eps), k)))


def main():
    print("闭合结构方向转变：环绕闭环数值验证（笔记 §5.5：命题 2.6 行波环绕轴闭合）")
    print("=" * 78)

    # S1: 圆偏振基矢 ε± 的环绕（沿 z 传播，k̂ = ẑ）
    khat = np.array([0.0, 0.0, 1.0])
    ep = np.array([1.0, 1j, 0.0]) / np.sqrt(2)    # ε+（σ+，右旋）
    em = np.array([1.0, -1j, 0.0]) / np.sqrt(2)   # ε-（σ-，左旋）
    s_plus = im_cross_dot(ep, khat)
    s_minus = im_cross_dot(em, khat)
    print(f"\nS1  圆偏振环绕：Im(ε+*×ε+)·k̂ = {s_plus:+.1f}、Im(ε-*×ε-)·k̂ = {s_minus:+.1f}")
    ok1 = abs(s_plus - 1) < 1e-12 and abs(s_minus + 1) < 1e-12
    check("S1  螺旋度定量：Im(ε±*×ε±)·k̂ = ±1（拓扑表述 2.5.1，环绕定向）", ok1)

    # S2: 相位环绕轨迹——E(t) = Re(ε+ e^{-iωt}) 在法向平面圆轨迹
    t = np.linspace(0, 2 * np.pi / OMEGA, 200)
    E = np.zeros((len(t), 3))
    for i, tt in enumerate(t):
        E[i] = np.real(ep * np.exp(-1j * OMEGA * tt))
    r2 = np.sum(E ** 2, axis=1)                     # |E|²（法向平面 x²+y²）
    norm_var = np.max(np.abs(r2 - r2[0]))
    ok2 = norm_var < 1e-12
    check("S2  相位环绕轨迹：E(t) 在法向平面圆轨迹（|E|² 恒定，模守恒）", ok2,
          f"|E|² 最大变化 = {norm_var:.2e}")

    # S3: 线偏振 = ε± 等权叠加——无净环绕
    lin = (ep + em) / np.sqrt(2)                    # 线偏振（x 方向）
    s_lin = im_cross_dot(lin, khat)
    print(f"   线偏振 Im((ε++ε-)*×(ε++ε-))·k̂ = {s_lin:+.2e}")
    ok3 = abs(s_lin) < 1e-12
    check("S3  线偏振 = ε± 等权叠加：无净环绕（Im=0，非 s=0 本征态）", ok3)

    # S4: 直线传播 = 环绕投影——螺旋线在轴向投影为直线
    # 螺旋线 r(t) = (R cos ωt, R sin ωt, vt)；z 投影 = vt（直线）
    R, v = 1.0, 0.5
    hel = np.zeros((len(t), 3))
    for i, tt in enumerate(t):
        hel[i] = [R * np.cos(OMEGA * tt), R * np.sin(OMEGA * tt), v * tt]
    z_proj = hel[:, 2]                               # 轴向投影
    # z 投影为直线：z 与 t 严格线性
    linear_err = np.max(np.abs((z_proj - z_proj[0]) - v * (t - t[0])))
    ok4 = linear_err < 1e-12
    check("S4  直线传播 = 环绕投影：螺旋线轴向投影为直线（宏观直线运动）", ok4,
          f"线性偏差 = {linear_err:.2e}")

    # S5: 与拓扑表述 2.5.1 一致——螺旋度 = 手性（环绕定向）
    # s=+1（右旋 σ+）与 s=-1（左旋 σ-）对应两个环绕定向
    ok5 = (s_plus > 0 and s_minus < 0 and abs(s_plus + s_minus) < 1e-12)
    check("S5  与拓扑表述 2.5.1 一致：螺旋度 s=±1 = 环绕定向（两个手性）", ok5,
          f"s_+=+1（右旋）、s_-=-1（左旋）")

    results = [ok1, ok2, ok3, ok4, ok5]
    print("\n" + "=" * 78)
    print(f"环绕闭环数值验证：{sum(results)}/5 通过")
    if not all(results):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
