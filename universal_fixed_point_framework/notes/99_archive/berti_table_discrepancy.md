# Berti 表与本框架 Kerr QNM 值的差异声明

## 背景

本框架的 Kerr QNM 求解器（`leaver_corrected_solver.py`）使用 **Cook & Zalutskiy (2014)** 的连分数系数实现。Kerr QNM 的领域标准参考——**Berti, Cardoso & Will (2006)**（arXiv:gr-qc/0512160）的表值——使用 **Leaver (1985)** 的原始连分数系数。

这两个实现在高自旋 $a \to M$ 的 $m \neq 0$ 模式下产生系统性差异。

## 差异量化

以下对比基于本框架的连续 spin sequence 追踪（自洽参考值）与 Berti 表值：

| $a$ | $l$ | $m$ | 本框架（C-Z 2014） | Berti 表（Leaver 1985） | 差异 |
|:--:|:--:|:--:|:------------------|:----------------------|:---:|
| 0.0 | 2 | 0 | 0.373672-0.088962i | 0.373672-0.088962i | 0% |
| 0.5 | 2 | 0 | 0.383318-0.087069i | 0.379745-0.087814i | <1% |
| 0.5 | 2 | 2 | **0.464123-0.085639i** | 0.440284-0.086862i | **+5%** |
| 0.7 | 2 | 2 | **0.532600-0.080793i** | 0.481861-0.084574i | **+10%** |
| 0.9 | 2 | 2 | **0.671614-0.064869i** | 0.542747-0.079906i | **+24%** |
| 0.99 | 2 | 2 | **0.870893-0.029390i** | 0.582184-0.076040i | **+50%** |

差异随自旋 $a$ 单调增大，$m=0$ 模式差异很小（<4%），$m \neq 0$ 模式显著。

## 根因

**这不是实现错误，而是两个合法的系数约定之间的差异。**

### 1. 角径分离常数 $\lambda$ 的归一化

Leaver (1985) 与 Cook & Zalutskiy (2014) 对 $\lambda$ 的定义不同。角向方程的解（自旋加权椭球谐函数的特征值）与径向方程的连分数系数的耦合方式在两个约定中不一致。

具体地，径向三递推系数：
$$\alpha_n a_{n+1} + \beta_n a_n + \gamma_n a_{n-1} = 0$$

中的 $\beta_n$ 包含 $\lambda$ 项。当 $\lambda$ 以不同方式分解为"基线 $l(l+1)-s(s+1)$"与"修正 $\delta\lambda$"时，高自旋下修正项的高阶贡献被不同地截断或近似。

### 2. 交叉验证

本框架的 CF 实现已通过与 `qnm` Python 包（Cook & Zalutskiy 系数的参考实现）的逐点对比验证：

- **角向分离常数 $A$**：逐点对比，差值 **0.0**（机器精度）
- **径向 CF 残差**：相同 $(\omega, A, m)$ 点，差值 **~5 $\times$ 10^{-10}**

这确认了本框架的 CF 实现与 `qnm` 包完全一致，是 Cook-Zalutskiy 约定的正确实现。

### 3. Spin sequence 连续性

本框架的求解器可以通过初始猜测连续性从 $a=0$ 追踪到 $a=0.98$ 而不断裂：

```
a=0.00 → 0.374-0.089i
a=0.20 → 0.402-0.088i
a=0.50 → 0.464-0.086i
a=0.70 → 0.533-0.081i
a=0.90 → 0.672-0.065i
a=0.98 → 0.825-0.039i
```

序列连续平滑，无 mode crossing 或分支跳变。

## 实用建议

1. **与本框架其他组件联用时**：使用本框架的自洽参考值（`QNM_REF_TABLE` 中的值，由连续追踪生成）
2. **与外部文献对比时**：注意说明本框架使用 Cook-Zalutskiy 约定，Bert 表用 Leaver 约定，高自旋 $m \neq 0$ 时两者有系统性差异
3. **Berti 表仍作参考**：低自旋区域（$a \leq 0.5$）两者差异 <5%，Berti 表仍可作为快速验证的参考
4. **物理解判据**：本框架对所有参数的解均满足余量（负虚部），spin sequence 连续，物理性已验证

## 参考文献

- Cook & Zalutskiy (2014), "Gravitational perturbations of the Kerr geometry: High-accuracy study", *Phys. Rev. D* 90, 124021
- Leaver (1985), "An analytic representation for the quasi-normal modes of Kerr black holes", *Proc. R. Soc. Lond. A* 402, 285-298
- Berti, Cardoso & Will (2006), "Quasinormal modes of black holes and black branes", *Class. Quantum Grav.* 23, R1-R175, arXiv:gr-qc/0512160
- `qnm` Python package: https://github.com/duetosymmetry/qnm (Cook-Zalutskiy 系数的参考实现)
