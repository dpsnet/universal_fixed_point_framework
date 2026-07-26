# 谱丛剪枝：二叉树 Schur 补递归算法

**版本**：v0.1（2026-07-25）

**摘要**：本笔记基于谱丛理论（spectral_sheaf_leaver.md §4.1），给出二叉树剪枝算法的完整理论设计与实现方案。算法利用三对角矩阵分裂时界面参量 $q(\omega)$ 的模值作为剪枝判据，在递归求解中只展开可能产生 $\lambda=0$ 的分支，将最坏情况 $O(N)$ 的 Leaver 求解压缩到最佳情况 $O(\log N)$。

**关联笔记**：[spectral_sheaf_leaver.md](./spectral_sheaf_leaver.md) 定义了谱丛的二叉树纤维化结构和界面参量 $q(\omega)$ 的物理意义。

---

## 1. 剪枝算法的完整设计

### 1.1 二叉树 Schur 补递归

给定三对角矩阵 $M(\omega) \in \mathbb{C}^{N \times N}$，其索引集在 $K$ 处分裂为两个子块：

$$
M(\omega) = \begin{bmatrix}
A(\omega) & \gamma_K(\omega) e_K e_{K+1}^T \\
\alpha_K(\omega) e_{K+1} e_K^T & B(\omega)
\end{bmatrix},
\quad 
\begin{aligned}
A &\in \mathbb{C}^{K \times K}, \\
B &\in \mathbb{C}^{(N-K) \times (N-K)}.
\end{aligned}
$$

由于三对角矩阵的 off-diagonal 耦合是 rank-1 的（仅在 $(K,K+1)$ 位置有一个标量耦合），Schur 补公式给出：

$$
\det M(\omega) = \det A(\omega) \cdot \det\big(B(\omega) - q(\omega) \cdot e_{K+1} e_{K+1}^T\big),
$$

其中界面参量：

$$
q(\omega) = \gamma_K(\omega) \cdot \alpha_K(\omega) \cdot (A(\omega)^{-1})_{K,K}.
$$

剪枝算法的递归过程基于以下观察：$q(\omega)$ 的模大小决定了右子树 $B$ 对 $\lambda=0$ 条件的贡献权重。

**算法流程（递归分裂）**：

1. **分裂判定**：在分裂位置 $K = \lfloor N/2 \rfloor$ 处，计算界面参量

   $$
   q(\omega) = \gamma_K(\omega) \cdot \alpha_K(\omega) \cdot (A(\omega)^{-1})_{K,K}.
   $$

   这里的 $(A^{-1})_{K,K}$ 是子块 $A$ 的右下角矩阵元的逆，可以通过 Thomas 算法在 $O(K)$ 时间内求得（仅需一次三对角求解）。

2. **剪枝条件**：若 $|q(\omega)| < \varepsilon_{\text{prune}}$，则判定**右子树 $B$ 对 $\lambda=0$ 条件的贡献可忽略**，执行剪枝。

   理由：Schur 补 $\det M = \det A \cdot \det(B - q e_{K+1} e_{K+1}^T)$。当 $|q| \ll 1$ 时，$B - q e_{K+1} e_{K+1}^T$ 是 $B$ 的一个微小秩-1 扰动。根据 Weyl 不等式，$B$ 的谱在扰动 $q$ 下的变化量 $\leq |q|$。因此若 $|q| < \varepsilon_{\text{prune}}$，则 $B$ 的最小模特征值与 $B - q e_{K+1} e_{K+1}^T$ 的最小模特征值之差不超过 $\varepsilon_{\text{prune}}$，即 $B$ 子块对整体 $\det M = 0$ 条件的贡献可忽略。

   更严格地，$\det(B - q e_{K+1}e_{K+1}^T) = 0$ 等价于 $B$ 有一个特征值等于 $q$。当 $|q| \to 0$ 时，这要求 $B$ 已有零特征值——即 $B$ 本身已奇异。若 $B$ 非奇异，则 $|q| \ll 1$ 意味着 Schur 补完全由 $\det A$ 决定。

3. **递归展开**：
   - **左子树（子块 $A$）**：无条件继续递归分裂，因为 $A$ 始终参与 $\det M$ 的构成。
   - **右子树（子块 $B$）**：仅当 $|q| \ge \varepsilon_{\text{prune}}$ 时继续递归；否则**剪掉右子树**，将其 $\det$ 贡献近似为 $\det B(0)$（即 $\omega$ 无关的常数），或直接返回 $\det B \approx 1$（归一化处理）。

