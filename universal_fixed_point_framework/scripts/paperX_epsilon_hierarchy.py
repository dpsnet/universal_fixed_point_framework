#!/usr/bin/env python3
"""
paperX_epsilon_hierarchy.py — ε 与层次距离猜想的判别分析（2026-07-29）

猜想（§6.3 开放问题）：
  −ln(ε)/(3·d_H) ≈ √2π，其中 ε = 8.12×10⁻¹⁷（Paper II 预测），
  3·d_H 是层次 0→3 的谱间隙距离。

判别程序（四条独立判据）：
  1. 不确定度预算：失配是否在数据精度内？（统计显著性）
  2. 精确形式可证伪检验：H₁: ε = e^{−3·d_H·√2π} 的预测值与 Paper II 值比较
  3. δ 无关性：失配是否可被 d_H 的 δ 修正吸收？（v1.4/v1.31 遗留问题）
  4. 多重比较基线：√2π 在候选常数族中的排名与"偶然接近"的先验概率

结论（剧透）：猜想**不通过**全部四条判据 → 从"推测性"降级为
"已判别排除"（负结果闭合）。
"""

import numpy as np

eps = 8.12e-17
ln_eps = -np.log(eps)
d_fit = 2.7095
d0 = np.log(15)
d_exact = 2.70949946  # v1.31: 精确固定点 d(√5)
s2pi = np.sqrt(2) * np.pi

print("=" * 74)
print("S1 不确定度预算：失配的统计显著性")
print("=" * 74)
# ε = 8.12e-17（3 位有效数字）→ δ(−ln ε) = δε/ε ≈ 6.2×10⁻⁴
u_ln = 0.005 / 8.12
u_dH = 5e-5  # d_H = 2.7095 舍入
R = ln_eps / (3 * d_fit)
u_R = R * np.sqrt((u_ln / ln_eps) ** 2 + (u_dH / d_fit) ** 2)
print(f"  −ln(ε)   = {ln_eps:.6f} ± {u_ln:.4f}（ε 的 3 位有效数字主导）")
print(f"  3·d_H    = {3*d_fit:.6f} ± {3*u_dH:.1e}")
print(f"  R        = {R:.6f} ± {u_R:.6f}")
print(f"  √2π      = {s2pi:.6f}")
print(f"  失配     = {R - s2pi:.6f} = {abs(R-s2pi)/s2pi*100:.2f}%")
print(f"  显著性   = {(R - s2pi)/u_R:.0f}σ")
print(f"  ⇒ 失配超出数据精度三个数量级——不是'近似成立'，是确定性失配")

print("\n" + "=" * 74)
print("S2 精确形式可证伪检验：H₁: ε = e^{−3·d_H·√2π}")
print("=" * 74)
for name, d in [("d_H = ln15", d0), ("d_H = d_exact (v1.31)", d_exact), ("d_H = 2.7095 (拟合)", d_fit)]:
    eps_pred = np.exp(-3 * d * s2pi)
    print(f"  H₁({name}): ε_pred = {eps_pred:.3e}  vs ε = 8.12e-17  因子 {eps_pred/eps:.2f}")
print(f"  ⇒ H₁ 预测 ε 偏大 2.5-2.6 倍，而 ε 已知到 0.6%（3 位有效数字）")
print(f"  ⇒ 精确形式被 Paper II 的 ε 值**排除**（因子 2.55 ≫ 1.006）")

print("\n" + "=" * 74)
print("S3 δ 无关性：失配不能被 d_H 修正吸收")
print("=" * 74)
for name, d in [("ln15（零阶）", d0), ("d_exact（含 δ 全修正）", d_exact), ("d_fit（拟合值）", d_fit)]:
    Rv = ln_eps / (3 * d)
    print(f"  R({name:>18s}) = {Rv:.6f}  与 √2π 失配 {abs(Rv-s2pi)/s2pi*100:.2f}%")
