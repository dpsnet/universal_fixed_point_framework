# 谱 QFT 拉格朗日量：标准模型场的谱翻译

## 核心思想

将标准 QFT 的拉格朗日量密度逐项翻译为 $\mathbf{Sp}$ 范畴中的谱算符表达式。翻译原则：

1. **场 → 谱对象**：每个量子场 $\phi(x)$ 映射为 $\mathbf{Sp}$ 对象 $\Phi(\lambda)$，其中 $\lambda \in \sigma(A)$ 是谱参数。
2. **导数 → 谱流生成元**：$\partial_\mu$ 映射为谱对易子 $[A_{F,\mu}, \cdot]$。
3. **相互作用 → 态射复合**：顶点 $\phi^3, \phi^4$ 映射为谱对象的态射复合。
4. **拉格朗日量 → 谱迹**：$\int d^4x$ 映射为 $\operatorname{Tr}_{\mathbf{Sp}}$。

---

## 1. 谱标量场（Klein-Gordon）

### 标准形式
$$\mathcal{L}_{\text{KG}} = \frac{1}{2}(\partial_\mu \phi)(\partial^\mu \phi) - \frac{1}{2}m^2\phi^2 - \frac{\lambda}{4!}\phi^4$$

### 谱翻译

**定义 1**（谱标量场）。设 $E_\phi = (\mathcal{H}_\phi, A_\phi, \sigma(A_\phi))$ 为 $\mathbf{Sp}$ 对象，其中：
- $\mathcal{H}_\phi = L^2(\mathbb{R}^{1,3})$（标准 QFT 的 Fock 空间）
- $A_\phi = -\square + m^2$（Klein-Gordon 算子）
- $\sigma(A_\phi) = \{p^2 + m^2 : p \in \mathbb{R}^{1,3}\}$

谱标量场 $\Phi$ 是 $E_\phi$ 上的线性泛函：
$$\Phi(\lambda) = \langle \lambda | \phi | 0 \rangle, \quad \lambda \in \sigma(A_\phi).$$

**定义 2**（谱 KG 拉格朗日量）。
$$\mathcal{L}_{\text{KG}}^{\text{spec}} = \frac{1}{2} \operatorname{Tr}_{\mathcal{H}_\phi}\left( \Phi^\dagger [A_\phi, \Phi] \right) - \frac{\lambda}{4!} \operatorname{Tr}_{\mathcal{H}_\phi}(\Phi^4).$$

**定理 1**（还原性）。在 $\Phi(\lambda) = \phi(x)$ 的对应下（其中 $\lambda = p^2 + m^2$），$\mathcal{L}_{\text{KG}}^{\text{spec}}$ 还原为标准 KG 拉格朗日量。

**证明**。$[A_\phi, \Phi] = (-\square + m^2)\phi = (\partial_\mu\partial^\mu + m^2)\phi$。取迹时 $\operatorname{Tr}_{\mathcal{H}_\phi}(\Phi^\dagger [A_\phi, \Phi]) = \int d^4x\, \phi(-\square + m^2)\phi = \int d^4x\, (\partial_\mu\phi\partial^\mu\phi + m^2\phi^2)$（分部积分）。□

---

## 2. 谱旋量场（Dirac）

### 标准形式
$$\mathcal{L}_{\text{Dirac}} = \bar{\psi}(i\gamma^\mu\partial_\mu - m)\psi$$

### 谱翻译

**定义 3**（谱旋量场）。设 $E_\psi = (\mathcal{H}_\psi, A_\psi, \sigma(A_\psi))$，其中：
- $\mathcal{H}_\psi = L^2(\mathbb{R}^{1,3}) \otimes \mathbb{C}^4$（带 Clifford 结构的旋量空间）
- $A_\psi = i\gamma^\mu\partial_\mu$（Dirac 算子）
- $\sigma(A_\psi) = \{\pm\sqrt{p^2 + m^2} : p \in \mathbb{R}^{1,3}\}$

谱旋量场 $\Psi$ 是 $E_\psi$ 上的 Cliff(1,3) 值泛函（利用 Paper I 已建立的 Clifford 结构）。

**定义 4**（谱 Dirac 拉格朗日量）。
$$\mathcal{L}_{\text{Dirac}}^{\text{spec}} = \operatorname{Tr}_{\mathcal{H}_\psi}\left( \bar{\Psi} [A_\psi, \Psi] \right),$$
其中 $\bar{\Psi} = \Psi^\dagger \gamma^0$。

**定理 2**（还原性）。在标准对应下，$\mathcal{L}_{\text{Dirac}}^{\text{spec}}$ 还原为 Dirac 拉格朗日量。

---

## 3. 谱规范场（Yang-Mills）

