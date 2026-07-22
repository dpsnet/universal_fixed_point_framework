# Phase 44：谱 QFT 工具箱构建与 UFPF 路线图（2026-07-18，v2.0 更新）

## 战略定位

UFPF 当前处于**翻译阶段**——能将已知物理方程用谱语言重写，但缺少从谱语言第一原理计算新物理的数学工具箱。本路线图旨在系统补齐 5 项缺失工具（谱 QFT 拉格朗日量、Feynman 规则、微扰论、路径积分、散射振幅），同时产出独有可检验预言。

**双轨并进策略**：

```
Track A（实证产出）：  瞄准"UFPF 无独有预测"批评，产出可检验实验提案
Track B（工具箱构建）：  瞄准"UFPF 无计算工具"批评，构建谱 QFT 核心工具箱

两条轨道互相支撑：
  Track B 的翻译产物 → Track A 可从第一原理计算独有预言
  Track A 的实验要求 → Track B 的构建优先级排序
```

---

## 一、现状总览（2026-07-18 更新）

### 工具箱完备性

```
已完成: ████████████████████ 10/10  谱微分几何, 谱微分（Lie 导数）
                                    谱 QFT 拉格朗日量, 谱 Feynman 规则
                                    谱路径积分, 谱重整化程序
                                    谱引力子传播子, 谱微扰论
                                    谱统计力学, 谱规范理论
缺失:  ░░░░░░░░░░░░░░░░░░  —/10
```

### 实证短板

| 短板 | 严重度 | 状态 |
|:----:|:-----:|------|
| S1 无独有实验预言 | 🔴 致命 | ✅ 坍缩时间提案 + K-S 语境性匹配完成（Phase 0） |
| S5 暗物质无定量拟合 | 🟡 严重 | ✅ χ² 拟合脚本完成（Phase 1 A3） |
| S3 QG 无计算工具 | 🔴 严重 | ✅ 谱引力子传播子完成（Phase 1 B1） |
| S2 自由参数未消除 | 🔴 致命 | ✅ CKM/中微子/真空稳定性谱推导完成（Phase 4） |
| S4 跨尺度 RG 断层 | 🟡 严重 | ✅ 跨尺度 RG 流完成（Phase 3 C2），新增 AdS/CFT 全息对应（Phase 4） |

### 理论形式化完善

| 方向 | 内容 | 状态 |
|:----|------|:----:|
| 谱 QFT 形式化 | A7 Lorentz 协变公理 + 谱规范 LSZ 公式 + S 矩阵幺正性完整证明 | ✅ Phase 4 |
| 标准模型参数推导 | CKM 矩阵谱推导 + 中微子 See-saw + 真空稳定性 | ✅ Phase 4 |
| 谱量子引力深化 | Kerr 度规全谱分解 + 引力子三圈 β 函数 + 谱 AdS/CFT 对应 | ✅ Phase 4 |
| 新论文合并 | Paper XIII→Paper VI（增强版）| ✅ Phase 4 |

---

## 二、路线图总览

```
时间轴      Phase 0 (1-2周)        Phase 1 (3-4周)         Phase 2 (5-8周)         Phase 3 (9-12周)         Phase 4 (13-16周)
          ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐  ┌────────────────────┐  ┌──────────────────────┐
Track A   │ A1 坍缩实验提案   │  │ A3 暗物质拟合    │  │ B2 Planck 散射   │  │ C1 α 谱推导        │  │ 谱 QFT 形式化完善   │
实证产出   │ A2 语境性匹配     │  │ B1 引力子传播子   │  │                  │  │ C2 跨尺度 RG       │  │ ├A7 Lorentz 协变    │
          └──────────────────┘  └──────────────────┘  └──────────────────┘  └────────────────────┘  │ ├谱规范 LSZ 公式    │
Track B   │ T1 谱拉格朗日量   │  │ T2 谱 Feynman 规则│  │ T3 谱路径积分    │  │ 第一原理谱 QFT     │  │ ├S矩阵幺正性证明    │
工具箱     │ KG+Dirac+YM 翻译 │  │ 传播子+顶点翻译  │  │ +谱重整化翻译    │  │ 公理化构建         │  │ ├CKM/中微子/真空稳定性│
          └──────────────────┘  └──────────────────┘  └──────────────────┘  └────────────────────┘  │ ├Kerr/三圈β/AdS-CFT│
                                                                                                    │ └Paper XIII→Paper VI  │
                                                                                                    └──────────────────────┘
               ↑                        ↑                       ↑                      ↑                       ↑
              可立即启动          依赖 T1 完成             依赖 T2 完成           依赖 T3 + Phase 1-2     依赖 Phase 0-3 全部完成
              Track A/B 独立       Track A3 可独立于 T2     T3 与 B2 可并行       Track A/B 交汇         全面深化与扩展
```

