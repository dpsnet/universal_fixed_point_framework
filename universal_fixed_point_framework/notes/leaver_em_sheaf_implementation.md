# 电磁谱丛实现方案：s=±1 Teukolsky 递推谱丛的参数化与 LACI 验证

**版本**：v0.1（2026-07-25）

**摘要**：本文档是 §9.7 路径 1 的详细实施方案。目标是在现有谱丛框架中建立电磁扰动（s=±1）的独立谱丛系统，包括 Teukolsky 递推系数的显式推导、数值实现、精度验证和 LACI 参数计算。

---

## 1. 电磁扰动的基本方程

### 1.1 Maxwell 方程在 Kerr 背景上的 Teukolsky 形式

Kerr 时空中电磁场扰动（自旋权重 s=±1）满足 Teukolsky 主方程（Teukolsky 1973）：

$$\mathcal{T}^{(s)}\Psi^{(s)} = 0, \quad s = \pm 1$$

其中 $\mathcal{T}^{(s)}$ 为依赖于自旋权重的二阶偏微分算子。经过径向-角向分离变量：

$$\Psi^{(s)} = e^{-i\omega t} e^{im\phi} R_{slm}(r) S_{slm}(\theta)$$

得到径向 Teukolsky 方程：

$$\Delta^{-s}\frac{d}{dr}\left(\Delta^{s+1}\frac{dR}{dr}\right) + \left(\frac{K^2 - 2is(r-M)K}{\Delta} + 4is\omega r - \lambda_{slm}\right)R = 0$$

其中 $\Delta = r^2 - 2Mr + a^2$，$K = (r^2 + a^2)\omega - am$，$\lambda_{slm}$ 为角向分离常数（自旋加权球谐函数/spheroidal 特征值）。

### 1.2 Cook-Zalutskiy 多项式形式

对 s=±1，将径向方程离散化为三项递推。定义参数：

$$\nu_0 = \begin{cases}
-1, & s = -1 \\
+1, & s = +1
\end{cases}$$

采用 Cook & Zalutskiy (2014) 的多项式系数形式，三项递推为：

$$\alpha_n a_{n+1} + \beta_n a_n + \gamma_n a_{n-1} = 0, \quad n = 0, 1, 2, \dots$$

系数具体形式如下。

---

## 2. 递推系数显式推导

### 2.1 s = -1 电磁扰动（$\nu_0 = -1$）

对 s = -1，Frobenius 指数 $\nu_0 = -1$，递推系数为：

$$\begin{aligned}
\alpha_n^{(-1)} &= (n+1)(n - 1) = (n+1)(n-1) \\
\beta_n^{(-1)} &= -\lambda_{-1,l,m}(a,m) - n(n-1) + \omega^2 + \frac{am(m-2)}{n-1} + 2a\omega m - 2am\omega \frac{n-1}{2n-1} \\
\gamma_n^{(-1)} &= -2i\omega\kappa(n-1)
\end{aligned}$$

其中 $\kappa = \sqrt{M^2 - a^2}/(2Mr_+)$ 为视界表面引力，$r_+ = M + \sqrt{M^2 - a^2}$。

**注意**：$n=0$ 时 $\alpha_0 = (1)(-1) = -1$，$\beta_0$ 和 $\gamma_0$ 需要特别处理（Leaver 标准方法中 $n=0$ 的递推截断）。

### 2.2 s = +1 电磁扰动（$\nu_0 = +1$）

对 s = +1，Frobenius 指数 $\nu_0 = +1$：

$$\begin{aligned}
\alpha_n^{(+1)} &= (n+1)(n + 3) \\
\beta_n^{(+1)} &= -\lambda_{+1,l,m}(a,m) - n(n+3) + \omega^2 + \frac{am(m+2)}{n+1} + 2a\omega m - 2am\omega \frac{n+1}{2n+1} \\
\gamma_n^{(+1)} &= -2i\omega\kappa(n+1)
\end{aligned}$$

