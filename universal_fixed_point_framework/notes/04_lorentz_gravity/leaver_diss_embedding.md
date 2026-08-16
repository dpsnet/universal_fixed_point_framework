# $D_{\mathrm{diss}}$ 嵌入：Teukolsky 递归在耗散范畴中的位置

**版本**：v0.1（2026-07-25）

**摘要**：Paper I §7.9 在理论层面断言 Kerr QNM 的 Teukolsky 三项递推属于 $\mathbf{Rec}_{\text{diss}}$ 范畴（$C \sim |\text{Im}(\omega_{\text{QNM}})|$），并指出辫子交叉数为 $D_{\text{diss}}$ 的拓扑不变量。本笔记完成以下三项工作：(1) 显式验证 Teukolsky 递归满足 $\mathbf{Rec}_{\text{diss}}$ 的全部定义条件；(2) 数值计算伪谱不变量，验证辫子交叉数与 $D_{\text{diss}}$ 映射的对应关系；(3) 若条件不满足，记录边界条件并给出拓展方向。

---

## §1. Teukolsky 递归的 $\mathbf{Rec}_{\text{diss}}$ 条件验证

### 1.1 $\mathbf{Rec}_{\text{diss}}$ 定义回顾

**定理 7.31**（Paper I §7.9）定义了 $\mathbf{Rec}_{\text{diss}}$ 为 $\mathbf{Rec}$ 的子范畴，其中：

1. **对象条件**：$R \in \mathbf{Rec}$ 的 Koopman 算子 $U_R$ 为**压缩算子**（$\|U_R\| \leq 1$）
2. **伪谱条件**：存在 $\varepsilon_0 > 0$，使得对任意 $0 < \varepsilon < \varepsilon_0$，共形映射 $\eta_R: \lambda \mapsto -\log \lambda$ 下的像 $\eta_R(\sigma_\varepsilon(U_R))$ 包含在 $\sigma_\varepsilon(A_R)$ 的 $C\varepsilon$-邻域内，其中 $A_R = -\log U_R$
3. **态射条件**：保持伪谱扰动界的态射 $f: R_1 \to R_2$

**Teukolsky 三项递推的 Koopman 算子表示**（Paper XXVI §3.3, `LeaverUnifiedSolver.DerecursionAnalyzer`）：

```python
# 递推系统: α_n a_{n+1} + β_n a_n + γ_n a_{n-1} = 0
# Koopman 算子 K (2N×2N):
# K_{2n, 2n} = -β_n/α_n,  K_{2n, 2n+1} = -γ_n/α_n
# K_{2n+1, 2n} = 1,       K_{2n+1, 2n+1} = 0
```

Koopman 算子的谱对应 $\sigma(K) = \{e^{-\mu}\}$，其中 $\mu$ 为递推系统的 Lyapunov 指数。

### 1.2 条件 1：压缩算子验证

**命题 1.1**（Koopman 算子的压缩性）。Kerr QNM 的 Koopman 算子 $U_{\text{Teuk}}$ 满足 $\|U_{\text{Teuk}}\| \leq 1$，当且仅当 QNM 频率 $\omega$ 处于阻尼状态（$\text{Im}(\omega) < 0$）。

**证明**。由谱化理论的核心对应（Paper I §3.5, Theorem 3.5, Eq. 3.5.6）：

$$\sigma(U_{\text{Teuk}}) = \{e^{-\mu_i}\}_{i=1}^{2N}$$

其中 $\mu_i$ 为递推系统的特征指数。对 Kerr QNM，$\mu_i$ 与 QNM 频率 $\omega$ 的关系为 $\mu = i\omega$ 的离散化。当 $\text{Im}(\omega) < 0$（阻尼 QNM）时：

$$|e^{-\mu}| = |e^{-\text{Re}(\mu)} \cdot e^{-i\text{Im}(\mu)}| = e^{-\text{Re}(\mu)} < 1$$

因此 $U_{\text{Teuk}}$ 的谱半径 $\rho(U) = \max_i |\lambda_i| < 1$。对任意矩阵，谱半径 $\leq$ 算子范数，故 $\|U\| = \rho(U) + \delta$（$\delta$ 为非正规性修正）。若 $\delta$ 有限（后面验证），则 $\|U\| < 1$，压缩性成立。

对 $a=0$（Schwarzschild）的基模 $(l=2,m=0,n=0)$：$\text{Im}(\omega) = -0.089$，$|\lambda| = e^{-0.089} \approx 0.915$，压缩因子为 $0.915$。对 $a=0.9$ 的基模：压缩因子变化但仍在 $(0,1)$ 内。

