# Phase 60：范畴理论绝对性验证路线图

> **目标**：实现 UFPF 范畴理论层面的完全独立验证，不依赖物理实例层的实验数据。
>
> **原则**：验证对象是元公理层和结构定理层本身，而非其物理应用。实例层的"正确性"不构成对上层公理的验证。
>
> **策略**：三条路径并行，按投入产出比排序执行。
>
> **进度**：✅ 路径 C 已完成（2026-07-30）—— `verify/` 模块 8/8 全部 PASS。✅ 向外推形式化已完成（2026-07-30）—— `CoherenceToBranching.lean §11` 新增 `dimension_gap` + `outward_proof_maps_to_orthogonal_layer`（维数间隙 ln 15 < 3 + 层正交分离 S₄/c₁ = e³）。详见下文 §Lean 形式化更新。✅ **路径 B 已完成（2026-07-31）**—— `agda_formalization/` 核心 8 模块（B1-B8）全部通过 Agda 2.8.0 类型检查，`Everything.agda` 整体编译通过，定理签名与 Lean 一一对应。详见下文 §路径 B 状态。

---

## 三路径总览

| 路径 | 方法 | 时间 | 验证类型 | 状态 | 产出 |
|:-----|:------|:----:|:---------|:---:|:-----|
| **C** | Python 可执行范畴语义 | 数天 | 运行时自洽性 | ✅ **已完成** | `python -m verify.run_all` → 8/8 PASS |
| **B** | Agda/Coq 独立重形式化 | 数周 | 证明助理交叉验证 | ✅ **已完成** | `agda_formalization/` 8 模块编译通过（Agda 2.8.0） |
| **A** | Lean 零 `sorry` 持续闭合 | 长期 | 机器证明完备化 | 🔄 持续 | 全库零 `sorry` |

---

## 路径 C：可执行范畴语义（已 ✅ 完成）

### 状态

**2026-07-30 完成**。`verify/` 模块 8/8 全部 PASS，注册于 `run_all_tests.py`（Phase 60）。

```bash
$ cd universal_fixed_point_framework
$ python -m verify.run_all
✓ PASS  V1   Sp is strict 4-category
✓ PASS  V2   D functor is faithful
✓ PASS  V3   D ⊣ R triangle identities
✓ PASS  V4   Spectral correspondence natural
✓ PASS  V5   Unified 3 theorem
✓ PASS  V6   Inequality chain
✓ PASS  V7   c₁ < c₂ < c₃
✓ PASS  V8   Delta algebraic form
结果: 8/8 通过 — 范畴理论自洽性验证完成
```

### 实现方案（参考）

在 `ufpf/` 包中新增 `verify/` 子模块：

```
ufpf/
├── core/              # 现有：范畴定义、函子
│   ├── category.py
│   ├── functor.py
│   └── natural_transformation.py
├── verify/            # 新增：验证套件
│   ├── __init__.py
│   ├── categorical_axioms.py    # 范畴公理自洽性检查
│   ├── sp_4_category.py         # Sp 严格 4-范畴条件
│   ├── D_adjunction.py          # D ⊣ R 伴随 + 三角恒等式
│   ├── spectral_correspondence.py # 谱对应自然同构
│   ├── coherence_conditions.py  # 交换律偏差检测
│   └── run_all.py               # 一键运行全部验证
└── examples/
    └── verify_demo.py           # 演示脚本
```

### 验证项清单

| # | 验证项 | 对应 Lean 模块 | 检查方法 |
|:-:|:-------|:---------------|:---------|
| V1 | $\mathbf{Sp}$ 是严格 4-范畴 | `SpCategory.lean` | 对象/1-/2-/3-态射的四层复合检查，结合律/单位律/交换律自动测试 |
| V2 | D 函子忠实性 | `DecursionFunctor.lean` | 生成随机态射，验证 $D(f) = D(g) \Rightarrow f = g$ |
| V3 | D ⊣ R 三角恒等式 | `DecursionFunctor.lean` | 对随机对象验证 $\varepsilon_D \circ D(\eta_R) = \text{id}$ 及对偶 |
| V4 | 谱对应 $\lambda = e^{-\mu}$ 自然性 | `SpectralCorrespondence.lean` | 验证自然性方块对所有态射交换 |
| V5 | 统一 3 定理 | `Unified3Theorem.lean` | 检查 $d = N_{\text{gen}} = \log_2 k_{\max} = N_{\text{active}}$ |
| V6 | 不等式链 $\ln 15 < d_H < e < 3$ | `DHStructuralAnalysis.lean` | 数值精度浮点验证 |
| V7 | $c_1 < c_2 < c_3$ 排序 | `IFSFractal.lean §6` | 对全域 $d \geq 1$ 扫描 |
| V8 | 偏差 $\Delta$ 的代数形式 | `DeviationBound.lean` | 随机矩阵测试 `spExchangeLaw_deviation_partial_commutator` |

### 成功标准

```bash
$ ufpf-verify --all
✓ V1: Sp is strict 4-category ......... PASS
✓ V2: D functor is faithful .......... PASS
✓ V3: D ⊣ R triangle identities ...... PASS
✓ V4: Spectral correspondence natural . PASS
✓ V5: Unified 3 theorem .............. PASS
✓ V6: Inequality chain ................ PASS
✓ V7: c1 < c2 < c3 ................... PASS
✓ V8: Delta algebraic form ........... PASS
All 8/8 verification checks passed.
```

---

## 路径 B：独立证明助理重形式化（数周，第二优先）

### 动机

Lean 4 是单一实现。**用不同证明助理独立实现核心模块**，消除证明助理 bug / mathlib 假设 / 形式化风格的潜在偏差。

### 选择：Agda

推荐 Agda 而非 Coq，原因：
- Agda 的范畴论生态（`agda-categories`）更成熟
- Agda 的依赖类型风格接近范畴论的"自然推导"
- 相对 Lean 的额外收益最大（类型论体系不同：Lean 依赖 CIC，Agda 用 Martin-Löf 类型论）

### 重形式化范围（核心 8 模块）

| # | 模块 | 对应 Lean | 工作量估计 | 状态 |
|:-:|:-----|:----------|:----------:|:----:|
| B1 | $\mathbf{Sp}$ 4-范畴定义 | `SpCategory.lean` | 2 天 | ✅ `Sp/SpCategory.agda` |
| B2 | 高阶态射（2-/3-态射） | `HigherSpCategory.lean` | 3 天 | ✅ `Sp/HigherSpCategory.agda` |
| B3 | D 函子 + 伴随 | `DecursionFunctor.lean` | 2 天 | ✅ `DecursionFunctor/DecursionFunctor.agda` |
| B4 | $d_H$ 不等式链 | `DHStructuralAnalysis.lean` | 1 天 | ✅ `DHStructural/DHStructuralAnalysis.agda` |
| B5 | 统一 3 定理 | `Unified3Theorem.lean` | 2 天 | ✅ `Unified3/Unified3Theorem.agda` |
| B6 | Bott 塔 | `BottTower.lean` | 2 天 | ✅ `BottTower/BottTower.agda` |
| B7 | 静默定理组 | `CoherenceToBranching.lean` | 3 天 | ✅ `CoherenceToBranching/CoherenceToBranching.agda` |
| B8 | IFS 排序定理 | `IFSFractal.lean §6` | 1 天 | ✅ `IFSFractal/IFSFractal.agda` |
| | **合计** | | **约 16 天** | **8/8 编译通过** |

### 成功标准

Agda 版本的 8 个核心模块通过类型检查（`agda --ignore-interfaces Everything.agda`），导出定理与 Lean 版本一致。
注：`--safe` 模式下 `postulate` 不被允许；ℝ 实数公理、ℂ 占位类型及部分解析定理（exp/log 分析、omega 自动化）
在 Agda 版本中以 `postulate` 声明，纯结构部分（层双射、计数、Moran 方程绑定、层独立性、维数分解）直接证明。

### 交叉验证协议

```
Lean 版本:  定理 T 的证明链 L₁ → L₂ → ... → Lₙ
Agda 版本:  定理 T 的证明链 A₁ → A₂ → ... → Aₙ

验证: 证明链长度一致，中间引理一一对应
```

### 路径 B 状态（2026-07-31 完成）

`agda_formalization/` 目录结构（8 模块，全部编译通过）：

```
agda_formalization/
├── UFPF.agda-lib                    # Agda 库注册（name: UFPF）
├── Everything.agda                  # 全部模块导入，整体编译验证
├── Sp/
│   ├── SpCategory.agda              # B1: 𝐒𝐩 4-范畴（对象/1-态射/层结构/层对计数）
│   └── HigherSpCategory.agda        # B2: 2-态射、3-态射、交换律偏差结构
├── Rec/
│   └── RecCategory.agda             # Rec 范畴（有限状态 + 演化规则）
├── DecursionFunctor/
│   └── DecursionFunctor.agda        # B3: D 函子 + 右伴随 R + 伴随对 D ⊣ R
├── DHStructural/
│   └── DHStructuralAnalysis.agda    # B4: d_H 不等式链（ln 15 < 65/24 < e < 3）
├── Unified3/
│   └── Unified3Theorem.agda         # B5: 统一 3 定理（card = 3 双射 + GenSpace + Bott 截断）
├── BottTower/
│   └── BottTower.agda               # B6: Bott 塔（旋量维数翻倍 + log₂ k_max = 3）
├── CoherenceToBranching/
│   └── CoherenceToBranching.agda    # B7: 分支计数原理 + 层独立性 + 向外推
└── IFSFractal/
    └── IFSFractal.agda              # B8: 物理 3-map IFS + c₁ < c₂ < c₃ 排序
```

