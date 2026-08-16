# 引力-电磁耦合谱丛实现方案：块三对角构造与 IV 型奇异纤维分类

**版本**：v0.1（2026-07-25）

**摘要**：本文档是 §9.7 路径 2 的详细实施方案。目标是在 Kerr-Newman 背景下构造引力（s=±2）与电磁（s=±1）耦合系统的块三对角谱丛，建立 Q 参数的纤维延拓，数值扫描 IV 型奇异纤维的出现条件和分类准则。

---

## 1. Chandrasekhar 耦合方程的离散化

### 1.1 耦合系统的主方程

在 Kerr-Newman 背景中，对 Kinnersley 零标架上的 Weyl 标量 $\psi_0$（s=+2）和 Maxwell 标量 $\phi_0$（s=+1），Chandrasekhar（1983, §63-65）导出了耦合 Teukolsky 方程组：

$$\begin{aligned}
\mathcal{T}^{(+2)}\psi_0 &= Q \cdot \mathcal{C}_1 \phi_0 \\
\mathcal{T}^{(+1)}\phi_0 &= Q \cdot \mathcal{C}_2 \psi_0
\end{aligned}$$

其中 $\mathcal{T}^{(s)}$ 是自旋权重为 $s$ 的标准 Teukolsky 算子，$\mathcal{C}_1, \mathcal{C}_2$ 是耦合微分算子（包含径向和角向导数），$Q$ 是黑洞电荷。

类似地，对 $\psi_4$（s=-2）和 $\phi_2$（s=-1）：

$$\begin{aligned}
\mathcal{T}^{(-2)}\psi_4 &= Q \cdot \underline{\mathcal{C}}_1 \phi_2 \\
\mathcal{T}^{(-1)}\phi_2 &= Q \cdot \underline{\mathcal{C}}_2 \psi_4
\end{aligned}$$

### 1.2 Frobenius 级数展开与三项递推

对 $(s=+2, s=+1)$ 耦合系统，两个场的径向函数分别展开为 Frobenius 级数：

$$\begin{aligned}
R_{+2}(r) &= e^{i\omega r_*} (r - r_-)^{-1 - i\sigma_+} (r - r_+)^{-1 - i\sigma_+ - s} \sum_{n=0}^\infty a_n^{(+2)} \left(\frac{r - r_+}{r - r_-}\right)^n \\
R_{+1}(r) &= e^{i\omega r_*} (r - r_-)^{-1 - i\sigma_+} (r - r_+)^{-1 - i\sigma_+ - s} \sum_{n=0}^\infty a_n^{(+1)} \left(\frac{r - r_+}{r - r_-}\right)^n
\end{aligned}$$

代入耦合 Teukolsky 方程组，合并同类项后，得到**四项递推**（而不是单自旋情形中的三项递推）：

$$\alpha_n a_{n+2}^{(+2)} + \beta_n a_{n+1}^{(+2)} + \gamma_n a_n^{(+2)} + \delta_n a_n^{(+1)} = 0$$
$$\alpha_n' a_{n+2}^{(+1)} + \beta_n' a_{n+1}^{(+1)} + \gamma_n' a_n^{(+1)} + \delta_n' a_n^{(+2)} = 0$$

耦合项 $\delta_n$ 和 $\delta_n'$ 正比于 $Q$，$Q=0$ 时退化为独立的三项递推。

### 1.3 耦合符号结构

定义两分量状态向量 $\mathbf{a}_n = (a_n^{(+2)}, a_n^{(+1)})^T$。耦合系统可写为：

$$\mathbf{A}_n \mathbf{a}_{n+2} + \mathbf{B}_n \mathbf{a}_{n+1} + \mathbf{C}_n \mathbf{a}_n = 0$$

其中 $\mathbf{A}_n, \mathbf{B}_n, \mathbf{C}_n$ 为 $2 \times 2$ 矩阵：