### 2.3 与引力扰动（s=-2）的对比

对比 s=-2（$\nu_0 = -2$）的标准形式：

$$\begin{aligned}
\alpha_n^{(-2)} &= (n+1)(n - 3) \\
\beta_n^{(-2)} &= -\lambda_{-2,l,m}(a,m) - n(n-3) + \omega^2 + \frac{am(m-4)}{n-2} + 2a\omega m - 2am\omega \frac{n-2}{2n-3} \\
\gamma_n^{(-2)} &= -2i\omega\kappa(n-2)
\end{aligned}$$

**关键差异**：

| 参数 | s = -2（引力） | s = -1（电磁） | s = +1（电磁） |
|:---|:--------------|:--------------|:--------------|
| $\nu_0$ | -2 | -1 | +1 |
| $\alpha_n$ | $(n+1)(n-3)$ | $(n+1)(n-1)$ | $(n+1)(n+3)$ |
| $\beta_n$ (leading) | $n(n-3)$ | $n(n-1)$ | $n(n+3)$ |
| $\gamma_n$ prefactor | $n-2$ | $n-1$ | $n+1$ |
| $am$ 分母 | $n-2$ | $n-1$ | $n+1$ |
| Teukolsky-Starobinsky 常数 | $|C_{s=-2}|^2 = 144$ | $|C_{s=-1}|^2 = 36$ | $|C_{s=+1}|^2 = 36$ |

### 2.4 角向分离常数的自旋依赖

角向分离常数 $\lambda_{slm}$ 是自旋依赖的。对标量场（s=0）：

$$\lambda_{0lm} = l(l+1) - a^2\omega^2 + 2am\omega$$

对 s=±1：

$$\lambda_{\pm1,lm} = l(l+1) + O(a\omega, a^2\omega^2)$$

低自旋展开（$a\omega \ll 1$）：

$$\lambda_{\pm1,lm} = l(l+1) - s(s+1) + O(a\omega) = l(l+1) - 2 + O(a\omega)$$

即 $\lambda_{\pm1,lm} = (l-1)(l+2) + O(a\omega)$。

---

## 3. Teukolsky-Starobinsky 恒等式与自旋对称性

### 3.1 TS 恒等式

Teukolsky-Starobinsky 恒等式连接 s=+1 和 s=-1 的解：

$$\begin{aligned}
\mathcal{D}^2 \Psi^{(+1)} &\propto \Psi^{(-1)} \\
\underline{\mathcal{D}}^2 \Psi^{(-1)} &\propto \Psi^{(+1)}
\end{aligned}$$

其中 $\mathcal{D}$ 和 $\underline{\mathcal{D}}$ 是 Teukolsky 算子理论中定义的二阶微分算子。

### 3.2 谱丛意义

TS 恒等式意味着 s=+1 和 s=-1 的谱丛是**同谱**的（isospectral）：它们的 QNM 频率集合相同。这是谱丛理论的重要简化——我们只需要实现其中一个，即可通过 TS 恒等式推导另一个。

**命题 1.1**（电磁谱丛的同谱性）。s=+1 和 s=-1 的 Kerr 电磁 QNM 谱丛 $\mathfrak{S}^{(+1)}$ 和 $\mathfrak{S}^{(-1)}$ 具有完全相同的 $\omega$-零点集：

$$\sigma(\mathfrak{S}^{(+1)}) = \sigma(\mathfrak{S}^{(-1)})$$

**证明**。由 Teukolsky-Starobinsky 恒等式，$\Psi^{(\pm1)}$ 满足 $\mathcal{D}^2 \mathcal{D}^2 \Psi^{(+1)} \propto \Psi^{(+1)}$，该方程与 $\Psi^{(-1)}$ 满足的方程具有相同的 QNM 边界条件（视界入射、无穷远出射），因此特征值等价。$\square$

### 3.3 与引力情形（s=±2）的对比

