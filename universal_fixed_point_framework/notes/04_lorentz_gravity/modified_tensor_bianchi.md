# 修正张量第二 Bianchi 恒等式（Phase 16B 方向 (β)-3）

日期：2026-09-12
状态：已闭合（Lean §26.11，模块 28 定理/引理零 sorry，全库 4078 jobs `lake build` 通过）
关联：`DiscreteCovariantBianchi.lean` §26.11、`numerical/phase16b_beta3_debug.py`

## 问题

算子级第二 Bianchi（`discrete_second_bianchi_operator`，(β)-1）与分量恒等式
（`discrete_second_bianchi_components`，(β)-1 的分量形态）都在**场**层级。
Phase 66–69 论文需要的是**张量**层级的陈述：朴素张量 Bianchi
Σ_cyc(λ,μ,ν) ∇̃_λ R̂_{μν} ≡ 0 在差分代数中是否精确成立？若否，残差的
精确代数结构是什么？

## 推导链

1. **常值试验场限制**：对常值场 v̂ = fun _ => v，由 `curvature_op_apply`
   （(β)-1）代入 v̂(step) = v，双移位项 v−v 逐点抵消，得
   (F_{μν} v̂)(x) = R̂_{μν}(x)·v（`curvature_op_const_apply`，纯环恒等式）。

2. **协变导数展开**：对 D_λ v̂ = Γ_λ·v（常值场，hU），算子恒等式
   Σ_cyc [D_λ, F_{μν}] = 0 作用于 v̂ 的左端为
   Σ_cyc (∂̃_λ R̂_{μν})·v + Γ_λ R̂_{μν}·v − F_{μν}(Γ_λ·v)。

3. **R̂Γ_λv 项精确抵消**：F_{μν}(Γ_λ·v) 相对逐点作用 R̂_{μν}·(Γ_λ·v)
   的偏差（`curvature_op_apply` 前三项）经 v-系数提取后，其含
   R̂·∂̃Γ 的部分与 naiveNablaCurv 联络项中的 R̂Γ_λv 部分**逐项相消**，
   合并化简后残差为纯二阶差分结构。

4. **修正项**：

   C_{λμν}^r_s = [Γ_λ(step_ν step_μ x) − Γ_λ(step_μ step_ν x)]^r_s     （双移位差）
     + Σ_l ∂̃_μ Γ^r_{νl}(x) · ∂̃_μ Γ^l_{λs}(x)
     − Σ_l ∂̃_ν Γ^r_{μl}(x) · ∂̃_ν Γ^l_{λs}(x)，

   其中 ∂̃_μ Γ(x) = Γ(step_μ x) − Γ(x)。

5. **系数提取**：算子恒等式按 v 线性，左端 = Σ_s [Σ_cyc(∇̃R̂ − C)]^r_s v^s；
   由 `sum4_coeff_zero`（取指示函数 v）得张量恒等式
   **Σ_cyc(λ,μ,ν) (∇̃_λ R̂_{μν} − C_{λμν})^r_s = 0**（逐点精确，无任何假设）。

## 修正项的结构性质

- 三项全是二阶差分结构：双移位差与两个 ∂̃Γ·∂̃Γ 积。光滑场上 Γ 的
  差分为 O(a)，故 C = O(a²)。
- **退化链**（与 §26.6 骨架层一致）：StepsCommute 假设下双移位差消失；
  GammaConstant 假设下 ∂̃Γ 项消失；两者同时成立时 C ≡ 0，恒等式退化为
  `skeleton_second_bianchi`（骨架层第二 Bianchi）。
- 朴素张量 Bianchi（C ≡ 0 的形式）不精确成立；C 是其残差的精确闭形态。

## 数值验证

`numerical/phase16b_beta3_debug.py`：随机 8 点网格、随机 Γ 场与 v，
对全部 64 组 (λ,μ,ν) 复现 Lean 定义，LHS（张量恒等式左端作用于 v）对 RHS
（算子 Jacobi 左端作用于常值场 v）worst |LHS − RHS| = 1.4e-14。

## 边界

本结果是 **Bianchi 层面**的张量恒等式。∇̃^μ G_{μν} = 0（Einstein 散度）
仍需：η 缩并（依赖 Ricci 对称性 + ginv 升指标的 Leibniz 修正，均为 O(a²)）
——这是 (β)-4；开放命题 `EinsteinDivergenceFree` 维持开放。

## 教训

- 第一版修正项第二因子用 Γ(step_μ x) l lam s（未减 Γ x），数值调试
  显示其遗漏了 R̂ 的 ∂̃Γ 部分作用于 Γ_λ v 的项；合并后恰好化简为
  ∂̃Γ·∂̃Γ 的乘积形态。修正结构的对称性（指标 lam 只出现在差分因子中）
  是化简正确的检验标准。
- 证明技术：`set_option maxRecDepth 32768` 必需（simp 深层嵌套）；
  simp only 展开全部定义后 ring 闭合，无需手工分项。
