# 离散 Riemann 散度恒等式——(β)-4 第一阶段（裸迹缩并）

日期：2026-09-12
状态：已闭合（Lean §26.12，模块 31 定理/引理零 sorry，全库 4078 jobs `lake build` 通过）
关联：`DiscreteCovariantBianchi.lean` §26.12（`discrete_riemann_divergence`）、
`numerical/phase16b_beta4_explore.py`

## 结果

对 (β)-3 修正张量 Bianchi 恒等式取 λ = r 并对 r 求和（裸迹缩并，无度量），得
**离散 Riemann 散度恒等式**（逐点精确，无任何假设）：

  Σ_r (∇̃_r R̂_{μν})^r_s − ∂̃_μ Riĉ_{sν} + ∂̃_ν Riĉ_{sμ}
  = Cc3 − K2 − K3

- `Riĉ_{sν}(x) = Σ_r R̂^r{}_{s r ν}(x)`（`ricciTensor`，裸迹）
- `K2_{μνs} = Σ_{r,a} Γ^r_{μa} R̂^a{}_{sνr} + Σ_a Riĉ_{aν} Γ^a_{μs}`（`contractConn2`）
- `K3_{μνs} = Σ_{r,a} Γ^r_{νa} R̂^a{}_{srμ} − Σ_a Riĉ_{aμ} Γ^a_{νs}`（`contractConn3`）
- `Cc3 = Σ_r [C(r,μ,ν) + C(μ,ν,r) + C(ν,r,μ)]^r_s`（`contractCorr`，(β)-3 修正项
  三循环位置的裸迹，O(a²) 结构）

连续对应：∇^ρ R_{ρsμν} = ∇_μ Ric_{sν} − ∇_ν Ric_{sμ}。这是把 Bianchi 缩并为
散度恒等式的第一级；修正项 K2/K3 是联络一阶项，骨架层（Γ 常值 + step 对易）
下退化为骨架恒等式，与 §26.6/§26.7 退化链一致。

## 证明结构（技术要点）

1. `(β)-3` 在 λ = r 处实例化并对 r 求和（`Finset.sum_eq_zero`）：
   Σ_r Σ_cyc(r,μ,ν)(∇̃R̂ − C)^r_s = 0。
2. 循环位置二/三的和分别归约（`sum_nabla_right2/3`）：
   - 位置二需要**逐点反对称** `naiveCurv(x,r,s,ν,r) = −naiveCurv(x,r,s,r,ν)`
     把耦合指标的联络项归约为 Ricci——此步必须 `Finset.sum_comm` 交换求和
     顺序 + `Finset.sum_mul` 因子化，**ring 不能自动完成**（不交换求和指标、
     不提出 (∑)·c 因子）；
   - 位置三的裸迹与 `ricciTensor` 定义同向，无需反对称。
3. `linarith` 组装（h0 + eP2 + eP3 + ecc 四个线性假设）。

## 数值验证

`numerical/phase16b_beta4_explore.py`（随机度量 + 离散 Christoffel + 随机 step，
无对易假设）：
- ginv 缩并循环和：朴素 O(1) 残差，−C 修正后 1.8e-15（精确）；
- 裸迹缩并（−C）：9.8e-15；
- Riemann 散度恒等式 LHS−RHS：2.1e-14；
- 附带发现：**场层级 Ricci 不对称**（max|Ric−Ric^T| ≈ 0.29·|Ric|）——
  度量相容 Christoffel 下场层级 Ricci 对称性需要修正形态，是下一阶段
  （缩并为 ∇^μG_{μν}）的前置缺口。

## 与此前负面结果的关系

2026-09-11 (b) 的负面结果（场层级 Einstein 散度 E ≠ α·缩并(Bianchi)，E = O(a)）
针对**朴素**张量 Bianchi 的直接缩并；本恒等式是**修正** Bianchi 的缩并，
修正项结构完全不同（联络一阶项 + C 的 O(a²) 裸迹），为 (β)-4 第二阶段
（度量缩并出 ∇̃^μ Riĉ_{μν} = ½ ∂̃_ν R̂ + 修正）提供第一级载体。

## 教训（ring 技术）

- `ring` 能把 `−∑` 归约为 `∑−`，但不能提出 `−(∑)·c` 中的因子、
  不交换求和指标顺序——含耦合指标缩并的恒等式必须手工
  `Finset.sum_comm` / `(Finset.sum_mul _ _ _).symm` 逐步归约。
- `rw [← Finset.sum_mul]` 会同时重写目标两侧所有匹配项，应改用
  `have key := (Finset.sum_mul _ _ _).symm; rw [key]` 局部因子化。
- docstring 必须紧邻定理：`/-- doc -/ set_option ... in theorem` 解析失败。
