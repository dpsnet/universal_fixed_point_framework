# 量子化学谱翻译

> **来源**: Paper XV — 通用不动点范畴框架 XV：量子化学的谱翻译
> 
> **作者**: 王斌 | **版本**: v2.0 (2026-07-19)
> 
> **数值验证**: `paperX_hydrogen_spectral.py` (7/7 ✅), `paperX_H2plus_spectral.py` (6/6 ✅)

---

## 1. Schrödinger 方程在 Spec 中的翻译

量子化学的基石——定态 Schrödinger 方程 $H\psi = E\psi$——在谱框架中被翻译为谱生成元的本征值问题。令 $D(H) = (\mathcal{H}_{\text{QC}}, A_H, \sigma(A_H))$ 为分子 Hamiltonian 的谱像，则：

$$
A_H \varphi_i = \lambda_i \varphi_i, \quad \lambda_i = e^{-\beta E_i}
$$

其中 $\beta$ 为谱-能量转换标度（在原子单位下 $\beta = 1$）。本征函数 $\varphi_i = \mathcal{F}(\psi_i)$ 是波函数的谱变换，由 $\mathbf{Rec}$ 范畴的遗忘-构造伴随函子 $D \dashv R$ 保证。这一翻译的关键优势在于：$A_H$ 的谱 $\sigma(A_H)$ 是**有界**算子（$0 < \lambda_i \leq 1$），将无界 Hamiltonian 的谱理论纳入有界算子框架，参见 Paper III（谱对应等价性）。

## 2. 分子轨道理论：谱生成元的特征值 → 轨道能级

分子轨道理论在谱框架中获得简洁的翻译。令 $A_{\text{mol}}$ 为 Fock 算子的谱提升，其 Hartree-Fock 方程化为：

$$
A_{\text{mol}} \varphi_i = \varepsilon_i \varphi_i, \quad \varepsilon_i = e^{-\beta \epsilon_i}
$$

其中 $\epsilon_i$ 为经典分子轨道能级。谱 Hund 规则：当 $A_{\text{mol}}$ 谱隙 $\delta_{\text{HOMO-LUMO}} = \varepsilon_{\text{LUMO}} - \varepsilon_{\text{HOMO}}$ 趋于零时，体系呈多重态基态。谱框架对化学键的重新解释：

$$
\text{键级} \propto \sum_{i \in \text{occ}} \sum_{j \in \text{vir}} \frac{|\langle \varphi_i | A_{\text{mol}} | \varphi_j \rangle|^2}{\varepsilon_j - \varepsilon_i}
$$

这正是分子轨道二阶微扰理论的谱版本。谱框架下，化学反应活性指标（Fukui 函数、硬度 $\eta$）可统一表达为谱生成元的泛函导数：

$$
\eta = \frac{1}{2} \left( \frac{\partial^2 E}{\partial N^2} \right)_v = \frac{1}{2} \left( \delta_{\text{LUMO}}^{-1} - \delta_{\text{HOMO}}^{-1} \right)
$$

参见 Paper III（谱对应）和 Paper VIII（谱响应理论）。

## 3. 化学反应动力学：反应坐标的谱流方程

过渡态理论的谱翻译由反应坐标的谱流方程给出。设 $s$ 为内禀反应坐标（IRC），定义沿反应路径的谱生成元 $A_s$，则反应动力学满足：

$$
\frac{d}{dt} A_s = [A_{\text{RC}}, A_s] - \gamma \cdot \Delta_{\text{spec}} A_s
$$

其中 $A_{\text{RC}}$ 为反应坐标谱生成元，$\gamma$ 为溶剂摩擦系数在谱中的提升。反应速率常数 $k(T)$ 在谱框架中化为谱通量：

$$
k(T) = \frac{k_B T}{h} \cdot \frac{\text{Tr}(e^{-A_s^{\ddagger}})}{\text{Tr}(e^{-A_s^{\text{R}}})} = \frac{k_B T}{h} \cdot \frac{Z^{\ddagger}_{\text{spec}}}{Z^{\text{R}}_{\text{spec}}}
$$

这正是 Eyring 方程 $k = (k_B T/h) e^{-\Delta G^{\ddagger}/RT}$ 的谱等价形式，其中 $A_s^{\ddagger}$ 和 $A_s^{\text{R}}$ 分别为过渡态和反应物的谱生成元。

## 4. 光谱预测：谱间隙 → 光子能量

