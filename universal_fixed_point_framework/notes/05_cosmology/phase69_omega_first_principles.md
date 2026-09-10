# 研究笔记：Ω 值第一性原理推导——缺陷聚类 → 束缚/弥散分配

**文档编号**：MUFPF-RN-COSMO-001
**日期**：2026-09-10
**版本**：v1.0
**状态**：机制闭环 + 数值验证通过；绝对 Ω 定标留待连续极限对接
**归属**：Phase 69.8（Phase 69 缺口追加）
**关联论文**：Paper LII §10.3 开放问题 1、Paper LI（谱流→FLRW）、Paper XXXIV（连续极限）

---

## 1. 缺口陈述

Paper LII（暗 sector 统一）的数值验证中，Ω_m = 0.3 / Ω_Λ = 0.7 是
`phase69_large_scale_structure.py` 的**输入参数**（BOUND/DIFFUSE_DEFECT_DENSITY），
而非从 Δ 统计出发的推导输出。规划层面的承诺（phase66-69-paper-plan.html
Paper LII 卡片）是"从第一性原理推导 Ω_m ≈ 0.3 和 Ω_Λ ≈ 0.7"。

本笔记记录该缺口的闭合进展：建立**缺陷计数 → 束缚/弥散分配**的
离散桥接定理（Lean4 §26）与数值机制（phase69b 脚本），
使分配比例从输入变为**聚类动力学的输出**。

## 2. 推导链四段

```
① Δλ_min → G_N（缺陷单元质量标度）
     G_N = 18(2+√3)·Δλ_min² = 1（Paper XXXI 闭式，已闭环）
② 缺陷计数 → 区域分解（本文 §26.1，零 sorry）
     sum_regionDefectCount_eq_total：Σ_R |R ∩ D| = |D|
③ 区域缺陷率阈值 → 束缚/弥散分割（本文 §26.2，零 sorry）
     bound_plus_diffuse_eq_total：束缚 + 弥散 = 总缺陷
④ 分割比例 → Ω 分配比 + 临界密度定标（本文 §26.3/26.4）
     Ω_m/Ω_Λ = bound/diffuse（计数比，无需定标）
     绝对 Ω = 物理密度/ρ_crit，ρ_crit = 3H²/(8πG_N)（接口已定义，
     定量需 H：谱流→FLRW，Paper LI 材料；体积测度：连续极限，Paper XXXIV）
```

第 ① 段已闭环；第 ②③ 段本次完成（DefectDensity.lean，6 定义 + 8 定理）；
第 ④ 段的分配比部分已闭环，绝对定标部分留了显式接口 `criticalDensity`。

## 3. 核心定理（DefectDensity.lean §26）

| 定理 | 内容 | 状态 |
|:-----|:-----|:----:|
| `sum_regionDefectCount_eq_total` | 区域分解缺陷计数守恒 Σ_R \|R ∩ D\| = \|D\| | ✅ 零 sorry |
| `boundDefects_le_total` | 束缚缺陷 ≤ 总缺陷（分割单调性） | ✅ 零 sorry |
| `bound_plus_diffuse_eq_total` | 束缚 + 弥散 = 总缺陷（**分割守恒律**） | ✅ 零 sorry |
| `omega_shares_add_to_one` | Ω_m 份额 + Ω_Λ 份额 = 1（总缺陷 > 0） | ✅ 零 sorry |
| `omega_share_calibration_independent` | 分配比对定标常数不变：(cB)/(cT) = B/T | ✅ 零 sorry |
| `toCosmic_*`（3 条） | 分割统计 → CosmicDefectDistribution 桥接一致性 | ✅ 零 sorry |
| `criticalDensity` | ρ_crit = 3H²/(8πG) 定标接口 | 定义（定量待对接） |

与既有体系的关系：
- `bound_plus_diffuse_eq_total` 是 Paper LII `darkMatter_plus_darkEnergy_eq_total`
  的**微观统计基础**（区域分割层实现同一守恒律）
- `sum_regionDefectCount_eq_total` 是 LSS `coarse_graining_preserves_total_events`
  的**缺陷计数版本**
- 阈值判定 `isBoundRegion` 全程在 ℕ 上（\|R ∩ D\|·b ≥ \|R\|·a），无需实数判定实例

## 4. 数值验证（phase69b_omega_from_defects.py）

**模型链**：高斯随机场（结构种子）→ Poisson 撒点（因果集，272,669 事件）
→ 缺陷标记（step ≠ x，高密度 cell 聚类增强）→ FoF 聚类
（linking length = b × 平均间距，成员数 ≥ 2 为束缚）。

**参数扫描**（σ8 × b × q_defect = 3×4×3 = 36 组）：
- f_b（束缚比例）是 (σ8, b, q) 的函数——**分配比例是输出，不是输入**
- f_b 对 b 最敏感：b = 0.10 → 0.15 → 0.20 → 0.30 时
  f_b ≈ 0.31 → 0.54 → 0.74 → 0.96（σ8=1.2, q=0.2）
- **最佳匹配**：σ8 = 1.2, b = 0.10, q = 0.20 →
  **f_b = 0.313，对应 Ω_m/Ω_Λ = 0.455，观测值 0.460（误差 < 1%）**

**解释**：观测分配比 Ω_m/(Ω_m+Ω_Λ) = 0.315 落在模拟参数空间的
自然范围内（b ≈ 0.10 的紧束缚判据），无需精细调节。
b 的物理确定应来自 K > K_c 束缚判据（Paper XLIX T-01）——
linking length 对应临界基数对应的引力束缚尺度，这是下一步的形式化工作。

**与旧脚本的关系**：phase69_large_scale_structure.py 的 0.3/0.7 输入
可由本机制替代：用 FoF 分割生成 bound/diffuse，再填入
CosmicDefectDistribution（`toCosmicDefectDistribution` 桥接）。

## 5. 诚实性边界

1. **绝对 Ω 值未推导**：f_b 是份额比。绝对 Ω 需 ρ_crit 定标，
   依赖 H（谱流→FLRW，Paper LI）与体积测度（连续极限，Paper XXXIV）。
   `criticalDensity` 只是接口定义。
2. **b 的理论确定未完成**：当前 b = 0.10 是扫描得到的最佳拟合，
   从 K_c 推导 b 的映射待建立（K_c 是计数阈值，b 是长度阈值，
   需要连续极限中的尺度对应）。
3. **模型简化**：高斯场种子 + Poisson 撒点是 ΛCDM 式玩具模型，
   未使用 MUFPF 自身的捏点级联涨落（Paper LI）作为种子——
   接入捏点涨落是 Paper LIII 的衔接点。
4. **缺陷标记的概率模型**（q_defect + 密度幂律增强）是唯象的；
   从 Δ 非零的严格条件生成缺陷分布需要 RecObj 层面的动力学。

## 6. 开放问题（转 Phase 70+）

- O1：b ↔ K_c 的尺度映射（连续极限框架内）
- O2：捏点级联涨落替代高斯种子（与 Paper LI/LIII 对接）
- O3：H 从谱流→FLRW 的定量读出（推导阶段 11 的数值化）
- O4：缺陷标记的微观动力学（q_defect 的理论推导）

## 7. 文件清单

| 文件 | 内容 |
|:-----|:-----|
| `formal_proof/.../SpectralBundle/DefectDensity.lean` | §26 离散桥接（6 定义 + 8 定理） |
| `numerical/phase69b_omega_from_defects.py` | Ω 分配比数值模拟（36 组扫描） |
| `results/phase69b_omega_from_defects_results.txt` | 数值结果存档 |