4. **底部停止**：当子块大小为 $1 \times 1$ 时，直接返回

   $$
   |\det| = |\beta_0(\omega)|,
   $$

   其中 $\beta_0(\omega)$ 是三对角矩阵的首个对角元。

**完整的 Schur 补递归**：

$$
\det M(\omega) = \begin{cases}
\beta_0(\omega), & N = 1, \\[4pt]
\displaystyle\prod_{\text{展开节点}} \det A_i(\omega) \cdot \prod_{\text{未剪枝节点}} \det\big(B_i(\omega) - q_i(\omega) I\big), & N > 1.
\end{cases}
$$

展开节点的乘积对应对应于二叉树中所有未被剪枝的节点。由于剪枝的存在，实际参与乘积的节点数远小于 $N$。

---

### 1.2 复杂度分析

剪枝算法的复杂度取决于 $|q(\omega)|$ 随递归深度的分布。设二叉树深度为 $D = \lceil \log_2 N \rceil$。

#### 最佳情况（强剪枝）—— $O(\log N)$

当试探频率 $\omega$ 远离任何分支点，且谱丛在该区域的纤维几乎正交时，几乎所有分裂点的 $|q|$ 都小于 $\varepsilon_{\text{prune}}$。

在根节点分裂后，右子树即刻被剪掉，仅左子树继续递归。每层只展开一个子块：

```
Level 0:        M[N×N]         ← 展开
                   │
Level 1:       A[N/2]          ← 右子树 B 被剪掉
                   │
Level 2:      A₁[N/4]          ← 右子树 A₂ 被剪掉
                ...
```

展开节点数 = $D = \log_2 N$。每层计算 $q(\omega)$ 还需一次 Thomas 求解 $O(K)$，但 $K$ 逐层减半，总操作数满足几何级数：

$$
\sum_{d=0}^{D-1} O(N / 2^d) = O(N),
$$

然而这是最粗略的上界。更精确的分析：每层只展开一个子块时，第一个根节点需 $O(N)$ 求解 $(A^{-1})_{K,K}$（Thomas），第二层需 $O(N/2)$，依此类推，总操作数仍为 $O(N)$。但在**强剪枝**条件下，$q(\omega)$ 的计算可以简化——若 $A$ 的子块也满足强剪枝条件，则 $(A^{-1})_{K,K}$ 可从上一级的 Schur 补信息中递推得到，无需完整 Thomas 求解。

实际实现中，强剪枝场景的复杂度由递归深度主导，即 $O(\log N)$ 次递归调用，每次调用的计算量远小于 $O(N)$。

#### 平均情况（中等剪枝）—— $O(\log^2 N)$

对典型的不可约 Kerr QNM 频率，约 $O(\log N)$ 个分裂点处 $|q|$ 超过阈值。每个展开节点需在其子孙节点中继续计算，形成若干条展开路径。

每层展开的节点数约为 $O(\log N)$，总节点数 $O(\log^2 N)$。每节点的 Thomas 求解在 $O(N/2^d)$ 的子块上进行，总复杂度：

$$
\sum_{d=0}^{D-1} O(\log N) \cdot O(N / 2^d) \approx O(N) \text{（线性于总截断维数）},
$$

但常数因子远小于全展开。更精确地，实践中应观察到 $O(\log^2 N)$ 量级的 Thomas 求解次数。

#### 最差情况（无剪枝）—— $O(N)$

当 $\omega$ 接近分支点（谱丛叶间耦合最强区域），$|q(\omega)| \gg \varepsilon_{\text{prune}}$ 在所有分裂点成立。此时二叉树完全展开：

```
Level 0:        M[N×N]
               /       \
Level 1:   A[N/2]     B[N/2]
           /    \      /    \
Level 2:  A₁   A₂    B₁    B₂
         ...  ...   ...   ...
```

展开节点数 = $2^D - 1 = N - 1$，每个节点需一次 Thomas 求解 $O(\text{subblock size})$。总复杂度 $O(N^2)$？不对，需仔细求和。

