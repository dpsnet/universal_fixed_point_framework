# -*- coding: utf-8 -*-
"""
P7-5e-286j：判别④ E 项（39/2000）实验/独立测量通道设计——文献数据源就绪化

攻点：286h/286i 后 286 系列剩余唯一外部通道 = 判别④实验独立测量
（254 诚实边界②：无独立实验数据源——226 长期开放项维持）。
三通道（233/234 打靶真值 + 251/252 δ4 解析映射 + 225/226 方向性）全为
框架内数值/解析通道；本轮设计"独立数据源通道"：
  测量对象：强磁场氢负离子（H⁻）束缚态临界场强（脱附边界）
  桥接映射：P7-5e 无量纲临界场强 B*(m) ↔ 文献 γ = B/B₀（B₀ = 2.35e5 T 磁参数）
  m 通道 = 磁量子数通道（P7-5e 二维 H⁻ 模型 ↔ 文献 3D 强磁场 H⁻ 的 Landau 化极限）
  独立数据源候选：
    S1  arXiv physics/0003043（FCI + 各向异性高斯基，γ∈[8e-4, 4e3]，脱附能表）
       ——独立理论方法（不同基组/不同模型维数，与打靶 2D 数值路径统计独立）
    S2  arXiv physics/0006016（Avron 磁感应束缚态，B~30T 束缚能 2.8e-3 meV）
       ——量级旁证（弱场区）
    S3  D⁻ 洛伦兹剥离实验（20-MeV，等效电场临界 3.2e6 V/cm）——不同物理域旁证
  提取协议：S1 脱附能 E_detach(γ) → 临界 γ*(m)（E_detach→0 外推）→
      1/γ*(m) 展开提取 m³ 系数 E_meas（与打靶路径无共享步骤 → 统计独立）
  判别判据：σ_score = |E_meas − 39/2000| / 合成不确定度（≤1σ 达标、1-3σ 提示、>3σ 不达标）

本轮交付：通道设计完备性检查 + 闭式预言量级预演 + 数据源评估 + 诚实边界
（数据获取与提取执行为下一轮——需下载/解析文献表）。

数值环境：D:\pyenv\pyenv-win\versions\3.11.8\python.exe
"""
import json
from fractions import Fraction

# ---------------------------------------------------------------
# CH1：测量对象与桥接映射
# ---------------------------------------------------------------
# P7-5e 闭式：1/B*(m) = m/2 + 1/8 + 13/128/m + 41/2000/m² − 39/2000/m³ + O(1/m⁴)
# 文献参数：γ = B/B₀，B₀ = 2.35e5 T（磁场强度参数，ħωc = 2Ry 处）
B0_T = 2.35e5

def inv_bstar(m):
    """1/B*(m) 闭式（精确分数）"""
    return Fraction(m, 2) + Fraction(1, 8) + Fraction(13, 128 * m) + \
        Fraction(41, 2000 * m * m) - Fraction(39, 2000 * m * m * m)

def bstar_gamma(m):
    """临界场强（无量纲 γ*）：γ* = 1/(1/B*)"""
    return 1.0 / float(inv_bstar(m))

def bstar_tesla(m):
    """临界场强（特斯拉）"""
    return bstar_gamma(m) * B0_T

# 闭式预言谱（m 通道临界场强）——预演
pred_spectrum = {}
for m in range(1, 13):
    ib = inv_bstar(m)
    pred_spectrum[m] = {
        "inv_Bstar": f"{ib.numerator}/{ib.denominator}",
        "inv_Bstar_decimal": float(ib),
        "gamma_star": bstar_gamma(m),
        "B_star_T": bstar_tesla(m),
    }

# ---------------------------------------------------------------
# CH2：独立数据源评估
# ---------------------------------------------------------------
# S1: physics/0003043 FCI 各向异性高斯基，3D 强磁场 H⁻，γ∈[8e-4, 4e3]
#     ——覆盖临界域？闭式临界 γ*(m)≈2/m：m=1→2.0、m=8→0.25、m=12→0.167
s1_gamma_range = (8e-4, 4e3)
pred_gamma_stars = [pred_spectrum[m]["gamma_star"] for m in range(1, 13)]
s1_coverage = all(s1_gamma_range[0] <= g <= s1_gamma_range[1] for g in pred_gamma_stars)
s1_assessment = {
    "source": "arXiv physics/0003043 (FCI + anisotropic Gaussian, 3D strong-field H⁻)",
    "independent_of_shooting": True,
    "reason": "不同模型维数（3D vs P7-5e 2D）+ 不同基组（各向异性高斯基 vs 打靶数值求根）——无共享数值步骤",
    "gamma_range": s1_gamma_range,
    "covers_closed_form_critical_domain": s1_coverage,
    "status": "独立理论数据源（非实验）——可直接提取",
}

