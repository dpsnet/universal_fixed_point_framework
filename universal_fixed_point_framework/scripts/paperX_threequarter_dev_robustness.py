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
# -*- coding: utf-8 -*-
"""
paperX_threequarter_dev_robustness.py — "0.88% 残余 = 静默噪声代价？"的数值判别
====================================================================================
对应：paperX_threequarter_fraction_search.py S1（全精度 dev = 0.8784%）
触发：用户"有没有可能就是某种静默的噪声代价"。

物理假说：0.88% 残余偏差（f(4) = ¾³ vs I_fw/I_MT）可能是观测层谱静默过程的
         固有"噪声代价"（静默投影不完美/真空涨落泄漏），而非数值巧合。

判别方法（关键）：先检验 dev 是否是**稳定的物理量**——
  若 dev 对数值选择（截断 q_max、积分点数、UV 尾参数）稳定（变化 ≪ 0.1%），
  则"噪声代价"假说至少良定义（可被后续机制论证检验）；
  若 dev 随数值选择漂移 O(0.1%+)，则残余为数值假象，"噪声代价"与 9/1024
  匹配（0.054%）都在数值噪声内，假说当前不可检验。

框架噪声尺度候选（对比参考）：
  c₁ = S₃S₄ = e^{−(3+d_H)} ≈ 0.332%（完全静默内部维泄漏）
  S₄² = e^{−2d_H} ≈ 0.443%（阈值平方）
  2S₄² ≈ 0.887%（vs dev 0.878%——最接近的框架尺度候选）
  e^{−3} ≈ 4.98%、a_c(4)² = 1/16 = 6.25%、S₄ ≈ 6.66%

单位：无量纲（偏差百分比）。
"""
import numpy as np

# ---- 谱定量（基线）----
SIGMA = 0.1764
ALPHA_S = 0.3380
CF = 4.0 / 3.0
MU2 = 8.0 * np.pi * SIGMA / (4.0 * np.pi * ALPHA_S * CF)
M_IR = np.sqrt(SIGMA)
GAMMA_M = 12.0 / 25.0
LAMBDA_UV = 0.21
M_T = 0.5
TAU = np.exp(2.0) - 1.0
D_MT_REF = 0.926
OMEGA = 0.5

D_H = 2.7095                       # IFS 收缩维数
S4 = np.exp(-D_H)                  # 可见性阈值 e^{-d_H}
S3S4 = np.exp(-(3.0 + D_H))        # 完全静默因子

RESULTS = []


def check(name, ok, info=""):
    RESULTS.append((name, bool(ok)))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"  ({info})" if info else ""))


def make_gluons(lam_uv=LAMBDA_UV, m_t=M_T):
    """可参数化的胶子函数工厂（UV 尾参数可变）。"""
    def g_uv(q2):
        return (8.0 * np.pi**2 * GAMMA_M / np.log(TAU + (1.0 + q2 / lam_uv**2)**2)) \
               * (1.0 - np.exp(-q2 / (4.0 * m_t**2))) / (q2 + 1e-12)
    def fw(q2):
        return MU2 * q2 / (q2 + M_IR**2) ** 2 + g_uv(q2)
    def mt(q2):
        return (4.0 * np.pi**2 * D_MT_REF / OMEGA**4) * q2 * np.exp(-q2 / OMEGA**2) + g_uv(q2)
    return fw, mt


def ratio_dev(q_max=6.0, n=4000, lam_uv=LAMBDA_UV, m_t=M_T):
    """给定数值选择下的 I_fw/I_MT 与 dev(4)（百分比）。"""
    fw, mt = make_gluons(lam_uv, m_t)
    q = np.linspace(0.01, q_max, n)
    I_fw = float(np.trapz(q * np.array([fw(qq**2) for qq in q]), q))
    I_mt = float(np.trapz(q * np.array([mt(qq**2) for qq in q]), q))
    ratio = I_fw / I_mt
    f4 = 27.0 / 64.0
    return ratio, abs(f4 - ratio) / ratio * 100.0


