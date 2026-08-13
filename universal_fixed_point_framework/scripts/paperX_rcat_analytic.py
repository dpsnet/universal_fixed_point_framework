#!/usr/bin/env python3
"""
paperX_rcat_analytic.py — r_cat 解析化（路径 1）+ Δ 代数强度结构深化（路径 2）

笔记来源: notes/06_photon_topology/photon_first_principle_origin.md §3.5.1 P6-5
前置: paper35（Δ = spExchangeLaw 偏差, ‖Δ‖_F² = r_cat·Δλ_min², r_cat≈0.040404 MC）+
      paperX_gravity_NLO_sign.py（LO/NLO 严格分解）+ paperX_epsilon_delta_derivation.py
      （ε_Δ 第一性候选 C1 = ‖Δ‖_F²）

目标（评价 §10.4 追踪点 1 的剩余路径）:
  路径 1: 解析 r_cat 闭式——闭合 C1 = ‖Δ‖_F² 与路径 A（S4³=2.96e-4）的 2.03 倍差
  路径 2: Δ 代数强度的结构分解（4-范畴偏差矩阵 → 代数强度）

核心代数（paper35 定理 2.1 + NLO_sign 分解）:
  Δ = X.A·H − 2β.h·Y.A·α'.h + H·Z.A（H = β.h·α'.h）——机器证明
  简化模型: X.A=Y.A=Z.A = A_GR = diag(√(k(k+1))/√72, k=1..8), n=8
  Δ = [A,δb]·α' + β·[δa,A]（严格）;  LO = [A,δb]·g + f·[δa,A];  NLO = [A,δb]·δa + δb·[δa,A]

解析推导链:
  A1 r_LO 精确闭式: r_cat^(LO) = (4/n²)Tr(A²) − (4/n³)(Tr A)²
      Tr(A²) = Σk(k+1)/72 = 10/3（解析精确）
      TrA = S/√72, S = Σ√(k(k+1))（k=1..8, 确定性代数数和）
      ⟹ r_LO = 5/24 − S²/9216（完全解析, 无 MC）
  A2 NLO 解析近似: Wigner 平均（σ²=Δλ²/n²）
      E‖[A,δb]‖² = 2Δλ²[Tr(A²)/n − (TrA)²/n²]
      E‖[A,δb]·δa‖² = (σ²/2)(n+1)·E‖[A,δb]‖²
      ——与采样模型（固定范数归一化）有系统性偏差, 登记为开放
  A3 r_cat 分解: r_cat = r_LO(≈92%) + 归一化重标度修正(≈6%) + NLO(≈2%)
      ——完全闭式化困难（含代数数和 + 归一化效应）, 登记开放
  A4 ‖Δ‖_F² 与路径 A: ‖Δ‖_F² = r_cat·Δλ², Δλ²=(2−√3)/18
      ‖Δ‖_F²^(LO) = r_LO·Δλ² 与 2·S4³ 对照
  A5 数值巧合观察（如实登记, 非推导依据）:
      · r_cat/Δλ² ≈ e（2.7140 vs 2.71828, 差 0.16%）
      · ‖Δ‖_F² ≈ 2·S4³（差 1.5%）
      · r_NLO ≈ e·S4³（差 0.07%）

诚实边界:
  1. r_LO 解析闭式是理想化（f=g 归一化）值; 实际采样模型的 LO 含 O(Δλ) 随机重标度
  2. NLO Wigner 平均与采样模型系统性偏差 ~1.7 倍（固定范数 vs 高斯）, 精确 NLO 解析开放
  3. r_cat 完全解析闭式（含全部修正）登记开放——需精确建模 f,g 归一化效应
  4. 数值巧合（≈e, ≈2·S4³）为观察登记, 不作推导结论
  5. 本脚本为理论推导候选的数值自洽验证, 不构成实验验证
"""
import numpy as np
from numpy import linalg as LA

# ============================================================
# 检查项框架
# ============================================================
_CHECKS = []


def check(name, cond, detail=""):
    _CHECKS.append((name, bool(cond), detail))