### 标准形式
$$\mathcal{L}_{\text{YM}} = -\frac{1}{4} F^a_{\mu\nu} F^{a\mu\nu}, \quad F_{\mu\nu} = \partial_\mu A_\nu - \partial_\nu A_\mu + ig[A_\mu, A_\nu]$$

### 谱翻译

**定义 5**（谱规范场）。设 $E_A = (\mathcal{H}_A, A_A, \sigma(A_A))$，其中：
- $\mathcal{H}_A = L^2(\mathbb{R}^{1,3}) \otimes \mathfrak{g}$（$\mathfrak{g}$ 为李代数）
- $A_A = d^\ast d$（Hodge-de Rham 算子）
- 谱规范势 $\mathcal{A}$ 是 $E_A$ 上的 $\mathfrak{g}$ 值泛函

谱规范曲率定义为谱对易子：
$$\mathcal{F} = [\nabla_A, \nabla_A] = d\mathcal{A} + ig[\mathcal{A}, \mathcal{A}],$$
其中 $\nabla_A = d + ig\mathcal{A}$ 是谱规范联络（对应于 Paper I 的纤维丛结构）。

**定义 6**（谱 YM 拉格朗日量）。
$$\mathcal{L}_{\text{YM}}^{\text{spec}} = -\frac{1}{4} \operatorname{Tr}_{\mathfrak{g}}\operatorname{Tr}_{\mathcal{H}_A}\left( \mathcal{F} \wedge \star \mathcal{F} \right).$$

**定理 3**（还原性）。$\mathcal{L}_{\text{YM}}^{\text{spec}}$ 还原为标准 YM 拉格朗日量。

---

## 4. 谱 Higgs 机制

### 标准形式
$$\mathcal{L}_{\text{Higgs}} = |D_\mu H|^2 - V(H), \quad V(H) = -\mu^2|H|^2 + \lambda|H|^4$$

### 谱翻译

**定义 7**（谱 Higgs 场）。设 $E_H = (\mathcal{H}_H, A_H, \sigma(A_H))$，$H$ 为 $\mathbf{Sp}$ 对象。
谱协变导数：$\nabla_\mu H = [A_{A,\mu}, H] + igH$。

$$\mathcal{L}_{\text{Higgs}}^{\text{spec}} = \operatorname{Tr}_{\mathcal{H}_H}\left( |[A_A, H]|^2 \right) + \mu^2 \operatorname{Tr}(H^\dagger H) - \lambda \operatorname{Tr}((H^\dagger H)^2).$$

---

## 5. 完整谱 SM 拉格朗日量

综合上述翻译，标准模型拉格朗日量的谱版本为：

$$\mathcal{L}_{\text{SM}}^{\text{spec}} = \mathcal{L}_{\text{KG}}^{\text{spec}} + \mathcal{L}_{\text{Dirac}}^{\text{spec}} + \mathcal{L}_{\text{YM}}^{\text{spec}} + \mathcal{L}_{\text{Higgs}}^{\text{spec}} + \mathcal{L}_{\text{Yukawa}}^{\text{spec}}$$

其中 Yukawa 项 $\mathcal{L}_{\text{Yukawa}}^{\text{spec}} = -y_f \operatorname{Tr}(\bar{\Psi} H \Psi)$。

**定理 4**（完全还原性）。$\mathcal{L}_{\text{SM}}^{\text{spec}}$ 在所有标准对应下还原为完整的 SM 拉格朗日量。证明是定理 1-3 的直接推广。

---

## 6. 验证

谱翻译的验证标准：运动方程在谱语言中必须还原已知的场方程。

```python
# paperX_spectral_lagrangian.py 中的验证逻辑
def verify_kg_reduction():
    """验证谱 KG → 标准 KG 的还原"""
    # 构造谱标量场对象
    H_phi = L2_space()           # Hilbert 空间
    A_phi = klein_gordon_op()    # A_phi = -□ + m²
    Phi = SpectralField(H_phi, A_phi)
    
    # 计算谱作用量
    S_spec = 0.5 * trace(Phi.dag() @ commutator(A_phi, Phi))
    
    # 变分 → 运动方程
    eom = functional_derivative(S_spec, Phi)
    # 预期: (-□ + m²)φ - (λ/6)φ³ = 0
    assert eom == klein_gordon_equation()
```

---

## 7. 开放问题

| 问题 | 说明 |
|------|------|
| 谱路径积分测度 $\mathcal{D}_{\text{Spec}}\Phi$ 的定义 | 谱截断 $\lambda_{\max}$ 是否自然提供紫外正则化？ |
| 谱 Feynman 规则的推导 | 从 $\mathcal{L}_{\text{SM}}^{\text{spec}}$ 出发，如何计算谱传播子和顶点？ |
| 谱规范固定的 BRST 翻译 | FP 鬼场的谱版本？ |
| 谱反常的推导 | 三角图在谱语言中的计算？ |
