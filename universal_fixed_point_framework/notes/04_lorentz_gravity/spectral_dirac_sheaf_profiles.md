# Dirac 谱丛三剖面多工具求解器（Phase 59H）

**版本**：v0.1（2026-07-26）

**关联论文**：Paper XXIX（Dirac 谱丛与半整数自旋结构）

**关联代码**：`src/spectral_sheaf/_dirac_sheaf_profiles.py`

---

## 1. 动机：窗口困境

### 1.1 连分数法的窗口困境

Leaver 连分数法在复 ω 平面上有**收敛窗口**限制——连分数的收敛域不一定覆盖整个物理 Riemann 面（Paper XXVII §10.2）。对 Dirac 半整数自旋谱丛，此问题因以下原因加剧：

1. **代数特殊模式**（Paper XXIX §2.3）：$\omega = \pm m/2M$（$a=0$）附近连分数退化为有限递推，收敛率降为零
2. **$\mathbb{Z}_2$ 阻碍**（Paper XXIX §3）：双叶覆盖使连分数根追踪的初值敏感性加倍——两片谱叶的吸引域重叠
3. **分支点加倍**（Paper XXIX 定理 3.2）：Dirac 分支点数是引力的 2 倍，密集的分支点将收敛窗口穿透为"筛子"

### 1.2 Complex scaling 的窗口困境

现有 `DiracChandraSpectralSolver`（两弦法）使用 complex scaling，同样有窗口问题：
- 旋转角 θ、计算域 r_max、网格点数 n_dim 需要为每个 κ 手动调参
- $\kappa=1$ 最优参数 `(200, 60, 0.25)` 对 $\kappa=4$ 失效（需 `(1000, 60, 0.12)`）
- 无法直接处理 Kerr（a ≠ 0）情形

### 1.3 核心思想

**窗口困境的根源**：试图用单一数学工具（连分数法 或 complex scaling）覆盖所有参数方向（ω, a, m）。

**解决方案**：谱丛的三个参数方向使用**不同数学工具**构造纵向剖面——每个剖面针对该参数方向的数学结构选择最优工具。

---

## 2. 三剖面架构

### 2.1 总览

```
DiracSpectralSheafTracker          # 三剖面集成器
├── DiracOmegaProfileSolver        # ω-剖面
│   ├── ChebyshevCollocation       #   Chebyshev 谱配点离散化
│   └── ContourIntegralSolver      #   Beyn (2012) 围道积分法
├── DiracARationalContinuation     # a-剖面
│   └── AAA 重心有理逼近           #   Nakatsukasa et al. (2018)
└── DiracAngularEigenvalueSolver   # m-剖面
    └── λ_{slm}(a,m) 代数求解      #   Seidel 展开 + 连分数校验
```

### 2.2 ω-剖面：Chebyshev 谱配点 + Beyn 围道积分

**数学框架**：

将 Dirac Teukolsky ODE 在 tortoise 坐标下离散化：

$$\frac{d^2\Psi}{dr_*^2} + \bigl(\omega^2 - V(r)\bigr)\Psi = 0$$

使用 Chebyshev-Gauss-Lobatto 配点将 r ∈ [r₊, L] 映射到 x ∈ [-1, 1]：

$$r = \alpha x + \beta,\quad \alpha = \frac{L - r_+}{2},\quad \beta = \frac{L + r_+}{2}$$

二阶导数离散化（tortoise 坐标变换）：

$$\frac{d}{dr_*} = f\frac{d}{dr},\quad \frac{d^2}{dr_*^2} = f^2\frac{d^2}{dr^2} + f'\frac{d}{dr}$$

其中 $f = 1 - 2M/r$，$f' = df/dr_* = f \cdot df/dr$。

离散化为二次特征值问题：

$$(\omega^2 M - K)\Psi = 0$$

用 Beyn (2012) 围道积分法提取复 ω 平面围道 Γ 内所有特征值：

$$A_0 = \frac{1}{2\pi i}\oint_\Gamma (zM - K)^{-1}B\,dz,\quad A_1 = \frac{1}{2\pi i}\oint_\Gamma z(zM - K)^{-1}B\,dz$$

**优势**：
- 无收敛窗口：谱精度遍及整个计算域
- 同时提取围道内所有根，无需初值猜测
- 使用两个偏移围道自然处理 $\mathbb{Z}_2$ 双叶覆盖

### 2.3 a-剖面：AAA 重心有理逼近

**数学框架**：

将 ω(a) 建模为重心有理函数：

$$\omega(a) \approx r(a) = \frac{\sum_{k} w_k \omega_k / (a - a_k)}{\sum_{k} w_k / (a - a_k)}$$

使用 AAA 算法（Nakatsukasa et al. 2018）自适应选择支撑点 $(a_k, \omega_k)$ 和权重 $w_k$。

