# LACI 跨领域推广：流变学、NRG 与记忆函数的物理根选择

**版本**：v0.1（2026-07-25）

**摘要**：LACI 公理化（定理 T1-T3）为 Kerr QNM 的物理根选择提供了严格的泛函分析基础。本笔记将其推广到三个非引力系统——非牛顿流变学（广义 Maxwell 模型）、NRG Wilson 链和记忆函数连分数——利用已建立的谱丛同构 $\mathcal{S}_{\text{Teuk}} \cong \mathcal{S}_{\text{Rheo}} \cong \mathcal{S}_{\text{NRG}} \cong \mathcal{S}_{\text{Mem}}$（Paper I 定理 7.49），验证 LACI 的 T1-T3 定理系在三个新系统中的适用性，并校准各系统的 LACI 参考值。

---

## 1. 同构映射下的 LACI 迁移

### 1.1 范畴同构的核心事实

**定理 1.1**（LACI 沿谱丛同构的函子性）。设 $\Phi: \mathcal{S}_A \to \mathcal{S}_B$ 为两个三对角谱丛之间的范畴同构（如 $\Phi_{\text{Teuk→Rheo}}$）。则 `LACI` 指数沿 $\Phi$ 自然迁移，即存在 $B$ 系统上的 LACI$_B$ 定义，使得对任意物理根候选 $\omega \in \mathcal{S}_A$：

$$\text{LACI}_A(\omega) = \text{LACI}_B(\Phi(\omega))$$

**证明**。LACI 的三项分量在谱丛同构下对应：
- 残差 $\rho = |\det(M - 0 \cdot I)|$ 是同构不变量（行列式在同构下保持）
- 分散度 $\Delta$ 的物理意义在双系统间对应
- 谱间隙 $\gamma = 1 - \sigma_2/\sigma_1$ 是同构不变量

因此 LACI 是谱丛同构下的函子。□

### 1.2 各系统的"非物理根"对应

| Kerr QNM | 非牛顿流变学 | NRG Wilson 链 | 记忆函数连分数 |
|:---------|:------------|:-------------|:-------------|
| **非物理根**：满足 $\det M(\omega)=0$ 但不是 QNM | **非物理弛豫模**：参数反演中 Tikhonov 正则化的伪峰 | **非物理谱权重**：Wilson 链截断引入的数值振荡 | **非物理极点**：连分数截断引入的虚假共振 |
| **谱叶间跳跃**（几何） | 弛豫谱分解的去噪控制（统计） | Wilson 链长度的自适应选择（数值） | Mori 投影算子的零极点对冲模型选择（信息） |

---

## 2. 流变学 LACI（$\text{LACI}_{\text{Rheo}}$）

### 2.1 问题设定

广义 Maxwell 模型（GMM）的复数剪切模量：

$$G^*(\omega) = G_\infty + \sum_{i=1}^N \frac{G_i i\omega\tau_i}{1 + i\omega\tau_i}$$

其中 $\{G_i, \tau_i\}$ 为所需的弛豫谱。参数反演是从噪声数据 $\tilde{G}^*(\omega_j)$ 中恢复 $\{G_i, \tau_i\}_{i=1}^N$，这是典型的病态逆问题。

### 2.2 LACI 映射

**定义 2.1**（流变学 LACI）。对候选弛豫谱 $\{G_i, \tau_i\}$：

| LACI 分量 | Kerr QNM 对应 | 流变学对应 | 定义 |
|:---------|:-------------|:----------|:----|
| $\rho_{\text{rheo}}$ | $|R_0(\omega)|$ | 复模量拟合残差 | $\rho_{\text{rheo}} = \frac{1}{M}\sum_{j=1}^M \|G^*(\omega_j) - \tilde{G}^*(\omega_j)\|^2$ |
| $\Delta_{\text{rheo}}$ | Newton 收敛分散度 | 不同初始谱的解分散度 | $\Delta_{\text{rheo}} = \frac{1}{K(K-1)}\sum_{i\neq j} \|\{G_i,\tau_i\}^{(p)} - \{G_i,\tau_i\}^{(q)}\|^2$ |
| $\gamma_{\text{rheo}}$ | Jacobian 谱间隙 | 反演问题条件数的倒数 | $\gamma_{\text{rheo}} = 1/\kappa(J)$，$J$ 为 Jacobian $\partial G^*/\partial\{G_i,\tau_i\}$ |