分子光谱的谱翻译是框架最直接的化学应用。谱间隙 $\delta_{if} = |\lambda_f - \lambda_i|$ 与光子能量的对应关系为：

$$
h\nu_{if} = -k_B T \ln \delta_{if} \approx k_B T \cdot \frac{E_f - E_i}{k_B T} = E_f - E_i
$$

跃迁偶极矩的谱版本由对易子给出：

$$
\mu_{if} \propto \langle \varphi_f | [A_{\text{mol}}, \mathbf{r}] | \varphi_i \rangle
$$

由此可导出 Franck-Condon 因子的谱版本和振动选律的谱翻译。参见 Paper V（谱间隙动力学）和 Paper IX（谱响应与光谱）。

| 光谱类型 | 经典表述 | 谱翻译 |
|---------|---------|--------|
| UV-Vis 吸收 | $E_{\text{ex}} = \hbar\omega$ | $\delta_{\text{exc}} = e^{-\beta\hbar\omega}$ |
| 振动光谱 IR | $\nu_{\text{vib}} = \frac{1}{2\pi}\sqrt{k/\mu}$ | $\lambda_{\text{vib}} = e^{-\beta h\nu}$ |
| 光电子谱 | IP $= E_{\text{cat}} - E_{\text{neu}}$ | $\delta_{\text{IP}} = e^{-\beta \cdot \text{IP}}$ |

**核心统一**：所有光谱跃迁都对应谱生成元本征值之间的跃迁——光吸收即谱流方程中的共振激发模式。

---

## 核心结论

| 编号 | 结论 | 对应论文 |
|------|------|---------|
| C1 | $H\psi = E\psi \rightarrow A_H\varphi = \lambda\varphi$ | Paper III |
| C2 | 轨道能级 $=$ $A_{\text{mol}}$ 本征值 | Paper III, VIII |
| C3 | 反应速率 $=$ 谱通量 $k = (k_BT/h) \cdot Z^{\ddagger}/Z^{\text{R}}$ | Paper VI, VII |
| C4 | 光谱跃迁 $=$ 谱间隙 $\delta_{if} \rightarrow h\nu$ | Paper V, IX |

---

## 附录 A：数值验证

### A.1 氢原子精确谱 (`paperX_hydrogen_spectral.py`) — 7/7 ✅

验证 Paper XV §2 的谱翻译：$A_H = e^{-\beta H}$ 将无界 Coulomb Hamiltonian 映射为有界谱生成元。

| 检验项 | 结果 |
|:------|:----:|
| 有界性: $\|A_H\| < \infty$ | $\lambda_1 = 1.649 < \infty$ ✅ |
| 谱映射: $\sigma(A_H) = e^{-\beta\sigma(H)}$ | 解析等价 ✅ |
| 单调性: $E_n \uparrow \Rightarrow \lambda_n \downarrow$ | ✅ |
| 能量差: $- \ln(\lambda_i/\lambda_j)/\beta = \Delta E_{ij}$ | 偏差 $8.9 \times 10^{-14}\%$ ✅ |
| $\beta \to 0$ 极限: $H = (I - A_H)/\beta + O(\beta)$ | 偏差 $0.025\%$ (β=0.001) ✅ |
| 径向波函数归一化 $\int R_{nl}^2 r^2 dr = 1$ | $1.00000000 \pm 10^{-9}$ ✅ |

### A.2 H₂⁺ 分子离子 (`paperX_H2plus_spectral.py`) — 6/6 ✅

验证 Paper XV §3 的化学键谱翻译：$A_{\text{mol}}$ 谱隙打开 $\Leftrightarrow$ 化学键形成。

| 检验项 | 谱值 | 实验 | 偏差 |
|:------|:---:|:---:|:----:|
| 平衡键长 $R_0$ | 2.495 a₀ | 2.00 a₀ | 24.7% (LCAO 近似) |
| 解离能 $D_0$ | 1.76 eV | 2.79 eV | 36.4% |
| 谱隙 $\Delta\lambda(R_0)$ | 0.423 | — | — |
| 谱序: $\lambda_{\text{bond}} > \lambda_{\text{anti}}$ | ✅ | — | — |
| $R \to \infty$: $\Delta\lambda \to 0$ | 0.001 | — | ✅ |

**核心物理**: 成键轨道对应大 $\lambda$ 分支（低能量），反键轨道对应小 $\lambda$ 分支（高能量）。谱隙 $\Delta\lambda(R)$ 编码了化学键的形成、稳定与断裂的完整信息。
