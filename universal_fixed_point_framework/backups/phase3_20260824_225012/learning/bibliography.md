# 参考文献与资源

> 本文件为 UFPF 范畴论学习提供经典教材、在线资源和 UFPF 内部论文索引。

## 经典教材

### 入门

1. **Steve Awodey, *Category Theory***
   - 适合初学者，强调概念直觉与例子
   - 推荐章节：1-5（基础）、6-8（函子与自然变换）、9-10（伴随）

2. **Tom Leinster, *Basic Category Theory***
   - 可免费获取的精炼教材
   - 推荐章节：1-4（基础与函子）、5-6（伴随）

3. **Bartosz Milewski, *Category Theory for Programmers***
   - 以编程直觉引入范畴论
   - 适合有计算机背景的学习者

### 进阶

4. **Saunders Mac Lane, *Categories for the Working Mathematician***
   - 范畴论圣经
   - 推荐章节：I-IV（基础）、V-VI（极限）、VII（伴随）、IX（层）、XII（单子和代数）

5. **Emily Riehl, *Category Theory in Context***
   - 现代风格，丰富的例子
   - 推荐章节：1-4（基础）、5（伴随）、6（极限）、7（层和纤维）

6. **Francis Borceux, *Handbook of Categorical Algebra*（三卷）**
   - 百科全书式参考
   - 卷 1：基本范畴论；卷 2：纤维范畴与层；卷 3：topos 与高阶范畴

### 高阶范畴

7. **Emily Riehl, *Categorical Homotopy Theory***
   - 模型范畴与 ∞-范畴的桥梁

8. **Emily Riehl, *Elements of ∞-Category Theory***
   - ∞-范畴的入门教材

9. **Kenji Lefevre-Hasegawa, *Sur les A-infini catégories***
   - $A_\infty$ 范畴的经典博士论文

10. **Jim Stasheff, *H-Spaces from a Homotopy Point of View***
    - $A_\infty$ 空间的历史来源

## 在线资源

### 课程与讲义

- **The nLab**（https://ncatlab.org）
  - 范畴论、高阶范畴、topos 理论的维基百科
  - 推荐条目：category, functor, adjunction, sheaf, Grothendieck fibration, ∞-category

- **Stacks Project**（https://stacks.math.columbia.edu）
  - 代数几何中的层、topos、纤维化严格处理

- **Kerodon**（https://kerodon.net）
  - Jacob Lurie 的 ∞-范畴在线教材

### Lean 4 与 Mathlib

- **Lean 4 官方文档**（https://lean-lang.org/lean4/doc/）
- **Mathlib 文档**（https://leanprover-community.github.io/mathlib4_docs/）
  - 关键模块：
    - `Mathlib.CategoryTheory.Category.Basic`
    - `Mathlib.CategoryTheory.Functor.Basic`
    - `Mathlib.CategoryTheory.NatTrans`
    - `Mathlib.CategoryTheory.Adjunction.Basic`
    - `Mathlib.CategoryTheory.Limits`
    - `Mathlib.CategoryTheory.Monad.Basic`
    - `Mathlib.CategoryTheory.Sites.Sheaf`
    - `Mathlib.CategoryTheory.FiberedCategory`

- **Theorem Proving in Lean 4**（https://leanprover.github.io/theorem_proving_in_lean4/）

## UFPF 内部论文索引

### 基础范畴论

- [paper1_fractal_spectral_derecursion.md](../paper/paper1_fractal_spectral_derecursion.md)：$\mathbf{Rec}$, $\mathbf{Sp}$, $D \dashv R$, 自然同构
- [paper1_appendix.md](../paper/paper1_appendix.md)：Yoneda, Freyd, slice category, $C^*$ 框架
- [paper1_philosophy.md](../paper/paper1_philosophy.md)：伴随的哲学诠释

### 2-范畴与高阶