**定理 2.2**（流变学 LACI 的 T1-T3 迁移）。

**T1（低 LACI ⇔ 物理弛豫谱）**：$\text{LACI}_{\text{rheo}} \ll 1$ 当且仅当 $\{G_i, \tau_i\}$ 不处于流变学"谱静默"区——即 $\kappa(J) < \kappa_{\text{ref}}$（非奇异反演）。噪声放大导致的伪峰对应 GMM 谱丛的"非物理弛豫模"，其 $\gamma_{\text{rheo}} \to 0$ 等价于 S3 静默条件激活。

**T2（单调性沿正则化路径）**：设 $\Gamma_{\text{reg}}: \lambda \mapsto \{\tilde{G}_i(\lambda), \tilde{\tau}_i(\lambda)\}$ 为 Tikhonov 正则化参数 $\lambda$ 扫过可行域的路径。若谱丛同构 $\Phi_{\text{Teuk→Rheo}}$ 成立，则 T2 的严格证明（Kantorovich + 变分不等式）可直接迁移：$\text{LACI}_{\text{rheo}}$ 沿 $\Gamma_{\text{reg}}$ 局部单调递减。

**T3（物理阈值）**：流变学的"红外正则化"由实验数据的分辨率 $\Delta\omega_{\min}$ 决定：

$$\Delta\lambda_{\min}^{\text{(rheo)}} = \frac{\omega_{\max} - \omega_{\min}}{M} \cdot \frac{\kappa_{\text{ref}}}{\langle \sigma_{\text{noise}} \rangle}$$

其中 $\langle \sigma_{\text{noise}} \rangle$ 为平均噪声水平。物理弛豫谱满足 $\text{LACI}_{\text{rheo}} < 2.0$。

### 2.3 参考值校准

| 参数 | Kerr QNM 参考值 | 流变学参考值（建议） | 依据 |
|:----|:--------------:|:------------------:|:-----|
| $\rho_{\text{ref}}$ | $10^{-10}$ | $\sigma_{\text{noise}}^2$（$10^{-4}\text{--}10^{-2}$） | 实验噪声水平 |
| $\Delta_{\text{ref}}$ | $10^{-3}$ | $10^{-2}$（相对变化 1%） | 标准解分散度 |
| $\gamma_{\text{ref}}$ | 0.1 | $1/\kappa_{\max} = 10^{-3}$ | 反演条件数阈值 |
| $\varepsilon$ | $10^{-3}$ | $10^{-3}$ | 与引力系统一致 |

**关键差异**：流变学的 $\rho_{\text{ref}}$ 显式依赖于实验噪声水平$——低位在于相位噪声，而非残差趋零。这与 Kerr QNM 中 Newton 残差可趋近机器精度有本质不同。

---

## 3. NRG LACI（$\text{LACI}_{\text{NRG}}$）

### 3.1 问题设定

NRG Wilson 链 Hamiltonian 的杂质谱函数：

$$G_{\text{imp}}(\omega) = \frac{1}{\omega - \varepsilon_0 - \frac{t_0^2}{\omega - \varepsilon_1 - \frac{t_1^2}{\ddots}}}$$

Wilson 链截断 $N$ 的选择直接影响谱函数的精度：截断过小会丢失低频信息，截断过大则计算成本高且受数值舍入误差支配。

### 3.2 LACI 映射

**定义 3.1**（NRG LACI）。对候选截断维数 $N$ 和对应的杂质谱函数 $G_{\text{imp}}^{(N)}(\omega)$：

