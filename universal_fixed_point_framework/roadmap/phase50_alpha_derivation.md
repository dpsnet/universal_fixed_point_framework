# Phase 50：α 指数第一性推导路线图

## 状态评估

| 前提条件 | 状态 | 说明 |
|:--------|:----:|------|
| 谱 QFT 工具箱 | ✅ Phase 44 | 拉格朗日量、Feynman 规则、路径积分、重整化已翻译 |
| 谱作用量形式 | ✅ Paper XI | Tr(f(D/Λ)) 展开到曲率项 |
| IFS 谱框架 | ✅ Paper I | Rec/Spec 范畴、D 函子、谱对应 λ=e^(-μ) |
| γ_m 积分路径 | ❌ 已闭合 | 方向性矛盾：α_down < α_lepton 在 γ_m 框架不可实现 |
| α_l = d_H/2 | ✅ **已发现** | 0.24% 精度匹配（1.355 vs 1.358） |
| KO-维数手征结构 | ❌ 待发展 | 需要建立有限谱三元组的 IFS 自相似理论 |

## 推导链结构

```
Step 1: IFS 有限谱三元组
  └── 将内禀空间 (A_F, H_F, D_F) 构造为 IFS 自相似结构
  └── D_F 的谱标度律 → c_i^α
  └── 依赖：非交换几何标准模型 (Connes 2006)

Step 2: 谱维数 → α_base
  └── 证明 α_base = d_H/2 来自 IFS 吸引子的谱维数
  └── 轻子扇区无规范修正 → α_l = α_base ✅ 已验证
  └── 依赖：谱维数定理、IFS 热核展开

Step 3: KO-维数 → 扇区分化
  └── KO-维数 mod 8 = 6 的手征结构
  └── 上型/下型 Yukawa 耦合 H vs H̅ 的符号差异
  └── 规范联络对谱维数的修正 → δ_u, δ_d
  └── 依赖：实结构 J、手征算子 γ 的对易关系

Step 4: 数值验证
  └── α_u = α_base + δ_u = 1.945?
  └── α_d = α_base + δ_d = 1.229?
  └── 验证三代质量比全部在实验误差内
```

## 阶段划分

### Phase 50A：IFS 有限谱三元组构造（理论构建）

**输入**：
- Connes 标准模型谱三元组 (A_F, H_F, D_F)
- Paper I §6 IFS 谱理论
- `notes/spectral_alpha_exponent.md` 现有推导

**工作内容**：
1. 将有限代数 A_F = C ⊕ H ⊕ M₃(C) 嵌入 IFS 结构
2. 定义 IFS 收缩映射在表示空间上的作用
3. 构造 D_F 的 IFS 自相似分解
4. 证明 D_F 特征值标度律 = c_i^α

**产出**：
- `notes/spectral_finite_IFS_triple.md` — IFS 有限谱三元组构造
- `notes/proof_IFS_eigenvalue_scaling.md` — 特征值标度律证明

**验证标准**：
- 构造在数学上自洽（谱三元组公理满足）
- 特征值标度律与现有 c₁:c₂:c₃ = S₃S₄:S₄:1 一致

**依赖**：
- Paper I §6（Clifford 值谱、IFS RKHS）
- Connes & Marcolli (2008), *Noncommutative Geometry, Quantum Fields and Motives*

### Phase 50B：谱维数与 α_base（解析证明）

**输入**：
- Phase 50A 的 IFS 有限谱三元组
- d_H = 2.7095（已知）
- α_l = 1.358（已知拟合值）

**工作内容**：
1. 计算 IFS 谱三元组的谱维数 d_s
2. 建立 α 与 d_s 的关系 α = f(d_s, d_H)
3. 证明轻子扇区 α_l = d_H/2
4. 分析证明误差来源（0.24%偏差的解释）

**产出**：
- `notes/spectral_dimension_alpha.md` — 谱维数 → α 的严格推导
- 数值验证脚本 `paperX_alpha_spectral_dimension.py`

