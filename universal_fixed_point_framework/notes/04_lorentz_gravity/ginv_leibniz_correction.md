# ginv 升指标的 Leibniz 修正——Phase 16B (β)-4 第二阶段缺口②闭合

> 研究笔记 · 2026-09-12 · 状态：**数值与形式化双闭合**
> 形式化：`DiscreteCovariantBianchi.lean` §26.14（`solve_right` / `dginv_left` / `dginv_right` / `discrete_metric_compatible`，模块 38 定理零 sorry，全库 4078 jobs 构建通过）
> 数值：`numerical/phase16b_beta5_ginv_leibniz.py`

## 1. 三条精确恒等式（逐点，机器精度验证）

记 ∂̃_ρ T(x) := T(step_ρ x) − T(x)，δ 假设 ginv^{mi}g_{is} = δ^m_s（逐点），g/ginv 对称。

### 1.1 ginv 差分恒等式（双移位变体）

$$∂̃_ρ ginv^{μν}(x) = -ginv^{μa}(step_ρ x)\, ∂̃_ρ g_{ab}(x)\, ginv^{bν}(x) \quad (A)$$
$$∂̃_ρ ginv^{μν}(x) = -ginv^{μa}(x)\, ∂̃_ρ g_{ab}(x)\, ginv^{bν}(step_ρ x) \quad (B)$$

数值：变体 A 残差 1.3e-15，变体 B 残差 1.1e-15（随机对称正定度量，8 点）。连续对应 ∂(g⁻¹) = −g⁻¹·∂g·g⁻¹——差分代数中**逐点精确成立**（双 δ + 双对称的纯代数推论），非渐近。

### 1.2 离散度规相容恒等式

对任何满足离散 Christoffel 公式 Γ^r_{μn} = ½ ginv^{rl}(∂̃_μ g_{ln} + ∂̃_n g_{μl} − ∂̃_l g_{nμ}) 的 Γ：

$$∂̃_ρ g_{μν}(x) = g_{μλ}(x)\,Γ^λ_{ρν}(x) + g_{νλ}(x)\,Γ^λ_{ρμ}(x)$$

数值残差 2.1e-14。连续对应 ∇_ρ g_{μν} = 0（Levi-Civita 相容性）的差分形态。**移位配置唯一**：Γ 的导数指标 ρ 必须位于下标对 (ρν)/(ρμ)，降指标度量取同点 x；g(step_ρ x) 降指标、半程移位均不成立（残差 O(1)）。

### 1.3 升指标 Leibniz 的精确亏损

精确移位 Leibniz ∂̃(A·B)(x) = ∂̃A(x)·B(step x) + A(x)·∂̃B(x)（数值 4.4e-16）给出：把 ginv 提出协变差分 ∇̃^μ T_μ ≡ Σ ginv^{μa}∇̃_μ T_a 时，修正项为 ∂̃ginv·(移位值)，由 1.1 的显式恒等式承载。

## 2. 与 (β)-4 主线的关系

Einstein 张量 G_{μν} = R̂_{μν} − ½ g_{μν}R̂ 的场层级协变散度修正 ∇̃^μ G_{μν} 需要：
- 升指标 ∇̃^μ = ginv^{μa}∇̃_a 与 ∇̃_μ 的交换——修正由 1.1 给出；
- ginv 穿过差分与缩并的分配——修正由 1.2（相容）控制。

至此 (β) 剩余仅 ③：Einstein 张量构造与散度（`EinsteinDivergenceFree` 维持开放）。

## 3. Lean 证明结构（§26.14）

- `solve_right`：右 δ-解引理——线性方程 A·g = B 在互逆对称下的显式解 A t = Σ_s B s·ginv x s t。δ-插入（g·ginv = δ 由双对称从 hctr 推出）+ sum_comm + sum_mul 因子化。
- `dginv_left`/`dginv_right`：在 x / step_ρ x 点分别应用 solve_right；hAB 的建立用双 δ 相消。
- `discrete_metric_compatible`：核心折叠引理 key0——Σ_λ g_{aλ}·Σ_l ginv^{λl}T(l) 经 mul_sum、sum_comm、δ-折叠（sum4_ite_eq'）化为 T(a)；两次应用 + g 对称交叉项相消。

**求和技术教训（本次新确立）**：`rw` 的求和模式不能匹配绑定变量下的子项（模式含 ?f 需实例化绑定元时失败）；因子提取在绑定下须用 `simp only [Finset.sum_mul]`（simp 可入绑定）或先 `Finset.sum_congr` 逐项下降；`Finset.sum_comm` 的显式 `f :=` 第一个形式参数是**外层**求和指标；`rw [sum4_eq_finset_sum]` 只转换首个出现，多处转换用 `simp only`；`Finset.sum_neg_distrib` 的 `-∑ → ∑-` 方向用 `←`。