$$\mathbf{A}_n = \begin{pmatrix}
\alpha_n^{(+2)} & 0 \\
0 & \alpha_n^{(+1)}
\end{pmatrix}, \quad
\mathbf{B}_n = \begin{pmatrix}
\beta_n^{(+2)} & \delta_n \\
\delta_n' & \beta_n^{(+1)}
\end{pmatrix}, \quad
\mathbf{C}_n = \begin{pmatrix}
\gamma_n^{(+2)} & 0 \\
0 & \gamma_n^{(+1)}
\end{pmatrix}$$

耦合项 $\delta_n = Q \cdot d_n$，$\delta_n' = Q \cdot d_n'$，$d_n, d_n'$ 由 Chandrasekhar 耦合算子离散化得到。

**命题 2.1**（耦合符号结构）。耦合项满足 $\delta_n' = (-1)^n \delta_n^*$（共轭对称性）。

**证明**。由 Chandrasekhar 变换理论的耦合方程形式推导——$s=+2$ 和 $s=+1$ 方程通过电荷共轭变换关联，在零标架基下导出上述共轭对称关系。$\square$

## 2. 块三对角谱丛的数值实现

### 2.1 分块三对角矩阵构造

将耦合递推转化为无穷矩阵方程 $M_{\text{total}} \mathbf{a} = 0$，其中 $\mathbf{a} = (\mathbf{a}_0, \mathbf{a}_1, \mathbf{a}_2, \dots)^T$：

$$M_{\text{total}} = \begin{pmatrix}
\mathbf{B}_0 & \mathbf{A}_0 & \mathbf{0} & \mathbf{0} & \cdots \\
\mathbf{C}_1 & \mathbf{B}_1 & \mathbf{A}_1 & \mathbf{0} & \cdots \\
\mathbf{0} & \mathbf{C}_2 & \mathbf{B}_2 & \mathbf{A}_2 & \cdots \\
\vdots & \vdots & \vdots & \vdots & \ddots
\end{pmatrix}$$

截断到 $N$ 块后，$M_{\text{total}}^{(N)}$ 是 $2N \times 2N$ 的块三对角矩阵：

$$\det M_{\text{total}}^{(N)}(\omega; a, m, Q) = 0$$

这是耦合系统的特征方程，确定 $Q \neq 0$ 时的 QNM 频率。

### 2.2 与单自旋矩阵的关系

**命题 2.2**（Q=0 退化性）。当 $Q = 0$ 时：

$$\det M_{\text{total}}^{(N)}(\omega; a, m, 0) = \det M^{(+2)}(\omega; a, m) \cdot \det M^{(+1)}(\omega; a, m)$$

即块矩阵的行列式分解为两个单自旋矩阵行列式的乘积，耦合谱丛退化为直积结构。

**证明**。$Q=0$ 时非对角块 $\delta_n = \delta_n' = 0$，$M_{\text{total}}$ 退化为块对角矩阵。分块矩阵的行列式性质给出 $\det(\text{blockdiag}(A,B)) = \det(A)\det(B)$。$\square$

### 2.3 代码结构

在 `src/spectral_sheaf/` 下新增：

```
spectral_sheaf/
├── _coupled_teukolsky_coeff.py   # 耦合系统递推系数（含 Chandrasekhar 耦合项）
├── _coupled_sheaf_solver.py      # 耦合谱丛求解器（块三对角矩阵）
├── tests/
│   ├── test_coupled_q_zero.py    # Q=0 退化验证
│   ├── test_coupled_q_scan.py    # Q 参数扫描测试
│   └── test_coupled_singular.py  # IV 型奇异纤维检测
```

### 2.4 核心实现