**验证标准**：
- α_l = d_H/2 的推导误差 < 1%
- 公式 f(d_s, d_H) 无自由参数

**依赖**：
- Phase 50A
- `notes/spectral_alpha_silence.md`（当前探索记录）

### Phase 50C：KO-维数手征修正 δ_u, δ_d（理论推导）

**输入**：
- Phase 50B 的 α_base 公式
- 标准模型手征结构 (SU(3)×SU(2)×U(1) 表示)
- 谱三元组 KO-维数 = 6 (mod 8)

**工作内容**：
1. 从 KO-维数的实结构 J 推导上型/下型的符号差异
2. 计算规范联络对谱维数的修正
3. 推导 δ_u = F(C_F·α_s, C_2·α₂, Y²·α₁) 的显式公式
4. 推导 δ_d 的显式公式（预期含符号翻转）

**产出**：
- `notes/spectral_KO_dimension_gauge_correction.md`
- 闭合形式 δ_u, δ_d 公式

**验证标准**：
- δ_u = +0.590（匹配 α_u = d_H/2 + δ_u = 1.945）
- δ_d = -0.126（匹配 α_d = d_H/2 + δ_d = 1.229）
- 修正量不自带自由参数

**依赖**：
- Phase 50B
- Connes (1996), *Gravity coupled with matter and the foundation of noncommutative geometry*
- `paper11_spectral_QFT.md` §9（谱传播子与谱 LSZ）

### Phase 50D：完整链数值验证

**输入**：
- Phase 50C 的闭合形式 α_u, α_d, α_l 公式

**工作内容**：
1. 计算三代质量比 m_u/m_t, m_c/m_t, m_d/m_b, m_s/m_b, m_e/m_τ, m_μ/m_τ
2. 与 PDG 实验值对比
3. 误差分析
4. 更新 `spectral_root_cause_analysis.md` 第 3 层

**产出**：
- `paperX_alpha_first_principles.py` — 第一性 α 计算脚本
- `spectral_root_cause_analysis.md` 更新（闭合 α 缺口）

**验证标准**：
- 全部 6 个质量比在 2σ 实验误差内
- 0 个拟合自由参数

**依赖**：
- Phase 50A-50C

## 时间估计

| Phase | 工作类型 | 估计工作量 |
|:-----|:--------|:---------:|
| 50A | 理论构造 | 中（2-3 周） |
| 50B | 解析推导 | 中（1-2 周） |
| 50C | 理论构造 | 难（3-4 周） |
| 50D | 数值验证 | 易（3-5 天） |
| **合计** | | **7-10 周** |

## 路线图

```
Phase 50A (2-3周)     Phase 50B (1-2周)     Phase 50C (3-4周)     Phase 50D (3-5天)
┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
│ IFS 有限谱三元组   │  │ 谱维数 → α_base  │  │ KO-维数手征修正   │  │ 完整链数值验证    │
│                  │  │                  │  │                  │  │                  │
│ D_F IFS自相似分解 │→│ α_l = d_H/2 证明  │→│ δ_u, δ_d 闭合公式 │→│ 6个质量比全部     │
│ 特征值标度律证明   │  │ 误差分析         │  │ 符号翻转机制      │  │ 在实验误差内      │
└──────────────────┘  └──────────────────┘  └──────────────────┘  └──────────────────┘
        ↓                     ↓                     ↓                     ↓
 notes/               notes/               notes/               spectral_root_cause_
 spectral_finite_    spectral_dimension_  spectral_KO_         analysis.md 闭合
 IFS_triple          alpha                dimension_gauge
```

## 相关资源

- `notes/spectral_alpha_exponent.md` — γ_m 路径的现有推导（已弃用，仅作参考）
- `notes/spectral_alpha_silence.md` — 当前探索记录（含已闭合路径和发现）
- `paperX_alpha_exponent_v2.py` — γ_m 积分数值脚本
- Paper XI (`paper11_spectral_QFT.md`) — 谱 QFT 形式化基础
- Paper I §6 — Clifford 值谱与纤维丛理论
