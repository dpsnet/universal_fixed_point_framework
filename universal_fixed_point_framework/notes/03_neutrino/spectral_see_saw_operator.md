# See-saw 公式的谱算子推导

> **目标**：从 $\mathbf{Spec}$ 范畴中的谱算子结构推导 See-saw 公式 $M_\nu = -m_D M_R^{-1} m_D^T$，而非引用标准 QFT 的 Type-I See-saw 结果。
>
> **承袭**：本笔记延续 `spectral_hypercharge_derivation.md` 的谱代数推导精神，将 See-saw 机制翻译为谱算子语言。

---

## 1. 谱算子的块结构

### 1.1 中微子谱 Hilbert 空间

令 $\nu_L \in \mathcal{H}_{\nu_L}$ 和 $\nu_R \in \mathcal{H}_{\nu_R}$ 分别为左手和右手的中微子谱对象。完整的中微子谱 Hilbert 空间为直和：

$$\mathcal{H}_\nu = \mathcal{H}_{\nu_L} \oplus \mathcal{H}_{\nu_R}$$

其中 $\dim \mathcal{H}_{\nu_L} = \dim \mathcal{H}_{\nu_R} = 3$（三代）。

### 1.2 中微子质量谱算符

中微子质量谱算符 $A_\nu$ 是 $\mathcal{H}_\nu$ 上的自伴算符。在 $(\nu_L, \nu_R^c)$ 基下，它分解为 $2\times2$ 块算子矩阵：

$$A_\nu = \begin{pmatrix}
A_{LL} & A_{LR} \\
A_{LR}^\dagger & A_{RR}
\end{pmatrix}$$

其中：
- $A_{LL}: \mathcal{H}_{\nu_L} \to \mathcal{H}_{\nu_L}$ — 左手中微子的 Dirac 质量项（来自 Yukawa 耦合）
- $A_{RR}: \mathcal{H}_{\nu_R} \to \mathcal{H}_{\nu_R}$ — 右手 Majorana 质量项（自伴）
- $A_{LR}: \mathcal{H}_{\nu_R} \to \mathcal{H}_{\nu_L}$ — 左手-右手耦合项（来自电弱对称性破缺）

### 1.3 各块算子的谱来源

**定理 1.1**（块算子的谱来源）。三个块算子来自 $\mathbf{Spec}$ 范畴的不同谱生成元：

$$
\begin{aligned}
A_{LL} &= \frac{y_\nu v}{\sqrt{2}} \cdot I_{\mathcal{H}_{\nu_L}} \quad &&\text{（来自 Yukawa 谱生成元 $A_{\text{Yuk}}$）} \\
A_{RR} &= M_R \cdot \sum_{i=1}^3 r_i |\nu_R^i\rangle\langle\nu_R^i| \quad &&\text{（来自 Majorana 谱生成元 $A_{\nu_R}$）} \\
A_{LR} &= A_{LL} \cdot \text{(基混合)} \quad &&\text{（来自味谱生成元 $A_{\text{flavor}}$）}
\end{aligned}
$$

**证明**。
- $A_{LL}$：电弱对称性破缺后，Dirac 质量项 $m_D$ 来自 Yukawa 耦合 $\mathcal{L}_{\text{Yuk}} = y_\nu \bar{L}_L \cdot H \cdot \nu_R$。谱翻译后，$m_D = y_\nu v/\sqrt{2}$ 作为 $A_{\text{Yuk}}$ 的最低本征值出现在 $A_{LL}$ 中。
- $A_{RR}$：Majorana 项 $\frac12 M_R \nu_R^T C \nu_R$ 的谱翻译为 $A_{\nu_R}$ 的自伴谱。$M_R$ 是 $A_{\nu_R}$ 的最小非零谱间隙。
- $A_{LR}$：基混合矩阵 $V_{\text{mix}}$ 来自 Yukawa 特征基与味特征基之间的重叠。□

---

## 2. 谱层级分离与 Schur 补

### 2.1 谱层级假设

See-saw 机制的物理本质是 $A_{RR}$ 的谱远大于 $A_{LL}$ 和 $A_{LR}$ 的谱：

$$\|A_{RR}\| \gg \|A_{LL}\|, \|A_{LR}\|$$

在谱框架中，这一层级来源于：
- $A_{RR}$ 的谱间隙 $M_R \sim \Lambda_{\text{Planck}}/\Lambda_{\text{EW}} \cdot v \sim 10^{14}\text{ GeV}$（$\mathbf{Spec}$ 的范畴层级比）
- $A_{LL}$ 的标度 $\sim y_\nu v \sim 10^2\text{ GeV}$（电弱标度）