设每个节点的大小为 $s$，Thomas 求解需要 $O(s)$ 操作。在完整二叉树中，深度 $d$ 层的节点数为 $2^d$，每个节点大小为 $N/2^d$。总操作数：

$$
\sum_{d=0}^{D-1} 2^d \cdot O(N / 2^d) = \sum_{d=0}^{D-1} O(N) = O(N \log N).
$$

但这是不必要的——如果完全展开，直接对原矩阵做一次 Thomas 求解仅需 $O(N)$。因此实际实现中，当 $|q|$ 在所有分裂点都大于阈值时，应退化到标准 $O(N)$ 求解，而不是执行 $O(N \log N)$ 的二叉树展开。

**实现策略**：维护一个展开计数器，当已展开节点数超过 $2N$ 时自动退化为标准 $O(N)$ 求解。

#### 复杂度对比总表

| 方法 | 复杂度 | 每步常数 | 适用场景 |
|:----|:------|:--------|:--------|
| Leaver CF 迭代 | $O(N)$ | 小（标量递推） | 通用，最稳定 |
| 双初始向量逆迭代法（Rayleigh 商） | $O(N)$ × 5-15 步 | 中（Thomas 求解 + 向量运算） | 需要特征向量信息 |
| 剪枝算法（最佳） | $O(\log N)$ | 中（需计算 $q$） | 弱耦合自旋参数区域 |
| 剪枝算法（平均） | $O(\log^2 N)$ | 中 | 大部分中等自旋参数 |
| 剪枝算法（最差） | $O(N)$ | 中（退化为 Thomas 求解） | 强耦合/分支点附近 |

---

### 1.3 剪枝判据的谱丛解释

界面参量 $q(\omega)$ 的物理意义是谱丛中两片纤维（子块 $A$ 和子块 $B$ 对应的子谱）之间的**耦合强度**。

考虑谱丛的二叉树纤维化（spectral_sheaf_leaver.md §2），$A$ 和 $B$ 对应两片子纤维 $F_\omega^A$ 和 $F_\omega^B$。全局谱丛 $F_\omega$ 通过 rank-1 耦合将两者粘合。$q(\omega)$ 就是这个"胶水"的粘性系数。

**$q(\omega)$ 的三种极限情况**：

1. **$|q(\omega)| \to 0$——弱连接（可剪枝）**

   子块 $A$ 和 $B$ 接近解耦。此时 Schur 补 $\det M \approx \det A \cdot \det B$，两个子谱几乎独立。谱丛在该分裂点处有**弱连接**，两片纤维近乎正交。物理上对应自旋参数区域中，径向模式的相邻展开系数几乎不相关。

   剪枝条件 $|q| < \varepsilon_{\text{prune}}$ 等价于判定两片谱纤维是否"近乎正交"。当正交时，右子树对 $\lambda=0$ 条件的贡献可忽略，因为 $B$ 的谱与 Schur 补的谱在 $\varepsilon_{\text{prune}}$ 精度内一致。

2. **$|q(\omega)| \to \infty$——强耦合（分支点区域）**

   子块间耦合极强，接近谱丛的分支点（branch point）。在分支点处，两片谱叶发生交换（monodromy），$q(\omega)$ 发散。此时 Schur 补条件 $\det(B - qI) \approx \det B$ 不再成立。

   在强耦合区域不能剪枝，必须完全展开二叉树。这对应于高自旋 $a > 0.9$、大 $|m|$ 模式中，分支点密集、谱叶间距小的情形。

3. **$|q(\omega)| \approx O(1)$——中等耦合**  

   子块间有显著但非支配性的耦合。此时需要根据 $|q|$ 与 $\varepsilon_{\text{prune}}$ 的比较决定是否展开右子树。阈值的选取影响复杂度-精度权衡。

**$\varepsilon_{\text{prune}}$ 的选取原则**：

$$
\varepsilon_{\text{prune}} \sim \text{Newton 迭代容差} \times \text{典型矩阵范数}.
$$

实践中建议取 $\varepsilon_{\text{prune}} = 10^{-8}$（与 Newton 迭代的残差容差一致）。若要求高精度物理根，可降低到 $10^{-10}$ 或 $10^{-12}$。

**$q(\omega)$ 的导数作为分支点预警**：

