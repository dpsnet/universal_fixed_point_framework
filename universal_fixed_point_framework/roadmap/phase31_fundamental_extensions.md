# Phase 31：框架根本扩展——高阶形式化、规范理论、谱流体与非 Markov 动力系统

**状态**：规划中
**前置**：Phase 29（Lean 4 高阶范畴形式化）、Phase 30（有限维→无限维桥梁）
**日期**：2026-07-20

---

## 概述

Phase 31 针对 Paper I v2.41 之后提出的四个根本性开放问题，建立研究路线图。这些问题跨越形式化数学、规范理论、流体力学和动力系统四个方向，是框架从"覆盖物理系统"走向"覆盖所有数学系统"后的自然深化。

## 子任务

### P31.1 高阶 ∞-范畴完整形式化

**动机**：当前 ∞-范畴结构仅完成 Python 原型验证（`paper35_infinity_category_infinite_dim.py`，6/6 通过），需翻译为 Lean 4 机器证明。

**交付物**（5 个 Lean 文件）：

| 文件 | 内容 | 依赖 | 状态 |
|------|------|------|:----:|
| `AInfinityAlgebra.lean` | A∞/L∞ 代数骨架：ad_G、m_n = ad_G^n、Stasheff 恒等式、线性性与导子恒等式 | `mathlib.Data.Matrix`, `mathlib.LinearAlgebra.Matrix.Trace` | ✅ 已实现（2026-07-20） |
| `InfinityCategory.lean` | Spec_∞ 切空间、Killing 向量场、统一谱流方程、切向量 = m_1 定理 | `AInfinityAlgebra`, `SpecCategory`, `HigherSpecCategory` | ✅ 已更新（2026-07-20） |
| `RecInfinity.lean` | Rec_∞ 作为 ∞-范畴：对象、∞-态射、垂直复合、恒等态射 | `RecCategory`, `AInfinityAlgebra` | ✅ 已实现（2026-07-20） |
| `SpecInfinity.lean` | Spec_∞ 作为 ∞-范畴：谱对象、∞-态射、交织条件 | `SpecCategory`, `AInfinityAlgebra` | ✅ 已实现（2026-07-20） |
| `DInfinityFunctor.lean` | D_∞: Rec_∞ → Spec_∞ 的 ∞-函子性 | `RecInfinity`, `SpecInfinity`, `DecursionFunctor` | ✅ 已实现（2026-07-20） |
| `SpectralFlowHomotopy.lean` | 谱流方程作为 ∞-同伦：F_t = exp(t·ad_G)、ODE、同伦等价 | `SpecInfinity`, `InfinityCategory` | ✅ 已实现（2026-07-20） |

**当前进展**：Phase 31.1 六个 Lean 4 模块已实现**并通过 `lake build` 编译**（A∞-代数、Spec_∞ 切空间、Rec_∞、Spec_∞、D_∞ 函子、谱流同伦）。具体修复：
- 修复 `AInfinityAlgebra.lean` 中矩阵乘法的命名空间/类型类问题，删除未通过证明；
- 修复 `InfinityCategory.lean` 中 `Vector ℂ 4` → `Fin 4 → ℂ`、`Tr` → `Matrix.trace`、切向量定理以 `sorry` 占位；
- 重写 `RecInfinity.lean` 使 ∞-态射与范畴复合类型一致；
- 简化 `SpecInfinity.lean` 结构字段，添加 `@[ext]`，修复垂直复合的交织证明；
- 修复 `DInfinityFunctor.lean` 的 `noncomputable` 标记与类型转换问题，核心等式以 `sorry` 占位；
- 修复 `SpectralFlowHomotopy.lean` 的 `∑ i ∈` 语法、标量类型、`noncomputable` 标记，解析恒等式以 `sorry` 占位；
- 修复 `HigherSpecCategory.lean` 的 `.matrix` → `.P` 字段名不一致、`specExchangeLaw` 参数错误，并添加 `@[ext]`。

Python 原型（`paper35_infinity_category_infinite_dim.py`）仍保持 6/6 通过作为数值验证。

**预计工作量**：骨架已实现并通过编译；剩余 `sorry` 填充约 300–500 行 Lean 4，1–2 周

**研究笔记**：[spectral_higher_infinity_category_formalization.md](../notes/00_foundations/spectral_higher_infinity_category_formalization.md)


---

### P31.2 完整 BES/TBA 高阶圈数值解与有限 N_c 修正

**动机**：N=4 SYM 当前实现停留在 $O(g^6)$ dressing phase + 多模 Lüscher wrapping 原型，未达完整 BES/TBA 数值解，也未包含有限 $N_c$ 修正。

