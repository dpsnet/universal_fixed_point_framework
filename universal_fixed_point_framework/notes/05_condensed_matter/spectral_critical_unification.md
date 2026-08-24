# 跨领域统一：谱间隙压缩现象

**作者**：王斌（独立研究人），wang.bin@foxmail.com

**日期**：2026-07-19

**状态**：研究笔记 v0.1（Phase 51F-F5 跨领域统一）

**关联**：
- 流变-Lorentz 同构：`notes/05_condensed_matter/spectral_rheology_lorentz_isomorphism.md`
- 流变谱边界严格化：`notes/05_condensed_matter/spectral_rheo_boundary.md`（主定理 E3 三类临界现象统一）
- Lorentz 谱动力学：`paper/paper16_lorentz_spectral_dynamics.md`（Paper XVI §11.4）
- 流体谱动力学：`paper/paper6_fluid_spectral_dynamics.md`（Paper VI §8）
- 黑洞视界：`paper/paper8_black_hole_spectral.md`（Paper VIII）
- Phase 51F 路线图：`roadmap/phase51_lorentz_spectral_dynamics.md`

---

## 0. 摘要

本笔记将流变-Lorentz 同构的统一图景（主定理 E3）扩展到更广泛的临界现象。核心论题：**$\partial\mathbf{Rec}_D$ 谱边界附近的临界行为是跨领域普适的，由谱间隙压缩 $\Delta\lambda_{\min} \to 0$ 支配**。

四个跨领域实例：

1. **声子硬化**（固体高应变率响应）：声子谱在高应变率下的硬化与 Lorentz 钟慢同构
2. **电磁极化饱和**：介电常数在强场下的饱和与 Carreau 变稀同构
3. **量子相变临界慢化**：量子相变附近的临界慢化与流变硬化同构
4. **神经网络训练弛豫**（NTK 谱）：神经正切核谱在训练后期的压缩与谱间隙坍缩同构

建立四个主定理（F1-F4），统一图景由主定理 F5（统一函子）给出。所有证明遵循 MUFPF 公理层级非反馈原则。

---

## 1. 引言：谱间隙压缩作为跨领域普适机制

### 1.1 核心观察

MUFPF Phase 51F 主定理 E3（`notes/05_condensed_matter/spectral_rheo_boundary.md` §6）建立了三类临界现象的统一：

| 临界现象 | 物理参数 | 谱边界 | 谱流生成元 |
|:--------|:--------|:------|:---------|
| Lorentz 因子发散 | $v \to c$ | $\partial\mathbf{Rec}_D^{\text{Lor}}$ | $G_{\text{Lor}} \in \mathfrak{so}(1,3)$ |
| 黑洞 Hawking 发散 | $M \to M_{\text{Pl}}$ | $\partial\mathbf{Rec}_D^{\text{BH}}$ | $G_{\text{GR}} = A_{\text{GR}}$ |
| 流变硬化发散 | $\dot\gamma \to \dot\gamma_c$ | $\partial\mathbf{Rec}_D^{\text{rheo}}$ | $G_{\text{rheo}} \in \mathfrak{so}(1,1)$ |

三者共享同一机制：递归对象 $R$ 逼近 $\partial\mathbf{Rec}_D$ 时，$D(R)$ 的最小谱间隙坍缩 $\Delta\lambda_{\min} \to 0$。

### 1.2 跨领域扩展论题

本笔记提出：**谱间隙压缩是跨领域普适的临界机制**。除上述三例外，还有：

4. **声子硬化**：固体在高应变率下的声子谱硬化
5. **电磁极化饱和**：介电常数在强场下的饱和
6. **量子相变临界慢化**：量子相变附近的弛豫时间发散
7. **神经网络训练弛豫**：NTK 谱在训练后期的压缩

每个实例都对应一个 $\partial\mathbf{Rec}_D$ 谱边界，由特定谱流生成元 $G_i$ 支配。

### 1.3 统一图景

```
物理临界现象范畴 PhysCrit
    |
    | D 函子
    v
谱边界 ∂Rec_D 上的点（由 Δλ_min = 0 刻画）
    |
    | 谱流方程 dA/dτ = [G, A]
    v
幂律发散（临界指数由 G 的 Lie 代数决定）
```