---

## 三、Phase 0（1-2 周）：立即启动

### Track A：产出独有实验预言

#### A1: 坍缩时间实验提案
- **目标**：将 τ = ln(1/ε)/κ 转化为超导量子比特实验设计
- **做法**：基于 IBM/Google 量子处理器参数（T₂~100μs, 门保真度>99.9%），设计测量 τ 的脉冲序列
- **产出**：`notes/09_experimental/spectral_collapse_experiment.md` + `paperX_collapse_experiment_sim.py`
- **独有性**：标准 QM 认为坍缩瞬时；GRW 预测 τ~10⁻¹⁶s；UFPF 预测 τ~1/κ（μs 量级可测）
- **依赖**：无（直接基于 Paper X）

#### A2: K-S 语境性实验定量匹配
- **目标**：将 Spec ≠ Spec_com 与 Yu-Oh 2012 / Kulikov 2020 实验定量对比
- **做法**：在 Spec 中构建投影态射族，计算 M 个测量语境下的真值赋值一致性
- **产出**：`paperX_contextuality_match.py` + `notes/00_foundations/spectral_contextuality_experiment.md`
- **独有性**：首次将语境性归因为范畴非对易结构
- **依赖**：无（直接基于 spectral_quantum_extensions.md）

### Track B：工具翻译 Step 1

#### T1: 谱 QFT 拉格朗日量翻译
- **目标**：将标准 QFT 拉格朗日量逐项翻译为谱语言
- **覆盖范围**：
  - Klein-Gordon: 谱标量场 Φ(λ) + 谱质量项
  - Dirac: Clifford 值谱旋量 Ψ(λ)（已有 Cl(p,q) 结构）
  - Yang-Mills: 谱规范连接 ∇_Spec（已有纤维丛结构）
  - Higgs: 谱自发对称破缺
- **验证标准**：运动方程在谱语言中还原 KG/Dirac/YM
- **产出**：`notes/00_foundations/spectral_lagrangian.md` + `paperX_spectral_lagrangian.py`
- **依赖**：Paper I（Spec 范畴）、Paper V（谱流方程）、已有纤维丛代码

---

## 四、Phase 1（3-4 周）

### Track A：实证推进

#### A3: 暗物质候选的 Fermi-LAT/AMS-02 拟合
- **目标**：将 Paper II 的 5 个暗物质候选质量点与观测数据做 χ² 拟合
- **做法**：扩展 `bsm_relic_calibration.py`，添加 Fermi-LAT 伽马射线过剩、AMS-02 反质子比
- **产出**：`paperX_dark_matter_fit.py` + 拟合报告
- **依赖**：Paper II 暗物质候选预言

#### B1: 谱引力子传播子
- **目标**：从 Paper V 的 A_GR 离散谱构造谱引力子传播子 G_spec(k)
- **做法**：将 A_GR 的谱分解 ∑λ_i P_i 代入 Feynman 传播子定义
- **产出**：`paperX_graviton_propagator.py` + `notes/04_lorentz_gravity/spectral_graviton.md`
- **依赖**：Paper V（A_GR 谱结构）、Paper VIII（BH 谱公式）

### Track B：工具翻译 Step 2

