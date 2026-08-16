# 双星并合 Inspiral 阶段谱分析

**版本**：v0.1（2026-07-25）

**摘要**：本笔记将后牛顿（PN）展开翻译为谱语言，建立双黑洞 inspiral 阶段的谱数值框架。核心成果包括：(1) PN 哈密顿量的谱分解，(2) 辐射功率谱 dE/df 的谱表示，(3) 质量比/自旋对谱的敏感性分析，(4) 与标准 PN 结果的数值验证。

---

## §1 谱 PN 哈密顿量

### 1.1 谱表示原理

后牛顿展开是在弱场、慢运动极限下对广义相对论的逐阶修正，展开参数为 $\varepsilon = (v/c)^2 \sim GM/(rc^2)$。在谱框架中，PN 哈密顿量可表示为谱算子：

$$H_{\text{PN}} = \sum_{n} \lambda_n |\psi_n\rangle\langle\psi_n|$$

其中 $\lambda_n$ 是谱特征值，$|\psi_n\rangle$ 是轨道本征态。Newton 项在轨道角动量基下对角化：

$$\lambda_n^{(0)} = -\frac{\mu M^2}{2n^2}, \quad n = 1, 2, \ldots$$

### 1.2 各阶谱修正

谱 PN 展开系统地将标准 PN 哈密顿量各阶翻译为谱算子的矩阵元：

| PN 阶 | 物理内容 | 谱修正形式 |
|:-----|:--------|:----------|
| 0PN (Newton) | 二体 Kepler 运动 | $E_n = -\mu M^2/(2n^2)$ |
| 1PN | 近日点进动 | $\Delta E_n^{(1)} = E_n \cdot \nu/n^2$ |
| 2PN | 自旋-轨道耦合 | $\Delta E_n^{(2)} = E_n \cdot (\nu^2/n^4 + 2\chi_{\text{eff}}/(n\sqrt{Mr}))$ |
| 3PN | 自旋-自旋耦合 | $\Delta E_n^{(3)} = E_n \cdot (\nu^3/n^6 + \chi^2/(4n^2))$ |

其中 $\nu = \mu/M$ 是对称质量比，$\chi_{\text{eff}}$ 是有效自旋参数。

## §2 谱辐射功率谱

### 2.1 谱 dE/df 公式

引力波辐射功率谱在谱框架中写为 Newton 项与谱修正因子的乘积：

$$\frac{dE}{df} = \frac{\pi}{3} M_c^{5/3} f^{-1/3} \cdot F_{\text{spec}}(f)$$

其中 $F_{\text{spec}}(f)$ 通过 PN 谱能级的导数计算：

$$F_{\text{spec}}(f) = \left|\frac{d\lambda_{\text{PN}}/df}{d\lambda_{\text{Newton}}/df}\right|$$

### 2.2 数值验证

在测试质量（$M = 1 M_{\text{Pl}}$）下：

- **Newton 极限**：0PN 时谱结果与标准 dE/df 精确匹配（相对偏差 $<10^{-15}$）
- **幂律行为**：$\log(dE/df) \propto -\frac{1}{3}\log(f)$，斜率 $-0.3333$ 与理论预期一致
- **谱能级**：PN 哈密顿量的谱能级均为负（束缚态），基态 ($n=1$) 能量最低

### 2.3 天体质量缩放

对于实际天体质量 $M = M_{\odot} \approx 9.14 \times 10^{37} M_{\text{Pl}}$，物理波形可通过以下缩放恢复：

$$f_{\text{phys}} = f_{\text{spec}} / M, \quad \frac{dE}{df}_{\text{phys}} = M^2 \cdot \frac{dE}{df}_{\text{spec}}$$

## §3 参数敏感性分析

### 3.1 质量比影响

谱修正因子 $F_{\text{spec}}$ 对质量比 $q = m_1/m_2$ 的依赖性为：

$$F_{\text{spec}}(q) \approx 1 + \frac{3\nu}{8}\varepsilon + \mathcal{O}(\varepsilon^2)$$

其中 $\nu = q/(1+q)^2$ 对称质量比越小（高 $q$），PN 修正越弱。

### 3.2 自旋影响

自旋-轨道耦合在谱框架中表现为 1.5PN 阶的有效势修正：

$$\chi_{\text{eff}} = \frac{\chi_1 m_1^2 + \chi_2 m_2^2}{m_1^2 + m_2^2}$$

高自旋 ($\chi \to 1$) 显著改变谱能级结构，在接近合并时可产生可观测的谱漂移。

## §4 与标准 PN 理论的对应

### 4.1 对应规则

| 标准 PN 量 | 谱框架对应量 |
|:-----------|:-------------|
| 轨道能量 $E_{\text{orb}}$ | 谱特征值 $\lambda_n$ |
| 轨道相位 $\Phi(t)$ | 谱流 $\phi(t) = \int \lambda(t) dt$ |
| 辐射功率 $P_{\text{GW}}$ | 谱功率 $P_{\text{spec}} = d\lambda/dt$ |
| 波形 $h(t)$ | 谱截面 $\sigma_{\text{spec}}(t)$ |

### 4.2 谱流程

Inspiral 的频率演化由谱流方程控制：

$$\frac{df}{dt} = \frac{P_{\text{GW}}}{dE/df}$$

在谱框架中，$P_{\text{GW}}$ 和 $dE/df$ 均从谱算子导出，无需求解标准 PN 方程，为 Phase 52B（合并阶段谱演化）奠定基础。

---

## §5 开放问题

1. **高阶 PN 谱修正**：4PN 以上谱算子的显式构造（需要保守通量项分离）
2. **偏心轨道谱**：$e \neq 0$ 时需在谐波基矢下重新对角化
3. **数值相对论谱对标**：与 SEOBNR/IMRPhenom 波形的全谱对比

## 关联文件

- `src/dynamic_spectrum/binary_inspiral_spectrum.py` — A1 实现
- `src/dynamic_spectrum/spectral_numerics.py` — C1 基础框架
- `notes/00_foundations/spectral_feynman_rules.md` — 谱 Feynman 规则
- `notes/00_foundations/spectral_path_integral.md` — 谱路径积分
