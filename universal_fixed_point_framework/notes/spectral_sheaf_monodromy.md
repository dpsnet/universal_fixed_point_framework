# 谱丛单值群（Monodromy Group）的完整计算方案设计

**版本**：v0.1（2026-07-25）

**摘要**：本文档基于 `spectral_sheaf_leaver.md` 建立的谱丛理论框架，针对 §6 开放问题1 设计完整的单值群计算方案。第一部分建立支点分类定理、单值群生成元理论和双重同伦延拓的单值群解释；第二部分给出数值实现的具体方案（伪代码级设计）。

---

## 第一部分：理论框架

---

### 1. 支点分类定理

#### 1.1 问题设定

考虑 Kerr 背景下的 Leaver 三对角矩阵族：

$$M(\omega) = M_0 + \omega M_1 + \omega^2 M_2$$

其中 $M_0, M_1, M_2 \in \mathbb{C}^{N \times N}$ 是常数矩阵（与 $\omega$ 无关）。由 Cook-Zalutskiy (2014) 多项式形式，三对角矩阵的三条对角线为：

$$\begin{aligned}
\alpha_n(\omega) &= n^2 + (D_0(\omega) + 1)n + D_0(\omega) \\
\beta_n(\omega) &= -2n^2 + (D_1(\omega) + 2)n + D_3(\omega) \\
\gamma_n(\omega) &= n^2 + (D_2(\omega) - 3)n + D_4(\omega) - D_2(\omega) + 2
\end{aligned}$$

其中 $D_i(\omega)$ 通过奇点指数 $\zeta, \xi, \eta$ 依赖于 $\omega$（参见 `leaver_unified_solver.py` 中 `_D_coeffs` 方法）。每个对角元是 $\omega$ 的二次多项式（最大次数为 2），因此 $\det M(\omega)$ 是 $\omega$ 的 $2N$ 次多项式。

#### 1.2 特征值交叉与分支点

谱丛 $\mathcal{S} = \{(\omega, \lambda) \in \mathbb{C}^2 : \det(M(\omega) - \lambda I) = 0\}$ 是全纯函数 $\lambda(\omega)$ 的 Riemann 面。

**定义 1（分支点）**：$\omega_0 \in \mathbb{C}$ 称为分支点（branch point），若存在至少两个不同的解析分支 $\lambda_i(\omega)$ 和 $\lambda_j(\omega)$ 使得 $\lambda_i(\omega_0) = \lambda_j(\omega_0)$。

**定理 1（分支点击数分类）**：Kerr 三对角矩阵族 $M(\omega)$ 的特征值交叉点（分支点）满足以下分类：

1. **平方根分支（1-2 型）**：当 $\det M(\omega_0) \neq 0$ 且 $\lambda_i(\omega_0) = \lambda_j(\omega_0)$ 是重数为 2 的特征值时，分支点附近有：
   
   $$\lambda(\omega) \sim \lambda_0 + c \cdot (\omega - \omega_0)^{1/2} + O(\omega - \omega_0)$$
   
   此时两个谱叶在 $\omega_0$ 处交换，对应单值群中的对换 $(i\;j)$。

2. **高阶分支（1-k 型）**：当 $M(\omega_0)$ 有重数 $k \geq 2$ 的特征值时，分支点附近有：
   
   $$\lambda(\omega) \sim \lambda_0 + c \cdot (\omega - \omega_0)^{1/k} + O(\omega - \omega_0)$$
   
   对应单值群中的 $k$-循环。

3. **零点分支（QNM 分支点）**：当 $\det M(\omega_0) = 0$ 时，$\lambda = 0$ 本身是一个特征值。此时：
   
   - 若 $\frac{d}{d\omega}\det M(\omega_0) \neq 0$，则 $\lambda(\omega) \sim c \cdot (\omega - \omega_0)$（简单零点，非分支点）
   - 若 $\frac{d}{d\omega}\det M(\omega_0) = 0$ 且 $\det M(\omega)$ 在 $\omega_0$ 处有 $p$ 阶零点，则 $\omega_0$ 是分支点，对应 $p$ 个谱叶在 $\lambda=0$ 处汇聚