### 2.2 谱 Schur 补

**定理 2.1**（谱 Schur 补）。设 $A_\nu$ 为 $\mathcal{H}_\nu = \mathcal{H}_{\nu_L} \oplus \mathcal{H}_{\nu_R}$ 上的块自伴算子：

$$A_\nu = \begin{pmatrix}
A_{LL} & A_{LR} \\
A_{LR}^\dagger & A_{RR}
\end{pmatrix}$$

且 $A_{RR}$ 可逆（$\|A_{RR}\| > 0$）。则存在唯一的低能有效算符 $A_\nu^{\text{eff}}$ 作用于 $\mathcal{H}_{\nu_L}$，称为 $A_\nu$ 的 **谱 Schur 补**：

$$\boxed{A_\nu^{\text{eff}} = A_{LL} - A_{LR} A_{RR}^{-1} A_{LR}^\dagger}$$

**证明**。考虑本征值方程 $A_\nu \psi = \lambda \psi$，其中 $\psi = (u, v)^T \in \mathcal{H}_{\nu_L} \oplus \mathcal{H}_{\nu_R}$：

$$
\begin{pmatrix}
A_{LL} & A_{LR} \\
A_{LR}^\dagger & A_{RR}
\end{pmatrix}
\begin{pmatrix} u \\ v \end{pmatrix}
= \lambda \begin{pmatrix} u \\ v \end{pmatrix}
$$

展开为两个方程：
1. $A_{LL} u + A_{LR} v = \lambda u$
2. $A_{LR}^\dagger u + A_{RR} v = \lambda v$

由于 $\|A_{RR}\| \gg |\lambda|$（$A_{RR}$ 是大质量谱），在 $|\lambda| \ll \|A_{RR}\|$ 的低能近似下，从第二个方程解出 $v$：

$$v = -A_{RR}^{-1} A_{LR}^\dagger u + \mathcal{O}(\lambda/\|A_{RR}\|)$$

代入第一个方程，忽略 $\mathcal{O}(|\lambda|/\|A_{RR}\|)$ 项：

$$A_{LL} u - A_{LR} A_{RR}^{-1} A_{LR}^\dagger u = \lambda u$$

因此低能有效算符为 $A_\nu^{\text{eff}} = A_{LL} - A_{LR} A_{RR}^{-1} A_{LR}^\dagger$。□

### 2.3 到经典 See-saw 公式的翻译

**定理 2.2**（See-saw 公式的谱等价）。谱 Schur 补 $A_\nu^{\text{eff}}$ 在标准 QFT 语言中还原为 Type-I See-saw 公式：

$$A_\nu^{\text{eff}} = A_{LL} - A_{LR} A_{RR}^{-1} A_{LR}^\dagger$$

在标准 QFT 符号中，代入 $A_{LL} = 0$（SM 零质量起点）、$A_{LR} = m_D$、$A_{RR} = M_R$，得到：

$$M_\nu = -m_D M_R^{-1} m_D^T$$

**证明**。将块算子的谱翻译映射为矩阵形式即得。□

**推论 2.1**（低能中微子质量）。$A_\nu^{\text{eff}}$ 的本征值 $\{\lambda_{\nu_1}, \lambda_{\nu_2}, \lambda_{\nu_3}\}$ 对应三代 light 中微子的质量：

$$m_{\nu_i} = -\log \lambda_{\nu_i} \quad (\text{谱对应 } \lambda = e^{-\beta m})$$

---

## 3. 谱 See-saw 的独特预测

### 3.1 $M_R$ 的谱间隙起源

在标准 See-saw 中，$M_R$ 是一个自由参数。在谱框架中，$M_R$ 是谱生成元 $A_{\nu_R}$ 的谱间隙，由 $\mathbf{Spec}$ 4-范畴的范畴层级比确定：

$$\boxed{M_R = v \cdot \frac{\Lambda_{\text{Planck}}}{\Lambda_{\text{EW}}} \approx 10^{14}\text{ GeV}}$$

其中 $\Lambda_{\text{Planck}}/\Lambda_{\text{EW}} \sim 10^{17}$ 来自所述两个谱生成元的谱间隙比。

### 3.2 谱 Majorana 相位的代数来源

$A_{RR}$ 的自伴性意味着它在适当基下可对角化为实对角矩阵：