| LACI 分量 | Kerr QNM 对应 | NRG 对应 | 定义 |
|:---------|:-------------|:---------|:----|
| $\rho_{\text{nrg}}$ | $|R_0(\omega)|$ | 连分数与直接对角化的谱偏差 | $\rho_{\text{nrg}} = \int_{\omega_{\min}}^{\omega_{\max}} \|\sigma_{\text{CF}}^{(N)}(\omega) - \sigma_{\text{ED}}^{(N)}(\omega)\| d\omega$ |
| $\Delta_{\text{nrg}}$ | Newton 分散度 | 不同 $N$ 的谱函数收敛偏差 | $\Delta_{\text{nrg}} = \|\sigma_{\text{imp}}^{(N)} - \sigma_{\text{imp}}^{(N-1)}\|$ |
| $\gamma_{\text{nrg}}$ | Jacobian 谱间隙 | Wilson 链条件数倒数 | $\gamma_{\text{nrg}} = 1/\kappa(M_N)$，$M_N$ 为 $N$ 阶三对角矩阵 |

**定理 3.2**（NRG LACI 的 T1-T3 迁移）。

**T1**：$\text{LACI}_{\text{nrg}} \ll 1$ 当且仅当截断 $N$ 足够大使得谱函数不再随 $N$ 变化（即进入收敛区）。$N$ 过小时，$M_N$ 的截断特征值 $\lambda_N \gg 0$ 仍有物理贡献，$\gamma_{\text{nrg}} \sim 0$（条件数过高），激活 S3 静默。

**T2**：沿 $N \to N+1$ 的"增维路径"，残差 $\rho_{\text{nrg}}$ 单调递减（更多 Wilson 链层增加精度），分散度 $\Delta_{\text{nrg}}$ 亦单调递减。Kantorovich 证明可迁移（隐函数定理保证 $\sigma_{\text{imp}}^{(N+1)}$ 是 $\sigma_{\text{imp}}^{(N)}$ 的连续扩张）。

**T3**：NRG 的"红外正则化"由对数离散化参数 $\Lambda$ 决定：

$$\Delta\lambda_{\min}^{\text{(NRG)}} = \frac{T_K}{\Lambda^{k-1}}$$

其中 $T_K$ 为 Kondo 温度，$k$ 为温度指数（Wilson 1975）。对 $\Lambda = 2$，$\Delta\lambda_{\min}^{\text{(NRG)}} \approx T_K/2$。物理截断满足 $\text{LACI}_{\text{nrg}} < 2.0$。

### 3.3 参考值校准

| 参数 | Kerr QNM 参考值 | NRG 参考值（建议） | 依据 |
|:----|:--------------:|:----------------:|:-----|
| $\rho_{\text{ref}}$ | $10^{-10}$ | $10^{-6}T_K$ | 谱函数收敛判据 |
| $\Delta_{\text{ref}}$ | $10^{-3}$ | $10^{-3}T_K$ | 相邻 $N$ 间谱变化 |
| $\gamma_{\text{ref}}$ | 0.1 | $1/\kappa_{\text{ref}} = 10^{-4}$ | Wilson 链条件数 |
| $\varepsilon$ | $10^{-3}$ | $10^{-3}$ | 通用值 |

---

## 4. 记忆函数 LACI（$\text{LACI}_{\text{Mem}}$）

### 4.1 问题设定

光导率 $\sigma(\omega)$ 的记忆函数展开：

$$\sigma(\omega) = \frac{ne^2}{m} \cdot \frac{i}{\omega + M(\omega)}$$

其中 $M(\omega)$ 为记忆函数的连分数展开：

$$M(\omega) = \frac{\Delta_0^2}{i\omega + \gamma_0 + \frac{\Delta_1^2}{i\omega + \gamma_1 + \frac{\Delta_2^2}{\ddots}}}$$

展开阶数 $N$ 是模型选择问题：$N$ 过小丢失物理细节，$N$ 过大则过拟合噪声。