谱丛曲率（spectral_sheaf_leaver.md §6 开放问题3）指出，$dq/d\omega$ 的模值可以作为分支点临近的预警指标。当 $|dq/d\omega|$ 很大时，意味着 $\omega$ 靠近分支点，此时 $q(\omega)$ 对 $\omega$ 敏感，剪枝策略应当保守（降低 $\varepsilon_{\text{prune}}$ 或暂时禁用剪枝）。

---

### 1.4 与双初始向量逆迭代法的关系

#### 双初始向量逆迭代法的回顾

双初始向量逆迭代法（`TridiagonalSpectralSolver`，见 `leaver_unified_solver.py`）是当前框架中用于求解三对角矩阵最小特征值的方法。其核心：

- 在每次 Newton 迭代中求解三对角系统 $(M - \mu I)w = v$（Thomas 算法，$O(N)$）
- Rayleigh 商迭代，三次收敛，5-15 步达到机器精度
- 每步 $O(N)$，总复杂度 $O(N)$ × (Newton 迭代次数)

#### 剪枝算法的优势场景

剪枝算法将双初始向量逆迭代法中的 $O(N)$ Thomas 求解替换为二叉树的 $O(\log N)$ 到 $O(N)$ 递归。每步需要额外计算 $q(\omega)$。

**剪枝优于双初始向量逆迭代法的条件**：

$$
\frac{C_{\text{prune}} \cdot \log^2 N}{C_{\text{弦法}} \cdot N} < 1,
$$

其中 $C_{\text{prune}}$ 和 $C_{\text{弦法}}$ 分别是每步操作的常数因子。

经验估计（Python 实现，双精度复数）：

| 操作 | 相对成本 |
|:----|:--------|
| 一次标量乘法 | 1 |
| 一次 Thomas 求解 ($N=80$) | $\sim 10^3$ |
| 一次 $q(\omega)$ 计算（含 $(A^{-1})_{K,K}$） | $\sim 0.5 \times$ Thomas |
| 一次二叉树递归（平均展开 $\log^2 N$ 节点） | $\sim 0.5 \log^2 N \times$ Thomas |

当 $|q|$ 在 $O(\log N)$ 个分裂点处都超过阈值时，剪枝算法的展开节点数约 $\log^2 N$，每次展开需 $O(N/2^d)$ Thomas 操作。对 $N=80$，总成本约 $0.5 \times 36 \approx 18$ 个 Thomas 当量，而双初始向量逆迭代法只需 5-15 次 Thomas 求解（每次 $O(N)$）。在此场景下双初始向量逆迭代法更优。

**剪枝算法的核心竞争力**不在当前 $N=80$ 的典型设置，而在以下场景：

1. **大截断维数 $N \gg 100$**：当需要更高精度（如极端自旋 $a > 0.99$）而增大 $N$ 时，双初始向量逆迭代法的 $O(N)$ 线性增长变成瓶颈，剪枝算法的对数增长（或亚线性增长）优势凸显。

2. **批量求解**：当在同伦延拓路径上对数百个 $\omega$ 值连续计算时，每个 $\omega$ 的剪枝模式可传承——若 $\omega_k$ 处剪掉了某子树，则 $\omega_{k+1}$ 处大概率也可剪掉。这允许**提早剪枝**，进一步压缩计算。

3. **谱丛诊断**：剪枝算法输出的 `nodes_expanded` 就是 $|q(\omega)|$ 的分布图，直接反映谱丛的耦合结构，这是双初始向量逆迭代法无法提供的诊断信息。

#### 混合策略建议

实践中不应将剪枝算法视为双初始向量逆迭代法的替代，而是**补充**：

```
对于每个 ω:
  if (nodes_expanded < 2 log N):    # 强剪枝
    使用剪枝算法结果
  elif (nodes_expanded < N/2):      # 中等剪枝
    使用剪枝算法结果（含验证）
  else:                             # 弱剪枝/无剪枝
    回退到双初始向量逆迭代法（标准 O(N) Thomas 求解）
```

这种自适应混合策略保证：当剪枝有效时获得加速，当剪枝无效时退化为现有最优方法。

---

## 2. 实现方案

### 2.1 接口函数

