# Dirac 谱丛后续工作详细研究笔记（Paper XXIX §9 未来工作对应）

**版本**：v0.1（2026-07-26）

**摘要**：本文档对应 Paper XXIX §9 列出的四项未来工作，包含完整的理论基础、实施方案、预期困难与验证标准。本文档是各子项从"理论框架"推进到"数值验证/形式化实现"的详细研究笔记。

---

## 1. $\mathbb{Z}_2$ 阻碍的严格数值验证：谱叶追踪算法

### 1.1 问题背景

§3 证明了 Dirac 谱丛存在非平凡 $\mathbb{Z}_2$ 阻碍 $H^2(\mathcal{M}_\omega^{(s)},\mathbb{Z}_2) \neq 0$，提出了 $2\pi$ vs $4\pi$ 回路数值检测协议（§3.5）。严格数值验证的目的是将该结论从"数学证明"提升为"数值可观测效应"，使得 $\mathbb{Z}_2$ 阻碍成为诊断半整数自旋谱丛的实验可测信号。

### 1.2 验证目标

| 目标 | 成功标准 | 优先级 |
|:----|:--------|:------:|
| T1. 实现高精度谱叶追踪算法 | 沿 $2\pi$ 回路精度 $< 10^{-6}$，叶标识正确率 $> 99.9\%$ | P0 |
| T2. 确认 $2\pi$ 回路谱叶置换非平凡 | 置换群像 $\rho(\ell_{2\pi})$ 含奇置换（sgn = -1） | P0 |
| T3. 确认 $4\pi$ 回路谱叶置换回到恒等 | $\rho(\ell_{4\pi}) = \text{id} \in S_N$ | P0 |
| T4. 排除非自旋因素（截断误差、模式混叠） | 对照实验证明奇置换不出现于 $s=-2,-1,0$ 整数自旋 | P1 |
| T5. 扫描 $a$ 参数空间验证自旋结构持续性 | $\mathbb{Z}_2$ 阻碍在 $a \in [0, 0.999]$ 上连续可观测 | P1 |

### 1.3 谱叶追踪算法详细设计

#### 1.3.1 算法结构（分三阶段）

**阶段 A：回路的离散化与初始参数化**

输入：自旋 $s$，黑洞参数 $a,m$，截断 $N$，回路中心 $\omega_0$（分支点），回路半径 $r$，离散化步数 $K$。

回路参数化：

$$\ell(\theta) = \omega_0 + r e^{i\theta},\quad \theta \in [0, 2\pi] \text{ 或 } [0, 4\pi]$$

**分支点定位**：先用 Newton 法求解 $\det M_{a,m}^{(s)}(\omega) = 0$ 定位 QNM 频率，再用判别式 $\Delta(\omega) = \det M_{a,m}^{(s)}(\omega)$ 的零点附近扫描确定分支点位置。分支点 $\omega_b$ 满足：

$$\frac{\partial}{\partial \omega} \det M_{a,m}^{(s)}(\omega_b) = 0,\quad \det M_{a,m}^{(s)}(\omega_b) = 0$$

**回路半径选择**：$r$ 应满足：
- $r > |\omega_b - \omega_0| + \delta$（环绕所有目标分支点）
- $r < r_{\text{max}}$（避免与其他分支点相交）
- 经验值：$r = 0.05$（对 $a < 0.99$），$r = 0.02$（对 $a \geq 0.99$）

**阶段 B：谱叶的渐进追踪（双重同伦延拓）**

在每个离散点 $\theta_k = k \cdot 2\pi/K$（$k=0,\dots,K-1$），计算：

$$\ell_k = \ell(\theta_k) = \omega_0 + r e^{i\theta_k}$$

对每个 $\ell_k$，计算 $M_{a,m}^{(s)}(\ell_k)$ 的特征值 $\{\lambda_i(\ell_k)\}_{i=1}^N$。由于 $M$ 是非 Hermitian 的，使用 QR 算法（或 Divide-anHausdorff 维数凹性onquer SVD）计算全部 $N$ 个特征值。截断 $N=64$ 时，单次特征值分解的复杂度 $O(N^3) \approx 2.6\times 10^5$ 次运算。

**谱叶匹配**：在相邻点 $\ell_k \to \ell_{k+1}$ 之间建立特征值的一一对应。使用**最小位移准则**：

$$P_k(i) = \arg\min_{j} |\lambda_j(\ell_{k+1}) - \lambda_i(\ell_k)|$$

若 $|\lambda_{P_k(i)}(\ell_{k+1}) - \lambda_i(\ell_k)| > \Delta_{\text{jump}}$（跳跃阈值，默认 $\Delta_{\text{jump}} = 0.1$），则标记可能的分支点交叉，触发局部网格加密。

