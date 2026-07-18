# Phase 51：CKM 统一路线图——Yukawa 矩阵的非对角 IFS 结构

## 1. 问题定位

Phase 50 的 $\alpha$ 公式给出了质量层级的主干结构，但残留了 $\times 2$ 以内的 Yukawa 权重偏差。
同时，CKM 混合角（$\theta_{12}, \theta_{13}, \theta_{23}, \delta_{\text{CP}}$）的来源尚未纳入 IFS 框架。

**核心洞见**：两者源于同一个根因——Yukawa 矩阵 $Y_f$ 在 IFS 基中的**非对角结构**。

### 1.1 Phase 50E 的关键发现

超算子方程 $Y = \sum_i c_i^{\alpha_f} U_i Y U_i^*$ 在 $Y$ 对角时只有平凡解 $y_1=y_2=y_3$。
这证明：**$Y_f$ 必须在 IFS 基中非对角**。其非对角元同时编码：
- Yukawa 特征值 $y_i$（质量层级精细结构）
- 代间混合矩阵 $V = U_u^* U_d$（CKM 矩阵）

### 1.2 当前状态

| 问题 | 当前精度 | 状态 |
|:----|:-------:|:----|
| 质量比主干（$\alpha$ 公式） | 5/6 在 $\times 2$ 内 | ✅ Phase 50 |
| Yukawa 权重精细结构 | 未推导 | 🟡 待整合到 CKM |
| CKM 角度 $\theta_{12}, \theta_{13}, \theta_{23}$ | 半定量 | 🟡 待统一 |
| CP 相位 $\delta_{\text{CP}}$ | 未推导 | 🔴 |

---

## 2. 理论基础

### 2.1 IFS 基中的 $Y_f$ 形式

在 Phase 50A 的 IFS 有限谱三元组中，$\mathcal{H}_{\text{gen}} = \mathbb{C}^3$ 承载三个收缩映射。
$D_F$ 在代空间上的一般形式为：

$$D_F = \begin{pmatrix} M_{11} & M_{12} & M_{13} \\ M_{21} & M_{22} & M_{23} \\ M_{31} & M_{32} & M_{33} \end{pmatrix} \otimes \gamma^5$$

其中 $M_{ij} \in \mathbb{C}$ 是 Yukawa 矩阵元。IFS 自相似方程约束 $M$ 的结构。

### 2.2 超算子方程的一般解

$$M = \sum_{i=1}^3 c_i^{\alpha_f} \cdot U_i M U_i^*$$

其中 $U_i$ 是 $\mathbb{C}^3$ 上的幺正矩阵。此方程可重写为超算子 $\Phi(M) = \sum_i c_i^{\alpha} U_i M U_i^*$ 的不动点问题：

$$\Phi(M) = M$$

$\Phi$ 的特征值 1 的本征空间（$\ker(\Phi - \text{id})$）的维数决定允许的 $M$ 的自由度。

### 2.3 从 $M$ 到可观测量

对每个扇区 $f$（上型/下型/轻子），Yukawa 矩阵 $Y_f$ 的极分解为：

$$Y_f = U_f \cdot \Sigma_f \cdot V_f^*$$

其中 $\Sigma_f = \operatorname{diag}(y_1, y_2, y_3)$ 为特征值，$U_f, V_f$ 为酉混合矩阵。

**质量比**：$m_i^{(f)} = y_i^{(f)} \cdot v \cdot c_i^{\alpha_f}$（Phase 50 公式，$y_i$ 现在是 $Y_f$ 的特征值）
**CKM 矩阵**：$V_{\text{CKM}} = U_u^* U_d$（上型和下型左旋混合矩阵的乘积）
**PMNS 矩阵**：$U_{\text{PMNS}} = U_e^* U_\nu$（类似）

---

## 3. 阶段划分

### Phase 51A：$U_i$ 的非交换表示分类

**目标**：确定满足 IFS 谱三元组公理（尤其第一阶条件 $[D_F, a] = 0$）的 $U_i$ 幺正表示。

**方法**：
1. 列出 $\mathrm{U}(3)$ 中所有可能的 $U_1, U_2, U_3$ 满足：
   - $U_1 = I$（约定）
   - $U_i U_i^* = I$（幺正性）
   - $U_i$ 构成 $S_3$（6 元置换群）或 $A_3$（循环群）的表示
2. 对每种表示计算超算子 $\Phi$ 的特征值与特征空间
3. 筛选特征值 $\lambda = 1$ 的非平凡本征空间

**候选**：
- $S_3$ 置换表示（6 种置换矩阵）
- $U(2)$ 非交换子群表示
- 混合：置换 × 相位

**产出**：
- `notes/spectral_Ui_classification.md` — $U_i$ 表示分类
- 数值筛选脚本 `paperX_Ui_search.py`

**验证标准**：
- $\dim \ker(\Phi - \text{id}) \geq 1$（存在非平凡解）
- 解空间至少容下 3 个扇区（$Y_u, Y_d, Y_e$）的独立 $M$ 矩阵

---

### Phase 51B：$Y_f$ 的一般解空间

**目标**：对 Phase 51A 选出的 $U_i$，解析求解 $Y_f$ 的参数化形式。

**方法**：
1. 对 $\Phi(M) = M$ 展开为 9 个实方程（$M$ 为 $3\times 3$ 复矩阵，自由度 18）
2. 解空间维数 $d = \dim\ker(\Phi - \text{id})$
3. 参数化 $Y_f$ 为 $d$ 个自由参数的函数
4. 分别代入 $Y_u, Y_d, Y_e$（不同 $\alpha$ 值）

