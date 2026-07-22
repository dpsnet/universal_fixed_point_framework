# Phase 53B 分析笔记：SU(2) 范畴涌现定理

> 日期：2026-07-21
> 关联：Phase 53 路线图，CategoryRepBridge.lean, SpectralGap.lean

---

## 1. 核心问题

从 Phase 53A 中我们确定了 `A_GR_fromBoundary = ad(G)(A) = [G, A]`。现在需要证明：当 A 是 SU(2) 表示中的 Casimir 算子时，`ad(G)(A)` 的特征值谱为 `√{k(k+1)}`。

### 1.1 推导链

```
Rec/Spec 范畴框架
    ↓  A_GR = ad(G)(A) = [G, A]               [53A ✅]
    ↓  选定 G, A 为 SU(2) Lie 代数生成元
    ↓  Casimir 算子 C₂ = Σ L_i²
SU(2) 特征值谱 √{j(j+1)}                      [53B ⬅️ 本阶段]
    ↓  归一化 j = k/2, j_max = k_max/2
agEigenvalue(k, k_max) = √{k(k+1)}/√{k_max(k_max+1)}  [53C ⬅️]
```

### 1.2 关键定理陈述

**定理 1（SU(2) 伴随作用）**。设 `{L₁, L₂, L₃}` 是 SU(2) Lie 代数生成元，满足 `[L_i, L_j] = i·ε_{ijk}·L_k`。则 Casimir 算子 `C₂ = L₁² + L₂² + L₃²` 与所有生成元对易：
`ad(L_i)(C₂) = [L_i, C₂] = 0`

**定理 2（Casimir 谱）**。在自旋 j 表示中，Casimir 算子 C₂ 的特征值为 `j(j+1)`。令 `k = 2j`，则 `C₂` 的特征值正比于 `√{k(k+1)}`。

**定理 3（A_GR 谱）**。设 `A = C₂`（Casimir）, `G = L₃`（一个生成元）。则 `A_GR = ad(G)(A) = [L₃, C₂] = 0`。但这过于平凡。实际需要的 A_GR 是**谱流生成元在切空间的作用**，而非 Casimir 本身。

### 1.3 关键洞察：A_GR 不是 ad(G)(C₂)

这里有一个微妙的点需要澄清：

- `agEigenvalue` 的 `√{k(k+1)}` 谱是 **Casimir 算子 C₂ 的特征值**，不是 `ad(G)(C₂)` 的特征值
- `ad(G)(C₂) = [G, C₂] = 0` 因为 Casimir 与所有生成元对易——但零矩阵的特征值全为零，这显然不对

**正确的连接**：A_GR 本身就是 Casimir 算子（或正比于它），而不是 ad(G) 作用于 Casimir 的结果。

修正后的推导链：

```
A_GR_fromBoundary = ad(G)(A)     [53A: 这是方向导数/生成元]
但 agEigenvalue 是 A_GR 自身（即 SpecObj 中的 A 矩阵）的特征值
    ↓
需要证明：在 Rec_D 边界处，SpecObj.A ∝ C₂ (Casimir)
    ↓
C₂ 的特征值 = j(j+1) = (k/2)(k/2+1) = k(k+1)/4
    ↓
归一化后得到 agEigenvalue(k, k_max) = √{k(k+1)}/√{k_max(k_max+1)}
```

所以 Phase 53A 中 `A_GR_fromBoundary = ad(G)(A)` 的定义是对的，但它是**谱流的生成元**，而 `agEigenvalue` 描述的是被作用的那个 **A 矩阵**（SpecObj 的谱算子）的特征值。两者是不同的对象。

**纠正后的图像**：
- `A_GR_fromBoundary = ad(G)(A)`：谱流的方向导数（作用在 A 上）
- 但 `agEigenvalue` 描述的是 A 本身的特征值（Casimir 谱）
- A_GR 在两种语境中的含义不同：生成元 vs 谱算子

这个混淆需要在 Phase 53A 的修复中澄清。让我更新 A_GR 的命名以避免歧义。

---

## 2. 修正后的定义方案

### 2.1 明确区分两个概念

| 概念 | 符号 | 定义 | 谱 |
|:----|:----|:-----|:---|
| **谱流生成元** | `G_GR` | 作用于 A 的伴随生成元 | 依赖于 Lie 代数结构 |
| **谱算子** | `A_GR` | SpecObj 中的 A 矩阵（Casimir） | `√{k(k+1)}` |

`G_GR = ad(G)(A)` 是 Phase 53A 定义的 `A_GR_fromBoundary`。应改名为 `G_GR_fromBoundary`。

`A_GR` 应定义为 Casimir 算子（或正比于它）。

### 2.2 新的 Lean 模块内容

```lean
/-- SU(2) Lie 代数生成元结构 -/
structure SU2Generators (n : ℕ) where
  L1 : Matrix (Fin n) (Fin n) ℂ
  L2 : Matrix (Fin n) (Fin n) ℂ
  L3 : Matrix (Fin n) (Fin n) ℂ
  commute_L1_L2 : L1 * L2 - L2 * L1 = Complex.I • L3
  commute_L2_L3 : L2 * L3 - L3 * L2 = Complex.I • L1
  commute_L3_L1 : L3 * L1 - L1 * L3 = Complex.I • L2

/-- Casimir 算子 -/
noncomputable def casimir {n : ℕ} (L1 L2 L3 : Matrix (Fin n) (Fin n) ℂ) : Matrix (Fin n) (Fin n) ℂ :=
  L1 * L1 + L2 * L2 + L3 * L3

/-- Casimir 与所有生成元对易 -/
theorem casimir_commutes {n : ℕ} (gen : SU2Generators n) :
    gen.L1 * casimir gen.L1 gen.L2 gen.L3 = casimir gen.L1 gen.L2 gen.L3 * gen.L1 := ...

/-- Casimir 在 2×2 表示中的特征值 -/
theorem casimir_eigenvalue_2x2 : (casimir pauliX pauliY pauliZ).eigenvalues = {3} := ...
```

---

## 3. 执行计划

1. **Step 1**（本笔记）：澄清概念混淆，明确区分 G_GR 和 A_GR
2. **Step 2**：重命名 `A_GR_fromBoundary` → `G_GR_fromBoundary`（在 CategoryGeometry.lean 和 SpectralDynamics.lean 中）
3. **Step 3**：创建 `CategoryRepBridge.lean`，定义 SU(2) 结构 + Casimir + 谱定理
4. **Step 4**：将 `agEigenvalue` 与 Casimir 特征值关联
5. **Step 5**：`lake build` 验证
