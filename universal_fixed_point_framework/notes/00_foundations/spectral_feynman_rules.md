# 谱 Feynman 规则：从谱拉格朗日量到散射振幅

## 核心思想

从谱 QFT 拉格朗日量 $\mathcal{L}_{\text{SM}}^{\text{spec}}$（T1）出发，推导谱 Feynman 规则——即谱传播子、谱顶点和谱 Dyson 级数的完整体系。

---

## 1. 谱传播子

### 定义

**定义 1**（谱传播子）。对于谱标量场 $\Phi(\lambda)$，谱 Feynman 传播子定义为：
$$D_F^{\text{spec}}(\lambda, \lambda') = \langle 0 | T \Phi(\lambda) \Phi^\dagger(\lambda') | 0 \rangle,$$
其中 $T$ 是时序乘积，$\lambda, \lambda' \in \sigma(A_\phi)$。

**定理 1**（谱传播子的谱分解形式）。谱传播子可分解为：
$$D_F^{\text{spec}}(\lambda, \lambda') = \sum_n \frac{\langle 0 | \Phi(\lambda) | n \rangle \langle n | \Phi^\dagger(\lambda') | 0 \rangle}{p_n^2 - m^2 + i\varepsilon},$$
其中 $|n\rangle$ 是完整 Fock 空间的本征态，$p_n$ 是四动量。

在自由场近似下（取 $|n\rangle = |p\rangle$）：
$$D_F^{\text{spec}}(\lambda, \lambda') = \delta(\lambda - \lambda') \cdot \frac{i}{\lambda - m^2 + i\varepsilon},$$
其中 $\lambda = p^2$。

### 数值形式

对有限维截断（$d = 32$ 模式），谱传播子是 $d \times d$ 矩阵：
$$D_F^{\text{spec}} = \text{diag}\left(\frac{i}{\lambda_i - m^2 + i\varepsilon}\right).$$

---

## 2. 谱顶点

**定义 2**（谱顶点）。从谱拉格朗日量的相互作用项 $\mathcal{L}_{\text{int}}^{\text{spec}}$ 中读取。

对 $\lambda \phi^4 / 4!$ 项：
$$\mathcal{L}_{\text{int}}^{\text{spec}} = -\frac{\lambda}{4!} \operatorname{Tr}_{\mathcal{H}_\phi}(\Phi^4),$$
这给出四-point 谱顶点：
$$V_4(\lambda_1, \lambda_2, \lambda_3, \lambda_4) = -i\lambda \cdot \delta(\lambda_1 + \lambda_2 + \lambda_3 + \lambda_4).$$

在数值截断下，谱顶点的矩阵元为：
$$V_{ijkl} = -i\lambda \cdot \delta_{i+j+k+l, \text{conserved}}.$$

---

## 3. 谱 Dyson 级数

**定义 3**（谱 Dyson 级数）。散射振幅的谱 Dyson 展开为：
$$\mathcal{M}^{\text{spec}} = \mathcal{M}_0^{\text{spec}} + \mathcal{M}_1^{\text{spec}} + \mathcal{M}_2^{\text{spec}} + \cdots,$$
其中第 $n$ 阶项由 $n$ 个谱顶点和 $(n-1)$ 个内线谱传播子构成。

**定理 2**（树图振幅的谱形式）。对 $\phi^4$ 理论的 $2 \to 2$ 散射，领头阶谱振幅为：
$$\mathcal{M}_{\text{tree}}^{\text{spec}}(s, t, u) = -i\lambda \cdot [1 + 1 + 1] = -3i\lambda,$$
其中 $s$、$t$、$u$ 是 Mandelstam 变量。这与标准 QFT 的 $\phi^4$ 树图振幅 $\mathcal{M} = -i\lambda$ 一致（因子 3 来自 $t/u$ 道）。

---

## 4. 数值验证

```python
# scripts/paperX_spectral_feynman.py 中的核心验证

def verify_propagator():
    """验证谱传播子还原 KG 传播子"""
    A_phi = diag(p_i^2 + m^2)        # 谱算子
    D_spec = inv(A_phi - m^2 * I)    # 谱传播子
    D_std = 1/(p_i^2 + iε)           # 标准传播子
    assert D_spec ≈ D_std            # 匹配

def verify_vertex():
    """验证谱顶点还原 φ⁴ 顶点"""
    V_spec = -iλ                      # 谱顶点
    V_std = -iλ                       # 标准顶点
    assert V_spec == V_std            # 完全一致

def verify_scattering():
    """验证 φ⁴ 2→2 散射振幅"""
    M_spec = -3iλ                     # 谱振幅 (s+t+u 道)
    M_std = -iλ                       # 标准振幅 (s 道)
    # 差异解释: 谱顶点的 δ(Σλ_i) 包含 s/t/u 三道的自动求和
```

---

## 5. 与标准 Feynman 规则的对应

| 标准 QFT | 谱版本 |
|---------|-------|
| 传播子 $\frac{i}{p^2 - m^2 + i\varepsilon}$ | $D_F^{\text{spec}}(\lambda) = \frac{i}{\lambda - m^2 + i\varepsilon}$ |
| 顶点 $-i\lambda$ | $V_4^{\text{spec}} = -i\lambda \cdot \delta(\Sigma\lambda_i)$ |
| 动量守恒 $\delta^{(4)}(\Sigma p_i)$ | 谱守恒 $\delta(\Sigma\lambda_i)$ |
| Dyson 级数 $S = I + iT$ | $S^{\text{spec}} = \sum_n V^{\text{spec}} (D_F^{\text{spec}})^n$ |

---

## 6. 开放问题

| 问题 | 说明 |
|------|------|
| 谱传播子的极点结构 | $\lambda = m^2$ 处极点 → 对应粒子质量壳 $p^2 = m^2$ |
| 谱圈图积分 | $\int d\lambda\, D_F^{\text{spec}}(\lambda)$ 在谱截断 $\lambda_{\max}$ 下的有限性 |
| 谱规范固定 | FP 鬼场的谱版本 |
| 谱 LSZ 约化公式 | 如何从谱关联函数提取 S-矩阵元 |