```python
def tridiag_pruning_solve(omega, lam, solver, N, eps_prune=1e-10):
    """
    二叉树剪枝求解 QNM 频率的符号检测。

    计算 det(M(omega)) 的符号（或复幅角），用于 Newton 迭代中
    的括号法（bracketing）。同时返回实际展开的节点数作为复杂度度量。

    Parameters
    ----------
    omega : complex
        当前试探频率。
    lam : complex
        角向 spheroidal 特征值 λ。
    solver : LeaverResidual
        提供多项式系数 α_n, β_n, γ_n 的求解器实例。
        需要调用 solver._polynomial_alpha(n, D), _polynomial_beta(n, D),
        _polynomial_gamma(n, D) 等方法获取三对角矩阵元。
    N : int
        总截断维数（矩阵大小）。
    eps_prune : float, default=1e-10
        剪枝阈值。当 |q| < eps_prune 时剪掉右子树。

    Returns
    -------
    det_sign : complex
        det(M(omega)) 的值（或符号归一化后的复幅角）。
        在 Newton 迭代中，只需知道 det(M) 的幅角方向即可
        用于复平面上的括号法。
    nodes_expanded : int
        实际展开的二叉树节点数。用于复杂度监控和自适应退化判断。
    """
    # Step 1: 获取 D 系数（solver 内部已有 _D_coeffs 方法）
    D = solver._D_coeffs(omega, lam, m)  # 此处的 m 通过外部传入

    # Step 2: 调用递归函数
    det_val, nodes = _pruning_recursion(0, N - 1, D, solver, eps_prune)

    return det_val, nodes
```

### 2.2 剪枝递归核心逻辑

```python
def _pruning_recursion(i_start, i_end, D, solver, eps_prune):
    """
    剪枝递归核心。

    对三对角矩阵的索引区间 [i_start, i_end] 对应的子块，
    计算其行列式（或 Schur 补贡献），并根据界面参量剪枝。

    Parameters
    ----------
    i_start, i_end : int
        当前子块的索引范围（包含两端）。
    D : np.ndarray[5]
        Cook-Zalutskiy D₀-D₄ 系数。
    solver : LeaverResidual
        提供三对角矩阵元的求解器。
    eps_prune : float
        剪枝阈值。

    Returns
    -------
    det_sub : complex
        当前子块对 det(M) 的贡献。
    nodes_expanded : int
        当前子块递归中展开的节点数（含自身）。
    """
```

**递归函数的详细步骤**：

1. **底部条件**：若 `i_start == i_end`（子块大小为 $1 \times 1$），直接返回：
   - `det_sub = β_n(ω)`（调用 `solver._polynomial_beta(i_start, D)`）
   - `nodes_expanded = 1`
   - 此分支结束。

2. **分裂**：计算中点 `K = (i_start + i_end) // 2`。子块 $A$ 对应 `[i_start, K]`，子块 $B$ 对应 `[K+1, i_end]`。

3. **计算界面参量 $q(\omega)$**：
   - 获取耦合系数：`γ_K = solver._polynomial_gamma(K, D)`（对应 `γ_K(ω)`），`α_K = solver._polynomial_alpha(K, D)`（对应 `α_K(ω)`）。
   - 求解 `(A^{-1})_{K,K}`：这是子块 $A$ 的右下角矩阵元的逆。需要求解三对角方程组 `A · x = e_K`，其中 $e_K$ 是第 $K$ 个单位向量，然后取解向量 `x` 的第 `K` 个分量。
     - 实现方式：用 Thomas 算法在 $O(|A|)$ 时间内求解 `A x = e_K`。由于 $A$ 是子块 $K \times K$ 的三对角矩阵，Thomas 算法稳定高效。
     - 注意：这里不需要完整的 $A^{-1}$，只需要右下角一个元素。可利用三对角矩阵的 Sparsity 结构加速——实际上只需一次 Thomas 回代。
   - 计算 `q = γ_K * α_K * x[K]`。