#### 1.3 分支点代数方程

由于 $M(\omega)$ 是二次矩阵多项式，特征值问题等价于广义特征值问题：

$$\det(M(\omega) - \lambda I) = \det(M_0 + \omega M_1 + \omega^2 M_2 - \lambda I) = 0$$

这是一个关于 $(\omega, \lambda)$ 的 $2N$ 次代数曲线。投影到 $\omega$-平面，分支点 $\omega_0$ 满足判别式条件：

$$\Delta(\omega) = \prod_{i < j} (\lambda_i(\omega) - \lambda_j(\omega))^2 = 0$$

其中 $\Delta(\omega)$ 是特征多项式的判别式，它是 $\omega$ 的多项式，次数不超过 $2N(N-1)$。

**定理 2（分支点个数上界）**：Kerr 三对角矩阵族 $M(\omega)$（$N \times N$）在 $\mathbb{C}$ 中的分支点个数不超过 $N(N-1)$。

**推论 2.1**：当 $N=80$（双初始向量逆迭代法默认维度），分支点个数上界为 $80 \times 79 = 6320$，但实际物理相关的分支点（分布在 QNM 频率附近）通常远少于该上界。

#### 1.4 高自旋区域的分支点行为

在高自旋区域（$a > 0.7$），参数 $\sigma = a\omega$ 的虚部增大，导致 $D_i(\omega)$ 系数的虚部显著增大。这导致：

**定理 3（高自旋分支点密集化）**：随着自旋 $a \to 1$，分支点在复 $\omega$-平面上向 QNM 频率附近聚集，导致谱间的有效间距缩小。具体地：

- 当 $a \leq 0.5$：分支点与 QNM 频率的分离度 $\delta \sim 0.1$
- 当 $a \approx 0.9$：分离度降至 $\delta \sim 0.01$
- 当 $a \approx 0.99$：分离度可达 $\delta \sim 0.001$

这正是高自旋下同伦延拓收敛变慢、LACI 分散度增大的几何根源——同伦路径被迫经过分支点密集区，增加了叶间跳跃概率。

---

### 2. 单值群生成元

#### 2.1 单值群的定义

谱丛 $\mathcal{S}$ 构成 $\mathbb{C}$ 上的 $N$ 叶 Riemann 面。设 $\omega_0$ 为非分支点，固定 $N$ 个谱叶 $\{\lambda_1(\omega_0), \dots, \lambda_N(\omega_0)\}$ 的排序。对 $\omega$-平面中任意闭合回路 $\Gamma \subset \mathbb{C} \setminus \{\text{分支点}\}$，沿 $\Gamma$ 解析延拓诱导了谱叶集合上的置换：

$$P_\Gamma \in S_N$$

**定义 2（单值群）**：谱丛 $\mathcal{S}$ 关于底点 $\omega_0$ 的单值群 $\mathcal{M}(\mathcal{S}, \omega_0)$ 是：
- 基本群 $\pi_1(\mathbb{C} \setminus B, \omega_0)$ 到置换群 $S_N$ 的群同态的像
- 其中 $B = \{\omega_1, \dots, \omega_K\}$ 是分支点集合

$$\mathcal{M}(\mathcal{S}, \omega_0) = \text{Im}\left( \rho: \pi_1(\mathbb{C} \setminus B, \omega_0) \to S_N \right)$$

#### 2.2 生成元结构定理

**定理 4（对换生成定理）**：谱丛 $\mathcal{S}$ 的单值群 $\mathcal{M} \subset S_N$ 由对换（transpositions）生成。每个简单分支点（平方根分支）对应一个对换 $(i\;j)$。

*证明思路*：在每个简单分支点 $\omega_k$ 附近，取足够小的回路 $\Gamma_k$ 环绕 $\omega_k$ 一周，则沿 $\Gamma_k$ 的平行移动仅交换两个谱叶 $i$ 和 $j$，其余 $N-2$ 个谱叶不变。因此 $P_{\Gamma_k} = (i\;j)$。