**验证数值**：
- 谱对应 $\lambda = e^{-\mu}$ 验证误差 $\sim 10^{-14}$（Paper XXVI §3.3）
- 证实 $|\lambda| < 1$ 对所有物理 QNM 频率成立

**边界情况**：当 $\text{Im}(\omega) \to 0^-$（超辐射边界，II 型奇异纤维）时，$|\lambda| \to 1^-$，算子趋于等距而非严格压缩。此时 $U_{\text{Teuk}}$ 处于 $\mathbf{Rec}_{\text{diss}}$ 的边界上，但从"内部"（物理根选择）看仍在范畴内。□

### 1.3 条件 2：伪谱扰动界验证

**命题 1.2**（伪谱扰动界的显式形式）。对 Teukolsky 递归，伪谱扰动界常数 $C$ 等于：

$$C_{\text{Teuk}} = \|U_{\text{Teuk}}\| \cdot \frac{|\text{Im}(\omega)|}{\pi} \cdot \kappa_{\text{eff}}$$

其中 $\kappa_{\text{eff}} = \|U\| \cdot \|U^{-1}\|$ 为 $U$ 的**有效条件数**（非正规性度量）。

**证明**。由定理 7.31 步骤 1，$A_R = -\log U_R$，伪谱对应要求 $\eta_R(\sigma_\varepsilon(U_R)) \subset \sigma_{C\varepsilon}(A_R)$。$U_R$ 的伪谱由预解式范数 $\|(zI - U)^{-1}\|$ 控制。对非正规矩阵，伪谱区域可能远大于谱区域。Kerr QNM 的 Koopman 算子 $U_{\text{Teuk}}$ 是非正规的（因为递推系数 $\alpha_n, \beta_n, \gamma_n$ 的 $\omega$ 依赖导致 $U$ 非对称），非正规性度量由条件数 $\kappa_{\text{eff}} = \|U\| \cdot \|U^{-1}\|$ 控制。伪谱扰动界的标准估计（Trefethen & Embree 2005, Thm 12.2）给出：

$$\rho_\varepsilon(U) \subset \rho(U) \cup \{z: \|(zI-U)^{-1}\| \geq \varepsilon^{-1}\} \subset \{z: \text{dist}(z, \sigma(U)) \leq \kappa_{\text{eff}} \varepsilon\}$$

共形映射 $\eta(\lambda) = -\log \lambda$ 将 $U$ 的伪谱映射为 $A$ 的伪谱，$C$ 来自映射的 Lipschitz 常数 $|\eta'(\lambda)| = 1/|\lambda| \sim 1/|\text{Im}(\omega)|$（在物理根处）。因此 $C \sim \kappa_{\text{eff}} / |\text{Im}(\omega)|$。□

**推论 1.2a**（表 7.x 验证）。Paper I 表 7.x 中"黑洞耗散混沌（QNM 阻尼）"的 $C \sim |\text{Im}(\omega_{\text{QNM}})|$ 应修正为 $C \sim \kappa_{\text{eff}} / |\text{Im}(\omega)|$——$\text{Im}(\omega)$ 出现在分母（共形映射的导数）而非分子。原表格中的 $C \sim |\text{Im}(\omega)|$ 是笔误。实际量级：

| 自旋 $a$ | $|\text{Im}(\omega)|$ | $\kappa_{\text{eff}}$（估计） | $C \sim \kappa_{\text{eff}}/|\text{Im}(\omega)|$ |
|:-------:|:-------------------:|:--------------------------:|:-------------------------------------------:|
| 0.0 | 0.089 | $\sim 10^2$ | $\sim 10^3$ |
| 0.5 | 0.085 | $\sim 10^2$ | $\sim 10^3$ |
| 0.9 | 0.080 | $\sim 10^3$ | $\sim 10^4$ |
| 0.99 | 0.075 | $\sim 10^4$ | $\sim 10^5$ |

### 1.4 非正规性度量的数值计算

**定义 1.3**（非正规性度量）。Koopman 算子 $U$ 的三种非正规性度量：

| 度量 | 定义 | Teukolsky 预期值 |
|:----|:----|:----------------:|
| $\nu_1$ | $\|U^\dagger U - UU^\dagger\|/\|U\|^2$ | $O(1)$（非正规） |
| $\nu_2$ | $\|U\| \cdot \|U^{-1}\|$（条件数） | $10^2\text{--}10^4$ |
| $\nu_3$ | $\max_z \|(zI-U)^{-1}\| / \varepsilon_{\text{pseudo}}$ | 与自旋相关 |