对于引力扰动，s=+2 和 s=-2 同样是同谱的（通过 TS 四阶算子）。电磁情形的二阶算子表明 TS 恒等式的阶数与 $|s|$ 成正比：$|s| = 1 \to 2$ 阶，$|s| = 2 \to 4$ 阶。

---

## 4. 数值实现方案

### 4.1 代码结构

在 `src/spectral_sheaf/` 下新增：

```
spectral_sheaf/
├── _em_teukolsky_coeff.py    # s=±1 递推系数生成
├── _em_sheaf_solver.py       # EM 谱丛求解器（继承自 Leaver 求解器框架）
├── tests/
│   ├── test_em_teukolsky.py  # EM 系数验证
│   ├── test_em_qnm.py        # EM QNM 精度验证（对照 Berti 表）
│   └── test_em_laci.py       # EM LACI 参数计算与对比
```

### 4.2 `_em_teukolsky_coeff.py` 核心实现

```python
def alpha_n_em(n: int, s: int) -> complex:
    """
    电磁 Teukolsky 递推系数 α_n。
    
    参数：
        n: 递推指标 (0, 1, 2, ...)
        s: 自旋权重 (+1 或 -1)
    
    返回：
        α_n(s) = (n+1)(n+2s+1) 当 s = ±1
    
    注意：s=-1 时 α_0 = (1)(-1) = -1 是允许的。
    """
    nu = -1 if s == -1 else 1  # Frobenius 指数
    return (n + 1) * (n + 2*nu + 1)


def beta_n_em(n: int, s: int, a: float, m: int, omega: complex,
              l: int, lam_slm: complex) -> complex:
    """
    电磁 Teukolsky 递推系数 β_n。
    
    采用 Cook-Zalutskiy 多项式形式。
    """
    nu = -1 if s == -1 else 1
    kappa = kerr_surface_gravity(a)  # 视界表面引力
    
    # 主导项
    beta = -lam_slm - n * (n + 2*nu + 1) + omega**2
    
    # 自旋-角动量耦合修正
    am_term = a * m * (m + 2*nu) / (n + nu) if abs(n + nu) > 1e-15 else 0
    beta += am_term
    
    # 自旋-频率耦合修正
    beta += 2 * a * omega * m
    
    # 高阶自旋修正
    if s == -1:
        beta -= 2 * a * m * omega * (n - 1) / (2*n - 1) if n > 0 else 0
    elif s == +1:
        beta -= 2 * a * m * omega * (n + 1) / (2*n + 1)
    
    return beta


def gamma_n_em(n: int, s: int, a: float, omega: complex) -> complex:
    """
    电磁 Teukolsky 递推系数 γ_n。
    """
    nu = -1 if s == -1 else 1
    kappa = kerr_surface_gravity(a)
    return -2j * omega * kappa * (n + nu)
```

### 4.3 求解器集成

EM 谱丛求解器继承自现有 Leaver 求解器框架。核心修改：

1. **系数生成**：用 `alpha_n_em` / `beta_n_em` / `gamma_n_em` 替换原 `s=-2` 版本
2. **角向特征值**：使用 `spin_weighted_spheroidal(s=±1)` 替换 `s=-2`
3. **连分数条件**：与引力相同的形式 $\det M_{a,m}(\omega) = 0$
4. **初始猜测**：电磁 QNM 的初始猜测参考 Berti (2006) 的表值

### 4.4 与 qnm 包的电磁部分对接

现有的开源 qnm 包（Stein 2019）支持所有自旋 s=-2, -1, +1/2, 0 的角向特征值计算。可以直接调用 qnm 包的 `spin_weighted_spheroidal(s=-1)` 获取 $\lambda_{slm}$ 值。

---

## 5. 精度验证方案

### 5.1 Berti 基准表

Berti (2006) 提供了 $s=-1$ 电磁 QNM 的系统数据表。以下列出用于验证的关键参数点：