与 Lean 的双实现一致性要点：

| 模块 | Agda 中直接证明 | Agda 中 postulate |
|:-----|:---------------|:------------------|
| B1 | `B-eq-15 : layerPair-count ≡ 15`（refl） | `compose` 占位 |
| B4 | `dimension-gap`（链传递） | ℝ 公理、`dH_from_branching` |
| B5 | `card-active-layers`（显式双射）、`genSpaceEquiv`、`bott-truncation-index` | 正交性、层条件 |
| B6 | `spinorDim-succ`（递归定义 refl）、`spinorDim-eq-pow`（归纳）、满射前像 | `log2` 公理 |
| B7 | `layers-distinct`（≃ Fin 5）、`branchIndex-dH-unique`（双向）、层独立性、维数分解 | ℝ 分析、`layerPair-card-15` |
| B8 | `physicalIFS-n ≡ 3`（refl） | 收缩率正性/排序/Moran 方程 |

### 路径 B 闭合路线图（2026-07-31 立项）

**立场**（2026-07-31 用户决议）：签名镜像不构成第二条验证路径。路径 B 必须**完整闭合**——Agda 侧以独立证明覆盖全部定理，含实分析层（T3）。未闭合前，每条 postulate 均为登记在案的开放项。

**闭合账目**（47 个 postulate 块中，定理形状的可闭合项）：

| 层级 | 待闭合项 | 所需机制 | 状态 |
|:-:|:---------|:---------|:----:|
| **T1 纯 ℕ/组合** | `layerPair-card-15`（B7） | 显式双射枚举（15 项） | ✅ 已闭合（2026-07-31） |
| | `spacetime-dim-eq-category-order`（B7） | ℕ 归纳（∸-zero/∸-1） | ✅ 已闭合（2026-07-31） |
| | `dimension-counting-eq-two-mul`（B7） | ℕ 归纳（+ℕ-suc/∸-1） | ✅ 已闭合（2026-07-31） |
| | `category-order-unique`（B7） | ℕ 算术（half-2*ℕ/half-8 链） | ✅ 已闭合（2026-07-31） |
| | `log2`（B5/B6） | 良基递归 WfRec（NatArith §3：`<`/`Acc`/`wfRec` + `half-lt` 递减引理） | ✅ 已闭合（2026-07-31） |
| **T2 结构增强** | B1 `compose`/`𝟙-matrix`/`unit-intertwine` | ℤ/3 载体 + 矩阵乘/单位矩阵具体构造；`*mat-id-l/r`（矩阵单位律）+ 真实 `unit-intertwine`（𝟙·A=A·𝟙）均闭合 | ✅ 构造与单位律闭合 |
| | B1 `*mat-assoc`（矩阵乘法结合律） | `sumFin` 代数引理链（`+-rearrange`/`sumFin-+`/`sumFin-distrib-r/l`/`sumFin-swap`）+ ℤ/3 环律 | ✅ 已闭合（2026-07-31） |
| | B1 `zeroMat-absorb-l/r`（零矩阵吸收） | `sumFin-cong` + `*-zero-l/r` + `sumFin-zero` | ✅ 已闭合（2026-07-31） |
| | B2 `spVertComp-assoc`/`spThreeVertComp-assoc` | ℤ/3 加法结合律 + `SpTwoMorphism-≡`/`SpThreeMorphism-≡`（UIP） | ✅ 已闭合（2026-07-31） |
| | ℤ/3 环律全套 | `+-assoc/comm/id/inv`、`*-assoc/comm/id/zero/distrib`（有限情形枚举） | ✅ 已闭合（2026-07-31） |
| | B2 condition 字段真实化 | `SpTwoMorphism.condition`/`SpThreeMorphism.condition` 升级为真实交换子等式；`id-two-morphism`/`spVertComp`/`id-three-morphism`/`spThreeVertComp` 条件经 `commutator-add`/`-mat-cancel-mid` 闭合；`layer2/3-condition` 直接引用 | ✅ 已闭合（2026-07-31） |
| | B2 `spHorizComp`/`spThreeHorizComp` 同伦构造 | 具体同伦构造（`α·P' + Q·α'`，与 Lean 公式一致） | ✅ 已闭合（2026-07-31） |
| | B2 水平复合 condition | `spHorizComp-condition`/`spThreeHorizComp-condition`（交换子代数引理链：`neg-mul-l/r`/`horiz-cross-scalar`/`*mat-distrib-l/r-minus`/`horiz-cross`，对应 Lean 侧 70 行证明链） | ✅ 已闭合（2026-07-31） |
| | B3 左三角恒等式（adjUnit/left-triangle） | adjUnit 构造为常函数同态（R-obj step 为恒等）；left-triangle 两边均为零矩阵态射，refl | ✅ 已闭合（2026-07-31） |
| | B3 右三角恒等式（right-triangle） | 论文正确构造 C2.2/R11（R(E) 演化映射 = e^{-A_E}，仅 D 的像子范畴上严格，定理 2.4.5）；Lean 恒等原型（step=id, P=1）隐含 nS=nT + S.A=单位矩阵两个未声明条件，非论文构造的忠实实现；有限维化依赖 exp | ⏳ 登记待闭合（T3 依赖） |
| | B3 R11 有限维化（SpImD 子范畴） | 对应 RAP5a：SpIso/SpImD/DIm-obj/R-obj-img/DR-iso/adjUnit-img/adjCounit-img 对象层闭合；`left-triangle-img` 闭合（𝟙·𝟙=𝟙） | ✅ 对象层闭合 |
| | B3 SpImD 态射层（RIm_map/右三角） | **结构性不可闭合（基数反例）**：2 状态平凡系统下 Hom_Sp(D(X),D(Y)) = ℂ⁴（不可数）vs Hom_Rec(X,Y) = 4（有限），无双射；P=[[1,0],[1,1]] 是合法谱态射但非转移矩阵（D 的 full 性为假）。闭合仅当态射限制为转移矩阵（平庸化）或转无限维（论文 R11 断言，需 T3 谱定理验证）。**定性为 S0 表示静默**（`notes/00_foundations/spectral_representation_silence.md`），推进方向见下文 §后续影响与推进方向 | ⏳ 登记（结构性障碍，S0 静默） |
| | Lean 侧 DAdjR 编译失败（交叉校验） | `lake env lean` 验证失败：RFunctor.map 恒等需 nS=nT（L30）、adjUnit 需 step=id（L48）、adjCounit P=1 无 OfNat 实例/交织需 S.A=单位阵（L58-59）；正确路径为 RAP5a SpImD 方案 | ✅ 已核实并标注（Adjunction.lean 审计注释） |
| | B5 `layer-orthogonality` | ℂ 三元素载体 + 9 情形枚举 | ✅ 已闭合（2026-07-31） |
| | B5 `layer1-condition` | 真实交织 `P·A_Y = A_X·P` + `-mat-elim`（`cong-app` + `+-inv`） | ✅ 已闭合（2026-07-31） |
| | B5 `layer2/3-condition` | 经 `SpTwoMorphism.condition`/`SpThreeMorphism.condition`（真实化后直接引用） | ✅ 已闭合（2026-07-31） |
| | SpHom 真实交织条件 | `SpHom.intertwine` 升级为真实等式 `P·A_Y = A_X·P`；`compose-intertwine`（`*mat-assoc` 链）与 `unit-intertwine` 真实闭合；DecursionFunctor 零矩阵态射（idSp/compSp/adjCounit）经 `zeroMat-absorb` 闭合 | ✅ 已闭合（2026-07-31） |
| | B3 `transferMatrix` 具体化 | 对应 Lean `fun i j => if f i = j then 1 else 0`；`transferMatrix-comp`（反变复合，`sumFin-pick-dep-l` + `if-mul-lemma`）闭合 | ✅ 已闭合（2026-07-31） |
| | B3 `D-map-intertwine` | `transferMatrix-comp` + `RecHom.comm`（对应 Lean `DFunctor_map`） | ✅ 已闭合（2026-07-31） |
| | B3 `transferMatrix-inj`（D 忠实性） | `Fin-eq?-refl/true` + `if-c1` + 逐点单射（对应 Lean `transferMatrix_injective`） | ✅ 已闭合（2026-07-31） |
| **T3 实分析** | B4 不等式链（`ln15-lt-65-24` 等） | exp/log 分析开发 | ✅ 已闭合（2026-07-31）：`ln15-lt-65-24`/`sixtyfive-over-24-lt-e`/`e-lt-3` 全为定理（阶段 2-3）；其余见下方阶段 3 开放项 |
| | T3 阶段 3 scoped 公理 `ln2-lt`（ln2 < 0.69317） | Σ 1/(k·2^k) 级数上界（定义性公理，待实现为可证明定理） | ⏳ 登记开放（log 级数机制，阶段 3+ 待建） |
| | T3 阶段 3 scoped 公理 `ln1615-lb`（ln(1+1/15) > 29/450） | ln(1+u) 交替级数下界（定义性公理） | ⏳ 登记开放（同上） |
| | T3 阶段 3 scoped 数值公理 `ln15-arith-ax`（4·0.69317-29/450 < 65/24） | 纯有理比较；分母 ~1e5、交叉乘积 1e9-1e11 超出 `_*ℕ_` 归一化能力（实测挂起）——资源/实践静默，非结构性；标准分析中可计算验证 | ⏳ 登记开放（需算术决策机制/反射，或更高效的 ℕ 算术） |
| | T3 exp 单射（`exp-inj`） | exp-mono 严格单调 + 三分律 | ✅ 已闭合（2026-08-01）：trichotomy-ℝ 三分律 + exp-mono（严格单调）+ irreflexive-ℝ 排除两严格分支，零新增公理——不再为 postulate |
| | T3 阶段 6 谱定理层（`SpectralTheory/SpectralTheory.agda`） | 谱测度/Fuglede/Hille-Yosida（无限维谱论） | 🔄 首轮完成（2026-08-01）：谱论基础公理（Borel 谓词谱测度 E/谱表示/谱积分线性/Fuglede 方向/谱测度复合/外延/Hille-Yosida/函数演算 fc）+ **引理 2 核心 M_Rec ⊆ M_σ 可证**（`Rec-to-σ`：Fuglede 对 e^(-A) → 谱测度复合 → E-phi-image，φ 单射经 exp-inj）+ 定理 3 无限维版（theorem3）+ 推论 5（corollary5 对象重建）；谱论基础登记公理并注明降定理路径；Everything.agda 14 模块编译通过 |
| | B4 Moran 方程族（`dH-from-branching`） | rpow-exp + exp/log 代数 | ✅ 已闭合（2026-07-31）：(e⁻¹)^{ln15} = e^{-ln15} = 1/15 [rpow-exp + log(e⁻¹)=-1 + exp-recip]，15·(1/15)=1 |
| | B4 Moran 解唯一（`dH-moran-solution-unique`） | exp-inj + exp-recip + 商消去 | ✅ 已闭合（2026-07-31）：e^{-x}=1/15=e^{-ln15} ⟹ -x=-ln15 [exp-inj，**已闭合 2026-08-01**：三分律 + exp-mono] ⟹ x=ln15 |
| | B4 Moran 解存在（`moran-solution-iff`） | rpow-exp + log 换底 + 取负乘法 | ✅ 已闭合（2026-07-31）：B·r^x=1 ⟹ x·log r=-log B ⟹ x=log B/log(1/r) [*-div-impl + neg-mul-ℝ + log-recip] |
| | B4 粘合递归（`glued-recursion-fixed-point`/`glued-recursion-dH-eq-ln15`） | 二次方程 + 正根选择 + ρ 范围 | ✅ 已闭合（2026-07-31）：通用版设 x=r^d [rpow-2d-sq] ⟹ (1-ρ)x+A·x²=1，factor-glued 因式分解 (Bx-1)·M=0，glued-M-pos（x>0、B-1>0、ρ≥0）⟹ M>0，zero-factor-ℝ ⟹ Bx-1=0（M=0 分支被 irreflexive-ℝ 排除）⟹ B·r^d=1 ⟹ moran-solution-iff ⟹ d=log B/log(1/r)；特化版 B=15、r=e⁻¹：log(1/(e⁻¹))=1 [log-recip+log-exp+neg-neg] ⟹ d=ln15 [div-one-ℝ]。新定义性公理 3 条：`trichotomy-ℝ`/`zero-factor-ℝ`/`irreflexive-ℝ`（标准全序域）。**阶段 4 全部闭合，无剩余 postulate** |
| | B4 §5 唯象不等式（`sixtyfive-over-24-lt-dH`） | 公共分母通分 + 中间步控制规模 | ✅ 已闭合（2026-07-31）：65/24 < 27095/10000，公共分母 6000（16250 < 16257，经 5419/2000 中间步） |
| | B4 §5 唯象不等式（`dH-lt-e`） | partial-e 5 = 163/60 通分 + exp 级数截断 | ✅ 已闭合（2026-07-31）：d_H < 27100/10000 < 813/300 < 815/300 = partial-e 5 < e |
| | B4 完整链（`inequality-chain-full`） | 四项闭合积类型组合 | ✅ 已闭合（2026-07-31）：(ln15 < 65/24) × (65/24 < d-H-fit) × (d-H-fit < e) × (e < 3) |
| | B7 `r-uniform-pos`/`r-uniform-lt-one`（收缩率 0<e⁻¹<1） | exp 正性 + 单调 | ✅ 已闭合（2026-07-31）：exp-pos + exp-mono（-1<0 经取负引理）+ exp-zero |
| | B7 `ln15-solution-form`（Moran 解标准形式） | log 换底 + 逆 | ✅ 已闭合（2026-07-31）：log(1/(e⁻¹)) = 1 经 log-recip + log-exp + neg-neg，log 15/1 = log 15 [div-one-ℝ] |
| | B7 静默分离（`silence-separation`） | exp 不等式 | ✅ 已闭合（2026-07-31）：e⁻³<1 [exp-mono + *-pos-mono + *-zero] × e⁻ᵈ>0 保序 |
| | B7 静默裕度（`silence-margin`，S₄/c₁ = e³） | exp 商结构 + 除法消去 | ✅ 已闭合（2026-07-31）：a/(b·a)=1/b [/-cross+comm+one-mul]，1/e⁻³=e³ [exp-add+neg-one-mul+exp-zero] |
| | B7 Moran 方程族（`moran-solution-iff` 等） | exp/log 场论 | ✅ 已闭合（2026-07-31，v0.35，同 B4 行） |
| | B8 收缩率 c₁/c₂ 正性 + <1（`c1/c2-physical-pos/lt-one`） | exp 正性 + 单调 | ✅ 已闭合（2026-07-31）：exp-pos + exp-mono + ≤-pos（d≥1⟹0<d） |
| | B8 `c1 < c2`（`c1-lt-c2-physical`） | exp 单调 + 取负 | ✅ 已闭合（2026-07-31）：exp-mono + -(3+d)<-d ⟸ 3+d>d |
| | B8 `exp-neg-one-lt-37-100`（e⁻¹ < 37/100） | 倒数单调 + B4 链 | ✅ 已闭合（2026-07-31）：e⁻¹=1/e<37/100 ⟸ 100/37<65/24<e |
| | B8 c₃ 组（`c3-physical-pos/lt-one`、`one-sub-c1d-c2d-pos`） | rpow 分析 | ✅ 已闭合（2026-07-31）：`one-sub-c1d-c2d-pos`（two-exp + pos-sub）、`c3-physical-pos`（one-sub + rpow-pos） |
| | B8 `moran-3map-holds`（c₁^d+c₂^d+c₃^d=1） | rpow 幂合成 + 减法定义 | ✅ 已闭合（2026-07-31）：c₃^d=(1-c₁^d-c₂^d)^((1/d)·d)=(1-c₁^d)-c₂^d [rpow-pow/rpow-one 可证 + sub-ℝ-def 基础假设]，cancel-sub 抵消 |
| | B8 `two-exp-add-exp-lt-one`（2e^{-d²}+e^{-d(3+d)}<1） | exp 定量估计 | ✅ 已闭合（2026-07-31）：≤ 层公理 4 条 + exp-mono-≤ + e⁻⁴<1/8<13/100 数值链 + /-add-same-ℝ 同分母加法，2e^{-d²}<74/100、e^{-d(3+d)}<13/100 ⟹ 和<87/100<1 |
| | B8 `c-physical-strictly-ordered`/`physicalIFS-ratios-ordered` | rpow 单调 + Moran | ✅ 已闭合（2026-07-31）：c₂<c₃ 经 c₂^d<c₃^d（two-exp 移项 + c3d-base）+ rpow-mono-inv-ℝ 单调逆；c₁<c₂ 已闭合；B8 全部闭合 |

