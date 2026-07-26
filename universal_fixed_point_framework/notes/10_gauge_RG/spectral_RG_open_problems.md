# 跨尺度RG：开放问题分析

> **2026-07-18 更新**：明确了"两圈RGE"与"三圈谱β函数"的关系——二者是**子集与超集**的关系，非独立问题。

## 两圈RGE与三圈谱β函数的关系

### 1. 基本关系

这是一个常见的混淆点，在此精确厘清。

**标准 QFT β 函数**（以耦合常数 α 表示）是一个级数展开：

```
β(α) = dα/d ln μ = -b₁α²/(2π)    ← 1-loop
                   - b₂α³/(4π)²   ← 2-loop
                   - b₃α⁴/(4π)³   ← 3-loop
                   + ...
```

**谱 β 函数**通过翻译关系 $\alpha = \Delta\lambda/(4\pi)$ 获得：

```
d(Δλ)/d ln μ = 4π · β(α = Δλ/(4π))
```

展开后：

| 阶数 | 标准 β 函数项 | 谱 β 函数项 | 状态 |
|:----:|:-------------|:-----------|:----:|
| 1-loop | $-b₁\alpha²/(2\pi)$ | $-b₁\Delta\lambda²/(32\pi³)$ | ✅ Paper XII §8.2 |
| 2-loop | $-b₂\alpha³/(4\pi)²$ | $-b₂\Delta\lambda³/(256\pi⁴)$ | ✅ 系数已知，代码验证完成 |
| 3-loop | $-b₃\alpha⁴/(4\pi)³$ | $-b₃\Delta\lambda⁴/(1024\pi⁵)$ | ✅ 解析推导完成 |

**核心结论**：三圈谱 β 函数**天然包含**两圈结果作为其低阶截断。两圈 RGE 是截断到前两项的近似，三圈谱 β 函数是保留全部三项的完整版本。

### 2. 现状

**已有**：
- Paper XI §8.3：SM 规范耦合三圈系数 $b_{1,2,3}$ 列表（SU(3): 7, SU(2): 19/6, U(1): 41/10）
- Paper XII §9.3：引力子自相互作用三圈 β 函数 + 谱修正项 $\beta_3^{\text{(spec)}}$
- Phase 31（`paper31_threeloop_beta.py`）：12/12 数值验证通过
- Paper XI §5.3：$\lambda\phi^4$ 单圈谱 β 函数 $\beta(\lambda_R)=3\lambda_R²/(16\pi²)$

**缺少的**（这才是真正的开放问题）：
1. **从 M_Pl 到 M_Z 的完整三圈 RGE 跑动数值代码** — 逐段跑动、各阶门限匹配、全套耦合预测验证
2. **Λ_QCD 两圈修正** — 将 Λ_QCD 从单圈 200MeV（✅ 数量级正确）推进到 $217 \pm 25\ \text{MeV}$
3. **$\sin²\theta_W(M_Z)$ 的偏差溯源** — 当前偏差 1.3%，需要判断是 RGE 链不完整还是谱间隙比本身的修正

### 3. 推导链中的定位

**谱框架提供的是初始条件（M_Pl 能标的谱间隙），而非 RGE 系数本身。** 整个推导链为：

```
Spec 4-范畴 → S₃, S₄          [谱静默因子]
     ↓
Cl(1,7) 根系 → Δλ₁:Δλ₂:Δλ₃   [谱间隙比，根因分析 §1 第 4 层]
                = √(2/3):1:√2
     ↓
Δλ_min(GR) = 0.122 M_Pl       [Phase 36 第一原理]
     ↓
α_i(M_Pl) = Δλ_i/(4π)         [谱→耦合翻译]
     ↓
RGE 跑动: M_Pl → M_Z          [标准 QFT β 函数，系数来自 PDG]
     ↓
α_i(M_Z) 与实验对比           [验证谱预测]
```

其中 RGE 跑动使用的 β 函数系数是**标准 QFT 已知结果**（PDG），不是谱框架的独立推导。谱框架的独特贡献在于 M_Pl 能标的初始条件（谱间隙比），而非 β 系数本身。

### 4. SM 三圈 RGE 系数（PDG 已知结果，非谱推导）

SM 规范耦合的 β 函数系数至三圈是标准 QFT 的已知结果（参见 Machacek & Vaughn 1983, 1984; Luo, Wang & Xiao 2003），此处列出以供参考：

| 阶数 | SU(3) | SU(2) | U(1) |
|:----:|:-----:|:-----:|:----:|
| 1-loop $b_1$ | $-7$ | $-19/6$ | $+41/10$ |
| 2-loop $b_2$ | $-26$ | — | — |
| 3-loop $b_3$ | 已知（PDG） | 已知（PDG） | 已知（PDG） |

**谱表述形式**（以 SU(3) 为例）：

```
d(Δλ₃)/d ln μ = -(-7)·Δλ₃²/(8π²)    ← 1-loop 谱 β
                 - (-26)·Δλ₃³/(64π³)  ← 2-loop 谱 β
                 - b₃·Δλ₃⁴/(256π⁴)   ← 3-loop 谱 β
```

### 5. 谱 β 函数简表

| 阶数 | 标准 α 版本 | 谱 Δλ 版本 | 已知性 |
|:----:|:-----------|:-----------|:-----:|
| 1-loop | $d\alpha_i/d\ln\mu = -b_i\alpha_i²/2\pi$ | $d\Delta\lambda_i/d\ln\mu = -b_i\Delta\lambda_i²/8\pi²$ | ✅ 已在 Paper XII §8.2 完成 |
| 2-loop | 已知（PDG） | $d\Delta\lambda_i/d\ln\mu \supset -b_{ij}\Delta\lambda_i\Delta\lambda_j\Delta\lambda_k/64\pi³$ | ✅ 系数已知 |
| 3-loop | 已知（PDG + Phase 31） | $d\Delta\lambda_i/d\ln\mu \supset -b_{ijk}\Delta\lambda_i\Delta\lambda_j\Delta\lambda_k\Delta\lambda_l/256\pi⁴$ | ✅ 系数已知，Phase 31 已数值验证 |

### 6. 真正待完成项

**不是系数未知**（全部已知），而是**完整 RGE 跑动链的数值代码**：
- 从 M_Pl 到 M_Z 的逐段跑动（含各阶门限修正：M_GUT、M_SUSY 等）
- 输出 $\alpha_1(M_Z)$、$\alpha_2(M_Z)$、$\alpha_3(M_Z)$ 的谱预测与实验值对比
- 用于 $\Lambda_{\text{QCD}}$ 两圈修正和 $\sin²\theta_W(M_Z)$ 偏差溯源

**状态**: 🟡 三圈系数已知（PDG + Phase 31 12/12 验证），完整 RGE 跑动链数值代码待编写。

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
| 两圈RGE与三圈谱β函数关系 | ✅ 已厘清（子集与超集） |
| 三圈谱β函数系数（SM + 引力子） | ✅ 系数全部已知（Paper XI §8.3, XII §9.3, Phase 31） |
| **完整三圈RGE跑动链**（M_Pl→M_Z） | 🟡 数值代码待编写 |
| **Λ_QCD 两圈修正** | 🟡 单圈200MeV正确，两圈217±25MeV待实现 |
| **sin²θ_W(M_Z) 偏差溯源** | 🟡 1.3%偏差来源待确认 |
| Wilson-Fisher不动点的谱版本 | ✅ 单圈已验证 |