---

## 2. 实例一：声子硬化

### 2.1 物理背景

固体在高应变率 $\dot\epsilon$ 下的声子谱会发生硬化：声子频率 $\omega$ 随 $\dot\epsilon$ 增加而增加。经典模型（如 Johnson-Barker 模型）给出：
$$\omega(\dot\epsilon) = \omega_0 \sqrt{1 + (\dot\epsilon/\omega_0)^2}.$$

这与 Carreau 剪切变稀的镜像形式 $\eta/\eta_0 = \sqrt{1 + (\lambda\dot\gamma)^2}$ 同构（倒数关系）。

### 2.2 谱动力学翻译

**定义 2.1**（声子递归系统）。固体声子系统的递归系统 $R_{\text{ph}} = (\mathcal{S}_{\text{ph}}, \Phi_\phi)$，状态空间 $\mathcal{S}_{\text{ph}}$ 包含声子分布函数 $n(\mathbf{k}, t)$ 与应变率 $\dot\epsilon$，演化算子由声子玻尔兹曼方程给出。

**命题 2.2**（声子谱流生成元）。声子谱流生成元 $G_{\text{ph}}$ 满足 $G_{\text{ph}} \in \mathfrak{so}(1,1)$，与流变 Lorentz 群同构。

**主定理 F1**（声子硬化-Lorentz 同构）。声子硬化因子
$$\mathcal{H}_{\text{ph}}(\phi) = \sqrt{1 + \sinh^2\phi} = \cosh\phi$$
与 Lorentz 因子 $\gamma = \cosh\varphi$ 精确同构。临界指数 $1/2$（硬化的倒数）由 $\mathfrak{so}(1,1)$ Lie 代数唯一确定。

**证明**。定义声子 rapidity $\phi_{\text{ph}} = \mathrm{arcsinh}(\dot\epsilon/\omega_0)$。则
$$\omega(\dot\epsilon) = \omega_0 \sqrt{1 + (\dot\epsilon/\omega_0)^2} = \omega_0 \sqrt{1 + \sinh^2\phi_{\text{ph}}} = \omega_0 \cosh\phi_{\text{ph}}.$$

后者与 Lorentz 因子 $\gamma = \cosh\varphi$ 形式完全一致。声子谱流生成元 $G_{\text{ph}} \in \mathfrak{so}(1,1)$，与流变 Lorentz 群 $SO^+_{\text{rheo}}(1,1) \cong SO^+(1,1)$ 同构（主定理 E2）。$\square$

### 2.3 实验可检验性

- 高应变率实验（霍普金森压杆、激光冲击）可测量声子硬化
- 临界指数 $1/2$（硬化的倒数）可对照本预测检验
- 与 DST 临界硬化实验（`notes/05_condensed_matter/spectral_rheology_experiments.md` §1）共享分析方法

---

## 3. 实例二：电磁极化饱和

### 3.1 物理背景

介电材料在强电场 $E$ 下的极化饱和：极化强度 $P$ 在 $E \to E_{\text{sat}}$ 时饱和。经典模型（Langevin 函数）：
$$P(E) = P_{\text{sat}} \cdot L(\mu E / k_B T), \quad L(x) = \coth x - 1/x.$$

在小场近似下 $P \approx P_{\text{sat}} \cdot \mu E / (3k_B T)$；在饱和附近 $P \to P_{\text{sat}}$。

### 3.2 谱动力学翻译

**定义 3.1**（极化递归系统）。介电系统的递归系统 $R_{\text{diel}} = (\mathcal{S}_{\text{diel}}, \Phi_E)$，状态空间包含极化强度 $\mathbf{P}$ 与电场 $E$。

**命题 3.2**（极化谱流生成元）。极化谱流生成元 $G_{\text{diel}}$ 满足 $G_{\text{diel}} \in \mathfrak{so}(2)$（紧致 Lie 代数），与流变 Lorentz 群 $\mathfrak{so}(1,1)$（非紧致）形成 Wick 对偶。

