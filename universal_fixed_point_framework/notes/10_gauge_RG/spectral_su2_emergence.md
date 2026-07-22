# 谱 SU(2) 范畴涌现：为什么是 SU(2)？

> 本文推导 $A_{\text{GR}}$ 的 Lie 代数结构被 $\mathbf{Rec}/\mathbf{Spec}$ 范畴框架唯一锁定为 $\mathfrak{su}(2)$。

---

## 1. 问题定位

Paper XX 的核心推导链为：

```
三层伴随对嵌套 → 谱流生成元 G_GR = ad(G)(A) → SU(2) Casimir 谱 λ_k ∝ √{k(k+1)} → 谱间隙 Δλ_min → ...
```

其中"SU(2) Casimir 谱"是推导的**中间节点**，但迄今以**输入**而非**输出**出现。本文填补的空白：从 $\mathbf{Rec}/\mathbf{Spec}$ 范畴架构出发，证明 $A_{\text{GR}}$ 的 Lie 代数必须是 $\mathfrak{su}(2)$，而非其他 Lie 代数。

---

## 2. 范畴约束条件（五个约束）

### C1：非平凡谱流（非交换性）

谱流方程（Paper V）：

$$\frac{d}{dt} A_t = [G, A_t]$$

$A_{\text{GR}}$ 是谱流方程中的核心生成元。若 $A_{\text{GR}}$ 对应的 Lie 代数是交换的，则 $[G, A_t] = 0$ 恒成立，谱流退化为平凡恒等映射 —— 这对应 $A_{\text{EM}}$（U(1) 交换生成元），而非引力扇区。**引力扇区的非平凡动力学要求 $A_{\text{GR}}$ 生成一个非交换 Lie 代数**。

**推论 2.1**（排除 U(1)）。$A_{\text{GR}}$ 的 Lie 代数 $\mathfrak{g}_{\text{GR}}$ 满足 $[\mathfrak{g}_{\text{GR}}, \mathfrak{g}_{\text{GR}}] \neq 0$。

### C2：紧形式（谱有界性）

$\mathbf{Spec}$ 范畴中的谱对象 $D(R)$ 具有有界谱（来自 Rec 对象在 D 函子下的紧性保持）。$A_{\text{GR}}$ 作为谱生成元，其谱是有界的，这意味着其 Lie 代数对应的群必须是紧的。

**推论 2.2**（紧实形式）。$\mathfrak{g}_{\text{GR}}$ 是紧实 Lie 代数（对应紧 Lie 群的 Lie 代数）。

### C3：唯一谱间隙（秩为 1）

记 $\Delta\lambda_{\min}$ 为 $A_{\text{GR}}$ 的谱间隙。该值在框架中具有唯一性：
- 从 $\Delta\lambda_{\min}$ 导出裸耦合常数比 $\alpha_1^{(0)}:\alpha_2^{(0)}:\alpha_3^{(0)} = \sqrt{2/3}:1:\sqrt{2}$
- 从 $\Delta\lambda_{\min}$ 导出 R² 系数和临界能量密度
- 框架中不需要第二个独立的谱间隙

对紧半单 Lie 代数 $\mathfrak{g}$，秩 $r = \dim \mathfrak{h}$（Cartan 子代数维数）决定独立 Casimir 不变量个数 $r$。若 $r \geq 2$，则存在 $r$ 个独立 Casimir 算子 $C_2, C_3, \dots, C_{r+1}$，产生多个独立谱间距——与框架中 $\Delta\lambda_{\min}$ 的唯一性矛盾。

**推论 2.3**（秩为 1）。$\text{rank}(\mathfrak{g}_{\text{GR}}) = 1$。

### C4：实正谱条件

$\mathbf{Rec}_D$ 是压缩映射范畴，要求 $D(R)$ 的谱 $\sigma(A_R) \subset \mathbb{R}_{\ge 0}$（实正谱）。$A_{\text{GR}}$ 作为 $\partial\mathbf{Rec}_D$ 处的边界生成元，继承实谱条件。