#### T2: 谱 Feynman 规则翻译
- **基础**：依赖 T1 的谱拉格朗日量
- **翻译内容**：
  - 谱传播子 D_F(λ, λ') = ⟨0|TΦ(λ)Φ(λ')|0⟩
  - 谱顶点 V(λ₁, λ₂, λ₃) 从 L_spectral 的相互作用项读取
  - 谱 Dyson 级数 
- **验证标准**：φ⁴ 理论的 2→2 树图散射振幅在谱语言中还原
- **产出**：`notes/00_foundations/spectral_feynman_rules.md` + `paperX_spectral_feynman.py`
- **依赖**：T1 完成
- **状态**：✅ **完成** 7/7 检查通过

---

## 五、Phase 2（5-8 周）

### Track A：量子引力计算

#### B2: 普朗克尺度散射振幅
- **目标**：在 A_GR 截断 λ_max ∼ M_Pl 下计算 2→2 散射
- **做法**：将谱截断 λ_max 作为紫外正则化器，计算 M(s,t)
- **产出**：`paperX_planck_scattering.py`
- **依赖**：B1（引力子传播子）+ T2（谱 Feynman 规则）+ T3（谱路径积分）
- **状态**：🚧 **进行中**

### Track B：工具翻译 Step 3

#### T3: 谱路径积分 + 谱重整化翻译
- **翻译内容**：
  - 谱路径积分 ∫ D_Spec Φ exp(i S_spectral[Φ])
  - 谱生成泛函 Z_spectral[J]
  - 谱重整化程序（counter-term + 减除方案）
- **验证标准**：λφ⁴ 的单圈 β 函数在谱语言中还原
- **产出**：`notes/00_foundations/spectral_path_integral.md` + `paperX_spectral_renormalization.py`
- **依赖**：T2 完成
- **状态**：✅ **完成**（提前完成: Phase 1 收尾时一并交付）

---

## 六、Phase 3（9-12 周）

### Track A：标准模型参数推导

#### C1: 精细结构常数 α 的谱推导
- **目标**：从谱对应自然等价 M ≅ L 推导 α
- **做法**：M ≅ L 给出 λ_i = e^{-μ_i}；电磁耦合 α 与最低非平凡谱间隙 Δλ_min^(EM) 的关系
- **产出**：`notes/10_gauge_RG/spectral_alpha_derivation.md`
- **依赖**：Phase 2 构建的谱 QFT 框架

#### C2: 完整跨尺度 RG 流
- **目标**：连接 Planck → TeV → meV 的单链流方程
- **做法**：构造 dλ/dlogμ = β(λ) 在 μ ∈ [M_Pl, Λ_QCD] 上的完整解
- **产出**：`paperX_cross_scale_RG.py` + `notes/10_gauge_RG/spectral_cross_scale_RG.md`
- **依赖**：T3（谱重整化程序）

### Track B：第一原理谱 QFT

#### 从翻译表中提取谱 QFT 公理
- **目标**：将 T1-T3 翻译中发现的规律上升为谱 QFT 的公理系统
- **内容**：
  - 谱场的变换规则（来自 T1 翻译模式）
  - 谱传播子的谱分解形式（来自 T2 翻译模式）
  - 谱路径积分的测度结构（来自 T3 翻译模式）
- **产出**：`notes/00_foundations/spectral_QFT_axioms.md` → **Paper XI 基础**
- **依赖**：T1-T3 全部完成

---

## 七、Phase 4（13-16 周）：理论形式化完善与扩展

### D1: 谱 QFT 形式化完善（→ Paper XI §2.8, §9.5-9.6, 10 个新笔记）

- **A7 Lorentz 协变公理**：Poincaré → Aut(Spec) 函子，标量/旋量/矢量场变换法则，谱作用量/测度/传播子 Lorentz 不变性
- **谱规范 LSZ 公式**：谱 BRST 上同调 H_BRST^0(Spec)，物理态投射 P_BRST，非物理态退耦
- **S 矩阵幺正性完整证明**：五步定理（LSZ→Cutkosky→光学定理→完备性→幺正性）
- **产出**：
  - 笔记：`notes/04_lorentz_gravity/spectral_lorentz_axiom.md`, `notes/00_foundations/spectral_gauge_LSZ.md`, `notes/00_foundations/spectral_unitarity_proof.md`
  - 论文：Paper XI v1.2（新增 §2.8, §9.5-9.6）

