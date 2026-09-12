# 修正 Ricci 对称性（场层级）——Phase 16B (β)-4 前置缺口闭合

> 研究笔记 · 2026-09-12 · 状态：**数值与形式化双闭合**
> 形式化：`formal_proof/MUFPFormalization/src/MUFPFormalization/DiscreteCovariantBianchi.lean` §26.13（定理 `metric_ricci_eq`、`modified_ricci_symmetry`，模块 33 定理零 sorry，全库 4078 jobs 构建通过）

## 1. 恒等式

场层级 Ricci 张量 $\hat{R}_{\sigma\nu}$（裸迹定义 $\hat{R}_{\sigma\nu}=\sum_{a,r}\hat{R}^{r}{}_{\sigma a\nu}$，无对称性假设）满足

$$\hat{R}_{\sigma\nu}-\hat{R}_{\nu\sigma}
=\tfrac12\, g^{ab}\bigl(\mathrm{PS}_{b\sigma a\nu}-\mathrm{PS}_{b\nu a\sigma}\bigr),$$

其中

- $\mathrm{R4}_{abcd}(p)=\sum_r g_{ar}(p)\,\hat{R}^{r}{}_{bcd}(p)$ —— 度量降指标 $(0,4)$ 曲率（`lower4`）；
- $\mathrm{PS}_{abcd}(p)=\mathrm{R4}_{abcd}(p)-\mathrm{R4}_{cdab}(p)$ —— **对偶交换残差**（`pairSwapRes`）。

## 2. 推导链（纯 δ-代数，无场方程、无联络假设）

1. **度量 Ricci = 裸迹 Ricci**（`metric_ricci_eq`）：
   $\sum_{a,b}g^{ab}\,\mathrm{R4}_{b\sigma a\nu}=\hat{R}_{\sigma\nu}$。
   证明路线：ginv 因子移入 r-和（`Finset.mul_sum`）→ b/r 双和交换（`Finset.sum_comm`，显式 `f :=`）→ 因子化（`Finset.sum_mul`）→ δ 缩并（假设 `hctr : ginv^{mi}g_{is}=\delta^m_s`）→ δ 求值（`sum4_ite_eq'`）→ `ricciTensor` 定义。
2. **Pair swap 分解**：$A=-A+S$。把两侧度量化后相减，反对称部分由四项 `ginv·lower4` 双和构成；利用 **ginv 对称假设** `hginv : g^{μν}=g^{νμ}` 与 `Finset.sum_comm` 双和换名（hX/hY），把它们配成两对 `±`；乘积分配（dist）把 `ginv·(PS−PS)` 展开为恰好这四项；合并得 $\hat{R}_{\sigma\nu}-\hat{R}_{\nu\sigma}=g^{ab}\,\mathrm{PS}_{b\sigma a\nu}$ 的反对称化，即 ½ 形式。

形式化只需两条度量假设：`hginv`（ginv 对称）与 `hctr`（ginv·g = δ）。无 $\widetilde\partial\Gamma=0$、无场方程。

## 3. 数值证据

`numerical/phase16b_beta4_explore.py` 第 7 节：随机场上 `max|A − rhs| = 3.3×10⁻¹⁵`（机器精度）。场层级 Ricci 不对称幅值 ≈ 0.29·|Ric|，**全部由 PS 承载**。

## 4. 物理含义

- **PS 是连续理论中恒零的对偶交换对称性 $\mathrm{R4}_{abcd}=\mathrm{R4}_{cdab}$ 在差分代数中的残差**，量级 $O(\widetilde\partial\Gamma)$（一阶差分导数量级）。
- 场层级 Ricci 不对称不是误差，而是有精确载体（PS）的结构性现象：不对称 ⟺ 对偶交换残差的反对称缩并。
- **骨架层退化**（$\widetilde\partial\equiv0$）下 PS ≡ 0，恒等式右端归零，退化为骨架 Ricci 对称 `skeleton_ricci_symmetric`——场层级修正与骨架层结果严格衔接。
- 连续极限（∂̃→0）下右端 → 0，回到经典 Ricci 对称。

## 5. 环/求和技术教训（形式化耗时点）

`ring` 的三个结构性盲区：① 不把 `−∑` 提出为 `−(∑)`；② 不交换求和指标顺序（耦合指标缩并必须手工 `Finset.sum_comm (f := 二元函数)`）；③ 不提出 `(∑f)·c` 的因子（用 `Finset.sum_mul` 正向，或对目标用 `(Finset.sum_mul _ _ _).symm`；`rw [← Finset.sum_mul]` 会同时重写两侧所有匹配，慎用）。docstring 必须紧邻定理：`/-- doc -/ set_option ... in theorem` 解析失败，docstring 要放在 set_option 行之后。

## 6. 在 (β)-4 中的位置

这是 (β)-4 第二阶段（Einstein 张量 $G_{\mu\nu}=\hat{R}_{\mu\nu}-\tfrac12 g_{\mu\nu}\hat{R}$ 及其协变散度修正）的前置缺口：要写出 $G$ 的对称/散度修正，必先有 $\hat{R}_{\sigma\nu}-\hat{R}_{\nu\sigma}$ 的精确表达式。剩余缺口：② ginv 升指标的 Leibniz 修正；③ Einstein 张量构造与散度（`EinsteinDivergenceFree` 维持开放，勿过度宣称）。
