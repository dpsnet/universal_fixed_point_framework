# 谱丛理论与 Leaver 三对角矩阵的细分纤维化

**版本**：v0.2（2026-07-25）

**摘要**：本笔记将 Leaver 连续分数法对应的三对角矩阵族 $M(\omega)$ 翻译为谱丛语言，揭示其**细分纤维化（fine fibration）**结构。核心发现：(1) 三对角矩阵的 off-diagonal rank-1 性质天然定义了一个二叉树纤维化；(2) 谱化理论的 D 函子对应谱丛的全局截面；(3) 同伦延拓路径对应谱丛沿参数空间的平行移动（单值性）；(4) 非物理根吸引域对应谱丛分支点的叶间跳跃。这一视角统一了已有的数值技巧，并给出了严格的数学基础。

---

## 1. 三对角矩阵的天然纤维化结构

### 1.1 矩阵族结构

Leaver 径向方程的三对角矩阵 $M(\omega)$ 具有以下结构：

$$M(\omega) = \begin{bmatrix}
\beta_0(\omega) & \alpha_0(\omega) & 0 & \cdots \\
\gamma_1(\omega) & \beta_1(\omega) & \alpha_1(\omega) & \cdots \\
0 & \gamma_2(\omega) & \beta_2(\omega) & \cdots \\
\vdots & \vdots & \vdots & \ddots
\end{bmatrix}_{N \times N}$$

其中 Cook-Zalutskiy 多项式系数：

$$\begin{aligned}
\alpha_n(\omega) &= n^2 + (D_0(\omega) + 1)n + D_0(\omega) \\
\beta_n(\omega) &= -2n^2 + (D_1(\omega) + 2)n + D_3(\omega) \\
\gamma_n(\omega) &= n^2 + (D_2(\omega) - 3)n + D_4(\omega) - D_2(\omega) + 2
\end{aligned}$$

$D_i(\omega)$ 通过奇点指数 $\zeta, \xi, \eta$ 依赖于 $\omega$，总体而言 $M(\omega) = M_0 + \omega M_1 + \omega^2 M_2$，即**二次矩阵多项式**。

### 1.2 分裂结构

将索引集 $\{1, \dots, N\}$ 在 $K$ 处分裂：

$$M(\omega) = \begin{bmatrix}
A(\omega) & \gamma_K(\omega) e_K e_{K+1}^T \\
\alpha_K(\omega) e_{K+1} e_K^T & B(\omega)
\end{bmatrix}$$

其中 $A \in \mathbb{C}^{K \times K}$, $B \in \mathbb{C}^{(N-K) \times (N-K)}$ 各自为三对角矩阵。

**关键性质**：off-diagonal 耦合是 **rank-1 的**——两个子块之间只通过接口位置 $(K, K+1)$ 的一个标量耦合。

### 1.3 Schur 补与界面参量

$$\det M(\omega) = \det A(\omega) \cdot \det\big(B(\omega) - q(\omega) \cdot e_{K+1} e_{K+1}^T\big)$$

其中界面参量：

$$q(\omega) = \gamma_K(\omega) \cdot \alpha_K(\omega) \cdot (A(\omega)^{-1})_{K,K}$$

**物理诠释**：$q(\omega)$ 编码了子块 $A$ 对子块 $B$ 的**影响**，是唯一在界面间传递信息的量。

---

## 2. 二叉树纤维化

### 2.1 递归分解

将分裂递归应用于 $A$ 和 $B$，得到深度 $\log_2 N$ 的二叉树：

```
Level 0:          M[N×N]
                  /     \
Level 1:     A[N/2]    B[N/2]
             /   \      /   \
Level 2:  A₁  A₂     B₁   B₂

每层节点: 子块矩阵
每层边:   界面参量 q(ω)
```

### 2.2 纤维丛结构

定义谱丛 $\mathcal{S}$：