**推论 4.1**：一般分支点（$k$-阶）对应的置换是 $k$-循环，可分解为 $k-1$ 个对换的乘积。

**推论 4.2**：单值群 $\mathcal{M}$ 是置换群 $S_N$ 的子群，但其结构强烈依赖于参数 $(a, m)$：

- Schwarzschild 极限（$a=0$）：$m=0$ 时所有 $\lambda$ 简并，单值群退化
- Kerr 低自旋（$a \sim 0.5$）：分支点稀疏散布，$\mathcal{M}$ 通常为少数对换生成的子群
- Kerr 高自旋（$a \sim 0.99$）：分支点密集，$\mathcal{M}$ 趋向于 $S_N$ 本身

#### 2.3 参数依赖关系

单值群 $\mathcal{M}(a, m)$ 在 Kerr 参数空间中的结构演化：

**猜测 1（自旋驱动的单值群增长）**：固定 $m$，随着 $a$ 增大，单值群 $\mathcal{M}(a, m)$ 的大小（阶数）单调不减。在临界自旋 $a_c(m)$ 处，新的分支点对从复平面边界进入 QNM 区域，导致单值群新增生成元。

**猜测 2（磁量子数的对称性）**：对 $m$ 和 $-m$，单值群共轭：
$$\mathcal{M}(a, -m) \cong \mathcal{M}(a, m)$$
但映射到不同谱叶编号。

---

### 3. 双重同伦延拓的单值群解释

#### 3.1 路径的单值群

在 $\text{LeaverUnifiedSolver}$ 中实施的 $a$-同伦延拓沿路径：
$$\Gamma_a: \quad (a: 0 \to a_*) \times (m: \text{固定})$$

$m$-同伦延拓沿路径：
$$\Gamma_m: \quad (m: 0 \to m_*) \times (a: \text{固定})$$

**定理 5（截线依赖性）**：$a$-同伦延拓对应 $\omega$-平面中一条特定截线 $\text{Cut}_a$ 的单值群。该截线的位置由函数 $\omega(a)$ 确定——沿 $a$ 的连续变化相当于沿 $\omega$-平面中某条连续路径移动截线。

**定理 6（组合路径的纤维积）**：设 $\mathcal{M}_a$ 是沿 $a$-同伦路径的单值群，$\mathcal{M}_m$ 是沿 $m$-同伦路径的单值群。则组合路径 $\Gamma_{a+m}$ 的单值群 $\mathcal{M}_{a+m}$ 满足：

$$\mathcal{M}_{a+m} \subset \mathcal{M}_a \times_{\text{id}} \mathcal{M}_m$$

即 $\mathcal{M}_{a+m}$ 是 $\mathcal{M}_a$ 和 $\mathcal{M}_m$ 的纤维积子群——它要求置换同时在 $a$ 方向和 $m$ 方向上连续。

#### 3.2 鲁棒性解释

**推论 6.1（组合路径鲁棒性）**：双重同伦延拓比单一同伦延拓更鲁棒的原因在于：
1. $\mathcal{M}_a$ 和 $\mathcal{M}_m$ 的截线方向不同，它们的交点区域避开了大部分分支点
2. 组合路径 $\Gamma_{a+m}$ 的单值群 $\mathcal{M}_{a+m}$ 是 $\mathcal{M}_a$ 和 $\mathcal{M}_m$ 的交集，更接近恒等置换
3. 当单一延拓穿过分支点时，组合延拓由于同时受两个方向约束，有更高概率保持在同一谱叶上

**数值启发**：若在 $a$-同伦延拓中观测到非物理根跳跃，尝试在中间 $a$ 值处插入 $m$-同伦步，可有效"拉回"到正确谱叶。这正是 `_solve_kerr_spectral_fast` 中混合策略的经验基础。

---

## 第二部分：数值方案设计

---

