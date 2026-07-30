# Phase 60：范畴理论绝对性验证路线图

> **目标**：实现 UFPF 范畴理论层面的完全独立验证，不依赖物理实例层的实验数据。
>
> **原则**：验证对象是元公理层和结构定理层本身，而非其物理应用。实例层的"正确性"不构成对上层公理的验证。
>
> **策略**：三条路径并行，按投入产出比排序执行。

---

## 三路径总览

| 路径 | 方法 | 时间 | 验证类型 | 产出 |
|:-----|:------|:----:|:---------|:-----|
| **C** | Python 可执行范畴语义 | 数天 | 运行时自洽性 | `pip install ufpf && verify_all()` |
| **B** | Agda/Coq 独立重形式化 | 数周 | 证明助理交叉验证 | 核心 8 模块双实现一致 |
| **A** | Lean 零 `sorry` 持续闭合 | 长期 | 机器证明完备化 | 全库零 `sorry` |

---

## 路径 C：可执行范畴语义（数天，先做）

### 动机

Lean 证明虽然可靠，但门槛高（需安装 Lean + mathlib，需懂依赖类型语法）。**可执行 Python 语义**让任何人能在 10 秒内验证核心范畴公理的自洽性。

### 实现方案

在 `ufpf/` 包中新增 `ufpf/verify/` 子模块：

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

| # | 模块 | 对应 Lean | 工作量估计 |
|:-:|:-----|:----------|:----------:|
| B1 | $\mathbf{Sp}$ 4-范畴定义 | `SpCategory.lean` | 2 天 |
| B2 | 高阶态射（2-/3-态射） | `HigherSpCategory.lean` | 3 天 |
| B3 | D 函子 + 伴随 | `DecursionFunctor.lean` | 2 天 |
| B4 | $d_H$ 不等式链 | `DHStructuralAnalysis.lean` | 1 天 |
| B5 | 统一 3 定理 | `Unified3Theorem.lean` | 2 天 |
| B6 | Bott 塔 | `BottTower.lean` | 2 天 |
| B7 | 静默定理组 | `CoherenceToBranching.lean` | 3 天 |
| B8 | IFS 排序定理 | `IFSFractal.lean §6` | 1 天 |
| | **合计** | | **约 16 天** |

### 成功标准

Agda 版本的 8 个核心模块通过 `agda --safe` 编译，导出定理与 Lean 版本一致。

### 交叉验证协议

```
Lean 版本:  定理 T 的证明链 L₁ → L₂ → ... → Lₙ
Agda 版本:  定理 T 的证明链 A₁ → A₂ → ... → Aₙ

验证: 证明链长度一致，中间引理一一对应
```

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