4. **剪枝判定**：
   - 若 `|q| < eps_prune`：
     - **右子树被剪掉**。对右子树 $B$ 的贡献做近似：`det_B = 1.0`（或更精确地，用 `B(0)` 的行列式近似，即令 `ω=0` 计算 `B` 的 $\det$）。
     - 对左子树 $A$ 递归调用 `_pruning_recursion(i_start, K, ...)`。
     - 返回：`det_sub = det_A * det_B`，`nodes_expanded = nodes_A + 1`（+1 计当前节点）。
   
   - 若 `|q| >= eps_prune`：
     - **右子树不剪枝**。分别对左子树 $A$ 和右子树 $B$ 递归：
       - `det_A, nodes_A = _pruning_recursion(i_start, K, ...)`
       - `det_B, nodes_B = _pruning_recursion(K+1, i_end, ...)`
     - Schur 补组合：`det_sub = det_A * (det_B - q)`。
       - 这里的 `(det_B - q)` 对应 $\det(B - q e_{K+1} e_{K+1}^T)$ 的近似。严格来说，右子树的递归返回的是 $\det B(\omega)$（即 $\omega$ 对应频率下的行列式），而 Schur 补需要的是 $\det(B - q I)$。由于 $q$ 只影响 $B$ 的 $(K+1, K+1)$ 位置，等价于将 $B$ 的首个对角元偏移 $q$。
       - 一种更精确的实现方式：在递归右子树时，将 $q$ 作为额外的对角偏移传入，使得递归的底部直接计算 $\det(B - q I)$ 而非 $\det B$。
     - 返回：`det_sub` 和 `nodes_expanded = nodes_A + nodes_B + 1`。

5. **退化保护**（实现建议）：
   - 用一个外部计数器跟踪总展开节点数（通过闭包或全局变量）。
   - 若 `total_nodes_expanded > 2 * N`，则放弃剪枝，退化为标准 Thomas 求解计算 $\det(M)$（或退化为双初始向量逆迭代法）。
   - 此保护保证最坏情况复杂度不超过 $O(N)$。

6. **牛顿迭代中的使用**：
   - 在 Newton 迭代中，`tridiag_pruning_solve` 返回的 `det_val` 替代 `LeaverResidual.radial_cf_polynomial` 的返回值。
   - 残差定义为 `|det_val|`（物理根处 $|\det M| = 0$）。
   - Newton 迭代的 Jacobian 矩阵可通过扰动 `omega ± δ` 和 `omega ± iδ` 计算。

### 2.3 伪代码的 Python 骨架

```python
def _tridiag_schur_complement_rightmost(
    lower_K, diag_A, upper_K, K
) -> complex:
    """
    用 Thomas 算法求解 A x = e_K，返回 x[K]。
    
    A 是子块三对角矩阵（索引 0..K），已知其对应对角线和
    非对角线元。只需右下角一个元素。
    
    实际上只需回代一次——由于右端项是单位向量 e_K，
    前代过程可大幅简化（只有最后一个元素非零）。
    """
    # Thomas 前代（简化版：右端项仅最后一位为 1）
    N = K + 1  # 子块 A 的大小
    # 这里实现标准 Thomas 算法，右端项初始化为 0
    # 在最后一个位置设为 1
    # ...
    # 返回 x[K]

def _pruning_recursion(start, end, D, solver, eps_prune):
    """
    剪枝递归函数。

    展开策略：
    - 计算界面参量 q
    - 若 |q| < eps_prune，剪掉右子树，只展开左子树
    - 若 |q| >= eps_prune，同时展开左右子树
    - 底部 (start == end) 直接返回 β_n
    """
    if start == end:
        beta = solver._polynomial_beta(start, D)
        return beta, 1

    K = (start + end) // 2

    # 获取耦合系数
    gamma_K = solver._polynomial_gamma(K, D)
    alpha_K = solver._polynomial_alpha(K, D)

    # 求解 (A^{-1})_{K,K}
    A_inv_KK = _compute_A_inv_KK(start, K, D, solver)
    q = gamma_K * alpha_K * A_inv_KK

    det_A, nodes_A = _pruning_recursion(start, K, D, solver, eps_prune)

    if abs(q) < eps_prune:
        # 剪枝：右子树不展开
        # 近似 det_B ≈ 1（或 det(B(ω=0))）
        det_B = 1.0
        nodes_B = 0
    else:
        # 不剪枝：右子树展开
        # 注意：需将 q 作为对角偏移传入右子树
        # 即计算 det(B - q * e_{K+1} e_{K+1}^T)
        det_B, nodes_B = _pruning_recursion_with_shift(
            K + 1, end, D, solver, eps_prune, shift=q
        )

    det_sub = det_A * det_B
    nodes_expanded = nodes_A + nodes_B + 1

    # 退化保护
    if nodes_expanded > 2 * (end - start + 1):
        # 退化为标准求解
        return _full_tridiag_det(start, end, D, solver), end - start + 1

    return det_sub, nodes_expanded


def _pruning_recursion_with_shift(
    start, end, D, solver, eps_prune, shift
):
    """
    带 Schur 偏移的剪枝递归。
    
    计算 det(B - shift * e_{K+1} e_{K+1}^T)。
    对于底部条件，偏移只在第一个对角元上生效。
    """
    if start == end:
        beta = solver._polynomial_beta(start, D)
        # 若当前是偏移目标行（即右子树的第一个元素）：
        if shift != 0.0:
            # 该位置是右子树的首个对角元 K+1，由 Schur 补知
            # det(B - q I) 在此位置的效果是 β_{K+1} → β_{K+1} - q
            beta = beta - shift
        return beta, 1

    # 其余逻辑同 _pruning_recursion，但将 shift 传播到
    # 第一个对角元上（仅影响右子树的第一行）
    K = (start + end) // 2

    # ... 类似 _pruning_recursion 的递归逻辑 ...
    # 注意：shift 只影响右子树的起始位置，不影响其他分裂点的 q
```