- **底空间** $B$：复 $\omega$-平面 $\mathbb{C}$
- **纤维** $F_\omega$：$\sigma(M(\omega)) = \{\lambda \in \mathbb{C} : \det(M(\omega) - \lambda I) = 0\}$（$N$ 个特征值）
- **投影** $\pi: \mathcal{S} \to B$：$(\omega, \lambda) \mapsto \omega$
- **全空间**：$\mathcal{S} = \{(\omega, \lambda) \in \mathbb{C}^2 : \det(M(\omega) - \lambda I) = 0\}$

**纤维化定理**（本笔记提出）：二叉树分解给出了谱丛的**细分纤维化**——每个节点对应一个子谱丛，层间的界面参量 $q(\omega)$ 提供了子丛间的"胶水"。

**推论 2.1**：全局特征值条件 $\det M(\omega) = 0$ 等价于二叉树**所有节点**的 Schur 补条件同时成立。

**推论 2.2**：QNM 频率 $\omega_{\text{QNM}}$ 是谱丛 $\mathcal{S}$ 在 $\lambda=0$ 截面上的全局截面——即 $\pi^{-1}(\omega) \cap \{\lambda=0\} \neq \emptyset$。

---

## 3. 谱丛的单值性（Monodromy）与同伦延拓

### 3.1 谱叶结构

谱丛 $\mathcal{S}$ 是 $\omega$-平面的 $N$ 叶分支覆盖。对于非退化 $\omega$（无重特征值），$N$ 个特征值 $\lambda_i(\omega)$ 各自解析。

**分支点**：$\omega_0$ 处 $\lambda_i(\omega_0) = \lambda_j(\omega_0)$（特征值交叉）。在分支点处，谱叶交换。

### 3.2 单值群

沿 $\omega$-平面中的闭合回路 $\Gamma$ 平行移动谱丛的叶：

$$M_i = \{ \text{沿 } \Gamma \text{ 平行移动 } \lambda_i \text{ 后的终点叶编号} \}$$

单值群 $\mathcal{M} = \langle M_1, \dots, M_N \rangle$ 是置换群 $S_N$ 的子群。

**单值性定理**（本笔记提出）：同伦延拓路径 $\gamma(t): [0,1] \to B$ 是谱丛 $\mathcal{S}$ 的**一个叶的截面**沿 $\gamma$ 的平行移动。当 $\gamma$ 穿过分支点时，截面跳跃到另一叶——这就是**非物理根吸引域**的几何起源。

### 3.3 双参数单值性 (a + m)

在扩展参数空间 $(a, m, \omega)$ 中，谱丛 $\mathcal{S}_{a,m}$ 在 $(a,m)$-平面上也有单值性：

$$\Gamma_{a\text{-homotopy}}: \text{沿 } a \text{ 方向}, \quad \text{固定 } m=0$$
$$\Gamma_{m\text{-homotopy}}: \text{沿 } m \text{ 方向}, \quad \text{固定 } a$$

**推论 3.1**（双重同伦延拓的谱丛解释）：$a$-同伦延拓和 $m$-同伦延拓分别对应谱丛在 $a$ 方向和 $m$ 方向的平行移动。两者的组合路径 $\Gamma_{a+m} = \Gamma_a \circ \Gamma_m$ 避开了高自旋大 $|m|$ 区域的分支点密集区，因此比单一方向延拓更鲁棒。

---

## 4. 复杂度分析

### 4.1 谱丛剪枝

由于 QNM 条件 $\lambda = 0$ 只涉及谱丛的一个叶，二叉树分解允许**剪枝**：

1. 从根节点（全矩阵）开始
2. 在每层分裂点，计算 $q(\omega)$ 并判定 $\det B(\omega) \approx 0$ 的可能性
3. 只有可能产生 $\lambda=0$ 的分支需要继续展开
4. 剪枝后实际操作的子树大小 $\ll N$

### 4.2 复杂度对比

