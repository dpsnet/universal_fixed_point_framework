# 度规项散度的 δ 缩并与曲率化简（Phase 16B (β) 新阶段）

日期：2026-09-12
状态：数值闭合 + Lean §26.17 形式化闭合（43 定理零 sorry，全库 4078 jobs）

## 1. 背景

(β)-链端到端显式修正形态（phase16b_beta7，2.8e-14）：

```
∇̃^μG_{μν} = Q + T2 + ConnRic − ginv·(Cc3−K2−K3) − ½B
```

其中 `B_ν = Σ_{μa} ginv^{μa}∇̃_μ(g_{aν}R̂)` 为度规项散度。
结构性发现：无单一主载体（Q−½∂̃R̂ 缺陷 7.4，分布式抵消；
PS 非主载体 |E^sym|/|E|=0.91）。

本轮（beta8，seed 43）目标：把 B 项与 ConnRic 项显式化为
ginv·∂̃g·R̂ / ginv·Γ·g·R̂ / ginv·Γ·naiveCurv 型纯曲率修正，
为 `EinsteinDivergenceFree` 的最终显式陈述扫清最后代数障碍。

## 2. beta8 三个数值结论

脚本：`numerical/phase16b_beta8_metric_term.py`（seed 43，全部机器精度闭合）

### 2.1 度规项 δ 展开（残差 2.8e-14）

```
B_ν = ∂̃_νR̂ + 度规相容型修正（5 项）
```

对 T_{aν} = g_{aν}·R̂ 施加 (0,2)-协变差分（移位混合约定）：

```
∇̃_μ(g_{aν}R̂) = ∂̃_μ(g_{aν}R̂) + Σ_b [Γ^b_{μα}(x)g_{bν}R̂(step) + Γ^b_{μν}(x)g_{ab}R̂(step)
                              − Γ^b_{μα}(step)g_{bν}R̂(x) − Γ^b_{μν}(step)g_{ab}R̂(x)]
```

∂̃(gR̂) 移位分裂：`∂̃_μ(g_{aν}R̂) = ∂̃_μg_{aν}·R̂(step) + g_{aν}(x)·∂̃_μR̂`。

关键：`Σ_a ginv^{μa}g_{aν} = δ^μ_ν` **直接走 hctr（ginv·g 缩并），
无需 g 对称性**。δ 缩并把 g_{aν}(x)·∂̃_μR̂ 项化为 ∂̃_νR̂。
其余修正：ginv·∂̃g·R̂(step) 一项 + ginv·Γ·g·R̂ 移位四项
（连续极限为 O(a) artifact）。

### 2.2 相容代换（残差 5.7e-14）

修正中的 `∂̃_μg_{aν}` 用 §26.14 `discrete_metric_compatible` 代换：

```
∂̃_μg_{aν} = g_{aλ}Γ^λ_{μν} + g_{νλ}Γ^λ_{μa}
```

代换后 B_ν 成为**纯 Γ·g·R̂ 型**七项修正（ginv·Γ·g·R̂ 全移位族）。

### 2.3 ConnRic 曲率迹展开（残差 2.1e-14）

```
ConnRic_ν = Σ_{μa} ginv^{μa}(conn_μRiĉ)_{aν}
          = Σ_{μabr} ginv^{μa}·Γ^r_{μb}·naiveCurv^{b}_{~ raν}   （K 型，四重和）
```

纯 ricciTensor 定义展开：(conn_μRiĉ)_{aν} = Σ_{br} Γ^r_{μb}·naiveCurv...
不含任何 ∇̃ 或 ∂̃。这是 ConnRic 可 Lean 化的形态：
只含 γ 与 naiveCurv（均为已有原语）。

## 3. Lean §26.17：metric_term_divergence

文件：`formal_proof/MUFPFormalization/src/MUFPFormalization/DiscreteCovariantBianchi.lean`

- `covDiff02`：(0,2)-张量协变差分定义（移位混合约定，与数值 nabla02 一致）。
- `metric_term_divergence`：在 `hctr : Σ_a ginv^{μa}g_{aν} = δ^μ_ν`
  （无需 hg 对称）下，

  ```
  Σ_{μa} ginv^{μa}∇̃_μ(g_{aν}R̂) = ∂̃_νR̂ + Σ_{μa} ginv^{μa}(∂̃g·R̂(step) + 4 项 Γ·g·R̂ 移位修正)
  ```