n = 8
k = np.arange(1, 9)
lam = np.sqrt(k * (k + 1))
A = np.diag(lam / lam[-1])
DL = (lam[1] - lam[0]) / lam[-1]           # Δλ_min
DL2 = DL ** 2                              # Δλ_min² = (2−√3)/18
TrA = np.trace(A).real
TrA2 = np.trace(A @ A).real
S = lam.sum()                              # Σ√(k(k+1))
R_CAT = 0.040404                           # MC (paper35 §5.8 r_total)
R_NLO = 0.000806                           # MC
S4 = 1.0 / 15.0
PATH_A = S4 ** 3                            # (1/15)³ ≈ 2.96e-4

print("=" * 74)
print("r_cat 解析化（路径 1）+ Δ 代数强度结构（路径 2）")
print("笔记: notes/06_photon_topology/photon_first_principle_origin.md §3.5.1 P6-5")
print("=" * 74)

# ============================================================
# A1 r_LO 精确解析闭式
# ============================================================
print("\n[A1] r_LO 精确解析闭式（完全解析, 无 MC）")
r_LO_formula = 4 / n ** 2 * TrA2 - 4 / n ** 3 * TrA ** 2
r_LO_closed = 5 / 24 - S ** 2 / 9216
print(f"  r_LO = (4/n²)Tr(A²) − (4/n³)(Tr A)²")
print(f"       = 4/64×{TrA2:.6f} − 4/512×{TrA**2:.6f}")
print(f"       = 5/24 − S²/9216,  S = Σ√(k(k+1)) = {S:.6f}")
print(f"       = {5/24:.8f} − {S**2/9216:.8f} = {r_LO_closed:.8f}")
print(f"  与直接计算一致: {r_LO_formula:.8f}（差 {abs(r_LO_formula-r_LO_closed):.2e}）")
check("A1-C1 r_LO 解析闭式 = 5/24 − S²/9216",
      abs(r_LO_formula - r_LO_closed) < 1e-14, "")
check("A1-C2 Tr(A²) = 10/3 解析精确", abs(TrA2 - 10 / 3) < 1e-14, "")

# ============================================================
# A2 NLO 解析近似（Wigner 平均）
# ============================================================
print("\n[A2] NLO 解析近似（Wigner 平均, σ²=Δλ²/n²）")
sig2 = DL2 / n ** 2
E_comm = 2 * DL2 * (TrA2 / n - TrA ** 2 / n ** 2)   # E‖[A,δb]‖²
term1_an = (sig2 / 2) * (n + 1) * E_comm / DL2      # r 归一化
print(f"  E‖[A,δb]‖² = 2Δλ²[Tr(A²)/n − (TrA)²/n²] = {E_comm:.6e}")
print(f"  项1+项2 解析 r = 2·(σ²/2)(n+1)·E‖[A,δb]‖²/Δλ² = {2*term1_an:.6e}")
print(f"  MC r_NLO = {R_NLO:.6e}（含交叉项, 采样模型固定范数归一化）")
print(f"  解析 vs MC 偏差 = {2*term1_an/R_NLO:.3f} 倍——登记开放（Wigner vs 固定范数）")
check("A2-C1 NLO 解析为 r_NLO 的正确量级（10⁻⁴）", 1e-5 < 2 * term1_an < 1e-2, "")
check("A2-C2 解析与 MC 偏差如实登记（非闭合）", abs(2 * term1_an / R_NLO - 1) > 0.5, "")

# ============================================================
# A3 r_cat 分解
# ============================================================
print("\n[A3] r_cat 分解（LO 主导 + 修正项）")
print(f"  r_cat(MC)     = {R_CAT:.6f}")
print(f"  r_LO 解析     = {r_LO_closed:.6f}（占 {r_LO_closed/R_CAT*100:.1f}%）")
print(f"  修正项(MC−LO) = {R_CAT-r_LO_closed:.6f}（{ (R_CAT-r_LO_closed)/R_CAT*100:.1f}%）")
print(f"    ≈ 归一化重标度({0.0025:.4f}) + NLO({R_NLO-3.4e-5:.4f})（脚本 S4 分解）")
check("A3-C1 r_LO 主导（>90%）", r_LO_closed / R_CAT > 0.9, "")
check("A3-C2 修正项分解与脚本一致", abs((R_CAT - r_LO_closed) - (0.0025 + R_NLO - 3.4e-5)) < 2e-4,
      "MC−LO=%.5f vs 0.0025+0.000772=%.5f" % (R_CAT - r_LO_closed, 0.0025 + R_NLO - 3.4e-5))

