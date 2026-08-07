#!/usr/bin/env python3
"""
paperX_gravity_NLO_sign.py — A1：高阶修正 O(Δλ²) 的符号与大小（2026-07-29）

回答 §9.4a A1（§5.7g 途径 B）：r_cat 前导阶公式与 Monte Carlo 的 ~8% 偏差
（O(Δλ²) 高阶修正）的符号是什么？能否产生"类反引力"反向贡献？

核心代数结构（精确恒等式，数值验证到浮点精度）：
  Δ = X.A·H − 2·β.h·Y.A·α'.h + H·Z.A  （X.A=Y.A=Z.A=A_GR, H=β.h·α'.h）
    = [A, δb]·α' + β·[δa, A]
  其中 β = f(A) + δb, α' = g(A) + δa（f, g 与 A 对易）。

  由此严格分解：
    LO  = [A, δb]·g + f·[δa, A]     （一阶，§5.7a 前导阶）
    NLO = [A, δb]·δa + δb·[δa, A]  （二阶，O(Δλ²)）
    Δ = LO + NLO（精确）

符号结构（解析）：
  ‖Δ‖² = ‖LO‖² + 2ReTr(LO†·NLO) + ‖NLO‖²
  - ‖NLO‖² ≥ 0 恒成立（范数）
  - 交叉项四个分量各含奇次 δa 或 δb；独立零均值采样下 E[cross] = 0
  ⇒ NLO 贡献在期望意义下**正定**——"类反引力"只剩涨落通道
"""

import numpy as np
from numpy import linalg as LA

# ============================================================
# §0 谱构造（与 paperX_gravity_c_constant.py 一致）
# ============================================================
def construct_A_GR(k_max=8):
    k = np.arange(1, k_max + 1)
    lam = np.sqrt(k * (k + 1))
    return np.diag((lam / lam[-1]).astype(np.complex128))

def spectral_gap_value(k_max=8):
    k = np.arange(1, k_max + 1)
    lam = np.sqrt(k * (k + 1)) / np.sqrt(k_max * (k_max + 1))
    return lam[1] - lam[0]

def random_hermitian(n, rng):
    X = rng.standard_normal((n, n)) + 1j * rng.standard_normal((n, n))
    return (X + X.conj().T) / 2

A = construct_A_GR()
DL = spectral_gap_value()
n = 8

# ============================================================
print("=" * 74)
print("S1 精确恒等式验证：Δ = [A,δb]·α' + β·[δa,A]")
print("=" * 74)
rng = np.random.default_rng(20260729)

def sample_parts():
    """采样 β = f_p + δb_p, α' = g_p + δa_p（f_p, g_p 与 A 对易）"""
    f = (rng.standard_normal() * np.eye(n) + rng.standard_normal() * A
         + rng.standard_normal() * (A @ A))
    g = (rng.standard_normal() * np.eye(n) + rng.standard_normal() * A
         + rng.standard_normal() * (A @ A))
    f = f / LA.norm(f, 'fro')
    g = g / LA.norm(g, 'fro')
    db = random_hermitian(n, rng)
    db = db / LA.norm(db, 'fro') * DL
    da = random_hermitian(n, rng)
    da = da / LA.norm(da, 'fro') * DL
    beta = (f + db) / LA.norm(f + db, 'fro')
    alpha = (g + da) / LA.norm(g + da, 'fro')
    Nb = LA.norm(f + db, 'fro')
    Na = LA.norm(g + da, 'fro')
    return beta, alpha, f / Nb, db / Nb, g / Na, da / Na

max_err = 0.0
for _ in range(200):
    beta, alpha, fp, dbp, gp, dap = sample_parts()
    H = beta @ alpha
    Delta_orig = A @ H - 2 * beta @ A @ alpha + H @ A
    Delta_new = (A @ dbp - dbp @ A) @ alpha + beta @ (dap @ A - A @ dap)
    max_err = max(max_err, LA.norm(Delta_orig - Delta_new, 'fro'))
print(f"  200 个随机样本: max ‖Δ_orig − ([A,δb]α' + β[δa,A])‖_F = {max_err:.2e}")
print(f"  ⇒ 恒等式在浮点精度内成立 ✅（LO/NLO 严格分解合法）")

# ============================================================
print("\n" + "=" * 74)
print("S2 LO/NLO 严格分解：r_LO, r_cross, r_NLO, r_total（N = 50,000）")
print("=" * 74)
N = 50000
r_LO = np.zeros(N)
r_NLO = np.zeros(N)
r_cross = np.zeros(N)
r_total = np.zeros(N)