**抗锯齿策略**：在分支点附近，谱叶可能快速变化。处理方案：
- 在 $\theta \in [\theta_b - \pi/K, \theta_b + \pi/K]$ 区间加密 2 倍
- 使用预测-校正方法：线性外推 $\tilde{\lambda}_i(\ell_{k+1}) = \lambda_i(\ell_k) + (\ell_{k+1} - \ell_k) \cdot \lambda_i'(\ell_k)$ 后最近邻匹配
- 若加密后匹配仍失败，使用全局优化（匈牙利算法）替代贪心匹配

**阶段 C：置换的提取与验证**

沿回路追踪起点谱叶 $\lambda_i(\ell_0)$ 到终点 $\lambda_{P_{\text{total}}(i)}(\ell_K)$。由于 $\ell_K = \ell_0$（闭回路），$P_{\text{total}}$ 是 $S_N$ 中的置换。

**置换提取算法**：

```
Input: 特征值序列 {λ_i(ℓ_k)} 对 i=1..N, k=0..K
Output: 置换 σ ∈ S_N

初始化匹配链 chain[i] = [i] 对 i=1..N
For k = 0 to K-1:
    For i = 1 to N:
        j = match(λ_i(ℓ_k), λ_{chain[i][-1]}(ℓ_{k+1}))
        chain[i].append(j)
End For
σ(i) = chain[i][-1]  # 最终谱叶编号
```

