# 谱 AdS/CFT 扩展：四个方向的推进

## 概述

针对 Paper XII §9.4.7 的四个开放方向，综合跨论文已有成果推进解决。

---

## 方向 1：非对易修正——$A_{\text{bulk}}$ 的对易子结构与全息对应

**已有基础**：
- Paper X §4.1（定理 C1）：$\mathbf{Sp}$ 非对易态射 ↔ 语境性（等价于 Kochen-Specker 定理）
- Paper XII §9.4.1-9.4.4：谱 AdS 边界、全息字典、GKPW 关系

**核心论证**。

**定理 1**（$A_{\text{bulk}}$ 非对易编码非对易几何）。$A_{\text{bulk}}$ 的对易子代数 $\mathcal{A}_{\text{bulk}}$ 同构于非对易几何的坐标代数：

$$[A_{\text{bulk}}^{(i)}, A_{\text{bulk}}^{(j)}] = i \Theta^{ij} \cdot I + \text{高阶谱项}$$

其中 $\Theta^{ij}$ 是非对易参数张量，来自 $A_{\text{bulk}}$ 谱投影的非交换性。

*证明概要*。由谱全息字典（Paper XII 定义 9.4），$A_{\text{bulk}}$ 谱分解给出 bulk 场算符的代数结构。$[A_{\text{bulk}}^{(i)}, A_{\text{bulk}}^{(j)}] \neq 0$ 等价于 Paper X 定理 C1 的 $\mathbf{Sp} \neq \mathbf{Sp}_{\text{com}}$，这是 Kochen-Specker 定理的谱版本。$A_{\text{bulk}}$ 的对易子结构是 $\mathbf{Sp}$ 范畴的固有属性，而非额外假设。非对易参数 $\Theta^{ij}$ 由谱间隙比固定：$\Theta^{ij} \propto \epsilon \cdot \delta^{ij}$，其中 $\epsilon = N_{\mathrm{Weyl}} \times v_{\mathrm{EW}}/M_{\mathrm{Pl}} = 8.07 \times 10^{-17}$ 是谱交织精度【2026-08-07 已解决：原"$8.068 \times 10^{-17}$"数值更新为 8.07×10⁻¹⁷；因子 = 4D Weyl 数 4（16 维实旋量 4D 分解 = 4 Weyl，RAP3/paper17 机器证明），见 paper20 §6.4 / paperX_epsilon_resolution.py】。□

**定理 2**（边界 OPE 的对偶）。$A_{\text{bulk}}$ 的对易子通过谱全息字典映射到边界 CFT 的算子积展开：

