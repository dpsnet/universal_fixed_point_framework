# 中微子质量的谱 See-saw

标准模型中微子无质量的困境来源于缺少右手中微子。在谱框架中，右手中微子 $\nu_R$ 自然地作为谱对象存在，从而激活标准的 See-saw 机制。

## 右手中微子的谱对象

在 $\mathbf{Sp}$ 范畴中，右手中微子 $\nu_R$ 对应谱对象 $(\mathcal{H}_{\nu_R}, A_{\nu_R}, \sigma(A_{\nu_R}))$，其中 $\mathcal{H}_{\nu_R}$ 是右手中微子的 Hilbert 空间，$A_{\nu_R}$ 是 Majorana 质量谱算符，$\sigma(A_{\nu_R})$ 是其特征值谱。谱 Majorana 质量项为：

$$\mathcal{L}_{\text{Majorana}} = \frac12 \nu_R^\dagger [A_{\nu_R}, \nu_R] = \frac12 M_R \nu_R^T C \nu_R + \text{h.c.},$$

其中 $M_R$ 是 $A_{\nu_R}$ 的最小非零特征值（谱间隙），$C$ 是荷共轭矩阵。

## 谱 See-saw 拉格朗日量

完整的谱 See-saw 拉格朗日量为：

$$\boxed{\mathcal{L}_\nu^{\text{spec}} = \frac12 \nu_R^\dagger [A_{\nu_R}, \nu_R] + y_\nu \bar{L}_L \cdot H \cdot \nu_R + \text{h.c.}},$$

其中 $L_L = (\nu_L, e_L)^T$ 是左手轻子二重态，$H$ 是 Higgs 二重态，$y_\nu$ 是中微子 Yukawa 耦合。

## 电弱对称性破缺后的质量矩阵

在 Higgs 获得真空期望值 $\langle H \rangle = (0, v/\sqrt{2})^T$ 后，Dirac 质量项为 $m_D = y_\nu v/\sqrt{2}$。完整的 $6\times6$ 中微子质量矩阵在 $(\nu_L, \nu_R^c)$ 基下为：

$$\mathcal{M}_\nu = \begin{pmatrix}
0 & m_D \\
m_D^T & M_R
\end{pmatrix}.$$

See-saw 关系（$M_R \gg m_D$）给出 light 中微子的有效质量矩阵：

$$\boxed{M_\nu = -m_D M_R^{-1} m_D^T}.$$

## 谱预测

在谱框架中，Majorana 质量谱算符 $A_{\nu_R}$ 的谱间隙由 $\mathbf{Sp}$ 范畴中电弱能标与 Planck 能标之间的层级决定：

$$M_R \sim \frac{\Lambda_{\text{Planck}}}{\Lambda_{\text{EW}}} \cdot v \sim 10^{14}\ \text{GeV},$$

其中 $\Lambda_{\text{Planck}} = 1.22 \times 10^{19}\ \text{GeV}$ 是 Planck 能标，$\Lambda_{\text{EW}} \sim 10^2\ \text{GeV}$ 是电弱能标。代入 $m_D \sim y_\nu v$ 并取 $y_\nu \sim \mathcal{O}(1)$，得到 light 中微子质量：

$$m_{\nu_i} \sim \frac{m_D^2}{M_R} \sim 0.01\text{–}0.1\ \text{eV},$$

与太阳中微子 ($\Delta m_{21}^2 \approx 7.4 \times 10^{-5}\ \text{eV}^2$) 和大气中微子 ($\Delta m_{31}^2 \approx 2.5 \times 10^{-3}\ \text{eV}^2$) 的振荡实验数据一致。

## PMNS 混合矩阵

在带三代结构的一般情形下，中微子混合由 Pontecorvo-Maki-Nakagawa-Sakata (PMNS) 矩阵描述：

$$\boxed{U_{\text{PMNS}} = U_\ell^\dagger U_\nu},$$

其中 $U_\ell$ 对角化带电轻子质量矩阵（通过 $Y_e^\dagger Y_e$ 的谱分解），$U_\nu$ 对角化有效中微子质量矩阵 $M_\nu$。与 CKM 矩阵类似，$U_{\text{PMNS}}$ 在谱框架中是 Yukawa 谱算子和 Majorana 谱算子的特征基重叠量。不同之处在于，中微子为 Majorana 费米子，因此 $U_{\text{PMNS}}$ 包含额外的 Majorana 相位 $\alpha_1, \alpha_2$：

$$U_{\text{PMNS}} = V_{\text{PMNS}} \cdot \operatorname{diag}(1, e^{i\alpha_1}, e^{i\alpha_2}),$$

其中 $V_{\text{PMNS}}$ 是标准的三混合矩阵（$\theta_{12}, \theta_{23}, \theta_{13}, \delta_{\text{CP}}$），Majorana 相位 $\alpha_1, \alpha_2$ 由 $A_{\nu_R}$ 的谱相位结构决定。

## 要点

右手中微子在谱框架中不是附加假设，而是 $\mathbf{Sp}$ 范畴的天然谱对象。See-saw 机制的谱版本不仅复现了标准 See-saw 的所有结果，还通过 $A_{\nu_R}$ 的谱间隙为 $M_R$ 的能标提供了理论依据。

---

*摘自 Paper XI §8.6*