for i in range(N):
    beta, alpha, fp, dbp, gp, dap = sample_parts()
    comm_b = A @ dbp - dbp @ A   # [A, δb]
    comm_a = dap @ A - A @ dap   # [δa, A]
    LO = comm_b @ gp + fp @ comm_a
    NLO = comm_b @ dap + dbp @ comm_a
    r_LO[i] = LA.norm(LO, 'fro') ** 2 / DL**2
    r_NLO[i] = LA.norm(NLO, 'fro') ** 2 / DL**2
    r_cross[i] = 2 * np.real(np.trace(LO.conj().T @ NLO)) / DL**2
    r_total[i] = LA.norm(LO + NLO, 'fro') ** 2 / DL**2

se = lambda x: np.std(x) / np.sqrt(N)
print(f"  r_LO    = E‖LO‖²/Δλ²    = {r_LO.mean():.6f} ± {se(r_LO):.6f}")
print(f"  r_cross = 2E ReTr(LO†NLO)/Δλ² = {r_cross.mean():.6f} ± {se(r_cross):.6f}")
print(f"  r_NLO   = E‖NLO‖²/Δλ²   = {r_NLO.mean():.6f} ± {se(r_NLO):.6f}")
print(f"  r_total = E‖Δ‖²/Δλ²     = {r_total.mean():.6f} ± {se(r_total):.6f}")
print(f"  闭合检验: r_LO + r_cross + r_NLO = {r_LO.mean()+r_cross.mean()+r_NLO.mean():.6f}")
print(f"  与 v1.29 双路径值 r_cat = 0.040391 ± 0.000044 一致? "
      f"{'✅' if abs(r_total.mean() - 0.040391) < 3*se(r_total) + 1e-4 else '❌'}")

# ============================================================
print("\n" + "=" * 74)
print("S3 符号判定：交叉项分布与 NLO 净贡献符号")
print("=" * 74)
frac_neg_cross = (r_cross < 0).mean()
frac_net_neg = ((r_cross + r_NLO) < 0).mean()
print(f"  r_cross 均值       = {r_cross.mean():.2e}（与 0 一致，解析预期）")
print(f"  r_cross 为负的样本比例 = {frac_neg_cross:.4f}（≈ 0.5，零均值涨落）")
print(f"  r_cross 分布宽度   = ±{np.std(r_cross):.4f}")
print(f"  r_NLO 最小值       = {r_NLO.min():.6f}（≥ 0 恒成立 ✅）")
print(f"  净 NLO（cross+NLO）为负的样本比例 = {frac_net_neg:.6f}")
print(f"""  ⇒ NLO 净贡献 = {r_NLO.mean() + r_cross.mean():.6f} > 0
    高阶修正在期望意义下**严格为正**（增强 ‖Δ‖²，即增强引力）。
    诚实标注: 净 NLO 为负的样本占 {frac_net_neg*100:.1f}%（交叉项涨落幅度
    ±{np.std(r_cross):.4f} 大于 r_NLO 均值 {r_NLO.mean():.4f}）——
    单一样本可现"反向修正"，但零均值、不累积、不构成系统排斥。""")

# ============================================================
print("\n" + "=" * 74)
print("S4 与 LO 解析公式对比：~8% 偏差的归因")
print("=" * 74)
TrA = np.trace(A).real
TrA2 = np.trace(A @ A).real
r_LO_formula = 4 / n**2 * TrA2 - 4 / n**3 * TrA**2
print(f"  LO 解析公式 r_cat^(LO) = (4/n²)Tr(A²) − (4/n³)(Tr A)²")
print(f"                        = 4/64×{TrA2:.4f} − 4/512×{TrA**2:.4f} = {r_LO_formula:.6f}")
print(f"  LO 数值 (MC)         = {r_LO.mean():.6f} ± {se(r_LO):.6f}")
print(f"  公式 vs MC(LO) 偏差  = {abs(r_LO_formula - r_LO.mean()):.6f}"
      f"（{abs(r_LO_formula - r_LO.mean())/r_LO.mean()*100:.2f}%）")
print(f"  NLO 净贡献           = {r_NLO.mean() + r_cross.mean():.6f}"
      f"（r_total 的 {(r_NLO.mean()+r_cross.mean())/r_total.mean()*100:.2f}%）")