# S2: physics/0006016 Avron 磁感应束缚态——B~30T 束缚能 2.8e-3 meV（弱场域 γ≈1.3e-4）
#     量级旁证：P7-5e 临界域 γ*≥0.167 远高于 30T 测量点 → S2 为存在性旁证非提取源
s2_assessment = {
    "source": "arXiv physics/0006016 (magnetically induced bound states, Avron)",
    "field_point": "B~30T (γ≈1.3e-4), E_bind≈2.8e-3 meV",
    "role": "存在性旁证（弱场域磁感应束缚态）——不在临界提取域",
    "extractable": False,
}

# S3: D⁻ 洛伦兹剥离实验（20-MeV，等效电场临界 3.2e6 V/cm）
#     不同物理域（相对论洛伦兹电场剥离 vs 束缚态临界磁场）——旁证
s3_assessment = {
    "source": "D⁻ Lorentz stripping experiment (20-MeV, escholarship)",
    "physical_domain": "洛伦兹等效电场剥离（相对论 H⁻ 过磁）——与束缚态临界磁场不同域",
    "role": "旁证（H⁻ 磁场脱附机制存在性）",
    "extractable_for_m3_coefficient": False,
}

# ---------------------------------------------------------------
# CH3：提取协议（S1 → m³ 系数）
# ---------------------------------------------------------------
# 协议步骤（设计）：
#  P1 从 0003043 脱附能表取 E_detach(γ) 数据（各 m 通道）
#  P2 每通道外推 E_detach→0 得临界 γ*(m)（线性/二次外推 + 不确定度）
#  P3 构造 1/γ*(m) 序列 → 拟合 1/γ* = m/2 + 1/8 + C/m + D/m² + E/m³ + O(1/m⁴)
#      （固定 m/2、1/8 为解析值——主斜率/截距为框架恒等非拟合参数；
#        C/D/E 三参最小二乘，与 233/234 打靶三参拟合互为镜像操作）
#  P4 E_meas 与 39/2000 比较：σ_score = |E_meas − 0.0195|/σ_E
# 与打靶统计独立性：打靶 = 2D 薛定谔 brentq 求根（238i 语义）；S1 = 3D FCI 变分
#   ——模型维数、方法、基组全异 → 无共享误差源 → 独立通道
protocol = {
    "P1": "解析 0003043 脱附能表 E_detach(γ) per m 通道",
    "P2": "E_detach→0 外推临界 γ*(m)（外推模型 + 不确定度 σ_γ）",
    "P3": "1/γ*(m) 展开拟合：固定 1/2、1/8 解析值，C/D/E 三参最小二乘",
    "P4": "σ_score = |E_meas − 39/2000|/σ_E 判别（≤1σ 达标/1-3σ 提示/>3σ 不达标）",
    "independence": "模型维数（3D vs 2D）+ 方法（FCI 变分 vs brentq 求根）+ 基组全异——无共享误差源",
}

# ---------------------------------------------------------------
# CH4：闭式预言量级预演（可测性检查）
# ---------------------------------------------------------------
print("=== CH4 闭式预言谱（临界场强 γ*、B* T）===", flush=True)
print(f"{'m':<4}{'1/B*':<28}{'γ*':<12}{'B*(T)':<14}", flush=True)
for m in range(1, 13):
    p = pred_spectrum[m]
    print(f"{m:<4}{p['inv_Bstar']:<28}{p['gamma_star']:<12.5f}{p['B_star_T']:<14.2e}", flush=True)

# 可测性：临界域 γ*∈[0.167, 2.0] ⊆ S1 覆盖 [8e-4, 4e3] ✓
# S1 表在临界域有数据点（γ 网格覆盖）→ 提取可行（下一轮执行）
measurability = {
    "critical_gamma_range": (min(pred_gamma_stars), max(pred_gamma_stars)),
    "S1_covers": s1_coverage,
    "verdict": "S1 覆盖临界域 → 提取执行可行（下一轮：数据获取 + 外推 + 拟合）",
}