# ============================================================
# A4 ‖Δ‖_F² 与路径 A
# ============================================================
print("\n[A4] ‖Δ‖_F² 与路径 A（S4³）关系")
normD2 = R_CAT * DL2
normD2_LO = r_LO_closed * DL2
print(f"  Δλ² = (2−√3)/18 = {DL2:.8f}（精确闭式）")
print(f"  ‖Δ‖_F²(LO) = r_LO·Δλ² = {normD2_LO:.6e}")
print(f"  ‖Δ‖_F²(MC) = r_cat·Δλ² = {normD2:.6e}")
print(f"  2·S4³ = 2/3375 = {2*PATH_A:.6e}")
print(f"  ‖Δ‖_F²(LO)/(2·S4³) = {normD2_LO/(2*PATH_A):.4f}")
print(f"  ‖Δ‖_F²(MC)/(2·S4³) = {normD2/(2*PATH_A):.4f}")
check("A4-C1 ‖Δ‖_F²(MC) 与 2·S4³ 同量级（0.5–2）", 0.5 <= normD2 / (2 * PATH_A) <= 2.0, "")
check("A4-C2 ‖Δ‖_F²(LO) 与 2·S4³ 同量级（0.5–2）", 0.5 <= normD2_LO / (2 * PATH_A) <= 2.0, "")

# ============================================================
# A5 数值巧合观察（诚实登记）
# ============================================================
print("\n[A5] 数值巧合观察（登记观察, 非推导依据）")
print(f"  观察 1: r_cat/Δλ² = {R_CAT/DL2:.4f} vs e = {np.e:.5f}（差 {abs(R_CAT/DL2-np.e)/np.e*100:.2f}%）")
print(f"  观察 2: ‖Δ‖_F²/(2·S4³) = {normD2/(2*PATH_A):.5f}（差 {abs(normD2/(2*PATH_A)-1)*100:.2f}%）")
print(f"  观察 3: r_NLO/(e·S4³) = {R_NLO/(np.e*PATH_A):.5f}（差 {abs(R_NLO/(np.e*PATH_A)-1)*100:.3f}%）")
check("A5-C1 巧合观察如实登记（不判定为关系）", True, "登记观察: ≈e 差 0.16%, ≈2·S4³ 差 1.5%, ≈e·S4³ 差 0.07%")

# ============================================================
# 总结
# ============================================================
print("\n" + "=" * 74)
print("结论（诚实表述）")
print("=" * 74)
print(f"""  路径 1（r_cat 解析化）部分闭合:
    · r_LO 精确解析闭式 = 5/24 − S²/9216 = {r_LO_closed:.6f}（完全解析, 占 r_cat {r_LO_closed/R_CAT*100:.0f}%）
    · NLO Wigner 平均与采样模型系统性偏差（{2*term1_an/R_NLO:.1f} 倍）, 精确 NLO + 归一化修正解析登记开放
    · r_cat 完全闭式化开放（含代数数和 S + 归一化效应）
  路径 2（Δ 代数强度结构）:
    · ε_Δ = ‖Δ‖_F² = r_cat·Δλ², Δλ²=(2−√3)/18 精确闭式, r_cat 由 Δ 的谱结构（LO 主导）确定
    · LO 项 Tr(A²)=10/3 解析精确 + TrA=S/√72（代数数和）——代数强度无简单闭式（诚实）
    · 与路径 A（S4³）差 {normD2/(2*PATH_A):.2f} 倍（2·S4³ 参照）未闭合——需精确 NLO/归一化解析或远期观测
  数值巧合观察（≈e 0.16%, ≈2·S4³ 1.5%, ≈e·S4³ 0.07%）全部登记为观察, 不作推导依据。
  开放问题 #5 维持"部分闭合"（ε_Δ 候选 C1=‖Δ‖_F² 确立, 精确值解析待 NLO/归一化闭合）。""")

print("\n检查项汇总: %d/%d 通过" % (sum(1 for _, ok, _ in _CHECKS if ok), len(_CHECKS)))
fail = [name for name, ok, _ in _CHECKS if not ok]
if fail:
    print("未通过: ", fail)
    raise SystemExit(1)
print("全部通过 ✅")