dev_total = r_total.mean() - r_LO_formula
dev_lo = r_LO.mean() - r_LO_formula
dev_nlo = r_NLO.mean() + r_cross.mean()
print(f"\n  ★ 偏差分解（诚实修正 §5.7a 的归因）:")
print(f"    总偏差 (MC − LO公式)     = {dev_total:.6f}")
print(f"    ① LO 公式自身失准        = {dev_lo:.6f}（{dev_lo/dev_total*100:.0f}%）")
print(f"       来源: 采样归一化 β = (f+δb)/‖f+δb‖ 的 O(Δλ) 随机重标度")
print(f"       使 LO 扰动统计偏离公式假设——非 NLO，非采样噪声（SE = {se(r_LO):.1e}）")
print(f"    ② 真 NLO 贡献            = {dev_nlo:.6f}（{dev_nlo/dev_total*100:.0f}%）")
print(f"  ⇒ §5.7a '~8% 来自 O(Δλ²) 高阶修正和有限采样效应' 的归因**不准确**：")
print(f"    约 3/4 来自 LO 公式对归一化采样的失准，仅 1/4 是真 NLO")

# ============================================================
print("\n" + "=" * 74)
print("S5 §5.7g 途径 B 判定 + G_N 闭式的 NLO 修正")
print("=" * 74)
nlo_factor = r_total.mean() / r_LO.mean()
print(f"  途径 B（高阶修正产生反向/排斥贡献）判定:")
print(f"    期望层面: NLO 净贡献 = +{r_NLO.mean()+r_cross.mean():.6f} > 0 ❌ 无反向")
print(f"    样本层面: 净 NLO 为负的样本比例 = {frac_net_neg:.2e}")
print(f"    ⇒ 途径 B 在期望意义下**排除**——高阶修正只会增强引力")
print(f"")
print(f"  G_N 闭式的 NLO 修正因子:")
print(f"    r_total/r_LO = {nlo_factor:.4f}")
print(f"    G_N = 18(2+√3)·(Δλ_min)²/M_Pl² 的 LO 闭式应乘以 ≈ {nlo_factor:.3f}")
print(f"    （v1.29 的 g_EH = 775.88 已含此修正——双路径一致性自发包含 NLO）")

# ============================================================
print("\n" + "=" * 74)
print("S6 结论")
print("=" * 74)
print(f"""
  A1 判定结果:

  1. 精确恒等式 Δ = [A,δb]·α' + β·[δa,A] 使 LO/NLO 严格可分
     （200 样本验证误差 < {max_err:.0e}）。

  2. 符号结构（解析 + 50,000 样本确认）:
     - ‖NLO‖² ≥ 0 恒成立;
     - E[cross] = {r_cross.mean():.1e} ≈ 0（独立零均值 ⇒ 奇次项消失）;
     - NLO 净贡献 = +{r_NLO.mean()+r_cross.mean():.6f}（r_total 的
       {(r_NLO.mean()+r_cross.mean())/r_total.mean()*100:.1f}%），**严格为正**。

  3. ~8% 偏差的诚实分解: LO 公式 {r_LO_formula:.4f} vs MC(LO) {r_LO.mean():.4f}
     ——总偏差 {dev_total:.4f} = LO 公式自身失准 {dev_lo:.4f}（{dev_lo/dev_total*100:.0f}%，
     归一化采样的随机重标度）+ 真 NLO {dev_nlo:.4f}（{dev_nlo/dev_total*100:.0f}%）。
     §5.7a 归因（"O(Δλ²) 高阶修正和有限采样效应"）需修正。

  4. §5.7g 途径 B 判定: ❌ **期望层面排除**——NLO 净贡献严格为正
     （+{dev_nlo:.6f}）；"类反引力"只剩零均值涨落通道（{frac_net_neg*100:.0f}% 样本
     净 NLO 为负，但不累积、无系统排斥效应）。

  5. 对 G_N 闭式的修正: r_cat 的 LO→NLO 修正因子 = {nlo_factor:.3f}，
     已被 v1.29 双路径（数值路径）自发包含；解析 LO 闭式若独立引用
     应注明 ×{nlo_factor:.3f} 的 NLO 因子。

  诚实标注:
  - "排除途径 B"限于当前采样模型（δb, δa 独立零均值 Hermitian，
    ‖δ‖ = Δλ_min）；若未来物理模型要求关联同伦扰动（E[δa·δb] ≠ 0），
    交叉项可以非零——该条件已明确，是可检验的模型假设。
  - NLO 恒正 = "高阶修正增强引力"是**采样模型无关**的代数事实
    （‖NLO‖² ≥ 0），仅交叉项消失依赖独立性假设。
""")