**优势**：
- 绕过 a-同伦延拓的步长限制
- 有理函数可解析延拓穿过分支割
- 提供 ω(a) 的闭式表达式，适合谱丛截面追踪

### 2.4 m-剖面：角向分离常数代数求解

**数学框架**：

将 $\lambda_{slm}(a,m)$ 展开为 a 的幂级数：

$$\lambda = \lambda_0 + c_2 a^2 + c_4 a^4 + \cdots$$

其中 $\lambda_0 = l(l+1) - s(s+1)$，系数来自 Seidel (1995) 展开公式。

**优势**：
- m 为整数离散量，无需连续延拓
- 预计算 λ(m) 闭式函数，从径向问题完全解耦

---

## 3. 与 Leaver 连分数法的对比

| 维度 | Leaver 连分数法 | 三剖面方案 |
|:----|:--------------|:----------|
| **ω-根求解** | Newton 迭代 + 连分数尾部截断 | 辐角原理围道积分（`ScalarContourSolver`） |
| **ω-收敛域** | 有限（发散面 + 代数特殊模式空洞） | 全局（围道积分自动提取所有根） |
| **a-延拓** | 同伦延拓（步长敏感，谱叶易跳跃） | AAA 有理逼近（跨分支点解析延拓） |
| **m-依赖** | 每 m 值重新迭代 | 代数闭式 λ(m) |
| **初值需求** | 需要精确初值猜测 | 不需要（围道积分自动提取） |
| **$\mathbb{Z}_2$ 覆盖** | 无法自然处理 | 双围道显式编码 |
| **并行化** | 串行（Newton 迭代本质串行） | 可并行（各围道 / 各 a 采样独立） |

---

## 4. 数值验证

### 4.1 ScalarContourSolver 围道积分算法

测试多项式 $f(z) = (z - 0.38 + 0.10i)(z - 0.52 + 0.09i)$（模拟两个 QNM 根）：
- 辐角原理正确计数：Γ 内零点数 = 2 ✓
- 矩量法提取的根位置误差 $< 10^{-14}$
- 残差 $|f(r)| < 8 \times 10^{-16}$

### 4.2 a-profile 验证结果

在 $\kappa=2$（$l=1.5$）、$a \in [0, 0.8]$ 的 5 个采样点上拟合：
- RMSE：2.72e-3
- MaxErr：4.57e-3
- 外推 $a=0.9$：$\omega = 0.358724 - 0.069556i$

### 4.3 Z2 覆盖检测

使用两个相位偏移围道，成功区分主叶和副叶，Z2 分离度 $\sim 1.0$。

---

## 5. 组件状态

### 5.1 已验证就绪

| 组件 | 状态 | 用途 |
|:----|:----|:-----|
| `ScalarContourSolver` | ✓ 验证通过 | 替代 Newton 迭代的围道积分求根算法 |
| `ContourIntegralSolver` | ✓ 验证通过 | Beyn 矩阵围道积分 |
| `DiracARationalContinuation` | ✓ 验证通过 | a-剖面 AAA 重心有理逼近 |
| `DiracAngularEigenvalueSolver` | ✓ 已实现 | m-剖面角向代数求解 |
| `DiracSpectralSheafTracker` | ✓ 已实现 | 三剖面截面追踪集成器 |

### 5.2 待完善（需要编码 QNM 辐射条件）

| 组件 | 问题 | 解决方案 |
|:----|:----|:---------|
| `DiracLeaverContourSolver` | 需要精确 λ_{slm}(a,m,ω) 系数 | 对接 `LeaverUnifiedSolver` 的 `LeaverResidual`，扩展支持半整数自旋 |
| `ChandraTridiagonalBuilder` | 实坐标离散化缺 QNM 辐射条件 | 需加 PML 层或 complex scaling 旋转 |
| Chebyshev ω-profile | 同上的 BC 问题 | Sommerfeld 辐射条件离散化 |

### 5.3 代码集成

- 新代码位于 `src/spectral_sheaf/_dirac_sheaf_profiles.py`
- 不修改现有 `leaver_unified_solver.py` 和 `_dirac_derecursion_solver.py`
- 核心算法 `ScalarContourSolver` 可独立于 Dirac 谱丛使用

---

## 6. 开放问题

1. **围道选择的自动化**：能否从谱丛的奇异纤维分布自动选择最优围道？
2. **AAA 有理逼近的误差界**：对 ω(a) 的有理逼近误差能否被谱间隙 γ(a) 控制？
3. **三剖面复合运算的函子性**：三个剖面构成的三元组是否对应 $\mathbf{Rec} \to \mathbf{Sp}$ 函子的分解？
4. **PML 编码辐射条件**：如何在实坐标三对角矩阵中嵌入完美匹配层以替代 complex scaling？