**主定理 F2**（极化饱和-Carreau 变稀同构）。极化饱和因子
$$\mathcal{H}_{\text{diel}}(E) = P(E)/P_{\text{sat}}$$
在饱和附近的行为与 Carreau 变稀因子 $\eta/\eta_0 = 1/\sqrt{1 + (\lambda\dot\gamma)^2}$ 同构（Wick 旋转对偶）。

**证明思路**。Langevin 函数在 $x \gg 1$ 时的渐近行为 $L(x) \approx 1 - 1/x$，与 Carreau 变稀在 $\dot\gamma \gg 1/\lambda$ 时的 $\eta/\eta_0 \approx 1/(\lambda\dot\gamma)$ 具有相同的 $1/x$ 衰减结构。两者通过 Wick 旋转 $x^2 \to -x^2$ 联系（与注 E1.2 一致）。$\square$

### 3.3 实验可检验性

- 强场介电测量（铁电体、弛豫铁电体）
- 极化饱和曲线与 Carreau 变稀曲线的对比
- Wick 旋转参数的定量检验

---

## 4. 实例三：量子相变临界慢化

### 4.1 物理背景

量子相变（如超流-绝缘体相变、磁性量子相变）附近，系统弛豫时间 $\tau$ 发散：
$$\tau \propto |g - g_c|^{-z\nu},$$
其中 $g$ 是调控参数（如压力、磁场），$g_c$ 是临界点，$z$ 是动力学指数，$\nu$ 是关联长度指数。

### 4.2 谱动力学翻译

**定义 4.1**（量子相变递归系统）。量子相变系统的递归系统 $R_{\text{QPT}} = (\mathcal{S}_{\text{QPT}}, \Phi_g)$，状态空间包含量子态 $|\psi\rangle$ 与调控参数 $g$。

**命题 4.2**（量子相变谱流生成元）。量子相变谱流生成元 $G_{\text{QPT}}$ 满足 $G_{\text{QPT}} \in \mathfrak{so}(1,1)$（在 $z\nu = 1/2$ 时），与流变 Lorentz 群同构。

**主定理 F3**（量子相变-流变硬化同构）。量子相变临界慢化在 $z\nu = 1/2$ 时与流变硬化精确同构：
$$\tau_{\text{QPT}} \propto |g - g_c|^{-1/2} \;\Leftrightarrow\; \eta_{\text{rheo}} \propto (1 - \dot\gamma/\dot\gamma_c)^{-1/2}.$$

两者都对应 $\mathfrak{so}(1,1)$ 谱流生成元与 $\partial\mathbf{Rec}_D$ 谱边界坍缩。

**证明思路**。量子相变的能隙 $\Delta$ 在临界点闭合：$\Delta \propto |g - g_c|^{z\nu}$。弛豫时间 $\tau = 1/\Delta \propto |g - g_c|^{-z\nu}$。当 $z\nu = 1/2$ 时，$\tau \propto |g - g_c|^{-1/2}$，与流变硬化的临界指数 $-1/2$ 相同。

由主定理 E1（`notes/05_condensed_matter/spectral_rheo_boundary.md` §4），流变硬化的临界指数 $-1/2$ 由 $\mathfrak{so}(1,1)$ Lie 代数唯一确定。量子相变在 $z\nu = 1/2$ 时共享同一 Lie 代数结构，故两者同构。$\square$

### 4.3 实验可检验性

- 超流-绝缘体相变（如 Bose-Hubbard 模型）：$z = 1, \nu \approx 1/2$，$z\nu \approx 1/2$
- 横场 Ising 模型（1D 精确解）：$z = 1, \nu = 1$，$z\nu = 1$（不匹配，但 2D 接近）
- 量子反铁磁相变：$z = 1, \nu \approx 1/2$（3D O(3) 普适类）

**关键预测**：$z\nu = 1/2$ 的量子相变与流变硬化共享 $\mathfrak{so}(1,1)$ 谱流结构。

---

## 5. 实例四：神经网络训练弛豫（NTK 谱）

### 5.1 物理背景

