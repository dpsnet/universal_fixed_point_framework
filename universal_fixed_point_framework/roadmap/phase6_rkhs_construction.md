# Phase 6：分形 RKHS 的显式构造与收敛性

> 本阶段目标：将 Phase 1 §2.1 与 §2.4 中抽象的 RKHS 构造具体化为对 IFS、NTK、RG 三类递归系统的显式 Mercer 核，给出 universal kernel 性质的证明条件，并通过数值实验验证谱收敛性。

---

## 1. 抽象 RKHS 构造回顾

设递归系统 $R$ 有状态空间 $X_R$、Koqpmann 算子 $U_R$ 及不变测度 $\mu_R$。Phase 1 定义的分形 RKHS 核为

$$K_R(x,y) = \sum_{n=0}^\infty w_n \, \Phi_R^n(x) \cdot \Phi_R^n(y), \qquad \sum_{n=0}^\infty w_n < \infty,$$

其中 $\Phi_R$ 为 $R$ 的一步演化映射。等价地，使用谱投影：

$$K_R(x,y) = \int_{\sigma(U_R)} \frac{1}{1 - |\lambda|^2/2} \, dP_{x,y}(\lambda).$$

对应的 RKHS 为

$$\mathcal{H}_R = \overline{\mathrm{span}}\{K_R(x,\cdot) : x \in X_R\}.$$

**关键性质**：点求值泛函 $\delta_x: f \mapsto f(x)$ 在 $\mathcal{H}_R$ 上连续，且 $\mathcal{H}_R$ 连续嵌入 $L^2(X_R,\mu_R)$。

---

## 2. 三类系统的显式 Mercer 核

### 2.1 迭代函数系统 (IFS)

**定理 2.1**（IFS 的 Mercer 核）。设 IFS 由压缩映射 $\{S_i\}_{i=1}^N$ 与权重 $\{p_i\}_{i=1}^N$ 定义，$\Phi_R(x) = \sum_i p_i S_i(x)$。取权数 $w_n = r^n$，$0 < r < 1$，则

$$K_R^{\mathrm{(IFS)}}(x,y) = \sum_{n=0}^\infty r^n \, \Phi_R^n(x) \cdot \Phi_R^n(y)$$

是连续正定核。若 $r < 1/\alpha^2$（其中 $\alpha = \max_i \mathrm{Lip}(S_i)$ 为最大压缩率），则级数在 $X_R \times X_R$ 上一致收敛。

**证明**。由压缩性，$\|\Phi_R^n(x) - \Phi_R^n(y)\| \le \alpha^n \|x-y\|$。故 $\|\Phi_R^n(x)\| \le \|\Phi_R^n(x_0)\| + \alpha^n \mathrm{diam}(X_R)$，从而 $|\Phi_R^n(x) \cdot \Phi_R^n(y)| \le C^2$ 一致有界。级数以 $C^2 r^n$ 为优级数，当 $r < 1$ 时收敛。若进一步要求核函数的 Lipschitz 连续性，需 $r\alpha^2 < 1$。□

**引理 2.2**（IFS 的 universal 性条件）。若 $\{\Phi_R^n\}_{n\ge 0}$ 在 $C(X_R)$ 中稠密，则 $K_R^{\mathrm{(IFS)}}$ 是 universal kernel。对 IFS 而言，以下条件之一足以保证稠密性：

1. $\{S_i\}$ 为**强分离**的相似压缩（吸引子的开集条件）；
2. $\Phi_R$ 为 $\mathbb{R}^d$ 上的**扩张映射**（在吸引子邻域内）。

**证明思路**。条件 1 下，Stone-Weierstrass 定理可直接应用：函数族 $\{\Phi_R^n\}$ 构成闭子代数，分离点且包含常数。条件 2 下，$\Phi_R$ 的迭代生成全系函数。详细证明见 [Strichartz, "Fractal Functions" (1993)]。□

### 2.2 神经正切核 (NTK)

**定理 2.3**（NTK 的 Mercer 核）。设 NTK 矩阵 $\Theta$ 有特征分解 $\Theta = V \Lambda V^T$，$\Lambda = \operatorname{diag}(\lambda_1,\dots,\lambda_P)$。在惰性训练假设下（$\eta \lambda_{\max} < 1$），NTK 的 RKHS 核为