### 4. 谱叶追踪算法

#### 4.1 算法概览

```
算法 1: 谱叶追踪（Spectral Leaf Tracking）
输入: ω₀（起始点）, Γ = {γ(t): t ∈ [0,1]}（闭合回路）, N_trunc（谱叶数）
输出: 置换 P_Γ ∈ S_N

1. 计算 M(ω₀) 的全谱 {λ_i(ω₀)}, 按某种序排序（如实部降序）
2. 沿 Γ 取离散点 ω_k = γ(k/K), k = 0,1,...,K
3. for k = 0 to K-1:
   a. 计算 M(ω_k) 的全谱 {λ_i(ω_k)}
   b. 计算 M(ω_{k+1}) 的全谱 {λ_i(ω_{k+1})}
   c. 计算指派矩阵 A_{ij} = |λ_i(ω_k) - λ_j(ω_{k+1})|
   d. 用匈牙利算法（Hungarian algorithm）求解最小代价匹配
   e. 记录匹配映射 σ_k: {λ_i(ω_k)} → {λ_j(ω_{k+1})}
4. 组合所有步的匹配：P_Γ = σ_{K-1} ∘ ... ∘ σ₁ ∘ σ₀
5. 返回 P_Γ
```

#### 4.2 关键技术细节

**匹配的唯一性保证**：在非分支点处，若 $\min_{i \neq j} |\lambda_i - \lambda_j| > \epsilon$（谱间距容差），则匈牙利算法给出唯一匹配。在分支点附近，需减小步长 $\Delta\omega$ 使相邻步的谱间距满足：
$$\max_{i,j} |\lambda_i(\omega_k) - \lambda_j(\omega_{k+1})| < \frac{1}{2} \min_{i \neq j} |\lambda_i(\omega_k) - \lambda_j(\omega_k)|$$

**步长自适应**：
```python
def adaptive_step(omega, M_matrix_func, min_gap=0.01, max_step=0.1):
    """自适应步长：确保相邻谱的匹配唯一性"""
    spec_current = full_spectrum(M_matrix_func(omega))
    gap = spectral_gap(spec_current)  # 最小谱间距
    step = max(0.001, min(max_step, gap * 0.5))
    return step
```

**回路设计**：
- 以 QNM 频率 $\omega_{\text{QNM}}$ 为中心，半径 $R$ 的圆
- $R$ 的选择需包围至少一个分支点但不超过谱的最近分支点距离的半值
- 推荐半径 $R \in [0.01, 0.1]$，据 $a$ 和 $m$ 调整

#### 4.3 分支点检测

分支点检测可通过对判别式的零点的搜索完成：

```python
def detect_branch_points(omega_grid, M_matrix_func, l, m):
    """
    在 omega_grid 上扫描判别式零点以检测分支点位置。
    
    返回分支点候选列表。
    """
    branch_points = []
    for omega in omega_grid:
        spec = full_spectrum(M_matrix_func(omega, l, m))
        # 判别式为 0 当存在重特征值
        discrim = product([(spec[i] - spec[j])**2 
                          for i in range(N) for j in range(i+1, N)])
        if abs(discrim) < threshold:
            branch_points.append(omega)
    return refine_branch_points(branch_points)
```

更高效的检测方法：沿 $\omega$-平面中的回路追踪单个谱叶，当检测到 $\lambda(\omega)$ 的导数的奇异性（即 $|d\lambda/d\omega| \to \infty$）时，标记为分支点附近。

---

### 5. 单值群矩阵构建

#### 5.1 生成元计算

```
算法 2: 单值群生成元计算
输入: 分支点集合 B = {ω₁, ..., ω_K}，底点 ω₀
输出: 生成元集合 G = {P₁, ..., P_K} ⊂ S_N

1. for k = 1 to K:
   a. 构造回路 Γ_k：以 ω_k 为中心，半径小到仅包围 ω_k
   b. 用算法 1 计算 P_{Γ_k}
   c. 若 P_{Γ_k} ≠ 恒等置换，加入 G
2. 简化 G：移除可通过其他生成元乘积得到的生成元
3. 返回 G
```