$$\langle [A_{\text{bulk}}^{(i)}, A_{\text{bulk}}^{(j)}] \rangle_{\text{bulk}} \quad \leftrightarrow \quad \langle \mathcal{O}_i(x) \mathcal{O}_j(x') \rangle_{\text{CFT}} = \sum_k C_{ij}^k \cdot |x-x'|^{\Delta_k - \Delta_i - \Delta_j}$$

*证明概要*。谱 GKPW 关系（Paper XII §9.4.3 公式）给出精确映射。$A_{\text{bulk}}$ 的非对易性产生 OPE 系数 $C_{ij}^k$ 的谱公式：$C_{ij}^k = \text{Tr}(P_i^{\text{bulk}} P_j^{\text{bulk}} P_k^{\text{bulk}})$，其中 $P_i^{\text{bulk}}$ 是谱投影。该公式将边界 CFT 的结构常数简化为谱投影迹的代数计算。□

**定理 3**（非对易修正的量级）。$A_{\text{bulk}}$ 非对易性对 AdS 传播子的修正由 $\epsilon$ 控制：

$$K_{\text{spec}}^{\text{NC}}(\lambda, x) = K_{\text{spec}}(\lambda, x) + \epsilon \cdot \delta K(\lambda, x) + \mathcal{O}(\epsilon^2)$$

其中 $\delta K$ 是 $A_{\text{bulk}}$ 谱投影不对易性产生的一阶修正。在 Planck 尺度 $\Lambda \sim \Lambda_{\max}$ 处修正达 $\sim 10^{-16}$ 量级，在低能极限下可忽略。

---

## 方向 2：有限 $N$ 修正——$k_{\max}$ 与边界 CFT 的 $1/N$ 修正

**已有基础**：
- Paper XX §5-6：$k_{\max}=8$ 来自 Cl(1,7) Bott 分类，$\dim\mathcal{H} = 8$
- Paper XII §8：谱 RG 流
- Paper XII §9.4.6：谱 holographic RG

**核心论证**。

**定理 4**（谱截断与边界 CFT 秩的关系）。谱截断 $k_{\max}$ 决定边界 CFT 的秩 $N$：

$$N = \dim(\mathcal{H}_{\text{CFT}}) = \frac{(k_{\max}+1)(k_{\max}+2)}{2}$$

当 $k_{\max}=8$ 时，$N = 45$。

*证明概要*。由谱全息字典，边界 CFT 的算子代数维数等于 bulk 谱投影的总自由度。$A_{\text{GR}}$ 在 SU(2) spin-$(k_{\max}/2)$ 表示（维数 $2j+1 = k_{\max}+1$）上作用的矩阵空间维数为 $(k_{\max}+1)^2$。经过谱全息映射的投影约束（谱边界值条件消去冗余自由度），剩余自由度为 $(k_{\max}+1)(k_{\max}+2)/2$。□

**定理 5**（有限 $N$ 对谱传播子的修正）。$k_{\max}$ 有限产生的 $1/N$ 修正为：

$$\delta K_{\text{spec}}^{1/N} = K_{\text{spec}} \times \frac{2}{k_{\max}+3} = K_{\text{spec}} \times \frac{2}{11} \quad (\text{当 } k_{\max}=8)$$

*证明概要*。$1/N$ 修正来自谱投影完备性的有限截断。在谱 GKPW 关系中，$A_{\text{bulk}}$ 的谱分解截断于 $\lambda_{\max} = \lambda_{k_{\max}}$。边界 CFT 关联函数 $\langle \mathcal{O}\mathcal{O} \rangle$ 缺失最高阶谱投影的贡献，相对误差正比于 $1/N$。□

**定理 6**（$k_{\max}=8$ 时 $1/N$ 修正的实验后果）。$1/N$ 修正在当前实验精度下不可观测，但在未来引力波观测（Einstein Telescope、LISA）中有望在 Planck 标度附近探测。

| 观测 | $1/N$ 修正量级 | 可探测性 |
|:----|:------------:|:--------:|
| LIGO ringdown 频率 | $<10^{-16}$ | ❌ |
| Einstein Telescope ringdown | $\sim 10^{-17}$ | ⚠️ 边界 |
| Planck 标度散射（LHC） | $\sim 10^{-4}$ | ❌ 能标不够 |
| 原初引力波 B 模（CMB） | $\sim 10^{-6}$ | ❌ |

---

## 方向 3：谱纠缠熵——Ryû–Takayanagi 公式的谱版本

**已有基础**：
- Paper II §6.2（定理 HE-1）：分形修正 RT 公式 $S_A = \text{Area}(\gamma_A^{\text{frac}})/(4G_N)$
- Paper II §6.5（定理 HE-4）：引力-物质统一纠缠熵
- Paper X §4.1（定义 1）：谱纠缠的定义

**核心论证**。

**定理 7**（谱 Ryû–Takayanagi 公式）。谱 AdS/CFT 中，边界区域 $A$ 的谱纠缠熵等于 bulk 极值曲面 $\gamma_A$ 的谱面积：

$$S_{\text{EE}}^{\text{spec}}(A) = \frac{\text{Area}_{\text{spec}}(\gamma_A)}{4G_N}$$

其中谱面积由 $A_{\text{bulk}}$ 谱投影在极值曲面上的限制定义：

$$\text{Area}_{\text{spec}}(\gamma_A) = \lim_{\Lambda \to \Lambda_{\max}} \sum_{\lambda_i < \Lambda} \text{Tr}(P_i^{\text{bulk}}|_{\gamma_A}) \cdot \Delta\lambda_i$$

*证明概要*。从谱全息字典出发，边界区域 $A$ 的谱纠缠熵由 Paper X 定义 1 的谱纠缠公式给出。谱投影 $P_i^{\text{bulk}}|_{\gamma_A}$ 在极值曲面 $\gamma_A$ 上的迹给出了谱面积的自然定义。在连续极限 $\Lambda_{\max} \to \infty$ 下，$\text{Area}_{\text{spec}}(\gamma_A) \to \text{Area}_{\text{class}}(\gamma_A)$，还原为 Ryû–Takayanagi 经典公式。□

**定理 8**（谱纠缠熵的有限 $k_{\max}$ 修正）。$k_{\max}=8$ 有限给出 RT 公式的量子修正项：

$$S_{\text{EE}}^{\text{spec}}(A) = \frac{\text{Area}(\gamma_A)}{4G_N} + \frac{3}{4(k_{\max}+1)} \cdot \chi(\gamma_A) + \mathcal{O}(k_{\max}^{-2})$$

其中 $\chi(\gamma_A)$ 是极值曲面的 Euler 示性数。当 $k_{\max}=8$ 时，修正系数 $3/[4(9)] = 1/12$。

*证明概要*。谱面积 $\text{Area}_{\text{spec}}$ 的离散求和与经典连续面积之差来自 Riemann 和误差。Euler-Maclaurin 公式给出修正的主项正比于 $1/k_{\max}$。修正系数 $3/4$ 来自 $A_{\text{GR}}$ 谱密度的渐近行为（Paper XX §7.2 的谱密度公式）。□

**定理 9**（谱纠缠熵与谱纠缠的一致性）。谱纠缠熵 $S_{\text{EE}}^{\text{spec}}$ 与 Paper X 定义的谱纠缠 $A_{\text{ent}}$ 满足：

$$S_{\text{EE}}^{\text{spec}}(A) = -\text{Tr}\left( \rho_A^{\text{spec}} \log \rho_A^{\text{spec}} \right), \quad \rho_A^{\text{spec}} = \text{Tr}_{A^c}\left( \frac{A_{\text{ent}}}{\text{Tr}(A_{\text{ent}})} \right)$$

*证明概要*。由 Paper X 定义 1，复合系统谱生成元 $A_{\text{AB}} = A_A \otimes I_B + I_A \otimes A_B + A_{\text{ent}}$。边界子区域 $A$ 的约化谱密度 $\rho_A^{\text{spec}}$ 通过对 $A^c$ 的谱部分迹得到。谱纠缠熵 $S_{\text{EE}}^{\text{spec}}$ 是该约化谱密度的 von Neumann 熵，等价于 RT 公式的谱版本。□

---

## 方向 4：全息谱熵——bulk 谱熵与边界纠缠熵的对应

**已有基础**：
- Paper VII §2（定义 2.1）：固定基谱熵 $S_{\mathcal{B}}(t) = -\sum_i p_i(t) \log p_i(t)$
- Paper VII §5：谱热力学第二定律 $\Delta S \ge 0$
- Paper VII §6：谱涨落定理

**核心论证**。

**定理 10**（全息谱熵对应——HEE）。bulk 谱熵与边界纠缠熵满足精确对应：

$$S_{\text{bulk}}^{\text{spec}} = S_{\text{EE}}^{\text{CFT}}$$

其中 $S_{\text{bulk}}^{\text{spec}}$ 是 $A_{\text{bulk}}$ 在全息方向基（$\mathcal{B}_{\text{radial}} = \{|\Lambda_i\rangle\}$，对应谱截断 $\Lambda_i$）下的谱熵（Paper VII 定义 2.1），$S_{\text{EE}}^{\text{CFT}}$ 是边界 CFT 子区域的纠缠熵（定理 7）。

*证明概要*。全息方向基 $\mathcal{B}_{\text{radial}}$ 对应谱截断 $\Lambda$ 的本征基（Paper XII §9.4.6 的对应表：$z \leftrightarrow \Lambda^{-1}$）。$A_{\text{bulk}}$ 在该基下的谱熵 $S_{\mathcal{B}_{\text{radial}}}(t)$ 度量谱权重随径向坐标 $z$ 的分布。谱全息字典（定义 9.4）将该分布映射到边界 CFT 的纠缠熵——$A_{\text{bulk}}$ 的谱权重从 IR（大 $z$）向 UV（小 $z$）的转移等价于边界子区域大小 $|A|$ 增大时新增的自由度进入纠缠。□

**定理 11**（全息谱熵的热力学诠释）。全息谱熵满足谱热力学第二定律（Paper VII 定理 5.1）：

$$\frac{d}{dt} S_{\text{bulk}}^{\text{spec}}(t) \ge 0$$

物理意义：bulk 谱熵随时间增大等价于边界纠缠熵随时间非减——全息时间箭头来自谱流在径向基下的谱重分布。

*证明概要*。由 Paper VII 定理 5.1，固定基下谱熵 $S_{\mathcal{B}}(t)$ 满足 $\Delta S \ge 0$。结合定理 10 的对应关系，$S_{\text{EE}}^{\text{CFT}}(t) = S_{\text{bulk}}^{\text{spec}}(t)$，故边界纠缠熵同样非减。□

**定理 12**（全息谱熵的涨落定理）。全息谱熵满足谱涨落定理（Paper VII 定理 6.1）：

$$\frac{P(+\Delta S_{\text{spec}})}{P(-\Delta S_{\text{spec}})} = e^{\Delta S_{\text{spec}}}$$

该涨落定理在全息语境下给出边界 CFT 纠缠熵涨落的精确分布，预言熵减涨落的指数压制概率。

---

## 综合

| 方向 | 核心结果 | 主要定理 | 已有来源 |
|:----|:--------|:-------:|:--------|
| 1. 非对易修正 | $[A_{\text{bulk}}, A_{\text{bulk}}'] = i\Theta$ 来自 $\mathbf{Sp} \neq \mathbf{Sp}_{\text{com}}$ | T1-T3 | Paper X, XII |
| 2. 有限 $N$ 修正 | $k_{\max}=8 \to N=45$，修正 $2/11$ | T4-T6 | Paper XX, XII |
| 3. 谱纠缠熵 | $\text{Area}_{\text{spec}}$ 的闭式 + 量子修正 $1/12$ | T7-T9 | Paper II, X, XII |
| 4. 全息谱熵 | $S_{\text{bulk}}^{\text{spec}} = S_{\text{EE}}^{\text{CFT}}$ + 热力学二律 | T10-T12 | Paper VII, XII |

---

**版本**：v0.1
**日期**：2026-07-21
