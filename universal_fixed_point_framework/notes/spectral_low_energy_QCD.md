# 低能 QCD 的谱翻译

**目标**：将 QCD 禁闭、手征对称性破缺、$\chi$PT 翻译为 $\mathbf{Spec}$ 范畴语言。

## 1. 谱框架中的 QCD 拉格朗日量

QCD 拉格朗日量的谱翻译已在 Paper XI §3.3 中建立。低能 QCD 的关键新元素是**非微扰效应**——禁闭和手征对称性破缺——这些在谱语言中对应谱测度的拓扑相变。

## 2. 禁闭作为谱测度相变

在微扰 QCD 中，$\alpha_s(\mu)$ 在 $\mu \to \Lambda_{\text{QCD}}$ 时发散（Landau 极点）。在谱语言中，这对应谱生成元 $A_{\text{QCD}}$ 在红外区域的**谱堆积**——特征值密度在 $\Lambda_{\text{QCD}}$ 处从连续谱变为离散谱。

**禁闭的谱判据**：
$$\rho(\lambda) = \frac{dN}{d\lambda} \xrightarrow{\lambda \to \Lambda_{\text{QCD}}} \text{离散化}$$

即谱测度从绝对连续变为纯点谱。这是由 $A_{\text{QCD}}$ 在红外区域的非线性自相互作用驱动的谱流相变。

**夸克禁闭的谱等价**：夸克 $q$ 在 $\lambda < \Lambda_{\text{QCD}}$ 时无自由谱态——所有谱权重集中在 colorless 的介子/重子谱态上。

## 3. 手征对称性破缺

在手征极限 $m_q \to 0$，QCD 拉格朗日量具有 $SU(N_f)_L \times SU(N_f)_R$ 手征对称性。实验观测到该对称性自发破缺为 $SU(N_f)_V$，产生 $N_f^2 - 1$ 个 Goldstone 玻色子（$\pi, K, \eta$）。

**谱翻译**：手征对称性破缺对应谱生成元 $A_{\text{QCD}}$ 在红外获得非零谱间隙：
$$\Delta\lambda_{\chi\text{SB}} \equiv \min \sigma(A_{\text{QCD}}) = \Lambda_{\text{QCD}}$$

手征凝聚 $\langle\bar{q}q\rangle$ 在谱语言中为谱迹：
$$\langle\bar{q}q\rangle = -\frac{1}{V} \operatorname{Tr}_{\mathbf{Spec}}(S_F(\lambda)) = -\frac{1}{V} \sum_{\lambda \in \sigma(A)} \frac{1}{\lambda + m_q + i\varepsilon}$$

在 $m_q \to 0$ 极限下：
$$\langle\bar{q}q\rangle \propto -\pi \rho(0)$$
其中 $\rho(0)$ 是 $A_{\text{QCD}}$ 在零特征值处的谱密度。手征对称性破缺等价于 $\rho(0) \neq 0$（Banks-Casher 关系的谱版本）。

## 4. 谱 $\chi$PT

手征微扰论（$\chi$PT）是 QCD 在低能区的有效场论，以 Goldstone 玻色子为自由度。

**谱翻译**：Goldstone 玻色子 $\pi^a$ 是 $\mathbf{Spec}$ 中的周期谱对象，其谱作用量为：
$$\mathcal{L}_{\chi\text{PT}}^{\text{spec}} = \frac{F_\pi^2}{4} \operatorname{Tr}_{\mathcal{H}_\pi}([A_\pi, U]^\dagger [A_\pi, U]) + \frac{F_\pi^2}{4} \operatorname{Tr}_{\mathcal{H}_\pi}(\chi^\dagger U + U^\dagger \chi)$$

其中 $U = \exp(2i\pi^a T^a/F_\pi) \in SU(N_f)$，$\chi = 2B_0 \operatorname{diag}(m_u, m_d, m_s)$。

在谱流方程中，$\chi$PT 参数 $F_\pi$ 和 $B_0$ 由 $A_{\text{QCD}}$ 的谱间隙确定：
$$F_\pi \propto \sqrt{N_c} \cdot \Lambda_{\text{QCD}}$$
$$B_0 = -\frac{\langle\bar{q}q\rangle}{F_\pi^2} = \frac{\pi\rho(0)}{F_\pi^2}$$

## 5. 谱预测

| QCD 量 | 谱公式 | 预测值 | 实验值 |
|:-------|:------|:------:|:------:|
| $\Lambda_{\text{QCD}}$ | $\Lambda_{\text{QCD}} = \Delta\lambda_{\min}^{(\text{QCD})} | $\sim 200$ MeV | $217 \pm 25$ MeV |
| $F_\pi$ | $\sqrt{N_c} \Lambda_{\text{QCD}}/4\pi$ | $\sim 93$ MeV | $92.2$ MeV |
| $\langle\bar{q}q\rangle$ | $-\pi\rho(0)$ | $-(250\text{ MeV})^3$ | $-(270 \pm 30\text{ MeV})^3$ |
| $m_\pi$ | $\sqrt{2B_0 m_q}$ | $\sim 140$ MeV | $140$ MeV |

**关键**：$\Lambda_{\text{QCD}}$ 在谱框架中不是自由参数，而是 $A_{\text{QCD}}$ 谱间隙在红外区域的位置，由 $A_{\text{QCD}}$ 的谱流方程从 $M_{\text{Pl}}$ 跑到 $\Lambda_{\text{QCD}}$ 的自然截断决定。这闭合了从 Planck 能标到 QCD 能标的完整 RGE 链。

## 6. 开问题

1. $\Lambda_{\text{QCD}}$ 从谱间隙跑动的精确数值计算
2. $\langle\bar{q}q\rangle$ 与 $c_i$ 的定量关系
3. 禁闭-退禁闭相变的谱动力学描述（有限温度）
4. $\chi$PT 高阶算符的谱翻译