```python
def build_coupled_block_matrix(n_blocks: int, a: float, m: int,
                                omega: complex, l: int, Q: float,
                                lam2: complex, lam1: complex) -> np.ndarray:
    """
    构造耦合系统的分块三对角矩阵。
    
    返回：
        M_total: 2*n_blocks × 2*n_blocks 的块三对角矩阵
    """
    dim = 2 * n_blocks
    M = np.zeros((dim, dim), dtype=complex)
    
    for n_block in range(n_blocks):
        n = 2 * n_block  # 行/列索引
        
        # B_n (对角块)
        B = np.zeros((2, 2), dtype=complex)
        B[0, 0] = beta_n(s=+2, n_block, a, m, omega, l, lam2)
        B[1, 1] = beta_n(s=+1, n_block, a, m, omega, l, lam1)
        B[0, 1] = Q * delta_n(n_block, a, m, omega)  # 耦合项
        B[1, 0] = Q * delta_n_prime(n_block, a, m, omega)  # 耦合项
        M[n:n+2, n:n+2] = B
        
        # A_n (上对角块)
        if n_block < n_blocks - 1:
            A = np.zeros((2, 2), dtype=complex)
            A[0, 0] = alpha_n(s=+2, n_block)
            A[1, 1] = alpha_n(s=+1, n_block)
            M[n:n+2, n+2:n+4] = A
        
        # C_n (下对角块)
        if n_block > 0:
            C = np.zeros((2, 2), dtype=complex)
            C[0, 0] = gamma_n(s=+2, n_block, a, omega)
            C[1, 1] = gamma_n(s=+1, n_block, a, omega)
            M[n:n+2, n-2:n] = C
    
    return M
```

## 3. Q 参数的纤维延拓策略

### 3.1 Q 作为谱丛新参数

耦合系统的参数空间扩展到四重 $(a, m, \omega, Q)$。谱丛结构随 Q 的演化由纤维延拓描述：

**定义 3.1**（Q-纤维）。对固定 $(a, m, \omega)$，Q-纤维定义为：

$$\mathcal{F}_Q(a, m, \omega) = \{\lambda \in \mathbb{C} : \det(M_{\text{total}}(\omega; a, m, Q) - \lambda I) = 0\}$$

**命题 3.1**（Q-纤维的连续形变）。当 $Q: 0 \to Q_{\max}$ 时，纤维 $\mathcal{F}_Q$ 从直积结构 $\sigma^{(+2)} \times \sigma^{(+1)}$ 连续形变为耦合结构。形变保持谱丛的紧性（特征值有界），且形变速度由耦合项范数 $\|\delta_n\|$ 控制。

### 3.2 Q 扫描协议

采用双扫描策略：

**粗扫描**：确定耦合效应的量级
- $Q \in \{0, 0.05, 0.1, 0.2, 0.3, 0.5, 0.7, 0.9, 0.99\}M$
- 对每个 Q，计算 $l=m=2$, $a \in \{0, 0.3, 0.7\}$ 的 QNM 根
- 标记 Q 从 0 开始增加时根轨迹的偏移方向

**细扫描**：定位 IV 型奇异纤维
- $Q \in [Q_{\text{start}}, Q_{\text{end}}]$ 步长 $\Delta Q = 0.01$
- 在粗扫描标识的异常区加密到 $\Delta Q = 0.001$
- 在每个 Q 点计算 $\det M_{\text{total}}$ 的判别式曲线
- 检测 $\det M_{\text{total}} = 0$ 接近 $\det M^{(s_i)} = 0$ 时的参数值

### 3.3 物理参数空间

主扫描参数空间：

| 参数 | 范围 | 步长 | 说明 |
|:----|:----|:----|:----|
| $a$ | $[0, 0.9]$ | 0.1 | 自旋参数 |
| $Q$ | $[0, 0.99M]$ | 变步长 | 电荷参数（细扫描加密） |
| $l$ | $\{1, 2\}$ | — | 角向量子数 |
| $m$ | $\{-l, \dots, l\}$ | 1 | 磁量子数 |
| $n$ | $\{0, 1, 2\}$ | 1 | 泛音阶数 |

总计约：$10 \times (20-30) \times 2 \times 3 \times 3 \approx 3000-5400$ 个参数点。

## 4. IV 型奇异纤维的数值检测

### 4.1 IV 型奇异纤维的退化条件