证明结构（三步）：
1. `splitTerm`：逐 (μ,a) 把 covDiff02 按 ∂̃(gR̂) 移位分裂 + conn 逐 b 重组，
   分裂为「修正载体 + g_{aν}(x)·∂̃_μR̂」；
2. `eLHS`：sum4_congr 逐项 + `unfold sum4; ring` 完成求和分配
   LHS = S_main + S_delta；
3. `eS2`：S_delta 经 fac（`unfold sum4; ring` 因子提取，避开 Finset.sum_mul
   在绑定变量下的匹配失败）、hctr 化为 ite、ν=μ flip、`sum4_ite_eq'`，
   得 ∂̃_νR̂。

### 证明教训（本轮新增）

- `rw [show ... from by ...]` 中内层 by 块：若 rw 的子句使目标成为 rfl，
  rw 自动关闭目标，后续 tactic 报 "No goals to be solved"——直接省略。
- 求和分配优先用 `unfold sum4; ring`，避免 Finset 引理在绑定下的匹配问题。

## 4. 剩余缺口（通往 EinsteinDivergenceFree）

1. ~~ConnRic 的 K 型 Lean 化~~ **已闭合（2026-09-12，§26.18）**：
   `conn02`（(0,2)-张量协变差分的联络部分，covDiff02 = ∂̃ + conn02）+
   `connric_curvature_expand` 四重 K 型和定理（44 定理零 sorry，一次通过）。
   证明要点：ricciTensor 的 x 参数在 curry 末尾（`s ν x`），需包
   lambda `fun y c d => ricciTensor F Γf c d y` 适配 conn02 的
   `T : X.T → Fin 4 → Fin 4 → ℝ`；逐 b 因子入和用
   `unfold sum4; ring` 一次闭合。
2. ~~EinsteinDivergenceFree 最终显式陈述~~ **已闭合（2026-09-12，§26.19，
   `einsteinDiv` + `einstein_divergence_explicit`，45 定理零 sorry）**：

   **E_ν = T1_ν + K_ν − ½(∂̃_νR̂ + 修正_ν)**（Q/T2 抵消形态 + 全曲率原语）

   beta9（`phase16b_beta9_final_assembly.py`，seed 43）四个验证全部机器精度：
   定义层 2.8e-14、抵消形态 2.8e-14、全显式形态 3.2e-14、方向分裂 2.8e-14。

   关键推导：beta7 装配 `E = Q + T2 + ConnRic − ginv·(Cc3−K2−K3) − ½B`
   代入 §26.16 收缩 Bianchi `ginv·(Cc3−K2−K3) = Q − T1 + T2` 后
   **Q、T2 完全抵消**——收缩 Bianchi 修正对 Einstein 散度无净贡献，
   最终公式只剩 Ricci 散度载体（T1 + K）与度规项修正（½B 展开）。

   Lean 证明三步：`e1` 逐点线性 covDiff02(G) = covDiff02(Riĉ) − ½covDiff02(gR̂)
   + 求和分配（simp only [covDiff02, einsteinTensor] + unfold sum4; ring）；
   `e2` covDiff02 = ∂̃ + conn02 逐点 rfl + 分配；然后 rw 代入
   §26.18 与 §26.17 两个定理自动收尾。

   适配要点：einsteinTensor 与 ricciTensor 的 x 参数均在 curry 末尾，
   需包 `fun y c d => ... c d y` lambda。

   **至此 (β) 真值路径全链闭合**：∇̃^μG_{μν} 的显式修正公式以纯曲率原语
   （ginv·Γ·g·R̂、ginv·Γ·naiveCurv、∂̃R̂、∂̃Riĉ）形式机器证明，
   连续极限 O(a) 退化到经典 ∇^μG_{μν} = 0。

## 5. 数值记录

| 验证 | 脚本 | seed | 残差 |
|------|------|------|------|
| 度规项 δ 展开 | phase16b_beta8_metric_term.py | 43 | 2.8e-14 |
| 相容代换 | 同上 | 43 | 5.7e-14 |
| ConnRic 曲率迹展开 | 同上 | 43 | 2.1e-14 |
| (β) 端到端显式修正 | phase16b_beta7_*.py | — | 2.8e-14 |