**产出**：
- `notes/spectral_Yukawa_solution_space.md`
- 数值脚本 `paperX_Yukawa_parameterization.py`

**验证标准**：
- 解空间包含至少 6 个自由参数（足够拟合 3 个扇区 × 2 类数据）
- 解空间物理（特征值正定、混合矩阵酉）

---

### Phase 51C：特征值分解 → 质量比 + CKM

**目标**：将 $Y_f$ 对角化，提取质量比和混合矩阵，与实验对比。

**方法**：
1. 对 $Y_u$ 进行奇异值分解（或极分解）
2. 对 $Y_d$ 同理
3. 计算 $V_{\text{CKM}} = U_u^* U_d$
4. 与实验的 CKM 矩阵对比：
   - $|V_{us}| = 0.2243$（Cabibbo 角）
   - $|V_{cb}| = 0.0410$
   - $|V_{ub}| = 0.0038$
   - $\delta_{\text{CP}} = 1.20\ \text{rad}$
5. 质量比 $m_i^{(f)}$ 与 Phase 50 公式对比，验证 ×2 以内偏差是否被 $Y_f$ 特征值修正

**产出**：
- `notes/spectral_CKM_from_IFS.md` — CKM 矩阵的 IFS 推导
- 数值脚本 `paperX_CKM_prediction.py`

**验证标准**：
- 全部 6 个质量比在 ×1.5 以内
- CKM 角度在实验误差 ×2 以内
- 自由参数数 ≤ 6（3 扇区 × 2 参数/扇区）

---

### Phase 51D：CP 相位与 PMNS

**目标**：将框架扩展到 CP 相位 $\delta_{\text{CP}}$ 和 PMNS 中微子混合矩阵。

**方法**：
1. 引入 $Y_f$ 的复相位自由度（当前 $M$ 为实矩阵的推广）
2. CP 相位来自 $U_u^* U_d$ 的不可约复相位
3. 唯象公式：$\delta_{\text{CP}} \approx \arg\det[Y_u^* Y_u, Y_d^* Y_d]$ 或类似
4. 中微子扇区：通过 See-saw 的 $M_\nu = -M_D M_R^{-1} M_D^T$ 推导 PMNS

**产出**：
- `notes/spectral_CP_phase.md`
- `notes/spectral_PMNS_from_IFS.md`
- 数值脚本 `paperX_CP_PMNS.py`

**验证标准**：
- $\delta_{\text{CP}}$ 在 $1.0\ \text{rad}$ — $1.5\ \text{rad}$ 范围内
- PMNS 混合角数量级正确（大角 $\theta_{23} \approx 45^\circ$）

---

### Phase 51E：完整链数值验证

**目标**：全部可观测量统一验证。

| 可观测量 | 当前精度 | 目标精度 |
|:--------|:-------:|:--------:|
| 6 个质量比 | $\times 1.2$ - $\times 2.3$ | $\times 1.5$ 以内 |
| $|V_{us}| = 0.2243$ | 未推导 | $\pm 30\%$ |
| $|V_{cb}| = 0.0410$ | 未推导 | $\pm 50\%$ |
| $|V_{ub}| = 0.0038$ | 未推导 | 数量级正确 |
| $\delta_{\text{CP}} = 1.20$ rad | 未推导 | 符号 + 范围正确 |
| PMNS $\theta_{23} \approx 45^\circ$ | 未推导 | 大角 |

**产出**：
- `notes/spectral_CKM_complete.md`
- 完整数值脚本 `paperX_ckm_complete.py`

---

## 4. 路线图

```
Phase 51A (1-2周)    Phase 51B (2-3周)    Phase 51C (2-3周)    Phase 51D (1-2周)    Phase 51E (1周)
┌───────────────┐   ┌───────────────┐   ┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│ U_i 表示分类   │   │ Y_f 解空间    │   │ F特征值/CKM   │   │ CP/PMNS      │   │ 完整验证      │
│               │   │               │   │               │   │               │   │               │
│ S₃/非交换表示  │→  │ Φ(M)=M 解析解 │→  │ Y_f对角化→质量│→  │ 复相位→δ_CP  │→  │ 全部6质量+    │
│ 超算子Φ特征值  │   │ d自由度参数化  │   │ V_CKM=U_u^*U_d│   │ See-saw→PMNS │   │ CKM+PMNS+CP  │
└───────────────┘   └───────────────┘   └───────────────┘   └───────────────┘   └───────────────┘
```

## 5. 依赖关系

| Phase | 依赖 | 说明 |
|:-----|:----|:----|
| 51A | Phase 50A (IFS 有限谱三元组) | $U_i$ 的定义依赖 IFS 构造 |
| 51B | Phase 51A | 解空间依赖 $U_i$ 的显式形式 |
| 51C | Phase 51B + Phase 50 (α 公式) | $V_{\text{CKM}}$ 来自 $Y_f$ 对角化 |
| 51D | Phase 51C | CP 相位是中微子扇区的推广 |
| 51E | 全部 | 统一收敛 |

## 6. 参考文献

1. Phase 50E: `notes/spectral_yukawa_IFS_weights.md` — U_i 探索记录
2. Phase 50A: `notes/spectral_finite_IFS_triple.md` — IFS 有限谱三元组
3. Connes & Marcolli (2008), *Noncommutative Geometry, Quantum Fields and Motives*
4. Cabibbo (1963), *Unitary Symmetry and Leptonic Decays*, Phys. Rev. Lett. 10, 531
5. Kobayashi & Maskawa (1973), *CP-Violation in the Renormalizable Theory of Weak Interaction*, Prog. Theor. Phys. 49, 652