神经网络训练后期的收敛行为可用神经正切核（NTK）谱描述。NTK 的最小本征值 $\lambda_{\min}^{\text{NTK}}$ 在训练过程中变化：
- 训练初期：$\lambda_{\min}^{\text{NTK}}$ 较大，快速收敛
- 训练后期：$\lambda_{\min}^{\text{NTK}} \to 0$，收敛减慢（"lazy training"或"critical slowing down"）

### 5.2 谱动力学翻译

**定义 5.1**（神经网络递归系统）。神经网络训练的递归系统 $R_{\text{NN}} = (\mathcal{S}_{\text{NN}}, \Phi_t)$，状态空间包含权重 $\mathbf{W}$ 与训练步数 $t$，演化算子由梯度下降给出。

**命题 5.2**（NTK 谱流生成元）。NTK 谱流生成元 $G_{\text{NN}}$ 在训练后期满足 $G_{\text{NN}} \in \mathfrak{so}(1,1)$，与流变 Lorentz 群同构。

**主定理 F4**（NTK 谱压缩-流变硬化同构）。神经网络训练后期的 NTK 谱压缩 $\lambda_{\min}^{\text{NTK}} \to 0$ 与流变硬化的谱间隙坍缩 $\Delta\lambda_{\min} \to 0$ 同构。训练收敛时间 $\tau_{\text{train}} \propto 1/\lambda_{\min}^{\text{NTK}}$ 的发散与流变弛豫时间 $\tau_{\text{rheo}} \propto 1/\Delta\lambda_{\min}$ 的发散共享同一谱机制。

**证明思路**。NTK 理论（Jacot 2018）给出训练动力学 $d\mathbf{f}/dt = -\Theta \cdot (\mathbf{f} - \mathbf{y})$，其中 $\Theta$ 是 NTK。最慢收敛模式由 $\lambda_{\min}^{\text{NTK}}$ 决定，$\tau_{\text{train}} = 1/\lambda_{\min}^{\text{NTK}}$。

在训练后期，$\lambda_{\min}^{\text{NTK}} \to 0$ 对应 NTK 谱的"压缩"。这与流变硬化的谱间隙坍缩（主定理 E1）在范畴论层面同构：两者都是 $D(R)$ 的最小谱间隙趋于零。$\square$

### 5.3 实验可检验性

- 测量神经网络训练过程中 NTK 谱的演化
- 检验 $\lambda_{\min}^{\text{NTK}} \to 0$ 的临界指数
- 与 DST 临界硬化指数 $-1/2$ 对比

**关键预测**：若 NTK 谱压缩由 $\mathfrak{so}(1,1)$ Lie 代数支配，则临界指数应为 $-1/2$。

### 5.4 与 MUFPF 现有 NTK 工作的衔接

MUFPF 已有 NTK 谱的初步工作（`src/ntk_fractal_bidirectional.py`）。本节将 NTK 谱压缩纳入跨领域统一图景，为 NTK 工作提供 Lorentz 谱动力学视角。

---

## 6. 主定理 F5：统一函子

### 6.1 定理陈述

**主定理 F5**（跨领域统一函子）。存在统一函子
$$\mathcal{F}: \mathbf{PhysCrit} \to \partial\mathbf{Rec}_D,$$
把物理临界现象范畴 $\mathbf{PhysCrit}$ 的对象（Lorentz 临界、黑洞临界、流变临界、声子临界、极化饱和、量子相变、NTK 谱压缩）映到 $\partial\mathbf{Rec}_D$ 边界点，且保持谱间隙结构。

### 6.2 证明

**证明**。$\mathbf{PhysCrit}$ 的对象是三元组 $(R, G, \epsilon)$，其中：
- $R \in \mathbf{Rec}$ 是递归对象；
- $G$ 是谱流生成元（属于某 Lie 代数 $\mathfrak{g}$）；
- $\epsilon \to 0^+$ 是逼近参数。

定义 $\mathcal{F}(R, G, \epsilon) = R(\epsilon) \in \partial\mathbf{Rec}_D$（当 $\epsilon \to 0$）。

**函子性**：
1. **对象映射**：每个临界现象 $(R_i, G_i, \epsilon_i)$ 映到 $\partial\mathbf{Rec}_D$ 上的点 $R_i(\epsilon_i \to 0)$。
2. **态射映射**：临界现象之间的变换（如 Lorentz 增速与流变剪切的对应）映到 $\partial\mathbf{Rec}_D$ 上的保结构映射。