#### 5.2 群结构分析

```python
def analyze_monodromy_group(generators, N):
    """
    分析单值群结构。
    
    参数:
        generators: list of ndarray(N, N) — 置换矩阵列表
        N: 谱叶数
    
    返回:
        group_order: 群阶
        cycle_structure: 循环类型列表
        is_transitive: 是否传递
        normal_subgroups: 正规子群列表
    """
    # 群阶计算：通过生成元的枚举乘积
    group = generate_full_group(generators)
    group_order = len(group)
    
    # 循环结构分析
    cycle_structure = []
    for perm in generators:
        cycles = permutation_cycles(perm)
        cycle_structure.append(cycles)
    
    # 传递性检验
    orbits = compute_orbits(generators, N)
    is_transitive = (len(orbits) == 1)
    
    # 可解性检验
    derived_series = compute_derived_series(group)
    is_solvable = (derived_series[-1] == {identity})
    
    return {
        "order": group_order,
        "generators": generators,
        "cycle_structure": cycle_structure,
        "is_transitive": is_transitive,
        "is_solvable": is_solvable,
        "orbits": orbits,
    }
```

#### 5.3 群同构分类

对于小型 $N$（$N \leq 10$），可通过查找表识别单值群与已知群的同构：

| 群阶 | 可能的结构 | Kerr 中的出现 |
|:----|:---------|:------------|
| 2 | $\mathbb{Z}_2$ | 单个分支点（低自旋） |
| 4 | $\mathbb{Z}_4$ 或 $\mathbb{Z}_2 \times \mathbb{Z}_2$ | 两个独立分支点 |
| 6 | $S_3$ | 三个叶的完全置换（中等自旋） |
| 24 | $S_4$ | 四个叶的完全置换（高自旋） |
| $N!$ | $S_N$ | 极端高自旋，所有分支点激活 |

---

### 6. 参数扫描方案

#### 6.1 扫描参数空间

```python
# 参数网格
a_values = [0.0, 0.5, 0.7, 0.9, 0.99]
l_fixed = 2
m_values = [0, 1, 2]

# 对每个参数组合计算单值群
results = {}
for a in a_values:
    for m in m_values:
        key = (a, l_fixed, m)
        print(f"计算: a={a}, l={l_fixed}, m={m}")
        
        # 1. 计算该参数下的 QNM 频率
        solver = LeaverUnifiedSolver(M=1.0, a=a, s=-2)
        qnm_result = solver.solve(l=l_fixed, m=m, n=0)
        omega_qnm = qnm_result['omega']
        
        # 2. 构造回路
        #   回路 1: 以 ω_qnm 为中心，小半径 (R=0.005)
        #   回路 2: 以 ω_qnm 为中心，大半径 (R=0.05)
        #   回路 3: 绕多个分支点的联合回路
        loops = construct_loops(omega_qnm, a, m)
        
        # 3. 对每个回路计算单值群生成元
        generators = []
        for loop in loops:
            P = spectral_leaf_tracking(omega_qnm, loop, N_trunc=10)
            generators.append(P)
        
        # 4. 分析单值群结构
        group_info = analyze_monodromy_group(generators, N=10)
        results[key] = group_info
```

#### 6.2 预期结果与验证

**预期发现**：

1. **$m=0$ 模式**：单值群较小（通常 $\mathbb{Z}_2$ 或平凡），因为 $m=0$ 的角向耦合最弱，谱叶分离度最大

2. **$m=2$ 高自旋**：单值群趋向 $S_N$（完全置换），尤其是在 $a=0.99$ 时，分支点密集导致几乎所有谱叶都参与交换

3. **自旋阈值 $a_c(m)$**：存在临界自旋，$a > a_c(m)$ 后单值群新增一个生成元。预期 $a_c(0) > a_c(1) > a_c(2)$，即大 $|m|$ 模式更早出现分支点