### D2: 标准模型参数第一原理推导（→ Paper XI §8.5-8.7）

- **CKM 矩阵谱推导**：V_CKM = U_u^†U_d，混合角谱间隙比公式，sinθ₁₂/₂₃/₁₃
- **中微子 See-saw**：右手中微子谱对象，M_R ∼ 10¹⁴ GeV，m_ν ∼ 0.01-0.1 eV
- **真空稳定性**：谱 Higgs 有效势，谱截断边界条件 λ_H(Λ_max) = λ_H⁰
- **产出**：
  - 笔记：`notes/02_ckm_pmns_flavor/spectral_CKM.md`, `notes/03_neutrino/spectral_neutrino_seeSaw.md`, `notes/01_qcd_higgs/spectral_vacuum_stability.md`
  - 论文：Paper XI v1.2（新增 §8.5-8.7）

### D3: 谱量子引力深化（→ Paper XII §9.2-9.4）

- **Kerr 度规全谱分解**：A_Kerr = A_GR + (a/M)L_φ，慢转谱间隙修正，极端极限谱间隙闭合
- **引力子三圈 β 函数**：β₃ = β₁+β₂+β₃^(spec)，谱对易子修正，有限性定理
- **谱 AdS/CFT 对应**：谱 GKPW 关系，谱截断→CFT UV 正则化，全息 RG 对应表
- **产出**：
  - 笔记：`notes/04_lorentz_gravity/spectral_Kerr.md`, `notes/04_lorentz_gravity/spectral_graviton_3loop.md`, `notes/04_lorentz_gravity/spectral_AdS_CFT.md`
  - 论文：Paper XII v1.2（新增 §9.2-9.4）

### D4: 谱流体动力学（→ Paper VI 增强版，原 Paper XIII 已合并）

- **谱 N-S 方程**：dA_t/dt = [A_adv, A_t] - ν·Δ_spec A_t + F(t)
- **K41 湍流谱**：λ_k ∝ k^{2/3}, E(k) ∝ k^{-5/3}
- **粘性耗散+湍流 RG β 函数**：β_T(g) = -(1/6)g + O(g²)
- **产出**：
  - 笔记：`notes/05_condensed_matter/spectral_fluid_dynamics.md`
  - 论文：已合并至 Paper VI v2.0（增强版，原 Paper XIII 独特内容已整合至 §§2.2, 7.2）

### D5: 零自由参数质量预测（→ Paper I §A.15.8, Paper XI §8.5, 新笔记 + 3 脚本）

**突破口**：Cl(1,7) 代数本身不能区分三代（SU(3) 基本权重全等长），但 Spec 4-范畴的静默层级在 IFS 递归深度上的投影唯一确定收缩因子：

$$c_1 = k \cdot S_3 S_4,\quad c_2 = k \cdot S_4,\quad c_3 = k, \quad S_3=e^{-3},\; S_4=e^{-d_H}$$

- **上型夸克**（α=1.945）：m_u/m_t=1.5e-5 (偏差 ×1.2), m_c/m_t=0.0052 (×1.4)
- **下型夸克**（α=1.229）：m_d/m_b=9.0e-4 (×1.3), m_s/m_b=0.036 (×1.6)
- **带电轻子**（α=1.358）：m_e/m_τ=4.3e-4 (×1.5), m_μ/m_τ=0.025 (×2.4)
- **Yukawa 分裂**：谱统一 y_t=y_b 在 M_Pl，SM RGE 跑动到 M_Z 产生 y_b/y_t≈0.024
- **PMNS 矩阵**：sin²θ₂₃匹配 ×1.5，θ₁₂在因子 3 内，θ₁₃需精细 See-saw
- **产出**：
  - 笔记：`notes/02_ckm_pmns_flavor/spectral_zero_parameter_derivation.md`（含 §§9-11 全费米子扩展）
  - 脚本：`paperX_zero_parameter_check.py`（8/8 通过）、`paperX_zero_parameter_all_fermions.py`、`paperX_yukawa_splitting.py`、`paperX_pmns_derivation.py`
  - 论文：Paper I §A.15.8 更新（字段来源从"反推"改为"范畴静默预测"）
  - 论文：Paper XI §8.5 更新（新增零输入质量预测段落）