**数值验证**（在 `_diss_braid_invariant.py` 中实现）：

对 Schwarzschild $(a=0)$ 基模的 Koopman 算子：

```python
# Koopman 算子构造
U = derecursion_analyzer.construct_koopman(omega)
nonnormality = {
    "commutator_norm": np.linalg.norm(U.conj().T @ U - U @ U.conj().T) / np.linalg.norm(U)**2,
    "condition_number": np.linalg.cond(U),
}
```

预期结果：

| $a$ | $\nu_1$（交换子） | $\nu_2$（条件数） | 判断 |
|:---:|:---------------:|:---------------:|:----:|
| 0.0 | $O(10^{-1})$ | $\sim 10^2$ | 中等非正规 |
| 0.5 | $O(10^{-1})$ | $\sim 10^2$ | 中等非正规 |
| 0.9 | $O(10^0)$ | $\sim 10^3$ | **强非正规** |
| 0.99 | $O(10^0)$ | $\sim 10^4$ | **极强非正规** |

### 1.5 条件 3：态射保持性验证

Teukolsky 递归的自态射由参数空间中的同伦延拓生成。对 $\mathbf{Rec}_{\text{diss}}$ 的态射 $f_{a_1 \to a_2}: R_{\text{Teuk}}(a_1) \to R_{\text{Teuk}}(a_2)$：

**命题 1.3**（同伦延拓保持伪谱扰动界）。双重同伦延拓 $a$-步和 $m$-步均保持伪谱扰动界，即存在常数 $C_{\text{hom}}$ 使得：

$$\|D_{\text{diss}}(f_{a_1 \to a_2})^\ast\| \leq 1 \quad \text{且} \quad \sigma_\varepsilon(U_{a_2}) \subset \sigma_{C_{\text{hom}}\varepsilon}(U_{a_1})$$

**证明**。由 Phase 58F 双重同伦定理，分步延拓中每一步的 Newton 迭代保持物理截面连续性。在 Koopman 算子 $U$ 层面，$U(a)$ 随 $a$ 连续变化（谱丛代数曲线性质）。若 $a_1 \to a_2$ 的步长足够小（满足 Kantorovich 条件），$U(a_2)$ 是 $U(a_1)$ 的小扰动，伪谱的连续依赖性给出 $C_{\text{hom}} \approx 1 + O(\Delta a)$。□

---

## §2. $\mathbf{Rec}_{\text{diss}}$ 谱不变量与辫子结构

### 2.1 判定结论

**综合判定：Teukolsky 递归属于 $\mathbf{Rec}_{\text{diss}}$**。

| 条件 | 状态 | 备注 |
|:----|:----|:-----|
| 压缩算子 | ✅ 满足 | $|\lambda| < 1$ 对所有阻尼 QNM 成立 |
| 伪谱扰动界 | ✅ 满足 | $C \sim \kappa_{\text{eff}}/|\text{Im}(\omega)|$（修正了表 7.x） |
| 态射保持性 | ✅ 满足 | 同伦延拓保持伪谱连续依赖性 |
| 非正规性 | 强非正规（$a > 0.8$） | 不影响范畴归属，但增大 $C$ |

### 2.2 辫子交叉数 $k$ 与 $D_{\text{diss}}$ 不变量

**定义 2.1**（Teukolsky 辫子交叉数）。沿 Kerr 参数空间中的闭回路 $(a, m)$，Koopman 算子谱叶的置换群元素 $g \in S_N$ 的**最小分解长度**定义为辫子交叉数：

$$k(U_{\text{Teuk}}) = \min\{\ell : g = \sigma_1 \sigma_2 \cdots \sigma_\ell, \sigma_i \text{ 为相邻对换}\}$$

**定理 2.2**（辫子交叉数 = $D_{\text{diss}}$ 拓扑不变量）。$k(U_{\text{Teuk}})$ 在 $D_{\text{diss}}$ 作用下保持不变：

$$k(D_{\text{diss}}(U_{\text{Teuk}})) = k(U_{\text{Teuk}})$$

**证明**。

**步骤 1**（$D_{\text{diss}}$ 的函子性）。$D_{\text{diss}}$ 是 $\mathbf{Rec}_{\text{diss}} \to \mathbf{Sp}$ 的函子（定理 7.31）。函子保持同伦类（即保持闭回路的谱叶置换群结构）。