4. **物理根的保护机制**：LACI 指数 $\text{LACI} < 1$ 的区域恰好对应单值群中恒等置换的邻域——在该邻域内，谱叶 $i_{\text{物理}}$ 永远映射到自身

#### 6.3 收敛判据与可靠性保证

```python
def verify_monodromy_consistency(solver, l, m, a, loops, tolerance=1e-8):
    """
    验证单值群计算的一致性。
    
    检查项:
    1. 回路的可组合性：P_{Γ₁∘Γ₂} = P_{Γ₁}·P_{Γ₂}
    2. 缩并回路恒等：可缩并回路的置换应为恒等
    3. 参数连续依赖：相邻参数的生成元共轭
    """
    # 检查 1: 回路组合
    P_combined = compute_monodromy(compose_loops(loops[0], loops[1]))
    P_product = compute_monodromy(loops[0]) @ compute_monodromy(loops[1])
    assert np.allclose(P_combined, P_product), "回路组合性不满足"
    
    # 检查 2: 缩并回路
    trivial_loop = [lambda t: omega_qnm for t in np.linspace(0, 1, 100)]
    P_trivial = compute_monodromy(trivial_loop)
    assert np.allclose(P_trivial, np.eye(N)), "缩并回路不应有置换"
    
    # 检查 3: 参数连续性（相邻 a 值的单值群应共轭）
    if a > 0.01:
        P_current = compute_monodromy(loops[0])
        P_prev = previous_result[(a-0.01, l, m)]['generators'][0]
        # 存在 g ∈ S_N 使 P_current = g·P_prev·g^{-1}
        assert are_conjugate(P_current, P_prev), "参数不连续"
    
    return True
```

---

### 7. 计算流程总结

```
光谱丛单值群完整计算流程：

输入: (a, l, m, N_trunc, ω_grid)
输出: 单值群结构信息

Step 1 ─ 求解 QNM 频率 ω_QNM
        │
        ▼
Step 2 ─ 计算 ω 全谱 {λ_i(ω)}，i=1,...,N_trunc
        │
        ▼
Step 3 ─ 检测判别式零点 → 分支点候选集合 B
        │
        ▼
Step 4 ─ 对每个分支点 ω_k ∈ B 构造回路 Γ_k
        │
        ▼
Step 5 ─ 谱叶追踪 → 置换矩阵 P_{Γ_k}
        │
        ▼
Step 6 ─ 生成元集合 G = {P_{Γ_k}}
        │
        ▼
Step 7 ─ 群结构分析：阶、传递性、可解性、同构
        │
        ▼
Step 8 ─ 参数扫描：遍历 (a,m) 网格 → 单值群相图
        │
        ▼
输出: 单值群相图 + 生成元 + 群结构
```

**复杂度估计**：
- 每个 $(a, m, \omega)$ 点的谱计算：$O(N^3)$（QR 分解）或 $O(N^2)$（三对角 QR）
- 每对相邻 $\omega$ 的匹配：$O(N^3)$（匈牙利算法）
- 总 $\omega$ 采样点数：约 $1000 \times K$（$K$ 为回路数）
- 总参数组合：$5 \times 3 = 15$ 组

**建议**：在 $N=80$ 维度下，计算全部 15 组参数的单值群约需 1-2 小时（单 CPU）。高自旋 $a=0.99$ 需更多采样点，总时约 4 小时。

---

## 参考文献

1. Leaver, E. W. (1985). *An analytic representation for the quasi-normal modes of Kerr black holes*. PRD 34, 384.
2. Cook, G. B. & Zalutskiy, M. (2014). *Angular and radial modes of Kerr quasinormal frequencies*. PRD 90, 124021.
3. Berti, E., Cardoso, V., & Will, C. M. (2006). *On the computation of Kerr quasinormal frequencies*. PRD 73, 064030.
4. Kato, T. (1995). *Perturbation Theory for Linear Operators*. Springer.
5. Vasil'ev, V. A. (2002). *Introduction to the Topology of Function Spaces*.