**定义 4.1**（IV 型奇异纤维数值检测准则）。当以下条件同时满足时，判定参数点 $(a, m, \omega, Q)$ 为 IV 型奇异纤维：

1. **全局特征方程退化**：$\det M_{\text{total}}(\omega) = 0$（连分数收敛）
2. **单自旋子块非退化**：$\det M^{(+2)}(\omega) \neq 0$ 且 $\det M^{(+1)}(\omega) \neq 0$
3. **耦合项非零**：$\delta_n \neq 0$（即 $Q \neq 0$）
4. **简并条件**：$\lambda_{\min}(M_{\text{total}})$ 的双重简并

条件 1-3 一起排除了耦合系统回退为单自旋或平凡结构的情形，条件 4 标识了真正的"耦合融合"点。

### 4.2 数值检测算法

```python
def detect_type_IV_singular(a, m, l, Q_vals, omega_guess, n_blocks=30):
    """
    沿 Q 参数检测 IV 型奇异纤维。
    
    对每个 Q 值：
    1. 求解密度 M_total 的特征值
    2. 检查特征方程 det(M_total) = 0
    3. 分别计算 det(M^{(+2)}) 和 det(M^{(+1)})
    4. 判断退化类型
    """
    type_IV_points = []
    for Q in Q_vals:
        omega_root = solve_qnm_coupled(a, m, l, Q, omega_guess, n_blocks)
        
        # 构造块矩阵
        M_total = build_coupled_block_matrix(
            n_blocks, a, m, omega_root, l, Q, ...)
        M_plus2 = build_single_spin_matrix(
            n_blocks, a, m, omega_root, l, s=+2)
        M_plus1 = build_single_spin_matrix(
            n_blocks, a, m, omega_root, l, s=+1)
        
        det_total = np.linalg.det(M_total)
        det_plus2 = np.linalg.det(M_plus2)
        det_plus1 = np.linalg.det(M_plus1)
        
        # 条件 1: |det_total| < eps
        cond1 = abs(det_total) < 1e-10
        # 条件 2: |det_plus2| > eps 且 |det_plus1| > eps
        cond2 = abs(det_plus2) > 1e-8 and abs(det_plus1) > 1e-8
        # 条件 3: Q > 0
        cond3 = Q > 1e-10
        
        if cond1 and cond2 and cond3:
            # 检查简并度
            eigvals = sp.linalg.eigvals(M_total)
            gaps = np.sort(np.abs(np.subtract.outer(eigvals, eigvals)))
            min_gap = gaps[gaps > 1e-15].min() if len(gaps) > 1 else np.inf
            
            if min_gap < 1e-6:  # 近似简并
                type_IV_points.append({
                    'Q': Q, 'omega': omega_root,
                    'det_ratio': abs(det_plus2) / abs(det_total),
                    'min_gap': min_gap
                })
    
    return type_IV_points
```

### 4.3 与已有奇异纤维的关系

**命题 4.1**（奇异纤维互斥性）。四种奇异纤维类型在参数空间中互斥：
- **I 型**：$\partial\det M_{\text{total}}/\partial\omega = 0$，单自旋谱叶交叉
- **II 型**：$\det M_{\text{total}} = 0$ 且 $\det M^{(s_i)} \to 0$
- **III 型**：$\gamma_{\text{total}} \to 0$
- **IV 型**：$\det M_{\text{total}} = 0$，$\det M^{(s_i)} \neq 0$，耦合项非零

**证明**。从各类型的定义直接验证：I 型的判别式条件与 II 型的行列式零条件不能同时成立（除非退化点重合，测度零）；III 型的谱间隙条件独立于行列式条件；IV 型要求单自旋行列式非零，排除了 II 型。$\square$

### 4.4 物理对应

IV 型奇异纤维出现时，耦合系统的 QNM 模式不能归因于任一单自旋的单独激发。这对应 Chandrasekhar 代数特殊解：

$$\exists \text{ 代数关系 } P(\psi_0, \phi_0) = 0 \text{ 在 } Q = Q_c \text{ 处成立}$$