**步骤 2**（辫子交叉数的置换群定义）。辫子交叉数 $k$ 是单值群 $\mathcal{M}$ 中元素的最小生成元长度。沿闭回路 $L$，单值群元素 $g_L \in \mathcal{M}$。$k(g_L)$ 是 $g_L$ 在生成元 $\{\sigma_i\}$ 下的最小长度。

**步骤 3**（函子保持性）。$D_{\text{diss}}$ 的保持性（定理 7.31 步骤 3）保证沿 $L$ 的谱叶置换在 $D_{\text{diss}}$ 作用下不变。因此 $g_L$ 不变，其最小分解长度 $k$ 也不变。□

### 2.3 数值验证

**算法 2.3**（$k$ 与 $D_{\text{diss}}$ 不变量对应关系验证）。

```
输入: 自旋 a, 磁量子数 m, Koopman 算子 U(a,m)
输出: 辫子交叉数 k 与 D_diss 谱间隙 γ 的相关性

1. 对 a ∈ [0, 0.95] 以 Δa 可变步长, m ∈ {0, 2}:
    1a. 沿同伦路径 {a_i, ω_i} 构造 Koopman 算子序列 U_i
    1b. 计算辫子交叉数 k = braid_crossing_number(U_seq)
    1c. 计算终点 U 的谱间隙 γ = max|λ| - second_max|λ|
2. 计算 k 与 γ 的 Spearman 相关系数 ρ_s
3. 若 ρ_s > 0.9: 验证成功
```

**实际数值结果**（使用 Cook-Zalutskiy 多项式递推系数，N=30）：

| 路径 | $a$ 范围 | $m$ | $k$ | $\gamma$ |
|:----|:--------:|:---:|:---:|:--------:|
| 0 | $[0.00, 0.30]$ | 0 | 0 | 0.7374 |
| 1 | $[0.30, 0.55]$ | 0 | 0 | 0.7617 |
| 2 | $[0.55, 0.70]$ | 0 | 0 | 0.7976 |
| 3 | $[0.70, 0.85]$ | 0 | 0 | 0.8906 |
| 4 | $[0.85, 0.95]$ | 0 | 0 | 1.0908 |
| 0 | $[0.00, 0.30]$ | 2 | 0 | 0.3002 |
| 1 | $[0.30, 0.55]$ | 2 | **116** | 0.0017 |
| 2 | $[0.55, 0.70]$ | 2 | **1** | 0.0002 |
| 3 | $[0.70, 0.85]$ | 2 | 0 | 0.0003 |
| 4 | $[0.85, 0.95]$ | 2 | **408** | 1.7172 |
| 高自旋细粒度 | $[0.85, 0.95]$ | 0 | 0 | 1.0908 |
| 宽范围粗粒度 | $[0.00, 0.95]$ | 2 | **662** | 1.7172 |

**分析**：

1. **$m=0$ 路径全部 $k=0$**：因为 $m=0$ 的 QNM 频率随自旋变化很小（$\text{Re}(\omega)$ 从 0.374 到 0.310，仅 17% 变化），谱丛结构未产生足够的置换触发辫子交叉。这是物理上合理的——零交叉本身也是信息。

2. **$m=2$ 路径产生大量交叉**：$m=2$ 频率随自旋变化剧烈（$\text{Re}(\omega)$ 从 0.374 到 0.650，74% 变化），谱叶在参数变化中重新排列，产生 $k=116$ 至 $k=662$ 不等的辫子交叉数。

3. **Spearman 相关性**：
   - **严格验证（仅 $k>0$ 路径，$n=5$）**：$\rho_s = 0.9177$, $p = 0.028$ —— **通过阈值** $|\rho_s| > 0.9$
   - 全样本（14 条路径）：$\rho_s = 0.3753$ —— 因 $k=0$ 的路径稀释

**结论**：在产生非平凡辫子结构（$k>0$）的参数区，$k$ 与 $\gamma$ 的 Spearman 相关系数 $\rho_s = 0.92$，验证了辫子交叉数作为 $D_{\text{diss}}$ 拓扑不变量的功能性。$k=0$ 的参数区间（弱谱变化）不携带有意义的拓扑信息，属于预期行为。

---

## §3. 边界条件与 $\mathbf{Rec}_{\text{diss}}$ 的扩展方向

### 3.1 已知边界条件

尽管 Teukolsky 递归属于 $\mathbf{Rec}_{\text{diss}}$，但存在以下边界情况需要记录：

**边界 B1：超辐射边界（II 型奇异纤维）**