spread = (ln_eps/(3*d0) - ln_eps/(3*d_fit)) / (ln_eps/(3*d_fit)) * 100
print(f"  R 在三个 d_H 变体间的变化: {spread:.3f}%")
print(f"  ⇒ δ 的全部物理修正只改变 R 的 0.05%，而失配为 2.6%——")
print(f"    失配不是'等待 δ 精确化的近似'，是稳健失配（v1.4 遗留问题解答）")

print("\n" + "=" * 74)
print("S4 多重比较判别：候选常数族排名 + 偶然接近基线")
print("=" * 74)
# 由 {π, e, √2, √3, √5, φ, 小整数} 经常见运算生成的 [4,5] 区间候选族
phi = (1 + np.sqrt(5)) / 2
cands = {
    "√2·π": np.sqrt(2)*np.pi, "π+√2": np.pi+np.sqrt(2), "9/2": 4.5,
    "2√5": 2*np.sqrt(5), "4π/e": 4*np.pi/np.e, "e·φ": np.e*phi,
    "√2·e": np.sqrt(2)*np.e, "√21": np.sqrt(21), "π·√2.1": np.pi*np.sqrt(2.1),
    "14/π": 14/np.pi, "13/e": 13/np.e, "π+φ": np.pi+phi,
    "e+√3": np.e+np.sqrt(3), "4+1/φ": 4+1/phi, "π·e/2": np.pi*np.e/2,
    "√(8π)": np.sqrt(8*np.pi), "ln(90)": np.log(90), "ln(96)": np.log(96),
    "3φ": 3*phi, "π²/2.2": np.pi**2/2.2, "2π/√2+...": 2*np.pi/np.sqrt(2),
    "e+π/2": np.e+np.pi/2, "41/9": 41/9, "√3·e": np.sqrt(3)*np.e,
    "π·1.45": np.pi*1.45, "23/(2e)": 23/(2*np.e), "5−φ/3": 5-phi/3,
}
rank = sorted(cands.items(), key=lambda kv: abs(kv[1] - R) / kv[1])
print(f"  R = {R:.4f}，候选族（{len(cands)} 个）按失配排名:")
for i, (name, v) in enumerate(rank[:8], 1):
    mark = " <-- 猜想目标" if name == "√2·π" else ""
    print(f"    #{i}  {name:>10s} = {v:.4f}  失配 {abs(v-R)/v*100:5.2f}%{mark}")
pos = [i for i, (n, _) in enumerate(rank, 1) if n == "√2·π"][0]
print(f"  √2·π 在 {len(cands)} 个候选中排名第 {pos}")
print(f"  ⇒ π+√2 以 0.05% 失配居首——比 √2π 好 ~50 倍，")
print(f"    '接近某常数'在多重比较下不携带信息")

# 基线：随机 R' ∈ [4.4, 4.7] 落在任一候选 2.6% 内的概率
rng = np.random.default_rng(1)
trials = 100000
Rs = rng.uniform(4.4, 4.7, trials)
vals = np.array(list(cands.values()))
hit = np.any(np.abs(Rs[:, None] - vals[None, :]) / vals[None, :] < 0.026, axis=1)
print(f"\n  基线实验: 随机 R' ∈ [4.4, 4.7]（10⁵ 次）落在任一候选 2.6% 内的概率")
print(f"    = {hit.mean()*100:.1f}%")
print(f"  ⇒ '2.6% 接近某简单常数'是多重比较下的常态事件，无判别力")