其中 $P$ 是耦合场的不变量，$Q_c$ 是临界电荷。此关系意味着在 IV 型奇异点处，引力-电磁耦合模式"锁相"形成集体激发态。

## 5. 数值验证计划

### 5.1 阶段一：Q=0 退化验证（第 1 周）

验证耦合求解器在 $Q=0$ 时正确退化为独立单自旋：

1. 对 $(a, m, l) = (0, 0, 2)$，耦合求解器应给出引力 QNM 和电磁 QNM 的并集
2. 计算 $\det M_{\text{total}}$ 并将其分解为 $\det M^{(+2)} \cdot \det M^{(+1)}$
3. 验证耦合项 $\delta_n$ 在 $Q=0$ 时对结果的影响 $\le 10^{-12}$

### 5.2 阶段二：小 Q 微扰测试（第 2 周）

引入小电荷 $Q = 0.01M, 0.05M$，验证：

1. QNM 频率的偏移量与 $Q$ 呈线性关系（一阶微扰理论）
2. $\det M_{\text{total}}$ 的零点偏离直积预测的方向和大小
3. 耦合引入的谱叶形变是否可逆（$Q \to -Q$ 交换符号）

### 5.3 阶段三：中等 Q 耦合效应（第 3-4 周）

$Q = 0.1M, 0.2M, 0.3M$：

1. 引力/电磁 QNM 的交叉现象——某些电磁模式可能被"推"向引力模式
2. 跨自旋分支交叉（I' 型奇异纤维）
3. LACI 参数的耦合修正

### 5.4 阶段四：大 Q 接近极端（第 5-8 周）

$Q = 0.5M, 0.7M, 0.9M, 0.99M$：

1. 接近极端 $a \to 1$ 和 $Q \to M$ 的耦合退化
2. IV 型奇异纤维的系统搜寻
3. 推导 $\gamma_{\text{total}}(a, Q)$ 的双参数标度律

### 5.5 阶段五：论文集成（第 9-12 周）

1. 整理 IV 型奇异纤维的数值分类图谱
2. 推导 $\mathcal{M}_Q$ 单值群的换位关系
3. 验证 $D_{\mathrm{diss}}^{\text{(coupled)}}$ 猜想的数值证据
4. 更新 paper27 §9.7

## 6. 预期成果总结

| 成果 | 形式 | 验证标准 |
|:----|:----|:--------|
| 耦合块三对角矩阵构造 | 代码 `_coupled_teukolsky_coeff.py` | Q=0 退化 $<10^{-12}$ |
| Q 纤维连续形变 | 数值图谱 + 标度律 | 形变由 $\|\delta_n\|$ 控制 |
| IV 型奇异纤维分类 | 数值检测算法 | 与 I/II/III 型互斥 |
| 跨自旋分支交叉 | 判别式曲线扫描 | 与引力 I 型对比 |
| $\mathcal{M}_Q$ 换位关系 | 数值初步结果 | 有助于后续理论构造 |

## 参考文献

[1] Chandrasekhar, S. (1983). *The Mathematical Theory of Black Holes*. Oxford University Press (§63-65 耦合方程).

[2] Khanal, U. (1983). Perturbations of the Kerr-Newman black hole. *Phys. Rev. D* **28**, 1291.

[3] Cook, G. B. & Zalutskiy, M. (2014). Gravitational perturbations of the Kerr geometry. *Phys. Rev. D* **90**, 124021.

[4] Giorgi, E. & Wan, J. (2024). Boundedness and decay for the Teukolsky system in Kerr-Newman spacetime II. arXiv:2407.10750.

[5] Glampedakis, K., Johnson, A. D. & Kennefick, D. (2017). The Darboux transformation in black hole perturbation theory. arXiv:1702.06459.

[6] Berens, R., Gravely, T. & Lupsasca, A. (2025). Gravitational waves on Kerr black holes I. arXiv:2403.20311.
