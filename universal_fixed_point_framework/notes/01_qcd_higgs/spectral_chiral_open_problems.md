# 手征理论：开放问题分析

## Witten 反常的谱表述

SU(2) Witten 反常（$\pi_4(SU(2)) = \mathbb{Z}_2$）意味着奇数个 SU(2) 双态使理论不自洽。其谱表述：大规范变换下 Weyl 费米子的谱流携带 $\mathbb{Z}_2$ 相位。

在 Spec 框架中，Witten 反常对应谱流指标：
$$
\operatorname{ind}(D_{\text{spec}}) \mod 2 \equiv (\#\text{ of SU(2) doublets}) \mod 2
$$

标准模型有 6 个 SU(2) 双态（3 代 × 2）→ 偶数 → $0 \mod 2$ → 无反常。✅ 已在 Paper XI §7.4 验证。

**关键要点**：
- 谱流指标 $\operatorname{ind}(D_{\text{spec}})$ 是 Dirac 算符在紧化时空上的指标定理的谱类比
- $\mathbb{Z}_2$ 相位的出现源于 SU(2) 同伦群 $\pi_4 = \mathbb{Z}_2$ 在谱流上的映射
- 该翻译为理解更高维手征反常提供了谱语言框架

---

## 't Hooft 反常匹配

't Hooft 反常匹配条件要求 UV 理论的 't Hooft 反常与 IR 理论的 't Hooft 反常一致。在谱语言中，这是 UV 和 IR 算符谱流之间的一致性条件。

设 $A_{\text{UV}}$ 为 UV 理论的 't Hooft 反常，$A_{\text{IR}}$ 为 IR 理论的 't Hooft 反常。匹配条件：
$$
A_{\text{UV}} = A_{\text{IR}}
$$

**谱版本的翻译**：
$$
\operatorname{ind}(D_{\text{spec, UV}}) = \operatorname{ind}(D_{\text{spec, IR}})
$$

即，UV 算符总谱流指标必须等于 IR 算符总谱流指标。

**对 QCD 的显式验证**：
- UV 理论：$N_f$ 种无质量夸克 → 't Hooft 反常为 $N_f \times \mathcal{A}_{\text{fund}}$
- IR 理论：若手征对称性自发破缺，Goldstone 玻色子通过 WZW 项携带相同反常
- 谱版本需验证：
  $$
  \sum_{\text{UV fermions}} \operatorname{ind}(D_{\text{spec}}) = \sum_{\text{IR Goldstones}} \operatorname{ind}(D_{\text{spec}})
  $$

**状态**: 🟡 概念翻译已完成，QCD 的显式验证尚待开展。

---

## 谱轴子势的严格推导

轴子势来自瞬子效应。在谱语言中：

$$
V_{\text{spec}}(a) = -\Lambda_{\text{QCD}}^4 \times \cos\left(\frac{a}{f_a}\right) \times S_4^2
$$

其中 $S_4 = e^{-d_H} \approx 0.067$ 是辫子沉默因子（braid silence factor）。

**轴子质量**：
$$
m_a = \frac{\Lambda_{\text{QCD}}^2}{f_a} \times S_4 \approx 6 \times 10^{-5}\ \text{eV}
$$

（来自轴子沉默笔记结果。）

**推导要点**：
- $\Lambda_{\text{QCD}}^4$ 来自 QCD 瞬子幅度的量纲分析
- $\cos(a/f_a)$ 来自 U(1) 轴子对称性的破缺
- $S_4^2$ 是辫子群结构在四维时空中的拓扑压制因子
- 沉默因子 $S_4 = e^{-d_H}$ 中的 $d_H$ 是 Hausdorff 维数

**状态**: ✅ 半定量一致。$f_a$ 的精确值需要进一步确定。

---

## 状态总结

| 子问题 | 状态 |
|--------|------|
| Witten 反常的谱表述 | ✅ 已在 Paper XI §7.4 验证 |
| 't Hooft 反常匹配 | 🟡 概念翻译完成，QCD 显式验证待续 |
| 谱轴子势严格推导 | ✅ 半定量，$f_a$ 精确值待定 |