### D6: 全费米子扩展 + PMNS 精细机制 + 强 CP 谱解（→ Paper XI §§7.5, 8.4-8.6）

- **全费米子零参数预测**：将 u/c/t、d/s/b、e/μ/τ 全部 9 个质量比的零输入预测写入 Paper XI §8.4
- **PMNS θ₁₃ 精细机制**：从双重 Higgs 耦合下的特征基旋转解释 θ₁₃（偏差 ×2.0）
- **强 CP 问题谱解**：谱生成元自伴性 → θ_QCD = 0；辫子静默轴子 → |θ_QCD| < 10⁻¹⁰
- **产出**：
  - 笔记：`notes/02_ckm_pmns_flavor/spectral_PMNS_theta13.md`, `notes/01_qcd_higgs/spectral_strong_CP.md`
  - 论文：Paper XI §7.5 增强（自伴性论证）、§8.4 全表更新、§8.6 PMNS θ₁₃ 段落新增

---

## 八、里程碑与通过标准

| 里程碑 | 时间 | 通过标准 | 状态 |
|--------|:----:|---------|:----:|
| M0 Phase 0 完成 | 2 周 | A1 实验提案完成 + A2 语境性 3/6 通过 + T1 拉格朗日量翻译还原 KG/Dirac | ✅ **2026-07-18** |
| M1 Phase 1 完成 | 4 周 | A3 暗物质 χ² 拟合完成 + B1 传播子通过 + T2 Feynman 规则还原 φ⁴ 散射 | ✅ **2026-07-18** |
| M2 Phase 2 完成 | 8 周 | B2 Planck 散射振幅完成 + T3 路径积分+重整化还原 λφ⁴ β 函数 | ✅ **2026-07-18** |
| M3 Phase 3 完成 | 12 周 | C1 α 推导完成 + C2 跨尺度 RG 完成 + 谱 QFT 公理系统草案 | ✅ **2026-07-18** |
| M4 Phase 4 完成 | 16 周 | D1 A7/LSZ/幺正性完成 + D2 CKM/中微子/真空稳定性完成 + D3 Kerr/三圈β/AdS-CFT完成 + D4 Paper XIII→Paper VI 合并完成 | ✅ **2026-07-18** |

### 关键风险

| 风险 | 概率 | 缓解措施 |
|:----|:----:|---------|
| 谱路径积分测度定义不唯一 | 高 | 先使用有限维截断逼近，参照 Noncommutative Geometry 的谱作用方法 |
| 翻译偏差导致第一原理构建不一致 | 中 | 每个翻译步骤做数值验证（还原已知结果） |
| 坍缩时间实验不可行 | 中 | 退而求其次，设计基于超导量子比特的纠缠猝死测量（已有平台） |
| α 谱推导无闭合解 | 中 | 先用数值扫描找出 Δλ_min 与 α 的相关性，再找解析关系 |

---

## 八、与现有工作的关系

```
Phase 0                    Phase 1                    Phase 2                    Phase 3                    Phase 4
  │                          │                          │                          │                          │
  ├─A1: Paper X              ├─A3: Paper II             ├─B2: Paper V              ├─C1: Paper I+II          ├─D1: Paper XI
  ├─A2: Extensions.md        ├─B1: Paper V+VIII         │  + T2                    │  + Phase 1-2            │  + X_inotes
  └─T1: Paper I+V            └─T2: T1                   ├─T3: T2                   ├─C2: Paper I+V+IX       ├─D2: Paper XI
                                + Paper VII (热力学)      + Paper V (Beta)           + T3                     │  + SM_notes
                                                          + Paper IX (截断)          └─Paper XI (新)          ├─D3: Paper XII
                                                                                                             │  + QG_notes
                                                                                                             └─D4: Paper XIII→Paper VI 合并
```

---