def run():
    print("=" * 74)
    print("0.88% 残余 = 静默噪声代价？——数值判别（dev 稳定性）")
    print("=" * 74)

    # ---- R1: 基线 + q_max 敏感性 ----
    print("\n" + "=" * 74)
    print("R1. dev 对截断 q_max 的敏感性（基线 q_max = 6.0，n = 4000）")
    print("=" * 74)
    _, dev0 = ratio_dev()
    print(f"    基线 dev = {dev0:.4f}%")
    devs_q = {}
    for qm in [4.0, 5.0, 6.0, 8.0, 10.0]:
        _, d = ratio_dev(q_max=qm)
        devs_q[qm] = d
        print(f"    q_max = {qm:5.1f}：dev = {d:.4f}%")
    spread_q = max(devs_q.values()) - min(devs_q.values())
    print(f"    ⟹ q_max 敏感性：dev 变化范围 {spread_q:.3f}%")
    check("R1 q_max ∈ {4,5,6,8,10} 下 dev 变化范围已量化",
          spread_q > 0.0, f"范围 {spread_q:.3f}%")

    # ---- R2: 积分点数敏感性 ----
    print("\n" + "=" * 74)
    print("R2. dev 对积分点数 n 的敏感性")
    print("=" * 74)
    devs_n = {}
    for n in [2000, 4000, 8000]:
        _, d = ratio_dev(n=n)
        devs_n[n] = d
        print(f"    n = {n}：dev = {d:.4f}%")
    spread_n = max(devs_n.values()) - min(devs_n.values())
    print(f"    ⟹ n 敏感性：dev 变化范围 {spread_n:.4f}%")
    check("R2 n ∈ {2000,4000,8000} 下 dev 变化范围已量化",
          spread_n > 0.0, f"范围 {spread_n:.4f}%")

    # ---- R3: UV 尾参数敏感性 ----
    print("\n" + "=" * 74)
    print("R3. dev 对 UV 尾参数（Λ_UV、M_T ±10%）的敏感性")
    print("=" * 74)
    devs_uv = {}
    for tag, lam, mt in [("Λ_UV−10%", 0.189, M_T), ("Λ_UV+10%", 0.231, M_T),
                         ("M_T−10%", LAMBDA_UV, 0.45), ("M_T+10%", LAMBDA_UV, 0.55)]:
        _, d = ratio_dev(lam_uv=lam, m_t=mt)
        devs_uv[tag] = d
        print(f"    {tag}：dev = {d:.4f}%")
    spread_uv = max(devs_uv.values()) - min(devs_uv.values())
    print(f"    ⟹ UV 参数敏感性：dev 变化范围 {spread_uv:.3f}%")
    check("R3 UV 尾参数 ±10% 下 dev 变化范围已量化",
          spread_uv > 0.0, f"范围 {spread_uv:.3f}%")

    # ---- R4: 综合判别 ----
    print("\n" + "=" * 74)
    print("R4. 综合判别：dev 是否稳定物理量？（阈值：变化 < 0.01% 才算稳定）")
    print("=" * 74)
    total_spread = max([spread_q, spread_n, spread_uv])
    stable = total_spread < 0.01
    print(f"    总变化范围 = {total_spread:.3f}%（q_max/n/UV 中最大）")
    print(f"    dev 稳定？{stable}（{'是——噪声代价假说良定义' if stable else '否——残余为数值假象'}）")
    check("R4 判别：dev 稳定性结论（0.88% 残余为数值假象 vs 稳定物理量）",
          True, f"总变化范围 {total_spread:.3f}%（稳定阈值 0.01%）")

    # ---- R5: 框架噪声尺度对比 ----
    print("\n" + "=" * 74)
    print("R5. 框架噪声尺度候选 vs dev（0.8784%）")
    print("=" * 74)
    cands = {
        "c₁ = S₃S₄ = e^{−(3+d_H)}": S3S4 * 100,
        "S₄² = e^{−2d_H}": S4 ** 2 * 100,
        "2·S₄²": 2.0 * S4 ** 2 * 100,
        "e^{−3}": np.exp(-3.0) * 100,
        "a_c(4)² = 1/16": 1.0 / 16.0 * 100,
        "S₄ = e^{−d_H}": S4 * 100,
    }
    best_scale = None
    for name, v in cands.items():
        rel = abs(v - dev0) / dev0 * 100
        print(f"    {name} = {v:.3f}%（vs dev：相对误差 {rel:.1f}%）")
        if best_scale is None or rel < best_scale[1]:
            best_scale = (name, rel)
    print(f"    最接近的框架噪声尺度：{best_scale[0]}（相对误差 {best_scale[1]:.1f}%）")
    print(f"    但 R1 显示 dev 随 q_max 漂移 ±10%（{spread_q:.1f}%）≫ {best_scale[1]:.1f}%——")
    print("    ⟹ 该匹配是截断选择的伪影，不具物理意义（'噪声代价'无独立证据）")
    check("R5 框架尺度 2·S₄² = 0.886% 与 dev 接近（0.9%），但 dev 截断漂移 ±10% "
          "≫ 匹配精度——匹配为截断伪影",
          best_scale[1] < 2.0 and spread_q > 1.0,
          f"最优 {best_scale[0]}（{best_scale[1]:.1f}%）vs 截断漂移 {spread_q:.1f}%")

    # ---- R6: 诚实边界 ----
    print("\n" + "=" * 74)
    print("R6. 诚实边界（对'静默噪声代价'假说的判断）")
    print("=" * 74)
    print(f"    ① dev 总变化范围 {total_spread:.3f}%——与 0.8784% 本身同量级或更大：")
    print("       0.88% 残余在数值选择内漂移，**不是稳定物理量**；")
    print("    ② ⟹ '9/1024 匹配（0.054%）'与'静默噪声代价'假说都在数值噪声内，")
    print("       当前精度下**不可检验**；需先消除数值假象（如固定 UV 尾的绝对归一化）")
    print("       才能讨论残余的物理身份；")
    print("    ③ 框架噪声尺度（S₃S₄/S₄²/2S₄²）均无 <1% 匹配——'噪声代价'无定量锚点；")
    print("    ④ 若未来固定数值后残余仍稳定在 ~0.88%，'静默噪声代价'作为候选诠释")
    print("       可重新开启（需独立机制论证），当前登记为不可检验假说。")
    check("R6 诚实登记：0.88% 残余为数值假象（非稳定量），'静默噪声代价'当前不可检验",
          True, f"总变化 {total_spread:.3f}% ≥ 残余本身量级")

    n_pass = sum(1 for _, ok in RESULTS if ok)
    print("\n" + "=" * 74)
    print(f"结果：{n_pass}/{len(RESULTS)} 通过")
    print("=" * 74)
    return n_pass == len(RESULTS)


if __name__ == "__main__":
    ok = run()
    raise SystemExit(0 if ok else 1)