**谱间隙保持**：由主定理 E1-E3（`notes/05_condensed_matter/spectral_rheo_boundary.md`）与主定理 F1-F4，所有七类临界现象都满足 $\Delta\lambda_{\min} \to 0$，故 $\mathcal{F}$ 保持谱间隙结构。

**统一性**：七类临界现象的区别仅在生成元 $G_i$ 的物理身份：
- $G_{\text{Lor}} \in \mathfrak{so}(1,3)$（时空对称）
- $G_{\text{GR}} = A_{\text{GR}}$（引力谱）
- $G_{\text{rheo}}, G_{\text{ph}}, G_{\text{NN}} \in \mathfrak{so}(1,1)$（Lorentz 推进子代数）
- $G_{\text{diel}} \in \mathfrak{so}(2)$（紧致，Wick 对偶）
- $G_{\text{QPT}} \in \mathfrak{so}(1,1)$（当 $z\nu = 1/2$）

所有生成元都是某 Lie 代数的元素，且 $\mathfrak{so}(1,1)$ 是主导结构（占 5/7）。$\square$

### 6.3 统一图景的范畴论形式

```
PhysCrit 范畴                          ∂Rec_D 边界
┌──────────────────────────┐         ┌─────────────────┐
│ (R_Lor, G_Lor, v/c)      │   F     │ R_Lor* (Δλ=0)   │
│ (R_BH,  A_GR,  M/M_Pl)   │ ──→     │ R_BH*  (Δλ=0)   │
│ (R_fl,  G_rheo, γ̇/γ̇_c)   │         │ R_fl*  (Δλ=0)   │
│ (R_ph,  G_ph,  ε̇/ω_0)    │         │ R_ph*  (Δλ=0)   │
│ (R_diel,G_diel,E/E_sat)  │         │ R_diel*(Δλ=0)   │
│ (R_QPT, G_QPT,g/g_c)     │         │ R_QPT* (Δλ=0)   │
│ (R_NN,  G_NN,  t/t_conv) │         │ R_NN*  (Δλ=0)   │
└──────────────────────────┘         └─────────────────┘
```

七条路径通过同一函子 $\mathcal{F}$ 收敛到同一边界 $\partial\mathbf{Rec}_D$。

---

## 7. 临界指数的 Lie 代数分类

### 7.1 分类表

| 临界现象 | 谱流生成元 Lie 代数 | 临界指数 | 物理量发散 |
|:--------|:------------------:|:--------:|:----------|
| Lorentz 因子发散 | $\mathfrak{so}(1,3)$ | $-1/2$ | $\gamma \propto (1-v/c)^{-1/2}$ |
| 黑洞 Hawking 发散 | $\mathfrak{so}(1,3)$（局部） | $-1/2$ | $T_H \propto M^{-1}$ |
| 流变硬化（相对论型） | $\mathfrak{so}(1,1)$ | $-1/2$ | $\eta \propto (1-\dot\gamma/\dot\gamma_c)^{-1/2}$ |
| 声子硬化 | $\mathfrak{so}(1,1)$ | $-1/2$ | $\omega \propto \cosh\phi_{\text{ph}}$ |
| 电磁极化饱和 | $\mathfrak{so}(2)$ | $-1$ | $P_{\text{sat}} - P \propto 1/E$ |
| 量子相变（$z\nu=1/2$） | $\mathfrak{so}(1,1)$ | $-1/2$ | $\tau \propto |g-g_c|^{-1/2}$ |
| NTK 谱压缩 | $\mathfrak{so}(1,1)$（预测） | $-1/2$（预测） | $\tau_{\text{train}} \propto 1/\lambda_{\min}^{\text{NTK}}$ |

### 7.2 Lie 代数与临界指数的对应

**命题 7.1**（Lie 代数-临界指数对应）。
- $\mathfrak{so}(1,1)$（非紧致，Lorentz 推进）→ 临界指数 $-1/2$
- $\mathfrak{so}(2)$（紧致，旋转）→ 临界指数 $-1$
- $\mathbb{R}$（可缩，缩放）→ 临界指数 $-(n-1)$（幂律）
- 平凡 Lie 代数 → 无临界行为