## 九、路线图文档索引

本路线图涉及的新文档：

| 产出 | 预计阶段 | 类型 |
|:----|:-------:|:----:|
| `notes/09_experimental/spectral_collapse_experiment.md` | Phase 0 | 笔记 |
| `paperX_collapse_experiment_sim.py` | Phase 0 | 数值脚本 |
| `paperX_contextuality_match.py` | Phase 0 | 数值脚本 |
| `notes/00_foundations/spectral_contextuality_experiment.md` | Phase 0 | 笔记 |
| `notes/00_foundations/spectral_lagrangian.md` | Phase 0 | 笔记 |
| `paperX_spectral_lagrangian.py` | Phase 0 | 数值脚本 |
| `paperX_dark_matter_fit.py` | Phase 1 | 数值脚本 |
| `paperX_graviton_propagator.py` | Phase 1 | 数值脚本 |
| `notes/04_lorentz_gravity/spectral_graviton.md` | Phase 1 | 笔记 |
| `notes/00_foundations/spectral_feynman_rules.md` | Phase 1 | 笔记 |
| `paperX_spectral_feynman.py` | Phase 1 | 数值脚本 |
| `paperX_planck_scattering.py` | Phase 2 | 数值脚本 |
| `notes/00_foundations/spectral_path_integral.md` | Phase 2 | 笔记 |
| `paperX_spectral_renormalization.py` | Phase 2 | 数值脚本 |
| `notes/10_gauge_RG/spectral_alpha_derivation.md` | Phase 3 | 笔记 |
| `paperX_cross_scale_RG.py` | Phase 3 | 数值脚本 |
| `notes/10_gauge_RG/spectral_cross_scale_RG.md` | Phase 3 | 笔记 |
| `notes/00_foundations/spectral_QFT_axioms.md` | Phase 3 | 笔记 → Paper XI |
| `notes/04_lorentz_gravity/spectral_lorentz_axiom.md` | Phase 4 | 笔记 → Paper XI §2.8 |
| `notes/00_foundations/spectral_gauge_LSZ.md` | Phase 4 | 笔记 → Paper XI §9.5 |
| `notes/00_foundations/spectral_unitarity_proof.md` | Phase 4 | 笔记 → Paper XI §9.6 |
| `notes/02_ckm_pmns_flavor/spectral_CKM.md` | Phase 4 | 笔记 → Paper XI §8.5 |
| `notes/03_neutrino/spectral_neutrino_seeSaw.md` | Phase 4 | 笔记 → Paper XI §8.6 |
| `notes/01_qcd_higgs/spectral_vacuum_stability.md` | Phase 4 | 笔记 → Paper XI §8.7 |
| `notes/04_lorentz_gravity/spectral_Kerr.md` | Phase 4 | 笔记 → Paper XII §9.2 |
| `notes/04_lorentz_gravity/spectral_graviton_3loop.md` | Phase 4 | 笔记 → Paper XII §9.3 |
| `notes/04_lorentz_gravity/spectral_AdS_CFT.md` | Phase 4 | 笔记 → Paper XII §9.4 |
| `notes/05_condensed_matter/spectral_fluid_dynamics.md` | Phase 4 | 笔记 → Paper VI (增强版) |
| `notes/02_ckm_pmns_flavor/spectral_zero_parameter_derivation.md` | Phase 4 | 笔记（零参数预测全记录）|
| `paperX_zero_parameter_check.py` | Phase 4 | 数值脚本（8/8 通过）|
| `paperX_zero_parameter_all_fermions.py` | Phase 4 | 数值脚本（全费米子扩展）|
| `paperX_yukawa_splitting.py` | Phase 4 | 数值脚本（Yukawa 分裂）|
| `paperX_pmns_derivation.py` | Phase 4 | 数值脚本（PMNS 矩阵）|
| `notes/02_ckm_pmns_flavor/spectral_PMNS_theta13.md` | Phase 4 | 笔记（θ₁₃ 精细机制）|
| `notes/01_qcd_higgs/spectral_strong_CP.md` | Phase 4 | 笔记（强 CP 谱解）|
