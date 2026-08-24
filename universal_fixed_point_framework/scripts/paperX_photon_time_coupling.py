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
paperX_photon_time_coupling.py — 时间耦合线数值验证（paper44 §7.5 开放问题 #1 推进, 2026-08-11）

推进方向：笔记 06_photon_topology/photon_first_principle_origin.md 方向 6（v0.25），
对应 paper44 推论 2.1 / 命题 2.7 / 洛伦兹变换时间耦合诠释。

S11: γ 极限收敛——v→c 时 dτ/dt = 1/γ → 0（钟慢极限，推论 2.1 γ→∞ 数值层）
S12: cosθ 时间耦合一致性——cosθ(θ=arcsin(v/c)) ≡ 1/γ（角度/γ 双路径等价）
S13: boost 三角参数化一致性——secθ/tanθ 参数化 ≡ 标准 γ/γβ（洛伦兹诠释数值等价）
S14: 牛顿斜线 vs 相对论渐近——v(t) 对比：直线穿过光速 vs 渐近贴近 c（θ(t)→90°）
S15: 光速锁定复核——E=pc（零质量，Planck+de Broglie+波速三恒等式）⟹ v=c

诚实边界：均为标准相对论/量子关系的数值复核（时间耦合语言诠释），非新物理预言；
与推论 2.1 的"递归静止"极限一致；γ→∞ 为渐近（v<c 不可达）。
"""
import numpy as np

C = 299792458.0  # m/s，SI 测定值


def gamma(v):
    return 1.0 / np.sqrt(1.0 - (v / C) ** 2)


def check(name, cond, detail=""):
    status = "PASS" if cond else "FAIL"
    print(f"[{status}] {name}" + (f" — {detail}" if detail else ""))
    return bool(cond)


def main():
    print("时间耦合线数值验证（paper44 推论 2.1/命题 2.7 数值层，开放问题 #1 推进）")
    print("=" * 78)

    # S11: γ 极限收敛（钟慢极限）
    vs = np.array([0.0, 0.5, 0.9, 0.99, 0.999, 0.9999, 0.99999, 0.999999,
                   (1 - 1e-13)]) * C
    gs = gamma(vs)
    ratios = 1.0 / gs          # dτ/dt = 1/γ
    print("\nS11  γ→∞ 极限收敛（v→c 时 1/γ→0，推论 2.1 钟慢极限数值层）")
    for v, g, r in zip(vs / C, gs, ratios):
        print(f"   v/c={v:<19.16f}  γ={g:<14.2f}  dτ/dt={r:.6e}")
    ok11 = (ratios[-1] < 1e-6) and np.all(np.diff(ratios) < 0)
    check("S11  γ→∞：1/γ 单调递减至 <1e-6（渐近零，不可达）", ok11,
          f"v=(1-1e-13)c 时 1/γ={ratios[-1]:.2e}")

    # S12: cosθ 时间耦合一致性（θ=arcsin(v/c)，cosθ ≡ 1/γ）
    v_test = np.array([0.0, 0.3, 0.5, 0.7, 0.9, 0.99, 0.999]) * C
    th = np.arcsin(v_test / C)
    cos_th = np.cos(th)
    inv_g = 1.0 / gamma(v_test)
    err12 = np.max(np.abs(cos_th - inv_g))
    check("S12  cosθ(θ=arcsin(v/c)) ≡ 1/γ（时间耦合 = cosθ 数值等价）", err12 < 1e-12,
          f"max|cosθ - 1/γ| = {err12:.2e}")

    # S13: boost 三角参数化一致性（secθ/tanθ ≡ γ/γβ）
    # 标准：ct'=γ(ct-βx), x'=γ(x-βct)；三角：ct'=secθ·ct-tanθ·x, x'=secθ·x-tanθ·ct（c=1 单位）
    beta = np.array([0.0, 0.2, 0.5, 0.8, 0.95])
    ct, x = 3.0, 1.0
    for b in beta:
        g = 1.0 / np.sqrt(1 - b * b)
        th2 = np.arcsin(b)
        # 标准（c=1）
        ct_std = g * (ct - b * x)
        x_std = g * (x - b * ct)
        # 三角
        ct_tri = np.cos(th2) ** -1 * ct - np.tan(th2) * x
        x_tri = np.cos(th2) ** -1 * x - np.tan(th2) * ct
        assert abs(ct_std - ct_tri) < 1e-12 and abs(x_std - x_tri) < 1e-12
    check("S13  boost 三角参数化(secθ/tanθ) ≡ 标准(γ/γβ)——洛伦兹诠释数值等价", True,
          "5 个 β 值全部一致（<1e-12）")

    # S14: 牛顿斜线 vs 相对论渐近（匀加速 a=g，t∈[0,5yr]）
    A = 9.8
    t = np.linspace(0, 5 * 365.25 * 86400, 500)
    v_newt = A * t / C                      # 牛顿：线性，穿过光速
    v_rel = (A * t / C) / np.sqrt(1 + (A * t / C) ** 2)   # 相对论：渐近 1
    crossing = np.argmax(v_newt >= 1.0) if np.any(v_newt >= 1.0) else None
    ok14a = crossing is not None and v_newt[crossing] >= 1.0
    ok14b = v_rel.max() < 1.0 and abs(v_rel[-1] - 1.0) < 0.05
    check("S14  牛顿 v/c=at 直线穿过光速（超光速不自洽）", ok14a,
          f"穿过点 t≈{t[crossing]/86400/365.25:.2f} yr" if crossing else "未穿过")
    check("S14b 相对论 v/c=at/√(1+a²t²) 渐近贴近 1（θ→90°，永不到达）", ok14b,
          f"5yr 末 v/c={v_rel[-1]:.4f}，θ={np.degrees(np.arcsin(v_rel[-1])):.2f}°")

    # S15: 光速锁定复核（E=pc，三恒等式 ⟹ v=c）
    h_planck = 6.62607015e-34
    nu = 5e14  # Hz
    lam = C / nu
    E = h_planck * nu                      # Planck: E=hν
    p = h_planck / lam                     # de Broglie: p=h/λ
    v_g = E / p                            # v = ∂E/∂p = c
    err15 = abs(v_g - C) / C
    check("S15  光速锁定 E=pc（Planck+de Broglie+波速恒等式）⟹ v=c", err15 < 1e-12,
          f"v_g/c = {v_g/C:.15f}")

    ok12 = err12 < 1e-12
    passed = sum(1 for _ in [ok11, ok12, True, ok14a, ok14b, err15 < 1e-12] if _)
    print("=" * 78)
    print(f"通过 {passed}/6（S11-S15 共 6 项断言）")
    print("诚实边界：γ→∞ 为渐近极限（v<c 不可达）；cosθ=1/γ 与 boost 三角参数化"
          "为数学等价重述；光速锁定为三恒等式共同推论（框架推导复核）。")
    assert passed == 6, "存在未通过断言"


if __name__ == "__main__":
    main()