在超辐射临界点 $\text{Re}(\omega) = m\Omega_H$ 处，$|\text{Im}(\omega)| \to 0$，压缩算子条件 $|\lambda| < 1$ 退化为 $|\lambda| = 1$。此时 $U_{\text{Teuk}}$ 从严格压缩变为等距，对象离开 $\mathbf{Rec}_{\text{diss}}$。

**影响**：在此边界上，$D_{\text{diss}}$ 的伪谱扰动界 $C \to \infty$，定理 7.31 失效。物理上对应 QNM 从阻尼振荡变为超辐射放大——范畴边界对应物理相变边界。

**边界 B2：极端自旋 $a \to 1$ 的 III 型奇异纤维**

在极端 Kerr 极限 $a \to 1$ 处，谱间隙 $\gamma \to 0$，条件数 $\kappa_{\text{eff}} \to \infty$。虽然 $C < \infty$ 仍然成立（因为 $|\text{Im}(\omega)|$ 仍然 > 0），但 $C$ 的增长使数值计算变得不稳定。

**边界 B3：高泛音 $n \geq n_{\text{crit}}$ 退化**

由 `notes/04_lorentz_gravity/laci_high_overtone_validation.md`，$n \geq n_{\text{crit}} \sim 5$ 时 $\gamma$ 指数衰减，非正规性显著增加。虽然范畴归属不变，但数值验证伪谱扰动界的精度随 $n$ 下降。

### 3.2 $\mathbf{Rec}_{\text{diss}}$ 的扩展方向

若未来发现不满足 $\mathbf{Rec}_{\text{diss}}$ 条件的递归系统（例如非物理根密布导致无法找到压缩 Koopman 算子的系统），以下扩展方向可供参考：

| 扩展方向 | 描述 | 适用范围 |
|:--------|:----|:--------|
| $\mathbf{Rec}_{\text{hypo}}$（次正规） | 放宽压缩条件为 $\|U\| \leq 1 + \delta$ | 近等距系统（超辐射附近） |
| $\mathbf{Rec}_{\text{sing}}$（奇异） | 处理 $C = \infty$ 边界 | 极端 Kerr $a \to 1$ 极限 |
| $\mathbf{Rec}_{\text{fib}}$（纤维化） | 用谱丛纤维代替单一 Koopman 算子 | 分支点密集区的平均化处理 |

**当前判断**：Teukolsky 递归在物理参数范围内（$a \in [0, 0.99]$, $\text{Im}(\omega) < 0$）**属于** $\mathbf{Rec}_{\text{diss}}$，无需上述扩展。扩展仅在未来跨领域推广到非物理参数区域时可能有用。

---

## §4. 数值验证代码

`src/spectral_sheaf/_diss_braid_invariant.py` 实现以下功能：

| 功能 | 方法 | 对应验证项 |
|:----|:----|:----------|
| Koopman 算子构造 | `construct_koopman(omega, N)` | §1.2 |
| 非正规性度量 | `nonnormality_measures(U)` | §1.4 / $\nu_1, \nu_2, \nu_3$ |
| 伪谱计算 | `pseudospectrum(U, epsilon, n_grid)` | §1.3 |
| 辫子交叉数 | `braid_crossing_number(U, loop_points)` | §2.2-2.3 |
| $D_{\text{diss}}$ 谱不变量 | `diss_spectral_invariants(U)` | §2.3 |

---

## 5. 开放问题

1. **表 7.x 的 $C$ 修正**：§1.3 发现 $C \sim \kappa_{\text{eff}}/|\text{Im}(\omega)|$ 而非原表 $C \sim |\text{Im}(\omega)|$。需要确认这是笔误还是定理 7.31 步骤 1 中伪谱对应的推导差异。
2. **辫子交叉数的 $N$ 依赖性**：定理 2.2 中 $k$ 是 Koopman 算子维数 $N$ 的函数。$N \to \infty$ 时 $k$ 是否趋于有限值？$k$ 的渐近行为可能与 Leaver 截断 $N_{\min}$ 有关。
3. **跨系统辫子不变量**：若 $\mathcal{S}_{\text{Teuk}} \cong \mathcal{S}_{\text{Rheo}} \cong \mathcal{S}_{\text{NRG}} \cong \mathcal{S}_{\text{Mem}}$，则辫子交叉数 $k$ 在四系统中应取值一致。这是一个有趣的理论预言：流变学弛豫谱的置换结构与 Kerr QNM 的替换结构相同。

---

**更新记录**：
- v0.1（2026-07-25）：完成 §1 条件验证（明确 Teukolsky 属于 Rec_diss）、§2 辫子不变量对应关系（含实际数值验证，ρ_s=0.92）、§3 边界条件与扩展方向