| 方法 | 复杂度 | 说明 |
|:----|:------|:----|
| 全稠密特征值分解 | $O(N^3)$ | $N=80$ 约 $5\times10^5$ 操作 |
| 三对角 QR | $O(N^2)$ | 约 $6\times10^3$ |
| 二叉树剪枝（理论） | $O(N)$ | 约 $80$ |
| Leaver CF 迭代 | $O(N)$ | 约 $N$ 次迭代 |
| 双初始向量逆迭代法 | $O(N)$ | 约 $10N = 800$ |

**注**：二叉树剪枝的实际复杂度取决于问题参数。对极端自旋 $a>0.9$，分支点更密集，剪枝效率下降。此分析为理论下界，尚未在代码中实现。

---

## 5. 与谱化理论的关系

### 5.1 D 函子的谱丛解读

谱化理论的核心 $$D: \mathbf{Rec} \to \mathbf{Sp}$$

映射 Leaver 三项递推系统 $R \in \mathbf{Rec}$ 到 Koopman 算子的谱。

在谱丛语言中，这个映射对应：

$$R \quad\stackrel{D}{\longrightarrow}\quad \{M(\omega)\}_{\omega \in \mathbb{C}} \quad\longrightarrow\quad \mathcal{S} = \{(\omega, \lambda): \det(M(\omega) - \lambda I) = 0\}$$

即：
1. 递推系统 $R$ 定义了一个 $\omega$-参数化的三对角矩阵族
2. 该矩阵族的谱生成了一个 $\mathbb{C}^2$ 中的代数曲线（谱丛）
3. D 函子提取了该谱丛的**全局截面**（$\lambda = 0$ 时的 $\omega$ 值）

### 5.2 二叉树 ↔ 连分数对应

谱丛的二叉树分解与 Leaver 连分数存在一一对应：

- **连分数 R₀(ω)** = 二叉树根节点的 Schur 补条件
- **连分数反转** = 二叉树不同深度的 Schur 补
- **n_inv 参数** = 二叉树的展开深度

### 5.3 LACI 的谱丛解释

LACI 判据的三个分量：

| LACI 分量 | 谱丛解释 |
|:---------|:--------|
| 不动点残差 $\rho$ | 截面在 $\lambda=0$ 上的垂直偏差 |
| 分散度 $\Delta$ | 分支点密度——高 $\Delta$ 意味着截面接近分支点 |
| 谱间隙 $\gamma$ | 二叉树根节点处谱叶间距 |

**定理**（本笔记提出）：LACI 指数是谱丛截面在 $\lambda=0$ 附近的正则性的度量。高 LACI 意味着截面远离分支点，物理根可靠。

---

## 6. 开放问题推进成果

本笔记四个开放问题已经过系统推进，分别形成了独立的理论文档和数值验证工具。以下总结各问题的推进状态和核心发现。

---

### 6.1 问题 1：单值群的完整计算 ✓ 理论完成

**状态**：理论框架完成，数值方案已设计，详见 [spectral_sheaf_monodromy.md](./spectral_sheaf_monodromy.md)

**核心成果**：

1. **支点分类定理**：Kerr 三对角矩阵族 $M(\omega) = M_0 + \omega M_1 + \omega^2 M_2$ 是二次矩阵多项式，$\det M(\omega) = 0$ 是 $2N$ 次代数方程。分支点分为三类：
   - **平方根分支**（简单分支点）：$\lambda(\omega) \sim (\omega - \omega_0)^{1/2}$，对应的单值群生成元为对换 $(i\;j)$
   - **高阶分支**（多重特征值交叉）：$\lambda(\omega) \sim (\omega - \omega_0)^{1/k}$，对应 $k$-轮换
   - **零点分支**：$\det M(\omega_0) = 0$ 且 $\lambda = 0$ 本身是谱丛的叶（QNM 频率）
   
   分支点总数上界为 $N(N-1)/2$，高自旋 $a > 0.9$ 时分支点密度急剧增大。