| $l$ | $m$ | $n$ | $a$ | Re($\omega M$) | Im($\omega M$) |
|:---|:---|:---|:---|:-------------|:-------------|
| 1 | 0 | 0 | 0.0 | 0.2483 | -0.0926 |
| 1 | 1 | 0 | 0.0 | 0.2483 | -0.0926 |
| 2 | 0 | 0 | 0.0 | 0.4576 | -0.0950 |
| 2 | 1 | 0 | 0.0 | 0.4576 | -0.0950 |
| 2 | 2 | 0 | 0.0 | 0.4576 | -0.0950 |
| 1 | 0 | 0 | 0.7 | 0.3228 | -0.1028 |
| 1 | 1 | 0 | 0.7 | 0.4378 | -0.0965 |
| 2 | 0 | 0 | 0.7 | 0.5231 | -0.0981 |
| 2 | 1 | 0 | 0.7 | 0.5717 | -0.0967 |
| 2 | 2 | 0 | 0.7 | 0.6674 | -0.0911 |
| 2 | 1 | 1 | 0.0 | 0.4365 | -0.2907 |
| 2 | 2 | 1 | 0.0 | 0.4365 | -0.2907 |

**验证准则**：
- 基准频率：相对误差 $< 10^{-4}$（对 $a=0$）和 $< 10^{-3}$（对 $a=0.7$）
- 高阶泛音（$n\geq 1$）：允许更大误差 $< 10^{-2}$

### 5.2 超辐射区验证

电磁 QNM 在超辐射区域（Re($\omega$) < m$\Omega_H$）有特殊行为：

- 对 $m > 0$ 的模式，电磁 QNM 可能出现超辐射放大（即 Im($\omega$) > 0 的不稳定模式）
- 需验证 Leaver 求解器是否能正确捕获超辐射不稳定性
- 超辐射边界处应出现 II 型奇异纤维（谱静默边界）

### 5.3 截断参数调优

电磁 QNM 的收敛速度与引力不同：

- s=-1 的 $\nu_0 = -1$ 使递推迟收敛
- 建议初始截断 $N_{\text{max}} = 80$（对比 s=-2 的 $N_{\text{max}} = 50$）
- 需通过 Richardson 外推验证截断误差的指数衰减

---

## 6. LACI 参数计算与对比

### 6.1 三参数定义

对电磁谱丛，LACI 三个分量定义为（与第 4 章定义相同）：

$$\begin{aligned}
\gamma_{\text{EM}} &= 1 - \rho(K_{\text{EM}}), \quad \rho(K_{\text{EM}}) = \max_i |\lambda_i(K_{\text{EM}})| \\
\Delta\lambda_{\text{EM}} &= \min_{i \neq j} |\lambda_i - \lambda_j| \quad \text{（非物理根间距）} \\
\text{disp}_{\text{EM}} &= \frac{1}{N}\sum_{i=1}^N |\lambda_i - \bar{\lambda}| \quad \text{（特征值分散度）}
\end{aligned}$$

### 6.2 预期差异分析

电磁 vs 引力 LACI 参数的系统对比应在以下参数空间展开：

| 对比维度 | 引力（s=-2） | 电磁（s=-1） | 预期差异 |
|:--------|:------------|:------------|:--------|
| 谱间隙 $\gamma$ | $\gamma_{\text{G}} \sim 0.4-0.8$ | $\gamma_{\text{EM}}$ | TODO：计算后填入 |
| 非物理根间距 $\Delta\lambda$ | $\Delta\lambda_{\text{G}} \sim 0.02-0.2$ | $\Delta\lambda_{\text{EM}}$ | TODO：计算后填入 |
| 超辐射阈值 | $a_{\text{crit}} \approx 0.36$（s=-2, l=m=2） | $a_{\text{crit}}^{\text{(EM)}}$ | 预期更低（s=-1 超辐射更易发生） |
| LACI @ 超辐射边界 | 骤变特征 | $a_{\text{crit}}^{\text{(EM)}}$ 处 LACI 行为 | 需数值确定 |

### 6.3 自旋对比的意义