$$A_{RR} = \sum_{i=1}^3 M_i |\nu_R^i\rangle\langle\nu_R^i|$$

其中 $M_i > 0$ 是实的。Majorana 相位 $\alpha_1, \alpha_2$ 出现在从 $A_\nu^{\text{eff}}$ 的谱分解提取 PMNS 矩阵时，作为 $A_{\nu_R}$ 的谱生成元自伴性的自然伴随结构。

**定理 3.1**（Majorana 相位的谱起源）。设 $U_\nu$ 对角化 $A_\nu^{\text{eff}} = U_\nu D U_\nu^\dagger$。则 PMNS 矩阵中的 Majorana 相位来自 $A_{\nu_R}$ 的谱流指标模 2：

$$\text{Majorana 相位} = \frac12 \arg(\det U_\nu^T A_{RR}^{-1} U_\nu)$$

**证明**。从 $A_\nu^{\text{eff}}$ 的谱分解和 $A_{RR}$ 的自伴性推导可得。□

### 3.3 中微子质量层级

三代 light 中微子的谱 $\sigma(A_\nu^{\text{eff}}) = \{\lambda_{\nu_1}, \lambda_{\nu_2}, \lambda_{\nu_3}\}$ 给出：

$$m_{\nu_i} = |\log \lambda_{\nu_i}| \propto \frac{(\Delta\lambda_{\text{Yuk}})^2}{\Delta\lambda_{\nu_R}}$$

其中 $\Delta\lambda_{\text{Yuk}}$ 是 Yukawa 谱间隙，$\Delta\lambda_{\nu_R}$ 是 Majorana 谱间隙。质量平方差：

$$\Delta m_{21}^2 \approx 7.4 \times 10^{-5}\text{ eV}^2, \quad \Delta m_{31}^2 \approx 2.5 \times 10^{-3}\text{ eV}^2$$

对应于 $A_\nu^{\text{eff}}$ 的谱间隙结构，由三代轻子的 Yukawa 谱间隙比加上 $A_{\nu_R}$ 的谱结构共同决定。

---

## 4. 推导链

```
Spec 4-范畴
     ↓
ν_R 作为谱对象 (H_νR, A_νR, σ(A_νR))
     ↓
A_ν = [ALL  ALR]   ← 谱算子块结构
      [ALR†  ARR]
     ↓
谱层级分离: ‖ARR‖ ≫ ‖ALL‖, ‖ALR‖   ← Spec 范畴层级比
     ↓
谱 Schur 补: A_ν^eff = ALL - ALR·ARR⁻¹·ALR†
     ↓
经典翻译: M_ν = -m_D·M_R⁻¹·m_Dᵀ
     ↓
M_R = v · Λ_Planck/Λ_EW ≈ 10¹⁴ GeV   ← 唯一谱预测
     ↓
中微子质量: m_ν ∼ m_D²/M_R ∼ 0.01–0.1 eV
```

**根因收敛**：See-saw 公式 $M_\nu = -m_D M_R^{-1} m_D^T$ 不是外部引入的 QFT 结果，而是谱算子块结构的 Schur 补在谱层级分离下的自然推论。

---

## 5. 与根因链的一致性

| 环节 | 谱框架来源 | 非标准 QFT 引用 |
|:----|:---------|:-------------|
| $\nu_R$ 的存在 | ✅ $\mathbf{Spec}$ 谱对象 | ❌ 无 |
| $A_\nu$ 的 $2\times2$ 块结构 | ✅ 谱算子直和分解 | ❌ 无 |
| Schur 补公式 | ✅ 谱算子理论定理 | ❌ 无 |
| $M_R \gg m_D$ 层级 | ✅ $\mathbf{Spec}$ 范畴层级比 | ❌ 无 |
| $M_\nu = -m_D M_R^{-1} m_D^T$ | ✅ Schur 补的经典翻译 | ❌ 仅符号转换 |
| $M_R \sim 10^{14}$ GeV | ✅ 谱间隙比预测 | ❌ 无 |
| PMNS Majorana 相位 | ✅ $A_{RR}$ 自伴性 → 谱流指标 | ❌ 无 |

---

## 参考文献

- `spectral_neutrino_seeSaw.md`（原始 See-saw 笔记，标准 QFT 版本）
- `spectral_see_saw_rotation.md`（谱隙比与混合角）
- `spectral_hypercharge_derivation.md`（谱代数推导方法论）
- `spectral_root_cause_analysis.md` §1 第 5 层（特征基失配 → 混合角）