- [paper5_spectral_dynamics.md](../paper/paper5_spectral_dynamics.md)：$D_2: \mathbf{Rec}_2 \to \mathbf{Sp}_2$
- [paper2_physics_applications.md](../paper/paper2_physics_applications.md)：2-范畴严格化
- [paper9_singularity_resolution.md](../paper/paper9_singularity_resolution.md)：范畴维数与 ∞-范畴

### 层论与纤维化

- [paper16_lorentz_spectral_dynamics.md](../paper/paper16_lorentz_spectral_dynamics.md)：谱预层、层公理与广义协变性
- [paper19_category_extension.md](../paper/paper19_category_extension.md)：Temp/RG 纤维范畴
- [paper21_grothendieck_fibration_synthesis.md](../paper/paper21_grothendieck_fibration_synthesis.md)：纤维化综合
- [paper22_spectral_fibration_synthesis.md](../paper/paper22_spectral_fibration_synthesis.md)：纤维精细分解
- [paper27_leaver_spectral_sheaf.md](../paper/paper27_leaver_spectral_sheaf.md)：Leaver 谱覆盖
- [paper28_kerr_newman_coupled_sheaf.md](../paper/paper28_kerr_newman_coupled_sheaf.md)：Kerr-Newman 耦合谱层
- [paper29_dirac_spectral_sheaf.md](../paper/paper29_dirac_spectral_sheaf.md)：Dirac 谱层

### 应用论文

- [paper10_spectral_quantum.md](../paper/paper10_spectral_quantum.md)：Wigner 朋友函子模型
- [paper11_spectral_QFT.md](../paper/paper11_spectral_QFT.md)：涨落-耗散伴随对
- [paper14_spectral_condensed_matter.md](../paper/paper14_spectral_condensed_matter.md)：谱丛在凝聚态中的应用
- [paper15_spectral_quantum_chemistry.md](../paper/paper15_spectral_quantum_chemistry.md)：遗忘-构造伴随对
- [paper17_zero_parameter_predictions.md](../paper/paper17_zero_parameter_predictions.md)：味扇区纤维范畴
- [paper20_spectral_gap_first_principles.md](../paper/paper20_spectral_gap_first_principles.md)：Bott 周期与签名纤维化
- [paper25_fibration_cross_domain_methodology.md](../paper/paper25_fibration_cross_domain_methodology.md)：跨域纤维化方法论

## 按主题推荐阅读顺序

### 如果想快速理解 $D \dashv R$
1. Awodey *Category Theory* 第 1-5 章
2. UFPF Paper I §2
3. UFPF Paper I 附录引理 A.3

### 如果想掌握 Grothendieck 纤维化
1. Riehl *Category Theory in Context* 第 7 章
2. Borceux 卷 2 第 8 章
3. UFPF Paper XXI 全文

### 如果想学习层论
1. Mac Lane *Categories for the Working Mathematician* 第 IX 章
2. Stacks Project 第 6 章
3. UFPF Paper XVI §10

### 如果想学习 ∞-范畴
1. Riehl *Elements of ∞-Category Theory* 第 1-3 章
2. Kerodon 第 1 章
3. UFPF Paper I 附录 Phase 30.4/31.1

### 如果想学习幺半范畴与辫子结构
1. Kassel, *Quantum Groups*（辫子张量范畴标准参考）
2. Etingof, Gelaki, Nikshych, Ostrik, *Tensor Categories*
3. UFPF `Braided.lean`

### 如果想学习 Gelfand 对偶与谱几何
1. Connes, *Noncommutative Geometry* 第 1-2 章
2. Gracia-Bondía, Várilly, Figueroa, *Elements of Noncommutative Geometry*
3. UFPF `GelfandDuality.lean`

### 如果想学习同伦与谱流
1. Atiyah, Patodi, Singer, *Spectral Asymmetry and Riemannian Geometry*
2. Riehl, *Categorical Homotopy Theory*
3. UFPF `SpectralFlowHomotopy.lean`

## 版本

- v0.1（2026-08-18）：初始版本
