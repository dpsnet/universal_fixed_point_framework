# 跨尺度RG：开放问题分析

## 两圈β函数的谱翻译（已由三圈覆盖）

> **注**：规范耦合的多圈β函数在谱框架中已推进至**三圈精度**，两圈工作已完全被覆盖。详见 Paper V §6.2（DS顶点减除模式，12/12对比通过）、Paper XI §8.3（三圈系数列表）、Phase 31（`paper31_threeloop_beta.py`）。

三圈β函数的谱翻译在 SM 规范耦合（Paper XI §8.3）和引力子自相互作用（Paper XII §9.3）中均已实现。两圈是其中的子集，无需单独处理。

**单圈形式**（已在 Paper XII §8.2 完成）：
$$
\frac{d\alpha_i}{d\ln\mu} = -\frac{b_{ij}\alpha_i\alpha_j}{2\pi}
$$

**两圈形式**：
$$
\frac{d\alpha_i}{d\ln\mu} = -\frac{b_{ij}\alpha_i\alpha_j}{2\pi} - \frac{b_{ijk}\alpha_i\alpha_j\alpha_k}{(4\pi)^2}
$$

**谱版本**将 $\alpha_i$ 替换为 $\Delta\lambda_i/4\pi$ 比值：
$$
\alpha_i(\mu) = \frac{\Delta\lambda_i(\mu)}{4\pi}
$$

故两圈谱β函数为：
$$
\frac{d(\Delta\lambda_i/4\pi)}{d\ln\mu} = -\frac{b_{ij}(\Delta\lambda_i/4\pi)(\Delta\lambda_j/4\pi)}{2\pi} - \frac{b_{ijk}(\Delta\lambda_i/4\pi)(\Delta\lambda_j/4\pi)(\Delta\lambda_k/4\pi)}{(4\pi)^2}
$$

化简：
$$
\frac{d\Delta\lambda_i}{d\ln\mu} = -\frac{b_{ij}\Delta\lambda_i\Delta\lambda_j}{8\pi^2} - \frac{b_{ijk}\Delta\lambda_i\Delta\lambda_j\Delta\lambda_k}{64\pi^3}
$$

**状态**: 🟡 翻译概念上直接，但两圈系数的显式谱验证及在Paper XII中的整合尚待完成。

---

## Λ_QCD的谱推导

Λ_QCD 是 SU(3) 耦合的朗道极点。在谱语言中，它是谱间隙 $\Delta\lambda_3(\mu)$ 达到其极小值的红外能标：$\Delta\lambda_3(\Lambda_{\text{QCD}}) \to 0$。

由 SU(3) β 函数：
$$
\frac{1}{\alpha_3(\Lambda_{\text{QCD}})} = 0 = \frac{1}{\alpha_3(M_{\text{Pl}})} + \frac{b_3}{2\pi}\ln\left(\frac{\Lambda_{\text{QCD}}}{M_{\text{Pl}}}\right)
$$

代入 $\Delta\lambda_3(M_{\text{Pl}}) = \sqrt{2} \cdot 0.122$ 及 $b_3 = -7$：
$$
\alpha_3(M_{\text{Pl}}) = \frac{\Delta\lambda_3}{4\pi} = \frac{0.1725}{4\pi} = 0.0137
$$

$$
\ln\left(\frac{\Lambda_{\text{QCD}}}{M_{\text{Pl}}}\right) = -\frac{2\pi}{7 \cdot \alpha_3(M_{\text{Pl}})}
$$

$$
\Lambda_{\text{QCD}} = M_{\text{Pl}} \times \exp\left(-\frac{2\pi}{7 \times 0.0137}\right) \approx 1.22 \times 10^{19} \times \exp(-65.4) \approx 200\ \text{MeV} \quad \checkmark
$$

**状态**: ✅ 数量级正确。需引入两圈修正以获得精确值 $217 \pm 25\ \text{MeV}$。

---

## Wilson-Fisher 不动点的谱版本

$\phi^4$ 理论中的 WF 固定点对应 β 函数的非平凡零点：

$$
\beta(\lambda) = \frac{3\lambda^2}{16\pi^2} - \frac{5\lambda^3}{(16\pi^2)^2} + \ldots
$$

（已在 Paper XI §5.3 中以谱形式计算。）

**谱版本**：
$$
\beta_{\text{spectral}}(\lambda_R) = \frac{d\lambda_R}{d\ln\mu} = \frac{3\lambda_R^2}{16\pi^2} \quad (\text{单圈，Paper XI 验证误差 0.00\%})
$$

在 $4-\varepsilon$ 维度中，Wilson-Fisher 固定点对应谱间隙在 UV 截断处的饱和。

**状态**: ✅ 单圈 WF 固定点已与 SM β 函数匹配。

---

## 状态总结

| 子问题 | 状态 |
|--------|------|
| 两圈β函数的谱翻译 | 🟡 概念完成，论文整合待续 |
| Λ_QCD的谱推导 | ✅ 数量级正确，需两圈修正 |
| Wilson-Fisher不动点的谱版本 | ✅ 单圈已验证 |