**推论 2.4**（实谱）。$\sigma(A_{\text{GR}}) \subset \mathbb{R}$，即 $A_{\text{GR}}$ 是实谱算子。

### C5：Casimir 型结构

从 $D \dashv R$ 伴随对和谱流方程的结构可知，$A_{\text{GR}}$ 与所有 Lie 生成元对易：

$$[A_{\text{GR}}, X] = 0,\quad \forall X \in \mathfrak{g}_{\text{GR}}$$

即 $A_{\text{GR}}$ 正比于 $\mathfrak{g}_{\text{GR}}$ 的二次 Casimir 算子 $C_2$。

**推论 2.5**（Casimir 型）。$A_{\text{GR}} \propto C_2$，其中 $C_2$ 是 $\mathfrak{g}_{\text{GR}}$ 的二次 Casimir 不变量。

---

## 3. 锁定定理：$\mathfrak{g}_{\text{GR}} \cong \mathfrak{su}(2)$

**定理 1**（SU(2) 唯一锁定）。在约束 C1–C5 下，$A_{\text{GR}}$ 的 Lie 代数 $\mathfrak{g}_{\text{GR}}$ 同构于 $\mathfrak{su}(2)$。

*证明*。

1. **C1 + C2 + C4**：$\mathfrak{g}_{\text{GR}}$ 是非交换紧实 Lie 代数（C1 排除交换代数，C2 要求紧形式，C4 要求实谱，三者共同确定 $\mathfrak{g}_{\text{GR}}$ 是紧实型 Lie 代数）。

2. **C3**：$\text{rank}(\mathfrak{g}_{\text{GR}}) = 1$。

3. **分类**：紧实秩-1 非交换 Lie 代数只有同构类 $\mathfrak{su}(2) \cong \mathfrak{so}(3) \cong \mathfrak{sp}(1)$（紧实型 $A_1$）。所有这三种实形式在 Lie 代数层面完全同构，且均与 $\mathfrak{su}(2)$ 同构。

4. **C5**：验证 $\mathfrak{su}(2)$ 的二次 Casimir $C_2 = L_1^2 + L_2^2 + L_3^2$ 的特征值为 $j(j+1)$，与 Paper XX §4 中的 $\sqrt{k(k+1)}$ 谱完全一致。$A_{\text{GR}}$ 正比于 $\sqrt{C_2}$，归一化后得到 $\lambda_k = \sqrt{k(k+1)}/\sqrt{k_{\max}(k_{\max}+1)}$。

综上，$\mathfrak{g}_{\text{GR}} \cong \mathfrak{su}(2)$。∎

**注 1.1**（SO(3) vs SU(2)）。在 Lie 代数层面 $\mathfrak{so}(3) \cong \mathfrak{su}(2)$，二者的差异在于全局拓扑（$\pi_1(\text{SO}(3)) = \mathbb{Z}_2$, $\pi_1(\text{SU}(2)) = 0$）。$A_{\text{GR}}$ 的离散谱 $\sqrt{k(k+1)}$ 标记整数 $j = k/2$，允许半整数 $j$（$k$ 奇数），这要求全局群为 $\text{SU}(2)$ 而非 $\text{SO}(3)$。因此 $A_{\text{GR}}$ 的谱结构进一步挑选出 $\text{SU}(2)$。

---

## 4. 为什么排除了其他 Lie 代数？