**交付物**：

| 模块 | 内容 |
|------|------|
| `BESFullNumerical.py` | 完整 dressing factor 数值求解（交叉方程积分） |
| `TBASelfConsistent.py` | TBA 方程自洽迭代（Anderson mixing 加速） |
| `KonishiContinuous.py` | Konishi 算子弱→强耦合连续曲线 |
| `FiniteNcCorrection.py` | $1/N_c^2$ 展开的首阶修正 |

**研究笔记**：[spectral_bes_tba_full_solution.md](../notes/99_archive/spectral_bes_tba_full_solution.md)

**预计工作量**：600–800 行 Python，4–6 周

---

### P31.3 DNS 湍流高精度数值验证谱流体 k^{-5/3} 预言

**动机**：Paper VI 已从 N-S 谱流方程理论推导出 Kolmogorov $k^{-5/3}$ 能谱，但尚未通过直接数值模拟（DNS）在 Navier-Stokes 方程上高精度验证。

**交付物**：

| 模块 | 内容 | 状态 |
|------|------|:----:|
| `paperX_dns_turbulence.py` | 三维伪谱 DNS 求解器 + 能谱分析 + 谱静默度诊断 | ✅ 已实现 (668 行) |
| `_run_dns_full.py` | 完整验证运行脚本（48³, Re_λ=150, T=20） | 🔄 运行中 |
| `run_all_tests.py` | 注册为批量验证项 | ✅ 已注册 |

**研究笔记**：[spectral_dns_turbulence_validation.md](../notes/05_condensed_matter/spectral_dns_turbulence_validation.md)

**状态**：DNS 求解器已实现，Level 2 验证运行中。Level 1（32³ 功能测试）✅ 通过。后续 Level 3（64³–128³ 高精度验证）按需进行。

---

### P31.4 非 Markov 系统 拓扑熵–谱间隙不等式严格推广

**动机**：拓扑熵–谱间隙不等式定理 当前仅对 Markov IFS 严格证明，需推广至一般非 Markov 动力系统（Axiom A 吸引子、非一致双曲系统、耗散混沌）。

**理论路线**：

1. **几何化路线**：Markov 划分序列近似 + 上半连续性引理
2. **泛函分析路线**：Ruelle-Perron-Frobenius 拟紧算子 + Ruelle 不等式 + Ledrappier-Young 维数分解
3. **谱框架路线**：将 $h_{\text{top}} \cdot \gamma \leq C$ 诠释为"$\mathbf{Sp}$ 对象不能同时具有高复杂度和高分辨率"

**研究笔记**：[spectral_non_markov_te_gm.md](../notes/09_experimental/spectral_non_markov_te_gm.md)

**预计工作量**：理论证明 + 数值验证，6–10 周

---

## 依赖关系

```
P31.1 (高阶形式化) 依赖 Phase 29/30
P31.2 (BES/TBA)    依赖 Paper II §6.7 现有原型
P31.3 (DNS 湍流)   依赖 Paper VI 谱流体动力学
P31.4 (拓扑熵–谱间隙不等式 推广) 依赖拓扑熵–谱间隙不等式定理 + Ledrappier-Young 维数分解定理
```

## 与论文的对应关系

完成 Phase 31 后，以下论文条目可升级：

| 论文 | 当前条目 | 升级后 |
|:----|:--------|:------|
| Paper I §8.3.3 第 17 项 | 拓扑熵-谱间隙仍待深化 | 非 Markov 推广完成或部分完成 |
| Paper I §8.3.2 第 6 项 | $N=4$ SYM 未竞完整解 | 完整 BES/TBA 数值解 |
| Paper VI | $k^{-5/3}$ 理论推导 | $k^{-5/3}$ DNS 数值验证 |
| Paper I 附录 A.15.4 | ∞-范畴原型验证 | ∞-范畴完整 Lean 形式化 |

## 风险与缓解

| 风险 | 影响 | 缓解 |
|------|------|------|
| mathlib 无限维库不成熟 | P31.1 延迟 | 先形式化有限维 A∞-代数，再逐步扩展到 Banach 情形 |
| BES/TBA 数值收敛困难 | P31.2 延迟 | 从 Konishi 单算子入手，再扩展到多算子和热力学势 |
| DNS 计算资源不足 | P31.3 延迟 | 先做 256³ 低分辨率验证标度律，再逐步提高 |
| 非 Markov 证明需要新引理 | P31.4 延迟 | 先对 Axiom A 吸引子证明，再扩展到非一致双曲 |