**推进策略**：
1. **T1 ✅ 已全部闭合**（2026-07-31）：`NatArith/NatArith.agda` 算术引理库（含良基递归 §3）建成，5 项全部闭合。注：Lean 的 `bott_truncation_index` 为具体数值定理（`Nat.log 2 k_max = 3`），Agda 侧由良基递归定义 + 具体计算 refl 匹配；一般形式的 `log2-pow2` 不再需要（原为自加泛化，已移除）。
2. **T2**：重构 B1-B3 占位为具体构造；ℂ 载体扩充为至少 3 个互异元素。
3. **T3**：需实数/分析基础。Agda stdlib 无 exp/log/rpow——需自建（或引入 cubical 实数库），工程量级等同 Lean 侧 Mathlib 分析库，为持续主线。**T3 建设蓝图已立项（2026-07-31，`notes/00_foundations/spectral_T3_analysis_foundation.md`）**：闭合项盘点（B4/B7/B8/P1）+ 引理依赖图 + 建设阶段（0 序代数 → 1 部分和 → 2 exp 级数截断 → 3 log → 4 rpow → 5 P1）+ 最小公理集。阶段 0（ℝ 序代数公理：0<1、加法单调、乘正性、≤-混合传递）已完成并登记为基础假设。
4. 每条闭合项完成后在 `Everything.agda` 整体编译验证并更新本账目。

**已排除/不需闭合**：ℝ 公理体系本身（B4 §0）是基础假设（对应 Lean/Mathlib 的 ℝ 公理），非"未证明"，不计入闭合账目；B1/B2 记录条件占位（refl 型等式）随 T2 一并真实化。

### 后续影响与推进方向（2026-07-31，S0 表示静默）

**分析记录**：`notes/00_foundations/spectral_representation_silence.md`（§1-§9）。核心结论：SpImD 态射层的结构性不可闭合被定性为一种新静默类型——**S0 表示静默**（$P_{\mathrm{Im}(D)}(\varphi)=0$，谱态射在递归表示下不可达），静默体系由四层扩为五层（S0 + S1-S4）。