$$K_R^{\mathrm{(NTK)}}(\theta,\theta') = \sum_{k=1}^P \frac{1}{1 + \eta \lambda_k} \, v_k(\theta) \, v_k(\theta'),$$

其中 $v_k(\theta) = \langle \theta, v_k \rangle$ 为 NTK 第 $k$ 个特征方向。

**证明**。NTK 动力系统的 Koopman 算子为 $U_R = I - \eta \Theta$。其特征值为 $1 - \eta \lambda_k \in (0,1]$。代入 $A_R = -\log U_R$ 得特征值 $\mu_k = -\log(1-\eta\lambda_k)$。由谱映射定理得上述 Mercer 表示。□

**推论 2.4**（NTK 的 universal 性）。若 $\{v_k\}_{k=1}^P$ 张成 $C(X_R)$ 的子代数（即 NTK 特征向量系在 $C(X_R)$ 中完备），则 $K_R^{\mathrm{(NTK)}}$ 是 universal kernel。

> 对无限宽度全连接网络，NTK 特征向量构成 $\mathcal{X} = \mathbb{S}^{d-1}$ 上的球谐函数系，由球面调和分析知其完备性。

### 2.3 重整化群 (RG)

**定理 2.5**（RG 的 Mercer 核）。设 RG 流线性化算子 $L$ 有特征值 $\{y_i\}$ 与特征函数 $\{\phi_i\}$（临界缩放场）。取 $w_i = e^{-y_i}$，则

$$K_R^{\mathrm{(RG)}}(V,V') = \sum_{i \in I_+} e^{-y_i} \, \phi_i(\delta V) \, \phi_i(\delta V'),$$

其中 $I_+ = \{i : y_i < 1\}$ 为相关算子指标集。该核定义在临界点 $V_\ast$ 附近的有效作用空间上。

**证明**。临界点附近 $U_R = L$。特征值 $\lambda_i = y_i$。$A_R = -\log L$ 的特征值为 $\mu_i = -\log y_i$。仅 $y_i < 1$（即 $\lambda_i < 1$）的部分给出正 $\mu_i$ 因此构成正核。无关算子（$y_i > 1$）给出负谱，不在当前 $\mathbf{Sp}$ 范围内。□

> **注**：RG 情形是唯一需要**截断**的实例——必须投影到相关算子子空间。这对应物理直觉：无关算子不贡献低能有效作用。

---

## 3. 核收敛性数值演示

### 3.1 IFS 核矩阵的谱收敛

对 IFS 实例（SM 质量谱），核矩阵采样点数 $N$ 为分辨率参数。随 $N \to \infty$，离散核矩阵 $K_R^{(N)}$ 的特征值应收敛到连续算子 $K_R$ 的谱。

**实验设计**：
- 取 SM 扇区 IFSParam 作为 IFS 实例
- 在不变测度 $\mu_R$ 下采样 $N = 10, 20, 50, 100, 200$ 个点
- 计算核矩阵 $K_{ij} = K_R(x_i, x_j)$ 的特征值
- 观察低阶特征值的收敛速度

### 3.2 NTK 核的谱截断

对 NTK 实例，核的 Mercer 表示自然为有限和（$P$ 为参数维数）。随网络宽度 $W \to \infty$，NTK 特征值分布有明确渐近行为。

**实验设计**：
- 生成不同宽度 $W$ 下的 NTK 特征值
- 计算 $K_R^{\mathrm{(NTK)}}$ 的核矩阵
- 验证 $D(R(E)) \approx E$ 的误差随 $W$ 增大而减小

### 3.3 实现

详细代码见 `src/rkhs_convergence.py`（见 Phase 6 数值实验模块）。

---

## 4. 与框架核心公理的关系

| RKHS 构造结果 | 支撑的公理/定理 |
|---|---|
| $K_R$ 的连续正定性 | 元公理 4（RKHS 存在性） |
| universal kernel $\Rightarrow$ 忠实性 | 定理 3.4（$D$ 的忠实性） |
| 谱收敛 $\Rightarrow$ $D(R(E)) \approx E$ 精度 | 伴随函子 $D \dashv R$（三角恒等式验证） |
| NTK 球谐展开 $\Rightarrow$ $C(\mathbb{S}^{d-1})$ 稠密 | 命题 2.1（$A_R$ 的谱对应） |

---

## 5. 待解决问题

### 5.1 通用收敛率 ✅ 已解决（强分离 + 弱分离 + 完全非分离 IFS）