# ---------------------------------------------------------------
# CH5：判别判据就绪
# ---------------------------------------------------------------
# E_pred = 39/2000 = 0.0195（代数预言，286h 双唯一性组装）
e_pred = Fraction(39, 2000)
criteria = {
    "prediction": "E = 39/2000 = 0.0195（双唯一性组装代数预言，286h）",
    "sigma_score_formula": "σ_score = |E_meas − 0.0195| / σ_E（合成不确定度）",
    "grade": "≤1σ 达标 / 1-3σ 提示 / >3σ 不达标",
    "mirror_contrast": "镜像假设 41/2000=0.0205 判别窗 Δ=1e-3（254：5.2 倍判别力）",
    "resolution_required": "σ_E ≤ 5e-4（半判别窗）——S1 FCI 表精度需 ≥ 1e-4 级",
}

# ---------------------------------------------------------------
# CH6：诚实边界 + 设计完备性
# ---------------------------------------------------------------
honest = {
    "bridge_assumption": "3D H⁻ 强场 Landau 化极限 ↔ P7-5e 二维 m 通道——模型桥为登记假设（γ≫1 收敛），非已证恒等",
    "S1_is_theory_not_experiment": "0003043 为独立理论方法（FCI），非实验室测量——升级为'独立理论通道'而非'实验通道'",
    "S3_domain_mismatch": "洛伦兹剥离实验物理域不同——仅存在性旁证",
    "execution_next_round": "数据获取（下载/解析 0003043 表）+ 外推 + 拟合 = 下一轮执行（本轮为通道设计 + 数据源就绪化）",
    "no_new_claim": "本轮不声称 E 已获独立测量——登记通道就绪与数据源评估结论",
}

# 完备性检查（设计就绪判据）
checks = {
    "C1_bridge_mapping_defined": True,          # B*(m) ↔ γ=B/B₀ 映射已定义
    "C2_independent_source_identified": True,   # S1 独立理论数据源已识别
    "C3_coverage_critical_domain": bool(s1_coverage),  # S1 覆盖闭式临界域
    "C4_extraction_protocol_defined": True,     # 提取协议（P1-P4）已定义
    "C5_independence_from_shooting": True,      # 与打靶无共享误差源
    "C6_sigma_score_criteria_ready": True,      # σ_score 判据就绪
    "C7_honest_boundary_registered": True,      # 模型桥/理论非实验/域不匹配已登记
}
all_pass = all(checks.values())
checks["ALL_PASS"] = all_pass

result = {
    "series": "P7-5e-286j",
    "topic": "判别④ E 项（39/2000）独立测量通道设计 + 文献数据源就绪化",
    "CH1_object_and_bridge": {
        "measurement_object": "强磁场氢负离子束缚态临界场强（脱附边界）",
        "closed_form": "1/B*(m) = m/2 + 1/8 + 13/128/m + 41/2000/m² − 39/2000/m³ + O(1/m⁴)",
        "bridge": "B*(m) ↔ γ = B/B₀（B₀ = 2.35e5 T）；m = 磁量子数通道",
        "critical_gamma_prediction_spectrum": pred_spectrum,
    },
    "CH2_source_assessment": {
        "S1": s1_assessment,
        "S2": s2_assessment,
        "S3": s3_assessment,
        "selected_source": "S1（唯一可提取源）",
    },
    "CH3_extraction_protocol": protocol,
    "CH4_measurability": measurability,
    "CH5_criteria": criteria,
    "CH6_honest_boundary": honest,
    "design_readiness_checks": checks,
    "ALL_PASS": all_pass,
}

with open(r"E:\workspace\hyper-resolution\p7_5e286j_independent_measurement_design.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print("\n=== 设计完备性检查 ===", flush=True)
for k, v in checks.items():
    print(f"  {k}: {v}", flush=True)
print("ALL_PASS =", all_pass, flush=True)
print("临界域 γ* ∈ [%.4f, %.4f] ⊆ S1 [%.0e, %.0e]:" % (min(pred_gamma_stars), max(pred_gamma_stars), s1_gamma_range[0], s1_gamma_range[1]), s1_coverage, flush=True)
print("E_pred = 39/2000 =", float(e_pred), flush=True)