| Lie 代数 $\mathfrak{g}$ | 秩 | 非交换 | 紧形 | 排除理由 |
|:----------------------|:--:|:-----:|:----:|:---------|
| $\mathfrak{u}(1)$ | 0 | ✗ | ✓ | C1: 非平凡谱流要求非交换性 |
| $\mathfrak{su}(2)$ | 1 | ✓ | ✓ | ✅ **唯一满足** |
| $\mathfrak{so}(3)$ | 1 | ✓ | ✓ | 代数同构于 $\mathfrak{su}(2)$，但全局拓扑不符 |
| $\mathfrak{su}(3)$ | 2 | ✓ | ✓ | C3: 两个独立 Casimir → 两个谱间隙 |
| $\mathfrak{so}(4)$ | 2 | ✓ | ✓ | C3 + $\mathfrak{so}(4) \cong \mathfrak{su}(2) \oplus \mathfrak{su}(2)$ 非单 |
| $\mathfrak{so}(5)$ | 2 | ✓ | ✓ | C3: 秩 2 |
| $\mathfrak{sp}(2)$ | 2 | ✓ | ✓ | C3: 秩 2 |
| $\mathfrak{g}_2$ | 2 | ✓ | ✓ | C3: 秩 2 |
| $\mathfrak{su}(n)\ (n \geq 3)$ | $n-1$ | ✓ | ✓ | C3: 秩 $\geq 2$ |
| $\mathfrak{so}(n)\ (n \geq 5)$ | $\lfloor n/2 \rfloor$ | ✓ | ✓ | C3: 秩 $\geq 2$ |

**注 4.1**（例外 Lie 代数）。$\mathfrak{g}_2, \mathfrak{f}_4, \mathfrak{e}_6, \mathfrak{e}_7, \mathfrak{e}_8$ 的秩分别为 2, 4, 6, 7, 8，均被 C3 排除。

**注 4.2**（$\mathfrak{so}(4)$ 的特殊性）。$\mathfrak{so}(4) \cong \mathfrak{su}(2) \oplus \mathfrak{su}(2)$ 是半单而非单 Lie 代数，有两个独立的 Casimir 不变量（分别来自两个 $\mathfrak{su}(2)$ 因子），且非单的结构意味着谱流方程会有两个独立的生成元通道，与引力 $A_{\text{GR}}$ 的单一性矛盾。

---

## 5. 与三层伴随对嵌套的统一

上述推导可通过三层伴随对嵌套（Paper I §5.8.4）与 Paper XX 的 Cl(1,7) 推导链无缝衔接：

```
三层伴随对嵌套 (Paper I §5.8.4)
    │
    ├── 内层 D ⊣ R: 谱流生成元 G_GR = ad(G)(A) (Paper XX §3)
    │       ↓
    │   约束 C1-C5 作用
    │       ↓
    │   定理 1: g_GR ≅ su(2)
    │       ↓
    ├── SU(2) Casimir 谱 λ_k ∝ √{k(k+1)} (Paper XX §4)
    │       ↓
    ├── Cl(1,7) Bott 分类 → k_max = 8 (Paper XX §5-6)
    │       ↓
    └── 谱间隙 Δλ_min = (√3-1)/6 (Paper XX §6)
```

关键点：定理 1 不依赖 $k_{\max}$ 的值，也不依赖 Cl(1,7) 的具体结构。SU(2) 的身份完全由范畴内部约束 C1-C5 决定，$k_{\max}=8$ 和 Cl(1,7) 只决定 SU(2) 的**表示维数**（$d=8$），而非它的**代数身份**。

---

## 6. 结论

从 $\mathbf{Rec}/\mathbf{Spec}$ 范畴框架出发，通过五个约束条件（非平凡谱流、紧形式、唯一谱间隙、实谱、Casimir 型结构），$A_{\text{GR}}$ 的 Lie 代数被唯一锁定为 $\mathfrak{su}(2)$。该推导填补了 Paper XX 推导链中"SU(2) 从何而来"的逻辑缺口，使整条推导链不再以 SU(2) 为输入，而以范畴约束为输入。

**核心定理**（$A_{\text{GR}}$ Lie 代数锁定）：

$$\boxed{\text{C1 (非交换)} + \text{C2 (紧)} + \text{C3 (秩=1)} + \text{C4 (实谱)} + \text{C5 (Casimir)} \Longrightarrow \mathfrak{g}_{\text{GR}} \cong \mathfrak{su}(2)}$$

---

**版本**：v0.1
**日期**：2026-07-21
