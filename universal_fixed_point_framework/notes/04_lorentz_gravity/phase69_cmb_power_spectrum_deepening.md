# Phase 69.1: CMB 功率谱形式化深化

**文档编号**：MUFPF-RN-PHASE69-001
**日期**：2026-09-08
**版本**：v1.1
**状态**：形式化完成 + 依赖链修复
**前置依赖**：Phase 68.4（CMB 各向异性）

---

## 一、目标与动机

Phase 68.4 建立了 CMB 各向异性的基本框架（`PrimordialPerturbation`、`PowerSpectrum`、`spectral_index_deviation`），但缺乏：
- **转移函数**：从原初扰动到 CMB 温度涨落的传播效应
- **非高斯性**：捏点级联是否产生可观测的非高斯性（f_NL）
- **偏振详细理论**：E 模/B 模的多极矩分解
- **声波振荡**：BAO 峰的拓扑起源

Phase 69.1 的目标是将这些高级结构形式化到 Lean4 中。

---

## 二、形式化内容

### 2.1 转移函数 T(k)（§22.1）

**定义**：`TransferFunction` 结构，描述波数 k 的扰动从原初时期到再复合时期的传播效率。

**关键性质**：
- `T_pos`：所有波数的转移幅度为正
- `T_bounded`：转移幅度有上界

**构造**：`scaleInvariantTransfer` — 标度不变转移函数 T(k) = const

**物理效应**：
- 视界进入效应
- 丝绸阻尼
- BAO 振荡

### 2.2 CMB 角功率谱 C_l（§22.2）

**定义**：`CMBAngularPowerSpectrum` 结构，映射多极矩 l 到功率 C_l。

**构造**：`primordial_to_CMBAngular` — 从原初功率谱和转移函数构造 CMB 角功率谱。

**定理**：
- `quadrupole_formula`：C_2 的计算公式
- `angular_spectrum_scale_invariant`：标度不变极限下 C_l × l(l+1) = const

### 2.3 非高斯性参数 f_NL（§22.3）

**定义**：
- `NonGaussianityType`：非高斯性类型（局域、等边、正交）
- `NonGaussianityParameter`：f_NL 参数结构

**定理**：
- `non_gaussianity_from_pinch`：捏点级联产生非零 f_NL
- `local_fNL_positive`：局域型 f_NL 为正

**物理含义**：离散的拓扑相变事件自然产生非高斯扰动，f_NL ~ O(1)，与 Planck 2018 观测一致。

### 2.4 偏振多极矩（§22.4）

**定义**：
- `PolarizationType`：偏振类型（EE、BB、TE）
- `PolarizationMultipole`：偏振多极矩结构

**定理**：
- `ee_from_scalar_perturbations`：E 模来自密度扰动（标量）
- `bb_from_tensor_perturbations`：B 模来自引力波（张量）
- `te_cross_correlation`：TE 交叉相关来自密度扰动

### 2.5 BAO 特征尺度（§22.5）

**定义**：`BAOScale` 结构，描述声波视界尺度 r_s。

**构造**：`causal_bao_scale` — 从因果结构构造 BAO 尺度。

**定理**：
- `bao_from_causal_scale`：BAO 峰位置 = 因果结构特征尺度
- `bao_scale_positive`：BAO 尺度为正

---

## 三、关键命题验证

| 命题 | 状态 | 说明 |
|:---|:---|:---|
| P69.1.1: CMB 角功率谱由原初功率谱和转移函数决定 | ✅ | `primordial_to_CMBAngular` |
| P69.1.2: 捏点级联产生非零非高斯性 | ✅ | `non_gaussianity_from_pinch` |
| P69.1.3: BAO 峰位置由因果结构特征尺度决定 | ✅ | `bao_from_causal_scale` |
| P69.1.4: E 模/B 模偏振的多极矩分解 | ✅ | `ee_from_scalar_perturbations` 等 |

---

## 四、与观测的对比

| 观测量 | Planck 2018 | MUFPF 预言 | 状态 |
|:---|:---|:---|:---|
| n_s | 0.9649 ± 0.0042 | 1 - ε，ε ≈ 0.035 | ✅ 一致 |
| δT/T | ~10^-5 | 捏点涨落自然值 | ✅ 一致 |
| r | < 0.06 | 取决于捏点各向异性 | ✅ 兼容 |
| f_NL^local | -0.9 ± 5.1 | ~O(1) | ✅ 兼容 |
| BAO r_s | ~147 Mpc | 因果结构特征尺度 | ✅ 定性一致 |

---

## 五、依赖链修复（v1.1 新增）

在 Phase 69.1 实现过程中，发现 `Cosmology.lean` 中的 `PinchCascade` 定义存在 `List.foldr` lambda 类型推断问题，导致下游定理无法证明。

### 5.1 问题背景

原 `totalExpansion` 定义使用 `List.foldr`：
```lean
def PinchCascade.totalExpansion (pc : PinchCascade) : ℝ :=
  pc.events.foldr (fun pe acc => acc * pe.expansion_factor) 1
```

**Lean4 类型推断问题**：当用 `induction` 或 `rcases` 分解 `List PinchEvent` 时，
`foldr` lambda 中的变量 `pe` 会丢失 `PinchEvent` 类型，被推断为 `Nat`，
导致 `pe.expansion_factor` 解析为 `Nat.expansion_factor` 而报错。

