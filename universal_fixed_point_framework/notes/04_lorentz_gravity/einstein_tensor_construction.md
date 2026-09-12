# Einstein 张量构造与散度修正——Phase 16B (β)-4 缺口③第一阶段

> 研究笔记 · 2026-09-12 · 状态：**构造层数值与形式化双闭合；散度修正结构已识别，修正闭合留待下一阶段**
> 形式化：`DiscreteCovariantBianchi.lean` §26.15（`scalarCurvature` / `einsteinTensor` / `einstein_trace` / `einstein_asymmetry`，模块 40 定理零 sorry，全库 4078 jobs 通过）
> 数值：`numerical/phase16b_beta6_einstein_div.py`

## 1. 构造与恒等式（机器精度）

- **标量曲率** R̂ = ginv^{σν}Riĉ_{σν}；**Einstein 张量** G_{μν} = Riĉ_{μν} − ½ g_{μν}R̂。
- **迹恒等式**：ginv^{μν}G_{μν} = −R̂（4 维；数值 1.1e-16）。纯 δ-代数：ginv^{μν}g_{μν} = 4（逐 μ：Σ_ν ginv^{μν}g_{νμ} = 1，经 g 对称 + hctr）。
- **不对称推论**：G_{μν} − G_{νμ} = Riĉ_{μν} − Riĉ_{νμ}（度量项对称相消）——G 的不对称仍由 PS 精确承载（§26.13 衔接）。

## 2. 散度亏损的结构（数值发现）

E_ν = ∇̃^μ G_{μν}（(β)-链 ∇̃ 约定）在场层级 **不恒零**（max|E| = 19.4，|E|/|R̂| ≈ 38），三个关键结构结论：

1. **PS 非主载体**：用对称化 Ricci 构造 G^sym，|E^sym|/|E| = 0.91——散度亏损的主要载体**不是** Ricci 不对称（PS），而是升指标/联络/Leibniz 结构。这与 §26.13（PS 承载 Ricci 不对称）互补：不对称与散度是两个独立的差分artifact通道。
2. **方向指标化精确分解**（3.6e-15）：

   E_ν = Σ_μ ∂̃_μ H^{(μ)}_ν − Σ_{μa} ∂̃_μ ginv^{μa}·G_{aν}(step_μ) + Σ_{μa} ginv^{μa}·(conn_μ G)_{aν}

   其中 **H^{(μ)}_ν(y) := Σ_a ginv[y,μ,a]G[y,a,ν] 是方向指标化的标量场**——收缩指标 μ 与求导方向 μ 绑定，不能先对 μ 求和再造标量场（本笔记记录了一次由此导致的分解失败与修正）。
3. **一阶 artifact**：度量扰动标定 g = I + εh 下 max|E| ≈ 19.4 / 1.27 / 0.145（ε = 1 / 0.1 / 0.01），E = O(ε)——与 §26.7(b) 负面结果（场层级 E = O(a)，比缩并残差 O(a²) 高一阶）一致：场层级不存在朴素散度恒等式。

## 3. 对 EinsteinDivergenceFree 的定位

开放命题维持开放，但修正结构已完全识别：E_ν 的三项分解中，∂̃ginv 项由 §26.14 `dginv_left/right` 承载，conn 项与 ∂̃H 项的曲率化简需走 §26.12 Riemann 散度恒等式 + §26.13 修正 Ricci 对称的链。下一阶段：将 E_ν 化为 **2 阶差分结构 + PS 缩并 + O(a²) 骨架残差** 的显式修正形态（类比 §26.12 的 Cc3−K2−K3 分解）。

## 4. Lean 证明要点（§26.15）

- `einstein_trace`：e1 展开为显式 16 项后 `ring`；e2 逐 μ 用 `sum4_congr` + `hg` 改写 + `hctr` + `simp` 得 1，再 `unfold sum4; ring` 得 4。新教训：含 ℝ 除法的 def 需 `noncomputable`；`show` 折叠定义时括号结构必须与目标语法一致（`1/2 * (4 * R)` 左结合）。

---

## 5. 散度修正显式形态（2026-09-12 补，§26.16，端到端闭合）

**数值装配（`numerical/phase16b_beta7_contracted_bianchi.py`，max 残差 2.8e-14）**：

$$\nablã^μ G_{μν} = Q_ν + T2_ν + ConnRic_ν - ginv\!\cdot\!(Cc3{-}K2{-}K3)_ν - \tfrac12\, ginv^{μa}\nablã_μ(g_{aν}\hat R)$$

其中 Q_ν = Σ_{sμr} ginv^{sμ}(∇̃_r R̂_{μν})^r_s，T2_ν = Σ_{sμ} ginv^{sμ}∂̃_νRiĉ_{sμ}，ConnRic 为 Ricci 的联络散度，Cc3−K2−K3 为 §26.12 的修正项。链条：ginv 缩并 §26.12（3.6e-15）+ ∇̃^μRiĉ = T1 + ConnRic（7.1e-15）+ ∇̃^μG = ∇̃^μRiĉ − ½ginv∇̃(gR̂)。

**结构性发现**：Q − ½∂̃_νR̂ 缺陷达 7.4（∂̃R̂ 幅值 4.0）——Q 本身是一阶量，与 T2/ConnRic/gC/½B 的各项在连续极限下分布式抵消，无单一主载体（与 beta6 的 |E^sym|/|E| = 0.91 一致：不对称与散度是两个独立 artifact 通道）。

**Lean（§26.16，模块 42 定理零 sorry）**：
- `contracted_riemann_divergence`：Q − T1 + T2 = Σ ginv·(Cc3−K2−K3)——§26.12 点值恒等式的 ginv 加权求和（sum4_congr 逐项 + rw，一次通过）；
- `scalar_curvature_leibniz`：T2 = ∂̃_νR̂ − Σ∂̃ginv·Riĉ(step)——标量移位积规则（unfold + ring）。

至此 (β)-4 全链闭合：分量级/张量级修正 Bianchi（§26.6）→ Riemann 散度（§26.12）→ 修正 Ricci 对称（§26.13）→ ginv Leibniz（§26.14）→ Einstein 构造层（§26.15）→ 收缩 Bianchi 恒等式（§26.16）。`EinsteinDivergenceFree` 的场层级显式修正形态已由数值端到端确立，Lean 端收缩恒等式与 Leibniz 已闭合；conn 项与 ∇̃(gR̂) 项的进一步曲率化简（ConnRic → K 型修正、½B → 度规相容型修正）为下一阶段。