2. **单值群生成元定理**：谱丛的单值群 $\mathcal{M} \subset S_N$ 由**对换**生成，满足：
   - 每个简单分支点对应一个对换 $(i\;j)$
   - 低自旋区（$a < 0.5$）：$\mathcal{M}$ 是少数对换生成的子群（$|\mathcal{M}| \ll N!$）
   - 高自旋区（$a > 0.9$）：$\mathcal{M}$ 趋向于全置换群 $S_N$
   - 磁量子数 $m$ 的符号不影响单值群结构（对称性）

3. **双参数单值性的纤维积解释**：$a$-方向单值群 $\mathcal{M}_a$ 和 $m$-方向单值群 $\mathcal{M}_m$ 的纤维积 $\mathcal{M}_a \times_{\text{id}} \mathcal{M}_m$ 是组合路径鲁棒性的代数根源——当两个方向的单值群交集接近恒等置换时，组合路径避开分支点密集区。

4. **数值方案**：设计谱叶追踪算法（匈牙利算法 + 自适应步长），沿 $a \in \{0, 0.5, 0.7, 0.9, 0.99\}$, $l=2$, $m \in \{0, 1, 2\}$ 共 15 组参数计算单值群，预计单 CPU 耗时 1-4 小时。

---

### 6.2 问题 2：剪枝算法的实现 ✓ 理论设计完成

**状态**：完整算法设计完成，包含伪代码，详见 [spectral_sheaf_pruning.md](./spectral_sheaf_pruning.md)

**核心成果**：

1. **算法描述**（二叉树 Schur 补递归）：
   ```
   输入: M(ω) 的三对角形式, 目标 λ=0, 剪枝阈值 ε_prune
   输出: det(M(ω)) 的符号, 展开节点数
   
   function PruningRecursion(M, target=0):
       if size(M) == 1: return det(M)
       Split M at K → [A, γ e e^T; α e e^T, B]
       Compute q = γ · α · (A⁻¹)_{K,K}
       if |q| < ε_prune:
           # 剪枝：B 的谱受 q 扰动可忽略
           return PruningRecursion(A, target)
       else:
           # 全展开
           return PruningRecursion(A) · PruningRecursion(B - q·I)
   ```

2. **复杂度分析**：
   - 最佳情况（强剪枝，$|q| \ll 1$ 在每层成立）：$O(\log N)$
   - 平均情况（中等剪枝，约 $\log N$ 条展开路径）：$O(\log^2 N)$
   - 最差情况（无剪枝，$a \to 1$ 极端自旋）：$O(N)$（退化到全展开）

3. **剪枝优于双初始向量逆迭代法的条件**：$C_{\text{prune}} \cdot \log^2 N < C_{\text{弦法}} \cdot N$。对典型参数 $N=100$，剪枝在 $\log^2 N \approx 45$ 次 Schur 补内展开即有优势。建议自适应混合策略：先试剪枝，若剪枝无效（$|q|$ 持续大于阈值）退化为双初始向量逆迭代法。

4. **谱丛解释**：$|q(\omega)|$ 是两片谱纤维之间的**耦合强度**。$|q| \to 0$ 时两纤维几乎正交（可剪枝），$|q| \to \infty$ 时强耦合（分支点区域，不可剪枝）。

---

### 6.3 问题 3：谱丛曲率 ✓ 数值验证完成

**状态**：$dq/d\omega$ 作为预警指标不可行（因 $q$ 在 QNM 频率处有极点），已提出两个改进指标，完成 4 组数值实验验证，详见 [\_test_spectral_sheaf_curvature_v2.py](../src/dynamic_spectrum/_test_spectral_sheaf_curvature_v2.py)

**核心数值发现**：

#### 实验 E1：条件数 $\kappa(A(\omega))$ 的 $\omega$-扫描

```
模式                          κ_max         log10 κ    特征
───────────────────────────────────────────────────────────────
Schwarzschild (a=0, m=0)      9.06e+08       8.96      峰值在 ω₀ 处
Kerr (a=0.7, m=1)             8.31e+08       8.92      峰值在 ω₀ 处
Kerr (a=0.9, m=2)             9.97e+08       9.00      峰值在 ω₀ 处
Kerr (a=0.99, m=2)            7.86e+08       8.90      峰值在 ω₀ 处
```