print("\n" + "=" * 74)
print("S6 后续候选检验：失配 2.8% = 2¹×(15−1)×10⁻³ ?（2026-07-29 追加）")
print("=" * 74)
# 针对猜想失配本身提出的结构式: 2^1 × (15-1) × 10^-3 = 2.8%
# 检验它是否给失配赋予结构意义
cand = 2**1 * (15 - 1) * 1e-3 * 100
R0 = ln_eps / (3 * d0)
dev_precise = (R0 - s2pi) / s2pi * 100          # 精确偏差（−ln ε = 37.0496）
dev_rounded = (37.1 / (3 * d0) - s2pi) / s2pi * 100  # 文档 2.8%（−ln ε ≈ 37.1 舍入）
u_dev = (0.005 / 8.12) / (3 * d0) / s2pi * 100
print(f"  精确失配（−ln ε = 37.0496）: {dev_precise:.3f}% ± {u_dev:.3f}%")
print(f"  文档失配（−ln ε ≈ 37.1 舍入）: {dev_rounded:.3f}%")
print(f"  候选 2¹×(15−1)×10⁻³          = {cand:.3f}%")
print(f"  对舍入值的吻合: {abs(cand-dev_rounded)/dev_rounded*100:.2f}% 失配")
print(f"  对精确值的吻合: {abs(cand-dev_precise)/dev_precise*100:.2f}% 失配 = {abs(cand-dev_precise)/u_dev:.0f}σ")
# 同族密度
hits = []
for k1 in [1, 2, 3, 4]:
    for k2 in [0, 1, 2, 3]:
        for k3 in [3, 4]:
            v = k1 * (15 - k2) * 10**(-k3) * 100
            if abs(v - dev_precise) / dev_precise < 0.06:
                hits.append((f"{k1}×(15−{k2})×10⁻³ = {v:.3f}%", abs(v-dev_precise)/dev_precise*100))
print(f"  同族表达式 k₁×(15−k₂)×10⁻ᵏ 中落在精确失配 6% 内的: {len(hits)} 个")
for h, m in hits:
    print(f"    {h}（失配 {m:.1f}%）")
print(f"""  判定: ❌ 候选是**舍入伪影的拟合**——
    ① 0.53% 的吻合只对 −ln ε ≈ 37.1 的舍入值成立;
       对精确失配 2.646% 失配 5.83%（90σ，排除为精确关系）;
    ② 同族表达式过密: 2×(15−2)×10⁻³ = 2.600% 对精确失配的
       吻合（1.8%）反而优于候选（5.8%）——选择 2.800% 无判别依据;
    ③ 父猜想（√2π）本身已被排除（S1-S5），对其失配项再赋结构
       是二阶数值拟合。
  ⇒ 与 v1.35 主结论一致: 该方向无结构关系。""")

print("\n" + "=" * 74)
print("S5 判别结论")
print("=" * 74)
print(f"""
  猜想 −ln(ε)/(3·d_H) ≈ √2π 的判别结果:

  | 判据 | 结果 | 判定 |
  |:-----|:-----|:----:|
  | 1. 统计显著性 | 失配 2.59% = ~1000σ（数据精度内不可调和） | ❌ |
  | 2. 精确形式检验 | ε_pred = 2.07×10⁻¹⁶ vs ε = 8.12×10⁻¹⁷（因子 2.55，ε 精度 0.6%） | ❌ 排除 |
  | 3. δ 无关性 | 失配在 d_H 变体间稳定（ΔR 仅 0.05%）——稳健失配 | ❌ 非近似 |
  | 4. 多重比较 | √2π 在候选族中排名 #{pos}；π+√2 好 50 倍；基线概率 {hit.mean()*100:.0f}% | ❌ 无判别力 |

  ★ 最终判定：猜想**已判别排除**（负结果闭合）。
    −ln(ε) ≈ 37.05 与 3·d_H ≈ 8.13 的比值 ≈ 4.56 不对应任何
    已知结构常数；§6.3 的"可能不是巧合"经检验是多重比较噪声。

  遗留意义（诚实标注）：
    −ln(ε) = 37.05 本身的结构分解（为何谱交织精度恰好是这个数）
    仍是开放问题，但答案不在"3·d_H × 简单常数"的形式中——
    该方向已排除，避免未来重复探索。
""")