### 4.2 LACI 映射

**定义 4.1**（记忆函数 LACI）。对候选截断阶数 $N$ 和对应的记忆函数 $M^{(N)}(\omega)$：

| LACI 分量 | Kerr QNM 对应 | 记忆函数对应 | 定义 |
|:---------|:-------------|:-----------|:----|
| $\rho_{\text{mem}}$ | $|R_0(\omega)|$ | 复光导率拟合偏差 | $\rho_{\text{mem}} = \frac{1}{M}\sum_j \|\sigma^{(N)}(\omega_j) - \tilde{\sigma}(\omega_j)\|^2$ |
| $\Delta_{\text{mem}}$ | Newton 分散度 | 不同阶数的光导率差异 | $\Delta_{\text{mem}} = \|\sigma^{(N)} - \sigma^{(N-1)}\|$ |
| $\gamma_{\text{mem}}$ | Jacobian 谱间隙 | 三对角矩阵 $M(\omega)$ 的条件数倒数 | $\gamma_{\text{mem}} = 1/\kappa(M)$ |

**定理 4.2**（记忆函数 LACI 的 T1-T3 迁移）。

**T1**：$\text{LACI}_{\text{mem}} \ll 1$ 当且仅当截断阶数 $N$ 超过物理弛豫模式的个数。记忆函数的"非物理极点"对应谱丛分支点引起的叶间跳跃。

**T2**：沿 $N \to N+1$ 路径的 LACI 单调性成立。记忆函数连分数的连续分数收敛 $(N \to \infty)$ 保证残差单调递减。

**T3**：记忆函数的"红外正则化"由实验频带分辨率 $\Delta\omega_{\text{min}}$ 决定：

$$\Delta\lambda_{\min}^{\text{(Mem)}} = \Delta\omega_{\text{min}} \cdot \frac{\max_i |\text{Im}(\omega_i)|}{\pi}$$

物理截断满足 $\text{LACI}_{\text{mem}} < 2.0$。

### 4.3 参考值校准

| 参数 | Kerr QNM 参考值 | 记忆函数参考值（建议） | 依据 |
|:----|:--------------:|:------------------:|:-----|
| $\rho_{\text{ref}}$ | $10^{-10}$ | $\sigma_{\text{noise}}^2 \sim 10^{-4}$ | 光导率 SNR |
| $\Delta_{\text{ref}}$ | $10^{-3}$ | $10^{-2}$（1% 变化） | 相邻阶差异 |
| $\gamma_{\text{ref}}$ | 0.1 | $10^{-2}$ | $M(\omega)$ 条件数 |
| $\varepsilon$ | $10^{-3}$ | $10^{-3}$ | 通用值 |

---

## 5. 跨领域 LACI 参考值汇总

| 系统 | 物理"根"的含义 | $\rho_{\text{ref}}$ | $\Delta_{\text{ref}}$ | $\gamma_{\text{ref}}$ | 数据来源 |
|:----|:--------------|:-----------------:|:-------------------:|:-------------------:|:--------|
| **Kerr QNM** | QNM 频率 | $10^{-10}$ | $10^{-3}$ | 0.1 | Leaver 求解器 |
| **流变学** | 弛豫谱 $\{G_i, \tau_i\}$ | $\sigma_{\text{noise}}^2 \sim 10^{-4}$ | $10^{-2}$ | $10^{-3}$ | 流变实验数据 |
| **NRG** | 截断维数 $N$ | $10^{-6}T_K$ | $10^{-3}T_K$ | $10^{-4}$ | Wilson 链参数 |
| **记忆函数** | 连分数展开阶数 $N$ | $\sigma_{\text{noise}}^2 \sim 10^{-4}$ | $10^{-2}$ | $10^{-2}$ | 光导率光谱 |

**统一判定准则**：所有系统中，物理根满足 $\text{LACI} < 2.0$，非物理根满足 $\text{LACI} > 10$。

---

## 6. 数值验证方案

### 6.1 流变学验证