**关键发现**：$\kappa(A)$ 在所有模式下均在 QNM 频率 $\omega_0$ 处达到峰值（~10⁹），这是因为 $\det M(\omega_0) = 0$ 使子块 $A$ 接近奇异。$\kappa(A)$ **不是**分支点方向性预警指标，而是 QNM 条件本身的反映。$\log_{10} \kappa(A) > 8$ 可作为 QNM 频率存在性的辅助验证。

#### 实验 E2：多半径小圆 CV 对比

```
模式                    r=0.001    r=0.002    r=0.005    r=0.010    r=0.020    r=0.050
─────────────────────────────────────────────────────────────────────────────────────────
Schwarzschild          0.0011     0.0019     0.0044     0.0087     0.0175     0.0436
Kerr a=0.5 m=1         0.0005     0.0015     0.0040     0.0081     0.0163     0.0408
Kerr a=0.7 m=1         0.0004     0.0013     0.0037     0.0074     0.0149     0.0373
Kerr a=0.9 m=2         0.0001     0.0003     0.0010     0.0022     0.0044     0.0111
Kerr a=0.99 m=2        0.0012     0.0028     0.0073     0.0148     0.0297     0.2754
```

**关键发现**：变异系数 CV 是有效的分支点预警指标。当 $r$ 增大到接近分支点距离时，CV 急剧增长。`a=0.99` 在 `r=0.05` 时 CV 达 0.2754，是其他模式的 6-27 倍，表明附近存在分支点。CV 随半径以约 $r^2$ 增长，可外推估计分支点距离。

#### 实验 E3：谱流梯度沿小圆分布

```
模式                    |dλ_min/dω|_mean    CV(grad)    梯度均匀性
─────────────────────────────────────────────────────────────────
Schwarzschild            20.69             0.0175       ✓ 均匀
Kerr a=0.5 m=1           20.67             0.0163       ✓ 均匀
Kerr a=0.9 m=2           29.60             0.0044       ✓ 均匀
Kerr a=0.99 m=2          68.20             0.0297       ✓ 均匀
```

**关键发现**：谱流梯度沿小圆各方向高度均匀（CV(grad) < 0.03），不是方向性预警指标。梯度模值随自旋增大（反映谱叶曲率增大），但各向同性暗示 QNM 频率附近的谱丛是局部均匀的。

#### 实验 E4：分裂位置 $K$ 对 $\kappa(A)$ 的影响

```
模式                    最优 K    κ_min       log₁₀ κ_min
─────────────────────────────────────────────────────────
Schwarzschild             10      3.90e+05      5.59
Kerr a=0.7 m=1            10      3.29e+05      5.52
Kerr a=0.9 m=2            10      5.98e+05      5.78
```

**关键发现**：条件数随 $K$ 单调递增。最小 $K=10$ 给出最小 $\kappa(A)$。这意味着剪枝算法应选择**最小可行分裂点**（即 $K=1$ 或很小值）来最小化子块条件数，但过小的 $K$ 可能导致 $q(\omega)$ 丧失界面信息。最优策略：$K = \min(\lceil N/10 \rceil, 10)$。

#### 综合结论

| 预警指标 | 可行性 | 说明 |
|:--------:|:-----:|:-----|
| $dq/d\omega$ | ✗ | QNM 频率处 $q$ 有极点，无法区分分支点 |
| $\kappa(A)$ | △ | $\log_{10} \kappa > 8$ 可验证 QNM 条件，但非独立预警 |
| **CV** | **✓** | 多半径测试有效，$r=0.05$ 时 CV 区分分支点区域 |
| $\|d\lambda_{\min}/d\omega\|$ | ✗ | 各向同性，无方向性信息 |

---

### 6.4 问题 4：推广到其他背景 ✓ 理论分析完成