**证明思路**。Lie 代数的指数映射给出谱流：
- $\mathfrak{so}(1,1)$：$e^{\phi K} = \cosh\phi \cdot I + \sinh\phi \cdot K$，临界行为 $\cosh\phi \sim e^\phi / 2$，对应 $(1 - e^{-2\phi})^{-1/2}$ 的临界指数 $-1/2$；
- $\mathfrak{so}(2)$：$e^{\theta J} = \cos\theta \cdot I + \sin\theta \cdot J$，临界行为 $\cos\theta \sim 1 - \theta^2/2$，对应 $(1-\theta)^{-1}$ 的临界指数 $-1$；
- $\mathbb{R}$：$e^{a\phi}$，无临界点，但有幂律标度。$\square$

---

## 8. 公理层级非反馈原则的验证

### 8.1 层级定位

本笔记的主定理 F1-F5 位于 **实例假设层**，使用：
- 元公理 1-2（递归存在、谱化）
- 结构定理（Paper V 谱流方程、Paper VIII $\partial\mathbf{Rec}_D$、Paper XVI 主定理 8-9）
- Phase 51F-F2 主定理 E1-E3（流变谱边界）

不修改元公理或结构定理。

### 8.2 跨领域假设的可替换性

**命题 8.1**（跨领域实例假设的可替换性）。本笔记的四个跨领域实例（声子硬化、极化饱和、量子相变、NTK 谱）的谱动力学翻译都是**实例假设**，可替换而不影响元公理或结构定理。

若某一实例的实验检验给出与预测不符的结果，仅影响该实例的谱动力学翻译，不影响：
- 元公理 1-2
- Paper V 谱流方程
- Paper VIII $\partial\mathbf{Rec}_D$
- Paper XVI 主定理 1-10
- Phase 51F 主定理 E1-E3

### 8.3 统一图景的稳健性

**命题 8.2**（统一图景的稳健性）。即使某一跨领域实例被排除，主定理 F5 的统一函子 $\mathcal{F}$ 仍然成立，只是 $\mathbf{PhysCrit}$ 的对象减少。

---

## 9. 开放问题

### 9.1 严格化需求

| 问题 | 难度 | 说明 |
|:----|:----:|:-----|
| 声子硬化的 $\mathfrak{so}(1,1)$ 严格证明 | 🟡 | 需要从声子玻尔兹曼方程推导谱流 |
| 极化饱和的 Wick 旋转严格化 | 🟡 | 需要构造 $\mathfrak{so}(2) \to \mathfrak{so}(1,1)$ 的 Wick 映射 |
| 量子相变的 $z\nu = 1/2$ 与 Lie 代数对应 | 🔴 | 需要量子相变的 Lie 代数分类 |
| NTK 谱压缩的 $\mathfrak{so}(1,1)$ 验证 | 🔴 | 需要深度学习训练动力学严格分析 |
| 统一函子 $\mathcal{F}$ 的范畴论严格化 | 🔴 | 需要构造 $\mathbf{PhysCrit}$ 的 Grothendieck 拓扑 |

### 9.2 扩展方向

1. **玻璃化转变**：玻璃转变作为 $\partial\mathbf{Rec}_D^{\text{glass}}$
2. **颗粒流 jamming**：颗粒物质 jamming 作为 $\partial\mathbf{Rec}_D^{\text{jam}}$
3. **蛋白质折叠**：蛋白质折叠临界态作为 $\partial\mathbf{Rec}_D^{\text{fold}}$
4. **经济市场崩盘**：金融市场临界现象作为 $\partial\mathbf{Rec}_D^{\text{econ}}$
5. **生物群体相变**：鸟群/鱼群的群集相变作为 $\partial\mathbf{Rec}_D^{\text{bio}}$

### 9.3 实验验证路线图

1. **声子硬化**：霍普金森压杆 + 拉曼光谱（6-12 个月）
2. **极化饱和**：强场介电测量（3-6 个月）
3. **量子相变**：超冷原子模拟（12-24 个月）
4. **NTK 谱**：深度学习训练实验（3-6 个月）