**置换验证**：
- 计算 $\sigma$ 的循环分解 $\sigma = \prod_{c \in \text{cycles}} c$
- 计算符号 $\text{sgn}(\sigma) = (-1)^{N - \#\text{cycles}}$
- 对 $2\pi$ 回路：期望 $\text{sgn}(\sigma) = -1$（奇置换）
- 对 $4\pi$ 回路：期望 $\sigma = \text{id}$（恒等）

**命题 1.1**（有限精度下的可靠性条件）。当回路离散化步数 $K$ 满足：

$$K > \frac{2\pi r}{\min_i |\lambda_i'(\ell(\theta))| \cdot \eta_{\text{match}}}$$

时，谱叶追踪算法沿整个回路的累积错误概率 $< 10^{-6}$，其中 $\eta_{\text{match}}$ 是匹配容忍度（建议 $\eta_{\text{match}} = 0.01$，即特征值变化率的 1%）。

#### 1.3.2 计算资源估计

| 参数 | 值 | 说明 |
|:----|:---|:-----|
| $N$（截断）| 64 | 与现有 Leaver 求解器一致 |
| $K$（离散点数）| 200 | 典型值，$r=0.05$ 时 $\Delta\theta \approx 1.8^\circ$ |
| $a$ 采样 | 10 个值 | $\{0, 0.5, 0.8, 0.9, 0.95, 0.98, 0.99, 0.995, 0.998, 0.999\}$ |
| 单次回路计算量 | $K \times N^3 \sim 200 \times 2.6\times10^5 \approx 5\times10^7$ | 约 0.5 秒（现代 CPU） |
| 总计算量（含扫描） | $10 \times 2 \times 5\times10^7 \approx 1\times10^9$ | 约 10 秒 |

### 1.4 对照实验设计

#### 1.4.1 整数自旋零假设

对 $s=-2$（引力）和 $s=-1$（电磁），重复相同谱叶追踪过程。零假设 $H_0$：$\mathbb{Z}_2$ 阻碍不存在于整数自旋，即 $\text{sgn}(\sigma_{2\pi}) = +1$ 对所有回路成立。

**实验参数**：与 Dirac 完全相同（相同 $a,m,N,K,\omega_0,r$），仅改变 $s$。

**统计检验**：对 10 个 $a$ 值、每个 $s$ 执行 5 次独立回路追踪（共 50 次实验）。使用二项检验：若整数自旋中观察到 $\text{sgn}(\sigma_{2\pi}) = -1$ 的次数 $\leq 1$（显著性水平 $\alpha=0.05$），则拒绝 $H_0$。

#### 1.4.2 截断误差效应排除

增加截断 $N$ 从 64 到 128，观察 $\sigma$ 是否变化。若 $N=64$ 和 $N=128$ 给出相同 $\sigma$，则截断误差不是伪信号源。

#### 1.4.3 模式混叠排除

选取 $m$ 非简并模式（如 $l=m=2$ 的基模），排除 $m$ 简并对置换的伪装。

### 1.5 预期结果与数据可视化

| $s$ | 预期 $\text{sgn}(\sigma_{2\pi})$ | 预期 $\text{sgn}(\sigma_{4\pi})$ | 对应的物理含义 |
|:--:|:------------------------------:|:------------------------------:|:-------------|
| $-2$ | $+1$（偶置换） | $+1$ | 整数自旋，无 $\mathbb{Z}_2$ 阻碍 |
| $-1$ | $+1$（偶置换） | $+1$ | 整数自旋，无 $\mathbb{Z}_2$ 阻碍 |
| $-1/2$ | $-1$（奇置换） | $+1$ | 半整数自旋，$\mathbb{Z}_2$ 阻碍 |

**可视化方案**：
1. 复平面中谱叶轨迹：用不同颜色标记 $N$ 个谱叶，绘制 $\lambda_i(\theta)$ 沿 $\ell(\theta)$ 的路径
2. 置换矩阵热图：$N\times N$ 矩阵，$M_{ij} = 1$ 若 $\sigma(i)=j$，否则 0
3. $\text{sgn}(\sigma)$ 对 $a$ 的散点图：应观察到 $s=-1/2$ 在 $a \in [0,0.999]$ 上 $\text{sgn} = -1$ 持续，而 $s=-2,-1$ 为 $+1$

---

## 2. Dirac QNM 基准表

### 2.1 问题背景

目前缺乏系统的 Dirac QNM 基准表。对标引力和电磁 QNM（Berti 表, 2006; Cook-Zalutskiy 参考表, 2014），Dirac QNM 仅有少量分散结果（Chandrasekhar, 1976; Dolan, 2006）。建立基准表后可以：
1. 验证 Leaver 求解器在 $s=-1/2$ 的计算精度
2. 验证截断误差指数衰减率 $c_{\mathrm{D}}$ 的预期值 $\approx 1.66$
3. 为跨自旋排序 $\gamma_{\mathrm{D}} > \gamma_{\mathrm{EM}} > \gamma_{\mathrm{G}}$ 提供数值基础

### 2.2 基准表结构

#### 2.2.1 参数覆盖

| 维度 | 覆盖方案 | 点数 | 说明 |
|:----|:--------|:---:|:-----|
| 自旋 $s$ | $-\frac12, +\frac12$ | 2 | 正负自旋共轭关系（Parity 定理） |
| 旋转参数 $a$ | $\{0, 0.2, 0.5, 0.7, 0.85, 0.9, 0.95, 0.98, 0.99, 0.999\}$ | 10 | 覆盖慢速到极值旋转 |
| 角量子数 $l$ | $\frac12, \frac32, \frac52$ | 3 | 基模主导模，覆盖低角动量 |
| 磁量子数 $m$ | $-\frac12, +\frac12$ (对 $l=1/2$)；$-l,\dots,l$ (整数步长，对 $l\geq 3/2$) | 2-6 | 覆盖正负旋转方向 |
| 倍频 $n$ | 0, 1, 2 | 3 | 基模和第一个倍频 |

**总条目数估计**：$2 \times 10 \times 3 \times (2+4+6)/3 \times 3 \approx 720$ 条。

其中自旋 $s=+1/2$ 的条目可通过 Parity 定理 $\lambda^{(+1/2)}(\omega) = \overline{\lambda^{(-1/2)}(\overline{\omega})}$ 从 $s=-1/2$ 导出，实际计算仅需 $s=-1/2$，约 **360 条**。

#### 2.2.2 基准表条目格式

每条基准记录包含：

```
| s | a | l | m | n | Re(ω) | Im(ω) | Δω_err | ε_trunc | ε_Newton | ε_LACI | N_eff | 来源 |
```

其中：
- $\Delta\omega_{\text{err}}$：估计总误差 $\sqrt{\varepsilon_{\text{trunc}}^2 + \varepsilon_{\text{Newton}}^2 + \varepsilon_{\text{LACI}}^2}$
- $\varepsilon_{\text{trunc}}$：通过 $N=48,64,80$ Richardson 外推估计
- $\varepsilon_{\text{Newton}}$：Leaver 连续分数 Newton 迭代残差
- $\varepsilon_{\text{LACI}}$：从 LACI 参数转换的误差界
- $N_{\text{eff}}$：有效截断（Dirac 无跳项，$N_{\text{eff}}=N$）

#### 2.2.3 $a=0$ 解析基准点

Schwarzschild 极限下，Dirac QNM 有部分解析参考值：

**Theorem 2.1**（Schwarzschild Dirac QNM 参考值，Dolan 2006）。对 $a=0$, $s=-1/2$, $l=1/2$, $m=\pm1/2$，基模 $(n=0)$：

$$\omega_{l=1/2}^{\text{ref}} = 0.378721 - 0.096458i$$

该值来自 Dolan (2006) 使用 Leaver 连分数法的独立计算，误差估计 $< 10^{-6}$。

### 2.3 计算方案

#### 2.3.1 递推系数实现

在现有 Leaver 求解器框架（`src/dynamic_spectrum/`）中扩展支持 $s=\pm1/2$。

**核心实现**（`_dirac_teukolsky_coeff.py`，待创建）：

```python
def alpha_n_dirac(n, s):
    """Dirac 递推 alpha 系数"""
    if s == -0.5:
        return (n+1)*n  # n(n+1)
    elif s == +0.5:
        return (n+1)*(n+2)
    else:
        raise ValueError(f"Unsupported spin: {s}")

def beta_n_dirac(n, s, a, m, omega, lam):
    """Dirac 递推 beta 系数"""
    kappa = np.sqrt(1 - a**2)
    if s == -0.5:
        A = -lam - n*(n+0) + omega**2
        B = a*m*(m-1)/(n - 0.5) + 2*a*omega*m
        C = -2*a*m*omega * (n - 0.5)/(2*n - 1)
        return A + B + C
    elif s == +0.5:
        A = -lam - n*(n+2) + omega**2
        B = a*m*(m+1)/(n + 0.5) + 2*a*omega*m
        C = -2*a*m*omega * (n + 0.5)/(2*n + 1)
        return A + B + C

def gamma_n_dirac(n, s, omega, a):
    """Dirac 递推 gamma 系数"""
    kappa = np.sqrt(1 - a**2)
    return -2*1j*omega*kappa*(n - s)
```

#### 2.3.2 角向特征值求解

Dirac 角向分离常数 $\lambda_{\pm1/2,lm}$ 通过角向 Teukolsky 方程的谱方法求解：

**角向矩阵构造**（`angular_dirac.py`，待创建）：

- 基函数：自旋权重球谐函数 ${}_sY_{lm}$
- 矩阵元素：三对角形式（与径向类似但不同递推系数）
- 求解方法：QR 算法 + Newton 迭代修正

预期精度：$|\Delta\lambda| < 10^{-12}$（采用 $l_{\max}=30$ 截断）。

#### 2.3.3 连分数求根

Leaver 连分数法。对给定 $(s,a,m,\lambda)$，QNM 频率 $\omega$ 满足：

$$0 = R_0(\omega) = \beta_0 - \frac{\alpha_0\gamma_1}{\beta_1 - \frac{\alpha_1\gamma_2}{\beta_2 - \cdots}}$$

计算使用向后递归（Muller 法或 Newton 法求根）。初始猜测从 $a=0$ 解析值出发，沿 $a$ 参数连续延拓。

**收敛标准**：
- 连续分数残差 $|R_0(\omega)| < 10^{-10}$
- Newton 迭代步 $|\Delta\omega| < 10^{-8}$
- 截断 $N=64$（验证使用 $N=128$ 确认收敛）

### 2.4 截断误差验证

**命题 2.1**（Dirac 截断误差指数衰减率）。Dirac 三项递推的截断误差指数衰减率为：

$$c_{\mathrm{D}} = 2\ln\left|\frac{\alpha_\infty^{(-1/2)}}{\gamma_\infty^{(-1/2)}}\right| = 2\ln\left|\frac{1}{-2i\omega\kappa}\right| = 2\ln\frac{1}{2|\omega|\kappa}$$

对典型值 $\omega \approx 0.38-0.10i$（$|\omega| \approx 0.393$），$\kappa = \sqrt{1-a^2}$：

| $a$ | $\kappa$ | $c_{\mathrm{D}}$ | $e^{-c_{\mathrm{D}} \cdot 64}$ |
|:---:|:-------:|:----------------:|:-----------------------------:|
| 0 | 1.000 | $2\ln(1.272) \approx 0.481$ | $4.6\times10^{-14}$ |
| 0.5 | 0.866 | $2\ln(1.469) \approx 0.769$ | $6.2\times10^{-22}$ |
| 0.9 | 0.436 | $2\ln(2.917) \approx 2.141$ | $\sim 10^{-60}$ |
| 0.99 | 0.141 | $2\ln(9.019) \approx 4.400$ | $\sim 10^{-122}$ |

**验证协议**：对每个基准点，用 $N=48,64,80$ 计算 $\omega_N$，使用 Richardson 外推：

$$\omega_\infty \approx \omega_N + (\omega_N - \omega_{N-\Delta N}) \cdot \frac{e^{-c_{\mathrm{D}}N}}{e^{-c_{\mathrm{D}}N} - e^{-c_{\mathrm{D}}(N-\Delta N)}}$$

若 $|\omega_{64} - \omega_\infty| < 10^{-8}$ 对所有 $a$ 成立，则截断误差得到验证。

### 2.5 预期结果

基准表完成后，可执行以下验证：

| 验证项 | 预期结果 | 成功标准 |
|:------|:--------|:--------|
| $a=0$ 解析基准校核 | $\omega_{l=1/2}$ 相对误差 $< 10^{-6}$ | 通过 |
| 截断误差指数衰减 | $e^{-c_{\mathrm{D}}N}$ 拟合 $R^2 > 0.99$ | 通过 |
| LACI 参数排序 | $\gamma_{\mathrm{D}} > \gamma_{\mathrm{EM}} > \gamma_{\mathrm{G}}$ | 通过 |
| Parity 定理验证 | $\lambda^{(+1/2)}(\omega) = \overline{\lambda^{(-1/2)}(\overline{\omega})}$ | 通过 |
| 代数特殊模式 | $\omega_{\text{AS}}$ 处谱间隙 $\gamma_{\mathrm{D}} \to 0$ | 定性符合 |

---

## 3. 三自旋联合谱丛的数值验证

### 3.1 问题背景

§7 建立了 $S=\{-2,-1,-1/2\}$ 三自旋联合谱丛 $\mathfrak{S}^{(S)}$ 的理论框架。数值验证的目的是确认无耦合极限退化的连续性、弱耦合（小 $Q$）下纤维形变的结构、以及耦合曲率 $R^{(s_i,s_j)}$ 对 IV 型奇异纤维的定量诊断能力。

### 3.2 验证目标

| 目标 | 方法 | 成功标准 | 优先级 |
|:----|:-----|:--------|:------:|
| V1. 无耦合极限退化连续性 | $Q=0$ 时块矩阵对角化，谱退化为 Minkowski 和 | 特征值误差 $< 10^{-8}$ | P0 |
| V2. 小 $Q$ 纤维形变 | $0 < |Q| \ll M$ 时追踪谱叶分裂 | 谱裂宽度 $\propto Q$ 线性检验 | P0 |
| V3. IV 型奇异纤维阈值 | 扫描 $Q$ 寻找耦合曲率发散点 | $R^{(s_i,s_j)}$ 发散处谱间隙归零 | P1 |
| V4. 耦合强度的谱丛分类 | 弱/强耦合的数值判定标准 | 找到 $Q_c$ 使分类有意义 | P1 |

### 3.3 无耦合极限退化验证

#### 3.3.1 块三对角矩阵的构造

对 $S=\{-2,-1,-1/2\}$，耦合块三对角矩阵为 $3N \times 3N$ 矩阵（每个自旋截断 $N=64$，总维数 $192$）：

$$M_{\text{total}}(a,m,\omega,Q) = \text{tridiag}(\mathbf{A}_n,\ \mathbf{B}_n,\ \mathbf{C}_n)$$

其中 $3\times3$ 矩阵块为：

$$\mathbf{A}_n = \begin{pmatrix}
\alpha_n^{(-2)} & 0 & 0 \\
0 & \alpha_n^{(-1)} & 0 \\
0 & 0 & \alpha_n^{(-1/2)}
\end{pmatrix}$$

$$\mathbf{B}_n = \begin{pmatrix}
\beta_n^{(-2)} & \delta_n^{(-2,-1)} & \delta_n^{(-2,-1/2)} \\
\delta_n^{(-1,-2)} & \beta_n^{(-1)} & \delta_n^{(-1,-1/2)} \\
\delta_n^{(-1/2,-2)} & \delta_n^{(-1/2,-1)} & \beta_n^{(-1/2)}
\end{pmatrix}$$

$$\mathbf{C}_n = \begin{pmatrix}
\gamma_n^{(-2)} & 0 & 0 \\
0 & \gamma_n^{(-1)} & 0 \\
0 & 0 & \gamma_n^{(-1/2)}
\end{pmatrix}$$

耦合项 $\delta_n^{(-2,-1)}$ 的显式形式（在 Kerr-Newman 背景下）：

$$\delta_n^{(-2,-1)}(Q) = Q \cdot \frac{2i\omega (r_+ - r_-)}{(2n+4)(2n+2)} \cdot f(n,a,\omega,m)$$

其中 $f$ 为有界函数（$|f| \leq 1$），$r_\pm = M \pm \sqrt{M^2-a^2-Q^2}$ 是内外视界。

#### 3.3.2 退化验证协议

**协议**：对 $Q=0$ 时的 $M_{\text{total}}$ 计算全部 $3N$ 个特征值，并与各子谱丛特征值的 Minkowski 和 $\{\lambda_i^{(-2)} + \lambda_j^{(-1)} + \lambda_k^{(-1/2)}\}_{i,j,k=1}^{N/3}$ 比较。

由于 Minkowski 和给出 $N^3/27$ 个特征值（远大于 $3N$），正确比较方式：取 $Q=0$ 时 $M_{\text{total}}$ 的 $3N$ 个特征值应与三个子谱丛特征值的**并集**一致：

$$\sigma(M_{\text{total}}(Q=0)) = \sigma(M^{(-2)}) \cup \sigma(M^{(-1)}) \cup \sigma(M^{(-1/2)})$$

而非 Minkowski 和（Minkowski 和对应张量积谱丛而非直和谱丛）。

**验证指标**：
- Hausdorff 距离 $d_H(\sigma(M_{\text{total}}(0)), \sigma_{\text{union}}) < 10^{-10}$
- 对每个子谱丛特征值 $\lambda$，存在 $\lambda' \in \sigma(M_{\text{total}}(0))$ 满足 $|\lambda - \lambda'| < 10^{-12}$

#### 3.3.3 耦合引入的谱分裂

当 $|Q| > 0$ 时，$\delta_n \neq 0$ 导致谱分裂。弱耦合下的微扰分析：

**命题 3.1**（小 $Q$ 一阶微扰）。对 $|Q| \ll M$，特征值 $\lambda_i(Q)$ 的一阶修正为：

$$\lambda_i(Q) = \lambda_i(0) + Q \cdot v_i^\dagger M_{\text{coupling}} v_i + O(Q^2)$$

其中 $v_i$ 是 $M_{\text{total}}(0)$ 的第 $i$ 个特征向量，$M_{\text{coupling}} = \partial M_{\text{total}}/\partial Q|_{Q=0}$。

**验证方案**：
1. 计算 $M_{\text{total}}(Q)$ 对 $Q=0, 0.001, 0.01, 0.05, 0.1, 0.2$ 的特征值
2. 对每个特征值 $\lambda_i(Q)$，计算差值 $\Delta\lambda_i(Q) = \lambda_i(Q) - \lambda_i(0)$
3. 检验 $\Delta\lambda_i(Q) \propto Q$ 的线性关系（Pearson 相关系数 $> 0.99$）
4. 记录偏离线性的 $Q$ 值（即 $O(Q^2)$ 项变得显著的阈值）

**预期结果**：对引力-电磁耦合（$\delta^{(-2,-1)}$），线性关系在 $Q < 0.1$ 时保持；对引力-Dirac 耦合（$\delta^{(-2,-1/2)}$），线性关系在 $Q < 0.05$ 时保持（因为 Dirac 谱间隙更小，对微扰更敏感）。

### 3.4 IV 型奇异纤维的定量诊断

#### 3.4.1 耦合曲率的数值定义

**定义 3.1**（数值耦合曲率）。对离散参数值 $Q_k = k\Delta Q$（$k=0,\dots,K-1$），耦合曲率估计为：

$$R^{(s_i,s_j)}(Q_k) = \frac{1}{\Delta Q^2}\left( \text{Tr}[M_{\text{diag}}(Q_{k+1}) - M_{\text{diag}}(Q_k)] \cdot [M_{\text{off}}(Q_{k+1}) - M_{\text{off}}(Q_k)] \right)$$

其中 $M_{\text{diag}}$ 和 $M_{\text{off}}$ 分别是 $M_{\text{total}}$ 的对角块和非对角块。

#### 3.4.2 IV 型奇异纤维的检测

扫描 $Q$ 从 0 到 $Q_{\text{max}}$（$Q_{\text{max}} \approx 0.5M$，对 $a=0.9$），对每个 $Q$：

1. 计算 $M_{\text{total}}(Q)$ 的全部特征值
2. 计算谱间隙 $\gamma_{\text{total}}(Q) = 1 - \rho(K_{\text{total}}(Q))$ 的代理量 $\sigma_{\min}(M_{\text{total}}(Q))$
3. 计算耦合曲率 $R(Q)$

**IV 型奇异纤维判据**：

$$Q_c^{(s_i,s_j)} = \inf\{Q > 0 : |R^{(s_i,s_j)}(Q)| > \Theta_R \land \gamma_{\text{total}}(Q) < \Theta_\gamma\}$$

其中 $\Theta_R$（曲率阈值）和 $\Theta_\gamma$（谱间隙阈值）为经验参数。建议 $\Theta_R = 10 \cdot R(Q=0)$（曲率比未耦合时大一个数量级），$\Theta_\gamma = 0.1 \cdot \gamma_{\text{total}}(0)$（谱间隙下降一个数量级）。

**预期结果**：
- $Q_c^{(-2,-1)}$ 在 $Q \approx 0.3-0.4$ 范围（对 $a=0.9$），对应引力-电磁耦合融合
- $Q_c^{(-2,-1/2)}$ 在 $Q \approx 0.2-0.3$ 范围（对 $a=0.9$），对应引力-Dirac 耦合融合（Dirac 谱间隙更小，融合更早发生）
- $Q_c^{(-1,-1/2)}$ 在 $Q \approx 0.25-0.35$ 范围，介于两者之间

#### 3.4.3 参数空间的系统扫描

沿三个方向扩展 IV 型奇异纤维的相图：

| 扫描方向 | 范围 | 步长 | 目的 |
|:--------|:----|:----|:-----|
| $a$ 旋转 | $[0, 0.999]$ | $\Delta a = 0.1$（稀疏），$0.01$（$a>0.9$ 加密） | $a$ 对 $Q_c$ 的影响 |
| $Q$ 电荷 | $[0, 0.5M]$ | $\Delta Q = 0.01M$ | 耦合阈值定位 |
| $m$ 方位 | $\pm l$ | $\Delta m = 1$ | $(s_i,s_j)$ 耦合强度对 $m$ 的依赖 |

预计总扫描点数为：$15(a) \times 50(Q) \times 5(m) = 3750$ 个点，每个点计算 $3N \times 3N = 192\times 192$ 矩阵的 SVD（复杂度 $O((3N)^3) \approx 7\times 10^6$）。总计算量 $3750 \times 7\times10^6 \approx 2.6\times10^{10}$ 次运算，约 5 分钟（现代 CPU，使用 NumPy 加速）。

### 3.5 验证结果的可视化

| 图 | 类型 | $x$ 轴 | $y$ 轴 | 颜色/标记 |
|:--|:----|:------|:------|:---------|
| Fig. 1 | 散点 | $Q$ | $\sigma_{\min}$ | 自旋对颜色编码 |
| Fig. 2 | 热图 | $a$ | $Q$ | $|R(Q,a)|$ |
| Fig. 3 | 线图 | $Q$ | $\Delta\lambda_i(Q)$ | 特征值索引 |
| Fig. 4 | 热图 | $a$ | $Q$ | IV 型奇异纤维相图 |

---

## 4. $\infty$-范畴谱丛的形式化实现

### 4.1 问题背景

§8 提出了三条 $\infty$-范畴提升路径。Phase 31.1 已完成六个 Lean 4 模块（`AInfinityAlgebra`, `InfinityCategory`, `RecInfinity`, `SpecInfinity`, `DInfinityFunctor`, `SpectralFlowHomotopy`），通过 `lake build` 编译，但核心定理以 `sorry` 占位。

本文档将三条路径的具体实现方案细化到 Lean 4 代码层面。

### 4.2 路径 1：$\infty$-层粘合条件（优先级最高）

#### 4.2.1 需要形式化的数学内容

路径 1 的核心是 §8.1 的 $\infty$-层粘合条件：$(\infty,1)$-谱丛 $\tilde{\mathfrak{S}}^{(\infty,s)}$ 定义为 $\pi: \tilde{\mathfrak{S}}^{(\infty,s)} \to \mathfrak{S}^{(\infty,s)}$ 上的 $\infty$-层，满足下降条件。

**依赖关系**：

```
ℤ₂-覆盖（Paper XXIX §3）
    ↓
∞-层条件（定理 7.1 下降条件）
    ↓
$(\infty,1)$-谱丛定义
    ↓
与 Phase 31.1 Rec_∞ / Spec_∞ 对接
```

#### 4.2.2 Lean 4 实现结构

在 `SpectraInfinity.lean` 中定义 $(\infty,1)$-谱丛：

```lean4
import UFPFormalization.RecInfinity
import UFPFormalization.SpecInfinity
import Mathlib.CategoryTheory.InfinityCategory.SimplicialSet

open CategoryTheory
open Simplicial

/-!
# Paper XXIX §8 : (∞,1)-Spectral Sheaf with ℤ₂-Covering
  
This module formalizes the (∞,1)-categorical spectral sheaf that 
lifts the ℤ₂-covering structure of Dirac spectral sheaves.
-/

universe u v

/--
Structure of an (∞,1)-categorical spectral sheaf over a ℤ₂-covering.
-/
structure SpectraInfinity
  (S : Set ℕ)                          -- set of spin weights
  (C : Set Type*)                      -- parameter space (ℂ³ as simplicial set)
  [IsSimplicialSet C] :=
  (baseSheaf : C → Spec∞)             -- base spectral sheaf
  (covering : C → C)                  -- ℤ₂-covering map
  (descentData : (x y : C) →         -- descent condition (gluing)
    baseSheaf x → baseSheaf (covering x))
  (cocycleCondition : ∀ (x y z : C),  -- cocycle condition
    descentData x y ∘ descentData y z = descentData x z)
  (nonTrivialZ2 :                       -- non-trivial ℤ₂ obstruction
    H² (fundamentalGroupoid C) (ZMod 2) ≠ 0)
    -- this is the core theorem: H²(ℳ_ω, ℤ₂) ≠ 0 for s = ±1/2
```

#### 4.2.3 需要填充的核心定理

**定理 A**（$\infty$-下降条件 $\Rightarrow$ 下降数据的可积性）。

```lean4
theorem descentCocycleIntegrable (F : SpectraInfinity S C)
  (h : ∀ (x : C), (F.covering (F.covering x)) = x) :  -- ℤ₂ involution
  (sheafCondition F.baseSheaf) :=
by
  -- 需要从 descentData 满足 cocycleCondition 构造 Cech 下降同构
  -- 核心困难：将离散群上同调 H²(π₁, ℤ₂) 翻译为 ∞-范畴的 Postnikov 塔数据
  sorry
```

**定理 B**（$\mathbb{Z}_2$ 阻碍的 ∞-范畴表达）。

```lean4
theorem Z2ObstructionAsPostnikovInvariant (s : ℚ) (hs : s = 1/2 ∨ s = -1/2) :
  H² (MonodromyGroup s) (ZMod 2) ≠ 0 :=
by
  -- 使用定理 3.1 的置换条件 (3)，通过分支点加倍和单值群扩大构造非平凡 2-上循环
  sorry
```

### 4.3 路径 2：导出交义构造

#### 4.3.1 数学内容

路径 2 基于 §8.2 的导出纤维对应（定理 7.3），使用 $\pi: \mathfrak{S}^{(s)} \to \mathbb{C}^3$ 的导出推前 $R\pi_*(\mathcal{O})$ 构造完美导出纤维。

#### 4.3.2 Lean 4 实现

```lean4
import Mathlib.AlgebraicGeometry.DerivedCategory.PerfectComplex

/-! 
# Path 2: Derived fiber construction for the ∞-spectral sheaf
-/

structure DerivedFiberSpectralSheaf
  (S : Set ℕ)
  (X : Scheme)                          -- ℂ³ as algebraic variety
  [IsSmooth X] [DimEq X 3] :=
  (fibration : X → SpectralCategory)   -- fiber map
  (derivedPushforward : 
    PerfectComplex (DerivedCategory X))  -- Rπ_*(O)
  (supportCondition : 
    support derivedPushforward = image fibration)
  (perfectness : IsPerfectComplex derivedPushforward)
```

#### 4.3.3 与 Phase 31.1 的对接

Phase 31.1 的 `DInfinityFunctor.lean` 已经定义了 $\mathrm{D}_\infty: \mathbf{Rec}_\infty \to \mathbf{Sp}_\infty$。路径 2 需要在此基础上升级为导出纤维版本的 $\mathcal{E}_{\mathfrak{S}}$：

```lean4
-- Extend DInfinityFunctor to derived category
theorem derivedFiberCorrespondence
  (R : Rec∞) (S : Spec∞) (h : D∞ R = S) :
  PerfectComplex (DerivedCategory (parameterSpace R)) :=
by
  -- construct perfect complex from the spectral sheaf
  -- using the decursion functor D
  sorry
```

### 4.4 路径 3：SimpSet 方法

#### 4.4.1 数学内容

路径 3 使用单纯集合（Simplicial Set）直接构造 $\infty$-范畴，将谱丛编码为 SimpSet 的纤维化。

#### 4.4.2 实现计划

```lean4
import Mathlib.CategoryTheory.InfinityCategory.SimplicialSet

/-!
# Path 3: Simplicial set encoding of spectral sheaf
-/

structure SimplicialSpectralSheaf
  (S : Set ℕ)
  (Δ : SimplicialSet) :=
  (nerve : Δ → Set ℂ)                  -- nerve of spectral cover
  (fiberSimplex : (n : ℕ) → Δ [n] →    -- n-simplices encode
    (S → Matrix (ℂ) (ℂ)))             -- spectral data
  (KanCondition : IsKanFibration fiberSimplex)
```

### 4.5 三条路径的比较与优先级

| 路径 | 依赖 | 难度 | 与 Phase 31.1 的重叠 | 推荐优先级 |
|:---:|:----|:---:|:-------------------:|:---------:|
| 1: ∞-层粘合 | 定理 7.1 下降条件 | 高（需 ∞-层的理论形式化）| 中（`RecInfinity` + `SpecInfinity` 已实现）| **最高** |
| 2: 导出交义 | 定理 7.3 导出纤维 | 中（`DInfinityFunctor` 已实现）| 高（可复用 `DInfinityFunctor`）| 次之 |
| 3: SimpSet | 无额外依赖 | 低-中（SimpSet 理论成熟）| 低（需从头实现）| 最低 |

**推荐执行顺序**：路径 2 → 路径 1 → 路径 3

- **路径 2** 最直接：`DInfinityFunctor.lean` 已通过 `lake build`，只需补充导出纤维和完美复形的形式化
- **路径 1** 是最终目标：$\infty$-层粘合条件的完整形式化
- **路径 3** 作为备选：若路径 1/2 遇到理论困难，可用 SimpSet 方法提供替代实现

### 4.6 实施里程碑

| 里程碑 | 内容 | 预计工作量 | 依赖 |
|:------|:----|:---------:|:----|
| M1 | 填充 `DInfinityFunctor.lean` 的 `sorry`：证明 $D_\infty$ 函子性 | 1 周 | Phase 31.1 |
| M2 | 实现 `DerivedFiberSpectralSheaf.lean`：导出纤维结构与完美性验证 | 2 周 | M1 |
| M3 | 实现 `SpectraInfinity.lean`：$(\infty,1)$-谱丛定义与下降条件形式化 | 3 周 | 定理 7.1 证明 |
| M4 | 证明 `Z2ObstructionAsPostnikovInvariant` 定理 | 2 周 | M3, 定理 3.1 |
| M5 | 三路径集成测试 | 1 周 | M1-M4 |
| M6 | 与 `SilenceHierarchy.lean` 对接 | 1 周 | M5 |
| **总计** | | **10 周** | |

---

## 参考文献

[1] Dolan, S. R. & Gair, J. R. (2006). *Dirac quasinormal modes of the Kerr black hole.* arXiv:gr-qc/0612024.

[2] Cook, G. B. & Zalutskiy, M. (2014). *Gravitational perturbations of the Kerr geometry: High-accuracy study.* Phys. Rev. D 90, 124021.

[3] Berti, E., Cardoso, V. & Will, C. M. (2006). *On the computation of black hole quasinormal modes.* Phys. Rev. D 73, 064030.

[4] Stein, L. C. (2019). *qnm: A Python package for computing Kerr quasi-normal mode frequencies.* JOSS 4, 1623.

[5] Chandrasekhar, S. (1983). *The Mathematical Theory of Black Holes.* Oxford University Press.

[6] Lurie, J. *Higher Topos Theory* (HTT). Princeton University Press, 2009.