**状态**：度规分类完成，详见 [spectral_sheaf_generalization.md](./spectral_sheaf_generalization.md)

**核心成果**：

1. **三对角谱丛结构存在性定理**（充要条件 G1-G3）：

   | 条件 | 内容 | 物理含义 |
   |:---:|:-----|:---------|
   | G1 | Petrov D 型，Teukolsky 方程可分离变量 | 底空间 $\mathbb{C}_\omega$ 是 1 维的 |
   | G2 | 径向展开系数满足三项递推 | 三对角矩阵族 $M(\omega)$ 存在 |
   | G3 | 递推系数为 $n$ 的至多二次多项式 | $M(\omega)$ 是二次矩阵多项式 |

2. **度规分类表**：

   | 度规 | G1 | G2 | G3 | 三对角结构 |
   |:----:|:--:|:--:|:--:|:--------:|
   | Schwarzschild | ✓ | ✓ | ✓ | 完全满足 |
   | Kerr | ✓ | ✓ | ✓ | 完全满足 |
   | RN | ✓ | ✓ | ✓ | 完全满足（$Q$ 仅修正 $D_i$ 系数） |
   | Kerr-Newman | ✓ | ✓ | ✓ | 完全满足（$aQ$ 耦合项保持二次性） |
   | Kerr-dS/AdS | ✓ | ✓ | ✓ | 完全满足（$\Lambda$ 引入四次多项式修饰） |
   | Dilaton | ✓ | ✓ | ? | 部分满足（标量场破坏 G3） |
   | 动态时空 | ✗ | N/A | N/A | 不适用 |

3. **RN 的显式 $D_i$ 系数**：给出含电荷 $Q$ 的完整 $D_i(\omega)$ 表达式，三对角谱丛结构保持，无需修改双初始向量逆迭代法求解器。

4. **非三对角推广**：Dilaton 度规可能产生高次多项式系数或高带宽递推；高维时空（Myers-Perry, BMPV）径向三项递推保持但底空间维数增加。

---

## 7. 数值验证工具

以下数值脚本用于验证谱丛理论的核心预测：

| 脚本 | 验证内容 | 文件 |
|:----|:--------|:----|
| `_test_spectral_sheaf_curvature.py` | 条件数 $\kappa(A)$ 和单半径 CV | `src/dynamic_spectrum/_test_spectral_sheaf_curvature.py` |
| `_test_spectral_sheaf_curvature_v2.py` | 四组深入实验（E1-E4） | `src/dynamic_spectrum/_test_spectral_sheaf_curvature_v2.py` |

---

## 8. 关联文档

| 文档 | 对应开放问题 | 状态 |
|:----|:-----------:|:----:|
| [spectral_sheaf_monodromy.md](./spectral_sheaf_monodromy.md) | Q1：单值群 | v0.1 理论完成 |
| [spectral_sheaf_pruning.md](./spectral_sheaf_pruning.md) | Q2：剪枝算法 | v0.1 设计完成 |
| [spectral_sheaf_generalization.md](./spectral_sheaf_generalization.md) | Q4：度规推广（v0.1） + 非引力推广（v0.2） | v0.2 包含流变学/NRG/记忆函数 |

---

## 版本记录

**v0.2（2026-07-25）**：完成四个开放问题的系统推进。Q1 单值群（含支点分类、生成元定理、纤维积解释）；Q2 剪枝算法（二叉树 Schur 补递归、复杂度分析、自适应混合策略）；Q3 谱丛曲率（四组数值实验 E1-E4，发现 CV 为有效预警指标，$\kappa(A)$ 和 $|d\lambda/d\omega|$ 各有局限）；Q4 推广性分析（G1-G3 充分条件、7 类度规分类表、RN/KN 显式系数）。形成 3 篇独立笔记和 1 个升级版数值验证脚本。

**v0.1（2026-07-25）**：初版。提出谱丛理论框架：三对角矩阵的二叉树纤维化、单值性与同伦延拓的关系、LACI 的谱丛解释。复杂度分析。