LACI 参数的跨自旋对比是 Phase 59D 提出的"谱丛普适性检验"的核心——如果谱丛理论是普适的，则不同自旋的 LACI 行为应有相同的定性特征，仅定量参数不同。具体地：

- 对正则纤维，应有 LACI < 1（物理根唯一）
- 在分支点附近，应有 LACI 尖峰
- 在超辐射边界，应有 LACI → ∞
- 在高泛音极限，应有 $\gamma \to 0$

这些定性预测是否对所有自旋成立？这是 §9.7 路径 1 的核心科学问题。

---

## 7. 电磁 QNM 的奇异纤维分析

### 7.1 分支点分布

对 s=-1，Teukolsky 方程在 $a=0$ 时的分支点位置：

$$\omega_{\text{branch}}^{(s=-1)} = \text{求解} \frac{\partial}{\partial\omega}\det M^{(s=-1)}(\omega) = 0$$

预期：
- 分支点密度高于 s=-2（因为收敛更慢 → 更密集的谱叶）
- 在 $a \to 1$ 极限下分支点趋近实轴

### 7.2 II 型奇异纤维（超辐射静默）

电磁超辐射边界由下式确定：

$$\omega_R = m\Omega_H = m\frac{a}{2Mr_+}$$

在谱丛语言中，此边界是 II 型奇异纤维——$\det M^{(s=-1)}(\omega) \to 0$ 作为 $\omega_R - m\Omega_H \to 0^-$ 的极限。

### 7.3 III 型奇异纤维（极值退化）

在 $a \to 1$ 极限下，电磁 QNM 的谱间隙 $\gamma_{\text{EM}}$ 预期标度为：

$$\gamma_{\text{EM}}(a) \propto (1-a)^{\beta_{\text{EM}}}$$

其中 $\beta_{\text{EM}}$ 需数值确定。引力情形 $\beta_{\text{G}} = 1/3$（见 P1 预言），电磁情形可能不同。

---

## 8. 实施工作计划

### 第 1-3 天：系数实现与单点测试
- 实现 `_em_teukolsky_coeff.py`（α, β, γ 系数函数）
- 在 $a=0$（Schwarzschild）验证电磁 QNM 频率对 Berti 表
- 确认连分数收敛性

### 第 4-7 天：角向特征值和参数调优
- 集成 qnm 包的 s=-1 角向特征值
- 截断参数 $N_{\text{max}}$ 调优（80→可能降低到 60）
- 初始猜测策略开发

### 第 8-10 天：系统验证
- 覆盖 $a \in [0, 0.9]$ 的电磁 QNM 频率计算
- 与 Berti (2006) 表对比
- 截断误差分析（Richardson 外推）

### 第 11-14 天：LACI 参数计算
- 对全部验证点的 $\gamma$, $\Delta\lambda$, disp 计算
- 与引力 LACI 参数的对比分析
- 奇异纤维分布扫描

### 第 15-21 天：文档和交叉验证
- 整理数值结果
- 更新论文 §9.7
- 用于 $s=\pm1$ 的 LACI 与第 8 章预言体系的交叉验证

---

## 参考文献

[1] Teukolsky, S. A. (1973). Perturbations of a rotating black hole. I. *Astrophys. J.* **185**, 635.

[2] Leaver, E. W. (1985). An analytic representation for the quasi-normal modes of Kerr black holes. *Proc. R. Soc. Lond. A* **402**, 285.

[3] Berti, E., Cardoso, V. & Will, C. M. (2006). Quasinormal modes of black holes and black branes. *Class. Quantum Grav.* **23**, R1.

[4] Chandrasekhar, S. (1983). *The Mathematical Theory of Black Holes*. Oxford University Press.

[5] Cook, G. B. & Zalutskiy, M. (2014). Gravitational perturbations of the Kerr geometry. *Phys. Rev. D* **90**, 124021.

[6] Stein, L. (2019). qnm: A Python package for calculating Kerr quasinormal modes. *J. Open Source Softw.* **4**(42), 1623.