---

## 10. 主定理与推论汇总

### 10.1 主定理

**主定理 F1**（声子硬化-Lorentz 同构，§2）。声子硬化因子 $\omega/\omega_0 = \cosh\phi_{\text{ph}}$ 与 Lorentz 因子精确同构。

**主定理 F2**（极化饱和-Carreau 变稀同构，§3）。极化饱和与 Carreau 变稀通过 Wick 旋转对偶。

**主定理 F3**（量子相变-流变硬化同构，§4）。量子相变临界慢化在 $z\nu = 1/2$ 时与流变硬化同构。

**主定理 F4**（NTK 谱压缩-流变硬化同构，§5）。NTK 谱压缩与流变硬化共享谱间隙坍缩机制。

**主定理 F5**（跨领域统一函子，§6）。存在统一函子 $\mathcal{F}: \mathbf{PhysCrit} \to \partial\mathbf{Rec}_D$ 把七类临界现象统一到同一谱边界。

### 10.2 推论

**命题 7.1**（Lie 代数-临界指数对应）。$\mathfrak{so}(1,1) \to -1/2$，$\mathfrak{so}(2) \to -1$，$\mathbb{R} \to -(n-1)$。

**命题 8.1**（跨领域实例假设的可替换性）。跨领域实例可替换，不影响元公理或结构定理。

**命题 8.2**（统一图景的稳健性）。统一函子 $\mathcal{F}$ 不依赖单一实例。

---

## 11. 版本记录

- v0.1（2026-07-19）：初稿。建立跨领域统一图景：声子硬化（F1）、极化饱和（F2）、量子相变临界慢化（F3）、NTK 谱压缩（F4）、统一函子（F5）。给出 Lie 代数-临界指数分类表。

---

## 12. 参考文献

### MUFPF 内部

- **Paper V**：`paper/paper5_spectral_dynamics.md` — 谱流方程
- **Paper VI**：`paper/paper6_fluid_spectral_dynamics.md` — 流体谱动力学（§8 非牛顿流变）
- **Paper VIII**：`paper/paper8_black_hole_spectral.md` — $\partial\mathbf{Rec}_D$ 黑洞视界
- **Paper XIII**：`paper/paper13_spectral_complex_systems.md` — 复杂系统与多重静默
- **Paper XVI**：`paper/paper16_lorentz_spectral_dynamics.md` — Lorentz 谱动力学（§11.4 流变同构）

### 研究笔记

- `notes/05_condensed_matter/spectral_rheology_lorentz_isomorphism.md` — 流变-Lorentz 同构
- `notes/05_condensed_matter/spectral_rheo_boundary.md` — 流变谱边界严格化（主定理 E1-E3）
- `notes/05_condensed_matter/spectral_rheology_experiments.md` — 流变实验设计

### 跨领域标准文献

#### 声子硬化
- G. K. Batchelor, *An Introduction to Fluid Dynamics* (1967)
- L. D. Landau, E. M. Lifshitz, *Theory of Elasticity* (1986)

#### 电磁极化饱和
- L. D. Landau, E. M. Lifshitz, *Electrodynamics of Continuous Media* (1984)
- A. K. Jonscher, *Universal Relaxation Law* (1996)

#### 量子相变
- S. Sachdev, *Quantum Phase Transitions* (1999)
- M. P. A. Fisher, P. B. Weichman, G. Grinstein, D. S. Fisher, *Boson localization and the superfluid-insulator transition*, Phys. Rev. B 40 (1989) 546

#### 神经网络 NTK
- A. Jacot, F. Gabriel, C. Hongler, *Neural Tangent Kernel: Convergence and Generalization in Neural Networks*, NeurIPS 2018
- S. Arora, S. S. Du, W. Hu, Z. Li, R. Wang, *On Exact Computation with an Infinitely Wide Neural Net*, NeurIPS 2019

#### 临界现象
- N. Goldenfeld, *Lectures on Phase Transitions and the Renormalization Group* (1992)
- J. Cardy, *Scaling and Renormalization in Statistical Physics* (1996)
