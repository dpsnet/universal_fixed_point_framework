# 谱 AdS/CFT 对应

AdS/CFT 对应是全息原理最重要的具体实现。谱版本将 $A_{\text{GR}}$ 的谱分解与 AdS 边界 CFT 联系起来，揭示谱截断的全息诠释——谱截断 $\Lambda_{\max}$ 提供了边界 CFT 的天然 UV 正则化器。

## 谱 AdS 边界

谱 AdS 空间的边界对应 UV 极限 $\Lambda \to \Lambda_{\max}$：

$$\partial(\text{AdS}_{\text{spec}}) = \left\{ \Lambda = \Lambda_{\max} \right\},$$

其中 $\Lambda$ 是谱 RG 标度，$\Lambda_{\max} = M_{\text{Pl}}$ 是谱截断。该边界是 $\mathbf{Spec}$ 范畴中的谱边界，而非几何边界。

谱 bulk 算符 $A_{\text{bulk}}$ 作用于谱 bulk Hilbert 空间 $\mathcal{H}_{\text{bulk}}$：

$$A_{\text{bulk}} \in \mathbf{Spec}(\mathcal{H}_{\text{bulk}}), \quad A_{\text{bulk}} = \sum_i \lambda_i P_i^{\text{bulk}}.$$

## 谱全息字典

边界 CFT 算符 $\mathcal{O}_{\text{CFT}}(\lambda)$ 是 bulk 谱场的边界值。谱全息对应关系的核心是全息字典：

$$\boxed{Z_{\text{spec}}^{\text{bulk}}[J] = \big\langle \exp\!\big(i\!\int J \cdot \mathcal{O}_{\text{CFT}}\big) \big\rangle_{\text{CFT}}}.$$

其中 $Z_{\text{spec}}^{\text{bulk}}[J]$ 由谱路径积分定义：

$$Z_{\text{spec}}^{\text{bulk}}[J] = \int \prod_{\lambda_i < \Lambda_{\max}} d\Phi_i \; \exp\!\left(i S_{\text{spec}}^{\text{bulk}}[\Phi] + i \sum_i J_i \Phi_i\right).$$

## 谱 GKPW 关系

标准 AdS/CFT 的 Gubser–Klebanov–Polyakov–Witten (GKPW) 关系的谱版本：

$$\boxed{\langle \mathcal{O}(x_1) \cdots \mathcal{O}(x_n) \rangle_{\text{CFT}} = Z_{\text{spec}}^{\text{bulk}}\big[\Phi(\lambda_i) = \lambda_i^{\Delta - d} J_i\big]}.$$

其中 $\Delta$ 是边界 CFT 算符的标度维数，$d$ 是边界时空维数。谱质量 $m$ 与 $\Delta$ 的标准关系保持不变：

$$\Delta(\Delta - d) = m^2 L^2,$$

其中 $L$ 是 AdS 半径。谱修正体现在 $\lambda_i$ 的离散求和替代连续动量积分——UV 边界由 $\lambda_{\max}$ 自然截断。

## 谱 bulk-边界传播子

bulk-边界传播子 $K_{\text{spec}}(\lambda, x)$ 通过 $A_{\text{bulk}}$ 的谱分解表达：

$$K_{\text{spec}}(\lambda, x) = \sum_i \frac{\Delta_{\lambda_i}(x)}{\lambda_i - m^2} \cdot \Pi_i^{\text{bulk}}(x),$$

其中 $\Delta_{\lambda_i}(x)$ 是谱特征函数在边界点 $x$ 的值，$\Pi_i^{\text{bulk}}$ 是谱投影。连续极限下：

$$\lim_{k_{\max} \to \infty} K_{\text{spec}}(\lambda, x) = \int_0^{\Lambda_{\max}} \frac{\rho_{\text{bulk}}(\lambda') \Delta_{\lambda'}(x)}{\lambda' - m^2} d\lambda',$$

其中 $\rho_{\text{bulk}}$ 是 $A_{\text{bulk}}$ 的谱密度。该积分在 UV 端自然截止于 $\Lambda_{\max}$，无需人工截断。

**定理**（标准 AdS/CFT 的谱复现）。在连续极限 $k_{\max} \to \infty$（等价于 $\Lambda_{\max} \to \infty$）下，谱 bulk-边界传播子 $K_{\text{spec}}$ 还原为标准 AdS 的 bulk-边界传播子：

$$\lim_{\Lambda_{\max} \to \infty} K_{\text{spec}}(\lambda, x) = K_{\text{AdS}}(z, x),$$

其中 $K_{\text{AdS}}(z, x) = C_\Delta \left( \frac{z}{z^2 + (x - x')^2} \right)^\Delta$ 是标准 AdS 传播子。

## 谱截断作为 CFT 天然 UV 正则化器

谱截断 $\Lambda_{\max}$ 对边界 CFT 的关键贡献：它为 CFT 关联函数提供天然 UV 正则化。

在标准 AdS/CFT 中，边界 CFT 的短距离行为对应 bulk 中的大动量。谱截断 $\Lambda_{\max}$ 等效于 CFT 的最小长度 $\ell_{\min} \sim 1/\Lambda_{\max} = L_{\text{Pl}}$：

$$\langle \mathcal{O}(x)\mathcal{O}(x') \rangle_{\text{CFT}}^{\text{spec}} \xrightarrow{|x-x'| \to L_{\text{Pl}}} \text{有限},$$

而非标准 CFT 中的 $(x-x')^{-2\Delta}$ 发散。

## 全息 RG 对应

谱 RG 流在 AdS/CFT 框架中获得全息诠释：谱截断 $\Lambda$ 的流动对应 AdS 径向坐标 $z$ 的演化。

| AdS/CFT 概念 | 谱对应 |
|:-----------|:------|
| AdS 径向坐标 $z$ | 谱截断 $\Lambda^{-1}$ |
| UV 边界 $z \to 0$ | $\Lambda \to \Lambda_{\max}$ |
| IR 边界 $z \to \infty$ | $\Lambda \to 0$ |
| bulk 场 $\Phi(z,x)$ | 谱场 $\Phi(\lambda)$ |
| 边界算符 $\mathcal{O}(x)$ | 谱边界值 $\Phi(\Lambda_{\max})$ |
| holographic RG | 谱 Wetterich 方程 |

该对应表明谱量子引力可以作为 AdS/CFT 的 UV 完备版本——谱截断 $\Lambda_{\max}$ 提供了边界 CFT 的天然截止，消除了紫外发散。

---

*摘自 Paper XII §9.4。*