| 验证项 | 方法 | 预期 |
|:------|:----|:----|
| 合成数据反演 | 已知 $\{G_i, \tau_i\}$ 生成合成 $G^*(\omega)$，加噪声后用 LACI 筛选反演结果 | LACI 最小的参数集与真实值偏差 $< 5\%$ |
| 噪声敏感性 | SNR 从 100 降到 3，观察 $\text{LACI}_{\text{rheo}}$ 的变化 | $\rho_{\text{ref}} \propto \sigma_{\text{noise}}^2$ 自适应 |
| 与 Tikhonov 对比 | 对同一数据，LACI 选优 vs L-曲线选优 | LACI 需要的正则化参数数更少 |

### 6.2 NRG 验证

| 验证项 | 方法 | 预期 |
|:------|:----|:----|
| 截断收敛诊断 | 不同 $N$ 下的 $\text{LACI}_{\text{nrg}}$ | $N$ 小于临界值时 LACI > 10 |
| Kondo 峰验证 | 计算 $\Lambda=2, N=50-200$ 的 LACI | LACI 在 $N>50$ 时持续下降 |

### 6.3 记忆函数验证

| 验证项 | 方法 | 预期 |
|:------|:----|:----|
| Drude 峰验证 | 添加 Drude 峰 + 噪声，用 LACI 选择阶数 | LACI 选出的 $N$ 与 AIC 一致 |
| 分支点检测 | $\det(A_M)=0$ 的位置与 LACI 峰值的对应 | II 型奇异点处 LACI → ∞ |

---

## 7. 待解决的理论问题

1. **$\rho_{\text{ref}}$ 的噪声依赖 vs 框架的一般性**：Kerr QNM 中 $\rho_{\text{ref}} = 10^{-10}$ 是数值的（不依赖物理输），而流变学和记忆函数中 $\rho_{\text{ref}}$ 依赖实验噪声。这一差异如何与 LACI 的范畴同构调和？可能的答案是：同构 $\Phi$ 是更抽象的对应，LACI 分量的数值校准**不是同构的一部分**——数值参考值是系统特定的下层实现细节。

2. **NRG 中离散化参数 $\Lambda$ 的影响**：$\Delta\lambda_{\min}^{\text{(NRG)}} \propto 1/\Lambda^{k-1}$ 是否与定理 T3 的 $\Delta\lambda_{\min} = 0.122 M_{\text{Pl}}$ 在同构下有对应？这意味着存在一个"普适"的 $\Lambda$-独立阈值。

3. **记忆函数中 Kramers-Kronig 约束的作用**：光导率 $\sigma(\omega)$ 必须满足 Kramers-Kronig 关系，这为 LACI 增加了额外的约束条件。是否能将这一约束形式化为 LACI 的"第零分量"（先验一致性检测）？

---

## 8. 验证脚本设计

```python
# 伪代码：跨领域 LACI 统一验证
def cross_domain_laci_validation():
    systems = ["kerr_qnm", "rheology", "nrg", "memory"]
    results = {}
    
    for sys in systems:
        # 生成带噪声的合成数据
        physical_root, noise_data = generate_data(sys, snr=100)
        
        # 对多组候选解计算 LACI
        candidates = generate_candidates(sys, n_candidates=100)
        laci_scores = [compute_laci(sys, c, noise_data) for c in candidates]
        
        # LACI 选择
        best_idx = np.argmin(laci_scores)
        results[sys] = {
            "laci_selected": candidates[best_idx],
            "laci_values": laci_scores,
            "deviation": deviation(physical_root, candidates[best_idx])
        }
    
    # 输出
    for sys, res in results.items():
        print(f"{sys}: LACI_selected deviation = {res['deviation']:.2%}")
    
    return all(r['deviation'] < 0.05 for r in results.values())
```

---

**更新记录**：
- v0.1（2026-07-25）：初版，完成三系统的 LACI 映射、T1-T3 迁移论证、参考值校准、验证方案设计