**影响**：
1. **理论核心层**：paper I 定理 2.4.5"严格成立"须限定为"对象层 + 受限态射层（转移矩阵）或无限维"；波及 paper XIX 定理 13.1、三层伴随嵌套地基、谱对应自然同构 $M\cong L$、完备性定理 5.32
2. **静默理论层**：S0 是"编码前"静默（与 S1-S4 的"编码后不可观测"平行独立）；态射限制为转移矩阵由此获得规范语义（保留 D-非静默态射的投影）
3. **形式化层**：有限维态射层结构性不可闭合（强行闭合只引入错误断言）；无限维（论文 R11）是唯一可能完整闭合路径，断言未形式化

**推进方向（按优先级）**：

| 优先级 | 方向 | 内容 | 依赖 | 状态 |
|:-:|:--|:--|:--|:--|
| P0 | 论文层范围修正 | paper I 定理 2.4.5 加限定；RAP 方案 §13.1"概念闭合"标注修正；paper XIX 定理 13.1 证明链注明依赖条件 | 无，文档修订 | ✅ 已执行（2026-07-31） |
| P1 | R11 无限维态射层严格验证（**决定性**） | 谱定理下验证 Hom_Sp(D(X),D(Y)) ≅ Hom_RecD(R(E),S) 的基数自洽与谱匹配断言——决定伴随"能否真闭合" | T3 分析层（谱定理 + 函数空间） | 🔄 已分析（2026-07-31：语义分岔判定）+ **有限维特例完整闭合**（2026-08-01，P1Spectral：定理 3 + 推论 4）+ **无限维组装完成**（2026-08-01，SpectralTheory §6：corollary4-∞ 恒等双射，定理 3 无限维版 + 引理 2 核心可证）；谱论基础登记公理（降定理路径），无限维形式化持续推进 |
| P2 | S0 静默理论结构 | S0 筛/sieve 判定、S_D 算子刻画、与 S1-S4 复合行为 | P0 后 | ✅ 完成（2026-07-31：sieve 判定 + 遗留项解析） |
| P3 | 物理对应研判 | 表示静默 ↔ 经典化/相干性丢失？是"特征还是缺陷" | P2 后 | ✅ 已执行（2026-07-31） |
| P4 | 基数反例形式化 | Agda/Lean 中证明"Hom_Sp 不可数 vs Hom_Rec 有限无双射" | 基础设施 | ✅ 已执行（Agda + Lean 双侧，2026-07-31） |

**关键判断**：P1 决定性——若 R11 无限维谱匹配断言成立，则伴随在无限维闭合、S0 仅出现在有限维原型；若不成立，则表示静默是结构性普遍现象，静默体系从"动力学现象分类"升级为"表示论基本约束"。P1 并入 T3（谱定理验证）。

**P2 部分完成（2026-07-31）**：sieve 判定为**负**——S0 静默态射类不构成 sieve（左、右复合均破坏静默，`paperX_s0_sieve.py` 7/7 PASS：S0 静默空间 = span{[[1,1],[-1,-1]]}；复合后 S_D 中位数 0.294、73% 压到 <0.5；n=3 时 S0 静默空间维数 = 2 非平凡；标量演化 e^{-t}I 保持静默——破坏源于结构性复合）。静默体系内部出现"筛/非筛"二元结构（S1-S4 构成 sieve，S0 不构成）。分析入笔记 `spectral_representation_silence.md §10-§10.2b`。剩余：S_D 下降率解析刻画、非平凡谱对象上动力学演化复合、高维维数闭式。

**P3 完成（2026-07-31）**：研判为**特征而非缺陷**——S0 静默是表示论基本约束（Rec 范畴定义本质：有限码本），首选"有损压缩"类比（区别于 decoherence：静默可经复合"打开"，非不可逆丢失）；早期"D ⊣ R 全域严格成立"声明过度属缺陷，已由 P0 修正。分析入笔记 §11。

**P4 完成（Agda + Lean 双侧，2026-07-31）**：
- **Agda**：`Cardinality/Cardinality.agda`——`P-spectral`（P=[[1,0],[1,1]] 合法谱态射，交织条件闭合）、`transferMatrix-not-P`/`D-not-full`（D 不 full）、`fun2-card`/`rec-hom-card`（Hom_Rec 恰 4 函数）、`transfers-distinct`/`P-distinct-transfers`（Hom_Sp ≥ 5 互异元素）；**§5 鸽笼补全**：`分类` + `fun2-excl-all` + `fun2-no-5`（5 个互异 F2→F2 函数不可能）；**§6 无双射**：`no-bijection`（Equiv (SpHom DX DX) (F2 → F2) → ⊥，4 转移矩阵态射 + P-spectral 五个互异 SpHom + 双射单射 + 鸽笼）。设计说明：Agda 侧计数落在**函数层**（Hom_Sp ≥ 5 vs |F2→F2| = 4）——RecHom-≡ 记录外延性需依赖版 funext，超出库公理范围（仅非依赖 funext），RecHom 经 rec-hom-card 落入同 4 类关联。注册 `Everything.agda` 整体编译通过，无新增 postulate。
- **Lean**：`RAP5a_explicit_adjunction.lean §7-§8`——`P_counter_morph`（交织经 A=1 平凡闭合）、`P_counter_not_transferMatrix`/`D_not_full`、`complex_emb`（ℂ↪Hom_Sp 单射）+ `homSp_infinite`（**Hom_Sp 不可数**）、`recHomTrivialEquiv`/`homRec_finite`（**Hom_Rec 有限**）、`no_bijection_homSp_homRec`（**无双射**——完全形式化的基数论证）。单独编译通过，无新增 sorry（L97 RIm_map 为既有登记项）。

**P1 分析完成（2026-07-31，理论层；形式化待 T3）**：落点 `notes/00_foundations/spectral_R11_morphism_layer.md`。结论——**谱匹配双射的真值取决于 Rec 态射语义**：
- **线性语义**（Rec_D 态射 = 有界线性谱匹配算子，论文 C2.3 隐含）：双射**成立且为恒等**（Hom_Sp = M_σ = Hom_Rec 同一方程解集；谱测度输送引理 + exp 单射引理）。伴随无限维闭合，S0 仅有限维原型。
- **集合语义**（框架 RecHom 原始语义 `toFun : Fin n → Fin m` 的无限维延伸）：双射**不成立**（存在非线性谱匹配映射，命题 6）。S0 静默升级为**结构性普遍现象**。
- 推荐裁决：采用线性语义闭合（与有限维"受限态射层=转移矩阵"连续）；构成 P0 之后的第二项论文层限定（无限维闭合需注明"受限态射层 = 线性连续谱匹配映射"）。依赖标准谱论事实：Fuglede 定理（谱测度输送）、exp/log 函数演算单射、Hille-Yosida（正自伴 m-增生）。

---

## 路径 A：Lean 零 `sorry` 持续闭合（长期）

### 当前状态

| `sorry` | 位置 | 性质 | 闭合路径 |
|:--------|:-----|:-----|:---------|
| `spExchangeLaw` | `HigherSpCategory.lean:103` | 🔴 L3 概念特征 | **不消除**，已由偏差代数定理覆盖 |
| `spectral_gap_estimate` | `DeviationBound.lean:386` | 🟡 L2 待 Mathlib | 监视 `Matrix.Spectrum` 进展 |
| `deviation_spectral_bound` | `DeviationBound.lean:412` | 🟡 L2 依赖上者 | 自动闭合 |

### 时间线

- **短期**：路径 C 完成后，用 Python 验证结果交叉确认偏差代数形式（$\Delta$ 的 Frobenius 范数行为）的正确性
- **中期**：Mathlib `Matrix.Spectrum` 稳定后，2 个 L2 `sorry` 数小时内可补全
- **长期**：Agda 版本完成后，对比两个证明助理的实现一致性

---

## 依赖关系

```
路径 C（数天）     ← 无外部依赖，纯 Python
    ↓
路径 B（数周）     ← 需 Agda + agda-categories 环境
    ↓
路径 A（长期）     ← 依赖 Mathlib 进展 + B 的交叉验证
```

路径 C **独立可交付**，不受路径 B/A 影响。

---

## 版本记录