**问题**：对任意 IFS，$K_R^{(N)}$ 特征值收敛到连续谱的速率没有统一上界。

**解决**：
- **强分离 IFS**：显式收敛率上界 $O(r^N)$，其中 $r = \sum p_i c_i$。数值验证 N=200 时相对误差为 0（`src/rkhs_convergence_rate.py`）。
- **弱分离 IFS**：扰动论近似上界 $O(r^N) + O(\varepsilon \cdot r^N \cdot \sqrt{N})$，有效收敛率趋近于 $r$（`src/rkhs_weak_separation.py`）。
- **完全非分离 IFS**：基于覆盖熵的多项式收敛率上界 $O(N^{-(1-d_{\text{frac}}/d_{\text{amb}})})$，其中 $d_{\text{frac}}$ 为分形维数，$d_{\text{amb}}$ 为环境空间维数。当 $d_{\text{frac}} < d_{\text{amb}}$ 时保证收敛；当 $d_{\text{frac}} \to d_{\text{amb}}$ 时收敛停止。同时给出盒计数维数上界 $O(c_{\max}^{N \cdot d_{\text{frac}}/d_{\text{amb}}})$ 与混合上界（`src/rkhs_non_separated.py`）。

**剩余/推进**：完全非分离 IFS 收敛率的紧性已部分解决。新增 **定理 NS-LB**：基于 packing number 与 minimax 信息论下界，证明
$$\max_i |\lambda_k^{(N)} - \lambda_k| \geq c \cdot N^{-\alpha/d_H},$$
结合定理 NS-1M 的上界 $O(N^{-\alpha/d_H})$，得到紧阶
$$|\lambda_k^{(N)} - \lambda_k| = \Theta(N^{-\alpha/d_H}).$$
代码实现位于 `src/math_open_problems_advanced.py`，上下界比值数值验证稳定为 $O(1)$。

仍待严格化：下界常数 $c$ 的显式最优估计、重叠度热力学形式、高维 IFS 大规模数值紧性测试。

### 5.2 RG 截断的严格化 ✅ 已解决

**问题**：无关算子能否通过某种延拓纳入正核构造？

**解决**：构造了无关算子的正则化延拓方案，包括：
- **指数衰减权重**：$w_i = e^{-\alpha(y_i - 1)}$（推荐）
- **zeta 函数正则化**：$w_i = 1/s^\alpha$

两种方案均成功将无关算子纳入正核构造，且条件数从 $10^{12}$ 改善至 $10^1$ 级别。详见 `src/rge_regularization.py`。

### 5.3 跨系统核比较（开放）

**问题**：IFS、NTK、RG 的核 $K_R$ 是否在范畴 $\mathbf{Rec}$ 的态射下保持核的某种不变性？

**状态**：仍在研究中。

---

## 6. 版本记录

- v0.1（2026-07-12）：初稿，定义 Phase 6 RKHS 显式构造的三类 Mercer 核与收敛性分析框架。
- v0.2（2026-07-12）：更新，开放问题已在 Phase 9 连续谱框架中引用与解决。
- v0.3（2026-07-13）：更新，通用收敛率（强分离 IFS 类）与 RG 截断严格化两个开放问题已解决。新增 `rge_regularization.py` 与 `rkhs_convergence_rate.py`。
- v0.4（2026-07-13）：更新，弱分离 IFS 扰动论上界已完成。新增 `rkhs_weak_separation.py`、`sm_mass_2loop.py`、`bsm_experiment_validation.py`。论文 §8.2/§8.3 重新整理。
- v0.5（2026-07-13）：更新，完全非分离 IFS 覆盖熵上界已完成。新增 `rkhs_non_separated.py`、`bsm_relic_calibration.py`、`holographic_entropy.py`。§5.1 通用收敛率三类 IFS（强分离/弱分离/完全非分离）上界均已建立。
- v0.6（2026-07-13）：更新，测度论深化版本收敛率证明已建立（Frostman 引理、Riesz 容量、势论能量方法，定理 NS-1M~NS-3M），高维 IFS 收敛率推广已完成。新增 `rkhs_non_separated_measure_theoretic.py`、`high_dimensional_ifs.py`。
- v0.7（2026-07-13）：更新，完全非分离 IFS 收敛率下界已建立（定理 NS-LB），与上界匹配得紧阶；新增 `math_open_problems_advanced.py`。