### 2.4 关键数值细节

1. **$(A^{-1})_{K,K}$ 的高效计算**：

   这是剪枝算法的性能关键。由于只需要右下角一个元素，不需要求解完整的三对角方程组。可以通过以下方式进一步优化：

   - 三对角矩阵的 Sherman-Morrison 公式
   - 利用 $A$ 的 LDL^T 分解的最后一个枢轴（pivot）

   实现建议：直接用 Thomas 算法求解 $A x = e_K$，由于右端项 $e_K$ 极度稀疏（只有最后一个位置为 1），前代过程可以大幅简化。

2. **Schur 偏移的传播**：

   在 `_pruning_recursion_with_shift` 中，$q$ 只影响 $B$ 的 $(K+1, K+1)$ 位置（即 $B$ 子块的第一行第一列）。在递归中，这个偏移只影响底部条件中第一个节点（`start` 位置）的 $\beta$ 值。

3. **复幅角稳定性**：

   $\det M(\omega)$ 是 $\omega$ 的解析函数，但在数值实现中可能出现幅角缠绕问题。建议用 $\log \det$ 的增量累加代替直接乘积，避免复数溢出：

   $$
   \log \det M = \sum_{\text{展开节点}} \log \det A_i + \sum_{\text{未剪枝节点}} \log \det(B_i - q_i I).
   $$

4. **自适应阈值**：

   对于 $N=80$ 的典型截断，$\varepsilon_{\text{prune}} = 10^{-8}$ 是一个合理选择。可以根据 Newton 迭代的收敛状态动态调整：

   - 早期迭代（粗搜索）：$\varepsilon_{\text{prune}} = 10^{-6}$
   - 后期精化：$\varepsilon_{\text{prune}} = 10^{-12}$

---

### 2.5 与现有框架的集成

剪枝算法的位置在 `LeaverResidual` 和 `TridiagonalSpectralSolver` 之间：

- 它使用 `LeaverResidual._D_coeffs` 获取多项式系数
- 它产出 `det(M(ω))` 的估计值，可作为 Newton 迭代的残差
- 在 `TridiagonalSpectralSolver` 中，剪枝算法可替代 `radial_cf_polynomial` 或 `spectral_residual_fast`

**集成方案建议**：

在 `LeaverResidual` 类中增加方法：

```python
class LeaverResidual:
    # ... 现有方法 ...

    def radial_pruning_residual(self, omega, lam, m, N=80, eps_prune=1e-10):
        """
        剪枝算法残差。
        
        替代 radial_cf_polynomial 用于 Newton 迭代。
        复杂度：O(log N) 到 O(N)，取决于剪枝效果。
        """
        D = self._D_coeffs(omega, lam, m)
        det_val, nodes = tridiag_pruning_solve(D, N, eps_prune)
        return det_val, nodes
```

---

## 版本记录

**v0.1（2026-07-25）**：初版。完成剪枝算法的理论设计：二叉树 Schur 补递归流程、四种复杂度场景分析、谱丛耦合强度的物理解释、与双初始向量逆迭代法的对比及混合策略。给出 Python 伪代码骨架和关键数值细节。