| 版本 | 日期 | 变更 |
|:-----|:----:|:-----|
| v0.1 | 2026-07-30 | 初版创建。三路径策略：C（Python 可执行语义）→ B（Agda 重形式化）→ A（Lean 零 sorry） |
| v0.2 | 2026-07-30 | **路径 C 完成**。`verify/` 模块 8/8 PASS，注册 `run_all_tests.py`。文档更新状态为 ✅ |
| v0.3 | 2026-07-30 | **向外推形式化完成**。`CoherenceToBranching.lean §11` 新增 `dimension_gap` + `outward_proof_maps_to_orthogonal_layer`。Lean 模块数：74 → 74（内容扩展，未新增模块）。文档更新为 ✅ |
| v0.4 | 2026-07-31 | **路径 B 完成**。`agda_formalization/` 核心 8 模块（B1-B8）全部通过 Agda 2.8.0 类型检查，`Everything.agda` 整体编译通过。双实现一致性要点记录于 §路径 B 状态 |
| v0.5 | 2026-07-31 | **路径 B 闭合路线图立项**（用户决议：签名镜像不构成第二条验证路径，必须完整闭合）。登记 T1/T2/T3 闭合账目（47 个 postulate 块的可闭合项）。T1 首批 3 项闭合中 |
| v0.6 | 2026-07-31 | **T2 关键基石闭合**：`*mat-assoc`（矩阵乘法结合律，`sumFin` 代数引理链）、`zeroMat-absorb-l/r`；`SpHom.intertwine` 升级为真实等式 `P·A_Y = A_X·P`，`compose-intertwine`/`unit-intertwine` 真实闭合，DecursionFunctor 零矩阵态射交织闭合（`D-map-intertwine` 登记 postulate） |
| v0.7 | 2026-07-31 | **T2 继续闭合**：B2 `spHorizComp`/`spThreeHorizComp` 具体同伦构造；B5 `layer1-condition` 经 `-mat-elim`（新增 `cong-app`）闭合；`layer2/3-condition` 待 condition 字段真实化 |
| v0.8 | 2026-07-31 | **T2 condition 真实化**：交换子代数引理库（`commutator`/`neg-add`/`cancel-mid`/`*mat-distrib`/`commutator-add` 等）；`SpTwoMorphism`/`SpThreeMorphism` condition 升级为真实交换子等式，`id/spVertComp/id3/spThreeVertComp` 条件闭合；`layer2/3-condition` 闭合；结合律经 UIP 保持；水平复合 condition 登记 postulate |
| v0.9 | 2026-07-31 | **T2 继续闭合**：B3 `adjUnit` 构造为常函数同态、`left-triangle` refl 闭合；`right-triangle` 登记待闭合（依赖 R-map） |
| v0.10 | 2026-07-31 | **T2 收官（结构代数部分）**：B2 水平复合 condition 闭合（`spHorizComp-condition`/`spThreeHorizComp-condition`，交换子代数引理链含 `neg-mul-l/r`/`horiz-cross-scalar`/`*mat-distrib-l/r-minus`/`horiz-cross` + 单侧同余引理）；T2 仅剩 `right-triangle`（依赖 R-map）与 `D-map-intertwine`（依赖 transferMatrix 语义）两项语义构造 |
| v0.11 | 2026-07-31 | **T2 语义构造闭合**：`transferMatrix` 具体化（对应 Lean `fun i j => if f i = j then 1 else 0`）+ `transferMatrix-comp` 闭合；`D-map-intertwine` 经 `transferMatrix-comp` + `RecHom.comm` 闭合（对应 Lean `DFunctor_map`）；`right-triangle` 保持登记（Lean 侧 R-map 恒等隐式要求 nS = nT，Agda 泛化下不可构造，维度约束差异） |
| v0.12 | 2026-07-31 | **论文推导审计**：校验显示 Lean 侧 `DAdjR` 恒等/单位矩阵构造隐含 nS=nT + S.A=单位矩阵两个未声明条件，非论文构造的忠实实现；论文层已用显式构造修复原文 Freyd 循环（构造 C2.2/R11，演化映射 e^{-A_E}，仅 D 的像子范畴上严格，定理 2.4.5）；`right-triangle` 对齐论文 R11 登记为 T3 依赖项（有限维化需 exp）；两侧统一标注原型限制 |
| v0.13 | 2026-07-31 | **双路线推进**：(1) Lean 侧 `lake env lean` 验证 DAdjR 编译失败（nS=nT/step=id/S.A=单位阵三处），Adjunction.lean 加审计注释，正确路径指向 RAP5a；(2) Agda 侧 R11 有限维化：SpImD 子范畴（SpIso/DR-iso/adjUnit-img/adjCounit-img），`left-triangle-img` 闭合，右三角登记（依赖 D 的 full 性，对应 RAP5a RIm_map 开放项） |
| v0.14 | 2026-07-31 | **Lean 编译修复 + Agda D 忠实性实现**：Adjunction.lean 恢复编译（RFunctor.map/adjUnit/adjCounit/DAdjR 以 sorry 占位登记——泛化不可构造为结构性数学障碍（Fin m → Fin n 在 m>0=n 时为空类型），非可修复错误）；Agda 新增 `transferMatrix-inj`（`Fin-eq?-refl/true` + `if-c1` 引理链，对应 Lean `transferMatrix_injective`，D 忠实性基础） |
| v0.15 | 2026-07-31 | **S0 表示静默分析与推进方向记录**：SpImD 态射层不可闭合定性为表示静默（S0 层，静默体系四层 → 五层），分析入笔记 `notes/00_foundations/spectral_representation_silence.md`（§9 后续影响：理论核心层/静默理论层/形式化层 + P0-P4 推进方向 + P1 决定性判断）；路线图新增 §后续影响与推进方向，闭合账目 SpImD 态射层条目关联 S0 静默，P1（R11 无限维态射层验证）并入 T3 |
| v0.16 | 2026-07-31 | **P4 Agda 侧收官（鸽笼 + 无双射）**：Cardinality.agda §5 鸽笼 `fun2-no-5`（5 个互异 F2→F2 函数不可能，`分类` 枚举排除树，修复模式变量与 ℂ 构造子 c2 冲突改名 q1..q4）+ §6 无双射 `no-bijection`（Equiv (SpHom (D-obj trivial2) (D-obj trivial2)) (F2 → F2) → ⊥，5 互异 SpHom + 双射单射 + 鸽笼；新增 Set₁ 工具 `_≢₁_`/`congL1`/`sym₁`/`trans₁`）。设计说明：Agda 计数落在函数层（RecHom-≡ 需依赖版 funext，库仅非依赖公理，经 rec-hom-card 关联）；Lean 侧为 Hom_Sp 不可数 vs Hom_Rec 有限。Everything.agda 整体编译通过，无新增 postulate |
| v0.17 | 2026-07-31 | **P1 理论分析完成（语义分岔判定）**：新笔记 `notes/00_foundations/spectral_R11_morphism_layer.md`——谱匹配双射真值取决于 Rec 态射语义：线性语义下恒等双射（M_Sp = M_σ = M_Rec，谱测度输送引理 + exp 单射引理），伴随无限维闭合；集合语义（框架 RecHom 原始语义）下非线性谱匹配映射破坏双射，S0 静默升级为结构性现象。推荐采用线性语义作闭合路径，构成 P0 之后第二项论文层限定。形式化依赖 T3（Fuglede 定理/exp-log 函数演算/Hille-Yosida） |
| v0.18 | 2026-07-31 | **P1 论文层限定修正**：paper1 新增注 C2.3b（态射对应语义限定：谱匹配双射隐含线性语义，集合语义下不成立）并更新注 2.4.5a（无限维闭合声明注明"受限态射层 = 线性连续谱匹配映射"，引用 P1 笔记）；表示静默笔记 §7/§8 同步登记 |
| v0.19 | 2026-07-31 | **P1 深化（数值验证 + 反例修正）**：新脚本 `paperX_spectral_matching.py`（7/7 PASS，注册 run_all_tests.py）验证谱匹配三条件等价（交织/谱匹配/exp 交换解空间一致、闭式 dim=Σm_E·m_S、谱不相交⟹{0}、非线性元、重数块结构）；**命题 6 反例修正**：ψ=|z|z 齐次度 2 错误 → ψ=|z|（正齐次）；P1 笔记 v0.2（引理 1 完整论证：Cayley 变换 + Fuglede + 谱测度输送） |
| v0.20 | 2026-07-31 | **P2 遗留项解析完成（S0 静默理论结构收官）**：新脚本 `paperX_s0_analytic.py`（6/6 PASS，注册 run_all_tests.py）——遗留 1：S_D(ψφ)=1-√U 解析分布（ψ 复高斯，中位数 1-√(1/2)≈0.2929 解释 §10.2 的 0.294，均值 1/3，σ=√(1/18)）；遗留 2：非平凡动力学 e^{-tA}（A=diag(1,2)）演化 S_D(t)=1-|e^{-t}-e^{-2t}|/√(2(e^{-2t}+e^{-4t})) 从 1 降至 1-1/√2——非平凡动力学破坏 S0 静默；swap 系统 Hom_Sp⊆Im(D) ⟹ S0 静默={0}（结构依赖）；遗留 3：Im(D) 张成=行和相等空间 ⟹ dim S_D=n-1 闭式（n=2..7 验证）。P2 状态更新为 ✅；表示静默笔记 §10.4 更新 |
| v0.21 | 2026-07-31 | **T3 实分析基础立项（持续主线启动）**：新蓝图笔记 `notes/00_foundations/spectral_T3_analysis_foundation.md`——闭合项盘点（B4 不等式链 / B7 静默分离+Moran / B8 收缩率排序 / P1 谱匹配）、引理依赖图（ℝ 完备性→级数→exp→log→rpow）、建设阶段 0-5、最小公理集方案（关键判断：65/24<e<3 仅需有限部分和+几何上界，为最轻切入点）。**阶段 0 完成**：DHStructuralAnalysis.agda 补充 ℝ 序代数公理（0<1、加法单调、乘正性、≤-混合传递，登记为基础假设），Everything.agda 编译通过 |
| v0.22 | 2026-07-31 | **T3 阶段 1 完成（部分和基础）**：DHStructuralAnalysis.agda 补充 ℝ 域公理（+/* 结合交换分配、0/1 单位、逆、natℝ 同态、保序嵌入、除法正性、加正增量，登记为基础假设）+ `factorial`/`recip-factorial`/`partial-e` 定义 + `recip-factorial-pos`（0<1/n!）/`partial-e-suc`（部分和严格递增）可证明引理（factorial-pos 经 case+等式传递，本地 subst）。Everything.agda 编译通过。蓝图阶段 1 标记 ✅；阶段 2（65/24<e<3）待推进 |
| v0.23 | 2026-07-31 | **T3 阶段 2 机制就位**：DHStructuralAnalysis.agda 登记 `/-add-ℝ`（分数加法法则）、`/-cross-ℝ`（交叉相乘消去）与 `exp-partial-<`（exp 级数截断：部分和 < exp 1，定义性公理，对应 Lean exp 级数）——65/24<e 的闭合机制齐备。Everything.agda 编译通过。蓝图阶段 2 标记 🔄（机制就位）；剩余 `partial-e 4 ≡ 65/24` 通分计算证明（需 natℝ 具体值展开）为下一步 |
| v0.24 | 2026-07-31 | **T3 阶段 0-2 成果补录研究笔记**：蓝图笔记 `spectral_T3_analysis_foundation.md` 升 v0.2，§5 记录已执行阶段完整成果——阶段 0（ℝ 序公理 5 条）、阶段 1（ℝ 域公理 13 条 + factorial/recip-factorial/partial-e 定义 + factorial-pos/recip-factorial-pos/partial-e-suc 可证明引理）、阶段 2（/-add-ℝ、/-cross-ℝ、exp-partial-< 闭合机制 + 闭合链 65/24<e ⟸ partial-e 4 ≡ 65/24 + exp-partial-< 4） |
| v0.25 | 2026-07-31 | **T3 首个实质闭合：`sixtyfive-over-24-lt-e`**：`partial-e-4-value` 通分计算证明（/-add-ℝ 逐步 2/1→5/2→32/12→780/288 + /-cross-ℝ 交叉相乘 780·24=65·288；natℝ-*/-+ 的 ℕ 层定义性化简，无需展开 natℝ 具体值）+ `exp-partial-< 4` 级数截断公理 ⟹ 65/24 < e 闭合（对应 Lean Real.exp_one_gt_d9），不再是 postulate。蓝图阶段 2 更新（65/24<e ✅，e<3 待几何级数上界）；B4 不等式链 3 项剩 2 项（ln15-lt-65-24、e-lt-3） |
| v0.26 | 2026-07-31 | **T3 完备性层建立（阶段 3 启动）**：DHStructuralAnalysis.agda 登记完备性公理（sup-ℝ/upper/least）+ exp 上确界（exp-partial-≤-ub：exp 1 是部分和上界；exp-least-ub：exp 1 是最小上界，级数定义）——T3 完备性假设就位（蓝图 §4/§5.4）。e < 3 闭合链明确：几何上界（ℕ 层 factorial-2^，待）+ exp-least-ub + e-def。Everything.agda 编译通过 |
| v0.27 | 2026-07-31 | **T3 ℕ 层几何上界完成（e < 3 组件）**：DHStructuralAnalysis.agda 新增保序引理库（s<s-inj、+ℕ-<-mono-l/r、+ℕ-<-mono、*ℕ-<-mono-l/r、2-lt-4m）+ `factorial-2^`（2^{k-1} <ℕ k!，k≥3，经 *ℕ-<-mono-l/r + 归纳）——e < 3 的关键 ℕ 层组件可证明。Everything.agda 编译通过。蓝图 §5.4 更新（factorial-2^ ✅）；剩余 ℝ 层：1/k! < 1/2^{k-1}（倒数单调）+ 几何和 < 1 + partial-e n < 3 |
| v0.28 | 2026-07-31 | **T3 ℝ 层几何上界完成（e < 3 组件）**：DHStructuralAnalysis.agda 新增 `recip-mono-ℝ`（倒数单调公理：0<a<b ⟹ 1/b < 1/a，登记为基础假设）+ `2^-pos`（0 <ℕ 2^n，归纳 + 带模式匹配修复）+ `recip-half`（1/2^n 定义）+ `recip-factorial-<-half`（1/k! < 1/2^{k-1}，k=3+m：factorial-2^ → natℝ-<-embed → recip-mono-ℝ，natℝ-pos-embed 保证分母正性）——e < 3 的 ℝ 层组件闭合。Everything.agda 编译通过。蓝图 §5.4 更新（recip-factorial-<-half ✅）；剩余：几何和 < 1（Σ_{k≥2} 1/2^{k-1}）+ partial-e n < 3 组合 |
| v0.29 | 2026-07-31 | **T3 e < 3 闭合（B4 不等式链倒数第二项）**：DHStructuralAnalysis.agda `e-lt-3` 由 postulate 转为定理——**统一上界策略**（sup 层严格性要求固定间隙：`partial-e n < 3` 只给 `exp 1 ≤ 3`，故改用 `partial-e n < 67/24 < 3`）：新增基础假设 5 条（`*-/ℝ`、`div-one-ℝ`、`lt-+-mono-r-ℝ`、`/-lt-same-den-ℝ`、`<-≤-ℝ`）+ 可证明引理链 `factorial-2^-4`（2^k<k!，k≥4）→ `recip-factorial-<-half4` → `dbl-recip`（2·2^{-(n+1)}=2^{-n}）→ `geo4-ident`（Σ_{k=4}^{4+m}1/2^k + 1/2^{4+m} = 1/8 闭式）→ `tail-e4-lt-geo4` 逐项比较 → `partial-e-decomp`/`partial-e-3-value`（8/3 通分）→ `partial-e-lt-67-24` → `sixtyseven-over-24-lt-3` → e-lt-3（exp-least-ub + 67/24<3）。Everything.agda 编译通过。蓝图 §5.4/§6 更新（阶段 2 ✅）；B4 剩 `ln15-lt-65-24` 一项 |
| v0.30 | 2026-07-31 | **T3 ln15 < 65/24 闭合（B4 不等式链收官）**：DHStructuralAnalysis.agda `ln15-lt-65-24` 由 postulate 转为定理——ln15 = 4ln2 + ln(15/16)（`log-mul`/`log-one`/`log-16`/`log-recip` 全为可证明定理，由定义性公理 exp-add/log-exp/exp-log/exp-zero 推出）；级数截断（`ln2-lt`：ln2 < 0.69317 = Σ1/(k·2^k) 截断；`ln1615-lb`：ln(1+1/15) > 29/450 = u-u²/2）；**关键设计决策**：65/24 与 ln15 相对间隙 ~1e-4，有理比较需分母 ~1e5，`_*ℕ_` 归一化 1e9-1e11 交叉乘积致 Agda 挂起（实测），故纯有理比较 `ln15-arith-ax`（4·0.69317 - 29/450 ≈ 2.7082356 < 65/24 ≈ 2.7083333）按 scoped 公理登记，log 代数部分全部可证。Everything.agda 编译通过。蓝图 §3 阶段 3 部分闭合 / §5.5 新节 / §6 更新；**B4 不等式链 ln 15 < 65/24 < e < 3 三项全部闭合** |
| v0.31 | 2026-07-31 | **公理纪律收紧（对齐审计）**：`neg-unique-ℝ`（经 +-assoc/comm/ident/inv）与 `lt-+-mono-l-ℝ`（经 lt-+-mono-r-ℝ + +-comm-ℝ）改为**可证明定理**，删除对应 postulate——基础假设净剩 3 条（`*-pos-mono-ℝ`/`*-/cancel-ℝ`/`neg-<-ℝ`，均为标准有序域定理，模型必然性由"ℝ 是有序域"保证，且与现公理集独立）；`ln2-lt`/`ln1615-lb`/`ln15-arith-ax` 在闭合账目登记为**阶段 3 开放项**（前两者为 log 级数内容=定义性公理待实现；`ln15-arith-ax` 为纯有理比较，归**资源/实践静默**——非 S0 结构性，标准分析可验证，需算术决策机制闭合）。Everything.agda 编译通过。蓝图 §5.5 更新（对齐纪律 + 模型必然性 + 开放项归类） |
| v0.32 | 2026-07-31 | **T3 阶段 4 首批（B7 收缩率/解形式/静默分离）**：DHStructuralAnalysis.agda 新增定义性公理 `exp-pos`/`exp-mono`（蓝图 §4 exp 正性/单调）+ 基础假设 `neg-one-ℝ-def`（neg-oneℝ 定义）/`*-zero-ℝ`（零吸收）+ 可证取负引理（`neg-zero`/`neg-neg`/`neg-one-lt-zero`）；CoherenceToBranching.agda 四项由 postulate 转定理——`r-uniform-pos`（exp-pos）、`r-uniform-lt-one`（exp-mono -1<0 + exp-zero）、`ln15-solution-form`（log(1/(e⁻¹)) = 1 经 log-recip+log-exp+neg-neg，log 15/1 = log 15）、`silence-separation`（e⁻³<1 经 exp-mono + *-pos-mono + *-zero，乘 e⁻ᵈ>0 保序）。`silence-margin`（S₄/c₁ = e³）登记待闭合（需 exp-商结构 + 除法消去）。Everything.agda 编译通过。蓝图 §3 阶段 3/4 / §5.6 新节 / §6；路线图账目 B7 行更新 |
| v0.33 | 2026-07-31 | **T3 阶段 4 后半（silence-margin + B8 首批）**：DHStructuralAnalysis.agda 新增可证引理 `one-mul-ℝ`/`*-zero-l-ℝ`/`zero-add-ℝ`/`neg-one-mul`（(-1)·x=-x，经分配律+neg-unique）；CoherenceToBranching.agda `silence-margin` 闭合（a/(b·a)=1/b [/-cross+comm+one-mul]，1/e⁻³=e³ [exp-add+neg-one-mul+exp-zero]）；IFSFractal.agda B8 首批闭合——`c1/c2-physical-pos`（exp-pos）、`c1/c2-physical-lt-one`（exp-mono+取负+≤-pos）、`c1-lt-c2-physical`（exp-mono+-(3+d)<-d）、`exp-neg-one-lt-37-100`（e⁻¹=1/e<37/100 ⟸ 100/37<65/24<e，公共分母 888 + 交叉 2400<2405）。Everything.agda 编译通过。蓝图 §3 阶段 4 / §5.6 扩充；路线图账目 B7/B8 行更新。**待**：Moran 方程族、B8 c₂<c₃ 组（rpow 单调 + 定量估计，阶段 4 后半/5）、P1 形式化（阶段 5） |
| v0.34 | 2026-07-31 | **T3 Moran 首项（dH-from-branching）**：DHStructuralAnalysis.agda 新增定义性公理 `rpow-exp`（a^b = e^{b·ln a}，蓝图 §4 rpow 内容）+ 可证引理 `exp-recip`（e^{-x} = 1/e^x，经 exp-add + 加性逆）；`dH-from-branching`（15·(e⁻¹)^{ln15} = 1）由 postulate 转定理——(e⁻¹)^{ln15} = e^{ln15·log(e⁻¹)} [rpow-exp] = e^{-ln15} [log(e⁻¹) = -1 经 log-exp + neg-one-ℝ-def；ln15·(-1) = -ln15 经 neg-one-mul] = 1/15 [exp-recip + exp-log]，15·(1/15) = 1 [*-/cancel-ℝ]。Everything.agda 编译通过。蓝图 §3 阶段 4 / §5.6；路线图账目 Moran 行拆分。**待**：`moran-solution-iff`/`dH-moran-solution-unique`/`glued-recursion-*`（需 exp 单射/三分律）、B8 c₂<c₃ 组、P1 形式化 |
| v0.35 | 2026-07-31 | **T3 Moran 解唯一 + 解存在（moran-solution-iff 族收官）**：DHStructuralAnalysis.agda 新增定义性公理 `exp-inj`（exp 单射，记入账目开放项）+ 可证引理 `*-recip-impl`（a·b=1⟹b=1/a）、`*-div-impl`（a·b=c⟹a=c/b）、`neg-mul-ℝ`（(-x)·y=-(x·y)，经分配律+neg-unique）；`dH-moran-solution-unique`（e^{-x}=1/15=e^{-ln15} ⟹ -x=-ln15 [exp-inj] ⟹ x=ln15 [neg-neg]）与 `moran-solution-iff`（B·r^x=1 ⟹ x·log r=-log B [log-exp+log-recip] ⟹ x=(-log B)/log r [*-div-impl] = log B/log(1/r) [neg-mul-ℝ + log-recip]）由 postulate 转定理。Everything.agda 编译通过。蓝图 §3 阶段 4 / §5.6；路线图账目 Moran 行拆分。**待**：`glued-recursion-*`（二次方程 + 正根选择）、B8 c₂<c₃ 组、P1 形式化 |
| v0.36 | 2026-07-31 | **T3 §5 唯象不等式闭合（d_H 拟合值夹逼 + 完整链）**：DHStructuralAnalysis.agda `partial-e-5-value`（partial-e 5 = 163/60：通分 65/24 + 1/120 = 7824/2880 [/-add-ℝ 分子在前] + 交叉相乘 7824·60=163·2880）、`sixtyfive-over-24-lt-dH`（65/24 < 27095/10000，公共分母 6000 + 中间步 5419/2000 控制规模）、`dH-lt-e`（27095/10000 < e：27100/10000 < 813/300 < 815/300 = partial-e 5 < e，subst 作用于左侧谓词 + `trans-<ℝ` 传递）由 postulate 转定理，`inequality-chain-full`（ln15 < 65/24 < d_H < e < 3 四元组）闭合。修复过程：`/-add-ℝ` 参数顺序、`b815` 重写方向、`trans`→`trans-<ℝ`。Everything.agda 编译通过。蓝图 §3 阶段 4 / §5.7 / §6；路线图账目新增 B4 唯象不等式行。**待**：`glued-recursion-*`、B8 c₂<c₃ 组、P1 形式化 |
| v0.37 | 2026-07-31 | **T3 B8 `moran-3map-holds` 闭合（rpow 幂合成）**：IFSFractal.agda `moran-3map-holds`（c₁^d+c₂^d+c₃^d=1）由 postulate 转定理——新增基础假设 1 条 `sub-ℝ-def`（减法定义 x-y=x+(-y)，标准有序域事实）+ 可证引理 `rpow-pow`（(a^b)^c=a^(b·c)，rpow-exp 展开 + *-assoc/comm + log-exp，**零新增公理**）、`rpow-one`（a^1=a）、`swap-pair`/`add-neg-cancel`/`cancel-sub`（(x+y)+((z-x)-y)=z）；闭合链 c₃^d=((1-c₁^d)-c₂^d)^((1/d)·d)=(1-c₁^d)-c₂^d + cancel-sub。Everything.agda 编译通过。蓝图 §3 阶段 4 / §5.8 / §6；路线图账目 B8 行拆分。**待**：`glued-recursion-*`、B8 c₃ 组其余项（c₃ 正性/排序 + two-exp-add-exp-lt-one 定量估计）、P1 形式化 |
| v0.38 | 2026-07-31 | **T3 B8 `two-exp-add-exp-lt-one` 闭合（exp 定量枢纽）**：IFSFractal.agda `two-exp-add-exp-lt-one`（2e^{-d²}+e^{-d(3+d)}<1，d≥1）由 postulate 转定理——新增基础假设 4 条（`≤-trans-ℝ`/`*-≤-mono-ℝ`/`neg-≤-ℝ`/`≤-+-mono-ℝ`，全序域标准事实）+ 定义性公理 `exp-mono-≤`（exp ≤ 单调）+ 可证引理链 `d-sq-ge-1`/`d-3d-ge-4`（d²≥1、d(3+d)≥4）、`partial-e-1-value`/`e-gt-2`/`e2-gt-4`/`e3-gt-8`/`e4-gt-16`（e>2 ⟹ eⁿ 幂界）、`exp-nat2`/`exp-nat4`（exp(natℝ n)=eⁿ）、`exp-neg-4-lt-1-8`（e⁻⁴<1/8，倒数单调）、`one-8-lt-13-100`、`exp-neg-d2/d3d-lt-*`、`/-add-same-ℝ`（同分母加法）；`exp-neg-one-lt-37-100` 从 IFSFractal 迁入 DHStructural（依赖 B4 链，避免前向引用）。闭合链 2e^{-d²}<74/100 + e^{-d(3+d)}<13/100 ⟹ 和<87/100<1。数值规模控制：13/100 界（交叉 100<104）替代 1/16 长链。Everything.agda 编译通过。蓝图 §3 阶段 4 / §5.9 / §6；路线图账目 B8 行更新。**待**：B8 c₃ 组其余项（c₃ 正性/排序依赖 two-exp + rpow 单调）、`glued-recursion-*`、P1 形式化 |
| v0.39 | 2026-07-31 | **T3 B8 c₃ 底数正性与正性（one-sub + c3-pos）**：IFSFractal.agda `one-sub-c1d-c2d-pos`（c₁^d+c₂^d<1 ⟺ 0<(1-c₁^d)-c₂^d）与 `c3-physical-pos`（0<c₃）由 postulate 转定理——新增定义性公理 `rpow-mono-ℝ`（蓝图 §4 rpow 单调内容）+ 可证引理 `rpow-pos`（0<a⟹0<a^b）、`rpow-one-base`（1^b=1）、`one-lt-2-ℝ`、`zero-sum`、`pos-sub`（x+y<1⟹0<(1-x)-y）、`sub-lt`/`sub-one-lt`（DHStructural）+ `c1d-exp`/`c2d-exp`（c₁^d=e^{-d(3+d)}、c₂^d=e^{-d²}，rpow-exp 展开，IFSFractal）。one-sub 闭合链：e₁+e₂<e₁+2e₂<1 [two-exp] + pos-sub；c3-pos：one-sub + rpow-pos。Everything.agda 编译通过。蓝图 §3 阶段 4 / §5.10 / §6；路线图账目 B8 c₃ 行更新。**待**：B8 排序（`c-physical-strictly-ordered` c₂<c₃ 需 rpow 单调逆）、`glued-recursion-*`、P1 形式化 |
| v0.40 | 2026-07-31 | **T3 B8 排序闭合（O2 统一性定理收官，阶段 4 完成）**：IFSFractal.agda `c-physical-strictly-ordered`（c₁<c₂<c₃）与 `physicalIFS-ratios-ordered` 由 postulate 转定理——新增定义性公理 `rpow-mono-inv-ℝ`（a^c<b^c ⟹ a<b，严格单调 ⟹ 单射）+ 可证引理 `two-mul-add`（2x=x+x）、`sub-elim`（a+b<c ⟹ a<c-b，移项）（DHStructural）+ `c3d-base`（c₃^d=(1-c₁^d)-c₂^d，全局化）、`c2-lt-c3-physical`（IFSFractal）。c₂<c₃ 链：two-exp（2e₂+e₁<1）⟹ sub-elim 移项 ⟹ e₂<(1-e₁)-e₂ ⟹ 替换 e₁→c₁^d、e₂→c₂^d ⟹ c₂^d<c₃^d ⟹ rpow-mono-inv-ℝ ⟹ c₂<c₃。**B8 全部闭合**（B4/B7/B8 齐），阶段 4 仅剩 `glued-recursion-*`。Everything.agda 编译通过。蓝图 §3 阶段 4 / §5.11 / §6；路线图账目 B8 行更新。**待**：`glued-recursion-*`（二次方程 + 正根选择）、P1 形式化 |
| v0.41 | 2026-08-01 | **T3 阶段 4 收官：glued-recursion-* 闭合（无剩余 postulate）**：DHStructuralAnalysis.agda `glued-recursion-fixed-point`（通用版：ρ∈[0,1]，(1-ρ)·r^d+(B(B-1)+ρB)·r^{2d}=1 ⟹ d=log B/log(1/r)）与 `glued-recursion-dH-eq-ln15`（B=15、r=e⁻¹ ⟹ d=ln15）由 postulate 转定理——新增定义性公理 3 条（`trichotomy-ℝ` 三分律/`zero-factor-ℝ` 域无零因子/`irreflexive-ℝ` 严格序反自反，标准全序域内容）+ 可证引理 `eq-sub-zero`/`sub-eq-zero`/`lt-sub-pos`/`rpow-2d-sq`/`glued-M-pos`/`neg-add-ℝ`/`B-sub-C`/`mul-sub-add`/`sub-mul-distrib`/`add-sub-assoc`/`BC-replace`/`factor-glued`（因式分解 (Bx-1)(x(B-1+ρ)+1)=A·x²+(1-ρ)x-1）。闭合链：x=r^d [rpow-2d-sq] ⟹ (1-ρ)x+A·x²=1 ⟹ factor-glued ⟹ (Bx-1)·M=0 ⟹ glued-M-pos（M>0）⟹ zero-factor-ℝ（M=0 分支经 irreflexive-ℝ 排除）⟹ Bx=1 ⟹ moran-solution-iff；特化 log(1/(e⁻¹))=1 [log-recip+log-exp+neg-neg] ⟹ d=ln15。修复：`log-1-over-r` 的 subst 方向（neg-one-ℝ-def 需 sym）。**T3 阶段 4 全部闭合**；蓝图 §3 阶段 4 / §5.12 / §6；路线图账目 glued-recursion 行 + B7 Moran 遗留行更新。**待**：阶段 5 P1 形式化（Fuglede/谱测度输送，线性语义） |
| v0.42 | 2026-08-01 | **Agda 环境迁移永久目录 + 阶段 5 启动（P1 有限维特例闭合）**：(1) **环境迁移**——Agda 工具链自 `%LOCALAPPDATA%\Temp` 迁入永久目录（cabal 数据 → `%LOCALAPPDATA%\cabal`，Temp 原位置 junction 保内嵌绝对路径，exe → `%USERPROFILE%\.local\bin` 已在 PATH），`--ignore-interfaces` 全量重编译 12 模块通过；重建指南入 `agda_formalization/AGDA_ENV.md`。(2) **P1 有限维特例**——新模块 `P1Spectral/P1Spectral.agda`：定理 3 退化版 M_Sp = M_σ = M_Rec（算子代数公理 + 有限谱表示 + 谱匹配⟹交织/exp交换**可证** `proj-comm-scalar-sum`，谱定理方向 `intertwine-imp-proj`/`intertwine-exp-imp-proj` 登记定义性公理），`theorem3` 四方向组合，Everything.agda 编译通过（13 模块）。**教训**：Agda 嵌套块注释中 `e^{-A}` 的 `{-` 序列开启嵌套注释（"Unterminated '{-'"），改写为 `e^(-A)`。蓝图 §3 阶段 5 🔄 / §5.13 / §6；路线图 P1 行更新。**待**：P1 无限维形式化（T3 谱定理层） |
| v0.43 | 2026-08-01 | **账目开放项闭合：`exp-inj`（exp 单射）**：DHStructuralAnalysis.agda `exp-inj` 由定义性公理转为**可证明定理**——trichotomy-ℝ 三分律 + exp-mono（严格单调）+ irreflexive-ℝ（两严格分支 x<y/y<x 分别经 h/sym h 得 exp y<exp y / exp x<exp x 矛盾）⟹ x=y，**零新增公理**。postulate 块删除，定义置于 irreflexive-ℝ 之后（依赖其声明，前向引用处理）。Everything.agda 全量编译通过（13 模块）。P1Spectral §6 注释补充推论 4 说明（恒等双射互逆往返一致性依赖谱分解与谱定理方向间的一致性公理，留待谱定理层登记）。蓝图 §5.13 更新；路线图账目新增 exp-inj 行 + Moran 解唯一行注释更新。**剩余开放项**：`ln2-lt`/`ln1615-lb`/`ln15-arith-ax`（log 级数机制） |
| v0.44 | 2026-08-01 | **P1 有限维特例完整收官（推论 4 恒等双射）**：P1Spectral.agda 追加 §7——登记互逆往返一致性公理 4 条（`σ→Sp∘Sp→σ`/`Sp→σ∘σ→Sp`/`σ→Rec∘Rec→σ`/`Rec→σ∘σ→Rec`，谱分解与谱定理方向间往返一致性，有限维由"Eᵢ 是 A 的插值多项式"可证，谱定理层完整实现时降为定理）；构造 Hom-Sp/Hom-σ/Hom-Rec 集合（record：op + prop）与恒等双射 `_≅_`（to/from/to∘from/from∘to）`Sp≅σ`/`Rec≅σ`，`corollary4 : (Hom-Sp ≅ Hom-σ) × (Hom-Rec ≅ Hom-σ)`——P1 笔记推论 4 的 Agda 对应物（Hom 两边都是 M_σ，双射 = 恒等）。Everything.agda 全量编译通过（13 模块）。蓝图 §3 阶段 5 / §5.13 更新；路线图 P1 行更新。**待**：P1 无限维形式化（T3 谱定理层） |
| v0.45 | 2026-08-01 | **T3 谱定理层立项 + 首轮完成（阶段 6）**：新模块 `SpectralTheory/SpectralTheory.agda`（14 模块编译通过）——(1) 谱论基础公理：Borel 集 = ℝ 谓词（Set₁）、谱测度 `E`/谱支集 `E-support-pos`/谱表示 `spectral-rep-A`/谱积分线性 `X-comm-spectral-int`/Fuglede `intertwine-imp-spectral`/谱测度复合 `exp-spectral-measure`/谱测度外延 `spectral-ext`/Hille-Yosida（`semigroup`/`exp-tA-zero`/`exp-tA-one`）/函数演算 `fc`（`fc-id`/`fc-ext`）。(2) **引理 2 核心可证**：`phi-inj`（φ 单射，exp-inj 闭合 + neg-neg）、`φ-image-roundtrip`（谱测度输送往返）、`E-phi-image`、`Rec-to-σ`（M_Rec ⊆ M_σ：Fuglede 对 e^(-A) → 谱测度复合 → spectral-ext 回 P）、`σ-to-Sp`/`σ-to-Rec`（谱积分线性 + 谱表示重写）。(3) 定理 3 无限维版（theorem3）+ 推论 5（`neg-log-phi-id`/`corollary5` 对象重建）。公理纪律：谱论基础登记公理（注明降定理路径），核心定理真实证明无占位。蓝图 §3 阶段 6 / §5.14；路线图账目新增阶段 6 行。**待**：谱积分细化降公理、Hille-Yosida 完整层、Fuglede 引理 1 证明、P1 无限维组装 |
| v0.46 | 2026-08-01 | **P1 无限维组装完成（SpectralTheory §6）**：corollary4-∞——`Hom-Sp ≅ₗ Hom-σ ×₁ Hom-Rec ≅ₗ Hom-σ`（恒等双射，level 多态 `_≅ₗ_` 容纳 Hom-Sp : Set 与 Hom-σ : Set₁；level 多态 `cong₁`；登记互逆往返一致性公理 4 条，谱表示与谱积分线性间往返，降定理路径注明）。**Lean 侧参考检查**：无谱论实现（OperatorTheory.lean `SpectralMeasure` 为 Phase 16B 占位、`spectralMappingExp` 为 trivial；RAP5a 仅 P4 基数反例 + P1 分析注释）——自给自足。Everything.agda 全量编译通过（14 模块）。蓝图 §5.14 阶段 6 状态更新；路线图 P1 行更新。**待**：谱积分理论细化降公理、Hille-Yosida 完整层、Fuglede 引理 1 谱积分证明 |
| v0.47 | 2026-08-01 | **谱积分理论细化第一步（SpectralTheory §7 简单函数层）**：`sum-op`（Op 层有限求和）+ `spec-int-simple`（简单函数谱积分 ∫(Σ cᵢ·1_{Ωᵢ}) dE = Σ cᵢ·E(Ωᵢ)）+ **`simple-comm` 可证**（谱匹配 ⟹ 与简单函数谱积分交换：distribₒ + ·ₒ-comm 逐项 + 归纳，零新增公理）——X-comm-spectral-int 公理降定理路径的实质第一步（简单函数部分从公理变为定理；一般函数经测度论逼近待完备性扩展）。Everything.agda 全量编译通过（14 模块）。蓝图 §5.14 阶段 6 状态更新。**待**：① 一般函数逼近层（极限，降 X-comm-spectral-int 为定理）；② Hille-Yosida 完整层；③ Fuglede 引理 1 谱积分证明 |