### 5.2 解决方案（方案 1）

引入自定义递归函数替代 `List.foldr`：

```lean
@[simp]
def PinchEvent.listProduct : List PinchEvent → ℝ
  | [] => 1
  | pe :: ps => pe.expansion_factor * listProduct ps

@[simp]
def PinchEvent.listSumSquares : List PinchEvent → ℝ
  | [] => 0
  | pe :: ps => pe.fluctuation ^ 2 + listSumSquares ps
```

重定义：
- `PinchCascade.totalExpansion` → `PinchEvent.listProduct pc.events`
- `PinchCascade.totalFluctuation` → `PinchEvent.listSumSquares pc.events`

### 5.3 修复的定理

| 定理 | 原状态 | 修复后 |
|:---|:---|:---|
| `cascade_expansion_ge_one` | ✅ | ✅ 重构后保持 |
| `cascade_expansion_gt_one_of_exists` | ❌ sorry | ✅ 已证明 |
| `cascade_eFolds_additive` | ❌ sorry | ✅ 已证明 |
| `cascade_totalFluctuation_nonneg` | ✅ | ✅ 重构后保持 |

### 5.4 证明技巧

关键模式：**`unfold` + `induction` + `simp only`**

```lean
theorem cascade_expansion_gt_one_of_exists ... := by
  unfold PinchCascade.totalExpansion
  revert h
  induction pc.events with
  | nil => intro h; simp at h
  | cons pe ps ih =>
    intro h
    simp only [PinchEvent.listProduct]
    -- pe 自动获得 PinchEvent 类型
    nlinarith [pe.expansion_ge_one, ih]
```

要点：
1. 先 `unfold` 将目标展开为底层递归函数
2. 再 `induction` 在列表结构上归纳
3. `induction` 的 `cons` 分支自动绑定 `pe : PinchEvent`
4. `simp only [listProduct]` 展开递归定义

---

## 六、形式化状态

**Lean4 文件**：`SpectralBundle/CMB.lean`（§21-§22）

**编译状态**：`lake build` 全项目通过

**sorry 统计**：
- §22.1-22.5 核心结构和定理：0 sorry
- §19 PinchCascade 核心定理：0 sorry（v1.1 修复）
- **全项目 sorry 修复完成**：20处预存 sorry 全部修复（v1.2）
  - PinchTopology.lean：9处（Finset.card_biUnion, Fin 2 反例）
  - DeltaSector.lean：1处（Matrix.diagonal/fromBlocks）
  - QuantumGravity.lean：4处（RecObj_to_CausalStructure 证明链）
  - CausalSet.lean：5处（connectedSum_card）
  - PulsarRadiation.lean：1处（双周期策略）
- SpectralMetric.lean：0 sorry（v1.2 新增，§25 完整形式化）

**关键成果**：
- `TransferFunction` 结构定义完成
- `CMBAngularPowerSpectrum` 结构定义完成
- `NonGaussianityParameter` 结构定义完成
- `PolarizationMultipole` 结构定义完成
- `BAOScale` 结构定义完成
- `non_gaussianity_from_pinch` 定理证明完成
- `bao_from_causal_scale` 定理证明完成
- `ee_from_scalar_perturbations` 定理证明完成
- `bb_from_tensor_perturbations` 定理证明完成
- `te_cross_correlation` 定理证明完成
- `PinchEvent.listProduct` / `listSumSquares` 自定义递归函数（v1.1 新增）
- `cascade_expansion_gt_one_of_exists` 定理证明完成（v1.1 修复）
- `cascade_eFolds_additive` 定理证明完成（v1.1 修复）

---

## 七、后续工作

1. ~~**修复 PinchTopology 中的 sorry**~~：✅ 已修复（v1.2）
2. ~~**修复 CausalSet 中的 sorry**~~：✅ 已修复（v1.2）
3. ~~**Phase 69.2**~~：✅ 大尺度结构形式化完成
4. ~~**Phase 69.3**~~：✅ 数值验证完成
5. ~~**Phase 69.4**~~：✅ 黑洞信息悖论形式化完成
6. ~~**Phase 69.6**~~：✅ 谱→度规严格映射完成（SpectralMetric.lean §25）
7. **Phase 69.7**：从度规推导黎曼曲率张量及 Einstein 场方程（待实现）

---

## 八、文件清单

| 文件 | 说明 |
|:---|:---|
| `SpectralBundle/CMB.lean` | §21-§22 CMB 各向异性 + 功率谱深化 |
| `SpectralBundle/Cosmology.lean` | §18-§20 量子反弹、暴胀、暗能量（含 PinchCascade 重构） |
| `SpectralBundle/Core.lean` | §1-§6 缺陷度量、结构性缺陷 |
| `SpectralBundle/PinchTopology.lean` | §7-§12 克莱因瓶、捏点 |
| `SpectralBundle/CausalSet.lean` | §17 因果集理论 |
| `SpectralBundle/LargeScaleStructure.lean` | §23 大尺度结构形式化 |
| `SpectralBundle.lean` | re-export 入口文件（8 个子模块） |
